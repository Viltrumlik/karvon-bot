"""End-to-end: the real aiogram Dispatcher polls a local fake Telegram Bot API (no real token)."""
from __future__ import annotations

import asyncio
import re

import pytest

from karvon.bot.app import build_bot, build_dispatcher
from karvon.i18n import t
from karvon.storage import Storage
from tests.fake_telegram import FakeTelegram

USER = 777001


def plain(html: str) -> str:
    return re.sub(r"<[^>]+>", "", html)


def pick_choice(actions: list[str]) -> str:
    """Prefer the cautious answer (never sell out to Qorabek in this test)."""
    events = [a for a in actions if a.startswith("ev:")]
    for safe in ("ev:refuse", "ev:decline", "ev:pass", "ev:note", "ev:trade", "ev:look", "ev:keep"):
        if safe in events:
            return safe
    return events[-1]


class Harness:
    def __init__(self, fake: FakeTelegram, user_id: int, lang: str) -> None:
        self.fake = fake
        self.user = user_id
        self.lang = lang

    @property
    def msg(self):
        m = self.fake.current(self.user)
        assert m is not None, "the bot has not sent anything yet"
        return m

    def actions(self) -> list[str]:
        return [data.split("|", 1)[1] for _, data in self.msg.buttons()]

    async def press(self, action: str) -> str:
        msg = self.msg
        data = next((d for _, d in msg.buttons() if d.split("|", 1)[1] == action), None)
        assert data is not None, f"{action!r} not in {self.actions()}\n{plain(msg.text)}"
        cb = self.fake.press(self.user, msg.message_id, data, self.lang)
        assert await self.fake.wait_callback_answered(cb), f"callback for {action} not answered"
        return plain(self.msg.text)

    async def command(self, text: str) -> str:
        before = len(self.fake.calls)
        self.fake.send_text(self.user, text, self.lang)
        assert await self.fake.wait_for(
            lambda: any(m == "sendMessage" for m, _ in self.fake.calls[before:]), timeout=5
        ), f"no reply to {text}"
        await self.fake.wait_idle()
        return plain(self.msg.text)


@pytest.fixture
async def running(tmp_path):
    fake = FakeTelegram()
    base = await fake.start()
    db = Storage(str(tmp_path / "e2e.db"))
    bot = build_bot(fake.token, base)
    dp = build_dispatcher(db, seed_fn=lambda: 20241109)
    task = asyncio.create_task(dp.start_polling(bot, handle_signals=False, polling_timeout=1))
    assert await fake.wait_for(lambda: any(m == "getUpdates" for m, _ in fake.calls), timeout=10)
    try:
        yield fake, db
    finally:
        await dp.stop_polling()
        await asyncio.wait_for(task, timeout=10)
        await fake.stop()
        db.close()


@pytest.mark.parametrize("lang", ["uz", "en"])
async def test_full_journey(running, lang):
    fake, db = running
    h = Harness(fake, USER, lang)

    # /start -> language picker with the user's language preselected
    text = await h.command("/start")
    assert t("en", "lang.prompt") in text and t("uz", "lang.prompt") in text
    first_label = h.msg.buttons()[0][0]
    assert first_label.startswith("✅") and h.actions()[0] == f"L:{lang}"
    game_msg = h.msg.message_id

    # pick the language -> main menu (same message edited in place)
    text = await h.press(f"L:{lang}")
    assert h.msg.message_id == game_msg and h.msg.edits >= 1
    assert plain(t(lang, "menu.text")).splitlines()[0] in text
    assert fake.callback_answers[fake.sent_callbacks[-1]].get("text") == t(lang, "lang.saved")

    # new game on Hard -> Samarkand hub with Ravshan's welcome tip
    await h.press("new")
    text = await h.press("df:hard")
    assert t(lang, "city.sam") in text and "📅 1/100" in text
    assert plain(t(lang, "tip.prefix")) in text

    # market -> paper -> buy 5
    text = await h.press("mk")
    assert plain(t(lang, "mk.title", city="sam")) in text
    await h.press("g:paper")
    text = await h.press("b:paper:5")
    assert plain(t(lang, "ok.bought", good="paper", n=5, money=0)).split(",")[0].split("×")[0] in text
    assert "📦 5/40" in text

    # travel to Bukhara
    await h.press("mk")
    await h.press("h")
    await h.press("tr")
    text = await h.press("tc:buk")
    assert t(lang, "city.buk") in text
    text = await h.press("go:buk")
    assert plain(t(lang, "ok.departed", city="buk")) in text
    assert "nd" in h.actions() and "ro" in h.actions()

    # advance day by day until an event or arrival; every press must change the message
    for _ in range(12):
        before = h.msg.text
        text = await h.press("nd")
        assert h.msg.text != before
        acts = h.actions()
        if any(a.startswith("ev:") for a in acts) or "mk" in acts:
            break
    acts = h.actions()
    if any(a.startswith("ev:") for a in acts):
        # resolve the event: the result screen shows the outcome and a Continue button
        choice = pick_choice(acts)
        text = await h.press(choice)
        assert h.actions() == ["ok"]
        text = await h.press("ok")
        acts = h.actions()
    # ride on until we are in Bukhara (resolving any further events with their first choice)
    for _ in range(20):
        if "mk" in acts:
            break
        if any(a.startswith("ev:") for a in acts):
            await h.press(pick_choice(acts))
            await h.press("ok")
        elif "ro" in acts:
            await h.press("ro")
        acts = h.actions()
    assert "mk" in acts, "never arrived in Bukhara"
    assert t(lang, "city.buk") in plain(h.msg.text)

    # all callbacks were answered and the whole game happened in ONE message
    await fake.wait_idle()
    assert not fake.unanswered_callbacks()
    assert h.msg.message_id == game_msg
    assert not fake.unknown_methods
    assert set(fake.commands) >= {"", "uz", "ru", "en"}

    # the session survived in SQLite
    rec = db.load_player(USER)
    assert rec and rec["lang"] == lang and rec["state"]["game"]["city"] == "buk"


