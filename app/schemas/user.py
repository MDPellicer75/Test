"""
TravelOS - User Schemas
"""

from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ─── Auth ───────────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    """Registration payload."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=2, max_length=100)
    language: str = Field(default="es", max_length=10)
    country: Optional[str] = Field(default=None, max_length=100)


class UserLoginRequest(BaseModel):
    """Login payload."""

    email: EmailStr
    password: str


# ─── Profile ────────────────────────────────────────────

class UserResponse(BaseModel):
    """Public user profile."""

    id: UUID
    email: str
    name: str
    language: str
    country: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    """Update profile fields."""

    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    language: Optional[str] = Field(default=None, max_length=10)
    country: Optional[str] = Field(default=None, max_length=100)
    photo_url: Optional[str] = Field(default=None, max_length=500)


# ─── Travel DNA ─────────────────────────────────────────

class TravelDNAResponse(BaseModel):
    """User's travel personality profile."""

    food_score: float
    museum_score: float
    walking_score: float
    nightlife_score: float
    history_score: float
    nature_score: float
    photography_score: float
    adventure_score: float
    shopping_score: float
    relaxation_score: float
    sports_score: float
    art_score: float
    budget_level: int
    pace: int
    planning_style: int
    social_level: int
    fitness_level: int
    max_walking_km: float
    dietary_preferences: Optional[str] = None

    model_config = {"from_attributes": True}


class TravelDNAUpdateRequest(BaseModel):
    """Update travel preferences."""

    food_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    museum_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    walking_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    nightlife_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    history_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    nature_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    photography_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    adventure_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    shopping_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    relaxation_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    sports_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    art_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    budget_level: Optional[int] = Field(default=None, ge=1, le=5)
    pace: Optional[int] = Field(default=None, ge=1, le=5)
    planning_style: Optional[int] = Field(default=None, ge=1, le=5)
    social_level: Optional[int] = Field(default=None, ge=1, le=5)
    fitness_level: Optional[int] = Field(default=None, ge=1, le=5)
    max_walking_km: Optional[float] = Field(default=None, ge=0.0, le=50.0)
    dietary_preferences: Optional[str] = Field(default=None, max_length=200)
