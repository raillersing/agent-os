---
document_id: DAT-002
title: Agent OS Data Classification, Retention and Deletion Standard
version: 0.2.0
status: draft
register_status: proposed_unregistered
owner: data-owner
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
related_documents: []
dependencies:
  - DAT-001
  - SEC-001
  - IAM-001
  - POL-001
  - ART-001
  - MEM-001
  - BCP-001
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
  - IAM-001
  - POL-001
  - SAN-001
  - SEC-002
  - AUD-001
  - CST-001
  - ADP-HER-001
  - ADP-CDX-001
  - UXA-001
  - DSN-001
  - A11Y-001
  - VVR-001
related_adrs:
  - ADR-TBD-DAT2-001
  - ADR-TBD-DAT2-002
  - ADR-TBD-DAT2-003
  - ADR-TBD-DAT2-004
  - ADR-TBD-DAT2-005
  - ADR-TBD-DAT2-006
  - ADR-TBD-DAT2-007
  - ADR-TBD-DAT2-008
---

# DAT-002 — Agent OS Data Classification, Retention and Deletion Standard

> **Status: Draft — proposed/unregistered.** This document defines the proposed data classification, handling, retention, hold, deletion, backup, export, and evidence standard for Agent OS. It covers human identity data, organization and workspace data, tasks, runs, prompts, model inputs and outputs, artifacts, memory, embeddings, logs, telemetry, audit evidence, approvals, secrets, support data, incidents, backups, caches, indexes, sandbox data, adapter/provider data, and deletion propagation. It does not provide legal advice, set final statutory retention periods, authorize silent deletion of audit evidence, or claim compliance with any privacy regime.

## 1. Purpose

Agent OS processes many kinds of information with different confidentiality, integrity, availability, retention, and deletion needs.

The standard establishes:

1. how information is classified;
2. how classification is inherited and changed;
3. where data may be stored or transmitted;
4. how long data may be retained;
5. when holds override deletion;
6. how deletion propagates;
7. how backups and derived data are handled;
8. how exports and external disclosure are governed;
9. what evidence proves lifecycle actions;
10. how unknown or conflicting lifecycle state is handled.

## 2. Objectives

The standard must:

- classify all material Agent OS data;
- preserve workspace and organization ownership;
- minimize collection and propagation;
- distinguish source data, derived data, metadata, evidence, and secrets;
- bind retention to purpose and data class;
- avoid indefinite retention by default;
- support explicit holds;
- support deletion, purge, anonymization, and cryptographic erasure directions;
- propagate lifecycle state to caches, indexes, embeddings, previews, exports, and backups;
- preserve negative facts such as deletion, quarantine, and revocation after restore;
- produce deletion and retention evidence;
- remain provider-neutral;
- support local MVP, pilot, and future controlled-commercial maturity.

## 3. Non-goals

DAT-002 does not:

- provide jurisdiction-specific legal advice;
- select final statutory retention periods;
- guarantee that every external provider supports immediate deletion;
- authorize deletion of required security, financial, contractual, or audit evidence without governance;
- permit data-classification downgrade by agents;
- equate hiding with deletion;
- equate database row deletion with complete erasure;
- treat backups as exempt from retention;
- claim privacy-law compliance;
- define final customer contract terms.

## 4. Principle — Purpose limitation

Data is collected, used, disclosed, and retained only for explicit approved purposes.

## 5. Principle — Data minimization

Agent OS stores and transmits the minimum data needed for product, security, operations, evidence, and support.

## 6. Principle — Classification follows the data

Copies, derived outputs, exports, previews, caches, and embeddings inherit or strengthen classification unless explicitly reviewed.

## 7. Principle — Workspace scope is authoritative

Operational data belongs to one workspace or an explicit platform scope.

## 8. Principle — Deletion is a lifecycle process

Deletion includes source, derived, cached, indexed, exported, backed-up, and provider-held representations.

## 9. Principle — Holds are explicit

A hold suspends deletion only for the exact scope, reason, owner, and period.

## 10. Principle — Negative facts survive restore

Deleted, expired, quarantined, revoked, and held states are reapplied after restore.

## 11. Principle — Unknown does not mean deleted

Unverified deletion or provider status is recorded as unknown and requires reconciliation.

## 12. Principle — Secrets are a separate class

Secrets use references, dedicated stores, short lifetimes, and restricted evidence.

## 13. Principle — Audit is not ordinary application data

Audit and evidence have integrity and retention requirements distinct from operational convenience.

## 14. Principle — Users can see material lifecycle state

Classification, retention, hold, export, and deletion status are visible to authorized users.

## 15. Principle — No silent policy downgrade

Agents, adapters, imports, and provider responses cannot silently reduce classification or retention requirements.

## 16. Data lifecycle bounded context

The data-lifecycle context owns:

- classification taxonomies;
- data-category definitions;
- retention schedules;
- lifecycle policies;
- hold records;
- deletion requests and jobs;
- purge evidence;
- anonymization direction;
- backup propagation;
- provider deletion state;
- export lifecycle metadata;
- lifecycle reconciliation;
- data inventory and lineage references.

It does not own business-domain entities, audit semantics, IAM authentication, policy evaluation, or storage-engine implementation.

## 17. Controlled lifecycle vocabulary

```text
collect
create
ingest
classify
store
use
transform
derive
index
embed
cache
preview
share
export
archive
hold
expire
delete
purge
anonymize
quarantine
restore
reconcile
```

## 18. Data-state vocabulary

```text
active
archived
retention_due
under_hold
deletion_requested
deletion_approved
deleting
deleted_logically
purge_pending
purged
anonymized
quarantined
restored_pending_validation
provider_deletion_pending
provider_deletion_confirmed
deletion_failed
unknown
```

## 19. Lifecycle state — Active

Available for approved operational use.

## 20. Lifecycle state — Archived

Removed from ordinary workflows but retained under policy.

## 21. Lifecycle state — Retention due

The normal retention period has ended and lifecycle action is required.

## 22. Lifecycle state — Under hold

Deletion is suspended for an explicit approved reason and scope.

## 23. Lifecycle state — Deletion requested

A deletion request exists but is not yet authorized or actionable.

## 24. Lifecycle state — Deletion approved

The request passed required policy and approval checks.

## 25. Lifecycle state — Deleting

Deletion propagation is executing.

## 26. Lifecycle state — Deleted logically

Ordinary product access is removed while purge, evidence, or backup propagation remains pending.

## 27. Lifecycle state — Purge pending

Physical or cryptographic removal from one or more stores is outstanding.

## 28. Lifecycle state — Purged

Removal is confirmed across the defined active-store scope.

## 29. Lifecycle state — Anonymized

Direct identifiers are irreversibly removed or transformed according to an approved method.

## 30. Lifecycle state — Quarantined

Use is blocked because of malware, integrity, classification, legal, or security concerns.

## 31. Lifecycle state — Restored pending validation

Data was restored but cannot return to normal use before lifecycle reconciliation.

## 32. Lifecycle state — Provider deletion pending

An external provider deletion request was sent but not yet confirmed.

## 33. Lifecycle state — Provider deletion confirmed

The provider returned an accepted deletion confirmation or equivalent evidence.

## 34. Lifecycle state — Deletion failed

One or more lifecycle actions failed and require remediation.

## 35. Lifecycle state — Unknown

The current lifecycle state cannot be established.

