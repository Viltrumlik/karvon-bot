"""Engine unit tests: market, capacity, provisions, wages, interest, fights, serialisation, determinism."""
from __future__ import annotations

import json

import pytest

from karvon import engine as E
from karvon.engine import data as D
from karvon.engine import market as M
from karvon.engine.events import EVENTS, bandit_strength, expected_strength, fight, player_strength
from karvon.engine.rng import Rng


def city_game(seed: int = 1, difficulty: str = "hard") -> E.GameState:
    return E.new_game(seed, difficulty, "Tester")


def on_road(g: E.GameState, dest: str = "buk") -> E.GameState:
    g.provisions = g.prov_cap
    res = E.travel_start(g, dest)
    assert res.ok, res.key
    return g


def quiet(monkeypatch) -> None:
    """No random road events / world shocks: isolates the mechanic under test."""
    monkeypatch.setattr(D, "EVENT_BASE", -1.0)
    monkeypatch.setattr(D, "EVENT_PER_DANGER", 0.0)
    monkeypatch.setattr(D, "CITY_EVENT_CHANCE", 0.0)
    monkeypatch.setattr(D, "WORLD_SHOCK_CHANCE", 0.0)


# --------------------------------------------------------------------------- setup
@pytest.mark.parametrize("difficulty", D.DIFFICULTY_ORDER)
def test_new_game_follows_difficulty(difficulty):
    g = city_game(3, difficulty)
    cfg = D.DIFFICULTIES[difficulty]
    assert g.debt == cfg["debt"] and g.money == cfg["money"]
    assert (g.camels, g.provisions, g.morale, g.rep, g.day) == (4, 40, 70, 30, 1)
    assert g.city == "sam" and g.phase == "city" and set(g.prices) == set(D.CITIES)


def test_world_matches_gdd():
    assert len(D.CITIES) == 7 and len(D.ROADS) == 7 and len(D.GOODS) == 10
    for good, producer in D.PRODUCER.items():
        cheapest = min(D.CITIES, key=lambda c: D.equilibrium(c, good))
        assert cheapest == producer
        assert D.price_factor(producer, good) == pytest.approx(0.55)


# --------------------------------------------------------------------------- market
def test_buying_raises_and_selling_lowers_price():
    g = city_game()
    before = M.mid(g, "sam", "paper")
    assert E.buy(g, "paper", 10).ok
    after_buy = M.mid(g, "sam", "paper")
    assert after_buy == pytest.approx(before * (1 + D.impact("paper")) ** 10, rel=1e-3)
    assert E.sell(g, "paper", 10).ok
    assert M.mid(g, "sam", "paper") < after_buy


def test_buy_price_above_sell_price_and_quotes_grow():
    g = city_game()
    for good in D.GOOD_ORDER:
        assert M.buy_price(g, "sam", good) >= M.sell_price(g, "sam", good)
        assert M.quote_buy(g, "sam", good, 10) >= 10 * M.buy_price(g, "sam", good)
        assert M.quote_sell(g, "sam", good, 10) <= 10 * M.sell_price(g, "sam", good)


def test_prices_drift_back_to_equilibrium(monkeypatch):
    quiet(monkeypatch)
    monkeypatch.setattr(D, "NOISE", 0.0)
    g = city_game()
    eq = D.equilibrium("buk", "silk")
    g.prices["buk"]["silk"] = eq * 2
    rng = Rng(g)
    for _ in range(40):
        M.daily_update(g, rng)
    assert g.prices["buk"]["silk"] == pytest.approx(eq, rel=0.03)


def test_random_walk_is_bounded():
    g = city_game(9)
    rng = Rng(g)
    for _ in range(300):
        M.daily_update(g, rng)
    for city in D.CITIES:
        for good in D.GOOD_ORDER:
            eq = D.equilibrium(city, good)
            assert eq * D.PRICE_MIN_MULT - 1e-6 <= g.prices[city][good] <= eq * D.PRICE_MAX_MULT + 1e-6


def test_glut_and_shortage_modifiers():
    g = city_game()
    p = M.mid(g, "her", "tea")
    M.add_mod(g, "her", "tea", 1.6, 10)
    assert M.mid(g, "her", "tea") == pytest.approx(p * 1.6, rel=1e-3)
    assert M.target_price(g, "her", "tea") == pytest.approx(D.equilibrium("her", "tea") * 1.6)
    g.day += 11
    M.daily_update(g, Rng(g))
    assert not g.mods


# --------------------------------------------------------------------------- capacity
def test_capacity_limits():
    g = city_game()
    g.money = 100000
    res = E.buy(g, "paper", 500)
    assert res.ok and g.cargo_units == g.capacity == 40
    assert E.buy(g, "iron", 1).key == "err.no_space"
    assert E.buy_camels(g, 1).ok
    assert g.capacity == 50 and g.free_space == 10


