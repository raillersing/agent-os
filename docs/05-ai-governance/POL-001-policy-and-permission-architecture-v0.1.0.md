---
document_id: POL-001
title: Agent OS Policy and Permission Architecture
version: 0.1.0
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
last_reviewed: 2026-07-20
classification: internal
source_of_truth: false
dependencies:
  - IAM-001
  - AUT-001
  - APR-001
  - SEC-001
  - DDD-001
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
  - CAP-001
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
  - PLG-001
related_proposed_documents:
  - IAM-001
  - SAN-001
  - SEC-002
  - DAT-002
  - AUD-001
  - CST-001
  - UXA-001
  - DSN-001
  - A11Y-001
  - VVR-001
related_adrs:
  - ADR-TBD-POL-001
  - ADR-TBD-POL-002
  - ADR-TBD-POL-003
  - ADR-TBD-POL-004
  - ADR-TBD-POL-005
  - ADR-TBD-POL-006
  - ADR-TBD-POL-007
---

# POL-001 — Agent OS Policy and Permission Architecture

> **Status: Draft — proposed/unregistered.** This document defines the proposed policy and permission architecture for Agent OS. It covers authorization decisions, policy administration, information and enforcement points, attributes, roles, grants, deny precedence, approval gating, obligations, explanations, policy lifecycle, simulation, rollout, caching, emergency restrictions, operations, tests, and evidence. It does not select a final policy engine or language, allow policies to perform protected side effects, or allow agents to approve or activate policy changes.

## 1. Purpose

Agent OS must decide whether a requested action is permitted, denied, approval-gated, permitted only with mandatory obligations, not applicable, indeterminate, or unknown.

These decisions govern workspaces, data, runs, agents, adapters, tools, models, artifacts, memory, external destinations, costs, exports, administration, recovery, and emergency controls.

The architecture makes decisions scoped, deterministic for the same authoritative inputs, explainable, versioned, enforceable, fail-closed, auditable, testable, and separate from approval and execution.

## 2. Objectives

The architecture must:

- implement default deny;
- establish workspace scope before protected retrieval;
- combine roles, grants, relationships, attributes, risk, environment, and revocations;
- preserve deny and revocation precedence;
- distinguish permission, capability, enablement, readiness, approval, and execution;
- support approval-required outcomes without granting approval;
- enforce mandatory obligations;
- support immutable versions, simulation, staged rollout, and rollback;
- expose safe reason codes and explanations;
- support urgent restrictive controls;
- prevent agent or adapter self-elevation;
- preserve low-latency evaluation without accepting stale negative facts.

## 3. Non-goals

POL-001 does not define authentication, final IAM roles, approval decisions, sandbox implementation, a final policy language, or a vendor. It does not let a client set the authoritative decision, allow arbitrary executable policy code, equate a role with unconditional authority, or treat policy advice as a mandatory control.

## 4. Principle — Default deny

Without an applicable authoritative permit, a protected action is denied.

## 5. Principle — Deny is durable

Revocation, suspension, emergency restriction, and explicit deny override stale or broad positive authority.

## 6. Principle — Permission is not capability

Authorization does not prove that an adapter or tool has a validated and ready capability.

## 7. Principle — Permission is not approval

A policy may require approval, but only an eligible human may decide it.

## 8. Principle — Approval is not execution

An approved action is re-evaluated before its protected effect.

## 9. Principle — Evaluation has no side effect

The decision engine returns a decision and never executes the requested operation.

## 10. Principle — Authoritative attributes only

Protected decisions rely on attributes with known source, scope, version, integrity, and freshness.

## 11. Principle — Unknown fails closed

Missing, stale, conflicting, or unverifiable critical facts do not become permits.

## 12. Principle — Workspace scope first

Authorization occurs before retrieval, search, count, preview, ranking, subscription, or export.

## 13. Principle — Obligations are mandatory

A permit with unfulfilled mandatory obligations is not executable.

## 14. Principle — Immutable policy versions

Material changes create new versions and never rewrite historical decisions.

## 15. Principle — Safe explanations

Decision explanations help users without revealing protected resources, secrets, or exploitable rule details.

## 16. Policy bounded context

The Policy bounded context owns policy sets, immutable versions, rules, targets, combining behavior, attribute requirements, obligations, advice, simulations, activations, rollbacks, emergency restrictions, decision reason codes, and policy-decision evidence.

It consumes authoritative identity, data, capability, run, approval, cost, environment, and security facts. It does not own those source facts.

## 17. Core separation model

```text
identity
→ principal and session

roles, grants, relationships, revocations
→ candidate authority facts

capability and readiness
→ technical availability

policy evaluation
→ permit, deny, approval requirement, or indeterminate

human approval
→ one exact decision

re-evaluation and enforcement
→ current permission and obligations

execution
→ governed effect

evidence
→ actual outcome
```

## 18. Policy Administration Point (PAP)

Creates, validates, reviews, versions, stages, activates, rolls back, suspends, and retires policies.

## 19. Policy Information Point (PIP)

Provides authoritative attributes and relationships.

## 20. Policy Decision Point (PDP)

Evaluates a structured request and returns a structured decision.

## 21. Policy Enforcement Point (PEP)

Blocks or allows the protected operation and enforces mandatory obligations.

## 22. Policy Registry

Stores immutable versions, activation state, dependencies, hashes, and validation evidence.

## 23. Policy Simulation Service

Evaluates candidate versions without changing live authority.

## 24. Policy Decision Cache

Caches bounded decisions while preserving scope, versions, revocation, and expiry.

## 25. Policy Evidence Recorder

Persists decision inputs by reference, policy version, result, reasons, obligations, and enforcement.

## 26. Emergency Restriction Controller

Applies urgent restrictive controls such as emergency stop, workspace freeze, provider block, export prohibition, or network block.

## 27. Policy request model

A request includes:

- request and correlation IDs;
- principal and session;
- organization and workspace;
- action and resource reference;
- capability, tool, adapter, provider, and model where relevant;
- run, step, attempt, or approval reference;
- environment;
- data classification and destination;
- risk and effect class;
- cost and budget context;
- current authoritative time;
- material action fingerprint;
- attribute-source references.

Raw secrets and unnecessary full content are excluded.

## 28. Canonical decision outcomes

```text
permit
permit_with_obligations
approval_required
deny
not_applicable
indeterminate
unknown
```

## 29. Decision — Permit

Allowed under current authoritative facts with no unfulfilled mandatory obligation.

## 30. Decision — Permit with obligations

