from __future__ import annotations

from abc import ABC, abstractmethod

from app.features.social_media.application.command.generate_social_command import (
    GenerateSocialCommand,
)
from app.features.social_media.application.result.social_result import SocialResult


class IGenerateSocialPostPort(ABC):
    @abstractmethod
    async def execute(self, command: GenerateSocialCommand) -> SocialResult: ...
