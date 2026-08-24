# Contribuer à Agent OS

Merci de votre intérêt pour Agent OS ! Ce guide explique comment contribuer au projet.

## Prérequis

- Python 3.12
- Node.js 20
- Docker & Docker Compose
- Git

## Démarrage rapide

```bash
# Cloner le dépôt
git clone https://github.com/raillersing/agent-os.git
cd agent-os

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec des secrets locaux (SECRET_KEY, ADMIN_PASSWORD, LLM keys)

# Lancer la stack de développement (Postgres, Redis, Temporal, backend, worker, frontend)
docker compose up -d
make migrate

# Vérifier l'état
make status
make logs-backend
```

## Développement backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

## Développement frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:3080 avec NEXT_PUBLIC_API_URL
npm run lint
npm run build
```

## Prototype

```bash
cd prototype
npm install
npm run dev
npm run build
```

## Structure du code

```
backend/
├── app/
│   ├── api/        # Routes FastAPI
│   ├── core/       # Sécurité, configuration, base de données
│   ├── models/     # Modèles SQLAlchemy
│   ├── schemas/    # Contrats Pydantic
│   ├── services/   # Logique métier réutilisable
│   ├── temporal/   # Workflows et activités Temporal
│   └── simulator/  # Simulateur déterministe D0/D1
├── migrations/     # Révisions Alembic
└── tests/          # Tests pytest hermétiques

frontend/
├── src/
│   ├── app/        # Routes Next.js App Router
│   ├── components/ # Composants React
│   └── lib/        # Appels API et utilitaires
```

## Style et qualité

- Python : `black`, `isort`, `flake8` (configuration dans `.flake8` et `backend/pyproject.toml`)
- TypeScript / Next.js : ESLint, `next build`
- Les migrations Alembic doivent rester compatibles SQLite et PostgreSQL (utiliser `batch_alter_table` pour SQLite)
- Les datetimes backend doivent être timezone-aware via `app.core.time.utcnow()`

## Tests

- Backend : `cd backend && pytest -q` (base SQLite temporaire par session)
- Intégration HTTP : `tests/test_api_integration.py`
- Intégration Temporal : `tests/test_temporal_integration.py`

## Pull requests

1. Créer une branche depuis `main`.
2. Faire des commits atomiques et explicites.
3. S'assurer que `pytest -q`, `make lint` et `docker compose config --quiet` passent.
4. Ouvrir une Pull Request avec une description claire.

## Signalement de bugs

Ouvrir une issue avec :
- Le contexte et les étapes de reproduction
- Le comportement attendu vs observé
- Les logs et captures d'écran si pertinent

## Conduite

- Respecter les autres contributeurs
- Privilégier la sécurité et la maintenabilité
- Documenter les changements de contrat API ou de schéma
