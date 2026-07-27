"""
TravelOS - Auth Endpoint Tests
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    """Register a new user successfully."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "nuevo@travelos.com",
            "password": "SecurePass123!",
            "name": "Viajero Nuevo",
            "language": "es",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Registering with an existing email fails."""
    payload = {
        "email": "duplicado@travelos.com",
        "password": "SecurePass123!",
        "name": "User 1",
    }
    # First registration
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201

    # Second registration with same email
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient):
    """Registration with short password fails."""
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "weak@travelos.com",
            "password": "123",
            "name": "Weak User",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Login with correct credentials."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@travelos.com",
            "password": "SecurePass123!",
            "name": "Login User",
        },
    )

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@travelos.com",
            "password": "SecurePass123!",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Login with wrong password fails."""
    # Register first
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong@travelos.com",
            "password": "SecurePass123!",
            "name": "Wrong User",
        },
    )

    # Login with wrong password
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong@travelos.com",
            "password": "WrongPassword!",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Login with non-existent email fails."""
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "noexiste@travelos.com",
            "password": "Whatever123!",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token(client: AsyncClient):
    """Refresh token returns new access token."""
    # Register
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "refresh@travelos.com",
            "password": "SecurePass123!",
            "name": "Refresh User",
        },
    )
    refresh_token = response.json()["refresh_token"]

    # Refresh
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
