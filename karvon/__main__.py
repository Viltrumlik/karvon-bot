"""Entry point: ``python -m karvon`` (reads BOT_TOKEN, TELEGRAM_API_BASE, DB_PATH from env or .env)."""
from __future__ import annotations

import asyncio
import logging
import sys

from .bot.app import run_polling
from .config import Config


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    cfg = Config.from_env()
    if not cfg.bot_token:
        print(
            "BOT_TOKEN is not set. Create a bot with @BotFather, then put BOT_TOKEN=... into .env "
            "(see .env.example), or play locally without a token: python scripts/console_play.py",
            file=sys.stderr,
        )
        return 2
    try:
        asyncio.run(run_polling(cfg.bot_token, cfg.api_base, cfg.db_path))
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
