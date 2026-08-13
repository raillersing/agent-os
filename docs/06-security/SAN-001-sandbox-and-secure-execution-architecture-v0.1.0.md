---
document_id: SAN-001
title: Agent OS Sandbox and Secure Execution Architecture
version: 0.1.0
status: approved
owner: security-owner
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
related_documents: []
dependencies:
  - SAD-001
  - SEC-001
  - THR-001
  - RUN-001
  - AGC-001
  - CAP-001
  - POL-001
related_official_documents:
  - DOC-000
  - GLO-001
  - SCP-001
  - PRD-001
  - SRS-001
  - NFR-001
  - AUT-001
  - SAD-001
  - DDD-001
  - DAT-001
  - SEC-001
  - THR-001
  - AGC-001
  - CAP-001
  - RUN-001
  - APR-001
  - ART-001
  - API-001
  - EVT-001
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
  - SEC-002
  - DAT-002
  - AUD-001
  - CST-001
  - ADP-HER-001
  - ADP-CDX-001
  - UXA-001
  - DSN-001
  - A11Y-001
  - VVR-001
related_adrs:
  - ADR-CANDIDATE-SAN-001
  - ADR-CANDIDATE-SAN-002
  - ADR-CANDIDATE-SAN-003
  - ADR-CANDIDATE-SAN-004
  - ADR-CANDIDATE-SAN-005
  - ADR-CANDIDATE-SAN-006
  - ADR-CANDIDATE-SAN-007
  - ADR-CANDIDATE-SAN-008
---

# SAN-001 — Agent OS Sandbox and Secure Execution Architecture

> **Status: Approved baseline — 2026-08-13.** This document defines the proposed sandbox and secure-execution architecture for Agent OS. It covers execution profiles, process and filesystem isolation, network egress, secrets, identities, resource quotas, Tool Gateway enforcement, artifact staging, violations, recovery, deployment, operations, testing, and adapter integration. It does not select a final container, VM, microVM, namespace, or enforcement technology; authorize unrestricted host access; or permit agents to weaken their own sandbox.

## 1. Purpose

Agent OS may execute code, commands, tests, repository operations, file transformations, model-assisted workflows, and external integrations. These activities can affect the host, repositories, data, credentials, external systems, budgets, and other workspaces.

The sandbox architecture limits blast radius and makes execution isolated, governed, attributable, resource-bounded, observable, recoverable, evidence-producing, and explicit about uncertainty.

## 2. Objectives

The architecture must:

- isolate untrusted execution from the control plane and host;
- enforce least privilege for processes, filesystem, network, secrets, and devices;
- prevent cross-workspace access;
- require an immutable sandbox specification per attempt;
- prevent agent or adapter self-elevation;
- mediate protected tools through a Tool Gateway;
- stage outputs before artifact acceptance;
- enforce CPU, memory, process, disk, network, and time limits;
- preserve exact run, step, attempt, policy, approval, and identity context;
- support cancellation, cleanup, and reconciliation;
- block blind retries when effect certainty is unknown.

## 3. Non-goals

This document does not select final sandbox technology, guarantee perfect kernel-level containment, permit arbitrary host shell access, permit unrestricted internet, define every tool permission, replace IAM/policy/approval/audit contracts, or claim commercial multi-tenant readiness without validation.

## 4. Principle — Control plane outside the sandbox

The sandbox cannot mutate authoritative platform state or grant itself permissions.

## 5. Principle — Default-denied execution

No process, file, network, secret, device, or tool access exists unless explicitly granted.

## 6. Principle — One attempt, one execution identity

Every attempt has its own identity, workspace scope, profile, storage, leases, and evidence.

## 7. Principle — Workspace isolation before mounting

Authorization occurs before repositories, artifacts, or paths are exposed.

## 8. Principle — Profiles selected by policy

Agents may request a capability; policy chooses the effective profile.

## 9. Principle — No raw secrets by default

Secrets are purpose-bound, short-lived, and brokered.

## 10. Principle — Network is explicit

Outbound destinations, ports, protocols, and data classes are allowlisted.

## 11. Principle — Outputs are untrusted

Generated files and logs are staged, classified, validated, and possibly quarantined.

## 12. Principle — Cancellation is not rollback

Stopping a process does not prove external effects were reversed.

## 13. Principle — Unknown effect blocks unsafe retry

Reconciliation is required before a protected action is repeated.

## 14. Principle — Evidence before trust

Process success alone does not prove a protected effect.

## 15. Principle — Containment failure is an incident

Escape, cross-workspace access, or secret exposure triggers containment.

## 16. Bounded context

The secure-execution context owns sandbox profiles, immutable specifications, environment preparation, mounts, network rules, process/resource controls, secret plans, tool bindings, output staging, cleanup, violations, and sandbox evidence.

It does not own run lifecycle, policy decisions, approvals, artifact acceptance, or identity lifecycle.

## 17. Logical architecture

```text
Orchestrator
→ Policy evaluation
→ Approval validation
→ Sandbox Planner
→ Sandbox Executor
→ isolated process tree
→ Tool Gateway
→ output staging
→ validation/quarantine
→ evidence and run reconciliation
```

## 18. Sandbox Planner

Builds the effective specification from capability, policy obligations, data classification, identity, and environment.

## 19. Profile Registry

Stores immutable, versioned profiles and compatibility metadata.

## 20. Sandbox Executor

Creates, monitors, stops, and destroys isolated environments.

## 21. Tool Gateway

Mediates protected capabilities and external effects.

## 22. Secret Broker

Provides purpose-bound access without broadly exposing raw values.

## 23. Network Enforcement Layer

Applies destination, protocol, DNS, proxy, and bandwidth rules.

## 24. Filesystem Stager

Prepares read-only inputs, writable roots, repository worktrees, and output collection.

## 25. Resource Controller

Enforces CPU, memory, process, disk, I/O, timeout, and concurrency limits.

## 26. Evidence Collector

Records profile, runtime, commands, tool calls, outputs, violations, and cleanup.

## 27. Validation and Quarantine Service

Scans outputs before wider use.

## 28. Cleanup/Reconciliation Worker

