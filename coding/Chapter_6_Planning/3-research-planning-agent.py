"""
3-research-planning-agent.py

研究型规划智能体实现
模拟 Deep Research 模式的多步规划和执行
"""
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import time

# 添加父目录与其他目录到路径
parent_dir = str(Path(__file__).parent.parent)
chapter1_dir = str(Path(__file__).parent.parent / "Chapter_1_Prompt_Chaining")

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if chapter1_dir not in sys.path:
    sys.path.insert(0, chapter1_dir)

from llm_config import get_default_llm_config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import Tool

## 1. 初始化 LLM 配置
llm_config = get_default_llm_config()
llm_config.print_config()
print()

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

@dataclass
class ResearchResult:
    """研究结果"""
    topic: str
    plan: ResearchPlan
    findings: List[str]
    summary: str
    references: List[Dict]
    execution_time: float

## 3. 模拟搜索工具
def mock_search(query: str) -> List[Dict]:
    """
    模拟网络搜索工具

    Args:
        query: 搜索查询

    Returns:
        List[Dict]: 搜索结果
    """
    # 这里模拟返回一些结果
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

## 4. Deep Research 智能体类
class DeepResearchAgent:
    """Deep Research 智能体"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.search_tool = Tool(
            name="web_search",
            func=mock_search,
            description="搜索网络信息，返回相关文档和资源"
        )

    def create_research_plan(self, topic: str, num_queries: int = 3) -> ResearchPlan:
        """
        创建研究计划

        Args:
            topic: 研究主题
            num_queries: 生成查询的数量

        Returns:
            ResearchPlan: 研究计划
        """
        print(f"正在为主题创建研究计划：{topic}\n")

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

    def _parse_queries(self, plan_text: str) -> List[ResearchQuery]:
        """
        解析查询文本

        Args:
            plan_text: 计划文本

        Returns:
            List[ResearchQuery]: 查询列表
        """
        queries = []
        lines = plan_text.split('\n')

        for i, line in enumerate(lines):
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '- '))):
                # 提取查询文本
                query_text = line.lstrip('0123456789.- ').strip()

                # 生成搜索术语（简化处理）
                search_terms = [term.lower() for term in query_text.split()[:4]]

                queries.append(ResearchQuery(
                    query_id=i + 1,
                    query_text=query_text,
                    search_terms=search_terms
                ))

        return queries

    def execute_research_plan(self, plan: ResearchPlan) -> ResearchResult:
        """
        执行研究计划

        Args:
            plan: 研究计划

        Returns:
            ResearchResult: 研究结果
        """
        start_time = time.time()

        print(f"\n{'='*80}")
        print(f"开始执行研究计划")
        print(f"主题：{plan.research_topic}")
        print(f"查询数：{len(plan.queries)}")
        print(f"{'='*80}\n")

        # 执行每个查询
        for i, query in enumerate(plan.queries):
            print(f"查询 {i+1}/{len(plan.queries)}: {query.query_text}")
            print(f"搜索术语：{', '.join(query.search_terms)}")

            # 执行搜索
            search_results = self.search_tool.func(query.query_text)

            print(f"找到 {len(search_results)} 个结果")
            for j, result in enumerate(search_results, 1):
                print(f"  {j}. {result['title']}")
                print(f"     {result['snippet'][:80]}...")
                print(f"     相关性：{result['relevance_score']:.2f}")
                query.results.append(result)

            query.status = "completed"
            print(f"  ✓ 查询完成\n")

        # 综合结果
        print(f"{'='*80}")
        print("正在综合研究结果...")
        print(f"{'='*80}\n")

        summary = self._synthesize_results(plan)

        execution_time = time.time() - start_time

        print(f"{'='*80}")
        print(f"研究完成！总耗时：{execution_time:.2f}秒")
        print(f"{'='*80}\n")

        return ResearchResult(
            topic=plan.research_topic,
            plan=plan,
            findings=self._extract_findings(plan),
            summary=summary,
            references=self._collect_references(plan),
            execution_time=execution_time
        )

    def _synthesize_results(self, plan: ResearchPlan) -> str:
        """
        综合研究结果

        Args:
            plan: 研究计划

        Returns:
            str: 研究摘要
        """
        synthesis_prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一个专业的研究分析师。你的任务是综合多个搜索查询的结果，提供连贯的研究摘要。

你的摘要应该：
1. 涵盖研究的核心发现
2. 突出关键主题和趋势
3. 提供有意义的见解
4. 保持客观和准确"""),
            ("user", """研究主题：{topic}

研究结果概要：
{research_summary}

请提供一份全面的研究摘要。""")
        ])

        # 收集结果摘要
        research_summary = []
        for query in plan.queries:
            research_summary.append(f"查询：{query.query_text}")
            for result in query.results[:2]:  # 只使用前两个结果
                research_summary.append(f"- {result['snippet']}")

        chain = synthesis_prompt | self.llm
        response = chain.invoke({
            "topic": plan.research_topic,
            "research_summary": "\n".join(research_summary)
        })

        return response.content

    def _extract_findings(self, plan: ResearchPlan) -> List[str]:
        """提取研究发现"""
        findings = []
        for query in plan.queries:
            for result in query.results:
                findings.append(result['snippet'])
        return findings

    def _collect_references(self, plan: ResearchPlan) -> List[Dict]:
        """收集参考文献"""
        references = []
        for query in plan.queries:
            for result in query.results:
                references.append({
                    "title": result['title'],
                    "url": result['url'],
                    "query": query.query_text
                })
        return references

## 5. 使用示例
def main():
    # 创建 Deep Research 智能体
    agent = DeepResearchAgent(llm)

    # 示例 1：技术主题研究
    print("="*80)
    print("示例 1：技术主题研究")
    print("="*80)
    print()

    tech_topic = "人工智能在医疗诊断中的应用"
    tech_plan = agent.create_research_plan(tech_topic, num_queries=4)

    print(f"\n生成的研究计划：")
    print(f"主题：{tech_plan.research_topic}")
    print(f"创建时间：{tech_plan.created_at}")
    print(f"\n搜索查询：")
    for query in tech_plan.queries:
        print(f"  {query.query_id}. {query.query_text}")

    tech_result = agent.execute_research_plan(tech_plan)

    print("\n" + "="*80)
    print("研究摘要")
    print("="*80)
    print(tech_result.summary)
    print()

    print("\n" + "="*80)
    print("参考文献")
    print("="*80)
    for i, ref in enumerate(tech_result.references, 1):
        print(f"{i}. {ref['title']}")
        print(f"   URL: {ref['url']}")
        print(f"   查询：{ref['query']}")
        print()

    # 示例 2：商业分析
    print("\n" + "="*80)
    print("示例 2：商业分析")
    print("="*80)
    print()

    business_topic = "可持续能源市场的未来发展趋势"
    business_plan = agent.create_research_plan(business_topic, num_queries=3)

    print(f"\n生成的研究计划：")
    print(f"主题：{business_plan.research_topic}")
    print(f"\n搜索查询：")
    for query in business_plan.queries:
        print(f"  {query.query_id}. {query.query_text}")

    business_result = agent.execute_research_plan(business_plan)

    print("\n" + "="*80)
    print("研究摘要")
    print("="*80)
    print(business_result.summary[:500] + "...")  # 只显示部分
    print()

if __name__ == "__main__":
    main()
