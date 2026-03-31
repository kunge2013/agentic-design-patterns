# 第7章 多智能体协作模式 - 代码实现

本目录包含多智能体协作模式的Python实现，基于LangChain框架。这些示例展示了如何构建多个协作的AI智能体来解决复杂问题。

## 文件说明

### 1_顺序交接模式.py
**功能**：演示多个智能体按顺序处理任务，每个智能体将输出传递给下一个智能体

**实现内容**：
- `SequentialAgent` 类：顺序智能体基类，定义了智能体的角色、目标和处理逻辑
- `sequential_handover_example()`：技术博客创建示例（研究员→分析师→作家）
- `sequential_data_pipeline_example()`：客户反馈分析流水线示例（提取→分类→优先级）

**应用场景**：
- 文档处理工作流（提取 → 分析 → 汇总）
- 数据流水线（收集 →. 清洗 → 转换）
- 代码生成（需求分析 → 设计 → 编码）

**运行方式**：
```bash
python 1_sequential_handover.py
```

### 2_并行处理模式.py
**功能**：演示多个智能体同时处理不同任务，然后汇总结果

**实现内容**：
- `ParallelAgent` 类：并行智能体基类，支持异步处理
- `ParallelProcessor` 类：并行处理器，管理多个智能体的并行执行和结果综合
- `parallel_research_analysis_example()`：多角度产品分析示例
- `parallel_data_gathering_example()`：企业信息收集示例
- `parallel_decision_making_example()`：项目方案评估示例

**应用场景**：
- 多源数据收集（多个API同时获取）
- 并行分析（从不同角度分析同一数据）
- 分布式决策（多个专家同时评估）

**运行方式**：
```bash
python 2_parallel_processing.py
```

### 3_层次结构模式.py
**功能**：演示管理者智能体将任务委托给专门的工作智能体，并综合其结果

**实现内容**：
- `WorkerAgent` 类：工作智能体，专门处理特定任务，具有专长领域
- `ManagerAgent` 类：管理者智能体，协调和委托任务给合适的工作智能体
- `HierarchicalTeam` 类：层次化团队，包含管理者和多个工作智能体
- `hierarchical_management_example()`：项目管理团队示例
- `multi_level_hierarchy_example()`：企业决策系统示例
- `specialization_team_example()`：医疗诊断团队示例

**应用场景**：
- 任务分解与分配（复杂任务拆解为子任务）
- 专家团队协作（管理者协调多个专家）
- 层级决策（上级协调下级执行）

**运行方式**：
```bash
python 3_hierarchical_structure.py
```

### 4_批评者审查者模式.py
**功能**：演示一个智能体生成内容，另一个智能体审查和评估，然后修订

**实现内容**：
- `CreatorAgent` 类：创建者智能体，生成初始内容
- `CriticAgent` 类：批评者智能体，审查和评估内容质量
- `RevisorAgent` 类：修订者智能体，根据审查意见修订内容
- `CriticReviewerWorkflow` 类：批评者-审查者工作流，实现迭代改进循环
- `code_review_example()`：代码审查示例
- `content`_safety_review_example()：内容安全审查示例
- `security_assessment_example()`：系统安全评估示例

**应用场景**：
- 代码审查（生成代码 → 质量检查 → 修正）
- 内容审核（生成内容 → 合规检查 → 修改）
- 安全审查（生成方案 → 安全评估 → 改进）

**运行方式**：
```bash
python 4_critic_reviewer.py
```

### 5_综合协作系统.py
**功能**：演示多种多智能体协作模式的组合使用，构建复杂的协作系统

**实现内容**：
- `BaseAgent` 类：基础智能体类，提供通用的处理能力
- `ResearchAssistant` 类：研究助手，负责信息收集和初步分析
- `AnalysisTeam` 类：分析团队，并行分析多个维度
- `DecisionCouncil` 类：决策委员会，通过辩论达成共识
- `QualityReviewer` 类：质量审查者，评估决策质量
- `ExecutionPlanner` 类：执行规划者，制定执行计划
- `IntelligentProblemSolvingSystem` 类：智能问题解决系统，综合所有模式
- 多个应用示例：企业战略决策、产品开发决策、技术转型决策

**应用场景**：
- 复杂问题解决系统（研究 + 分析 + 决策）
- 智能客服系统（理解 + 分发 + 解决 + 反馈）
- 企业知识管理系统（收集 + 组织 + 分享 + 应用）

