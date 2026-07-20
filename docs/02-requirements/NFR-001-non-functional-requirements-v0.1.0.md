---
document_id: NFR-001
title: Agent OS Non-Functional Requirements
version: 0.1.0
status: draft
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - ux-accessibility-owner
  - quality-owner
  - operations-owner
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
  - AUT-001
  - RTM-001
  - SAD-001
  - SEC-001
  - THR-001
  - A11Y-001
  - TST-001
  - QAG-001
  - OPS-001
  - OBS-001
  - BCP-001
related_adrs: []
related_evidence:
  - VIDEO-002
  - VIDEO-003
  - VIDEO-004
---

# NFR-001 — Agent OS Non-Functional Requirements

> **Status: Draft.** The targets in this document are proposed initial baselines for the local Agent OS MVP and pilot. They are not implementation evidence, production SLAs, warranties, or commercial commitments. Final values require architecture, security, UX/accessibility, quality, operations, workload, cost, and pilot validation.

## 1. Document purpose

This document defines measurable quality attributes and operational constraints for Agent OS.

It complements `SRS-001` by specifying how well the required functions must perform and under which quality conditions.

It covers:

- performance and responsiveness;
- reliability, durability, and availability;
- recovery and continuity;
- security and privacy;
- accessibility and usability;
- observability;
- maintainability and quality;
- portability and interoperability;
- capacity and scalability;
- cost and resource efficiency;
- data integrity;
- localization;
- release and governance controls.

## 2. Scope

These requirements apply to the first MVP and local pilot:

- local single-node Linux/WSL deployment;
- responsive web Mission Control;
- one organization context;
- multiple isolated workspaces;
- one primary operator or a small trusted team;
- Hermes and Codex adapter targets;
- durable tasks, runs, approvals, artifacts, memory, audit, and cost records;
- no public internet exposure by default;
- no production financial posting;
- no high-availability SLA;
- no unrestricted autonomous host control.

## 3. Relationship to product and functional requirements

`PRD-001` defines product outcomes and priorities.

`SRS-001` defines required functional behavior.

`NFR-001` defines measurable quality constraints that apply across those behaviors.

Examples:

```text
SRS: the system shall persist a run before dispatch.
NFR: 100% of external dispatches must have a prior durable run record.

SRS: the system shall block approval-required actions.
NFR: 100% of approval-conformance tests must block execution without valid approval.

SRS: the system shall support responsive Mission Control.
NFR: defined Must journeys must pass viewport, keyboard, performance, and accessibility targets.
```

## 4. Requirement status and target confidence

Each target is one of:

| Label | Meaning |
|---|---|
| `Approved baseline` | Already present in the approved vision baseline, still requiring detailed measurement definition |
| `Proposed` | Initial engineering/product target requiring review |
| `To benchmark` | A baseline must be measured before a final threshold is approved |
| `Deferred` | Not required for the first MVP |

Unless otherwise stated, targets in this version are `Proposed`.

## 5. Priority model

- `Must` — required for MVP acceptance;
- `Should` — expected unless explicitly deferred through approved risk acceptance;
- `Could` — optional after Must and Should;
- `Won't-MVP` — intentionally excluded.

## 6. Reference pilot environment

Final hardware and software specifications belong in `DEP-001`, but performance and capacity testing require a controlled profile.

The reference environment must record:

- CPU model and allocated cores;
- RAM;
- storage type and available space;
- operating system/distribution;
- WSL version where applicable;
- container/runtime versions where applicable;
- browser version;
- database/storage versions;
- Agent OS build identity;
- representative dataset size;
- network assumptions;
- enabled adapters/providers.

A performance claim is invalid without the associated reference profile and workload.

## 7. NFR catalogue summary

| Category | Count |
|---|---:|
| Performance and responsiveness | 8 |
| Reliability, durability, availability | 12 |
| Backup, continuity, recovery | 5 |
| Security | 14 |
| Privacy and data governance | 5 |
| Accessibility and usability | 14 |
| Observability | 6 |
| Maintainability and quality | 9 |
| Portability, compatibility, interoperability | 6 |
| Capacity, scalability, resources | 6 |
| Cost and efficiency | 5 |
| Data integrity | 5 |
| Localization and terminology | 3 |
| Release, licensing, governance | 5 |
| **Total** | **103** |


## 8. Performance and responsiveness requirements

### `NFR-PERF-001` — Mission Control initial render responsiveness

- **Priority:** `Must`
- **Category:** Performance
- **Rationale:** The primary operational view must become usable quickly on the approved local pilot hardware.
- **Metric:** Time from authenticated navigation to meaningful interactive content, excluding deliberate provider calls.
- **Initial target:** p95 ≤ 2.5 seconds on the reference local pilot profile; p99 ≤ 5 seconds.
- **Verification:** Automated browser performance test plus manual validation on the reference environment.
- **Proposed owner:** architecture-owner / ux-accessibility-owner
- **Dependencies:** SAD-001, UXA-001, TST-001
- **Notes / exclusions:** Target applies to persisted local data already available to Agent OS; large artifact previews are excluded.

### `NFR-PERF-002` — Primary navigation response

- **Priority:** `Must`
- **Category:** Performance
- **Rationale:** Users must move between core sections without perceiving the application as blocked.
- **Metric:** Time from navigation action to visible destination shell and loading state.
- **Initial target:** p95 ≤ 500 ms for local route transition; destination data may continue loading with explicit state.
- **Verification:** Automated UI timing test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** UXA-001, API-001, TST-001

### `NFR-PERF-003` — Local API response for ordinary reads

- **Priority:** `Must`
- **Category:** Performance
- **Rationale:** Core reads should remain responsive on a local single-node deployment.
- **Metric:** Server processing time for ordinary authenticated reads excluding external provider latency.
- **Initial target:** p95 ≤ 500 ms; p99 ≤ 1.5 seconds at the approved pilot concurrency.
- **Verification:** API load test with representative seeded data.
- **Proposed owner:** architecture-owner
- **Dependencies:** SAD-001, API-001, DAT-001, TST-001

### `NFR-PERF-004` — Ordinary write acknowledgement

- **Priority:** `Must`
- **Category:** Performance
- **Rationale:** Users need prompt confirmation that tasks, approvals, or metadata changes were persisted.
- **Metric:** Time from accepted request to durable acknowledgement for ordinary metadata writes.
- **Initial target:** p95 ≤ 1 second; p99 ≤ 2.5 seconds.
- **Verification:** Integration tests with durable datastore acknowledgement.
- **Proposed owner:** architecture-owner
- **Dependencies:** DAT-001, API-001, TST-001

### `NFR-PERF-005` — Approval inbox freshness

- **Priority:** `Must`
- **Category:** Performance
- **Rationale:** A consequential action must not remain hidden from an eligible approver for long.
- **Metric:** Delay between durable approval-request creation and visibility in the approver inbox.
- **Initial target:** p95 ≤ 2 seconds in the local pilot.
- **Verification:** End-to-end test using correlated timestamps.
- **Proposed owner:** quality-owner
- **Dependencies:** APR-001, EVT-001, TST-001

### `NFR-PERF-006` — Run state propagation

- **Priority:** `Must`
- **Category:** Performance
- **Rationale:** Mission Control must reflect persisted run transitions without misleading lag.
- **Metric:** Delay between accepted run-state persistence and display to an active authorized client.
- **Initial target:** p95 ≤ 2 seconds for local client updates; stale status shown when the update channel is unhealthy.
- **Verification:** End-to-end timing and failure-injection tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** ORC-001, RUN-001, EVT-001, OBS-001

### `NFR-PERF-007` — Search responsiveness

- **Priority:** `Should`
- **Category:** Performance
- **Rationale:** Users need to retrieve authorized tasks, runs, artifacts, and memory efficiently.
- **Metric:** Search response time at the initial pilot dataset size.
- **Initial target:** p95 ≤ 1.5 seconds for metadata search; content/retrieval search target to be refined in MEM-001.
- **Verification:** Representative dataset benchmark.
- **Proposed owner:** architecture-owner
- **Dependencies:** DAT-001, MEM-001, TST-001

