---
document_id: ADP-HER-001
title: Agent OS Hermes Adapter Detailed Specification
version: 0.1.0
status: draft
register_status: proposed_unregistered
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-07-20
last_reviewed: 2026-07-20
classification: internal
source_of_truth: false
dependencies:
  - AGC-001
  - CAP-001
  - MOD-001
  - RUN-001
  - APR-001
  - ART-001
  - MEM-001
  - ORC-001
  - POL-001
  - SAN-001
  - AUD-001
  - CST-001
related_official_documents:
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
  - RTM-001
  - SAD-001
  - C4-001
  - C4-002
  - DDD-001
  - DAT-001
  - DCT-001
  - MEM-001
  - ORC-001
  - INT-001
  - SEC-001
  - THR-001
  - AGC-001
  - CAP-001
  - MOD-001
  - RUN-001
  - APR-001
  - ART-001
  - API-001
  - EVT-001
  - DEV-001
  - TST-001
  - QAG-001
  - OBS-001
  - DEP-001
  - OPS-001
  - BCP-001
  - PLG-001
related_proposed_documents:
  - UXA-001
  - DSN-001
  - A11Y-001
  - VVR-001
  - IAM-001
  - POL-001
  - SAN-001
  - SEC-002
  - DAT-002
  - AUD-001
  - CST-001
  - ADP-CDX-001
related_adrs:
  - ADR-TBD-HER-001
  - ADR-TBD-HER-002
  - ADR-TBD-HER-003
  - ADR-TBD-HER-004
  - ADR-TBD-HER-005
  - ADR-TBD-HER-006
  - ADR-TBD-HER-007
  - ADR-TBD-HER-008
---

# ADP-HER-001 — Agent OS Hermes Adapter Detailed Specification

> **Status: Draft — proposed/unregistered.** This document defines the proposed detailed adapter contract between Agent OS and a Hermes-family agent runtime. It covers discovery, identity, handshake, registration, capability mapping, session and run orchestration, tool mediation, model routing, memory exchange, approvals, sandboxing, costs, events, errors, cancellation, health, recovery, security, observability, evidence, compatibility, testing, and rollout. It does not claim that every Hermes distribution currently exposes all described interfaces, guarantee long autonomy or perfect memory, allow Hermes to bypass Agent OS governance, or select a final transport or implementation technology.

## 1. Purpose

The Hermes adapter allows Agent OS to orchestrate a Hermes-family runtime as one governed execution provider among several.

The adapter must translate between:

- Agent OS identities, tasks, runs, approvals, policies, artifacts, memory, costs, and audit;
- Hermes sessions, capabilities, tools, model routes, runtime events, outputs, and operational states.

The adapter exists to preserve Agent OS governance while exposing useful Hermes functionality in a predictable, testable, and provider-neutral way.

## 2. Objectives

The adapter must:

- register a Hermes runtime and its version;
- expose declared and validated capabilities;
- distinguish configured, enabled, ready, and healthy states;
- map Agent OS runs to Hermes sessions or jobs;
- map steps and attempts without losing retry history;
- mediate every protected tool through Agent OS policy and Tool Gateway;
- expose actual model/provider identity where available;
- exchange memory through explicit source and authority contracts;
- support cancellation and reconciliation;
- report usage, cost, artifacts, and evidence;
- preserve actor chains;
- fail closed when critical state is unknown;
- support local-first deployment and future stronger isolation.

## 3. Non-goals

ADP-HER-001 does not:

- make Hermes the Agent OS control plane;
- allow Hermes to approve actions;
- allow Hermes to grant roles or permissions;
- allow Hermes to select unrestricted network or filesystem access;
- assume that Hermes memory is authoritative;
- assume perfect persistence or lossless resume;
- assume cross-agent collaboration is available;
- assume provider/model identity is always available;
- claim production readiness for unsupported features;
- require a specific messaging protocol or SDK in this draft.

## 4. Principle — Agent OS remains authoritative

Hermes may execute or propose, but Agent OS owns identity, policy, approval, run state, artifact acceptance, and audit.

## 5. Principle — Capabilities are declared and validated

A Hermes claim is not enough; Agent OS validates what the runtime can actually do.

## 6. Principle — Session is not run authority

A Hermes session may support execution but cannot directly set Agent OS run state.

## 7. Principle — Tool calls are proposals

Protected tool calls are proposed by Hermes and enforced by Agent OS.

## 8. Principle — Memory is scoped and sourced

Hermes memory never becomes globally authoritative without verification.

## 9. Principle — Actual model identity is distinct

Configured, selected, reported, inferred, and unknown model identities remain separate.

## 10. Principle — Cancellation is observable

A cancellation request and a confirmed stop are separate states.

## 11. Principle — Unknown effect blocks blind retry

Hermes cannot cause automatic retry when an external effect remains uncertain.

## 12. Principle — Evidence is required

A completion claim must reference the evidence appropriate to the action.

## 13. Principle — No hidden autonomy

Background, long-running, or delegated work remains visible, bounded, and stoppable.

## 14. Principle — No privilege inheritance from branding

The Hermes name or runtime reputation grants no extra authority.

## 15. Principle — Version compatibility is explicit

Adapter, Hermes runtime, schema, capability, and protocol versions are negotiated.

## 16. Adapter bounded context

The Hermes adapter owns:

- runtime discovery;
- registration;
- handshake;
- version negotiation;
- capability translation;
- session translation;
- command/event translation;
- Hermes-specific health;
- Hermes-specific errors;
- model and tool metadata mapping;
- usage and receipt mapping;
- compatibility checks;
- adapter evidence.

It does not own Agent OS policy, approvals, run lifecycle, artifact acceptance, or memory verification.

## 17. Logical topology

```text
Agent OS Orchestrator
→ Hermes Adapter
→ Hermes Runtime
→ Hermes internal model/tool/session mechanisms
```

Protected capabilities additionally pass through:

```text
Hermes Runtime
→ Hermes Adapter
→ Agent OS Tool Gateway
→ Policy / Approval / Sandbox
→ protected target
```

## 18. Deployment modes

Potential deployment modes:

```text
embedded_local_process
local_sidecar
local_service
remote_managed_runtime
containerized_runtime
isolated_worker_pool
```

Each mode declares transport, identity, isolation, network, secrets, lifecycle, and recovery behavior.

## 19. Trust boundaries

Primary trust boundaries:

- Agent OS control plane to adapter;
- adapter to Hermes runtime;
- Hermes runtime to model provider;
- Hermes runtime to Tool Gateway;
- Hermes runtime to local filesystem;
- Hermes runtime to memory store;
- adapter to event and audit systems;
- adapter to cost and usage collectors.

Each boundary requires explicit authentication, authorization, schema, and evidence.

## 20. Runtime identity

A Hermes runtime registration contains:

- runtime ID;
- deployment mode;
- instance identity;
- runtime version;
- distribution/build;
- adapter version;
- environment;
- organization/workspace eligibility;
- endpoint or local process reference;
- supported transports;
- health;
- capability manifest;
- model/tool metadata;
- last validation;
- owner.

## 21. Adapter identity

The adapter uses its own workload identity, distinct from:

- the Hermes process identity;
- the logical agent profile;
- the requesting human;
- the sandbox identity;
- model-provider credentials.

This identity is scoped and revocable.

## 22. Handshake lifecycle

```text
discovered
→ connecting
→ authenticated
→ version_negotiated
→ capability_manifest_received
→ capability_validation
→ ready
```

Exceptional states:

```text
incompatible
authentication_failed
manifest_invalid
capability_drift
degraded
quarantined
revoked
unknown
```

