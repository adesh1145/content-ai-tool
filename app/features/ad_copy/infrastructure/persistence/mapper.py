from __future__ import annotations

import json

from app.common.domain.value_objects import AdPlatform, GenerationStatus, Language, Tone
from app.features.ad_copy.infrastructure.persistence.entity import AdCopyModel
from app.features.ad_copy.domain.model.ad_copy import AdCopy


class AdCopyMapper:
    """Bidirectional mapping between the AdCopy aggregate and the SQLAlchemy model."""

    @staticmethod
    def to_domain(model: AdCopyModel) -> AdCopy:
        variations = json.loads(model.variations_json) if model.variations_json else []
        return AdCopy(
            id=model.id,
            user_id=model.user_id,
            platform=AdPlatform(model.platform),
            product_name=model.product_name,
            product_description=model.product_description,
            target_audience=model.target_audience,
            headline=model.headline,
            primary_text=model.primary_text,
            cta_text=model.cta_text,
            variations=variations,
            tone=Tone(model.tone),
            language=Language(model.language),
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: AdCopy) -> AdCopyModel:
        return AdCopyModel(
            id=entity.id,
            user_id=entity.user_id,
            platform=entity.platform.value,
            product_name=entity.product_name,
            product_description=entity.product_description,
            target_audience=entity.target_audience,
            headline=entity.headline,
            primary_text=entity.primary_text,
            cta_text=entity.cta_text,
            variations_json=json.dumps(entity.variations),
            tone=entity.tone.value,
            language=entity.language.value,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: AdCopyModel, entity: AdCopy) -> None:
        model.platform = entity.platform.value
        model.product_name = entity.product_name
        model.product_description = entity.product_description
        model.target_audience = entity.target_audience
        model.headline = entity.headline
        model.primary_text = entity.primary_text
        model.cta_text = entity.cta_text
        model.variations_json = json.dumps(entity.variations)
        model.tone = entity.tone.value
        model.language = entity.language.value
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
