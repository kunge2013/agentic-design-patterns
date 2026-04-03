// 初始化
let currentResponse = '';
let currentQuestion = '';
let currentUserId = '';

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    mermaid.initialize({startOnLoad: true});
    loadStatistics();
    selectRating(3); // 默认3星
});

// 选择评分
function selectRating(rating) {
    document.getElementById('selected-rating').value = rating;

    // 更新按钮样式
    const buttons = document.querySelectorAll('.btn-group .btn');
    buttons.forEach((btn, index) => {
        if (index + 1 === rating) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// 提问
async function askQuestion() {
    const question = document.getElementById('question').value.trim();
    const userId = document.getElementById('user-id').value.trim() || 'anonymous';

    if (!question) {
        alert('请输入问题！');
        return;
    }

    currentQuestion = question;
    currentUserId = userId;

    // 显示用户消息
    addChatMessage('user', question, userId);

    // 禁用输入
    document.getElementById('question').disabled = true;

    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                user_id: userId
            })
        });

        const data = await response.json();

        if (data.success) {
            currentResponse = data.response;

            // 显示助手回复
            addChatMessage('assistant', data.response, data.question_type);

            // 清空输入框
            document.getElementById('question').value = '';
        } else {
            alert('处理失败：' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('请求失败，请稍后再试');
    } finally {
        // 启用输入
        document.getElementById('question').disabled = false;
        document.getElementById('question').focus();
    }
}

