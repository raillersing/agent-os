---
document_id: AUD-001
title: Agent OS Audit and Evidence Architecture
version: 0.2.0
status: draft
register_status: proposed_unregistered
owner: security-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-07-20
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents: []
dependencies:
  - SEC-001
  - THR-001
  - IAM-001
  - POL-001
  - RUN-001
  - APR-001
  - EVT-001
  - DAT-002
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
  - CST-001
  - ADP-HER-001
  - ADP-CDX-001
related_adrs:
  - ADR-TBD-AUD-001
  - ADR-TBD-AUD-002
  - ADR-TBD-AUD-003
  - ADR-TBD-AUD-004
  - ADR-TBD-AUD-005
  - ADR-TBD-AUD-006
  - ADR-TBD-AUD-007
  - ADR-TBD-AUD-008
---

# AUD-001 — Agent OS Audit and Evidence Architecture

> **Status: Draft — proposed/unregistered.** This document defines the proposed audit and evidence architecture for Agent OS. It covers audit events, actor chains, decision and execution evidence, receipts, timelines, integrity, append-only direction, evidence packages, exports, retention, holds, deletion treatment, investigations, incident forensics, recovery validation, access control, APIs, events, operations, tests, and release gates. It does not claim legal non-repudiation, select a final immutable-log or ledger technology, permit raw secrets in audit, or replace operational logs, application data, or legal advice.

## 1. Purpose

Agent OS coordinates humans, agents, adapters, models, tools, policies, approvals, sandboxes, artifacts, data, and external systems. A trustworthy platform must be able to reconstruct:

1. who or what acted;
2. under which identity and session;
3. in which organization, workspace, and environment;
4. which policy and approval applied;
5. which model, adapter, tool, and sandbox were involved;
6. what was requested;
7. what was observed;
8. what effect was confirmed, partial, unknown, or denied;
9. which evidence supports the claim;
10. whether the evidence remains complete and trustworthy.

The audit architecture provides durable, access-controlled evidence without treating ordinary logs as proof by default.

## 2. Objectives

The architecture must:

- make consequential actions attributable;
- preserve human, agent, adapter, workload, and support identities separately;
- record organization, workspace, environment, run, step, and attempt scope;
- bind decisions to policy, attributes, approvals, and exact targets;
- bind executions to tools, sandboxes, resources, secrets, and effect certainty;
- preserve receipts and external confirmations;
- support trustworthy timelines;
- detect evidence gaps, tampering, and ordering uncertainty;
- support investigations and controlled exports;
- support retention, holds, minimization, and lifecycle controls;
- preserve negative facts after restore;
- support local-first, pilot, and controlled-commercial maturity;
- remain provider-neutral and storage-technology-neutral.

## 3. Non-goals

AUD-001 does not:

- claim legal non-repudiation;
- make all data immutable forever;
- permit raw secrets, passwords, tokens, or private keys in evidence;
- store complete prompts or artifacts merely for convenience;
- replace business-domain records;
- replace operational metrics, logs, or traces;
- replace incident-response procedures;
- select a final ledger, WORM, database, object store, hash-chain, or signing solution;
- guarantee complete evidence from external providers that expose no receipts;
- authorize unbounded audit access;
- define final statutory retention periods.

## 4. Principle — Evidence is purpose-built

Audit evidence is designed for accountability and verification, not copied wholesale from application logs.

## 5. Principle — Actor chains remain explicit

Human, service, agent, adapter, workload, support, and external identities are never collapsed into one actor.

## 6. Principle — Workspace scope is mandatory

Every workspace-scoped event carries an authoritative workspace reference before storage or retrieval.

## 7. Principle — Decision and effect are separate

A policy permit, approval, command dispatch, process exit, and external effect are distinct evidence facts.

## 8. Principle — Unknown remains unknown

Missing receipt, conflicting source, stale state, or lost event cannot be presented as confirmed success.

## 9. Principle — Append, do not rewrite

Material audit facts are appended or superseded rather than silently edited.

## 10. Principle — Corrections preserve history

Corrections reference the original record, explain the change, and retain both states.

## 11. Principle — Secrets are referenced, not recorded

Audit stores secret references, purposes, and access outcomes without raw values.

## 12. Principle — Evidence is minimized

Record enough to prove the action without duplicating unrestricted personal or confidential content.

## 13. Principle — Time has multiple meanings

Occurred, observed, received, recorded, and effective times remain distinct.

## 14. Principle — Evidence integrity is verifiable

Critical evidence has hashes, signatures, sequence controls, or equivalent verification appropriate to maturity.

## 15. Principle — Audit access is itself audited

Viewing, exporting, redacting, holding, or deleting evidence creates additional evidence.

## 16. Audit bounded context

The Audit bounded context owns:

- audit-event schemas;
- evidence records;
- actor chains;
- event sequencing;
- evidence packages;
- receipts;
- integrity metadata;
- audit timelines;
- evidence access records;
- export records;
- audit holds;
- audit reconciliation;
- evidence health;
- verification results.

It does not own authoritative business state, authentication state, policy logic, run state, artifact content, or backup orchestration.

## 17. Core distinction

```text
operational log
≠ audit event
≠ trace span
≠ business record
≠ evidence package
≠ external receipt
```

These may reference one another but serve different purposes.

## 18. Audit event

An audit event records one consequential fact or observation, including:

- event ID;
- event type and schema version;
- actor chain;
- organization/workspace/environment;
- object and action;
- result;
- occurred/observed/recorded time;
- source component;
- correlation and causation;
- policy/approval/run references;
- safe metadata;
- integrity metadata;
- classification and retention profile.

## 19. Evidence record

An evidence record is a structured proof element supporting a claim.

Examples:

- a policy decision;
- an approval decision;
- a sandbox specification hash;
- a tool-call receipt;
- an artifact hash;
- a Git commit hash;
- a provider response reference;
- a backup verification report;
- a restore validation result;
- a visual validation evidence set.

## 20. Evidence package

An evidence package groups the minimum proofs needed to verify a lifecycle or decision.

Examples:

```text
run evidence package
approval evidence package
artifact acceptance package
export evidence package
deployment evidence package
restore evidence package
incident evidence package
security-control evidence package
```

## 21. Receipt

A receipt is a structured confirmation from an authoritative internal or external actor that an action, request, or effect reached a specific state.

A receipt may confirm:

- request accepted;
- effect completed;
- effect partially completed;
- effect rejected;
- provider deletion requested;
- provider deletion confirmed;
- export delivered;
- backup verified;
- Git commit created;
- remote push accepted.

