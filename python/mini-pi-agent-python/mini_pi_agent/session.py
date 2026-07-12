"""最小 Session 抽象。

pi Harness 使用树形、可分支的 session；mini 版先提供线性内存 Session，
展示“运行状态”和“跨次调用历史”应该分离。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class MemorySession:
    messages: list[Any] = field(default_factory=list)

    async def load(self) -> list[Any]:
        return list(self.messages)

    async def append(self, messages: list[Any]) -> None:
        self.messages.extend(messages)

    async def clear(self) -> None:
        self.messages.clear()

