---
document_id: API-002
title: Agent OS v2 Goldie Edition API Specification
version: 2.1.0
status: draft
owner: api-owner
approvers:
  - api-owner
  - architecture-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents: [API-001, AGC-001, RUN-001, APR-001]
related_adrs: []
---

# Agent OS v2 — API Specification

## Goldie Edition

**Version:** 2.1.0-Goldie
**Base URL:** `https://agentos.local`
**Date:** 2026-08-11

---

## 1. API Versioning Strategy

Agent OS follows **URL-path versioning** with a single active version:

```
/api/v1/…
```

| Rule | Detail |
|------|--------|
| Active version | `v1` (current) |
| Deprecated versions | Respond with `410 Gone` and a sunset header |
| Breaking changes | Bump to `v2` |
| Non-breaking additions | Stay on `v1`; document in changelog |
| Sunset header | `Sunset: <date>` + `Deprecation: true` on deprecated endpoints |

All endpoints in this spec are prefixed with `/api/v1/` unless noted otherwise.

---

## 2. Authentication

### 2.1 JWT Bearer Tokens

Every protected endpoint requires an `Authorization` header:

```
Authorization: Bearer <access_token>
```

Token claims:

| Claim | Type | Description |
|-------|------|-------------|
| `sub` | UUID | User ID |
| `wid` | UUID | Active workspace ID |
| `role` | string | `owner`, `operator`, `approver`, `contributor`, `auditor` |
| `iat` | int | Issued at (epoch) |
| `exp` | int | Expires at (epoch) |
| `jti` | string | Token unique ID (for revocation) |

Access token TTL: **15 minutes**
Refresh token TTL: **7 days**

### 2.2 Refresh Flow

```
POST /api/v1/auth/refresh
```

Request:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 900
}
```

Rotation: every refresh issues a **new pair** and invalidates the old refresh token.
Grace window: **30 seconds** overlap for concurrent requests.

### 2.3 Logout

```
POST /api/v1/auth/logout
```

Invalidates the refresh token on the server (stored in Redis blocklist).
Clients must also purge local tokens.

---

## 3. Error Response Format (RFC 7807 Problem Details)

Every error response uses `Content-Type: application/problem+json`:

```json
{
  "type": "https://agentos.local/errors/invalid-credentials",
  "title": "Invalid credentials",
  "status": 401,
  "detail": "The email or password provided is incorrect.",
  "instance": "/api/v1/auth/login",
  "trace_id": "abc123-def456",
  "errors": {
    "email": ["Invalid email format."]
  }
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `type` | Yes | URI identifying the error type |
| `title` | Yes | Short, human-readable summary |
| `status` | Yes | HTTP status code |
| `detail` | Yes | Detailed, human-readable explanation |
| `instance` | Yes | Request path |
| `trace_id` | Yes | Correlation ID for logs |
| `errors` | No | Per-field validation errors |

Standard error types:

| Status | Type URI | When |
|--------|----------|------|
| 400 | `/errors/validation-failed` | Request body/schema invalid |
| 401 | `/errors/unauthorized` | Missing or invalid token |
| 403 | `/errors/forbidden` | Insufficient permissions |
| 404 | `/errors/not-found` | Resource does not exist |
| 409 | `/errors/conflict` | Resource already exists / state conflict |
| 422 | `/errors/unprocessable` | Semantic validation failed |
| 429 | `/errors/rate-limited` | Rate limit exceeded |
| 500 | `/errors/internal` | Server error |
| 503 | `/errors/service-unavailable` | Gateway or downstream unavailable |

---

## 4. Pagination Conventions

All list endpoints use **cursor-based pagination**.

### Request Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | int | 20 | Items per page (max 100) |
| `cursor` | string | — | opaque cursor from previous response |
| `direction` | enum | `next` | `next` or `previous` |

### Response Envelope

```json
{
  "data": […],
  "pagination": {
    "limit": 20,
    "next_cursor": "eyJpZCI6…",
    "prev_cursor": null,
    "has_more": true,
    "total": null
  }
}
```

> `total` is omitted by default for performance. Include `?count=true` to request it.

### Sorting

Use `sort` (e.g., `sort=-created_at,+name`).
Prefix `-` for descending, `+` or no prefix for ascending.

---

## 5. Rate Limiting

Headers returned on every response:

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Requests allowed per window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Epoch seconds until window resets |

### Limits

| Tier | Window | Limit |
|------|--------|-------|
| Anonymous | 1 min | 10 req/min |
| Authenticated | 1 min | 120 req/min |
| SSE/WS | — | 5 concurrent streams |
| Gateway proxy | 1 min | 60 req/min per provider |

On `429`:
```json
{
  "type": "/errors/rate-limited",
  "title": "Rate limit exceeded",
  "status": 429,
  "detail": "Limit: 120 req/min. Retry after 45s.",
  "instance": "/api/v1/agents",
  "retry_after": 45
}
```

---

## 6. Endpoint Catalog

### 6.1 Auth

#### POST `/auth/login`
- **Auth:** No
- **Request:**
```json
{
  "email": "user@example.com",
  "password": "hunter2",
  "mfa_code": "123456"
}
```
- **Response:**
```json
{
  "access_token": "eyJ…",
  "refresh_token": "eyJ…",
  "token_type": "Bearer",
  "expires_in": 900,
  "user": { "id": "…", "email": "user@example.com", "name": "Ada Lovelace" }
}
```
- **Curl:**
```bash
curl -X POST https://agentos.local/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"hunter2"}'
```

#### POST `/auth/refresh`
- **Auth:** No (requires refresh_token body)
- **Request:** `{ "refresh_token": "eyJ…" }`
- **Response:** New token pair (see §2.2)

#### POST `/auth/logout`
- **Auth:** Bearer
- **Request:** `{}`
- **Response:** `204 No Content`

#### GET `/auth/me`
- **Auth:** Bearer
- **Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "name": "Ada Lovelace",
  "avatar_url": "https://…",
  "workspace": { "id": "uuid", "name": "Acme Corp", "role": "owner" }
}
```

#### GET `/dashboard`
- **Auth:** Bearer
- **Response:**
```json
{
  "active_agents": 3,
  "pending_tasks": 12,
  "awaiting_approvals": 4,
  "daily_cost_usd": 1.23,
  "system_health": "healthy",
  "agents": [
    { "id": "uuid", "name": "Claude", "status": "online", "last_heartbeat": "2026-08-11T12:00:00Z" }
  ],
  "recent_tasks": []
}
```

---

### 6.2 Agents

#### GET `/agents`
- **Auth:** Bearer
- **Query:** `?limit=20&cursor=&sort=+name`
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Claude",
      "slug": "claude",
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "color": "#F97316",
      "status": "online",
      "skills": ["chat", "code", "vision"],
      "created_at": "2026-08-01T12:00:00Z"
    }
  ],
  "pagination": {…}
}
```

