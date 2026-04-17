from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import EmailType, GenerationStatus, Language, Tone
from app.features.email_writer.domain.event.email_created_event import EmailCreatedEvent


@dataclass
class EmailContent(AggregateRoot):
    """
    EmailContent aggregate root.

    Invariants:
    - email_type must be a valid EmailType.
    - Status transitions: PENDING -> PROCESSING -> COMPLETED | FAILED.
    - Domain events are emitted on lifecycle transitions.
    """

    user_id: str = ""
    email_type: EmailType = EmailType.COLD_EMAIL
    recipient_name: str = ""
    company_name: str = ""
    purpose: str = ""
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    subject_line: str = ""
    body: str = ""
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str | None = None

    def complete_generation(self, subject: str, body: str, tokens: int) -> None:
        self.subject_line = subject
        self.body = body
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            EmailCreatedEvent(
                aggregate_id=self.id,
                aggregate_type="EmailContent",
                email_type=self.email_type.value,
                tokens_used=tokens,
            )
        )

    def fail_generation(self, error: str) -> None:
        self.status = GenerationStatus.FAILED
        self.error_message = error
        self.touch()

    @classmethod
    def create(
        cls,
        user_id: str,
        email_type: EmailType,
        recipient_name: str,
        company_name: str,
        purpose: str,
        tone: Tone,
        language: Language,
    ) -> EmailContent:
        return cls(
            user_id=user_id,
            email_type=email_type,
            recipient_name=recipient_name,
            company_name=company_name,
            purpose=purpose,
            tone=tone,
            language=language,
        )
