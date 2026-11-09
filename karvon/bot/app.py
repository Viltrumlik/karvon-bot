"""Bot / Dispatcher factory and the polling entry point."""
from __future__ import annotations

import logging
from typing import Callable

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault

from ..i18n import LANGS, t
from ..storage import Storage
from .handlers import KarvonBot, build_router

log = logging.getLogger("karvon")

COMMANDS = ("start", "status", "lang", "restart", "help", "top")


def build_bot(token: str, api_base: str | None = None) -> Bot:
    session = AiohttpSession(api=TelegramAPIServer.from_base(api_base)) if api_base else AiohttpSession()
    return Bot(token=token, session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def bot_commands(lang: str) -> list[BotCommand]:
    return [BotCommand(command=c, description=t(lang, f"cmd.{c}")) for c in COMMANDS]


async def setup_commands(bot: Bot) -> None:
    await bot.set_my_commands(bot_commands("en"), scope=BotCommandScopeDefault())
    for lang in LANGS:
        await bot.set_my_commands(bot_commands(lang), scope=BotCommandScopeDefault(), language_code=lang)


def build_dispatcher(db: Storage, seed_fn: Callable[[], int] | None = None) -> Dispatcher:
    app = KarvonBot(db, seed_fn)
    dp = Dispatcher()
    dp["karvon"] = app
    dp.include_router(build_router(app))

    async def on_startup(bot: Bot) -> None:
        try:
            await setup_commands(bot)
        except Exception:  # commands are cosmetic; never block startup
            log.warning("could not register bot commands", exc_info=True)

    dp.startup.register(on_startup)
    return dp


async def run_polling(token: str, api_base: str | None, db_path: str) -> None:
    db = Storage(db_path)
    bot = build_bot(token, api_base)
    dp = build_dispatcher(db)
    try:
        await bot.delete_webhook(drop_pending_updates=False)
        log.info("Karvonboshi bot is polling (db=%s)", db_path)
        await dp.start_polling(bot)
    finally:
        db.close()
