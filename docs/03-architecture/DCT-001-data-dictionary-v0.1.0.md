---
document_id: DCT-001
title: Agent OS Data Dictionary
version: 0.2.0
status: approved
owner: data-owner
approvers:
  - product-owner
  - architecture-owner
  - data-owner
  - security-owner
  - quality-owner
created: 2026-07-19
last_reviewed: 2026-08-13
approval_date: 2026-08-13
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
  - role: architecture-owner
    status: approved
    approval_date: 2026-08-13
  - role: data-owner
    status: approved
    approval_date: 2026-08-13
  - role: security-owner
    status: approved
    approval_date: 2026-08-13
  - role: quality-owner
    status: approved
    approval_date: 2026-08-13
pending_approvals: []
classification: internal
source_of_truth: false
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
related_adrs:
  - ADR-CANDIDATE-DCT-001
  - ADR-CANDIDATE-DCT-002
  - ADR-CANDIDATE-DCT-003
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# DCT-001 — Agent OS Data Dictionary

> **Status: Approved baseline — 2026-08-13.** This document defines the canonical business and technical vocabulary for the first Agent OS MVP. It does not prescribe final physical database column types, select a database engine, approve exact retention periods, or replace detailed API/event contracts.

## 1. Purpose

This document standardizes how Agent OS names, defines, validates, classifies, stores, exchanges, and interprets data.

It provides canonical entity names, field names, semantic types, formats, nullability rules, ownership, source-of-truth classes, classifications, lifecycle states, validation rules, examples, controlled vocabularies, and compatibility rules.

Its purpose is to reduce naming drift, duplicated concepts, ambiguous states, provider-specific leakage, inconsistent API/event fields, unsafe free-text status values, and migration ambiguity.

## 2. Scope

Included: identifiers, scope, identity, authorization, registry, capabilities, tasks, snapshots, runs, steps, attempts, jobs, leases, checkpoints, policy, approvals, memory, artifacts, audit, receipts, usage, cost, budgets, operations, health, backups, restores, migrations, request/response envelopes, event envelopes, and controlled vocabularies.

Excluded: final SQL DDL, physical indexes, ORM mappings, provider payloads, complete OpenAPI/AsyncAPI contracts, exact retention periods, cryptographic algorithms, and localized UI copy.

## 3. Naming principles

| ID | Principle | Rule |
| --- | --- | --- |
| DNP-001 | Canonical English identifiers | Machine-facing names use English. |
| DNP-002 | Snake case | Canonical fields use `snake_case`. |
| DNP-003 | Singular entity names | Use `workspace`, `run`, `artifact`. |
| DNP-004 | Identifier suffix | Identifiers end in `_id`. |
| DNP-005 | Timestamp suffix | Point-in-time fields end in `_at`. |
| DNP-006 | Explicit quantities | Examples: `timeout_seconds`, `size_bytes`. |
| DNP-007 | Positive booleans | Use `is_active`, not a double negative. |
| DNP-008 | State versus status | `state` is lifecycle; `status` is operational condition. |
| DNP-009 | Source versus authority | These are modeled separately. |
| DNP-010 | Unknown is explicit | Unknown is never silently defaulted. |

## 4. Semantic type catalogue

| Semantic type | Meaning |
| --- | --- |
| opaque_id | Stable, non-meaningful identifier |
| display_name | Human-readable mutable label |
| slug | URL-safe label; never an authority key |
| short_text | Bounded short text |
| long_text | Bounded longer text |
| markdown_text | Sanitized Markdown |
| uri_reference | URI or internal typed reference |
| timestamp_utc | UTC timestamp |
| date_only | Calendar date |
| duration_seconds | Non-negative integer duration |
| money_amount | Decimal amount |
| currency_code | Three-letter currency code |
| content_hash | Integrity digest |
| version_string | Semantic or contract version |
| enum_code | Controlled vocabulary value |
| json_object | Versioned structured object |
| json_array | Versioned structured array |
| byte_count | Non-negative byte count |
| count | Non-negative integer |
| classification_code | Controlled data classification |
| correlation_id | Cross-operation correlation ID |
| idempotency_key | Duplicate-protection key |
| action_fingerprint | Digest of normalized action |
| source_reference | Typed provenance/content reference |
| evidence_reference | Typed evidence reference |

## 5. Common field rules

- Identifiers are opaque, stable, non-reusable, and independent of mutable names.
- Timestamps use UTC. Source occurrence time and platform recording time remain distinct.
- Published versions are immutable.
- Text is bounded, validated, safely rendered, and classified.
- JSON is schema-versioned and cannot bypass canonical fields.
- Defaults never grant authority, lower classification, mark unknown data as healthy, or convert unknown cost to zero.

## 6. Common identifiers

| Field | Definition | Type | Required | Owner |
| --- | --- | --- | --- | --- |
| organization_id | Organization identifier | opaque_id | Contextual | BC-ORG |
| workspace_id | Workspace isolation identifier | opaque_id | Protected records | BC-ORG |
| project_id | Project identifier | opaque_id | Conditional | BC-ORG |
| identity_id | Actor/workload identity | opaque_id | Actor-bound records | BC-IAM |
| task_id | Task identifier | opaque_id | Task/run records | BC-WRK |
| task_snapshot_id | Immutable snapshot identifier | opaque_id | Runs | BC-WRK |
| run_id | Durable execution identifier | opaque_id | Run-related | BC-RUN |
| step_id | Run-step identifier | opaque_id | Step-related | BC-RUN |
| attempt_id | Step-attempt identifier | opaque_id | Attempt-related | BC-RUN |
| approval_request_id | Approval request identifier | opaque_id | Approval-related | BC-APR |
| artifact_id | Artifact identifier | opaque_id | Artifact-related | BC-ART |
| memory_record_id | Memory identifier | opaque_id | Memory-related | BC-MEM |
| audit_event_id | Audit event identifier | opaque_id | Audit events | BC-AUD |
| usage_event_id | Usage event identifier | opaque_id | Usage events | BC-CST |
| backup_operation_id | Backup identifier | opaque_id | Backup records | BC-OPS |

## 7. Common scope fields

| Field | Definition | Type | Required | Rules |
| --- | --- | --- | --- | --- |
| organization_id | Owning organization | opaque_id | Yes for protected scope | Immutable |
| workspace_id | Owning workspace | opaque_id | Yes for workspace data | Immutable |
| project_id | Project context | opaque_id | Optional | Must belong to workspace |
| scope_type | Scope category | enum_code | Conditional | Controlled vocabulary |
| scope_id | Scoped object ID | opaque_id | Conditional | Must match type |
| resource_scope | Resource boundary | json_object | Conditional | Versioned |
| network_scope | Network boundary | json_object | Conditional | Versioned |
| data_classification | Highest data class | classification_code | Yes for protected content | Cannot silently lower |

## 8. Common provenance fields

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| source_type | Source category | enum_code | Yes |
| source_system | Producing system | short_text | Conditional |
| source_record_id | Source-system record ID | short_text | Conditional |
| source_version | Source version | version_string | Conditional |
| source_timestamp | Time at source | timestamp_utc | Conditional |
| source_class | Authority/source class | enum_code | Yes |
| producer_identity_id | Producing identity | opaque_id | Conditional |
| captured_at | Captured by Agent OS | timestamp_utc | Yes |
| evidence_reference | Supporting evidence | evidence_reference | Conditional |
| integrity_hash | Content integrity digest | content_hash | Conditional |

