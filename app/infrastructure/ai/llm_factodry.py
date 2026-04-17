"""Typo-compat shim — redirects to llm_factory.py."""

from app.infrastructure.ai.llm_factory import get_llm_provider, create_llm_provider

__all__ = ["get_llm_provider", "create_llm_provider"]
