# integration/llm_factory.py
"""
LLM Factory - Unified interface for multiple LLM providers.

Supports:
- OpenAI (GPT-4o, GPT-4-turbo, GPT-4)
- Anthropic (Claude Sonnet 4, Claude Opus 4)
- Mock responses for testing without API keys

Usage:
    from integration.llm_factory import get_factory, get_llm_response
    
    # Quick usage
    response = get_llm_response("Hello", model="gpt-4o")
    
    # Factory pattern
    factory = get_factory()
    response = factory.query("Hello", model="claude-sonnet-4")
"""

import os
import json
import time
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from enum import Enum


# ========== CONFIGURATION ==========

class ModelProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"


@dataclass
class ModelConfig:
    """Model configuration."""
    provider: ModelProvider
    model_id: str
    max_tokens: int = 2048
    temperature: float = 0.7
    description: str = ""


# Güncel model tanımları (Mayıs 2025)
SUPPORTED_MODELS: Dict[str, ModelConfig] = {
    # OpenAI Models
    "gpt-4o": ModelConfig(
        provider=ModelProvider.OPENAI,
        model_id="gpt-4o",
        max_tokens=4096,
        temperature=0.7,
        description="GPT-4o - Flagship multimodal model"
    ),
    "gpt-4o-mini": ModelConfig(
        provider=ModelProvider.OPENAI,
        model_id="gpt-4o-mini",
        max_tokens=4096,
        temperature=0.7,
        description="GPT-4o Mini - Fast and affordable"
    ),
    "gpt-4-turbo": ModelConfig(
        provider=ModelProvider.OPENAI,
        model_id="gpt-4-turbo",
        max_tokens=4096,
        temperature=0.7,
        description="GPT-4 Turbo - 128k context"
    ),
    "gpt-4": ModelConfig(
        provider=ModelProvider.OPENAI,
        model_id="gpt-4",
        max_tokens=4096,
        temperature=0.7,
        description="GPT-4 - Original"
    ),
    "o1": ModelConfig(
        provider=ModelProvider.OPENAI,
        model_id="o1",
        max_tokens=4096,
        temperature=1.0,  # o1 requires temperature=1
        description="O1 - Reasoning model"
    ),
    "o1-mini": ModelConfig(
        provider=ModelProvider.OPENAI,
        model_id="o1-mini",
        max_tokens=4096,
        temperature=1.0,
        description="O1 Mini - Fast reasoning"
    ),
    
    # Anthropic Models
    "claude-sonnet-4": ModelConfig(
        provider=ModelProvider.ANTHROPIC,
        model_id="claude-sonnet-4-20250514",
        max_tokens=4096,
        temperature=0.7,
        description="Claude Sonnet 4 - Balanced performance"
    ),
    "claude-opus-4": ModelConfig(
        provider=ModelProvider.ANTHROPIC,
        model_id="claude-opus-4-20250514",
        max_tokens=4096,
        temperature=0.7,
        description="Claude Opus 4 - Most capable"
    ),
    "claude-haiku-3.5": ModelConfig(
        provider=ModelProvider.ANTHROPIC,
        model_id="claude-3-5-haiku-20241022",
        max_tokens=4096,
        temperature=0.7,
        description="Claude 3.5 Haiku - Fast and efficient"
    ),
    "claude-sonnet-3.5": ModelConfig(
        provider=ModelProvider.ANTHROPIC,
        model_id="claude-3-5-sonnet-20241022",
        max_tokens=4096,
        temperature=0.7,
        description="Claude 3.5 Sonnet - Previous gen"
    ),
}

# Alias mappings for convenience
MODEL_ALIASES: Dict[str, str] = {
    "gpt": "gpt-4o",
    "gpt4": "gpt-4o",
    "claude": "claude-sonnet-4",
    "claude-4": "claude-sonnet-4",
    "sonnet": "claude-sonnet-4",
    "opus": "claude-opus-4",
    "haiku": "claude-haiku-3.5",
}


# ========== LLM FACTORY ==========

