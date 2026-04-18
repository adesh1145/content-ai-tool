from __future__ import annotations

from abc import abstractmethod

from app.common.port.inbound.use_case import UseCase
from app.features.seo_optimizer.application.command.analyze_seo_command import (
    AnalyzeSEOCommand,
)
from app.features.seo_optimizer.application.result.seo_analysis_result import (
    SEOAnalysisResult,
)


class IAnalyzeSEO(UseCase[AnalyzeSEOCommand, SEOAnalysisResult]):
    """Input port: run comprehensive SEO analysis on content."""

    @abstractmethod
    async def execute(self, input_data: AnalyzeSEOCommand) -> SEOAnalysisResult: ...
