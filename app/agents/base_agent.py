"""
TravelOS - Base Agent
All agents inherit from this base class.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from app.models.trip import Trip
from app.models.travel_dna import TravelDNA


@dataclass
class AgentContext:
    """
    Context passed to every agent.
    Contains everything an agent needs to make decisions.
    """

    user_id: UUID
    trip_id: UUID
    message: str
    trip: Optional[Trip] = None
    travel_dna: Optional[TravelDNA] = None

    @property
    def destination(self) -> str:
        """Get trip destination or fallback."""
        if self.trip and self.trip.destination:
            return self.trip.destination
        return "destino no especificado"

    @property
    def budget(self) -> Optional[float]:
        """Get trip budget."""
        if self.trip:
            return self.trip.budget
        return None

    @property
    def currency(self) -> str:
        """Get trip currency."""
        if self.trip:
            return self.trip.currency
        return "USD"


class BaseAgent(ABC):
    """
    Base class for all TravelOS agents.
    
    Rules:
    - Agents NEVER talk to the user directly.
    - Agents return structured data to the Orchestrator.
    - Agents can call external APIs.
    - Agents should be stateless.
    """

    @abstractmethod
    async def run(self, context: AgentContext) -> str:
        """
        Execute the agent's logic.
        Returns a text response that the Orchestrator will format.
        """
        ...