## 23. Handshake request

The Agent OS side may send:

- adapter protocol version;
- requested schema versions;
- environment identity;
- Agent OS instance ID;
- nonce/challenge;
- required capability classes;
- policy profile;
- maximum message sizes;
- supported event delivery modes;
- supported cancellation modes;
- evidence requirements.

## 24. Handshake response

Hermes should return where supported:

- runtime identity;
- runtime version/build;
- protocol versions;
- manifest version;
- supported capability classes;
- supported session model;
- supported tool-call protocol;
- model metadata support;
- memory features;
- streaming support;
- cancellation support;
- resume support;
- usage reporting support;
- health endpoints;
- limitations;
- integrity metadata.

## 25. Handshake authentication

Authentication may use:

- local process identity;
- Unix-domain peer credentials;
- mutual TLS;
- workload identity;
- short-lived token;
- signed challenge.

The selected method depends on deployment mode and requires ADR.

## 26. Handshake integrity

The adapter verifies:

- endpoint identity;
- runtime version;
- manifest hash;
- protocol compatibility;
- nonce freshness;
- transport integrity;
- environment match;
- revocation state.

Unknown identity or mismatched environment blocks readiness.

## 27. Registration states

```text
proposed
registered
validated
enabled
ready
degraded
disabled
suspended
quarantined
revoked
retired
unknown
```

## 28. Registered versus enabled

`registered` means Agent OS knows the runtime.

`enabled` means an authorized scope permits use.

`ready` means the runtime, adapter, dependencies, credentials, and required controls are currently operational.

These states must not be collapsed.

## 29. Capability manifest

The Hermes capability manifest should contain:

- capability code;
- version;
- description;
- input/output schema references;
- side-effect class;
- network/filesystem needs;
- secret needs;
- sandbox profile compatibility;
- streaming;
- cancellation;
- resume;
- idempotency;
- evidence support;
- usage metrics;
- limitations.

## 30. Capability classes

Potential Hermes capability classes:

```text
conversation.session
task.execute
plan.generate
tool.propose
memory.read
memory.propose
artifact.generate
artifact.transform
model.invoke
stream.output
background.run
agent.delegate
state.resume
usage.report
health.report
```

Availability is runtime-specific.

## 31. Capability validation

Validation combines:

- manifest schema checks;
- protocol tests;
- positive functional tests;
- negative security tests;
- cancellation tests;
- evidence checks;
- usage/cost checks;
- version compatibility;
- operator review.

A declared capability becomes `validated` only after evidence.

## 32. Capability states

```text
declared
validated
enabled
ready
degraded
unsupported
incompatible
revoked
unknown
```

## 33. Capability drift

Capability drift occurs when:

- manifest changes;
- runtime version changes;
- observed behavior differs;
- schemas change;
- model/tool routes change;
- cancellation or evidence fails;
- security posture changes.

Material drift suspends affected capabilities until revalidation.

## 34. Capability-to-permission mapping

Each capability maps to Agent OS permissions.

Example:

```text
Hermes capability: tool.propose
Agent OS permissions:
  - tool.request
does not imply:
  - tool.execute
  - secret.read_raw
  - network.unrestricted
```

## 35. Capability-to-sandbox mapping

Capabilities declare compatible sandbox profiles.

Examples:

- plan generation may use `SAN-P1` or no execution;
- local transformation may use `SAN-P2`;
- repository edits may use `SAN-P3`;
- restricted provider/tool access may use `SAN-P4`;
- protected external effects may require `SAN-P5`.

Hermes cannot select a broader profile than policy permits.

## 36. Agent profile mapping

An Agent OS agent profile may reference:

- Hermes runtime;
- Hermes agent/persona identifier;
- allowed capability set;
- model profile;
- memory policy;
- tool policy;
- autonomy limits;
- budget;
- environment;
- owner;
- version.

Display labels are not security identities.

## 37. Hermes persona mapping

Hermes persona, prompt, role, or agent configuration is treated as runtime configuration.

It cannot:

- create Agent OS roles;
- grant permissions;
- approve;
- modify policies;
- weaken sandboxing;
- suppress audit;
- access secrets outside the broker.

## 38. Session model

A Hermes session is a runtime interaction context.

Potential attributes:

- session ID;
- runtime instance;
- agent/persona;
- model route;
- creation/last activity;
- status;
- context window;
- memory bindings;
- tool availability;
- streaming state;
- expiration;
- resume capability;
- lineage to Agent OS run or task.

## 39. Session states

```text
creating
active
idle
paused
streaming
waiting_for_tool
waiting_for_approval
cancelling
cancelled
completed
failed
expired
lost
unknown
```

## 40. Session ownership

Sessions are scoped to:

- organization/workspace;
- Agent OS principal;
- run or task;
- runtime instance;
- agent profile;
- environment.

Cross-workspace session reuse is prohibited.

## 41. Session creation

Agent OS creates a Hermes session through a governed command including:

- run/task snapshot;
- agent profile;
- model profile;
- memory scope;
- allowed capability set;
- tool policy;
- cost/budget context;
- correlation IDs;
- evidence requirements;
- expiration.

## 42. Session continuation

Continuation verifies:

- current session state;
- workspace;
- runtime identity;
- model route;
- policy;
- budget;
- memory scope;
- approval state;
- context integrity;
- expiration.

A stale or unknown session cannot resume protected work.

## 43. Session resume

Resume support is optional. Where supported, Agent OS records:

- resume token/reference;
- checkpoint identity;
- previous runtime/version;
- context fingerprint;
- unresolved tools/effects;
- expired authority;
- memory changes;
- usage.

Resume never restores expired permissions, approvals, or secret leases.

## 44. Lost session

When a Hermes session is lost:

- mark the session `lost`;
- preserve last confirmed event;
- inspect pending tool calls;
- mark unconfirmed external effects unknown;
- cancel or expire leases;
- collect available evidence;
- decide whether a new attempt is safe;
- never fabricate completion.

## 45. Run mapping

An Agent OS run may map to:

- one Hermes session;
- multiple Hermes sessions over retries;
- one session per step;
- one session per attempt;
- a Hermes background job plus session.

The mapping strategy is explicit and versioned.

## 46. Step mapping

Each Agent OS step sent to Hermes includes:

- step ID;
- attempt ID;
- immutable inputs;
- expected output;
- allowed capabilities;
- tool constraints;
- model profile;
- cost cap;
- deadline;
- approval state;
- evidence checklist.

## 47. Attempt mapping

Every retry creates a new Agent OS attempt and a new Hermes execution reference even if the same Hermes session continues.

The adapter preserves:

- attempt ordinal;
- previous attempt relation;
- reason;
- changed inputs;
- model/tool changes;
- cost;
- effect certainty.

## 48. Execution request

A Hermes execution request may include:

- command ID;
- task/run/step/attempt references;
- structured instruction;
- selected context references;
- memory references;
- expected output schema;
- capability allowlist;
- tool allowlist;
- sandbox profile;
- model profile;
- cost reservation;
- timeouts;
- cancellation token;
- correlation and causation.

## 49. Execution response

The response should distinguish:

- accepted;
- rejected;
- queued;
- started;
- partial output;
- completed candidate;
- waiting for tool;
- waiting for approval;
- cancelled;
- failed;
- unknown.

It must not directly set Agent OS run state.

## 50. Streaming output

Streaming may carry:

- text chunks;
- structured progress;
- tool proposals;
- plan updates;
- artifact references;
- usage updates;
- warnings;
- heartbeat;
- completion candidate.

Chunks are ordered, bounded, schema-versioned, and associated with session/attempt IDs.

## 51. Streaming integrity

