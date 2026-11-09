"""Every screen renders in all languages: no exceptions, no unfilled placeholders, balanced HTML,
text <= 4096 chars and callback_data <= 64 bytes."""
from __future__ import annotations

import re

import pytest

from karvon import engine as E
from karvon.bot.keyboards import build
from karvon.bot.render import SCREENS, render
from karvon.bot.session import Session
from karvon.engine import data as D
from karvon.engine.events import EVENTS
from karvon.engine.rng import Rng
from karvon.i18n import LANGS

PLACEHOLDER = re.compile(r"\{[a-z_0-9]+\}")
TAG = re.compile(r"<(/?)([a-z]+)[^>]*>")


def check_html(text: str) -> None:
    stack: list[str] = []
    for closing, name in TAG.findall(text):
        assert name in ("b", "i", "code", "pre", "u", "s"), f"unexpected tag <{name}>"
        if closing:
            assert stack and stack[-1] == name, f"unbalanced </{name}> in: {text[:200]}"
            stack.pop()
        else:
            stack.append(name)
    assert not stack, f"unclosed tags {stack}"


def check(sess: Session, lang: str, ctx: dict | None = None) -> str:
    text, rows = render(sess, lang, ctx or {})
    assert text and len(text) <= 4096
    assert not PLACEHOLDER.search(text), PLACEHOLDER.search(text).group(0) + " in " + text[:300]
    check_html(text)
    markup = build(rows, sess.bump())
    if markup is not None:
        for row in markup.inline_keyboard:
            assert 1 <= len(row) <= 3
            for button in row:
                assert button.text.strip()
                assert not PLACEHOLDER.search(button.text), button.text
                assert len(button.callback_data.encode("utf-8")) <= 64
    return text


def new_session(seed: int = 3) -> Session:
    s = Session()
    s.game = E.new_game(seed, "hard", "Tester")
    s.lang_chosen = True
    return s


@pytest.mark.parametrize("lang", LANGS)
def test_menus_render(lang):
    s = Session()
    for screen in ("lang", "menu", "diff", "help", "top"):
        s.go(screen)
        check(s, lang)
    s.go("top")
    rows = [
        {"name": "<b>Hacker</b> & co", "ending": e, "score": 1234 * i, "day": 50 + i, "difficulty": "hard"}
        for i, e in enumerate(D.ENDINGS, 1)
    ]
    text = check(s, lang, {"top": rows})
    assert "&lt;b&gt;Hacker" in text


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("city", D.CITIES)
def test_city_screens_render(lang, city):
    s = new_session()
    g = s.game
    g.city = city
    g.money = 5000
    g.cargo = {"silk": 5, "paper": 12}
    g.cargo_cost = {"silk": 300, "paper": 130}
    g.flags.update(letter=True, token=True, nilufar_ally=True, hostile=True)
    g.contract = {"good": "paper", "qty": 10, "city": city, "until": 40, "reward": 400}
    g.camel_deal = {"city": city, "until": g.day, "price": 80}
    E.rumor(g)
    for screen in ("hub", "market", "stable", "guards", "prov", "inn", "tea", "lender", "council", "travel",
                   "status", "ledger", "restart"):
        s.go(screen)
        check(s, lang)
    for good in D.GOOD_ORDER:
        s.go("good", good)
        check(s, lang)
    for dest, *_ in D.neighbours(city):
        s.go("confirm", dest)
        check(s, lang)
    for c in D.CITIES:
        s.go("ledger", c)
        check(s, lang)


@pytest.mark.parametrize("lang", LANGS)
def test_lender_states_render(lang):
    s = new_session()
    g = s.game
    s.go("lender")
    check(s, lang)
    E.borrow(g)
    check(s, lang)
    g.money = 100000
    E.pay_debt(g, "all")
    check(s, lang)
    s.go("hub")
    assert "rt" in str(render(s, lang)[1])


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("dest", ["buk", "tas"])
def test_road_screens_render(lang, dest):
    s = new_session()
    g = s.game
    if dest == "tas":
        g.city = "tas"
        dest = "kas"
    E.travel_start(g, dest)
    s.go("road")
    check(s, lang)
    g.city, g.travel = "buk", None
    g.phase = "city"
    E.travel_start(g, "khi")
    check(s, lang)


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("ev_id", sorted(EVENTS))
def test_event_and_result_screens_render(lang, ev_id):
    s = new_session()
    g = s.game
    g.money, g.provisions, g.guards, g.rep = 600, 100, 3, 10
    g.cargo = {"furs": 3, "cotton": 4, "silk": 2}
    g.flags["nilufar_ally"] = True
    ctx = {"danger": 2, "terrain": "desert", "city": "sam"}
    g.pending = {"id": ev_id, "params": EVENTS[ev_id].setup(g, ctx, Rng(g)), "src": "road"}
    s.go("event")
    check(s, lang)
    for choice in E.pending_choices(g):
        s2 = Session(s.to_dict())
        res = E.resolve_event_choice(s2.game, choice)
        assert res.ok
        s2.result = res.to_dict()
        s2.go("result")
        check(s2, lang)


@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("ending", D.ENDINGS)
def test_ending_screens_render(lang, ending):
    s = new_session()
    E.finish(s.game, ending)
    s.go("ending")
    text = check(s, lang)
    assert D.ENDING_EMOJI[ending] in text


@pytest.mark.parametrize("lang", LANGS)
def test_flash_messages_render(lang):
    s = new_session()
    g = s.game
    results = [
        E.buy(g, "paper", 5),
        E.sell(g, "paper", 2),
        E.buy(g, "silk", 999),
        E.hire_guards(g, 1),
        E.buy_provisions(g, 10),
        E.rest(g),
        E.rumor(g),
        E.borrow(g),
        E.pay_debt(g, 100),
        E.sell_camels(g, 1),
        E.travel_start(g, "nowhere"),
    ]
    g.pending = None
    for res in results:
        s.set_flash(res)
        s.go("hub")
        check(s, lang)
    E.travel_start(g, "buk")
    s.set_flash(E.ride_on(g))
    s.game_home()
    check(s, lang)


def test_all_screens_registered():
    assert {"hub", "market", "good", "road", "event", "result", "ending", "status", "ledger"} <= set(SCREENS)


def test_stale_screen_is_normalised():
    s = new_session()
    s.go("road")  # not on the road: must fall back to the hub
    render(s, "en")
    assert s.screen == "hub"
    s.go("event")
    render(s, "en")
    assert s.screen == "hub"
    s.game = None
    s.go("market")
    render(s, "en")
    assert s.screen == "menu"
