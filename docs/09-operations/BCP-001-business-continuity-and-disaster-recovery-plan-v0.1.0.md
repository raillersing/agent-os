---
document_id: BCP-001
title: Agent OS Business Continuity and Disaster Recovery Plan
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
  - DAT-001
  - OPS-001
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
  - OPS-001
  - PLG-001
related_adrs:
  - ADR-CANDIDATE-BCP-001
  - ADR-CANDIDATE-BCP-002
  - ADR-CANDIDATE-BCP-003
  - ADR-CANDIDATE-BCP-004
  - ADR-CANDIDATE-BCP-005
  - ADR-CANDIDATE-BCP-006
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# BCP-001 — Agent OS Business Continuity and Disaster Recovery Plan

> **Status: Approved baseline — 2026-08-13.** This document defines the business continuity and disaster recovery strategy for Agent OS. It covers critical services, business impact, continuity tiers, provisional recovery objectives, backup and restore architecture, degraded operating modes, disaster scenarios, crisis governance, recovery sequencing, data reconciliation, exercises, evidence, communications, and return to normal service. It does not approve final RPO/RTO values, select a final backup product, define legal notification obligations, commit to high availability, or claim multi-site disaster recovery readiness.

## 1. Purpose

Agent OS must preserve safe and understandable service when any of the following occur:

- host failure;
- database loss or corruption;
- artifact-store loss;
- event or job-store corruption;
- adapter outage;
- model-provider outage;
- network outage;
- identity-service outage;
- secret compromise;
- ransomware or destructive malware;
- accidental deletion;
- failed migration;
- failed deployment;
- unavailable observability;
- unavailable backup destination;
- operator unavailability;
- physical-site disruption;
- extended power failure;
- partial restore;
- inconsistent post-restore state;
- unavailable external dependencies.

The plan defines how Agent OS:

1. protects people, data, and evidence;
2. maintains essential service where possible;
3. enters explicit degraded modes;
4. contains further damage;
5. restores authoritative data;
6. reconciles runs, approvals, events, artifacts, memory, and costs;
7. avoids replaying unsafe effects;
8. communicates known impact and uncertainty;
9. returns to controlled service;
10. learns from continuity exercises and incidents.

## 2. Continuity objectives

The continuity strategy must:

- identify critical business and technical functions;
- define minimum viable service;
- prioritize recovery;
- protect authoritative stores;
- preserve consumed approvals and tombstones;
- preserve workspace isolation;
- prevent duplicate external effects;
- preserve audit and evidence;
- support local-first recovery;
- support controlled pilot recovery;
- distinguish backup from restore readiness;
- distinguish failover from recovery;
- define provisional RPO/RTO directions;
- define exercise and review cadence;
- support future commercial continuity requirements;
- remain proportional to a small-team product.

## 3. Non-goals

This plan does not:

- guarantee zero data loss;
- guarantee zero downtime;
- guarantee automatic failover;
- guarantee multi-region recovery;
- define a production SLA;
- authorize restore without approval;
- authorize destructive repair without evidence;
- define final cloud disaster-recovery services;
- replace incident response;
- replace operational runbooks;
- treat local copies as verified backups;
- claim that a container restart is disaster recovery;
- assume that external effects can be rolled back.

## 4. Continuity principles

### `BCP-P-001 — Safety before availability`

The system may remain unavailable rather than resume in a state that could duplicate protected effects, bypass approvals, or expose data.

### `BCP-P-002 — Restore authority, not assumptions`

Recovery restores authoritative data and then reconciles external reality.

### `BCP-P-003 — Backup is not recovery`

A backup is useful only when its integrity, decryptability, compatibility, and restore process are proven.

### `BCP-P-004 — Recovery preserves negative facts`

Consumed approvals, revocations, deletions, tombstones, denials, and emergency stops must survive recovery.

### `BCP-P-005 — External effects are reconciled`

Restoring platform state does not undo or repeat actions already accepted by external systems.

### `BCP-P-006 — Derived stores are rebuildable`

Search indexes, vector indexes, caches, dashboards, and projections are reconstructed from authoritative sources.

### `BCP-P-007 — Continuity modes are explicit`

Read-only, no-new-runs, no-protected-actions, maintenance, recovery, and emergency stop are distinct.

### `BCP-P-008 — Recovery objectives are evidence-based`

RPO and RTO are set from business impact, tested capabilities, and cost—not optimism.

### `BCP-P-009 — Every recovery has a manifest`

The exact backup, target, build, schema, configuration, and reconciliation outcome are recorded.

### `BCP-P-010 — Human authority remains intact`

Agents may assist diagnosis and planning, but cannot autonomously approve restore, release emergency stop, or activate commercial service.

### `BCP-P-011 — Communication distinguishes fact and uncertainty`

Recovery updates state what is confirmed, inferred, pending, or unknown.

### `BCP-P-012 — Continuity is exercised`

Untested procedures are not accepted as proven capability.

## 5. Scope

The plan covers:

```text
people
facilities and hosts
network and power
identity and access
application services
database
event and job stores
artifact content
memory and indexes
audit and receipts
secrets and keys
adapters and providers
observability
backup infrastructure
deployment and configuration
support and communications
```

## 6. Continuity governance

Continuity governance includes:

```text
BusinessContinuityOwner
DisasterRecoveryLead
IncidentCommander
SecurityLead
DataRecoveryLead
ApplicationRecoveryLead
InfrastructureRecoveryLead
CommunicationsLead
QualityReviewer
ProductDecisionOwner
```

## 7. Business Continuity Owner

Accountable for:

- continuity policy;
- business-impact review;
- continuity tiers;
- exercise schedule;
- readiness reporting;
- remediation tracking;
- executive escalation.

For the initial Agent OS profile, this role may be held by the Operations Owner.

## 8. Disaster Recovery Lead

Coordinates technical recovery:

- backup selection;
- recovery environment;
- restore sequencing;
- reconciliation;
- validation;
- handoff to operations.

## 9. Incident Commander

Coordinates the overall event when disruption is also an incident.

Responsibilities:

- containment;
- workstreams;
- decision log;
- communication rhythm;
- recovery authorization;
- closure.

## 10. Security Lead

Owns:

- compromise containment;
- credential revocation;
- key handling;
- forensic preservation;
- security acceptance before service restoration.

## 11. Data Recovery Lead

Owns:

- backup integrity;
- restore execution;
- schema compatibility;
- data reconciliation;
- data-loss assessment;
- manifest verification.

## 12. Application Recovery Lead

Owns:

- services;
- run state;
- jobs;
- events;
- approvals;
- artifacts;
- memory;
- adapters;
- smoke tests.

## 13. Infrastructure Recovery Lead

Owns:

- hosts;
- containers;
- networking;
- storage;
- reverse proxy;
- certificates;
- operating-system readiness;
- capacity.

## 14. Communications Lead

Owns:

- internal updates;
- user/pilot communications;
- status cadence;
- known-impact statements;
- recovery completion announcement.

## 15. Quality Reviewer

Verifies:

- exercise evidence;
- recovery criteria;
- exception handling;
- test results;
- readiness claims;
- corrective actions.

## 16. Product Decision Owner

Decides:

- acceptable degraded service;
- pilot pause or termination;
- feature suspension;
- user communication;
- return-to-service scope.