The adapter should detect:

- missing sequence;
- duplicate sequence;
- out-of-order chunks;
- changed stream identity;
- oversized chunks;
- invalid schema;
- secret leakage;
- cross-workspace references.

Gaps remain visible.

## 52. Partial output

Partial output is not completion. Agent OS may display it but labels it as provisional and unaccepted.

A partial artifact is not an accepted artifact version.

## 53. Plan generation

Hermes may propose a plan with:

- steps;
- dependencies;
- capabilities;
- tools;
- model routes;
- estimates;
- risks;
- approvals;
- expected artifacts;
- completion criteria.

Agent OS validates and may modify or reject the plan.

## 54. Plan authority

A Hermes-generated plan is a proposal. It cannot:

- create permissions;
- override task scope;
- remove required approval;
- increase budget;
- broaden workspace;
- change retention;
- suppress evidence.

## 55. Background and long-running work

Background execution must be:

- registered;
- linked to run/attempt;
- visible;
- time-bounded;
- cost-bounded;
- cancellable where supported;
- heartbeat-monitored;
- subject to current policy;
- paused or stopped on revocation/emergency control.

No hidden autonomous daemon is permitted.

## 56. Autonomy levels

Hermes autonomy is represented through the Agent OS autonomy matrix, not a free-form runtime claim.

Potential adapter modes:

```text
assist_only
propose_plan
execute_low_risk_steps
execute_with_approval_gates
bounded_background_execution
```

Unbounded autonomy is not supported.

## 57. Delegation and sub-agents

If Hermes can delegate to internal sub-agents, the adapter must expose:

- parent session;
- child identifier;
- delegated objective;
- capability subset;
- model route;
- cost;
- lifecycle;
- evidence;
- tool calls;
- cancellation.

Opaque sub-agent activity is not acceptable for protected work.

## 58. Sub-agent authority

A child agent receives no broader authority than its parent and remains constrained by Agent OS policy, sandbox, budget, and approval.

Internal delegation cannot create a human approver.

## 59. Tool proposal model

Hermes tool calls are proposals containing:

- tool code/version;
- action;
- target;
- structured arguments;
- purpose;
- expected effect;
- side-effect class;
- idempotency key suggestion;
- required secrets;
- network/filesystem needs;
- cost estimate;
- evidence expectation.

## 60. Tool Gateway mediation

The adapter sends tool proposals to Agent OS Tool Gateway.

The Tool Gateway:

- authenticates the adapter/runtime;
- verifies workspace and attempt;
- validates schema and target;
- evaluates policy;
- checks approval;
- selects sandbox/secret/network controls;
- enforces idempotency;
- executes;
- returns structured result and certainty.

## 61. Tool result mapping

Hermes receives only the result fields needed for continuation.

The adapter maps:

```text
accepted
denied
approval_required
completed
partial
failed
unknown
reconciliation_required
```

Raw secrets and hidden policy internals are excluded.

## 62. Direct tool access

Direct Hermes access to protected external APIs is denied unless an explicitly approved integration provides controls equivalent to the Tool Gateway.

Direct access is never enabled merely because Hermes supports a plugin or MCP endpoint.

## 63. MCP direction

MCP servers or equivalent tool protocols may be exposed through Agent OS governance.

Requirements:

- registered server identity;
- capability manifest;
- permissions;
- transport security;
- schemas;
- workspace scope;
- secret brokerage;
- network policy;
- audit;
- revocation;
- health;
- versioning.

MCP connectivity is not authentication or authorization by itself.

## 64. Tool-call cancellation

Tool-call cancellation support is declared per tool.

The adapter distinguishes:

- cancellation requested;
- cancellation accepted;
- effect confirmed absent;
- effect possibly occurred;
- effect unknown.

Hermes must not retry a protected tool after unknown effect.

## 65. Model profile mapping

Agent OS model profiles map to Hermes runtime configuration:

- provider;
- model family;
- actual model identity source;
- temperature and generation controls;
- context/output limits;
- safety settings;
- region/account;
- fallback policy;
- pricing version;
- data handling.

## 66. Configured versus actual model

The adapter records:

```text
configured model
selected model
Hermes-reported model
provider-reported model
inferred model
unknown model
```

These states remain distinct.

## 67. Model fallback

Hermes may request fallback only when Agent OS policy permits it.

A material fallback may require:

- policy re-evaluation;
- approval;
- cost re-estimation;
- data-policy check;
- context adjustment;
- evidence.

Silent fallback is prohibited.

## 68. Model capability validation

The adapter validates where possible:

- context window;
- modalities;
- tool/function support;
- structured output;
- streaming;
- latency class;
- provider route;
- usage reporting;
- cancellation;
- safety constraints.

Unknown capability remains unknown.

## 69. Model errors

Model/provider errors are mapped into controlled categories:

```text
authentication
authorization
rate_limit
quota
invalid_request
context_too_large
unsupported_capability
provider_unavailable
timeout
safety_block
content_error
billing_or_budget
unknown
```

## 70. Prompt construction boundary

Agent OS controls authoritative system governance instructions. Hermes may add runtime formatting but cannot replace or weaken:

- identity;
- workspace;
- policy;
- approval;
- secret;
- sandbox;
- audit;
- cost;
- retention instructions.

## 71. Prompt content minimization

The adapter sends only the context required for the task and selected memory/artifacts. It avoids full workspace dumps, unrelated history, hidden metadata, secrets, and cross-project content.

## 72. Prompt and output fingerprints

For consequential execution, the adapter records fingerprints of:

- structured instruction;
- selected context;
- model profile;
- tool schema set;
- output candidate.

Fingerprints support audit and approval without storing full content by default.

## 73. Memory architecture boundary

Hermes memory is treated as a runtime-local or provider-local memory source unless explicitly integrated with Agent OS Memory.

Agent OS Memory remains the authoritative governed memory layer.

## 74. Memory read

A Hermes memory-read request includes:

- workspace;
- project/task;
- purpose;
- query;
- classification ceiling;
- source/authority filters;
- freshness;
- maximum records/tokens;
- cost limit.

Agent OS returns governed memory references and safe content.

## 75. Memory proposal

Hermes may propose memory with:

- content;
- source references;
- scope;
- purpose;
- classification;
- confidence;
- suggested authority;
- freshness;
- conflicts;
- retention;
- generating run/attempt.

The proposal is not automatically verified.

## 76. Memory verification

Only authorized Agent OS workflows may verify, reject, or resolve memory. Hermes cannot mark its own proposal authoritative.

## 77. Memory synchronization

If runtime-local Hermes memory is enabled, synchronization requires:

- explicit scope;
- source lineage;
- direction;
- conflict policy;
- deletion propagation;
- classification;
- encryption;
- retention;
- health;
- evidence.

Bidirectional unsupervised synchronization is not a default.

## 78. Memory deletion

Source deletion, workspace deletion, hold, or retention expiry triggers:

- Agent OS memory action;
- Hermes-local memory deletion request where applicable;
- embedding/index cleanup;
- provider deletion tracking;
- evidence;
- unknown status if confirmation is unavailable.

## 79. Artifact generation

Hermes may generate artifact candidates.

The adapter records:

- type;
- content/file reference;
- size;
- hash;
- source inputs;
- model/tool;
- run/attempt;
- classification;
- validation needs;
- provenance;
- completion state.

## 80. Artifact transformation

Transformations require exact input artifact versions and produce new candidate versions.

Hermes cannot overwrite an accepted artifact in place.

## 81. Artifact validation

The adapter routes outputs through Agent OS validation and quarantine.

Hermes success does not imply:

- malware-free;
- schema-valid;
- accessible;
- policy-compliant;
- accepted;
- exportable.

## 82. Artifact previews

Preview generation uses safe derived representations and profile-specific execution. Hermes cannot actively render untrusted content in the control plane.

## 83. Artifact acceptance

Acceptance is an Agent OS decision made by authorized workflow/humans. Hermes may recommend acceptance but cannot set it.

## 84. Usage reporting

Hermes should report supported usage metrics such as:

- input/output/cache tokens;
- requests;
- model/provider;
- tool proposals;
- tool executions by reference;
- session duration;
- background duration;
- memory retrieval;
- artifact processing;
- retries;
- provider receipts.

Unsupported metrics remain explicit.

## 85. Usage completeness

The adapter records whether usage is:

```text
complete
complete_with_limitations
partial
estimated
delayed
unsupported
unknown
```

## 86. Cost estimation

Before execution, the adapter may provide:

- model estimate;
- tool estimate;
- duration estimate;
- memory/retrieval estimate;
- artifact processing estimate;
- confidence;
- assumptions.

Agent OS `CST-001` remains authoritative for budget decisions.

## 87. Budget enforcement

Hermes receives:

- reservation reference;
- cost cap;
- threshold behavior;
- permitted model/tool set;
- unknown-cost policy.

It cannot modify these values.

## 88. Cost overrun

When usage approaches or exceeds limits:

- emit usage update;
- pause or stop if supported;
- block new tool/model calls;
- request approval where policy allows;
- preserve partial output;
- record overrun;
- avoid hidden continuation.

## 89. Unknown cost

If Hermes cannot report cost-relevant usage:

- mark unsupported/unknown;
- use bounded estimates if available;
- apply policy cap;
- require approval or block as configured;
- reconcile with provider/invoice later.

Unknown cost is never reported as zero.

## 90. Policy integration

The adapter requests policy decisions for:

- runtime enablement;
- session creation/resume;
- capability use;
- memory read/write;
- model/provider route;
- tool proposal;
- artifact export;
- background execution;
- cost overrun;
- cancellation/retry;
- support access.

Hermes never interprets policy text as optional advice.

## 91. Approval integration

Approvals may govern:

- high-risk tool;
- external write;
- long background execution;
- sensitive memory access;
- restricted data disclosure;
- model/provider fallback;
- high cost;
- artifact export;
- destructive action.

Approval binds to exact material fields.

## 92. Approval wait state

When approval is required:

- session/attempt enters `waiting_for_approval`;
- protected action is not dispatched;
- relevant non-sensitive context is preserved;
- timeout/expiry applies;
- cancellation remains available;
- policy is re-evaluated after approval.

## 93. Approval denial

On denial:

- Hermes receives a controlled denial reason;
- no protected effect occurs;
- the plan may be revised within task scope;
- denial is audited;
- no automatic alternative bypass is attempted.

## 94. Approval invalidation

Material changes after approval invalidate the path, including:

- target;
- tool;
- arguments;
- data;
- model/provider;
- cost;
- sandbox;
- network;
- secret purpose;
- policy;
- expiration.

## 95. Sandbox integration

Hermes execution requirements are translated to an immutable `SAN-001` specification.

Hermes may request but cannot set:

- filesystem mounts;
- writable roots;
- network access;
- secret access;
- process limits;
- runtime image;
- devices;
- tool bindings.

## 96. Hermes local execution

If Hermes launches local commands internally, one of two models is required:

1. Hermes commands are fully mediated through Agent OS Sandbox/Tool Gateway; or
2. the entire Hermes runtime itself runs inside an approved sandbox profile.

Unmediated host command execution is prohibited.

## 97. Network access

Hermes network needs are declared by capability and action. Agent OS applies destination, protocol, port, DNS, proxy, data-classification, and rate rules.

No broad internet access is inherited from the host.

## 98. Secret access

Hermes receives secret references or brokered results, not raw platform secrets by default.

Secret access is bound to:

- workspace;
- session/attempt;
- capability/tool;
- destination;
- purpose;
- expiry;
- policy/approval.

## 99. Security events

Security-relevant Hermes events include:

- authentication failure;
- identity mismatch;
- manifest drift;
- capability drift;
- policy bypass attempt;
- direct tool/network attempt;
- secret request denial;
- cross-workspace reference;
- prompt-injection signal;
- sandbox violation;
- evidence failure;
- unknown external effect.

## 100. Prompt-injection handling

Content from prompts, tools, web, memory, artifacts, or internal Hermes plans is untrusted.

The adapter blocks any attempt to reinterpret such content as:

- permission;
- approval;
- secret authority;
- sandbox change;
- workspace change;
- policy change;
- audit suppression;
- cost override.

## 101. Adapter errors

Controlled adapter error categories:

```text
connection_error
authentication_error
authorization_error
protocol_incompatible
schema_invalid
runtime_unavailable
runtime_degraded
capability_unsupported
capability_not_ready
session_not_found
session_lost
model_error
tool_error
memory_error
artifact_error
usage_error
cost_error
cancellation_error
evidence_error
security_violation
unknown_error
```

## 102. Error envelope

An error envelope contains:

- error code;
- category;
- safe message;
- retryability;
- effect certainty;
- session/attempt;
- component;
- correlation ID;
- source time;
- evidence reference;
- remediation hint;
- no raw secrets.

## 103. Retryability

Retry states:

```text
not_retryable
retryable_same_attempt
retryable_new_attempt
retry_after_reconciliation
retry_after_approval
retry_after_operator_action
unknown
```

Protected retries normally create a new Agent OS attempt.

## 104. Backoff

Retry backoff is bounded and policy-aware. It considers:

- provider rate limits;
- runtime health;
- cost;
- deadline;
- user cancellation;
- repeated identical failure;
- external effect uncertainty.

Infinite retry loops are prohibited.

## 105. Cancellation model

Cancellation phases:

```text
requested
acknowledged
stopping
stopped
cleanup_pending
cleaned
effect_unknown
reconciliation_required
```

The adapter must not map `requested` directly to `cancelled`.

## 106. Cancellation propagation

Agent OS cancellation propagates to:

- Hermes session/job;
- streaming;
- pending tool proposals;
- sandbox;
- model request if supported;
- background child agents;
- secret leases;
- network;
- reservation release after reconciliation.

## 107. Cancellation timeout

If Hermes does not confirm stop:

- mark cancellation incomplete;
- revoke privileged channels;
- quarantine or terminate runtime if needed;
- preserve evidence;
- mark effects unknown;
- require operator reconciliation.

## 108. Pause and resume

Pause support is optional and capability-declared. Pause must suspend new protected actions and privileged channels.

Resume revalidates policy, approval, budget, model, memory, runtime version, and session integrity.

## 109. Heartbeat

Hermes emits or answers heartbeat with:

- runtime/session identity;
- timestamp;
- current state;
- progress marker;
- active child agents;
- pending tool/approval;
- usage snapshot;
- health;
- last evidence checkpoint.

Heartbeat absence triggers degraded/lost handling.

## 110. Health model

Health dimensions:

```text
transport
runtime
session_engine
model_route
tool_bridge
memory_bridge
event_stream
usage_meter
evidence
sandbox_integration
```

## 111. Health states

```text
healthy
degraded
unavailable
incompatible
quarantined
unknown
```

Overall readiness depends on the capabilities requested, not only a generic ping.

## 112. Readiness checks

Readiness may verify:

- authenticated transport;
- compatible protocol;
- valid manifest;
- required model route;
- Tool Gateway;
- memory bridge;
- sandbox;
- cost meter;
- audit pipeline;
- event stream;
- no active quarantine.