#### POST `/agents`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "name": "Grok Beta",
  "slug": "grok-beta",
  "provider": "xai",
  "model": "grok-3-beta",
  "color": "#EC4899",
  "skills": ["chat", "web_search"],
  "config": { "temperature": 0.7, "max_tokens": 4096 }
}
```

#### GET `/agents/{agent_id}`
- **Auth:** Bearer
- **Response:** Single agent object with full config

#### PATCH `/agents/{agent_id}`
- **Auth:** Bearer (owner/operator)
- **Request:** Partial agent fields

#### DELETE `/agents/{agent_id}`
- **Auth:** Bearer (owner)
- **Response:** `204`

#### GET `/agents/{agent_id}/status`
- **Auth:** Bearer
- **Response:** `{ "status": "online", "last_seen": "2026-08-11T16:50:00Z", "latency_ms": 42 }`

#### GET `/agents/{agent_id}/skills`
- **Auth:** Bearer
- **Response:** `{ "skills": [{ "id": "uuid", "name": "code", "version": "1.0.0" }] }`

#### POST `/agents/{agent_id}/skills`
- **Auth:** Bearer (owner/operator)
- **Request:** `{ "skill_id": "uuid" }`

---

### 6.3 Tasks / Goals

#### POST `/tasks`
- **Auth:** Bearer
- **Request:**
```json
{
  "title": "Refactor auth module",
  "description": "Migrate from Flask-JWT to python-jose",
  "agent_id": "uuid",
  "priority": "high",
  "due_date": "2026-08-15T00:00:00Z",
  "tags": ["backend", "security"]
}
```
- **Response:** `201 Created` with task object including `dag_status: pending`

#### GET `/tasks`
- **Auth:** Bearer
- **Query:** `?status=running&agent_id=uuid&limit=20&cursor=`
- **Response:** Paginated task list

#### GET `/tasks/{task_id}`
- **Auth:** Bearer
- **Response:** Full task with `dag_root_id` and `progress_pct`

#### DELETE `/tasks/{task_id}`
- **Auth:** Bearer
- **Response:** `204`

#### POST `/tasks/{task_id}/cancel`
- **Auth:** Bearer
- **Response:** `202 Accepted` — signal sent to Celery workers

#### GET `/tasks/{task_id}/nodes`
- **Auth:** Bearer
- **Response:** DAG drill-down
```json
{
  "nodes": [
    { "id": "n1", "type": "root", "status": "completed", "agent_id": "uuid", "output_preview": "…" },
    { "id": "n2", "type": "parallel", "status": "running", "depends_on": ["n1"] },
    { "id": "n3", "type": "parallel", "status": "pending", "depends_on": ["n1"] }
  ],
  "edges": [["n1","n2"],["n1","n3"]]
}
```

---

### 6.4 Task Nodes

#### PATCH `/task-nodes/{node_id}`
- **Auth:** Bearer
- **Request:** `{ "status": "completed", "output": "…", "exit_code": 0 }`

#### POST `/task-nodes/{node_id}/retry`
- **Auth:** Bearer
- **Response:** `202` — re-queues the node

#### GET `/task-nodes/{node_id}/output`
- **Auth:** Bearer
- **Response:** `{ "stdout": "…", "stderr": "", "artifacts": ["artifact_uuid"] }`

---

### 6.5 Chat

#### POST `/chat/sessions`
- **Auth:** Bearer
- **Request:** `{ "agent_id": "uuid", "title": "Q3 Planning" }`
- **Response:** `201` with session object

#### GET `/chat/sessions`
- **Auth:** Bearer
- **Response:** Paginated sessions

#### GET `/chat/sessions/{session_id}/messages`
- **Auth:** Bearer
- **Response:** Paginated messages

#### POST `/chat/sessions/{session_id}/messages`
- **Auth:** Bearer
- **Request:** `{ "role": "user", "content": "Hello Claude", "attachments": ["file_uuid"] }`
- **Response:** Triggers SSE stream (see §7.1)

#### DELETE `/chat/sessions/{session_id}`
- **Auth:** Bearer
- **Response:** `204`

---

### 6.6 Notebook

#### GET `/notes`
- **Auth:** Bearer
- **Query:** `?q=search&sort=-updated_at`
- **Response:** Paginated notes

#### POST `/notes`
- **Auth:** Bearer
- **Request:**
```json
{
  "title": "Architecture Decision",
  "body": "## Context\nWe chose FastAPI because…",
  "tags": ["adr", "backend"],
  "links_to": ["note_uuid_2"]
}
```

#### GET `/notes/{note_id}`
- **Auth:** Bearer
- **Response:** Note with `backlinks: […]` computed

#### PATCH `/notes/{note_id}`
- **Auth:** Bearer

#### DELETE `/notes/{note_id}`
- **Auth:** Bearer
- **Response:** `204`

#### GET `/notes/search`
- **Auth:** Bearer
- **Query:** `?q=FastAPI&limit=20`
- **Response:** Full-text search results via SQLite FTS5 / PostgreSQL tsvector

#### GET `/notes/semantic`
- **Auth:** Bearer
- **Query:** `?q=async database patterns&limit=10`
- **Response:** Semantic search via pgvector / SQLite-vec

---

### 6.7 Studio

#### POST `/studio/generate`
- **Auth:** Bearer
- **Request:**
```json
{
  "type": "image",
  "prompt": "A futuristic agent OS dashboard",
  "model": "dall-e-3",
  "size": "1024x1024",
  "n": 1
}
```
- **Response:** `202` with job ID

#### GET `/studio/jobs`
- **Auth:** Bearer
- **Response:** Paginated generation jobs

#### GET `/studio/jobs/{job_id}`
- **Auth:** Bearer
- **Response:** `{ "id": "…", "status": "completed", "result_url": "https://…", "metadata": {} }`

#### DELETE `/studio/jobs/{job_id}`
- **Auth:** Bearer
- **Response:** `202` — cancels pending job

---

### 6.8 Mission Board (Kanban)

#### GET `/board/columns`
- **Auth:** Bearer
- **Response:** Array of columns with cards

#### POST `/board/cards`
- **Auth:** Bearer
- **Request:** `{ "title": "Fix N+1", "column": "todo", "task_id": "uuid", "assignee_id": "uuid" }`

#### PATCH `/board/cards/{card_id}/move`
- **Auth:** Bearer
- **Request:** `{ "column": "in_progress", "position": 2 }`

#### DELETE `/board/cards/{card_id}`
- **Auth:** Bearer
- **Response:** `204` (archives, does not hard-delete)

---

### 6.9 Gateway (Hermes Proxy)

Base path: `/api/v1/gateway`

#### POST `/gateway/complete`
- **Auth:** Bearer
- **Request:**
```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "messages": [{"role":"user","content":"Hello"}],
  "stream": true,
  "temperature": 0.7
}
```
- **Response:** SSE stream or JSON completion

#### GET `/gateway/models`
- **Auth:** Bearer
- **Query:** `?provider=anthropic`
- **Response:** Array of available models

#### GET `/gateway/models/{model_id}`
- **Auth:** Bearer
- **Response:** Model metadata (context window, pricing, capabilities)

---

### 6.11 Verifier

#### GET `/verifier/results/{run_id}`
- **Auth:** Bearer
- **Response:** Verification report with pass/fail per assertion

#### GET `/verifier/queue`
- **Auth:** Bearer (operator/approver)
- **Response:** Human review queue items

#### POST `/verifier/queue/{item_id}/review`
- **Auth:** Bearer (operator/approver)
- **Request:** `{ "action": "approve", "comment": "Looks good" }`

---

### 6.12 Approvals

#### GET `/approvals`
- **Auth:** Bearer
- **Query:** `?status=pending&limit=20`
- **Response:** Pending approvals for the user

#### POST `/approvals/{approval_id}/approve`
- **Auth:** Bearer
- **Request:** `{ "comment": "Approved — proceed with deploy" }`

#### POST `/approvals/{approval_id}/reject`
- **Auth:** Bearer
- **Request:** `{ "reason": "Security concern in step 3" }`

#### POST `/approvals/{approval_id}/revise`
- **Auth:** Bearer
- **Request:** `{ "reason": "string", "new_deadline": "string" }`

---

### 6.13 Workspace

#### GET `/workspace`
- **Auth:** Bearer
- **Response:** Current workspace details

#### PATCH `/workspace`
- **Auth:** Bearer (owner/operator)
- **Request:** `{ "name": "New Name", "settings": {…} }`

#### GET `/workspace/branding`
- **Auth:** Bearer
- **Response:** `{ "logo_url": "…", "primary_color": "#A855F7", "favicon": "…" }`

#### PATCH `/workspace/branding`
- **Auth:** Bearer (owner/operator)

#### GET `/workspace/members`
- **Auth:** Bearer
- **Response:** Members with roles

#### POST `/workspace/members`
- **Auth:** Bearer (owner/operator)
- **Request:** `{ "email": "new@example.com", "role": "contributor" }`

#### DELETE `/workspace/members/{user_id}`
- **Auth:** Bearer (owner/operator)

---

### 6.14 Audit

#### GET `/audit/events`
- **Auth:** Bearer (operator/approver)
- **Query:** `?entity_type=task&entity_id=uuid&from=2026-08-01&to=2026-08-11`
- **Response:** Paginated audit trail

#### GET `/audit/events/export`
- **Auth:** Bearer (operator/approver)
- **Query:** `?format=csv|json`
- **Response:** `200` with `Content-Disposition: attachment`

---

### 6.15 SEO Module

#### GET `/seo/campaigns`
- **Auth:** Bearer
- **Query:** `?status=active&limit=20&cursor=`
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Q3 Organic Growth",
      "target_domain": "goldie.agency",
      "target_locale": "en-US",
      "status": "active",
      "start_date": "2026-07-01",
      "end_date": "2026-09-30",
      "budget_usd": 50000.00,
      "keyword_count": 124,
      "created_at": "2026-07-01T00:00:00Z"
    }
  ],
  "pagination": {…}
}
```

