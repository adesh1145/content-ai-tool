from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.dependencies import get_current_user_id
from app.features.email_writer.presentation.rest.dto.request import GenerateEmailRequest
from app.features.email_writer.presentation.rest.dto.response import GenerateEmailResponse
from app.features.email_writer.application.command.generate_email_command import GenerateEmailCommand
from app.features.email_writer.config.container import get_generate_email_service
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/email", tags=["Email Writer"])


@router.post("", response_model=ApiResponse[GenerateEmailResponse], status_code=201)
async def generate_email(
    body: GenerateEmailRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate email content with type-specific prompts.

    - **cold_email**: Concise with clear CTA
    - **newsletter**: Informative and engaging
    - **followup**: References previous interaction, gentle nudge
    - **welcome**: Warm, onboarding-focused
    """
    service = get_generate_email_service(db)
    result = await service.execute(
        GenerateEmailCommand(
            user_id=user_id,
            email_type=body.email_type,
            recipient_name=body.recipient_name,
            company_name=body.company_name,
            purpose=body.purpose,
            tone=body.tone,
            language=body.language,
            key_points=body.key_points,
        )
    )

    response = GenerateEmailResponse(
        email_id=result.email_id,
        email_type=result.email_type,
        subject_line=result.subject_line,
        body=result.body,
        tokens_used=result.tokens_used,
    )

    return ApiResponse.ok(
        response,
        message=f"{body.email_type.replace('_', ' ').title()} email generated successfully.",
    )
