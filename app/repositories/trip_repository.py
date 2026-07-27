"""
TravelOS - Trip Repository
Data access layer for trips, days, and activities.
"""

from uuid import UUID
from typing import Optional, List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.trip import Trip, TripDay, Activity, TripStatus


class TripRepository:
    """Handles all database operations for Trip, TripDay, and Activity."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── Trip CRUD ──────────────────────────────────────

    async def get_by_id(self, trip_id: UUID, user_id: UUID) -> Optional[Trip]:
        """Get a trip by ID, ensuring it belongs to the user."""
        result = await self.db.execute(
            select(Trip)
            .options(selectinload(Trip.days).selectinload(TripDay.activities))
            .where(Trip.id == trip_id, Trip.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all_by_user(
        self,
        user_id: UUID,
        status: Optional[TripStatus] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Trip]:
        """Get all trips for a user, optionally filtered by status."""
        query = select(Trip).where(Trip.user_id == user_id)

        if status:
            query = query.where(Trip.status == status)

        query = query.order_by(Trip.created_at.desc()).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def count_by_user(
        self, user_id: UUID, status: Optional[TripStatus] = None
    ) -> int:
        """Count trips for a user."""
        query = select(func.count(Trip.id)).where(Trip.user_id == user_id)
        if status:
            query = query.where(Trip.status == status)
        result = await self.db.execute(query)
        return result.scalar_one()

    async def create(self, trip: Trip) -> Trip:
        """Create a new trip."""
        self.db.add(trip)
        await self.db.flush()
        await self.db.refresh(trip)
        return trip

    async def update(self, trip: Trip, **kwargs) -> Trip:
        """Update trip fields."""
        for key, value in kwargs.items():
            if value is not None and hasattr(trip, key):
                setattr(trip, key, value)
        await self.db.flush()
        await self.db.refresh(trip)
        return trip

    async def delete(self, trip: Trip) -> None:
        """Delete a trip and all its days/activities (cascade)."""
        await self.db.delete(trip)
        await self.db.flush()

    # ─── TripDay CRUD ───────────────────────────────────

    async def add_day(self, day: TripDay) -> TripDay:
        """Add a day to a trip."""
        self.db.add(day)
        await self.db.flush()
        await self.db.refresh(day)
        return day

    async def get_days(self, trip_id: UUID) -> List[TripDay]:
        """Get all days for a trip, ordered by day number."""
        result = await self.db.execute(
            select(TripDay)
            .options(selectinload(TripDay.activities))
            .where(TripDay.trip_id == trip_id)
            .order_by(TripDay.day_number)
        )
        return list(result.scalars().all())

    async def delete_day(self, day: TripDay) -> None:
        """Delete a day and its activities."""
        await self.db.delete(day)
        await self.db.flush()

    # ─── Activity CRUD ──────────────────────────────────

    async def add_activity(self, activity: Activity) -> Activity:
        """Add an activity to a day."""
        self.db.add(activity)
        await self.db.flush()
        await self.db.refresh(activity)
        return activity

    async def get_activities(self, trip_day_id: UUID) -> List[Activity]:
        """Get all activities for a day, ordered."""
        result = await self.db.execute(
            select(Activity)
            .where(Activity.trip_day_id == trip_day_id)
            .order_by(Activity.order, Activity.start_time)
        )
        return list(result.scalars().all())

    async def update_activity(self, activity: Activity, **kwargs) -> Activity:
        """Update an activity."""
        for key, value in kwargs.items():
            if value is not None and hasattr(activity, key):
                setattr(activity, key, value)
        await self.db.flush()
        await self.db.refresh(activity)
        return activity

    async def delete_activity(self, activity: Activity) -> None:
        """Delete an activity."""
        await self.db.delete(activity)
        await self.db.flush()
