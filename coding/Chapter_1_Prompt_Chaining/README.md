# Chapter 1: Prompt Chaining 代码示例

本目录包含第1章"提示词链"的完整代码示例，基于LangChain框架实现。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

### 使用 OpenAI API

```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_MODEL="gpt-3.5-turbo"  # 可选，默认 gpt-3.5-turbo
```

### 使用兼容 OpenAI API 的其他服务

所有兼容 OpenAI API 规范的服务都可以使用：

#### 国内模型服务示例

**智谱AI (GLM-4)**
```bash
export OPENAI_API_KEY="your-zhipu-api-key"
export OPENAI_API_URL="https://open.bigmodel.cn/api/paas/v4/"
export OPENAI_MODEL="glm-4"
```

**阿里云通义千问**
```bash
export OPENAI_API_KEY="your-dashscope-api-key"
export OPENAI_API_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export OPENAI_MODEL="qwen-turbo"
```

**百度文心一言**
```bash
export OPENAI_API_KEY="your-ernie-api-key"
export OPENAI_API_URL="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
export OPENAI_MODEL="ERNIE-Bot-4"
```

**月之暗面 Kimi (Moonshot)**
```bash
export OPENAI_API_KEY="your-moonshot-api-key"
export OPENAI_API_URL="https://api.moonshot.cn/v1"
export OPENAI_MODEL="moonshot-v1-8k"
```

#### 其他兼容服务

**Groq**
```bash
export OPENAI_API_KEY="your-groq-api-key"
export OPENAI_API_URL="https://api.groq.com/openai/v1"
export OPENAI_MODEL="llama3-8b-8192"
```

**Together AI**
```bash
export OPENAI_API_KEY="your-together-api-key"
export OPENAI_API_URL="https://api.together.xyz/v1"
export OPENAI_MODEL="meta-llama/Llama-3-8b-chat-hf"
```

#### Azure OpenAI

```bash
export OPENAI_API_KEY="your-azure-api-key"
export OPENAI_API_URL="https://your-resource.openai.azure.com/openai/deployments/your-deployment"
export OPENAI_MODEL="gpt-35-turbo"
```

### 使用 .env 文件（推荐）

创建 `.env` 文件：
```bash
OPENAI_API_KEY=your-api-key
OPENAI_API_URL=https://your-api-endpoint  # 可选
OPENAI_MODEL=your-model-name  # 可选
OPENAI_TEMPERATURE=0.7  # 可选
```

然后在代码中添加：
```python
from dotenv import load_dotenv
load_dotenv()
```

## 代码示例说明

### 1. basic-prompt-chaining.py
**基础提示词链示例**
- 演示最简单的两步链：信息提取 → JSON转换
- 使用LangChain表达式语言（LCEL）
- 适合初学者理解提示词链的基本概念

运行：
```bash
python basic-prompt-chaining.py
```

### 2. information-processing-workflow.py
**信息处理工作流**
- 演示5步信息处理管道
- 文本提取 → 摘要 → 实体提取提取 → 知识库搜索 → 报告生成
- 展示如何构建复杂的多步骤工作流

运行：
```bash
python information-processing-workflow.py
```

### 3. complex-query-answering.py
**复杂查询回答**
- 演示多步推理能力
- 问题分解 → 信息检索 → 答案综合
- 适合需要深度分析的查询处理

运行：
```bash
python complex-query-answering.py
```

### 4. data-extraction-transformation.py
**数据提取和转换**
- 演示从非结构化文本到结构化数据的转换
- 包含数据验证和改进循环
- 模拟真实的数据处理场景（发票提取）

运行：
```bash
python data-extraction-transformation.py
```

### 5. content-generation-workflow.py
**内容生成工作流**
- 演示多步骤内容创作过程
- 主题生成 → 大纲创建 → 逐段起草 → 审查完善
- 适用于博客文章、技术文档等内容创作

运行：
```bash
python content-generation-workflow.py
```

### 6. conversational-agent-system.py
**具有状态的对话智能体系统**
- 演示如何维护对话状态和上下文
- 意图识别、实体提取、状态管理
- 实现多轮对话的连贯性

运行：
```bash
python conversational-agent-system.py
```

### 7. code-generation-refinement.py
**代码生成和完善**
- 演示多步骤代码开发流程
- 需求理解 → 代码生成 → 错误检查 → 代码完善 → 文档测试
- 展示提示词链在软件AI中的应用

运行：
```bash
python code-generation-refinement.py
```

## 核心概念

### 提示词链（Prompt Chaining）
将复杂任务分解为一系列较小的、聚焦的步骤，每个步骤的输出作为下一步的输入。

### LangChain表达式语言（LCEL）
使用 `|` 操作符优雅地链接组件：
```python
chain = prompt | llm | parser
result = chain.invoke({"input": value})
```

### 状态管理
在多步骤处理中维护和传递状态，确保上下文的连续性。

## 扩展建议

1. **添加更多验证步骤**：在每个输出步骤后添加验证逻辑
2. **集成外部工具**：在链中添加数据库查询、API调用等
3. **实现条件分支**：基于前一步的输出选择不同的处理路径
4. **添加错误处理**：增强代码的健壮性
5. **性能优化**：对独立步骤使用并行处理

## 注意事项

- **API兼容性**: 所有代码示例使用LangChain的`ChatOpenAI`类，兼容任何遵循OpenAI API规范的服务
- **必要配置**: 运行前必须设置 `OPENAI_API_KEY` 环境变量
- **API费用**: API调用会产生费用，请注意成本控制
- **模型选择**: 可以通过 `OPENAI_MODEL` 环境变量指定不同模型
- **自定义端点**: 通过 `OPENAI_API_URL` 或 `OPENAI_API_BASE` 设置自定义API端点

## 核心概念

### 提示词链（Prompt Chaining）
将复杂任务分解为一系列较小的、聚焦的步骤，每个步骤的输出作为下一步的输入。

### LangChain表达式语言（LCEL）
使用 `|` 操作符优雅地链接组件：
```python
chain = prompt | llm | parser
result = chain.invoke({"input": value})
```

### 状态管理
在多步骤处理中维护和传递状态，确保上下文的连续性。

## 扩展建议

1. **添加更多验证步骤**：在每个输出步骤后添加验证逻辑
2. **集成外部工具**：在链中添加数据库查询、API调用等
3. **实现条件分支**：基于前一步的输出选择不同的处理路径
4. **添加错误处理**：增强代码的健壮性
5. **性能优化**：对独立步骤使用并行处理
6. **使用不同的模型**：在不同步骤使用不同能力的模型（如创意生成用GPT-4，简单任务用GPT-3.5）

## 故障排除

### API连接失败
```bash
# 检查环境变量
echo $OPENAI_API_KEY
echo $OPENAI_API_URL

# 测试API连接
curl -X POST $OPENAI_API_URL/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"test","messages":[{"role":"user","content":"Hello"}]}'
```

### 模型名称错误
- 确保模型名称与所选服务匹配
- 不同服务的模型名称不同（如 `gpt-3.5-turbo` vs `glm-4`）

### 依赖问题
```bash
# 升级pip
python -m pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
pip install -r requirements.txt --force-reinstall
```

## 参考资源

- [LangChain文档](https://python.langchain.com/)
- [提示词工程指南](https://www.promptingguide.ai/)
- [本书第1章详细内容](../chapters/Chapter 1_ Prompt Chaining.md)
- [llm_config.py源码](llm_config.py) - 详细的配置管理实现
