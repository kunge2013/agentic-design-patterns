"""
Chapter 12 - 代码示例 1：基础异常处理 (Basic Exception Handling)

此示例演示Agent执行过程中的基础异常捕获和处理。
"""
import sys
import os
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config


class ErrorType(Enum):
    """错误类型枚举"""
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    VALIDATION_ERROR = "validation_error"
    API_ERROR = "api_error"
    UNKNOWN_ERROR = "unknown_error"


class AgentError(Exception):
    """Agent基础异常类"""
    def __init__(
        self,
        error_type: ErrorType,
        message: str,
        details: Optional[Dict] = None
    ):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "details": self.details,
            "timestamp": datetime.now().isoformat()
        }


class ToolExecution:
    """工具执行基类"""

    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.success_count = 0
        self.failure_count = 0
        self.error_history: List[Dict] = []

    def execute(self, *args, **kwargs) -> Any:
        """执行工具（子类实现）"""
        raise NotImplementedError("子类必须实现execute方法")

    def _simulate_failure(self, failure_rate: float = 0.3) -> bool:
        """模拟失败（用于演示）"""
        return random.random() < failure_rate

    def _record_error(self, error: AgentError):
        """记录错误"""
        self.failure_count += 1
        error_record = {
            "tool_name": self.tool_name,
            "error": error.to_dict(),
            "occurred_at": datetime.now().isoformat()
        }
        self.error_history.append(error_record)

    def _record_success(self):
        """记录成功"""
        self.success_count += 1

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        total = self.success_count + self.failure_count
        success_rate = (self.success_count / total * 100) if total > 0 else 0

        return {
            "tool_name": self.tool_name,
            "total_executions": total,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": success_rate,
            "recent_errors": self.error_history[-5:]  # 最近5个错误
        }


