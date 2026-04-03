"""
LangGraph 记忆存储示例
演示如何在 LangGraph 中使用存储来管理长期记忆
"""
from langgraph.store.memory import InMemoryStore
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, List, Sequence
import operator
from llm_config import create_llm


class AgentState(TypedDict):
    """智能体状态"""
    messages: Annotated[Sequence[str], operator.add]
    user_id: str
    context: dict


class LangGraphMemoryManager:
    """LangGraph 记忆管理器"""

    def __init__(self):
        # 创建带有嵌入索引的存储
        self.store = InMemoryStore()
        self.llm = create_llm(temperature=0.3)

    def semantic_memory_storage(self):
        """演示语义记忆存储（事实和概念）"""
        print("=== 语义记忆存储演示 ===\n")

        # 定义命名空间
        user_id = "user_123"
        namespace = (user_id, "semantic_memory")

        # 存储用户偏好和事实
        self.store.put(
            namespace,
            "preferences",
            {
                "language": "Python",
                "difficulty": "intermediate",
                "topics": ["机器学习", "数据分析", "Web开发"]
            }
        )

        self.store.put(
            namespace,
            "learning_progress",
            {
                "completed_lessons": 15,
                "current_lesson": "数据结构",
                "total_lessons": 30
            }
        )

        # 检索记忆
        preferences = self.store.get(namespace, "preferences")
        progress = self.store.get(namespace, "learning_progress")

        print("用户偏好:")
        print(f"  编程语言: {preferences.value['language']}")
        print(f"  难度水平: {preferences.value['difficulty']}")
        print(f"  兴趣话题: {preferences.value['topics']}")

        print("\n学习进度:")
        print(f"  完成课程: {progress.value['completed_lessons']}/{progress.value['total_lessons']}")
        print(f"  当前课程: {progress.value['current_lesson']}")

        # 使用LLM基于用户偏好生成学习建议
        print("\n基于用户偏好的AI建议:")
        prompt = f"""
        你是一个编程学习助手。根据以下用户信息，给出针对性的学习建议：
        - 编程语言: {preferences.value['language']}
        - 难度水平: {preferences.value['difficulty']}
        - 兴趣话题: {', '.join(preferences.value['topics'])}
        - 完成课程: {progress.value['completed_lessons']}/{progress.value['total_lessons']}
        - 当前课程: {progress.value['current_lesson']}

        请给出3条具体的建议，每条不超过50字。
        """
        try:
            response = self.llm.invoke(prompt)
            print(response.content)
        except Exception as e:
            print(f"LLM调用失败: {e}")

    def episodic_memory_storage(self):
        """演示情景记忆存储（经历和事件）"""
        print("\n=== 情景记忆存储演示 ===\n")

        user_id = "user_123"
        namespace = (user_id, "episodic_memory")

        # 存储重要的学习事件
        learning_events = [
            {
                "event_id": "event_001",
                "description": "完成第一个Python项目",
                "date": "2026-03-15",
                "outcome": "成功",
                "skills_gained": ["基础语法", "变量", "循环"]
            },
            {
                "event_id": "event_002",
                "description": "解决数据分析问题",
                "date": "2026-03-20",
                "outcome": "成功",
                "skills_gained": ["pandas", "数据清洗", "可视化"]
            },
            {
                "event_id": "event_003",
                "description": "机器学习模型训练失败",
                "date": "2026-03-25",
                "outcome": "失败",
                "lessons_learned": "需要更多数据预处理"
            }
        ]

        for event in learning_events:
            self.store.put(namespace, event['event_id'], event)

        # 搜索特定类型的记忆
        print("最近的学习事件:")
        items = self.store.search(namespace, query="学习项目")
        for item in items:
            print(f"  - {item.value['description']}: {item.value['outcome']}")

    def procedural_memory_storage(self):
        """演示程序记忆存储（规则和指令）"""
        print("\n=== 程序记忆存储演示 ===\n")

        user_id = "user_123"
        namespace = (user_id, "procedural_memory")

        # 存储智能体指令和规则
        agent_instructions = {
            "system_prompt": """你是一个编程学习助手，专门帮助用户学习Python编程。

指导原则：
1. 鼓励渐进式学习，从基础到高级
2. 提供具体的代码示例和解释
3. 针对用户水平调整难度
4. 鼓励实践和动手编程
5. 耐心回答问题，避免技术术语过多

响应风格：
- 友好和鼓励的语气
- 提供清晰、简洁的解释
- 包含可运行的代码示例
- 建议进一步学习的资源""",
            "interaction_rules": [
                "每次回答后询问是否需要更多解释",
                "遇到错误时提供调试建议",
                "推荐相关的练习项目"
            ]
        }

        self.store.put(namespace, "agent_instructions", agent_instructions)

        # 检索指令
        instructions = self.store.get(namespace, "agent_instructions")
        print("智能体系统指令:")
        print(instructions.value['system_prompt'][:200] + "...")

        # 使用LLM演示基于存储的指令生成响应
        print("\n=== 测试智能体响应 ===")
        test_question = "我想学习Python中的列表推导式，能给我举个例子吗？"

        # 使用存储的系统提示构建完整提示
        full_prompt = f"""
        {instructions.value['system_prompt']}

        用户问题: {test_question}

        请遵循上述指导原则回答。
        """

        try:
            print(f"\n用户问题: {test_question}")
            print("\n智能体响应:")
            response = self.llm.invoke(full_prompt)
            print(response.content)
        except Exception as e:
            print(f"LLM调用失败: {e}")

    def create_memory_aware_agent(self):
        """创建具有记忆感知能力的智能体"""
        print("\n" + "="*50)
        print("=== 记忆感知智能体示例 ===")
        print("="*50 + "\n")

        # 创建状态图
        workflow = StateGraph(AgentState)

        # 定义节点
        def retrieve_memory_node(state: AgentState):
            """检索长期记忆节点"""
            user_id = state['user_id']
            namespace = (user_id, "semantic_memory")

            try:
                preferences = self.store.get(namespace, "preferences")
                if preferences:
                    state['context']['user_preferences'] = preferences.value
            except:
                pass

            print(f"为用户 {user_id} 检索记忆...")
            return state

        def process_with_context_node(state: AgentState):
            """使用上下文处理请求节点"""
            user_preferences = state['context'].get('user_preferences', {})

            print("处理请求时使用以下上下文:")
            if user_preferences:
                print(f"  用户语言偏好: {user_preferences.get('language', '未知')}")
                print(f"  用户难度水平: {user_preferences.get('difficulty', '未知')}")

            # 如果有消息，使用LLM生成个性化响应
            if state['messages']:
                last_message = state['messages'][-1]
                print(f"\n用户消息: {last_message}")

                # 构建上下文感知的提示
                context_info = ""
                if user_preferences:
                    context_info = f"""
                    用户偏好信息:
                    - 编程语言: {user_preferences.get('language', '未知')}
                    - 难度水平: {user_preferences.get('difficulty', '未知')}
                    - 兴趣话题: {', '.join(user_preferences.get('topics', []))}
                    """

                prompt = f"""
                你是一个个性化的编程学习助手。

                {context_info}

                请根据用户的偏好信息，用适合的方式回答用户的问题或请求。

                用户说: {last_message}
                """

                try:
                    response = self.llm.invoke(prompt)
                    print(f"\nAI响应: {response.content[:200]}...")
                    state['context']['last_response'] = response.content
                except Exception as e:
                    print(f"LLM调用失败: {e}")

            return state

        def update_memory_node(state: AgentState):
            """更新记忆节点"""
            user_id = state['user_id']
            namespace = (user_id, "episodic_memory")

            # 记录交互
            interaction = {
                "event_id": f"interaction_{len(state['messages'])}",
                "messages": state['messages'][-1] if state['messages'] else "",
                "timestamp": datetime.now().isoformat()
            }

            self.store.put(namespace, interaction['event_id'], interaction)
            print("交互已保存到长期记忆")

            return state

        # 添加节点
        workflow.add_node("retrieve_memory", retrieve_memory_node)
        workflow.add_node("process_with_context", process_with_context_node)
        workflow.add_node("update_memory", update_memory_node)

        # 添加边
        workflow.add_edge(START, "retrieve_memory")
        workflow.add_edge("retrieve_memory", "process_with_context")
        workflow.add_edge("process_with_context", "update_memory")
        workflow.add_edge("update_memory", END)

        # 编译图
        app = workflow.compile()

        # 可视化图结构
        self.visualize_graph(app)

        return app

    def demonstrate_cross_session_memory(self):
        """演示跨会话记忆"""
        print("\n=== 跨会话记忆演示 ===\n")

        user_id = "user_shared"
        app_namespace = (user_id, "application_data")

        # 在第一个会话中保存数据
        print("会话1: 保存用户数据")
        self.store.put(app_namespace, "user_profile", {
            "name": "王五",
            "email": "wangwu@example.com",
            "preferences": {
                "theme": "dark",
                "language": "zh-CN"
            }
        })

        # 在第二个会话中访问相同数据
        print("\n会话2: 访问用户数据")
        profile = self.store.get(app_namespace, "user_profile")
        if profile:
            print(f"用户名: {profile.value['name']}")
            print(f"邮箱: {profile.value['email']}")
            print(f"主题偏好: {profile.value['preferences']['theme']}")

    def visualize_graph(self, app):
        """可视化 LangGraph 流程"""
        print("\n" + "="*50)
        print("=== LangGraph 流程可视化 ===")
        print("="*50 + "\n")

        try:
            # 方法1: 打印 ASCII 格式的图
            print("1. ASCII 格式流程图:")
            print("-" * 30)
            app.get_graph().print_ascii()

            # 方法2: 获取图结构信息
            print("\n2. 图结构信息:")
            print("-" * 30)
            graph = app.get_graph()

            # 获取所有节点
            nodes = list(graph.nodes)
            print(f"节点总数: {len(nodes)}")
            print(f"节点列表: {nodes}")

            # 获取所有边
            edges = list(graph.edges)
            print(f"\n边总数: {len(edges)}")
            print("边连接关系:")
            for i, (source, target) in enumerate(edges, 1):
                print(f"  {i}. {source} → {target}")

            # 方法3: 生成 Mermaid 格式（可用于 Markdown 文档）
            print("\n3. Mermaid 格式（用于文档）:")
            print("-" * 30)
            try:
                mermaid_code = app.get_graph().draw_mermaid()
                print(mermaid_code)
            except Exception as e:
                print(f"Mermaid 生成失败: {e}")

            # 方法4: 获取节点详情
            print("\n4. 节点详细信息:")
            print("-" * 30)
            for node in nodes:
                print(f"  节点: {node}")
                if hasattr(graph, 'nodes'):
                    node_data = graph.nodes.get(node)
                    if node_data:
                        print(f"    数据: {node_data}")

        except Exception as e:
            print(f"可视化失败: { {e}}")
            print("提示: 部分可视化功能可能需要额外的依赖库")

    def export_graph_image(self, app, filename="graph", format="png"):
        """导出图为图片格式（需要安装 graphviz）"""
        try:
            # 导出为 PNG 或 SVG 格式
            if format == "png":
                app.get_graph().draw_png(f"{filename}.png")
            else:
                app.get_graph().draw_svg(f"{filename}.svg")
            print(f"\n✅ 图已导出为 {filename}.{format}")
        except ImportError:
            print(f"\n⚠️  需要 graphviz 库支持")
            print("安装方法: pip install graphviz")
            print("还需要安装系统级 Graphviz: https://graphviz.org/download/")
        except Exception as e:
            print(f"\n❌ 导出失败: {e}")


