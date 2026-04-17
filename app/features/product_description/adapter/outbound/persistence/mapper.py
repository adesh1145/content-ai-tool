from __future__ import annotations

import json

from app.common.domain.value_objects import GenerationStatus, Language, Tone
from app.features.product_description.adapter.outbound.persistence.entity import ProductDescriptionModel
from app.features.product_description.domain.model.product_description import ProductDescription


class ProductDescriptionMapper:
    """Bidirectional mapping between ProductDescription aggregate and SQLAlchemy model."""

    @staticmethod
    def to_domain(model: ProductDescriptionModel) -> ProductDescription:
        features = json.loads(model.features_json) if model.features_json else []
        return ProductDescription(
            id=model.id,
            user_id=model.user_id,
            product_name=model.product_name,
            category=model.category,
            features=features,
            description=model.description,
            tone=Tone(model.tone),
            language=Language(model.language),
            status=GenerationStatus(model.status),
            tokens_used=model.tokens_used,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @staticmethod
    def to_model(entity: ProductDescription) -> ProductDescriptionModel:
        return ProductDescriptionModel(
            id=entity.id,
            user_id=entity.user_id,
            product_name=entity.product_name,
            category=entity.category,
            features_json=json.dumps(entity.features or []),
            description=entity.description,
            tone=entity.tone.value,
            language=entity.language.value,
            status=entity.status.value,
            tokens_used=entity.tokens_used,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def update_model(model: ProductDescriptionModel, entity: ProductDescription) -> None:
        model.product_name = entity.product_name
        model.category = entity.category
        model.features_json = json.dumps(entity.features or [])
        model.description = entity.description
        model.tone = entity.tone.value
        model.language = entity.language.value
        model.status = entity.status.value
        model.tokens_used = entity.tokens_used