## 36. Classification model

The proposed confidentiality classification is:

```text
C0 — Public
C1 — Internal
C2 — Confidential
C3 — Restricted
C4 — Secret material
```

Classification labels are directions pending governance approval.

## 37. C0 — Public

Information approved for public disclosure. Public does not mean unowned or unversioned.

## 38. C1 — Internal

Routine internal product, operational, or project information not approved for public distribution.

## 39. C2 — Confidential

Information whose unauthorized disclosure could harm users, workspaces, business operations, or contractual relationships.

## 40. C3 — Restricted

Highly sensitive identity, customer, security, incident, source, model, financial, or operational information requiring narrow access and stronger controls.

## 41. C4 — Secret material

Credentials, private keys, recovery codes, bearer tokens, signing material, and equivalent secret-bearing data.

## 42. Classification dimensions

Confidentiality is only one dimension. Data may also carry:

```text
integrity: low | normal | high | critical
availability: best_effort | important | critical
privacy: none | personal | sensitive_personal | unknown
evidence: ordinary | audit_relevant | legal_or_security_hold
residency: unrestricted | approved_region | local_only | unknown
lifecycle: transient | short | standard | extended | permanent_by_policy
```

## 43. Classification metadata

A classified object or dataset should record:

- classification code;
- category;
- organization/workspace;
- owner;
- source;
- purpose;
- integrity and availability class;
- privacy flag;
- residency constraint;
- retention profile;
- hold state;
- exportability;
- deletion method;
- effective time;
- classifier and authority;
- reason;
- confidence only where legitimate;
- policy/version.

## 44. Classification authority

Classification may be assigned by:

- system defaults;
- data owner;
- security owner;
- authorized workspace role;
- approved ingestion mapping;
- approved policy;
- validated detector as a proposal.

Agents, adapters, models, or detectors may propose classification but cannot autonomously downgrade protected data.

## 45. Classification inheritance

Derived content inherits the highest applicable classification among:

- source data;
- prompt/context;
- tool input;
- memory;
- artifact;
- secret exposure;
- user override;
- policy minimum;
- destination restriction.

A lower classification requires an explicit governed review and justification.

## 46. Classification aggregation risk

Multiple low-sensitivity fields may become sensitive when aggregated. Classification considers:

- volume;
- linkability;
- cross-workspace correlation;
- identity linkage;
- time range;
- operational detail;
- security relevance;
- financial insight;
- model/provider telemetry.

Aggregation may raise classification.

## 47. Unknown classification

Unknown classification is treated conservatively. Protected export, external model disclosure, broad search, or public sharing is blocked until classification is resolved.

## 48. Data category taxonomy

Primary categories:

```text
identity_and_contact
authentication_and_session
organization_and_workspace
roles_grants_and_policy
tasks_projects_and_goals
runs_steps_attempts
prompts_and_context
model_inputs_and_outputs
tool_calls_and_external_effects
artifacts_and_previews
memory_and_embeddings
source_code_and_repositories
integration_and_provider
usage_cost_and_budget
logs_metrics_and_traces
audit_evidence_and_receipts
support_and_feedback
security_incident_and_forensics
backup_and_recovery
sandbox_and_ephemeral
configuration_and_secrets
commercial_and_contractual
```

## 49. Data category — Identity and contact data

Names, emails, locale, timezone, organization affiliation, directory identifiers, and account metadata.

## 50. Data category — Authentication and session data

Credential references, factors, session metadata, devices, authentication events, recovery state, and revocations.

## 51. Data category — Organization and workspace data

Workspace names, memberships, settings, ownership, lifecycle, and configuration.

## 52. Data category — Roles, grants, and policy data

Role assignments, grants, delegations, policy versions, decisions, restrictions, and explanations.

## 53. Data category — Tasks, projects, and goals

Intent, scope, descriptions, priorities, assignments, status, and related business context.

## 54. Data category — Runs, steps, and attempts

Execution plans, states, timestamps, agent/model/tool selections, errors, retries, and reconciliation.

## 55. Data category — Prompts and context

User instructions, system-generated context, retrieved content, selected memory, and structured prompt material.

## 56. Data category — Model inputs and outputs

Provider requests and responses, token usage, model identity, safety metadata, and output candidates.

## 57. Data category — Tool calls and external effects

Structured tool arguments, targets, results, receipts, idempotency records, and effect certainty.

## 58. Data category — Artifacts and previews

Files, documents, images, code, reports, derived previews, metadata, versions, and validation results.

## 59. Data category — Memory and embeddings

Memory records, sources, citations, verification, embeddings, indexes, and conflict state.

## 60. Data category — Source code and repositories

Repository metadata, worktrees, diffs, commits, branches, tests, configuration, and generated code.

## 61. Data category — Integration and provider data

Adapter registrations, provider identifiers, endpoint configuration, capabilities, model routes, and health.

## 62. Data category — Usage, cost, and budget data

Usage measurements, estimates, reservations, invoices, pricing versions, budgets, and cost attribution.

## 63. Data category — Logs, metrics, and traces

Operational events, performance, errors, counters, traces, and diagnostic metadata.

## 64. Data category — Audit evidence and receipts

Immutable or durable evidence of identity, decisions, approvals, policy, execution, exports, and recovery.

## 65. Data category — Support and feedback

Support cases, user reports, diagnostic bundles, screenshots, comments, and satisfaction feedback.

## 66. Data category — Security incidents and forensics

Alerts, investigation notes, indicators, timelines, evidence, containment, and impact assessments.

## 67. Data category — Backup and recovery data

Backups, snapshots, manifests, restore points, validation evidence, and continuity records.

## 68. Data category — Sandbox and ephemeral data

Temporary workspaces, runtime files, package caches, logs, outputs, and secret handles.

## 69. Data category — Configuration and secrets

Environment configuration, secret references, credentials, certificates, keys, and rotation metadata.

## 70. Data category — Commercial and contractual data

Customer agreements, service terms, billing contacts, procurement information, and approved contractual evidence.

## 71. Personal-data direction

Potential personal data includes identity, contact, device, network, support, usage, and activity metadata.

The system should:

- minimize collection;
- avoid unnecessary precise location;
- avoid invasive fingerprinting;
- avoid copying complete identity-provider profiles;
- separate personal data from secret material;
- record purpose and access;
- support correction and deletion workflows where applicable;
- avoid promising legal rights or timelines until jurisdictional review.

## 72. Sensitive-personal-data direction

Agent OS should avoid intentionally collecting sensitive personal categories unless explicitly required, approved, and supported by stronger controls.

Unknown uploaded content may nevertheless contain such data. Classification, quarantine, restricted access, export controls, and deletion must account for this possibility.

## 73. Secrets

Secret material is classified `C4`.

Examples:

- passwords;
- API tokens;
- OAuth refresh tokens;
- private keys;
- recovery codes;
- signing keys;
- client secrets;
- database credentials;
- session bearer tokens;
- one-time setup secrets.

The normal retention target is the shortest technically required lifetime.

## 74. Secret references

Ordinary domain records store secret references and lifecycle metadata, not raw secret values. Secret references remain `C2` or `C3` depending on what they reveal.

## 75. Prompts and context

Prompts may contain customer data, code, secrets, personal information, artifacts, memory, and operational instructions.

Requirements:

