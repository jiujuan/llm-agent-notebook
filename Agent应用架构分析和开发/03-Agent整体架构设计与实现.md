当你已经有：

```text
Model Hub
Prompt Hub
```

接下来 **Agent Hub** 不能简单理解为：

```text
Prompt + LLM = Agent
```

这种设计在真实业务里很快失效。

更合理的抽象是：

```text
Agent = Goal + Reasoning + Tool + Memory + Prompt + Model
```

Agent Hub 是整个 AIOS 的「执行中枢」。

------

# Agent Hub 在 AIOS 中的位置

```text
┌─────────────────────┐
│      Model Hub      │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│     Prompt Hub      │
└─────────┬───────────┘
          │
┌─────────▼───────────┐
│      Agent Hub      │
└─────┬───────┬───────┘
      │       │
      │       │
      ▼       ▼

Knowledge Hub   MCP Hub
      │
      ▼

Workflow Hub
```

------

# Agent Hub职责

Agent负责：

```text
Agent定义
Agent配置
Agent执行
Agent编排
Agent记忆
Agent工具调用
Agent推理
Agent日志
Agent监控
```

------

# Agent核心抽象

很多框架：

- LangGraph
- CrewAI
- AutoGen
- OpenAI Agent SDK

最终都会收敛成：

```typescript
Agent
{
    brain
    memory
    tools
    model
    prompt
}
```

------

# 目录结构

```text
src/modules/agent

├── domain
│
├── agent.entity.ts
├── agent-memory.entity.ts
├── agent-tool.entity.ts
├── agent-execution.entity.ts
│
├── schemas
│
├── create-agent.schema.ts
├── execute-agent.schema.ts
├── update-agent.schema.ts
│
├── repository
│
├── agent.repository.ts
├── memory.repository.ts
│
├── service
│
├── agent.service.ts
├── agent-executor.service.ts
├── agent-memory.service.ts
├── agent-tool.service.ts
├── agent-planner.service.ts
│
├── engine
│
├── AgentRuntime.ts
├── AgentContext.ts
├── AgentLoop.ts
├── ToolDispatcher.ts
├── MemoryManager.ts
│
└── controller
    └── agent.controller.ts
```

------

# Agent实体

```typescript
export interface Agent {

  id:string;

  name:string;

  description?:string;

  modelId:string;

  promptVersionId:string;

  memoryEnabled:boolean;

  maxIterations:number;

  status:
    | "ACTIVE"
    | "PAUSED";

  createdAt:Date;
}
```

------

# Agent Memory

```typescript
export interface AgentMemory {

  id:string;

  agentId:string;

  sessionId:string;

  role:
    | "user"
    | "assistant"
    | "tool";

  content:string;

  createdAt:Date;
}
```

类似：

```text
User
你好

Assistant
你好

Tool
搜索结果...
```

------

# Agent Tool

```typescript
export interface AgentTool {

  id:string;

  name:string;

  description:string;

  inputSchema:any;

  enabled:boolean;
}
```

例如：

```text
search
calculator
weather
database
knowledge
mcp
```

------

# Agent Execution

```typescript
export interface AgentExecution {

  id:string;

  agentId:string;

  sessionId:string;

  input:string;

  output:string;

  cost:number;

  tokenUsage:number;

  startedAt:Date;

  completedAt?:Date;
}
```

------

# Zod

Create Agent

```typescript
import { z } from "zod";

export const CreateAgentSchema =
  z.object({

    name:z.string(),

    description:z.string().optional(),

    modelId:z.string(),

    promptVersionId:z.string(),

    memoryEnabled:z.boolean(),

    maxIterations:z.number()
  });

export type CreateAgentDto =
  z.infer<typeof CreateAgentSchema>;
```

------

执行Agent

```typescript
export const ExecuteAgentSchema =
  z.object({

    agentId:z.string(),

    sessionId:z.string(),

    input:z.string()
  });
```

------

# Agent Context

运行时上下文

```typescript
export interface AgentContext {

  sessionId:string;

  agentId:string;

  input:string;

  memories:string[];

  toolResults:string[];

  currentIteration:number;
}
```

------

# Agent Runtime

Agent执行器核心

```typescript
export interface AgentRuntime {

  run(
    context:AgentContext
  ):Promise<string>;
}
```

------

# Tool抽象

统一工具接口

```typescript
export interface Tool {

  name:string;

  description:string;

  execute(
    input:any
  ):Promise<any>;
}
```

------

# Search Tool

```typescript
export class SearchTool
implements Tool {

  name="search";

  description="search web";

  async execute(input:any){

    return {
      result:"search result"
    };
  }
}
```

------

# Calculator Tool

```typescript
export class CalculatorTool
implements Tool {

  name="calculator";

  description="calculate";

  async execute(input:any){

    return eval(input.expression);
  }
}
```

（生产环境不要直接 eval，这里只是示意）

------

# Tool Dispatcher

```typescript
export class ToolDispatcher {

  constructor(
    private tools:Tool[]
  ){}

  getTool(name:string){

    return this.tools.find(
      x => x.name === name
    );
  }

  async invoke(
    name:string,
    input:any
  ){

    const tool =
      this.getTool(name);

    if(!tool){

      throw new Error(
        "tool not found"
      );
    }

    return tool.execute(input);
  }
}
```

