#!/usr/bin/env python3
"""Balance check: run a greedy trading bot and a do-nothing bot over many seeds.

Usage:
    python scripts/balance.py                 # 300 seeds per difficulty
    python scripts/balance.py --seeds 100 --difficulty hard

The greedy bot knows the static price structure (equilibrium prices of every city, which
a player learns after a few trips) plus its own ledger of observed prices. It does not see
hidden modifiers in other cities. It trades between neighbouring cities, keeps provisions,
hires a few guards, rests when morale is low, and runs home to pay the moneylender.
"""
from __future__ import annotations

import argparse
import os
import statistics
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from karvon import engine as E  # noqa: E402
from karvon.engine import data as D  # noqa: E402
from karvon.engine import market as M  # noqa: E402
from karvon.engine.events import expected_strength, pending_choices  # noqa: E402


# --------------------------------------------------------------------------- helpers
def est_sell(state: E.GameState, city: str, good: str) -> float:
    """What the bot expects to get per unit at ``city`` (ledger if fresh, else equilibrium)."""
    known = state.known.get(city, {}).get(good)
    if known and state.day - known[2] <= 8:
        return float(known[1])
    rep_adj = (state.rep - 50) / 50 * D.REP_PRICE_SWING
    p = D.equilibrium(city, good) * (1 - D.SPREAD) * (1 + rep_adj)
    if M.hostile_here(state, city):
        p *= 1 - D.HOSTILE_PENALTY
    return p


def est_mid(state: E.GameState, city: str, good: str) -> float:
    if city == state.city:
        return M.mid(state, city, good)
    return D.equilibrium(city, good)


def plan_cargo(
    state: E.GameState, src: str, dest: str, budget: int, space: int
) -> tuple[list[tuple[str, int]], float]:
    """Greedy marginal allocation of money and cargo slots for a trip ``src`` -> ``dest``."""
    mids = {g: est_mid(state, src, g) for g in D.GOOD_ORDER}
    target = {g: est_sell(state, dest, g) for g in D.GOOD_ORDER}
    bought: Counter = Counter()
    profit = 0.0
    money = budget
    for _ in range(max(0, space)):
        best = None
        for g in D.GOOD_ORDER:
            k = bought[g]
            imp = D.impact(g)
            buy_p = M._buy_from_mid(state, src, mids[g] * (1 + imp) ** k)
            if buy_p > money:
                continue
            sell_p = target[g] * (1 - imp) ** k
            margin = sell_p - buy_p
            if margin > max(1.0, buy_p * 0.05) and (best is None or margin / buy_p > best[0]):
                best = (margin / buy_p, g, buy_p, margin)
        if best is None:
            break
        _, g, buy_p, margin = best
        bought[g] += 1
        money -= buy_p
        profit += margin
    return [(g, n) for g, n in bought.items() if n > 0], profit


def trip_cost(state: E.GameState, src: str, dest: str, guards: int) -> float:
    road = D.road_between(src, dest)
    assert road
    days, _, terrain = road
    per_day = (D.CREW_BASE + guards + state.camels) * (2 if terrain == "desert" else 1)
    return days * (per_day * D.PROVISION_PRICE[src] + guards * D.GUARD_WAGE + 1.5)


def leg_value(state: E.GameState, src: str, dest: str, capital: int) -> tuple[float, int]:
    road = D.road_between(src, dest)
    assert road
    days, danger, terrain = road
    g = want_guards(state, danger, days, terrain == "desert")
    _, profit = plan_cargo(state, src, dest, capital, state.capacity)
    return profit - trip_cost(state, src, dest, g), days


def dist_home(city: str) -> int:
    return D.DIST[city][D.HOME]


def next_hop_home(city: str) -> str:
    best = None
    for other, days, _, _ in D.neighbours(city):
        d = days + D.DIST[other][D.HOME]
        if best is None or d < best[0]:
            best = (d, other)
    assert best
    return best[1]


def want_guards(state: E.GameState, danger: int, days: int = 5, desert: bool = False) -> int:
    if danger >= 2 and not state.flags.get("bw_done") and 40 <= state.day <= 65 and state.money > 900:
        g = 6
    elif danger >= 3:
        g = 3 if state.money > 600 else 2
    elif danger == 2:
        g = 2 if state.money > 300 else 1
    else:
        g = 1 if state.money > 900 else 0
    # never hire more mouths than the camels can feed on this road
    per_day_cap = state.prov_cap // (days * (2 if desert else 1)) - D.CREW_BASE - state.camels
    return max(0, min(g, per_day_cap))