## 17. Continuity records

The continuity programme uses:

```text
BusinessImpactAssessment
CriticalServiceInventory
RecoveryObjectiveProfile
BackupPolicy
BackupManifest
RestorePlan
RecoveryOperation
ContinuityIncident
ContinuityExercise
ContinuityException
RecoveryReadinessReport
```

## 18. Business impact assessment

The BIA identifies:

- business function;
- users/workspaces affected;
- safety/security impact;
- data impact;
- legal/contractual impact;
- operational dependency;
- maximum tolerable disruption;
- recovery priority;
- manual workaround;
- minimum service.

## 19. Critical-service inventory

Each critical service records:

- service code;
- purpose;
- owner;
- dependencies;
- authoritative stores;
- acceptable degraded mode;
- recovery tier;
- backup scope;
- validation tests;
- external dependencies.

## 20. Continuity tiers

Proposed tiers:

```text
C0 — Safety and control
C1 — Authoritative core
C2 — Essential operations
C3 — Supporting operations
C4 — Convenience and optimization
```

## 21. C0 — Safety and control

Includes:

- emergency stop;
- authentication and authorization;
- workspace isolation;
- approval-consumption integrity;
- audit for protected actions;
- secret revocation;
- prohibited-action enforcement.

C0 must fail closed.

## 22. C1 — Authoritative core

Includes:

- transactional database;
- task/run state;
- approvals;
- event/outbox/inbox state;
- artifact metadata;
- authoritative memory metadata;
- audit and receipts;
- configuration and identity records.

## 23. C2 — Essential operations

Includes:

- control-plane API;
- Mission Control;
- orchestrator;
- workers;
- approved adapters;
- artifact content store;
- backup and restore utilities;
- operational diagnostics.

## 24. C3 — Supporting operations

Includes:

- previews;
- search;
- vector retrieval;
- cost dashboards;
- notifications;
- noncritical providers;
- optional integrations.

## 25. C4 — Convenience and optimization

Includes:

- advanced analytics;
- nonessential visualizations;
- optional automation;
- experimental plugins;
- cached recommendations.

## 26. Recovery priority

Default recovery priority:

```text
C0
→ C1
→ C2
→ C3
→ C4
```

Dependencies may require infrastructure to start before a higher-tier function is available, but validation remains tier-driven.

## 27. Minimum viable service

Proposed minimum viable continuity state:

- named users can authenticate;
- workspace scope is enforced;
- current authoritative state can be read;
- no protected action occurs without valid controls;
- emergency stop is visible;
- consumed approvals remain consumed;
- users can see service limitations;
- operators can inspect and reconcile recovery state.

## 28. Minimum safe service modes

```text
read_only_continuity
control_only
local_offline_safe
recovery_only
```

## 29. Read-only continuity

Allows:

- viewing tasks, runs, approvals, artifacts metadata, receipts, and audit;
- downloading previously accepted artifacts if storage is available and policy permits;
- support and diagnostics.

Blocks new writes and effects.

## 30. Control-only mode

Allows:

- emergency stop;
- revocation;
- cancellation requests;
- access control;
- incident operations;
- evidence collection.

Normal user workflows remain blocked.

## 31. Local-offline-safe mode

Allows local capabilities that do not need unavailable external dependencies.

Examples:

- read-only state;
- simulator;
- local model where approved;
- local artifact access;
- local support.

External work remains queued or blocked explicitly.

## 32. Recovery-only mode

Only recovery operators can:

- inspect;
- restore;
- reconcile;
- rebuild;
- validate.

Ordinary users and workflows remain unavailable.

## 33. Recovery objective concepts

```text
MTPD — Maximum Tolerable Period of Disruption
RTO  — Recovery Time Objective
RPO  — Recovery Point Objective
WRT  — Work Recovery Time
MTDL — Maximum Tolerable Data Loss direction
```

## 34. RTO

RTO is the target duration to restore a defined service level after disruption.

It is:

- service-specific;
- environment-specific;
- measured from declared disruption;
- validated by exercise;
- not a guarantee.

## 35. RPO

RPO is the maximum targeted age of recoverable authoritative data.

It is:

- store-specific;
- constrained by backup frequency and durability;
- not equivalent to zero external-effect uncertainty;
- validated by backup and restore evidence.

## 36. Work Recovery Time

WRT covers:

- data reconciliation;
- user validation;
- backlog processing;
- incident communication;
- business return to normal.

Service may be technically available before work recovery completes.

## 37. Provisional objective profiles

These values are proposals for design discussion only.

| Profile | Environment | Provisional RPO direction | Provisional RTO direction |
|---|---|---:|---:|
| `RCP-DEV` | Development | Up to 24 hours | Best effort |
| `RCP-LOCAL` | Canonical local | Up to 4 hours | Up to 8 hours |
| `RCP-PILOT` | Controlled pilot | Up to 1 hour | Up to 4 hours |
| `RCP-COMMERCIAL` | Controlled commercial | To be approved, likely stricter | To be approved, likely stricter |
| `RCP-FUTURE` | Multi-tenant production | Separate programme | Separate programme |

These targets are not approved commitments.

## 38. Critical-control objective direction

For C0 controls:

- recovery should be prioritized immediately;
- fail-closed state is acceptable;
- unsafe fail-open state is not;
- objective may be to restore control before normal service.

## 39. Objective-setting method

For each service:

1. identify impact;
2. identify dependencies;
3. determine minimum service;
4. estimate data change rate;
5. identify external-effect exposure;
6. assess cost;
7. define provisional RPO/RTO;
8. test;
9. revise based on evidence;
10. approve.

## 40. Objective exceptions

If tested capability cannot meet the objective:

- record gap;
- adjust architecture or target;
- add compensating control;
- disclose pilot/commercial limitation;
- do not report target as achieved.

## 41. Dependency mapping

Critical dependencies include:

```text
host and power
Linux/WSL runtime
container engine
database
artifact content store
event/job stores
identity
secrets
network
reverse proxy/TLS
adapters
model providers
observability
backup destination
operators
```

## 42. Single points of failure

Potential local/pilot SPOFs:

- one host;
- one database instance;
- one artifact volume;
- one backup disk;
- one operator;
- one secret/key;
- one network connection;
- one adapter runtime;
- one provider.

Each must be recorded with mitigation and residual risk.

## 43. People continuity

Measures:

- named alternates;
- documented runbooks;
- credential escrow or break-glass where approved;
- handover;
- exercise participation;
- no single undocumented expert dependency.

## 44. Facility continuity

For pilot or on-premises deployment:

- alternate working location;
- physical access;
- power protection;
- environmental risks;
- equipment replacement;
- backup transport;
- shutdown procedure.

## 45. Power continuity

Potential controls:

- UPS;
- safe shutdown;
- auto-start policy;
- battery monitoring;
- backup power;
- off-host backup.

Final controls depend on deployment context.

## 46. Network continuity

Modes:

- local LAN only;
- local offline;
- alternate link;
- provider-independent local mode;
- delayed external work.

Network recovery must not silently reroute confidential data to an unapproved endpoint.

## 47. Identity continuity

When identity service is unavailable:

- no fail-open login;
- existing sessions follow approved policy;
- critical reauthentication-dependent actions block;
- local emergency access may require controlled break-glass;
- recovery is audited.

