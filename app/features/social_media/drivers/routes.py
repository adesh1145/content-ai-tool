"""
app/features/social_media/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Social Media Post Generator.
POST /content/social — supports LinkedIn, Twitter/X, Instagram
"""

from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user_id

from app.core.response import APIResponse
from app.features.social_media.adapters.schemas import SocialPostRequest, SocialPostResponse
from app.features.social_media.adapters.social_gateway import SocialGateway
from app.features.social_media.drivers.ai.social_chain import SocialAIService
from app.features.social_media.use_cases.generate_social_post import GenerateSocialPostInput, GenerateSocialPostUseCase
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/social", tags=["Social Media"])

VALID_PLATFORMS = {"linkedin", "twitter", "instagram"}


@router.post("", response_model=APIResponse[SocialPostResponse], status_code=201)
async def generate_social_post(
    body: SocialPostRequest,
    user_id: str = Depends(get_current_user_id),
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
        use_case = GenerateSocialPostUseCase(
            social_repo=SocialGateway(db),
            ai_service=SocialAIService()
        )
        
        result = await use_case.execute(GenerateSocialPostInput(
            user_id=user_id,
            topic=body.topic,
            platform=body.platform,
            tone=body.tone,
            language=body.language,
            target_audience=body.target_audience,
            include_emoji=body.include_emoji,
        ))

        return APIResponse.ok(
            SocialPostResponse(
                post_id=result.post_id,
                platform=result.platform,
                caption=result.caption,
                hashtags=result.hashtags,
                char_count=result.char_count,
                within_limit=result.within_limit,
                tokens_used=result.tokens_used,
            ),
            message=f"{body.platform.title()} post generated successfully.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