Allowed only if every returned mandatory obligation is enforced.

## 31. Decision — Approval required

Eligible to create or continue an exact approval path, but not permitted to execute.

## 32. Decision — Deny

Explicitly prohibited.

## 33. Decision — Not applicable

The current rule or set does not target the request. Final absence of a permit becomes default deny.

## 34. Decision — Indeterminate

Required facts, schemas, dependencies, or evaluation failed.

## 35. Decision — Unknown

The platform cannot establish the integrity, freshness, or current decision state.

## 36. Decision record

A decision record contains the decision ID, request fingerprint, principal, session assurance, workspace, action, resource, selected policy versions, evaluated rules, attribute references and versions, result, reason codes, obligations, advice, approval requirement, decision time, expiry, cache state, enforcement reference, and audit reference.

It contains no raw credentials or unrestricted protected content.

## 37. Restrictive precedence

Recommended precedence:

```text
platform emergency restriction
→ organization or workspace suspension
→ principal, membership, grant, session, or credential revocation
→ explicit deny
→ mandatory security/data obligations
→ approval requirement
→ scoped permit
→ default deny
```

The final combining semantics require an ADR and formal tests.

## 38. Deny precedence

An applicable authoritative deny normally overrides a permit. Any narrower exception must be explicit in a higher-authority policy design.

Break-glass cannot override non-waivable prohibitions such as disabling audit, cross-workspace isolation, hidden impersonation, or self-approval.

## 39. Default-deny behavior

At the final protected boundary:

```text
no permit
or indeterminate
or unknown
or stale critical fact
or unfulfilled obligation
→ deny or block
```

A degraded read-only mode must be explicitly designed and cannot be inferred from evaluation failure.

## 40. Policy scopes and targeting

Policy scopes may be platform, environment, organization, workspace, project, resource type, resource instance, capability, tool, model/provider, data class, destination, risk class, time window, or emergency restriction.

Target matching must be deterministic. Lower scopes can narrow authority but cannot silently override a non-overridable higher-scope deny.

## 41. Policy set

A policy set records ID, scope, target, immutable version, rules, combining algorithm, attribute dependencies, obligations, owner, approvers, lifecycle state, effective period, validation evidence, and integrity hash.

## 42. Policy rule

A rule records ID, target, condition, effect, reason code, obligations, advice, priority where applicable, owner, tests, and change history.

A rule cannot execute a tool, consume an approval, create a grant, or modify itself.

## 43. Combining algorithms

Potential algorithms:

```text
deny_overrides
ordered_deny_overrides
permit_overrides
first_applicable
only_one_applicable
explicit_priority
```

Security-sensitive sets should prefer restrictive behavior. Source-file order must never become an accidental combining algorithm.

## 44. Combining safety

Validation detects conflicting effects, missing priority, circular references, duplicate IDs, incompatible obligations, ambiguous overrides, unresolved dependencies, and unsupported effect combinations.

Ambiguous conflict cannot resolve to a permissive result.

## 45. Attribute groups

```text
subject
session
organization
workspace
resource
action
capability
environment
data
risk
approval
cost
time
relationship
security
operations
```

## 46. Subject attributes

Principal type and state, roles, grants, delegations, memberships, support or break-glass context.

## 47. Session attributes

Assurance, authentication age, device trust, issue/expiry, reauthentication, revocation version.

## 48. Organization attributes

Organization state, global restrictions, federation state, customer profile.

## 49. Workspace attributes

Workspace state, classification ceiling, budget, operational mode, allowed integrations.

## 50. Resource attributes

Type, workspace, owner, version, state, classification, integrity, sensitivity.

## 51. Action attributes

Action code, side-effect class, reversibility, idempotency, target and destination.

## 52. Capability attributes

Declared, validated, enabled, ready, sandbox needs, cancellation and evidence support.

## 53. Environment attributes

Development, test, pilot, commercial, maintenance, recovery, or emergency-stop state.

## 54. Data attributes

Classification, category, residency, retention, exportability, deletion hold.

## 55. Risk attributes

Risk class, blast radius, threat signals, reversibility, unresolved unknowns.

## 56. Approval attributes

Exact fingerprint, state, expiry, independence, consumption, approver eligibility.

## 57. Cost attributes

Estimate, reservation, budget, currency, pricing version, unknown or conflicted cost.

## 58. Time attributes

Current time, policy effective period, grant expiry, approval expiry, maintenance window.

## 59. Relationship attributes

Ownership, project membership, sponsorship, delegation, reviewer independence.

## 60. Security attributes

Secret use, destination, sandbox profile, quarantine, integrity, violation state.

## 61. Operations attributes

Health, readiness, incident, recovery stage, backup/restore state.

## 62. Attribute metadata

Every critical attribute records name, explicit value or unknown, authoritative source, source version, effective and observed time, freshness threshold, scope, classification, integrity reference where needed, and reason for absence or conflict.

## 63. Attribute source precedence

Precedence is defined per attribute.

Examples:

```text
current membership registry
→ authoritative for membership

cached token claim
→ cannot override current revocation

adapter-reported model identity
→ observation, not authority for workspace permission
```

## 64. Missing, stale, and conflicting attributes

Missing mandatory attributes return indeterminate or unknown. Stale critical revocation, suspension, approval-consumption, emergency, classification, quarantine, readiness, or budget facts block protected execution.

Conflicting authoritative facts are recorded and reconciled; they are never resolved by choosing the more permissive value.

## 65. Untrusted attributes

User, agent, adapter, provider, extension, prompt, tool-description, and external-content values are untrusted until validated by an authoritative service.

Prompt text cannot grant a permission. External identity claims cannot create privileged roles without trusted mapping and policy.

## 66. Hybrid authorization model

Recommended direction:

```text
scoped RBAC
+ explicit grants and revocations
+ ABAC conditions
+ selected authoritative relationships
+ human approval gates
+ mandatory obligations
```

The model must remain understandable to administrators and reviewers.

## 67. RBAC

Roles provide understandable baseline responsibility. They never bypass workspace scope, explicit deny, data classification, session assurance, approval, readiness, emergency controls, or budget restrictions.

## 68. ABAC

Attribute rules handle dynamic conditions such as classification, environment, risk, destination, time, model/provider, authentication age, cost, and resource state.

## 69. Relationship-based authorization

Relationships may include project membership, resource ownership, sponsorship, delegation, task assignment, organization/workspace ancestry, and reviewer independence.

Relationships must be authoritative, versioned, and scoped.