Destroys environments and resolves uncertain effects.

## 29. Secure-execution request

A request includes run/step/attempt IDs, principal and workload identity, workspace, capability, tool intent, immutable task snapshot, policy and approval references, requested profile, inputs, repository references, filesystem/network/secret needs, resource estimate, timeout, expected outputs, and effect class.

## 30. Immutable sandbox specification

The planner produces a specification containing profile/version, runtime image/digest, workspace/attempt scope, process identity, mounts, writable paths, network rules, environment allowlist, secret plan, tool bindings, limits, output paths, evidence requirements, cleanup policy, expiry, and integrity hash.

Any material privilege change requires a new specification and re-evaluation.

## 31. Profile taxonomy

```text
SAN-P0 — no execution
SAN-P1 — read-only analysis
SAN-P2 — isolated local computation
SAN-P3 — repository write without external network
SAN-P4 — restricted network integration
SAN-P5 — protected external side effect
SAN-P6 — recovery or forensic execution
```

## 32. Profile — SAN-P0

No process is started; used for denied, unavailable, or simulation-only actions.

## 33. Profile — SAN-P1

Read-only inputs, no write, network, or secret access.

## 34. Profile — SAN-P2

Writable ephemeral work area with no host/repository mutation and no external network.

## 35. Profile — SAN-P3

Attempt-specific repository worktree writable; remote Git and network denied.

## 36. Profile — SAN-P4

Allowlisted destinations and brokered secrets under stronger evidence.

## 37. Profile — SAN-P5

Exact approved protected effect with target, data, idempotency, receipt, and reconciliation.

## 38. Profile — SAN-P6

Restricted recovery/forensic execution with explicit human governance.

## 39. Profile selection

Selection considers capability, effect class, classification, destination, repository write intent, network and secret requirements, environment, identity, approval, artifact type, resources, and policy obligations.

Use the most restrictive profile that can satisfy the approved action.

## 40. No in-place privilege broadening

A running sandbox cannot broaden mounts, network, secrets, tools, or resource authority. A broader request creates a new specification, new policy evaluation, new approval where needed, and normally a new attempt.

## 41. Lifecycle

```text
planned
→ preparing
→ prepared
→ starting
→ running
→ stopping
→ stopped
→ collecting
→ validating
→ cleaning
→ cleaned
```

Exceptional states include preparation failure, policy violation, limit exceeded, escape suspected, quarantine, cleanup failure, effect unknown, and reconciliation required.

## 42. Preparation

Preparation verifies profile, policy, approval, workspace, artifact versions, runtime digest, storage, mounts, identity, limits, network policy, Tool Gateway bindings, secret broker, and pre-execution evidence before any user command runs.

## 43. Start and runtime verification

The executor creates the process tree under a unique workload identity and verifies that observed mounts, network mode, user, runtime image, profile, and limits match the specification.

## 44. Runtime monitoring

Monitor process tree, CPU, memory, disk, I/O, open files, network attempts, Tool Gateway calls, secret leases, output growth, heartbeat, timeout, policy violations, and executor health.

## 45. Cancellation and stop

Cancellation stops new tool calls, attempts graceful termination, force-kills after a bounded period, revokes secrets and network, collects partial evidence, cleans the environment, and reconciles protected effects.

Cancellation acknowledgement is not cancellation completion and never implies rollback.

## 46. Collection and validation

Only declared output roots are collected. Outputs are hashed, classified, size-checked, scanned, validated, and proposed as artifacts. Unexpected outputs are ignored, quarantined, or recorded as violations according to policy.

## 47. Cleanup

Cleanup terminates all processes, removes network, revokes leases, unmounts filesystems, deletes ephemeral storage, clears credentials, verifies no orphan process, and records the result.

Cleanup failure remains visible even when the command itself succeeded.

## 48. Execution identity

Each attempt receives a unique sandbox instance, short-lived workload identity, workspace binding, profile binding, run/step/attempt binding, and expiration. It never reuses a human credential or another attempt's identity.

## 49. Actor separation

Evidence distinguishes requesting human/service principal, logical agent profile, adapter runtime, sandbox workload identity, Tool Gateway executor, and external target. These cannot be collapsed into one ambiguous `agent` actor.

## 50. Operating-system privilege

Processes should run as a non-root dedicated user. Directional controls include dropped capabilities, no privileged mode, no host PID/network namespace, no host devices, no runtime socket, restricted ptrace, controlled IPC, read-only runtime filesystems, and no arbitrary mount operations.

## 51. Process-tree policy

The sandbox owns a bounded process tree with maximum process count, inherited limits, process groups for cancellation, no surviving daemon, and controlled interpreter/compiler availability.

## 52. Governed shell

Shell is a specific governed capability, not a generic right. It requires exact working directory, structured command or validated template, environment allowlist, timeout, profile, output limit, approval when required, and evidence.

Unrestricted host shell access is prohibited.

## 53. Command construction

Prefer structured argument arrays. Where a shell is required, use a fixed interpreter, controlled PATH, disabled profile loading, safe quoting, no untrusted interpolation, and redacted evidence.

## 54. Environment variables

Only allowlisted variables are supplied. Host credentials, cloud tokens, platform DB credentials, user shell initialization, unrelated workspace IDs, and control-plane session tokens are denied.

## 55. Filesystem zones

```text
/runtime      read-only runtime
/input        read-only staged inputs
/work         writable ephemeral area
/repository   profile-dependent worktree
/output       declared output roots
/tmp          quota-bound temporary storage
/secrets      ephemeral handles only where unavoidable
/evidence     executor-controlled evidence path
```

## 56. Read-only inputs

Inputs are exact versioned artifacts, snapshots, or repository states exposed read-only. The sandbox cannot mutate authoritative source content or metadata.

## 57. Writable roots

Writes are limited to declared attempt-scoped roots. Direct write access to platform configuration, databases, audit, secret stores, deployments, arbitrary home directories, or other workspaces is prohibited.

## 58. Repository isolation

Repository work uses an attempt-specific worktree, clone, or snapshot with explicit repository ID, base commit, branch, clean/dirty state, allowed paths, write mode, Git boundaries, diff evidence, and cleanup.

