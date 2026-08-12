---
document_id: UCD-001
title: Agent OS User Journeys and Use Cases
version: 0.2.0
status: draft
owner: product-owner
approvers:
  - product-owner
  - ux-accessibility-owner
  - architecture-owner
  - security-owner
created: 2026-07-19
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PER-001
  - PRD-001
  - SRS-001
  - NFR-001
  - AUT-001
  - IAM-001
  - UXA-001
  - A11Y-001
  - TST-001
related_adrs: []
related_evidence:
  - VIDEO-002
  - VIDEO-003
---

# UCD-001 — Agent OS User Journeys and Use Cases

> **Status: Draft.** This document defines proposed journeys and use cases for the first Agent OS pilot. It does not prove implementation, usability, security, or product-market fit. All journeys must be validated through requirements review, prototype testing, security analysis, and implementation evidence.

## 1. Document purpose

This document translates the approved vision, proposed scope, personas, and Jobs to Be Done into concrete user journeys and use cases.

It defines:

- who performs each journey;
- what outcome the user expects;
- preconditions and permissions;
- the main success path;
- alternate and failure paths;
- approval and security implications;
- accessibility expectations;
- measurable completion criteria;
- dependencies on future requirements, architecture, security, and test documents.

It is a primary input to:

- `PRD-001`;
- `SRS-001`;
- `NFR-001`;
- `AUT-001`;
- `IAM-001`;
- `UXA-001`;
- `SAD-001`;
- `TST-001`;
- `RTM-001`.

## 2. Scope

This document covers the first local Agent OS pilot:

- one organization context;
- one primary operator or a small trusted team;
- multiple isolated workspaces;
- local Linux/WSL deployment;
- responsive web Mission Control;
- Hermes and Codex as initial adapter targets;
- bounded tasks and durable runs;
- human approval for consequential actions;
- permission-aware memory;
- artifact storage and provenance;
- audit and cost attribution;
- backup and recovery foundations.

It excludes:

- public multi-tenant SaaS;
- anonymous users;
- public internet exposure by default;
- unrestricted host control;
- production financial posting;
- autonomous commit, push, pull-request creation, or merge;
- unrestricted external messaging;
- full media Studio;
- multi-agent swarms;
- high-availability deployment.

## 3. Relationship to personas and scope

This document uses the following primary personas from `PER-001`:

- `PERS-001` — Builder-Operator;
- `PERS-002` — Product / Workspace Owner;
- `PERS-003` — Technical Operator / Platform Administrator;
- `PERS-004` — Reviewer / Approver;
- `PERS-005` — Auditor / Assurance Reviewer;
- `PERS-006` — Contributor / Artifact Consumer.

It uses the MVP and trust boundaries proposed in `SCP-001`.

Where this document conflicts with an approved source, the approved source prevails.

## 4. Evidence and confidence labels

The following labels apply throughout this document:

| Label | Meaning |
|---|---|
| `SUPPORTED` | Consistent with approved vision and scope |
| `PROPOSED` | Product or UX hypothesis requiring review |
| `NOT CONFIRMED` | Important but not validated by direct evidence |
| `FUTURE` | Outside the first MVP |
| `REJECTED` | Inconsistent with approved principles or scope |

The research videos are discovery inputs only. They do not prove persistence, authorization, safe autonomy, business accuracy, or production readiness.

## 5. Journey design principles

1. **State before decoration:** every visible status must correspond to persisted or explicitly classified state.
2. **Boundaries are visible:** workspace, project, agent, model, tool, and approval scope must be understandable.
3. **Approval is exact:** a reviewer sees the precise action and parameters.
4. **Failure is actionable:** every failure state should explain what happened, what is known, and what can be done next.
5. **Recovery is first-class:** interrupted work must have clear resume, retry, cancel, or investigate paths.
6. **Source and provenance travel with outputs:** artifacts and memory never become detached from origin.
7. **Security is not hidden:** permission denial and policy decisions are visible enough to support correction.
8. **Progressive disclosure:** simple summaries are available first, with technical evidence on demand.
9. **Accessibility is built in:** keyboard, screen reader, contrast, focus, and responsive behavior are acceptance concerns.
10. **No implicit authority from prompts:** natural language cannot bypass policy.

## 6. Journey catalogue

| Journey ID | Title | Primary persona | Priority |
|---|---|---|---|
| `JRN-001` | First local onboarding | Builder-Operator / Technical Operator | Must |
| `JRN-002` | Create an organization context and workspace | Workspace Owner | Must |
| `JRN-003` | Register and verify an agent adapter | Technical Operator | Must |
| `JRN-004` | Configure a model profile and provider | Technical Operator | Must |
| `JRN-005` | Create a bounded task | Builder-Operator | Must |
| `JRN-006` | Start and monitor a run | Builder-Operator | Must |
| `JRN-007` | Handle an approval-required action | Approver / Builder-Operator | Must |
| `JRN-008` | Reject and revise an approval request | Approver / Builder-Operator | Must |
| `JRN-009` | Recover an interrupted run | Builder-Operator / Technical Operator | Must |
| `JRN-010` | Retrieve and review an artifact | Builder-Operator / Contributor | Must |
| `JRN-011` | Store and retrieve governed memory | Builder-Operator / Auditor | Must |
| `JRN-012` | Inspect cost and usage attribution | Owner / Builder-Operator | Must |
| `JRN-013` | Audit a task from instruction to outcome | Auditor | Must |
| `JRN-014` | Verify workspace isolation | Owner / Auditor | Must |
| `JRN-015` | Back up and restore the local pilot | Technical Operator | Must |
| `JRN-016` | Diagnose adapter or provider failure | Technical Operator | Must |
| `JRN-017` | Cancel a running or waiting run | Builder-Operator | Must |
| `JRN-018` | Review Mission Control state integrity | Owner / Auditor | Must |
| `JRN-019` | Manage workspace members and roles | Workspace Owner | Should |
| `JRN-020` | Export authorized evidence | Auditor / Owner | Should |
| `JRN-F01` | Remote trusted-team access | Future | Future |
| `JRN-F02` | Multi-agent delegation | Future | Future |
| `JRN-F03` | Read-only business analytics | Future | Future |

