from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.auth.application.command.register_command import RegisterCommand
from app.features.auth.application.result.user_result import UserResult


class IRegisterUser(UseCase[RegisterCommand, UserResult]):
    """Input port for user registration."""
    ...
