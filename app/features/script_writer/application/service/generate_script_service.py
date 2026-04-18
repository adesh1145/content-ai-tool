from __future__ import annotations

from app.common.domain.value_objects import GenerationStatus, Language, ScriptFormat, Tone
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.script_writer.application.command.generate_script_command import (
    GenerateScriptCommand,
)
from app.features.script_writer.application.result.script_result import ScriptResult
from app.features.script_writer.application.validator.script_validator import ScriptValidator
from app.features.script_writer.domain.exception.script_generation_failed import (
    ScriptGenerationFailed,
)
from app.features.script_writer.domain.model.script import Script
from app.features.script_writer.application.port.inbound.generate_script_port import IGenerateScript
from app.features.script_writer.domain.port.outbound.script_ai_port import IScriptAIService
from app.features.script_writer.domain.port.outbound.script_repository_port import (
    IScriptRepository,
)


class GenerateScriptService(IGenerateScript):
    """
    Orchestrates script generation:
      1. Validate command
      2. Create Script aggregate
      3. Call AI service
      4. Complete generation (emits domain event)
      5. Persist aggregate
      6. Publish domain events
    """

    def __init__(
        self,
        script_repo: IScriptRepository,
        script_ai: IScriptAIService,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._script_repo = script_repo
        self._script_ai = script_ai
        self._event_publisher = event_publisher

    async def execute(self, input_data: GenerateScriptCommand) -> ScriptResult:
        ScriptValidator.validate(input_data)

        script = Script(
            user_id=input_data.user_id,
            script_format=ScriptFormat(input_data.script_format),
            topic=input_data.topic,
            tone=Tone(input_data.tone),
            language=Language(input_data.language),
            target_audience=input_data.target_audience,
            duration_seconds=input_data.duration_seconds,
            status=GenerationStatus.PROCESSING,
        )

        try:
            ai_result = await self._script_ai.generate_script(
                script_format=input_data.script_format,
                topic=input_data.topic,
                tone=input_data.tone,
                language=input_data.language,
                target_audience=input_data.target_audience,
                duration_seconds=input_data.duration_seconds,
            )
        except Exception as exc:
            script.fail_generation(str(exc))
            await self._script_repo.save(script)
            raise ScriptGenerationFailed(f"AI service error: {exc}") from exc

        script.complete_generation(
            script_text=ai_result.script_text,
            estimated_duration=ai_result.estimated_duration_seconds,
            tokens=ai_result.word_count * 2,
        )

        await self._script_repo.save(script)
        await self._event_publisher.publish_all(script.collect_events())

        return ScriptResult(
            script_id=script.id,
            script_format=script.script_format.value,
            topic=script.topic,
            script_text=script.script_text,
            word_count=ai_result.word_count,
            estimated_duration_seconds=script.estimated_duration_seconds,
            tokens_used=script.tokens_used,
        )