A receipt must not be inferred merely from process exit.

## 22. Timeline

A timeline is an ordered, evidence-linked view of relevant events. It may contain gaps, conflicts, late arrivals, and uncertain ordering.

A timeline must never hide:

- missing intervals;
- source disagreement;
- stale state;
- reordered events;
- duplicate suppression;
- correction events;
- unknown effects.

## 23. Audit subject taxonomy

```text
human_principal
service_principal
workload_identity
agent_profile
adapter_runtime
sandbox_instance
tool_gateway
model_profile
provider
workspace
organization
run
step
attempt
approval
artifact
memory
policy
secret_reference
export
backup
restore
incident
security_control
```

## 24. Actor chain

The actor chain records all relevant actors without collapsing them.

Example:

```text
human requester
→ logical agent profile
→ adapter runtime
→ sandbox workload identity
→ Tool Gateway
→ external provider
```

Each hop has its own identity, authority, and evidence.

## 25. Actor-chain fields

Potential fields:

- initiating principal;
- delegated authority source;
- support or break-glass context;
- logical agent profile;
- adapter registration and runtime;
- sandbox workload identity;
- tool executor;
- model/provider;
- target system;
- impersonation or simulation marker;
- chain completeness.

## 26. Real actor preservation

Support access, delegated access, break-glass, and simulation must preserve the real human actor.

Impersonation, where ever allowed, cannot replace the actor with the impersonated user in audit.

## 27. Anonymous and unknown actors

Protected actions cannot use anonymous actors. When a source cannot establish an actor:

- record `unknown_actor`;
- mark the event incomplete;
- block protected effect where appropriate;
- alert or reconcile;
- never invent a human identity.

## 28. Organization, workspace, and environment scope

Every event records:

- organization where applicable;
- authoritative workspace;
- environment;
- deployment/build identity;
- source service instance;
- region or execution location where relevant.

Cross-workspace retrieval of audit evidence is denied by default.

## 29. Object and action model

Audit actions should use controlled identifiers:

```text
identity.authenticate
membership.activate
role.assign
policy.evaluate
policy.activate
approval.request
approval.decide
run.create
attempt.start
tool.invoke
artifact.accept
memory.verify
export.create
secret.lease
sandbox.violation
backup.verify
restore.complete
emergency_stop.activate
```

## 30. Outcome vocabulary

```text
requested
accepted
denied
blocked
started
completed
partially_completed
failed
cancelled
expired
revoked
quarantined
unknown
reconciliation_required
```

The event outcome must reflect the fact being recorded, not an optimistic interpretation.

## 31. Effect certainty

For protected effects:

```text
not_started
confirmed_no_effect
effect_confirmed
effect_partially_confirmed
effect_unknown
reconciliation_required
```

Effect certainty remains separate from command status.

## 32. Time semantics

Audit distinguishes:

- `occurred_at` — when the source says the action happened;
- `observed_at` — when a component observed it;
- `received_at` — when the audit pipeline received it;
- `recorded_at` — when durable storage committed it;
- `effective_at` — when a policy, grant, hold, or lifecycle state became effective.

Clock source and skew state are recorded where relevant.

## 33. Clock health

Security-relevant services should expose clock synchronization health.

When clock skew exceeds the approved threshold:

- record the skew;
- mark ordering confidence;
- alert;
- avoid unsupported precise ordering;
- rely on sequence/causation where available.

## 34. Event identifiers

Identifiers should be:

- globally unique or unique within a defined partition;
- stable;
- non-secret;
- sortable only if that does not create privacy or information leakage;
- independent from mutable display labels.

Audit event IDs are never reused.

## 35. Correlation and causation

Audit events may record:

- correlation ID;
- causation event ID;
- request ID;
- idempotency key reference;
- run/step/attempt;
- command/tool-call ID;
- approval ID;
- policy-decision ID;
- trace ID;
- external receipt reference.

Causation should not be inferred solely from timestamp proximity.

## 36. Schema versioning

Audit schemas are versioned and backward-readable according to an approved compatibility policy.

Schema changes define:

- added/removed/renamed fields;
- semantic changes;
- classification changes;
- retention impact;
- migration/reader compatibility;
- validation;
- consumer impact.

## 37. Event validation

Before acceptance, validate:

- schema;
- required identifiers;
- workspace and environment;
- actor-chain shape;
- timestamp format;
- controlled action/result values;
- classification;
- size limits;
- prohibited secret fields;
- integrity metadata;
- source authorization.

Invalid events are quarantined or rejected with evidence.

## 38. Event source identity

Every source service, adapter, executor, and gateway that emits protected audit events uses an authenticated workload identity and authorized schema set.

A client browser cannot directly assert an authoritative backend audit event.

## 39. Audit ingestion

A directional ingestion flow:

```text
source component
→ local durable outbox or transactional write
→ authenticated audit ingestion
→ schema and policy validation
→ durable append
→ integrity update
→ projection/index
→ monitoring and evidence availability
```

## 40. Transactional outbox direction

Where audit corresponds to an authoritative state change, the business state and an outbox record should commit atomically or through an equivalent consistency mechanism.

This reduces the chance of state changes without evidence.

## 41. At-least-once delivery

Audit ingestion may be at-least-once. Therefore:

- event IDs are idempotent;
- duplicates are detected;
- original arrival attempts may be recorded;
- duplicate suppression does not hide conflicting payloads;
- the first valid durable event remains authoritative unless corrected.

## 42. Duplicate events

Exact duplicates may be safely collapsed in projections while retaining ingestion diagnostics.

Same event ID with different material content is an integrity incident.

## 43. Late events

Late-arriving events are appended with original occurred/observed time and current recorded time. Timelines update visibly and indicate the late arrival.

Late arrival does not rewrite earlier evidence.

## 44. Event gaps

Sequence gaps, missing causation references, stalled outboxes, or expected-event absence create explicit evidence-health findings.

The platform must not silently fabricate missing events.

## 45. Corrections

Corrections are appended as new events that reference:

- original event;
- corrected fields;
- reason;
- correcting actor;
- authority;
- timestamp;
- approval if required.

The original event remains available to authorized reviewers.

## 46. Redactions

Redaction of audit content is exceptional and must preserve:

- original record integrity reference;
- redaction reason;
- redacting actor;
- fields affected;
- legal/security authority;
- effective time;
- access to original only for approved roles where retention permits.

Redaction cannot falsify actor, action, outcome, or effect certainty.

