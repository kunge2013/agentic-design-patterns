from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

GEMINI_MODEL = "gemini-2.0-flash"

## --- 1. 定义研究员子智能体（并行运行）---
## 研究员 1：可再生能源
researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=GEMINI_MODEL,
    instruction="""你是一名专门研究能源的 AI 研究助理。研究"可再生能源"的最新进展。使用提供的 Google 搜索工具。简洁地总结你的主要发现（1-2 句话）。*只*输出摘要。""",
    description="研究可再生能源。",
    tools=[google_search],
    # 将结果存储在状态中供合并智能体使用
    output_key="renewable_energy_result"
)

## 研究员 2：电动汽车
researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=GEMINI_MODEL,
    instruction="""你是一名专门研究交通的 AI 研究助理。研究"电动汽车技术"的最新发展。使用提供的 Google 搜索工具。简洁地总结你的主要发现（1-2 句话）。*只*输出摘要。""",
    description="研究电动汽车技术。",
    tools=[google_search],
    # 将结果存储在状态中供合并智能体使用
    output_key="ev_technology_result"
)

## 研究员 3：碳捕获
researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=GEMINI_MODEL,
    instruction="""你是一名专门研究气候解决方案的 AI 研究助理。研究"碳捕获方法"的当前状态。使用提供的 Google 搜索工具。简洁地总结你的主要发现（1-2 句话）。*只*输出摘要。""",
    description="研究碳捕获方法。",
    tools=[google_search],
    # 将结果存储在状态中供合并智能体使用
    output_key="carbon_capture_result"
)

## --- 2. 创建 ParallelAgent（并发运行研究员）---
## 此智能体协调研究员的并发执行。
## 一旦所有研究员完成并将结果存储在状态中，它就完成。
parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
    description="并行运行多个研究智能体以收集信息。"
)

## --- 3. 定义合并智能体（在并行智能体*之后*运行）---
## 此智能体获取并行智能体存储在会话状态中的结果
## 并将它们综合成一个带有归属的单一结构化响应。
merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=GEMINI_MODEL,  # 或者如果需要，可以使用更强大的模型进行综合
    instruction="""你是一名负责将研究发现组合成结构化报告的 AI 助理。你的主要任务是综合以下研究摘要，清楚地将发现归属于其来源领域。使用每个主题的标题构建你的响应。确保报告连贯并平滑地整合关键点。
**关键：你的整个响应必须*完全*基于下面"输入摘要"中提供的信息。不要添加这些特定摘要中不存在的任何外部知识、事实或细节。**

**输入摘要：**
*   **可再生能源：**
    {renewable_energy_result}
*   **电动汽车：**
    {ev_technology_result}
*   **碳捕获：**
    {carbon_capture_result}

**输出格式：**
## 近期可持续技术进展摘要

### 可再生能源发现
（基于 RenewableEnergyResearcher 的发现）
[*仅*综合并详细说明上面提供的可再生能源输入摘要。]

### 电动汽车发现
（基于 EVResearcher 的发现）
[*仅*综合并详细说明上面提供的电动汽车输入摘要。]

### 碳捕获发现
（基于 CarbonCaptureResearcher 的发现）
[*仅*综合并详细说明上面提供的碳捕获输入摘要。]

### 总体结论
[提供一个简短的（1-2 句话）结论性陈述，*仅*连接上面提供的发现。]

*仅*输出遵循此格式的结构化报告。不要在此结构之外包含介绍性或结论性短语，并严格遵守仅使用提供的输入摘要内容。""",
    description="将并行智能体的研究发现组合成结构化的、引用的报告，严格基于提供的输入。",
    # 合并不需要工具
    # 这里不需要 output_key，因为其直接响应是序列的最终输出
)

## --- 4. 创建 SequentialAgent（协调整体流程）---
## 这是将运行的主智能体。它首先执行 ParallelAgent
## 以填充状态，然后执行 MergerAgent 以产生最终输出。
sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    # 首先运行并行研究，然后合并
    sub_agents=[parallel_research_agent, merger_agent],
    description="协调并行研究并综合结果。"
)

root_agent = sequential_pipeline_agent