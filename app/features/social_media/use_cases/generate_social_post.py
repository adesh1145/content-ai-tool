from dataclasses import dataclass
from typing import Any

from app.core.interfaces.base_use_case import BaseUseCase
from app.features.social_media.use_cases.interfaces.social_interfaces import ISocialAIService, ISocialGateway


@dataclass
class GenerateSocialPostInput:
    user_id: str
    topic: str
    platform: str
    tone: str
    language: str
    target_audience: str
    include_emoji: bool


@dataclass
class GenerateSocialPostOutput:
    post_id: str
    platform: str
    caption: str
    hashtags: list[str]
    char_count: int
    within_limit: bool
    tokens_used: int


class GenerateSocialPostUseCase(BaseUseCase[GenerateSocialPostInput, GenerateSocialPostOutput]):
    def __init__(self, social_repo: ISocialGateway, ai_service: ISocialAIService) -> None:
        self.social_repo = social_repo
        self.ai_service = ai_service

    async def execute(self, input_data: GenerateSocialPostInput) -> GenerateSocialPostOutput:
        # 1. Generate content via AI
        result = await self.ai_service.generate(
            topic=input_data.topic,
            platform=input_data.platform,
            tone=input_data.tone,
            language=input_data.language,
            target_audience=input_data.target_audience,
            include_emoji=input_data.include_emoji,
        )

        caption = result["caption"]
        hashtags = result["hashtags"]
        char_count = result["char_count"]
        
        # Calculate limits organically in the domain
        limits = {"linkedin": 3000, "twitter": 280, "instagram": 2200}
        within_limit = char_count <= limits.get(input_data.platform, 3000)
        
        tokens_used = len(caption.split()) * 2

        # 2. Save to DB
        saved_post = await self.social_repo.save({
            "user_id": input_data.user_id,
            "platform": input_data.platform,
            "topic": input_data.topic,
            "caption": caption,
            "hashtags": hashtags,
            "char_count": char_count,
            "tokens_used": tokens_used,
        })

        return GenerateSocialPostOutput(
            post_id=saved_post["post_id"],
            platform=saved_post["platform"],
            caption=caption,
            hashtags=hashtags,
            char_count=char_count,
            within_limit=within_limit,
            tokens_used=tokens_used,
        )
