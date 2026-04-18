from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.common.exception.base_exception import AppException, ValidationException
from app.dependencies import get_current_user_id
from app.features.script_writer.presentation.rest.dto.request import ScriptGenerateRequest
from app.features.script_writer.presentation.rest.dto.response import ScriptGenerateResponse
from app.features.script_writer.application.command.generate_script_command import (
    GenerateScriptCommand,
)
from app.features.script_writer.config.container import get_generate_script_usecase
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/script", tags=["Script Writer"])

_VALID_FORMATS = {"youtube", "reel", "podcast"}


@router.post("", response_model=ApiResponse[ScriptGenerateResponse], status_code=201)
async def generate_script(
    body: ScriptGenerateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate a script for YouTube, Reel, or Podcast.

    - **YouTube**: Hook (0-30s) + Intro + Main Content (3-5 sections with timestamps) + CTA
    - **Reel**: 15-60s, HOOK -> VALUE -> CTA. Punchy, pattern interrupts
    - **Podcast**: INTRO + TOPIC SEGMENTS (bullet-style talking points) + KEY INSIGHTS + OUTRO
    """
    if body.script_format not in _VALID_FORMATS:
        raise HTTPException(
            status_code=422,
            detail=f"Format must be one of: {', '.join(sorted(_VALID_FORMATS))}.",
        )

    try:
        use_case = get_generate_script_usecase(db)
        result = await use_case.execute(
            GenerateScriptCommand(
                user_id=user_id,
                script_format=body.script_format,
                topic=body.topic,
                tone=body.tone,
                language=body.language,
                target_audience=body.target_audience,
                duration_seconds=body.duration_seconds,
            )
        )

        response = ScriptGenerateResponse(
            script_id=result.script_id,
            script_format=result.script_format,
            topic=result.topic,
            script_text=result.script_text,
            word_count=result.word_count,
            estimated_duration_seconds=result.estimated_duration_seconds,
            tokens_used=result.tokens_used,
        )

        return ApiResponse.ok(
            response,
            message=f"{body.script_format.title()} script generated successfully.",
        )
    except ValidationException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
