---
document_id: PLG-001
title: Agent OS Plugin and Extension Architecture
version: 0.2.0
status: draft
priority: P1
owner: architecture-owner
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
dependencies:
  - SAD-001
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
related_adrs:
  - ADR-TBD-PLG-001
  - ADR-TBD-PLG-002
  - ADR-TBD-PLG-003
  - ADR-TBD-PLG-004
  - ADR-TBD-PLG-005
  - ADR-TBD-PLG-006
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# PLG-001 — Agent OS Plugin and Extension Architecture

> **Status: Draft — Priority P1.** This document defines the future plugin and extension architecture for Agent OS. It covers extension types, manifests, capability declaration, installation, validation, trust, signing, permissions, sandboxing, lifecycle, compatibility, configuration, secrets, data access, UI extensions, API/event extensions, MCP integration direction, skills, adapters, governance, operations, testing, marketplace direction, revocation, uninstall, backup, restore, and vendor exit. It does not authorize dynamic third-party code execution in the MVP, define a public marketplace, select a package format, approve MCP as an authentication mechanism, or allow plugins to bypass Agent OS policy, approval, workspace isolation, audit, or security controls.

## 1. Purpose

Agent OS is intended to become extensible without becoming uncontrollable.

Extensions may eventually provide:

- new agent adapters;
- new model providers;
- new tools;
- new MCP servers or MCP bridges;
- new skills;
- new artifact processors;
- new memory sources;
- new integrations;
- new UI panels;
- new workflow templates;
- new notification channels;
- new policy data sources;
- new observability exporters;
- new backup/storage implementations.

The extension architecture must allow these capabilities while preserving:

1. provider neutrality;
2. control-plane authority;
3. workspace isolation;
4. least privilege;
5. explicit permissions;
6. human approval;
7. capability validation;
8. sandboxing;
9. data classification;
10. provenance;
11. auditability;
12. disablement and revocation;
13. compatibility;
14. operational recovery;
15. safe uninstall and exit.

## 2. Objectives

The plugin architecture must:

- define stable extension points;
- distinguish code, configuration, content, and remote integrations;
- make capabilities explicit;
- make permissions explicit;
- make data access explicit;
- make network and filesystem access explicit;
- support installation review;
- support signature and provenance verification;
- support compatibility checks;
- support workspace-specific enablement;
- support runtime health and readiness;
- support revocation;
- support upgrade and rollback;
- support backup and restore;
- support operational isolation;
- prevent extension-based policy bypass;
- prevent extension-based approval bypass;
- prevent hidden native-tool execution;
- prevent secrets from becoming plugin-owned plaintext;
- keep MVP extensibility bounded and conservative.

## 3. Non-goals

This document does not:

- mandate a plugin system in the first MVP;
- authorize arbitrary third-party code;
- authorize runtime package installation from the public internet;
- authorize auto-update without review;
- define a public marketplace;
- define a revenue-sharing model;
- guarantee binary compatibility;
- treat MCP servers as trusted by default;
- treat a signed package as safe;
- allow plugins to approve actions;
- allow plugins to grant themselves capabilities;
- allow plugins to access all workspaces;
- allow plugins to receive raw secrets by default;
- allow plugins to mutate core lifecycle states directly;
- allow plugins to bypass the Tool Gateway;
- allow plugins to merge Git branches or perform prohibited actions.

## 4. Core principles

### `PLG-P-001 — Extension is not authority`

A plugin can propose, transform, observe, or execute within granted scope. It cannot become the authority for platform state, policy, approval, or workspace ownership.

### `PLG-P-002 — Capability before execution`

Every executable extension declares capabilities and passes validation before enablement.

### `PLG-P-003 — Installation is not enablement`

A package may be installed but disabled, quarantined, incompatible, revoked, or awaiting review.

### `PLG-P-004 — Enablement is not authorization`

Workspace enablement does not imply that every user, run, or action is authorized.

### `PLG-P-005 — Authorization is not approval`

An allowed capability may still require exact human approval for a consequential action.

### `PLG-P-006 — Signing is provenance, not safety`

A valid signature proves package origin and integrity under a trust model. It does not prove absence of vulnerabilities or malicious behavior.

### `PLG-P-007 — Default deny`

Undeclared filesystem, network, secret, data, UI, event, and tool access is denied.

### `PLG-P-008 — Extension boundaries are observable`

Health, readiness, calls, failures, permissions, data access, version, and drift are visible.

### `PLG-P-009 — Remote integrations are also extensions`

A remote MCP server, provider API, webhook service, or SaaS connector is not safer merely because its code runs elsewhere.

### `PLG-P-010 — Uninstall does not erase history`

Disabling or removing an extension does not delete audit, receipts, artifacts, provenance, decisions, or historical capability records.

### `PLG-P-011 — Unknown behavior blocks protected use`

If tool visibility, side-effect semantics, cancellation, or data handling is unknown, protected workflows remain blocked.

### `PLG-P-012 — The core remains useful without optional plugins`

Core Agent OS functionality must not depend on an ungoverned extension ecosystem.

## 5. Extension taxonomy

Agent OS distinguishes:

```text
adapter_extension
model_provider_extension
tool_extension
mcp_extension
skill_extension
workflow_template_extension
artifact_processor_extension
memory_connector_extension
integration_extension
notification_extension
ui_extension
observability_extension
storage_extension
policy_data_extension
authentication_extension
```

Not every extension type is permitted in every product stage.

## 6. Adapter extension

Provides a bridge to an agent runtime.

Examples:

- Hermes adapter;
- Codex adapter;
- future local agent runtime.

Governed primarily by `AGC-001` and `CAP-001`.

## 7. Model-provider extension

Provides:

- provider bindings;
- model metadata;
- invocation;
- usage observations;
- identity observations;
- error normalization.

Governed by `MOD-001`, `INT-001`, `SEC-001`, and cost controls.

## 8. Tool extension

Provides a bounded action through the Tool Gateway.

Examples:

- filesystem operation;
- Git operation;
- issue tracker operation;
- messaging;
- calendar;
- document conversion;
- code analysis.

A tool extension never receives authority to bypass the Tool Gateway.

## 9. MCP extension

Represents:

- an MCP server;
- an MCP client bridge;
- an MCP capability catalogue;
- an MCP tool/resource/prompt mapping.

MCP is a transport and capability protocol, not an authorization or trust system.

## 10. Skill extension

Provides reusable instructions, prompts, recipes, or orchestrated procedures.

A skill may contain:

- human-readable guidance;
- structured parameters;
- capability dependencies;
- safety constraints;
- expected outputs;
- evaluation criteria.

A skill is content, not automatically executable authority.

## 11. Workflow-template extension

Provides a reusable graph or mission template.

It may define:

- tasks;
- dependencies;
- checkpoints;
- approvals;
- expected artifacts;
- recovery rules.

Instantiation creates governed platform objects.

## 12. Artifact-processor extension

Processes artifacts for:

- validation;
- preview;
- conversion;
- extraction;
- classification support;
- redaction;
- indexing.

It must treat content as untrusted.

## 13. Memory-connector extension

Provides access to:

- document repositories;
- knowledge bases;
- source systems;
- structured datasets.

It must preserve source, authority, classification, and deletion semantics.

## 14. Integration extension

Connects a business or engineering system.

Examples:

- Git hosting;
- issue tracker;
- storage provider;
- email;
- calendar;
- CRM;
- document system.

## 15. Notification extension

Delivers notifications through:

- local UI;
- email;
- messaging platform;
- webhook;
- mobile push.

Delivery does not replace authoritative platform state.

## 16. UI extension

Adds bounded user-interface surfaces.

Examples:

- dashboard panel;
- artifact viewer;
- configuration panel;
- run detail section;
- workspace tool page.

UI extensions cannot bypass backend authorization.

## 17. Observability extension

