"""
TravelOS - Token Schemas
"""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Returned after login/register."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequest(BaseModel):
    """Request to get a new access token."""

    refresh_token: str
