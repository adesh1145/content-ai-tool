"""Maps SocialResult (application) → SocialPostResponse (presentation)."""

from __future__ import annotations

from app.features.social_media.application.result.social_result import SocialResult
from app.features.social_media.presentation.rest.dto.response import SocialPostResponse


class SocialRestMapper:
    @staticmethod
    def to_response(result: SocialResult) -> SocialPostResponse:
        return SocialPostResponse(
            post_id=result.post_id,
            platform=result.platform,
            content=result.content,
            hashtags=result.hashtags,
            tokens_used=result.tokens_used,
            status=result.status,
        )
