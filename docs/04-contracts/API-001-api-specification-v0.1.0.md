---
document_id: API-001
title: Agent OS API Specification
version: 0.3.0
status: draft
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-07-19
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
dependencies:
  - SAD-001
  - AGC-001
  - RUN-001
  - APR-001
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PRD-001
  - SRS-001
  - NFR-001
  - AUT-001
  - RTM-001
  - SAD-001
  - C4-001
  - C4-002
  - DDD-001
  - DAT-001
  - MEM-001
  - ORC-001
  - INT-001
  - SEC-001
  - THR-001
  - DCT-001
  - AGC-001
  - CAP-001
  - MOD-001
  - RUN-001
  - APR-001
  - ART-001
  - EVT-001
  - DEV-001
  - TST-001
  - QAG-001
  - OBS-001
  - OPS-001
  - BCP-001
related_adrs:
  - ADR-TBD-API-001
  - ADR-TBD-API-002
  - ADR-TBD-API-003
  - ADR-TBD-API-004
  - ADR-TBD-API-005
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# API-001 — Agent OS API Specification

> **Status: Draft.** This document defines the proposed control-plane API contract for Agent OS. It describes resources, operations, request and response envelopes, authentication, authorization, workspace scoping, idempotency, optimistic concurrency, pagination, filtering, errors, long-running operations, event access, security, observability, compatibility, and tests. It does not select a final web framework, API gateway, serialization library, transport stack, or public SaaS exposure model.

## 1. Purpose

The Agent OS API is the authoritative programmatic boundary for the control plane.

It supports:

- authenticated user and workload access;
- organization, workspace, project, membership, and role management;
- agent and adapter registration;
- capability discovery and enablement;
- model-profile management and routing inspection;
- task and snapshot management;
- durable run commands and read models;
- approval review and consumption;
- artifact staging, review, export, and deletion;
- governed memory;
- audit and execution receipts;
- usage, cost, budget, and reconciliation;
- component health and operational controls;
- backup, restore, maintenance, and recovery;
- event and timeline access;
- conformance and administrative diagnostics.

## 2. Core API principles

### `API-P-001 — Control plane authority`

Clients request commands and query state. They do not directly assign authoritative lifecycle states.

### `API-P-002 — Workspace scope first`

Protected resources are scoped and authorized before retrieval, mutation, search, sorting, ranking, or export.

### `API-P-003 — Commands are explicit`

Consequential state changes use explicit command endpoints or command resources rather than ambiguous generic updates.

### `API-P-004 — Idempotency is first-class`

Create and consequential commands support idempotency.

### `API-P-005 — Concurrency is explicit`

Mutable aggregates expose versions and reject stale writes.

### `API-P-006 — Async work is represented`

Long-running work returns accepted operations, runs, jobs, or status resources rather than holding fragile requests open indefinitely.

### `API-P-007 — Unknown remains unknown`

Missing, stale, unavailable, estimated, inferred, or conflicted data is represented explicitly.

### `API-P-008 — Errors are safe and actionable`

Errors have stable codes, correlation, retry guidance, current state, and no raw secrets.

### `API-P-009 — Provider-neutral core`

Provider-, adapter-, model-, and tool-specific data lives in controlled extension namespaces.

### `API-P-010 — Evidence is linkable`

Commands, state transitions, approvals, outputs, costs, and operations expose audit or evidence references where permitted.

### `API-P-011 — Compatibility is governed`

Breaking changes require versioning and migration.

### `API-P-012 — Public exposure is not assumed`

The MVP API is designed for protected local or controlled network use, not anonymous public access.

## 3. Non-goals

This specification does not:

- expose direct unrestricted shell execution;
- expose direct unrestricted database access;
- expose raw secret values;
- allow client-side approval tokens to bypass server validation;
- allow clients to set run state directly;
- allow agents to assign themselves roles;
- define a public plugin marketplace;
- define production or financial mutation APIs;
- guarantee backward compatibility for draft schemas;
- define every provider-specific payload;
- select REST, RPC, GraphQL, gRPC, or another transport as the only implementation.

## 4. API style direction

The primary documented style is resource-oriented HTTP with JSON-like representations and explicit command subresources.

Illustrative base path:

```text
/api/v1
```

The final style requires an ADR.

The design supports:

- synchronous reads;
- synchronous bounded validation;
- asynchronous commands;
- event streams or cursor polling;
- typed downloadable/exportable content;
- optional local IPC profiles.

## 5. Base URL and deployment profiles

Possible deployment profiles:

```text
local_loopback
local_lan_protected
reverse_proxy_protected
controlled_internal_network
```

Public internet exposure is outside MVP unless separately approved.

Example:

```text
http://127.0.0.1:<port>/api/v1
```

TLS, reverse proxy, host validation, and network access depend on deployment profile.

## 6. Media types

Core JSON media type direction:

```text
application/json
```

Versioned vendor media type remains an option:

```text
application/vnd.agentos.v1+json
```

Download/upload media types depend on artifact content.

The API must send anti-sniffing and safe content-disposition headers for content responses.

## 7. Character encoding and time

- JSON uses UTF-8.
- Machine timestamps use UTC RFC3339-style strings.
- Date-only values remain date-only.
- Durations use explicit seconds or structured duration fields.
- Monetary amounts use decimal strings, never binary floating point in contracts.
- Unknown times use explicit state or null only where allowed.

## 8. Canonical identifiers

Identifiers are opaque.

Clients must not infer:

- creation time;
- organization;
- role;
- state;
- ordering;
- database shard;
- resource type beyond documented prefixes if prefixes are used.

Identifiers are never reused.

## 9. Common request headers

Recommended headers:

| Header | Purpose |
|---|---|
| `Authorization` | Authenticated session/token where applicable |
| `Content-Type` | Request media type |
| `Accept` | Response media type |
| `Idempotency-Key` | Duplicate protection |
| `If-Match` | Expected resource version/ETag |
| `X-Correlation-Id` | Caller-provided correlation, validated |
| `X-Request-Id` | Optional caller request ID |
| `X-Workspace-Id` | Optional context hint; not authority |
| `Prefer` | Async/representation preferences where supported |

The server remains authoritative for identity and workspace membership.

## 10. Common response headers

Recommended headers:

| Header | Purpose |
|---|---|
| `Content-Type` | Response media type |
| `ETag` | Resource version |
| `Location` | Newly created resource |
| `Retry-After` | Retry timing |
| `X-Request-Id` | Server request ID |
| `X-Correlation-Id` | Correlation ID |
| `X-RateLimit-*` | Rate-limit metadata where available |
| `Cache-Control` | Safe caching policy |
| `Vary` | Authorization/context cache correctness |

## 11. Authentication

The API requires authenticated access for all protected operations.

Potential methods:

- local account session;
- external identity-provider session;
- bounded workload identity;
- short-lived service token;
- local IPC identity.

Final mechanisms require an ADR.

Anonymous access is disabled by default.

## 12. Session endpoints

Potential resources:

```text
POST   /sessions
GET    /sessions/current
DELETE /sessions/current
GET    /sessions/current/authority
POST   /sessions/current/reauthenticate
```

### `POST /sessions`

Creates an authenticated session.

Response should include:

- session ID;
- identity summary;
- assurance level;
- idle expiry;
- absolute expiry;
- reauthentication requirements;
- accessible organization/workspace summaries;
- no raw credential echo.

### `DELETE /sessions/current`

Revokes the current session.

Logout does not cancel active runs automatically.

## 13. Reauthentication

Sensitive actions may require recent reauthentication.

Examples:

- changing roles;
- approving high-risk actions;
- viewing secret metadata;
- restoring backups;
- disabling security controls;
- exporting confidential evidence.

The API should return:

```text
REAUTHENTICATION_REQUIRED
```

with a safe reauthentication flow reference.

## 14. Workload authentication

Adapters, workers, tool gateways, preview workers, and backup processes use distinct workload identities.

Workload credentials are:

- bounded;
- non-human;
- short-lived where possible;
- scoped to capabilities and workspace/resource class;
- rotatable;
- auditable;
- denied access to human approval endpoints.

