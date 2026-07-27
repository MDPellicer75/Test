"""
TravelOS - Main Application
FastAPI entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import engine
from app.db.base import Base

# Import all models so they register with Base.metadata
from app.models import User, Trip, TripDay, Activity, TravelDNA  # noqa: F401

# Import routers
from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.trips import router as trips_router
from app.api.v1.chat import router as chat_router
from app.api.v1.destinations import router as destinations_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle.
    Creates tables on startup (dev mode).
    In production, use Alembic migrations instead.
    """
    # Startup
    if settings.DEBUG:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown
    await engine.dispose()


# ─── Create App ─────────────────────────────────────────

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Travel Operating System — El copiloto de IA que acompaña al viajero antes, durante y después del viaje.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── CORS ───────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Register Routers ──────────────────────────────────

# Health (no prefix)
app.include_router(health_router)

# API v1
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(trips_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(destinations_router, prefix="/api/v1")