## 9. Common lifecycle fields

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| state | Lifecycle state | enum_code | Yes |
| status | Operational condition | enum_code | Conditional |
| state_reason | Safe reason code and message | json_object | Conditional |
| created_at | Creation time | timestamp_utc | Yes |
| created_by | Creating identity | opaque_id | Where attributable |
| updated_at | Last material update | timestamp_utc | Conditional |
| updated_by | Updating identity | opaque_id | Conditional |
| version | Aggregate version | count | Yes |
| archived_at | Archive time | timestamp_utc | Conditional |
| deleted_at | Active deletion time | timestamp_utc | Conditional |
| expires_at | Expiry time | timestamp_utc | Conditional |

## 10. Organization

| Field | Definition | Type | Required | Classification |
| --- | --- | --- | --- | --- |
| organization_id | Stable organization ID | opaque_id | Yes | Internal |
| name | Display name | display_name | Yes | Internal |
| purpose | Organization purpose | long_text | Optional | Internal |
| state | Lifecycle state | organization_state | Yes | Internal |
| policy_profile_reference | Default policy profile | source_reference | Optional | Internal |
| created_at | Creation time | timestamp_utc | Yes | Internal |
| created_by | Creator | opaque_id | Yes | Internal |
| version | Aggregate version | count | Yes | Internal |

Controlled values:

```text
active
suspended
archived
```

## 11. Workspace

| Field | Definition | Type | Required | Classification |
| --- | --- | --- | --- | --- |
| workspace_id | Stable workspace ID | opaque_id | Yes | Internal |
| organization_id | Parent organization | opaque_id | Yes | Internal |
| name | Display name | display_name | Yes | Internal |
| purpose | Workspace purpose | long_text | Yes | Internal |
| classification | Default handling class | classification_code | Yes | Confidential metadata |
| state | Workspace lifecycle | workspace_state | Yes | Internal |
| policy_profile_reference | Workspace policy profile | source_reference | Optional | Internal |
| created_at | Creation time | timestamp_utc | Yes | Internal |
| created_by | Creator | opaque_id | Yes | Internal |
| version | Aggregate version | count | Yes | Internal |

Controlled values:

```text
active
read_only
suspended
archived
```

## 12. Project

| Field | Definition | Type | Required | Classification |
| --- | --- | --- | --- | --- |
| project_id | Stable project ID | opaque_id | Yes | Internal |
| workspace_id | Parent workspace | opaque_id | Yes | Internal |
| name | Display name | display_name | Yes | Internal |
| purpose | Project purpose | long_text | Optional | Internal |
| state | Lifecycle | project_state | Yes | Internal |
| created_at | Creation time | timestamp_utc | Yes | Internal |
| created_by | Creator | opaque_id | Yes | Internal |
| version | Aggregate version | count | Yes | Internal |

Controlled values:

```text
active
paused
archived
```

## 13. Identity

| Field | Definition | Type | Required | Classification |
| --- | --- | --- | --- | --- |
| identity_id | Stable identity ID | opaque_id | Yes | Internal |
| identity_type | Human/workload type | identity_type | Yes | Internal |
| display_name | Human-readable label | display_name | Yes | Internal |
| external_subject | External IdP subject | short_text | Conditional | Confidential |
| state | Identity lifecycle | identity_state | Yes | Internal |
| created_at | Creation time | timestamp_utc | Yes | Internal |
| last_authenticated_at | Last successful authentication | timestamp_utc | Optional | Internal |
| version | Aggregate version | count | Yes | Internal |

Controlled values:

```text
human
agent
adapter
worker
service
integration
backup_operator_process
active
disabled
revoked
expired
unknown
```

## 14. Session

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| session_id | Session ID | opaque_id | Yes |
| identity_id | Authenticated identity | opaque_id | Yes |
| authentication_method | Login method | enum_code | Yes |
| assurance_level | Session assurance | enum_code | Yes |
| created_at | Session start | timestamp_utc | Yes |
| last_seen_at | Last activity | timestamp_utc | Yes |
| idle_expires_at | Idle expiry | timestamp_utc | Yes |
| absolute_expires_at | Absolute expiry | timestamp_utc | Yes |
| revoked_at | Revocation time | timestamp_utc | Optional |
| state | Session state | session_state | Yes |
| authority_version | Authorization snapshot version | count | Yes |

```text
active
expired
revoked
invalid
```

## 15. WorkspaceMembership

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| membership_id | Membership ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| identity_id | Member identity | opaque_id | Yes |
| state | Membership lifecycle | membership_state | Yes |
| joined_at | Membership start | timestamp_utc | Yes |
| ended_at | Membership end | timestamp_utc | Optional |
| created_by | Granting identity | opaque_id | Yes |

```text
active
suspended
removed
expired
```

## 16. RoleAssignment

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| role_assignment_id | Assignment ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Conditional |
| identity_id | Identity | opaque_id | Yes |
| role_code | Assigned role | role_code | Yes |
| scope_type | Platform/organization/workspace/project | enum_code | Yes |
| scope_id | Scope ID | opaque_id | Conditional |
| assigned_by | Assigning identity | opaque_id | Yes |
| assigned_at | Assignment time | timestamp_utc | Yes |
| expires_at | Optional expiry | timestamp_utc | Optional |
| state | Assignment state | enum_code | Yes |

```text
product_owner
workspace_owner
builder_operator
technical_operator
reviewer_approver
auditor
contributor
artifact_consumer
```

## 17. AgentRegistration

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| agent_registration_id | Registration ID | opaque_id | Yes |
| adapter_type | Hermes/Codex/custom | adapter_type | Yes |
| display_name | Display name | display_name | Yes |
| adapter_identity_id | Workload identity | opaque_id | Yes |
| implementation_version | Adapter/runtime version | version_string | Yes |
| configuration_reference | Non-secret config | source_reference | Yes |
| registration_state | Lifecycle | integration_state | Yes |
| health_state | Current health | health_state | Yes |
| last_validated_at | Last validation | timestamp_utc | Optional |
| version | Aggregate version | count | Yes |

```text
hermes
codex
custom
unknown
```

## 18. CapabilityDeclaration

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| capability_declaration_id | Declaration ID | opaque_id | Yes |
| agent_registration_id | Parent registration | opaque_id | Yes |
| capability_code | Capability identifier | short_text | Yes |
| capability_version | Contract version | version_string | Yes |
| effect_class | Effect category | effect_class | Yes |
| supported_target_classes | Target categories | json_array | Yes |
| supported_data_classes | Allowed classes | json_array | Yes |
| supports_streaming | Streaming support | boolean | Yes |
| supports_cancellation | Cancellation support | boolean | Yes |
| supports_pause | Pause support | boolean | Yes |
| supports_resume | Resume support | boolean | Yes |
| supports_checkpoint | Checkpoint support | boolean | Yes |
| supports_idempotency | Native idempotency | boolean | Yes |
| supports_usage_reporting | Usage reporting | boolean | Yes |
| state | Capability state | capability_state | Yes |

```text
declared
validated
partially_validated
unsupported
temporarily_unavailable
unknown
deprecated
disabled
```