#### POST `/seo/campaigns`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "name": "Q3 Organic Growth",
  "target_domain": "goldie.agency",
  "target_locale": "en-US",
  "start_date": "2026-07-01",
  "end_date": "2026-09-30",
  "budget_usd": 50000.00
}
```
- **Response:** `201 Created`

#### GET `/seo/campaigns/{campaign_id}`
- **Auth:** Bearer
- **Response:** Campaign object with `summary: { keywords, rankings, competitors, briefs }`

#### PATCH `/seo/campaigns/{campaign_id}`
- **Auth:** Bearer (owner/operator)

#### DELETE `/seo/campaigns/{campaign_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### GET `/seo/campaigns/{campaign_id}/keywords`
- **Auth:** Bearer
- **Query:** `?intent=informational&cluster_id=uuid&limit=50`
- **Response:** Paginated keyword list with latest position

#### POST `/seo/campaigns/{campaign_id}/keywords`
- **Auth:** Bearer
- **Request:**
```json
{
  "keyword": "ai agent operating system",
  "search_volume": 1200,
  "difficulty": 45,
  "intent": "informational",
  "priority": 1
}
```

#### POST `/seo/campaigns/{campaign_id}/keywords/bulk`
- **Auth:** Bearer
- **Request:** `{ "keywords": ["kw1", "kw2", "kw3"] }`
- **Response:** `{ "created": 3, "skipped": 0 }`

#### GET `/seo/campaigns/{campaign_id}/keywords/{keyword_id}`
- **Auth:** Bearer
- **Response:** Keyword with `history: [ { position, scraped_at } ]`

#### GET `/seo/campaigns/{campaign_id}/keywords/{keyword_id}/rankings`
- **Auth:** Bearer
- **Query:** `?from=2026-07-01&to=2026-08-11&device=desktop`
- **Response:** Time-series ranking data

#### POST `/seo/keywords/{keyword_id}/track`
- **Auth:** Bearer
- **Request:** `{ "engines": ["google","bing"], "devices": ["desktop","mobile"] }`
- **Response:** `202 Accepted` with background job ID

#### GET `/seo/campaigns/{campaign_id}/competitors`
- **Auth:** Bearer
- **Response:** Competitor list with `last_metrics: { domain_authority, organic_traffic }`

#### POST `/seo/campaigns/{campaign_id}/competitors`
- **Auth:** Bearer
- **Request:**
```json
{
  "domain": "competitor.com",
  "display_name": "Competitor Inc",
  "watch_urls": ["https://competitor.com/blog"],
  "alert_on_rank_change": true,
  "alert_threshold_pct": 5.0
}
```

#### GET `/seo/competitors/{competitor_id}/changes`
- **Auth:** Bearer
- **Query:** `?since=7d`
- **Response:** Array of detected content/rank changes

#### GET `/seo/campaigns/{campaign_id}/briefs`
- **Auth:** Bearer
- **Response:** Content brief list

#### POST `/seo/campaigns/{campaign_id}/briefs`
- **Auth:** Bearer
- **Request:**
```json
{
  "target_keyword": "ai agent operating system",
  "tone": "professional",
  "suggested_word_count_min": 1500,
  "suggested_word_count_max": 3000,
  "assigned_agent_id": "uuid"
}
```
- **Response:** `201 Created` (triggers SERP analysis before generation)

#### POST `/seo/briefs/{brief_id}/generate`
- **Auth:** Bearer
- **Response:** `202 Accepted` — background job analyzes top-10 and produces brief

#### GET `/seo/briefs/{brief_id}`
- **Auth:** Bearer
- **Response:** Full brief with `outline_json`, `headings`, `questions_to_answer`

#### POST `/seo/briefs/{brief_id}/approve`
- **Auth:** Bearer
- **Response:** Brief status → `approved`

#### POST `/seo/briefs/{brief_id}/publish`
- **Auth:** Bearer
- **Request:** `{ "cms_connection_id": "uuid", "publish_mode": "draft" }`
- **Response:** `202 Accepted` with `cms_post_id`

#### GET `/seo/audits`
- **Auth:** Bearer
- **Query:** `?domain=goldie.agency&depth=100`
- **Response:** Paginated audit results (speed, mobile, schema, broken links)

#### POST `/seo/audits`
- **Auth:** Bearer
- **Request:** `{ "target_domain": "goldie.agency", "crawl_depth": 100, "checks": ["speed","mobile","schema","broken_links"] }`
- **Response:** `202 Accepted` with audit job ID

#### GET `/seo/audits/{audit_id}`
- **Auth:** Bearer
- **Response:** `{ "status": "completed", "score": 87, "issues": […] }`

#### GET `/seo/internal-links`
- **Auth:** Bearer
- **Query:** `?note_id=uuid&max_suggestions=10`
- **Response:** Contextual internal link proposals with anchor text

#### POST `/seo/internal-links/apply`
- **Auth:** Bearer
- **Request:** `{ "suggestions": [ { "source_note_id": "uuid", "target_note_id": "uuid", "anchor_text": "…" } ] }`
- **Response:** `{ "applied": 5, "failed": 0 }`

#### GET `/seo/reports`
- **Auth:** Bearer
- **Query:** `?campaign_id=uuid&period=30d&format=pdf|html`
- **Response:** White-label SEO report download URL

#### POST `/seo/reports`
- **Auth:** Bearer
- **Request:**
```json
{
  "campaign_id": "uuid",
  "period_days": 30,
  "format": "pdf",
  "branding": { "logo_url": "…", "primary_color": "#A855F7" },
  "sections": ["rankings","competitors","traffic","briefs"]
}
```
- **Response:** `202 Accepted` with report generation job ID

---

### 6.16 CMS Connections

#### GET `/cms/connections`
- **Auth:** Bearer
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Goldie Blog WP",
      "cms_type": "wordpress",
      "base_url": "https://blog.goldie.agency",
      "is_connected": true,
      "last_synced_at": "2026-08-11T12:00:00Z"
    }
  ]
}
```

#### POST `/cms/connections`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "name": "Goldie Blog WP",
  "cms_type": "wordpress",
  "base_url": "https://blog.goldie.agency",
  "auth_method": "api_key",
  "credentials_ref": "vault://cms/wp-api-key"
}
```