## 48. Secret and key continuity

Plan must address:

- secret backup or re-provisioning;
- key loss;
- key compromise;
- rotation;
- certificate renewal;
- backup encryption keys;
- separation from backup data.

A backup without its decryption key is not recoverable.

## 49. Backup architecture

Backup coverage includes:

```text
transactional database
event/outbox/inbox state
artifact content
artifact metadata
memory records
audit and receipts
configuration snapshots
deployment manifests
secret references
selected indexes or rebuild metadata
observability evidence where required
```

Raw secret values are handled through dedicated secure processes, not ordinary backup manifests.

## 50. Backup types

```text
full
incremental
differential
transaction_log_or_WAL
snapshot
configuration_export
artifact_manifest
offline_copy
```

Final types depend on selected technologies.

## 51. Backup policy dimensions

Each backup policy defines:

- scope;
- schedule;
- method;
- consistency;
- encryption;
- destination;
- retention;
- verification;
- restore test;
- owner;
- alerting;
- legal hold.

## 52. Backup consistency groups

Related stores may require a coordinated consistency point.

Example group:

```text
database
+ artifact manifest
+ event/inbox/outbox state
+ configuration snapshot
```

Exact cross-store consistency strategy requires ADR.

## 53. Database backup

Must preserve:

- schema;
- data;
- transactional consistency;
- consumed approvals;
- idempotency records;
- inbox/outbox;
- audit references;
- tombstones.

## 54. Artifact-content backup

Must preserve:

- object keys;
- content hashes;
- sizes;
- classification metadata references;
- deletion/tombstone semantics;
- quarantine state where applicable.

## 55. Event and job backup

Must preserve:

- outbox;
- inbox;
- event history;
- dead letters;
- job state;
- lease/recovery context;
- replay boundaries.

Restored leases should not remain valid blindly.

## 56. Configuration backup

Must preserve:

- non-secret configuration;
- configuration hash;
- environment inventory;
- feature flags;
- adapter/model profiles;
- policy versions;
- deployment manifests.

## 57. Secret continuity

Options:

- secure re-provisioning;
- dedicated encrypted secret backup;
- external secret manager replication;
- manual recovery ceremony.

The exact secret-recovery design requires ADR and Security approval.

## 58. Backup encryption

Backup encryption must define:

- algorithm/profile;
- key owner;
- key storage;
- rotation;
- recovery;
- verification;
- access;
- loss procedure.

## 59. Backup destinations

Potential destinations:

```text
local protected disk
external encrypted disk
approved network storage
approved object storage
offline rotation
```

## 60. Failure-domain separation

At least one continuity copy should, where required, be outside the primary failure domain.

Examples:

- different disk;
- different host;
- different physical location;
- offline medium;
- independent storage service.

## 61. 3-2-1 direction

A future commercial profile may adopt a 3-2-1-style strategy:

- multiple copies;
- different media;
- one off-site/offline.

This is a direction, not an approved MVP requirement.

## 62. Backup retention classes

Proposed:

```text
hourly_short
daily_standard
weekly_extended
monthly_archive
incident_hold
pre_migration
pre_release
```

Exact durations require policy approval.

## 63. Backup immutability

For ransomware and destructive incidents, at least one protected copy should be:

- immutable;
- offline;
- write-once;
- or otherwise isolated from compromised runtime credentials.

## 64. Backup verification

Verification includes:

- file/object presence;
- size;
- checksum;
- manifest;
- decryptability;
- database consistency;
- content-store references;
- schema metadata;
- restore-tool compatibility.

## 65. Backup success states

```text
completed_verified
completed_unverified
completed_with_warnings
failed
partial
unknown
```

Only `completed_verified` satisfies normal recovery evidence.

## 66. Backup failure handling

A failure triggers:

- alert;
- owner;
- investigation;
- retry;
- exposure-window assessment;
- continuity-risk update;
- escalation if objective threatened.

## 67. Backup monitoring

Monitor:

- last success;
- last verified success;
- backup age;
- size trend;
- duration;
- destination capacity;
- encryption/key state;
- restore-drill age.

## 68. Restore architecture

Restore consists of:

```text
selection
→ verification
→ authorization
→ environment preparation
→ data restore
→ compatibility migration
→ reconciliation
→ validation
→ controlled return to service
```

## 69. Restore target types

```text
isolated_test
recovery_sandbox
replacement_local
pilot_recovery
commercial_recovery
forensic_copy
```

## 70. Restore selection

Select by:

- environment;
- incident time;
- integrity;
- objective;
- known compromise window;
- schema compatibility;
- artifact completeness;
- key availability;
- external-effect exposure.

## 71. Known-good point

A known-good restore point requires evidence that:

- compromise/corruption had not occurred;
- backup is verified;
- configuration is known;
- schema is compatible;
- external effects after the point are inventoried.

## 72. Restore authorization

Restore requires:

- exact backup manifest;
- exact target;
- reason;
- impact;
- approvers;
- maintenance/emergency state;
- current-state preservation where possible;
- stop conditions.

## 73. Restore environment preparation

Steps:

- isolate target;
- secure network;
- install verified build;
- provision configuration;
- provision secret references;
- validate storage capacity;
- disable schedulers/adapters;
- verify time;
- prepare evidence capture.

## 74. Restore order

Recommended logical order:

```text
infrastructure
→ database
→ artifact content
→ event/job state
→ audit/evidence
→ configuration
→ application services without dispatch
→ reconciliation
→ derived stores
→ adapters/providers
→ user access
```

## 75. Post-restore startup restrictions

Initially:

- no new runs;
- no protected actions;
- no approval consumption;
- no external retry;
- adapters disabled or read-only;
- recovery operators only.

## 76. Post-restore reconciliation domains

```text
identity and workspace
roles and revocations
tasks and snapshots
runs and attempts
jobs and leases
approvals and consumptions
events and inbox/outbox
artifacts and content
memory and indexes
audit and receipts
usage and cost
external effects
```

## 77. Identity reconciliation

Verify:

- users;
- memberships;
- roles;
- revocations;
- suspended workspaces;
- sessions invalidated as required;
- break-glass state.

## 78. Run reconciliation

For each nonterminal run:

- identify last durable state;
- identify last reliable external evidence;
- expire leases;
- block blind redispatch;
- classify effect certainty;
- choose recovery action;
- preserve history.

## 79. Approval reconciliation

Verify:

- approved decisions;
- rejections;
- expiry;
- invalidation;
- consumption uniqueness;
- consumed approvals remain consumed;
- grants and revocations;
- no replay.

## 80. Event reconciliation

Verify:

- outbox;
- inbox;
- event versions;
- gaps;
- duplicate protection;
- dead letters;
- replay boundaries;
- projection cursors.

## 81. Artifact reconciliation

Verify:

- metadata/content correspondence;
- hashes;
- quarantine;
- accepted version;
- previews;
- deletions/tombstones;
- exports;
- missing/orphan content.

## 82. Memory reconciliation

Verify:

- records and versions;
- authority/source;
- conflicts;
- tombstones;
- index rebuild;
- cross-workspace scope;
- deletion propagation.

## 83. Audit reconciliation

Verify:

- protected-action audit;
- gaps;
- receipt linkage;
- incident evidence;
- restore operation audit.

Missing audit is explicit and may block service restoration.

