---
document_id: PRD-001
title: Agent OS Product Requirements Document
version: 1.0.0
status: approved
owner: product-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - ux-accessibility-owner
  - quality-owner
created: 2026-07-19
last_reviewed: 2026-08-12
approval_date: 2026-08-13
review_records:
  - role: product-owner
    review_status: approved
    review_date: 2026-08-13
    evidence: explicit user authorization after document review; cross-functional approval remains required
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user authorization in this request
pending_approvals:
  - architecture-owner
  - security-owner
  - ux-accessibility-owner
  - quality-owner
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PER-001
  - UCD-001
  - SRS-001
  - NFR-001
  - AUT-001
  - RTM-001
  - SAD-001
  - SEC-001
  - TST-001
related_adrs: []
---

# PRD-001 — Agent OS Product Requirements Document

> **Status: Approved baseline — 2026-08-13.** This Product Requirements Document defines the approved MVP product baseline. It does not prove implementation, select final technologies, authorize production use, or replace detailed functional, non-functional, architecture, security, contract, and test documents.

## 1. Document purpose

This document defines the proposed product requirements for the first Agent OS MVP and local pilot.

It establishes:

- the product problem and intended outcomes;
- the primary users and jobs;
- the MVP capability baseline;
- prioritized product requirements;
- release slices and sequencing;
- product-level acceptance criteria;
- success measures;
- assumptions, constraints, dependencies, and risks;
- explicit exclusions;
- traceability to scope, personas, and journeys.

This document is the primary product input to:

- `SRS-001` — Functional Requirements Specification;
- `NFR-001` — Non-Functional Requirements;
- `AUT-001` — Autonomy and Approval Matrix;
- `RTM-001` — Requirements Traceability Matrix;
- `SAD-001` — System Architecture Description;
- `SEC-001` and `THR-001`;
- `UXA-001`, `DSN-001`, and `A11Y-001`;
- `AGC-001`, `RUN-001`, `APR-001`, and `ART-001`;
- `TST-001` and `QAG-001`;
- the MVP backlog and delivery roadmap.

## 2. Product summary

Agent OS is a provider-neutral control, orchestration, and governance platform for operating AI agents, models, tools, workflows, knowledge, and artifacts through durable workspaces.

The first MVP is a local, single-node, responsive web Mission Control intended for one primary operator or a small trusted team. It must prove that two agent adapters—Hermes and Codex—can execute bounded work through common product concepts while preserving:

- durable task and run state;
- explicit permissions;
- human approval for consequential actions;
- artifact provenance;
- permission-aware memory;
- audit evidence;
- usage and cost attribution;
- failure visibility;
- safe recovery;
- workspace isolation.

The MVP is not intended to provide broad autonomous control, public SaaS tenancy, production financial actions, high availability, multi-agent swarms, or a full media-generation Studio.

## 3. Product problem

AI-assisted work is fragmented across chats, coding agents, model providers, terminals, repositories, files, automation services, and dashboards.

Users experience:

- repeated context reconstruction;
- state loss after interruption;
- weak separation between prompts and permissions;
- inconsistent agent and provider interfaces;
- difficulty understanding what is running;
- unverified completion claims;
- unclear costs and side effects;
- outputs without provenance;
- memory that can mix facts and generated claims;
- tools that are connected but not safely authorized;
- dashboards that may hide mock, stale, or disconnected data;
- retries that risk duplicate effects.

Agent OS must solve the control and governance problem before attempting breadth of features.

## 4. Product vision alignment

The product must preserve the approved principles from `VSN-001`:

1. provider, model, agent, tool, and storage replaceability;
2. workspace-centered organization;
3. durable execution;
4. evidence before status;
5. human control over consequential actions;
6. least privilege;
7. provenance-aware memory;
8. separation of generated analysis from authoritative sources;
9. observable and reproducible runs;
10. local-first deployment with a production upgrade path;
11. accessibility and responsive design;
12. explicit uncertainty, stale state, and failure.

## 5. Product objectives

### OBJ-001 — Durable continuity

Users can stop, restart, refresh, or recover the local environment without losing the accepted state of tasks, runs, approvals, artifacts, and audit evidence.

### OBJ-002 — Governed delegation

Users can delegate bounded work with explicit resource, time, cost, data, tool, and approval limits.

### OBJ-003 — Provider and agent portability

Hermes and Codex operate through common product concepts and contracts rather than defining separate user workflows.

### OBJ-004 — Human control

Consequential actions remain blocked until an authorized person approves the exact action.

### OBJ-005 — Evidence-backed operation

Mission Control and detail views reflect persisted facts, provider-reported states, estimates, stale data, and unknown data honestly.

### OBJ-006 — Workspace isolation

Data, memory, artifacts, permissions, integrations, and costs are scoped by workspace.

### OBJ-007 — Recoverable execution

Users can diagnose, cancel, retry, or resume work without silently duplicating side effects.

### OBJ-008 — Provenance and retrieval

Artifacts and memory remain linked to their task, run, source, producer, classification, and lifecycle.

### OBJ-009 — Cost visibility

Supported model and tool usage can be attributed to organization, workspace, project, task, and run.

### OBJ-010 — Operable local pilot

The first pilot can be installed, configured, backed up, restored, diagnosed, and reviewed without undocumented operator knowledge.

## 6. Non-objectives

The MVP does not aim to:

- provide public multi-tenant SaaS;
- replace operating systems;
- build or train foundation models;
- grant unrestricted host-machine control;
- provide perfect or unlimited memory;
- provide unattended open-ended autonomy;
- autonomously commit, push, create pull requests, or merge;
- send unrestricted external communications;
- post production financial transactions;
- replace ERP, CRM, accounting, GitHub, or identity systems;
- provide high availability or multi-region failover;
- provide multi-agent swarms;
- provide a public adapter marketplace;
- provide full image, video, and voice Studio workflows;
- prove product-market fit;
- claim production readiness based only on UI completion.

## 7. Target users

### Primary

- `PERS-001` — Builder-Operator;
- `PERS-002` — Product / Workspace Owner;
- `PERS-003` — Technical Operator / Platform Administrator;
- `PERS-004` — Reviewer / Approver.

### Secondary

- `PERS-005` — Auditor / Assurance Reviewer;
- `PERS-006` — Contributor / Artifact Consumer.

### Future

- organization administrator for public multi-organization deployment;
- extension developer;
- business analyst consuming read-only business-system data.

## 8. Priority Jobs to Be Done

The MVP must support at least the following jobs:

- `JTBD-001` — recover project context and current state;
- `JTBD-002` — define a bounded task;
- `JTBD-003` — understand agent/model/provider selection;
- `JTBD-004` — supervise persisted execution;
- `JTBD-005` — review consequential actions;
- `JTBD-006` — recover or terminate interrupted work;
- `JTBD-007` — retain and retrieve artifacts with provenance;
- `JTBD-008` — store and retrieve governed memory;
- `JTBD-009` — attribute usage and cost;
- `JTBD-010` — grant minimum tool/integration capability;
- `JTBD-011` — reconstruct work from audit evidence;
- `JTBD-012` — manage workspace membership and policy;
- `JTBD-014` — distinguish real, stale, estimated, and unknown state;
- `JTBD-015` — operate backup, restore, and local recovery.

## 9. Product scope summary

### In scope for MVP

- authenticated local access;
- one organization context;
- multiple isolated workspaces;
- projects;
- workspace membership and basic roles;
- agent registry;
- Hermes and Codex adapters;
- model-profile foundation;
- tasks;
- durable runs and run steps;
- cancellation and bounded retry;
- interruption/recovery foundation;
- approval inbox;
- tool registry and basic scoped permissions;
- permission-aware memory foundation;
- artifact storage and metadata;
- audit events and execution receipts;
- token/tool usage and cost attribution;
- responsive accessible Mission Control;
- health diagnostics;
- backup and restore foundation.

### Explicitly excluded

- public onboarding and subscriptions;
- public internet exposure by default;
- production financial writes;
- unrestricted production access;
- autonomous source-control side effects;
- unrestricted messaging;
- high availability;
- swarms;
- self-modifying skills;
- marketplace;
- predictive profit automation;
- full media Studio;
- broad business-system integrations;
- consequential mobile execution by default.

## 10. Product priority model

Requirements use the following priorities:

| Priority | Meaning |
|---|---|
| `Must` | Required for MVP acceptance |
| `Should` | Important but may move to a stabilization release if necessary |
| `Could` | Useful if capacity remains after Must and Should |
| `Won't-MVP` | Explicitly excluded from the first MVP |

A `Must` requirement may be removed only through explicit scope change and impact review.

## 11. Release model

### Release `MVP-0` — Repository and quality foundation

Purpose:

- establish application repository structure;
- development environment;
- CI;
- initial security and documentation gates;
- empty system with health endpoint and validated persistence.

### Release `MVP-1` — Identity, organization, and workspaces

Purpose:

- authenticated access;
- one organization context;
- multiple workspaces;
- projects;
- membership and roles;
- basic Mission Control shell.

### Release `MVP-2` — Task and run vertical slice

Purpose:

- register one adapter;
- create bounded task;
- persist and execute run;
- show run state;
- retain an artifact;
- show execution evidence.

### Release `MVP-3` — Approvals and governed tools

Purpose:

- classify consequential actions;
- create approval requests;
- enforce approve/reject/expiry;
- register tools and scopes;
- store execution receipts.

### Release `MVP-4` — Two adapters, memory, audit, and costs

Purpose:

- Hermes and Codex through common contracts;
- permission-aware memory;
- audit exploration;
- model/tool usage and cost attribution;
- richer Mission Control.

### Release `MVP-5` — Recovery, backup, accessibility, and pilot acceptance

Purpose:

- interruption recovery;
- idempotency validation;
- backup and restore exercise;
- isolation tests;
- accessibility acceptance;
- complete pilot evidence.

Release identifiers are planning constructs and may change in the delivery plan.

## 12. Product epics

| Epic | Title | MVP |
|---|---|---|
| `EPIC-001` | Identity and sessions | Yes |
| `EPIC-002` | Organization, workspaces, projects, and membership | Yes |
| `EPIC-003` | Agent registry and adapters | Yes |
| `EPIC-004` | Model profiles, routing, budgets, and provider attribution | Yes |
| `EPIC-005` | Tasks and durable runs | Yes |
| `EPIC-006` | Approvals and human control | Yes |
| `EPIC-007` | Tools, integrations, and permission enforcement | Yes |
| `EPIC-008` | Memory and knowledge | Yes, foundation |
| `EPIC-009` | Artifacts and provenance | Yes |
| `EPIC-010` | Audit, execution receipts, and evidence | Yes |
| `EPIC-011` | Usage and cost attribution | Yes |
| `EPIC-012` | Mission Control and navigation | Yes |
| `EPIC-013` | Operations, health, backup, and recovery | Yes |
| `EPIC-014` | Accessibility, responsive design, and usability | Yes |
| `EPIC-015` | Read-only business-system analytics | Post-MVP |
| `EPIC-016` | Media Studio | Post-MVP |
| `EPIC-017` | Multi-agent coordination | Post-MVP |
| `EPIC-018` | Public multi-tenant commercialization | Post-MVP |

## 13. EPIC-001 — Identity and sessions

### Product outcome

Only authenticated identities can access protected Agent OS capabilities, and each action can be attributed to a user or workload identity.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-IDN-001` | The product shall require authentication for every protected view and action. | Must | Unauthenticated requests cannot access protected data or execute work. | `UC-001` |
| `PRD-IDN-002` | The product shall maintain a bounded authenticated session. | Must | Session expiry and reauthentication are enforced. | `UC-001` |
| `PRD-IDN-003` | The product shall attribute user-visible and security-relevant actions to an identity. | Must | Audit records identify the acting identity. | `JTBD-011` |
| `PRD-IDN-004` | The product shall distinguish human users from agent, worker, and integration identities. | Must | Audit and policy views identify identity type. | `PER-001` |
| `PRD-IDN-005` | The product shall not grant anonymous fallback access when identity services fail. | Must | Identity failure produces blocked state. | `UC-001` |
| `PRD-IDN-006` | The product should support local authentication suitable for the first pilot. | Should | Pilot can operate without public identity federation. | `JRN-001` |
| `PRD-IDN-007` | The product shall protect authentication events and avoid exposing credentials in logs. | Must | Validation finds no raw secret in ordinary logs. | `SEC-001` |
| `PRD-IDN-008` | The product shall show the current user and active organization/workspace context. | Must | User can identify their active scope from primary views. | `JRN-002` |

## 14. EPIC-002 — Organization, workspaces, projects, and membership

### Product outcome

Users organize work inside durable, isolated workspaces with explicit membership and role boundaries.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-WSP-001` | The product shall support one organization context in the first MVP. | Must | All pilot work belongs to the configured organization. | `SCP-001` |
| `PRD-WSP-002` | The product shall support multiple workspaces inside the organization. | Must | At least two workspaces can coexist. | `JRN-014` |
| `PRD-WSP-003` | Each workspace shall have a stable identifier, name, purpose, owner, classification, and policy profile. | Must | Workspace survives restart and can be audited. | `JRN-002` |
| `PRD-WSP-004` | The product shall support projects inside one workspace. | Must | Tasks and artifacts may be grouped by project. | `JRN-002` |
| `PRD-WSP-005` | The product shall prevent data access across workspaces by default. | Must | Negative-access tests pass across all supported paths. | `JRN-014` |
| `PRD-WSP-006` | The product shall support workspace membership. | Must | Authorized users can be added and removed. | `JRN-019` |
| `PRD-WSP-007` | The product shall support predefined roles for owner, operator, approver, auditor, and contributor. | Must | Permission behavior is testable by role. | `PER-001` |
| `PRD-WSP-008` | The product shall display the effective role and permissions for a workspace. | Should | User can understand what they may do. | `JTBD-012` |
| `PRD-WSP-009` | Membership and role changes shall be audited. | Must | Change timeline identifies actor, target, old state, and new state. | `JRN-019` |
| `PRD-WSP-010` | The product shall prevent removal of the last required workspace owner without transfer. | Must | Workspace cannot become ownerless through normal UI/API. | `JRN-019` |
| `PRD-WSP-011` | Tool, memory, artifact, task, run, approval, and cost records shall carry workspace scope. | Must | Every persisted record is traceable to a workspace. | `SCP-001` |
| `PRD-WSP-012` | The MVP shall exclude public tenant onboarding and cross-organization delegation. | Won't-MVP | No public tenant creation or cross-organization flow exists. | `SCP-001` |