#### POST `/cms/connections/{connection_id}/test`
- **Auth:** Bearer
- **Response:** `{ "success": true, "cms_version": "6.7", "user": "admin" }`

#### GET `/cms/connections/{connection_id}/posts`
- **Auth:** Bearer
- **Query:** `?status=published&limit=20`
- **Response:** Paginated CMS posts synced from external platform

#### POST `/cms/connections/{connection_id}/posts`
- **Auth:** Bearer
- **Request:**
```json
{
  "title": "New Post Title",
  "content_html": "<p>…</p>",
  "status": "draft",
  "seo_title": "…",
  "seo_description": "…"
}
```
- **Response:** `201 Created` with `external_id`

#### POST `/cms/connections/{connection_id}/posts/{post_id}/sync`
- **Auth:** Bearer
- **Response:** `202 Accepted` — pull latest from CMS

#### DELETE `/cms/connections/{connection_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

---

### 6.17 Visual Workflows

#### GET `/workflows/templates`
- **Auth:** Bearer
- **Query:** `?category=seo&is_public=true&limit=20`
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "SEO Content Pipeline",
      "category": "seo",
      "version": 1,
      "status": "active",
      "is_public": false,
      "node_count": 8,
      "created_by": { "id": "uuid", "name": "Ada Lovelace" },
      "created_at": "2026-08-01T12:00:00Z"
    }
  ]
}
```

#### POST `/workflows/templates`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "name": "SEO Content Pipeline",
  "description": "From brief to published content",
  "category": "seo",
  "nodes": [
    { "type": "trigger_cron", "label": "Weekly", "position_x": 100, "position_y": 100, "cron_expression": "0 9 * * 1" },
    { "type": "task", "label": "Generate Brief", "position_x": 300, "position_y": 100, "agent_id": "uuid", "prompt_template": "…" },
    { "type": "approval_gate", "label": "Review Brief", "position_x": 500, "position_y": 100 },
    { "type": "task", "label": "Write Article", "position_x": 700, "position_y": 100, "agent_id": "uuid" },
    { "type": "condition", "label": "Quality Check", "position_x": 900, "position_y": 100, "condition_expression": "{{score}} >= 8" },
    { "type": "task", "label": "Publish to CMS", "position_x": 1100, "position_y": 100, "agent_id": "uuid" },
    { "type": "end", "label": "Done", "position_x": 1300, "position_y": 100 }
  ],
  "edges": [
    { "source_node_id": "…", "target_node_id": "…", "edge_type": "success" },
    { "source_node_id": "…", "target_node_id": "…", "edge_type": "conditional", "label": "pass", "condition_expression": "{{score}} >= 8" },
    { "source_node_id": "…", "target_node_id": "…", "edge_type": "conditional", "label": "fail", "condition_expression": "{{score}} < 8" }
  ]
}
```
- **Response:** `201 Created` with full template object

#### GET `/workflows/templates/{template_id}`
- **Auth:** Bearer
- **Response:** Full template with nodes and edges expanded

#### PATCH `/workflows/templates/{template_id}`
- **Auth:** Bearer (owner/operator)
- **Request:** Partial template fields or full node/edge array replacement

#### POST `/workflows/templates/{template_id}/fork`
- **Auth:** Bearer
- **Response:** `201 Created` with new template (copies nodes + edges, sets `parent_template_id`)

#### POST `/workflows/templates/{template_id}/export`
- **Auth:** Bearer
- **Query:** `?format=json|yaml`
- **Response:** `200` with `Content-Disposition: attachment`

#### POST `/workflows/templates/import`
- **Auth:** Bearer
- **Request:** `{ "format": "json", "data": "…" }` or multipart file upload
- **Response:** `201 Created` with imported template

#### DELETE `/workflows/templates/{template_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### GET `/workflows/templates/{template_id}/nodes`
- **Auth:** Bearer
- **Response:** Array of workflow nodes

#### POST `/workflows/templates/{template_id}/nodes`
- **Auth:** Bearer (owner/operator)
- **Request:** Single node object
- **Response:** `201 Created`

#### PATCH `/workflows/nodes/{node_id}`
- **Auth:** Bearer (owner/operator)
- **Request:** Partial node fields

#### DELETE `/workflows/nodes/{node_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### GET `/workflows/templates/{template_id}/edges`
- **Auth:** Bearer
- **Response:** Array of workflow edges

#### POST `/workflows/templates/{template_id}/edges`
- **Auth:** Bearer (owner/operator)
- **Request:** Single edge object
- **Response:** `201 Created`

#### DELETE `/workflows/edges/{edge_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### POST `/workflows/templates/{template_id}/trigger`
- **Auth:** Bearer
- **Request:** `{ "inputs": { "keyword": "ai agents" }, "agent_id": "uuid", "mode": "live" }`
- **Response:** `202 Accepted` with `execution_id`

#### POST `/workflows/templates/{template_id}/simulate`
- **Auth:** Bearer
- **Request:** `{ "inputs": { "keyword": "ai agents" }, "variables_json": { "score": 9 } }`
- **Response:** `200` with simulated execution trace (no external API calls)
```json
{
  "execution_id": "sim-uuid",
  "status": "completed",
  "trace": [
    { "node_id": "…", "node_type": "trigger_cron", "entered_at": "…", "exited_at": "…", "output": {} },
    { "node_id": "…", "node_type": "task", "entered_at": "…", "exited_at": "…", "output": { "brief": "…" }, "simulated": true },
    { "node_id": "…", "node_type": "approval_gate", "entered_at": "…", "status": "waiting_approval", "simulated": true }
  ],
  "variables": { "score": 9, "brief": "…" }
}
```

