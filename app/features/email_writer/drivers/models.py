from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class EmailModel(Base):
    __tablename__ = "emails"

    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    email_type: Mapped[str] = mapped_column(String(50), nullable=False)
    recipient_name: Mapped[str] = mapped_column(String(100), nullable=False)
    sender_company: Mapped[str] = mapped_column(String(100), nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="completed")
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
