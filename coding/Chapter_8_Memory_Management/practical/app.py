"""
Web 智能学习助手系统 - 基于记忆管理的个性化学习平台

这是一个完整的 Web 应用，展示了 Agentic 设计模式中记忆管理的实际应用。

技术栈：
- Flask: Web 后端框架
- LangGraph: 记忆感知智能体
- InMemoryStore: 记忆管理
- OpenAI API: 自然语言处理
"""
from flask import Flask, render_template, request, jsonify, session
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence
import operator
import os
import httpx
from datetime import datetime
import uuid
from llm_config import create_llm

# 禁用代理
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'


app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# 全局记忆存储
memory_store = InMemoryStore()


class AgentState(TypedDict):
    """智能体状态"""
    messages: Annotated[Sequence[str], operator.add]
    user_id: str
    request_type: str
    context: dict


class LearningAssistantAgent:
    """学习助手智能体"""

    def __init__(self):
        """初始化智能体"""
        self.store = memory_store
        try:
            self.llm = create_llm(temperature=0.7)
            print("✅ LLM 初始化成功")
        except Exception as e:
            print(f"⚠️ LLM 初始化失败: {e}")
            self.llm = None

        self.setup_system_memory()

    def setup_system_memory(self):
        """设置系统程序记忆"""
        namespace = ("system", "procedural_memory")

        # 教学原则
        self.store.put(namespace, "teaching_principles", {
            "scaffolding": "提供渐进式帮助",
            "active_learning": "鼓励主动学习",
            "personalization": "个性化内容调整"
        })

    def create_workflow(self):
        """创建记忆感知工作流"""
        workflow = StateGraph(AgentState)

        def retrieve_context(state):
            """检索用户上下文"""
            user_id = state['user_id']
            namespace = (user_id, "semantic_memory")

            # 获取用户画像
            profile = self.store.get(namespace, "profile")
            if profile:
                state['context']['user_profile'] = profile.value
            else:
                state['context']['user_profile'] = None

            # 获取学习历史
            namespace_history = (user_id, "episodic_memory")
            history_items = self.store.search(namespace_history)
            state['context']['recent_history'] = [item.value for item in history_items[-5:]]

            return state

        def process_request(state):
            """处理请求"""
            if not state['messages']:
                return state

            profile = state['context'].get('user_profile')
            request_type = state['request_type']
            message = state['messages'][-1]

            # 根据 LLM 可用性选择处理方式
            if self.llm:
                response = self.generate_llm_response(message, request_type, profile)
            else:
                response = self.generate_mock_response(message, request_type, profile)

            state['context']['response'] = response
            return state

        def update_memory(state):
            """更新记忆"""
            user_id = state['user_id']
            request_type = state['request_type']
            response = state['context'].get('response', '')

            # 记录交互
            if request_type == 'question':
                self.record_interaction(user_id, state['messages'][-1], response)

            return state

        # 构建工作流
        workflow.add_node("retrieve_context", retrieve_context)
        workflow.add_node("process_request", process_request)
        workflow.add_node("update_memory", update_memory)

        workflow.add_edge(START, "retrieve_context")
        workflow.add_edge("retrieve_context", "process_request")
        workflow.add_edge("process_request", "update_memory")
        workflow.add_edge("update_memory", END)

        return workflow.compile()

    def generate_llm_response(self, message, request_type, profile):
        """使用 LLM 生成响应"""
        context = ""
        if profile:
            context = f"""
            用户信息：
            - 姓名：{profile.get('name', '未知')}
            - 水平：{profile.get('level', 'beginner')}
            - 目标：{profile.get('goal', '学习编程')}
            """

        prompt = f"""你是一个专业的编程学习助手。

        {context}

        用户消息：{message}

        请根据用户水平和目标提供有帮助的回复。
        保持友好和鼓励的语气。
        """

        try:
            response = self.llm.invoke(prompt)
            return response.content
        except Exception as e:
            return f"生成响应时出错：{str(e)}"

    def generate_mock_response(self, message, request_type, profile):
        """生成模拟响应（无 LLM 时）"""
        name = profile.get('name', '同学') if profile else '同学'
        level = profile.get('level', 'beginner') if profile else 'beginner'

        if request_type == 'learn':
            return f"""你好 {name}！

            基于你的水平 ({level})，我建议：

            📚 学习路径：
            1. Python 基础语法（变量、数据类型、控制流）
            2. 数据结构（列表、字典、集合）
            3. 函数和模块化编程
            4. 实际项目练习

            💪 实践建议：
            - 每天坚持写代码
            - 完成小项目练习
            - 参与编程社区

            需要详细解释任何部分吗？"""

        elif request_type == 'question':
            return f"""好的 {name}，让我来帮助你！

            关于你的问题："{message}"

            💡 回答：
            这里是一个简要的回答。概念解释需要理解基本原理，
            代码示例可以帮助理解实际应用。

            📝 代码示例：
            ```python
            # 示例代码
            def example_function():
                result = "Hello, World!"
                return result
            ```

            🔍 学习要点：
            - 理解代码逻辑
            - 多练习不同场景
            - 注意错误和调试技巧

            需要更详细的解释吗？"""

        elif request_type == 'progress':
            history_count = len(self._get_user_history(profile['user_id'] if profile else 'guest'))
            return f"""📊 学习进度报告

            👤 学习者：{name}
            📈 当前水平：{level}
            📚 学习会话：{history_count} 次

            💡 学习建议：
            - 保持持续学习的习惯
            - 定期复习已学内容
            - 尝试实际项目练习

            继续加油！💪"""

        else:
            return f"""你好 {name}！我可以帮你：

            1. 📚 制定学习计划
            2. ❓ 解答技术问题
            3. 📊 查询学习进度
            4. 💾 记录学习会话

            有什么需要帮助的吗？"""

    def record_interaction(self, user_id, question, answer):
        """记录交互到情景记忆"""
        namespace = (user_id, "episodic_memory")

        interaction_id = f"qa_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        self.store.put(namespace, interaction_id, {
            "id": interaction_id,
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer
        })

    def _get_user_history(self, user_id):
        """获取用户历史"""
        namespace = (user_id, "episodic_memory")
        items = self.store.search(namespace)
        return [item.value for item in items]


