"""Screen renderers: Session -> (HTML text, button rows).

Button rows are ``[[(label, action), ...], ...]``; ``keyboards.build`` turns them into an
inline keyboard with ``"<seq>|<action>"`` callback data.
"""
from __future__ import annotations

from html import escape
from typing import Any, Callable

from .. import engine as E
from ..engine import data as D
from ..engine import market as M
from ..engine.events import expected_strength
from ..i18n import LANGS, STRINGS, fmt_days, fmt_num, fmt_signed, good_title, t
from .session import Session

Row = list[tuple[str, str]]
MAX_TEXT = 4096

GAME_SCREENS = {
    "hub", "market", "good", "stable", "guards", "prov", "inn", "tea", "lender", "council",
    "travel", "confirm", "road", "event", "result", "status", "ledger", "ending", "restart",
}
CITY_SCREENS = {
    "hub", "market", "good", "stable", "guards", "prov", "inn", "tea", "lender", "council", "travel", "confirm",
}
LANG_LABELS = {"uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}
DIFF_EMOJI = {"normal": "🙂", "hard": "😐", "legendary": "💀"}
DELTA_ICONS = (
    ("money", "💰"),
    ("provisions", "🍞"),
    ("camels", "🐫"),
    ("guards", "🛡"),
    ("morale", "😊"),
    ("rep", "⭐"),
    ("debt", "💳"),
)
TIP_BY_SCREEN = {
    "market": "market",
    "travel": "travel",
    "road": "road",
    "event": "event",
    "lender": "lender",
    "guards": "guards",
    "stable": "stable",
    "ledger": "ledger",
    "tea": "teahouse",
}


# --------------------------------------------------------------------------- small helpers
def n(lang: str, value: int | float) -> str:
    return fmt_num(lang, value)


def gname(lang: str, good: str) -> str:
    return f"{D.GOOD_EMOJI[good]} {good_title(lang, good)}"


def age(lang: str, day_seen: int, today: int) -> str:
    d = max(0, today - day_seen)
    return t(lang, "age.today") if d == 0 else t(lang, "age.ago", days=d)


def deltas_line(lang: str, deltas: dict) -> str:
    items = [f"{icon} {fmt_signed(lang, deltas[k])}" for k, icon in DELTA_ICONS if deltas.get(k)]
    for good, d in (deltas.get("cargo") or {}).items():
        if d and good in D.GOODS:
            items.append(f"{D.GOOD_EMOJI[good]} {fmt_signed(lang, d)}")
    return " · ".join(items)


def notes_lines(lang: str, notes: list) -> list[str]:
    out = []
    for item in notes or []:
        try:
            key, params = item
        except (TypeError, ValueError):
            continue
        if key == "note.ending":
            continue
        out.append(t(lang, key, **(params or {})))
    return out


def clip(text: str) -> str:
    if len(text) <= MAX_TEXT:
        return text
    return text[: MAX_TEXT - 1] + "…"


def danger_marks(danger: int) -> str:
    return "⚔" * max(1, danger)


def effective_danger(g: E.GameState, danger: int) -> int:
    return max(1, danger - 1) if g.flags.get("exposed") else danger


# --------------------------------------------------------------------------- header / flash / tips
def header(g: E.GameState, lang: str) -> str:
    limit = D.FINAL_DAY if g.debt_paid else D.DEADLINE_DAY
    debt = "✅" if g.debt_paid else n(lang, g.total_debt)
    return (
        f"📅 {g.day}/{limit} · 💰 {n(lang, g.money)} · 📦 {g.cargo_units}/{g.capacity} · "
        f"🍞 {n(lang, g.provisions)} · 😊 {g.morale} · 💳 {debt}"
    )


def flash_text(sess: Session, lang: str) -> str:
    if not sess.flash:
        return ""
    res = E.Result.from_dict(sess.flash)
    if not res.ok:
        return "⚠️ " + t(lang, res.key, **res.params)
    lines = [t(lang, res.key, **res.params)]
    dl = deltas_line(lang, res.deltas)
    if dl:
        lines.append(dl)
    lines.extend(notes_lines(lang, res.notes))
    return "\n".join(lines)


def tip_candidates(sess: Session) -> list[str]:
    g = sess.game
    if g is None or g.ended:
        return []
    out: list[str] = []
    if g.morale < 30:
        out.append("low_morale")
    if g.debt_paid:
        out.append("debt_paid")
    s = sess.screen
    if s == "hub":
        out.append("welcome" if g.city == D.HOME else f"city.{g.city}")
    elif s == "confirm" and sess.arg:
        road = D.road_between(g.city, sess.arg)
        if road and road[2] in ("desert", "mountain"):
            out.append(road[2])
    elif s in TIP_BY_SCREEN:
        out.append(TIP_BY_SCREEN[s])
    return out


def tip_text(sess: Session, lang: str) -> str:
    if not sess.tips or sess.game is None:
        return ""
    for tip in tip_candidates(sess):
        if tip not in sess.seen:
            sess.seen.append(tip)
            body = t(lang, f"tip.{tip}", debt=sess.game.total_debt)
            return f"{t(lang, 'tip.prefix')} <i>{body}</i>"
    return ""


# --------------------------------------------------------------------------- screens: menus
def scr_lang(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    pre = sess.arg if sess.arg in LANGS else lang
    order = [pre] + [x for x in LANGS if x != pre]
    prompt = "\n".join(STRINGS[x]["lang.prompt"] for x in order)
    rows = [[(("✅ " if x == pre else "") + LANG_LABELS[x], f"L:{x}")] for x in order]
    return prompt, rows


def scr_menu(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    text = t(lang, "menu.text")
    rows: list[Row] = []
    if sess.active:
        text += "\n\n" + t(lang, "menu.active", day=sess.game.day)  # type: ignore[union-attr]
        rows.append([(t(lang, "btn.continue"), "cont")])
    rows.append([(t(lang, "btn.new_game"), "new")])
    rows.append([(t(lang, "btn.how_to"), "help"), (t(lang, "btn.top"), "top")])
    rows.append(
        [(t(lang, "btn.language"), "lang"), (t(lang, "btn.tips_on" if sess.tips else "btn.tips_off"), "tips")]
    )
    return text, rows


def scr_diff(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    text = t(lang, "diff.title") + "\n\n" + t(lang, "diff.text")
    rows = [[(f"{DIFF_EMOJI[d]} {t(lang, 'diff.' + d)}", f"df:{d}")] for d in D.DIFFICULTY_ORDER]
    rows.append([(t(lang, "btn.back"), "menu")])
    return text, rows


def scr_restart(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    return t(lang, "restart.text"), [[(t(lang, "btn.restart_yes"), "ry"), (t(lang, "btn.cancel"), "cont")]]


def scr_help(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    return t(lang, "help.text"), [[(t(lang, "btn.back"), "cont")]]


def scr_top(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    rows_data = ctx.get("top") or []
    lines = [t(lang, "top.title"), ""]
    if not rows_data:
        lines.append(t(lang, "top.empty"))
    for i, r in enumerate(rows_data, 1):
        ending = str(r.get("ending", "E5"))
        diff = str(r.get("difficulty", "hard"))
        lines.append(
            t(
                lang,
                "top.row",
                rank=i,
                emoji=D.ENDING_EMOJI.get(ending, "🏁"),
                name=escape(str(r.get("name") or "?"))[:40],
                score=int(r.get("score") or 0),
                ending=t(lang, f"end.{ending}.title"),
                diff=t(lang, f"diff.{diff}"),
                day=int(r.get("day") or 0),
            )
        )
    return "\n".join(lines), [[(t(lang, "btn.back"), "cont")]]


# --------------------------------------------------------------------------- screens: city
def scr_hub(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    city = g.city
    lines = [t(lang, "hub.title", city=city), f"<i>{t(lang, f'city.{city}.desc')}</i>"]
    if g.contract and g.contract["city"] == city:
        lines.append(t(lang, "note.contract_here", good=g.contract["good"], n=g.contract["qty"]))
    if g.camel_deal and g.camel_deal["city"] == city and g.camel_deal["until"] >= g.day:
        lines.append(t(lang, "st.deal"))
    rows: list[Row] = [
        [(t(lang, "btn.market"), "mk"), (t(lang, "btn.stable"), "st")],
        [(t(lang, "btn.guards"), "gu"), (t(lang, "btn.provisions"), "pr")],
        [(t(lang, "btn.inn"), "inn"), (t(lang, "btn.teahouse"), "tea")],
    ]
    special: Row = []
    if city == D.HOME:
        special.append((t(lang, "btn.lender"), "ln"))
    if E.can_council(g):
        special.append((t(lang, "btn.council"), "co"))
    if special:
        rows.append(special)
    if E.can_deliver(g) and g.contract:
        rows.append([(t(lang, "btn.deliver", good=g.contract["good"], n=g.contract["qty"]), "dl")])
    rows.append([(t(lang, "btn.travel"), "tr"), (t(lang, "btn.status"), "stt")])
    last: Row = [(t(lang, "btn.ledger"), "lg")]
    if g.debt_paid:
        last.append((t(lang, "btn.retire"), "rt"))
    last.append((t(lang, "btn.menu"), "menu"))
    rows.append(last)
    return "\n".join(lines), rows


def scr_market(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    city = g.city
    lines = [t(lang, "mk.title", city=city), t(lang, "mk.cols")]
    buttons: list[tuple[str, str]] = []
    for good in D.GOOD_ORDER:
        have = g.cargo.get(good, 0)
        line = f"{gname(lang, good)}: <b>{n(lang, M.buy_price(g, city, good))}</b> / {n(lang, M.sell_price(g, city, good))}"
        if have:
            line += f" · 🎒{have}"
        lines.append(line)
        buttons.append((gname(lang, good) + (f" ·{have}" if have else ""), f"g:{good}"))
    lines.append("")
    lines.append(t(lang, "mk.hint"))
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    rows.append([(t(lang, "btn.back"), "h")])
    return "\n".join(lines), rows


def scr_good(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    good = sess.arg if sess.arg in D.GOODS else D.GOOD_ORDER[0]
    city = g.city
    have = g.cargo.get(good, 0)
    lines = [
        f"<b>{gname(lang, good)}</b>",
        t(lang, "gd.prices", buy=M.buy_price(g, city, good), sell=M.sell_price(g, city, good)),
    ]
    if have:
        avg = g.cargo_cost.get(good, 0) / have
        lines.append(t(lang, "gd.have", n=have, avg=int(round(avg))))
    else:
        lines.append(t(lang, "gd.none"))
    lines.append(t(lang, "gd.space", space=g.free_space, money=g.money))
    known = []
    for c in D.CITIES:
        if c == city:
            continue
        entry = g.known.get(c, {}).get(good)
        if entry:
            known.append((entry[1], c, entry[2]))
    lines.append("")
    if known:
        lines.append(t(lang, "gd.elsewhere"))
        for price, c, day in sorted(known, reverse=True):
            lines.append(t(lang, "gd.elsewhere_row", city=c, price=price, age=age(lang, day, g.day)))
    else:
        lines.append(t(lang, "gd.unknown"))
    max_buy = M.max_affordable(g, city, good)
    buy_row: Row = []
    if max_buy >= 1:
        buy_row.append((t(lang, "btn.buy", n=1), f"b:{good}:1"))
    if max_buy >= 5:
        buy_row.append((t(lang, "btn.buy", n=5), f"b:{good}:5"))
    if max_buy >= 2:
        buy_row.append((t(lang, "btn.buy_max", n=max_buy), f"bm:{good}"))
    sell_row: Row = []
    if have >= 1:
        sell_row.append((t(lang, "btn.sell", n=1), f"s:{good}:1"))
    if have >= 5:
        sell_row.append((t(lang, "btn.sell", n=5), f"s:{good}:5"))
    if have >= 2:
        sell_row.append((t(lang, "btn.sell_all", n=have), f"sa:{good}"))
    rows = [r for r in (buy_row, sell_row) if r]
    rows.append([(t(lang, "btn.back"), "mk")])
    return "\n".join(lines), rows


def scr_stable(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    price = E.camel_price(g)
    lines = [
        t(lang, "st.title"),
        t(
            lang,
            "st.text",
            camels=g.camels,
            max=D.MAX_CAMELS,
            slots=D.SLOTS_PER_CAMEL,
            prov=D.PROV_PER_CAMEL,
            price=price,
            sell=D.CAMEL_SELL_PRICE,
        ),
    ]
    if g.camel_deal and g.camel_deal["city"] == g.city and g.camel_deal["until"] >= g.day:
        lines.append(t(lang, "st.deal"))
    row: Row = []
    if g.camels < D.MAX_CAMELS:
        row.append((t(lang, "btn.camel_buy", price=price), "cb"))
    if g.camels > 1:
        row.append((t(lang, "btn.camel_sell", price=D.CAMEL_SELL_PRICE), "cs"))
    rows = [row] if row else []
    rows.append([(t(lang, "btn.back"), "h")])
    return "\n".join(lines), rows


def scr_guards(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    text = t(lang, "gu.title") + "\n" + t(
        lang,
        "gu.text",
        n=g.guards,
        max=D.MAX_GUARDS,
        signup=D.GUARD_SIGNUP,
        wage=D.GUARD_WAGE,
        strength=expected_strength(g),
    )
    row: Row = []
    if g.guards < D.MAX_GUARDS:
        row.append((t(lang, "btn.hire", n=1, money=D.GUARD_SIGNUP), "gh:1"))
    if g.guards <= D.MAX_GUARDS - 2:
        row.append((t(lang, "btn.hire", n=2, money=2 * D.GUARD_SIGNUP), "gh:2"))
    rows = [row] if row else []
    if g.guards:
        rows.append([(t(lang, "btn.dismiss"), "gd")])
    rows.append([(t(lang, "btn.back"), "h")])
    return text, rows


def scr_prov(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    price = E.provision_price(g)
    text = t(lang, "pr.title") + "\n" + t(
        lang, "pr.text", prov=g.provisions, cap=g.prov_cap, price=price, eat=g.crew + g.camels
    )
    room = max(0, g.prov_cap - g.provisions)
    row: Row = []
    for amount in (10, 25):
        if room >= amount:
            row.append((t(lang, "btn.prov", n=amount, money=amount * price), f"pb:{amount}"))
    fill = min(room, g.money // price) if price else room
    rows = [row] if row else []
    if fill >= 1:
        rows.append([(t(lang, "btn.prov_max", n=fill), "pm")])
    rows.append([(t(lang, "btn.back"), "h")])
    return text, rows


def scr_inn(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    cost = E.rest_cost(g)
    lines = [t(lang, "inn.title"), t(lang, "inn.text", morale=D.REST_MORALE, cost=cost, cur=g.morale)]
    if g.city == "khi" and g.flags.get("nilufar_ally"):
        lines.append(f"<i>{t(lang, 'inn.nilufar')}</i>")
    rows = [
        [(t(lang, "btn.rest", cost=cost), "rs"), (t(lang, "btn.wait"), "wt")],
        [(t(lang, "btn.back"), "h")],
    ]
    return "\n".join(lines), rows


def scr_tea(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    cost = E.rumor_cost(g)
    lines = [t(lang, "tea.title"), t(lang, "tea.text", cost=D.RUMOR_COST)]
    if g.city == "khi" and g.flags.get("nilufar_ally"):
        lines.append(f"<i>{t(lang, 'tea.nilufar')}</i>")
    rows = [[(t(lang, "btn.rumor", cost=cost), "ru")], [(t(lang, "btn.back"), "h")]]
    return "\n".join(lines), rows


def next_interest_day(g: E.GameState) -> int:
    nxt = (g.day // D.INTEREST_EVERY + 1) * D.INTEREST_EVERY
    return min(nxt, D.INTEREST_LAST_DAY) if g.day < D.INTEREST_LAST_DAY else D.INTEREST_LAST_DAY


def scr_lender(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    lines = [t(lang, "ln.title")]
    rows: list[Row] = []
    if g.total_debt <= 0:
        lines.append(t(lang, "ln.paid"))
    else:
        loan = t(lang, "ln.loan", loan=g.loan) if g.loan else ""
        lines.append(
            t(
                lang,
                "ln.text",
                debt=g.total_debt,
                loan=loan,
                next=next_interest_day(g),
                deadline=D.DEADLINE_DAY,
                money=g.money,
            )
        )
        if E.can_borrow(g):
            lines.append(t(lang, "ln.offer", amount=D.LOAN_AMOUNT))
        pay_row: Row = []
        for amount in (100, 500):
            if g.money >= amount and g.total_debt > amount:
                pay_row.append((t(lang, "btn.pay", n=amount), f"lp:{amount}"))
        if pay_row:
            rows.append(pay_row)
        all_n = min(g.money, g.total_debt)
        if all_n > 0:
            rows.append([(t(lang, "btn.pay_all", n=all_n), "la")])
        if E.can_borrow(g):
            rows.append([(t(lang, "btn.borrow", n=D.LOAN_AMOUNT), "lb")])
    rows.append([(t(lang, "btn.back"), "h")])
    return "\n".join(lines), rows


def scr_council(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    rows: list[Row] = []
    if sess.game is not None and E.can_council(sess.game):
        rows.append([(t(lang, "btn.expose"), "cx")])
    rows.append([(t(lang, "btn.back"), "h")])
    return t(lang, "co.title") + "\n" + t(lang, "co.text"), rows


def scr_travel(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    text = t(lang, "tr.title", city=g.city) + "\n" + t(lang, "tr.hint")
    rows: list[Row] = []
    for dest, days, danger, terrain in D.neighbours(g.city):
        label = t(
            lang,
            "tr.btn",
            city=dest,
            n=days,
            terrain=D.TERRAIN_EMOJI[terrain],
            danger=danger_marks(effective_danger(g, danger)),
        )
        rows.append([(label, f"tc:{dest}")])
    rows.append([(t(lang, "btn.back"), "h")])
    return text, rows


def scr_confirm(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    dest = sess.arg or ""
    road = D.road_between(g.city, dest)
    if road is None:
        sess.go("travel")
        return scr_travel(sess, lang, ctx)
    days, danger, terrain = road
    danger = effective_danger(g, danger)
    need = E.trip_need(g, dest)
    wages = g.guards * D.GUARD_WAGE * days
    lines = [
        t(lang, "tc.title", src=t(lang, f"city.{g.city}"), dst=t(lang, f"city.{dest}")),
        t(
            lang,
            "tc.text",
            days=days,
            terrain=f"{D.TERRAIN_EMOJI[terrain]} {t(lang, 'terrain.' + terrain)}",
            danger=danger_marks(danger),
            need=need,
            prov=g.provisions,
            wages=wages,
            arrive=g.day + days,
        ),
    ]
    warns = []
    if need > g.prov_cap:
        warns.append(t(lang, "tc.warn_cap"))
    elif need > g.provisions:
        warns.append(t(lang, "tc.warn_food"))
    if wages > g.money:
        warns.append(t(lang, "tc.warn_wages"))
    if not g.debt_paid and g.day + days + D.DIST[dest][D.HOME] > D.DEADLINE_DAY:
        warns.append(t(lang, "tc.warn_deadline", deadline=D.DEADLINE_DAY))
    if warns:
        lines.append("")
        lines.extend(warns)
    rows = [[(t(lang, "btn.depart"), f"go:{dest}")], [(t(lang, "btn.provisions"), "pr"), (t(lang, "btn.back"), "tr")]]
    return "\n".join(lines), rows


# --------------------------------------------------------------------------- screens: road / events
def progress_bar(done: int, total: int, width: int = 10) -> str:
    total = max(1, total)
    filled = min(width, int(round(width * done / total)))
    return "▰" * filled + "▱" * (width - filled)


def scr_road(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None and g.travel is not None
    tr = g.travel
    per_day = (g.crew + g.camels) * (2 if tr["terrain"] == "desert" else 1)
    lines = [
        t(lang, "rd.title", src=t(lang, f"city.{tr['src']}"), dst=t(lang, f"city.{tr['dst']}")),
        f"<i>{t(lang, 'rd.flavor.' + tr['terrain'])}</i>",
        "",
        t(lang, "rd.progress", bar=progress_bar(tr["done"], tr["total"]), done=tr["done"], total=tr["total"]),
        f"{D.TERRAIN_EMOJI[tr['terrain']]} {danger_marks(int(tr['danger']))} · "
        + t(lang, "rd.food", days=g.provisions // max(1, per_day)),
    ]
    rows = [
        [(t(lang, "btn.next_day"), "nd"), (t(lang, "btn.ride_on"), "ro")],
        [(t(lang, "btn.status"), "stt"), (t(lang, "btn.menu"), "menu")],
    ]
    return "\n".join(lines), rows


def scr_event(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None and g.pending is not None
    ev_id = g.pending["id"]
    params = dict(g.pending.get("params") or {})
    lines = [f"⚡ <b>{t(lang, f'ev.{ev_id}.title', **params)}</b>", "", t(lang, f"ev.{ev_id}.text", **params)]
    if "ours" in params and "theirs" in params:
        lines.append("")
        lines.append(t(lang, "ev.strength", ours=params["ours"], theirs=params["theirs"]))
        if params.get("bonus"):
            lines.append(t(lang, "ev.warned", bonus=params["bonus"]))
    rows = [[(t(lang, f"ev.{ev_id}.c.{c}", **params), f"ev:{c}")] for c in E.pending_choices(g)]
    return "\n".join(lines), rows


def scr_result(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    res = E.Result.from_dict(sess.result or {})
    parts = res.key.split(".")
    ev_id = parts[1] if len(parts) >= 4 and parts[0] == "ev" else ""
    lines = []
    if ev_id:
        lines.append(f"⚡ <b>{t(lang, f'ev.{ev_id}.title', **res.params)}</b>")
        lines.append("")
    lines.append(t(lang, res.key, **res.params))
    dl = deltas_line(lang, res.deltas)
    extra = notes_lines(lang, res.notes)
    if dl or extra:
        lines.append("")
    if dl:
        lines.append(dl)
    lines.extend(extra)
    return "\n".join(lines), [[(t(lang, "btn.continue_ev"), "ok")]]


# --------------------------------------------------------------------------- screens: info
def scr_status(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    lines = [t(lang, "stt.title"), ""]
    if g.debt_paid:
        lines.append(t(lang, "stt.day_paid", day=g.day, final=D.FINAL_DAY))
    else:
        lines.append(t(lang, "stt.day", day=g.day, left=max(0, D.DEADLINE_DAY - g.day)))
    lines.append(t(lang, "stt.money", money=g.money))
    if g.debt_paid:
        lines.append(t(lang, "stt.debt_paid", day=g.paid_day))
    else:
        lines.append(t(lang, "stt.debt", debt=g.total_debt, next=next_interest_day(g)))
    lines.append(t(lang, "stt.camels", camels=g.camels, cargo=g.cargo_units, cap=g.capacity))
    lines.append(t(lang, "stt.prov", prov=g.provisions, cap=g.prov_cap, days=g.provisions // max(1, g.crew + g.camels)))
    lines.append(t(lang, "stt.guards", guards=g.guards, strength=expected_strength(g)))
    lines.append(t(lang, "stt.morale", morale=g.morale))
    lines.append(t(lang, "stt.rep", rep=g.rep))
    lines.append(t(lang, "stt.nw", nw=E.net_worth(g)))
    lines.append(t(lang, "stt.diff", diff=t(lang, f"diff.{g.difficulty}")))
    lines.append("")
    if g.cargo_units:
        lines.append(t(lang, "stt.cargo"))
        for good in D.GOOD_ORDER:
            q = g.cargo.get(good, 0)
            if q:
                lines.append(f"• {gname(lang, good)} ×{q}")
    else:
        lines.append(t(lang, "stt.cargo_empty"))
    if g.contract:
        c = g.contract
        lines.append(t(lang, "stt.contract", good=c["good"], n=c["qty"], city=c["city"], until=c["until"], reward=c["reward"]))
    flags = []
    for flag, key in (
        ("letter", "letter"),
        ("token", "token"),
        ("exposed", "exposed"),
        ("hostile", "hostile"),
        ("nilufar_ally", "nilufar"),
    ):
        if g.flags.get(flag) and not (flag == "hostile" and g.flags.get("exposed")):
            flags.append(t(lang, f"stt.flag.{key}"))
    if flags:
        lines.append("")
        lines.append(t(lang, "stt.clues"))
        lines.extend(flags)
    return "\n".join(lines), [[(t(lang, "btn.back"), "h")]]


def scr_ledger(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    city = sess.arg if sess.arg in D.CITIES else None
    if city is None:
        text = t(lang, "lg.title") + "\n" + t(lang, "lg.pick")
        buttons = []
        for c in D.CITIES:
            mark = " ✓" if g.known.get(c) else ""
            buttons.append((t(lang, f"city.{c}") + mark, f"lg:{c}"))
        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        rows.append([(t(lang, "btn.back"), "h")])
        return text, rows
    known = g.known.get(city) or {}
    if not known:
        text = t(lang, "lg.title") + "\n" + t(lang, "lg.none", city=city)
    else:
        latest = max(v[2] for v in known.values())
        lines = [t(lang, "lg.city", city=city, age=age(lang, latest, g.day))]
        for good in D.GOOD_ORDER:
            if good in known:
                b, s, day = known[good]
                line = f"{gname(lang, good)}: {n(lang, b)} / {n(lang, s)}"
                if day != latest:
                    line += f" ({age(lang, day, g.day)})"
                lines.append(line)
        text = "\n".join(lines)
    return text, [[(t(lang, "btn.back"), "lg")]]


def scr_ending(sess: Session, lang: str, ctx: dict) -> tuple[str, list[Row]]:
    g = sess.game
    assert g is not None
    ending = g.ending or "E5"
    lines = [
        t(lang, "end.head", title=f"{D.ENDING_EMOJI.get(ending, '')} {t(lang, f'end.{ending}.title')}"),
        "",
        t(lang, f"end.{ending}.text"),
        "",
        t(
            lang,
            "end.stats",
            score=g.score,
            day=g.day,
            diff=t(lang, f"diff.{g.difficulty}"),
            nw=int(g.stats.get("final_nw", E.net_worth(g))),
        ),
    ]
    rows = [[(t(lang, "btn.new_game"), "new"), (t(lang, "btn.top"), "top")], [(t(lang, "btn.menu"), "menu")]]
    return "\n".join(lines), rows


SCREENS: dict[str, Callable[[Session, str, dict], tuple[str, list[Row]]]] = {
    "lang": scr_lang,
    "menu": scr_menu,
    "diff": scr_diff,
    "restart": scr_restart,
    "help": scr_help,
    "top": scr_top,
    "hub": scr_hub,
    "market": scr_market,
    "good": scr_good,
    "stable": scr_stable,
    "guards": scr_guards,
    "prov": scr_prov,
    "inn": scr_inn,
    "tea": scr_tea,
    "lender": scr_lender,
    "council": scr_council,
    "travel": scr_travel,
    "confirm": scr_confirm,
    "road": scr_road,
    "event": scr_event,
    "result": scr_result,
    "status": scr_status,
    "ledger": scr_ledger,
    "ending": scr_ending,
}


# --------------------------------------------------------------------------- entry point
def normalize_screen(sess: Session) -> None:
    """Make sure the screen is valid for the current game state (stale sessions, old saves)."""
    g = sess.game
    s = sess.screen
    if s not in SCREENS:
        sess.game_home() if sess.game else sess.go("menu")
        s = sess.screen
    if s in GAME_SCREENS and g is None:
        sess.go("menu")
        return
    if g is None:
        return
    if s == "result" and not sess.result:
        sess.game_home()
        return
    if g.ended and s in GAME_SCREENS and s not in ("ending", "status", "result"):
        sess.go("ending")
        return
    if s == "ending" and not g.ended:
        sess.game_home()
        return
    if g.pending and s not in ("event", "status", "result") and s in GAME_SCREENS:
        sess.go("event")
        return
    if s == "event" and not g.pending:
        sess.game_home()
        return
    if s in CITY_SCREENS and g.phase != "city":
        sess.game_home()
        return
    if s == "road" and not g.on_road:
        sess.game_home()


def render(sess: Session, lang: str, ctx: dict[str, Any] | None = None) -> tuple[str, list[Row]]:
    ctx = ctx or {}
    normalize_screen(sess)
    body, rows = SCREENS[sess.screen](sess, lang, ctx)
    parts = []
    if sess.game is not None and sess.screen in GAME_SCREENS and sess.screen != "ending":
        parts.append(header(sess.game, lang))
    fl = flash_text(sess, lang)
    if fl:
        parts.append(fl)
    tip = tip_text(sess, lang) if sess.screen in GAME_SCREENS else ""
    if tip:
        parts.append(tip)
    parts.append(body)
    sess.flash = None
    return clip("\n\n".join(p for p in parts if p)), rows
