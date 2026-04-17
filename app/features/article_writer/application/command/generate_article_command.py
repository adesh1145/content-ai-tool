from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenerateArticleCommand:
    user_id: str
    topic: str
    tone: str = "professional"
    language: str = "en"
    target_audience: str = "general"
    focus_keyword: str = ""
    word_count_target: int = 1500