Exports or visualizes:

- logs;
- metrics;
- traces;
- alerts;
- diagnostics.

It must obey telemetry classification and export policy.

## 18. Storage extension

Implements:

- artifact content storage;
- backup destination;
- index store;
- cache.

Storage extensions are high-risk and require strong validation.

## 19. Policy-data extension

Provides attributes or external data used by policy evaluation.

It does not make the final authorization decision.

## 20. Authentication extension

Provides identity federation or authentication mechanisms.

This is a critical extension class and is not recommended for early dynamic plugin support.

## 21. Extension execution models

```text
declarative_content
in_process_module
separate_local_process
isolated_container
remote_service
mcp_server
managed_platform_service
```

## 22. Declarative content

Examples:

- skill;
- workflow template;
- UI schema;
- policy-data mapping;
- static capability metadata.

Lowest code-execution risk, but content may still contain prompt injection or misleading instructions.

## 23. In-process module

Runs inside a core process.

Advantages:

- low latency;
- simple invocation.

Risks:

- memory and privilege sharing;
- crash impact;
- dependency conflicts;
- weak isolation.

Not recommended for untrusted third-party plugins.

## 24. Separate local process

Uses:

- IPC;
- HTTP over loopback;
- Unix socket;
- standard streams with framed protocol.

Provides stronger process isolation and independent lifecycle.

## 25. Isolated container

Provides:

- dependency isolation;
- resource limits;
- filesystem/network profiles;
- independent deployment.

Still not a complete security sandbox.

## 26. Remote service

Runs outside Agent OS.

Risks include:

- data disclosure;
- external retention;
- provider identity;
- availability;
- unobservable internal behavior;
- jurisdiction;
- vendor exit.

## 27. MCP server

May be local or remote.

Agent OS must separately govern:

- server identity;
- transport;
- tools;
- resources;
- prompts;
- roots;
- notifications;
- capability drift;
- data disclosure;
- authentication;
- authorization;
- approval.

## 28. Managed platform service

A future hosted extension service may provide:

- package registry;
- validation;
- distribution;
- telemetry;
- revocation.

It remains outside the local MVP.

## 29. Trust classes

Proposed trust classes:

```text
T0_core
T1_first_party
T2_reviewed_partner
T3_reviewed_third_party
T4_local_unverified
T5_remote_unverified
T6_revoked
```

## 30. T0 core

Built and versioned with the Agent OS core.

Still tested and governed.

## 31. T1 first-party

Developed by the Agent OS project but deployed separately.

Examples:

- official Hermes adapter;
- official Codex adapter.

## 32. T2 reviewed partner

Developed by a named partner and passed contractual and technical review.

## 33. T3 reviewed third-party

Third-party extension that passes defined validation but has no privileged trust by default.

## 34. T4 local unverified

Manually installed local extension with unknown or incomplete provenance.

Permitted only in development/security-test profiles by default.

## 35. T5 remote unverified

Remote extension or MCP server without completed validation.

Protected use is blocked.

## 36. T6 revoked

Known unsafe, compromised, unsupported, expired, or administratively revoked.

Cannot be enabled or invoked.

## 37. Trust does not equal permission

A first-party extension may still receive narrow permissions.

A third-party extension may be installed but disabled.

## 38. Lifecycle states

```text
discovered
submitted
staged
scanning
under_review
validated
installed
disabled
enabled
degraded
incompatible
quarantined
suspended
revoked
upgrade_pending
uninstall_pending
uninstalled
retired
unknown
```

## 39. Discovered

Metadata or package reference found, not yet imported.

## 40. Submitted

Package or remote endpoint proposed for review.

## 41. Staged

Stored in an isolated staging area.

No runtime enablement.

## 42. Scanning

Static, dependency, malware, secret, schema, and provenance checks are running.

## 43. Under review

Human and automated review is incomplete.

## 44. Validated

Passed the required validation profile.

Validation has version, evidence, scope, and expiry.

## 45. Installed

Package/runtime is present but not necessarily enabled.

## 46. Disabled

Not callable by ordinary workflows.

Historical records remain.

## 47. Enabled

May be considered for routing within workspace and policy scope.

## 48. Degraded

Available with explicit limitations.

## 49. Incompatible

Does not satisfy current core, protocol, schema, runtime, or dependency requirements.

## 50. Quarantined

Blocked pending security or integrity investigation.

## 51. Suspended

Temporarily disabled operationally.

## 52. Revoked

Explicitly prohibited.

## 53. Upgrade pending

A new version is staged or awaiting approval.

## 54. Uninstall pending

Disablement and dependency checks are complete or in progress.

## 55. Uninstalled

Runtime/package removed, historical records retained.

## 56. Retired

No longer supported or distributed.

## 57. Unknown

Current state cannot be verified.

Protected use is blocked.

## 58. Plugin identity

Every extension has:

- extension ID;
- canonical name;
- publisher;
- extension type;
- version;
- package digest or endpoint identity;
- manifest version;
- trust class;
- validation profile;
- lifecycle state;
- owner;
- support status.

## 59. Extension ID

Opaque and stable.

Package name is not authority.

## 60. Version identity

Distinguish:

```text
declared_version
package_version
runtime_reported_version
protocol_version
manifest_version
validation_version
```

Conflicts are explicit.

## 61. Publisher identity

May include:

- organization;
- signing identity;
- repository/source;
- contact;
- trust relationship;
- revocation status.

## 62. Package digest

A cryptographic content digest identifies the exact reviewed package.

A version label alone is insufficient.

## 63. Endpoint identity

For remote services:

- canonical endpoint;
- certificate identity;
- service identity;
- protocol version;
- metadata hash;
- region;
- owner.

## 64. Manifest

Every extension has a machine-readable manifest.

The manifest is declarative and schema-validated.

## 65. Manifest minimum fields

```text
manifest_version
extension_id
name
version
publisher
extension_type
entrypoint_or_endpoint
package_digest
required_core_version
protocol_versions
capabilities
permissions
data_access
network_access
filesystem_access
secret_references
configuration_schema
events
api_extensions
ui_extensions
health
readiness
update_policy
uninstall_behavior
support
license
```

## 66. Manifest example

```yaml
manifest_version: "1"
extension_id: "ext_example"
name: "Example Read-Only Repository Inspector"
version: "0.1.0"
publisher:
  name: "Example Publisher"
extension_type: "tool_extension"
execution_model: "isolated_container"
required_core_version: ">=0.1,<0.2"
capabilities:
  - code: "repository.inspect"
    effect_class: "read_only"
permissions:
  filesystem:
    read:
      - "workspace_repository"
    write: []
  network:
    destinations: []
  secrets: []
data_access:
  maximum_classification: "internal"
health:
  endpoint: "/health"
readiness:
  endpoint: "/ready"
```

## 67. Manifest authority

The manifest is a declaration.

Actual package/runtime behavior must be validated.

## 68. Manifest immutability

A published package digest maps to one immutable manifest.

Material manifest change creates a new version/digest.

## 69. Manifest extensions

Unknown vendor fields must use a namespaced extension section.

Core security fields cannot be overridden by vendor extensions.

## 70. Capability declaration

Capabilities follow `CAP-001`.

Each capability includes:

- code;
- description;
- effect class;
- risk class;
- target types;
- inputs;
- outputs;
- data classifications;
- operational semantics;
- cancellation;
- idempotency;
- evidence;
- dependencies.

## 71. Capability states

```text
declared
schema_valid
tested
validated
enabled
ready
authorized
approval_required
invoked
observed
revoked
```

These states are not collapsed.

## 72. Capability drift

Drift occurs when runtime behavior differs from the validated declaration.

Examples:

- new tool appears;
- filesystem access expands;
- endpoint changes;
- cancellation semantics change;
- new data retention;
- model/provider changes;
- output schema changes.

## 73. Drift response

