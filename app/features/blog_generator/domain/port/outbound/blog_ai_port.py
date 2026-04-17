from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class BlogAIResult:
    """Output DTO from the AI blog generation pipeline."""

    title: str = ""
    body: str = ""
    outline: list[str] = field(default_factory=list)
    meta_title: str = ""
    meta_description: str = ""
    slug: str = ""
    focus_keyword: str = ""
    secondary_keywords: list[str] = field(default_factory=list)
    word_count: int = 0
    readability_score: float = 0.0
    reading_time_minutes: int = 0
    tokens_used: int = 0


class IBlogAIService(ABC):
    """Output port for AI-powered blog generation."""

    @abstractmethod
    async def generate_blog(
        self,
        *,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        focus_keyword: str,
        secondary_keywords: list[str],
        word_count: int,
    ) -> BlogAIResult: ...
