---
document_id: DEV-001
title: Agent OS Development and Implementation Guide
version: 0.1.0
status: draft
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
  - SAD-001
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
  - TST-001
  - QAG-001
  - OBS-001
  - OPS-001
  - BCP-001
related_adrs:
  - ADR-TBD-DEV-001
  - ADR-TBD-DEV-002
  - ADR-TBD-DEV-003
  - ADR-TBD-DEV-004
  - ADR-TBD-DEV-005
  - ADR-TBD-DEV-006
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# DEV-001 — Agent OS Development and Implementation Guide

> **Status: Draft.** This guide translates the approved and draft Agent OS contracts into concrete implementation rules, repository structure, module boundaries, coding conventions, local development workflows, test strategy, Docker/WSL practices, security controls, and phased delivery guidance. It does not select final frameworks, programming-language versions, cloud services, or deployment platforms. Any reference stack described here remains provisional until the corresponding ADR is approved.

## 1. Purpose

This guide defines how Agent OS should be implemented so that the codebase preserves the product, security, data, orchestration, approval, artifact, API, and event contracts already documented.

It provides:

- a recommended repository layout;
- application and service boundaries;
- domain-module rules;
- dependency rules;
- transactional and asynchronous implementation patterns;
- adapter and provider integration conventions;
- frontend architecture and accessibility rules;
- database and migration practices;
- artifact and memory implementation rules;
- configuration and secret management;
- local Linux/WSL and Docker workflow;
- test categories and local commands;
- code quality and review standards;
- Git and delivery workflow;
- implementation phases and vertical slices;
- Definition of Ready and Definition of Done;
- forbidden shortcuts and common failure patterns;
- traceability to controlled documents.

## 2. Development objectives

The implementation must:

1. preserve provider neutrality;
2. keep the control plane authoritative;
3. persist runs before external dispatch;
4. keep task snapshots immutable;
5. keep attempts append-only;
6. enforce workspace isolation everywhere;
7. keep policy, capability, approval, and execution separate;
8. prevent direct adapter authority;
9. make unknown, stale, partial, and unavailable states explicit;
10. support durable recovery after process restart;
11. support idempotency and optimistic concurrency;
12. preserve exact approval consumption;
13. treat model, tool, and artifact output as untrusted;
14. preserve provenance and evidence;
15. support local Linux/WSL operation;
16. keep the first product operable by a small team;
17. provide a path from local MVP to controlled commercial deployment;
18. keep implementation choices replaceable behind contracts.

## 3. Non-goals

This guide does not:

- select the final backend web framework;
- select the final frontend framework version;
- select the final event broker;
- select the final workflow engine;
- select the final object store;
- define public SaaS tenancy;
- define high availability;
- authorize production or financial operations;
- authorize autonomous Git merge;
- authorize unrestricted host access;
- authorize unrestricted network access;
- provide a shortcut around security or approval controls;
- treat prototypes or mock data as completed production functionality.

## 4. Engineering principles

### `DEV-P-001 — Contracts before implementations`

Implementations must conform to stable domain contracts rather than inventing new semantics in controllers, components, or adapters.

### `DEV-P-002 — Domain logic remains framework-independent`

Core state transitions, invariants, policy decisions, and value objects should be testable without HTTP, UI, database, provider, or adapter dependencies.

### `DEV-P-003 — Persist before effect`

External calls, workers, adapters, tools, messages, Git effects, and provider requests occur only after the relevant command, state, and dispatch intent are durable.

### `DEV-P-004 — Explicit states over implicit booleans`

Use controlled lifecycle states, source states, confidence states, and reason codes.

Avoid ambiguous flags such as:

```text
is_done
is_ok
has_error
is_connected
```

unless they are derived convenience fields.

### `DEV-P-005 — Unknown is a valid result`

Do not coerce unknown cost, model identity, effect state, provider health, or artifact integrity into false, zero, empty, or completed.

### `DEV-P-006 — Every boundary validates`

Validate at API, command, domain, adapter, tool, persistence, and content boundaries.

### `DEV-P-007 — Least privilege by construction`

Code receives only the workspace, data, paths, network destinations, secret references, and capabilities required for one operation.

### `DEV-P-008 — Append evidence, do not rewrite history`

Attempts, decisions, events, receipts, and material artifact versions are append-oriented.

### `DEV-P-009 — Safe degradation`

Unavailable optional systems may reduce capability, but must not create false success or bypass controls.

### `DEV-P-010 — Build for recovery`

Every long-running operation must define restart, duplicate, timeout, stale, unknown, and reconciliation behavior.

### `DEV-P-011 — Generated code is not trusted code`

AI-generated changes require tests, review, and the same quality gates as human-written changes.

### `DEV-P-012 — Vertical slices prove architecture`

Implement one end-to-end safe workflow before broad feature expansion.

## 5. Reference implementation profile

The initial recommended profile is:

```text
Provider-neutral modular control-plane application
+ separate durable workers
+ isolated Hermes and Codex adapter processes
+ relational transactional database
+ database-backed outbox/inbox and durable job mechanism
+ protected artifact-content storage abstraction
+ TypeScript web client
+ Docker Compose local orchestration
+ Linux/WSL-first development
```

This profile is a recommendation, not an approved technology decision.

## 6. Candidate technology families

The implementation may use technologies from these families:

| Concern | Candidate family |
|---|---|
| Backend/control plane | Typed Python or another strongly governed server stack |
| Web API | Resource-oriented HTTP/JSON with machine-readable schemas |
| Frontend | TypeScript component application |
| Database | Transactional relational database |
| Job/event durability | Database-backed queue/outbox first, broker later if justified |
| Content storage | Local protected filesystem through an object-store abstraction |
| Search | Relational/full-text first; derived search index later |
| Vector retrieval | Optional derived index after core memory rules |
| Auth | Local protected sessions first; external IdP later |
| Containers | Docker Compose for local development and pilot |
| Testing | Unit, integration, contract, browser, fault, security |
| Documentation | Markdown and generated machine-readable contracts |

Final selections require ADRs.

## 7. Repository strategy

A monorepo is recommended for the first implementation because:

- contracts span frontend, backend, adapters, workers, and tests;
- a small team needs synchronized changes;
- shared schemas and fixtures should remain close;
- local orchestration is easier;
- traceability is simpler.

The monorepo must still enforce module boundaries.

## 8. Recommended repository layout

```text
agent-os/
├── apps/
│   ├── control-plane-api/
│   ├── mission-control-web/
│   ├── worker/
│   └── local-admin/
├── services/
│   ├── orchestrator/
│   ├── policy/
│   ├── approval/
│   ├── artifact/
│   ├── memory/
│   ├── audit/
│   ├── cost/
│   └── operations/
├── adapters/
│   ├── common/
│   ├── hermes/
│   ├── codex/
│   └── simulator/
├── packages/
│   ├── domain/
│   ├── contracts/
│   ├── event-schemas/
│   ├── api-client/
│   ├── ui-components/
│   ├── test-fixtures/
│   └── observability/
├── infrastructure/
│   ├── docker/
│   ├── compose/
│   ├── database/
│   ├── local-storage/
│   └── reverse-proxy/
├── migrations/
├── scripts/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── concurrency/
│   ├── fault/
│   ├── security/
│   ├── accessibility/
│   ├── e2e/
│   └── recovery/
├── docs/
├── .env.example
├── compose.yaml
├── Makefile
└── README.md
```

The exact physical layout may be adapted, but responsibilities must remain explicit.

## 9. Application boundaries

### `apps/control-plane-api`

Responsibilities:

- authentication/session boundary;
- API request validation;
- command dispatch;
- query/read-model access;
- response and error mapping;
- rate limiting;
- request correlation;
- no direct provider/tool business logic.

### `apps/mission-control-web`

Responsibilities:

- operator UI;
- accessible workflows;
- read-model consumption;
- explicit loading, empty, stale, partial, unavailable, and error states;
- command submission;
- no client-authoritative lifecycle state.

### `apps/worker`

Responsibilities:

- consume durable jobs;
- acquire leases and fencing tokens;
- execute bounded domain/application work;
- heartbeat;
- persist results;
- no approval authority.

### `apps/local-admin`

Optional local administrative utility for:

- bootstrap;
- status;
- backup;
- restore validation;
- recovery diagnostics;
- schema checks;
- no hidden bypass of control-plane rules.

## 10. Domain services

The first implementation may package services inside a modular monolith process, provided boundaries remain logical and testable.

Recommended logical modules:

```text
identity
organization
workspace
project
registry
task
run
policy
approval
adapter_gateway
model_gateway
tool_gateway
artifact
memory
audit
cost
operations
events
```

## 11. Modular-monolith rule

The modular monolith is acceptable when:

- each module owns its domain objects;
- cross-module writes use application contracts;
- database tables remain logically owned;
- direct cross-module repository calls are restricted;
- events or application services mediate integration;
- tests can instantiate modules independently;
- later extraction remains possible.

A modular monolith is not permission to create one global service layer.

## 12. Dependency direction

Recommended direction:

```text
UI / API / CLI
        ↓
Application commands and queries
        ↓
Domain model
        ↓
Ports / interfaces
        ↓
Infrastructure adapters
```

The domain model does not import:

- web framework;
- ORM model classes;
- HTTP clients;
- provider SDKs;
- Docker APIs;
- frontend types;
- environment variables.

## 13. Layer responsibilities

### Domain layer

Contains:

- aggregates;
- entities;
- value objects;
- policies that are truly domain rules;
- state machines;
- invariants;
- domain errors;
- domain events.

