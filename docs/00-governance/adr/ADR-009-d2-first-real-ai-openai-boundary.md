---
document_id: ADR-009
title: D2 First Real AI Provider Boundary and Evidence
version: 0.1.0
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
created: 2026-08-16
last_reviewed: 2026-08-16
classification: internal
source_of_truth: false
related_documents: [ADR-006, MOD-001, CTX-001, CST-001, EVAL-001]
related_adrs: [ADR-003, ADR-004, ADR-006, ADR-007]
---

# ADR-009 — D2 First Real AI Provider Boundary and Evidence

Status: Proposed

## Context

Issue #10 adds the first real model invocation while preserving the D0/D1
deterministic execution path. The provider must remain replaceable, and an
operator must be able to distinguish configured identity, actual identity,
context evidence, usage, and cost uncertainty.

## Decision drivers

- Keep provider SDK types and transport details outside the control-plane port.
- Make the simulator the deterministic CI and local default.
- Prevent implicit fallback from a requested OpenAI execution to the simulator.
- Persist context, provenance, usage, and cost evidence without secrets or raw
  prompts in the manifest.
- Disable external tools for this first slice.

## Decision

Agent OS exposes provider-neutral invocation dataclasses. The first real
adapter is an OpenAI Responses API adapter, isolated to one module. It sends a
structured-output schema, `tools=[]`, server-side credentials, and a stable
client request identifier. OpenAI execution requires both a configured API key
and explicit `OPENAI_EXECUTION_ENABLED=true`; a denied or unavailable provider
is a terminal provider error and never silently falls back.

Each attempt receives a versioned Context Manifest containing segment metadata,
authority/trust classification, hashes, transformations, disclosure state, and
bounded token budget. ModelInvocation and UsageRecord persist identity,
request/response identifiers, latency, token-source completeness, pricing
version, and cost state. Unknown cost is represented as unknown, never zero.

## Consequences

### Positive

- Simulator-based qualification remains credential-free and deterministic.
- OpenAI is replaceable without leaking SDK contracts into domain code.
- Reviewers can inspect provenance and cost evidence through the API and UI.

### Negative

- A live OpenAI smoke test requires explicit environment configuration and
  approved credentials.
- Provider-reported usage does not establish a cost without a pricing profile.

### Neutral or operational

- Hermes, Codex, Claude, external tools, and D3 IAM are outside this slice.
- Provider profile administration remains configuration-backed rather than a
  user-editable registry.

## Risks and mitigations

- Provider response semantics may change: pin SDK/runtime versions and use
  structured-output validation plus deterministic evals.
- Untrusted task text may contain prompt instructions: classify it as
  `untrusted_data`, keep system policy separate, and expose no tools.
- A worker may stop after a provider response: use the durable run/attempt
  terminal check and stable request identifier before creating terminal
  evidence.

## D2 reconciliation semantics

The attempt, Context Manifest, prepared ModelInvocation, and pending
UsageRecord are committed before an external request is started. The
invocation then records `request_sent` and the attempt records uncertain side
effect certainty in a separate commit. If the worker stops before response
evidence is committed, reconciliation marks that attempt and invocation
`unknown` and preserves usage/cost as unknown; a later retry may issue a new
provider request with the same run correlation identifier. A terminal commit
is idempotent and redelivery returns the existing artifact/receipt. This is
at-least-once external invocation with explicit uncertainty, not an exactly
once guarantee.

## Validation plan

Run the D2 provider contract tests, simulator-backed golden suite, D1
regression suite, migration round-trip on PostgreSQL, documentation and
frontend gates. A live provider smoke test is an explicit credential-gated
follow-up.

The compatibility spike is pinned to `openai==1.109.1` and exercises
`AsyncOpenAI.responses.create` with `input`, `text.format` JSON Schema,
`max_output_tokens`, `tools=[]`, `store=False`, and the client request header.
The provider contract tests capture this request shape without importing SDK
types outside the adapter module.

## Migration or compatibility impact

Migration 0006 adds D2 execution mode/profile defaults, provenance fields, and
context/invocation/usage/evaluation evidence tables. Existing D1 rows default
to simulator mode and remain readable.

## Related requirements

- Issue #10 — D2 First Real AI
- ADR-006 — MVP Model Provider and Cost-Control Baseline
- MOD-001, CTX-001, CST-001, EVAL-001

## Supersedes / Superseded by

None.