## 7. Common interaction states

The product should use a controlled set of state semantics.

### 7.1 Task states

- draft;
- ready;
- blocked;
- active;
- completed;
- cancelled;
- archived.

### 7.2 Run states

- queued;
- starting;
- running;
- waiting-for-approval;
- waiting-for-resource;
- paused;
- retrying;
- failed;
- cancelled;
- completed;
- stale;
- unknown.

### 7.3 Approval states

- requested;
- under-review;
- approved;
- rejected;
- revision-requested;
- expired;
- cancelled;
- consumed;
- invalidated.

### 7.4 Artifact states

- generated;
- under-review;
- accepted;
- rejected;
- superseded;
- archived;
- deleted;
- unavailable.

### 7.5 Source-confidence states

- authoritative;
- verified;
- user-approved;
- generated;
- inferred;
- stale;
- unknown;
- unavailable.

Final state models belong in `SRS-001`, `RUN-001`, `APR-001`, and `ART-001`.

## 8. Common preconditions

Unless a use case states otherwise:

- the local Agent OS service is running;
- the user is authenticated;
- the user has access to the selected organization and workspace;
- the workspace exists;
- relevant adapters or tools are registered and healthy;
- required secrets are referenced through an approved mechanism;
- the action is allowed by current policy;
- the UI displays the active workspace and project context.

## 9. Common postconditions

A successful consequential use case should produce:

- persisted state;
- user-visible confirmation;
- correlated audit event;
- task/run/step linkage;
- identity attribution;
- timestamp;
- related artifact or approval reference where applicable;
- error or warning record if the result is partial;
- no silent cross-workspace side effect.

## 10. JRN-001 — First local onboarding

### 10.1 Objective

Help a primary operator initialize the local pilot safely and understand its non-production boundaries.

### 10.2 Primary actors

- `PERS-001` Builder-Operator;
- `PERS-003` Technical Operator.

### 10.3 Preconditions

- Agent OS is installed locally;
- the user can access the local web interface;
- no organization context exists;
- Hermes and Codex availability may be unknown.

### 10.4 Main journey

1. The user opens Agent OS.
2. The system states that the installation is local and not production-ready by default.
3. The user creates the first organization context.
4. The user creates the first workspace.
5. The user reviews the workspace boundary and default permissions.
6. The system checks local service health.
7. The user registers or verifies Hermes.
8. The user registers or verifies Codex.
9. The system presents adapter health and capability status.
10. The user configures one model/provider profile through a secret reference.
11. The user runs a safe diagnostic task.
12. The system stores the run and output artifact.
13. The user reviews the execution trace.
14. The user reviews the approval model.
15. The system prompts the user to confirm backup guidance.
16. The onboarding completes.

### 10.5 Alternate paths

- Adapter unavailable: continue with one adapter but mark the second adapter requirement incomplete.
- Provider credential missing: continue without provider execution and show configuration guidance.
- Health check fails: onboarding enters a recoverable blocked state.
- Storage unavailable: stop before accepting the pilot as initialized.

### 10.6 Failure behavior

The system must not:

- mark onboarding complete when persistence fails;
- expose secret values;
- claim an adapter is functional based only on successful registration;
- treat a failed diagnostic as success.

### 10.7 Completion criteria

- organization and workspace are persisted;
- at least one adapter health check is visible;
- diagnostic task state survives refresh;
- user can find the resulting artifact;
- user can identify where approvals appear;
- backup guidance is accessible.

## 11. JRN-002 — Create an organization context and workspace

### Objective

Create a durable isolation boundary for projects, members, policies, artifacts, memory, and cost.

### Main journey

1. Workspace Owner selects “Create workspace.”
2. The system requests a name, purpose, classification, and default policy profile.
3. The user reviews isolation rules.
4. The user optionally creates a first project.
5. The system assigns the user as Workspace Owner.
6. The workspace is persisted.
7. Mission Control displays the new workspace with empty-state guidance.

### Alternate paths

- Duplicate name: allow with distinct identifier or request clarification.
- Invalid classification/policy combination: block and explain.
- Persistence failure: do not display a successful workspace card.

### Acceptance conditions

- workspace has stable identifier;
- organization and owner linkage are stored;
- no data from another workspace appears;
- audit event records creation;
- empty states are accessible and actionable.

## 12. JRN-003 — Register and verify an agent adapter

### Objective

Register Hermes or Codex through a controlled adapter without granting unrestricted authority.

### Main journey

1. Technical Operator opens the agent registry.
2. User selects adapter type.
3. System displays required configuration and permissions.
4. User configures executable/API reference without embedding secrets.
5. System performs a read-only availability check.
6. System queries declared capabilities where supported.
7. System stores adapter registration and version.
8. System labels unsupported capabilities as unavailable or unknown.
9. Operator enables the adapter for selected workspaces.
10. Audit event records the configuration change.

### Alternate paths

- binary/API unavailable;
- version incompatible;
- capability discovery unsupported;
- adapter reports healthy but test run fails;
- workspace authorization denied.

### Security rules

- registration does not grant filesystem/network/secret access;
- adapter must not be enabled globally by default;
- secret values must never be displayed;
- health must distinguish “registered,” “reachable,” and “validated.”

### Acceptance conditions

- exact adapter identity and version are recorded;
- health status is evidence-backed;
- workspace enablement is explicit;
- unsupported capability is not advertised as supported.

