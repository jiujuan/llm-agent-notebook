"""有状态 Agent 外观。

对应 pi-agent-core 的 Agent 类：

- 持有可变 AgentState；
- 把低层事件同步回 state；
- 提供 prompt/continue/abort/wait_for_idle；
- 提供 steering/follow-up 队列；
- 订阅者按注册顺序 await，形成明确的状态屏障。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Literal
import asyncio

from .loop import AgentLoopConfig, run_agent_loop, run_agent_loop_continue
from .model import Model
from .session import MemorySession
from .tools import AgentTool
from .types import (
    AgentContext,
    AgentEvent,
    AgentState,
    AssistantMessage,
    LLMMessage,
    ToolResultMessage,
    UserMessage,
)


Subscriber = Callable[[AgentEvent, asyncio.Event], Awaitable[None] | None]


class _PendingMessageQueue:
    def __init__(self, mode: Literal["all", "one-at-a-time"] = "one-at-a-time") -> None:
        self.mode = mode
        self._items: list[Any] = []

    def push(self, message: Any) -> None:
        self._items.append(message)

    async def drain(self) -> list[Any]:
        if not self._items:
            return []
        if self.mode == "all":
            items, self._items = self._items, []
            return items
        return [self._items.pop(0)]

    def clear(self) -> None:
        self._items.clear()


def default_convert_to_llm(messages: list[Any]) -> list[LLMMessage]:
    """AgentMessage -> LLMMessage 的默认桥梁。

    自定义 UI 消息会被忽略；应用也可以注入自己的转换函数。
    """

    converted: list[LLMMessage] = []
    for message in messages:
        if isinstance(message, UserMessage):
            converted.append({"role": "user", "content": message.content})
        elif isinstance(message, AssistantMessage):
            content: list[dict[str, Any]] = []
            tool_calls: list[dict[str, Any]] = []
            for block in message.content:
                if getattr(block, "type", None) == "text":
                    content.append({"type": "text", "text": block.text})
                elif getattr(block, "type", None) == "tool_call":
                    tool_calls.append(
                        {
                            "id": block.id,
                            "type": "function",
                            "function": {"name": block.name, "arguments": __import__("json").dumps(block.arguments)},
                        }
                    )
            payload: LLMMessage = {"role": "assistant", "content": "".join(p["text"] for p in content)}
            if tool_calls:
                payload["tool_calls"] = tool_calls
            converted.append(payload)
        elif isinstance(message, ToolResultMessage):
            converted.append(
                {
                    "role": "tool",
                    "tool_call_id": message.tool_call_id,
                    "content": message.content,
                }
            )
    return converted


@dataclass(slots=True)
class AgentOptions:
    system_prompt: str
    model: Model
    tools: list[AgentTool] | None = None
    messages: list[Any] | None = None
    convert_to_llm: Callable[[list[Any]], list[LLMMessage] | Awaitable[list[LLMMessage]]] = default_convert_to_llm
    transform_context: Callable[[list[Any], asyncio.Event], Awaitable[list[Any]]] | None = None
    tool_execution: Literal["parallel", "sequential"] = "parallel"
    steering_mode: Literal["all", "one-at-a-time"] = "one-at-a-time"
    follow_up_mode: Literal["all", "one-at-a-time"] = "one-at-a-time"
    max_turns: int = 20
    before_tool_call: Any = None
    after_tool_call: Any = None
    should_stop_after_turn: Any = None
    session: MemorySession | None = None


class Agent:
    def __init__(self, options: AgentOptions) -> None:
        self.state = AgentState(
            system_prompt=options.system_prompt,
            model=options.model,
            tools=list(options.tools or []),
            messages=list(options.messages or []),
        )
        self.convert_to_llm = options.convert_to_llm
        self.transform_context = options.transform_context
        self.tool_execution = options.tool_execution
        self.max_turns = options.max_turns
        self.before_tool_call = options.before_tool_call
        self.after_tool_call = options.after_tool_call
        self.should_stop_after_turn = options.should_stop_after_turn
        self.session = options.session
        self._steering = _PendingMessageQueue(options.steering_mode)
        self._follow_up = _PendingMessageQueue(options.follow_up_mode)
        self._subscribers: list[Subscriber] = []
        self._abort_signal = asyncio.Event()
        self._active_task: asyncio.Task[list[Any]] | None = None

    def subscribe(self, listener: Subscriber) -> Callable[[], None]:
        self._subscribers.append(listener)

        def unsubscribe() -> None:
            if listener in self._subscribers:
                self._subscribers.remove(listener)

        return unsubscribe

    async def _emit(self, event: AgentEvent) -> None:
        """先更新 AgentState，再按注册顺序等待订阅者。

        这让 message_end 成为工具 preflight 前的屏障，是 pi 高层 Agent 相对低层流的关键差异。
        """

        self._apply_event(event)
        for subscriber in list(self._subscribers):
            result = subscriber(event, self._abort_signal)
            if hasattr(result, "__await__"):
                await result

    def _apply_event(self, event: AgentEvent) -> None:
        data = event.data
        if event.type == "agent_start":
            self.state.is_streaming = True
            self.state.error_message = None
        elif event.type == "message_start" and isinstance(data.get("message"), AssistantMessage):
            self.state.streaming_message = data["message"]
        elif event.type == "message_update":
            self.state.streaming_message = data["message"]
        elif event.type == "message_end":
            message = data.get("message")
            self.state.streaming_message = None
            if isinstance(message, AssistantMessage) and message.stop_reason == "error":
                self.state.error_message = message.error_message or "model error"
            # 低层循环稍后也维护 context.messages；这里不重复 append。
        elif event.type == "tool_execution_start":
            self.state.pending_tool_calls.add(data["tool_call_id"])
        elif event.type == "tool_execution_end":
            self.state.pending_tool_calls.discard(data["tool_call_id"])
        elif event.type == "agent_end":
            self.state.streaming_message = None
            self.state.pending_tool_calls.clear()
            self.state.is_streaming = False

    def _config(self) -> AgentLoopConfig:
        return AgentLoopConfig(
            model=self.state.model,
            convert_to_llm=self.convert_to_llm,
            transform_context=self.transform_context,
            get_steering_messages=self._steering.drain,
            get_follow_up_messages=self._follow_up.drain,
            before_tool_call=self.before_tool_call,
            after_tool_call=self.after_tool_call,
            should_stop_after_turn=self.should_stop_after_turn,
            tool_execution=self.tool_execution,
            max_turns=self.max_turns,
        )

    async def prompt(self, prompt: str | Any) -> list[Any]:
        if self.state.is_streaming:
            raise RuntimeError("agent is already running; use steer() or follow_up()")
        if self.session and not self.state.messages:
            self.state.messages.extend(await self.session.load())
        message = UserMessage(prompt) if isinstance(prompt, str) else prompt
        return await self._start([message], continuing=False)

    async def continue_run(self) -> list[Any]:
        if self.state.is_streaming:
            raise RuntimeError("agent is already running")
        return await self._start([], continuing=True)

    async def _start(self, prompts: list[Any], continuing: bool) -> list[Any]:
        self._abort_signal = asyncio.Event()
        context = AgentContext(self.state.system_prompt, self.state.messages, self.state.tools)

        async def run() -> list[Any]:
            if continuing:
                new_messages = await run_agent_loop_continue(
                    context, self._config(), self._emit, self._abort_signal
                )
            else:
                new_messages = await run_agent_loop(
                    prompts, context, self._config(), self._emit, self._abort_signal
                )
            if self.session:
                await self.session.append(new_messages)
            return new_messages

        self._active_task = asyncio.create_task(run())
        try:
            return await self._active_task
        finally:
            self._active_task = None

    def steer(self, message: str | Any) -> None:
        if not self.state.is_streaming:
            raise RuntimeError("cannot steer an idle agent")
        self._steering.push(UserMessage(message) if isinstance(message, str) else message)

    def follow_up(self, message: str | Any) -> None:
        if not self.state.is_streaming:
            raise RuntimeError("cannot queue follow-up for an idle agent")
        self._follow_up.push(UserMessage(message) if isinstance(message, str) else message)

    def abort(self) -> None:
        self._abort_signal.set()
        if self._active_task:
            self._active_task.cancel()

    async def wait_for_idle(self) -> None:
        task = self._active_task
        if task:
            try:
                await task
            except asyncio.CancelledError:
                pass

    def reset(self) -> None:
        if self.state.is_streaming:
            raise RuntimeError("cannot reset while running")
        self.state.messages.clear()
        self.state.error_message = None
        self._steering.clear()
        self._follow_up.clear()

