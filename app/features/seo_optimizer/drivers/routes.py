"""
app/features/seo_optimizer/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for SEO Optimizer feature.

POST /seo/analyze   — Full SEO analysis of any content
POST /seo/meta      — Generate meta title + description + slug
"""

from __future__ import annotations
import re
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.core.response import APIResponse
from app.features.seo_optimizer.adapters.schemas import (
    KeywordAnalysisResponse,
    MetaGenerateRequest,
    MetaGenerateResponse,
    SEOAnalyzeRequest,
    SEOAnalysisResponse,
)
from app.features.seo_optimizer.drivers.ai.seo_chain import SEOAnalysisService
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/seo", tags=["SEO Optimizer"])


@router.post("/analyze", response_model=APIResponse[SEOAnalysisResponse], status_code=200)
async def analyze_seo(
    body: SEOAnalyzeRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Perform a comprehensive SEO analysis of any content.

    Returns:
    - SEO score (0-100)
    - Readability scores (Flesch Reading Ease + Grade Level)
    - Keyword density analysis
    - On-page SEO checks (headings, links, images, meta)
    - 5 AI-powered actionable recommendations
    """
    try:
        service = SEOAnalysisService()
        analysis = await service.analyze(
            content=body.content,
            focus_keyword=body.focus_keyword,
            meta_title=body.meta_title,
            meta_description=body.meta_description,
            url=body.url,
        )

        return APIResponse.ok(
            SEOAnalysisResponse(
                analysis_id=str(uuid.uuid4()),
                seo_score=analysis.seo_score,
                readability_score=analysis.readability_score,
                flesch_kincaid_grade=analysis.flesch_kincaid_grade,
                word_count=analysis.word_count,
                heading_count=analysis.heading_count,
                has_h1=analysis.has_h1,
                internal_links_count=analysis.internal_links_count,
                external_links_count=analysis.external_links_count,
                image_count=analysis.image_count,
                images_with_alt=analysis.images_with_alt,
                meta_title_length=analysis.meta_title_length,
                meta_description_length=analysis.meta_description_length,
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
                    for ka in analysis.keyword_analyses
                ],
                recommendations=analysis.recommendations,
            ),
            message=f"SEO analysis complete. Score: {analysis.seo_score}/100",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e!s}")


@router.post("/meta", response_model=APIResponse[MetaGenerateResponse], status_code=201)
async def generate_meta_tags(
    body: MetaGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate SEO-optimised meta title, meta description, and URL slug
    from any content. Follows Google's character guidelines.
    """
    from app.infrastructure.ai.llm_factory import get_llm_provider
    provider = get_llm_provider()
    from app.infrastructure.ai.llm_factory import OpenAIProvider, AnthropicProvider
    if isinstance(provider, (OpenAIProvider, AnthropicProvider)):
        llm = provider.get_langchain_llm()
    else:
        raise HTTPException(status_code=500, detail="LLM provider not available.")

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an SEO specialist. Generate meta tags following Google best practices. "
            "Meta title: 50-60 characters, include focus keyword near start. "
            "Meta description: 145-160 characters, include focus keyword, write a compelling summary. "
            "Slug: URL-friendly, lowercase, hyphens only, include focus keyword. "
            "Return ONLY valid JSON: {\"meta_title\": \"...\", \"meta_description\": \"...\", \"slug\": \"...\"}"
        )),
        ("human", (
            "Content (first 500 chars): {content_preview}\n"
            "Focus keyword: {focus_keyword}\n\n"
            "Generate the meta tags."
        )),
    ])

    chain = prompt | llm | StrOutputParser()
    raw = await chain.ainvoke({
        "content_preview": body.content[:500],
        "focus_keyword": body.focus_keyword or "not specified",
    })

    import json
    result = {}
    try:
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
    except (json.JSONDecodeError, AttributeError):
        pass

    def slugify(text: str) -> str:
        return re.sub(r"[-\s]+", "-", re.sub(r"[^\w\s-]", "", text.lower().strip()))

    return APIResponse.ok(
        MetaGenerateResponse(
            meta_title=result.get("meta_title", body.content[:55] + "..."),
            meta_description=result.get("meta_description", body.content[:155] + "..."),
            slug=result.get("slug", slugify(body.content[:50])),
        ),
        message="Meta tags generated successfully.",
    )
