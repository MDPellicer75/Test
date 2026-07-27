"""
TravelOS - Application Configuration
All settings loaded from environment variables.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # App
    APP_NAME: str = "TravelOS"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://travelos:travelos_secret@postgres:5432/travelos"

    # Redis
    REDIS_URL: str = "redis://redis:6379/0"

    # JWT
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Google Maps
    GOOGLE_MAPS_API_KEY: str = ""

    # Weather
    WEATHER_API_KEY: str = ""

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()
