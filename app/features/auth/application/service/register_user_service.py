from __future__ import annotations

from app.common.exception.base_exception import ConflictException
from app.common.port.outbound.event_publisher_port import EventPublisherPort
from app.features.auth.application.command.register_command import RegisterCommand
from app.features.auth.application.result.user_result import UserResult
from app.features.auth.application.validator.register_validator import RegisterValidator
from app.features.auth.domain.event.user_registered_event import UserRegisteredEvent
from app.features.auth.domain.model.email import Email
from app.features.auth.domain.model.user import User
from app.features.auth.application.port.inbound.register_user_port import IRegisterUser
from app.features.auth.domain.port.outbound.user_repository_port import IUserRepository
from app.features.auth.domain.service.password_service import PasswordService


class RegisterUserService(IRegisterUser):
    """Register a new user — validates, checks duplicates, persists, publishes events."""

    def __init__(
        self,
        user_repo: IUserRepository,
        event_publisher: EventPublisherPort,
    ) -> None:
        self._user_repo = user_repo
        self._event_publisher = event_publisher

    async def execute(self, input_data: RegisterCommand) -> UserResult:
        RegisterValidator.validate(input_data)

        existing = await self._user_repo.get_by_email(input_data.email.lower())
        if existing:
            raise ConflictException(f"User with email '{input_data.email}' already exists")

        email_vo = Email(input_data.email)
        hashed = PasswordService.hash(input_data.password)

        user = User(
            email=email_vo,
            hashed_password=hashed,
            full_name=input_data.full_name.strip(),
        )

        user.register_event(
            UserRegisteredEvent(
                aggregate_id=user.id,
                email=email_vo.value,
                full_name=input_data.full_name.strip(),
            )
        )

        saved = await self._user_repo.save(user)
        await self._event_publisher.publish_all(saved.collect_events())

        return UserResult(
            user_id=saved.id,
            email=str(saved.email),
            full_name=saved.full_name,
            plan=saved.plan.value,
            is_active=saved.is_active,
        )
