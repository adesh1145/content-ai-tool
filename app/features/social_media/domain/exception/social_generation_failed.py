from __future__ import annotations

from app.common.exception.base_exception import AppException


class SocialGenerationFailed(AppException):
    def __init__(self, reason: str = "Social post generation failed"):
        super().__init__(reason, code="SOCIAL_GENERATION_FAILED", status_code=500)
