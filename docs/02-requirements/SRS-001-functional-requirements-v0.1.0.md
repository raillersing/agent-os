---
document_id: SRS-001
title: Agent OS Functional Requirements Specification
version: 0.2.0
status: approved
owner: product-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - quality-owner
created: 2026-07-19
last_reviewed: 2026-08-13
approval_date: 2026-08-13
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user authorization; user assumes the designated approval roles for this finalization
pending_approvals: []
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PER-001
  - UCD-001
  - PRD-001
  - NFR-001
  - AUT-001
  - RTM-001
  - SAD-001
  - SEC-001
  - TST-001
related_adrs: []
---

# SRS-001 — Agent OS Functional Requirements Specification

> **Status: Approved baseline — 2026-08-13.** This document defines proposed, testable functional requirements for the first Agent OS MVP. It does not prove implementation, choose final technologies, authorize production use, or replace non-functional, architecture, security, contract, and test specifications.

## 1. Document purpose

This document converts the product requirements in `PRD-001` and the journeys/use cases in `UCD-001` into stable, testable functional requirements.

Every mandatory requirement includes:

- stable identifier;
- title and rationale;
- priority;
- actors;
- preconditions;
- required behavior;
- failure behavior;
- security or approval implications;
- measurable acceptance criteria;
- source traceability.

Detailed API schemas, state schemas, events, storage models, security controls, and test procedures remain owned by downstream controlled documents.

## 2. Scope

The specification covers the first local Agent OS MVP:

- authenticated access;
- one organization context;
- multiple isolated workspaces;
- projects, membership, and predefined roles;
- Hermes and Codex adapters;
- model profiles and budgets;
- bounded tasks;
- durable runs and steps;
- cancellation, retry, interruption, and recovery;
- exact-action approvals;
- governed tools and integrations;
- permission-aware memory;
- artifacts and provenance;
- audit and execution receipts;
- usage and cost attribution;
- responsive Mission Control;
- health, backup, and restore.

The specification excludes public multi-tenant SaaS, unrestricted machine control, production financial posting, autonomous merge, unrestricted external messaging, high availability, swarms, self-modifying skills, marketplace, predictive profit automation, and full media Studio.

## 3. Source precedence

For this draft:

1. approved `VSN-001`;
2. approved content direction of `SCP-001`;
3. `PRD-001`;
4. `PER-001` and `UCD-001`;
5. this `SRS-001`;
6. future architecture, contracts, implementation, and tests.

When a conflict is found, the higher-precedence approved source governs until a controlled change resolves it.

## 4. Requirement conventions

### 4.1 Requirement identifiers

Functional requirements use:

```text
FR-<DOMAIN>-<NUMBER>
```

Domains:

- `AUTH` — authentication and identity;
- `WSP` — organization, workspace, project, membership;
- `AGT` — agent registry and adapters;
- `MOD` — model profiles and provider use;
- `TSK` — task management;
- `RUN` — run execution and recovery;
- `APR` — approvals;
- `TOL` — tools and integrations;
- `MEM` — memory and knowledge;
- `ART` — artifacts;
- `AUD` — audit and evidence;
- `CST` — usage and cost;
- `UI` — Mission Control and interaction;
- `OPS` — operations, health, backup, restore.

### 4.2 Priorities

- `Must` — required for MVP acceptance;
- `Should` — important and expected unless explicitly deferred;
- `Could` — optional after higher priorities;
- `Won't-MVP` — intentionally excluded.

### 4.3 Normative language

- **shall** indicates mandatory behavior;
- **should** indicates a strong recommendation requiring documented rationale if deferred;
- **may** indicates permitted behavior;
- ambiguous words such as “fast,” “easy,” or “secure” require measurable definition in `NFR-001`.

## 5. Actors

| Actor | Description |
|---|---|
| Human user | Authenticated person |
| Platform administrator | Operates the local installation |
| Workspace Owner | Manages one workspace, members, budgets, and policy |
| Builder-Operator | Creates tasks and supervises runs |
| Reviewer / Approver | Decides exact consequential actions |
| Auditor | Reads authorized evidence |
| Contributor | Consumes permitted artifacts |
| Agent adapter | Hermes, Codex, or future adapter implementation |
| Agent worker | Workload identity executing bounded work |
| Tool gateway | Enforces tool and integration policy |
| System | Agent OS control-plane behavior |

## 6. Shared functional rules

1. Every protected action shall be attributable to an identity.
2. Every protected record shall carry organization/workspace scope where applicable.
3. Prompt text shall not override authorization.
4. External execution shall not begin before a durable run exists.
5. Consequential actions shall remain blocked without valid exact-action approval.
6. Unknown, unavailable, stale, partial, failed, cancelled, and completed states shall remain distinct.
7. Secrets shall not be stored as ordinary prompt, memory, artifact, log, or audit content.
8. Cross-workspace access shall be denied by default.
9. Accepted workflows shall not silently depend on non-persistent mock data.
10. Generated analysis shall remain separate from authoritative source records.
11. Failure to record mandatory security/audit evidence may block consequential execution.
12. Historical evidence shall not be erased merely because a capability is disabled or a task is archived.

## 7. Functional requirement catalogue

| Domain | Requirement range | Count |
|---|---:|---:|
| Authentication and identity | `FR-AUTH-001`–`004` | 4 |
| Workspaces and membership | `FR-WSP-001`–`007` | 7 |
| Agent adapters | `FR-AGT-001`–`006` | 6 |
| Models and providers | `FR-MOD-001`–`005` | 5 |
| Tasks | `FR-TSK-001`–`006` | 6 |
| Runs and recovery | `FR-RUN-001`–`010` | 10 |
| Approvals | `FR-APR-001`–`008` | 8 |
| Tools and integrations | `FR-TOL-001`–`007` | 7 |
| Memory and knowledge | `FR-MEM-001`–`006` | 6 |
| Artifacts | `FR-ART-001`–`006` | 6 |
| Audit and evidence | `FR-AUD-001`–`006` | 6 |
| Usage and cost | `FR-CST-001`–`005` | 5 |
| Mission Control and UI | `FR-UI-001`–`007` | 7 |
| Operations | `FR-OPS-001`–`006` | 6 |
| **Total** |  | **89** |

## 8. Authentication and identity requirements

### `FR-AUTH-001` — Authenticate access to protected capabilities

- **Priority:** `Must`
- **Rationale:** Every protected action must be attributable to an authenticated identity.
- **Actors:** Human user
- **Preconditions:**
  - Agent OS is reachable.
  - An approved identity mechanism is configured.
- **Required behavior:**
  1. Require authentication before displaying protected data or accepting protected commands.
  2. Create a bounded session after successful authentication.
  3. Associate the session with a stable user identity and identity type.
  4. Redirect or return an authorization-safe error for unauthenticated requests.
- **Failure behavior:**
  - Invalid credentials are rejected without revealing whether an account exists.
  - Identity-service failure does not enable anonymous fallback access.
- **Security / approval implications:** Authentication events are security-relevant and must not expose credentials or secret material.
- **Acceptance criteria:**
  - `FR-AUTH-001-AC-01` — Every protected route rejects unauthenticated access.
  - `FR-AUTH-001-AC-02` — A successful login creates an attributable session.
  - `FR-AUTH-001-AC-03` — A failed identity dependency leaves protected capabilities unavailable.
- **Traceability:** `PRD-IDN-001`, `PRD-IDN-005`, `UC-001`, `JRN-001`

### `FR-AUTH-002` — Enforce session expiry and reauthentication

- **Priority:** `Must`
- **Rationale:** Long-lived or abandoned sessions increase unauthorized-access risk.
- **Actors:** Human user
- **Preconditions:**
  - The user has an authenticated session.
- **Required behavior:**
  1. Track session creation, last activity, and expiry state.
  2. Invalidate an expired or revoked session before executing the next protected request.
  3. Preserve unsent client-side work where practical without treating it as persisted.
  4. Require reauthentication before continuing protected operations.
- **Failure behavior:**
  - Expired sessions return an explicit reauthentication-required state.
  - A session-store failure fails closed for protected actions.
- **Security / approval implications:** Session expiry and revocation must be auditable; security-sensitive values must not be logged.
- **Acceptance criteria:**
  - `FR-AUTH-002-AC-01` — Expired sessions cannot execute protected requests.
  - `FR-AUTH-002-AC-02` — Reauthentication restores only the permissions currently granted.
  - `FR-AUTH-002-AC-03` — Revoked permissions are not restored by reusing an older session.
- **Traceability:** `PRD-IDN-002`, `UC-001`

### `FR-AUTH-003` — Distinguish human, agent, worker, and integration identities

- **Priority:** `Must`
- **Rationale:** Authorization and audit decisions depend on who or what performed an action.
- **Actors:** Platform administrator, auditor
- **Preconditions:**
  - An identity is created or registered.
- **Required behavior:**
  1. Assign every identity a controlled identity type.
  2. Display identity type in relevant administration and audit views.
  3. Prevent workload identities from being represented as human approvers.
  4. Preserve identity type in events, runs, approvals, and tool receipts.
- **Failure behavior:**
  - Unknown identity type blocks privileged registration.
  - Legacy or malformed identities are quarantined or migrated explicitly.
- **Security / approval implications:** Only human identities with delegated authority may approve human-required actions.
- **Acceptance criteria:**
  - `FR-AUTH-003-AC-01` — Audit records identify identity and type.
  - `FR-AUTH-003-AC-02` — An agent identity cannot approve an approval request.
  - `FR-AUTH-003-AC-03` — Permission evaluation receives the identity type.
- **Traceability:** `PRD-IDN-003`, `PRD-IDN-004`, `PER-001`

### `FR-AUTH-004` — Display active identity and scope

- **Priority:** `Must`
- **Rationale:** Users must understand the organization and workspace in which an action will occur.
- **Actors:** All authenticated users
- **Preconditions:**
  - The user is authenticated.
  - The user has at least one authorized scope.
- **Required behavior:**
  1. Display the current user identity.
  2. Display the active organization and workspace in primary application views.
  3. Display the active project when a project-specific view is open.
  4. Require explicit scope selection when an action could otherwise be ambiguous.
- **Failure behavior:**
  - If the prior scope is no longer authorized, require a new valid selection.
  - If no scope is available, show an access-safe empty state.
- **Security / approval implications:** Scope changes must not broaden permissions and must not leak unauthorized scope names.
- **Acceptance criteria:**
  - `FR-AUTH-004-AC-01` — A user can correctly identify the active workspace from every protected operational view.
  - `FR-AUTH-004-AC-02` — Ambiguous actions cannot be submitted without scope resolution.
- **Traceability:** `PRD-IDN-008`, `PRD-UI-006`, `JRN-014`


## 9. Organization, workspace, project, and membership requirements

### `FR-WSP-001` — Create the first organization context

- **Priority:** `Must`
- **Rationale:** The MVP requires one durable organization boundary for all pilot work.
- **Actors:** Platform administrator, Product / Workspace Owner
- **Preconditions:**
  - The user is authenticated with organization-creation authority.
  - No organization context exists for the pilot.
- **Required behavior:**
  1. Collect organization name, purpose, and initial policy profile.
  2. Create a stable organization identifier.
  3. Assign the creating authorized user an initial administrative role.
  4. Persist the organization before displaying completion.
  5. Record an audit event.
- **Failure behavior:**
  - Validation or persistence failure creates no partial successful organization.
  - Duplicate submission is handled idempotently where practical.
- **Security / approval implications:** Organization creation is privileged and must not create public tenant onboarding.
- **Acceptance criteria:**
  - `FR-WSP-001-AC-01` — The organization survives service restart.
  - `FR-WSP-001-AC-02` — The initial administrative assignment is recorded.
  - `FR-WSP-001-AC-03` — Only one organization context is active in the MVP.
- **Traceability:** `PRD-WSP-001`, `JRN-001`, `UC-002`

### `FR-WSP-002` — Create and persist a workspace

- **Priority:** `Must`
- **Rationale:** A workspace is the primary boundary for membership, policy, data, tasks, runs, memory, artifacts, and cost.
- **Actors:** Workspace Owner
- **Preconditions:**
  - The organization exists.
  - The actor may create workspaces.
- **Required behavior:**
  1. Collect workspace name, purpose, classification, and policy profile.
  2. Create a stable workspace identifier.
  3. Assign the actor the Workspace Owner role.
  4. Persist the workspace and ownership before showing success.
  5. Create an auditable creation record.
- **Failure behavior:**
  - Invalid classification-policy combinations are rejected.
  - Persistence failure leaves no visible successful workspace.
- **Security / approval implications:** Workspace creation is authorization-controlled and must not expose other workspace metadata.
- **Acceptance criteria:**
  - `FR-WSP-002-AC-01` — At least two workspaces can be created.
  - `FR-WSP-002-AC-02` — Each workspace survives restart.
  - `FR-WSP-002-AC-03` — Creation appears in audit evidence.
- **Traceability:** `PRD-WSP-002`, `PRD-WSP-003`, `UC-003`, `JRN-002`

### `FR-WSP-003` — Create and manage projects inside a workspace

- **Priority:** `Must`
- **Rationale:** Projects organize goals and resources without replacing the workspace security boundary.
- **Actors:** Workspace Owner, Operator
- **Preconditions:**
  - The workspace exists.
  - The actor has project-management permission.
- **Required behavior:**
  1. Create a project with stable identifier, name, purpose, and lifecycle state.
  2. Associate the project with exactly one workspace.
  3. Allow authorized update and archival.
  4. Prevent a project from overriding workspace policy.
  5. Audit material changes.
- **Failure behavior:**
  - A project cannot be moved across workspaces in the MVP.
  - Unauthorized updates are denied safely.
- **Security / approval implications:** Project access inherits workspace authorization and may be further restricted later.
- **Acceptance criteria:**
  - `FR-WSP-003-AC-01` — Every project has one workspace.
  - `FR-WSP-003-AC-02` — Archived projects remain traceable.
  - `FR-WSP-003-AC-03` — Project changes are attributable.
- **Traceability:** `PRD-WSP-004`, `JRN-002`, `UC-004`

### `FR-WSP-004` — Enforce workspace isolation

- **Priority:** `Must`
- **Rationale:** Cross-workspace leakage would violate the central trust boundary.
- **Actors:** System, all users and workloads
- **Preconditions:**
  - Two or more workspaces exist.
- **Required behavior:**
  1. Evaluate workspace scope for every supported data and action path.
  2. Deny access to unauthorized workspace records, metadata, files, memory, artifacts, tools, costs, approvals, and audit data.
  3. Return a safe denial that does not disclose protected titles, paths, or identifiers.
  4. Record security-relevant denial evidence.
  5. Apply the rule to human, agent, worker, and integration identities.
