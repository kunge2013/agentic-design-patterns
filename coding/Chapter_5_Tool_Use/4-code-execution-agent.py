#!/usr/bin/env python3
"""
基于 LangChain 的代码执行工具示例

这个示例展示了如何实现代码执行工具，
让智能体能够在安全的环境中运行代码片段。

智能体能够：
1. 编写和执行 Python 代码
2. 进行精确的数学计算
3. 处理数据分析任务
4. 在沙盒环境中安全执行代码

范式：工具使用模式（代码执行）
"""

import os
import getpass
from typing import Any, Dict
from dotenv import load_dotenv
import logging
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_agent
import httpx

# 禁用代理，避免代理配置问题
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

# --- 配置 ---
load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 安全地设置 API 密钥
if not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

# 使用 .env 中的配置
model_name = os.getenv("OPENAI_MODEL", "qwen-plus")
api_url = os.getenv("OPENAI_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

try:
    llm = ChatOpenAI(
        model=model_name,
        temperature=0.2,
        base_url=api_url if api_url else None
    )
    print(f"✅ 语言模型已初始化：{llm.model}")
except Exception as e:
    print(f"🛑 初始化语言模型时出错：{e}")
    llm = None

# --- 1. 安全代码执行工具 ---
def _execute_python_code_internal(code: str) -> Dict[str, Any]:
    """
    在安全的沙盒环境中执行 Python 代码并返回结果。
    支持基本的数学计算、数据处理和简单的操作。
    """
    logging.info(f"工具调用：execute_python_code，代码长度：{len(code)} 字符")

    # 创建受限的执行环境
    safe_globals = {
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "sum": sum,
            "max": max,
            "min": min,
            "abs": abs,
            "round": round,
            "sorted": sorted,
            "enumerate": enumerate,
            "zip": zip,
        },
        "math": __import__("math"),
        "statistics": __import__("statistics"),
    }

    result = {
        "success": False,
        "output": None,
        "error": None,
        "code": code
    }

    try:
        # 使用 exec 执行代码
        exec(code, safe_globals)

        # 尝试获取输出变量
        if "output" in safe_globals:
            output_value = safe_globals["output"]
            try:
                json.dumps(output_value)  # 测试是否可可序列化
                result["output"] = output_value
            except TypeError:
                result["output"] = str(output_value)

            result["success"] = True
        else:
            result["error"] = "代码未定义 'output' 变量"
            result["success"] = False

    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result

# 创建工具包装
execute_python_code = langchain_tool(_execute_python_code_internal)

# --- 2. 数学计算工具 ---
def _calculate_math_internal(expression: str) -> Dict[str, Any]:
    """
    计算数学表达式并返回结果。
    支持基本的数学运算和常见数学函数。
    """
    logging.info(f"工具调用：calculate_math，表达式：{expression}")

    import math
    safe_math_dict = {
        "math": math,
        "sqrt": math.sqrt,
        "pow": pow,
        "abs": abs,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
    }

    result = {
        "expression": expression,
        "result": None,
        "error": None,
        "success": False
    }

    try:
        # 使用 eval 计算数学表达式
        calculation_result = eval(expression, {"__builtins__": {}}, safe_math_dict)
        result["result"] = calculation_result
        result["success"] = True
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result

calculate_math = langchain_tool(_calculate_math_internal)

# --- 3. 数据分析工具 ---
@langchain_tool
def analyze_statistics(data: Any) -> Dict[str, Any]:
    """
    对数值数据集进行统计分析。
    计算平均值、中位数、标准差、最大值、最小值等统计指标。
    """
    logging.info(f"工具调用：analyze_statistics，数据类型：{type(data)}")

    # 确保数据是数值列表
    if isinstance(data, list):
        numeric_data = [float(x) for x in data if isinstance(x, (int, float))]
    else:
        return {
            "error": "输入必须是数值列表",
            "success": False
        }

    if not numeric_data:
        return {
            "error": "数据列表不能为空或包含无效数值",
            "success": False
        }

    import statistics

    try:
        result = {
            "data_count": len(numeric_data),
            "mean": round(statistics.mean(numeric_data), 4),
            "median": round(statistics.median(numeric_data), 4),
            "std_dev": round(statistics.stdev(numeric_data), 4) if len(numeric_data) > 1 else 0,
            "variance": round(statistics.variance(numeric_data), 4) if len(numeric_data) > 1 else 0,
            "min": min(numeric_data),
            "max": max(numeric_data),
            "range": round(max(numeric_data) - min(numeric_data), 4),
            "sum": round(sum(numeric_data), 4),
            "data_sorted": sorted(numeric_data),
            "success": True
        }
        return result
    except Exception as e:
        return {
            "error": f"统计分析失败：{str(e)}",
            "success": False
        }