## 15. Authorization evaluation

Authorization evaluates:

- authenticated identity;
- session/workload state;
- organization/workspace membership;
- role assignments;
- delegated authority;
- resource ownership;
- classification;
- action;
- current policy;
- emergency stop;
- maintenance state;
- approval where required.

Authorization is checked on every protected request.

## 16. Workspace scoping

Protected requests may identify a workspace by path or resource relationship.

Example:

```text
/workspaces/{workspace_id}/tasks
```

A header or query parameter alone never grants scope.

Cross-workspace object references return a safe denial or not-found posture according to security policy.

## 17. API permission categories

Suggested categories:

```text
organization.read
organization.manage
workspace.read
workspace.manage
workspace.members.manage
project.read
project.manage
agent.read
agent.manage
capability.read
capability.enable
model_profile.read
model_profile.manage
task.read
task.create
task.manage
run.read
run.create
run.command
approval.read
approval.decide
artifact.read
artifact.create
artifact.review
artifact.export
artifact.delete
memory.read
memory.write
memory.verify
audit.read
audit.export
cost.read
budget.manage
operations.read
operations.manage
backup.create
restore.execute
```

Permissions remain distinct from approvals.

## 18. Request envelope

For JSON command endpoints, the body may include:

```json
{
  "schema_version": "1.0.0",
  "request_id": "req_...",
  "correlation_id": "corr_...",
  "requested_at": "2026-07-19T12:00:00Z",
  "payload": {}
}
```

The HTTP method/path remains the primary operation indicator.

## 19. Response envelope

A common response may contain:

```json
{
  "schema_version": "1.0.0",
  "request_id": "req_...",
  "correlation_id": "corr_...",
  "status": "completed",
  "data": {},
  "meta": {},
  "links": {}
}
```

The final implementation may use unwrapped resources if an ADR selects that style.

## 20. Error envelope

Canonical direction:

```json
{
  "schema_version": "1.0.0",
  "error": {
    "code": "RUN_STATE_CONFLICT",
    "message": "The run cannot be cancelled from its current state.",
    "retryable": false,
    "correlation_id": "corr_...",
    "resource": {
      "type": "run",
      "id": "run_..."
    },
    "current_state": "completed",
    "remediation_code": "REFRESH_RESOURCE",
    "details_reference": null
  }
}
```

## 21. Error requirements

Errors include:

- stable code;
- safe message;
- HTTP status;
- retryable flag;
- correlation;
- current state/version where relevant;
- side-effect certainty for consequential operations;
- remediation direction;
- no raw secrets;
- no unrestricted internal stack trace;
- no hidden authorization-policy disclosure.

## 22. HTTP status direction

Suggested mapping:

| Status | Meaning |
|---:|---|
| `200` | Successful read or idempotent command result |
| `201` | Resource created |
| `202` | Asynchronous operation accepted |
| `204` | Successful no-content action |
| `400` | Invalid request |
| `401` | Authentication required/invalid |
| `403` | Authenticated but not authorized |
| `404` | Resource unavailable/not visible |
| `409` | State, version, or idempotency conflict |
| `412` | Precondition/ETag failed |
| `413` | Payload too large |
| `415` | Unsupported media type |
| `422` | Semantically invalid command |
| `423` | Resource locked/held where chosen |
| `429` | Rate limit |
| `500` | Internal error |
| `502` | Upstream adapter/provider error |
| `503` | Service unavailable/degraded |
| `504` | Upstream timeout |

Exact mapping remains subject to API ADR.

## 23. Idempotency

Idempotency is required for:

- create run;
- create approval request;
- consume approval;
- consequential tool command;
- artifact proposal/finalization;
- export;
- backup;
- restore;
- migration;
- cancellation;
- role/permission changes where applicable.

## 24. Idempotency behavior

The server stores:

- key;
- identity;
- workspace;
- operation;
- canonical request hash;
- result reference;
- response status;
- creation/expiry.

Rules:

1. Same key + same request returns original logical result.
2. Same key + different request returns conflict.
3. Keys are scoped to authenticated identity/workspace/operation.
4. Expiry is documented by operation.
5. A timeout does not justify changing the key blindly.
6. Side-effect certainty is returned where relevant.

## 25. Optimistic concurrency

Mutable resources expose:

- integer `version`;
- and/or `ETag`.

Mutations require:

```text
If-Match: "<etag>"
```

or:

```json
{
  "expected_version": 12
}
```

Stale updates return `409` or `412`.

## 26. Patch semantics

Generic JSON Patch or Merge Patch may be used only for safely mutable configuration resources.

Lifecycle-critical resources should use explicit commands.

Clients cannot patch:

- run state;
- approval state;
- approval decision;
- approval consumption;
- artifact acceptance;
- audit event;
- execution receipt;
- usage source state;
- cost source authority.

## 27. Pagination

Cursor pagination is preferred for large or changing collections.

Parameters:

```text
limit
cursor
sort
direction
```

Response metadata:

```json
{
  "page": {
    "limit": 50,
    "next_cursor": "...",
    "previous_cursor": null,
    "has_more": true
  }
}
```

## 28. Pagination rules

- server enforces maximum limit;
- cursor is opaque;
- cursor includes ordering/filter context;
- stale/invalid cursor returns a stable error;
- total counts may be omitted or marked estimated;
- authorization filtering occurs before pagination;
- deleted/revoked resources do not leak through count differences beyond approved policy.

## 29. Sorting

Canonical syntax direction:

```text
sort=created_at
sort=-created_at
```

Only allowlisted fields are sortable.

Sort order must be deterministic with a stable tiebreaker.

## 30. Filtering

Example:

```text
state=running
classification=internal
created_after=...
created_before=...
project_id=...
producer_identity_id=...
```

Filtering is allowlisted and typed.

Arbitrary database query syntax is prohibited.

## 31. Search

Search endpoints or query parameters must:

- scope by workspace first;
- apply authorization before ranking;
- expose freshness;
- label lexical/vector/combined mode;
- avoid returning unauthorized snippets;
- handle deleted/quarantined content;
- rate-limit expensive searches;
- preserve unknown indexing state.

## 32. Field selection and expansion

Potential parameters:

```text
fields=
include=
expand=
```

Rules:

- restricted fields cannot be expanded without authority;
- expansions are bounded;
- cyclic expansion is prohibited;
- maximum depth and count apply;
- expansions do not bypass workspace/classification checks.

## 33. Long-running operations

Asynchronous command response:

```json
{
  "status": "accepted",
  "operation": {
    "operation_id": "op_...",
    "type": "artifact_export",
    "state": "queued",
    "resource_reference": "/artifact-exports/export_..."
  }
}
```

The operation resource exposes state, progress evidence, errors, and result references.

## 34. Operation states

```text
accepted
queued
running
waiting
succeeded
failed
cancelled
stale
unknown
```

Progress percentage is optional and must not be fabricated.

## 35. Operation endpoints

```text
GET  /operations/{operation_id}
POST /operations/{operation_id}/commands/cancel
GET  /operations/{operation_id}/timeline
```

Some domain resources, such as runs and exports, are themselves the long-running resource and may not need a generic operation.

## 36. Event access

The API may expose:

- cursor polling;
- server-sent events;
- WebSocket;
- another approved internal event profile.

Potential endpoints:

```text
GET /events
GET /events/stream
GET /workspaces/{workspace_id}/events
GET /runs/{run_id}/timeline
```

Detailed event contracts belong in `EVT-001`.

## 37. Event API rules

- event IDs are opaque;
- delivery may duplicate;
- cursors are opaque;
- reconnect is supported;
- event classification and workspace filtering apply;
- clients do not set authoritative state from raw adapter events;
- event payload version is explicit;
- retention limits are documented;
- stream disconnect does not imply run failure.

## 38. Organizations

Potential endpoints:

```text
GET  /organizations
POST /organizations
GET  /organizations/{organization_id}
POST /organizations/{organization_id}/commands/suspend
POST /organizations/{organization_id}/commands/archive
```

Organization creation is a privileged operation.

No anonymous organization self-registration is assumed.