- classify based on included content;
- minimize context;
- redact secrets;
- record source references;
- separate system governance instructions from untrusted content;
- avoid retaining full prompts indefinitely by default;
- govern provider transmission;
- support retention and deletion of prompt copies and derived traces.

## 76. Model inputs

Model inputs include prompt text, selected memory, tool summaries, files, images, and structured metadata.

Before external disclosure, validate:

- workspace;
- classification;
- provider/model policy;
- destination/region;
- retention/training terms where known;
- redaction;
- user/contract constraints;
- budget;
- approval where required.

## 77. Model outputs

Model outputs are untrusted derived data. They inherit classification from inputs and may contain newly generated personal, confidential, incorrect, or unsafe content.

Outputs remain candidates until validated or accepted.

## 78. Provider retention status

For each provider route, record where possible:

- provider;
- account/tenant;
- product/API;
- configured retention mode;
- training/use terms;
- region;
- deletion capability;
- deletion request state;
- evidence source;
- last verification.

Unknown provider retention blocks claims of deletion or zero retention.

## 79. Artifacts

Artifacts carry:

- content classification;
- metadata classification;
- provenance;
- version;
- validation;
- quarantine state;
- retention profile;
- hold state;
- deletion state;
- export history.

Deleting an artifact version does not automatically delete its citations, audit references, derived previews, exports, or backups.

## 80. Derived previews

Previews, thumbnails, extracted text, OCR, transcodes, indexes, and summaries are derived data and must inherit lifecycle and classification.

A preview may have a shorter retention period than the original, but never a longer one without explicit purpose.

## 81. Memory records

Memory records contain source, content, scope, authority, verification, freshness, conflict, classification, and retention.

Memory should not become a permanent copy of every prompt or artifact. Only approved useful knowledge is retained, and deletion of source data triggers memory review or deletion where lineage exists.

## 82. Embeddings and vector indexes

Embeddings may preserve information about their source and are not treated as anonymous by default.

Requirements:

- workspace scope;
- source linkage;
- classification;
- index version;
- deletion propagation;
- rebuild capability;
- no cross-workspace search;
- no indefinite orphan vectors;
- clear treatment after source deletion.

If exact vector deletion cannot be proven, rebuild or cryptographic/index replacement may be required.

## 83. Logs and telemetry

Logs, metrics, and traces should avoid full prompts, full artifact content, credentials, session tokens, and unnecessary personal data.

Use:

- stable IDs;
- hashes where safe;
- classifications;
- sizes/counts;
- reason codes;
- correlation IDs;
- redacted structured fields.

Debug logging must not become a permanent retention bypass.

## 84. Audit and evidence

Audit evidence may require longer retention than ordinary operational data because it proves identity, authorization, approval, execution, export, recovery, and incident actions.

Audit evidence should reference protected objects rather than duplicate full content where possible.

Detailed evidence architecture is defined in proposed/unregistered `AUD-001`.

## 85. Support data

Support cases may contain screenshots, logs, artifact excerpts, personal data, secrets, and incident details.

Support collection should:

- use purpose-bound diagnostic bundles;
- redact secrets;
- identify classification;
- restrict access;
- set case-linked retention;
- delete temporary uploads after resolution unless held;
- record customer or workspace authorization where required.

## 86. Security incident data

Incident and forensic data may receive `C3` classification and extended retention under an explicit incident hold.

Access is limited to incident roles, Security, Operations, and approved reviewers. Evidence integrity and chain-of-custody direction apply.

## 87. Sandbox and ephemeral data

Sandbox data should be transient by default.

After attempt completion:

- terminate processes;
- revoke secrets;
- collect declared outputs;
- preserve required evidence;
- delete ephemeral work directories;
- invalidate caches and package state as required;
- record cleanup.

Cleanup failure means data remains present and must be reconciled.

## 88. Repository and source-code data

Source code and repository metadata inherit workspace classification and may include secrets, customer content, infrastructure details, licenses, or vulnerability information.

Local worktrees, clones, package caches, diffs, logs, and generated files require lifecycle rules separate from authoritative remote repositories.

## 89. Usage, cost, and budget data

Cost records may be financially and commercially sensitive. They include usage units, pricing version, estimates, reservations, actuals, currency, cost center, provider references, and budget decisions.

Detailed cost retention is refined in proposed/unregistered `CST-001`.

## 90. Data inventory

The data inventory should record:

```text
dataset_or_entity
category
system_of_record
owner
organization_or_workspace_scope
classification
privacy_flag
purpose
storage_locations
processors_or_providers
retention_profile
deletion_method
backup_scope
exportability
lineage
last_review
```

## 91. Data lineage

Lineage links:

- source object;
- prompt/context;
- run/attempt;
- tool call;
- model output;
- artifact;
- preview;
- memory;
- embedding;
- export;
- audit record;
- external provider request.

Lineage enables classification inheritance, deletion propagation, impact analysis, and evidence.

## 92. Lineage limitations

When lineage is incomplete:

- record the gap;
- use conservative classification;
- block claims of complete deletion;
- consider broader purge or rebuild;
- improve instrumentation;
- preserve reconciliation evidence.

## 93. Retention model

Retention is assigned through profiles rather than arbitrary ad hoc dates.

Proposed profiles:

```text
R0 — ephemeral
R1 — short operational
R2 — standard operational
R3 — extended business
R4 — security/audit
R5 — contractual or legal hold
R6 — permanent by explicit policy
```

Exact durations require governance and legal review.

## 94. R0 — Ephemeral

Minutes to days directionally. Sandbox files, temporary uploads, transient caches, unaccepted previews, and short-lived diagnostics.

## 95. R1 — Short operational

Days to weeks directionally. Debug logs, failed uploads, temporary exports, provider request caches, and pending drafts.

## 96. R2 — Standard operational

Months directionally. Active tasks, runs, accepted artifacts, workspace settings, ordinary support records, and usage details.

## 97. R3 — Extended business

Longer business retention direction. Contracts, financial records, release records, accepted deliverables, and customer-agreed history.

## 98. R4 — Security and audit

Extended integrity-focused retention for approvals, policy, identity changes, exports, incidents, recovery, and protected effects.

## 99. R5 — Hold

Deletion suspended until an authorized hold is released.

## 100. R6 — Permanent by explicit policy

Exceptional records retained indefinitely only with approved purpose, owner, review, and storage controls.

## 101. Candidate retention ranges

The following are discussion ranges, not approved periods:

| Profile | Candidate direction |
|---|---|
| `R0` | session end to 30 days |
| `R1` | 7 to 90 days |
| `R2` | 3 to 24 months |
| `R3` | 1 to 7 years depending on purpose |
| `R4` | 1 to 7+ years depending on security, contractual, and audit needs |
| `R5` | until explicit hold release |
| `R6` | indefinite with periodic review |

Final periods must be recorded in an approved retention schedule.

## 102. Retention schedule

A retention schedule records:

- data category;
- scope;
- purpose;
- trigger event;
- retention period;
- archival period;
- deletion method;
- backup treatment;
- external provider treatment;
- hold behavior;
- owner;
- approval;
- review date;
- legal/contractual basis where applicable.

## 103. Retention triggers

Retention may start from:

- creation;
- last activity;
- task closure;
- run completion;
- artifact supersession;
- workspace closure;
- membership termination;
- support case closure;
- contract termination;
- incident closure;
- approval decision;
- export completion;
- secret rotation;
- policy supersession.