#### GET `/workflows/executions`
- **Auth:** Bearer
- **Query:** `?template_id=uuid&status=running&mode=simulation&limit=20`
- **Response:** Paginated execution list

#### GET `/workflows/executions/{execution_id}`
- **Auth:** Bearer
- **Response:** Full execution with `trace`, `current_node_id`, `variables_json`, `output_json`

#### POST `/workflows/executions/{execution_id}/pause`
- **Auth:** Bearer
- **Response:** `202 Accepted`

#### POST `/workflows/executions/{execution_id}/resume`
- **Auth:** Bearer
- **Response:** `202 Accepted`

#### POST `/workflows/executions/{execution_id}/cancel`
- **Auth:** Bearer
- **Response:** `202 Accepted`

#### POST `/workflows/executions/{execution_id}/retry`
- **Auth:** Bearer
- **Request:** `{ "from_node_id": "uuid", "preserve_variables": true }`
- **Response:** `202 Accepted` with new execution ID

#### GET `/workflows/executions/{execution_id}/variables`
- **Auth:** Bearer
- **Response:** `{ "variables": { "score": 9, "brief": "…" } }`

#### POST `/workflows/executions/{execution_id}/variables`
- **Auth:** Bearer
- **Request:** `{ "variables": { "score": 9 } }`
- **Response:** `200` (updates runtime variables)

#### GET `/workflows/executions/{execution_id}/logs`
- **Auth:** Bearer
- **Response:** Step-by-step execution logs with timestamps

#### GET `/workflows/schedules`
- **Auth:** Bearer
- **Response:** Array of schedules bound to templates

#### POST `/workflows/schedules`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "template_id": "uuid",
  "name": "Weekly SEO Report",
  "schedule_type": "cron",
  "cron_expression": "0 9 * * 1",
  "timezone": "America/New_York",
  "is_active": true
}
```
- **Response:** `201 Created`

#### PATCH `/workflows/schedules/{schedule_id}`
- **Auth:** Bearer (owner/operator)

#### DELETE `/workflows/schedules/{schedule_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

---

### 6.18 Agent Roles

#### GET `/agent-roles`
- **Auth:** Bearer
- **Query:** `?limit=20&cursor=`
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "SEO Strategist",
      "slug": "seo-strategist",
      "icon": "search",
      "color": "#22C55E",
      "default_agent_id": "uuid",
      "autonomy_level": "suggest",
      "skill_count": 8,
      "assigned_agents": 3,
      "created_at": "2026-08-01T12:00:00Z"
    }
  ]
}
```

#### POST `/agent-roles`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "name": "SEO Strategist",
  "slug": "seo-strategist",
  "description": "Expert in organic search strategy and content planning.",
  "icon": "search",
  "color": "#22C55E",
  "default_agent_id": "uuid",
  "system_prompt_template": "You are an SEO strategist. Your goal is to…",
  "memory_profile": "semantic_heavy",
  "autonomy_level": "suggest",
  "handoff_threshold_pct": 80.0
}
```
- **Response:** `201 Created`

#### GET `/agent-roles/{role_id}`
- **Auth:** Bearer
- **Response:** Full role with `skills`, `assigned_agents`, `history_summary`

#### PATCH `/agent-roles/{role_id}`
- **Auth:** Bearer (owner/operator)
- **Request:** Partial role fields

#### DELETE `/agent-roles/{role_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### POST `/agent-roles/{role_id}/clone`
- **Auth:** Bearer
- **Response:** `201 Created` with cloned role (new UUID, name suffix "(Copy)")

#### GET `/agent-roles/{role_id}/skills`
- **Auth:** Bearer
- **Response:** Array of role skills

#### POST `/agent-roles/{role_id}/skills`
- **Auth:** Bearer (owner/operator)
- **Request:** `{ "skill_name": "serp_analysis", "skill_version": "1.0.0", "is_required": true }`
- **Response:** `201 Created`

#### DELETE `/agent-roles/{role_id}/skills/{skill_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### GET `/agent-roles/{role_id}/assignments`
- **Auth:** Bearer
- **Response:** Array of agent-role assignments with priority

#### POST `/agent-roles/{role_id}/assignments`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "agent_id": "uuid",
  "priority": 0,
  "is_primary": true
}
```
- **Response:** `201 Created`

#### DELETE `/agent-roles/{role_id}/assignments/{assignment_id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

#### GET `/agents/{agent_id}/roles`
- **Auth:** Bearer
- **Response:** All roles assigned to this agent

#### POST `/agents/{agent_id}/roles`
- **Auth:** Bearer (owner/operator)
- **Request:** `{ "role_id": "uuid", "priority": 1, "is_primary": false }`

#### POST `/agents/{agent_id}/switch-role`
- **Auth:** Bearer
- **Request:** `{ "role_id": "uuid", "preserve_context": true, "reason": "User requested SEO help" }`
- **Response:** `200` with new system prompt and role context

---

### 6.19 Agent Reflections

#### GET `/agents/{agent_id}/reflections`
- **Auth:** Bearer
- **Query:** `?type=task&since=30d&limit=20`
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "run_id": "uuid",
      "reflection_type": "task",
      "what_worked": "The outline covered all user questions.",
      "what_failed": "Missed long-tail keyword cluster.",
      "improvement": "Add keyword gap analysis step before outline.",
      "confidence_score": 0.92,
      "applied_to_prompt": false,
      "created_at": "2026-08-10T14:00:00Z"
    }
  ]
}
```

#### POST `/agents/{agent_id}/reflections`
- **Auth:** Bearer (system or agent token)
- **Request:**
```json
{
  "run_id": "uuid",
  "task_id": "uuid",
  "reflection_type": "task",
  "what_worked": "…",
  "what_failed": "…",
  "improvement": "…",
  "confidence_score": 0.92
}
```
- **Response:** `201 Created`

#### POST `/agents/{agent_id}/reflections/synthesize`
- **Auth:** Bearer
- **Request:** `{ "period": "weekly", "from": "2026-08-01", "to": "2026-08-11" }`
- **Response:** `202 Accepted` with synthesis job ID

#### GET `/agents/{agent_id}/reflections/synthesis/{synthesis_id}`
- **Auth:** Bearer
- **Response:** Synthesized reflection with `applied_to_prompt: true` and updated system prompt diff

---

### 6.20 Swarm Sessions

#### GET `/swarm/sessions`
- **Auth:** Bearer
- **Query:** `?status=active&limit=20`
- **Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Q3 Report Collaboration",
      "objective": "Produce a 20-page quarterly report on AI agent adoption.",
      "status": "active",
      "participant_count": 5,
      "consensus_required": true,
      "started_at": "2026-08-11T09:00:00Z"
    }
  ]
}
```

#### POST `/swarm/sessions`
- **Auth:** Bearer
- **Request:**
```json
{
  "task_id": "uuid",
  "name": "Q3 Report Collaboration",
  "objective": "Produce a 20-page quarterly report on AI agent adoption.",
  "consensus_required": true,
  "consensus_threshold": 1,
  "participants": [
    { "agent_id": "uuid", "swarm_role": "lead", "priority": 0 },
    { "agent_id": "uuid", "swarm_role": "researcher", "priority": 1 },
    { "agent_id": "uuid", "swarm_role": "writer", "priority": 2 },
    { "agent_id": "uuid", "swarm_role": "reviewer", "priority": 3 },
    { "agent_id": "uuid", "swarm_role": "fact_checker", "priority": 4 }
  ]
}
```
- **Response:** `201 Created` with session object

