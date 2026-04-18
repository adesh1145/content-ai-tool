"""Maps ProductResult (application) → GenerateProductResponse (presentation)."""

from __future__ import annotations

from app.features.product_description.application.result.product_result import ProductResult
from app.features.product_description.presentation.rest.dto.response import GenerateProductResponse


class ProductRestMapper:
    @staticmethod
    def to_response(result: ProductResult) -> GenerateProductResponse:
        return GenerateProductResponse(
            product_id=result.product_id,
            description=result.description,
            word_count=result.word_count,
            tokens_used=result.tokens_used,
        )
