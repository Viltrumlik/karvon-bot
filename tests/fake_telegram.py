"""A small in-process fake of the Telegram Bot API (aiohttp).

It implements just enough for an aiogram bot doing long polling:
getMe, deleteWebhook, getUpdates (long-poll + offset), sendMessage, editMessageText,
answerCallbackQuery, setMyCommands, getMyCommands, deleteMessage, close, logOut.

Tests (and ``scripts/console_play.py``) act as the *user*: they enqueue updates with
``send_text`` / ``press`` and inspect what the bot sent via ``messages`` / ``calls``.
"""
from __future__ import annotations

import asyncio
import itertools
import json
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from aiohttp import web

BOT_USER = {"id": 123456, "is_bot": True, "first_name": "Karvonboshi", "username": "karvon_test_bot"}
NOT_MODIFIED = (
    "Bad Request: message is not modified: specified new message content and reply markup are exactly "
    "the same as a current content and reply markup of the message"
)


class ApiError(Exception):
    def __init__(self, code: int, description: str) -> None:
        super().__init__(description)
        self.code = code
        self.description = description


@dataclass
class BotMessage:
    chat_id: int
    message_id: int
    text: str
    reply_markup: dict | None = None
    deleted: bool = False
    edits: int = 0
    touched: int = 0  # global counter of the last send/edit, to find the "current" message

    def buttons(self) -> list[tuple[str, str]]:
        out = []
        for row in (self.reply_markup or {}).get("inline_keyboard", []):
            for b in row:
                out.append((b.get("text", ""), b.get("callback_data", "")))
        return out

    def as_api(self) -> dict:
        msg = {
            "message_id": self.message_id,
            "date": int(time.time()),
            "chat": {"id": self.chat_id, "type": "private", "first_name": "Player"},
            "from": BOT_USER,
            "text": self.text,
        }
        if self.reply_markup:
            msg["reply_markup"] = self.reply_markup
        return msg


