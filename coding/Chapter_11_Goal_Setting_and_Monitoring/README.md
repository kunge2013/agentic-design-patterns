# Chapter 11: Goal Setting and Monitoring (目标设置与监控)

本章节展示目标设置与监控模式的代码示例。

## 目录结构

```
Chapter_11_Goal_Setting_and_Monitoring/
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

### 1. 目标设置 (Goal Setting)
- **文件**: `1-goal_setting.py`
- **说明**: 演示如何为Agent设置明确、可量化的目标

### 2. 目标监控 (Goal Monitoring)
- **文件**: `2-goal_monitoring.py`
- **说明**: 演示如何实时监控Agent目标的执行进度

### 3. 目标调整 (Goal Adjustment)
- **文件**: `3-goal_adjustment.py`
- **说明**: 演示如何在执行过程中动态调整目标

### 4. 多目标管理 (Multi-Goal Management)
- **文件**: `4-multi_goal_management.py`
- **说明**: 演示如何管理多个并行的目标

## 实战项目

**项目名称**: 智能项目管理系统

**技术栈**:
- Flask (Web框架)
- LangChain (Agent框架)
- Flasgger (Swagger文档)

**功能特性**:
- 创建和设置项目目标
- 实时监控目标执行进度
- 动态调整项目目标
- 多项目协同管理

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

### 目标设置模式 (Goal Setting Pattern)
- 为Agent设置清晰、可度量的目标
- 使用SMART原则（具体、可衡量、可实现、相关、有时限）
- 将复杂目标分解为子目标

### 目标监控模式 (Goal Monitoring Pattern)
- 实时追踪目标执行状态
- 提供进度反馈和可视化
- 识别偏差和异常情况

### 目标调整模式 (Goal Adjustment Pattern)
- 基于执行反馈动态调整目标
- 处理环境变化和意外情况
- 保持目标的相关性和可实现性

## 参考资料

- 原始英文内容: `original/Chapter 11_ Goal Setting and Monitoring.md`
- 中文翻译内容: `chapters/Chapter 11_ 目标设置与监控.md`
- 摘要文档: `coding/Chapter_11_Goal_Setting_and_Monitoring_SUMMARY/`
