---
document_id: UG-API-REFERENCE
title: Référence API - Agent OS
version: 0.2.0
status: draft
owner: documentation-owner
approvers:
  - api-owner
  - architecture-owner
created: 2026-07-20
last_reviewed: 2026-08-13
classification: public
source_of_truth: false
related_documents:
  - API-001
  - AGC-001
  - RUN-001
  - APR-001
related_adrs:
  - ADR-002
---

# Référence API — Agent OS

Cette référence décrit les routes actuellement montées par `backend/app/main.py`. Le contrat interactif généré par FastAPI est disponible sur `http://localhost:8080/docs` et `http://localhost:8080/openapi.json` lorsque le backend est démarré.

## Convention

- Base locale : `http://localhost:8080` ;
- préfixe API : `/api/v1` ;
- les routes protégées exigent `Authorization: Bearer <token>` ;
- les identifiants de ressources sont des UUID sauf indication contraire ;
- les chemins terminés par `/` sont les chemins canoniques exposés par les routeurs FastAPI.

Les routes `/`, `/health` et `/api/v1/auth/token` sont publiques. Les autres routes documentées ici sont protégées.

## Authentification

### `POST /api/v1/auth/token`

Obtient un token pour le compte de bootstrap configuré par `ADMIN_EMAIL` et `ADMIN_PASSWORD`.

```json
{"email":"admin@example.local","password":"mot-de-passe"}
```

Réponse `200` :

```json
{"access_token":"<jwt>","token_type":"bearer","expires_in":3600}
```

Réponses possibles : `401` identifiants invalides, `503` authentification non configurée.

## Agents

### `GET /api/v1/agents/`

Liste les agents. Query parameters : `limit` (défaut 20), `offset` (défaut 0), `status` (optionnel). La réponse est un tableau d'agents, pas un objet paginé.

### `POST /api/v1/agents/`

Crée un agent :

```json
{
  "name":"mon-agent",
  "model":"provider/model",
  "description":"Agent de démonstration",
  "capabilities":["text-generation"],
  "config":{},
  "policies":{}
}
```

Réponse `201` : agent avec `id`, `status`, compteurs d'exécution, dates et champs fournis.

### `GET /api/v1/agents/{agent_id}`

Retourne un agent. `404` si l'UUID n'existe pas.

### `PATCH /api/v1/agents/{agent_id}`

Met à jour partiellement `name`, `model`, `status`, `description`, `capabilities`, `config` ou `policies`.

### `DELETE /api/v1/agents/{agent_id}`

Supprime l'agent. Réponse `204` en cas de succès.

## Runs

### `GET /api/v1/runs/`

Liste les runs. Query parameters : `limit`, `offset`, `agent_id`, `status`.

### `POST /api/v1/runs/{agent_id}/run`

Crée un run persistant et retourne HTTP `202` :

```json
{
  "prompt":"Présente l’état de cet agent",
  "context":{},
  "options":{"stream":false,"timeout":30}
}
```

Le backend actuel crée le run avec `status: "pending"`. Le champ `stream` est accepté dans le schéma, mais aucune route SSE ou WebSocket n'est implémentée et aucun résultat fournisseur n'est garanti.

### `GET /api/v1/runs/{run_id}`

Retourne le run avec `status`, `prompt`, `context`, `options`, `result`, `error`, `progress`, `steps`, `tokens_used`, `cost`, `started_at`, `completed_at` et `created_at`.

### `POST /api/v1/runs/{run_id}/cancel`

Annule un run `pending` ou `running`. Réponse `400` si son état ne permet pas l'annulation, `404` si le run est inconnu.

## Mémoire

### `POST /api/v1/memory/`

Crée ou remplace la mémoire correspondant à `key` :

```json
{
  "key":"contexte-projet",
  "content":"Mémoire de démonstration",
  "type":"knowledge",
  "source":"documentation",
  "agent_id":null,
  "metadata_":{},
  "ttl":86400
}
```

### `GET /api/v1/memory/search?q=<texte>&limit=10`

Recherche dans `key` et `content`. Réponse : `{"results":[...],"total":<entier>}`.

### `GET /api/v1/memory/{key}` et `DELETE /api/v1/memory/{key}`

Récupère ou supprime une mémoire. La lecture incrémente le compteur d'accès. Réponses `404` si la clé n'existe pas ; suppression réussie : `204`.

## Outils

### `GET /api/v1/tools/`

Retourne le registre d'outils actuellement en mémoire. Il contient les entrées MVP visibles dans `backend/app/api/tools.py`.

### `POST /api/v1/tools/{tool_id}/execute`

Accepte :

```json
{"parameters":{},"agent_id":"<uuid-ou-identifiant>"}
```

La réponse est `{ "success": true, "output": {...}, "error": null }` pour les outils connus. L'implémentation actuelle retourne un résultat MVP et ne doit pas être interprétée comme l'exécution réelle d'une commande système.

## Control Plane

Toutes les routes suivantes sont protégées.

| Méthode | Route | Objet |
|---|---|---|
| `GET` / `POST` | `/api/v1/workspaces` | Lister/créer des espaces de travail |
| `GET` / `POST` | `/api/v1/missions` | Lister/créer des missions |
| `PATCH` | `/api/v1/missions/{mission_id}/status` | Modifier statut et progression |
| `GET` / `POST` | `/api/v1/automations` | Lister/créer des automatisations |
| `GET` | `/api/v1/approvals` | Lister les approbations, filtre `status` |
| `POST` | `/api/v1/approvals` | Créer une demande d'approbation |
| `POST` | `/api/v1/approvals/{approval_id}/decision` | Décider `approved` ou `rejected` |
| `GET` | `/api/v1/audit-events` | Lire les événements, `workspace_id` obligatoire, `limit` 1–200 |

Les schémas exacts de ces ressources sont consultables dans `/openapi.json` et dans `backend/app/schemas/control_plane.py`.

## Routes publiques et absence de routes

- `GET /health` retourne `{ "status": "healthy", "version": "..." }`.
- `GET /` retourne le nom, la version et le chemin de documentation.
- Il n'existe actuellement aucune route `/metrics`, `/audit/logs`, `/policies`, `/executions/{id}`, SSE ou WebSocket.
- Les quotas, plans commerciaux et limites de débit ne sont pas implémentés par ce backend et ne sont donc pas documentés comme fonctionnalités.

## Erreurs communes

`401` token absent/invalide, `403` refus d'autorisation par la couche de sécurité, `404` ressource inconnue, `409` conflit d'état, `422` validation FastAPI/Pydantic, `500` erreur serveur et `503` service non configuré.

## Source machine-readable

La source machine-readable locale est l'OpenAPI généré par FastAPI (`/openapi.json`). `schemas/openapi.yaml` doit rester synchronisé avec les routes réellement montées avant de pouvoir servir de contrat de publication. Cette référence narrative ne constitue pas une preuve d'exécution fournisseur, de streaming, de plugin ou de déploiement production.
