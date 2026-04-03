# 智能学习助手系统

## 项目概述

智能学习助手系统是一个完整的 Web 应用，展示了 Agentic 设计模式中记忆管理的实际应用。该系统集成了语义记忆、情景记忆和程序记忆，通过记忆感知智能体提供个性化的学习体验。

## 核心特性

### 1. 🧠 语义记忆（Semantic Memory）
存储用户的静态信息和长期知识：
- 用户基本画像（姓名、学习目标）
- 学习偏好（编程水平、学习风格）
- 技能评估（各个技术领域掌握程度）

### 2. 📖 情景记忆（Episodic Memory）
记录学习过程中的具体事件和经历：
- 学习会话记录（主题、时长、备注）
- 问答交互历史（问题、答案、时间戳）
- 学习事件的时间序列

### 3. 📚 程序记忆（Procedural Memory）
存储教学策略和操作规则：
- 教学原则（脚手架、主动学习等）
- 响应模板（标准化回复格式）
- 评估标准（不同水平的学习目标）

### 4. 🤖 记忆感知智能体
自动整合三种记忆类型：
- 处理请求前检索用户画像和历史
- 根据用户水平生成个性化响应
- 更新情景记忆以维持上下文

### 5. 💾 跨会话记忆
保持长期学习记录：
- 用户画像持久化
- 学习进度追踪
- 个性化体验连续性

## 系统架构

```mermaid
graph TD
    A[浏览器用户界面] --> B[Flask Web 后端]
    B --> C[记忆感知智能体]

    C --> D{记忆检索层}
    D --> D1[语义记忆<br/>用户画像]
    D --> D2[情景记忆<br/>学习历史]
    D --> D3[程序记忆<br/>教学策略]

    D1 --> E[上下文集成构建]
    D2 --> E
    D3 --> E

    E --> F[LLM 处理生成]
    F --> G[个性化响应]

    G --> H{记忆更新层}
    H --> H1[记录新交互]
    H --> H2[更新学习统计]

    H1 --> I[InMemoryStore]
    H2 --> I

    I --> J[响应返回]
    J --> A
```

## 智能体工作流程

```mermaid
graph LR
    START([开始]) --> A[检索用户上下文]
    A --> B[处理学习请求]
    B --> C[更新学习记忆]
    C --> END([结束])

    A --> A1[获取用户画像]
    A --> A2[获取教学策略]
    A --> A3[获取学习历史]

    B --> B1{请求类型}
    B1 -->|学习计划| B2[生成学习路径]
    B1 -->|技术问题| B3[回答编程问题]
    B1 -->|进度查询| B4[生成统计报告]
    B1 -->|其他| B5[处理一般请求]

    C --> C1[记录交互历史]
    C --> C2[更新统计数据]
```

## 技术栈

- **Flask 3.0+**: Web 后端框架
- **LangGraph**: 构建记忆感知智能体工作流
- **InMemoryStore**: 提供内存中的持久化存储
- **LangChain**: LLM 集成和提示管理
- **OpenAI API**: 自然语言处理和响应生成
- **HTML5/CSS3**: 响应式前端界面

## 安装和运行

### 环境要求

- Python 3.9+
- pip 包管理器

### 安装步骤

1. **创建虚拟环境**
```bash
cd coding/practical
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置 API 密钥**（可选）
```bash
export OPENAI_API_KEY='your-api-key'
```

### 运行应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

## 使用指南

### 1. 设置学习档案

首次使用时，请创建学习档案：

1. 在"设置学习档案"卡片中填写以下信息：
   - 姓名：你的名字
   - 当前水平：初学者/中级/高级
   - 学习目标：例如"成为一名全栈 Python 开发者"

2. 点击"创建学习档案"按钮

### 2. 使用学习助手

在"学习助手"卡片中进行交互：

**学习计划请求**
- 选择请求类型：`学习计划`
- 输入你想学习的内容
- 点击"获取帮助"
- 系统会根据你的水平生成个性化学习路径

**技术问题咨询**
- 选择请求类型：`技术问题`
- 提出具体的编程问题
- 系统会提供详细解答和代码示例

**学习进度查询**
- 选择请求类型：`学习进度`
- 点击"获取帮助"
- 系统会显示你的学习统计和建议

### 3. 快捷操作

**查看学习历史**
- 点击"查看学习历史"按钮
- 查看最近的学习会话和问答记录

**学习统计**
- 点击"学习统计"按钮
- 查看总体学习数据和用户画像状态

**记录学习会话**
- 点击"记录学习会话"按钮
- 记录当前的学习活动

**系统信息**
- 点击"系统信息"按钮
- 查看系统配置和功能特性

## API 端点

### 用户画像管理

#### 设置用户画像
```http
POST /setup_profile
Content-Type: application/json

