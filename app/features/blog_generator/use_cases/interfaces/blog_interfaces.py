"""
app/features/blog_generator/use_cases/interfaces/blog_ai.py
and
app/features/blog_generator/use_cases/interfaces/blog_repo.py
─────────────────────────────────────────────────────────────
Abstract interfaces for blog_generator feature.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass

from app.core.interfaces.base_repository import IRepository
from app.features.blog_generator.entities.blog_content import BlogContent, SEOMetadata


class IBlogRepository(IRepository[BlogContent]):
    """Blog-specific repository contract."""

    @abstractmethod
    async def list_by_user(self, user_id: str, limit: int = 20, offset: int = 0) -> list[BlogContent]: ...


@dataclass
class BlogGenerationRequest:
    topic: str
    tone: str
    language: str
    target_audience: str
    focus_keyword: str
    secondary_keywords: list[str]
    word_count: int = 800


@dataclass
class BlogGenerationResult:
    title: str
    outline: list[str]
    body: str
    seo: SEOMetadata
    tokens_used: int


class IBlogAIService:
    """Abstract AI service for blog generation."""

    @abstractmethod
    async def generate(self, request: BlogGenerationRequest) -> BlogGenerationResult: ...
