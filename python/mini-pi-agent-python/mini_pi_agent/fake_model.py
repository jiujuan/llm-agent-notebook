"""确定性的脚本模型，用于示例与测试。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import AsyncIterator
import asyncio

from .model import ModelEvent, ModelRequest
from .types import AssistantMessage


@dataclass(slots=True)
class ScriptedModel:
    """每次模型调用取出一个预先写好的 AssistantMessage。"""

    responses: list[AssistantMessage]
    requests: list[ModelRequest] = field(default_factory=list)

    async def stream(self, request: ModelRequest, signal: asyncio.Event) -> AsyncIterator[ModelEvent]:
        if signal.is_set():
            raise asyncio.CancelledError()
        self.requests.append(request)
        if not self.responses:
            raise RuntimeError("ScriptedModel has no response left")

        message = self.responses.pop(0)
        # 按字符输出增量，使测试能够验证 streaming_message 与 message_update。
        for char in message.text:
            if signal.is_set():
                raise asyncio.CancelledError()
            await asyncio.sleep(0)
            yield ModelEvent(type="text_delta", delta=char)
        yield ModelEvent(type="message_end", message=message)