### Application layer

Contains:

- commands;
- queries;
- use cases;
- transaction coordination;
- authorization/policy orchestration;
- idempotency coordination;
- outbox scheduling;
- DTO mapping.

### Infrastructure layer

Contains:

- database repositories;
- event/job transport;
- adapter clients;
- content storage;
- provider clients;
- secret resolution;
- telemetry;
- filesystem/network implementations.

### Interface layer

Contains:

- HTTP/API;
- CLI;
- worker handlers;
- UI;
- serialization;
- safe error mapping.

## 14. Bounded-context ownership

Each bounded context from `DDD-001` must have:

- code owner;
- module root;
- aggregate list;
- database-table ownership;
- command/query interfaces;
- event catalogue;
- tests;
- operational metrics;
- migration responsibility.

## 15. Cross-context interaction

Permitted patterns:

```text
application service call through explicit interface
domain/integration event
read-only projection
anti-corruption adapter
```

Discouraged:

```text
direct table mutation across contexts
shared mutable ORM entity
global service locator
untyped dictionary payload
framework signal with hidden semantics
```

## 16. Shared kernel

The shared kernel should be minimal.

Allowed shared concepts:

- opaque IDs;
- timestamps;
- classification;
- source and authority states;
- money/usage semantic types;
- correlation;
- common error envelope;
- event envelope;
- pagination;
- idempotency;
- workspace scope.

Business aggregates should not live in a shared “models” package.

## 17. Canonical contracts package

`packages/contracts` should contain or generate:

- API schemas;
- event schemas;
- adapter contracts;
- capability schemas;
- model-profile schemas;
- run command and read-model schemas;
- approval schemas;
- artifact schemas;
- error codes;
- controlled enums.

Human-readable documents remain the governing design until machine schemas are approved.

## 18. Contract-generation rule

Generated contracts must be reproducible.

A generated file should contain:

- source document/schema reference;
- generator version;
- generation time if required;
- content hash;
- warning against manual edits.

CI should fail when generated contracts are stale.

## 19. Domain identifiers

Use opaque IDs generated by a controlled ID service or library.

Rules:

- never reuse IDs;
- never trust client-selected protected IDs without validation;
- preserve IDs across retries;
- distinguish aggregate IDs and external IDs;
- store external provider IDs separately;
- use explicit type wrappers where language permits.

## 20. Semantic types

Avoid primitive obsession.

Prefer types such as:

```text
WorkspaceId
RunId
AttemptId
ApprovalFingerprint
ContentHash
Classification
CurrencyAmount
UtcTimestamp
ProviderRequestId
NormalizedTarget
```

This reduces accidental cross-field substitution.

## 21. Controlled enums

Controlled enum handling:

- one canonical definition;
- database value stable;
- API/event value stable;
- frontend labels separate;
- unknown values handled safely;
- lifecycle changes require review;
- no free-form state strings.

## 22. Database design direction

Use a transactional relational database as the first authoritative store.

Reasons:

- strong consistency for runs, approvals, budgets, and artifact metadata;
- transactions;
- unique constraints;
- optimistic concurrency;
- referential integrity;
- mature backup and migration support;
- straightforward local operation.

## 23. Database schema ownership

Each table has:

- owning context;
- purpose;
- primary key;
- workspace/organization fields where required;
- classification where required;
- version field for mutable aggregates;
- creation/update times;
- retention behavior;
- indexes;
- constraints;
- migration owner.

## 24. Workspace-first data access

Every protected repository method requires workspace scope.

Preferred interface:

```text
get_run(workspace_id, run_id)
list_artifacts(workspace_id, filters)
save_approval(workspace_id, approval)
```

Discouraged:

```text
get_by_id(run_id)
```

unless the repository is internal and the caller already has an enforced scoped handle.

## 25. Row-level protection

The implementation should use multiple layers:

- application repository scope;
- database constraints;
- query tests;
- optional database row-level security where an ADR selects it;
- negative cross-workspace integration tests.

One layer alone is not sufficient assurance.

## 26. Aggregate transactions

Strongly consistent operations include:

- create run and outbox event;
- transition run state;
- create attempt and dispatch intent;
- consume approval and bind attempt;
- reserve budget;
- finalize artifact version;
- create memory version;
- activate/revoke role or grant;
- activate/release emergency stop.

These operations must use explicit transactions.

## 27. Unit of work

A unit of work should:

- open one transaction;
- load scoped aggregates;
- enforce expected versions;
- collect domain events;
- write aggregate changes;
- write outbox events;
- commit;
- expose deterministic result.

External calls do not occur inside the transaction.

## 28. Optimistic concurrency

Mutable aggregates carry a version.

Update pattern:

```text
UPDATE ...
SET ..., version = version + 1
WHERE id = ?
  AND workspace_id = ?
  AND version = expected_version
```

No affected row means conflict or missing scoped resource.

## 29. Unique constraints

Examples:

- task snapshot number per task;
- attempt number per step;
- approval consumption per request;
- event inbox per consumer/event;
- idempotency key per actor/workspace/operation;
- active lease uniqueness;
- active workspace capability enablement;
- artifact version number per artifact;
- usage deduplication key.

Constraints are part of correctness, not only optimization.

## 30. Transactional outbox

Every domain state change that requires async communication writes an outbox record in the same transaction.

Publisher behavior:

- lease records;
- publish;
- record success;
- retry boundedly;
- keep stable event IDs;
- dead-letter after policy threshold;
- expose metrics.

## 31. Consumer inbox

Stateful consumers persist:

- event ID;
- consumer ID;
- processing state;
- result;
- attempts;
- errors.

Processing business state and inbox completion should be atomic where practical.

## 32. Durable jobs

Durable jobs may initially use database-backed records.

A job record includes:

- job type;
- workspace;
- run/step/attempt;
- payload reference;
- schedule;
- priority;
- deduplication;
- attempts;
- lease;
- state.

A broker may be added later, but the durable source remains clear.

## 33. Worker leasing

Workers must:

1. select eligible jobs;
2. acquire lease atomically;
3. receive fencing token;
4. persist attempt binding;
5. execute bounded work;
6. heartbeat;
7. commit result using valid fencing token;
8. release or complete lease.

Expired leases trigger reconciliation before consequential redispatch.

## 34. Fencing-token implementation

Every state-changing worker result includes the lease fencing token.

The database update rejects results from older tokens.

This protects against:

- paused process resuming late;
- network partition;
- duplicate worker;
- scheduler race;
- restored old worker state.

## 35. Scheduler

The scheduler handles:

- available jobs;
- delayed retries;
- waiting-condition checks;
- approval expiry;
- lease expiry;
- deadline processing;
- maintenance windows;
- recovery scans;
- retention tasks.

The scheduler never bypasses domain commands.

## 36. State-machine implementation

Lifecycle transitions must be implemented as:

- explicit command handlers;
- aggregate methods;
- transition tables;
- or another testable pattern.

Avoid generic:

```text
set_state(new_state)
```

Preferred:

```text
run.start_preflight(...)
run.mark_waiting_for_approval(...)
run.request_cancellation(...)
run.complete(...)
```

Each method enforces guards.

## 37. Domain errors

Domain errors use stable codes.

Examples:

```text
RUN_STATE_CONFLICT
APPROVAL_FINGERPRINT_MISMATCH
ARTIFACT_INTEGRITY_FAILED
WORKSPACE_SCOPE_MISMATCH
CAPABILITY_NOT_READY
```

Framework exceptions are translated at the interface boundary.

## 38. Idempotency implementation

An idempotency service stores:

- key;
- operation;
- actor;
- workspace;
- canonical request hash;
- state;
- result reference;
- response metadata;
- expiry.

Handling:

```text
new key
→ reserve
→ execute
→ persist result

same key + same hash
→ return original result

same key + different hash
→ conflict
```

## 39. Canonical request hashing

Canonicalization rules must be:

- deterministic;
- versioned;
- independent of JSON field order;
- explicit about omitted/null/default values;
- safe for Unicode;
- stable across supported implementations;
- tested with golden fixtures.

## 40. External-effect idempotency

Platform idempotency does not automatically make an external effect idempotent.

For each tool/provider operation document:

- native idempotency support;
- platform key;
- target key;
- side-effect certainty;
- duplicate-detection method;
- reconciliation method.

## 41. API implementation

Controllers/handlers should:

- authenticate;
- resolve correlation;
- validate schema;
- dispatch command/query;
- map result/error;
- set safe headers;
- never contain domain state-transition logic;
- never call adapters/tools directly.

## 42. API schema validation

Validate:

- types;
- required fields;
- bounds;
- controlled enums;
- media types;
- nested depth;
- array length;
- semantic formats;
- extension namespaces;
- reference syntax.

Semantic domain validation still occurs after schema validation.

## 43. API error mapping

Map domain/application errors to:

- stable HTTP status;
- stable machine code;
- safe message;
- retryability;
- current state/version;
- side-effect certainty;
- remediation code;
- correlation.

Do not expose raw ORM, SQL, provider, or stack exceptions.

## 44. API pagination

Use cursor pagination for mutable large collections.

Cursor generation must bind:

- workspace;
- filters;
- sort;
- stable tiebreaker;
- retention epoch;
- authorization context if required.

## 45. API client generation

The frontend client should be generated or strongly typed from machine-readable schemas.

Generated client responsibilities:

- request/response types;
- error types;
- pagination;
- ETag;
- idempotency header support;
- operation polling;
- event cursors.