// 添加聊天消息
function addChatMessage(type, content, meta = '') {
    const chatHistory = document.getElementById('chat-history');

    // 清除占位符
    if (chatHistory.querySelector('.text-center')) {
        chatHistory.innerHTML = '';
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}-message`;

    const time = new Date().toLocaleTimeString('zh-CN');

    messageDiv.innerHTML = `
        <div class="message-meta">
            ${type === 'user' ? '用户' : '客服助手'} | ${time}
            ${meta ? ` | 类型: ${meta}` : ''}
        </div>
        <div class="message-content">${content}</div>
    `;

    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// 提交反馈
async function submitFeedback() {
    if (!currentResponse || !currentQuestion) {
        alert('请先提问并获得回复后再提交反馈！');
        return;
    }

    const rating = parseInt(document.getElementById('selected-rating').value);
    const feedbackText = document.getElementById('feedback-text').value.trim();

    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: currentUserId,
                question: currentQuestion,
                response: currentResponse,
                rating: rating,
                feedback_text: feedbackText
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('感谢您的反馈！系统将学习并改进。');

            // 清空反馈表单
            document.getElementById('feedback-text').value = '';
            selectRating(3);

            // 刷新统计
            loadStatistics();

            // 显示学习结果
            if (data.learning_result.learned) {
                console.log('学习结果:', data.learning_result);
                showNotification('系统已根据您的反馈调整策略');
            }
        } else {
            alert('提交反馈失败：' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('提交反馈失败，请稍后再试');
    }
}

// 自我评估
async function evaluate() {
    showNotification('正在进行自我评估...');

    try {
        const response = await fetch('/api/evaluate');
        const data = await response.json();

        displayEvaluationResult(data);
        showNotification('自我评估完成');
    } catch (error) {
        console.error('Error:', error);
        alert('评估失败，请稍后再试');
    }
}

// 显示评估结果
function displayEvaluationResult(evaluation) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">自我评估结果</h5>
                    <button type="button" class="btn-close" onclick="closeModal(this)"></button>
                </div>
                <div class="modal-body">
                    <h6>综合得分: ${evaluation.overall_score ? (evaluation.overall_score * 100).toFixed(1) + '%' : 'N/A'}</h6>

                    ${evaluation.areas_to_improve && evaluation.areas_to_improve.length > 0 ? `
                    <div class="alert alert-warning">
                        <strong>需要改进的领域：</strong>
                        <ul>
                            ${evaluation.areas_to_improve.map(area => `<li>${area}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}

                    ${evaluation.strengths && evaluation.strengths.length > 0 ? `
                    <div class="alert alert-success">
                        <strong>优势领域：</strong>
                        <ul>
                            ${evaluation.strengths.map(strength => `<li>${strength}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}

                    ${evaluation.recommendations && evaluation.recommendations.length > 0 ? `
                    <div class="alert alert-info">
                        <strong>改进建议：</strong>
                        <ul>
                            ${evaluation.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}

                    ${evaluation.basic_metrics ? `
                    <h6 class="mt-3">基础指标：</h6>
                    <ul>
                        <li>总反馈数: ${evaluation.basic_metrics.total_feedback || 0}</li>
                        <li>平均评分: ${evaluation.basic_metrics.avg_rating ? evaluation.basic_metrics.avg_rating.toFixed(2) : 'N/A'}</li>
                        <li>最近平均评分: ${evaluation.basic_metrics.recent_avg ? evaluation.basic_metrics.recent_avg.toFixed(2) : 'N/A'}</li>
                    </ul>
                    ` : ''}
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.classList.add('show');
    modal.style.display = 'block';
}

// 自动改进
async function autoImprove() {
    if (!confirm('确定要执行自动改进吗？这将基于当前反馈数据调整系统策略。')) {
        return;
    }

    showNotification('正在执行自动改进...');

    try {
        const response = await fetch('/api/improve', {
            method: 'POST'
        });
        const data = await response.json();

        displayAutoImproveResult(data);
        showNotification('自动改进完成');

        // 刷新统计
        loadStatistics();
    } catch (error) {
        console.error('Error:', error);
        alert('自动改进失败，请稍后再试');
    }
}

// 显示自动改进结果
function displayAutoImproveResult(result) {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">自动改进结果</h5>
                    <button type="button" class="btn-close" onclick="closeModal(this)"></button>
                </div>
                <div class="modal-body">
                    <h6>学习阶段</h6>
                    ${result.learning ? `
                    <ul>
                        <li>是否学习: ${result.learning.learned ? '是' : '否'}</li>
                        <li>版本: ${result.learning.version || 'N/A'}</li>
                        <li>消息: ${result.learning.message || ''}</li>
                        ${result.learning.changes && result.learning.changes.length > 0 ? `
                        <li>改进: ${result.learning.changes.join(', ')}</li>
                        ` : ''}
                    </ul>
                    ` : ''}

                    <h6 class="mt-3">评估阶段</h6>
                    ${result.evaluation ? `
                    <ul>
                        <li>综合得分: ${result.evaluation.overall_score ? (result.evaluation.overall_score * 100).toFixed(1) + '%' : 'N/A'}</li>
                        ${result.evaluation.areas_to_improve && result.evaluation.areas_to_improve.length > 0 ? `
                        <li>需要改进: ${result.evaluation.areas_to_improve.join(', ')}</li>
                        ` : ''}
                        ${result.evaluation.strengths && result.evaluation.strengths.length > 0 ? `
                        <li>优势: ${result.evaluation.strengths.join(', ')}</li>
                        ` : ''}
                    </ul>
                    ` : ''}

                    <h6 class="mt-3">改进实施</h6>
                    ${result.implementation ? `
                    <ul>
                        <li>已实施: ${result.implementation.implemented ? result.implementation.implemented.length : 0} 项</li>
                        <li>跳过: ${result.implementation.skipped ? result.implementation.skipped.length : 0} 项</li>
                    </ul>
                    ${result.implementation.implemented && result.implementation.implemented.length > 0 ? `
                    <div class="alert alert-success">
                        <strong>已实施的改进：</strong>
                        <ul>
                            ${result.implementation.implemented.map(imp => `<li>${imp}</li>`).join('')}
                        </ul>
                    </div>
                    ` : ''}
                    ` : ''}
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.classList.add('show');
    modal.style.display = 'block';
}

// 加载统计信息
async function loadStatistics() {
    try {
        const response = await fetch('/api/statistics');
        const data = await response.json();

        // 更新显示
        document.getElementById('version').textContent = data.version;

        if (data.basic_metrics) {
            document.getElementById('total-feedback').textContent = data.basic_metrics.total_feedback || 0;
            document.getElementById('avg-rating').textContent =
                (data.basic_metrics.avg_rating || 0).toFixed(2);
        }

        document.getElementById('total-users').textContent = data.total_users || 0;

        if (data.overall_score !== undefined) {
            document.getElementById('overall-score').textContent =
                (data.overall_score * 100).toFixed(1) + '%';
        }

        // 更新策略参数
        updateStrategyParams(data.strategy_params);

        // 加载反馈历史
        loadFeedbackHistory();
    } catch (error) {
        console.error('Error:', error);
    }
}

// 更新策略参数显示
function updateStrategyParams(params) {
    const container = document.getElementById('strategy-params');

    if (!params) {
        container.innerHTML = '<div class="text-muted">暂无数据</div>';
        return;
    }

    let html = '<ul class="list-group">';
    for (const [key, value] of Object.entries(params)) {
        const displayValue = typeof value === 'boolean' ? (value ? '是' : '否') : value;
        html += `<li class="list-group-item">
            <strong>${key}:</strong> ${displayValue}
        </li>`;
    }
    html += '</ul>';

    container.innerHTML = html;
}

// 加载反馈历史
async function loadFeedbackHistory() {
    try {
        const response = await fetch('/api/feedback_history?limit=10');
        const data = await response.json();

        const tbody = document.getElementById('feedback-table-body');

        if (data.history && data.history.length > 0) {
            tbody.innerHTML = data.history.map(item => `
                <tr>
                    <td>${item.timestamp.split('T')[1].split('.')[0]}</td>
                    <td>${item.user_id}</td>
                    <td>${item.question.substring(0, 30)}...</td>
                    <td>${'⭐'.repeat(item.rating)}</td>
                    <td>${item.feedback_text || '无'}</td>
                </tr>
            `).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">暂无反馈记录</td></tr>';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// 关闭模态框
function closeModal(button) {
    const modal = button.closest('.modal');
    modal.classList.remove('show');
    modal.style.display = 'none';
    setTimeout(() => modal.remove(), 300);
}

// 显示通知
function showNotification(message) {
    // 创建通知元素
    const notification = document.createElement('div');
    notification.className = 'toast-notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #0d6efd;
        color: white;
        padding: 15px 25px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease-out;
    `;

    document.body.appendChild(notification);

    // 3秒后自动消失
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-in';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 添加动画样式
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }

    .modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1050;
    }

    .modal-dialog {
        background-color: white;
        border-radius: 0.5rem;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    }
`;
document.head.appendChild(style);

// 添加CSS
const cssLink = document.createElement('link');
cssLink.rel = 'stylesheet';
cssLink.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css';
document.head.appendChild(cssLink);

// 知识库管理功能
async function addKnowledge() {
    const questionType = document.getElementById('knowledge-type').value;
    const content = document.getElementById('knowledge-content').value.trim();

    if (!content) {
        alert('请输入知识内容！');
        return;
    }

    try {
        const response = await fetch('/api/knowledge', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_type: questionType,
                content: content
            })
        });

        const data = await response.json();

        if (data.success) {
            alert('知识库条目添加成功！');

            // 清空输入
            document.getElementById('knowledge-content').value = '';

            // 显示成功通知
            showNotification('知识库已更新');
        } else {
            alert('添加失败：' + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('添加失败，请稍后再试');
    }
}

async function viewKnowledge() {
    showNotification('正在加载知识库...');

    try {
        const response = await fetch('/api/knowledge');
        const data = await response.json();

        displayKnowledgeBase(data.knowledge_base);
        showNotification('知识库加载完成');
    } catch (error) {
        console.error('Error:', error);
        alert('加载知识库失败，请稍后再试');
    }
}

function displayKnowledgeBase(knowledgeBase) {
    let html = '<div class="list-group">';

    for (const [type, entries] of Object.entries(knowledgeBase)) {
        const typeNames = {
            'product': '产品信息',
            'pricing': '价格信息',
            'technical': '技术支持',
            'shipping': '配送信息',
            'refund': '退款政策',
            'other': '其他'
        };

        html += `
            <div class="list-group-item">
                <strong>${typeNames[type] || type}</strong>
                <span class="badge bg-secondary float-end">${entries.length} 条</span>
                <ul class="mt-2 mb-0">
                    ${entries.map(entry => `<li>${entry}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    html += '</div>';

    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">知识库内容</h5>
                    <button type="button" class="btn-close" onclick="closeModal(this)"></button>
                </div>
                <div class="modal-body">
                    ${html}
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);
    modal.classList.add('show');
    modal.style.display = 'block';
}