### `NFR-PERF-008` — External latency representation

- **Priority:** `Must`
- **Category:** Performance / UX
- **Rationale:** Provider and adapter latency must not make the UI appear frozen or completed.
- **Metric:** Percentage of external calls with visible pending state and elapsed-time indication.
- **Initial target:** 100% of external calls exceeding 1 second display explicit pending/running state.
- **Verification:** UI integration and usability tests.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** UCD-001, UXA-001, TST-001

## 9. Reliability, durability, and availability requirements

### `NFR-REL-001` — Persisted terminal run state reliability

- **Priority:** `Must`
- **Category:** Reliability
- **Rationale:** Accepted runs must retain terminal state and required evidence.
- **Metric:** Percentage of accepted MVP runs retaining terminal state and mandatory records after restart.
- **Initial target:** ≥99% over the approved pilot cohort; every observed loss is a release blocker until disposition.
- **Verification:** Integration tests, restart tests, and pilot telemetry.
- **Proposed owner:** quality-owner
- **Dependencies:** RUN-001, DAT-001, TST-001

### `NFR-REL-002` — Approval-policy enforcement reliability

- **Priority:** `Must`
- **Category:** Reliability / Safety
- **Rationale:** Actions classified as approval-required must never execute without valid approval.
- **Metric:** Pass rate of positive and negative approval conformance cases.
- **Initial target:** 100% of defined approval-required test actions blocked without valid exact approval.
- **Verification:** Policy conformance suite including expiry, invalidation, replay, and changed-parameter cases.
- **Proposed owner:** security-owner
- **Dependencies:** AUT-001, APR-001, SEC-001, TST-001

### `NFR-REL-003` — Resumable interruption success

- **Priority:** `Must`
- **Category:** Reliability / Recovery
- **Rationale:** Supported interruptions should resume without duplicated effects.
- **Metric:** Percentage of approved resumable scenarios completing without duplicate side effects.
- **Initial target:** ≥95%; the remaining ≤5% must fail safe with explicit state and no silent duplicate effect.
- **Verification:** Fault-injection and idempotency test suite.
- **Proposed owner:** architecture-owner
- **Dependencies:** ORC-001, RUN-001, TST-001

### `NFR-REL-004` — Cross-workspace isolation reliability

- **Priority:** `Must`
- **Category:** Reliability / Security
- **Rationale:** Workspace isolation is a central trust boundary.
- **Metric:** Pass rate of negative-access tests across every supported access path.
- **Initial target:** 100% pass rate.
- **Verification:** Automated authorization, retrieval, search, artifact, memory, tool, cost, and audit negative tests.
- **Proposed owner:** security-owner
- **Dependencies:** IAM-001, SEC-001, DAT-001, MEM-001, TST-001

### `NFR-REL-005` — Authorized artifact retrieval reliability

- **Priority:** `Must`
- **Category:** Reliability
- **Rationale:** Retained artifacts must remain available to authorized users.
- **Metric:** Successful retrieval rate for retained, non-deleted, integrity-valid pilot artifacts.
- **Initial target:** ≥99%, excluding deliberate deletion, policy denial, and declared storage outage.
- **Verification:** Storage/API integration tests and pilot telemetry.
- **Proposed owner:** architecture-owner
- **Dependencies:** ART-001, DAT-001, TST-001

### `NFR-REL-006` — Trace completeness

- **Priority:** `Must`
- **Category:** Reliability / Audit
- **Rationale:** Accepted runs need enough evidence for reconstruction.
- **Metric:** Percentage of accepted runs containing all mandatory event and receipt fields.
- **Initial target:** 100% for the defined minimum trace contract.
- **Verification:** Schema validation and end-to-end trace tests.
- **Proposed owner:** quality-owner
- **Dependencies:** AUD-001, RUN-001, EVT-001, TST-001

### `NFR-REL-007` — Adapter conformance

- **Priority:** `Must`
- **Category:** Reliability / Interoperability
- **Rationale:** Hermes and Codex must behave through common platform contracts.
- **Metric:** Required adapter conformance test pass rate.
- **Initial target:** 100% for the mandatory Hermes and Codex conformance subset.
- **Verification:** Automated contract suite.
- **Proposed owner:** architecture-owner
- **Dependencies:** AGC-001, CAP-001, ADP-HER-001, ADP-CDX-001

### `NFR-REL-008` — Idempotent duplicate protection

- **Priority:** `Must`
- **Category:** Reliability
- **Rationale:** Retries or client re-submissions must not duplicate protected side effects.
- **Metric:** Pass rate for duplicate-request and replay tests on designated idempotent operations.
- **Initial target:** 100% for operations classified as idempotent or one-time.
- **Verification:** Concurrency and replay tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** RUN-001, APR-001, API-001, TST-001

### `NFR-REL-009` — Clean restart data preservation

- **Priority:** `Must`
- **Category:** Reliability / Durability
- **Rationale:** The local service must tolerate controlled restart.
- **Metric:** Required record preservation across clean stop/start.
- **Initial target:** 100% preservation of committed organization, workspace, task, run, approval, artifact metadata, memory, audit, and cost records.
- **Verification:** Automated restart test.
- **Proposed owner:** operations-owner
- **Dependencies:** DAT-001, OPS-001, TST-001

### `NFR-REL-010` — Unexpected process interruption behavior

- **Priority:** `Must`
- **Category:** Reliability
- **Rationale:** A crash must not create false completion or silently lose known state.
- **Metric:** Percentage of approved crash scenarios ending in recoverable, failed, stale, or unknown state with preserved last durable evidence.
- **Initial target:** 100%.
- **Verification:** Crash/fault-injection suite.
- **Proposed owner:** architecture-owner
- **Dependencies:** ORC-001, RUN-001, OBS-001, TST-001

### `NFR-AVL-001` — Local pilot service availability

- **Priority:** `Should`
- **Category:** Availability
- **Rationale:** The local pilot should be sufficiently available for regular use without implying production SLA.
- **Metric:** Service availability during planned pilot operating windows, excluding approved maintenance and host shutdown.
- **Initial target:** Initial target ≥99% during measured pilot windows.
- **Verification:** Pilot telemetry and operations log.
- **Proposed owner:** operations-owner
- **Dependencies:** OPS-001, OBS-001, SLO-001
- **Notes / exclusions:** This is a pilot target, not a contractual production SLA.

### `NFR-AVL-002` — Graceful degraded mode

- **Priority:** `Must`
- **Category:** Availability / UX
- **Rationale:** Failure of one adapter or provider should not make unrelated platform records unreadable.
- **Metric:** Ability to access persisted workspaces, tasks, runs, artifacts, approvals, and audit when an external adapter/provider is unavailable.
- **Initial target:** 100% for defined external dependency outage scenarios.
- **Verification:** Dependency-outage tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** SAD-001, INT-001, TST-001

## 10. Backup, continuity, and recovery requirements

### `NFR-BCP-001` — Recovery Time Objective for local pilot

- **Priority:** `Must`
- **Category:** Business Continuity
- **Rationale:** The project needs a measurable restore objective.
- **Metric:** Time to restore the local pilot service and retained data from an approved backup scenario.
- **Initial target:** ≤4 hours, pending final approval in BCP-001.
- **Verification:** Documented recovery exercise.
- **Proposed owner:** operations-owner
- **Dependencies:** BCP-001, OPS-001, DAT-001, TST-001

### `NFR-BCP-002` — Recovery Point Objective

- **Priority:** `Must`
- **Category:** Business Continuity
- **Rationale:** Acceptable data loss must be explicit.
- **Metric:** Maximum age of recoverable committed data after the approved backup process.
- **Initial target:** Proposed RPO ≤24 hours for the first pilot; tighter targets require architecture and cost review.
- **Verification:** Backup schedule inspection and recovery exercise.
- **Proposed owner:** operations-owner
- **Dependencies:** BCP-001, DAT-001
- **Notes / exclusions:** Final value remains an open decision.

