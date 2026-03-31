"""
5_综合协作系统
演示多种多智能体协作模式的组合使用，构建复杂的协作系统

应用场景：
- 复杂问题解决系统（研究 + 分析 + 决策）
- 智能客服系统（理解 + 分发 + 解决 + 反馈）
- 企业知识管理系统（收集 + 组织 + 分享 + 应用）
"""
from typing import Dict, Any, List, Optional
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import sys
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

# 添加父目录到路径以导入配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_config import create_llm


class BaseAgent:
    """基础智能体类"""

    def __init__(self, name: str, role: str, llm: ChatOpenAI, temperature: float = 0.7):
        self.name = name
        self.role = role
        self.llm = llm
        self.temperature = temperature

        # 创建动态LLM（可以调整温度）
        self.dynamic_llm = create_llm(temperature=temperature)

        self.default_chain = LLMChain(
            llm=self.dynamic_llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个{role}。请用专业、准确的方式回应。"),
                ("human", "{input}")
            ])
        )

    def process(self, input_text: str, **kwargs) -> str:
        """处理输入"""
        print(f"[{self.name}] 正在处理...")
        try:
            if kwargs:
                # 使用自定义参数
                custom_chain = LLMChain(
                    llm=self.llm,
                    prompt=ChatPromptTemplate.from_messages([
                        ("system", f"你是一个{self.role}。{kwargs.get('system_instruction', '')}"),
                        ("human", "{input}")
                    ])
                )
                result = custom_chain.run(input=input_text)
            else:
                result = self.default_chain.run(input=input_text)
            print(f"[{self.name}] 处理完成")
            return result
        except Exception as e:
            print(f"[{self.name}] 处理失败: {e}")
            raise


class ResearchAssistant(BaseAgent):
    """研究助手 - 负责信息收集和初步分析"""

    def __init__(self, llm: ChatOpenAI):
        super().__init__(
            name="研究助手",
            role="信息收集和分析专家",
            llm=llm,
            temperature=0.5
        )

    def gather_information(self, topic: str) -> Dict[str, Any]:
        """收集信息"""
        prompt = f"""
        请收集关于"{topic}"的以下信息：
        1. 背景和定义
        2. 主要组成部分或关键要素
        3. 重要的发展趋势
        4. 相关的技术或方法
        5. 实际应用案例
        """
        return {
            "topic": topic,
            "information": self.process(prompt),
            "source": "研究助手"
        }