## 15. EPIC-003 — Agent registry and adapters

### Product outcome

Hermes and Codex can be registered, inspected, enabled per workspace, and used through common product concepts.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-AGT-001` | The product shall provide an agent registry. | Must | Registered agents/adapters are discoverable with status. | `JRN-003` |
| `PRD-AGT-002` | The MVP shall support Hermes as an adapter target. | Must | Hermes passes the approved adapter conformance subset. | `VSN-001` |
| `PRD-AGT-003` | The MVP shall support Codex as an adapter target. | Must | Codex passes the approved adapter conformance subset. | `VSN-001` |
| `PRD-AGT-004` | Registration, reachability, health, and validated capability shall be distinct states. | Must | UI/API never treats registration alone as health proof. | `JRN-003` |
| `PRD-AGT-005` | The product shall record adapter type, identity, version, configuration state, and last validation evidence. | Must | Operator can identify exact adapter state. | `JRN-003` |
| `PRD-AGT-006` | The product shall support workspace-level adapter enablement. | Must | An adapter may be enabled for one workspace and denied for another. | `JRN-003` |
| `PRD-AGT-007` | The product shall expose declared capabilities and unavailable/unknown capability states. | Must | Unsupported capabilities are not advertised as supported. | `AGC-001` |
| `PRD-AGT-008` | The product shall preserve common task, run, approval, artifact, and event concepts across adapters. | Must | User workflow remains consistent between Hermes and Codex. | `OBJ-003` |
| `PRD-AGT-009` | The product shall report adapter-specific limitations transparently. | Must | Missing cancellation/resume/cost features are visible. | `JRN-016` |
| `PRD-AGT-010` | An adapter shall not be able to change its own platform permissions. | Must | Policy prevents self-expansion. | `SCP-001` |
| `PRD-AGT-011` | The product shall support disabling an adapter without deleting its historical evidence. | Should | Future runs stop; prior records remain readable. | `UC-033` |
| `PRD-AGT-012` | The MVP shall not provide a public adapter marketplace. | Won't-MVP | No marketplace discovery, purchase, or public install flow exists. | `SCP-001` |

## 16. EPIC-004 — Model profiles, routing, budgets, and provider attribution

### Product outcome

Users configure provider-neutral model profiles, understand what model is used, and bound provider usage.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-MOD-001` | The product shall support logical model profiles independent of user-facing provider-specific workflows. | Must | Tasks reference a profile or approved routing policy. | `JTBD-003` |
| `PRD-MOD-002` | A model profile shall identify provider, provider model ID, intended capabilities, constraints, and validation state. | Must | Operator can inspect profile configuration without secret values. | `JRN-004` |
| `PRD-MOD-003` | The product shall support workspace-level model-profile enablement. | Must | A profile may be restricted to selected workspaces. | `JRN-004` |
| `PRD-MOD-004` | The product shall support budget or usage limits at least at workspace and task/run level. | Must | Run preflight blocks requests exceeding configured limits. | `JTBD-002` |
| `PRD-MOD-005` | The product shall record the actual provider and model used where available. | Must | Run detail shows actual provider/model or explicit unknown state. | `JTBD-003` |
| `PRD-MOD-006` | The product shall distinguish profile configuration from successful provider validation. | Must | Failed validation does not appear as ready. | `JRN-004` |
| `PRD-MOD-007` | The product shall support transparent fallback policy only when explicitly configured. | Should | Fallback does not occur silently. | `VSN-001` |
| `PRD-MOD-008` | The product shall apply data-classification and provider-policy checks before sending context. | Must | Prohibited content is blocked before provider dispatch. | `SCP-001` |
| `PRD-MOD-009` | The product shall expose delayed, missing, or unavailable usage/cost data. | Must | Unknown cost is not displayed as zero. | `JRN-012` |
| `PRD-MOD-010` | The MVP shall not require one specific model provider as a permanent platform dependency. | Must | Core product concepts remain provider-neutral. | `OBJ-003` |

## 17. EPIC-005 — Tasks and durable runs

### Product outcome

