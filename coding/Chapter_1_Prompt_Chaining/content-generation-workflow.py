"""
内容生成工作流示例
演示多步骤内容创作：主题生成、大纲创建、起草和修订
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import create_llm

# 初始化语言模型（支持自定义API配置）
try:
    llm_creative = create_llm(temperature=0.8)  # 更高的温度用于创意生成
    llm_structure = create_llm(temperature=0.3)  # 较低的温度用于结构化内容
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    exit(1)

# --- 步骤 1：主题生成 ---
prompt_generate_topics = ChatPromptTemplate.from_template(
    "基于用户的兴趣生成5个博客文章主题想法：{interests}\n\n"
    "主题应该是：\n"
    "- 时事相关\n"
    "- 技术性强但易懂\n"
    "- 有实用价值\n\n"
    "以编号列表格式返回主题。"
)

# --- 步骤 2：大纲创建 ---
prompt_create_outline = ChatPromptTemplate.from_template(
    "为以下博客主题创建详细大纲：\n\n{topic}\n\n"
    "大纲应该包含：\n"
    "- 引人注目的标题\n"
    "- 3-5个主要章节\n"
    "- 每个章节的关键点\n"
    "- 结尾总结\n\n"
    "以结构化的 Markdown 格式返回。"
)

# --- 步骤 3：内容起草 ---
prompt_draft_section = ChatPromptTemplate.from_template(
    "根据以下大纲编写博客文章的某个部分：\n\n"
    "主题：{topic}\n"
    "大纲点：{outline_point}\n"
    "上下文（前文）：{previous_context}\n\n"
    "写作风格：\n"
    "- 专业但友好\n"
    "- 技术性强但易懂\n"
    "- 包含实际例子\n\n"
    "编写约200-300字的内容。"
)

# --- 步骤 4：全文审查和完善 ---
prompt_review_refine = ChatPromptTemplate.from_template(
    "审查和完善以下博客文章：\n\n{full_article}\n\n"
    "检查以下方面：\n"
    "- 内容连贯性和逻辑流\n"
    "- 语法和拼写错误\n"
    "- 技术准确性\n"
    "- 可读性和吸引力\n\n"
    "提供改进建议和修改后的完整文章。"
)

def generate_blog_post(interests, selected_topic=None):
    """完整的博客文章生成流程"""

    # 1. 生成主题
    print("--- 步骤 1：生成主题 ---")
    topics_response = prompt_generate_topics | llm_creative | StrOutputParser()
    topics = topics_response.invoke({"interests": interests})
    print(topics)

    # 选择主题（如果未提供）
    if not selected_topic:
        # 简单选择第一个主题
        selected_topic = topics.split('\n')[0].split('. ')[1]
        print(f"\n自动选择主题：{selected_topic}")
    else:
        print(f"\n使用指定主题：{selected_topic}")

    # 2. 创建大纲
    print("\n--- 步骤 2：创建大纲 ---")
    outline_response = prompt_create_outline | llm_structure | StrOutputParser()
    outline = outline_response.invoke({"topic": selected_topic})
    print(outline)

    # 提取大纲点
    import re
    outline_points = re.findall(r'\d+\.\s+(.+)', outline)

    # 3. 逐段起草
    print("\n--- 步骤 3：编写内容 ---")
    sections = []
    previous_context = ""

    for i, point in enumerate(outline_points):
        print(f"编写第 {i+1} 部分：{point[:50]}...")

        draft_response = prompt_draft_section | llm_creative | StrOutputParser()
        section_content = draft_response.invoke({
            "topic": selected_topic,
            "outline_point": point,
            "previous_context": previous_context[-300:] if len(previous_context) > 300 else previous_context
        })

        sections.append(f"## {point}\n\n{section_content}")
        previous_context += f"## {point}\n\n{section_content}\n\n"

    # 组合全文
    full_article = f"# {selected_topic}\n\n" + "\n\n".join(sections)

    # 4. 审查和完善
    print("\n--- 步骤 4：审查和完善 ---")
    review_response = prompt_review_refine | llm_structure | StrOutputParser()
    final_article = review_response.invoke({"full_article": full_article})

    print("\n--- 最终博客文章 ---")
    return final_article

# --- 运行示例 ---
user_interests = "人工智能、机器学习、Python编程、数据科学"
article = generate_blog_post(user_interests)
print(article)
