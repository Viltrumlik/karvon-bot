"""Configuration from environment variables or a ``.env`` file (no extra dependency)."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def load_dotenv(path: str | os.PathLike = ".env") -> None:
    """Minimal .env reader: KEY=VALUE lines; existing environment variables win."""
    p = Path(path)
    if not p.is_file():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key.startswith("export "):
            key = key[len("export ") :].strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class Config:
    bot_token: str
    api_base: str | None
    db_path: str

    @classmethod
    def from_env(cls, dotenv: str | os.PathLike = ".env") -> "Config":
        load_dotenv(dotenv)
        return cls(
            bot_token=os.environ.get("BOT_TOKEN", "").strip(),
            api_base=(os.environ.get("TELEGRAM_API_BASE") or "").strip() or None,
            db_path=(os.environ.get("DB_PATH") or "karvon.db").strip(),
        )