## 13. JRN-004 — Configure a model profile and provider

### Objective

Create a provider-neutral model profile with visible privacy, capability, latency, and budget characteristics.

### Main journey

1. Technical Operator opens Model Profiles.
2. User selects a provider adapter.
3. User creates a logical profile name.
4. User selects or enters the provider model identifier.
5. User declares intended capabilities and constraints.
6. User sets budget and usage limits.
7. User links an approved secret reference.
8. System performs a safe validation request if enabled.
9. System stores validation result, timestamp, and limitations.
10. User enables the profile for selected workspaces.

### Failure paths

- provider authentication failure;
- model unavailable;
- usage endpoint unavailable;
- cost data delayed;
- profile requests prohibited data class;
- validation request rejected by policy.

### Acceptance conditions

- profile is not treated as validated when test fails;
- actual model/provider used by future runs can be recorded;
- secret is referenced, not stored in ordinary content;
- workspace scope is explicit.

## 14. JRN-005 — Create a bounded task

### Objective

Define a task with explicit outcome, resources, limits, and risk context.

### Main journey

1. Builder-Operator selects workspace and project.
2. User creates a new task.
3. User defines desired outcome.
4. User selects permitted resources.
5. User selects preferred agent or allows policy-based routing.
6. User sets model/budget/time/retry limits.
7. User reviews tool and data permissions.
8. User identifies expected artifacts.
9. System summarizes approval implications.
10. User saves as draft or marks ready.
11. System persists the task and creates an audit event.

### Validation rules

Task cannot become ready when:

- workspace is missing;
- requested resource is outside scope;
- no permitted agent can perform the task;
- required approval policy is unresolved;
- task requests excluded data class;
- limits are absent where policy requires them.

### Acceptance conditions

- task has stable identifier;
- outcome and limits are visible;
- task survives refresh;
- task cannot silently gain permissions later;
- user can compare draft versus ready state.

## 15. JRN-006 — Start and monitor a run

### Objective

Execute a ready task through a selected adapter while preserving durable state.

### Main journey

1. Builder-Operator opens a ready task.
2. System performs preflight:
   - user authority;
   - workspace policy;
   - adapter health;
   - model profile;
   - tool scopes;
   - budget;
   - approval prerequisites.
3. User starts the run.
4. System creates persisted run and initial step.
5. Adapter receives bounded execution request.
6. Mission Control updates from persisted events.
7. User sees current state, elapsed time, cost, and active agent.
8. System records produced steps, tool requests, warnings, and outputs.
9. Run reaches terminal or waiting state.
10. System generates execution receipt.
11. Artifacts are linked.
12. User reviews completion evidence.

### Alternate paths

- adapter unavailable before start;
- budget exceeded;
- provider unavailable;
- approval required;
- worker loses heartbeat;
- tool denied;
- output partial;
- cancellation requested;
- final state unknown.

### Acceptance conditions

- refresh does not erase run state;
- no success is shown without terminal evidence;
- waiting-for-approval is distinct from running;
- unknown and stale states are visible;
- actual provider/model are shown where known.

## 16. JRN-007 — Handle an approval-required action

### Objective

Allow an authorized reviewer to make an informed decision on an exact consequential action.

### Main journey

1. A run proposes a consequential action.
2. Policy classifies the action.
3. System blocks execution.
4. System creates an approval request containing:
   - requester identity;
   - task/run/step;
   - exact action and parameters;
   - target resource;
   - risk class;
   - reason approval is required;
   - preview/diff where applicable;
   - expiry;
   - expected side effects.
5. Authorized approver receives the request.
6. Approver reviews summary and technical details.
7. Approver approves.
8. System validates that the proposal has not materially changed.
9. System marks approval consumed for the exact action.
10. Execution proceeds.
11. Result is recorded and shown to requester and approver.

### Failure and alternate paths

- approver lacks authority;
- request expired;
- target changed;
- parameters changed;
- policy changed;
- duplicate approval attempt;
- action fails after approval;
- approval service unavailable.

### Acceptance conditions

- approval is exact and time-bounded;
- changed action requires new approval;
- execution without approval is impossible;
- approval and execution are correlated;
- failure after approval does not imply successful side effect.

## 17. JRN-008 — Reject and revise an approval request

### Objective

Support safe rejection and correction instead of pressuring approvers toward acceptance.

### Main journey

1. Approver opens a request.
2. Approver identifies insufficient scope or excessive risk.
3. Approver rejects or requests revision.
4. System blocks the action.
5. Builder-Operator receives reason and context.
6. User revises task/action.
7. System invalidates the old request.
8. System generates a new request for materially changed parameters.
9. Approver reviews and decides again.

### Acceptance conditions

- rejected request cannot be reused;
- reason is preserved;
- revised action has a new immutable request identity;
- system distinguishes reject from revision-requested;
- no hidden side effect occurs before approval.

## 18. JRN-009 — Recover an interrupted run

### Objective

Diagnose and safely continue work after process, adapter, provider, machine, or network interruption.

### Main journey

1. System detects missing heartbeat or interruption.
2. Run enters stale, paused, failed, or unknown state based on evidence.
3. User opens recovery view.
4. System shows:
   - last persisted step;
   - last known side effect;
   - checkpoint availability;
   - retry eligibility;
   - approval validity;
   - adapter/provider status.
5. User chooses resume, retry, cancel, or investigate.
6. System revalidates permissions, budget, and approvals.
7. System prevents duplicate side effects through idempotency or explicit confirmation.
8. Execution continues or terminates.
9. Recovery result is recorded.

### Failure paths

- checkpoint corrupt;
- side effect status unknown;
- approval expired;
- provider session unrecoverable;
- resource changed;
- retry unsafe.

### Acceptance conditions

