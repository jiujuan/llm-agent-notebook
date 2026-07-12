> Prompt Hub架构设计和实现，用typescript+zod

如果你后面要做：

```text
Model Hub
Prompt Hub
Agent Hub
Workflow Hub
Knowledge Hub
MCP Hub
```

那么 **Prompt Hub 不应该只是 Prompt 模板管理**。

很多团队第一版设计成：

```text
Prompt
├── name
├── content
└── version
```

很快就废了。

因为 Agent、Workflow、RAG、MCP 都会依赖 Prompt。

所以 Prompt Hub 应该设计成：

```text
Prompt = AI应用中的最小能力单元
```

类似：

```text
Java
Class

Spring
Bean

K8S
Pod

AIOS
Prompt
```

------

# 一、Prompt Hub定位

Prompt Hub负责：

```text
Prompt创建
Prompt版本管理
Prompt变量管理
Prompt测试
Prompt发布
Prompt运行
Prompt依赖管理
Prompt分类管理
Prompt评测
Prompt调用统计
```

架构位置：

```text
                    ┌──────────────┐
                    │   Model Hub  │
                    └──────┬───────┘
                           │
                           ▼

┌───────────────────────────────────┐
│          Prompt Hub               │
└───────────────────────────────────┘
         │
         ├────────► Agent Hub
         │
         ├────────► Workflow Hub
         │
         ├────────► Knowledge Hub
         │
         └────────► MCP Hub
```

------

# 二、目录结构

```text
src
│
├── modules
│
│   └── prompt
│
│       ├── domain
│       │
│       ├── prompt.entity.ts
│       ├── prompt-version.entity.ts
│       ├── prompt-variable.entity.ts
│       └── prompt-category.entity.ts
│
│
│       ├── schemas
│       │
│       ├── create-prompt.schema.ts
│       ├── update-prompt.schema.ts
│       ├── test-prompt.schema.ts
│       └── execute-prompt.schema.ts
│
│
│       ├── repository
│       │
│       └── prompt.repository.ts
│
│
│       ├── service
│       │
│       ├── prompt.service.ts
│       ├── prompt-render.service.ts
│       ├── prompt-test.service.ts
│       └── prompt-execute.service.ts
│
│
│       ├── controller
│       │
│       └── prompt.controller.ts
│
│
│       └── engine
│
│           ├── TemplateEngine.ts
│           ├── VariableResolver.ts
│           └── PromptCompiler.ts
```

------

# 三、领域模型设计

Prompt

```typescript
export interface Prompt {

  id:string;

  name:string;

  description?:string;

  categoryId:string;

  latestVersion:string;

  status:
    | "DRAFT"
    | "PUBLISHED"
    | "ARCHIVED";

  createdAt:Date;

  updatedAt:Date;
}
```

------

PromptVersion

真正运行的是Version

```typescript
export interface PromptVersion {

  id:string;

  promptId:string;

  version:string;

  systemPrompt:string;

  userPrompt:string;

  modelId:string;

  temperature:number;

  topP:number;

  maxTokens:number;

  published:boolean;

  createdAt:Date;
}
```

例如：

```text
System

你是一名资深产品经理

User

请分析以下需求：

{{requirement}}
```

------

PromptVariable

```typescript
export interface PromptVariable {

  id:string;

  promptVersionId:string;

  name:string;

  type:
    | "string"
    | "number"
    | "boolean"
    | "json";

  required:boolean;

  defaultValue?:string;
}
```

例如：

```text
requirement
```

------

# 四、Zod设计

Create Prompt

```typescript
import { z } from "zod";

export const CreatePromptSchema =
  z.object({

    name:z.string(),

    description:z.string().optional(),

    categoryId:z.string()
  });

export type CreatePromptDto =
  z.infer<typeof CreatePromptSchema>;
```

------

Create Version

```typescript
export const CreatePromptVersionSchema =
  z.object({

    promptId:z.string(),

    version:z.string(),

    systemPrompt:z.string(),

    userPrompt:z.string(),

    modelId:z.string(),

    temperature:z.number(),

    topP:z.number(),

    maxTokens:z.number()
  });
```

------

