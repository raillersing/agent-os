---
document_id: MLC-001
title: Agent OS Model and Provider Lifecycle and Change Management Standard
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
created: 2026-08-13
last_reviewed: 2026-08-13
classification: internal
source_of_truth: false
related_documents:
  - MOD-001
  - CST-001
  - CTX-001
  - EVAL-001
  - RUN-001
  - AGC-001
  - INT-001
  - POL-001
  - SEC-001
  - THR-001
  - TST-001
  - QAG-001
  - OBS-001
  - OPS-001
  - AUD-001
related_adrs:
  - ADR-006
  - ADR-007
  - ADR-008
pending_approvals:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
---

# MLC-001 — Model and Provider Lifecycle and Change Management Standard

> **Status: In review.** This document proposes the lifecycle, qualification, rollout, rollback, suspension, and retirement process for model-provider bindings used by Agent OS. It is intentionally non-authoritative until the required review roles approve it.

## 1. Purpose

External and local AI models are moving dependencies. They may change because of:

- provider model releases;
- model snapshot changes;
- deprecations or removals;
- API behavior changes;
- capability changes;
- pricing changes;
- context/output limit changes;
- tool/function-call behavior changes;
- safety-policy changes;
- latency or availability changes;
- regional/data-processing changes;
- adapter changes;
- local model or inference-runtime upgrades.

Agent OS MUST NOT treat a model name configured once as a permanently stable implementation dependency.

This standard defines how model/provider changes should move from discovery to controlled use.

## 2. Core principle

A provider/model change is an engineering change with potential product, security, data, cost, and operational impact.

The default lifecycle SHOULD be:

```text
discovered
   ↓
registered candidate
   ↓
compatibility checked
   ↓
evaluated
   ↓
qualified for explicit profile
   ↓
limited rollout
   ↓
observed
   ↓
promoted
   ↓
maintained
   ↓
retired
```

At any point, the configuration may instead be:

```text
rejected
restricted
regressed
suspended
rolled back
retired
```

## 3. Lifecycle object

Lifecycle decisions SHOULD apply to a complete binding identity rather than a marketing model family name.

A binding record SHOULD identify where observable:

```yaml
binding_id:
provider_id:
provider_api_profile:
configured_model:
actual_model_identity_state:
actual_model:
model_snapshot_or_version:
region_profile:
endpoint_profile:
capabilities:
context_limits:
output_limits:
modalities:
tool_support:
pricing_profile:
data_policy_profile:
adapter_compatibility:
qualification_refs: []
status:
introduced_at:
last_verified_at:
retirement_at:
```

Unknown provider facts MUST remain `unknown` rather than inferred as stable guarantees.

## 4. Lifecycle states

Recommended states:

```text
discovered
candidate
compatibility_review
experimental
qualified_restricted
qualified
active
regressed
suspended
deprecated
retired
unavailable
unknown
```

`MOD-001` governs logical model profiles; this document governs the lifecycle of concrete provider/model bindings that may satisfy those profiles.

## 5. Discovery

A candidate may be discovered because of:

- provider release/change notice;
- operator request;
- architecture review;
- cost optimization;
- capability requirement;
- security/data requirement;
- provider incident;
- local inference improvement;
- deprecation of an active model.

Discovery alone MUST NOT make a model eligible for production-like or pilot execution.

## 6. Candidate registration

Before evaluation, a candidate SHOULD have a controlled record of:

- intended purpose;
- expected capabilities;
- source of configuration information;
- provider/model identity;
- API/adapter compatibility assumptions;
- known context/output limits;
- known data-policy restrictions;
- known pricing source/version;
- expected evaluation suites;
- intended rollout scope.

Marketing claims SHOULD NOT be treated as qualification evidence.

## 7. Compatibility gate

Compatibility checks SHOULD verify at minimum:

- provider API connectivity in controlled environment;
- authentication mechanism;
- request/response schema;
- streaming semantics where used;
- tool/function schema compatibility where used;
- structured-output behavior where required;
- context and output limits;
- cancellation/timeout behavior;
- model identity observability;
- usage observability;
- provider request/correlation identifiers where available;
- adapter error normalization;
- configured classification/region restrictions.