## 19. ModelProfile

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| model_profile_id | Profile ID | opaque_id | Yes |
| logical_name | Stable logical label | display_name | Yes |
| provider_id | Configured provider | short_text | Yes |
| provider_model_id | Configured model | short_text | Yes |
| capability_intent | Intended uses | json_array | Yes |
| data_class_rules | Classification rules | json_object | Yes |
| context_limit | Maximum context units | count | Optional |
| output_limit | Maximum output units | count | Optional |
| fallback_policy | Explicit fallback | json_object | Optional |
| secret_reference | Credential reference | source_reference | Conditional |
| validation_state | Profile validation | validation_state | Yes |
| state | Profile state | enum_code | Yes |
| version | Profile version | count | Yes |

## 20. ToolRegistration

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| tool_registration_id | Tool ID | opaque_id | Yes |
| tool_type | Tool/integration type | short_text | Yes |
| name | Display name | display_name | Yes |
| implementation_version | Version | version_string | Yes |
| capabilities | Capability references | json_array | Yes |
| side_effect_classes | Effect classes | json_array | Yes |
| configuration_reference | Config reference | source_reference | Yes |
| health_state | Health | health_state | Yes |
| state | Lifecycle | integration_state | Yes |

## 21. Task

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| task_id | Task ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| project_id | Project | opaque_id | Optional |
| title | Task title | short_text | Yes |
| desired_outcome | Intended result | long_text | Yes |
| state | Task lifecycle | task_state | Yes |
| current_snapshot_id | Current immutable snapshot | opaque_id | Optional |
| created_by | Creator | opaque_id | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| version | Aggregate version | count | Yes |

```text
draft
ready
active
blocked
completed
cancelled
archived
```

## 22. TaskSnapshot

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| task_snapshot_id | Snapshot ID | opaque_id | Yes |
| task_id | Parent task | opaque_id | Yes |
| snapshot_number | Monotonic version | count | Yes |
| desired_outcome | Frozen outcome | long_text | Yes |
| resource_scopes | Approved resources | json_array | Yes |
| data_classification | Highest class | classification_code | Yes |
| agent_preference | Preferred adapter | json_object | Optional |
| model_profile_reference | Model profile | source_reference | Optional |
| tool_capability_requests | Required tools | json_array | Optional |
| time_limit_seconds | Wall-clock limit | duration_seconds | Yes |
| step_limit | Maximum steps | count | Yes |
| retry_limit | Maximum retries | count | Yes |
| cost_limit | Maximum cost | money_amount | Optional |
| expected_artifacts | Expected outputs | json_array | Optional |
| content_hash | Snapshot fingerprint | content_hash | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| created_by | Creator | opaque_id | Yes |

## 23. Run

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| run_id | Run ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| project_id | Project | opaque_id | Optional |
| task_id | Task | opaque_id | Yes |
| task_snapshot_id | Immutable snapshot | opaque_id | Yes |
| requested_by | Requester | opaque_id | Yes |
| agent_registration_id | Selected adapter/agent | opaque_id | Conditional |
| model_profile_id | Selected model profile | opaque_id | Conditional |
| state | Run lifecycle | run_state | Yes |
| state_reason | Safe reason | json_object | Optional |
| execution_bounds | Time/step/attempt/cost/resource limits | json_object | Yes |
| policy_snapshot_reference | Policy context | source_reference | Yes |
| idempotency_key | Duplicate-protection key | idempotency_key | Yes |
| created_at | Created | timestamp_utc | Yes |
| started_at | Started | timestamp_utc | Optional |
| ended_at | Ended | timestamp_utc | Optional |
| last_reliable_evidence_at | Latest trustworthy evidence | timestamp_utc | Optional |
| receipt_state | Receipt status | receipt_state | Yes |
| version | Aggregate version | count | Yes |

```text
created
queued
preflighting
blocked
starting
running
waiting_for_approval
waiting_for_resource
waiting_for_adapter
waiting_for_budget
paused
cancelling
retrying
resuming
stale
unknown
completed
failed
cancelled
```

## 24. RunStep

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| step_id | Step ID | opaque_id | Yes |
| run_id | Parent run | opaque_id | Yes |
| step_type | Step category | step_type | Yes |
| sequence_number | Ordered position | count | Conditional |
| dependency_ids | Predecessor steps | json_array | Optional |
| capability_code | Required capability | short_text | Conditional |
| normalized_target | Exact target | json_object | Conditional |
| effect_class | Effect category | effect_class | Yes |
| state | Step lifecycle | step_state | Yes |
| attempt_count | Attempts created | count | Yes |
| timeout_seconds | Step timeout | duration_seconds | Yes |
| approval_requirement | Approval rule | json_object | Optional |
| created_at | Creation time | timestamp_utc | Yes |
| started_at | Start time | timestamp_utc | Optional |
| ended_at | End time | timestamp_utc | Optional |
| version | Step version | count | Yes |

Step types:

```text
agent_execution
model_inference
tool_proposal
approval_wait
tool_execution
artifact_creation
checkpoint_creation
validation
finalization
custom
```

Step states:

```text
planned
ready
leased
starting
running
waiting_for_approval
waiting_for_resource
retry_scheduled
paused
cancelling
completed
failed
cancelled
stale
unknown
skipped
```

## 25. RunAttempt

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| attempt_id | Attempt ID | opaque_id | Yes |
| step_id | Parent step | opaque_id | Yes |
| attempt_number | Monotonic number | count | Yes |
| idempotency_key | Attempt key | idempotency_key | Yes |
| state | Attempt lifecycle | attempt_state | Yes |
| worker_identity_id | Worker/adapter identity | opaque_id | Conditional |
| lease_id | Lease reference | opaque_id | Conditional |
| approval_consumption_id | Exact approval use | opaque_id | Conditional |
| input_reference | Frozen input | source_reference | Yes |
| result_reference | Result/evidence | source_reference | Optional |
| failure_class | Failure category | failure_class | Optional |
| side_effect_certainty | Effect knowledge | side_effect_certainty | Yes |
| started_at | Start time | timestamp_utc | Optional |
| ended_at | End time | timestamp_utc | Optional |
| last_heartbeat_at | Latest heartbeat | timestamp_utc | Optional |

```text
created
leased
dispatched
acknowledged
running
succeeded
failed
timed_out
cancel_requested
cancelled
lost
unknown
```

## 26. Failure classes

```text
validation_failure
authentication_failed
authorization_denied
policy_denied
approval_missing
approval_invalid
capability_unavailable
resource_unavailable
budget_exceeded
timeout_before_effect
timeout_after_effect
timeout_unknown_effect
transient_external
permanent_external
worker_lost
integrity_failure
internal_failure
unknown_failure
```

## 27. Side-effect certainty

```text
none
known_not_started
failed_before_effect
known_completed
known_partial
compensated
compensation_failed
unknown
```

## 28. DurableJob

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| job_id | Job ID | opaque_id | Yes |
| job_type | Job category | short_text | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| run_id | Run | opaque_id | Optional |
| step_id | Step | opaque_id | Optional |
| attempt_id | Attempt | opaque_id | Optional |
| payload_reference | Job payload reference | source_reference | Yes |
| priority | Scheduling priority | priority_code | Yes |
| scheduled_at | Earliest execution | timestamp_utc | Yes |
| expires_at | Expiry | timestamp_utc | Optional |
| state | Job state | job_state | Yes |
| lease_owner_id | Worker identity | opaque_id | Optional |
| lease_expires_at | Lease expiry | timestamp_utc | Optional |
| attempt_count | Delivery attempts | count | Yes |
| max_attempts | Maximum deliveries | count | Yes |
| deduplication_key | Duplicate key | short_text | Yes |
| last_error_code | Last normalized error | short_text | Optional |

