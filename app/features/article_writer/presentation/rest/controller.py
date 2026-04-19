from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.dependencies import get_current_user_id
from app.features.article_writer.presentation.rest.dto.request import (
    GenerateArticleRequest,
)
from app.features.article_writer.presentation.rest.dto.response import (
    ArticleResponse,
)
from app.features.article_writer.presentation.rest.mapper import ArticleRestMapper
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
        ArticleRestMapper.to_response(result),
        message="Article generated successfully.",
    )


@router.get(
    "/{article_id}",
    response_model=ApiResponse[ArticleResponse],
)
async def get_article(
    article_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    service = get_get_article_service(db)
    result = await service.execute(
        GetArticleQuery(article_id=article_id, user_id=user_id)
    )
    return ApiResponse.ok(ArticleRestMapper.to_response(result))

