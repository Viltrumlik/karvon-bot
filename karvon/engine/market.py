"""Market model: equilibrium + temporary modifiers + drift + random walk + price impact."""
from __future__ import annotations

import math

from . import data as D
from .rng import Rng
from .state import GameState


# --------------------------------------------------------------------------- setup
def init_prices(state: GameState, rng: Rng) -> None:
    state.prices = {
        city: {good: round(D.equilibrium(city, good) * rng.uniform(0.9, 1.1), 3) for good in D.GOOD_ORDER}
        for city in D.CITIES
    }


# --------------------------------------------------------------------------- prices
def mod_mult(state: GameState, city: str, good: str) -> float:
    mult = 1.0
    for m in state.mods:
        if m["city"] == city and m["good"] == good and m["until"] >= state.day:
            mult *= m["mult"]
    return mult


def target_price(state: GameState, city: str, good: str) -> float:
    return D.equilibrium(city, good) * mod_mult(state, city, good)


def mid(state: GameState, city: str, good: str) -> float:
    return state.prices[city][good]


def hostile_here(state: GameState, city: str) -> bool:
    return bool(state.flags.get("hostile")) and not state.flags.get("exposed") and city == "buk"


def _rep_adj(state: GameState) -> float:
    return (state.rep - 50) / 50.0 * D.REP_PRICE_SWING


def _buy_from_mid(state: GameState, city: str, m: float) -> int:
    price = m * (1 + D.SPREAD) * (1 - _rep_adj(state))
    if hostile_here(state, city):
        price *= 1 + D.HOSTILE_PENALTY
    return max(1, int(round(price)))


def _sell_from_mid(state: GameState, city: str, m: float) -> int:
    price = m * (1 - D.SPREAD) * (1 + _rep_adj(state))
    if hostile_here(state, city):
        price *= 1 - D.HOSTILE_PENALTY
    return max(1, int(round(price)))


def buy_price(state: GameState, city: str, good: str) -> int:
    return _buy_from_mid(state, city, mid(state, city, good))


def sell_price(state: GameState, city: str, good: str) -> int:
    return _sell_from_mid(state, city, mid(state, city, good))


def quote_buy(state: GameState, city: str, good: str, qty: int) -> int:
    """Total tanga for buying ``qty`` units one by one (each unit moves the price)."""
    m = mid(state, city, good)
    total = 0
    for _ in range(max(0, qty)):
        total += _buy_from_mid(state, city, m)
        m *= 1 + D.impact(good)
    return total


def quote_sell(state: GameState, city: str, good: str, qty: int) -> int:
    m = mid(state, city, good)
    total = 0
    for _ in range(max(0, qty)):
        total += _sell_from_mid(state, city, m)
        m *= 1 - D.impact(good)
    return total


def max_affordable(state: GameState, city: str, good: str, money: int | None = None, limit: int | None = None) -> int:
    money = state.money if money is None else money
    limit = state.free_space if limit is None else limit
    m = mid(state, city, good)
    n = 0
    while n < limit:
        p = _buy_from_mid(state, city, m)
        if p > money:
            break
        money -= p
        m *= 1 + D.impact(good)
        n += 1
    return n


def apply_trade(state: GameState, city: str, good: str, qty: int, buying: bool) -> None:
    factor = (1 + D.impact(good)) if buying else (1 - D.impact(good))
    eq = D.equilibrium(city, good)
    p = state.prices[city][good] * factor**qty
    state.prices[city][good] = round(min(max(p, eq * D.PRICE_MIN_MULT), eq * D.PRICE_MAX_MULT), 3)


# --------------------------------------------------------------------------- dynamics
def add_mod(state: GameState, city: str, good: str, mult: float, days: int, immediate: bool = True) -> None:
    state.mods.append({"city": city, "good": good, "mult": round(mult, 3), "until": state.day + days})
    if immediate:
        eq = D.equilibrium(city, good)
        p = state.prices[city][good] * mult
        state.prices[city][good] = round(min(max(p, eq * D.PRICE_MIN_MULT), eq * D.PRICE_MAX_MULT), 3)


def daily_update(state: GameState, rng: Rng) -> None:
    state.mods = [m for m in state.mods if m["until"] >= state.day]
    for city in D.CITIES:
        row = state.prices[city]
        for good in D.GOOD_ORDER:
            eq = D.equilibrium(city, good)
            tgt = target_price(state, city, good)
            p = row[good]
            p += D.REVERSION * (tgt - p)
            p *= 1 + rng.uniform(-D.NOISE, D.NOISE)
            row[good] = round(min(max(p, eq * D.PRICE_MIN_MULT), eq * D.PRICE_MAX_MULT), 3)
    if rng.chance(D.WORLD_SHOCK_CHANCE):
        city = rng.choice(D.CITIES)
        good = rng.choice(D.GOOD_ORDER)
        if rng.chance(0.6):
            add_mod(state, city, good, rng.uniform(1.35, 1.6), rng.randint(10, 20), immediate=False)
        else:
            add_mod(state, city, good, rng.uniform(0.6, 0.75), rng.randint(10, 20), immediate=False)


def record_known(state: GameState, city: str) -> None:
    state.known[city] = {
        good: [buy_price(state, city, good), sell_price(state, city, good), state.day] for good in D.GOOD_ORDER
    }


def make_rumor(state: GameState, rng: Rng, create: bool) -> dict:
    """Reveal (and optionally create) a notable price somewhere else.

    Returns ``{"city", "good", "kind": "high"|"low", "price"}`` and writes it into the ledger.
    """
    here = {state.city}
    if state.travel:
        here |= {state.travel["src"], state.travel["dst"]}
    cities = [c for c in D.CITIES if c not in here] or [c for c in D.CITIES if c != state.city]
    if create:
        city = rng.choice(cities)
        goods = [g for g in D.GOOD_ORDER if D.PRODUCER[g] != city]
        good = rng.choice(goods)
        if rng.chance(0.7):
            add_mod(state, city, good, rng.uniform(1.4, 1.7), rng.randint(12, 20))
        else:
            add_mod(state, city, good, rng.uniform(0.55, 0.7), rng.randint(12, 20))
    else:
        best = None
        for c in cities:
            for g in D.GOOD_ORDER:
                dev = abs(math.log(state.prices[c][g] / D.equilibrium(c, g)))
                if best is None or dev > best[0]:
                    best = (dev, c, g)
        assert best is not None
        _, city, good = best
    kind = "high" if state.prices[city][good] >= D.equilibrium(city, good) else "low"
    b, s = buy_price(state, city, good), sell_price(state, city, good)
    state.known.setdefault(city, {})[good] = [b, s, state.day]
    return {"city": city, "good": good, "kind": kind, "price": s if kind == "high" else b}


def cargo_value(state: GameState, city: str | None = None) -> int:
    """Value of the cargo at ``city``'s current sell prices (base prices if city is None)."""
    total = 0
    for good, qty in state.cargo.items():
        if qty <= 0:
            continue
        if city is None:
            total += D.GOODS[good] * qty
        else:
            total += sell_price(state, city, good) * qty
    return total
