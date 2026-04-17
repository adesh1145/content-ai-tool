from __future__ import annotations

from app.common.exception.base_exception import AppException


class ArticleGenerationFailed(AppException):
    def __init__(self, reason: str = "Article generation failed"):
        super().__init__(reason, code="ARTICLE_GENERATION_FAILED", status_code=500)
