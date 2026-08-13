---
document_id: OPS-001
title: Agent OS Operations and Production Runbook
version: 0.1.0
status: approved
owner: operations-owner
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
  - DEP-001
  - SEC-001
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
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
  - BCP-001
  - PLG-001
related_adrs:
  - ADR-CANDIDATE-OPS-001
  - ADR-CANDIDATE-OPS-002
  - ADR-CANDIDATE-OPS-003
  - ADR-CANDIDATE-OPS-004
  - ADR-CANDIDATE-OPS-005
  - ADR-CANDIDATE-OPS-006
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# OPS-001 — Agent OS Operations and Production Runbook

> **Status: Approved baseline — 2026-08-13.** This document defines the operational model and runbooks for Agent OS: startup, shutdown, readiness, daily checks, deployments, migrations, maintenance, emergency stop, run recovery, job and event backlogs, adapter and provider failures, approvals, artifacts, memory, costs, backups, restores, security events, support, escalation, evidence, and post-incident review. It relies on the deployment architecture proposed in `DEP-001`, whose autonomous registration is still pending confirmation. It does not select final operations tooling, on-call software, ticketing systems, monitoring products, hosting providers, or contractual response targets.

## 1. Purpose

Agent OS must remain operable when:

- processes restart;
- workers lose leases;
- adapters become unavailable;
- model providers rate-limit or fail;
- approvals expire;
- artifact previews fail;
- events duplicate or arrive out of order;
- queues grow;
- disks fill;
- backups fail;
- migrations stop midway;
- state becomes stale or unknown;
- security controls trigger;
- users report inconsistent behavior.

This runbook defines how authorized operators:

1. establish the current state;
2. identify the authoritative source;
3. protect users and data;
4. stop unsafe activity;
5. restore safe service;
6. reconcile uncertain work;
7. preserve evidence;
8. communicate accurately;
9. avoid duplicate effects;
10. close and learn from operational events.

## 2. Operational objectives

Operations must ensure:

- known ownership;
- safe startup and shutdown;
- clear health and readiness;
- controlled deployments and migrations;
- explicit maintenance modes;
- rapid emergency stop;
- durable run recovery;
- no blind retry after unknown effects;
- dead-letter visibility and remediation;
- adapter and provider isolation;
- artifact and memory integrity;
- backup verification and restore readiness;
- observable capacity and cost;
- workspace-scoped support;
- controlled diagnostic exports;
- evidence for quality gates;
- pilot and commercial readiness.

## 3. Non-goals

This document does not:

- replace `BCP-001`;
- define final RPO or RTO;
- define a complete legal incident-notification process;
- select an on-call provider;
- select a ticketing platform;
- authorize operators to bypass policy or approvals;
- authorize autonomous deployment;
- authorize destructive repair without evidence;
- authorize direct database editing as routine recovery;
- define high-availability architecture;
- claim general production readiness;
- prescribe final command names before implementation.

## 4. Core operating principles

### `OPS-P-001 — Protect first, diagnose second`

When safety, security, or data integrity is uncertain, contain the risk before pursuing full diagnosis.

### `OPS-P-002 — Authoritative state first`

Operators consult transactional state, domain events, audit, and receipts before relying on logs, dashboards, or adapter claims.

### `OPS-P-003 — Unknown is not failure and not success`

Unknown side effects require reconciliation.

### `OPS-P-004 — No blind redispatch`

A stale lease, timeout, lost process, or absent heartbeat does not prove that an external action did not occur.

### `OPS-P-005 — Every action is scoped`

Operational actions specify environment, workspace, run, adapter, store, and time window.

### `OPS-P-006 — Maintenance is explicit`

Read-only, no-new-runs, no-protected-actions, adapter maintenance, and full maintenance are distinct states.

### `OPS-P-007 — Evidence is preserved`

Logs, events, manifests, configuration fingerprints, approvals, and operator actions remain traceable.

### `OPS-P-008 — Restore is privileged`

Restore is never used as an ordinary retry mechanism.

### `OPS-P-009 — Operators do not self-authorize prohibited work`

Operations can stop, isolate, recover, and reconcile. They cannot convert prohibited work into allowed work.

### `OPS-P-010 — Communication reflects certainty`

Operational updates distinguish confirmed fact, source report, inference, estimate, and unknown.

### `OPS-P-011 — Recovery is tested`

Runbooks require exercises and evidence.

### `OPS-P-012 — Small-team operations remain explicit`

A small team may combine roles, but authority, decisions, and reviews remain recorded.

## 5. Operational scope

The runbooks cover:

```text
environment
host
container
service
database
event and job stores
workers and leases
runs and attempts
adapters
model providers
tool gateway and sandbox
approvals
artifacts and previews
memory and indexes
audit and receipts
usage and cost
observability
backup and restore
security events
support
deployment and migration
```

## 6. Operational state model

Environment operating states:

```text
normal
degraded
read_only
no_new_runs
no_protected_actions
maintenance
recovery
emergency_stop
shutdown
unknown
```

## 7. Normal

Conditions:

- required services ready;
- no critical drift;
- queues within threshold;
- storage healthy;
- backups current;
- adapters/providers within approved limits;
- no active A0/A1;
- protected controls operational.

## 8. Degraded

Examples:

- optional search index unavailable;
- one adapter unavailable;
- provider rate-limited;
- preview conversion unavailable;
- telemetry partially degraded.

The remaining capabilities and limitations must be explicit.

## 9. Read-only

Permits:

- authenticated reads;
- timelines;
- evidence review;
- diagnostics;
- approved exports where policy allows.

Blocks ordinary writes.

## 10. No-new-runs

Permits:

- existing safe work to complete;
- diagnostics;
- reconciliation;
- approved cancellations;
- reads.

Blocks creation or dispatch of new runs.

## 11. No-protected-actions

Permits safe read-only and reversible internal workflows.

Blocks:

- approval consumption;
- tool dispatch;
- external messages;
- Git commit/push/PR;
- external-effect retries;
- privileged restore/migration.

## 12. Maintenance

Used for:

- deployment;
- migration;
- storage maintenance;
- controlled restore;
- certificate or secret rotation;
- adapter upgrade.

Scope and user impact are declared.

## 13. Recovery

Used when the system is restoring authoritative consistency after:

- crash;
- restore;
- partial deployment;
- lost lease;
- event gap;
- missing artifact;
- unknown effect.

## 14. Emergency stop

Used for immediate containment of:

- security compromise;
- cross-workspace leak;
- approval bypass;
- unsafe tool execution;
- destructive replay;
- uncontrolled external effects;
- critical data integrity risk.

## 15. Shutdown

No service processing is expected.

Data, leases, runs, and evidence must reflect the shutdown.

## 16. Unknown environment state

Used when:

- build cannot be identified;
- configuration is unclear;
- schema cannot be confirmed;
- core stores are inaccessible;
- telemetry and authoritative data conflict.

Unknown state blocks protected actions.

## 17. Operational roles

```text
operations_lead
release_operator
incident_commander
security_lead
data_recovery_operator
application_operator
adapter_operator
support_operator
quality_reviewer
product_decision_owner
```

## 18. Operations Lead

Accountable for:

- operational readiness;
- runbook ownership;
- environment inventory;
- maintenance;
- alert ownership;
- drills;
- operational acceptance.

## 19. Release Operator

Authorized to execute an approved deployment plan.

Not automatically authorized to:

- approve release;
- execute destructive migration;
- restore data;
- change production policy;
- rotate all secrets.

## 20. Incident Commander

Coordinates:

- containment;
- workstreams;
- status;
- evidence;
- decisions;
- recovery;
- communication;
- review.

## 21. Security Lead

Owns security containment for:

- access compromise;
- secret exposure;
- sandbox escape;
- approval bypass;
- cross-workspace access;
- malicious artifact;
- event forgery.

## 22. Data Recovery Operator

Owns:

- backup validation;
- restore execution;
- data reconciliation;
- manifests;
- data-integrity checks.

## 23. Application Operator

Handles:

- services;
- runs;
- jobs;
- events;
- workers;
- health;
- diagnostics.

## 24. Adapter Operator

Handles:

- adapter health;
- sessions;
- compatibility;
- capabilities;
- versioning;
- revocation;
- reconciliation.

## 25. Support Operator

Handles:

- user reports;
- safe evidence collection;
- workspace-scoped diagnosis;
- escalation;
- known-issue guidance.

## 26. Quality Reviewer

Validates:

- runbook exercise evidence;
- release and recovery gates;
- exception expiry;
- test results;
- post-incident actions.

## 27. Separation of operational authority

High-risk actions should separate, where practical:

```text
request
approval
execution
verification
```

Examples:

- restore requested by Operations, approved by Data/Security as required, executed by Recovery Operator, verified by Quality/Data;
- deployment approved by release board, executed by Release Operator;
- emergency-stop release approved separately from activation.

## 28. Operational records

Operations uses:

```text
EnvironmentRecord
MaintenanceRecord
DeploymentOperation
MigrationOperation
RecoveryOperation
EmergencyStopRecord
IncidentRecord
RunbookExecution
DiagnosticBundle
OperationalException
ChangeRecord
```

## 29. Environment record

Contains:

- environment ID;
- profile;
- owner;
- current build;
- schema;
- configuration hash;
- services;
- stores;
- adapters;
- providers;
- feature flags;
- exposure;
- backup status;
- support status;
- current operating state.

## 30. Operational command safety

Every operational command should support:

- dry-run or preview where practical;
- exact target;
- environment validation;
- confirmation;
- idempotency;
- correlation;
- audit;
- bounded output;
- safe failure;
- no hidden wildcard.

## 31. Operator access

Requirements:

- named identity;
- least privilege;
- environment scope;
- reauthentication for critical actions;
- no shared generic administrator account;
- session expiry;
- audit;
- emergency revocation.

## 32. Privileged access

Privileged access includes:

- migration;
- restore;
- backup-key access;
- secret rotation;
- emergency-stop release;
- database administration;
- host administration.

It is time-bound and purpose-bound where possible.

## 33. Break-glass access

A future break-glass mechanism may be used only when ordinary access is unavailable.

It requires:

- sealed or controlled credential;
- explicit activation;
- high-severity audit;
- notification;
- short expiry;
- review;
- rotation after use.

## 34. Daily operating cadence

Recommended daily checks for pilot or controlled commercial environments:

1. verify environment/build identity;
2. verify critical service readiness;
3. inspect A0/A1/A2 alerts;
4. inspect stale and unknown runs;
5. inspect outbox/inbox/dead letters;
6. inspect adapter/provider readiness;
7. inspect artifact quarantine and storage;
8. inspect backup age and verification;
9. inspect capacity and budget warnings;
10. review active exceptions and maintenance.

## 35. Weekly operating cadence

- restore-drill status;
- security findings;
- adapter/model validation age;
- queue trends;
- storage growth;
- cost reconciliation;
- support trends;
- certificate/secret expiry;
- quality debt;
- runbook updates.

## 36. Monthly or milestone cadence

- backup restore exercise;
- emergency-stop exercise;
- dependency review;
- access review;
- incident trend review;
- capacity forecast;
- documentation consistency;
- pilot/commercial readiness review.

Exact cadence requires governance approval.

## 37. Shift handover

Handover includes:

- current environment state;
- active incidents;
- stale/unknown runs;
- maintenance;
- deployments/migrations;
- adapter/provider issues;
- backups;
- exceptions;
- pending user commitments;
- next actions;
- owners.

## 38. Startup runbook — purpose

Safely start Agent OS and prove readiness without dispatching work prematurely.

## 39. Startup prerequisites

- approved environment inventory;
- host time synchronized;
- disk capacity acceptable;
- configuration available;
- secret references valid;
- data volumes present;
- database recoverable;
- current build identified;
- emergency-stop state known;
- no conflicting restore/migration.

## 40. Startup procedure

1. verify host and environment ID;
2. verify current build digest;
3. verify configuration fingerprint;
4. verify volume mounts and permissions;
5. start database and durable stores;
6. verify schema and migrations;
7. start control-plane services without schedulers if supported;
8. run startup recovery scan;
9. reconcile leases, runs, outbox/inbox, adapters, artifacts;
10. start workers and schedulers;
11. start adapters according to enablement;
12. verify health and readiness;
13. run safe smoke test;
14. set environment state to normal or degraded;
15. record evidence.

## 41. Startup blockers

- unknown schema;
- invalid configuration;
- missing critical volume;
- database integrity failure;
- unresolved restore;
- emergency stop of unknown scope;
- critical drift;
- secret invalid for required service;
- consumed approval inconsistency;
- cross-workspace integrity failure.

## 42. Startup recovery scan

Must identify:

- nonterminal runs;
- expired leases;
- active job locks;
- pending cancellation;
- outbox backlog;
- inbox incomplete processing;
- adapter sessions;
- orphan artifact content;
- missing artifact content;
- stale projections;
- unfinished migration;
- unfinished restore.

## 43. Startup result states

```text
ready
ready_degraded
blocked_recovery_required
blocked_configuration
blocked_data_integrity
blocked_security
unknown
```

## 44. Shutdown runbook — purpose

Stop services without silently losing or duplicating work.

## 45. Planned shutdown procedure

1. announce maintenance;
2. activate no-new-runs;
3. block protected dispatch if required;
4. inspect active runs;
5. allow bounded safe completion;
6. request cancellation or pause where supported;
7. stop schedulers;
8. drain or persist outbox;
9. stop workers gracefully;
10. stop adapters and preserve session references;
11. stop API/UI;
12. stop durable stores last;
13. record nonterminal and unknown state;
14. verify backup if required;
15. record shutdown evidence.

## 46. Forced shutdown

If forced:

- record time and reason;
- assume active external effects may be unknown;
- do not mark runs cancelled/completed;
- require startup recovery;
- preserve logs and host evidence;
- communicate degraded certainty.

## 47. Shutdown completion criteria

- no new dispatch;
- services stopped;
- stores consistent or recovery required recorded;
- leases expire or are revoked;
- active runs documented;
- evidence preserved;
- environment state `shutdown`.

## 48. Health-check runbook

Purpose:

Distinguish liveness, readiness, dependency health, and functional health.

## 49. Health evaluation order

1. environment/build;
2. critical stores;
3. schema;
4. control plane;
5. workers/schedulers;
6. adapters/providers;
7. artifacts/memory;
8. observability;
9. backup readiness;
10. user-safe functional smoke.

## 50. False-green prevention

If telemetry is unavailable:

```text
health = unknown or degraded
not healthy by absence
```

## 51. Database-unavailable runbook

Immediate actions:

- block new protected dispatch;
- set API not ready or degraded;
- stop workers from new effects;
- preserve in-memory diagnostic information safely;
- verify host/storage/network;
- avoid repeated restarts that obscure evidence.

Diagnosis:

- process/container;
- disk;
- connection limits;
- authentication;
- schema;
- locks;
- corruption;
- network;
- resource exhaustion.

Recovery:

- restore database service;
- validate integrity;
- run startup recovery;
- reconcile jobs/runs/events;
- verify approvals and artifacts;
- resume gradually.

## 52. Database corruption suspected

Containment:

- emergency stop or no-protected-actions;
- stop writes;
- preserve evidence;
- do not run repair blindly;
- involve Data and Security;
- validate backup;
- decide repair versus restore.

## 53. Disk-capacity runbook

Indicators:

- write failures;
- database errors;
- artifact staging failures;
- telemetry drops;
- backup failure.

Actions:

1. stop growth-producing operations;
2. identify filesystem and top consumers;
3. protect authoritative data;
4. rotate/delete only under retention policy;
5. expand storage or move data;
6. verify stores;
7. resume cautiously.

Never delete:

- database files;
- artifact content;
- event/audit evidence;
- backups;

without exact governed procedure.

## 54. CPU or memory saturation

Actions:

- identify component;
- reduce concurrency;
- stop noncritical jobs;
- disable optional preview/index workload;
- preserve protected operations;
- inspect leaks/runaway processes;
- scale or restart with recovery plan.

## 55. Container restart loop

Actions:

- stop automatic loop if obscuring evidence;
- inspect exit code;
- validate config/secrets;
- validate migrations;
- inspect volume permissions;
- inspect dependency readiness;
- run foreground diagnostic;
- fix/redeploy;
- verify no run duplication.

## 56. Run-operations overview

Operator views should classify runs as:

```text
normal
waiting_expected
waiting_too_long
stale
unknown
blocked
recovery_required
terminal_with_gaps
```

