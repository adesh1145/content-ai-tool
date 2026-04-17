from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ArticleResult:
    article_id: str
    topic: str
    title: str
    content: str
    meta_title: str = ""
    meta_description: str = ""
    word_count: int = 0
    tokens_used: int = 0
    status: str = "pending"
