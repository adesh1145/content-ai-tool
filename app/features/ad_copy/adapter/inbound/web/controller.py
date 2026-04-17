from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.common.exception.base_exception import AppException
from app.dependencies import get_current_user_id
from app.features.ad_copy.adapter.inbound.web.dto.request import GenerateAdRequest
from app.features.ad_copy.adapter.inbound.web.dto.response import GenerateAdResponse
from app.features.ad_copy.application.command.generate_ad_command import GenerateAdCommand
from app.features.ad_copy.config.container import get_generate_ad_service
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/ad-copy", tags=["Ad Copy"])


@router.post("", response_model=ApiResponse[GenerateAdResponse], status_code=201)
async def generate_ad_copy(
    body: GenerateAdRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate ad copy for Google Ads or Facebook Ads.

    - **Google Ads**: AIDA framework, headline <=30 chars, description <=90 chars
    - **Facebook Ads**: PAS framework, emotionally compelling copy
    - Returns multiple A/B test variations
    """
    service = get_generate_ad_service(db)
    result = await service.execute(
        GenerateAdCommand(
            user_id=user_id,
            platform=body.platform,
            product_name=body.product_name,
            product_description=body.product_description,
            target_audience=body.target_audience,
            tone=body.tone,
            language=body.language,
            num_variations=body.num_variations,
        )
    )

    response = GenerateAdResponse(
        ad_id=result.ad_id,
        platform=result.platform,
        headline=result.headline,
        primary_text=result.primary_text,
        cta_text=result.cta_text,
        variations=result.variations,
        tokens_used=result.tokens_used,
    )

    return ApiResponse.ok(
        response,
        message=f"{body.platform.title()} ad copy generated with {len(result.variations)} variations.",
    )
