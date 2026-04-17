from __future__ import annotations

from app.common.application.base_command import BaseCommand


class GenerateAdCommand(BaseCommand):
    """Command to generate ad copy variations for a given platform."""

    user_id: str = ""
    platform: str = "google"
    product_name: str = ""
    product_description: str = ""
    target_audience: str = ""
    tone: str = "persuasive"
    language: str = "en"
    num_variations: int = 2
