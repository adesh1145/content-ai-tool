from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.ad_copy.application.command.generate_ad_command import GenerateAdCommand
from app.features.ad_copy.application.result.ad_result import AdResult


class GenerateAdPort(UseCase[GenerateAdCommand, AdResult]):
    """Inbound port for generating ad copy."""

    ...
