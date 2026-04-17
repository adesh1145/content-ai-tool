from __future__ import annotations

from app.common.exception.base_exception import AppException


class SEOAnalysisFailed(AppException):
    """Raised when the SEO analysis or AI service fails."""

    def __init__(self, message: str = "SEO analysis failed.") -> None:
        super().__init__(message=message, code="SEO_ANALYSIS_FAILED", status_code=500)
