"""
代码生成和完善示例
演示多步骤代码开发：理解需求、生成代码、错误检查和完善
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict
import json
from llm_config import create_llm

# 初始化语言模型（支持自定义API配置）
try:
    llm_coding = create_llm(model="qwen-plus", temperature=0.2)  # 使用qwen-plus用于代码生成
    llm_review = create_llm(model="qwen-plus", temperature=0.1)  # 低温用于一致性代码审查
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    print("提示：代码生成推荐使用qwen-plus，如果没有访问权限，请修改model参数")
    exit(1)

# --- 步骤 1：需求理解和大纲生成 ---
prompt_understand_requirement = ChatPromptTemplate.from_template(
    "分析以下代码需求并生成实现大纲：\n\n{requirement}\n\n"
    "返回JSON格式：\n"
    "{{\n"
    "  'understanding': '需求理解摘要',\n"
    "  'function_name': '建议的函数名',\n"
    "  'input_spec': '输入参数说明',\n"
    "  'output_spec': '输出说明',\n"
    "  'key_components': ['关键组件列表'],\n"
    "  'implementation_outline': ['实现步骤']\n"
    "}}"
)

# --- 步骤 2：初始代码生成 ---
prompt_generate_code = ChatPromptTemplate.from_template(
    "基于以下大纲生成Python代码：\n\n{outline}\n\n"
    "要求：\n"
    "- 实现完整的函数\n"
    "- 包含适当的错误处理\n"
    "- 添加类型注解\n"
    "- 包含基本的使用示例\n"
    "- 代码应该清晰、可维护\n\n"
    "只返回代码，不要解释。"
)

# --- 步骤 3：代码审查 ---
prompt_review_code = ChatPromptTemplate.from_template(
    "审查以下Python代码的质量：\n\n```python\n{code}\n```\n\n"
    "检查：\n"
    "- 语法错误\n"
    "- 逻辑错误\n"
    "- 潜在的bug\n"
    "- 性能问题\n"
    "- 代码风格问题\n"
    "- 缺失的错误处理\n"
    "- 类型安全问题\n\n"
    "返回JSON格式：\n"
    "{{\n"
    "  'has_issues': true/false,\n"
    "  'critical_issues': ['严重问题列表'],\n"
    "  'improvements': ['改进建议列表'],\n"
    "  'overall_score': 1-10\n"
    "}}"
)

# --- 步骤 4：代码完善 ---
prompt_refine_code = ChatPromptTemplate.from_template(
    "完善以下Python代码：\n\n```python\n{original_code}\n```\n\n"
    "需要解决的问题：\n{issues}\n\n"
    "改进建议：\n{improvements}\n\n"
    "提供完善后的代码，解决所有指出的问题。"
)

# --- 步骤 5：文档和测试生成 ---
prompt_generate_docs_tests = ChatPromptTemplate.from_template(
    "为以下代码生成文档和测试：\n\n```python\n{code}\n```\n\n"
    "生成：\n"
    "1. 完整的函数文档字符串（docstring），包含：\n"
    "   - 功能描述\n"
    "   - 参数说明\n"
    "   - 返回值说明\n"
    "   - 异常说明\n"
    "   - 使用示例\n\n"
    "2. 单元测试代码（使用unittest）\n\n"
    "返回完整版本的代码（包含文档和测试）。"
)

def code_development_pipeline(requirement: str, max_iterations: int = 2) -> Dict:
    """完整的代码开发流程"""

    print("="*80)
    print("代码开发流程")
    print("="*80)

    result = {
        "requirement": requirement,
        "iterations": []
    }

    # 步骤 1：理解需求
    print("\n--- 步骤 1：需求分析 ---")
    understand_chain = prompt_understand_requirement | llm_coding | StrOutputParser()
    outline_text = understand_chain.invoke({"requirement": requirement})

    try:
        outline = json.loads(outline_text)
    except json.JSONDecodeError:
        outline = {"implementation_outline": ["根据需求实现功能"]}

    print(f"理解：{outline.get('understanding', 'N/A')}")
    print(f"函数名：{outline.get('function_name', 'N/A')}")

    # 步骤 2：生成初始代码
    print("\n--- 步骤 2：初始代码生成 ---")
    code_gen_chain = prompt_generate_code | llm_coding | StrOutputParser()
    current_code = code_gen_chain.invoke({"outline": json.dumps(outline, ensure_ascii=False)})

    print("生成的代码：")
    print(current_code[:500] + "..." if len(current_code) > 500 else current_code)

    # 步骤 3-4：代码审查和完善循环
    for iteration in range(max_iterations):
        print(f"\n--- 步骤 3-4：代码审查和完善（迭代 {iteration + 1}）---")

        # 代码审查
        review_chain = prompt_review_code | llm_review | StrOutputParser()
        review_text = review_chain.invoke({"code": current_code})

        try:
            review = json.loads(review_text)
        except json.JSONDecodeError:
            review = {"has_issues": False, "critical_issues": [], "improvements": []}

        print(f"是否有问题：{review.get('has_issues', False)}")
        print(f"整体评分：{review.get('overall_score', 'N/A')}/10")

        if review.get("critical_issues"):
            print(f"严重问题：{review.get('critical_issues', [])}")

        if review.get("improvements"):
            print(f"改进建议：{review.get('improvements', [])[:3]}...")

        # 记录迭代结果
        result["iterations"].append({
            "iteration": iteration + 1,
            "review": review,
            "code": current_code
        })

        # 如果没有问题，跳出循环
        if not review.get("has_issues", False) or iteration == max_iterations - 1:
            break

        # 完善代码
        refine_chain = prompt_refine_code | llm_coding | StrOutputParser()
        current_code = refine_chain.invoke({
            "original_code": current_code,
            "issues": json.dumps(review.get("critical_issues", []), ensure_ascii=False),
            "improvements": json.dumps(review.get("improvements", []), ensure_ascii=False)
        })

        print("完善后的代码：")
        print(current_code[:500] + "..." if len(current_code) > 500 else current_code)

    # 步骤 5：生成文档和测试
    print("\n--- 步骤 5：文档和测试生成 ---")
    docs_tests_chain = prompt_generate_docs_tests | llm_coding | StrOutputParser()
    final_code = docs_tests_chain.invoke({"code": current_code})

    result["final_code"] = final_code

    print("\n--- 最终代码（带文档和测试）---")
    print(final_code)

    return result

# --- 运行示例 ---
if __name__ == "__main__":
    requirement = """
    编写一个Python函数，用于计算两个日期之间的工作日数量。
    函数应该：
    - 接受两个日期作为参数（可以是字符串或datetime对象）
    - 忽略周末（周六和周日）
    - 可以接受可选的节假日列表
    - 返回工作日数量
    - 包含适当的错误处理
    """

    development_result = code_development_pipeline(requirement)

    print("\n" + "="*80)
    print("开发完成！")
    print(f"总迭代次数：{len(development_result['iterations'])}")
    print("="*80)
