from __future__ import annotations

from app.common.exception.base_exception import ValidationException
from app.features.seo_optimizer.application.command.analyze_seo_command import (
    AnalyzeSEOCommand,
)


class SEOValidator:
    """Validates SEO analysis commands before they enter the use case layer."""

    @staticmethod
    def validate_analyze(cmd: AnalyzeSEOCommand) -> None:
        if not cmd.content or not cmd.content.strip():
            raise ValidationException("Content is required for SEO analysis.")

        if len(cmd.content.strip()) < 100:
            raise ValidationException("Content must be at least 100 characters.")

        if cmd.focus_keyword and len(cmd.focus_keyword) > 100:
            raise ValidationException("Focus keyword must be 100 characters or fewer.")

        if cmd.meta_title and len(cmd.meta_title) > 70:
            raise ValidationException("Meta title must be 70 characters or fewer.")

        if cmd.meta_description and len(cmd.meta_description) > 200:
            raise ValidationException("Meta description must be 200 characters or fewer.")
