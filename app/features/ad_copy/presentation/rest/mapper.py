"""Maps AdResult (application) → GenerateAdResponse (presentation)."""

from __future__ import annotations

from app.features.ad_copy.application.result.ad_result import AdResult
from app.features.ad_copy.presentation.rest.dto.response import GenerateAdResponse


class AdRestMapper:
    @staticmethod
    def to_response(result: AdResult) -> GenerateAdResponse:
        return GenerateAdResponse(
            ad_id=result.ad_id,
            platform=result.platform,
            headline=result.headline,
            primary_text=result.primary_text,
            cta_text=result.cta_text,
            variations=result.variations,
            tokens_used=result.tokens_used,
        )
