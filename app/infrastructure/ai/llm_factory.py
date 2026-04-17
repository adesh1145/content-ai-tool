"""
Backward-compatible shim — delegates to the new LLM registry.
"""

from __future__ import annotations

from app.common.port.outbound.llm_port import LLMPort
from app.infrastructure.ai.llm_registry import get_llm_registry


def create_llm_provider() -> LLMPort:
    return get_llm_registry().get_provider()


def get_llm_provider() -> LLMPort:
    return get_llm_registry().get_provider()


__all__ = ["create_llm_provider", "get_llm_provider"]
