"""
TravelOS - Destination Schemas
ALL information about a destination. Everything the traveler needs to decide.
"""

from datetime import date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field


# ─── VUELOS ─────────────────────────────────────────────

class FlightOption(BaseModel):
    """A single flight option."""
    airline: str
    flight_number: Optional[str] = None
    origin_airport: str
    origin_city: str
    destination_airport: str
    destination_city: str
    departure_time: str
    arrival_time: str
    duration_hours: float
    stops: int  # 0 = directo
    stop_cities: List[str] = []
    price_usd: float
    price_local: Optional[float] = None
    currency: str = "USD"
    baggage_included: bool
    baggage_kg: Optional[int] = None
    cabin_class: str = "economy"  # economy, premium, business, first
    booking_url: Optional[str] = None
    # Comparisons
    is_cheapest: bool = False
    is_fastest: bool = False
    price_difference_vs_cheapest: float = 0
    time_difference_vs_fastest_hours: float = 0


class FlightInfo(BaseModel):
    """All flight information for a destination."""
    origin: str
    destination: str
    options: List[FlightOption] = []
    cheapest_price: Optional[float] = None
    fastest_duration_hours: Optional[float] = None
    best_day_to_buy: Optional[str] = None
    avg_price_variation: Optional[str] = None  # "Prices drop 20% on Tuesdays"
    airports_at_destination: List[str] = []
    tips: List[str] = []  # "Book 3 weeks in advance for best prices"


# ─── TRANSPORTE INTERNO ─────────────────────────────────

class TransportRoute(BaseModel):
    """A specific route between two points."""
    from_location: str
    to_location: str
    method: str  # train, metro, bus, taxi, uber, walk, bike
    duration_minutes: int
    cost_usd: float
    cost_local: Optional[float] = None
    frequency: Optional[str] = None  # "Every 5 min", "Every hour"
    notes: Optional[str] = None


class TransportPass(BaseModel):
    """Tourist transport passes."""
    name: str  # "Japan Rail Pass", "Oyster Card"
    price_usd: float
    duration_days: int
    covers: List[str]  # ["trains", "metro", "bus"]
    worth_it_if: str  # "If you travel more than 3 days between cities"
    savings_estimate: Optional[str] = None


class TransportInfo(BaseModel):
    """All transport information for a destination."""
    airport_to_center: List[TransportRoute] = []
    internal_options: List[str] = []  # ["Metro", "Bus", "Taxi", "Bike rental"]
    passes_available: List[TransportPass] = []
    common_routes: List[TransportRoute] = []
    tips: List[str] = []
    best_option_budget: Optional[str] = None
    best_option_comfort: Optional[str] = None
    best_option_speed: Optional[str] = None
    uber_available: bool = True
    bike_rental_available: bool = False
    walkable_city: bool = False


# ─── ALOJAMIENTO ────────────────────────────────────────

class Accommodation(BaseModel):
    """A specific hotel/hostel/airbnb."""
    name: str
    type: str  # hotel, hostel, airbnb, apartment, resort
    zone: str
    price_per_night_usd: float
    rating: float = Field(ge=0, le=5)
    reviews_count: int = 0
    distance_to_center_km: float
    includes_breakfast: bool = False
    includes_wifi: bool = True
    includes_pool: bool = False
    booking_url: Optional[str] = None
    highlights: List[str] = []  # "Rooftop bar", "Near subway"


class Zone(BaseModel):
    """A neighborhood/area recommendation."""
    name: str
    description: str
    why_stay_here: str
    type: str  # tourist, local, nightlife, family, budget
    avg_price_per_night_usd: float
    distance_to_center_km: float
    pros: List[str] = []
    cons: List[str] = []


class AccommodationInfo(BaseModel):
    """All accommodation information."""
    recommended_zones: List[Zone] = []
    options: List[Accommodation] = []
    avg_price_budget: float = 0  # hostel/budget hotel
    avg_price_mid: float = 0
    avg_price_luxury: float = 0
    tips: List[str] = []
    best_booking_platform: Optional[str] = None


# ─── COMIDA ─────────────────────────────────────────────