- **Failure behavior:**
  - Authorization-service uncertainty fails closed.
  - Malformed or missing workspace scope blocks the request.
- **Security / approval implications:** Prompt content, adapter behavior, or tool output cannot override workspace authorization.
- **Acceptance criteria:**
  - `FR-WSP-004-AC-01` — Negative-access tests pass for every supported path.
  - `FR-WSP-004-AC-02` — Denied responses contain no protected metadata.
  - `FR-WSP-004-AC-03` — Cross-workspace requests are auditable without leaking target content.
- **Traceability:** `PRD-WSP-005`, `PRD-WSP-011`, `UC-027`, `JRN-014`

### `FR-WSP-005` — Manage workspace membership

- **Priority:** `Must`
- **Rationale:** Trusted-team use requires explicit membership rather than shared unrestricted access.
- **Actors:** Workspace Owner
- **Preconditions:**
  - The workspace exists.
  - The actor has membership-management authority.
  - The target identity exists or can be selected through the approved identity mechanism.
- **Required behavior:**
  1. Add a user to one workspace.
  2. Remove a user from one workspace.
  3. Show current members and status.
  4. Apply changes without affecting unrelated workspaces.
  5. Audit actor, target, previous state, and new state.
- **Failure behavior:**
  - Duplicate addition is handled safely.
  - Removal of the last required owner is blocked until ownership is transferred.
- **Security / approval implications:** Membership change may require stronger approval in later policies; it must always be attributable.
- **Acceptance criteria:**
  - `FR-WSP-005-AC-01` — Added users receive only the selected workspace.
  - `FR-WSP-005-AC-02` — Removed users lose future workspace access within the defined enforcement bound.
  - `FR-WSP-005-AC-03` — No unrelated workspace membership changes occur.
- **Traceability:** `PRD-WSP-006`, `PRD-WSP-009`, `JRN-019`, `UC-025`

### `FR-WSP-006` — Assign predefined workspace roles

- **Priority:** `Must`
- **Rationale:** The MVP needs a bounded role model without premature custom-role complexity.
- **Actors:** Workspace Owner
- **Preconditions:**
  - The target user is a workspace member.
- **Required behavior:**
  1. Support at least owner, operator, approver, auditor, and contributor roles.
  2. Display the effective capabilities of each role before assignment.
  3. Persist the assignment.
  4. Recompute authorization after changes.
  5. Audit assignment changes.
- **Failure behavior:**
  - Incompatible or unauthorized role assignments are blocked.
  - The last required owner cannot be demoted without transfer.
- **Security / approval implications:** Role assignment cannot grant secret access or global platform rights implicitly.
- **Acceptance criteria:**
  - `FR-WSP-006-AC-01` — Role changes affect future authorization.
  - `FR-WSP-006-AC-02` — Effective role is visible to the user.
  - `FR-WSP-006-AC-03` — Audit shows old and new role.
- **Traceability:** `PRD-WSP-007`, `PRD-WSP-008`, `UC-026`

### `FR-WSP-007` — Carry workspace scope on protected records

- **Priority:** `Must`
- **Rationale:** Isolation cannot be enforced consistently if records lack an explicit workspace association.
- **Actors:** System
- **Preconditions:**
  - A protected record is being created.
- **Required behavior:**
  1. Require workspace scope on tasks, runs, approvals, tool grants, memory, artifacts, cost events, and relevant audit events.
  2. Reject creation when required scope is missing.
  3. Prevent ordinary updates from changing workspace ownership.
  4. Include scope in authorization evaluation and trace correlation.
- **Failure behavior:**
  - Malformed or unknown workspace identifiers are rejected.
  - Migration exceptions must be explicit and auditable.
- **Security / approval implications:** Workspace scope is a protected field and cannot be changed by prompt or adapter output.
- **Acceptance criteria:**
  - `FR-WSP-007-AC-01` — Every protected MVP record has valid workspace scope.
  - `FR-WSP-007-AC-02` — Cross-workspace reassignment is unavailable in normal MVP behavior.
- **Traceability:** `PRD-WSP-011`, `PRD-XC-002`, `SCP-001`


## 10. Agent registry and adapter requirements

### `FR-AGT-001` — Register an agent adapter

- **Priority:** `Must`
- **Rationale:** Agent OS needs an explicit registry rather than implicit executable discovery.
- **Actors:** Technical Operator
- **Preconditions:**
  - The actor has adapter-management authority.
  - The adapter type is supported or registered through an approved internal mechanism.
- **Required behavior:**
  1. Collect adapter type, name, endpoint/executable reference, version information, and non-secret configuration.
  2. Store secret references separately from ordinary configuration.
  3. Create registration state before health validation.
  4. Record the configuring identity and timestamp.
- **Failure behavior:**
  - Invalid configuration is rejected.
  - Registration failure does not produce a healthy adapter card.
- **Security / approval implications:** Registration does not grant workspace, filesystem, network, or secret authority.
- **Acceptance criteria:**
  - `FR-AGT-001-AC-01` — The adapter appears as registered but not automatically validated.
  - `FR-AGT-001-AC-02` — Raw secret values are absent from ordinary storage.
  - `FR-AGT-001-AC-03` — Registration is auditable.
- **Traceability:** `PRD-AGT-001`, `PRD-AGT-004`, `UC-005`, `JRN-003`

### `FR-AGT-002` — Validate adapter reachability and health

- **Priority:** `Must`
- **Rationale:** Operators must distinguish configured, reachable, functional, degraded, and unknown states.
- **Actors:** Technical Operator, System
- **Preconditions:**
  - The adapter is registered.
- **Required behavior:**
  1. Perform a read-only reachability check.
  2. Perform a capability or diagnostic validation where supported.
  3. Store evidence, timestamp, and observed limitations.
  4. Expose registered, reachable, validated, degraded, failed, stale, and unknown states.
  5. Avoid claiming unsupported health certainty.
- **Failure behavior:**
  - Timeout, authentication failure, incompatible version, and unsupported diagnostics are distinct outcomes.
  - A stale result is not displayed as current health.
- **Security / approval implications:** Diagnostics must not execute consequential actions or expose secrets.
- **Acceptance criteria:**
  - `FR-AGT-002-AC-01` — Registration alone never yields validated status.
  - `FR-AGT-002-AC-02` — Health details identify the failing boundary where known.
  - `FR-AGT-002-AC-03` — Stale health is visibly labeled.
- **Traceability:** `PRD-AGT-004`, `PRD-AGT-005`, `JRN-016`, `UC-006`

### `FR-AGT-003` — Support Hermes adapter target

- **Priority:** `Must`
- **Rationale:** The MVP must prove a common platform contract across the first approved adapter target.
- **Actors:** Builder-Operator, Technical Operator
- **Preconditions:**
  - Hermes integration surface is available and permitted.
  - The common adapter contract is defined sufficiently for the implemented slice.
- **Required behavior:**
  1. Register Hermes through the agent registry.
  2. Expose supported capabilities and limitations.
  3. Execute approved bounded tasks through the common run model.
  4. Map Hermes-specific states to common states without hiding loss of fidelity.
  5. Retain adapter-specific diagnostic evidence.
- **Failure behavior:**
  - Unsupported cancellation, resume, usage, or artifact features are marked unavailable.
  - Hermes failure does not corrupt platform-side run history.
- **Security / approval implications:** Hermes cannot self-grant permissions or human approval authority.
- **Acceptance criteria:**
  - `FR-AGT-003-AC-01` — Hermes passes the required conformance subset.
  - `FR-AGT-003-AC-02` — A pilot task produces common run and artifact evidence.
  - `FR-AGT-003-AC-03` — Limitations are visible.
- **Traceability:** `PRD-AGT-002`, `PILOT-004`, `AGC-001`

### `FR-AGT-004` — Support Codex adapter target

- **Priority:** `Must`
- **Rationale:** The MVP must prove the same common platform concepts with a second adapter.
- **Actors:** Builder-Operator, Technical Operator
- **Preconditions:**
  - Codex integration surface is available and permitted.
  - The common adapter contract is defined sufficiently for the implemented slice.
- **Required behavior:**
  1. Register Codex through the agent registry.
  2. Expose supported capabilities and limitations.
  3. Execute approved bounded tasks through the common run model.
  4. Map Codex-specific states to common states without inventing unsupported certainty.
  5. Retain adapter-specific diagnostic evidence.
- **Failure behavior:**
  - Unsupported capabilities are marked unavailable.
  - Codex failure does not erase platform-side run history.
- **Security / approval implications:** Codex cannot autonomously commit, push, create PRs, merge, or expand permissions without applicable policy and approval.
- **Acceptance criteria:**
  - `FR-AGT-004-AC-01` — Codex passes the required conformance subset.
  - `FR-AGT-004-AC-02` — A pilot task produces common run and artifact evidence.
  - `FR-AGT-004-AC-03` — Limitations are visible.
- **Traceability:** `PRD-AGT-003`, `PILOT-004`, `AGC-001`

### `FR-AGT-005` — Expose declared adapter capabilities

- **Priority:** `Must`
- **Rationale:** Routing and user expectations depend on explicit capability declarations.
- **Actors:** Technical Operator, Builder-Operator
- **Preconditions:**
  - The adapter is registered.
- **Required behavior:**
  1. Store a versioned capability declaration.
  2. Show supported, unsupported, degraded, and unknown capabilities.
  3. Associate validation evidence where available.
  4. Prevent routing to a capability declared unavailable unless an explicit override policy exists.
  5. Preserve historical capability version on runs.
- **Failure behavior:**
  - Malformed declarations are rejected.
  - Unknown capability remains unknown rather than assumed supported.
- **Security / approval implications:** Capabilities describe technical ability, not authorization.
- **Acceptance criteria:**
  - `FR-AGT-005-AC-01` — Users can inspect capability state.
  - `FR-AGT-005-AC-02` — Runs record the capability version used.
  - `FR-AGT-005-AC-03` — Unavailable capability is not advertised as usable.
- **Traceability:** `PRD-AGT-007`, `CAP-001`, `JTBD-003`

### `FR-AGT-006` — Enable or disable adapters by workspace

- **Priority:** `Must`
- **Rationale:** An adapter may be acceptable in one workspace and prohibited in another.
- **Actors:** Workspace Owner, Technical Operator
- **Preconditions:**
  - The adapter is registered.
  - The actor has workspace configuration authority.
- **Required behavior:**
  1. Enable an adapter for selected workspace scope.
  2. Disable future use without deleting historical evidence.
  3. Display effective workspace enablement.
  4. Block task readiness or run preflight when the adapter is unavailable in the workspace.
  5. Audit configuration changes.
- **Failure behavior:**
  - Disabling an adapter with active runs triggers policy-defined pause, cancel, or warning behavior.
  - Unauthorized enablement is denied.
- **Security / approval implications:** Workspace enablement does not grant tool or data permissions automatically.
- **Acceptance criteria:**
  - `FR-AGT-006-AC-01` — Workspace A can use the adapter while Workspace B cannot.
  - `FR-AGT-006-AC-02` — Historical runs remain readable after disablement.
  - `FR-AGT-006-AC-03` — Future dispatch is blocked.
- **Traceability:** `PRD-AGT-006`, `PRD-AGT-011`, `JRN-003`


## 11. Model profile and provider requirements

### `FR-MOD-001` — Create a provider-neutral model profile

- **Priority:** `Must`
- **Rationale:** Core workflows should depend on capability and policy profiles, not hard-coded provider model names.
- **Actors:** Technical Operator
- **Preconditions:**
  - At least one provider adapter or direct provider integration is configured.
- **Required behavior:**
  1. Collect logical profile name, provider, provider model identifier, intended capabilities, constraints, and validation state.
  2. Associate profile with organization and allowed workspaces.
  3. Store secret references without raw secret values.
  4. Persist the profile before validation.
  5. Audit creation and material changes.
- **Failure behavior:**
  - Invalid provider/model identifiers are reported without exposing credentials.
  - Unvalidated profiles remain visibly unvalidated.
- **Security / approval implications:** Profile creation does not authorize prohibited data classes or exceed provider policy.
- **Acceptance criteria:**
  - `FR-MOD-001-AC-01` — Tasks can reference a logical profile.
  - `FR-MOD-001-AC-02` — Profile inspection shows provider-specific details without leaking secrets.
  - `FR-MOD-001-AC-03` — Validation state is separate from configuration state.
- **Traceability:** `PRD-MOD-001`, `PRD-MOD-002`, `JRN-004`, `UC-007`

### `FR-MOD-002` — Validate model profile availability

- **Priority:** `Must`
- **Rationale:** Configuration alone does not prove that a model can be used.
- **Actors:** Technical Operator, System
- **Preconditions:**
  - The profile exists.
  - Required provider secret reference is available.
- **Required behavior:**
  1. Perform a safe validation request when enabled.
  2. Record result, timestamp, latency where available, and limitations.
  3. Mark profile validated, failed, stale, or unknown.
  4. Avoid sending prohibited workspace content during validation.
- **Failure behavior:**
  - Authentication, model-not-found, quota, network, and policy failures are distinct.
  - Provider usage data unavailability does not imply model unavailability.
- **Security / approval implications:** Validation must use minimal non-sensitive content.
- **Acceptance criteria:**
  - `FR-MOD-002-AC-01` — Failed validation does not appear ready.
  - `FR-MOD-002-AC-02` — Stale validation is labeled.
  - `FR-MOD-002-AC-03` — Validation evidence is auditable.
- **Traceability:** `PRD-MOD-006`, `JRN-004`

### `FR-MOD-003` — Enable model profiles by workspace

- **Priority:** `Must`
- **Rationale:** Provider terms, data classes, and budgets may differ by workspace.
- **Actors:** Workspace Owner, Technical Operator
- **Preconditions:**
  - The model profile exists.
- **Required behavior:**
  1. Enable or disable the profile for selected workspaces.
  2. Display effective policy and validation state.
  3. Block use in unauthorized workspaces.
  4. Audit changes.
- **Failure behavior:**
  - Disabling a profile with active runs triggers a policy-defined state.
  - Unauthorized changes are denied.
- **Security / approval implications:** Workspace enablement must not override data-class or provider-policy restrictions.
- **Acceptance criteria:**
  - `FR-MOD-003-AC-01` — Workspace-specific availability is enforced.
  - `FR-MOD-003-AC-02` — Historical run attribution remains intact after disablement.
- **Traceability:** `PRD-MOD-003`, `JRN-004`

### `FR-MOD-004` — Apply model budget and usage limits

