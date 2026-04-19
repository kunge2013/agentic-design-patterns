"""
Chapter 13 - 代码示例 1：基本人工确认 (Basic Human Confirmation)

此示例演示Agent在关键决策点请求人工确认。
"""
import sys
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config


class ConfirmationType(Enum):
    """确认类型"""
    YES_NO = "yes_no"
    YES_NO_CANCEL = "yes_no_cancel"
    CUSTOM = "custom"


@dataclass
class HumanConfirmation:
    """人工确认请求"""
    confirmation_id: str
    question: str
    options: List[str]
    confirmation_type: ConfirmationType
    context: Optional[Dict] = None
    created_at: datetime = field(default_factory=datetime.now)
    responded_at: Optional[datetime] = None
    response: Optional[str] = None
    status: str = "pending"  # pending, responded, cancelled

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "confirmation_id": self.confirmation_id,
            "question": self.question,
            "options": self.options,
            "type": self.confirmation_type.value,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
            "status": self.status
        }


class HumanConfirmationManager:
    """人工确认管理器"""

    def __init__(self, auto_confirm: bool = False):
        self.confirmations: Dict[str, HumanConfirmation] = {}
        self.confirmation_counter = 0
        self.auto_confirm = auto_confirm  # 用于自动化测试
        self.default_response = "yes"  # 自动测试的默认响应

    def request_confirmation(
        self,
        question: str,
        options: Optional[List[str]] = None,
        confirmation_type: ConfirmationType = ConfirmationType.YES_NO,
        context: Optional[Dict] = None
    ) -> HumanConfirmation:
        """
        请求人工确认

        Args:
            question: 要确认的问题
            options: 可选选项列表
            confirmation_type: 确认类型
            context: 上下文信息

        Returns:
            确认对象
        """
        # 设置默认选项
        if options is None:
            if confirmation_type == ConfirmationType.YES_NO:
                options = ["yes", "no"]
            elif confirmation_type == ConfirmationType.YES_NO_CANCEL:
                options = ["yes", "no", "cancel"]
            else:
                options = ["confirm", "deny"]

        self.confirmation_counter += 1
        confirmation = HumanConfirmation(
            confirmation_id=f"conf_{self.confirmation_counter:04d}",
            question=question,
            options=options,
            confirmation_type=confirmation_type,
            context=context
        )

        self.confirmations[confirmation.confirmation_id] = confirmation

        print("\n" + "=" * 80)
        print("🤔 人工确认请求")
        print("=" * 80)
        print(f"ID: {confirmation.confirmation_id}")
        print(f"问题: {question}")
        print(f"选项: {', '.join(options)}")

        if context:
            print(f"上下文: {context}")

        print("=" * 80)

        # 如果启用了自动确认，模拟响应
        if self.auto_confirm:
            self._auto_respond(confirmation.confirmation_id)

        return confirmation

    def respond(self, confirmation_id: str, response: str) -> bool:
        """
        提供人工响应

        Args:
            confirmation_id: 确认ID
            response: 响应内容

        Returns:
            是否成功响应
        """
        if confirmation_id not in self.confirmations:
            print(f"❌ 确认ID {confirmation_id} 不存在")
            return False

        confirmation = self.confirmations[confirmation_id]

        if confirmation.status != "pending":
            print(f"⚠️  确认 {confirmation_id} 已经被响应")
            return False

        if response not in confirmation.options:
            print(f"❌ 无效的响应 '{response}'，有效选项: {confirmation.options}")
            return False

        confirmation.response = response
        confirmation.responded_at = datetime.now()
        confirmation.status = "responded"

        print(f"\n✅ 人工响应记录:")
        print(f"   确认ID: {confirmation_id}")
        print(f"   响应: {response}")
        print(f"   响应时间: {confirmation.responded_at.strftime('%Y-%m-%d %H:%M:%S')}")

        return True

    def cancel(self, confirmation_id: str) -> bool:
        """
        取消确认

        Args:
            confirmation_id: 确认ID

        Returns:
            是否成功取消
        """
        if confirmation_id not in self.confirmations:
            return False

        confirmation = self.confirmations[confirmation_id]
        confirmation.status = "cancelled"
        confirmation.responded_at = datetime.now()

        print(f"\n⏸️  确认 {confirmation_id} 已取消")
        return True

    def get_confirmation(self, confirmation_id: str) -> Optional[HumanConfirmation]:
        """获取确认"""
        return self.confirmations.get(confirmation_id)

    def _auto_respond(self, confirmation_id: str):
        """自动响应（用于测试）"""
        print(f"\n🤖 自动响应: {self.default_response}")
        time.sleep(1)  # 模拟思考时间
        self.respond(confirmation_id, self.default_response)


