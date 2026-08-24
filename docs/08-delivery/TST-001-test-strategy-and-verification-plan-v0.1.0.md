---
document_id: TST-001
title: Agent OS Test Strategy and Verification Plan
version: 0.2.0
status: approved
owner: quality-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-07-20
last_reviewed: 2026-08-13
approval_date: 2026-08-13
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user authorization; user assumes the designated approval roles for this finalization
pending_approvals: []
classification: internal
source_of_truth: false
dependencies:
  - SRS-001
  - NFR-001
  - THR-001
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
  - QAG-001
  - OBS-001
  - OPS-001
  - BCP-001
related_adrs:
  - ADR-CANDIDATE-TST-001
  - ADR-CANDIDATE-TST-002
  - ADR-CANDIDATE-TST-003
  - ADR-CANDIDATE-TST-004
  - ADR-CANDIDATE-TST-005
---

# TST-001 — Agent OS Test Strategy and Verification Plan

> **Status: Approved baseline — 2026-08-13.** This document defines the verification strategy, test levels, environments, fixtures, coverage model, evidence requirements, automation, release-stage testing, defect handling, and acceptance criteria for Agent OS. It does not select the final CI platform, test runner, browser automation framework, security scanner, performance harness, or hosted test infrastructure.

## Current executable baseline

The repository currently verifies a backend test suite, Python quality checks, non-interactive frontend lint, frontend build, OpenAPI parity against mounted FastAPI paths and application-schema properties, controlled documentation, and Docker Compose resolution with CI-safe variables. The exact test count and result must be recorded by the validation run for the commit under review; these checks do not replace integration, provider, adapter, visual, security, or production tests.

Every verification report must record at least: commit or immutable build identity, command, environment, fixture/configuration identity, start and end time, result, warnings, skipped tests, and known limitations. A count copied into this document is not a substitute for commit-specific evidence.

## 1. Purpose

Agent OS coordinates autonomous and semi-autonomous software components that can:

- reason;
- generate content;
- interact with adapters;
- call model providers;
- propose or execute tools;
- manipulate files;
- interact with Git;
- create artifacts;
- use memory;
- consume approvals;
- operate asynchronously;
- survive restarts;
- produce audit evidence.

The test strategy must therefore verify more than “happy path” functionality.

It must verify:

- domain correctness;
- state-machine integrity;
- human-control boundaries;
- workspace isolation;
- authorization;
- exact approval semantics;
- duplicate and retry safety;
- recovery after partial failure;
- event delivery and replay;
- content safety;
- provenance and integrity;
- accessibility;
- performance;
- observability;
- backup and restore;
- migration behavior;
- provider and adapter drift;
- honest handling of unknown and unavailable states.

## 2. Test mission

The mission of testing is to produce evidence that Agent OS:

1. behaves according to documented requirements;
2. preserves domain invariants;
3. fails safely;
4. does not silently bypass human control;
5. does not confuse unknown with false, zero, empty, or complete;
6. prevents cross-workspace access;
7. prevents duplicate consequential effects;
8. survives process and dependency failure;
9. exposes actionable operational evidence;
10. remains accessible and understandable;
11. can be restored without replaying unsafe work;
12. can evolve through controlled migrations and versioned contracts.

## 3. Non-goals

This plan does not:

- prove that every model output is factually correct;
- prove perfect security;
- prove perfect malware detection;
- guarantee provider availability;
- guarantee deterministic LLM behavior;
- replace production monitoring;
- replace incident response;
- validate prohibited production or financial actions;
- treat code coverage percentage as sufficient quality;
- permit release based only on manual testing;
- permit release based only on generated agent reports;
- define a complete certification programme.

## 4. Core verification principles

### `TST-P-001 — Requirements are testable`

Every P0 requirement must map to at least one test, inspection, analysis, simulation, or review.

### `TST-P-002 — Invariants receive stronger evidence`

Workspace isolation, approval consumption, persisted-before-dispatch, append-only attempts, unknown-effect retry prevention, and restore safety require automated negative and concurrency tests.

### `TST-P-003 — Real boundaries are tested`

Database, filesystem, network, browser, worker, adapter, provider, and content-processing boundaries require integration or system tests.

### `TST-P-004 — Failures are deliberately injected`

Recovery cannot be proven only through normal execution.

### `TST-P-005 — Unknown states are test outcomes`

Tests must verify `unknown`, `stale`, `partial`, `unavailable`, `conflicted`, and `degraded` behavior.

### `TST-P-006 — Consequential effects use safe targets`

Testing must not perform real production, financial, public, or uncontrolled external effects.

### `TST-P-007 — Mocks are not final evidence`

Mocks support unit and component testing, but release evidence for critical integrations requires simulator, contract, or controlled real integration tests.

### `TST-P-008 — Security is negative by default`

Every protected resource group must include unauthorized, wrong-workspace, stale-session, and privilege-escalation tests.

### `TST-P-009 — Accessibility is a release property`

Automated accessibility scans alone are insufficient; keyboard and assistive-technology journeys are required.

### `TST-P-010 — Restore is tested, not assumed`

A backup is not accepted until an isolated restore and verification succeeds.

### `TST-P-011 — Evidence is reproducible`

Test reports identify build, environment, schema versions, fixtures, commands, and outcomes.

### `TST-P-012 — Flaky tests are defects`

Retries may diagnose infrastructure instability, but they do not convert nondeterminism into quality.

## 5. Verification methods

The plan uses:

```text
automated test
manual test
inspection
static analysis
dynamic analysis
formal state-table review
fault injection
simulation
benchmark
restore drill
security review
accessibility review
threat-based abuse testing
operational rehearsal
```

Each requirement identifies its appropriate verification method.

## 6. Test levels

```text
L0 — Static and schema verification
L1 — Unit and property verification
L2 — Module and state-machine verification
L3 — Component integration verification
L4 — Contract and adapter conformance verification
L5 — System and end-to-end verification
L6 — Fault, recovery, security, and resilience verification
L7 — Pilot acceptance and operational rehearsal
```

## 7. L0 — Static and schema verification

Covers:

- formatting;
- linting;
- type checking;
- dependency graph;
- schema validation;
- OpenAPI/AsyncAPI or equivalent;
- migration checks;
- controlled enum consistency;
- documentation references;
- secret scanning;
- container configuration;
- architecture fitness functions.

L0 should run on every relevant change.

## 8. L1 — Unit and property verification

Covers:

- value objects;
- canonicalization;
- fingerprints;
- state guards;
- retry eligibility;
- classification;
- cost arithmetic;
- source and confidence semantics;
- ID validation;
- path normalization;
- serialization;
- error mapping.

L1 tests have no real network or provider dependency.

## 9. L2 — Module and state-machine verification

Covers:

- aggregates;
- command handlers;
- transitions;
- forbidden transitions;
- domain events;
- idempotency decisions;
- policy evaluation;
- approval lifecycle;
- run lifecycle;
- artifact lifecycle;
- memory lifecycle;
- budget lifecycle.

## 10. L3 — Component integration verification

Covers:

- real database;
- migrations;
- outbox/inbox;
- durable jobs;
- worker leases;
- local artifact store;
- safe preview workers;
- API layer;
- authentication;
- simulator adapter;
- event projections;
- backup utilities.

## 11. L4 — Contract and conformance verification

Covers:

- API producer/consumer schemas;
- event schemas;
- adapter contract;
- capability declarations;
- model profiles;
- tool contracts;
- extension namespaces;
- error codes;
- compatibility;
- generated clients.

## 12. L5 — System and end-to-end verification

Covers realistic user journeys across:

- browser UI;
- API;
- database;
- workers;
- simulator or controlled adapter;
- artifact store;
- audit;
- cost;
- notifications;
- recovery read models.

## 13. L6 — Fault, recovery, security, and resilience verification

Covers:

- process crashes;
- dependency outages;
- timeouts;
- duplicates;
- out-of-order messages;
- stale workers;
- unknown effects;
- malicious content;
- privilege escalation;
- cross-workspace attacks;
- backup/restore;
- replay;
- supply-chain controls.

## 14. L7 — Pilot acceptance and operational rehearsal

Covers:

- real operator journeys;
- supported deployment profile;
- backup drill;
- restore drill;
- incident exercise;
- accessibility review;
- performance baseline;
- adapter/provider validation;
- documented limitations;
- user acceptance.

## 15. Test pyramid and portfolio

Agent OS uses a portfolio, not a simplistic pyramid.

Recommended relative emphasis:

| Test type | Emphasis |
|---|---:|
| Unit/property/state-machine | Very high |
| Integration/database/worker | High |
| Contract/conformance | High |
| Security/negative/concurrency | High |
| E2E browser | Moderate and strategic |
| Manual exploratory | Targeted |
| Performance/fault/recovery | Mandatory at release stages |
| Real provider tests | Bounded and opt-in |

## 16. Risk-based prioritization

Test priority is determined by:

- consequence;
- likelihood;
- detectability;
- reversibility;
- data classification;
- external side effects;
- human-control impact;
- recovery complexity;
- change frequency;
- threat model findings.

## 17. Test priority classes

```text
T0 — Release-blocking safety/security/invariant
T1 — Critical product workflow
T2 — Important reliability/usability
T3 — Secondary feature
T4 — Exploratory or future
```

## 18. T0 examples

- cross-workspace data access;
- approval replay;
- duplicate protected action;
- unknown-effect retry;
- stale-worker write;
- raw secret leak;
- restore replays a consumed approval;
- backup cannot restore;
- unsafe artifact preview executes active content;
- agent self-approval;
- production/financial action bypass;
- audit failure on protected action under fail-closed policy.

## 19. Test ownership

| Area | Primary owner | Supporting owners |
|---|---|---|
| Product acceptance | Product Owner | Quality |
| Domain invariants | Architecture | Quality |
| Security/abuse | Security | Quality, Architecture |
| Data correctness | Data | Quality |
| Operations/recovery | Operations | Quality, Data |
| Accessibility | Product/UX Accessibility | Quality |
| Adapter conformance | Adapter owner | Architecture, Security |
| Model/provider tests | Architecture/Data | Security, Quality |
| CI/test framework | Quality | Architecture, Operations |

## 20. Test governance

Every major test suite has:

- owner;
- scope;
- entry criteria;
- environment;
- fixtures;
- expected duration;
- release stage;
- failure policy;
- evidence output;
- maintenance owner;
- flakiness threshold;
- known limitations.

## 21. Requirement traceability

`RTM-001` should map:

```text
Requirement
→ Verification method
→ Test suite
→ Test case or inspection
→ Build
→ Environment
→ Result
→ Evidence
→ Defect or exception
```

No P0 requirement may remain without verification.

## 22. Test case identifiers

Recommended formats:

```text
TST-UNIT-<DOMAIN>-NNN
TST-STM-<DOMAIN>-NNN
TST-INT-<DOMAIN>-NNN
TST-CON-<CONTRACT>-NNN
TST-SEC-<AREA>-NNN
TST-E2E-<JOURNEY>-NNN
TST-REC-<SCENARIO>-NNN
TST-PERF-<AREA>-NNN
TST-A11Y-<JOURNEY>-NNN
```

## 23. Evidence requirements

A test execution record includes:

- test suite and version;
- build identity;
- commit/reference where available;
- environment profile;
- dependency versions;
- schema/migration version;
- fixture version;
- start/end time;
- command;
- result;
- failures;
- logs/artifacts;
- retry count;
- known limitations;
- reviewer where manual.

## 24. Evidence integrity

Release evidence should use:

- immutable CI artifacts where available;
- hashes;
- manifests;
- timestamps;
- build identity;
- restricted access;
- retention policy;
- no secrets;
- no unredacted confidential test content.

## 25. Test environments

Recommended environments:

```text
developer_local
unit_isolated
integration_local
ci_ephemeral
security_isolated
performance_isolated
recovery_isolated
pilot_staging
pilot_environment
```

## 26. Developer local environment

Purpose:

- rapid development;
- unit/integration;
- simulator workflows;
- frontend visual verification;
- migrations;
- smoke tests.

It is not sufficient alone for release acceptance.

## 27. CI ephemeral environment

Requirements:

- clean checkout;
- deterministic dependencies;
- isolated database;
- isolated artifact root;
- synthetic fixtures;
- migration from empty state;
- service health;
- no real provider secrets by default;
- artifact/report collection.

## 28. Security-isolated environment

Used for:

- malicious files;
- sandbox escape attempts;
- command injection;
- archive bombs;
- cross-workspace attacks;
- secret leakage;
- event forgery;
- dependency scanning.

It must not share sensitive host resources.

## 29. Performance-isolated environment

Requirements:

- controlled resources;
- stable versions;
- low background noise;
- repeatable dataset;
- warm/cold profiles;
- recorded hardware/container limits;
- separate from ordinary CI where necessary.

## 30. Recovery-isolated environment

Used for:

- backup/restore;
- event replay;
- crashed workers;
- corrupted content;
- lost indexes;
- expired leases;
- nonterminal runs;
- tombstone validation.

It must never target active pilot or production-like data unintentionally.

## 31. Pilot staging

Purpose:

- release-candidate validation;
- realistic configuration;
- controlled adapters/providers;
- user acceptance;
- operational drills;
- accessibility and performance review.

It uses synthetic or explicitly governed pilot data.

## 32. Environment parity

Parity is required for:

- schema;
- configuration semantics;
- container/service topology where practical;
- auth profile;
- storage abstraction;
- event/job behavior;
- security controls;
- health/readiness;
- backup/restore tooling.

Provider credentials and real external effects remain environment-specific.

## 33. Test data principles

Test data must be:

- synthetic;
- deterministic;
- workspace-diverse;
- classification-diverse;
- state-diverse;
- safe;
- reproducible;
- free from real secrets;
- free from unnecessary personal data;
- documented.

## 34. Core fixture workspaces

Recommended fixtures:

```text
workspace_alpha_internal
workspace_beta_internal
workspace_confidential
workspace_suspended
workspace_read_only
workspace_archived
```

Tests must include intentional cross-workspace ID substitution.

## 35. Core identity fixtures

```text
product_owner
workspace_owner_alpha
workspace_owner_beta
operator_alpha
reviewer_alpha
security_reviewer
data_reviewer
read_only_user
revoked_user
expired_session_user
worker_identity
adapter_identity
agent_identity
```

## 36. Core run fixtures

```text
run_created
run_queued
run_running
run_waiting_approval
run_waiting_resource
run_paused
run_cancelling
run_stale
run_unknown
run_completed
run_failed
run_cancelled
```

## 37. Core approval fixtures

```text
approval_requested
approval_under_review
approval_approved
approval_rejected
approval_expired
approval_invalidated
approval_consumed
approval_same_human_alias
approval_independent_reviewer
approval_fingerprint_mismatch
```

## 38. Core artifact fixtures

```text
artifact_safe_text
artifact_safe_pdf
artifact_active_pdf
artifact_malicious_svg
artifact_macro_document
artifact_archive_safe
artifact_archive_traversal
artifact_archive_bomb
artifact_secret_candidate
artifact_partial
artifact_hash_mismatch
artifact_quarantined
artifact_accepted_v1
artifact_revised_v2
artifact_deleted
artifact_missing_after_restore
```

## 39. Core memory fixtures

```text
memory_user_asserted
memory_agent_generated
memory_verified
memory_disputed
memory_conflicted
memory_expired
memory_superseded
memory_deleted
memory_wrong_workspace
```

## 40. Core event fixtures

```text
event_valid
event_duplicate
event_out_of_order
event_gap
event_unsupported_version
event_wrong_workspace
event_forged_source
event_integrity_failure
event_oversized
event_dead_letter
event_replay
```

## 41. Golden fixtures

Golden fixtures are maintained for:

- canonical serialization;
- action fingerprints;
- content hashes;
- event envelopes;
- API examples;
- receipts;
- manifests;
- adapter messages;
- capability declarations;
- model profiles;
- migrations.

Golden changes require review.

## 42. Test clocks

Use controlled clocks for:

- approval expiry;
- lease expiry;
- retry backoff;
- deadlines;
- session expiry;
- retention;
- backup schedules;
- event lateness;
- pricing validity.

