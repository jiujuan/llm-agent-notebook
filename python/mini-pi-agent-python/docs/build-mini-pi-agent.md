# 一步一步实现 mini pi agent

## 第 1 步：先定义协议，不写循环

阅读顺序从 `mini_pi_agent/types.py` 开始。

这里定义 `UserMessage`、`AssistantMessage`、`ToolCall`、`ToolResultMessage`、`AgentEvent` 和 `AgentState`。先定义协议的原因是：模型、工具、UI 和 Agent Runtime 都要共享它们；如果直接从 while-loop 开始，后续会充满隐式字典和特殊判断。

`AssistantMessage.content` 是 block 数组而不是纯字符串，因此一次响应可以同时包含文本和多个 ToolCall。

## 第 2 步：把模型变成端口

`mini_pi_agent/model.py` 的 `Model` 只有一个 `stream()` 方法。Agent Loop 不知道请求最终发给 OpenAI、OpenRouter、vLLM 还是 FakeModel。

`ScriptedModel` 是最重要的测试工具：它让 ToolCall 和最终回答完全可预测，因此控制流测试不依赖真实模型概率。

## 第 3 步：定义 Tool，而不是让循环直接调用函数

`mini_pi_agent/tools.py` 给工具增加：

- 名称、描述和参数 Schema；
- parallel/sequential 提示；
- 取消信号；
- `on_update` 流式进度回调；
- 标准 `ToolResult`。

这使 Tool 执行可以被统一验证、观测和治理。

## 第 4 步：实现无状态 Agent Loop

`mini_pi_agent/loop.py` 是核心。请沿着 `run_agent_loop()` 阅读：

1. 发出 `agent_start`；
2. 注入 pending/steering 消息；
3. 发出 `turn_start`；
4. 对每条输入发出 message start/end；
5. 调用 `_stream_assistant_response()`；
6. 如果存在 ToolCall，调用 `_execute_tool_calls()`；
7. 发出 `turn_end`；
8. 依次判断 stop hook、terminate、steering、自动 Tool 后续、follow-up；
9. 最终发出 `agent_end`。

循环接收外部 `context`，并通过 `emit` 输出事件，因此没有隐藏的 UI 或数据库依赖。

## 第 5 步：实现工具批次

`_execute_tool_calls()` 展示一个很容易被忽略的设计：

```text
并行执行顺序 != Transcript 保存顺序
```

并行任务通过 `asyncio.as_completed()` 让结束事件尽快出现，但最终 ToolResultMessage 按 `source_index` 排序。用户能及时看到进度，模型又能得到稳定消息序列。

`_execute_one_tool()` 把异常转成 error result。这样文件不存在、参数错误或策略拒绝都成为下一轮模型的 Observation。

## 第 6 步：在 Core 上包有状态 Agent

`mini_pi_agent/agent.py` 提供用户友好 API：

```python
await agent.prompt("hello")
agent.steer("change direction")
agent.follow_up("also summarize")
agent.abort()
await agent.wait_for_idle()
```

`Agent._emit()` 的顺序非常重要：

```text
先 apply event 到 AgentState
→ 再按注册顺序 await subscribers
→ 返回低层 loop
```

所以 subscriber 能看到最新状态，且可以在 `message_end` 中安全完成持久化后，才允许 Tool preflight 继续。

## 第 7 步：加入 Session，但不污染 Loop

`MemorySession` 只负责跨 `prompt()` 调用保存消息。Agent Loop 完全不知道 Session 的存在。

如果要扩展成 pi Harness 的树形 Session，应新增 `SessionEntry(parent_id, type, payload)` 和 Storage port，而不是修改模型调用核心。

## 第 8 步：用测试锁定语义

测试覆盖：

- ToolCall 后自动进入下一模型轮次；
- 事件与消息顺序；
- mixed terminate 不提前结束；
- before hook 拒绝后工具不执行；
- streaming state 同步；
- subscriber barrier；
- follow-up 在正常完成点后进入下一轮。

运行：

```powershell
python -m pytest -q
```

## 下一步扩展建议

按优先级可以继续加入：

1. 完整 JSON Schema 参数校验；
2. 真正的 Provider SSE 流；
3. 超时和重试；
4. SQLite/JSONL Session；
5. append-only Session tree；
6. Context compaction；
7. Tool 权限、审批和幂等；
8. OpenTelemetry Trace；
9. Durable task/checkpoint 层。

保持原则：这些能力应通过端口、事件、Hook 或 Harness 加入，不要把所有逻辑塞回 `run_agent_loop()`。

