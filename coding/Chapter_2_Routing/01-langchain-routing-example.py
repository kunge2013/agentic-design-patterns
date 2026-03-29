"""
LangChain路由示例 - 使用LLM作为路由器
演示如何使用LangChain和RunnableBranch实现智能路由
"""
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch
from llm_config import create_llm
import os

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# --- 初始化LLM ---
try:
    llm = create_llm(temperature=0)  # 使用较低的温度以获得更确定性的输出
    print(f"语言模型已初始化: {llm.model_name}")
except Exception as e:
    print(f"初始化语言模型时出错: {e}")
    llm = None

# --- 定义模拟子智能体处理程序 ---
def booking_handler(request: str) -> str:
    """模拟预订智能体请求"""
    print("\n--- 委托给预订处理程序 ---")
    return f"预订处理程序处理了请求：'{request}'。结果：模拟预订操作。"

def info_handler(request: str) -> str:
    """模拟信息智能体请求"""
    print("\n--- 委托给信息处理程序 ---")
    return f"信息处理程序处理了请求：'{request}'。结果：模拟信息检索。"

def unclear_handler(request: str) -> str:
    """处理无法委托的请求"""
    print("\n--- 处理不清楚的请求 ---")
    return f"协调器无法委托请求：'{request}'。请澄清。"

# --- 定义打印提示词的函数 ---
def print_prompt(messages):
    """打印发送给LLM的提示词内容"""
    print(f"\n{'=' * 60}")
    print("发送给LLM的提示词：")
    print(f"{'=' * 60}")
    for message in messages:
        role = message.role.upper()
        content = message.content
        print(f"\n【{role}】")
        print(f"{content}")
    print(f"{'=' * 60}")
    return messages

# --- 定义协调器路由链 ---
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    ("system", """分析用户的请求并确定哪个专家处理程序应处理它。
     - 如果请求与预订航班或酒店相关，输出 'booker'。
     - 对于所有其他一般信息问题，输出 'info'。
     - 如果请求不清楚或不适合任一类别，输出 'unclear'。
     只输出一个词：'booker'、'info' 或 'unclear'。"""),
    ("user", "{request}")
])

if llm:
    # 创建路由链，在调用LLM之前打印提示词
    coordinator_router_chain = (
        coordinator_router_prompt |
        RunnablePassthrough.assign(debug_prompt=print_prompt) |
        llm |
        StrOutputParser()
    )

# --- 定义委托逻辑 ---
# 使用RunnableBranch根据路由链的输出进行路由
branches = {
    "booker": RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']['request'])),
    "info": RunnablePassthrough.assign(output=lambda x: info_handler(x['request']['request'])),
    "unclear": RunnablePassthrough.assign(output=lambda x: unclear_handler(x['request']['request'])),
}

# 创建RunnableBranch
delegation_branch = RunnableBranch(
    (lambda x: x['decision'].strip() == 'booker', branches["booker"]),
    (lambda x: x['decision'].strip() == 'info', branches["info"]),
    branches["unclear"]  # 默认分支
)

# 组合成单个可运行对象
coordinator_agent = {
    "decision": coordinator_router_chain,
    "request": RunnablePassthrough()
} | delegation_branch | (lambda x: x['output'])

# --- 示例用法 ---
def main():
    if not llm:
        print("\n由于 LLM 初始化失败，跳过执行。")
        return

    print("=" * 60)
    print("LangChain路由示例")
    print("=" * 60)

    # 测试预订请求
    print("\n1. 测试预订请求")
    print("-" * 40)
    request_a = "给我预订去伦敦的航班"
    result_a = coordinator_agent.invoke({"request": request_a})
    print(f"最终结果: {result_a}")

    # 测试信息请求
    print("\n2. 测试信息请求")
    print("-" * 40)
    request_b = "意大利的首都是什么？"
    result_b = coordinator_agent.invoke({"request": request_b})
    print(f"最终结果: {result_b}")

    # 测试不清楚的请求
    print("\n3. 测试不清楚的请求")
    print("-" * 40)
    request_c = "告诉我关于量子物理学的事"
    result_c = coordinator_agent.invoke({"request"  : request_c})
    print(f"最终结果: {result_c}")

    # 额外的测试用例
    print("\n4. 测试酒店预订请求")
    print("-" * 40)
    request_d = "我想在巴黎预订一家酒店"
    result_d = coordinator_agent.invoke({"request": request_d})
    print(f"最终结果: {result_d}")

    print("\n5. 测试一般知识问题")
    print("-" * 40)
    request_e = "世界上最高的山是什么？"
    result_e = coordinator_agent.invoke({"request": request_e})
    print(f"最终结果: {result_e}")

if __name__ == "__main__":
    main()