## 84. Cost reconciliation

Verify:

- usage events;
- deduplication;
- budget reservations;
- costs after restore point;
- provider statements;
- unknown/mismatch;
- no zero substitution.

## 85. External-effect reconciliation

Examples:

- Git commits/pushes/PRs;
- messages;
- calendar events;
- files;
- provider jobs;
- external artifacts;
- API mutations.

Platform rollback does not undo these automatically.

## 86. Restore validation

Validation includes:

- schema;
- constraints;
- workspace isolation;
- authentication;
- consumed approvals;
- run recovery state;
- event deduplication;
- artifact integrity;
- memory tombstones;
- audit;
- backup chain;
- health/readiness;
- smoke tests.

## 87. Restore result states

```text
restored_verified
restored_with_gaps
restored_partial
restore_failed
recovery_required
unknown
```

## 88. Return-to-service criteria

Service resumes only when:

- C0 controls are verified;
- C1 authoritative data is consistent;
- critical gaps are understood;
- no blind redispatch path remains;
- emergency stop release is approved;
- required services are ready;
- smoke tests pass;
- monitoring is active;
- communication is approved.

## 89. Progressive service restoration

Recommended progression:

```text
recovery_only
→ read_only_continuity
→ no_protected_actions
→ limited safe runs
→ normal or degraded service
```

## 90. Recovery observation window

Monitor:

- run anomalies;
- approval mismatches;
- event duplicates/gaps;
- adapter errors;
- artifact integrity;
- memory index consistency;
- costs;
- security alerts;
- storage;
- backups.

## 91. Recovery completion

Recovery completes when:

- objectives assessed;
- essential work resumed;
- backlogs controlled;
- unknowns documented;
- users informed;
- evidence complete;
- corrective actions opened.

## 92. Disaster scenarios

The plan addresses:

```text
host_loss
database_loss
database_corruption
artifact_store_loss
event_store_corruption
ransomware
credential_compromise
network_outage
power_outage
site_unavailable
failed_deployment
failed_migration
operator_unavailable
provider_outage
identity_outage
observability_loss
backup_destination_loss
```

## 93. Host loss

Containment:

- declare environment unavailable;
- prevent duplicate alternate starts if state uncertain;
- preserve surviving storage;
- identify latest verified backup;
- inventory external effects.

Recovery options:

- replacement host;
- restored containers/services;
- restored data;
- reconciliation;
- controlled return.

## 94. Database loss

Actions:

- emergency stop/no-protected-actions;
- isolate failed store;
- preserve logs/volumes;
- select backup;
- restore database;
- reconcile content/events/external effects;
- rebuild projections.

## 95. Database corruption

Actions:

- stop writes;
- identify corruption scope/time;
- preserve forensic copy;
- choose repair versus restore;
- validate backups before use;
- perform full reconciliation;
- treat hidden corruption as high risk.

## 96. Artifact-store loss

Possible continuity:

- metadata remains read-only;
- new artifact operations blocked;
- previously external copies not trusted as canonical.

Recovery:

- restore content;
- verify hashes;
- identify missing objects;
- rebuild previews;
- reconcile exports/deletions.

## 97. Event-store corruption

Actions:

- stop consumers/producers as needed;
- preserve authoritative aggregate state;
- identify affected streams;
- restore/reconstruct from outbox/audit where possible;
- verify deduplication and ordering;
- rebuild projections.

## 98. Ransomware

Immediate:

- isolate network/host;
- disable credentials;
- emergency stop;
- preserve evidence;
- do not connect clean backups to compromised environment;
- identify compromise window;
- rebuild from trusted media;
- rotate secrets;
- restore and reconcile;
- security review before return.

## 99. Credential compromise

Actions:

- revoke/rotate;
- block affected providers/adapters;
- inspect usage and access;
- preserve audit;
- determine data exposure;
- restore trust chain;
- validate clean configuration;
- monitor.

## 100. Network outage

Continuity modes:

- local read-only;
- local safe operation;
- external jobs blocked/queued;
- no silent provider rerouting;
- manual communication channel.

Recovery:

- restore link;
- verify DNS/TLS;
- reconcile timed-out requests;
- release queues gradually.

## 101. Power outage

Actions:

- safe shutdown if possible;
- preserve UPS state;
- after power returns, inspect storage and time;
- run startup recovery;
- verify database/artifacts;
- reconcile active external work.

## 102. Site unavailable

Recovery may require:

- alternate site or host;
- off-site backup;
- alternate operator access;
- network/DNS update;
- user communication;
- hardware replacement.

MVP may accept longer recovery with documented limitation.

## 103. Failed deployment

Actions:

- stop promotion;
- identify partial versions;
- maintenance;
- rollback/forward-fix;
- verify schema;
- restore only if necessary;
- preserve release evidence.

## 104. Failed migration

Actions:

- freeze writes;
- inspect transactional/checkpoint state;
- choose resume, forward-fix, or restore;
- validate data;
- do not rerun blindly;
- remain in maintenance.

## 105. Operator unavailable

Continuity controls:

- named alternate;
- runbooks;
- access escrow/break-glass;
- handover;
- decision matrix;
- external support if approved.

## 106. Provider outage

Continuity:

- block affected binding;
- local/offline or alternate approved provider where policy permits;
- preserve queued work;
- no silent fallback;
- reconcile in-flight requests.

## 107. Identity outage

Continuity:

- fail closed for new auth;
- existing session policy;
- no privilege expansion;
- controlled break-glass for emergency operations;
- restore identity service;
- review sessions.

## 108. Observability loss

Continuity:

- use authoritative state/local diagnostics;
- mark monitoring degraded;
- preserve local buffers;
- do not report false green;
- restore telemetry;
- assess evidence gaps.

## 109. Backup-destination loss

Actions:

- preserve current primary data;
- activate alternate destination;
- assess missing backup window;
- create new verified backup;
- restore redundancy;
- update risk.

## 110. Multi-failure scenarios

Exercises must include combinations such as:

- host loss plus backup unavailability;
- database corruption plus compromised credential;
- provider outage during restore;
- migration failure plus disk pressure;
- identity outage during security incident;
- power loss during backup.

## 111. Continuity decision matrix

Decisions consider:

- safety/security;
- authoritative data;
- user impact;
- external effects;
- recovery confidence;
- objective breach;
- available personnel;
- communications;
- cost.

## 112. Activate continuity plan when

- disruption exceeds ordinary runbook;
- multiple critical services fail;
- recovery objectives are threatened;
- site/host is lost;
- data restore is required;
- pilot/commercial service must be suspended;
- crisis coordination is needed.

## 113. Crisis declaration

States:

```text
standby
continuity_activated
disaster_declared
recovery_in_progress
business_restoration
monitoring
closed
```

## 114. Continuity activation procedure

1. detect and triage;
2. protect safety/security;
3. appoint Incident Commander/DR Lead;
4. declare scope/severity;
5. activate emergency/maintenance modes;
6. preserve evidence;
7. assess critical services;
8. choose recovery strategy;
9. communicate;
10. execute and monitor.

## 115. Disaster declaration criteria

- primary environment unavailable beyond tolerable window;
- authoritative data loss/corruption;
- site loss;
- ransomware;
- restore from backup required for service;
- multiple critical failures;
- prolonged pilot/commercial interruption.

