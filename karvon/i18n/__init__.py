"""Translations and the ``t(lang, key, **params)`` helper.

Param conventions (applied automatically by ``t``):
* ``good``/``good2``  -> localized good name (lowercase, as used inside sentences)
* ``city``/``city2``  -> localized city name; ``city_in``/``city_to``/``city_from`` (and ``city2_*``)
  are filled with the grammatical forms ("in Bukhara", "Buxoroda", "в Бухаре" ...)
* ``days``            -> number + localized plural word ("3 days", "3 дня", "3 kun")
* ``profit``          -> signed number (+120 / −30)
* ``kind``+``city``+``good``+``price`` -> ``rumor`` sentence
* any other int       -> number with digit grouping
"""
from __future__ import annotations

import string
from typing import Any

from . import en, ru, uz

LANGS: tuple[str, ...] = ("uz", "ru", "en")
DEFAULT_LANG = "en"
STRINGS: dict[str, dict[str, str]] = {"uz": uz.STRINGS, "ru": ru.STRINGS, "en": en.STRINGS}

MINUS = "−"


def norm_lang(code: str | None) -> str:
    """Map a Telegram ``language_code`` to one of our languages (uz, ru, else en)."""
    if not code:
        return DEFAULT_LANG
    code = code.lower()
    if code.startswith("uz"):
        return "uz"
    if code.startswith("ru"):
        return "ru"
    return "en"


def raw(lang: str, key: str) -> str:
    table = STRINGS.get(lang) or STRINGS[DEFAULT_LANG]
    if key in table:
        return table[key]
    return STRINGS[DEFAULT_LANG].get(key, key)


def has(lang: str, key: str) -> bool:
    return key in (STRINGS.get(lang) or {})


def fmt_num(lang: str, n: int | float) -> str:
    n = int(round(n))
    sep = raw(lang, "num.sep")
    sign = MINUS if n < 0 else ""
    body = f"{abs(n):,}".replace(",", sep)
    return sign + body


def fmt_signed(lang: str, n: int | float) -> str:
    n = int(round(n))
    if n > 0:
        return "+" + fmt_num(lang, n)
    return fmt_num(lang, n)


def plural(lang: str, n: int, key: str) -> str:
    forms = raw(lang, key).split("|")
    n_abs = abs(int(n))
    if lang == "ru" and len(forms) >= 3:
        if n_abs % 10 == 1 and n_abs % 100 != 11:
            return forms[0]
        if 2 <= n_abs % 10 <= 4 and not 12 <= n_abs % 100 <= 14:
            return forms[1]
        return forms[2]
    if len(forms) >= 2:
        return forms[0] if n_abs == 1 else forms[1]
    return forms[0]


def fmt_days(lang: str, n: int) -> str:
    return f"{fmt_num(lang, n)} {plural(lang, n, 'unit.days')}"


def good_name(lang: str, good: str) -> str:
    return raw(lang, f"good.{good}")


def good_title(lang: str, good: str) -> str:
    name = good_name(lang, good)
    return name[:1].upper() + name[1:]


def city_name(lang: str, city: str) -> str:
    return raw(lang, f"city.{city}")


def localize(lang: str, params: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in params.items():
        if k in ("good", "good2") and isinstance(v, str):
            out[k] = good_name(lang, v)
        elif k in ("city", "city2") and isinstance(v, str) and has(DEFAULT_LANG, f"city.{v}"):
            out[k] = city_name(lang, v)
            for form in ("in", "to", "from"):
                out[f"{k}_{form}"] = raw(lang, f"city.{v}.{form}")
        elif k == "days" and isinstance(v, int):
            out[k] = fmt_days(lang, v)
        elif k == "profit" and isinstance(v, (int, float)):
            out[k] = fmt_signed(lang, v)
        elif isinstance(v, bool):
            out[k] = v
        elif isinstance(v, (int, float)):
            out[k] = fmt_num(lang, v)
        else:
            out[k] = v
    kind = params.get("kind")
    if kind in ("high", "low") and "city" in params and "good" in params and "rumor" not in params:
        sentence = t(lang, f"rumor.{kind}", city=params["city"], good=params["good"], price=params.get("price", 0))
        out["rumor"] = sentence[:1].upper() + sentence[1:]
    return out


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:  # never crash on a missing placeholder
        return "{" + key + "}"


def t(lang: str, key: str, **params: Any) -> str:
    template = raw(lang, key)
    if not params and "{" not in template:
        return template
    try:
        return string.Formatter().vformat(template, (), _SafeDict(localize(lang, params)))
    except (ValueError, IndexError, KeyError):
        return template


def placeholders(template: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(template) if name}


__all__ = [
    "LANGS",
    "DEFAULT_LANG",
    "STRINGS",
    "t",
    "raw",
    "norm_lang",
    "fmt_num",
    "fmt_signed",
    "fmt_days",
    "plural",
    "good_name",
    "good_title",
    "city_name",
    "localize",
    "placeholders",
]