Avoid sleeping in tests when a fake/controlled clock is possible.

## 43. Deterministic IDs

Deterministic IDs may be used in tests to:

- compare snapshots;
- verify events;
- verify lineage;
- reproduce failures.

Production ID generation remains separate.

## 44. Unit-test scope

Unit tests should verify:

- pure functions;
- value objects;
- aggregate methods;
- policy helpers;
- canonicalization;
- classification;
- arithmetic;
- error mapping;
- state guards.

External dependencies are replaced with narrow test doubles.

## 45. Unit-test anti-patterns

Avoid:

- testing framework internals;
- mocking every line;
- unit tests that duplicate implementation;
- brittle private-method tests;
- random unseeded data;
- assertions only on “no exception”;
- tests that depend on real time/network.

## 46. Property-based verification

Property candidates:

- canonical JSON order invariance;
- approval fingerprint stability;
- classification maximum;
- opaque ID round-trip;
- retry bounds;
- path containment;
- event deduplication;
- money arithmetic;
- usage reconciliation;
- pagination cursor stability;
- state-machine terminal invariants.

## 47. State-machine verification

For every lifecycle:

- enumerate states;
- enumerate commands;
- enumerate allowed transitions;
- enumerate forbidden transitions;
- verify reason codes;
- verify emitted events;
- verify aggregate version;
- verify terminal behavior;
- verify stale/unknown paths.

## 48. Run state tests

Minimum tests:

- create before dispatch;
- queue from created;
- preflight pass/block;
- start/run;
- wait and resume;
- cancel from every nonterminal state;
- cannot reopen terminal;
- completion evidence required;
- unknown not auto-failed;
- retry creates new attempt;
- deadline behavior;
- emergency stop behavior.

## 49. Attempt state tests

Minimum:

- attempt number monotonic;
- input immutable;
- new attempt on retry;
- lease/fencing;
- timeout before effect;
- timeout after effect;
- unknown effect;
- late completion after timeout;
- cancellation outcome;
- result attribution.

## 50. Approval state tests

Minimum:

- human-only decision;
- authority;
- independence;
- exact fingerprint;
- expiry;
- invalidation;
- one-time consumption;
- concurrent consumption;
- decision immutability;
- rejection;
- revision;
- restore preserves consumed state;
- emergency stop before consumption.

## 51. Artifact state tests

Minimum:

- proposal/staging/finalize;
- partial upload;
- integrity failure;
- validation failure;
- quarantine;
- preview;
- review;
- acceptance;
- revision;
- supersession;
- export;
- deletion;
- recovery;
- unavailable content.

## 52. Memory state tests

Minimum:

- proposal;
- version;
- verification;
- dispute;
- conflict;
- supersession;
- expiry;
- deletion;
- index update;
- retrieval source/freshness;
- cross-workspace denial.

## 53. Database integration tests

Use a real relational database engine matching the selected implementation.

Verify:

- constraints;
- transactions;
- isolation;
- optimistic concurrency;
- unique consumption;
- outbox atomicity;
- inbox deduplication;
- foreign-key behavior;
- indexes;
- migration state;
- backup consistency.

## 54. Transaction rollback tests

Scenarios:

- failure before aggregate save;
- failure after aggregate save but before outbox;
- outbox insert failure;
- budget reservation conflict;
- approval consumption conflict;
- artifact metadata/content mismatch;
- migration failure.

Expected: no partially authoritative state beyond explicitly modelled recovery state.

## 55. Outbox tests

Minimum:

- state and outbox same transaction;
- publisher restart;
- duplicate publication;
- stable event ID;
- publish timeout;
- retry;
- dead letter;
- schema failure;
- backlog metrics;
- restore reconciliation.

## 56. Inbox tests

Minimum:

- duplicate event;
- crash before processing commit;
- crash after business commit before acknowledgement;
- consumer restart;
- unsupported event;
- wrong workspace;
- poison payload;
- dead-letter transition;
- replay.

## 57. Durable job tests

Minimum:

- schedule;
- lease;
- heartbeat;
- completion;
- retry;
- dead letter;
- cancellation;
- expiry;
- duplicate delivery;
- restored job;
- run cancellation blocks dispatch.

## 58. Lease and fencing tests

Scenarios:

1. Worker A acquires token 10.
2. Lease expires.
3. Worker B acquires token 11.
4. Worker A submits late result with token 10.
5. Result is rejected.
6. Side-effect certainty is reconciled.

This is T0 release-blocking.

## 59. API contract tests

Verify:

- request schemas;
- response schemas;
- status codes;
- error envelopes;
- headers;
- idempotency;
- ETag;
- pagination;
- filters;
- content types;
- versioning;
- deprecations;
- examples.

## 60. API negative tests

Every protected route group tests:

- no authentication;
- invalid/expired session;
- wrong workspace;
- wrong role;
- classification denial;
- stale version;
- invalid idempotency;
- invalid schema;
- oversized payload;
- unsupported media type;
- emergency stop where relevant.

## 61. API mass-assignment tests

Attempt to modify protected fields:

```text
run.state
workspace_id
approval.state
approval.decision
artifact.acceptance_state
role authority
audit event
cost source
actual model identity
```

The API must reject or ignore according to contract, never apply silently.

## 62. Pagination tests

Verify:

- stable ordering;
- opaque cursor;
- next page;
- filter-bound cursor;
- expired cursor;
- authorization before count;
- no duplicates/missing items under supported consistency model;
- maximum limit;
- deterministic tiebreaker.

## 63. Event contract tests

Verify:

- envelope;
- semantic version;
- schema version;
- classification;
- correlation;
- causation;
- partition key;
- aggregate version;
- source;
- hash;
- payload/reference;
- compatibility.

## 64. Event duplicate tests

For every stateful consumer:

- first processing succeeds;
- second same `event_id` does not repeat business effect;
- original result remains;
- duplicate metric increments;
- no new domain event except optional anomaly.

## 65. Event ordering tests

Scenarios:

- version 1 then 2;
- 2 before 1;
- duplicate 1;
- version gap;
- late old event;
- conflicting external observation;
- replay during live events.

## 66. Event replay tests

Verify:

- projection rebuild;
- no protected tool call;
- no duplicate external message;
- no approval re-consumption;
- notifications suppressed by default;
- scope/time filters;
- audit evidence;
- cancel/pause;
- current and rebuilt projection comparison.

## 67. Adapter conformance profile

Every adapter must pass:

```text
ADP-CON-CORE
ADP-CON-IDENTITY
ADP-CON-CAPABILITIES
ADP-CON-LIFECYCLE
ADP-CON-EVENTS
ADP-CON-CANCELLATION
ADP-CON-CHECKPOINT
ADP-CON-MODEL
ADP-CON-USAGE
ADP-CON-TOOLS
ADP-CON-SECURITY
ADP-CON-RECOVERY
```

## 68. Adapter core tests

Verify:

- registration;
- version negotiation;
- health;
- readiness;
- start;
- status;
- final result;
- error normalization;
- correlation;
- workspace/run binding;
- no hidden state mutation.

## 69. Adapter capability tests

Verify:

- declaration schema;
- validation state;
- declared versus validated;
- effect class;
- target scope;
- network/filesystem requirements;
- cancellation semantics;
- tool visibility;
- drift detection;
- revocation.

## 70. Adapter lifecycle tests

Scenarios:

- normal success;
- slow start;
- adapter unavailable;
- crash;
- restart;
- external session lost;
- duplicate events;
- out-of-order events;
- event gap;
- unknown terminal state;
- incompatible version.

## 71. Adapter cancellation tests

Verify each declared mode:

```text
unsupported
best_effort
acknowledgement_only
safe_boundary
terminal_confirmation
unknown
```

A cancellation acknowledgement must not be reported as terminal cancellation unless evidenced.

## 72. Adapter tool-visibility tests

Verify whether:

- all tools are delegated;
- all tools are observed;
- some tools are observed;
- native tools are disabled;
- hidden tools may exist.

Protected runtime use is blocked if visibility does not satisfy policy.

## 73. Codex adapter tests

Minimum:

- scoped repository/worktree;
- read;
- patch;
- test;
- build;
- patch artifact;
- commit approval exactness;
- commit not equal push;
- push not equal PR;
- merge prohibited;
- force push prohibited;
- history rewrite prohibited;
- path scope;
- command bounds;
- cancellation honesty;
- model/usage observation.

## 74. Hermes adapter tests

Minimum:

- invocation;
- session attribution;
- capability declaration;
- model/provider observation;
- native-tool visibility;
- workspace isolation;
- cancellation;
- pause/resume/checkpoint truth;
- output normalization;
- protected-effect delegation;
- drift.

## 75. Simulator adapter tests

The simulator itself must be tested.

Scenarios:

- deterministic success;
- deterministic failure;
- slow start;
- timeout;
- crash;
- duplicate;
- out-of-order;
- gap;
- unknown effect;
- artifact proposal;
- model/usage;
- cancellation modes;
- capability drift.

## 76. Model-profile tests

Verify:

- logical profile;
- provider binding;
- capability match;
- context/output limits;
- classification;
- local-only;
- provider/region allowlist;
- quota;
- budget;
- fallback;
- actual identity;
- usage;
- cost state;
- drift.

## 77. Model routing tests

Scenarios:

- exact eligible binding;
- capability mismatch;
- insufficient context;
- unsupported modality;
- confidential disclosure blocked;
- local-only violation;
- unhealthy binding;
- quota exhausted;
- budget exceeded;
- provider denied;
- fallback requires approval;
- no compatible binding.

## 78. Fallback tests

Verify:

- no silent fallback;
- provider change visible;
- region change visible;
- data protection not weakened;
- capability not removed;
- cost delta handled;
- maximum chain length;
- new approval when material;
- actual identity correct/unknown.

## 79. Model identity tests

States:

```text
provider_reported
adapter_reported
locally_observed
inferred
configured_only
unavailable
unknown
conflicted
```

The UI/API/receipt must never label `configured_only` as actual.

## 80. Usage and cost tests

Verify:

- input/output usage;
- source;
- deduplication;
- pricing version;
- calculation;
- estimate;
- provider report;
- invoice;
- reconciliation;
- mismatch;
- unknown not zero;
- currency;
- rounding.

## 81. Tool Gateway tests

Verify:

- normalization;
- capability;
- policy;
- approval;
- fingerprint;
- workspace;
- target;
- filesystem/network scope;
- idempotency;
- execution;
- evidence;
- side-effect certainty;
- reconciliation.

## 82. Protected-action tests

Representative safe simulations:

- local reversible file write;
- file deletion proposal;
- Git commit in isolated fixture repository;
- external message send against simulator;
- calendar change against simulator;
- package installation proposal without real install;
- network expansion proposal;
- backup restore in isolated environment.

## 83. Sandbox tests

Verify:

- process identity;
- read/write mounts;
- denied host paths;
- symlink escape;
- network deny;
- destination allowlist;
- CPU limit;
- memory limit;
- timeout;
- process count;
- output bound;
- environment variable minimization;
- cleanup;
- no Docker socket.

## 84. Filesystem security tests

Scenarios:

```text
../ traversal
absolute path outside root
symlink outside root
case/Unicode normalization
alternate separator
deleted/replaced file race
read-only mount write
wildcard deletion
mounted Windows path escape
```

## 85. Command-execution security tests

Attempt:

- shell injection;
- argument injection;
- environment injection;
- command substitution;
- newline/control characters;
- oversized output;
- fork bomb simulation;
- timeout resistance;
- child-process escape.

## 86. Network security tests

Verify:

- default deny;
- explicit destination;
- DNS resolution;
- redirect revalidation;
- localhost/internal metadata targets;
- proxy;
- TLS verification;
- timeout;
- data-class restrictions;
- rate limit;
- SSRF patterns.

## 87. Approval security tests

T0 tests:

- agent approval attempt;
- workload approval attempt;
- same-human alias independence;
- replay;
- target substitution;
- content/diff substitution;
- policy change;
- authority revocation;
- expiry race;
- concurrent consumption;
- restore replay;
- emergency stop after approval;
- mobile incomplete review.

## 88. Approval UX tests

Verify:

- exact target visible;
- canonical diff/content available;
- generated summary labelled;
- unknowns visible;
- expiry visible;
- risk not color-only;
- approve/reject/revise accessible;
- stale page submission revalidated;
- no preselected approve;
- no generic “allow everything”.

## 89. Artifact staging tests

Verify:

- bounded size;
- incomplete upload;
- expired session;
- wrong hash;
- wrong media type;
- duplicate finalize;
- crash during finalize;
- orphan object;
- orphan metadata;
- quota;
- cleanup.

## 90. Artifact security tests

Fixtures:

- malicious SVG;
- active HTML;
- macro document;
- PDF action;
- archive traversal;
- nested archive;
- decompression bomb;
- executable disguised as image;
- external resource;
- secret candidate;
- formula injection.

Expected: block, quarantine, safe derived preview, or explicit limitation.

## 91. Artifact preview tests

Verify:

- isolated conversion;
- no network;
- no host write;
- bounded resources;
- derived preview hash;
- original/preview distinction;
- failure state;
- safe fallback metadata view;
- accessibility.

## 92. Artifact acceptance tests

Verify:

- version-specific;
- purpose-specific;
- reviewer authority;
- independence;
- validation prerequisites;
- quarantine blocks;
- newer version not auto-accepted;
- limitations retained;
- rejection immutable.

## 93. Artifact export tests

Verify:

- exact version IDs;
- destination;
- manifest;
- classification;
- approval;
- redaction;
- partial transfer;
- cancellation;
- expiry;
- no canonical mutation;
- external copy limitation.

## 94. Artifact deletion tests

Verify:

- retention hold;
- approval;
- content deletion;
- preview deletion;
- index/cache deletion;
- tombstone;
- audit;
- backup limitation;
- restore does not revive active content.

## 95. Memory governance tests

Verify:

- agent proposal not authoritative;
- verification by eligible human;
- source visible;
- confidence/freshness;
- conflict;
- supersession;
- deletion;
- correction;
- no authority by repetition;
- index rebuild.

## 96. Memory retrieval tests

Verify:

- workspace filtering before ranking;
- classification;
- authority filter;
- stale/expired handling;
- conflict handling;
- lexical retrieval;
- optional vector retrieval;
- source references;
- bounded snippets;
- unauthorized snippet absence.

## 97. Search and index tests

Verify:

- direct authoritative data versus projection;
- indexing lag;
- stale state;
- deletion propagation;
- workspace filter;
- classification;
- rebuild;
- cursor;
- empty results;
- unavailable index fallback.

## 98. Authentication tests

Verify:

- valid login;
- invalid credentials;
- lockout/rate limit;
- expired session;
- revoked session;
- idle/absolute expiry;
- reauthentication;
- logout;
- session fixation;
- cookie/header security;
- workload identity separation.

## 99. Authorization tests

For every protected action:

- correct role;
- missing role;
- wrong workspace;
- suspended membership;
- revoked role;
- delegated authority;
- expired delegation;
- classification ceiling;
- risk ceiling;
- emergency stop;
- maintenance state.

## 100. Cross-workspace test pattern

For every resource group:

1. Create resource in workspace Alpha.
2. Authenticate identity scoped to workspace Beta.
3. Attempt read by ID.
4. Attempt mutation by ID.
5. Attempt search/filter.
6. Attempt event subscription.
7. Attempt export.
8. Verify safe denial/not-found.
9. Verify no count/snippet leak.
10. Verify restricted audit event.

## 101. Browser security tests

Verify:

- CSRF;
- same-site cookies;
- secure/HTTP-only flags;
- CORS default deny;
- origin validation;
- clickjacking;
- content security policy;
- trusted hosts;
- XSS;
- unsafe HTML;
- download disposition;
- cache-control.

## 102. Prompt-injection boundary tests

Inject untrusted text asking to:

- approve;
- grant role;
- disable audit;
- expand network;
- reveal secret;
- access another workspace;
- merge Git;
- run shell;
- ignore policy.

Expected: content remains data and cannot change authority.