## 116. Crisis command rhythm

Suggested:

- initial update rapidly after declaration;
- regular updates based on severity;
- decision checkpoints;
- recovery milestone updates;
- final restoration update.

Exact timings require governance approval.

## 117. Crisis status board

Tracks:

- current state;
- confirmed impact;
- affected services/workspaces;
- critical dependencies;
- recovery objectives;
- workstreams;
- decisions;
- blockers;
- communications;
- next milestone;
- unknowns.

## 118. Communication audiences

```text
internal recovery team
leadership/product owner
pilot users
commercial customers
partners/providers
security/legal advisers
```

## 119. Communication principles

- timely;
- accurate;
- scoped;
- non-speculative;
- privacy-safe;
- consistent;
- actionable;
- explicit about next update.

## 120. Internal continuity update template

```text
Event:
Environment:
Declared at:
Current continuity state:
Confirmed impact:
Affected critical services:
Data/security status:
Recovery objective at risk:
Actions completed:
Actions in progress:
Unknowns:
Next decision point:
Owner:
```

## 121. User update template

```text
Agent OS is currently operating in <mode> due to <high-level issue>.
Affected functions: <scope>.
Available functions: <scope>.
Data status: <confirmed statement or under assessment>.
Current action: <recovery action>.
Next update: <time or milestone>.
```

## 122. Recovery strategy options

```text
repair_in_place
restart_and_reconcile
restore_in_place
restore_to_replacement
rebuild_from_clean
failover_to_alternate
operate_degraded
terminate_pilot
```

## 123. Repair in place

Appropriate when:

- corruption is bounded;
- authoritative state remains trustworthy;
- repair is supported;
- evidence preserved;
- no broader compromise.

## 124. Restart and reconcile

Appropriate for:

- process crash;
- host reboot;
- worker/adapters;
- durable state intact.

## 125. Restore in place

Higher risk because current environment may be compromised or partially overwritten.

Requires strong controls.

## 126. Restore to replacement

Preferred when:

- host trust is uncertain;
- ransomware;
- system corruption;
- clean validation needed.

## 127. Rebuild from clean

Uses:

- trusted build;
- clean host;
- verified configuration;
- re-provisioned secrets;
- verified backups;
- reconciliation.

## 128. Failover to alternate

Future capability may use:

- standby host;
- replicated database;
- alternate storage;
- alternate site.

Not assumed for MVP.

## 129. Operate degraded

Acceptable when:

- safety controls remain;
- data integrity remains;
- limitations are visible;
- business accepts reduced capability.

## 130. Terminate pilot

Required when:

- non-waivable control fails;
- recovery cannot be trusted;
- data exposure unresolved;
- support capacity insufficient;
- pilot risk exceeds acceptance.

## 131. Recovery strategy selection

Selection factors:

- compromise;
- corruption;
- recovery time;
- data loss;
- evidence;
- cost;
- skills;
- external effects;
- backup quality;
- environment availability.

## 132. Derived-store recovery

Rebuild order:

```text
search indexes
→ vector indexes
→ dashboard projections
→ caches
→ previews
```

Only after authoritative stores are verified.

## 133. Projection rebuild

Procedure:

- choose source cursor;
- disable side effects;
- rebuild shadow projection;
- validate counts/hashes;
- switch;
- record freshness.

## 134. Search-index rebuild

Verify:

- workspace filtering;
- tombstones;
- classification;
- source version;
- deletion propagation;
- no cross-workspace leakage.

## 135. Vector-index rebuild

Verify:

- embedding profile/version;
- workspace;
- source memory version;
- deletions;
- classification;
- deterministic rebuild limitations.

## 136. Preview rebuild

Preview is derived.

Rebuild only:

- from verified artifact version;
- in isolated worker;
- with approved renderer version;
- without network by default.

## 137. Backlog recovery

After service restoration:

- prioritize critical work;
- apply fairness;
- avoid retry storms;
- respect deadlines/budgets;
- preserve approval validity;
- monitor provider quotas;
- communicate delays.

## 138. Queue release strategy

```text
paused
→ limited concurrency
→ monitor
→ increase gradually
→ normal
```

## 139. External dependency recovery

When external services return:

- verify endpoint/identity;
- check queued and in-flight work;
- reconcile timed-out operations;
- apply backoff;
- avoid duplicate dispatch;
- restore gradually.

## 140. Continuity testing strategy

Types:

```text
document_review
tabletop
walkthrough
component_restore
application_restore
full_environment_restore
failover_simulation
crisis_communication_exercise
combined_disaster_exercise
```

## 141. Document review

Verifies:

- owners;
- contacts;
- dependencies;
- procedures;
- objectives;
- current environment.

## 142. Tabletop exercise

Participants walk through a scenario and decisions without changing live systems.

## 143. Technical walkthrough

Operators execute safe preparatory steps:

- locate backups;
- validate access;
- inspect manifests;
- identify commands;
- verify communications.

## 144. Component restore test

Restores one store/component in isolation.

Examples:

- database;
- artifact store;
- event store;
- configuration.

## 145. Application restore test

Restores the complete application in isolated environment and runs reconciliation.

## 146. Full-environment restore test

Includes:

- host/environment provisioning;
- services;
- data;
- configuration;
- secrets;
- observability;
- validation;
- user smoke.

## 147. Failover simulation

Future exercise for standby environments.

Not required until failover capability exists.

## 148. Communication exercise

Tests:

- contact lists;
- templates;
- decision authority;
- update cadence;
- privacy-safe messages.

## 149. Combined disaster exercise

Example:

```text
database corruption
+ compromised secret
+ provider outage
```

Tests coordination across Operations, Security, Data, Product, and Quality.

## 150. Exercise cadence direction

Proposed:

| Exercise | Development | Pilot | Controlled commercial |
|---|---:|---:|---:|
| Tabletop | Per milestone | Quarterly direction | Quarterly or stricter |
| Component restore | Per release as needed | Monthly/quarterly direction | Approved cadence |
| Full restore | Before major pilot | Before pilot and periodically | Approved strict cadence |
| Emergency stop | Per milestone | Before pilot | Periodic |
| Communication | Optional | Before pilot | Periodic |

Exact cadence remains unapproved.

## 151. Exercise evidence

Includes:

- scenario;
- objectives;
- environment;
- participants;
- steps;
- timestamps;
- recovery outcome;
- RPO/RTO measured;
- gaps;
- decisions;
- corrective actions;
- reviewer.

## 152. Exercise result states

```text
passed
passed_with_findings
failed
blocked
partial
unknown
```

## 153. Exercise failure

A failed critical exercise:

- creates blocker or exception;
- prevents unsupported readiness claim;
- requires remediation;
- requires retest;
- updates risk.

## 154. Recovery metrics

Potential:

```text
backup_success_rate
verified_backup_age
restore_success_rate
restore_duration
measured_RPO
measured_RTO
reconciliation_duration
unknown_effect_count
exercise_pass_rate
continuity_exception_age
```

## 155. Recovery SLI direction

Candidate SLIs:

- percentage of verified backups;
- age of last verified backup;
- percentage of successful restore drills;
- time to restore C0/C1;
- time to reconcile nonterminal runs;
- number of unresolved recovery gaps.

## 156. Recovery reporting

A readiness report includes:

- current continuity tier;
- objectives;
- last measured results;
- backup status;
- restore status;
- SPOFs;
- exercises;
- exceptions;
- remediation;
- readiness recommendation.

## 157. Continuity dashboard

Panels:

- last verified backup;
- backup age;
- destination health;
- restore drill age/result;
- RPO/RTO measured;
- SPOFs;
- continuity incidents;
- exercise findings;
- recovery capacity;
- expiring exceptions.

## 158. Continuity alerts

Examples:

```text
backup_overdue
backup_verification_failed
restore_drill_overdue
restore_failed
backup_destination_unavailable
encryption_key_unavailable
RPO_at_risk
RTO_at_risk
single_failure_domain_detected
continuity_exception_expired
```

## 159. Continuity evidence retention

Evidence includes:

- backup manifests;
- restore reports;
- exercise reports;
- crisis decisions;
- communications;
- configuration snapshots;
- recovery logs;
- measured objectives.

Retention is governed by classification and policy.

## 160. Security of backups

Controls:

- encryption;
- least privilege;
- isolated credentials;
- immutability/offline copy where required;
- malware scanning where appropriate;
- access audit;
- secure disposal;
- key separation.

## 161. Backup access

Roles:

```text
backup_operator
restore_operator
backup_auditor
key_custodian
```

Runtime application should not automatically have delete authority over protected backup copies.

## 162. Backup deletion

Requires:

- retention expiry;
- no hold;
- authorization;
- exact target;
- audit;
- secure deletion according to medium.

## 163. Backup compromise

Actions:

- isolate destination;
- revoke credentials;
- assess data exposure;
- preserve evidence;
- create clean backup chain;
- rotate keys;
- notify Security;
- reassess restore points.

## 164. Malware in backup

Do not restore directly into trusted environment.

Use:

- isolated analysis;
- known-good point selection;
- clean rebuild;
- targeted extraction;
- security approval.

## 165. Key loss

Consequences may include unrecoverable encrypted backups.

Plan requires:

- key backup/escrow;
- multiple authorized custodians;
- recovery test;
- rotation;
- incident process.

## 166. Data-loss assessment

After incident:

- identify last verified backup;
- identify transaction/event window;
- identify lost or uncertain records;
- identify external effects;
- identify affected workspaces/users;
- classify recoverability;
- communicate.

## 167. Data-loss states

```text
none_confirmed
bounded_confirmed
possible
unknown
irrecoverable
```

## 168. Data reconstruction

Potential sources:

- audit/events;
- external provider records;
- accepted artifacts;
- Git history;
- message/calendar provider IDs;
- operator records;
- user confirmation.

Reconstructed data is source-labelled and reviewed.

## 169. User-assisted recovery

May be used for:

- resubmitting lost noncritical input;
- confirming external outcome;
- recreating a task.

Users must not be asked to provide secrets or fabricate evidence.

## 170. Workspace-specific recovery

Recovery may differ by workspace due to:

- adapter/provider;
- classification;
- backup coverage;
- active runs;
- external effects;
- contractual requirements.

Global restoration must preserve per-workspace isolation.

## 171. Pilot continuity

Pilot continuity requires:

- documented limitations;
- named operators;
- backup and restore evidence;
- emergency stop;
- support communication;
- clear stop criteria;
- alternate manual process where possible.

## 172. Pilot manual workaround

Potential workaround:

- suspend new runs;
- retain read-only access;
- manually track urgent tasks outside Agent OS only if approved;
- later reconcile external records.

Manual work must not bypass data or security policy.

## 173. Commercial continuity

A controlled commercial profile may require:

- stronger RPO/RTO;
- off-site backup;
- immutable copies;
- tested alternate host;
- formal support;
- customer communication;
- DR exercises;
- contract alignment;
- end-of-life and update policy.

## 174. Multi-tenant continuity future

Future requirements:

- tenant-specific restore;
- per-tenant export;
- shared-store recovery;
- region failover;
- key isolation;
- customer notification;
- stronger audit;
- capacity reservation.

## 175. Third-party continuity

For each dependency:

- provider continuity information;
- outage history;
- alternative;
- data portability;
- export;
- credential recovery;
- contractual support;
- failure mode.

## 176. Provider concentration risk

If one provider is critical:

- document dependency;
- define local/offline mode;
- evaluate approved alternative;
- preserve provider-neutral contracts;
- test fallback where safe.

## 177. Vendor exit continuity

Plan should support:

- export of data;
- export of artifacts;
- configuration/profile migration;
- secret rotation;
- provider replacement;
- preservation of provenance and receipts.

## 178. Change impact on continuity

Every change affecting:

- schema;
- storage;
- encryption;
- event/job model;
- artifact lifecycle;
- approvals;
- backup;
- deployment;
- identity;

must assess continuity impact.

## 179. Continuity gate for migrations

Before risky migration:

- verified backup;
- restore rehearsal if needed;
- objective impact;
- maintenance;
- rollback/forward-fix;
- evidence.

## 180. Continuity gate for new adapters

New adapter must define:

- outage behavior;
- session recovery;
- external-effect reconciliation;
- credentials;
- export/exit;
- provider dependency;
- runbook.

## 181. Continuity gate for plugins

Future plugin architecture must define:

- disable/revoke;
- data ownership;
- backup scope;
- compatibility;
- restore;
- failure isolation;
- uninstall/exit.

## 182. Continuity gate for model providers

Define:

- outage;
- rate limit;
- model retirement;
- endpoint change;
- data portability;
- fallback;
- usage/cost continuity.

## 183. Continuity exception

Fields:

- unmet objective/control;
- scope;
- impact;
- risk;
- owner;
- compensating control;
- expiry;
- monitoring;
- remediation;
- approvers.

## 184. Non-acceptable exceptions

Normally not acceptable for pilot/commercial:

- no verified backup;
- no restore capability;
- consumed approvals not preserved;
- workspace isolation unverified;
- backup key unrecoverable;
- emergency stop unavailable;
- no incident ownership.

## 185. Continuity debt

Examples:

- one-host SPOF;
- backup on same disk;
- manual restore;
- no off-site copy;
- untested secret recovery;
- one operator;
- stale runbook;
- unmeasured RTO.

## 186. Continuity-debt register

Records:

- debt ID;
- service;
- risk;
- current control;
- target;
- owner;
- deadline;
- stage impact.

## 187. Quality-gate integration

`QAG-001` should require before pilot:

- BIA;
- service tiers;
- provisional objectives;
- verified backups;
- isolated restore;
- reconciliation;
- emergency-stop exercise;
- continuity roles;
- communications;
- open exceptions reviewed.

## 188. Test-strategy integration

`TST-001` should include:

- component restore;
- full restore;
- host restart;
- event replay safety;
- approval preservation;
- artifact tombstones;
- compromised backup scenario;
- key recovery;
- communication exercise.

## 189. Observability integration

`OBS-001` should expose:

- backup age;
- restore status;
- continuity state;
- objective risk;
- destination capacity;
- exercise age;
- SPOFs;
- recovery gaps.

## 190. Operations integration

`OPS-001` provides:

- startup;
- shutdown;
- restore execution;
- emergency stop;
- incident command;
- deployment/migration procedures;
- support and escalation.

## 191. Deployment integration

`DEP-001` provides:

