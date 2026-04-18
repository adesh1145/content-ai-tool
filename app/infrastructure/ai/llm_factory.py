"""
Backward-compatible shim — delegates to the new LLM registry.
"""

from __future__ import annotations

from app.common.port.outbound.llm_port import LLMPort
from app.infrastructure.ai.llm_registry import get_llm_registry


def create_llm_provider(provider: str = "openai", model: str = "gpt-4o-mini") -> LLMPort:
    return get_llm_registry().get(provider, model)


def get_llm_provider(provider: str = "openai", model: str = "gpt-4o-mini") -> LLMPort:
    return get_llm_registry().get(provider, model)


__all__ = ["create_llm_provider", "get_llm_provider"]