- mark capability not ready;
- block protected use;
- record drift;
- suspend extension if material;
- rerun validation;
- update manifest/version;
- require re-enable decision.

## 74. Permission model

Extension permissions are separated into:

```text
platform_api
workspace_data
filesystem
network
secrets
tools
events
ui
artifact
memory
identity
operations
```

## 75. Platform API permissions

Examples:

- read run summary;
- create artifact proposal;
- query own extension state;
- publish bounded event;
- request tool action.

No generic unrestricted database/API access.

## 76. Workspace-data permissions

Specify:

- workspace scope;
- entity types;
- read/write;
- field subset;
- classification ceiling;
- purpose;
- retention.

## 77. Filesystem permissions

Specify:

- roots;
- read/write/delete;
- path patterns;
- symlink handling;
- temporary storage;
- maximum bytes;
- workspace binding.

## 78. Network permissions

Specify:

- destination;
- port/protocol;
- DNS/redirect behavior;
- TLS requirements;
- data classification;
- request limits;
- purpose.

## 79. Secret permissions

Specify:

- secret reference;
- purpose;
- component;
- workspace;
- duration;
- provider/account.

Raw secret values are not exposed to the control plane or plugin configuration UI.

## 80. Tool permissions

An extension may request access to Tool Gateway capabilities.

It does not receive direct executor authority unless it is itself the isolated tool implementation.

## 81. Event permissions

Specify:

- event types consumed;
- event types proposed/published;
- workspace;
- classification;
- replay behavior;
- ordering;
- rate.

## 82. UI permissions

Specify:

- extension points;
- routes;
- panels;
- actions;
- data requirements;
- content security;
- accessibility obligations.

## 83. Artifact permissions

Specify:

- propose;
- read metadata;
- read content;
- create preview;
- validate;
- export;
- delete.

Acceptance remains governed by core policy.

## 84. Memory permissions

Specify:

- propose memory;
- query;
- source types;
- authority ceiling;
- classification;
- retention;
- deletion.

An extension cannot self-verify its generated memory as authoritative.

## 85. Identity permissions

Highly restricted.

Examples:

- read current actor summary;
- validate external identity mapping.

An extension cannot assign platform roles.

## 86. Operations permissions

Highly restricted.

Examples:

- report health;
- request restart;
- produce diagnostics.

Extensions cannot autonomously deploy, restore, release emergency stop, or mutate core configuration.

## 87. Permission profiles

Proposed profiles:

```text
profile_declarative
profile_read_only
profile_artifact_processor
profile_memory_connector
profile_tool_low_risk
profile_tool_protected
profile_adapter
profile_observability_exporter
profile_storage_backend
profile_identity_critical
```

## 88. Least-privilege review

Every requested permission must have:

- capability dependency;
- purpose;
- risk;
- data class;
- validation;
- owner;
- expiry or review.

## 89. Permission escalation

A new version requesting broader permissions is a material upgrade.

It cannot inherit prior approval automatically.

## 90. Workspace enablement

An installed extension may be:

- globally disabled;
- enabled for selected workspaces;
- enabled for selected capabilities;
- enabled with policy restrictions;
- enabled for development only.

## 91. Workspace isolation

Extension runtime must not:

- infer another workspace;
- reuse cross-workspace cache;
- share unscoped credentials;
- write global mutable state with workspace data;
- expose aggregate counts without authority.

## 92. Multi-workspace runtime models

Options:

```text
shared_process_with_strict_scope
per_workspace_process
per_run_process
per_task_sandbox
remote_multi_tenant_service
```

Higher-risk extensions may require stronger isolation.

## 93. Data classification

Each extension declares:

- maximum input classification;
- maximum output classification;
- external disclosure;
- retention;
- training/use policy;
- region;
- subprocessors where remote.

## 94. Classification inheritance

Extension outputs inherit the maximum classification of:

- inputs;
- source data;
- generated content sensitivity;
- policy result.

## 95. Data minimization

Extensions receive only fields needed for the capability.

Avoid passing full task, run, artifact, or memory records unnecessarily.

## 96. Data retention

An extension declares whether it:

- does not retain;
- retains transiently;
- retains operational metadata;
- retains content;
- relies on remote provider retention.

Unknown retention blocks sensitive use.

## 97. Data deletion

Extensions with retained data must support:

- deletion request;
- tombstone/reference;
- confirmation;
- limitations;
- external copy disclosure.

## 98. Data export

External data transfer requires:

- destination;
- purpose;
- classification;
- approval where required;
- receipt;
- external copy limitation.

## 99. Secret handling

Plugin packages and manifests must not contain production secrets.

Secret values are resolved through governed secret infrastructure.

## 100. Secret injection models

Potential models:

```text
short_lived_environment
mounted_secret_file
brokered_request
sidecar_proxy
workload_identity
```

Final models require ADR.

## 101. Brokered secret use

Preferred for high-risk remote operations:

- plugin requests operation;
- trusted gateway uses secret;
- plugin receives result, not secret.

## 102. Secret leakage response

- revoke extension capability;
- rotate secret;
- quarantine extension/version;
- preserve evidence;
- inspect outputs/logs/events;
- security incident;
- invalidate validation.

## 103. Installation pipeline

```text
discover or submit
→ retrieve/import
→ verify digest
→ verify provenance/signature
→ parse manifest
→ static scan
→ dependency scan
→ malware/secret scan
→ permission analysis
→ compatibility analysis
→ sandbox test
→ contract/conformance test
→ human review
→ validation record
→ install disabled
```

## 104. Installation sources

Potential:

- first-party repository;
- approved registry;
- local package file;
- partner repository;
- remote service registration;
- MCP endpoint registration.

Public arbitrary install is disabled by default.

## 105. Source allowlist

Installation policy may allow only:

- first-party;
- reviewed partner;
- approved registry;
- local development source.

## 106. Package staging

Packages are staged outside runtime paths.

No execution during metadata inspection unless isolated.

## 107. Archive safety

Package extraction must prevent:

- path traversal;
- symlink escape;
- decompression bomb;
- device files;
- permission abuse;
- hidden executable substitution.

## 108. Static analysis

May inspect:

- manifest;
- dependencies;
- imports;
- binaries;
- install scripts;
- filesystem/network calls;
- dynamic execution;
- secret patterns;
- license.

## 109. Dynamic validation

Runs in isolated environment with synthetic data.

Tests:

- declared capabilities;
- denied accesses;
- resource limits;
- network behavior;
- cancellation;
- output schemas;
- event behavior;
- logging/redaction;
- failure/recovery.

## 110. Human review

Human review evaluates:

- business purpose;
- necessity;
- trust;
- permissions;
- data handling;
- support;
- license;
- vendor risk;
- residual unknowns.

## 111. Validation profile

Validation has:

- profile code/version;
- extension digest/version;
- environment;
- tests;
- results;
- limitations;
- expiry;
- reviewers;
- evidence.

## 112. Validation expiration

Triggered by:

- extension version;
- dependency changes;
- core version;
- protocol change;
- endpoint/certificate change;
- capability drift;
- security finding;
- elapsed review period.

## 113. Installation result states

```text
accepted
accepted_with_restrictions
rejected
quarantined
incompatible
deferred
unknown
```

## 114. Enablement pipeline

```text
installed
→ select workspace
→ select capabilities
→ review permissions
→ configure
→ bind secret references
→ validate health/readiness
→ policy evaluation
→ enable
→ observe
```

## 115. Enablement evidence

Includes:

- extension digest;
- capabilities;
- permission set;
- workspace;
- configuration hash;
- secret references;
- validation;
- owner;
- date;
- restrictions.

## 116. Runtime invocation

Core flow:

```text
request
→ resolve extension/capability
→ verify state and readiness
→ verify workspace enablement
→ authorize
→ evaluate policy
→ request approval if required
→ create run/attempt
→ invoke through gateway
→ observe
→ persist result/evidence
```

