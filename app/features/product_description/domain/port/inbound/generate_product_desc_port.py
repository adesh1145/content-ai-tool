from __future__ import annotations

from app.common.port.inbound.use_case import UseCase
from app.features.product_description.application.command.generate_product_command import GenerateProductCommand
from app.features.product_description.application.result.product_result import ProductResult


class GenerateProductDescPort(UseCase[GenerateProductCommand, ProductResult]):
    """Inbound port for generating product descriptions."""

    ...
