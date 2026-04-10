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

from app.core.response import APIResponse
from app.features.ad_copy.adapters.schemas import AdCopyRequest, AdCopyResponse, AdVariationResponse
from app.features.ad_copy.drivers.ai.ad_chain import AdCopyAIService
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/ad-copy", tags=["Ad Copy"])


@router.post("", response_model=APIResponse[AdCopyResponse], status_code=201)
async def generate_ad_copy(
    body: AdCopyRequest,
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
        ai = AdCopyAIService()
        variations_raw = await ai.generate(
            platform=body.platform,
            product=body.product_or_service,
            target_audience=body.target_audience,
            usp=body.unique_selling_point,
            tone=body.tone,
            num_variations=body.num_variations,
        )

        variations = [
            AdVariationResponse(
                headline=v.get("headline", ""),
                body=v.get("body", ""),
                cta=v.get("cta", "Learn More"),
            )
            for v in variations_raw
        ]

        return APIResponse.ok(
            AdCopyResponse(
                ad_id=str(uuid.uuid4()),
                platform=body.platform,
                variations=variations,
                tokens_used=sum(len(v.body.split()) * 2 for v in variations),
            ),
            message=f"{body.platform.title()} ad copy generated with {len(variations)} variations.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