## 47. Deletion treatment

Audit deletion follows `DAT-002`.

Preferred strategies:

- minimize at creation;
- store references instead of payloads;
- expire by approved retention profile;
- redact or pseudonymize selected fields;
- retain non-sensitive event facts when justified;
- preserve deletion evidence;
- avoid silently erasing accountability.

Deletion must not claim that an action never occurred when historical evidence is legitimately retained.

## 48. Classification

Audit data is classified according to content and aggregation risk.

Typical direction:

- ordinary operational audit: `C2`;
- identity, approval, security, support, export, and provider details: `C3`;
- raw secret material: prohibited;
- public release evidence: only after explicit sanitization and approval.

## 49. Retention profiles

Audit retention uses the profiles defined in `DAT-002`, commonly `R4` for security/audit evidence and `R5` for holds.

Final periods depend on product, security, contractual, and legal review.

## 50. Audit holds

Audit holds may apply for:

- security incidents;
- disputes;
- recovery investigations;
- control failures;
- customer cases;
- release investigations.

A hold is scoped, owned, time-reviewed, access-controlled, and released through governance.

## 51. Data minimization

Audit should prefer:

- IDs and hashes;
- classification;
- sizes/counts;
- reason codes;
- exact target references;
- policy/approval versions;
- receipts;
- validation results;
- safe summaries.

Avoid full prompts, model output, files, source code, emails, personal profiles, and HTTP bodies unless the evidence purpose truly requires them.

## 52. Secret handling

Prohibited in audit:

- passwords;
- bearer tokens;
- API keys;
- recovery codes;
- private keys;
- full session identifiers;
- secret plaintext;
- unredacted authorization headers.

Record secret reference, purpose, lease ID, result, expiry, and revocation status instead.

## 53. Personal data

Audit may include personal identifiers necessary for attribution. It should minimize display data, use stable principal IDs, restrict access, and separate searchable profile information from durable event attribution.

## 54. Prompt and model evidence

When model interaction is consequential, evidence may record:

- model profile;
- provider/model identity source;
- prompt/context fingerprint;
- classification;
- token/usage measurements;
- policy route;
- output fingerprint;
- validation status;
- safety or fallback state.

Full prompt/output retention is not required by default.

## 55. Policy-decision evidence

A policy-decision evidence record contains:

- decision ID;
- principal/session;
- organization/workspace;
- action/resource;
- policy set and versions;
- rule IDs;
- attribute-source references and versions;
- result;
- reason codes;
- obligations;
- approval requirement;
- expiry;
- cache status;
- enforcement reference.

Raw attributes are minimized.

## 56. Approval evidence

Approval evidence contains:

- request ID;
- requester;
- eligible approver and actual approver;
- independence evaluation;
- exact material fingerprint;
- target;
- risk and effect class;
- policy version;
- decision;
- reason/comment;
- expiry;
- invalidation;
- consumption;
- reauthentication assurance;
- subsequent execution linkage.

## 57. Run evidence

A run evidence package may contain:

- task snapshot;
- run ID;
- plan/version;
- assigned agent/adapter/model;
- policy decisions;
- approvals;
- steps and attempts;
- state transitions;
- retries/cancellations;
- artifacts;
- tool calls;
- costs;
- unknown effects;
- reconciliation;
- completion basis.

## 58. Attempt evidence

Each attempt records:

- attempt ID and ordinal;
- parent run/step;
- execution identity;
- profile/sandbox;
- inputs;
- command/tool;
- start/stop;
- result;
- effect certainty;
- outputs;
- limits;
- violations;
- cleanup;
- retry relationship.

Attempts are never overwritten by later retries.

## 59. Sandbox evidence

Sandbox evidence includes immutable specification hash, profile, runtime digest, mounts, network policy, resource limits, secret-lease references, process lifecycle, violations, outputs, validation, and cleanup.

Detailed requirements align with `SAN-001`.

## 60. Tool-call evidence

Tool evidence includes:

- tool and version;
- caller identity;
- workspace;
- target;
- structured argument fingerprint;
- policy and approval;
- idempotency key reference;
- dispatch and response time;
- result;
- effect certainty;
- receipt;
- errors;
- retries;
- reconciliation.

## 61. External receipt evidence

External receipts should preserve:

- external system/provider;
- external request/correlation ID;
- target;
- response status;
- receipt body fingerprint;
- received time;
- authenticity/validation state;
- interpretation;
- limitations;
- classification.

Raw provider payloads are stored only when justified.

## 62. Artifact evidence

Artifact evidence includes:

- artifact/version ID;
- content hash;
- source run/attempt;
- inputs;
- generator/tool/model;
- validation;
- classification;
- quarantine;
- acceptance/rejection;
- export;
- deletion/tombstone;
- preview derivation.

The audit record usually references content rather than duplicating it.

## 63. Memory evidence

Memory evidence includes proposal source, content fingerprint, citations, authority, verification, conflicts, freshness, classification, embedding/index lineage, use in prompts, and deletion.

## 64. Identity and access evidence

IAM evidence includes authentication outcomes, session creation/rotation/revocation, invitations, membership and role changes, grants/delegations, support access, recovery, identity linking, and break-glass.

## 65. Security-control evidence

`SEC-002` control evidence may include test reports, configuration checks, scan results, review decisions, runbook exercises, incident drills, and release-gate decisions.

Control status is not marked verified solely because an automated job ran.

## 66. Cost and budget evidence

Proposed/unregistered `CST-001` should produce evidence for estimates, reservations, usage, pricing versions, attribution, budget decisions, threshold approvals, unknown cost, and reconciliation.

## 67. Deployment evidence

Deployment evidence may contain:

- source revision;
- artifact/image digest;
- environment;
- configuration version;
- migration;
- policy/profile versions;
- deployment actor;
- start/health validation;
- smoke tests;
- visual validation;
- rollback reference;
- release decision.

## 68. Backup evidence

Backup evidence includes:

- backup ID;
- scope;
- source;
- time;
- classification;
- encryption reference;
- size/count;
- integrity verification;
- destination;
- retention;
- owner;
- access;
- restore-test linkage.

A completed backup job is not a verified backup unless validation evidence exists.

## 69. Restore evidence

Restore evidence includes:

- selected restore point;
- authorization and reason;
- environment;
- integrity checks;
- schema/migration;
- negative-fact reapplication;
- identity/session handling;
- audit reconciliation;
- index/embedding rebuild;
- provider/export reconciliation;
- progressive service enablement;
- validation and sign-off.