## 57. Stale-run runbook

A stale run lacks expected recent evidence.

Procedure:

1. identify run, step, attempt, adapter session;
2. verify last reliable evidence;
3. verify lease/heartbeat;
4. inspect adapter/provider;
5. inspect tool/provider idempotency and external reference;
6. classify side-effect certainty;
7. reconcile;
8. choose resume, retry, cancel, fail, complete, or remain unknown;
9. record decision and evidence.

## 58. Unknown-effect runbook

Never retry immediately.

Procedure:

1. activate no protected redispatch for the exact action;
2. identify normalized target and idempotency key;
3. query adapter/provider/tool;
4. inspect external evidence;
5. compare artifact, Git reference, message ID, calendar version, file hash, or provider request;
6. classify effect:
   - confirmed_none;
   - confirmed_applied;
   - partial;
   - conflicting;
   - unknown;
7. update reconciliation record;
8. authorize next action separately.

## 59. Run stuck waiting for approval

Check:

- approval request state;
- reviewer eligibility;
- independence;
- expiry;
- invalidation;
- fingerprint;
- notification delivery;
- emergency stop;
- review material freshness.

Actions:

- remind/escalate;
- request revision;
- cancel request/run;
- invalidate stale request;
- never approve on behalf of a human.

## 60. Run stuck waiting for adapter

Check:

- adapter health/readiness;
- version;
- capability enablement;
- queue;
- session limits;
- secret reference;
- network;
- validation expiry.

Actions:

- restore adapter;
- reroute only through policy;
- keep fallback explicit;
- preserve original attempt;
- create new attempt only when safe.

## 61. Run stuck waiting for model/provider

Check:

- binding health;
- provider status;
- rate limit;
- quota;
- budget;
- data restrictions;
- region;
- fallback.

Actions:

- wait/backoff;
- choose approved alternative;
- request new approval if material;
- cancel;
- never silently switch provider.

## 62. Run stuck waiting for resource

Check:

- worker capacity;
- lease;
- storage;
- artifact quota;
- budget reservation;
- sandbox capacity;
- maintenance.

Actions:

- release stale reservation;
- scale;
- reschedule;
- cancel;
- preserve priority/fairness.

## 63. Cancellation runbook

Procedure:

1. persist cancellation request;
2. block undispatched jobs;
3. signal workers/adapters;
4. observe acknowledgment;
5. wait for terminal evidence within bound;
6. classify partial/unknown effects;
7. reconcile;
8. set final cancellation state only when justified;
9. produce receipt.

## 64. Cancellation timeout

If no terminal evidence:

- mark cancellation outcome unknown or partial;
- block retry;
- alert;
- reconcile;
- communicate that cancellation was requested but not confirmed.

## 65. Retry runbook

Retry only when:

- failure classified;
- action idempotent or confirmed not applied;
- retry budget remains;
- deadline remains;
- approval valid for new attempt or renewed;
- provider/adapter ready;
- no emergency stop.

A retry creates a new attempt.

## 66. Manual run-state correction

Direct database state edits are prohibited as routine operations.

A governed resolution command must:

- reference evidence;
- state prior and resulting status;
- preserve history;
- identify operator;
- emit events/audit;
- avoid fabricating external certainty.

## 67. Job-backlog runbook

Check:

- pending count;
- oldest age;
- worker readiness;
- concurrency;
- lease conflicts;
- database locks;
- priority starvation;
- maintenance state.

Actions:

- restore workers;
- increase bounded concurrency;
- pause noncritical jobs;
- inspect poison jobs;
- avoid duplicate manual dispatch.

## 68. Expired-lease runbook

Procedure:

1. identify job/run/attempt;
2. inspect worker and last heartbeat;
3. reject stale fencing token;
4. determine external-effect certainty;
5. reconcile;
6. release/requeue only when safe;
7. record lease incident.

## 69. Fencing conflict

Treat as A1 or higher if stale writes were nearly or actually accepted.

Actions:

- stop affected workers;
- preserve transaction evidence;
- verify database constraints;
- inspect duplicate instances;
- test fencing;
- correct before resuming.

## 70. Dead-letter runbook

For each dead letter:

1. identify event/job and consumer;
2. classify reason;
3. inspect payload reference safely;
4. determine whether business state already changed;
5. correct code/config/data;
6. choose replay, ignore, quarantine, or manual resolution;
7. verify idempotency;
8. record outcome.

## 71. Poison-event runbook

Actions:

- quarantine;
- prevent hot-loop;
- capture schema/error;
- minimize payload access;
- fix consumer or transform event;
- test with isolated fixture;
- replay only after review.

## 72. Outbox-backlog runbook

Check:

- publisher health;
- transport/store;
- schema;
- oldest age;
- retries;
- dead letters;
- storage.

Actions:

- restore publisher;
- correct incompatibility;
- drain with bounded concurrency;
- monitor projections;
- preserve stable event IDs.

## 73. Inbox-backlog runbook

Check:

- consumer health;
- dependency;
- poison events;
- duplicates;
- schema versions;
- authorization/classification failures.

Actions:

- restore consumer;
- quarantine poison events;
- replay safely;
- verify no duplicate business effects.

## 74. Event-gap runbook

Procedure:

1. identify stream/aggregate and missing sequence/version;
2. inspect source store;
3. determine delayed, retained, lost, or corrupted;
4. block authoritative projection if necessary;
5. replay/rebuild;
6. reconcile aggregate;
7. document unresolved gap.

## 75. Projection-stale runbook

Actions:

- mark UI stale;
- inspect consumer lag;
- inspect cursor;
- rebuild shadow projection if needed;
- validate counts/checksums;
- switch atomically;
- keep authoritative reads available where possible.

## 76. Adapter-unavailable runbook

Actions:

1. set adapter not ready;
2. block new dispatch;
3. list affected runs/sessions;
4. inspect process, version, config, secret, network;
5. restore or revoke;
6. reconcile active attempts;
7. consider approved fallback;
8. verify before ready.

## 77. Adapter-capability drift

Actions:

- suspend affected capability;
- record drift;
- block routes requiring it;
- rerun conformance;
- inspect version/runtime/provider;
- update capability declaration;
- require re-enable approval where needed.

## 78. Adapter-version mismatch

Actions:

- mark incompatible;
- block readiness;
- deploy approved version or update contract;
- run conformance;
- reconcile pending sessions;
- do not ignore major mismatch.

## 79. Adapter-event gap

Actions:

- preserve external cursor;
- request replay/status where supported;
- compare platform state;
- reconcile;
- expose limitations;
- do not infer missing states.

## 80. Codex-adapter runbook

Operational checks:

- repository/worktree scope;
- branch;
- uncommitted changes;
- command bounds;
- runtime/model identity;
- test/build result;
- patch artifact;
- Git credentials;
- approval state.

Critical restrictions:

```text
no autonomous merge
no force push
no history rewrite
no broad home mount
no Docker socket
```

## 81. Codex workspace contamination

If unrelated user changes are detected:

- stop write operations;
- preserve diff;
- do not reset;
- identify ownership;
- isolate new worktree/branch;
- notify user/operator;
- resume only with clean scoped plan.

## 82. Hermes-adapter runbook

Checks:

- runtime identity;
- session binding;
- capabilities;
- native-tool visibility;
- provider/model;
- filesystem/network scope;
- health;
- event cursor;
- cancellation semantics.

If native-tool visibility is insufficient for a protected workflow, block that workflow.

## 83. Model-provider outage runbook

Actions:

- mark binding unhealthy;
- block new routing;
- preserve active request IDs;
- classify timed-out effects/output state;
- apply backoff;
- evaluate approved fallback;
- monitor quota/rate limit;
- communicate.

## 84. Provider rate limit

Actions:

- honor retry-after;
- reduce concurrency;
- queue boundedly;
- surface wait;
- avoid retry storm;
- review quotas;
- preserve deadlines/budget.

## 85. Provider identity unavailable

Do not report configured identity as actual.

Actions:

- mark actual identity unavailable/unknown;
- preserve configured and selected values;
- inspect adapter/provider evidence;
- block workflows requiring verified model identity.

## 86. Model fallback runbook

Verify:

- fallback policy;
- capability compatibility;
- data policy;
- region;
- cost;
- context limits;
- approval;
- user visibility.

