"""
数据提取和转换示例
演示从非结构化文本到结构化格式的转换，包含验证和改进循环
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from llm_config import create_llm

# 初始化语言模型（支持自定义API配置）
try:
    llm = create_llm(temperature=0)
    llm_creative = create_llm(temperature=0.3)
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    exit(1)

# --- 步骤 1：初始数据提取 ---
prompt_extract_invoice = ChatPromptTemplate.from_template(
    "从以下发票文本中提取以下字段：\n"
    "- 发票编号\n"
    "- 发票日期\n"
    "- 客户姓名\n"
    "- 客户地址\n"
    "- 总金额\n\n"
    "发票文本：\n{invoice_text}\n\n"
    "以JSON格式返回提取的信息。"
)

# --- 步骤 2：数据验证 ---
prompt_validate = ChatPromptTemplate.from_template(
    "验证以下提取的发票数据是否符合要求：\n"
    "- 发票编号：不为空\n"
    "- 发票日期：有效日期格式\n"
    "- 客户姓名：不为空\n"
    "- 客户地址：不为空\n"
    "- 总金额：正数\n\n"
    "提取的数据：\n{extracted_data}\n\n"
    "返回JSON对象，包含：\n"
    "- is_valid: 布尔值\n"
    "- missing_fields: 缺失或无效的字段列表\n"
    "- issues: 具体问题描述列表"
)

# --- 步骤 3：错误修正 ---
prompt_correct = ChatPromptTemplate.from_template(
    "原始发票文本：\n{invoice_text}\n\n"
    "当前提取的数据：\n{extracted_data}\n\n"
    "需要修正的字段：{missing_fields}\n\n"
    "基于原始文本，重新提取缺失的字段并合并到现有数据中。"
    "返回完整的修正后的JSON数据。"
)

# --- 步骤 4：数据规范化 ---
prompt_normalize = ChatPromptTemplate.from_template(
    "规范化以下发票数据：\n\n{data}\n\n"
    "规范化规则：\n"
    "- 日期格式统一为 YYYY-MM-DD\n"
    "- 金额移除货币符号和逗号，转换为数字\n"
    "- 姓名和地址去除多余空格\n\n"
    "返回规范化的JSON数据。"
)

# 构建处理链
json_parser = JsonOutputParser()
str_parser = StrOutputParser()

extraction_chain = prompt_extract_invoice | llm | json_parser
validation_chain = prompt_validate | llm | json_parser
correction_chain = prompt_correct | llm | json_parser
normalization_chain = prompt_normalize | llm | json_parser

def extract_invoice_with_validation(invoice_text, max_attempts=3):
    """带验证的发票提取"""
    print(f"--- 尝试提取发票数据（最多 {max_attempts} 次）---")

    for attempt in range(max_attempts):
        print(f"\n尝试 {attempt + 1}:")

        # 提取数据
        if attempt == 0:
            extracted_data = extraction_chain.invoke({"invoice_text": invoice_text})
        else:
            # 使用修正后的数据
            extracted_data = correction_chain.invoke({
                "invoice_text": invoice_text,
                "extracted_data": extracted_data,
                "missing_fields": validation_result["missing_fields"]
            })

        print(f"提取的数据：{extracted_data}")

        # 验证数据
        validation_result = validation_chain.invoke({"extracted_data": extracted_data})
        print(f"验证结果：{validation_result}")

        if validation_result["is_valid"]:
            print(f"✓ 数据验证通过！")
            break

        if attempt == max_attempts - 1:
            print(f"✗ 达到最大尝试次数，使用当前数据")
            break

    # 数据规范化
    print(f"\n规范化数据...")
    normalized_data = normalization_chain.invoke({"data": extracted_data})
    print(f"规范化后的数据：{normalized_data}")

    return normalized_data

# --- 运行示例 ---
invoice_sample = """
INVOICE
-------
Invoice#: INV-2024-0045
Date: March 15, 2024
Bill To: John Smith
Address: 123 Main Street, New York, NY 10001

Item Description        Qty    Price    Amount
---------------------------------------------------
Web Development       40      $85.00   $3,400.00
Server Setup         5       $120.00  $600.00
Technical Support    10      $95.00   $950.00

Total: $4,950.00
"""

result = extract_invoice_with_validation(invoice_sample)
print("\n--- 最终结果 ---")
print(result)
