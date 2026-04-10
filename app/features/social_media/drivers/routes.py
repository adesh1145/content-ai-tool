"""
app/features/social_media/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Social Media Post Generator.
POST /content/social — supports LinkedIn, Twitter/X, Instagram
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import APIResponse
from app.features.social_media.adapters.schemas import SocialPostRequest, SocialPostResponse
from app.features.social_media.drivers.ai.social_chain import SocialAIService
from app.infrastructure.db.connection import get_db_session
import uuid

router = APIRouter(prefix="/content/social", tags=["Social Media"])

VALID_PLATFORMS = {"linkedin", "twitter", "instagram"}


@router.post("", response_model=APIResponse[SocialPostResponse], status_code=201)
async def generate_social_post(
    body: SocialPostRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate a social media post for LinkedIn, Twitter/X, or Instagram.

    Enforces platform character limits automatically.
    """
    if body.platform not in VALID_PLATFORMS:
        raise HTTPException(
            status_code=422,
            detail=f"Platform must be one of: {', '.join(VALID_PLATFORMS)}"
        )

    try:
        ai_service = SocialAIService()
        result = await ai_service.generate(
            topic=body.topic,
            platform=body.platform,
            tone=body.tone,
            language=body.language,
            target_audience=body.target_audience,
            include_emoji=body.include_emoji,
        )

        limits = {"linkedin": 3000, "twitter": 280, "instagram": 2200}
        within_limit = result["char_count"] <= limits.get(body.platform, 3000)

        return APIResponse.ok(
            SocialPostResponse(
                post_id=str(uuid.uuid4()),
                platform=body.platform,
                caption=result["caption"],
                hashtags=result["hashtags"],
                char_count=result["char_count"],
                within_limit=within_limit,
                tokens_used=len(result["caption"].split()) * 2,  # estimate
            ),
            message=f"{body.platform.title()} post generated successfully.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
