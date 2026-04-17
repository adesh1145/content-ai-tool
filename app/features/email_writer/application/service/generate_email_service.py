from __future__ import annotations

from app.common.domain.value_objects import EmailType, Language, Tone
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.email_writer.application.command.generate_email_command import GenerateEmailCommand
from app.features.email_writer.application.result.email_result import EmailResult
from app.features.email_writer.application.validator.email_validator import EmailValidator
from app.features.email_writer.domain.exception.email_generation_failed import EmailGenerationFailed
from app.features.email_writer.domain.model.email_content import EmailContent
from app.features.email_writer.domain.port.inbound.generate_email_port import GenerateEmailPort
from app.features.email_writer.domain.port.outbound.email_ai_port import EmailAIPort
from app.features.email_writer.domain.port.outbound.email_repository_port import EmailRepositoryPort


class GenerateEmailService(GenerateEmailPort):
    """
    Orchestrates email content generation.

    Flow: validate -> create aggregate -> persist (PENDING) -> call AI ->
          complete_generation -> persist (COMPLETED) -> publish events -> return result.

    Email-type-specific prompts:
    - cold_email: concise with clear CTA
    - newsletter: informative and engaging
    - followup: references previous interaction, gentle nudge
    - welcome: warm, onboarding-focused
    """

    def __init__(
        self,
        email_repo: EmailRepositoryPort,
        email_ai: EmailAIPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._email_repo = email_repo
        self._email_ai = email_ai
        self._event_publisher = event_publisher

    async def execute(self, input_data: GenerateEmailCommand) -> EmailResult:
        EmailValidator.validate(input_data)

        email = EmailContent.create(
            user_id=input_data.user_id,
            email_type=EmailType(input_data.email_type),
            recipient_name=input_data.recipient_name,
            company_name=input_data.company_name,
            purpose=input_data.purpose,
            tone=Tone(input_data.tone),
            language=Language(input_data.language),
        )
        await self._email_repo.save(email)

        try:
            result = await self._email_ai.generate(
                email_type=input_data.email_type,
                recipient_name=input_data.recipient_name,
                company_name=input_data.company_name,
                purpose=input_data.purpose,
                tone=input_data.tone,
                language=input_data.language,
                key_points=input_data.key_points or None,
            )
        except Exception as exc:
            email.fail_generation(str(exc))
            await self._email_repo.save(email)
            raise EmailGenerationFailed(f"AI service error: {exc}") from exc

        email.complete_generation(
            subject=result["subject_line"],
            body=result["body"],
            tokens=result.get("tokens_used", 0),
        )

        await self._email_repo.save(email)
        await self._event_publisher.publish_all(email.collect_events())

        return EmailResult(
            email_id=email.id,
            email_type=email.email_type.value,
            subject_line=email.subject_line,
            body=email.body,
            tokens_used=email.tokens_used,
        )