## 117. Extension gateway

A dedicated Extension Gateway or equivalent boundary may provide:

- discovery;
- lifecycle;
- invocation;
- permission enforcement;
- health;
- rate limiting;
- telemetry;
- error normalization;
- revocation.

## 118. Invocation envelope

Includes:

- extension ID/version/digest;
- capability;
- workspace;
- run/attempt;
- actor;
- inputs/reference;
- classification;
- permissions;
- deadline;
- idempotency;
- correlation;
- approval reference;
- expected output schema.

## 119. Invocation response

Includes:

- accepted/rejected;
- external invocation ID;
- state;
- output/artifact references;
- errors;
- usage;
- effect certainty;
- evidence;
- limitations.

## 120. Runtime isolation

Controls may include:

- separate process/container;
- non-root;
- read-only root;
- scoped mounts;
- network allowlist;
- resource limits;
- process limits;
- timeouts;
- output limits;
- seccomp/AppArmor/SELinux;
- no Docker socket.

## 121. Runtime resource quotas

Per extension:

- CPU;
- memory;
- storage;
- concurrent invocations;
- network requests;
- artifact bytes;
- event rate;
- log rate.

## 122. Denial behavior

Denied access returns a stable error and audit record.

It does not trigger fallback to unrestricted execution.

## 123. Extension errors

Categories:

```text
manifest_invalid
signature_invalid
digest_mismatch
incompatible
permission_denied
not_enabled
not_ready
capability_unknown
schema_invalid
timeout
cancelled
resource_exhausted
remote_unavailable
protocol_error
security_violation
effect_unknown
internal_error
```

## 124. Error normalization

Raw vendor errors are sanitized.

Preserve:

- safe code;
- retryability;
- side-effect certainty;
- external reference;
- correlation;
- remediation.

## 125. Cancellation

Each capability declares:

```text
unsupported
best_effort
safe_boundary
terminal_confirmation
unknown
```

Cancellation acknowledgment is not terminal proof.

## 126. Pause and resume

Optional.

Must declare:

- support;
- checkpoint;
- durability;
- compatibility;
- effect boundaries;
- approval validity.

## 127. Idempotency

Extension declares:

- native idempotency support;
- key scope;
- retention;
- duplicate behavior;
- reconciliation method.

## 128. Reconciliation

Every consequential extension capability should define:

- external reference;
- status query;
- evidence;
- duplicate detection;
- partial outcome;
- unknown outcome;
- manual recovery.

## 129. Health

Extension health includes:

- liveness;
- readiness;
- dependency health;
- validation state;
- permission state;
- configuration state;
- secret state;
- drift.

## 130. Readiness blockers

- invalid config;
- expired validation;
- unavailable dependency;
- revoked secret;
- incompatible protocol;
- undeclared capability;
- critical drift;
- emergency stop;
- quarantine.

## 131. Telemetry

Extensions emit:

- lifecycle logs;
- invocation metrics;
- traces;
- errors;
- denied access;
- resource use;
- health/readiness;
- drift;
- usage/effect observations.

## 132. Metrics

Potential:

```text
extension_invocations_total
extension_invocation_duration_seconds
extension_errors_total
extension_permission_denials_total
extension_health_state
extension_validation_age_seconds
extension_capability_drift_total
extension_resource_limit_hits_total
extension_unknown_effects_total
```

## 133. Logs

Logs include:

- extension ID/version;
- capability;
- workspace reference where authorized;
- run/attempt;
- operation code;
- result;
- error;
- no raw secret/content by default.

## 134. Traces

Trace spans:

```text
extension.resolve
extension.authorize
extension.invoke
extension.remote_call
extension.reconcile
extension.disable
extension.upgrade
```

## 135. Alerts

Examples:

- extension unexpectedly unavailable;
- validation expired;
- capability drift;
- signature/digest mismatch;
- permission violation;
- resource abuse;
- unknown-effect surge;
- secret leakage;
- event flood;
- remote endpoint identity change.

## 136. Upgrade lifecycle

```text
new_version_discovered
→ staged
→ reviewed
→ validated
→ upgrade_pending
→ canary_or_test
→ enabled
→ observed
→ previous_version_retained_or_retired
```

## 137. Upgrade classes

```text
metadata_only
patch_compatible
minor_capability
permission_expanding
protocol_breaking
security_emergency
```

## 138. Permission-expanding upgrade

Requires new review and enablement.

Cannot inherit previous approval automatically.

## 139. Protocol-breaking upgrade

Requires:

- compatibility plan;
- core/adapters;
- migrations;
- rollback;
- event/API versioning;
- test evidence.

## 140. Auto-update policy

Default:

```text
disabled
```

Possible future profiles:

- notify only;
- stage automatically;
- install disabled;
- auto-apply first-party security patch under strict policy.

No unreviewed auto-enable.

## 141. Upgrade rollback

Requires:

- previous package/digest;
- configuration compatibility;
- data migration compatibility;
- event/API compatibility;
- artifact/data ownership;
- rollback test.

## 142. Dual-version operation

May be required during migration.

Must preserve:

- routing clarity;
- workspace binding;
- schema compatibility;
- separate telemetry;
- no ambiguous provenance.

## 143. Disablement

Disablement blocks new invocation.

Existing runs are:

- allowed to finish;
- cancelled;
- paused;
- or reconciled;

according to risk and capability semantics.

## 144. Suspension

Used during investigation.

Preserves package and evidence.

## 145. Revocation

Immediate or scheduled.

Triggers:

- compromised publisher;
- malicious behavior;
- critical vulnerability;
- signature failure;
- capability drift;
- policy violation;
- unsupported version.

## 146. Revocation effects

- block new invocation;
- invalidate readiness;
- list active runs;
- reconcile effects;
- rotate affected secrets;
- alert;
- preserve evidence;
- prevent reinstall of revoked digest.

## 147. Uninstall

Preconditions:

- disabled;
- no active invocation or recovery plan;
- dependencies identified;
- data ownership handled;
- configuration export/retention;
- secret references detached;
- audit preserved;
- rollback decision.

## 148. Uninstall result

Removes:

- executable package/runtime;
- disposable caches;
- optional derived data.

Preserves:

- manifest;
- version/digest history;
- approvals;
- audit;
- receipts;
- artifact provenance;
- historical runs;
- security findings.

## 149. Extension-owned data

The manifest declares:

- data created;
- data retained;
- data export;
- data deletion;
- migration;
- ownership after uninstall.

## 150. Orphan prevention

Uninstall must not leave:

- inaccessible accepted artifacts;
- unreadable canonical data;
- dangling secret references;
- broken workflow templates;
- unresolvable event schemas;
- hidden external subscriptions.

## 151. Backup

Backup may include:

- manifests;
- installed versions/digests;
- validation records;
- configuration;
- workspace enablements;
- data owned by extension;
- migration state;
- provenance.

Executable packages may be restored from verified registry or backup.

## 152. Restore

After restore:

- extensions start disabled unless policy explicitly allows;
- verify digest/signature;
- validate compatibility;
- rebind secret references;
- reconcile remote subscriptions;
- rerun readiness;
- enable progressively.

## 153. Restore and revocation

A restore must not reactivate a version revoked after the backup point.

The current revocation list is a negative fact that must be applied.

## 154. Continuity requirements

Every critical extension declares:

- outage behavior;
- degraded mode;
- backup scope;
- restore;
- external data;
- credentials;
- vendor exit;
- support;
- runbook.

## 155. Extension dependency graph

Dependencies may include:

- core version;
- another extension;
- provider;
- secret;
- service;
- schema;
- artifact processor;
- model profile.

Cycles are prohibited or tightly controlled.

## 156. Dependency failure

Extension readiness reflects required versus optional dependencies.

No false healthy state.