### `NFR-BCP-003` — Backup integrity verification

- **Priority:** `Must`
- **Category:** Business Continuity / Integrity
- **Rationale:** A backup is not useful unless integrity is checked.
- **Metric:** Percentage of complete backups with validated manifest and integrity checks.
- **Initial target:** 100%.
- **Verification:** Automated backup validation plus periodic restore test.
- **Proposed owner:** operations-owner
- **Dependencies:** BCP-001, ART-001, DAT-001

### `NFR-BCP-004` — Restore completeness reporting

- **Priority:** `Must`
- **Category:** Business Continuity
- **Rationale:** Partial recovery must not be presented as complete.
- **Metric:** Percentage of restore exercises producing an explicit component-by-component completeness report.
- **Initial target:** 100%.
- **Verification:** Recovery exercise evidence review.
- **Proposed owner:** quality-owner
- **Dependencies:** BCP-001, TST-001

### `NFR-BCP-005` — Recovery exercise frequency

- **Priority:** `Should`
- **Category:** Business Continuity
- **Rationale:** Untested procedures decay.
- **Metric:** Frequency of documented restore exercises during active pilot development.
- **Initial target:** At least once per major release candidate and at least quarterly while the pilot is actively used.
- **Verification:** Operations evidence review.
- **Proposed owner:** operations-owner
- **Dependencies:** BCP-001, REL-001

## 11. Security requirements

### `NFR-SEC-001` — Fail-closed authorization

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Authorization uncertainty must not grant access.
- **Metric:** Pass rate of dependency-failure and ambiguous-policy authorization tests.
- **Initial target:** 100% fail closed for protected actions and data.
- **Verification:** Security integration and fault-injection tests.
- **Proposed owner:** security-owner
- **Dependencies:** IAM-001, POL-001, SEC-001, TST-001

### `NFR-SEC-002` — Least-privilege default

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** New users, agents, adapters, tools, and integrations must not receive broad authority by default.
- **Metric:** Percentage of new protected identities/resources created with no authority beyond explicit baseline.
- **Initial target:** 100%.
- **Verification:** Configuration and policy tests.
- **Proposed owner:** security-owner
- **Dependencies:** IAM-001, POL-001, SEC-001

### `NFR-SEC-003` — Secret exclusion from ordinary content

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Credentials must not become prompts, memory, artifacts, logs, or audit content.
- **Metric:** Known secret leakage findings in tracked source, ordinary storage, logs, memory, artifacts, and audit during acceptance.
- **Initial target:** Zero unresolved confirmed leaks.
- **Verification:** Secret scanning, targeted tests, manual review, and redaction tests.
- **Proposed owner:** security-owner
- **Dependencies:** SEC-002, SEC-001, TST-001

### `NFR-SEC-004` — Encryption in transit

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Credentials and protected content require encrypted transport when crossing process or network trust boundaries.
- **Metric:** Percentage of approved non-localhost protected network interfaces using approved encrypted transport.
- **Initial target:** 100%.
- **Verification:** Configuration inspection and transport tests.
- **Proposed owner:** security-owner
- **Dependencies:** SAD-001, SEC-001, DEP-001
- **Notes / exclusions:** Pure in-process and explicitly approved local IPC may be handled separately by architecture.

### `NFR-SEC-005` — Encryption at rest for sensitive data

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Confidential, secret references, and sensitive metadata require protection on disk.
- **Metric:** Coverage of data classes requiring at-rest protection.
- **Initial target:** 100% of classes designated by DAT-002/SEC-001.
- **Verification:** Storage configuration and recovery tests.
- **Proposed owner:** security-owner
- **Dependencies:** DAT-002, SEC-001, DAT-001

### `NFR-SEC-006` — No unrestricted host access

- **Priority:** `Must`
- **Category:** Security / Sandboxing
- **Rationale:** Agent execution must not inherit full host authority.
- **Metric:** Pass rate of sandbox escape, path traversal, unauthorized process, and host-resource negative tests.
- **Initial target:** 100% for the defined threat-model test set.
- **Verification:** Security and sandbox conformance suite.
- **Proposed owner:** security-owner
- **Dependencies:** SAN-001, THR-001, TST-001

### `NFR-SEC-007` — Network egress restriction

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Unrestricted outbound access can enable exfiltration or production access.
- **Metric:** Pass rate of allowed/denied destination policy tests.
- **Initial target:** 100% for defined destinations and protocols.
- **Verification:** Network-policy integration tests.
- **Proposed owner:** security-owner
- **Dependencies:** SAN-001, SEC-001, INT-001

### `NFR-SEC-008` — Approval replay resistance

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Replayed approvals could duplicate high-impact actions.
- **Metric:** Pass rate for replay, double-consumption, changed-parameter, expired, and invalidated approval tests.
- **Initial target:** 100%.
- **Verification:** Policy and concurrency test suite.
- **Proposed owner:** security-owner
- **Dependencies:** APR-001, AUT-001, TST-001

### `NFR-SEC-009` — Audit integrity protection

- **Priority:** `Must`
- **Category:** Security / Audit
- **Rationale:** Audit evidence must resist unauthorized alteration.
- **Metric:** Detection or prevention rate for defined audit tampering scenarios.
- **Initial target:** 100% for the approved threat-model scenarios.
- **Verification:** Tamper tests and architecture review.
- **Proposed owner:** security-owner
- **Dependencies:** AUD-001, THR-001, SEC-001

### `NFR-SEC-010` — Security-event attribution

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Security investigation requires actor and scope attribution.
- **Metric:** Coverage of mandatory security-relevant event classes with identity, workspace, timestamp, result, and correlation.
- **Initial target:** 100%.
- **Verification:** Audit schema tests.
- **Proposed owner:** security-owner
- **Dependencies:** AUD-001, IAM-001, TST-001

### `NFR-SEC-011` — Dependency and supply-chain control

- **Priority:** `Must`
- **Category:** Security / Maintainability
- **Rationale:** Executable dependencies and plugins can introduce persistent risk.
- **Metric:** Percentage of shipped dependencies with version pinning/lock evidence, provenance where available, and vulnerability scanning.
- **Initial target:** 100% of production dependencies; zero unresolved critical vulnerabilities at release.
- **Verification:** Dependency inventory, SBOM, and vulnerability scan.
- **Proposed owner:** security-owner / engineering-owner
- **Dependencies:** DEV-001, QAG-001, SEC-001

### `NFR-SEC-012` — Secure preview behavior

- **Priority:** `Must`
- **Category:** Security
- **Rationale:** Artifact preview must not execute active content.
- **Metric:** Pass rate of malicious/active content preview tests.
- **Initial target:** 100%.
- **Verification:** Security test corpus.
- **Proposed owner:** security-owner
- **Dependencies:** ART-001, THR-001, TST-001

### `NFR-SEC-013` — Security patch response

- **Priority:** `Should`
- **Category:** Security / Operations
- **Rationale:** Known critical vulnerabilities require bounded remediation.
- **Metric:** Time from validated critical vulnerability notice to mitigation or accepted risk decision.
- **Initial target:** Proposed ≤72 hours for critical exploitable issues in supported pilot components.
- **Verification:** Incident and release records.
- **Proposed owner:** security-owner
- **Dependencies:** IRP-001, REL-001, OPS-001
- **Notes / exclusions:** Final severity model belongs in SEC/IRP documents.

### `NFR-SEC-014` — Default non-public exposure

- **Priority:** `Must`
- **Category:** Security / Deployment
- **Rationale:** The pilot is not approved for public internet exposure.
- **Metric:** Default reachable interfaces from outside the approved local environment.
- **Initial target:** Zero.
- **Verification:** Deployment/network inspection.
- **Proposed owner:** operations-owner
- **Dependencies:** DEP-001, SEC-001, OPS-001

## 12. Privacy and data-governance requirements

### `NFR-PRI-001` — Data minimization

