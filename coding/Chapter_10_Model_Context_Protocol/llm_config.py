"""
LLM配置模块
支持多种兼容OpenAI API的服务（OpenAI、Azure OpenAI、国内模型服务商等）
"""
import os
from typing import Optional
from langchain_openai import ChatOpenAI
import httpx

# 禁用代理，避免代理配置问题
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

class LLMConfig:
    """LLM配置类"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        **kwargs
    ):
        """
        初始化LLM配置

        Args:
            api_key: API密钥，默认从环境变量 OPENAI_API_KEY 读取
            api_url: API地址，默认从环境变量 OPENAI_API_BASE 或 OPENAI_API_URL 读取
            model: 模型名称，默认 gpt-3.5-turbo
            temperature: 温度参数，默认 0.7
            **kwargs: 其他传递给ChatOpenAI的参数
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.api_url = api_url or os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_API_URL", "")
        self.model = model
        self.temperature = temperature
        self.extra_kwargs = kwargs

        # 验证配置
        if not self.api_key:
            raise ValueError(
                "API密钥未设置！请设置环境变量 OPENAI_API_KEY 或传递 api_key 参数。\n"
                "例如：export OPENAI_API_KEY='your-api-key'"
            )

    def create_llm(self, **override_params) -> ChatOpenAI:
        """
        创建ChatOpenAI实例

        Args:
            **override_params: 覆盖盖默认配置的参数

        Returns:
            ChatOpenAI实例
        """
        # 创建不使用代理的http_client
        http_client = httpx.Client(timeout=30.0)

        params = {
            "api_key": self.api_key,
            "model": override_params.get("model", self.model),
            "temperature": override_params.get("temperature", self.temperature),
            "http_client": http_client,
            **self.extra_kwargs
        }

        # 如果设置了自定义API URL，添加到参数中
        if self.api_url:
            params["base_url"] = self.api_url

        # 合并其他覆盖参数
        params.update(override_params)

        return ChatOpenAI(**params)


def create_llm(
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    **kwargs
) -> ChatOpenAI:
    """
    快捷创建LLM实例

    Args:
        api_key: API密钥，默认从环境变量读取
        api_url: API地址，默认从环境变量读取
        model: 模型名称，，默认从环境变量 OPENAI_MODEL 读取，否则为 gpt-3.5-turbo
        temperature: 温度参数，默认从环境变量 OPENAI_TEMPERATURE 读取，否则为 0.7
        **kwargs:: 其他参数

    Returns:
        ChatOpenAI实例
    """
    # 如果没有提供参数，从环境变量读取默认值
    final_api_key = api_key or os.getenv("OPENAI_API_KEY")
    final_api_url = api_url or os.getenv("OPENAI_API_URL") or os.getenv("OPENAI_API_BASE")
    final_model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    final_temperature = temperature if temperature is not None else float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

    config = LLMConfig(
        api_key=final_api_key,
        api_url=final_api_url,
        model=final_model,
        temperature=final_temperature,
        **kwargs
    )
    return config.create_llm()