## 59. Git capability separation

```text
git.read
git.modify_worktree
git.stage
git.commit
git.push
pull_request.create
pull_request.update
branch.merge
tag.create
release.publish
```

Local modification or commit never implies push, PR, merge, tag, or release authority.

## 60. Git evidence

Record repository identity, base commit, branch/worktree, changed paths, diff hash, generated files, tests, commit hash, remote-effect status, and cleanup.

Unknown remote effect blocks blind retry.

## 61. Path and link safety

Controls cover traversal, symlink and hard-link escape, bind-mount confusion, case differences, reserved paths, normalization, race conditions, and archive extraction traversal. Every resolved path must remain within an approved root.

## 62. Archive safety

Safe extraction enforces path normalization, symlink/hard-link policy, file-count limit, expanded-size limit, compression-ratio limit, nested-archive limit, active-content classification, and quarantine on violation.

## 63. Host filesystem boundary

Host root, home, container/runtime socket, arbitrary repositories, devices, and platform storage are denied by default. Any exceptional path requires explicit profile, policy, scope, mode, purpose, review, and evidence.

## 64. Network default deny

Network is disabled by default. When enabled, the specification lists destinations, protocols, ports, TLS, proxy, DNS behavior, classification, request-size limits, rate limits, and evidence requirements.

## 65. Network profiles

```text
none
control_plane_only
approved_internal_services
allowlisted_external_services
single_protected_destination
recovery_diagnostics
```

A standard unrestricted-internet profile is not approved.

## 66. DNS and metadata controls

Use approved resolvers, hostname allowlists, revalidate resolved addresses, prevent DNS rebinding, block link-local/private/metadata destinations unless explicitly required, and deny arbitrary custom DNS.

## 67. Controlled egress proxy

A proxy may identify sandbox/workspace, enforce destinations and TLS, limit rate and size, block prohibited classifications, and support emergency disablement. It should log safe metadata, not raw secrets or full sensitive payloads.

## 68. Inbound and peer communication

Inbound network and direct sandbox-to-sandbox communication are denied by default. Collaboration occurs through the control plane, artifact store, event system, or Tool Gateway.

## 69. Exfiltration controls

Controls include destination allowlists, classification checks, redaction, secret scanning, request-size limits, no raw sockets, no DNS tunneling, no arbitrary clipboard/browser channel, and approval/receipt for protected exports.

## 70. Secret architecture

Secrets are referenced rather than embedded in tasks, prompts, policies, logs, artifacts, or source. The Secret Broker validates identity, workspace, purpose, tool, destination, policy, approval, and expiry.

## 71. Secret access order

Preferred order:

```text
broker performs the operation
→ short-lived scoped credential
→ ephemeral handle/file
→ ephemeral environment variable only when unavoidable
```

Persistent plaintext secret files are prohibited.

## 72. Secret leases

A lease records reference, purpose, sandbox identity, workspace, tool/destination, issue and expiry, use constraints, revocation, and evidence reference. Raw values are excluded.

## 73. Secret redaction

Redaction covers stdout/stderr, commands, environment diagnostics, stack traces, tool errors, network metadata, artifacts, diffs, and support bundles. Redaction is defense-in-depth, not permission for broad exposure.

## 74. Tool Gateway

Protected capabilities go through the Tool Gateway, which verifies identity, attempt context, policy, approval, arguments, target, idempotency, rate/size limits, secret purpose, and evidence requirements before executing or delegating.

## 75. Tool classes

```text
pure computation
read-only data access
workspace-local mutation
repository mutation
artifact transformation
network read
external write
cost-bearing action
administrative action
recovery action
```

## 76. Tool schemas

Tools define structured inputs, outputs, errors, side-effect class, target, idempotency key, timeout, classification, approval fingerprint fields, and evidence fields.

Unknown fields and malformed targets are rejected.

## 77. Effect certainty

```text
not_started
confirmed_no_effect
effect_confirmed
effect_partially_confirmed
effect_unknown
reconciliation_required
```

Exit code zero, HTTP success, or adapter acknowledgement alone may not prove a protected effect.

## 78. Tool idempotency

Consequential calls use an idempotency key scoped to tool, action fingerprint, target, workspace, and attempt. Idempotency does not make an unknown first effect automatically safe to repeat.

## 79. Prompt-injection boundary

Repository text, web pages, artifacts, emails, tool output, model output, and memory are untrusted content. They cannot grant permission, reveal secrets, change workspace, enable network, alter profile, suppress evidence, approve, or redefine tool schemas.

## 80. Untrusted code and packages

Repository, generated, downloaded, and package code is untrusted until validated. Package installation requires approved registry, version pinning, integrity checks, network limits, lifecycle-script policy, scanning, lockfiles, and evidence.

## 81. Build and test hooks

Builds and tests may execute arbitrary scripts. Package lifecycle hooks, compiler plugins, Git hooks, code generators, browser plugins, and test plugins are explicitly governed. A label such as `test` does not make execution safe.

## 82. Browser automation

Browser sandboxes use an isolated profile, controlled downloads/uploads, destination allowlists, no human-cookie reuse, credential brokerage, screenshot classification, protocol restrictions, and cleanup.

## 83. Devices and accelerators

Device access is denied by default. GPU, camera, microphone, serial, USB, audio, and other devices require dedicated capabilities, isolation, quotas, and side-channel review.

## 84. Resource quotas

Specifications define CPU, memory, process count, open files, disk, inode/file count, write rate, network bandwidth/connections, wall timeout, idle timeout, output/log size, GPU resources, tool-call count, and secret-access count.

## 85. Resource-limit outcome

Limit events record the limit, observed use, termination behavior, partial output, cleanup, and effect certainty. Limit exceeded is not automatically a safe failure.

## 86. Admission control

Scheduling checks capacity, workspace quota, profile availability, required isolation features, resource estimate, budget, maintenance/recovery mode, Tool Gateway health, and executor identity before admission.

## 87. Leases and fencing

Only the current executor owner may operate a sandbox. Stale workers cannot call protected tools, extend secret leases, collect outputs, or mark cleanup complete.

