"""Each of the 8 endings is reachable through the public engine API from a prepared state."""
from __future__ import annotations

import pytest

from karvon import engine as E
from karvon.engine import data as D
from karvon.engine.events import EVENTS
from karvon.engine.rng import Rng


@pytest.fixture(autouse=True)
def no_random_events(monkeypatch):
    monkeypatch.setattr(D, "EVENT_BASE", -1.0)
    monkeypatch.setattr(D, "EVENT_PER_DANGER", 0.0)
    monkeypatch.setattr(D, "CITY_EVENT_CHANCE", 0.0)


def game() -> E.GameState:
    g = E.new_game(42, "hard", "Tester")
    g.flags["qorabek_done"] = True  # keep the story offer out of the way unless a test wants it
    return g


def pend(g: E.GameState, ev_id: str) -> None:
    ctx = {"danger": 2, "terrain": "desert", "city": g.city}
    g.pending = {"id": ev_id, "params": EVENTS[ev_id].setup(g, ctx, Rng(g)), "src": "road"}


def pay_off(g: E.GameState, money: int) -> None:
    g.money = g.total_debt + money
    assert E.pay_debt(g, "all").key == "ok.debt_cleared"


def test_e1_legend():
    g = game()
    g.flags.update(exposed=True)
    pay_off(g, 15000)
    assert E.retire(g).ok
    assert g.ending == "E1" and g.score > 0


def test_e1_requires_exposure():
    g = game()
    pay_off(g, 15000)
    E.retire(g)
    assert g.ending == "E2"


def test_e2_honest_trader():
    g = game()
    pay_off(g, 6000)
    E.retire(g)
    assert g.ending == "E2"


def test_e3_free_but_poor():
    g = game()
    pay_off(g, 50)
    E.retire(g)
    assert g.ending == "E3"


def test_final_day_150_retires_automatically():
    g = game()
    pay_off(g, 50)
    g.day = D.FINAL_DAY - 1
    E.wait(g)
    assert g.ending == "E3" and g.ended


def test_e4_qorabek_clerk():
    g = game()
    g.flags["qorabek_done"] = False
    g.city = "buk"
    pend(g, "qorabek")
    res = E.resolve_event_choice(g, "accept")
    assert res.ok and g.ending == "E4" and g.score > 0


def test_e5_debt_slave():
    g = game()
    g.day = D.DEADLINE_DAY
    E.wait(g)
    assert g.ending == "E5"


def test_e5_not_triggered_when_paid():
    g = game()
    pay_off(g, 0)
    g.day = D.DEADLINE_DAY
    E.wait(g)
    assert not g.ended


def test_e6_lost_camels():
    g = game()
    g.camels = 1
    g.provisions = 25
    E.travel_start(g, "buk")
    pend(g, "sick_camel")
    E.resolve_event_choice(g, "leave")
    assert g.ending == "E6"


def test_e6_starvation():
    g = game()
    g.provisions = 0
    E.travel_start(g, "tas")
    E.ride_on(g)
    assert g.ending == "E6" and g.starving == 3


def test_e7_mutiny():
    g = game()
    g.morale = 1
    g.provisions = 100
    g.city = "buk"
    E.travel_start(g, "khi")  # desert: -2 morale a day
    E.next_day(g)
    assert g.ending == "E7"


def test_e8_black_wind_partner():
    g = game()
    g.rep = 10
    E.travel_start(g, "buk")
    pend(g, "black_wind")
    assert "join" in E.pending_choices(g)
    E.resolve_event_choice(g, "join")
    assert g.ending == "E8"


def test_join_needs_low_reputation():
    g = game()
    g.rep = 50
    E.travel_start(g, "buk")
    pend(g, "black_wind")
    assert "join" not in E.pending_choices(g)


def test_black_wind_victory_gives_signet():
    g = game()
    g.guards = 12
    g.morale = 100
    E.travel_start(g, "buk")
    pend(g, "black_wind")
    g.pending["params"]["enemy"] = 10
    res = E.resolve_event_choice(g, "fight")
    assert res.key == "ev.black_wind.r.fight_win" and g.flags["token"]


def test_actions_after_ending_are_rejected():
    g = game()
    g.day = D.DEADLINE_DAY
    E.wait(g)
    assert E.buy(g, "silk", 1).key == "err.ended"
    assert E.wait(g).key == "err.ended"
