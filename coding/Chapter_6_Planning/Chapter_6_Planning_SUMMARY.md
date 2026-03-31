# 规划模式

## 模式概述

规划模式是智能体系统中将复杂目标分解为可管理步骤的核心计算过程。当用户请求一个无法通过单一行动解决的复杂任务时，规划模式允许智能体系统首先创建一个连贯的计划，然后系统性地执行该计划。这种模式从简单的反应性智能体转变为战略性、目标导向的执行者，能够主动朝着复杂目标努力。

### 核心思想

规划模式的核心在于将高层目标转换为一系列离散的可执行步骤。智能体不需要预先知道所有步骤，而是根据当前状态、约束条件和目标，动态生成最优的行动序列。这种适应性使得智能体能够处理动态环境中的复杂任务，并在遇到障碍时重新评估和调整计划。

### 适用场景

规划模式特别适用于以下场景：
- 需要多步处理的复杂任务
- 工作流自动化和编排
- 竞争分析和市场研究
- 深度文献综述
- 跨系统的依赖管理
- 需要整合多个工具或数据源的任务

## 核心组件

### 规划智能体 (Planning Agent)

规划智能体是规划模式的核心组件，负责：
- 分析用户的复杂目标
- 识别初始状态和目标状态
- 生成详细的执行计划
- 监控执行过程并在必要时调整计划

### 执行计划 (Execution Plan)

执行计划包含以下要素：
- **目标描述**: 清晰陈述要达成的目标
- **执行步骤**: 按顺序排列的可操作步骤
- **依赖关系**: 步骤之间的依赖和约束
- **工具需求**: 每个步骤需要的工具或资源
- **复杂度评估**: 对整体任务复杂度的判断

### 工具集成

规划模式通常需要与各种工具集成：
- 搜索工具：获取信息
- 计算工具：数据分析和处理
- 写作工具：内容生成
- 代码执行工具：动态计算和验证

## 实现方式

### 1. 基于 CrewAI 的规划模式

CrewAI 框架提供了一个简洁的方式来实现规划模式。通过定义具有明确角色的智能体和结构化的任务，CrewAI 能够自动处理规划和执行流程。

#### 代码实现

```python
"""
1-crewai-planning.py

基于 CrewAI 的规划模式实现
"""
import os
import sys
from pathlib import Path

# 添加父目录到路径，以便导入 llm_config
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from llm_config import get_default_llm_config

from crewai importation Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

## 1. 初始化 LLM 配置
llm_config = get_default_llm_config()
llm = llm_config.create_llm()

## 2. 定义规划智能体
planner_writer_agent = Agent(
    role='文章规划者和撰写者',
    goal='规划然后撰写关于指定主题的简洁、引人入胜的摘要。',
    backstory=(
        '你是一位专业的技术作家和内容策略师。'
        '你的优势在于在写作之前创建清晰、可操作的计划，'
        '确保最终摘要既信息丰富又易于理解。'
    ),
    verbose=True,
    allow_delegation=False,
    llm=llm
)

## 3. 定义规划任务
topic = "强化学习在 AI 中的重要性"
planning_task = Task(
    description=(
        f"1. 为主题'{topic}'的摘要创建要点计划。\n"
        f"2. 根据您的计划撰写摘要，保持在 200 字左右。"
    ),
    expected_output=(
        "包含两个不同部分的最终报告：\n\n"
        "### 计划\n"
        "- 概述摘要要点的项目符号列表。\n\n"
        "### 摘要\n"
        "- 主题的简洁且结构良好的摘要。"
    ),
    agent=planner_writer_agent,
)

## 4. 创建并执行团队
crew = Crew(
    agents=[planner_writer_agent],
    tasks=[planning_task],
    process=Process.sequential,
)

## 5. 执行任务
result = crew.kick.koff()
print(result)
```

#### 关键特性

- **角色定义**: 明确智能体的角色和职责
- **任务结构化**: 任务的描述和预期输出都被明确定义
- **顺序处理**: 使用 `Process.sequential` 确保按顺序执行
- **自动规划**: CrewAI 框架自动处理规划逻辑

### 2. 自定义规划智能体

对于更复杂的需求，可以实现自定义的规划智能体，提供更大的灵活性和控制力。

#### 代码实现

