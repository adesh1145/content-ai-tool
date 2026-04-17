from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.ad_copy.drivers.models import AdCopyModel
from app.features.ad_copy.use_cases.interfaces.ad_interfaces import IAdGateway


class AdGateway(IAdGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, ad_data: dict[str, Any]) -> dict[str, Any]:
        ad_copy = AdCopyModel(**ad_data)
        self.session.add(ad_copy)
        await self.session.commit()
        await self.session.refresh(ad_copy)
        
        return {
            "ad_id": ad_copy.id,
            "platform": ad_copy.platform,
            "product": ad_copy.product,
            "variations": ad_copy.variations,
            "tokens_used": ad_copy.tokens_used,
            "status": ad_copy.status,
            "created_at": ad_copy.created_at,
        }