# --- 4. 文本数据处理工具 ---
@langchain_tool
def process_text_data(text: str, operation: str, **kwargs) -> Dict[str, Any]:
    """
    对文本数据进行处理操作。
    支持的操作：word_count, char_count, split, find_replace, extract_numbers, extract_words。
    """
    logging.info(f"工具调用：process_text_data，操作：{operation}")

    result = {
        "original_length": len(text),
        "operation": operation,
        "result": None,
        "error": None,
        "success": False
    }

    try:
        if operation == "word_count":
            words = text.split()
            result["result"] = len(words)
            result["success"] = True

        elif operation == "char_count":
            result["result"] = len(text.replace(" ", "").replace("\n", ""))
            result["success"] = True

        elif operation == "extract_numbers":
            import re
            numbers = re.findall(r'\d+\.?\d*', text)
            result["result"] = [float(num) for num in numbers]
            result["success"] = True

        elif operation == "extract_words":
            import re
            words = re.findall(r'\b\w+\b', text.lower())
            result["result"] = words
            result["unique_words"] = list(set(words))
            result["success"] = True

        else:
            result["error"] = f"不支持的操作：{operation}"

    except Exception as e:
        result["error"] = str(e)
        result["success"] = False

    return result

# 创建工具列表
tools = [
    execute_python_code,
    calculate_math,
    analyze_statistics,
    process_text_data
]

# --- 创建代码执行智能体 ---
if llm:
    system_prompt = """你是一个强大的计算和数据分析助手，你可以：
        1. 编写和执行 Python 代码
        2. 进行数学计算
        3. 对数据进行统计分析
        4. 分析文本数据

        在回答问题时，请使用适当的工具进行精确计算和分析。
        对于计算任务，优先使用代码执行工具以确保准确性。"""

    agent = create_agent(
        llm,
        tools,
        system_prompt=system_prompt
    )

def run_code_execution_queries():
    """
    运行代码执行查询示例
    """
    if not llm:
        print("🛑 语言模型未初始化，跳过代码执行查询")
        return None

    queries = [
        "编写 Python 代码计算 1 到 100 的和",
        "计算 sin(45°) + cos(45°) 的值",
        "对数据集 [12, 15, 18, 22, 25, 28, 30] 进行统计分析",
        "从文本 '价格是$99.99, 另一个价格是$199.50' 中提取所有数字"
    ]

    print("\n" + "="*40 + " 代码执行查询 " + "="*40)

    for query in queries:
        print(f"\n💻 查询：{query}")
        try:
            response = agent.invoke({"messages": [("user", query)]})
            last_message = response["messages"][-1]
            if hasattr(last_message, 'content'):
                print(f"📊 结果：{last_message.content}")
            else:
                print(f"📊 结果：{last_message}")
        except Exception as e:
            print(f"🛑 查询出错：{e}")
        print("-" * 40)

def demonstrate_code_execution_capabilities():
    """
    演示代码执行工具的能力
    """
    print("\n" + "="*40 + " 代码执行能力演示 " + "="*40)

    # 演示 Python 代码执行
    print("\n🐍 测试 Python 代码执行")
    code = """
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
squares = [x**2 for x in data]
output = {
    "original": data,
    "squares": squares,
    "sum_squares": sum(squares),
    "average": sum(data) / len(data)
}
"""
    result = _execute_python_code_internal(code)
    print(f"✅ 代码执行结果：{result}")

    # 演示数学计算
    print("\n🔢 测试数学计算")
    math_expr = "math.sqrt(16) + pow(2, 3)"
    result = _calculate_math_internal(math_expr)
    print(f"✅ 计算结果：{result}")

    # 演示统计分析
    print("\n📈 测试统计分析")
    test_data = [23, 45, 67, 89, 34, 56, 78, 12, 90, 45]
    result = _analyze_statistics_internal(test_data)
    print(f"✅ 统计分析结果：{json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    print("代码执行智能体演示")
    print("="*50)

    # 演示基础功能
    demonstrate_code_execution_capabilities()

    # 运行代码执行查询
    run_code_execution_queries()