```python
"""
2-simple-planning-agent.py

简单的规划智能体实现
"""
import os
import sys
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

# 添加父目录到路径
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from llm_config import get_default_llm_config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

## 1. 初始化 LLM 配置
llm_config = get_default_llm_config()
llm = llm_config.create_llm()

## 2. 定义数据模型
@dataclass
class PlanningStep:
    """规划步骤"""
    step_number: int
    description: str
    tool_needed: str = None
    dependencies: List[int] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

@dataclass
class ExecutionPlan:
    """执行计划"""
    goal: str
    steps: List[PlanningStep]
    estimated_complexity: str

## 3. 规划智能体类
class PlanningAgent:
    """规划智能体"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def create_plan(self, goal: str, context: str = "") -> ExecutionPlan:
        """创建执行计划"""
        planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的规划助手。你的任务是将复杂目标分解为清晰的执行步骤。

请分析给定的目标，并提供一个结构化的计划。
计划应该包括：
1. 明确的目标重述
2. 按顺序排列的执行步骤
3. 每个步骤可能需要的工具
4. 步骤之间的依赖关系
5. 整体复杂度评估

请以结构化的格式回答，便于解析。"""),
            ("user", """目标：{goal}
上下文：{context}
请创建一个详细的执行计划。""")
        ])

        # 使用 LLM 生成计划
        chain = planning_prompt | self.llm
        response = chain.invoke({"goal": goal, "context": context})
        plan_text = response.content

        # 解析生成的计划
        return self._parse_plan(goal, plan_text)

    def _parse_plan(self, goal: str, plan_text: str) -> ExecutionPlan:
        """解析计划文本（简化实现）"""
        steps = []
        lines = plan_text.split('\n')

        step_num = 1
        for i, line in enumerate(lines):
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '4.', '5.'))):
                # 提取步骤描述
                description = line.lstrip('0123456789.- ').strip()

                # 检查是否提到工具
                tool_needed = None
                if '搜索' in description or '查找' in description:
                    tool_needed = 'search'
                elif '分析' in description or '计算' in description:
                    tool_needed = 'analysis'
                elif '报告' in description or '生成' in description:
                    tool_needed = 'report_generation'

                steps.append(PlanningStep(
                    step_number=step_num,
                    description=description,
                    tool_needed=tool_needed
                ))
                step_num += 1

        # 评估复杂度
        complexity = "低"
        if len(steps) > 3:
            complexity = "中"
        if len(steps) > 5:
            complexity = "高"

        return ExecutionPlan(
            goal=goal,
            steps=steps,
            estimated_complexity=complexity
        )

    def execute_plan(self, plan: ExecutionPlan) -> Dict[str, any]:
        """执行计划（模拟执行）"""
        results = {}

        for step in plan.steps:
            print(f"步骤 {step.step_number}: {step.description}")
            if step.tool_needed:
                print(f"  需要工具：{step.tool_needed}")

            # 模拟执行结果
            results[f"step_{step.step_number}"] = {
                "description": step.description,
                "status": "completed",
                "tool_used": step.tool_needed
            }

        return {
            "goal": plan.goal,
            "status": "completed",
            "steps_completed": len(plan.steps),
            "results": results
        }
```

#### 关键特性

- **数据模型**: 使用 `dataclass` 定义清晰的数据结构
- **计划解析**: 智能解析 LLM 生成的计划文本
- **复杂度评估**: 自动评估任务复杂度
- **工具识别**: 根据步骤描述识别需要的工具

### 3. Deep Research 模式

Deep Research 模式是规划模式的复杂应用，模拟像 Google Deep Research 和 OpenAI Deep Research 这样的系统。

#### 代码实现

```python
"""
3-research-planning-agent.py

研究型规划智能体实现
模拟 Deep Research 模式的多步规划和执行
"""
import os
import sys
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime
import time

# 添加父目录到路径
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from llm_config import get_default_llm_config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

## 1. 初始化 LLM 配置
llm_config = get_default_llm_config()
llm = llm_config.create_llm()

## 2. 定义数据模型
@dataclass
class ResearchQuery:
    """研究查询"""
    query_id: int
    query_text: str
    search_terms: List[str]
    status: str = "pending"
    results: List[Dict] = None

    def __post_init__(self):
        if self.results is None:
            self.results = []

@dataclass
class ResearchPlan:
    """研究计划"""
    research_topic: str
    queries: List[ResearchQuery]
    created_at: datetime = None
    status: str = "planned"

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

## 3. Deep Research 智能体类
class DeepResearchAgent:
    """Deep Research 智能体"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.search_tool = Tool(
            name="web_search",
            func=self.mock_search,
            description="搜索网络信息，返回相关文档和资源"
        )

    def create_research_plan(self, topic: str, num_queries: int = 3) -> ResearchPlan:
        """创建研究计划"""
        planning_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的研究规划师。你的任务是创建一个全面的研究计划。

对于给定的研究主题，你需要：
1. 识别关键的研究方向和子主题
2. 生成具体可执行的搜索查询
3. 确保查询覆盖主题的各个方面
4. 避免重复，确保每个查询都能带来独特价值

请输出 {num_queries} 个独特的搜索查询，每个查询应该：
- 具体明确
- 针对主题的不同方面
- 使用合适的搜索术语"""),
            ("user", """研究主题：{topic}
请创建包含 {num_queries} 个搜索查询的研究计划。
输出格式：每个查询占一行，以编号开头。""")
        ])

        chain = planning_prompt | self.llm
        response = chain.invoke({"topic": topic, "num_queries": num_queries})
        plan_text = response.content

        # 解析生成的查询
        queries = self._parse_queries(plan_text)

        return ResearchPlan(
            research_topic=topic,
            queries=queries,
            status="planned"
        )

    def execute_research_plan(self, plan: Research) -> Dict[str, any]:
        """执行研究计划"""
        start_time = time.time()

        # 执行每个查询
        for i, query in enumerate(plan.queries):
            print(f"查询 {i+1}/{len(plan.queries)}: {query.query_text}")

            # 执行搜索
            search_results = self.search_tool.func(query.query_text)

            query.results = search_results
            query.status = "completed"

        # 综合结果
        summary = self._synthesize_results(plan)

        execution_time = time.time() - start_time

        return {
            "topic": plan.research_topic,
            "summary": summary,
            "execution_time": execution_time,
            "queries_completed": len(plan.queries)
        }

    def mock_search(self, query: str) -> List[Dict]:
        """模拟网络搜索工具"""
        mock_results = [
            {
                "title": f"关于 {query} 的研究论文",
                "url": f"https://example.com/papers/{hash(query) % 1000}",
                "snippet": f"这是一篇关于 {query} 的权威研究...",
                "relevance_score": 0.9
            },
            {
                "title": f"{query} 最新进展",
                "url": f"https://example.com/news/{hash(query) % 1000}",
                "snippet": f"最新研究表明 {query} 有重要的突破...",
                "relevance_score": 0.85
            }
        ]
        return mock_results
```

