from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.ad_copy.application.command.generate_ad_command import GenerateAdCommand

_VALID_PLATFORMS = {"google", "facebook"}


class AdValidator:
    """Validates ad copy generation commands."""

    @staticmethod
    def validate(cmd: GenerateAdCommand) -> None:
        if cmd.platform not in _VALID_PLATFORMS:
            raise ValidationException(
                f"Platform must be one of: {', '.join(sorted(_VALID_PLATFORMS))}."
            )

        if not cmd.product_name or len(cmd.product_name) < 3:
            raise ValidationException(
                "Product name must be at least 3 characters long."
            )

        if not cmd.product_description or len(cmd.product_description) < 10:
            raise ValidationException(
                "Product description must be at least 10 characters long."
            )

        if cmd.num_variations < 1 or cmd.num_variations > 5:
            raise ValidationException(
                "Number of variations must be between 1 and 5."
            )