## 39. Workspaces

```text
GET  /organizations/{organization_id}/workspaces
POST /organizations/{organization_id}/workspaces
GET  /workspaces/{workspace_id}
PATCH /workspaces/{workspace_id}
POST /workspaces/{workspace_id}/commands/set-read-only
POST /workspaces/{workspace_id}/commands/suspend
POST /workspaces/{workspace_id}/commands/archive
GET  /workspaces/{workspace_id}/health
GET  /workspaces/{workspace_id}/usage
```

Workspace update supports only defined mutable metadata.

## 40. Workspace creation request

Example:

```json
{
  "schema_version": "1.0.0",
  "name": "Research Workspace",
  "purpose": "Controlled agent research",
  "classification": "internal",
  "policy_profile_reference": "policy_profile_...",
  "initial_owner_identity_id": "identity_..."
}
```

## 41. Workspace read model

Response fields may include:

- workspace ID;
- organization ID;
- name and purpose;
- state;
- classification;
- owner summary;
- member count;
- policy profile;
- enabled adapters/capabilities/models;
- budget summary;
- health;
- created/updated times;
- version;
- freshness.

## 42. Workspace members

```text
GET    /workspaces/{workspace_id}/members
POST   /workspaces/{workspace_id}/members
GET    /workspaces/{workspace_id}/members/{identity_id}
PATCH  /workspaces/{workspace_id}/members/{identity_id}
DELETE /workspaces/{workspace_id}/members/{identity_id}
```

Removing membership invalidates future access and may affect sessions/approvals according to policy.

## 43. Role assignments

```text
GET  /workspaces/{workspace_id}/role-assignments
POST /workspaces/{workspace_id}/role-assignments
GET  /workspaces/{workspace_id}/role-assignments/{role_assignment_id}
POST /workspaces/{workspace_id}/role-assignments/{role_assignment_id}/commands/revoke
```

Role changes are explicit, auditable, and may require approval or reauthentication.

## 44. Projects

```text
GET  /workspaces/{workspace_id}/projects
POST /workspaces/{workspace_id}/projects
GET  /projects/{project_id}
PATCH /projects/{project_id}
POST /projects/{project_id}/commands/pause
POST /projects/{project_id}/commands/archive
```

Project resources cannot move between workspaces.

## 45. Agent registrations

```text
GET  /workspaces/{workspace_id}/agent-registrations
POST /workspaces/{workspace_id}/agent-registrations
GET  /agent-registrations/{agent_registration_id}
PATCH /agent-registrations/{agent_registration_id}
POST /agent-registrations/{agent_registration_id}/commands/validate
POST /agent-registrations/{agent_registration_id}/commands/disable
POST /agent-registrations/{agent_registration_id}/commands/revoke
GET  /agent-registrations/{agent_registration_id}/health
GET  /agent-registrations/{agent_registration_id}/readiness
GET  /agent-registrations/{agent_registration_id}/capabilities
```

Raw secret values are not accepted in ordinary registration payloads.

## 46. Register adapter request

Example:

```json
{
  "adapter_type": "codex",
  "display_name": "Local Codex Adapter",
  "implementation_name": "agent-os-codex-adapter",
  "implementation_version": "0.1.0",
  "contract_version": "0.1.0",
  "process_or_endpoint_reference": {
    "type": "local_process_profile",
    "reference_id": "process_profile_..."
  },
  "configuration_reference": "config_...",
  "secret_reference_ids": [],
  "declared_workspace_scope": {
    "workspace_ids": ["workspace_..."]
  }
}
```

## 47. Adapter validation

```text
POST /agent-registrations/{id}/commands/validate
```

Response:

- validation operation;
- profile;
- state;
- tests passed/failed/skipped;
- evidence;
- limitations;
- expiry;
- readiness impact.

Validation never performs unapproved consequential actions.

## 48. Capability registry

```text
GET  /capability-declarations
GET  /capability-declarations/{capability_declaration_id}
GET  /capabilities/{capability_code}
POST /agent-registrations/{id}/commands/refresh-capabilities
GET  /workspaces/{workspace_id}/capability-enablement
POST /workspaces/{workspace_id}/capability-enablement
GET  /workspace-capability-enablement/{id}
POST /workspace-capability-enablement/{id}/commands/suspend
POST /workspace-capability-enablement/{id}/commands/revoke
```

## 49. Capability matching

Potential endpoint:

```text
POST /capability-matches
```

Request includes:

- workspace;
- capability code/version range;
- target type;
- data class;
- required features;
- model requirements;
- resource/network constraints.

Response includes eligible candidates and reasoned exclusions.

This endpoint does not authorize execution.

## 50. Model profiles

```text
GET  /workspaces/{workspace_id}/model-profiles
POST /workspaces/{workspace_id}/model-profiles
GET  /model-profiles/{model_profile_id}
PATCH /model-profiles/{model_profile_id}
POST /model-profiles/{model_profile_id}/commands/validate
POST /model-profiles/{model_profile_id}/commands/disable
POST /model-profiles/{model_profile_id}/commands/deprecate
GET  /model-profiles/{model_profile_id}/readiness
GET  /model-profiles/{model_profile_id}/bindings
POST /model-profiles/{model_profile_id}/bindings
```

## 51. Provider bindings

```text
GET  /provider-bindings/{provider_binding_id}
PATCH /provider-bindings/{provider_binding_id}
POST /provider-bindings/{provider_binding_id}/commands/validate
POST /provider-bindings/{provider_binding_id}/commands/disable
POST /provider-bindings/{provider_binding_id}/commands/revoke
GET  /provider-bindings/{provider_binding_id}/health
GET  /provider-bindings/{provider_binding_id}/quota
GET  /provider-bindings/{provider_binding_id}/pricing
```

## 52. Model route preview

Potential endpoint:

```text
POST /model-routing-previews
```

The preview returns:

- eligible bindings;
- blocked candidates;
- estimated cost state;
- data-disclosure state;
- fallback implications;
- model-identity limitations;
- reasons;
- freshness.

A preview is not a binding reservation or execution.

## 53. Tasks

```text
GET  /workspaces/{workspace_id}/tasks
POST /workspaces/{workspace_id}/tasks
GET  /tasks/{task_id}
PATCH /tasks/{task_id}
POST /tasks/{task_id}/commands/mark-ready
POST /tasks/{task_id}/commands/block
POST /tasks/{task_id}/commands/complete
POST /tasks/{task_id}/commands/cancel
POST /tasks/{task_id}/commands/archive
GET  /tasks/{task_id}/snapshots
POST /tasks/{task_id}/snapshots
```

## 54. Task creation

Example fields:

- title;
- desired outcome;
- project;
- initial scope;
- classification;
- preferred agent;
- preferred model profile;
- execution bounds;
- expected artifacts;
- tags/metadata.

Task creation does not start execution automatically unless an explicit combined workflow is defined.

## 55. Task snapshots

```text
GET  /task-snapshots/{task_snapshot_id}
GET  /task-snapshots/{task_snapshot_id}/integrity
```

Snapshots are immutable.

No update or delete endpoint is provided for active historical snapshots except governed archival/deletion policy where allowed.

## 56. Runs

```text
GET  /workspaces/{workspace_id}/runs
POST /tasks/{task_id}/runs
GET  /runs/{run_id}
GET  /runs/{run_id}/timeline
GET  /runs/{run_id}/steps
GET  /runs/{run_id}/attempts
GET  /runs/{run_id}/waiting-conditions
GET  /runs/{run_id}/checkpoints
GET  /runs/{run_id}/side-effects
GET  /runs/{run_id}/receipt
GET  /runs/{run_id}/cost-summary
```

## 57. Create run

```text
POST /tasks/{task_id}/runs
```

Requires:

- idempotency key;
- selected or latest explicit task snapshot;
- execution bounds;
- optional preferred adapter/model;
- current workspace authorization.

Response:

- `201` if fully created synchronously;
- or `202` if creation/preflight is asynchronous;
- run resource location;
- current state;
- readiness blockers if any.

## 58. Run command endpoints

