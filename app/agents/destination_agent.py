"""
TravelOS - Destination Intelligence Agent
Generates COMPLETE information about any destination.
Uses OpenAI to produce comprehensive travel intelligence.
"""

from openai import AsyncOpenAI
from app.core.config import settings
from app.agents.base_agent import BaseAgent, AgentContext


class DestinationAgent(BaseAgent):
    """
    Generates ALL information about a destination.
    This is the core differentiator of TravelOS.
    """

    async def run(self, context: AgentContext) -> str:
        """Not used directly - use specific methods below."""
        return ""

    async def get_full_destination_info(
        self,
        destination: str,
        from_city: str = "Buenos Aires",
        days: int = 5,
        budget_usd: float = None,
        travelers: int = 1,
    ) -> dict:
        """
        Generate EVERYTHING about a destination.
        Returns structured JSON with all sections.
        """
        prompt = self._build_full_prompt(
            destination, from_city, days, budget_usd, travelers
        )
        return await self._call_ai_json(prompt)


    def _build_full_prompt(
        self,
        destination: str,
        from_city: str,
        days: int,
        budget_usd: float,
        travelers: int,
    ) -> str:
        """Build the mega-prompt for complete destination info."""

        budget_str = f"Presupuesto: USD {budget_usd}" if budget_usd else "Sin presupuesto definido"

        return f"""Sos un experto en viajes con conocimiento enciclopédico.
El viajero quiere ir a: {destination}
Sale desde: {from_city}
Días disponibles: {days}
Viajeros: {travelers}
{budget_str}

Generá un JSON con TODA esta información real y actualizada:

{{
  "basic": {{
    "name": "nombre del destino",
    "country": "país",
    "continent": "continente",
    "description": "descripción de 2-3 oraciones",
    "tagline": "frase corta que lo define",
    "language": "idioma principal",
    "time_zone": "zona horaria (UTC+X)",
    "best_months": ["meses ideales"],
    "tags": ["beach", "culture", etc]
  }},
  "flights": {{
    "options": [
      {{
        "airline": "nombre",
        "origin_airport": "código",
        "destination_airport": "código",
        "duration_hours": X.X,
        "stops": 0,
        "stop_cities": [],
        "price_usd": XXXX,
        "baggage_included": true/false,
        "baggage_kg": XX,
        "is_cheapest": true/false,
        "is_fastest": true/false
      }}
    ],
    "cheapest_price": XXXX,
    "fastest_duration_hours": X.X,
    "best_day_to_buy": "día de la semana",
    "airports_at_destination": ["códigos"],
    "tips": ["consejo 1", "consejo 2"]
  }},
  "transport": {{
    "airport_to_center": [
      {{
        "method": "train/bus/taxi",
        "duration_minutes": XX,
        "cost_usd": XX,
        "frequency": "cada X min",
        "is_fastest": true/false,
        "is_cheapest": true/false,
        "comfort_level": "alto/medio/bajo"
      }}
    ],
    "common_routes": [
      {{
        "from": "lugar A",
        "to": "lugar B",
        "options": [
          {{"method": "metro", "duration_minutes": XX, "cost_usd": XX, "is_best": true}},
          {{"method": "taxi", "duration_minutes": XX, "cost_usd": XX, "is_best": false}}
        ]
      }}
    ],
    "internal_options": ["Metro", "Bus", "Taxi"],
    "passes_available": [
      {{
        "name": "nombre del pase",
        "price_usd": XX,
        "duration_days": X,
        "covers": ["train", "metro"],
        "worth_it_if": "explicación"
      }}
    ],
    "best_option_budget": "descripción completa",
    "best_option_comfort": "descripción completa",
    "best_option_speed": "descripción completa",
    "uber_available": true/false,
    "walkable_city": true/false,
    "tips": ["consejo"]
  }},
  "accommodation": {{
    "recommended_zones": [
      {{
        "name": "barrio",
        "description": "qué es",
        "why_stay_here": "por qué",
        "type": "tourist/local/nightlife/family/budget",
        "avg_price_per_night_usd": XX,
        "pros": ["pro1"],
        "cons": ["con1"]
      }}
    ],
    "hotels": [
      {{
        "name": "nombre real del hotel/hostel",
        "zone": "barrio donde está",
        "type": "hotel/hostel/apartment/boutique/luxury",
        "price_per_night_usd": XX,
        "rating": X.X,
        "highlights": ["wifi", "breakfast", "pool"],
        "best_for": "parejas/solo/familias/mochileros",
        "latitude": XX.XXXX,
        "longitude": XX.XXXX
      }}
    ],
    "avg_price_budget": XX,
    "avg_price_mid": XX,
    "avg_price_luxury": XX,
    "tips": ["consejo"]
  }},
  "food": {{
    "typical_dishes": [
      {{
        "name": "plato",
        "description": "qué es",
        "avg_price_usd": XX,
        "is_must_try": true/false,
        "vegetarian": true/false
      }}
    ],
    "avg_meal_budget_usd": XX,
    "avg_meal_mid_usd": XX,
    "avg_meal_luxury_usd": XX,
    "tipping_culture": "explicación",
    "vegetarian_friendly": true/false,
    "markets": ["mercado 1", "mercado 2"],
    "tips": ["consejo"]
  }},
  "activities": {{
    "must_do": [
      {{
        "name": "actividad",
        "category": "museum/nature/adventure/culture",
        "description": "descripción",
        "duration_hours": X,
        "cost_usd": XX,
        "is_free": true/false,
        "best_time_to_visit": "horario",
        "reservation_required": true/false,
        "rating": X.X,
        "is_must_do": true,
        "best_for": ["couples", "families"]
      }}
    ],
    "free_activities": [lista],
    "unique_experiences": [lista de cosas "solo acá"],
    "total_count": XX,
    "tips": ["consejo"]
  }},
  "climate": {{
    "by_month": [
      {{
        "month": "Enero",
        "avg_temp_celsius": XX,
        "rain_days": X,
        "is_best_time": true/false,
        "what_to_wear": "ropa sugerida"
      }}
    ],
    "best_months_to_visit": ["mes1", "mes2"],
    "rainy_season": "meses",
    "packing_essentials": ["item1", "item2"]
  }},
  "safety": {{
    "safety_score": X,
    "visa_required": true/false,
    "visa_type": "tipo o null",
    "vaccines_required": [],
    "vaccines_recommended": [],
    "dangerous_zones": ["zona"],
    "common_scams": ["estafa"],
    "emergency_number": "número",
    "tap_water_safe": true/false,
    "lgbtq_friendly": true/false,
    "tips": ["consejo"]
  }},
  "money": {{
    "local_currency": "nombre",
    "currency_code": "XXX",
    "exchange_rate_usd": X.XX,
    "cards_accepted": true/false,
    "cash_preferred": true/false,
    "atm_available": true/false,
    "tipping_expected": true/false,
    "budget_backpacker_usd": XX,
    "budget_mid_usd": XX,
    "budget_comfort_usd": XX,
    "budget_luxury_usd": XX,
    "tips": ["consejo"]
  }},
  "comparisons": {{
    "trip_by_duration": [
      {{
        "days": 3,
        "total_cost_mid_usd": XXXX,
        "what_you_can_do": ["cosa1", "cosa2"],
        "what_you_miss": ["cosa perdida"],
        "recommendation": "recomendación"
      }},
      {{
        "days": 5,
        "total_cost_mid_usd": XXXX,
        "what_you_can_do": ["más cosas"],
        "what_you_miss": [],
        "recommendation": "ideal"
      }},
      {{
        "days": 7,
        "total_cost_mid_usd": XXXX,
        "what_you_can_do": ["todo"],
        "what_you_miss": [],
        "recommendation": "si tenés tiempo"
      }}
    ],
    "insights": ["insight útil 1", "insight 2"]
  }},
  "suggested_itineraries": [
    {{
      "title": "Nombre del itinerario",
      "days": X,
      "style": "budget/comfort/luxury/adventure",
      "total_cost_usd": XXXX,
      "daily_plan": [
        {{
          "day_number": 1,
          "title": "Título del día",
          "activities": ["act1", "act2", "act3"],
          "estimated_cost_usd": XX,
          "walking_km": X
        }}
      ],
      "best_for": ["first-timers", "couples"]
    }}
  ],
  "quick_stats": {{
    "avg_cost_per_day_usd": XX,
    "best_time_to_visit": "descripción",
    "min_days_recommended": X,
    "ideal_days": X
  }}
}}

REGLAS:
- Usá datos REALES y actualizados
- Precios reales del mercado actual
- Mínimo 4 opciones de vuelo
- Mínimo 3 zonas de alojamiento
- Mínimo 8 hoteles REALES con nombre, precio, rating y coordenadas
- Incluí desde hostels baratos hasta hoteles de lujo
- Mínimo 8 platos típicos
- Mínimo 8 actividades con coordenadas (latitude, longitude)
- Los 12 meses de clima (solo mes, temp, rain_days, is_best_time, what_to_wear)
- 3 itinerarios sugeridos obligatorios: uno "budget", uno "comfort", uno "luxury"
- Cada itinerario con daily_plan completo
- Comparaciones para 3, 5 y 7 días
- En transporte: ruta aeropuerto-centro con 3 opciones
- Todo en español
- NO inventar URLs
- Sé conciso en descripciones (máximo 15 palabras cada una)
- Respondé SOLO el JSON, sin texto adicional"""


    async def get_hotels_by_zone(self, destination: str, zone: str) -> dict:
        """Get 10 hotels for a specific zone."""
        prompt = f"""Necesito 10 hoteles REALES en la zona "{zone}" de {destination}.

Generá un JSON:
{{
  "zone": "{zone}",
  "hotels": [
    {{
      "name": "nombre real",
      "type": "hotel/hostel/boutique/luxury/apartment",
      "price_per_night_usd": XX,
      "rating": X.X,
      "highlights": ["wifi", "pool", "gym"],
      "best_for": "parejas/familias/negocios/mochileros",
      "stars": X,
      "latitude": XX.XXXX,
      "longitude": XX.XXXX
    }}
  ]
}}

REGLAS:
- 10 hoteles REALES que existan
- Coordenadas REALES de cada hotel
- Variedad: desde hostels hasta 5 estrellas
- Precios realistas del mercado actual
- Respondé SOLO JSON"""
        return await self._call_ai_json(prompt)

    async def get_transport_routes(self, destination: str, from_point: str, to_point: str) -> dict:
        """Get transport options between two points."""
        prompt = f"""Necesito opciones de transporte en {destination} desde "{from_point}" hasta "{to_point}".

Generá un JSON:
{{
  "from": "{from_point}",
  "to": "{to_point}",
  "options": [
    {{
      "method": "Metro/Taxi/Bus/Uber/Tren/Caminando",
      "duration_minutes": XX,
      "cost_usd": XX,
      "details": "línea X, dirección Y",
      "is_fastest": true/false,
      "is_cheapest": true/false,
      "comfort_level": "alto/medio/bajo"
    }}
  ],
  "car_rental": {{
    "available": true,
    "agencies": [
      {{
        "name": "Hertz/Avis/Enterprise",
        "price_per_day_usd": XX,
        "location": "dirección",
        "latitude": XX.XXXX,
        "longitude": XX.XXXX
      }}
    ],
    "recommended": true/false,
    "why": "razón"
  }}
}}

REGLAS:
- Datos reales
- Mínimo 4 opciones de transporte
- Mínimo 3 agencias de alquiler de auto
- Respondé SOLO JSON"""
        return await self._call_ai_json(prompt)
        """Get more hotels for a destination."""
        existing_names = [h.get('name','') for h in existing_hotels]
        prompt = f"""Necesito MÁS hoteles en {destination} para un viajero que sale desde {from_city}.
Ya tengo estos: {', '.join(existing_names)}

Generá un JSON con 10 hoteles NUEVOS (que NO estén en la lista anterior):
{{
  "hotels": [
    {{
      "name": "nombre real del hotel/hostel",
      "zone": "barrio",
      "type": "hotel/hostel/apartment/boutique/luxury",
      "price_per_night_usd": XX,
      "rating": X.X,
      "highlights": ["wifi", "breakfast", "pool"],
      "best_for": "parejas/solo/familias/mochileros",
      "latitude": XX.XXXX,
      "longitude": XX.XXXX
    }}
  ]
}}

REGLAS:
- Hoteles REALES con coordenadas reales
- Incluí desde hostels USD 15/noche hasta 5 estrellas USD 600+/noche
- Variedad de zonas y tipos
- Respondé SOLO JSON"""
        return await self._call_ai_json(prompt)

    async def get_more_activities(self, destination: str, existing_activities: list) -> dict:
        """Get more activities for a destination."""
        existing_names = [a.get('name','') for a in existing_activities]
        prompt = f"""Necesito MÁS actividades en {destination}.
Ya tengo estas: {', '.join(existing_names)}

Generá un JSON con 10 actividades NUEVAS:
{{
  "activities": [
    {{
      "name": "actividad",
      "category": "museum/nature/adventure/culture/nightlife/shopping/food",
      "description": "descripción corta",
      "duration_hours": X,
      "cost_usd": XX,
      "is_free": false,
      "best_time_to_visit": "horario",
      "rating": X.X,
      "latitude": XX.XXXX,
      "longitude": XX.XXXX
    }}
  ]
}}

REGLAS:
- Actividades REALES con coordenadas reales
- Variedad: gratis, pagas, aventura, cultura, comida, nocturnas
- NO repetir las que ya tengo
- Respondé SOLO JSON"""
        return await self._call_ai_json(prompt)

    async def get_more_flights(self, destination: str, from_city: str, flight_class: str = "economy") -> dict:
        """Get more flight options."""
        prompt = f"""Necesito MÁS opciones de vuelo desde {from_city} a {destination}, clase {flight_class}.

Generá un JSON con 8 opciones de vuelo:
{{
  "options": [
    {{
      "airline": "nombre",
      "origin_airport": "código",
      "destination_airport": "código",
      "duration_hours": X.X,
      "stops": 0,
      "stop_cities": [],
      "price_usd": XXXX,
      "baggage_included": true,
      "baggage_kg": 23,
      "is_cheapest": false,
      "is_fastest": false
    }}
  ]
}}

REGLAS:
- Vuelos reales con aerolíneas reales
- Incluí directos y con escalas
- Clase: {flight_class}
- Variedad de precios
- Respondé SOLO JSON"""
        return await self._call_ai_json(prompt)

    def _fallback_destination_data(self) -> dict:
        """Fallback data when OpenAI is not available."""
        return {
            "basic": {
                "name": "Tokyo",
                "country": "Japón",
                "continent": "Asia",
                "description": "Capital de Japón. Mezcla de tradición milenaria y tecnología futurista.",
                "tagline": "Donde el futuro y la tradición conviven",
                "language": "Japonés",
                "time_zone": "UTC+9",
                "best_months": ["Marzo", "Abril", "Octubre", "Noviembre"],
                "tags": ["culture", "food", "technology", "temples", "shopping"],
            },
            "flights": {
                "options": [
                    {
                        "airline": "ANA",
                        "origin_airport": "EZE",
                        "destination_airport": "NRT",
                        "duration_hours": 24.5,
                        "stops": 1,
                        "stop_cities": ["Houston"],
                        "price_usd": 1450,
                        "baggage_included": True,
                        "baggage_kg": 23,
                        "is_cheapest": False,
                        "is_fastest": True,
                    },
                    {
                        "airline": "Emirates",
                        "origin_airport": "EZE",
                        "destination_airport": "NRT",
                        "duration_hours": 30,
                        "stops": 1,
                        "stop_cities": ["Dubai"],
                        "price_usd": 1200,
                        "baggage_included": True,
                        "baggage_kg": 30,
                        "is_cheapest": True,
                        "is_fastest": False,
                    },
                    {
                        "airline": "LATAM + JAL",
                        "origin_airport": "EZE",
                        "destination_airport": "HND",
                        "duration_hours": 28,
                        "stops": 2,
                        "stop_cities": ["Santiago", "Los Angeles"],
                        "price_usd": 1100,
                        "baggage_included": True,
                        "baggage_kg": 23,
                        "is_cheapest": False,
                        "is_fastest": False,
                    },
                ],
                "cheapest_price": 1100,
                "fastest_duration_hours": 24.5,
                "best_day_to_buy": "Martes o miércoles",
                "airports_at_destination": ["NRT (Narita)", "HND (Haneda)"],
                "tips": [
                    "Haneda está más cerca del centro (30 min vs 90 min Narita)",
                    "Comprá con 3-6 semanas de anticipación",
                    "Los vuelos por Dubai suelen ser los más baratos",
                ],
            },
            "transport": {
                "airport_to_center": [
                    {"method": "Narita Express (tren)", "duration_minutes": 60, "cost_usd": 25, "frequency": "Cada 30 min"},
                    {"method": "Limousine Bus", "duration_minutes": 90, "cost_usd": 15, "frequency": "Cada 20 min"},
                    {"method": "Taxi", "duration_minutes": 60, "cost_usd": 200, "frequency": "Siempre disponible"},
                ],
                "internal_options": ["Metro/Subway", "JR Lines", "Bus", "Taxi", "Bike rental"],
                "passes_available": [
                    {
                        "name": "Japan Rail Pass (7 días)",
                        "price_usd": 280,
                        "duration_days": 7,
                        "covers": ["Shinkansen", "JR trains", "JR bus"],
                        "worth_it_if": "Si viajás entre ciudades (Tokyo-Kyoto-Osaka)",
                    },
                    {
                        "name": "Suica/Pasmo Card",
                        "price_usd": 5,
                        "duration_days": 0,
                        "covers": ["Metro", "JR local", "Bus", "Tiendas"],
                        "worth_it_if": "Siempre. Es como una SUBE recargable",
                    },
                    {
                        "name": "Tokyo Subway Ticket (72h)",
                        "price_usd": 13,
                        "duration_days": 3,
                        "covers": ["Tokyo Metro", "Toei Subway"],
                        "worth_it_if": "Si te quedás solo en Tokyo 3+ días",
                    },
                ],
                "best_option_budget": "Metro + Suica Card (USD 5-8/día)",
                "best_option_comfort": "Taxi app (Japan Taxi) o JR + Metro",
                "best_option_speed": "Shinkansen entre ciudades, Metro en ciudad",
                "uber_available": False,
                "walkable_city": True,
                "tips": [
                    "Uber no funciona bien. Usá Japan Taxi app",
                    "El metro cierra a las 00:30. Planificá bien la noche",
                    "Google Maps funciona perfecto para rutas de tren",
                ],
            },
            "accommodation": {
                "recommended_zones": [
                    {
                        "name": "Shinjuku",
                        "description": "Centro neurálgico. Estación más grande del mundo",
                        "why_stay_here": "Conectado a todo, vida nocturna, restaurantes",
                        "type": "tourist",
                        "avg_price_per_night_usd": 120,
                        "pros": ["Transporte", "Nightlife", "Restaurantes"],
                        "cons": ["Ruidoso", "Muy turístico"],
                    },
                    {
                        "name": "Asakusa",
                        "description": "Barrio tradicional con el templo Senso-ji",
                        "why_stay_here": "Ambiente japonés auténtico, más barato",
                        "type": "local",
                        "avg_price_per_night_usd": 70,
                        "pros": ["Barato", "Cultura", "Tranquilo"],
                        "cons": ["Lejos de Shibuya/Shinjuku"],
                    },
                    {
                        "name": "Shibuya",
                        "description": "El cruce más famoso del mundo. Joven y moderno",
                        "why_stay_here": "Shopping, moda, energía joven",
                        "type": "nightlife",
                        "avg_price_per_night_usd": 140,
                        "pros": ["Moda", "Nightlife", "Céntrico"],
                        "cons": ["Caro", "Multitudes"],
                    },
                ],
                "avg_price_budget": 35,
                "avg_price_mid": 100,
                "avg_price_luxury": 350,
                "tips": [
                    "Los capsule hotels cuestan USD 30-40 y son una experiencia",
                    "Reservá con 1 mes de anticipación en temporada alta",
                    "Los ryokan (posada tradicional) cuestan USD 150-300 pero valen la pena",
                ],
            },
            "food": {
                "typical_dishes": [
                    {"name": "Ramen", "description": "Sopa de fideos con caldo intenso", "avg_price_usd": 8, "is_must_try": True, "vegetarian": False},
                    {"name": "Sushi", "description": "Pescado fresco sobre arroz", "avg_price_usd": 15, "is_must_try": True, "vegetarian": False},
                    {"name": "Tempura", "description": "Vegetales y mariscos fritos en masa ligera", "avg_price_usd": 12, "is_must_try": True, "vegetarian": True},
                    {"name": "Yakitori", "description": "Brochetas de pollo a la parrilla", "avg_price_usd": 6, "is_must_try": False, "vegetarian": False},
                    {"name": "Okonomiyaki", "description": "Tortilla/panqueque japonés", "avg_price_usd": 9, "is_must_try": True, "vegetarian": True},
                    {"name": "Tonkatsu", "description": "Milanesa de cerdo japonesa", "avg_price_usd": 10, "is_must_try": False, "vegetarian": False},
                    {"name": "Matcha desserts", "description": "Postres de té verde", "avg_price_usd": 5, "is_must_try": True, "vegetarian": True},
                    {"name": "Gyoza", "description": "Empanaditas japonesas", "avg_price_usd": 5, "is_must_try": True, "vegetarian": False},
                    {"name": "Udon", "description": "Fideos gruesos en caldo", "avg_price_usd": 7, "is_must_try": False, "vegetarian": True},
                    {"name": "Takoyaki", "description": "Bolitas de pulpo", "avg_price_usd": 4, "is_must_try": True, "vegetarian": False},
                ],
                "avg_meal_budget_usd": 8,
                "avg_meal_mid_usd": 20,
                "avg_meal_luxury_usd": 80,
                "tipping_culture": "NO se deja propina. Es considerado ofensivo.",
                "vegetarian_friendly": False,
                "markets": ["Tsukiji Outer Market", "Ameya-Yokocho", "Nishiki Market (Kyoto)"],
                "tips": [
                    "Los convenience stores (7-Eleven, Lawson) tienen comida increíble por USD 3-5",
                    "Muchos restaurantes tienen ticket machines en la entrada",
                    "Los food courts de centros comerciales tienen opciones baratas y buenas",
                ],
            },
            "activities": {
                "must_do": [
                    {"name": "Templo Senso-ji", "category": "culture", "description": "El templo más antiguo de Tokyo", "duration_hours": 1.5, "cost_usd": 0, "is_free": True, "best_time_to_visit": "6-7 AM (vacío)", "rating": 4.7, "is_must_do": True},
                    {"name": "Cruce de Shibuya", "category": "culture", "description": "El cruce peatonal más famoso del mundo", "duration_hours": 0.5, "cost_usd": 0, "is_free": True, "best_time_to_visit": "Atardecer", "rating": 4.5, "is_must_do": True},
                    {"name": "Meiji Shrine", "category": "culture", "description": "Santuario sintoísta en un bosque dentro de la ciudad", "duration_hours": 1, "cost_usd": 0, "is_free": True, "best_time_to_visit": "Mañana temprano", "rating": 4.8, "is_must_do": True},
                    {"name": "Akihabara", "category": "shopping", "description": "Barrio de electrónica, anime y gaming", "duration_hours": 3, "cost_usd": 0, "is_free": True, "best_time_to_visit": "Tarde", "rating": 4.3, "is_must_do": True},
                    {"name": "TeamLab Borderless", "category": "art", "description": "Museo de arte digital inmersivo", "duration_hours": 2, "cost_usd": 25, "is_free": False, "best_time_to_visit": "Día de semana", "rating": 4.9, "is_must_do": True},
                ],
                "free_activities": [
                    {"name": "Caminar por Harajuku", "category": "culture", "description": "Moda alternativa y Takeshita Street", "duration_hours": 2, "cost_usd": 0, "is_free": True, "rating": 4.4},
                    {"name": "Jardines del Palacio Imperial", "category": "nature", "description": "Jardines del emperador", "duration_hours": 1.5, "cost_usd": 0, "is_free": True, "rating": 4.2},
                    {"name": "Mirador del Tokyo Metropolitan Building", "category": "culture", "description": "Vista 360° gratis de Tokyo", "duration_hours": 1, "cost_usd": 0, "is_free": True, "rating": 4.6},
                ],
                "total_count": 50,
                "tips": [
                    "Reservá TeamLab con 2 semanas de anticipación",
                    "Los templos son gratis y abren desde las 6 AM",
                    "Los parques son perfectos para descansar entre actividades",
                ],
            },
            "climate": {
                "by_month": [
                    {"month": "Enero", "avg_temp_celsius": 5, "rain_days": 4, "is_best_time": False, "what_to_wear": "Abrigo grueso"},
                    {"month": "Febrero", "avg_temp_celsius": 6, "rain_days": 5, "is_best_time": False, "what_to_wear": "Abrigo grueso"},
                    {"month": "Marzo", "avg_temp_celsius": 10, "rain_days": 9, "is_best_time": True, "what_to_wear": "Campera liviana + capas"},
                    {"month": "Abril", "avg_temp_celsius": 15, "rain_days": 10, "is_best_time": True, "what_to_wear": "Ropa liviana + campera"},
                    {"month": "Mayo", "avg_temp_celsius": 20, "rain_days": 9, "is_best_time": True, "what_to_wear": "Remera + pantalón"},
                    {"month": "Junio", "avg_temp_celsius": 23, "rain_days": 12, "is_best_time": False, "what_to_wear": "Ropa liviana + paraguas"},
                    {"month": "Julio", "avg_temp_celsius": 27, "rain_days": 10, "is_best_time": False, "what_to_wear": "Ropa muy liviana"},
                    {"month": "Agosto", "avg_temp_celsius": 29, "rain_days": 8, "is_best_time": False, "what_to_wear": "Ropa muy liviana"},
                    {"month": "Septiembre", "avg_temp_celsius": 25, "rain_days": 11, "is_best_time": False, "what_to_wear": "Ropa liviana"},
                    {"month": "Octubre", "avg_temp_celsius": 19, "rain_days": 9, "is_best_time": True, "what_to_wear": "Campera liviana"},
                    {"month": "Noviembre", "avg_temp_celsius": 14, "rain_days": 6, "is_best_time": True, "what_to_wear": "Campera + bufanda"},
                    {"month": "Diciembre", "avg_temp_celsius": 8, "rain_days": 4, "is_best_time": False, "what_to_wear": "Abrigo grueso"},
                ],
                "best_months_to_visit": ["Marzo", "Abril", "Octubre", "Noviembre"],
                "rainy_season": "Junio-Julio (Tsuyu)",
                "packing_essentials": ["Paraguas compacto", "Zapatos cómodos para caminar", "Adaptador tipo A/B"],
            },
            "safety": {
                "safety_score": 9,
                "visa_required": False,
                "vaccines_required": [],
                "vaccines_recommended": ["Ninguna específica"],
                "dangerous_zones": ["Kabukicho de noche (estafas en bares)"],
                "common_scams": [
                    "Bares con precios ocultos en Kabukicho",
                    "Falsos monjes pidiendo donaciones",
                ],
                "emergency_number": "110 (policía) / 119 (ambulancia)",
                "tap_water_safe": True,
                "lgbtq_friendly": True,
                "tips": [
                    "Japón es extremadamente seguro. Podés caminar a cualquier hora",
                    "Si perdés algo, probablemente lo encuentres en la oficina de objetos perdidos",
                ],
            },
            "money": {
                "local_currency": "Yen japonés",
                "currency_code": "JPY",
                "exchange_rate_usd": 150,
                "cards_accepted": True,
                "cash_preferred": True,
                "atm_available": True,
                "tipping_expected": False,
                "budget_backpacker_usd": 60,
                "budget_mid_usd": 120,
                "budget_comfort_usd": 200,
                "budget_luxury_usd": 500,
                "tips": [
                    "Muchos lugares pequeños solo aceptan efectivo",
                    "Los ATM de 7-Eleven aceptan tarjetas internacionales",
                    "NO se deja propina nunca",
                ],
            },
            "comparisons": {
                "trip_by_duration": [
                    {"days": 3, "total_cost_mid_usd": 1800, "what_you_can_do": ["Tokyo básico: Shibuya, Senso-ji, Akihabara"], "what_you_miss": ["Kyoto", "Monte Fuji", "Nara"], "recommendation": "Muy poco. Solo si es escala"},
                    {"days": 5, "total_cost_mid_usd": 2400, "what_you_can_do": ["Tokyo completo + día en Kamakura o Nikko"], "what_you_miss": ["Kyoto", "Osaka"], "recommendation": "Mínimo recomendado para Tokyo"},
                    {"days": 7, "total_cost_mid_usd": 3000, "what_you_can_do": ["Tokyo + Kyoto + Nara"], "what_you_miss": ["Osaka", "Hiroshima"], "recommendation": "Ideal para primer viaje"},
                    {"days": 10, "total_cost_mid_usd": 3800, "what_you_can_do": ["Tokyo + Kyoto + Osaka + Nara + Hiroshima"], "what_you_miss": ["Hokkaido", "Okinawa"], "recommendation": "Viaje completo sin apuros"},
                ],
                "insights": [
                    "El JR Pass (USD 280/7 días) se paga solo si hacés Tokyo-Kyoto ida y vuelta (USD 250 sin pase)",
                    "Hostel vs Hotel: ahorrás USD 70/noche pero perdés privacidad",
                    "Vuelo con 1 escala vs 2 escalas: +USD 150 pero ahorrás 6 horas",
                ],
            },
            "suggested_itineraries": [
                {
                    "title": "Tokyo Express - 5 días budget",
                    "days": 5,
                    "style": "budget",
                    "total_cost_usd": 1800,
                    "daily_plan": [
                        {"day_number": 1, "title": "Llegada + Shinjuku", "activities": ["Check-in", "Shinjuku Gyoen", "Golden Gai"], "estimated_cost_usd": 40, "walking_km": 5},
                        {"day_number": 2, "title": "Tradición", "activities": ["Senso-ji (6AM)", "Ueno Park", "Akihabara"], "estimated_cost_usd": 25, "walking_km": 12},
                        {"day_number": 3, "title": "Cultura Pop", "activities": ["Harajuku", "Shibuya", "Shibuya Sky"], "estimated_cost_usd": 35, "walking_km": 10},
                        {"day_number": 4, "title": "Excursión", "activities": ["Kamakura", "Gran Buda", "Playa"], "estimated_cost_usd": 30, "walking_km": 8},
                        {"day_number": 5, "title": "Último día", "activities": ["Tsukiji Market", "Ginza", "Tokyo Tower"], "estimated_cost_usd": 40, "walking_km": 7},
                    ],
                    "best_for": ["budget", "first-timers", "solo"],
                },
            ],
            "quick_stats": {
                "avg_cost_per_day_usd": 120,
                "best_time_to_visit": "Marzo-Abril (sakura) u Octubre-Noviembre (otoño)",
                "min_days_recommended": 5,
                "ideal_days": 7,
            },
        }


    async def _call_ai_json(self, prompt: str) -> dict:
        """Call OpenAI and get JSON response."""
        import json

        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "sk-placeholder":
            return self._fallback_destination_data()

        try:
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Sos un experto en viajes. Respondé SOLO JSON válido. "
                            "Sin markdown, sin ```json, sin texto extra. Solo el JSON. "
                            "Sé conciso en descripciones."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=8000,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Try to repair truncated JSON
                repaired = self._repair_json(content)
                if repaired:
                    return repaired
                print(f"[TravelOS AI ERROR] Could not parse or repair JSON")
                return self._fallback_destination_data()

        except Exception as e:
            print(f"[TravelOS AI ERROR] {type(e).__name__}: {e}")
            return self._fallback_destination_data()

    def _repair_json(self, content: str) -> dict:
        """Try to repair broken/truncated JSON from AI."""
        import json
        # Close any unclosed brackets/braces
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        # Remove trailing comma if any
        content = content.rstrip()
        if content.endswith(','):
            content = content[:-1]
        # Close open strings (find last unclosed quote)
        if content.count('"') % 2 != 0:
            content += '"'
        # Close arrays and objects
        content += ']' * open_brackets
        content += '}' * open_braces
        try:
            return json.loads(content)
        except:
            # Last resort: try to find the largest valid JSON substring
            for i in range(len(content), 0, -100):
                substr = content[:i]
                open_b = substr.count('{') - substr.count('}')
                open_a = substr.count('[') - substr.count(']')
                attempt = substr + ']' * open_a + '}' * open_b
                try:
                    return json.loads(attempt)
                except:
                    continue
            return None


    async def get_more_hotels(self, destination: str, from_city: str, existing_hotels: list) -> dict:
        """Get more hotels for a destination."""
        existing_names = [h.get('name','') for h in existing_hotels]
        prompt = f"""Necesito MÁS hoteles en {destination}.
Ya tengo estos: {', '.join(existing_names[:5])}

Generá un JSON con 10 hoteles NUEVOS:
{{
  "hotels": [
    {{
      "name": "nombre real",
      "zone": "barrio",
      "type": "hotel/hostel/boutique/luxury",
      "price_per_night_usd": XX,
      "rating": X.X,
      "highlights": ["wifi", "breakfast"],
      "best_for": "parejas/solo/familias",
      "latitude": XX.XXXX,
      "longitude": XX.XXXX
    }}
  ]
}}
- Hoteles REALES, coordenadas reales
- NO repetir los que ya tengo
- Respondé SOLO JSON"""
        return await self._call_ai_json(prompt)