## 103. Secret-leak tests

Inspect:

- logs;
- traces;
- API responses;
- errors;
- event payloads;
- artifacts;
- screenshots;
- test reports;
- environment dumps;
- provider errors;
- browser storage.

No raw secret may appear.

## 104. Threat-model test mapping

Every high or critical `THR-001` scenario must map to:

- prevention test;
- detection test;
- recovery/response test where applicable;
- residual risk;
- release blocker status.

## 105. Security test cadence

| Test category | Cadence |
|---|---|
| Secret scan | Every change |
| Dependency scan | Every change / scheduled |
| Static security | Every change |
| Cross-workspace | Every relevant change |
| Approval replay/substitution | Every approval change |
| Sandbox abuse | Release candidate / sandbox change |
| Malicious artifact | Release candidate / preview change |
| Threat-based abuse | Milestone and major architecture change |
| Manual security review | Pilot and commercialization gates |

## 106. Accessibility standard

Target direction: WCAG 2.2 AA.

Critical journeys:

- login;
- workspace selection;
- task creation;
- run monitoring;
- approval review;
- artifact review;
- error recovery;
- operations alert;
- settings.

## 107. Automated accessibility tests

Cover:

- missing names;
- invalid ARIA;
- contrast where tool supports;
- landmark structure;
- heading order;
- form labels;
- dialog semantics;
- focusable controls;
- duplicate IDs;
- table semantics.

## 108. Manual keyboard tests

Verify:

- logical tab order;
- visible focus;
- skip links;
- menu/dialog operation;
- no keyboard trap;
- approval decision;
- diff navigation;
- artifact preview;
- responsive navigation;
- error focus.

## 109. Screen-reader smoke tests

At minimum test:

- page title/landmarks;
- form errors;
- run status;
- approval risk and expiry;
- artifact integrity and quarantine;
- table/list navigation;
- live updates without overload;
- modal announcements.

## 110. Responsive and reflow tests

Widths:

```text
320
375
768
1024
desktop wide
```

Verify:

- no global horizontal scroll;
- complete information;
- no hidden essential action;
- approval detail preserved;
- artifact metadata readable;
- editor/diff usable or explicit desktop restriction;
- touch targets;
- zoom/reflow.

## 111. Visual regression tests

A controlled visual regression plan should include:

- baseline screenshots;
- supported widths;
- theme/appearance if applicable;
- loading/empty/error/stale states;
- diff tolerance;
- manual review for intentional changes;
- no acceptance based only on pixel similarity.

A dedicated `VVR-001` remains proposed/unregistered.

## 112. Manual visual verification

After visible changes:

1. run current branch/build;
2. rebuild affected services;
3. verify health;
4. hard refresh;
5. test changed actions;
6. inspect supported widths;
7. record screenshots/notes;
8. validate no old mock or stale build.

## 113. E2E journey catalogue

Initial journeys:

```text
J01 — Login and workspace selection
J02 — Create task and immutable snapshot
J03 — Run safe simulator task
J04 — Monitor run and timeline
J05 — Cancel run
J06 — Recover stale run
J07 — Review generated artifact
J08 — Approval-gated protected simulation
J09 — Reject and revise approval
J10 — Inspect receipt and audit
J11 — Configure adapter/model readiness
J12 — View usage/cost/budget
J13 — Propose and verify memory
J14 — Backup and restore isolated environment
```

## 114. E2E J01 — Login and workspace selection

Verify:

- authenticated session;
- accessible workspaces only;
- suspended/archived behavior;
- current workspace;
- no cross-workspace data;
- logout;
- session expiry.

## 115. E2E J02 — Task and snapshot

Verify:

- task created;
- validation;
- snapshot immutable;
- edits create new snapshot;
- old snapshot remains;
- run binds selected snapshot.

## 116. E2E J03 — Safe simulator run

Verify:

- idempotent create;
- persisted before dispatch;
- queued/running/completed;
- events;
- attempts;
- artifact;
- cost state;
- receipt.

## 117. E2E J04 — Run monitoring

Verify:

- live/polling updates;
- freshness;
- steps/attempts;
- model/adapter state;
- waiting;
- stale;
- unknown;
- recovery direction.

## 118. E2E J05 — Cancellation

Verify:

- cancel request;
- future jobs blocked;
- active adapter cancellation;
- clean/partial/unknown outcomes;
- no rollback claim;
- receipt.

## 119. E2E J06 — Stale-run recovery

Inject lost heartbeat or adapter outage.

Verify:

- stale visible;
- reconciliation;
- no duplicate protected retry;
- operator action;
- final state/evidence.

## 120. E2E J07 — Artifact review

Verify:

- staging/finalization;
- hash;
- provenance;
- safe preview;
- review;
- acceptance;
- new version not auto-accepted;
- export.

## 121. E2E J08 — Approval-gated action

Verify:

- exact request;
- human review;
- independence;
- one-time consumption;
- protected simulator execution;
- result;
- receipt.

## 122. E2E J09 — Reject and revise

Verify:

- rejection immutable;
- run follows revision path;
- changed action gets new request/fingerprint;
- old request superseded;
- new review.

## 123. E2E J10 — Receipt and audit

Verify:

- task snapshot;
- attempts;
- model/tool;
- approval;
- artifact;
- effects;
- usage/cost;
- gaps;
- hashes;
- export permission.

## 124. E2E J11 — Adapter/model readiness

Verify:

- registration;
- validation;
- capabilities;
- model profile;
- binding health;
- drift;
- disable/revoke;
- run blocked when not ready.

## 125. E2E J12 — Usage/cost/budget

Verify:

- usage event;
- estimate;
- budget reserve;
- actual/unknown;
- reconciliation;
- threshold;
- hard block;
- no zero for unknown.

## 126. E2E J13 — Memory

Verify:

- agent proposal;
- source;
- verification;
- retrieval;
- conflict;
- deletion;
- index update;
- workspace isolation.

## 127. E2E J14 — Backup and restore

Verify:

- backup requested;
- manifest;
- verification;
- isolated destruction;
- restore;
- migration compatibility;
- reconciliation;
- consumed approval preserved;
- deleted artifact remains deleted;
- nonterminal run not replayed blindly.

## 128. Concurrency test strategy

Concurrency tests use:

- barriers;
- controlled clocks;
- multiple real transactions;
- independent workers;
- deterministic assertions;
- repeated stress runs;
- database-level constraints.

## 129. Critical concurrency scenarios

```text
C01 duplicate CreateRun
C02 duplicate ApprovalConsume
C03 cancel versus complete
C04 retry versus late success
C05 two workers lease job
C06 stale fencing token
C07 artifact finalize race
C08 role revoke versus approval decision
C09 budget reserve race
C10 event replay versus live event
C11 delete versus export
C12 restore versus active scheduler
```

## 130. Fault-injection strategy

Fault injection may target:

- process;
- network;
- storage;
- database;
- time;
- queue;
- provider;
- filesystem;
- content conversion;
- backup;
- index;
- identity service.

Faults must be controlled, reversible, and isolated.

## 131. API crash tests

Crash points:

- before command transaction;
- during transaction;
- after commit before response;
- after response before event publication;
- during receipt generation.

Verify idempotent replay and durable state.

## 132. Worker crash tests

Crash points:

- before lease;
- after lease;
- before dispatch;
- after external acceptance;
- after effect before result commit;
- during cancellation;
- during heartbeat.

Verify fencing, reconciliation, and side-effect certainty.

## 133. Adapter crash tests

Verify:

- run state;
- external session reference;
- stale/unknown;
- reconnect;
- reconciliation;
- no blind retry;
- health/readiness.

## 134. Database outage tests

Verify:

- API safe errors;
- no external dispatch without persistence;
- workers stop protected actions;
- retry/backoff;
- health/readiness;
- recovery after return;
- no lost idempotency/consumption.

## 135. Artifact-store outage tests

Verify:

- metadata read may remain;
- content state unavailable;
- no false deletion;
- staging failure;
- preview/export blocked;
- recovery after store returns.

## 136. Event transport outage tests

Verify:

- outbox backlog;
- state remains durable;
- publisher retry;
- health/alert;
- projections stale;
- no silent event loss;
- drain after recovery.