## 157. Dependency substitution

Replacing a dependency may be material.

Example:

- different model provider;
- different storage backend;
- different MCP server.

Requires policy and potentially approval.

## 158. License

Manifest declares:

- license identifier;
- source availability;
- redistribution;
- commercial restrictions;
- model/data licenses;
- notices.

## 159. Intellectual property

Review:

- ownership;
- generated output rights;
- embedded assets;
- third-party code;
- terms of service;
- marketplace redistribution.

## 160. Supply-chain controls

- approved source;
- package digest;
- signature/provenance;
- dependency lock;
- vulnerability scan;
- license scan;
- build provenance;
- revocation;
- reproducibility where possible.

## 161. Signature trust

A trust store maps publisher identities to allowed extension classes and scopes.

## 162. Key compromise

If signing key compromised:

- revoke key;
- identify affected packages;
- suspend/revoke versions;
- require re-sign/rebuild/revalidation;
- notify operators;
- preserve evidence.

## 163. Transparency direction

A future registry may provide an append-only transparency log for:

- package digests;
- publisher;
- signatures;
- validation;
- revocations.

Not required for MVP.

## 164. Marketplace direction

A future marketplace may support:

- discovery;
- publisher profiles;
- version history;
- validation badges;
- permissions;
- reviews;
- support;
- pricing;
- revocation.

Marketplace listing does not imply installation or enablement.

## 165. Marketplace governance

Requires:

- publisher onboarding;
- content policy;
- security review;
- dispute process;
- removal/revocation;
- vulnerability response;
- legal terms;
- privacy disclosures.

## 166. Marketplace trust labels

Potential labels:

```text
first_party
verified_publisher
validated_version
restricted_permissions
security_reviewed
experimental
deprecated
revoked
```

Labels must be precise and evidence-backed.

## 167. Plugin pricing direction

Possible future models:

- free;
- paid license;
- subscription;
- usage-based;
- enterprise agreement.

Cost architecture must distinguish plugin charge, provider usage, and Agent OS cost.

## 168. Billing safety

A plugin cannot create unbounded charges without:

- budget;
- pricing disclosure;
- usage evidence;
- authorization;
- alerts;
- hard limits.

## 169. MCP integration direction

MCP extension support must distinguish:

```text
server registration
transport security
server identity
tool catalogue
resource catalogue
prompt catalogue
roots
sampling requests
notifications
capability changes
authorization
approval
```

## 170. MCP server registration

Record:

- server ID;
- endpoint/process command;
- transport;
- publisher/operator;
- certificate/process identity;
- version;
- capabilities;
- data classes;
- network/filesystem;
- secrets;
- health/readiness;
- validation.

## 171. MCP tools

Each MCP tool maps to an Agent OS capability with:

- effect class;
- target;
- inputs;
- output;
- data policy;
- approval;
- idempotency;
- cancellation;
- evidence.

## 172. MCP resources

Resource access is treated as data access.

Specify:

- URI patterns;
- workspace scope;
- classification;
- read/write semantics;
- freshness;
- retention.

## 173. MCP prompts

MCP prompts are untrusted content/templates.

They cannot alter platform policy, permissions, or approval state.

## 174. MCP roots

Roots define visible filesystem/workspace scope.

Agent OS must not blindly accept server-requested roots.

## 175. MCP capability drift

Tool/resource/prompt catalogue changes trigger:

- drift detection;
- suspension of new capability;
- review;
- manifest update;
- revalidation.

## 176. MCP authentication

MCP authentication proves connection identity under selected mechanism.

It does not grant platform authorization.

## 177. MCP remote server risks

- external data retention;
- endpoint compromise;
- changing tools;
- unknown model/tool execution;
- hidden subprocessors;
- region;
- availability;
- billing.

## 178. Skills architecture

A skill manifest may include:

- skill ID/version;
- purpose;
- inputs;
- expected outputs;
- capability dependencies;
- prohibited actions;
- approval checkpoints;
- evaluation;
- examples;
- source/provenance;
- compatibility.

## 179. Skill validation

Review:

- prompt injection;
- hidden authority claims;
- unsafe instructions;
- missing approval;
- unsupported assumptions;
- data disclosure;
- output quality;
- version compatibility.

## 180. Skill enablement

Skills may be:

- globally available;
- workspace-enabled;
- role-restricted;
- agent-profile-bound;
- experimental.

## 181. Skill execution

A skill instantiates a governed task or workflow.

It does not execute outside run and policy controls.

## 182. Workflow-template architecture

Template defines:

- graph;
- tasks;
- conditions;
- retries;
- approvals;
- artifacts;
- recovery;
- limits.

## 183. Template instantiation

Creates immutable task/run configuration snapshot.

Later template changes do not alter an active run.

## 184. UI-extension architecture

Potential extension points:

```text
dashboard_panel
workspace_settings_section
run_detail_panel
artifact_viewer
approval_context_panel
operations_panel
navigation_item
```

## 185. UI extension isolation

Options:

- schema-driven components;
- approved component registry;
- sandboxed iframe;
- separately built module with strict CSP.

Arbitrary script injection is prohibited.

## 186. UI authorization

Backend remains authoritative.

Hiding or showing UI is not an authorization control.

## 187. UI data access

UI extension receives a bounded API client and scoped data.

No raw database or unrestricted token.

## 188. UI accessibility

Every UI extension must satisfy:

- keyboard;
- semantic structure;
- screen reader;
- contrast;
- reflow;
- focus;
- localization;
- error states.

## 189. UI consistency

UI extensions use controlled design tokens and components when available.

A proposed design-system document remains outside this official plugin contract until registered.

## 190. API extensions

Options:

- core-mediated extension resources;
- namespaced routes;
- extension gateway proxy.

No extension may register unreviewed root-level routes.

## 191. API namespace

Recommended direction:

```text
/api/v1/extensions/{extension_id}/...
```

## 192. API extension rules

- schema;
- authentication;
- workspace authorization;
- rate limits;
- idempotency;
- error envelope;
- versioning;
- audit;
- no secret leakage.

## 193. Event extensions

Extensions may consume/publish namespaced events.

Publishing does not mutate authoritative state unless processed by an authorized core command.

## 194. Event namespace

Recommended:

```text
extension.<publisher>.<extension>.<event>
```

Core events remain controlled.

## 195. Event-schema governance

- versioned;
- compatibility;
- classification;
- correlation;
- payload limits;
- reference over large content;
- consumer idempotency;
- replay behavior.

## 196. Extension configuration

Configuration schema declares:

- fields;
- type;
- default;
- validation;
- sensitivity;
- scope;
- reload behavior;
- migration;
- UI labels.

## 197. Configuration scopes

```text
global_installation
environment
workspace
capability
user_preference
run_snapshot
```

## 198. Configuration safety

A plugin configuration cannot:

- disable core security;
- grant undeclared permission;
- alter another workspace;
- embed secrets in plaintext;
- exceed validated capability.

## 199. Configuration migration

Extension upgrade may require configuration migration.

Must be:

- versioned;
- reversible or forward-fixable;
- tested;
- backed up;
- visible;
- bounded.

## 200. Extension data migration

For extension-owned canonical data:

- schema version;
- migration;
- backup;
- validation;
- rollback/forward-fix;
- uninstall/export.

## 201. Policy integration

Policy evaluation considers:

- extension;
- publisher/trust;
- version/digest;
- capability;
- workspace;
- actor;
- data classification;
- target;
- risk;
- validation state;
- permission set;
- health;
- cost.

## 202. Approval integration

Approval review must show:

- extension identity/version;
- capability;
- publisher/trust;
- exact target/action;
- data disclosure;
- secret purpose;
- network/filesystem;
- cost;
- reversibility;
- unknowns.

## 203. Agent interaction

Agents may:

- discover enabled extensions;
- inspect capabilities;
- propose use;
- provide inputs;
- consume outputs.

