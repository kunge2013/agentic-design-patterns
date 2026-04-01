"""
1_顺序交接模式
演示多个智能体按顺序处理任务，每个智能体将输出传递给下一个智能体

应用场景：
- 文档处理工作流（提取 -> 分析 -> 汇总）
- 数据流水线（收集 -> 清洗 -> 转换）
- 代码生成（需求分析 -> 设计 -> 编码）
"""
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import sys
import os

# 添加父目录到路径以导入配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_config import create_llm


class SequentialAgent:
    """顺序智能体基类"""

    def __init__(self, name: str, role: str, goal: str, llm: ChatOpenAI):
        self.name = name
        self.role = role
        self.goal = goal
        self.llm = llm
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", f"你是一个{role}。你的目标是：{goal}"),
            ("human", "{input}")
        ])
        # 使用现代LangChain LCEL方式
        self.chain = self.prompt_template | llm

    def process(self, input_text: str) -> str:
        """处理输入并返回输出"""
        print(f"\n[{self.name}] 正在处理...")
        result = self.chain.invoke({"input": input_text})
        result_text = result.content if hasattr(result, 'content') else str(result)
        print(f"[{self.name}] 输出: {result_text[:100]}...")
        return result_text


def sequential_handover_example():
    """顺序交接示例：创建一个技术博客文章"""

    print("=== 顺序交接模式示例：技术博客创建 ===\n")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 定义三个顺序智能体
    # 第一步：研究员 - 收集信息
    researcher = SequentialAgent(
        name="研究员",
        role="研究专家",
        goal="收集并整理关于指定主题的关键信息",
        llm=llm
    )

    # 第二步：分析师 - 分析信息
    analyst = SequentialAgent(
        name="分析师",
        role="技术分析师",
        goal="深入分析研究信息，提取关键见解和趋势",
        llm=llm
    )

    # 第三步：作家 - 撰写博客
    writer = SequentialAgent(
        name="作家",
        role="技术博客作家",
        goal="将分析结果转化为引人入胜的技术博客文章",
        llm=llm
    )

    # 初始输入
    topic = "Python异步编程的发展与最佳实践"
    print(f"初始主题: {topic}\n")

    # 顺序处理
    research_output = researcher.process(topic)

    analysis_output = analyst.process(f"研究主题：{topic}\n\n研究发现：\n{research_output}")

    final_blog = writer.process(f"分析结果：\n{analysis_output}\n\n请基于以上分析撰写一篇结构完整的技术博客文章。")

    print("\n" + "="*50)
    print("最终输出：技术博客文章")
    print("="*50)
    print(final_blog)


def sequential_data_pipeline_example():
    """数据流水线示例：客户反馈分析"""

    print("\n\n=== 顺序数据流水线示例：客户反馈分析 ===\n")

    # 创建LLM
    llm = create_llm(temperature=0.5)

    # 定义流水线智能体
    # 第一步：提取 - 提取关键信息
    extractor = SequentialAgent(
        name="提取器",
        role="信息提取专家",
        goal="从客户反馈中提取关键信息，包括问题类型、严重程度、具体描述",
        llm=llm
    )

    # 第二步：分类 - 分类问题
    classifier = SequentialAgent(
        name="分类器",
        role="问题分类专家",
        goal="将提取的问题信息分类到合适的类别（如：功能缺陷、性能问题、用户体验等）",
        llm=llm
    )

    # 第三步：优先级 - 确定处理优先级
    prioritizer = SequentialAgent(
        name="优先级评估器",
        role="优先级评估专家",
        goal="根据问题类型和严重程度，确定处理的优先级和时限",
        llm=llm
    )

    # 模拟客户反馈
    feedback = """
    客户反馈：应用在数据量较大时加载非常慢，有时候甚至超时。
    这严重影响了用户的使用体验，特别是对于我们这种对实时性要求很高的业务场景。
    我们使用的是Chrome浏览器，版本120。
    """

    print(f"原始反馈: {feedback.strip()}\n")

    # 顺序处理
    extracted_info = extractor.process(feedback)

    classified_info = classifier.process(f"提取的信息：\n{extracted_info}")

    final_result = prioritizer.process(f"分类结果：\n{classified_info}")

    print("\n" + "="*50)
    print("最终输出：优先级评估结果")
    print("="*50)
    print(final_result)


if __name__ == "__main__":
    try:
        # 示例1：技术博客创建
        sequential_handover_example()

        # 示例2：数据流水线
        sequential_data_pipeline_example()

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已设置正确的 OPENAI_API_KEY 环境变量")
