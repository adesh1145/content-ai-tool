from __future__ import annotations

from app.common.exception.base_exception import AppException


class ProductGenerationFailed(AppException):
    """Raised when the AI service fails to generate a product description."""

    def __init__(self, message: str = "Product description generation failed.") -> None:
        super().__init__(message=message, code="PRODUCT_GENERATION_FAILED", status_code=502)