## 88. Pause, resume, and checkpoints

Pause is allowed only when execution can be frozen safely and privileged channels suspended. Resume revalidates policy, identity, profile compatibility, approval, resources, and effect certainty.

Checkpoints never preserve expired authority, secret leases, approval consumption rights, or external effect certainty.

## 89. Timeout

Timeout triggers bounded termination, credential and network revocation, partial-output collection, cleanup, and reconciliation. It is not proof that an external request did not complete.

## 90. Output trust states

```text
untrusted_raw
validated
quarantined
rejected
proposed_artifact
accepted_artifact_version
```

Leaving the sandbox does not make content trusted.

## 91. Output validation and quarantine

Validation may include type, size, count, hash, malware, secret scan, archive safety, schema, syntax, tests, accessibility, classification, provenance, and active-content detection.

Quarantined content is not actively rendered, imported, or re-executed.

## 92. Artifact handoff

The sandbox proposes artifacts with content hash, type, size, generating attempt, profile, inputs, command/tool evidence, classification, validation, quarantine state, and provenance. Acceptance remains governed by `ART-001`.

## Logs and evidence package

Logs are bounded, structured where practical, timestamped, and linked to run, step, attempt, sandbox, and executor IDs. Logs are not the sole proof of protected effects and never contain raw secrets.

A sandbox evidence package may contain:

- immutable specification hash;
- profile/version;
- runtime image or environment digest;
- requesting and execution identities;
- mount manifest;
- network policy;
- resource limits;
- effective command or tool invocation;
- policy and approval references;
- secret-lease references;
- process start/stop;
- resource use;
- output hashes;
- validation results;
- violations;
- cleanup result;
- effect certainty;
- external receipts.

## Violation taxonomy

```text
filesystem_denied
path_escape_attempt
network_denied
dns_policy_violation
secret_access_denied
tool_not_authorized
argument_schema_violation
process_limit_exceeded
memory_limit_exceeded
disk_limit_exceeded
timeout
unexpected_output
malware_detected
cross_workspace_attempt
identity_mismatch
profile_integrity_mismatch
sandbox_escape_suspected
cleanup_incomplete
evidence_failure
```

## Violation response

Depending on severity, the platform denies the operation, records evidence, alerts, terminates the process or sandbox, revokes network and secrets, quarantines outputs, blocks the adapter/profile, quarantines the executor, activates emergency restrictions, declares an incident, or requires reconciliation.

A sandbox violation is never silently converted into an ordinary tool failure.

## Sandbox escape response

On suspected escape:

1. stop new scheduling on the affected executor/profile;
2. revoke workload and secret credentials;
3. isolate the executor host or node;
4. preserve volatile and durable evidence;
5. quarantine outputs;
6. identify affected runs and workspaces;
7. rotate potentially exposed credentials;
8. rebuild from trusted images;
9. complete incident and integrity review;
10. re-enable only after approval.

## Cross-workspace attempts

Any attempt to access another workspace is a critical security finding. The platform terminates or isolates the attempt, records safe evidence, invalidates affected leases/caches, investigates the source, and performs impact assessment.

## Evidence failure

If required evidence cannot be captured or persisted, protected execution should not begin. If evidence fails after start, the attempt transitions to an explicit noncompliant or unknown state, outputs remain untrusted, and operations are alerted.

Process success cannot override evidence failure.

## Cleanup failure

Cleanup failure creates a durable operational and security state. The executor is drained or quarantined until orphan processes, mounts, storage, credentials, network, and attempt state are verified.

## Executor trust and runtime images

Runtime environments should be minimal, reproducible, versioned, pinned by digest where supported, scanned, free from embedded secrets, tested against profiles, and retired through controlled lifecycle.

Future commercial profiles may add image signing, provenance, measured boot, or attestation direction. No specific attestation technology is mandated here.

## Supply-chain controls

Controls include trusted registries, pinned versions, SBOM generation, signatures/provenance direction, vulnerability and malware scanning, license review, isolated image builds, build-log evidence, emergency image revocation, and profile compatibility tests.

## Profile compatibility

A profile declares compatible executor types, operating systems, runtime images, capabilities, Tool Gateway versions, policy/obligation schemas, evidence collectors, and required isolation features.

Missing or incompatible features block scheduling.

## Local development profile

A local Linux/WSL development profile may use container-compatible isolation for practicality, but it must avoid broad host mounts, inherited credentials, unrestricted network, and autonomous Git push/merge.

The UI and evidence must explicitly state when local isolation is weaker than pilot or commercial expectations.

## Single-node pilot

A single-node pilot may place control plane and executors on one machine, but identities, processes, storage, network, secrets, and evidence boundaries remain explicit.

The pilot documentation must disclose that host compromise can affect multiple logical components.

## Shared pilot and commercial direction

Stronger deployments may separate the control plane, executor pools, artifact validation, secret broker, and network egress into independent trust zones with dedicated workload identities and customer- or risk-specific placement.

## Offline and air-gapped execution

Offline profiles deny external network, use pre-approved runtime images and package caches, broker local secrets, support signed artifact transfer, retain evidence locally, define controlled import/update workflows, and prohibit unverified removable-media execution.

## Multi-tenant direction

True multi-tenant execution requires validated isolation across identity, scheduler, filesystem, network, caches, logs, artifacts, secrets, executor placement, and evidence.

A workspace ID in application data is not by itself proof of tenant isolation.

## Adapter boundary

Adapters may submit capability and execution requirements, but cannot directly create sandboxes, broaden mounts, enable unrestricted network, obtain raw platform secrets, change profiles, bypass the Tool Gateway, approve execution, or declare effect certainty without evidence.

## Hermes adapter direction

Registered `ADP-HER-001` should map Hermes sessions, tools, memory access, model routes, network needs, and workspace operations to explicit profiles and Tool Gateway capabilities.

Claims of long autonomy or agent collaboration do not broaden sandbox permission.

## Codex adapter direction

Registered `ADP-CDX-001` should map repository selection, worktree creation, command execution, tests, diffs, commits, package access, and remote Git operations to explicit profiles and approvals.

