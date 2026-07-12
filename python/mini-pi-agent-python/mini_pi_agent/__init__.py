"""mini-pi-agent 的公开 API。

这个包不是 pi-agent-core 的 Python 绑定，而是一个用于学习其核心设计的最小实现。
"""

from .agent import Agent, AgentOptions
from .fake_model import ScriptedModel
from .model import Model, OpenAICompatibleModel
from .session import MemorySession
from .tools import AgentTool, ToolExecutionContext
from .types import (
    AgentContext,
    AgentEvent,
    AgentState,
    AssistantMessage,
    TextBlock,
    ToolCall,
    ToolResult,
    ToolResultMessage,
    UserMessage,
)

__all__ = [
    "Agent",
    "AgentOptions",
    "AgentContext",
    "AgentEvent",
    "AgentState",
    "AgentTool",
    "AssistantMessage",
    "MemorySession",
    "Model",
    "OpenAICompatibleModel",
    "ScriptedModel",
    "TextBlock",
    "ToolCall",
    "ToolExecutionContext",
    "ToolResult",
    "ToolResultMessage",
    "UserMessage",
]

