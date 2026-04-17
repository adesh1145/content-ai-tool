from dataclasses import dataclass

from app.core.interfaces.base_use_case import BaseUseCase
from app.features.script_writer.use_cases.interfaces.script_interfaces import IScriptAIService, IScriptGateway


@dataclass
class GenerateScriptInput:
    user_id: str
    format: str
    topic: str
    tone: str
    target_audience: str
    language: str
    target_duration: int


@dataclass
class GenerateScriptOutput:
    script_id: str
    script_text: str
    estimated_duration_seconds: int
    tokens_used: int


class GenerateScriptUseCase(BaseUseCase[GenerateScriptInput, GenerateScriptOutput]):
    def __init__(self, script_repo: IScriptGateway, ai_service: IScriptAIService) -> None:
        self.script_repo = script_repo
        self.ai_service = ai_service

    async def execute(self, input_data: GenerateScriptInput) -> GenerateScriptOutput:
        # 1. Generate content via AI
        result = await self.ai_service.generate(
            format=input_data.format,
            topic=input_data.topic,
            tone=input_data.tone,
            target_audience=input_data.target_audience,
            language=input_data.language,
            target_duration=input_data.target_duration,
        )

        script_text = result["script"]
        estimated_duration_seconds = result.get("estimated_duration_seconds", input_data.target_duration)
        
        tokens_used = len(script_text.split()) * 2

        # 2. Save to DB
        saved_script = await self.script_repo.save({
            "user_id": input_data.user_id,
            "format": input_data.format,
            "topic": input_data.topic,
            "script_text": script_text,
            "estimated_duration_seconds": estimated_duration_seconds,
            "tokens_used": tokens_used,
        })

        return GenerateScriptOutput(
            script_id=saved_script["script_id"],
            script_text=script_text,
            estimated_duration_seconds=estimated_duration_seconds,
            tokens_used=tokens_used,
        )
