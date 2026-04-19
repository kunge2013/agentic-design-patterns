# 第10章 模型上下文协议 (MCP)

本章代码示例展示了如何实现和使用模型上下文协议（MCP）来标准化 LLM 与外部系统的交互。

## 目录

- [1-mcp-implementation.py](1-mcp-implementation.py) - MCP 实现示例
- [llm_config.py](llm_config.py) - LLM 配置模块

## 文件说明

### 1-mcp-implementation.py

演示了 MCP 的核心组件：

1. **MCP 服务器** - 实现文件系统和数据库服务器
2. **MCP 客户端** - 连接和调用 MCP 服务器
3. **MCP 资源** - 静态数据（如文档、配置）
4. **MCP 工具** - 可执行函数（如文件操作、数据库查询）
5. **MCP 提示** - 交互模板
6. **MCP 智能体** - 使用 MCP 处理请求的智能体

运行方式：
```bash
python 1-mcp-implementation.py
```

### llm_config.py

LLM 配置模块，支持多种兼容 OpenAI API 的服务。

## MCP 架构

### 客户端-服务器模型
- **MCP 服务器** - 向客户端公开工具、资源和提示
- **MCP 客户端** - 代表 LLM 连接和使用 MCP 服务器
- **LLM** - 核心智能，决定何时使用 MCP

### MCP 组件

#### 工具（Tools）
可执行函数，用于执行操作：
- 文件系统操作（读取、写入、列出文件）
- 数据库查询
- API 调用
- IoT 设备控制

#### 资源（Resources）
静态数据，提供数据访问：
- 文档（PDF、Markdown）
- 配置文件
- 数据库记录

#### 提示（Prompts）
交互模板，指导 LLM 如何与资源或工具交互

## MCP 与函数调用的区别

| 特性 | 函数调用 | MCP |
|-----|---------|-----|
| 标准化 | 专有，供应商特定 | 开放标准协议 |
| 范围 | 特定函数调用 | 广泛的通信框架 |
| 架构 | 一对一交互 | 客户端-服务器 |
| 发现 | 静态配置 | 动态发现 |
| 可重用性 | 紧耦合 | 高度可重用 |

## 使用场景

1. **数据库集成** - 访问和查询数据库
2. **文件系统操作** - 读写文件
3. **外部 API 交互** - 调用第三方 API
4. **IoT 设备控制** - 控制智能设备
5. **生成媒体编排** - 集成图像、视频、音频生成
6. **复杂工作流** - 编排多步骤任务系统

## 依赖安装

```bash
pip install langchain langchain-openai
```

## 环境变量设置

```bash
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_URL="your-api-url"  # 可选
```

## 关键优势

1. **标准化** - 开放协议，促进互操作性
2. **可发现性** - 动态发现可用能力
3. **可重用性** - 一次编写，多处使用
4. **组合性** - 组合多个 MCP 服务器构建复杂系统
5. **安全性** - 标准化的认证和授权机制

## 快速开始

```python
# 创建 MCP 服务器
server = FileSystemMCPServer("/path/to/directory")

# 创建客户端
client = MCPClient("my_client")
client.connect_to_server(server)

# 调用工具
files = client.call_tool("filesystem_server", "list_directory", {"path": "."})
```
