---
document_id: ADR-010
title: Multi-Execution Backends and Normalized AI Economics
version: 0.1.0
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-08-18
last_reviewed: 2026-08-18
classification: internal
source_of_truth: false
related_documents:
  - GLO-001
  - ADR-006
  - MOD-001
  - CST-001
  - INT-001
  - ADP-CDX-001
  - OBS-001
  - DOC-000
related_adrs:
  - ADR-003
  - ADR-004
  - ADR-006
  - ADR-009
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-18
    evidence: explicit Product Owner direction for multi-execution backends and normalized AI economics
pending_approvals:
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
---

# ADR-010 — Multi-Execution Backends and Normalized AI Economics

## Status

**In review — Product Owner direction approved on 2026-08-18.** Architecture,
security, data, operations, and quality approvals remain pending. This ADR is
an architectural proposal and does not mark D3 as started or any future
adapter as implemented.

## Context

Agent OS must support several execution routes at the same time without
collapsing their identity, authority, authentication, billing, or evidence
semantics. A direct model-provider request, an agent-runtime session, and a
deterministic simulator are different execution backend classes.

The Product Owner direction is:

- model-provider connections include the OpenAI Responses API and future
  direct or local providers;
- agent-runtime connections include Codex authenticated through a
  ChatGPT/Codex subscription session, Hermes, and future governed runtimes;
- the deterministic simulator remains a first-class backend for CI and safe
  qualification;
- OpenAI API billing and ChatGPT/Codex subscription usage are separate
  authentication and billing domains;
- no silent fallback is permitted; a paid API fallback from a subscription
  runtime requires explicit policy and authorization.

The existing D2 proof remains deliberately narrower. `ADR-009` in the D2
worktree is reserved for the OpenAI Responses API boundary and is not changed
by this documentation update.

## Decision

Agent OS introduces the architectural concept:

```text
ExecutionBackend
├── ModelProviderConnection
└── AgentRuntimeConnection
```

The Execution Router selects one explicit backend under policy for each
attempt. Concurrent use is allowed:

```text
Task A → OpenAI API
Task B → Codex subscription runtime
Task C → deterministic simulator
```

The selected backend, actual backend/runtime, configured and actual model
identity, authentication source, billing source, usage source, fallback
decision, actual monetary cost, and normalized equivalent cost are separate
facts in routing and execution evidence. Missing facts remain unknown.

### Backend taxonomy

| Backend class | Meaning | Initial direction |
|---|---|---|
| `model_provider_connection` | Direct model inference through a provider or local model endpoint | OpenAI Responses API in D2; future direct/local providers |
| `agent_runtime_connection` | Governed invocation of a runtime that may itself manage model access, sessions, tools, and work | Codex subscription bridge and Hermes after D2 |
| `deterministic_simulator` | Local synthetic execution with deterministic fixtures and explicitly synthetic identity | Required for CI and fault qualification |

An Agent Runtime Connection is not represented as a Model Provider Connection
merely because the runtime may use a model provider internally. A runtime's
model observation and its provider observation may each be unavailable or
reported by different authorities.

### Explicit routing and fallback

The Execution Router evaluates the requested backend, policy, capability,
workspace, data classification, auth source, budget, and readiness. It
records `requested_backend`, `selected_backend`, `actual_backend`, and the
fallback decision before or at invocation.

Fallback is `not_allowed` unless an explicit policy permits the exact
alternative. A subscription-backed runtime may not silently fall back to a
paid API call. A model-provider failure may not silently become simulator
success. Any approved fallback records the reason, authorization, changed
provider/runtime, data disclosure, model identity, usage source, and cost
impact.

### Security boundary for subscription runtimes

The preferred Codex subscription design is a governed host/runtime bridge.
Agent OS persists only authentication source/type, runtime identity, a safe
session/runtime reference, and capability/evidence metadata. Reusable human
ChatGPT/Codex credentials are not copied into backend or worker containers,
and broad human credential directories are not mounted into containers.

### Normalized economics

Every backend should expose two independent economic views where evidence
permits:

1. **Actual Monetary Cost** — provider billed/calculated, subscription
   included, allocated, invoiced, or unknown according to its source.
2. **Normalized Equivalent Cost** — a simulated USD equivalent under an
   immutable, versioned reference pricing model.

They are never the same semantic fact. A subscription-backed run uses:

```text
actual_cost_state = subscription_included
actual_cost_usd = null
```

It must not be represented as `$0` actual cost merely because no incremental
API invoice exists. Normalized equivalent cost is not provider billing,
accounting truth, realized savings, or a customer charge.

Required equivalent-cost evidence includes:

```text
equivalent_cost_usd
equivalent_cost_state
pricing_catalog_id
pricing_snapshot_id
pricing_basis
pricing_version
effective_at
token_usage_source
calculation_method
confidence
assumptions
```

