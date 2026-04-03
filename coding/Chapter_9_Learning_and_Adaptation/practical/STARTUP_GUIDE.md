# 智能客服学习助手 - 启动指南

## 🚀 快速启动

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

#### 方法 A：使用 .env 文件
```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填入你的 API 密钥
nano .env
```

#### 方法 B：设置环境变量
```bash
export OPENAI_API_KEY='your-api-key-here'
```

### 3. 启动应用
```bash
python app.py
```

应用将在 `http://localhost:5000` 启动

## 📚 Swagger API 文档访问

### 主要文档地址

1. **Swagger UI 交互式文档**
   ```
   http://localhost:5000/api/docs
   ```
   这是推荐的访问方式，提供：
   - 完整的 API 文档
   - 在线测试功能
   - 请求/响应示例
   - 代码示例生成

2. **API 规范文件 (JSON)**
   ```
   http://localhost:5000/apispec.json
   ```
   这是机器可读的 OpenAPI 规范文件

3. **主应用界面**
   ```
   http://localhost:5000/
   ```
   Web 用户界面

## 📋 API 接口列表

### 客服对话
- `POST /api/ask` - 处理用户问题

### 用户反馈
- `POST /api/feedback` - 提交用户反馈

### 系统管理
- `GET /api/health` - 健康检查
- `GET /api/version` - 获取版本信息
- `GET /api/evaluate` - 系统自我评估
- `POST /api/improve` - 自动改进系统
- `GET /api/statistics` - 获取统计信息
- `GET /api/feedback_history` - 获取反馈历史

### 知识库管理
- `GET /api/knowledge` - 获取知识库内容
- `POST /api/knowledge` - 添加知识库条目

## 🧪 测试 API

### 自动化测试
```bash
python test_swagger_api.py
```

### 手动测试（使用 curl）

#### 健康检查
```bash
curl http://localhost:5000/api/health
```

#### 提问
```bash
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "你们的产品有什么特点？",
    "user_id": "test_user"
  }'
```

#### 提交反馈
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user",
    "question": "你们的产品有什么特点？",
    "response": "我们提供多种智能产品...",
    "rating": 5,
    "feedback_text": "回答很详细"
  }'
```

## 📖 文档资源

- **Swagger 配置说明**: `SWAGGER_README.md`
- **全局配置**: `swagger_config.yml`
- **接口文档**: `docs/` 目录

## 🔧 常见问题

### Q: 应用启动失败，提示缺少 API 密钥
A: 请按照上述方法配置 `OPENAI_API_KEY` 环境变量

### Q: Swagger 文档无法访问
A: 确认应用已正常启动，访问 `http://localhost:5000/api/docs`

### Q: 接口调用失败
A: 检查 API 密钥是否正确，网络连接是否正常

## 📝 开发说明

### 添加新接口
1. 在 `docs/` 目录创建 YAML 文档
2. 在 `app.py` 添加路由和 `@swag_from` 装饰器
3. 重启应用查看文档

### 修改现有接口
1. 编辑对应的 YAML 文档
2. 重启应用查看更新

## 🌐 部署

### 生产环境
```bash
# 使用 gunicorn 启动
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker 部署
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 📞 支持

如有问题，请查看：
- 项目文档
- GitHub Issues
- Swagger UI 内的文档说明