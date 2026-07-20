---
document_id: RTM-001
title: Agent OS Requirements Traceability Matrix
version: 0.1.0
status: draft
owner: quality-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - quality-owner
created: 2026-07-19
last_reviewed: 2026-07-19
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
  - SRS-001
  - NFR-001
  - AUT-001
  - SAD-001
  - SEC-001
  - TST-001
  - QAG-001
related_adrs: []
related_evidence:
  - VIDEO-001
  - VIDEO-002
  - VIDEO-003
  - VIDEO-004
  - VIDEO-EVIDENCE-INDEX
---

# RTM-001 — Agent OS Requirements Traceability Matrix

> **Status: Draft.** This matrix records the current documentation-level traceability baseline. Architecture, implementation, tests, evidence, release, and acceptance links remain incomplete because those artifacts have not yet been generated.

## 1. Purpose

This document provides a controlled trace from product intent to verifiable delivery. A requirement cannot be marked implemented or accepted merely because a screen, prototype, mock, or document exists.

## 2. Trace chain

```text
Vision / Scope
→ Personas / JTBD
→ Journeys / Use Cases
→ Objectives / Epics / Product Requirements
→ Functional Requirements / NFRs / Autonomy Policy
→ Architecture / Security / Contracts / ADRs
→ Backlog / Implementation
→ Tests / Evidence / Release
→ Acceptance
```

## 3. Status vocabulary

| Status | Meaning |
|---|---|
| `Drafted` | Trace object exists but is not approved |
| `Approved` | Baseline explicitly approved |
| `Designed` | Architecture/control/contract exists |
| `Implemented` | Code/configuration exists in an identified revision |
| `Verified` | Tests passed with retained evidence |
| `Accepted` | Authorized owner accepted it for a release |
| `Deferred` | Moved with explicit owner and rationale |
| `Blocked` | Unresolved dependency prevents progress |
| `TBD` | Link or status not yet created |

## 4. Current documentation state

| Document | Working state |
|---|---|
| `VSN-001` | Approved and versioned |
| `SCP-001` | Content approved; Git integration deferred |
| `PER-001` | Draft generated |
| `UCD-001` | Draft generated |
| `PRD-001` | Draft generated |
| `SRS-001` | Draft generated |
| `NFR-001` | Draft generated |
| `AUT-001` | Draft generated |
| `RTM-001` | This draft |
| Architecture, security, contracts, tests, evidence | Not yet generated |

## 5. Indexed coverage

| Identifier class | Count |
|---|---:|
| Personas | 6 |
| Jobs to Be Done | 15 |
| Journeys | 23 |
| Use cases | 35 |
| Product objectives | 10 |
| Product epics | 18 |
| Product requirements | 171 |
| Functional requirements | 89 |
| Non-functional requirements | 103 |
| Autonomy actions | 72 |
| **Total indexed trace objects** | **542** |

## 6. Product objectives

| Objective | Title | Downstream owner | Design | Test | Evidence |
|---|---|---|---|---|---|
| `OBJ-001` | Durable continuity | DAT-001, ORC-001, BCP-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-002` | Governed delegation | AUT-001, IAM-001, POL-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-003` | Provider and agent portability | INT-001, AGC-001, MOD-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-004` | Human control | AUT-001, APR-001, SEC-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-005` | Evidence-backed operation | OBS-001, AUD-001, UXA-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-006` | Workspace isolation | DDD-001, DAT-001, IAM-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-007` | Recoverable execution | ORC-001, RUN-001, TST-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-008` | Provenance and retrieval | ART-001, MEM-001, DAT-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-009` | Cost visibility | CST-001, OBS-001 | `TBD` | `TBD` | `TBD` |
| `OBJ-010` | Operable local pilot | DEP-001, OPS-001, BCP-001 | `TBD` | `TBD` | `TBD` |

## 7. Personas and Jobs to Be Done

### 7.1 Personas

| Persona | Title | Journey trace | Research validation |
|---|---|---|---|
| `PERS-001` | Builder-Operator | `UCD-001` | `TBD` |
| `PERS-002` | Product / Workspace Owner | `UCD-001` | `TBD` |
| `PERS-003` | Technical Operator / Platform Administrator | `UCD-001` | `TBD` |
| `PERS-004` | Reviewer / Approver | `UCD-001` | `TBD` |
| `PERS-005` | Auditor / Assurance Reviewer | `UCD-001` | `TBD` |
| `PERS-006` | Contributor / Artifact Consumer | `UCD-001` | `TBD` |

### 7.2 Jobs to Be Done

| JTBD | Job | Journey trace | Product trace | Test/evidence |
|---|---|---|---|---|
| `JTBD-001` | When I return to a project, help me recover the current context, state, permissions, and outputs so I can continue without reconstructing everything manually. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-002` | When I delegate work, help me define a bounded task, permitted resources, limits, and expected outcome so the agent cannot silently expand the assignment. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-003` | When an agent or model is selected, show me which capability, provider, model, cost policy, and fallback apply so I understand the execution choice. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-004` | When work is running, show persisted progress, waiting conditions, failures, costs, and evidence so I can supervise without reading every log line. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-005` | When an action is consequential, pause it and give the authorized reviewer enough exact context to decide safely. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-006` | When a run fails or is interrupted, help me diagnose, retry, resume, or cancel it without duplicating side effects. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-007` | When an output is produced, retain it with source, version, permissions, and lifecycle state so I can trust and reuse the correct artifact. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-008` | When context is stored as memory, show its source, scope, age, and verification state so unverified claims do not silently become facts. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-009` | When resources are consumed, attribute usage and cost to the responsible workspace, task, and run so I can control spend. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-010` | When I connect an agent, tool, or MCP server, let me grant the minimum capability and revoke it independently of prompt text. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-011` | When I investigate an event, let me reconstruct identities, policy, approvals, steps, outputs, and side effects from correlated evidence. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-012` | When I manage a workspace, let me define membership, roles, budget, and permitted integrations without affecting other workspaces. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-013` | When a provider becomes unavailable or unsuitable, preserve the task and workspace concepts so I can change implementation without losing core work. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-014` | When I review Mission Control, distinguish real, partial, stale, estimated, failed, and unavailable state so I do not act on a misleading dashboard. | `UCD-001` | `PRD-001` | `TBD` |
| `JTBD-015` | When I operate the local pilot, provide backup, restore, startup, health, and recovery guidance so the platform is not dependent on undocumented knowledge. | `UCD-001` | `PRD-001` | `TBD` |

## 8. Journeys and use cases

### 8.1 Journeys

| Journey | Title | PRD | SRS | E2E test | Evidence |
|---|---|---|---|---|---|
| `JRN-001` | First local onboarding | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-002` | Create an organization context and workspace | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-003` | Register and verify an agent adapter | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-004` | Configure a model profile and provider | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-005` | Create a bounded task | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-006` | Start and monitor a run | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-007` | Handle an approval-required action | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-008` | Reject and revise an approval request | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-009` | Recover an interrupted run | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-010` | Retrieve and review an artifact | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-011` | Store and retrieve governed memory | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-012` | Inspect cost and usage attribution | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-013` | Audit a task from instruction to outcome | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-014` | Verify workspace isolation | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-015` | Back up and restore the local pilot | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-016` | Diagnose adapter or provider failure | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-017` | Cancel a running or waiting run | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-018` | Review Mission Control state integrity | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-019` | Manage workspace members and roles | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-020` | Export authorized evidence | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-F01` | Remote trusted-team access | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-F02` | Multi-agent delegation | `PRD-001` | `SRS-001` | `TBD` | `TBD` |
| `JRN-F03` | Read-only business analytics | `PRD-001` | `SRS-001` | `TBD` | `TBD` |