#### 关键特性

- **多步规划**: 生成多个搜索查询
- **动态查询**: 根据主题动态生成搜索术语
- **结果综合**: 将多个搜索结果整合为连贯报告
- **引用管理**: 跟踪所有使用的来源

## 流程图

以下是规划模式的典型执行流程：

```mermaid
graph TD
    A[用户输入复杂目标] --> B[规划智能体接收请求]
    B --> C{分析目标复杂度}
    C -->|简单目标| D[直接执行]
    C -->|复杂目标| E[创建执行计划]
    E --> F[分解为多个步骤]
    F --> G[识别依赖关系]
    G --> H[确定工具需求]
    H --> I[生成结构化计划]
    I --> J[用户审阅计划]
    J --> K{批准计划?}
    K -->|否|修改| L[修改计划]
    L --> E
    K -->|是| M[按顺序执行步骤]
    M --> N{步骤完成?}
    N -->|否| O[继续执行]
    O --> N
    N -->|是| P[综合结果]
    P --> Q[生成最终报告]
    Q --> R[返回给用户]

    style A fill:#e1f5ff
    style R fill:#e1f5ff
    style E fill:#fff4e1
    style M fill:#e8f5e9
    style Q fill:#fce4ec
```

## 使用场景总结

### 1. 内容创作和写作

- **场景**: 需要为复杂主题撰写结构化文章或报告
- **优势**: 先规划结构确保内容逻辑连贯
- **示例**: 技术文档撰写、研究报告生成、营销内容创作

### 2. 深度研究

- **场景**: 需要从多个来源收集和综合信息
- **优势**: 系统化搜索、避免遗漏、确保全面性
- **示例**: 竞争分析、市场调研、文献综述、技术调研

### 3. 工作流自动化

- **场景**: 需要协调多个步骤和系统的复杂业务流程
- **优势**: 明确步骤、管理依赖、处理异常
- **示例**: 员工入职、项目启动、流程审批

### 4. 问题解决

- **场景**: 需要系统分析并解决复杂问题
- **优势**: 结构化分析、逐步验证、可追溯
- **示例**: 故障诊断、根因分析、决策支持

### 5. 跨系统集成

- **场景**: 需要与多个外部系统交互
- **优势**: 统一接口、错误处理、数据转换
- **示例**: 数据同步、API集成、第三方服务调用

## 最佳实践

### 1. 计划可视化

- 向用户展示计划以获得反馈
- 提供计划的清晰视图和进度追踪
- 允许用户在执行前修改计划

### 2. 灵活执行

- 支持动态调整计划
- 处理执行过程中的异常和失败
- 提供重试和回退机制

### 3. 透明度

- 记录每个步骤的执行状态
- 保存中间结果和日志
- 提供详细的执行报告

### 4. 工具管理

- 明确定义每个工具的输入输出
- 验证工具调用的参数
- 处理工具调用失败的情况

### 5. 成本控制

- 估算计划的资源消耗
- 限制并行执行的数量
- 提供执行预算控制

## 结论

规划模式是将智能体从简单的反应性响应者提升为战略性、目标导向的执行者的基础组件。通过将复杂目标分解为可管理的步骤，规划模式使智能体系统能够处理人类级别的复杂任务。

现代大型语言模型为此提供了核心能力，自主地将高级目标分解为连贯的可操作步骤。从简单的顺序任务执行（如 CrewAI 智能体）到复杂的动态研究系统（如 Deep Research），规划模式展示了其在各种应用场景中的强大能力。

关键要点：
- 规划使智能体将复杂目标分解为可操作的顺序步骤
- 它对于处理多步任务、工作流自动化和导航复杂环境至关重要
- LLM 可以通过基于任务描述生成逐步方法来执行规划
- 明确提示或设计任务以要求规划步骤会在智能体框架中鼓励这种行为
- Google Deep Research 是规划模式的高级应用代表

通过构建问题解决方法，规划模式为复杂问题的人类意图和自动化执行之间提供了必要的桥梁，使智能体能够管理工作流并提供全面的综合结果。