A compatibility pass means “can be integrated,” not “is behaviorally qualified.”

## 8. Behavioral qualification gate

Behavioral qualification is governed by `EVAL-001`.

Before promotion, the candidate SHOULD pass the suites required for its intended qualification profile, including where applicable:

- capability;
- grounding;
- instruction adherence;
- prompt-injection/authority resistance;
- tool behavior;
- repeated-run reliability;
- unknown/partial-state handling;
- usage/cost;
- latency;
- human acceptance.

Qualification evidence MUST identify the candidate binding and relevant context/agent profile versions.

## 9. Data and security gate

Security/Data review SHOULD establish:

- maximum allowed data classification;
- local-only requirements;
- provider/region allowlist status;
- prohibited data categories;
- redaction/minimization rules;
- external retention/training-use assumptions if governed;
- credential scope;
- network destination policy;
- logging/redaction implications;
- tool execution boundaries;
- threat-model deltas.

A model that is behaviorally strong but violates data/security constraints is not eligible for that operating profile.

## 10. Cost and quota gate

`CST-001` governs usage and cost architecture.

Lifecycle review SHOULD establish:

- pricing source and effective date/version;
- input/output/cached-token pricing dimensions where applicable;
- request/rate/quota constraints;
- expected cost distribution for target task class;
- high-cost failure modes;
- reservation/budget behavior;
- unknown-cost handling;
- fallback cost delta.

Unknown price MUST NOT be represented as zero cost.

## 11. Promotion decision

A promotion decision SHOULD explicitly state:

```text
binding identity
qualification profile
allowed task classes
allowed data classes
allowed environments
allowed tools/effects
human-review requirements
budget/quota profile
fallback eligibility
known limitations
rollback target
review/expiry date
```

A generic “approved model” flag without scope is insufficient for controlled agentic use.

## 12. Rollout stages

Recommended stages:

### Stage A — simulator only
Validate Agent OS logic without real model behavior/cost.

### Stage B — developer experimental
Real provider/local model, synthetic or explicitly permitted data, no protected external effects.

### Stage C — controlled internal
Qualified restricted profile with bounded users/tasks and enhanced evidence.

### Stage D — pilot
Explicitly approved pilot environment/profile with operational monitoring and rollback.

### Stage E — broader supported use
Only after evidence supports the expanded scope.

The MVP does not require Stage E.

## 13. Limited rollout controls

A limited rollout MAY be constrained by:

- workspace allowlist;
- user/role allowlist;
- task class;
- data classification;
- percentage of eligible runs;
- daily cost budget;
- concurrency;
- maximum context size;
- tool capability;
- mandatory human review;
- environment;
- time window.

Rollout constraints SHOULD be enforceable by policy/configuration rather than informal operator memory.

## 14. Shadow evaluation

Where technically and financially appropriate, a candidate MAY run in shadow mode against selected inputs with no authoritative or protected effect.

Shadow results SHOULD be clearly separated from user-visible authoritative results.

Shadow mode MUST NOT duplicate consequential tool calls.

## 15. Comparison and regression

Candidate comparison SHOULD reference the current accepted baseline.

Material regressions include:

- new critical safety failure;
- reduced task success beyond accepted threshold;
- increased unsupported-claim behavior;
- tool misuse;
- instruction-authority regression;
- cost amplification;
- latency degradation affecting NFRs;
- inability to establish actual identity/usage evidence required by policy;
- data-policy incompatibility.

Regression status SHOULD be visible to routing and release decisions.

## 16. Change classes

### Class 0 — metadata-only
No expected runtime behavioral impact.

### Class 1 — compatible operational change
Example: quota adjustment without behavior/model change.

### Class 2 — material binding change
Example: provider endpoint, model snapshot, pricing model, context limit, tool behavior, adapter behavior.

### Class 3 — high-risk change
Example: new provider, new data region, new tool-execution model, major context/profile change, model identity uncertainty, new protected-effect capability.

