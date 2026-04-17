"""
app/features/script_writer/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Script Writer.
POST /content/script — YouTube, Reels, Podcast
"""

from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user_id

from app.core.response import APIResponse
from app.features.script_writer.adapters.schemas import ScriptRequest, ScriptResponse
from app.features.script_writer.adapters.script_gateway import ScriptGateway
from app.features.script_writer.drivers.ai.script_chain import ScriptAIService
from app.features.script_writer.use_cases.generate_script import GenerateScriptInput, GenerateScriptUseCase
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/script", tags=["Script Writer"])

VALID_FORMATS = {"youtube", "reel", "podcast"}


@router.post("", response_model=APIResponse[ScriptResponse], status_code=201)
async def generate_script(
    body: ScriptRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate video/audio scripts:
    - **youtube**: Full script with hook + sections + CTA (with B-Roll cues)
    - **reel**: 15-60s viral short-form script (Instagram Reels / TikTok)
    - **podcast**: Conversational episode script with talking points
    """
    if body.script_format not in VALID_FORMATS:
        raise HTTPException(
            status_code=422,
            detail=f"script_format must be one of: {', '.join(VALID_FORMATS)}"
        )

    try:
        use_case = GenerateScriptUseCase(
            script_repo=ScriptGateway(db),
            ai_service=ScriptAIService()
        )
        
        result = await use_case.execute(GenerateScriptInput(
            user_id=user_id,
            format=body.script_format,
            topic=body.topic,
            tone=body.tone,
            target_audience=body.target_audience,
            language=body.language,
            target_duration=body.duration_seconds,
        ))

        return APIResponse.ok(
            ScriptResponse(
                script_id=result.script_id,
                script_format=body.script_format,
                topic=body.topic,
                script=result.script_text,
                word_count=len(result.script_text.split()),
                estimated_duration_seconds=result.estimated_duration_seconds,
                tokens_used=result.tokens_used,
            ),
            message=f"{body.script_format.title()} script generated successfully.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
