# mini-pi-agent-python

这是一个只使用 Python 3 标准库的教学项目，用来复现 `pi-agent-core` 最有辨识度的架构思想。

它不是官方 Python SDK，也不追求逐字段兼容 TypeScript API。目标是让读者可以在约 1000 行以内看清：

- Agent 状态与无状态 Agent Loop 如何分离；
- AgentMessage 如何经过两阶段处理后发送给 LLM；
- 模型输出如何驱动工具调用和后续模型轮次；
- 工具批次如何并行执行、按源顺序写回消息；
- before/after hook、terminate、steering 和 follow-up 如何进入控制流；
- 事件为什么既是 UI 协议，也是 Agent 状态同步协议。

详细源码分析见 [docs/pi-agent-architecture.md](docs/pi-agent-architecture.md)，逐步实现说明见 [docs/build-mini-pi-agent.md](docs/build-mini-pi-agent.md)。

## 目录

```text
mini-pi-agent-python/
├── pyproject.toml
├── README.md
├── mini_pi_agent/
│   ├── __init__.py
│   ├── types.py       # Message、ToolCall、Event、State
│   ├── model.py       # 模型端口与 OpenAI-compatible 适配器
│   ├── tools.py       # Tool 定义、参数校验、进度回调
│   ├── loop.py        # 无状态 Agent Loop
│   ├── agent.py       # 有状态 Agent 外观、事件屏障、队列
│   ├── session.py     # 最小内存 Session
│   └── fake_model.py  # 确定性测试模型
├── examples/
│   ├── basic.py
│   └── tool_and_steering.py
├── tests/
│   ├── test_agent_loop.py
│   └── test_agent.py
└── docs/
    ├── pi-agent-architecture.md
    └── build-mini-pi-agent.md
```

## 快速运行

```powershell
cd mini-pi-agent-python
python examples\basic.py
python examples\tool_and_steering.py
python -m pytest -q
```

## 连接 OpenAI-compatible 服务

```python
from mini_pi_agent import Agent, AgentOptions, OpenAICompatibleModel

model = OpenAICompatibleModel(
    model="your-model-id",
    api_key="your-api-key",
    base_url="http://localhost:8000/v1",  # 也可指向 OpenAI/OpenRouter
)

agent = Agent(AgentOptions(
    system_prompt="You are a helpful assistant.",
    model=model,
))
```

适配器采用 Chat Completions 兼容协议；不同服务的非标准扩展并未覆盖。

## 明确没有实现的生产能力

- 完整 JSON Schema 校验；
- 真正的 SSE Provider 流式传输；
- pi Harness 的树形 Session、分支和 compaction；
- Durable Harness、分布式恢复和持久化队列；
- Provider 重试、限流、计费、Tracing；
- Tool 权限、审批、沙箱和外部副作用幂等。

这些是有意保留的扩展边界，而不是应该偷偷塞进 Agent Loop 的职责。