- system never claims resume safety when unknown;
- unsafe retry is blocked;
- user sees last reliable state;
- recovered run keeps same lineage;
- duplicate side effects are prevented or explicitly surfaced.

## 19. JRN-010 — Retrieve and review an artifact

### Objective

Find the correct output with provenance, status, permissions, and lifecycle information.

### Main journey

1. User opens workspace artifacts.
2. User filters by project, task, run, type, status, or date.
3. User opens an artifact.
4. System shows:
   - title and media type;
   - producer;
   - task/run source;
   - version;
   - integrity metadata;
   - lifecycle state;
   - classification;
   - preview safety status.
5. User previews or downloads if authorized.
6. User may accept, reject, comment, supersede, or archive based on role.
7. Action is recorded.

### Failure paths

- binary missing;
- preview unsafe;
- user lacks permission;
- artifact superseded;
- integrity mismatch;
- retention period expired.

### Acceptance conditions

- wrong-workspace artifacts are not discoverable;
- superseded status is prominent;
- unavailable artifact is not shown as downloadable;
- provenance is understandable;
- preview does not execute unsafe content.

## 20. JRN-011 — Store and retrieve governed memory

### Objective

Preserve useful context without turning unverified agent output into authoritative truth.

### Main journey

1. User or run proposes a memory record.
2. System captures source, scope, classification, author/producer, and confidence.
3. Policy determines whether automatic storage is permitted.
4. Record is stored in workspace scope.
5. Later task requests relevant memory.
6. Retrieval applies workspace permissions and relevance rules.
7. System provides source, age, and reason for inclusion.
8. User may correct, supersede, or delete within policy.
9. Changes are recorded.

### Alternate paths

- memory contains secret;
- source unavailable;
- record conflicts with authoritative source;
- cross-workspace result attempted;
- retention expired;
- user correction denied.

### Acceptance conditions

- secret content is not stored as ordinary memory;
- generated hypothesis remains labeled;
- cross-workspace retrieval is denied;
- corrections preserve history where required;
- retrieval is auditable where practical.

## 21. JRN-012 — Inspect cost and usage attribution

### Objective

Understand provider/model/tool usage and attributed cost without confusing estimates with authoritative billing.

### Main journey

1. Owner opens Cost and Usage.
2. User selects period, workspace, project, task, or run.
3. System displays usage events and available provider records.
4. System labels values as:
   - provider-reported;
   - calculated;
   - estimated;
   - pending;
   - unavailable.
5. User drills into a run.
6. System shows model, token/tool usage, currency, and timestamp.
7. User exports authorized report if needed.

### Failure paths

- provider usage delayed;
- exchange rate unavailable;
- unattributed event;
- tool cost unknown;
- reconciliation mismatch.

### Acceptance conditions

- estimated values are visibly labeled;
- values can be traced to events;
- unattributed costs are not hidden;
- business profit is not inferred from provider spend;
- source and freshness are shown.

## 22. JRN-013 — Audit a task from instruction to outcome

### Objective

Reconstruct what happened and identify evidence gaps.

### Main journey

1. Auditor opens Audit.
2. Auditor filters by workspace/task/run.
3. System presents correlated timeline:
   - identity;
   - task creation;
   - policy decisions;
   - adapter/model selection;
   - run steps;
   - tool calls;
   - approvals;
   - artifacts;
   - costs;
   - failures/retries;
   - terminal state.
4. Auditor opens evidence details.
5. System distinguishes persisted fact, provider report, derived estimate, and missing data.
6. Auditor exports authorized evidence package.
7. Export event is recorded.

### Acceptance conditions

- audit is read-only;
- missing evidence is visible;
- correlation identifiers are stable;
- secret values are redacted;
- one workspace does not expose another;
- export content is access-controlled.

## 23. JRN-014 — Verify workspace isolation

### Objective

Demonstrate that data, memory, artifacts, tools, and permissions do not cross workspace boundaries by default.

### Main journey

1. Owner creates Workspace A and Workspace B.
2. Separate projects and artifacts are created.
3. User with access only to Workspace A searches for B content.
4. System denies or omits B content.
5. Agent in Workspace A requests B resource.
6. Policy denies the request.
7. Audit records the denial without exposing protected content.
8. Authorized auditor reviews the evidence.

### Acceptance conditions

- no metadata leak beyond allowed denial information;
- search, memory, artifact, tool, and cost paths are covered;
- negative tests pass;
- denial does not reveal secret paths or titles;
- cross-workspace access requires explicit future policy.

## 24. JRN-015 — Back up and restore the local pilot

### Objective

Restore retained service and data from an approved backup scenario.

### Main journey

1. Technical Operator opens Operations.
2. System displays backup status and last successful backup.
3. Operator creates or verifies a backup.
4. System records backup metadata and integrity check.
5. In a controlled recovery exercise, service is stopped.
6. Operator restores configuration references and retained data.
7. System starts in recovery mode.
8. Integrity and schema checks run.
9. Operator verifies workspaces, tasks, runs, approvals, artifacts, and audit records.
10. Recovery evidence is stored.

### Failure paths

- backup missing;
- integrity failure;
- schema incompatible;
- artifact binary missing;
- secret reference unavailable;
- restore partially succeeds.

### Acceptance conditions

- partial restore is not shown as complete;
- secrets are not embedded in backup documentation;
- recovery target is measured;
- lost or unavailable data is listed;
- exercise is repeatable.

## 25. JRN-016 — Diagnose adapter or provider failure

### Objective

Identify whether a failure belongs to Agent OS, adapter, provider, configuration, permission, or network.

### Main journey

1. Technical Operator opens health diagnostics.
2. System displays component status separately:
   - control plane;
   - adapter process/API;
   - provider authentication;
   - capability check;
   - tool gateway;
   - storage;
   - event pipeline.
3. Operator selects a failing component.
4. System shows last check, evidence, and safe remediation.
5. Operator retries a read-only diagnostic.
6. Result is recorded.