```text
POST /runs/{run_id}/commands/queue
POST /runs/{run_id}/commands/preflight
POST /runs/{run_id}/commands/pause
POST /runs/{run_id}/commands/resume
POST /runs/{run_id}/commands/cancel
POST /runs/{run_id}/commands/reconcile
POST /runs/{run_id}/commands/resolve-unknown
POST /runs/{run_id}/commands/extend-bounds
POST /runs/{run_id}/commands/finalize
POST /runs/{run_id}/commands/archive
```

Clients cannot set `state` directly.

## 59. Run cancellation request

Example:

```json
{
  "reason_code": "USER_REQUESTED",
  "reason": "The requested work is no longer needed.",
  "deadline_at": "2026-07-19T13:00:00Z",
  "expected_version": 12
}
```

Response distinguishes:

```text
cancel_requested
already_terminal
cannot_cancel
unknown
```

## 60. Step operations

```text
GET  /runs/{run_id}/steps/{step_id}
GET  /runs/{run_id}/steps/{step_id}/attempts
POST /runs/{run_id}/steps/{step_id}/commands/retry
POST /runs/{run_id}/steps/{step_id}/commands/reconcile
POST /runs/{run_id}/steps/{step_id}/commands/skip
```

Skip requires a permitted deterministic reason and cannot bypass required protected work.

## 61. Attempts

```text
GET /runs/{run_id}/attempts/{attempt_id}
GET /runs/{run_id}/attempts/{attempt_id}/events
GET /runs/{run_id}/attempts/{attempt_id}/outputs
GET /runs/{run_id}/attempts/{attempt_id}/usage
GET /runs/{run_id}/attempts/{attempt_id}/model-observation
```

Attempts are append-only and not directly editable.

## 62. Checkpoints

```text
GET  /runs/{run_id}/checkpoints
GET  /checkpoints/{checkpoint_id}
POST /runs/{run_id}/commands/create-checkpoint
POST /checkpoints/{checkpoint_id}/commands/validate
```

Checkpoint content access is classification- and scope-controlled.

## 63. Waiting conditions

```text
GET /runs/{run_id}/waiting-conditions
GET /waiting-conditions/{waiting_condition_id}
```

Administrative resolution, when permitted, uses explicit commands rather than deleting the condition.

## 64. Approval requests

```text
GET  /workspaces/{workspace_id}/approval-requests
POST /runs/{run_id}/approval-requests
GET  /approval-requests/{approval_request_id}
GET  /approval-requests/{approval_request_id}/review-material
GET  /approval-requests/{approval_request_id}/eligibility
GET  /approval-requests/{approval_request_id}/timeline
POST /approval-requests/{approval_request_id}/commands/begin-review
POST /approval-requests/{approval_request_id}/decisions
POST /approval-requests/{approval_request_id}/commands/invalidate
POST /approval-requests/{approval_request_id}/commands/cancel
POST /approval-requests/{approval_request_id}/commands/consume
```

## 65. Approval decision endpoint

```text
POST /approval-requests/{id}/decisions
```

Request:

```json
{
  "decision": "approve",
  "request_version": 4,
  "action_fingerprint": "sha256:...",
  "rationale": "Reviewed the exact diff and target branch."
}
```

The server revalidates:

- session;
- authority;
- independence;
- request state;
- expiry;
- fingerprint;
- policy;
- emergency stop.

## 66. Approval consumption

`consume` is primarily an internal control-plane/Tool Gateway operation.

Human-facing clients generally do not call it directly.

It requires workload identity and exact attempt/action context.

## 67. Standing approval grants

If included:

```text
GET  /workspaces/{workspace_id}/standing-approval-grants
POST /workspaces/{workspace_id}/standing-approval-grants
GET  /standing-approval-grants/{standing_grant_id}
POST /standing-approval-grants/{standing_grant_id}/commands/suspend
POST /standing-approval-grants/{standing_grant_id}/commands/revoke
GET  /standing-approval-grants/{standing_grant_id}/uses
```

These resources remain optional and policy-restricted.

## 68. Artifacts

```text
GET  /workspaces/{workspace_id}/artifacts
POST /workspaces/{workspace_id}/artifacts
GET  /artifacts/{artifact_id}
PATCH /artifacts/{artifact_id}
GET  /artifacts/{artifact_id}/versions
GET  /artifacts/{artifact_id}/versions/{artifact_version_id}
GET  /artifacts/{artifact_id}/provenance
GET  /artifacts/{artifact_id}/relationships
GET  /artifacts/{artifact_id}/timeline
```

Artifact metadata patch is limited to safe mutable metadata.

## 69. Artifact staging

```text
POST /artifacts/{artifact_id}/staging-sessions
GET  /artifact-staging-sessions/{staging_session_id}
PUT  /artifact-staging-sessions/{staging_session_id}/content
POST /artifact-staging-sessions/{staging_session_id}/commands/finalize
POST /artifact-staging-sessions/{staging_session_id}/commands/cancel
```

Large-content upload may use multipart/chunked or signed internal references depending on ADR.

## 70. Artifact version content

```text
GET /artifact-versions/{artifact_version_id}/content
GET /artifact-versions/{artifact_version_id}/download
GET /artifact-versions/{artifact_version_id}/preview
```

Content access requires classification and lifecycle checks.

Quarantined or active content may be blocked.

## 71. Artifact validation and preview

```text
POST /artifact-versions/{id}/commands/validate
POST /artifact-versions/{id}/commands/generate-preview
GET  /artifact-versions/{id}/validations
GET  /artifact-versions/{id}/previews
```

Preview generation is asynchronous where appropriate.

## 72. Artifact review and acceptance

```text
POST /artifact-versions/{id}/reviews
GET  /artifact-versions/{id}/reviews
POST /artifact-reviews/{review_id}/decisions
GET  /artifact-versions/{id}/acceptances
```

Acceptance is version- and purpose-specific.

## 73. Artifact export

```text
POST /artifact-exports
GET  /artifact-exports/{artifact_export_id}
POST /artifact-exports/{artifact_export_id}/commands/cancel
GET  /artifact-exports/{artifact_export_id}/manifest
```

The request identifies exact versions and destination.

## 74. Artifact deletion

```text
POST /artifacts/{artifact_id}/deletion-requests
GET  /artifact-deletion-requests/{deletion_request_id}
POST /artifact-deletion-requests/{id}/commands/execute
POST /artifact-deletion-requests/{id}/commands/cancel
```

No direct generic `DELETE /artifacts/{id}` is required for governed artifacts.

## 75. Memory records

```text
GET  /workspaces/{workspace_id}/memory-records
POST /workspaces/{workspace_id}/memory-records
GET  /memory-records/{memory_record_id}
GET  /memory-records/{memory_record_id}/versions
POST /memory-records/{memory_record_id}/versions
GET  /memory-records/{memory_record_id}/sources
GET  /memory-records/{memory_record_id}/timeline
```

Memory content and authority are distinct fields.

## 76. Memory commands

```text
POST /memory-records/{id}/commands/verify
POST /memory-records/{id}/commands/dispute
POST /memory-records/{id}/commands/supersede
POST /memory-records/{id}/commands/expire
POST /memory-records/{id}/commands/request-deletion
POST /memory-records/{id}/commands/reconcile
```

Agents may propose memory but cannot self-verify authoritative facts.

## 77. Memory search

Potential endpoint:

```text
POST /memory-searches
```

Request includes:

- workspace;
- project;
- query;
- allowed classes;
- authority states;
- freshness;
- maximum results;
- lexical/vector/combined preference.

Response includes:

- source;
- authority;
- confidence;
- freshness;
- ranking explanation;
- index state;
- no unauthorized snippets.

## 78. Audit events

```text
GET /workspaces/{workspace_id}/audit-events
GET /audit-events/{audit_event_id}
GET /runs/{run_id}/audit-events
GET /approval-requests/{id}/audit-events
GET /artifacts/{id}/audit-events
```

Audit events are immutable and filtered by authority/classification.

## 79. Audit search

Filtering may include:

- time range;
- actor;
- action/event type;
- task/run;
- approval;
- artifact;
- result;
- source component;
- correlation;
- risk;
- classification.

