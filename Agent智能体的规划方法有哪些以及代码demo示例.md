
我将为您详细分析AI Agent智能体中LLM规划能力的各种主流方法。首先让我进行深入思考和研究。



AI Agent 智能体规划能力：LLM规划方法全面解析

## 引言

在人工智能领域，大语言模型（LLM）已经展现出令人瞩目的推理与规划能力。然而，如何有效地激发和利用这些能力，一直是研究和实践的核心课题。规划能力是智能体（Agent）完成复杂任务的关键所在，它决定了智能体能否像人类一样，将复杂问题分解为可处理的子问题，并在执行过程中进行动态调整和优化。

从技术演进的角度来看，LLM规划能力的发展经历了从简单的Chain of Thought（思维链）到更为复杂的Tree of Thoughts（思维树）和Graph of Thoughts（思维图）的过程。这些方法不仅仅是对提示工程的优化，更是对人类认知过程的深入模拟和工程化实现。随着技术的不断发展，研究者们还提出了ReAct、Reflexion、Plan-and-Execute等多种范式，以应对不同场景下的规划挑战。

本文将系统性地介绍当前主流的LLM规划方法，深入分析其原理和使用步骤，并提供基于DeepSeek API的Python代码示例，帮助读者全面理解和应用这些技术。

## 一、Chain of Thought（思维链）：规划能力的基石

### 1.1 原理深度剖析

Chain of Thought（CoT）方法是LLM规划能力的起点，它通过引导模型生成显式的推理步骤来增强复杂问题的解决能力。这一方法的核心理念源自对人类认知过程的观察：当人类面对复杂问题时，不会直接给出答案，而是会逐步思考、推导和验证。CoT正是将这一认知模式引入到LLM的推理过程中。

从技术实现角度来看，CoT的核心在于将问题求解过程分解为一系列中间推理步骤。在传统的提示方式中，模型直接基于输入生成输出，这种方式虽然简洁，但在处理多步骤推理任务时往往表现不佳。CoT则要求模型在给出最终答案之前，先展示其思考过程——这包括识别问题关键信息、运用逻辑规则进行推导、检验中间结果的正确性等。

CoT的有效性可以从多个角度理解。首先，通过生成中间步骤，模型获得了更多的"思考空间"，这使得它能够处理更复杂的问题。其次，显式的推理链使得模型的思考过程更加透明，便于人类理解和调试。最后，CoT本质上是一种上下文学习（In-Context Learning）的扩展，它通过提供推理示例来引导模型学习正确的推理模式。

然而，CoT方法也存在一定的局限性。由于其线性的推理结构，CoT难以处理需要探索多条路径或进行回溯的复杂问题。当模型在某个推理步骤出现错误时，整个推理链可能会受到影响，导致最终结果偏离正确答案。因此，CoT更适合于那些具有明确推理路径的问题，如数学计算、逻辑推理等。

### 1.2 使用步骤详解

CoT的实际应用需要遵循一定的步骤和最佳实践。以下是使用CoT方法的详细过程：

**第一步是设计提示模板**。一个有效的CoT提示通常包含以下几个要素：问题描述、推理引导语和示例。对于推理引导语，常用的表述包括"Let's think step by step"、"首先...然后...最后..."等。这些引导语的作用是触发模型的推理模式，使其生成中间步骤而非直接给出答案。

**第二步是构建示例库**。高质量的示例对于CoT的效果至关重要。示例应该涵盖不同类型的问题，并展示完整的推理过程。每个示例都应包含：问题描述、中间推理步骤和最终答案。通过这些示例，模型能够学习到不同类型问题的推理模式。

**第三步是执行推理**。在获得模型响应后，需要解析和验证推理过程。可以通过多次采样和投票（如CoT-SC方法）来提高推理的可靠性。Self-consistency方法通过生成多个推理链并选取出现频率最高的结果来提升性能，这种方法简单而有效，能够显著提高模型在各种推理任务上的表现。

### 1.3 代码实现示例

以下是使用DeepSeek API实现CoT的Python代码示例：