```text
pending
scheduled
available
leased
running
completed
retry_scheduled
dead_letter
cancelled
expired
```

Priorities:

```text
emergency
critical_control
interactive
normal
background
maintenance
```

## 29. WorkerLease

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| lease_id | Lease ID | opaque_id | Yes |
| job_id | Claimed job | opaque_id | Yes |
| attempt_id | Attempt | opaque_id | Conditional |
| worker_identity_id | Worker | opaque_id | Yes |
| fencing_token | Monotonic generation | count | Yes |
| acquired_at | Acquisition time | timestamp_utc | Yes |
| last_heartbeat_at | Latest heartbeat | timestamp_utc | Yes |
| expires_at | Expiry | timestamp_utc | Yes |
| state | Lease state | lease_state | Yes |

```text
active
expired
released
revoked
superseded
```

## 30. Checkpoint

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| checkpoint_id | Checkpoint ID | opaque_id | Yes |
| run_id | Run | opaque_id | Yes |
| step_id | Step | opaque_id | Yes |
| attempt_id | Attempt | opaque_id | Yes |
| adapter_type | Adapter | adapter_type | Yes |
| adapter_version | Adapter version | version_string | Yes |
| runtime_session_reference | External session | source_reference | Optional |
| content_reference | Checkpoint content | source_reference | Yes |
| integrity_hash | Integrity digest | content_hash | Yes |
| schema_version | Checkpoint schema | version_string | Yes |
| resume_capability | Resume support/state | enum_code | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| expires_at | Expiry | timestamp_utc | Optional |

## 31. PolicySet

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| policy_set_id | Policy set ID | opaque_id | Yes |
| scope_type | Platform/org/workspace | enum_code | Yes |
| scope_id | Scope | opaque_id | Conditional |
| policy_version | Published version | version_string | Yes |
| state | Policy lifecycle | policy_state | Yes |
| effective_at | Effective time | timestamp_utc | Yes |
| content_reference | Policy definition | source_reference | Yes |
| content_hash | Integrity digest | content_hash | Yes |
| published_by | Publishing identity | opaque_id | Yes |
| supersedes_policy_set_id | Previous policy | opaque_id | Optional |

```text
draft
published
superseded
retired
invalid
```

## 32. PermissionGrant

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| permission_grant_id | Grant ID | opaque_id | Yes |
| grantee_identity_id | Recipient identity | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Conditional |
| capability_code | Granted capability | short_text | Yes |
| resource_scope | Resource bounds | json_object | Yes |
| data_classes | Allowed classifications | json_array | Yes |
| network_scope | Allowed egress | json_object | Optional |
| cost_limit | Cost bound | money_amount | Optional |
| time_limit_seconds | Time bound | duration_seconds | Optional |
| attempt_limit | Attempt bound | count | Optional |
| issued_by | Issuer | opaque_id | Yes |
| issued_at | Issue time | timestamp_utc | Yes |
| expires_at | Expiry | timestamp_utc | Optional |
| state | Grant state | grant_state | Yes |

```text
active
suspended
revoked
expired
consumed
invalid
```

## 33. PolicyDecision

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| policy_decision_id | Decision ID | opaque_id | Yes |
| policy_set_id | Policy version | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| identity_id | Evaluated actor | opaque_id | Yes |
| action_class | Normalized action | short_text | Yes |
| normalized_target | Exact target | json_object | Yes |
| input_hash | Policy input digest | content_hash | Yes |
| decision | Decision result | policy_decision | Yes |
| risk_class | Risk category | risk_class | Yes |
| reason_codes | Deterministic reasons | json_array | Yes |
| decided_at | Decision time | timestamp_utc | Yes |
| expires_at | Decision validity | timestamp_utc | Optional |

```text
allow
allow_with_guards
require_approval
deny
unknown_block
```

Risk classes:

```text
r0_informational
r1_low
r2_moderate
r3_high
r4_critical
```

## 34. ApprovalRequest

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| approval_request_id | Request ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| requester_identity_id | Requesting identity | opaque_id | Yes |
| task_id | Task | opaque_id | Yes |
| run_id | Run | opaque_id | Yes |
| step_id | Step | opaque_id | Yes |
| action_class | Action category | short_text | Yes |
| normalized_target | Exact target | json_object | Yes |
| parameters | Exact parameters | json_object | Yes |
| action_fingerprint | Action digest | action_fingerprint | Yes |
| risk_class | Risk | risk_class | Yes |
| policy_reason | Policy explanation | json_object | Yes |
| expected_effects | Expected effects | json_array | Yes |
| preview_reference | Diff/content preview | source_reference | Conditional |
| required_authority | Required approver authority | json_object | Yes |
| independence_level | Separation requirement | independence_level | Yes |
| expires_at | Expiry | timestamp_utc | Yes |
| state | Approval lifecycle | approval_state | Yes |
| version | Request version | count | Yes |

```text
requested
under_review
approved
rejected
revision_requested
expired
invalidated
cancelled
consumed
```

Independence:

```text
i0_none
i1_requester_may_approve
i2_different_human_required
i3_designated_independent_authority
```

## 35. ApprovalDecision

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| approval_decision_id | Decision ID | opaque_id | Yes |
| approval_request_id | Request | opaque_id | Yes |
| decision | Human decision | approval_decision | Yes |
| decided_by | Human identity | opaque_id | Yes |
| authority_used | Authority scope | json_object | Yes |
| rationale | Decision rationale | long_text | Optional |
| decided_at | Decision time | timestamp_utc | Yes |
| request_version | Exact request version | count | Yes |
| policy_version | Policy version | version_string | Yes |

```text
approve
reject
request_revision
```

## 36. ApprovalConsumption

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| approval_consumption_id | Consumption ID | opaque_id | Yes |
| approval_request_id | Request | opaque_id | Yes |
| attempt_id | Authorized attempt | opaque_id | Yes |
| action_fingerprint | Verified fingerprint | action_fingerprint | Yes |
| policy_version | Revalidated policy version | version_string | Yes |
| consumed_at | Consumption time | timestamp_utc | Yes |
| result_reference | Later execution result | source_reference | Optional |

## 37. MemoryRecord

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| memory_record_id | Memory ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| project_id | Project | opaque_id | Optional |
| memory_class | Memory category | memory_class | Yes |
| authority_state | Authority | memory_authority_state | Yes |
| confidence | Confidence | confidence_state | Yes |
| classification | Data class | classification_code | Yes |
| active_version_id | Current version | opaque_id | Yes |
| producer_identity_id | Producer | opaque_id | Yes |
| task_id | Source task | opaque_id | Optional |
| run_id | Source run | opaque_id | Optional |
| step_id | Source step | opaque_id | Optional |
| retention_state | Retention | retention_state | Yes |
| state | Memory lifecycle | memory_state | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| version | Aggregate version | count | Yes |

Memory classes:

```text
temporary_run_context
working_note
generated_memory
inferred_memory
user_asserted_memory
user_preference
verified_project_fact
authoritative_reference
procedure_playbook
correction_supersession
retrieval_observation
conflict_record
```

Authority states:

```text
temporary
generated
inferred
user_asserted
user_preference
review_pending
verified
authoritative_reference
disputed
superseded
expired
deleted
unavailable
unknown
```

Confidence:

```text
not_assessed
low
medium
high
conflicted
unknown
```