Local modification does not imply push, pull-request creation, or merge authority.

## Policy integration

Registered `POL-001` may return mandatory obligations such as exact profile, read-only mounts, network allowlist, no secrets, specific secret reference, resource ceiling, output validation, approval, receipt, or quarantine.

The executor verifies every obligation is represented in the effective specification before start.

## IAM integration

Registered `IAM-001` supplies requesting human/service identity, adapter runtime identity, sandbox workload identity, support identity, and break-glass context.

Session or grant revocation blocks new privileged tool calls and may terminate or reconcile current execution according to policy.

## Approval integration

`APR-001` binds approval to material fields such as tool, target, command class, repository, branch, diff, destination, classification, network, secret purpose, profile, and cost.

Changing a material field invalidates the approval path.

## Run integration

`RUN-001` remains authoritative for attempts. Sandbox state is evidence used by the platform; the sandbox cannot mark the run complete directly.

Every retry receives a new attempt, specification, workload identity, leases, and evidence package.

## Artifact integration

`ART-001` governs proposal, validation, quarantine, review, acceptance, export, retention, and deletion. The sandbox only stages and proposes outputs.

## Observability integration

`OBS-001` consumes safe metrics and events for executor health, queue depth, preparation/start latency, resource use, network and secret denials, violations, cleanup, quarantine, evidence failures, and unknown effects.

Telemetry excludes raw secrets and unrestricted content.

## API direction

Potential resources:

```text
/sandbox-profiles
/sandbox-specifications
/sandbox-instances
/sandbox-leases
/sandbox-violations
/sandbox-evidence
/executor-pools
/network-policies
/secret-leases
/tool-bindings
```

## Command API direction

Potential commands:

```text
plan
prepare
start
pause
resume
cancel
terminate
collect
validate-outputs
cleanup
reconcile
quarantine-executor
release-executor
```

Clients cannot directly set lifecycle state or broaden the immutable specification.

## Event direction

Potential events:

```text
SandboxPlanned
SandboxPreparationStarted
SandboxPrepared
SandboxStarted
SandboxLimitApproaching
SandboxLimitExceeded
SandboxCancellationRequested
SandboxStopped
SandboxOutputCollected
SandboxOutputQuarantined
SandboxViolationDetected
SandboxEscapeSuspected
SandboxCleanupStarted
SandboxCleaned
SandboxCleanupFailed
SecretLeaseIssued
SecretLeaseRevoked
ToolCallProposed
ToolCallCompleted
ToolEffectUnknown
ExecutorQuarantined
```

## Data model direction

Core entities:

```text
SandboxProfile
SandboxProfileVersion
SandboxSpecification
SandboxInstance
SandboxLease
SandboxMount
SandboxNetworkRule
SandboxResourceLimit
SandboxSecretPlan
SandboxToolBinding
SandboxExecutionRecord
SandboxViolation
SandboxOutput
SandboxEvidencePackage
Executor
ExecutorPool
ExecutorQuarantine
SecretLease
ToolCall
```

## Executor operational states

```text
ready
degraded
draining
maintenance
quarantined
capacity_exhausted
unavailable
recovery
unknown
```

Admission and continuation behavior depend on the executor state and profile risk.

## Maintenance and draining

A draining executor accepts no new sandbox. Existing safe executions finish or are cancelled according to policy, leases cannot extend indefinitely, cleanup completes, health is verified, and maintenance evidence is recorded.

## Emergency stop

Emergency stop may block all new starts, selected profiles, a tool, network egress, secret leases, a workspace, or an executor pool.

Release requires current authority, reauthentication, reason, and executor/profile health validation.

## Backup and restore

Back up profile versions, policy mappings, executor configuration, image references, evidence references, and non-secret operational metadata.

Ephemeral sandboxes are normally not restored. After platform restore, old sessions and leases are invalid, executors re-register, profiles/images are verified, pending attempts are reconciled, and unknown external effects remain blocked.

## Recovery-only profile

Recovery execution may inspect evidence, validate backups, rebuild indexes, or reconcile state. It remains isolated, read-only where practical, explicitly governed, and unable to silently reactivate normal protected effects.

## Runbooks

Required runbooks include:

```text
prepare executor
drain executor
quarantine executor
investigate sandbox escape
investigate cross-workspace attempt
revoke secret leases
resolve cleanup failure
resolve output quarantine
rotate runtime image
update sandbox profile
restore executor pool
reconcile unknown tool effect
activate sandbox emergency stop
release sandbox emergency stop
```

## Monitoring

Monitor queue depth, executor capacity, preparation/start latency, duration, CPU, memory, disk, process count, output/log growth, network and secret denials, Tool Gateway latency, limit events, cleanup, orphan detection, quarantine, profile/image drift, executor identity, and evidence completeness.

## Alerts

Potential alerts:

```text
executor_unavailable
executor_identity_mismatch
sandbox_escape_suspected
cross_workspace_attempt
cleanup_failed
orphan_process_detected
secret_lease_not_revoked
network_policy_install_failed
profile_integrity_mismatch
runtime_image_revoked
output_quarantine_spike
evidence_capture_failed
capacity_exhausted
unknown_external_effect
```

## Security incidents

Critical incidents include sandbox escape, host compromise, cross-workspace access, raw secret exposure, Tool Gateway bypass, unapproved egress, unauthorized repository or external effect, evidence tampering, profile integrity failure, persistent orphan process, compromised image, or workload-identity theft.

## Test strategy

Testing layers:

```text
profile schema
planner unit/property
executor integration
filesystem isolation
network isolation
process/resource limits
secret broker
Tool Gateway
policy and approval integration
repository and Git
output validation
malware/quarantine
cancellation and timeout
leases and fencing
fault injection
escape simulation
cross-workspace
performance
accessibility and visual operations UI
backup/restore
adapter conformance
```

## Profile conformance tests

For every profile, test exact allowed and denied mounts, paths, commands, interpreters, processes, network destinations, secrets, tools, resources, outputs, and evidence. Positive tests alone are insufficient.

## Filesystem tests

