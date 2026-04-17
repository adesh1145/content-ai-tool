from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import GenerationStatus, Language, ScriptFormat, Tone
from app.features.script_writer.domain.event.script_completed_event import ScriptCompletedEvent


@dataclass
class Script(AggregateRoot):
    """Script aggregate root — owns the lifecycle of a script generation request."""

    user_id: str = ""
    script_format: ScriptFormat = ScriptFormat.YOUTUBE
    topic: str = ""
    script_text: str = ""
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    target_audience: str = ""
    duration_seconds: int = 0
    estimated_duration_seconds: int = 0
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str | None = None

    def complete_generation(
        self, script_text: str, estimated_duration: int, tokens: int
    ) -> None:
        self.script_text = script_text
        self.estimated_duration_seconds = estimated_duration
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            ScriptCompletedEvent(
                aggregate_id=self.id,
                aggregate_type="Script",
                script_format=self.script_format.value,
                topic=self.topic,
                estimated_duration_seconds=estimated_duration,
            )
        )

    def fail_generation(self, error: str) -> None:
        self.error_message = error
        self.status = GenerationStatus.FAILED
        self.touch()