### Acceptance conditions

- “healthy” is not inferred from registration alone;
- provider error is not mislabeled as platform success;
- remediation avoids exposing secrets;
- diagnostics do not perform consequential actions;
- stale checks are labeled.

## 26. JRN-017 — Cancel a running or waiting run

### Objective

Allow the user to stop future work while accurately reporting what may already have happened.

### Main journey

1. User opens active run.
2. User selects Cancel.
3. System displays expected cancellation semantics.
4. User confirms.
5. System records cancellation intent.
6. Orchestrator stops pending work where possible.
7. Adapter cancellation is requested.
8. Tool actions already completed remain recorded.
9. Run reaches cancelled, failed, or unknown terminal state.
10. System explains remaining uncertainty.

### Acceptance conditions

- cancellation does not erase evidence;
- completed side effects are not reversed silently;
- unknown adapter state remains visible;
- no new steps begin after enforceable cancellation;
- approval requests are cancelled or invalidated as appropriate.

## 27. JRN-018 — Review Mission Control state integrity

### Objective

Ensure the dashboard reflects real persisted state and distinguishes uncertainty.

### Main journey

1. Owner opens Mission Control.
2. System displays counts and active items from persisted sources.
3. User drills into one KPI.
4. Underlying records match the displayed summary.
5. Stale data shows timestamp and warning.
6. Unknown or failed collection is not converted to zero.
7. User can navigate to supporting evidence.

### Acceptance conditions

- dashboard cards are traceable;
- mock data is never silently mixed with real data;
- zero, unavailable, and unknown are distinct;
- last-updated time is visible;
- summary and detail agree.

## 28. JRN-019 — Manage workspace members and roles

### Objective

Assign least-privilege access within one workspace.

### Main journey

1. Workspace Owner opens Members.
2. Owner invites or selects a trusted user.
3. Owner assigns a predefined role.
4. System shows permissions and sensitive capabilities.
5. Owner confirms.
6. Membership is persisted.
7. New user receives only selected workspace access.
8. Audit records the change.

### Failure paths

- duplicate membership;
- owner removes their own last-owner role;
- user assigned incompatible role;
- identity unavailable;
- permission escalation requires approval.

### Acceptance conditions

- role effects are understandable;
- membership change is auditable;
- no implicit access to other workspaces;
- last required owner cannot be removed without transfer.

## 29. JRN-020 — Export authorized evidence

### Objective

Create a bounded evidence package for review without exposing unrelated or secret data.

### Main journey

1. Authorized user selects task, run, or period.
2. User selects export scope.
3. System previews included record types.
4. Policy validates access and classification.
5. System generates package with manifest.
6. Secrets and prohibited fields are redacted.
7. Integrity metadata is included.
8. Export is recorded.

### Acceptance conditions

- package scope is explicit;
- unrelated workspace data is excluded;
- redaction is deterministic and testable;
- export failure is visible;
- generated package is itself an artifact with provenance.

## 30. Future journeys

### JRN-F01 — Remote trusted-team access

Requires approved identity, encrypted transport, exposure design, rate limiting, session policy, incident response, and threat-model update.

### JRN-F02 — Multi-agent delegation

Requires reliable single-agent execution, explicit delegation contract, budget partitioning, loop prevention, provenance, and human-control rules.

### JRN-F03 — Read-only business analytics

Requires authorized source systems, metric definitions, freshness, reconciliation, generated-analysis labels, and named data owners.

## 31. Use case catalogue

| Use Case ID | Title |
|---|---|
| `UC-001` | Authenticate locally |
| `UC-002` | Create organization context |
| `UC-003` | Create workspace |
| `UC-004` | Create project |
| `UC-005` | Register agent adapter |
| `UC-006` | Validate adapter health |
| `UC-007` | Create model profile |
| `UC-008` | Create bounded task |
| `UC-009` | Start run |
| `UC-010` | View run timeline |
| `UC-011` | Request approval |
| `UC-012` | Approve exact action |
| `UC-013` | Reject approval |
| `UC-014` | Revise approval request |
| `UC-015` | Cancel run |
| `UC-016` | Retry run step |
| `UC-017` | Resume interrupted run |
| `UC-018` | Store artifact |
| `UC-019` | Retrieve artifact |
| `UC-020` | Store memory record |
| `UC-021` | Retrieve memory |
| `UC-022` | Correct or supersede memory |
| `UC-023` | Record audit event |
| `UC-024` | View cost attribution |
| `UC-025` | Manage workspace membership |
| `UC-026` | Assign workspace role |
| `UC-027` | Deny cross-workspace access |
| `UC-028` | Create backup |
| `UC-029` | Restore backup |
| `UC-030` | Export evidence package |
| `UC-031` | Diagnose adapter failure |
| `UC-032` | Review dashboard integrity |
| `UC-033` | Revoke future authority |
| `UC-034` | Expire approval |
| `UC-035` | Mark state stale or unknown |

## 32. UC-001 — Authenticate locally

**Primary actor:** Authorized user  
**Priority:** Must

### Preconditions

- local service available;
- identity is configured.

### Trigger

User opens Agent OS or accesses a protected route.

### Main success path

1. System requests authentication.
2. User presents approved credentials.
3. System verifies identity.
4. System creates bounded session.
5. User enters authorized organization/workspace view.

### Failure behavior

- invalid credentials: deny without revealing account details;
- expired session: require reauthentication;
- identity service unavailable: do not grant fallback anonymous access.

### Acceptance criteria

- every protected route requires authenticated identity;
- session expiry is enforced;
- audit records successful and failed security-relevant events appropriately;
- secrets are not logged.

## 33. UC-003 — Create workspace

**Primary actor:** Workspace Owner  
**Priority:** Must

### Preconditions

