"""Low-level state helpers shared by actions and events."""
from __future__ import annotations

import math

from . import data as D
from .state import GameState

RES_FIELDS = ("money", "camels", "provisions", "guards", "morale", "rep")


def diff_cfg(state: GameState) -> dict:
    return D.DIFFICULTIES.get(state.difficulty, D.DIFFICULTIES["hard"])


def harm(state: GameState) -> float:
    return diff_cfg(state)["harm"]


# --------------------------------------------------------------------------- snapshots
def snapshot(state: GameState) -> dict:
    snap = {f: getattr(state, f) for f in RES_FIELDS}
    snap["debt"] = state.total_debt
    snap["day"] = state.day
    snap["cargo"] = dict(state.cargo)
    return snap


def diff(before: dict, state: GameState) -> dict:
    after = snapshot(state)
    out: dict = {}
    for k in (*RES_FIELDS, "debt", "day"):
        d = after[k] - before[k]
        if d:
            out[k] = d
    cargo = {}
    for g in D.GOOD_ORDER:
        d = after["cargo"].get(g, 0) - before["cargo"].get(g, 0)
        if d:
            cargo[g] = d
    if cargo:
        out["cargo"] = cargo
    return out


# --------------------------------------------------------------------------- cargo
def add_cargo(state: GameState, good: str, qty: int, cost: int = 0) -> None:
    if qty <= 0:
        return
    state.cargo[good] = state.cargo.get(good, 0) + qty
    state.cargo_cost[good] = state.cargo_cost.get(good, 0) + cost


def remove_cargo(state: GameState, good: str, qty: int) -> int:
    """Remove up to ``qty`` units; returns the cost basis of the removed units."""
    have = state.cargo.get(good, 0)
    n = min(have, max(0, qty))
    if n <= 0:
        return 0
    cost = state.cargo_cost.get(good, 0)
    basis = int(round(cost * n / have)) if have else 0
    left = have - n
    if left:
        state.cargo[good] = left
        state.cargo_cost[good] = cost - basis
    else:
        state.cargo.pop(good, None)
        state.cargo_cost.pop(good, None)
    return basis


def lose_cargo_fraction(state: GameState, frac: float) -> int:
    """Lose ``frac`` of every good (rounded up). Returns units lost."""
    frac = min(0.95, max(0.0, frac))
    lost = 0
    for good in list(state.cargo):
        qty = state.cargo[good]
        n = min(qty, math.ceil(qty * frac))
        remove_cargo(state, good, n)
        lost += n
    return lost


def biggest_good(state: GameState) -> str | None:
    best = None
    for g in D.GOOD_ORDER:
        q = state.cargo.get(g, 0)
        if q > 0 and (best is None or q > state.cargo.get(best, 0)):
            best = g
    return best


def cargo_units_value(state: GameState) -> int:
    return sum(D.GOODS[g] * q for g, q in state.cargo.items())


# --------------------------------------------------------------------------- clamping
def clamp(state: GameState, notes: list | None = None) -> None:
    state.money = max(0, int(state.money))
    state.morale = min(100, max(0, int(state.morale)))
    state.rep = min(100, max(0, int(state.rep)))
    state.camels = max(0, int(state.camels))
    state.guards = min(D.MAX_GUARDS, max(0, int(state.guards)))
    state.provisions = max(0, int(state.provisions))
    if state.provisions > state.prov_cap:
        state.provisions = state.prov_cap
    over = state.cargo_units - state.capacity
    if over > 0:
        dropped = 0
        # camels that died take the cheapest loads with them first
        for good in sorted(state.cargo, key=lambda g: D.GOODS[g]):
            if over <= 0:
                break
            n = min(over, state.cargo[good])
            remove_cargo(state, good, n)
            over -= n
            dropped += n
        if notes is not None and dropped:
            notes.append(("note.cargo_dropped", {"n": dropped}))


def lose_camels(state: GameState, n: int) -> int:
    n = min(state.camels, max(0, n))
    state.camels -= n
    return n


def add_days(state: GameState, n: int) -> None:
    """Delay: on the road the journey gets longer (each extra day costs as usual)."""
    if n <= 0:
        return
    if state.travel is not None:
        state.travel["total"] += n


def stat(state: GameState, key: str, inc: int = 1) -> None:
    state.stats[key] = state.stats.get(key, 0) + inc