The trigger must be explicit.

## 104. Retention precedence

When multiple retention rules apply:

1. active hold;
2. non-waivable security/audit requirement;
3. contractual or legal requirement;
4. approved business requirement;
5. standard category retention;
6. shortest default.

Conflicts require Data and Security review.

## 105. Retention review

Long-lived and permanent datasets require periodic review for:

- continued purpose;
- classification;
- access;
- owner;
- minimization;
- provider copies;
- cost;
- deletion feasibility;
- hold state;
- contractual need.

No dataset remains `R6` without ongoing ownership.

## 106. Data holds

A hold suspends deletion for an exact data scope.

Hold types may include:

```text
security_incident_hold
litigation_or_legal_hold
contractual_dispute_hold
financial_audit_hold
product_integrity_hold
recovery_investigation_hold
```

This is a technical taxonomy, not legal advice.

## 107. Hold record

A hold records:

- hold ID;
- type;
- owner;
- authority;
- reason;
- organization/workspace;
- object/query scope;
- start;
- review date;
- expiry or release condition;
- affected retention jobs;
- access restrictions;
- evidence;
- release decision.

## 108. Hold restrictions

A hold must not become a hidden reason for broad indefinite retention.

It should be:

- narrowly scoped;
- time-reviewed;
- visible to authorized owners;
- applied to derived and backup data where required;
- protected from agents and ordinary users;
- released through a governed process.

## 109. Hold conflicts

When deletion is requested for held data:

- ordinary deletion is blocked;
- the requester receives a safe explanation;
- hold details are disclosed only to authorized roles;
- the deletion request remains tracked;
- action resumes after hold release if still valid.

## 110. Deletion request types

```text
user_or_customer_request
workspace_owner_request
retention_expiry
security_response
contract_termination
workspace_deletion
artifact_version_deletion
memory_deletion
account_deactivation
provider_deletion
administrative_correction
```

## 111. Deletion authorization

Deletion authorization considers:

- requester identity;
- organization/workspace authority;
- object ownership;
- classification;
- retention schedule;
- holds;
- audit requirements;
- contractual obligations;
- external effects;
- backups;
- derived data;
- approval and reauthentication requirements;
- risk of malicious or accidental deletion.

## 112. Deletion methods

Potential methods:

```text
logical deletion
physical row/object deletion
secure overwrite direction
cryptographic erasure
key destruction
anonymization
aggregation
index rebuild
provider deletion request
media destruction
```

The selected method depends on storage technology, classification, risk, and evidence needs.

## 113. Logical deletion

Logical deletion removes data from ordinary use and marks it deleted. It is an intermediate state unless the approved lifecycle intentionally requires historical tombstones or evidence.

Logical deletion alone is not complete purge.

## 114. Physical purge

Physical purge removes active-store content and associated derived representations within the defined scope.

Purge must be idempotent, resumable, observable, and evidence-producing.

## 115. Cryptographic erasure

Where data is encrypted with a dedicated key, destroying the key may form part of a deletion method if:

- key scope is sufficiently narrow;
- copies and backups use the intended key;
- key destruction is verifiable;
- metadata and indexes are handled;
- the method is approved.

It is not assumed valid for all stores.

## 116. Anonymization

Anonymization requires an approved method intended to prevent reasonable re-identification.

Simple removal of a name or replacement with a stable identifier is usually pseudonymization, not anonymization.

Anonymized data receives a new purpose, classification, lineage, and retention review.

## 117. Pseudonymization

Pseudonymization reduces direct identification but remains protected data when re-linking is possible.

Mapping tables are `C3` or `C4` depending on use and are stored separately.

## 118. Deletion tombstones

A tombstone may preserve:

- object ID;
- workspace;
- deletion time;
- deletion authority;
- policy/version;
- purge status;
- hold status;
- evidence reference;
- no ordinary content.

Tombstones prevent restore or replication from resurrecting deleted data.

## 119. Deletion job

A deletion job records:

- deletion ID;
- requested scope;
- source objects;
- derived objects;
- stores;
- caches/indexes;
- providers;
- backups;
- holds;
- method;
- status;
- attempts;
- failures;
- evidence;
- completion criteria.

## 120. Deletion propagation graph

```text
source object
→ relational/document records
→ artifacts and versions
→ previews and thumbnails
→ extracted text
→ search indexes
→ vector embeddings
→ caches
→ logs and traces where applicable
→ exports
→ provider copies
→ backups and snapshots
→ audit references
```

Not every node is deleted identically; each has a defined treatment.

## 121. Derived data deletion

Derived data is deleted, rebuilt, anonymized, or detached according to lineage and policy.

Examples:

- remove preview;
- remove extracted text;
- delete embedding;
- rebuild index;
- redact support bundle;
- invalidate cached summary;
- delete provider-side stored request;
- preserve minimal audit reference.

## 122. Cache deletion

Caches should use bounded retention and support invalidation by workspace, object, classification, policy version, and deletion event.

A cache that cannot prove invalidation must be flushed or rebuilt for the affected scope.

## 123. Search-index deletion

Search indexes must support exact document or workspace deletion, or controlled index rebuild.

Deletion completion is not claimed until index state is confirmed.

## 124. Embedding deletion

Vector stores must support source-linked deletion. Orphaned vectors are prohibited.

Where exact deletion cannot be verified, rebuild the affected workspace/index or replace the encryption boundary according to approved architecture.

## 125. Prompt and provider deletion

Deletion of prompt/model data may require:

- local prompt store purge;
- trace/log redaction or expiry;
- cache invalidation;
- provider deletion request;
- provider confirmation;
- model-output and derived artifact handling;
- audit preservation;
- status `provider_deletion_pending` if confirmation is unavailable.

## 126. Artifact deletion

Artifact deletion distinguishes:

- one version;
- all versions;
- preview only;
- export copy;
- local working copy;
- quarantined content;
- accepted artifact;
- referenced evidence.

Deleting an accepted artifact may require approval and may leave a minimal tombstone and evidence.

## 127. Memory deletion

Deleting memory requires:

- record deletion;
- source-link review;
- embedding deletion;
- cache/index invalidation;
- conflict graph update;
- derived prompt-context exclusion;
- evidence.

Verified memory must not survive source deletion without an approved independent basis.

## 128. Identity-data deletion

Identity deletion or deactivation must preserve historical attribution where needed while removing or minimizing active profile and contact data.

Past approvals and actions remain attributable to a stable historical principal reference without exposing unnecessary profile details.

## 129. Workspace deletion

Workspace deletion is a high-risk lifecycle operation.

It requires:

- owner authority;
- reauthentication;
- impact preview;
- retention and hold review;
- export option where appropriate;
- active run cancellation/reconciliation;
- integration revocation;
- artifact/memory/index handling;
- provider deletion;
- backup treatment;
- evidence;
- delayed or staged deletion direction where approved.

## 130. Organization deletion

Organization deletion includes every workspace, identity relationship, provider configuration, budget, policy, integration, artifact, memory, and audit scope.

It requires enhanced approval, impact analysis, and potentially contractual/legal review.

## 131. Secret deletion

Secret deletion normally means:

- revoke current value;
- terminate active leases;
- remove from secret store;
- rotate dependent systems;
- purge temporary copies;
- scan source/logs/artifacts;
- preserve non-secret rotation/revocation evidence.

A deleted secret reference must not expose the prior value.