Arbitrary free-form access to sensitive event payloads is not assumed.

## 80. Execution receipts

```text
GET  /runs/{run_id}/receipt
POST /runs/{run_id}/commands/generate-receipt
GET  /execution-receipts/{execution_receipt_id}
GET  /execution-receipts/{execution_receipt_id}/artifact
```

Receipt generation may be asynchronous.

## 81. Evidence exports

```text
POST /evidence-exports
GET  /evidence-exports/{evidence_export_id}
GET  /evidence-exports/{evidence_export_id}/manifest
POST /evidence-exports/{evidence_export_id}/commands/cancel
```

Sensitive exports may require exact approval.

## 82. Usage events

```text
GET /workspaces/{workspace_id}/usage-events
GET /runs/{run_id}/usage-events
GET /usage-events/{usage_event_id}
```

Usage records are source-labelled.

Clients cannot replace provider-reported or invoice-authoritative data through generic update.

## 83. Cost records

```text
GET /workspaces/{workspace_id}/cost-records
GET /runs/{run_id}/cost-records
GET /cost-records/{cost_record_id}
GET /workspaces/{workspace_id}/cost-summary
GET /runs/{run_id}/cost-summary
```

Summaries expose:

- known;
- estimated;
- pending;
- unavailable;
- unattributed;
- mismatched;
- reconciled;
- unknown amounts/states.

## 84. Pricing profiles

```text
GET  /pricing-profiles
GET  /pricing-profiles/{pricing_profile_id}
POST /pricing-profiles
POST /pricing-profiles/{id}/commands/deprecate
POST /pricing-profiles/{id}/commands/review
```

Pricing administration is privileged and source-versioned.

## 85. Budgets

```text
GET  /workspaces/{workspace_id}/budgets
POST /workspaces/{workspace_id}/budgets
GET  /budgets/{budget_id}
PATCH /budgets/{budget_id}
POST /budgets/{budget_id}/commands/suspend
POST /budgets/{budget_id}/commands/close
GET  /budgets/{budget_id}/reservations
```

Material budget increases may require approval.

## 86. Cost reconciliation

```text
POST /cost-reconciliations
GET  /cost-reconciliations/{reconciliation_id}
GET  /cost-reconciliations/{reconciliation_id}/findings
```

The reconciliation preserves source differences rather than overwriting them.

## 87. Component health

```text
GET /health
GET /health/live
GET /health/ready
GET /components
GET /components/{component_id}/health
GET /workspaces/{workspace_id}/health
```

### Health endpoint separation

- `live`: process is alive;
- `ready`: safe to accept intended traffic;
- component health: dependency-specific evidence;
- workspace health: scoped operational readiness.

## 88. Health response rules

Health responses may include:

- state;
- observed time;
- freshness;
- limitations;
- dependency states;
- build identity;
- schema version;
- no secrets;
- no unrestricted internal topology for unprivileged callers.

## 89. Emergency stop

```text
GET  /emergency-stops
POST /emergency-stops
GET  /emergency-stops/{emergency_stop_id}
POST /emergency-stops/{id}/commands/release
```

Emergency stop creation and release are privileged, audited, and may require reauthentication or independent authority.

## 90. Maintenance windows

```text
GET  /maintenance-windows
POST /maintenance-windows
GET  /maintenance-windows/{maintenance_window_id}
PATCH /maintenance-windows/{maintenance_window_id}
POST /maintenance-windows/{id}/commands/start
POST /maintenance-windows/{id}/commands/complete
POST /maintenance-windows/{id}/commands/cancel
```

Maintenance state influences readiness and dispatch.

## 91. Backups

```text
GET  /backup-operations
POST /backup-operations
GET  /backup-operations/{backup_operation_id}
GET  /backup-operations/{backup_operation_id}/manifest
POST /backup-operations/{backup_operation_id}/commands/cancel
POST /backup-operations/{backup_operation_id}/commands/verify
```

Backup requests identify exact scope and target reference.

## 92. Restore operations

```text
GET  /restore-operations
POST /restore-operations
GET  /restore-operations/{restore_operation_id}
POST /restore-operations/{id}/commands/validate
POST /restore-operations/{id}/commands/execute
POST /restore-operations/{id}/commands/cancel
GET  /restore-operations/{id}/reconciliation
```

Restore execution requires privileged authority and exact approval where policy requires.

## 93. Migrations

```text
GET  /migrations
GET  /migrations/{migration_id}
POST /migrations/{migration_id}/commands/validate
POST /migrations/{migration_id}/commands/execute
GET  /migrations/{migration_id}/verification
```

Migration APIs never accept arbitrary unreviewed scripts as a generic body.

## 94. Recovery

```text
GET  /recovery/nonterminal-runs
GET  /recovery/expired-leases
GET  /recovery/orphaned-artifacts
GET  /recovery/audit-gaps
POST /recovery/commands/scan
POST /recovery/commands/reconcile
```

Recovery commands are privileged and evidence-producing.

## 95. Configuration metadata

Potential read-only endpoint:

```text
GET /system/configuration-summary
```

It may expose safe non-secret configuration:

- deployment profile;
- build identity;
- enabled features;
- schema versions;
- adapter/model readiness summary;
- storage mode;
- maintenance/emergency state.

Raw environment variables and secrets are never returned.

## 96. Feature flags

Feature flags, if used, require:

- stable flag code;
- scope;
- owner;
- default;
- state;
- expiry/review;
- risk;
- audit;
- no security-control bypass without explicit governance.

Potential endpoints are administrative and may be deferred.

## 97. API versioning

Possible strategies:

```text
path versioning
media-type versioning
header versioning
schema-version fields
```

The final strategy requires ADR.

The draft uses `/api/v1` plus explicit schema versions.

## 98. Version compatibility

Rules:

- breaking resource/field behavior requires major version;
- additive optional fields may be minor-compatible;
- enum extensibility is defined per field;
- clients ignore unknown optional fields only where contract says so;
- clients never infer semantics from unknown lifecycle states;
- deprecations include replacement and removal version;
- event and API versions may evolve independently but are mapped.

## 99. Deprecation headers and metadata

Possible response metadata:

```text
Deprecation
Sunset
Link: rel="successor-version"
```

Resource representations may include:

- deprecated fields;
- replacement field;
- removal version;
- migration guidance.

Final header profile requires ADR.

## 100. Extension namespaces

Provider-specific extension format:

```json
{
  "extensions": {
    "adapter.codex.v1": {},
    "adapter.hermes.v1": {},
    "provider.example.v1": {}
  }
}
```

Extensions:

- are versioned;
- cannot override core fields;
- cannot contain raw secrets;
- obey classification;
- are bounded;
- are safely ignored or rejected according to profile.

## 101. Rate limiting

Rate limits may apply by:

- session;
- workload identity;
- workspace;
- endpoint group;
- expensive search;
- upload/download;
- event stream;
- administrative operation.

Responses include `429`, `Retry-After`, and safe limit metadata.

Rate limits do not replace budgets or provider quotas.

## 102. Request limits

Limits include:

- body size;
- field count;
- nesting depth;
- array length;
- string length;
- upload size;
- filter count;
- expansion depth;
- batch count;
- timeout;
- concurrent streams.

Rejected oversized requests do not enter partial authoritative state unless a staging resource explicitly represents partial content.

## 103. Batch APIs

Batch operations may support bounded reads or low-risk commands.

Rules:

- maximum item count;
- per-item result;
- no wildcard scope;
- explicit atomic versus partial semantics;
- per-item authorization;
- per-item idempotency/fingerprint where needed;
- no hidden expansion;
- no batch bypass of approval.

## 104. Batch response

Example:

```json
{
  "status": "partial",
  "results": [
    {
      "item_id": "artifact_1",
      "status": "completed"
    },
    {
      "item_id": "artifact_2",
      "status": "failed",
      "error": {
        "code": "ARTIFACT_QUARANTINED"
      }
    }
  ]
}
```

## 105. Caching

Default posture for protected resources:

```text
Cache-Control: no-store
```