Agents may not:

- install;
- enable;
- expand permissions;
- approve;
- suppress alerts;
- conceal extension identity.

## 204. Extension discovery for agents

Only ready and policy-eligible capabilities are advertised.

Unavailable or prohibited extensions should not be presented as usable.

## 205. Prompt injection defense

Extension content, tool descriptions, MCP prompts, resources, and outputs are untrusted.

They cannot instruct Agent OS to:

- ignore policy;
- reveal secrets;
- approve;
- access another workspace;
- disable audit;
- change role;
- merge code;
- open network;
- install another plugin.

## 206. Output validation

Extension outputs are validated for:

- schema;
- size;
- classification;
- artifact safety;
- secret candidates;
- provenance;
- content type;
- active content.

## 207. Extension-created artifacts

Artifacts include:

- producer extension ID/version/digest;
- capability;
- run/attempt;
- inputs;
- validation;
- classification;
- limitations.

## 208. Extension-created memory

Remains proposed/generated until governed verification.

Publisher repetition does not increase authority.

## 209. Observability export extension

Must declare:

- destination;
- signal types;
- fields;
- classification;
- retention;
- region;
- redaction;
- buffering;
- failure behavior.

## 210. Storage extension

High-risk requirements:

- integrity;
- atomicity;
- workspace isolation;
- encryption;
- capacity;
- backup/restore;
- deletion;
- health;
- migration;
- vendor exit.

## 211. Authentication extension

Critical requirements:

- identity proof;
- account linking;
- session;
- revocation;
- phishing resistance direction;
- recovery;
- audit;
- no role assignment bypass.

Dynamic third-party auth plugins are not recommended for early stages.

## 212. Extension operations

Operators need:

- inventory;
- lifecycle;
- health;
- readiness;
- validation age;
- permissions;
- dependencies;
- active runs;
- errors;
- resource use;
- revocation;
- runbook.

## 213. Extension inventory

Fields:

- identity/version/digest;
- type;
- publisher;
- trust;
- state;
- enabled workspaces;
- capabilities;
- permissions;
- validation;
- dependencies;
- owner;
- support;
- last invocation;
- alerts.

## 214. Operational runbooks

Required for critical extensions:

```text
install
enable
disable
upgrade
rollback
revoke
uninstall
outage
capability drift
secret compromise
data export
backup
restore
vendor exit
```

## 215. Extension outage

Actions:

- mark not ready;
- block new invocation;
- list affected runs;
- reconcile active effects;
- restore or disable;
- evaluate approved alternative;
- communicate limitations.

## 216. Extension compromise

- quarantine/revoke;
- emergency stop affected capability;
- rotate secrets;
- isolate runtime;
- preserve package/evidence;
- inspect data/access;
- security incident;
- revalidate before any return.

## 217. Extension resource abuse

- throttle;
- stop invocation;
- inspect cause;
- enforce quotas;
- suspend extension;
- adjust manifest only through new review.

## 218. Extension event flood

- rate-limit;
- quarantine consumer/publisher;
- preserve sample;
- inspect loop;
- prevent platform overload;
- verify no business effect duplication.

## 219. Extension dependency outage

- show degraded state;
- block affected capability;
- preserve unaffected functions;
- no silent substitution;
- monitor recovery.

## 220. Marketplace outage future

Installed extensions should continue according to local validation and policy.

Marketplace unavailability must not revoke local operation by accident.

Revocation updates may require a bounded grace policy.

## 221. Testing strategy

Test levels:

```text
manifest_schema
static_security
dependency
license
contract
capability
permission_negative
sandbox
integration
concurrency
fault
recovery
upgrade
rollback
uninstall
accessibility
performance
supply_chain
```

## 222. Manifest tests

- required fields;
- types;
- unknown fields;
- version;
- digest;
- permissions;
- capabilities;
- configuration;
- license;
- support;
- no secret values.

## 223. Permission-negative tests

Attempt:

- undeclared API;
- another workspace;
- higher classification;
- filesystem escape;
- unlisted network;
- unapproved secret;
- role mutation;
- direct lifecycle mutation;
- Tool Gateway bypass.

## 224. Sandbox tests

- path traversal;
- symlink escape;
- subprocess escape;
- network denial;
- resource exhaustion;
- output limit;
- child process;
- environment leakage;
- Docker socket absence.

## 225. Contract tests

- invocation envelope;
- response;
- errors;
- health/readiness;
- cancellation;
- idempotency;
- events;
- artifacts;
- usage;
- version negotiation.

## 226. Upgrade tests

- old to new configuration;
- permission diff;
- data migration;
- active runs;
- rollback;
- dual version;
- provenance;
- compatibility.

## 227. Uninstall tests

- active dependency;
- data export;
- artifacts;
- events;
- secrets;
- audit preservation;
- restore behavior;
- no orphan canonical data.

## 228. Recovery tests

- restored package missing;
- registry unavailable;
- revoked version in backup;
- secret rebind;
- remote subscription;
- data migration;
- capability readiness.

## 229. MCP tests

- server identity;
- tool/resource/prompt drift;
- roots;
- transport security;
- capability mapping;
- authorization;
- approval;
- data disclosure;
- remote outage;
- hidden native tool.

## 230. Skill tests

- unsafe instruction;
- missing approval;
- scope;
- capability dependency;
- prompt injection;
- output quality;
- version;
- accessibility of user-facing guidance.

## 231. UI-extension tests

- CSP;
- sandbox;
- backend authorization;
- workspace;
- accessibility;
- responsive;
- error/stale/unknown;
- no secret exposure;
- no arbitrary script.

## 232. Performance tests

- invocation latency;
- startup;
- resource use;
- concurrency;
- event volume;
- UI load;
- extension gateway overhead;
- failure isolation.

## 233. Security review profiles

Proposed:

```text
SRP-DECLARATIVE
SRP-READ-ONLY
SRP-LOCAL-CODE
SRP-REMOTE-SERVICE
SRP-PROTECTED-TOOL
SRP-STORAGE
SRP-IDENTITY
```

## 234. Quality gate integration

Before pilot use of an extension:

- manifest valid;
- digest/provenance;
- validation current;
- permissions reviewed;
- negative tests;
- health/readiness;
- runbook;
- backup/restore where relevant;
- support;
- known limitations;
- no S0/S1 findings.

## 235. Pilot extension policy

Recommended pilot allowlist:

- first-party declarative skills;
- first-party adapters;
- reviewed read-only integrations;
- reviewed artifact processors;
- adapter simulator;
- explicitly approved providers.

Dynamic unverified third-party code remains disabled.

## 236. Controlled commercial policy

May allow:

- first-party;
- reviewed partner;
- reviewed third-party;
- approved remote services.

Requires stronger:

- support;
- vulnerability response;
- license;
- continuity;
- contractual data handling;
- version lifecycle.

## 237. Plugin maturity stages

```text
P0 — No dynamic plugins; built-in extension points only
P1 — First-party separately deployed extensions
P2 — Reviewed local/partner extensions
P3 — Governed third-party registry
P4 — Marketplace and commercial ecosystem
```

## 238. P0

Core modules and static configurations only.

Safest MVP posture.

## 239. P1

Official adapters and processors deployed separately.

This document primarily prepares P1.

## 240. P2

Manually reviewed partner/local extensions.

Requires installation and validation tooling.

## 241. P3

Registry, signatures, revocation, automated validation.

## 242. P4

Marketplace, commercial terms, publisher programme, customer support.

## 243. Recommended roadmap

```text
MVP
→ stable internal extension contracts
→ official Hermes/Codex adapters
→ official simulator and processors
→ manifest/schema tooling
→ permission and validation engine
→ reviewed local extensions
→ MCP governance
→ registry
→ marketplace only after commercial controls
```

## 244. MVP recommendation

