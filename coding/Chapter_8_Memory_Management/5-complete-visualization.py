"""
完整的 LangGraph 图形可视化解决方案
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


def main():
    print("=== LangGraph 完整可视化解决方案 ===\n")

    agent = create_sample_graph()
    graph = agent.get_graph()

    # 1. ASCII 格式可视化
    print("1. ASCII 格式流程图:")
    print("-" * 40)
    graph.print_ascii()

    # 2. Mermaid 代码
    print("\n2. Mermaid 代码:")
    print("-" * 40)
    mermaid_code = graph.draw_mermaid()
    print(mermaid_code[:200] + "...")

    # 3. 保存 Mermaid 到文件
    print("\n3. 保存 Mermaid 代码到文件...")
    with open("langgraph_mermaid.md", 'w', encoding='utf-8') as f:
        f.write("# LangGraph 流程图\n\n")
        f.write("```mermaid\n")
        f.write(mermaid_code)
        f.write("\n```\n")
    print("✅ 已保存到 langgraph_mermaid.md")

    # 4. 导出 JSON 格式
    print("\n4. 导出 JSON 格式...")
    json_data = graph.to_json()
    with open("langgraph.json", 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print("✅ 已保存到 langgraph.json")

    # 5. 图结构信息
    print("\n5. 图结构信息:")
    print("-" * 40)
    nodes = list(graph.nodes)
    print(f"节点数: {len(nodes)}")
    print(f"节点: {nodes}")

    print("\n边连接关系:")
    for edge in list(graph.edges):
        if isinstance(edge, tuple) and len(edge) >= 2:
            print(f"  {edge[0]} → {edge[1]}")

    print("\n" + "="*60)
    print("可视化方案总结:")
    print("="*60)
    print("✅ ASCII 格式 - 终端直接查看（已显示）")
    print("✅ Mermaid 代码 - 保存到 langgraph_mermaid.md")
    print("✅ JSON 格式 - 保存到 langgraph.json")
    print("\n💡 使用建议:")
    print("1. 在 VS Code 中使用 Mermaid Preview 插件查看流程图")
    print("2. 将 Mermaid 代码复制到 https://mermaid.live/ 在线查看")
    print("3. 使用 JSON 格式进行程序化分析")
    print("4. ASCII 格式适合快速终端查看")


if __name__ == "__main__":
    main()
