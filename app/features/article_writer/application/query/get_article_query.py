from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GetArticleQuery:
    article_id: str
    user_id: str = ""
