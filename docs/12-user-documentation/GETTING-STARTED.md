---
document_id: UG-GETTING-STARTED
title: Guide de démarrage - Agent OS
version: 0.2.0
status: draft
owner: documentation-owner
approvers:
  - product-owner
created: 2026-07-20
last_reviewed: 2026-08-13
classification: public
source_of_truth: false
related_documents:
  - VSN-001
  - SCP-001
  - PRD-001
  - UG-INSTALLATION
  - UG-API-REFERENCE
related_adrs:
  - ADR-002
---

# Guide de démarrage — Agent OS

Ce parcours utilise l'implémentation locale actuelle : Docker Compose, un compte administrateur de bootstrap et l'API FastAPI. Le lancement d'un run crée actuellement un enregistrement `pending`; il ne constitue pas encore la preuve d'une exécution LLM complète.

## 1. Démarrer la stack

Suivez d'abord le [guide d'installation](./INSTALLATION.md), puis vérifiez :

```bash
curl -fsS http://localhost:8080/health
```

L'interface est disponible sur http://localhost:3080 et la documentation interactive sur http://localhost:8080/docs.

## 2. Obtenir un token

Le compte de bootstrap est défini par `ADMIN_EMAIL` et `ADMIN_PASSWORD` dans `.env` :

```bash
export API_URL=http://localhost:8080
export TOKEN=$(curl -fsS -X POST "$API_URL/api/v1/auth/token" \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@example.local","password":"replace-with-a-local-admin-password"}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
```

Remplacez les valeurs d'exemple par celles de votre `.env`. Le token est un bearer token valable 3 600 secondes.

## 3. Créer et consulter un agent

```bash
AGENT_ID=$(curl -fsS -X POST "$API_URL/api/v1/agents/" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"mon-agent","model":"provider/model","capabilities":["text-generation"]}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')

curl -fsS "$API_URL/api/v1/agents/$AGENT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

Les identifiants d'agents sont des UUID. Le champ `model` est une valeur de profil ; la configuration d'un fournisseur LLM et l'exécution réelle ne sont pas encore garanties par ce parcours.

## 4. Créer un run et suivre son état

```bash
RUN_ID=$(curl -fsS -X POST "$API_URL/api/v1/runs/$AGENT_ID/run" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Présente l’état de cet agent","context":{},"options":{"stream":false,"timeout":30}}' \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')

curl -fsS "$API_URL/api/v1/runs/$RUN_ID" \
  -H "Authorization: Bearer $TOKEN"
```

La création retourne HTTP 202 et un run généralement `pending`. Les routes de streaming SSE, de dispatch fournisseur et de workflow Temporal ne sont pas exposées par l'implémentation actuelle ; ne présentez donc pas ce parcours comme une exécution terminée.

## 5. Parcours mémoire minimal

```bash
curl -fsS -X POST "$API_URL/api/v1/memory/" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"key":"demo","content":"Mémoire de démonstration","type":"knowledge","source":"getting-started"}'

curl -fsS "$API_URL/api/v1/memory/search?q=demo&limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

## Limites actuelles

- l'authentification est limitée au compte administrateur configuré dans l'environnement ;
- les outils sont exposés par un registre en mémoire et leur exécution retourne un résultat MVP ;
- les runs sont persistés mais aucun résultat LLM complet n'est produit par ce parcours ;
- les adaptateurs, plugins dynamiques et validation visuelle automatisée restent des capacités à implémenter.

Pour la liste complète des routes et schémas, consultez la [référence API](./API-REFERENCE.md).