### 8.2 Use cases

| Use case | Title | Functional trace | Design | Test | Evidence |
|---|---|---|---|---|---|
| `UC-001` | Authenticate locally | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-002` | Create organization context | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-003` | Create workspace | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-004` | Create project | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-005` | Register agent adapter | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-006` | Validate adapter health | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-007` | Create model profile | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-008` | Create bounded task | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-009` | Start run | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-010` | View run timeline | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-011` | Request approval | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-012` | Approve exact action | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-013` | Reject approval | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-014` | Revise approval request | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-015` | Cancel run | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-016` | Retry run step | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-017` | Resume interrupted run | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-018` | Store artifact | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-019` | Retrieve artifact | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-020` | Store memory record | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-021` | Retrieve memory | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-022` | Correct or supersede memory | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-023` | Record audit event | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-024` | View cost attribution | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-025` | Manage workspace membership | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-026` | Assign workspace role | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-027` | Deny cross-workspace access | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-028` | Create backup | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-029` | Restore backup | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-030` | Export evidence package | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-031` | Diagnose adapter failure | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-032` | Review dashboard integrity | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-033` | Revoke future authority | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-034` | Expire approval | `SRS-001` | `TBD` | `TBD` | `TBD` |
| `UC-035` | Mark state stale or unknown | `SRS-001` | `TBD` | `TBD` | `TBD` |

## 9. Product epics

| Epic | Title | Downstream architecture/contracts | Backlog/release |
|---|---|---|---|
| `EPIC-001` | Identity and sessions | IAM-001, SEC-001 | `TBD` |
| `EPIC-002` | Organization, workspaces, projects, and membership | DDD-001, DAT-001, IAM-001 | `TBD` |
| `EPIC-003` | Agent registry and adapters | AGC-001, CAP-001, INT-001 | `TBD` |
| `EPIC-004` | Model profiles, routing, budgets, and provider attribution | MOD-001, INT-001, CST-001 | `TBD` |
| `EPIC-005` | Tasks and durable runs | ORC-001, RUN-001, EVT-001 | `TBD` |
| `EPIC-006` | Approvals and human control | AUT-001, APR-001, SEC-001 | `TBD` |
| `EPIC-007` | Tools, integrations, and permission enforcement | POL-001, SAN-001, INT-001 | `TBD` |
| `EPIC-008` | Memory and knowledge | MEM-001, DAT-001 | `TBD` |
| `EPIC-009` | Artifacts and provenance | ART-001, DAT-001 | `TBD` |
| `EPIC-010` | Audit, execution receipts, and evidence | AUD-001, OBS-001 | `TBD` |
| `EPIC-011` | Usage and cost attribution | CST-001, OBS-001 | `TBD` |
| `EPIC-012` | Mission Control and navigation | UXA-001, DSN-001, A11Y-001 | `TBD` |
| `EPIC-013` | Operations, health, backup, and recovery | DEP-001, OPS-001, BCP-001 | `TBD` |
| `EPIC-014` | Accessibility, responsive design, and usability | A11Y-001, VVR-001, TST-001 | `TBD` |
| `EPIC-015` | Read-only business-system analytics | Post-MVP | `TBD` |
| `EPIC-016` | Media Studio | Post-MVP | `TBD` |
| `EPIC-017` | Multi-agent coordination | Post-MVP | `TBD` |
| `EPIC-018` | Public multi-tenant commercialization | Post-MVP | `TBD` |

## 10. Product-requirement register

| Requirement | Title | Priority | Functional/NFR trace | Design | Test | Evidence | Status |
|---|---|---|---|---|---|---|---|
| `PRD-IDN-001` | The product shall require authentication for every protected view and action. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-002` | The product shall maintain a bounded authenticated session. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-003` | The product shall attribute user-visible and security-relevant actions to an identity. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-004` | The product shall distinguish human users from agent, worker, and integration identities. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-005` | The product shall not grant anonymous fallback access when identity services fail. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-006` | The product should support local authentication suitable for the first pilot. | `Should` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-007` | The product shall protect authentication events and avoid exposing credentials in logs. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-IDN-008` | The product shall show the current user and active organization/workspace context. | `Must` | FR-AUTH | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-001` | The product shall support one organization context in the first MVP. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-002` | The product shall support multiple workspaces inside the organization. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-003` | Each workspace shall have a stable identifier, name, purpose, owner, classification, and policy profile. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-004` | The product shall support projects inside one workspace. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-005` | The product shall prevent data access across workspaces by default. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-006` | The product shall support workspace membership. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-007` | The product shall support predefined roles for owner, operator, approver, auditor, and contributor. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-008` | The product shall display the effective role and permissions for a workspace. | `Should` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-009` | Membership and role changes shall be audited. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-010` | The product shall prevent removal of the last required workspace owner without transfer. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-011` | Tool, memory, artifact, task, run, approval, and cost records shall carry workspace scope. | `Must` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-WSP-012` | The MVP shall exclude public tenant onboarding and cross-organization delegation. | `Won't-MVP` | FR-WSP | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-001` | The product shall provide an agent registry. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-002` | The MVP shall support Hermes as an adapter target. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-003` | The MVP shall support Codex as an adapter target. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-004` | Registration, reachability, health, and validated capability shall be distinct states. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-005` | The product shall record adapter type, identity, version, configuration state, and last validation evidence. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-006` | The product shall support workspace-level adapter enablement. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-007` | The product shall expose declared capabilities and unavailable/unknown capability states. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-008` | The product shall preserve common task, run, approval, artifact, and event concepts across adapters. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-009` | The product shall report adapter-specific limitations transparently. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-010` | An adapter shall not be able to change its own platform permissions. | `Must` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-011` | The product shall support disabling an adapter without deleting its historical evidence. | `Should` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AGT-012` | The MVP shall not provide a public adapter marketplace. | `Won't-MVP` | FR-AGT | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-001` | The product shall support logical model profiles independent of user-facing provider-specific workflows. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-002` | A model profile shall identify provider, provider model ID, intended capabilities, constraints, and validation state. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-003` | The product shall support workspace-level model-profile enablement. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-004` | The product shall support budget or usage limits at least at workspace and task/run level. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-005` | The product shall record the actual provider and model used where available. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-006` | The product shall distinguish profile configuration from successful provider validation. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-007` | The product shall support transparent fallback policy only when explicitly configured. | `Should` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-008` | The product shall apply data-classification and provider-policy checks before sending context. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-009` | The product shall expose delayed, missing, or unavailable usage/cost data. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MOD-010` | The MVP shall not require one specific model provider as a permanent platform dependency. | `Must` | FR-MOD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-001` | The product shall support task creation in a workspace and optional project. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-002` | A task shall define desired outcome, permitted resources, limits, expected artifacts, and data classification. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-003` | The product shall support draft, ready, blocked, active, completed, cancelled, and archived task states. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-004` | The product shall create and persist a run before external execution starts. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-005` | The product shall persist run steps and state transitions. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-006` | The product shall expose queued, starting, running, waiting, paused, retrying, failed, cancelled, completed, stale, and unknown states. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-007` | The product shall perform preflight authorization, adapter, model, budget, tool, and approval checks. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-008` | The product shall support cancellation intent and adapter cancellation where available. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-009` | The product shall support bounded retry for approved retryable steps. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-010` | The product shall support recovery or explicit safe termination after defined interruptions. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-011` | The product shall use idempotency or equivalent safeguards for defined side-effecting operations. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-012` | The product shall retain lineage between original and resumed/retried steps. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-013` | The product shall distinguish completed, partial, failed, stale, and unknown results. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-014` | The product shall generate a basic execution receipt for accepted runs. | `Must` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-RUN-015` | The MVP shall exclude unattended open-ended runs without time, cost, and stop bounds. | `Won't-MVP` | FR-RUN / FR-TSK | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-001` | The product shall classify actions by side effect and approval policy. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-002` | The product shall block consequential actions without a valid approval. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-003` | An approval request shall identify requester, task, run, exact action, parameters, target, risk, reason, expiry, and expected effects. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-004` | The product shall support approve, reject, request revision, expire, cancel, and invalidate outcomes. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-005` | Approval shall be bound to exact parameters and target. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-006` | The product shall verify approver authority at decision time and execution time. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-007` | The product shall prevent double consumption or replay of an approval. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-008` | Approval expiry shall block execution and require renewal. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-009` | The product shall preserve rejection and revision reasons. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-010` | The product shall allow revocation of future authority. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-011` | The product shall provide an approval inbox prioritized by risk and age. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-012` | The product should provide plain-language summary and technical detail. | `Should` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-013` | The MVP shall treat commit, push, pull-request creation, merge, deletion, external messaging, production access, secret access, financial modification, destructive database action, public publication, executable installation, and permission expansion as candidate approval-required classes. | `Must` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-APR-014` | The MVP shall not autonomously merge source changes. | `Won't-MVP` | FR-APR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-001` | The product shall provide a registry of tools and integrations. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-002` | Tool availability shall not grant permission. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-003` | The product shall evaluate identity, workspace, capability, resource scope, data class, network target, side effect, budget, and approval before invocation. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-004` | The product shall support workspace-scoped tool enablement. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-005` | The product shall support bounded filesystem/repository scopes. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-006` | The product shall restrict network destinations according to policy. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-007` | The product shall record a receipt for accepted tool actions. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-008` | The product shall expose denied requests safely without leaking protected metadata. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-009` | The product shall support disabling/revoking a tool capability. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-010` | The product shall not treat MCP connectivity as authorization. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-011` | Package or executable installation shall require explicit policy and approval. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-TOL-012` | The MVP shall expose only a minimal approved tool set needed for pilot journeys. | `Must` | FR-TOL | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-001` | The product shall provide a workspace-scoped memory/knowledge foundation. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-002` | A memory record shall include source, scope, producer, creation time, classification, and verification/confidence state. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-003` | Generated or inferred content shall remain visibly labeled. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-004` | The product shall prevent ordinary storage of secrets as memory. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-005` | The product shall apply permission checks at ingestion, storage, retrieval, export, correction, and deletion. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-006` | The product shall deny cross-workspace memory retrieval by default. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-007` | Retrieval should expose source, age, and reason for inclusion. | `Should` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-008` | The product shall support correction, supersession, and controlled deletion. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-009` | The product shall support retention state. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-010` | The MVP shall not claim perfect, complete, or indefinite memory. | `Won't-MVP` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-011` | Automatic memory writes shall be policy-governed. | `Must` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-MEM-012` | Conflicts with an authoritative source shall be visible rather than silently merged. | `Should` | FR-MEM | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-001` | The product shall store artifact metadata and a retained content reference. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-002` | Artifact metadata shall include workspace, project, task, run, step, producer, media type, size, integrity, classification, lifecycle, and timestamp. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-003` | The product shall support at least text, Markdown, JSON, code patch, test log, and permitted small-file artifacts. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-004` | The product shall support generated, under-review, accepted, rejected, superseded, archived, deleted, and unavailable states. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-005` | The product shall prevent unauthorized artifact discovery and retrieval. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-006` | The product shall provide safe preview behavior. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-007` | Integrity mismatch shall be visible and block trusted use. | `Must` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-008` | The product shall preserve version or derivative relationships. | `Should` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-009` | Exported evidence packages shall themselves be artifacts with provenance. | `Should` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-ART-010` | Full image/video/voice generation workflows shall remain post-MVP. | `Won't-MVP` | FR-ART | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-001` | The product shall record correlated audit events for security-relevant and operationally significant actions. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-002` | Audit views shall be read-only for auditor roles. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-003` | The product shall distinguish platform fact, provider report, derived estimate, stale data, and missing data. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-004` | Audit records shall avoid exposing raw secrets. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-005` | The product shall preserve approval decision and execution linkage. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-006` | The product shall preserve retry, resume, cancellation, and failure lineage. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-007` | The product shall expose evidence gaps explicitly. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-008` | The product should support filtered authorized evidence export. | `Should` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-009` | Export shall exclude unrelated workspace and prohibited fields. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-AUD-010` | The MVP shall maintain enough trace completeness to validate the defined vertical slice. | `Must` | FR-AUD | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-001` | The product shall record supported model/token/tool usage events. | `Must` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-002` | Usage shall be attributable to organization, workspace, project where applicable, task, run, and provider/model/tool. | `Must` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-003` | Cost values shall identify currency, period, source, and freshness. | `Must` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-004` | Provider-reported, calculated, estimated, pending, unavailable, and unattributed values shall be distinct. | `Must` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-005` | The product shall surface reconciliation mismatches. | `Should` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-006` | The product shall support workspace and run-level budget thresholds. | `Must` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-007` | The cost view shall not present provider spend as business profit or accounting fact. | `Must` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-CST-008` | The product should support export of authorized cost detail. | `Should` | FR-CST | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-001` | The product shall provide responsive web Mission Control. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-002` | Mission Control shall summarize active tasks, runs, approvals, failures, costs, and health from persisted sources. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-003` | The UI shall distinguish zero, unavailable, stale, estimated, partial, failed, and unknown. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-004` | Every summary metric shall provide a path to supporting detail. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-005` | The primary navigation shall include workspaces, projects, tasks, runs, approvals, agents, models, tools/integrations, memory, artifacts, costs, audit, and operations. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-006` | The UI shall keep active organization/workspace/project context visible. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-007` | The UI shall use progressive disclosure for technical detail. | `Should` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-008` | Error states shall explain what failed, what is known, what may have happened, and next actions. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-009` | Empty states shall distinguish no data, missing configuration, denied access, and unavailable collection. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-010` | The UI shall avoid silently using mock data in accepted workflows. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-011` | Approval and critical failure states shall be visible without relying only on color. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-UI-012` | Mobile shall prioritize review and status; consequential execution shall remain restricted unless explicitly approved. | `Must` | FR-UI | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-001` | The MVP shall support a documented local single-node Linux/WSL deployment. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-002` | The product shall expose health for control plane, adapters, provider validation, storage, tool gateway, and event processing. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-003` | Health shall distinguish registered, reachable, validated, degraded, failed, stale, and unknown. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-004` | The product shall support controlled configuration without committing secrets. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-005` | The product shall provide a backup procedure covering defined retained data. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-006` | The product shall provide a restore procedure. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-007` | Partial backup or restore shall be visibly classified as partial. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-008` | The product shall record operational recovery evidence. | `Should` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-009` | The MVP shall not require high-availability infrastructure. | `Won't-MVP` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-010` | Remote access shall be excluded by default until separately approved. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-011` | The system shall support clean startup and shutdown without corrupting accepted state. | `Must` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-OPS-012` | The product shall provide an operator-visible version/build identity. | `Should` | FR-OPS | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-001` | The product shall target WCAG 2.2 AA for defined MVP workflows. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-002` | All Must journeys shall be completable by keyboard. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-003` | Interactive elements shall have accessible names, roles, and states. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-004` | Status shall not rely on color alone. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-005` | Focus shall be visible and follow logical order. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-006` | Content shall reflow at approved responsive widths without global horizontal scrolling. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-007` | The product shall support text zoom/scaling and reduced motion. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-008` | Errors and dynamic status changes shall be perceivable to assistive technology. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-009` | The product shall use plain, consistent terminology and expose technical detail progressively. | `Should` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-010` | Date, time, currency, and time-zone context shall be explicit. | `Should` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-011` | The content architecture should be localization-ready. | `Should` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-A11Y-012` | The MVP shall remain desktop-primary while supporting review-oriented tablet/mobile layouts. | `Must` | FR-UI / NFR-A11Y | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-001` | Every user-visible success state shall be backed by persisted or externally verified evidence. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-002` | Every protected record shall carry organization/workspace scope where applicable. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-003` | Every consequential operation shall be attributable to an identity. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-004` | Every provider-, model-, adapter-, tool-, approval-, artifact-, and cost-dependent view shall represent unknown/unavailable state explicitly. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-005` | Secrets shall remain outside prompts, source control, ordinary memory, artifacts, and logs. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-006` | No prompt shall override platform authorization. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-007` | No accepted workflow shall silently depend on non-persistent mock data. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-008` | Product actions shall be traceable from objective to requirement, architecture, contract, backlog, test, evidence, and release. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-009` | Final technology choices shall be recorded in architecture documents and ADRs rather than hidden in product requirements. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-010` | Unsupported functionality shall be displayed as unavailable or not implemented, not simulated as operational. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-011` | Product metrics shall state source, freshness, definition, and uncertainty. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |
| `PRD-XC-012` | Generated analysis shall remain separate from authoritative source records. | `Must` | Cross-cutting SRS/NFR | `TBD` | `TBD` | `TBD` | `Drafted` |