# --------------------------------------------------------------------------- event policy
def choose(state: E.GameState) -> str:
    ev = state.pending["id"]
    p = state.pending["params"]
    ch = pending_choices(state)

    def pick(*prefs: str) -> str:
        for c in prefs:
            if c in ch:
                return c
        return ch[0]

    if ev == "bandits":
        if p["ours"] >= p["theirs"] + 5:
            return "fight"
        return pick("pay", "flee") if state.cargo_units else pick("flee")
    if ev == "black_wind":
        return "fight" if p["ours"] >= p["theirs"] else pick("tribute")
    if ev == "qorabek":
        return "refuse"
    table = {
        "sandstorm": ("shelter",),
        "sick_camel": ("treat", "slaughter"),
        "oasis": ("water",),
        "traveler": ("share", "pass"),
        "toll": ("talk", "pay", "detour"),
        "wolves": ("fight", "fire", "run") if state.guards >= 2 else ("fire", "run"),
        "merchant": ("decline",),
        "quarrel": ("bonus", "judge"),
        "dervish": ("alms", "listen"),
        "flood": ("save_camels",),
        "saddle": ("rope", "fix"),
        "cold": ("burn", "camp"),
        "abandoned": ("take", "leave"),
        "deserter": ("pay", "let_go"),
        "pilgrims": ("escort", "decline"),
        "dry_well": ("buy", "dig"),
        "festival": ("trade",),
        "plague": ("medicine", "endure"),
        "guild_tax": ("pay", "refuse"),
        "glut": ("note",),
        "wedding": ("decline",),
        "camel_fair": ("look",),
        "nilufar": ("pay",) if state.money > 400 else ("refuse",),
        "grateful": ("gift",),
        "letter": ("keep",),
    }
    return pick(*table.get(ev, ()))


