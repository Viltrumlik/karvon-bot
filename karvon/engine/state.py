"""Game state (JSON-serialisable dataclass) and action result objects."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields
from typing import Any

STATE_VERSION = 1


@dataclass
class GameState:
    seed: int
    rng: int
    difficulty: str = "hard"
    name: str = ""
    version: int = STATE_VERSION
    day: int = 1
    phase: str = "city"  # "city" | "road" | "ended"
    city: str = "sam"  # current city (or the city we left while on the road)
    travel: dict | None = None  # {"src", "dst", "total", "done", "danger", "terrain"}
    money: int = 0
    camels: int = 0
    provisions: int = 0
    guards: int = 0
    morale: int = 0
    rep: int = 0
    debt: int = 0
    loan: int = 0
    loan_taken: bool = False
    paid_day: int = 0  # day the whole debt was cleared (0 = not yet)
    cargo: dict = field(default_factory=dict)  # good -> units
    cargo_cost: dict = field(default_factory=dict)  # good -> total tanga paid (for average cost)
    prices: dict = field(default_factory=dict)  # city -> good -> mid price
    mods: list = field(default_factory=list)  # [{"city", "good", "mult", "until"}]
    known: dict = field(default_factory=dict)  # city -> good -> [price, day]
    flags: dict = field(default_factory=dict)
    visited: list = field(default_factory=list)
    pending: dict | None = None  # {"id", "params", "src"}
    contract: dict | None = None  # {"good", "qty", "city", "until", "reward"}
    camel_deal: dict | None = None  # {"city", "until", "mult"}
    starving: int = 0  # consecutive road days without provisions
    ending: str | None = None
    score: int = 0
    stats: dict = field(default_factory=dict)

    # ---------------------------------------------------------------- serialisation
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"), sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameState":
        names = {f.name for f in fields(cls)}
        clean = {k: v for k, v in data.items() if k in names}
        return cls(**clean)

    @classmethod
    def from_json(cls, raw: str) -> "GameState":
        return cls.from_dict(json.loads(raw))

    # ---------------------------------------------------------------- convenience
    @property
    def on_road(self) -> bool:
        return self.phase == "road" and self.travel is not None

    @property
    def ended(self) -> bool:
        return self.phase == "ended"

    @property
    def total_debt(self) -> int:
        return self.debt + self.loan

    @property
    def debt_paid(self) -> bool:
        return self.paid_day > 0

    @property
    def capacity(self) -> int:
        from .data import SLOTS_PER_CAMEL

        return self.camels * SLOTS_PER_CAMEL

    @property
    def cargo_units(self) -> int:
        return sum(self.cargo.values())

    @property
    def free_space(self) -> int:
        return max(0, self.capacity - self.cargo_units)

    @property
    def prov_cap(self) -> int:
        from .data import PROV_PER_CAMEL

        return self.camels * PROV_PER_CAMEL

    @property
    def crew(self) -> int:
        from .data import CREW_BASE

        return CREW_BASE + self.guards


@dataclass
class Result:
    """Outcome of a player action.

    ``key``/``params`` describe the main message (an i18n key), ``deltas`` the
    resource changes, ``notes`` extra messages (interest charged, arrival, ...).
    Actions never raise on bad input: they return ``ok=False`` with an ``err.*`` key.
    """

    ok: bool
    key: str
    params: dict = field(default_factory=dict)
    deltas: dict = field(default_factory=dict)
    notes: list = field(default_factory=list)  # [(key, params)]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "key": self.key,
            "params": dict(self.params),
            "deltas": dict(self.deltas),
            "notes": [[k, dict(p)] for k, p in self.notes],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Result":
        return cls(
            ok=bool(data.get("ok")),
            key=str(data.get("key", "")),
            params=dict(data.get("params") or {}),
            deltas=dict(data.get("deltas") or {}),
            notes=[(k, dict(p)) for k, p in (data.get("notes") or [])],
        )