```python
import requests
import json

def deepseek_cot_request(api_key, prompt, model="deepseek-chat"):
    """
    使用DeepSeek API实现Chain of Thought推理
    
    参数:
        api_key: DeepSeek API密钥
        prompt: 输入提示
        model: 使用的模型名称
    返回:
        模型生成的推理结果
    """
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # 构建包含CoT引导的提示
    cot_prompt = f"""请逐步推理以下问题，并展示你的思考过程：

{prompt}

请按照以下格式回答：
第一步：[具体推理步骤]
第二步：[具体推理步骤]
...
最终答案：[答案]
"""
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": cot_prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# 示例使用
if __name__ == "__main__":
    API_KEY = "your_api_key_here"
    
    # 数学推理示例
    problem = "小明有15个苹果，他给了小红7个，后来又买了5个，请问小明现在有多少个苹果？"
    
    result = deepseek_cot_request(API_KEY, problem)
    print("推理过程：")
    print(result['choices'][0]['message']['content'])
```

## 二、Tree of Thoughts（思维树）：探索多路径规划

### 2.1 原理深度剖析

Tree of Thoughts（ToT）方法是对CoT的重要扩展，它解决了CoT在处理需要探索和回溯的问题时的局限性。ToT的核心创新在于将推理过程建模为树状搜索结构，允许模型在每个决策点生成多个可能的"想法"（Thoughts），并对这些想法进行评估和选择。

ToT的提出基于对人类解决问题过程的深入观察。人类在面对复杂问题时，往往不会遵循单一的推理路径，而是会同时考虑多种可能性，评估每种方案的优势和风险，并在必要时进行回溯。这种思维方式在ToT中得到了形式化的建模：通过维护一棵思维树，模型能够在每个节点生成多个分支，探索不同的推理路径，并使用搜索算法来系统性地探索解空间。

与CoT的线性推理不同，ToT支持以下关键能力：

**多路径探索**：在每个推理步骤，模型可以生成多个可能的下一步行动。这对于那些存在多种解决方案的问题尤为重要。例如，在创意写作或策略规划中，ToT能够生成多种方案供选择。

**前后向探索**：模型不仅可以向前推导，还可以验证当前状态是否可能达到最终目标。这种双向推理能力使得ToT能够更有效地剪枝不可能的路径，提高搜索效率。

**系统性搜索**：ToT支持多种搜索算法，包括深度优先搜索（DFS）、广度优先搜索（BFS）和启发式搜索等。这使得ToT能够适应不同类型的任务需求。

ToT的框架包含四个核心步骤：问题分解、想法生成、状态评价和搜索算法选择。问题分解将复杂问题拆解为可管理的子问题；想法生成在每个节点产生多个候选方案；状态评价评估每个方案的前景；搜索算法选择确定如何系统地探索思维树。

### 2.2 使用步骤详解

**第一步：问题分解**

ToT的第一步是将原始问题分解为一系列思维步骤。这一步骤需要考虑问题的性质和复杂度。对于需要多步推理的问题（如数学计算），每个步骤可能对应一个独立的计算或推理子任务；对于创意类问题（如写作），每个步骤可能对应一个段落的生成。问题分解的质量直接影响后续搜索的效果。

**第二步：想法生成**

在每个思维节点，模型需要生成多个候选想法。这些想法应该是多样化的，覆盖不同的推理方向。生成想法时，可以使用特定的提示来鼓励多样性，例如："请给出三种不同的解决思路"。每个想法都是一个可能的下一步行动或中间状态。

**第三步：状态评价**

对生成的想法进行评估是ToT的关键步骤。评估可以基于以下标准：想法的可行性（是否能够实现）、想法的前景（是否有可能导向最终解）、想法的效率（是否是最优路径）等。评估可以是模型自我评估，也可以结合外部工具或规则进行验证。

**第四步：搜索算法选择**

根据任务特性选择合适的搜索算法。深度优先搜索适合那些有明确目标的问题，它沿着一条路径深入探索，直到找到解或确定此路不通。广度优先搜索则适合需要评估多种方案的问题，它系统地探索所有可能的路径。启发式搜索结合启发式函数，优先探索更有可能成功的路径。

### 2.3 代码实现示例

以下是使用DeepSeek API实现ToT的Python代码示例：

