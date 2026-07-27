# TravelOS Backend

**Travel Operating System** — El copiloto de IA que acompaña al viajero antes, durante y después del viaje.

## Stack

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL 16
- Redis 7
- JWT Authentication
- OpenAI GPT
- Docker

## Quick Start

```bash
# 1. Copiar variables de entorno
cp .env.example .env

# 2. Editar .env con tus keys reales
nano .env

# 3. Levantar todo
docker compose up --build

# 4. Acceder a la API
# Swagger UI: http://localhost:8000/docs
# Health:     http://localhost:8000/health
```

## Estructura

```
backend/
├── app/
│   ├── api/v1/          # Endpoints (auth, users, trips, chat)
│   ├── core/            # Config, seguridad JWT
│   ├── db/              # Database connection
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── repositories/    # Data access
│   ├── orchestrator/    # AI brain
│   ├── agents/          # AI agents (Planner, Explorer, etc)
│   └── main.py          # FastAPI app
├── alembic/             # Migrations
├── tests/               # Pytest
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /api/v1/auth/register | Registro |
| POST | /api/v1/auth/login | Login (JWT) |
| GET | /api/v1/users/me | Perfil del usuario |
| PUT | /api/v1/users/me | Actualizar perfil |
| POST | /api/v1/trips | Crear viaje |
| GET | /api/v1/trips | Listar viajes |
| GET | /api/v1/trips/{id} | Obtener viaje |
| PUT | /api/v1/trips/{id} | Actualizar viaje |
| DELETE | /api/v1/trips/{id} | Eliminar viaje |
| POST | /api/v1/chat | Chat con IA |

## Arquitectura

```
Usuario → API → Service → Repository → Database
                  ↓
              Orchestrator → Agents (Planner, Explorer, Weather, Budget)
```

## Tests

```bash
docker compose exec api pytest tests/ -v
```