The generated client must not automatically retry consequential unknown effects.

## 46. Frontend architecture

Recommended frontend layers:

```text
app shell
route modules
feature modules
domain view models
API client
event/read-model subscriptions
shared accessible components
```

Avoid a global untyped state store containing every domain entity.

## 47. Mission Control modules

Initial modules:

```text
authentication
workspace selector
dashboard
tasks
runs
approvals
agents and adapters
model profiles
artifacts
memory
costs and budgets
audit and receipts
operations and health
settings
```

## 48. Frontend state categories

Every async view should distinguish:

```text
initial
loading
refreshing
ready
empty
partial
stale
degraded
blocked
unavailable
error
```

A successful HTTP response may still contain stale or partial domain data.

## 49. No mock-state substitution

Mocks are permitted for:

- isolated component development;
- Storybook-like environments;
- deterministic tests;
- prototype references.

Mocks must not:

- appear as live production data;
- mark actions as persisted;
- make buttons look functional when they are not;
- bypass backend contracts;
- remain in connected release pages without explicit label and gate.

## 50. Frontend command handling

For every command:

- disable duplicate submission while unresolved;
- send idempotency key where required;
- display accepted versus completed;
- handle `409`/`412` conflicts;
- preserve correlation ID;
- display approval/waiting states;
- refresh authoritative resource;
- avoid optimistic success for consequential actions.

## 51. Frontend read-model freshness

Views must show:

- source;
- observed/projected time;
- freshness state;
- last reliable evidence;
- pending update indicator where relevant.

Dashboard cards cannot silently present stale projections.

## 52. Approval UI

Approval pages must implement `APR-001`:

- canonical action;
- target;
- diff/content;
- requester;
- risk;
- reversibility;
- classifications;
- provider/tool/secret purpose;
- cost source;
- unknowns;
- expiry;
- independence;
- accessible decision controls.

Approval cannot be reduced to a generic modal for high-risk actions.

## 53. Artifact UI

Artifact pages must show:

- artifact and version;
- producer/provenance;
- classification;
- integrity;
- validation;
- preview state;
- quarantine;
- acceptance purpose;
- limitations;
- export/delete state.

Safe preview uses derived content, not direct unsafe execution.

## 54. Local file selection and preview

For image or file inputs in development and user workflows:

- support local file selection;
- show metadata and bounded preview where safe;
- do not add selected user files to the repository;
- keep URL input only as an optional fallback where useful;
- validate type and size;
- treat previews as local temporary state until upload/finalization.

## 55. Accessibility

Target WCAG 2.2 AA direction from `NFR-001`.

Implementation requirements:

- semantic HTML;
- keyboard operation;
- focus visibility;
- screen-reader labels;
- reduced-motion support;
- non-color state indicators;
- accessible dialogs;
- accessible tables and diffs;
- logical heading order;
- error association;
- responsive reflow;
- no global horizontal scroll at supported widths;
- adequate touch targets;
- automated and manual testing.

## 56. Responsive validation

Minimum validation widths should include:

```text
320
375
768
1024
desktop wide
```

For each visible frontend integration:

- update the actually running local app;
- rebuild/recreate containers where required;
- smoke test;
- hard refresh;
- visually verify before the next integration.

## 57. Frontend security

The frontend must:

- avoid storing raw secrets;
- use secure session mechanisms;
- avoid localStorage for sensitive long-lived credentials;
- render untrusted content safely;
- sanitize only with approved libraries;
- enforce CSP-compatible patterns;
- avoid arbitrary HTML injection;
- use safe download/preview flows;
- preserve CSRF protections;
- not infer authorization from hidden buttons.

## 58. Adapter architecture

Each adapter should have:

```text
adapter metadata
contract negotiation
capability declaration
health and readiness
start/status/events
cancel/pause/resume/checkpoint declarations
output normalization
usage/model observation
error normalization
security limits
conformance tests
```

## 59. Adapter common library

`adapters/common` may provide:

- canonical envelopes;
- correlation;
- schema validation;
- lifecycle types;
- error types;
- idempotency helpers;
- health/readiness scaffolding;
- logging/redaction;
- conformance fixtures.

It must not hide adapter-specific limitations.

## 60. Adapter process isolation

Adapters should run separately from the core API when practical.

Reasons:

- runtime crash isolation;
- dependency isolation;
- process permissions;
- version independence;
- network/filesystem restriction;
- clearer health;
- easier revocation.

## 61. Codex adapter implementation direction

The Codex adapter should:

- bind one workspace/run to one controlled repository/worktree context;
- report executable/runtime version;
- expose file read/patch/test/build capabilities explicitly;
- distinguish patch from commit;
- route commit/push/PR through exact approval;
- prohibit merge, force push, and history rewrite;
- expose command and tool visibility limitations;
- use bounded process execution;
- normalize outputs and errors;
- preserve actual model identity only where evidenced;
- support cancellation honestly;
- pass conformance and security tests.

## 62. Hermes adapter implementation direction

The Hermes adapter should:

- expose verified invocation and session semantics;
- declare capabilities honestly;
- expose native-tool visibility;
- expose model/provider observations where available;
- report cancellation, pause, resume, and checkpoint limitations;
- preserve workspace/session isolation;
- route protected effects through Agent OS;
- support health/readiness;
- normalize outputs and errors;
- pass the same core conformance profile.

## 63. Adapter simulator

Implement a deterministic simulator early.

The simulator should support:

- normal success;
- slow start;
- duplicate events;
- out-of-order events;
- event gap;
- cancellation;
- cancellation unknown;
- crash;
- timeout before/after acceptance;
- unknown side effect;
- artifact proposal;
- model/usage observations;
- capability drift.

The simulator enables reliable orchestration tests before real adapters mature.

## 64. Model gateway

The model gateway must:

- accept logical profile intent;
- evaluate eligible bindings;
- enforce data policy;
- enforce provider/region allowlists;
- reserve budget/quota;
- record routing decision;
- call provider through adapter/client;
- preserve configured versus actual identity;
- record usage/cost source;
- expose fallback explicitly;
- normalize errors.

## 65. Provider clients

Provider-specific clients belong behind interfaces.

They must implement:

- authentication through secret references;
- endpoint allowlists;
- timeout;
- rate limit;
- retries only when safe;
- request correlation;
- model identity evidence;
- usage evidence;
- provider error mapping;
- no raw prompt logging by default.

## 66. Tool Gateway

All protected tool actions pass through a single governed gateway or equivalent controlled boundary.

Responsibilities:

- normalize action;
- validate capability;
- evaluate policy;
- create/use approval;
- verify fingerprint;
- enforce target/resource/network scope;
- execute through sandbox/integration;
- record side-effect certainty;
- issue receipt/audit evidence.

## 67. Tool implementation interface

A tool implementation should expose:

```text
describe_capability()
normalize_target()
validate_request()
estimate_effect()
execute()
cancel()
reconcile()
collect_evidence()
```

Not every tool supports every operation; unsupported behavior is explicit.

## 68. Sandbox

The sandbox must define:

- process identity;
- filesystem mounts;
- read/write roots;
- network policy;
- environment variables;
- CPU/memory/time limits;
- process limits;
- output limits;
- working directory;
- cleanup;
- audit.

The final sandbox technology remains a separate proposed/unregistered `SAN-001` concern.

## 69. Filesystem access

Rules:

- canonicalize paths;
- verify path remains under allowed root;
- handle symlinks explicitly;
- no host-home access by default;
- no Docker socket;
- no device mounts;
- no arbitrary `/mnt/c` access in WSL;
- separate read and write capability;
- deletion is distinct;
- record hashes and affected paths.

## 70. Command execution

Do not build commands by string concatenation.

Preferred:

- executable path;
- argument array;
- controlled environment;
- no shell unless explicitly required;
- timeout;
- output bounds;
- working-directory allowlist;
- exit-code mapping;
- cancellation/reconciliation.

## 71. Network access

Network access is deny-by-default.

A network profile defines:

- destinations;
- ports/protocols;
- DNS behavior;
- redirect behavior;
- proxy;
- TLS verification;
- request-size limits;
- timeout;
- rate limits;
- data classifications.

Redirects require destination revalidation.

## 72. Secret references

Application configuration and commands carry secret references.

Secret resolution occurs:

- at the narrowest execution boundary;
- only for the approved purpose;
- without returning secret values to the control plane/UI;
- with audit metadata;
- with redaction;
- with rotation/expiry handling.

## 73. Secret handling in development

Rules:

- `.env` is local and ignored;
- `.env.example` contains names and safe placeholders only;
- no secrets in Git;
- no secrets in fixtures, screenshots, logs, traces, artifacts, or prompts;
- secret scanners run in CI;
- rotate any exposed test secret immediately;
- use separate development credentials.

## 74. Configuration hierarchy

Recommended precedence:

```text
compiled safe defaults
→ environment profile configuration
→ local non-secret configuration
→ secret references
→ workspace governed configuration
→ per-run bounded snapshot
```

A lower-trust source cannot override hard security controls.

## 75. Configuration profiles

Initial profiles:

```text
development
test
local_pilot
recovery
```

Future:

```text
controlled_internal
commercial_single_tenant
```

Each profile declares:

- enabled features;
- network exposure;
- storage;
- logging;
- provider access;
- adapter set;
- security restrictions;
- backup behavior.

## 76. Startup configuration validation

Startup fails safely when required configuration is:

