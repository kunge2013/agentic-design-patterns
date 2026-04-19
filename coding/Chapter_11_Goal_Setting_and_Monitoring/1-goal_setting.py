"""
Chapter 11 - 代码示例 1：目标设置 (Goal Setting)

此示例演示如何为Agent设置明确、可量化的目标，使用SMART原则。
"""
import sys
import os
from pathlib import Path

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config

from typing import Dict, List, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime, timedelta


class Goal(BaseModel):
    """目标类，实现SMART原则"""
    id: str
    title: str = Field(..., description="目标标题")
    description: str = Field(..., description="目标描述")
    target_value: float = Field(..., description="目标数值")
    current_value: float = Field(default=0.0, description="当前进度值")
    unit: str = Field(default="%", description="计量单位")
    deadline: datetime = Field(..., description="截止日期")
    priority: str = Field(default="medium", description="优先级：high/medium/low")
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="active", description="状态：active/completed/failed")

    @validator('priority')
    def validate_priority(cls, v):
        if v not in ['high', 'medium', 'low']:
            raise ValueError('priority必须是high、medium或low')
        return v

    def progress_percentage(self) -> float:
        """计算完成百分比"""
        if self.target_value == 0:
            return 0.0
        return min((self.current_value / self.target_value) * 100, 100.0)

    def is_complete(self) -> bool:
        """检查目标是否完成"""
        return self.current_value >= self.target_value

    def is_overdue(self) -> bool:
        """检查目标是否超期"""
        return datetime.now() > self.deadline and self.status != "completed"

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "target_value": self.target_value,
            "current_value": self.current_value,
            "unit": self.unit,
            "progress": self.progress_percentage(),
            "deadline": self.deadline.isoformat(),
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "is_complete": self.is_complete(),
            "is_overdue": self.is_overdue()
        }


class GoalManager:
    """目标管理器"""

    def __init__(self):
        self.goals: Dict[str, Goal] = {}
        self.goal_counter = 0

    def create_goal(
        self,
        title: str,
        description: str,
        target_value: float,
        unit: str = "%",
        days_to_deadline: int = 7,
        priority: str = "medium"
    ) -> Goal:
        """
        创建新目标（SMART原则）

        Args:
            title: 目标标题
            description: 目标描述
            target_value: 目标值
            unit: 单位
            days_to_deadline: 距离截止日期的天数
            priority: 优先级

        Returns:
            创建的目标对象
        """
        # 验证SMART原则
        if not title or not title.strip():
            raise ValueError("目标标题不能为空（Specific）")

        if target_value <= 0:
            raise ValueError("目标值必须大于0（Measurable）")

        if days_to_deadline <= 0:
            raise ValueError("截止日期必须在未来（Time-bound）")

        deadline = datetime.now() + timedelta(days=days_to_deadline)

        self.goal_counter += 1
        goal = Goal(
            id=f"goal_{self.goal_counter:04d}",
            title=title,
            description=description,
            target_value=target_value,
            unit=unit,
            deadline=deadline,
            priority=priority
        )

        self.goals[goal.id] = goal
        return goal

    def update_goal_progress(self, goal_id: str, progress: float) -> Goal:
        """
        更新目标进度

        Args:
            goal_id: 目标ID
            progress: 进度值

        Returns:
            更新后的目标
        """
        if goal_id not in self.goals:
            raise ValueError(f"目标 {goal_id} 不存在")

        goal = self.goals[goal_id]
        goal.current_value = min(progress, goal.target_value)

        # 检查是否完成
        if goal.is_complete():
            goal.status = "completed"

        return goal

    def get_goal(self, goal_id: str) -> Goal:
        """获取目标"""
        if goal_id not in self.goals:
            raise ValueError(f"目标 {goal_id} 不存在")
        return self.goals[goal_id]

    def list_goals(self) -> List[Dict[str, Any]]:
        """列出所有目标"""
        return [goal.to_dict() for goal in self.goals.values()]


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 11 - 示例 1：目标设置 (Goal Setting)")
    print("=" * 80)
    print()

    # 初始化目标管理器
    manager = GoalManager()

    print("🎯 创建SMART目标")
    print("-" * 80)

    # 示例1：创建代码质量目标
    try:
        code_quality_goal = manager.create_goal(
            title="提高代码测试覆盖率",
            description="将项目代码测试覆盖率提升到85%以上",
            target_value=85.0,
            unit="%",
            days_to_deadline=14,
            priority="high"
        )
        print(f"✅ 目标创建成功：{code_quality_goal.title}")
        print(f"   ID: {code_quality_goal.id}")
        print(f"   目标值: {code_quality_goal.target_value}{code_quality_goal.unit}")
        print(f"   截止日期: {code_quality_goal.deadline.strftime('%Y-%m-%d')}")
        print(f"   优先级: {code_quality_goal.priority}")
        print()
    except Exception as e:
        print(f"❌ 创建目标失败: {e}")
        print()

    # 示例2：创建用户增长目标
    try:
        user_growth_goal = manager.create_goal(
            title="月活用户增长",
            description="本月新增月活用户达到10000人",
            target_value=10000.0,
            unit="用户",
            days_to_deadline=30,
            priority="high"
        )
        print(f"✅ 目标创建成功：{user_growth_goal.title}")
        print(f"   ID: {user_growth_goal.id}")
        print(f"   目标值: {user_growth_goal.target_value}{user_growth_goal.unit}")
        print(f"   截止日期: {user_growth_goal.deadline.strftime('%Y-%m-%d')}")
        print()
    except Exception as e:
        print(f"❌ 创建目标失败: {e}")
        print()

    # 示例3：创建文档完成目标
    try:
        docs_goal = manager.create_goal(
            title="完成API文档",
            description="完成所有核心API接口的文档编写",
            target_value=50.0,
            unit="接口",
            days_to_deadline=7,
            priority="medium"
        )
        print(f"✅ 目标创建成功：{docs_goal.title}")
        print(f"   ID: {docs_goal.id}")
        print(f"   目标值: {docs_goal.target_value}{docs_goal.unit}")
        print(f"   截止日期: {docs_goal.deadline.strftime('%Y-%m-%d')}")
        print()
    except Exception as e:
        print(f"❌ 创建目标失败: {e}")
        print()

    print("📊 更新目标进度")
    print("-" * 80)

    # 更新第一个目标的进度
    try:
        goal_id = code_quality_goal.id
        updated_goal = manager.update_goal_progress(goal_id, 60.0)
        print(f"✅ 更新目标进度: {updated_goal.title}")
        print(f"   当前进度: {updated_goal.current_value}{updated_goal.unit}")
        print(f"   完成百分比: {updated_goal.progress_percentage():.1f}%")
        print(f"   状态: {updated_goal.status}")
        print()
    except Exception as e:
        print(f"❌ 更新进度失败: {e}")
        print()

    print("📋 列出所有目标")
    print("-" * 80)

    goals = manager.list_goals()
    for i, goal in enumerate(goals, 1):
        print(f"\n目标 #{i}:")
        print(f"  标题: {goal['title']}")
        print(f"  进度: {goal['current_value']:.1f}/{goal['target_value']:.1f} "
              f"({goal['progress']:.1f}%)")
        print(f"  状态: {goal['status']}")
        print(f"  优先级: {goal['priority']}")
        print(f"  截止: {goal['deadline'][:10]}")

    print()
    print("=" * 80)
    print("✨ 目标设置示例完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
