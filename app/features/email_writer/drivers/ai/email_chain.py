"""
app/features/email_writer/drivers/ai/email_chain.py
─────────────────────────────────────────────────────────────
LangChain chains for email writing.

Types:
  - Cold Email: AIDA framework, personalised opener
  - Newsletter: Story → Value → CTA structure
  - Follow-up: Short, direct, action-oriented
  - Welcome: Warm, onboarding-focused
"""

from __future__ import annotations
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from app.infrastructure.ai.llm_factory import get_llm_provider


EMAIL_SYSTEM_PROMPTS = {
    "cold_email": (
        "You are an expert cold email copywriter. Use the AIDA framework. "
        "Write a highly personalised, non-spammy cold email. Keep it under 150 words. "
        "Start with a personalised opener (not 'Hope this finds you well'). "
        "Make the value proposition crystal clear. End with ONE soft CTA. "
        "Return a JSON object with keys: subject, body."
    ),
    "newsletter": (
        "You are a newsletter writer. Write an engaging newsletter in Story → Value → CTA format. "
        "Start with a hook story, deliver actionable value, end with a clear CTA. "
        "Keep it scannable with short paragraphs. "
        "Return a JSON object with keys: subject, body."
    ),
    "followup": (
        "You are a sales follow-up expert. Write a brief, polite, non-pushy follow-up email. "
        "Reference the previous interaction. Add new value. Keep under 80 words. "
        "Return a JSON object with keys: subject, body."
    ),
    "welcome": (
        "You are an onboarding email specialist. Write a warm, exciting welcome email. "
        "Make the subscriber feel valued. Tell them what to expect. Include 1-2 next steps. "
        "Return a JSON object with keys: subject, body."
    ),
}


class EmailAIService:
    def __init__(self) -> None:
        provider = get_llm_provider()
        from app.infrastructure.ai.llm_factory import OpenAIProvider, AnthropicProvider
        if isinstance(provider, (OpenAIProvider, AnthropicProvider)):
            self._llm = provider.get_langchain_llm()
        else:
            raise RuntimeError("Unsupported provider")

    async def generate(
        self,
        email_type: str,
        recipient_name: str,
        sender_company: str,
        topic: str,
        tone: str,
        language: str,
        context: str = "",
    ) -> dict:
        system = EMAIL_SYSTEM_PROMPTS.get(email_type, EMAIL_SYSTEM_PROMPTS["cold_email"])

        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", (
                "Recipient: {recipient_name}\n"
                "Your company/product: {sender_company}\n"
                "Email topic/goal: {topic}\n"
                "Tone: {tone}\n"
                "Language: {language}\n"
                "Context/notes: {context}\n\n"
                "Write the email. Return ONLY valid JSON: {{\"subject\": \"...\", \"body\": \"...\"}}"
            )),
        ])

        chain = prompt | self._llm | StrOutputParser()
        raw = await chain.ainvoke({
            "recipient_name": recipient_name,
            "sender_company": sender_company,
            "topic": topic,
            "tone": tone,
            "language": language,
            "context": context or "None provided",
        })

        import json, re
        try:
            json_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass

        return {"subject": f"Re: {topic}", "body": raw}
