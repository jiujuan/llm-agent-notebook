OpenAI Agents SDK 本质上是一个**构建 AI Agent（智能体）系统的开发框架**，它不是单纯的大模型调用封装，而是一套围绕 Agent、Tool、Memory、Workflow、Handoff、Guardrail 等能力构建的运行时架构。

如果从系统设计角度分析，可以将其拆解为以下几个核心层次：

```text
┌───────────────────────────────┐
│           Application         │
│       (业务逻辑层)             │
└───────────────┬───────────────┘
                │
┌───────────────▼───────────────┐
│           Agent Layer         │
│    Agent / Handoff / Runner   │
└───────────────┬───────────────┘
                │
┌───────────────▼───────────────┐
│          Tool Layer           │
│ Function / API / MCP / DB     │
└───────────────┬───────────────┘
                │
┌───────────────▼───────────────┐
│        Context Layer          │
│ Memory / Session / State      │
└───────────────┬───────────────┘
                │
┌───────────────▼───────────────┐
│        Guardrail Layer        │
│ Validation / Safety / Policy  │
└───────────────┬───────────────┘
                │
┌───────────────▼───────────────┐
│         Model Layer           │
│ GPT-4o / GPT-4.1 / o3 等      │
└───────────────────────────────┘
```

------

# 1. Agent（智能体）

Agent 是整个 SDK 的核心对象。

一个 Agent 通常包含：

```python
Agent(
    name="Research Agent",
    instructions="你是一个研究助手",
    model="gpt-4.1",
    tools=[search_tool]
)
```

Agent 的职责：

- 定义角色（Role）
- 定义提示词（Instructions）
- 定义能力边界（Tools）
- 决定下一步行动（Reasoning）

可以理解为：

```text
Agent
=
Prompt
+
Model
+
Tools
+
Workflow
```

------

## Agent 内部结构

```text
Agent
│
├── Name
├── Instructions
├── Model
├── Tools
├── Memory
├── Handoffs
└── Guardrails
```

例如：

```python
customer_agent = Agent(
    name="Customer Service",
    instructions="处理客户问题",
    tools=[crm_tool],
    handoffs=[sales_agent]
)
```

------

# 2. Runner（运行器）

Runner 是执行引擎。

负责：

- 调用 Agent
- 管理上下文
- 管理工具调用
- 管理 Agent 切换

例如：

```python
result = Runner.run_sync(
    agent,
    "分析特斯拉未来发展"
)
```

运行流程：

```text
User Input
      │
      ▼
Runner
      │
      ▼
Agent
      │
      ▼
LLM推理
      │
      ├──调用Tool
      ├──切换Agent
      └──直接回答
```

Runner 相当于：

```text
Agent Runtime
```

类似于：

- Spring Boot 的容器
- LangGraph Runtime
- AutoGen Runtime

------

# 3. Tool（工具系统）

Tool 是 Agent 与外部世界交互的能力。

Agent 本身只能思考：

```text
Think
```

Tool 让 Agent 能：

```text
Act
```

------

## Function Tool

最常见

```python
@function_tool
def get_weather(city: str):
    return ...
```

自动转换：

```json
{
  "name":"get_weather",
  "parameters":{
    "city":"string"
  }
}
```

模型可自动调用。

------

## Tool调用流程

```text
Agent
 │
 ▼
LLM
 │
 ▼
Tool Selection
 │
 ▼
Execute Tool
 │
 ▼
Result
 │
 ▼
LLM
 │
 ▼
Answer
```

------

## MCP Tool

支持 Model Context Protocol。

例如：

- Notion
- Slack
- GitHub
- Jira
- PostgreSQL

都可通过 MCP 接入。

```text
Agent
 │
 ▼
MCP Server
 │
 ├──GitHub
 ├──Slack
 ├──Notion
 └──DB
```

这是 Agents SDK 与传统 Function Calling 最大区别之一。

------

# 4. Handoff（Agent协作）

OpenAI Agents SDK 的亮点。

支持多个 Agent 之间协作。

例如：

```text
CEO Agent
    │
    ├── Market Agent
    │
    ├── Product Agent
    │
    └── Finance Agent
```

------

## Handoff机制

```python
ceo_agent = Agent(
    handoffs=[
        market_agent,
        finance_agent
    ]
)
```

运行时：

```text
用户问题
      │
      ▼
CEO Agent
      │
      ▼
发现需要市场分析
      │
      ▼
Handoff
      │
      ▼
Market Agent
```