- **Priority:** `Must`
- **Rationale:** Bounded delegation requires enforceable spend and usage controls.
- **Actors:** Workspace Owner, Builder-Operator, System
- **Preconditions:**
  - A workspace and task/run exist.
  - Applicable budget policy exists.
- **Required behavior:**
  1. Evaluate workspace and task/run limits during preflight.
  2. Record the applicable limit snapshot on the run.
  3. Block start when the requested action exceeds hard limits.
  4. Warn or stop according to policy when runtime thresholds are reached.
  5. Expose remaining or unavailable budget information honestly.
- **Failure behavior:**
  - Missing or delayed usage data produces unknown/pending state, not false remaining balance.
  - Limit-evaluation failure fails closed for hard-budget actions.
- **Security / approval implications:** Budget changes and overrides are privileged and auditable.
- **Acceptance criteria:**
  - `FR-MOD-004-AC-01` — Runs over a hard preflight limit do not dispatch.
  - `FR-MOD-004-AC-02` — Threshold events are attributable.
  - `FR-MOD-004-AC-03` — Unknown cost state is not displayed as zero.
- **Traceability:** `PRD-MOD-004`, `PRD-CST-006`, `JTBD-009`

### `FR-MOD-005` — Record actual provider and model used

- **Priority:** `Must`
- **Rationale:** Users and auditors need to know the actual execution implementation.
- **Actors:** System, Builder-Operator, Auditor
- **Preconditions:**
  - A run has been dispatched to an adapter/provider.
- **Required behavior:**
  1. Record requested logical profile.
  2. Record actual provider and model identifier where reported.
  3. Record fallback or substitution when explicitly configured.
  4. Mark unknown when actual model cannot be verified.
  5. Expose the information in run and audit views.
- **Failure behavior:**
  - Conflicting provider reports are retained and flagged.
  - Missing actual-model data is not filled with the configured model automatically.
- **Security / approval implications:** Provider/model identifiers may be access-restricted but cannot be silently falsified.
- **Acceptance criteria:**
  - `FR-MOD-005-AC-01` — Run detail distinguishes requested profile from actual model.
  - `FR-MOD-005-AC-02` — Fallback is visible.
  - `FR-MOD-005-AC-03` — Unknown remains explicit.
- **Traceability:** `PRD-MOD-005`, `PRD-MOD-007`, `JTBD-003`


## 12. Task requirements

### `FR-TSK-001` — Create a draft task

- **Priority:** `Must`
- **Rationale:** Users need a durable place to define bounded work before execution.
- **Actors:** Builder-Operator
- **Preconditions:**
  - The actor has task-creation permission in the workspace.
- **Required behavior:**
  1. Create a task with stable identifier, workspace, optional project, title, desired outcome, and draft state.
  2. Persist partial valid task content.
  3. Record creator and timestamps.
  4. Allow authorized editing before readiness.
  5. Audit creation.
- **Failure behavior:**
  - Persistence failure does not show a successful task.
  - Unauthorized workspace selection is denied safely.
- **Security / approval implications:** Task free text cannot grant permissions.
- **Acceptance criteria:**
  - `FR-TSK-001-AC-01` — The draft survives refresh and restart.
  - `FR-TSK-001-AC-02` — The task is scoped to one workspace.
  - `FR-TSK-001-AC-03` — Creator attribution is visible.
- **Traceability:** `PRD-RUN-001`, `JRN-005`, `UC-008`

### `FR-TSK-002` — Define bounded task scope and limits

- **Priority:** `Must`
- **Rationale:** A task must state what an agent may do and when it must stop.
- **Actors:** Builder-Operator
- **Preconditions:**
  - A draft task exists.
- **Required behavior:**
  1. Capture desired outcome, permitted resources, data classification, agent/routing preference, model profile, tool scopes, time limit, cost limit, retry limit, and expected artifacts.
  2. Display a human-readable boundary summary.
  3. Validate resource references against workspace authorization.
  4. Persist the applicable policy context.
- **Failure behavior:**
  - Prohibited resource or data request is rejected.
  - Missing mandatory limits keep the task in draft or blocked state.
- **Security / approval implications:** Permissions come from policy and grants, not the task narrative.
- **Acceptance criteria:**
  - `FR-TSK-002-AC-01` — A ready task has all mandatory scope fields.
  - `FR-TSK-002-AC-02` — The boundary summary matches stored values.
  - `FR-TSK-002-AC-03` — Out-of-scope resources cannot be added.
- **Traceability:** `PRD-RUN-002`, `JTBD-002`, `JRN-005`

### `FR-TSK-003` — Manage task lifecycle states

- **Priority:** `Must`
- **Rationale:** Users and automation need controlled task status semantics.
- **Actors:** Builder-Operator, System
- **Preconditions:**
  - A task exists.
- **Required behavior:**
  1. Support draft, ready, blocked, active, completed, cancelled, and archived states.
  2. Define allowed transitions.
  3. Record transition actor, time, and reason where applicable.
  4. Prevent completed or archived state from erasing run history.
  5. Expose current and prior state.
- **Failure behavior:**
  - Invalid transition is rejected.
  - Concurrent transition conflict is surfaced.
- **Security / approval implications:** Privileged transitions may require role or policy checks.
- **Acceptance criteria:**
  - `FR-TSK-003-AC-01` — Only allowed transitions succeed.
  - `FR-TSK-003-AC-02` — Every transition is auditable.
  - `FR-TSK-003-AC-03` — State survives restart.
- **Traceability:** `PRD-RUN-003`, `UCD-001`

### `FR-TSK-004` — Validate task readiness

- **Priority:** `Must`
- **Rationale:** Execution should not start from an ambiguous or unauthorized task.
- **Actors:** System, Builder-Operator
- **Preconditions:**
  - A draft or blocked task exists.
- **Required behavior:**
  1. Check mandatory fields, workspace policy, selected adapter/model availability, tool permissions, limits, data classification, and expected approval classes.
  2. Return actionable validation findings.
  3. Move the task to ready only when all blocking conditions pass.
  4. Preserve warnings separately from blockers.
- **Failure behavior:**
  - Validation dependency failure yields blocked or unknown validation state.
  - No external execution occurs during readiness validation.
- **Security / approval implications:** Validation must not access unauthorized resources.
- **Acceptance criteria:**
  - `FR-TSK-004-AC-01` — A task cannot become ready with unresolved blockers.
  - `FR-TSK-004-AC-02` — Findings identify the field or policy causing the block.
  - `FR-TSK-004-AC-03` — Validation result is timestamped.
- **Traceability:** `PRD-RUN-002`, `PRD-RUN-007`, `JRN-005`

### `FR-TSK-005` — Version or audit material task changes

- **Priority:** `Must`
- **Rationale:** A run and approval must remain linked to the exact task definition used.
- **Actors:** Builder-Operator, System
- **Preconditions:**
  - A task exists.
- **Required behavior:**
  1. Identify material changes to outcome, resources, limits, agent/model, data class, tools, or expected artifacts.
  2. Record before/after values or a versioned snapshot.
  3. Invalidate readiness or pending approvals when required.
  4. Ensure each run links to the task snapshot used.
- **Failure behavior:**
  - Concurrent edits are rejected or reconciled explicitly.
  - Change-record failure prevents silent material update.
- **Security / approval implications:** Material scope expansion may require new approval.
- **Acceptance criteria:**
  - `FR-TSK-005-AC-01` — Runs retain the original task snapshot.
  - `FR-TSK-005-AC-02` — Material changes are auditable.
  - `FR-TSK-005-AC-03` — Changed scope cannot reuse stale approval.
- **Traceability:** `PRD-RUN-002`, `PRD-APR-005`, `UC-014`

### `FR-TSK-006` — Archive a task without deleting evidence

- **Priority:** `Should`
- **Rationale:** Completed or abandoned work should leave the active view while remaining traceable.
- **Actors:** Builder-Operator, Workspace Owner
- **Preconditions:**
  - The task exists.
  - The actor has archival authority.
- **Required behavior:**
  1. Move the task to archived state.
  2. Retain linked runs, approvals, artifacts, costs, and audit evidence.
  3. Remove it from default active lists.
  4. Allow authorized retrieval through filters.
- **Failure behavior:**
  - Active runs block archival or require explicit cancellation policy.
  - Unauthorized archival is denied.
- **Security / approval implications:** Archive is not deletion and must not bypass retention rules.
- **Acceptance criteria:**
  - `FR-TSK-006-AC-01` — Archived task is absent from default active view.
  - `FR-TSK-006-AC-02` — Historical evidence remains accessible.
  - `FR-TSK-006-AC-03` — Archive event is recorded.
- **Traceability:** `PRD-RUN-003`, `JTBD-001`


## 13. Run execution and recovery requirements

### `FR-RUN-001` — Create a persisted run before dispatch

- **Priority:** `Must`
- **Rationale:** External work must never begin without a durable platform record.
- **Actors:** Builder-Operator, System
- **Preconditions:**
  - The task is ready.
  - Preflight is requested.
- **Required behavior:**
  1. Create a stable run identifier.
  2. Persist task snapshot, workspace, project, requested adapter, model profile, limits, and initial state.
  3. Commit the run record before any external dispatch.
  4. Record creation event.
  5. Return the run identifier to the caller.
- **Failure behavior:**
  - Persistence failure prevents dispatch.
  - Duplicate start requests are idempotent or explicitly create separate runs with confirmation.
- **Security / approval implications:** Run creation requires authorization and applicable policy evaluation.
- **Acceptance criteria:**
  - `FR-RUN-001-AC-01` — Every external dispatch has a prior persisted run.
  - `FR-RUN-001-AC-02` — A failed persistence attempt produces no dispatch.
  - `FR-RUN-001-AC-03` — Run survives refresh and restart.
- **Traceability:** `PRD-RUN-004`, `UC-009`, `OBJ-001`

### `FR-RUN-002` — Perform run preflight

- **Priority:** `Must`
- **Rationale:** A run should dispatch only when all required boundaries are satisfied.
- **Actors:** System
- **Preconditions:**
  - A persisted run exists in a pre-dispatch state.
- **Required behavior:**
  1. Evaluate user/workload authority, workspace policy, task readiness, adapter health, model profile, data class, tools, network scope, budget, and prerequisite approvals.
  2. Store the preflight decision and policy inputs.
  3. Block dispatch on any hard failure.
  4. Expose warnings and blockers to the user.
- **Failure behavior:**
  - Policy-evaluation failure fails closed.
  - Stale adapter/model health may block according to policy.
- **Security / approval implications:** Preflight evidence is security-relevant and must not expose secrets.
- **Acceptance criteria:**
  - `FR-RUN-002-AC-01` — Blocked preflight produces no external execution.
  - `FR-RUN-002-AC-02` — User sees actionable blocker details.
  - `FR-RUN-002-AC-03` — Decision is auditable.
- **Traceability:** `PRD-RUN-007`, `JRN-006`

### `FR-RUN-003` — Dispatch a bounded execution request

- **Priority:** `Must`
- **Rationale:** The adapter must receive explicit limits and scope.
- **Actors:** System, Agent adapter
- **Preconditions:**
  - Run preflight passes.
  - The selected adapter is enabled.
- **Required behavior:**
  1. Create an adapter request containing run identity, capability, bounded task context, permitted resources, limits, and correlation information.
  2. Send only policy-approved context.
  3. Record dispatch time and adapter acknowledgement where available.
  4. Transition run to starting or running based on evidence.
- **Failure behavior:**
  - Dispatch timeout or rejection produces explicit failure or unknown state.
  - No automatic unconfigured fallback occurs.
- **Security / approval implications:** The request must not include raw secrets except through approved secure mechanisms.
- **Acceptance criteria:**
  - `FR-RUN-003-AC-01` — Adapter receives a bounded request.
  - `FR-RUN-003-AC-02` — Dispatch evidence is linked to the run.
  - `FR-RUN-003-AC-03` — Unapproved context is excluded.
- **Traceability:** `PRD-RUN-005`, `AGC-001`, `JRN-006`

### `FR-RUN-004` — Persist run steps and events

- **Priority:** `Must`
- **Rationale:** Users need durable progress and an auditable execution timeline.
- **Actors:** System, Agent adapter, Tool gateway
- **Preconditions:**
  - A run exists.
- **Required behavior:**
  1. Create stable step identifiers.
  2. Persist step type, state, timestamps, producer, inputs/outputs references, and correlation.
  3. Apply ordered or causally linked event processing.
  4. Retain duplicate-detection information.
  5. Expose the timeline in authorized views.
- **Failure behavior:**
  - Malformed events are rejected or quarantined.
  - Out-of-order events are reconciled without inventing success.
- **Security / approval implications:** Sensitive fields are redacted or stored according to classification policy.
- **Acceptance criteria:**
  - `FR-RUN-004-AC-01` — Accepted steps survive restart.
  - `FR-RUN-004-AC-02` — Timeline links to the correct run.
  - `FR-RUN-004-AC-03` — Duplicate events do not create duplicate effects.
- **Traceability:** `PRD-RUN-005`, `PRD-AUD-001`, `RUN-001`

### `FR-RUN-005` — Represent run states explicitly

- **Priority:** `Must`
- **Rationale:** Operational decisions depend on accurate and nuanced state.
- **Actors:** All authorized users
- **Preconditions:**
  - A run exists.
- **Required behavior:**
  1. Support queued, starting, running, waiting-for-approval, waiting-for-resource, paused, retrying, failed, cancelled, completed, stale, and unknown.
  2. Define allowed transitions.
  3. Store state reason and evidence reference.
  4. Propagate state to Mission Control and task summaries.
  5. Never convert missing evidence to completed.
- **Failure behavior:**
  - Conflicting state reports produce an explicit conflict/unknown condition.
  - Invalid transition is rejected or investigated.
- **Security / approval implications:** State transitions are auditable and permission-aware.
- **Acceptance criteria:**
  - `FR-RUN-005-AC-01` — Users can distinguish every required state.
  - `FR-RUN-005-AC-02` — Zero, failed, stale, and unknown are not conflated.
  - `FR-RUN-005-AC-03` — State survives restart.
- **Traceability:** `PRD-RUN-006`, `PRD-RUN-013`, `UCD-001`

### `FR-RUN-006` — Cancel a run

- **Priority:** `Must`
- **Rationale:** Users must be able to revoke future work while preserving truthful evidence.
- **Actors:** Builder-Operator, Workspace Owner
- **Preconditions:**
  - The run is non-terminal.
  - The actor has cancellation authority.
- **Required behavior:**
  1. Record cancellation intent durably.
  2. Stop pending dispatches.
  3. Request adapter/tool cancellation where supported.
  4. Invalidate or cancel related pending approvals as policy requires.
  5. Record known completed side effects.
  6. Set final state to cancelled, failed, or unknown based on evidence.