Selective private caching may be allowed for safe read models.

Shared caches must not serve protected data unless authorization-aware and explicitly designed.

Revocation-sensitive resources use conservative caching.

## 106. Conditional reads

ETag/If-None-Match may support efficient reads.

A `304` response must not leak resource existence to unauthorized callers.

Classification and authorization are evaluated before conditional response.

## 107. Content negotiation

Clients request supported formats through `Accept`.

Unsupported formats return `406` or an equivalent stable error.

Export formats are separate governed operations and not arbitrary negotiation on every resource.

## 108. File upload security

Upload endpoints enforce:

- authenticated workspace;
- staging resource;
- size/quota;
- declared media type;
- filename sanitization;
- no executable handling by default;
- integrity;
- timeout;
- classification;
- safe storage reference;
- no public upload URL;
- no path traversal.

## 109. File download security

Download endpoints enforce:

- workspace/classification authorization;
- lifecycle/quarantine state;
- safe disposition;
- no-sniff;
- short-lived internal reference where used;
- rate/size limit;
- audit where required;
- no raw host/storage path;
- no external redirect unless approved.

## 110. Streaming responses

Streaming may be used for:

- run events;
- adapter output;
- artifact upload/download;
- export generation status.

Rules:

- stream identity and scope are bound at open;
- authorization is rechecked or bounded by short-lived session;
- disconnect does not cancel work automatically;
- backpressure and size limits apply;
- partial/final markers are explicit;
- secrets are filtered;
- reconnect uses cursor where supported.

## 111. Security headers and browser use

For browser-facing control-plane APIs and UI:

- CSRF protection where cookie sessions are used;
- same-site cookie policy;
- secure/HTTP-only cookies;
- origin checks;
- content-security policy in UI;
- anti-clickjacking;
- HSTS when TLS is used;
- no wildcard CORS by default;
- trusted host validation.

## 112. CORS

Default:

```text
disabled or same-origin only
```

Any allowed origin is explicit and environment-specific.

Credentials with wildcard origins are prohibited.

## 113. CSRF

State-changing browser requests with cookie authentication require CSRF defense.

Bearer/workload profiles require equivalent replay and origin considerations.

Approval and restore actions may require recent reauthentication beyond CSRF.

## 114. Secret handling

The API:

- accepts secret reference IDs, not values, in ordinary resources;
- never returns raw secret values;
- redacts logs;
- validates purpose/target;
- audits secret-use metadata;
- rate-limits secret-sensitive operations;
- avoids secrets in URLs, query strings, events, and errors.

## 115. Prompt and untrusted content handling

API content fields may contain untrusted instructions.

The server treats them as data.

They cannot:

- assign roles;
- approve actions;
- expand workspace scope;
- alter policy;
- disable audit;
- authorize tools;
- change network or filesystem scope.

## 116. Audit of API calls

Audit coverage includes:

- authentication/session events;
- membership and role changes;
- adapter/model configuration;
- run commands;
- approval decisions/consumption;
- artifact export/deletion;
- memory verification/deletion;
- evidence export;
- budget changes;
- backup/restore;
- emergency stop;
- security-sensitive reads.

Ordinary high-volume safe reads may use configurable audit granularity.

## 117. API access logs

Access logs should contain:

- request/correlation ID;
- timestamp;
- route template;
- method;
- authenticated identity type/ID;
- workspace where applicable;
- status;
- latency;
- response size;
- error code;
- no raw secret;
- limited content data.

Sensitive path parameters may be normalized or hashed according to policy.

## 118. Observability

API metrics may include:

- request count;
- latency by route;
- error rate;
- authentication failure;
- authorization denial;
- rate limit;
- idempotency hit/conflict;
- concurrency conflict;
- payload rejection;
- async operation queue time;
- stream count/disconnect;
- upload/download volume;
- endpoint dependency failures;
- stale/unknown responses.

## 119. Tracing

Trace context should propagate through:

```text
API
→ control-plane service
→ orchestrator
→ adapter/model/tool gateway
→ artifact/audit/cost services
```

Trace data remains classified and does not include raw confidential payloads by default.

## 120. API health and degraded behavior

When a dependency is degraded:

| Dependency | API behavior |
|---|---|
| Audit unavailable | Protected writes fail closed according to policy |
| Job store unavailable | Run creation may persist blocked state or fail safely |
| Adapter unavailable | Readiness false; new run may block |
| Artifact store unavailable | Metadata reads may work; content unavailable |
| Search index unavailable | Direct reads work; search degraded |
| Cost service unavailable | Cost state unknown/pending |
| Event stream unavailable | Polling fallback where supported |
| Backup service unavailable | Backup/restore commands blocked |
| Identity provider unavailable | Existing bounded sessions may follow policy; new login blocked |

## 121. API documentation

The implementation should provide:

- machine-readable OpenAPI or equivalent;
- human-readable endpoint guide;
- authentication examples;
- idempotency examples;
- concurrency examples;
- error catalogue;
- event links;
- schema examples;
- compatibility/deprecation guidance;
- security warnings;
- local-development instructions.

Final machine-readable technology requires ADR.

## 122. Client SDK direction

Generated or maintained SDKs may support:

- typed resources;
- auth/session handling;
- pagination;
- idempotency;
- ETag concurrency;
- retries for safe operations;
- long-running operations;
- event cursors;
- error types;
- file staging;
- no automatic consequential retries.

SDKs must not hide unknown, partial, stale, or approval-required states.

## 123. Retry guidance for clients

Clients may retry automatically only when:

- operation is read-only;
- or idempotency is established;
- server marks retryable;
- side-effect certainty permits;
- retry limit/backoff applies;
- deadline remains valid.

Clients must not automatically retry:

- approval decisions with changed state;
- approval consumption after unknown response without reconciliation;
- protected tool actions with unknown effect;
- restore execution;
- destructive migration;
- external message send without idempotent evidence.

## 124. API error catalogue — common

```text
API_REQUEST_INVALID
API_SCHEMA_VERSION_UNSUPPORTED
API_MEDIA_TYPE_UNSUPPORTED
API_AUTHENTICATION_REQUIRED
API_AUTHENTICATION_FAILED
API_REAUTHENTICATION_REQUIRED
API_AUTHORIZATION_DENIED
API_RESOURCE_NOT_FOUND
API_WORKSPACE_SCOPE_MISMATCH
API_CLASSIFICATION_DENIED
API_IDEMPOTENCY_KEY_REQUIRED
API_IDEMPOTENCY_CONFLICT
API_VERSION_CONFLICT
API_PRECONDITION_FAILED
API_RATE_LIMITED
API_PAYLOAD_TOO_LARGE
API_FILTER_INVALID
API_CURSOR_INVALID
API_EXPANSION_LIMIT_EXCEEDED
API_OPERATION_NOT_SUPPORTED
API_DEPENDENCY_UNAVAILABLE
API_TIMEOUT
API_INTERNAL_ERROR
```

Domain errors from RUN/APR/ART/MEM/etc. remain domain-specific.

## 125. Security error posture

The API may intentionally return the same safe error posture for:

- nonexistent resource;
- unauthorized resource;
- cross-workspace resource.

Detailed denial reason remains in restricted audit evidence, not necessarily in client response.

## 126. API conformance tests

### Authentication and authorization

- no session;
- expired/revoked session;
- wrong workspace;
- role missing;
- classification denied;
- workload calls human endpoint;
- agent attempts approval.

### Idempotency

- same request/key;
- different request/same key;
- timeout and replay;
- concurrent replay;
- expired key.

### Concurrency

- stale ETag;
- two updates;
- cancel versus complete;
- approval decision race;
- artifact finalize race;
- budget update race.

### Pagination/filtering

- cursor continuity;
- filter change with old cursor;
- authorization before count;
- stable sorting;
- invalid limits.

### Async operations

- accepted;
- failure;
- cancellation;
- stale/unknown;
- reconnect and poll.

### Security

- secret in URL/body/error;
- CORS abuse;
- CSRF;
- path traversal;
- oversized JSON;
- nested payload;
- mass assignment;
- extension override;
- injection payload;
- cross-workspace object ID.

