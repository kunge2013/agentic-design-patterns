"""
基于规则的路由示例
演示如何使用规则引擎实现快速、确定性的路由
"""
import re
from typing import Dict, Callable, Optional

# --- 定义处理程序 ---
def booking_handler(request: str) -> str:
    """处理预订请求"""
    print(f"\n[路由器] 匹配到预订模式: 预订")
    return f"预订处理程序: '{request}' - 已模拟预订操作"

def info_handler(request: str) -> str:
    """处理信息查询"""
    print(f"\n[路由器] 匹配到信息模式: 信息查询")
    return f"信息处理程序: '{request}' - 已模拟信息检索"

def tech_support_handler(request: str) -> str:
    """处理技术支持"""
    print(f"\n[路由器] 匹配到技术支持模式: 技术支持")
    return f"技术支持处理程序: '{request}' - 已模拟技术支持"

def unclear_handler(request: str) -> str:
    """处理无法分类的请求"""
    print(f"\n[路由器] 无法匹配任何模式: 不清楚")
    return f"抱歉，我不确定如何处理 '{request}'，请提供更多信息。"

# --- 定义路由规则 ---
class RuleBasedRouter:
    """基于规则的路由器"""

    def __init__(self):
        self.rules = []
        self.default_handler = unclear_handler

    def add_rule(self, name: str, pattern: str, handler: Callable):
        """
        添加路由规则

        Args:
            name: 规则名称
            pattern: 正则表达式模式
            handler: 处理函数
        """
        self.rules.append({
            'name': name,
            'pattern': re.compile(pattern, re.IGNORECASE),
            'handler': handler
        })

    def set_default_handler(self, handler: Callable):
        """设置默认处理程序"""
        self.default_handler = handler

    def route(self, request: str) -> str:
        """
        根据规则路由请求

        Args:
            request: 用户请求

        Returns:
            处理结果
        """
        print(f"\n[路由器] 收到请求: '{request}'")

        # 按顺序检查规则
        for rule in self.rules:
            if rule['pattern'].search(request):
                return rule['handler'](request)

        # 没有匹配的规则，使用默认处理程序
        return self.default_handler(request)

    def list_rules(self):
        """列出所有规则"""
        print("\n当前路由规则:")
        for i, rule in enumerate(self.rules, 1):
            print(f"  {i}. {rule['name']}")

# --- 创建路由器并配置规则 ---
router = RuleBasedRouter()

# 添加预订相关规则
router.add_rule(
    name="预订航班",
    pattern=r"(预订|预定|book).*?(航班|飞机|flight)",
    handler=booking_handler
)

router.add_rule(
    name="预订酒店",
    pattern=r"(预订|预定|book).*?(酒店|旅馆|hotel)",
    handler=booking_handler
)

router.add_rule(
    name="座位预订",
    pattern=r"(预订|预定|book).*?(座位|票|ticket|seat)",
    handler=booking_handler
)

# 添加技术支持相关规则
router.add_rule(
    name="技术支持",
    pattern=r"(无法|不能|故障|错误|问题|help|support|error|trouble)",
    handler=tech_support_handler
)

router.add_rule(
    name="账户问题",
    pattern=r"(账户|密码|登录|账号|account|password|login)",
    handler=tech_support_handler
)

# 添加信息查询相关规则
router.add_rule(
    name="事实查询",
    pattern=r"(是什么|是什么|what|where|who|when|which)",
    handler=info_handler
)

router.add_rule(
    name="比较查询",
    pattern=r"(比较|哪个|更好|best|compare)",
    handler=info_handler
)

router.add_rule(
    name="一般问题",
    pattern=r"(怎么|如何|how|为什么|why|tell|explain)",
    handler=info_handler
)

# 设置默认处理程序
router.set_default_handler(unclear_handler)

# --- 示例用法 ---
def main():
    print("=" * 60)
    print("基于规则的路由示例")
    print("=" * 60)

    # 列出当前规则
    router.list_rules()

    # 测试用例
    test_requests = [
        "帮我预订一张去北京的机票",
        "我想在东京预订一家酒店",
        "系统登录不了怎么办",
        "我的密码忘记了",
        "世界上最高的山是什么",
        "如何比较这两个产品",
        "告诉我关于Python的信息",
        "这看起来像是一个完全随机的请求内容"
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
