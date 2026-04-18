from __future__ import annotations

from abc import abstractmethod

from app.common.port.inbound.use_case import UseCase
from app.features.seo_optimizer.application.command.generate_meta_command import (
    GenerateMetaCommand,
)
from app.features.seo_optimizer.application.result.meta_result import MetaResult


class IGenerateMeta(UseCase[GenerateMetaCommand, MetaResult]):
    """Input port: generate SEO meta tags from content."""

    @abstractmethod
    async def execute(self, input_data: GenerateMetaCommand) -> MetaResult: ...
