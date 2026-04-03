#!/bin/bash

echo "=========================================================="
echo "🎓 智能学习助手系统 - 快速启动"
echo "=========================================================="

# 检查 Python
if ! command -v python &> /dev/null; then
    echo "❌ 错误: 未找到 Python"
    exit 1
fi

echo "✅ Python 版本:"
python --version

# 检查并安装依赖
echo ""
echo "📦 检查依赖..."

if ! python -c "import flask" 2>/dev/null; then
    echo "🔧 安装 Flask..."
    pip install flask
fi

if ! python -c "import langgraph" 2>/dev/null; then
    echo "🔧 安装 LangGraph..."
    pip install langgraph langchain langchain-openai
fi

echo ""
echo "✅ 所有依赖已就绪！"

# 检查 API 密钥
if [ -z "$OPENAI_API_KEY" ]; then
    echo ""
    echo "⚠️  警告: 未设置 OPENAI_API_KEY"
    echo "系统将在演示模式下运行（模拟响应）"
    echo ""
    echo "如需使用真实 LLM，请设置："
    echo "  export OPENAI_API_KEY='your-api-key'"
    echo ""
else
    echo "✅ 已检测到 API 密钥，将使用真实 LLM"
    echo ""
fi

# 启动应用
echo "🚀 启动智能学习助手系统..."
echo "🌐 访问地址: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "=========================================================="
echo ""

python app.py
