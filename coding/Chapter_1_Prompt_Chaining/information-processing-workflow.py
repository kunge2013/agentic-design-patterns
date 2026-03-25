"""
信息处理工作流示例
演示多步骤信息处理：文本提取、摘要、实体提取、知识库搜索和报告生成
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from llm_config import create_llm

# 初始化语言模型（支持自定义API配置）
try:
    llm = create_llm(temperature=0.7)
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    exit(1)

# --- 步骤 1：文本提取 ---
prompt_extract_text = ChatPromptTemplate.from_template(
    "提取以下文档的正文内容：\n\n{document}"
)

# --- 步骤 2：摘要生成 ---
prompt_summarize = ChatPromptTemplate.from_template(
    "为以下文本生成简洁的摘要：\n\n{text}"
)

# --- 步骤 3：实体提取 ---
prompt_extract_entities = ChatPromptTemplate.from_template(
    "从以下文本中提取关键实体（姓名、日期、位置、组织等）：\n\n{text}"
)

# --- 步骤 4：知识库搜索模拟 ---
prompt_search_knowledge = ChatPromptTemplate.from_template(
    "基于以下实体，生成相关的知识库搜索查询：\n\n{entities}"
)

# --- 步骤 5：报告生成 ---
prompt_generate_report = ChatPromptTemplate.from_template(
    "生成包含以下信息的综合报告：\n"
    "摘要：{summary}\n"
    "实体：{entities}\n"
    "搜索结果：{search_results}\n"
    "报告应该专业、结构化且易于阅读。"
)

# 构建处理链
text_extraction_chain = prompt_extract_text | llm | StrOutputParser()
summarization_chain = prompt_summarize | llm | StrOutputParser()
entity_extraction_chain = prompt_extract_entities | llm | StrOutputParser()
knowledge_search_chain = prompt_search_knowledge | llm | StrOutputParser()

# 完整的信息处理流程
information_processing_chain = (
    {
        "text": text_extraction_chain,
        "document": RunnablePassthrough()
    }
    | {
        "summary": summarization_chain,
        "entities": entity_extraction_chain,
        "text": RunnablePassthrough()
    }
    | {
        "search_results": knowledge_search_chain,
        "summary": lambda x: x["summary"],
        "entities": lambda x: x["entities"]
    }
    | prompt_generate_report
    | llm
    | StrOutputParser()
)

# --- 运行示例 ---
sample_document = """
2024年3月15日，苹果公司在加利福尼亚州库比蒂诺总部举行了年度产品发布会。
CEO蒂姆·库克宣布了新一代的iPhone产品线，带来了多项创新功能。
该产品将于2024年9月正式发布，预计售价为999美元起。
"""

print("--- 信息处理工作流 ---")
final_report = information_processing_chain.invoke({"document": sample_document})
print(final_report)