- **Failure behavior:**
  - Adapter non-response leaves explicit unknown state.
  - Cancellation does not erase prior events.
- **Security / approval implications:** Cancellation authority is scoped; completed consequential effects are not silently reversed.
- **Acceptance criteria:**
  - `FR-RUN-006-AC-01` — No new enforceable step begins after cancellation.
  - `FR-RUN-006-AC-02` — Completed effects remain visible.
  - `FR-RUN-006-AC-03` — Uncertainty is shown.
- **Traceability:** `PRD-RUN-008`, `UC-015`, `JRN-017`

### `FR-RUN-007` — Retry an eligible step

- **Priority:** `Must`
- **Rationale:** Transient failures should be recoverable without uncontrolled duplication.
- **Actors:** Builder-Operator, System
- **Preconditions:**
  - A failed or retryable step exists.
  - Retry count and policy permit another attempt.
- **Required behavior:**
  1. Evaluate retry eligibility, idempotency protection, budget, adapter health, permissions, and approval validity.
  2. Create a new attempt linked to the original step.
  3. Increment retry count.
  4. Prevent reuse of invalid approval.
  5. Record result and lineage.
- **Failure behavior:**
  - Unsafe or unknown side-effect state blocks retry.
  - Retry-limit exhaustion produces terminal or review-required state.
- **Security / approval implications:** Consequential retry may require renewed approval.
- **Acceptance criteria:**
  - `FR-RUN-007-AC-01` — Retry never overwrites original attempt.
  - `FR-RUN-007-AC-02` — Duplicate protected side effects are prevented.
  - `FR-RUN-007-AC-03` — Retry lineage is visible.
- **Traceability:** `PRD-RUN-009`, `PRD-RUN-011`, `UC-016`

### `FR-RUN-008` — Detect interrupted or stale execution

- **Priority:** `Must`
- **Rationale:** The system must identify lost contact without pretending to know the outcome.
- **Actors:** System, Technical Operator
- **Preconditions:**
  - A running or starting run exists.
- **Required behavior:**
  1. Evaluate heartbeat, event recency, adapter status, and worker status.
  2. Mark state stale or unknown when evidence exceeds the configured threshold or conflicts.
  3. Record last known reliable step and time.
  4. Offer diagnostic and recovery options.
- **Failure behavior:**
  - Monitoring failure yields unknown monitoring state.
  - The system does not mark failed or completed without supporting evidence.
- **Security / approval implications:** Thresholds and diagnostic access are controlled and auditable.
- **Acceptance criteria:**
  - `FR-RUN-008-AC-01` — A stopped adapter leads to stale/unknown detection.
  - `FR-RUN-008-AC-02` — Last reliable state is visible.
  - `FR-RUN-008-AC-03` — Mission Control propagates uncertainty.
- **Traceability:** `PRD-RUN-010`, `UC-035`, `JRN-009`

### `FR-RUN-009` — Resume a supported interrupted run

- **Priority:** `Must`
- **Rationale:** Approved interruption scenarios should continue safely when evidence permits.
- **Actors:** Builder-Operator, Technical Operator
- **Preconditions:**
  - Run is interrupted.
  - Checkpoint or safe continuation is available.
  - Policy, budget, resource, and approval checks pass.
- **Required behavior:**
  1. Display checkpoint, last side effect, and resume limitations.
  2. Revalidate current authorization and resource state.
  3. Create a resume attempt linked to the original run.
  4. Continue from the defined checkpoint.
  5. Preserve lineage and update execution receipt.
- **Failure behavior:**
  - Corrupt checkpoint, unknown side effect, expired approval, or changed resource blocks resume.
  - Unsupported adapter resume offers safe retry/restart/terminate alternatives.
- **Security / approval implications:** Resume of a consequential action requires exact valid authority.
- **Acceptance criteria:**
  - `FR-RUN-009-AC-01` — Approved recovery scenarios resume without duplicate effect.
  - `FR-RUN-009-AC-02` — Blocked resume explains the unsafe condition.
  - `FR-RUN-009-AC-03` — Lineage remains one coherent run history.
- **Traceability:** `PRD-RUN-010`, `PRD-RUN-012`, `UC-017`, `JRN-009`

### `FR-RUN-010` — Generate a run execution receipt

- **Priority:** `Must`
- **Rationale:** Accepted runs need a concise evidence object supporting review and audit.
- **Actors:** System, Builder-Operator, Auditor
- **Preconditions:**
  - A run reaches terminal or significant waiting state.
- **Required behavior:**
  1. Generate a receipt containing run/task/workspace identity, adapter/model, policy and approval references, step summary, artifacts, known side effects, usage/cost references, state, timestamps, and evidence gaps.
  2. Version the receipt schema.
  3. Retain the receipt with the run.
  4. Expose authorized human-readable and machine-readable forms.
- **Failure behavior:**
  - Incomplete evidence is marked incomplete.
  - Receipt-generation failure is visible and does not change run outcome.
- **Security / approval implications:** Receipts must redact or reference secrets safely.
- **Acceptance criteria:**
  - `FR-RUN-010-AC-01` — Every accepted pilot run has required receipt fields.
  - `FR-RUN-010-AC-02` — Receipt matches underlying records.
  - `FR-RUN-010-AC-03` — Missing fields are explicit.
- **Traceability:** `PRD-RUN-014`, `PRD-AUD-010`, `JTBD-011`


## 14. Approval requirements

### `FR-APR-001` — Classify proposed actions by side effect and approval policy

- **Priority:** `Must`
- **Rationale:** The platform cannot enforce human control without a consistent action classification.
- **Actors:** System, Security/Policy Owner
- **Preconditions:**
  - A run or user proposes an action.
- **Required behavior:**
  1. Identify capability, target, resource scope, reversibility, data class, external visibility, financial/production impact, and permission expansion.
  2. Apply the active policy version.
  3. Return allowed, denied, approval-required, or unknown.
  4. Store decision inputs and reason.
- **Failure behavior:**
  - Unknown or failed classification defaults to deny or review according to security policy.
  - Unrecognized action types do not execute.
- **Security / approval implications:** The policy engine, not prompt content, is authoritative.
- **Acceptance criteria:**
  - `FR-APR-001-AC-01` — Every protected action receives a policy decision.
  - `FR-APR-001-AC-02` — Approval-required classes are blocked before execution.
  - `FR-APR-001-AC-03` — Decision is auditable.
- **Traceability:** `PRD-APR-001`, `AUT-001`, `SCP-001`

### `FR-APR-002` — Create an exact approval request

- **Priority:** `Must`
- **Rationale:** Approvers need the exact proposal rather than a vague permission grant.
- **Actors:** System, Run
- **Preconditions:**
  - Policy returns approval-required.
  - No valid approval exists.
- **Required behavior:**
  1. Create stable request identity.
  2. Store requester, workspace, task, run, step, exact action, parameters, target, risk, policy reason, preview/diff reference, expiry, expected effects, and required approver scope.
  3. Transition run to waiting-for-approval.
  4. Add request to authorized approval inbox.
- **Failure behavior:**
  - Missing exact parameters blocks request creation and action execution.
  - Request persistence failure keeps the action blocked.
- **Security / approval implications:** Request content must not reveal secrets beyond approver authorization.
- **Acceptance criteria:**
  - `FR-APR-002-AC-01` — The action cannot execute before request creation and approval.
  - `FR-APR-002-AC-02` — Request is bound to exact action hash/version.
  - `FR-APR-002-AC-03` — Authorized approvers can find it.
- **Traceability:** `PRD-APR-002`, `PRD-APR-003`, `UC-011`, `JRN-007`

### `FR-APR-003` — Review an approval request

- **Priority:** `Must`
- **Rationale:** A human must be able to make an informed decision efficiently.
- **Actors:** Reviewer / Approver
- **Preconditions:**
  - The approver is authenticated and authorized for the request.
- **Required behavior:**
  1. Display plain-language summary and exact technical parameters.
  2. Display target, risk, policy reason, expected effects, cost impact where relevant, expiry, and preview/diff.
  3. Display related prior requests and changes where relevant.
  4. Provide approve, reject, and request-revision actions.
- **Failure behavior:**
  - Unauthorized review is denied.
  - Unavailable preview is labeled rather than hidden.
- **Security / approval implications:** Sensitive details are disclosed only to authorized approvers.
- **Acceptance criteria:**
  - `FR-APR-003-AC-01` — Approver can identify target and side effect.
  - `FR-APR-003-AC-02` — Keyboard and assistive-technology operation is possible.
  - `FR-APR-003-AC-03` — Missing evidence is visible.
- **Traceability:** `PRD-APR-011`, `PRD-APR-012`, `JRN-007`, `UCD-001`

### `FR-APR-004` — Approve an exact action

- **Priority:** `Must`
- **Rationale:** Approval must authorize one reviewed action under current policy.
- **Actors:** Reviewer / Approver
- **Preconditions:**
  - Request is valid, unexpired, and under the approver's delegated authority.
- **Required behavior:**
  1. Record the approver decision, time, request version, and optional rationale.
  2. Revalidate approver authority and current policy.
  3. Verify action parameters and target have not materially changed.
  4. Mark approval available for one exact consumption.
  5. Notify the waiting run.
- **Failure behavior:**
  - Expired, changed, unauthorized, or cancelled request cannot be approved.
  - Decision persistence failure leaves action blocked.
- **Security / approval implications:** Human-required approval cannot be provided by an agent/workload identity.
- **Acceptance criteria:**
  - `FR-APR-004-AC-01` — Approved action hash matches execution action.
  - `FR-APR-004-AC-02` — Material change requires new request.
  - `FR-APR-004-AC-03` — Decision is durable and attributable.
- **Traceability:** `PRD-APR-005`, `PRD-APR-006`, `UC-012`

### `FR-APR-005` — Reject or request revision

- **Priority:** `Must`
- **Rationale:** Governance must support refusal and correction without side effects.
- **Actors:** Reviewer / Approver
- **Preconditions:**
  - The request is valid and reviewable.
- **Required behavior:**
  1. Allow rejection with reason.
  2. Allow revision request with reason and requested change.
  3. Keep the proposed action blocked.
  4. Notify the requester.
  5. Invalidate the old request when a materially revised proposal is created.
- **Failure behavior:**
  - A rejected request cannot later be consumed.
  - Failure to record the decision keeps the action blocked.
- **Security / approval implications:** Rejection reason follows access and retention policy.
- **Acceptance criteria:**
  - `FR-APR-005-AC-01` — Rejected request remains blocked.
  - `FR-APR-005-AC-02` — Revision creates a new request identity.
  - `FR-APR-005-AC-03` — Reasons are visible to authorized participants.
- **Traceability:** `PRD-APR-004`, `PRD-APR-009`, `UC-013`, `UC-014`, `JRN-008`

### `FR-APR-006` — Expire and invalidate approval requests

- **Priority:** `Must`
- **Rationale:** Approval should not grant indefinite authority.
- **Actors:** System
- **Preconditions:**
  - A request has an expiry or invalidation trigger.
- **Required behavior:**
  1. Mark the request expired when its time bound passes.
  2. Invalidate when action parameters, target, policy, authority, or relevant resource changes materially.
  3. Keep the action blocked.
  4. Notify relevant users.
  5. Record the event.
- **Failure behavior:**
  - Expiry-processing failure must not permit execution.
  - Ambiguous invalidation state fails closed.
- **Security / approval implications:** Expiry and invalidation are security controls.
- **Acceptance criteria:**
  - `FR-APR-006-AC-01` — Expired request cannot be consumed.
  - `FR-APR-006-AC-02` — Waiting run remains blocked or transitions according to policy.
  - `FR-APR-006-AC-03` — New approval is required.
- **Traceability:** `PRD-APR-008`, `UC-034`

### `FR-APR-007` — Consume approval exactly once

- **Priority:** `Must`
- **Rationale:** Replay or double consumption could authorize duplicate side effects.
- **Actors:** System
- **Preconditions:**
  - A valid approval exists for the exact action.
- **Required behavior:**
  1. Atomically verify request, approval, action hash, target, expiry, policy, and consumption state.
  2. Mark approval consumed.
  3. Link the resulting execution attempt.
  4. Reject later consumption attempts.
  5. Preserve outcome even when the action subsequently fails.
- **Failure behavior:**
  - Concurrent consumption permits at most one accepted attempt.
  - Storage failure prevents action dispatch.
- **Security / approval implications:** Consumption is a security-critical transaction.
- **Acceptance criteria:**
  - `FR-APR-007-AC-01` — Replay test is denied.
  - `FR-APR-007-AC-02` — One approval maps to one authorized execution attempt unless policy explicitly defines otherwise.
  - `FR-APR-007-AC-03` — Failure after approval remains failure.
- **Traceability:** `PRD-APR-007`, `UC-012`

### `FR-APR-008` — Revoke future authority

- **Priority:** `Must`
- **Rationale:** Users need a direct way to stop future use of a permission, adapter, tool, or grant.
- **Actors:** Workspace Owner, Authorized administrator
- **Preconditions:**
  - The actor has revocation authority.
- **Required behavior:**
  1. Select the grant, role, adapter, tool, secret reference, or policy authority.
  2. Identify affected active runs and requests.
  3. Confirm revocation.
  4. Block future use within the defined enforcement bound.
  5. Pause, cancel, or mark affected active work according to policy.
  6. Audit the revocation.
- **Failure behavior:**
  - Revocation uncertainty fails closed for new protected actions.
  - Prompt text cannot restore revoked authority.
- **Security / approval implications:** Revocation must preserve historical evidence while preventing future authorization.
- **Acceptance criteria:**
  - `FR-APR-008-AC-01` — Future invocation is denied.
  - `FR-APR-008-AC-02` — Affected active runs are visible.
  - `FR-APR-008-AC-03` — Revocation is attributable.
- **Traceability:** `PRD-APR-010`, `UC-033`


## 15. Tool and integration requirements

### `FR-TOL-001` — Register a tool or integration capability

- **Priority:** `Must`
- **Rationale:** Tools must be explicit governed capabilities rather than hidden agent behaviors.
- **Actors:** Technical Operator
- **Preconditions:**
  - The actor has integration-management authority.
- **Required behavior:**
  1. Register tool identity, type, version, endpoint/executable reference, declared capabilities, side-effect classes, and non-secret configuration.
  2. Store secret references separately.
  3. Set registration state distinct from validation.
  4. Audit changes.
- **Failure behavior:**
  - Invalid or unsupported registration is rejected.
  - Registration does not imply workspace enablement.