## 38. MemoryVersion

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| memory_version_id | Version ID | opaque_id | Yes |
| memory_record_id | Parent memory | opaque_id | Yes |
| version_number | Monotonic version | count | Yes |
| content_reference | Content | source_reference | Yes |
| normalized_summary | Bounded summary | long_text | Optional |
| language_code | Content language | short_text | Optional |
| source_references | Sources | json_array | Yes |
| authority_state | Authority of version | memory_authority_state | Yes |
| confidence | Confidence | confidence_state | Yes |
| classification | Data class | classification_code | Yes |
| valid_from | Validity start | timestamp_utc | Yes |
| valid_to | Validity end | timestamp_utc | Optional |
| supersedes_version_id | Replaced version | opaque_id | Optional |
| content_hash | Integrity digest | content_hash | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| created_by | Creator | opaque_id | Yes |

## 39. Artifact

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| artifact_id | Artifact ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| project_id | Project | opaque_id | Optional |
| task_id | Task | opaque_id | Optional |
| run_id | Run | opaque_id | Optional |
| step_id | Step | opaque_id | Optional |
| producer_identity_id | Producer | opaque_id | Yes |
| artifact_type | Artifact category | artifact_type | Yes |
| media_type | MIME media type | short_text | Yes |
| classification | Data class | classification_code | Yes |
| lifecycle_state | Artifact lifecycle | artifact_state | Yes |
| active_version_id | Current version | opaque_id | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| version | Aggregate version | count | Yes |

Types:

```text
document
code_patch
source_file
report
image
dataset
archive
log_bundle
execution_receipt
evidence_export
backup_manifest
other
```

States:

```text
proposed
staging
stored
partial
integrity_failed
under_review
accepted
rejected
superseded
archived
deleted
unavailable
```

## 40. ArtifactVersion

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| artifact_version_id | Version ID | opaque_id | Yes |
| artifact_id | Parent artifact | opaque_id | Yes |
| version_number | Monotonic version | count | Yes |
| storage_reference | Content location | source_reference | Yes |
| filename | Suggested filename | short_text | Optional |
| media_type | MIME type | short_text | Yes |
| size_bytes | Content size | byte_count | Yes |
| integrity_hash | Digest | content_hash | Yes |
| preview_state | Preview status | preview_state | Yes |
| created_at | Creation time | timestamp_utc | Yes |
| created_by | Producer | opaque_id | Yes |
| supersedes_version_id | Previous version | opaque_id | Optional |

```text
not_generated
pending
safe
blocked
failed
unavailable
```

## 41. AuditEvent

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| audit_event_id | Event ID | opaque_id | Yes |
| schema_version | Event schema | version_string | Yes |
| event_type | Event code | short_text | Yes |
| occurred_at | Source occurrence time | timestamp_utc | Yes |
| recorded_at | Platform recording time | timestamp_utc | Yes |
| actor_identity_id | Actor | opaque_id | Conditional |
| actor_identity_type | Actor type | identity_type | Conditional |
| organization_id | Organization | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Conditional |
| project_id | Project | opaque_id | Optional |
| task_id | Task | opaque_id | Optional |
| run_id | Run | opaque_id | Optional |
| step_id | Step | opaque_id | Optional |
| correlation_id | Correlation | correlation_id | Yes |
| causation_id | Causing event/command | opaque_id | Optional |
| target_reference | Target | source_reference | Optional |
| result | Event result | event_result | Yes |
| reason_codes | Reasons | json_array | Optional |
| source_class | Source class | source_class | Yes |
| payload_reference | Detailed payload | source_reference | Optional |
| redaction_state | Redaction | redaction_state | Yes |
| integrity_reference | Integrity proof | source_reference | Optional |

Results:

```text
success
failure
denied
partial
unknown
not_applicable
```

Redaction:

```text
not_required
redacted
partially_redacted
restricted
unknown
```

## 42. ExecutionReceipt

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| execution_receipt_id | Receipt ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| task_id | Task | opaque_id | Yes |
| run_id | Run | opaque_id | Yes |
| receipt_type | Receipt category | short_text | Yes |
| task_snapshot_reference | Snapshot | source_reference | Yes |
| adapter_model_tool_references | Execution identities | json_array | Yes |
| policy_decision_references | Policy decisions | json_array | Yes |
| approval_references | Approval chain | json_array | Optional |
| step_summary | Step/attempt summary | json_array | Yes |
| artifact_references | Produced artifacts | json_array | Optional |
| usage_cost_references | Usage/cost | json_array | Optional |
| known_side_effects | Side effects | json_array | Yes |
| evidence_gaps | Missing evidence | json_array | Yes |
| terminal_state | Run terminal state | run_state | Yes |
| generated_at | Generation time | timestamp_utc | Yes |
| schema_version | Receipt schema | version_string | Yes |

```text
not_requested
pending
complete
partial
failed
unavailable
```

## 43. UsageEvent

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| usage_event_id | Usage event ID | opaque_id | Yes |
| source_type | Provider/adapter/tool/local | usage_source_type | Yes |
| source_reference | External/internal source | source_reference | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| project_id | Project | opaque_id | Optional |
| task_id | Task | opaque_id | Optional |
| run_id | Run | opaque_id | Optional |
| step_id | Step | opaque_id | Optional |
| provider_id | Provider | short_text | Optional |
| model_id | Actual model | short_text | Optional |
| tool_id | Tool | short_text | Optional |
| metric | Usage metric | usage_metric | Yes |
| quantity | Quantity | count or decimal | Yes |
| occurred_at | Usage time | timestamp_utc | Yes |
| state | Usage state | usage_state | Yes |
| deduplication_key | Duplicate protection | short_text | Yes |

Sources:

```text
provider_reported
adapter_reported
tool_reported
locally_measured
imported_reconciliation
```

States:

```text
reported
calculated
estimated
pending
unavailable
unattributed
duplicate
reconciled
mismatched
```

Metrics:

```text
input_tokens
output_tokens
total_tokens
request_count
compute_seconds
wall_seconds
storage_bytes
network_bytes
tool_calls
other
```

## 44. CostRecord

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| cost_record_id | Cost record ID | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Yes |
| usage_event_id | Related usage | opaque_id | Optional |
| source_type | Cost source | cost_source_type | Yes |
| amount | Decimal cost | money_amount | Conditional |
| currency | Currency code | currency_code | Conditional |
| pricing_version | Pricing version | version_string | Optional |
| calculation_method | Method | short_text | Optional |
| freshness_state | Freshness | freshness_state | Yes |
| state | Cost state | cost_state | Yes |
| calculated_at | Calculation time | timestamp_utc | Optional |

Sources:

```text
provider_reported
provider_invoice
calculated
estimated
manual_reconciliation
unknown
```

States:

```text
known
estimated
pending
unavailable
unattributed
mismatched
reconciled
unknown
```

## 45. Budget

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| budget_id | Budget ID | opaque_id | Yes |
| scope_type | Workspace/project/task/run | enum_code | Yes |
| scope_id | Scope ID | opaque_id | Yes |
| period_start | Start | timestamp_utc | Yes |
| period_end | End | timestamp_utc | Yes |
| currency | Currency | currency_code | Yes |
| soft_limit | Warning threshold | money_amount | Optional |
| hard_limit | Blocking threshold | money_amount | Optional |
| spent_amount | Known spend | money_amount | Yes |
| reserved_amount | Reserved spend | money_amount | Yes |
| state | Budget state | budget_state | Yes |
| version | Aggregate version | count | Yes |

```text
active
soft_limit_reached
hard_limit_reached
suspended
expired
closed
unknown
```

