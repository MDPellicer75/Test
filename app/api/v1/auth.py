"""
TravelOS - Auth Endpoints
Registration, login, and token refresh.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.schemas.token import TokenResponse, TokenRefreshRequest

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(
    data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user.
    Returns access and refresh tokens.
    """
    service = AuthService(db)
    return await service.register(data)


@router.post("/login", response_model=TokenResponse)
async def login(
    data: UserLoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate with email and password.
    Returns access and refresh tokens.
    """
    service = AuthService(db)
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: TokenRefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Get new access token using a valid refresh token.
    """
    service = AuthService(db)
    return await service.refresh(data.refresh_token)
