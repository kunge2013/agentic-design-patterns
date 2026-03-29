"""
多层级路由示例
演示如何构建多层级路由系统，实现复杂的分类和分发逻辑
"""
from typing import Dict, Optional
import re

# --- 第一级：意图分类 ---
class IntentClassifier:
    """意图分类器"""

    def __init__(self):
        self.patterns = {
            'booking': [
                r'预订|预定|book|reserve|make.*?reservation',
                r'航班|机票|酒店|hotel|flight'
            ],
            'support': [
                r'问题|故障|错误|无法|help|support|error',
                r'登录|密码|账号|account|password'
            ],
            'info': [
                r'是什么|什么|怎么|如何|what|how|why',
                r'告诉|告诉我|tell|explain|information'
            ]
        }

    def classify(self, request: str) -> Optional[str]:
        """分类用户请求的意图"""
        request_lower = request.lower()

        for intent, patterns in self.patterns.items():
            for intent_pattern in patterns:
                if re.search(intent_pattern, request_lower):
                    return intent

        return None


# --- 第二级：具体动作分类 ---
class ActionClassifier:
    """动作分类器"""

    @staticmethod
    def classify_booking(request: str) -> str:
        """分类预订相关的具体动作"""
        request_lower = request.lower()

        if re.search(r'航班|机票|flight|airplane', request_lower):
            return 'flight_booking'
        elif re.search(r'酒店|旅馆|hotel|room', request_lower):
            return 'hotel_booking'
        elif re.search(r'座位|票|ticket|seat', request_lower):
            return 'seat_booking'
        else:
            return 'general_booking'

    @staticmethod
    def classify_support(request: str) -> str:
        """分类技术支持相关的具体动作"""
        request_lower = request.lower()

        if re.search(r'登录|登入|login|sign.?in', request_lower):
            return 'login_issue'
        elif re.search(r'密码|password|pwd', request_lower):
            return 'password_issue'
        elif re.search(r'支付|付款|payment|pay', request_lower):
            return 'payment_issue'
        else:
            return 'general_support'

    @staticmethod
    def classify_info(request: str) -> str:
        """分类信息查询相关的具体动作"""
        request_lower = request.lower()

        if re.search(r'首都|capital|city', request_lower):
            return 'fact_query'
        elif re.search(r'比较|对比|compare|which.*?better', request_lower):
            return 'comparison_query'
        elif re.search(r'历史|history|origin', request_lower):
            return 'historical_query'
        else:
            return 'general_info'


# --- 定义最终处理程序 ---
class RequestHandlers:
    """请求处理程序集合"""

    @staticmethod
    def flight_booking_handler(request: str) -> str:
        """处理航班预订"""
        return f"✈️ 航班预订: '{request}' - 已模拟航班预订操作"

    @staticmethod
    def hotel_booking_handler(request: str) -> str:
        """处理酒店预订"""
        return f"🏨 酒店预订: '{request}' - 已模拟酒店预订操作"

    @staticmethod
    def seat_booking_handler(request: str) -> str:
        """处理座位预订"""
        return f"🪑 座位预订: '{request}' - 已模拟座位预订操作"

    @staticmethod
    def general_booking_handler(request: str) -> str:
        """处理一般预订"""
        return f"📋 一般预订: '{request}' - 已模拟预订操作"

    @staticmethod
    def login_issue_handler(request: str) -> str:
        """处理登录问题"""
        return f"🔐 登录问题: '{request}' - 已模拟登录问题排查"

    @staticmethod
    def password_issue_handler(request: str) -> str:
        """处理密码问题"""
        return f"🔑 密码问题: '{request}' - 已模拟密码问题处理"

    @staticmethod
    def payment_issue_handler(request: str) -> str:
        """处理支付问题"""
        return f"💳 支付问题: '{request}' - 已模拟支付问题处理"

    @staticmethod
    def general_support_handler(request: str) -> str:
        """处理一般技术支持"""
        return f"🔧 技术支持: '{request}' - 已模拟技术支持"

    @staticmethod
    def fact_query_handler(request: str) -> str:
        """处理事实查询"""
        return f"📚 事实查询: '{request}' - 已模拟事实查询"

    @staticmethod
    def comparison_query_handler(request: str) -> str:
        """处理比较查询"""
        return f"⚖️ 比较查询: '{request}' - 已模拟比较分析"

    @staticmethod
    def historical_query_handler(request: str) -> str:
        """处理历史查询"""
        return f"📜 历史查询: '{request}' - 已模拟历史信息检索"

    @staticmethod
    def general_info_handler(request: str) -> str:
        """处理一般信息查询"""
        return f"ℹ️ 信息查询: '{request}' - 已模拟信息检索"

    @staticmethod
    def fallback_handler(request: str) -> str:
        """处理无法分类的请求"""
        return f"❓ 通用处理: '{request}' - 无法精确分类，使用通用处理"


