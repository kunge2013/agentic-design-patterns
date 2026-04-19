"""
Chapter 11 - 代码示例 2：目标监控 (Goal Monitoring)

此示例演示如何实时监控Agent目标的执行进度。
"""
import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config

from pydantic import BaseModel, Field


class GoalMetrics(BaseModel):
    """目标指标"""
    timestamp: datetime = Field(default_factory=datetime.now)
    current_value: float
    target_value: float
    progress_percentage: float
    status: str


class MonitorEvent(BaseModel):
    """监控事件"""
    timestamp: datetime = Field(default_factory=datetime.now)
    event_type: str  # 'progress_update', 'milestone_reached', 'goal_complete', 'error'
    goal_id: str
    message: str
    data: Optional[Dict] = None


class GoalMonitor:
    """目标监控器"""

    def __init__(self):
        self.goals: Dict[str, Dict] = {}
        self.metrics_history: Dict[str, List[GoalMetrics]] = {}
        self.events: List[MonitorEvent] = []
        self.callbacks: Dict[str, List[Callable]] = {}

    def register_goal(
        self,
        goal_id: str,
        title: str,
        target_value: float,
        unit: str = "%"
    ):
        """注册要监控的目标"""
        self.goals[goal_id] = {
            "id": goal_id,
            "title": title,
            "target_value": target_value,
            "current_value": 0.0,
            "unit": unit,
            "start_time": datetime.now(),
            "status": "running"
        }
        self.metrics_history[goal_id] = []
        self._add_event("goal_registered", goal_id, f"目标'{title}'已注册")

    def update_progress(self, goal_id: str, current_value: float):
        """
        更新目标进度

        Args:
            goal_id: 目标ID
            current_value: 当前进度值
        """
        if goal_id not in self.goals:
            raise ValueError(f"目标 {goal_id} 未注册")

        goal = self.goals[goal_id]
        goal["current_value"] = current_value

        # 计算进度百分比
        progress = (current_value / goal["target_value"]) * 100 if goal["target_value"] > 0 else 0

        # 记录指标
        metrics = GoalMetrics(
            current_value=current_value,
            target_value=goal["target_value"],
            progress_percentage=progress,
            status=goal["status"]
        )
        self.metrics_history[goal_id].append(metrics)

        # 触发事件
        self._add_event("progress_update", goal_id,
                       f"进度更新: {current_value:.1f}/{goal['target_value']:.1f} ({progress:.1f}%)")

        # 检查里程碑
        self._check_milestones(goal_id, progress)

        # 检查是否完成
        if current_value >= goal["target_value"]:
            self.mark_complete(goal_id)

        # 触发回调
        self._trigger_callbacks(goal_id, metrics)

    def _check_milestones(self, goal_id: str, progress: float):
        """检查和触发里程碑"""
        milestones = [25, 50, 75, 100]
        goal = self.goals[goal_id]

        for milestone in milestones:
            milestone_key = f"milestone_{milestone}"
            if milestone <= progress and milestone_key not in goal:
                goal[milestone_key] = True
                self._add_event("milestone_reached", goal_id,
                              f"里程碑达成: {milestone}%")

    def mark_complete(self, goal_id: str):
        """标记目标为完成"""
        if goal_id not in self.goals:
            raise ValueError(f"目标 {goal_id} 未注册")

        goal = self.goals[goal_id]
        goal["status"] = "completed"
        goal["end_time"] = datetime.now()

        duration = (goal["end_time"] - goal["start_time"]).total_seconds()
        self._add_event("goal_complete", goal_id,
                       f"目标'{goal['title']}'已完成! 耗时: {duration:.1f}秒")

    def get_metrics(self, goal_id: str) -> Optional[Dict]:
        """获取目标当前指标"""
        if goal_id not in self.goals:
            return None

        goal = self.goals[goal_id]
        progress = (goal["current_value"] / goal["target_value"]) * 100 if goal["target_value"] > 0 else 0

        return {
            "goal_id": goal_id,
            "title": goal["title"],
            "current_value": goal["current_value"],
            "target_value": goal["target_value"],
            "unit": goal["unit"],
            "progress_percentage": progress,
            "status": goal["status"],
            "start_time": goal["start_time"].isoformat(),
            "end_time": goal.get("end_time", "").isoformat() if "end_time" in goal else None
        }

    def get_event_history(self, goal_id: Optional[str] = None) -> List[MonitorEvent]:
        """获取事件历史"""
        if goal_id:
            return [e for e in self.events if e.goal_id == goal_id]
        return self.events

    def register_callback(self, event_type: str, callback: Callable):
        """注册回调函数"""
        if event_type not in self.callbacks:
            self.callbacks[event_type] = []
        self.callbacks[event_type].append(callback)

    def _add_event(self, event_type: str, goal_id: str, message: str):
        """添加事件"""
        event = MonitorEvent(
            event_type=event_type,
            goal_id=goal_id,
            message=message
        )
        self.events.append(event)
        print(f"[{event.timestamp.strftime('%H:%M:%S')}] {message}")

    def _trigger_callbacks(self, goal_id: str, metrics: GoalMetrics):
        """触发回调"""
        for callback in self.callbacks.get("progress_update", []):
            callback(goal_id, metrics)


def simulate_progress_monitoring():
    """模拟进度监控"""
    monitor = GoalMonitor()

    # 注册目标
    monitor.register_goal(
        goal_id="project_001",
        title="完成项目开发",
        target_value=100.0,
        unit="%"
    )

    monitor.register_goal(
        goal_id="test_coverage_001",
        title="测试覆盖率提升",
        target_value=80.0,
        unit="%"
    )

    monitor.register_goal(
        goal_id="api_completion_001",
        title="API接口完成",
        target_value=50.0,
        unit="个"
    )

    print("\n" + "=" * 80)
    print("开始模拟进度更新...")
    print("=" * 80 + "\n")

    # 模拟进度更新
    project_progress = [10, 25, 40, 55, 70, 85, 95, 100]
    test_progress = [15, 30, 45, 60, 75, 80]
    api_progress = [5, 10, 20, 30, 40, 50]

    # 同时更新多个目标
    for i in range(max(len(project_progress), len(test_progress), len(api_progress))):
        print(f"\n--- 时间步 {i + 1} ---")

        if i < len(project_progress):
            monitor.update_progress("project_001", project_progress[i])

        if i < len(test_progress):
            monitor.update_progress("test_coverage_001", test_progress[i])

        if i < len(api_progress):
            monitor.update_progress("api_completion_001", api_progress[i])

        time.sleep(0.5)  # 模拟处理时间

    print("\n" + "=" * 80)
    print("监控总结")
    print("=" * 80 + "\n")

    for goal_id in monitor.goals.keys():
        metrics = monitor.get_metrics(goal_id)
        if metrics:
            print(f"目标: {metrics['title']}")
            print(f"  状态: {metrics['status']}")
            print(f"  进度: {metrics['current_value']:.1f}/{metrics['target_value']:.1f} "
                  f"({metrics['progress_percentage']:.1f}%)")
            if metrics['end_time']:
                duration = (datetime.fromisoformat(metrics['end_time']) -
                          datetime.fromisoformat(metrics['start_time'])).total_seconds()
                print(f"  耗时: {duration:.1f}秒")
            print()


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 11 - 示例 2：目标监控 (Goal Monitoring)")
    print("=" * 80)
    print()
    print("📊 此示例演示实时目标监控和进度跟踪")
    print()

    simulate_progress_monitoring()

    print("=" * 80)
    print("✨ 目标监控示例完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