## 70. Incident evidence

Incident evidence includes alerts, detection source, actor chain, timeline, affected scope, containment, credentials revoked, artifacts, indicators, decisions, communications, recovery, impact, and post-incident actions.

Access is highly restricted and all access is audited.

## 71. Visual-validation evidence

`VVR-001` evidence sets may be registered as audit-relevant release evidence with:

- scenario IDs;
- build/environment;
- routes;
- viewports/themes;
- captures/diffs;
- findings;
- reviewer decisions;
- exceptions;
- hashes;
- retention.

## 72. Evidence integrity levels

Proposed levels:

```text
E0 — ordinary record
E1 — validated structured record
E2 — hash-protected evidence
E3 — chained or signed evidence
E4 — independently anchored or externally witnessed evidence
```

The level depends on risk and maturity. No legal conclusion is implied.

## 73. Hashing

Hashing may protect:

- event payloads;
- evidence files;
- manifests;
- artifact content;
- policy versions;
- sandbox specifications;
- visual captures;
- export bundles.

Use approved algorithms and store algorithm/version metadata.

## 74. Hash chains

A hash-chain direction may link ordered events within a partition or evidence bundle.

Design must address:

- partitions;
- concurrency;
- late events;
- corrections;
- checkpointing;
- archival;
- verification;
- recovery;
- chain gaps.

Final use requires ADR.

## 75. Digital signatures

Signing may be used for release manifests, provider receipts, evidence bundles, policy versions, or audit checkpoints.

Key ownership, rotation, revocation, timestamping, and verification are required. Signing does not make false content true.

## 76. External anchoring direction

Future commercial assurance may anchor selected checkpoints to an independent service or medium. This is optional and must be evaluated for privacy, availability, cost, and legal meaning.

## 77. Append-only direction

Critical audit stores should prevent ordinary application roles from updating or deleting existing events.

Administrative maintenance and lifecycle jobs use separate governed interfaces and produce their own audit.

## 78. Audit-store access

Access is based on:

- principal and session assurance;
- organization/workspace;
- role;
- purpose;
- classification;
- incident/support context;
- hold;
- export;
- time range;
- field-level restrictions.

Search permission does not automatically imply payload export.

## 79. Field-level protection

Sensitive audit fields may require:

- masking;
- separate encrypted columns/objects;
- stricter role;
- reauthentication;
- reason;
- access logging;
- no bulk export.

Examples include support details, incident indicators, network identifiers, and provider account references.

## 80. Audit access evidence

Record:

- viewer/exporter;
- workspace/scope;
- query/time range;
- reason;
- fields accessed;
- records returned;
- export status;
- approval;
- time;
- client/session;
- subsequent deletion of temporary export.

## 81. Search architecture

Audit search should support:

- event ID;
- actor;
- workspace;
- run/attempt;
- approval;
- artifact;
- policy decision;
- tool call;
- receipt;
- time range;
- action/outcome;
- incident/control reference.

Search indexes are derived and rebuildable.

## 82. Search authorization

Authorization is applied before query and before result expansion.

Counts, facets, suggestions, and autocomplete must not leak data from unauthorized workspaces or classifications.

## 83. Search freshness

Search results display index freshness and known gaps. Critical investigations may query the authoritative store or use a verified export when the projection is stale.

## 84. Audit timeline UX

A timeline should display:

- actor chain;
- action;
- target;
- result;
- certainty;
- source;
- occurred and recorded times;
- policy/approval;
- evidence links;
- corrections;
- gaps;
- late arrivals;
- conflicts.

Unknown and partial states must be visually distinct.

## 85. Decision explorer

Authorized reviewers can inspect:

- request summary;
- policy decision;
- approval;
- execution;
- effect receipt;
- evidence completeness;
- integrity state;
- timeline;
- unresolved findings.

The explorer does not expose raw secret or unrestricted content.

## 86. Evidence package viewer

The viewer should show:

- package purpose and scope;
- included records/files;
- hashes and verification;
- classification;
- missing evidence;
- external receipts;
- retention and hold;
- export eligibility;
- reviewer decision.

## 87. Audit export

Audit exports require:

- authorized requester;
- exact workspace/time/object scope;
- purpose;
- classification;
- field selection;
- redaction;
- approval where required;
- encrypted destination;
- expiry;
- receipt;
- export-access logging.

## 88. Export formats

Potential formats:

```text
JSON/JSONL for machine verification
CSV for bounded tabular review
PDF for human-readable approved reports
signed manifest plus evidence files
```

No format is automatically complete for every investigation.

## 89. Export manifest

An export manifest records:

- export ID;
- query/scope;
- event count;
- included schema versions;
- file list;
- hashes;
- classification;
- redactions;
- requester/reviewer;
- generated time;
- expiry;
- integrity method;
- known gaps.

## 90. Temporary audit exports

Temporary evidence bundles and downloads use short-lived access, scoped authorization, encryption where appropriate, download limits, and automatic deletion.

## 91. Chain of custody direction

For incident or external-review evidence, custody records may include:

- collector;
- collection time;
- source;
- method;
- hash;
- storage location;
- transfers;
- access;
- transformations;
- export;
- destruction.

This supports integrity but is not a legal conclusion by itself.

## 92. Investigation case

An investigation case can group:

- case ID;
- owner;
- purpose;
- scope;
- authorized reviewers;
- holds;
- queries;
- evidence packages;
- findings;
- decisions;
- exports;
- closure and retention.

Case access is narrower than ordinary workspace administration.

## 93. Investigation timeline

Investigations preserve both the event timeline and the investigation-action timeline. Reviewer notes are distinguished from authoritative system facts.

## 94. Evidence annotations

Annotations may add context but cannot alter original records.

They record author, time, type, content, classification, and relationship to evidence.

## 95. Evidence conflicts

When sources disagree:

- retain each source;
- record source authority;
- show conflict;
- avoid choosing a favorable answer without justification;
- initiate reconciliation;
- record the resolution as a new fact.

Conflicted evidence cannot support an unqualified success claim.

## 96. Evidence completeness

A package may be:

```text
complete
complete_with_declared_limitations
partial
incomplete
conflicted
unknown
```

Completeness is assessed against a package-specific checklist.

## 97. Evidence health

Monitor:

- outbox backlog;
- ingestion errors;
- schema rejection;
- duplicate conflicts;
- sequence gaps;
- clock skew;
- delayed events;
- integrity verification failures;
- storage saturation;
- index staleness;
- export failures;
- hold/retention anomalies;
- unauthorized access attempts.

