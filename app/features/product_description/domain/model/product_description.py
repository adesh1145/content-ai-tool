from __future__ import annotations

from dataclasses import dataclass

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.features.product_description.domain.event.product_desc_created_event import ProductDescCreatedEvent


@dataclass
class ProductDescription(AggregateRoot):
    """
    ProductDescription aggregate root.

    Invariants:
    - Product name must be >= 3 characters.
    - Features list should not be empty.
    - Status transitions: PENDING -> PROCESSING -> COMPLETED | FAILED.
    """

    user_id: str = ""
    product_name: str = ""
    category: str = ""
    features: list[str] | None = None
    description: str = ""
    tone: Tone = Tone.PROFESSIONAL
    language: Language = Language.ENGLISH
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str | None = None

    def __post_init__(self) -> None:
        if self.features is None:
            self.features = []

    def mark_completed(self, description: str, tokens: int) -> None:
        self.description = description
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            ProductDescCreatedEvent(
                aggregate_id=self.id,
                aggregate_type="ProductDescription",
                product_name=self.product_name,
                word_count=len(description.split()),
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
        product_name: str,
        category: str,
        features: list[str],
        tone: Tone,
        language: Language,
    ) -> ProductDescription:
        return cls(
            user_id=user_id,
            product_name=product_name,
            category=category,
            features=features,
            tone=tone,
            language=language,
        )
