import asyncio

from mini_pi_agent import Agent, AgentOptions, AssistantMessage, ScriptedModel, TextBlock


def test_agent_updates_streaming_state_and_awaits_subscribers():
    async def scenario():
        model = ScriptedModel([AssistantMessage([TextBlock("ok")])])
        agent = Agent(AgentOptions(system_prompt="system", model=model))
        observed = []

        async def subscriber(event, _signal):
            await asyncio.sleep(0)
            observed.append((event.type, agent.state.is_streaming))

        agent.subscribe(subscriber)
        await agent.prompt("hello")

        assert agent.state.is_streaming is False
        assert agent.state.messages[-1].text == "ok"
        assert observed[-1] == ("agent_end", False)

    asyncio.run(scenario())


def test_follow_up_runs_after_normal_completion_point():
    async def scenario():
        model = ScriptedModel(
            [AssistantMessage([TextBlock("first")]), AssistantMessage([TextBlock("second")])]
        )
        agent = Agent(AgentOptions(system_prompt="system", model=model))
        queued = False

        async def subscriber(event, _signal):
            nonlocal queued
            message = event.data.get("message")
            if event.type == "message_end" and getattr(message, "text", "") == "first" and not queued:
                queued = True
                agent.follow_up("more")

        agent.subscribe(subscriber)
        await agent.prompt("start")

        assert len(model.requests) == 2
        assert [m.role for m in agent.state.messages] == ["user", "assistant", "user", "assistant"]
        assert agent.state.messages[-1].text == "second"

    asyncio.run(scenario())