## 113. Degraded operation

A degraded runtime may still support selected low-risk capabilities. Agent OS must expose exact affected capabilities and avoid a single misleading green state.

## 114. Runtime quarantine

Quarantine may be triggered by:

- identity mismatch;
- manifest tampering;
- capability drift;
- policy bypass;
- cross-workspace behavior;
- secret leakage;
- repeated evidence failure;
- suspicious network/tool access;
- compromised build.

Quarantined runtimes receive no new protected work.

## 115. Runtime revocation

Revocation invalidates registration, credentials, sessions, leases, pending dispatches, and cache entries. Historical evidence remains.

## 116. Upgrade compatibility

Before a Hermes runtime or adapter upgrade:

- compare protocol/schema versions;
- revalidate manifest;
- run conformance tests;
- test existing session behavior;
- test cancellation;
- test tool mediation;
- test usage/cost;
- test evidence;
- stage/canary;
- preserve rollback.

## 117. Rolling upgrade

If rolling upgrades are supported:

- new sessions target validated versions;
- existing sessions remain on original runtime or migrate through governed resume;
- mixed-version state is visible;
- capability differences are respected;
- rollback remains possible.

## 118. Session migration

Session migration is optional. Where supported, it requires:

- checkpoint;
- context fingerprint;
- model compatibility;
- memory state;
- unresolved effects;
- policy/approval revalidation;
- new runtime identity;
- evidence.

Unsupported migration results in a new attempt.

## 119. Recovery after runtime crash

1. mark runtime/session lost;
2. stop new dispatch;
3. revoke privileged channels;
4. inspect last durable events;
5. reconcile tool effects;
6. collect checkpoints;
7. determine resumability;
8. create new attempt if safe;
9. preserve cost and partial artifacts;
10. restore readiness only after validation.

## 120. Recovery after Agent OS restart

After Agent OS restart:

- reload Hermes registrations;
- reauthenticate adapters;
- reconcile active sessions;
- verify runtime versions;
- invalidate stale leases;
- compare event sequences;
- restore pending approvals;
- preserve unknown effects;
- resume only after policy and budget checks.

## 121. Offline behavior

For local/offline operation:

- use approved local model/tool routes;
- deny external network unless explicitly enabled;
- use local memory/artifact stores;
- preserve audit locally;
- expose unavailable provider capabilities;
- avoid pretending remote tools succeeded;
- reconcile only when connectivity returns.

## 122. Event model

Adapter events should use the Agent OS event envelope and include:

- event ID;
- runtime/session;
- run/step/attempt;
- workspace/environment;
- actor chain;
- event type;
- sequence;
- occurred/recorded time;
- payload schema;
- correlation/causation;
- classification;
- integrity metadata.

## 123. Hermes lifecycle events

Potential events:

```text
HermesRuntimeDiscovered
HermesRuntimeRegistered
HermesHandshakeCompleted
HermesManifestValidated
HermesCapabilityDriftDetected
HermesRuntimeReady
HermesRuntimeDegraded
HermesRuntimeQuarantined
HermesSessionCreated
HermesSessionResumed
HermesSessionLost
HermesExecutionAccepted
HermesExecutionStarted
HermesOutputChunkReceived
HermesToolProposed
HermesWaitingForApproval
HermesUsageReported
HermesArtifactProposed
HermesCancellationAcknowledged
HermesExecutionCompletedCandidate
HermesExecutionFailed
HermesEffectUnknown
```

## 124. Event ordering

Session streams use sequence numbers or equivalent ordering. Late, duplicate, missing, and conflicting events remain explicit and are reconciled.

## 125. Event delivery

Potential delivery modes:

- synchronous response;
- server-sent stream;
- WebSocket;
- message broker;
- polling;
- local IPC.

The final transport requires ADR.

## 126. Event replay

Where supported, the adapter can request replay from a sequence/checkpoint. Replay is idempotent and cannot duplicate tool effects or approval consumption.

## 127. Audit evidence

`AUD-001` evidence for Hermes should cover:

- runtime registration;
- handshake;
- manifest;
- capability validation;
- session creation/resume/loss;
- model selection/fallback;
- memory read/proposal;
- tool proposal/result;
- approval wait/decision;
- sandbox;
- usage/cost;
- artifacts;
- cancellation;
- health;
- upgrade/recovery;
- unknown effects.

## 128. Evidence completeness

A Hermes execution evidence package may be:

```text
complete
complete_with_declared_limitations
partial
incomplete
conflicted
unknown
```

Missing Hermes-native receipts do not become fabricated Agent OS evidence.

## 129. Observability

Monitor:

- runtime availability;
- handshake latency;
- capability readiness;
- session creation latency;
- stream lag;
- event gaps;
- tool-proposal rate;
- approval wait time;
- model errors;
- fallback;
- memory errors;
- usage freshness;
- cancellation latency;
- lost sessions;
- evidence completeness;
- cost variance;
- quarantine events.

## 130. Metrics

Potential metrics:

```text
hermes_runtime_ready
hermes_sessions_active
hermes_session_create_seconds
hermes_event_lag_seconds
hermes_event_gap_total
hermes_tool_proposals_total
hermes_tool_denials_total
hermes_approval_wait_seconds
hermes_model_requests_total
hermes_model_fallback_total
hermes_memory_reads_total
hermes_cancellation_seconds
hermes_session_lost_total
hermes_unknown_effect_total
hermes_usage_delay_seconds
hermes_evidence_incomplete_total
```

## 131. Alerts

Potential alerts:

```text
hermes_runtime_unavailable
hermes_identity_mismatch
hermes_manifest_invalid
hermes_capability_drift
hermes_event_stream_stalled
hermes_session_lost
hermes_tool_gateway_bypass_attempt
hermes_cross_workspace_reference
hermes_secret_exposure_detected
hermes_cost_overrun
hermes_usage_meter_delayed
hermes_cancellation_timeout
hermes_effect_unknown
hermes_evidence_failure
hermes_runtime_quarantined
```

## 132. Operational dashboard

The Hermes operations view should show:

- runtime/version;
- adapter version;
- environment;
- readiness;
- capability matrix;
- active sessions;
- degraded dependencies;
- event freshness;
- usage freshness;
- cost status;
- incidents;
- quarantines;
- last validation;
- pending upgrade.

## 133. Runbooks

Required runbooks:

```text
register Hermes runtime
validate capability manifest
enable Hermes for workspace
disable or revoke Hermes
investigate handshake failure
investigate capability drift
recover lost session
reconcile unknown tool effect
resolve event gap
handle model fallback
handle usage delay
cancel stuck execution
quarantine Hermes runtime
upgrade adapter/runtime
rollback adapter/runtime
restore after Agent OS restart
delete Hermes-local memory/session data
```

## 134. Security controls

Hermes integration must satisfy at minimum:

- authenticated workload identity;
- default deny;
- workspace scope;
- capability validation;
- Tool Gateway mediation;
- sandbox enforcement;
- secret brokerage;
- approval independence;
- cost limits;
- audit evidence;
- cross-workspace tests;
- prompt-injection boundary;
- revocation and quarantine.

## 135. Data classification

Hermes requests and outputs inherit Agent OS classification. The adapter enforces provider, memory, artifact, log, and export rules from `DAT-002`.

Hermes-local caches and sessions are included in deletion and retention.

## 136. Retention

Potential retention direction:

- transient streams/session caches: `R0/R1`;
- operational session/run metadata: `R2`;
- accepted artifacts: according to artifact profile;
- audit evidence: `R4`;
- incident data: `R4/R5`;
- provider-held data: tracked separately.