# --------------------------------------------------------------------------- bots
def greedy_city_turn(state: E.GameState) -> None:
    city = state.city
    # 1. sell cargo (keep goods that sell far below cost here)
    for g in list(state.cargo):
        qty = state.cargo[g]
        avg = state.cargo_cost.get(g, 0) / qty if qty else 0
        elsewhere = max(est_sell(state, n, g) for n, *_ in D.neighbours(city))
        if M.sell_price(state, city, g) >= min(avg * 0.85, elsewhere * 0.9):
            E.sell(state, g, "all")
    # 2. story / quests
    if E.can_council(state):
        E.council(state)
    if E.can_deliver(state):
        E.deliver(state)
    # 3. moneylender
    if city == D.HOME and state.total_debt > 0:
        if state.money >= state.total_debt + 150:
            E.pay_debt(state, "all")
        elif state.day >= 55:
            reserve = 250 if state.day < 85 else 80
            if state.money - reserve > 0:
                E.pay_debt(state, state.money - reserve)
    if state.debt_paid and (state.day >= 130 or state.ended):
        if not state.ended:
            E.retire(state)
        return
    # 5. choose destination
    days_left = D.DEADLINE_DAY - state.day
    must_go_home = not state.debt_paid and days_left <= dist_home(city) + 6 and city != D.HOME
    options = []
    for dest, days, danger, terrain in D.neighbours(city):
        if must_go_home and dest != next_hop_home(city):
            continue
        if not state.debt_paid and state.day + days + dist_home(dest) > D.DEADLINE_DAY and dest != D.HOME:
            continue
        g = want_guards(state, danger, days, terrain == "desert")
        budget = state.money - max(0, g - state.guards) * D.GUARD_SIGNUP - 60
        plan, profit = plan_cargo(state, city, dest, max(0, budget), state.free_space)
        first = profit - trip_cost(state, city, dest, g)
        best2 = 0.0
        days2 = 5
        for nxt, *_ in D.neighbours(dest):
            v, d2 = leg_value(state, dest, nxt, int(max(0, budget) + max(0, first)))
            if v / d2 > best2 / days2:
                best2, days2 = v, d2
        score = (first + 0.8 * best2) / (days + days2)
        options.append((score, dest, plan, danger, days))
    if not options:
        dest = next_hop_home(city) if city != D.HOME else D.neighbours(city)[0][0]
        road = D.road_between(city, dest)
        assert road
        options.append((0, dest, [], road[1], road[0]))
    options.sort(key=lambda o: -o[0])
    _, dest, plan, danger, days = options[0]
    # 4. morale: arrive with a safety margin
    terrain = D.road_between(city, dest)[2]
    drift = days * {"desert": 2.5, "mountain": 1.5}.get(terrain, 1.0)
    while state.morale - drift < 35 and state.money >= E.rest_cost(state) + 40:
        E.rest(state)
        if state.pending or state.ended:
            return
    # 6. camels when capacity binds and there is cash
    if state.camels < 8 and state.money > 1400 and state.free_space < 10:
        E.buy_camels(state, 1)
    # 7. guards
    target = want_guards(state, danger, days, terrain == "desert")
    if state.guards < target:
        E.hire_guards(state, min(target - state.guards, max(0, state.money // D.GUARD_SIGNUP - 2)))
    elif state.guards > target + 1:
        E.dismiss_guards(state, state.guards - target)
    # 8. provisions (reserve them before buying goods)
    need = int(E.trip_need(state, dest) * 1.25) + 4
    if state.provisions < need:
        E.buy_provisions(state, need - state.provisions)
    # 9. buy goods per (re-computed) plan
    reserve = state.guards * D.GUARD_WAGE * (days + 2) + 30
    plan, _ = plan_cargo(state, city, dest, state.money - reserve, state.free_space)
    for g, n in plan:
        E.buy(state, g, n)
    if state.provisions < E.trip_need(state, dest):
        return  # cannot feed the caravan on this road: wait for better days
    E.travel_start(state, dest)


def run_greedy(seed: int, difficulty: str) -> E.GameState:
    s = E.new_game(seed, difficulty, "bot")
    for _ in range(3000):
        if s.ended:
            break
        if s.pending:
            E.resolve_event_choice(s, choose(s))
        elif s.on_road:
            E.ride_on(s)
        else:
            greedy_city_turn(s)
            if not s.ended and not s.pending and s.phase == "city":
                E.wait(s)
    return s


def run_idle(seed: int, difficulty: str) -> E.GameState:
    s = E.new_game(seed, difficulty, "idle")
    for _ in range(400):
        if s.ended:
            break
        if s.pending:
            ch = pending_choices(s)
            E.resolve_event_choice(s, "refuse" if "refuse" in ch else ch[-1])
        else:
            E.wait(s)
    return s


# --------------------------------------------------------------------------- report
def summarize(runs: list[E.GameState]) -> dict:
    n = len(runs)
    paid = [r for r in runs if r.paid_day > 0]
    ends = Counter(r.ending for r in runs)
    return {
        "n": n,
        "win": len(paid) / n if n else 0.0,
        "payday": statistics.mean(r.paid_day for r in paid) if paid else float("nan"),
        "ends": ends,
        "nw": statistics.median(r.stats.get("final_nw", 0) for r in runs) if runs else 0,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", type=int, default=300)
    ap.add_argument("--difficulty", default="all", choices=["all", *D.DIFFICULTY_ORDER])
    args = ap.parse_args(argv)
    diffs = D.DIFFICULTY_ORDER if args.difficulty == "all" else [args.difficulty]

    header = "| Bot | Difficulty | Runs | Debt paid | Avg payoff day | Median final net worth | Endings |"
    print(header)
    print("|---|---|---|---|---|---|---|")
    ok = True
    for diff in diffs:
        for label, fn in (("greedy", run_greedy), ("do-nothing", run_idle)):
            runs = [fn(seed, diff) for seed in range(1, args.seeds + 1)]
            st = summarize(runs)
            ends = " ".join(f"{k}:{v}" for k, v in sorted(st["ends"].items(), key=lambda kv: str(kv[0])))
            payday = "—" if st["payday"] != st["payday"] else f"{st['payday']:.1f}"
            print(
                f"| {label} | {diff} | {st['n']} | {st['win'] * 100:.1f}% | {payday} | {int(st['nw']):,} | {ends} |"
            )
            if label == "do-nothing" and st["win"] > 0:
                ok = False
    if not ok:
        print("\nWARNING: the do-nothing bot paid the debt in some runs!")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