- authenticated user;
- organization context exists;
- user has workspace-creation authority.

### Main success path

1. User submits valid workspace data.
2. System validates policy profile and classification.
3. System creates stable workspace identifier.
4. System assigns owner role.
5. System stores audit event.
6. System displays workspace.

### Failure behavior

- validation error: no partial workspace;
- persistence error: no success state;
- authorization error: deny and audit.

### Acceptance criteria

- workspace is isolated;
- owner linkage exists;
- duplicate request is idempotent where practical;
- workspace appears after refresh.

## 34. UC-005 — Register agent adapter

**Primary actor:** Technical Operator  
**Priority:** Must

### Main success path

1. User submits adapter configuration.
2. System validates type and version format.
3. System stores configuration without raw secrets.
4. System performs safe reachability check.
5. System stores health evidence.
6. User scopes adapter to workspaces.

### Acceptance criteria

- adapter registration and health are separate states;
- raw secrets are absent from persisted ordinary fields;
- unsupported capabilities remain unavailable;
- change is auditable.

## 35. UC-008 — Create bounded task

**Primary actor:** Builder-Operator  
**Priority:** Must

### Required fields

- workspace;
- project or explicit no-project state;
- title;
- desired outcome;
- permitted resources;
- agent/routing policy;
- limits;
- expected artifact;
- data classification;
- approval context.

### Acceptance criteria

- task cannot become ready without mandatory fields;
- limits are persisted;
- permissions cannot be broadened through free text;
- task changes are versioned or auditable.

## 36. UC-009 — Start run

**Primary actor:** Builder-Operator  
**Priority:** Must

### Preconditions

- task ready;
- user authorized;
- adapter and model profile permitted;
- budget available;
- policy preflight passes.

### Main success path

1. System creates run before external execution.
2. System records immutable run identity.
3. System records selected adapter/profile.
4. System dispatches bounded request.
5. System receives or polls execution events.
6. System updates persisted state.

### Acceptance criteria

- external execution does not begin before run persistence;
- duplicate start does not create uncontrolled duplicate run;
- preflight failure prevents dispatch;
- run state is traceable.

## 37. UC-011 — Request approval

**Primary actor:** System / Run  
**Priority:** Must

### Preconditions

- proposed action classified as approval-required;
- no valid approval exists.

### Main success path

1. System records exact proposed action.
2. System identifies eligible approver scope.
3. System creates request with expiry.
4. Run enters waiting-for-approval.
5. Notification/inbox entry is created.

### Acceptance criteria

- action is blocked;
- request contains exact parameters;
- eligible approvers are policy-derived;
- request cannot approve a different action.

## 38. UC-012 — Approve exact action

**Primary actor:** Approver  
**Priority:** Must

### Preconditions

- authenticated approver;
- valid request;
- delegated authority;
- request not expired.

### Main success path

1. Approver reviews request.
2. Approver confirms.
3. System revalidates policy and parameters.
4. Approval is persisted.
5. Approval is consumed by exact action.
6. Execution result is linked.

### Acceptance criteria

- approval is immutable once consumed;
- material change invalidates approval;
- double consumption is prevented;
- failed execution remains failed even if approval existed.

## 39. UC-015 — Cancel run

**Primary actor:** Builder-Operator  
**Priority:** Must

### Acceptance criteria

- cancellation intent persists;
- no new dispatch occurs after enforceable cancellation;
- completed side effects remain visible;
- final state may be unknown when adapter confirmation is absent;
- cancellation is auditable.

## 40. UC-017 — Resume interrupted run

**Primary actor:** Builder-Operator / Technical Operator  
**Priority:** Must

### Preconditions

- interruption detected;
- run is resumable;
- checkpoint or safe continuation exists;
- policy and approvals remain valid.

### Acceptance criteria

- resume is blocked when side-effect state is unknown and unsafe;
- resumed steps retain lineage;
- duplicate side effects are prevented;
- expired approval requires renewal.

## 41. UC-018 — Store artifact

**Primary actor:** Run / User  
**Priority:** Must

### Required metadata

- artifact identifier;
- workspace;
- task/run/step;
- producer;
- media type;
- size;
- integrity hash;
- classification;
- lifecycle state;
- storage reference;
- created timestamp.

### Acceptance criteria

- binary and metadata failures are not reported as complete;
- unsafe preview is disabled;
- unauthorized workspace cannot retrieve metadata or content;
- artifact lineage is preserved.

## 42. UC-020 — Store memory record

**Primary actor:** Run / User  
**Priority:** Must

### Acceptance criteria

- source and scope are mandatory;
- secret classification blocks ordinary storage;
- generated content is labeled;
- policy controls automatic writes;
- correction/deletion path exists.

## 43. UC-024 — View cost attribution

**Primary actor:** Owner / Builder-Operator  
**Priority:** Must

### Acceptance criteria

- each supported usage event links to workspace/task/run;
- estimates and provider-reported values are distinct;
- missing cost is visible;
- currency and period are shown;
- user cannot infer official profit from model spend view.

## 44. UC-027 — Deny cross-workspace access

**Primary actor:** System  
**Priority:** Must

### Trigger

A user, agent, tool, search, memory, or artifact request targets a workspace outside authorized scope.

### Main success path

1. System evaluates scope.
2. System denies request.
3. System returns safe error.
4. System records security-relevant event.
5. Protected data remains undisclosed.

### Acceptance criteria

- no title/path/content leak;
- denial applies to metadata and content;
- negative tests cover every access path;
- denial cannot be overridden by prompt.

## 45. UC-028 — Create backup

**Primary actor:** Technical Operator  
**Priority:** Must

### Acceptance criteria

- backup manifest identifies included data classes;
- integrity check is recorded;
- raw secrets are excluded or separately protected;
- failure is visible;
- retention policy applies.

