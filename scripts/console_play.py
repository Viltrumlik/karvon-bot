#!/usr/bin/env python3
"""Play Karvonboshi in the terminal, without a Telegram token.

It starts the in-process fake Bot API (tests/fake_telegram.py) and the *real* bot polling it,
then acts as the Telegram user:

    python scripts/console_play.py                 # interactive; language picked in the game
    python scripts/console_play.py --lang ru       # pretend the Telegram client is Russian
    python scripts/console_play.py --auto 300 --lang uz   # random button presses, smoke test

Interactive: each bot message is printed (HTML stripped) with numbered buttons.
Type a number to press that button; any other text is sent as a chat message (/start, /status ...);
"q" quits. In --auto mode the script exits non-zero on any bot error.
"""
from __future__ import annotations

import argparse
import asyncio
import html
import logging
import os
import random
import re
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from karvon.bot.app import build_bot, build_dispatcher  # noqa: E402
from karvon.storage import Storage  # noqa: E402
from tests.fake_telegram import FakeTelegram  # noqa: E402

USER_ID = 4242
COMMANDS = ["/start", "/status", "/help", "/top", "/lang", "/restart", "hello"]
BENIGN_API_ERRORS = ("message is not modified", "message to edit not found")


class ErrorCollector(logging.Handler):
    def __init__(self) -> None:
        super().__init__(level=logging.ERROR)
        self.records: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record)


