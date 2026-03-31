"""
2-simple-planning-agent.py

简单的规划智能体实现
演示智能体如何将复杂任务分解为多个步骤
"""
import os
import sys
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass

# 添加父目录到路径
parent_dir = str(Path(__file__).parent.parent)
chapter1_dir = str(Path(__file__).parent.parent / "Chapter_1_Prompt_Chaining")

if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if chapter1_dir not in sys.path:
    sys.path.insert(0, chapter1_dir)

from llm_config import get_default_llm_config
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

## 1. 初始化 LLM 配置
llm_config = get_default_llm_config()
llm_config.print_config()
print()

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
        """
        创建执行计划

        Args:
            goal: 目标描述
            context: 上下文信息

        Returns:
            ExecutionPlan: 执行计划
        """
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

        # 解析生成的计划（简化版）
        return self._parse_plan(goal, plan_text)

    def _parse_plan(self, goal: str, plan_text: str) -> ExecutionPlan:
        """
        解析计划文本（简化实现）

        Args:
            goal: 原始目标
            plan_text: 生成的计划文本

        Returns:
            ExecutionPlan: 解析后的计划
        """
        # 这里简化处理，实际应用中应该更 robust 地解析
        steps = []
        lines = plan_text.split('\n')

        step_num = 1
        for i, line in enumerate(lines):
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '- '))):
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
        """
        执行计划（模拟执行）

        Args:
            plan: 执行计划

        Returns:
            Dict: 执行结果
        """
        print(f"\n{'='*80}")
        print(f"开始执行计划：{plan.goal}")
        print(f"复杂度：{plan.estimated_complexity}")
        print(f"步骤数：{len(plan.steps)}")
        print(f"{'='*80}\n")

        results = {}

        for step in plan.steps:
            print(f"步骤 {step.step_number}: {step.description}")
            if step.tool_needed:
                print(f"  需要工具：{step.tool_needed}")
            print(f"  ✓ 执行完成\n")

            # 模拟执行结果
            results[f"step_{step.step_number}"] = {
                "description": step.description,
                "status": "completed",
                "tool_used": step.tool_needed
            }

        print(f"{'='*80}")
        print("计划执行完成！")
        print(f"{'='*80}\n")

        return {
            "goal": plan.goal,
            "status": "completed",
            "steps_completed": len(plan.steps),
            "results": results
        }

## 4. 使用示例
def main():
    # 创建规划智能体
    agent = PlanningAgent(llm)

    # 示例 1：研究任务
    print("示例 1：研究任务规划\n")
    research_goal = "研究并总结人工智能在医疗诊断领域的最新进展"
    research_context = "重点关注 2023-2024 年的研究成果和实际应用案例"

    research_plan = agent.create_plan(research_goal, research_context)

    print(f"目标：{research_plan.goal}")
    print(f"复杂度：{research_plan.estimated_complexity}")
    print("\n执行步骤：")
    for step in research_plan.steps:
        print(f"  {step.step_number}. {step.description}")
        if step.tool_needed:
            print(f"     工具：{step.tool_needed}")

    # 执行计划
    research_result = agent.execute_plan(research_plan)

    # 示例 2：项目开发任务
    print("\n" + "="*80 + "\n")
    print("示例 2：项目开发任务规划\n")

    dev_goal = "开发一个基于 Web 的任务管理应用"
    dev_context = "需要支持用户认证、任务 CRUD 操作和实时协作功能"

    dev_plan = agent.create_plan(dev_goal, dev_context)

    print(f"目标：{dev_plan.goal}")
    print(f"复杂度：{dev_plan.estimated_complexity}")
    print("\n执行步骤：")
    for step in dev_plan.steps:
        print(f"  {step.step_number}. {step.description}")
        if step.tool_needed:
            print(f"     工具：{step.tool_needed}")

if __name__ == "__main__":
    main()
