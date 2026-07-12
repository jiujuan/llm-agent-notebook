"""示例 1：不调用真实网络的基础流式回答。"""

import asyncio
from pathlib import Path
import sys

# 允许在没有 pip install 的情况下直接运行：python examples/basic.py
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mini_pi_agent import Agent, AgentOptions, AssistantMessage, ScriptedModel, TextBlock


async def main() -> None:
    model = ScriptedModel([AssistantMessage([TextBlock("你好，我是 mini pi agent。")])])
    agent = Agent(AgentOptions(system_prompt="你是一个简洁的助手。", model=model))

    async def print_events(event, _signal) -> None:
        if event.type == "message_update":
            print(event.data["delta"], end="", flush=True)
        elif event.type == "agent_end":
            print()

    agent.subscribe(print_events)
    await agent.prompt("你好")


if __name__ == "__main__":
    asyncio.run(main())
