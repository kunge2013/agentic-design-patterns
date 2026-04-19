# Chapter 14: Knowledge Retrieval (RAG) (知识检索 RAG)

本章节展示知识检索（RAG）模式的代码示例。

## 目录结构

```
Chapter_14_Knowledge_Retrieval_RAG/
├── llm_config.py          # LLM配置文件
├── README.md              # 本文件
├── 1-xxx.py              # 代码示例1
├── 2-xxx.py              # 代码示例2
└── practical/            # 实战项目
    ├── llm_config.py     # LLM配置文件
    ├── README.md         # 项目说明文档
    └── docs/             # Swagger API
        └── api_xxx.yml
```

## 代码示例说明

本章节包含以下代码示例：

### 1. 基础RAG实现 (Basic RAG Implementation)
- **文件**: `1-basic_rag.py`
- **说明**: 演示最基础的RAG实现流程

### 2. 文档索引和检索 (Document Indexing and Retrieval)
- **文件**: `2-document_indexing.py`
- **说明**: 演示如何创建文档索引和执行检索

### 3. 向量数据库集成 (Vector Database Integration)
- **文件**: `3-vector_database.py`
- **说明**: 演示使用向量数据库存储和检索嵌入

### 4. 混合检索策略 (Hybrid Retrieval Strategy)
- **文件**: `4-hybrid_retrieval.py`
- **说明**: 演示结合关键词搜索和语义搜索的混合检索

### 5. RAG优化技术 (RAG Optimization Techniques)
- **文件**: `5-rag_optimization.py`
- **说明**: 演示RAG性能优化技术（重排序、压缩等）

## 实战项目

**项目名称**: 智能企业知识库

**技术栈**:
- Flask (Web框架)
- LangChain (Agent框架)
- LangChain Community (向量存储)
- Flasgger (Swagger文档)

**功能特性**:
- 文档上传和索引
- 智能知识问答
- 多种检索策略
- 知识来源追踪

**使用方法**:
1. 安装依赖: `pip install -r requirements.txt`
2. 配置环境变量:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   export OPENAI_API_URL='your-api-url'  # 可选
   ```
3. 启动服务:
   ```bash
   cd practical
   python app.py
   ```
4. 访问Swagger文档: `http://localhost:5000/api/docs`

## 核心概念

### RAG模式 (Retrieval-Augmented Generation Pattern)
- 从外部知识库检索相关信息
- 将检索结果作为上下文提供给LLM
- 生成基于知识的准确回答

### 文档索引 (Document Indexing)
- 文档分块和预处理
- 嵌入向量化
- 向量存储和索引

### 检索策略 (Retrieval Strategies)
- 语义检索（基于向量相似度）
- 关键词检索（BM25等）
- 混合检索（语义+关键词）
- 重排序（Reranking）

### 上下文优化 (Context Optimization)
- 检索结果压缩
- 相关性评分
- 上下文窗口管理

## 参考资料

- 原始英文内容: `original/Chapter 14_ Knowledge Retrieval (RAG).md`
- 中文翻译内容: `chapters/Chapter 14_ 知识检索 (RAG).md`
- 摘要文档: `coding/Chapter_14_Knowledge_Retrieval_RAG_SUMMARY/`