Test path traversal, symlink and hard-link escape, bind mounts, archive traversal, races, case differences, device paths, host paths, other workspaces, and cleanup.

## Network tests

Test no-network mode, destination allowlists, ports, protocols, DNS rebinding, metadata/link-local access, proxy bypass, IPv4/IPv6, redirects, tunneling, inbound ports, and emergency shutdown.

## Secret tests

Test no-secret profiles, purpose binding, wrong workspace, wrong tool/destination, expiry, revocation, log redaction, crash output, artifact/diff scanning, broker outage, and cleanup.

## Resource tests

Test CPU, memory, process count, file descriptors, disk, inodes, output size, bandwidth, connection count, wall timeout, idle timeout, tool-call count, and concurrent admission.

## Cancellation and cleanup tests

Test graceful and forced stop, child/grandchild processes, background daemons, network calls in flight, secret revocation, partial output, unmounting, orphan detection, cleanup failure, and retry blocking.

## Tool Gateway tests

Test identity, policy, approval, schemas, target, idempotency, timeout, destination, secrets, receipts, certainty, adapter spoofing, replay, and direct-call bypass attempts.

## Repository and Git tests

Test exact repository/worktree, base commit, dirty state, path restrictions, local modification, staging, commit, prohibited push/PR/merge, remote URL changes, Git hooks, submodules, large files, symlink escape, and cleanup.

## Cross-workspace tests

For every mount, artifact, repository, cache, service, secret, tool, and log path:

1. create resources in workspace A;
2. run an attempt in workspace B;
3. attempt direct and indirect access;
4. verify denial and no metadata leakage;
5. repeat with symlinks, archives, forged IDs, and stale caches;
6. treat any access as critical.

## Fault-injection tests

Inject executor crash, control-plane disconnect, network-policy failure, Secret Broker failure, Tool Gateway timeout, disk full, evidence-store outage, cleanup failure, clock skew, lease expiry, duplicate command, and event loss.

The system must preserve explicit state and avoid blind retry.

## Escape-resistance tests

Security testing should cover known escape classes, privileged syscalls, device access, namespace/runtime misconfiguration, socket mounts, `/proc` and `/sys`, ptrace, setuid, mount operations, cloud metadata, and host-path discovery.

The exact penetration methodology requires Security approval.

## Performance and capacity direction

Measure preparation time, start latency, execution overhead, filesystem/network throughput, evidence overhead, cleanup time, concurrent capacity, queue fairness, and saturation behavior.

Formal targets remain in `NFR-001`.

## Accessibility and visual validation

Sandbox operations UI follows registered `A11Y-001` and `VVR-001`.

Required scenarios include profile selection, preparation, running, cancellation, limit warning, violation, quarantine, cleanup failure, executor drain, emergency stop, and unknown effect across supported widths and themes.

## MVP scope

Recommended MVP:

- profiles `SAN-P0` through `SAN-P3`;
- network denied by default;
- restricted network only for selected integrations;
- non-root execution;
- attempt-specific writable work area;
- read-only inputs;
- isolated repository worktree;
- bounded process/resource use;
- Tool Gateway for protected operations;
- secret references and short-lived leases;
- output staging and validation;
- cleanup and evidence;
- no autonomous Git push, PR, or merge;
- no production multi-tenant claim.

## Pilot readiness

Before pilot:

- enabled profiles pass positive and negative tests;
- cross-workspace tests pass;
- images are pinned and scanned;
- secret brokerage/redaction are tested;
- egress is allowlisted;
- Tool Gateway bypass is tested;
- Git boundaries are validated;
- cleanup and orphan detection work;
- emergency stop and executor quarantine are exercised;
- runbooks and evidence exist;
- no critical defect remains.

## Controlled-commercial direction

A controlled commercial profile may add stronger executor separation, dedicated trust zones, microVM/VM or equivalent isolation, workload attestation, signed profiles/images, customer-specific pools, advanced egress proxy, formal penetration tests, stronger forensics, and availability guarantees.

## Maturity stages

```text
S0 — no untrusted execution
S1 — local isolated computation and repository worktrees
S2 — Tool Gateway, Secret Broker, restricted network, pilot controls
S3 — stronger shared/commercial isolation and attestation
S4 — mature multi-tenant secure-execution platform
```

## Requirement catalogue — Profiles and isolation

- `SAN-REQ-ISO-001` — Every executable attempt uses an immutable sandbox specification.
- `SAN-REQ-ISO-002` — Sandbox profile selection is governed by policy.
- `SAN-REQ-ISO-003` — Agents and adapters cannot broaden their sandbox.
- `SAN-REQ-ISO-004` — Execution uses a unique attempt-scoped workload identity.
- `SAN-REQ-ISO-005` — Processes run without unnecessary privilege.
- `SAN-REQ-ISO-006` — Host filesystems, runtime sockets, devices, and host namespaces are denied by default.
- `SAN-REQ-ISO-007` — Workspace isolation is established before mounting inputs.
- `SAN-REQ-ISO-008` — Material privilege changes require a new specification and re-evaluation.
- `SAN-REQ-ISO-009` — Profile and runtime integrity are verified before start.
- `SAN-REQ-ISO-010` — Unknown profile or executor state blocks protected execution.
- `SAN-REQ-ISO-011` — Every profile has positive and negative conformance tests.
- `SAN-REQ-ISO-012` — Commercial multi-tenant claims require validated isolation evidence.

## Requirement catalogue — Filesystem, network, and secrets

- `SAN-REQ-BND-001` — Inputs are read-only and version-bound.
- `SAN-REQ-BND-002` — Writes are restricted to declared attempt-scoped roots.
- `SAN-REQ-BND-003` — Path traversal, link, archive, and mount escape are controlled.
- `SAN-REQ-BND-004` — Network is denied by default.
- `SAN-REQ-BND-005` — Allowed destinations, protocols, and ports are explicit.
- `SAN-REQ-BND-006` — Cloud metadata and link-local targets are blocked by default.
- `SAN-REQ-BND-007` — Inbound and peer-sandbox network are denied by default.
- `SAN-REQ-BND-008` — Secrets use references and purpose-bound leases.
- `SAN-REQ-BND-009` — Raw secrets are excluded from prompts, logs, diffs, artifacts, and evidence.
- `SAN-REQ-BND-010` — Secret leases are short-lived and revocable.
- `SAN-REQ-BND-011` — Cross-workspace files, services, secrets, and caches are prohibited.
- `SAN-REQ-BND-012` — Output collection is limited to declared paths.

