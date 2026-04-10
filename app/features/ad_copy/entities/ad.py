"""
app/features/ad_copy/entities/ad.py
"""

from __future__ import annotations
from dataclasses import dataclass, field
from app.core.entities.base_entity import BaseEntity
from app.core.entities.value_objects import AdPlatform, GenerationStatus, Tone


@dataclass
class AdVariation:
    headline: str = ""
    body: str = ""
    cta: str = ""


@dataclass
class Ad(BaseEntity):
    user_id: str = ""
    platform: AdPlatform = AdPlatform.GOOGLE
    product_or_service: str = ""
    target_audience: str = ""
    unique_selling_point: str = ""
    tone: Tone = Tone.PERSUASIVE
    variations: list[AdVariation] = field(default_factory=list)
    status: GenerationStatus = GenerationStatus.PENDING
    tokens_used: int = 0
