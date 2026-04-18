from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.common.exception.base_exception import AppException, NotFoundException, ValidationException
from app.dependencies import get_current_user_id
from app.features.blog_generator.application.command.generate_blog_command import GenerateBlogCommand
from app.features.blog_generator.application.query.get_blog_query import GetBlogQuery
from app.features.blog_generator.application.query.list_blogs_query import ListBlogsQuery
from app.features.blog_generator.config.container import BlogContainer
from app.features.blog_generator.presentation.rest.dto.request import BlogGenerateRequest
from app.features.blog_generator.presentation.rest.dto.response import BlogGenerateResponse
from app.features.blog_generator.presentation.rest.mapper import BlogRestMapper
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/blog", tags=["Blog Generator"])


@router.post("", response_model=ApiResponse[BlogGenerateResponse], status_code=201)
async def generate_blog(
    body: BlogGenerateRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate an SEO-optimised blog post using a multi-step AI pipeline.

    Pipeline steps:
    1. Outline generation — structured section headings
    2. Content writing — full markdown blog body
    3. SEO optimisation — meta title, description, slug
    4. Readability analysis — Flesch-Kincaid scoring
    """
    try:
        service = BlogContainer.generate_blog_service(db)
        result = await service.execute(
            GenerateBlogCommand(
                user_id=user_id,
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
        return ApiResponse.ok(
            BlogRestMapper.to_response(result),
            message="Blog post generated successfully.",
        )
    except ValidationException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/history", response_model=ApiResponse[list[BlogGenerateResponse]])
async def list_blogs(
    limit: int = 20,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """List the authenticated user's generated blog posts with pagination."""
    try:
        service = BlogContainer.list_blogs_service(db)
        results = await service.execute(
            ListBlogsQuery(user_id=user_id, limit=limit, offset=offset)
        )
        return ApiResponse.ok(
            BlogRestMapper.to_response_list(results),
            message=f"Retrieved {len(results)} blog(s).",
        )
    except ValidationException as e:
        raise HTTPException(status_code=422, detail=e.message)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get("/{blog_id}", response_model=ApiResponse[BlogGenerateResponse])
async def get_blog(
    blog_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """Retrieve a specific generated blog post by ID."""
    try:
        service = BlogContainer.get_blog_service(db)
        result = await service.execute(GetBlogQuery(blog_id=blog_id, user_id=user_id))
        return ApiResponse.ok(BlogRestMapper.to_response(result))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except AppException as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