def test_buy_is_limited_by_money():
    g = city_game()
    g.money = 30
    res = E.buy(g, "silk", 5)
    assert res.key == "err.no_money"
    res = E.buy(g, "paper", "max")
    assert res.ok and g.money >= 0 and g.money < M.buy_price(g, "sam", "paper")


def test_losing_camels_drops_cargo_and_provisions():
    g = city_game()
    g.money = 100000
    E.buy(g, "paper", 40)
    g.provisions = 100
    g.camels = 2
    notes: list = []
    from karvon.engine.core import clamp

    clamp(g, notes)
    assert g.cargo_units == 20 and g.provisions == 50
    assert notes and notes[0][0] == "note.cargo_dropped"


def test_cannot_sell_last_camel_or_overloaded_camel():
    g = city_game()
    g.camels = 1
    assert E.sell_camels(g, 1).key == "err.last_camel"
    g = city_game()
    g.money = 10000
    E.buy(g, "paper", 40)
    assert E.sell_camels(g, 1).key == "err.cargo_wont_fit"


# --------------------------------------------------------------------------- provisions & wages
def test_provisions_and_wages_per_road_day(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    g.money = 1000
    E.hire_guards(g, 2)
    on_road(g, "buk")  # steppe
    prov, money = g.provisions, g.money
    E.next_day(g)
    assert prov - g.provisions == g.crew + g.camels == 8
    assert money - g.money == 2 * D.GUARD_WAGE


def test_desert_doubles_food(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    g.city = "buk"
    on_road(g, "khi")
    prov = g.provisions
    E.next_day(g)
    assert prov - g.provisions == 2 * (g.crew + g.camels)


def test_unpaid_wages_hurt_morale(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    g.money = 60
    E.hire_guards(g, 2)
    on_road(g)
    g.money = 0
    morale = g.morale
    res = E.next_day(g)
    assert any(k == "note.wages_unpaid" for k, _ in res.notes)
    assert g.morale <= morale - 6


def test_starvation_three_days_is_lost(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    g.city = "tas"
    on_road(g, "kas")
    g.provisions = 0
    for _ in range(3):
        E.next_day(g)
    assert g.ending == "E6"


def test_rest_restores_morale_and_costs_money(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    g.morale = 40
    cost = E.rest_cost(g)
    res = E.rest(g)
    assert res.ok and g.morale == 40 + D.REST_MORALE and res.deltas["money"] == -cost and g.day == 2


# --------------------------------------------------------------------------- debt
def test_interest_schedule(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    debts = {}
    for _ in range(99):
        E.wait(g)
        if g.pending:
            g.pending = None
        debts[g.day] = g.debt
    assert debts[9] == 3000
    assert debts[10] == 3090
    assert debts[19] == 3090 and debts[20] == 3183
    charged = [d for d in range(2, 100) if debts[d] != debts.get(d - 1, 3000)]
    assert charged == [10, 20, 30, 40, 50, 60, 70, 80, 90]


def test_loan_and_payment(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    assert E.borrow(g).ok and g.loan == 1000 and g.money == 1400
    assert E.borrow(g).key == "err.no_loan"
    for _ in range(10):
        E.wait(g)
        g.pending = None
    assert g.loan == 1050 and g.debt == 3090
    g.money = 10000
    res = E.pay_debt(g, 1000)
    assert res.ok and g.loan == 50  # the dearer loan is repaid first
    res = E.pay_debt(g, "all")
    assert res.key == "ok.debt_cleared" and g.debt_paid and g.total_debt == 0


def test_pay_only_in_samarkand():
    g = city_game()
    g.city = "buk"
    assert E.pay_debt(g, 100).key == "err.not_here"


# --------------------------------------------------------------------------- fights
def test_fight_strength_bounds_and_monotonicity():
    g = city_game()
    rng = Rng(g)
    for guards in range(0, 13):
        g.guards = guards
        lo = guards * 10 + g.camels + g.morale / 10 + 1
        for _ in range(50):
            assert lo <= player_strength(g, rng) <= lo + 5
    g.guards = 0
    weak = expected_strength(g)
    g.guards = 3
    assert expected_strength(g) == weak + 30


def test_bandit_strength_bounds():
    g = city_game()
    rng = Rng(g)
    for danger in (1, 2, 3):
        for _ in range(50):
            s = bandit_strength(g, danger, rng)
            base = 10 + 5 * danger + g.day * 0.25
            assert base * 0.85 - 1 <= s <= base * 1.15 + 1


def test_strong_caravan_beats_weak_bandits():
    g = city_game()
    rng = Rng(g)
    g.guards = 10
    assert all(fight(g, 20, rng) for _ in range(100))
    g.guards = 0
    assert not any(fight(g, 200, rng) for _ in range(100))


# --------------------------------------------------------------------------- events
def test_event_catalogue_size():
    road = [k for k, v in EVENTS.items() if v.kind == "road"]
    city = [k for k, v in EVENTS.items() if v.kind == "city"]
    assert len(road) >= 16 and len(city) >= 5
    assert "black_wind" in EVENTS and "qorabek" in EVENTS and "letter" in EVENTS


@pytest.mark.parametrize("ev_id", sorted(EVENTS))
def test_every_event_choice_resolves(ev_id):
    for seed in range(1, 6):
        base = city_game(seed)
        base.money, base.provisions, base.guards = 500, 100, 3
        base.rep = 10
        E.buy(base, "furs", 3)
        E.buy(base, "cotton", 3)
        if EVENTS[ev_id].kind != "city" and ev_id not in ("qorabek", "letter", "nilufar", "grateful"):
            base.travel = {"src": "sam", "dst": "buk", "total": 5, "done": 1, "danger": 2, "terrain": "mountain"}
            base.phase = "road"
        ctx = {"danger": 2, "terrain": "mountain", "city": "sam"}
        params = EVENTS[ev_id].setup(base, ctx, Rng(base))
        base.pending = {"id": ev_id, "params": params, "src": "road"}
        for choice in E.pending_choices(base):
            g = E.GameState.from_json(base.to_json())
            res = E.resolve_event_choice(g, choice)
            assert res.ok and res.key.startswith(f"ev.{ev_id}.r."), res.key
            assert g.pending is None


def test_bad_input_never_raises():
    g = city_game()
    garbage = [None, "", "x", -5, 10**9, "max", "all", {"a": 1}, 3.5]
    for value in garbage:
        for fn in (E.buy, E.sell):
            for good in (value, "silk"):
                assert isinstance(fn(g, good, value), E.Result)
        for fn in (E.buy_camels, E.sell_camels, E.hire_guards, E.dismiss_guards, E.buy_provisions, E.pay_debt):
            assert isinstance(fn(g, value), E.Result)
        assert isinstance(E.travel_start(g, value), E.Result)
        assert isinstance(E.resolve_event_choice(g, value), E.Result)
    assert E.next_day(g).key == "err.not_on_road"
    assert E.retire(g).key == "err.debt_first"


# --------------------------------------------------------------------------- story
def test_council_exposes_qorabek(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    assert E.council(g).key == "err.not_here"
    g.flags.update(letter=True, token=True, hostile=True, qorabek_done=True)
    res = E.council(g)
    assert res.ok and g.flags["exposed"] and not g.flags["hostile"] and g.rep == 60
    on_road(g, "buk")
    assert g.travel["danger"] == 1  # danger 1 roads stay at 1
    g2 = city_game()
    g2.flags.update(exposed=True, qorabek_done=True)
    g2.city = "mer"
    on_road(g2, "her")
    assert g2.travel["danger"] == 2  # 3 -> 2 after exposure


def test_qorabek_offer_triggers_on_first_bukhara_visit(monkeypatch):
    quiet(monkeypatch)
    g = city_game()
    on_road(g, "buk")
    E.ride_on(g)
    assert g.pending and g.pending["id"] == "qorabek"


# --------------------------------------------------------------------------- serialisation / determinism
def play_script(seed: int) -> E.GameState:
    g = city_game(seed)
    E.buy(g, "paper", 12)
    E.buy(g, "iron", 3)
    E.travel_start(g, "buk")
    for _ in range(200):
        if g.ended:
            break
        if g.pending:
            E.resolve_event_choice(g, E.pending_choices(g)[-1])
        elif g.on_road:
            E.ride_on(g)
        else:
            for good in list(g.cargo):
                E.sell(g, good, "all")
            E.buy_provisions(g, 30)
            E.buy(g, "carpets" if g.city == "buk" else "paper", 6)
            E.travel_start(g, "sam" if g.city != "sam" else "buk")
    return g


def test_serialisation_round_trip():
    g = play_script(11)
    raw = g.to_json()
    g2 = E.GameState.from_json(raw)
    assert g2.to_json() == raw
    assert json.loads(raw)["seed"] == 11


def test_resume_after_save_continues_identically():
    a = play_script(5)
    b = E.GameState.from_json(a.to_json())
    for g in (a, b):
        if g.ended:
            continue
        if g.pending:
            E.resolve_event_choice(g, E.pending_choices(g)[0])
        elif g.on_road:
            E.ride_on(g)
        else:
            E.wait(g)
    assert a.to_json() == b.to_json()


def test_determinism_same_seed_same_actions():
    assert play_script(7).to_json() == play_script(7).to_json()
    assert play_script(7).to_json() != play_script(8).to_json()