if __name__ == "__main__":
    from datetime import datetime
    try:
        manager = LangGraphMemoryManager()

        # 运行所有演示
        manager.semantic_memory_storage()
        manager.episodic_memory_storage()
        manager.procedural_memory_storage()
        manager.demonstrate_cross_session_memory()

        # 创建记忆感知智能体
        agent = manager.create_memory_aware_agent()

        # 实际使用 agent 处理用户请求
        print("\n" + "="*50)
        print("=== 使用记忆感知智能体 ===")
        print("="*50 + "\n")

        # 准备初始状态
        initial_state = {
            "messages": ["我想学习 Python 中的列表推导式，能给我举个例子吗？"],
            "user_id": "user_123",  # 使用前面存储用户偏好的同一个用户
            "context": {}
        }

        print("用户请求:")
        print(f"  {initial_state['messages'][0]}")
        print(f"  用户ID: {initial_state['user_id']}\n")

        print("执行智能体流程...")
        print("-" * 50)

        # 调用 agent 处理请求
        result = agent.invoke(initial_state)

        print("-" * 50)
        print("\n✅ 智能体执行完成！")

        # 显示结果
        print("\n最终状态:")
        print(f"  消息数: {len(result.get('messages', []))}")
        print(f"  用户ID: {result.get('user_id', '未知')}")
        print(f"  上下文: {result.get('context', {})}")

        # 另一个示例请求
        print("\n" + "="*50)
        print("=== 第二个示例请求 ===")
        print("="*50 + "\n")

        second_state = {
            "messages": ["如何提高我的编程技能？"],
            "user_id": "user_123",  # 同一个用户，会使用之前的记忆
            "context": {}
        }

        print("用户请求:")
        print(f"  {second_state['messages'][0]}")

        print("\n执行智能体流程...")
        print("-" * 50)

        result2 = agent.invoke(second_state)

        print("-" * 50)
        print("\n✅ 智能体执行完成！")

        # 可选：导出图形文件

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已正确设置 OPENAI_API_KEY 环境变量")
