#!/usr/bin/env python3
"""
基于 LangChain 的多工具协作智能体示例

这个示例展示了如何创建具有多个工具的智能体，
这些工具可以协同工作来解决复杂任务。

智能体能够：
1. 使用多个相关工具解决复杂问题
2. 在工具之间传递数据
3. 整合多个工具的结果
4. 处理工具调用失败的情况

范式：工具使用模式（多工具协作）
"""

import os
import getpass
from typing import List, Dict
from dotenv import load_dotenv
import logging
import datetime
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

# --- 1. 天气查询工具 ---
@langchain_tool
def get_weather(location: str) -> Dict:
    """
    获取指定位置的当前天气信息。
    返回包含温度、湿度、天气状况的字典。
    """
    logging.info(f"工具调用：get_weather，位置：{location}")

    # 模拟天气数据
    weather_data = {
        "北京": {
            "temperature": 22,
            "humidity": 45,
            "condition": "晴朗",
            "wind_speed": 15,
            "visibility": 10
        },
        "上海": {
            "temperature": 25,
            "humidity": 70,
            "condition": "多云",
            "wind_speed": 12,
            "visibility": 8
        },
        "深圳": {
            "temperature": 28,
            "humidity": 80,
            "condition": "阵雨",
            "wind_speed": 20,
            "visibility": 6
        }
    }

    weather = weather_data.get(location, {
        "temperature": 20,
        "humidity": 50,
        "condition": "未知",
        "wind_speed": 10,
        "visibility": 10
    })

    return weather

# --- 2. 货币转换工具 ---
@langchain_tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict:
    """
    将指定金额从一种货币转换为另一种货币。
    支持的主要货币：USD, EUR, GBP, JPY, CNY。
    """
    logging.info(f"工具调用：convert_currency，{amount} {from_currency} -> {to_currency}")

    # 模拟汇率数据（相对于 USD）
    exchange_rates = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "JPY": 151.3,
        "CNY": 7.24
    }

    try:
        from_rate = exchange_rates[from_currency.upper()]
        to_rate = exchange_rates[to_currency.upper()]

        # 转换为 USD，然后转换为目标货币
        amount_usd = amount / from_rate
        converted_amount = amount_usd * to_rate

        return {
            "original_amount": amount,
            "original_currency": from_currency,
            "converted_amount": round(converted_amount, 2),
            "target_currency": to_currency,
            "exchange_rate": round(to_rate / from_rate, 4),
            "timestamp": datetime.datetime.now().isoformat()
        }
    except KeyError as e:
        return {
            "error": f"不支持的货币代码：{e}",
            "supported_currencies": list(exchange_rates.keys())
        }

# --- 3. 旅行距离计算工具 ---
@langchain_tool
def calculate_distance(city1: str, city2: str, unit: str = "km") -> Dict:
    """
    计算两个城市之间的直线距离。
    单位可以是 'km'（公里）或 'miles'（英里）。
    """
    logging.info(f"工具调用：calculate_distance，{city1} -> {city2}，单位：{unit}")

    # 模拟城市坐标数据（简化版）
    city_coordinates = {
        "北京": (39.9, 116.4),
        "上海": (31.2, 121.5),
        "深圳": (22.5, 114.1),
        "广州": (23.1, 113.3),
        "成都": (30.7, 104.1),
        "西安": (34.3, 108.9)
    }

    if city1 not in city_coordinates or city2 not in city_coordinates:
        return {
            "error": f"不支持的城市位置",
            "supported_cities": list(city_coordinates.keys())
        }

    # 简单的直线距离计算（实际应该使用专业的地理计算库）
    lat1, lon1 = city_coordinates[city1]
    lat2, lon2 = city_coordinates[city2]

    # Haversine 公式的简化版本
    import math
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    distance_km = 6371 * math.sqrt(dlat**2 + dlon**2)

    if unit.lower() == "miles":
        distance = distance_km * 0.621371
        unit_label = "英里"
    else:
        distance = distance_km
        unit_label = "公里"

    return {
        "city1": city1,
        "city2": city2,
        "distance": round(distance, 2),
        "unit": unit_label,
        "coordinates": {
            city1: {"lat": lat1, "lon": lon1},
            city2: {"lat": lat2, "lon": lon2}
        }
    }

# --- 4. 旅行时间估算工具 ---
@langchain_tool
def estimate_travel_time(distance: float, transport_mode: str) -> Dict:
    """
    基于距离和交通方式估算旅行时间。
    交通方式包括：car, train, plane, bus, bicycle。
    """
    logging.info(f"工具调用：estimate_travel_time，{distance}，{transport_mode}")

    # 不同交通方式的平均速度（公里/小时）
    speeds = {
        "car": 80,
        "train": 120,
        "plane": 800,
        "bus": 60,
        "bicycle": 20
    }

    if transport_mode not in speeds:
        return {
            "error": f"不支持的交通方式：{transport_mode}",
            "supported_modes": list(speeds.keys())
        }

    speed = speeds[transport_mode]
    time_hours = distance / speed

    # 转换为小时和分钟
    hours = int(time_hours)
    minutes = int((time_hours - hours) * 60)

    return {
        "distance_km": distance,
        "transport_mode": transport_mode,
        "speed_kmh": speed,
        "travel_time_hours": round(time_hours, 2),
        "travel_time_formatted": f"{hours}小时{minutes}分钟",
        "estimated_arrival": (datetime.datetime.now() +
                             datetime.timedelta(hours=time_hours)).strftime("%Y-%m-%d %H:%M")
    }

