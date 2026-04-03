"""
智能客服学习助手 - 学习和适应模式实战项目
演示智能体如何通过用户反馈学习和自我改进
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
from llm_config import create_llm
from langchain_core.messages import HumanMessage, SystemMessage


@dataclass
class UserFeedback:
    """用户反馈数据"""
    user_id: str
    question: str
    response: str
    rating: int  # 1-5 星评分
    feedback_text: str
    timestamp: str


@dataclass
class QuestionPattern:
    """问题模式"""
    question_type: str
    common_keywords: List[str]
    success_count: int
    total_count: int

    @property
    def success_rate(self) -> float:
        if self.total_count == 0:
            return 0.0
        return self.success_count / self.total_count


class LearningCustomerService:
    """学习型客服系统"""

    def __init__(self):
        self.llm = create_llm()
        self.feedback_history: List[UserFeedback] = []
        self.question_patterns: Dict[str, QuestionPattern] = {}
        self.user_profiles: Dict[str, Dict] = {}
        self.knowledge_base: Dict[str, str] = {}
        self.strategy_params = {
            'temperature': 0.7,
            'response_length': 'medium',  # short, medium, long
            'use_empathy': True,
            'use_examples': True
        }
        self.version = 1
        self.improvement_log: List[Dict] = []

    def identify_question_type(self, question: str) -> str:
        """识别问题类型 - 使用LLM"""
        try:
            system_prompt = """你是一个问题分类专家。根据用户的问题，判断问题类型。

常见问题类型包括：
1. product - 产品相关问题
2. pricing - 价格和支付相关问题
3. technical - 技术支持问题
4. shipping - 配送和物流问题
5. refund - 退款和售后问题
6. other - 其他问题

