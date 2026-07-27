"""
TravelOS - Trip, TripDay, Activity Models
"""

import uuid
from datetime import datetime, date, time, timezone

from sqlalchemy import (
    String,
    DateTime,
    Date,
    Time,
    Float,
    Integer,
    Text,
    ForeignKey,
    Enum,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.db.base import Base


class TripStatus(str, enum.Enum):
    """Trip lifecycle states."""

    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    destination: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus), default=TripStatus.PLANNING
    )
    travelers_count: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    user = relationship("User", back_populates="trips")
    days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Trip {self.title} -> {self.destination}>"


class TripDay(Base):
    __tablename__ = "trip_days"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    trip_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("trips.id", ondelete="CASCADE"), nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    trip = relationship("Trip", back_populates="days")
    activities = relationship(
        "Activity", back_populates="day", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<TripDay {self.day_number} - {self.date}>"


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    trip_day_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("trip_days.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location_name: Mapped[str | None] = mapped_column(String(300), nullable=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    start_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD")
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    booking_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    day = relationship("TripDay", back_populates="activities")

    def __repr__(self) -> str:
        return f"<Activity {self.title}>"
