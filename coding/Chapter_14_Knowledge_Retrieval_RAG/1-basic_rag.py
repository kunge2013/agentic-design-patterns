"""
Chapter 14 - 代码示例 1：基础RAG实现 (Basic RAG Implementation)

此示例演示最基础的RAG实现流程。
"""
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加父目录到路径以导入llm_config
sys.path.append(str(Path(__file__).parent))
from llm_config import get_default_llm_config

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter


class SimpleRAGSystem:
    """简化的RAG系统（无向量数据库，用于演示）"""

    def __init__(self, llm_config):
        """
        初始化RAG系统

        Args:
            llm_config: LLM配置
        """
        self.llm = llm_config.create_llm()
        self.documents: List[Document] = []
        self.chunk_size = 200
        self.chunk_overlap = 50

        print("✅ RAG系统初始化完成")
        print(f"   分块大小: {self.chunk_size}")
        print(f"   分块重叠: {self.chunk_overlap}")

    def add_document(self, text: str, metadata: Optional[Dict] = None):
        """
        添加文档到知识库

        Args:
            text: 文档文本
            metadata: 文档元数据
        """
        metadata = metadata or {}
        doc = Document(page_content=text, metadata=metadata)
        self.documents.append(doc)
        print(f"📄 添加文档: {metadata.get('title', '无标题')}")

    def chunk_documents(self) -> List[Document]:
        """
        将文档分割成块

        Returns:
            分块后的文档列表
        """
        if not self.documents:
            print("⚠️  没有文档可分块")
            return []

        print(f"\n🔧 分割 {len(self.documents)} 个文档...")

        # 创建分块器
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )

        # 分割所有文档
        all_chunks = []
        for i, doc in enumerate(self.documents, 1):
            chunks = text_splitter.split_documents([doc])
            print(f"   文档 #{i}: {len(chunks)} 个分块")
            all_chunks.extend(chunks)

        print(f"✅ 总共生成 {len(all_chunks)} 个分块")
        return all_chunks

    def simple_retrieve(self, query: str, chunks: List[Document], top_k: int = 3) -> List[Document]:
        """
        简单检索（基于关键词匹配，用于演示）

        Args:
            query: 查询文本
            chunks: 文档分块
            top_k: 返回前K个结果

        Returns:
            相关文档块
        """
        print(f"\n🔍 检索: '{query}'")

        # 提取查询关键词（简单分词）
        query_keywords = set(query.lower().split())

        # 计算每个分块的相关性分数
        scored_chunks = []
        for chunk in chunks:
            content = chunk.page_content.lower()
            chunk_keywords = set(content.split())

            # 计算关键词重叠
            overlap = len(query_keywords & chunk_keywords)
            score = overlap / len(query_keywords) if query_keywords else 0

            if score > 0:
                scored_chunks.append((chunk, score))

        # 按分数排序并返回top_k
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        top_chunks = [chunk for chunk, score in scored_chunks[:top_k]]

        print(f"✅ 检索到 {len(top_chunks)} 个相关分块")
        for i, (chunk, score) in enumerate(scored_chunks[:top_k], 1):
            print(f"   {i}. 相关性: {score:.2f}")

        return top_chunks

    def generate_response(self, query: str, retrieved_docs: List[Document]) -> str:
        """
        基于检索的文档生成回答

        Args:
            query: 用户查询
            retrieved_docs: 检索到的文档

        Returns:
            生成的回答
        """
        if not retrieved_docs:
            print("⚠️  没有检索到相关文档，使用一般知识回答")
            context = "未找到相关文档。"
        else:
            # 构建上下文
            context_parts = []
            for i, doc in enumerate(retrieved_docs, 1):
                context_parts.append(f"[文档片段 {i}]")
                context_parts.append(doc.page_content)
            context = "\n".join(context_parts)

        print(f"\n🤖 生成回答...")

        # 创建提示模板
        template = """
你是一个专业的问答助手。请根据以下检索到的文档内容回答用户的问题。

检索到的文档：
{context}

用户问题：{question}

请基于文档内容回答问题。如果文档中没有相关信息，请明确说明。
回答要简洁、准确。

回答：
        """.strip()

        prompt_template = ChatPromptTemplate.from_template(template)

        # 构建提示
        prompt = prompt_template.format(context=context, question=query)

        # 生成回答
        response = self.llm.invoke(prompt)
        answer = response.content

        print(f"✅ 回答生成完成")
        return answer

    def query(self, question: str, top_k: int = 3) -> str:
        """
        执行完整的RAG查询

        Args:
            question: 用户问题
            top_k: 检索的文档数量

        Returns:
            生成的回答
        """
        print("\n" + "=" * 80)
        print(f"📝 RAG查询: {question}")
        print("=" * 80)

        # 1. 分块文档
        chunks = self.chunk_documents()

        if not chunks:
            return "没有可用文档。"

        # 2. 检索相关文档
        retrieved_docs = self.simple_retrieve(question, chunks, top_k)

        # 3. 生成回答
        answer = self.generate_response(question, retrieved_docs)

        return answer


