"""
TravelOS - Trip Endpoint Tests
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_trip(client: AsyncClient, auth_headers: dict):
    """Create a trip successfully."""
    response = await client.post(
        "/api/v1/trips",
        json={
            "title": "Japón 2026",
            "destination": "Tokyo, Japan",
            "budget": 2500.0,
            "currency": "USD",
            "start_date": "2026-10-01",
            "end_date": "2026-10-05",
            "travelers_count": 2,
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Japón 2026"
    assert data["destination"] == "Tokyo, Japan"
    assert data["budget"] == 2500.0
    assert data["status"] == "planning"
    assert data["travelers_count"] == 2


@pytest.mark.asyncio
async def test_create_trip_unauthorized(client: AsyncClient):
    """Creating a trip without auth fails."""
    response = await client.post(
        "/api/v1/trips",
        json={
            "title": "Test",
            "destination": "Nowhere",
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_trips(client: AsyncClient, auth_headers: dict):
    """List trips for user."""
    # Create two trips
    await client.post(
        "/api/v1/trips",
        json={"title": "Trip 1", "destination": "Paris"},
        headers=auth_headers,
    )
    await client.post(
        "/api/v1/trips",
        json={"title": "Trip 2", "destination": "Rome"},
        headers=auth_headers,
    )

    # List
    response = await client.get("/api/v1/trips", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_trip_detail(client: AsyncClient, auth_headers: dict):
    """Get trip with full details."""
    # Create
    response = await client.post(
        "/api/v1/trips",
        json={"title": "Detail Trip", "destination": "Berlin"},
        headers=auth_headers,
    )
    trip_id = response.json()["id"]

    # Get detail
    response = await client.get(f"/api/v1/trips/{trip_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Detail Trip"
    assert "days" in data


@pytest.mark.asyncio
async def test_update_trip(client: AsyncClient, auth_headers: dict):
    """Update trip fields."""
    # Create
    response = await client.post(
        "/api/v1/trips",
        json={"title": "Old Title", "destination": "Madrid"},
        headers=auth_headers,
    )
    trip_id = response.json()["id"]

    # Update
    response = await client.put(
        f"/api/v1/trips/{trip_id}",
        json={"title": "New Title", "budget": 1000.0},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["budget"] == 1000.0


@pytest.mark.asyncio
async def test_delete_trip(client: AsyncClient, auth_headers: dict):
    """Delete a trip."""
    # Create
    response = await client.post(
        "/api/v1/trips",
        json={"title": "Delete Me", "destination": "Nowhere"},
        headers=auth_headers,
    )
    trip_id = response.json()["id"]

    # Delete
    response = await client.delete(f"/api/v1/trips/{trip_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify gone
    response = await client.get(f"/api/v1/trips/{trip_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_trip_not_found(client: AsyncClient, auth_headers: dict):
    """Accessing non-existent trip returns 404."""
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await client.get(f"/api/v1/trips/{fake_id}", headers=auth_headers)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_trip_invalid_dates(client: AsyncClient, auth_headers: dict):
    """End date before start date fails."""
    response = await client.post(
        "/api/v1/trips",
        json={
            "title": "Bad Dates",
            "destination": "Test",
            "start_date": "2026-10-10",
            "end_date": "2026-10-01",
        },
        headers=auth_headers,
    )
    assert response.status_code == 422