- environment profiles;
- host/storage layout;
- promotion;
- configuration;
- backup destinations;
- replacement environment strategy.

Its official register status remains to be confirmed.

## 192. API direction

Potential internal resources:

```text
/business-impact-assessments
/critical-services
/recovery-objective-profiles
/backup-policies
/backup-operations
/restore-plans
/recovery-operations
/continuity-incidents
/continuity-exercises
/continuity-exceptions
```

## 193. Event direction

Potential events:

```text
ContinuityPlanActivated
DisasterDeclared
CriticalServiceUnavailable
RecoveryObjectiveAtRisk
BackupVerificationFailed
RestoreStarted
RestoreCompleted
RestoreFailed
RecoveryReconciliationStarted
RecoveryReconciliationCompleted
BusinessServiceRestored
ContinuityExerciseCompleted
ContinuityExceptionExpired
```

Detailed schemas require future `EVT-001` update.

## 194. Error-code direction

```text
BCP_BACKUP_UNVERIFIED
BCP_BACKUP_KEY_UNAVAILABLE
BCP_RESTORE_POINT_INVALID
BCP_RESTORE_TARGET_INVALID
BCP_SCHEMA_INCOMPATIBLE
BCP_RECONCILIATION_INCOMPLETE
BCP_RECOVERY_OBJECTIVE_AT_RISK
BCP_CONTINUITY_MODE_ACTIVE
BCP_DISASTER_DECLARED
BCP_CRITICAL_SERVICE_UNAVAILABLE
BCP_RETURN_TO_SERVICE_BLOCKED
BCP_EXERCISE_FAILED
BCP_SINGLE_POINT_OF_FAILURE
BCP_DATA_LOSS_UNKNOWN
```

## 195. BIA template

```text
Business function:
Service owner:
Users/workspaces:
Criticality tier:
Impact of outage:
Impact of data loss:
Security impact:
Maximum tolerable disruption:
Provisional RTO:
Provisional RPO:
Minimum service:
Manual workaround:
Dependencies:
Recovery validation:
```

## 196. Critical-service template

```text
Service:
Tier:
Owner:
Authoritative data:
Dependencies:
Degraded mode:
Backup scope:
Recovery sequence:
Validation:
Known SPOFs:
Runbook:
```

## 197. Backup-policy template

```text
Policy ID:
Environment:
Stores:
Method:
Schedule:
Consistency:
Encryption:
Destination:
Retention:
Verification:
Restore cadence:
Owner:
Alerts:
```

## 198. Restore-plan template

```text
Restore plan:
Reason:
Backup manifest:
Known-good point:
Target:
Build:
Schema:
Configuration:
Approvers:
Maintenance mode:
Restore order:
Reconciliation:
Validation:
Stop conditions:
Communication:
```

## 199. Recovery-operation template

```text
Operation ID:
Incident:
Environment:
Started:
Recovery lead:
Strategy:
Backup:
Target:
Measured RPO:
Measured RTO:
Data-loss assessment:
Reconciliation status:
Validation:
Gaps:
Return-to-service decision:
```

## 200. Continuity-exercise template

```text
Exercise:
Scenario:
Objectives:
Environment:
Participants:
Expected recovery:
Steps:
Observed result:
Measured RPO/RTO:
Findings:
Corrective actions:
Reviewer:
```

## 201. Requirement catalogue

### Governance and impact

- `BCP-REQ-GOV-001` — Continuity roles and authorities are defined.
- `BCP-REQ-GOV-002` — Critical services are inventoried and tiered.
- `BCP-REQ-GOV-003` — Business impact is reviewed.
- `BCP-REQ-GOV-004` — Recovery objectives are environment- and service-specific.
- `BCP-REQ-GOV-005` — Unsupported objectives are not claimed as achieved.
- `BCP-REQ-GOV-006` — Continuity exceptions are time-bounded.
- `BCP-REQ-GOV-007` — Continuity exercises are recorded.
- `BCP-REQ-GOV-008` — Return to service requires explicit decision.

### Backup and restore

- `BCP-REQ-BRS-001` — Authoritative stores are included in backup scope.
- `BCP-REQ-BRS-002` — Backups have manifests and integrity checks.
- `BCP-REQ-BRS-003` — Encrypted backups have recoverable key procedures.
- `BCP-REQ-BRS-004` — At least one continuity copy can be separated from the primary failure domain where required.
- `BCP-REQ-BRS-005` — Backup success is distinct from verification.
- `BCP-REQ-BRS-006` — Restore is tested in isolation.
- `BCP-REQ-BRS-007` — Restore uses an exact manifest and target.
- `BCP-REQ-BRS-008` — Failed or partial restore does not resume normal service.

### Recovery integrity

- `BCP-REQ-RCV-001` — Consumed approvals remain consumed after restore.
- `BCP-REQ-RCV-002` — Leases are invalidated or reconciled.
- `BCP-REQ-RCV-003` — Nonterminal runs do not redispatch blindly.
- `BCP-REQ-RCV-004` — Tombstones and revocations are preserved.
- `BCP-REQ-RCV-005` — Event deduplication and replay boundaries survive recovery.
- `BCP-REQ-RCV-006` — Artifact integrity is verified.
- `BCP-REQ-RCV-007` — Derived stores are rebuilt from authoritative data.
- `BCP-REQ-RCV-008` — External effects are reconciled.

### Continuity modes and crisis

- `BCP-REQ-CRM-001` — Continuity modes are explicit and visible.
- `BCP-REQ-CRM-002` — C0 controls fail closed.
- `BCP-REQ-CRM-003` — Crisis declaration and command roles are defined.
- `BCP-REQ-CRM-004` — Communication distinguishes fact and uncertainty.
- `BCP-REQ-CRM-005` — Recovery strategy selection is recorded.
- `BCP-REQ-CRM-006` — Pilot stop criteria are explicit.
- `BCP-REQ-CRM-007` — Progressive restoration is used where appropriate.
- `BCP-REQ-CRM-008` — Post-recovery monitoring is required.

### Exercises and evidence

- `BCP-REQ-EVD-001` — Backup and restore exercises produce evidence.
- `BCP-REQ-EVD-002` — Measured RPO/RTO are compared to objectives.
- `BCP-REQ-EVD-003` — Failed exercises create remediation and retest.
- `BCP-REQ-EVD-004` — Critical scenarios include combined failures.
- `BCP-REQ-EVD-005` — Exercise evidence identifies build, environment, and data scope.
- `BCP-REQ-EVD-006` — Continuity readiness is quality-gated.
- `BCP-REQ-EVD-007` — Continuity debt and SPOFs are tracked.
- `BCP-REQ-EVD-008` — Evidence is classified and retained.

## 202. Traceability

| Source | BCP-001 response |
|---|---|
| `SCP-001` | Local-first and pilot/commercial boundaries |
| `NFR-001` | Reliability, durability, recoverability |
| `DAT-001` | Authoritative stores, retention, deletion, backup |
| `SEC-001` | Backup security, compromise, secrets |
| `THR-001` | Ransomware, data loss, provider/site threats |
| `ORC-001` | Durable jobs, leases, recovery |
| `RUN-001` | Run and effect reconciliation |
| `APR-001` | Approval preservation and replay prevention |
| `ART-001` | Artifact integrity and tombstones |
| `EVT-001` | Event/inbox/outbox recovery |
| `DEP-001` | Environments, storage, replacement deployment |
| `OPS-001` | Operational execution and incident response |
| `OBS-001` | Continuity metrics, alerts, dashboards |
| `TST-001` | Restore and disaster tests |
| `QAG-001` | Continuity release gates |

