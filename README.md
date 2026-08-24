# Agent OS

A vendor-neutral control plane for durable, observable, and governable AI agent execution.

Agent OS separates **planning** (missions, tasks, approvals) from **execution** (durable Temporal workflows, simulator/OpenAI adapters) and records immutable evidence for every run.

## Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2 async, Pydantic v2, Alembic
- **Orchestration**: Temporal (durable D0/D1/D2 workflows)
- **Frontend**: Next.js 14/15, React, TypeScript
- **Data**: PostgreSQL 16, Redis 7, SQLite for local tests
- **Ops**: Docker Compose, GitHub Actions

## Prerequisites

- Python 3.12
- Node.js 20
- Docker & Docker Compose
- (Optional) Temporal CLI or `docker compose` for the full stack

## Quick start

```bash
# 1. Copy the example environment
cp .env.example .env
# Edit .env and replace the placeholder secrets.

# 2. Start the local stack
docker compose up -d

# 3. Run database migrations
make migrate

# 4. Open the API docs
open http://localhost:8080/docs
```

## Development without Docker

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Testing & linting

```bash
# Backend tests
cd backend && pytest -q

# Backend lint
cd backend && black --check . && isort --check-only . && flake8 .

# Frontend lint/build
cd frontend && npm run lint && npm run build
```

## Project layout

```
agent-os/
├── backend/          # FastAPI control plane + Temporal activities
│   ├── app/
│   │   ├── api/      # HTTP routers
│   │   ├── models/   # SQLAlchemy domain models
│   │   ├── schemas/  # Pydantic request/response contracts
│   │   ├── temporal/ # Workflows & activities
│   │   └── core/     # Security, database, config
│   ├── migrations/   # Alembic revisions
│   └── tests/
├── frontend/         # Next.js application
├── schemas/        # OpenAPI / AsyncAPI contracts
├── docs/           # Controlled documentation
└── scripts/        # Utility & evaluation scripts
```

## Documentation

- [CONTRIBUTING.md](./CONTRIBUTING.md) — development workflow and conventions
- [CLAUDE.md](./CLAUDE.md) — project context and commands for Claude Code
- `docs/` — controlled product, architecture, and governance documents

## License

This project is proprietary and unlicensed unless otherwise specified.
