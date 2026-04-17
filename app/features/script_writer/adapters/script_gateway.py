from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.features.script_writer.drivers.models import ScriptModel
from app.features.script_writer.use_cases.interfaces.script_interfaces import IScriptGateway


class ScriptGateway(IScriptGateway):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, script_data: dict[str, Any]) -> dict[str, Any]:
        script = ScriptModel(**script_data)
        self.session.add(script)
        await self.session.commit()
        await self.session.refresh(script)
        
        return {
            "script_id": script.id,
            "format": script.format,
            "topic": script.topic,
            "script_text": script.script_text,
            "estimated_duration_seconds": script.estimated_duration_seconds,
            "tokens_used": script.tokens_used,
            "status": script.status,
            "created_at": script.created_at,
        }
