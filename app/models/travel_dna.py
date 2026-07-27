"""
TravelOS - TravelDNA Model
The AI uses this to understand traveler preferences.
Scores from 0.0 (hates it) to 1.0 (loves it).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TravelDNA(Base):
    """
    Traveler personality profile.
    The AI learns and updates this over time.
    """

    __tablename__ = "travel_dna"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    # Interest scores (0.0 to 1.0)
    food_score: Mapped[float] = mapped_column(Float, default=0.5)
    museum_score: Mapped[float] = mapped_column(Float, default=0.5)
    walking_score: Mapped[float] = mapped_column(Float, default=0.5)
    nightlife_score: Mapped[float] = mapped_column(Float, default=0.5)
    history_score: Mapped[float] = mapped_column(Float, default=0.5)
    nature_score: Mapped[float] = mapped_column(Float, default=0.5)
    photography_score: Mapped[float] = mapped_column(Float, default=0.5)
    adventure_score: Mapped[float] = mapped_column(Float, default=0.5)
    shopping_score: Mapped[float] = mapped_column(Float, default=0.5)
    relaxation_score: Mapped[float] = mapped_column(Float, default=0.5)
    sports_score: Mapped[float] = mapped_column(Float, default=0.5)
    art_score: Mapped[float] = mapped_column(Float, default=0.5)

    # Travel style
    budget_level: Mapped[int] = mapped_column(
        Integer, default=3
    )  # 1=backpacker, 5=luxury
    pace: Mapped[int] = mapped_column(
        Integer, default=3
    )  # 1=very relaxed, 5=non-stop
    planning_style: Mapped[int] = mapped_column(
        Integer, default=3
    )  # 1=spontaneous, 5=planned
    social_level: Mapped[int] = mapped_column(
        Integer, default=3
    )  # 1=solo/quiet, 5=social/groups

    # Physical
    fitness_level: Mapped[int] = mapped_column(
        Integer, default=3
    )  # 1=low, 5=athlete
    max_walking_km: Mapped[float] = mapped_column(Float, default=10.0)

    # Dietary
    dietary_preferences: Mapped[str | None] = mapped_column(
        String(200), nullable=True
    )  # vegetarian, vegan, halal, etc.

    # Metadata
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="travel_dna")

    def __repr__(self) -> str:
        return f"<TravelDNA user={self.user_id}>"