#### GET `/swarm/sessions/{session_id}`
- **Auth:** Bearer
- **Response:** Full session with `participants`, `shared_context`, `final_output`

#### POST `/swarm/sessions/{session_id}/delegate`
- **Auth:** Bearer (orchestrator agent)
- **Request:**
```json
{
  "agent_id": "uuid",
  "task": "Research top 10 AI agent frameworks.",
  "context": "Focus on enterprise adoption in 2026.",
  "deadline": "2026-08-11T18:00:00Z",
  "success_criteria": "At least 10 frameworks with citation links.",
  "output_format": "markdown_bullets",
  "approval_needed": false
}
```
- **Response:** `202 Accepted` with delegation task ID

#### POST `/swarm/sessions/{session_id}/participants/{participant_id}/submit`
- **Auth:** Bearer (participant agent)
- **Request:** `{ "contribution_json": { "section": "…", "sources": […] } }`
- **Response:** `200`

#### POST `/swarm/sessions/{session_id}/participants/{participant_id}/vote`
- **Auth:** Bearer (participant agent)
- **Request:** `{ "vote": "approve", "vote_reason": "Sources verified and tone matches brand." }`
- **Response:** `200`

#### GET `/swarm/sessions/{session_id}/consensus`
- **Auth:** Bearer
- **Response:** `{ "status": "pending", "votes": { "approve": 3, "reject": 0, "abstain": 1 }, "required": 4 }`

#### POST `/swarm/sessions/{session_id}/finalize`
- **Auth:** Bearer (lead agent or owner)
- **Request:** `{ "force": false }`
- **Response:** `200` with final output or `409` if consensus not reached

#### POST `/swarm/sessions/{session_id}/cancel`
- **Auth:** Bearer
- **Response:** `202 Accepted`

---

### 6.21 Cost

#### GET `/cost/spend`
- **Auth:** Bearer
- **Query:** `?period=30d&group_by=agent`
- **Response:** `{ "total_usd": 12.34, "breakdown": […] }`

#### POST `/cost/budget`
- **Auth:** Bearer (owner)
- **Request:** `{ "monthly_limit_usd": 500, "alert_threshold_pct": 80 }`

#### GET `/cost/alerts`
- **Auth:** Bearer
- **Response:** Active alerts

---

### 6.22 Files (via Hermes Proxy)

#### GET `/files`
- **Auth:** Bearer
- **Response:** File tree (virtual paths)

#### GET `/files/{path}`
- **Auth:** Bearer
- **Response:** File content or directory listing

#### PUT `/files/{path}`
- **Auth:** Bearer
- **Request:** Raw bytes or `{ "content": "base64…" }`
- **Response:** `201`

#### DELETE `/files/{path}`
- **Auth:** Bearer
- **Response:** `204`

---

### 6.23 Terminal (via Hermes Proxy)

#### POST `/terminal/sessions`
- **Auth:** Bearer
- **Request:** `{ "cwd": "/workspace", "shell": "/bin/bash" }`
- **Response:** `{ "session_id": "term_abc123", "ws_url": "wss://agentos.local/ws/terminal/term_abc123" }`

#### POST `/terminal/sessions/{session_id}/input`
- **Auth:** Bearer
- **Request:** `{ "data": "ls -la\n" }`

#### POST `/terminal/sessions/{session_id}/resize`
- **Auth:** Bearer
- **Request:** `{ "cols": 120, "rows": 40 }`

#### DELETE `/terminal/sessions/{session_id}`
- **Auth:** Bearer

---

### 6.24 Voice

#### POST `/voice/sessions`
- **Auth:** Bearer
- **Request:**
```json
{
  "agent_id": "uuid",
  "mode": "push_to_talk | hands_free | voice_first",
  "stt_provider": "string",
  "tts_provider": "string"
}
```
- **Response:** `{ "id": "uuid", "status": "idle", "ws_url": "string" }`

#### GET `/voice/sessions`
- **Auth:** Bearer
- **Response:** List of voice sessions for the workspace

#### GET `/voice/sessions/{id}`
- **Auth:** Bearer
- **Response:** Voice session details

#### POST `/voice/sessions/{id}/audio`
- **Auth:** Bearer
- **Request:** multipart/form-data with audio file
- **Response:** `{ "transcript": "string", "confidence": 0.95, "duration_ms": 4200 }`

#### POST `/voice/sessions/{id}/speak`
- **Auth:** Bearer
- **Request:** `{ "text": "string", "voice_profile_id": "uuid", "speed": 1.0 }`
- **Response:** `{ "audio_url": "string", "duration_ms": 4200 }` or stream

#### WS `/voice/sessions/{id}/stream`
- **Auth:** Bearer (token as query param)
- **Description:** Bidirectional WebSocket for real-time STT/TTS

#### GET `/voice/profiles`
- **Auth:** Bearer
- **Response:** List voice profiles

#### POST `/voice/profiles`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "agent_id": "uuid",
  "voice_name": "string",
  "provider": "string",
  "provider_voice_id": "string",
  "speed": 1.0,
  "pitch": 0.0
}
```

#### PUT `/voice/profiles/{id}`
- **Auth:** Bearer (owner/operator)
- **Request:** Partial voice profile fields

#### DELETE `/voice/profiles/{id}`
- **Auth:** Bearer (owner/operator)
- **Response:** `204`

---

### 6.25 Import & Export

#### POST `/import`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "source_type": "obsidian | notion | chatgpt | claude | evernote | onenote | markdown",
  "file_path": "string",
  "conflict_resolution": "skip | overwrite | merge"
}
```
- **Response:** `{ "id": "uuid", "status": "pending", "total_items": 0 }`

#### GET `/import/{id}`
- **Auth:** Bearer
- **Response:**
```json
{
  "id": "uuid",
  "status": "running | completed | failed",
  "total_items": 100,
  "processed_items": 42,
  "errors": [{ "item": "string", "error": "string" }]
}
```