```python
import requests
import json
from typing import List, Dict, Any

class TreeOfThoughts:
    """
    Tree of Thoughts 实现类
    支持多路径探索和状态评估
    """
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    def generate_thoughts(self, state: str, num_thoughts: int = 3) -> List[str]:
        """
        生成多个候选想法
        
        参数:
            state: 当前状态/问题
            num_thoughts: 生成的候选想法数量
        返回:
            候选想法列表
        """
        prompt = f"""给定当前状态：{state}

请生成{num_thoughts}种不同的思考方向或行动方案。
每种方案应该提供不同的视角或方法。

请以列表形式输出："""
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.8,
            "max_tokens": 500
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        content = response.json()['choices'][0]['message']['content']
        
        # 解析生成的想法
        thoughts = [line.strip() for line in content.split('\n') if line.strip()]
        return thoughts
    
    def evaluate_state(self, state: str, goal: str) -> Dict[str, Any]:
        """
        评估当前状态
        
        参数:
            state: 当前状态
            goal: 目标状态
        返回:
            评估结果，包含得分和推理
        """
        prompt = f"""评估以下状态是否有可能达到目标：

当前状态：{state}

目标：{goal}

请从以下三个方面进行评估：
1. 可行性（1-10分）：这个状态是否可行？
2. 前景（1-10分）：继续沿着这个方向是否有可能达到目标？
3. 效率（1-10分）：这个方向是否高效？

最后给出综合建议：继续探索/可能需要回溯/放弃当前路径

请详细说明你的推理过程。"""
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 800
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        content = response.json()['choices'][0]['message']['content']
        
        return {"evaluation": content, "state": state}
    
    def dfs_search(self, initial_state: str, goal: str, max_depth: int = 5, 
                   num_thoughts: int = 3) -> Dict[str, Any]:
        """
        深度优先搜索实现
        
        参数:
            initial_state: 初始状态
            goal: 目标状态
            max_depth: 最大搜索深度
            num_thoughts: 每步生成的想法数量
        返回:
            搜索结果
        """
        def search(state: str, depth: int, path: List[str]) -> Dict[str, Any]:
            # 检查是否达到目标
            if depth >= max_depth:
                return {"status": "max_depth_reached", "path": path, "final_state": state}
            
            # 评估当前状态
            eval_result = self.evaluate_state(state, goal)
            
            # 如果评估建议放弃，返回当前结果
            if "放弃" in eval_result["evaluation"]:
                return {"status": "abandoned", "path": path, "evaluation": eval_result}
            
            # 生成多个想法
            thoughts = self.generate_thoughts(state, num_thoughts)
            
            # 递归搜索每个想法
            for thought in thoughts:
                new_path = path + [thought]
                new_state = state + " -> " + thought
                
                result = search(new_state, depth + 1, new_path)
                if result["status"] == "goal_reached":
                    return result
            
            return {"status": "explored", "best_path": path}
        
        return search(initial_state, 0, [initial_state])

# 示例使用
if __name__ == "__main__":
    tot = TreeOfThoughts(api_key="your_api_key_here")
    
    # 示例：解决"算24点"游戏
    initial_state = "数字：[3, 3, 8, 8]，目标：24"
    goal = "计算出结果为24"
    
    result = tot.dfs_search(initial_state, goal, max_depth=3, num_thoughts=3)
    print("搜索结果：")
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 三、Graph of Thoughts（思维图）：网状推理的进化

### 3.1 原理深度剖析

Graph of Thoughts（GoT）是在ToT基础上的进一步发展，它将LLM生成的信息建模为任意图结构，其中信息单位（"LLM thoughts"）是顶点，边对应于这些顶点之间的依赖关系。GoT的核心优势在于其能够建模比树更通用的图结构，从而支持更复杂的推理模式，如合并、分支和反馈循环。

人类思维过程实际上是极其复杂的网络结构，而非简单的线性链条或树状结构。我们在思考时，会建立各种联系、进行类比、整合来自不同来源的信息。GoT正是试图捕捉这种人脑思维的网状特性。

与ToT相比，GoT的主要优势包括：

**任意图结构**：GoT允许每个推理步骤有多于一条入边，这意味着可以支持链路的合并。在实际应用中，一个复杂的推理过程可能需要整合多个子问题的解，GoT能够自然地建模这种依赖关系。

**反馈循环**：GoT支持使用反馈循环来增强推理。这意味着模型可以回顾之前的结果，修正错误，并进一步优化推理过程。这种能力在处理需要迭代改进的任务时尤为重要。

**思想组合**：GoT能够将任意的LLM思想组合成协同结果。模型可以提炼整个思想网络的本质，从多个相关的想法中提取共同模式，形成更高级别的推理。

GoT框架还引入了"思想体积"（Volume of a Thought）的概念，这是一个可用于评估提示策略的指标。对于给定的思想v，其体积是LLM思想的数量，即有多少条有向边可以到达v。这个概念帮助我们理解和量化推理过程的复杂度。

### 3.2 使用步骤详解

**第一步：建模问题为图结构**

GoT应用的第一步是将问题建模为图 of Operations（GoO）。这需要分析问题的结构，确定：有哪些需要生成的中间思想？这些思想之间存在怎样的依赖关系？是否需要合并操作或反馈循环？

**第二步：图操作定义**

GoT支持多种图操作，包括：

- **生成（Generate）**：产生新的思想节点
- **合并（Merge）**：将多个思想节点合并为一个
- **提炼（Distill）**：从一组思想中提取共同本质形成新思想
- **反馈（Feedback）**：使用前面思想的结果来改进后续思想

**第三步：图遍历与评估**

根据问题的性质，选择合适的图遍历策略。这可以是深度优先、广度优先或基于启发式的遍历。在遍历过程中，持续评估每个思想节点的质量和前景。

**第四步：结果提取**

从最终的图结构中提取答案。这可能涉及追踪从根节点到目标节点的路径，或从多个相关节点综合得出结论。

### 3.3 代码实现示例

以下是使用DeepSeek API实现GoT的Python代码示例：

```python
import requests
import json
from typing import List, Dict, Any, Set
from collections import defaultdict

