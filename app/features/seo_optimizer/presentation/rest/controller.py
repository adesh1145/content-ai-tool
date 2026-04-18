from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.common.exception.base_exception import AppException, ValidationException
from app.dependencies import get_current_user_id
from app.features.seo_optimizer.presentation.rest.dto.request import (
    MetaGenerateRequest,
    SEOAnalyzeRequest,
)
from app.features.seo_optimizer.presentation.rest.dto.response import (
    KeywordAnalysisResponse,
    MetaGenerateResponse,
    SEOAnalyzeResponse,
)
from app.features.seo_optimizer.application.command.analyze_seo_command import (
    AnalyzeSEOCommand,
)
from app.features.seo_optimizer.application.command.generate_meta_command import (
    GenerateMetaCommand,
)
from app.features.seo_optimizer.config.container import (
    get_analyze_seo_usecase,
    get_generate_meta_usecase,
)
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/seo", tags=["SEO Optimizer"])


@router.post("/analyze", response_model=ApiResponse[SEOAnalyzeResponse], status_code=200)
async def analyze_seo(
    body: SEOAnalyzeRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Run comprehensive SEO analysis on content.

    Analyses: word count, heading structure, readability (Flesch),
    keyword density, link counts, image alt tags, meta tag quality,
    plus AI-generated recommendations.
    """
    try:
        use_case = get_analyze_seo_usecase(db)
        result = await use_case.execute(
            AnalyzeSEOCommand(
                user_id=user_id,
                content=body.content,
                focus_keyword=body.focus_keyword,
                meta_title=body.meta_title,
                meta_description=body.meta_description,
                url=body.url,
            )
        )

        response = SEOAnalyzeResponse(
            analysis_id=result.analysis_id,
            overall_score=result.overall_score,
            readability_score=result.readability_score,
            flesch_reading_ease=result.flesch_reading_ease,
            flesch_kincaid_grade=result.flesch_kincaid_grade,
            avg_sentence_length=result.avg_sentence_length,
            word_count=result.word_count,
            heading_count=result.heading_count,
            has_h1=result.has_h1,
            internal_links_count=result.internal_links_count,
            external_links_count=result.external_links_count,
            image_count=result.image_count,
            images_with_alt=result.images_with_alt,
            has_meta_title=result.has_meta_title,
            has_meta_description=result.has_meta_description,
            meta_title_length=result.meta_title_length,
            meta_description_length=result.meta_description_length,
            keyword_analyses=[
                KeywordAnalysisResponse(
                    keyword=ka.keyword,
                    density_percent=ka.density_percent,
                    occurrences=ka.occurrences,
                    is_in_title=ka.is_in_title,
                    is_in_first_paragraph=ka.is_in_first_paragraph,
                    is_in_headings=ka.is_in_headings,
                    recommendation=ka.recommendation,
                )
                for ka in result.keyword_analyses
            ],
            recommendations=result.recommendations,
            tokens_used=result.tokens_used,
        )

        return ApiResponse.ok(response, message="SEO analysis completed.")
    except ValidationException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/meta", response_model=ApiResponse[MetaGenerateResponse], status_code=201)
async def generate_meta(
    body: MetaGenerateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate SEO-optimized meta tags (title, description, slug) from content.
    """
    try:
        use_case = get_generate_meta_usecase(db)
        result = await use_case.execute(
            GenerateMetaCommand(
                user_id=user_id,
                content=body.content,
                focus_keyword=body.focus_keyword,
            )
        )

        response = MetaGenerateResponse(
            meta_title=result.meta_title,
            meta_description=result.meta_description,
            slug=result.slug,
            tokens_used=result.tokens_used,
        )

        return ApiResponse.ok(response, message="Meta tags generated successfully.")
    except ValidationException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
