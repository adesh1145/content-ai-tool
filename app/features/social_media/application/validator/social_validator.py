from __future__ import annotations

from app.common.domain.value_objects import SocialPlatform
from app.common.exception.base_exception import ValidationException
from app.features.social_media.application.command.generate_social_command import (
    GenerateSocialCommand,
)

VALID_PLATFORMS = {p.value for p in SocialPlatform}


class SocialValidator:
    @staticmethod
    def validate(command: GenerateSocialCommand) -> None:
        if len(command.topic.strip()) < 5:
            raise ValidationException("Topic must be at least 5 characters long.")
        if command.platform not in VALID_PLATFORMS:
            raise ValidationException(
                f"Invalid platform '{command.platform}'. "
                f"Valid platforms: {', '.join(sorted(VALID_PLATFORMS))}"
            )
