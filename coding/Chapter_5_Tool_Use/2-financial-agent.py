#!/usr/bin/env python3
"""
基于 LangChain 的股票查询智能体示例

这个示例展示了如何创建专门的金融分析智能体，
通过工具调用获取股票价格并进行金融分析。

智能体能够：
1. 查询实时股票价格
2. 执行金融计算
3. 提供投资建议

范式：工具使用模式（金融数据分析）
"""

import os
import getpass
from typing import List
from dotenv import load_dotenv
import logging

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

# --- 1. 股票价格查询工具 ---
@langchain_tool
def get_stock_price(ticker: str) -> float:
    """
    获取给定股票代码符号的最新模拟股票价格。
    以浮点数形式返回价格。如果未找到代码，则引发 ValueError。
    """
    logging.info(f"工具调用：get_stock_price，代码为 '{ticker}'")

    simulated_prices = {
        "AAPL": 178.15,
        "GOOGL": 1750.30,
        "MSFT": 425.50,
        "TSLA": 245.67,
        "AMZN": 178.25,
        "META": 358.92,
        "NVDA": 489.78,
        "JPM": 195.43,
    }

    price = simulated_prices.get(ticker.upper())
    if price is not None:
        return price
    else:
        raise ValueError(f"未找到代码 '{ticker.upper()}' 的模拟价格。")

# --- 2. 投资回报率计算工具 ---
@langchain_tool
def calculate_roi(investment_amount: float, current_value: float) -> float:
    """
    计算投资回报率 (ROI)。
    ROI = ((当前价值 - 投资金额) / 投资金额) * 100
    """
    logging.info(f"计算 ROI：投资 {investment_amount}，当前价值 {current_value}")

    if investment_amount == 0:
        raise ValueError("投资金额不能为零")

    roi = ((current_value - investment_amount) / investment_amount) * 100
    return round(roi, 2)

# --- 3. 投资建议生成工具 ---
@langchain_tool
def get_investment_advice(ticker: str, price: float, holding_period: str) -> str:
    """
    基于当前价格和持仓期间提供投资建议。
    这是一个模拟的投资建议工具。
    """
    logging.info(f"生成投资建议：{ticker}，价格 {price}，持仓期 {holding_period}")

    # 模拟投资逻辑
    if price > 400:
        risk_level = "高风险"
        recommendation = "建议谨慎投资，考虑分批建仓"
    elif price > 200:
        risk_level = "中等风险"
        recommendation = "可以适量投资，建议设置止损点"
    else:
        risk_level = "相对较低风险"
        recommendation = "投资价值相对稳定，适合分散投资"

    advice = f"""
    投资建议分析 ({ticker}):
    - 当前价格: ${price}
    - 风险等级: {risk_level}
    - 持仓期间: {holding_period}
    - 建议: {recommendation}
    - 提醒: 这是模拟数据，实际投资请咨询专业金融顾问
    """

    return advice.strip()

# --- 4. 市场情绪分析工具 ---
@langchain_tool
def analyze_market_sentiment(ticker: str) -> str:
    """
    分析给定股票的市场情绪。
    返回市场情绪的简要分析。
    """
    logging.info(f"分析市场情绪：{ticker}")

    # 模拟市场情绪数据
    sentiment_data = {
        "AAPL": "积极 - 最近的财报超预期，新产品发布受到市场欢迎",
        "GOOGL": "中性 - AI业务增长稳定，但面临监管挑战",
        "MSFT": "积极 - 云服务增长强劲，AI集成效果显著",
        "TSLA": "波动 - 市场对电动汽车市场前景看法分化",
    }

    sentiment = sentiment_data.get(ticker.upper(),
                                  "中性 - 市场对该股票前景看法相对平稳")

    return sentiment

# 创建工具列表
tools = [
    get_stock_price,
    calculate_roi,
    get_investment_advice,
    analyze_market_sentiment
]

# --- 创建金融分析智能体 ---
if llm:
    system_prompt = """你是一个专业的金融分析师助手。你可以：
        1. 查询股票价格
        2. 计算投资回报率
        3. 提供投资建议
        4. 分析市场情绪

        在回答用户问题时，请使用适当的工具来获取最新的数据和分析。
        总是提供有数据支撑的准确答案，并提醒用户这是模拟数据。"""

    agent = create_agent(
        llm,
        tools,
        system_prompt=system_prompt
    )

def run_financial_analysis_queries():
    """
    运行金融分析查询示例
    """
    if not llm:
        print("🛑 语言模型未初始化，跳过金融分析查询")
        return None

    queries = [
        "Apple (AAPL) 的当前股票价格是多少？",
        "如果我以 150 美元投资 AAPL，现在价值是 178.15 美元，我的投资回报率是多少？",
        "分析 TSLA 的市场情绪",
        "为 NVDA 提供投资建议，计划长期持有",
        "比较 AAPL 和 MSFT 的投资价值"
    ]

    print("\n" + "="*40 + " 金融分析查询 " + "="*40)

    for query in queries:
        print(f"\n📊 查询：{query}")
        try:
            response = agent.invoke({"messages": [("user", query)]})
            # 获取最后一个消息的内容
            last_message = response["messages"][-1]
            if hasattr(last_message, 'content'):
                print(f"📈 回答：{last_message.content}")
            else:
                print(f"📈 回答：{last_message}")
        except Exception as e:
            print(f"🛑 查询出错：{e}")
        print("-" * 40)

def demonstrate_financial_agent_capabilities():
    """
    演示金融智能体的能力
    """
    print("\n" + "="*40 + " 金融智能体能力演示 " + "="*40)

    # 测试单个工具
    print("\n🧪 测试股票价格查询工具")
    try:
        aapl_price = get_stock_price("AAPL")
        print(f"✅ AAPL 价格: ${aapl_price}")
    except Exception as e:
        print(f"❌ 查询失败: {e}")

    print("\n🧪 测试投资回报率计算")
    try:
        roi = calculate_roi(150.0, 178.15)
        print(f"✅ ROI: {roi}%")
    except Exception as e:
        print(f"❌ 计算失败: {e}")

    print("\n🧪 测试投资建议生成")
    try:
        advice = get_investment_advice("AAPL", 178.15, "长期")
        print(f"✅ 投资建议已生成")
        print(advice)
    except Exception as e:
        print(f"❌ 建议生成失败: {e}")

    print("\n🧪 测试市场情绪分析")
    try:
        sentiment = analyze_market_sentiment("AAPL")
        print(f"✅ 市场情绪: {sentiment}")
    except Exception as e:
        print(f"❌ 分析失败: {e}")

if __name__ == "__main__":
    print("金融分析智能体演示")
    print("="*50)

    # 演示单个工具功能
    demonstrate_financial_agent_capabilities()

    # 运行金融分析查询
    run_financial_analysis_queries()