## 132. Log deletion

Logs follow their own retention schedule and may not be individually mutable if stored in append-protected systems.

Where a deletion obligation applies, options include:

- shortened retention;
- field minimization;
- redaction tokenization;
- encrypted partition/key erasure;
- protected rewrite where architecture allows;
- documented residual limitation.

The solution must not falsify security evidence.

## 133. Audit-evidence deletion

Audit deletion is exceptional and governed separately because it can undermine accountability.

The standard direction is:

- minimize content at creation;
- retain references rather than full payloads;
- use approved retention;
- support lawful/contractual deletion where required without falsifying history;
- preserve non-sensitive event facts where justified;
- require Security and Data approval.

## 134. Exports

An export creates a new managed copy.

Export metadata includes:

- source scope;
- classification;
- requester;
- recipient/destination;
- purpose;
- format;
- creation time;
- expiry;
- encryption;
- receipt;
- deletion expectation;
- policy/approval.

## 135. Temporary exports

Temporary exports should expire automatically and be unavailable after the approved period. Download links are short-lived, scoped, and revocable.

## 136. External recipients

Agent OS may lose direct deletion control after an authorized recipient downloads data.

The system should:

- show this limitation before export;
- record the recipient/destination;
- use contractual/technical controls where available;
- avoid claiming complete deletion of recipient-held copies;
- retain export evidence.

## 137. Data portability direction

Where product or contract requires portability, exports should use documented formats, include scope and metadata, protect restricted data, and avoid secret material.

This is a product direction, not a legal-right commitment.

## 138. Backup classification

Backups inherit the highest classification of their contents and may require stronger classification because of aggregation.

Backup manifests, encryption keys, and restore credentials are separately classified.

## 139. Backup retention

Backups are included in the retention schedule.

Requirements:

- approved retention windows;
- rotation;
- encryption;
- off-host/offline direction where appropriate;
- access control;
- hold support;
- deletion propagation;
- restore testing;
- evidence.

Backups are not an indefinite archive by default.

## 140. Deletion in backups

Immediate object-level deletion from immutable backups may not always be technically feasible.

Approved direction:

- prevent ordinary access;
- record tombstone/negative fact;
- ensure deleted data is not restored into active use;
- expire backups on schedule;
- reapply deletion after restore;
- use key or partition strategies where stronger deletion is required;
- document residual period.

## 141. Restore lifecycle reconciliation

After restore:

1. mark restored data pending validation;
2. load current tombstones, holds, revocations, and classifications;
3. reapply deletions and expiries;
4. invalidate restored sessions and secret leases;
5. reconcile provider deletion and export state;
6. rebuild indexes/embeddings;
7. validate audit and evidence;
8. enable ordinary access progressively.

## 142. Deletion after restore

Restored copies of deleted data are not treated as active.

The platform should automatically re-delete or quarantine them using current lifecycle state and record the reconciliation outcome.

## 143. Provider and processor inventory

For every external processor or provider, record:

- service;
- owner;
- data categories;
- classifications permitted;
- workspace/organization scope;
- regions;
- retention terms;
- training/use terms;
- deletion interface;
- deletion evidence;
- subprocessor direction where known;
- contract reference;
- last review.

## 144. Provider data minimization

Send providers only the fields and content needed for the request. Avoid sending full workspace context, hidden metadata, unrelated memory, internal IDs, or secrets.

## 145. Provider deletion requests

Provider deletion requests should include:

- provider account;
- request reference;
- data scope;
- time range;
- workspace;
- local lineage;
- request time;
- response;
- confirmation;
- unresolved limitations.

No confirmation means the state remains pending or unknown.

## 146. Provider contract change

A change in provider retention, region, training use, deletion capability, or subprocessor terms triggers:

- risk review;
- policy re-evaluation;
- data-flow update;
- customer/owner review where needed;
- possible route suspension;
- new evidence.

## 147. Local-first data storage

Local-first deployments should:

- keep workspace data on approved local storage;
- separate data from container lifecycle;
- encrypt where risk requires;
- protect WSL/host backups;
- avoid hidden cloud synchronization;
- display external provider transfers;
- support local export and deletion;
- document limitations of local device compromise.

## 148. Removable media

Use of removable media for backups or exports requires:

- explicit authorization;
- classification check;
- encryption;
- inventory;
- physical custody;
- malware controls;
- retention;
- secure disposal;
- evidence.

## 149. Test and development data

Development and test environments should use synthetic or sanitized data.

Using real restricted data requires explicit authorization, equivalent controls, minimization, and deletion after use.

Copying production data into local developer environments by convenience is prohibited.

## 150. Synthetic data

Synthetic data should avoid reproducing real identities, secrets, customer content, or unique confidential patterns.

Synthetic does not automatically mean public.

## 151. Anonymized analytics

Analytics should prefer aggregate or anonymized data when possible. Re-identification risk, small cohorts, unique events, and linkage must be considered.

Raw event retention should be shorter than aggregate metric retention where feasible.

## 152. Data-quality correction

Correction of inaccurate data should:

- preserve relevant history;
- update derived indexes and memory;
- identify source;
- avoid rewriting audit facts;
- propagate corrected state;
- record evidence.

Incorrect model output is not silently promoted to authoritative corrected data.

## 153. Deletion safety

Deletion operations require safeguards against:

- wrong workspace;
- broad wildcard scope;
- stale query;
- race conditions;
- partial deletion;
- malicious insider;
- compromised account;
- restored data;
- provider mismatch;
- irreversible deletion without preview.

High-impact deletions require dry-run or impact preview.

## 154. Deletion preview

A deletion preview should show:

- objects;
- versions;
- derived data;
- indexes/embeddings;
- providers;
- backups;
- audit treatment;
- holds;
- exports;
- active runs;
- integrations;
- estimated duration;
- irreversibility;
- unknowns.

## 155. Deletion approval

Deletion may require:

- owner or data-owner authority;
- recent reauthentication;
- independent approval;
- typed confirmation or equivalent;
- delay/cooling period;
- backup/export check;
- hold check;
- exact scope fingerprint.

Approval cannot override an active non-waivable hold.

## 156. Deletion idempotency

Deletion jobs are idempotent. Repeating a completed deletion should not recreate state or fail unsafely.

Partial jobs resume from durable progress and preserve evidence.

## 157. Deletion failure

On failure:

- mark exact failed nodes/stores;
- block false completion;
- retry safe idempotent steps;
- avoid recreating deleted content;
- escalate persistent failures;
- preserve classification and access restrictions;
- expose current state to authorized users.

## 158. Deletion completion criteria

Deletion is complete only when all required active-store, derived-data, cache, index, provider, and evidence actions meet the approved scope.

Backup expiration may remain future-dated if the approved method relies on tombstones and scheduled expiry. This residual state must be visible.

## 159. Deletion receipt

A deletion receipt may contain:

- deletion ID;
- scope;
- requester and approver;
- policy/version;
- start and completion;
- methods;
- stores processed;
- providers requested/confirmed;
- backup treatment;
- holds;
- failures or unknowns;
- evidence hashes;
- no deleted content.

## 160. Lifecycle events

Potential events:

```text
DataClassified
ClassificationChanged
RetentionAssigned
RetentionDue
HoldApplied
HoldExtended
HoldReleased
DeletionRequested
DeletionApproved
DeletionStarted
DeletionNodeCompleted
DeletionFailed
DataLogicallyDeleted
DataPurged
DataAnonymized
ProviderDeletionRequested
ProviderDeletionConfirmed
ProviderDeletionFailed
BackupExpiryScheduled
RestoredDataReconciled
```

## 161. API direction

Potential resources:

```text
/data-classifications
/data-categories
/retention-profiles
/retention-schedules
/data-holds
/deletion-requests
/deletion-jobs
/deletion-receipts
/data-inventory
/data-lineage
/provider-data-processors
/export-records
```

## 162. Command API direction

Potential commands:

```text
classify
propose-classification-change
approve-classification-change
assign-retention
apply-hold
extend-hold
release-hold
request-deletion
approve-deletion
cancel-deletion
execute-deletion
retry-deletion-node
reconcile-provider-deletion
reconcile-restored-data
generate-deletion-receipt
```

Clients cannot directly set `purged`, `anonymized`, or `provider_deletion_confirmed`.

## 163. Data model direction

Core entities:

```text
DataClassification
DataCategory
RetentionProfile
RetentionSchedule
RetentionAssignment
DataHold
DeletionRequest
DeletionJob
DeletionJobNode
DeletionReceipt
DataInventoryEntry
DataLineageEdge
ProviderProcessor
ProviderDeletionRequest
ExportRecord
LifecycleTombstone
AnonymizationMethod
```

## 164. Access control

Lifecycle operations require server-side IAM and policy enforcement.

Examples:

- ordinary users may view classification for accessible objects;
- workspace data owners may propose retention/deletion;
- Security may apply incident holds;
- Operations may execute approved jobs;
- only authorized roles may release holds;
- agents may assist analysis but cannot approve classification downgrade, hold release, or destructive deletion.

## 165. Observability

Monitor:

- unclassified data;
- unknown classification;
- retention due;
- overdue deletion;
- deletion failures;
- provider deletion pending;
- hold age;
- orphan embeddings/index records;
- backup age;
- restored-data reconciliation;
- exports;
- excessive debug retention;
- secret detections;
- workspace lifecycle progress.

## 166. Alerts

Potential alerts:

```text
restricted_data_unclassified
retention_job_failed
deletion_job_failed
provider_deletion_overdue
hold_review_overdue
orphan_embedding_detected
deleted_data_restored
export_expired_but_accessible
backup_retention_exceeded
secret_found_in_artifact_or_log
classification_downgrade_requested
workspace_deletion_stalled
```

## 167. Operational runbooks

Required runbooks:

```text
classify unknown data
apply and release hold
execute artifact deletion
execute memory and embedding deletion
delete workspace
delete or deactivate identity
process provider deletion
handle deletion failure
reconcile restored data
expire temporary exports
purge sandbox data
rotate and expire backups
respond to secret found in logs/artifacts
review long-lived retention
```

## 168. Security incidents

Data-lifecycle incidents include:

- unauthorized export;
- wrong-workspace deletion;
- deletion of held data;
- failure to delete restricted data;
- restored deleted data becoming active;
- provider retention mismatch;
- secret in logs/artifacts;
- cross-workspace index or embedding;
- classification downgrade abuse;
- backup disclosure;
- deletion evidence tampering.

## 169. Incident response

Response may require:

1. contain access and exports;
2. apply hold where evidence must be preserved;
3. revoke credentials;
4. identify source, derived, provider, and backup copies;
5. classify impact;
6. preserve safe evidence;
7. correct lifecycle state;
8. notify authorized owners;
9. verify deletion or recovery;
10. update controls, tests, and retention schedule.

## 170. Testing strategy

Testing layers:

```text
classification rules
inheritance and aggregation
retention scheduling
hold precedence
deletion authorization
deletion graph
cache/index/embedding deletion
provider deletion
backup/restore reconciliation
workspace deletion
secret handling
export expiry
cross-workspace isolation
failure and retry
accessibility
visual validation
performance and scale
```

## 171. Classification tests

Test defaults, manual assignment, detector proposals, downgrade rejection, source inheritance, aggregation risk, unknown state, provider route, artifact preview, memory, and export.

## 172. Retention tests

Test trigger dates, timezones, expiry, archival, hold suspension, hold release, policy changes, inactive workspaces, long-running runs, provider copies, and backup windows.

## 173. Deletion graph tests

For representative objects, verify deletion across source rows, artifacts, previews, extracted text, search, embeddings, caches, exports, provider records, backups, and audit references.

## 174. Workspace deletion tests

Test active runs, approvals, holds, exports, integrations, artifacts, memory, embeddings, logs, backups, providers, secret references, and restore.

Any surviving unauthorized active copy is a critical defect.

## 175. Restore tests

Restore a backup containing deleted, expired, quarantined, revoked, and held data. Verify current negative lifecycle facts are re-applied before ordinary access.

## 176. Provider tests

Test data minimization, provider route classification, deletion requests, confirmation, timeout, unknown state, provider-account mismatch, and changed retention terms.

## 177. Cross-workspace tests

Verify that classification, retention, deletion, export, index, embedding, and provider operations cannot access or affect another workspace through direct IDs, queries, caches, events, or malformed lineage.

## 178. Accessibility requirements

Lifecycle interfaces follow proposed/unregistered `A11Y-001`.

Critical journeys:

- classification review;
- retention assignment;
- hold application/release;
- deletion preview;
- destructive confirmation;
- deletion progress/failure;
- export expiry;
- provider deletion status;
- restored-data reconciliation.

Critical state cannot rely only on color.

## 179. Visual validation

Proposed/unregistered `VVR-001` should cover:

- C0–C4 labels;
- unknown/conflicted classification;
- retention due;
- active hold;
- deletion preview;
- deletion running;
- partial failure;
- provider pending;
- purge completed;
- backup residual window;
- restored pending validation;
- workspace deletion;
- mobile restrictions;
- dark theme and focus.

## 180. MVP scope

Recommended MVP scope:

- C0–C4 classification;
- workspace-scoped ownership;
- core category taxonomy;
- R0–R4 retention profiles;
- explicit active holds;
- artifact, memory, prompt, log, sandbox, and workspace lifecycle rules;
- deletion tombstones;
- cache/index/embedding propagation;
- backup reapplication of deletion;
- provider deletion state;
- export records and expiry;
- deletion receipts;
- no claim of jurisdictional compliance.

## 181. Pilot readiness

Before pilot:

- all pilot datasets are inventoried;
- classification defaults are implemented;
- real secrets are excluded from prompts/logs/artifacts;
- retention schedules exist;
- sandbox and temporary data are cleaned;
- artifact/memory/index deletion works;
- workspace deletion is tested;
- backup restore re-applies lifecycle state;
- provider routes and retention are documented;
- holds and deletion evidence are operational;
- no critical lifecycle defect remains.

## 182. Controlled-commercial direction

A controlled commercial profile may require:

- contract-specific retention;
- regional residency;
- customer-admin retention controls;
- data-subject workflows;
- processor/subprocessor governance;
- stronger cryptographic erasure;
- legal-hold workflows;
- customer deletion reports;
- external privacy/security review;
- documented regulatory mappings.

These require jurisdictional legal review.

## 183. Maturity stages

```text
D0 — ad hoc storage and manual cleanup
D1 — classified workspace data and basic retention
D2 — automated retention, holds, deletion graph, provider tracking
D3 — customer-configurable governed lifecycle and stronger evidence
D4 — mature multi-jurisdiction data-governance programme
```

