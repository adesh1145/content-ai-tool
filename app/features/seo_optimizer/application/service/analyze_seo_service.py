from __future__ import annotations

import json
import re

from app.common.domain.value_objects import GenerationStatus
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.seo_optimizer.application.command.analyze_seo_command import (
    AnalyzeSEOCommand,
)
from app.features.seo_optimizer.application.result.seo_analysis_result import (
    SEOAnalysisResult,
)
from app.features.seo_optimizer.application.validator.seo_validator import SEOValidator
from app.features.seo_optimizer.domain.exception.seo_analysis_failed import SEOAnalysisFailed
from app.features.seo_optimizer.domain.model.seo_analysis import SEOAnalysis
from app.features.seo_optimizer.domain.port.inbound.analyze_seo_port import IAnalyzeSEO
from app.features.seo_optimizer.domain.port.outbound.seo_ai_port import ISEOAIPort
from app.features.seo_optimizer.domain.port.outbound.seo_repository_port import ISEORepository
from app.features.seo_optimizer.domain.service.keyword_density_service import (
    KeywordDensityService,
)
from app.features.seo_optimizer.domain.service.readability_service import ReadabilityService


class AnalyzeSEOService(IAnalyzeSEO):
    """
    Orchestrates comprehensive SEO analysis:
      1. Validate command
      2. Content structural analysis (headings, links, images)
      3. Readability analysis
      4. Keyword density analysis
      5. AI-generated recommendations
      6. SEO scoring
      7. Persist and publish events
    """

    def __init__(
        self,
        seo_repo: ISEORepository,
        seo_ai: ISEOAIPort,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._seo_repo = seo_repo
        self._seo_ai = seo_ai
        self._event_publisher = event_publisher

    async def execute(self, input_data: AnalyzeSEOCommand) -> SEOAnalysisResult:
        SEOValidator.validate_analyze(input_data)

        content = input_data.content
        analysis = SEOAnalysis(
            user_id=input_data.user_id,
            content_text=content,
            url=input_data.url,
            focus_keyword=input_data.focus_keyword,
            status=GenerationStatus.PROCESSING,
        )

        lines = content.split("\n")
        word_count = len(re.findall(r"\b\w+\b", content))
        headings = [l for l in lines if l.strip().startswith("#")]
        heading_count = len(headings)
        has_h1 = any(l.strip().startswith("# ") and not l.strip().startswith("##") for l in lines)

        internal_links = len(re.findall(r"\[.*?\]\(/[^)]*\)", content))
        external_links = len(re.findall(r"\[.*?\]\(https?://[^)]*\)", content))

        image_matches = re.findall(r"!\[(.*?)\]\([^)]+\)", content)
        image_count = len(image_matches)
        images_with_alt = sum(1 for alt in image_matches if alt.strip())

        has_meta_title = bool(input_data.meta_title)
        has_meta_description = bool(input_data.meta_description)
        meta_title_length = len(input_data.meta_title)
        meta_description_length = len(input_data.meta_description)

        readability = ReadabilityService.analyze(content)

        keyword_analysis = None
        if input_data.focus_keyword:
            keyword_analysis = KeywordDensityService.analyze(content, input_data.focus_keyword)
            analysis.add_keyword_analysis(keyword_analysis)

        issues: list[str] = []
        if word_count < 600:
            issues.append(f"Word count is {word_count}, aim for at least 600.")
        if not has_h1:
            issues.append("Missing H1 heading.")
        if heading_count < 3:
            issues.append(f"Only {heading_count} headings found, use at least 3.")
        if readability.flesch_reading_ease < 50:
            issues.append(f"Readability score is {readability.flesch_reading_ease}, aim for 50+.")
        if keyword_analysis and keyword_analysis.density_percent < 0.5:
            issues.append(f"Keyword density is {keyword_analysis.density_percent}%, aim for 0.5-3%.")

        recommendations: list[str] = []
        tokens_used = 0
        try:
            ai_result = await self._seo_ai.generate_recommendations(
                content=content[:3000],
                focus_keyword=input_data.focus_keyword,
                current_score=0,
                issues=issues,
            )
            recommendations = ai_result.recommendations
            tokens_used = ai_result.tokens_used
        except Exception as exc:
            analysis.fail_analysis(str(exc))
            await self._seo_repo.save(analysis)
            raise SEOAnalysisFailed(f"AI service error: {exc}") from exc

        overall_score = self._calculate_seo_score(
            word_count=word_count,
            has_h1=has_h1,
            heading_count=heading_count,
            readability_score=readability.flesch_reading_ease,
            keyword_density=keyword_analysis.density_percent if keyword_analysis else 0,
            keyword_in_headings=keyword_analysis.is_in_headings if keyword_analysis else False,
            internal_links=internal_links,
            image_count=image_count,
            images_with_alt=images_with_alt,
            meta_title_length=meta_title_length,
            meta_description_length=meta_description_length,
        )

        keyword_density_json = ""
        if keyword_analysis:
            keyword_density_json = json.dumps({
                "keyword": keyword_analysis.keyword,
                "density_percent": keyword_analysis.density_percent,
                "occurrences": keyword_analysis.occurrences,
            })

        analysis.complete_analysis(
            overall_score=overall_score,
            readability_score=readability.readability_score,
            flesch_reading_ease=readability.flesch_reading_ease,
            flesch_kincaid_grade=readability.flesch_kincaid_grade,
            avg_sentence_length=readability.avg_sentence_length,
            word_count=word_count,
            heading_count=heading_count,
            has_h1=has_h1,
            internal_links_count=internal_links,
            external_links_count=external_links,
            image_count=image_count,
            images_with_alt=images_with_alt,
            has_meta_title=has_meta_title,
            has_meta_description=has_meta_description,
            meta_title_length=meta_title_length,
            meta_description_length=meta_description_length,
            keyword_density_json=keyword_density_json,
            suggestions_json=json.dumps(recommendations),
            recommendations=recommendations,
            tokens_used=tokens_used,
        )

        await self._seo_repo.save(analysis)
        await self._event_publisher.publish_all(analysis.collect_events())

        return SEOAnalysisResult(
            analysis_id=analysis.id,
            overall_score=analysis.overall_score,
            readability_score=analysis.readability_score,
            flesch_reading_ease=analysis.flesch_reading_ease,
            flesch_kincaid_grade=analysis.flesch_kincaid_grade,
            avg_sentence_length=analysis.avg_sentence_length,
            word_count=analysis.word_count,
            heading_count=analysis.heading_count,
            has_h1=analysis.has_h1,
            internal_links_count=analysis.internal_links_count,
            external_links_count=analysis.external_links_count,
            image_count=analysis.image_count,
            images_with_alt=analysis.images_with_alt,
            has_meta_title=analysis.has_meta_title,
            has_meta_description=analysis.has_meta_description,
            meta_title_length=analysis.meta_title_length,
            meta_description_length=analysis.meta_description_length,
            keyword_analyses=analysis.keyword_analyses,
            recommendations=analysis.recommendations,
            tokens_used=analysis.tokens_used,
        )

    @staticmethod
    def _calculate_seo_score(
        *,
        word_count: int,
        has_h1: bool,
        heading_count: int,
        readability_score: float,
        keyword_density: float,
        keyword_in_headings: bool,
        internal_links: int,
        image_count: int,
        images_with_alt: int,
        meta_title_length: int,
        meta_description_length: int,
    ) -> float:
        score = 0.0

        if word_count >= 600:
            score += 15
        elif word_count >= 300:
            score += 8

        if has_h1:
            score += 10

        if heading_count >= 3:
            score += 10
        elif heading_count >= 1:
            score += 5

        if readability_score >= 50:
            score += 15
        elif readability_score >= 30:
            score += 8

        if 0.5 <= keyword_density <= 3.0:
            score += 15
        elif keyword_density > 0:
            score += 5

        if keyword_in_headings:
            score += 10

        if internal_links >= 2:
            score += 10
        elif internal_links >= 1:
            score += 5

        if image_count > 0 and images_with_alt == image_count:
            score += 5
        elif images_with_alt > 0:
            score += 2

        if 50 <= meta_title_length <= 60:
            score += 5
        elif 30 <= meta_title_length <= 70:
            score += 2

        if 145 <= meta_description_length <= 160:
            score += 5
        elif 100 <= meta_description_length <= 200:
            score += 2

        return min(score, 100.0)
