"""
TravelOS - Intent Definitions
Every user message is classified into one of these intents.
The Orchestrator uses the intent to route to the correct agent(s).
"""

from enum import Enum


class Intent(str, Enum):
    """All possible user intents."""

    # Planning
    PLAN_TRIP = "PLAN_TRIP"          # "Quiero ir a Japón 5 días"
    PLAN_DAY = "PLAN_DAY"            # "Tengo 4 horas libres"
    REPLAN = "REPLAN"                # "Cambiame el día, llueve"

    # Discovery
    FIND_RESTAURANT = "FIND_RESTAURANT"  # "¿Dónde comemos?"
    FIND_ACTIVITY = "FIND_ACTIVITY"      # "¿Qué hago esta tarde?"
    FIND_HOTEL = "FIND_HOTEL"            # "Busco hotel barato"

    # Information
    SHOW_BUDGET = "SHOW_BUDGET"      # "¿Cuánto llevo gastado?"
    SHOW_TIMELINE = "SHOW_TIMELINE"  # "¿Qué tengo mañana?"
    SHOW_MAP = "SHOW_MAP"            # "Mostrá el mapa"
    SHOW_WEATHER = "SHOW_WEATHER"    # "¿Va a llover?"

    # Actions
    ADD_EXPENSE = "ADD_EXPENSE"      # "Gasté 30 euros en almuerzo"
    BOOK = "BOOK"                    # "Reservá eso"
    TRANSLATE = "TRANSLATE"          # "¿Cómo se dice 'la cuenta'?"

    # Utility
    EMERGENCY = "EMERGENCY"          # "Necesito un hospital"
    HELP = "HELP"                    # "¿Qué podés hacer?"

    # Fallback
    GENERAL_CHAT = "GENERAL_CHAT"    # Conversación general sobre viaje