## 46. ComponentHealth

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| component_health_id | Health record ID | opaque_id | Yes |
| component_id | Component/integration ID | short_text | Yes |
| registration_state | Registration | integration_state | Yes |
| reachability_state | Reachability | reachability_state | Yes |
| validation_state | Validation | validation_state | Yes |
| readiness_state | Readiness | readiness_state | Yes |
| last_observed_at | Observation time | timestamp_utc | Yes |
| evidence_reference | Health evidence | source_reference | Optional |
| limitations | Known limitations | json_array | Optional |
| version | Version | count | Yes |

Health:
```text
healthy
degraded
unhealthy
stale
unknown
disabled
```

Reachability:
```text
reachable
unreachable
intermittent
not_tested
unknown
```

Validation:
```text
not_validated
validating
validated
partially_validated
failed
expired
unknown
```

Readiness:
```text
ready
degraded
blocked_configuration
blocked_identity
blocked_policy
blocked_dependency
blocked_security
maintenance
unknown
```

## 47. BackupOperation

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| backup_operation_id | Backup ID | opaque_id | Yes |
| requested_by | Requester | opaque_id | Yes |
| scope | Backup scope | json_object | Yes |
| state | Backup state | backup_state | Yes |
| manifest_reference | Manifest | source_reference | Yes |
| target_reference | Backup target | source_reference | Yes |
| build_identity | Application build | version_string | Yes |
| schema_identity | Data schema | version_string | Yes |
| started_at | Start | timestamp_utc | Yes |
| completed_at | Completion | timestamp_utc | Optional |
| integrity_result | Integrity result | integrity_state | Yes |

```text
requested
running
complete
partial
failed
cancelled
expired
```

## 48. BackupManifest

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| backup_manifest_id | Manifest ID | opaque_id | Yes |
| backup_operation_id | Backup operation | opaque_id | Yes |
| schema_version | Manifest schema | version_string | Yes |
| included_stores | Included logical stores | json_array | Yes |
| excluded_stores | Exclusions | json_array | Yes |
| record_counts | Counts by entity/store | json_object | Yes |
| object_counts | Content-object counts | json_object | Optional |
| total_size_bytes | Total size | byte_count | Yes |
| classification | Highest class | classification_code | Yes |
| encryption_state | Encryption | encryption_state | Yes |
| checksums | Integrity checks | json_array | Yes |
| component_results | Per-component state | json_array | Yes |
| created_at | Manifest time | timestamp_utc | Yes |

Encryption:

```text
not_required
encrypted
partially_encrypted
not_encrypted
unknown
```

Integrity:

```text
not_checked
valid
invalid
partial
unknown
```

## 49. RestoreOperation

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| restore_operation_id | Restore ID | opaque_id | Yes |
| requested_by | Requester | opaque_id | Yes |
| approved_by | Approver | opaque_id | Yes |
| backup_reference | Backup set | source_reference | Yes |
| target_environment | Restore target | short_text | Yes |
| maintenance_window_id | Maintenance reference | opaque_id | Yes |
| state | Restore state | restore_state | Yes |
| started_at | Start | timestamp_utc | Yes |
| completed_at | Completion | timestamp_utc | Optional |
| recovery_duration_seconds | Duration | duration_seconds | Optional |
| data_loss_summary | Data loss/rollback summary | json_object | Optional |
| component_results | Restore components | json_array | Yes |

```text
requested
approved
validating
running
reconciling
complete
partial
failed
cancelled
```

## 50. MigrationRecord

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| migration_id | Migration ID | short_text | Yes |
| source_schema_version | From version | version_string | Yes |
| target_schema_version | To version | version_string | Yes |
| description | Purpose | long_text | Yes |
| risk_class | Risk | risk_class | Yes |
| backup_required | Requires backup | boolean | Yes |
| state | Migration state | migration_state | Yes |
| started_at | Start | timestamp_utc | Optional |
| completed_at | Completion | timestamp_utc | Optional |
| verification_reference | Verification evidence | source_reference | Optional |
| executed_by | Operator identity | opaque_id | Optional |

```text
planned
approved
running
verifying
complete
failed
recovery_required
rolled_forward
cancelled
```

## 51. Common integration fields

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| integration_id | Integration registration ID | opaque_id | Yes |
| integration_type | Integration class | short_text | Yes |
| implementation_version | Runtime/adapter version | version_string | Yes |
| endpoint_reference | Endpoint/process reference | source_reference | Conditional |
| configuration_reference | Configuration reference | source_reference | Yes |
| secret_reference | Secret reference | source_reference | Conditional |
| compatibility_state | Contract compatibility | compatibility_state | Yes |
| last_validated_at | Last validation | timestamp_utc | Optional |

Lifecycle:

```text
unregistered
registered
configured
reachable
validated
ready
degraded
unreachable
incompatible
disabled
revoked
retired
```

Compatibility:

```text
compatible
compatible_with_reduced_capability
incompatible
unknown
upgrade_required
```

## 52. Common request envelope

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| request_id | Request ID | opaque_id | Yes |
| schema_version | Contract schema | version_string | Yes |
| organization_id | Organization | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Conditional |
| identity_id | Requesting identity | opaque_id | Yes |
| correlation_id | Correlation | correlation_id | Yes |
| causation_id | Causing command/event | opaque_id | Optional |
| idempotency_key | Duplicate protection | idempotency_key | Conditional |
| requested_at | Request time | timestamp_utc | Yes |
| expires_at | Request expiry | timestamp_utc | Optional |
| data_classification | Highest class | classification_code | Yes |

## 53. Common response envelope

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| response_id | Response ID | opaque_id | Yes |
| request_id | Related request | opaque_id | Yes |
| schema_version | Contract schema | version_string | Yes |
| status | Response status | response_status | Yes |
| result_reference | Result | source_reference | Optional |
| error | Normalized error | json_object | Optional |
| retryable | Retry hint | boolean | Yes |
| side_effect_certainty | Effect knowledge | side_effect_certainty | Yes |
| external_reference | External ID/session | source_reference | Optional |
| recorded_at | Platform recording time | timestamp_utc | Yes |

```text
accepted
completed
failed
denied
partial
pending
unknown
```

## 54. Common event envelope

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| event_id | Event ID | opaque_id | Yes |
| event_type | Event code | short_text | Yes |
| schema_version | Event schema | version_string | Yes |
| producer_context | Producing bounded context | short_text | Yes |
| organization_id | Organization | opaque_id | Yes |
| workspace_id | Workspace | opaque_id | Conditional |
| aggregate_type | Aggregate type | short_text | Yes |
| aggregate_id | Aggregate ID | opaque_id | Yes |
| aggregate_version | Aggregate version | count | Yes |
| correlation_id | Correlation | correlation_id | Yes |
| causation_id | Causing ID | opaque_id | Optional |
| actor_identity_id | Actor | opaque_id | Conditional |
| occurred_at | Source occurrence | timestamp_utc | Yes |
| recorded_at | Platform recording | timestamp_utc | Yes |
| classification | Data class | classification_code | Yes |
| payload | Event payload | json_object | Yes |
| redaction_state | Redaction | redaction_state | Yes |

## 55. Classification vocabulary

```text
public
internal
confidential
secret
restricted
```

Highest class governs composites; derived content inherits classification; `secret` values remain outside ordinary content stores; `restricted` processing is excluded by default.

## 56. Source-class vocabulary

