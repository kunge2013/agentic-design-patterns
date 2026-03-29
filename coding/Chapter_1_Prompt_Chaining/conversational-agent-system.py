"""
具有状态的对话智能体系统示例
演示如何维护对话状态和上下文
"""
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
import json
from llm_config import create_llm

# 初始化语言模型（支持自定义API配置）
try:
    llm = create_llm(temperature=0.7)
    print("✓ LLM初始化成功")
except Exception as e:
    print(f"✗ LLM初始化失败: {e}")
    exit(1)

# --- 步骤 1：意图识别和实体提取 ---
prompt_intent_extraction = ChatPromptTemplate.from_template(
    "你是一个对话智能体。分析用户的输入：\n\n{user_input}\n\n"
    "识别：\n"
    "- 意图（intent）：用户的目的是什么？\n"
    "- 实体（entities）：提取的关键信息（日期、地点、人名、数量等）\n"
    "- 情绪（sentiment）：正面、负面或中性\n\n"
    "以JSON格式返回：{{'intent': '...', 'entities': {{...}}, 'sentiment': '...'}}"
)

# --- 步骤 2：状态更新和响应生成 ---
prompt_generate_response = ChatPromptTemplate.from_template(
    "你是一个友好的对话智能体。\n\n"
    "当前对话状态：\n{conversation_state}\n\n"
    "当前用户输入分析：\n{current_analysis}\n\n"
    "生成合适的回复，考虑：\n"
    "- 对话历史和上下文\n"
    "- 用户的意图和情绪\n"
    "- 提取的实体\n"
    "- 保持对话的连贯性和个性化\n\n"
    "同时更新对话状态，记录重要信息。"
)

class ConversationalAgent:
    """具有状态的对话智能体"""

    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.conversation_state = {
            "user_profile": {},
            "context": {},
            "last_intent": None,
            "topic_stack": []
        }
        self.turn_count = 0

    def process_user_input(self, user_input: str) -> str:
        """处理用户输入并生成响应"""

        self.turn_count += 1
        print(f"\n--- 对话轮次 {self.turn_count} ---")
        print(f"用户输入：{user_input}")

        # 步骤 1：提取意图和实体
        intent_chain = prompt_intent_extraction | llm | StrOutputParser()
        analysis_text = intent_chain.invoke({"user_input": user_input})

        try:
            current_analysis = json.loads(analysis_text)
        except json.JSONDecodeError:
            # 如果JSON解析失败，创建基本结构
            current_analysis = {
                "intent": "general_conversation",
                "entities": {},
                "sentiment": "neutral",
                "raw_analysis": analysis_text
            }

        print(f"意图分析：{current_analysis.get('intent', 'unknown')}")
        print(f"提取实体：{current_analysis.get('entities', {})}")

        # 步骤 2：更新对话状态
        self._update_state(current_analysis)

        # 步骤 3：生成响应
        response_chain = prompt_generate_response | llm | StrOutputParser()
        response = response_chain.invoke({
            "conversation_state": json.dumps(self.conversation_state, indent=2, ensure_ascii=False),
            "current_analysis": json.dumps(current_analysis, indent=2, ensure_ascii=False)
        })

        # 步骤 4：更新对话历史
        self.conversation_history.append({
            "turn": self.turn_count,
            "user_input": user_input,
            "analysis": current_analysis,
            "response": response
        })

        print(f"智能体响应：{response[:100]}...")
        return response

    def _update_state(self, analysis: Dict):
        """更新对话状态"""

        # 更新最后意图
        self.conversation_state["last_intent"] = analysis.get("intent")

        # 更新用户档案
        entities = analysis.get("entities", {})
        for key, value in entities.items():
            if value and key not in self.conversation_state["user_profile"]:
                self.conversation_state["user_profile"][key] = value

        # 维护话题栈
        intent = analysis.get("intent", "")
        if intent and intent != self.conversation_state.get("last_intent"):
            if len(self.conversation_state["topic_stack"]) > 5:
                self.conversation_state["topic"].pop(0)
            self.conversation_state["topic_stack"].append(intent)

    def get_conversation_summary(self) -> str:
        """获取对话摘要"""
        return f"""
对话摘要：
- 总轮次：{self.turn_count}
- 最后意图：{self.conversation_state.get('last_intent', 'None')}
- 用户档案信息：{self.conversation_state['user_profile']}
- 讨论过的主题：{self.conversation_state['topic_stack']}
"""

# --- 运行示例 ---
def run_conversation_demo():
    """运行对话演示"""
    agent = ConversationalAgent()

    # 模拟对话
    conversation_inputs = [
        "你好，我叫张三，最近在学习机器学习",
        "我想了解一下Python的基本语法",
        "我对数据分析很感兴趣，特别是Pandas",
        "能给我推荐一些学习资源吗？",
        "谢谢你的帮助！"
    ]

    print("="*80)
    print("对话智能体演示")
    print("="*80)

    for user_input in conversation_inputs:
        response = agent.process_user_input(user_input)
        print(f"\n{response}\n")
        print("-" * 80)

    print(agent.get_conversation_summary())

if __name__ == "__main__":
    run_conversation_demo()
