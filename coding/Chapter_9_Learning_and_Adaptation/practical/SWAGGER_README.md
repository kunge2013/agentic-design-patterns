# Swagger API 文档配置说明

本项目使用 **Flasgger** 和 **装饰器注解** 的方式配置 Swagger API 文档。

## 项目结构

```
practical/
├── app.py                      # Flask 应用主文件
├── swagger_config.yml           # 全局 Swagger 配置
├── docs/                       # 接口文档目录
│   ├── api_ask.yml             # 提问接口文档
│   ├── api_feedback.yml        # 反馈接口文档
│   ├── api_health.yml          # 健康检查接口文档
│   ├── api_version.yml         # 版本接口文档
│   ├── api_evaluate.yml        # 评估接口文档
│   ├── api_improve.yml         # 改进接口文档
│   ├── api_statistics.yml       # 统计接口文档
│   ├── api_knowledge_get.yml   # 获取知识库接口文档
│   ├── api_knowledge_post.yml  # 添加知识库接口文档
│   └── api_feedback_history.yml # 反馈历史接口文档
├── test_swagger_api.py         # API 测试脚本
└── requirements.txt
```

## 核心特性

### 1. 装饰器注解配置

使用 `@swag_from` 装饰器从外部 YAML 文件加载文档：

```python
from flasgger import swag_from

@app.route('/api/ask', methods=['POST'])
@swag_from('docs/api_ask.yml')
def ask_question():
    """处理用户问题"""
    # 业务逻辑
    pass
```

### 2. 外部 YAML 配置文件

每个接口的文档都存储在独立的 YAML 文件中：

```yaml
tags:
  - 客服对话
summary: 处理用户问题
description: 接收用户问题并生成智能回复
consumes:
  - application/json
produces:
  - application/json
parameters:
  - in: body
    name: body
    required: true
    schema:
      $ref: '#/definitions/AskRequest'
responses:
  200:
    description: 请求成功
    schema:
      $ref: '#/definitions/AskResponse'
definitions:
  AskRequest:
    type: object
    required:
      - question
    properties:
      question:
        type: string
        description: 用户提问内容
        example: "你们的产品有什么特点？"
```

### 3. 全局配置文件

`swagger_config.yml` 包含全局配置：

```yaml
info:
  title: 智能客服学习助手 API
  description: 基于学习和适应模式的智能客服系统
  version: "1.0.0"
  contact:
    name: Agentic Design Patterns Team
    url: https://github.com/anthropics/anthropic-cookbook
```

## 优势

### ✅ 代码整洁
- 业务逻辑和文档分离
- 函数体保持简洁
- 易于维护和更新

### ✅ 文档集中管理
- 所有文档存储在 `docs/` 目录
- 版本控制友好
- 支持团队协作

### ✅ 类型定义复用
- 使用 `definitions` 定义可复用的数据结构
- 通过 `$ref` 引用避免重复
- 保持文档一致性

### ✅ 易于扩展
- 添加新接口只需创建新的 YAML 文件
- 使用装饰器即可配置
- 支持多语言文档

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

主要依赖：
- `flask==3.0.0` - Web 框架
- `flasgger==0.9.7.1` - Swagger 文档生成
- `langchain==0.1.6` - LLM 集成

### 2. 启动应用

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 3. 访问 API 文档

打开浏览器访问：
- **Swagger UI**: http://localhost:5000/api/docs
- **API 规范**: http://localhost:5000/apispec.json

### 4. 测试 API

运行自动化测试脚本：

```bash
python test_swagger_api.py
```

## 添加新接口

### 步骤 1: 创建文档文件

在 `docs/` 目录创建新的 YAML 文件：

```bash
touch docs/api_your_endpoint.yml
```

### 步骤 2: 编写文档内容

```yaml
tags:
  - 接口分类
summary: 接口简短描述
description: |
  接口详细描述
  可以使用 Markdown 格式
parameters:
  - name: param1
    in: query
    type: string
    required: true
    description: 参数描述
responses:
  200:
    description: 成功响应
    schema:
      type: object
      properties:
        success:
          type: boolean
```

### 步骤 3: 添加路由和装饰器

```python
@app.route('/api/your_endpoint', methods=['GET'])
@swag_from('docs/api_your_endpoint.yml')
def your_endpoint():
    """接口描述"""
    # 业务逻辑
    return jsonify({'success': True})
```

### 步骤 4: 更新全局配置（可选）

在 `swagger_config.yml` 中添加接口定义：

```yaml
paths:
  /api/your_endpoint:
    get:
      $ref: 'docs/api_your_endpoint.yml#/get'
```

## YAML 文档格式

### 基本信息

```yaml
tags:
  - 接口分类标签
summary: 单行简短描述
description: |
  详细描述
  支持 Markdown 格式
```

### 参数定义

```yaml
parameters:
  # Query 参数
  - name: limit
    in: query
    type: integer
    default: 20
    description: 限制返回数量

  # Body 参数
  - in: body
    name: body
    required: true
    schema:
      $ref: '#/definitions/MyRequest'
```

### 响应定义

```yaml
responses:
  200:
    description: 成功
    schema:
      $ref: '#/definitions/MyResponse'
  400:
    description: 错误
    schema:
      $ref: '#/definitions/ErrorResponse'
```

### 数据类型定义

```yaml
definitions:
  MyRequest:
    type: object
    required:
      - field1
    properties:
      field1:
        type: string
        description: 字段描述
      field2:
        type: integer
        minimum: 1
        maximum: 10
```

## 常见配置

### 数据类型

- `string` - 字符串
- `integer` - 整数
- `number` - 浮点数
- `boolean` - 布尔值
- `array` - 数组
- `object` - 对象

### 参数位置

- `query` - URL 查询参数
- `body` - 请求体
- `path` - URL 路径参数
- `header` - 请求头

### 验证规则

```yaml
properties:
  email:
    type: string
    format: email
  age:
    type: integer
    minimum: 0
    maximum: 120
  status:
    type: string
    enum: [active, inactive, pending]
```

## 最佳实践

1. **使用复用定义**
   - 在 `definitions` 中定义常用数据结构
   - 使用 `$ref` 引用避免重复

2. **提供示例**
   - 为每个参数提供 `example`
   - 帮助开发者快速理解接口用法

3. **详细描述**
   - 使用 `description` 解释参数用途
   - 说明约束条件和业务规则

4. **版本管理**
   - 在 `swagger_config.yml` 中管理版本号
   - 记录重要变更

5. **统一错误格式**
   - 定义标准的错误响应结构
   - 使用 `ErrorResponse` 引用

## 故障排除

### 装饰器不生效

**问题**: 装饰器无法正确加载 YAML 文件

**解决**:
1. 检查文件路径是否正确
2. 确认 YAML 语法无误
3. 验证文件编码为 UTF-8

### 文档不显示

**问题**: Swagger UI 显示空页面

**解决**:
1. 确认 `Swagger` 初始化在路由定义之后
2. 检查 `swagger_config.yml` 路径
3. 查看控制台错误信息

### 类型定义引用失败

**问题**: `$ref` 无法正确引用定义

**解决**:
1. 确认引用路径格式正确
2. 验证 `definitions` 中存在目标定义
3. 检查 YAML 缩进

## 相关资源

- [Flasgger 文档](https://github.com/flasgger/flasgger)
- [OpenAPI 规范](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)

## 联系方式

如有问题，请：
- 提交 Issue
- 查看项目文档
- 联系开发团队