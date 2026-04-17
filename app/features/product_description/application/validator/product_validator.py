from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.product_description.application.command.generate_product_command import GenerateProductCommand


class ProductValidator:
    """Validates product description generation commands."""

    @staticmethod
    def validate(cmd: GenerateProductCommand) -> None:
        if not cmd.product_name or len(cmd.product_name) < 3:
            raise ValidationException(
                "Product name must be at least 3 characters long."
            )

        if not cmd.features or len(cmd.features) == 0:
            raise ValidationException(
                "At least one product feature is required."
            )

        if cmd.word_count < 50 or cmd.word_count > 2000:
            raise ValidationException(
                "Word count must be between 50 and 2000."
            )
