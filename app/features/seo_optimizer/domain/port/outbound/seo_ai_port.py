from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class SEORecommendationsResult:
    """Result from AI-generated SEO recommendations."""

    recommendations: list[str] = field(default_factory=list)
    tokens_used: int = 0


@dataclass
class MetaTagsResult:
    """Result from AI-generated meta tags."""

    meta_title: str = ""
    meta_description: str = ""
    slug: str = ""
    tokens_used: int = 0


class ISEOAIPort(ABC):
    """Output port: AI service for SEO recommendations and meta tag generation."""

    @abstractmethod
    async def generate_recommendations(
        self,
        *,
        content: str,
        focus_keyword: str,
        current_score: float,
        issues: list[str],
    ) -> SEORecommendationsResult: ...

    @abstractmethod
    async def generate_meta_tags(
        self,
        *,
        content: str,
        focus_keyword: str,
    ) -> MetaTagsResult: ...
