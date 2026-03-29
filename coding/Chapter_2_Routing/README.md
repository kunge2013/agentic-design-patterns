# Chapter 2: Routing - 代码示例

本目录包含了第2章"路由"模式的所有代码示例，演示了不同类型的路由实现方法。

## 文件说明

### 1. 01-langchain-routing-example.py
**基于LLM的路由示例**

演示如何使用LangChain和RunnableBranch实现基于语言模型的智能路由。系统会分析用户请求的意图，然后将请求路由到相应的处理程序。

**特点：**
- 使用ChatOpenAI进行意图分类
- 使用RunnableBranch实现动态路由
- 包含模拟的子智能体处理程序

**运行方式：**
```bash
cd Chapter_2_Routing
python 01-langchain-routing-example.py
```

### 2. 02-rule-based-routing.py
**基于规则的路由示例**

演示如何使用正则表达式规则引擎实现快速、确定性的路由。

**特点：**
- 使用正则表达式匹配请求模式
- 按顺序检查规则，第一个匹配的规则生效
- 包含预设的默认处理程序
- 快速且无需外部API调用

**运行方式：**
```bash
python 02-rule-based-routing.py
```

### 3. 03-embedding-based-routing.py
**基于嵌入的路由示例**

演示如何使用向量嵌入和语义相似性进行路由。使用向量相似度来匹配请求与路由目标。

**特点：**
- 使用模拟的文本嵌入生成（实际应用中应使用真实嵌入模型）
- 计算余弦相似度进行匹配
- 支持语义路由，而不仅是关键词匹配
- 可设置相似度阈值

**运行方式：**
```bash
python 03-embedding-based-routing.py
```

### 4. 04-multi-level-routing.py
**多层级路由示例**

演示如何构建多层级路由系统，实现复杂的分类和分发逻辑。

**特点：**
- 两级路由：第一级识别意图，第二级识别具体动作
- 层次化的路由映射表
- 支持fallback机制处理未知请求
- 灵活的路由结构易于扩展

**运行方式：**
```bash
python 04-multi-level-routing.py
```

### 5. 05-hybrid-routing-system.py
**综合路由系统示例**

演示如何将不同的路由策略结合起来，构建一个完整的智能路由系统。

**特点：**
- 结合快速规则路由和LLM语义路由
- 包含路由统计和性能监控
- 支持A/B测试
- 生产级路由架构

**运行方式：**
```bash
python 05-hybrid-routing-system.py
```

## 环境配置

### 1. 安装依赖

```bash
cd coding
pip install -r requirements.txt
```

### 2. 配置API密钥

复制环境变量示例文件：
```bash
cd Chapter_2_Routing
cp .env.example .env
```

编辑`.env`文件，填入你的OpenAI API密钥：
```env
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_API_URL=
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7
```

## 路由模式比较

| 路线类型 | 优点 | 缺点 | 适用场景 |
|---------|------|------|---------|
| **基于LLM** | 理解语义，处理复杂意图 | 速度慢，需要API调用，成本高 | 复杂的意图识别，需要理解语义 |
| **基于规则** | 快速，确定性，无成本 | 不够灵活，难以处理新颖输入 | 简单明确的意图，性能要求高 |
| **基于嵌入** | 语义匹配，比LLM快 | 需要维护示例查询，需要嵌入模型 | 语义相似性路由，中等复杂度 |
| **多层级** | 结构清晰，易于扩展 | 配置复杂，需要精心设计 | 复杂系统，需要细粒度控制 |

## 代码结构

```
Chapter_2_Routing/
├── 01-langchain-routing-example.py  # 基于LLM的路由
├── 02-rule-based-routing.py        # 基于规则的路由
├── 03-embedding-based-routing.py    # 基于嵌入的路由
├── 04-multi-level-routing.py        # 多层级路由
├── 05-hybrid-routing-system.py      # 综合路由系统
├── llm_config.py                # LLM配置模块
├── .env.example                 # 环境变量示例
└── README.md                    # 本文件
```

## 扩展建议

1. **添加新的路由目标：**
   - 在相应的示例文件中添加新的处理函数
   - 更新路由规则或映射表

2. **集成真实嵌入模型：**
   - 使用OpenAI、HuggingFace或Cohere的嵌入API
   - 替换`mock_embedding`函数

3. **构建生产级路由器：**
   - 结合多种路由策略
   - 添加缓存和性能监控
   - 实现A/B测试

## 注意事项

1. **API密钥安全：**
   - 不要将`.env`文件提交到版本控制
   - 使用环境变量管理敏感信息

2. **性能考虑：**
   - 基于规则的路由最快
   - 基于LLM的路由最慢但最灵活
   - 考虑添加缓存机制

3. **错误处理：**
   - 所有示例都包含基本的错误处理
   - 生产环境需要更完善的异常处理

## 相关章节

- **第1章：Prompt Chaining** - 基础的序列处理
- **第14章：RAG** - 嵌入和向量检索
