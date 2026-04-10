"""
app/infrastructure/ai/llm_factory.py
─────────────────────────────────────────────────────────────
Concrete LLM provider implementations + factory.

Implements ILLMProvider interface for:
  - OpenAI (primary)
  - Anthropic / Claude (optional)

Factory reads LLM_PROVIDER from config and returns the right impl.
Use cases never import this directly — injected via DI.
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage

from app.config import get_settings
from app.core.interfaces.llm_provider import ILLMProvider, LLMResponse
from app.core.utils.logger import logger

settings = get_settings()


class OpenAIProvider(ILLMProvider):
    """OpenAI LLM provider via LangChain."""

    def __init__(self) -> None:
        self._llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY,
        )

    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        llm = self._llm.with_config(
            configurable={"temperature": temperature, "max_tokens": max_tokens}
        )

        logger.debug(f"[OpenAI] Calling {settings.OPENAI_MODEL}, prompt_len={len(prompt)}")
        response = await llm.ainvoke(messages)

        usage = response.usage_metadata or {}
        return LLMResponse(
            content=str(response.content),
            model=settings.OPENAI_MODEL,
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
        )

    def get_model_name(self) -> str:
        return settings.OPENAI_MODEL

    def get_langchain_llm(self) -> ChatOpenAI:
        """Expose raw LangChain LLM for chain building."""
        return self._llm


class AnthropicProvider(ILLMProvider):
    """Anthropic / Claude LLM provider via LangChain."""

    def __init__(self) -> None:
        self._llm = ChatAnthropic(
            model=settings.ANTHROPIC_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.ANTHROPIC_API_KEY,
        )

    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        system_prompt: str | None = None,
    ) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        logger.debug(f"[Anthropic] Calling {settings.ANTHROPIC_MODEL}, prompt_len={len(prompt)}")
        response = await self._llm.ainvoke(messages)

        usage = response.usage_metadata or {}
        return LLMResponse(
            content=str(response.content),
            model=settings.ANTHROPIC_MODEL,
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
        )

    def get_model_name(self) -> str:
        return settings.ANTHROPIC_MODEL

    def get_langchain_llm(self) -> ChatAnthropic:
        return self._llm


def create_llm_provider() -> ILLMProvider:
    """
    Factory function — returns the configured LLM provider.
    Change LLM_PROVIDER in .env to switch providers.
    """
    provider = settings.LLM_PROVIDER
    if provider == "openai":
        return OpenAIProvider()
    elif provider == "anthropic":
        return AnthropicProvider()
    else:
        raise ValueError(f"Unknown LLM provider: '{provider}'. Use 'openai' or 'anthropic'.")


# ── Singleton ──────────────────────────────────────────────────────────────────
# Instantiated once at startup via app/dependencies.py
_llm_provider_instance: ILLMProvider | None = None


def get_llm_provider() -> ILLMProvider:
    """Return shared LLM provider singleton."""
    global _llm_provider_instance
    if _llm_provider_instance is None:
        _llm_provider_instance = create_llm_provider()
    return _llm_provider_instance
