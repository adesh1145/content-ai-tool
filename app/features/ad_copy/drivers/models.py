from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base_model import Base


class AdCopyModel(Base):
    __tablename__ = "ad_copies"

    user_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)
    platform: Mapped[str] = mapped_column(String(50), nullable=False)
    product: Mapped[str] = mapped_column(String(255), nullable=False)
    variations: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="completed")
    tokens_used: Mapped[int] = mapped_column(Integer, default=0)