- missing;
- malformed;
- insecure;
- incompatible;
- referencing unavailable secrets;
- exposing public interfaces unexpectedly;
- enabling prohibited features.

Optional dependencies may place the component in degraded state.

## 77. Feature flags

Feature flags must not become hidden permanent configuration.

Every flag has:

- code;
- owner;
- purpose;
- scope;
- default;
- expiry/review;
- security impact;
- test coverage;
- removal plan.

Security controls are not disabled through ordinary feature flags.

## 78. Database migrations

Migration principles:

- version-controlled;
- deterministic;
- reviewed;
- tested from clean and previous states;
- backward/forward compatibility considered;
- backup required for risky changes;
- no unreviewed arbitrary script execution;
- verification step;
- immutable migration IDs/checksums.

## 79. Migration categories

```text
schema_additive
schema_transform
data_backfill
constraint_enforcement
index_change
destructive_cleanup
storage_migration
event_schema_migration
```

Destructive cleanup is deferred until compatibility and backup gates pass.

## 80. Expand-and-contract

Preferred breaking-change workflow:

```text
add new schema
→ dual read/write if needed
→ backfill
→ validate
→ migrate consumers
→ stop old writes
→ remove old schema later
```

Do not combine incompatible schema removal with first deployment of replacement.

## 81. Migration transaction behavior

Document whether a migration is:

- fully transactional;
- partially transactional;
- nontransactional;
- resumable;
- idempotent;
- requires maintenance.

Large backfills should use bounded batches and checkpoints.

## 82. Migration verification

Verification includes:

- schema version;
- row counts;
- null/constraint checks;
- workspace isolation;
- hashes/checksums where appropriate;
- application health;
- run/approval/artifact invariants;
- rollback/forward-fix readiness.

## 83. Rollback direction

Application rollback does not always imply database rollback.

Prefer:

- backward-compatible releases;
- forward-fix migration;
- restore only under governed procedure;
- preservation of new data.

## 84. Artifact storage implementation

Artifact metadata remains relational.

Content is accessed through an abstraction:

```text
put_staging()
finalize()
open_read()
verify()
delete()
list_orphans()
health()
```

The abstraction prevents direct host paths from leaking into domain/API code.

## 85. Local artifact store

The local MVP store may use a protected Linux filesystem directory behind the storage abstraction.

Requirements:

- not under source repository;
- no direct public serving;
- workspace/object-key isolation;
- safe permissions;
- atomic finalization;
- hash verification;
- backup support;
- orphan detection;
- quota.

## 86. Artifact preview workers

Preview workers:

- run isolated;
- use read-only input;
- use bounded scratch output;
- have no unrestricted network;
- produce derived preview artifact;
- report limitations;
- clean up;
- are disposable.

## 87. Malware and secret scanning

Scanning integrations are fallible.

The code must represent:

```text
passed
passed_with_warnings
failed
unavailable
unknown
```

Unavailable scanner is not equivalent to passed.

## 88. Memory implementation

Memory should start with relational authoritative metadata and optional text retrieval.

Do not introduce a vector database before:

- source/authority model exists;
- workspace filtering is proven;
- deletion propagation exists;
- lexical baseline exists;
- evaluation fixtures exist.

## 89. Memory write path

```text
proposal
→ schema/source validation
→ classification
→ duplicate/conflict detection
→ version creation
→ optional verification
→ durable store
→ outbox
→ derived indexing
```

An agent-created memory remains proposed/generated until governed verification.

## 90. Memory retrieval path

```text
authorize workspace
→ apply classification and authority filters
→ retrieve lexical/structured candidates
→ optional vector candidates
→ merge/rank
→ attach source/freshness/conflict state
→ return bounded context
```

Authorization occurs before ranking and snippet generation.

## 91. Vector indexing

If added:

- index is derived;
- entries include workspace and version;
- embedding profile/version recorded;
- model change triggers rebuild;
- deletions/tombstones propagate;
- cross-workspace tests required;
- scores are not universal confidence.

## 92. Audit implementation

Audit records should be append-only and source-labelled.

Audit write failures for protected actions should fail closed according to policy.

High-volume telemetry remains separate.

## 93. Execution receipt generation

Receipt generation reads:

- task snapshot;
- run/steps/attempts;
- adapters/models/tools;
- approvals;
- artifacts;
- usage/cost;
- effects;
- audit gaps.

It produces:

- structured receipt record;
- optional artifact;
- completeness state;
- hash;
- evidence references.

## 94. Cost implementation

Cost service separates:

- usage event;
- pricing profile;
- calculation;
- provider report;
- invoice;
- reconciliation.

Never store unknown cost as zero.

Money uses decimal semantic types and explicit currency.

## 95. Budget reservations

Budget reservation and attempt dispatch should coordinate transactionally where possible.

Reservation lifecycle:

```text
requested
reserved
consumed
released
expired
unknown
```

Retries and fallback account for additional reservation.

## 96. Logging

Structured logs should include:

- timestamp;
- level;
- component;
- request/correlation;
- workspace where permitted;
- run/step/attempt;
- event ID;
- error code;
- safe message;
- build identity.

Do not include:

- secrets;
- full prompts;
- full confidential artifacts;
- raw provider tokens;
- unrestricted stack traces in user-facing logs.

## 97. Log redaction

Redaction should be centralized and tested.

Redact:

- credentials;
- authorization headers;
- cookies;
- secret-looking query values;
- environment variables;
- provider keys;
- private URLs;
- sensitive content fields.

Redaction failures are security findings.

## 98. Metrics

Implementation exposes metrics for:

- API;
- database;
- outbox/inbox;
- jobs/leases;
- runs;
- approvals;
- adapters/models;
- tools;
- artifacts;
- memory;
- cost;
- backups;
- recovery.

Metric labels must avoid unbounded cardinality and sensitive values.

## 99. Tracing

Trace propagation:

```text
UI/API
→ application command
→ transaction/outbox
→ worker
→ adapter/model/tool
→ artifact/audit/cost
```

Sampling and content rules must preserve privacy.

## 100. Health endpoints

Each component exposes:

```text
live
ready
dependency health
build identity
limitations
freshness
```

Readiness is false when the component cannot safely perform its intended role.

## 101. Local development environment

Primary development environment:

```text
Linux or WSL2 Linux filesystem
+ Docker engine / Docker Desktop integration
+ repository inside Linux home
+ local browser on Windows or Linux
```

Keep the repository under:

```text
/home/<user>/projects/agent-os
```

Avoid active development under mounted Windows paths when filesystem semantics or performance are unreliable.

## 102. WSL practices

- use Linux line endings;
- keep source and virtual environments in WSL;
- configure Git identity inside WSL;
- verify Docker integration;
- avoid duplicate dev servers;
- bind local services intentionally;
- document Windows-to-WSL URLs;
- use Linux permissions for secret/config files;
- test file watching;
- avoid exposing services on all interfaces by default.

## 103. Docker Compose profile

The local Compose environment may include:

```text
control-plane-api
mission-control-web
worker
database
artifact-store
adapter-simulator
codex-adapter
hermes-adapter
optional reverse proxy
```

Some services may run outside containers during active development, but one canonical startup path must exist.

## 104. Container rules

- non-root where practical;
- read-only filesystem where practical;
- explicit volumes;
- no Docker socket;
- bounded resources;
- health checks;
- restart policy;
- no baked secrets;
- deterministic builds;
- minimal runtime image;
- build/runtime stages;
- SBOM or dependency inventory direction;
- version/build labels.

## 105. Compose data volumes

Persistent data includes:

- database;
- artifact content;
- backup output;
- optional local indexes.

Volumes are not stored inside the Git repository.

Backup/restore procedures must cover them.

## 106. Environment file workflow

Recommended:

```text
.env.example    tracked, no secrets
.env            local, ignored
.env.test       safe test configuration, no real secrets
```

Startup validates required values.

A developer should not copy production credentials into local development.

## 107. Recommended command interface

The repository should provide a consistent command facade, for example:

```text
make bootstrap
make dev
make stop
make status
make logs
make lint
make format-check
make typecheck
make test
make test-unit
make test-integration
make test-contract
make test-security
make test-e2e
make test-recovery
make migrate
make migration-check
make schema-check
make smoke
make backup-test
make restore-test
```

These commands are recommended interfaces to implement; they are not claimed to exist yet.

## 108. Bootstrap command

`make bootstrap` should:

- verify supported toolchain;
- verify Docker;
- create local safe configuration if absent;
- never invent secrets silently;
- install dependencies;
- initialize database;
- run migrations;
- create local bootstrap identity through controlled process;
- validate schemas;
- print next commands.

## 109. Development startup

`make dev` should:

- start canonical dependencies;
- apply safe migrations;
- start API/frontend/workers/adapters;
- verify health;
- print URLs;
- avoid multiple duplicate servers;
- fail if required services are unhealthy.

## 110. Runtime verification after changes

After changes affecting visible UI, templates, static assets, API behavior, workers, or runtime configuration:

1. rebuild/recreate affected services;
2. verify service status;
3. run quick HTTP/API smoke checks;
4. inspect logs for startup errors;
5. hard-refresh the browser;
6. visually verify changed surfaces;
7. verify relevant actions;
8. only then proceed to the next visible integration.

## 111. Toolchain locking

Dependencies and tooling must be locked.

Use:

- backend lockfile;
- frontend lockfile;
- container base image digests or controlled tags;
- schema generator version;
- migration tool version;
- formatter/linter versions.

Updates occur through explicit dependency-change missions.

## 112. Dependency management