- **Priority:** `Must`
- **Category:** Privacy
- **Rationale:** Agent OS should store only data necessary for the approved purpose.
- **Metric:** Percentage of persistent fields with documented purpose, classification, owner, and retention rule.
- **Initial target:** 100% before production-oriented use; ≥95% before pilot acceptance with no unknown sensitive field.
- **Verification:** Data inventory and privacy review.
- **Proposed owner:** data-owner
- **Dependencies:** DAT-001, DAT-002, PRI-001

### `NFR-PRI-002` — Purpose-bound telemetry

- **Priority:** `Must`
- **Category:** Privacy / Analytics
- **Rationale:** Product analytics must not become indiscriminate surveillance.
- **Metric:** Percentage of telemetry fields mapped to an approved metric and retention rule.
- **Initial target:** 100%.
- **Verification:** Telemetry schema review.
- **Proposed owner:** product-owner / data-owner
- **Dependencies:** OBS-001, PRI-001, DAT-002

### `NFR-PRI-003` — Deletion and correction propagation

- **Priority:** `Must`
- **Category:** Privacy / Data Lifecycle
- **Rationale:** Deleted or corrected memory/artifact metadata must stop appearing as active.
- **Metric:** Time for approved deletion/correction to propagate to active indexes and retrieval paths.
- **Initial target:** p95 ≤15 minutes in the local pilot; failures visible and retryable.
- **Verification:** Lifecycle integration tests.
- **Proposed owner:** data-owner
- **Dependencies:** DAT-001, MEM-001, ART-001

### `NFR-PRI-004` — Provider data handling transparency

- **Priority:** `Must`
- **Category:** Privacy / Explainability
- **Rationale:** Users need to know when content may be sent to an external provider.
- **Metric:** Coverage of provider-bound actions with visible provider/profile and applicable data-handling warning/summary.
- **Initial target:** 100%.
- **Verification:** UI and policy tests.
- **Proposed owner:** product-owner / security-owner
- **Dependencies:** MOD-001, SEC-001, UXA-001

### `NFR-PRI-005` — Sensitive-data exclusion baseline

- **Priority:** `Must`
- **Category:** Privacy / Scope
- **Rationale:** Regulated or highly sensitive data is outside the first MVP unless explicitly approved.
- **Metric:** Number of accepted MVP workflows requiring unapproved regulated/sensitive data.
- **Initial target:** Zero.
- **Verification:** Requirements and pilot-data review.
- **Proposed owner:** product-owner / security-owner
- **Dependencies:** SCP-001, DAT-002, PRI-001

## 13. Accessibility and usability requirements

### `NFR-A11Y-001` — WCAG 2.2 AA baseline

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Primary workflows must be accessible from the beginning.
- **Metric:** Conformance of defined MVP workflows against WCAG 2.2 AA.
- **Initial target:** No unresolved critical blocker; all applicable Level A and AA criteria pass or have approved documented exception.
- **Verification:** Automated checks plus manual keyboard and assistive-technology review.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** A11Y-001, DSN-001, TST-001

### `NFR-A11Y-002` — Keyboard-only completion

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Users must complete Must journeys without a pointing device.
- **Metric:** Percentage of Must journeys completable by keyboard without trap.
- **Initial target:** 100%.
- **Verification:** Manual keyboard test suite.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** UCD-001, A11Y-001, TST-001

### `NFR-A11Y-003` — Accessible names, roles, and states

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Assistive technology requires semantic controls.
- **Metric:** Coverage of interactive controls with programmatically determinable name, role, state, and value.
- **Initial target:** 100% for Must journeys.
- **Verification:** Automated accessibility scan plus screen-reader review.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** DSN-001, A11Y-001

### `NFR-A11Y-004` — Non-color state communication

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Operational state cannot rely only on color.
- **Metric:** Coverage of status indicators with text, icon, shape, or programmatic label in addition to color.
- **Initial target:** 100%.
- **Verification:** Visual and accessibility review.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** DSN-001, VVR-001

### `NFR-A11Y-005` — Responsive reflow

- **Priority:** `Must`
- **Category:** Accessibility / Responsive Design
- **Rationale:** The product must work across approved viewport sizes without global horizontal scrolling.
- **Metric:** Must-journey viewport pass rate at 320, 375, 768, 1024, and desktop reference widths.
- **Initial target:** 100%, except explicitly documented component-local overflow such as code/table viewers with accessible alternatives.
- **Verification:** Automated viewport screenshots and manual interaction review.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** UXA-001, DSN-001, VVR-001

### `NFR-A11Y-006` — Text scaling

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Users may need enlarged text.
- **Metric:** Must-journey usability at 200% browser zoom/text scaling.
- **Initial target:** 100% of Must journeys remain operable with no loss of content or function.
- **Verification:** Manual zoom test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** A11Y-001, VVR-001

### `NFR-A11Y-007` — Reduced motion support

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Motion can cause discomfort or impair comprehension.
- **Metric:** Coverage of nonessential animation respecting reduced-motion preference.
- **Initial target:** 100%.
- **Verification:** CSS/behavior inspection and manual test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** DSN-001, A11Y-001

### `NFR-A11Y-008` — Dynamic status announcement

- **Priority:** `Must`
- **Category:** Accessibility
- **Rationale:** Run, approval, error, and recovery state changes must be perceivable.
- **Metric:** Coverage of critical asynchronous status changes with appropriate programmatic announcement.
- **Initial target:** 100% for defined critical events.
- **Verification:** Screen-reader interaction tests.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** A11Y-001, UCD-001

### `NFR-USAB-001` — Defined journey completion

- **Priority:** `Must`
- **Category:** Usability
- **Rationale:** The MVP must enable representative users to complete priority jobs.
- **Metric:** Completion rate for defined Must journeys after approved onboarding.
- **Initial target:** Establish baseline, then target ≥80%.
- **Verification:** Moderated/instrumented usability test.
- **Proposed owner:** product-owner / ux-accessibility-owner
- **Dependencies:** PER-001, UCD-001, TST-001

### `NFR-USAB-002` — Run-state comprehension

- **Priority:** `Must`
- **Category:** Usability
- **Rationale:** Users must correctly interpret operational state.
- **Metric:** Percentage of representative users correctly identifying run state, evidence type, and required next action.
- **Initial target:** ≥90% for defined acceptance scenarios.
- **Verification:** Usability test with real/stale/unknown/partial cases.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** UCD-001, UXA-001, TST-001

### `NFR-USAB-003` — Approval comprehension

- **Priority:** `Must`
- **Category:** Usability / Safety
- **Rationale:** Approvers must understand the exact action and side effect.
- **Metric:** Percentage of test participants correctly identifying target, parameters, side effect, and expiry before decision.
- **Initial target:** ≥90%; critical misunderstanding rate 0 for high-risk scenarios.
- **Verification:** Moderated approval UX test.
- **Proposed owner:** ux-accessibility-owner / security-owner
- **Dependencies:** AUT-001, APR-001, TST-001

### `NFR-USAB-004` — Artifact provenance comprehension

- **Priority:** `Must`
- **Category:** Usability
- **Rationale:** Users must know where an artifact came from and whether it is current.
- **Metric:** Percentage of participants correctly identifying producing task/run, lifecycle, and supersession state.
- **Initial target:** ≥90%.
- **Verification:** Artifact review usability test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** ART-001, UCD-001

### `NFR-USAB-005` — Workspace isolation mental model

- **Priority:** `Must`
- **Category:** Usability / Security
- **Rationale:** Users should predict what is and is not shared across workspaces.
- **Metric:** Percentage of participants correctly predicting allowed and denied access in representative scenarios.
- **Initial target:** ≥90%.
- **Verification:** Usability and security scenario test.
- **Proposed owner:** product-owner / security-owner
- **Dependencies:** PER-001, IAM-001, TST-001

### `NFR-USAB-006` — Misleading state prevention

- **Priority:** `Must`
- **Category:** Usability / Integrity
- **Rationale:** Users must not mistake mock, stale, estimated, unavailable, or unknown data for current fact.
- **Metric:** Number of acceptance-test cases where participants interpret a non-current state as current fact.
- **Initial target:** Zero critical misinterpretations.
- **Verification:** Moderated state-semantics test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** UCD-001, DSN-001, TST-001