Users define bounded work and supervise execution through durable, recoverable state.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-RUN-001` | The product shall support task creation in a workspace and optional project. | Must | Task persists and is visible after refresh/restart. | `JRN-005` |
| `PRD-RUN-002` | A task shall define desired outcome, permitted resources, limits, expected artifacts, and data classification. | Must | Task cannot become ready when mandatory scope is missing. | `JRN-005` |
| `PRD-RUN-003` | The product shall support draft, ready, blocked, active, completed, cancelled, and archived task states. | Must | State transitions are explicit and auditable. | `UCD-001` |
| `PRD-RUN-004` | The product shall create and persist a run before external execution starts. | Must | No accepted external dispatch lacks a run ID. | `UC-009` |
| `PRD-RUN-005` | The product shall persist run steps and state transitions. | Must | Browser refresh or worker restart does not erase accepted state. | `JTBD-004` |
| `PRD-RUN-006` | The product shall expose queued, starting, running, waiting, paused, retrying, failed, cancelled, completed, stale, and unknown states. | Must | Users can distinguish operational states. | `UCD-001` |
| `PRD-RUN-007` | The product shall perform preflight authorization, adapter, model, budget, tool, and approval checks. | Must | Failed preflight prevents dispatch. | `JRN-006` |
| `PRD-RUN-008` | The product shall support cancellation intent and adapter cancellation where available. | Must | Future dispatch stops where enforceable; uncertainty remains visible. | `JRN-017` |
| `PRD-RUN-009` | The product shall support bounded retry for approved retryable steps. | Must | Retry count and eligibility are enforced. | `JTBD-006` |
| `PRD-RUN-010` | The product shall support recovery or explicit safe termination after defined interruptions. | Must | Approved recovery scenarios complete without duplicate side effect. | `JRN-009` |
| `PRD-RUN-011` | The product shall use idempotency or equivalent safeguards for defined side-effecting operations. | Must | Duplicate dispatch does not duplicate protected effect. | `JRN-009` |
| `PRD-RUN-012` | The product shall retain lineage between original and resumed/retried steps. | Must | Audit shows recovery chain. | `UC-017` |
| `PRD-RUN-013` | The product shall distinguish completed, partial, failed, stale, and unknown results. | Must | No unsupported success claim is shown. | `JRN-018` |
| `PRD-RUN-014` | The product shall generate a basic execution receipt for accepted runs. | Must | Receipt links inputs, configuration, steps, outputs, and known effects. | `JTBD-011` |
| `PRD-RUN-015` | The MVP shall exclude unattended open-ended runs without time, cost, and stop bounds. | Won't-MVP | Every run has enforceable limits or is blocked. | `SCP-001` |

## 18. EPIC-006 — Approvals and human control

### Product outcome

Consequential actions are blocked until an authorized human approves the exact proposal.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-APR-001` | The product shall classify actions by side effect and approval policy. | Must | Approval-required actions are identifiable before execution. | `AUT-001` |
| `PRD-APR-002` | The product shall block consequential actions without a valid approval. | Must | Conformance tests show 100% denial without approval. | `JRN-007` |
| `PRD-APR-003` | An approval request shall identify requester, task, run, exact action, parameters, target, risk, reason, expiry, and expected effects. | Must | Reviewer can inspect exact proposal. | `JRN-007` |
| `PRD-APR-004` | The product shall support approve, reject, request revision, expire, cancel, and invalidate outcomes. | Must | Every outcome has distinct durable state. | `JRN-008` |
| `PRD-APR-005` | Approval shall be bound to exact parameters and target. | Must | Material change requires a new approval. | `UC-012` |
| `PRD-APR-006` | The product shall verify approver authority at decision time and execution time. | Must | Unauthorized or stale approval cannot be consumed. | `UC-012` |
| `PRD-APR-007` | The product shall prevent double consumption or replay of an approval. | Must | One-time approval cannot authorize duplicate action. | `UC-012` |
| `PRD-APR-008` | Approval expiry shall block execution and require renewal. | Must | Expired approval cannot be consumed. | `UC-034` |
| `PRD-APR-009` | The product shall preserve rejection and revision reasons. | Must | Requester can understand required change. | `JRN-008` |
| `PRD-APR-010` | The product shall allow revocation of future authority. | Must | Revoked permission cannot be restored through prompt text. | `UC-033` |
| `PRD-APR-011` | The product shall provide an approval inbox prioritized by risk and age. | Must | Reviewer can find pending requests. | `PERS-004` |
| `PRD-APR-012` | The product should provide plain-language summary and technical detail. | Should | Nontechnical and technical review are both supported. | `PERS-004` |
| `PRD-APR-013` | The MVP shall treat commit, push, pull-request creation, merge, deletion, external messaging, production access, secret access, financial modification, destructive database action, public publication, executable installation, and permission expansion as candidate approval-required classes. | Must | Final matrix can be implemented without scope gap. | `SCP-001` |
| `PRD-APR-014` | The MVP shall not autonomously merge source changes. | Won't-MVP | No autonomous merge path exists. | `VSN-001` |

## 19. EPIC-007 — Tools, integrations, and permission enforcement

### Product outcome

Tools and integrations expose capabilities without receiving implicit or excessive authority.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-TOL-001` | The product shall provide a registry of tools and integrations. | Must | Operator can inspect registered capability and status. | `JTBD-010` |
| `PRD-TOL-002` | Tool availability shall not grant permission. | Must | Unauthorized invocation is denied. | `SCP-001` |
| `PRD-TOL-003` | The product shall evaluate identity, workspace, capability, resource scope, data class, network target, side effect, budget, and approval before invocation. | Must | Policy evidence exists for every protected invocation. | `SCP-001` |
| `PRD-TOL-004` | The product shall support workspace-scoped tool enablement. | Must | Tool can be enabled in one workspace and denied in another. | `JTBD-012` |
| `PRD-TOL-005` | The product shall support bounded filesystem/repository scopes. | Must | Paths outside approved scope are denied. | `SCP-001` |
| `PRD-TOL-006` | The product shall restrict network destinations according to policy. | Must | Unapproved destination access is denied. | `SEC-001` |
| `PRD-TOL-007` | The product shall record a receipt for accepted tool actions. | Must | Audit can identify request, decision, execution, and result. | `JTBD-011` |
| `PRD-TOL-008` | The product shall expose denied requests safely without leaking protected metadata. | Must | Cross-workspace/resource denial reveals no sensitive details. | `UC-027` |
| `PRD-TOL-009` | The product shall support disabling/revoking a tool capability. | Must | Future invocations are blocked within defined bound. | `UC-033` |
| `PRD-TOL-010` | The product shall not treat MCP connectivity as authorization. | Must | Connected MCP server remains policy-controlled. | `VSN-001` |
| `PRD-TOL-011` | Package or executable installation shall require explicit policy and approval. | Must | Agent cannot install executable content silently. | `SCP-001` |
| `PRD-TOL-012` | The MVP shall expose only a minimal approved tool set needed for pilot journeys. | Must | Tool surface remains bounded. | `SCP-001` |

## 20. EPIC-008 — Memory and knowledge

### Product outcome

Useful context can be retained and retrieved without turning unverified outputs into hidden truth or leaking across workspaces.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-MEM-001` | The product shall provide a workspace-scoped memory/knowledge foundation. | Must | Records are stored and retrieved only in authorized scope. | `JRN-011` |
| `PRD-MEM-002` | A memory record shall include source, scope, producer, creation time, classification, and verification/confidence state. | Must | User can inspect provenance. | `JTBD-008` |
| `PRD-MEM-003` | Generated or inferred content shall remain visibly labeled. | Must | Generated hypotheses do not appear authoritative. | `JRN-011` |
| `PRD-MEM-004` | The product shall prevent ordinary storage of secrets as memory. | Must | Secret-class content is blocked or redirected to approved secret handling. | `SCP-001` |
| `PRD-MEM-005` | The product shall apply permission checks at ingestion, storage, retrieval, export, correction, and deletion. | Must | Unauthorized lifecycle action is denied. | `VSN-001` |
| `PRD-MEM-006` | The product shall deny cross-workspace memory retrieval by default. | Must | Negative retrieval tests pass. | `JRN-014` |
| `PRD-MEM-007` | Retrieval should expose source, age, and reason for inclusion. | Should | User can understand why context was returned. | `JTBD-008` |
| `PRD-MEM-008` | The product shall support correction, supersession, and controlled deletion. | Must | User can resolve inaccurate memory within policy. | `JRN-011` |
| `PRD-MEM-009` | The product shall support retention state. | Must | Expired/deleted records are not returned as active. | `SCP-001` |
| `PRD-MEM-010` | The MVP shall not claim perfect, complete, or indefinite memory. | Won't-MVP | UI/docs make no such guarantee. | `VSN-001` |
| `PRD-MEM-011` | Automatic memory writes shall be policy-governed. | Must | Agent cannot silently promote all outputs to memory. | `JRN-011` |
| `PRD-MEM-012` | Conflicts with an authoritative source shall be visible rather than silently merged. | Should | User sees conflict and source priority. | `DOC-000` |

