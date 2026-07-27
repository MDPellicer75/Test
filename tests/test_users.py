"""
TravelOS - User Endpoint Tests
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_profile(client: AsyncClient, auth_headers: dict):
    """Get current user profile."""
    response = await client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "name" in data
    assert data["language"] == "es"


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient, auth_headers: dict):
    """Update user profile."""
    response = await client.put(
        "/api/v1/users/me",
        json={"name": "Nombre Nuevo", "country": "Argentina"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Nombre Nuevo"
    assert data["country"] == "Argentina"


@pytest.mark.asyncio
async def test_get_travel_dna(client: AsyncClient, auth_headers: dict):
    """Get travel DNA (created on registration)."""
    response = await client.get("/api/v1/users/me/dna", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    # Default values
    assert data["food_score"] == 0.5
    assert data["budget_level"] == 3
    assert data["max_walking_km"] == 10.0


@pytest.mark.asyncio
async def test_update_travel_dna(client: AsyncClient, auth_headers: dict):
    """Update travel personality scores."""
    response = await client.put(
        "/api/v1/users/me/dna",
        json={
            "food_score": 0.9,
            "museum_score": 0.2,
            "nature_score": 0.8,
            "budget_level": 2,
            "max_walking_km": 15.0,
            "dietary_preferences": "vegetariano",
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["food_score"] == 0.9
    assert data["museum_score"] == 0.2
    assert data["nature_score"] == 0.8
    assert data["budget_level"] == 2
    assert data["max_walking_km"] == 15.0
    assert data["dietary_preferences"] == "vegetariano"


@pytest.mark.asyncio
async def test_get_profile_unauthorized(client: AsyncClient):
    """Accessing profile without token fails."""
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 403