## 14. Observability requirements

### `NFR-OBS-001` — End-to-end correlation coverage

- **Priority:** `Must`
- **Category:** Observability
- **Rationale:** Operators and auditors need one trace across user action, task, run, step, approval, tool, artifact, and cost.
- **Metric:** Coverage of accepted vertical-slice events with stable correlation identifiers.
- **Initial target:** 100%.
- **Verification:** End-to-end trace validation.
- **Proposed owner:** operations-owner
- **Dependencies:** OBS-001, AUD-001, EVT-001

### `NFR-OBS-002` — Health freshness disclosure

- **Priority:** `Must`
- **Category:** Observability
- **Rationale:** A health value without age can be misleading.
- **Metric:** Coverage of health/status observations with source and last-checked timestamp.
- **Initial target:** 100%.
- **Verification:** UI/API schema tests.
- **Proposed owner:** operations-owner
- **Dependencies:** OBS-001, UXA-001

### `NFR-OBS-003` — Structured log coverage

- **Priority:** `Must`
- **Category:** Observability
- **Rationale:** Operational diagnostics require machine-searchable events.
- **Metric:** Coverage of mandatory service and workflow events emitted in the approved structured format.
- **Initial target:** 100% for events defined in OBS-001.
- **Verification:** Schema tests and log inspection.
- **Proposed owner:** operations-owner
- **Dependencies:** OBS-001, EVT-001

### `NFR-OBS-004` — Sensitive-log redaction

- **Priority:** `Must`
- **Category:** Observability / Security
- **Rationale:** Logs must not become a secret store.
- **Metric:** Confirmed raw secret findings in ordinary logs during acceptance.
- **Initial target:** Zero.
- **Verification:** Secret scanning and test fixtures.
- **Proposed owner:** security-owner / operations-owner
- **Dependencies:** SEC-001, OBS-001, TST-001

### `NFR-OBS-005` — Actionable alerting

- **Priority:** `Should`
- **Category:** Observability
- **Rationale:** The pilot should surface meaningful failures without alert fatigue.
- **Metric:** Percentage of defined critical conditions producing one deduplicated actionable notification within the target delay.
- **Initial target:** 100% for approval blockage, audit pipeline failure, storage integrity failure, backup failure, and critical security condition; delay ≤2 minutes locally.
- **Verification:** Alert integration tests.
- **Proposed owner:** operations-owner
- **Dependencies:** OBS-001, IRP-001

### `NFR-OBS-006` — Unknown-state propagation

- **Priority:** `Must`
- **Category:** Observability / Integrity
- **Rationale:** Collection failures must propagate to user-facing state.
- **Metric:** Coverage of defined evidence/telemetry failures producing stale, unavailable, or unknown state rather than false zero/success.
- **Initial target:** 100%.
- **Verification:** Fault-injection tests.
- **Proposed owner:** quality-owner
- **Dependencies:** OBS-001, UCD-001, TST-001

## 15. Maintainability and quality requirements

### `NFR-MNT-001` — Modular adapter replaceability

- **Priority:** `Must`
- **Category:** Maintainability
- **Rationale:** Agent/provider-specific behavior must remain replaceable.
- **Metric:** Percentage of core task/run/approval/artifact behavior exercised through common interfaces rather than direct Hermes/Codex branching.
- **Initial target:** 100% of the approved common adapter surface.
- **Verification:** Architecture review and contract tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** SAD-001, AGC-001, CAP-001

### `NFR-MNT-002` — Controlled dependency direction

- **Priority:** `Must`
- **Category:** Maintainability
- **Rationale:** The control plane must not depend directly on adapter/provider internals.
- **Metric:** Architecture-rule violations detected by static checks/review.
- **Initial target:** Zero unresolved violations.
- **Verification:** Architecture tests and dependency analysis.
- **Proposed owner:** architecture-owner
- **Dependencies:** SAD-001, DEV-001, QAG-001

### `NFR-MNT-003` — Automated test coverage of critical logic

- **Priority:** `Must`
- **Category:** Maintainability / Quality
- **Rationale:** Authorization, approval, state transitions, and idempotency require regression protection.
- **Metric:** Decision/branch coverage or mutation/conformance evidence for designated critical modules.
- **Initial target:** Targets defined in TST-001; proposed ≥90% branch coverage for critical policy/state modules, with no untested mandatory transition.
- **Verification:** Coverage reports plus mutation or contract tests where practical.
- **Proposed owner:** quality-owner
- **Dependencies:** TST-001, QAG-001

### `NFR-MNT-004` — Static analysis and type safety

- **Priority:** `Must`
- **Category:** Maintainability / Quality
- **Rationale:** Early defect detection reduces runtime ambiguity.
- **Metric:** Unresolved high-severity static-analysis/type errors in changed production code.
- **Initial target:** Zero at merge.
- **Verification:** CI static analysis and type checking.
- **Proposed owner:** engineering-owner
- **Dependencies:** DEV-001, QAG-001

### `NFR-MNT-005` — Documentation traceability

- **Priority:** `Must`
- **Category:** Maintainability / Governance
- **Rationale:** Implementation and decisions must remain connected to approved requirements.
- **Metric:** Accepted MVP requirements linked to architecture, backlog, tests, evidence, and release.
- **Initial target:** 100%.
- **Verification:** RTM and document-validator checks.
- **Proposed owner:** quality-owner
- **Dependencies:** RTM-001, DOC-000, QAG-001

### `NFR-MNT-006` — Schema and contract versioning

- **Priority:** `Must`
- **Category:** Maintainability / Compatibility
- **Rationale:** Adapters, events, artifacts, approvals, and APIs will evolve.
- **Metric:** Coverage of externally consumed schemas/contracts with explicit version and compatibility policy.
- **Initial target:** 100%.
- **Verification:** Contract inventory and compatibility tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** AGC-001, API-001, EVT-001, RUN-001, APR-001, ART-001

### `NFR-MNT-007` — Database migration safety

- **Priority:** `Must`
- **Category:** Maintainability / Data Integrity
- **Rationale:** Schema evolution must not silently lose state.
- **Metric:** Pass rate of upgrade and rollback/forward-recovery tests for supported migration paths.
- **Initial target:** 100% for supported paths; destructive migration requires explicit backup and approval.
- **Verification:** Migration integration tests.
- **Proposed owner:** architecture-owner / operations-owner
- **Dependencies:** DAT-001, DEV-001, OPS-001

### `NFR-MNT-008` — Reproducible local development setup

- **Priority:** `Must`
- **Category:** Maintainability / Delivery
- **Rationale:** Contributors and agents need a predictable environment.
- **Metric:** Successful setup rate using documented steps from a clean supported environment.
- **Initial target:** 100% in CI/reference verification; target ≤30 minutes for prepared developer after prerequisites.
- **Verification:** Clean-environment setup exercise.
- **Proposed owner:** engineering-owner
- **Dependencies:** DEV-001, OPS-001

### `NFR-MNT-009` — No unresolved critical quality gate

- **Priority:** `Must`
- **Category:** Quality
- **Rationale:** Critical defects must block release.
- **Metric:** Open critical defects, critical security findings, critical accessibility blockers, and failed Must requirement tests at release.
- **Initial target:** Zero.
- **Verification:** Quality gate review.
- **Proposed owner:** quality-owner
- **Dependencies:** QAG-001, TST-001

## 16. Portability, compatibility, and interoperability requirements

### `NFR-PORT-001` — Supported local Linux/WSL environment

- **Priority:** `Must`
- **Category:** Portability
- **Rationale:** The first pilot targets a controlled local environment.
- **Metric:** Successful install, startup, operation, backup, and restore on the reference Linux and WSL profiles.
- **Initial target:** 100% on the approved reference profiles.
- **Verification:** Environment matrix test.
- **Proposed owner:** operations-owner
- **Dependencies:** DEP-001, DEV-001, OPS-001

