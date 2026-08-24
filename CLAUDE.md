# Agent OS — Instructions pour Claude Code

## Vue d'ensemble

Agent OS est un control plane vendor-neutral qui orchestre des agents IA de manière durable, observable et gouvernable. Il sépare la planification (workspaces, projets, missions, tâches, approbations) de l'exécution (workflows Temporal, simulateur/OpenAI) et conserve une preuve immuable pour chaque run.

## Structure du projet

```
agent-os/
├── backend/               # FastAPI + Temporal
│   ├── app/
│   │   ├── api/           # Routers HTTP (agents, auth, control_plane, memory, runs, tools)
│   │   ├── core/          # Config, sécurité, base de données
│   │   ├── models/        # Modèles SQLAlchemy
│   │   ├── schemas/       # Contrats Pydantic
│   │   ├── services/      # Logique métier
│   │   ├── simulator/     # Simulateur déterministe
│   │   ├── temporal/      # Workflows, activities, worker
│   │   └── providers/     # Adaptateurs LLM (OpenAI…)
│   ├── migrations/        # Révisions Alembic
│   ├── tests/             # Tests pytest (DB SQLite temporaire)
│   ├── requirements.txt   # Dépendances complètes (dev + runtime)
│   ├── requirements.runtime.txt
│   ├── pyproject.toml     # Outils Python (pytest, black, isort)
│   └── Dockerfile
├── frontend/              # Next.js 14/15, React, TypeScript
│   ├── src/
│   │   ├── app/           # App Router
│   │   ├── components/    # Composants React
│   │   └── lib/           # API client, hooks
│   └── Dockerfile
├── prototype/             # Prototype Next.js léger avec connexion API minimale
├── docker-compose.yml     # Stack dev (Postgres, Redis, Temporal, backend, worker, frontend)
├── .env.example           # Variables d'environnement de développement
├── schemas/               # OpenAPI / AsyncAPI
├── docs/                  # Documentation contrôlée
└── scripts/               # Scripts utilitaires et évaluations
```

## Commandes courantes

### Backend

```bash
cd backend
.venv/bin/pytest -q                              # tests
.venv/bin/black --check . && .venv/bin/isort --check-only . && .venv/bin/flake8 .  # lint
uvicorn app.main:app --reload                    # serveur local
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm run lint
npm run build
```

### Docker Compose

```bash
cp .env.example .env
# éditer .env (secrets, ports)
docker compose up -d
make migrate                                     # alembic upgrade head
docker compose config --quiet                    # valider la config
```

### Documentation

```bash
python3 scripts/validate_docs.py
python3 scripts/check_openapi_parity.py
```

## Conventions

- Python 3.12, typage explicite, Pydantic v2.
- Formatage avec `black` (88 caractères), imports triés avec `isort`.
- `flake8` : F401 actif sauf dans `__init__.py`.
- Datetimes : utiliser `app.core.time.utcnow()` (timezone-aware UTC) ; plus de `datetime.utcnow()`.
- Migrations Alembic : maintenir la compatibilité SQLite (`batch_alter_table`) et PostgreSQL.
- Tests : base SQLite temporaire par session, migrations appliquées via `alembic upgrade head`.
- Tests d'intégration : `tests/test_api_integration.py` (HTTP) et `tests/test_temporal_integration.py` (Temporal local).

## Points de vigilance

- Ne jamais exposer `SECRET_KEY` ou les credentials LLM.
- Les runs sont idempotents par `(workspace_id, task_id, idempotency_key)`.
- Les endpoints `/approvals`, `/automations`, `/execution-runs`, `/artifacts`, etc. exigent `workspace_id`.
- `allow_credentials=True` est interdit si `*` figure dans `CORS_ORIGINS`.
- Le heartbeat Temporal est encapsulé dans `_safe_heartbeat` pour tolérer les appels hors contexte d'activité (tests unitaires).
- L'authentification se fait par cookie httpOnly `access_token` ; le header `Authorization: Bearer` reste accepté pour les appels scripts/API.

## Statuts des documents contrôlés

- `draft` → En rédaction
- `in-review` → En revue
- `approved` → Approuvé
- `deprecated` → Obsolète
