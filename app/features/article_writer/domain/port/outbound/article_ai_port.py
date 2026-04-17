from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ArticleAIResult:
    title: str
    content: str
    meta_title: str = ""
    meta_description: str = ""
    tokens_used: int = 0


class IArticleAIService(ABC):
    @abstractmethod
    async def generate_article(
        self,
        *,
        topic: str,
        tone: str,
        language: str,
        target_audience: str,
        focus_keyword: str,
        word_count: int,
    ) -> ArticleAIResult: ...
