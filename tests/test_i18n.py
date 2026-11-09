"""i18n completeness: identical keys, identical placeholders, no empty strings, all engine keys present."""
from __future__ import annotations

import re

import pytest

from karvon.engine import data as D
from karvon.engine.events import EVENTS
from karvon.i18n import LANGS, STRINGS, fmt_days, fmt_num, placeholders, t
from karvon.bot.render import TIP_BY_SCREEN

CITY_FORM = re.compile(r"_(in|to|from)$")


def norm(template: str) -> set[str]:
    """City placeholders may use any grammatical form ({city}, {city_in}, {city_to}, {city_from})."""
    return {CITY_FORM.sub("", p) for p in placeholders(template)}


def test_identical_key_sets():
    base = set(STRINGS["en"])
    for lang in LANGS:
        assert set(STRINGS[lang]) == base, f"{lang}: {set(STRINGS[lang]) ^ base}"


@pytest.mark.parametrize("lang", ["uz", "ru"])
def test_same_placeholders(lang):
    bad = [k for k, v in STRINGS["en"].items() if norm(v) != norm(STRINGS[lang][k])]
    assert not bad, bad


@pytest.mark.parametrize("lang", LANGS)
def test_no_empty_strings(lang):
    for key, value in STRINGS[lang].items():
        assert value != "", key
        if key != "num.sep":  # the thousands separator is a (non-breaking) space by design
            assert value.strip(), key


def test_uzbek_uses_ascii_apostrophe():
    bad = [k for k, v in STRINGS["uz"].items() if any(c in v for c in "ʻʼ‘’`")]
    assert not bad, bad


@pytest.mark.parametrize("lang", LANGS)
def test_epilogues_length(lang):
    for e in D.ENDINGS:
        words = len(STRINGS[lang][f"end.{e}.text"].split())
        assert 55 <= words <= 125, (lang, e, words)  # 60-120 words, with a little slack for Uzbek agglutination


def test_engine_keys_exist():
    en = STRINGS["en"]
    for city in D.CITIES:
        for suffix in ("", ".in", ".to", ".from", ".desc"):
            assert f"city.{city}{suffix}" in en
    for good in D.GOODS:
        assert f"good.{good}" in en
    for e in D.ENDINGS:
        assert f"end.{e}.title" in en and f"end.{e}.text" in en
    for ev_id in EVENTS:
        assert f"ev.{ev_id}.title" in en and f"ev.{ev_id}.text" in en
    keys = set(en)
    for k in keys:
        if k.startswith("ev.") and ".r." in k:
            assert k.split(".")[1] in EVENTS, k
    for tip in set(TIP_BY_SCREEN.values()) | {"welcome", "desert", "mountain", "low_morale", "debt_paid"}:
        assert f"tip.{tip}" in en
    for city in D.CITIES:
        if city != D.HOME:
            assert f"tip.city.{city}" in en


def test_every_event_choice_and_outcome_has_text():
    """Outcomes are scanned from the event source; choices are enumerated from rich and poor states."""
    import inspect

    from karvon import engine as E
    from karvon.engine.rng import Rng

    for ev_id, ev in EVENTS.items():
        for outcome in re.findall(r'return "([a-z_]+)", ', inspect.getsource(type(ev))):
            assert f"ev.{ev_id}.r.{outcome}" in STRINGS["en"], (ev_id, outcome)
        for rich in (True, False):
            g = E.new_game(1, "hard", "x")
            if rich:
                g.money, g.provisions, g.guards, g.rep = 900, 100, 4, 60
                g.cargo = {"furs": 3, "cotton": 3}
            else:
                g.money, g.provisions, g.guards, g.rep = 0, 0, 0, 5
            params = ev.setup(g, {"danger": 2, "terrain": "mountain", "city": "buk"}, Rng(g))
            for choice in ev.choices(g, params):
                assert f"ev.{ev_id}.c.{choice}" in STRINGS["en"], (ev_id, choice)


def test_number_and_plural_formatting():
    assert fmt_num("en", 12345) == "12,345"
    assert fmt_num("ru", 12345) == "12 345"
    assert fmt_num("uz", -1200) == "−1 200"
    assert fmt_days("ru", 1) == "1 день" and fmt_days("ru", 3) == "3 дня" and fmt_days("ru", 11) == "11 дней"
    assert fmt_days("en", 1) == "1 day" and fmt_days("en", 2) == "2 days"
    assert fmt_days("uz", 5) == "5 kun"


def test_param_localisation():
    assert t("uz", "note.arrived", city="buk") == "🏁 Buxoroga yetib keldingiz."
    assert "Bukhara" in t("en", "note.arrived", city="buk")
    assert "шёлк" in t("ru", "ok.bought", good="silk", n=5, money=100)
    assert t("en", "missing.key") == "missing.key"
    assert t("en", "ok.bought") == STRINGS["en"]["ok.bought"]  # missing params never crash