def main():
    """主函数"""
    print("=" * 80)
    print("Chapter 14 - 示例 1：基础RAG实现 (Basic RAG Implementation)")
    print("=" * 80)
    print()
    print("📚 此示例演示基础的RAG（检索增强生成）流程")
    print("   注意：此示例使用简单的关键词匹配代替向量搜索")
    print()

    try:
        # 初始化LLM配置
        llm_config = get_default_llm_config()

        # 创建RAG系统
        rag_system = SimpleRAGSystem(llm_config)

        # 添加示例文档
        print("\n📥 添加知识库文档...")
        print("-" * 80)

        rag_system.add_document(
            text="""
产品功能概述

我们的产品是一个智能项目管理平台，具有以下核心功能：

1. 任务管理：用户可以创建、分配和跟踪任务。支持设置优先级、截止日期和依赖关系。
2. 团队协作：提供实时聊天、文件共享和评论功能，促进团队成员之间的沟通。
3. 时间跟踪：内置时间跟踪器，允许员工记录工作时间并生成详细报告。
4. 集成API：提供RESTful API，支持与第三方工具集成。
5. 数据分析：提供项目进度、团队效率和资源利用率的可视化分析。

产品目标是为中小型企业提供高效、易用的项目管理解决方案。
            """.strip(),
            metadata={"title": "产品功能文档", "category": "产品"}
        )

        rag_system.add_document(
            text="""
API使用指南

平台提供RESTful API，开发者可以通过API访问所有功能。

认证：
- 使用API密钥进行认证
- 将API密钥放在HTTP头的Authorization字段中

基础URL：https://api.example.com/v1

常用端点：

1. 获取项目列表
   GET /projects
   返回用户有权访问的所有项目

2. 创建任务
   POST /tasks
   请求体包含任务详情

3. 更新任务状态
   PUT /tasks/{id}/status
   更新指定任务的状态

4. 获取时间记录
   GET /time-entries
   返回指定时间范围的时间记录

API响应格式为JSON，包含data字段和可选的error字段。
            """.strip(),
            metadata={"title": "API文档", "category": "技术"}
        )

        rag_system.add_document(
            text="""
定价策略

我们提供灵活的定价方案，满足不同规模企业的需求：

1. 免费版
   - 最多5个项目
   - 最多10个用户
   - 基础功能
   - 无技术支持

2. 专业版（$29/用户/月）
   - 无限项目
   - 无限用户
   - 全部功能
   - 邮件支持
   - 50GB存储

3. 企业版（$49/用户/月）
   - 包含专业版所有功能
   - 专属支持经理
   - 24/7技术支持
   - 无限存储
   - 自定义集成

年度订阅可享受20%折扣。
所有计划都包含30天免费试用。
            """.strip(),
            metadata={"title": "定价文档", "category": "商业"}
        )

        # 执行示例查询
        queries = [
            "这个产品有哪些主要功能？",
            "如何使用API创建任务？",
            "有什么定价方案？",
            "免费版包含什么功能？",
            "如何获得技术支持？"
        ]

        print("\n" + "=" * 80)
        print("🔍 执行查询")
        print("=" * 80)

        for i, query in enumerate(queries, 1):
            print(f"\n{'=' * 80}")
            print(f"查询 #{i}: {query}")
            print(f"{'=' * 80}")

            try:
                answer = rag_system.query(query, top_k=3)
                print(f"\n💬 回答:")
                print(f"{answer}\n")
            except Exception as e:
                print(f"❌ 查询失败: {str(e)}")

        print("\n" + "=" * 80)
        print("✨ 基础RAG实现示例完成")
        print("=" * 80)

    except ValueError as e:
        print(f"\n❌ 配置错误: {str(e)}")
        print("请设置OPENAI_API_KEY环境变量")
    except Exception as e:
        print(f"\n❌ 运行错误: {str(e)}")


if __name__ == "__main__":
    main()