# --- 多层级路由器 ---
class MultiLevelRouter:
    """多层级路由器"""

    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.action_classifier = ActionClassifier()
        self.handlers = RequestHandlers()

        # 路由映射表
        self.route_map = {
            'booking': {
                'flight_booking': self.handlers.flight_booking_handler,
                'hotel_booking': self.handlers.hotel_booking_handler,
                'seat_booking': self.handlers.seat_booking_handler,
                'general_booking': self.handlers.general_booking_handler
            },
            'support': {
                'login_issue': self.handlers.login_issue_handler,
                'password_issue': self.handlers.password_issue_handler,
                'payment_issue': self.handlers.payment_issue_handler,
                'general_support': self.handlers.general_support_handler
            },
            'info': {
                'fact_query': self.handlers.fact_query_handler,
                'comparison_query': self.handlers.comparison_query_handler,
                'historical_query': self.handlers.historical_query_handler,
                'general_info': self.handlers.general_info_handler
            }
        }

    def route(self, request: str, verbose: bool = True) -> str:
        """
        多层级路由处理

        Args:
            request: 用户请求
            verbose: 是否显示详细信息

        Returns:
            处理结果
        """
        if verbose:
            print(f"\n[多层级路由] 收到请求: '{request}'")

        # 第一级：意图分类
        intent = self.intent_classifier.classify(request)
        if verbose:
            print(f"[第一级路由] 意图分类: {intent or '未知'}")

        # 如果无法分类意图，使用fallback
        if not intent or intent not in self.route_map:
            if verbose:
                print(f"[路由结果] 使用通用处理")
            return self.handlers.fallback_handler(request)

        # 第二级：动作分类
        if intent == 'booking':
            action = self.action_classifier.classify_booking(request)
        elif intent == 'support':
            action = self.action_classifier.classify_support(request)
        elif intent == 'info':
            action = self.action_classifier.classify_info(request)
        else:
            action = None

        if verbose:
            print(f"[第二级路由] 动作分类: {action or '未知'}")

        # 查找对应的处理程序
        if action and action in self.route_map[intent]:
            handler = self.route_map[intent][action]
            if verbose:
                print(f"[路由结果] 执行: {intent} -> {action}")
            return handler(request)
        else:
            # 使用该意图的默认处理程序
            default_action = f"general_{intent}"
            if default_action in self.route_map[intent]:
                handler = self.route_map[intent][default_action]
                if verbose:
                    print(f"[路由结果] 使用默认处理: {intent} -> {default_action}")
                return handler(request)
            else:
                if verbose:
                    print(f"[路由结果] 使用通用处理")
                return self.handlers.fallback_handler(request)


# --- 示例用法 ---
def main():
    print("=" * 60)
    print("多层级路由示例")
    print("=" * 60)

    # 创建路由器
    router = MultiLevelRouter()

    # 显示路由结构
    print("\n路由器结构:")
    print("  第一级: 意图分类")
    print("    - booking (预订)")
    print("    - support (技术支持)")
    print("    - info (信息查询)")
    print("  第二级: 具体动作分类")
    print("    - 预订: 航班/酒店/座位/一般")
    print("    - 支持: 登录/密码/支付/一般")
    print("    - 信息: 事实/比较/历史/一般")

    # 测试用例
    test_requests = [
        "帮我预订一张去北京的机票",
        "我想在上海预定一家酒店",
        "我的账户登录不了怎么办",
        "忘记了密码，如何重置",
        "支付系统出错了",
        "中国的首都是哪里",
        "比较这两个产品的优缺点",
        "人工智能的历史发展",
        "这是一个无法理解的随机请求"
    ]

    print(f"\n共有 {len(test_requests)} 个测试请求\n")

    for i, request in enumerate(test_requests, 1):
        print(f"\n{'=' * 60}")
        print(f"测试请求 {i}: {request}")
        print(f"{'=' * 60}")

        result = router.route(request)
        print(f"\n最终结果: {result}")

if __name__ == "__main__":
    main()
