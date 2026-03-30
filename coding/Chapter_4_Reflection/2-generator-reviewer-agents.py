#!/usr/bin/env python3
"""
基于 LangChain 的内容生成与评审示例

这个示例展示了生成器-评审者模型在内容创建中的应用。
通过分离内容生成和质量评审两个角色，系统能够：
1. 生成器智能体创建初始内容
2. 评审者智能体检查事实准确性和质量
3. 提供结构化的评审反馈

范式：反思模式（生成器-评审者智能体）
"""

import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# --- 配置 ---
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("在 .env 文件中未找到 OPENAI_API_KEY。请添加它。")

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

class GeneratorAgent:
    """
    生成器智能体：负责创建初始内容
    """
    def __init__(self, description, instruction):
        self.description = description
        self.instruction = instruction
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", f"{description}\n{instruction}"),
            ("user", "{topic}")
        ])

    def generate(self, topic):
        """生成关于给定主题的内容"""
        response = llm.invoke(self.system_prompt.format(topic=topic))
        return response.content

class ReviewerAgent:
    """
    评审者智能体：负责评估生成内容的质量
    """
    def __init__(self, description, instruction):
        self.description = description
        self.instruction = instruction
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", f"{description}\n{instruction}"),
            ("user", "待评审文本：\n{text}\n\n请提供你的结构化评审：")
        ])

    def review(self, text):
        """评审文本并返回结构化反馈"""
        response = llm.invoke(self.system_prompt.format(text=text))
        return response.content

class SequentialAgent:
    """
    顺序智能体：管理生成器和评审者的执行顺序
    """
    def __init__(self, name, generator, reviewer):
        self.name = name
        self.generator = generator
        self.reviewer = reviewer

    def execute(self, topic):
        """执行完整的生成-评审流程"""
        print(f"\n{'='*20} {self.name} {'='*20}")

        # 步骤 1：生成器运行
        print("\n>>> 步骤 1：生成器创建初始内容...")
        draft = self.generator.generate(topic)
        print(f"生成的草稿：\n{draft}\n")

        # 步骤 2：评审者运行
        print(">>> 步骤 2：评审者评估内容质量...")
        review = self.reviewer.review(draft)
        print(f"评审结果：\n{review}\n")

        return {
            "draft": draft,
            "review": review
        }

def main():
    """
    主函数：演示生成器-评审者模式
    """
    # 创建生成器智能体
    generator = GeneratorAgent(
        description="你是一个专业的内容创作者。",
        instruction="撰写关于用户主题的简短、信息丰富的段落。确保内容准确且有价值。"
    )

    # 创建评审者智能体
    reviewer = ReviewerAgent(
        description="你是一个细致的事实核查员和质量评审者。",
        instruction="""
        1. 仔细阅读提供的文本。
        2. 评估事实准确性和内容质量。
        3. 你的最终输出必须是包含两个键的 JSON 格式：
           - "status": 字符串，"ACCURATE" 或 "INACCURATE"
           - "reasoning": 字符串，提供对你的状态的清楚解释，如果发现任何问题则引用具体问题
           - "suggestions": 可选字符串，提供改进建议
        """
    )

    # 创建顺序智能体管道
    pipeline = SequentialAgent(
        name="WriteAndReview_Pipeline",
        generator=generator,
        reviewer=reviewer
    )

    # 执行流程
    topics = [
        "量子计算的基本原理",
        "人工智能在医疗健康领域的应用",
        "气候变化的主要影响因素"
    ]

    results = []
    for topic in topics:
        result = pipeline.execute(topic)
        results.append(result)

    # 汇总结果
    print("\n" + "="*30 + " 结果汇总 " + "="*30)
    for i, (topic, result) in enumerate(zip(topics, results), 1):
        print(f"\n主题 {i}: {topic}")
        print(f"草稿长度: {len(result['draft'])} 字符")
        print(f"评审结果: {result['review'][:100]}...")  # 显示前100个字符

if __name__ == "__main__":
    print("生成器-评审者模式演示：内容质量保证")
    print("="*50)
    main()
