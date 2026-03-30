#!/usr/bin/env python3
"""
基于 LangChain 的基础工具使用示例

这个示例展示了如何使用 LangChain 框架实现工具调用。
通过工具调用机制，智能体能够：
1. 定义和描述外部工具
2. 让 LLM 决定何时使用工具
3. 执行工具调用并获取结果
4. 将工具结果整合到最终响应中

范式：工具使用模式（基础实现）
"""

import os
import getpass
import asyncio
import nest_asyncio
from typing import List
from dotenv import load_dotenv
import logging

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# --- 配置 ---
load_dotenv()

# 安全地设置 API 密钥
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

try:
    # 需要具有函数/工具调用能力的模型
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    print(f"✅ 语言模型已初始化：{llm.model}")
except Exception as e:
    print(f"🛑 初始化语言模型时出错：{e}")
    llm = None

# --- 定义工具 ---
@langchain_tool
def search_information(query: str) -> str:
    """提供有关给定主题的事实信息。使用此工具查找诸如"法国首都"或"伦敦的天气？"等短语的答案。
    """
    print(f"\n--- 🛠️ 工具调用：search_information，查询：'{query}' ---")

    # 使用预定义结果字典模拟搜索工具
    simulated_results = {
        "weather in london": "伦敦目前多云，温度为 15°C。",
        "capital of france": "法国的首都是巴黎。",
        "population of earth": "地球的估计人口约为 80 亿人。",
        "tallest mountain": "珠穆朗玛峰是海拔最高的山峰。",
        "default": f"'{query}' 的模拟搜索结果：未找到特定信息，但该主题似乎很有趣。"
    }

    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- 工具结果：{result} ---")
    return result

@langchain_tool
def calculate(expression: str) -> str:
    """计算数学表达式。输入应该是有效的数学表达式，如 '2 + 3 * 4' 或 'sqrt(16)'。
    """
    print(f"\n--- 🛠️ 工具调用：calculate，表达式：'{expression}' ---")

    try:
        # 安全地评估数学表达式
        import math
        # 创建安全的命名空间
        safe_dict = {
            "math": math,
            "sqrt": math.sqrt,
            "pow": pow,
            "abs": abs,
            "round": round,
            "max": max,
            "min": min
        }
        result = eval(expression, {"__builtins__": {}}, safe_dict)
        print(f"--- 计算结果：{result} ---")
        return str(result)
    except Exception as e:
        print(f"--- 计算错误：{e} ---")
        return f"计算错误：{str(e)}"

tools = [search_information, calculate]

# --- 创建工具调用智能体 ---
if llm:
    # 此提示词模板需要一个 `agent_scratchpad` 占位符用于智能体的内部步骤
    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个有用的助手，可以使用搜索和计算工具来回答问题。"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    # 创建智能体，将 LLM、工具和提示词绑定在一起
    agent = create_tool_calling_agent(llm, tools, agent_prompt)

    # AgentExecutor 是调用智能体并执行所选工具的运行时
    agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

async def run_agent_with_tool(query: str):
    """使用查询调用智能体执行器并打印最终响应。"""
    print(f"\n--- 🏃 使用查询运行智能体：'{query}' ---")
    try:
        response = await agent_executor.ainvoke({"input": query})
        print("\n--- ✅ 最终智能体响应 ---")
        print(response["output"])
    except Exception as e:
        print(f"\n🛑 智能体执行期间发生错误：{e}")

async def main():
    """并发运行所有智能体查询。"""
    tasks = [
        run_agent_with_tool("法国的首都是什么？"),
        run_agent_with_tool("伦敦的天气怎么样？"),
        run_agent_with_tool("计算 25 的平方根加上 10 的值"),
        run_agent_with_tool("计算 (5 + 7) * 3 - 2 的结果"),
        run_agent_with_tool("告诉我一些关于狗的事情。")  # 应该触发默认工具响应
    ]
    await asyncio.gather(*tasks)

def demonstrate_tool_calling_flow():
    """
    演示工具调用的完整流程
    """
    print("\n" + "="*40 + " 工具调用流程演示 " + "="*40)

    # 步骤1: 工具定义
    print("\n步骤1: 工具定义")
    print("- 搜索信息工具: search_information")
    print("- 数学计算工具: calculate")
    print(f"已定义工具数量: {len(tools)}")

    # 步骤2: LLM决策
    print("\n步骤2: LLM决策")
    print("- 智能体接收用户请求")
    print("- 分析请求，决定是否需要使用工具")

    # 步骤3: 函数调用生成
    print("\n步骤3: 函数调用生成")
    print("- LLM生成结构化的工具调用请求")
    print("- 指定工具名称和参数")

    # 步骤4: 工具执行
    print("\n步骤4: 工具执行")
    print("- AgentExecutor拦截工具调用请求")
    print("- 使用提供的参数执行实际函数")

    # 步骤5: 观察/结果
    print("\n步骤5: 观察/结果")
    print("- 工具执行的输出返回给智能体")

    # 步骤6: LLM处理
    print("\n步骤6: LLM处理")
    print("- LLM接收工具输出")
    print("- 整合工具结果生成最终响应")

if __name__ == "__main__":
    print("工具使用模式演示：基础实现")
    print("="*50)

    # 演示工具调用流程
    demonstrate_tool_calling_flow()

    if llm:
        nest_asyncio.apply()
        asyncio.run(main())
    else:
        print("\n🛑 由于语言模型初始化失败，跳过智能体执行演示。")
