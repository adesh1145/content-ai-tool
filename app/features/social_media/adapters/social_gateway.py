from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.social_media.drivers.models import SocialPostModel
from app.features.social_media.use_cases.interfaces.social_interfaces import ISocialGateway


class SocialGateway(ISocialGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, post_data: dict[str, Any]) -> dict[str, Any]:
        post = SocialPostModel(**post_data)
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        
        return {
            "post_id": post.id,
            "platform": post.platform,
            "topic": post.topic,
            "caption": post.caption,
            "hashtags": post.hashtags,
            "char_count": post.char_count,
            "tokens_used": post.tokens_used,
            "status": post.status,
            "created_at": post.created_at,
        }
