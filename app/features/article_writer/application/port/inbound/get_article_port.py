from __future__ import annotations

from abc import ABC, abstractmethod

from app.features.article_writer.application.query.get_article_query import (
    GetArticleQuery,
)
from app.features.article_writer.application.result.article_result import (
    ArticleResult,
)


class IGetArticlePort(ABC):
    @abstractmethod
    async def execute(self, query: GetArticleQuery) -> ArticleResult: ...
