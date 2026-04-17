from __future__ import annotations

from app.common.exception.base_exception import NotFoundException
from app.common.port.inbound.use_case import UseCase
from app.features.article_writer.application.query.get_article_query import (
    GetArticleQuery,
)
from app.features.article_writer.application.result.article_result import (
    ArticleResult,
)
from app.features.article_writer.domain.port.outbound.article_repository_port import (
    IArticleRepository,
)


class GetArticleService(UseCase[GetArticleQuery, ArticleResult]):

    def __init__(self, article_repo: IArticleRepository) -> None:
        self._repo = article_repo

    async def execute(self, query: GetArticleQuery) -> ArticleResult:
        article = await self._repo.find_by_id(query.article_id)
        if article is None:
            raise NotFoundException("Article", query.article_id)

        word_count = len(article.content.split()) if article.content else 0
        return ArticleResult(
            article_id=article.id,
            topic=article.topic,
            title=article.title,
            content=article.content,
            word_count=word_count,
            tokens_used=article.tokens_used,
            status=article.status.value,
        )
