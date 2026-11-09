"""Road, city and story events.

Every event has an id; i18n keys are derived from it:
``ev.<id>.title``, ``ev.<id>.text``, ``ev.<id>.c.<choice>`` and ``ev.<id>.r.<outcome>``.
"""
from __future__ import annotations

import math

from . import data as D
from . import market as M
from .core import (
    add_cargo,
    add_days,
    biggest_good,
    cargo_units_value,
    diff_cfg,
    harm,
    lose_camels,
    lose_cargo_fraction,
    remove_cargo,
    stat,
)
from .rng import Rng
from .state import GameState


# --------------------------------------------------------------------------- fights
def expected_strength(state: GameState, bonus: int = 0) -> int:
    return int(round(state.guards * 10 + state.camels + state.morale / 10 + 3.5 + bonus))


def player_strength(state: GameState, rng: Rng, bonus: int = 0) -> float:
    """guards*10 + camels + morale/10 + d6 (+ bonus). Bounded and monotonic in guards/morale."""
    return state.guards * 10 + state.camels + state.morale / 10 + rng.randint(1, 6) + bonus


def bandit_strength(state: GameState, danger: int, rng: Rng) -> int:
    base = 10 + 5 * danger + state.day * 0.25 + cargo_units_value(state) / 150
    return int(round(base * diff_cfg(state)["bandit"] * rng.uniform(0.85, 1.15)))


def black_wind_strength(state: GameState, rng: Rng) -> int:
    base = D.BW_BASE_STRENGTH + max(0, state.day - D.BW_FIRST_DAY) * 0.6 + cargo_units_value(state) / 120
    return int(round(base * diff_cfg(state)["bandit"] * rng.uniform(0.9, 1.1)))


def fight(state: GameState, enemy: int, rng: Rng, bonus: int = 0) -> bool:
    ours = player_strength(state, rng, bonus)
    theirs = enemy * rng.uniform(0.9, 1.1)
    return ours >= theirs


def round5(x: float) -> int:
    return int(5 * round(x / 5))


def _hostile(state: GameState) -> bool:
    return bool(state.flags.get("hostile")) and not state.flags.get("exposed")


# --------------------------------------------------------------------------- base
class Event:
    id = ""
    kind = "road"  # road | city | story

    def weight(self, s: GameState, ctx: dict) -> float:  # 0 = not eligible
        return 1.0

    def setup(self, s: GameState, ctx: dict, rng: Rng) -> dict:
        return {}

    def choices(self, s: GameState, p: dict) -> list[str]:
        raise NotImplementedError

    def resolve(self, s: GameState, p: dict, choice: str, rng: Rng, notes: list) -> tuple[str, dict]:
        raise NotImplementedError


EVENTS: dict[str, Event] = {}


def register(cls):
    EVENTS[cls.id] = cls()
    return cls


