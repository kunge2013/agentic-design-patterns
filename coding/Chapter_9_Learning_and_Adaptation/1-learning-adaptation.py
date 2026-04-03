"""
学习和适应模式示例代码
演示智能体如何通过反馈学习和自我改进
"""
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import random
import json
from datetime import datetime
from llm_config import create_llm
from langchain_core.messages import HumanMessage, SystemMessage


class FeedbackType(Enum):
    """反馈类型"""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class PerformanceMetric:
    """性能指标"""
    success_rate: float
    average_time: float
    resource_usage: float
    user_satisfaction: float

    def calculate_score(self) -> float:
        """计算综合得分"""
        weights = {'success': 0.4, 'time': 0.2, 'resource': 0.2, 'satisfaction': 0.2}
        return (
            self.success_rate * weights['success'] +
            (1.0 - self.average_time / 100.0) * weights['time'] +
            (1.0 - self.resource_usage / 100.0) * weights['resource'] +
            self.user_satisfaction * weights['satisfaction']
        )


class LearningAgent:
    """学习智能体 - 能够从反馈中学习"""

    def __init__(self, name: str, llm=None):
        self.name = name
        self.llm = llm or create_llm()
        self.strategy_params = {
            'temperature': 0.7,
            'top_p': 0.9,
            'max_tokens': 500
        }
        self.performance_history: List[PerformanceMetric] = []
        self.total_interactions = 0
        self.successful_interactions = 0

    def execute_task(self, task: str) -> str:
        """执行任务 - 使用LLM来完成任务"""
        print(f"  {self.name} 执行任务: {task}")

        try:
            # 使用LLM来完成任务
            system_prompt = """你是一个智能助手，擅长执行各种任务。
请简洁地回答用户的问题或完成用户的请求。如果任务完成，说明完成情况。
回答控制在100字以内。"""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=task)
            ]

            response = self.llm.invoke(messages)
            result = response.content.strip()

            print(f"  LLM响应: {result[:50]}...")

            # 基于LLM响应判断是否成功
            success_keywords = ['完成', '成功', '可以', '是的', '好的', '没问题']
            success = any(keyword in result for keyword in success_keywords)

            if success:
                self.successful_interactions += 1
            else:
                # 添加一些随机性让学习更有意义
                success = random.random() < 0.7
                if success:
                    self.successful_interactions += 1

            execution_time = random.uniform(10, 50)

            if success:
                return f"任务完成！{result[:100]} 耗时: {execution_time:.1f}秒"
            else:
                return f"任务处理中，结果: {result[:100]} 耗时: {execution_time:.1f}秒"

        except Exception as e:
            print(f"  LLM调用失败，使用模拟: {e}")
            # 如果LLM调用失败，回退到模拟
            success = random.random() < 0.8
            execution_time = random.uniform(10, 50)

            if success:
                self.successful_interactions += 1
                return f"任务完成！耗时: {execution_time:.1f}秒"
            else:
                return f"任务失败。耗时: {execution_time:.1f}秒"

    def receive_feedback(self, feedback: FeedbackType, rating: float = 0.0):
        """接收反馈并调整策略 - 使用LLM分析反馈"""
        print(f"  接收反馈: {feedback.value}, 评分: {rating}")

        self.total_interactions += 1

        # 根据反馈调整参数
        if feedback == FeedbackType.POSITIVE:
            # 成功时保持当前策略
            self.strategy_params['temperature'] = max(0.3, self.strategy_params['temperature'] * 0.95)
        elif feedback == FeedbackType.NEGATIVE:
            # 失败时增加探索
            self.strategy_params['temperature'] = min(1.0, self.strategy_params['temperature'] * 1.1)

    def evaluate_performance(self) -> PerformanceMetric:
        """评估当前性能"""
        if self.total_interactions == 0:
            return PerformanceMetric(0.0, 50.0, 50.0, 0.0)

        success_rate = self.successful_interactions / self.total_interactions
        avg_time = 30.0  # 简化计算
        resource_usage = 40.0
        user_satisfaction = success_rate * 0.8 + 0.2

        metric = PerformanceMetric(success_rate, avg_time, resource_usage, user_satisfaction)
        self.performance_history.append(metric)

        return metric