```text
authoritative_platform
authoritative_external
external_reported
calculated
estimated
generated
user_asserted
verified_reference
unknown
unavailable
stale
conflicted
```

## 57. Retention-state vocabulary

```text
transient
short
operational
evidence
project
user_controlled
security
backup
hold
expired
deletion_requested
purge_pending
purged
```

Exact periods remain outside this draft.

## 58. Freshness vocabulary

```text
current
aging
stale
expired
unknown
not_applicable
```

## 59. Effect-class vocabulary

```text
read_only
local_reversible
local_destructive
external_reversible
external_consequential
security_sensitive
financial
production
unknown
```

`financial`, `production`, and `unknown` are blocked for MVP execution.

## 60. Autonomy-level vocabulary

```text
l0_prohibited
l1_observe
l2_draft_prepare
l3_guarded_execution
l4_approval_gated_execution
l5_high_autonomy_orchestration
```

`l5_high_autonomy_orchestration` is unavailable in MVP.

## 61. Error object

| Field | Definition | Type | Required |
| --- | --- | --- | --- |
| code | Stable error code | short_text | Yes |
| message | Safe user-facing explanation | short_text | Yes |
| details_reference | Restricted detailed evidence | source_reference | Optional |
| retryable | Whether retry may be attempted | boolean | Yes |
| side_effect_certainty | Effect knowledge | side_effect_certainty | Yes |
| correlation_id | Correlation | correlation_id | Yes |
| remediation_code | Suggested next action | short_text | Optional |

Errors must not expose secrets, private stack traces, or hidden authorization details.

## 62. State-reason object

```json
{
  "code": "RUN_WAITING_FOR_APPROVAL",
  "message": "An exact human approval is required before this action.",
  "source": "policy_engine",
  "evidence_reference": "audit://...",
  "observed_at": "2026-07-19T12:00:00Z"
}
```

Codes are stable, messages are safe, and timestamps use UTC.

## 63. Normalized target object

```json
{
  "target_type": "git_repository",
  "repository_id": "repo_...",
  "worktree_id": "worktree_...",
  "branch_name": "feature/example",
  "path": "docs/example.md",
  "remote_name": "origin",
  "external_target_reference": null
}
```

Targets are canonicalized before policy evaluation and approval fingerprinting.

## 64. Execution bounds object

```json
{
  "max_wall_seconds": 3600,
  "max_active_seconds": 1800,
  "max_steps": 50,
  "max_attempts": 5,
  "max_consecutive_failures": 3,
  "max_cost_amount": "10.00",
  "currency": "USD",
  "max_output_bytes": 104857600,
  "expires_at": "2026-07-19T13:00:00Z"
}
```

## 65. Evidence reference object

```json
{
  "evidence_type": "audit_event",
  "reference": "audit_event_id",
  "source_class": "authoritative_platform",
  "classification": "internal",
  "integrity_hash": null
}
```

## 66. Secret reference object

```json
{
  "secret_reference_id": "secret_ref_...",
  "purpose": "model_provider_authentication",
  "workspace_id": "workspace_...",
  "capability_code": "model.inference",
  "target": "provider.example",
  "expires_at": null
}
```

Raw secret values are prohibited.

## 67. Validation rules

- Validate identifier format, entity type, and workspace ownership.
- Validate controlled states and permitted transitions.
- Validate organization/workspace/project consistency.
- Validate classification inheritance and destination compatibility.
- Validate content size, encoding, safe rendering, secret detection, and schema version.
- Reject ambiguous targets, paths, recipients, model identities, or side-effect classes.

## 68. Nullability rules

Use `null` only when a field is genuinely optional or not applicable. Use explicit controlled states for unknown, unavailable, stale, conflicted, and pending. Empty strings and zero values must not represent unknown state.

## 69. Default-value rules

Defaults must never grant authority, lower classification, mark health as healthy, mark evidence as complete, make model/provider identity known, enable egress/tools, approve an action, or convert unknown cost to zero. Safe defaults are deny, unknown, disabled, or not validated.

## 70. Historical-data rules

Historical records preserve original identifiers, source, timestamps, state, prior versions, correction/supersession links, policy and approval context, and evidence. Corrections create new records or versions rather than rewriting history.

## 71. Search and index fields

Every protected index entry should carry workspace, optional project, entity type and ID, lifecycle state, classification, authority/source class, freshness, active-version flag, source-update time, and index-update time. Embeddings inherit classification and scope.

## 72. Cache fields

Protected cache keys include workspace, identity or permission projection where needed, resource/version, query/filter, classification, and locale where relevant. Security-sensitive entries require revocation-aware invalidation.

## 73. Export metadata

Exports include export ID, schema version, source build, workspace scope, selected entities, time range, classification, redaction state, generated time, generating identity, manifest, integrity hash, and evidence reference.

## 74. Import metadata

Imports include import ID, source, schema version, target workspace, classification, validation result, duplicate strategy, error report, provenance, importing identity, and import time.

## 75. Machine-readable dictionary strategy

A future machine-readable representation may use YAML, JSON Schema, OpenAPI components, AsyncAPI schemas, and generated documentation. It must preserve canonical name, semantic type, required/optional status, allowed values, owner, source class, classification, validation, deprecation, and version.

## 76. Deprecation rules

A field may be deprecated only when a replacement, migration path, compatibility period, consumer impact, and removal version are documented. Deprecated fields are never silently repurposed.

## 77. Field-change classification

Non-breaking changes are generally optional additive fields or safe documentation clarifications. Required-field additions, type changes, enum removals, semantic changes, nullability changes, source-of-truth changes, and classification changes are potentially breaking and require versioning.

## 78. Ownership rules

Every canonical field has one semantic owner, optional technical steward, classification owner, validation authority, and change approver. The semantic owner is the bounded context owning the meaning, not necessarily every service storing a copy.

## 79. Cross-document naming rules

`AGC-001`, `CAP-001`, `MOD-001`, `RUN-001`, `APR-001`, `ART-001`, `API-001`, `EVT-001`, `TST-001`, `OBS-001`, and `OPS-001` must reuse these canonical names. Divergence requires an explicit alias or deprecation mapping.

## 80. Quality checks

Automated checks should detect duplicate names, missing owners, undefined enum values, inconsistent state names, invalid identifier suffixes, unknown represented as zero/empty, secret fields in ordinary schemas, protected entities without workspace scope, non-UTC timestamps, and undocumented breaking changes.

## 81. Security checks

The dictionary must contain no raw-secret field, client-provided authorization truth, human role on an agent identity, unscoped protected record, approval without fingerprint, run without snapshot, attempt without side-effect certainty, artifact without classification, memory without source, or audit event without applicable scope and correlation.

## 82. Requirement traceability

| Requirement area | Dictionary coverage |
| --- | --- |
| Identity and access | Identities, sessions, memberships, roles |
| Workspaces/projects | Scope and lifecycle fields |
| Agents/models/tools | Registration, capability, health |
| Tasks/runs | Snapshots, runs, steps, attempts |
| Approvals | Request, decision, consumption |
| Memory | Classes, authority, confidence, versions |
| Artifacts | Metadata, versions, integrity, preview |
| Audit | Event envelope, source, redaction |
| Cost | Usage, cost, budget, freshness |
| Operations | Health, backup, restore, migration |
| APIs/events | Common envelopes and errors |
| Security | Classification, scope, effect, evidence |

## 83. ADR backlog

