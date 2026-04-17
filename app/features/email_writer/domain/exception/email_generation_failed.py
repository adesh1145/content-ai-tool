from __future__ import annotations

from app.common.exception.base_exception import AppException


class EmailGenerationFailed(AppException):
    """Raised when the AI service fails to generate email content."""

    def __init__(self, message: str = "Email content generation failed.") -> None:
        super().__init__(message=message, code="EMAIL_GENERATION_FAILED", status_code=502)
