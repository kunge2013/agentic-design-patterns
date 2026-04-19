"""
Chapter 12 - 代码示例 2：错误恢复策略 (Error Recovery Strategies)

此示例演示不同的错误恢复策略（重试、回退、降级等）。
"""
import sys
import os
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Callable, Optional, Any
from enum import Enum

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config


class RetryStrategy(Enum):
    """重试策略类型"""
    NO_RETRY = "no_retry"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"


class FallbackStrategy(Enum):
    """回退策略类型"""
    NO_FALLBACK = "no_fallback"
    CACHED_VALUE = "cached_value"
    SIMPLIFIED_OPERATION = "simplified_operation"
    ALTERNATIVE_API = "alternative_api"


class RetryConfig:
    """重试配置"""

    def __init__(
        self,
        max_retries: int = 3,
        strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
        backoff_factor: float = 2.0,
        initial_delay: float = 1.0
    ):
        self.max_retries = max_retries
        self.strategy = strategy
        self.backoff_factor = backoff_factor
        self.initial_delay = initial_delay


class ErrorRecovery:
    """错误恢复器"""

    def __init__(self):
        self.recovery_attempts: Dict[str, int] = {}
        self.recovery_history: List[Dict] = []

    def calculate_backoff_delay(
        self,
        attempt: int,
        config: RetryConfig
    ) -> float:
        """
        计算退避延迟

        Args:
            attempt: 当前尝试次数
            config: 重试配置

        Returns:
            延迟时间（秒）
        """
        if config.strategy == RetryStrategy.LINEAR:
            # 线性退避
            delay = config.initial_delay * attempt
        elif config.strategy == RetryStrategy.EXPONENTIAL:
            # 指数退避
            delay = config.initial_delay * (config.backoff_factor ** (attempt - 1))
        else:
            delay = 0

        return min(delay, 60.0)  # 最大延迟60秒

    def execute_with_retry(
        self,
        operation: Callable,
        operation_id: str,
        config: RetryConfig,
        fallback: Optional[Callable] = None
    ) -> Any:
        """
        带重试执行操作

        Args:
            operation: 要执行的操作
            operation_id: 操作ID
            config: 重试配置
            fallback: 回退函数

        Returns:
            操作结果

        Raises:
            Exception: 所有重试失败后
        """
        self.recovery_attempts[operation_id] = 0

        for attempt in range(1, config.max_retries + 1):
            self.recovery_attempts[operation_id] = attempt

            try:
                print(f"\n🔄 尝试 #{attempt} 执行操作: {operation_id}")
                result = operation()

                # 成功，记录历史
                history = {
                    "operation_id": operation_id,
                    "attempt": attempt,
                    "status": "success",
                    "timestamp": datetime.now().isoformat()
                }
                self.recovery_history.append(history)

                print(f"✅ 操作成功!")
                return result

            except Exception as e:
                print(f"❌ 尝试 #{attempt} 失败: {str(e)}")

                # 记录失败
                history = {
                    "operation_id": operation_id,
                    "attempt": attempt,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.recovery_history.append(history)

                # 检查是否还有重试机会
                if attempt < config.max_retries:
                    delay = self.calculate_backoff_delay(attempt, config)
                    print(f"⏰ {config.strategy.value}退避 {delay:.1f}秒后重试...")
                    time.sleep(delay)
                else:
                    print(f"⚠️  所有重试失败")
                    if fallback:
                        print(f"🔄 执行回退策略...")
                        try:
                            fallback_result = fallback()
                            fallback_history = {
                                "operation_id": operation_id,
                                "strategy": "fallback",
                                "status": "success",
                                "timestamp": datetime.now().isoformat()
                            }
                            self.recovery_history.append(fallback_history)
                            print(f"✅ 回退成功!")
                            return fallback_result
                        except Exception as fallback_error:
                            print(f"❌ 回退也失败: {str(fallback_error)}")
                    raise e

    def get_recovery_stats(self, operation_id: str) -> Dict[str, Any]:
        """获取恢复统计"""
        attempts = self.recovery_attempts.get(operation_id, 0)
        operation_history = [h for h in self.recovery_history if h["operation_id"] == operation_id]

        return {
            "operation_id": operation_id,
            "total_attempts": attempts,
            "history": operation_history
        }


class DegradationStrategy:
    """降级策略"""

    def __init__(self):
        self.degraded_services: Dict[str, bool] = {}
        self.fallback_data: Dict[str, Any] = {}

    def register_fallback(self, service_name: str, fallback_data: Any):
        """注册回退数据"""
        self.fallback_data[service_name] = fallback_data
        print(f"📝 为服务 '{service_name}' 注册回退数据")

    def execute_with_degradation(
        self,
        operation: Callable,
        service_name: str,
        fallback_data: Optional[Any] = None
    ) -> Any:
        """
        带降级执行操作

        Args:
            operation: 要执行的操作
            service_name: 服务名称
            fallback_data: 回退数据

        Returns:
            操作结果或回退数据
        """
        try:
            print(f"\n🔧 执行服务操作: {service_name}")
            result = operation()

            # 服务恢复正常
            if self.degraded_services.get(service_name, False):
                self.degraded_services[service_name] = False
                print(f"✅ 服务 '{service_name}' 已恢复正常")

            return result

        except Exception as e:
            print(f"❌ 服务 '{service_name}' 失败: {str(e)}")
            print(f"⚠️  启用降级模式")

            self.degraded_services[service_name] = True

            # 使用回退数据
            if fallback_data is not None:
                print(f"📥 使用提供的回退数据")
                return fallback_data
            elif service_name in self.fallback_data:
                print(f"📥 使用缓存的回退数据")
                return self.fallback_data[service_name]
            else:
                print(f"⚠️  无回退数据可用")
                raise e

    def get_degraded_status(self) -> Dict[str, bool]:
        """获取降级状态"""
        return self.degraded_services


# 模拟操作
def unreliable_database_query() -> Dict[str, Any]:
    """模拟不可靠的数据库查询"""
    time.sleep(0.5)

    # 70%失败率
    if random.random() < 0.7:
        raise Exception("数据库连接超时")

    return {"data": "query_result", "timestamp": datetime.now().isoformat()}


def fallback_data_source() -> Dict[str, Any]:
    """回退数据源"""
    return {
        "data": "cached_result",
        "source": "cache",
        "timestamp": datetime.now().isoformat()
    }


def unreliable_api_call() -> Dict[str, Any]:
    """模拟不可靠的API调用"""
    time.sleep(0.3)

    # 60%失败率
    if random.random() < 0.6:
        raise Exception("API服务暂时不可用")

    return {"result": "api_response", "status": "success"}


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 12 - 示例 2：错误恢复策略 (Error Recovery Strategies)")
    print("=" * 80)
    print()
    print("🛡️  此示例演示重试、回退和降级策略")
    print()

    # 初始化恢复器
    recovery = ErrorRecovery()
    degradation = DegradationStrategy()

    print("🔄 策略 1: 指数退避重试")
    print("-" * 80)

    retry_config = RetryConfig(
        max_retries=5,
        strategy=RetryStrategy.EXPONENTIAL,
        backoff_factor=2.0,
        initial_delay=1.0
    )

    try:
        result = recovery.execute_with_retry(
            operation=unreliable_database_query,
            operation_id="db_query_001",
            config=retry_config,
            fallback=fallback_data_source
        )
        print(f"\n✅ 最终结果: {result}")
    except Exception as e:
        print(f"\n❌ 操作最终失败: {str(e)}")

    stats = recovery.get_recovery_stats("db_query_001")
    print(f"\n📊 恢复统计:")
    print(f"  操作ID: {stats['operation_id']}")
    print(f"  总尝试次数: {stats['total_attempts']}")
    print(f"  历史记录数: {len(stats['history'])}")

    print("\n" + "=" * 80)
    print("🔄 策略 2: 线性退避重试")
    print("-" * 80)

    linear_config = RetryConfig(
        max_retries=4,
        strategy=RetryStrategy.LINEAR,
        backoff_factor=1.0,
        initial_delay=2.0
    )

    try:
        result = recovery.execute_with_retry(
            operation=unreliable_api_call,
            operation_id="api_call_001",
            config=linear_config
        )
        print(f"\n✅ 最终结果: {result}")
    except Exception as e:
        print(f"\n❌ 操作最终失败: {str(e)}")

    print("\n" + "=" * 80)
    print("🔄 策略 3: 优雅降级")
    print("-" * 80)

    # 注册回退数据
    degradation.register_fallback(
        "user_service",
        {
            "users": [
                {"id": 1, "name": "默认用户1"},
                {"id": 2, "name": "默认用户2"}
            ],
            "source": "static_cache",
            "timestamp": datetime.now().isoformat()
        }
    )

    # 执行带降级的操作
    try:
        result = degradation.execute_with_degradation(
            operation=unreliable_api_call,
            service_name="user_service"
        )
        print(f"\n✅ 服务结果: {result}")
    except Exception as e:
        print(f"\n❌ 操作失败: {str(e)}")

    # 显示降级状态
    degraded_status = degradation.get_degraded_status()
    print(f"\n📊 降级状态: {degraded_status}")

    print("\n" + "=" * 80)
    print("✨ 错误恢复策略示例完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
