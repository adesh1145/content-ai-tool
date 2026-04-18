"""
app/infrastructure/ai/llm_registry.py
─────────────────────────────────────────────────────────────
LLM Registry — central hub for obtaining ANY LLM provider + model.

DESIGN PHILOSOPHY:
  - No default models. Every caller MUST specify provider + model.
  - A single feature can request MULTIPLE different providers/models.
  - Providers are cached by (provider, model) tuple for efficiency.
  - API keys come from .env; model selection comes from the feature code.

USAGE IN FEATURE AI SERVICES:
    registry = get_llm_registry()

    # Blog feature uses GPT-4o for outline, Claude for writing
    outline_llm = registry.get("openai", "gpt-4o-mini")
    writer_llm  = registry.get("anthropic", "claude-sonnet-4-20250514")
    seo_llm     = registry.get("google", "gemini-2.0-flash")
"""

from __future__ import annotations

import logging
from typing import Any

from app.common.config.settings import get_settings
from app.common.port.outbound.llm_port import LLMPort

logger = logging.getLogger(__name__)


class LLMRegistry:
    """
    Registry of all available LLM providers with lazy instantiation.

    Key design:
      - Every call MUST specify both provider and model.
      - Instances are cached by (provider:model) key.
      - A feature can use multiple providers in the same pipeline.
    """

    def __init__(self) -> None:
        self._providers: dict[str, LLMPort] = {}

    def get(self, provider: str, model: str) -> LLMPort:
        """
        Get or create an LLM provider instance for the given provider + model.

        Args:
            provider: One of 'openai', 'anthropic', 'google', 'huggingface', 'ollama'
            model: The specific model name (e.g. 'gpt-4o', 'claude-sonnet-4-20250514', 'gemini-2.0-flash')

        Returns:
            LLMPort implementation ready to use.

        Example:
            llm = registry.get("openai", "gpt-4o-mini")
            result = await llm.generate("Write a poem")
        """
        cache_key = f"{provider}:{model}"

        if cache_key not in self._providers:
            self._providers[cache_key] = self._create_provider(provider, model)
            logger.info("LLM provider instantiated: %s", cache_key)

        return self._providers[cache_key]

    def get_langchain_llm(self, provider: str, model: str) -> Any:
        """
        Shortcut to get the underlying LangChain chat model directly.

        Used by feature AI services that build LangChain chains/graphs.

        Example:
            llm = registry.get_langchain_llm("openai", "gpt-4o")
            chain = prompt | llm | StrOutputParser()
        """
        return self.get(provider, model).get_langchain_llm()

    # Legacy compatibility — delegates to get()
    def get_provider(
        self,
        provider_name: str | None = None,
        model: str | None = None,
    ) -> LLMPort:
        """Backward-compatible method. Prefer get(provider, model) instead."""
        return self.get(
            provider=provider_name or "openai",
            model=model or "gpt-4o-mini",
        )

    def _create_provider(self, provider_name: str, model: str) -> LLMPort:
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
                f"Available: {', '.join(self.available_providers)}"
            )

    @property
    def available_providers(self) -> list[str]:
        return ["openai", "anthropic", "google", "huggingface", "ollama"]


# ── Singleton ──────────────────────────────────────────────────────────────────
_registry: LLMRegistry | None = None


def get_llm_registry() -> LLMRegistry:
    global _registry
    if _registry is None:
        _registry = LLMRegistry()
    return _registry
