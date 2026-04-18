"""Maps EmailResult (application) → GenerateEmailResponse (presentation)."""

from __future__ import annotations

from app.features.email_writer.application.result.email_result import EmailResult
from app.features.email_writer.presentation.rest.dto.response import GenerateEmailResponse


class EmailRestMapper:
    @staticmethod
    def to_response(result: EmailResult) -> GenerateEmailResponse:
        return GenerateEmailResponse(
            email_id=result.email_id,
            email_type=result.email_type,
            subject_line=result.subject_line,
            body=result.body,
            tokens_used=result.tokens_used,
        )
