#!/usr/bin/env python3
"""
Swagger API 测试脚本
测试所有 API 接口是否正常工作并生成测试报告
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_swagger_docs():
    """测试 Swagger 文档页面"""
    print_section("测试 Swagger 文档页面")
    try:
        response = requests.get(f"{BASE_URL}/api/docs")
        if response.status_code == 200:
            print("✅ Swagger 文档页面访问成功")
            print(f"   URL: {BASE_URL}/api/docs")
            return True
        else:
            print(f"❌ Swagger 文档页面访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_swagger_spec():
    """测试 Swagger 规范文件"""
    print_section("测试 Swagger 规范文件")
    try:
        response = requests.get(f"{BASE_URL}/apispec.json")
        if response.status_code == 200:
            spec = response.json()
            print("✅ Swagger 规范文件获取成功")
            print(f"   标题: {spec.get('info', {}).get('title', 'N/A')}")
            print(f"   版本: {spec.get('info', {}).get('version', 'N/A')}")
            print(f"   接口数量: {len(spec.get('paths', {}))}")

            # 列出所有接口
            print("\n   可用接口:")
            for path, methods in spec.get('paths', {}).items():
                for method in methods.keys():
                    print(f"   - {method.upper()} {path}")
            return True
        else:
            print(f"❌ Swagger 规范文件获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取规范文件失败: {e}")
        return False

def test_health_check():
    """测试健康检查接口"""
    print_section("测试健康检查接口")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ 健康检查成功")
            print(f"   状态: {data.get('status', 'N/A')}")
            print(f"   版本: {data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查请求失败: {e}")
        return False

def test_get_version():
    """测试版本接口"""
    print_section("测试版本接口")
    try:
        response = requests.get(f"{BASE_URL}/api/version")
        if response.status_code == 200:
            data = response.json()
            print("✅ 版本信息获取成功")
            print(f"   版本号: {data.get('version', 'N')}")
            print(f"   描述: {data.get('description', 'N/A')}")
            return True
        else:
            print(f"❌ 版本信息获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 版本信息请求失败: {e}")
        return False

def test_ask_question():
    """测试提问接口"""
    print_section("测试提问接口")
    try:
        payload = {
            "question": "你们的产品有什么特点？",
            "user_id": "test_user"
        }
        response = requests.post(
            f"{BASE_URL}/api/ask",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ 提问请求成功")
            print(f"   问题类型: {data.get('question_type', 'N/A')}")
            print(f"   回答: {data.get('response', 'N/A')[:50]}...")
            return True
        else:
            print(f"❌ 提问请求失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 提问请求失败: {e}")
        return False

def test_get_statistics():
    """测试统计信息接口"""
    print_section("测试统计信息接口")
    try:
        response = requests.get(f"{BASE_URL}/api/statistics")
        if response.status_code == 200:
            data = response.json()
            print("✅ 统计信息获取成功")
            print(f"   版本: {data.get('version', 'N/A')}")
            print(f"   总用户数: {data.get('total_users', 0)}")
            if data.get('basic_metrics'):
                print(f"   总反馈数: {data['basic_metrics'].get('total_feedback', 0)}")
            return True
        else:
            print(f"❌ 统计信息获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 统计信息请求失败: {e}")
        return False

def test_get_knowledge():
    """测试获取知识库接口"""
    print_section("测试获取知识库接口")
    try:
        response = requests.get(f"{BASE_URL}/api/knowledge")
        if response.status_code == 200:
            data = response.json()
            print("✅ 知识库获取成功")
            kb = data.get('knowledge_base', {})
            print(f"   知识库类型数: {len(kb)}")
            for kb_type, entries in kb.items():
                print(f"   - {kb_type}: {len(entries)} 条")
            return True
        else:
            print(f"❌ 知识库获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 知识库请求失败: {e}")
        return False

def test_add_knowledge():
    """测试添加知识库接口"""
    print_section("测试添加知识库接口")
    try:
        payload = {
            "question_type": "test",
            "content": "测试知识库条目，用于验证 Swagger API 功能"
        }
        response = requests.post(
            f"{BASE_URL}/api/knowledge",
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ 知识库条目添加成功")
            print(f"   消息: {data.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ 知识库条目添加失败: {response.status_code}")
            print(f"   错误: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 知识库添加请求失败: {e}")
        return False

def test_get_feedback_history():
    """测试获取反馈历史接口"""
    print_section("测试获取反馈历史接口")
    try:
        response = requests.get(f"{BASE_URL}/api/feedback_history?limit=5")
        if response.status_code == 200:
            data = response.json()
            print("✅ 反馈历史获取成功")
            print(f"   总记录数: {data.get('total', 0)}")
            print(f"   返回记录数: {len(data.get('history', []))}")
            return True
        else:
            print(f"❌ 反馈历史获取失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 反馈历史请求失败: {e}")
        return False

def test_evaluate():
    """测试自我评估接口"""
    print_section("测试自我评估接口")
    try:
        response = requests.get(f"{BASE_URL}/api/evaluate")
        if response.status_code == 200:
            data = response.json()
            print("✅ 自我评估执行成功")
            print(f"   综合得分: {data.get('overall_score', 0) * 100:.1f}%")
            if data.get('areas_to_improve'):
                print(f"   需要改进: {len(data['areas_to_improve'])} 项")
            if data.get('strengths'):
                print(f"   优势: {len(data['strengths'])} 项")
            return True
        else:
            print(f"❌ 自我评估失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 自我评估请求失败: {e}")
        return False

def generate_report(results):
    """生成测试报告"""
    print_section("测试报告汇总")
    total = len(results)
    passed = sum(1 for result in results.values() if result)
    failed = total - passed

    print(f"总测试数: {total}")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"成功率: {passed/total*100:.1f}%")

    print("\n详细结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")

    return passed == total

def main():
    """主测试函数"""
    print(f"""
╔═════════════════════════════════════════════════════════════════╗
║           智能客服学习助手 - Swagger API 测试                  ║
║           测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}          ║
╚═════════════════════════════════════════════════════════════════╝
    """)

    results = {}

    # 测试 Swagger 文档
    results["Swagger 文档页面"] = test_swagger_docs()
    results["Swagger 规范文件"] = test_swagger_spec()

    # 测试基础接口
    results["健康检查"] = test_health_check()
    results["版本信息"] = test_get_version()

    # 测试核心功能
    results["提问接口"] = test_ask_question()
    results["统计信息"] = test_get_statistics()
    results["知识库获取"] = test_get_knowledge()
    results["知识库添加"] = test_add_knowledge()
    results["反馈历史"] = test_get_feedback_history()
    results["自我评估"] = test_evaluate()

    # 生成报告
    success = generate_report(results)

    print(f"""
╔═════════════════════════════════════════════════════════════════╗
║  测试完成！访问 {BASE_URL}/api/docs 查看 API 文档              ║
╚═════════════════════════════════════════════════════════════════╝
    """)

    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())