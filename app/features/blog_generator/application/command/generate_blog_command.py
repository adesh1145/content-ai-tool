from __future__ import annotations

from app.common.application.base_command import BaseCommand


class GenerateBlogCommand(BaseCommand):
    """CQRS command to generate a new blog post."""

    user_id: str
    topic: str
    tone: str = "professional"
    language: str = "en"
    target_audience: str = "general"
    focus_keyword: str = ""
    secondary_keywords: list[str] = []
    word_count: int = 800
    project_id: str | None = None