Agent 自主决定：

```text
是否转交
转交给谁
转交什么内容
```

------

# 5. Context（上下文）

Context 是 Agent 的工作记忆。

包含：

```text
Conversation
+
Tool Results
+
State
+
User Data
```

------

## Context对象

例如：

```python
ctx.user_id
ctx.session_id
ctx.state
```

Agent 和 Tool 都能访问。

```python
def query_order(ctx):
    user_id = ctx.user_id
```

------

## State管理

Agent 可共享状态：

```python
ctx.state["customer_level"] = "VIP"
```

多个 Agent：

```text
Agent A
      │
      ▼
Shared State
      ▲
      │
Agent B
```

------

# 6. Memory（记忆）

当前 SDK 没有像 LangGraph 那样内置长期记忆系统，但提供扩展点。

一般分：

## 短期记忆

当前会话

```text
Session Memory
```

例如：

```python
conversation_history
```

------

## 长期记忆

开发者实现：

```text
Vector DB
Redis
PostgreSQL
Neo4j
```

例如：

```python
retrieve_memory()
```

作为 Tool 接入。

------

# 7. Guardrail（护栏）

Guardrail 是生产环境非常重要的一层。

作用：

```text
输入校验
输出校验
安全控制
合规检查
```

------

## Input Guardrail

用户输入前检查。

```text
User
 │
 ▼
Guardrail
 │
 ▼
Agent
```

例如：

- 敏感词
- Prompt Injection
- 非法请求

------

## Output Guardrail

Agent 输出后检查。

```text
Agent
 │
 ▼
Guardrail
 │
 ▼
User
```

例如：

- PII检测
- 数据脱敏
- 格式验证

------

# 8. Model（模型层）

Agent 实际依赖模型工作。

支持：

- GPT-4.1
- GPT-4o
- GPT-4o-mini
- o3
- o4-mini 等

例如：

```python
Agent(
    model="gpt-4.1"
)
```

------

## 模型层职责

```text
Reasoning
Planning
Tool Selection
Agent Routing
Response Generation
```

即：

```text
Agent的大脑
```

------

# 9. Tracing（链路追踪）

这是企业级开发非常重要的能力。

OpenAI 提供内置 Trace。

```python
from agents import trace
```

可记录：

```text
User Input
↓
Agent Decision
↓
Tool Call
↓
Tool Result
↓
Agent Output
```

类似：

- Jaeger
- Zipkin
- LangSmith

------

架构示意：

```text
Trace
│
├── Agent Start
├── Tool Call
├── Tool Result
├── Handoff
└── Final Output
```

------

# 10. OpenAI Agents SDK 整体架构图

```text
                    User
                      │
                      ▼
              ┌────────────┐
              │   Runner   │
              └─────┬──────┘
                    │
                    ▼
              ┌────────────┐
              │   Agent    │
              └─────┬──────┘
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
  Tool Call     Handoff      Guardrail
      │             │             │
      ▼             ▼             ▼
 Function      Other Agent   Validation
 MCP Server
 Database
 API
      │
      ▼
   Result
      │
      ▼
   Context
      │
      ▼
   Model
      │
      ▼
   Response
```

# 从企业级系统角度看

如果你正在构建 AI 商业系统（客户洞察、营销自动化、销售智能体、CEO Agent 等），可以把 Agents SDK 理解为：

| 组件      | 类比微服务架构     |
| --------- | ------------------ |
| Agent     | Service            |
| Tool      | RPC/API            |
| Handoff   | Service Mesh       |
| Runner    | Kubernetes Runtime |
| Context   | Redis Session      |
| Memory    | Knowledge Base     |
| Guardrail | Gateway + Policy   |
| Trace     | SkyWalking/Jaeger  |
| Model     | CPU（智能核心）    |

因此，一个完整的企业 AI Agent 系统通常会演化为：

```text
CEO Agent
│
├── 市场洞察 Agent
├── 用户研究 Agent
├── 产品策略 Agent
├── 销售 Agent
├── 内容 Agent
└── 数据分析 Agent

       ↓

OpenAI Agents SDK Runtime

       ↓

MCP生态
GitHub
Notion
Slack
CRM
数据库

       ↓

向量数据库
Neo4j
PostgreSQL
Redis
```

这也是目前 OpenAI Agents SDK 最推荐的生产级架构模式：**Agent（决策）+ Tool（执行）+ Handoff（协作）+ Guardrail（治理）+ Trace（观测）**。