## 70. Permission taxonomy

Illustrative stable action identifiers:

```text
workspace.read
workspace.manage
member.invite
role.assign
task.create
run.start
run.cancel
run.reconcile
approval.review
artifact.accept
artifact.export
memory.verify
agent.configure
adapter.enable
tool.invoke
secret.reference.use
policy.simulate
policy.activate
backup.restore
emergency_stop.release
```

## 71. Permission catalogue

Each permission records code, description, resource type, action class, risk, valid scopes, approval behavior, reauthentication requirement, obligations, incompatible roles, owner, status, and version.

Avoid one generic `manage_all` permission.

## 72. Capability and permission mapping

Capabilities map to narrow permissions.

Example:

```text
capability: git.commit
requires:
  - repository.read
  - repository.write_commit
may require:
  - human approval
does not include:
  - repository.push
  - pull_request.create
  - branch.merge
```

## 73. Enablement and readiness

A permit remains non-executable when the extension is not installed, the capability is not validated, the workspace has not enabled it, the runtime is not ready, secret references are invalid, or the required sandbox/network controls are unavailable.

The UI should distinguish technical unavailability from policy denial.

## 74. Approval-required outcome

`approval_required` means the action is not currently permitted to execute. It may produce an exact approval request bound to the material fingerprint.

Only an eligible human may decide. Policy is re-evaluated before dispatch, and a new deny overrides an earlier approval.

## 75. Approval requirement details

A decision may specify approval type, eligible roles, independence constraints, number of approvers, expiry, fingerprint fields, reason, evidence, and reauthentication requirement.

These constraints must remain compatible with `APR-001`.

## 76. Pre-execution re-evaluation

After approval and before protected dispatch, re-evaluate principal, session, membership, grants, revocations, policy version, emergency restrictions, target/resource version, classification, capability readiness, budget, and approval fingerprint/expiry/consumption.

## 77. Obligations

Mandatory obligations may require:

- redaction;
- an exact sandbox profile;
- network allowlists;
- encryption;
- audit/receipt generation;
- classification labels;
- cost ceilings;
- safe artifact preview;
- a specific model profile;
- retention or notification;
- export restrictions;
- evidence preservation.

## 78. Obligation lifecycle

Each obligation identifies type, parameters, enforcing component, completion criterion, failure behavior, evidence, timing, and expiry.

An unavailable or unverified pre-execution obligation blocks execution. A post-execution obligation failure creates a security or operational finding.

## 79. Advice

Advice is optional guidance such as selecting a lower-cost model, narrowing scope, using an approved destination, or reviewing on desktop. Advice must never carry a control that should be mandatory.

## 80. Reason codes

Illustrative reason codes:

```text
POL_DEFAULT_DENY
POL_WORKSPACE_ACCESS_MISSING
POL_PRINCIPAL_SUSPENDED
POL_GRANT_EXPIRED
POL_REAUTH_REQUIRED
POL_APPROVAL_REQUIRED
POL_APPROVAL_EXPIRED
POL_CAPABILITY_NOT_READY
POL_DATA_EXPORT_RESTRICTED
POL_BUDGET_EXCEEDED
POL_EMERGENCY_STOP_ACTIVE
POL_ATTRIBUTE_STALE
POL_ATTRIBUTE_CONFLICT
POL_OBLIGATION_UNAVAILABLE
```

## 81. Safe explanations

End-user explanations identify the decision, general reason, scope, missing requirement, safe next action, and decision reference without disclosing hidden resources, secret rule logic, or sensitive attributes.

Authorized administrators may inspect matched policy/rule IDs, attribute sources, freshness, combining path, obligations, and cache state.

## 82. Denial example

```text
You cannot export this artifact from the current workspace.
The artifact is restricted and the selected destination is not approved.
Choose an approved destination or contact the workspace data owner.
Decision reference: DEC-1042
```

## 83. Approval-required example

```text
Human approval is required before this Git commit can be created.
The approval covers repository X, branch Y, and the displayed diff only.
Push, pull-request creation, and merge are not included.
```

## Policy lifecycle states

```text
draft
validation_failed
validated
under_review
approved
staged
shadow
canary
active
suspended
superseded
rolled_back
retired
revoked
unknown
```

## Policy lifecycle — Draft

Editable candidate, never used for live enforcement.

## Policy lifecycle — Validation failed

Schema, reference, safety, compatibility, or test validation failed.

## Policy lifecycle — Validated

Machine validation and required tests passed.

## Policy lifecycle — Under review

Human review is incomplete.

## Policy lifecycle — Approved

Authorized for controlled deployment but not yet active.

## Policy lifecycle — Staged

Available in the target environment without live enforcement.

## Policy lifecycle — Shadow

Evaluated alongside active policy without enforcing the candidate result.

## Policy lifecycle — Canary

Enforced only for an explicit bounded scope.

## Policy lifecycle — Active

Authoritative for the configured scope.

## Policy lifecycle — Suspended

Temporarily not used because of incident, uncertainty, or governance action.

## Policy lifecycle — Superseded

Replaced by a newer version and retained historically.

## Policy lifecycle — Rolled back

No longer active because a prior approved version was restored.

## Policy lifecycle — Retired

Unavailable for new activation.

## Policy lifecycle — Revoked

Prohibited because of compromise, integrity failure, or unacceptable risk.

## Policy lifecycle — Unknown

Lifecycle state cannot be established; activation and protected use are blocked.

## Immutable policy versioning

Approved versions are immutable. Material changes create a new version.

Version identity includes policy ID, semantic or monotonic version, content hash, schema version, permission/attribute/obligation catalogue versions, engine version where material, author, reviewers, effective period, and test evidence.

## Policy dependencies

A policy may depend on:

- permission catalogue;
- role catalogue;
- attribute schema;
- data-classification taxonomy;
- capability catalogue;
- risk taxonomy;
- obligation catalogue;
- engine/compiler version.

Unresolved or incompatible dependencies block activation.

## Policy authoring model

The preferred direction is a controlled declarative format with schema validation, type checking, explicit targets, stable identifiers, deterministic evaluation, and no network, filesystem, shell, database, or tool side effects.

Unrestricted executable policy code is prohibited.

## Agent-generated policy proposals

Agents may draft policy text, tests, or simulations, but cannot:

- approve;
- activate;
- expand their own authority;
- remove a deny;
- suppress audit;
- choose themselves as reviewers;
- alter live policy.

Agent-generated material is labelled and receives independent human review.

## Policy review