Exact periods remain governed by `DAT-002`.

## 137. Deletion

Deletion workflows may need to remove:

- Hermes session state;
- runtime-local history;
- local cache;
- memory;
- embeddings;
- artifact candidates;
- logs;
- provider copies;
- credentials/leases;
- search indexes.

Unconfirmed provider/runtime deletion remains pending or unknown.

## 138. Privacy

The adapter minimizes personal data and avoids sending user profile fields not required for execution. Stable principal references are preferred over full names/emails in runtime context.

## 139. API direction

Potential adapter resources:

```text
/hermes-runtimes
/hermes-runtimes/{id}/manifest
/hermes-runtimes/{id}/capabilities
/hermes-runtimes/{id}/health
/hermes-sessions
/hermes-executions
/hermes-events
/hermes-usage
/hermes-evidence
/hermes-quarantines
```

## 140. Command API direction

Potential commands:

```text
discover
register
authenticate
negotiate
validate-manifest
enable
disable
revoke
create-session
resume-session
execute-step
send-input
cancel
pause
resume
request-event-replay
reconcile-effect
quarantine
release-quarantine
upgrade
rollback
```

Clients cannot set readiness, completion, capability validation, or effect certainty directly.

## 141. Data model direction

Core entities:

```text
HermesRuntimeRegistration
HermesRuntimeInstance
HermesHandshake
HermesManifest
HermesCapabilityMapping
HermesAgentProfileMapping
HermesSession
HermesSessionCheckpoint
HermesExecutionReference
HermesEventCursor
HermesModelObservation
HermesToolProposal
HermesMemoryExchange
HermesUsageReport
HermesEvidencePackage
HermesHealthSnapshot
HermesQuarantine
HermesCompatibilityRecord
```

## 142. Protocol compatibility

Compatibility dimensions:

- adapter protocol;
- event envelope;
- capability manifest;
- tool proposal schema;
- model observation schema;
- memory exchange;
- usage report;
- cancellation;
- checkpoint/resume;
- evidence package.

Each dimension has version and compatibility status.

## 143. Compatibility states

```text
compatible
compatible_with_limitations
requires_translation
incompatible
untested
unknown
```

## 144. Compatibility matrix

The compatibility matrix should list:

- Agent OS version;
- adapter version;
- Hermes runtime/distribution version;
- protocol versions;
- validated capabilities;
- limitations;
- test date;
- environment;
- evidence.

## 145. Feature flags

New Hermes capabilities may be introduced behind controlled flags by:

- environment;
- workspace;
- agent profile;
- capability;
- runtime version;
- risk class.

Feature flags do not override policy or approval.

## 146. Canary rollout

Canary rollout should use explicit development/test workspaces and low-risk capabilities before broader enablement.

Observe:

- errors;
- event gaps;
- cost;
- cancellation;
- evidence;
- policy denials;
- tool behavior;
- memory behavior.

## 147. Rollback

Rollback may revert adapter/runtime version or disable specific capabilities.

Rollback preserves:

- sessions that cannot migrate as lost/blocked;
- run/attempt history;
- cost;
- artifacts;
- evidence;
- unknown effects;
- quarantine findings.

## 148. Conformance test strategy

Test layers:

```text
manifest schema
handshake
identity
version negotiation
capability validation
session lifecycle
run/step/attempt mapping
streaming
tool mediation
model routing
memory
artifact
policy and approval
sandbox
usage and cost
cancellation
health
events
evidence
security abuse
fault injection
performance
accessibility
visual operations UI
upgrade and rollback
```

## 149. Handshake tests

Test valid registration, invalid identity, wrong environment, nonce replay, incompatible protocol, invalid manifest, oversized manifest, revoked runtime, and stale validation.

## 150. Capability tests

For each capability:

- declaration;
- schema;
- positive execution;
- denial;
- readiness loss;
- version drift;
- evidence;
- usage;
- cancellation;
- unknown state.

A capability without negative tests is not validated.

## 151. Session tests

Test creation, workspace isolation, continuation, idle expiry, resume, lost session, runtime restart, multiple sessions, cross-run reuse, and deletion.

## 152. Streaming tests

Test ordering, duplicate chunks, gaps, reconnect, replay, oversized output, secret leakage, cancellation, late completion, and mixed session IDs.

## 153. Tool tests

Test proposal schema, denial, approval required, approval granted, target change, idempotency, unknown effect, cancellation, direct bypass, secret use, network, and receipts.

## 154. Model tests

Test configured/reported identity, fallback, context limits, tool support, streaming, usage, provider errors, cost change, data restriction, and unknown identity.

## 155. Memory tests

Test scoped read, authority filters, proposal, verification, conflict, deletion, provider/local memory, cross-workspace denial, stale memory, and embedding cleanup.

## 156. Artifact tests

Test generation, transformation, partial output, large files, active content, validation, quarantine, acceptance denial, export, and deletion.

## 157. Approval tests

Test waiting state, ineligible approver, denial, expiry, fingerprint change, consumption, policy change, cancellation while waiting, and session resume.

## 158. Sandbox tests

Test command mediation, filesystem, network, secrets, process limits, Tool Gateway, host access denial, sandbox unavailability, cleanup, and evidence.

## 159. Cost tests

Test estimates, token/usage reports, unsupported metrics, delayed usage, reservation, overrun, cost approval, fallback price change, cancellation cost, and invoice reconciliation.

## 160. Cancellation tests

Test cancellation before start, during model call, during tool wait, during tool execution, during streaming, child agents, timeout, unknown effect, and cleanup.

## 161. Fault-injection tests

Inject runtime crash, adapter crash, transport partition, event loss, duplicate events, sequence reset, model outage, Tool Gateway outage, memory outage, meter outage, audit outage, and Agent OS restart.

## 162. Security-abuse tests

Attempt to:

- forge runtime identity;
- claim unvalidated capability;
- change workspace;
- bypass Tool Gateway;
- request raw secret;
- self-approve;
- widen sandbox;
- hide cost;
- suppress audit;
- replay approval;
- inject policy through prompt;
- exfiltrate cross-workspace memory;
- mark unknown effect confirmed.

## 163. Performance direction

Measure handshake, session creation, stream latency, event throughput, tool round-trip, memory retrieval, cancellation, resume, usage reporting, evidence packaging, and concurrent-session capacity.

Formal targets remain in `NFR-001`.

## 164. Accessibility and visual validation

Hermes administration and runtime views follow proposed/unregistered `A11Y-001` and `VVR-001`.

Scenarios include:

- registration;
- manifest;
- capability ready/degraded/unknown;
- session active/waiting/cancelling/lost;
- approval wait;
- model fallback;
- usage stale;
- cost overrun;
- event gap;
- quarantine;
- upgrade;
- rollback.

## 165. MVP scope

Recommended MVP Hermes adapter:

- one local Hermes runtime;
- authenticated local transport;
- runtime registration and version;
- basic capability manifest;
- one session per attempt direction;
- text/structured output streaming;
- Tool Gateway proposals;
- explicit model profile mapping;
- governed memory read/proposal;
- artifact candidates;
- cancellation;
- usage report where available;
- explicit unknown usage/cost;
- health and event cursor;
- audit evidence;
- no unbounded background autonomy;
- no direct protected tool access;
- no cross-agent opaque delegation.

## 166. Pilot readiness

Before pilot:

- runtime identity and handshake pass;
- manifest is validated;
- enabled capabilities pass positive/negative tests;
- workspace isolation passes;
- Tool Gateway mediation passes;
- approvals cannot be bypassed;
- sandbox and secret boundaries pass;
- model identity/fallback is visible;
- memory authority is governed;
- usage/cost unknowns are visible;
- cancellation and lost-session recovery work;
- event gaps and evidence failures are visible;
- runtime quarantine works;
- no critical adapter defect remains.