class Dish(BaseModel):
    """A typical dish."""
    name: str
    description: str
    avg_price_usd: float
    where_to_try: Optional[str] = None
    is_must_try: bool = False
    vegetarian: bool = False
    vegan: bool = False


class Restaurant(BaseModel):
    """A recommended restaurant."""
    name: str
    cuisine: str
    zone: str
    price_range: str  # "$", "$$", "$$$", "$$$$"
    avg_meal_usd: float
    rating: float = Field(ge=0, le=5)
    specialty: Optional[str] = None
    reservation_needed: bool = False
    maps_url: Optional[str] = None


class FoodInfo(BaseModel):
    """All food information."""
    typical_dishes: List[Dish] = []
    restaurants: List[Restaurant] = []
    street_food: List[Dish] = []
    markets: List[str] = []
    avg_meal_budget_usd: float = 0  # street food / cheap
    avg_meal_mid_usd: float = 0
    avg_meal_luxury_usd: float = 0
    tipping_culture: str = ""  # "10-15% expected", "Not customary"
    vegetarian_friendly: bool = True
    halal_available: bool = False
    tips: List[str] = []


# ─── ACTIVIDADES ────────────────────────────────────────

class Activity(BaseModel):
    """A thing to do."""
    name: str
    category: str  # museum, nature, adventure, culture, nightlife, shopping
    description: str
    duration_hours: float
    cost_usd: float  # 0 = free
    is_free: bool = False
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    opening_hours: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    reservation_required: bool = False
    booking_url: Optional[str] = None
    rating: float = Field(default=0, ge=0, le=5)
    time_needed_minutes: int = 60
    is_must_do: bool = False
    best_for: List[str] = []  # ["couples", "families", "solo", "photography"]
    tips: Optional[str] = None


class ActivityInfo(BaseModel):
    """All activities information."""
    must_do: List[Activity] = []  # Top 10 imperdibles
    all_activities: List[Activity] = []
    free_activities: List[Activity] = []
    by_category: dict = {}  # {"museum": [...], "nature": [...]}
    unique_experiences: List[Activity] = []  # "Only here"
    total_count: int = 0
    tips: List[str] = []


# ─── CLIMA ──────────────────────────────────────────────

class MonthClimate(BaseModel):
    """Climate for a specific month."""
    month: str
    avg_temp_celsius: float
    min_temp_celsius: float
    max_temp_celsius: float
    rain_days: int
    humidity_percent: int
    sunshine_hours: float
    is_best_time: bool = False
    what_to_wear: str = ""
    events_this_month: List[str] = []


class ClimateInfo(BaseModel):
    """All climate information."""
    current_temp_celsius: Optional[float] = None
    current_condition: Optional[str] = None
    by_month: List[MonthClimate] = []
    best_months_to_visit: List[str] = []
    worst_months: List[str] = []
    rainy_season: Optional[str] = None
    packing_essentials: List[str] = []
    tips: List[str] = []


# ─── SEGURIDAD / LEGAL ──────────────────────────────────

class SafetyInfo(BaseModel):
    """All safety and legal information."""
    safety_score: int = Field(ge=1, le=10)  # 1=dangerous, 10=very safe
    visa_required: bool = False
    visa_type: Optional[str] = None
    visa_cost_usd: Optional[float] = None
    visa_process: Optional[str] = None
    vaccines_required: List[str] = []
    vaccines_recommended: List[str] = []
    dangerous_zones: List[str] = []
    common_scams: List[str] = []
    emergency_number: str = ""
    police_number: str = ""
    ambulance_number: str = ""
    embassy_address: Optional[str] = None
    embassy_phone: Optional[str] = None
    health_insurance_required: bool = False
    tap_water_safe: bool = False
    lgbtq_friendly: bool = True
    solo_female_safe: bool = True
    tips: List[str] = []


# ─── DINERO ─────────────────────────────────────────────

