"""A tiny deterministic PRNG (splitmix64) whose whole state is one integer.

The integer lives inside ``GameState.rng`` so a saved game resumes the exact same
random sequence, which makes runs reproducible and JSON-serialisable.
"""
from __future__ import annotations

from typing import Sequence, TypeVar

MASK = (1 << 64) - 1
T = TypeVar("T")


def seed_state(seed: int) -> int:
    return (int(seed) * 0x9E3779B97F4A7C15 + 0xD1B54A32D192ED03) & MASK


class Rng:
    """View over a ``GameState`` that reads/writes its ``rng`` field."""

    __slots__ = ("_s",)

    def __init__(self, state) -> None:
        self._s = state

    def _next(self) -> int:
        self._s.rng = (self._s.rng + 0x9E3779B97F4A7C15) & MASK
        z = self._s.rng
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)

    def random(self) -> float:
        return (self._next() >> 11) / float(1 << 53)

    def uniform(self, a: float, b: float) -> float:
        return a + (b - a) * self.random()

    def randint(self, a: int, b: int) -> int:
        """Inclusive on both ends, like ``random.randint``."""
        if b <= a:
            return a
        return a + int(self.random() * (b - a + 1))

    def chance(self, p: float) -> bool:
        return self.random() < p

    def choice(self, seq: Sequence[T]) -> T:
        return seq[int(self.random() * len(seq))]

    def weighted(self, items: Sequence[tuple[T, float]]) -> T | None:
        total = sum(w for _, w in items if w > 0)
        if total <= 0:
            return None
        r = self.random() * total
        for item, w in items:
            if w <= 0:
                continue
            r -= w
            if r < 0:
                return item
        return items[-1][0]