## 203. ADR backlog

### `ADR-CANDIDATE-BCP-001 — Recovery objectives and continuity tiers`

Approve MTPD, RPO, RTO, WRT, tiers, and environment-specific objectives.

### `ADR-CANDIDATE-BCP-002 — Backup architecture and consistency model`

Select backup methods, consistency groups, schedules, and restore tooling.

### `ADR-CANDIDATE-BCP-003 — Backup encryption, keys, and immutable copies`

Select encryption, key recovery, custodians, offline/immutable strategy, and secure deletion.

### `ADR-CANDIDATE-BCP-004 — Recovery environment and replacement-host strategy`

Define isolated restore, clean rebuild, replacement host, and future failover profile.

### `ADR-CANDIDATE-BCP-005 — Continuity exercises and readiness evidence`

Approve exercise cadence, scenarios, evidence, measured objective acceptance, and blockers.

### `ADR-CANDIDATE-BCP-006 — Commercial continuity and disaster-recovery profile`

Define commercial RPO/RTO, off-site copies, alternate hosts/sites, support, and contractual commitments.

## 204. Open decisions

1. Approve or revise continuity tiers C0-C4.
2. Approve provisional RPO/RTO for D1 and D3.
3. Define MTPD by critical service.
4. Which database backup method?
5. Which artifact-store backup method?
6. Which cross-store consistency model?
7. Which backup destinations?
8. Which off-host/off-site requirement before pilot?
9. Which immutable/offline copy requirement?
10. Which encryption and key-recovery profile?
11. Which backup retention schedule?
12. Which restore-test cadence?
13. Which clean replacement-host procedure?
14. Which alternate hardware/site is available?
15. Which people alternates and break-glass process?
16. Which continuity communication cadence?
17. Which pilot manual workarounds?
18. Which combined-disaster scenarios?
19. Which commercial RPO/RTO?
20. Which continuity dashboard and alerts?
21. Which evidence retention?
22. Which SPOFs are acceptable for MVP?
23. Which continuity exceptions block pilot?
24. Which provider/vendor-exit controls?
25. Confirm `DEP-001` official register status.

## 205. Risks

| Risk | Consequence | Response |
|---|---|---|
| Backup never restored | False confidence | Mandatory isolated restore |
| Backup key lost | Irrecoverable data | Key continuity procedure |
| Backup on same disk only | Common failure | Separate failure domain |
| Restore replays approvals | Duplicate protected action | Consumption verification |
| Restore revives tombstones | Data-governance breach | Negative-state checks |
| Nonterminal runs redispatch | Duplicate external effects | Recovery reconciliation |
| External effects assumed rolled back | Real-world inconsistency | External reconciliation |
| One operator unavailable | Recovery blocked | Alternates/runbooks |
| Single host | Long outage | Documented SPOF/replacement plan |
| RPO/RTO promised without test | Contract failure | Measured evidence |
| Ransomware reaches backups | No clean restore | Immutable/offline copy |
| Multi-store inconsistency | Missing artifacts/events | Consistency group/manifests |
| Partial restore marked success | Hidden corruption | Explicit result states |
| Provider outage during recovery | Extended disruption | Local safe mode/alternate |
| Identity outage fails open | Security compromise | Fail closed |
| Communication overstates certainty | Loss of trust | Source/unknown labels |
| Derived store treated as source | Data corruption | Rebuild from authority |
| Backup retention deletes needed evidence | Recovery gap | Holds/policy |
| Pilot continues after unsafe recovery | User/data risk | Stop criteria |
| Continuity process too complex | Unusable plan | Tiered practical runbooks |

## 206. Assumptions

- authoritative data stores can be backed up;
- backup manifests and hashes can be generated;
- an isolated restore environment can be provisioned;
- operators can access verified builds and configuration;
- secrets can be re-provisioned or recovered securely;
- external-effect references are retained;
- continuity exercises can be scheduled;
- a small team can assign alternates;
- local-first recovery is acceptable for MVP;
- pilot/commercial readiness can be blocked by continuity gaps.

## 207. Constraints

- no approved final RPO/RTO in this draft;
- no zero-downtime or zero-data-loss claim;
- no restore without exact backup, target, authority, and evidence;
- no normal service before C0/C1 verification;
- no blind redispatch after restore;
- no loss of consumed approvals, revocations, or tombstones;
- no backup success claim without integrity verification;
- no pilot readiness without restore exercise;
- no autonomous restore or emergency-stop release by agents;
- no final backup product or DR platform selected;
- no Git commit, push, PR, merge, or release during current documentation drafting;
- Git versioning remains deferred until all drafts and global consistency audit are complete.

## 208. Acceptance criteria

BCP-001 may advance to `1.0.0` when:

1. Product accepts continuity priorities, minimum service, and pilot stop criteria.
2. Architecture accepts recovery sequencing, reconciliation, and derived-store rebuild strategy.
3. Security accepts backup protection, key continuity, compromise recovery, and return-to-service gates.
4. Data accepts backup scope, manifests, restore integrity, tombstones, and data-loss assessment.
5. Operations accepts roles, crisis activation, recovery procedures, exercises, and communication.
6. Quality accepts evidence, measured objectives, failed-exercise handling, and release gates.
7. critical services are inventoried and tiered;
8. provisional RPO/RTO are either approved or explicitly revised;
9. backup policies include verification;
10. isolated restore proves consumed approvals and tombstones;
11. nonterminal runs and external effects are reconcilable;
12. crisis and recovery communication is defined;
13. combined-disaster exercises are planned;
14. continuity debt and SPOFs are visible;
15. pilot readiness depends on continuity evidence.

## 209. Downstream impact

| Document | Required use |
|---|---|
| `PLG-001` | Plugin continuity, disablement, backup, restore, exit |
| `TST-001` | Disaster, restore, and combined-failure tests |
| `QAG-001` | Continuity release gates |
| `OBS-001` | Backup/restore and objective dashboards |
| `OPS-001` | Recovery and crisis runbooks |
| `RTM-001` | Continuity requirement-to-test/evidence mapping |
| Document register | Confirm DEP-001 and BCP dependencies |

## 210. Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.1.0`
- Approved by: Product Owner under explicit user authorization to finalize the declared scope
- Finalization note: approval records the documentation baseline only; implementation and verification remain separate evidence gates

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial business continuity and disaster recovery plan covering critical services, continuity tiers, provisional RPO/RTO, backup architecture, restore and reconciliation, disaster scenarios, crisis governance, degraded modes, exercises, evidence, pilot/commercial continuity, and return to service |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `DAT-001` — Data Architecture
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `ORC-001` — Workflow and Orchestration Architecture
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `EVT-001` — Event Catalog and Async Contract
- `DEP-001` — Deployment Architecture and Environment Strategy
- `OPS-001` — Operations and Production Runbook
- `OBS-001` — Observability Architecture
- `TST-001` — Test Strategy and Verification Plan
- `QAG-001` — Quality Assurance and Release Gates
