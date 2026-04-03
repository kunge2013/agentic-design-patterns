"""
测试用 LLM 配置 - 用于 Swagger 测试，不需要真实的 API 密钥
"""
from typing import Optional
from langchain_openai import ChatOpenAI

class MockLLMConfig:
    """测试用 LLM 配置类"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        **kwargs
    ):
        """
        初始化测试 LLM 配置
        """
        # 使用测试密钥
        self.api_key = api_key or "test-api-key"
        self.api_url = api_url or "https://api.openai.com/v1"
        self.model = model
        self.temperature = temperature
        self.extra_kwargs = kwargs

    def create_llm(self, **override_params) -> ChatOpenAI:
        """
        创建 ChatOpenAI 实例（测试模式）
        """
        params = {
            "api_key": self.api_key,
            "base_url": self.api_url,
            "model": self.model,
            "temperature": self.temperature,
            **self.extra_kwargs,
            **override_params
        }

        # 添加超时和重试配置
        params.update({
            "timeout": 10.0,
            "max_retries": 2
        })

        return ChatOpenAI(**params)

def create_llm(
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    **kwargs
) -> ChatOpenAI:
    """
    创建 LLM 实例（测试模式）

    Args:
        api_key: API密钥（可选）
        api_url: API地址（可选）
        model: 模型名称
        temperature: 温度参数
        **kwargs: 其他参数

    Returns:
        ChatOpenAI: LangChain LLM 实例
    """
    config = MockLLMConfig(
        api_key=api_key,
        api_url=api_url,
        model=model,
        temperature=temperature,
        **kwargs
    )
    return config.create_llm()

if __name__ == "__main__":
    # 测试配置
    llm = create_llm()
    print(f"✅ 测试 LLM 配置成功")
    print(f"模型: {llm.model}")
    print(f"温度: {llm.temperature}")