"""
Driven adapter: LangChain email content generation with email-type-specific system prompts.
Uses the LLM configured in EMAIL_WRITER_LLM from model_config.py.

cold_email  -> Concise, clear CTA, professional
newsletter  -> Informative, engaging, value-driven
followup    -> References previous interaction, gentle nudge
welcome     -> Warm, onboarding-focused, helpful
"""

from __future__ import annotations

import json
import re

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from app.features.email_writer.domain.port.outbound.email_ai_port import EmailAIPort
from app.infrastructure.ai.llm_registry import get_llm_registry
from app.infrastructure.ai.model_config import EMAIL_WRITER_LLM

_TYPE_PROMPTS = {
    "cold_email": (
        "You are a cold email specialist. Write concise, compelling cold emails "
        "that grab attention in the first line and include a clear call-to-action. "
        "Keep the email under 200 words. Be direct and professional."
    ),
    "newsletter": (
        "You are a newsletter copywriter. Write informative, engaging newsletter "
        "emails that provide value to subscribers. Use a conversational tone, "
        "include section headers where appropriate, and end with a clear next step."
    ),
    "followup": (
        "You are a follow-up email expert. Write polite follow-up emails that "
        "reference a previous interaction. Be brief, add a gentle nudge, "
        "and propose a concrete next step. Avoid being pushy."
    ),
    "welcome": (
        "You are an onboarding email specialist. Write warm, welcoming emails "
        "that make new users feel valued. Include a brief overview of key features, "
        "helpful resources, and an encouraging tone for getting started."
    ),
}

_HUMAN_PROMPT = (
    "Recipient: {recipient_name}\n"
    "Company: {company_name}\n"
    "Purpose: {purpose}\n"
    "Tone: {tone}\n"
    "Language: {language}\n"
    "{key_points_section}\n"
    "Generate the email as a JSON object with keys: subject_line, body. "
    "Return ONLY valid JSON, no other text."
)


class EmailAIService(EmailAIPort):
    """Implements EmailAIPort. Model from model_config.py."""

    def __init__(self) -> None:
        step = EMAIL_WRITER_LLM.get_step("generate")
        self._llm = get_llm_registry().get_langchain_llm(step.provider, step.model)

    async def generate(
        self,
        email_type: str,
        recipient_name: str,
        company_name: str,
        purpose: str,
        tone: str,
        language: str,
        key_points: list[str] | None = None,
    ) -> dict:
        system_prompt = _TYPE_PROMPTS.get(email_type, _TYPE_PROMPTS["cold_email"])

        key_points_section = ""
        if key_points:
            points = "\n".join(f"- {p}" for p in key_points)
            key_points_section = f"Key points to include:\n{points}"

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", _HUMAN_PROMPT),
        ])

        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "recipient_name": recipient_name,
            "company_name": company_name or "N/A",
            "purpose": purpose,
            "tone": tone,
            "language": language,
            "key_points_section": key_points_section,
        })

        return self._parse_response(raw)

    @staticmethod
    def _parse_response(raw: str) -> dict:
        try:
            json_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return {
                    "subject_line": data.get("subject_line", ""),
                    "body": data.get("body", ""),
                    "tokens_used": len(raw.split()) * 2,
                }
        except (json.JSONDecodeError, AttributeError):
            pass
        lines = raw.strip().split("\n", 1)
        return {
            "subject_line": lines[0][:100] if lines else "",
            "body": lines[1] if len(lines) > 1 else raw,
            "tokens_used": len(raw.split()) * 2,
        }
