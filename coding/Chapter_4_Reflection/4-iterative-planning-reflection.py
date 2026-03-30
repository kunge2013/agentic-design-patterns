#!/usr/bin/env python3
"""
基于 LangChain 的迭代反思与规划优化示例

这个示例展示了反思模式在复杂任务规划中的应用。
通过迭代反思，系统能够：
1. 生成初始行动计划
2. 评估计划的可行性和质量
3. 根据反馈优化计划
4. 重复直到获得满意方案

范式：反思模式（迭代规划优化）
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage

# --- 配置 ---
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("在 .env 文件中未找到 OPENAI_API_KEY。请添加它。")

llm = ChatOpenAI(model="gpt-4o", temperature=0.5)

class PlanningReflectionSystem:
    """
    规划反思系统：能够生成、评估和优化行动计划
    """
    def __init__(self, system_name):
        self.system_name = system_name

        # 规划器提示
        self.planner_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的项目规划师。"),
            ("user", """目标：
{goal}

约束条件：
{constraints}

请创建一个详细的行动计划，包括：
1. 主要步骤
2. 每个步骤的具体描述
3. 预期时间线
4. 潜在风险和缓解措施

以结构化的方式呈现你的计划。""")
        ])

        # 评估者提示
        self.evaluator_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个严格的项目评估师。"),
            ("user", """原始目标：
{goal}

约束条件：
{constraints}

提出的计划：
{plan}

请评估这个计划：
1. 检查是否满足所有约束条件
2. 识别逻辑漏洞或可行性问题
3. 评估风险的合理性
4. 提供改进建议

如果计划完美，返回 "PLAN_PERFECT"。
否则，提供具体的改进建议。""")
        ])

        # 优化器提示
        self.optimizer_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个经验丰富的项目优化师。"),
            ("user", """原始计划：
{current_plan}

评估反馈：
{feedback}

请根据反馈优化计划，解决所有指出的问题。""")
        ])

    def generate_plan(self, goal, constraints):
        """生成初始计划"""
        print(f"\n{'='*20} 计划生成阶段 {'='*20}")
        print(f"目标: {goal}")
        print(f"约束: {constraints[:50]}...")

        prompt = self.planner_prompt.format(
            goal=goal,
            constraints=constraints
        )
        response = llm.invoke(prompt)
        return response.content

    def evaluate_plan(self, goal, constraints, plan):
        """评估计划质量"""
        print(f"\n{'='*20} 计划评估阶段 {'='*20}")

        prompt = self.evaluator_prompt.format(
            goal=goal,
            constraints=constraints,
            plan=plan
        )
        response = llm.invoke(prompt)
        feedback = response.content

        is_perfect = "PLAN_PERFECT" in feedback
        return feedback, is_perfect

    def optimize_plan(self, current_plan, feedback):
        """优化计划"""
        print(f"\n{'='*20} 计划优化阶段 {'='*20}")

        prompt = self.optimizer_prompt.format(
            current_plan=current_plan,
            feedback=feedback
        )
        response = llm.invoke(prompt)
        return response.content

    def iterative_planning(self, goal, constraints, max_iterations=3):
        """迭代规划和反思"""
        print(f"\n{'='*15} {self.system_name} {'='*15}")
        print(f"启动迭代规划过程，最多 {max_iterations} 次迭代")

        # 生成初始计划
        current_plan = self.generate_plan(goal, constraints)

        # 迭代评估和优化
        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*15} 迭代 {iteration} {'='*15}")

            # 评估计划
            feedback, is_perfect = self.evaluate_plan(goal, constraints, current_plan)

            if is_perfect:
                print("✓ 计划完美，无需优化")
                break

            print(f"评估反馈: {feedback[:200]}...")

            # 优化计划
            current_plan = self.optimize_plan(current_plan, feedback)
            print(f"优化后的计划: {current_plan[:200]}...")

        return current_plan

def complex_problem_solving():
    """
    演示复杂问题解决的反思循环
    """
    print("\n" + "="*40 + " 复杂问题解决演示 " + "="*40)

    # 创建规划反思系统
    planner = PlanningReflectionSystem("复杂问题解决系统")

    # 示例：软件开发项目规划
    goal = "在3个月内开发一个完整的电商网站，包含用户认证、商品管理、购物车和支付功能"
    constraints = """
    1. 团队规模：5名开发者
    2. 预算：10万美元
    3. 技术栈：React + Node.js + PostgreSQL
    4. 安全要求：符合PCI-DSS标准
    5. 性能要求：支持10,000并发用户
    """

    optimized_plan = planner.iterative_planning(
        goal=goal,
        constraints=constraints,
        max_iterations=3
    )

    print(f"\n{'='*30} 最终计划 {'='*30}")
    print(optimized_plan)

def step_by_step_reflection():
    """
    演示分步反思过程
    """
    print("\n" + "="*40 + " 分步反思演示 " + "="*40)

    # 模拟一个多步骤的问题解决过程
    problem = "如何优化数据库查询性能？"

    # 步骤1：初步分析
    step1_prompt = f"分析以下问题并提供初步解决方案：{problem}"
    step1_response = llm.invoke([HumanMessage(content=step1_prompt)])
    initial_solution = step1_response.content

    print(f"\n步骤1 - 初步分析:")
    print(f"{initial_solution[:300]}...")

    # 步骤2：反思和评审
    step2_prompt = f"""原始问题：{problem}