The pricing basis distinguishes at least `exact_model_api_price`,
`proxy_model_api_price`, `configured_reference_rate`, and `unavailable`.
The system never silently maps a runtime model to another pricing SKU.
Incomplete token breakdowns remain partial; input/output/cached splits are
not invented.

### Pricing catalogue and immutable snapshot

The Pricing Catalog is versioned and records provider, model/SKU, effective
period, currency, input/cached/output rates, tool or unit rates, conditional
rules, source/reference, freshness, confidence, and supersession. Each
execution binds to an immutable Pricing Snapshot. Historical equivalent
costs therefore do not change when the current provider price changes.

Calculation states include `calculated`, `estimated`, `estimated_range`,
`partial`, and `unknown`.

### Independent budgets

Budget policy has two independent dimensions:

- actual monetary budget, such as `actual_api_budget_usd = 20/day`;
- normalized equivalent-consumption budget, such as
  `equivalent_ai_consumption_budget_usd = 100/day`.

Subscription usage can be bounded by normalized consumption even when its
incremental actual monetary cost is subscription-included.

Subscription fees are tracked separately from per-run equivalent value.
Dashboards may compare subscription fee with normalized equivalent
consumption, but any derived savings or value is labelled simulated
economics and is never claimed as realized financial savings.

## Codex compatibility evidence (non-normative)

The Product Owner supplied the following local compatibility evidence dated
2026-08-18:

```text
Codex CLI: 0.147.0
command: codex exec
reported model: gpt-5.6-luna
reported provider: openai
OPENAI_API_KEY: absent
authentication path: ChatGPT/Codex subscription session
result: CODEX_RUNTIME_OK
reported total tokens: 6082
```

This proves that a subscription-backed Codex runtime is technically viable
for the tested environment. It does not freeze the CLI version, require the
reported model indefinitely, prove token-category breakdown, make human
credentials reusable by containers, or authorize unrestricted filesystem,
network, Git, or external effects.

Official references are evidence, not architectural authority:

- [Codex CLI and Sign in with ChatGPT](https://help.openai.com/en/articles/11381614-api-codex-cli-and-sign-in-with-chatgpt)
- [Managing Billing Settings on ChatGPT Web and Platform](https://help.openai.com/en/articles/9039756-managing-billing-settings-on-chatgpt-web-and-platform)
- [GPT-5.6 Luna model and pricing](https://developers.openai.com/api/docs/models/gpt-5.6-luna)
- [GPT-5.6 availability and pricing](https://openai.com/index/gpt-5-6/)

## D2 boundary and post-D2 direction

D2 remains the OpenAI Responses API direct-provider proof described by
`ADR-009` and `Issue #10`. Codex subscription execution does not replace D2
and this ADR does not change Issue #10 scope.

The proposed post-D2 implementation sequence is:

```text
D3A — Multi-Execution Backend & Normalized Economics Foundation
D3B — Hermes Runtime Adapter
D3C — Codex Subscription Runtime Adapter
D3D — Protected Tool Gateway Effects
```

This is implementation planning only. D3 has not started.

## Trade-offs

Benefits include simultaneous use of direct providers, governed runtimes, and
the deterministic simulator while preserving auditability and honest cost
semantics. The cost is additional routing, identity, authentication,
pricing, and reconciliation state. Subscription economics are useful for
capacity planning but cannot replace provider invoices or accounting facts.

## Migration direction

The D3A foundation should add explicit backend and routing records, separate
provider and runtime connection contracts, Pricing Catalog versions and
per-execution Pricing Snapshots, actual/equivalent budget dimensions, and
observability dimensions without rewriting historical D2 evidence. Existing
D2 OpenAI runs remain direct-provider runs; simulator records remain
synthetic. No historical cost is recalculated under a new price without a
new snapshot and correction evidence.

## Validation criteria

Before this ADR can be approved, reviewers must verify:

1. backend classes remain distinct in contracts and evidence;
2. concurrent backend use and explicit no-fallback behavior are testable;
3. subscription authentication never requires credential copying into
   containers;
4. actual and equivalent cost states cannot collapse to one field;
5. pricing snapshots are immutable and historical calculations stable;
6. partial/unknown token evidence remains honest;
7. actual and normalized budget checks are independent;
8. Codex compatibility evidence remains non-normative and dated;
9. D2 remains unchanged and D3 remains a proposal;
10. specialist approvals are recorded only after their owners explicitly
    review this revision.

## Open questions

- Which host/runtime bridge and session reference format will be selected?
- Which runtime-reported usage is authoritative for each Codex mode?
- Which pricing snapshot confidence and expiry rules apply to opaque runtime
  usage?
- Which exact fallback policies require human approval?
- Which D3A data contracts and migrations are needed?