Review covers purpose, owner, scope, targets, effects, deny behavior, approval behavior, obligations, attribute sources and freshness, conflicts, cross-workspace impact, explanation safety, performance, compatibility, migration, rollback, and evidence.

## Separation of duties

High-risk policy governance should distinguish:

- author;
- security reviewer;
- data reviewer;
- operations reviewer;
- product reviewer;
- quality reviewer;
- activation authority.

The same person should not be the sole author and activator of a high-risk platform policy.

## Validation pipeline

```text
parse
→ schema validation
→ type checking
→ reference resolution
→ dependency validation
→ static safety checks
→ unit/property tests
→ scenario simulation
→ conflict analysis
→ performance test
→ human review
→ approval
→ staging
```

## Static safety checks

Static checks detect:

- unreachable rules;
- duplicate identifiers;
- missing default behavior;
- broad wildcard permits;
- unbounded scope;
- missing restrictive controls;
- unresolved attributes;
- unsupported obligations;
- circular dependencies;
- ambiguous priority;
- approval bypass;
- self-elevation paths;
- missing tests.

## Policy simulation

Simulation evaluates a candidate without changing live authority.

Inputs may use synthetic scenarios, sanitized historical request references, generated boundary cases, cross-workspace negative cases, role/grant matrices, incident states, classifications, destinations, and cost states.

Simulation is evidence, not activation.

## Simulation modes

```text
unit scenario
batch scenario
historical replay
differential comparison
shadow evaluation
what-if query
```

## Historical replay safety

Historical replay must not re-execute effects, consume approvals, mutate grants, spend budgets, expose unnecessary personal data, or change live state. It evaluates recorded request facts or protected references only.

## Differential comparison

Candidate and active versions are compared for:

```text
same decision
new permit
new deny
new approval requirement
removed approval requirement
changed obligation
changed explanation
new indeterminate
```

New permits and removed obligations receive the strongest review.

## What-if analysis

Authorized users may simulate role changes, classification changes, destination changes, stronger authentication, alternate environments, emergency restrictions, or narrower resource scope.

The UI must display a persistent simulation label and never represent the result as live authority.

## Shadow mode

In shadow mode, the candidate evaluates representative live requests but the active policy remains authoritative. Candidate results cannot alter execution, approval, grants, or budgets.

## Canary rollout

Canary enforcement should use explicit bounded scopes such as one test workspace, one low-risk capability, or selected synthetic users. High-risk policy should avoid opaque random percentage rollout.

## Activation

Activation requires:

- an approved immutable version;
- compatible dependencies;
- current validation and simulations;
- activation authority;
- explicit target scope;
- effective time;
- rollback version;
- observability and runbook;
- no unresolved blocker.

A client cannot set the lifecycle state directly.

## Rollback

Rollback restores a prior approved compatible version, preserves historical decisions, records the reason, invalidates caches, re-evaluates pending protected actions, notifies owners, and creates evidence.

Rollback never rewrites decisions made under the previous version.

## Suspension and revocation

Suspend or revoke a policy when integrity fails, a repository or publisher is compromised, false permits occur, the engine becomes unstable, dependencies are invalid, or evidence is incomplete.

Any fallback must be explicitly restrictive. A broad permissive fallback is prohibited.

## Emergency restrictions

Emergency restrictions are narrow restrictive policies for:

- emergency stop;
- workspace freeze;
- provider/model block;
- tool or adapter block;
- export prohibition;
- external network prohibition;
- compromised credential containment;
- artifact quarantine enforcement;
- budget freeze;
- maintenance or recovery mode.

They cannot create positive privilege.

## Emergency restriction precedence and lifecycle

Emergency restrictions have high restrictive precedence and explicit scope.

Lifecycle:

```text
proposed
activated
active
extended
released
expired
superseded
unknown
```

Release or extension requires current authority, reason, reauthentication, and evidence.

## Policy decision caching

A decision-cache key may include principal, session assurance, authentication age, organization, workspace, action, resource version, policy version, role/grant/revocation versions, critical attribute versions, approval fingerprint and state, environment, and bounded time context.

A protected permit never outlives the shortest relevant expiry.

## Cache prohibitions

Never reuse cached decisions across:

- workspaces;
- principals;
- policy versions;
- revocation changes;
- approval consumption;
- emergency restrictions;
- resource classification changes;
- action fingerprints;
- material provider or destination changes.

## Cache invalidation

Invalidate on principal/session revocation, membership/role/grant/delegation change, policy activation/rollback, emergency restriction, resource version or classification change, approval state or consumption, capability readiness change, budget state change, quarantine, or retention hold.

## Distributed consistency

Policy evaluation must account for asynchronous state. Directional mechanisms include authoritative versions, transactional outbox events, bounded cache TTLs, stale markers, and revalidation at the protected-effect boundary.

Negative facts such as revocation and emergency stop receive stronger freshness guarantees.

## Time semantics

Distinguish request time, authentication time, policy effective time, grant expiry, approval expiry, attribute observed/effective time, and evaluation time. Use an authoritative clock and bounded clock-skew handling.

## Long-running runs

A task snapshot does not freeze authority indefinitely.

Each protected step uses current policy. Safe computation may continue only under explicit policy. New external effects require current evaluation. An approval under an old policy does not override a new deny. Policy transitions are recorded in the run timeline.

## Retries and cancellation

A retry is a new attempt and receives current policy evaluation. Unknown external effect blocks retry even when permission otherwise exists.

Cancellation itself may require permission and obligations. Permission to cancel does not imply rollback authority.

## Artifact policies

Policy may govern artifact read, preview, validation, acceptance, export, deletion, classification, retention hold, quarantine, and external destination. Decisions bind to exact artifact version and workspace.

## Memory policies

Policy may govern memory proposal, verification, retrieval, source access, export, reuse, conflict resolution, and deletion. Agent-generated memory cannot authorize its own promotion to verified authority.

## Model and provider policies

Policy may restrict provider, model profile, actual model identity, region, data class, retention/training terms, cost, fallback, external disclosure, and unknown identity.

A material fallback change triggers re-evaluation and possibly approval.

## Tool policies

Tool invocation considers tool identity/version, capability, target, side-effect class, reversibility, network/filesystem access, secret use, sandbox profile, approval, cost, evidence support, and effect certainty.

Tool-description text is never an authority source.

## Extension policies

Extension decisions consider publisher/trust, version/digest, validation, declared capability, workspace enablement, requested permissions, data handling, network/filesystem, runtime isolation, readiness, and revocation.