## 11. Functional-requirement register

| Functional requirement | Title | Design/contract owner | Verification family | Implementation | Evidence | Status |
|---|---|---|---|---|---|---|
| `FR-AUTH-001` | Authenticate access to protected capabilities | IAM-001, SEC-001, API-001 | authentication/session/negative-access | `TBD` | `TBD` | `Drafted` |
| `FR-AUTH-002` | Enforce session expiry and reauthentication | IAM-001, SEC-001, API-001 | authentication/session/negative-access | `TBD` | `TBD` | `Drafted` |
| `FR-AUTH-003` | Distinguish human, agent, worker, and integration identities | IAM-001, SEC-001, API-001 | authentication/session/negative-access | `TBD` | `TBD` | `Drafted` |
| `FR-AUTH-004` | Display active identity and scope | IAM-001, SEC-001, API-001 | authentication/session/negative-access | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-001` | Create the first organization context | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-002` | Create and persist a workspace | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-003` | Create and manage projects inside a workspace | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-004` | Enforce workspace isolation | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-005` | Manage workspace membership | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-006` | Assign predefined workspace roles | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-WSP-007` | Carry workspace scope on protected records | DDD-001, DAT-001, IAM-001, API-001 | RBAC/isolation/membership | `TBD` | `TBD` | `Drafted` |
| `FR-AGT-001` | Register an agent adapter | SAD-001, INT-001, AGC-001, CAP-001 | adapter contract/conformance | `TBD` | `TBD` | `Drafted` |
| `FR-AGT-002` | Validate adapter reachability and health | SAD-001, INT-001, AGC-001, CAP-001 | adapter contract/conformance | `TBD` | `TBD` | `Drafted` |
| `FR-AGT-003` | Support Hermes adapter target | SAD-001, INT-001, AGC-001, CAP-001 | adapter contract/conformance | `TBD` | `TBD` | `Drafted` |
| `FR-AGT-004` | Support Codex adapter target | SAD-001, INT-001, AGC-001, CAP-001 | adapter contract/conformance | `TBD` | `TBD` | `Drafted` |
| `FR-AGT-005` | Expose declared adapter capabilities | SAD-001, INT-001, AGC-001, CAP-001 | adapter contract/conformance | `TBD` | `TBD` | `Drafted` |
| `FR-AGT-006` | Enable or disable adapters by workspace | SAD-001, INT-001, AGC-001, CAP-001 | adapter contract/conformance | `TBD` | `TBD` | `Drafted` |
| `FR-MOD-001` | Create a provider-neutral model profile | INT-001, MOD-001, CST-001 | provider/profile/budget | `TBD` | `TBD` | `Drafted` |
| `FR-MOD-002` | Validate model profile availability | INT-001, MOD-001, CST-001 | provider/profile/budget | `TBD` | `TBD` | `Drafted` |
| `FR-MOD-003` | Enable model profiles by workspace | INT-001, MOD-001, CST-001 | provider/profile/budget | `TBD` | `TBD` | `Drafted` |
| `FR-MOD-004` | Apply model budget and usage limits | INT-001, MOD-001, CST-001 | provider/profile/budget | `TBD` | `TBD` | `Drafted` |
| `FR-MOD-005` | Record actual provider and model used | INT-001, MOD-001, CST-001 | provider/profile/budget | `TBD` | `TBD` | `Drafted` |
| `FR-TSK-001` | Create a draft task | DDD-001, ORC-001, API-001 | validation/lifecycle/versioning | `TBD` | `TBD` | `Drafted` |
| `FR-TSK-002` | Define bounded task scope and limits | DDD-001, ORC-001, API-001 | validation/lifecycle/versioning | `TBD` | `TBD` | `Drafted` |
| `FR-TSK-003` | Manage task lifecycle states | DDD-001, ORC-001, API-001 | validation/lifecycle/versioning | `TBD` | `TBD` | `Drafted` |
| `FR-TSK-004` | Validate task readiness | DDD-001, ORC-001, API-001 | validation/lifecycle/versioning | `TBD` | `TBD` | `Drafted` |
| `FR-TSK-005` | Version or audit material task changes | DDD-001, ORC-001, API-001 | validation/lifecycle/versioning | `TBD` | `TBD` | `Drafted` |
| `FR-TSK-006` | Archive a task without deleting evidence | DDD-001, ORC-001, API-001 | validation/lifecycle/versioning | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-001` | Create a persisted run before dispatch | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-002` | Perform run preflight | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-003` | Dispatch a bounded execution request | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-004` | Persist run steps and events | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-005` | Represent run states explicitly | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-006` | Cancel a run | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-007` | Retry an eligible step | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-008` | Detect interrupted or stale execution | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-009` | Resume a supported interrupted run | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-RUN-010` | Generate a run execution receipt | ORC-001, RUN-001, EVT-001, API-001 | state/fault/idempotency/recovery | `TBD` | `TBD` | `Drafted` |
| `FR-APR-001` | Classify proposed actions by side effect and approval policy | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-002` | Create an exact approval request | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-003` | Review an approval request | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-004` | Approve an exact action | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-005` | Reject or request revision | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-006` | Expire and invalidate approval requests | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-007` | Consume approval exactly once | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-APR-008` | Revoke future authority | AUT-001, APR-001, SEC-001, THR-001 | expiry/invalidation/replay/concurrency | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-001` | Register a tool or integration capability | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-002` | Enable tools by workspace and scope | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-003` | Evaluate tool invocation policy | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-004` | Enforce bounded filesystem and repository access | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-005` | Enforce network destination restrictions | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-006` | Require approval for executable installation or permission expansion | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-TOL-007` | Record tool execution receipt | INT-001, POL-001, SAN-001, MCP-001 | policy/sandbox/filesystem/network | `TBD` | `TBD` | `Drafted` |
| `FR-MEM-001` | Create a governed memory record | MEM-001, DAT-001, SEC-001 | provenance/isolation/retention | `TBD` | `TBD` | `Drafted` |
| `FR-MEM-002` | Retrieve memory within authorized scope | MEM-001, DAT-001, SEC-001 | provenance/isolation/retention | `TBD` | `TBD` | `Drafted` |
| `FR-MEM-003` | Label generated, inferred, verified, and authoritative knowledge | MEM-001, DAT-001, SEC-001 | provenance/isolation/retention | `TBD` | `TBD` | `Drafted` |
| `FR-MEM-004` | Correct or supersede memory | MEM-001, DAT-001, SEC-001 | provenance/isolation/retention | `TBD` | `TBD` | `Drafted` |
| `FR-MEM-005` | Delete or expire memory under policy | MEM-001, DAT-001, SEC-001 | provenance/isolation/retention | `TBD` | `TBD` | `Drafted` |
| `FR-MEM-006` | Govern automatic memory writes | MEM-001, DAT-001, SEC-001 | provenance/isolation/retention | `TBD` | `TBD` | `Drafted` |
| `FR-ART-001` | Store an artifact with provenance | ART-001, DAT-001, API-001 | storage/integrity/lifecycle/preview | `TBD` | `TBD` | `Drafted` |
| `FR-ART-002` | Support initial artifact types | ART-001, DAT-001, API-001 | storage/integrity/lifecycle/preview | `TBD` | `TBD` | `Drafted` |
| `FR-ART-003` | Retrieve and preview an authorized artifact | ART-001, DAT-001, API-001 | storage/integrity/lifecycle/preview | `TBD` | `TBD` | `Drafted` |
| `FR-ART-004` | Manage artifact lifecycle | ART-001, DAT-001, API-001 | storage/integrity/lifecycle/preview | `TBD` | `TBD` | `Drafted` |
| `FR-ART-005` | Validate artifact integrity | ART-001, DAT-001, API-001 | storage/integrity/lifecycle/preview | `TBD` | `TBD` | `Drafted` |
| `FR-ART-006` | Create an evidence export artifact | ART-001, DAT-001, API-001 | storage/integrity/lifecycle/preview | `TBD` | `TBD` | `Drafted` |
| `FR-AUD-001` | Record correlated audit events | AUD-001, OBS-001, SEC-001 | schema/correlation/redaction/tamper | `TBD` | `TBD` | `Drafted` |
| `FR-AUD-002` | Provide a read-only audit timeline | AUD-001, OBS-001, SEC-001 | schema/correlation/redaction/tamper | `TBD` | `TBD` | `Drafted` |
| `FR-AUD-003` | Link approvals to execution outcomes | AUD-001, OBS-001, SEC-001 | schema/correlation/redaction/tamper | `TBD` | `TBD` | `Drafted` |
| `FR-AUD-004` | Preserve retry, resume, cancellation, and failure lineage | AUD-001, OBS-001, SEC-001 | schema/correlation/redaction/tamper | `TBD` | `TBD` | `Drafted` |
| `FR-AUD-005` | Redact secrets from audit evidence | AUD-001, OBS-001, SEC-001 | schema/correlation/redaction/tamper | `TBD` | `TBD` | `Drafted` |
| `FR-AUD-006` | Expose evidence gaps and collection failures | AUD-001, OBS-001, SEC-001 | schema/correlation/redaction/tamper | `TBD` | `TBD` | `Drafted` |
| `FR-CST-001` | Record model and tool usage events | CST-001, OBS-001 | usage/reconciliation/threshold | `TBD` | `TBD` | `Drafted` |
| `FR-CST-002` | Calculate and display attributed cost | CST-001, OBS-001 | usage/reconciliation/threshold | `TBD` | `TBD` | `Drafted` |
| `FR-CST-003` | Surface unattributed and reconciliation mismatches | CST-001, OBS-001 | usage/reconciliation/threshold | `TBD` | `TBD` | `Drafted` |
| `FR-CST-004` | Enforce cost thresholds | CST-001, OBS-001 | usage/reconciliation/threshold | `TBD` | `TBD` | `Drafted` |
| `FR-CST-005` | Separate AI operating cost from business profit | CST-001, OBS-001 | usage/reconciliation/threshold | `TBD` | `TBD` | `Drafted` |
| `FR-UI-001` | Provide a responsive Mission Control | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-UI-002` | Display controlled state semantics | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-UI-003` | Provide primary domain navigation | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-UI-004` | Provide actionable error and empty states | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-UI-005` | Provide progressive disclosure of evidence | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-UI-006` | Support accessible interaction | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-UI-007` | Restrict consequential mobile actions | UXA-001, DSN-001, A11Y-001, VVR-001 | E2E/responsive/accessibility/comprehension | `TBD` | `TBD` | `Drafted` |
| `FR-OPS-001` | Expose component health and diagnostics | DEP-001, OPS-001, BCP-001, OBS-001 | health/restart/backup/restore/exposure | `TBD` | `TBD` | `Drafted` |
| `FR-OPS-002` | Support controlled local configuration | DEP-001, OPS-001, BCP-001, OBS-001 | health/restart/backup/restore/exposure | `TBD` | `TBD` | `Drafted` |
| `FR-OPS-003` | Start and stop cleanly | DEP-001, OPS-001, BCP-001, OBS-001 | health/restart/backup/restore/exposure | `TBD` | `TBD` | `Drafted` |
| `FR-OPS-004` | Create a backup with manifest and integrity evidence | DEP-001, OPS-001, BCP-001, OBS-001 | health/restart/backup/restore/exposure | `TBD` | `TBD` | `Drafted` |
| `FR-OPS-005` | Restore from an approved backup | DEP-001, OPS-001, BCP-001, OBS-001 | health/restart/backup/restore/exposure | `TBD` | `TBD` | `Drafted` |
| `FR-OPS-006` | Keep default deployment local and non-public | DEP-001, OPS-001, BCP-001, OBS-001 | health/restart/backup/restore/exposure | `TBD` | `TBD` | `Drafted` |

## 12. Non-functional-requirement register

| NFR | Title | Design/operations owner | Verification family | Evidence | Release gate | Status |
|---|---|---|---|---|---|---|
| `NFR-PERF-001` | Mission Control initial render responsiveness | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-002` | Primary navigation response | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-003` | Local API response for ordinary reads | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-004` | Ordinary write acknowledgement | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-005` | Approval inbox freshness | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-006` | Run state propagation | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-007` | Search responsiveness | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-PERF-008` | External latency representation | SAD-001, DAT-001, ORC-001, UXA-001 | performance/load | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-001` | Persisted terminal run state reliability | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-002` | Approval-policy enforcement reliability | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-003` | Resumable interruption success | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-004` | Cross-workspace isolation reliability | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-005` | Authorized artifact retrieval reliability | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-006` | Trace completeness | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-007` | Adapter conformance | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-008` | Idempotent duplicate protection | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-009` | Clean restart data preservation | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-REL-010` | Unexpected process interruption behavior | SAD-001, ORC-001, RUN-001 | reliability/restart/conformance | `TBD` | `TBD` | `Drafted` |
| `NFR-AVL-001` | Local pilot service availability | OPS-001, OBS-001 | availability/outage | `TBD` | `TBD` | `Drafted` |
| `NFR-AVL-002` | Graceful degraded mode | OPS-001, OBS-001 | availability/outage | `TBD` | `TBD` | `Drafted` |
| `NFR-BCP-001` | Recovery Time Objective for local pilot | BCP-001, OPS-001, DAT-001 | backup/recovery exercise | `TBD` | `TBD` | `Drafted` |
| `NFR-BCP-002` | Recovery Point Objective | BCP-001, OPS-001, DAT-001 | backup/recovery exercise | `TBD` | `TBD` | `Drafted` |
| `NFR-BCP-003` | Backup integrity verification | BCP-001, OPS-001, DAT-001 | backup/recovery exercise | `TBD` | `TBD` | `Drafted` |
| `NFR-BCP-004` | Restore completeness reporting | BCP-001, OPS-001, DAT-001 | backup/recovery exercise | `TBD` | `TBD` | `Drafted` |
| `NFR-BCP-005` | Recovery exercise frequency | BCP-001, OPS-001, DAT-001 | backup/recovery exercise | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-001` | Fail-closed authorization | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-002` | Least-privilege default | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-003` | Secret exclusion from ordinary content | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-004` | Encryption in transit | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-005` | Encryption at rest for sensitive data | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-006` | No unrestricted host access | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-007` | Network egress restriction | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-008` | Approval replay resistance | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-009` | Audit integrity protection | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-010` | Security-event attribution | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-011` | Dependency and supply-chain control | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-012` | Secure preview behavior | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-013` | Security patch response | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-SEC-014` | Default non-public exposure | SEC-001, THR-001, IAM-001, SAN-001 | security/negative | `TBD` | `TBD` | `Drafted` |
| `NFR-PRI-001` | Data minimization | PRI-001, DAT-002, SEC-001 | privacy/lifecycle | `TBD` | `TBD` | `Drafted` |
| `NFR-PRI-002` | Purpose-bound telemetry | PRI-001, DAT-002, SEC-001 | privacy/lifecycle | `TBD` | `TBD` | `Drafted` |
| `NFR-PRI-003` | Deletion and correction propagation | PRI-001, DAT-002, SEC-001 | privacy/lifecycle | `TBD` | `TBD` | `Drafted` |
| `NFR-PRI-004` | Provider data handling transparency | PRI-001, DAT-002, SEC-001 | privacy/lifecycle | `TBD` | `TBD` | `Drafted` |
| `NFR-PRI-005` | Sensitive-data exclusion baseline | PRI-001, DAT-002, SEC-001 | privacy/lifecycle | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-001` | WCAG 2.2 AA baseline | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-002` | Keyboard-only completion | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-003` | Accessible names, roles, and states | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-004` | Non-color state communication | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-005` | Responsive reflow | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-006` | Text scaling | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-007` | Reduced motion support | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-A11Y-008` | Dynamic status announcement | A11Y-001, DSN-001, VVR-001 | accessibility | `TBD` | `TBD` | `Drafted` |
| `NFR-USAB-001` | Defined journey completion | UXA-001, UCD-001 | usability | `TBD` | `TBD` | `Drafted` |
| `NFR-USAB-002` | Run-state comprehension | UXA-001, UCD-001 | usability | `TBD` | `TBD` | `Drafted` |
| `NFR-USAB-003` | Approval comprehension | UXA-001, UCD-001 | usability | `TBD` | `TBD` | `Drafted` |
| `NFR-USAB-004` | Artifact provenance comprehension | UXA-001, UCD-001 | usability | `TBD` | `TBD` | `Drafted` |
| `NFR-USAB-005` | Workspace isolation mental model | UXA-001, UCD-001 | usability | `TBD` | `TBD` | `Drafted` |
| `NFR-USAB-006` | Misleading state prevention | UXA-001, UCD-001 | usability | `TBD` | `TBD` | `Drafted` |
| `NFR-OBS-001` | End-to-end correlation coverage | OBS-001, AUD-001, EVT-001 | observability/fault | `TBD` | `TBD` | `Drafted` |
| `NFR-OBS-002` | Health freshness disclosure | OBS-001, AUD-001, EVT-001 | observability/fault | `TBD` | `TBD` | `Drafted` |
| `NFR-OBS-003` | Structured log coverage | OBS-001, AUD-001, EVT-001 | observability/fault | `TBD` | `TBD` | `Drafted` |
| `NFR-OBS-004` | Sensitive-log redaction | OBS-001, AUD-001, EVT-001 | observability/fault | `TBD` | `TBD` | `Drafted` |
| `NFR-OBS-005` | Actionable alerting | OBS-001, AUD-001, EVT-001 | observability/fault | `TBD` | `TBD` | `Drafted` |
| `NFR-OBS-006` | Unknown-state propagation | OBS-001, AUD-001, EVT-001 | observability/fault | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-001` | Modular adapter replaceability | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-002` | Controlled dependency direction | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-003` | Automated test coverage of critical logic | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-004` | Static analysis and type safety | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-005` | Documentation traceability | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-006` | Schema and contract versioning | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-007` | Database migration safety | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-008` | Reproducible local development setup | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-MNT-009` | No unresolved critical quality gate | SAD-001, DEV-001, QAG-001 | static/contract/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-PORT-001` | Supported local Linux/WSL environment | DEP-001, DEV-001, OPS-001 | environment/compatibility | `TBD` | `TBD` | `Drafted` |
| `NFR-PORT-002` | Browser compatibility | DEP-001, DEV-001, OPS-001 | environment/compatibility | `TBD` | `TBD` | `Drafted` |
| `NFR-PORT-003` | Data export portability | DEP-001, DEV-001, OPS-001 | environment/compatibility | `TBD` | `TBD` | `Drafted` |
| `NFR-INT-001` | Adapter protocol isolation | INT-001, AGC-001, ADRs | interoperability | `TBD` | `TBD` | `Drafted` |
| `NFR-INT-002` | Standards adoption decision discipline | INT-001, AGC-001, ADRs | interoperability | `TBD` | `TBD` | `Drafted` |
| `NFR-INT-003` | Backward compatibility for stored evidence | INT-001, AGC-001, ADRs | interoperability | `TBD` | `TBD` | `Drafted` |
| `NFR-CAP-001` | Initial workspace capacity | SAD-001, DAT-001, ORC-001 | capacity/load | `TBD` | `TBD` | `Drafted` |
| `NFR-CAP-002` | Initial retained run capacity | SAD-001, DAT-001, ORC-001 | capacity/load | `TBD` | `TBD` | `Drafted` |
| `NFR-CAP-003` | Initial artifact metadata capacity | SAD-001, DAT-001, ORC-001 | capacity/load | `TBD` | `TBD` | `Drafted` |
| `NFR-CAP-004` | Pilot concurrency | SAD-001, DAT-001, ORC-001 | capacity/load | `TBD` | `TBD` | `Drafted` |
| `NFR-CAP-005` | Resource-bounded execution | SAD-001, DAT-001, ORC-001 | capacity/load | `TBD` | `TBD` | `Drafted` |
| `NFR-SCL-001` | Scale-out readiness without MVP implementation | SAD-001, ORC-001, DAT-001 | scale-readiness | `TBD` | `TBD` | `Drafted` |
| `NFR-COST-001` | Cost attribution coverage | CST-001, OBS-001 | cost/threshold | `TBD` | `TBD` | `Drafted` |
| `NFR-COST-002` | Cost-status transparency | CST-001, OBS-001 | cost/threshold | `TBD` | `TBD` | `Drafted` |
| `NFR-COST-003` | Budget enforcement latency | CST-001, OBS-001 | cost/threshold | `TBD` | `TBD` | `Drafted` |
| `NFR-COST-004` | No hidden provider fallback cost | CST-001, OBS-001 | cost/threshold | `TBD` | `TBD` | `Drafted` |
| `NFR-COST-005` | Reference operating-cost baseline | CST-001, OBS-001 | cost/threshold | `TBD` | `TBD` | `Drafted` |
| `NFR-DAT-001` | Referential integrity for core records | DDD-001, DAT-001, DCT-001 | integrity/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-DAT-002` | Durable acknowledgement semantics | DDD-001, DAT-001, DCT-001 | integrity/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-DAT-003` | Time consistency and ordering | DDD-001, DAT-001, DCT-001 | integrity/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-DAT-004` | No silent data truncation | DDD-001, DAT-001, DCT-001 | integrity/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-DAT-005` | Source-of-truth separation | DDD-001, DAT-001, DCT-001 | integrity/migration | `TBD` | `TBD` | `Drafted` |
| `NFR-L10N-001` | Localization-ready user interface | DSN-001, A11Y-001, DEV-001 | localization | `TBD` | `TBD` | `Drafted` |
| `NFR-L10N-002` | Explicit locale-sensitive formatting | DSN-001, A11Y-001, DEV-001 | localization | `TBD` | `TBD` | `Drafted` |
| `NFR-L10N-003` | Controlled terminology consistency | DSN-001, A11Y-001, DEV-001 | localization | `TBD` | `TBD` | `Drafted` |
| `NFR-RELSE-001` | Release provenance | REL-001, DEV-001, OPS-001 | release/recovery | `TBD` | `TBD` | `Drafted` |
| `NFR-RELSE-002` | Rollback or forward-recovery plan | REL-001, DEV-001, OPS-001 | release/recovery | `TBD` | `TBD` | `Drafted` |
| `NFR-COMP-001` | License and third-party notice control | QAG-001, DEV-001, DAT-002 | license/retention/exception | `TBD` | `TBD` | `Drafted` |
| `NFR-COMP-002` | Evidence retention policy completeness | QAG-001, DEV-001, DAT-002 | license/retention/exception | `TBD` | `TBD` | `Drafted` |
| `NFR-COMP-003` | Documented risk acceptance | QAG-001, DEV-001, DAT-002 | license/retention/exception | `TBD` | `TBD` | `Drafted` |

