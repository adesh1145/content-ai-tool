from __future__ import annotations

from app.common.domain.value_objects import Language, Tone
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.product_description.application.command.generate_product_command import GenerateProductCommand
from app.features.product_description.application.result.product_result import ProductResult
from app.features.product_description.application.validator.product_validator import ProductValidator
from app.features.product_description.domain.exception.product_generation_failed import ProductGenerationFailed
from app.features.product_description.domain.model.product_description import ProductDescription
from app.features.product_description.application.port.inbound.generate_product_desc_port import GenerateProductDescPort
from app.features.product_description.domain.port.outbound.product_ai_port import ProductAIPort
from app.features.product_description.domain.port.outbound.product_repository_port import ProductRepositoryPort


class GenerateProductService(GenerateProductDescPort):
    """
    Orchestrates product description generation using the F-A-B framework.

    Flow: validate -> create aggregate -> persist (PENDING) -> call AI ->
          mark_completed -> persist (COMPLETED) -> publish events -> return result.
    """

    def __init__(
        self,
        product_repo: ProductRepositoryPort,
        product_ai: ProductAIPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._product_repo = product_repo
        self._product_ai = product_ai
        self._event_publisher = event_publisher

    async def execute(self, input_data: GenerateProductCommand) -> ProductResult:
        ProductValidator.validate(input_data)

        product = ProductDescription.create(
            user_id=input_data.user_id,
            product_name=input_data.product_name,
            category=input_data.category,
            features=input_data.features,
            tone=Tone(input_data.tone),
            language=Language(input_data.language),
        )
        await self._product_repo.save(product)

        try:
            result = await self._product_ai.generate(
                product_name=input_data.product_name,
                category=input_data.category,
                features=input_data.features,
                tone=input_data.tone,
                target_audience=input_data.target_audience,
                language=input_data.language,
                word_count=input_data.word_count,
            )
        except Exception as exc:
            product.fail_generation(str(exc))
            await self._product_repo.save(product)
            raise ProductGenerationFailed(f"AI service error: {exc}") from exc

        product.mark_completed(
            description=result["description"],
            tokens=result.get("tokens_used", 0),
        )

        await self._product_repo.save(product)
        await self._event_publisher.publish_all(product.collect_events())

        return ProductResult(
            product_id=product.id,
            description=product.description,
            word_count=len(product.description.split()),
            tokens_used=product.tokens_used,
        )
