"""
TravelOS - Planner Agent
Generates and adjusts itineraries using AI.
"""

from openai import AsyncOpenAI

from app.core.config import settings
from app.agents.base_agent import BaseAgent, AgentContext


class PlannerAgent(BaseAgent):
    """
    Plans itineraries, day plans, and replans.
    Uses the user's TravelDNA to personalize recommendations.
    """

    async def run(self, context: AgentContext) -> str:
        """Generate a plan based on the user's message and context."""

        # Build the system prompt with user preferences
        system_prompt = self._build_system_prompt(context)

        # Build the user prompt
        user_prompt = self._build_user_prompt(context)

        # Call OpenAI (or fallback)
        response = await self._call_ai(system_prompt, user_prompt)

        return response

    def _build_system_prompt(self, context: AgentContext) -> str:
        """Create a system prompt personalized with TravelDNA."""

        base = (
            "Sos un planificador de viajes experto. "
            "Generás itinerarios detallados, realistas y personalizados. "
            "Respondé siempre en español. "
            "Sé conciso pero completo. "
            "Incluí horarios, lugares específicos, y costos estimados. "
        )

        # Add TravelDNA context if available
        if context.travel_dna:
            dna = context.travel_dna
            preferences = []

            if dna.food_score > 0.7:
                preferences.append("Le encanta la gastronomía")
            if dna.museum_score < 0.3:
                preferences.append("No le gustan los museos")
            if dna.walking_score > 0.7:
                preferences.append("Le gusta caminar mucho")
            if dna.walking_score < 0.3:
                preferences.append("Prefiere no caminar demasiado")
            if dna.nature_score > 0.7:
                preferences.append("Ama la naturaleza")
            if dna.nightlife_score > 0.7:
                preferences.append("Le gusta la vida nocturna")
            if dna.photography_score > 0.7:
                preferences.append("Le gusta la fotografía")
            if dna.adventure_score > 0.7:
                preferences.append("Busca aventura")
            if dna.relaxation_score > 0.7:
                preferences.append("Prefiere relax")

            budget_labels = {
                1: "mochilero",
                2: "económico",
                3: "moderado",
                4: "confortable",
                5: "lujo",
            }
            budget_label = budget_labels.get(dna.budget_level, "moderado")
            preferences.append(f"Presupuesto: {budget_label}")
            preferences.append(f"Máximo caminar: {dna.max_walking_km} km/día")

            if dna.dietary_preferences:
                preferences.append(f"Dieta: {dna.dietary_preferences}")

            if preferences:
                base += "\n\nPerfil del viajero:\n" + "\n".join(
                    f"- {p}" for p in preferences
                )

        return base

    def _build_user_prompt(self, context: AgentContext) -> str:
        """Create the user prompt with trip context."""

        parts = [context.message]

        if context.trip:
            trip = context.trip
            parts.append(f"\nDestino: {trip.destination}")
            if trip.start_date and trip.end_date:
                days = (trip.end_date - trip.start_date).days + 1
                parts.append(f"Duración: {days} días ({trip.start_date} a {trip.end_date})")
            if trip.budget:
                parts.append(f"Presupuesto total: {trip.budget} {trip.currency}")
            if trip.travelers_count > 1:
                parts.append(f"Viajeros: {trip.travelers_count}")

        return "\n".join(parts)

    async def _call_ai(self, system_prompt: str, user_prompt: str) -> str:
        """Call OpenAI API or return fallback response."""

        if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "sk-placeholder":
            return self._fallback_response(user_prompt)

        try:
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
            )

            return response.choices[0].message.content

        except Exception as e:
            return self._fallback_response(user_prompt)

    def _fallback_response(self, user_prompt: str) -> str:
        """Fallback when OpenAI is not available."""
        return (
            "He analizado tu solicitud. Para generar un itinerario personalizado "
            "necesito la conexión con el servicio de IA. "
            "Mientras tanto, te sugiero:\n\n"
            "1. Definir las fechas exactas del viaje\n"
            "2. Establecer un presupuesto diario\n"
            "3. Indicar tus intereses principales\n\n"
            "Una vez configurada la API de OpenAI, podré crear "
            "itinerarios detallados hora por hora, adaptados a tus gustos."
        )
