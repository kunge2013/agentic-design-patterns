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

# 完整的信息处理流程（分步执行更清晰）
def process_information(document: str) -> str:
    """执行完整的信息处理流程"""

    print("步骤 1：文本提取")
    text = (prompt_extract_text | llm | StrOutputParser()).invoke({"document": document})
    print(f"提取的文本（前100字）：{text[:100]}...\n")

    print("步骤 2：摘要生成")
    summary = (prompt_summarize | llm | StrOutputParser()).invoke({"text": text})
    print(f"摘要：{summary}\n")

    print("步骤 3：实体提取")
    entities = (prompt_extract_entities | llm | StrOutputParser()).invoke({"text": text})
    print(f"实体：{entities}\n")

    print("步骤 4：知识库搜索")
    search_results = (prompt_search_knowledge | llm | StrOutputParser()).invoke({"entities": entities})
    print(f"搜索结果：{search_results}\n")

    print("步骤 5：生成报告")
    report = (prompt_generate_report | llm | StrOutputParser()).invoke({
        "summary": summary,
        "entities": entities,
        "search_results": search_results
    })

    return report

# --- 运行示例 ---
sample_document = """
2024年3月15日，苹果公司在加利福尼亚州库比蒂诺总部举行了年度产品发布会。
CEO蒂姆·库克宣布了新一代的iPhone产品线，带来了多项创新功能。
该产品将于2024年9月正式发布，预计售价为999美元起。
"""

print("--- 信息处理工作流 ---")
final_report = process_information(sample_document)
print(final_report)