### `NFR-PORT-002` — Browser compatibility

- **Priority:** `Must`
- **Category:** Compatibility
- **Rationale:** The responsive web Mission Control needs a defined browser baseline.
- **Metric:** Must-journey pass rate on approved current stable browser versions.
- **Initial target:** 100% on the documented Chromium-based reference browser; secondary browser set to be finalized in A11Y/DEP documents.
- **Verification:** Cross-browser E2E test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** A11Y-001, DEP-001, TST-001

### `NFR-PORT-003` — Data export portability

- **Priority:** `Should`
- **Category:** Portability
- **Rationale:** Users should retain access to their core metadata and evidence outside one implementation.
- **Metric:** Coverage of core export formats with documented, versioned, non-proprietary representation.
- **Initial target:** Tasks, runs, approvals, artifact metadata, memory metadata, audit manifests, and cost events exportable in documented structured form.
- **Verification:** Export contract tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** DAT-001, API-001, ART-001

### `NFR-INT-001` — Adapter protocol isolation

- **Priority:** `Must`
- **Category:** Interoperability
- **Rationale:** Hermes/Codex-specific transport must not redefine core domain semantics.
- **Metric:** Percentage of adapter-specific fields isolated to adapter extension areas.
- **Initial target:** 100% for approved common contracts.
- **Verification:** Contract review and conformance tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** AGC-001, CAP-001, INT-001

### `NFR-INT-002` — Standards adoption decision discipline

- **Priority:** `Must`
- **Category:** Interoperability / Governance
- **Rationale:** MCP, AG-UI, A2A, OpenAPI, and AsyncAPI should not be adopted by assumption.
- **Metric:** Percentage of adopted external protocols with documented fitness/security decision and version.
- **Initial target:** 100%.
- **Verification:** ADR and standards-register review.
- **Proposed owner:** architecture-owner
- **Dependencies:** INT-001, SAD-001, ADRs

### `NFR-INT-003` — Backward compatibility for stored evidence

- **Priority:** `Must`
- **Category:** Compatibility
- **Rationale:** Historical runs and artifacts must remain readable after compatible upgrades.
- **Metric:** Successful read/interpretation rate for supported prior schema versions.
- **Initial target:** 100% for versions declared supported.
- **Verification:** Compatibility fixture tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** RUN-001, ART-001, AUD-001, DAT-001

## 17. Capacity, scalability, and resource requirements

### `NFR-CAP-001` — Initial workspace capacity

- **Priority:** `Should`
- **Category:** Capacity
- **Rationale:** The pilot needs a bounded reference dataset for performance and storage tests.
- **Metric:** Supported active workspaces in one organization on the reference environment.
- **Initial target:** At least 20 workspaces without breaching approved responsiveness targets.
- **Verification:** Load test with representative data.
- **Proposed owner:** architecture-owner
- **Dependencies:** DAT-001, SAD-001, TST-001

### `NFR-CAP-002` — Initial retained run capacity

- **Priority:** `Should`
- **Category:** Capacity
- **Rationale:** The local pilot must retain meaningful history.
- **Metric:** Retained runs on the reference environment while meeting read/search targets.
- **Initial target:** At least 10,000 runs with representative steps/events.
- **Verification:** Dataset benchmark.
- **Proposed owner:** architecture-owner
- **Dependencies:** DAT-001, OBS-001, TST-001

### `NFR-CAP-003` — Initial artifact metadata capacity

- **Priority:** `Should`
- **Category:** Capacity
- **Rationale:** Artifact discovery should remain usable as history grows.
- **Metric:** Retained artifact metadata records meeting retrieval/search targets.
- **Initial target:** At least 25,000 metadata records; binary storage capacity governed separately.
- **Verification:** Storage and search benchmark.
- **Proposed owner:** architecture-owner
- **Dependencies:** ART-001, DAT-001

### `NFR-CAP-004` — Pilot concurrency

- **Priority:** `Must`
- **Category:** Capacity
- **Rationale:** A small trusted team may operate simultaneously.
- **Metric:** Concurrent authenticated users and active runs supported on the reference environment.
- **Initial target:** At least 5 concurrent users and 4 active runs while meeting stated local API/UI targets.
- **Verification:** Load and concurrency test.
- **Proposed owner:** architecture-owner
- **Dependencies:** SAD-001, ORC-001, TST-001

### `NFR-CAP-005` — Resource-bounded execution

- **Priority:** `Must`
- **Category:** Capacity / Safety
- **Rationale:** Agent work must not exhaust the local machine.
- **Metric:** Coverage of active runs with configured CPU/memory/time/process/output limits.
- **Initial target:** 100% of agent/tool execution contexts.
- **Verification:** Sandbox/resource-limit tests.
- **Proposed owner:** security-owner / architecture-owner
- **Dependencies:** SAN-001, ORC-001, NFR-001

### `NFR-SCL-001` — Scale-out readiness without MVP implementation

- **Priority:** `Should`
- **Category:** Scalability
- **Rationale:** The MVP is single-node but core identifiers and contracts should not block later distributed execution.
- **Metric:** Architecture review of state ownership, idempotency, correlation, and worker identity.
- **Initial target:** No identified irreversible single-process assumption in approved core contracts.
- **Verification:** Architecture review.
- **Proposed owner:** architecture-owner
- **Dependencies:** SAD-001, ORC-001, DAT-001
- **Notes / exclusions:** This does not require distributed deployment in the MVP.

## 18. Cost and efficiency requirements

### `NFR-COST-001` — Cost attribution coverage

- **Priority:** `Must`
- **Category:** FinOps
- **Rationale:** Supported billable events must be tied to responsible work.
- **Metric:** Percentage of supported billable model/tool events attributed to workspace, task, and run.
- **Initial target:** ≥95%.
- **Verification:** Provider/tool reconciliation tests and pilot telemetry.
- **Proposed owner:** data-owner / operations-owner
- **Dependencies:** CST-001, OBS-001, TST-001

### `NFR-COST-002` — Cost-status transparency

- **Priority:** `Must`
- **Category:** FinOps / Integrity
- **Rationale:** Unknown and estimated values must not look authoritative.
- **Metric:** Coverage of displayed cost values with source class, currency, period, and freshness.
- **Initial target:** 100%.
- **Verification:** UI/API schema tests.
- **Proposed owner:** product-owner / data-owner
- **Dependencies:** CST-001, UXA-001

### `NFR-COST-003` — Budget enforcement latency

- **Priority:** `Must`
- **Category:** FinOps / Safety
- **Rationale:** Hard thresholds must affect execution promptly.
- **Metric:** Delay between threshold determination and enforceable pause/block/stop action.
- **Initial target:** ≤5 seconds for locally observable hard-limit events; provider-delayed usage remains explicitly pending.
- **Verification:** Runtime threshold tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** ORC-001, CST-001, TST-001

### `NFR-COST-004` — No hidden provider fallback cost

- **Priority:** `Must`
- **Category:** FinOps / Transparency
- **Rationale:** Fallback can change quality, privacy, and cost.
- **Metric:** Percentage of fallback/substitution events explicitly recorded and shown.
- **Initial target:** 100%.
- **Verification:** Routing/fallback integration tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** MOD-001, INT-001, TST-001

### `NFR-COST-005` — Reference operating-cost baseline

- **Priority:** `Should`
- **Category:** FinOps
- **Rationale:** The team needs a measurable baseline before optimizing infrastructure.
- **Metric:** Documented local infrastructure and provider spend for the approved pilot workload.
- **Initial target:** Baseline established before MVP acceptance; no arbitrary optimization target until measured.
- **Verification:** Pilot cost report.
- **Proposed owner:** product-owner / operations-owner
- **Dependencies:** FIN-001, OBS-001

## 19. Data-integrity requirements

### `NFR-DAT-001` — Referential integrity for core records

