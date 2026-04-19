from __future__ import annotations

from enum import Enum


class Tone(str, Enum):
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    PERSUASIVE = "persuasive"
    HUMOROUS = "humorous"
    INSPIRATIONAL = "inspirational"
    EDUCATIONAL = "educational"
    FORMAL = "formal"
    FRIENDLY = "friendly"


class Language(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    PORTUGUESE = "pt"


class SocialPlatform(str, Enum):
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"


class AdPlatform(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"


class EmailType(str, Enum):
    COLD_EMAIL = "cold_email"
    NEWSLETTER = "newsletter"
    FOLLOWUP = "followup"
    WELCOME = "welcome"


class ScriptFormat(str, Enum):
    YOUTUBE = "youtube"
    REEL = "reel"
    PODCAST = "podcast"
    WEBINAR = "webinar"


class GenerationStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UserPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"

