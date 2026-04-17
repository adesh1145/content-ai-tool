from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.common.exception.base_exception import AppException
from app.dependencies import get_current_user_id
from app.features.social_media.adapter.inbound.web.dto.request import (
    GenerateSocialPostRequest,
)
from app.features.social_media.adapter.inbound.web.dto.response import (
    SocialPostResponse,
)
from app.features.social_media.application.command.generate_social_command import (
    GenerateSocialCommand,
)
from app.features.social_media.config.container import (
    get_generate_social_service,
)
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/social", tags=["Social Media"])


@router.post(
    "",
    response_model=ApiResponse[SocialPostResponse],
    status_code=201,
)
async def generate_social_post(
    body: GenerateSocialPostRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = get_generate_social_service(db)
        result = await service.execute(
            GenerateSocialCommand(
                user_id=user_id,
                platform=body.platform,
                topic=body.topic,
                tone=body.tone,
                language=body.language,
                target_audience=body.target_audience,
            )
        )
        return ApiResponse.ok(
            SocialPostResponse(
                post_id=result.post_id,
                platform=result.platform,
                content=result.content,
                hashtags=result.hashtags,
                tokens_used=result.tokens_used,
                status=result.status,
            ),
            message=f"{body.platform.title()} post generated successfully.",
        )
    except AppException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
