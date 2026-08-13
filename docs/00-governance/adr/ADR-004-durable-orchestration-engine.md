---
document_id: ADR-004
title: Durable Orchestration Engine
version: 0.3.0
status: approved
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - operations-owner
  - quality-owner
created: 2026-08-12
last_reviewed: 2026-08-13
classification: internal
source_of_truth: true
related_documents:
  - DOC-000
  - ADR-001
  - ADR-003
  - SAD-001
  - ORC-001
  - RUN-001
  - EVT-001
  - DEP-001
related_adrs:
  - ADR-001
  - ADR-003
supersedes: []
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval after review while assuming the product-owner role
  - role: architecture-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval after review while assuming the architecture-owner role
  - role: security-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval after review while assuming the security-owner role
  - role: operations-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval after review while assuming the operations-owner role
  - role: quality-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval after review while assuming the quality-owner role
---

# ADR-004 — Durable Orchestration Engine

## Status

**Approved — 2026-08-13.** This ADR selects Temporal as the durable orchestration boundary. It does not claim that Temporal is deployed or that execution is implemented.

## Context

Agent OS requires durable workflows that may run for a long time, wait for approvals, use timers, retry bounded work, pause, resume, cancel, recover workers, and preserve ordered execution history. A transient task queue alone does not provide the required workflow authority.

## Decision

Agent OS will use **Temporal** as the durable workflow engine for long-running orchestration.

- Temporal owns workflow execution history, timers, signals, approval waits, retry scheduling, cancellation, worker task queues, and workflow recovery.
- PostgreSQL remains authoritative for Agent OS business state: identities, workspaces, permissions, conversations, projects, missions, tasks, artifacts, memory metadata, audit records, and cost records.
- Redis is auxiliary only: cache, notification fan-out, or bounded non-authoritative transport.
- External effects, model calls, tool calls, filesystem operations, and database writes execute as activities behind Agent OS policy and Tool Gateway controls.
- Temporal history is not a substitute for Agent OS audit evidence; consequential actions still emit platform audit events and receipts.
- Workflow definitions remain bounded, versioned, deterministic, and subject to Agent OS limits. Unbounded autonomous graph generation is excluded from the first implementation baseline.

## Consequences

### Positive

- Durable approval waits and recovery are first-class.
- Run history survives API and worker restarts.
- Retries, timers, cancellation, and signals have an explicit execution boundary.
- Agent adapters remain workers behind a stable control-plane contract.

### Trade-offs

- Local deployment gains an additional service and operational dependency.
- Workflow code must obey deterministic replay constraints.
- Temporal history and Agent OS audit records require retention and privacy coordination.

## Migration and conflict resolution

ADR-001 is harmonized with this decision for the durable orchestration boundary. Celery is not part of the authoritative workflow path. It may remain only for clearly bounded auxiliary jobs documented in a later decision and must not own run history, approvals, timers, recovery, or consequential dispatch.

## Acceptance criteria

- A local profile can start Temporal and a worker without exposing Temporal publicly.
- A workflow can survive worker restart and resume from durable history.
- Approval wait, retry, timeout, cancellation, and unknown-effect paths are testable.
- PostgreSQL and Temporal responsibilities are documented and do not compete as sources of truth.
- Backup, restore, upgrade, and retention procedures cover both systems.
- The implementation pins a compatible Temporal server and SDK version and records the compatibility evidence.
- Compose, local deployment, and operations documentation expose the same Temporal service and worker topology.

## References

- Temporal Workflows documentation: https://docs.temporal.io/workflows
