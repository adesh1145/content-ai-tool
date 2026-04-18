"""
Driven adapter: LangChain SEO AI service for recommendations and meta tag generation.
Uses the LLMs configured in SEO_OPTIMIZER_LLM from model_config.py.
Each use case step can use a different provider/model.
"""

from __future__ import annotations

import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.seo_optimizer.domain.port.outbound.seo_ai_port import (
    ISEOAIPort,
    MetaTagsResult,
    SEORecommendationsResult,
)
from app.infrastructure.ai.llm_registry import get_llm_registry
from app.infrastructure.ai.model_config import SEO_OPTIMIZER_LLM

_RECOMMENDATIONS_SYSTEM = (
    "You are an SEO expert. Analyze the content and provide exactly 5 specific, "
    "actionable SEO improvement tips. Consider on-page SEO, content quality, "
    "keyword optimization, and readability.\n\n"
    "Return a JSON array of 5 strings, each being one recommendation.\n"
    "Return ONLY valid JSON array, no other text."
)

_RECOMMENDATIONS_HUMAN = (
    "Content (first 3000 chars):\n{content}\n\n"
    "Focus keyword: {focus_keyword}\n"
    "Current issues:\n{issues}\n\n"
    "Provide 5 actionable SEO recommendations."
)

_META_SYSTEM = (
    "You are an SEO specialist. Generate optimized meta tags.\n"
    "Requirements:\n"
    "- meta_title: 50-60 characters, include the focus keyword\n"
    "- meta_description: 145-160 characters, compelling and keyword-rich\n"
    "- slug: URL-friendly, lowercase, hyphens, include keyword\n\n"
    'Return only JSON: {{"meta_title": "...", "meta_description": "...", "slug": "..."}}'
)

_META_HUMAN = (
    "Content preview:\n{content}\n\n"
    "Focus keyword: {focus_keyword}\n\n"
    "Generate meta tags."
)


class SEOAIService(ISEOAIPort):
    """Implements ISEOAIPort. Each step uses its own model from model_config.py."""

    def __init__(self) -> None:
        registry = get_llm_registry()

        analyze_step = SEO_OPTIMIZER_LLM.get_step("analyze")
        meta_step = SEO_OPTIMIZER_LLM.get_step("generate_meta")

        self._analyze_llm = registry.get_langchain_llm(analyze_step.provider, analyze_step.model)
        self._meta_llm = registry.get_langchain_llm(meta_step.provider, meta_step.model)

    async def generate_recommendations(
        self,
        *,
        content: str,
        focus_keyword: str,
        current_score: float,
        issues: list[str],
    ) -> SEORecommendationsResult:
        prompt = ChatPromptTemplate.from_messages([
            ("system", _RECOMMENDATIONS_SYSTEM),
            ("human", _RECOMMENDATIONS_HUMAN),
        ])

        chain = prompt | self._analyze_llm | StrOutputParser()
        raw = await chain.ainvoke({
            "content": content,
            "focus_keyword": focus_keyword or "not specified",
            "issues": "\n".join(f"- {i}" for i in issues) if issues else "None identified",
        })

        recommendations = self._parse_recommendations(raw)
        tokens_estimated = len(raw.split()) * 2

        return SEORecommendationsResult(
            recommendations=recommendations,
            tokens_used=tokens_estimated,
        )

    async def generate_meta_tags(
        self,
        *,
        content: str,
        focus_keyword: str,
    ) -> MetaTagsResult:
        prompt = ChatPromptTemplate.from_messages([
            ("system", _META_SYSTEM),
            ("human", _META_HUMAN),
        ])

        chain = prompt | self._meta_llm | StrOutputParser()
        raw = await chain.ainvoke({
            "content": content[:2000],
            "focus_keyword": focus_keyword or "not specified",
        })

        meta_title, meta_description, slug = "", "", ""
        try:
            m = re.search(r"\{.*\}", raw, re.DOTALL)
            if m:
                data = json.loads(m.group())
                meta_title = data.get("meta_title", "")
                meta_description = data.get("meta_description", "")
                slug = data.get("slug", "")
        except (json.JSONDecodeError, AttributeError):
            pass

        tokens_estimated = len(raw.split()) * 2

        return MetaTagsResult(
            meta_title=meta_title,
            meta_description=meta_description,
            slug=slug,
            tokens_used=tokens_estimated,
        )

    @staticmethod
    def _parse_recommendations(raw: str) -> list[str]:
        try:
            json_match = re.search(r"\[.*\]", raw, re.DOTALL)
            if json_match:
                items = json.loads(json_match.group())
                return [str(item) for item in items[:5]]
        except (json.JSONDecodeError, AttributeError):
            pass
        return [line.strip("- ").strip() for line in raw.strip().split("\n") if line.strip()][:5]