## 167. Controlled-commercial direction

A controlled commercial profile may add:

- remote managed Hermes runtimes;
- stronger workload identity and mTLS;
- dedicated runtime pools;
- customer-specific runtime placement;
- signed manifests/builds;
- stronger attestation;
- richer resume/checkpoint;
- customer-configurable model/tool policies;
- higher-availability event streams;
- customer audit exports;
- formal compatibility certification.

## 168. Maturity stages

```text
H0 — manual/local invocation outside Agent OS
H1 — registered runtime, sessions, basic output, governed tools
H2 — capabilities, memory, cost, cancellation, evidence, recovery
H3 — remote pools, signed manifests, stronger isolation, customer policies
H4 — mature multi-tenant Hermes integration programme
```

## 169. Requirement catalogue — Identity, registration, and compatibility

- `HER-REQ-REG-001` — Hermes runtime and adapter use distinct authenticated identities.
- `HER-REQ-REG-002` — Runtime registration records version, environment, owner, and integrity metadata.
- `HER-REQ-REG-003` — Handshake negotiates protocol and schema versions.
- `HER-REQ-REG-004` — Unknown or mismatched runtime identity blocks readiness.
- `HER-REQ-REG-005` — Capabilities are declared and validated before use.
- `HER-REQ-REG-006` — Capability drift suspends affected capabilities.
- `HER-REQ-REG-007` — Registered, enabled, ready, degraded, and revoked remain distinct.
- `HER-REQ-REG-008` — Compatibility is recorded by Agent OS, adapter, runtime, protocol, and capability version.
- `HER-REQ-REG-009` — Upgrade and rollback are tested.
- `HER-REQ-REG-010` — Quarantined or revoked runtimes receive no new protected work.
- `HER-REQ-REG-011` — Cross-environment registration is denied.
- `HER-REQ-REG-012` — Feature flags do not override policy.

## 170. Requirement catalogue — Sessions, runs, and execution

- `HER-REQ-RUN-001` — Every Hermes session is scoped to workspace, run/task, runtime, and agent profile.
- `HER-REQ-RUN-002` — Every retry creates a new Agent OS attempt reference.
- `HER-REQ-RUN-003` — Hermes cannot directly set Agent OS run state.
- `HER-REQ-RUN-004` — Partial output is never treated as completion.
- `HER-REQ-RUN-005` — Background work is visible, bounded, and cancellable.
- `HER-REQ-RUN-006` — Opaque child-agent activity is not accepted for protected work.
- `HER-REQ-RUN-007` — Session resume revalidates policy, approvals, budget, and identity.
- `HER-REQ-RUN-008` — Lost sessions preserve unknown effects and partial evidence.
- `HER-REQ-RUN-009` — Cancellation request and confirmed stop remain distinct.
- `HER-REQ-RUN-010` — Heartbeat and event freshness are monitored.
- `HER-REQ-RUN-011` — Run completion requires Agent OS validation.
- `HER-REQ-RUN-012` — Execution evidence references exact session and attempt.

## 171. Requirement catalogue — Tools, models, memory, and artifacts

- `HER-REQ-CAP-001` — Protected tool calls are mediated through Agent OS Tool Gateway.
- `HER-REQ-CAP-002` — Hermes cannot receive unrestricted host, network, or secret access.
- `HER-REQ-CAP-003` — Tool proposals use controlled schemas and target fingerprints.
- `HER-REQ-CAP-004` — Unknown tool effects block blind retry.
- `HER-REQ-CAP-005` — Configured and actual model identities remain distinct.
- `HER-REQ-CAP-006` — Material fallback triggers re-evaluation.
- `HER-REQ-CAP-007` — Memory reads are scoped, filtered, and attributable.
- `HER-REQ-CAP-008` — Hermes memory proposals are not automatically authoritative.
- `HER-REQ-CAP-009` — Source deletion propagates to integrated Hermes memory where applicable.
- `HER-REQ-CAP-010` — Artifacts remain candidates until Agent OS validation and acceptance.
- `HER-REQ-CAP-011` — Partial or quarantined artifacts are not exportable by default.
- `HER-REQ-CAP-012` — Prompt content cannot change governance boundaries.

## 172. Requirement catalogue — Cost, audit, security, and operations

- `HER-REQ-OPS-001` — Usage completeness is explicit.
- `HER-REQ-OPS-002` — Unknown cost is not zero.
- `HER-REQ-OPS-003` — Budget and cost caps are enforced outside Hermes.
- `HER-REQ-OPS-004` — Hermes cannot modify budgets or approve spend.
- `HER-REQ-OPS-005` — Critical lifecycle and effects produce Agent OS audit evidence.
- `HER-REQ-OPS-006` — Raw secrets are excluded from adapter events and evidence.
- `HER-REQ-OPS-007` — Cross-workspace access receives negative testing.
- `HER-REQ-OPS-008` — Policy, approval, sandbox, and cost failures fail closed.
- `HER-REQ-OPS-009` — Runtime quarantine and revocation are operational.
- `HER-REQ-OPS-010` — Event gaps, delayed usage, and evidence failures are visible.
- `HER-REQ-OPS-011` — Critical adapter defects block pilot and release.
- `HER-REQ-OPS-012` — Agents or runtimes cannot self-certify conformance.

## 173. Traceability

| Source | ADP-HER-001 response |
|---|---|
| `AGC-001` | Adapter identity, lifecycle, commands, events, errors, and evidence |
| `CAP-001` | Capability manifest, validation, readiness, and drift |
| `MOD-001` | Model profiles, actual identity, fallback, limits, and provider evidence |
| `RUN-001` | Run/step/attempt mapping, retries, cancellation, and unknown effects |
| `APR-001` | Exact approvals, waiting, invalidation, and consumption |
| `ART-001` | Artifact candidate, validation, quarantine, acceptance, and export |
| `MEM-001` | Memory source, authority, scope, freshness, conflict, and deletion |
| `ORC-001` | Plans, dependencies, scheduling, delegation, and background work |
| `POL-001` | Enablement, permissions, obligations, emergency restrictions, and re-evaluation |
| `SAN-001` | Filesystem, network, secrets, process limits, Tool Gateway, and cleanup |
| `SEC-002` | Adapter, prompt-injection, secret, sandbox, cost, audit, and revocation controls |
| `DAT-002` | Prompt, session, memory, artifact, provider, retention, and deletion lifecycle |
| `AUD-001` | Actor chains, events, receipts, evidence packages, gaps, and recovery |
| `CST-001` | Usage, pricing, reservations, budgets, unknown cost, and reconciliation |
| `API-001` | Adapter resources and command direction |
| `EVT-001` | Event envelopes, ordering, replay, idempotency, and outbox |
| `OBS-001` | Health, metrics, alerts, freshness, and dashboards |
| `OPS-001` | Registration, incidents, upgrades, quarantine, and recovery runbooks |

## 174. ADR-TBD-HER-001 — Hermes transport, identity, and deployment modes

Select local IPC, service, remote transport, authentication, workload identity, process ownership, and trust boundaries.

## 175. ADR-TBD-HER-002 — Handshake, manifest, and capability protocol

Define protocol versions, schemas, manifest integrity, capability validation, readiness, drift, and compatibility.

## 176. ADR-TBD-HER-003 — Session, run, attempt, streaming, and resume mapping

Define one-session-per-run/step/attempt strategy, event ordering, replay, heartbeat, checkpoint, resume, and lost-session behavior.