#### POST `/export`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "export_type": "workspace | notebook | chats | seo_reports | encrypted",
  "password": "string"
}
```
- **Response:** `{ "id": "uuid", "status": "pending" }`

#### GET `/export/{id}`
- **Auth:** Bearer
- **Response:** Export job progress

#### GET `/export/{id}/download`
- **Auth:** Bearer
- **Response:** Exported file download (`Content-Disposition: attachment`)

---

### 6.26 Disaster Recovery

#### POST `/backups`
- **Auth:** Bearer (owner/operator)
- **Request:** `{ "type": "manual" }`
- **Response:** `{ "id": "uuid", "status": "running", "created_at": "2026-08-11T12:00:00Z" }`

#### GET `/backups`
- **Auth:** Bearer (owner/operator)
- **Response:**
```json
[
  {
    "id": "uuid",
    "type": "auto | manual",
    "status": "completed | failed",
    "file_path": "string",
    "file_size_bytes": 1073741824,
    "checksum": "sha256…",
    "retention_until": "2026-09-11T12:00:00Z",
    "created_at": "2026-08-11T12:00:00Z"
  }
]
```

#### POST `/backups/{id}/restore`
- **Auth:** Bearer (owner)
- **Response:** `{ "id": "uuid", "status": "running" }`

#### POST `/backups/targets`
- **Auth:** Bearer (owner/operator)
- **Request:**
```json
{
  "name": "string",
  "type": "s3 | dropbox | gdrive | minio",
  "config": {
    "endpoint": "string",
    "bucket": "string",
    "access_key": "string",
    "secret_key": "string"
  }
}
```

#### GET `/health/backup`
- **Auth:** Bearer (owner/operator)
- **Response:**
```json
{
  "status": "healthy | warning | failed",
  "last_backup_at": "2026-08-11T12:00:00Z",
  "last_backup_status": "completed | failed",
  "next_scheduled": "2026-08-12T02:00:00Z",
  "disk_space_percent": 65
}
```

#### POST `/export/everything`
- **Auth:** Bearer (owner)
- **Request:** `{ "password": "string" }`
- **Response:** `{ "id": "uuid", "status": "pending", "file_path": "string" }`

---

## 7. Streaming Protocols

### 7.1 SSE — Chat Streaming

Endpoint: `POST /api/v1/chat/sessions/{session_id}/messages?stream=true`

Headers:
```
Accept: text/event-stream
Cache-Control: no-cache
```

Events:

| Event | Payload |
|-------|---------|
| `message.start` | `{ "message_id": "uuid", "agent_id": "uuid" }` |
| `message.chunk` | `{ "content": "partial text" }` |
| `message.tool_call` | `{ "tool": "…", "args": {} }` |
| `message.tool_result` | `{ "tool": "…", "output": "…" }` |
| `message.end` | `{ "message_id": "uuid", "finish_reason": "stop" }` |
| `error` | RFC 7807 Problem Details |

Example stream:
```
event: message.start
data: {"message_id":"msg_123","agent_id":"agent_456"}

event: message.chunk
data: {"content":"The"}

event: message.chunk
data: {"content":" quick"}

event: message.end
data: {"message_id":"msg_123","finish_reason":"stop"}
```

### 7.2 WebSocket — DAG Live Updates

URL: `wss://agentos.local/ws/tasks/{task_id}`

Connect with JWT as query param: `?token=eyJ…`

Messages (JSON):

**Client → Server:**
```json
{ "action": "subscribe", "channels": ["nodes", "logs"] }
```

**Server → Client:**
```json
{ "type": "node.update", "node_id": "n2", "status": "running", "started_at": "…" }
{ "type": "node.complete", "node_id": "n2", "output_preview": "…", "duration_ms": 4200 }
{ "type": "log.append", "node_id": "n2", "level": "info", "message": "Build succeeded" }
{ "type": "error", "detail": "Node timed out" }
```

Heartbeat: server sends `{ "type": "ping" }` every 30s; client must respond with `{ "type": "pong" }`.

---

## 8. Provider-Specific Endpoints

### 8.1 Kimi (Moonshot AI)

- **Gateway proxy:** `provider: "moonshot"`
- **Models:** `moonshot-v1-8k`, `moonshot-v1-32k`, `moonshot-v1-128k`
- **Extra params:** `max_tokens`, `temperature`, `top_p`
- **Endpoint:** Same `/gateway/complete` with `"provider": "moonshot"`

### 8.2 Claude (Anthropic)

- **Gateway proxy:** `provider: "anthropic"`
- **Models:** `claude-sonnet-4-20250514`, `claude-opus-4-20250514`, `claude-haiku-4-20250514`
- **Extra params:** `thinking`, `extended_output`
- **Tool use:** Native via `messages` array with `content` blocks

### 8.3 Grok (xAI)

- **Gateway proxy:** `provider: "xai"`
- **Models:** `grok-3-beta`, `grok-3-mini-beta`
- **Extra params:** `web_search`, `image_generation`

### 8.4 Ollama (Local)

- **Gateway proxy:** `provider: "ollama"`
- **Models:** Dynamic list from local Ollama instance
- **Base URL:** Configured per workspace (`OLLAMA_HOST`)
- **Extra params:** `raw`, `format`, `options`

---

## 9. Schema Reference

### 9.1 Common Enums

```yaml
TaskStatus:
  - draft
  - ready
  - active
  - blocked
  - completed
  - cancelled
  - archived

// Kanban column mapping: draft→Backlog, ready→Ready, active→In Progress, blocked→Blocked, completed→Done, archived→Done

NodeStatus:
  - pending
  - running
  - completed
  - failed
  - skipped
  - retrying

ApprovalStatus:
  - pending
  - approved
  - rejected
  - escalated
  - expired
  - cancelled
  - consumed

Role:
  - owner
  - operator
  - approver
  - contributor
  - auditor

SeoCampaignStatus:
  - draft
  - active
  - paused
  - archived

SeoKeywordIntent:
  - informational
  - navigational
  - transactional
  - commercial
  - unknown

SeoBriefStatus:
  - draft
  - in_review
  - approved
  - published
  - archived

CmsConnectionType:
  - wordpress
  - shopify
  - webflow
  - ghost
  - strapi
  - custom

CmsPostStatus:
  - draft
  - scheduled
  - published
  - archived
  - deleted

WorkflowNodeType:
  - start
  - task
  - condition
  - loop
  - approval_gate
  - delay
  - trigger_cron
  - trigger_webhook
  - trigger_manual
  - trigger_event
  - end

WorkflowEdgeType:
  - success
  - failure
  - conditional
  - default

WorkflowExecutionStatus:
  - pending
  - queued
  - running
  - paused
  - waiting_approval
  - completed
  - failed
  - cancelled

WorkflowRunMode:
  - live
  - simulation
  - dry_run

WorkflowScheduleType:
  - cron
  - interval
  - event

AgentRoleAutonomy:
  - fully_autonomous
  - suggest
  - confirm_each_step
  - manual_only

AgentReflectionType:
  - task
  - synthesis_weekly
  - synthesis_monthly
  - skill_learned
  - error

SwarmRole:
  - lead
  - researcher
  - writer
  - reviewer
  - fact_checker
  - contributor

SwarmSessionStatus:
  - forming
  - active
  - paused
  - consensus_reached
  - completed
  - failed
  - cancelled

SwarmParticipantStatus:
  - invited
  - joined
  - active
  - paused
  - completed
  - abandoned
```

### 9.2 OpenAPI

Full OpenAPI 3.1 spec is available at:
`GET /api/v1/openapi.json` (no auth required)

Interactive docs: `https://agentos.local/docs/api`

---

## 10. Changelog

| Version | Date | Notes |
|---------|------|-------|
| 2.0.0-MVP | 2026-08-11 | Initial Goldie Edition spec |
| 2.1.0-Goldie | 2026-08-11 | Added SEO Module (§6.15), CMS Connections (§6.16), Visual Workflows (§6.17), Agent Roles (§6.18), Agent Reflections (§6.19), Swarm Sessions (§6.20) |

---

## 11. New Endpoint Summary

