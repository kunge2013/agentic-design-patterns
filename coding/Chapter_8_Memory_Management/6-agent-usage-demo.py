"""
LangGraph Agent 实际使用演示
展示如何使用记忆感知智能体处理用户请求
"""
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence
import operator
import os
import httpx
from langchain_openai import ChatOpenAI


# 禁用代理
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'


class AgentState(TypedDict):
    """智能体状态"""
    messages: Annotated[Sequence[str], operator.add]
    user_id: str
    context: dict


class MemoryAwareAgent:
    """记忆感知智能体"""

    def __init__(self, llm=None):
        self.store = InMemoryStore()
        self.llm = llm or ChatOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            http_client=httpx.Client(timeout=30.0)
        )

    def setup_user_memory(self, user_id):
        """设置用户的初始记忆"""
        print(f"=== 设置用户 {user_id} 的记忆 ===\n")

        #. 存储用户偏好
        namespace = (user_id, "preferences")
        self.store.put(namespace, "profile", {
            "name": "学习者小明",
            "language": "Python",
            "level": "intermediate",
            "topics": ["数据结构", "算法", "Web开发"],
            "learning_style": "hands-on"  # 动手实践型
        })

        # 存储学习进度
        self.store.put(namespace, "progress", {
            "completed_lessons": 12,
            "current_topic": "列表推导式",
            "total_lessons": 20
        })

        print("✅ 用户记忆已设置")
        print(f"  姓名: 学习者小明")
        print(f"  语言: Python")
        print(f"  水平: intermediate")
        print(f"  学习方式: 动手实践型\n")

    def create_graph(self):
        """创建记忆感知工作流"""
        workflow = StateGraph(AgentState)

        def retrieve_memory(state):
            """检索用户记忆"""
            user_id = state['user_id']
            namespace = (user_id, "preferences")

            print("\n📖 步骤1: 检索用户记忆...")
            try:
                profile = self.store.get(namespace, "profile")
                progress = self.store.get(namespace, "progress")

                if profile:
                    state['context']['user_profile'] = profile.value
                    print(f"  找到用户: {profile.value['name']}")
                    print(f"  编程语言: {profile.value['language']}")
                    print(f"  当前水平: {profile.value['level']}")

                if progress:
                    state['context']['learning_progress'] = progress.value
                    print(f"  学习进度: {progress.value['completed_lessons']}/{progress.value['total_lessons']}")
            except Exception as e:
                print(f"  ⚠️ 记忆检索失败: {e}")

            return state

        def generate_response(state):
            """生成个性化响应"""
            print("\n💭 步骤2: 生成响应...")

            if not state['messages']:
                print("  ⚠️ 没有用户消息")
                return state

            user_message = state['messages'][-1]
            profile = state['context'].get('user_profile', {})
            progress = state['context'].get('learning_progress', {})

            # 构建个性化提示
            prompt = self._build_personalized_prompt(
                user_message, profile, progress
            )

            try:
                response = self.llm.invoke(prompt)
                state['context']['response'] = response.content
                print(f"  ✅ 响应已生成 (长度: {len(response.content)} 字符)")
                print(f"\n📝 AI 响应:")
                print(f"  {response.content[:200]}..." if len(response.content) > 200 else f"  {response.content}")
            except Exception as e:
                print(f"  ❌ 响应生成失败: {e}")
                state['context']['response'] = f"抱歉，生成响应时出错: {str(e)}"

            return state

        def update_memory(state):
            """更新用户记忆"""
            print("\n💾 步骤3: 更新用户记忆...")

            user_id = state['user_id']
            namespace = (user_id, "interactions")

            # 记录交互
            interaction = {
                "timestamp": __import__('datetime').datetime.now().isoformat(),
                "user_message": state['messages'][-1],
                "agent_response": state['context'].get('response', ''),
                "context_used": {
                    "profile": bool(state['context'].get('user_profile')),
                    "progress": bool(state['context'].get('learning_progress'))
                }
            }

            self.store.put(namespace, f"interaction_{len(state['messages'])}", interaction)
            print("  ✅ 交互已保存到长期记忆")

            return state

        # 添加节点
        workflow.add_node("retrieve_memory", retrieve_memory)
        workflow.add_node("generate_response", generate_response)
        workflow.add_node("update_memory", update_memory)

        # 构建流程
        workflow.add_edge(START, "retrieve_memory")
        workflow.add_edge("retrieve_memory", "generate_response")
        workflow.add_edge("generate_response", "update_memory")
        workflow.add_edge("update_memory", END)

        return workflow.compile()

    def _build_personalized_prompt(self, user_message, profile, progress):
        """构建个性化提示"""
        base_prompt = """你是一个友好的编程学习助手，专门帮助用户学习 Python 编程。

        你的特点:
        - 友好和鼓励的语气
        - 提供清晰、简洁的解释
        - 包含可运行的代码示例
        - 根据用户水平调整难度
        """

        # 添加用户信息
        if profile:
            user_info = f"""
        用户信息:
        {profile.get('name', '未知学员')}
        - 编程语言: {profile.get('language', 'Python')}
        - 当前水平: {profile.get('level', 'beginner')}
        - 学习方式: {profile.get('learning_style', 'balanced')}
        - 兴趣领域: {', '.join(profile.get('topics', []))}
            """
            base_prompt += user_info

        # 添加进度信息
        if progress:
            progress_info = f"""
        学习进度:
        - 完成课程: {progress.get('completed_lessons', 0)}/{progress.get('total_lessons', 0)}
        - 当前主题: {progress.get('current_topic', '未知')}
            """
            base_prompt += progress_info

        # 添加用户消息
        base_prompt += f"""
        用户问题: {user_message}

        请根据用户的背景信息，用适合的方式回答问题。
        如果用户是"动手实践型"，提供更多的代码示例。
        """

        return base_prompt

    def visualize_graph(self, app):
        """可视化流程图"""
        print("\n" + "="*60)
        print("=== 工作流可视化 ===")
        print("="*60 + "\n")

        try:
            graph = app.get_graph()
            graph.print_ascii()
        except Exception as e:
            print(f"可视化失败: {e}")

    def get_user_interactions(self, user_id):
        """获取用户的交互历史"""
        namespace = (user_id, "interactions")
        items = self.store.search(namespace)

        print(f"\n用户 {user_id} 的交互历史:")
        print("-" * 50)

        for item in items:
            data = item.value
            print(f"时间: {data['timestamp'][:19]}")
            print(f"问题: {data['user_message']}")
            print(f"响应: {data['agent_response'][:100]}...")
            print()


