from __future__ import annotations

from app.common.domain.value_objects import EmailType, GenerationStatus, Language, Tone
from app.features.email_writer.adapter.outbound.persistence.entity import EmailContentModel
from app.features.email_writer.domain.model.email_content import EmailContent


class EmailContentMapper:
    """Bidirectional mapping between EmailContent aggregate and SQLAlchemy model."""

    @staticmethod
    def to_domain(model: EmailContentModel) -> EmailContent:
        return EmailContent(
            id=model.id,
            user_id=model.user_id,
            email_type=EmailType(model.email_type),
            recipient_name=model.recipient_name,
            company_name=model.company_name,
            purpose=model.purpose,
            subject_line=model.subject_line,
            body=model.body,
            tone=Tone(model.tone),
            language=Language(model.language),
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: EmailContent) -> EmailContentModel:
        return EmailContentModel(
            id=entity.id,
            user_id=entity.user_id,
            email_type=entity.email_type.value,
            recipient_name=entity.recipient_name,
            company_name=entity.company_name,
            purpose=entity.purpose,
            subject_line=entity.subject_line,
            body=entity.body,
            tone=entity.tone.value,
            language=entity.language.value,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            error_message=entity.error_message,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: EmailContentModel, entity: EmailContent) -> None:
        model.email_type = entity.email_type.value
        model.recipient_name = entity.recipient_name
        model.company_name = entity.company_name
        model.purpose = entity.purpose
        model.subject_line = entity.subject_line
        model.body = entity.body
        model.tone = entity.tone.value
        model.language = entity.language.value
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
        model.error_message = entity.error_message
