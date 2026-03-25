"""
基础 Prompt Chaining 示例
演示使用 LangChain 构建简单的两步链：信息提取和JSON转换
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import create_llm, get_default_llm_config

# 初始化语言模型（支持自定义API配置）
# 通过环境变量配置：
# export OPENAI_API_KEY="your-api-key"
# export OPENAI_API_URL="https://your-api-endpoint"  # 可选，默认为OpenAI
# export OPENAI_MODEL="gpt-3.5-turbo"  # 可选
# export OPENAI_TEMPERATURE="0"  # 可选

# 也可以直接指定配置：
# llm = create_llm(
#     api_key="your-api-key",
#     api_url="https://your-api-endpoint",
#     model="your-model",
#     temperature=0
# )

try:
    llm = create_llm(temperature=0)
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    print("\n请配置环境变量：")
    print("  export OPENAI_API_KEY='your-api-key'")
    print("  export OPENAI_API_URL='https://your-api-endpoint'  # 可选")
    exit(1)

# --- 提示词 1：提取信息 ---
prompt_extract = ChatPromptTemplate.from_template(
    "从以下文本中提取技术规格：\n\n{text_input}"
)

# --- 提示词 2：转换为 JSON ---
prompt_transform = ChatPromptTemplate.from_template(
    "将以下规格转换为 JSON 对象，使用 'cpu'、'memory' 和 'storage' 作为键：\n\n{specifications}"
)

# --- 利用 LCEL 构建处理链 ---
# StrOutputParser() 将 LLM 的消息输出转换为简单字符串。
extraction_chain = prompt_extract | llm | StrOutputParser()

# 完整的链将提取链的输出传递到转换提示词的 'specifications' 变量中。
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

# --- 运行链 ---
input_text = "新款笔记本电脑型号配备 3.5 GHz 八核处理器、16GB 内存和 1TB NVMe 固态硬盘。"

print("\n=== 基础 Prompt Chaining 示例 ===")
print(f"输入文本: {input_text}\n")

# 使用输入文本字典执行链。
final_result = full_chain.invoke({"text_input": input_text})

print("\n--- 最终 JSON 输出 ---")
print(final_result)
print("\n=== 示例完成 ===")