请只返回问题类型（英文），例如：product、pricing等。"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=question)
            ]

            response = self.llm.invoke(messages)
            question_type = response.content.strip().lower()

            # 验证返回的类型是否有效
            valid_types = ['product', 'pricing', 'technical', 'shipping', 'refund', 'other']
            if question_type not in valid_types:
                question_type = 'other'

            return question_type

        except Exception as e:
            print(f"识别问题类型失败: {e}")
            return 'other'

    def generate_response(self, question: str, user_id: str = None) -> str:
        """生成回复 - 基于学习策略和用户偏好"""
        question_type = self.identify_question_type(question)

        # 获取用户偏好
        user_profile = self.user_profiles.get(user_id, {}) if user_id else {}

        # 根据策略调整生成参数
        temperature = self.strategy_params['temperature']
        response_length_pref = user_profile.get('preferred_length', self.strategy_params['response_length'])

        # 设置响应长度指导
        length_guidance = {
            'short': '请用简洁的语言回答，控制在50字以内。',
            'medium': '请用适中的语言回答，控制在100-200字之间。',
            'long': '请详细回答，提供尽可能多的信息。'
        }

        try:
            system_prompt = f"""你是一个专业的客服助手，负责回答用户问题。

当前策略参数：
- 使用共情：{self.strategy_params['use_empathy']}
- 使用示例：{self.strategy_params['use_examples']}
- 温度：{temperature}

{length_guidance[response_length_pref]}

回答要求：
1. 准确回答用户问题
2. 保持专业和友好的语气
3. 如果使用共情，请先理解用户的需求和情绪
4. 如果使用示例，请提供具体的例子帮助用户理解
5. 回答要有条理，使用项目符号"""

            # 添加知识库上下文
            kb_context = self._get_knowledge_base_context(question_type)

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=kb_context + "\n\n用户问题：" + question)
            ]

            response = self.llm.invoke(messages)
            return response.content.strip()

        except Exception as e:
            print(f"生成回复失败: {e}")
            return "抱歉，我现在无法处理您的问题，请稍后再试。"

    def _get_knowledge_base_context(self, question_type: str) -> str:
        """获取知识库上下文"""
        kb_entries = self.knowledge_base.get(question_type, "")
        if kb_entries:
            return f"相关知识库信息：\n{kb_entries}"
        return ""

    def record_feedback(self, user_id: str, question: str, response: str,
                     rating: int, feedback_text: str = ""):
        """记录用户反馈"""
        feedback = UserFeedback(
            user_id=user_id,
            question=question,
            response=response,
            rating=rating,
            feedback_text=feedback_text,
            timestamp=datetime.now().isoformat()
        )

        self.feedback_history.append(feedback)

        # 更新问题模式
        question_type = self.identify_question_type(question)
        if question_type not in self.question_patterns:
            self.question_patterns[question_type] = QuestionPattern(
                question_type=question_type,
                common_keywords=[],
                success_count=0,
                total_count=0
            )

        pattern = self.question_patterns[question_type]
        pattern.total_count += 1
        if rating >= 4:  # 4-5星算作成功
            pattern.success_count += 1

        # 更新用户档案
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'total_interactions': 0,
                'average_rating': 0.0,
                'preferred_length': 'medium',
                'feedback_count': 0
            }

        profile = self.user_profiles[user_id]
        profile['total_interactions'] += 1
        profile['feedback_count'] += 1

        # 更新平均评分
        old_avg = profile['average_rating']
        total = profile['feedback_count']
        new_avg = ((old_avg * (total - 1)) + rating) / total
        profile['average_rating'] = new_avg

    def learn_from_feedback(self) -> Dict[str, any]:
        """从反馈中学习并调整策略"""
        if not self.feedback_history:
            return {
                'learned': False,
                'message': '没有足够的反馈数据进行学习'
            }

        # 分析最近50条反馈
        recent_feedback = self.feedback_history[-50:]

        # 计算平均评分
        avg_rating = sum(f.rating for f in recent_feedback) / len(recent_feedback)

        learning_result = {
            'learned': True,
            'version': self.version + 1,
            'previous_avg_rating': avg_rating,
            'changes': []
        }

        # 调整策略参数
        if avg_rating < 3.0:
            # 评分较低，需要改进
            self.strategy_params['temperature'] = min(1.0, self.strategy_params['temperature'] * 1.1)
            self.strategy_params['use_empathy'] = True
            learning_result['changes'].append('增加温度参数，启用共情')
        elif avg_rating >= 4.0:
            # 评分较高，可以优化效率
            self.strategy_params['temperature'] = max(0.3, self.strategy_params['temperature'] * 0.95)
            learning_result['changes'].append('降低温度参数，保持当前策略')

        # 分析问题类型成功率
        for q_type, pattern in self.question_patterns.items():
            if pattern.total_count >= 5:  # 至少5次交互才分析
                if pattern.success_rate < 0.6:
                    # 该类型问题成功率低，需要添加到知识库
                    learning_result['changes'].append(
                        f'问题类型 "{q_type}" 成功率低 ({pattern.success_rate:.1%})，建议丰富知识库'
                    )

        self.version += 1

        # 记录改进日志
        self.improvement_log.append({
            'version': self.version,
            'timestamp': datetime.now().isoformat(),
            'avg_rating': avg_rating,
            'changes': learning_result['changes']
        })

        return learning_result

    def self_evaluate(self) -> Dict[str, any]:
        """自我评估当前表现 - 使用LLM"""
        if not self.feedback_history:
            return {
                'overall_score': 0.5,
                'areas_to_improve': [],
                'strengths': [],
                'message': '没有足够的数据进行评估'
            }

        # 计算基本指标
        total_feedback = len(self.feedback_history)
        avg_rating = sum(f.rating for f in self.feedback_history) / total_feedback
        recent_feedback = self.feedback_history[-20:]
        recent_avg = sum(f.rating for f in recent_feedback) / len(recent_feedback)

        # 分析问题类型表现
        type_performance = {}
        for q_type, pattern in self.question_patterns.items():
            if pattern.total_count >= 3:
                type_performance[q_type] = pattern.success_rate

        try:
            # 使用LLM进行深度评估
            system_prompt = """你是一个AI系统评估专家。请评估智能客服系统的表现。

请分析以下数据并返回JSON格式的评估结果：
{
    "overall_score": 0.0-1.0之间的综合评分,
    "areas_to_improve": ["需要改进的领域1", "需要改进的领域2"],
    "strengths": ["做得好的方面1", "做得好的方面2"],
    "recommendations": ["改进建议1", "改进建议2"]
}

评估标准：
- 整体评分基于平均评分（5分制转换为0.8）和趋势（最近表现改善加分）
- 识别评分低于3.5的问题类型作为改进领域
- 识别评分高于4.0的问题类型作为优势
- 提供具体的改进建议"""

            evaluation_data = f"""
当前版本：{self.version}
总反馈数：{total_feedback}
平均评分：{avg_rating:.2f}/5.0
最近20条反馈平均评分：{recent_avg:.2f}/5.0

问题类型表现：
{json.dumps(type_performance, ensure_ascii=False, indent=2)}

策略参数：
{json.dumps(self.strategy_params, ensure_ascii=False, indent=2)}
"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=evaluation_data)
            ]

            response = self.llm.invoke(messages)
            result_text = response.content.strip()

            # 尝试解析JSON
            try:
                evaluation = json.loads(result_text)
                evaluation['basic_metrics'] = {
                    'total_feedback': total_feedback,
                    'avg_rating': avg_rating,
                    'recent_avg': recent_avg
                }
                return evaluation
            except json.JSONDecodeError:
                print("JSON解析失败，使用简单评估")

        except Exception as e:
            print(f"自我评估失败: {e}")

        # 回退到简单评估
        overall_score = avg_rating / 5.0
        if recent_avg > avg_rating:
            overall_score += 0.1  # 趋势改善加分

        return {
            'overall_score': min(1.0, overall_score),
            'areas_to_improve': [q_type for q_type, rate in type_performance.items() if rate < 0.7],
            'strengths': [q_type for q_type, rate in type_performance.items() if rate >= 0.8],
            'basic_metrics': {
                'total_feedback': total_feedback,
                'avg_rating': avg_rating,
                'recent_avg': recent_avg
            },
            'recommendations': []
        }

    def auto_improve(self) -> Dict[str, any]:
        """自动改进 - 学习+评估+改进的完整流程"""
        print("开始自动改进流程...")

        # 1. 从反馈中学习
        learning_result = self.learn_from_feedback()

        # 2. 自我评估
        evaluation = self.self_evaluate()

        # 3. 生成改进方案
        improvements = self._generate_improvement_plan(evaluation)

        # 4. 实施改进
        improvement_result = self._implement_improvements(improvements)

        return {
            'learning': learning_result,
            'evaluation': evaluation,
            'improvements': improvements,
            'implementation': improvement_result
        }

    def _generate_improvement_plan(self, evaluation: Dict) -> List[str]:
        """生成改进方案 - 使用LLM"""
        try:
            system_prompt = """你是一个AI系统优化专家。根据评估结果生成改进方案。