## 13. Autonomy-action register

| Action | Action class | Risk | Max autonomy | Decision | Control design | Conformance test | Evidence |
|---|---|---|---|---|---|---|---|
| `ACT-001` | Read authorized workspace metadata | `R0` | `L1` | `ALLOW` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-002` | Read authorized project files or repository content | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-003` | Search authorized tasks, runs, artifacts, audit, or memory | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-004` | Create or update a draft task | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-005` | Mark a task ready | `R2` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-006` | Start a bounded run | `R2` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-007` | Cancel a run | `R2` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-008` | Retry an idempotent low-risk step | `R2` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-009` | Resume from a verified checkpoint | `R2` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-010` | Retry or resume a consequential step | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-011` | Create a draft text/Markdown/JSON/code-patch/test-log artifact | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-012` | Accept an artifact as reviewed output | `R2` | `L3` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-013` | Publish artifact outside the workspace | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-014` | Delete artifact content or metadata | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-015` | Archive or supersede an artifact | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-016` | Write temporary working context | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-017` | Write durable generated memory under pre-approved type | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-018` | Promote memory to verified or authoritative status | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-019` | Correct or supersede memory | `R2` | `L3` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-020` | Delete durable memory | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-021` | Create or modify an approved working file inside a sandbox | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-022` | Delete an approved working file | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-023` | Access a file outside approved workspace mounts | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-024` | Run an approved read-only diagnostic command | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-025` | Run approved tests or build inside sandbox | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-026` | Run an arbitrary shell command | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-027` | Install a package or executable dependency | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-028` | Upgrade an approved dependency within pinned policy | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-029` | Call an approved model/provider endpoint | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-030` | Call an approved read-only external API | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-031` | Send data to an unapproved destination | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-032` | Use a secret reference through an approved capability | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-033` | Display, export, copy, or store a raw secret | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-034` | Read Git status, log, diff, or branch metadata | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-035` | Create or modify an uncommitted patch in approved worktree | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-036` | Create a Git commit | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-037` | Push a branch | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-038` | Create a pull request | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-039` | Merge a pull request | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-040` | Force push, delete protected branch, rewrite shared history | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-041` | Draft an external e-mail or message | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-042` | Send an external e-mail or message | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-043` | Create or modify a calendar event with invitees | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-044` | Read authorized calendar availability | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-045` | Read approved ERP/CRM/accounting data | `R3` | `L3` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-046` | Write or modify ERP/CRM/accounting records | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-047` | Create, modify, approve, or post a financial transaction | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-048` | Access a production system | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-049` | Read approved local Agent OS application data through governed API | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-050` | Execute destructive database operation | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-051` | Apply an approved application migration | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-052` | Create a backup | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-053` | Restore a backup | `R4` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-054` | Add a workspace member | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-055` | Change a workspace role or approver authority | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-056` | Create or expand platform-administrator authority | `R4` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-057` | Register an adapter, tool, or MCP server | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-058` | Enable a registered capability for a workspace | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-059` | Expand filesystem, network, data, model, or tool permission | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-060` | Revoke or reduce a permission | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-061` | Create or update a model profile without secret disclosure | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-062` | Change routing or fallback policy | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-063` | Change a workspace or task budget limit | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-064` | Change an autonomy or approval policy | `R4` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-065` | Disable audit, approval, sandbox, or workspace-isolation control | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-066` | Expose the local service remotely | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-067` | Restart an unhealthy non-production local component | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-068` | Deploy to production | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-069` | Read authorized audit evidence | `R1` | `L2` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-070` | Export an evidence package | `R3` | `L4` | `REQUIRE_APPROVAL` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-071` | Modify or delete audit evidence | `R4` | `L0` | `DENY` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |
| `ACT-072` | Trigger emergency stop / revoke future execution | `R2` | `L3` | `ALLOW_WITH_GUARDS` | IAM-001 / POL-001 / APR-001 / SAN-001 | `TBD` | `TBD` |

