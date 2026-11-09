"""Player actions. Each validates its input and returns a ``Result``; none raise on bad input."""
from __future__ import annotations

import math
from typing import Any

from . import data as D
from . import market as M
from .core import clamp, diff, diff_cfg, remove_cargo, add_cargo, snapshot, stat
from .endings import check_failure, final_ending, finish, net_worth
from .events import EVENTS, pending_choices, roll_city_event, roll_road_event
from .rng import Rng, seed_state
from .state import GameState, Result


# --------------------------------------------------------------------------- new game
def new_game(seed: int, difficulty: str = "hard", name: str = "") -> GameState:
    if difficulty not in D.DIFFICULTIES:
        difficulty = "hard"
    cfg = D.DIFFICULTIES[difficulty]
    s = GameState(seed=int(seed), rng=seed_state(seed), difficulty=difficulty, name=str(name)[:64])
    s.money = cfg["money"]
    s.debt = cfg["debt"]
    s.camels = D.START_CAMELS
    s.provisions = D.START_PROVISIONS
    s.morale = D.START_MORALE
    s.rep = D.START_REP
    s.city = D.HOME
    s.phase = "city"
    s.visited = [D.HOME]
    rng = Rng(s)
    M.init_prices(s, rng)
    M.record_known(s, D.HOME)
    return s


# --------------------------------------------------------------------------- helpers
def _err(key: str, **params: Any) -> Result:
    return Result(False, key, params)


def _to_int(value: Any, default: int | None = None) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _check(state: GameState, where: str = "city") -> Result | None:
    if state.ended:
        return _err("err.ended")
    if state.pending:
        return _err("err.pending")
    if where == "city" and state.phase != "city":
        return _err("err.not_in_city")
    if where == "road" and not state.on_road:
        return _err("err.not_on_road")
    return None


def _settle(state: GameState, notes: list) -> None:
    """Clamp values and trigger failure endings."""
    clamp(state, notes)
    if state.ended:
        return
    if state.flags.get("sold_out"):
        finish(state, "E4", notes)
        return
    if state.flags.get("joined"):
        finish(state, "E8", notes)
        return
    ending = check_failure(state)
    if ending:
        finish(state, ending, notes)


def _pass_day(state: GameState, notes: list, on_road: bool) -> None:
    rng = Rng(state)
    state.day += 1
    if state.guards:
        wage = state.guards * D.GUARD_WAGE
        if state.money >= wage:
            state.money -= wage
        else:
            state.money = 0
            state.morale -= 6
            notes.append(("note.wages_unpaid", {}))
            if rng.chance(0.35):
                state.guards -= 1
                notes.append(("note.guard_left", {}))
    if on_road and state.travel is not None:
        stat(state, "road_days")
        desert = state.travel.get("terrain") == "desert"
        need = (state.crew + state.camels) * (2 if desert else 1)
        if state.provisions >= need:
            state.provisions -= need
            state.starving = 0
        else:
            state.provisions = 0
            state.starving += 1
            state.morale -= 10
            notes.append(("note.starving", {"n": max(0, 3 - state.starving)}))
        terrain = state.travel.get("terrain")
        if terrain == "desert":
            state.morale -= 2
        elif terrain == "mountain" or state.day % 2:
            state.morale -= 1
    if (
        state.day % D.INTEREST_EVERY == 0
        and state.day <= D.INTEREST_LAST_DAY
        and not state.debt_paid
        and state.total_debt > 0
    ):
        inc = math.ceil(state.debt * D.INTEREST_RATE) + math.ceil(state.loan * D.LOAN_RATE)
        state.debt += math.ceil(state.debt * D.INTEREST_RATE)
        state.loan += math.ceil(state.loan * D.LOAN_RATE)
        notes.append(("note.interest", {"money": inc, "debt": state.total_debt}))
    M.daily_update(state, rng)
    if state.contract and state.day > state.contract["until"]:
        notes.append(("note.contract_failed", {"good": state.contract["good"], "city": state.contract["city"]}))
        state.contract = None
        state.rep -= 5
    if state.camel_deal and state.day > state.camel_deal["until"]:
        state.camel_deal = None
    if state.phase == "city":
        M.record_known(state, state.city)
    if state.day == D.DEADLINE_DAY - 10 and not state.debt_paid:
        notes.append(("note.deadline_near", {"n": 10}))
    _settle(state, notes)


def _result(state: GameState, before: dict, key: str, params: dict | None = None, notes: list | None = None) -> Result:
    return Result(True, key, params or {}, diff(before, state), notes or [])


def _good(good: Any) -> str | None:
    return good if isinstance(good, str) and good in D.GOODS else None