- **Security / approval implications:** Registration grants no authority by itself.
- **Acceptance criteria:**
  - `FR-TOL-001-AC-01` — Tool appears in registry with explicit state.
  - `FR-TOL-001-AC-02` — Secret values are not stored in ordinary fields.
  - `FR-TOL-001-AC-03` — Capabilities and risks are inspectable.
- **Traceability:** `PRD-TOL-001`, `JTBD-010`

### `FR-TOL-002` — Enable tools by workspace and scope

- **Priority:** `Must`
- **Rationale:** A tool may be safe only for a bounded workspace resource set.
- **Actors:** Workspace Owner, Technical Operator
- **Preconditions:**
  - The tool is registered.
- **Required behavior:**
  1. Enable selected capabilities for one workspace.
  2. Define resource, path, network, data-class, time, and cost scope.
  3. Display effective grant and expiry.
  4. Allow disablement/revocation.
  5. Audit grant changes.
- **Failure behavior:**
  - Invalid or broader-than-authorized scope is rejected.
  - Disabling with active work triggers policy-defined handling.
- **Security / approval implications:** Workspace enablement is subordinate to global security policy.
- **Acceptance criteria:**
  - `FR-TOL-002-AC-01` — Workspace A and B can have different grants.
  - `FR-TOL-002-AC-02` — Future invocation respects revocation.
  - `FR-TOL-002-AC-03` — Grant is not inferred from task text.
- **Traceability:** `PRD-TOL-004`, `PRD-TOL-009`, `JRN-003`

### `FR-TOL-003` — Evaluate tool invocation policy

- **Priority:** `Must`
- **Rationale:** Each invocation can carry different risk and target.
- **Actors:** System, Tool gateway
- **Preconditions:**
  - A run or user requests a tool capability.
- **Required behavior:**
  1. Evaluate identity, workspace, capability, target, resource scope, data class, network destination, side effect, cost, grant expiry, and approval.
  2. Return allowed, denied, approval-required, or unknown.
  3. Persist the policy decision.
  4. Block execution until allowed.
- **Failure behavior:**
  - Policy failure or unknown action fails closed.
  - Denied response avoids protected metadata leakage.
- **Security / approval implications:** MCP connection, tool installation, or agent capability does not bypass authorization.
- **Acceptance criteria:**
  - `FR-TOL-003-AC-01` — Unauthorized invocation never reaches the tool.
  - `FR-TOL-003-AC-02` — Decision evidence is linked to the run/step.
  - `FR-TOL-003-AC-03` — Prompt attempts to broaden scope fail.
- **Traceability:** `PRD-TOL-002`, `PRD-TOL-003`, `PRD-TOL-010`

### `FR-TOL-004` — Enforce bounded filesystem and repository access

- **Priority:** `Must`
- **Rationale:** Local agents must not receive unrestricted host access.
- **Actors:** Tool gateway, Agent worker
- **Preconditions:**
  - A file/repository capability is requested.
- **Required behavior:**
  1. Resolve the requested path against approved mounted roots.
  2. Prevent path traversal, symlink escape, and unauthorized repository access.
  3. Enforce read/write capability separately.
  4. Record the normalized target and decision.
  5. Expose safe denial.
- **Failure behavior:**
  - Unknown normalization or mount state denies access.
  - Denied response does not reveal unrelated host paths.
- **Security / approval implications:** Write, delete, commit, push, and merge remain distinct action classes.
- **Acceptance criteria:**
  - `FR-TOL-004-AC-01` — Out-of-scope path access is denied.
  - `FR-TOL-004-AC-02` — Read-only grant cannot write.
  - `FR-TOL-004-AC-03` — Cross-workspace repository access is denied.
- **Traceability:** `PRD-TOL-005`, `SCP-001`, `SAN-001`

### `FR-TOL-005` — Enforce network destination restrictions

- **Priority:** `Must`
- **Rationale:** Unbounded network access can exfiltrate data or reach production systems.
- **Actors:** Tool gateway, Agent worker
- **Preconditions:**
  - A network-capable tool request exists.
- **Required behavior:**
  1. Match destination, protocol, port, and purpose against policy.
  2. Block unapproved destinations.
  3. Apply workspace and data-class rules.
  4. Record destination classification and decision.
  5. Support revocation.
- **Failure behavior:**
  - DNS or destination ambiguity follows restrictive policy.
  - Production destinations remain excluded or high-risk.
- **Security / approval implications:** Secret-bearing and confidential requests require additional policy review.
- **Acceptance criteria:**
  - `FR-TOL-005-AC-01` — Unapproved destination is blocked.
  - `FR-TOL-005-AC-02` — Approved destination access is attributable.
  - `FR-TOL-005-AC-03` — No public/production access exists by default.
- **Traceability:** `PRD-TOL-006`, `SCP-001`, `SEC-001`

### `FR-TOL-006` — Require approval for executable installation or permission expansion

- **Priority:** `Must`
- **Rationale:** Installation and expanded authority can persist beyond one task.
- **Actors:** System, Approver
- **Preconditions:**
  - A request proposes package/plugin installation or broader scope.
- **Required behavior:**
  1. Classify the request as consequential.
  2. Create exact approval request with package/source/version, requested permissions, target, and effects.
  3. Block installation or expansion until approved.
  4. Revalidate source and parameters before execution.
  5. Record receipt.
- **Failure behavior:**
  - Changed package/version/permissions invalidate approval.
  - Unknown source is denied or escalated.
- **Security / approval implications:** Self-modifying skills and autonomous permission expansion are excluded.
- **Acceptance criteria:**
  - `FR-TOL-006-AC-01` — Installation cannot occur without valid approval.
  - `FR-TOL-006-AC-02` — Approved scope matches executed scope.
  - `FR-TOL-006-AC-03` — Historical evidence remains after disablement.
- **Traceability:** `PRD-TOL-011`, `PRD-APR-013`, `SCP-001`

### `FR-TOL-007` — Record tool execution receipt

- **Priority:** `Must`
- **Rationale:** Audit and recovery depend on knowing what tool action occurred.
- **Actors:** Tool gateway, Auditor
- **Preconditions:**
  - A tool invocation is accepted or attempted.
- **Required behavior:**
  1. Record request identity, run/step, tool/capability/version, normalized target, policy decision, approval reference, start/end, result, side-effect status, and evidence gaps.
  2. Link artifacts or output references.
  3. Redact secrets.
  4. Preserve failure and unknown outcomes.
- **Failure behavior:**
  - Receipt failure is visible and may block consequential execution according to policy.
  - Tool timeout does not become success.
- **Security / approval implications:** Receipt integrity is security-relevant.
- **Acceptance criteria:**
  - `FR-TOL-007-AC-01` — Every accepted protected invocation has a receipt.
  - `FR-TOL-007-AC-02` — Receipt links to policy and approval.
  - `FR-TOL-007-AC-03` — Unknown side effect is explicit.
- **Traceability:** `PRD-TOL-007`, `JTBD-011`, `AUD-001`


## 16. Memory and knowledge requirements

### `FR-MEM-001` — Create a governed memory record

- **Priority:** `Must`
- **Rationale:** Useful context should be retained with source and authority labels.
- **Actors:** Builder-Operator, Run, System
- **Preconditions:**
  - The actor/run has memory-write permission.
  - The proposed content passes data-classification policy.
- **Required behavior:**
  1. Create stable record identity.
  2. Store workspace, optional project, source, producer, creation time, record type, classification, confidence/verification state, retention state, and content reference.
  3. Apply policy for automatic versus approval-required writes.
  4. Audit creation.
- **Failure behavior:**
  - Secret or prohibited data is blocked from ordinary memory.
  - Missing source or workspace prevents active storage.
- **Security / approval implications:** Agent output cannot become authoritative merely by being stored.
- **Acceptance criteria:**
  - `FR-MEM-001-AC-01` — Every active record has provenance and workspace scope.
  - `FR-MEM-001-AC-02` — Generated content remains labeled.
  - `FR-MEM-001-AC-03` — Unauthorized writes fail.
- **Traceability:** `PRD-MEM-001`, `PRD-MEM-002`, `UC-020`, `JRN-011`

### `FR-MEM-002` — Retrieve memory within authorized scope

- **Priority:** `Must`
- **Rationale:** Context retrieval must respect workspace isolation and explain inclusion.
- **Actors:** Builder-Operator, Run, Auditor
- **Preconditions:**
  - The requester has memory-read permission in the workspace.
- **Required behavior:**
  1. Filter candidates by workspace and policy before relevance processing.
  2. Apply classification and retention rules.
  3. Return source, age, verification/confidence state, and reason for inclusion where practical.
  4. Record security-relevant retrieval evidence where defined.
  5. Exclude inactive, deleted, or unauthorized records.
- **Failure behavior:**
  - Authorization uncertainty denies retrieval.
  - Cross-workspace candidates are excluded before response construction.
- **Security / approval implications:** Retrieved content remains subject to provider/tool data policy before onward use.
- **Acceptance criteria:**
  - `FR-MEM-002-AC-01` — Cross-workspace retrieval tests pass.
  - `FR-MEM-002-AC-02` — Returned records include source and state.
  - `FR-MEM-002-AC-03` — Deleted/expired records are not returned as active.
- **Traceability:** `PRD-MEM-005`, `PRD-MEM-006`, `PRD-MEM-007`, `UC-021`

### `FR-MEM-003` — Label generated, inferred, verified, and authoritative knowledge

- **Priority:** `Must`
- **Rationale:** Users must distinguish evidence quality and source authority.
- **Actors:** All authorized memory users
- **Preconditions:**
  - A memory/knowledge record exists.
- **Required behavior:**
  1. Support controlled verification/source states.
  2. Display the state with source information.
  3. Prevent generated or inferred records from being displayed as authoritative without explicit governed promotion.
  4. Preserve prior state history.
- **Failure behavior:**
  - Unknown state remains unknown.
  - Conflicting authoritative sources are flagged.
- **Security / approval implications:** Promotion to higher authority may require designated owner approval.
- **Acceptance criteria:**
  - `FR-MEM-003-AC-01` — Generated hypotheses are visibly labeled.
  - `FR-MEM-003-AC-02` — Authority state is auditable.
  - `FR-MEM-003-AC-03` — UI does not hide conflict.
- **Traceability:** `PRD-MEM-003`, `PRD-MEM-012`, `JRN-011`

### `FR-MEM-004` — Correct or supersede memory

- **Priority:** `Must`
- **Rationale:** Users need a governed way to fix inaccurate retained context.
- **Actors:** Authorized user, Data/Knowledge owner
- **Preconditions:**
  - The record exists and the actor has correction authority.
- **Required behavior:**
  1. Create a correction or superseding record.
  2. Link prior and new versions.
  3. Preserve historical provenance according to policy.
  4. Mark the prior record inactive or superseded.
  5. Audit the change.
- **Failure behavior:**
  - Unauthorized correction is denied.
  - Concurrent conflicting correction is surfaced.
- **Security / approval implications:** Correction cannot rewrite immutable audit history.
- **Acceptance criteria:**
  - `FR-MEM-004-AC-01` — Retrieval returns the active corrected record.
  - `FR-MEM-004-AC-02` — Historical relationship remains inspectable.
  - `FR-MEM-004-AC-03` — Correction is attributable.
- **Traceability:** `PRD-MEM-008`, `UC-022`

### `FR-MEM-005` — Delete or expire memory under policy

- **Priority:** `Must`
- **Rationale:** Retention and user control require records to leave active retrieval.
- **Actors:** Authorized user, System
- **Preconditions:**
  - A record exists.
  - Deletion/retention policy permits the action.
- **Required behavior:**
  1. Mark the record deleted or expired.
  2. Remove it from active retrieval.
  3. Handle content deletion and retained audit metadata according to policy.
  4. Record the action.
  5. Propagate deletion to derived indexes within the defined bound.
- **Failure behavior:**
  - Deletion failure is visible and retried according to policy.
  - Legal/security retention prevents deletion only with explicit reason.
- **Security / approval implications:** Deletion authorization and audit are required.
- **Acceptance criteria:**
  - `FR-MEM-005-AC-01` — Deleted record is not returned as active.
  - `FR-MEM-005-AC-02` — Deletion state is visible to authorized reviewers.
  - `FR-MEM-005-AC-03` — Indexes converge within the specified bound.
- **Traceability:** `PRD-MEM-008`, `PRD-MEM-009`

### `FR-MEM-006` — Govern automatic memory writes

- **Priority:** `Must`
- **Rationale:** Agents should not silently store every output as persistent context.
- **Actors:** System, Workspace Owner
- **Preconditions:**
  - A run proposes automatic memory creation.
- **Required behavior:**
  1. Evaluate record type, source, data class, task policy, workspace policy, and approval requirement.
  2. Allow, deny, request approval, or store as temporary context according to policy.
  3. Show the resulting memory action in run evidence.
- **Failure behavior:**
  - Unknown classification blocks permanent automatic storage.
  - Denied write does not fail the entire run unless the task requires it.
- **Security / approval implications:** Prompt instruction cannot override memory-write policy.
- **Acceptance criteria:**
  - `FR-MEM-006-AC-01` — Automatic writes occur only under explicit policy.
  - `FR-MEM-006-AC-02` — Denied writes are visible.
  - `FR-MEM-006-AC-03` — Permanent and temporary context are distinct.
- **Traceability:** `PRD-MEM-011`, `JRN-011`


## 17. Artifact requirements

### `FR-ART-001` — Store an artifact with provenance

- **Priority:** `Must`
- **Rationale:** Outputs must remain linked to their producing work.
- **Actors:** Run, Builder-Operator
- **Preconditions:**
  - The producer has artifact-write permission.
  - The content type and size are permitted.
- **Required behavior:**
  1. Create stable artifact identity.
  2. Store workspace, project, task, run, step, producer, media type, size, integrity hash, classification, lifecycle state, storage reference, and timestamp.
  3. Persist metadata and content reference consistently.
  4. Audit creation.
- **Failure behavior:**
  - Metadata-only or content-only partial failure is marked unavailable/partial, not complete.
  - Integrity calculation failure blocks trusted state.
- **Security / approval implications:** Artifact content follows classification, malware, and safe-storage policy.
- **Acceptance criteria:**
  - `FR-ART-001-AC-01` — Artifact survives restart.
  - `FR-ART-001-AC-02` — Provenance links are complete.
  - `FR-ART-001-AC-03` — Partial storage is visible.
- **Traceability:** `PRD-ART-001`, `PRD-ART-002`, `UC-018`, `JRN-010`

### `FR-ART-002` — Support initial artifact types

- **Priority:** `Must`
- **Rationale:** The pilot needs a bounded useful set of outputs.
- **Actors:** Builder-Operator, Contributor
- **Preconditions:**
  - Artifact storage is available.
