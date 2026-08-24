---
document_id: ADR-006
title: MVP Model Provider and Cost-Control Baseline
version: 0.2.0
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-08-13
last_reviewed: 2026-08-18
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - MOD-001
  - CST-001
  - DAT-002
  - SEC-001
  - INT-001
  - RUN-001
related_adrs:
  - ADR-001
  - ADR-003
supersedes: []
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user approval of the MVP implementation recommendations on 2026-08-13
  - role: product-owner
    status: approved
    approval_date: 2026-08-18
    evidence: explicit Product Owner approval of the compatible multi-backend and normalized economics extension
pending_approvals:
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
---

# ADR-006 — MVP Model Provider and Cost-Control Baseline

## Status

**In review — product-owner direction approved on 2026-08-13.** Architecture, security, data, operations, and quality approvals remain required before this decision is treated as fully approved under `DOC-000`.

This ADR selects an implementation sequence. It does not approve a specific production model, current provider price, contractual term, restricted-data use, or legal/privacy claim.

## Context

`MOD-001` intentionally defines a provider-neutral model contract and does not select the first concrete provider. Development now requires a narrow, testable provider baseline so that the first durable vertical slice can be implemented without simultaneously introducing several external-provider behaviors.

The MVP also needs deterministic CI execution that never depends on paid external inference, explicit cost attribution, and no silent fallback between providers.

## Decision

### 1. Provider-neutral contract remains authoritative

Agent OS continues to request logical model profiles through `MOD-001`. Application and workflow code must not hard-code provider-specific behavior outside provider bindings, gateways, or adapters.

### 2. Mandatory simulator

A deterministic model/provider simulator is mandatory for CI, contract tests, fault injection, cost-path tests, recovery tests, and development without external credentials.

The simulator must be able to produce at least:

- successful text output;
- deterministic usage metadata;
- timeout;
- rate-limit style failure;
- malformed/invalid structured output;
- provider unavailable;
- delayed response;
- cancellation observation;
- unknown or incomplete usage evidence.

Simulator output must always be visibly identified as synthetic and must not be presented as real provider execution.

### 3. First external provider binding

The first real external provider binding targeted by the MVP is **OpenAI**.

Only explicitly configured and policy-approved OpenAI model bindings are eligible. A configured account or API key does not make every model eligible automatically.

### 4. Local-model direction

A local model runtime is permitted as an optional development or controlled-pilot binding when it passes the same `MOD-001` capability, identity, usage, data-handling, and readiness checks.

Local inference is not required to complete the first external-provider vertical slice and must not create a parallel ungoverned model path.

### 5. Deferred providers

Anthropic is the next planned external provider after the first OpenAI vertical slice is proven. Additional direct providers and provider aggregators are deferred until an explicit binding and policy decision exists.

No provider is enabled merely because an SDK dependency exists in the repository.

### 5.1 Post-D2 coexistence extension

The first real provider proof remains the OpenAI Responses API path defined by
D2 and `ADR-009`. A Codex subscription-backed runtime does not replace D2,
change Issue #10 scope, or become an approved provider through this ADR.

After D2, direct API providers, subscription-backed agent runtimes, and the
deterministic simulator coexist under the explicit backend taxonomy and
router proposed in `ADR-010`. OpenAI API billing/authentication and
ChatGPT/Codex subscription billing/authentication are distinct domains.

Actual monetary cost remains distinct from normalized equivalent cost. A
subscription-backed run may have `actual_cost_state=subscription_included`
and `actual_cost_usd=null`; it is not represented as zero. Equivalent cost is
a versioned simulated reference value and is not provider billing truth.

### 6. No silent fallback

Fallback remains explicit, bounded, auditable, and policy-controlled as required by `MOD-001`.

A provider, model, region, endpoint, data-disclosure scope, quality class, or material cost change must never occur silently.

### 7. Secret boundary

Provider credentials are never persisted as ordinary Agent OS business data, prompts, conversations, artifacts, memory, logs, or audit payloads.

Development credentials may be supplied through ignored local environment configuration. Pilot handling is governed by `ADR-008`.

### 8. Usage and cost evidence

Every real model attempt must preserve, when available:

- organization and workspace;
- project, task, run, step, and attempt identifiers;
- logical model profile and version;
- configured provider/model;
- selected binding;
- provider-reported or otherwise observed actual model identity;
- provider request identifier;
- input, output, cached, and other provider-reported usage units;
- usage-source authority and completeness;
- pricing-profile version;
- currency;
- estimate, reservation, measured/calculated actual, provider-reported cost, and later invoice/reconciliation state as distinct facts.

Unknown usage or cost remains `unknown`; it is never converted to zero.

### 9. Cost ceiling

No universal monetary amount is hard-coded into the architecture.

The MVP must support configurable workspace/run budget policy and explicit upper bounds before paid execution. The pilot monetary values require a separate operational approval based on observed usage and current provider pricing.

## First provider vertical slice

The minimum real-provider path is:

```text
Task snapshot
→ durable Run
→ one Step
→ one Attempt
→ Model Gateway
→ approved OpenAI ProviderBinding
→ response observation
→ Artifact/Result
→ usage and cost evidence
→ receipt and audit
```

No external tool effect is required in this slice.

## Consequences

### Positive

- The first implementation has one real external-provider variable rather than several.
- CI remains deterministic and credential-free through the simulator.
- Provider neutrality is preserved at the contract boundary.
- Cost and token evidence are designed before paid usage scales.
- A local model can be introduced without creating a second architecture.

### Trade-offs

- Anthropic and other providers are not MVP blockers.
- Real multi-provider routing is deferred until the first provider path is proven.
- Cost policy must tolerate provider metadata that can be partial or delayed.

## Implementation requirements

Before a real OpenAI binding is marked ready:

1. provider credentials are referenced through the approved secret boundary;
2. data classification and outbound-disclosure policy are evaluated;
3. model capability and context/output limits are validated;
4. rate-limit and timeout handling are tested;
5. usage evidence is captured without logging prompt/output content by default;
6. estimate and actual cost remain distinct;
7. fallback is disabled unless explicitly configured;
8. simulator tests pass independently of external availability;
9. actual model identity is never fabricated from configured identity;
10. audit and receipt evidence link to the exact run attempt.

## Validation criteria

- CI can complete model-path tests with no external key.
- One approved external binding can complete the first vertical slice.
- Unknown usage/cost is represented honestly.
- A provider failure does not trigger silent fallback.
- Workspace budget policy can block dispatch before paid execution.
- Provider/model identity shown in Mission Control distinguishes configured, selected, reported/observed, and unknown states.

## Migration and compatibility

Existing OpenAI and Anthropic SDK dependencies are implementation details and do not constitute approved provider enablement. Implementation work may remove unused SDKs or move them behind optional provider packages in a later bounded change.

## References

- `MOD-001` — Model Profile Contract
- `CST-001` — Usage, Cost and Budget Architecture
- `DAT-002` — Data Classification, Retention and Deletion Standard
- `SEC-001` — Security Architecture