执行Prompt

```typescript
export const ExecutePromptSchema =
  z.object({

    versionId:z.string(),

    variables:z.record(
      z.string(),
      z.any()
    )
  });
```

------

# 五、Prompt编译器

核心能力

Prompt → 最终Prompt

------

TemplateEngine.ts

```typescript
export class TemplateEngine {

  render(
    template:string,
    variables:Record<string,any>
  ){

    return template.replace(
      /\{\{(.*?)\}\}/g,

      (_,key)=>{

        return String(
          variables[key.trim()] ?? ""
        );
      }
    );
  }
}
```

------

例子

模板：

```text
请分析：

{{requirement}}
```

变量：

```json
{
  "requirement":"做一个AI客服"
}
```

结果：

```text
请分析：

做一个AI客服
```

------

# 六、PromptCompiler

```typescript
export class PromptCompiler {

  constructor(
    private templateEngine:
      TemplateEngine
  ){}

  compile(
    systemPrompt:string,

    userPrompt:string,

    variables:Record<string,any>
  ){

    return {

      system:

      this.templateEngine.render(
        systemPrompt,
        variables
      ),

      user:

      this.templateEngine.render(
        userPrompt,
        variables
      )
    };
  }
}
```

------

# 七、Prompt Execute

这是Prompt Hub核心

```typescript
Prompt

↓ compile

Final Prompt

↓ invoke

Model Hub

↓ response

Result
```

------

PromptExecuteService

```typescript
export class PromptExecuteService {

  constructor(

    private compiler:
      PromptCompiler,

    private modelInvoker:
      ModelInvoker
  ){}

  async execute(
    version:PromptVersion,

    variables:Record<string,any>
  ){

    const compiled =
      this.compiler.compile(

        version.systemPrompt,

        version.userPrompt,

        variables
      );

    const finalPrompt =
`
${compiled.system}

${compiled.user}
`;

    return this.modelInvoker.invoke(
      version.modelId,
      finalPrompt
    );
  }
}
```

------

# 八、数据库设计

Prompt

```prisma
model Prompt {

  id String @id @default(uuid())

  name String

  description String?

  categoryId String

  latestVersion String?

  status String

  createdAt DateTime @default(now())

  updatedAt DateTime @updatedAt

  versions PromptVersion[]
}
```

------

PromptVersion

```prisma
model PromptVersion {

  id String @id @default(uuid())

  promptId String

  version String

  systemPrompt String @db.Text

  userPrompt String @db.Text

  modelId String

  temperature Float

  topP Float

  maxTokens Int

  published Boolean

  createdAt DateTime @default(now())

  prompt Prompt @relation(
    fields:[promptId],
    references:[id]
  )
}
```

------

# 九、API设计

创建Prompt

```http
POST /prompts
```

------

创建版本

```http
POST /prompts/version
```

------

发布版本

```http
POST /prompts/version/:id/publish
```

------

测试Prompt

```http
POST /prompts/test
```

Body

```json
{
  "versionId":"xxx",
  "variables":{
    "requirement":"开发AI销售系统"
  }
}
```

------

执行Prompt

```http
POST /prompts/execute
```

------

获取Prompt历史版本

```http
GET /prompts/:id/versions
```

------

# 十、升级版（企业级）

真正生产环境的 Prompt Hub 会继续增加：

```text
Prompt Hub
│
├── Prompt Template
│
├── Prompt Version
│
├── Prompt Variable
│
├── Prompt Tag
│
├── Prompt Category
│
├── Prompt Evaluation
│
├── Prompt Dataset
│
├── Prompt Playground
│
├── Prompt A/B Testing
│
├── Prompt Cost Analysis
│
├── Prompt Execution History
│
├── Prompt Trace
│
├── Prompt Optimization
│
└── Prompt Marketplace
```

这时 Prompt Hub 的定位已经不是“提示词管理”，而是类似于：

- PromptLayer
- LangSmith Prompt Hub
- Dify Prompt
- OpenAI Playground + Prompt Registry

成为整个 AIOS 中连接 **Model Hub → Agent Hub → Workflow Hub → Knowledge Hub** 的中枢层。