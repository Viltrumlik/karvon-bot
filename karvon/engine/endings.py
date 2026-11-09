"""Ending evaluation, net worth and scoring."""
from __future__ import annotations

from . import data as D
from .core import diff_cfg
from .market import cargo_value
from .state import GameState


def valuation_city(state: GameState) -> str:
    if state.travel is not None:
        return state.travel["dst"]
    return state.city


def net_worth(state: GameState) -> int:
    return (
        state.money
        + cargo_value(state, valuation_city(state))
        + state.camels * D.CAMEL_SELL_PRICE
        - state.total_debt
    )


def final_ending(state: GameState) -> str:
    """Ending for a run whose debt was paid (retirement or day 150)."""
    nw = net_worth(state)
    if state.flags.get("exposed") and nw >= D.NW_LEGEND:
        return "E1"
    if nw >= D.NW_HONEST:
        return "E2"
    return "E3"


def check_failure(state: GameState) -> str | None:
    """Endings that can trigger at any moment (checked after every state change)."""
    if state.morale <= 0:
        return "E7"
    if state.camels <= 0 or state.starving >= 3:
        return "E6"
    if state.day > D.DEADLINE_DAY and not state.debt_paid:
        return "E5"
    if state.day >= D.FINAL_DAY and state.debt_paid:
        return final_ending(state)
    return None


def compute_score(state: GameState, ending: str) -> int:
    nw = net_worth(state)
    if ending == "E4":
        base = D.QORABEK_BUYOUT
    elif ending in ("E5", "E6", "E7"):
        base = max(0, nw) // 4 + state.day * 2
    else:
        base = max(0, nw) + D.ENDING_BONUS.get(ending, 0)
        if state.debt_paid:
            base += max(0, D.DEADLINE_DAY - state.paid_day) * 25
    return int(round(base * diff_cfg(state)["score"]))


def finish(state: GameState, ending: str, notes: list | None = None) -> None:
    if state.phase == "ended":
        return
    state.ending = ending
    state.score = compute_score(state, ending)
    state.stats["final_nw"] = net_worth(state)
    state.phase = "ended"
    state.pending = None
    if notes is not None:
        notes.append(("note.ending", {"ending": ending}))