## 14. Required downstream contributions

| Document | Required RTM contribution |
|---|---|
| `SAD-001` | Map FR/NFR domains to system components and decisions |
| `C4-001`, `C4-002` | Map actors, systems, containers, and trust boundaries |
| `DDD-001` | Map FRs to aggregates, entities, and domain services |
| `DAT-001`, `DCT-001` | Map data ownership, stores, schemas, and retention |
| `MEM-001` | Map memory requirements and lifecycle controls |
| `ORC-001` | Map task/run/retry/resume requirements |
| `INT-001` | Map adapter, provider, tool, and protocol requirements |
| `SEC-001`, `THR-001` | Map controls and threats to FR/NFR/AUT requirements |
| `AGC-001`, `CAP-001`, `MOD-001` | Map adapter/model requirements to contracts |
| `RUN-001`, `APR-001`, `ART-001`, `AUD-001` | Map states and evidence to schemas |
| `API-001`, `EVT-001` | Map requirements to operations and events |
| `TST-001` | Assign test IDs and verification methods |
| `QAG-001` | Assign blocking quality gates |
| `OPS-001`, `OBS-001`, `BCP-001` | Map operations and recovery evidence |

## 15. Mandatory traceability gates

Before development at scale:

- every `Must` PRD requirement maps to one or more FR/NFR/AUT items;
- every `Must` FR/NFR has a design owner;
- every consequential `ACT-*` maps to policy, approval, sandbox, and test ownership;
- every blocking open decision has an owner.

