from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.seo_optimizer.application.command.generate_meta_command import (
    GenerateMetaCommand,
)
from app.features.seo_optimizer.application.result.meta_result import MetaResult
from app.features.seo_optimizer.domain.exception.seo_analysis_failed import SEOAnalysisFailed
from app.features.seo_optimizer.domain.port.inbound.generate_meta_port import IGenerateMeta
from app.features.seo_optimizer.domain.port.outbound.seo_ai_port import ISEOAIPort


class GenerateMetaService(IGenerateMeta):
    """Generates SEO meta tags (title, description, slug) via AI."""

    def __init__(self, seo_ai: ISEOAIPort) -> None:
        self._seo_ai = seo_ai

    async def execute(self, input_data: GenerateMetaCommand) -> MetaResult:
        if not input_data.content or len(input_data.content.strip()) < 100:
            raise ValidationException("Content must be at least 100 characters for meta generation.")

        try:
            ai_result = await self._seo_ai.generate_meta_tags(
                content=input_data.content[:3000],
                focus_keyword=input_data.focus_keyword,
            )
        except Exception as exc:
            raise SEOAnalysisFailed(f"Meta tag generation failed: {exc}") from exc

        return MetaResult(
            meta_title=ai_result.meta_title,
            meta_description=ai_result.meta_description,
            slug=ai_result.slug,
            tokens_used=ai_result.tokens_used,
        )
