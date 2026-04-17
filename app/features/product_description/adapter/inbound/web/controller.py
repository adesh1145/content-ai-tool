from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.dto.api_response import ApiResponse
from app.dependencies import get_current_user_id
from app.features.product_description.adapter.inbound.web.dto.request import GenerateProductRequest
from app.features.product_description.adapter.inbound.web.dto.response import GenerateProductResponse
from app.features.product_description.application.command.generate_product_command import GenerateProductCommand
from app.features.product_description.config.container import get_generate_product_service
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/product-description", tags=["Product Description"])


@router.post("", response_model=ApiResponse[GenerateProductResponse], status_code=201)
async def generate_product_description(
    body: GenerateProductRequest,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate a product description using the F-A-B framework.

    - **F-A-B**: Feature-Advantage-Benefit framework
    - Produces compelling, conversion-optimized product descriptions
    """
    service = get_generate_product_service(db)
    result = await service.execute(
        GenerateProductCommand(
            user_id=user_id,
            product_name=body.product_name,
            category=body.category,
            features=body.features,
            tone=body.tone,
            target_audience=body.target_audience,
            language=body.language,
            word_count=body.word_count,
        )
    )

    response = GenerateProductResponse(
        product_id=result.product_id,
        description=result.description,
        word_count=result.word_count,
        tokens_used=result.tokens_used,
    )

    return ApiResponse.ok(
        response,
        message=f"Product description generated ({result.word_count} words).",
    )