- **Priority:** `Must`
- **Category:** Data Integrity
- **Rationale:** Orphaned runs, approvals, artifacts, or costs would break evidence.
- **Metric:** Integrity violations among organization, workspace, task, run, step, approval, artifact, memory, audit, and cost records.
- **Initial target:** Zero unresolved violations.
- **Verification:** Database constraints and integrity tests.
- **Proposed owner:** architecture-owner / data-owner
- **Dependencies:** DDD-001, DAT-001, DCT-001

### `NFR-DAT-002` — Durable acknowledgement semantics

- **Priority:** `Must`
- **Category:** Data Integrity
- **Rationale:** The UI must not claim persistence before the durable store accepts the change.
- **Metric:** Percentage of success responses issued only after the defined durability boundary.
- **Initial target:** 100%.
- **Verification:** Persistence failure and crash tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** DAT-001, API-001, TST-001

### `NFR-DAT-003` — Time consistency and ordering

- **Priority:** `Must`
- **Category:** Data Integrity / Audit
- **Rationale:** Event reconstruction depends on reliable timestamps and causal order.
- **Metric:** Coverage of records with normalized timestamp, source clock context, and causal/correlation identifiers.
- **Initial target:** 100% for mandatory events.
- **Verification:** Schema and ordering tests.
- **Proposed owner:** architecture-owner
- **Dependencies:** EVT-001, AUD-001, OBS-001

### `NFR-DAT-004` — No silent data truncation

- **Priority:** `Must`
- **Category:** Data Integrity
- **Rationale:** Large prompts, outputs, logs, or artifacts must not be silently cut.
- **Metric:** Percentage of truncation events explicitly recorded with original/retained size and reason.
- **Initial target:** 100%.
- **Verification:** Boundary-size tests.
- **Proposed owner:** quality-owner
- **Dependencies:** ART-001, RUN-001, API-001

### `NFR-DAT-005` — Source-of-truth separation

- **Priority:** `Must`
- **Category:** Data Governance
- **Rationale:** Generated analysis must not overwrite authoritative source facts.
- **Metric:** Number of accepted workflows that overwrite authoritative external records or relabel generated analysis as authoritative without governed promotion.
- **Initial target:** Zero.
- **Verification:** Integration and data-lineage review.
- **Proposed owner:** data-owner
- **Dependencies:** SCP-001, DAT-001, MEM-001

## 20. Localization and terminology requirements

### `NFR-L10N-001` — Localization-ready user interface

- **Priority:** `Should`
- **Category:** Localization
- **Rationale:** The product may need French, English, or Malagasy support later.
- **Metric:** Percentage of user-facing strings externalized from business logic and available to the localization layer.
- **Initial target:** 100% of new production UI strings.
- **Verification:** Static inspection and UI test.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** DSN-001, DEV-001

### `NFR-L10N-002` — Explicit locale-sensitive formatting

- **Priority:** `Should`
- **Category:** Localization / Usability
- **Rationale:** Dates, times, numbers, and currency can be misinterpreted.
- **Metric:** Coverage of displayed locale-sensitive values with explicit locale/time-zone/currency rules.
- **Initial target:** 100%.
- **Verification:** Localization-format tests.
- **Proposed owner:** ux-accessibility-owner
- **Dependencies:** A11Y-001, CST-001

### `NFR-L10N-003` — Controlled terminology consistency

- **Priority:** `Must`
- **Category:** Usability / Governance
- **Rationale:** Inconsistent terms increase errors in a complex control system.
- **Metric:** Unresolved terminology deviations from `GLO-001` in controlled UI/document strings.
- **Initial target:** Zero at release for defined key terms.
- **Verification:** Terminology lint/review.
- **Proposed owner:** product-owner
- **Dependencies:** GLO-001, DSN-001, QAG-001

## 21. Release, licensing, and governance requirements

### `NFR-RELSE-001` — Release provenance

- **Priority:** `Must`
- **Category:** Release Management
- **Rationale:** Operators must know exactly what build is running.
- **Metric:** Coverage of release artifacts with version, commit, build time, dependency manifest/SBOM reference, and migration version.
- **Initial target:** 100%.
- **Verification:** Release pipeline validation.
- **Proposed owner:** engineering-owner
- **Dependencies:** REL-001, DEV-001, OPS-001

### `NFR-RELSE-002` — Rollback or forward-recovery plan

- **Priority:** `Must`
- **Category:** Release Management
- **Rationale:** Failed upgrades must have a controlled recovery path.
- **Metric:** Percentage of supported releases with tested rollback or forward-recovery procedure.
- **Initial target:** 100%.
- **Verification:** Release rehearsal.
- **Proposed owner:** operations-owner
- **Dependencies:** REL-001, BCP-001, DAT-001

### `NFR-COMP-001` — License and third-party notice control

- **Priority:** `Must`
- **Category:** Compliance
- **Rationale:** Commercial or internal reuse requires known third-party obligations.
- **Metric:** Coverage of shipped dependencies/assets with license classification and required notices.
- **Initial target:** 100%; zero unresolved prohibited-license finding.
- **Verification:** Dependency/license scan and review.
- **Proposed owner:** engineering-owner / product-owner
- **Dependencies:** DEV-001, QAG-001

### `NFR-COMP-002` — Evidence retention policy completeness

- **Priority:** `Must`
- **Category:** Compliance / Governance
- **Rationale:** Audit, approval, and artifact evidence need explicit retention rather than indefinite storage.
- **Metric:** Percentage of retained record classes with owner, retention, deletion, and exception rule.
- **Initial target:** 100% before production-oriented use; all MVP classes defined before pilot acceptance.
- **Verification:** Data-retention review.
- **Proposed owner:** data-owner / security-owner
- **Dependencies:** DAT-002, PRI-001, AUD-001

### `NFR-COMP-003` — Documented risk acceptance

- **Priority:** `Must`
- **Category:** Governance
- **Rationale:** Exceptions to Must security, accessibility, reliability, or privacy requirements cannot be implicit.
- **Metric:** Percentage of accepted exceptions with owner, rationale, duration, impact, compensating control, and review date.
- **Initial target:** 100%.
- **Verification:** Quality gate and risk register review.
- **Proposed owner:** product-owner / relevant owner
- **Dependencies:** QAG-001, SEC-001, DOC-000

## 22. Quality-attribute conflict rules

Quality attributes can conflict. The following precedence applies unless an approved ADR or risk decision states otherwise:

1. safety and authorization;
2. data confidentiality and workspace isolation;
3. integrity and durable evidence;
4. explicit human control;
5. recoverability;
6. accessibility;
7. correctness;
8. observability;
9. performance;
10. convenience and feature breadth.

Examples:

- a faster action must not bypass approval;
- a more available service must not fail open;
- a cheaper provider must not receive prohibited data;
- a richer dashboard must not use mock or stale data without explicit labeling;
- a retry must not proceed when duplicate side-effect risk is unknown.

## 23. Service-level indicators

The initial pilot should define at least these indicators:

| SLI | Description |
|---|---|
| Run persistence success | Accepted runs retaining required state |
| Approval enforcement | Approval-required actions blocked correctly |
| Run recovery success | Supported interruptions recovered safely |
| Workspace isolation | Negative-access tests and runtime denials |
| Artifact retrieval | Authorized retained-artifact availability |
| Trace completeness | Required event/receipt coverage |
| Cost attribution | Supported billable-event attribution |
| Adapter conformance | Hermes/Codex contract pass rate |
| Journey completion | Representative user success |
| Accessibility conformance | Critical blocker count and applicable criteria |
| Backup success | Complete verified backup rate |
| Restore success | Recovery time and restored-data completeness |
| Health freshness | Current versus stale health coverage |
| Security leakage | Confirmed secret/data leakage findings |

Production SLOs are deferred until workload and operating model are validated.

## 24. Performance test workload

Performance tests must use documented representative workloads, including:

- at least two workspaces;
- active and historical tasks;
- runs with multiple steps;
- approval requests;
- artifact metadata and permitted files;
- memory records;
- audit events;
- cost events;
- adapter/provider health states;
- stale, unknown, partial, failed, and completed cases.

Tests using only empty or trivial datasets cannot support acceptance claims.