------

# Memory Manager

```typescript
export class MemoryManager {

  constructor(
    private memoryRepo:any
  ){}

  async load(
    sessionId:string
  ){

    return this.memoryRepo.findMany({
      sessionId
    });
  }

  async save(
    sessionId:string,
    role:string,
    content:string
  ){

    return this.memoryRepo.create({
      sessionId,
      role,
      content
    });
  }
}
```

------

# Planner

Agent思考层

```typescript
export interface Plan {

  thought:string;

  tool?:string;

  toolInput?:any;

  finalAnswer?:string;
}
```

------

Planner Prompt

```text
你是Agent Planner

可用工具:

{{tools}}

用户问题:

{{input}}

返回JSON:

{
  thought:"",
  tool:"",
  toolInput:{}
}
```

------

Planner Service

```typescript
export class AgentPlannerService {

  constructor(
    private modelInvoker:ModelInvoker
  ){}

  async plan(
    prompt:string
  ):Promise<Plan>{

    const result =
      await this.modelInvoker.invoke(
        "planner-model",
        prompt
      );

    return JSON.parse(
      result.content
    );
  }
}
```

------

# Agent Loop

Agent核心循环

```typescript
while(true){

  think()

  if(finalAnswer){

      return answer
  }

  useTool()

  observe()

}
```

实现：

```typescript
export class AgentLoop {

  constructor(

    private planner:
      AgentPlannerService,

    private dispatcher:
      ToolDispatcher
  ){}

  async run(
    context:AgentContext
  ){

    while(
      context.currentIteration < 10
    ){

      const plan =
        await this.planner.plan(
          JSON.stringify(context)
        );

      if(plan.finalAnswer){

        return plan.finalAnswer;
      }

      const result =
        await this.dispatcher.invoke(
          plan.tool!,
          plan.toolInput
        );

      context.toolResults.push(
        JSON.stringify(result)
      );

      context.currentIteration++;
    }

    throw new Error(
      "max iteration exceeded"
    );
  }
}
```

------

# Agent Executor

Agent统一入口

```typescript
export class AgentExecutorService {

  constructor(

    private memoryManager:
      MemoryManager,

    private loop:
      AgentLoop
  ){}

  async execute(
    agent:Agent,
    sessionId:string,
    input:string
  ){

    const memories =
      await this.memoryManager.load(
        sessionId
      );

    const context = {

      agentId:agent.id,

      sessionId,

      input,

      memories:
        memories.map(
          x=>x.content
        ),

      toolResults:[],

      currentIteration:0
    };

    const output =
      await this.loop.run(
        context
      );

    await this.memoryManager.save(
      sessionId,
      "user",
      input
    );

    await this.memoryManager.save(
      sessionId,
      "assistant",
      output
    );

    return output;
  }
}
```

------

# Prisma设计

Agent

```prisma
model Agent {

  id String @id @default(uuid())

  name String

  description String?

  modelId String

  promptVersionId String

  memoryEnabled Boolean

  maxIterations Int

  status String

  createdAt DateTime @default(now())
}
```

------

AgentMemory

```prisma
model AgentMemory {

  id String @id @default(uuid())

  agentId String

  sessionId String

  role String

  content String @db.Text

  createdAt DateTime @default(now())
}
```

------

AgentExecution

```prisma
model AgentExecution {

  id String @id @default(uuid())

  agentId String

  sessionId String

  input String @db.Text

  output String @db.Text

  cost Float

  tokenUsage Int

  createdAt DateTime @default(now())
}
```

------

# API设计

创建Agent

```http
POST /agents
```

查询Agent

```http
GET /agents
```

执行Agent

```http
POST /agents/execute
```

请求：

```json
{
  "agentId":"sales-agent",
  "sessionId":"session-001",
  "input":"帮我分析客户需求"
}
```

------

# 下一阶段（真正AIOS）

当后面继续扩展时，Agent Hub会升级成：

```text
Agent Hub
│
├── Agent Registry
├── Agent Runtime
├── Agent Planner
├── Agent Memory
├── Agent Tool
├── Agent Skill
├── Agent Role
├── Agent Team
├── Agent Evaluation
├── Agent Monitoring
├── Agent Marketplace
└── Agent Security
```

然后进一步支持：

```text
Single Agent

↓

Multi Agent

↓

Agent Team

↓

Agent Organization
```

类似：

- CrewAI
- AutoGen
- LangGraph
- OpenAI Agents

的架构演进路线。

如果结合前面已经设计的 Model Hub + Prompt Hub，那么一个比较成熟的 AIOS 分层会是：

```text
Foundation Layer
├── Model Hub
├── Prompt Hub

Execution Layer
├── Agent Hub
├── Workflow Hub

Knowledge Layer
├── Knowledge Hub
├── MCP Hub

Application Layer
├── AI Apps
├── AI Employees
├── AI SaaS
```

这样各层职责清晰，后续扩展多 Agent、RAG、工作流和 MCP 都不会推翻已有设计。