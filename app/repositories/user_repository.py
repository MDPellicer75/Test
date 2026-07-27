"""
TravelOS - User Repository
Data access layer for users and travel DNA.
"""

from uuid import UUID
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.travel_dna import TravelDNA


class UserRepository:
    """Handles all database operations for User and TravelDNA."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── User CRUD ──────────────────────────────────────

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Create a new user."""
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self, user: User, **kwargs) -> User:
        """Update user fields."""
        for key, value in kwargs.items():
            if value is not None and hasattr(user, key):
                setattr(user, key, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """Delete a user."""
        await self.db.delete(user)
        await self.db.flush()

    async def email_exists(self, email: str) -> bool:
        """Check if email is already registered."""
        result = await self.db.execute(select(User.id).where(User.email == email))
        return result.scalar_one_or_none() is not None

    # ─── Travel DNA ─────────────────────────────────────

    async def get_travel_dna(self, user_id: UUID) -> Optional[TravelDNA]:
        """Get user's travel personality profile."""
        result = await self.db.execute(
            select(TravelDNA).where(TravelDNA.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_travel_dna(self, user_id: UUID) -> TravelDNA:
        """Create default travel DNA for a new user."""
        dna = TravelDNA(user_id=user_id)
        self.db.add(dna)
        await self.db.flush()
        await self.db.refresh(dna)
        return dna

    async def update_travel_dna(self, dna: TravelDNA, **kwargs) -> TravelDNA:
        """Update travel DNA scores."""
        for key, value in kwargs.items():
            if value is not None and hasattr(dna, key):
                setattr(dna, key, value)
        await self.db.flush()
        await self.db.refresh(dna)
        return dna
