"""示例 2：工具调用、进度事件和 steering。"""

import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mini_pi_agent import (
    Agent,
    AgentOptions,
    AgentTool,
    AssistantMessage,
    ScriptedModel,
    TextBlock,
    ToolCall,
    ToolResult,
)


async def calculate(context, arguments):
    await context.on_update(ToolResult("正在计算……"))
    await asyncio.sleep(0.01)
    return ToolResult(str(arguments["a"] + arguments["b"]), {"operation": "add"})


async def main() -> None:
    model = ScriptedModel(
        [
            AssistantMessage([ToolCall("call-1", "calculate", {"a": 2, "b": 3})], "tool_use"),
            AssistantMessage([TextBlock("计算结果是 5。")]),
            AssistantMessage([TextBlock("补充：这是整数加法。")]),
        ]
    )
    tool = AgentTool(
        name="calculate",
        description="两个整数相加",
        parameters={"type": "object", "required": ["a", "b"]},
        execute=calculate,
    )
    agent = Agent(AgentOptions(system_prompt="使用工具完成计算。", model=model, tools=[tool]))

    async def observe(event, _signal):
        if event.type in {"tool_execution_start", "tool_execution_update", "tool_execution_end"}:
            print(event.type, event.data)
        if event.type == "message_update":
            print(event.data["delta"], end="", flush=True)
        # 第一次最终回答结束后，排入 follow-up；它会在本轮结束后触发下一轮。
        if event.type == "message_end" and getattr(event.data.get("message"), "text", "") == "计算结果是 5。":
            agent.follow_up("请补充说明计算类型")

    agent.subscribe(observe)
    await agent.prompt("2 + 3 等于多少？")
    print()


if __name__ == "__main__":
    asyncio.run(main())