class AnalysisTeam:
    """分析团队 - 并行分析多个维度"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.analysts = [
            BaseAgent(name="技术分析师", role="技术分析专家", llm=llm, temperature=0.6),
            BaseAgent(name="市场分析师", role="市场分析专家", llm=llm, temperature=0.6),
            BaseAgent(name="风险评估师", role="风险评估专家", llm=llm, temperature=0.6),
            BaseAgent(name="成本分析师", role="成本分析专家", llm=llm, temperature=0.6)
        ]

    async def analyze_aspect(self, agent: BaseAgent, information: str, aspect: str) -> Dict[str, Any]:
        """异步分析特定维度"""
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            analysis = await loop.run_in_executor(
                executor,
                agent.process,
                f"基于以下信息，从{aspect}角度进行深度分析：\n\n{information}"
            )
        return {
            "agent": agent.name,
            "aspect": aspect,
            "analysis": analysis
        }

    async def comprehensive_analysis(self, research_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """综合分析"""
        aspects = ["技术可行性", "市场前景", "潜在风险", "成本效益"]
        print("\n=== 分析团队开始综合分析 ===")

        tasks = [
            self.analyze_aspect(agent, research_result["information"], aspects[i])
            for i, agent in enumerate(self.analysts)
        ]

        results = await asyncio.gather(*tasks)
        print("=== 分析团队综合分析完成 ===\n")
        return results


class DecisionCouncil:
    """决策委员会 - 辩论和共识"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.council_members = [
            BaseAgent(name="保守派成员", role="保守决策专家，注重风险控制", llm=llm, temperature=0.5),
            BaseAgent(name="激进派成员", role="激进决策专家，注重创新和机会", llm=llm, temperature=0.8),
            BaseAgent(name="平衡派成员", role="平衡决策专家，注重综合评估", llm=llm, temperature=0.7)
        ]

    def debate(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """辩论和决策"""
        print("=== 决策委员会开始辩论 ===")

        # 汇总分析结果
        summary = "\n".join([
            f"{result['agent']}({result['aspect']}): {result['analysis'][:200]}..."
            for result in analyses
        ])

        # 让每个成员发表意见
        opinions = []
        for member in self.council_members:
            opinion = member.process(
                f"基于以下分析结果，请从你的专业角度提出决策建议：\n\n{summary}",
                system_instruction="请明确表达你的立场（支持/反对/有条件支持）和理由。"
            )
            opinions.append({
                "member": member.name,
                "opinion": opinion
            })
            print(f"[{member.name}] 发表意见完成")

        # 综合意见并达成共识
        consensus_maker = BaseAgent(
            name="共识协调员",
            role="共识协调专家",
            llm=self.llm,
            temperature=0.3
        )

        opinions_text = "\n".join([
            f"{op['member']}: {op['opinion']}"
            for op in opinions
        ])

        consensus = consensus_maker.process(
            f"以下委员会成员对同一决策的不同意见：\n\n{opinions_text}\n\n请综合各方意见，提供一个平衡的决策建议。",
            system_instruction="你需要考虑各方观点的合理性，提出一个能够平衡各方关切的综合建议。"
        )

        print("=== 决策委员会达成共识 ===\n")

        return {
            "opinions": opinions,
            "consensus": consensus
        }


class QualityReviewer:
    """质量审查者 - 批评者模式"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.reviewer = BaseAgent(
            name="质量审查员",
            role="质量评估专家",
            llm=llm,
            temperature=0.5
        )

    def review(self, decision_result: Dict[str, Any]) -> Dict[str, Any]:
        """审查决策质量"""
        print("=== 质量审查员开始审查 ===")

        review_prompt = f"""
        请审查以下决策的质量：

        委员会成员意见：
        {chr(10).join([f'- {op["member"]}: {op["opinion"][:100]}...' for op in decision_result["opinions"]])}

        共识建议：
        {decision_result["consensus"]}

        请从以下维度进行审查：
        1. 决策的合理性
        2. 考虑因素的全面性
        3. 风险的充分评估
        4. 实施的可行性
        5. 长远影响的分析

        如果发现问题，请指出并提供改进建议。
        """

        review_result = self.reviewer.process(review_prompt)
        print("=== 质量审查完成 ===\n")

        return {
            "review": review_result,
            "approved": "批准" in review_result or "通过" in review_result
        }


class ExecutionPlanner:
    """执行规划者 - 制定执行计划"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.planner = BaseAgent(
            name="执行规划师",
            role="项目执行规划专家",
            llm=llm,
            temperature=0.6
        )

    def create_plan(self, decision: Dict[str, Any], quality_review: Dict[str, Any]) -> str:
        """创建执行计划"""
        print("=== 执行规划师开始制定计划 ===")

        if not quality_review["approved"]:
            print("决策未通过质量审查，需要重新考虑")
            return "决策未通过质量审查，请根据审查意见调整方案。"

        plan_prompt = f"""
        基于以下批准的决策，制定详细的执行计划：

        决策建议：
        {decision["consensus"]}

        质量审查意见：
        {quality_review["review"]}

        请制定包含以下内容的执行计划：
        1. 执行目标和里程碑
        2. 具体行动步骤
        3. 资源需求
        4. 时间安排
        5. 风险应对措施
        6. 成功标准
        """

        plan = self.planner.process(plan_prompt)
        print("=== 执行计划制定完成 ===\n")

        return plan


