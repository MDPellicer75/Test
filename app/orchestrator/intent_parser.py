"""
TravelOS - Intent Parser
Classifies user messages into intents using OpenAI.
Falls back to keyword matching if API is unavailable.
"""

from openai import AsyncOpenAI

from app.core.config import settings
from app.orchestrator.intents import Intent


# Keyword-based fallback classifier
KEYWORD_MAP = {
    Intent.PLAN_TRIP: [
        "planificar", "planifica", "organizar", "armar viaje", "quiero ir",
        "viajo a", "voy a viajar", "trip to", "plan trip",
    ],
    Intent.PLAN_DAY: [
        "horas libres", "esta tarde", "hoy", "mañana hacer",
        "qué hago", "plan del día", "free hours",
    ],
    Intent.REPLAN: [
        "cambiar", "reorganizar", "llueve", "cancelar", "mover",
        "reprogramar", "replan",
    ],
    Intent.FIND_RESTAURANT: [
        "comer", "restaurante", "comida", "almorzar", "cenar",
        "desayunar", "café", "bar", "restaurant",
    ],
    Intent.FIND_ACTIVITY: [
        "hacer", "actividad", "visitar", "conocer", "ver",
        "atracción", "museo", "parque", "activity",
    ],
    Intent.FIND_HOTEL: [
        "hotel", "hostel", "alojamiento", "dormir", "hospedaje",
        "airbnb", "accommodation",
    ],
    Intent.SHOW_BUDGET: [
        "presupuesto", "gasté", "gastado", "dinero", "plata",
        "budget", "money", "spent",
    ],
    Intent.SHOW_TIMELINE: [
        "itinerario", "agenda", "horario", "cronograma",
        "timeline", "schedule",
    ],
    Intent.SHOW_MAP: [
        "mapa", "ubicación", "dónde queda", "cómo llego",
        "map", "location", "directions",
    ],
    Intent.SHOW_WEATHER: [
        "clima", "tiempo", "lluvia", "temperatura", "weather",
        "rain", "cold", "hot",
    ],
    Intent.ADD_EXPENSE: [
        "gasté", "pagué", "costó", "expense", "paid", "cost",
    ],
    Intent.BOOK: [
        "reservar", "reservá", "booking", "book", "reserve",
    ],
    Intent.TRANSLATE: [
        "traducir", "cómo se dice", "translate", "how do you say",
        "qué significa",
    ],
    Intent.EMERGENCY: [
        "emergencia", "hospital", "policía", "embajada", "ayuda urgente",
        "emergency", "police", "ambulance",
    ],
    Intent.HELP: [
        "ayuda", "qué podés", "funciones", "help", "what can you",
    ],
}


def classify_by_keywords(message: str) -> Intent:
    """Fallback: classify intent using keyword matching."""
    message_lower = message.lower()

    best_intent = Intent.GENERAL_CHAT
    best_score = 0

    for intent, keywords in KEYWORD_MAP.items():
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent


async def classify_intent(message: str) -> Intent:
    """
    Classify user message into an intent using OpenAI.
    Falls back to keyword matching if API fails.
    """
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "sk-placeholder":
        return classify_by_keywords(message)

    try:
        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        intents_list = ", ".join([i.value for i in Intent])

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an intent classifier for a travel app. "
                        f"Classify the user message into exactly one of these intents: {intents_list}. "
                        "Respond with ONLY the intent name, nothing else."
                    ),
                },
                {"role": "user", "content": message},
            ],
            temperature=0,
            max_tokens=30,
        )

        intent_str = response.choices[0].message.content.strip()

        # Try to match the response to an Intent
        try:
            return Intent(intent_str)
        except ValueError:
            return classify_by_keywords(message)

    except Exception:
        # If OpenAI fails, fall back to keywords
        return classify_by_keywords(message)
