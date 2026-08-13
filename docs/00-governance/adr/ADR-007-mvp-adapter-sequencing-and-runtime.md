---
document_id: ADR-007
title: MVP Adapter Sequencing, Runtime Profile, and Transport Boundaries
version: 0.1.0
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - operations-owner
  - quality-owner
created: 2026-08-13
last_reviewed: 2026-08-13
classification: internal
source_of_truth: true
related_documents:
  - DOC-000
  - AGC-001
  - CAP-001
  - ADP-HER-001
  - ADP-CDX-001
  - ADP-CLA-001
  - ORC-001
  - RUN-001
  - DEP-001
  - SAN-001
related_adrs:
  - ADR-001
  - ADR-003
  - ADR-004
supersedes:
  - ADR-003#initial-agent-adapters-implementation-scope
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval of the MVP implementation recommendations on 2026-08-13
pending_approvals:
  - architecture-owner
  - security-owner
  - operations-owner
  - quality-owner
---

# ADR-007 — MVP Adapter Sequencing, Runtime Profile, and Transport Boundaries

## Status

**In review — product-owner direction approved on 2026-08-13.** Architecture, security, operations, and quality approvals remain required before this ADR is fully approved under `DOC-000`.

## Context

`ADR-003` established Hermes, Codex, and Claude Code as the initial adapter target set. Their detailed specifications exist, but requiring three real adapter implementations before proving the first durable execution slice would multiply runtime, authentication, transport, cancellation, filesystem, tool, and recovery variables at the same time.

The implementation therefore needs a narrower delivery sequence while preserving the three-adapter contract target.

## Decision

### 1. Contract target versus MVP implementation target

The **initial adapter contract target remains Hermes, Codex, and Claude Code**.

The **first MVP implementation gate does not require all three real adapters**. The required implementation sequence is:

```text
1. Adapter Simulator
2. Hermes
3. Codex
4. Claude Code
```

This ADR narrows the implementation sequencing portion of `ADR-003`; it does not retire the Codex or Claude Code adapter contracts.

### 2. Adapter Simulator is mandatory first

Before any real adapter is allowed to drive a durable Run, Agent OS must provide a deterministic adapter simulator implementing the versioned `AGC-001` contract.

It must support at minimum:

- registration and readiness;
- capability manifest;
- start;
- status/event reporting;
- completion;
- failure;
- timeout;
- cancellation request and confirmed cancellation as distinct states;
- delayed/late result;
- unknown terminal/effect state;
- restart/recovery test scenarios.

### 3. Hermes is the first real adapter

Hermes is the first real adapter targeted after the simulator because the first objective is to prove a general governed agent-runtime boundary before expanding to coding-specific runtimes.

The first Hermes capability profile is deliberately restricted:

```text
generate / converse
stream output where supported
report model/runtime observations
report usage/cost evidence where available
```

Protected filesystem, shell, browser, network, Git, secret, deployment, or external-effect capabilities remain disabled until they are routed through Agent OS policy, approval, Tool Gateway, and sandbox controls.

### 4. Hermes transport direction

The first Hermes adapter shall target a **local authenticated HTTP/JSON boundary with SSE streaming where the selected Hermes runtime exposes it**.

Requirements:

- bind locally or on a controlled internal interface only;
- authenticate the adapter/runtime channel;
- negotiate/version capabilities rather than infer them from branding;
- treat streaming as observations, not direct Run-state authority;
- preserve explicit cancellation acknowledgement versus confirmed stop;
- fail closed if the selected Hermes runtime does not expose the expected boundary.

The adapter contract, not Hermes-specific payloads, remains the Agent OS-facing API.

### 5. Codex follows Hermes

Codex is the second real adapter target.

A release may select an SDK, CLI wrapper, local client, or another validated Codex invocation mode. Agent OS does not assume a universal Codex protocol. The chosen mode must pass `ADP-CDX-001` conformance and preserve repository, worktree, command, Git-effect, secret, evidence, and approval boundaries.

### 6. Claude Code follows Codex

Claude Code is the third real adapter target.

The initial integration should prefer a controlled non-interactive execution mode with structured/streamed output when supported by the validated runtime. The exact invocation boundary remains feature-detected and versioned through `ADP-CLA-001`.

### 7. Reference host/runtime profile

The first supported execution host profile is:

```text
architecture: x86-64
OS family: Linux
reference distribution: Ubuntu 24.04 LTS
local developer alternative: WSL2 with the repository in the Linux filesystem
container runtime: Docker + Docker Compose for Agent OS services
Agent OS Python runtime: Python 3.12 baseline
```

Native Windows agent execution is outside the first supported runtime profile. Windows may host WSL2 and the browser/UI.

Alternative Linux distributions may be added after compatibility validation; Ubuntu is a reference profile, not a product lock-in.

### 8. One adapter does not grant authority

Adapter readiness never grants:

- workspace access;
- model-provider eligibility;
- tool permissions;
- filesystem/network permissions;
- secret access;
- approval authority;
- Git push/merge authority;
- deployment authority.

These remain independent Agent OS decisions.

## First real-adapter vertical slice

```text
Task snapshot
→ Run persisted
→ Temporal workflow
→ one Step / one Attempt
→ Hermes adapter
→ restricted generate/converse capability
→ model invocation through approved binding
→ streamed/final observations
→ accepted result/artifact
→ cost and usage evidence
→ receipt and audit
```

No protected external effect is required for the first Hermes completion gate.

## Consequences

### Positive

- Adapter-contract correctness is tested before vendor-specific complexity.
- The MVP can prove useful real execution with one runtime.
- Codex and Claude Code remain first-class planned targets without blocking the first slice.
- Runtime and transport differences stay explicit rather than being forced behind a false universal protocol.

### Trade-offs

- The first MVP release may not yet provide real Codex or Claude Code execution.
- Hermes functionality is intentionally narrower than the runtime may support natively.
- A Linux/WSL2-first profile excludes native Windows execution initially.

## Acceptance criteria

Before Hermes is marked supported:

1. simulator conformance and recovery tests pass;
2. the exact Hermes runtime/version is recorded;
3. transport authentication is enabled;
4. capability discovery/validation passes;
5. a durable Run survives worker or adapter restart without false completion;
6. cancellation semantics are tested;
7. an unknown state remains unknown and blocks blind retry where an effect may have occurred;
8. protected tools are unavailable unless mediated through Agent OS;
9. usage/model identity limitations are surfaced honestly;
10. audit evidence links Agent OS state to adapter/runtime observations.

## Compatibility note

`ADR-003` remains authoritative for the existence of Hermes, Codex, and Claude Code as the initial adapter target family. This ADR is authoritative for **delivery order and the minimum real-adapter requirement of the MVP** once approved.
