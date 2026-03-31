"""
3_层次结构模式
演示管理者智能体将任务委托给专门的工作智能体，并综合其结果

应用场景：
- 任务分解与分配（复杂任务拆解为子任务）
- 专家团队协作（管理者协调多个专家）
- 层级决策（上级协调下级执行）
"""
from typing import Dict, Any, List
from langchain.schema import HumanMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import sys
import os

# 添加父目录到路径以导入配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from llm_config import create_llm


class WorkerAgent:
    """工作智能体 - 专门处理特定任务的智能体"""

    def __init__(self, name: str, specialty: str, description: str, llm: ChatOpenAI):
        self.name = name
        self.specialty = specialty  # 专长领域
        self.description = description
        self.llm = llm

        # 创建专用的处理链
        self.processing_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个{specialty}专家。\n{description}\n请用专业、准确的方式处理用户的请求。"),
                ("human", "{task}")
            ])
        )

    def can_handle(self, task: str) -> float:
        """评估该智能体能否处理此任务，返回一个置信度分数（0-1）"""
        # 简化版本：在实际应用中，可以使用分类器或语义匹配
        keywords = {
            "技术": ["开发", "代码", "架构", "技术", "编程", "算法", "系统"],
            "市场": ["营销", "推广", "客户", "市场", "品牌", "销售", "竞争"],
            "财务": ["预算", "成本", "财务", "资金", "投资", "收入", "支出"],
            "法律": ["合同", "法规", "法律", "合规", "条款", "义务"]
        }

        task_lower = task.lower()
        match_count = 0
        for keyword in keywords.get(self.specialty, []):
            if keyword in task_lower:
                match_count += 1

        # 返回置信度分数
        return min(match_count * 0.3, 1.0)  # 最大置信度为1.0

    def execute_task(self, task: str) -> Dict[str, Any]:
        """执行任务"""
        print(f"  [{self.name}] 正在处理任务...")
        try:
            result = self.processing_chain.run(task=task)
            print(f"  [{self.name}] 任务完成")
            return {
                "agent": self.name,
                "specialty": self.specialty,
                "success": True,
                "result": result
            }
        except Exception as e:
            print(f"  [{self.name}] 任务失败: {e}")
            return {
                "agent": self.name,
                "specialty": self.specialty,
                "success": False,
                "error": str(e)
            }


class ManagerAgent:
    """管理者智能体 - 协调和委托任务"""

    def __init__(self, name: str, coordination_style: str, llm: ChatOpenAI):
        self.name = name
        self.coordination_style = coordination_style
        self.llm = llm
        self.workers: List[WorkerAgent] = []

        # 协调链
        self.coordination_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个任务协调管理者。\n{coordination_style}\n你的职责是分析任务需求，分解任务，并整合下属智能体的结果。"),
                ("human", "{request}")
            ])
        )

        # 综合链
        self.synthesis_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", "你是一个结果综合专家。你的任务是将多个专家的结果整合成一个连贯、完整的答案。"),
                ("human", "{original_request}\n\n专家结果：\n{expert_results}\n\n请综合以上专家的结果，提供一个全面、准确的答案。")
            ])
        )

    def add_worker(self, worker: WorkerAgent):
        """添加工作智能体"""
        self.workers.append(worker)
        print(f"[{self.name}] 添加工作智能体: {worker.name} ({worker.specialty})")

    def delegate_task(self, task: str) -> Dict[str, Any]:
        """分析任务，找到最适合的工作智能体"""
        print(f"\n[{self.name}] 分析任务需求...")

        # 找到最适合的工作智能体
        best_worker = None
        best_confidence = 0.0

        for worker in self.workers:
            confidence = worker.can_handle(task)
            if confidence > best_confidence:
                best_confidence = confidence
                best_worker = worker

        if best_worker and best_confidence > 0.3:
            print(f"[{self.name}] 委派任务给 {best_worker.name} (置信度: {best_confidence:.2f})")
            return best_worker.execute_task(task)
        else:
            # 如果没有合适的工作智能体，管理者自己处理
            print(f"[{self.name}] 没有找到合适的工作智能体，由管理者处理")
            return self._handle_directly(task)

    def _handle_directly(self, task: str) -> Dict[str, Any]:
        """管理者直接处理任务"""
        try:
            result = self.coordination_chain.run(request=task)
            return {
                "agent": self.name,
                "specialty": "综合管理",
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "agent": self.name,
                "specialty": "综合管理",
                "success": False,
                "error": str(e)
            }

    def orchestrate_task(self, task: str, use_delegation: bool = True) -> str:
        """编排任务处理流程"""
        print(f"\n{'='*50}")
        print(f"[{self.name}] 开始任务编排")
        print(f"{'='*50}")

        if use_delegation and self.workers:
            result = self.delegate_task(task)
        else:
            result = self._handle_directly(task)

        return result["result"] if result["success"] else f"任务处理失败: {result.get('error', '未知错误')}"


