from dataclasses import dataclass
from typing import Any

from app.core.interfaces.base_use_case import BaseUseCase
from app.features.product_description.use_cases.interfaces.product_interfaces import IProductAIService, IProductGateway


@dataclass
class GenerateProductDescInput:
    user_id: str
    product_name: str
    category: str
    features: list[str]
    tone: str
    target_audience: str
    language: str
    word_count: int


@dataclass
class GenerateProductDescOutput:
    product_id: str
    description: str
    word_count: int
    tokens_used: int


class GenerateProductDescUseCase(BaseUseCase[GenerateProductDescInput, GenerateProductDescOutput]):
    def __init__(self, product_repo: IProductGateway, ai_service: IProductAIService) -> None:
        self.product_repo = product_repo
        self.ai_service = ai_service

    async def execute(self, input_data: GenerateProductDescInput) -> GenerateProductDescOutput:
        # 1. Generate content via AI
        result = await self.ai_service.generate(
            product_name=input_data.product_name,
            category=input_data.category,
            features=input_data.features,
            tone=input_data.tone,
            target_audience=input_data.target_audience,
            language=input_data.language,
            word_count=input_data.word_count,
        )

        description = result["description"]
        actual_word_count = result["word_count"]
        tokens_used = actual_word_count * 2

        # 2. Save to DB
        saved_desc = await self.product_repo.save({
            "user_id": input_data.user_id,
            "product_name": input_data.product_name,
            "category": input_data.category,
            "features": input_data.features,
            "description": description,
            "word_count": actual_word_count,
            "tokens_used": tokens_used,
        })

        return GenerateProductDescOutput(
            product_id=saved_desc["product_id"],
            description=description,
            word_count=actual_word_count,
            tokens_used=tokens_used,
        )