def plain(text: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def show(fake: FakeTelegram) -> None:
    msg = fake.current(USER_ID)
    if msg is None:
        print("(no message yet)")
        return
    print("\n" + "─" * 60)
    print(plain(msg.text))
    buttons = msg.buttons()
    if buttons:
        print()
        for i, (label, _) in enumerate(buttons, 1):
            print(f"  [{i}] {label}")
    print("─" * 60)


async def start_stack(db_path: str, seed: int | None):
    fake = FakeTelegram()
    base = await fake.start()
    db = Storage(db_path)
    bot = build_bot(fake.token, base)
    dp = build_dispatcher(db, seed_fn=(lambda: seed) if seed is not None else None)
    task = asyncio.create_task(dp.start_polling(bot, handle_signals=False, polling_timeout=1))
    await fake.wait_for(lambda: any(m == "getUpdates" for m, _ in fake.calls), timeout=10)
    return fake, db, dp, task


async def stop_stack(fake: FakeTelegram, db: Storage, dp, task) -> None:
    await dp.stop_polling()
    try:
        await asyncio.wait_for(task, timeout=10)
    finally:
        await fake.stop()
        db.close()


async def settle(fake: FakeTelegram, timeout: float = 10.0) -> bool:
    ok = await fake.wait_idle(timeout)
    await asyncio.sleep(0.02)  # let a trailing deleteMessage / edit land
    return ok


async def interactive(args) -> int:
    fake, db, dp, task = await start_stack(args.db, args.seed)
    try:
        fake.send_text(USER_ID, "/start", args.lang)
        await settle(fake)
        show(fake)
        while True:
            try:
                line = (await asyncio.to_thread(input, "> ")).strip()
            except (EOFError, KeyboardInterrupt):
                break
            if line.lower() in ("q", "quit", "exit"):
                break
            if not line:
                show(fake)
                continue
            msg = fake.current(USER_ID)
            if line.isdigit() and msg is not None:
                buttons = msg.buttons()
                idx = int(line) - 1
                if not 0 <= idx < len(buttons):
                    print(f"No button {line}.")
                    continue
                fake.press(USER_ID, msg.message_id, buttons[idx][1], args.lang)
            else:
                fake.send_text(USER_ID, line, args.lang)
            await settle(fake)
            show(fake)
    finally:
        await stop_stack(fake, db, dp, task)
    return 0


async def auto(args) -> int:
    collector = ErrorCollector()
    logging.getLogger().addHandler(collector)
    rng = random.Random(args.seed if args.seed is not None else 1)
    fake, db, dp, task = await start_stack(args.db, args.seed)
    problems: list[str] = []
    presses = commands = 0
    try:
        fake.send_text(USER_ID, "/start", args.lang)
        if not await settle(fake):
            problems.append("no answer to /start")
        for step in range(args.auto):
            msg = fake.current(USER_ID)
            buttons = msg.buttons() if msg else []
            if not buttons or rng.random() < args.command_rate:
                fake.send_text(USER_ID, rng.choice(COMMANDS), args.lang)
                commands += 1
            else:
                weights = [1.0 if args.uniform else weight(d) for _, d in buttons]
                _, data = rng.choices(buttons, weights=weights)[0]
                fake.press(USER_ID, msg.message_id, data, args.lang)
                presses += 1
            if not await settle(fake):
                problems.append(f"step {step}: bot did not finish handling the update in time")
                break
            msg = fake.current(USER_ID)
            if msg is not None and len(plain(msg.text)) > 4096:
                problems.append(f"step {step}: message longer than 4096 characters")
            if args.verbose:
                show(fake)
        if fake.unanswered_callbacks():
            problems.append(f"unanswered callbacks: {fake.unanswered_callbacks()}")
        if fake.unknown_methods:
            problems.append(f"unknown Bot API methods: {sorted(set(fake.unknown_methods))}")
        bad_api = [e for e in fake.api_errors if not any(b in e[1] for b in BENIGN_API_ERRORS)]
        if bad_api:
            problems.append(f"Bot API errors: {bad_api[:5]}")
        long_buttons = [
            d for m in fake.messages.values() for _, d in m.buttons() if len(d.encode("utf-8")) > 64
        ]
        if long_buttons:
            problems.append(f"callback_data over 64 bytes: {long_buttons[:3]}")
        endings_seen = db_endings(db)
        rec = db.load_player(USER_ID)
        state = (rec or {}).get("state", {})
        game = state.get("game") or {}
    finally:
        await stop_stack(fake, db, dp, task)
        logging.getLogger().removeHandler(collector)
    for r in collector.records:
        problems.append(f"log {r.levelname} {r.name}: {r.getMessage()}")
    print(
        f"auto lang={args.lang} steps={args.auto} presses={presses} commands={commands} "
        f"edits={sum(m.edits for m in fake.messages.values())} messages={len(fake.messages)} "
        f"finished_runs={db_runs_count(args.db)} last_screen={state.get('screen')} "
        f"game_day={game.get('day')} api_errors={len(fake.api_errors)} endings={endings_seen}"
    )
    if problems:
        print("PROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    print("OK: no errors")
    return 0


PROGRESS = ("ev:", "ok", "go:", "tc:", "tr", "ro", "nd", "df:", "new", "cont", "L:", "b:", "bm:", "sa:", "g:", "mk", "h")


def weight(data: str) -> float:
    """Bias random presses towards buttons that move the game forward (so roads, events and endings
    get exercised), while every visible button can still be pressed."""
    action = data.split("|", 1)[-1]
    if action in ("menu", "lang", "help", "top", "tips", "ry"):
        return 0.3
    return 4.0 if action.startswith(PROGRESS) else 1.0


def db_endings(db: Storage) -> dict[str, int]:
    rows = db._conn.execute("SELECT ending, COUNT(*) FROM runs GROUP BY ending ORDER BY ending").fetchall()
    return {r[0]: r[1] for r in rows}


def db_runs_count(path: str) -> int:
    try:
        db = Storage(path)
        try:
            return db.runs_count()
        finally:
            db.close()
    except Exception:
        return -1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Play Karvonboshi in the terminal (no Telegram token needed).")
    ap.add_argument("--lang", default="en", choices=["uz", "ru", "en"], help="the fake Telegram client language")
    ap.add_argument("--auto", type=int, default=0, metavar="N", help="press N random buttons and exit")
    ap.add_argument("--seed", type=int, default=None, help="game seed (and random-press seed in --auto)")
    ap.add_argument("--db", default=None, help="SQLite file (default: a temporary file)")
    ap.add_argument("--command-rate", type=float, default=0.04, help="--auto: chance to send a command instead")
    ap.add_argument("--verbose", action="store_true", help="--auto: print every screen")
    ap.add_argument("--uniform", action="store_true", help="--auto: pick buttons uniformly (no progress bias)")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s")
    tmp = None
    if args.db is None:
        tmp = tempfile.TemporaryDirectory(prefix="karvon-console-")
        args.db = os.path.join(tmp.name, "console.db")
    try:
        return asyncio.run(auto(args) if args.auto else interactive(args))
    finally:
        if tmp is not None:
            tmp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
