from __future__ import annotations

import logging

from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.common.port.inbound.use_case import UseCase
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.article_writer.application.command.generate_article_command import (
    GenerateArticleCommand,
)
from app.features.article_writer.application.result.article_result import (
    ArticleResult,
)
from app.features.article_writer.application.validator.article_validator import (
    ArticleValidator,
)
from app.features.article_writer.domain.exception.article_generation_failed import (
    ArticleGenerationFailed,
)
from app.features.article_writer.domain.model.article import Article
from app.features.article_writer.domain.port.outbound.article_ai_port import (
    IArticleAIService,
)
from app.features.article_writer.domain.port.outbound.article_repository_port import (
    IArticleRepository,
)

logger = logging.getLogger(__name__)


class GenerateArticleService(UseCase[GenerateArticleCommand, ArticleResult]):
    """
    Orchestrates article generation:
    validate -> create aggregate -> save(PROCESSING) -> AI pipeline ->
    complete -> save(COMPLETED) -> publish events.
    """

    def __init__(
        self,
        article_repo: IArticleRepository,
        article_ai: IArticleAIService,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._repo = article_repo
        self._ai = article_ai
        self._publisher = event_publisher

    async def execute(self, command: GenerateArticleCommand) -> ArticleResult:
        ArticleValidator.validate(command)

        article = Article(
            user_id=command.user_id,
            topic=command.topic,
            tone=Tone(command.tone),
            language=Language(command.language),
            target_audience=command.target_audience,
            word_count_target=command.word_count_target,
            status=GenerationStatus.PROCESSING,
        )
        article.start_generation()
        await self._repo.save(article)

        try:
            ai_result = await self._ai.generate_article(
                topic=command.topic,
                tone=command.tone,
                language=command.language,
                target_audience=command.target_audience,
                focus_keyword=command.focus_keyword,
                word_count=command.word_count_target,
            )
        except Exception as exc:
            article.fail_generation(str(exc))
            await self._repo.save(article)
            logger.error("Article generation failed for topic=%s: %s", command.topic, exc)
            raise ArticleGenerationFailed(str(exc)) from exc

        article.complete_generation(
            title=ai_result.title,
            content=ai_result.content,
            tokens=ai_result.tokens_used,
        )
        await self._repo.save(article)

        await self._publisher.publish_all(article.collect_events())

        word_count = len(ai_result.content.split())
        return ArticleResult(
            article_id=article.id,
            topic=article.topic,
            title=ai_result.title,
            content=ai_result.content,
            meta_title=ai_result.meta_title,
            meta_description=ai_result.meta_description,
            word_count=word_count,
            tokens_used=ai_result.tokens_used,
            status=article.status.value,
        )