- **Required behavior:**
  1. Support text, Markdown, JSON, code patch, test log, and approved small-file artifacts.
  2. Validate media type and size.
  3. Reject unsupported executable behavior.
  4. Record unavailable preview where necessary.
- **Failure behavior:**
  - Unsupported or oversized content is rejected with actionable guidance.
  - Declared and detected type mismatch is flagged.
- **Security / approval implications:** Executable content is not run through preview.
- **Acceptance criteria:**
  - `FR-ART-002-AC-01` — Each required pilot artifact type can be stored and retrieved.
  - `FR-ART-002-AC-02` — Unsupported types are not silently accepted.
  - `FR-ART-002-AC-03` — Type mismatch is visible.
- **Traceability:** `PRD-ART-003`, `SCP-001`

### `FR-ART-003` — Retrieve and preview an authorized artifact

- **Priority:** `Must`
- **Rationale:** Users need safe access to the correct retained output.
- **Actors:** Builder-Operator, Contributor, Auditor
- **Preconditions:**
  - The artifact exists.
  - The actor has workspace and artifact permission.
- **Required behavior:**
  1. Authorize metadata and content separately as needed.
  2. Display provenance, lifecycle, classification, version/derivative relationship, integrity status, and availability.
  3. Provide safe preview or explicit no-preview state.
  4. Allow authorized download/export.
- **Failure behavior:**
  - Unauthorized access returns safe denial.
  - Missing content, integrity mismatch, or unsafe preview is prominently shown.
- **Security / approval implications:** Preview must not execute active content or leak unrelated data.
- **Acceptance criteria:**
  - `FR-ART-003-AC-01` — Wrong-workspace artifact is not discoverable.
  - `FR-ART-003-AC-02` — Integrity failure blocks trusted preview/download.
  - `FR-ART-003-AC-03` — Provenance is visible.
- **Traceability:** `PRD-ART-005`, `PRD-ART-006`, `PRD-ART-007`, `UC-019`

### `FR-ART-004` — Manage artifact lifecycle

- **Priority:** `Must`
- **Rationale:** Users need to know whether an output is draft, accepted, rejected, superseded, or unavailable.
- **Actors:** Authorized reviewer, Builder-Operator, System
- **Preconditions:**
  - The artifact exists.
- **Required behavior:**
  1. Support generated, under-review, accepted, rejected, superseded, archived, deleted, and unavailable states.
  2. Define allowed transitions and role requirements.
  3. Record reason and actor for review transitions.
  4. Link superseding artifact.
  5. Keep evidence after archival/deletion according to policy.
- **Failure behavior:**
  - Invalid transition is rejected.
  - Missing superseding target prevents superseded state.
- **Security / approval implications:** Acceptance does not make generated business data authoritative outside its declared scope.
- **Acceptance criteria:**
  - `FR-ART-004-AC-01` — Lifecycle state is visible.
  - `FR-ART-004-AC-02` — Superseded artifacts link to replacement.
  - `FR-ART-004-AC-03` — Transitions are auditable.
- **Traceability:** `PRD-ART-004`, `PRD-ART-008`, `JRN-010`

### `FR-ART-005` — Validate artifact integrity

- **Priority:** `Must`
- **Rationale:** Corrupted or replaced content must not be treated as trusted output.
- **Actors:** System, Auditor
- **Preconditions:**
  - Artifact content and expected integrity metadata exist.
- **Required behavior:**
  1. Calculate and store integrity hash at ingestion.
  2. Verify on retrieval or scheduled validation according to policy.
  3. Mark mismatch or missing content.
  4. Prevent accepted/trusted presentation when integrity fails.
  5. Record validation evidence.
- **Failure behavior:**
  - Storage read failure yields unavailable state.
  - Hash mismatch triggers alert and investigation path.
- **Security / approval implications:** Integrity metadata is protected from ordinary modification.
- **Acceptance criteria:**
  - `FR-ART-005-AC-01` — Tampered content is detected in test.
  - `FR-ART-005-AC-02` — Mismatch is visible.
  - `FR-ART-005-AC-03` — Trusted download is blocked or warned according to policy.
- **Traceability:** `PRD-ART-007`, `JRN-010`

### `FR-ART-006` — Create an evidence export artifact

- **Priority:** `Should`
- **Rationale:** Authorized reviews may require a bounded portable package.
- **Actors:** Auditor, Product / Workspace Owner
- **Preconditions:**
  - The actor has export permission.
  - The selected scope is valid.
- **Required behavior:**
  1. Preview included record classes and exclusions.
  2. Apply workspace, classification, redaction, and retention policy.
  3. Create manifest with source records and integrity metadata.
  4. Store the export itself as an artifact with provenance.
  5. Audit the export.
- **Failure behavior:**
  - Export failure produces no misleading complete package.
  - Prohibited or unrelated records are excluded.
- **Security / approval implications:** Evidence export is a consequential disclosure action and may require approval.
- **Acceptance criteria:**
  - `FR-ART-006-AC-01` — Package contains only authorized scope.
  - `FR-ART-006-AC-02` — Redaction tests pass.
  - `FR-ART-006-AC-03` — Export artifact links to request and source range.
- **Traceability:** `PRD-ART-009`, `PRD-AUD-008`, `JRN-020`, `UC-030`


## 18. Audit and evidence requirements

### `FR-AUD-001` — Record correlated audit events

- **Priority:** `Must`
- **Rationale:** The platform must support reconstruction of significant actions.
- **Actors:** System
- **Preconditions:**
  - A security-relevant or operationally significant event occurs.
- **Required behavior:**
  1. Create event with stable identity, timestamp, actor, identity type, organization, workspace, project/task/run/step where applicable, event type, result, correlation, and evidence references.
  2. Use a versioned schema.
  3. Preserve ordering/causality information.
  4. Protect event integrity.
- **Failure behavior:**
  - Event-ingestion failure is visible and may block consequential actions.
  - Malformed events are rejected or quarantined.
- **Security / approval implications:** Audit storage and modification require strong controls; raw secrets are prohibited.
- **Acceptance criteria:**
  - `FR-AUD-001-AC-01` — Required event fields validate.
  - `FR-AUD-001-AC-02` — Events correlate across the pilot vertical slice.
  - `FR-AUD-001-AC-03` — Tampering attempts are detectable according to the chosen design.
- **Traceability:** `PRD-AUD-001`, `UC-023`, `AUD-001`

### `FR-AUD-002` — Provide a read-only audit timeline

- **Priority:** `Must`
- **Rationale:** Auditors need evidence without operational modification authority.
- **Actors:** Auditor / Assurance Reviewer
- **Preconditions:**
  - The actor has audit-read permission for the workspace.
- **Required behavior:**
  1. Filter by workspace, project, task, run, identity, adapter, model, tool, approval, artifact, and period.
  2. Display correlated timeline.
  3. Distinguish fact, provider report, derived estimate, stale, unknown, and missing evidence.
  4. Provide drill-down to authorized details.
- **Failure behavior:**
  - Unauthorized filters return safe denial or empty authorized results.
  - Missing data remains visible.
- **Security / approval implications:** Audit role cannot change operational state.
- **Acceptance criteria:**
  - `FR-AUD-002-AC-01` — Auditor reconstructs the defined pilot scenario.
  - `FR-AUD-002-AC-02` — Evidence gaps are explicit.
  - `FR-AUD-002-AC-03` — Cross-workspace data is absent.
- **Traceability:** `PRD-AUD-002`, `PRD-AUD-003`, `JRN-013`

### `FR-AUD-003` — Link approvals to execution outcomes

- **Priority:** `Must`
- **Rationale:** Reviewers must know whether an approved action actually ran and what happened.
- **Actors:** System, Auditor, Approver
- **Preconditions:**
  - An approval request or decision exists.
- **Required behavior:**
  1. Link request, decision, consumption, execution attempt, tool receipt, and outcome.
  2. Display unused, expired, rejected, invalidated, consumed-success, consumed-failure, and consumed-unknown relationships.
  3. Preserve the exact action hash/version.
- **Failure behavior:**
  - Missing execution evidence is shown as unknown.
  - Failed action does not appear successful because approval existed.
- **Security / approval implications:** Linkage is immutable or tamper-evident according to architecture.
- **Acceptance criteria:**
  - `FR-AUD-003-AC-01` — Every consumed approval links to one execution attempt.
  - `FR-AUD-003-AC-02` — Outcome state is correct.
  - `FR-AUD-003-AC-03` — Replay is detectable.
- **Traceability:** `PRD-AUD-005`, `JRN-007`

### `FR-AUD-004` — Preserve retry, resume, cancellation, and failure lineage

- **Priority:** `Must`
- **Rationale:** Recovery history must remain understandable.
- **Actors:** System, Auditor
- **Preconditions:**
  - A run has multiple attempts or interruption events.
- **Required behavior:**
  1. Link original step, attempts, checkpoints, cancellation intent, adapter response, and final state.
  2. Display sequence and reasons.
  3. Preserve side-effect and approval status for each attempt.
- **Failure behavior:**
  - Missing attempt data is marked incomplete.
  - Lineage conflict triggers investigation state.
- **Security / approval implications:** Lineage records cannot be rewritten by the agent.
- **Acceptance criteria:**
  - `FR-AUD-004-AC-01` — Auditor can identify every attempt.
  - `FR-AUD-004-AC-02` — Duplicate-effect protection is evidenced.
  - `FR-AUD-004-AC-03` — Unknown status remains visible.
- **Traceability:** `PRD-AUD-006`, `JRN-009`

### `FR-AUD-005` — Redact secrets from audit evidence

- **Priority:** `Must`
- **Rationale:** Audit usefulness must not create a credential repository.
- **Actors:** System, Security Owner
- **Preconditions:**
  - An event or receipt contains fields that may include sensitive values.
- **Required behavior:**
  1. Apply schema-based redaction and safe-reference rules.
  2. Store approved secret identifiers rather than values.
  3. Prevent user-provided raw secrets from appearing in ordinary audit payloads where detectable.
  4. Record redaction occurrence without exposing the value.
- **Failure behavior:**
  - Redaction failure blocks or quarantines the sensitive event according to policy.
  - Unknown sensitive content is flagged.
- **Security / approval implications:** Secret-scanning and access control are mandatory.
- **Acceptance criteria:**
  - `FR-AUD-005-AC-01` — Known secret patterns are absent from ordinary audit output.
  - `FR-AUD-005-AC-02` — Authorized reviewers see reference and reason, not value.
  - `FR-AUD-005-AC-03` — Redaction tests pass.
- **Traceability:** `PRD-AUD-004`, `PRD-XC-005`, `SEC-001`

### `FR-AUD-006` — Expose evidence gaps and collection failures

- **Priority:** `Must`
- **Rationale:** A complete-looking timeline must not hide missing data.
- **Actors:** System, Auditor, Owner
- **Preconditions:**
  - Expected evidence is missing, delayed, contradictory, or unavailable.
- **Required behavior:**
  1. Create an explicit gap or collection-status record.
  2. Identify the affected component, period, and impact.
  3. Propagate the limitation to run receipts and Mission Control where relevant.
  4. Provide diagnostic path.
- **Failure behavior:**
  - Gap-recording failure does not convert missing evidence to success.
  - Unknown impact remains unknown.
- **Security / approval implications:** Evidence gaps may block acceptance of consequential or terminal states.
- **Acceptance criteria:**
  - `FR-AUD-006-AC-01` — Missing data is visible in audit and receipt.
  - `FR-AUD-006-AC-02` — Dashboard does not silently treat missing as zero.
  - `FR-AUD-006-AC-03` — Users can locate diagnostics.
- **Traceability:** `PRD-AUD-007`, `PRD-UI-003`, `JTBD-014`


## 19. Usage and cost requirements

### `FR-CST-001` — Record model and tool usage events

- **Priority:** `Must`
- **Rationale:** Cost attribution begins with normalized usage evidence.
- **Actors:** System, Provider adapter, Tool gateway
- **Preconditions:**
  - A supported billable or measurable event occurs.
- **Required behavior:**
  1. Record provider/tool source, metric type, quantity, unit, timestamp/period, workspace, task, run, and correlation.
  2. Identify whether the value is provider-reported, calculated, estimated, pending, unavailable, or unattributed.
  3. Preserve source payload reference where permitted.
- **Failure behavior:**
  - Malformed or duplicate events are rejected or reconciled.
  - Missing usage remains visible.
- **Security / approval implications:** Usage records follow workspace authorization and privacy rules.
- **Acceptance criteria:**
  - `FR-CST-001-AC-01` — Supported events are stored.
  - `FR-CST-001-AC-02` — Duplicate ingestion does not double count.
  - `FR-CST-001-AC-03` — Status/source is explicit.
- **Traceability:** `PRD-CST-001`, `PRD-CST-002`, `JRN-012`

### `FR-CST-002` — Calculate and display attributed cost

- **Priority:** `Must`
- **Rationale:** Users need understandable spend at workspace, task, and run level.
- **Actors:** Workspace Owner, Builder-Operator
- **Preconditions:**
  - Usage records and applicable pricing data exist or are explicitly unavailable.
- **Required behavior:**
  1. Calculate cost using versioned pricing inputs where appropriate.
  2. Display currency, source, period, freshness, and attribution scope.
  3. Aggregate by workspace, project, task, run, provider/model, and tool.
  4. Keep provider-reported and calculated values distinct.
- **Failure behavior:**
  - Missing pricing yields unavailable/estimated state.
  - Currency conversion is not performed without a defined source and timestamp.
- **Security / approval implications:** Cost views must not expose unauthorized workspace activity.
- **Acceptance criteria:**
  - `FR-CST-002-AC-01` — Aggregation reconciles with underlying events within defined tolerance.
  - `FR-CST-002-AC-02` — Unknown cost is not zero.
  - `FR-CST-002-AC-03` — Source and freshness are visible.
- **Traceability:** `PRD-CST-003`, `PRD-CST-004`, `JRN-012`

### `FR-CST-003` — Surface unattributed and reconciliation mismatches

- **Priority:** `Should`
- **Rationale:** Hidden mismatches undermine budget control.
- **Actors:** Workspace Owner, Technical Operator, Auditor
- **Preconditions:**
  - Provider/tool records and Agent OS usage records can be compared.
- **Required behavior:**
  1. Identify unmatched, duplicate, delayed, or conflicting events.
  2. Display reconciliation status and affected amount/usage.
  3. Allow authorized drill-down.
  4. Preserve resolution notes.
- **Failure behavior:**
  - Unavailable provider records remain pending/unavailable.
  - Mismatch is not silently absorbed.
