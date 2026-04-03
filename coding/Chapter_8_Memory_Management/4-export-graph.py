"""
导出 LangGraph 图形为 PNG 格式
"""
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated, Sequence
import operator
import json


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
        print("节点: retrieve_memory")
        return state

    def process_with_context_node(state):
        print("节点: process_with_context")
        return state

    def update_memory_node(state):
        print("节点: update_memory")
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


if __name__ == "__main__":
    print("=== 导出 LangGraph 图形 ===\n")

    agent = create_sample_graph()
    graph = agent.get_graph()

    # 1. 尝试导出 Mermaid PNG
    print("1. 尝试导出 Mermaid PNG...")
    try:
        graph.draw_mermaid_png()  # 不带参数，方法会处理文件输出
        print("✅ Mermaid PNG 导出成功")
    except Exception as e:
        print(f"❌ Mermaid PNG 导出失败: {e}")
        try:
            # 尝试另一种方式
            result = graph.draw_mermaid_png()
            if result:
                print("✅ Mermaid PNG 生成成功（返回结果）")
        except Exception as e2:
            print(f"❌ 备用方法也失败: {e2}")

    # 2. 尝试导出标准 PNG
    print("\n2. 尝试导出标准 PNG...")
    try:
        graph.draw_png("langgraph.png")
        print("✅ 标准 PNG 导出成功: langgraph.png")
    except Exception as e:
        print(f"❌ 标准 PNG 导出失败: {e}")
        print("💡 提示: 需要安装 pygraphviz: pip install pygraphviz")

    # 3. 导出 JSON 格式
    print("\n3. 导出 JSON 格式...")
    try:
        json_data = graph.to_json()
        with open("langgraph.json", 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        print("✅ JSON 导出成功: langgraph.json")
    except Exception as e:
        print(f"❌ JSON 导出失败: {e}")

    print("\n=== 导出完成 ===")
    print("生成的文件:")
    print("- langgraph_mermaid.png (Mermaid 格式)")
    print("- langgraph.png (标准格式)")
    print("- langgraph.json (JSON 格式)")