class AdaptiveLearningSystem:
    """自适应学习系统"""

    def __init__(self):
        self.agents: Dict[str, LearningAgent] = {}
        self.task_queue: List[str] = []
        self.feedback_log: List[Dict] = []

    def register_agent(self, agent: LearningAgent):
        """注册学习智能体"""
        self.agents[agent.name] = agent
        print(f"已注册智能体: {agent.name}")

    def add_task(self, task: str):
        """添加任务到队列"""
        self.task_queue.append(task)

    def process_tasks(self, iterations: int = 10):
        """处理任务并学习"""
        print(f"\n开始处理任务（{iterations}次迭代）:")
        print("=" * 60)

        for iteration in range(iterations):
            print(f"\n=== 迭代 {iteration + 1} ===")

            for agent_name, agent in self.agents.items():
                if self.task_queue:
                    task = self.task_queue.pop(0)

                    # 执行任务
                    result = agent.execute_task(task)

                    # 生成模拟反馈
                    if "完成" in result:
                        feedback = FeedbackType.POSITIVE
                        rating = random.uniform(0.7, 1.0)
                    else:
                        feedback = FeedbackType.NEGATIVE
                        rating = random.uniform(0.0, 0.4)

                    agent.receive_feedback(feedback, rating)

                    # 记录反馈
                    self.feedback_log.append({
                        'timestamp': datetime.now().isoformat(),
                        'agent': agent_name,
                        'task': task,
                        'feedback': feedback.value,
                        'rating': rating
                    })

    def report_performance(self):
        """报告系统性能"""
        print("\n" + "=" * 60)
        print("性能报告")
        print("=" * 60)

        for agent_name, agent in self.agents.items():
            metric = agent.evaluate_performance()
            score = metric.calculate_score()

            print(f"\n智能体: {agent_name}")
            print(f"  成功率: {metric.success_rate:.2%}")
            print(f"  综合得分: {score:.3f}")
            print(f"  当前温度参数: {agent.strategy_params['temperature']:.3f}")

            if score > 0.7:
                print(f"  状态: 优秀 ✓")
            elif score > 0.5:
                print(f"  状态: 良好 ~")
            else:
                print(f"  状态: 需改进 ✗")


def demonstrate_feedback_learning():
    """演示基于反馈的学习"""
    print("=== 基于反馈的学习演示 ===\n")

    system = AdaptiveLearningSystem()

    # 创建智能体
    agent1 = LearningAgent("智能体A")
    agent2 = LearningAgent("智能体B")

    system.register_agent(agent1)
    system.register_agent(agent2)

    # 添加任务
    tasks = [
        "代码审查",
        "文档生成",
        "测试用例编写",
        "性能优化",
        "错误修复"
    ]

    for task in tasks:
        system.add_task(task)

    # 处理任务
    system.process_tasks(iterations=5)

    # 报告性能
    system.report_performance()