Record selected and actual identity separately.

## 87. Tool-Gateway denial runbook

A policy, scope, network, filesystem, or sandbox denial is usually expected protection.

Actions:

- verify request;
- inspect reason code;
- correct task or policy through governance;
- do not bypass gateway;
- escalate repeated suspicious attempts.

## 88. Tool action unknown

Use the unknown-effect runbook.

Potential evidence:

- file hash;
- Git commit;
- external message ID;
- remote API resource;
- calendar event version;
- process result;
- sandbox receipt.

## 89. Sandbox violation

Immediate actions:

- terminate/isolate sandbox;
- emergency stop affected capability if needed;
- preserve logs and image/version;
- revoke adapter/tool;
- inspect host exposure;
- rotate secrets if possibly exposed;
- security incident process.

## 90. Approval-service unavailable

Actions:

- block approval-dependent actions;
- keep requests visible where possible;
- do not use cached approval as new authority;
- preserve expiration;
- restore service;
- reconcile consumption records.

## 91. Approval replay detected

Treat as security event.

Actions:

- block action;
- preserve request/decision/consumption evidence;
- identify actor/session/workload;
- inspect duplicate dispatch;
- invalidate related grants if needed;
- escalate.

## 92. Approval fingerprint mismatch

Expected response:

- deny consumption;
- mark request stale/invalid;
- show changed material fields;
- create new request if action still desired;
- investigate repeated mismatches.

## 93. Approval consumed but dispatch uncertain

Procedure:

- preserve consumed state;
- do not issue second approval automatically;
- inspect dispatch intent and adapter/tool;
- reconcile effect;
- create new request only for a new bounded action if needed.

## 94. Artifact-store unavailable

Actions:

- mark content unavailable;
- keep metadata read-only;
- block staging/finalization/preview/export;
- inspect filesystem/object store;
- verify permissions/capacity;
- restore;
- reconcile missing/orphan objects.

## 95. Artifact hash mismatch

Actions:

- quarantine version;
- block preview/accept/export;
- preserve object and metadata evidence;
- determine corruption or wrong upload;
- reupload as new version;
- inspect storage integrity.

## 96. Artifact-preview failure

Actions:

- mark preview failed/unavailable;
- do not open original actively;
- inspect converter and limits;
- quarantine suspicious content;
- provide metadata-only safe view;
- retry only in isolated worker.

## 97. Artifact quarantine surge

Potential causes:

- malicious corpus;
- scanner/config change;
- false positive;
- active attack;
- format drift.

Actions:

- stop affected ingestion if needed;
- sample safely;
- validate scanner;
- security review;
- communicate limitations.

## 98. Orphan artifact content

Procedure:

- identify object without metadata or metadata without object;
- preserve object;
- classify;
- verify manifests;
- reconcile staging/finalization;
- delete only under governed orphan policy.

## 99. Artifact deletion stuck

Check:

- hold;
- approval;
- content store;
- previews;
- indexes;
- backups;
- external exports.

Do not mark deleted until canonical deletion state is justified.

## 100. Memory-index unavailable

Actions:

- mark index unavailable/stale;
- use direct authoritative retrieval where safe;
- block vector-only features;
- rebuild index;
- verify workspace/deletion;
- do not mark memory lost.

## 101. Memory conflict surge

Actions:

- inspect source/authority changes;
- review ingestion;
- suspend automatic verification;
- surface conflicts;
- correct mapping or content;
- avoid majority-by-repetition authority.

## 102. Memory deletion not propagated

Treat as data-governance issue.

Actions:

- block affected index/export;
- verify tombstone;
- remove derived copies;
- rebuild;
- inspect backups/external copies;
- record limitations.

## 103. Audit write failure

For protected actions under fail-closed policy:

- block action;
- alert;
- preserve pending intent;
- restore audit service/store;
- do not continue without required evidence.

## 104. Receipt generation failure

Actions:

- keep run terminal state separate;
- mark receipt failed/partial;
- inspect missing evidence;
- retry receipt generation safely;
- expose gaps;
- do not fabricate completeness.

## 105. Cost unknown or mismatched

Actions:

- preserve unknown/mismatch;
- inspect usage source;
- pricing version;
- provider report;
- invoice;
- deduplication;
- fallback;
- reconcile;
- avoid substituting zero.

## 106. Budget hard-limit reached

Actions:

- block new cost-incurring work;
- allow safe reads/reconciliation;
- notify owner;
- inspect reservations;
- release stale reservations;
- change budget only through authority.

## 107. Cost anomaly

Examples:

- unexpected provider;
- large usage;
- duplicate usage;
- missing pricing;
- fallback cost increase.

Actions:

- pause affected routing;
- inspect runs/profile;
- reconcile;
- alert Product/Data/Operations;
- update budget or policy only through governance.

## 108. Backup-operations overview

Routine operations include:

- scheduled backup;
- manifest;
- verification;
- retention;
- capacity;
- alerting;
- restore drill.

Detailed continuity policy belongs in `BCP-001`.

## 109. Backup-failure runbook

Actions:

1. alert owner;
2. identify failed store/step;
3. preserve last successful backup;
4. inspect capacity, credentials, destination, locks;
5. rerun safely;
6. verify manifest;
7. assess exposure window;
8. escalate if RPO direction threatened.

## 110. Backup overdue

Actions:

- verify scheduler;
- inspect last success;
- run manual approved backup if safe;
- assess environment state;
- consider no-protected-actions for critical exposure;
- communicate.

## 111. Backup verification failure

Do not treat backup as usable.

Actions:

- quarantine failed backup;
- inspect manifest/hash/encryption;
- create new backup;
- perform restore drill when required;
- update continuity risk.

## 112. Restore overview

Restore is governed by:

- exact backup;
- target environment;
- maintenance;
- approval;
- compatibility;
- post-restore reconciliation;
- evidence.

## 113. Restore preflight

- reason and scope;
- backup manifest;
- integrity;
- encryption/key access;
- target isolated;
- schema compatibility;
- current data preservation;
- active runs;
- consumed approvals;
- tombstones;
- external effects;
- rollback/stop plan;
- approvers.

## 114. Restore procedure direction

1. activate maintenance/emergency controls;
2. stop new work;
3. snapshot current state where possible;
4. validate target;
5. restore database and content stores;
6. apply approved compatibility migrations;
7. invalidate leases/sessions as required;
8. run startup recovery;
9. reconcile runs, approvals, events, artifacts, memory, costs;
10. rebuild derived stores;
11. run integrity and smoke tests;
12. record gaps;
13. release maintenance only after approval.

## 115. Restore blockers

- backup integrity unknown;
- wrong target;
- missing key;
- incompatible schema without plan;
- no current-state preservation;
- operator authority missing;
- cross-workspace integrity failure;
- inability to reconcile protected actions.

## 116. Post-restore checks

T0:

- consumed approvals remain consumed;
- no blind redispatch;
- leases invalid;
- nonterminal runs in recovery;
- tombstones preserved;
- artifact hashes consistent;
- inbox/outbox state safe;
- users/workspaces correct;
- secrets/config correct;
- audit gaps visible.

## 117. Restore failure

Actions:

- remain in maintenance;
- preserve partial state;
- do not retry destructively without analysis;
- evaluate alternate backup;
- involve Data/Security/Architecture;
- communicate uncertainty;
- create incident.

## 118. Deployment-operations overview

Deployments follow approved `DEP-001` plans and `QAG-001` gates.

## 119. Deployment preflight runbook

Verify:

- release candidate digest;
- target environment;
- approvals;
- config drift;
- secrets;
- capacity;
- backup;
- migration;
- maintenance;
- support;
- stop conditions;
- monitoring.

## 120. Deployment execution runbook

1. announce;
2. acquire environment lock;
3. enter maintenance mode if needed;
4. verify/create backup;
5. verify candidate digest;
6. deploy compatible services;
7. execute migrations;
8. start/restart;
9. verify readiness;
10. run smoke;
11. observe;
12. release maintenance;
13. update environment record;
14. release lock;
15. publish result.

## 121. Deployment failure

Classify:

```text
preflight_failed
before_migration
migration_failed
services_not_ready
smoke_failed
observation_failed
rollback_failed
recovery_required
unknown
```

## 122. Deployment rollback

Use only approved compatible method:

- application rollback;
- feature disablement;
- adapter/provider disablement;
- forward-fix;
- restore.

Verify schema compatibility first.

## 123. Partial deployment

Actions:

- stop new promotion;
- identify versions per service;
- enter maintenance/degraded state;
- preserve logs;
- decide complete forward or rollback;
- avoid repeated uncontrolled restarts.

## 124. Environment-lock runbook

If lock appears stale:

- inspect operator/process;
- inspect fencing token;
- determine whether operation may continue;
- do not simply delete lock;
- recover through governed command.

## 125. Migration-operations overview

Migrations are explicit, checksummed, and evidence-bearing.

## 126. Migration preflight runbook

- current/target schema;
- migration checksum;
- representative rehearsal;
- disk/capacity;
- backup;
- active runs;
- locks;
- estimated duration;
- maintenance mode;
- forward-fix/restore plan.

## 127. Migration execution runbook

1. acquire environment/migration lock;
2. activate maintenance mode;
3. verify backup;
4. run migration with bounded logs;
5. monitor locks/progress;
6. checkpoint long backfills;
7. verify schema/data;
8. start compatible services;
9. run smoke/performance checks;
10. release maintenance;
11. record evidence.

## 128. Migration interrupted

Actions:

- stop concurrent changes;
- inspect checkpoint;
- determine transaction state;
- resume if designed;
- otherwise use forward-fix or restore;
- do not rerun blindly;
- preserve checksum and logs.

## 129. Migration verification failure

Remain in maintenance.

Actions:

- identify invariant failure;
- protect data;
- choose forward-fix, application rollback, or restore;
- involve Data/Architecture;
- record incident if material.

## 130. Secret-rotation runbook

1. identify secret reference and dependents;
2. provision new secret;
3. validate in isolated/bounded way;
4. update reference/config;
5. reload/redeploy affected components;
6. verify readiness;
7. revoke old secret;
8. monitor failures;
9. record audit.

## 131. Secret exposure runbook

Immediate:

- stop affected capability;
- revoke/rotate secret;
- preserve evidence without spreading value;
- inspect logs/artifacts/events;
- identify access;
- assess provider/account activity;
- security incident;
- verify redaction and cleanup.

## 132. Certificate-expiry runbook

- verify expiry;
- renew;
- deploy safely;
- validate chain/host;
- reload proxy;
- test clients;
- revoke old if required;
- update alerts.

## 133. User-access issue runbook

Check:

- identity;
- session;
- workspace membership;
- role;
- classification;
- suspension;
- reauthentication;
- environment URL.

Do not grant broad role solely to solve a support issue.

## 134. Cross-workspace access report

Treat as high severity until disproven.

Actions:

- contain;
- preserve request/audit;
- verify actual disclosure versus denial;
- identify resource/query/projection/cache;
- test related surfaces;
- notify Security;
- stop pilot if confirmed.

## 135. Authentication failure surge

Potential causes:

- attack;
- expired credentials;
- identity outage;
- client misconfiguration.

Actions:

- inspect source patterns safely;
- rate-limit/block;
- verify identity service;
- communicate;
- avoid leaking account existence.

## 136. Security-event severity

Operational severity:

```text
A0 immediate emergency
A1 critical
A2 major
A3 warning
A4 informational
```

Security severity and defect severity remain separate but mapped.

## 137. A0 operational response

- emergency stop or containment;
- incident commander;
- Security Lead;
- preserve evidence;
- block affected access/effects;
- assess data integrity;
- communicate;
- recover only after explicit approval.

## 138. Incident lifecycle

```text
detected
triaged
declared
contained
investigating
recovering
monitoring
resolved
review_pending
closed
```

## 139. Incident declaration criteria

Declare incident for:

- S0/A0;
- confirmed data leak;
- approval bypass;
- destructive duplicate effect;
- unrecoverable service loss;
- failed restore during required recovery;
- material data corruption;
- repeated unknown protected effects;
- prolonged pilot outage.

## 140. Incident command structure

- Incident Commander;
- Operations;
- Security;
- Data;
- Architecture;
- Product/Communications;
- Quality/Scribe.

Small teams may combine roles but preserve decision ownership.

## 141. Incident timeline

Record:

- detection;
- alerts;
- authoritative state;
- actions;
- decisions;
- evidence;
- communications;
- containment;
- recovery;
- unresolved unknowns.

## 142. Incident communication principles

- state what is known;
- state source;
- state impact;
- state uncertainty;
- state containment;
- state next update;
- avoid blame and unsupported claims;
- protect sensitive details.

## 143. Internal status template

```text
Incident:
Severity:
Environment:
Detected:
Current impact:
Confirmed facts:
Unknowns:
Containment:
Current actions:
Data/security status:
Next update:
Owner:
```

## 144. User-facing status template

```text
We are investigating an issue affecting <scope>.
Current impact: <confirmed impact>.
We have <containment action>.
No further action is required from users / Users should <action>.
Next update: <time or condition>.
```

## 145. Incident evidence bundle

Include:

- build/config;
- alerts;
- events;
- audit;
- logs/traces;
- run timelines;
- adapter/provider evidence;
- approvals;
- artifacts;
- operator actions;
- backup/restore state;
- gaps.

## 146. Incident closure criteria

- safe state restored;
- affected users/workspaces identified;
- containment stable;
- data integrity assessed;
- unknowns documented;
- alerts normal;
- monitoring window complete;
- owner approves;
- review scheduled.

## 147. Post-incident review

Covers:

- summary;
- impact;
- timeline;
- detection;
- root and contributing causes;
- controls that worked/failed;
- recovery;
- communication;
- evidence gaps;
- corrective actions;
- tests/runbooks/docs;
- owners/dates.

## 148. Blameless review with accountability

The review avoids personal blame while assigning:

- control ownership;
- remediation owner;
- due date;
- verification;
- governance update.

## 149. Problem management

Repeated incidents create a problem record.

Track:

- pattern;
- aggregate impact;
- root cause;
- workaround;
- permanent fix;
- quality debt;
- release gate impact.

## 150. Support intake

Support request fields:

- requester;
- workspace;
- environment;
- time;
- route/action;
- expected/actual;
- screenshot safely redacted;
- correlation/request ID;
- severity;
- data/security concern;
- reproducibility.

## 151. Support triage

Categories:

```text
how_to
access
run_state
approval
adapter_or_model
artifact
memory
cost
performance
security
data_integrity
deployment
```

## 152. Support evidence collection

Prefer:

- correlation ID;
- run ID;
- timestamp;
- safe diagnostic bundle;
- environment/build;
- screenshots without secrets.

Avoid asking users to send:

- passwords;
- API keys;
- confidential full prompts;
- raw database dumps.

## 153. Support access

Support access to a workspace requires:

- authorization;
- purpose;
- scope;
- time bound;
- audit;
- no unrestricted impersonation by default.

## 154. Known-issue handling

Known issue record:

- symptom;
- affected versions;
- severity;
- workaround;
- risk;
- owner;
- fix status;
- user guidance;
- expiry.

## 155. Escalation matrix

Potential escalation:

| Condition | Primary | Secondary |
|---|---|---|
| Run stale/unknown | Operations | Architecture/Adapter |
| Approval failure | Operations | Security/Product |
| Artifact quarantine | Security | Operations/Data |
| Cross-workspace | Security | Incident Commander/Data |
| Database integrity | Data | Operations/Architecture |
| Adapter drift | Adapter Owner | Architecture/Security |
| Cost anomaly | Data/Product | Operations |
| Restore failure | Data Recovery | Operations/Architecture |
| Deployment failure | Release Operator | Operations/Architecture |

## 156. Escalation triggers

- severity increase;
- deadline exceeded;
- user/data impact expands;
- repeated workaround failure;
- evidence conflict;
- owner unavailable;
- security implication;
- restore/rollback uncertainty.

## 157. Operational alerts inventory direction

Critical alerts include:

```text
database_unavailable
critical_store_unavailable
outbox_age_critical
consumer_lag_critical
fencing_conflict
unknown_effect_surge
approval_replay
cross_workspace_denial_surge
secret_exposure
artifact_quarantine_surge
backup_overdue
restore_failed
disk_capacity_critical
adapter_security_drift
emergency_stop_failed
```

## 158. Alert response

For every alert:

1. acknowledge;
2. verify signal/freshness;
3. identify environment/scope;
4. consult runbook;
5. contain;
6. diagnose;
7. resolve/recover;
8. verify;
9. document;
10. tune alert if needed.

## 159. Alert suppression

Suppression requires:

- maintenance or known condition;
- scope;
- owner;
- expiry;
- remaining protection;
- audit.

A0 suppression is exceptional and highly governed.

## 160. False-positive alert

Do not simply disable.

- verify data/source;
- assess hidden risk;
- adjust query/threshold;
- test;
- document;
- preserve event.

## 161. Observability-backend unavailable

Actions:

- mark observability degraded;
- rely on authoritative state and local diagnostics;
- preserve local buffers;
- ensure audit remains separate;
- restore backend;
- inspect dropped signals;
- alert on critical evidence loss.

## 162. Diagnostic-bundle runbook

1. define scope/time/workspace;
2. authorize;
3. collect bounded signals;
4. redact;
5. generate manifest/hash;
6. classify;
7. verify;
8. share through controlled channel;
9. expire/delete according to policy.

## 163. Diagnostic-bundle failure

- do not collect broader raw data as shortcut;
- identify failing source;
- produce partial bundle with gaps;
- preserve classification;
- escalate if required for incident.

## 164. Capacity-management runbook

Review:

- CPU/memory;
- disk;
- database connections;
- worker saturation;
- queue age;
- artifact growth;
- telemetry growth;
- backup capacity;
- provider quota;
- cost budget.

## 165. Capacity warning

Actions:

- determine trend and time to exhaustion;
- reduce noncritical workload;
- expand capacity;
- clean only governed derived/expired data;
- validate backup space;
- update forecast.

## 166. Capacity critical

- no-new-runs or no-protected-actions;
- protect database and artifacts;
- stop noncritical ingestion;
- expand immediately;
- incident if service/data risk.

## 167. Cost-operations cadence

- daily/weekly budget review;
- unknown/unattributed cost;
- provider mismatch;
- pricing freshness;
- stale reservations;
- pilot spend.

## 168. Cost containment

Possible actions:

- pause cost-incurring capabilities;
- disable provider binding;
- reduce concurrency;
- use approved lower-cost profile;
- adjust budget with authority;
- preserve active work safely.

## 169. Maintenance planning

Maintenance plan includes:

- purpose;
- scope;
- environment;
- impact;
- start/end;
- owner;
- prerequisites;
- backup;
- actions;
- alerts suppressed;
- validation;
- rollback;
- communication.

## 170. Maintenance start checklist

- approval;
- communication;
- environment lock;
- state change;
- active runs reviewed;
- backup;
- monitoring;
- support available.

## 171. Maintenance completion checklist

- action completed;
- migrations verified;
- services ready;
- smoke passed;
- queues normal;
- alerts checked;
- state returned;
- users informed;
- record closed.

## 172. Change-management categories

```text
standard_change
normal_change
emergency_change
```

## 173. Standard change

Pre-approved low-risk repeatable change with documented procedure and tests.

It still records execution.

## 174. Normal change

Requires assessment, approval, scheduling, deployment plan, and verification.

## 175. Emergency change

Used to contain urgent severe risk.

Requires:

- emergency authority;
- bounded scope;
- evidence;
- retrospective review;
- follow-up tests/docs.

## 176. Operational exception

An exception records:

- control/runbook deviation;
- reason;
- risk;
- compensating measure;
- owner;
- expiry;
- monitoring;
- approvers.

## 177. Configuration-change runbook

- identify exact key;
- assess security/data impact;
- update controlled source;
- validate;
- compare config fingerprint;
- deploy/reload;
- verify;
- rollback if needed;
- record.

## 178. Feature-flag runbook

- identify flag/owner/expiry;
- verify environment/workspace;
- evaluate data migration/state;
- change;
- observe;
- revert if needed;
- remove expired flag.

Security controls are not ordinary flags.

## 179. Adapter enablement runbook

- registration;
- version;
- conformance;
- capability validation;
- secret/network;
- workspace enablement;
- policy;
- smoke;
- monitoring;
- owner/runbook.

## 180. Adapter disablement runbook

- block new dispatch;
- list active sessions;
- reconcile/cancel;
- preserve evidence;
- disable/revoke;
- update readiness;
- communicate.

## 181. Model-profile enablement runbook

- validate logical profile;
- provider binding;
- data policy;
- region;
- quota;
- cost/pricing;
- secret;
- fallback;
- smoke;
- monitor actual identity.

## 182. Provider-binding revocation

- block routing;
- preserve active requests;
- reconcile;
- invalidate fallback assumptions;
- update workspaces;
- rotate/revoke secret if needed;
- communicate.

## 183. Workspace suspension runbook

Reasons:

- security;
- contract;
- data issue;
- operator request.

Actions:

- block new work;
- preserve reads/evidence as policy allows;
- handle active runs;
- revoke sessions/permissions as required;
- audit;
- define release conditions.

## 184. Workspace archival runbook

- no active protected work;
- data/export/retention reviewed;
- adapters/providers detached;
- backups/holds;
- archive;
- verify no new activity;
- preserve evidence.

## 185. Emergency-stop activation runbook

1. identify scope and reason;
2. activate through authoritative command;
3. verify new protected dispatch blocked;
4. verify approval consumption blocked;
5. inspect active work;
6. signal cancel/contain where safe;
7. alert stakeholders;
8. preserve evidence;
9. open incident if required.

## 186. Emergency-stop release runbook

Requires:

- cause understood;
- containment verified;
- security/data review;
- affected runs reconciled;
- controls tested;
- explicit approval;
- gradual resume;
- observation window;
- audit.

## 187. Operational readiness checklist

Before pilot:

- environment inventory;
- named operators;
- startup/shutdown tested;
- deployment/migration tested;
- emergency stop tested;
- alerts/runbooks;
- backup/restore drill;
- stale/unknown reconciliation;
- adapter/provider runbooks;
- support;
- incident process;
- known limitations.

## 188. Pilot-day checklist

- verify build/config;
- verify backups;
- verify adapters/models;
- verify budgets;
- verify support contacts;
- verify emergency stop;
- monitor active runs;
- record user-impacting events;
- perform end-of-day review.

## 189. Pilot stop criteria

Stop pilot for:

- A0/S0;
- cross-workspace leak;
- approval bypass;
- uncontrolled effect;
- material data corruption;
- restore unavailability;
- repeated operator inability to reconcile;
- critical inaccessible workflow;
- uncontrolled cost.

## 190. Controlled-commercial readiness

Additional operations requirements:

- supported deployment profile;
- patch/update process;
- vulnerability response;
- support hours and escalation;
- customer communication;
- service objectives;
- continuity;
- access review;
- audit retention;
- end-of-life process.

## 191. Operations documentation set

Required:

- environment inventory;
- service inventory;
- alert inventory;
- runbook catalogue;
- access matrix;
- maintenance calendar;
- backup/restore records;
- deployment records;
- migration records;
- incident records;
- known issues;
- operational exceptions;
- support guide.

## 192. Runbook structure

Each runbook should include:

```text
purpose
scope
triggers
severity
prerequisites
authorities
safety constraints
diagnosis
containment
recovery
verification
communication
evidence
rollback
escalation
follow-up
```

## 193. Runbook execution record

Fields:

- runbook ID/version;
- trigger;
- environment;
- subject;
- operator;
- start/end;
- steps/actions;
- deviations;
- evidence;
- result;
- follow-up.

## 194. Runbook testing

Runbooks are tested through:

- tabletop exercise;
- simulation;
- integration test;
- fault injection;
- restore drill;
- pilot rehearsal.

## 195. Runbook review cadence

Review after:

- incident;
- failed drill;
- architecture change;
- adapter/provider change;
- deployment change;
- major release;
- elapsed review period.

## 196. Operational KPIs

Potential metrics:

- environment readiness;
- stale/unknown runs;
- mean time to acknowledge;
- mean time to recover;
- dead-letter age;
- backup success;
- restore drill success;
- deployment failure;
- rollback frequency;
- adapter readiness;
- alert noise;
- runbook exercise pass rate;
- support volume;
- exception age.

## 197. KPI cautions

Do not:

- hide severity in averages;
- treat unknown as zero;
- reward premature incident closure;
- compare environments without context;
- use MTTR alone as quality proof.