- `ADR-CANDIDATE-DCT-001` — Identifier format.
- `ADR-CANDIDATE-DCT-002` — Machine-readable dictionary format.
- `ADR-CANDIDATE-DCT-003` — Closed versus extensible enum policy.

## 83A. Conversation canonical fields

The following fields are canonical for the `Conversation` aggregate and related records:

| Field | Semantic type | Required | Meaning |
|---|---|---|---|
| `conversation_id` | UUID | Yes | Stable conversation identifier |
| `workspace_id` | UUID | Yes | Isolation boundary |
| `owner_identity_id` | UUID | Yes | Human or service owner |
| `project_id` | UUID | No | Linked durable domain |
| `mission_id` | UUID | No | Linked outcome objective |
| `task_id` | UUID | No | Linked executable work |
| `run_id` | UUID | No | Linked execution |
| `visibility` | enum | Yes | `private`, `project`, or `workspace` |
| `capture_boundary` | enum | Yes | Agent OS interface or adapter that observed the content |
| `retention_profile` | enum | Yes | `R0` through `R6` under DAT-002 |
| `classification` | enum | Yes | Data classification applied to content |
| `deleted_at` | timestamp | No | Effective deletion time |

`ConversationMessage` additionally requires `message_id`, `conversation_id`, `actor_chain`, `role`, `content_reference`, `provider_reference`, `created_at`, and `correlation_id`. Content references must not embed raw secrets. Derived artifacts, memory records, indexes, and previews retain a source conversation reference and cannot broaden its visibility.

## 83B. Message canonical fields

`Message` is the canonical externally referenced record for one captured conversational contribution. `ConversationMessage` is the domain-model name for the same record; implementations must not expose two competing identifiers or schemas.

| Field | Semantic type | Required | Meaning |
|---|---|---:|---|
| `message_id` | UUID | Yes | Stable message identifier, unique within the workspace |
| `conversation_id` | UUID | Yes | Owning conversation; immutable after creation |
| `workspace_id` | UUID | Yes | Isolation and authorization partition |
| `actor_chain` | array of identity/provider references | Yes | Ordered human, agent, adapter, and provider provenance |
| `role` | enum | Yes | `user`, `assistant`, `system`, `tool`, or `event` |
| `content_reference` | protected reference | Yes | Reference to content storage; raw secrets are prohibited |
| `provider_reference` | object or null | Yes | Provider/model/adapter observation, or explicit unknown |
| `created_at` | UTC timestamp | Yes | Server-observed creation time |
| `correlation_id` | UUID | Yes | Request/run correlation identifier |
| `classification` | enum | Yes | Effective data classification |
| `retention_profile` | enum | Yes | Inherited or explicitly assigned `R0` through `R6` |
| `deleted_at` | UTC timestamp or null | Yes | Tombstone time when deletion has taken effect |

Messages inherit conversation visibility and retention. A message cannot be moved between conversations or workspaces, and a projection, export, search index, or notification cannot broaden its visibility. Message recording is idempotent on `(conversation_id, message_id)` and must preserve provenance when a provider reference is unavailable.

## 84. Open decisions

1. Identifier format.
2. Language-code standard.
3. Initial currencies.
4. Semantic-to-physical type mappings.
5. Closed versus extensible enums.
6. Public API field exposure.
7. URI versus typed source references.
8. Mandatory content hashes.
9. Soft-delete entities.
10. Mandatory timestamps.
11. Retention fields stored on entities.
12. Extension namespaces.
13. Searchable and indexable fields.
14. Canonical machine-readable format.
15. Field-level classification overrides.
16. Aliases requiring migration.
17. Shared versus domain-specific errors.
18. Localization fields.
19. Companion documents to register.

## 85. Risks

| Risk | Consequence | Response |
| --- | --- | --- |
| Dictionary too abstract | Implementation drift | Generate machine-readable schemas |
| Physical design leaks into semantics | Vendor lock-in | Semantic types first |
| Enum sprawl | Inconsistent behavior | Controlled ownership |
| Unknown represented inconsistently | Misleading state | Explicit vocabulary |
| Field reused with new meaning | Data corruption | Version/deprecation rules |
| Missing workspace field | Leakage | Mandatory scope checks |
| Raw secret field introduced | Credential compromise | Schema review/scanning |
| API/event names diverge | Integration defects | Shared dictionary |
| Source and authority conflated | False trust | Separate fields |
| Unowned field | Governance gap | Owner required |
| Null/empty ambiguity | Logic errors | Nullability rules |
| Classification lowered | Disclosure | Inheritance and review |

## 86. Assumptions

The domain model is stable enough for a first dictionary; detailed contracts will refine subsets; semantic types can remain vendor-neutral; fields can be versioned; a machine-readable representation can be generated later; data owners will review vocabularies; API and event contracts will reuse these names.

## 87. Constraints

No final physical schema, database technology, retention periods, secret values, public multi-tenant fields, production/financial execution fields, or accepted mock source-of-truth fields are defined here. These remain implementation-level decisions; this dictionary is the approved semantic contract.

## 88. Acceptance criteria

DCT-001 may advance to `1.0.0` when:

1. Product accepts the business definitions.
2. Architecture accepts entity and field boundaries.
3. Data accepts semantic types, ownership, source, lifecycle, and validation.
4. Security accepts scope, classification, secrets, and approval fields.
5. Quality confirms machine-checkable consistency.
6. All core aggregates have canonical fields.
7. Primary lifecycle states are defined.
8. Unknown, unavailable, stale, and conflicted states are explicit.
9. Source and authority remain distinct.
10. Protected records can be workspace-scoped.
11. Downstream contracts reuse the vocabulary.
12. No field silently grants authority.
13. No raw-secret field exists.
14. Compatibility rules are accepted.
15. Metadata, terminology, Markdown, and examples validate.

## 89. Downstream impact

| Document | Required use |
| --- | --- |
| AGC-001 | Adapter, request, response, and health fields |
| CAP-001 | Capability vocabulary |
| MOD-001 | Model/provider/profile fields |
| RUN-001 | Run/step/attempt/job/lease/checkpoint fields |
| APR-001 | Approval fields and states |
| ART-001 | Artifact fields |
| API-001 | Canonical resources and envelopes |
| EVT-001 | Event envelope and enums |
| DEV-001 | Schema generation and validation |
| TST-001 | Field, enum, nullability, compatibility tests |
| QAG-001 | Dictionary consistency gates |
| OBS-001 | Telemetry/correlation fields |
| OPS-001 | Health, backup, migration fields |
| RTM-001 | Field/contract/test traceability |

## 90. Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.2.0`
- Approved by: Product, Architecture, Data, Security, and Quality owners under explicit stakeholder authorization communicated by the product owner
- Approval date: 2026-08-13
- Required next action: implement and validate the dictionary; approval does not claim implementation

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial canonical dictionary covering entities, fields, semantic types, states, classifications, source classes, request/response/event envelopes, validation, compatibility, and governance |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `PRD-001` — Product Requirements Document
- `SRS-001` — Functional Requirements Specification
- `NFR-001` — Non-Functional Requirements
- `AUT-001` — Autonomy and Approval Matrix
- `RTM-001` — Requirements Traceability Matrix
- `SAD-001` — System Architecture Description
- `C4-001` — System Context Diagram
- `C4-002` — Container Diagram
- `DDD-001` — Domain Model
- `DAT-001` — Data Architecture
- `MEM-001` — Memory and Knowledge Architecture
- `ORC-001` — Workflow and Orchestration Architecture
- `INT-001` — Integration Architecture
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
