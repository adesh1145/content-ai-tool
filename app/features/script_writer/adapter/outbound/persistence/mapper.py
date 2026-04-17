from __future__ import annotations

from app.common.domain.value_objects import GenerationStatus, Language, ScriptFormat, Tone
from app.features.script_writer.adapter.outbound.persistence.entity import ScriptModel
from app.features.script_writer.domain.model.script import Script


class ScriptORMMapper:
    """Bidirectional mapping between the Script aggregate and the SQLAlchemy model."""

    @staticmethod
    def to_domain(model: ScriptModel) -> Script:
        return Script(
            id=model.id,
            user_id=model.user_id,
            script_format=ScriptFormat(model.format),
            topic=model.topic,
            script_text=model.script_text or "",
            tone=Tone(model.tone),
            language=Language(model.language),
            target_audience=model.target_audience,
            duration_seconds=model.duration_seconds,
            estimated_duration_seconds=model.estimated_duration_seconds,
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            error_message=model.error_message,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: Script) -> ScriptModel:
        return ScriptModel(
            id=entity.id,
            user_id=entity.user_id,
            format=entity.script_format.value,
            topic=entity.topic,
            script_text=entity.script_text,
            tone=entity.tone.value,
            language=entity.language.value,
            target_audience=entity.target_audience,
            duration_seconds=entity.duration_seconds,
            estimated_duration_seconds=entity.estimated_duration_seconds,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            error_message=entity.error_message,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: ScriptModel, entity: Script) -> None:
        model.format = entity.script_format.value
        model.topic = entity.topic
        model.script_text = entity.script_text
        model.tone = entity.tone.value
        model.language = entity.language.value
        model.target_audience = entity.target_audience
        model.duration_seconds = entity.duration_seconds
        model.estimated_duration_seconds = entity.estimated_duration_seconds
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
        model.error_message = entity.error_message