## 198. Operational audit

Audit:

- privileged login;
- maintenance state;
- deployment;
- migration;
- emergency stop;
- restore;
- secret rotation;
- adapter/provider enablement;
- manual state resolution;
- diagnostic export;
- incident decisions.

## 199. Operational evidence retention

Retention depends on:

- incident;
- release;
- security;
- restore;
- pilot/commercial commitments;
- data classification;
- legal holds.

## 200. Operational security

Operations systems must protect:

- deployment credentials;
- backup keys;
- database admin;
- secret manager;
- host access;
- diagnostic bundles;
- incident evidence;
- customer/workspace data.

## 201. Operational tooling requirements

Selected tools should support:

- environment inventory;
- health and alerts;
- change/deployment records;
- incident records;
- runbook execution;
- access control;
- evidence links;
- exception expiry;
- audit.

Final tools require ADR.

## 202. Automation boundaries

Operational automation may:

- run health checks;
- collect diagnostics;
- rotate logs;
- schedule backups;
- expire leases;
- detect drift;
- open alerts;
- execute pre-approved bounded standard changes.

It may not autonomously:

- release emergency stop;
- restore production data;
- execute destructive migration;
- grant access;
- approve protected effects;
- merge/deploy unapproved code.

## 203. ChatOps direction

A future ChatOps interface must:

- authenticate user;
- show exact target;
- require approval for critical commands;
- avoid secret content;
- preserve audit;
- use idempotency;
- reject ambiguous natural-language actions.

## 204. Command-line administration direction

CLI commands should:

- print environment and target;
- support machine and human output;
- use safe confirmation;
- return stable error codes;
- support dry run;
- emit audit;
- avoid secret echo;
- require reauthentication for critical action.

## 205. Operational API direction

Potential resources:

```text
/environments
/maintenance-windows
/emergency-stops
/recovery-operations
/deployment-operations
/migration-operations
/diagnostic-bundles
/incidents
/operational-exceptions
/runbook-executions
```

## 206. Operational event direction

Potential events:

```text
EnvironmentStateChanged
MaintenanceStarted
MaintenanceCompleted
EmergencyStopActivated
EmergencyStopReleased
RecoveryStarted
RecoveryCompleted
RunReconciliationRequired
DeadLetterRemediationStarted
AdapterRevoked
BackupOverdue
RestoreFailed
IncidentDeclared
IncidentResolved
RunbookExecuted
```

Schemas require future `EVT-001` update.

## 207. Error-code direction

```text
OPS_ENVIRONMENT_UNKNOWN
OPS_STARTUP_BLOCKED
OPS_RECOVERY_REQUIRED
OPS_MAINTENANCE_ACTIVE
OPS_EMERGENCY_STOP_ACTIVE
OPS_DEPLOYMENT_LOCKED
OPS_MIGRATION_INCOMPLETE
OPS_RESTORE_BLOCKED
OPS_BACKUP_UNVERIFIED
OPS_RUN_RECONCILIATION_REQUIRED
OPS_ADAPTER_NOT_READY
OPS_CAPACITY_CRITICAL
OPS_DIAGNOSTIC_INCOMPLETE
OPS_PRIVILEGE_REQUIRED
OPS_RUNBOOK_DEVIATION
```

## 208. Testing strategy

Operational verification includes:

```text
startup
shutdown
restart
maintenance
deployment
migration
rollback
run recovery
unknown effect
event backlog
dead letter
adapter outage
provider outage
artifact failure
backup
restore
emergency stop
incident exercise
support
```

## 209. Startup tests

Verify:

- clean start;
- invalid configuration;
- missing volume;
- database unavailable;
- unfinished migration;
- nonterminal runs;
- expired leases;
- emergency stop;
- degraded optional service.

## 210. Shutdown tests

Verify:

- no-new-runs;
- graceful worker stop;
- adapter session preservation;
- outbox persistence;
- forced termination;
- startup recovery.

## 211. Run-recovery tests

Verify:

- lost worker;
- stale lease;
- timeout before effect;
- timeout after effect;
- cancellation unknown;
- late provider result;
- duplicate event;
- receipt gap.

## 212. Deployment tests

Verify:

- approved digest;
- configuration drift;
- migration;
- partial deployment;
- failed readiness;
- smoke;
- rollback;
- environment lock.

## 213. Backup/restore tests

Verify:

- backup failure;
- manifest;
- corruption;
- isolated restore;
- consumed approvals;
- tombstones;
- inbox/outbox;
- nonterminal runs;
- artifacts;
- indexes.

## 214. Incident exercises

Tabletop and technical exercises:

- cross-workspace leak;
- approval replay;
- database loss;
- adapter compromise;
- secret exposure;
- sandbox violation;
- restore failure;
- provider outage;
- disk full.

## 215. Support tests

Verify:

- safe intake;
- correlation lookup;
- workspace authorization;
- diagnostic bundle;
- escalation;
- privacy-safe communication.

## 216. Quality-gate integration

Before pilot, `QAG-001` should require:

- runbook inventory;
- exercised critical runbooks;
- named owners;
- alert/runbook mapping;
- backup/restore evidence;
- emergency stop evidence;
- startup/shutdown evidence;
- support and escalation;
- known limitations.

## 217. Requirement catalogue

### Operational governance

- `OPS-REQ-GOV-001` — Environments have named owners and states.
- `OPS-REQ-GOV-002` — Critical operational actions are audited.
- `OPS-REQ-GOV-003` — Operators use named identities.
- `OPS-REQ-GOV-004` — High-risk actions separate request, approval, execution, and verification.
- `OPS-REQ-GOV-005` — Runbooks are versioned and owned.
- `OPS-REQ-GOV-006` — Deviations and exceptions are recorded.
- `OPS-REQ-GOV-007` — Communication reflects certainty.
- `OPS-REQ-GOV-008` — Automation cannot self-authorize critical work.

### Service and recovery

- `OPS-REQ-SRV-001` — Startup verifies configuration, schema, stores, and recovery state.
- `OPS-REQ-SRV-002` — Shutdown prevents new dispatch and preserves durable state.
- `OPS-REQ-SRV-003` — Health and readiness are distinct.
- `OPS-REQ-SRV-004` — Unknown effects block blind retry.
- `OPS-REQ-SRV-005` — Stale leases use reconciliation and fencing.
- `OPS-REQ-SRV-006` — Event/job backlogs and dead letters are operable.
- `OPS-REQ-SRV-007` — Partial deployment is explicit.
- `OPS-REQ-SRV-008` — Emergency stop is testable and auditable.

### Deployment and maintenance

- `OPS-REQ-DPM-001` — Deployments use approved candidate digests.
- `OPS-REQ-DPM-002` — Deployment preflight validates drift, backup, migration, and capacity.
- `OPS-REQ-DPM-003` — Migrations are explicit and verified.
- `OPS-REQ-DPM-004` — Maintenance modes are explicit.
- `OPS-REQ-DPM-005` — Environment locks prevent conflicting operations.
- `OPS-REQ-DPM-006` — Rollback compatibility is assessed.
- `OPS-REQ-DPM-007` — Deployment observation and smoke are required.
- `OPS-REQ-DPM-008` — Failed deployments remain contained and evidenced.

### Data, backup, and security

- `OPS-REQ-DBS-001` — Backup failures are alerted and remediated.
- `OPS-REQ-DBS-002` — Restore preflight validates exact backup and target.
- `OPS-REQ-DBS-003` — Post-restore reconciliation preserves approvals, tombstones, and deduplication.
- `OPS-REQ-DBS-004` — Secret exposure triggers revocation and incident handling.
- `OPS-REQ-DBS-005` — Cross-workspace reports are treated as high severity.
- `OPS-REQ-DBS-006` — Artifact and memory integrity failures block unsafe use.
- `OPS-REQ-DBS-007` — Diagnostic exports are scoped and redacted.
- `OPS-REQ-DBS-008` — Audit failure blocks protected actions where required.

### Support and incident

- `OPS-REQ-SUP-001` — Support intake captures workspace, environment, time, and correlation.
- `OPS-REQ-SUP-002` — Support never requests raw credentials.
- `OPS-REQ-SUP-003` — Incidents have commander, timeline, evidence, and state.
- `OPS-REQ-SUP-004` — A0 incidents trigger immediate containment.
- `OPS-REQ-SUP-005` — Incident closure requires safe state and monitoring.
- `OPS-REQ-SUP-006` — Post-incident review assigns corrective actions.
- `OPS-REQ-SUP-007` — Pilot stop criteria are explicit.
- `OPS-REQ-SUP-008` — Operational readiness is quality-gated before pilot.