## 46. UC-029 — Restore backup

**Primary actor:** Technical Operator  
**Priority:** Must

### Acceptance criteria

- restore validates schema and integrity;
- partial restore is labeled;
- restored state can be reconciled;
- recovery time is measured;
- audit/evidence is retained where feasible.

## 47. UC-031 — Diagnose adapter failure

**Primary actor:** Technical Operator  
**Priority:** Must

### Acceptance criteria

- check is read-only;
- component boundary is identified;
- stale diagnostics are labeled;
- secret values remain redacted;
- corrective action is specific and safe.

## 48. UC-032 — Review dashboard integrity

**Primary actor:** Owner / Auditor  
**Priority:** Must

### Acceptance criteria

- summary values link to underlying records;
- zero differs from unavailable;
- stale data has timestamp;
- no accepted KPI silently uses mock data;
- filter scope is visible.

## 49. UC-033 — Revoke future authority

**Primary actor:** Workspace Owner / Authorized administrator  
**Priority:** Must

### Main success path

1. User selects adapter, tool, role, secret reference, or policy grant.
2. User requests revocation.
3. System identifies active runs affected.
4. User confirms.
5. Future authority is removed.
6. Active work is paused, cancelled, or marked according to policy.
7. Revocation is audited.

### Acceptance criteria

- prompt text cannot restore revoked authority;
- revocation takes effect within defined bound;
- affected active work is visible;
- past evidence remains readable according to retention policy.

## 50. UC-034 — Expire approval

**Primary actor:** System  
**Priority:** Must

### Acceptance criteria

- expiry time is explicit;
- expired request cannot be consumed;
- waiting run remains blocked;
- new request is required;
- expiry event is auditable.

## 51. UC-035 — Mark state stale or unknown

**Primary actor:** System  
**Priority:** Must

### Trigger

Expected state evidence is older than threshold or contradictory/unavailable.

### Acceptance criteria

- stale/unknown is not converted to failed or completed without evidence;
- timestamp and reason are visible;
- user has a diagnostic path;
- dashboard summaries propagate uncertainty honestly.

## 52. Cross-journey navigation model

The proposed navigation should support:

- Mission Control;
- Workspaces;
- Projects;
- Tasks;
- Runs;
- Approvals;
- Agents;
- Models;
- Tools and Integrations;
- Memory and Knowledge;
- Artifacts;
- Costs and Usage;
- Audit;
- Administration;
- Operations and Health.

Final navigation belongs in `UXA-001`.

## 53. Notifications and attention model

Notifications should be reserved for events requiring awareness or action.

Priority categories:

- critical security or integrity issue;
- approval required;
- run failed or unknown;
- budget threshold reached;
- adapter/provider unavailable;
- artifact ready for review;
- backup/recovery issue;
- informative completion.

The system should avoid turning every run event into a notification.

## 54. Approval UX requirements

Approval views should show:

- plain-language action summary;
- exact technical parameters;
- requesting user/run;
- target resource;
- risk category;
- policy reason;
- side effects;
- diff/preview;
- expiry;
- cost impact where relevant;
- prior related requests;
- approve/reject/request-revision controls.

Keyboard operation and screen-reader semantics are mandatory design concerns.

## 55. Error-message requirements

An actionable error should answer:

1. What failed?
2. What remains safe or persisted?
3. What may already have happened?
4. What is unknown?
5. What can the user do next?
6. Does the action require new approval?
7. Where can technical evidence be found?

Errors must not expose credentials, private paths, or unrelated workspace data.

## 56. Empty-state requirements

Every empty state should explain:

- what the section contains;
- why it may be empty;
- what the user can do next;
- whether configuration or permission is missing;
- whether data is unavailable rather than absent.

## 57. Accessibility requirements across journeys

All priority journeys should support:

- keyboard-only completion;
- visible focus;
- semantic landmarks and headings;
- non-color state indicators;
- accessible names for controls;
- readable error summaries;
- responsive reflow;
- zoom and text scaling;
- reduced motion;
- adequate target size;
- table alternatives where needed;
- time/date clarity;
- status changes announced appropriately.

Final measurable requirements belong in `A11Y-001` and `NFR-001`.

## 58. Responsive behavior

### Desktop

Primary full-operation environment.

### Tablet

Review, monitoring, artifact inspection, and selected low-risk operations.

### Mobile

Status review, safe approvals where explicitly permitted, and artifact access.

The MVP should not permit mobile execution of consequential actions unless `AUT-001`, `SEC-001`, and UX acceptance explicitly allow the action class.

## 59. Data and privacy considerations

Journeys must minimize unnecessary exposure of:

- prompts and private context;
- source code;
- personal information;
- financial data;
- secrets;
- provider identifiers where restricted;
- audit content outside authorized scope.

Telemetry must be purposeful and privacy-reviewed.

## 60. Security abuse cases

The following abuse cases must be considered by `THR-001`:

- prompt attempts to broaden permissions;
- malicious file causing tool execution;
- forged adapter status;
- approval request with hidden changed parameters;
- cross-workspace memory poisoning;
- artifact preview exploit;
- audit-log tampering;
- secret leakage in logs;
- replayed approval;
- duplicate side effect after retry;
- compromised local browser session;
- malicious MCP server;
- provider response used as trusted instruction;
- dashboard hiding stale or failed collection.

## 61. Journey metrics

| Journey | Proposed measure |
|---|---|
| Onboarding | Completion rate and time to safe diagnostic |
| Workspace creation | Successful persisted creation without leakage |
| Task creation | Time and error rate for bounded task definition |
| Run monitoring | Time to correctly identify state |
| Approval | Correct comprehension of action and side effect |
| Recovery | Successful safe recovery without duplicate effect |
| Artifact retrieval | Retrieval success and provenance comprehension |
| Memory | Correct source/confidence interpretation |
| Cost | Attribution coverage and estimate comprehension |
| Audit | Ability to reconstruct required event chain |
| Isolation | Negative-access test pass rate |
| Backup/restore | Recovery time and retained-data verification |
| Accessibility | Journey completion with keyboard and assistive technology |

