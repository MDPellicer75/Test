"""
TravelOS - Intent Parser Tests
Tests the keyword-based fallback classifier.
"""

import pytest

from app.orchestrator.intent_parser import classify_by_keywords
from app.orchestrator.intents import Intent


def test_plan_trip_intent():
    """Detects trip planning intent."""
    assert classify_by_keywords("Quiero ir a Japón") == Intent.PLAN_TRIP
    assert classify_by_keywords("Planificame un viaje a Roma") == Intent.PLAN_TRIP


def test_plan_day_intent():
    """Detects day planning intent."""
    assert classify_by_keywords("Tengo 4 horas libres") == Intent.PLAN_DAY
    assert classify_by_keywords("Qué hago esta tarde?") == Intent.PLAN_DAY


def test_find_restaurant_intent():
    """Detects restaurant search intent."""
    assert classify_by_keywords("Dónde comemos?") == Intent.FIND_RESTAURANT
    assert classify_by_keywords("Busco un restaurante barato") == Intent.FIND_RESTAURANT


def test_find_activity_intent():
    """Detects activity search intent."""
    assert classify_by_keywords("Qué puedo visitar cerca?") == Intent.FIND_ACTIVITY


def test_emergency_intent():
    """Detects emergency intent."""
    assert classify_by_keywords("Necesito un hospital urgente") == Intent.EMERGENCY
    assert classify_by_keywords("Dónde está la policía?") == Intent.EMERGENCY


def test_budget_intent():
    """Detects budget queries."""
    assert classify_by_keywords("Cuánto llevo gastado?") == Intent.SHOW_BUDGET
    assert classify_by_keywords("Mostrame el presupuesto") == Intent.SHOW_BUDGET


def test_weather_intent():
    """Detects weather queries."""
    assert classify_by_keywords("Va a llover mañana?") == Intent.SHOW_WEATHER
    assert classify_by_keywords("Cómo está el clima?") == Intent.SHOW_WEATHER


def test_translate_intent():
    """Detects translation requests."""
    assert classify_by_keywords("Cómo se dice la cuenta en japonés?") == Intent.TRANSLATE


def test_help_intent():
    """Detects help requests."""
    assert classify_by_keywords("Qué podés hacer?") == Intent.HELP


def test_general_chat_fallback():
    """Falls back to general chat for unknown messages."""
    assert classify_by_keywords("Hola qué tal") == Intent.GENERAL_CHAT
    assert classify_by_keywords("xyz abc 123") == Intent.GENERAL_CHAT