Rules:

- smallest necessary dependency set;
- trusted source/registry;
- license and security review;
- exact or controlled versions;
- lockfile changes reviewed;
- no install scripts without review;
- dependency inventory;
- automated vulnerability alerts where available;
- remove unused dependencies.

## 113. Supply-chain controls

Before adding a package/plugin/tool:

- confirm need;
- inspect maintainer/source;
- inspect release history;
- inspect transitive dependencies;
- inspect scripts;
- inspect permissions/network;
- inspect license;
- pin version;
- record approval for high-risk additions;
- add tests;
- add removal plan.

## 114. Coding standards

Code should be:

- typed;
- explicit;
- testable;
- small in responsibility;
- documented at boundaries;
- free from hidden global state;
- deterministic where required;
- safe under duplicate/retry;
- observable;
- accessible in UI.

## 115. Naming conventions

Use domain terminology from `GLO-001`.

Examples:

```text
RunAttempt
ApprovalConsumption
ProviderBinding
ArtifactVersion
SideEffectCertainty
```

Avoid alternate synonyms that create semantic drift.

## 116. Function design

Functions that mutate state should:

- have explicit names;
- receive typed inputs;
- return typed outcomes;
- raise domain errors;
- avoid hidden I/O;
- have transaction boundaries documented;
- expose idempotency/retry behavior.

## 117. Side effects in code

Mark external side effects clearly.

Recommended separation:

```text
plan / normalize / validate
→ persist intent
→ perform effect
→ record result
→ reconcile if uncertain
```

Do not bury external effects inside entity constructors, serializers, or UI hooks.

## 118. Null and unknown handling

Use null only when contract permits.

Prefer controlled fields such as:

```text
state: unknown
source: unavailable
value: null
```

Do not interpret empty string or zero as unknown.

## 119. Time handling

- UTC internally;
- timezone-aware types;
- server clock for authoritative expiry;
- monotonic clock for durations where possible;
- source/recorded times separate;
- no naive datetime values;
- deterministic test clocks.

## 120. Money handling

- decimal values;
- explicit currency;
- no binary float;
- source state;
- pricing version;
- rounding rule;
- estimate versus actual separation.

## 121. Serialization

Serialization must:

- use canonical field names;
- validate enums;
- preserve unknown/source states;
- avoid accidental secret fields;
- version schemas;
- support deterministic hashing;
- reject unsupported breaking versions safely.

## 122. Database repository interfaces

Repositories return domain objects or typed records, not unrestricted ORM query objects.

Repositories should not leak database sessions to controllers.

## 123. ORM use

If an ORM is selected:

- ORM models remain infrastructure concerns;
- domain rules do not depend on lazy loading;
- avoid implicit cross-context relationships;
- control transaction scope;
- avoid hidden queries;
- test generated SQL for scoped access;
- use database constraints.

## 124. Query performance

Every list/search endpoint should define:

- expected cardinality;
- indexes;
- pagination;
- sort;
- filter;
- query plan tests where critical;
- maximum expansion;
- projection freshness.

Avoid unbounded `SELECT *`.

## 125. Cache use

Caches are optional optimizations.

Rules:

- never authority;
- workspace/classification scoped;
- explicit TTL;
- invalidation;
- source/freshness;
- safe fallback;
- no secrets;
- no cross-workspace shared result unless public and approved.

## 126. Error handling

Every boundary translates errors once.

Do not:

- catch and ignore;
- convert every error to 500;
- retry every exception;
- log secrets;
- mark run failed when state is unknown;
- mark cancellation successful without evidence.

## 127. Retry implementation

Retry logic is centralized and policy-driven.

Inputs:

- failure class;
- side-effect certainty;
- idempotency;
- attempts;
- elapsed time;
- budget;
- deadline;
- approval;
- health;
- emergency stop.

No infinite retries.

## 128. Circuit breakers and bulkheads

External integrations may use:

- per-provider circuit breaker;
- bounded concurrency;
- timeout;
- queue isolation;
- separate worker pool;
- health/readiness impact.

A breaker-open state is visible and does not imply permanent failure.

## 129. Reconciliation handlers

Every external-effect integration must implement a reconciliation path.

Examples:

- adapter session;
- provider request;
- Git reference;
- file hash;
- message provider ID;
- calendar event version;
- artifact object;
- backup manifest.

## 130. Test architecture

Tests are organized by purpose, not only by code folder.

Required categories:

```text
unit
property
state-machine
integration
contract
database
concurrency
fault
security
accessibility
e2e
performance
recovery
backup_restore
migration
```

## 131. Unit tests

Unit tests cover:

- value objects;
- state guards;
- risk/effect mapping;
- normalization;
- fingerprinting;
- retry eligibility;
- classification inheritance;
- source/unknown behavior;
- cost calculations.

They do not require network or real providers.

## 132. Property-based tests

Good candidates:

- canonical serialization;
- action fingerprints;
- state-machine forbidden transitions;
- ID/value-object validation;
- path normalization;
- classification maximum;
- money/usage reconciliation;
- event duplicate handling.

## 133. State-machine tests

Generate or enumerate:

- allowed transitions;
- forbidden transitions;
- terminal-state behavior;
- stale/unknown paths;
- cancellation races;
- approval expiry/invalidation;
- artifact lifecycle.

## 134. Integration tests

Integration tests use:

- real transactional database;
- real migrations;
- outbox/inbox;
- local artifact store;
- simulator adapters;
- sandbox fixture;
- API layer;
- no uncontrolled external provider.

## 135. Contract tests

Contracts include:

- API schemas;
- event schemas;
- adapter profiles;
- capability declarations;
- model profiles;
- tool contracts;
- error catalogues;
- generated clients.

Producer and consumer fixtures must agree.

## 136. Concurrency tests

Required scenarios:

- duplicate run create;
- two workers lease one job;
- stale fencing token;
- approval consume race;
- cancel versus completion;
- retry versus late external completion;
- artifact finalization race;
- budget reservation race;
- duplicate/out-of-order event.

## 137. Fault tests

Inject:

- API crash;
- worker crash;
- adapter crash;
- database outage;
- content-store outage;
- event publisher outage;
- consumer failure;
- timeout before/after external acceptance;
- lost heartbeat;
- restore;
- partial artifact upload.

## 138. Security tests

Cover:

- cross-workspace object IDs;
- IDOR;
- auth/session expiry;
- CSRF;
- CORS;
- mass assignment;
- prompt injection boundary;
- tool bypass;
- secret leakage;
- path traversal;
- symlink escape;
- archive traversal;
- malicious preview;
- event forgery/replay;
- approval replay/substitution.

## 139. Accessibility tests

Include:

- automated scanner;
- keyboard journeys;
- screen-reader smoke;
- focus management;
- semantic landmarks;
- accessible names;
- contrast;
- reflow;
- mobile;
- reduced motion;
- accessible diff/approval/artifact views.

Automated accessibility tests are necessary but not sufficient.

## 140. End-to-end tests

Initial E2E scenarios:

1. create workspace;
2. register simulator adapter;
3. create task and snapshot;
4. create/run safe read-only task;
5. monitor lifecycle;
6. retrieve accepted artifact;
7. view receipt;
8. run approval-gated simulated action;
9. reject and revise approval;
10. cancel a long-running run;
11. recover after worker restart;
12. inspect cost and audit.

## 141. Recovery tests

Recovery tests must verify:

- nonterminal run after API restart;
- expired lease;
- outbox backlog;
- consumer inbox preservation;
- unknown side effect;
- pending cancellation;
- approval consumed before crash;
- missing artifact content;
- restored deleted artifact;
- projection rebuild.

## 142. Backup and restore tests

At minimum:

- create representative data;
- create backup;
- verify manifest;
- destroy isolated test environment;
- restore;
- reconcile;
- verify workspace isolation;
- verify consumed approvals remain consumed;
- verify tombstones;
- verify runs do not replay blindly;
- verify integrity.

## 143. Migration tests

CI should test:

- empty database to latest;
- previous supported schema to latest;
- representative data;
- downgrade compatibility only where supported;
- constraint introduction;
- backfill resumption;
- migration checksum;
- application startup.

## 144. Performance tests

Measure:

- common API reads;
- Mission Control aggregate reads;
- run command acceptance;
- event propagation;
- outbox backlog drain;
- approval queue;
- artifact metadata list;
- memory retrieval;
- restore/recovery scan.

Performance targets come from `NFR-001`.

## 145. Test data

Test data must:

- be synthetic;
- contain no real secrets;
- contain no unnecessary personal data;
- include multiple workspaces;
- include high classifications;
- include stale/unknown/conflicted states;
- include malicious fixtures in quarantined test paths;
- be deterministic.

## 146. Golden fixtures

Maintain golden fixtures for:

- canonical hashes;
- approval fingerprints;
- event envelopes;
- API examples;
- adapter messages;
- capability declarations;
- receipts;
- artifact manifests.

Golden changes require review.

## 147. Test isolation

Tests should:

- use isolated databases/schemas;
- use isolated content roots;
- use fake clocks;
- use deterministic IDs when needed;
- clean up;
- avoid port conflicts;
- avoid depending on execution order;
- avoid real provider calls by default.

## 148. Provider integration tests

Real provider tests, if enabled:

- opt-in;
- separate credentials;
- small budget;
- safe data;
- explicit network;
- non-blocking for ordinary local tests unless release gate requires;
- usage/cost recorded;
- no production secrets.

## 149. Code coverage

Coverage is a signal, not the objective.