{
    "name": "张小明",
    "level": "intermediate",
    "goal": "成为一名全栈 Python 开发者"
}
```

### 智能体交互

#### 发送学习请求
```http
POST /learning_request
Content-Type: application/json

{
    "message": "我想学习 Python Web 开发",
    "type": "learn"
}
```

**请求类型**：
- `learn`: 学习计划请求
- `question`: 技术问题咨询
- `progress`: 进度查询

#### 记录学习会话
```http
POST /record_session
Content-Type: application/json

{
    "topic": "Python Web 开发",
    "duration": 30,
    "notes": "学习 Flask 基础"
}
```

### 信息查询

#### 获取学习历史
```http
GET /get_history
```

#### 获取学习统计
```http
GET /get_stats
```

#### 获取系统信息
```http
GET /system_info
```

## 记忆组织结构

### 命名空间设计

```python
# 语义记忆命名空间
(user_id, "semantic_memory")
    ├── profile          # 用户基本信息
    └── preferences       # 学习偏好和目标

# 情景记忆命名空间
(user_id, "episodic_memory")
    ├── session_*        # 学习会话记录
    └── qa_*            # 问答交互记录

# 程序记忆命名空间
("system", "procedural_memory")
    ├── teaching_principles  # 教学原则
    └── response_templates   # 响应模板
```

## 扩展功能

### 添加新的请求类型

1. 在 `app.py` 中添加新的处理函数
2. 更新前端的请求类型选择器
3. 在智能体中实现新的响应逻辑

### 集成外部存储

替换 `InMemoryStore` 为持久化存储：

```python
from langgraph.store.postgres import AsyncPostgresStore

# 初始化时使用外部存储
memory_store = AsyncPostgresStore(conn_string="postgresql://user:pass@localhost/db")
```

### 添加用户认证

在 Flask 应用中添加用户认证：

```python
from flask_login import LoginManager, login_required

@app.route('/protected')
@login_required
def protected_view():
    # 需要登录的页面
    pass
```

## 开发和调试

### 前端调试

1. 打开浏览器开发者工具（F12）
2. 查看 Console 中的错误信息
3. 使用 Network 标签查看 API 请求

### 后端调试

应用默认以 debug 模式运行：

```python
app.run(debug=True, host='0.0.0.0', port=5000)
)
```

修改代码后会自动重载。

### 查看记忆状态

在 Python 交互式环境中检查记忆：

```python
from app import memory_store

# 获取用户画像
profile = memory_store.get(("user001", "semantic_memory"), "profile")
print(profile.value)

# 搜索学习历史
history = memory_store.search(("user001", "episodic_memory"))
for item in history:
    print(item.value)
```

## 性能优化建议

### 1. 前端优化

- 使用浏览器缓存
- 实现请求节流
- 添加加载状态指示器

### 2. 后端优化

- 使用异步存储操作
- 实现记忆缓存机制
- 批量处理记忆更新

### 3. 数据优化

- 定期清理过期记忆
- 压缩存储的数据
- 使用索引加速查询

## 部署

### 本地部署

```bash
# 设置生产环境变量
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key

# 运行应用
python app.py
```

### Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

构建和运行：

```bash
docker build -t learning-assistant .
docker run -p 5000:5000 learning-assistant
```

## 安全注意事项

### 生产环境配置

1. **更改密钥**
```python
app.secret_key = 'your-secure-random-secret-key'
```

2. **启用 HTTPS**
```python
from flask_sslify import SSLify
app = SSLify(app)
```

3. **添加 CORS 支持**
```python
from flask_cors import CORS
CORS(app)
```

## 应用场景

### 1. 在线教育平台
- 个性化学习路径推荐
- 智能作业批改
- 学习效果分析

### 2. 企业培训系统
- 员工技能管理
- 培训进度跟踪
- 知识问答助手

### 3. 编程教育应用
- 代码学习指导
- 错误诊断和建议
- 项目实践支持

### 4. 个人学习助手
- 学习笔记管理
- 知识关联和检索
- 学习成果可视化

## 总结

智能学习助手系统完整展示了记忆管理的实际应用：

**核心价值**：
- ✅ 个性化体验 - 基于用户画像定制内容
- ✅ 连续学习 - 跨会话维持上下文
- ✅ 智能适应 - 根据反馈调整策略
- ✅ 长期成长 - 追踪学习历程和进步

**技术亮点**：
- 三种记忆类型协同工作
- LangGraph 状态机工作流
- 记忆感知智能体设计
- 完整的 Web 应用架构
- 可扩展的架构模式

这个项目可以作为构建个性化 AI 应用和智能教育系统的基础框架，展示了 Agentic 设计模式中记忆管理的最佳实践。