Installation and enablement are not blanket invocation permits.

## Sandbox obligations

Proposed/unregistered `SAN-001` will define the execution boundary. Policy may require a sandbox profile, filesystem roots, network allowlists, resource quotas, secret-broker mode, artifact staging, process restrictions, and timeout.

If the required sandbox cannot be enforced, execution is blocked.

## Cost policies

Proposed/unregistered `CST-001` will define budget facts. Policy may permit within budget, require approval above a threshold, deny when exhausted, require a cheaper profile, or return indeterminate when cost is unknown.

Unknown cost is not zero.

## Data classification policies

Proposed/unregistered `DAT-002` will define classification and lifecycle. Policy may govern accessible classes, destination compatibility, external disclosure, export, retention hold, deletion, backup, and restore.

Policy evaluation cannot itself downgrade classification.

## Audit integration

Proposed/unregistered `AUD-001` will define durable evidence. Every consequential decision preserves the request fingerprint, policy versions, rule IDs, attribute-source references, result, reasons, obligations, approval requirement, enforcement outcome, actor/session, time, and correlation.

Operational logs do not replace audit evidence.

## Policy administration permissions

Illustrative permissions:

```text
policy.read
policy.propose
policy.edit_draft
policy.validate
policy.simulate
policy.review
policy.approve
policy.stage
policy.activate
policy.rollback
policy.suspend
policy.retire
emergency_restriction.activate
emergency_restriction.release
```

They should be separated for least privilege.

## Policy change approval

High-risk changes may require security, data, operations, product, and quality review; independent activation authority; recent reauthentication; exact semantic diff; simulation report; and rollback plan.

## Semantic policy diff

A policy review should show:

- new and removed permits;
- new and removed denies;
- changed targets and scopes;
- changed attributes;
- changed obligations;
- changed approval rules;
- affected roles and resources;
- simulation differences;
- unresolved conflicts.

A raw text diff alone may be insufficient.

## Policy user-interface architecture

Primary surfaces:

```text
policy inventory
policy detail
version history
semantic diff
simulation
decision explorer
activation
rollback
emergency restrictions
policy health
access-denial explanation
```

## Policy inventory and detail

The inventory shows name, ID, scope, active version, lifecycle state, owner, effective period, risk, validation age, affected permissions/capabilities, health, and pending changes.

The detail view contains Overview, Scope, Rules, Attributes, Obligations, Approvals, Tests, Simulation, Versions, Decisions, and Operations.

## Decision explorer

Authorized users can inspect decision, request summary, principal/scope, policy version, reason codes, obligations, approval requirements, attribute sources and freshness, conflict state, cache use, and enforcement result.

The interface clearly distinguishes live, historical, and simulated decisions.

## Simulation user experience

Simulation displays:

```text
SIMULATION — no live permission change
```

Users can compare candidate and active results. Activation remains a separate governed workflow.

## Denial user experience

A denial provides a safe reason and a legitimate next action such as request access, reauthenticate, narrow scope, choose an approved destination, wait for maintenance, contact the owner, or reconcile stale facts.

It avoids protected-object enumeration and sensitive rule disclosure.

## Accessibility requirements

Policy administration follows proposed/unregistered `A11Y-001`. It requires semantic tables, keyboard-operable simulation, accessible semantic diffs, non-color-only states, screen-reader access to reasons and obligations, focus-safe activation dialogs, readable identifiers, and accessible emergency controls.

## Visual validation

Proposed/unregistered `VVR-001` should cover permit, deny, approval-required, indeterminate, unknown, stale/conflicting attributes, simulation, semantic diff, staged/shadow/canary/active/rollback states, emergency restrictions, mobile read-only review, dark theme, focus, and long explanations.

## API direction

Potential resources:

```text
/policies
/policy-sets
/policies/{id}/versions
/policy-validations
/policy-simulations
/policy-decisions
/emergency-restrictions
/permission-catalogue
/obligation-catalogue
/attribute-schemas
```

## Command API direction

Potential commands:

```text
create-draft
validate
submit-for-review
approve
stage
start-shadow
start-canary
activate
rollback
suspend
retire
simulate
activate-emergency-restriction
release-emergency-restriction
explain-decision
```

Clients cannot set authoritative results or lifecycle states directly.

## Evaluation API

A bounded internal evaluation API may return decision ID, result, safe reasons, obligations, advice, approval requirement, policy version, and expiry.

Unrestricted public policy evaluation could expose authorization structure and is not permitted by default.

## Event direction

Potential events:

```text
PolicyDraftCreated
PolicyValidationFailed
PolicyValidated
PolicySubmittedForReview
PolicyApproved
PolicyStaged
PolicyShadowStarted
PolicyCanaryStarted
PolicyActivated
PolicyRolledBack
PolicySuspended
PolicyRetired
PolicyRevoked
PolicyDecisionRecorded
PolicyObligationFailed
EmergencyRestrictionActivated
EmergencyRestrictionReleased
PolicyConflictDetected
AttributeSourceStale
```

## Event minimization

Events reference requests and protected objects instead of embedding complete sensitive attributes or policy content. Detailed evidence remains separately authorized.

## Data model direction

Core entities:

```text
PermissionDefinition
AttributeDefinition
ObligationDefinition
PolicySet
PolicyVersion
PolicyRule
PolicyTarget
PolicyDependency
PolicyValidation
PolicySimulation
PolicySimulationCase
PolicyDecision
DecisionReason
DecisionObligation
PolicyActivation
PolicyRollback
EmergencyRestriction
PolicyException
```

## Policy integrity

Approved content should be protected by immutable versioning, content hashes, controlled repository or registry, authorization, review evidence, backup, restore verification, and optional signing/provenance.

An integrity mismatch blocks activation and may trigger an emergency restriction.

## Backup and restore

Back up immutable versions, activation history, catalogues, validation and simulation evidence, decision references, emergency restrictions, and rollback metadata.

After restore, reapply current revocations and emergency restrictions, verify the active version, clear caches, and re-evaluate pending protected actions. Unknown activation state blocks protected effects.

## Operational states

```text
ready
degraded
read_only_administration
evaluation_available
evaluation_unavailable
emergency_restriction_only
recovery
unknown
```

Administration availability and evaluation availability are distinct.

## PDP, PIP, and PAP outages

If the PDP is unavailable, new protected actions are blocked. Cached permits are accepted only when explicitly safe, current, scoped, and not invalidated.

If a required PIP is stale or unavailable, affected decisions return indeterminate or unknown.