class HierarchicalTeam:
    """层次化团队 - 包含管理者和多个工作智能体"""

    def __init__(self, name: str, llm: ChatOpenAI):
        self.name = name
        self.llm = llm
        self.managers: List[ManagerAgent] = []

    def add_manager(self, manager: ManagerAgent):
        """添加管理者"""
        self.managers.append(manager)

    def process_request(self, request: str, manager_index: int = 0) -> str:
        """处理请求，选择合适的管理者"""
        if manager_index < len(self.managers):
            return self.managers[manager_index].orchestrate_task(request)
        else:
            return "没有可用的管理者"


def hierarchical_management_example():
    """层次化管理示例：项目管理团队"""

    print("=== 层次结构模式示例：项目管理团队 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建团队
    project_team = HierarchicalTeam("项目管理团队", llm)

    # 创建项目经理
    project_manager = ManagerAgent(
        name="项目经理",
        coordination_style="你负责协调项目中的各种技术、市场和财务问题。根据任务类型，将其委托给合适的专家。",
        llm=llm
    )

    # 添加专门的工作智能体
    project_manager.add_worker(WorkerAgent(
        name="技术顾问",
        specialty="技术",
        description="擅长处理技术开发、架构设计、系统优化等技术相关问题",
        llm=llm
    ))

    project_manager.add_worker(WorkerAgent(
        name="市场分析师",
        specialty="市场",
        description="擅长处理市场分析、营销策略、客户需求等市场相关问题",
        llm=llm
    ))

    project_manager.add_worker(WorkerAgent(
        name="财务顾问",
        specialty="财务",
        description="擅长处理预算规划、成本控制、财务分析等财务相关问题",
        llm=llm
    ))

    project_manager.add_worker(WorkerAgent(
        name="法律顾问",
        specialty="法律",
        description="擅长处理合同审查、合规检查、法律风险评估等法律相关问题",
        llm=llm
    ))

    project_team.add_manager(project_manager)

    # 测试不同类型的任务
    tasks = [
        "我们需要设计一个高可用的电商系统架构，请给出技术方案建议",
        "如何制定新产品的市场推广策略？",
        "项目预算应该如何分配和控制？",
        "在开展国际合作项目时，需要注意哪些法律合规问题？"
    ]

    for i, task in enumerate(tasks, 1):
        print(f"\n{'#'*60}")
        print(f"任务 {i}: {task}")
        print(f"{'#'*60}")

        result = project_team.process_request(task)
        print(f"\n处理结果:\n{result}\n")


def multi_level_hierarchy_example():
    """多层次层次结构示例：组织架构"""

    print("\n\n=== 多层次层次结构示例：企业决策系统 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建团队
    corporate_team = HierarchicalTeam("企业决策团队", llm)

    # 创建CEO（顶级管理者）
    ceo = ManagerAgent(
        name="CEO",
        coordination_style="你是公司CEO，负责制定公司战略和重大决策。根据问题类型，将其委托给合适的副总裁。",
        llm=llm
    )

    # 添加副总裁级的管理者（在简化版本中，我们创建工作智能体模拟VP）
    ceo.add_worker(WorkerAgent(
        name="技术副总裁",
        specialty="技术",
        description="负责公司技术战略、研发方向和技术架构决策",
        llm=llm
    ))

    ceo.add_worker(WorkerAgent(
        name="市场副总裁",
        specialty="市场",
        description="负责公司市场战略、产品定位和市场拓展决策",
        llmm=llm
    ))

    ceo.add_worker(WorkerAgent(
        name="财务副总裁",
        specialty="财务",
        description="负责公司财务战略、投资决策和资本管理",
        llm=llm
    ))

    corporate_team.add_manager(ceo)

    # 测试企业级决策任务
    corporate_tasks = [
        "公司应该如何规划下一年的技术发展方向？",
        "针对新兴市场，我们制定什么产品策略？",
        "公司应该如何进行下一轮的融资和资本配置？"
    ]

    for i, task in enumerate(corporate_tasks, 1):
        print(f"\n{'#'*60}")
        print(f"企业决策 {i}: {task}")
        print(f"{'#'*60}")

        result = corporate_team.process_request(task)
        print(f"\n决策建议:\n{result}\n")


def specialization_team_example():
    """专家团队示例：医疗诊断团队"""

    print("\n\n=== 专家团队示例：医疗诊断团队 ===")

    # 创建LLM
    llm = create_llm(temperature=0.6)

    # 创建诊断团队
    diagnostic_team = HierarchicalTeam("医疗诊断团队", llm)

    # 创建主治医师
    chief_physician = ManagerAgent(
        name="主治医师",
        coordination_style="你是主治医师，负责患者整体诊断和治疗方案的制定。根据症状类型，请相应的专科医生会诊。",
        llm=llm
    )

    # 添加专科医生
    chief_physician.add_worker(WorkerAgent(
        name="心血管科专家",
        specialty="心血管",
        description="专门诊断心血管疾病，包括心脏病、高血压、心律失常等",
        llm=llm
    ))

    chief_physician.add_worker(WorkerAgent(
        name="神经内科专家",
        specialty="神经内科",
        description="专门诊断神经系统疾病，包括头痛、癫痫、中风等",
        llm=llm
    ))

    chief_physician.add_worker(WorkerAgent(
        name="呼吸内科专家",
        specialty="呼吸内科",
        description="专门诊断呼吸系统疾病，包括哮喘、肺炎、肺结核等",
        llm=llm
    ))

    chief_physician.add_worker(WorkerAgent(
        name="消化内科专家",
        specialty="消化内科",
        description="专门诊断消化系统疾病，包括胃炎、溃疡、肝病等",
        llm=llm
    ))

    diagnostic_team.add_manager(chief_physician)

    # 测试诊断案例
    patient_cases = [
        "患者主诉胸痛、呼吸困难，特别是运动后加重，伴有心悸",
        "患者出现剧烈头痛、恶心、呕吐，左侧肢体无力",
        "患者咳嗽、咳痰、发热，呼吸困难，活动后气促",
        "患者腹痛、腹胀、恶心、食欲不振，伴有消化不良"
    ]

    for i, case in enumerate(patient_cases, 1):
        print(f"\n{'#'*60}")
        print(f"病例 {i}: {case}")
        print(f"{'#'*60}")

        diagnosis = diagnostic_team.process_request(case)
        print(f"\n诊断结果:\n{diagnosis}\n")


if __name__ == "__main__":
    try:
        # 示例1：项目管理团队
        hierarchical_management_example()

        # 示例2：企业决策系统
        multi_level_hierarchy_example()

        # 示例3：医疗诊断团队
        specialization_team_example()

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已设置正确的 OPENAI_API_KEY 环境变量")
