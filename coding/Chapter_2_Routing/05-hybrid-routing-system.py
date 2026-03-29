"""
综合路由系统示例
演示如何在实际应用中结合不同的路由策略，构建一个完整的智能路由系统
"""
from typing import Dict, Optional, Tuple
import re
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 尝试导入LLM相关库
try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from llm_config import create_llm
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("警告: LangChain不可用，将仅使用基于规则的路由")

# --- 打印提示词的函数 ---
def print_prompt_debug(messages):
    """打印发送给LLM的提示词内容用于调试"""
    print(f"\n{'=' * 60}")
    print("发送给LLM的提示词（语义路由）：")
    print(f"{'=' * 60}")
    for message in messages:
        role = message.role.upper()
        content = message.content
        print(f"\n【{role}】")
        print(f"{content}")
    print(f"{'=' * 60}")
    return messages

# --- 第一层：快速规则路由（用于明确请求）---
class FastRuleRouter:
    """快速规则路由器 - 处理明确的、高频的请求"""

    def __init__(self):
        self.rules = {
            'booking': [
                r'预订|预定|book|reserve',
                r'航班|机票|酒店|hotel|flight'
            ],
            'support': [
                r'无法|不能|不能|失败|error',
                r'登录|密码|账号|login|password'
            ]
        }

    def route(self, request: str) -> Optional[str]:
        """快速路由，返回意图或None"""
        request_lower = request.lower()

        for intent, patterns in self.rules.items():
            for pattern in patterns:
                if re.search(pattern, request_lower):
                    return intent

        return None


