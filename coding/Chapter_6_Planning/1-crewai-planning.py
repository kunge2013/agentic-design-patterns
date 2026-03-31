"""
1-crewai-planning.py

基于 CrewAI 的规划模式实现
演示智能体如何先规划再执行复杂任务
"""
import os
import sys
from pathlib import Path

# 添加父目录到路径，以便导入 llm_config
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from llm_config import get_default_llm_config

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

## 1. 初始化 LLM 配置
llm_config = get_default_llm_config()
llm_config.print_config()
print()

## 2. 创建 LLM 实例
llm = llm_config.create_llm()

## 3. 定义规划智能体
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

## 4. 定义规划任务
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

## 5. 创建并执行团队
crew = Crew(
    agents=[planner_writer_agent],
    tasks=[planning_task],
    process=Process.sequential,
)

print("="*80)
print("## 运行规划和写作任务 ##")
print("="*80)
print()

result = crew.kickoff()

print()
print("="*80)
print("## 任务结果 ##")
print("="*80)
print(result)
print()
