from __future__ import annotations

from app.common.exception.base_exception import AppException


class AdGenerationFailed(AppException):
    """Raised when the AI service fails to generate ad copy."""

    def __init__(self, message: str = "Ad copy generation failed.") -> None:
        super().__init__(message=message, code="AD_GENERATION_FAILED", status_code=502)