## 21. EPIC-009 — Artifacts and provenance

### Product outcome

Users can retain, find, inspect, review, and safely reuse outputs with source and lifecycle context.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-ART-001` | The product shall store artifact metadata and a retained content reference. | Must | Artifact remains discoverable after restart. | `JRN-010` |
| `PRD-ART-002` | Artifact metadata shall include workspace, project, task, run, step, producer, media type, size, integrity, classification, lifecycle, and timestamp. | Must | Provenance chain is complete for MVP fields. | `UC-018` |
| `PRD-ART-003` | The product shall support at least text, Markdown, JSON, code patch, test log, and permitted small-file artifacts. | Must | Pilot artifact types can be retained and retrieved. | `SCP-001` |
| `PRD-ART-004` | The product shall support generated, under-review, accepted, rejected, superseded, archived, deleted, and unavailable states. | Must | Lifecycle state is explicit. | `UCD-001` |
| `PRD-ART-005` | The product shall prevent unauthorized artifact discovery and retrieval. | Must | Negative-access tests cover metadata and content. | `JRN-014` |
| `PRD-ART-006` | The product shall provide safe preview behavior. | Must | Unsafe content is not executed through preview. | `JRN-010` |
| `PRD-ART-007` | Integrity mismatch shall be visible and block trusted use. | Must | Corrupted content cannot appear accepted. | `JRN-010` |
| `PRD-ART-008` | The product shall preserve version or derivative relationships. | Should | User can find superseding artifact. | `JTBD-007` |
| `PRD-ART-009` | Exported evidence packages shall themselves be artifacts with provenance. | Should | Export can be audited and retrieved. | `JRN-020` |
| `PRD-ART-010` | Full image/video/voice generation workflows shall remain post-MVP. | Won't-MVP | No full Studio workflow is required for acceptance. | `SCP-001` |

## 22. EPIC-010 — Audit, execution receipts, and evidence

### Product outcome

Authorized users can reconstruct what happened and identify missing evidence without altering history.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-AUD-001` | The product shall record correlated audit events for security-relevant and operationally significant actions. | Must | Timeline links identity, workspace, task, run, step, approval, and artifact. | `JRN-013` |
| `PRD-AUD-002` | Audit views shall be read-only for auditor roles. | Must | Auditor cannot alter operational state. | `PERS-005` |
| `PRD-AUD-003` | The product shall distinguish platform fact, provider report, derived estimate, stale data, and missing data. | Must | Evidence type is visible. | `JRN-013` |
| `PRD-AUD-004` | Audit records shall avoid exposing raw secrets. | Must | Secret-scanning and review find no raw secret in ordinary evidence. | `SEC-001` |
| `PRD-AUD-005` | The product shall preserve approval decision and execution linkage. | Must | Auditor can identify whether and how approval was consumed. | `JRN-007` |
| `PRD-AUD-006` | The product shall preserve retry, resume, cancellation, and failure lineage. | Must | Recovery chain is reconstructable. | `JRN-009` |
| `PRD-AUD-007` | The product shall expose evidence gaps explicitly. | Must | Missing event/data does not appear as successful completion. | `PERS-005` |
| `PRD-AUD-008` | The product should support filtered authorized evidence export. | Should | User can export a bounded manifest/package. | `JRN-020` |
| `PRD-AUD-009` | Export shall exclude unrelated workspace and prohibited fields. | Must | Access and redaction tests pass. | `JRN-020` |
| `PRD-AUD-010` | The MVP shall maintain enough trace completeness to validate the defined vertical slice. | Must | Required event/receipt fields pass schema checks. | `VSN-001` |

## 23. EPIC-011 — Usage and cost attribution

### Product outcome

Users can understand supported model and tool consumption by workspace, task, and run.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-CST-001` | The product shall record supported model/token/tool usage events. | Must | Usage records exist for supported providers/tools. | `JRN-012` |
| `PRD-CST-002` | Usage shall be attributable to organization, workspace, project where applicable, task, run, and provider/model/tool. | Must | Reconciliation coverage can be measured. | `OBJ-009` |
| `PRD-CST-003` | Cost values shall identify currency, period, source, and freshness. | Must | User can interpret the value. | `JRN-012` |
| `PRD-CST-004` | Provider-reported, calculated, estimated, pending, unavailable, and unattributed values shall be distinct. | Must | Unknown cost is never shown as zero. | `JRN-012` |
| `PRD-CST-005` | The product shall surface reconciliation mismatches. | Should | Mismatch is visible and traceable. | `VSN-001` |
| `PRD-CST-006` | The product shall support workspace and run-level budget thresholds. | Must | Preflight or runtime policy can block/stop according to rules. | `JTBD-009` |
| `PRD-CST-007` | The cost view shall not present provider spend as business profit or accounting fact. | Must | UI labels prevent financial-source confusion. | `SCP-001` |
| `PRD-CST-008` | The product should support export of authorized cost detail. | Should | Owner can review records outside UI. | `JRN-012` |

## 24. EPIC-012 — Mission Control and navigation

### Product outcome

Users can understand current work, risk, evidence, and system health through a coherent interface backed by real state.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-UI-001` | The product shall provide responsive web Mission Control. | Must | Defined MVP journeys work at approved viewports. | `VSN-001` |
| `PRD-UI-002` | Mission Control shall summarize active tasks, runs, approvals, failures, costs, and health from persisted sources. | Must | Summary values reconcile with detail records. | `JRN-018` |
| `PRD-UI-003` | The UI shall distinguish zero, unavailable, stale, estimated, partial, failed, and unknown. | Must | Usability tests show correct interpretation. | `JTBD-014` |
| `PRD-UI-004` | Every summary metric shall provide a path to supporting detail. | Must | User can drill into underlying records. | `JRN-018` |
| `PRD-UI-005` | The primary navigation shall include workspaces, projects, tasks, runs, approvals, agents, models, tools/integrations, memory, artifacts, costs, audit, and operations. | Must | Users can locate each core domain. | `UCD-001` |
| `PRD-UI-006` | The UI shall keep active organization/workspace/project context visible. | Must | Users correctly identify current scope. | `JRN-014` |
| `PRD-UI-007` | The UI shall use progressive disclosure for technical detail. | Should | Primary summaries remain understandable while evidence is available. | `PER-001` |
| `PRD-UI-008` | Error states shall explain what failed, what is known, what may have happened, and next actions. | Must | Error review meets defined checklist. | `UCD-001` |
| `PRD-UI-009` | Empty states shall distinguish no data, missing configuration, denied access, and unavailable collection. | Must | Users do not misinterpret empty sections. | `UCD-001` |
| `PRD-UI-010` | The UI shall avoid silently using mock data in accepted workflows. | Must | Acceptance tests verify persisted sources. | `VSN-001` |
| `PRD-UI-011` | Approval and critical failure states shall be visible without relying only on color. | Must | Accessibility review passes. | `A11Y-001` |
| `PRD-UI-012` | Mobile shall prioritize review and status; consequential execution shall remain restricted unless explicitly approved. | Must | Mobile flow has no unauthorized sensitive action. | `SCP-001` |