## 127. Contract tests

Contract tests validate:

- request/response schemas;
- required headers;
- status/error mapping;
- enum behavior;
- version/ETag behavior;
- idempotency;
- pagination;
- content types;
- examples;
- backward compatibility;
- deprecation metadata.

## 128. Negative tests

Every mutation endpoint requires negative tests for:

- unauthorized identity;
- wrong workspace;
- invalid lifecycle state;
- stale version;
- invalid idempotency;
- prohibited action;
- malformed extension;
- invalid classification;
- invalid target/reference;
- emergency stop;
- dependency unavailable.

## 129. Performance targets

Initial API targets align with `NFR-001`.

Proposed:

- common local read p95 ≤ 500 ms;
- Mission Control aggregate read p95 ≤ 2.5 s;
- command acceptance p95 ≤ 1 s excluding external work;
- health endpoint p95 ≤ 500 ms locally;
- event propagation p95 ≤ 2 s after accepted platform event;
- bounded upload/download resource use.

Targets remain provisional until measured.

## 130. Capacity targets

Initial MVP direction:

- 5 concurrent users;
- 4 active runs;
- 20 workspaces;
- 10,000 runs;
- 25,000 artifact metadata records;
- bounded event and audit history;
- multiple adapters/model profiles.

API limits and pagination must support these volumes without relying on unbounded responses.

## 131. Availability and consistency

Strong consistency is required for:

- role/membership changes;
- run transitions;
- approval decisions/consumption;
- budget reservation;
- artifact version finalization;
- deletion state;
- emergency stop.

Eventual consistency is acceptable for:

- dashboards;
- search;
- indexes;
- cost summaries;
- observability;
- derived analytics;
- some timeline projections.

Responses expose freshness.

## 132. Read-after-write behavior

Command responses should include or link to the new authoritative resource version.

Read models may lag.

Clients should use the authoritative resource or operation location rather than assume every dashboard projection updates immediately.

## 133. Data minimization

API representations should support audience-appropriate fields.

A user who can list artifacts may not automatically access:

- full content;
- provenance detail;
- approval rationale;
- secret metadata;
- audit payload;
- confidential cost source;
- restricted operational diagnostics.

## 134. Privacy and personal data

The API must:

- minimize personal data;
- expose purpose and scope;
- support deletion/export lifecycle where applicable;
- avoid leaking identity through unauthorized counts/search;
- protect access logs;
- retain approval/audit identity only as required;
- expose provider disclosure state for model operations.

A dedicated privacy document remains **proposed/unregistered**.

## 135. Accessibility implications

Although APIs are not visual interfaces, they must support accessible clients by exposing:

- explicit state labels;
- reason codes;
- structured errors;
- canonical review material;
- text alternatives/metadata for artifact previews;
- no color-only semantics;
- stable ordering and labels;
- locale-independent machine codes.

## 136. Localization

Machine codes remain English and stable.

Human-readable messages may be localized.

Clients must use machine codes for logic, not translated message text.

Locale may be requested through standard headers or user settings.

## 137. API changelog

Every release should publish:

- added endpoints/fields;
- changed semantics;
- deprecated endpoints/fields;
- removed behavior;
- migration steps;
- security implications;
- event/schema changes;
- SDK impact.

## 138. Release gates

Before an API version is released:

1. machine schema validates;
2. examples validate;
3. auth/authorization tests pass;
4. workspace isolation tests pass;
5. idempotency tests pass;
6. concurrency tests pass;
7. domain lifecycle tests pass;
8. errors are safe;
9. secrets are absent;
10. request limits are enforced;
11. documentation is generated;
12. backward compatibility is assessed;
13. deprecation metadata is correct;
14. observability exists;
15. negative and abuse tests pass.

## 139. Requirement catalogue

### Core contract

- `API-REQ-CORE-001` — All protected operations authenticate.
- `API-REQ-CORE-002` — Workspace scope is authorized before access.
- `API-REQ-CORE-003` — Lifecycle changes use guarded commands.
- `API-REQ-CORE-004` — Idempotency is available for consequential creates/commands.
- `API-REQ-CORE-005` — Optimistic concurrency protects mutable aggregates.
- `API-REQ-CORE-006` — Async work has durable status resources.
- `API-REQ-CORE-007` — Errors have stable codes and correlation.
- `API-REQ-CORE-008` — Unknown/stale/partial states remain explicit.
- `API-REQ-CORE-009` — Provider extensions cannot override core fields.
- `API-REQ-CORE-010` — Compatibility and deprecation are versioned.

### Security

- `API-REQ-SEC-001` — Raw secrets are never returned.
- `API-REQ-SEC-002` — Human approval endpoints reject workload identities.
- `API-REQ-SEC-003` — Cross-workspace references are rejected safely.
- `API-REQ-SEC-004` — CSRF/CORS/browser controls match auth profile.
- `API-REQ-SEC-005` — Upload/download are bounded and classified.
- `API-REQ-SEC-006` — Mass assignment is prevented.
- `API-REQ-SEC-007` — Emergency stop gates consequential commands.
- `API-REQ-SEC-008` — Sensitive actions may require reauthentication.
- `API-REQ-SEC-009` — Access logs exclude sensitive payloads.
- `API-REQ-SEC-010` — Public anonymous access is disabled.

### Reliability

- `API-REQ-REL-001` — Idempotent replay returns original logical result.
- `API-REQ-REL-002` — Same key/different payload conflicts.
- `API-REQ-REL-003` — Stale mutations fail.
- `API-REQ-REL-004` — Stream disconnect does not imply execution failure.
- `API-REQ-REL-005` — Dependency degradation is explicit.
- `API-REQ-REL-006` — Event cursors support reconnect where provided.
- `API-REQ-REL-007` — Pagination is stable and bounded.
- `API-REQ-REL-008` — Long-running operations survive client disconnect.
- `API-REQ-REL-009` — Safe retry guidance includes side-effect certainty.
- `API-REQ-REL-010` — Read-model freshness is exposed.

### Data

- `API-REQ-DAT-001` — Canonical fields reuse `DCT-001`.
- `API-REQ-DAT-002` — Identifiers are opaque.
- `API-REQ-DAT-003` — Time and money formats are explicit.
- `API-REQ-DAT-004` — Classification is carried on protected content.
- `API-REQ-DAT-005` — Source/authority states are preserved.
- `API-REQ-DAT-006` — Configured and actual model identities remain distinct.
- `API-REQ-DAT-007` — Usage and cost states remain explicit.
- `API-REQ-DAT-008` — Audit/event schemas are versioned.
- `API-REQ-DAT-009` — Extensions are namespaced.
- `API-REQ-DAT-010` — Breaking changes require versioning.

## 140. Traceability

| Source | API-001 response |
|---|---|
| `FR-IDN-*` | Authentication and sessions |
| `FR-WSP-*` | Organizations, workspaces, roles, projects |
| `FR-AGT-*` | Adapter registration and health |
| `FR-MOD-*` | Model profiles, bindings, routing |
| `FR-TSK-*` | Tasks and snapshots |
| `FR-RUN-*` | Run/step/attempt commands and reads |
| `FR-APR-*` | Approval request/decision/consumption |
| `FR-MEM-*` | Memory records/search/lifecycle |
| `FR-ART-*` | Artifact staging/version/review/export/delete |
| `FR-AUD-*` | Audit and receipts |
| `FR-CST-*` | Usage, cost, budgets, reconciliation |
| `FR-OPS-*` | Health, backup, restore, maintenance, recovery |
| `NFR-SEC-*` | Auth, scope, secrets, browser security |
| `NFR-REL-*` | Idempotency, concurrency, async behavior |
| `NFR-PERF-*` | Latency, pagination, bounded requests |
| `NFR-INT-*` | Versioning and provider neutrality |
| `THR-001` | API abuse, leakage, replay, injection controls |

## 141. Mapping to components