class GraphOfThoughts:
    """
    Graph of Thoughts 实现类
    支持网状推理结构和反馈循环
    """
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 图结构：节点 -> [依赖节点列表]
        self.graph: Dict[str, List[str]] = defaultdict(list)
        # 节点内容
        self.nodes: Dict[str, str] = {}
    
    def add_node(self, node_id: str, content: str, dependencies: List[str] = None):
        """
        添加图节点
        
        参数:
            node_id: 节点唯一标识
            content: 节点内容/思想
            dependencies: 依赖的节点ID列表
        """
        self.nodes[node_id] = content
        if dependencies:
            for dep in dependencies:
                self.graph[node_id].append(dep)
    
    def generate_node(self, prompt: str, context: str = "") -> str:
        """
        生成新思想
        
        参数:
            prompt: 生成提示
            context: 上下文信息
        返回:
            生成的思想内容
        """
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": full_prompt}],
            "temperature": 0.7,
            "max_tokens": 600
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        return response.json()['choices'][0]['message']['content']
    
    def merge_nodes(self, node_ids: List[str], merge_prompt: str = None) -> str:
        """
        合并多个节点的思想
        
        参数:
            node_ids: 要合并的节点ID列表
            merge_prompt: 合并提示
        返回:
            合并后的思想
        """
        # 收集所有依赖节点的内容
        contexts = []
        for node_id in node_ids:
            if node_id in self.nodes:
                contexts.append(f"思想{node_id}：{self.nodes[node_id]}")
        
        context_str = "\n".join(contexts)
        
        if merge_prompt is None:
            merge_prompt = """请分析并整合以下思想，提炼出共同的本质和关键洞察。

整合后的思想应该：
1. 包含所有输入思想的核心要点
2. 建立思想之间的联系
3. 形成统一、连贯的结论"""
        
        return self.generate_node(f"{merge_prompt}\n\n{context_str}", "")
    
    def feedback_enhance(self, node_id: str, feedback_prompt: str = None) -> str:
        """
        使用反馈增强思想
        
        参数:
            node_id: 要增强的节点ID
            feedback_prompt: 反馈提示
        返回:
            增强后的思想
        """
        if node_id not in self.nodes:
            return ""
        
        if feedback_prompt is None:
            feedback_prompt = """请审视这个思想，识别可能的错误或改进空间。
同时考虑如何整合来自其他相关思想的反馈。

改进后的思想应该："""

        return self.generate_node(
            f"当前思想：{self.nodes[node_id]}\n\n{feedback_prompt}",
            ""
        )
    
    def get_execution_order(self) -> List[str]:
        """
        获取图的执行顺序（拓扑排序）
        
        返回:
            节点ID列表，按照依赖顺序排列
        """
        # 计算入度
        in_degree = defaultdict(int)
        for node in self.nodes:
            in_degree[node] = len(self.graph[node])
        
        # BFS拓扑排序
        queue = [n for n in self.nodes if in_degree[n] == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            # 减少依赖该节点的节点的入度
            for n in self.nodes:
                if node in self.graph[n]:
                    in_degree[n] -= 1
                    if in_degree[n] == 0:
                        queue.append(n)
        
        return result
    
    def execute(self) -> Dict[str, Any]:
        """
        执行图中的所有操作
        
        返回:
            执行结果
        """
        execution_order = self.get_execution_order()
        results = {}
        
        for node_id in execution_order:
            deps = self.graph[node_id]
            
            if not deps:
                # 根节点，生成思想
                results[node_id] = self.nodes[node_id]
            else:
                # 有依赖，先合并依赖节点
                merged = self.merge_nodes(deps)
                # 生成当前节点思想
                self.nodes[node_id] = self.generate_node(
                    self.nodes[node_id],
                    context=merged
                )
                results[node_id] = self.nodes[node_id]
        
        return {
            "execution_order": execution_order,
            "results": results,
            "final_result": results.get(execution_order[-1], "") if execution_order else ""
        }

# 示例使用
if __name__ == "__main__":
    got = GraphOfThoughts(api_key="your_api_key_here")
    
    # 构建一个复杂的推理图
    # 节点1：分析问题
    got.add_node("analyze", "请分析这个商业问题的关键要素：某公司想要开拓新市场")
    
    # 节点2：市场调研（依赖节点1）
    got.add_node("research", "基于上述分析，进行市场调研", dependencies=["analyze"])
    
    # 节点3：竞争分析（依赖节点1）
    got.add_node("competition", "基于上述分析，进行竞争分析", dependencies=["analyze"])
    
    # 节点4：综合策略（依赖节点2和3）
    got.add_node("strategy", "整合市场调研和竞争分析结果，制定市场进入策略", 
                 dependencies=["research", "competition"])
    
    # 执行图
    result = got.execute()
    
    print("执行顺序：", result["execution_order"])
    print("\n最终策略：")
    print(result["final_result"])
```

## 四、其他主流规划方法

### 4.1 ReAct：推理与行动的协同

ReAct（Reasoning and Acting）是一种将推理和行动集成到LLM中的范式。与CoT仅关注推理过程不同，ReAct同时考虑行动的执行和观察结果的利用。在ReAct范式中，LLM交替生成推理轨迹和任务动作，这种模式使得模型能够与外部环境（如API、工具）进行交互，同时保持推理的连贯性。

ReAct的核心思想可以概括为"思考-行动-观察"的循环：模型首先分析当前状态并决定下一步行动（Thought），然后执行该行动（Action），接着获取环境反馈（Observation），最后基于反馈进行下一轮推理。这个循环持续进行，直到模型认为可以给出最终答案。

ReAct的优势在于它将LLM的推理能力与外部工具的执行能力结合起来，使模型能够处理需要与环境交互的复杂任务。例如，在构建问答系统时，模型可能需要调用搜索API获取最新信息，然后基于搜索结果进行进一步推理。

### 4.2 Reflexion：基于语言反馈的自我改进

Reflexion是一种将试错学习转化为基于自然语言反馈的方法。传统的强化学习方法需要大量的训练样本和昂贵的模型微调，而Reflexion通过语言反馈来实现学习，避免了权重更新的高成本。

Reflexion框架引入了一个关键组件：episodic memory（情景记忆）。这个记忆模块存储了Agent在执行任务过程中的关键决策和结果，使Agent能够回顾并分析过去的行为。当Agent遇到失败时，它可以查询记忆模块，分析失败原因，并生成改进策略。

与ReAct相比，Reflexion的改进主要体现在：它不仅执行动作，还能够反思动作的结果，并将反思结果存储在记忆中供后续决策参考。这种能力使Reflexion在需要长期规划的任务中表现更为出色。

### 4.3 Plan-and-Execute：先规划后执行

Plan-and-Execute模式是一种将规划与执行分离的架构。在这种模式中，一个专门的规划器（通常是LLM）负责生成多步计划，而执行器则负责调用工具完成各个子任务。

这种分离设计的优势在于：规划器可以专注于整体策略的制定，不被具体的执行细节所干扰；执行器则可以高效地执行具体操作，不需要理解完整的任务上下文。Plan-and-Execute模式特别适合于那些需要详细规划的任务，如复杂的项目管理、多步骤的问题解决等。

然而，这种模式也有局限性：它缺乏执行过程中的灵活性，当环境发生变化时，可能无法及时调整计划。因此，一些改进方法引入了" replanning"机制，允许在执行过程中根据观察到的结果重新生成计划。

### 4.4 LLM-Modulo：外部验证的规划框架

LLM-Modulo框架将规划任务外包给外部工具，同时利用LLM的推理能力来生成候选方案。在这种架构中，LLM负责生成计划的内容，而外部的验证器（如形式化验证工具、模拟器等）负责检查计划的正确性和可行性。

这种设计有效地解决了LLM在规划任务中可能出现"幻觉"的问题。通过引入外部验证，LLM生成的计划能够得到客观的检验和评估，从而提高规划的可靠性。LLM-Modulo框架特别适合于那些有明确验证标准的任务，如路径规划、时间调度等。

## 五、方法对比与选择指南

### 5.1 各方法特性对比

不同的规划方法适用于不同的场景和任务类型。以下是主要方法的核心特性对比：

| 方法 | 推理结构 | 回溯能力 | 适用场景 | 计算成本 |
|------|----------|----------|----------|----------|
| CoT | 线性链 | 无 | 简单推理任务 | 低 |
| ToT | 树状 | 有限 | 多路径探索 | 中等 |
| GoT | 网状图 | 完全支持 | 复杂推理与整合 | 较高 |
| ReAct | 循环链 | 支持 | 环境交互任务 | 中等 |
| Reflexion | 循环链+记忆 | 完全支持 | 长期任务学习 | 中等 |
| Plan-and-Execute | 分离式 | 需重规划 | 复杂多步骤任务 | 取决于规划器 |

### 5.2 选择建议

选择合适的规划方法需要考虑多个因素：

**任务复杂度**：对于简单的单步或多步推理任务，CoT通常是足够且高效的选择。当任务需要探索多个解决方案或进行复杂的决策时，ToT或GoT更为适合。

**是否需要环境交互**：如果任务需要与外部环境进行交互（如调用API、访问数据库），ReAct模式是更好的选择，因为它明确地建模了行动-观察的循环。

**任务的时间跨度**：对于需要跨长时间执行的任务，Reflexion的记忆机制可以帮助Agent积累经验并持续改进。对于一次性完成的任务，Plan-and-Execute可能更为简洁高效。

**计算资源限制**：不同的方法有不同的计算成本。CoT的计算成本最低，而GoT由于需要维护图结构和进行更复杂的操作，成本相对较高。在资源有限的场景下，应优先考虑更轻量级的方法。

## 六、完整代码示例：多方法对比实现

以下代码展示了如何使用DeepSeek API实现多种规划方法的对比：

```python
import requests
import json
import time
from typing import Dict, List, Any, Callable
from abc import ABC, abstractmethod

# ==================== 基础接口定义 ====================

class PlanningMethod(ABC):
    """规划方法抽象基类"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.url = "https://api.deepseek.com/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    
    @abstractmethod
    def solve(self, problem: str) -> Dict[str, Any]:
        """解决问题并返回结果"""
        pass
    
    def call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """调用LLM API"""
        data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": 1000
        }
        
        response = requests.post(self.url, headers=self.headers, json=data)
        return response.json()['choices'][0]['message']['content']

# ==================== Chain of Thought 实现 ====================

class ChainOfThought(PlanningMethod):
    """思维链方法"""
    
    def solve(self, problem: str) -> Dict[str, Any]:
        start_time = time.time()
        
        prompt = f"""请逐步推理以下问题：

{problem}

要求：
1. 展示完整的推理过程
2. 每一步都要有清晰的逻辑依据
3. 最终给出明确答案

推理过程："""
        
        reasoning = self.call_llm(prompt)
        
        # 提取最终答案
        answer_prompt = f"""基于以下推理过程，总结最终答案：

{reasoning}

最终答案："""
        
        final_answer = self.call_llm(answer_prompt, temperature=0.3)
        
        return {
            "method": "Chain of Thought",
            "problem": problem,
            "reasoning": reasoning,
            "final_answer": final_answer,
            "time_taken": time.time() - start_time
        }

# ==================== Tree of Thoughts 实现 ====================

class TreeOfThoughts(PlanningMethod):
    """思维树方法"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", max_depth: int = 3, 
                 num_branches: int = 3):
        super().__init__(api_key, model)
        self.max_depth = max_depth
        self.num_branches = num_branches
    
    def solve(self, problem: str) -> Dict[str, Any]:
        start_time = time.time()
        
        # 初始化思维树
        tree = {
            "nodes": [],
            "edges": [],
            "current_path": []
        }
        
        def explore(state: str, depth: int) -> str:
            if depth >= self.max_depth:
                return state
            
            # 生成多个分支
            branch_prompt = f"""针对以下状态，生成{self.num_branches}种不同的思考方向：

当前状态：{state}

请列出{self.num_branches}种可能的下一步思考或行动："""
            
            branches_text = self.call_llm(branch_prompt, temperature=0.9)
            branches = [b.strip() for b in branches_text.split('\n') if b.strip()]
            
            # 评估并选择最佳分支
            best_branch = None
            best_score = -1
            
            for branch in branches[:self.num_branches]:
                eval_prompt = f"""评估以下思考方向的质量和前景：

{branch}

请从以下方面评分（1-10分）：
1. 创新性
2. 可行性
3. 与目标的相关性

并说明理由。"""
                
                eval_result = self.call_llm(eval_prompt, temperature=0.3)
                
                # 简单解析评分（实际应用中应更 robust）
                score = 7  # 默认分数
                if "8" in eval_result or "9" in eval_result or "10" in eval_result:
                    score = 8
                elif "4" in eval_result or "5" in eval_result or "6" in eval_result:
                    score = 5
                
                if score > best_score:
                    best_score = score
                    best_branch = branch
            
            if best_branch:
                new_state = state + " -> " + best_branch
                return explore(new_state, depth + 1)
            
            return state
        
        final_state = explore(problem, 0)
        
        # 提取最终答案
        answer_prompt = f"""基于以下思维树的探索结果，给出最终答案：

{final_state}

最终答案："""
        
        final_answer = self.call_llm(answer_prompt, temperature=0.3)
        
        return {
            "method": "Tree of Thoughts",
            "problem": problem,
            "exploration_tree": final_state,
            "final_answer": final_answer,
            "time_taken": time.time() - start_time
        }

