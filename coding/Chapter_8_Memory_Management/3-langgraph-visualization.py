"""
LangGraph 流程可视化演示（无需 API 密钥）
演示如何可视化 LangGraph 的流程结构
"""
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence
import operator


class AgentState(TypedDict):
    """智能体状态"""
    messages: Annotated[Sequence[str], operator.add]
    user_id: str
    context: dict


def create_sample_graph():
    """创建一个示例流程图"""
    workflow = StateGraph(AgentState)

    # 定义节点
    def retrieve_memory_node(state):
        """检索长期记忆节点"""
        print(f"节点1: 为用户 {state['user_id']} 检索记忆...")
        return state

    def process_with_context_node(state):
        """使用上下文处理请求节点"""
        print("节点2: 使用上下文处理请求...")
        return state

    def update_memory_node(state):
        """更新记忆节点"""
        print("节点3: 更新长期记忆...")
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
    return workflow.compile()


def visualize_graph(app):
    """可视化 LangGraph 流程"""
    print("\n" + "="*60)
    print("=== LangGraph 流程可视化 ===")
    print("="*60 + "\n")

    try:
        # 方法1: 打印 ASCII 格式的图
        print("1. ASCII 格式流程图:")
        print("-" * 40)
        app.get_graph().print_ascii()

        # 方法2: 获取图结构信息
        print("\n2. 图结构信息:")
        print("-" * 40)
        graph = app.get_graph()

        # 获取所有节点
        nodes = list(graph.nodes)
        print(f"节点总数: {len(nodes)}")
        print(f"节点列表: {nodes}")

        # 获取所有边
        edges = list(graph.edges)
        print(f"\n边总数: {len(edges)}")
        print("边连接关系:")
        for i, edge in enumerate(edges, 1):
            # 边是一个元组，处理不同的情况
            if isinstance(edge, tuple):
                if len(edge) == 2:
                    source, target = edge
                    print(f"  {i}. {source} → {target}")
                elif len(edge) == 3:
                    source, target, data = edge
                    print(f"  {i}. {source} → {target} (数据: {data})")
            else:
                print(f"  {i}. {edge}")

        # 方法3: 生成 Mermaid 格式（可用于 Markdown 文档）
        print("\n3. Mermaid 格式（用于文档）:")
        print("-" * 40)
        try:
            mermaid_code = app.get_graph().draw_mermaid()
            print(mermaid_code)
        except Exception as e:
            print(f"Mermaid 生成失败: {e}")

        # 方法4: 获取节点详情
        print("\n4. 节点详细信息:")
        print("-" * 40)
        for node in nodes:
            print(f"  节点: {node}")

    except Exception as e:
        print(f"可视化失败: {e}")
        print("提示: 部分可视化功能可能需要额外的依赖库")


def export_graph_image(app, filename="graph", format="png"):
    """导出图为图片格式（需要安装 graphviz）"""
    try:
        graph = app.get_graph()

        # 尝试不同的导出方法
        if format == "png":
            if hasattr(graph, 'draw_mermaid_png'):
                graph.draw_mermaid_png(f"{filename}.png")
                print(f"\n✅ 图已导出为 {filename}.png")
            elif hasattr(graph, 'draw_png'):
                graph.draw_png(f"{filename}.png")
                print(f"\n✅ 图已导出为 {filename}.png")
            else:
                print("\n⚠️  PNG 导出方法不可用")
                print("可用的图形方法:")
                display_graph_methods(graph)

        elif format == "svg":
            if hasattr(graph, 'draw_mermaid_svg'):
                graph.draw_mermaid_svg(f"{filename}.svg")
                print(f"\n✅ 图已导出为 {filename}.svg")
            elif hasattr(graph, 'draw_svg'):
                graph.draw_svg(f"{filename}.svg")
                print(f"\n✅ 图已导出为 {filename}.svg")
            else:
                print("\n⚠️  SVG 导出方法不可用")
                display_graph_methods(graph)

    except ImportError as e:
        print(f"\n⚠️  需要额外库支持: {e}")
        print("安装方法: pip install grandalf graphviz")
        print("系统级 Graphviz: https://graphviz.org/download/")
    except Exception as e:
        print(f"\n❌ 导出失败: {e}")
        print("提示: 可以使用 Mermaid 格式在 Markdown 文档中显示")