## 184. Requirement catalogue — Classification and handling

- `DAT2-REQ-CLS-001` — Every material dataset or object has a category and classification.
- `DAT2-REQ-CLS-002` — Unknown classification is handled conservatively.
- `DAT2-REQ-CLS-003` — Derived data inherits or strengthens classification.
- `DAT2-REQ-CLS-004` — Agents and adapters cannot autonomously downgrade classification.
- `DAT2-REQ-CLS-005` — Workspace scope is established before lifecycle action.
- `DAT2-REQ-CLS-006` — Secret material is classified separately and stored through approved secret systems.
- `DAT2-REQ-CLS-007` — Model input/output classification follows included source data.
- `DAT2-REQ-CLS-008` — Embeddings are not assumed anonymous.
- `DAT2-REQ-CLS-009` — Logs and telemetry minimize content and personal data.
- `DAT2-REQ-CLS-010` — Exports preserve classification and lifecycle metadata.
- `DAT2-REQ-CLS-011` — Provider routes respect classification and residency constraints.
- `DAT2-REQ-CLS-012` — Classification changes are versioned and auditable.

## 185. Requirement catalogue — Retention and holds

- `DAT2-REQ-RET-001` — Every data category has an approved retention profile.
- `DAT2-REQ-RET-002` — Retention has an explicit trigger event.
- `DAT2-REQ-RET-003` — Data is not retained indefinitely by default.
- `DAT2-REQ-RET-004` — Active holds override ordinary deletion.
- `DAT2-REQ-RET-005` — Holds have exact scope, authority, owner, review date, and release condition.
- `DAT2-REQ-RET-006` — Expired or obsolete holds are reviewed and released.
- `DAT2-REQ-RET-007` — Long-lived datasets receive periodic purpose review.
- `DAT2-REQ-RET-008` — Backups are included in retention schedules.
- `DAT2-REQ-RET-009` — Temporary exports and sandbox data have bounded lifetimes.
- `DAT2-REQ-RET-010` — Provider retention is inventoried and periodically verified.
- `DAT2-REQ-RET-011` — Unknown provider retention blocks zero-retention claims.
- `DAT2-REQ-RET-012` — Retention conflicts receive Data and Security review.

## 186. Requirement catalogue — Deletion and propagation

- `DAT2-REQ-DEL-001` — Deletion is authorized and bound to exact scope.
- `DAT2-REQ-DEL-002` — High-impact deletion receives reauthentication and approval where required.
- `DAT2-REQ-DEL-003` — Deletion jobs are idempotent and resumable.
- `DAT2-REQ-DEL-004` — Deletion propagates to derived data, caches, indexes, embeddings, previews, and providers.
- `DAT2-REQ-DEL-005` — Deletion completion is not claimed while required nodes remain failed or unknown.
- `DAT2-REQ-DEL-006` — Tombstones prevent restored or replicated data from becoming active.
- `DAT2-REQ-DEL-007` — Backups reapply current deletion state after restore.
- `DAT2-REQ-DEL-008` — Provider deletion remains pending until confirmed or explicitly unknown.
- `DAT2-REQ-DEL-009` — Artifact deletion treats versions, previews, exports, and evidence separately.
- `DAT2-REQ-DEL-010` — Memory deletion includes embeddings and retrieval indexes.
- `DAT2-REQ-DEL-011` — Secret deletion includes revocation, lease termination, and dependent rotation.
- `DAT2-REQ-DEL-012` — Deletion receipts contain no deleted content.

## 187. Requirement catalogue — Governance, evidence, and quality

- `DAT2-REQ-GOV-001` — Data lifecycle actions produce evidence.
- `DAT2-REQ-GOV-002` — Audit and evidence retention are distinct from ordinary application retention.
- `DAT2-REQ-GOV-003` — Lifecycle evidence excludes raw secrets.
- `DAT2-REQ-GOV-004` — Lifecycle state is visible to authorized users.
- `DAT2-REQ-GOV-005` — Lifecycle failures and overdue actions are observable.
- `DAT2-REQ-GOV-006` — Cross-workspace lifecycle operations receive negative tests.
- `DAT2-REQ-GOV-007` — Restore tests verify deletion, expiry, quarantine, revocation, and hold state.
- `DAT2-REQ-GOV-008` — Agents cannot approve destructive deletion or hold release.
- `DAT2-REQ-GOV-009` — Exceptions are time-bounded and approved.
- `DAT2-REQ-GOV-010` — Jurisdiction-specific claims require legal review.
- `DAT2-REQ-GOV-011` — Pilot and release are blocked by critical unresolved lifecycle failures.
- `DAT2-REQ-GOV-012` — Global document audit reconciles categories, identifiers, owners, and dependencies.

## 188. Traceability

| Source | DAT-002 response |
|---|---|
| `DAT-001` | Systems of record, workspace scope, storage, backup, and lineage |
| `DCT-001` | Entity and field definitions |
| `SEC-001` | Confidentiality, integrity, secrets, data flows, and exports |
| `THR-001` | Exfiltration, over-retention, restore, provider, and cross-workspace threats |
| `IAM-001` | Identity lifecycle, memberships, sessions, and historical attribution |
| `POL-001` | Classification, retention, export, deletion, and hold decisions |
| `SAN-001` | Ephemeral data, secret leases, outputs, cleanup, and quarantine |
| `MEM-001` | Memory source, authority, embeddings, indexes, and deletion |
| `ART-001` | Artifact versions, previews, quarantine, export, and deletion |
| `RUN-001` | Run/attempt lifecycle, prompts, tool effects, and recovery |
| `AUD-001` | Proposed evidence integrity, retention, export, and deletion treatment |
| `CST-001` | Proposed usage, cost, budget, and financial-data lifecycle |
| `OPS-001` | Lifecycle jobs, incidents, restore, and runbooks |
| `BCP-001` | Backup, restore, recovery, and negative-fact reapplication |
| `PLG-001` | Extension/provider data declarations and lifecycle |

## 189. ADR-TBD-DAT2-001 — Classification taxonomy and inheritance

Approve C0–C4, privacy/integrity/availability dimensions, aggregation, unknown handling, and downgrade authority.

## 190. ADR-TBD-DAT2-002 — Data inventory, lineage, and category ownership

Define inventory technology, lineage coverage, owners, provider mapping, and orphan detection.

## 191. ADR-TBD-DAT2-003 — Retention profiles and schedules

Approve R0–R6, trigger events, candidate periods, review cadence, and contractual/legal override process.

## 192. ADR-TBD-DAT2-004 — Deletion architecture and evidence

Define tombstones, deletion graph, idempotent jobs, receipts, completion criteria, failures, and cryptographic erasure.

## 193. ADR-TBD-DAT2-005 — Holds and high-risk lifecycle governance

Define hold authorities, review, release, deletion conflicts, workspace deletion, and organization deletion.

## 194. ADR-TBD-DAT2-006 — Backup, restore, and deletion propagation

Define immutable backup treatment, tombstones, key scope, expiration, restore reconciliation, and residual windows.

## 195. ADR-TBD-DAT2-007 — External provider data lifecycle

Define provider inventory, allowed classifications, retention/training terms, regions, deletion requests, confirmations, and route suspension.