class MoneyInfo(BaseModel):
    """All money/currency information."""
    local_currency: str
    currency_code: str
    exchange_rate_usd: float  # 1 USD = X local
    where_to_exchange: List[str] = []  # "Airport (worst rate)", "ATM (best rate)"
    cards_accepted: bool = True
    cash_preferred: bool = False
    atm_available: bool = True
    atm_fees: Optional[str] = None
    tipping_expected: bool = False
    tipping_percentage: Optional[str] = None
    # Daily budgets
    budget_backpacker_usd: float = 0  # per day
    budget_mid_usd: float = 0
    budget_comfort_usd: float = 0
    budget_luxury_usd: float = 0
    budget_breakdown: Optional[dict] = None  # {"hotel": 40, "food": 30, "transport": 15, "activities": 15}
    tips: List[str] = []


# ─── COMPARACIONES ──────────────────────────────────────

class TripComparison(BaseModel):
    """Compare different trip lengths/budgets."""
    days: int
    total_cost_budget_usd: float
    total_cost_mid_usd: float
    total_cost_luxury_usd: float
    what_you_can_do: List[str] = []
    what_you_miss: List[str] = []
    recommendation: str = ""


class CostComparison(BaseModel):
    """Compare two options."""
    option_a: str
    option_b: str
    price_difference_usd: float
    time_difference: Optional[str] = None
    comfort_difference: Optional[str] = None
    recommendation: str


class ComparisonInfo(BaseModel):
    """All comparisons to help decide."""
    trip_by_duration: List[TripComparison] = []
    flight_comparisons: List[CostComparison] = []
    hotel_comparisons: List[CostComparison] = []
    transport_comparisons: List[CostComparison] = []
    insights: List[str] = []  # "JR Pass saves $200 if you travel 4+ days"


# ─── ITINERARIOS SUGERIDOS ──────────────────────────────

class SuggestedDayPlan(BaseModel):
    """A suggested day."""
    day_number: int
    title: str
    activities: List[str]
    estimated_cost_usd: float
    walking_km: float
    highlights: str


class SuggestedItinerary(BaseModel):
    """A pre-made itinerary suggestion."""
    title: str  # "Tokyo en 5 días - Cultura y Gastronomía"
    days: int
    style: str  # "budget", "comfort", "luxury", "adventure", "family"
    total_cost_usd: float
    daily_plan: List[SuggestedDayPlan] = []
    best_for: List[str] = []  # ["couples", "first-timers", "foodies"]


# ─── RESPUESTA COMPLETA DEL DESTINO ────────────────────

class DestinationSearchResult(BaseModel):
    """Brief result for search."""
    id: str
    name: str
    country: str
    description: str
    image_url: Optional[str] = None
    avg_cost_per_day_usd: float
    best_months: List[str] = []
    tags: List[str] = []  # ["beach", "culture", "nightlife"]


class DestinationFull(BaseModel):
    """
    THE COMPLETE DESTINATION RESPONSE.
    This is what the traveler sees when they pick a destination.
    EVERYTHING. No exceptions.
    """
    # Basic
    id: str
    name: str
    country: str
    continent: str
    description: str
    tagline: str  # "La capital donde tradición y futuro se encuentran"
    image_urls: List[str] = []
    tags: List[str] = []
    language: str
    time_zone: str
    best_months: List[str] = []

    # ALL sections
    flights: FlightInfo
    transport: TransportInfo
    accommodation: AccommodationInfo
    food: FoodInfo
    activities: ActivityInfo
    climate: ClimateInfo
    safety: SafetyInfo
    money: MoneyInfo
    comparisons: ComparisonInfo
    suggested_itineraries: List[SuggestedItinerary] = []

    # Quick stats
    avg_cost_per_day_usd: float
    best_time_to_visit: str
    min_days_recommended: int
    ideal_days: int


class DestinationSearchRequest(BaseModel):
    """Search for destinations."""
    query: Optional[str] = None  # "Japón", "playa barata", "europa invierno"
    budget_max_usd: Optional[float] = None
    days: Optional[int] = None
    month: Optional[str] = None
    interests: List[str] = []  # ["beach", "culture", "food"]
    from_city: Optional[str] = None  # For flight calculations


class ExploreRequest(BaseModel):
    """Request full info for a destination."""
    destination: str  # "Tokyo, Japan"
    from_city: Optional[str] = None  # "Buenos Aires" (for flights)
    travel_dates_start: Optional[date] = None
    travel_dates_end: Optional[date] = None
    travelers: int = 1
    budget_usd: Optional[float] = None
