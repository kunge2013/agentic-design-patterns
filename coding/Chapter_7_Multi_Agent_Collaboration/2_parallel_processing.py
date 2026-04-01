"""
2_并行处理模式
演示多个智能体同时处理不同任务，然后汇总结果

应用场景：
- 多源数据收集（多个API同时获取）
- 并行分析（从不同角度分析同一数据）
- 分布式决策（多个专家同时评估）
"""
import asyncio
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import sys
import os

# 添加父目录到路径以导入配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_config import create_llm


class ParallelAgent:
    """并行智能体基类"""

    def __init__(self, name: str, role: str, goal: str, llm: ChatOpenAI):
        self.name = name
        self.role = role
        self.goal = goal
        self.llm = llm
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", f"你是一个{role}。你的目标是：{goal}"),
            ("human", "{input}")
        ])
        # 使用现代LangChain LCEL方式
        self.chain = self.prompt_template | llm

    def process(self, input_text: str) -> Dict[str, Any]:
        """处理输入并返回结果"""
        print(f"[{self.name}] 开始处理...")
        try:
            result = self.chain.invoke({"input": input_text})
            result_text = result.content if hasattr(result, 'content') else str(result)
            print(f"[{self.name}] 处理完成")
            return {
                "agent": self.name,
                "success": True,
                "result": result_text
            }
        except Exception as e:
            print(f"[{self.name}] 处理失败: {e}")
            return {
                "agent": self.name,
                "success": False,
                "error": str(e)
            }


async def run_agent_async(agent: ParallelAgent, input_text: str) -> Dict[str, Any]:
    """异步执行智能体"""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(
            executor,
            agent.process,
            input_text
        )


class ParallelProcessor:
    """并行处理器"""

    def __init__(self, name: str, synthesizer_role: str = "综合器"):
        self.name = name
        self.agents: List[ParallelAgent] = []
        self.synthesizer_role = synthesizer_role

    def add_agent(self, agent: ParallelAgent):
        """添加智能体"""
        self.agents.append(agent)

    async def process_parallel(self, input_text: str) -> List[Dict[str, Any]]:
        """并行处理所有智能体"""
        print(f"\n=== {self.name} 开始并行处理 ===")
        tasks = [run_agent_async(agent, input_text) for agent in self.agents]
        results = await asyncio.gather(*tasks)
        print(f"=== {self.name} 并行处理完成 ===\n")
        return results

    def synthesize(self, results: List[Dict[str, Any]], llm: ChatOpenAI) -> str:
        """汇总所有智能体的结果"""
        # Synthesizer将结果整合到最终的字符串中
        synthesis_input = "以下是多个并行智能体的处理结果：\n\n"
        for result in results:
            if result["success"]:
                synthesis_input += f"【{result['agent']}】\n{result['result']}\n\n"
            else:
                synthesis_input += f"【{result['agent']}】处理失败：{result['error']}\n\n"

        synthesis_input += "\n请综合以上所有智能体的结果，提供一个全面、连贯的总结。"

        synthesizer_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个{self.synthesizer_role}。你的目标是将多个智能体的结果整合成一个连贯、全面的总结。"),
                ("human", "{input}")
            ])
        )

        print("=== 开始综合处理 ===")
        synthesis_result = synthesizer_chain.run(input=synthesis_input)
        print("=== 综合处理完成 ===\n")
        return synthesis_result


async def parallel_research_analysis_example():
    """并行研究分析示例：从多个角度分析同一主题"""

    print("=== 并行处理模式示例：多角度产品分析 ===\n")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建并行处理器
    processor = ParallelProcessor("产品分析器")

    # 添加多个专业智能体
    processor.add_agent(ParallelAgent(
        name="市场分析师",
        role="市场分析专家",
        goal="从市场角度分析产品的竞争力、市场定位和机会",
        llm=llm
    ))

    processor.add_agent(ParallelAgent(
        name="技术专家",
        role="技术评估专家",
        goal="从技术角度分析产品的技术架构、创新点和潜在风险",
        llm=llm
    ))

    processor.add_agent(ParallelAgent(
        name="用户体验专家",
        role="用户体验评估专家",
        goal="从用户体验角度分析产品的易用性、功能完整性和用户满意度",
        llm=llm
    ))

    processor.add_agent(ParallelAgent(
        name="财务分析师",
        role="财务分析专家",
        goal="从财务角度分析产品的盈利模式、成本结构和投资回报",
        llm=llm
    ))

    # 输入主题
    product_description = """
    产品描述：AI驱动的智能客服系统
    主要功能：
    - 基于大语言模型的自然语言理解和生成
    - 多轮对话和上下文记忆
    - 多渠道支持（网页、微信、电话等）
    - 实时翻译和情感分析
    - 知识库集成和智能推荐
    """

    print(f"分析对象: {product_description.strip()[:100]}...\n")

    # 并行处理
    results = await processor.process_parallel(product_description)

    # 汇总结果
    final_synthesis = processor.synthesize(results, llm)

    print("="*60)
    print("最终综合分析结果")
    print("="*60)
    print(final_synthesis)