## 177. ADR-TBD-HER-004 — Tool Gateway and MCP integration

Define tool proposal schema, MCP/server registration, policy, approvals, secrets, network, idempotency, receipts, and cancellation.

## 178. ADR-TBD-HER-005 — Model, prompt, and provider integration

Define model-profile mapping, actual identity, fallback, prompt construction, usage, provider errors, and data policy.

## 179. ADR-TBD-HER-006 — Memory and artifact integration

Define Agent OS versus Hermes memory, synchronization, proposals, verification, deletion, artifact candidates, previews, and acceptance.

## 180. ADR-TBD-HER-007 — Usage, cost, audit, and operational evidence

Define usage metrics, completeness, cost estimates, event/evidence schemas, gaps, retention, health, alerts, and reports.

## 181. ADR-TBD-HER-008 — Upgrade, quarantine, recovery, and commercial hardening

Define rolling upgrades, session migration, runtime quarantine, signed manifests, attestation direction, remote pools, and certification.

## 182. Open decisions

1. Confirm `ADP-HER-001` registration.
2. Identify the exact Hermes runtime/distribution initially supported.
3. Select local and future remote transport.
4. Define runtime and adapter workload identity.
5. Approve handshake and protocol versions.
6. Approve capability manifest schema.
7. Define capability validation and drift thresholds.
8. Choose run-to-session mapping for MVP.
9. Define streaming and replay semantics.
10. Define session checkpoint/resume support.
11. Define Tool Gateway proposal schema.
12. Decide MCP integration boundary.
13. Define model-profile and actual-model mapping.
14. Define prompt-governance injection model.
15. Define Agent OS versus Hermes memory boundary.
16. Define Hermes-local memory deletion.
17. Define artifact candidate handoff.
18. Define usage metrics and completeness.
19. Define cost estimation and unknown-cost policy.
20. Define cancellation and lost-session timeouts.
21. Define runtime quarantine and release authority.
22. Define upgrade/rollback compatibility testing.
23. Confirm accessibility and visual scenarios.
24. Define pilot runtime packaging and isolation.
25. Align with `ADP-CDX-001` for common adapter contracts.

## 183. Risks

| Risk | Consequence | Response |
|---|---|---|
| Hermes runtime treated as control plane | Governance bypass | Agent OS authority |
| Declared capability trusted blindly | Unsafe execution | Validation |
| Session reused across workspaces | Data leak | Scoped sessions |
| Hermes tool bypasses gateway | Unauthorized effect | Network/tool enforcement |
| MCP treated as authorization | Privilege escalation | Registered governed servers |
| Hidden model fallback | Cost/data-policy violation | Actual identity and re-evaluation |
| Hermes memory becomes authoritative | Poisoned decisions | Proposal/verification |
| Local host command execution | Host compromise | Sandbox or full runtime isolation |
| Background work hidden | Unbounded autonomy | Registered jobs/heartbeat |
| Child agents opaque | Unattributable activity | Delegation evidence |
| Cancellation shown complete too early | Duplicate/continued effects | Phased cancellation |
| Lost session retried blindly | Duplicate effect | Reconciliation |
| Usage unsupported shown zero | Budget bypass | Explicit unknown |
| Event gaps hidden | False timeline | Sequence/gap detection |
| Adapter version drift | Incompatible behavior | Compatibility matrix |
| Runtime upgrade breaks resume | Lost work/effects | Staging/rollback |
| Prompt changes governance | Policy bypass | Control-plane boundary |
| Secrets embedded in runtime context | Exposure | Brokered references |
| Agent self-certifies evidence | False assurance | Independent validation |
| Product overclaims Hermes autonomy | Trust/reputation harm | Explicit limitations |

## 184. Assumptions

- A Hermes-family runtime can expose at least one supported control interface.
- Agent OS can wrap or isolate the Hermes runtime where required.
- Protected tools can be routed through Tool Gateway.
- Model and usage metadata may vary by Hermes distribution.
- Some features such as resume, sub-agents, or memory synchronization may be unsupported initially.
- A local MVP can start with one validated runtime and limited capabilities.
- The adapter contract can preserve unsupported/unknown states rather than fabricating capability.
- Global document audit will reconcile common adapter vocabulary with `ADP-CDX-001`.

## 185. Constraints

- no Hermes approval authority;
- no Hermes IAM or policy authority;
- no unrestricted host, network, secret, or tool access;
- no cross-workspace session or memory reuse;
- no unvalidated capability use;
- no hidden model fallback;
- no unknown cost represented as zero;
- no unknown effect retried blindly;
- no partial output represented as accepted artifact;
- no runtime self-certification;
- no promise of perfect memory, lossless resume, or unbounded autonomy;
- no final transport or vendor-specific implementation selected in this draft;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## 186. Acceptance criteria

ADP-HER-001 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts Hermes user journeys, limitations, and autonomy boundaries;
3. Architecture accepts identity, handshake, capabilities, sessions, tools, models, memory, events, and recovery;
4. Security accepts Tool Gateway, sandbox, secrets, policy, approval, prompt-injection, isolation, and quarantine;
5. Data accepts prompts, memory, artifacts, provider data, retention, and deletion;
6. Operations accepts registration, health, metrics, alerts, upgrades, rollback, quarantine, and runbooks;
7. Quality accepts conformance, negative, cross-workspace, fault-injection, accessibility, visual, and compatibility tests;
8. initial Hermes runtime/distribution is identified;
9. transport and identity are approved;
10. manifest and capability protocol are approved;
11. session/run/attempt mapping is approved;
12. Tool Gateway and model integration are approved;
13. memory and artifact boundaries are approved;
14. usage, cost, cancellation, and evidence are approved;
15. pilot packaging and runtime isolation are approved.

## 187. Downstream impact

| Document | Required use |
|---|---|
| `ADP-CDX-001` | Reuse common adapter identity, lifecycle, events, errors, evidence, and conformance patterns |
| `SEC-002` | Add Hermes-specific implementation evidence for relevant security controls |
| `DAT-002` | Finalize Hermes session, prompt, memory, provider, and deletion treatment |
| `AUD-001` | Finalize Hermes event, actor-chain, receipt, and evidence schemas |
| `CST-001` | Finalize Hermes usage metrics, cost completeness, and reconciliation |
| `UXA-001` | Hermes runtime, capability, session, approval, cost, and recovery journeys |
| `DSN-001` | Hermes status, capability, event, fallback, quarantine, and evidence components |
| `A11Y-001` | Accessible Hermes administration and session controls |
| `VVR-001` | Hermes visual scenarios and regression baselines |
| Document register | Add proposed document and dependencies |

## 188. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial detailed Hermes adapter specification covering identity, handshake, capabilities, sessions, runs, streaming, tools, MCP direction, models, memory, artifacts, approvals, sandbox, usage, cost, cancellation, health, events, evidence, recovery, testing, and rollout |

## 189. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `AGC-001` — Agent Adapter Contract
- `CAP-001` — Agent Capability Schema
- `MOD-001` — Model Profile Contract
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `MEM-001` — Memory and Knowledge Architecture
- `ORC-001` — Workflow and Orchestration Architecture
- `POL-001` — Policy and Permission Architecture — proposed/unregistered
- `SAN-001` — Sandbox and Secure Execution Architecture — proposed/unregistered
- `SEC-002` — Security Control Catalogue — proposed/unregistered
- `DAT-002` — Data Classification, Retention and Deletion Standard — proposed/unregistered
- `AUD-001` — Audit and Evidence Architecture — proposed/unregistered
- `CST-001` — Usage, Cost and Budget Architecture — proposed/unregistered
