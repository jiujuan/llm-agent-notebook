"""工具定义与执行上下文。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Literal
import asyncio

from .types import ToolResult


ToolUpdateCallback = Callable[[ToolResult], Awaitable[None]]
ToolExecutor = Callable[["ToolExecutionContext", dict[str, Any]], Awaitable[ToolResult]]


@dataclass(slots=True)
class ToolExecutionContext:
    """传入工具的受控运行信息。"""

    tool_call_id: str
    signal: asyncio.Event
    on_update: ToolUpdateCallback

    def raise_if_cancelled(self) -> None:
        if self.signal.is_set():
            raise asyncio.CancelledError("agent run was aborted")


@dataclass(slots=True)
class AgentTool:
    """模型可调用的工具。

    parameters 使用简化 JSON Schema。mini 版只校验 required 字段，重点展示边界，
    生产代码应使用完整 JSON Schema 验证器。
    """

    name: str
    description: str
    parameters: dict[str, Any]
    execute: ToolExecutor
    label: str | None = None
    execution_mode: Literal["parallel", "sequential"] | None = None

    def validate(self, arguments: dict[str, Any]) -> None:
        required = self.parameters.get("required", [])
        missing = [name for name in required if name not in arguments]
        if missing:
            raise ValueError(f"missing required argument(s): {', '.join(missing)}")

