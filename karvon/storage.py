"""SQLite persistence (stdlib ``sqlite3``): players' sessions and finished runs."""
from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    user_id    INTEGER PRIMARY KEY,
    lang       TEXT    NOT NULL,
    state_json TEXT    NOT NULL,
    msg_id     INTEGER,
    updated_at TEXT    NOT NULL
);
CREATE TABLE IF NOT EXISTS runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    ending      TEXT    NOT NULL,
    score       INTEGER NOT NULL,
    day         INTEGER NOT NULL,
    difficulty  TEXT    NOT NULL,
    finished_at TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS runs_score_idx ON runs (score DESC);
CREATE INDEX IF NOT EXISTS runs_user_idx ON runs (user_id);
"""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class Storage:
    """Tiny synchronous wrapper; calls are fast (single row by primary key)."""

    def __init__(self, path: str = "karvon.db") -> None:
        self.path = path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        with self._lock:
            self._conn.executescript(SCHEMA)
            self._conn.commit()

    # ------------------------------------------------------------------ players
    def load_player(self, user_id: int) -> dict[str, Any] | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT user_id, lang, state_json, msg_id, updated_at FROM players WHERE user_id = ?", (user_id,)
            ).fetchone()
        if row is None:
            return None
        try:
            state = json.loads(row["state_json"])
        except (TypeError, ValueError):
            state = {}
        return {
            "user_id": row["user_id"],
            "lang": row["lang"],
            "state": state if isinstance(state, dict) else {},
            "msg_id": row["msg_id"],
            "updated_at": row["updated_at"],
        }

    def save_player(self, user_id: int, lang: str, state: dict[str, Any], msg_id: int | None) -> None:
        payload = json.dumps(state, ensure_ascii=False, separators=(",", ":"))
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO players (user_id, lang, state_json, msg_id, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    lang = excluded.lang,
                    state_json = excluded.state_json,
                    msg_id = excluded.msg_id,
                    updated_at = excluded.updated_at
                """,
                (user_id, lang, payload, msg_id, utc_now()),
            )
            self._conn.commit()

    # ------------------------------------------------------------------ runs
    def add_run(self, user_id: int, name: str, ending: str, score: int, day: int, difficulty: str) -> int:
        with self._lock:
            cur = self._conn.execute(
                "INSERT INTO runs (user_id, name, ending, score, day, difficulty, finished_at) VALUES (?,?,?,?,?,?,?)",
                (user_id, name[:64], ending, int(score), int(day), difficulty, utc_now()),
            )
            self._conn.commit()
            return int(cur.lastrowid or 0)

    def top(self, limit: int = 10) -> list[dict[str, Any]]:
        """Best run per player, highest score first."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT user_id, name, ending, score, day, difficulty, finished_at FROM runs "
                "ORDER BY score DESC, finished_at ASC LIMIT 500"
            ).fetchall()
        seen: set[int] = set()
        out: list[dict[str, Any]] = []
        for r in rows:
            if r["user_id"] in seen:
                continue
            seen.add(r["user_id"])
            out.append(dict(r))
            if len(out) >= limit:
                break
        return out

    def runs_count(self) -> int:
        with self._lock:
            return int(self._conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0])

    def close(self) -> None:
        with self._lock:
            self._conn.close()
