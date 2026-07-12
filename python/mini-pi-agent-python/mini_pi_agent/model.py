"""模型端口以及一个最小 OpenAI-compatible 适配器。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncIterator, Protocol
import asyncio
import json
import urllib.request
import uuid

from .types import AssistantMessage, LLMMessage, TextBlock, ToolCall


@dataclass(slots=True)
class ModelRequest:
    system_prompt: str
    messages: list[LLMMessage]
    tools: list[dict[str, Any]]


@dataclass(slots=True)
class ModelEvent:
    """模型流事件。

    为保持实现小而清晰，只保留文本增量和最终消息两种事件。
    """

    type: str
    delta: str | None = None
    message: AssistantMessage | None = None


class Model(Protocol):
    async def stream(self, request: ModelRequest, signal: asyncio.Event) -> AsyncIterator[ModelEvent]: ...


@dataclass(slots=True)
class OpenAICompatibleModel:
    """无第三方依赖的 OpenAI Chat Completions 适配器。

    它采用非流式 HTTP 请求，但转换为统一 ModelEvent，证明 Agent Loop 不依赖特定 SDK。
    base_url 可指向 OpenAI、OpenRouter、vLLM 或兼容服务。
    """

    model: str
    api_key: str
    base_url: str = "https://api.openai.com/v1"
    timeout_seconds: float = 60.0

    async def stream(self, request: ModelRequest, signal: asyncio.Event) -> AsyncIterator[ModelEvent]:
        if signal.is_set():
            raise asyncio.CancelledError()

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": ([{"role": "system", "content": request.system_prompt}] if request.system_prompt else [])
            + request.messages,
        }
        if request.tools:
            payload["tools"] = request.tools

        response = await asyncio.to_thread(self._post, payload)
        choice = response["choices"][0]
        raw_message = choice["message"]
        blocks: list[TextBlock | ToolCall] = []

        if raw_message.get("content"):
            blocks.append(TextBlock(raw_message["content"]))

        for raw_call in raw_message.get("tool_calls") or []:
            fn = raw_call["function"]
            try:
                arguments = json.loads(fn.get("arguments") or "{}")
            except json.JSONDecodeError as error:
                raise ValueError(f"model returned invalid tool JSON: {error}") from error
            blocks.append(ToolCall(raw_call.get("id") or str(uuid.uuid4()), fn["name"], arguments))

        message = AssistantMessage(
            content=blocks,
            stop_reason="tool_use" if any(isinstance(block, ToolCall) for block in blocks) else "stop",
        )
        if message.text:
            yield ModelEvent(type="text_delta", delta=message.text)
        yield ModelEvent(type="message_end", message=message)

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            return json.loads(response.read().decode("utf-8"))


def tool_to_openai_schema(tool: Any) -> dict[str, Any]:
    """把内部 AgentTool 映射为 OpenAI-compatible tool schema。"""

    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        },
    }