| Domain | Endpoints | Auth Level |
|--------|-----------|------------|
| SEO Campaigns | `GET/POST/PATCH/DELETE /seo/campaigns` | Bearer / owner+admin for mutations |
| SEO Keywords | `GET/POST/bulk/track /seo/campaigns/{id}/keywords` | Bearer |
| SEO Rankings | `GET /seo/keywords/{id}/rankings` | Bearer |
| SEO Competitors | `GET/POST/changes /seo/competitors` | Bearer |
| SEO Briefs | `GET/POST/generate/approve/publish /seo/briefs` | Bearer |
| SEO Audits | `GET/POST /seo/audits` | Bearer |
| SEO Internal Links | `GET/apply /seo/internal-links` | Bearer |
| SEO Reports | `GET/POST /seo/reports` | Bearer |
| CMS Connections | `CRUD + test + posts + sync` | Bearer / owner+admin for mutations |
| Workflow Templates | `CRUD + fork + import/export` | Bearer / owner+admin for mutations |
| Workflow Nodes/Edges | `CRUD` | Bearer / owner+admin for mutations |
| Workflow Executions | `GET + trigger/simulate/pause/resume/cancel/retry/variables/logs` | Bearer |
| Workflow Schedules | `CRUD` | Bearer / owner+admin for mutations |
| Agent Roles | `CRUD + clone + skills + assignments` | Bearer / owner+admin for mutations |
| Agent Reflections | `GET/POST/synthesize` | Bearer / system token |
| Swarm Sessions | `CRUD + delegate + submit/vote + consensus + finalize` | Bearer / system token |

---

*End of API Specification*

## 12. Curl Examples

### SEO Module

**Create SEO campaign:**
```bash
curl -X POST https://agentos.local/api/v1/seo/campaigns \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q3 Organic Growth",
    "target_domain": "goldie.agency",
    "target_locale": "en-US",
    "serp_provider": "serpapi",
    "budget_usd": 50000
  }'
```

**Query SERP for a keyword:**
```bash
curl -X POST https://agentos.local/api/v1/seo/keywords/{keyword_id}/track \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "engines": ["google","bing"],
    "devices": ["desktop","mobile"]
  }'
```

**Generate content brief:**
```bash
curl -X POST https://agentos.local/api/v1/seo/briefs/{brief_id}/generate \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Track keyword rankings:**
```bash
curl -X POST https://agentos.local/api/v1/seo/keywords/{keyword_id}/track \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "engines": ["google"], "devices": ["desktop","mobile"] }'
```

**Publish brief to CMS:**
```bash
curl -X POST https://agentos.local/api/v1/seo/briefs/{brief_id}/publish \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cms_connection_id": "uuid",
    "publish_mode": "draft"
  }'
```

**Generate white-label report:**
```bash
curl -X POST https://agentos.local/api/v1/seo/reports \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "uuid",
    "period_days": 30,
    "format": "pdf",
    "branding": { "logo_url": "…", "primary_color": "#A855F7" },
    "sections": ["rankings","competitors","traffic","briefs"]
  }'
```

### Visual Workflows

**Create workflow template:**
```bash
curl -X POST https://agentos.local/api/v1/workflows/templates \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SEO Content Pipeline",
    "category": "seo",
    "nodes": [
      { "type": "trigger_cron", "label": "Weekly", "position_x": 100, "position_y": 100, "cron_expression": "0 9 * * 1" },
      { "type": "task", "label": "Generate Brief", "position_x": 300, "position_y": 100, "agent_id": "uuid", "prompt_template": "…" },
      { "type": "approval_gate", "label": "Review Brief", "position_x": 500, "position_y": 100 },
      { "type": "task", "label": "Write Article", "position_x": 700, "position_y": 100, "agent_id": "uuid" },
      { "type": "condition", "label": "Quality Check", "position_x": 900, "position_y": 100, "condition_expression": "{{score}} >= 8" },
      { "type": "task", "label": "Publish to CMS", "position_x": 1100, "position_y": 100, "agent_id": "uuid" },
      { "type": "end", "label": "Done", "position_x": 1300, "position_y": 100 }
    ],
    "edges": [
      { "source_node_id": "…", "target_node_id": "…", "edge_type": "success" },
      { "source_node_id": "…", "target_node_id": "…", "edge_type": "conditional", "label": "pass", "condition_expression": "{{score}} >= 8" },
      { "source_node_id": "…", "target_node_id": "…", "edge_type": "conditional", "label": "fail", "condition_expression": "{{score}} < 8" }
    ]
  }'
```

**Simulate workflow execution:**
```bash
curl -X POST https://agentos.local/api/v1/workflows/templates/{template_id}/simulate \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": { "keyword": "ai agents" },
    "variables_json": { "score": 9 }
  }'
```

**Trigger live workflow run:**
```bash
curl -X POST https://agentos.local/api/v1/workflows/templates/{template_id}/trigger \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": { "repo_url": "https://github.com/…" },
    "agent_id": "uuid",
    "mode": "live"
  }'
```

### Agent Roles

**Create agent role:**
```bash
curl -X POST https://agentos.local/api/v1/agent-roles \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SEO Strategist",
    "slug": "seo-strategist",
    "description": "Expert in organic search strategy.",
    "icon": "search",
    "color": "#22C55E",
    "default_agent_id": "uuid",
    "system_prompt_template": "You are an SEO strategist. Your goal is to…",
    "autonomy_level": "suggest",
    "handoff_threshold_pct": 80.0
  }'
```

**Assign agent to role:**
```bash
curl -X POST https://agentos.local/api/v1/agent-roles/{role_id}/assignments \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "uuid",
    "priority": 1,
    "is_primary": true
  }'
```

**Switch role mid-conversation:**
```bash
curl -X POST https://agentos.local/api/v1/chat/sessions/{session_id}/switch-role \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "role_id": "uuid", "preserve_context": true }'
```

### Swarm Sessions

**Create swarm session:**
```bash
curl -X POST https://agentos.local/api/v1/swarm/sessions \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "uuid",
    "name": "Q3 Report Collaboration",
    "objective": "Produce a 20-page quarterly report on AI agent adoption.",
    "consensus_required": true,
    "participants": [
      { "agent_id": "uuid", "swarm_role": "lead", "priority": 0 },
      { "agent_id": "uuid", "swarm_role": "researcher", "priority": 1 },
      { "agent_id": "uuid", "swarm_role": "writer", "priority": 2 },
      { "agent_id": "uuid", "swarm_role": "reviewer", "priority": 3 }
    ]
  }'
```

**Delegate task within swarm:**
```bash
curl -X POST https://agentos.local/api/v1/swarm/sessions/{session_id}/delegate \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "uuid",
    "task": "Research top 10 AI agent frameworks.",
    "context": "Focus on enterprise adoption in 2026.",
    "deadline": "2026-08-11T18:00:00Z",
    "success_criteria": "At least 10 frameworks with citation links.",
    "output_format": "markdown_bullets",
    "approval_needed": false
  }'
```

**Cast consensus vote:**
```bash
curl -X POST https://agentos.local/api/v1/swarm/sessions/{session_id}/participants/{participant_id}/vote \
  -H "Authorization: Bearer \$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vote": "approve",
    "vote_reason": "Sources verified and tone matches brand."
  }'
```

---

*End of API Specification — Agent OS v2 Goldie Edition*
