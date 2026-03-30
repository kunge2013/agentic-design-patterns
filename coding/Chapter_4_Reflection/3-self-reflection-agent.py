#!/usr/bin/env python3
"""
基于 LangChain 的自我反思智能体示例

这个示例展示了单个智能体如何进行自我反思，
而不需要分离的评审者智能体。智能体通过角色切换
来实现生成和评审功能。

范式：反思模式（自我反思）
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

llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

class SelfReflectingAgent:
    """
    自我反思智能体：能够生成内容并自我评审
    """
    def __init__(self, name, task_description):
        self.name = name
        self.task_description = task_description

        # 生成提示模板
        self.generator_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的{role}。"),
            ("user", "{task}\n\n请完成这个任务。")
        ])

        # 评审提示模板
        self.reflector_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个严谨的评审者。"),
            ("user", """任务描述：
{task}

生成的内容：
{content}

请评审上述内容。如果内容满足所有要求，返回 "PERFECT"。
否则，提供具体的改进建议。""")
        ])

        # 改进提示模板
        self.improver_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的{role}。"),
            ("user", """原始内容：
{content}

评审反馈：
{feedback}

请根据反馈改进内容。""")
        ])

    def generate(self, role, task):
        """生成初始内容"""
        print(f"\n>>> {self.name} - 生成阶段")
        print(f"角色: {role}")
        print(f"任务: {task[:50]}...")

        prompt = self.generator_prompt.format(
            role=role,
            task=task
        )
        response = llm.invoke(prompt)
        return response.content

    def reflect(self, task, content):
        """自我评审生成的内容"""
        print(f"\n>>> {self.name} - 评审阶段")

        prompt = self.reflector_prompt.format(
            task=task,
            content=content
        )
        response = llm.invoke(prompt)
        feedback = response.content

        return feedback, "PERFECT" in feedback

    def improve(self, role, content, feedback):
        """基于反馈改进内容"""
        print(f"\n>>> {self.name} - 改进阶段")

        prompt = self.improver_prompt.format(
            role=role,
            content=content,
            feedback=feedback
        )
        response = llm.invoke(prompt)
        return response.content

    def execute_with_reflection(self, role, task, max_iterations=3):
        """执行带有自我反思的任务"""
        print(f"\n{'='*20} {self.name} {'='*20}")
        print(f"执行带有自我反思的任务，最多 {max_iterations} 次迭代")

        # 生成初始内容
        content = self.generate(role, task)

        # 迭代反思和改进
        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*15} 迭代 {iteration} {'='*15}")

            # 自我评审
            feedback, is_perfect = self.reflect(task, content)

            if is_perfect:
                print("✓ 内容完美，无需改进")
                break

            # 改进内容
            content = self.improve(role, content, feedback)

        return content

def main():
    """
    演示自我反思智能体的使用
    """
    print("自我反思智能体演示")
    print("="*50)

    # 创建自我反思智能体
    agent = SelfReflectingAgent(
        name="写作助手",
        task_description="能够生成高质量文本并进行自我评审"
    )

    # 示例任务
    tasks = [
        {
            "role": "技术文档撰写者",
            "task": "为机器学习初学者写一段关于梯度下降算法的解释，要求清晰易懂，包含数学公式说明"
        },
        {
            "role": "营销文案撰稿人",
            "task": "为一个环保产品写一段吸引人的产品描述，突出其环保特性和使用价值"
        }
    ]

    # 执行任务
    results = []
    for task_info in tasks:
        result = agent.execute_with_reflection(
            role=task_info["role"],
            task=task_info["task"],
            max_iterations=2
        )
        results.append(result)

    # 显示结果
    print("\n" + "="*30 + " 最终结果 " + "="*30)
    for i, (task_info, result) in enumerate(zip(tasks, results), 1):
        print(f"\n任务 {i}: {task_info['task'][:50]}...")
        print(f"角色: {task_info['role']}")
        print(f"结果长度: {len(result)} 字符")
        print(f"内容预览: {result[:200]}...")

def demonstrate_role_switching():
    """
    演示角色切换的自我反思
    """
    print("\n" + "="*40 + " 角色切换演示 " + "="*40)

    # 智能体在不同角色间切换
    roles = [
        "作家",
        "编辑",
        "批评家"
    ]

    task = "写一段关于AI伦理的短文"

    current_content = ""
    for i, role in enumerate(roles):
        print(f"\n--- 切换到角色: {role} ---")

        if i == 0:
            # 第一个角色生成内容
            prompt = f"作为{role}，请完成以下任务：{task}"
            response = llm.invoke([HumanMessage(content=prompt)])
            current_content = response.content
            print(f"生成内容: {current_content[:100]}...")
        else:
            # 后续角色评审和改进
            if role == "编辑":
                prompt = f"作为{role}，请改进以下文本：{current_content}"
                response = llm.invoke([HumanMessage(content=prompt)])
                current_content = response.content
            elif role == "批评家":
                prompt = f"作为{role}，请评审以下文本并提供反馈：{current_content}"
                response = llm.invoke([HumanMessage(content=prompt)])
                feedback = response.content
                print(f"评审反馈: {feedback[:100]}...")

    print(f"\n最终内容: {current_content[:150]}...")

if __name__ == "__main__":
    main()
    demonstrate_role_switching()
