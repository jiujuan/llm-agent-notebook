"""mini-pi-agent 的核心执行循环。

对应 pi-agent-core 的 agent-loop.ts，本模块有意保持“无状态函数”风格：

    输入消息 + AgentContext + LoopConfig -> 异步事件流

高层 Agent 类负责保存状态、消费事件和实现订阅屏障；低层循环只关心控制流。
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Awaitable, Callable, Literal
import asyncio

from .model import Model, ModelRequest, tool_to_openai_schema
from .tools import AgentTool, ToolExecutionContext
from .types import (
    AgentContext,
    AgentEvent,
    AgentMessage,
    AssistantMessage,
    LLMMessage,
    TextBlock,
    ToolCall,
    ToolResult,
    ToolResultMessage,
)


EventSink = Callable[[AgentEvent], Awaitable[None]]
ConvertToLlm = Callable[[list[Any]], Awaitable[list[LLMMessage]] | list[LLMMessage]]
TransformContext = Callable[[list[Any], asyncio.Event], Awaitable[list[Any]]]
MessageProvider = Callable[[], Awaitable[list[Any]]]
BeforeToolCall = Callable[[ToolCall, dict[str, Any], AgentContext], Awaitable[dict[str, Any] | None]]
AfterToolCall = Callable[
    [ToolCall, ToolResult, bool, AgentContext], Awaitable[dict[str, Any] | None]
]
ShouldStopAfterTurn = Callable[[AssistantMessage, list[ToolResultMessage], AgentContext, list[Any]], Awaitable[bool] | bool]


@dataclass(slots=True)
class AgentLoopConfig:
    model: Model
    convert_to_llm: ConvertToLlm
    transform_context: TransformContext | None = None
    get_steering_messages: MessageProvider | None = None
    get_follow_up_messages: MessageProvider | None = None
    before_tool_call: BeforeToolCall | None = None
    after_tool_call: AfterToolCall | None = None
    should_stop_after_turn: ShouldStopAfterTurn | None = None
    tool_execution: Literal["parallel", "sequential"] = "parallel"
    max_turns: int = 20


@dataclass(slots=True)
class _FinalizedToolCall:
    source_index: int
    call: ToolCall
    result: ToolResult
    is_error: bool


async def _maybe_await(value: Any) -> Any:
    if hasattr(value, "__await__"):
        return await value
    return value


async def run_agent_loop(
    prompts: list[Any],
    context: AgentContext,
    config: AgentLoopConfig,
    emit: EventSink,
    signal: asyncio.Event,
) -> list[Any]:
    """从一组新消息开始运行，直到完成、终止或达到 max_turns。"""

    await emit(AgentEvent("agent_start"))
    new_messages: list[Any] = []
    pending_messages = list(prompts)
    turns = 0

    try:
        while True:
            if signal.is_set():
                raise asyncio.CancelledError()
            if turns >= config.max_turns:
                raise RuntimeError(f"maximum turns exceeded: {config.max_turns}")

            # Steering 也允许在第一次模型调用前到达。
            if config.get_steering_messages:
                pending_messages.extend(await config.get_steering_messages())

            turns += 1
            await emit(AgentEvent("turn_start", {"turn": turns}))

            for message in pending_messages:
                context.messages.append(message)
                new_messages.append(message)
                await emit(AgentEvent("message_start", {"message": message}))
                await emit(AgentEvent("message_end", {"message": message}))
            pending_messages = []

            assistant = await _stream_assistant_response(context, config, emit, signal)
            context.messages.append(assistant)
            new_messages.append(assistant)

            tool_results: list[ToolResultMessage] = []
            terminate_batch = False
            if assistant.tool_calls:
                tool_results, terminate_batch = await _execute_tool_calls(
                    assistant.tool_calls, context, config, emit, signal
                )
                context.messages.extend(tool_results)
                new_messages.extend(tool_results)

            await emit(
                AgentEvent(
                    "turn_end",
                    {"message": assistant, "tool_results": tool_results, "turn": turns},
                )
            )

            if config.should_stop_after_turn and await _maybe_await(
                config.should_stop_after_turn(assistant, tool_results, context, new_messages)
            ):
                break

            # pi 的 terminate 是“全批一致”语义。混合批次仍继续下一轮。
            if terminate_batch:
                break

            steering = await config.get_steering_messages() if config.get_steering_messages else []
            if steering:
                pending_messages = steering
                continue

            if assistant.tool_calls:
                # 工具结果已加入上下文，自动再调用一次模型，让模型解释结果。
                continue

            follow_up = await config.get_follow_up_messages() if config.get_follow_up_messages else []
            if follow_up:
                pending_messages = follow_up
                continue

            break

        return new_messages
    finally:
        # 即使中途异常/取消也发送结束事件，便于上层清理 streaming 状态。
        await emit(AgentEvent("agent_end", {"messages": list(new_messages)}))


async def run_agent_loop_continue(
    context: AgentContext,
    config: AgentLoopConfig,
    emit: EventSink,
    signal: asyncio.Event,
) -> list[Any]:
    """不追加新用户消息，从既有 user/tool_result 上下文继续。"""

    if not context.messages:
        raise ValueError("cannot continue an empty context")
    if getattr(context.messages[-1], "role", None) not in {"user", "tool_result"}:
        raise ValueError("continue requires the last message to be user or tool_result")
    return await run_agent_loop([], context, config, emit, signal)


async def _stream_assistant_response(
    context: AgentContext,
    config: AgentLoopConfig,
    emit: EventSink,
    signal: asyncio.Event,
) -> AssistantMessage:
    messages = list(context.messages)
    if config.transform_context:
        messages = await config.transform_context(messages, signal)
    llm_messages = await _maybe_await(config.convert_to_llm(messages))

    request = ModelRequest(
        system_prompt=context.system_prompt,
        messages=llm_messages,
        tools=[tool_to_openai_schema(tool) for tool in context.tools],
    )
    partial = AssistantMessage(content=[])
    await emit(AgentEvent("message_start", {"message": partial}))

    final_message: AssistantMessage | None = None
    streamed_text = ""
    async for event in config.model.stream(request, signal):
        if event.type == "text_delta" and event.delta is not None:
            streamed_text += event.delta
            partial = AssistantMessage(content=[TextBlock(streamed_text)])
            await emit(
                AgentEvent(
                    "message_update",
                    {"message": partial, "delta": event.delta},
                )
            )
        elif event.type == "message_end":
            final_message = event.message

    if final_message is None:
        final_message = AssistantMessage(content=[TextBlock(streamed_text)], stop_reason="error")
    await emit(AgentEvent("message_end", {"message": final_message}))
    return final_message


async def _execute_tool_calls(
    calls: list[ToolCall],
    context: AgentContext,
    config: AgentLoopConfig,
    emit: EventSink,
    signal: asyncio.Event,
) -> tuple[list[ToolResultMessage], bool]:
    tools = {tool.name: tool for tool in context.tools}
    # 任一工具要求 sequential，则整批串行，与 pi 的 batch 语义一致。
    force_sequential = config.tool_execution == "sequential" or any(
        tools.get(call.name) and tools[call.name].execution_mode == "sequential" for call in calls
    )

    if force_sequential:
        finalized = []
        for index, call in enumerate(calls):
            finalized.append(await _execute_one_tool(index, call, tools, context, config, emit, signal))
    else:
        tasks = [
            asyncio.create_task(_execute_one_tool(index, call, tools, context, config, emit, signal))
            for index, call in enumerate(calls)
        ]
        # as_completed 让 tool_execution_end 按真实完成顺序发出；随后再按 source_index 排序持久化。
        finalized = [await task for task in asyncio.as_completed(tasks)]

    ordered = sorted(finalized, key=lambda item: item.source_index)
    messages: list[ToolResultMessage] = []
    for item in ordered:
        message = ToolResultMessage(
            tool_call_id=item.call.id,
            tool_name=item.call.name,
            content=item.result.content,
            is_error=item.is_error,
            details=item.result.details,
        )
        messages.append(message)
        await emit(AgentEvent("message_start", {"message": message}))
        await emit(AgentEvent("message_end", {"message": message}))

    terminate = bool(ordered) and all(item.result.terminate for item in ordered)
    return messages, terminate


async def _execute_one_tool(
    source_index: int,
    call: ToolCall,
    tools: dict[str, AgentTool],
    context: AgentContext,
    config: AgentLoopConfig,
    emit: EventSink,
    signal: asyncio.Event,
) -> _FinalizedToolCall:
    await emit(
        AgentEvent(
            "tool_execution_start",
            {"tool_call_id": call.id, "tool_name": call.name, "args": call.arguments},
        )
    )
    tool = tools.get(call.name)
    is_error = False

    try:
        if tool is None:
            raise ValueError(f"unknown tool: {call.name}")
        tool.validate(call.arguments)

        if config.before_tool_call:
            decision = await config.before_tool_call(call, call.arguments, context)
            if decision and decision.get("block"):
                raise PermissionError(decision.get("reason") or "tool call blocked")

        async def on_update(partial: ToolResult) -> None:
            await emit(
                AgentEvent(
                    "tool_execution_update",
                    {
                        "tool_call_id": call.id,
                        "tool_name": call.name,
                        "args": call.arguments,
                        "partial_result": partial,
                    },
                )
            )

        execution_context = ToolExecutionContext(call.id, signal, on_update)
        result = await tool.execute(execution_context, call.arguments)
    except asyncio.CancelledError:
        raise
    except Exception as error:  # 工具异常转成 LLM 可观察的错误结果，而非击穿整个循环。
        is_error = True
        result = ToolResult(content=str(error), details={"error_type": type(error).__name__})

    if config.after_tool_call:
        patch = await config.after_tool_call(call, result, is_error, context)
        if patch:
            result = replace(
                result,
                content=patch.get("content", result.content),
                details=patch.get("details", result.details),
                terminate=patch.get("terminate", result.terminate),
            )

    finalized = _FinalizedToolCall(source_index, call, result, is_error)
    await emit(
        AgentEvent(
            "tool_execution_end",
            {
                "tool_call_id": call.id,
                "tool_name": call.name,
                "result": result,
                "is_error": is_error,
            },
        )
    )
    return finalized