# =========================================================================== road events
@register
class Sandstorm(Event):
    id = "sandstorm"

    def weight(self, s, ctx):
        return {"desert": 3.0, "steppe": 0.8}.get(ctx["terrain"], 0.0)

    def choices(self, s, p):
        return ["shelter", "push"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "shelter":
            add_days(s, 1)
            s.morale -= 2
            return "shelter", {}
        s.provisions -= int(round(s.provisions * rng.uniform(0.15, 0.3) * harm(s)))
        if rng.chance(0.35 * harm(s)):
            lose_camels(s, 1)
            return "push_camel", {}
        return "push", {}


@register
class Bandits(Event):
    id = "bandits"

    def weight(self, s, ctx):
        w = 0.9 * ctx["danger"]
        if _hostile(s):
            w *= 1.6
        w *= 1 + min(1.0, cargo_units_value(s) / 2000)
        return w

    def setup(self, s, ctx, rng):
        enemy = bandit_strength(s, ctx["danger"], rng)
        return {"enemy": enemy, "n": max(3, enemy // 5), "theirs": round5(enemy), "ours": round5(expected_strength(s)),
                "danger": ctx["danger"]}

    def choices(self, s, p):
        return ["fight", "pay", "flee"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "fight":
            stat(s, "fights")
            if fight(s, p["enemy"], rng):
                loot = rng.randint(10, 30) + p["n"] * 4
                s.money += loot
                s.rep += 3
                s.morale += 8
                stat(s, "fights_won")
                return "fight_win", {"loot": loot}
            lose_cargo_fraction(s, 0.35 * harm(s))
            s.guards -= 1 if s.guards else 0
            if s.guards >= 4 and rng.chance(0.5):
                s.guards -= 1
            s.money -= int(round(s.money * 0.1 * harm(s)))
            s.morale -= 10
            return "fight_lose", {}
        if choice == "pay":
            s.morale -= 3
            if s.cargo_units > 0:
                lose_cargo_fraction(s, 0.2)
                return "pay", {}
            s.money -= max(min(s.money, 15), int(round(s.money * 0.15)))
            return "pay_money", {}
        # flee
        chance = 0.6 - 0.08 * (p.get("danger", 1) - 1) + (0.05 if s.camels <= 4 else 0.0)
        if rng.chance(chance):
            s.morale -= 2
            return "flee_ok", {}
        lose_cargo_fraction(s, 0.25 * harm(s))
        if rng.chance(0.5 * harm(s)):
            lose_camels(s, 1)
        s.morale -= 5
        return "flee_fail", {}


@register
class SickCamel(Event):
    id = "sick_camel"

    def weight(self, s, ctx):
        return 1.3 if ctx["terrain"] == "desert" else 0.9

    def choices(self, s, p):
        out = []
        if s.provisions >= 8:
            out.append("treat")
        return out + ["leave", "slaughter"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "treat":
            s.provisions -= 8
            if rng.chance(0.75):
                return "treat_ok", {}
            lose_camels(s, 1)
            return "treat_fail", {}
        lose_camels(s, 1)
        if choice == "slaughter":
            s.provisions += 15
            return "slaughter", {}
        return "leave", {}


@register
class Oasis(Event):
    id = "oasis"

    def weight(self, s, ctx):
        return {"desert": 1.4, "steppe": 0.9}.get(ctx["terrain"], 0.0)

    def choices(self, s, p):
        return ["rest", "water"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "rest":
            add_days(s, 1)
            s.morale += 12
            s.provisions += 25
            return "rest", {}
        s.provisions += 12
        s.morale += 4
        return "water", {}


@register
class Traveler(Event):
    id = "traveler"

    def choices(self, s, p):
        out = []
        if s.provisions >= 5:
            out.append("share")
        if s.provisions >= 10:
            out.append("escort")
        return out + ["pass"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "share":
            s.provisions -= 5
            s.rep += 4
            s.flags["helped"] = s.flags.get("helped", 0) + 1
            return "share", {}
        if choice == "escort":
            s.provisions -= 10
            add_days(s, 1)
            s.rep += 7
            s.flags["helped"] = s.flags.get("helped", 0) + 1
            if rng.chance(0.4):
                gift = rng.randint(30, 60)
                s.money += gift
                return "escort_paid", {"money": gift}
            return "escort", {}
        s.morale -= 2
        return "pass", {}


@register
class Toll(Event):
    id = "toll"

    def weight(self, s, ctx):
        return 1.1

    def setup(self, s, ctx, rng):
        fee = int(round((10 + s.cargo_units + s.camels * 2) * harm(s)))
        return {"fee": fee}

    def choices(self, s, p):
        out = []
        if s.money >= p["fee"]:
            out.append("pay")
        out.append("detour")
        if s.rep >= 50:
            out.append("talk")
        return out

    def resolve(self, s, p, choice, rng, notes):
        fee = p["fee"]
        if choice == "pay":
            s.money -= fee
            return "pay", {"fee": fee}
        if choice == "talk":
            if rng.chance(0.75):
                return "talk_ok", {}
            s.money -= min(s.money, fee)
            return "talk_fail", {"fee": fee}
        add_days(s, 2)
        return "detour", {}


@register
class Wolves(Event):
    id = "wolves"

    def weight(self, s, ctx):
        return {"mountain": 2.5, "steppe": 0.4}.get(ctx["terrain"], 0.0)

    def setup(self, s, ctx, rng):
        return {"enemy": int(round((14 + 3 * ctx["danger"]) * harm(s) * rng.uniform(0.8, 1.2)))}

    def choices(self, s, p):
        out = ["fight"] if s.guards >= 1 else []
        if s.provisions >= 6:
            out.append("fire")
        return out + ["run"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "fight":
            stat(s, "fights")
            if fight(s, p["enemy"], rng):
                s.morale += 5
                stat(s, "fights_won")
                return "fight_win", {}
            lose_camels(s, 1)
            if rng.chance(0.3):
                s.guards -= 1
            s.morale -= 6
            return "fight_lose", {}
        if choice == "fire":
            s.provisions -= 6
            s.morale -= 3
            return "fire", {}
        if rng.chance(0.45 * harm(s)):
            lose_camels(s, 1)
            s.morale -= 4
            return "run_loss", {}
        return "run_ok", {}


@register
class Merchant(Event):
    id = "merchant"

    def setup(self, s, ctx, rng):
        good = rng.choice(D.GOOD_ORDER)
        price = max(2, int(round(D.GOODS[good] * rng.uniform(0.6, 0.8))))
        return {"good": good, "qty": rng.randint(4, 10), "price": price}

    def choices(self, s, p):
        if s.money >= p["price"] and s.free_space >= 1:
            return ["buy", "haggle", "decline"]
        return ["decline"]

    def _buy(self, s, p, price):
        n = min(p["qty"], s.free_space, s.money // price)
        add_cargo(s, p["good"], n, n * price)
        s.money -= n * price
        return n

    def resolve(self, s, p, choice, rng, notes):
        if choice == "buy":
            n = self._buy(s, p, p["price"])
            return "buy", {"good": p["good"], "n": n, "money": n * p["price"]}
        if choice == "haggle":
            if rng.chance(0.35 + s.rep / 200):
                price = max(1, int(round(p["price"] * 0.85)))
                n = self._buy(s, p, price)
                return "haggle_ok", {"good": p["good"], "n": n, "money": n * price}
            return "haggle_fail", {}
        return "decline", {}


@register
class Quarrel(Event):
    id = "quarrel"

    def weight(self, s, ctx):
        return 1.8 if s.morale < 50 else 0.8

    def choices(self, s, p):
        out = ["bonus"] if s.money >= 3 * s.crew else []
        return out + ["judge", "ignore"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "bonus":
            cost = 3 * s.crew
            s.money -= cost
            s.morale += 6
            return "bonus", {"money": cost}
        if choice == "judge":
            if rng.chance(0.4 + s.rep / 150):
                s.morale += 4
                s.rep += 1
                return "judge_ok", {}
            s.morale -= 8
            return "judge_fail", {}
        s.morale -= 6
        return "ignore", {}


@register
class Dervish(Event):
    id = "dervish"

    def weight(self, s, ctx):
        return 0.8

    def choices(self, s, p):
        out = ["alms"] if s.money >= 5 else []
        return out + ["listen", "pass"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "alms":
            s.money -= 5
            s.rep += 2
            return "alms", M.make_rumor(s, rng, create=True)
        if choice == "listen":
            if rng.chance(0.5):
                return "listen_ok", M.make_rumor(s, rng, create=False)
            return "listen_vague", {}
        return "pass", {}


@register
class Flood(Event):
    id = "flood"

    def weight(self, s, ctx):
        w = {"mountain": 1.2, "steppe": 0.8, "desert": 0.3}.get(ctx["terrain"], 0.0)
        return w if s.cargo_units else w * 0.3

    def choices(self, s, p):
        return ["save_cargo", "save_camels"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "save_cargo":
            if rng.chance(0.4 * harm(s)):
                lose_camels(s, 1)
                return "cargo_camel", {}
            return "cargo_ok", {}
        lose_cargo_fraction(s, 0.3 * harm(s))
        return "camels", {}


@register
class Saddle(Event):
    id = "saddle"

    def weight(self, s, ctx):
        return 1.0 if s.cargo_units >= 5 else 0.0

    def choices(self, s, p):
        out = ["rope"] if s.provisions >= 8 else []
        return out + ["fix", "drop"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "rope":
            s.provisions -= 8
            return "rope", {}
        if choice == "fix":
            add_days(s, 1)
            return "fix", {}
        good = biggest_good(s)
        if good is None:
            return "fix", {}
        n = min(8, s.cargo.get(good, 0))
        remove_cargo(s, good, n)
        return "drop", {"good": good, "n": n}


@register
class Cold(Event):
    id = "cold"

    def weight(self, s, ctx):
        return 2.5 if ctx["terrain"] == "mountain" else 0.0

    def choices(self, s, p):
        out = ["camp", "push"]
        if s.cargo.get("furs", 0) + s.cargo.get("cotton", 0) >= 3:
            out.append("burn")
        return out

    def resolve(self, s, p, choice, rng, notes):
        if choice == "camp":
            add_days(s, 1)
            s.morale -= 3
            return "camp", {}
        if choice == "burn":
            need = 3
            for good in ("cotton", "furs"):
                take = min(need, s.cargo.get(good, 0))
                remove_cargo(s, good, take)
                need -= take
            s.morale += 2
            return "burn", {}
        s.morale -= 4
        if rng.chance(0.45 * harm(s)):
            lose_camels(s, 1)
            return "push_loss", {}
        return "push_ok", {}


@register
class Abandoned(Event):
    id = "abandoned"

    def weight(self, s, ctx):
        return 0.8

    def setup(self, s, ctx, rng):
        return {"good": rng.choice(D.GOOD_ORDER), "qty": rng.randint(3, 8)}

    def choices(self, s, p):
        out = ["take"] if s.free_space >= 1 else []
        return out + ["bury", "leave"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "take":
            n = min(p["qty"], s.free_space)
            add_cargo(s, p["good"], n, 0)
            if rng.chance(0.4):
                s.rep -= 6
                return "take_seen", {"good": p["good"], "n": n}
            return "take", {"good": p["good"], "n": n}
        if choice == "bury":
            s.rep += 3
            s.morale -= 1
            return "bury", {}
        return "leave", {}


@register
class Deserter(Event):
    id = "deserter"

    def weight(self, s, ctx):
        if s.guards < 1:
            return 0.0
        return 1.4 if s.morale < 40 else 0.5

    def choices(self, s, p):
        out = ["pay"] if s.money >= 20 else []
        out.append("let_go")
        if s.guards >= 2:
            out.append("chase")
        return out

    def resolve(self, s, p, choice, rng, notes):
        if choice == "pay":
            s.money -= 20
            s.morale += 2
            return "pay", {}
        if choice == "chase":
            if rng.chance(0.5):
                s.morale += 3
                return "chase_ok", {}
            s.guards -= 1
            s.money -= int(round(s.money * 0.1))
            return "chase_fail", {}
        s.guards -= 1
        return "let_go", {}


@register
class Pilgrims(Event):
    id = "pilgrims"

    def weight(self, s, ctx):
        return 0.7

    def choices(self, s, p):
        out = ["escort"] if s.provisions >= 6 else []
        return out + ["decline"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "escort":
            s.provisions -= 6
            s.rep += 4
            gift = rng.randint(10, 30)
            s.money += gift
            return "escort", {"money": gift}
        s.rep -= 1
        return "decline", {}


@register
class DryWell(Event):
    id = "dry_well"

    def weight(self, s, ctx):
        return 1.5 if ctx["terrain"] == "desert" else 0.0

    def setup(self, s, ctx, rng):
        return {"cost": 2 * s.crew}

    def choices(self, s, p):
        out = ["dig"]
        if s.money >= p["cost"]:
            out.append("buy")
        return out + ["ration"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "dig":
            add_days(s, 1)
            s.provisions += 12
            return "dig", {}
        if choice == "buy":
            s.money -= p["cost"]
            s.provisions += 10
            return "buy", {"money": p["cost"]}
        s.morale -= 8
        return "ration", {}


# --------------------------------------------------------------------------- story: road
@register
class BlackWind(Event):
    id = "black_wind"
    kind = "story"

    def setup(self, s, ctx, rng):
        enemy = black_wind_strength(s, rng)
        bonus = 15 if s.flags.get("nilufar_ally") else 0
        return {"enemy": enemy, "theirs": round5(enemy), "ours": round5(expected_strength(s, bonus)), "bonus": bonus}

    def choices(self, s, p):
        out = ["fight", "tribute", "flee"]
        if s.rep < 20:
            out.append("join")
        return out

    def resolve(self, s, p, choice, rng, notes):
        s.flags["bw_done"] = True
        if choice == "join":
            s.flags["joined"] = True
            return "join", {}
        if choice == "fight":
            stat(s, "fights")
            if fight(s, p["enemy"], rng, p.get("bonus", 0)):
                s.flags["token"] = True
                loot = rng.randint(120, 200)
                s.money += loot
                s.rep += 10
                s.morale += 15
                stat(s, "fights_won")
                return "fight_win", {"loot": loot}
            lose_cargo_fraction(s, 0.5 * harm(s))
            s.guards -= math.ceil(s.guards / 2)
            if rng.chance(0.6):
                lose_camels(s, 1)
            s.morale -= 15
            return "fight_lose", {}
        if choice == "tribute":
            s.morale -= 8
            s.rep -= 3
            if s.cargo_units:
                lose_cargo_fraction(s, 0.4)
            else:
                s.money -= int(round(s.money * 0.4))
            return "tribute", {}
        # flee into the dunes
        if rng.chance(0.5):
            if rng.chance(0.3):
                lose_camels(s, 1)
            s.morale -= 4
            return "flee_ok", {}
        lose_camels(s, rng.randint(1, 2))
        lose_cargo_fraction(s, 0.3)
        s.morale -= 10
        return "flee_fail", {}


# =========================================================================== city events
@register
class Festival(Event):
    id = "festival"
    kind = "city"

    def setup(self, s, ctx, rng):
        goods = [g for g in D.GOOD_ORDER if D.PRODUCER[g] != ctx["city"]]
        g1 = rng.choice(goods)
        g2 = rng.choice([g for g in goods if g != g1])
        for g in (g1, g2):
            M.add_mod(s, ctx["city"], g, 1.5, 10)
        return {"good": g1, "good2": g2, "cost": 4 * s.crew}

    def choices(self, s, p):
        out = ["feast"] if s.money >= p["cost"] else []
        return out + ["trade"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "feast":
            s.money -= p["cost"]
            s.morale += 12
            return "feast", {"money": p["cost"]}
        return "trade", {}


@register
class Plague(Event):
    id = "plague"
    kind = "city"

    def weight(self, s, ctx):
        return 0.5

    def setup(self, s, ctx, rng):
        for g in D.GOOD_ORDER:
            M.add_mod(s, ctx["city"], g, 1.2, 8)
        return {}

    def choices(self, s, p):
        out = ["endure"]
        if s.money >= 25:
            out.append("medicine")
        if s.provisions >= 10:
            out.append("help")
        return out

    def resolve(self, s, p, choice, rng, notes):
        if choice == "medicine":
            s.money -= 25
            return "medicine", {}
        if choice == "help":
            s.provisions -= 10
            s.rep += 6
            if rng.chance(0.4):
                s.morale -= 6
                return "help_sick", {}
            return "help_ok", {}
        s.morale -= int(round(8 * harm(s)))
        return "endure", {}


@register
class GuildTax(Event):
    id = "guild_tax"
    kind = "city"

    def weight(self, s, ctx):
        return 3.0 if ctx["city"] == "buk" and _hostile(s) else 0.0

    def setup(self, s, ctx, rng):
        tax = max(10, int(round(s.money * 0.05)))
        return {"tax": tax, "bribe": max(5, int(round(tax * 0.6)))}

    def choices(self, s, p):
        out = []
        if s.money >= p["tax"]:
            out.append("pay")
        out.append("refuse")
        if s.money >= p["bribe"]:
            out.append("bribe")
        return out

    def resolve(self, s, p, choice, rng, notes):
        if choice == "pay":
            s.money -= p["tax"]
            return "pay", {"money": p["tax"]}
        if choice == "bribe":
            s.money -= p["bribe"]
            if rng.chance(0.3):
                s.rep -= 8
                return "bribe_caught", {}
            return "bribe", {}
        s.rep -= 6
        if rng.chance(0.5):
            lose_cargo_fraction(s, 0.15)
            return "refuse_seized", {}
        return "refuse", {}


@register
class Glut(Event):
    id = "glut"
    kind = "city"

    def setup(self, s, ctx, rng):
        good = rng.choice(D.GOOD_ORDER)
        M.add_mod(s, ctx["city"], good, 0.6, rng.randint(10, 20))
        price = max(1, int(round(M.buy_price(s, ctx["city"], good) * 0.9)))
        return {"good": good, "price": price}

    def choices(self, s, p):
        if s.money >= p["price"] and s.free_space >= 1:
            return ["buy_lot", "note"]
        return ["note"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "buy_lot":
            n = min(10, s.free_space, s.money // p["price"])
            add_cargo(s, p["good"], n, n * p["price"])
            s.money -= n * p["price"]
            return "buy_lot", {"good": p["good"], "n": n, "money": n * p["price"]}
        return "note", {"good": p["good"]}


@register
class Wedding(Event):
    id = "wedding"
    kind = "city"

    def weight(self, s, ctx):
        return 0.9 if s.contract is None and s.day < D.FINAL_DAY - 25 else 0.0

    def setup(self, s, ctx, rng):
        here = ctx["city"]
        dests = [c for c in D.CITIES if c != here and D.DIST[here][c] <= 21]
        dest = rng.choice(dests)
        goods = [g for g in D.GOOD_ORDER if D.PRODUCER[g] != dest]
        good = rng.choice(goods)
        qty = rng.randint(6, 12)
        until = s.day + D.DIST[here][dest] + rng.randint(6, 12)
        reward = int(round(qty * D.GOODS[good] * 1.6 + 40))
        return {"good": good, "qty": qty, "city": dest, "until": until, "reward": reward}

    def choices(self, s, p):
        return ["accept", "decline"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "accept":
            s.contract = {k: p[k] for k in ("good", "qty", "city", "until", "reward")}
            return "accept", {}
        return "decline", {}


@register
class CamelFair(Event):
    id = "camel_fair"
    kind = "city"

    def weight(self, s, ctx):
        return 0.6

    def setup(self, s, ctx, rng):
        price = int(round(D.CAMEL_PRICE[ctx["city"]] * 0.7))
        s.camel_deal = {"city": ctx["city"], "until": s.day, "price": price}
        return {"price": price}

    def choices(self, s, p):
        out = ["buy_one"] if s.money >= p["price"] and s.camels < D.MAX_CAMELS else []
        return out + ["look"]

    def resolve(self, s, p, choice, rng, notes):
        if choice == "buy_one":
            s.money -= p["price"]
            s.camels += 1
            return "buy_one", {"money": p["price"]}
        return "look", {}


@register
class Nilufar(Event):
    id = "nilufar"
    kind = "story"

    def choices(self, s, p):
        out = ["pay"] if s.money >= 60 else []
        return out + ["refuse"]

    def resolve(self, s, p, choice, rng, notes):
        s.flags["nilufar_met"] = True
        if choice == "pay":
            s.money -= 60
            s.rep += 3
            s.flags["nilufar_ally"] = True
            return "pay", {}
        return "refuse", {}


@register
class Grateful(Event):
    id = "grateful"
    kind = "story"

    def choices(self, s, p):
        return ["gift", "news"]

    def resolve(self, s, p, choice, rng, notes):
        s.flags["grateful_done"] = True
        if choice == "gift":
            s.money += 80
            return "gift", {"money": 80}
        r1 = M.make_rumor(s, rng, create=True)
        r2 = M.make_rumor(s, rng, create=True)
        s.rep += 2
        return "news", {"good": r1["good"], "city": r1["city"], "good2": r2["good"], "city2": r2["city"]}


@register
class Qorabek(Event):
    id = "qorabek"
    kind = "story"

    def setup(self, s, ctx, rng):
        return {"money": D.QORABEK_BUYOUT}

    def choices(self, s, p):
        return ["accept", "refuse"]

    def resolve(self, s, p, choice, rng, notes):
        s.flags["qorabek_done"] = True
        if choice == "accept":
            s.flags["sold_out"] = True
            return "accept", {}
        s.flags["hostile"] = True
        return "refuse", {}


@register
class Letter(Event):
    id = "letter"
    kind = "story"

    def choices(self, s, p):
        return ["keep", "burn"]

    def resolve(self, s, p, choice, rng, notes):
        s.flags["letter_done"] = True
        if choice == "keep":
            s.flags["letter"] = True
            return "keep", {}
        s.morale += 8
        return "burn", {}


ROAD_EVENT_IDS = [k for k, v in EVENTS.items() if v.kind == "road"]
CITY_EVENT_IDS = [k for k, v in EVENTS.items() if v.kind == "city"]
STORY_EVENT_IDS = [k for k, v in EVENTS.items() if v.kind == "story"]


# --------------------------------------------------------------------------- triggers
def start_event(state: GameState, ev_id: str, ctx: dict, rng: Rng, src: str) -> None:
    ev = EVENTS[ev_id]
    params = ev.setup(state, ctx, rng)
    state.pending = {"id": ev_id, "params": params, "src": src}
    stat(state, "events")


def road_ctx(state: GameState) -> dict:
    t = state.travel or {}
    return {"danger": int(t.get("danger", 1)), "terrain": t.get("terrain", "steppe")}


def roll_road_event(state: GameState, rng: Rng) -> bool:
    ctx = road_ctx(state)
    f = state.flags
    if (
        not f.get("bw_done")
        and D.BW_FIRST_DAY <= state.day <= D.BW_LAST_DAY
        and ctx["danger"] >= 2
        and rng.chance(0.6 if state.day >= 58 else 0.3)
    ):
        start_event(state, "black_wind", ctx, rng, "road")
        return True
    p = D.EVENT_BASE + D.EVENT_PER_DANGER * ctx["danger"]
    if _hostile(state) and ctx["danger"] >= 2:
        p += D.HOSTILE_EVENT_BONUS
    p *= diff_cfg(state)["event"]
    if not rng.chance(p):
        return False
    choice = rng.weighted([(eid, EVENTS[eid].weight(state, ctx)) for eid in ROAD_EVENT_IDS])
    if choice is None:
        return False
    start_event(state, choice, ctx, rng, "road")
    return True


def roll_city_event(state: GameState, rng: Rng, arrival: bool) -> bool:
    """Story beats first, then (on arrival only) a random city event."""
    f = state.flags
    city = state.city
    ctx = {"city": city, "danger": 0, "terrain": ""}
    if not f.get("qorabek_done") and (city == "buk" or state.day >= 15):
        start_event(state, "qorabek", ctx, rng, "city")
        return True
    if not f.get("letter_done") and state.day >= 30 and state.rep >= 40:
        start_event(state, "letter", ctx, rng, "city")
        return True
    if city == "khi" and not f.get("nilufar_met"):
        start_event(state, "nilufar", ctx, rng, "city")
        return True
    if not arrival:
        return False
    if f.get("helped") and not f.get("grateful_done") and rng.chance(0.35):
        start_event(state, "grateful", ctx, rng, "city")
        return True
    if not rng.chance(D.CITY_EVENT_CHANCE):
        return False
    choice = rng.weighted([(eid, EVENTS[eid].weight(state, ctx)) for eid in CITY_EVENT_IDS])
    if choice is None:
        return False
    start_event(state, choice, ctx, rng, "city")
    return True


def pending_choices(state: GameState) -> list[str]:
    if not state.pending:
        return []
    ev = EVENTS.get(state.pending["id"])
    if ev is None:
        return []
    return ev.choices(state, state.pending["params"])
