---
document_id: UG-API-REFERENCE
title: Référence API - Agent OS
version: 0.1.0
status: draft
owner: documentation-owner
approvers:
  - api-owner
  - architecture-owner
created: 2026-07-20
last_reviewed: 2026-07-20
classification: public
source_of_truth: false
related_documents:
  - API-001
  - AGC-001
  - RUN-001
  - APR-001
related_adrs: []
---

# Référence API - Agent OS

**Version:** 0.1.0
**Base URL:** `http://localhost:8080/api/v1`

## Table des Matières

1. [Authentification](#authentification)
2. [Agents](#agents)
3. [Exécution](#exécution)
4. [Mémoire](#mémoire)
5. [Outils](#outils)
6. [Politiques](#politiques)
7. [Monitoring](#monitoring)

---

## Authentification

Toutes les requêtes API nécessitent un token d'authentification.

### Obtenir un Token

```http
POST /auth/token
Content-Type: application/json

{
  "email": "utilisateur@example.com",
  "password": "mot-de-passe"
}
```

**Réponse:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Utiliser le Token

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

## Agents

### Liste des Agents

```http
GET /agents
```

**Paramètres Query:**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Nombre max de résultats (défaut: 20) |
| `offset` | integer | Décalage pour la pagination |
| `status` | string | Filtrer par statut: `active`, `inactive`, `error` |

**Réponse:**

```json
{
  "agents": [
    {
      "id": "agent_abc123",
      "name": "agent-analyse",
      "model": "gpt-4",
      "status": "active",
      "capabilities": ["text-generation", "code-analysis"],
      "created_at": "2026-07-20T10:00:00Z",
      "updated_at": "2026-07-20T10:00:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

### Créer un Agent

```http
POST /agents
Content-Type: application/json

{
  "name": "agent-analyse",
  "model": "gpt-4",
  "capabilities": ["text-generation", "code-analysis"],
  "config": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "policies": {
    "autonomy_level": "supervised",
    "requires_approval": ["file-write", "api-call"]
  }
}
```

**Réponse:**

```json
{
  "id": "agent_abc123",
  "name": "agent-analyse",
  "model": "gpt-4",
  "status": "active",
  "capabilities": ["text-generation", "code-analysis"],
  "config": {
    "temperature": 0.7,
    "max_tokens": 4096
  },
  "policies": {
    "autonomy_level": "supervised",
    "requires_approval": ["file-write", "api-call"]
  },
  "created_at": "2026-07-20T10:00:00Z"
}
```

### Obtenir un Agent

```http
GET /agents/{agent_id}
```

### Mettre à Jour un Agent

```http
PATCH /agents/{agent_id}
Content-Type: application/json

{
  "config": {
    "temperature": 0.5
  }
}
```

### Supprimer un Agent

```http
DELETE /agents/{agent_id}
```

---

## Exécution

### Lancer une Exécution

```http
POST /agents/{agent_id}/run
Content-Type: application/json

{
  "prompt": "Analyse ce code et suggère des améliorations",
  "context": {
    "code": "def hello(): print('Hello World')",
    "language": "python"
  },
  "options": {
    "stream": false,
    "timeout": 30
  }
}
```

**Réponse (synchrone):**

```json
{
  "execution_id": "exec_xyz789",
  "status": "completed",
  "result": {
    "response": "Voici mes suggestions d'améliorations...",
    "tokens_used": 256,
    "cost": 0.005
  },
  "started_at": "2026-07-20T10:00:00Z",
  "completed_at": "2026-07-20T10:00:05Z"
}
```

### Lancer une Exécution Streamée

```http
POST /agents/{agent_id}/run
Content-Type: application/json

{
  "prompt": "Raconte-moi une histoire",
  "options": {
    "stream": true
  }
}
```

**Réponse (SSE):**

```
data: {"chunk": "Il"}
data: {"chunk": " était"}
data: {"chunk": " une"}
data: {"chunk": " fois"}
data: [DONE]
```

### Annuler une Exécution

```http
POST /executions/{execution_id}/cancel
```

### Obtenir le Statut d'une Exécution

```http
GET /executions/{execution_id}
```

---

## Mémoire

### Ajouter à la Mémoire

```http
POST /memory
Content-Type: application/json

{
  "key": "contexte-projet",
  "content": "Le projet Agent OS utilise une architecture hexagonale",
  "metadata": {
    "type": "knowledge",
    "source": "documentation",
    "agent_id": "agent_abc123"
  },
  "ttl": 86400  // Time to live en secondes (optionnel)
}
```

### Rechercher dans la Mémoire

```http
GET /memory/search?q=architecture+hexagonale&limit=10
```

**Réponse:**

```json
{
  "results": [
    {
      "key": "contexte-projet",
      "content": "Le projet Agent OS utilise une architecture hexagonale",
      "score": 0.95,
      "metadata": {
        "type": "knowledge",
        "created_at": "2026-07-20T10:00:00Z"
      }
    }
  ]
}
```

### Récupérer par Clé

```http
GET /memory/{key}
```

### Supprimer

```http
DELETE /memory/{key}
```

---

## Outils

### Liste des Outils Disponibles

```http
GET /tools
```

**Réponse:**

```json
{
  "tools": [
    {
      "id": "tool_web_search",
      "name": "Recherche Web",
      "description": "Rechercher sur internet",
      "category": "research",
      "requires_approval": false
    },
    {
      "id": "tool_code_execute",
      "name": "Exécuter du Code",
      "description": "Exécuter du code Python",
      "category": "development",
      "requires_approval": true
    }
  ]
}
```

### Exécuter un Outil

```http
POST /tools/{tool_id}/execute
Content-Type: application/json

{
  "parameters": {
    "query": "Agent OS architecture"
  },
  "agent_id": "agent_abc123"
}
```

---

## Politiques

### Obtenir les Politiques d'un Agent

```http
GET /agents/{agent_id}/policies
```

### Mettre à Jour les Politiques

```http
PATCH /agents/{agent_id}/policies
Content-Type: application/json

{
  "autonomy_level": "supervised",
  "requires_approval": ["file-write", "api-call", "database-write"],
  "budget_limit": 100.00,
  "rate_limit": {
    "requests_per_minute": 60
  },
  "security": {
    "sandbox_enabled": true,
    "allowed_domains": ["github.com", "stackoverflow.com"],
    "blocked_patterns": ["DROP TABLE", "DELETE FROM"]
  }
}
```

---

## Monitoring

### Métriques

```http
GET /metrics
```

**Réponse (Prometheus format):**

```
# HELP agent_os_requests_total Total des requêtes
# TYPE agent_os_requests_total counter
agent_os_requests_total{method="POST",endpoint="/agents"} 42

# HELP agent_os_tokens_used Total des tokens utilisés
# TYPE agent_os_tokens_used counter
agent_os_tokens_used{model="gpt-4"} 15000

# HELP agent_os_cost_usd Total des coûts en USD
# TYPE agent_os_cost_usd counter
agent_os_cost_usd{model="gpt-4"} 15.50
```

### Logs d'Audit

```http
GET /audit/logs
```

**Paramètres:**

| Paramètre | Type | Description |
|-----------|------|-------------|
| `start_date` | ISO 8601 | Date de début |
| `end_date` | ISO 8601 | Date de fin |
| `agent_id` | string | Filtrer par agent |
| `action` | string | Filtrer par action |

---

## Codes d'Erreur

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 201 | Créé |
| 400 | Requête invalide |
| 401 | Non authentifié |
| 403 | Non autorisé |
| 404 | Ressource non trouvée |
| 429 | Trop de requêtes (rate limit) |
| 500 | Erreur serveur |

## Limites de Débit

| Plan | Requêtes/minute | Tokens/jour |
|------|-----------------|-------------|
| Gratuit | 20 | 100,000 |
| Pro | 100 | 1,000,000 |
| Enterprise | Illimité | Illimité |

---

## Exemples de Requêtes

### cURL

```bash
# Créer un agent
curl -X POST http://localhost:8080/api/v1/agents \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "mon-agent",
    "model": "gpt-4"
  }'
```

### Python

```python
import requests

# Configuration
BASE_URL = "http://localhost:8080/api/v1"
TOKEN = "votre-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Créer un agent
response = requests.post(
    f"{BASE_URL}/agents",
    headers=headers,
    json={
        "name": "mon-agent",
        "model": "gpt-4"
    }
)

agent = response.json()
print(f"Agent créé: {agent['id']}")
```

### JavaScript

```javascript
const BASE_URL = 'http://localhost:8080/api/v1';
const TOKEN = 'votre-token';

// Créer un agent
const response = await fetch(`${BASE_URL}/agents`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    name: 'mon-agent',
    model: 'gpt-4'
  })
});

const agent = await response.json();
console.log(`Agent créé: ${agent.id}`);
```