## 218. Traceability

| Source | OPS-001 response |
|---|---|
| `DEP-001` | Environments, deployment, migration, maintenance, rollback |
| `SEC-001` | Privilege, containment, secrets, security events |
| `THR-001` | Abuse and incident triggers |
| `ORC-001` | Workers, jobs, leases, recovery |
| `RUN-001` | Run diagnosis, cancellation, retry, reconciliation |
| `APR-001` | Approval operations and replay |
| `ART-001` | Artifact integrity, quarantine, preview, deletion |
| `EVT-001` | Outbox, inbox, gaps, dead letters, replay |
| `OBS-001` | Health, alerts, dashboards, diagnostic evidence |
| `TST-001` | Operational tests and drills |
| `QAG-001` | Operational readiness gates |
| `BCP-001` | Continuity, RPO/RTO, disaster recovery |

## 219. Mapping to operational components

| Area | Primary components |
|---|---|
| User access | Mission Control, API |
| Run operations | Orchestrator, workers, job store |
| Adapter operations | Adapter Gateway, Hermes/Codex adapters |
| Model operations | Model Gateway |
| Tool operations | Tool Gateway, sandbox |
| Artifact operations | Artifact Service, content store, preview workers |
| Memory operations | Memory Service, indexes |
| Events | Outbox/inbox/event consumers |
| Data | Transactional database |
| Audit/evidence | Audit and Receipt services |
| Costs | Cost Service |
| Operations | Operations Service, telemetry, backup/restore |

## 220. ADR backlog

### `ADR-CANDIDATE-OPS-001 — Operational tooling and record system`

Select incident/change/runbook tooling, ticketing, evidence storage, and ownership workflow.

### `ADR-CANDIDATE-OPS-002 — Administrative CLI and operational API`

Define command model, authentication, approvals, idempotency, and audit.

### `ADR-CANDIDATE-OPS-003 — Maintenance, locks, and emergency-stop implementation`

Define environment states, locks/fencing, emergency scope, and release controls.

### `ADR-CANDIDATE-OPS-004 — Incident severity, escalation, and communication`

Confirm A0-A4 mapping, incident declaration, roles, and status communication.

### `ADR-CANDIDATE-OPS-005 — Backup/restore operational interface`

Define backup scheduler, manifests, restore activation, privileges, and reconciliation workflow.

### `ADR-CANDIDATE-OPS-006 — Pilot and controlled-commercial operating model`

Define support coverage, maintenance cadence, access model, and operating responsibilities.

## 221. Open decisions

1. Confirm `DEP-001` autonomous registration.
2. Which operational record/ticketing tool?
3. Which on-call or escalation mechanism?
4. Which exact A0-A4 response targets?
5. Which maintenance modes enter MVP?
6. Which administrative CLI/API?
7. Which break-glass mechanism?
8. Which environment-lock implementation?
9. Which operational command approval profile?
10. Which run-resolution commands?
11. Which alert inventory enters pilot?
12. Which runbooks must be technically exercised before G4?
13. Which support hours for pilot?
14. Which incident communication channel?
15. Which diagnostic bundle retention?
16. Which access-review cadence?
17. Which backup/restore operators?
18. Which maintenance calendar?
19. Which pilot stop authority?
20. Which commercial support model?
21. Which problem-management process?
22. Which operational KPI targets?
23. Which automation qualifies as standard change?
24. Which privileged commands are nondelegable to agents?
25. Which runbook-review cadence?

## 222. Risks

| Risk | Consequence | Response |
|---|---|---|
| Logs treated as truth | Incorrect recovery | Authoritative-state-first |
| Timeout retried blindly | Duplicate effect | Unknown-effect runbook |
| Operator edits DB directly | Broken history/invariants | Governed commands |
| Stale lock deleted casually | Concurrent operation | Lease/fencing recovery |
| Approval consumed twice | Duplicate action | Unique consumption/reconciliation |
| Adapter restored without conformance | Unsafe execution | Readiness validation |
| Backup file assumed valid | Failed recovery | Verification/restore drill |
| Restore revives deleted data | Governance breach | Tombstone checks |
| Emergency stop released early | Repeated incident | Separate release approval |
| Shared admin account | No accountability | Named identity |
| Support asks for secrets | Credential exposure | Safe intake |
| Incident closed before unknowns resolved | Hidden risk | Closure criteria |
| Runbook never exercised | Failure during incident | Drills |
| Alert without owner | No response | Inventory and ownership |
| Maintenance not visible | User confusion/data risk | Explicit state |
| Partial deployment shown healthy | Mixed-version defects | Partial state |
| Small team bypasses separation | Concentrated risk | Recorded multi-role decisions |
| Overautomation | Autonomous critical action | Automation boundaries |
| Diagnostic bundle too broad | Data leakage | Scope/redaction |
| Pilot becomes permanent production | Missing controls | G5 transition |

## 223. Assumptions

- deployment architecture follows `DEP-001`;
- health, alerts, and dashboards from `OBS-001` are available progressively;
- a transactional database and durable stores exist;
- operators can access authoritative data safely;
- runbook exercises can be performed in isolated environments;
- backup and restore tooling can produce evidence;
- adapter/provider status can be queried;
- operational roles can be assigned;
- quality gates can block pilot;
- incident evidence can be retained.

## 224. Constraints

- no direct routine database state edits;
- no blind retry of unknown protected effects;
- no autonomous release, migration, restore, or emergency-stop release;
- no shared generic production administrator account;
- no raw secrets in operational evidence;
- no restore without exact target and approval;
- no deployment success claim for partial state;
- no pilot without critical runbook exercises;
- no final operational tools or response targets selected in this draft;
- no Git commit, push, PR, merge, or release during the current documentation phase;
- Git versioning remains deferred until all drafts and global consistency review are complete.

## 225. Acceptance criteria

OPS-001 may advance to `1.0.0` when:

1. `DEP-001` status and dependency are resolved.
2. Product accepts pilot support, communication, and stop criteria.
3. Architecture accepts run, event, adapter, migration, and recovery procedures.
4. Security accepts access, emergency, secret, incident, and evidence procedures.
5. Data accepts database, artifact, memory, backup, restore, and reconciliation procedures.
6. Operations accepts ownership, cadence, alerts, maintenance, deployment, and runbooks.
7. Quality accepts drills, evidence, readiness gates, and post-incident review.
8. critical runbooks are inventoried and assigned;
9. startup and shutdown are testable;
10. stale/unknown runs are reconcilable without blind retry;
11. deployment and migration partial states are explicit;
12. emergency stop is operationally testable;
13. backup and restore procedures preserve critical invariants;
14. support and incident processes are defined;
15. `BCP-001` can proceed with a stable operational dependency.

## 226. Downstream impact

| Document | Required use |
|---|---|
| `BCP-001` | Continuity roles, recovery operations, crisis procedures |
| `PLG-001` | Plugin operations, enablement, revocation, incident handling |
| `TST-001` | Runbook drills and operational test suites |
| `QAG-001` | Operational readiness gates |
| `OBS-001` | Alert/runbook mapping and dashboards |
| `RTM-001` | Operations requirements-to-tests/evidence mapping |
| Document register | Confirm DEP-001 and OPS dependency |

## 227. Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.1.0`
- Approved by: Product Owner under explicit user authorization to finalize the declared scope
- Finalization note: approval records the documentation baseline only; implementation and verification remain separate evidence gates

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial operations and production runbook covering operating states, roles, startup, shutdown, health, run recovery, unknown effects, jobs, events, adapters, models, approvals, artifacts, memory, audit, costs, backup, restore, deployments, migrations, secrets, incidents, support, maintenance, emergency stop, drills, and governance |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `DEP-001` — Deployment Architecture and Environment Strategy
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `ORC-001` — Workflow and Orchestration Architecture
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `EVT-001` — Event Catalog and Async Contract
- `OBS-001` — Observability Architecture
- `TST-001` — Test Strategy and Verification Plan
- `QAG-001` — Quality Assurance and Release Gates
