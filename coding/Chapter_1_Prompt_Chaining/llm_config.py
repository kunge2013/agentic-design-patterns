"""
API配置模块
支持多种兼容OpenAI API的服务（OpenAI、Azure OpenAI、国内模型服务商等）
"""
import os
from typing import Optional
from langchain_openai import ChatOpenAI

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
            **override_params: 覆盖默认配置的参数

        Returns:
            ChatOpenAI实例
        """
        params = {
            "api_key": self.api_key,
            "model": override_params.get("model", self.model),
            "temperature": override_params.get("temperature", self.temperature),
            **self.extra_kwargs
        }

        # 如果设置了自定义API URL，添加到参数中
        if self.api_url:
            params["base_url"] = self.api_url

        # 合并其他覆盖参数
        params.update(override_params)

        return ChatOpenAI(**params)

    def print_config(self):
        """打印当前配置（隐藏敏感信息）"""
        masked_key = self.api_key[:8] + "..." if len(self.api_key) > 8 else "***"
        print(f"LLM配置:")
        print(f"  API Key: {masked_key}")
        print(f"  API URL: {self.api_url or '默认（OpenAI）'}")
        print(f"  Model: {self.model}")
        print(f"  Temperature: {self.temperature}")


# 预设配置
class LLMConfigs:
    """预设配置类"""

    # OpenAI官方配置
    OPENAI = LLMConfig(
        model="gpt-3.5-turbo",
        temperature=0.7
    )

    # OpenAI GPT-4
    OPENAI_GPT4 = LLMConfig(
        model="gpt-4",
        temperature=0.7
    )

    # 智谱AI（GLM-4）示例配置
    ZHIPU_AI = LLMConfig(
        model="glm-4",
        temperature=0.7,
        api_url="https://open.bigmodel.cn/api/paas/v4/"
    )

    # 阿里云通义千问示例配置
    QWEN = LLMConfig(
        model="qwen-turbo",
        temperature=0.7,
        api_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    # 百度文心一言示例配置
    ERNIE = LLMConfig(
        model="ERNIE-Bot-4",
        temperature=0.7,
        api_url="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat"
    )

    # 月之暗面 Kimi 示例配置
    KIMI = LLMConfig(
        model="moonshot-v1-8k",
        temperature=0.7,
        api_url="https://api.moonshot.cn/v1"
    )


def get_default_llm_config() -> "LLMConfig":
    """
    获取默认LLM配置

    优先级：
    1. 环境变量 OPENAI_API_KEY + OPENAI_API_URL/OPENAI_API_BASE
    2. OPENAI默认配置

    Returns:
        LLMConfig实例
    """
    api_key = os.getenv("OPENAI_API_KEY")
    api_url = os.getenv("OPENAI_API_URL") or os.getenv("OPENAI_API_BASE")

    if api_key:
        return LLMConfig(
            api_key=api_key,
            api_url=api_url,
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        )
    else:
        raise ValueError(
            "未找到API配置！请设置以下环境变量之一：\n"
            "1. OPENAI_API_KEY（使用OpenAI）\n"
            "2. OPENAI_API_KEY + OPENAI_API_URL（使用自定义API）\n\n"
            "示例：\n"
            "export OPENAI_API_KEY='your-api-key'\n"
            "export OPENAI_API_URL='https://your-api-endpoint'"
        )


# 快捷函数
def create_llm(
    api_key: Optional[str] = None,
    api_url: Optional[str] = None,
    model: str = "gpt-3.5-turbo",
    temperature: float = 0.7,
    **kwargs
) -> ChatOpenAI:
    """
    快捷创建LLM实例

    Args:
        api_key: API密钥，默认从环境变量读取
        api_url: API地址，默认从环境变量读取
        model: 模型名称
        temperature: 温度参数
        **kwargs: 其他参数

    Returns:
        ChatOpenAI实例
    """
    config = LLMConfig(api_key=api_key, api_url=api_url, model=model, temperature=temperature, **kwargs)
    return config.create_llm()


if __name__ == "__main__":
    # 测试配置模块
    print("=== LLM配置模块测试 ===\n")

    # 测试默认配置
    try:
        config = get_default_llm_config()
        config.print_config()
    except ValueError as e:
        print(f"配置错误: {e}")

    print("\n=== 预设配置示例 ===\n")

    # 打印预设配置（不实际创建LLM）
    LLMConfigs.OPENAI.print_config()
    print()
    LLMConfigs.ZHIPU_AI.print_config()
    print()
    LLMConfigs.QWEN.print_config()
