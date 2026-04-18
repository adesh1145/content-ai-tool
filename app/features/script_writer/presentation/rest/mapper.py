"""Maps ScriptResult (application) → ScriptGenerateResponse (presentation)."""

from __future__ import annotations

from app.features.script_writer.application.result.script_result import ScriptResult
from app.features.script_writer.presentation.rest.dto.response import ScriptGenerateResponse


class ScriptRestMapper:
    @staticmethod
    def to_response(result: ScriptResult) -> ScriptGenerateResponse:
        return ScriptGenerateResponse(
            script_id=result.script_id,
            script_format=result.script_format,
            topic=result.topic,
            script_text=result.script_text,
            word_count=result.word_count,
            estimated_duration_seconds=result.estimated_duration_seconds,
            tokens_used=result.tokens_used,
        )
