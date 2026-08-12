---
document_id: ADR-002
title: Runtime Authentication and Secret Configuration
version: 0.1.0
status: draft
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
created: 2026-08-12
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents:
  - SEC-001
  - API-001
  - DEP-001
related_adrs:
  - ADR-001
---

# ADR-002 — Runtime Authentication and Secret Configuration

Status: Proposed

## Context

The MVP exposed control-plane routes without an authentication dependency and
contained development credentials and signing-key defaults in source/config.
The local stack also lacked a deterministic migration step for all runtime
tables.

## Decision drivers

- Protect every non-health API route with a bearer token.
- Keep credentials and signing keys outside version control.
- Preserve local Docker reproducibility without creating a hidden default user.
- Make the database schema owned by Alembic in runtime deployments.

## Considered options

### Option A — Global JWT dependency with environment bootstrap identity

Selected for the current MVP. It is small, vendor-neutral, and keeps the
authentication boundary explicit while a persistent identity provider is not
yet part of the product.

### Option B — Leave routes public until a full identity service exists

Rejected because durable workspaces, approvals, and audit records would remain
exposed during development and staging.

### Option C — Add an external identity provider now

Deferred. It requires a product and deployment decision beyond this bounded
runtime hardening mission.

## Decision

- `/api/v1/auth/token` issues short-lived JWTs only for the administrator
  identity supplied through `ADMIN_EMAIL` and `ADMIN_PASSWORD`.
- All other `/api/v1` routers require a valid bearer token.
- `SECRET_KEY`, database credentials, and bootstrap credentials are required
  through environment configuration and documented in `.env.example` only as
  placeholders.
- Alembic upgrades the complete schema before the backend starts in Compose.
- The frontend stores the access token locally for this prototype and provides
  an explicit sign-in/sign-out flow.

## Consequences

### Positive

- Unauthenticated API calls fail with `401`.
- No default account or signing key is committed.
- Runtime and test schemas have an explicit migration path.

### Negative

- A single bootstrap administrator is not a complete multi-user IAM system.
- Existing local users must configure credentials and sign in again.
- Browser local storage is an MVP token storage choice and needs a stronger
  session model before production.

## Risks and mitigations

- Rotate the environment secret if it is exposed.
- Replace the bootstrap identity with persistent IAM before production.
- Add CSRF/session hardening if cookie-based authentication is introduced.

## Validation plan

- API tests cover token issuance, unauthenticated rejection, and authenticated
  access.
- Compose applies Alembic revisions `0001` through `0003`.
- Frontend production build and authenticated local runtime are required.

## Migration or compatibility impact

API consumers must send `Authorization: Bearer <token>` to protected routes.
The frontend login screen is the supported local entry point.

## Related requirements

- `SEC-001` security controls
- `API-001` control-plane API contract

## Supersedes / Superseded by

None.