def export_mermaid_to_file(app, filename="graph"):
    """将 Mermaid 代码导出到文件"""
    try:
        graph = app.get_graph()
        mermaid_code = graph.draw_mermaid()

        # 保存 Mermaid 代码到文件
        with open(f"{filename}.md", 'w', encoding='utf-8') as f:
            f.write("# LangGraph 流程图\n\n")
            f.write("```mermaid\n")
            f.write(mermaid_code)
            f.write("\n```\n\n")
            f.write("## 使用说明\n")
            f.write("可以通过以下方式查看此图：\n")
            f.write("1. 将此文件复制到支持 Mermaid 的编辑器（如 VS Code + Mermaid Preview）\n")
            f.write("2. 在线查看: https://mermaid.live/ (将 ```mermaid``` 中的代码粘贴)\n")
            f.write("3. 使用 GitHub、GitLab 等平台的 Markdown 渲染\n")

        print(f"\n✅ Mermaid 代码已导出到 {filename}.md")
        print("💡 提示: 可以在支持 Mermaid 的平台上查看流程图")
    except Exception as e:
        print(f"\n❌ Mermaid 导出失败: {e}")


def display_graph_methods(graph):
    """显示图对象可用的所有方法"""
    print("\n可用的图形方法:")
    print("-" * 40)
    draw_methods = []
    for attr in dir(graph):
        if not attr.startswith('_') and callable(getattr(graph, attr)):
            if any(keyword in attr.lower() for keyword in ['draw', 'print', 'get', 'to']):
                draw_methods.append(attr)

    for method in sorted(draw_methods):
        print(f"  - {method}()")

    if not draw_methods:
        print("  未找到相关方法")
        print("  常用方法: print_ascii(), draw_mermaid()")


def demonstrate_graph_execution():
    """演示图的执行过程"""
    print("\n" + "="*60)
    print("=== 执行流程演示 ===")
    print("="*60 + "\n")

    agent = create_sample_graph()

    # 初始化状态
    initial_state = {
        "messages": ["用户: 请帮我分析代码"],
        "user_id": "user_123",
        "context": {}
    }

    print("初始状态:")
    print(f"  用户ID: {initial_state['user_id']}")
    print(f"  消息: {initial_state['messages'][0]}")
    print(f"  上下文: {initial_state['context']}")

    print("\n执行流程:")
    # 执行图
    try:
        result = agent.invoke(initial_state)
        print("\n✅ 流程执行完成")
        print(f"最终状态中的上下文: {result.get('context', {})}")
    except Exception as e:
        print(f"❌ 执行失败: {e}")


if __name__ == "__main__":
    # 创建示例图
    agent = create_sample_graph()

    # 可视化流程结构
    visualize_graph(agent)

    # 演示执行过程
    demonstrate_graph_execution()

    # 尝试导出图形文件
    print("\n" + "="*60)
    print("=== 尝试导出图形文件 ===")
    print("="*60)

    # 显示可用的图形方法
    graph = agent.get_graph()
    display_graph_methods(graph)

    # 导出 Mermaid 文件
    export_mermaid_to_file(agent, "memory_agent_graph")

    print("\n" + "="*60)
    print("可视化功能说明:")
    print("="*60)
    print("1. ASCII格式 - 终端直接查看")
    print("2. 图结构信息 - 编程方式访问节点和边")
    print("3. Mermaid格式 - 可用于Markdown文档")
    print("4. Mermaid文件 - 已导出到 memory_agent_graph.md")
    print("\n💡 提示: 可以使用 memory_agent_graph.md 在支持 Mermaid 的平台查看流程图")
