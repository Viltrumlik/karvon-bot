"""aiogram handlers: commands, free text and inline-button callbacks."""
from __future__ import annotations

import logging
import random
from typing import Any, Callable

from aiogram import Bot, F, Router
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message, User

from .. import engine as E
from ..engine import data as D
from ..i18n import LANGS, norm_lang, t
from ..storage import Storage
from .keyboards import build, parse
from .render import render
from .session import Session, UserLocks

log = logging.getLogger("karvon.bot")

NAV_SCREENS = {
    "mk": "market",
    "st": "stable",
    "gu": "guards",
    "pr": "prov",
    "inn": "inn",
    "tea": "tea",
    "ln": "lender",
    "co": "council",
    "tr": "travel",
    "stt": "status",
}


def display_name(user: User) -> str:
    name = " ".join(x for x in (user.first_name, user.last_name) if x).strip()
    return (name or user.username or str(user.id))[:40]


class KarvonBot:
    """Holds dependencies and implements the screen state machine."""

    def __init__(self, db: Storage, seed_fn: Callable[[], int] | None = None) -> None:
        self.db = db
        self.locks = UserLocks()
        self.seed_fn = seed_fn or (lambda: random.randrange(1, 2**31))

    # ------------------------------------------------------------------ persistence
    def load(self, user: User) -> tuple[Session, str, int | None]:
        rec = self.db.load_player(user.id)
        if rec is None:
            lang = norm_lang(user.language_code)
            sess = Session()
            sess.go("lang", lang)
            msg_id = None
        else:
            sess = Session(rec["state"])
            lang = rec["lang"] if rec["lang"] in LANGS else norm_lang(user.language_code)
            msg_id = rec["msg_id"]
        sess.name = display_name(user)
        return sess, lang, msg_id

    def save(self, user_id: int, sess: Session, lang: str, msg_id: int | None) -> None:
        self.db.save_player(user_id, lang, sess.to_dict(), msg_id)

    def record_if_ended(self, user_id: int, sess: Session) -> None:
        g = sess.game
        if g is not None and g.ended and not sess.recorded:
            self.db.add_run(user_id, sess.name or "?", g.ending or "E5", g.score, g.day, g.difficulty)
            sess.recorded = True

    # ------------------------------------------------------------------ output
    async def show(self, bot: Bot, chat_id: int, sess: Session, lang: str, msg_id: int | None, edit: bool) -> int:
        seq = sess.bump()
        ctx: dict[str, Any] = {}
        if sess.screen == "top":
            ctx["top"] = self.db.top(10)
        text, rows = render(sess, lang, ctx)
        markup = build(rows, seq)
        if edit and msg_id:
            try:
                await bot.edit_message_text(text=text, chat_id=chat_id, message_id=msg_id, reply_markup=markup)
                return msg_id
            except TelegramBadRequest as exc:
                if "not modified" in str(exc).lower():
                    return msg_id
                log.info("edit failed (%s); sending a new message", exc)
            except TelegramAPIError as exc:
                log.info("edit failed (%s); sending a new message", exc)
        sent = await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        return sent.message_id

    # ------------------------------------------------------------------ commands / text
    async def on_command(self, message: Message, bot: Bot, cmd: str) -> None:
        user = message.from_user
        if user is None:
            return
        async with self.locks.get(user.id):
            sess, lang, old_msg = self.load(user)
            if cmd == "start":
                if sess.lang_chosen:
                    sess.go("menu")
                else:
                    sess.go("lang", norm_lang(user.language_code) if old_msg is None else lang)
            elif cmd == "lang":
                sess.go("lang", lang)
            elif cmd == "status":
                if sess.game is not None and not sess.game.ended:
                    sess.go("status")
                else:
                    sess.game_home()
            elif cmd == "restart":
                sess.go("restart" if sess.active else "diff")
            elif cmd == "help":
                sess.go("help")
            elif cmd == "top":
                sess.go("top")
            else:  # free text: re-send the current screen at the bottom of the chat
                sess.set_flash(E.Result(True, "use_buttons"))
            new_id = await self.show(bot, message.chat.id, sess, lang, None, edit=False)
            if old_msg and old_msg != new_id:
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=old_msg)
                except TelegramAPIError:
                    pass
            self.save(user.id, sess, lang, new_id)

    # ------------------------------------------------------------------ callbacks
    async def on_callback(self, query: CallbackQuery, bot: Bot) -> None:
        user = query.from_user
        toast: str | None = None
        async with self.locks.get(user.id):
            sess, lang, msg_id = self.load(user)
            seq, action = parse(query.data)
            chat_id = query.message.chat.id if query.message else user.id
            tapped = query.message.message_id if query.message else msg_id
            if seq is None or seq != sess.seq or tapped != msg_id:
                toast = t(lang, "stale")
            else:
                try:
                    toast, lang = self.dispatch(sess, lang, action)
                except Exception:  # never let one bad tap break the player's game
                    log.exception("error while handling action %r for user %s", action, user.id)
                    sess.game_home() if sess.game else sess.go("menu")
            self.record_if_ended(user.id, sess)
            new_id = await self.show(bot, chat_id, sess, lang, tapped, edit=True)
            self.save(user.id, sess, lang, new_id)
        try:
            await query.answer(text=(toast or "")[:200])
        except TelegramAPIError:
            pass

    def dispatch(self, sess: Session, lang: str, action: str) -> tuple[str | None, str]:
        """Apply one button press to the session. Returns (toast, lang)."""
        head, _, rest = action.partition(":")
        g = sess.game
        res: E.Result | None = None
        toast: str | None = None

        # ---------- menus (work without a game)
        if head == "L":
            if rest in LANGS:
                lang = rest
                sess.lang_chosen = True
                sess.go("menu")
                toast = t(lang, "lang.saved")
            return toast, lang
        if head == "lang":
            sess.go("lang", lang)
            return None, lang
        if head == "menu":
            sess.go("menu")
            return None, lang
        if head == "cont":
            sess.game_home() if g is not None else sess.go("menu")
            return None, lang
        if head == "new":
            sess.go("diff")
            return None, lang
        if head == "df":
            if rest in D.DIFFICULTIES:
                sess.game = E.new_game(self.seed_fn(), rest, sess.name)
                sess.recorded = False
                sess.result = None
                sess.go("hub")
            return None, lang
        if head == "help":
            sess.go("help")
            return None, lang
        if head == "top":
            sess.go("top")
            return None, lang
        if head == "tips":
            sess.tips = not sess.tips
            return None, lang
        if head == "ry":
            sess.game = None
            sess.go("diff")
            return None, lang
        if g is None:
            sess.go("menu")
            return t(lang, "stale"), lang

        # ---------- in-game navigation
        if head == "h":
            sess.game_home()
        elif head in NAV_SCREENS:
            sess.go(NAV_SCREENS[head])
        elif head == "lg":
            sess.go("ledger", rest if rest in D.CITIES else None)
        elif head == "g":
            sess.go("good", rest)
        elif head == "tc":
            sess.go("confirm", rest)
        # ---------- market
        elif head == "b":
            good, _, qty = rest.partition(":")
            res = E.buy(g, good, qty)
        elif head == "bm":
            res = E.buy(g, rest, "max")
        elif head == "s":
            good, _, qty = rest.partition(":")
            res = E.sell(g, good, qty)
        elif head == "sa":
            res = E.sell(g, rest, "all")
        # ---------- services
        elif head == "cb":
            res = E.buy_camels(g, 1)
        elif head == "cs":
            res = E.sell_camels(g, 1)
        elif head == "gh":
            res = E.hire_guards(g, rest)
        elif head == "gd":
            res = E.dismiss_guards(g, 1)
        elif head == "pb":
            res = E.buy_provisions(g, rest)
        elif head == "pm":
            res = E.buy_provisions(g, "max")
        elif head == "rs":
            res = E.rest(g)
        elif head == "wt":
            res = E.wait(g)
        elif head == "ru":
            res = E.rumor(g)
        elif head == "lp":
            res = E.pay_debt(g, rest)
        elif head == "la":
            res = E.pay_debt(g, "all")
        elif head == "lb":
            res = E.borrow(g)
        elif head == "cx":
            res = E.council(g)
            if res.ok:
                sess.go("hub")
        elif head == "dl":
            res = E.deliver(g)
            sess.go("hub")
        elif head == "rt":
            res = E.retire(g)
        # ---------- road
        elif head == "go":
            res = E.travel_start(g, rest)
            if res.ok:
                sess.go("road")
        elif head == "nd":
            res = E.next_day(g)
            sess.game_home()
        elif head == "ro":
            res = E.ride_on(g)
            sess.game_home()
        # ---------- events
        elif head == "ev":
            r = E.resolve_event_choice(g, rest)
            if r.ok:
                sess.result = r.to_dict()
                sess.go("result")
            else:
                res = r
        elif head == "ok":
            sess.result = None
            sess.game_home()
        else:
            toast = t(lang, "stale")

        if res is not None:
            sess.set_flash(res)
            if not res.ok:
                toast = t(lang, res.key, **res.params)
        if (g.ended or g.pending) and sess.screen not in ("result", "status"):
            sess.game_home()
        return toast, lang


def build_router(app: KarvonBot) -> Router:
    router = Router(name="karvon")

    @router.message(CommandStart())
    async def cmd_start(message: Message, bot: Bot) -> None:
        await app.on_command(message, bot, "start")

    for name in ("lang", "status", "restart", "help", "top"):

        def make(cmd: str):
            async def handler(message: Message, bot: Bot) -> None:
                await app.on_command(message, bot, cmd)

            handler.__name__ = f"cmd_{cmd}"
            return handler

        router.message.register(make(name), Command(name))

    @router.callback_query()
    async def on_callback(query: CallbackQuery, bot: Bot) -> None:
        await app.on_callback(query, bot)

    @router.message(F.text)
    async def on_text(message: Message, bot: Bot) -> None:
        await app.on_command(message, bot, "text")

    return router
