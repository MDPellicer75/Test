"""
TravelOS - Trip Endpoints
CRUD for trips.
"""

from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.services.trip_service import TripService
from app.models.trip import TripStatus
from app.schemas.trip import (
    TripCreate,
    TripUpdate,
    TripResponse,
    TripDetailResponse,
)

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.post("", response_model=TripResponse, status_code=201)
async def create_trip(
    data: TripCreate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Create a new trip."""
    service = TripService(db)
    return await service.create_trip(user_id, data)


@router.get("", response_model=list[TripResponse])
async def list_trips(
    status: Optional[TripStatus] = Query(default=None, description="Filter by status"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """List all trips for the current user."""
    service = TripService(db)
    return await service.list_trips(user_id, status_filter=status, limit=limit, offset=offset)


@router.get("/{trip_id}", response_model=TripDetailResponse)
async def get_trip(
    trip_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get a trip with all days and activities."""
    service = TripService(db)
    return await service.get_trip(trip_id, user_id)


@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: UUID,
    data: TripUpdate,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update a trip."""
    service = TripService(db)
    return await service.update_trip(trip_id, user_id, data)


@router.delete("/{trip_id}", status_code=204)
async def delete_trip(
    trip_id: UUID,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Delete a trip and all its data."""
    service = TripService(db)
    await service.delete_trip(trip_id, user_id)
