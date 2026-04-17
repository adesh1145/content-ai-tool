from __future__ import annotations

from app.common.exception.base_exception import AppException


class ScriptGenerationFailed(AppException):
    """Raised when the AI service fails to generate a script."""

    def __init__(self, message: str = "Script generation failed.") -> None:
        super().__init__(message=message, code="SCRIPT_GENERATION_FAILED", status_code=500)
