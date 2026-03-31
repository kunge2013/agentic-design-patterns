"""
4_批评者审查者模式
演示一个智能体生成内容，另一个智能体审查和评估，然后修订

应用场景：
- 代码审查（生成代码 -> 质量检查 -> 修正）
- 内容审核（生成内容 -> 合规检查 -> 修改）
- 安全审查（生成方案 -> 安全评估 -> 改进）
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


class CreatorAgent:
    """创建者智能体 - 生成初始内容"""

    def __init__(self, name: str, role: str, llm: ChatOpenAI):
        self.name = name
        self.role = role
        self.llm = llm

        self.creation_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个{role}。你的目标是根据用户需求生成高质量的初始内容。"),
                ("human", "{request}")
            ])
        )

    def create(self, request: str) -> Dict[str, Any]:
        """创建内容"""
        print(f"[{self.name}] 正在生成内容...")
        try:
            content = self.creation_chain.run(request=request)
            print(f"[{self.name}] 内容生成完成")
            return {
                "success": True,
                "content": content,
                "version": 1
            }
        except Exception as e:
            print(f"[{self.name}] 内容生成失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": None
            }


class CriticAgent:
    """批评者智能体 - 审查和评估内容"""

    def __init__(self, name: str, role: str, review_criteria: str, llm: ChatOpenAI):
        self.name = name
        self.role = role
        self.review_criteria = review_criteria
        self.llm = llm

        self.review_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个{role}。\n\n你的审查标准是：{review_criteria}\n\n请按照以下格式提供审查意见：\n1. 整体评估（通过/不通过）\n2. 发现的问题列表\n3. 具体的改进建议\n4. 是否需要重新生成"),
                ("human", "原始请求：{request}\n\n待审查内容：\n{content}")
            ])
        )

    def review(self, request: str, content: str) -> Dict[str, Any]:
        """审查内容"""
        print(f"[{self.name}] 正在审查内容...")
        try:
            review_result = self.review_chain.run(request=request, content=content)
            print(f"[{self.name}] 审查完成")

            # 分析审查结果
            needs_revision = "需要重新生成" in review_result or "不通过" in review_result

            return {
                "success": True,
                "review": review_result,
                "needs_revision": needs_revision
            }
        except Exception as e:
            print(f"[{self.name}] 审查失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "review": None,
                "needs_revision": False
            }


class RevisorAgent:
    """修订者智能体 - 根据审查意见修订内容"""

    def __init__(self, name: str, role: str, llm: ChatOpenAI):
        self.name = name
        self.role = role
        self.llm = llm

        self.revision_chain = LLMChain(
            llm=llm,
            prompt=ChatPromptTemplate.from_messages([
                ("system", f"你是一个{role}。你的目标是根据审查意见修订内容，解决所有发现的问题，同时保持原有的优点。"),
                ("human", "原始请求：{request}\n\n当前内容：\n{current_content}\n\n审查意见：\n{review}\n\n请提供修订后的完整内容。")
            ])
        )

    def revise(self, request: str, current_content: str, review: str) -> Dict[str, Any]:
        """修订内容"""
        print(f"[{self.name}] 正在修订内容...")
        try:
            revised_content = self.revision_chain.run(
                request=request,
                current_content=current_content,
                review=review
            )
            print(f"[{self.name}] 内容修订完成")
            return {
                "success": True,
                "content": revised_content
            }
        except Exception as e:
            print(f"[{self.name}] 内容修订失败: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": current_content  # 返回原内容
            }


class CriticReviewerWorkflow:
    """批评者-审查者工作流"""

    def __init__(self, creator: CreatorAgent, critic: CriticAgent, revisor: RevisorAgent, max_iterations: int = 3):
        self.creator = creator
        self.critic = critic
        self.revisor = revisor
        self.max_iterations = max_iterations

    def execute(self, request: str, verbose: bool = True) -> Dict[str, Any]:
        """执行批评者-审查者循环"""

        if verbose:
            print(f"\n{'='*60}")
            print("批评者-审查者工作流启动")
            print(f"{'='*60}\n")

        # 第一步：创建初始内容
        creation_result = self.creator.create(request)
        if not creation_result["success"]:
            return {
                "success": False,
                "error": f"创建内容失败: {creation_result['error']}",
                "final_content": None,
                "iterations": 0
            }

        current_content = creation_result["content"]
        iteration = 0
        reviews = []

        # 循环：审查 -> 修订
        while iteration < self.max_iterations:
            iteration += 1

            if verbose:
                print(f"\n{'#'*60}")
                print(f"迭代 {iteration}/{self.max_iterations}")
                print(f"{'#'*60}\n")

            # 审审查内容
            review_result = self.critic.review(request, current_content)
            reviews.append(review_result)

            if not review_result["success"]:
                if verbose:
                    print("审查失败，停止迭代")
                break

            if verbose:
                print(f"\n审查结果:\n{review_result['review']}\n")

            # 检查是否需要修订
            if not review_result["needs_revision"]:
                if verbose:
                    print("✓ 内容通过审查，无需进一步修订")
                break

            # 修订内容
            if iteration >= self.max_iterations:
                if verbose:
                    print(f"已达到最大迭代次数 ({self.max_iterations})，停止修订")
                break

            revision_result = self.revisor.revise(request, current_content, review_result["review"])

            if revision_result["success"]:
                current_content = revision_result["content"]
            else:
                if verbose:
                    print(f"修订失败: {revision_result['error']}")
                break

        return {
            "success": True,
            "final_content": current_content,
            "iterations": iteration,
            "reviews": reviews
        }


def code_review_example():
    """代码审查示例：生成并审查Python代码"""

    print("=== 批评者-审查者模式示例：代码审查 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建智能体
    code_creator = CreatorAgent(
        name="代码生成器",
        role="Python编程专家，擅长编写高质量的Python代码",
        llm=llm
    )

    code_critic = CriticAgent(
        name="代码审查员",
        role="资深的代码审查专家",
        review_criteria="""
        代码质量标准：
        1. 代码风格：遵循PEP 8规范
        2. 错误处理：包含适当的异常处理
        3. 文档：有清晰的注释和文档字符串
        4. 安全性：没有明显的安全漏洞
        5. 性能：没有明显的性能问题
        6. 可测试性：代码易于测试
        """,
        llm=llm
    )

    code_revisor = RevisorAgent(
        name="代码修订者",
        role="经验丰富的代码维护专家，能够根据审查意见改进代码",
        llm=llm
    )

    # 创建工作流
    code_workflow = CriticReviewerWorkflow(
        creator=code_creator,
        critic=code_critic,
        revisor=code_revisor,
        max_iterations=3
    )

    # 执行工作流
    request = "编写一个Python函数，用于安全的API请求处理，包括重试逻辑、超时设置和错误处理。"

    result = code_workflow.execute(request, verbose=True)

    print(f"\n{'='*60}")
    print(f"最终结果（经过 {result['iterations']} 次迭代）")
    print(f"{'='*60}\n")
    print(result["final_content"])


def content_safety_review_example():
    """内容安全审查示例：生成并审查营销文案"""

    print("\n\n=== 批评者-审查者模式示例：内容安全审查 ===")

    # 创建LLM
    llm = create_llm(temperature=0.7)

    # 创建智能体
    content_creator = CreatorAgent(
        name="文案生成器",
        role="专业的营销文案撰写专家，擅长撰写吸引人的产品文案",
        llm=llm
    )

    safety_critic = CriticAgent(
        name="安全审查员",
        role="内容安全和合规审查专家",
        review_criteria="""
        内容安全标准：
        1. 法律合规：不违反广告法和相关法律法规
        2. 事实准确性：不做虚假或误导性宣传
        3. 社会责任：避免负面社会影响
               4. 品牌形象：符合品牌价值观和形象
        5. 目标受众：适合目标受众群体
        6. 语言规范：用词得体，避免争议性表达
        """,
        llm=llm
    )

    content_revisor = RevisorAgent(
        name="文案修订者",
        role="内容优化专家，能够根据安全审查意见调整文案内容",
        llm=llm
    )

    # 创建工作流
    content_workflow = CriticReviewerWorkflow(
        creator=content_creator,
        critic=safety_critic,
        revisor=content_revisor,
        max_iterations=2
    )

    # 执行工作流
    request = "为一款智能手机产品撰写营销文案，强调产品的创新性和优势。"

    result = content_workflow.execute(request, verbose=True)

    print(f"\n{'='*60}")
    print(f"最终营销文案（经过 {result['iterations']} 次迭代）")
    print(f"{'='*60}\n")
    print(result["final_content"])


def security_assessment_example():
    """安全评估示例：设计并评估系统架构"""

    print("\n\n=== 批评者-审查者模式示例：系统安全评估 ===")

    # 创建LLM
    llm = create_llm(temperature=0.6)

    # 创建智能体
    architect_creator = CreatorAgent(
        name="架构设计师",
        role="系统架构设计专家，擅长设计安全可靠的系统架构",
        llm=llm
    )

    security_critic = CriticAgent(
        name="安全评估员",
        role="系统安全评估专家",
        review_criteria="""
        安全评估标准：
        1. 认证与授权：是否有完善的身份认证和访问控制
        2. 数据保护：是否实现了数据加密和安全存储
        3. 网络安全：是否有适当的网络安全防护措施
        4. 审计日志：是否有完善的审计和监控机制
        5. 漏洞防护：是否考虑了常见的安全漏洞
        6. 灾难恢复：是否有备份和恢复机制
        7. 合规性：是否符合相关的安全标准和法规
        """,
        llm=llm
    )

    security_revisor = RevisorAgent(
        name="架构优化师",
        role="安全架构优化专家，能够根据安全评估建议改进架构设计",
        llm=llm
    )

    # 创建工作流
    security_workflow = CriticReviewerWorkflow(
        creator=architect_creator,
        critic=security_critic,
        revisor=security_revisor,
        max_iterations=2
    )

    # 执行工作流
    request = "设计一个安全的在线支付系统架构，支持多种支付方式和高并发访问。"

    result = security_workflow.execute(request, verbose=True)

    print(f"\n{'='*60}")
    print(f"最终架构方案（经过 {result['iterations']} 次迭代）")
    print(f"{'='*60}\n")
    print(result["final_content"])


if __name__ == "__main__":
    try:
        # 示例1：代码审查
        code_review_example()

        # 示例2：内容安全审查
        content_safety_review_example()

        # 示例3：系统安全评估
        security_assessment_example()

    except Exception as e:
        print(f"错误: {e}")
        print("请确保已设置正确的 OPENAI_API_KEY 环境变量")
