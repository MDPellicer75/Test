"""
TravelOS - User Endpoints
Profile and Travel DNA management.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserResponse,
    UserUpdateRequest,
    TravelDNAResponse,
    TravelDNAUpdateRequest,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's profile."""
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    return UserResponse.model_validate(user)


@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdateRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's profile."""
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )

    update_data = data.model_dump(exclude_unset=True)
    user = await repo.update(user, **update_data)
    return UserResponse.model_validate(user)


# ─── Travel DNA ─────────────────────────────────────────

@router.get("/me/dna", response_model=TravelDNAResponse)
async def get_my_travel_dna(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get current user's travel personality profile."""
    repo = UserRepository(db)
    dna = await repo.get_travel_dna(user_id)

    if not dna:
        # Create default if doesn't exist
        dna = await repo.create_travel_dna(user_id)

    return TravelDNAResponse.model_validate(dna)


@router.put("/me/dna", response_model=TravelDNAResponse)
async def update_my_travel_dna(
    data: TravelDNAUpdateRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Update current user's travel personality profile."""
    repo = UserRepository(db)
    dna = await repo.get_travel_dna(user_id)

    if not dna:
        dna = await repo.create_travel_dna(user_id)

    update_data = data.model_dump(exclude_unset=True)
    dna = await repo.update_travel_dna(dna, **update_data)
    return TravelDNAResponse.model_validate(dna)