## 25. EPIC-013 — Operations, health, backup, and recovery

### Product outcome

A technical operator can run and recover the local pilot with documented, evidence-backed procedures.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-OPS-001` | The MVP shall support a documented local single-node Linux/WSL deployment. | Must | Pilot can be started from a clean documented environment. | `SCP-001` |
| `PRD-OPS-002` | The product shall expose health for control plane, adapters, provider validation, storage, tool gateway, and event processing. | Must | Operator can identify failing boundary. | `JRN-016` |
| `PRD-OPS-003` | Health shall distinguish registered, reachable, validated, degraded, failed, stale, and unknown. | Must | Status is evidence-backed. | `JRN-016` |
| `PRD-OPS-004` | The product shall support controlled configuration without committing secrets. | Must | Repository and ordinary documents contain no secrets. | `VSN-001` |
| `PRD-OPS-005` | The product shall provide a backup procedure covering defined retained data. | Must | Backup manifest and integrity evidence exist. | `JRN-015` |
| `PRD-OPS-006` | The product shall provide a restore procedure. | Must | Approved recovery exercise restores expected records. | `JRN-015` |
| `PRD-OPS-007` | Partial backup or restore shall be visibly classified as partial. | Must | Operator cannot mistake partial recovery for success. | `UC-029` |
| `PRD-OPS-008` | The product shall record operational recovery evidence. | Should | Recovery time and missing data can be reviewed. | `JRN-015` |
| `PRD-OPS-009` | The MVP shall not require high-availability infrastructure. | Won't-MVP | Single-node remains valid acceptance topology. | `SCP-001` |
| `PRD-OPS-010` | Remote access shall be excluded by default until separately approved. | Must | Default deployment has no public exposure. | `SCP-001` |
| `PRD-OPS-011` | The system shall support clean startup and shutdown without corrupting accepted state. | Must | Restart tests preserve required records. | `OBJ-001` |
| `PRD-OPS-012` | The product shall provide an operator-visible version/build identity. | Should | Operator can identify deployed version during diagnostics. | `JRN-016` |

## 26. EPIC-014 — Accessibility, responsive design, and usability

### Product outcome

Primary workflows are usable by keyboard, assistive technology, and users with varying viewport, language, motor, visual, and cognitive needs.

### Requirements

| ID | Requirement | Priority | Acceptance outcome | Source |
|---|---|---|---|---|
| `PRD-A11Y-001` | The product shall target WCAG 2.2 AA for defined MVP workflows. | Must | Automated and manual review shows no unresolved critical blocker. | `VSN-001` |
| `PRD-A11Y-002` | All Must journeys shall be completable by keyboard. | Must | Keyboard test passes without trap. | `UCD-001` |
| `PRD-A11Y-003` | Interactive elements shall have accessible names, roles, and states. | Must | Assistive-technology review passes. | `UCD-001` |
| `PRD-A11Y-004` | Status shall not rely on color alone. | Must | State remains understandable without color perception. | `UCD-001` |
| `PRD-A11Y-005` | Focus shall be visible and follow logical order. | Must | Manual keyboard review passes. | `UCD-001` |
| `PRD-A11Y-006` | Content shall reflow at approved responsive widths without global horizontal scrolling. | Must | Viewport validation passes. | `UCD-001` |
| `PRD-A11Y-007` | The product shall support text zoom/scaling and reduced motion. | Must | Manual accessibility checks pass. | `PER-001` |
| `PRD-A11Y-008` | Errors and dynamic status changes shall be perceivable to assistive technology. | Must | Screen-reader review receives required announcements. | `UCD-001` |
| `PRD-A11Y-009` | The product shall use plain, consistent terminology and expose technical detail progressively. | Should | Usability review shows correct comprehension. | `PER-001` |
| `PRD-A11Y-010` | Date, time, currency, and time-zone context shall be explicit. | Should | Users can interpret event ordering and costs. | `PER-001` |
| `PRD-A11Y-011` | The content architecture should be localization-ready. | Should | User-facing strings are not inseparably embedded in logic. | `PER-001` |
| `PRD-A11Y-012` | The MVP shall remain desktop-primary while supporting review-oriented tablet/mobile layouts. | Must | Critical desktop journeys remain complete; mobile scope is bounded. | `SCP-001` |

## 27. Cross-cutting product requirements

| ID | Requirement | Priority |
|---|---|---|
| `PRD-XC-001` | Every user-visible success state shall be backed by persisted or externally verified evidence. | Must |
| `PRD-XC-002` | Every protected record shall carry organization/workspace scope where applicable. | Must |
| `PRD-XC-003` | Every consequential operation shall be attributable to an identity. | Must |
| `PRD-XC-004` | Every provider-, model-, adapter-, tool-, approval-, artifact-, and cost-dependent view shall represent unknown/unavailable state explicitly. | Must |
| `PRD-XC-005` | Secrets shall remain outside prompts, source control, ordinary memory, artifacts, and logs. | Must |
| `PRD-XC-006` | No prompt shall override platform authorization. | Must |
| `PRD-XC-007` | No accepted workflow shall silently depend on non-persistent mock data. | Must |
| `PRD-XC-008` | Product actions shall be traceable from objective to requirement, architecture, contract, backlog, test, evidence, and release. | Must |
| `PRD-XC-009` | Final technology choices shall be recorded in architecture documents and ADRs rather than hidden in product requirements. | Must |
| `PRD-XC-010` | Unsupported functionality shall be displayed as unavailable or not implemented, not simulated as operational. | Must |
| `PRD-XC-011` | Product metrics shall state source, freshness, definition, and uncertainty. | Must |
| `PRD-XC-012` | Generated analysis shall remain separate from authoritative source records. | Must |

## 28. Consequential action baseline

The following product-level action classes must be evaluated in `AUT-001`:

| Action class | Proposed MVP policy |
|---|---|
| Read approved workspace data | May be permitted without per-action approval |
| Draft artifact | May be permitted under task policy |
| Run safe tests in bounded sandbox | May be permitted under task policy |
| Write approved working files | Policy-dependent |
| Create Git commit | Mandatory approval candidate |
| Push branch | Mandatory approval candidate |
| Create pull request | Mandatory approval candidate |
| Merge | Excluded from autonomous MVP execution |
| Delete project data | Mandatory approval candidate |
| Send external e-mail/message | Mandatory approval candidate |
| Access production | Excluded or mandatory high-risk approval |
| Request/use secret | Mandatory approval and strict policy candidate |
| Modify database/business record | Mandatory approval; production financial writes excluded |
| Install executable/package/plugin | Mandatory approval candidate |
| Expand filesystem/network/tool permission | Mandatory approval candidate |
| Publish public content | Mandatory approval candidate |

The definitive policy matrix belongs in `AUT-001`, `SEC-001`, and `APR-001`.

## 29. Product data boundaries

The product must recognize at least the following provisional classes:

| Class | Product treatment |
|---|---|
| Public | Permitted subject to tool and source policy |
| Internal | Restricted to authorized workspaces |
| Confidential | Restricted, provider/tool handling explicitly approved |
| Secret | Excluded from ordinary prompts, memory, artifacts, and logs |
| Regulated/sensitive | Excluded unless a future approved policy permits it |

Detailed retention, residency, deletion, export, and provider-processing requirements belong in `DAT-002`, `PRI-001`, `SEC-001`, and `NFR-001`.

## 30. Business-system boundary

Future ERP, CRM, accounting, finance, analytics, and campaign connectors shall:

- begin as read-only;
- preserve source-system authority;
- expose source, metric definition, period, freshness, and reconciliation state;
- label AI-generated interpretation;
- never silently post business or financial records;
- not treat model/tool cost as profit.

These capabilities are post-MVP unless a later approved scope revision adds a constrained discovery slice.

## 31. Product success metrics

Initial product-level metrics:

| Metric | Initial baseline target |
|---|---:|
| Accepted persisted runs retaining required terminal state | ≥99% |
| Approval-required test actions blocked without valid approval | 100% |
| Approved resumable interruption scenarios without duplicate side effect | ≥95% |
| Cross-workspace negative-access test pass rate | 100% |
| Authorized retained-artifact retrieval success | ≥99% |
| Accepted runs with required trace/receipt fields | 100% |
| Billable supported usage attributed to workspace/task/run | ≥95% |
| Hermes and Codex required conformance tests passed | 100% |
| Defined journey completion after onboarding | ≥80% |
| Critical accessibility blockers in MVP journeys | 0 |
| Local pilot restore from approved backup scenario | within 4 hours, pending NFR confirmation |
| Accepted requirements linked through traceability | 100% |

Final measurement definitions, cohorts, exclusions, and owners belong in `NFR-001`, `TST-001`, and `RTM-001`.

## 32. MVP product acceptance gates

The MVP cannot be accepted unless evidence demonstrates:

1. authenticated access and workspace isolation;
2. at least two adapter targets operating through common contracts;
3. durable task, run, and step state;
4. exact-action approval enforcement;
5. cancellation and approved recovery behavior;
6. artifact retention and provenance;
7. permission-aware memory foundation;
8. audit reconstruction;
9. usage and cost attribution;
10. Mission Control backed by real state;
11. explicit stale, partial, failed, and unknown states;
12. no hidden mock dependency in accepted journeys;
13. backup and restore evidence;
14. accessibility acceptance for defined Must journeys;
15. security and negative-access tests;
16. traceability from product objective through evidence;
17. explicit Product, Architecture, Security, UX, Quality, and Operations acceptance.

## 33. Pilot definition

The first pilot should include:

- one primary Builder-Operator;
- Product/Workspace Owner responsibility;
- Technical Operator responsibility;
- at least one distinct approval scenario;
- assurance review;
- one organization;
- at least two workspaces;
- Hermes and Codex experiments;
- non-production repositories/data;
- no production financial action;
- no public internet exposure;
- measured backup and recovery exercise.

## 34. Pilot scenarios

### PILOT-001 — Documentation artifact

Create a bounded task, run it through one adapter, retain a Markdown artifact, review trace and cost, and verify state after restart.

### PILOT-002 — Coding patch with approval boundary

Generate a patch, propose a consequential Git action, verify blocking, reject once, revise, and re-request approval. Actual commit/push execution remains governed by final scope and AUT requirements.

### PILOT-003 — Interrupted run

Stop adapter or worker during a run, detect stale/unknown state, recover safely or terminate without duplicate side effect.

### PILOT-004 — Adapter portability

Run equivalent bounded tasks through Hermes and Codex and compare common state, artifact, and evidence behavior.

### PILOT-005 — Workspace isolation

Attempt cross-workspace search, memory, artifact, tool, and cost access and verify safe denial.

### PILOT-006 — Backup and restore

Back up workspaces, tasks, runs, approvals, artifacts, and audit records; restore; reconcile expected retained state.

### PILOT-007 — Accessibility

Complete Must journeys by keyboard and with selected assistive-technology checks at approved viewports.

## 35. Product analytics

The MVP may collect privacy-reviewed product analytics for:

- journey completion;
- task creation errors;
- run state transitions;
- approval decision time;
- recovery outcomes;
- artifact retrieval;
- cost-attribution coverage;
- denied cross-workspace requests;
- health and backup status;
- accessibility issue reporting.

Analytics must not collect raw secrets or unnecessary private content.

## 36. Dependencies

### Controlled documents

- `VSN-001`;
- approved content of `SCP-001`;
- `PER-001`;
- `UCD-001`;
- `DOC-000`;
- `GLO-001`.

### Required downstream baselines

- `SRS-001`;
- `NFR-001`;
- `AUT-001`;
- `SAD-001`;
- `DDD-001`;
- `DAT-001`;
- `SEC-001`;
- `THR-001`;
- `AGC-001`;
- `RUN-001`;
- `APR-001`;
- `ART-001`;
- `TST-001`;
- `QAG-001`;
- `RTM-001`.

### External dependencies

- permitted Hermes integration surface;
- permitted Codex integration surface;
- model-provider accounts and terms;
- approved identity approach;
- approved secrets mechanism;
- suitable local execution isolation;
- representative pilot projects and users;
- reviewer capacity.

## 37. Assumptions

This PRD assumes:

- a local single-node pilot is acceptable;
- one organization with multiple workspaces is sufficient for MVP;
- Hermes and Codex remain approved first adapter targets;
- adapter runtimes expose enough information for useful state and evidence;
- the initial user is technically capable;
- a small trusted team may share responsibilities;
- users value durability, approval, provenance, recovery, and cost visibility more than Studio breadth;
- provider usage information is available for at least some pilot calls;
- local backup and restore can be tested;
- named reviewers will be assigned before document approval.

No assumption is proof.

## 38. Constraints

- product requirements must remain inside `SCP-001`;
- architecture choices are deferred to architecture documents and ADRs;
- application implementation is not yet confirmed;
- secrets and local research media remain outside Git;
- accepted workflows cannot depend silently on mock data;
- first implementation must prove a complete vertical slice before breadth;
- production and financial side effects are excluded or strictly controlled;
- accessibility is required from the beginning;
- the MVP must remain operable on the approved local pilot environment;
- remote access is excluded by default.

## 39. Product risks

| Risk | Consequence | Product response |
|---|---|---|
| Scope expansion | MVP becomes unfinishable | Enforce Must baseline and Won't-MVP list |
| Adapter inconsistency | Separate products emerge for Hermes and Codex | Common contracts and conformance suite |
| False status | Users act on unsupported success | Evidence-backed state semantics |
| Approval fatigue | Governance is bypassed | Risk-based matrix and good approval UX |
| Unsafe retry | Duplicate side effects | Idempotency and explicit unknown state |
| Workspace leakage | Confidential data exposure | Negative-access tests across all paths |
| Memory contamination | Generated claim becomes fact | Provenance, labels, correction, source hierarchy |
| Cost confusion | Estimates treated as billing/accounting | Source/freshness/status labels |
| Local operational fragility | Pilot loses state | Backup, restore, health, and recovery exercises |
| Accessibility debt | Primary workflows require redesign | Acceptance from first release slice |
| Premature microservices/HA | Delivery delayed | Local single-node first |
| Protocol lock-in | Provider/tool portability reduced | Candidate standards decided by ADR |
| Dashboard-first implementation | Mock UI outruns backend | Vertical slice and source traceability |
| Incomplete audit | Incidents cannot be reconstructed | Required event/receipt contract |

## 39A. ADR-003 product baseline

The product must support:

- personal and team workspaces;
- `Project`, `Mission`, `Task`, `Run`, and independent `Conversation` concepts;
- private, project, and workspace conversation visibility, with private as the default;
- direct interaction with Codex, Hermes, and Claude Code through Agent OS;
- configurable autonomy with mandatory approval for external, destructive, and critical actions;
- long-lived conversation, artifact, memory, run, and audit records with explicit deletion and retention behavior;
- local Windows/Linux operation and authenticated VPS deployment.

## 40. Open product decisions

1. Who are the named Product, Architecture, Security, UX, Quality, and Operations approvers?
2. Is the first pilot one person, a small trusted team, or staged from one to the other?
3. Which concrete projects and tasks are used in pilot scenarios?
4. Which Hermes integration mode is permitted?
5. Which Codex integration mode is permitted?
6. Which Git actions are proposal-only versus executable after approval?
7. Which model providers and profiles are part of pilot acceptance?
8. Which tool capabilities form the minimum MVP tool set?
9. Which memory writes require explicit approval?
10. Which artifact types and maximum sizes are supported?
11. Which interruptions must support resume versus safe restart?
12. Which mobile approval classes, if any, are allowed?
13. Which UI languages are required for MVP?
14. Which identity and secret-management approaches are acceptable?
15. Which stale-state thresholds apply?
16. What exact backup recovery-point objective applies?
17. What budget, staffing, schedule, and provider-spend ceiling govern delivery?
18. Which requirements may move from Must to Should without invalidating the MVP?
19. What direct user research must occur before Product Owner approval?
20. What constitutes successful completion of the first pilot?

## 41. Product backlog derivation rules

Every backlog item derived from this PRD must include:

- source requirement ID;
- related persona/JTBD/journey;
- acceptance criteria;
- architecture component;
- security and approval implications;
- test evidence;
- documentation impact;
- no hidden scope expansion.

A backlog item cannot mark a requirement implemented solely because a UI element exists.

## 42. Change control

A material PRD change requires:

- rationale;
- impact on `SCP-001`, personas, journeys, requirements, architecture, security, testing, roadmap, and cost;
- updated version;
- updated RTM;
- affected-owner review;
- explicit Product Owner approval.

Changes that add public access, production authority, financial writes, broad autonomy, new tenancy, or cross-workspace behavior require scope and threat-model review.

## 43. PRD acceptance criteria

PRD-001 may advance to version `1.0.0` when:

1. Product Owner approves the objectives, MVP epics, Must requirements, exclusions, and pilot;
2. Architecture confirms that requirements are implementable without hidden contradiction;
3. Security accepts the product-level authority, data, tool, workspace, and approval boundaries as inputs;
4. UX/accessibility confirms that primary users and journeys are represented;
5. Quality confirms that Must requirements are testable;
6. every Must requirement has a stable ID, priority, acceptance outcome, and source;
7. no requirement claims implementation;
8. open decisions have named owning documents or owners;
9. the scope is coherent with `VSN-001` and `SCP-001`;
10. downstream SRS/NFR/AUT/SAD/SEC/TST work can proceed without inventing missing product decisions;
11. metadata, links, terminology, and document validation pass.

## 44. Downstream traceability

| Product area | Downstream documents |
|---|---|
| Identity and roles | `SRS-001`, `IAM-001`, `SEC-001` |
| Workspaces/projects | `SRS-001`, `DDD-001`, `DAT-001`, `UXA-001` |
| Agents/adapters | `SAD-001`, `INT-001`, `AGC-001`, `CAP-001` |
| Models/providers | `INT-001`, `MOD-001`, `CST-001` |
| Tasks/runs | `SRS-001`, `ORC-001`, `RUN-001`, `EVT-001` |
| Approvals | `AUT-001`, `APR-001`, `SEC-001`, `THR-001` |
| Tools/MCP | `INT-001`, `POL-001`, `SAN-001`, `MCP-001` |
| Memory | `MEM-001`, `DAT-001`, `SEC-001` |
| Artifacts | `ART-001`, `DAT-001`, `API-001` |
| Audit | `AUD-001`, `OBS-001`, `TST-001` |
| Costs | `CST-001`, `OBS-001`, `FIN-001` |
| Mission Control | `UXA-001`, `DSN-001`, `A11Y-001`, `API-001` |
| Operations | `DEP-001`, `OPS-001`, `BCP-001` |
| Quality | `NFR-001`, `TST-001`, `QAG-001`, `RTM-001` |

## 45. Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.1.0`
- Approved by: product-owner on 2026-08-13
- Approval date: not applicable
- Required next action: Product, Architecture, Security, UX/accessibility, and Quality review

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial product requirements baseline covering objectives, epics, prioritized MVP requirements, release slices, pilot, metrics, gates, and traceability | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `PER-001` — Personas and Jobs to Be Done
- `UCD-001` — User Journeys and Use Cases
