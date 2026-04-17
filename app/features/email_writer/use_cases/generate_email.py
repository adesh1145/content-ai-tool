from dataclasses import dataclass

from app.core.interfaces.base_use_case import BaseUseCase
from app.features.email_writer.use_cases.interfaces.email_interfaces import IEmailAIService, IEmailGateway


@dataclass
class GenerateEmailInput:
    user_id: str
    email_type: str
    recipient_name: str
    sender_company: str
    topic: str
    tone: str
    language: str
    context: str | None


@dataclass
class GenerateEmailOutput:
    email_id: str
    email_type: str
    subject: str
    body: str
    tokens_used: int


class GenerateEmailUseCase(BaseUseCase[GenerateEmailInput, GenerateEmailOutput]):
    def __init__(self, email_repo: IEmailGateway, ai_service: IEmailAIService) -> None:
        self.email_repo = email_repo
        self.ai_service = ai_service

    async def execute(self, input_data: GenerateEmailInput) -> GenerateEmailOutput:
        # 1. Generate content via AI
        result = await self.ai_service.generate(
            email_type=input_data.email_type,
            recipient_name=input_data.recipient_name,
            sender_company=input_data.sender_company,
            topic=input_data.topic,
            tone=input_data.tone,
            language=input_data.language,
            context=input_data.context or "",
        )

        subject = result["subject"]
        body = result["body"]
        
        # Estimate tokens
        tokens_used = len(body.split()) * 2

        # 2. Save to DB
        saved_email = await self.email_repo.save({
            "user_id": input_data.user_id,
            "email_type": input_data.email_type,
            "recipient_name": input_data.recipient_name,
            "sender_company": input_data.sender_company,
            "topic": input_data.topic,
            "subject": subject,
            "body": body,
            "tokens_used": tokens_used,
        })

        return GenerateEmailOutput(
            email_id=saved_email["email_id"],
            email_type=saved_email["email_type"],
            subject=subject,
            body=body,
            tokens_used=tokens_used,
        )
