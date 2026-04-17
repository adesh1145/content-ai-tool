from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.features.article_writer.domain.event.article_completed_event import (
    ArticleCompletedEvent,
)
from app.features.article_writer.domain.event.article_started_event import (
    ArticleStartedEvent,
)


@dataclass
class Article(AggregateRoot):
    """Aggregate root representing an AI-generated article."""

    user_id: str = ""
    topic: str = ""
    title: str = ""
    content: str = ""
    outline: str = ""
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    target_audience: str = ""
    word_count_target: int = 1500
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str = ""

    def start_generation(self) -> None:
        self.status = GenerationStatus.PROCESSING
        self.touch()
        self.register_event(
            ArticleStartedEvent(
                aggregate_id=self.id,
                aggregate_type="Article",
                topic=self.topic,
                user_id=self.user_id,
            )
        )

    def complete_generation(self, title: str, content: str, tokens: int) -> None:
        self.title = title
        self.content = content
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            ArticleCompletedEvent(
                aggregate_id=self.id,
                aggregate_type="Article",
                topic=self.topic,
                title=title,
                tokens_used=tokens,
                user_id=self.user_id,
            )
        )

    def fail_generation(self, error: str) -> None:
        self.status = GenerationStatus.FAILED
        self.error_message = error
        self.touch()