async def test_stale_buttons_and_commands(running):
    fake, db = running
    h = Harness(fake, USER + 1, "ru")
    await h.command("/start")
    await h.press("L:ru")
    await h.press("new")
    await h.press("df:normal")
    hub_msg = h.msg
    old_data = hub_msg.buttons()[0][1]  # "mk" with the current seq
    await h.press("st")  # go to the stable: the seq changes

    # pressing the outdated "market" button must not trade or crash: it re-renders the current screen
    cb = fake.press(h.user, hub_msg.message_id, old_data, "ru")
    assert await fake.wait_callback_answered(cb)
    assert fake.callback_answers[cb]["text"] == t("ru", "stale")
    assert "cb" in h.actions()  # still on the stable screen

    # garbage callback data is answered too
    cb = fake.press(h.user, hub_msg.message_id, "nonsense", "ru")
    assert await fake.wait_callback_answered(cb)

    # /status sends a fresh game message and removes the old one
    old_id = h.msg.message_id
    text = await h.command("/status")
    assert h.msg.message_id != old_id
    assert await fake.wait_for(lambda: fake.messages[(h.user, old_id)].deleted, timeout=5)
    assert fake.messages[(h.user, old_id)].deleted
    assert plain(t("ru", "stt.title")) in text

    # free text re-sends the current screen with a hint
    text = await h.command("привет")
    assert t("ru", "use_buttons") in text

    # /restart asks for confirmation, /top and /help work, /lang reopens the picker
    text = await h.command("/restart")
    assert t("ru", "restart.text") in text
    text = await h.command("/top")
    assert plain(t("ru", "top.title")) in text
    text = await h.command("/help")
    assert "/start" in text
    text = await h.command("/lang")
    assert h.actions()[0] == "L:ru"
    await fake.wait_idle()
    assert not fake.unanswered_callbacks()


async def test_edit_failure_falls_back_to_new_message(running):
    fake, db = running
    h = Harness(fake, USER + 2, "en")
    await h.command("/start")
    await h.press("L:en")
    msg = h.msg
    data = msg.buttons()[0][1]
    msg.deleted = True  # the user deleted the game message; the bot can no longer edit it
    cb = fake.press(h.user, msg.message_id, data, "en")
    assert await fake.wait_callback_answered(cb)
    assert h.msg.message_id != msg.message_id  # a new message was sent instead
    assert db.load_player(h.user)["msg_id"] == h.msg.message_id


async def test_double_tap_is_serialised(running):
    fake, db = running
    h = Harness(fake, USER + 3, "en")
    await h.command("/start")
    await h.press("L:en")
    await h.press("new")
    await h.press("df:hard")
    await h.press("mk")
    await h.press("g:paper")
    msg = h.msg
    data = next(d for _, d in msg.buttons() if d.endswith("|b:paper:5"))
    cb1 = fake.press(h.user, msg.message_id, data, "en")
    cb2 = fake.press(h.user, msg.message_id, data, "en")  # same button twice, before any re-render
    assert await fake.wait_callback_answered(cb1) and await fake.wait_callback_answered(cb2)
    state = db.load_player(h.user)["state"]["game"]
    assert state["cargo"] == {"paper": 5}  # bought once; the second tap was stale