# 全局智能体实例
assistant_agent = None


def get_agent():
    """获取或创建智能体实例"""
    global assistant_agent
    if assistant_agent is None:
        assistant_agent = LearningAssistantAgent()
    return assistant_agent


# ==================== Web 路由 ====================

@app.route('/')
def index():
    """首页"""
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

    return render_template('index.html')


@app.route('/setup_profile', methods=['GET', 'POST'])
def setup_profile():
    """设置用户画像"""
    if request.method == 'GET':
        # 检查是否已存在画像
        user_id = session.get('user_id')
        namespace = (user_id, "semantic_memory")
        profile = memory_store.get(namespace, "profile")

        if profile:
            return jsonify({
                'success': True,
                'profile': profile.value
            })
        return jsonify({'success': False})

    elif request.method == 'POST':
        data = request.json
        user_id = session.get('user_id')

        # 存储用户画像
        namespace = (user_id, "semantic_memory")
        memory_store.put(namespace, "profile", {
            "user_id": user_id,
            "name": data.get('name', ''),
            "level": data.get('level', 'beginner'),
            "goal": data.get('goal', '学习编程'),
            "created_at": datetime.now().isoformat()
        })

        return jsonify({
            'success': True,
            'message': '用户画像创建成功！'
        })


@app.route('/learning_request', methods=['POST'])
def learning_request():
    """处理学习请求"""
    data = request.json
    user_id = session.get('user_id')
    message = data.get('message', '')
    request_type = data.get('type', 'learn')

    # 创建智能体工作流
    agent = get_agent()
    workflow = agent.create_workflow()

    # 准备状态
    state = {
        "messages": [message],
        "user_id": user_id,
        "request_type": request_type,
        "context": {}
    }

    # 执行工作流
    try:
        result = workflow.invoke(state)
        response = result['context'].get('response', '抱歉，无法生成响应')

        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/record_session', methods=['POST'])
def record_session():
    """记录学习会话"""
    data = request.json
    user_id = session.get('user_id')

    namespace = (user_id, "episodic_memory")
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    memory_store.put(namespace, session_id, {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "topic": data.get('topic', '未知'),
        "duration": data.get('duration', 0),
        "notes": data.get('notes', '')
    })

    return jsonify({
        'success': True,
        'session_id': session_id
    })


@app.route('/get_history', methods=['GET'])
def get_history():
    """获取学习历史"""
    user_id = session.get('user_id')
    namespace = (user_id, "episodic_memory")

    items = memory_store.search(namespace)
    history = sorted(
        [item.value for item in items],
        key=lambda x: x['timestamp'],
        reverse=True
    )

    return jsonify({
        'success': True,
        'history': history[:10]
    })


@app.route('/get_stats', methods=['GET'])
def get_stats():
    """获取学习统计"""
    user_id = session.get('user_id')

    # 获取用户画像
    namespace_profile = (user_id, "semantic_memory")
    profile = memory_store.get(namespace_profile, "profile")

    # 获取学习历史
    namespace_history = (user_id, "episodic_memory")
    history_items = memory_store.search(namespace_history)

    stats = {
        'total_sessions': len(history_items),
        'total_interactions': len([h for h in history_items if 'question' in h.value]),
        'profile': '存在' if profile else '不存在'
    }

    return jsonify({
        'success': True,
        'stats': stats
    })


@app.route('/system_info', methods=['GET'])
def system_info():
    """获取系统信息"""
    return jsonify({
        'success': True,
        'info': {
            'system_name': '智能学习助手系统',
            'version': '1.0.0',
            'features': [
                '语义记忆：用户画像管理',
                '情景记忆：学习历史追踪',
                '程序记忆：教学策略应用',
                '记忆感知智能体：个性化响应生成',
                '跨会话记忆：持久化数据存储'
            ],
            'llm_available': assistant_agent is not None and assistant_agent.llm is not None,
            'memory_types': ['semantic', 'episodic', 'procedural']
        }
    })


if __name__ == '__main__':
    print("="*60)
    print("🌐 Web 智能学习助手系统启动中...")
    print("="*60)
    print("\n💡 启动信息:")
    print("  - 智能体: 记忆感知学习助手")
    print("  - 记忆管理: 三种记忆类型（语义、情景、程序）")
    print("  - 持久化: InMemoryStore")
    print("\n🔗 访问地址: http://localhost:5000")
    print("⚠️  注意: 生产环境请更改 secret_key\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
