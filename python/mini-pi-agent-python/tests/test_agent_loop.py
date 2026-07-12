import asyncio

from mini_pi_agent.agent import default_convert_to_llm
from mini_pi_agent.fake_model import ScriptedModel
from mini_pi_agent.loop import AgentLoopConfig, run_agent_loop
from mini_pi_agent.tools import AgentTool
from mini_pi_agent.types import (
    AgentContext,
    AgentEvent,
    AssistantMessage,
    TextBlock,
    ToolCall,
    ToolResult,
    UserMessage,
)


def test_tool_loop_preserves_event_and_message_order():
    async def scenario():
        async def add(ctx, args):
            await ctx.on_update(ToolResult("working"))
            return ToolResult(str(args["a"] + args["b"]))

        model = ScriptedModel(
            [
                AssistantMessage([ToolCall("c1", "add", {"a": 1, "b": 2})], "tool_use"),
                AssistantMessage([TextBlock("3")]),
            ]
        )
        context = AgentContext(
            "system",
            [],
            [AgentTool("add", "add numbers", {"required": ["a", "b"]}, add)],
        )
        events: list[AgentEvent] = []

        async def emit(event):
            events.append(event)

        await run_agent_loop(
            [UserMessage("1+2")],
            context,
            AgentLoopConfig(model=model, convert_to_llm=default_convert_to_llm),
            emit,
            asyncio.Event(),
        )

        assert [m.role for m in context.messages] == ["user", "assistant", "tool_result", "assistant"]
        types = [e.type for e in events]
        assert types[0] == "agent_start"
        assert "tool_execution_update" in types
        assert types[-1] == "agent_end"
        assert len(model.requests) == 2

    asyncio.run(scenario())


def test_terminate_requires_every_tool_in_batch():
    async def scenario():
        async def ending(_ctx, _args):
            return ToolResult("done", terminate=True)

        async def continuing(_ctx, _args):
            return ToolResult("keep going", terminate=False)

        model = ScriptedModel(
            [
                AssistantMessage(
                    [ToolCall("a", "ending", {}), ToolCall("b", "continuing", {})], "tool_use"
                ),
                AssistantMessage([TextBlock("followed up")]),
            ]
        )
        context = AgentContext(
            "system",
            [],
            [
                AgentTool("ending", "", {}, ending),
                AgentTool("continuing", "", {}, continuing),
            ],
        )

        async def emit(_event):
            pass

        await run_agent_loop(
            [UserMessage("go")],
            context,
            AgentLoopConfig(model=model, convert_to_llm=default_convert_to_llm),
            emit,
            asyncio.Event(),
        )
        assert len(model.requests) == 2
        assert context.messages[-1].text == "followed up"

    asyncio.run(scenario())


def test_before_hook_can_block_tool_as_observation():
    async def scenario():
        executed = False

        async def dangerous(_ctx, _args):
            nonlocal executed
            executed = True
            return ToolResult("should not run")

        async def before(_call, _args, _context):
            return {"block": True, "reason": "policy denied"}

        model = ScriptedModel(
            [
                AssistantMessage([ToolCall("x", "danger", {})], "tool_use"),
                AssistantMessage([TextBlock("blocked safely")]),
            ]
        )
        context = AgentContext("system", [], [AgentTool("danger", "", {}, dangerous)])

        async def emit(_event):
            pass

        await run_agent_loop(
            [UserMessage("go")],
            context,
            AgentLoopConfig(
                model=model,
                convert_to_llm=default_convert_to_llm,
                before_tool_call=before,
            ),
            emit,
            asyncio.Event(),
        )
        assert executed is False
        result = next(message for message in context.messages if message.role == "tool_result")
        assert result.is_error is True
        assert result.content == "policy denied"

    asyncio.run(scenario())


def test_parallel_completion_events_but_source_ordered_results():
    async def scenario():
        async def slow(_ctx, _args):
            await asyncio.sleep(0.02)
            return ToolResult("slow")

        async def fast(_ctx, _args):
            await asyncio.sleep(0)
            return ToolResult("fast")

        model = ScriptedModel(
            [
                AssistantMessage(
                    [ToolCall("slow-id", "slow", {}), ToolCall("fast-id", "fast", {})],
                    "tool_use",
                ),
                AssistantMessage([TextBlock("finished")]),
            ]
        )
        context = AgentContext(
            "system",
            [],
            [AgentTool("slow", "", {}, slow), AgentTool("fast", "", {}, fast)],
        )
        end_order = []

        async def emit(event):
            if event.type == "tool_execution_end":
                end_order.append(event.data["tool_call_id"])

        await run_agent_loop(
            [UserMessage("go")],
            context,
            AgentLoopConfig(model=model, convert_to_llm=default_convert_to_llm),
            emit,
            asyncio.Event(),
        )

        assert end_order == ["fast-id", "slow-id"]
        persisted = [m.tool_call_id for m in context.messages if m.role == "tool_result"]
        assert persisted == ["slow-id", "fast-id"]

    asyncio.run(scenario())


def test_steering_is_injected_before_automatic_tool_follow_up():
    async def scenario():
        steering = [UserMessage("change direction")]

        async def drain_steering():
            nonlocal steering
            result, steering = steering, []
            return result

        async def lookup(_ctx, _args):
            return ToolResult("data")

        model = ScriptedModel(
            [
                AssistantMessage([ToolCall("x", "lookup", {})], "tool_use"),
                AssistantMessage([TextBlock("changed")]),
            ]
        )
        context = AgentContext("system", [], [AgentTool("lookup", "", {}, lookup)])

        async def emit(_event):
            pass

        # 第一次启动时 queue 会被轮询，因此先返回空；工具完成后的第二次轮询返回 steering。
        polls = 0

        async def delayed_steering():
            nonlocal polls
            polls += 1
            if polls == 1:
                return []
            return await drain_steering()

        await run_agent_loop(
            [UserMessage("start")],
            context,
            AgentLoopConfig(
                model=model,
                convert_to_llm=default_convert_to_llm,
                get_steering_messages=delayed_steering,
            ),
            emit,
            asyncio.Event(),
        )
        roles = [m.role for m in context.messages]
        assert roles == ["user", "assistant", "tool_result", "user", "assistant"]
        assert context.messages[3].content == "change direction"

    asyncio.run(scenario())
