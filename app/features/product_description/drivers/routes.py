"""
app/features/product_description/drivers/routes.py
─────────────────────────────────────────────────────────────
FastAPI routes for Product Description Generator.
POST /content/product-description
"""

from __future__ import annotations
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.response import APIResponse
from app.features.product_description.adapters.schemas import ProductDescRequest, ProductDescResponse
from app.features.product_description.drivers.ai.product_chain import ProductDescAIService
from app.infrastructure.db.connection import get_db_session

router = APIRouter(prefix="/content/product-description", tags=["Product Description"])


@router.post("", response_model=APIResponse[ProductDescResponse], status_code=201)
async def generate_product_description(
    body: ProductDescRequest,
    db: AsyncSession = Depends(get_db_session),
):
    """
    Generate an ecommerce product description using the F-A-B framework.
    Converts technical features into customer benefits.
    """
    try:
        ai = ProductDescAIService()
        result = await ai.generate(
            product_name=body.product_name,
            category=body.category,
            features=body.features,
            tone=body.tone,
            target_audience=body.target_audience,
            language=body.language,
            word_count=body.word_count,
        )
        return APIResponse.ok(
            ProductDescResponse(
                product_id=str(uuid.uuid4()),
                product_name=body.product_name,
                description=result["description"],
                word_count=result["word_count"],
                tokens_used=result["word_count"] * 2,
            ),
            message="Product description generated successfully.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e!s}")
