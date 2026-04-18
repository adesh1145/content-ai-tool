from __future__ import annotations

from abc import abstractmethod

from app.common.port.inbound.use_case import UseCase
from app.features.script_writer.application.command.generate_script_command import (
    GenerateScriptCommand,
)
from app.features.script_writer.application.result.script_result import ScriptResult


class IGenerateScript(UseCase[GenerateScriptCommand, ScriptResult]):
    """Input port: generate a script from a command."""

    @abstractmethod
    async def execute(self, input_data: GenerateScriptCommand) -> ScriptResult: ...
