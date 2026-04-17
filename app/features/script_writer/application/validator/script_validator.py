from __future__ import annotations

from app.common.domain.value_objects import ScriptFormat
from app.common.exception.base_exception import ValidationException
from app.features.script_writer.application.command.generate_script_command import (
    GenerateScriptCommand,
)

_VALID_FORMATS = {f.value for f in ScriptFormat}


class ScriptValidator:
    """Validates script generation commands before they enter the use case layer."""

    @staticmethod
    def validate(cmd: GenerateScriptCommand) -> None:
        if cmd.script_format not in _VALID_FORMATS:
            raise ValidationException(
                f"Script format must be one of: {', '.join(sorted(_VALID_FORMATS))}."
            )

        if not cmd.topic or not cmd.topic.strip():
            raise ValidationException("Topic must not be empty.")

        if cmd.duration_seconds <= 0:
            raise ValidationException("Duration must be greater than 0 seconds.")
