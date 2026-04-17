from dataclasses import dataclass
from typing import Any

from app.core.interfaces.base_use_case import BaseUseCase
from app.features.ad_copy.use_cases.interfaces.ad_interfaces import IAdAIService, IAdGateway


@dataclass
class GenerateAdCopyInput:
    user_id: str
    platform: str
    product_or_service: str
    target_audience: str
    unique_selling_point: str
    tone: str
    num_variations: int


@dataclass
class AdVariationOutput:
    headline: str
    body: str
    cta: str


@dataclass
class GenerateAdCopyOutput:
    ad_id: str
    platform: str
    variations: list[AdVariationOutput]
    tokens_used: int


class GenerateAdCopyUseCase(BaseUseCase[GenerateAdCopyInput, GenerateAdCopyOutput]):
    def __init__(self, ad_repo: IAdGateway, ai_service: IAdAIService) -> None:
        self.ad_repo = ad_repo
        self.ai_service = ai_service

    async def execute(self, input_data: GenerateAdCopyInput) -> GenerateAdCopyOutput:
        # 1. Generate content via AI
        variations_raw = await self.ai_service.generate(
            platform=input_data.platform,
            product=input_data.product_or_service,
            target_audience=input_data.target_audience,
            usp=input_data.unique_selling_point,
            tone=input_data.tone,
            num_variations=input_data.num_variations,
        )

        variations = [
            AdVariationOutput(
                headline=v.get("headline", ""),
                body=v.get("body", ""),
                cta=v.get("cta", "Learn More"),
            )
            for v in variations_raw
        ]

        # Calculate token usage purely as an estimate for logging/quotas
        tokens_used = sum(len(v.body.split()) * 2 for v in variations)

        # 2. Save to DB
        saved_ad = await self.ad_repo.save({
            "user_id": input_data.user_id,
            "platform": input_data.platform,
            "product": input_data.product_or_service,
            "variations": [
                {"headline": v.headline, "body": v.body, "cta": v.cta}
                for v in variations
            ],
            "tokens_used": tokens_used,
        })

        return GenerateAdCopyOutput(
            ad_id=saved_ad["ad_id"],
            platform=saved_ad["platform"],
            variations=variations,
            tokens_used=tokens_used,
        )
