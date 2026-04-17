from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.product_description.drivers.models import ProductDescModel
from app.features.product_description.use_cases.interfaces.product_interfaces import IProductGateway


class ProductGateway(IProductGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, product_data: dict[str, Any]) -> dict[str, Any]:
        product_desc = ProductDescModel(**product_data)
        self.session.add(product_desc)
        await self.session.commit()
        await self.session.refresh(product_desc)
        
        return {
            "product_id": product_desc.id,
            "product_name": product_desc.product_name,
            "category": product_desc.category,
            "features": product_desc.features,
            "description": product_desc.description,
            "word_count": product_desc.word_count,
            "tokens_used": product_desc.tokens_used,
            "status": product_desc.status,
            "created_at": product_desc.created_at,
        }
