from __future__ import annotations

from dataclasses import dataclass, field

from app.common.domain.aggregate_root import AggregateRoot
from app.common.domain.value_objects import AdPlatform, GenerationStatus, Language, Tone
from app.features.ad_copy.domain.event.ad_copy_created_event import AdCopyCreatedEvent


@dataclass
class AdCopy(AggregateRoot):
    """
    Ad Copy aggregate root.

    Invariants:
    - Platform must be a valid AdPlatform.
    - Status transitions: PENDING -> PROCESSING -> COMPLETED | FAILED.
    """

    user_id: str = ""
    platform: AdPlatform = AdPlatform.GOOGLE
    product_name: str = ""
    product_description: str = ""
    target_audience: str = ""
    tone: Tone = Tone.PERSUASIVE
    language: Language = Language.ENGLISH
    headline: str = ""
    primary_text: str = ""
    cta_text: str = ""
    variations: list[dict] = field(default_factory=list)
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
    error_message: str | None = None

    def complete_generation(
        self,
        headline: str,
        primary_text: str,
        cta_text: str,
        variations: list[dict],
        tokens: int,
    ) -> None:
        self.headline = headline
        self.primary_text = primary_text
        self.cta_text = cta_text
        self.variations = variations
        self.tokens_used = tokens
        self.status = GenerationStatus.COMPLETED
        self.touch()
        self.register_event(
            AdCopyCreatedEvent(
                aggregate_id=self.id,
                aggregate_type="AdCopy",
                platform=self.platform.value,
                num_variations=len(variations),
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
        platform: AdPlatform,
        product_name: str,
        product_description: str,
        target_audience: str,
        tone: Tone,
        language: Language,
    ) -> AdCopy:
        return cls(
            user_id=user_id,
            platform=platform,
            product_name=product_name,
            product_description=product_description,
            target_audience=target_audience,
            tone=tone,
            language=language,
        )