## 98. Audit pipeline operational states

```text
healthy
degraded
ingestion_delayed
projection_stale
read_only
no_new_evidence
integrity_at_risk
recovery
unknown
```

Protected actions may be blocked when required evidence cannot be recorded.

## 99. Evidence-before-action controls

For selected critical actions, the platform must confirm evidence availability before execution.

Examples:

- approvals;
- role/grant changes;
- policy activation;
- secret operations;
- protected external effects;
- emergency-stop release;
- restore completion;
- workspace deletion.

If mandatory evidence cannot be stored, the action is blocked.

## 100. Evidence-after-action failure

If evidence fails after an action may have occurred:

- mark effect and evidence status separately;
- preserve local/source references;
- block false success;
- trigger reconciliation;
- alert Operations/Security;
- avoid blind retry;
- record recovery evidence.

## 101. Audit outage

During audit ingestion or storage outage:

- ordinary low-risk operations may continue only if explicit policy allows and durable local outbox exists;
- protected actions requiring synchronous evidence are blocked;
- emergency restrictions and revocation must remain enforceable;
- users see degraded state;
- no silent evidence loss is accepted.

## 102. Outbox recovery

After outage:

1. restore ingestion;
2. verify source identities;
3. drain outboxes with idempotency;
4. detect gaps and conflicts;
5. update timelines;
6. verify integrity checkpoints;
7. reconcile protected actions;
8. close incident only after evidence health returns.

## 103. Storage saturation

Audit storage capacity has alerts and reserve thresholds. On saturation:

- reject or block nonessential verbose evidence first;
- never silently drop critical events;
- activate protective limits;
- expand/rotate storage;
- preserve integrity and retention;
- document any evidence gap.

## 104. Backup and restore

Audit stores and manifests are backed up according to classification and integrity needs.

After restore:

- verify backup hash/integrity;
- restore schema and indexes;
- reapply holds and retention;
- reconcile events after restore point;
- verify chains/checkpoints;
- invalidate restored sessions;
- mark gaps;
- compare source outboxes;
- progressively re-enable protected actions.

## 105. Negative facts after restore

The following remain authoritative:

- revoked identities/sessions;
- denied policy states;
- consumed/expired approvals;
- deleted/quarantined artifacts;
- active holds;
- unknown effects;
- compromised keys/profiles/adapters;
- open incidents;
- failed controls.

Restore cannot erase negative facts.

## 106. Audit recovery mode

Recovery mode permits bounded verification, replay from trusted outboxes, chain validation, index rebuild, export of diagnostics, and reconciliation. It does not permit ordinary protected actions before evidence health is restored.

## 107. Audit runbooks

Required runbooks:

```text
investigate missing audit event
resolve schema rejection
resolve duplicate event conflict
reconcile sequence gap
repair stale audit projection
verify evidence package
export audit evidence
apply/release audit hold
respond to audit integrity failure
recover audit pipeline
restore audit store
rotate signing/integrity keys
investigate unauthorized audit access
reconcile evidence after protected effect
```

## 108. Security monitoring

Alert on:

- audit disabled or bypassed;
- protected action without expected evidence;
- event ID collision with changed payload;
- integrity mismatch;
- unauthorized access/export;
- mass audit query;
- unusual redaction/deletion;
- clock skew;
- outbox backlog;
- cross-workspace query;
- signing-key failure;
- evidence-store saturation.

## 109. Audit incidents

Critical incidents include:

- tampering;
- deletion outside lifecycle policy;
- cross-workspace disclosure;
- raw secret in evidence;
- forged source identity;
- protected effect without evidence;
- false receipt;
- compromised signing key;
- undetected event loss;
- restore that removes negative facts.

## 110. Incident response

1. restrict evidence access;
2. preserve affected stores and source outboxes;
3. revoke compromised identities/keys;
4. verify integrity checkpoints;
5. determine affected events and actions;
6. reconcile with business state and external receipts;
7. issue correction or gap records;
8. restore trustworthy service;
9. notify authorized owners;
10. update controls and tests.

## 111. API direction

Potential resources:

```text
/audit-events
/audit-timelines
/evidence-records
/evidence-packages
/evidence-receipts
/investigation-cases
/audit-holds
/audit-exports
/audit-integrity-checkpoints
/audit-health
```

## 112. Command API direction

Potential commands:

```text
append-event
register-evidence
build-evidence-package
verify-evidence-package
annotate-evidence
apply-audit-hold
release-audit-hold
create-investigation
close-investigation
request-audit-export
approve-audit-export
verify-integrity
reconcile-gap
register-correction
```

Clients cannot directly overwrite, delete, or mark evidence verified.

## 113. Audit-system events

Potential meta-events:

```text
AuditEventAccepted
AuditEventRejected
AuditDuplicateDetected
AuditConflictDetected
AuditGapDetected
AuditGapReconciled
EvidenceRegistered
EvidencePackageBuilt
EvidencePackageVerified
EvidenceIntegrityFailed
AuditHoldApplied
AuditHoldReleased
AuditExportRequested
AuditExportGenerated
AuditExportDownloaded
AuditExportExpired
InvestigationOpened
InvestigationClosed
AuditStoreRestored
AuditProjectionRebuilt
```

## 114. Data model direction

Core entities:

```text
AuditEvent
AuditActorChain
AuditObjectReference
AuditIntegrityMetadata
AuditSequence
AuditCorrection
AuditAnnotation
EvidenceRecord
EvidencePackage
EvidencePackageItem
EvidenceVerification
ExternalReceipt
AuditTimelineProjection
AuditAccessRecord
AuditExport
AuditExportManifest
AuditHold
InvestigationCase
ChainOfCustodyRecord
AuditHealthFinding
```

## 115. Indexing and projections

Indexes and timelines are derived, rebuildable, and access-controlled.

The authoritative event/evidence store remains separate from convenience projections. Projection corruption does not rewrite original evidence.

## 116. Partitioning direction

Potential partitions:

- environment;
- organization/workspace;
- time;
- event class;
- security/incident domain.

Partition strategy must preserve cross-event investigation capability, integrity verification, retention, and tenant isolation.

## 117. Scalability direction

The architecture should support:

- high-volume run/tool events;
- bounded event size;
- batch ingestion;
- backpressure;
- partitioned verification;
- tiered retention;
- archived evidence;
- selective indexes;
- efficient workspace-scoped queries.

Performance optimizations must not weaken integrity or isolation.

## 118. Accessibility requirements

