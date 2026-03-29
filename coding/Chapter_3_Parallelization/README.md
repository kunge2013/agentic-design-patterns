# Chapter 3: Parallelization Code Examples

本目录包含第三章"并行化"的代码示例，展示了如何在AI Agent系统中实现并行处理模式。

## 文件说明

### 1-langchain-parallel-example.py
**用途：演示LangChain框架中的并行处理模式**

该文件展示了如何使用LangChain表达式语言（LCEL）实现并行执行：
- 定义了三个独立的处理链：摘要生成、问题生成、关键术语提取
- 使用`RunnableParallel`同时执行这三个独立的LLM调用
- 最后通过综合步骤将并行结果整合为统一输出

**关键技术点：**
- `RunnableParallel` - 并行运行多个可运行对象
- `RunnablePassthrough` - 传递原始输入到后续步骤
- 异步执行 (`ainvoke`) - 使用asyncio管理并发操作
- 链式组合 (`|`) - 构建完整的处理工作流

### 2-google-adk-parallel-example.py
**用途：演示Google ADK框架中的多智能体并行处理**

该文件展示了如何使用Google ADK构建并行多智能体系统：
- 定义了三个专门的研究员智能体，分别研究不同领域
- 使用`ParallelAgent`并发执行这些研究员智能体
- 通过`SequentialAgent`协调并行研究后的结果综合

**关键技术点：**
- `LlmAgent` - 基础LLM驱动的智能体
- `ParallelAgent` - 并行执行多个子智能体
- `SequentialAgent` - 顺序协调智能体执行流程
- 状态管理 - 通过`output_key`在智能体间传递结果

## 运行要求

### 环境依赖
- Python 3.7+
- OpenAI API密钥（用于LangChain示例）
- Google API密钥和搜索工具访问权限（用于Google ADK示例）

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行示例

**LangChain示例：**
```bash
python 1-langchain-parallel-example.py
```

**Google ADK示例：**
```bash
# 需要配置Google环境后运行
python 2-google-adk-parallel-example.py
```

## 学习目标

通过这些示例，您将学到：
1. 如何识别可并行执行的独立任务
2. 如何使用LangChain的`RunnableParallel`实现并行处理
3. 如何使用Google ADK的`ParallelAgent`构建多智能体并行系统
4. 如何在并行执行后综合多个任务的结果
5. 理解并行化模式在处理外部API调用时的性能优势

## 注意事项

1. **并发vs并行：** Python的asyncio提供的是并发性而非真正的并行性，通过事件循环在单线程上智能切换任务
2. **错误处理：** 并行任务中的错误需要妥善处理，避免影响整体工作流
3. **资源管理：** 大量并行请求可能触发API速率限制，需要适当的限流控制
4. **状态同步：** 确保并行任务完成后再进行综合步骤