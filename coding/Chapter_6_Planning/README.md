# Chapter 6: Planning - 代码示例

本目录包含第 6 章"规划模式"的代码实现，演示智能体如何将复杂任务分解为可管理的步骤并执行。

## 文件说明

### 1-crewai-planning.py
**功能：** 基于 CrewAI 框架的规划模式实现

**主要功能：**
- 演示如何使用 CrewAI 创建规划智能体
- 智能体首先为任务创建计划，然后执行计划
- 展示"规划-执行"两阶段工作流

**关键组件：**
- `planner_writer_agent`: 规划和写作智能体
- `planning_task`: 需要规划的任务
- `crew`: 智能体团队，使用顺序处理

**使用场景：**
- 需要先规划后执行的内容创作任务
- 文章写作、报告生成等需要结构化的工作

### 2-simple-planning-agent.py
**功能：** 简单的规划智能体实现

**主要功能：**
- 将复杂目标分解为清晰的执行步骤
- 分析任务的复杂度和依赖关系
- 模拟计划的执行过程

**关键组件：**
- `PlanningAgent`: 规划智能体核心类
- `create_plan()`: 创建执行计划
- `execute_plan()`: 执行计划
- `PlanningStep`: 单个规划步骤数据模型
- `ExecutionPlan`: 完整执行计划数据模型

**使用场景：**
- 需要任务分解的复杂目标
- 项目规划、研究计划、开发流程

### 3-research-planning-agent.py
**功能：** 研究型规划智能体（模拟 Deep Research 模式）

**主要功能：**
- 创建多步研究计划
- 动态生成搜索查询
- 执行搜索并综合研究结果
- 生成带引用的研究报告

**关键组件：**
- `DeepResearchAgent`: Deep Research 智能体
- `create_research_plan()`: 创建研究计划
- `execute_research_plan()`: 执行研究
- `ResearchPlan`: 研究计划数据模型
- `ResearchQuery`: 研究查询数据模型
- `mock_search()`: 模拟搜索工具

**使用场景：**
- 复杂主题的深入研究
- 竞争分析、市场研究
- 文献综述、技术调研

## 运行环境

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件（如果还没有）：

```bash
OPENAI_API_KEY=your-api-key
OPENAI_API_BASE=your-api-base-url  # 可选
```

### 运行示例

```bash
# 激活虚拟环境
source ~/.bashrc & conda activate agentic-design-patterns

# 运行 CrewAI 规划示例
python 1-crewai-planning.py.py

# 运行简单规划智能体
python 2-simple-planning-agent.py

# 运行研究规划智能体
python 3-research-planning-agent.py
```

## 技术要点

### 规划模式核心概念

1. **目标分解**: 将复杂目标分解为可管理的小步骤
2. **依赖分析**: 识别步骤之间的依赖关系
3. **工具识别**: 确定每个步骤需要的工具
4. **动态调整**: 根据执行结果调整计划

### 数据模型设计

- 使用 `dataclass` 定义清晰的数据结构
- 状态管理（pending, completed, failed）
- 结果追踪和引用管理

### 执行流程

1. 分析目标和上下文
2. 生成执行计划
3. 按顺序或并行执行步骤
4. 综合结果并生成报告

## 扩展建议

1. **集成真实搜索**: 替换 `mock_search` 为真实的搜索 API
2. **并行执行**: 支持独立步骤的并行执行
3. **计划优化**: 添加计划优化和重新规划能力
4. **持久化**: 保存和加载计划状态
5. **可视化**: 生成计划执行的可视化图表

## 注意事项

- 所有示例使用模拟搜索，实际应用需要集成真实工具
- CrewAI 示例需要正确的 API 配置
- 执行时间取决于网络和模型响应速度
- 复杂计划可能需要大量 token，注意成本控制