# ==================== ReAct 实现 ====================

class ReAct(PlanningMethod):
    """ReAct方法：推理与行动协同"""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat", max_iterations: int = 5):
        super().__init__(api_key, model)
        self.max_iterations = max_iterations
    
    def solve(self, problem: str) -> Dict[str, Any]:
        start_time = time.time()
        
        trajectory = []
        current_state = problem
        observation = ""
        
        for i in range(self.max_iterations):
            # Thought阶段
            thought_prompt = f"""问题：{problem}

当前状态：{current_state}
历史观察：{observation}

请分析：
1. 当前状态是什么？
2. 下一步应该做什么？
3. 需要什么信息来解决问题？

思考："""
            
            thought = self.call_llm(thought_prompt, temperature=0.7)
            
            # Action阶段
            action_prompt = f"""基于以下思考，决定下一步行动：

思考：{thought}

可选行动：
1. 继续推理 - 进一步分析问题
2. 获取信息 - 请求补充信息
3. 给出答案 - 认为已有足够信息给出答案

请选择一个行动并说明理由。"""
            
            action = self.call_llm(action_prompt, temperature=0.5)
            
            trajectory.append({
                "step": i + 1,
                "thought": thought,
                "action": action
            })
            
            # 检查是否应该给出答案
            if "给出答案" in action or "final" in action.lower():
                break
            
            # Observation阶段（这里简化为自我反思）
            observation_prompt = f"""基于之前的思考和行动，分析：

行动：{action}

这个行动的结果是什么？有什么发现？"""
            
            observation = self.call_llm(observation_prompt, temperature=0.5)
            current_state = current_state + f"\n[Step {i+1}] " + observation
        
        # 最终答案
        final_prompt = f"""基于以下推理轨迹，给出最终答案：

{json.dumps(trajectory, ensure_ascii=False, indent=2)}

最终答案："""
        
        final_answer = self.call_llm(final_prompt, temperature=0.3)
        
        return {
            "method": "ReAct",
            "problem": problem,
            "trajectory": trajectory,
            "final_answer": final_answer,
            "time_taken": time.time() - start_time
        }

