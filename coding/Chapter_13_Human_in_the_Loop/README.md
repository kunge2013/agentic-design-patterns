# Chapter 13: Human-in-the-Loop (人在回路)

本章节展示人在回路模式的代码示例。

## 目录结构

```
Chapter_13_Human_in_the_Loop/
├── llm_config.py          # LLM配置文件
├── README.md              # 本文件
├── 1-xxx.py              # 代码示例1
├── 2-xxx.py              # 代码示例2
└── practical/            # 实战项目
    ├── llm_config.py     # LLM配置文件
    ├── README.md         # 项目说明文档
    └── docs/             # Swagger API文档
        └── api_xxx.yml
```

## 代码示例说明

本章节包含以下代码示例：

### 1. 基本人工确认 (Basic Human Confirmation)
- **文件**: `1-basic_human_confirmation.py`
- **说明**: 演示Agent在关键决策点请求人工确认

### 2. 人工输入收集 (Human Input Collection)
- **文件**: `2-human_input_collection.py`
- **说明**: 演示Agent从人类用户收集所需信息

### 3. 人工反馈集成 (Human Feedback Integration)
- **文件**: `3-human_feedback_integration.py`
- **说明**: 演示如何将人工反馈集成到Agent的学习过程中

### 4. 异步人工审核 (Asynchronous Human Review)
- **文件**: `4-asynchronous_human_review.py`
- **说明**: 演示异步人工审核工作流

## 实战项目

**项目名称**: 智能内容审核系统

**技术栈**:
- Flask (Web框架)
- LangChain (Agent框架)
- Flasgger (Swagger文档)

**功能特性**:
- 自动AI内容审核
- 可疑内容人工复核
- 审核决策记录和追踪
- 审核质量反馈和学习

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

### 人在回路模式 (Human-in-the-Loop Pattern)
- 在关键决策点引入人工干预
- 平衡自动化和人工监督
- 确保高风险决策的人类可控性

### 人工确认模式 (Human Confirmation Pattern)
- 在执行关键操作前请求确认
- 提供充分的上下文信息
- 记录人工决策的理由

### 人工反馈模式 (Human Feedback Pattern)
- 收集人类对AI决策的反馈
- 使用反馈优化Agent行为
- 持续学习和改进

### 异步审核模式 (Asynchronous Review Pattern)
- AI处理异步人工审核任务
- 支持审核队列和优先级
- 审核结果回调和通知

## 参考资料

- 原始英文内容: `original/Chapter 13_ Human-in-the-Loop.md`
- 中文翻译内容: `chapters/Chapter 13_ 人在回路.md`
- 摘要文档: `coding/Chapter_13_Human_in_the_Loop_SUMMARY/`
