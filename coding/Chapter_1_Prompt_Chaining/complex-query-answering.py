"""
复杂查询回答示例
演示多步骤推理：问题分解、信息检索和答案综合
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import create_llm

# 初始化语言模型（支持自定义API配置）
try:
    llm = create_llm(temperature=0.3)
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    exit(1)

# --- 步骤 1：问题分解 ---
prompt_decompose = ChatPromptTemplate.from_template(
    "将以下复杂问题分解为核心子问题：\n\n{query}\n\n"
    "请列出子问题和每个子问题的重点。"
)

# --- 步骤 2：子问题 1 研究 ---
prompt_research_causes = ChatPromptTemplate.from_template(
    "研究并详细解释：{subquery_1}\n\n"
    "提供具体的原因、背景信息和影响。"
)

# --- 步骤 3：子问题 2 研究 ---
prompt_research_response = ChatPromptTemplate.from_template(
    "研究并详细解释：{subquery_2}\n\n"
    "提供具体的政策响应、措施和效果。"
)

# --- 步骤 4：答案综合 ---
prompt_synthesize = ChatPromptTemplate.from_template(
    "基于以下信息，综合回答原始问题：{original_query}\n\n"
    "原因分析：\n{causes_research}\n\n"
    "政策响应：\n{response_research}\n\n"
    "提供全面、连贯且逻辑清晰的答案。"
)

# 构建处理链
decompose_chain = prompt_decompose | llm | StrOutputParser()

# --- 运行示例 ---
complex_query = "1929年股市崩盘的主要原因是什么，政府政策如何应对？"

print("--- 复杂查询回答 ---")
print(f"原始问题：{complex_query}\n")

# 首先分解问题
decomposition = decompose_chain.invoke({"query": complex_query})
print("问题分解：")
print(decomposition)
print("\n" + "="*80 + "\n")

# 研究原因
causes_research = (prompt_research_causes | llm | StrOutputParser()).invoke({
    "subquery_1": "1929年股市崩盘的主要原因"
})
print("原因研究：")
print(causes_research)
print("\n" + "="*80 + "\n")

# 研究政策响应
response_research = (prompt_research_response | llm | StrOutputParser()).invoke({
    "subquery_2": "政府如何应对1929年股市崩盘"
})
print("政策响应研究：")
print(response_research)
print("\n" + "="*80 + "\n")

# 综合答案
final_answer = (prompt_synthesize | llm | StrOutputParser()).invoke({
    "original_query": complex_query,
    "causes_research": causes_research,
    "response_research": response_research
})
print("综合答案：")
print(final_answer)