Stronger gates apply to:

- state transitions;
- approval consumption;
- workspace scope;
- retry/unknown behavior;
- artifact integrity;
- event deduplication;
- cost calculations;
- recovery.

## 150. Static analysis

Recommended gates:

- formatter check;
- linter;
- type checker;
- dependency audit;
- secret scanner;
- schema validation;
- migration check;
- frontend compile/build;
- dead-code/import checks where practical.

## 151. Security scanning

Potential CI scans:

- dependency vulnerabilities;
- secret detection;
- static application security;
- container image;
- license inventory;
- infrastructure configuration;
- generated SBOM.

Findings need severity, owner, exception, and expiry.

## 152. Local preflight

Before starting a mission:

```text
git status
current branch
dependency/toolchain health
database migration state
compose status
baseline tests
working tree cleanliness
```

Do not overwrite unrelated user changes.

## 153. Git workflow

Standing rules:

- one mission per branch/PR;
- do not commit, push, merge, or rewrite history without explicit authorization;
- keep changes scoped;
- do not mix refactor and feature unless necessary;
- preserve user work;
- include tests and docs;
- review generated files;
- no force push;
- no autonomous merge.

## 154. Branch naming

Suggested:

```text
feature/<mission-id>-short-name
fix/<mission-id>-short-name
docs/<mission-id>-short-name
chore/<mission-id>-short-name
```

Final convention may be simplified.

## 155. Commit conventions

When authorized, commits should:

- be focused;
- use clear imperative subject;
- reference mission/document/requirement;
- avoid generated noise;
- include migration and schema changes intentionally;
- not contain secrets;
- not claim tests that were not run.

## 156. Pull-request content

A PR should state:

- problem and scope;
- requirements addressed;
- architecture decisions;
- implementation;
- migrations;
- security/privacy impact;
- tests run and results;
- visual evidence for UI;
- screenshots where safe;
- known limitations;
- rollback/forward-fix;
- follow-up items.

## 157. Review ownership

Required reviewers depend on change:

| Change | Required review |
|---|---|
| Domain lifecycle | Architecture + Quality |
| Auth/permissions/approval | Security + Architecture |
| Data schema/retention | Data + Architecture |
| Adapter/provider/tool | Architecture + Security |
| UI approval/accessibility | Product + UX/Accessibility + Security |
| Backup/restore | Operations + Data |
| Cost/budget | Product + Data |
| Docs/register | Document owner + governance owner |

## 158. Visual verification

Visible frontend changes require:

- actual rendered local application;
- correct current branch/build;
- supported widths;
- interactive action checks;
- loading/empty/error/stale states;
- no global horizontal overflow;
- accessibility basics;
- screenshots or notes;
- user review before next major visual integration.

## 159. Definition of Ready

A mission is ready when:

- scope is explicit;
- source documents/requirements identified;
- dependencies resolved;
- acceptance criteria exist;
- security/data/approval impact assessed;
- test plan exists;
- UI reference exists where applicable;
- migration impact known;
- rollback/recovery considered;
- no contradictory open decision blocks work.

## 160. Definition of Done

A mission is done when:

1. requirements and acceptance criteria are satisfied;
2. domain/API/event contracts remain consistent;
3. tests pass;
4. type/lint/build pass;
5. migrations validate;
6. security and workspace isolation are checked;
7. error, stale, partial, and unknown states are handled;
8. logs/metrics exist;
9. docs are updated;
10. UI is visually verified where applicable;
11. no secrets or mock production state remain;
12. known limitations are recorded;
13. no commit/push/merge occurs without authorization.

## 161. Review checklist — domain

- Are invariants explicit?
- Are transitions guarded?
- Is workspace immutable?
- Are attempts/history append-only?
- Is unknown distinct?
- Are errors stable?
- Are events generated after acceptance?
- Are retries safe?
- Is recovery defined?

## 162. Review checklist — security

- Is authentication required?
- Is authorization scoped?
- Can an agent approve?
- Can content override policy?
- Are paths/network bounded?
- Are secrets references only?
- Are logs redacted?
- Are cross-workspace tests present?
- Are prohibited actions still prohibited?

## 163. Review checklist — data

- Are source and authority states preserved?
- Is classification correct?
- Are versions immutable where required?
- Are timestamps and money safe?
- Are retention/deletion impacts defined?
- Are indexes derived?
- Is lineage/provenance retained?
- Are migrations reversible or forward-fixable?

## 164. Review checklist — async

- Is state committed before publication?
- Is event ID stable?
- Is consumer idempotent?
- Is ordering scope documented?
- Are gaps handled?
- Is dead-letter behavior defined?
- Can replay repeat an effect?
- Are lag and failure observable?

## 165. Review checklist — frontend

- Is state sourced from backend/read model?
- Are loading/empty/partial/stale/error states visible?
- Are actions really connected?
- Are approvals exact?
- Is unknown labelled?
- Is accessibility covered?
- Is responsive behavior verified?
- Is unsafe content isolated?

## 166. Forbidden shortcuts

Do not:

- write directly to run/approval/artifact lifecycle columns;
- mark adapter observation as platform completion;
- retry unknown consequential effects;
- store approval as boolean;
- reuse approval across attempts;
- use one global workspace-unaware repository;
- put business logic in controllers;
- trust client-provided role/workspace;
- store raw secrets;
- execute model-generated shell strings directly;
- preview active files directly;
- treat mocks as persisted data;
- swallow event publication errors;
- assume a lease expiry means no effect;
- set unknown cost to zero;
- set configured model as actual;
- add dependencies without review;
- skip migrations/backups for destructive changes.

## 167. Anti-pattern — boolean approval

Bad:

```text
run.approved = true
```

Required model:

```text
ApprovalRequest
→ immutable human decision
→ validity/fingerprint checks
→ one-time ApprovalConsumption
→ exact RunAttempt
```

## 168. Anti-pattern — generic integration client

Bad:

```text
integration.execute(name, payload)
```

Preferred:

```text
normalized capability
+ typed target
+ effect class
+ policy
+ approval
+ scoped executor
+ receipt
```

## 169. Anti-pattern — generic state update endpoint

Bad:

```text
PATCH /runs/{id}
{ "state": "completed" }
```

Preferred:

```text
command handler
→ invariant checks
→ completion evidence
→ transition
→ outbox event
```

## 170. Anti-pattern — hidden background task

Bad:

```text
HTTP handler starts thread/process after response
```

Preferred:

```text
persist durable job
→ commit
→ worker leases job
→ observable execution
```

## 171. Anti-pattern — mock operational dashboard

Bad:

- local arrays presented as real active runs;
- generated costs presented as provider costs;
- buttons with no action;
- stale static statuses.

Preferred:

- read models from backend;
- clear fixture/demo mode;
- source/freshness;
- functioning commands;
- error and unavailable states.

## 172. Initial implementation phases

Recommended sequence:

```text
Phase 0 — Repository and contract tooling
Phase 1 — Identity, organization, workspace
Phase 2 — Task snapshots and durable run skeleton
Phase 3 — Jobs, workers, outbox/inbox, simulator adapter
Phase 4 — Mission Control operational visibility
Phase 5 — Approval and Tool Gateway
Phase 6 — Artifact lifecycle
Phase 7 — Codex and Hermes adapters
Phase 8 — Model profiles, usage, and cost
Phase 9 — Governed memory
Phase 10 — Audit receipts, backup, restore, recovery
Phase 11 — Pilot hardening
```

## 173. Phase 0 — Repository and contract tooling

Deliver:

- monorepo structure;
- build command facade;
- local Compose;
- database;
- schema package;
- API/event validation;
- formatter/linter/type checker;
- test harness;
- simulator skeleton;
- documentation checks;
- no business feature claim.

Exit gate:

- one command boots;
- health works;
- tests run;
- contracts validate;
- no secrets.

## 174. Phase 1 — Identity and workspace

Deliver:

- local protected identity/session;
- organization;
- workspace;
- membership;
- roles;
- workspace-scoped repositories;
- authorization middleware;
- audit for identity/governance;
- Mission Control login/workspace shell.

Exit gate:

- negative cross-workspace tests;
- revoked membership blocks access;
- no anonymous protected access.

## 175. Phase 2 — Task and run skeleton

Deliver:

- task;
- immutable task snapshot;
- run creation;
- run read model;
- state machine skeleton;
- idempotency;
- optimistic concurrency;
- outbox;
- timeline.

No external agent execution yet.

Exit gate:

- persisted-before-dispatch invariant structurally proven;
- duplicate run create safe;
- terminal transition tests.

## 176. Phase 3 — Durable worker and simulator

Deliver:

- durable jobs;
- worker leases/fencing;
- simulator adapter;
- start/status/events;
- cancellation paths;
- stale/unknown;
- retry eligibility;
- recovery scan.

Exit gate:

- crash/restart tests;
- duplicate event tests;
- stale worker rejected;
- unknown effect blocks retry.

## 177. Phase 4 — Mission Control

Deliver:

- run list/detail;
- state and freshness;
- steps/attempts;
- timeline;
- waiting conditions;
- cancellation;
- recovery indicators;
- responsive/accessibility baseline.

Exit gate:

- all critical states visible;
- no mock production data;
- visual validation at supported widths.

## 178. Phase 5 — Approval and Tool Gateway

Deliver:

- policy decision interface;
- approval request/review/decision;
- fingerprint;
- independence;
- one-time consumption;
- protected simulator tool;
- replay/substitution tests;
- approval UI.

Exit gate:

- concurrent consume has one winner;
- material change invalidates;
- agents cannot approve;
- emergency stop blocks consumption.

## 179. Phase 6 — Artifact lifecycle

Deliver:

- proposal;
- staging;
- immutable versions;
- hashes;
- provenance;
- local protected store;
- validation;
- safe text/basic preview;
- review/acceptance;
- export manifest;
- deletion/tombstone.

Exit gate:

- unsafe fixture blocked;
- version acceptance isolated;
- restore respects deletion;
- cross-workspace content denied.

## 180. Phase 7 — Real adapters

Deliver in separate missions:

```text
Codex adapter
Hermes adapter
```

For each:

- verified capability map;
- conformance profile;
- health/readiness;
- output normalization;
- cancellation truth;
- tool visibility;
- security limits;
- operational runbook.

Do not implement both in one uncontrolled branch.

## 181. Phase 8 — Models, usage, and cost

Deliver:

- logical model profiles;
- provider binding;
- routing;
- explicit fallback;
- configured/actual identity;
- usage events;
- pricing profiles;
- estimates;
- budgets;
- reconciliation.

Exit gate:

- unknown identity/cost visible;
- fallback not silent;
- budget tests.

## 182. Phase 9 — Governed memory

Deliver:

- proposals;
- versions;
- source/authority;
- conflict;
- verification;
- lexical search;
- deletion;
- optional vector proof-of-concept behind feature gate.

Exit gate:

- workspace-first search;
- source visible;
- agent cannot self-verify;
- deletion propagates.

## 183. Phase 10 — Evidence and recovery

Deliver:

- complete/partial receipts;
- audit gaps;
- backup;
- verification;
- restore validation/execution;
- startup recovery;
- projection rebuild;
- operational tools.

Exit gate:

- restore drill passes;
- consumed approvals preserved;
- no blind job replay;
- evidence gaps visible.

## 184. Phase 11 — Pilot hardening

Deliver:

- performance;
- accessibility;
- security review;
- threat closure;
- dependency/supply-chain review;
- backup drill;
- operator guide;
- monitoring;
- pilot support process;
- release candidate.

## 185. First vertical slice

The first recommended vertical slice is:

```text
Authenticated user
→ workspace
→ safe read-only task
→ immutable snapshot
→ durable run
→ simulator adapter
→ run events/status
→ generated text artifact
→ artifact review/acceptance
→ execution receipt
```

This proves the core without consequential external effects.

## 186. Second vertical slice

```text
Task
→ protected simulated file-write proposal
→ policy
→ exact approval
→ one-time consumption
→ sandboxed tool execution
→ artifact/result
→ receipt
```

This proves human control and protected execution.

## 187. Third vertical slice

```text
Codex read/patch/test workflow
→ patch artifact
→ review
→ optional exact commit approval
→ receipt
```

Push and PR creation follow later separate approvals.

Merge remains prohibited.

## 188. Implementation tickets

Each ticket should include:

- requirement IDs;
- affected documents;
- bounded scope;
- domain/API/event changes;
- migrations;
- security impact;
- tests;
- visual validation;
- operational impact;
- acceptance evidence.

## 189. Architecture decision workflow

When an open technology decision blocks implementation:

1. create ADR draft;
2. list options;
3. evaluate product, security, data, operations, quality;
4. prototype if needed;
5. decide;
6. update affected documents/contracts;
7. implement;
8. record consequences.

Do not hide architecture decisions inside a dependency or code pattern.

## 190. Documentation workflow

Implementation changes may require updates to:

- register;
- glossary;
- requirements;
- architecture;
- contracts;
- API/event schemas;
- runbooks;
- developer guide;
- tests/quality gates;
- traceability.

Shared register/index files should be edited by one integration stream.

## 191. Documentation validation

Automated documentation checks should cover:

- YAML front matter;
- document IDs;
- statuses;
- related document references;
- broken links;
- duplicate IDs;
- Mermaid syntax where tooling permits;
- code-block formatting;
- controlled terms;
- requirement-ID uniqueness.

## 192. Traceability in code

Code and tests may reference controlled requirement IDs.

Examples:

```text
RUN-REQ-RR-002
APR-REQ-CO-001
ART-REQ-SP-002
API-REQ-SEC-003
EVT-REQ-DLV-003
```

Avoid excessive comments that merely duplicate code. Use IDs in test names, design notes, or module docs where they aid traceability.

## 193. Generated documentation

Generate, where useful:

- OpenAPI;
- event catalogue;
- schema reference;
- error catalogue;
- CLI help;
- migration inventory;
- adapter conformance report;
- test report;
- build metadata.

Generated docs do not replace controlled human-readable architecture documents.

## 194. Local AI-assisted development

When using Codex or another coding agent:

- provide bounded mission scope;
- provide relevant documents and requirements;
- prohibit unrelated changes;
- prohibit commit/push/merge without authorization;
- require preflight;
- require tests;
- require report of changed files;
- require known limitations;
- require visual verification for UI;
- require no raw secrets or user files in repo.

## 195. Agent prompt structure

Recommended coding-agent prompt sections:

```text
Mission
Repository and branch
Authoritative documents
Scope
Out of scope
Constraints
Implementation steps
Tests
Runtime verification
Reporting format
Git restrictions
```

## 196. Agent change review

Never accept an agent report alone.

Verify:

- actual diff;
- files changed;
- commands/tests;
- runtime;
- visible UI;
- migrations;
- secret leakage;
- mock data;
- unrelated changes;
- Git status.

## 197. Local data safety

Development commands must not:

- delete user repositories;
- operate outside workspace roots;
- overwrite backups;
- reset databases silently;
- remove volumes without confirmation;
- add user files to Git;
- reuse production credentials.

Destructive local commands require explicit naming and confirmation.

## 198. Seed data

Seed data should:

- be synthetic;
- be deterministic;
- represent multiple states;
- represent multiple workspaces;
- include no real secrets;
- be safe to recreate;
- never be confused with production state.

The UI should label demo/fixture environments.

## 199. Development admin account

Bootstrap admin:

- local only;
- forced password/credential setup;
- no default public credential;
- documented rotation/reset;
- no embedded secret;
- auditable.

## 200. Test and development ports

Ports should be:

- configurable;
- documented;
- non-public by default;
- checked for conflicts;
- consistent across commands;
- not assumed to grant security.

## 201. Browser hard refresh and cache

After frontend rebuild:

- verify correct asset version/build identity;
- hard refresh;
- check network errors;
- confirm no stale service worker/cache;
- display safe build/version in diagnostics.

## 202. Build identity

Every component should expose:

- application version;
- commit/build reference where available;
- build time;
- schema versions;
- adapter/runtime version;
- environment profile.

Build identity must not expose secrets.

## 203. Release build

A release build should be:

- reproducible;
- versioned;
- dependency-locked;
- tested;
- schema-validated;
- migration-validated;
- security-scanned;
- documented;
- accompanied by manifest/checksums.

## 204. Release candidate gate

Before pilot release:

- all P0 requirements traced;
- critical/high threats treated;
- no critical residual accepted silently;
- state/recovery tests pass;
- approvals pass replay/race tests;
- artifact preview security passes;
- backup restore passes;
- accessibility blockers resolved;
- operator runbooks exist;
- known limitations published.

## 205. Hotfix workflow

Hotfixes still require:

- scoped branch;
- root-cause note;
- regression test;
- relevant gates;
- no bypass of Git authorization;
- follow-up documentation/cleanup.

Security hotfix may use expedited review but not silent merge.

## 206. Technical debt

Technical debt records should include:

- affected requirements;
- risk;
- reason;
- owner;
- deadline/review;
- workaround;
- test limitations;
- removal plan.

Do not encode debt only as TODO comments.

## 207. Feature completeness

A feature is not complete when only:

- UI exists;
- API route exists;
- adapter returns mock;
- state is not persisted;
- approval is a placeholder;
- error handling is absent;
- tests are absent;
- recovery is absent;
- button has no behavior.

Commercial readiness requires the full bounded workflow.

## 208. Security exception process

A security exception requires:

- exact control;
- reason;
- scope;
- risk;
- compensating controls;
- owner;
- expiry;
- approval;
- evidence;
- removal plan.

No permanent silent exceptions.

## 209. Performance optimization rule

Optimize after:

- correctness;
- observability;
- baseline measurement;
- bottleneck identification.

Do not weaken workspace scoping, transactions, integrity, or evidence for speculative speed.

## 210. Scalability direction

Scale first through:

- bounded queries;
- indexes;
- worker concurrency;
- separate adapter processes;
- projection/read models;
- storage abstraction;
- component metrics.

Do not prematurely introduce distributed complexity without evidence.

## 211. Commercialization readiness path

Future controlled commercialization may require:

- stronger tenant isolation;
- external identity;
- encryption/key management;
- audited deployment;
- service-level objectives;
- support processes;
- billing;
- data-processing/legal controls;
- high availability;
- incident response;
- stronger sandboxing.

These are not implied by local MVP completion.

## 212. Development metrics

Useful engineering metrics:

- lead time;
- deployment frequency in local/pilot context;
- change failure;
- recovery time;
- flaky tests;
- contract drift;
- migration failure;
- security findings;
- accessibility blockers;
- escaped defects;
- unknown/stale run rate;
- restore drill success.

Metrics should guide improvement, not reward unsafe velocity.

## 213. Developer onboarding

Onboarding should cover:

- product purpose;
- workspace/security model;
- document hierarchy;
- repository;
- local startup;
- test commands;
- domain invariants;
- Git restrictions;
- secret handling;
- adapter simulator;
- first safe change;
- review process.

## 214. Developer environment checklist

- repository in Linux filesystem;
- Git configured;
- Docker available;
- supported runtime/toolchain;
- `.env` safe and ignored;
- no real secrets;
- database healthy;
- migrations current;
- contract validation passes;
- baseline tests pass;
- browser access works;
- simulator healthy.

## 215. Troubleshooting order

When local runtime fails:

1. verify branch and working tree;
2. verify environment file;
3. verify containers/processes;
4. verify health endpoints;
5. inspect bounded logs;
6. verify database/migrations;
7. verify ports;
8. verify adapter readiness;
9. run smoke test;
10. rebuild only affected services;
11. avoid destructive reset unless explicitly justified.

## 216. Reset procedures

Provide separate commands for:

```text
reset test data
reset development database
reset derived indexes
reset staging content
```

Do not combine them with:

```text
delete all backups
delete source files
delete user repositories
```

Reset commands must print affected paths/resources.

## 217. Backup before destructive local operations

Before destructive migration, volume removal, or database reset:

- offer/create backup;
- verify target;
- record timestamp;
- print restore command;
- avoid overwriting prior backup.

## 218. Open-source and licensing

Track:

- dependency licenses;
- model licenses;
- tool/adapter licenses;
- generated asset rights;
- external API terms.

License incompatibility is a release blocker where applicable.

## 219. Privacy by development

Developers should use:

- synthetic data;
- minimized fixtures;
- redacted diagnostics;
- bounded retention;
- safe screenshots;
- controlled exports;
- no real conversation content in tests unless explicitly governed.

## 220. Developer security responsibilities

Every contributor must:

- protect credentials;
- avoid unreviewed dependencies;
- report suspected secret exposure;
- preserve workspace scope;
- run required tests;
- avoid bypasses;
- document unknowns;
- not claim unverified safety or completeness.

## 221. Architecture fitness functions

Automated or semi-automated checks should verify:

- no domain import from web framework;
- no adapter/provider SDK import in domain;
- no raw secret fields in schemas;
- workspace fields present on protected aggregates;
- event schemas include classification/correlation;
- approval consumption unique;
- run attempts append-only;
- API has no generic lifecycle-state patch;
- cross-module dependency rules;
- generated contracts current.

## 222. Repository policy checks

Potential checks:

- forbidden paths/files;
- secrets;
- large binaries;
- user-uploaded files;
- untracked generated changes;
- missing migration;
- lockfile mismatch;
- documentation references;
- no direct edits to generated contracts.

## 223. Quality ownership

| Area | Owner |
|---|---|
| Domain correctness | Architecture Owner |
| Product acceptance | Product Owner |
| Security controls | Security Owner |
| Data semantics | Data Owner |
| Runtime/operations | Operations Owner |
| Test strategy/gates | Quality Owner |
| Accessibility | UX/Accessibility Owner or assigned reviewer |
| Adapter implementation | Adapter owner |
| Shared contracts | Architecture + Data + Quality |

## 224. ADR backlog

### `ADR-TBD-DEV-001 — Backend framework and language profile`

Select the server framework, language/runtime support policy, dependency management, and application structure.

### `ADR-TBD-DEV-002 — Frontend framework and component system`

Select frontend framework, routing, state/query approach, component library, and accessibility strategy.

### `ADR-TBD-DEV-003 — Database/job/event implementation`

Select relational database, migration tool, job mechanism, outbox/inbox implementation, and future broker path.

### `ADR-TBD-DEV-004 — Local artifact storage and preview toolchain`

Select local store, object-key layout, hash profile, preview/conversion tools, and sandbox.

### `ADR-TBD-DEV-005 — Local authentication and secrets`

Select bootstrap identity, session mechanism, credential storage, secret-reference implementation, and reauthentication.

### `ADR-TBD-DEV-006 — Repository build and test tooling`

Select monorepo tooling, command facade, CI jobs, code generation, and release packaging.

## 225. Open decisions

1. Which backend framework and runtime?
2. Which frontend framework and component system?
3. Which relational database?
4. Which migration tool?
5. Which job/outbox implementation?
6. Is a broker deferred or included?
7. Which local authentication profile?
8. Which secret-reference backend?
9. Which artifact store?
10. Which preview converters/scanners?
11. Which sandbox mechanism?
12. Which local model/provider clients?
13. Which adapter transport?
14. Which schema technology?
15. Which API/event generators?
16. Which monorepo/build tooling?
17. Which test runner and browser automation?
18. Which accessibility tooling?
19. Which container base images?
20. Which supported host environments?
21. Which CI platform and gates?
22. Which packaging/distribution profile?
23. Which code ownership rules?
24. Which minimum vertical slice enters first?
25. Which P1 plugin architecture work is deferred?

## 226. Risks

| Risk | Consequence | Response |
|---|---|---|
| Framework leaks into domain | Lock-in and poor testing | Ports/layers |
| Modular monolith becomes global blob | Extraction and ownership failure | Context boundaries |
| Broker introduced too early | Operational complexity | DB-backed first |
| Generic CRUD bypasses lifecycle | Invalid state | Commands/aggregates |
| Adapter runs in API process | Crash/permission coupling | Separate process |
| Mock UI presented as real | False readiness | Connected backend/state labels |
| Unknown coerced to success | Unsafe decisions | Controlled states |
| Worker lease lacks fencing | Stale writes | Monotonic token |
| External effect inside DB transaction | Long locks/uncertain commit | Persist intent first |
| Secrets in environment/logs | Credential exposure | References/redaction |
| Local file store leaks paths | Host exposure | Storage abstraction |
| Preview executes content | Compromise | Isolated derived preview |
| Vector search before governance | Leakage/poor quality | Relational/lexical baseline |
| Migrations destructive early | Data loss | Expand/contract |
| AI agent changes too much | Regression | Bounded missions/review |
| Dependency sprawl | Supply-chain risk | Review/lock/inventory |
| UI built before backend workflow | Dead buttons/mocks | Vertical slices |
| Tests rely on provider | Flaky/costly | Simulator/default offline |
| Restore not tested | False backup confidence | Restore drills |
| Git automation merges | Loss of human control | Explicit prohibition |

## 227. Assumptions

- the first implementation is local Linux/WSL;
- a small team can maintain a monorepo;
- a relational database and Docker are available;
- backend and frontend can share generated contracts;
- adapters can run as separate processes;
- a simulator can model failure paths;
- controlled local storage is available;
- CI can run database/browser/container tests;
- documentation remains available during implementation;
- Product, Architecture, Security, Data, Operations, and Quality owners can review major decisions.

## 228. Constraints

- no final technology selection in this draft;
- no public anonymous access;
- no production or financial actions;
- no autonomous Git merge, force push, or history rewrite;
- no raw secrets;
- no unrestricted host/network;
- no direct client lifecycle mutation;
- no adapter or model approval authority;
- no accepted mock operational state;
- no destructive migration without backup and approval;
- no commit, push, PR, or merge without separate authorization during current documentation phase;
- Git versioning remains deferred until all documents and consistency review are complete.

## 229. Acceptance criteria

DEV-001 may advance to `1.0.0` when:

1. Product accepts the phased implementation and vertical slices.
2. Architecture accepts repository, modules, layers, transactions, workers, adapters, and dependency direction.
3. Security accepts local environment, secrets, sandbox, network, supply-chain, and review controls.
4. Data accepts database, migrations, classification, artifact, memory, audit, and cost implementation rules.
5. Operations accepts Docker/WSL, startup, health, backup, recovery, and troubleshooting workflows.
6. Quality accepts test categories, gates, Definition of Ready, Definition of Done, and review checklists.
7. framework choices are recorded through ADRs;
8. a canonical repository command interface is approved;
9. the first two vertical slices are implementable without semantic gaps;
10. workspace isolation is enforced structurally and tested;
11. persist-before-effect and outbox/inbox patterns are implementable;
12. approval and artifact controls are preserved;
13. UI cannot present mocks as production state;
14. backup/restore and recovery are part of development, not deferred indefinitely;
15. `TST-001`, `QAG-001`, `OBS-001`, `OPS-001`, and `BCP-001` can proceed.

## 230. Downstream impact

| Document | Required use |
|---|---|
| `TST-001` | Formalize the complete verification strategy and test suites |
| `QAG-001` | Define release gates and evidence |
| `OBS-001` | Define logs, metrics, traces, alerts, and dashboards |
| `OPS-001` | Define startup, maintenance, incident, recovery, and support runbooks |
| `BCP-001` | Define backup, restore, continuity, and disaster recovery |
| `PLG-001` | Future plugin/extension implementation model |
| `RTM-001` | Trace development rules to tests and evidence |

## 231. Revision and approval history

### Approval state

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial development and implementation guide covering repository structure, modular architecture, database transactions, outbox/inbox, workers, adapters, frontend, artifacts, memory, security, configuration, Docker/WSL, migrations, testing, Git workflow, quality gates, vertical slices, and phased implementation |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SAD-001` — System Architecture Description
- `DDD-001` — Domain Model
- `DAT-001` — Data Architecture
- `ORC-001` — Workflow and Orchestration Architecture
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `AGC-001` — Agent Adapter Contract
- `CAP-001` — Agent Capability Schema
- `MOD-001` — Model Profile Contract
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `API-001` — API Specification
- `EVT-001` — Event Catalog and Async Contract
