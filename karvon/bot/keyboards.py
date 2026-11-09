"""Inline keyboard construction. Callback data format: ``"<seq>|<action>"`` (always < 64 bytes)."""
from __future__ import annotations

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

MAX_CALLBACK_BYTES = 64


def callback(seq: int, action: str) -> str:
    data = f"{seq}|{action}"
    if len(data.encode("utf-8")) > MAX_CALLBACK_BYTES:  # defensive: never send oversized data
        data = data.encode("utf-8")[:MAX_CALLBACK_BYTES].decode("utf-8", "ignore")
    return data


def parse(data: str | None) -> tuple[int | None, str]:
    if not data or "|" not in data:
        return None, data or ""
    seq, _, action = data.partition("|")
    try:
        return int(seq), action
    except ValueError:
        return None, action


def build(rows: list[list[tuple[str, str]]], seq: int) -> InlineKeyboardMarkup | None:
    keyboard = [
        [InlineKeyboardButton(text=label[:64], callback_data=callback(seq, action)) for label, action in row]
        for row in rows
        if row
    ]
    if not keyboard:
        return None
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