A PAP outage may prevent policy administration while active immutable evaluation continues. Emergency restriction paths may require independent protection.

## Policy engine upgrades

An engine upgrade requires compatibility analysis, replay of all policy tests, differential evaluation, performance testing, shadow/canary deployment, rollback capability, and evidence.

Identical source policy cannot be assumed to produce identical decisions across engine versions without verification.

## Monitoring and alerts

Monitor evaluation volume and latency; permit, deny, approval, default-deny, and indeterminate rates; stale/missing attributes; cache invalidation; obligation failure; conflicts; simulation differences; activations; rollbacks; and emergency restrictions.

Potential alerts include:

```text
policy_evaluation_unavailable
protected_permit_rate_anomaly
indeterminate_rate_high
attribute_source_stale
revocation_version_lag
policy_integrity_mismatch
obligation_failure
emergency_restriction_active_too_long
new_permit_diff_detected
decision_cache_invalidation_failed
policy_conflict_detected
```

## Policy incidents and response

Incidents include false permit, critical false deny, revocation bypass, cross-workspace permit, tampering, stale cache, approval bypass, obligation failure, emergency restriction failure, engine incompatibility, or compromised authorship.

Response:

1. activate restrictive containment;
2. identify policy/version and scope;
3. suspend or roll back;
4. invalidate caches;
5. preserve evidence;
6. identify affected actions and data;
7. reconcile runs and approvals;
8. correct and validate;
9. shadow/canary;
10. complete post-incident review.

## Policy runbooks

Required runbooks:

```text
create and review policy
activate policy
rollback policy
suspend compromised policy
investigate false permit
investigate false deny
resolve stale attribute source
clear decision cache
activate emergency restriction
release emergency restriction
upgrade policy engine
restore policy registry
reconcile pending protected actions
```

## Test strategy

Testing layers:

```text
schema
parser/compiler
unit rule
property
combining algorithm
attribute-source contract
permission matrix
cross-workspace
approval gating
obligation enforcement
simulation differential
cache and concurrency
fault injection
engine compatibility
performance
security abuse
accessibility
visual regression
backup and restore
```

## Rule test requirements

Every rule should include:

- positive match;
- negative non-match;
- boundary values;
- missing attributes;
- stale attributes;
- conflicting attributes;
- wrong workspace;
- suspended principal;
- expired grant;
- emergency restriction;
- explanation;
- obligations;
- decision expiry.

## Policy property tests

Important properties:

- adding an explicit deny never creates a permit;
- revoking membership never increases permission;
- an unknown critical attribute never produces protected permit;
- approval-required never directly executes;
- switching workspace invalidates the prior workspace decision;
- expired approval never becomes valid through cache;
- an unfulfilled obligation never becomes executable;
- policy rollback never rewrites old decisions;
- agent-generated policy never self-activates.

## Permission-matrix tests

For each role and action family, test expected permit, deny, approval requirement, resource and workspace boundaries, direct and temporary grants, revocation, session assurance, environment, data classification, destination, cost, and emergency restriction.

## Cross-workspace negative tests

For every protected API and query:

1. create a resource in workspace A;
2. authenticate a principal limited to workspace B;
3. attempt direct retrieval, list, search, count, export, event subscription, artifact URL, and mutation;
4. verify safe denial and no metadata leakage;
5. repeat with a stale cached permit;
6. repeat after membership revocation;
7. retain evidence.

## Approval-gating tests

Test:

- approval-eligible request;
- ineligible requester;
- ineligible approver;
- independence violation;
- expired approval;
- fingerprint change;
- approval already consumed;
- new deny after approval;
- new mandatory obligation after approval;
- policy-version change;
- workspace suspension;
- emergency restriction.

## Obligation tests

Test obligation emission, correct enforcement component, success, unavailable enforcement, partial failure, missing evidence, post-execution failure, incompatible obligations, retry, idempotency, and recovery.

## Cache tests

Test cache-key isolation, workspace separation, expiry, role/grant changes, revocation, activation, rollback, emergency restriction, approval consumption, resource/classification change, stale attributes, cache poisoning, concurrency, and invalidation failure.

## Simulation tests

Test no live side effect, no approval consumption, no grant mutation, deterministic results, active/candidate comparison, new-permit detection, historical-data minimization, access control, and persistent simulation labelling.

## Fault-injection tests

Inject PDP outage, PIP outage, policy-registry corruption, cache outage, stale revocation, clock skew, unavailable obligation service, event lag, engine crash, and incompatible versions.

Protected actions must fail safely.

## Security-abuse tests

Test attempts to:

- inject policy through prompts;
- submit client-controlled role or workspace attributes;
- spoof resource scope;
- reuse stale token claims;
- alter a decision response;
- bypass the PEP;
- self-approve;
- suppress a deny;
- activate an unreviewed policy;
- leak hidden rule detail;
- replay a permit;
- exploit wildcard rules;
- use an extension description as authority.

## Performance direction

Measure median and tail evaluation latency, cold and warm evaluations, cache behavior, large role/grant sets, high rule counts, PIP latency, simulation and shadow overhead, and evidence throughput.

Formal targets remain governed by `NFR-001`.

## MVP scope

Recommended MVP policy scope:

- default deny;
- platform and workspace policy sets;
- scoped roles and grants supplied by IAM;
- explicit denies and revocations;
- a controlled core permission catalogue;
- approval-required outcomes;
- basic mandatory obligations;
- immutable versions;
- synthetic simulation;
- controlled activation and rollback;
- decision reasons;
- cross-workspace tests;
- no unrestricted policy code.

## Pilot readiness

Before pilot:

- the role/permission matrix is approved;
- policy lifecycle is operational;
- deny precedence is validated;
- approval gating is validated;
- explanations are usable;
- emergency restrictions are exercised;
- cross-workspace tests pass;
- cache invalidation and revocation are tested;
- runbooks exist;
- no critical policy finding remains.

## Controlled-commercial direction

A controlled commercial profile may add organization-specific policies, richer ABAC and relationships, enterprise federation attributes, customer policy administration, stronger signing/provenance, policy distribution, formal access certification, regulatory retention, and independent security review.

## Policy maturity stages

```text
P0 — hard-coded restrictive boundaries
P1 — versioned declarative core policies and permissions
P2 — simulation, staged rollout, richer attributes, emergency control
P3 — organization-specific governed administration
P4 — mature multi-tenant policy programme and external assurance
```

## Requirement catalogue — Decision and enforcement

