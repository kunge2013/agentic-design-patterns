"""
智能客服学习助手 - Flask Web应用
"""
from flask import Flask, render_template, request, jsonify
from flasgger import Swagger, swag_from
from datetime import datetime
from customer_service_agent import LearningCustomerService

app = Flask(__name__)

# 初始化客服系统
cs_system = LearningCustomerService()

# 预设一些知识库
cs_system.add_knowledge_base_entry('product', '产品信息：我们提供多种智能产品，包括AI助手、自动化工具、数据分析平台等。')
cs_system.add_knowledge_base_entry('product', '产品保修：所有产品享受1年质保，可延保至3年。')
cs_system.add_knowledge_base_entry('pricing', '价格信息：基础版免费，专业版每月99元，企业版定制价格。')
cs_system.add_knowledge_base_entry('pricing', '支付方式：支持微信、支付宝、银行转账。')
cs_system.add_knowledge_base_entry('technical', '技术支持：提供7x24小时在线支持。')
cs_system.add_knowledge_base_entry('technical', '常见问题：请查看官网帮助中心或联系技术支持。')
cs_system.add_knowledge_base_entry('shipping', '配送时间：国内2-3天，国际7-14天。')
cs_system.add_knowledge_base_entry('shipping', '配送费用：订单满99元免邮，否则收10元运费。')
cs_system.add_knowledge_base_entry('refund', '退款政策：7天无理由退款。')
cs_system.add_knowledge_base_entry('refund', '退款流程：联系客服申请退款，审核通过后3-5个工作日到账。')


@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


@app.route('/api/ask', methods=['POST'])
@swag_from('docs/api_ask.yml')
def ask_question():
    """处理用户问题"""
    data = request.json
    question = data.get('question', '')
    user_id = data.get('user_id', 'anonymous')

    if not question:
        return jsonify({'error': '问题不能为空'}), 400

    # 生成回复
    response = cs_system.generate_response(question, user_id)

    # 识别问题类型
    question_type = cs_system.identify_question_type(question)

    return jsonify({
        'success': True,
        'response': response,
        'question_type': question_type,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/feedback', methods=['POST'])
@swag_from('docs/api_feedback.yml')
def submit_feedback():
    """提交用户反馈"""
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    question = data.get('question', '')
    response = data.get('response', '')
    rating = data.get('rating', 3)
    feedback_text = data.get('feedback_text', '')

    if not question or not response:
        return jsonify({'error': '缺少必要参数'}), 400

    # 记录反馈
    cs_system.record_feedback(user_id, question, response, rating, feedback_text)

    # 学习并调整策略
    learning_result = cs_system.learn_from_feedback()

    return jsonify({
        'success': True,
        'learning_result': learning_result
    })


@app.route('/api/health', methods=['GET'])
@swag_from('docs/api_health.yml')
def health_check():
    """系统健康检查"""
    return jsonify({
        'status': 'healthy',
        'version': cs_system.version,
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/version', methods=['GET'])
@swag_from('docs/api_version.yml')
def get_version():
    """获取系统版本信息"""
    return jsonify({
        'version': cs_system.version,
        'description': f'学习版本 {cs_system.version}'
    })


@app.route('/api/evaluate', methods=['GET'])
@swag_from('docs/api_evaluate.yml')
def evaluate():
    """系统自我评估"""
    evaluation = cs_system.self_evaluate()
    return jsonify(evaluation)


@app.route('/api/improve', methods=['POST'])
@swag_from('docs/api_improve.yml')
def auto_improve():
    """自动改进系统"""
    result = cs_system.auto_improve()
    return jsonify(result)


@app.route('/api/statistics', methods=['GET'])
@swag_from('docs/api_statistics.yml')
def statistics():
    """获取系统统计信息"""
    stats = cs_system.get_statistics()
    return jsonify(stats)


@app.route('/api/knowledge', methods=['GET'])
@swag_from('docs/api_knowledge_get.yml')
def get_knowledge():
    """获取知识库内容"""
    return jsonify({
        'knowledge_base': cs_system.knowledge_base
    })


@app.route('/api/knowledge', methods=['POST'])
@swag_from('docs/api_knowledge_post.yml')
def add_knowledge():
    """添加知识库条目"""
    data = request.json
    question_type = data.get('question_type', 'other')
    content = data.get('content', '')

    if not content:
        return jsonify({'error': '内容不能为空'}), 400

    cs_system.add_knowledge_base_entry(question_type, content)

    return jsonify({
        'success': True,
        'message': '知识库条目已添加'
    })


@app.route('/api/feedback_history', methods=['GET'])
@swag_from('docs/api_feedback_history.yml')
def feedback_history():
    """获取反馈历史"""
    limit = request.args.get('limit', 20, type=int)
    history = cs_system.feedback_history[-limit:]

    return jsonify({
        'total': len(cs_system.feedback_history),
        'history': [
            {
                'user_id': f.user_id,
                'question': f.question,
                'response': f.response[:100] + '...' if len(f.response) > 100 else f.response,
                'rating': f.rating,
                'feedback_text': f.feedback_text,
                'timestamp': f.timestamp
            }
            for f in history
        ]
    })


# 配置 Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "info": {
        "title": "智能客服学习助手 API",
        "description": "基于学习和适应模式的智能客服系统，提供问答、反馈收集、自我评估和自动改进功能",
        "contact": {
            "name": "Agentic Design Patterns Team",
            "url": "https://github.com/anthropics/anthropic-cookbook"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/api",
    "schemes": [
        "http",
        "https"
    ],
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ],
    "tags": [
        {
            "name": "客服对话",
            "description": "用户提问和系统回复相关接口"
        },
        {
            "name": "用户反馈",
            "description": "用户反馈收集和学习接口"
        },
        {
            "name": "系统管理",
            "description": "系统评估、统计和自动改进接口"
        },
        {
            "name": "知识库管理",
            "description": "知识库管理接口"
        }
    ]
}

swag = Swagger(app, config=swagger_config, template=swagger_template)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)