Audit and evidence interfaces follow proposed/unregistered `A11Y-001`.

Critical journeys include:

- timeline navigation;
- event detail;
- actor-chain review;
- decision/effect comparison;
- evidence-package verification;
- export;
- integrity failure;
- investigation case;
- restore reconciliation.

Meaning cannot rely only on color or position.

## 119. Visual validation

Proposed/unregistered `VVR-001` should cover:

- complete/partial/conflicted/unknown evidence;
- event gaps;
- late arrivals;
- correction events;
- actor chains;
- policy/approval/effect linkage;
- integrity verified/failed;
- export review;
- audit hold;
- investigation case;
- recovery mode;
- dark theme, mobile, focus, and long identifiers.

## 120. Testing strategy

Testing layers:

```text
schema
source authentication
ingestion
transactional outbox
idempotency
duplicate conflict
ordering and gaps
actor chain
workspace isolation
classification and redaction
integrity and hash/signature
policy/approval/run linkage
receipts
exports
retention and holds
deletion treatment
backup/restore
fault injection
security abuse
accessibility
visual regression
performance
```

## 121. Schema tests

Test required fields, versions, controlled vocabularies, size limits, prohibited secret fields, invalid workspace, invalid actor chain, malformed timestamps, unknown actions, and backward compatibility.

## 122. Ingestion tests

Test authenticated source, unauthorized source, duplicate IDs, changed duplicate payload, event delay, retry, outbox replay, partial outage, storage error, and backpressure.

## 123. Workspace-isolation tests

For every audit API, search, count, facet, timeline, export, package, hold, and investigation function:

1. create evidence in workspace A;
2. authenticate a principal limited to workspace B;
3. attempt direct ID access and indirect search;
4. verify denial and no metadata leakage;
5. repeat with stale caches and malformed references.

## 124. Actor-chain tests

Test human, delegated, support, break-glass, agent, adapter, sandbox, Tool Gateway, provider, simulation, unknown actor, and identity mismatch scenarios.

## 125. Decision/effect tests

Test permit without execution, approval without execution, dispatch without receipt, process success with unknown effect, partial effect, reconciled effect, denied action, cancelled attempt, and repeated idempotent request.

## 126. Integrity tests

Test payload modification, deleted event, reordered event, broken chain, invalid signature, revoked key, wrong hash algorithm, incomplete manifest, archive corruption, and recovery verification.

## 127. Redaction and secret tests

Seed known secret values into errors, prompts, commands, environment, provider responses, diffs, and support bundles. Verify they do not enter durable audit or exports.

## 128. Export tests

Test exact scope, field selection, redaction, approval, encryption, manifest, hash verification, download limits, expiry, deletion, and cross-workspace denial.

## 129. Retention and hold tests

Test R4/R5 assignment, expiry, hold precedence, hold release, archive, purge, redaction, investigation closure, provider evidence, and restored holds.

## 130. Restore tests

Restore a backup with later events, revocations, consumed approvals, deleted artifacts, active holds, and integrity checkpoints. Verify all current negative facts and missing intervals are reconciled.

## 131. Fault-injection tests

Inject audit-store outage, outbox failure, duplicate delivery, clock skew, index corruption, signature service outage, disk full, key revocation, network partition, event loss, and restore interruption.

## 132. Security-abuse tests

Attempt to:

- forge actor identity;
- submit client-authored authoritative events;
- suppress audit;
- overwrite events;
- delete held evidence;
- export another workspace;
- inject secrets;
- fake receipts;
- mark evidence verified;
- hide an event gap;
- use support or break-glass identity without disclosure.

## 133. Performance direction

Measure ingestion throughput, tail latency, outbox drain, event size, verification cost, index lag, timeline query, evidence-package generation, export generation, and recovery time.

Formal targets remain in `NFR-001`.

## 134. MVP scope

Recommended MVP:

- structured audit events;
- explicit actor chains;
- workspace/environment scope;
- policy, approval, run, attempt, tool, and artifact linkage;
- append/supersede correction model;
- durable outbox direction;
- idempotent ingestion;
- safe receipts;
- evidence packages for critical workflows;
- C2/C3 classification and `R4` retention direction;
- access-controlled timeline and export;
- no raw secrets;
- evidence health and gap detection;
- restore reconciliation;
- no legal non-repudiation claim.

## 135. Pilot readiness

Before pilot:

- critical event coverage is verified;
- actor-chain and workspace-isolation tests pass;
- policy, approval, sandbox, tool, artifact, export, and restore evidence are linked;
- audit outage behavior is exercised;
- no raw secret appears in evidence;
- holds and retention work;
- integrity checks and backup restore pass;
- export is scoped and protected;
- evidence gaps are visible;
- runbooks exist;
- no critical audit defect remains.

## 136. Controlled-commercial direction

A controlled commercial profile may add:

- stronger append-only storage;
- signed or chained checkpoints;
- external anchoring;
- customer-visible audit exports;
- formal chain-of-custody;
- tenant-specific keys/partitions;
- longer approved retention;
- independent verification;
- integration with customer security operations;
- regulatory mappings after legal review.

## 137. Maturity stages

```text
A0 — ordinary application logs only
A1 — structured attributable audit events
A2 — evidence packages, integrity checks, holds, exports, restore validation
A3 — signed/chained checkpoints and customer assurance
A4 — mature multi-tenant externally reviewed evidence programme
```

## 138. Requirement catalogue — Core audit and attribution

- `AUD-REQ-COR-001` — Every consequential protected action has an attributable audit record.
- `AUD-REQ-COR-002` — Human, agent, adapter, workload, support, and external actors remain distinct.
- `AUD-REQ-COR-003` — Every workspace-scoped event contains an authoritative workspace reference.
- `AUD-REQ-COR-004` — Environment and build identity are recorded for relevant events.
- `AUD-REQ-COR-005` — Decision, approval, dispatch, process result, and external effect remain separate facts.
- `AUD-REQ-COR-006` — Unknown or partial effect is never shown as confirmed success.
- `AUD-REQ-COR-007` — Corrections preserve the original event.
- `AUD-REQ-COR-008` — Audit access and export are themselves audited.
- `AUD-REQ-COR-009` — Client applications cannot author authoritative backend audit facts.
- `AUD-REQ-COR-010` — Critical audit schemas are versioned and validated.
- `AUD-REQ-COR-011` — Events contain correlation and causation references where available.
- `AUD-REQ-COR-012` — Actor identity is never invented when unknown.

## 139. Requirement catalogue — Evidence integrity and lifecycle

