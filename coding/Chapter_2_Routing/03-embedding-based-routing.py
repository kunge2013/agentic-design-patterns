"""
嵌入式路由示例
演示如何使用向量嵌入和语义相似性进行路由
"""
from typing import List, Dict, Optional
import numpy as np

# 模拟嵌入生成（在实际应用中，使用OpenAI、HuggingFace等的嵌入模型）
def mock_embedding(text: str) -> np.ndarray:
    """
    模拟文本嵌入生成
    注意：这是一个简化的实现，仅用于演示
    在实际应用中，应使用真实的嵌入模型
    """
    # 使用字符编码的简单哈希来生成模拟向量
    embedding = np.zeros(128, dtype=np.float32)
    for i, char in enumerate(text.lower()):
        idx = ord(char) % 128
        embedding[idx] += 1.0 / (i + 1)

    # 归一化
    norm = np.linalg.norm(embedding)
    if norm > 0:
        embedding = embedding / norm

    return embedding


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    计算余弦相似度

    Args:
        a, b: 嵌入向量

    Returns:
        相似度分数（0-1之间）
    """
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# --- 定义路由目标 ---
class RoutingTarget:
    """路由目标类"""

    def __init__(
        self,
        name: str,
        description: str,
        example_queries: List[str],
        handler: callable
    ):
        self.name = name
        self.description = description
        self.example_queries = example_queries
        self.handler = handler
        self.embedding = self._compute_average_embedding()

    def _compute_average_embedding(self) -> np.ndarray:
        """计算示例查询的平均嵌入"""
        embeddings = [mock_embedding(q) for q in self.example_queries]
        return np.mean(embeddings, axis=0)


# --- 定义处理程序 ---
def booking_handler(request: str) -> str:
    """处理预订请求"""
    return f"✈️ 预订处理程序: '{request}' - 已模拟预订操作"


def info_handler(request: str) -> str:
    """处理信息查询"""
    return f"ℹ️ 信息处理程序: '{request}' - 已模拟信息检索"


def tech_support_handler(request: str) -> str:
    """处理技术支持"""
    return f"🔧 技术支持: '{request}' - 已模拟技术支持"


def general_handler(request: str) -> str:
    """处理一般请求"""
    return f"💬 一般处理程序: '{request}' - 已模拟一般处理"


# --- 创建路由目标 ---
routing_targets = [
    RoutingTarget(
        name="booking",
        description="处理航班和酒店预订",
        example_queries=[
            "预订航班",
            "book a hotel",
            "预定机票",
            "make reservation",
            "预订房间",
            "航班预订"
        ],
        handler=booking_handler
    ),
    RoutingTarget(
        name="tech_support",
        description="处理技术问题和故障排除",
        example_queries=[
            "系统故障",
            "无法登录",
            "密码错误",
            "系统崩溃",
            "技术支持",
            "help me"
        ],
        handler=tech_support_handler
    ),
    RoutingTarget(
        name="info",
        description="回答事实性问题",
        example_queries=[
            "什么是人工智能",
            "首都",
            "最高山",
            "事实",
            "信息查询",
            "告诉我"
        ],
        handler=info_handler
    ),
]


# --- 定义嵌入路由器 ---
class EmbeddingRouter:
    """基于嵌入的路由器"""

    def __init__(self, targets: List[RoutingTarget], threshold: float = 0.5):
        self.targets = targets
        self.threshold = threshold

    def route(self, request: str, verbose=True) -> tuple[str, float]:
        """
        路由请求到最相似的目标

        Args:
            request: 用户请求
            verbose: 是否显示详细信息

        Returns:
            (目标名称, 相似度分数)
        """
        # 计算请求的嵌入
        request_embedding = mock_embedding(request)

        # 计算与所有目标的相似度
        similarities = []
        for target in self.targets:
            similarity = cosine_similarity(request_embedding, target.embedding)
            similarities.append((target.name, similarity))

        # 按相似度排序
        similarities.sort(key=lambda x: x[1], reverse=True)

        if verbose:
            print(f"\n[嵌入路由器] 收到请求: '{request}'")
            print(f"[嵌入路由器] 目标相似度分析:")
            for name, score in similarities:
                print(f"  - {name}: {score:.3f}")

        # 返回最相似的目标
        best_match = similarities[0]
        return best_match

    def route_and_execute(self, request: str) -> str:
        """
        路由并执行请求

        Args:
            request: 用户请求

        Returns:
            处理结果
        """
        target_name, similarity = self.route(request)

        # 找到对应的目标
        target = next((t for t in self.targets if t.name == target_name), None)

        if target and similarity >= self.threshold:
            return target.handler(request)
        else:
            return general_handler(request)


# --- 示例用法 ---
def main():
    print("=" * 60)
    print("嵌入式路由示例")
    print("=" * 60)

    # 创建路由器
    router = EmbeddingRouter(routing_targets, threshold=0.3)

    # 显示可用的路由目标
    print("\n可用的路由目标:")
    for target in routing_targets:
        print(f"  - {target.name}: {target.description}")

    # 测试用例
    test_requests = [
        "我想预订一张去上海的机票",
        "我的账户登录不了",
        "世界上最高的山是什么",
        "告诉我一些关于人工智能的信息",
        "系统总是崩溃怎么办",
        "想要预定一间酒店房间"
    ]

    print(f"\n共有 {len(test_requests)} 个测试请求\n")

    for i, request in enumerate(test_requests, 1):
        print(f"\n{i}. {'-' * 50}")
        print(f"测试请求: {request}")
        print(f"{'-' * 50}")

        # 路由并执行
        result = router.route_and_execute(request)
        print(f"\n最终结果: {result}")

if __name__ == "__main__":
    main()
