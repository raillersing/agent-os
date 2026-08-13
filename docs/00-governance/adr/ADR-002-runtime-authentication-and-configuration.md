---
document_id: ADR-002
title: Runtime Authentication and Secret Configuration
version: 1.0.1
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
created: 2026-08-12
last_reviewed: 2026-08-13
review_records:
  - role: product-owner
    review_status: approved
    review_date: 2026-08-13
    evidence: explicit user authorization after document review; architecture-owner approval remains required
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user authorization after document review
pending_approvals:
  - architecture-owner
classification: internal
source_of_truth: false
related_documents:
  - SEC-001
  - API-001
  - DEP-001
related_adrs:
  - ADR-001
  - ADR-008
---

# ADR-002 — Runtime Authentication and Secret Configuration

**Status: In review — product-owner approval recorded on 2026-08-13; architecture-owner approval remains pending.**

This status correction does not reverse the runtime hardening already present in the repository. It corrects the prior contradiction between an `approved` status and a non-empty `pending_approvals` list. The implemented bootstrap authentication remains a development baseline, not the target pilot IAM model.

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

Selected for the current development MVP. It is small, vendor-neutral, and keeps the
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
- Alembic upgrades the complete schema before the backend starts in the current development Compose profile.
- The frontend stores the access token locally for this prototype and provides
  an explicit sign-in/sign-out flow.
- The environment-provided administrator is a **temporary D0/D1 bootstrap mechanism**. It must not be the shared or generic pilot identity model.
- Before the D3 controlled pilot, Agent OS must use persistent named human identities, workspace memberships, role/grant evaluation, session expiry, and reauthentication for critical actions as governed by `IAM-001` and the approved pilot baseline.
- Pilot secret handling is not defined by this ADR; `ADR-008` owns the selected pilot deployment and secret-handling baseline once approved.

## Consequences

### Positive

- Unauthenticated API calls fail with `401`.
- No default account or signing key is committed.
- Runtime and test schemas have an explicit migration path.
- The documentation no longer presents the bootstrap administrator as the target identity architecture.

### Negative

- A single bootstrap administrator is not a complete multi-user IAM system.
- Existing local users must configure credentials and sign in again.
- Browser local storage is an MVP token storage choice and needs a stronger
  session model before pilot use.

## Risks and mitigations

- Rotate an environment secret if exposure is suspected.
- Replace the bootstrap identity with persistent IAM before the controlled pilot.
- Add CSRF/session hardening if cookie-based authentication is introduced.
- Never treat presence of a bootstrap credential as authorization for a workspace, approval, secret, restore, migration, or deployment operation.

## Validation plan

- API tests cover token issuance, unauthenticated rejection, and authenticated
  access.
- Development Compose applies the currently supported Alembic revisions.
- Frontend production build and authenticated local runtime are required.
- Pilot readiness additionally requires named identities and workspace-isolation tests under `IAM-001` and `QAG-001`.

## Migration or compatibility impact

API consumers must send `Authorization: Bearer <token>` to protected routes for the current development implementation.
The frontend login screen is the supported local entry point until persistent IAM replaces the bootstrap path.

## Related requirements

- `SEC-001` security controls
- `API-001` control-plane API contract
- `IAM-001` target identity and access-management architecture
- `ADR-008` pilot deployment and secret-handling baseline

## Supersedes / Superseded by

None.
