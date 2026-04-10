"""
app/features/blog_generator/use_cases/generate_blog.py
─────────────────────────────────────────────────────────────
GenerateBlogUseCase — Layer 2: Application Business Rules.

Orchestrates: quota check → blog entity → AI generation → persist → return.
Depends only on abstractions (IBlogRepository, IBlogAIService, IUsageTracker).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.core.entities.value_objects import GenerationStatus, Language, Tone
from app.core.exceptions import ValidationError
from app.core.interfaces.base_use_case import IUseCase
from app.features.blog_generator.entities.blog_content import BlogContent, SEOMetadata
from app.features.blog_generator.use_cases.interfaces.blog_interfaces import (
    BlogGenerationRequest,
    IBlogAIService,
    IBlogRepository,
)


@dataclass
class GenerateBlogInput:
    user_id: str
    topic: str
    tone: str = "professional"
    language: str = "en"
    target_audience: str = "general"
    focus_keyword: str = ""
    secondary_keywords: list[str] = field(default_factory=list)
    word_count: int = 800
    project_id: str | None = None


@dataclass
class GenerateBlogOutput:
    blog_id: str
    title: str
    body: str
    outline: list[str]
    seo_meta_title: str
    seo_meta_description: str
    seo_slug: str
    seo_focus_keyword: str
    seo_readability_score: float
    word_count: int
    tokens_used: int
    status: str


class GenerateBlogUseCase(IUseCase[GenerateBlogInput, GenerateBlogOutput]):
    """
    Generate an SEO-optimized blog post.

    DIP: Depends on IBlogRepository and IBlogAIService (interfaces).
    SRP: Only orchestrates blog generation — no direct LLM/DB code here.
    """

    def __init__(
        self,
        blog_repo: IBlogRepository,
        blog_ai: IBlogAIService,
    ) -> None:
        self._blog_repo = blog_repo
        self._blog_ai = blog_ai

    async def execute(self, input_data: GenerateBlogInput) -> GenerateBlogOutput:
        # Domain validation
        if not input_data.topic or len(input_data.topic.strip()) < 10:
            raise ValidationError("Topic must be at least 10 characters.")
        if input_data.word_count < 300 or input_data.word_count > 5000:
            raise ValidationError("Word count must be between 300 and 5000.")

        # Create blog entity (starts as PROCESSING)
        blog = BlogContent(
            user_id=input_data.user_id,
            topic=input_data.topic.strip(),
            tone=Tone(input_data.tone),
            language=Language(input_data.language),
            target_audience=input_data.target_audience,
            project_id=input_data.project_id,
            status=GenerationStatus.PROCESSING,
        )
        blog = await self._blog_repo.save(blog)

        try:
            # Call AI service (LangChain chain — injected via IBlogAIService)
            result = await self._blog_ai.generate(
                BlogGenerationRequest(
                    topic=input_data.topic,
                    tone=input_data.tone,
                    language=input_data.language,
                    target_audience=input_data.target_audience,
                    focus_keyword=input_data.focus_keyword,
                    secondary_keywords=input_data.secondary_keywords,
                    word_count=input_data.word_count,
                )
            )

            # Update entity with result
            blog.title = result.title
            blog.outline = result.outline
            blog.mark_completed(result.body, result.seo, result.tokens_used)
            await self._blog_repo.save(blog)

        except Exception as e:
            blog.mark_failed(str(e))
            await self._blog_repo.save(blog)
            raise

        return GenerateBlogOutput(
            blog_id=blog.id,
            title=blog.title,
            body=blog.body,
            outline=blog.outline,
            seo_meta_title=blog.seo.meta_title,
            seo_meta_description=blog.seo.meta_description,
            seo_slug=blog.seo.slug,
            seo_focus_keyword=blog.seo.focus_keyword,
            seo_readability_score=blog.seo.readability_score,
            word_count=blog.seo.word_count,
            tokens_used=blog.tokens_used,
            status=blog.status.value,
        )
