"""Agent Core 使用的领域类型。

pi-agent-core 的一个关键设计是区分：

1. AgentMessage：应用内部消息，可以扩展；
2. LLMMessage：真正发送给模型的标准消息；
3. AgentEvent：用于 UI、日志和状态同步的运行事件。

本教学版用 dataclass 表达这些协议，避免在循环里传递无约束字典。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, TypeAlias
import time


JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]


def now_ms() -> int:
    """统一生成毫秒时间戳，便于消息排序和测试替换。"""

    return int(time.time() * 1000)


@dataclass(slots=True)
class TextBlock:
    """Assistant 内容中的文本块。"""

    text: str
    type: Literal["text"] = "text"


@dataclass(slots=True)
class ToolCall:
    """模型提出的结构化工具调用。"""

    id: str
    name: str
    arguments: dict[str, Any]
    type: Literal["tool_call"] = "tool_call"


AssistantBlock: TypeAlias = TextBlock | ToolCall


@dataclass(slots=True)
class UserMessage:
    content: str
    timestamp: int = field(default_factory=now_ms)
    role: Literal["user"] = "user"


@dataclass(slots=True)
class AssistantMessage:
    """一次模型调用完成后形成的 Assistant 消息。

    stop_reason 为 tool_use 时，Agent Loop 会执行其中的 ToolCall；否则通常结束。
    """

    content: list[AssistantBlock] = field(default_factory=list)
    stop_reason: Literal["stop", "tool_use", "error", "aborted"] = "stop"
    error_message: str | None = None
    timestamp: int = field(default_factory=now_ms)
    role: Literal["assistant"] = "assistant"

    @property
    def text(self) -> str:
        return "".join(block.text for block in self.content if isinstance(block, TextBlock))

    @property
    def tool_calls(self) -> list[ToolCall]:
        return [block for block in self.content if isinstance(block, ToolCall)]


@dataclass(slots=True)
class ToolResult:
    """工具执行的标准结果。

    terminate 只是运行时提示：只有同一批所有工具结果都为 True，循环才提前停止。
    """

    content: str
    details: dict[str, Any] = field(default_factory=dict)
    terminate: bool = False


@dataclass(slots=True)
class ToolResultMessage:
    tool_call_id: str
    tool_name: str
    content: str
    is_error: bool = False
    details: dict[str, Any] = field(default_factory=dict)
    timestamp: int = field(default_factory=now_ms)
    role: Literal["tool_result"] = "tool_result"


# Python 的联合类型天然允许应用在 convert_to_llm 前使用自定义对象，
# 因此这里把 AgentMessage 保持为标准消息联合，同时回调签名允许 Any。
AgentMessage: TypeAlias = UserMessage | AssistantMessage | ToolResultMessage
LLMMessage: TypeAlias = dict[str, Any]


@dataclass(slots=True)
class AgentContext:
    """每次循环读取的上下文快照。"""

    system_prompt: str
    messages: list[Any]
    tools: list[Any]


@dataclass(slots=True)
class AgentEvent:
    """统一事件信封。

    event.type 表达稳定语义；data 携带不同事件的载荷。
    这样 UI 无需理解 Agent Loop 内部控制流。
    """

    type: Literal[
        "agent_start",
        "agent_end",
        "turn_start",
        "turn_end",
        "message_start",
        "message_update",
        "message_end",
        "tool_execution_start",
        "tool_execution_update",
        "tool_execution_end",
    ]
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AgentState:
    """Agent 对外可见的可变状态。

    streaming_message 和 pending_tool_calls 是运行时派生状态，不写入模型上下文。
    """

    system_prompt: str
    model: Any
    tools: list[Any] = field(default_factory=list)
    messages: list[Any] = field(default_factory=list)
    is_streaming: bool = False
    streaming_message: AssistantMessage | None = None
    pending_tool_calls: set[str] = field(default_factory=set)
    error_message: str | None = None

