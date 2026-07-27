"""
TravelOS - Destination Explorer Endpoints
The FIRST thing the traveler uses.
Shows EVERYTHING about a destination before they commit.
"""

from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.agents.destination_agent import DestinationAgent
from app.schemas.destination import (
    DestinationSearchResult,
    DestinationFull,
    ExploreRequest,
)

router = APIRouter(prefix="/destinations", tags=["Destinations"])



@router.post("/explore", response_model=None)
async def explore_destination(
    data: ExploreRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    THE MAIN ENDPOINT.

    The traveler picks a destination and gets EVERYTHING:
    - Flights (all options, cheapest, fastest, comparisons)
    - Transport (all routes, passes, costs, best options)
    - Accommodation (zones, prices, pros/cons)
    - Food (dishes, restaurants, markets, prices)
    - Activities (must-do, free, unique, by category)
    - Climate (12 months, best time, what to pack)
    - Safety (visa, vaccines, scams, emergency)
    - Money (currency, exchange, budgets, tips)
    - Comparisons (3 vs 5 vs 7 vs 10 days, costs)
    - Suggested itineraries (budget, comfort, adventure)

    Example:
    ```json
    {
        "destination": "Tokyo, Japan",
        "from_city": "Buenos Aires",
        "days": 5,
        "travelers": 2,
        "budget_usd": 2500
    }
    ```
    """
    agent = DestinationAgent()
    result = await agent.get_full_destination_info(
        destination=data.destination,
        from_city=data.from_city or "Buenos Aires",
        days=data.travel_dates_start and data.travel_dates_end
        and (data.travel_dates_end - data.travel_dates_start).days + 1
        or 5,
        budget_usd=data.budget_usd,
        travelers=data.travelers,
    )
    return result


@router.post("/more-hotels", response_model=None)
async def get_more_hotels(
    data: ExploreRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    """Get more hotels for a destination."""
    agent = DestinationAgent()
    result = await agent.get_more_hotels(
        destination=data.destination,
        from_city=data.from_city or "Buenos Aires",
        existing_hotels=[],
    )
    return result


@router.post("/hotels-by-zone", response_model=None)
async def get_hotels_by_zone(
    destination: str = Query(description="Destination"),
    zone: str = Query(description="Zone name"),
    user_id: UUID = Depends(get_current_user_id),
):
    """Get 10 hotels for a specific zone."""
    agent = DestinationAgent()
    result = await agent.get_hotels_by_zone(destination=destination, zone=zone)
    return result


@router.post("/transport-route", response_model=None)
async def get_transport_route(
    destination: str = Query(description="Destination"),
    from_point: str = Query(description="From"),
    to_point: str = Query(description="To"),
    user_id: UUID = Depends(get_current_user_id),
):
    """Get transport options between two points including car rental."""
    agent = DestinationAgent()
    result = await agent.get_transport_routes(
        destination=destination, from_point=from_point, to_point=to_point
    )
    return result


@router.post("/more-activities", response_model=None)
async def get_more_activities(
    data: ExploreRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    """Get more activities for a destination."""
    agent = DestinationAgent()
    result = await agent.get_more_activities(
        destination=data.destination,
        existing_activities=[],
    )
    return result


@router.post("/more-flights", response_model=None)
async def get_more_flights(
    data: ExploreRequest,
    user_id: UUID = Depends(get_current_user_id),
):
    """Get more flight options."""
    agent = DestinationAgent()
    result = await agent.get_more_flights(
        destination=data.destination,
        from_city=data.from_city or "Buenos Aires",
    )
    return result


@router.get("/search")
async def search_destinations(
    q: str = Query(description="Search query: 'japon', 'playa barata', 'europa'"),
    budget_max: Optional[float] = Query(default=None, description="Max budget USD"),
    days: Optional[int] = Query(default=None, description="Trip duration"),
    month: Optional[str] = Query(default=None, description="Travel month"),
    user_id: UUID = Depends(get_current_user_id),
):
    """
    Search destinations by text, budget, duration, or month.

    Returns brief cards that the user can tap to get full info.
    """
    # TODO: Connect to real search with database of destinations
    # For now, return curated results based on query
    results = _search_fallback(q, budget_max, days, month)
    return {"query": q, "results": results, "total": len(results)}


@router.get("/popular")
async def popular_destinations(
    user_id: UUID = Depends(get_current_user_id),
):
    """Get popular destinations (trending now)."""
    return {
        "destinations": [
            {
                "id": "tokyo-japan",
                "name": "Tokyo",
                "country": "Japón",
                "description": "Tradición milenaria y tecnología futurista",
                "avg_cost_per_day_usd": 120,
                "best_months": ["Marzo", "Abril", "Octubre"],
                "tags": ["culture", "food", "technology"],
            },
            {
                "id": "paris-france",
                "name": "París",
                "country": "Francia",
                "description": "La ciudad del amor, el arte y la gastronomía",
                "avg_cost_per_day_usd": 150,
                "best_months": ["Abril", "Mayo", "Septiembre"],
                "tags": ["romance", "art", "food", "history"],
            },
            {
                "id": "bali-indonesia",
                "name": "Bali",
                "country": "Indonesia",
                "description": "Templos, arrozales, playas y espiritualidad",
                "avg_cost_per_day_usd": 50,
                "best_months": ["Abril", "Mayo", "Junio"],
                "tags": ["beach", "nature", "spiritual", "budget"],
            },
            {
                "id": "nyc-usa",
                "name": "New York",
                "country": "Estados Unidos",
                "description": "La ciudad que nunca duerme",
                "avg_cost_per_day_usd": 200,
                "best_months": ["Abril", "Mayo", "Octubre"],
                "tags": ["city", "culture", "food", "shopping"],
            },
            {
                "id": "rome-italy",
                "name": "Roma",
                "country": "Italia",
                "description": "Historia viva en cada esquina",
                "avg_cost_per_day_usd": 110,
                "best_months": ["Abril", "Mayo", "Octubre"],
                "tags": ["history", "food", "art", "romance"],
            },
            {
                "id": "cape-town-sa",
                "name": "Cape Town",
                "country": "Sudáfrica",
                "description": "Montañas, viñedos y océano",
                "avg_cost_per_day_usd": 70,
                "best_months": ["Noviembre", "Diciembre", "Febrero"],
                "tags": ["nature", "adventure", "wine", "beach"],
            },
        ]
    }


@router.get("/recommended")
async def recommended_for_me(
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Personalized recommendations based on Travel DNA.
    The AI analyzes what you like and suggests matching destinations.
    """
    from app.repositories.user_repository import UserRepository

    repo = UserRepository(db)
    dna = await repo.get_travel_dna(user_id)

    # Recommend based on DNA scores
    recommendations = []

    if dna:
        if dna.food_score > 0.7:
            recommendations.append({
                "id": "tokyo-japan",
                "name": "Tokyo",
                "country": "Japón",
                "reason": "Te encanta la gastronomía. Tokyo tiene la mayor cantidad de restaurantes Michelin del mundo.",
                "match_score": 0.95,
            })
            recommendations.append({
                "id": "lima-peru",
                "name": "Lima",
                "country": "Perú",
                "reason": "Capital gastronómica de Latinoamérica.",
                "match_score": 0.88,
            })

        if dna.nature_score > 0.7:
            recommendations.append({
                "id": "queenstown-nz",
                "name": "Queenstown",
                "country": "Nueva Zelanda",
                "reason": "Amás la naturaleza. Montañas, lagos, glaciares.",
                "match_score": 0.92,
            })
            recommendations.append({
                "id": "patagonia-arg",
                "name": "Patagonia",
                "country": "Argentina",
                "reason": "Glaciares, bosques, montañas sin multitudes.",
                "match_score": 0.90,
            })

        if dna.adventure_score > 0.7:
            recommendations.append({
                "id": "nepal-ktm",
                "name": "Nepal",
                "country": "Nepal",
                "reason": "Aventura pura. Trekking en el Himalaya.",
                "match_score": 0.93,
            })

        if dna.nightlife_score > 0.7:
            recommendations.append({
                "id": "berlin-germany",
                "name": "Berlín",
                "country": "Alemania",
                "reason": "La mejor vida nocturna de Europa.",
                "match_score": 0.89,
            })

        if dna.history_score > 0.7:
            recommendations.append({
                "id": "rome-italy",
                "name": "Roma",
                "country": "Italia",
                "reason": "2700 años de historia caminable.",
                "match_score": 0.94,
            })

    # Sort by match score
    recommendations.sort(key=lambda x: x.get("match_score", 0), reverse=True)

    return {
        "personalized": True,
        "recommendations": recommendations[:6],
    }


def _search_fallback(
    query: str, budget_max: float, days: int, month: str
) -> list:
    """Simple keyword-based search fallback."""
    all_destinations = [
        {"id": "tokyo-japan", "name": "Tokyo", "country": "Japón", "tags": ["culture", "food", "technology"], "avg_cost_per_day_usd": 120, "best_months": ["Marzo", "Abril", "Octubre"]},
        {"id": "paris-france", "name": "París", "country": "Francia", "tags": ["romance", "art", "food"], "avg_cost_per_day_usd": 150, "best_months": ["Abril", "Mayo", "Septiembre"]},
        {"id": "bali-indonesia", "name": "Bali", "country": "Indonesia", "tags": ["beach", "nature", "budget"], "avg_cost_per_day_usd": 50, "best_months": ["Abril", "Mayo"]},
        {"id": "nyc-usa", "name": "New York", "country": "EEUU", "tags": ["city", "culture", "shopping"], "avg_cost_per_day_usd": 200, "best_months": ["Abril", "Octubre"]},
        {"id": "rome-italy", "name": "Roma", "country": "Italia", "tags": ["history", "food", "art"], "avg_cost_per_day_usd": 110, "best_months": ["Abril", "Octubre"]},
        {"id": "bangkok-thailand", "name": "Bangkok", "country": "Tailandia", "tags": ["food", "temple", "budget", "nightlife"], "avg_cost_per_day_usd": 40, "best_months": ["Noviembre", "Febrero"]},
        {"id": "london-uk", "name": "Londres", "country": "Reino Unido", "tags": ["culture", "history", "shopping"], "avg_cost_per_day_usd": 160, "best_months": ["Mayo", "Septiembre"]},
        {"id": "cancun-mexico", "name": "Cancún", "country": "México", "tags": ["beach", "party", "resort"], "avg_cost_per_day_usd": 80, "best_months": ["Diciembre", "Abril"]},
        {"id": "iceland", "name": "Islandia", "country": "Islandia", "tags": ["nature", "adventure", "aurora"], "avg_cost_per_day_usd": 180, "best_months": ["Junio", "Septiembre"]},
        {"id": "machu-picchu", "name": "Machu Picchu", "country": "Perú", "tags": ["history", "nature", "adventure", "culture"], "avg_cost_per_day_usd": 60, "best_months": ["Mayo", "Septiembre"]},
    ]

    query_lower = query.lower()
    results = []

    for dest in all_destinations:
        # Match by name, country, or tags
        match = (
            query_lower in dest["name"].lower()
            or query_lower in dest["country"].lower()
            or any(query_lower in tag for tag in dest["tags"])
        )

        # Budget filter
        if budget_max and dest["avg_cost_per_day_usd"] > budget_max / (days or 5):
            continue

        if match:
            results.append(dest)

    # If no match, return all (limited)
    if not results:
        results = all_destinations[:5]

    return results
