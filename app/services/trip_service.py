"""
TravelOS - Trip Service
Business logic for trip management.
"""

from uuid import UUID
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.trip import Trip, TripStatus
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreate, TripUpdate, TripResponse, TripDetailResponse


class TripService:
    """Handles trip business logic."""

    def __init__(self, db: AsyncSession):
        self.repo = TripRepository(db)

    async def create_trip(self, user_id: UUID, data: TripCreate) -> TripResponse:
        """Create a new trip for a user."""
        # Validate dates
        if data.start_date and data.end_date:
            if data.end_date < data.start_date:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="La fecha de fin no puede ser anterior a la fecha de inicio",
                )

        trip = Trip(
            user_id=user_id,
            title=data.title,
            destination=data.destination,
            description=data.description,
            start_date=data.start_date,
            end_date=data.end_date,
            budget=data.budget,
            currency=data.currency,
            travelers_count=data.travelers_count,
        )
        trip = await self.repo.create(trip)
        return TripResponse.model_validate(trip)

    async def get_trip(self, trip_id: UUID, user_id: UUID) -> TripDetailResponse:
        """Get a trip with all days and activities."""
        trip = await self.repo.get_by_id(trip_id, user_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Viaje no encontrado",
            )

        return TripDetailResponse.model_validate(trip)

    async def list_trips(
        self,
        user_id: UUID,
        status_filter: Optional[TripStatus] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[TripResponse]:
        """List all trips for a user."""
        trips = await self.repo.get_all_by_user(
            user_id, status=status_filter, limit=limit, offset=offset
        )
        return [TripResponse.model_validate(t) for t in trips]

    async def update_trip(
        self, trip_id: UUID, user_id: UUID, data: TripUpdate
    ) -> TripResponse:
        """Update a trip."""
        trip = await self.repo.get_by_id(trip_id, user_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Viaje no encontrado",
            )

        # Validate dates if both provided
        start = data.start_date or trip.start_date
        end = data.end_date or trip.end_date
        if start and end and end < start:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La fecha de fin no puede ser anterior a la fecha de inicio",
            )

        update_data = data.model_dump(exclude_unset=True)
        trip = await self.repo.update(trip, **update_data)
        return TripResponse.model_validate(trip)

    async def delete_trip(self, trip_id: UUID, user_id: UUID) -> None:
        """Delete a trip."""
        trip = await self.repo.get_by_id(trip_id, user_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Viaje no encontrado",
            )

        await self.repo.delete(trip)