For the MVP:

- do not implement arbitrary dynamic plugin loading;
- implement stable ports/interfaces;
- implement first-party adapters as separate processes;
- implement declarative skill/workflow formats;
- implement extension inventory concepts;
- keep installation manual and controlled;
- defer public registry and marketplace.

## 245. Architecture decisions to defer

Defer until justified:

- in-process dynamic loading;
- public package ecosystem;
- automatic updates;
- plugin billing;
- third-party authentication plugins;
- arbitrary UI modules;
- unreviewed MCP servers.

## 246. Extension API direction

Potential internal resources:

```text
/extensions
/extensions/{id}
/extensions/{id}/versions
/extensions/{id}/capabilities
/extensions/{id}/permissions
/extensions/{id}/validations
/extensions/{id}/commands/install
/extensions/{id}/commands/enable
/extensions/{id}/commands/disable
/extensions/{id}/commands/revoke
/extensions/{id}/commands/uninstall
/workspaces/{workspace_id}/extensions
```

## 247. Extension events direction

Potential events:

```text
ExtensionSubmitted
ExtensionStaged
ExtensionValidationStarted
ExtensionValidated
ExtensionRejected
ExtensionInstalled
ExtensionEnabled
ExtensionDisabled
ExtensionDegraded
ExtensionCapabilityDriftDetected
ExtensionSuspended
ExtensionRevoked
ExtensionUpgradeStarted
ExtensionUpgradeCompleted
ExtensionUninstalled
ExtensionSecurityFindingDetected
```

Detailed schemas require an `EVT-001` update.

## 248. Stable error-code direction

```text
PLG_MANIFEST_INVALID
PLG_DIGEST_MISMATCH
PLG_SIGNATURE_INVALID
PLG_PUBLISHER_REVOKED
PLG_INCOMPATIBLE
PLG_VALIDATION_EXPIRED
PLG_PERMISSION_DENIED
PLG_CAPABILITY_NOT_VALIDATED
PLG_NOT_ENABLED
PLG_NOT_READY
PLG_CONFIGURATION_INVALID
PLG_SECRET_REFERENCE_INVALID
PLG_CAPABILITY_DRIFT
PLG_EXTENSION_QUARANTINED
PLG_EXTENSION_REVOKED
PLG_UNINSTALL_BLOCKED
PLG_EFFECT_UNKNOWN
```

## 249. Extension manifest template

```text
Identity:
Publisher:
Version/digest:
Type:
Execution model:
Core/protocol compatibility:
Capabilities:
Permissions:
Data access:
Network:
Filesystem:
Secrets:
Configuration:
Events:
API/UI:
Health/readiness:
Update:
Uninstall:
Support:
License:
```

## 250. Validation record template

```text
Extension:
Version/digest:
Trust class:
Validation profile:
Environment:
Tests:
Permissions reviewed:
Data handling reviewed:
Security findings:
Operational limitations:
Result:
Expiry:
Reviewers:
Evidence:
```

## 251. Enablement record template

```text
Extension/version:
Workspace:
Capabilities enabled:
Permissions:
Configuration hash:
Secret references:
Policy restrictions:
Validation:
Owner:
Approved by:
Enabled at:
Monitoring:
```

## 252. Revocation record template

```text
Extension/version/digest:
Reason:
Scope:
Detected:
Active runs:
Secrets affected:
Data affected:
Containment:
Reconciliation:
Replacement:
Owner:
Evidence:
```

## 253. Requirement catalogue

### Identity and lifecycle

- `PLG-REQ-LCM-001` — Every extension has a stable identity, version, and digest or endpoint identity.
- `PLG-REQ-LCM-002` — Installation, enablement, authorization, approval, and execution are distinct.
- `PLG-REQ-LCM-003` — Lifecycle states are explicit.
- `PLG-REQ-LCM-004` — Revoked versions cannot be invoked.
- `PLG-REQ-LCM-005` — Historical records survive uninstall.
- `PLG-REQ-LCM-006` — Validation has scope and expiry.
- `PLG-REQ-LCM-007` — Material upgrades require review.
- `PLG-REQ-LCM-008` — Extension drift is detectable.

### Permissions and security

- `PLG-REQ-SEC-001` — Undeclared access is denied.
- `PLG-REQ-SEC-002` — Workspace scope is enforced.
- `PLG-REQ-SEC-003` — Plugins cannot approve or grant permissions.
- `PLG-REQ-SEC-004` — Protected tools remain behind the Tool Gateway.
- `PLG-REQ-SEC-005` — Raw secrets are not stored in manifests or packages.
- `PLG-REQ-SEC-006` — Network and filesystem access are explicit.
- `PLG-REQ-SEC-007` — Untrusted code is isolated.
- `PLG-REQ-SEC-008` — Signature verification does not replace security validation.

### Data and contracts

- `PLG-REQ-DAT-001` — Data access and classification are declared.
- `PLG-REQ-DAT-002` — Retention and deletion behavior are declared.
- `PLG-REQ-DAT-003` — Outputs preserve provenance.
- `PLG-REQ-DAT-004` — Extension-created memory cannot self-verify.
- `PLG-REQ-DAT-005` — Extension-created artifacts use the Artifact Contract.
- `PLG-REQ-DAT-006` — API/event schemas are versioned and namespaced.
- `PLG-REQ-DAT-007` — Data export is governed.
- `PLG-REQ-DAT-008` — Uninstall does not orphan canonical data.

### Operations and continuity

- `PLG-REQ-OPS-001` — Extensions expose health and readiness.
- `PLG-REQ-OPS-002` — Critical extensions have runbooks.
- `PLG-REQ-OPS-003` — Extensions support disablement and revocation.
- `PLG-REQ-OPS-004` — Unknown effects require reconciliation.
- `PLG-REQ-OPS-005` — Backup and restore behavior is declared.
- `PLG-REQ-OPS-006` — Restore does not reactivate revoked versions.
- `PLG-REQ-OPS-007` — Resource use is bounded and observable.
- `PLG-REQ-OPS-008` — Vendor exit and support status are documented.

### MCP, skills, and UI

- `PLG-REQ-EXT-001` — MCP identity, capabilities, and roots are separately governed.
- `PLG-REQ-EXT-002` — MCP authentication does not imply platform authorization.
- `PLG-REQ-EXT-003` — Skills remain subject to run, policy, and approval controls.
- `PLG-REQ-EXT-004` — Workflow instances use immutable snapshots.
- `PLG-REQ-EXT-005` — UI extensions cannot bypass backend authorization.
- `PLG-REQ-EXT-006` — UI extensions satisfy accessibility requirements.
- `PLG-REQ-EXT-007` — Arbitrary dynamic third-party code is disabled by default.
- `PLG-REQ-EXT-008` — The core remains operable without optional extensions.

## 254. Traceability

| Source | PLG-001 response |
|---|---|
| `SCP-001` | Provider-neutral extensibility and scope limits |
| `SAD-001` | Extension points and component boundaries |
| `DDD-001` | Extension lifecycle and bounded contexts |
| `DAT-001` | Extension data, classification, backup, deletion |
| `MEM-001` | Memory connectors and source authority |
| `ORC-001` | Workflow and extension invocation |
| `INT-001` | Integration and remote-service boundaries |
| `SEC-001` | Trust, secrets, sandbox, permissions |
| `THR-001` | Supply-chain, plugin, MCP, and remote threats |
| `AGC-001` | Agent adapter extensions |
| `CAP-001` | Capability declaration and validation |
| `MOD-001` | Model-provider extensions |
| `RUN-001` | Invocation attempts, retries, effects |
| `APR-001` | Exact approval for plugin actions |
| `ART-001` | Plugin-produced artifacts |
| `API-001` | Namespaced extension APIs |
| `EVT-001` | Extension event contracts |
| `DEV-001` | Repository and implementation direction |
| `TST-001` | Extension test and conformance suites |
| `QAG-001` | Extension quality gates |
| `OBS-001` | Extension telemetry and alerts |
| `DEP-001` | Packaging and deployment |
| `OPS-001` | Operations and revocation |
| `BCP-001` | Backup, restore, continuity, vendor exit |