- **Security / approval implications:** Reconciliation evidence follows provider and workspace access rules.
- **Acceptance criteria:**
  - `FR-CST-003-AC-01` — Unattributed usage is visible.
  - `FR-CST-003-AC-02` — Mismatch status is traceable.
  - `FR-CST-003-AC-03` — Resolution changes are auditable.
- **Traceability:** `PRD-CST-005`, `JRN-012`

### `FR-CST-004` — Enforce cost thresholds

- **Priority:** `Must`
- **Rationale:** Budgets must influence execution rather than being decorative.
- **Actors:** System, Workspace Owner
- **Preconditions:**
  - Applicable threshold exists.
  - Usage can be measured sufficiently for the policy.
- **Required behavior:**
  1. Evaluate hard and warning thresholds during preflight and runtime.
  2. Warn, pause, stop, or require approval according to policy.
  3. Record threshold events and action taken.
  4. Expose delayed-data limitations.
- **Failure behavior:**
  - Unknown cost state follows the configured conservative policy.
  - Threshold-processing failure fails safe for hard limits.
- **Security / approval implications:** Budget override is privileged and auditable.
- **Acceptance criteria:**
  - `FR-CST-004-AC-01` — Hard-limit tests block or stop as specified.
  - `FR-CST-004-AC-02` — Warning thresholds notify without false completion.
  - `FR-CST-004-AC-03` — Override evidence exists.
- **Traceability:** `PRD-CST-006`, `FR-MOD-004`

### `FR-CST-005` — Separate AI operating cost from business profit

- **Priority:** `Must`
- **Rationale:** Model/tool spend is not an accounting ledger or profit calculation.
- **Actors:** All cost-view users
- **Preconditions:**
  - Cost information is displayed.
- **Required behavior:**
  1. Label the view as AI/model/tool usage and cost.
  2. Avoid derived revenue, margin, or profit unless sourced from a future authorized business-data model.
  3. Display explanatory source and limitation text.
  4. Keep generated analysis separate from authoritative records.
- **Failure behavior:**
  - Unavailable business data remains unavailable.
  - No promotional placeholder is shown as real financial performance.
- **Security / approval implications:** Financial-source separation is mandatory.
- **Acceptance criteria:**
  - `FR-CST-005-AC-01` — Users cannot mistake provider spend for business profit.
  - `FR-CST-005-AC-02` — No production financial write is available.
  - `FR-CST-005-AC-03` — Source labels are present.
- **Traceability:** `PRD-CST-007`, `SCP-001`, `VSN-001`


## 20. Mission Control and interaction requirements

### `FR-UI-001` — Provide a responsive Mission Control

- **Priority:** `Must`
- **Rationale:** Users need one coherent operational overview rather than fragmented chats.
- **Actors:** All authenticated users
- **Preconditions:**
  - The user has at least one workspace.
- **Required behavior:**
  1. Display authorized active tasks, runs, approvals, failures, usage/cost, and health summaries.
  2. Use persisted or explicitly classified source data.
  3. Support drill-down to underlying records.
  4. Respect role and workspace scope.
  5. Reflow at approved viewports.
- **Failure behavior:**
  - Collection failure shows unavailable/stale state.
  - No mock fallback is silently substituted.
- **Security / approval implications:** Summary authorization must match detail authorization.
- **Acceptance criteria:**
  - `FR-UI-001-AC-01` — Summary values reconcile with detail.
  - `FR-UI-001-AC-02` — No global horizontal scroll at approved widths.
  - `FR-UI-001-AC-03` — Unauthorized information is absent.
- **Traceability:** `PRD-UI-001`, `PRD-UI-002`, `JRN-018`

### `FR-UI-002` — Display controlled state semantics

- **Priority:** `Must`
- **Rationale:** Users must correctly distinguish success, failure, absence, uncertainty, and staleness.
- **Actors:** All authenticated users
- **Preconditions:**
  - A state-dependent view is rendered.
- **Required behavior:**
  1. Display zero, unavailable, stale, estimated, partial, failed, cancelled, waiting, and unknown distinctly.
  2. Show timestamp and source where relevant.
  3. Provide explanatory text and non-color indicators.
  4. Propagate state consistently across summary and detail.
- **Failure behavior:**
  - Conflicting sources yield explicit conflict/unknown state.
  - Missing timestamp prevents current-state presentation.
- **Security / approval implications:** State display must not overstate evidence.
- **Acceptance criteria:**
  - `FR-UI-002-AC-01` — Usability tests show correct interpretation.
  - `FR-UI-002-AC-02` — Zero and unavailable are not visually or semantically identical.
  - `FR-UI-002-AC-03` — Screen readers receive state information.
- **Traceability:** `PRD-UI-003`, `JTBD-014`, `UCD-001`

### `FR-UI-003` — Provide primary domain navigation

- **Priority:** `Must`
- **Rationale:** Users need predictable access to core operational areas.
- **Actors:** All authenticated users
- **Preconditions:**
  - The user is authenticated.
- **Required behavior:**
  1. Provide navigation to workspaces, projects, tasks, runs, approvals, agents, models, tools/integrations, memory/knowledge, artifacts, costs/usage, audit, and operations according to permission.
  2. Show active scope.
  3. Support keyboard navigation and current-location indication.
  4. Hide or safely disable unauthorized sections without misleading access.
- **Failure behavior:**
  - Missing permission produces safe access explanation.
  - Navigation failure does not change scope.
- **Security / approval implications:** Navigation visibility is not the sole authorization control.
- **Acceptance criteria:**
  - `FR-UI-003-AC-01` — Every Must journey has a discoverable entry path.
  - `FR-UI-003-AC-02` — Keyboard navigation has no trap.
  - `FR-UI-003-AC-03` — Active location and scope are clear.
- **Traceability:** `PRD-UI-005`, `PRD-UI-006`, `UXA-001`

### `FR-UI-004` — Provide actionable error and empty states

- **Priority:** `Must`
- **Rationale:** Users need to know what failed or why a section is empty.
- **Actors:** All users
- **Preconditions:**
  - An error or empty collection occurs.
- **Required behavior:**
  1. Explain what failed or why no data appears.
  2. State what is known, what may have happened, what is unknown, and next actions.
  3. Distinguish no data, missing configuration, denied access, unavailable collection, and filter exclusion.
  4. Link to diagnostics or remediation where authorized.
- **Failure behavior:**
  - Sensitive details are omitted.
  - Unknown remains explicit.
- **Security / approval implications:** Errors must not expose secrets, private paths, or unrelated workspace data.
- **Acceptance criteria:**
  - `FR-UI-004-AC-01` — Users can choose a valid next step.
  - `FR-UI-004-AC-02` — Empty states are not mistaken for zero activity.
  - `FR-UI-004-AC-03` — Error summaries are accessible.
- **Traceability:** `PRD-UI-008`, `PRD-UI-009`, `UCD-001`

### `FR-UI-005` — Provide progressive disclosure of evidence

- **Priority:** `Should`
- **Rationale:** Primary users need concise summaries while technical users need detailed evidence.
- **Actors:** Builder-Operator, Owner, Technical Operator, Auditor
- **Preconditions:**
  - A detailed record exists.
- **Required behavior:**
  1. Display plain-language summary first.
  2. Provide expandable technical parameters, policy decisions, events, and raw structured references where authorized.
  3. Preserve context when expanding/collapsing.
  4. Keep critical warnings visible at every level.
- **Failure behavior:**
  - Unavailable technical evidence is labeled.
  - Collapsed detail does not hide approval-critical changes.
- **Security / approval implications:** Sensitive details follow role and classification.
- **Acceptance criteria:**
  - `FR-UI-005-AC-01` — Primary summary is understandable.
  - `FR-UI-005-AC-02` — Technical evidence is reachable.
  - `FR-UI-005-AC-03` — Critical risk is never hidden only in collapsed content.
- **Traceability:** `PRD-UI-007`, `PER-001`

### `FR-UI-006` — Support accessible interaction

- **Priority:** `Must`
- **Rationale:** The product must be usable without a mouse or color-only cues.
- **Actors:** All users
- **Preconditions:**
  - A user interacts with a Must journey.
- **Required behavior:**
  1. Provide keyboard operability, logical focus order, visible focus, accessible names/roles/states, non-color indicators, zoom/reflow, reduced motion, and perceivable dynamic updates.
  2. Use semantic landmarks and headings.
  3. Provide accessible table/timeline behavior.
- **Failure behavior:**
  - Accessibility failure is tracked as a product defect.
  - Critical blockers prevent acceptance of the affected journey.
- **Security / approval implications:** Approval and security-critical controls require especially clear accessible labeling.
- **Acceptance criteria:**
  - `FR-UI-006-AC-01` — All Must journeys complete by keyboard.
  - `FR-UI-006-AC-02` — No unresolved critical blocker remains.
  - `FR-UI-006-AC-03` — Dynamic state changes are announced appropriately.
- **Traceability:** `PRD-A11Y-001` through `PRD-A11Y-008`, `A11Y-001`

### `FR-UI-007` — Restrict consequential mobile actions

- **Priority:** `Must`
- **Rationale:** Mobile review can be useful, but sensitive execution needs explicit approval and security design.
- **Actors:** Mobile user
- **Preconditions:**
  - The user accesses Agent OS at a mobile viewport.
- **Required behavior:**
  1. Provide status, review, artifact, and permitted low-risk interactions.
  2. Hide or disable consequential execution classes unless `AUT-001` and security policy explicitly permit them.
  3. Explain why a restricted action requires desktop/trusted context.
  4. Preserve responsive accessibility.
- **Failure behavior:**
  - Viewport detection is not the sole security control; device/session policy applies.
  - Unsupported action returns safe denial.
- **Security / approval implications:** Consequential action authorization must be server-enforced.
- **Acceptance criteria:**
  - `FR-UI-007-AC-01` — Mobile cannot execute unapproved sensitive classes.
  - `FR-UI-007-AC-02` — Review information remains usable.
  - `FR-UI-007-AC-03` — Denial is clear and accessible.
- **Traceability:** `PRD-UI-012`, `SCP-001`, `UCD-001`


## 21. Operations, health, backup, and restore requirements

### `FR-OPS-001` — Expose component health and diagnostics

- **Priority:** `Must`
- **Rationale:** Operators need to identify whether failures belong to platform, adapter, provider, storage, tools, or event processing.
- **Actors:** Technical Operator
- **Preconditions:**
  - The local installation is running sufficiently to expose diagnostics.
- **Required behavior:**
  1. Display control plane, adapter, provider validation, storage, tool gateway, event pipeline, and backup status separately.
  2. Use registered, reachable, validated, degraded, failed, stale, and unknown semantics.
  3. Show last check, evidence, and safe remediation.
  4. Allow read-only diagnostic retry.
- **Failure behavior:**
  - Diagnostic failure is labeled.
  - No component is marked healthy solely because it is configured.
- **Security / approval implications:** Diagnostics must not reveal secrets or perform consequential actions.
- **Acceptance criteria:**
  - `FR-OPS-001-AC-01` — Operator can identify the failing boundary.
  - `FR-OPS-001-AC-02` — Stale checks are visible.
  - `FR-OPS-001-AC-03` — Diagnostic actions are auditable.
- **Traceability:** `PRD-OPS-002`, `PRD-OPS-003`, `JRN-016`, `UC-031`

### `FR-OPS-002` — Support controlled local configuration

- **Priority:** `Must`
- **Rationale:** The pilot must be reproducible without committing credentials.
- **Actors:** Technical Operator
- **Preconditions:**
  - The application is installed.
- **Required behavior:**
  1. Load configuration from approved local mechanisms.
  2. Use secret references or protected environment mechanisms.
  3. Validate required configuration at startup.
  4. Show missing configuration without exposing values.
  5. Record build/version identity.
- **Failure behavior:**
  - Missing required configuration prevents affected capability from appearing healthy.
  - Invalid secret reference is handled safely.
- **Security / approval implications:** Secrets must not be committed, logged, or stored in ordinary documents.
- **Acceptance criteria:**
  - `FR-OPS-002-AC-01` — Startup validation identifies missing fields.
  - `FR-OPS-002-AC-02` — Repository secret checks pass.
  - `FR-OPS-002-AC-03` — Operator can identify deployed build/version.
- **Traceability:** `PRD-OPS-004`, `PRD-OPS-012`, `VSN-001`

### `FR-OPS-003` — Start and stop cleanly

- **Priority:** `Must`
- **Rationale:** Local restarts must not corrupt accepted state.
- **Actors:** Technical Operator, System
- **Preconditions:**
  - The installation and persistent stores are configured.
- **Required behavior:**
  1. Start components in dependency-aware order.
  2. Run schema/configuration checks.
  3. Expose readiness separately from process liveness.
  4. Stop accepting new work during controlled shutdown.
  5. Persist or safely transition active work.
  6. Stop components without corrupting data.
- **Failure behavior:**
  - Startup migration/configuration failure leaves service not-ready.
  - Forced shutdown produces stale/unknown recovery state where necessary.
- **Security / approval implications:** Shutdown must not bypass audit or approval rules.
- **Acceptance criteria:**
  - `FR-OPS-003-AC-01` — Clean restart preserves required records.
  - `FR-OPS-003-AC-02` — Readiness is false until dependencies pass.
  - `FR-OPS-003-AC-03` — Interrupted active work is recoverable or explicitly unknown.
- **Traceability:** `PRD-OPS-011`, `OBJ-001`

### `FR-OPS-004` — Create a backup with manifest and integrity evidence

- **Priority:** `Must`
- **Rationale:** Local-first operation requires recoverable retained data.
- **Actors:** Technical Operator
- **Preconditions:**
  - The system is in an approved backup state.
  - The actor has backup authority.
- **Required behavior:**
  1. Define included data classes and exclusions.
  2. Create backup of approved persistent data and artifact references/content according to design.
  3. Create manifest with version, time, scope, counts, and integrity information.
  4. Protect or exclude secrets according to policy.
  5. Record success, partial, or failure state.
- **Failure behavior:**
  - Missing component or integrity failure prevents complete status.
  - Partial backup lists omitted/unavailable data.
- **Security / approval implications:** Backup access and storage are sensitive operations.
- **Acceptance criteria:**
  - `FR-OPS-004-AC-01` — Manifest matches included data.
  - `FR-OPS-004-AC-02` — Integrity verification passes for a complete backup.
  - `FR-OPS-004-AC-03` — Partial status cannot appear complete.
- **Traceability:** `PRD-OPS-005`, `UC-028`, `JRN-015`

### `FR-OPS-005` — Restore from an approved backup

