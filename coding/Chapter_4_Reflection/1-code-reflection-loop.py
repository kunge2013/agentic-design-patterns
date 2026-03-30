#!/usr/bin/env python3
"""
基于 LangChain 的代码反思循环示例

这个示例展示了如何使用反思模式来迭代改进 Python 代码。
通过生成器-评审者模型，系统能够：
1. 生成初始代码
2. 基于反馈进行反思和改进
3. 重复该过程直到代码满足质量标准

范式：反思模式（生成器-评审者模型）
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

# --- 配置 ---
# 从 .env 文件加载环境变量（用于 OPENAI_API_KEY）
load_dotenv()

# 检查是否设置了 API 密钥
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("在 .env 文件中未找到 OPENAI_API_KEY。请添加它。")

# 初始化聊天 LLM。我们使用 gpt-4o 以获得更好的推理。
# 使用较低的温度以获得更确定性的输出。
llm = ChatOpenAI(model="gpt-4o", temperature=0.1)

def run_reflection_loop():
    """
    演示多步 AI 反思循环以逐步改进 Python 函数。
    """
    # --- 核心任务 ---
    task_prompt = """
    你的任务是创建一个名为 `calculate_factorial` 的 Python 函数。
    此函数应执行以下操作：
    1. 接受单个整数 `n` 作为输入。
    2. 计算其阶乘 (n!)。
    3. 包含清楚解释函数功能的文档字符串。
    4. 处理边缘情况：0 的阶乘是 1。
    5. 处理无效输入：如果输入是负数，则引发 ValueError。
    """

    # --- 反思循环 ---
    max_iterations = 3
    current_code = ""

    # 我们将构建对话历史以在每一步中提供上下文。
    message_history = [HumanMessage(content=task_prompt)]

    for i in range(max_iterations):
        print("\n" + "="*25 + f" 反思循环：迭代 {i + 1} " + "="*25)

        # --- 1. 生成/完善阶段 ---
        # 在第一次迭代中，它生成。在后续迭代中，它完善。
        if i == 0:
            print("\n>>> 阶段 1：生成初始代码...")
            # 第一条消息只是任务提示词。
            response = llm.invoke(message_history)
            current_code = response.content
        else:
            print("\n>>> 阶段 1：基于先前批评完善代码...")
            # 消息历史现在包含任务、
            # 最后一个代码和最后一个批评。
            # 我们指示模型应用批评。
            message_history.append(HumanMessage(content="请使用提供的批评完善代码。"))
            response = llm.invoke(message_history)
            current_code = response.content

        print("\n--- 生成的代码 (v" + str(i + 1) + ") ---\n" + current_code)
        message_history.append(response) # 将生成的代码添加到历史记录

        # --- 2. 反思阶段 ---
        print("\n>>> 阶段 2：对生成的代码进行反思...")
        # 为反思智能体特定提示词。
        # 这要求模型充当高级代码审查员。
        reflector_prompt = [
            SystemMessage(content="""
                你是一名高级软件工程师和 Python 专家。
                你的角色是执行细致的代码审查。
                根据原始任务要求批判性地评估提供的 Python 代码。
                查找错误、风格问题、缺失的边缘情况和改进领域。
                如果代码完美并满足所有要求，
                用单一短语 'CODE_IS_PERFECT' 响应。
                否则，提供批评的项目符号列表。
            """),
            HumanMessage(content=f"原始任务：\n{task_prompt}\n\n要审查的代码：\n{current_code}")
        ]

        critique_response = llm.invoke(reflector_prompt)
        critique = critique_response.content

        # --- 3. 停止条件 ---
        if "CODE_IS_PERFECT" in critique:
            print("\n--- 批评 ---\n未发现进一步批评。代码令人满意。")
            break

        print("\n--- 批评 ---\n" + critique)

        # 将批评添加到历史记录以用于下一个完善循环。
        message_history.append(HumanMessage(content=f"对先前代码的批评：\n{critique}"))

    print("\n" + "="*30 + " 最终结果 " + "="*30)
    print("\n反思过程后的最终精炼代码：\n")
    print(current_code)

def run_simple_reflection():
    """
    更简单的反思示例，展示基本的生成-评审-优化流程
    """
    print("\n" + "="*20 + " 简单反思示例 " + "="*20)

    # --- 生成阶段 ---
    print("\n>>> 生成阶段：创建初始代码")
    generator_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个 Python 开发者。根据用户需求编写代码。"),
        ("user", "创建一个函数来检查一个数字是否为质数。")
    ])

    initial_code = llm.invoke(generator_prompt.format.invoke({})).content
    print(f"生成的代码：\n{initial_code}\n")

    # --- 评审阶段 ---
    print(">>> 评审阶段：分析代码质量")
    reviewer_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个高级代码审查员。评审提供的代码并提供改进建议。"),
        ("user", "评审以下代码：\n{code}")
    ])

    feedback = llm.invoke(reviewer_prompt.format(code=initial_code)).content
    print(f"评审反馈：\n{feedback}\n")

    # --- 优化阶段 ---
    print(">>> 优化阶段：基于反馈改进代码")
    optimizer_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个 Python 开发者。根据反馈改进代码。"),
        ("user", "改进以下代码：\n{code}\n\n反馈：\n{feedback}")
    ])

    improved_code = llm.invoke(optimizer_prompt.format(
        code=initial_code,
        feedback=feedback
    )).content

    print(f"改进后的代码：\n{improved_code}\n")

if __name__ == "__main__":
    print("反思模式演示：代码迭代改进")
    print("="*50)

    # 运行完整的反思循环
    run_reflection_loop()

    # 运行简单的反思示例
    run_simple_reflection()