class LLMFactory:
    """
    Unified LLM interface.
    
    Handles:
    - Multiple providers (OpenAI, Anthropic)
    - Automatic retries with exponential backoff
    - Mock responses when API keys missing
    - Model alias resolution
    """
    
    def __init__(
        self,
        openai_key: Optional[str] = None,
        anthropic_key: Optional[str] = None,
        default_model: str = "gpt-4o",
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.openai_key = openai_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_key = anthropic_key or os.getenv("ANTHROPIC_API_KEY")
        self.default_model = default_model
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Lazy-loaded clients
        self._openai_client = None
        self._anthropic_client = None
    
    @property
    def openai_client(self):
        """Lazy load OpenAI client."""
        if self._openai_client is None and self.openai_key:
            try:
                import openai
                self._openai_client = openai.OpenAI(api_key=self.openai_key)
            except ImportError:
                print("⚠️ openai package not installed. Run: pip install openai")
        return self._openai_client
    
    @property
    def anthropic_client(self):
        """Lazy load Anthropic client."""
        if self._anthropic_client is None and self.anthropic_key:
            try:
                import anthropic
                self._anthropic_client = anthropic.Anthropic(api_key=self.anthropic_key)
            except ImportError:
                print("⚠️ anthropic package not installed. Run: pip install anthropic")
        return self._anthropic_client
    
    def resolve_model(self, model: str) -> str:
        """Resolve model alias to canonical name."""
        model_lower = model.lower()
        
        # Check aliases first
        if model_lower in MODEL_ALIASES:
            return MODEL_ALIASES[model_lower]
        
        # Check if it's already a valid model
        if model_lower in SUPPORTED_MODELS:
            return model_lower
        
        # Try partial matching
        for name in SUPPORTED_MODELS:
            if model_lower in name.lower():
                return name
        
        # Default fallback
        return self.default_model
    
    def query(
        self,
        prompt: str,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Query an LLM.
        
        Args:
            prompt: User prompt
            model: Model name or alias
            system_prompt: Optional system prompt
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            **kwargs: Additional provider-specific arguments
        
        Returns:
            Model response text
        """
        model = self.resolve_model(model or self.default_model)
        config = SUPPORTED_MODELS.get(model)
        
        if not config:
            print(f"⚠️ Unknown model '{model}', using mock response")
            return self._mock_response(model)
        
        # Override config with provided values
        temp = temperature if temperature is not None else config.temperature
        tokens = max_tokens if max_tokens is not None else config.max_tokens
        
        # Route to appropriate provider
        if config.provider == ModelProvider.OPENAI:
            return self._query_openai(
                prompt=prompt,
                model_id=config.model_id,
                system_prompt=system_prompt,
                temperature=temp,
                max_tokens=tokens,
                **kwargs
            )
        elif config.provider == ModelProvider.ANTHROPIC:
            return self._query_anthropic(
                prompt=prompt,
                model_id=config.model_id,
                system_prompt=system_prompt,
                temperature=temp,
                max_tokens=tokens,
                **kwargs
            )
        else:
            return self._mock_response(model)
    
    def _query_openai(
        self,
        prompt: str,
        model_id: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """Query OpenAI API."""
        if not self.openai_client:
            print("⚠️ OPENAI_API_KEY not found. Returning mock response.")
            return self._mock_response("openai")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Retry logic
        for attempt in range(self.max_retries):
            try:
                # o1 models don't support system prompts and require temperature=1
                if model_id.startswith("o1"):
                    response = self.openai_client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": prompt}],
                        max_completion_tokens=max_tokens,
                    )
                else:
                    response = self.openai_client.chat.completions.create(
                        model=model_id,
                        messages=messages,
                        temperature=temperature,
                        max_tokens=max_tokens,
                    )
                return response.choices[0].message.content
            
            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"⚠️ OpenAI error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"❌ OpenAI failed after {self.max_retries} attempts: {e}")
                    return self._mock_response("openai", error=str(e))
    
    def _query_anthropic(
        self,
        prompt: str,
        model_id: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        **kwargs
    ) -> str:
        """Query Anthropic API."""
        if not self.anthropic_client:
            print("⚠️ ANTHROPIC_API_KEY not found. Returning mock response.")
            return self._mock_response("anthropic")
        
        # Retry logic
        for attempt in range(self.max_retries):
            try:
                create_kwargs = {
                    "model": model_id,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                if system_prompt:
                    create_kwargs["system"] = system_prompt
                
                response = self.anthropic_client.messages.create(**create_kwargs)
                return response.content[0].text
            
            except Exception as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"⚠️ Anthropic error: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                else:
                    print(f"❌ Anthropic failed after {self.max_retries} attempts: {e}")
                    return self._mock_response("anthropic", error=str(e))
    
    def _mock_response(self, model: str, error: Optional[str] = None) -> str:
        """Generate mock response for testing."""
        if error:
            return json.dumps({
                "score": 0,
                "justification": f"API Error: {error}",
                "suggestion": "Check API key and try again."
            })
        
        return json.dumps({
            "score": 4,
            "justification": f"Mock {model.upper()} response: This prompt shows moderate obfuscation but could be improved.",
            "suggestion": "Consider adding more layers of indirection, using homoglyphs, or embedding the payload in a narrative context."
        })
    
    def list_models(self) -> List[str]:
        """List all supported models."""
        return list(SUPPORTED_MODELS.keys())
    
    def get_model_info(self, model: str) -> Optional[ModelConfig]:
        """Get model configuration."""
        resolved = self.resolve_model(model)
        return SUPPORTED_MODELS.get(resolved)
    
    def is_available(self, model: str) -> bool:
        """Check if model is available (API key present)."""
        resolved = self.resolve_model(model)
        config = SUPPORTED_MODELS.get(resolved)
        
        if not config:
            return False
        
        if config.provider == ModelProvider.OPENAI:
            return bool(self.openai_key)
        elif config.provider == ModelProvider.ANTHROPIC:
            return bool(self.anthropic_key)
        
        return True  # Mock is always available


# ========== SINGLETON & CONVENIENCE FUNCTIONS ==========

_factory_instance: Optional[LLMFactory] = None


def get_factory(**kwargs) -> LLMFactory:
    """
    Get or create singleton factory instance.
    
    Args:
        **kwargs: Arguments passed to LLMFactory constructor
    
    Returns:
        LLMFactory instance
    """
    global _factory_instance
    
    if _factory_instance is None or kwargs:
        _factory_instance = LLMFactory(**kwargs)
    
    return _factory_instance


def reset_factory() -> None:
    """Reset factory singleton."""
    global _factory_instance
    _factory_instance = None


def get_llm_response(
    prompt: str,
    model: str = "gpt-4o",
    **kwargs
) -> str:
    """
    Quick function to get LLM response.
    
    Args:
        prompt: User prompt
        model: Model name or alias
        **kwargs: Additional arguments
    
    Returns:
        Model response text
    """
    factory = get_factory()
    return factory.query(prompt, model=model, **kwargs)


# ========== LEGACY COMPATIBILITY ==========

def gpt_respond(prompt: str, model: str = "gpt-4o") -> str:
    """Legacy function - use get_llm_response instead."""
    return get_llm_response(prompt, model=model)


def claude_respond(prompt: str, model: str = "claude-sonnet-4") -> str:
    """Legacy function - use get_llm_response instead."""
    return get_llm_response(prompt, model=model)


def mock_response(model_name: str) -> str:
    """Legacy function for mock responses."""
    return get_factory()._mock_response(model_name)


# ========== MODULE INFO ==========

__all__ = [
    "LLMFactory",
    "get_factory",
    "reset_factory",
    "get_llm_response",
    "ModelConfig",
    "ModelProvider",
    "SUPPORTED_MODELS",
    "MODEL_ALIASES",
    # Legacy
    "gpt_respond",
    "claude_respond",
    "mock_response",
]