**运行方式**：
```bash
python 5_comprehensive_system.py
```

### llm_config.py
**功能**：统一的LLM配置管理

**实现内容**：
- `LLMConfig` 类：封装LLM配置，支持多种API提供商
- `get_default_llm_config()`：从环境变量获取默认配置
- `create_llm()`：快捷创建LLM实例
- 支持OpenAI、Azure OpenAI以及国内模型服务商

**配置方式**：
```bash
export OPENAI_API_KEY='your-api-key'
export OPENAI_API_URL='https://your-api-endpoint'  # 可选
export OPENAI_MODEL='gpt-3.5-turbo'  # 可选
export OPENAI_TEMPERATURE='0.7'  # 可选
```

### requirements.txt
**功能**：项目依赖包列表依赖包**：
- langchain>=0.1.0
- langchain-openai>=0.0.20
- langchain-community>=0.0.10
- openai>=1.0.0
- python-dotenv>=1.0.0
- httpx>=0.25.0
- aiohttp>=3.9.0

**安装方式**：
```bash
pip install -r requirements.txt
```

## 核心概念

### 多智能体协作模式
多智能体协作模式通过将系统构建为由不同专门化智能体组成的协作集合来解决复杂问题。基于任务分解原则，将高级目标拆解为离散的子问题，然后将每个子问题分配给拥有最适合该任务的特定工具、数据访问或推理能力的智能体。

### 协作形式

1. **顺序交接**：一个智能体处理任务并将其输出传递给另一个智能体进行流水线中的下一步

2. **并行处理**：多个智能体同时处理问题的不同部分，然后它们的结果稍后被组合

3. **辩论与共识**：多个智能体协作，持有不同观点和信息来源的智能体通过讨论评估选项，最终达成共识

4. **层次结构**：管理者智能体根据工具访问或插件能力动态将任务委托给工作智能体，并并综合其结果

5. **专家团队**：在不同领域具有专业知识的智能体协作产生复杂输出

6. **批评者-审查者**：一个智能体生成初始输出，另一组智能体批判性地评估此输出是否符合政策、安全性、合规性等标准

## 使用示例

### 基本使用模式

所有示例都需要先配置API密钥：

```bash
export OPENAI_API_KEY='your-api-key'
```

然后运行任何示例文件：

```bash
python 1_sequential_handover.py
python 2_parallel_processing.py
python 3_hierarchical_structure.py
python 4_critic_reviewer.py
python 5_comprehensive_system.py
```

### 自定义配置

修改环境变量以使用不同的模型提供商：

```bash
# 使用OpenAI
export OPENAI_API_KEY='sk-...'
export OPENAI_MODEL='gpt-4'

# 使用其他兼容OpenAI API的服务
export OPENAI_API_KEY='your-key'
export OPENAI_API_URL='https://api.example.com/v1'
export OPENAI_MODEL='your-model'
```

## 技术特点

1. **模块化设计**：每个智能体都是独立的模块，可以单独测试和替换
2. **异步支持**：并行处理模式充分利用异步编程提高效率
3. **灵活配置**：统一的配置管理支持多种LLM提供商
4. **可扩展性**：易于添加新的智能体类型和协作模式
5. **实用导向**：所有示例都是可直接应用的场景

## 注意事项

1. **API密钥安全**：请勿将API密钥提交到版本控制系统
2. **成本控制**：多次迭代和多个智能体可能会增加API调用成本
3. **性能优化**：并行处理时注意并发数控制，避免API限流
4. **错误处理**：所有示例都包含基本的错误处理，实际使用时可能需要增强
5. **模型选择**：不同的协作模式可能适合不同的模型参数设置

## 扩展建议

1. **添加自定义工具**：在智能体中集成外部API和工具
2. **状态管理**：添加记忆和状态持久化功能
3. **监控和日志**：集成监控系统跟踪智能体执行状态
4. **测试覆盖**：添加单元测试和集成测试
5. **性能分析**：添加性能指标收集和分析

## 参考资料

- [LangChain文档](https://python.langchain.com/)
- [OpenAI API文档](https://platform.openai.com/docs)
- [多智能体协作模式 - 第7章](../../chapters/Chapter%207_%20Multi-Agent%20Collaboration.md)