- `AUD-REQ-INT-001` — Critical evidence has a verifiable integrity method appropriate to risk.
- `AUD-REQ-INT-002` — Audit records are append-only or equivalently protected from ordinary mutation.
- `AUD-REQ-INT-003` — Same event ID with different content is treated as an integrity incident.
- `AUD-REQ-INT-004` — Raw secrets are prohibited in evidence.
- `AUD-REQ-INT-005` — Audit classification and retention are explicit.
- `AUD-REQ-INT-006` — Audit holds override ordinary lifecycle deletion.
- `AUD-REQ-INT-007` — Deletion or redaction does not falsify historical facts.
- `AUD-REQ-INT-008` — Evidence exports include manifests and known limitations.
- `AUD-REQ-INT-009` — Backup and restore verify evidence integrity.
- `AUD-REQ-INT-010` — Current negative facts survive restore.
- `AUD-REQ-INT-011` — Integrity-key rotation and revocation are governed.
- `AUD-REQ-INT-012` — Unknown evidence integrity blocks unqualified verification.

## 140. Requirement catalogue — Operations and recovery

- `AUD-REQ-OPS-001` — Critical protected actions are blocked when mandatory evidence cannot be recorded.
- `AUD-REQ-OPS-002` — Audit pipelines expose health, backlog, gaps, staleness, and saturation.
- `AUD-REQ-OPS-003` — Outbox replay is idempotent.
- `AUD-REQ-OPS-004` — Late events are appended and visibly marked.
- `AUD-REQ-OPS-005` — Sequence gaps are detected and reconciled.
- `AUD-REQ-OPS-006` — Audit outages do not silently lose critical evidence.
- `AUD-REQ-OPS-007` — Evidence-store saturation does not silently drop critical events.
- `AUD-REQ-OPS-008` — Recovery mode limits ordinary protected effects.
- `AUD-REQ-OPS-009` — Restore reconciles post-backup events and current negative facts.
- `AUD-REQ-OPS-010` — Runbooks cover integrity failure, missing events, export, holds, and recovery.
- `AUD-REQ-OPS-011` — Critical audit failures trigger incident response.
- `AUD-REQ-OPS-012` — Audit evidence is included in release governance.

## 141. Requirement catalogue — Access, privacy, and quality

- `AUD-REQ-ACC-001` — Audit retrieval is authorized before search, count, facet, preview, or export.
- `AUD-REQ-ACC-002` — Cross-workspace audit access is denied by default.
- `AUD-REQ-ACC-003` — Field-level restrictions protect sensitive evidence.
- `AUD-REQ-ACC-004` — Evidence collection is minimized to approved purpose.
- `AUD-REQ-ACC-005` — Full prompts, artifacts, and personal profiles are not retained by default.
- `AUD-REQ-ACC-006` — Search indexes are derived and rebuildable.
- `AUD-REQ-ACC-007` — Audit interfaces are accessible.
- `AUD-REQ-ACC-008` — Audit visual states receive regression validation.
- `AUD-REQ-ACC-009` — Critical audit paths receive abuse and fault-injection tests.
- `AUD-REQ-ACC-010` — Evidence packages declare completeness and limitations.
- `AUD-REQ-ACC-011` — Agents and adapters cannot mark their own evidence verified.
- `AUD-REQ-ACC-012` — Audit exceptions are time-bounded and approved.

## 142. Traceability

| Source | AUD-001 response |
|---|---|
| `SEC-001` | Security-event coverage, integrity, secrets, access, and incidents |
| `THR-001` | Tampering, evidence loss, false success, cross-workspace, and impersonation threats |
| `IAM-001` | Principal, session, delegation, support, break-glass, and revocation evidence |
| `POL-001` | Decision, reason, obligation, activation, rollback, and emergency evidence |
| `SAN-001` | Sandbox specification, tool, secret, violation, output, and cleanup evidence |
| `SEC-002` | Security-control evidence and release gates |
| `DAT-002` | Classification, retention, holds, deletion, export, and restore treatment |
| `RUN-001` | Run, step, attempt, retry, cancellation, and effect-certainty evidence |
| `APR-001` | Approval fingerprint, independence, expiry, invalidation, and consumption |
| `ART-001` | Artifact provenance, validation, acceptance, export, and deletion evidence |
| `MEM-001` | Memory provenance, authority, use, conflict, embedding, and deletion evidence |
| `MOD-001` | Model identity, fallback, provider, usage, and certainty evidence |
| `API-001` | Audit resources and commands |
| `EVT-001` | Event contracts, outbox, idempotency, ordering, and replay |
| `OBS-001` | Health, freshness, alerting, and diagnostic observability |
| `OPS-001` | Audit operations, incidents, runbooks, and recovery |
| `BCP-001` | Backup, restore, recovery, and negative-fact reapplication |
| `VVR-001` | Proposed visual-validation evidence sets |

## 143. ADR-TBD-AUD-001 — Audit store and append-protection model

Select authoritative storage, append-only enforcement, partitions, indexes, archival, and lifecycle operations.

## 144. ADR-TBD-AUD-002 — Audit event schema and actor-chain model

Approve core envelope, actor hops, scope, action/result vocabularies, time semantics, schema versioning, and source authentication.

## 145. ADR-TBD-AUD-003 — Integrity, hashing, signing, and checkpointing

Define evidence levels, algorithms, hash chains, signatures, key lifecycle, checkpoint cadence, verification, and optional external anchoring.

## 146. ADR-TBD-AUD-004 — Transactional outbox, ingestion, and gap reconciliation

Define atomicity, delivery, idempotency, duplicate conflicts, ordering, late events, gaps, backpressure, and outage recovery.

## 147. ADR-TBD-AUD-005 — Evidence packages, receipts, and completeness

Define package types, mandatory items, external receipts, completeness states, manifests, verification, and limitations.

## 148. ADR-TBD-AUD-006 — Audit access, search, export, and investigations

Define field-level controls, search projections, cases, annotations, exports, chain-of-custody direction, and access evidence.

## 149. ADR-TBD-AUD-007 — Audit classification, retention, holds, and deletion

Define C2/C3 handling, R4/R5 schedules, minimization, redaction, personal data, lifecycle, backup, and restore.

## 150. ADR-TBD-AUD-008 — Commercial assurance and external integration

Define customer exports, SIEM integration direction, tenant partitioning, independent verification, regulatory mapping, and assurance claims.

## 150A. ADR-003 evidence refinement