class SelfImprovingAgent:
    """自我改进智能体 - 模拟 SICA 概念"""

    def __init__(self, initial_capabilities: Dict[str, float], llm=None):
        self.capabilities = initial_capabilities.copy()
        self.improvement_history: List[Dict] = []
        self.version = 1
        self.llm = llm or create_llm()

    def self_evaluate(self) -> Dict[str, float]:
        """自我评估当前能力 - 使用LLM进行评估"""
        print(f"  版本 {self.version} 自我评估...")

        try:
            # 使用LLM进行自我评估
            system_prompt = """你是一个AI智能体，需要评估自己的能力。
请对以下能力进行评估（0.0-1.0之间的分数）：
1. code_editing - 代码编辑能力
2. navigation - 导航能力
3. problem_solving - 问题解决能力
4. efficiency - 效率

请以JSON格式返回评估结果，例如：
{"code_editing": 0.8, "navigation": 0.7, "problem_solving":1.0, "efficiency": 0.6}"""

            current_state = f"当前版本: {self.version}\n当前能力: {self.capabilities}"
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=current_state)
            ]

            response = self.llm.invoke(messages)
            result_text = response.content.strip()

            print(f"  LLM评估结果: {result_text[:100]}...")

            # 尝试解析JSON，如果失败则使用随机值
            import json
            try:
                evaluation = json.loads(result_text)
                # 确保所有能力都在范围内
                for key in evaluation:
                    evaluation[key] = max(0.0, min(1.0, evaluation[key]))
                return evaluation
            except json.JSONDecodeError:
                print("  JSON解析失败，使用模拟评估")
                # 如果LLM调用失败，使用随机评估
                evaluation = {
                    'code_editing': random.uniform(0.5, 0.9),
                    'navigation': random.uniform(0.5, 0.9),
                    'problem_solving': random.uniform(0.5, 0.9),
                    'efficiency': random.uniform(0.5, 0.9)
                }

        except Exception as e:
            print(f"  LLM调用失败: {e}，使用模拟评估")
            evaluation = {
                'code_editing': random.uniform(0.5, 0.9),
                'navigation': random.uniform(0.5, 0.9),
                'problem_solving': random.uniform(0.5, 0.9),
                'efficiency': random.uniform(0.5, 0.9)
            }

        return evaluation

    def generate_improvement(self, evaluation: Dict[str, float]) -> Dict[str, str]:
        """生成改进方案 - 使用LLM生成改进建议"""
        print("  分析评估结果并生成改进方案...")

        improvements = {}

        try:
            # 使用LLM生成改进建议
            system_prompt = """你是一个AI智能体的自我改进系统。
根据能力评估结果，为得分低于0.7的能力提出改进建议。
请以JSON格式返回改进方案，例如：
{"code_editing": "加强代码编辑能力，学习更多编程技巧"}
只针对需要改进的能力返回建议。"""

            eval_text = f"能力评估结果：\n{json.dumps(evaluation, ensure_ascii=False, indent=2)}"
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=eval_text)
            ]

            response = self.llm.invoke(messages)
            result_text = response.content.strip()

            print(f"  LLM改进建议: {result_text[:100]}...")

            # 尝试解析JSON，如果失败则使用简单逻辑
            try:
                improvement_dict = json.loads(result_text)
                improvements.update(improvement_dict)
            except json.JSONDecodeError:
                print("  JSON解析失败，使用简单改进逻辑")
                for capability, score in evaluation.items():
                    if score < 0.7:
                        improvements[capability] = f"改进 {capability}（当前得分: {score:.2f}）"

        except Exception as e:
            print(f"  LLM调用失败: {e}，使用简单改进逻辑")
            for capability, score in evaluation.items():
                if score < 0.7:
                    improvements[capability] = f"改进 {capability}（当前得分: {score:.2f}）"

        return improvements

    def implement_improvement(self, improvements: Dict[str, str]):
        """实施改进"""
        if not improvements:
            print("  无需改进，当前表现良好")
            return

        print(f"  实施改进（共{len(improvements)}项）:")
        for capability, description in improvements.items():
            print(f"    - {description}")
            # 实际应用中，这里会真正改进能力
            self.capabilities[capability] = min(1.0, self.capabilities[capability] + random.uniform(0.1, 0.2))

        self.version += 1

        # 记录改进历史
        self.improvement_history.append({
            'version': self.version,
            'improvements': improvements,
            'timestamp': datetime.now().isoformat()
        })

    def improve(self, max_iterations: int = 5):
        """自我改进循环"""
        print(f"开始自我改进（最多 {max_iterations} 次迭代）:")
        print("=" * 60)

        for iteration in range(max_iterations):
            print(f"\n=== 改进迭代 {iteration + 1} ===")

            # 评估
            evaluation = self.self_evaluate()

            # 生成改进方案
            improvements = self.generate_improvement(evaluation)

            # 实施改进
            self.implement_improvement(improvements)

            # 检查是否达到目标
            avg_score = sum(evaluation.values()) / len(evaluation)
            if avg_score >= 0.85:
                print(f"\n✓ 达到目标性能（平均得分: {avg_score:.3f}）")
                break

    def get_capability_summary(self) -> str:
        """获取能力摘要"""
        avg_score = sum(self.capabilities.values()) / len(self.capabilities)

        summary = f"""
版本: {self.version}
平均能力得分: {avg_score:.3f}
详细能力:
"""
        for capability, score in self.capabilities.items():
            bar = "█" * int(score * 10)
            summary += f"  {capability}: {score:.3f} {bar}\n"

        return summary


