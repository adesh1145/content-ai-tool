"""
app/features/email_writer/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Email Writer.
POST /content/email — cold email, newsletter, follow-up, welcome
"""

from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_current_user_id

from app.core.response import APIResponse
from app.features.email_writer.adapters.schemas import EmailRequest, EmailResponse
from app.features.email_writer.adapters.email_gateway import EmailGateway
from app.features.email_writer.drivers.ai.email_chain import EmailAIService
from app.features.email_writer.use_cases.generate_email import GenerateEmailInput, GenerateEmailUseCase
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/email", tags=["Email Writer"])

VALID_EMAIL_TYPES = {"cold_email", "newsletter", "followup", "welcome"}


@router.post("", response_model=APIResponse[EmailResponse], status_code=201)
async def generate_email(
    body: EmailRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate professional emails:
    - **cold_email**: AIDA framework, personalised, concise
    - **newsletter**: Story → Value → CTA structure
    - **followup**: Brief, polite, adds value
    - **welcome**: Warm onboarding email for new subscribers
    """
    if body.email_type not in VALID_EMAIL_TYPES:
        raise HTTPException(
            status_code=422,
            detail=f"email_type must be one of: {', '.join(VALID_EMAIL_TYPES)}"
        )

    try:
        use_case = GenerateEmailUseCase(
            email_repo=EmailGateway(db),
            ai_service=EmailAIService()
        )
        
        result = await use_case.execute(GenerateEmailInput(
            user_id=user_id,
            email_type=body.email_type,
            recipient_name=body.recipient_name,
            sender_company=body.sender_company,
            topic=body.topic,
            tone=body.tone,
            language=body.language,
            context=body.context,
        ))

        return APIResponse.ok(
            EmailResponse(
                email_id=result.email_id,
                email_type=result.email_type,
                subject=result.subject,
                body=result.body,
                word_count=len(result.body.split()),
                tokens_used=result.tokens_used,
            ),
            message=f"{body.email_type.replace('_', ' ').title()} generated successfully.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