@dataclass
class FakeTelegram:
    token: str = "123456:TEST"
    updates: list[dict] = field(default_factory=list)
    messages: dict[tuple[int, int], BotMessage] = field(default_factory=dict)
    calls: list[tuple[str, dict]] = field(default_factory=list)
    callback_answers: dict[str, dict] = field(default_factory=dict)
    sent_callbacks: list[str] = field(default_factory=list)
    commands: dict[str, list] = field(default_factory=dict)
    unknown_methods: list[str] = field(default_factory=list)
    api_errors: list[tuple[str, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._update_ids = itertools.count(1)
        self._msg_ids = itertools.count(1000)
        self._user_msg_ids = itertools.count(1)
        self._cb_ids = itertools.count(1)
        self._touch = itertools.count(1)
        self._changed = asyncio.Event()
        self._new_updates = asyncio.Event()
        self._runner: web.AppRunner | None = None
        self.port = 0
        self.app = web.Application()
        self.app.router.add_route("*", "/bot{token}/{method}", self._handle)

    # ------------------------------------------------------------------ lifecycle
    async def start(self, host: str = "127.0.0.1", port: int = 0) -> str:
        self._runner = web.AppRunner(self.app, shutdown_timeout=0.5)
        await self._runner.setup()
        site = web.TCPSite(self._runner, host, port)
        await site.start()
        sockets = site._server.sockets  # type: ignore[union-attr]
        self.port = sockets[0].getsockname()[1]
        return self.base_url

    async def stop(self) -> None:
        self._new_updates.set()
        if self._runner is not None:
            await self._runner.cleanup()
            self._runner = None

    @property
    def base_url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    # ------------------------------------------------------------------ user side
    @staticmethod
    def user(user_id: int, lang: str = "en", first_name: str = "Tester") -> dict:
        return {"id": user_id, "is_bot": False, "first_name": first_name, "language_code": lang}

    def _push(self, update: dict) -> int:
        update_id = next(self._update_ids)
        update["update_id"] = update_id
        self.updates.append(update)
        self._new_updates.set()
        return update_id

    def send_text(self, user_id: int, text: str, lang: str = "en", first_name: str = "Tester") -> int:
        msg: dict[str, Any] = {
            "message_id": next(self._user_msg_ids),
            "date": int(time.time()),
            "chat": {"id": user_id, "type": "private", "first_name": first_name},
            "from": self.user(user_id, lang, first_name),
            "text": text,
        }
        if text.startswith("/"):
            msg["entities"] = [{"type": "bot_command", "offset": 0, "length": len(text.split()[0])}]
        return self._push({"message": msg})

    def press(self, user_id: int, message_id: int, data: str, lang: str = "en", first_name: str = "Tester") -> str:
        msg = self.messages.get((user_id, message_id))
        if msg is None:
            raise KeyError(f"no bot message {message_id} in chat {user_id}")
        cb_id = str(next(self._cb_ids))
        self.sent_callbacks.append(cb_id)
        self._push(
            {
                "callback_query": {
                    "id": cb_id,
                    "from": self.user(user_id, lang, first_name),
                    "chat_instance": f"ci{user_id}",
                    "data": data,
                    "message": msg.as_api(),
                }
            }
        )
        return cb_id

    def press_label(self, user_id: int, label_part: str, lang: str = "en") -> str:
        msg = self.current(user_id)
        assert msg is not None, "no current message"
        for text, data in msg.buttons():
            if label_part in text:
                return self.press(user_id, msg.message_id, data, lang)
        raise KeyError(f"button containing {label_part!r} not found in {[b[0] for b in msg.buttons()]}")

    def current(self, chat_id: int) -> BotMessage | None:
        """The most recently sent or edited, not deleted, bot message in the chat."""
        best = None
        for (cid, _), m in self.messages.items():
            if cid == chat_id and not m.deleted and (best is None or m.touched > best.touched):
                best = m
        return best

    def unanswered_callbacks(self) -> list[str]:
        return [c for c in self.sent_callbacks if c not in self.callback_answers]

    async def wait_for(self, predicate: Callable[[], bool], timeout: float = 5.0) -> bool:
        deadline = asyncio.get_running_loop().time() + timeout
        while True:
            if predicate():
                return True
            remaining = deadline - asyncio.get_running_loop().time()
            if remaining <= 0:
                return False
            self._changed.clear()
            try:
                await asyncio.wait_for(self._changed.wait(), timeout=min(remaining, 0.2))
            except asyncio.TimeoutError:
                pass

    async def wait_callback_answered(self, cb_id: str, timeout: float = 5.0) -> bool:
        return await self.wait_for(lambda: cb_id in self.callback_answers, timeout)

    async def wait_idle(self, timeout: float = 5.0) -> bool:
        """Wait until every queued update was fetched and every callback answered."""
        return await self.wait_for(lambda: not self.updates and not self.unanswered_callbacks(), timeout)

    # ------------------------------------------------------------------ server side
    async def _params(self, request: web.Request) -> dict:
        params: dict[str, Any] = dict(request.query)
        if request.can_read_body:
            ctype = request.content_type
            if ctype == "application/json":
                params.update(await request.json())
            else:
                post = await request.post()
                for k, v in post.items():
                    params[k] = v if isinstance(v, str) else str(v)
        out: dict[str, Any] = {}
        for k, v in params.items():
            if isinstance(v, str):
                s = v.strip()
                if s[:1] in "[{":
                    try:
                        v = json.loads(s)
                    except ValueError:
                        pass
                elif s.lstrip("-").isdigit() and k not in ("text", "callback_data"):
                    v = int(s)
                elif s in ("true", "false"):
                    v = s == "true"
            out[k] = v
        return out

    async def _handle(self, request: web.Request) -> web.Response:
        method = request.match_info["method"]
        token = request.match_info["token"]
        if token != self.token:
            return web.json_response({"ok": False, "error_code": 401, "description": "Unauthorized"}, status=401)
        params = await self._params(request)
        self.calls.append((method, params))
        handler = getattr(self, f"api_{method}", None)
        if handler is None:
            self.unknown_methods.append(method)
            return web.json_response(
                {"ok": False, "error_code": 404, "description": "Not Found: method not found"}, status=404
            )
        try:
            result = await handler(params)
        except ApiError as exc:
            self.api_errors.append((method, exc.description))
            return web.json_response(
                {"ok": False, "error_code": exc.code, "description": exc.description}, status=exc.code
            )
        finally:
            self._changed.set()
        return web.json_response({"ok": True, "result": result})

    async def api_getMe(self, p: dict) -> dict:
        return dict(BOT_USER, can_join_groups=True, can_read_all_group_messages=False, supports_inline_queries=False)

    async def api_deleteWebhook(self, p: dict) -> bool:
        return True

    async def api_close(self, p: dict) -> bool:
        return True

    async def api_logOut(self, p: dict) -> bool:
        return True

    async def api_setMyCommands(self, p: dict) -> bool:
        self.commands[str(p.get("language_code") or "")] = p.get("commands") or []
        return True

    async def api_getMyCommands(self, p: dict) -> list:
        return self.commands.get(str(p.get("language_code") or ""), [])

    async def api_getUpdates(self, p: dict) -> list:
        offset = int(p.get("offset") or 0)
        timeout = min(float(p.get("timeout") or 0), 2.0)
        limit = int(p.get("limit") or 100)
        if offset:
            self.updates = [u for u in self.updates if u["update_id"] >= offset]
        if not self.updates and timeout > 0:
            self._new_updates.clear()
            try:
                await asyncio.wait_for(self._new_updates.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                pass
        return [u for u in self.updates if u["update_id"] >= offset][:limit]

    async def api_sendMessage(self, p: dict) -> dict:
        chat_id = int(p["chat_id"])
        text = str(p.get("text", ""))
        if not text:
            raise ApiError(400, "Bad Request: message text is empty")
        if len(text) > 4096 + 2000:  # entities are stripped by Telegram; be lenient but catch nonsense
            raise ApiError(400, "Bad Request: message is too long")
        msg = BotMessage(chat_id, next(self._msg_ids), text, p.get("reply_markup") or None)
        msg.touched = next(self._touch)
        self.messages[(chat_id, msg.message_id)] = msg
        return msg.as_api()

    async def api_editMessageText(self, p: dict) -> dict:
        chat_id = int(p.get("chat_id") or 0)
        message_id = int(p.get("message_id") or 0)
        msg = self.messages.get((chat_id, message_id))
        if msg is None or msg.deleted:
            raise ApiError(400, "Bad Request: message to edit not found")
        text = str(p.get("text", ""))
        markup = p.get("reply_markup") or None
        if text == msg.text and markup == msg.reply_markup:
            raise ApiError(400, NOT_MODIFIED)
        msg.text = text
        msg.reply_markup = markup
        msg.edits += 1
        msg.touched = next(self._touch)
        return msg.as_api()

    async def api_answerCallbackQuery(self, p: dict) -> bool:
        cb_id = str(p.get("callback_query_id"))
        self.callback_answers[cb_id] = p
        return True

    async def api_deleteMessage(self, p: dict) -> bool:
        msg = self.messages.get((int(p.get("chat_id") or 0), int(p.get("message_id") or 0)))
        if msg is None or msg.deleted:
            raise ApiError(400, "Bad Request: message to delete not found")
        msg.deleted = True
        return True