def demonstrate_self_improvement():
    """演示自我改进"""
    print("\n=== 自我改进智能体演示 ===\n")

    # 初始化智能体
    initial_capabilities = {
        'code_editing': 0.6,
        'navigation': 0.5,
        'problem_solving': 0.6,
        'efficiency': 0.5
    }

    agent = SelfImprovingAgent(initial_capabilities)

    print("初始状态:")
    print(agent.get_capability_summary())

    # 执行自我改进
    agent.improve(max_iterations=10)

    print("\n" + "=" * 60)
    print("最终状态:")
    print(agent.get_capability_summary())


class EvolutionaryOptimizer:
    """进化优化器 - 模拟 AlphaEvolve/OpenEvolve 概念"""

    def __init__(self, initial_solution: str, fitness_function):
        self.population = [initial_solution]
        self.fitness_function = fitness_function
        self.generation = 0
        self.best_fitness = 0.0
        self.best_solution = initial_solution

    def mutate(self, solution: str) -> str:
        """变异操作"""
        # 简化示例：随机添加字符
        mutations = ["优化", "改进", "加速", "精简"]
        mutation = random.choice(mutations)
        return solution + " " + mutation

    def crossover(self, parent1: str, parent2: str) -> str:
        """交叉操作"""
        # 简化示例：合并两个解
        midpoint = len(parent1) // 2
        return parent1[:midpoint] + parent2[midpoint:]

    def select(self) -> str:
        """选择操作"""
        return random.choice(self.population)

    def evolve(self, max_generations: int = 10, population_size: int = 5):
        """进化循环"""
        print(f"开始进化优化（最多 {max_generations} 代）:")
        print("=" * 60)

        for generation in range(max_generations):
            self.generation = generation + 1
            print(f"\n=== 第 {generation + 1} 代 ===")

            new_population = []

            # 生成新个体
            while len(new_population) < population_size:
                parent = self.select()

                # 变异
                mutated = self.mutate(parent)
                fitness = self.fitness_function(mutated)

                print(f"  生成候选: {mutated[:50]}... | 适应度: {fitness:.3f}")

                new_population.append(mutated)

                # 更新最优解
                if fitness > self.best_fitness:
                    self.best_fitness = fitness
                    self.best_solution = mutated

            self.population = new_population

            print(f"  当前最优适应度: {self.best_fitness:.3f}")

            # 检查收敛
            if self.best_fitness >= 0.9:
                print(f"\n✓ 收敛到最优解（适应度: {self.best_fitness:.3f}）")
                break


def demonstrate_evolutionary_optimization():
    """演示进化优化"""
    print("\n=== 进化优化演示 ===\n")

    # 定义适应度函数
    def fitness_function(solution: str) -> float:
        # 简化适应度：基于解的长度和关键词
        keywords = ["优化", "改进", "加速", "精简"]
        score = 0.3  # 基础分
        score += len(solution) * 0.01  # 长度奖励
        score += sum(solution.count(keyword) * 0.15 for keyword in keywords)
        return min(1.0, score)

    initial_solution = "基础算法实现"
    print(f"初始解: {initial_solution}")
    print(f"初始适应度: {fitness_function(initial_solution):.3f}\n")

    optimizer = EvolutionaryOptimizer(initial_solution, fitness_function)
    optimizer.evolve(max_generations=8, population_size=4)

    print("\n" + "=" * 60)
    print("最终结果:")
    print(f"最优解: {optimizer.best_solution}")
    print(f"最优适应度: {optimizer.best_fitness:.3f}")


if __name__ == "__main__":
    try:
        demonstrate_feedback_learning()
        demonstrate_self_improvement()
        demonstrate_evolutionary_optimization()

        print("\n" + "=" * 60)
        print("学习和适应演示完成！")
        print("=" * 60)

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已正确设置 OPENAI_API_KEY 环境变量")
