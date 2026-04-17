from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.features.blog_generator.domain.event.blog_started_event import BlogStartedEvent
from app.features.blog_generator.domain.event.blog_completed_event import BlogCompletedEvent
from app.features.blog_generator.domain.model.seo_metadata import SEOMetadata


@dataclass
class BlogContent(AggregateRoot):
    """
    Blog content aggregate root.

    Invariants:
    - Status transitions: PENDING -> PROCESSING -> COMPLETED | FAILED.
    - Domain events are emitted on lifecycle transitions.
    """

    user_id: str = ""
    project_id: str | None = None
    topic: str = ""
    title: str = ""
    body: str = ""
    outline: list[str] = field(default_factory=list)
    seo: SEOMetadata = field(default_factory=SEOMetadata)
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    target_audience: str = ""
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str | None = None

    def start_generation(self) -> None:
        self.status = GenerationStatus.PROCESSING
        self.touch()
        self.register_event(
            BlogStartedEvent(
                aggregate_id=self.id,
                aggregate_type="BlogContent",
                user_id=self.user_id,
                topic=self.topic,
            )
        )

    def complete_generation(
        self,
        title: str,
        body: str,
        outline: list[str],
        seo: SEOMetadata,
        tokens: int,
    ) -> None:
        self.title = title
        self.body = body
        self.outline = outline
        self.seo = seo
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            BlogCompletedEvent(
                aggregate_id=self.id,
                aggregate_type="BlogContent",
                title=title,
                word_count=seo.word_count,
                tokens_used=tokens,
            )
        )

    def fail_generation(self, error: str) -> None:
        self.status = GenerationStatus.FAILED
        self.error_message = error
        self.touch()
