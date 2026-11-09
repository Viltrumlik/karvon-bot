"""Static world data and tunable constants for Karvonboshi.

Everything here is plain data so the balance script and tests can read it.
"""
from __future__ import annotations

# --------------------------------------------------------------------------- world
CITIES: list[str] = ["sam", "buk", "khi", "mer", "tas", "kas", "her"]
HOME = "sam"

# (a, b, days, danger 1-3, terrain)
ROADS: list[tuple[str, str, int, int, str]] = [
    ("sam", "buk", 5, 1, "steppe"),
    ("sam", "tas", 5, 1, "steppe"),
    ("buk", "khi", 8, 2, "desert"),
    ("buk", "mer", 6, 2, "steppe"),
    ("khi", "mer", 7, 3, "desert"),
    ("mer", "her", 7, 3, "mountain"),
    ("tas", "kas", 11, 2, "mountain"),
]

TERRAIN_EMOJI = {"steppe": "🌾", "desert": "🏜", "mountain": "⛰"}

# good -> base price
GOODS: dict[str, int] = {
    "lapis": 90,
    "silk": 70,
    "porcelain": 60,
    "spices": 55,
    "carpets": 45,
    "furs": 40,
    "tea": 30,
    "iron": 25,
    "paper": 20,
    "cotton": 15,
}
GOOD_ORDER: list[str] = list(GOODS)

GOOD_EMOJI = {
    "lapis": "💎",
    "silk": "🧵",
    "porcelain": "🏺",
    "spices": "🌶",
    "carpets": "🧶",
    "furs": "🦊",
    "tea": "🍵",
    "iron": "⚒",
    "paper": "📜",
    "cotton": "🌿",
}

PRODUCER: dict[str, str] = {
    "silk": "kas",
    "porcelain": "kas",
    "tea": "kas",
    "spices": "her",
    "lapis": "her",
    "paper": "sam",
    "carpets": "buk",
    "cotton": "mer",
    "furs": "khi",
    "iron": "tas",
}

PROVISION_PRICE = {"sam": 1, "buk": 1, "khi": 3, "mer": 2, "tas": 1, "kas": 2, "her": 2}
CAMEL_PRICE = {"sam": 120, "buk": 120, "khi": 80, "mer": 110, "tas": 115, "kas": 130, "her": 125}
CAMEL_SELL_PRICE = 60

# --------------------------------------------------------------------------- rules
SLOTS_PER_CAMEL = 10
PROV_PER_CAMEL = 25
MAX_CAMELS = 12
MAX_GUARDS = 12
GUARD_SIGNUP = 30
GUARD_WAGE = 4
CREW_BASE = 2  # you + Ravshan-ota
RUMOR_COST = 5

START_CAMELS = 4
START_PROVISIONS = 40
START_MORALE = 70
START_REP = 30

INTEREST_EVERY = 10
INTEREST_RATE = 0.03
INTEREST_LAST_DAY = 90  # interest is charged on days 10, 20, ... 90
LOAN_AMOUNT = 1000
LOAN_RATE = 0.05
DEADLINE_DAY = 100
FINAL_DAY = 150

REST_MORALE = 15
REST_COST_PERSON = 3
REST_COST_CAMEL = 1
ARRIVAL_MORALE = 3

# market model
PRICE_FACTOR_MIN = 0.55
PRICE_FACTOR_MAX = 2.0
PRICE_FACTOR_DIST = 12  # road-days from the producer at which the max factor is reached
SPREAD = 0.04  # buy = mid * (1 + SPREAD), sell = mid * (1 - SPREAD)
REP_PRICE_SWING = 0.05  # +-5% at reputation 100 / 0 (10% total range)
HOSTILE_PENALTY = 0.10  # Bukhara guild squeezes you while Qorabek is hostile
IMPACT_MIN = 0.008  # each unit traded moves the price 0.8% (cheap bulk goods) ...
IMPACT_MAX = 0.020  # ... up to 2% (lapis): luxury markets are thin
REVERSION = 0.10
NOISE = 0.06
PRICE_MIN_MULT = 0.3
PRICE_MAX_MULT = 3.0
WORLD_SHOCK_CHANCE = 0.05  # per day, a random glut/shortage appears somewhere

# events
EVENT_BASE = 0.10
EVENT_PER_DANGER = 0.07
HOSTILE_EVENT_BONUS = 0.04
CITY_EVENT_CHANCE = 0.30

BW_FIRST_DAY = 45
BW_LAST_DAY = 65
BW_BASE_STRENGTH = 58

DIFFICULTIES: dict[str, dict] = {
    "normal": {"debt": 2500, "money": 500, "harm": 0.8, "bandit": 0.8, "event": 0.9, "score": 0.75},
    "hard": {"debt": 3000, "money": 400, "harm": 1.0, "bandit": 1.0, "event": 1.0, "score": 1.0},
    "legendary": {"debt": 3800, "money": 350, "harm": 1.25, "bandit": 1.25, "event": 1.1, "score": 1.5},
}
DIFFICULTY_ORDER = ["normal", "hard", "legendary"]

ENDINGS = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"]
ENDING_EMOJI = {
    "E1": "🌟",
    "E2": "⚖️",
    "E3": "🕊",
    "E4": "📜",
    "E5": "⛓",
    "E6": "🏜",
    "E7": "🔥",
    "E8": "🌪",
}
ENDING_BONUS = {"E1": 5000, "E2": 2000, "E3": 500, "E4": 0, "E5": 0, "E6": 0, "E7": 0, "E8": 1000}
NW_LEGEND = 12000
NW_HONEST = 5000
QORABEK_BUYOUT = 1500
COUNCIL_REWARD = 300


# --------------------------------------------------------------------------- helpers
def neighbours(city: str) -> list[tuple[str, int, int, str]]:
    """Return [(other, days, danger, terrain)] for roads touching ``city``."""
    out = []
    for a, b, days, danger, terrain in ROADS:
        if a == city:
            out.append((b, days, danger, terrain))
        elif b == city:
            out.append((a, days, danger, terrain))
    return out


def road_between(a: str, b: str) -> tuple[int, int, str] | None:
    for x, y, days, danger, terrain in ROADS:
        if {x, y} == {a, b}:
            return days, danger, terrain
    return None


def _all_distances() -> dict[str, dict[str, int]]:
    dist = {c: {d: (0 if c == d else 10**6) for d in CITIES} for c in CITIES}
    for a, b, days, _, _ in ROADS:
        dist[a][b] = dist[b][a] = days
    for k in CITIES:
        for i in CITIES:
            for j in CITIES:
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


DIST = _all_distances()


def price_factor(city: str, good: str) -> float:
    d = DIST[PRODUCER[good]][city]
    span = PRICE_FACTOR_MAX - PRICE_FACTOR_MIN
    return PRICE_FACTOR_MIN + span * min(1.0, d / PRICE_FACTOR_DIST)


def equilibrium(city: str, good: str) -> float:
    return GOODS[good] * price_factor(city, good)


def impact(good: str) -> float:
    """Relative price move per unit bought (+) or sold (-)."""
    top = max(GOODS.values())
    return IMPACT_MIN + (IMPACT_MAX - IMPACT_MIN) * GOODS[good] / top