## Requirement catalogue — Tools, effects, and artifacts

- `SAN-REQ-EFF-001` — Protected tools are mediated by the Tool Gateway.
- `SAN-REQ-EFF-002` — Tool inputs and outputs use controlled schemas.
- `SAN-REQ-EFF-003` — Policy and approval are revalidated before protected effects.
- `SAN-REQ-EFF-004` — Consequential tools use idempotency controls.
- `SAN-REQ-EFF-005` — Effect certainty is explicit.
- `SAN-REQ-EFF-006` — Unknown effects block blind retry.
- `SAN-REQ-EFF-007` — Cancellation is not represented as rollback.
- `SAN-REQ-EFF-008` — Sandbox outputs remain untrusted until validated.
- `SAN-REQ-EFF-009` — Quarantined output is not actively rendered or executed.
- `SAN-REQ-EFF-010` — Artifact acceptance remains outside the sandbox.
- `SAN-REQ-EFF-011` — Repository modification does not imply remote Git authority.
- `SAN-REQ-EFF-012` — Evidence failure prevents trusted completion.

## Requirement catalogue — Operations and quality

- `SAN-REQ-OPS-001` — Resource limits are explicit and enforced.
- `SAN-REQ-OPS-002` — Cleanup terminates processes, revokes leases, removes network, and releases mounts.
- `SAN-REQ-OPS-003` — Cleanup failure quarantines or drains the executor.
- `SAN-REQ-OPS-004` — Escape suspicion triggers incident containment.
- `SAN-REQ-OPS-005` — Cross-workspace attempts are critical incidents.
- `SAN-REQ-OPS-006` — Executor and profile health are observable.
- `SAN-REQ-OPS-007` — Emergency stop can block execution and privileged channels.
- `SAN-REQ-OPS-008` — Restored sessions and secret leases are invalid.
- `SAN-REQ-OPS-009` — Pending attempts are reconciled after restore.
- `SAN-REQ-OPS-010` — Critical paths receive fault-injection and abuse tests.
- `SAN-REQ-OPS-011` — Operations UI is accessible and visually validated.
- `SAN-REQ-OPS-012` — Critical sandbox findings block pilot and release.

## Traceability

| Source | SAN-001 response |
|---|---|
| `SAD-001` | Sandbox Executor, Tool Gateway, adapters, stores, and trust boundaries |
| `SEC-001` | Least privilege, secret handling, network controls, and isolation |
| `THR-001` | Escape, exfiltration, prompt injection, confused deputy, and supply chain |
| `AGC-001` | Adapter boundary, tool proposals, cancellation, and evidence |
| `CAP-001` | Capability effects, resource, network, filesystem, and secret declarations |
| `RUN-001` | Attempt lifecycle, leases, cancellation, retries, and unknown effects |
| `APR-001` | Exact approval fingerprint and consumption |
| `ART-001` | Staging, validation, quarantine, and artifact acceptance |
| `POL-001` | Profiles, obligations, default deny, and emergency restrictions |
| `DAT-001` | Workspace-scoped data and storage |
| `API-001` | Secure-execution resources and commands |
| `EVT-001` | Sandbox lifecycle, tool, and violation events |
| `OBS-001` | Executor, resource, violation, and cleanup observability |
| `DEP-001` | Executor placement, runtime images, networks, and environments |
| `OPS-001` | Runbooks, incidents, maintenance, and emergency stop |
| `BCP-001` | Recovery-only execution and post-restore reconciliation |
| `PLG-001` | Extension runtime, permissions, capabilities, and trust |

## ADR-CANDIDATE-SAN-001 — Isolation technology and trust model

Select container, namespace, microVM, VM, or layered isolation for local, pilot, and commercial profiles.

## ADR-CANDIDATE-SAN-002 — Sandbox profile schema and planner

Define profile language, inheritance, materialization, validation, compatibility, signing, and versioning.

## ADR-CANDIDATE-SAN-003 — Filesystem, repository, and artifact staging

Select worktree/snapshot approach, mounts, writable roots, archive handling, output collection, and cleanup.

## ADR-CANDIDATE-SAN-004 — Network egress and destination enforcement

Define no-network defaults, proxy, DNS, allowlists, TLS, metadata blocking, receipts, and emergency shutdown.

## ADR-CANDIDATE-SAN-005 — Secret brokerage and workload identity

Define secret references, short-lived credentials, leases, redaction, rotation, executor identity, and compromise response.

## ADR-CANDIDATE-SAN-006 — Tool Gateway and effect-certainty contract

Define schemas, policy/approval revalidation, idempotency, receipts, certainty states, and reconciliation.

## ADR-CANDIDATE-SAN-007 — Resource control, scheduling, cancellation, and cleanup

Define quotas, leases, fencing, pause/resume, timeouts, orphan detection, and executor quarantine.

## ADR-CANDIDATE-SAN-008 — Runtime supply chain, evidence, and commercial hardening

Define image builds, SBOM, signatures, scanning, attestation direction, penetration tests, retention, and multi-tenant claims.

## Open decisions

1. Confirm `SAN-001` registration.
2. Select isolation technologies for local, pilot, and commercial profiles.
3. Approve profile taxonomy and names.
4. Define the immutable profile/specification schema.
5. Define repository worktree or snapshot strategy.
6. Define path, link, archive, and mount protections.
7. Select egress proxy and DNS enforcement direction.
8. Define network destination and TLS evidence.
9. Define workload identity and executor registration.
10. Define Secret Broker and lease mechanisms.
11. Define environment-variable fallback restrictions.
12. Define Tool Gateway deployment and trust boundary.
13. Approve effect-certainty vocabulary.
14. Define resource and timeout defaults.
15. Define cancellation grace and forced cleanup.
16. Define pause, resume, and checkpoint support.
17. Define runtime-image build, scanning, signing, and revocation.
18. Define executor quarantine and trusted rebuild.
19. Define commercial isolation and attestation targets.
20. Define offline package and image import.
21. Define evidence package and retention.
22. Confirm Hermes and Codex profile mappings.
23. Confirm accessibility and visual scenarios.
24. Define sandbox exceptions and expiry.
25. Align `SEC-002`, `DAT-002`, `AUD-001`, `CST-001`, `ADP-HER-001`, and `ADP-CDX-001`.

