# pi mono `packages/agent` 源码架构分析

分析基于本地下载仓库中 `packages/agent` 和其直接依赖 `packages/ai` 的源码。当前包版本为 `0.80.6`。

主要核对文件：

- `packages/agent/src/types.ts`
- `packages/agent/src/agent-loop.ts`
- `packages/agent/src/agent.ts`
- `packages/agent/src/harness/agent-harness.ts`
- `packages/agent/src/harness/types.ts`
- `packages/agent/src/harness/session/session.ts`
- `packages/agent/src/harness/compaction/*`
- `packages/agent/docs/*`
- `packages/ai/src/types.ts`

## 1. 准确定位

`packages/agent` 不是一个包含 Planner、长期 Memory、RAG、Handoff 和企业治理的全功能 Agent 平台。源码呈现的是两个层级：

```text
@earendil-works/pi-ai
    模型、Provider、消息、工具 Schema、流式响应
                ↓
pi-agent Core
    Agent Loop、状态、事件、Tool 执行、控制队列
                ↓
Agent Harness
    Session、资源、Hooks、压缩、分支、耐久执行适配
```

Core 的价值是提供一个足够薄、可嵌入 UI 或更高层 Harness 的 Agent 内核；Harness 才把这个内核包装成更接近 coding-agent 应用平台的形态。

## 2. Core 的主要组成

### 2.1 `types.ts`：协议中心

源码没有用一个万能 `Agent` 类承载全部概念，而是先定义稳定协议：

- `AgentMessage`：Agent 内部消息，可通过 TypeScript declaration merging 添加自定义消息；
- `AgentContext`：`systemPrompt + messages + tools`；
- `AgentTool`：在 `pi-ai Tool` 之上增加 label、executionMode、execute 和流式 update；
- `AgentEvent`：Agent、Turn、Message 和 Tool 的生命周期事件；
- `AgentLoopConfig`：模型调用、消息转换、上下文转换、队列、Hook、工具执行模式；
- `AgentState`：模型、系统提示词、工具、消息和运行时派生状态。

关键判断：pi 的扩展点首先体现在“协议”而不是继承层次。Agent Loop 只依赖这些函数和数据类型。

### 2.2 `packages/ai`：模型传输层

`packages/agent` 并不自己实现 OpenAI、Anthropic、Google 等 Provider。它依赖 `@earendil-works/pi-ai` 提供：

- 标准 `Model`、`Message`、`Tool` 类型；
- Provider 适配和模型注册；
- `streamSimple` 等流函数；
- Assistant 流事件；
- Token、usage、thinking、tool-call 等跨 Provider 表达。

因此分层边界是：

```text
pi-ai：怎样与模型通信
pi-agent：怎样围绕模型响应运行 Agent 循环
```

这使 Agent Core 不需要包含 Provider `if/else`。

### 2.3 `agent-loop.ts`：无状态执行内核

低层 API 有两组形态：

- `agentLoop()` / `agentLoopContinue()`：返回事件流；
- `runAgentLoop()` / `runAgentLoopContinue()`：接收 event sink 并直接执行。

核心闭环可以还原成：

```text
追加 pending messages
→ transformContext
→ convertToLlm
→ 调用模型并转发流事件
→ 得到 AssistantMessage
→ 提取 ToolCall
→ preflight + execute + postprocess
→ ToolResult 按模型原始调用顺序写回
→ turn_end
→ shouldStopAfterTurn
→ steering
→ 自动工具后续轮次
→ follow-up
→ agent_end
```

这里存在三个重要分界点。

#### 消息处理分成两阶段

```text
AgentMessage[]
→ transformContext()
→ AgentMessage[]
→ convertToLlm()
→ pi-ai Message[]
```

`transformContext` 负责压缩、裁剪和注入上下文；`convertToLlm` 负责协议转换与过滤 UI-only/custom messages。把两者分开，避免“上下文策略”和“模型协议”耦合。

#### 一个 Turn 不等于一个 Tool

一个 Turn 是“一次 LLM 响应 + 该响应产生的整批 Tool 执行”。工具执行结束后才发 `turn_end`。如果仍需模型解释 ToolResult，才开始下一 Turn。

#### 低层流是 observational

README 明确说明低层 `agentLoop()` 保证事件产生顺序，但不会把异步消费者当成生产阶段屏障。需要屏障语义时使用高层 `Agent` 类。

### 2.4 `agent.ts`：状态容器与控制外观

`Agent` 类没有重新实现循环，它主要完成：

- 保存 `AgentState`；
- 消费 loop 事件并同步 `streamingMessage`、`pendingToolCalls`、错误信息；
- 管理 `prompt()`、`continue()`、`abort()`、`waitForIdle()`；
- 管理 subscriber，并按注册顺序 await；
- 管理 steering/follow-up 两个消息队列；
- 把用户配置组装为 `AgentLoopConfig`。

高层 Agent 把 `message_end` 事件处理成屏障。因此 AssistantMessage 已经进入 Agent 状态后，`beforeToolCall` 才开始。这对于 UI 持久化、审计和审批非常重要。

## 3. 工具执行设计

### 3.1 Preflight 与 Execute 分离

工具调用先经历：

```text
查找工具
→ 参数 JSON 解析/Schema 校验
→ tool_execution_start
→ beforeToolCall
→ execute
→ afterToolCall
→ tool_execution_end
→ ToolResultMessage
```

参数错误、未知工具和 before hook 拒绝会变成 `isError: true` 的 ToolResult，反馈给模型，而不是轻易让整个 Agent 崩溃。