Classes 2–3 SHOULD trigger explicit compatibility/evaluation review before promotion.

## 17. Provider-side unannounced or ambiguous change

Agent OS cannot assume that all provider behavior changes are announced or fully versioned.

Potential drift signals include:

- changed model identity fields;
- changed response/schema behavior;
- eval regression;
- tool-call distribution shift;
- latency/cost shift;
- refusal/safety behavior shift;
- context-limit mismatch;
- new error patterns;
- provider documentation/configuration mismatch.

Material unexplained drift MAY suspend the binding pending review.

## 18. Model identity uncertainty

The runtime SHOULD distinguish identity evidence states such as:

```text
provider_reported
adapter_reported
locally_observed
configured_only
inferred
conflicted
unavailable
unknown
```

`configured_only` MUST NOT be displayed or stored as if it proves actual execution identity.

For qualification profiles requiring exact identity, inability to establish acceptable identity evidence SHOULD block promotion or trigger restriction.

## 19. Fallback lifecycle

Fallback bindings require their own lifecycle and qualification.

A fallback chain SHOULD NOT automatically inherit:

- qualification;
- data disclosure permission;
- region permission;
- budget permission;
- tool capability;
- human-review policy.

Before fallback execution, Agent OS SHOULD re-evaluate:

```text
capability compatibility
data-policy compatibility
security policy
cost/budget
tool behavior
approval impact
context limit
actual binding availability
```

No silent fallback is permitted where `ADR-006`/policy requires explicit visibility or approval.

## 20. Deprecation management

When a provider/model is announced for deprecation or retirement, the owner SHOULD record:

- announcement evidence/date;
- provider retirement date where known;
- affected logical model profiles;
- affected task classes/workspaces;
- proposed replacement;
- evaluation plan;
- migration deadline;
- rollback limitations;
- communication requirement.

A replacement SHOULD be qualified before the old binding becomes unavailable whenever practicable.

## 21. Emergency suspension

A binding SHOULD be suspendable rapidly when there is evidence of:

- data leakage risk;
- secret exposure;
- critical prompt-injection regression;
- unauthorized tool behavior;
- cross-workspace impact;
- provider compromise concern;
- severe cost runaway;
- material identity conflict;
- severe availability instability;
- repeated critical evaluation failure;
- policy or legal prohibition.

Suspension SHOULD preserve evidence and avoid deleting historical execution records.

## 22. Rollback

Every promoted binding SHOULD identify a rollback strategy where feasible.

Rollback MAY mean:

- return to previously qualified provider/model binding;
- restricted capability profile;
- simulator-only mode;
- local-only mode;
- disable affected task class;
- pause model execution entirely.

Rollback MUST NOT silently weaken data/security constraints merely to restore availability.

## 23. Operational degradation states

Agent OS SHOULD expose AI execution degradation explicitly.

Recommended state model:

```text
normal
   ↓
degraded
   ↓
restricted
   ↓
simulator_or_local_only
   ↓
paused
   ↓
emergency_stop
```

Transitions SHOULD be policy- and incident-driven rather than inferred solely by the model.

## 24. AI-specific incident categories

Operations SHOULD classify and rehearse at least:

```text
MODEL-QUALITY-DEGRADATION
PROVIDER-OUTAGE
PROVIDER-BEHAVIOR-DRIFT
MODEL-IDENTITY-CONFLICT
PROMPT-CONTEXT-REGRESSION
PROMPT-INJECTION-CAMPAIGN
TOOL-CALL-ANOMALY
UNSUPPORTED-CLAIM-SPIKE
REFUSAL-SPIKE
TOKEN-COST-AMPLIFICATION
LATENCY-DEGRADATION
CONTEXT-LEAKAGE
MEMORY-POISONING
EVAL-REGRESSION
PROVIDER-DATA-POLICY-CHANGE
```

This section extends `OPS-001`/`OBS-001`; it does not replace general incident response.

## 25. Detection signals

Potential signals include:

- eval-suite regression;
- increase in protected-action proposals;
- abnormal tool-call rate;
- unusual token/output growth;
- cost per accepted task increase;
- latency percentile shift;
- unknown model identity;
- provider error-rate increase;
- grounding/citation failure increase;
- prompt-injection detections;
- memory conflicts;
- operator/user incident reports.

A signal is not automatically proof of model failure, but it SHOULD be correlated with run/attempt/provider/context evidence.

## 26. Incident response actions

Depending on severity, actions MAY include:

- stop new routing to binding;
- preserve current evidence;
- invalidate qualification status;
- restrict task/data/tool scope;
- require human review;
- disable fallback;
- switch to known qualified binding;
- switch to simulator/local-only mode;
- revoke provider credential;
- quarantine affected memory/artifacts;
- run focused regression/evals;
- create sanitized incident regression cases;
- communicate known limitations.

No AI agent may close its own critical safety incident or re-qualify itself without the required human authority.

## 27. Evidence preservation

Lifecycle and incident evidence SHOULD correlate:

```text
provider/model binding
model identity state
model/context profile
agent/adapter version
run/attempt IDs
policy version
usage/cost records
eval qualification refs
observability traces
incident ID
actions/decisions
rollback target
```

Retention and access are governed by `DAT-002` and `AUD-001`.

## 28. Requalification triggers

A binding SHOULD be re-evaluated/requalified when materially affected by:

- model snapshot/version change;
- provider behavior change;
- adapter change;
- system/context profile change;
- tool schema/capability change;
- policy/security change;
- data classification change;
- pricing/quota change relevant to accepted cost profile;
- incident;
- qualification evidence expiry/staleness;
- material runtime dependency change affecting behavior.

## 29. Retirement

Retirement SHOULD:

- prevent new selection/routing;
- preserve historical identity references;
- preserve receipts/evidence according to retention policy;
- document replacement where applicable;
- expire credentials/endpoints no longer required;
- update model-profile routing configuration;
- retain enough metadata to interpret historical runs.

Historical runs MUST NOT be rewritten to pretend they used the replacement model.

## 30. Minimum MVP lifecycle baseline

Before the first real external model binding is treated as supported, Agent OS SHOULD implement or operationally establish:

1. candidate/active/suspended/retired states or equivalent;
2. deterministic simulator baseline;
3. explicit binding identity separate from logical model profile;
4. compatibility check evidence;
5. `EVAL-001` qualification evidence;
6. data/security eligibility decision;
7. usage/cost profile;
8. limited rollout scope;
9. rollback target;
10. model/provider identity evidence state;
11. no-silent-fallback policy;
12. ability to disable/suspend the binding without deleting history.

## 31. Governance roles

- Product: approves intended user/task scope and material behavior trade-offs.
- Architecture: owns provider/model binding architecture, compatibility, routing and rollback design.
- Security: owns provider security, data-disclosure controls and high-risk suspension criteria.
- Data: owns classification/region/data-use restrictions and provenance implications.
- Operations: owns credentials, runtime availability, monitoring, degradation and incident execution.
- Quality: owns qualification/evaluation evidence and regression gates.

A role may be assumed by the same human in an early project only where governance explicitly permits it; the evidence SHOULD still record which authority was exercised.

## 32. Relationship to `CTX-001` and `EVAL-001`

```text
MLC-001 selects and governs candidate bindings
              ↓
CTX-001 defines the effective instruction/context configuration
              ↓
EVAL-001 evaluates the combined behavioral configuration
              ↓
MLC-001 records qualification and rollout state
              ↓
OBS/OPS monitor real operation
              ↓
incidents/drift trigger re-evaluation or suspension
```

## 33. Review focus

Reviewers should specifically validate:

- lifecycle states and promotion criteria;
- exact scope of qualification inheritance;
- model identity requirements;
- fallback governance;
- provider/data policy gates;
- limited rollout controls;
- deprecation and emergency suspension behavior;
- AI-specific degradation/incident categories;
- minimum MVP lifecycle implementation boundary.