def main():
    """主函数 - 演示 agent 的实际使用"""
    print("="*60)
    print("=== LangGraph Agent 实际使用演示 ===")
    print("="*60 + "\n")

    # 检查 API 密钥
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ 未设置 OPENAI_API_KEY 环境变量")
        print("示例: export OPENAI_API_KEY='your-api-key'")
        return

    try:
        # 创建智能体
        agent = MemoryAwareAgent()

        # 设置用户记忆
        agent.setup_user_memory("user_123")

        # 创建工作流
        app = agent.create_graph()

        # 可视化工作流
        agent.visualize_graph(app)

        # 示例1: 第一次交互
        print("\n" + "="*60)
        print("=== 第一次交互 ===")
        print("="*60)

        initial_state = {
            "messages": ["我想学习 Python 中的列表推导式，能给我举个例子吗？"],
            "user_id": "user_123",
            "context": {}
        }

        print(f"\n用户问题: {initial_state['messages'][0]}")

        result = app.invoke(initial_state)

        print("\n" + "="*60)
        print("=== 第二次交互 ===")
        print("="*60)

        # 示例2: 第二次交互（复用记忆）
        second_state = {
            "messages": ["除了列表推导式，还有什么高效处理列表的方法？"],
            "user_id": "user_123",  # 同一个用户
            "context": {}
        }

        print(f"\n用户问题: {second_state['messages'][0]}")

        result2 = app.invoke(second_state)

        # 查看交互历史
        print("\n" + "="*60)
        print("=== 交互历史 ===")
        print("="*60)

        agent.get_user_interactions("user_123")

        print("\n✅ 演示完成！")
        print("记忆感知智能体的优势:")
        print("  1. 记住用户偏好和水平")
        print("  2. 生成个性化响应")
        print("  3. 维持对话上下文")
        print("  4. 跨会话记忆保持")

    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("请检查:")
        print("  1. OPENAI_API_KEY 是否正确设置")
        print("  2. 网络连接是否正常")
        print("  3. 依赖包是否正确安装")


if __name__ == "__main__":
    main()