class AgentWithHumanConfirmation:
    """带人工确认的Agent"""

    def __init__(self, confirmation_manager: HumanConfirmationManager):
        self.confirmation_manager = confirmation_manager
        self.operation_count = 0

    def execute_critical_operation(
        self,
        operation_name: str,
        operation_func: callable,
        context: Optional[Dict] = None
    ) -> Any:
        """
        执行关键操作（需要人工确认）

        Args:
            operation_name: 操作名称
            operation_func: 操作函数
            context: 操作上下文

        Returns:
            操作结果
        """
        print(f"\n🤖 准备执行关键操作: {operation_name}")

        # 请求确认
        confirmation = self.confirmation_manager.request_confirmation(
            question=f"是否允许执行操作 '{operation_name}'？",
            options=["yes", "no"],
            confirmation_type=ConfirmationType.YES_NO,
            context=context
        )

        # 等待响应（在实际应用中会使用异步或轮询）
        max_wait = 30  # 最大等待30秒
        waited = 0
        while confirmation.status == "pending" and waited < max_wait:
            time.sleep(1)
            waited += 1

        if confirmation.status != "responded":
            raise TimeoutError("等待人工确认超时")

        # 根据响应决定是否执行
        if confirmation.response == "yes":
            print(f"\n✅ 执行操作: {operation_name}")
            self.operation_count += 1
            return operation_func()
        else:
            print(f"\n⏸️  操作被拒绝")
            return None

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "operation_count": self.operation_count,
            "confirmation_count": self.confirmation_manager.confirmation_counter
        }


def operation_delete_file() -> str:
    """模拟删除文件操作"""
    print("🗑️  执行删除文件...")
    time.sleep(1)
    return "文件已删除"


def operation_send_email() -> str:
    """模拟发送邮件操作"""
    print("📧 发送邮件...")
    time.sleep(2)
    return "邮件已发送"


def operation_update_database() -> str:
    """模拟更新数据库操作"""
    print("💾 更新数据库...")
    time.sleep(1.5)
    return "数据库已更新"


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 13 - 示例 1：基本人工确认 (Basic Human Confirmation)")
    print("=" * 80)
    print()
    print("🤔 此示例演示Agent在关键决策点请求人工确认")
    print("   （为了演示，使用自动确认模式）")
    print()

    # 初始化确认管理器（启用自动确认用于演示）
    confirmation_manager = HumanConfirmationManager(auto_confirm=True)
    agent = AgentWithHumanConfirmation(confirmation_manager)

    print("🧪 场景 1: 删除重要文件")
    print("-" * 80)

    try:
        result = agent.execute_critical_operation(
            operation_name="删除重要文件",
            operation_func=operation_delete_file,
            context={
                "file_path": "/important/data.csv",
                "file_size": "10MB"
            }
        )
        print(f"操作结果: {result}")
    except TimeoutError:
        print("❌ 等待确认超时")

    print("\n🧪 场景 2: 发送批量邮件")
    print("-" * 80)

    # 设置不同的默认响应
    confirmation_manager.default_response = "no"

    try:
        result = agent.execute_critical_operation(
            operation_name="发送批量邮件",
            operation_func=operation_send_email,
            context={
                "recipient_count": 1000,
                "email_type": "marketing"
            }
        )
        print(f"操作结果: {result}")
    except TimeoutError:
        print("❌ 等待确认超时")

    print("\n🧪 场景 3: 更新生产数据库")
    print("-" * 80)

    confirmation_manager.default_response = "yes"

    try:
        result = agent.execute_critical_operation(
            operation_name="更新生产数据库",
            operation_func=operation_update_database,
            context={
                "database": "production_db",
                "table": "users"
            }
        )
        print(f"操作结果: {result}")
    except TimeoutError:
        print("❌ 等待确认超时")

    print("\n📊 统计信息")
    print("-" * 80)

    stats = agent.get_stats()
    print(f"执行的操作数: {stats['operation_count']}")
    print(f"总确认数: {stats['confirmation_count']}")

    print("\n" + "=" * 80)
    print("✨ 基本人工确认示例完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
