# integration/llm_factory.py

from integration.openai_adapter import OpenAIAdapter
from integration.anthropic_adapter import AnthropicAdapter

def get_llm_adapter(model_name: str):
    model_name = model_name.lower()

    if "gpt" in model_name:
        return OpenAIAdapter()

    if "claude" in model_name:
        return AnthropicAdapter()

    # gerekirse diğerlerini ekle
    raise ValueError(f"Unsupported LLM: {model_name}")