### 3.2 Parallel 是默认值，但有批次升级规则

默认工具批次并行：

- Preflight 按源顺序进行；
- 允许的工具并发执行；
- `tool_execution_end` 按真实完成顺序发出；
- 持久化 ToolResult 和 `turn_end.toolResults` 仍按 Assistant 中的源顺序排列。

如果批次中任意工具声明 `executionMode: sequential`，整批升级为串行。这避免有顺序要求的工具与其他调用交错。

### 3.3 terminate 是全批一致语义

Tool 或 `afterToolCall` 可以设置 `terminate: true`，但只有整批每个最终结果都为 true 才提前终止。混合批次仍让模型看到全部结果并继续。这避免某一个辅助工具意外吞掉其他工具之后的模型总结。

## 4. Steering 与 Follow-up

pi 没有把所有用户输入都视为同一种队列。

### Steering

- 用于 Agent 正在工作时改变方向；
- 当前 Assistant 的工具批次不会被硬中断；
- 当前 Turn 完成后注入；
- 优先于自动停止和 follow-up。

### Follow-up

- 用于 Agent 正常完成当前工作后追加任务；
- 只有没有 ToolCall、没有 steering 时才轮询；
- 可以设置 `one-at-a-time` 或 `all`。

这是一个实用的交互模型：不尝试把已经发出的副作用“假装撤销”，而是在安全边界（Turn 结束）改变下一步输入。

## 5. 事件模型

事件形成嵌套结构：

```text
agent_start
  turn_start
    message_start/update/end (user/assistant)
    tool_execution_start/update/end
    message_start/end (toolResult)
  turn_end
agent_end
```

它同时服务于：

- 流式 UI；
- AgentState 同步；
- Tool 进度展示；
- Session 持久化；
- Hooks 与 observability。

`agent_end` 是最后一个 loop 事件，但高层 `prompt()` 和 `waitForIdle()` 会等到被 await 的 `agent_end` subscribers 完成后才 settle。这使“flush session”可以成为完成语义的一部分。

## 6. Harness 的组成与职责

Harness 不是简单别名，而是 Core 上方的应用运行层。

### 6.1 AgentHarness

它负责：

- phase 状态机：`idle/turn/compaction/branch_summary/retry`；
- 每 Turn 获取资源快照；
- 动态 system prompt；
- 把 Harness hooks 适配到 Core 的 transform、stream、tool hooks；
- 在消息事件处积累/flush session 写入；
- 技能和 Prompt Template 调用；
- 模型、thinking level、active tools 更新；
- compact、navigateTree、branch summary。

### 6.2 Session 是树，不是简单 messages 数组

`SessionTreeEntry` 包含：

- message；
- model/thinking/tools 变更；
- compaction；
- branch summary；
- custom/custom_message；
- label 和 session_info。

每个 entry 带 parentId，当前 leaf 决定活跃分支。这支持回到历史节点、生成分支摘要和从不同分支继续。

### 6.3 存储端口与环境抽象

Harness 把文件和 shell 抽象成 `ExecutionEnv`，把 Session 持久化抽象成 `SessionStorage/SessionRepo`。已有内存和 JSONL 实现。这使浏览器、Node、远端执行或 durable harness 可以替换基础设施，而不改 Agent Loop。

### 6.4 Compaction

Context Compaction 属于 Harness 而非 Core：

- 判断需保留和需总结的消息；
- 调用模型生成摘要；
- 把 compaction 写成 Session entry；
- 后续从摘要 + 保留消息构建上下文。

这正好印证 Core 中 `transformContext` 的设计：Core 提供缝隙，Harness实现策略。

### 6.5 Hooks 是可返回 patch 的拦截器

Harness 不只有观察事件。部分 hooks 可以返回结果并修改执行：

- `before_agent_start` 修改 system prompt；
- `context` 修改消息；
- `before_provider_request/payload` 修改流配置或 payload；
- `tool_call` 阻止调用；
- `tool_result` 修改结果；
- compaction/tree hooks 提供摘要或取消操作。

因此其 Hook 系统兼具 observer 与 interceptor 两种语义。

## 7. 关键设计总结

1. **薄内核**：Provider 在 pi-ai，策略在 Harness，Core 只做 Agent Loop。
2. **数据和函数组合优先**：核心扩展通过 callback、event、port，而非复杂继承树。
3. **消息双阶段转换**：上下文策略与模型协议分离。
4. **事件即边界**：UI、状态同步和持久化围绕同一事件协议。
5. **Turn 是原子交互单位**：Steering 等待当前工具批次完成，避免破坏副作用语义。
6. **并发执行与确定性记录兼得**：完成事件按时间，Transcript 按源顺序。
7. **错误可观察**：工具错误优先转成模型可见结果，让 Agent 有机会恢复。
8. **高层提供 barrier**：状态和 subscriber 处理完成后才进入下一生产阶段。
9. **Harness 快照化资源**：一个 Turn 内使用稳定资源，Turn 间允许动态更新。
10. **Session 使用追加式树结构**：便于审计、分支、压缩和恢复。

## 8. 它没有刻意解决什么

Core 本身没有提供：

- Planner/Reviewer 固定范式；
- 多 Agent Handoff 协议；
- 企业权限和审批；
- 分布式任务租约；
- 外部写操作幂等；
- 长期语义 Memory；
- RAG 平台。

这不是缺陷，而是边界选择。合理扩展方式是让这些系统围绕 Tool、transformContext、Harness Hooks、Session Storage 和外部 Durable Runtime 接入。