- `POL-REQ-DEC-001` — Protected actions use default deny.
- `POL-REQ-DEC-002` — Authentication, authorization, approval, and execution remain distinct.
- `POL-REQ-DEC-003` — Decision results use controlled states.
- `POL-REQ-DEC-004` — Indeterminate and unknown cannot produce protected execution.
- `POL-REQ-DEC-005` — Explicit deny and revocation override stale positive authority.
- `POL-REQ-DEC-006` — The policy engine performs no protected side effect.
- `POL-REQ-DEC-007` — Every protected effect is enforced by a PEP.
- `POL-REQ-DEC-008` — Mandatory obligations are enforced as specified.
- `POL-REQ-DEC-009` — Unfulfilled obligations block compliant execution.
- `POL-REQ-DEC-010` — Approval-required is not a permit.
- `POL-REQ-DEC-011` — Approval is revalidated against current policy before execution.
- `POL-REQ-DEC-012` — Decision evidence records policy version and reason codes.

## Requirement catalogue — Attributes and scope

- `POL-REQ-ATT-001` — Critical attributes have source, scope, version, and freshness.
- `POL-REQ-ATT-002` — Workspace authorization precedes protected retrieval.
- `POL-REQ-ATT-003` — Untrusted user, agent, adapter, provider, or extension claims cannot grant permission.
- `POL-REQ-ATT-004` — Missing mandatory attributes return indeterminate or unknown.
- `POL-REQ-ATT-005` — Stale revocation, approval, emergency, and classification facts block protected execution.
- `POL-REQ-ATT-006` — Conflicting authoritative attributes are not resolved permissively.
- `POL-REQ-ATT-007` — Attribute-source precedence is defined per attribute.
- `POL-REQ-ATT-008` — Cross-workspace caches and queries are prohibited.
- `POL-REQ-ATT-009` — Permission, capability, enablement, and readiness remain distinct.
- `POL-REQ-ATT-010` — Resource version and action fingerprint are included where required.
- `POL-REQ-ATT-011` — Unknown cost is not treated as zero.
- `POL-REQ-ATT-012` — Material provider, model, destination, or fallback changes trigger re-evaluation.

## Requirement catalogue — Lifecycle and governance

- `POL-REQ-LCM-001` — Approved policy versions are immutable.
- `POL-REQ-LCM-002` — Material changes create a new version.
- `POL-REQ-LCM-003` — Activation requires validation, review, evidence, and rollback.
- `POL-REQ-LCM-004` — Agents may propose but cannot approve or activate policies.
- `POL-REQ-LCM-005` — High-risk changes support separation of duties.
- `POL-REQ-LCM-006` — Simulation never changes live authority or consumes approval.
- `POL-REQ-LCM-007` — New permits receive explicit differential review.
- `POL-REQ-LCM-008` — Emergency restrictions are restrictive, scoped, visible, and time-bounded.
- `POL-REQ-LCM-009` — Rollback preserves historical decisions.
- `POL-REQ-LCM-010` — Policy-integrity mismatch blocks activation.
- `POL-REQ-LCM-011` — Engine upgrades receive compatibility and differential testing.
- `POL-REQ-LCM-012` — Policy exceptions are time-bounded and approved.

## Requirement catalogue — Operations and quality

- `POL-REQ-OPS-001` — PDP or critical PIP failure does not fail open.
- `POL-REQ-OPS-002` — Decision caches include policy, revocation, scope, and expiry versions.
- `POL-REQ-OPS-003` — Revocation, emergency, approval, and policy changes invalidate caches.
- `POL-REQ-OPS-004` — Protected decisions are explainable without leaking sensitive details.
- `POL-REQ-OPS-005` — Decisions and enforcement outcomes are auditable.
- `POL-REQ-OPS-006` — Backup and restore preserve versions and current negative facts.
- `POL-REQ-OPS-007` — Pending protected actions are re-evaluated after restore or policy change.
- `POL-REQ-OPS-008` — Critical paths receive cross-workspace and abuse tests.
- `POL-REQ-OPS-009` — False permits are critical incidents and release blockers.
- `POL-REQ-OPS-010` — Policy administration is accessible.
- `POL-REQ-OPS-011` — Policy visual states receive regression validation.
- `POL-REQ-OPS-012` — Policy health, conflicts, stale attributes, and obligation failures are observable.

## Traceability

| Source | POL-001 response |
|---|---|
| `IAM-001` | Principals, sessions, roles, grants, delegations, revocations |
| `AUT-001` | Human-only and approval-gated action classes |
| `APR-001` | Exact approval, expiry, independence, and consumption |
| `SAD-001` | PDP, PIP, PEP, PAP, registry, and service boundaries |
| `DDD-001` | Policy, permission, decision, obligation, and restriction model |
| `DAT-001` | Attribute data, versions, backup, and restore |
| `SEC-001` | Default deny, least privilege, integrity, and emergency controls |
| `THR-001` | Privilege escalation, confused deputy, and policy tampering |
| `CAP-001` | Capability declaration, validation, and readiness |
| `MOD-001` | Provider, model, fallback, and cost attributes |
| `RUN-001` | Re-evaluation during durable execution |
| `ART-001` | Artifact classification, export, quarantine, and deletion |
| `API-001` | Resource and command API direction |
| `EVT-001` | Policy lifecycle and decision events |
| `OBS-001` | Evaluation health, stale attributes, and alerts |
| `OPS-001` | Activation, rollback, incidents, and emergency restrictions |
| `BCP-001` | Policy continuity and restore |
| `PLG-001` | Extension trust, capabilities, and permissions |

## ADR-TBD-POL-001 — Policy engine, language, and execution model

Select the declarative language, engine, parser/compiler, safety model, packaging, and runtime topology.

## ADR-TBD-POL-002 — Decision model and combining algorithms

Approve outcomes, default deny, deny precedence, hierarchy, conflicts, and combining algorithms.

## ADR-TBD-POL-003 — Attribute, permission, and obligation catalogues

Define schemas, sources, freshness, permission granularity, obligations, advice, and versioning.

## ADR-TBD-POL-004 — Caching, consistency, and revocation

Define cache keys, expiry, invalidation, distributed versions, authoritative revalidation, and outage behavior.

## ADR-TBD-POL-005 — Lifecycle, simulation, and rollout

Approve authoring, validation, semantic diff, shadow, canary, activation, rollback, and retirement.

## ADR-TBD-POL-006 — Emergency restrictions and continuity

Define restriction types, precedence, activation, release, restore, and fail-closed continuity.