class IntelligentProblemSolvingSystem:
    """智能问题解决系统 - 综合多智能体协作"""

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.researcher = ResearchAssistant(llm)
        self.analysis_team = AnalysisTeam(llm)
        self.decision_council = DecisionCouncil(llm)
        self.quality_reviewer = QualityReviewer(llm)
        self.execution_planner = ExecutionPlanner(llm)

    async def solve(self, problem: str) -> Dict[str, Any]:
        """解决复杂问题"""

        print("="*70)
        print("智能问题解决系统启动")
        print("="*70)
        print(f"待解决问题: {problem}\n")

        # 阶段1：信息收集
        print("【阶段1：信息收集】")
        research_result = self.researcher.gather_information(problem)

        # 阶段2：多维分析
        print("\n【阶段2：多维分析】")
        analysis_results = await self.analysis_team.comprehensive_analysis(research_result)

        # 阶段3：决策辩论
        print("\n【阶段3：决策辩论】")
        decision_result = self.decision_council.debate(analysis_results)

        # 阶段4：质量审查
        print("\n【阶段4：质量审查】")
        review_result = self.quality_reviewer.review(decision_result)

        # 阶段5：执行规划
        print("\n【阶段5：执行规划】")
        execution_plan = self.execution_planner.create_plan(decision_result, review_result)

        print("="*70)
        print("智能问题解决系统完成")
        print("="*70)

        return {
            "problem": problem,
            "research": research_result,
            "analysis": analysis_results,
            "decision": decision_result,
            "review": review_result,
            "execution_plan": execution_plan
        }


async def complex_problem_solving_example():
    """复杂问题解决示例"""

    print("=== 综合协作系统示例：企业战略决策 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建智能问题解决系统
    problem_solver = IntelligentProblemSolvingSystem(llm)

    # 定义复杂问题
    problem = "企业是否应该投资建立一个自主可控的AI大模型研发平台？"

    # 解决问题
    result = await problem_solver.solve(problem)

    # 输出最终结果
    print("\n" + "="*70)
    print("【最终解决方案】")
    print("="*70)
    print(result["execution_plan"])

    print("\n" + "="*70)
    print("【系统处理摘要】")
    print("="*70)
    print(f"研究信息来源: {result['research']['source']}")
    print(f"分析维度数量: {len(result['analysis'])}")
    print(f"决策委员会成员: {len(result['decision']['opinions'])}")
    print(f"质量审查结果: {'通过' if result['review']['approved'] else '未通过'}")


async def product_development_example():
    """产品开发决策示例"""

    print("\n\n=== 综合协作系统示例：产品开发决策 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建智能问题解决系统
    problem_solver = IntelligentProblemSolvingSystem(llm)

    # 定义产品开发问题
    problem = "公司应该开发什么类型的下一代智能硬件产品？"

    # 解决问题
    result = await problem_solver.solve(problem)

    # 输出关键结果
    print("\n" + "="*70)
    print("【产品开发执行计划】")
    print("="*70)
    print(result["execution_plan"])


async def technology_transformation_example():
    """技术转型决策示例"""

    print("\n\n=== 综合协作系统示例：技术转型决策 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建智能问题解决系统
    problem_solver = IntelligentProblemSolvingSystem(llm)

    # 定义技术转型问题
    problem = "传统企业如何成功进行数字化转型，采用云原生和微服务架构？"

    # 解决问题
    result = await problem_solver.solve(problem)

    # 输出关键结果
    print("\n" + "="*70)
    print("【数字化转型执行计划】")
    print("="*70)
    print(result["execution_plan"])


if __name__ == "__main__":
    try:
        # 示例1：企业战略决策
        asyncio.run(complex_problem_solving_example())

        # 示例2：产品开发决策
        asyncio.run(product_development_example())

        # 示例3：技术转型决策
        asyncio.run(technology_transformation_example())

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已设置正确的 OPENAI_API_KEY 环境变量")