Final thresholds belong in `NFR-001` and `TST-001`.

## 62. Pilot test scenarios

### Scenario A — Safe documentation task

- create workspace;
- register Codex;
- create bounded documentation task;
- execute;
- store Markdown artifact;
- review trace and cost.

### Scenario B — Approval-required Git commit proposal

- agent generates patch;
- run proposes commit;
- policy blocks;
- approver rejects;
- user revises;
- new request approved;
- actual commit execution remains outside MVP unless explicitly authorized by later requirements.

### Scenario C — Interrupted Hermes run

- run starts;
- adapter is stopped;
- system detects stale state;
- operator diagnoses;
- run resumes or safely terminates.

### Scenario D — Workspace isolation

- similar file names in two workspaces;
- search and memory retrieval from Workspace A;
- verify no Workspace B result or metadata leak.

### Scenario E — Backup and restore

- create tasks, runs, approvals, and artifacts;
- back up;
- simulate service loss;
- restore;
- reconcile retained records.

## 63. Out-of-scope journeys

The following are not part of MVP acceptance:

- public signup and subscription;
- external customer billing;
- marketplace purchase/install;
- unrestricted mobile administration;
- automatic production deployment;
- autonomous financial transaction;
- swarms of coordinating agents;
- image/video/voice Studio;
- public content publishing without approval;
- multi-region failover;
- cross-organization delegation.

## 64. Dependencies

This document depends on:

- `VSN-001`;
- approved content of `SCP-001`;
- `PER-001`;
- `DOC-000`;
- `GLO-001`.

Downstream documents:

- `PRD-001`;
- `SRS-001`;
- `NFR-001`;
- `AUT-001`;
- `IAM-001`;
- `UXA-001`;
- `A11Y-001`;
- `SAD-001`;
- `THR-001`;
- `TST-001`;
- `RTM-001`.

## 65. Risks

| Risk | Consequence | Response |
|---|---|---|
| Too many journeys in MVP | Delivery becomes unbounded | Keep Must journeys focused on one vertical slice |
| Journey assumes architecture | Premature lock-in | Describe behavior, not implementation |
| Approval overload | Poor adoption | Risk-based approval matrix |
| Technical bias | Nontechnical reviewers cannot decide | Plain summary plus technical detail |
| Recovery oversimplification | Duplicate side effects | Explicit unknown and unsafe states |
| Dashboard-first design | Mock-driven product | Trace every summary to persisted records |
| Mobile overreach | Sensitive action risk | Restrict consequential actions |
| Accessibility deferred | Redesign and exclusion | Include acceptance from first prototype |
| Persona-role confusion | Excess authority | Separate responsibility and permission |

## 65A. ADR-003 journey baseline

The primary journeys must include:

1. create or select a personal or team workspace;
2. create a project, mission, and task;
3. start a private conversation and optionally link it to the work;
4. launch Codex, Hermes, or Claude Code from the interface;
5. observe a durable run and its evidence;
6. receive an approval request for an external, destructive, or critical action;
7. share a conversation or artifact explicitly with a project or workspace audience;
8. resume, retry, pause, cancel, archive, or delete work according to policy.

## 66. Open decisions

1. Which journeys are mandatory for the first demonstration?
2. Which personas are represented by distinct people in the pilot?
3. Can any consequential approval occur on mobile?
4. Which safe diagnostic task should onboarding use?
5. Which Git actions remain proposal-only versus executable in MVP?
6. What exact interruption scenarios must be resumable?
7. Which artifact types are supported initially?
8. Which memory writes require explicit user approval?
9. Which cost sources are authoritative enough for pilot reporting?
10. What is the stale-state threshold for each component?
11. Which notification channels are in scope?
12. Which languages must the UI support?
13. What data may be included in evidence exports?
14. What user-research sample is sufficient for persona/journey validation?
15. Which journeys can be delayed without blocking the first vertical slice?

## 67. Acceptance criteria

UCD-001 may advance to version 1.0.0 when:

1. Product Owner approves the Must journey catalogue;
2. personas and JTBD references align with `PER-001`;
3. journeys remain within approved `SCP-001` scope;
4. every Must journey has main, alternate, and failure behavior;
5. approval and security implications are explicit;
6. state semantics are consistent across journeys;
7. accessibility requirements are represented;
8. no journey claims implementation;
9. out-of-scope journeys are explicit;
10. PRD and SRS can derive requirements without inventing core user behavior;
11. links, metadata, terminology, and document validation pass.

## 68. Downstream traceability

| Journey / Use case | Downstream owner |
|---|---|
| Workspace and membership | PRD, SRS, IAM, UXA |
| Agent/model registration | PRD, SAD, AGC, MOD |
| Task/run | PRD, SRS, ORC, RUN |
| Approval | AUT, APR, SEC, THR |
| Artifact | ART, DAT, UXA |
| Memory | MEM, DAT, SEC |
| Cost | NFR, FIN, OBS |
| Audit | AUD, SEC, TST |
| Backup/restore | BCP, OPS, TST |
| Accessibility | A11Y, NFR, TST |

## 69. Revision and approval history

### Approval state

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Approval date: not applicable
- Required next action: Product Owner, UX/accessibility, Architecture, and Security review

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial journey catalogue, detailed MVP journeys, use cases, failure behavior, accessibility expectations, and traceability | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `PER-001` — Personas and Jobs to Be Done
- `VIDEO-002` — UI/UX Evidence Audit
- `VIDEO-003` — Agent OS Capability and Opportunity Brief
