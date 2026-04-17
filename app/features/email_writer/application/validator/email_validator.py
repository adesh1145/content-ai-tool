from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.email_writer.application.command.generate_email_command import GenerateEmailCommand

_VALID_EMAIL_TYPES = {"cold_email", "newsletter", "followup", "welcome"}


class EmailValidator:
    """Validates email content generation commands."""

    @staticmethod
    def validate(cmd: GenerateEmailCommand) -> None:
        if cmd.email_type not in _VALID_EMAIL_TYPES:
            raise ValidationException(
                f"Email type must be one of: {', '.join(sorted(_VALID_EMAIL_TYPES))}."
            )

        if not cmd.purpose or len(cmd.purpose) < 10:
            raise ValidationException(
                "Purpose must be at least 10 characters long."
            )

        if not cmd.recipient_name:
            raise ValidationException(
                "Recipient name is required."
            )