async def parallel_data_gathering_example():
    """并行数据收集示例：同时从多个数据源获取信息"""

    print("\n\n=== 并行数据收集示例：企业信息收集 ===\n")

    # 创建LLM
    llm = create_llm(temperature=0.5)

    # 创建并行处理器
    data_collector = ParallelProcessor("企业信息收集器")

    # 添加数据收集智能体
    data_collector.add_agent(ParallelAgent(
        name="市场情报智能体",
        role="市场情报收集专家",
        goal="收集和整理指定公司的市场地位、竞争对手和行业趋势信息",
        llm=llm
    ))

    data_collector.add_agent(ParallelAgent(
        name="财务数据智能体",
        role="财务数据收集专家",
        goal="收集和整理指定公司的财务健康状况、营收和利润信息",
        llm=llm
    ))

    data_collector.add_agent(ParallelAgent(
        name="技术创新智能体",
        role="技术创新分析专家",
        goal="收集和整理指定公司的技术专利、研发投入和技术优势信息",
        llm=llm
    ))

    data_collector.add_agent(ParallelAgent(
        name="人力资源智能体",
        role="人力资源分析专家",
        goal="收集和整理指定公司的组织结构、人才战略和企业文化信息",
        llm=llm
    ))

    # 目标公司
    company = "某知名科技公司"

    print(f"目标公司: {company}\n")

    # 并行收集数据
    data_results = await data_collector.process_parallel(company)

    # 综合所有信息
    comprehensive_report = data_collector.synthesize(data_results, llm)

    print("="*60)
    print("综合企业分析报告")
    print("="*60)
    print(comprehensive_report)


async def parallel_decision_making_example():
    """并行决策示例：多个专家同时评估方案"""

    print("\n\n=== 并行决策示例：项目方案评估 ===\n")

    # 创建LLM
    llm = create_llm(temperature=0.6)

    # 创建并行决策器
    decision_maker = ParallelProcessor("方案评估委员会")

    # 添加专家智能体
    decision_maker.add_agent(ParallelAgent(
        name="技术专家",
        role="技术评估专家",
        goal="从技术可行性、架构合理性和技术风险角度评估方案",
        llm=llm
    ))

    decision_maker.add_agent(ParallelAgent(
        name="成本分析专家",
        role="成本评估专家",
        goal="从成本效益、资源投入和预算控制角度评估方案",
        llm=llm
    ))

    decision_maker.add_agent(ParallelAgent(
        name="风险评估专家",
        role="风险评估专家",
        goal="从项目风险、潜在问题和风险缓解角度评估方案",
        llm=llm
    ))

    decision_maker.add_agent(ParallelAgent(
        name="商业价值专家",
        role="商业价值评估专家",
        goal="从商业价值、市场前景和投资回报角度评估方案",
        llm=llm
    ))

    # 待评估的方案
    proposal = """
    项目方案：电商平台微服务架构升级
    主要内容：
    1. 将现有的单体架构拆分为用户、订单、商品、支付等微服务
    2. 采用Docker容器化部署和Kubernetes编排
    3. 引入服务网格和API网关
    4. 实施事件驱动架构和消息队列
    5. 建立自动化CI/CD流水线
    预期收益：提高系统可用性、扩展性和开发效率
    """

    print(f"评估方案: {proposal.strip()[:100]}...\n")

    # 并行评估
    evaluation_results = await decision_maker.process_parallel(proposal)

    # 综合评估结果
    final_recommendation = decision_maker.synthesize(evaluation_results, llm)

    print("="*60)
    print("综合评估报告和建议")
    print("="*60)
    print(final_recommendation)


if __name__ == "__main__":
    try:
        # 示例1：并行研究分析
        asyncio.run(parallel_research_analysis_example())

        # 示例2：并行数据收集
        asyncio.run(parallel_data_gathering_example())

        # 示例3：并行决策
        asyncio.run(parallel_decision_making_example())

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已设置正确的 OPENAI_API_KEY 环境变量")
