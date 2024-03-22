import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models import Base


class ReferralCodeORM(Base):
    __tablename__ = "referral_code"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(nullable=False)

    life_time: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)


class ReferrerReferralORM(Base):
    __tablename__ = "referrer_referral"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, nullable=False, default=uuid.uuid4)
    referral_code_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    referrer_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    referral_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
