"""
TravelOS - Health Check Endpoint
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    """
    Health check.
    Returns OK if the API is running.
    """
    return {
        "status": "ok",
        "app": "TravelOS",
        "version": "0.1.0",
    }
