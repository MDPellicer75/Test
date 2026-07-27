"""
TravelOS - Auth Service
Business logic for registration, login, and token refresh.
"""

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.schemas.token import TokenResponse


class AuthService:
    """Handles authentication business logic."""

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, data: UserRegisterRequest) -> TokenResponse:
        """
        Register a new user.
        Returns access + refresh tokens.
        """
        # Check if email already exists
        if await self.repo.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una cuenta con este email",
            )

        # Create user
        user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            name=data.name,
            language=data.language,
            country=data.country,
        )
        user = await self.repo.create(user)

        # Create default Travel DNA
        await self.repo.create_travel_dna(user.id)

        # Generate tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def login(self, data: UserLoginRequest) -> TokenResponse:
        """
        Authenticate user with email/password.
        Returns access + refresh tokens.
        """
        user = await self.repo.get_by_email(data.email)

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cuenta desactivada",
            )

        # Generate tokens
        access_token = create_access_token(user.id, user.email)
        refresh_token = create_refresh_token(user.id, user.email)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """
        Get a new access token using a valid refresh token.
        """
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token type inválido. Se espera refresh token.",
            )

        user_id = UUID(payload["sub"])
        email = payload["email"]

        # Verify user still exists and is active
        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado o desactivado",
            )

        # Generate new tokens
        new_access = create_access_token(user.id, user.email)
        new_refresh = create_refresh_token(user.id, user.email)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
        )
