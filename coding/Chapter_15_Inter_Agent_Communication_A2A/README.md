# Chapter 15: Inter-Agent Communication (A2A) (智能体间通信 A2A)

本章节展示智能体间通信（Agent-to-Agent，A2A）模式的代码示例。

## 目录结构

```
Chapter_15_Inter_Agent_Communication_A2A/
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

### 1. 基础Agent通信 (Basic Agent Communication)
- **文件**: `1-basic_agent_communication.py`
- **说明**: 演示两个Agent之间的基础消息传递

### 2. 消息协议设计 (Message Protocol Design)
- **文件**: `2-message_protocol.py`
- **说明**: 演示Agent间消息协议的设计和实现

### 3. Agent协调和协作 (Agent Coordination and Collaboration)
- **文件**: `3-agent_coordination.py`
- **说明**: 演示多个Agent的协调和工作分配

### 4. 分布式Agent系统 (Distributed Agent System)
- **文件**: `4-distributed_agents.py`
- **说明**: 演示跨进程/跨服务的Agent通信

## 实战项目

**项目名称**: 智能任务编排系统

**技术栈**:
- Flask (Web框架)
- LangChain (Agent框架)
- Flasgger (Swagger文档)

**功能特性**:
- 多Agent注册和发现
- Agent间消息路由
- 任务分发和协调
- Agent状态监控

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

### A2A通信模式 (Agent-to-Agent Communication Pattern)
- 定义Agent间的消息交换机制
- 支持同步和异步通信
- 实现Agent的协作和协调

### 消息协议 (Message Protocol)
- 标准化的消息格式
- 消息类型和语义定义
- 消息序列化和传输

### Agent发现和注册 (Agent Discovery and Registration)
- Agent注册中心
- 服务发现机制
- Agent能力描述

### 协作模式 (Collaboration Patterns)
- 主从模式（Master-Slave）
- 对等模式（Peer-to-Peer）
- 委员会模式（Committee）
- 管道模式（Pipeline）

## 参考资料

- 原始英文内容: `original/Chapter 15_ Inter-Agent Communication (A2A).md`
- 中文翻译内容: `chapters/Chapter 15_ 智能体间通信 (A2A).md`
- 摘要文档: `coding/Chapter_15_Inter_Agent_Communication_A2A_SUMMARY/`
