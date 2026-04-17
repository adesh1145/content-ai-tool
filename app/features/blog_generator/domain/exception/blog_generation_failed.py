from __future__ import annotations

from app.common.exception.base_exception import AppException


class BlogGenerationFailed(AppException):
    """Raised when the blog generation pipeline fails."""

    def __init__(self, message: str = "Blog generation failed") -> None:
        super().__init__(message, code="BLOG_GENERATION_FAILED", status_code=500)
