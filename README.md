# Selfinity Backend

Selfinity is a self-analysis tool built on an extended “wheel of life” model. It helps users track the state of key life areas, identify concrete problems, and map each one to an actionable step.

## Product Concept

- **Eight focus areas**: health, spirituality, friends, love/family, work & income, home, fun, rest.
- **Working sheets**: every area stores a score (0–100), a list of specific problems, and one matching action per problem.
- **Tight feedback loop**: users review scores weekly and adjust actions, turning self-improvement into a manageable process.
- **Core domain plan**: user → habit/action set → execution logs and analytics.

## Current Status

> Phase 1: backend foundation in place. We have a FastAPI skeleton with configuration, database connectivity, `/health` endpoint, Alembic migrations, and pytest. Future phases introduce domain models, auth, and frontend.

## Tech Stack

- **Language**: Python 3.11+
- **Web/API**: FastAPI, Uvicorn
- **Database**: PostgreSQL (asyncpg, SQLAlchemy 2.x, Alembic)
- **Testing**: pytest, pytest-asyncio, httpx
- **Containers**: Docker, docker-compose
- **Other**: pydantic-settings, Redis (planned by spec)

## Repository Structure

```
backend/
├── app/
│   ├── api/           # FastAPI routes
│   ├── core/          # configuration & database
│   ├── models/        # SQLAlchemy declarative base
│   └── main.py        # FastAPI entry point
├── alembic/           # migration scripts
├── tests/             # pytest fixtures and tests
├── requirements.txt   # Python dependencies
├── docker-compose.yml # local development stack
├── Dockerfile         # backend image
├── .env.example       # sample environment variables
└── README.md
```

Product documentation (vision, decomposition, stack) lives under `doc/`.

## Local Environment Without Docker

1. **Create a virtualenv and install dependencies**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Update `DATABASE_URL` (format `postgresql+asyncpg://USER:PASS@HOST:PORT/DB`).

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```
   Health check endpoint: `http://localhost:8000/health`.

## Docker Compose Spin-up

```bash
cd backend
docker compose up --build
```

Services:
- `postgres` — PostgreSQL 15 with persistent volume `postgres_data`
- `app` — FastAPI with hot reload

After startup the API is reachable at `http://localhost:8000/health`. Shut down with `docker compose down`.

## Alembic Migrations

1. Apply migrations:
   ```bash
   alembic upgrade head
   ```
2. Generate a new migration (after model changes):
   ```bash
   alembic revision --autogenerate -m "describe change"
   ```
3. (Optional) Mark the current state without applying:
   ```bash
   alembic stamp head
   ```

> ⚠️ Ensure the target database is up to date (`alembic upgrade head`) before running `revision --autogenerate`. Otherwise Alembic will refuse to generate the next revision.

## Testing

```bash
source .venv/bin/activate
pytest
```

Tests run against PostgreSQL. In CI a Postgres service is provided and `DATABASE_URL` points to it. For local runs, set `DATABASE_URL` to your Postgres instance (e.g. `postgresql+asyncpg://user:pass@localhost:5432/dbname`).

## Example Request

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2025-10-10T15:06:00Z",
  "database": "connected"
}
```

## Next Steps (per roadmap)

- Introduce user, habit, and log models.
- Implement JWT authentication.
- Add Redis for caching and sessions.
- Build the frontend (React + TypeScript + MUI/Tailwind).
- Wire up CI/CD and cloud environments on AWS/GCP.

See `doc/phase-1.md` and related files for the full development plan.