# --- 5. 智能旅行建议工具 ---
@langchain_tool
def get_travel_advice(destination: str, budget: float, currency: str) -> str:
    """
    根据目的地、预算和货币提供智能旅行建议。
    这是一些建议性信息，不构成专业旅行建议。
    """
    logging.info(f"工具调用：get_travel_advice，目的地：{destination}，预算：{budget} {currency}")

    # 模拟旅行成本数据（人民币）
    daily_costs = {
        "北京": 600,
        "上海": 800,
        "深圳": 700,
        "广州": 650,
        "成都": 500,
        "西安": 450
    }

    daily_cost = daily_costs.get(destination, 600)

    # 将预算转换为人民币（简化）
    if currency.upper() == "USD":
        budget_cny = budget * 7.24
        budget_str = f"${budget} (约 {budget_cny:.0f}元)"
    else:
        budget_cny = budget
        budget_str = f"{budget}元"

    affordable_days = int(budget_cny / daily_cost)

    advice = f"""
    旅行建议 - {destination}:

    🏷️ 预算分析:
    - 您的预算: {budget_str}
    - 预计每日花费: {daily_cost}元
    - 可负担旅行天数: {affordable_days}天

    💡 旅行建议:
    - 如果预算充足: {'可以享受高端酒店和特色餐厅' if affordable_days > 5 else '建议选择经济型酒店'}
    - 推荐行程: {'至少需要3-4天游览主要景点' if affordable_days >= 3 else '建议增加预算或缩短行程'}
    - 最佳旅行时间: 春秋季节天气宜人，避开节假日

    ⚠️ 温馨提示:
    - 这是模拟数据，实际费用请根据具体情况调整
    - 建议提前规划并预订交通和住宿
    - 注意当地天气和季节性活动
    """

    return advice.strip()

# 创建工具列表
tools = [
    get_weather,
    convert_currency,
    calculate_distance,
    estimate_travel_time,
    get_travel_advice
]

# --- 创建多工具协作智能体 ---
if llm:
    system_prompt = """你是一个智能旅行助手，可以帮助用户：
        1. 查询目的地的天气情况
        2. 进行货币转换和汇率查询
        3. 计算城市间的距离
        4. 估算不同交通方式的旅行时间
        5. 提供旅行建议和预算分析

        在回答问题时，请使用相关工具获取最新信息，并整合多个工具的结果为用户提供全面的旅行规划建议。"""

    agent = create_agent(
        llm,
        tools,
        system_prompt=system_prompt
    )

def run_travel_assistant_queries():
    """
    运行旅行助手查询示例
    """
    if not llm:
        print("🛑 语言模型未初始化，跳过旅行助手查询")
        return None

    queries = [
        "北京现在的天气怎么样？",
        "如果我准备去北京旅行，预算3000美元，能给些建议吗？",
        "从上海到北京的距离是多少？",
        "开车从上海到北京需要多长时间？",
        "我要兑换500美元成人民币，现在的汇率是多少？",
        "帮我规划一个从北京到深圳的旅行，包括交通时间和天气情况"
    ]

    print("\n" + "="*40 + " 智能旅行助手查询 " + "="*40)

    for query in queries:
        print(f"\n🌍 用户查询：{query}")
        try:
            response = agent.invoke({"messages": [("user", query)]})
            last_message = response["messages"][-1]
            if hasattr(last_message, 'content'):
                print(f"🤖 助手回答：{last_message.content}")
            else:
                print(f"🤖 助手回答：{last_message}")
        except Exception as e:
            print(f"🛑 查询出错：{e}")
        print("-" * 40)

def demonstrate_tool_collaboration():
    """
    演示工具之间的协作能力
    """
    print("\n" + "="*40 + " 工具协作演示 " + "="*40)

    # 演示工具链：距离计算 -> 时间估算
    print("\n🔗 工具链演示：距离计算 → 时间估算")
    try:
        # 第一步：计算距离
        distance_result = calculate_distance("上海", "北京", "km")
        print(f"第一步 - 距离：{distance_result}")

        if "distance" in distance_result:
            # 第二步：估算旅行时间
            time_result = estimate_travel_time(distance_result["distance"], "train")
            print(f"第二步 - 旅行时间：{time_result}")
        else:
            print(f"距离计算失败：{distance_result}")
    except Exception as e:
        print(f"工具链执行出错：{e}")

    # 演示多工具数据整合
    print("\n🔗 多工具数据整合演示")
    try:
        # 获取多个数据源
        weather = get_weather("北京")
        distance = calculate_distance("上海", "北京")
        time_estimate = estimate_travel_time(distance["distance"], "car")

        # 整合数据
        integrated_info = {
            "destination": "北京",
            "weather": weather,
            "travel_from_shanghai": {
                "distance": distance,
                "driving_time": time_estimate
            },
            "summary": f"从上海到北京{distance['distance']}公里，开车需要{time_estimate['travel_time_formatted']}。北京当前天气{weather['temperature']}°C，{weather['condition']}。"
        }

        print(f"整合信息：{json.dumps(integrated_info, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"数据整合出错：{e}")

if __name__ == "__main__":
    print("多工具协作智能体演示")
    print("="*50)

    # 演示工具协作
    demonstrate_tool_collaboration()

    # 运行旅行助手查询
    run_travel_assistant_queries()