## 25. Reliability test scenarios

Reliability and recovery tests must include:

- browser refresh during active run;
- worker restart;
- adapter process termination;
- provider timeout;
- provider authentication failure;
- event duplication;
- event reordering;
- storage temporary failure;
- approval expiry;
- approval replay;
- changed action after approval;
- tool timeout with unknown side effect;
- cancellation during waiting/running;
- backup interruption;
- partial restore;
- cross-workspace access attempt;
- artifact integrity mismatch.

## 26. Security and privacy verification baseline

Security verification must include:

- threat-model review;
- authentication and session tests;
- role and workspace authorization tests;
- prompt-based permission escalation attempts;
- filesystem path traversal and symlink escape tests;
- network egress denial tests;
- malicious MCP/tool scenarios;
- approval replay and substitution tests;
- secret scanning and redaction tests;
- artifact preview attack tests;
- audit tampering tests;
- dependency vulnerability and license review;
- backup confidentiality review;
- data-retention and deletion tests.

## 27. Accessibility verification baseline

Accessibility acceptance must include:

- automated accessibility scanning;
- keyboard-only completion;
- visible focus review;
- screen-reader review for critical journeys;
- zoom/text scaling at 200%;
- reduced-motion behavior;
- non-color status review;
- responsive reflow at approved viewports;
- dynamic state announcements;
- accessible errors and approval views;
- accessible tables, timelines, and code/diff alternatives.

Automated tools alone are insufficient.

## 28. Observability acceptance baseline

The system must provide enough evidence to answer:

- Who initiated the work?
- In which workspace and project?
- Which task and run?
- Which adapter, model, provider, and tool?
- Which policy decision?
- Which approval?
- Which steps occurred?
- Which artifacts were produced?
- Which side effects are known?
- What failed or is unknown?
- What usage and cost were attributed?
- What evidence is missing?
- What can be retried, resumed, or cancelled?

## 29. Capacity and scaling interpretation

The capacity targets in this draft:

- validate the local pilot;
- do not require multi-node infrastructure;
- do not constitute public SaaS capacity commitments;
- may be revised after benchmarking;
- must preserve safety, correctness, and responsiveness.

Scaling beyond the reference pilot requires:

- measured workload;
- approved architecture;
- updated threat model;
- operational cost analysis;
- revised SLOs;
- migration and recovery plan.

## 30. Exception policy

A Must NFR may be waived only through a documented exception containing:

- requirement ID;
- reason;
- affected users/data/workflows;
- severity and likelihood;
- compensating control;
- owner accepting the risk;
- expiration/review date;
- release limitation;
- user-visible disclosure where relevant.

Agents and implementers cannot self-approve exceptions.

## 31. Traceability expectations

Every Must NFR must link to:

- one or more product/functional requirements;
- architecture components;
- controls or contracts;
- test cases;
- evidence;
- release decision.

`RTM-001` will maintain the authoritative mapping.

## 32. Assumptions

This draft assumes:

- the MVP remains local, single-node, and non-public;
- the reference pilot environment can be defined and reproduced;
- Hermes and Codex are the first adapter targets;
- measurable usage data exists for some provider/tool calls;
- a suitable sandbox and secret mechanism can be selected;
- representative pilot tasks and datasets can be created;
- named quality, security, accessibility, and operations reviewers will be assigned;
- direct user testing is feasible before MVP acceptance.

## 33. Constraints

- no NFR target proves implementation;
- no target is a contractual production SLA;
- architecture technologies remain open;
- remote access and public multi-tenancy remain excluded by default;
- production financial posting remains excluded;
- accepted workflows cannot silently use mock data;
- security and approval override convenience/performance;
- the local environment still requires backup, authorization, and recovery;
- evidence must identify workload, environment, version, and exclusions.

## 34. Risks

| Risk | Consequence | Response |
|---|---|---|
| Targets too ambitious for local hardware | Delivery delay or misleading results | Benchmark early and revise through controlled review |
| Targets too weak | Unsafe or unusable MVP accepted | Preserve approved vision targets and negative tests |
| Aggregate metrics hide critical failure | Serious defect masked by averages | Add per-class gates and zero-tolerance security criteria |
| External-provider latency dominates | UI appears unresponsive | Separate local and external latency; show pending state |
| Small pilot sample overstates usability | False confidence | Record sample and confidence; continue research |
| Accessibility reduced to automation | Real barriers remain | Require manual keyboard and assistive-technology tests |
| Availability target mistaken for SLA | Commercial misunderstanding | Label pilot target explicitly |
| Cost data incomplete | False budget confidence | Show pending/unavailable/unattributed states |
| Recovery target untested | Backup creates false assurance | Require restore exercises |
| NFRs detached from implementation | Documentation drift | RTM and quality gates |

## 35. Open decisions

1. What exact hardware and WSL/Linux reference profiles will be supported?
2. Which browsers and versions form the acceptance matrix?
3. Is the proposed 24-hour RPO acceptable?
4. Which record classes require tighter backup frequency?
5. Which local service availability target is appropriate?
6. Which performance targets need separate values for Windows/WSL and native Linux?
7. What exact stale thresholds apply to runs, adapters, providers, cost data, and health?
8. What artifact size and total storage limits apply?
9. What audit, memory, artifact, and telemetry retention periods apply?
10. Which encryption mechanisms and key-management approach are approved?
11. Which sandbox escape and network attack scenarios define acceptance?
12. Which assistive technologies and languages will be tested?
13. What minimum user-research sample supports journey acceptance?
14. Which critical modules require mutation testing or higher coverage?
15. Which production-oriented NFRs remain deferred after MVP?
16. What provider/tool spend ceiling applies to pilot testing?
17. Which exceptions, if any, are acceptable before first pilot use?

## 36. NFR acceptance criteria

NFR-001 may advance to version `1.0.0` when:

1. Product Owner accepts the proposed user, pilot, and cost implications;
2. Architecture confirms targets are measurable on a defined reference environment;
3. Security approves the security/privacy baseline and zero-tolerance conditions;
4. UX/accessibility approves the accessibility and usability verification plan;
5. Quality confirms every Must NFR has a verification method;
6. Operations accepts backup, restore, health, availability, and recovery targets;
7. all targets are labeled approved, proposed, benchmark-required, or deferred;
8. conflicts with `VSN-001`, `SCP-001`, `PRD-001`, and `SRS-001` are resolved;
9. open decisions have owners and downstream documents;
10. RTM can trace every Must NFR;
11. metadata, terminology, links, Markdown, and validation checks pass.

## 37. Downstream document impact

| NFR category | Primary downstream documents |
|---|---|
| Performance/capacity | `SAD-001`, `DAT-001`, `ORC-001`, `TST-001` |
| Reliability/recovery | `ORC-001`, `RUN-001`, `BCP-001`, `TST-001` |
| Security/privacy | `SEC-001`, `THR-001`, `IAM-001`, `SAN-001`, `PRI-001` |
| Accessibility/usability | `UXA-001`, `DSN-001`, `A11Y-001`, `VVR-001` |
| Observability | `OBS-001`, `AUD-001`, `EVT-001` |
| Maintainability | `SAD-001`, `DEV-001`, `QAG-001` |
| Portability/deployment | `DEP-001`, `OPS-001`, `DEV-001` |
| Cost | `CST-001`, `FIN-001`, `OBS-001` |
| Data integrity | `DDD-001`, `DAT-001`, `DCT-001` |
| Release/compliance | `REL-001`, `QAG-001`, `DOC-000` |

## 38. Revision and approval history

### Approval state

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Approval date: not applicable
- Required next action: Product, Architecture, Security, UX/accessibility, Quality, and Operations review

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial measurable quality baseline with 103 requirements across performance, reliability, security, privacy, accessibility, observability, maintainability, portability, capacity, cost, data integrity, localization, and release governance | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `PER-001` — Personas and Jobs to Be Done
- `UCD-001` — User Journeys and Use Cases
- `PRD-001` — Product Requirements Document
- `SRS-001` — Functional Requirements Specification
