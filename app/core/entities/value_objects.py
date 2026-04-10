"""
app/core/entities/value_objects.py
─────────────────────────────────────────────────────────────
Shared value objects and enums used across all features.

Clean Architecture Layer 1: Enterprise Business Rules.
Zero external dependencies — pure Python only.
"""

from __future__ import annotations

from enum import Enum


# ── Content Tone ─────────────────────────────────────────────────────────────

class Tone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    PERSUASIVE = "persuasive"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    FORMAL = "formal"
    FRIENDLY = "friendly"


# ── Language ──────────────────────────────────────────────────────────────────

class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    PORTUGUESE = "pt"


# ── Social Media Platforms ────────────────────────────────────────────────────

class SocialPlatform(str, Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"


# ── Ad Platforms ──────────────────────────────────────────────────────────────

class AdPlatform(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"


# ── Email Types ───────────────────────────────────────────────────────────────

class EmailType(str, Enum):
    COLD_EMAIL = "cold_email"
    NEWSLETTER = "newsletter"
    FOLLOWUP = "followup"
    WELCOME = "welcome"


# ── Script Formats ────────────────────────────────────────────────────────────

class ScriptFormat(str, Enum):
    YOUTUBE = "youtube"
    REEL = "reel"
    PODCAST = "podcast"
    WEBINAR = "webinar"


# ── Content Generation Status ─────────────────────────────────────────────────

class GenerationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ── User Plans ────────────────────────────────────────────────────────────────

class UserPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"
