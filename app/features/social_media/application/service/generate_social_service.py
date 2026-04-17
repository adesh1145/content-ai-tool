from __future__ import annotations

import logging

from app.common.domain.value_objects import GenerationStatus, Language, SocialPlatform, Tone
from app.common.port.inbound.use_case import UseCase
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.social_media.application.command.generate_social_command import (
    GenerateSocialCommand,
)
from app.features.social_media.application.result.social_result import SocialResult
from app.features.social_media.application.validator.social_validator import (
    SocialValidator,
)
from app.features.social_media.domain.exception.social_generation_failed import (
    SocialGenerationFailed,
)
from app.features.social_media.domain.model.social_post import SocialPost
from app.features.social_media.domain.port.outbound.social_ai_port import (
    ISocialAIService,
)
from app.features.social_media.domain.port.outbound.social_repository_port import (
    ISocialRepository,
)

logger = logging.getLogger(__name__)


class GenerateSocialService(UseCase[GenerateSocialCommand, SocialResult]):
    """
    Orchestrates social post generation:
    validate -> create aggregate -> call AI -> complete -> save -> publish events.
    """

    def __init__(
        self,
        social_repo: ISocialRepository,
        social_ai: ISocialAIService,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._repo = social_repo
        self._ai = social_ai
        self._publisher = event_publisher

    async def execute(self, command: GenerateSocialCommand) -> SocialResult:
        SocialValidator.validate(command)

        post = SocialPost(
            user_id=command.user_id,
            platform=SocialPlatform(command.platform),
            topic=command.topic,
            tone=Tone(command.tone),
            language=Language(command.language),
            status=GenerationStatus.PROCESSING,
        )
        await self._repo.save(post)

        try:
            ai_result = await self._ai.generate(
                topic=command.topic,
                platform=command.platform,
                tone=command.tone,
                language=command.language,
                target_audience=command.target_audience,
            )
        except Exception as exc:
            post.fail_generation(str(exc))
            await self._repo.save(post)
            logger.error("Social post generation failed for topic=%s: %s", command.topic, exc)
            raise SocialGenerationFailed(str(exc)) from exc

        tokens_estimated = len(ai_result.content.split()) * 4
        post.complete_generation(
            content=ai_result.content,
            hashtags=ai_result.hashtags,
            tokens=tokens_estimated,
        )
        await self._repo.save(post)

        await self._publisher.publish_all(post.collect_events())

        return SocialResult(
            post_id=post.id,
            platform=post.platform.value,
            content=ai_result.content,
            hashtags=ai_result.hashtags,
            tokens_used=tokens_estimated,
            status=post.status.value,
        )
