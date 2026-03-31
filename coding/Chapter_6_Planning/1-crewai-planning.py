"""
1-crewai-planning.py

基于 LLM 的规划模式实现
演示智能体如何先规划再执行复杂任务
"""
import os
import sys
from pathlib import Path
from typing import List
from dataclasses import dataclass

# 添加父目录到路径，以便导入 llm_config
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

@dataclass
class ExecutionPlan:
    """执行计划"""
    topic: str
    plan_steps: List[PlanningStep]
    summary: str

## 3. 创建规划智能体
def create_planning_task(topic: str) -> ExecutionPlan:
    """创建规划任务并执行"""

    # 第一步：创建计划
    planning_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的文章规划师。你的任务是为给定主题创建一个清晰的写作计划。"),
        ("user", "请为主题'{topic}'创建一个简短摘要的写作计划。列出3-5个要点步骤。")
    ])

    chain = planning_prompt | llm
    plan_response = chain.invoke({"topic": topic})

    print("="*80)
    print("## 规划阶段：创建写作计划")
    print("="*80)
    print(plan_response.content)
    print()

    # 解析计划步骤
    plan_steps = []
    lines = plan_response.content.split('\n')
    step_num = 1
    for line in lines:
        line = line.strip()
        if line and (line.startswith(('1.', '2.', '3.', '4.', '5.', '- '))):
            description = line.lstrip('0123456789.- ').strip()
            plan_steps.append(PlanningStep(step_number=step_num, description=description))
            step_num += 1

    # 第二步：根据计划撰写摘要
    writing_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的技术作家。你能够根据提供的计划撰写简洁、准确的摘要。"),
        ("user", """主题：{topic}
写作计划：
{plan_text}

请根据以上计划撰写一个200字左右的简洁摘要。""")
    ])

    plan_text = "\n".join([f"{step.step_number}. {step.description}" for step in plan_steps])

    chain = writing_prompt | llm
    summary_response = chain.invoke({"topic": topic, "plan_text": plan_text})

    print("="*80)
    print("## 执行阶段：撰写摘要")
    print("="*80)
    print(summary_response.content)
    print()

    return ExecutionPlan(
        topic=topic,
        plan_steps=plan_steps,
        summary=summary_response.content
    )

## 4. 执行任务
if __name__ == "__main__":
    topic = "强化学习在 AI 中的重要性"

    print("="*80)
    print("## 运行规划和写作任务 ##")
    print("="*80)
    print(f"主题：{topic}")
    print()

    result = create_planning_task(topic)

    print()
    print("="*80)
    print("## 任务结果 ##")
    print("="*80)
    print(f"主题：{result.topic}")
    print(f"规划步骤数：{len(result.plan_steps)}")
    print("\n规划步骤：")
    for step in result.plan_steps:
        print(f"  {step.step_number}. {step.description}")
    print(f"\n摘要：{result.summary}")
    print()