# --- 第二层：LLM语义路由（用于复杂/模糊请求）---
class SemanticRouter:
    """语义路由器 - 使用LLM理解复杂的请求意图"""

    def __init__(self):
        if not LLM_AVAILABLE:
            self.llm = None
            return

        try:
            self.llm = create_llm(temperature=0)
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", """分析用户请求的意图并分类为以下类别之一：
                - booking: 与预订、预定、预约相关
                - support: 与技术支持、故障、问题、帮助相关
                - info: 与信息查询、知识、事实相关
                - unclear: 无法明确分类

                只输出一个词：booking, support, info, 或 unclear"""),
                ("user", "{request}")
            ])
            # 创建路由链，在调用LLM之前打印提示词
            self.chain = (
                self.prompt |
                RunnablePassthrough.assign(debug_prompt=print_prompt_debug) |
                self.llm |
                StrOutputParser()
            )
        except Exception as e:
            print(f"初始化语义路由器失败: {e}")
            self.llm = None

    def route(self, request: str) -> str:
        """语义路由，返回意图"""
        if not self.llm:
            return 'unclear'

        try:
            result = self.chain.invoke({"request": request}).strip().lower()
            # 清理结果
            for intent in ['booking', 'support', 'info', 'unclear']:
                if intent in result:
                    return intent
            return 'unclear'
        except Exception as e:
            print(f"语义路由错误: {e}")
            return 'unclear'


# --- 第三层：详细动作路由（根据意图进行细粒度路由）---
class DetailRouter:
    """详细路由器 - 根据意图进行细粒度路由"""

    @staticmethod
    def route_booking(request: str) -> str:
        """路由预订相关请求"""
        request_lower = request.lower()

        if re.search(r'航班|机票|flight', request_lower):
            return 'flight_booking'
        elif re.search(r'酒店|hotel', request_lower):
            return 'hotel_booking'
        else:
            return 'general_booking'

    @staticmethod
    def route_support(request: str) -> str:
        """路由技术支持相关请求"""
        request_lower = request.lower()

        if re.search(r'登录|login', request_lower):
            return 'login_issue'
        elif re.search(r'密码|password', request_lower):
            return 'password_issue'
        else:
            return 'general_support'

    @staticmethod
    def route_info(request: str) -> str:
        """路由信息查询相关请求"""
        request_lower = request.lower()

        if re.search(r'比较|compare|哪个更好', request_lower):
            return 'comparison'
        elif re.search(r'是什么|what', request_lower):
            return 'fact_query'
        else:
            return 'general_info'


# --- 请求处理程序 ---
class RequestHandler:
    """请求处理器 - 执行具体的业务逻辑"""

    @staticmethod
    def handle(request: str, intent: str, action: str) -> str:
        """处理请求"""
        handlers = {
            'flight_booking': f"✈️ 航班预订: '{request}'",
            'hotel_booking': f"🏨 酒店预订: '{request}'",
            'general_booking': f"📋 预订服务: '{request}'",
            'login_issue': f"🔐 登录支持: '{request}'",
            'password_issue': f"🔑 密码支持: '{request}'",
            'general_support': f"🔧 技术支持: '{request}'",
            'comparison': f"⚖️ 比较分析: '{request}'",
            'fact_query': f"📚 事实查询: '{request}'",
            'general_info': f"ℹ️ 信息服务: '{request}'"
        }

        if action in handlers:
            return handlers[action]
        return f"❓ 通用处理: '{request}' (意图: {intent})"


# --- 综合路由系统 ---
class HybridRouter:
    """混合路由系统 - 结合多种路由策略"""

    def __init__(self):
        self.fast_router = FastRuleRouter()
        self.semantic_router = SemanticRouter() if LLM_AVAILABLE else None
        self.detail_router = DetailRouter()
        self.handler = RequestHandler()

        # 统计信息
        self.stats = {
            'fast_route': 0,
            'semantic_route': 0,
            'fallback': 0
        }

    def route(self, request: str, verbose: bool = True) -> Tuple[str, str, str]:
        """
        路由请求

        Args:
            request: 用户请求
            verbose: 是否显示详细信息

        Returns:
            (intent, action, result)
        """
        if verbose:
            print(f"\n[混合路由] 收到请求: '{request}'")

        # 第一步：尝试快速规则路由
        intent = self.fast_router.route(request)
        if intent:
            self.stats['fast_route'] += 1
            if verbose:
                print(f"  → 快速规则路由匹配: {intent}")
        else:
            # 第二步：使用语义路由
            if self.semantic_router:
                intent = self.semantic_router.route(request)
                self.stats['semantic_route'] += 1
                if verbose:
                    print(f"  → 语义路由分析: {intent}")
            else:
                intent = 'info'  # 默认意图
                self.stats['fallback'] += 1
                if verbose:
                    print(f"  → 使用默认意图: {intent}")

        # 第三步：详细动作路由
        if intent == 'booking':
            action = self.detail_router.route_booking(request)
        elif intent == 'support':
            action = self.detail_router.route_support(request)
        else:  # info 或其他
            action = self.detail_router.route_info(request)

        if verbose:
            print(f"  → 详细动作路由: {action}")

        # 处理请求
        result = self.handler.handle(request, intent, action)

        return intent, action, result

    def print_stats(self):
        """打印路由统计信息"""
        print(f"\n路由统计:")
        print(f"  快速规则路由: {self.stats['fast_route']}")
        print(f"  语义路由: {self.stats['semantic_route']}")
        print(f"  回退处理: {self.stats['fallback']}")


# --- 示例用法 ---
def main():
    print("=" * 60)
    print("综合路由系统示例")
    print("=" * 60)

    if LLM_AVAILABLE:
        print("✓ LLM路由已启用")
    else:
        print("✗ LLM路由未启用（依赖缺失或API未配置）")
    print("✓ 规则路由已启用")

    # 创建路由器
    router = HybridRouter()

    # 测试用例 - 包含不同类型的请求
    test_requests = [
        # 快速规则路由应该能处理的请求
        ("预订一张去北京的机票", "快速规则路由"),
        ("登录不了怎么办", "快速规则路由"),
        ("预定上海酒店", "快速规则路由"),

        # 需要语义路由的请求
        ("我想安排一次旅行", "语义路由"),
        ("系统好像有问题", "语义路由"),
        ("你能帮我了解一下吗", "语义路由"),

        # 边界情况
        ("比较两个产品", "语义路由"),
        ("最高的山是什么", "语义路由"),
        ("忘记密码了", "快速规则路由")
    ]

    print(f"\n共有 {len(test_requests)} 个测试请求\n")

    for i, (request, expected_route) in enumerate(test_requests, 1):
        print(f"\n{'=' * 60}")
        print(f"测试请求 {i}: {request}")
        print(f"预期路由: {expected_route}")
        print(f"{'=' * 60}")

        intent, action, result = router.route(request)
        print(f"\n最终结果: {result}")

    # 显示统计信息
    print("\n" + "=" * 60)
    router.print_stats()
    print("=" * 60)

    # 性能测试
    print("\n性能测试（快速路由10次）:")
    import time
    start_time = time.time()
    for _ in range(10):
        router.route("预订航班", verbose=False)
    end_time = time.time()
    print(f"耗时: {(end_time - start_time) * 100:.2f}ms")


if __name__ == "__main__":
    main()