# --------------------------------------------------------------------------- market
def buy(state: GameState, good: Any, qty: Any) -> Result:
    if (e := _check(state)):
        return e
    good = _good(good)
    if good is None:
        return _err("err.bad_input")
    city = state.city
    if qty == "max":
        n = M.max_affordable(state, city, good)
    else:
        n = _to_int(qty)
        if n is None or n <= 0 or n > 500:
            return _err("err.bad_input")
    if state.free_space <= 0:
        return _err("err.no_space")
    n = min(n, state.free_space)
    if n <= 0:
        return _err("err.no_money")
    cost = M.quote_buy(state, city, good, n)
    if cost > state.money:
        n = M.max_affordable(state, city, good, limit=n)
        if n <= 0:
            return _err("err.no_money")
        cost = M.quote_buy(state, city, good, n)
    before = snapshot(state)
    state.money -= cost
    add_cargo(state, good, n, cost)
    M.apply_trade(state, city, good, n, buying=True)
    M.record_known(state, city)
    stat(state, "trades")
    return _result(state, before, "ok.bought", {"good": good, "n": n, "money": cost})


def sell(state: GameState, good: Any, qty: Any) -> Result:
    if (e := _check(state)):
        return e
    good = _good(good)
    if good is None:
        return _err("err.bad_input")
    have = state.cargo.get(good, 0)
    if have <= 0:
        return _err("err.no_goods")
    if qty == "all":
        n = have
    else:
        n = _to_int(qty)
        if n is None or n <= 0 or n > 500:
            return _err("err.bad_input")
        n = min(n, have)
    city = state.city
    before = snapshot(state)
    revenue = M.quote_sell(state, city, good, n)
    basis = remove_cargo(state, good, n)
    state.money += revenue
    M.apply_trade(state, city, good, n, buying=False)
    M.record_known(state, city)
    stat(state, "trades")
    stat(state, "profit", revenue - basis)
    return _result(state, before, "ok.sold", {"good": good, "n": n, "money": revenue, "profit": revenue - basis})


# --------------------------------------------------------------------------- stable / guards / provisions
def camel_price(state: GameState) -> int:
    deal = state.camel_deal
    if deal and deal["city"] == state.city and deal["until"] >= state.day:
        return deal["price"]
    return D.CAMEL_PRICE[state.city]


def buy_camels(state: GameState, n: Any = 1) -> Result:
    if (e := _check(state)):
        return e
    n = _to_int(n)
    if n is None or n <= 0 or n > D.MAX_CAMELS:
        return _err("err.bad_input")
    if state.camels + n > D.MAX_CAMELS:
        return _err("err.max_camels", n=D.MAX_CAMELS)
    price = camel_price(state)
    if state.money < price * n:
        return _err("err.no_money")
    before = snapshot(state)
    state.money -= price * n
    state.camels += n
    return _result(state, before, "ok.camels_bought", {"n": n, "money": price * n})


def sell_camels(state: GameState, n: Any = 1) -> Result:
    if (e := _check(state)):
        return e
    n = _to_int(n)
    if n is None or n <= 0:
        return _err("err.bad_input")
    if state.camels - n < 1:
        return _err("err.last_camel")
    if state.cargo_units > (state.camels - n) * D.SLOTS_PER_CAMEL:
        return _err("err.cargo_wont_fit")
    before = snapshot(state)
    state.camels -= n
    state.money += D.CAMEL_SELL_PRICE * n
    notes: list = []
    clamp(state, notes)  # provisions above the new cap are lost
    return _result(state, before, "ok.camels_sold", {"n": n, "money": D.CAMEL_SELL_PRICE * n}, notes)


def hire_guards(state: GameState, n: Any = 1) -> Result:
    if (e := _check(state)):
        return e
    n = _to_int(n)
    if n is None or n <= 0 or n > D.MAX_GUARDS:
        return _err("err.bad_input")
    if state.guards + n > D.MAX_GUARDS:
        return _err("err.max_guards", n=D.MAX_GUARDS)
    cost = D.GUARD_SIGNUP * n
    if state.money < cost:
        return _err("err.no_money")
    before = snapshot(state)
    state.money -= cost
    state.guards += n
    return _result(state, before, "ok.guards_hired", {"n": n, "money": cost})


def dismiss_guards(state: GameState, n: Any = 1) -> Result:
    if (e := _check(state)):
        return e
    n = _to_int(n)
    if n is None or n <= 0:
        return _err("err.bad_input")
    if state.guards < n:
        return _err("err.no_guards")
    before = snapshot(state)
    state.guards -= n
    return _result(state, before, "ok.guards_dismissed", {"n": n})


def provision_price(state: GameState) -> int:
    return D.PROVISION_PRICE[state.city]


