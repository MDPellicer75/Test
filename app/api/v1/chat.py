"""
TravelOS - Chat Endpoint
The main interface between the user and the AI system.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import get_current_user_id
from app.orchestrator.orchestrator import Orchestrator
from app.schemas.trip import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    user_id: UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message to the AI travel copilot.

    The orchestrator will:
    1. Classify the intent of the message
    2. Route to the appropriate agent(s)
    3. Return a response with optional actions for the frontend

    Example request:
    ```json
    {
        "trip_id": "uuid-of-trip",
        "message": "Tengo 4 horas libres, ¿qué hago?"
    }
    ```

    Example response:
    ```json
    {
        "intent": "PLAN_DAY",
        "answer": "Te recomiendo visitar el Mercado...",
        "actions": [{"type": "update_itinerary"}]
    }
    ```
    """
    orchestrator = Orchestrator(db)

    try:
        response = await orchestrator.process_message(
            user_id=user_id,
            trip_id=data.trip_id,
            message=data.message,
        )
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando el mensaje: {str(e)}",
        )
