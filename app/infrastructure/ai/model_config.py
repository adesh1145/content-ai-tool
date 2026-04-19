"""
app/infrastructure/ai/model_config.py
─────────────────────────────────────────────────────────────
Per-feature, per-step LLM model configuration.

DESIGN: Each feature defines which provider + model to use for
        EACH STEP of its pipeline. A single feature can use
        multiple different LLMs from different organizations.

        Change models here to switch any step without touching
        the feature's AI service code.

EXAMPLE:
    Blog generation uses:
      - GPT-4o-mini for outline generation (fast, cheap)
      - Claude Sonnet for content writing (better prose)
      - Gemini Flash for SEO metadata (fast, structured output)
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class LLMStep:
    """Defines which provider + model to use for a single pipeline step."""
    provider: str
    model: str


@dataclass(frozen=True)
class FeatureLLMConfig:
    """
    LLM configuration for a feature.
    Each step in the feature's pipeline gets its own provider + model.
    """
    steps: dict[str, LLMStep] = field(default_factory=dict)

    def get_step(self, step_name: str) -> LLMStep:
        """Get the LLM config for a specific step."""
        if step_name not in self.steps:
            raise KeyError(
                f"No LLM config for step '{step_name}'. "
                f"Available steps: {list(self.steps.keys())}"
            )
        return self.steps[step_name]


# ═══════════════════════════════════════════════════════════════════════════════
# FEATURE LLM CONFIGURATIONS
# Change provider + model per step here. No other file needs to change.
# ═══════════════════════════════════════════════════════════════════════════════

# BLOG_GENERATOR_LLM = FeatureLLMConfig(steps={
#     "outline":  LLMStep(provider="openai",    model="gpt-4o-mini"),
#     "writer":   LLMStep(provider="openai",    model="gpt-4o"),
#     "seo":      LLMStep(provider="openai",    model="gpt-4o-mini"),
# })

# TEMPORARY override to use Google provider since only Google API key is available
BLOG_GENERATOR_LLM = FeatureLLMConfig(steps={
    "outline":  LLMStep(provider="google",    model="gemini-2.5-flash"),
    "writer":   LLMStep(provider="google",    model="gemini-2.5-flash"),
    "seo":      LLMStep(provider="google",    model="gemini-2.5-flash"),
})

ARTICLE_WRITER_LLM = FeatureLLMConfig(steps={
    "research": LLMStep(provider="openai",    model="gpt-4o"),
    "outline":  LLMStep(provider="openai",    model="gpt-4o"),
    "draft":    LLMStep(provider="anthropic",  model="claude-sonnet-4-20250514"),
    "review":   LLMStep(provider="anthropic",  model="claude-sonnet-4-20250514"),
    "seo":      LLMStep(provider="openai",    model="gpt-4o-mini"),
})

SOCIAL_MEDIA_LLM = FeatureLLMConfig(steps={
    "generate": LLMStep(provider="openai",    model="gpt-4o-mini"),
})

AD_COPY_LLM = FeatureLLMConfig(steps={
    "generate": LLMStep(provider="openai",    model="gpt-4o-mini"),
})

PRODUCT_DESCRIPTION_LLM = FeatureLLMConfig(steps={
    "generate": LLMStep(provider="openai",    model="gpt-4o-mini"),
})

EMAIL_WRITER_LLM = FeatureLLMConfig(steps={
    "generate": LLMStep(provider="openai",    model="gpt-4o-mini"),
})

SCRIPT_WRITER_LLM = FeatureLLMConfig(steps={
    "generate": LLMStep(provider="openai",    model="gpt-4o"),
})

SEO_OPTIMIZER_LLM = FeatureLLMConfig(steps={
    "analyze":      LLMStep(provider="openai",    model="gpt-4o-mini"),
    "generate_meta": LLMStep(provider="openai",    model="gpt-4o-mini"),
})


# ── Registry of all feature configs ──────────────────────────────────────────

FEATURE_LLM_CONFIGS: dict[str, FeatureLLMConfig] = {
    "blog_generator":       BLOG_GENERATOR_LLM,
    "article_writer":       ARTICLE_WRITER_LLM,
    "social_media":         SOCIAL_MEDIA_LLM,
    "ad_copy":              AD_COPY_LLM,
    "product_description":  PRODUCT_DESCRIPTION_LLM,
    "email_writer":         EMAIL_WRITER_LLM,
    "script_writer":        SCRIPT_WRITER_LLM,
    "seo_optimizer":        SEO_OPTIMIZER_LLM,
}


def get_feature_llm_config(feature_name: str) -> FeatureLLMConfig:
    """Get the full LLM configuration for a feature."""
    if feature_name not in FEATURE_LLM_CONFIGS:
        raise KeyError(
            f"No LLM config for feature '{feature_name}'. "
            f"Available: {list(FEATURE_LLM_CONFIGS.keys())}"
        )
    return FEATURE_LLM_CONFIGS[feature_name]
