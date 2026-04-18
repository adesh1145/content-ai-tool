from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.common.exception.base_exception import AppException
from app.dependencies import get_current_user_id
from app.features.article_writer.presentation.rest.dto.request import (
    GenerateArticleRequest,
)
from app.features.article_writer.presentation.rest.dto.response import (
    ArticleResponse,
)
from app.features.article_writer.application.command.generate_article_command import (
    GenerateArticleCommand,
)
from app.features.article_writer.application.query.get_article_query import (
    GetArticleQuery,
)
from app.features.article_writer.config.container import (
    get_generate_article_service,
    get_get_article_service,
)
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/article", tags=["Article Writer"])


@router.post(
    "",
    response_model=ApiResponse[ArticleResponse],
    status_code=201,
)
async def generate_article(
    body: GenerateArticleRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = get_generate_article_service(db)
        result = await service.execute(
            GenerateArticleCommand(
                user_id=user_id,
                topic=body.topic,
                tone=body.tone,
                language=body.language,
                target_audience=body.target_audience,
                focus_keyword=body.focus_keyword,
                word_count_target=body.word_count_target,
            )
        )
        return ApiResponse.ok(
            ArticleResponse(
                article_id=result.article_id,
                topic=result.topic,
                title=result.title,
                content=result.content,
                meta_title=result.meta_title,
                meta_description=result.meta_description,
                word_count=result.word_count,
                tokens_used=result.tokens_used,
                status=result.status,
            ),
            message="Article generated successfully.",
        )
    except AppException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)


@router.get(
    "/{article_id}",
    response_model=ApiResponse[ArticleResponse],
)
async def get_article(
    article_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        service = get_get_article_service(db)
        result = await service.execute(
            GetArticleQuery(article_id=article_id, user_id=user_id)
        )
        return ApiResponse.ok(
            ArticleResponse(
                article_id=result.article_id,
                topic=result.topic,
                title=result.title,
                content=result.content,
                meta_title=result.meta_title,
                meta_description=result.meta_description,
                word_count=result.word_count,
                tokens_used=result.tokens_used,
                status=result.status,
            )
        )
    except AppException as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