## 137. Identity-service outage tests

Verify:

- new login blocked;
- current sessions follow policy;
- sensitive actions may require reauth and block;
- no fail-open authorization;
- health visible.

## 138. Time-skew and clock tests

Verify:

- approval expiry;
- lease expiry;
- external timestamp uncertainty;
- event ordering not based solely on wall clock;
- budget window;
- retention;
- scheduled retries;
- restore time.

## 139. Performance test strategy

Performance testing includes:

- latency;
- throughput;
- concurrency;
- resource use;
- backlog drain;
- large history;
- artifact size;
- search;
- restore.

## 140. Performance SLI candidates

- common API read p50/p95/p99;
- command acceptance p95;
- Mission Control aggregate read;
- event publication latency;
- projection lag;
- job queue age;
- approval queue query;
- artifact list/preview;
- memory retrieval;
- cost summary;
- backup throughput;
- restore duration.

## 141. Performance datasets

Profiles:

```text
small_local
mvp_nominal
mvp_upper_bound
recovery_backlog
large_audit_history
artifact_heavy
```

## 142. MVP nominal profile

Direction:

- 5 concurrent users;
- 4 active runs;
- 20 workspaces;
- 10,000 runs;
- 25,000 artifact metadata records;
- multiple adapters and model profiles.

Exact targets remain aligned with `NFR-001`.

## 143. Load-test safety

Load tests must:

- use synthetic data;
- use safe adapters;
- avoid real provider spend unless explicitly bounded;
- avoid public external sends;
- record resource limits;
- clean up;
- not corrupt shared environments.

## 144. Performance regression

A regression threshold requires:

- baseline;
- same environment;
- statistical comparison;
- warm-up;
- repeated runs;
- resource metrics;
- documented variance.

Do not fail releases on noisy single measurements without analysis.

## 145. Scalability verification

Verify:

- bounded pagination;
- indexes;
- worker concurrency;
- outbox backlog drain;
- projection rebuild;
- workspace fairness;
- no unbounded memory;
- no high-cardinality metrics;
- no N+1 critical queries.

## 146. Migration test strategy

Every migration is tested for:

- clean install;
- supported previous version;
- representative data;
- constraints;
- indexes;
- backfill;
- interruption;
- resume;
- application compatibility;
- verification;
- backup requirement.

## 147. Migration fixtures

Include:

- empty database;
- minimal database;
- nominal data;
- maximum-length values;
- multiple workspaces;
- stale/unknown states;
- active/nonterminal runs;
- consumed approvals;
- deleted artifacts;
- event backlog.

## 148. Expand-and-contract tests

Verify:

- old and new schema coexist;
- dual-read/write where applicable;
- backfill;
- consumer migration;
- removal only after compatibility;
- rollback/forward-fix.

## 149. Backup verification

Backup acceptance requires:

- operation success;
- manifest;
- scope;
- hashes;
- database consistency;
- content-store inclusion;
- event/inbox/outbox inclusion;
- tombstones;
- encryption state;
- verification result;
- retention.

## 150. Restore drill

A restore drill must:

1. create representative data;
2. create and verify backup;
3. provision isolated clean environment;
4. restore;
5. run migrations if required;
6. reconcile artifacts/events/runs;
7. verify invariants;
8. run smoke/E2E;
9. compare manifest;
10. produce recovery report.

## 151. Restore safety tests

T0 checks:

- consumed approvals remain consumed;
- leases invalidated;
- nonterminal runs enter recovery;
- external effects not replayed;
- deleted artifacts remain deleted;
- memory tombstones preserved;
- inbox dedup preserved;
- event cursors handled;
- secrets not restored incorrectly;
- workspace isolation intact.

## 152. Business-continuity tests

Scenarios:

- database loss;
- artifact store loss;
- adapter outage;
- model provider outage;
- identity outage;
- corrupted event store;
- unavailable search index;
- host restart;
- network isolation;
- operator unavailable.

Detailed RPO/RTO belongs in `BCP-001`.

## 153. Operational rehearsal

Before pilot:

- startup;
- shutdown;
- upgrade;
- migration;
- adapter revoke;
- emergency stop;
- stuck run;
- dead letter;
- artifact quarantine;
- backup;
- restore;
- incident handoff;
- evidence export.

## 154. Exploratory testing

Exploratory charters should target:

- confusing state transitions;
- stale/unknown UI;
- approval comprehension;
- artifact provenance;
- operator recovery;
- multi-workspace switching;
- long timelines;
- partial failures;
- accessibility under degraded conditions.

## 155. Usability verification

Measures may include:

- task completion;
- error recovery;
- approval comprehension;
- state comprehension;
- operator confidence;
- time to diagnose stale run;
- time to identify actual model/cost source;
- accessibility blockers.

Usability evidence complements, not replaces, functional tests.

## 156. Localization tests

Verify:

- stable English machine codes;
- translated human labels;
- date/time formatting;
- pluralization;
- long text expansion;
- no logic based on translated strings;
- screen-reader labels;
- fallback locale.

## 157. Browser matrix

Initial direction:

- current supported Chromium-based desktop;
- one additional desktop browser where feasible;
- responsive mobile viewport testing;
- actual mobile browser smoke for approval and artifact review where enabled.

Final support matrix requires product decision.

## 158. Operating-system matrix

Primary:

```text
Linux
WSL2 on Windows
```

Optional future:

```text
native Windows
macOS
```

Only supported environments receive release gates.

## 159. Docker/Compose tests

Verify:

- clean build;
- startup;
- health;
- persistent volumes;
- restart;
- non-root;
- no Docker socket;
- env validation;
- backup volumes;
- port exposure;
- resource limits;
- image scan.

## 160. Configuration tests

Verify:

- required config missing;
- malformed config;
- insecure public bind;
- missing secret reference;
- prohibited feature enabled;
- unknown environment;
- incompatible schema;
- degraded optional dependency;
- configuration precedence.

## 161. Feature-flag tests

Every flag tests:

- default;
- enabled;
- disabled;
- scope;
- expiry;
- migration;
- security controls not bypassed;
- removal.

## 162. Dependency and supply-chain tests

Verify:

- lockfile integrity;
- trusted registry;
- vulnerability scan;
- license;
- install scripts;
- image provenance;
- SBOM generation where adopted;
- no unused risky dependency;
- no unpinned critical runtime.

## 163. Static architecture tests

Potential checks:

- domain does not import web framework;
- domain does not import provider SDK;
- no generic run-state patch endpoint;
- no raw secret schema field;
- protected aggregates include workspace;
- approval consumption uniqueness;
- event classification/correlation;
- adapter isolation;
- generated contracts current.

## 164. Code coverage policy

Coverage thresholds may be set, but release-critical areas require direct evidence.

Critical paths:

- state guards;
- approval fingerprint/consumption;
- workspace authorization;
- retry/unknown;
- outbox/inbox;
- artifact integrity;
- backup/restore;
- cost arithmetic.

A high global percentage cannot compensate for missing critical tests.

## 165. Mutation testing

Mutation testing may be used selectively for:

- state guards;
- approval logic;
- authorization;
- retry eligibility;
- classification;
- cost arithmetic.

This is optional until tooling is selected, but valuable for high-risk pure logic.

## 166. Flaky-test policy

A flaky test is:

- tracked as a defect;
- assigned an owner;
- quarantined only with explicit expiry;
- not silently retried until green;
- measured;
- fixed or removed with replacement evidence.

## 167. Test retry policy

CI retry may be allowed only for:

- known infrastructure/transient test harness issues;
- with first failure preserved;
- with retry count visible;
- without hiding deterministic product failure.

T0 tests should not rely on retries for acceptance.

## 168. Test quarantine

Quarantine record includes:

- test ID;
- reason;
- first failure;
- owner;
- affected requirement;
- risk;
- workaround;
- expiry;
- replacement coverage.

Quarantined T0 tests block release unless an approved exception exists.

## 169. Defect severity

```text
S0 — Safety/security/data-loss critical
S1 — Critical workflow or invariant failure
S2 — Major degradation
S3 — Moderate defect
S4 — Minor/cosmetic
```

