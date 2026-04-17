from __future__ import annotations

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.common.domain.value_objects import AdPlatform, Language, Tone
from app.features.ad_copy.application.command.generate_ad_command import GenerateAdCommand
from app.features.ad_copy.application.result.ad_result import AdResult
from app.features.ad_copy.application.validator.ad_validator import AdValidator
from app.features.ad_copy.domain.exception.ad_generation_failed import AdGenerationFailed
from app.features.ad_copy.domain.model.ad_copy import AdCopy
from app.features.ad_copy.domain.port.inbound.generate_ad_port import GenerateAdPort
from app.features.ad_copy.domain.port.outbound.ad_ai_port import AdAIPort
from app.features.ad_copy.domain.port.outbound.ad_repository_port import AdRepositoryPort


class GenerateAdService(GenerateAdPort):
    """
    Orchestrates ad copy generation.

    Flow: validate -> create aggregate -> persist (PENDING) -> call AI ->
          complete_generation -> persist (COMPLETED) -> publish events -> return result.

    Uses platform-specific prompts:
    - Google Ads: AIDA framework (Attention-Interest-Desire-Action)
    - Facebook Ads: PAS framework (Problem-Agitate-Solution)
    """

    def __init__(
        self,
        ad_repo: AdRepositoryPort,
        ad_ai: AdAIPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._ad_repo = ad_repo
        self._ad_ai = ad_ai
        self._event_publisher = event_publisher

    async def execute(self, input_data: GenerateAdCommand) -> AdResult:
        AdValidator.validate(input_data)

        ad = AdCopy.create(
            user_id=input_data.user_id,
            platform=AdPlatform(input_data.platform),
            product_name=input_data.product_name,
            product_description=input_data.product_description,
            target_audience=input_data.target_audience,
            tone=Tone(input_data.tone),
            language=Language(input_data.language),
        )
        await self._ad_repo.save(ad)

        try:
            result = await self._ad_ai.generate(
                platform=input_data.platform,
                product_name=input_data.product_name,
                product_description=input_data.product_description,
                target_audience=input_data.target_audience,
                tone=input_data.tone,
                language=input_data.language,
                num_variations=input_data.num_variations,
            )
        except Exception as exc:
            ad.fail_generation(str(exc))
            await self._ad_repo.save(ad)
            raise AdGenerationFailed(f"AI service error: {exc}") from exc

        ad.complete_generation(
            headline=result["headline"],
            primary_text=result["primary_text"],
            cta_text=result["cta_text"],
            variations=result["variations"],
            tokens=result.get("tokens_used", 0),
        )

        await self._ad_repo.save(ad)
        await self._event_publisher.publish_all(ad.collect_events())

        return AdResult(
            ad_id=ad.id,
            platform=ad.platform.value,
            headline=ad.headline,
            primary_text=ad.primary_text,
            cta_text=ad.cta_text,
            variations=ad.variations,
            tokens_used=ad.tokens_used,
        )
