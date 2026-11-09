"""Per-player UI session: the game state plus which screen is shown.

Stored as JSON in ``players.state_json``::

    {"game": {...GameState...} | null, "screen": "hub", "arg": null, "seq": 7,
     "flash": {...Result...} | null, "result": {...} | null, "tips": true, "seen": [...],
     "name": "Aziz", "recorded": false, "lang_chosen": true}
"""
from __future__ import annotations

import asyncio
from collections import defaultdict
from typing import Any

from ..engine import GameState, Result

SEQ_MOD = 1000


class Session:
    def __init__(self, data: dict[str, Any] | None = None) -> None:
        data = dict(data or {})
        raw_game = data.get("game")
        self.game: GameState | None = None
        if isinstance(raw_game, dict):
            try:
                self.game = GameState.from_dict(raw_game)
            except TypeError:
                self.game = None
        self.screen: str = str(data.get("screen") or "menu")
        self.arg: str | None = data.get("arg")
        self.seq: int = int(data.get("seq") or 0) % SEQ_MOD
        self.flash: dict | None = data.get("flash")
        self.result: dict | None = data.get("result")
        self.tips: bool = bool(data.get("tips", True))
        self.seen: list[str] = list(data.get("seen") or [])
        self.name: str = str(data.get("name") or "")
        self.recorded: bool = bool(data.get("recorded", False))
        self.lang_chosen: bool = bool(data.get("lang_chosen", False))

    def to_dict(self) -> dict[str, Any]:
        return {
            "game": self.game.to_dict() if self.game else None,
            "screen": self.screen,
            "arg": self.arg,
            "seq": self.seq,
            "flash": self.flash,
            "result": self.result,
            "tips": self.tips,
            "seen": self.seen,
            "name": self.name,
            "recorded": self.recorded,
            "lang_chosen": self.lang_chosen,
        }

    # ------------------------------------------------------------------ helpers
    def go(self, screen: str, arg: str | None = None) -> None:
        self.screen = screen
        self.arg = arg

    def bump(self) -> int:
        self.seq = (self.seq + 1) % SEQ_MOD
        return self.seq

    def set_flash(self, res: Result | None) -> None:
        self.flash = res.to_dict() if res is not None else None

    @property
    def active(self) -> bool:
        return self.game is not None and not self.game.ended

    def game_home(self) -> None:
        """Pick the natural screen for the current game state."""
        g = self.game
        if g is None:
            self.go("menu")
        elif g.ended:
            self.go("ending")
        elif g.pending:
            self.go("event")
        elif g.on_road:
            self.go("road")
        else:
            self.go("hub")


class UserLocks:
    """One asyncio lock per user so double taps are processed strictly one after another."""

    def __init__(self) -> None:
        self._locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

    def get(self, user_id: int) -> asyncio.Lock:
        return self._locks[user_id]
