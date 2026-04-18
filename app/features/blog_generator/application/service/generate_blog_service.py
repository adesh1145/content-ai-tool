from __future__ import annotations

from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.blog_generator.application.command.generate_blog_command import GenerateBlogCommand
from app.features.blog_generator.application.mapper.blog_mapper import BlogMapper
from app.features.blog_generator.application.result.blog_result import BlogResult
from app.features.blog_generator.application.validator.blog_validator import BlogValidator
from app.features.blog_generator.domain.exception.blog_generation_failed import BlogGenerationFailed
from app.features.blog_generator.domain.model.blog_content import BlogContent
from app.features.blog_generator.domain.model.seo_metadata import SEOMetadata
from app.features.blog_generator.application.port.inbound.generate_blog_port import IGenerateBlog
from app.features.blog_generator.domain.port.outbound.blog_ai_port import IBlogAIService
from app.features.blog_generator.domain.port.outbound.blog_repository_port import IBlogRepository


class GenerateBlogService(IGenerateBlog):
    """
    Orchestrates blog generation.

    Flow: validate -> create aggregate -> persist (PROCESSING) -> call AI ->
          complete_generation -> persist (COMPLETED) -> publish events -> return result.
    """

    def __init__(
        self,
        blog_repo: IBlogRepository,
        blog_ai: IBlogAIService,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._blog_repo = blog_repo
        self._blog_ai = blog_ai
        self._event_publisher = event_publisher

    async def execute(self, input_data: GenerateBlogCommand) -> BlogResult:
        BlogValidator.validate_generate(input_data)

        blog = BlogContent(
            user_id=input_data.user_id,
            project_id=input_data.project_id,
            topic=input_data.topic,
            tone=input_data.tone,
            language=input_data.language,
            target_audience=input_data.target_audience,
        )
        blog.start_generation()
        blog = await self._blog_repo.save(blog)

        try:
            ai_result = await self._blog_ai.generate_blog(
                topic=input_data.topic,
                tone=input_data.tone,
                language=input_data.language,
                target_audience=input_data.target_audience,
                focus_keyword=input_data.focus_keyword or input_data.topic,
                secondary_keywords=list(input_data.secondary_keywords),
                word_count=input_data.word_count,
            )

            seo = SEOMetadata(
                meta_title=ai_result.meta_title,
                meta_description=ai_result.meta_description,
                slug=ai_result.slug,
                focus_keyword=ai_result.focus_keyword or input_data.focus_keyword,
                secondary_keywords=tuple(ai_result.secondary_keywords),
                word_count=ai_result.word_count,
                readability_score=ai_result.readability_score,
                reading_time_minutes=ai_result.reading_time_minutes,
            )

            blog.complete_generation(
                title=ai_result.title,
                body=ai_result.body,
                outline=ai_result.outline,
                seo=seo,
                tokens=ai_result.tokens_used,
            )
        except Exception as exc:
            blog.fail_generation(str(exc))
            await self._blog_repo.save(blog)
            await self._event_publisher.publish_all(blog.collect_events())
            raise BlogGenerationFailed(str(exc)) from exc

        await self._blog_repo.save(blog)
        await self._event_publisher.publish_all(blog.collect_events())

        return BlogMapper.to_result(blog)