# ==================== 主程序：方法对比 ====================

def compare_methods(api_key: str, problem: str):
    """
    对比多种规划方法的效果
    
    参数:
        api_key: DeepSeek API密钥
        problem: 测试问题
    """
    methods = [
        ChainOfThought(api_key),
        TreeOfThoughts(api_key, max_depth=2, num_branches=2),
        ReAct(api_key, max_iterations=3)
    ]
    
    results = []
    
    for method in methods:
        print(f"\n{'='*50}")
        print(f"测试方法：{method.__class__.__name__}")
        print(f"{'='*50}")
        
        try:
            result = method.solve(problem)
            results.append(result)
            
            print(f"\n问题：{problem}")
            print(f"\n推理结果：")
            print(result.get('reasoning', result.get('trajectory', 'N/A')))
            print(f"\n最终答案：{result.get('final_answer', 'N/A')}")
            print(f"\n耗时：{result.get('time_taken', 0):.2f}秒")
            
        except Exception as e:
            print(f"方法执行失败：{str(e)}")
            results.append({
                "method": method.__class__.__name__,
                "error": str(e)
            })
    
    return results

# 示例使用
if __name__ == "__main__":
    API_KEY = "your_api_key_here"
    
    # 测试问题
    test_problem = """小张计划在暑假期间用7天时间游览中国三个城市：北京、上海和广州。
    他需要从北京出发，最终回到北京。每个城市至少停留1天。
    请帮他规划一个合理的行程，使得总交通费用最低。

    已知各地之间的机票价格：
    北京-上海：800元
    北京-广州：1200元
    上海-广州：600元
    广州-北京：1100元
    上海-北京：850元（不同航空公司）
    广州-上海：650元（不同航空公司）

    请给出具体的行程安排和总费用。"""
    
    results = compare_methods(API_KEY, test_problem)
    
    # 保存结果
    with open("planning_comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print("\n\n结果已保存到 planning_comparison_results.json")
```

## 总结

本文系统性地介绍了当前主流的LLM规划方法，从最基本的Chain of Thought到更为复杂的Tree of Thoughts和Graph of Thoughts，再到ReAct、Reflexion等Agent范式。这些方法代表了人工智能领域在赋予大语言模型规划能力方面的不同探索路径和技术创新。

**Chain of Thought**通过引导模型生成显式的推理步骤，增强了模型处理复杂推理任务的能力，是后续各种方法的基础。其简单有效，适合于具有明确推理路径的问题。

**Tree of Thoughts**将推理过程扩展为树状结构，支持多路径探索和回溯，适合需要考虑多种方案的任务。其关键创新在于系统性地探索推理空间。

**Graph of Thoughts**进一步将推理建模为任意图结构，能够捕捉更复杂的思想关系和依赖，支持合并、分支和反馈循环，更接近人类思维的自然形态。

**ReAct**、**Reflexion**和**Plan-and-Execute**等方法则从Agent的角度出发，强调推理与行动、环境的交互，以及通过记忆和反馈实现持续改进的能力。

在实际应用中，选择哪种方法需要根据具体任务的特点、可用资源和性能要求来综合考虑。随着技术的不断发展，我们期待出现更多创新的规划方法，进一步提升LLM在复杂任务中的表现。