---
document_id: ADR-008
title: Pilot Deployment, Secret Handling, Backup, and Recovery Baseline
version: 0.1.0
status: in-review
owner: operations-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-08-13
last_reviewed: 2026-08-13
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - DEP-001
  - OPS-001
  - BCP-001
  - SEC-001
  - DAT-002
  - OBS-001
  - QAG-001
related_adrs:
  - ADR-001
  - ADR-002
  - ADR-004
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval of the MVP implementation recommendations on 2026-08-13
pending_approvals:
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
---

# ADR-008 — Pilot Deployment, Secret Handling, Backup, and Recovery Baseline

## Status

**In review — product-owner direction approved on 2026-08-13.** Architecture, security, data, operations, and quality approvals remain required before this ADR is fully approved under `DOC-000`.

This ADR defines the reference controlled-pilot deployment profile. It does not define a public SaaS architecture, contractual SLA, multi-region topology, or final commercial hosting platform.

## Context

`DEP-001` defines local, integration, pilot, and commercial deployment classes but intentionally leaves the concrete pilot host, pilot secret mechanism, and initial recovery objectives open. Development needs one reproducible reference so implementation, operations, security, and quality tests converge on the same environment.

## Decision

### 1. MVP deployment

The canonical MVP remains local-first and uses Docker Compose on Linux or WSL2. Public internet exposure is not required for MVP completion.

### 2. Controlled pilot topology

The first controlled pilot targets a **single dedicated Linux host or VM** running Docker Compose.

Reference host profile:

```text
OS: Ubuntu Server 24.04 LTS x86-64
access: private LAN and/or VPN by default
TLS: required when the pilot UI/API is exposed over a network
public database, storage, Temporal admin, or internal-service ports: prohibited
high availability: not required for the first pilot
```

A physical Linux server may replace a VM when it satisfies the same controls. The cloud/on-prem provider remains open.

### 3. Pilot service baseline

The pilot topology must account for at least:

- Mission Control web;
- control-plane API;
- Temporal server and required persistence;
- Agent OS Temporal worker(s);
- PostgreSQL business-state database;
- artifact content store;
- approved adapter(s);
- approved model-provider binding(s);
- approved telemetry;
- reverse-proxy/TLS boundary where required;
- backup utility and protected backup destination.

Redis remains auxiliary and is not authoritative workflow history.

### 4. Secret-handling baseline

Development may continue to use an ignored, permission-restricted local `.env` with `.env.example` containing placeholders only.

The first pilot standardizes on **SOPS + age** as the reference mechanism for encrypted secret configuration at rest. Secret values remain outside source-controlled plaintext, ordinary application data, prompts, artifacts, memory, logs, and audit payloads.

The pilot secret design must provide:

- environment and purpose scoping;
- restricted operator access;
- deployment-time resolution only where needed;
- rotation and revocation procedures;
- no UI disclosure of secret values;
- no raw secret values in diagnostic or audit output;
- a later migration path to a managed secret manager without changing application-level secret-reference contracts.

### 5. Backup scope

Pilot recovery must cover the continuity-relevant authoritative state, including:

- Agent OS PostgreSQL business state;
- Temporal persistence required to recover durable workflow history;
- artifact content and integrity metadata;
- audit/evidence data according to its authoritative storage design;
- versioned deployment/configuration manifests without plaintext secret values.

Derived caches and indexes may be rebuilt when their source data and rebuild procedures are verified.

### 6. Backup controls

Pilot backups must be encrypted, integrity-checked, manifested, access-controlled, monitored, and stored outside the same primary failure domain when practical.

A backup that has never passed a restore drill is not sufficient Pilot Ready evidence.

### 7. Initial recovery objectives

Initial engineering targets are:

```text
RPO target: <= 24 hours
RTO target: <= 4 hours
```

The RPO target assumes at least one successful backup cycle every 24 hours. The RTO target is an engineering objective to be measured during restore drills; it is not a contractual SLA and must not be presented as achieved without evidence.

### 8. Restore drill before pilot

Before G4 / Pilot Ready, recovery evidence must demonstrate:

- backup-manifest verification;
- restoration of Agent OS business state;
- supported Temporal recovery for durable workflow state;
- artifact integrity verification;
- schema/migration compatibility;
- reapplication of deletion, revocation, hold, and other negative lifecycle facts;
- authentication and workspace-isolation smoke tests;
- one synthetic safe Run;
- reconciliation of active, stale, or unknown Runs and approvals;
- audit/evidence availability;
- measured recovery duration and documented findings.

### 9. Deployment and recovery authority

The following authorities remain logically distinct:

```text
Release Owner        -> approves promotion/deployment
Operations Owner     -> executes deployment and ordinary rollback
Migration Operator   -> executes approved migrations
Restore Operator     -> executes approved restore operations
Security Owner       -> approves security-sensitive pilot operations
Data Owner           -> approves sensitive-data recovery/destructive lifecycle actions
Quality Owner        -> accepts release-gate evidence
```

A small team may combine roles, but each decision and action remains explicitly attributable and audited. AI agents may prepare plans and validation evidence but do not autonomously approve or execute pilot deployment, destructive migration, restore, security-sensitive configuration changes, or public exposure.

### 10. Availability posture

The MVP and first single-host pilot are **best effort**. They do not claim high availability or a contractual uptime percentage.

Single-host failure is an accepted and documented pilot limitation. Formal SLO/SLA values and HA architecture require later evidence and decisions.

## Consequences

### Positive

- Development, pilot, backup, and recovery converge on one reference environment.
- Secret handling improves without requiring a cloud-specific managed service.
- Temporal recovery becomes part of backup design rather than an omitted dependency.
- Recovery claims are tied to measured drills.
- The pilot remains deployable with limited infrastructure.

### Trade-offs

- Single-host availability is limited.
- SOPS + age introduces operational key-management responsibilities that require a security-reviewed runbook.
- Restore procedures must coordinate Agent OS business state and Temporal history.
- RTO/RPO targets may need revision after measurement.

## Acceptance criteria

- the pilot host inventory and exact software versions are recorded;
- no pilot secret is committed as plaintext;
- the selected secret mechanism passes security review;
- Temporal is present in the pilot topology;
- backup age/failure is monitored;
- a restore drill succeeds and records measured recovery time;
- emergency stop is tested;
- deployment, migration, restore, security, data, and quality authorities are named;
- no unsupported service is exposed publicly.
