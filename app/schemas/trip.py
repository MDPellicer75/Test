"""
TravelOS - Trip Schemas
"""

from datetime import datetime, date, time
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel, Field

from app.models.trip import TripStatus


# ─── Activity ───────────────────────────────────────────

class ActivityCreate(BaseModel):
    """Create an activity within a day."""

    title: str = Field(max_length=200)
    description: Optional[str] = None
    location_name: Optional[str] = Field(default=None, max_length=300)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    start_time: Optional[time] = None
    duration_minutes: Optional[int] = Field(default=None, ge=0, le=1440)
    cost: Optional[float] = Field(default=None, ge=0)
    currency: str = Field(default="USD", max_length=3)
    category: Optional[str] = Field(default=None, max_length=50)
    booking_url: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = None
    order: int = 0


class ActivityResponse(BaseModel):
    """Activity detail."""

    id: UUID
    title: str
    description: Optional[str] = None
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    start_time: Optional[time] = None
    duration_minutes: Optional[int] = None
    cost: Optional[float] = None
    currency: str
    category: Optional[str] = None
    booking_url: Optional[str] = None
    notes: Optional[str] = None
    order: int

    model_config = {"from_attributes": True}


# ─── TripDay ───────────────────────────────────────────

class TripDayCreate(BaseModel):
    """Create a day plan."""

    date: date
    day_number: int = Field(ge=1)
    notes: Optional[str] = None
    activities: List[ActivityCreate] = []


class TripDayResponse(BaseModel):
    """Day plan with activities."""

    id: UUID
    date: date
    day_number: int
    notes: Optional[str] = None
    activities: List[ActivityResponse] = []

    model_config = {"from_attributes": True}


# ─── Trip ──────────────────────────────────────────────

class TripCreate(BaseModel):
    """Create a new trip."""

    title: str = Field(max_length=200)
    destination: str = Field(max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = Field(default=None, ge=0)
    currency: str = Field(default="USD", max_length=3)
    travelers_count: int = Field(default=1, ge=1, le=50)


class TripUpdate(BaseModel):
    """Update trip fields."""

    title: Optional[str] = Field(default=None, max_length=200)
    destination: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, max_length=3)
    status: Optional[TripStatus] = None
    travelers_count: Optional[int] = Field(default=None, ge=1, le=50)


class TripResponse(BaseModel):
    """Trip summary (list view)."""

    id: UUID
    title: str
    destination: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    currency: str
    status: TripStatus
    travelers_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TripDetailResponse(BaseModel):
    """Full trip with days and activities."""

    id: UUID
    title: str
    destination: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    currency: str
    status: TripStatus
    travelers_count: int
    created_at: datetime
    days: List[TripDayResponse] = []

    model_config = {"from_attributes": True}


# ─── Chat ──────────────────────────────────────────────

class ChatRequest(BaseModel):
    """User sends a message to the AI."""

    trip_id: UUID
    message: str = Field(min_length=1, max_length=2000)


class ChatAction(BaseModel):
    """An action the frontend should execute."""

    type: str  # open_map, replace_activity, add_activity, show_budget, etc.
    data: Optional[dict] = None


class ChatResponse(BaseModel):
    """AI response with optional actions."""

    intent: str
    answer: str
    actions: List[ChatAction] = []
