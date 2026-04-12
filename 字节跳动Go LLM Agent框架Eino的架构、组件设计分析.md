字节跳动Go LLM Agent框架Eino的架构、组件设计分析

## 一、Eino 框架介绍

Eino 是字节跳动 CloudWeGo 团队开源的Go 企业级 LLM 大模型应用开发框架，提供了一个强调简洁性、可扩展性、可靠性与有效性，且更符合 Go 语言编程惯例的 LLM 应用开发框架。

Eino 提供的功能特性如下：

- 精心设计了的一系列 **组件（component）** 抽象与实现，可轻松复用与组合，用于构建 LLM 应用。
- 智能体开发套件（ADK），提供构建 AI 智能体的高级抽象，支持多智能体编排、人机协作中断机制以及预置的智能体模式。

- 强大的 **编排（orchestration）** 框架，为用户承担繁重的类型检查、流式处理、并发管理、切面注入、选项赋值等工作。
  - Chain ：简单的链式有向图，只能向前推进。
  - Graph ：有向有环或无环图。功能强大且灵活。
  - Workflow ：有向无环图，支持在结构体字段级别进行数据映射。
  
- 一套精心设计、注重简洁明了的 API。

- 以集成 流程（flow） 和 示例（example） 形式不断扩充的最佳实践集合。

- 一套实用 **工具（DevOps tools）**，涵盖从可视化开发与调试到在线追踪与评估的整个开发生命周期。

借助上述能力和工具，Eino 能够在人工智能应用开发生命周期的不同阶段实现标准化、简化操作并提高效率：

