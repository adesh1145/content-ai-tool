"""
app/features/blog_generator/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Blog Generator feature.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import APIResponse
from app.core.exceptions import ValidationError
from app.features.blog_generator.adapters.schemas import (
    BlogGenerateRequest,
    BlogGenerateResponse,
    SEOMetaResponse,
)
from app.features.blog_generator.drivers.ai.blog_chain import BlogAIService
from app.features.blog_generator.use_cases.generate_blog import (
    GenerateBlogInput,
    GenerateBlogUseCase,
)
from app.features.blog_generator.adapters.blog_gateway import BlogGateway
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/blog", tags=["Blog Generator"])


@router.post("", response_model=APIResponse[BlogGenerateResponse], status_code=201)
async def generate_blog(
    body: BlogGenerateRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate an SEO-optimised blog post.

    Returns full markdown content with:
    - Structured outline
    - SEO meta title, meta description, URL slug
    - Focus keyword integration
    - Flesch-Kincaid readability score
    - Estimated reading time
    """
    try:
        use_case = GenerateBlogUseCase(
            blog_repo=BlogGateway(db),
            blog_ai=BlogAIService(),
        )
        result = await use_case.execute(
            GenerateBlogInput(
                user_id="demo-user",  # Replace with actual auth user
                topic=body.topic,
                tone=body.tone,
                language=body.language,
                target_audience=body.target_audience,
                focus_keyword=body.focus_keyword,
                secondary_keywords=body.secondary_keywords,
                word_count=body.word_count,
                project_id=body.project_id,
            )
        )

        return APIResponse.ok(
            BlogGenerateResponse(
                blog_id=result.blog_id,
                title=result.title,
                body=result.body,
                outline=result.outline,
                seo=SEOMetaResponse(
                    meta_title=result.seo_meta_title,
                    meta_description=result.seo_meta_description,
                    slug=result.seo_slug,
                    focus_keyword=result.seo_focus_keyword,
                    readability_score=result.seo_readability_score,
                    word_count=result.word_count,
                ),
                tokens_used=result.tokens_used,
                status=result.status,
            ),
            message="Blog post generated successfully.",
        )

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")


@router.get("/history", response_model=APIResponse[list])
async def get_blog_history(
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db_session),
):
    """Get current user's blog generation history."""
    gateway = BlogGateway(db)
    blogs = await gateway.list_by_user("demo-user", limit=limit, offset=offset)
    return APIResponse.ok([{"id": b.id, "topic": b.topic, "title": b.title, "status": b.status.value} for b in blogs])


@router.get("/{blog_id}", response_model=APIResponse[BlogGenerateResponse])
async def get_blog(
    blog_id: str,
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve a specific generated blog post by ID."""
    gateway = BlogGateway(db)
    blog = await gateway.get_by_id(blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog '{blog_id}' not found.")
    return APIResponse.ok(
        BlogGenerateResponse(
            blog_id=blog.id,
            title=blog.title,
            body=blog.body,
            outline=blog.outline,
            seo=SEOMetaResponse(
                meta_title=blog.seo.meta_title,
                meta_description=blog.seo.meta_description,
                slug=blog.seo.slug,
                focus_keyword=blog.seo.focus_keyword,
                readability_score=blog.seo.readability_score,
                word_count=blog.seo.word_count,
            ),
            tokens_used=blog.tokens_used,
            status=blog.status.value,
        )
    )