class DatabaseTool(ToolExecution):
    """数据库工具"""

    def __init__(self):
        super().__init__("database_tool")

    def execute(
        self,
        operation: str,
        data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        执行数据库操作

        Args:
            operation: 操作类型（query/insert/update/delete）
            data: 操作数据

        Returns:
            操作结果

        Raises:
            AgentError: 操作失败时
        """
        print(f"\n🔧 执行数据库操作: {operation}")

        # 模拟各种错误
        if self._simulate_failure():
            error_types = [
                ErrorType.TIMEOUT,
                ErrorType.CONNECTION_ERROR,
                ErrorType.VALIDATION_ERROR
            ]
            error_type = random.choice(error_types)

            error_messages = {
                ErrorType.TIMEOUT: "数据库查询超时（30秒）",
                ErrorType.CONNECTION_ERROR: "无法连接到数据库服务器",
                ErrorType.VALIDATION_ERROR: "数据验证失败：缺少必需字段"
            }

            error = AgentError(
                error_type=error_type,
                message=error_messages[error_type],
                details={
                    "operation": operation,
                    "data": data
                }
            )
            self._record_error(error)
            raise error

        # 模拟成功执行
        print(f"✅ 操作成功: {operation}")
        result = {
            "status": "success",
            "operation": operation,
            "rows_affected": random.randint(1, 10),
            "timestamp": datetime.now().isoformat()
        }
        self._record_success()
        return result


class APITool(ToolExecution):
    """API工具"""

    def __init__(self, base_url: str):
        super().__init__("api_tool")
        self.base_url = base_url

    def execute(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        执行API调用

        Args:
            endpoint: API端点
            method: HTTP方法
            params: 请求参数

        Returns:
            API响应

        Raises:
            AgentError: API调用失败时
        """
        print(f"\n🌐 执行API调用: {method} {self.base_url}{endpoint}")

        # 模拟API错误
        if self._simulate_failure():
            error_types = [
                ErrorType.API_ERROR,
                ErrorType.CONNECTION_ERROR,
                ErrorType.TIMEOUT
            ]
            error_type = random.choice(error_types)

            error_messages = {
                ErrorType.API_ERROR: f"API错误: 500 Internal Server Error",
                ErrorType.CONNECTION_ERROR: "无法连接到API服务器",
                ErrorType.TIMEOUT: "API请求超时（60秒）"
            }

            error = AgentError(
                error_type=error_type,
                message=error_messages[error_type],
                details={
                    "endpoint": endpoint,
                    "method":: method,
                    "params": params
                }
            )
            self._record_error(error)
            raise error

        # 模拟成功响应
        print(f"✅ API调用成功: {method} {endpoint}")
        response = {
            "status_code": 200,
            "data": {
                "result": "success",
                "timestamp": datetime.now().isoformat()
            }
        }
        self._record_success()
        return response


class ExceptionHandler:
    """异常处理器"""

    def __init__(self):
        self.handled_errors: List[Dict] = []

    def handle(
        self,
        error: Exception,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        处理异常

        Args:
            error: 捕获的异常
            context: 上下文信息

        Returns:
            处理结果
        """
        handled_at = datetime.now()

        if isinstance(error, AgentError):
            print(f"\n⚠️  捕获到Agent错误:")
            print(f"   类型: {error.error_type.value}")
            print(f"   消息: {error.message}")
            print(f"   详情: {error.details}")

            handle_result = {
                "handled": True,
                "error_type": error.error_type.value,
                "message": error.message,
                "suggested_action": self._get_suggested_action(error.error_type),
                "handled_at": handled_at.isoformat(),
                "context": context
            }

            self.handled_errors.append(handle_result)
            return handle_result

        else:
            print(f"\n⚠️  捕获到未知错误:")
            print(f"   类型: {type(error).__name__}")
            print(f"   消息: {str(error)}")

            handle_result = {
                "handled": True,
                "error_type": "unknown",
                "message": str(error),
                "suggested_action": "检查错误日志并联系支持团队",
                "handled_at": handled_at.isoformat(),
                "context": context
            }

            self.handled_errors.append(handle_result)
            return handle_result

    def _get_suggested_action(self, error_type: ErrorType) -> str:
        """根据错误类型返回建议操作"""
        actions = {
            ErrorType.TIMEOUT: "增加超时时间或重试操作",
            "ErrorType.CONNECTION_ERROR": "检查网络连接或服务器状态",
            "ErrorType.VALIDATION_ERROR": "验证输入数据格式和必需字段",
            "ErrorType.API_ERROR": "检查API文档或联系API提供者",
            "ErrorType.UNKNOWN_ERROR": "收集详细信息并上报"
        }
        return actions.get(error_type, "联系技术支持")

    def get_error_summary(self) -> Dict[str, Any]:
        """获取错误摘要"""
        return {
            "total_handled": len(self.handled_errors),
            "errors": self.handled_errors
        }


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 12 - 示例 1：基础异常处理 (Basic Exception Handling)")
    print("=" * 80)
    print()
    print("🛡️  此示例演示Agent执行过程中的异常捕获和处理")
    print()

    # 初始化工具
    db_tool = DatabaseTool()
    api_tool = APITool(base_url="https://api.example.com")
    exception_handler = ExceptionHandler()

    print("🧪 测试场景 1: 数据库操作")
    (print("-" * 80)

    try:
        result = db_tool.execute(
            operation="query",
            data={"table": "users", "limit": 10}
        )
        print(f"✅ 结果: {result}")
    except AgentError as e:
        handle_result = exception_handler.handle(e, context={"scenario": "database_query"})

    print("\n🧪 测试场景 2: API调用")
    print("-" * 80)

    try:
        result = api_tool.execute(
            endpoint="/users",
            method="GET",
            params={"page": 1}
        )
        print(f"✅ 结果: {result}")
    except AgentError as e:
        handle_result = exception_handler.handle(e, context={"scenario": "api_call"})

    print("\n🧪 测试场景 3: 多次操作模拟")
    print("-" * 80)

    tools = [db_tool, api_tool]
    for i, tool in enumerate(tools * 3, 1):  # 运行6次操作
        print(f"\n--- 操作 #{i} ({tool.tool_name}) ---")
        try:
            if isinstance(tool, DatabaseTool):
                result = tool.execute("insert", {"id": i, "data": f"item_{i}"})
            else:
                result = tool.execute("/items", "POST", {"name": f"item_{i}"})
            print(f"✅ 操作成功")
        except AgentError as e:
            exception_handler.handle(e, context={"operation_index": i})

    print("\n📊 错误摘要")
    print("-" * 80)

    for tool in tools:
        stats = tool.get_stats()
        print(f"\n{stats['tool_name']}:")
        print(f"  总执行次数: {stats['total_executions']}")
        print(f"  成功次数: {stats['success_count']}")
        print(f"  失败次数: {stats['failure_count']}")
        print(f"  成功率: {stats['success_rate']:.1f}%")

    print("\n" + "=" * 80)
    print("✨ 基础异常处理示例完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