Before MVP acceptance:

- 100% of Must FR/NFR items have test IDs and evidence status;
- 100% of approval-required actions have positive and negative tests;
- 100% of workspace access paths have isolation tests;
- all deferred items have rationale and owner;
- no accepted item relies only on a prototype or mock.

## 16. Change-impact rules

| Changed artifact | Minimum impact review |
|---|---|
| `VSN-001` | Scope, personas, PRD, SRS, NFR, AUT, architecture, tests |
| `SCP-001` | PRD, SRS, AUT, SAD, SEC, roadmap |
| `PER-001` | UCD, PRD, UX, usability tests |
| `UCD-001` | PRD, SRS, UX, E2E tests |
| `PRD-001` | SRS, NFR, AUT, architecture, backlog |
| `SRS-001` | Architecture, contracts, implementation, tests |
| `NFR-001` | Architecture, operations, quality gates, tests |
| `AUT-001` | IAM, policy, approval, sandbox, security tests |
| Architecture/ADR | Contracts, implementation, migration, tests |
| Contract/API/event | Adapters, clients, compatibility tests |

## 17. Current traceability gaps

Expected gaps at this stage:

- architecture-component IDs;
- ADRs;
- contract/schema IDs;
- backlog and issue IDs;
- source-code paths;
- test-case IDs;
- CI/evidence IDs;
- release identifiers;
- defect/waiver IDs;
- acceptance sign-offs.