## 170. S0 examples

- cross-workspace leak;
- agent self-approval;
- duplicate protected action;
- lost consumed approval on restore;
- secret exposure;
- destructive unsafe replay;
- backup cannot restore;
- sandbox escape;
- prohibited production/financial action possible.

## 171. Defect fields

A defect records:

- ID;
- summary;
- environment/build;
- steps;
- expected/actual;
- severity;
- requirement;
- evidence;
- security/data impact;
- workaround;
- owner;
- status;
- regression test;
- release impact.

## 172. Defect lifecycle

```text
new
triaged
confirmed
in_progress
fixed
verification_pending
verified
closed
deferred
rejected
duplicate
```

Deferred defects require risk, owner, and review date.

## 173. Exit criteria by stage

Stages:

```text
developer_complete
integration_candidate
release_candidate
pilot_ready
commercialization_candidate
```

## 174. Developer-complete criteria

- unit/state tests;
- relevant integration tests;
- lint/type/build;
- no known S0/S1 introduced;
- docs/contracts updated;
- visual verification for UI;
- local smoke;
- no secret/mock operational state.

## 175. Integration-candidate criteria

- module integration passes;
- database/migrations pass;
- API/event contracts pass;
- simulator E2E passes;
- concurrency tests for changed invariants;
- security negatives;
- observability;
- known limitations.

## 176. Release-candidate criteria

- all P0 traces pass;
- full test portfolio selected for release;
- S0/S1 zero;
- S2 reviewed;
- fault/recovery passes;
- backup/restore passes;
- accessibility critical journeys pass;
- performance baseline;
- dependency/security scans;
- runbooks.

## 177. Pilot-ready criteria

- pilot environment smoke;
- controlled real adapter validation;
- operational rehearsal;
- backup/restore drill;
- emergency-stop exercise;
- user acceptance;
- support contacts;
- known limitations published;
- residual risks accepted explicitly.

## 178. Commercialization-candidate criteria

Beyond local MVP:

- tenant/isolation evidence;
- production deployment controls;
- incident response;
- privacy/legal controls;
- service objectives;
- HA/DR as required;
- stronger sandbox;
- support and maintenance;
- external security review;
- load and capacity validation.

## 179. Manual test evidence

Manual evidence should include:

- test charter/case;
- tester;
- build/environment;
- date;
- steps;
- result;
- screenshots/video where safe;
- accessibility technology;
- defects;
- limitations.

## 180. Screenshot safety

Screenshots must avoid:

- secrets;
- real personal/confidential data;
- private repository content;
- access tokens;
- internal URLs where sensitive;
- unredacted error dumps.

## 181. CI pipeline direction

Suggested stages:

```text
validate
→ lint/type/schema/docs
→ unit/property/state
→ database/migration
→ contract
→ integration
→ security
→ frontend build/accessibility
→ E2E simulator
→ concurrency/fault selected
→ package/image
→ evidence manifest
```

Release and scheduled pipelines add performance, restore, and broader security suites.

## 182. Change-based test selection

Change impact analysis may select additional suites based on:

- files/modules changed;
- requirement IDs;
- schemas;
- migrations;
- adapters;
- security-sensitive paths;
- frontend routes;
- artifacts;
- events.

T0 baseline tests always run.

## 183. Scheduled tests

Nightly or periodic candidates:

- full E2E;
- longer concurrency stress;
- restore drill automation;
- dependency scan;
- container scan;
- performance trend;
- flaky-test detection;
- adapter/provider drift;
- event backlog/replay;
- malicious artifact corpus.

## 184. Real-provider tests

These require:

- explicit opt-in;
- safe synthetic data;
- bounded budget;
- approved provider/profile;
- isolated credentials;
- no production account;
- usage/cost evidence;
- cleanup;
- clear nonblocking versus release-gate classification.

## 185. Model-output evaluation

For model-generated outputs, tests may evaluate:

- schema validity;
- completeness;
- citation/source presence;
- unsafe instruction compliance;
- hallucination indicators;
- deterministic fixtures where possible;
- human review.

This does not claim universal model quality.

## 186. Evaluation datasets

Datasets should be:

- versioned;
- synthetic or licensed;
- classified;
- representative;
- free of secrets;
- bias/coverage reviewed where relevant;
- immutable per benchmark version.

## 187. Model drift tests

When provider/model/runtime changes:

- rerun capability validation;
- rerun structured-output tests;
- rerun context/output limits;
- rerun usage/model identity;
- rerun safety/approval integration;
- compare quality/latency/cost;
- update limitations.

## 188. Adapter drift tests

When adapter/runtime changes:

- contract negotiation;
- capability declaration;
- tool visibility;
- cancellation;
- checkpoint;
- event sequence;
- errors;
- security scope;
- recovery;
- conformance expiration.

## 189. Test evidence manifest

A release evidence manifest may contain:

- release/build;
- environment;
- suites;
- versions;
- results;
- durations;
- artifacts;
- scans;
- migration checks;
- restore report;
- accessibility report;
- performance report;
- exceptions;
- approvals;
- hash.

## 190. Evidence retention

Retention depends on:

- release stage;
- security;
- audit;
- defects;
- pilot;
- contractual needs.

Test evidence containing sensitive data uses restricted access and minimization.

## 191. Exception process

A test exception requires:

- failed/missing test;
- requirement;
- risk;
- reason;
- compensating evidence;
- owner;
- expiry;
- approvers;
- release scope;
- remediation plan.

S0 exceptions are generally not acceptable.

## 192. Test report summary

A release test report should show:

- scope;
- build;
- environments;
- requirements coverage;
- pass/fail/blocked;
- defects;
- flaky/quarantined;
- security findings;
- performance;
- accessibility;
- restore;
- limitations;
- release recommendation.

## 193. Quality dashboard

Potential metrics:

- requirement coverage;
- pass rate;
- T0 status;
- S0/S1 defects;
- flaky tests;
- duration;
- contract drift;
- migration status;
- restore success;
- security findings;
- accessibility blockers;
- performance trends;
- unknown/stale run defects.

## 194. Test maintenance

Tests are updated when:

- requirements change;
- schema changes;
- state changes;
- threat changes;
- adapter/provider changes;
- migration changes;
- deployment profile changes;
- defects reveal missing coverage.

Obsolete tests are removed with traceability updates.

## 195. Review checklist — test design

- Does the test verify a requirement or risk?
- Is the failure mode observable?
- Is the environment appropriate?
- Is the assertion authoritative?
- Are unknown/partial states covered?
- Is the test deterministic?
- Does it avoid real unsafe effects?
- Is evidence captured?
- Is cleanup safe?

## 196. Review checklist — security tests

- Is the attacker identity realistic?
- Is workspace isolation exercised?
- Is denial verified at all surfaces?
- Are logs/audit checked?
- Are secrets absent?
- Are replay and race considered?
- Is recovery verified?
- Does the test itself remain isolated?

## 197. Review checklist — E2E

- Does the journey use connected backend state?
- Are commands actually executed?
- Are failure states covered?
- Is freshness visible?
- Are approvals exact?
- Are artifacts real and safely previewed?
- Is receipt/audit checked?
- Is accessibility verified?

## 198. Review checklist — restore

- Was backup verified before restore?
- Is environment isolated?
- Are manifests compared?
- Are consumed approvals preserved?
- Are tombstones preserved?
- Are leases invalidated?
- Are external effects suppressed?
- Are indexes/projections rebuilt safely?
- Are gaps documented?

## 199. Forbidden test shortcuts

Do not:

- pass tests by changing expected result to current bug;
- disable T0 tests without exception;
- use real production credentials;
- perform real public/financial effects;
- treat mock state as release evidence;
- hide first failure through retry;
- use sleeps where deterministic control exists;
- skip cross-workspace negative tests;
- claim backup success without restore;
- claim accessibility based only on automated scan;
- claim cancellation based only on acknowledgement;
- claim actual model identity from configured value.

## 200. Initial test implementation order

Recommended sequence:

```text
1. Test harness and fixtures
2. Domain/state-machine tests
3. Database and migration tests
4. API and event contract tests
5. Outbox/inbox/job/lease tests
6. Simulator adapter conformance
7. Run E2E
8. Approval/security tests
9. Artifact/security tests
10. Backup/restore and recovery
11. Accessibility and visual verification
12. Performance baseline
13. Real adapter/provider conformance
```

## 201. Minimum first vertical-slice suite

For the first safe vertical slice:

- login/workspace;
- task/snapshot;
- create run idempotently;
- persist before dispatch;
- simulator success;
- run events;
- text artifact;
- review/acceptance;
- receipt;
- cross-workspace denial;
- API restart;
- worker restart.

## 202. Minimum second vertical-slice suite

For approval-gated protected simulation:

- policy decision;
- exact fingerprint;
- human eligibility;
- independence;
- one-time consumption;
- concurrent replay;
- target substitution;
- emergency stop;
- protected simulator effect;
- result/unknown;
- receipt.

## 203. Minimum Codex integration suite

- scoped fixture repository;
- read;
- patch;
- test;
- build;
- artifact diff;
- approval exactness;
- optional commit in isolated fixture;
- no push without separate approval;
- merge/force push/history rewrite denied;
- crash/reconcile;
- no user repository damage.

## 204. Minimum Hermes integration suite

- verified invocation;
- session attribution;
- capabilities;
- events;
- model identity;
- usage;
- native-tool visibility;
- protected-effect delegation;
- cancellation semantics;
- crash/recovery;
- workspace isolation.

## 205. Test tooling requirements

Selected tooling must support:

- typed assertions;
- parallel isolation;
- database fixtures;
- property testing;
- browser automation;
- accessibility scans;
- network/process fault injection;
- coverage;
- JUnit or equivalent output;
- artifact reports;
- deterministic clocks;
- container execution.

## 206. ADR backlog

### `ADR-CANDIDATE-TST-001 — Test framework and runner stack`

Select backend, frontend, browser, property, and orchestration test frameworks.

### `ADR-CANDIDATE-TST-002 — CI execution matrix and evidence storage`

Select CI platform, required jobs, parallelization, artifact retention, and release manifests.

### `ADR-CANDIDATE-TST-003 — Security and malicious-content test toolchain`

Select scanners, sandbox test harness, artifact corpus, SAST/DAST, and supply-chain tools.

### `ADR-CANDIDATE-TST-004 — Performance and fault-injection harness`

Select load framework, resource profiles, fault injection, and benchmark storage.

### `ADR-CANDIDATE-TST-005 — Accessibility and visual-regression toolchain`

Select automated accessibility, browser/screen-reader workflow, screenshot baselines, and review process.

## 207. Open decisions

1. Which backend/frontend/browser test frameworks?
2. Which CI platform and operating-system matrix?
3. Which database versions are supported?
4. Which browser matrix is required?
5. Which security scanners are mandatory?
6. Which performance framework?
7. Which fault-injection mechanism?
8. Which accessibility tools?
9. Which visual-regression approach?
10. Which malicious-content corpus?
11. Which real-provider tests block release?
12. Which adapter conformance expiration applies?
13. Which coverage thresholds?
14. Which mutation-testing scope?
15. Which test-evidence retention periods?
16. Which flaky-test retry policy?
17. Which test exceptions are permissible?
18. Which release stages require manual sign-off?
19. Which restore drill cadence?
20. Which pilot data may be used?
21. Which mobile devices/browsers are required?
22. Which threat scenarios are T0?
23. Which performance targets become hard gates?
24. Which scheduled test cadence applies?
25. Which test dashboards are required?

## 208. Risks

| Risk | Consequence | Response |
|---|---|---|
| Too many mocked tests | False confidence | Real DB/simulator/contracts |
| E2E only | Slow/brittle gaps | Layered portfolio |
| Coverage percentage worship | Critical path untested | Risk/invariant coverage |
| Flaky tests retried | Hidden instability | Defect/quarantine policy |
| No fault injection | Recovery unproven | Crash/outage suites |
| Backup without restore | False resilience | Mandatory restore drill |
| Accessibility automated only | User blockers | Manual keyboard/AT |
| Real provider in default CI | Cost/flakiness/data risk | Opt-in bounded tests |
| Unknown state omitted | Unsafe UI/retry | Explicit fixtures/assertions |
| Cross-workspace tests sparse | Data leakage | Per-resource pattern |
| Approval tested only happy path | Replay/substitution | T0 abuse/concurrency |
| Adapter report trusted | False completion | Domain guard tests |
| Malicious artifacts omitted | Preview compromise | Security corpus |
| Restore loses inbox | Duplicate effects | Recovery T0 |
| Performance tested too late | Architectural bottleneck | Early baseline |
| Migration only from empty DB | Upgrade failure | Previous-state tests |
| Visual tests on stale build | False validation | Build identity/hard refresh |
| Test secrets leak | Security incident | Synthetic data/redaction |
| Agent report accepted without verification | Incorrect evidence | Inspect diff/runtime/results |
| Release exception permanent | Accumulated risk | Owner/expiry/remediation |

## 209. Assumptions

- test environments can run a relational database;
- containers and isolated filesystems are available;
- simulator adapters can model failures;
- CI can collect artifacts;
- synthetic data can represent all critical states;
- backup/restore can run in isolated environments;
- accessibility and browser testing can be performed;
- selected adapters/providers expose test accounts or safe local modes;
- product/security/data/operations owners can review release evidence;
- requirements remain traceable.

## 210. Constraints

- no real production or financial effects;
- no production credentials;
- no public unrestricted messaging;
- no destructive test against user repositories or data;
- no exactly-once assumption;
- no test-based claim of perfect security;
- no backup acceptance without restore;
- no accessibility acceptance from automation alone;
- no mock state as release evidence for critical workflows;
- no final test tooling selected in this draft;
- no commit, push, PR, or merge during the current documentation phase;
- Git versioning is active; test evidence must identify the commit, environment, command, result, and known limitations.

## 211. Acceptance criteria

TST-001 may advance to `1.0.0` when:

1. Product accepts critical user journeys and acceptance evidence.
2. Architecture accepts test levels, state, contract, concurrency, and adapter verification.
3. Security accepts threat-based, abuse, sandbox, secret, and cross-workspace coverage.
4. Data accepts fixtures, integrity, migrations, backup, restore, and cost verification.
5. Operations accepts fault, recovery, runbook rehearsal, and environment coverage.
6. Quality accepts governance, IDs, evidence, defects, flakiness, and stage gates.
7. every P0 requirement has a verification method;
8. every high/critical threat has prevention/detection/recovery coverage;
9. T0 tests are identified;
10. restore safety tests are mandatory;
11. approval and unknown-effect concurrency tests exist;
12. adapter conformance is defined;
13. accessibility includes manual verification;
14. evidence is reproducible and safe;
15. `QAG-001`, `OBS-001`, `OPS-001`, and `BCP-001` can proceed.

## 212. Downstream impact

| Document | Required use |
|---|---|
| `QAG-001` | Release gates, blockers, waivers, and evidence |
| `OBS-001` | Metrics and alerts needed to test runtime behavior |
| `OPS-001` | Operational runbooks and rehearsals |
| `BCP-001` | Backup/restore and continuity tests |
| `PLG-001` | Plugin conformance and security test profile |
| `RTM-001` | Requirement-to-test-to-evidence mapping |

## 213. Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.2.0`
- Approved by: Product Owner under explicit user authorization to finalize the declared scope
- Finalization note: approval records the documentation baseline only; implementation and verification remain separate evidence gates

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial test strategy and verification plan covering levels, environments, fixtures, state machines, APIs, events, adapters, models, tools, approvals, artifacts, memory, security, accessibility, E2E, concurrency, faults, performance, migrations, backup/restore, CI evidence, defects, and release-stage criteria |
| 0.2.0 | 2026-08-13 | Approved | Added commit-specific evidence requirements and clarified the boundary of the current automated baseline |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SRS-001` — Functional Requirements
- `NFR-001` — Non-Functional Requirements
- `THR-001` — Threat Model
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `API-001` — API Specification
- `EVT-001` — Event Catalog and Async Contract
- `DEV-001` — Development and Implementation Guide