## 196. ADR-TBD-DAT2-008 — Personal-data, analytics, and commercial governance

Define personal-data minimization, analytics aggregation, data-subject workflows, residency, customer controls, and legal review.

## 196A. ADR-003 retention baseline

The proposed default profiles are:

| Data category | Default profile |
|---|---|
| Conversations | Retain until user/workspace deletion; archive inactive content |
| Artifacts | Retain until explicit deletion; preserve version lineage |
| Memory | Retain until correction, expiry, or deletion; preserve provenance |
| Run metadata | Long-lived; archive high-volume logs separately |
| Consequential audit evidence | Seven years by default where no stricter policy applies |
| Secrets | Never in ordinary content; revoke immediately when compromised |
| Derived indexes and previews | Follow source deletion and rebuild policy |
| Backups | Encrypted, rotated, and bounded by the deployment recovery policy |

Deletion uses a 30-day recoverable period for ordinary content. Audit references may remain without the deleted content. These are product defaults and do not constitute legal retention advice.

## 197. Open decisions

1. Confirm `DAT-002` registration.
2. Approve C0–C4 classification labels and handling rules.
3. Approve privacy, integrity, availability, residency, and evidence dimensions.
4. Approve data categories and owners.
5. Approve R0–R6 retention profiles.
6. Set initial retention periods for MVP and pilot.
7. Define legal/contractual review authority.
8. Define hold types, authorities, review cadence, and release process.
9. Define deletion approval thresholds.
10. Define workspace and organization deletion workflows.
11. Select deletion-job and lineage architecture.
12. Define embedding and index deletion strategy.
13. Define audit-record minimization and deletion treatment.
14. Define backup deletion residual windows.
15. Define cryptographic-erasure applicability.
16. Define provider retention and deletion verification.
17. Define external processor inventory and review cadence.
18. Define personal-data and support-data handling.
19. Define analytics aggregation and anonymization method.
20. Define export expiry and recipient responsibilities.
21. Define customer-facing lifecycle reporting.
22. Confirm lifecycle monitoring, alerts, and release gates.
23. Confirm accessibility and visual scenarios.
24. Align `AUD-001`, `CST-001`, `ADP-HER-001`, and `ADP-CDX-001`.
25. Reconcile all durations and legal assumptions during global audit.

## 198. Risks

| Risk | Consequence | Response |
|---|---|---|
| Classification absent | Unsafe storage/export | Mandatory defaults |
| Agent downgrades data | Unauthorized disclosure | Human/policy authority |
| Logs retain full prompts | Privacy/security exposure | Structured minimization |
| Embeddings survive source deletion | Hidden retained data | Lineage and rebuild |
| Database row deleted only | Residual copies remain | Deletion graph |
| Backup restores deleted data | Data resurrection | Tombstones/reconciliation |
| Provider deletion unconfirmed | False deletion claim | Pending/unknown state |
| Hold becomes indefinite | Over-retention | Review and expiry |
| Audit deleted as ordinary data | Accountability loss | Separate treatment |
| Secret appears in evidence | Credential compromise | Scanning/redaction |
| Workspace deletion too broad | Irreversible loss | Preview and approval |
| Workspace deletion too weak | Residual data | Complete graph tests |
| Export recipient retains copy | Incomplete control | Disclosure and receipt |
| Anonymization reversible | Privacy breach | Approved method/review |
| Test data contains real customer data | Unauthorized spread | Synthetic/sanitized data |
| Retention periods guessed as legal | Compliance risk | Legal review |
| Provider terms change | Unexpected processing | Periodic verification |
| Lifecycle status green despite unknown nodes | False assurance | Explicit unknown |
| Local backup outside inventory | Residual exposure | Host backup inventory |
| Global audit misses duration conflicts | Inconsistent implementation | Cross-document audit |

## 199. Assumptions

- Workspace is the primary operational data boundary.
- Data stores can carry lifecycle and classification metadata.
- Artifacts, memory, prompts, indexes, and provider requests have lineage references.
- Deletion jobs can be durable, idempotent, and observable.
- Backups can reapply tombstones and negative facts after restore.
- External providers expose at least documented retention and deletion behavior, though confirmation may remain unavailable.
- Legal review will set jurisdiction-specific requirements before commercial claims.
- The local MVP can use simpler retention while preserving the same lifecycle contracts.

## 200. Constraints

- no silent classification downgrade;
- no indefinite retention by default;
- no raw secrets in prompts, logs, artifacts, evidence, or deletion receipts;
- no claim of deletion while required nodes are failed or unknown;
- no restored deleted data returned to ordinary access;
- no cross-workspace lifecycle action;
- no destructive workspace/organization deletion without governed review;
- no provider zero-retention or deletion claim without current evidence;
- no legal-compliance claim in this draft;
- no agent approval of hold release, classification downgrade, or destructive deletion;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## 201. Acceptance criteria

DAT-002 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts lifecycle, export, workspace deletion, and user-facing status behavior;
3. Architecture accepts classification metadata, lineage, deletion graph, provider, cache/index, and backup boundaries;
4. Security accepts secret, restricted-data, export, hold, deletion, restore, and incident controls;
5. Data accepts categories, owners, retention profiles, schedules, anonymization, and evidence;
6. Operations accepts lifecycle jobs, monitoring, failures, backups, restore, and runbooks;
7. Quality accepts tests, cross-workspace coverage, evidence, exceptions, and gates;
8. classification and retention taxonomies are approved;
9. initial MVP/pilot schedules are approved;
10. hold and deletion governance are approved;
11. backup and provider deletion treatment are approved;
12. lifecycle evidence and receipts are approved;
13. legal assumptions are explicitly reviewed or deferred;
14. accessibility and visual scenarios are accepted;
15. downstream audit, cost, and adapter documents can refine details without changing lifecycle invariants.

## 202. Downstream impact

| Document | Required use |
|---|---|
| `AUD-001` | Audit classifications, evidence retention, legal/security holds, exports, and deletion |
| `CST-001` | Usage, pricing, budget, financial-data retention, and aggregation |
| `ADP-HER-001` | Hermes prompts, memory, provider data, session data, and deletion |
| `ADP-CDX-001` | Codex repositories, worktrees, logs, diffs, artifacts, and provider data |
| `SEC-002` | Update control evidence and retention/deletion controls |
| `UXA-001` | Classification, retention, hold, export, and deletion journeys |
| `DSN-001` | Classification badges, hold states, deletion progress, and warnings |
| `A11Y-001` | Accessible lifecycle review and destructive actions |
| `VVR-001` | Lifecycle visual scenarios and regression baselines |
| Document register | Add proposed document and dependencies |

## 203. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial classification, retention, hold, deletion, backup, export, provider, lifecycle evidence, and restore-reconciliation standard covering Agent OS operational, AI, artifact, memory, identity, security, and support data |

## 204. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `DAT-001` — Data Architecture
- `DCT-001` — Data Dictionary
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `IAM-001` — Identity and Access Management Architecture — proposed/unregistered
- `POL-001` — Policy and Permission Architecture — proposed/unregistered
- `SAN-001` — Sandbox and Secure Execution Architecture — proposed/unregistered
- `MEM-001` — Memory and Knowledge Architecture
- `ART-001` — Artifact Contract
- `RUN-001` — Run and Execution Contract
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
- `SEC-002` — Security Control Catalogue — proposed/unregistered