Audit evidence must record workspace, resource visibility, conversation/resource scope, risk class, policy decision, approval fingerprint, actor chain, run correlation, effect certainty, retention profile, and deletion/reference treatment. Access to private, project, or workspace conversations and derived artifacts is itself auditable. Deletion of content must not silently delete the evidence that an access, decision, or deletion occurred.

## 151. Open decisions

1. Confirm `AUD-001` registration.
2. Select authoritative audit storage direction.
3. Approve core event envelope and actor-chain schema.
4. Approve action, outcome, effect-certainty, and completeness vocabularies.
5. Define audit source authentication.
6. Define transactional outbox requirements.
7. Define sequence, ordering, and gap-reconciliation model.
8. Define evidence-integrity levels and algorithms.
9. Decide whether and where to use hash chains.
10. Define signing-key ownership and rotation.
11. Define optional external anchoring.
12. Approve evidence-package types and mandatory contents.
13. Define external-receipt validation.
14. Define audit search and projection architecture.
15. Define field-level access and support/incident access.
16. Define export formats, encryption, expiry, and manifests.
17. Define investigation and chain-of-custody direction.
18. Approve audit classification and retention.
19. Define deletion/redaction treatment.
20. Define audit hold authorities.
21. Define audit-outage and evidence-before-action policy.
22. Define backup/restore and post-restore reconciliation.
23. Define customer-facing commercial audit scope.
24. Confirm accessibility and visual scenarios.
25. Align `CST-001`, `ADP-HER-001`, and `ADP-CDX-001`.

## 152. Risks

| Risk | Consequence | Response |
|---|---|---|
| Operational log treated as proof | False assurance | Structured evidence |
| Human and agent actors collapsed | Misattribution | Actor chain |
| Client emits authoritative audit | Forgery | Source authentication |
| Same ID, different payload | Tampering or collision | Integrity incident |
| Event loss between state and audit | Accountability gap | Transactional outbox |
| Clock skew creates false ordering | Bad investigation | Multi-time semantics |
| Late event silently rewrites timeline | Hidden history | Append late arrival |
| Missing receipt shown as success | Duplicate or false effect | Explicit certainty |
| Raw secret captured | Credential compromise | Prohibited fields/scanning |
| Full prompts retained indefinitely | Privacy and cost risk | Minimization/retention |
| Audit search leaks workspace data | Confidentiality breach | Authorization before query |
| Audit admin deletes evidence | Accountability loss | Append-protected access |
| Hash chain design breaks on concurrency | Unverifiable evidence | ADR and testing |
| Signing key compromised | False trust | Rotation/revocation |
| Export has no manifest | Incomplete investigation | Manifest and limitations |
| Restore loses post-backup events | Evidence gap | Outbox/source reconciliation |
| Projection stale but shown current | Wrong conclusion | Freshness indicators |
| Evidence store fills | Lost events | Capacity thresholds |
| Legal non-repudiation claimed prematurely | Misrepresentation | Explicit limitation |
| Catalogue too complex for MVP | Delay | Maturity stages |

## 153. Assumptions

- Backend services can emit authenticated structured events.
- Business state changes can use durable outbox or equivalent consistency patterns.
- Workspace and environment identity are available for protected operations.
- Policy, approval, run, sandbox, tool, artifact, and provider records expose stable references.
- Secrets can be represented by references.
- Evidence stores can be backed up and access-controlled.
- A local MVP can begin with structured append-protected records before stronger commercial integrity features.
- Legal review will determine external evidentiary claims and statutory retention.

## 154. Constraints

- no raw credentials or secret values in audit;
- no unscoped cross-workspace search or export;
- no rewriting original audit facts;
- no client-authored authoritative backend events;
- no confirmed-success claim without appropriate effect evidence;
- no hidden correction, redaction, or deletion;
- no agent or adapter self-verification;
- no unsupported legal non-repudiation claim;
- no release approval when mandatory audit evidence is failed or unknown;
- no final storage, ledger, signing, or SIEM vendor selected in this draft;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## 155. Acceptance criteria

AUD-001 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts timeline, evidence, export, investigation, and user-facing limitation behavior;
3. Architecture accepts ingestion, storage, schema, partition, projection, receipt, and recovery boundaries;
4. Security accepts attribution, integrity, access, secrets, incidents, signing, and audit-outage controls;
5. Data accepts classification, minimization, retention, holds, redaction, export, and deletion treatment;
6. Operations accepts health, capacity, backup, restore, runbooks, and recovery;
7. Quality accepts schema, isolation, integrity, fault-injection, abuse, accessibility, visual, and release tests;
8. actor-chain and event-envelope models are approved;
9. integrity levels and verification methods are approved;
10. evidence packages and receipts are approved;
11. audit access and exports are approved;
12. retention, holds, and deletion treatment are approved;
13. outage and evidence-before-action behavior are approved;
14. backup and restore reconciliation are approved;
15. downstream cost and adapter specifications can refine evidence fields without changing these invariants.

## 156. Downstream impact

| Document | Required use |
|---|---|
| `CST-001` | Cost estimates, reservations, usage, pricing, budgets, and reconciliation evidence |
| `ADP-HER-001` | Hermes sessions, prompts, tools, models, memory, and external-effect evidence |
| `ADP-CDX-001` | Codex repositories, commands, diffs, tests, commits, push/PR/merge, and receipts |
| `SEC-002` | Evidence requirements and control verification references |
| `DAT-002` | Audit categories, retention, holds, deletion, export, and backup treatment |
| `UXA-001` | Timeline, evidence, investigation, export, and recovery journeys |
| `DSN-001` | Timeline, receipt, integrity, conflict, gap, and evidence components |
| `A11Y-001` | Accessible evidence review, timelines, and exports |
| `VVR-001` | Audit visual scenarios and evidence baselines |
| Document register | Add proposed document and dependencies |

## 157. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial audit and evidence architecture covering events, actor chains, decisions, approvals, execution evidence, receipts, timelines, integrity, append-only direction, exports, investigations, retention, holds, deletion, recovery, operations, tests, and release gates |

## 158. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `IAM-001` — Identity and Access Management Architecture — proposed/unregistered
- `POL-001` — Policy and Permission Architecture — proposed/unregistered
- `SAN-001` — Sandbox and Secure Execution Architecture — proposed/unregistered
- `SEC-002` — Security Control Catalogue — proposed/unregistered
- `DAT-002` — Data Classification, Retention and Deletion Standard — proposed/unregistered
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `EVT-001` — Event Catalog and Async Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