- **Priority:** `Must`
- **Rationale:** The pilot must demonstrate recovery rather than only backup creation.
- **Actors:** Technical Operator
- **Preconditions:**
  - A compatible backup exists.
  - The actor has restore authority.
  - The system is in an approved restore state.
- **Required behavior:**
  1. Validate backup integrity and compatibility.
  2. Restore data in a controlled process.
  3. Run schema and consistency checks.
  4. Report restored, missing, partial, and failed components.
  5. Reconcile workspaces, tasks, runs, approvals, artifacts, memory, audit, and costs according to backup scope.
  6. Measure recovery time.
- **Failure behavior:**
  - Incompatible/corrupt backup is rejected.
  - Partial restore is never labeled complete.
- **Security / approval implications:** Restore is privileged and may require explicit approval; secret restoration follows separate controls.
- **Acceptance criteria:**
  - `FR-OPS-005-AC-01` — Approved recovery exercise restores expected records.
  - `FR-OPS-005-AC-02` — Data loss is enumerated.
  - `FR-OPS-005-AC-03` — Recovery evidence is retained.
- **Traceability:** `PRD-OPS-006`, `PRD-OPS-007`, `UC-029`, `JRN-015`

### `FR-OPS-006` — Keep default deployment local and non-public

- **Priority:** `Must`
- **Rationale:** The first pilot is not approved for public exposure.
- **Actors:** Technical Operator
- **Preconditions:**
  - The MVP is deployed using default supported configuration.
- **Required behavior:**
  1. Bind and expose services according to the approved local deployment profile.
  2. Require explicit later configuration and approval for remote access.
  3. Display deployment mode in operations view.
  4. Warn when detected exposure differs from the approved local profile where technically possible.
- **Failure behavior:**
  - Unknown exposure state is surfaced.
  - Remote-access configuration is not silently enabled.
- **Security / approval implications:** Public exposure requires later identity, transport, rate-limit, session, threat-model, and incident controls.
- **Acceptance criteria:**
  - `FR-OPS-006-AC-01` — Default pilot is not publicly reachable.
  - `FR-OPS-006-AC-02` — Deployment mode is visible.
  - `FR-OPS-006-AC-03` — Remote access is absent unless separately approved.
- **Traceability:** `PRD-OPS-001`, `PRD-OPS-010`, `SCP-001`


## 22. Functional state models requiring downstream contracts

The following state models shall be formalized in machine-readable or contract form where practical.

### 22.1 Task lifecycle

```text
draft
  → ready
  → active
  → completed
  → archived

draft/ready/active
  → blocked

draft/ready/blocked/active
  → cancelled
```

Exact transition guards belong in the task/run contract and SRS refinement.

### 22.2 Run lifecycle

```text
queued
→ starting
→ running
→ completed | failed | cancelled

running
→ waiting-for-approval
→ running | cancelled | failed

running
→ waiting-for-resource | paused | retrying | stale | unknown
```

Unknown and stale are evidence states, not automatic terminal success/failure.

### 22.3 Approval lifecycle

```text
requested
→ under-review
→ approved | rejected | revision-requested | expired | cancelled

approved
→ consumed | invalidated | expired
```

### 22.4 Artifact lifecycle

```text
generated
→ under-review
→ accepted | rejected
→ superseded | archived | deleted | unavailable
```

## 23. Business rules

| Rule ID | Rule |
|---|---|
| `BR-001` | A workspace is the default isolation boundary. |
| `BR-002` | A project belongs to exactly one workspace in the MVP. |
| `BR-003` | A run belongs to one task snapshot and one workspace. |
| `BR-004` | External execution cannot start before run persistence. |
| `BR-005` | Registration does not imply validation or authorization. |
| `BR-006` | Tool/MCP connectivity does not imply permission. |
| `BR-007` | Human-required approval cannot be supplied by an agent identity. |
| `BR-008` | Material action change invalidates prior approval. |
| `BR-009` | An approval is consumed at most once unless a later explicit policy defines another model. |
| `BR-010` | Unknown cost is not zero. |
| `BR-011` | Generated memory is not authoritative by default. |
| `BR-012` | Archived/deleted status does not erase required audit history. |
| `BR-013` | A disabled adapter cannot receive future dispatch but historical runs remain readable. |
| `BR-014` | A failed or unknown side effect may block retry/resume. |
| `BR-015` | Production financial posting is excluded from the MVP. |
| `BR-016` | Autonomous merge is excluded from the MVP. |
| `BR-017` | Public internet exposure is excluded by default. |
| `BR-018` | No accepted KPI may silently use mock data. |

## 24. Functional data entities

The following conceptual entities are required by the functional specification:

- Organization;
- Workspace;
- Project;
- Membership;
- Role assignment;
- Human identity;
- Workload identity;
- Agent registration;
- Adapter capability declaration;
- Model profile;
- Tool/integration registration;
- Permission grant;
- Task;
- Task snapshot;
- Run;
- Run step/attempt;
- Checkpoint;
- Approval request;
- Approval decision;
- Memory record;
- Artifact;
- Audit event;
- Execution receipt;
- Usage event;
- Cost record;
- Health check;
- Backup manifest;
- Restore exercise/evidence.

Entity schemas and relationships belong in `DDD-001`, `DAT-001`, and the relevant contracts.

## 25. Functional external interfaces

The MVP requires logical interfaces for:

- browser/user interaction;
- identity/session management;
- Hermes adapter;
- Codex adapter;
- model provider access;
- tool/integration gateway;
- filesystem/repository access;
- artifact storage;
- memory/knowledge storage;
- audit/event persistence;
- usage/cost ingestion;
- backup/restore operations.

Protocol and technology selection belongs in `SAD-001`, `INT-001`, API/event contracts, and ADRs.

## 26. Cross-requirement scenarios

### 26.1 First successful vertical slice

1. Authenticate (`FR-AUTH-001`).
2. Select workspace (`FR-AUTH-004`).
3. Create bounded task (`FR-TSK-001`, `FR-TSK-002`).
4. Validate readiness (`FR-TSK-004`).
5. Create persisted run (`FR-RUN-001`).
6. Preflight (`FR-RUN-002`).
7. Dispatch through one adapter (`FR-RUN-003`).
8. Persist steps (`FR-RUN-004`).
9. Store artifact (`FR-ART-001`).
10. Generate receipt (`FR-RUN-010`).
11. Display real state (`FR-UI-001`, `FR-UI-002`).

### 26.2 Consequential action

1. Tool invocation is proposed (`FR-TOL-003`).
2. Action is classified (`FR-APR-001`).
3. Exact request is created (`FR-APR-002`).
4. Approver reviews (`FR-APR-003`).
5. Exact action is approved (`FR-APR-004`).
6. Approval is consumed once (`FR-APR-007`).
7. Tool receipt and audit linkage are created (`FR-TOL-007`, `FR-AUD-003`).

### 26.3 Interrupted run

1. Run becomes stale/unknown (`FR-RUN-008`).
2. User sees actionable state (`FR-UI-004`).
3. Resume is evaluated (`FR-RUN-009`) or retry is evaluated (`FR-RUN-007`).
4. Unsafe duplicate side effect remains blocked.
5. Recovery lineage is preserved (`FR-AUD-004`).

## 27. Requirements intentionally deferred to NFR-001

The following require measurable non-functional definitions rather than additional functional behavior alone:

- availability;
- latency;
- throughput;
- concurrency;
- storage capacity;
- retention duration;
- recovery-point objective;
- recovery-time objective;
- encryption strength;
- password/session parameters;
- log retention;
- scalability;
- portability;
- browser and viewport support;
- accessibility conformance detail;
- reliability targets;
- observability coverage;
- resource limits;
- cost ceilings.

## 28. Requirements intentionally deferred to AUT-001

`AUT-001` shall define:

- action risk classes;
- approval requirements;
- eligible approver roles;
- mobile approval eligibility;
- time/cost/step autonomy levels;
- revocation behavior;
- emergency stop;
- production and financial exclusions;
- source-control action policy;
- package/plugin installation policy;
- external messaging policy.

## 29. Requirements intentionally deferred to architecture and contracts

The SRS does not select:

- programming language or framework;
- database;
- object storage;
- vector/retrieval technology;
- orchestration engine;
- sandbox technology;
- message broker;
- identity provider;
- secret manager;
- MCP, AG-UI, A2A, OpenAPI, or AsyncAPI adoption;
- deployment packaging;
- remote-access topology.

These decisions require `SAD-001`, domain/data/integration architecture, contracts, and ADRs.

## 30. Verification approach

Each requirement shall be assigned one or more verification methods in `TST-001` and `RTM-001`:

- unit test;
- integration test;
- contract test;
- policy conformance test;
- negative-access test;
- fault-injection test;
- end-to-end test;
- accessibility test;
- backup/restore exercise;
- security review;
- manual UX validation;
- audit evidence review.

No requirement may be marked implemented solely because a UI component exists.

## 31. Requirements coverage targets

Before MVP acceptance:

- 100% of `Must` requirements must have linked test cases;
- 100% of `Must` requirements must have an implementation/evidence status;
- all deferred requirements must have explicit rationale and owner;
- all security-sensitive requirements must include negative tests;
- all approval requirements must include denial, expiry, invalidation, and replay tests;
- all cross-workspace paths must include negative-access tests;
- all stateful recovery requirements must include interruption/fault testing.

## 32. Assumptions

This draft assumes:

- `SCP-001`, `PER-001`, `UCD-001`, and `PRD-001` retain their current approved/draft direction;
- Hermes and Codex remain the first adapters;
- the MVP remains local, single-node, and non-public;
- one organization with multiple workspaces is sufficient;
- an approved identity and secret mechanism can be selected;
- adapters expose enough information for useful state mapping;
- artifact and audit storage can provide required durability;
- the first users are technically capable;
- named reviewers will be assigned before approval.

## 33. Constraints

- no application behavior is claimed to exist;
- architecture choices remain open;
- product scope cannot expand silently;
- secrets and local research evidence remain outside ordinary tracked content;
- production financial posting and autonomous merge remain excluded;
- accepted workflows cannot depend silently on mock data;
- accessibility is a first-order acceptance condition;
- implementation must preserve provider/agent replaceability;
- Git/document approval remains explicit.

## 34. Risks

| Risk | Consequence | Response |
|---|---|---|
| Too many Must requirements | MVP delay | Validate first vertical slice and release sequencing |
| Requirements duplicate architecture | Premature lock-in | Keep implementation technology deferred |
| Approval semantics remain vague | Unsafe execution | Complete AUT-001 and APR-001 before consequential tools |
| Adapter capability mismatch | Inconsistent behavior | Conformance contract and explicit unavailable states |
| Recovery without idempotency | Duplicate side effects | Block unsafe retry/resume |
| Memory scope ambiguity | Leakage or contamination | Complete MEM/DAT/SEC baselines |
| UI outruns persistence | Mock-driven product | Require source/evidence for every status |
| Cost data delay | False budget view | Explicit pending/unavailable states |
| Local operations neglected | Lost pilot data | Backup/restore and health Must requirements |
| Requirement traceability drift | Unverifiable implementation | RTM and quality gates |

## 34A. ADR-003 functional baseline

The functional requirements must define resource relationships and authorization for `workspace`, `project`, `mission`, `task`, `conversation`, `run`, `artifact`, and `memory`. Conversation visibility must be explicit and enforced on reads, writes, search, notifications, exports, derived memory, and artifacts. The system must classify actions by risk and require exact approvals according to the approved policy. The initial adapter journey must cover Codex, Hermes, and Claude Code.

## 35. Open decisions

1. Which local identity implementation will satisfy `FR-AUTH-*`?
2. What is the exact predefined role permission matrix?
3. Which Hermes and Codex integration modes are permitted?
4. Which model providers are included in pilot acceptance?
5. What is the minimum approved tool set?
6. Which filesystem/repository writes are allowed without per-action approval?
7. Are Git commit and PR creation executable after approval or proposal-only in the MVP?
8. Which artifact size/type limits apply?
9. Which memory record types allow automatic write?
10. Which audit events are mandatory enough to block consequential execution on ingestion failure?
11. Which interruption scenarios support resume versus safe restart?
12. Which mobile approvals, if any, are permitted?
13. What backup scope and recovery-point target apply?
14. Which state-staleness thresholds apply?
15. Which requirements may move from Must to Should without invalidating the MVP?

## 36. SRS acceptance criteria

SRS-001 may advance to version `1.0.0` when:

1. Product Owner confirms that requirements represent the approved MVP;
2. Architecture confirms that requirements are implementable and technology-neutral;
3. Security confirms that authority, approval, workspace, tool, memory, and audit behavior is sufficiently specified for downstream design;
4. Quality confirms that every Must requirement is testable;
5. every requirement has a stable identifier and required metadata;
6. no requirement claims implementation;
7. conflicts with VSN/SCP/PRD/UCD are resolved or recorded;
8. deferred topics are assigned to explicit documents;
9. the initial RTM can map every Must requirement;
10. metadata, links, terminology, Markdown, and validation checks pass.

## 37. Downstream traceability

| Requirement domain | Downstream documents |
|---|---|
| `AUTH`, `WSP` | `IAM-001`, `SEC-001`, `DDD-001`, `DAT-001`, `API-001` |
| `AGT`, `MOD` | `SAD-001`, `INT-001`, `AGC-001`, `CAP-001`, `MOD-001` |
| `TSK`, `RUN` | `ORC-001`, `RUN-001`, `EVT-001`, `API-001` |
| `APR` | `AUT-001`, `APR-001`, `SEC-001`, `THR-001` |
| `TOL` | `INT-001`, `POL-001`, `SAN-001`, `MCP-001` |
| `MEM` | `MEM-001`, `DAT-001`, `SEC-001` |
| `ART` | `ART-001`, `DAT-001`, `API-001` |
| `AUD` | `AUD-001`, `OBS-001`, `SEC-001` |
| `CST` | `CST-001`, `OBS-001`, `FIN-001` |
| `UI` | `UXA-001`, `DSN-001`, `A11Y-001`, `VVR-001` |
| `OPS` | `DEP-001`, `OPS-001`, `BCP-001` |
| All | `NFR-001`, `TST-001`, `QAG-001`, `RTM-001` |

## 38. Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.1.0`
- Approved by: Product Owner under explicit user authorization to finalize the declared scope
- Approval date: not applicable
- Finalization note: approval records the documentation baseline only; implementation and verification remain separate evidence gates

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial functional specification with 89 testable requirements across identity, workspaces, adapters, tasks, runs, approvals, tools, memory, artifacts, audit, cost, UI, and operations | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `PER-001` — Personas and Jobs to Be Done
- `UCD-001` — User Journeys and Use Cases
- `PRD-001` — Product Requirements Document
