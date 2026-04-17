from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.email_writer.drivers.models import EmailModel
from app.features.email_writer.use_cases.interfaces.email_interfaces import IEmailGateway


class EmailGateway(IEmailGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, email_data: dict[str, Any]) -> dict[str, Any]:
        email = EmailModel(**email_data)
        self.session.add(email)
        await self.session.commit()
        await self.session.refresh(email)
        
        return {
            "email_id": email.id,
            "email_type": email.email_type,
            "subject": email.subject,
            "body": email.body,
            "tokens_used": email.tokens_used,
            "status": email.status,
            "created_at": email.created_at,
        }
