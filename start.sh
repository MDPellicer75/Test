#!/bin/bash
# ============================================
# TravelOS - Quick Start (sin Docker)
# ============================================

echo "📦 Instalando dependencias..."
pip install -r requirements.txt

echo "⚙️  Creando archivo .env..."
cp .env.example .env

echo "🚀 Iniciando TravelOS..."
echo ""
echo "=================================="
echo "  API: http://localhost:8000"
echo "  Swagger: http://localhost:8000/docs"
echo "=================================="
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