## Risks

| Risk | Consequence | Response |
|---|---|---|
| Container treated as perfect boundary | Host compromise | Layered trust model |
| Broad host mount | Data/control-plane compromise | Explicit roots |
| Runtime socket exposed | Full host control | Prohibited mount |
| Network enabled by default | Exfiltration | Default deny |
| DNS rebinding | Allowlist bypass | Resolution controls |
| Metadata endpoint reachable | Credential theft | Link-local blocking |
| Raw secret in environment | Log/artifact leakage | Secret Broker |
| Prompt changes profile | Policy bypass | Control-plane authority |
| Tool bypasses gateway | Untracked side effect | Network/API isolation |
| Local Git permission implies push | Unauthorized remote effect | Separate capabilities |
| Exit zero but effect unknown | False success or duplicate retry | Effect certainty |
| Cancellation assumed rollback | External effect persists | Reconciliation |
| Output trusted immediately | Malware or secret propagation | Validation/quarantine |
| Cleanup leaves daemon | Persistent compromise | Orphan detection |
| Stale worker continues | Duplicate effects | Lease and fencing |
| Resource exhaustion | Platform outage | Quotas and admission |
| Package hooks execute code | Supply-chain compromise | Controlled registries/scripts |
| Cross-workspace mount/cache | Data leak | Attempt scoping and tests |
| Weak local profile treated as commercial | False assurance | Explicit profile limitations |
| Evidence captures secrets | Secondary exposure | Redaction and minimization |
| Architecture too complex for MVP | Delivery delay | Maturity stages |

## Assumptions

- The control plane can persist an immutable sandbox specification.
- Executors can use distinct workload identities.
- Workspace-scoped inputs, repositories, and artifacts can be staged.
- Policy and approval can be revalidated before Tool Gateway effects.
- Process/resource controls and cleanup are available in the selected runtime.
- Network and secrets can be mediated.
- Repository work can use isolated worktrees or snapshots.
- Evidence and output validation execute outside the sandbox.
- Local development may begin with weaker isolation and explicit warnings.
- Stronger commercial isolation can be introduced without changing the execution contract.

## Constraints

- no unrestricted host shell;
- no host root, home, runtime socket, device, or platform database access by default;
- no unrestricted internet;
- no cross-workspace mount, cache, secret, service, log, or artifact access;
- no raw secret in prompts, logs, source, artifacts, diffs, or evidence;
- no agent or adapter sandbox self-upgrade;
- no protected tool outside the Tool Gateway without equivalent approved controls;
- no output promoted directly to accepted artifact;
- no blind retry after unknown effect;
- no successful-completion claim when required evidence or cleanup failed;
- no production multi-tenant assurance claim without validation;
- no final sandbox technology selected in this draft;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## Acceptance criteria

SAN-001 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts execution, approval, artifact, recovery, and limitation behavior;
3. Architecture accepts planner, executor, Tool Gateway, Secret Broker, staging, and trust boundaries;
4. Security accepts filesystem, network, process, secret, supply-chain, violation, and escape controls;
5. Data accepts workspace isolation, classification, output staging, retention, and deletion implications;
6. Operations accepts executor lifecycle, capacity, maintenance, quarantine, incidents, and recovery runbooks;
7. Quality accepts profile conformance, cross-workspace, abuse, fault-injection, cleanup, evidence, and release gates;
8. profile taxonomy and specification schema are approved;
9. local, pilot, and commercial isolation directions are approved;
10. Tool Gateway and effect-certainty contracts are approved;
11. Secret Broker and workload identity are approved;
12. network and filesystem controls are approved;
13. runtime supply-chain controls are approved;
14. evidence, cleanup, and reconciliation are approved;
15. downstream adapter and control documents can refine implementation without changing these invariants.

## Downstream impact

| Document | Required use |
|---|---|
| `SEC-002` | Sandbox, network, secret, runtime, supply-chain, and response controls |
| `DAT-002` | Input/output classification, ephemeral retention, quarantine, and deletion |
| `AUD-001` | Specification, tool, violation, cleanup, and effect evidence |
| `CST-001` | Compute, model, network, storage, quota, and budget accounting |
| `ADP-HER-001` | Hermes runtime, tools, memory, network, and workspace mappings |
| `ADP-CDX-001` | Codex repository, commands, tests, packages, diffs, and Git mappings |
| `UXA-001` | Execution, limit, violation, cancellation, and recovery journeys |
| `DSN-001` | Sandbox state, violation, resource, and emergency components |
| `A11Y-001` | Accessible execution and recovery controls |
| `VVR-001` | Lifecycle, violation, quarantine, and executor visual scenarios |
| Document register | Add proposed document and dependencies |

## Revision and approval history

### Approval state

- Current status: `approved`
- Current version: `0.1.0`
- Approved by: Product Owner under explicit user authorization to finalize the declared scope
- Finalization note: approval records the documentation baseline only; implementation and verification remain separate evidence gates

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial sandbox and secure-execution architecture covering profiles, process/filesystem/network/secret boundaries, Tool Gateway, repositories, resource controls, outputs, quarantine, evidence, violations, cleanup, recovery, deployment profiles, testing, and adapter integration |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SAD-001` — System Architecture Description
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `AGC-001` — Agent Adapter Contract
- `CAP-001` — Agent Capability Schema
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `POL-001` — Policy and Permission Architecture — registered
- `API-001` — API Specification
- `EVT-001` — Event Catalog and Async Contract
- `OBS-001` — Observability Architecture
- `DEP-001` — Deployment Architecture and Environment Strategy
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
- `PLG-001` — Plugin and Extension Architecture