初步解决方案：
{initial_solution}

作为数据库专家，请评审这个解决方案：
1. 识别遗漏的优化机会
2. 评估方案的完整性和可行性
3. 提供更深入的技术建议"""

    step2_response = llm.invoke([HumanMessage(content=step2_prompt)])
    critique = step2_response.content

    print(f"\n步骤2 - 评审反馈:")
    print(f"{critique[:300]}...")

    # 步骤3：优化解决方案
    step3_prompt = f"""初步解决方案：
{initial_solution}

评审反馈：
{critique}

请基于反馈优化解决方案，创建一个更完整和有效的方案。"""

    step3_response = llm.invoke([HumanMessage(content=step3_prompt)])
    optimized_solution = step3_response.content

    print(f"\n步骤3 - 优化解决方案:")
    print(f"{optimized_solution[:400]}...")

    return optimized_solution

def collaborative_reflection():
    """
    演示协作式反思
    """
    print("\n" + "="*40 + " 协作反思演示 " + "="*40)

    topic = "设计一个企业级微服务架构"

    perspectives = [
        "架构师",
        "安全专家",
        "运维工程师",
        "性能优化专家"
    ]

    current_design = ""

    for i, perspective in enumerate(perspectives):
        print(f"\n{'='*15} {perspective} 视角 {'='*15}")

        if i == 0:
            # 第一个视角生成初始设计
            prompt = f"作为{perspective}，为以下主题设计方案：{topic}"
            response = llm.invoke([HumanMessage(content=prompt)])
            current_design = response.content
            print(f"初始设计: {current_design[:200]}...")
        else:
            # 后续视角进行评审和改进
            review_prompt = f"""当前设计方案：
{current_design}

作为{perspective}，请评审这个设计并提供改进建议。"""
            review_response = llm.invoke([HumanMessage(content=review_prompt)])
            feedback = review_response.content

            print(f"{perspective} 反馈: {feedback[:200]}...")

            # 整合反馈
            integrate_prompt = f"""原设计：
{current_design}

来自 {perspective} 的反馈：
{feedback}

请整合反馈，改进设计方案。"""
            integrate_response = llm.invoke([HumanMessage(content=integrate_prompt)])
            current_design = integrate_response.content

    print(f"\n{'='*30} 最终设计 {'='*30}")
    print(f"{current_design[:300]}...")

if __name__ == "__main__":
    print("迭代反思与规划优化演示")
    print("="*50)

    # 复杂问题解决
    complex_problem_solving()

    # 分步反思
    step_by_step_reflection()

    #.协作反思
    collaborative_reflection()
