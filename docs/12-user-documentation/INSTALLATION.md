---
document_id: UG-INSTALLATION
title: Guide d'installation - Agent OS
version: 0.2.0
status: draft
owner: documentation-owner
approvers:
  - product-owner
  - operations-owner
created: 2026-07-20
last_reviewed: 2026-08-13
classification: public
source_of_truth: false
related_documents:
  - DEP-001
  - OPS-001
  - SEC-001
related_adrs:
  - ADR-002
---

# Guide d'installation — Agent OS

Ce guide décrit le démarrage local actuellement supporté par le dépôt. Il ne décrit pas un déploiement de production.

## Prérequis

- Git 2.30 ou version ultérieure ;
- Docker Engine et Docker Compose v2 ;
- environ 4 Go d'espace libre pour les images et les volumes de développement.

Python est nécessaire uniquement pour l'exécution locale du backend hors Docker. Le frontend utilise Node.js dans son image Docker ; la version exacte est définie par `frontend/Dockerfile`.

## Installation Docker Compose

Depuis la racine du dépôt :

```bash
cp .env.example .env
```

Modifiez au minimum `POSTGRES_PASSWORD`, `SECRET_KEY`, `ADMIN_EMAIL` et `ADMIN_PASSWORD`. `SECRET_KEY` doit contenir au moins 32 caractères. Ne versionnez jamais `.env`.

Démarrez ensuite la stack canonique :

```bash
docker compose up -d --build
docker compose ps
```

Les services locaux exposés sont :

| Service | URL ou port hôte | Rôle |
|---|---:|---|
| Frontend | http://localhost:3080 | Interface Next.js |
| API | http://localhost:8080 | Control Plane FastAPI |
| Documentation API | http://localhost:8080/docs | Swagger UI |
| PostgreSQL | `localhost:5435` | Base de données locale |
| Redis | `localhost:6381` | Service Redis local |

PostgreSQL et Redis sont principalement consommés par les conteneurs. N'exposez pas ces ports au réseau au-delà du poste de développement sans configuration de sécurité dédiée.

Les migrations sont exécutées par la commande de démarrage du conteneur backend (`alembic upgrade head`). Il n'existe pas de commande séparée `create-admin` : le compte de bootstrap est celui défini par `ADMIN_EMAIL` et `ADMIN_PASSWORD`.

## Vérification

```bash
curl -fsS http://localhost:8080/health
curl -fsS http://localhost:8080/
```

La réponse de santé doit contenir `status: healthy`. Vérifiez aussi que `http://localhost:3080` affiche le frontend.

Pour consulter les journaux :

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

## Exécution locale du backend (optionnelle)

Cette voie est utile pour le développement backend et nécessite une base PostgreSQL et Redis accessibles. Depuis `backend/` :

```bash
python3.12 -m venv .venv-local
source .venv-local/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Configurez les variables attendues par `backend/app/config.py`, notamment `DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, `ADMIN_EMAIL` et `ADMIN_PASSWORD`. Le fichier `config.yml`, `agent_os.server`, `agent_os.cli` et `requirements-dev.txt` ne font pas partie du chemin d'installation actuel.

## Arrêt et réinitialisation locale

```bash
docker compose down
```

Pour supprimer les données persistées de cette installation locale uniquement :

```bash
docker compose down -v
```

Cette dernière commande supprime les volumes PostgreSQL et Redis du projet ; elle ne doit pas être utilisée sur un environnement contenant des données à conserver.

## Dépannage

- `SECRET_KEY must contain at least 32 characters` : corrigez `SECRET_KEY` dans `.env`, puis recréez le backend avec `docker compose up -d --build backend`.
- Le backend ne démarre pas : consultez `docker compose logs backend` et vérifiez que PostgreSQL et Redis sont healthy.
- Le frontend ne répond pas : vérifiez `docker compose logs frontend` et l'accès au port 3080.
- Un port est occupé : modifiez le port hôte dans `docker-compose.yml` et adaptez `NEXT_PUBLIC_API_URL` ou les origines CORS en conséquence.
- Les modifications frontend ne sont pas visibles : redémarrez le service frontend et rechargez la page avec un cache navigateur vidé.

## Références

- [Guide de démarrage](./GETTING-STARTED.md)
- [Référence API](./API-REFERENCE.md)
- [Architecture de déploiement](../09-operations/DEP-001-deployment-architecture-and-environment-strategy-v0.1.0.md)
