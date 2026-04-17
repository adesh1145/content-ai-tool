"""
app/features/ad_copy/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Ad Copy Generator.
POST /content/ad-copy — supports Google Ads, Facebook Ads
"""

from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user_id

from app.core.response import APIResponse
from app.features.ad_copy.adapters.schemas import AdCopyRequest, AdCopyResponse, AdVariationResponse
from app.features.ad_copy.adapters.ad_gateway import AdGateway
from app.features.ad_copy.drivers.ai.ad_chain import AdCopyAIService
from app.features.ad_copy.use_cases.generate_ad_copy import GenerateAdCopyInput, GenerateAdCopyUseCase
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/ad-copy", tags=["Ad Copy"])


@router.post("", response_model=APIResponse[AdCopyResponse], status_code=201)
async def generate_ad_copy(
    body: AdCopyRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate ad copy for Google Ads or Facebook Ads.

    - **Google Ads**: AIDA framework, headline ≤30 chars, description ≤90 chars
    - **Facebook Ads**: PAS framework, emotionally compelling copy
    - Returns multiple A/B test variations
    """
    if body.platform not in {"google", "facebook"}:
        raise HTTPException(status_code=422, detail="Platform must be 'google' or 'facebook'.")

    try:
        use_case = GenerateAdCopyUseCase(
            ad_repo=AdGateway(db),
            ai_service=AdCopyAIService()
        )
        
        result = await use_case.execute(GenerateAdCopyInput(
            user_id=user_id,
            platform=body.platform,
            product_or_service=body.product_or_service,
            target_audience=body.target_audience,
            unique_selling_point=body.unique_selling_point,
            tone=body.tone,
            num_variations=body.num_variations,
        ))

        variations = [
            AdVariationResponse(
                headline=v.headline,
                body=v.body,
                cta=v.cta,
            )
            for v in result.variations
        ]

        return APIResponse.ok(
            AdCopyResponse(
                ad_id=result.ad_id,
                platform=result.platform,
                variations=variations,
                tokens_used=result.tokens_used,
            ),
            message=f"{body.platform.title()} ad copy generated with {len(variations)} variations.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
