"""
记忆管理示例代码
基于 LangChain 和 LangGraph 实现短期和长期记忆管理
"""
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import Dict, List, Any
from datetime import datetime
import json
from llm_config import create_llm


class SimpleMemory:
    """简化的记忆实现 - 替代已废弃的 langchain.memory"""

    def __init__(self, memory_key: str = "chat_history"):
        self.memory_key = memory_key
        self.messages: List[Any] = []

    def add_user_message(self, message: str):
        """添加用户消息"""
        self.messages.append(HumanMessage(content=message))

    def add_ai_message(self, message: str):
        """添加AI消息"""
        self.messages.append(AIMessage(content=message))

    def save_context(self, inputs: Dict, outputs: Dict):
        """保存上下文"""
        if "input" in inputs:
            self.add_user_message(inputs["input"])
        if "output" in outputs:
            self.add_ai_message(outputs["output"])

    def load_memory_variables(self, inputs: Dict = None) -> Dict:
        """加载记忆变量"""
        return {self.memory_key: self.messages}

    @property
    def chat_memory(self):
        """提供 chat_memory 接口"""
        return self


class MemoryManager:
    """记忆管理器 - 综合管理短期和长期记忆"""

    def __init__(self):
        self.short_term_memory = SimpleMemory(
            memory_key="chat_history"
        )
        self.long_term_memory = {}  # 简化的长期记忆存储
        self.session_state = {}  # 会话状态

    def add_user_message(self, message: str):
        """添加用户消息到短期记忆"""
        self.short_term_memory.chat_memory.add_user_message(message)

    def add_ai_message(self, message: str):
        """添加AI消息到短期记忆"""
        self.short_term_memory.chat_memory.add_ai_message(message)

    def update_session_state(self, key: str, value: Any):
        """更新会话状态"""
        self.session_state[key] = value
        self.session_state['last_updated'] = datetime.now().isoformat()

    def save_long_term_memory(self, user_id: str, key: str, value: Any):
        """保存长期记忆"""
        if user_id not in self.long_term_memory:
            self.long_term_memory[user_id] = {}
        self.long_term_memory[user_id][key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }

    def get_long_term_memory(self, user_id: str, key: str) -> Any:
        """获取长期记忆"""
        if user_id in self.long_term_memory and key in self.long_term_memory[user_id]:
            return self.long_term_memory[user_id][key]['value']
        return None

    def get_conversation_context(self) -> Dict[str, Any]:
        """获取完整的对话上下文"""
        return {
            'short_term': self.short_term_memory.load_memory_variables({}),
            'session_state': self.session_state,
            'conversation_messages': [
                {'type': type(msg).__name__, 'content': msg.content}
                for msg in self.short_term_memory.chat_memory.messages
            ]
        }


def demonstrate_short_term_memory():
    """演示短期记忆管理"""
    print("=== 短期记忆管理演示 ===\n")

    memory = SimpleMemory(
        memory_key="chat_history"
    )

    # 模拟对话
    conversation_pairs = [
        ("我叫张三", "你好张三！很高兴认识你。"),
        ("我是一名软件工程师", "听起来是个很棒的职业！你主要使用什么技术栈？"),
        ("我主要使用Python和Java", "Python和Java都是优秀的编程语言！"),
    ]

    for user_input, ai_response in conversation_pairs:
        memory.save_context(
            {"input": user_input},
            {"output": ai_response}
        )
        print(f"用户: {user_input}")
        print(f"AI: {ai_response}\n")

    # 检索记忆
    memory_vars = memory.load_memory_variables({})
    print("当前对话记忆:")
    for msg in memory_vars['chat_history']:
        msg_type = "用户" if isinstance(msg, HumanMessage) else "AI"
        print(f"  {msg_type}: {msg.content}")


def demonstrate_summary_memory():
    """演示记忆总结 - 适用于长对话"""
    print("\n=== 记忆总结演示 ===\n")

    # 简化实现 - 在新版本中 ConversationSummaryMemory 也已废弃
    # 我们使用简单的记忆计数和摘要
    print("记忆总结: 这是一个简化的示例")
    print("在实际应用中，可以使用 langgraph 或其他记忆管理方案")


def demonstrate_session_state():
    """演示会话状态管理"""
    print("\n=== 会话状态管理演示 ===\n")

    manager = MemoryManager()

    # 更新会话状态
    manager.update_session_state('user_name', '李四')
    manager.update_session_state('user_role', '产品经理')
    manager.update_session_state('task_status', 'active')
    manager.update_session_state('step_count', 1)

    print("会话状态:")
    print(json.dumps(manager.session_state, indent=2, ensure_ascii=False))


def demonstrate_long_term_memory():
    """演示长期记忆管理"""
    print("\n=== 长期记忆管理演示 ===\n")

    manager = MemoryManager()

    # 保存用户偏好和历史数据
    user_id = "user_123"
    manager.save_long_term_memory(user_id, 'preferred_language', 'Python')
    manager.save_long_term_memory(user_id, 'experience_level', 'intermediate')
    manager.save_long_term_memory(user_id, 'last_project', '数据分析系统')

    # 获取长期记忆
    print(f"用户 {user_id} 的长期记忆:")
    print(f"  偏好语言: {manager.get_long_term_memory(user_id, 'preferred_language')}")
    print(f"  经验水平: {manager.get_long_term_memory(user_id, 'experience_level')}")
    print(f"  上一个项目: {manager.get_long_term_memory(user_id, 'last_project')}")


def demonstrate_memory_integration():
    """演示记忆的综合使用"""
    print("\n=== 综合记忆管理演示 ===\n")

    manager = MemoryManager()

    # 模拟完整对话流程
    user_id = "user_456"

    # 第一轮对话
    manager.add_user_message("你好，我想学习编程")
    manager.add_ai_message("你好！我可以帮你学习编程。你之前有编程经验吗？")

    # 保存学习进度到长期记忆
    manager.save_long_term_memory(user_id, 'learning_goal', '编程基础')
    manager.save_long_term_memory(user_id, 'current_level', 'beginner')

    # 第二轮对话
    manager.add_user_message("我完全零基础")
    manager.add_ai_message("没关系！我们会从基础开始。建议先学习Python。")

    # 更新状态
    manager.update_session_state('current_lesson', 'Python基础')
    manager.update_session_state('progress', 10)

    # 查看完整上下文
    context = manager.get_conversation_context()
    print("当前对话上下文:")
    print(f"会话状态: {context['session_state']}")
    print(f"长期记忆中的学习目标: {manager.get_long_term_memory(user_id, 'learning_goal')}")


if __name__ == "__main__":
    # 运行所有演示
    try:
        demonstrate_short_term_memory()
        demonstrate_summary_memory()
        demonstrate_session_state()
        demonstrate_long_term_memory()
        demonstrate_memory_integration()
    except Exception as e:
        print(f"错误: {e}")
        print("请确保已正确设置 OPENAI_API_KEY 环境变量")