## 255. Mapping to architecture

Potential components:

```text
Extension Registry
Extension Gateway
Extension Validation Worker
Package Staging Store
Trust and Revocation Store
Permission Evaluator
Extension Runtime Manager
MCP Bridge
Skill and Template Registry
Extension Telemetry
```

These are logical components, not approved physical services.

## 256. ADR backlog

### `ADR-TBD-PLG-001 — Extension packaging and manifest format`

Select package format, manifest schema, digest, installation source, and staging layout.

### `ADR-TBD-PLG-002 — Extension runtime isolation`

Select process/container/IPC model, sandbox controls, resource quotas, and platform support.

### `ADR-TBD-PLG-003 — Trust, signing, registry, and revocation`

Select publisher identity, signature scheme, trust store, transparency, registry, and revocation.

### `ADR-TBD-PLG-004 — Permission and capability enforcement`

Define permission schema, workspace enablement, gateway enforcement, and policy integration.

### `ADR-TBD-PLG-005 — MCP, skills, workflows, and UI extensions`

Define MCP transport/governance, skill/template formats, UI extension points, and CSP/accessibility model.

### `ADR-TBD-PLG-006 — Upgrade, uninstall, backup, and marketplace lifecycle`

Define auto-update policy, rollback, data migration, uninstall, continuity, support, and future marketplace.

## 256A. ADR-003 plugin capability refinement

Plugins may expose broad modern agent capabilities, including code, filesystem, browser, network, model, MCP, and external integration operations. Every capability remains declared, scoped, policy-evaluated, sandboxed where applicable, approval-gated where required, and auditable. Installation, enablement, authorization, and approval remain separate states. A plugin cannot grant itself permissions, approve its own action, bypass the Tool Gateway, or cross workspace scope.

## 257. Open decisions

1. Which plugin maturity stage is required for MVP and pilot?
2. Which extension types are allowed first?
3. Which package and manifest format?
4. Which signing and trust model?
5. Which registry or local package store?
6. Which validation profiles?
7. Which runtime isolation?
8. Which IPC/transport?
9. Which permission schema?
10. Which extension gateway?
11. Which configuration and secret injection?
12. Which auto-update policy?
13. Which validation expiry?
14. Which revocation distribution?
15. Which MCP transports?
16. Which MCP server trust process?
17. Which skill format?
18. Which workflow-template format?
19. Which UI extension mechanism?
20. Which extension API namespace?
21. Which extension-owned data model?
22. Which backup/restore requirements?
23. Which marketplace roadmap?
24. Which publisher support obligations?
25. Which plugin pricing and billing rules, if any?

## 258. Risks

| Risk | Consequence | Response |
|---|---|---|
| Arbitrary code loading | Platform compromise | Defer/dedicated isolation |
| Signed plugin trusted blindly | Malicious signed code | Validation and permissions |
| Plugin bypasses Tool Gateway | Uncontrolled effects | Gateway enforcement |
| MCP treated as authorization | Privilege escalation | Separate auth/policy/approval |
| Capability drift | Hidden new access | Drift detection/suspension |
| Permission expansion on update | Silent privilege growth | New review |
| Cross-workspace cache | Data leak | Scope and negative tests |
| Secrets in plugin config | Credential exposure | Secret references/broker |
| Remote service retains data | Privacy breach | Declaration/policy |
| Plugin self-verifies memory | False authority | Core verification |
| UI plugin bypasses backend | Unauthorized action | Backend enforcement |
| Uninstall deletes history | Audit loss | Preserve records |
| Restore reactivates revoked plugin | Reintroduced compromise | Current revocation applied |
| Auto-update breaks workflows | Availability/security | Disabled by default |
| Dependency conflict | Runtime failure | Separate process/container |
| Event flood | Service degradation | Rate limits/quarantine |
| Marketplace label overstated | User trust loss | Evidence-backed labels |
| Extension billing unbounded | Cost incident | Budgets/limits |
| One extension becomes critical SPOF | Continuity risk | Core independence/fallback |
| Architecture too ambitious for MVP | Delay/complexity | Maturity stages |

## 259. Assumptions

- core extension contracts can be stabilized before dynamic loading;
- first-party adapters are deployed separately;
- capability and permission models exist;
- extension packages can be hashed and staged;
- validation can run in isolated environments;
- workspace scoping is enforceable;
- tool actions remain governed by the Tool Gateway;
- extension health and telemetry can be collected;
- operators can revoke extensions;
- marketplace functionality is deferred.

## 260. Constraints

- no arbitrary dynamic third-party code in the initial MVP by default;
- no plugin approval authority;
- no plugin permission self-grant;
- no direct core lifecycle mutation;
- no Tool Gateway bypass;
- no raw secrets in manifests/packages;
- no unreviewed network or filesystem access;
- no MCP trust by protocol alone;
- no restore reactivation of revoked extensions;
- no marketplace-readiness claim from first-party adapter support;
- no final package, runtime, signing, registry, or marketplace technology selected;
- no Git commit, push, PR, merge, package publication, or deployment during the current documentation phase;
- Git versioning remains deferred until all drafts and global consistency audit are complete.

## 261. Acceptance criteria

PLG-001 may advance to `1.0.0` when:

1. Product accepts the plugin maturity roadmap and marketplace boundary.
2. Architecture accepts extension taxonomy, manifests, lifecycle, runtime, and contracts.
3. Security accepts trust, signing, permissions, sandbox, MCP, secrets, and revocation.
4. Data accepts extension data access, provenance, retention, deletion, backup, and exit.
5. Operations accepts health, upgrade, rollback, disablement, uninstall, recovery, and runbooks.
6. Quality accepts validation profiles, conformance tests, drift, and release gates.
7. MVP extension policy is explicitly bounded;
8. installation and enablement remain separate;
9. permissions and capabilities are explicit;
10. protected actions remain behind policy and approval;
11. remote/MCP extensions are governed like code extensions;
12. upgrade and permission expansion require review;
13. revocation and uninstall preserve history;
14. backup/restore does not reactivate unsafe versions;
15. the remaining complementary documents can refine UX, IAM, policy, sandbox, audit, cost, and specific adapters without changing these core invariants.

## 262. Downstream impact

| Area | Required use |
|---|---|
| Future extension implementation | Manifest, lifecycle, permissions, gateway |
| Hermes/Codex adapter specifications | First-party extension profiles |
| MCP governance | Server/tool/resource/prompt controls |
| Skills/workflows | Declarative extension formats |
| Design system/UX | UI extension points and visual consistency |
| Security/sandbox documents | Runtime isolation and permission controls |
| Cost architecture | Plugin/provider usage and budgets |
| Audit architecture | Installation, invocation, revocation evidence |
| Document register | Mark PLG-001 drafted and resolve final dependencies |

## 263. Revision and approval history

### Approval state

- Current status: `draft`
- Priority: `P1`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial plugin and extension architecture covering extension types, manifests, trust, lifecycle, capabilities, permissions, sandboxing, installation, validation, runtime, MCP, skills, workflows, UI/API/events, upgrades, revocation, uninstall, continuity, testing, registry, and marketplace roadmap |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SAD-001` — System Architecture Description
- `DAT-001` — Data Architecture
- `MEM-001` — Memory and Knowledge Architecture
- `INT-001` — Integration Architecture
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
- `TST-001` — Test Strategy and Verification Plan
- `QAG-001` — Quality Assurance and Release Gates
- `OBS-001` — Observability Architecture
- `DEP-001` — Deployment Architecture and Environment Strategy
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