These gaps must close progressively and must never be represented as completed.

## 18. Validator requirements

The future RTM validator should detect:

- duplicate identifiers;
- missing source documents;
- Must requirements without design or test links;
- accepted requirements without evidence;
- evidence without build/release identity;
- approval-required actions without approver/control links;
- denied actions implemented through ordinary paths;
- stale version links;
- rejected/deferred requirements still included in release acceptance;
- orphan tests or components.

## 19. Open decisions

1. Will the RTM gain a machine-readable YAML or CSV companion?
2. What identifier format will architecture components and controls use?
3. What identifier format will test cases and evidence packages use?
4. Which system owns implementation and release status?
5. How will GitHub issues and PRs be linked without becoming the sole source of truth?
6. Which trace links are mandatory before the first coding mission?
7. Which links can be generated automatically?
8. Who approves traceability exceptions?
9. How will requirement splitting and merging preserve history?
10. How will superseded requirements remain searchable?

## 20. Acceptance criteria

RTM-001 may advance to version `1.0.0` when:

1. all controlled requirement identifiers are indexed;
2. duplicate IDs are absent;
3. every Must product requirement maps to functional, non-functional, or autonomy requirements;
4. every FR/NFR/AUT item has a downstream owner;
5. architecture and security documents populate component/control links;
6. `TST-001` populates verification IDs;
7. release/evidence fields use a controlled status model;
8. known trace gaps remain visible;
9. validators detect missing mandatory links;
10. Product, Architecture, Security, Quality, and Operations approve the matrix model.

## 21. Revision and approval history

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Approval date: not applicable

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial matrix indexing product intent, personas, journeys, product requirements, functional requirements, NFRs, and autonomy actions | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `PER-001` — Personas and Jobs to Be Done
- `UCD-001` — User Journeys and Use Cases
- `PRD-001` — Product Requirements Document
- `SRS-001` — Functional Requirements Specification
- `NFR-001` — Non-Functional Requirements
- `AUT-001` — Autonomy and Approval Matrix