def trip_need(state: GameState, dst: str) -> int:
    road = D.road_between(state.city, dst)
    if road is None:
        return 0
    days, _, terrain = road
    return days * (state.crew + state.camels) * (2 if terrain == "desert" else 1)


def buy_provisions(state: GameState, n: Any) -> Result:
    if (e := _check(state)):
        return e
    room = state.prov_cap - state.provisions
    if room <= 0:
        return _err("err.prov_full")
    price = provision_price(state)
    if n == "max":
        n = min(room, state.money // price)
    else:
        n = _to_int(n)
        if n is None or n <= 0 or n > 1000:
            return _err("err.bad_input")
        n = min(n, room, state.money // price)
    if n <= 0:
        return _err("err.no_money")
    before = snapshot(state)
    state.money -= n * price
    state.provisions += n
    return _result(state, before, "ok.provisions", {"n": n, "money": n * price})


# --------------------------------------------------------------------------- caravanserai / teahouse
def rest_cost(state: GameState) -> int:
    if state.city == "khi" and state.flags.get("nilufar_ally"):
        return 0
    return state.crew * D.REST_COST_PERSON + state.camels * D.REST_COST_CAMEL


def rest(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    cost = rest_cost(state)
    if state.money < cost:
        return _err("err.no_money")
    before = snapshot(state)
    notes: list = []
    state.money -= cost
    state.morale += D.REST_MORALE
    _pass_day(state, notes, on_road=False)
    if not state.ended:
        roll_city_event(state, Rng(state), arrival=False)
    return _result(state, before, "ok.rested", {"money": cost}, notes)


def wait(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    before = snapshot(state)
    notes: list = []
    _pass_day(state, notes, on_road=False)
    if not state.ended:
        roll_city_event(state, Rng(state), arrival=False)
    return _result(state, before, "ok.waited", {}, notes)


def rumor_cost(state: GameState) -> int:
    if state.city == "khi" and state.flags.get("nilufar_ally"):
        return 0
    return D.RUMOR_COST


def rumor(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    cost = rumor_cost(state)
    if state.money < cost:
        return _err("err.no_money")
    before = snapshot(state)
    state.money -= cost
    rng = Rng(state)
    nilufar = state.city == "khi" and state.flags.get("nilufar_ally")
    info = M.make_rumor(state, rng, create=bool(nilufar) or rng.chance(0.6))
    stat(state, "rumors")
    return _result(state, before, "ok.rumor_" + info["kind"], info)


# --------------------------------------------------------------------------- travel
def travel_start(state: GameState, dest: Any) -> Result:
    if (e := _check(state)):
        return e
    if not isinstance(dest, str) or dest not in D.CITIES:
        return _err("err.bad_input")
    road = D.road_between(state.city, dest)
    if road is None:
        return _err("err.no_road")
    days, danger, terrain = road
    if state.flags.get("exposed"):
        danger = max(1, danger - 1)
    before = snapshot(state)
    state.travel = {"src": state.city, "dst": dest, "total": days, "done": 0, "danger": danger, "terrain": terrain}
    state.phase = "road"
    state.camel_deal = None
    stat(state, "trips")
    return _result(state, before, "ok.departed", {"city": dest})


def _road_step(state: GameState, notes: list) -> None:
    _pass_day(state, notes, on_road=True)
    if state.ended or state.travel is None:
        return
    state.travel["done"] += 1
    rng = Rng(state)
    if state.travel["done"] >= state.travel["total"]:
        dst = state.travel["dst"]
        state.city = dst
        state.travel = None
        state.phase = "city"
        first = dst not in state.visited
        if first:
            state.visited.append(dst)
        M.record_known(state, dst)
        state.morale = min(100, state.morale + D.ARRIVAL_MORALE)
        notes.append(("note.arrived", {"city": dst}))
        if state.contract and state.contract["city"] == dst:
            notes.append(("note.contract_here", {"good": state.contract["good"], "n": state.contract["qty"]}))
        roll_city_event(state, rng, arrival=True)
    else:
        roll_road_event(state, rng)


def next_day(state: GameState) -> Result:
    if (e := _check(state, "road")):
        return e
    before = snapshot(state)
    notes: list = []
    _road_step(state, notes)
    return _result(state, before, "ok.day", {}, notes)


def ride_on(state: GameState, max_days: int = 40) -> Result:
    if (e := _check(state, "road")):
        return e
    before = snapshot(state)
    notes: list = []
    days = 0
    while days < max_days and state.on_road and not state.pending and not state.ended:
        _road_step(state, notes)
        days += 1
    # keep notes readable: collapse repeats, keep the last of each kind
    seen: dict = {}
    for k, p in notes:
        seen.pop(k, None)
        seen[k] = p
    return _result(state, before, "ok.rode", {"days": days}, list(seen.items()))


# --------------------------------------------------------------------------- events
def resolve_event_choice(state: GameState, choice: Any) -> Result:
    if state.ended:
        return _err("err.ended")
    if not state.pending:
        return _err("err.no_event")
    ev_id = state.pending["id"]
    if not isinstance(choice, str) or choice not in pending_choices(state):
        return _err("err.bad_choice")
    ev = EVENTS[ev_id]
    before = snapshot(state)
    notes: list = []
    params = dict(state.pending["params"])
    rng = Rng(state)
    outcome, extra = ev.resolve(state, params, choice, rng, notes)
    state.pending = None
    _settle(state, notes)
    out_params = {**params, **extra}
    return _result(state, before, f"ev.{ev_id}.r.{outcome}", out_params, notes)


# --------------------------------------------------------------------------- moneylender
def pay_debt(state: GameState, amount: Any) -> Result:
    if (e := _check(state)):
        return e
    if state.city != D.HOME:
        return _err("err.not_here")
    if state.total_debt <= 0:
        return _err("err.no_debt")
    if amount == "all":
        n = min(state.money, state.total_debt)
    else:
        n = _to_int(amount)
        if n is None or n <= 0:
            return _err("err.bad_input")
        n = min(n, state.money, state.total_debt)
    if n <= 0:
        return _err("err.no_money")
    before = snapshot(state)
    notes: list = []
    state.money -= n
    from_loan = min(state.loan, n)
    state.loan -= from_loan
    state.debt -= n - from_loan
    if state.total_debt == 0:
        state.paid_day = state.day
        state.rep += 5
        notes.append(("note.debt_cleared", {"n": state.day}))
        clamp(state)
        return _result(state, before, "ok.debt_cleared", {"money": n}, notes)
    return _result(state, before, "ok.paid", {"money": n, "debt": state.total_debt}, notes)


def can_borrow(state: GameState) -> bool:
    return (
        not state.loan_taken
        and not state.debt_paid
        and state.day <= D.INTEREST_LAST_DAY
        and state.city == D.HOME
        and state.phase == "city"
    )


def borrow(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    if state.city != D.HOME:
        return _err("err.not_here")
    if not can_borrow(state):
        return _err("err.no_loan")
    before = snapshot(state)
    state.loan_taken = True
    state.loan += D.LOAN_AMOUNT
    state.money += D.LOAN_AMOUNT
    return _result(state, before, "ok.borrowed", {"money": D.LOAN_AMOUNT})


# --------------------------------------------------------------------------- story & quests
def can_council(state: GameState) -> bool:
    f = state.flags
    return (
        state.phase == "city"
        and state.city == D.HOME
        and bool(f.get("letter"))
        and bool(f.get("token"))
        and not f.get("exposed")
    )


def council(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    if not can_council(state):
        return _err("err.not_here")
    before = snapshot(state)
    state.flags["exposed"] = True
    state.flags["hostile"] = False
    state.rep += 30
    state.money += D.COUNCIL_REWARD
    notes: list = []
    clamp(state, notes)
    return _result(state, before, "ok.council", {"money": D.COUNCIL_REWARD}, notes)


def can_deliver(state: GameState) -> bool:
    c = state.contract
    return bool(
        c
        and state.phase == "city"
        and state.city == c["city"]
        and state.cargo.get(c["good"], 0) >= c["qty"]
        and state.day <= c["until"]
    )


def deliver(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    if not can_deliver(state):
        return _err("err.cannot_deliver")
    c = state.contract
    assert c is not None
    before = snapshot(state)
    remove_cargo(state, c["good"], c["qty"])
    state.money += c["reward"]
    state.rep += 6
    state.contract = None
    stat(state, "contracts")
    notes: list = []
    clamp(state, notes)
    return _result(state, before, "ok.delivered", {"money": c["reward"]}, notes)


def retire(state: GameState) -> Result:
    if (e := _check(state)):
        return e
    if not state.debt_paid:
        return _err("err.debt_first")
    before = snapshot(state)
    notes: list = []
    finish(state, final_ending(state), notes)
    return _result(state, before, "ok.retired", {}, notes)


__all__ = [
    "new_game",
    "buy",
    "sell",
    "buy_camels",
    "sell_camels",
    "hire_guards",
    "dismiss_guards",
    "buy_provisions",
    "rest",
    "wait",
    "rumor",
    "travel_start",
    "next_day",
    "ride_on",
    "resolve_event_choice",
    "pay_debt",
    "borrow",
    "council",
    "deliver",
    "retire",
    "camel_price",
    "provision_price",
    "rest_cost",
    "rumor_cost",
    "trip_need",
    "can_borrow",
    "can_council",
    "can_deliver",
    "net_worth",
    "diff_cfg",
]
