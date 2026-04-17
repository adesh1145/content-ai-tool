from __future__ import annotations

import logging

from app.common.config.settings import get_settings
from app.common.port.outbound.llm_port import LLMPort

logger = logging.getLogger(__name__)


class LLMRegistry:
    """Registry of all available LLM providers with lazy instantiation."""

    def __init__(self) -> None:
        self._providers: dict[str, LLMPort] = {}

    def get_provider(
        self,
        provider_name: str | None = None,
        model: str | None = None,
    ) -> LLMPort:
        settings = get_settings()
        provider_name = provider_name or settings.LLM_PROVIDER
        cache_key = f"{provider_name}:{model or 'default'}"

        if cache_key not in self._providers:
            self._providers[cache_key] = self._create_provider(provider_name, model)
            logger.info(f"LLM provider instantiated: {cache_key}")

        return self._providers[cache_key]

    def _create_provider(self, provider_name: str, model: str | None) -> LLMPort:
        if provider_name == "openai":
            from app.infrastructure.ai.providers.openai_provider import OpenAIProvider
            return OpenAIProvider(model=model)
        elif provider_name == "anthropic":
            from app.infrastructure.ai.providers.anthropic_provider import AnthropicProvider
            return AnthropicProvider(model=model)
        elif provider_name == "google":
            from app.infrastructure.ai.providers.google_provider import GoogleProvider
            return GoogleProvider(model=model)
        elif provider_name == "huggingface":
            from app.infrastructure.ai.providers.huggingface_provider import HuggingFaceProvider
            return HuggingFaceProvider(model=model)
        elif provider_name == "ollama":
            from app.infrastructure.ai.providers.ollama_provider import OllamaProvider
            return OllamaProvider(model=model)
        else:
            raise ValueError(
                f"Unknown LLM provider: '{provider_name}'. "
                f"Available: openai, anthropic, google, huggingface, ollama"
            )

    @property
    def available_providers(self) -> list[str]:
        return ["openai", "anthropic", "google", "huggingface", "ollama"]


_registry: LLMRegistry | None = None


def get_llm_registry() -> LLMRegistry:
    global _registry
    if _registry is None:
        _registry = LLMRegistry()
    return _registry
