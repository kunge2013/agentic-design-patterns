# 第8章 记忆管理

本章代码示例展示了智能体如何管理短期和长期记忆，实现连贯对话和持续学习。

## 目录

- [1-memory-management.py](1-memory-management.py) - 基础记忆管理示例
- [2-langgraph-memory-store.py](2-langgraph-memory-store.py) - LangGraph 记忆存储示例
- [llm_config.py](llm_config.py) - LLM 配置模块

## 文件说明

### 1-memory-management.py

演示了记忆管理的核心概念：

1. **短期记忆管理** - 使用 ConversationBufferMemory 维护对话上下文
2. **记忆总结** - 使用 ConversationSummaryMemory 处理长对话
3. **会话状态管理** - 跟踪会话级临时数据
4. **长期记忆管理** - 存储用户偏好和历史数据
5. **综合记忆管理** - 整合短期和长期记忆

运行方式：
```bash
python 1-memory-management.py
```

### 2-langgraph-memory-store.py

展示了 LangGraph 框架中的高级记忆功能：

1. **语义记忆存储** - 存储事实、概念和用户偏好
2. **情景记忆存储** - 存储经历、事件和交互历史
3. **程序记忆存储** - 存储智能体指令和规则
4. **记忆感知智能体** - 创建能够使用长期记忆的智能体
5. **跨会话记忆** - 在不同会话间共享记忆

运行方式：
```bash
python 2-langgraph-memory-store.py
```

### llm_config.py

LLM 配置模块，支持多种兼容 OpenAI API 的服务。该模块提供了：
- 灵活的 API 配置
- 预设配置选项
- 环境变量支持
- 快捷函数创建 LLM 实例

## 记忆类型

### 短期记忆
- 维护当前对话上下文
- 存储在 LLM 上下文窗口中
- 会话结束即丢失

### 长期记忆
- 持久存储用户数据和知识
- 支持跨会话访问
- 使用向量数据库或键值存储

### 记忆分类
- **语义记忆** - 事实和概念
- **情景记忆** - 经历和事件
- **程序记忆** - 规则和指令

## 依赖安装

```bash
pip install langchain langchain-openai langgraph httpx
```

## 环境变量设置

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_URL="your-api-url"  # 可选
```

## 核心概念

1. **会话管理** - 跟踪对话线程和状态
2. **状态更新** - 维护会话临时数据
3. **记忆检索**. - 从长期存储获取相关信息
4. **记忆更新** - 保存新信息到长期存储
5. **上下文整合** - 将记忆融入当前处理流程