![Eino在人工智能应用开发生命周期的不同阶段实现标准化](https://img2024.cnblogs.com/blog/650581/202604/650581-20260410191955366-299590019.png)
（图片来自 https://www.cloudwego.io/）

## 二、Eino 框架整体结构

### 设计理念介绍
Eino 采用分层、模块化架构，将框架核心能力拆分为 Eino 与 Eino-ext 两大体系，同时配套全生命周期 DevOps 工具链。

核心设计理念分析：

- 静态类型安全：基于 Go 泛型实现编译时类型检查，彻底避免动态语言运行时类型断言的心智负担，上下游节点类型不匹配在编译阶段即可发现，大幅提升企业级生产环境稳定性。

- 接口与实现强解耦：核心仓库仅定义组件接口、编排机制、通用能力；所有具体实现（如 OpenAI 模型、向量数据库接入）均放在扩展仓库，实现「定义 - 实现」分离，组件可插拔、可替换、可自定义。

- 流式处理原生支持：框架层统一处理流的拼接、装箱、合并、复制，组件只需实现业务相关的流式范式，流式处理对开发者透明。

- 全生命周期工程化：覆盖从研发设计、开发调试、部署上线到运维监控的 AI 应用全流程，提供可观测、可调试、可审计、可灰度的企业级能力。

### Eino框架架构图

**Eino框架分层架构图**：

Eino框架分层架构图

![Eino分层架构图](https://img2024.cnblogs.com/blog/650581/202604/650581-20260410200221474-1826736789.png)
(AI生成图片)

```json
┌─────────────────────────────────────────────────────────────┐
│  应用层（Flow/ADK）：预置 Agent 范式、多智能体编排、高级模式    │
├─────────────────────────────────────────────────────────────┤
│  编排层（Compose）：Chain/Graph/Workflow 三大编排引擎        │
├─────────────────────────────────────────────────────────────┤
│  组件层（Components）：LLM 应用原子组件接口抽象与规范           │
├─────────────────────────────────────────────────────────────┤
│  基础层（Schema）：统一数据模型、通用契约、流处理基础能力       │
└─────────────────────────────────────────────────────────────┘
       ↖️  横切能力：Callback 切面、State 状态、Option 配置  ↗️
```


**Eino框架整体结构图**：

Eino框架整体结构图，包含组件

![Eino框架整体结构](https://img2024.cnblogs.com/blog/650581/202604/650581-20260410194122024-553176619.png)

### 框架中的核心模块

#### **基础层 Schema 层**

Schema 层是统一数据契约，定义了框架所有组件交互的通用数据结构与接口契约，确保不同组件、不同模块之间的数据互通性，核心内容包括，

**核心数据模型**：

- [Message](https://github.com/cloudwego/eino/blob/v0.8.8/schema/message.go)：对话消息核心结构，包含角色（User/System/Assistant/Tool）、文本内容、工具调用信息、多模态内容支持，是 LLM 交互的核心载体。

每条消息携带一个 RoleType（System、User、Assistant、Tool），其内容可以是简单字符串或由多个 ChatMessagePart 组成的多模态集合，外加通过 ToolCall 结构体提供的可选工具调用信息。消息系统通过 MessagesTemplate 接口。

- [Document](https://github.com/cloudwego/eino/blob/v0.8.8/schema/document.go)：文档数据结构，支持文本内容、元数据、密集向量 / 稀疏向量，是 RAG 场景的核心数据模型。
```go
// https://github.com/cloudwego/eino/blob/v0.8.8/schema/document.go
type Document struct {
	// ID is the unique identifier of the document.
	ID string `json:"id"`
	// Content is the content of the document.
	Content string `json:"content"`
	// MetaData is the metadata of the document, can be used to store extra information.
	MetaData map[string]any `json:"meta_data"`
}
```

- [ToolInfo](https://github.com/cloudwego/eino/blob/v0.8.8/schema/tool.go)：toolcall工具调用数据结构，包含工具名称、参数、额外信息，标准化模型工具调用的解析与执行。

- [Stream](https://github.com/cloudwego/eino/blob/v0.8.8/schema/stream.go)：流式模型构建在 StreamReader/StreamWriter 对之上，StreamReader[T] 是一个基于 channel 的泛型，泛型流式读取器，是全链路流式处理的核心，统一封装不同类型的流数据操作。

**Callback**

包提供了可观测性子系统，让你无需修改组件代码即可监控、追踪和埋点记录每次组件调用。回调在五个生命周期时机触发：`OnStart`、`OnEnd`、`OnError`、`OnStartWithStreamInput` 和 `OnEndWithStreamOutput`

#### Components 组件层

大模型应用开发和传统应用开发最显著的区别在于大模型所具备的两大核心能力：

- **基于语义的文本处理能力**：能够理解和生成人类语言，处理非结构化的内容语义关系
- **智能决策能力**：能够基于上下文进行推理和判断，做出相应的行为决策



这两项核心能力催生了三种主要的应用模式：

1. **直接对话模式**：处理用户输入并生成相应回答
2. **知识处理模式**：对文本文档进行语义化处理、存储和检索
3. **工具调用模式**：基于上下文做出决策并调用相应工具

> Components 组件层 详细的介绍：https://www.cloudwego.io/zh/docs/eino/core_modules/components/



组件是大模型应用能力的提供者，是大模型应用构建过程中的砖和瓦，组件抽象的优劣决定了大模型应用开发的复杂度，Eino 的组件抽象秉持着以下设计原则：

1. **模块化和标准化**，将一系列功能相同的能力抽象成统一的模块，组件间职能明确、边界清晰，支持灵活地组合。
2. **可扩展性**，接口的设计保持尽可能小的模块能力约束，让组件的开发者能方便地实现自定义组件的开发。
3. **可复用性**，把最常用的能力和实现进行封装，提供给开发者开箱即用的工具使用。

接口最小化设计：每个组件仅定义核心能力，避免过度封装，保证灵活性。实现透明化：组件的具体实现对上层无感知，任何实现了对应接口的组件，均可无缝替换、接入编排流程。

Components 层是 Eino 构建 LLM 应用的「乐高积木」，核心设计是面向接口编程，为每一类 LLM 应用核心构建块定义标准化的接口契约，明确输入输出类型、运行时 Option、流处理范式，彻底屏蔽底层实现差异。



核心子模块包括：`model`（ChatModel 抽象）、`tool`（工具抽象）、`prompt`（提示词模板）、`retriever`（检索器）、`document`（文档处理）、`embedding`（向量嵌入）、`indexer`（向量索引）等。

| 组件                      | 接口                               | 核心方法                                           | 流式支持                                 |
| ------------------------- | ---------------------------------- | -------------------------------------------------- | ---------------------------------------- |
| **mode(ChatModel)**       | `BaseChatModel`                    | `Generate(ctx, []*Message) (*Message, error)`      | `Stream` → `StreamReader[*Message]`      |
| **Tool**                  | `InvokableTool` / `StreamableTool` | `InvokableRun(ctx, json) (string, error)`          | `StreamableRun` → `StreamReader[string]` |
| **Retriever**             | `Retriever`                        | `Retrieve(ctx, string) ([]*Document, error)`       | 通过 Runnable 适配器                     |
| **Embedding**             | `Embedder`                         | `Embed(ctx, []Document) ([][]float64, error)`      | 通过 Runnable 适配器                     |
| **document(Loader)**      | `Loader`                           | `Load(ctx, Source) ([]*Document, error)`           | 通过 Runnable 适配器                     |
| **document(Transformer)** | `Transformer`                      | `Transform(ctx, []*Document) ([]*Document, error)` | 通过 Runnable 适配器                     |
| **Prompt(ChatTemplate)**  | `ChatTemplate`                     | `Format(ctx, map) ([]*Message, error)`             | 通过 Runnable 适配器                     |
| **Indexer**               | `Indexer`                          | `Index(ctx, []*Document) error`                    |                                          |



components/tool/interface:

定义了 `Invokable`/`Streamable` 两大核心接口，规范所有组件的调用范式：`Invoke`（同步调用）、`Stream`（流式调用）、`Collect`（流收束）、`Transform`（流转换）

#### Compose 层：编排核心层



### Eino 框架的几个部分组成：

- [Eino](https://github.com/cloudwego/eino)：包含类型定义、流数据处理机制、组件抽象定义、编排功能、Agent 核心接口、切面机制等。
- [EinoExt](https://github.com/cloudwego/eino-ext)：扩展实现，组件与工具的实现、回调处理程序实现、组件使用示例，以及各种工具，如评估器、DevOps 工具、提示优化器等。

>💡 针对字节内部使用的组件，有对应的内部代码仓库：

- [Eino Devops](https://github.com/cloudwego/eino-ext/tree/main/devops)：可视化开发、可视化调试、链路追踪等。
- [EinoExamples](https://github.com/cloudwego/eino-examples)：是包含示例应用程序和最佳实践的代码仓库（RAG、智能体、多智能体协作等）。

上面也是Eino的仓库体系，采用多仓库协同的架构，严格分离抽象、实现、工具与示例


## 参考

- https://www.cloudwego.io/zh/docs/eino/overview/ Eino 概述
- https://www.cloudwego.io/zh/docs/eino/overview/eino_open_source/