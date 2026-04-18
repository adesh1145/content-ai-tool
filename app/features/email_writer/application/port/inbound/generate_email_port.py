from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.email_writer.application.command.generate_email_command import GenerateEmailCommand
from app.features.email_writer.application.result.email_result import EmailResult


class GenerateEmailPort(UseCase[GenerateEmailCommand, EmailResult]):
    """Inbound port for generating email content."""

    ...
