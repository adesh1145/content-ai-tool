"""Maps ArticleResult (application) → ArticleResponse (presentation)."""

from __future__ import annotations

from app.features.article_writer.application.result.article_result import ArticleResult
from app.features.article_writer.presentation.rest.dto.response import ArticleResponse


class ArticleRestMapper:
    @staticmethod
    def to_response(result: ArticleResult) -> ArticleResponse:
        return ArticleResponse(
            article_id=result.article_id,
            topic=result.topic,
            title=result.title,
            content=result.content,
            meta_title=result.meta_title,
            meta_description=result.meta_description,
            word_count=result.word_count,
            tokens_used=result.tokens_used,
            status=result.status,
        )