## ADR-TBD-POL-007 — Explanation, evidence, and administration UX

Define reason codes, audience-specific explanations, decision explorer, evidence, accessibility, and access control.

## Open decisions

1. Confirm `POL-001` registration.
2. Select policy language and engine direction.
3. Approve decision-result vocabulary.
4. Approve combining algorithms and deny precedence.
5. Define policy hierarchy and inheritance.
6. Approve permission codes and granularity.
7. Define attribute schemas and authoritative sources.
8. Define freshness thresholds.
9. Define obligation catalogue and enforcement ownership.
10. Define advice usage.
11. Approve policy administration roles and separation of duties.
12. Approve semantic-diff requirements.
13. Approve simulation and historical-replay controls.
14. Approve shadow and canary rollout.
15. Define emergency restriction types and release authority.
16. Define cache and revocation propagation.
17. Define PDP, PIP, PAP, registry, and cache outage behavior.
18. Define explanation detail by audience.
19. Define decision-evidence retention.
20. Define organization-managed policies for commercial stages.
21. Define engine upgrade compatibility.
22. Define false-permit incident response.
23. Confirm accessibility and visual-validation matrices.
24. Confirm exceptions and expiry.
25. Align `IAM-001`, `SAN-001`, `SEC-002`, `DAT-002`, `AUD-001`, and `CST-001`.

## Risks

| Risk | Consequence | Response |
|---|---|---|
| Role treated as unconditional authority | Privilege escalation | Hybrid evaluation |
| Missing rule becomes permit | Unauthorized access | Default deny |
| Stale revocation cache | Continued access | Versioned invalidation |
| Prompt supplies fake attributes | Policy bypass | Authoritative PIP |
| Candidate creates broad permit | Data/security incident | Differential review |
| Approval-required treated as allow | Approval bypass | Distinct decision state |
| Obligation ignored | Noncompliant effect | PEP enforcement evidence |
| Conflict resolved by file order | Nondeterminism | Approved combining |
| Agent activates policy | Self-elevation | Human governance |
| Engine outage fails open | Compromise | Fail closed |
| Explanation leaks hidden data | Information disclosure | Audience-safe explanation |
| Emergency restriction persists | Operational lockout | Scope and expiry |
| Cache crosses workspace | Data leak | Scoped keys and tests |
| Old approval overrides new deny | Unsafe execution | Re-evaluation |
| Provider fallback bypasses data policy | External disclosure | Material-change evaluation |
| Policy permits arbitrary code | Escape and side effects | Declarative model |
| Simulation changes live state | Control failure | Isolated no-side-effect service |
| Rollback erases history | Audit gap | Immutable versions |
| Permissions too fine-grained | Administrative overload | Catalogue governance |
| Permissions too broad | Excess authority | Risk-based granularity |
| Architecture too complex for MVP | Delivery delay | Maturity stages |

## Assumptions

- IAM supplies current principals, sessions, roles, grants, delegations, and revocations.
- Workspace is the primary operational isolation boundary.
- Approval remains a separate human decision system.
- Capabilities and readiness are available from authoritative registries.
- Protected effects pass through enforcement points.
- Attribute sources expose versions and freshness.
- Policy versions can be stored immutably.
- Simulation can use synthetic and sanitized historical-safe facts.
- Evidence can be retained without raw secrets.
- A restrictive MVP can precede richer organization-specific policy.

## Constraints

- default deny for protected actions;
- no policy side effects;
- no client-controlled authoritative decision;
- no agent or adapter policy activation;
- no approval mutation by policy;
- no workspace retrieval before authorization;
- no stale negative fact treated as permissive;
- no unfulfilled obligation treated as compliant permit;
- no raw secrets in policy inputs, explanations, or evidence;
- no broad fail-open mode;
- no unrestricted executable policy language;
- no final engine or vendor selection in this draft;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## Acceptance criteria

POL-001 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts permission, approval, explanation, and administration journeys;
3. Architecture accepts PDP/PIP/PEP/PAP boundaries, lifecycle, and consistency;
4. Security accepts default deny, deny precedence, integrity, emergency restrictions, and governance;
5. Data accepts attribute sourcing, classification, minimization, and retention;
6. Operations accepts activation, rollback, outage, incident, and recovery runbooks;
7. Quality accepts simulation, differential tests, cross-workspace tests, evidence, exceptions, and gates;
8. decision vocabulary and combining behavior are approved;
9. permission, attribute, and obligation catalogues are approved;
10. lifecycle and rollout are approved;
11. cache and revocation behavior are approved;
12. approval integration is approved;
13. emergency restrictions are approved;
14. explanation and evidence models are approved;
15. `SAN-001`, `SEC-002`, `DAT-002`, `AUD-001`, and `CST-001` can refine their domains without changing these invariants.

## Downstream impact

| Document | Required use |
|---|---|
| `SAN-001` | Sandbox-profile and execution-boundary obligations |
| `SEC-002` | Policy-related preventive, detective, and corrective controls |
| `DAT-002` | Classification, residency, retention, export, and deletion attributes |
| `AUD-001` | Decision, enforcement, obligation, and policy-change evidence |
| `CST-001` | Cost, reservation, budget, and pricing attributes |
| `ADP-HER-001` | Hermes capability, tool, model, and runtime mappings |
| `ADP-CDX-001` | Codex repository, command, filesystem, network, and Git mappings |
| `UXA-001` | Decision-explanation and administration journeys |
| `DSN-001` | Policy states, semantic diff, obligations, and emergency components |
| `A11Y-001` | Accessible administration and explanations |
| `VVR-001` | Decision and lifecycle visual scenarios |
| Document register | Add proposed document and dependencies |

## Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial policy and permission architecture covering PDP/PIP/PEP/PAP, decision states, deny precedence, default deny, attributes, hybrid authorization, approval gating, obligations, explanations, immutable versions, simulation, rollout, caching, emergency restrictions, operations, testing, and release gates |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `IAM-001` — Identity and Access Management Architecture — proposed/unregistered
- `AUT-001` — Autonomy and Approval Matrix
- `APR-001` — Approval Contract
- `SAD-001` — System Architecture Description
- `DDD-001` — Domain Model
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `CAP-001` — Agent Capability Schema
- `MOD-001` — Model Profile Contract
- `RUN-001` — Run and Execution Contract
- `ART-001` — Artifact Contract
- `API-001` — API Specification
- `EVT-001` — Event Catalog and Async Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
- `PLG-001` — Plugin and Extension Architecture