| API area | Primary component |
|---|---|
| Sessions/authorization | Control Plane + Identity Service |
| Workspaces/projects | Workspace Governance |
| Agents/capabilities/models | Registry + Adapter/Model Gateways |
| Tasks/runs | Control Plane + Orchestrator |
| Approvals | Approval Service |
| Artifacts | Artifact Service |
| Memory | Memory Service |
| Audit/receipts | Audit Service |
| Cost/budget | Usage and Cost Service |
| Operations | Operations and Health Service |
| Backups/restores | Backup Utility |
| Events | Job/Event Store + projections |

## 142. ADR backlog

### `ADR-TBD-API-001 — Primary API style and framework`

Choose resource-oriented HTTP, RPC, GraphQL, gRPC, or hybrid and implementation framework.

### `ADR-TBD-API-002 — Versioning strategy`

Choose path, media type, header, schema versioning, and deprecation profile.

### `ADR-TBD-API-003 — Authentication and session profile`

Choose local identity, external IdP, cookie/bearer/workload credentials, session storage, and reauthentication.

### `ADR-TBD-API-004 — Long-running operation and event access`

Choose operation resources, polling, SSE, WebSocket, and cursor behavior.

### `ADR-TBD-API-005 — Machine-readable specification and SDK generation`

Choose OpenAPI or equivalent, code generation, contract testing, and publication process.

## 142A. ADR-003 API scope fields

Resource APIs must carry or derive the following scope where applicable: `workspace_id`, `project_id`, `mission_id`, `task_id`, `conversation_id`, actor identity, visibility (`private`, `project`, `workspace`), risk class, policy decision, approval reference, retention profile, correlation ID, and run ID. Authorization is enforced server-side for every resource and derived result. Client-provided identifiers never replace authorization checks.

## 142B. Conversation API profile

The conversation API is governed by `ADR-005` and must expose explicit scope and visibility:

| Operation | Endpoint direction | Required behavior |
|---|---|---|
| Create conversation | `POST /workspaces/{workspace_id}/conversations` | Defaults to `private`; records owner and capture boundary |
| List conversations | `GET /workspaces/{workspace_id}/conversations` | Returns only authorized conversations; filters before search/pagination |
| Read conversation | `GET /conversations/{conversation_id}` | Enforces conversation-level authorization |
| Add message | `POST /conversations/{conversation_id}/messages` | Records actor/provider/adapter provenance and correlation |
| Share conversation | `POST /conversations/{conversation_id}/shares` | Explicit project/workspace share, expiry, and audit event |
| Revoke share | `DELETE /conversations/{conversation_id}/shares/{share_id}` | Immediately invalidates derived access |
| Archive/delete | `POST /conversations/{conversation_id}/archive` and delete command | Applies retention, hold, backup, and derived-index rules |

Conversation responses must not expose messages, attachments, derived memory, artifacts, or run evidence outside the authorized visibility scope. Search and notification endpoints apply the same authorization predicate.

## 143. Open decisions

1. Which primary API style and framework?
2. Which base-path/versioning strategy?
3. Which authentication methods enter MVP?
4. Cookie session, bearer token, or both?
5. Which reauthentication rules apply?
6. Which resources use ETag versus expected version?
7. Which mutations allow PATCH?
8. Which long-running commands use generic operations?
9. Is SSE, WebSocket, polling, or a hybrid selected?
10. Which endpoints are UI-only versus stable external contract?
11. Which batch APIs are allowed?
12. Which fields support sparse fieldsets/expansion?
13. Which filters and sort orders are required first?
14. Which error-to-HTTP mapping is final?
15. Which idempotency retention periods apply?
16. Which read models are materialized?
17. Which event history is available through API?
18. Which audit reads require elevated authority?
19. Which artifact upload profile is selected?
20. Which direct-download formats are allowed?
21. Which memory-search modes enter MVP?
22. Which cost/pricing administration is exposed?
23. Which backup/restore APIs require dual approval?
24. Which API documentation and SDKs are generated?
25. Which public/internal compatibility commitments apply?

## 144. Risks

| Risk | Consequence | Response |
|---|---|---|
| Generic CRUD changes lifecycle state | Invariant bypass | Explicit commands |
| Header workspace treated as authority | Cross-workspace leakage | Resource authorization |
| Idempotency missing | Duplicate effects | Required keys |
| Client retries unknown effect | Duplicate consequence | Side-effect guidance |
| Stale update overwrites state | Data corruption | ETag/version |
| Search ranks before auth | Data leak | Scope first |
| Expansion exposes restricted data | Over-disclosure | Bounded authorization |
| API exposes raw secrets | Credential compromise | References only |
| Generic PATCH mass assignment | Privilege/state escalation | Allowlisted fields |
| Public CORS | Cross-origin abuse | Same-origin/default deny |
| Stream disconnect treated as failure | Unsafe retry | Durable state/polling |
| Error reveals policy/resource existence | Security leak | Safe error posture |
| Version changes silently | Client breakage | Contract/version governance |
| Provider extension overrides core | Semantic corruption | Namespaced extensions |
| Async operation lacks status | Lost work | Durable operation resource |
| Health endpoint leaks topology | Reconnaissance | Audience-specific detail |
| Upload executes content | Host compromise | Staging and validation |
| Restore API accepts arbitrary script | Catastrophic mutation | Registered plans and approval |
| Cost summary treats unknown as zero | Misleading decisions | Explicit states |
| SDK hides partial/unknown | Unsafe automation | Typed explicit states |

## 145. Assumptions

- protected local HTTP or equivalent transport is available;
- authentication/session infrastructure can be implemented;
- transactional storage supports idempotency and optimistic concurrency;
- domain services expose command/query boundaries;
- event cursors or timelines can be implemented;
- machine-readable schemas can be generated;
- clients can handle asynchronous resources;
- upload/download staging can be protected;
- API tests can run in CI and local environments.

## 146. Constraints

- no public anonymous API;
- no raw secret access;
- no direct client state assignment for runs/approvals/artifacts;
- no unrestricted shell/database endpoint;
- no production or financial mutation API;
- no autonomous merge endpoint;
- no wildcard CORS;
- no accepted mock state as authoritative;
- no final framework or transport selected;
- Git versioning remains deferred until all documents and global consistency review are complete.

## 147. Acceptance criteria

API-001 may advance to `1.0.0` when:

1. Product accepts exposed user and operator journeys.
2. Architecture accepts resources, commands, async model, versioning, and component boundaries.
3. Security accepts authentication, authorization, scope, secrets, browser controls, and error posture.
4. Data accepts canonical schemas, pagination, source, classification, and compatibility.
5. Operations accepts health, rate limits, maintenance, backup, restore, and recovery endpoints.
6. Quality accepts contract, negative, concurrency, security, and compatibility tests.
7. every lifecycle-critical mutation is guarded;
8. consequential creates/commands are idempotent;
9. stale writes are rejected;
10. workspace isolation is testable on every protected resource group;
11. errors are safe and stable;
12. async work is durable and observable;
13. upload/download is governed;
14. machine-readable specifications can be produced;
15. `EVT-001`, `DEV-001`, `TST-001`, `QAG-001`, `OBS-001`, `OPS-001`, and `BCP-001` can proceed.

## 148. Downstream impact

| Document | Required use |
|---|---|
| `EVT-001` | Event access, cursors, integration event links |
| `DEV-001` | API implementation, schemas, clients, local development |
| `TST-001` | Contract, security, concurrency, compatibility tests |
| `QAG-001` | API release and compatibility gates |
| `OBS-001` | Route latency/error/idempotency/stream metrics |
| `OPS-001` | API startup, auth, rate-limit, degraded-mode runbooks |
| `BCP-001` | Backup/restore/recovery API behavior |
| `RTM-001` | API requirements-to-tests/evidence traceability |

## 149. Revision and approval history

### Approval state

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial control-plane API specification covering authentication, authorization, organizations, workspaces, agents, capabilities, models, tasks, runs, approvals, artifacts, memory, audit, costs, operations, versioning, errors, idempotency, concurrency, pagination, streaming, security, testing, and governance |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SAD-001` — System Architecture Description
- `DCT-001` — Data Dictionary
- `AGC-001` — Agent Adapter Contract
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
