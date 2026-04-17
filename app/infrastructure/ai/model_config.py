"""Per-feature LLM model recommendations."""

from __future__ import annotations

FEATURE_LLM_MAP: dict[str, dict[str, str]] = {
    "blog_generator": {"provider": "openai", "model": "gpt-4o"},
    "article_writer": {"provider": "anthropic", "model": "claude-3-5-sonnet"},
    "social_media": {"provider": "openai", "model": "gpt-4o-mini"},
    "ad_copy": {"provider": "openai", "model": "gpt-4o-mini"},
    "product_description": {"provider": "openai", "model": "gpt-4o-mini"},
    "email_writer": {"provider": "anthropic", "model": "claude-3-5-sonnet"},
    "script_writer": {"provider": "openai", "model": "gpt-4o"},
    "seo_optimizer": {"provider": "google", "model": "gemini-2.0-flash"},
}


def get_feature_llm_config(feature_name: str) -> dict[str, str] | None:
    return FEATURE_LLM_MAP.get(feature_name)