请返回JSON格式：
{
    "improvements": ["改进方案1", "改进方案2"],
    "priority_adjustments": {"temperature": 0.7}
}

改进方案应该具体、可执行，针对评估中发现的不足。"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=json.dumps(evaluation, ensure_ascii=False, indent=2))
            ]

            response = self.llm.invoke(messages)
            result_text = response.content.strip()

            try:
                plan = json.loads(result_text)
                improvements = plan.get('improvements', [])

                # 应用优先级调整
                if 'priority_adjustments' in plan:
                    for param, value in plan['priority_adjustments'].items():
                        if param in self.strategy_params:
                            self.strategy_params[param] = value

                return improvements
            except json.JSONDecodeError:
                pass

        except Exception as e:
            print(f"生成改进方案失败: {e}")

        # 回退到简单方案
        return [
            "持续收集用户反馈以优化回答质量",
            "定期更新知识库内容",
            "分析高频问题类型并优化回复策略"
        ]

    def _implement_improvements(self, improvements: List[str]) -> Dict:
        """实施改进"""
        result = {
            'implemented': [],
            'skipped': []
        }

        for improvement in improvements:
            # 这里简化处理，实际应用中会实施具体的改进
            if isinstance(improvement, str) and len(improvement) > 10:
                result['implemented'].append(improvement)
            else:
                result['skipped'].append(improvement)

        return result

    def add_knowledge_base_entry(self, question_type: str, content: str):
        """添加知识库条目"""
        if question_type not in self.knowledge_base:
            self.knowledge_base[question_type] = ""

        self.knowledge_base[question_type] += f"\n{content}"

    def get_statistics(self) -> Dict:
        """获取系统统计信息"""
        return {
            'version': self.version,
            'total_feedback': len(self.feedback_history),
            'total_users': len(self.user_profiles),
            'question_types': len(self.question_patterns),
            'knowledge_base_entries': len(self.knowledge_base),
            'strategy_params': self.strategy_params,
            'question_patterns': {
                q_type: {
                    'success_rate': pattern.success_rate,
                    'total_count': pattern.total_count
                }
                for q_type, pattern in self.question_patterns.items()
            }
        }
