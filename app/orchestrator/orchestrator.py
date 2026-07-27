"""
TravelOS - Orchestrator
The brain of the application.

Flow:
    User Message → Intent Parser → Route to Agent(s) → Combine Responses → Return

Rules:
    - Agents NEVER talk to the user directly.
    - Only the Orchestrator formats the final response.
    - The Orchestrator can call multiple agents for a single request.
"""

from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.orchestrator.intents import Intent
from app.orchestrator.intent_parser import classify_intent
from app.agents.planner_agent import PlannerAgent
from app.agents.base_agent import AgentContext
from app.schemas.trip import ChatResponse, ChatAction
from app.repositories.trip_repository import TripRepository
from app.repositories.user_repository import UserRepository


class Orchestrator:
    """
    Central coordinator for all AI interactions.
    Routes messages to the appropriate agents based on intent.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.trip_repo = TripRepository(db)
        self.user_repo = UserRepository(db)

    async def process_message(
        self,
        user_id: UUID,
        trip_id: UUID,
        message: str,
    ) -> ChatResponse:
        """
        Process a user message:
        1. Classify intent
        2. Build context
        3. Route to agent(s)
        4. Return unified response
        """

        # 1. Classify intent
        intent = await classify_intent(message)

        # 2. Build context for agents
        context = await self._build_context(user_id, trip_id, message)

        # 3. Route to the appropriate agent
        response = await self._route(intent, context)

        return response

    async def _build_context(
        self, user_id: UUID, trip_id: UUID, message: str
    ) -> AgentContext:
        """Build the context object that agents need."""
        # Get trip info
        trip = await self.trip_repo.get_by_id(trip_id, user_id)

        # Get user's travel DNA
        travel_dna = await self.user_repo.get_travel_dna(user_id)

        return AgentContext(
            user_id=user_id,
            trip_id=trip_id,
            message=message,
            trip=trip,
            travel_dna=travel_dna,
        )

    async def _route(self, intent: Intent, context: AgentContext) -> ChatResponse:
        """Route to the correct agent based on intent."""

        # Planning intents
        if intent in (Intent.PLAN_TRIP, Intent.PLAN_DAY, Intent.REPLAN):
            agent = PlannerAgent()
            answer = await agent.run(context)
            return ChatResponse(
                intent=intent.value,
                answer=answer,
                actions=[ChatAction(type="update_itinerary")],
            )

        # Discovery intents
        if intent in (Intent.FIND_RESTAURANT, Intent.FIND_ACTIVITY, Intent.FIND_HOTEL):
            # TODO: ExplorerAgent (Sprint 1.2)
            return ChatResponse(
                intent=intent.value,
                answer=f"Entendido. Estoy buscando opciones cerca de {context.trip.destination if context.trip else 'tu ubicación'}. Esta función estará completa en la próxima versión.",
                actions=[ChatAction(type="show_recommendations")],
            )

        # Budget
        if intent == Intent.SHOW_BUDGET:
            return ChatResponse(
                intent=intent.value,
                answer="Función de presupuesto en desarrollo. Pronto podrás ver tus gastos en tiempo real.",
                actions=[ChatAction(type="show_budget")],
            )

        # Weather
        if intent == Intent.SHOW_WEATHER:
            return ChatResponse(
                intent=intent.value,
                answer="Consultando el clima... Esta función estará disponible con la integración de WeatherAPI.",
                actions=[ChatAction(type="show_weather")],
            )

        # Timeline
        if intent == Intent.SHOW_TIMELINE:
            return ChatResponse(
                intent=intent.value,
                answer="Mostrando tu itinerario.",
                actions=[ChatAction(type="show_timeline")],
            )

        # Map
        if intent == Intent.SHOW_MAP:
            return ChatResponse(
                intent=intent.value,
                answer="Abriendo el mapa con tus actividades.",
                actions=[ChatAction(type="open_map")],
            )

        # Translate
        if intent == Intent.TRANSLATE:
            # TODO: TranslatorAgent (Sprint 1.3)
            return ChatResponse(
                intent=intent.value,
                answer="Función de traducción en desarrollo.",
                actions=[],
            )

        # Emergency
        if intent == Intent.EMERGENCY:
            return ChatResponse(
                intent=intent.value,
                answer="MODO EMERGENCIA activado. Mostrando recursos de emergencia cerca de tu ubicación.",
                actions=[
                    ChatAction(type="emergency_mode", data={"show": True}),
                ],
            )

        # Help
        if intent == Intent.HELP:
            return ChatResponse(
                intent=intent.value,
                answer=(
                    "Soy tu copiloto de viaje. Puedo:\n\n"
                    "- Planificar tu viaje completo\n"
                    "- Reorganizar el día si cambia el clima\n"
                    "- Buscar restaurantes y actividades\n"
                    "- Controlar tu presupuesto\n"
                    "- Traducir en tiempo real\n"
                    "- Mostrarte el mapa\n"
                    "- Activar modo emergencia\n\n"
                    "Simplemente decime qué necesitás."
                ),
                actions=[],
            )

        # General chat / fallback
        return ChatResponse(
            intent=intent.value,
            answer="Entendido. ¿Querés que te ayude a planificar algo para tu viaje?",
            actions=[],
        )
