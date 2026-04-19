"""
Chapter 15 - 代码示例 1：基础Agent通信 (Basic Agent Communication)

此示例演示两个Agent之间的基础消息传递。
"""
import sys
import os
import time
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
import threading
import queue

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config


class MessageType(Enum):
    """消息类型"""
    TASK = "task"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    ERROR = "error"


@dataclass
class AgentMessage:
    """Agent消息"""
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_agent: str
    to_agent: str
    message_type: MessageType
    content: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    priority: str = "normal"  # normal, high, low
    metadata: Optional[Dict] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "message_type": self.message_type.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentMessage":
        """从字典创建"""
        return cls(
            message_id=data.get("message_id", str(uuid.uuid4())),
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=MessageType(data["message_type"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.now(),
            priority=data.get("priority", "normal"),
            metadata=data.get("metadata")
        )


class Agent:
    """Agent基类"""

    def __init__(self, agent_id: str, name: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.message_queue = queue.Queue()
        self.message_history: List[AgentMessage] = []
        self.running = False
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.message_counter = 0

        print(f"✅ Agent '{self.name}' ({self.agent_id}) 初始化")
        print(f"   能力: {', '.join(self.capabilities)}")

    def register_handler(self, message_type: MessageType, handler: Callable):
        """注册消息处理器"""
        self.message_handlers[message_type] = handler
        print(f"📥 {self.name} 注册处理器: {message_type.value}")

    def start(self):
        """启动Agent"""
        self.running = True
        print(f"🚀 Agent '{self.name}' 已启动")

        # 在后台线程运行消息处理
        self.message_thread = threading.Thread(target=self._process_messages, daemon=True)
        self.message_thread.start()

    def stop(self):
        """停止Agent"""
        self.running = False
        print(f"⏸️  Agent '{self.name}' 已停止")

    def send_message(self, to_agent_id: str, message_type: MessageType, content: Dict[str, Any], priority: str = "normal"):
        """
        发送消息（通常通过消息总线）

        Args:
            to_agent_id: 目标Agent ID
            message_type: 消息类型
            content: 消息内容
            priority: 消息优先级
        """
        # 创建消息
        message = AgentMessage(
            from_agent=self.agent_id,
            to_agent=to_agent_id,
            message_type=message_type,
            content=content,
            priority=priority
        )

        print(f"📤 {self.name} 发送消息 -> {to_agent_id}")
        print(f"   类型: {message_type.value}")
        print(f"   优先级: {priority}")

        # 在实际应用中，这里会通过消息总线发送
        # 对于此示例，我们记录消息
        self.message_history.append(message)

        return message

    def receive_message(self, message: AgentMessage):
        """
        接收消息

        Args:
            message: 接收的消息
        """
        print(f"📥 {self.name} 收到消息 <- {message.from_agent}")
        print(f"   类型: {message.message_type.value}")
        print(f"   内容: {message.content}")

        # 放入队列
        self.message_queue.put(message)
        self.message_counter += 1

    def _process_messages(self):
        """处理消息队列"""
        while self.running:
            try:
                # 从队列获取消息（超时1秒）
                message = self.message_queue.get(timeout=1.0)

                # 调用对应的处理器
                handler = self.message_handlers.get(message.message_type)
                if handler:
                    try:
                        response = handler(message)
                        if response:
                            print(f"✅ 处理器返回响应: {response}")
                    except Exception as e:
                        print(f"❌ 处理器错误: {str(e)}")
                        self._send_error(message, str(e))
                else:
                    print(f"⚠️  没有找到 {message.message_type.value} 的处理器")

            except queue.Empty:
                # 队列为空，继续等待
                continue
            except Exception as e:
                print(f"❌ 消息处理错误: {str(e)}")

    def _send_error(self, original_message: AgentMessage, error_message: str):
        """发送错误响应"""
        error_message_obj = AgentMessage(
            from_agent=self.agent_id,
            to_agent=original_message.from_agent,
            message_type=MessageType.ERROR,
            content={
                "original_message_id": original_message.message_id,
                "error": error_message
            }
        )
        print(f"❌ 发送错误响应: {error_message}")

    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "capabilities": self.capabilities,
            "messages_sent": len(self.message_history),
            "messages_received": self.message_counter,
            "queue_size": self.message_queue.qsize(),
            "is_running": self.running
        }


class MessageBus:
    """消息总线（用于Agent间通信）"""

    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_log: List[AgentMessage] = []
        print("✅ 消息总线初始化")

    def register_agent(self, agent: Agent):
        """注册Agent"""
        self.agents[agent.agent_id] = agent
        print(f"📝 注册Agent: {agent.name} ({agent.agent_id})")

    defunregister_agent(self, agent_id: str):
        """注销Agent"""
        if agent_id in self.agents:
            agent = self.agents.pop(agent_id)
            print(f"🗑️  注销Agent: {agent.name} ({agent_id})")
            agent.stop()

    def route_message(self, message: AgentMessage):
        """
        路由消息到目标Agent

        Args:
            message: 要路由的消息
        """
        self.message_log.append(message)

        # 查找目标Agent
        if message.to_agent not in self.agents:
            print(f"❌ Agent {message.to_agent} 不存在")
            return False

        target_agent = self.agents[message.to_agent]

        # 传递消息
        target_agent.receive_message(message)
        return True

    def broadcast(self, from_agent_id: str, message_type: MessageType, content: Dict[str, Any], exclude: Optional[List[str]] = None):
        """
        广播消息到所有Agent

        Args:
            from_agent_id: 发送方Agent ID
            message_type: 消息类型
            content: 消息内容
            exclude: 要排除的Agent ID列表
        """
        exclude = exclude or []
        exclude.append(from_agent_id)

        for agent_id, agent in self.agents.items():
            if agent_id not in exclude:
                message = AgentMessage(
                    from_agent=from_agent_id,
                    to_agent=agent_id,
                    message_type=message_type,
                    content=content
                )
                self.route_message(message)

    def get_message_log(self) -> List[Dict[str, Any]]:
        """获取消息日志"""
        return [msg.to_dict() for msg in self.message_log]


# 示例Agent
class DataAnalyzerAgent(Agent):
    """数据分析Agent"""

    def __init__(self):
        super().__init__(
            agent_id="data_analyzer_001",
            name="数据分析Agent",
            capabilities=["data_analysis", "statistics", "reporting"]
        )

        # 注册消息处理器
        self.register_handler(MessageType.TASK, self._handle_task)
        self.register_handler(MessageType.RESPONSE, self._handle_response)

    def _handle_task(self, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """处理任务消息请求"""
        task = message.content.get("task")
        data = message.content.get("data")

        print(f"\n📊 执行任务: {task}")
        print(f"   数据: {data}")

        # 模拟数据分析
        time.sleep(1)

        # 返回分析结果
        result = {
            "status": "success",
            "task": task,
            "analysis": {
                "total_records": len(data) if isinstance(data, list) else 1,
                "average": sum(data) / len(data) if isinstance(data, list) and data else 0,
                "processed_at": datetime.now().isoformat()
            }
        }

        print(f"✅ 分析完成: {result}")

        return result

    def _handle_response(self(self, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """处理响应消息"""
        print(f"📥 收到响应: {message.content}")
        return None


class ReportGeneratorAgent(Agent):
    """报告生成Agent"""

    def __init__(self):
        super().__init__(
            agent_id="report_generator_001",
            name="报告生成Agent",
            capabilities=["report_generation", "formatting", "export"]
        )

        # 注册消息处理器
        self.register_handler(MessageType.TASK, self._handle_task)
        self.register_handler(MessageType.RESPONSE, self._handle_response)

    def _handle_task(self, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """处理任务消息请求"""
        task = message.content.get("task")
        analysis_data = message.content.get("data")

        print(f"\n📝 生成报告: {task}")
        print(f"   分析数据: {analysis_data}")

        # 模拟报告生成
        time.sleep(1.5)

        # 返回报告结果
        result = {
            "status": "success",
            "task": task,
            "report": {
                "title": f"分析报告 - {task}",
                "summary": f"基于 {analysis_data.get('total_records', 0)} 条记录生成",
                "average_value": analysis_data.get('average', 0),
                "generated_at": datetime.now().isoformat(),
                "format": "PDF"
            }
        }

        print(f"✅ 报告生成完成: {result}")

        return result

    def _handle_response(self, message: AgentMessage) -> Optional[Dict[str, Any]]:
        """处理响应消息"""
        print(f"📥 收到响应: {message.content}")
        return None


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 15 - 示例 1：基础Agent通信 (Basic Agent Communication)")
    print("=" * 80)
    print()
    print("🤖 此示例演示两个Agent之间的基础消息传递")
    print()

    # 创建消息总线
    message_bus = MessageBus()

    print("\n" + "=" * 80)
    print("创建和注册Agent")
    print("=" * 80)
    print()

    # 创建Agent
    data_analyzer = DataAnalyzerAgent()
    report_generator = ReportGeneratorAgent()

    # 注册到消息总线
    message_bus.register_agent(data_analyzer)
    message_bus.register_agent(report_generator)

    print("\n" + "=" * 80)
    print("启动Agent")
    print("=" * 80)
    print()

    # 启动Agent
    data_analyzer.start()
    report_generator.start()

    print("\n" + "=" * 80)
    print("Agent通信示例")
    print("=" * 80)
    print()

    # 示例 1: 发送分析任务
    print("📤 发送分析任务到数据分析Agent...")

    task_message = AgentMessage(
        from_agent="orchestrator",
        to_agent=data_analyzer.agent_id,
        message_type=MessageType.TASK,
        content={
            "task": "sales_analysis",
            "data": [100, 200, 150, 300, 250, 180, 220, 280]
        }
    )

    message_bus.route_message(task_message)

    # 等待处理
    time.sleep(2)

    # 示例 2: 发送报告生成任务
    print("\n📤 发送报告生成任务到报告生成Agent...")

    report_message = AgentMessage(
        from_agent="orchestrator",
        to_agent=report_generator.agent_id,
        message_type=MessageType.TASK,
        content={
            "task": "generate_report",
            "data": {
                "total_records": 8,
                "average": 210.0,
                "analysis_type": "sales"
            }
        }
    )

    message_bus.route_message(report_message)

    # 等待处理
    time.sleep(2)

    print("\n" + "=" * 80)
    print("Agent统计信息")
    print("=" * 80)
    print()

    # 显示统计信息
    for agent in [data_analyzer, report_generator]:
        stats = agent.get_stats()
        print(f"\nAgent: {stats['name']}")
        print(f"  ID: {stats['agent_id']}")
        print(f"  能力: {', '.join(stats['capabilities'])}")
        print(f"  发送的消息数: {stats['messages_sent']}")
        print(f"  接收的消息数: {stats['messages_received']}")
        print(f"  队列大小: {stats['queue_size']}")
        print(f"  运行状态: {stats['is_running']}")

    print("\n" + "=" * 80)
    print("消息日志")
    print("=" * 80)
    print()

    # 显示消息日志
    message_log = message_bus.get_message_log()
    for i, msg in enumerate(message_log, 1):
        print(f"\n消息 #{i}:")
        print(f"  ID: {msg['message_id']}")
        print(f"  从: {msg['from_agent']} -> 到: {msg['to_agent']}")
        print(f"  类型: {msg['message_type']}")
        print(f"  时间: {msg['timestamp']}")

    # 停止Agent
    print("\n" + "=" * 80)
    print("停止Agent")
    print("=" * 80)
    print()

    data_analyzer.stop()
    report_generator.stop()

    time.sleep(1)

    print("\n" + "=" * 80)
    print("✨ 基础Agent通信示例完成")
    print("=" * 80)


if __name__ == "__main__":
    main()
