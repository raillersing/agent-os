---
document_id: SEC-002
title: Agent OS Security Control Catalogue
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
related_documents: []
dependencies:
  - SEC-001
  - THR-001
  - IAM-001
  - POL-001
  - SAN-001
related_official_documents:
  - DOC-000
  - GLO-001
  - SCP-001
  - PRD-001
  - SRS-001
  - NFR-001
  - AUT-001
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
  - ADR-TBD-SEC2-001
  - ADR-TBD-SEC2-002
  - ADR-TBD-SEC2-003
  - ADR-TBD-SEC2-004
  - ADR-TBD-SEC2-005
  - ADR-TBD-SEC2-006
  - ADR-TBD-SEC2-007
  - ADR-TBD-SEC2-008
---

# SEC-002 — Agent OS Security Control Catalogue

> **Status: Draft — proposed/unregistered.** This document translates the Agent OS security architecture, threat model, identity, policy, and sandbox designs into a concrete security-control catalogue. Each control defines purpose, type, applicability, implementation direction, evidence, owner, verification cadence, maturity, and release impact. It does not claim current implementation or certification, select final security products, replace legal advice, or supersede architecture and threat-model decisions.

## 1. Purpose

The catalogue provides a common, testable security baseline for Agent OS.

It enables teams to answer:

1. which security controls are required;
2. which threats they address;
3. who owns them;
4. what evidence proves implementation;
5. how often they are verified;
6. which controls block pilot or release;
7. which controls may be deferred by maturity stage;
8. how exceptions are governed;
9. how control failures become incidents or defects;
10. how the control set evolves without losing traceability.

## 2. Objectives

The catalogue must:

- convert architecture principles into operational controls;
- cover preventive, detective, corrective, recovery, and governance controls;
- support local MVP, pilot, and controlled-commercial maturity;
- remain provider-neutral;
- map controls to threats, requirements, and evidence;
- distinguish implemented, partially implemented, planned, not applicable, failed, and unknown;
- assign accountable owners;
- define minimum evidence and verification cadence;
- identify release blockers;
- support audits, penetration tests, incident reviews, and continuous improvement;
- prevent security claims unsupported by evidence.

## 3. Non-goals

This catalogue does not:

- prove that controls are implemented;
- claim compliance with ISO 27001, SOC 2, NIST, CIS, or other frameworks;
- select a specific SIEM, IAM, secret manager, scanner, WAF, sandbox, or cloud provider;
- replace `SEC-001` or `THR-001`;
- replace detailed runbooks;
- define final legal or regulatory scope;
- permit control exceptions without approval;
- allow automated evidence to replace human review for critical controls.

## 4. Control model

Each security control contains:

```text
control_id
title
objective
control_type
applicability
requirement
implementation_direction
evidence
verification
owner
maturity
release_impact
related_threats
related_documents
```

## 5. Control types

```text
preventive
detective
corrective
recovery
governance
compensating
```

A single control may have multiple types.

## 6. Applicability states

```text
required_all
required_pilot
required_commercial
conditional
future
not_applicable
```

## 7. Implementation states

```text
not_assessed
planned
in_progress
implemented
partially_implemented
verified
failed
exception
not_applicable
unknown
```

`implemented` without evidence is not equivalent to `verified`.

## 8. Control maturity

```text
M0 — absent or undocumented
M1 — documented and manually applied
M2 — repeatable with assigned ownership
M3 — automated where appropriate and measured
M4 — continuously improved and independently reviewed
```

## 9. Release impact

```text
RB0 — critical blocker
RB1 — major blocker
RB2 — conditional blocker
RB3 — monitored debt
RB4 — advisory
```

## 10. Security-control evidence principles

Evidence must be:

- attributable;
- current;
- linked to environment and build;
- protected against unauthorized change;
- reproducible where possible;
- privacy-minimized;
- free of raw secrets;
- retained according to policy;
- reviewable by authorized roles.

A screenshot alone is insufficient for many backend or enforcement controls.

## 11. Control ownership

Primary owners may include:

```text
security-owner
architecture-owner
operations-owner
quality-owner
data-owner
product-owner
iam-owner
platform-owner
application-owner
adapter-owner
```

A control may have one accountable owner and multiple responsible contributors.

## 12. Control verification cadence

Typical cadences:

```text
per_change
per_build
per_release
daily
weekly
monthly
quarterly
annually
after_incident
after_restore
continuous
```

The strictest applicable cadence prevails.

## 13. Control severity principles

Security controls are release blockers when failure can cause:

- cross-workspace disclosure;
- unauthorized privileged action;
- approval bypass;
- raw secret exposure;
- policy fail-open;
- sandbox escape;
- unverified restore;
- audit suppression;
- unknown external effect treated as success;
- compromised build or runtime accepted as trusted.

## 14. Control domain — Governance and security management

This domain contains **6 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 15. SEC-CTL-GOV-001 — Security ownership and authority

**Objective**

Security responsibilities, decision rights, approvers, escalation paths, and exception authority are documented and assigned.

**Control type**

`governance`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Approved responsibility matrix; register entries; review minutes; escalation contacts.

**Verification cadence**

`quarterly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-GOV-OWNERSHIP`
- `THR-GOV-UNCONTROLLED-CHANGE`

## 16. SEC-CTL-GOV-002 — Security architecture review

**Objective**

Material architecture, trust-boundary, identity, policy, sandbox, data-flow, and integration changes receive security review before implementation or release.

**Control type**

`governance,preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Architecture-review record; threat-model delta; approved ADR; change classification.

**Verification cadence**

`per_change`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-ARCH-BYPASS`
- `THR-TRUST-BOUNDARY-DRIFT`

## 17. SEC-CTL-GOV-003 — Threat-model maintenance

**Objective**

`THR-001` is reviewed after material architecture changes, incidents, new adapters, new external integrations, and before pilot/commercial milestones.

**Control type**

`governance,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Updated threat model; review log; mapped mitigations; unresolved-risk register.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-UNMODELED-ATTACK`
- `THR-ASSUMPTION-DRIFT`

## 18. SEC-CTL-GOV-004 — Security exception governance

**Objective**

Every security exception records scope, risk, compensating controls, owner, expiry, approval, and remediation plan.

**Control type**

`governance,compensating`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Exception record; approval evidence; expiry monitoring; closure record.

**Verification cadence**

`monthly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-PERMANENT-EXCEPTION`
- `THR-CONTROL-BYPASS`

## 19. SEC-CTL-GOV-005 — Security risk acceptance

**Objective**

Residual high or critical security risks require explicit acceptance by authorized human roles and cannot be accepted by agents or adapters.

**Control type**

`governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Risk-acceptance record; approver identity; expiry; remediation plan.

**Verification cadence**

`per_release`

**Accountable owner**

`product-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-UNACCEPTED-RISK`
- `THR-AUTONOMOUS-RISK-ACCEPTANCE`

## 20. SEC-CTL-GOV-006 — Security training and role readiness

**Objective**

Privileged operators, developers, reviewers, and support staff receive role-appropriate training on IAM, approvals, secrets, sandboxing, incidents, and data handling.

**Control type**

`preventive,governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Training material; completion records; competency checks; refresher schedule.

**Verification cadence**

`annually`

**Accountable owner**

`security-owner`

**Target maturity**

`M1`

**Release impact**

`RB2`

**Related threat identifiers**

- `THR-HUMAN-ERROR`
- `THR-SUPPORT-ABUSE`

## 21. Control domain — Asset, configuration, and environment management

This domain contains **6 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 22. SEC-CTL-AST-001 — Authoritative asset inventory

**Objective**

Maintain an inventory of services, repositories, environments, executors, adapters, models, providers, secrets, data stores, and owners.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Inventory export; owner mapping; environment tags; stale-asset report.

**Verification cadence**

`monthly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-UNKNOWN-ASSET`
- `THR-ORPHAN-SERVICE`

## 23. SEC-CTL-AST-002 — Environment identity and separation

**Objective**

Development, test, pilot, recovery, and commercial environments have explicit identities, configuration boundaries, credentials, and visible UI indicators.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Environment manifests; credential separation; screenshots; deployment evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`architecture-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-ENV-CONFUSION`
- `THR-PROD-CREDENTIAL-IN-DEV`

## 24. SEC-CTL-AST-003 — Configuration as controlled input

**Objective**

Security-relevant configuration is versioned, reviewed, validated, and separated from secrets.

**Control type**

`preventive,governance`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Configuration schema; review record; validation output; drift report.

**Verification cadence**

`per_change`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-CONFIG-TAMPERING`
- `THR-INSECURE-DEFAULT`

## 25. SEC-CTL-AST-004 — Secure defaults

**Objective**

New workspaces, users, adapters, tools, network routes, and sandbox profiles begin in the most restrictive safe state.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Default configuration tests; onboarding checks; negative tests.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-DEFAULT-PERMIT`
- `THR-OVERPRIVILEGED-ONBOARDING`

## 26. SEC-CTL-AST-005 — Configuration drift detection

**Objective**

Detect and reconcile drift between approved configuration, running services, profiles, images, network policy, and environment metadata.

**Control type**

`detective,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Drift scan; alert; reconciliation ticket; post-fix evidence.

**Verification cadence**

`daily`

**Accountable owner**

`operations-owner`

**Target maturity**

`M3`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-DRIFT`
- `THR-UNAPPROVED-RUNTIME`

## 27. SEC-CTL-AST-006 — End-of-life asset retirement

**Objective**

Retired adapters, models, images, credentials, services, and policies are disabled, revoked, removed from scheduling, and retained only as required for evidence.

**Control type**

`preventive,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Retirement record; revocation evidence; inventory update; residual dependency report.

**Verification cadence**

`per_change`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB2`

**Related threat identifiers**

- `THR-LEGACY-ATTACK-SURFACE`
- `THR-STALE-CREDENTIAL`

## 28. Control domain — Identity, authentication, and sessions

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 29. SEC-CTL-IAM-001 — Named human identities

**Objective**

All protected human access uses unique named identities; shared human accounts are prohibited.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Account inventory; duplicate/shared-account scan; onboarding/offboarding evidence.

**Verification cadence**

`monthly`

**Accountable owner**

`iam-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-NONATTRIBUTABLE-ACTOR`
- `THR-SHARED-CREDENTIAL`

## 30. SEC-CTL-IAM-002 — Strong credential storage

**Objective**

Passwords, tokens, recovery codes, and authenticators are stored only using approved protected mechanisms; raw credential values are never logged.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Credential-storage design; configuration test; log scan; code review.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-CREDENTIAL-THEFT`
- `THR-LOGGED-SECRET`

## 31. SEC-CTL-IAM-003 — Session security

**Objective**

Interactive sessions use secure transport, protected cookies or equivalent tokens, rotation, idle/absolute expiry, CSRF protection, and revocation.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Session tests; cookie/token configuration; revocation tests; security scan.

**Verification cadence**

`per_build`

**Accountable owner**

`iam-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SESSION-THEFT`
- `THR-SESSION-FIXATION`
- `THR-CSRF`

## 32. SEC-CTL-IAM-004 — Reauthentication for critical actions

**Objective**

Role changes, secret operations, restore, emergency-stop release, support elevation, break-glass, and other critical actions require recent authentication.

**Control type**

`preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Critical-action test matrix; reauthentication events; UI evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`iam-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-STOLEN-SESSION-PRIVILEGE`
- `THR-STALE-AUTH`

## 33. SEC-CTL-IAM-005 — MFA or phishing-resistant assurance for privileged roles

**Objective**

Privileged production roles use approved MFA or phishing-resistant authentication according to the environment risk profile.

**Control type**

`preventive`

**Applicability**

`required_commercial`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Enrollment report; policy configuration; privileged-login test; exception list.

**Verification cadence**

`quarterly`

**Accountable owner**

`iam-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-PHISHING`
- `THR-PRIVILEGED-ACCOUNT-TAKEOVER`

## 34. SEC-CTL-IAM-006 — Session and token revocation

**Objective**

Logout, suspension, offboarding, credential reset, role/grant revocation, incident response, and restore invalidate affected sessions and tokens promptly.

**Control type**

`preventive,corrective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Revocation propagation test; session inventory; incident evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`iam-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-REVOKED-SESSION-USE`
- `THR-STALE-TOKEN`

## 35. SEC-CTL-IAM-007 — Workload identity

**Objective**

Services, adapters, workers, and sandboxes use distinct workload identities and short-lived credentials rather than shared human credentials.

**Control type**

`preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Workload identity inventory; credential lifetimes; owner mapping; negative tests.

**Verification cadence**

`monthly`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-WORKLOAD-IMPERSONATION`
- `THR-SHARED-SERVICE-CREDENTIAL`

## 36. SEC-CTL-IAM-008 — Break-glass governance

**Objective**

Emergency access is strongly authenticated, time-bounded, visible, scoped, audited, auto-expiring, and reviewed after use.

**Control type**

`preventive,detective,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Break-glass drill; activation record; banner evidence; post-use review.

**Verification cadence**

`quarterly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-BREAK-GLASS-ABUSE`
- `THR-AUDIT-BYPASS`

## 37. Control domain — Authorization, policy, and approvals

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 38. SEC-CTL-AUT-001 — Default deny authorization

**Objective**

Every protected operation is denied unless an applicable current permit exists.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Policy tests; API negative tests; decision records; coverage matrix.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-IMPLICIT-PERMIT`
- `THR-MISSING-RULE`

## 39. SEC-CTL-AUT-002 — Workspace authorization before retrieval

**Objective**

Workspace access is established before direct read, list, search, count, preview, export, subscription, cache lookup, or mutation.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Cross-workspace test suite; query review; cache-key tests.

**Verification cadence**

`per_build`

**Accountable owner**

`application-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-CROSS-WORKSPACE-LEAK`
- `THR-METADATA-LEAK`

## 40. SEC-CTL-AUT-003 — Deny and revocation precedence

**Objective**

Explicit deny, suspension, revocation, emergency restriction, and current negative facts override positive roles, grants, approvals, and cached permits.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Policy property tests; revocation tests; cache invalidation evidence.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-STALE-PERMIT`
- `THR-REVOCATION-BYPASS`

## 41. SEC-CTL-AUT-004 — Least-privilege roles and grants

**Objective**

Roles and grants are scoped, reviewable, justified, and avoid broad generic administration rights.

**Control type**

`preventive,governance`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Role catalogue; grant review; overprivilege report; direct-grant inventory.

**Verification cadence**

`quarterly`

**Accountable owner**

`iam-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-OVERPRIVILEGE`
- `THR-ROLE-SPRAWL`

## 42. SEC-CTL-AUT-005 — Temporary privilege expiry

**Objective**

Temporary grants, support access, delegated access, and emergency restrictions expire automatically and cannot be silently renewed.

**Control type**

`preventive,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Expiry tests; active temporary-grant report; renewal evidence.

**Verification cadence**

`monthly`

**Accountable owner**

`iam-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-PERMANENT-ELEVATION`
- `THR-EXPIRED-GRANT-USE`

## 43. SEC-CTL-AUT-006 — Approval independence

**Objective**

Protected approvals are decided by eligible humans independent from the requester and cannot be performed by agents, adapters, service accounts, or conflicted delegates.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Approval eligibility tests; audit records; independence violation tests.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SELF-APPROVAL`
- `THR-PROXY-APPROVAL`

## 44. SEC-CTL-AUT-007 — Approval binding and invalidation

**Objective**

Approvals bind to exact material fields and become invalid after target, scope, diff, destination, data, policy, cost, or other material change.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Fingerprint tests; invalidation events; replay tests.

**Verification cadence**

`per_build`

**Accountable owner**

`application-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-APPROVAL-REPLAY`
- `THR-SCOPE-SWAP`

## 45. SEC-CTL-AUT-008 — Policy re-evaluation before effect

**Objective**

Current policy, revocation, resource state, approval, capability readiness, and emergency restrictions are re-evaluated before each protected effect.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Tool Gateway tests; decision/effect correlation; stale-state tests.

**Verification cadence**

`per_build`

**Accountable owner**

`platform-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-TOCTOU-AUTHORIZATION`
- `THR-OLD-APPROVAL-NEW-DENY`

## 46. Control domain — Sandbox and secure execution

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 47. SEC-CTL-SAN-001 — Immutable sandbox specification

**Objective**

Every executable attempt uses an immutable, integrity-checked sandbox specification generated outside the sandbox.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Specification schema; hash verification; mutation tests.

**Verification cadence**

`per_build`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SANDBOX-SELF-ELEVATION`
- `THR-PROFILE-TAMPERING`

## 48. SEC-CTL-SAN-002 — Non-root least-privilege execution

**Objective**

Sandbox processes run without unnecessary privilege and cannot access host namespaces, runtime sockets, devices, or arbitrary mounts.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Runtime inspection; negative tests; profile evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SANDBOX-ESCAPE`
- `THR-HOST-COMPROMISE`

## 49. SEC-CTL-SAN-003 — Filesystem isolation

**Objective**

Read-only inputs, declared writable roots, path normalization, link controls, archive safety, and host-path denial are enforced.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Filesystem isolation tests; path-escape tests; mount manifest.

**Verification cadence**

`per_build`

**Accountable owner**

`platform-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-PATH-TRAVERSAL`
- `THR-CROSS-WORKSPACE-FILE`

## 50. SEC-CTL-SAN-004 — Network default deny

**Objective**

Sandbox network access is disabled unless destinations, protocols, ports, DNS, proxy, and classification are explicitly allowed.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Network policy tests; egress logs; denied-destination tests.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-DATA-EXFILTRATION`
- `THR-METADATA-SERVICE-ACCESS`

## 51. SEC-CTL-SAN-005 — Tool Gateway enforcement

**Objective**

Protected tools and external effects are mediated by the Tool Gateway with policy, approval, schema, target, idempotency, secret, and evidence validation.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Gateway tests; direct-bypass tests; decision/effect linkage.

**Verification cadence**

`per_build`

**Accountable owner**

`platform-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-CONFUSED-DEPUTY`
- `THR-DIRECT-API-BYPASS`

## 52. SEC-CTL-SAN-006 — Resource quotas and admission control

**Objective**

CPU, memory, process, disk, I/O, network, time, output, and concurrency limits protect platform availability.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Quota tests; saturation tests; capacity dashboards; admission logs.

**Verification cadence**

`per_release`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-DENIAL-OF-SERVICE`
- `THR-RUNAWAY-AGENT`

## 53. SEC-CTL-SAN-007 — Cancellation, cleanup, and orphan detection

**Objective**

Cancellation revokes privileged channels, terminates process trees, collects partial evidence, cleans storage/mounts, and detects orphan processes.

**Control type**

`corrective,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Cancellation tests; cleanup records; orphan alerts; executor quarantine evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`operations-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-PERSISTENT-PROCESS`
- `THR-CREDENTIAL-LEASE-LEAK`

## 54. SEC-CTL-SAN-008 — Output validation and quarantine

**Objective**

Sandbox outputs remain untrusted until type, integrity, malware, secret, archive, schema, classification, and active-content checks complete.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Validation results; quarantine events; malware/secret scan tests.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-MALICIOUS-ARTIFACT`
- `THR-SECRET-IN-OUTPUT`

## 55. Control domain — Secrets and cryptographic material

This domain contains **6 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 56. SEC-CTL-SEC-001 — Secret references instead of embedded values

**Objective**

Tasks, prompts, policies, source, logs, artifacts, and configuration use secret references rather than raw secret values.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Secret scan; code review; configuration review; redaction tests.

**Verification cadence**

`continuous`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SECRET-EXPOSURE`
- `THR-PROMPT-SECRET-LEAK`

## 57. SEC-CTL-SEC-002 — Purpose-bound secret brokerage

**Objective**

Secret access validates workload identity, workspace, purpose, tool, destination, policy, approval, and expiry.

**Control type**

`preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Secret Broker tests; lease records; wrong-purpose negative tests.

**Verification cadence**

`per_release`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SECRET-MISUSE`
- `THR-CROSS-WORKSPACE-SECRET`

## 58. SEC-CTL-SEC-003 — Short-lived secret leases

**Objective**

Execution credentials and secret leases are short-lived, scoped, revocable, and invalid after restore or executor compromise.

**Control type**

`preventive,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Lease lifetime report; revocation tests; restore tests.

**Verification cadence**

`monthly`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-LONG-LIVED-CREDENTIAL`
- `THR-RESTORED-SECRET-LEASE`

## 59. SEC-CTL-SEC-004 — Secret rotation

**Objective**

Privileged, integration, signing, and service credentials rotate on schedule and after compromise, owner change, or environment transition.

**Control type**

`preventive,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Rotation schedule; completed rotation evidence; failed-rotation alerts.

**Verification cadence**

`quarterly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-STALE-SECRET`
- `THR-CREDENTIAL-COMPROMISE`

## 60. SEC-CTL-SEC-005 — Secret redaction and scanning

**Objective**

Logs, errors, diffs, artifacts, support bundles, and telemetry are scanned and redacted for secret material.

**Control type**

`detective,corrective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Scanning reports; seeded-secret tests; incident tickets.

**Verification cadence**

`per_build`

**Accountable owner**

`quality-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-SECONDARY-SECRET-LEAK`
- `THR-SUPPORT-BUNDLE-LEAK`

## 61. SEC-CTL-SEC-006 — Cryptographic key ownership and lifecycle

**Objective**

Encryption, signing, token, TLS, and backup keys have explicit owners, purpose, storage, rotation, revocation, and recovery procedures.

**Control type**

`governance,preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Key inventory; lifecycle records; rotation drill; owner review.

**Verification cadence**

`quarterly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-KEY-LOSS`
- `THR-KEY-COMPROMISE`

## 62. Control domain — Data protection and privacy

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 63. SEC-CTL-DAT-001 — Workspace-scoped data access

**Objective**

All persisted and derived operational data is bound to an authoritative workspace or approved platform scope.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Schema review; foreign-key/constraint tests; access tests.

**Verification cadence**

`per_build`

**Accountable owner**

`data-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-DATA-SCOPE-LOSS`
- `THR-CROSS-WORKSPACE-DATA`

## 64. SEC-CTL-DAT-002 — Data classification

**Objective**

Data, artifacts, memory, logs, evidence, and exports receive controlled classification and handling rules.

**Control type**

`preventive,governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Classification catalogue; sample audit; UI evidence; policy tests.

**Verification cadence**

`quarterly`

**Accountable owner**

`data-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-UNCLASSIFIED-SENSITIVE-DATA`
- `THR-INAPPROPRIATE-EXPORT`

## 65. SEC-CTL-DAT-003 — Encryption in transit

**Objective**

Protected data and credentials use approved encrypted transport across browser, API, service, adapter, executor, and external integration boundaries.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

TLS configuration; certificate validation; negative tests; scan results.

**Verification cadence**

`per_release`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-NETWORK-EAVESDROPPING`
- `THR-MITM`

## 66. SEC-CTL-DAT-004 — Encryption at rest direction

**Objective**

Sensitive databases, artifacts, backups, secret stores, and evidence use approved at-rest protection appropriate to environment risk.

**Control type**

`preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Storage configuration; key references; restore test; threat assessment.

**Verification cadence**

`per_release`

**Accountable owner**

`data-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-STORAGE-THEFT`
- `THR-BACKUP-DISCLOSURE`

## 67. SEC-CTL-DAT-005 — Data minimization

**Objective**

Collect, propagate, log, and expose only the identity, content, telemetry, and provider data needed for the stated purpose.

**Control type**

`preventive,governance`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Data-flow review; field inventory; telemetry review; deletion candidates.

**Verification cadence**

`quarterly`

**Accountable owner**

`data-owner`

**Target maturity**

`M2`

**Release impact**

`RB2`

**Related threat identifiers**

- `THR-EXCESSIVE-DATA`
- `THR-PRIVACY-EXPOSURE`

## 68. SEC-CTL-DAT-006 — Retention and deletion enforcement

**Objective**

Retention, expiry, legal/operational hold, deletion, purge, backup propagation, and deletion evidence are enforced by data class.

**Control type**

`preventive,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Retention jobs; deletion test; hold report; restore/deletion reconciliation.

**Verification cadence**

`monthly`

**Accountable owner**

`data-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-DATA-OVERRETENTION`
- `THR-DELETION-FAILURE`

## 69. SEC-CTL-DAT-007 — Export control

**Objective**

Exports validate workspace, classification, destination, approval, redaction, format, size, recipient, and receipt.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Export policy tests; receipt records; blocked-export evidence.

**Verification cadence**

`per_build`

**Accountable owner**

`data-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-DATA-EXFILTRATION`
- `THR-UNAPPROVED-DESTINATION`

## 70. SEC-CTL-DAT-008 — Safe preview and active-content isolation

**Objective**

Untrusted or active content is rendered only through safe preview, derived representation, quarantine, or metadata-only presentation.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Preview architecture tests; malicious-content tests; quarantine evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-ACTIVE-CONTENT`
- `THR-PREVIEW-ESCAPE`

## 71. Control domain — Application, API, and integration security

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 72. SEC-CTL-APP-001 — Secure API authorization

**Objective**

Every protected API endpoint performs server-side identity, workspace, policy, and resource authorization.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Endpoint authorization matrix; negative tests; code review.

**Verification cadence**

`per_build`

**Accountable owner**

`application-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-BOLA`
- `THR-BROKEN-FUNCTION-AUTH`

## 73. SEC-CTL-APP-002 — Input validation and output encoding

**Objective**

Inputs use schemas, limits, canonicalization, and allowlists; outputs are safely encoded for their context.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Schema tests; fuzzing; injection tests; code review.

**Verification cadence**

`per_build`

**Accountable owner**

`application-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-INJECTION`
- `THR-XSS`
- `THR-PATH-INJECTION`

## 74. SEC-CTL-APP-003 — Idempotency for consequential commands

**Objective**

Protected commands use scoped idempotency keys and durable outcomes where duplicate effects are possible.

**Control type**

`preventive,corrective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Replay tests; duplicate command tests; idempotency records.

**Verification cadence**

`per_build`

**Accountable owner**

`application-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-DUPLICATE-EFFECT`
- `THR-RETRY-REPLAY`

## 75. SEC-CTL-APP-004 — Safe error handling

**Objective**

Errors avoid raw secrets, stack traces, internal topology, hidden-object existence, and false effect certainty while retaining correlation.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Error-contract tests; log review; seeded-failure tests.

**Verification cadence**

`per_build`

**Accountable owner**

`quality-owner`

**Target maturity**

`M3`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-ERROR-DISCLOSURE`
- `THR-ENUMERATION`

## 76. SEC-CTL-APP-005 — Rate limiting and abuse protection

**Objective**

Authentication, approvals, exports, tool calls, runs, uploads, and expensive endpoints have scoped abuse limits.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Rate-limit tests; abuse dashboard; exception list.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-BRUTE-FORCE`
- `THR-RESOURCE-ABUSE`

## 77. SEC-CTL-APP-006 — Integration trust validation

**Objective**

Adapters, providers, webhooks, MCP servers, plugins, and external APIs are registered, authenticated, versioned, scoped, health-checked, and revocable.

**Control type**

`preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Integration inventory; credential tests; validation reports; revocation drill.

**Verification cadence**

`quarterly`

**Accountable owner**

`architecture-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-ROGUE-INTEGRATION`
- `THR-CAPABILITY-DRIFT`

## 78. SEC-CTL-APP-007 — Webhook/event authenticity and replay protection

**Objective**

External inbound events use authenticated origin, replay protection, timestamp/nonce, schema validation, and idempotency.

**Control type**

`preventive,detective`

**Applicability**

`conditional`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Signature tests; replay tests; event evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`application-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-WEBHOOK-SPOOFING`
- `THR-EVENT-REPLAY`

## 79. SEC-CTL-APP-008 — Prompt and content boundary enforcement

**Objective**

Prompt, repository, artifact, email, web, memory, and tool-output content cannot alter IAM, policy, approval, sandbox, secret, or tool-schema authority.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Prompt-injection tests; policy-boundary tests; incident simulations.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-PROMPT-INJECTION`
- `THR-CONFUSED-DEPUTY`

## 80. Control domain — Supply chain and development security

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 81. SEC-CTL-SUP-001 — Protected source control workflow

**Objective**

Protected branches, reviewed changes, signed/attributable commits where appropriate, and restricted merge/release authority are enforced.

**Control type**

`preventive,governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Repository settings; branch-protection evidence; change reviews.

**Verification cadence**

`quarterly`

**Accountable owner**

`quality-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-SOURCE-TAMPERING`
- `THR-UNREVIEWED-CHANGE`

## 82. SEC-CTL-SUP-002 — Dependency pinning and review

**Objective**

Dependencies are version-pinned or lockfile-controlled, reviewed, and updated through a governed process.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Lockfiles; dependency diff; update review; build evidence.

**Verification cadence**

`per_change`

**Accountable owner**

`application-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-DEPENDENCY-SUBSTITUTION`
- `THR-UNCONTROLLED-UPDATE`

## 83. SEC-CTL-SUP-003 — Vulnerability and malware scanning

**Objective**

Source, dependencies, containers/images, binaries, and artifacts receive risk-based vulnerability and malware scanning.

**Control type**

`detective,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Scan reports; triage records; remediation SLAs; exceptions.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-KNOWN-VULNERABILITY`
- `THR-MALICIOUS-PACKAGE`

## 84. SEC-CTL-SUP-004 — Build isolation and reproducibility

**Objective**

Builds execute in controlled environments without broad secrets or host access and produce reproducible or traceable outputs.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Build manifests; image digest; environment record; reproducibility sample.

**Verification cadence**

`per_release`

**Accountable owner**

`platform-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-BUILD-COMPROMISE`
- `THR-UNTRUSTED-BUILD-ENV`

## 85. SEC-CTL-SUP-005 — Artifact provenance and integrity

**Objective**

Release artifacts, runtime images, policies, and adapters have hashes, version identity, source linkage, and provenance/signing direction.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

SBOM; hashes; provenance record; verification logs.

**Verification cadence**

`per_release`

**Accountable owner**

`quality-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-ARTIFACT-SUBSTITUTION`
- `THR-IMAGE-TAMPERING`

## 86. SEC-CTL-SUP-006 — Secret scanning in source and artifacts

**Objective**

Repositories, commits, build outputs, logs, and release artifacts are scanned for secret material before integration or release.

**Control type**

`detective,corrective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Secret-scan reports; seeded tests; remediation evidence.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-COMMITTED-SECRET`
- `THR-BUILD-SECRET-LEAK`

## 87. SEC-CTL-SUP-007 — Security testing in CI

**Objective**

CI includes security-focused unit, property, negative, cross-workspace, policy, approval, sandbox, and API tests appropriate to the change.

**Control type**

`detective,preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

CI reports; coverage map; failed-gate evidence.

**Verification cadence**

`per_build`

**Accountable owner**

`quality-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-REGRESSION`
- `THR-CONTROL-OMISSION`

## 88. SEC-CTL-SUP-008 — Release artifact verification

**Objective**

The exact candidate digest is verified before deployment, and runtime identity is checked after deployment.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Release manifest; digest verification; post-deploy evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-WRONG-BUILD`
- `THR-MIXED-ASSET-VERSION`

## 89. Control domain — Logging, audit, and observability

This domain contains **6 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 90. SEC-CTL-AUD-001 — Security event coverage

**Objective**

Authentication, authorization, approvals, role/grant changes, policy changes, secret use, tool effects, sandbox violations, exports, support, break-glass, and recovery events are recorded.

**Control type**

`detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Event catalogue; sample records; coverage tests.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-UNOBSERVED-ACTION`
- `THR-NONREPUDIATION-GAP`

## 91. SEC-CTL-AUD-002 — Audit integrity and append direction

**Objective**

Security audit records are protected from unauthorized alteration or deletion and retain actor, scope, time, source, correlation, and outcome.

**Control type**

`detective,preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Access-control tests; integrity checks; retention configuration.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-AUDIT-TAMPERING`
- `THR-EVIDENCE-DELETION`

## 92. SEC-CTL-AUD-003 — Time synchronization and event ordering

**Objective**

Security-relevant systems use authoritative time, expose clock health, and distinguish occurred, observed, and recorded times.

**Control type**

`detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Clock-health metrics; event-order tests; skew alerts.

**Verification cadence**

`daily`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-CLOCK-SKEW`
- `THR-EVENT-ORDER-CONFUSION`

## 93. SEC-CTL-AUD-004 — Security alerting

**Objective**

High-risk authentication, authorization, cross-workspace, secret, sandbox, policy, supply-chain, and audit anomalies generate actionable alerts.

**Control type**

`detective,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Alert catalogue; routing tests; response records; noise review.

**Verification cadence**

`monthly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-UNDETECTED-ATTACK`
- `THR-ALERT-FATIGUE`

## 94. SEC-CTL-AUD-005 — Telemetry minimization

**Objective**

Logs and metrics exclude raw secrets and minimize personal, prompt, artifact, and sensitive payload content.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Telemetry schema review; secret scans; privacy review.

**Verification cadence**

`quarterly`

**Accountable owner**

`data-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-LOG-DATA-LEAK`
- `THR-OBSERVABILITY-PRIVACY`

## 95. SEC-CTL-AUD-006 — Evidence export governance

**Objective**

Audit and evidence exports require scope, authorization, classification, destination, redaction, approval where required, and receipt.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Export records; policy tests; sample redacted bundle.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-AUDIT-EXFILTRATION`
- `THR-OVERBROAD-EVIDENCE-EXPORT`

## 96. Control domain — Vulnerability, patch, and exposure management

This domain contains **5 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 97. SEC-CTL-VUL-001 — Vulnerability intake and triage

**Objective**

Vulnerabilities from scanners, advisories, research, users, vendors, and incidents are triaged by severity, exploitability, exposure, and affected scope.

**Control type**

`detective,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Vulnerability register; triage SLA; owner assignment.

**Verification cadence**

`weekly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-KNOWN-VULNERABILITY`
- `THR-UNTRIAGED-FINDING`

## 98. SEC-CTL-VUL-002 — Remediation targets

**Objective**

Security findings have severity-based remediation targets, compensating controls, escalation, and exception approval.

**Control type**

`corrective,governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Finding age report; SLA breaches; exception records.

**Verification cadence**

`weekly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-UNPATCHED-CRITICAL`
- `THR-EXCEPTION-ABUSE`

## 99. SEC-CTL-VUL-003 — Patch and upgrade governance

**Objective**

Runtime, OS, library, image, adapter, browser, policy-engine, and infrastructure patches are tested, staged, deployed, and rollback-capable.

**Control type**

`preventive,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Patch records; staging tests; rollback evidence; version inventory.

**Verification cadence**

`monthly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-VULNERABLE-COMPONENT`
- `THR-FAILED-UPGRADE`

## 100. SEC-CTL-VUL-004 — External attack-surface review

**Objective**

Exposed ports, endpoints, domains, certificates, webhooks, and remote services are inventoried and minimized.

**Control type**

`detective,preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Exposure scan; firewall/proxy config; endpoint inventory.

**Verification cadence**

`monthly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-UNINTENDED-EXPOSURE`
- `THR-OPEN-ADMIN-ENDPOINT`

## 101. SEC-CTL-VUL-005 — Penetration and abuse testing

**Objective**

Critical trust boundaries, IAM, APIs, policy, sandbox, adapters, artifact previews, and cross-workspace isolation receive independent or dedicated adversarial testing.

**Control type**

`detective`

**Applicability**

`required_commercial`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Test report; remediation evidence; retest result.

**Verification cadence**

`annually`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-COMPLEX-CHAIN`
- `THR-UNKNOWN-VULNERABILITY`

## 102. Control domain — Incident response and recovery

This domain contains **6 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 103. SEC-CTL-IR-001 — Security incident classification

**Objective**

Security incidents use controlled severity, ownership, escalation, containment, communication, evidence, recovery, and post-incident review.

**Control type**

`corrective,governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Incident procedure; severity matrix; incident records.

**Verification cadence**

`annually`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-CHAOTIC-RESPONSE`
- `THR-DELAYED-CONTAINMENT`

## 104. SEC-CTL-IR-002 — Credential and session containment

**Objective**

Compromised identities, sessions, tokens, secrets, workload credentials, and integrations can be revoked rapidly.

**Control type**

`corrective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Revocation drill; incident playbook; propagation evidence.

**Verification cadence**

`quarterly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-CREDENTIAL-COMPROMISE`
- `THR-ACTIVE-SESSION-ABUSE`

## 105. SEC-CTL-IR-003 — Emergency-stop capability

**Objective**

Authorized humans can disable selected executions, adapters, tools, network egress, secret leases, workspaces, or the full platform while preserving audit.

**Control type**

`corrective,preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Emergency-stop drill; UI and event evidence; release procedure.

**Verification cadence**

`quarterly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-AUTONOMOUS-HARM`
- `THR-CONTROL-PLANE-INCIDENT`

## 106. SEC-CTL-IR-004 — Security evidence preservation

**Objective**

Incident evidence is preserved with integrity, classification, access control, timeline, and chain-of-custody direction.

**Control type**

`detective,corrective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Incident evidence manifest; hashes; access log; retention.

**Verification cadence**

`after_incident`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-EVIDENCE-LOSS`
- `THR-POST-INCIDENT-UNCERTAINTY`

## 107. SEC-CTL-IR-005 — Post-incident review and control improvement

**Objective**

Material incidents receive root-cause analysis, control-gap mapping, remediation owners, deadlines, and verification.

**Control type**

`corrective,governance`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Post-incident review; action register; retest evidence.

**Verification cadence**

`after_incident`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-REPEAT-INCIDENT`
- `THR-SUPERFICIAL-FIX`

## 108. SEC-CTL-IR-006 — User and stakeholder security communication

**Objective**

Security communications are accurate, timely, scoped, approved, and avoid unsupported conclusions.

**Control type**

`corrective,governance`

**Applicability**

`conditional`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Communication templates; approval record; incident timeline.

**Verification cadence**

`after_incident`

**Accountable owner**

`product-owner`

**Target maturity**

`M1`

**Release impact**

`RB2`

**Related threat identifiers**

- `THR-MISLEADING-COMMUNICATION`
- `THR-DELAYED-NOTIFICATION`

## 109. Control domain — Business continuity and disaster recovery

This domain contains **5 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 110. SEC-CTL-BCP-001 — Security-preserving backups

**Objective**

Backups preserve confidentiality, integrity, access control, classification, and encryption while excluding unnecessary reusable sessions and raw secrets.

**Control type**

`preventive,recovery`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Backup config; encryption evidence; access tests; inventory.

**Verification cadence**

`monthly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-BACKUP-DISCLOSURE`
- `THR-RESTORED-SESSION`

## 111. SEC-CTL-BCP-002 — Restore verification

**Objective**

Restores verify integrity, schema, identity, revocation, policy, audit, artifacts, classification, and service readiness before normal operations resume.

**Control type**

`recovery,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Restore drill; validation checklist; release decision.

**Verification cadence**

`quarterly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-CORRUPT-RESTORE`
- `THR-PREMATURE-RECOVERY`

## 112. SEC-CTL-BCP-003 — Negative-fact reapplication after restore

**Objective**

Revocations, suspensions, expired grants, emergency restrictions, deleted/quarantined states, and unknown effects remain authoritative after restore.

**Control type**

`preventive,recovery`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Restore negative-state tests; reconciliation report.

**Verification cadence**

`quarterly`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-RESTORE-REVIVES-ACCESS`
- `THR-RESTORE-RETRIES-EFFECT`

## 113. SEC-CTL-BCP-004 — Recovery-only mode

**Objective**

During uncertain recovery, ordinary protected effects are blocked and only explicit recovery capabilities are available.

**Control type**

`preventive,recovery`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Recovery-mode tests; UI evidence; policy decision records.

**Verification cadence**

`quarterly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-RECOVERY-OVERPRIVILEGE`
- `THR-UNVERIFIED-NORMAL-OPS`

## 114. SEC-CTL-BCP-005 — Continuity of security operations

**Objective**

Security alerting, revocation, emergency restrictions, identity, and evidence remain available or have documented fallback during major outages.

**Control type**

`recovery`

**Applicability**

`required_commercial`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Continuity exercise; fallback records; recovery metrics.

**Verification cadence**

`annually`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-SECURITY-CONTROL-OUTAGE`
- `THR-BLIND-RECOVERY`

## 115. Control domain — Agent, model, and adapter-specific controls

This domain contains **8 controls**. Controls are cumulative: a later maturity stage may strengthen evidence, automation, and frequency, but does not remove lower-stage requirements.

## 116. SEC-CTL-AI-001 — Agent authority isolation

**Objective**

Agent profiles cannot authenticate as humans, approve actions, grant roles, change policy, weaken sandbox controls, or suppress evidence.

**Control type**

`preventive`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Capability tests; policy tests; approval tests; adapter conformance.

**Verification cadence**

`per_build`

**Accountable owner**

`security-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-AGENT-SELF-ELEVATION`
- `THR-AUTONOMOUS-APPROVAL`

## 117. SEC-CTL-AI-002 — Capability declaration and validation

**Objective**

Agent and adapter capabilities are declared, versioned, validated, mapped to permissions, and disabled on capability drift or unknown state.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Capability schema; validation report; drift events.

**Verification cadence**

`per_release`

**Accountable owner**

`adapter-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-CAPABILITY-DRIFT`
- `THR-FALSE-CAPABILITY`

## 118. SEC-CTL-AI-003 — Model identity and fallback transparency

**Objective**

Configured, selected, adapter-reported, provider-reported, inferred, and unknown model identities remain distinct; material fallback triggers re-evaluation.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Model decision records; fallback tests; UI evidence.

**Verification cadence**

`per_release`

**Accountable owner**

`architecture-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-MODEL-SUBSTITUTION`
- `THR-HIDDEN-FALLBACK`

## 119. SEC-CTL-AI-004 — Prompt-injection resilience

**Objective**

Untrusted instructions cannot change identity, policy, approval, secrets, sandbox, tools, or evidence boundaries.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Prompt-injection suite; red-team scenarios; failure records.

**Verification cadence**

`per_release`

**Accountable owner**

`security-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-PROMPT-INJECTION`
- `THR-TOOL-MISUSE`

## 120. SEC-CTL-AI-005 — Memory provenance and authority

**Objective**

Memory records expose source, authority, confidence, freshness, conflicts, and verification; agent-generated memory is not silently authoritative.

**Control type**

`preventive,detective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Memory tests; provenance records; conflict scenarios.

**Verification cadence**

`per_release`

**Accountable owner**

`data-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-POISONED-MEMORY`
- `THR-FALSE-AUTHORITY`

## 121. SEC-CTL-AI-006 — Unknown effect and retry safety

**Objective**

External effects have explicit certainty; unknown effects block retry until reconciliation.

**Control type**

`preventive,corrective`

**Applicability**

`required_all`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Tool effect tests; retry-block tests; reconciliation records.

**Verification cadence**

`per_build`

**Accountable owner**

`platform-owner`

**Target maturity**

`M3`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-DUPLICATE-EXTERNAL-EFFECT`
- `THR-FALSE-SUCCESS`

## 122. SEC-CTL-AI-007 — Cost and budget enforcement

**Objective**

Model, tool, network, storage, and compute use is attributed, bounded, and blocked or approval-gated when budget facts require.

**Control type**

`preventive,detective`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Budget tests; reservation records; cost alerts; unknown-cost scenarios.

**Verification cadence**

`per_release`

**Accountable owner**

`product-owner`

**Target maturity**

`M2`

**Release impact**

`RB1`

**Related threat identifiers**

- `THR-COST-RUNAWAY`
- `THR-UNKNOWN-COST-AS-ZERO`

## 123. SEC-CTL-AI-008 — Adapter revocation and kill switch

**Objective**

Compromised, drifting, or unsafe adapters can be disabled immediately without disabling unrelated core services.

**Control type**

`corrective,preventive`

**Applicability**

`required_pilot`

**Implementation direction**

- implement the control at the authoritative enforcement boundary;
- define explicit failure and unknown behavior;
- preserve organization and workspace scope;
- avoid raw secrets in configuration, logs, or evidence;
- expose operational health and ownership;
- connect the control to relevant runbooks and release gates.

**Minimum evidence**

Revocation drill; readiness state; blocked dispatch tests.

**Verification cadence**

`quarterly`

**Accountable owner**

`operations-owner`

**Target maturity**

`M2`

**Release impact**

`RB0`

**Related threat identifiers**

- `THR-COMPROMISED-ADAPTER`
- `THR-UNBOUNDED-ADAPTER-ACCESS`

## 124. Control evidence register

The evidence register should record:

```text
control_id
environment
implementation_status
implementation_reference
evidence_type
evidence_location
build_or_version
collected_at
collector
reviewer
verification_result
expiry
exception
next_review
```

## 125. Control assessment method

Assessment steps:

1. confirm applicability;
2. inspect implementation design;
3. inspect current environment;
4. execute required tests;
5. collect evidence;
6. classify result;
7. record defects or exceptions;
8. determine release impact;
9. assign remediation;
10. schedule re-verification.

## 126. Control failure states

```text
design_missing
implementation_missing
implementation_partial
evidence_missing
verification_failed
control_bypassed
control_stale
control_unknown
exception_expired
```

A control reported as `unknown` cannot be treated as passing.

## 127. Compensating controls

A compensating control must:

- address the same threat or risk;
- be at least proportionate to the missing control;
- have an owner and evidence;
- be operationally sustainable;
- be time-bounded;
- not undermine another critical control;
- be approved by Security and the accountable business/technical owner.

Compensating controls do not permanently redefine the baseline.

## 128. Control exception template

```text
exception_id:
control_id:
scope:
environment:
reason:
risk:
affected threats:
compensating controls:
owner:
approved_by:
created_at:
expires_at:
remediation:
verification:
release impact:
```

## 129. Pilot minimum control baseline

Before pilot, at minimum:

- every `RB0` control is verified or the pilot is blocked;
- every applicable `RB1` control is implemented and tested;
- cross-workspace, approval, policy, sandbox, secret, export, restore, and emergency-stop controls pass;
- no raw production secret or real customer data is used in test evidence;
- critical incidents and recovery runbooks are exercised;
- control exceptions are current and visible;
- the actual pilot deployment is re-verified after deployment.

## 130. Controlled-commercial baseline

Before controlled commercial operation:

- privileged MFA or equivalent assurance is implemented;
- external attack-surface and penetration testing are completed;
- workload identity, secret brokerage, audit integrity, and recovery controls are mature;
- customer/organization isolation is validated;
- access reviews and vulnerability SLAs are operational;
- security evidence can support customer and procurement review;
- unresolved `RB0` or `RB1` controls block release.

## 131. Security control release gate

A release decision must include:

- applicable control set;
- control-status summary;
- failed and unknown controls;
- critical evidence links;
- active exceptions and expiry;
- vulnerability status;
- threat-model delta;
- security test results;
- penetration-test status where applicable;
- residual risk;
- Security and Quality decision.

## 132. Control metrics

Potential metrics:

- control verification coverage;
- overdue verification count;
- failed `RB0/RB1` controls;
- exception count and age;
- mean remediation age;
- revocation propagation time;
- privileged access review completion;
- cross-workspace negative-test pass rate;
- secret-scan findings;
- sandbox violation rate;
- policy indeterminate rate;
- unknown-effect reconciliation time;
- vulnerability age by severity;
- restore security validation time;
- control evidence freshness.

## 133. Security control dashboard

The dashboard should distinguish:

```text
verified
implemented_not_verified
partial
failed
exception
not_applicable
unknown
overdue
```

It must not show an overall green status when a critical control is failed, unknown, or supported only by an expired exception.

## 134. Control review cadence

Recommended governance:

- monthly review of failed, unknown, and expired controls;
- quarterly review of critical control effectiveness;
- per-release review of release-scope controls;
- annual full-catalogue review;
- immediate review after material incidents or architecture changes.

## 135. Requirement catalogue

- `SEC2-REQ-001` — Every applicable control has an accountable owner.
- `SEC2-REQ-002` — Every applicable control has current evidence.
- `SEC2-REQ-003` — Unknown control state is not treated as verified.
- `SEC2-REQ-004` — `RB0` control failure blocks pilot and release.
- `SEC2-REQ-005` — `RB1` failure blocks release unless an approved, time-bounded exception exists.
- `SEC2-REQ-006` — Security exceptions have compensating controls, owner, expiry, and remediation.
- `SEC2-REQ-007` — Critical control evidence is tied to build and environment.
- `SEC2-REQ-008` — Control effectiveness is tested, not inferred from documentation alone.
- `SEC2-REQ-009` — Architecture and threat-model changes trigger control applicability review.
- `SEC2-REQ-010` — Control evidence excludes raw secrets and unnecessary sensitive data.
- `SEC2-REQ-011` — Restore and recovery re-verify current negative security facts.
- `SEC2-REQ-012` — Security-control status is visible in release governance.
- `SEC2-REQ-013` — Agents and adapters cannot attest their own security controls as verified.
- `SEC2-REQ-014` — Control automation failures remain visible.
- `SEC2-REQ-015` — Compensating controls do not silently replace the baseline.
- `SEC2-REQ-016` — Critical controls receive independent or dual review where appropriate.

## 136. Traceability

| Source | SEC-002 response |
|---|---|
| `SEC-001` | Security architecture principles and trust boundaries |
| `THR-001` | Threats, abuse cases, residual risks |
| `IAM-001` | Identity, session, role, grant, support, and break-glass controls |
| `POL-001` | Default deny, policy lifecycle, obligations, emergency restrictions |
| `SAN-001` | Process, filesystem, network, secret, tool, and executor controls |
| `AUT-001` | Human-only actions and autonomy boundaries |
| `APR-001` | Exact approval, independence, expiry, and consumption |
| `RUN-001` | Durable attempts, retries, cancellation, unknown effects |
| `ART-001` | Validation, quarantine, preview, export, and deletion |
| `DAT-001` | Data architecture, backups, restore, and workspace scope |
| `OBS-001` | Security telemetry, freshness, alerts, and dashboards |
| `DEP-001` | Environment, deployment, image, network, and configuration controls |
| `OPS-001` | Operational runbooks, emergency stop, incidents, maintenance |
| `BCP-001` | Security-preserving continuity and recovery |
| `PLG-001` | Extension trust, permissions, validation, and revocation |

## 137. ADR-TBD-SEC2-001 — Control ownership and assessment model

Approve accountable owners, assessment roles, evidence review, implementation states, and maturity scoring.

## 138. ADR-TBD-SEC2-002 — Control evidence storage and integrity

Define evidence repository, access control, hashes, retention, privacy minimization, and audit export.

## 139. ADR-TBD-SEC2-003 — Security release-gate policy

Approve RB0–RB4 semantics, exception authority, pilot/commercial minimums, and residual-risk acceptance.

## 140. ADR-TBD-SEC2-004 — Security testing and scanning stack

Select SAST, dependency, secret, image, malware, DAST, policy, sandbox, and infrastructure testing directions.

## 141. ADR-TBD-SEC2-005 — Vulnerability severity and remediation objectives

Define severity model, exploitability adjustments, SLA targets, escalation, and exception rules.

## 142. ADR-TBD-SEC2-006 — Security monitoring and alert routing

Define security metrics, alert severity, routing, retention, escalation, and false-positive governance.

## 143. ADR-TBD-SEC2-007 — Independent assurance and penetration testing

Define pilot/commercial adversarial testing, scope, independence, retesting, and evidence handling.

## 144. ADR-TBD-SEC2-008 — External framework mapping

Decide whether and when to map controls to ISO 27001, SOC 2, NIST CSF, CIS, OWASP, or customer questionnaires.

## 145. Open decisions

1. Confirm `SEC-002` registration.
2. Approve control identifier and status vocabularies.
3. Confirm accountable owners for every control.
4. Approve RB0–RB4 release semantics.
5. Define pilot and controlled-commercial minimum baselines.
6. Define evidence storage, access, retention, and integrity.
7. Select security scanning and testing directions.
8. Define vulnerability severity and remediation targets.
9. Define penetration-testing scope and independence.
10. Define control-verification cadence by environment.
11. Define security exception authority and maximum duration.
12. Define control dashboard and metrics.
13. Define external-framework mapping timing.
14. Define customer-facing assurance evidence.
15. Align control references with final `THR-001` threat identifiers.
16. Align `DAT-002`, `AUD-001`, and `CST-001`.
17. Align Hermes and Codex adapter-specific controls.
18. Confirm accessibility and visual validation for security administration.
19. Confirm security-control treatment during recovery.
20. Confirm annual catalogue review and versioning.

## 146. Risks

| Risk | Consequence | Response |
|---|---|---|
| Catalogue mistaken for implementation | False assurance | Evidence-based status |
| Too many controls too early | Delivery paralysis | Maturity and applicability |
| Controls have no owner | Persistent gaps | Accountable ownership |
| Automated scan treated as complete | Missed design/runtime flaws | Layered verification |
| Evidence becomes stale | False green status | Expiry and cadence |
| Exceptions never expire | Permanent exposure | Time-bounded governance |
| Control IDs drift from threat model | Lost traceability | Global audit |
| Security evidence leaks secrets | Secondary compromise | Minimization and access control |
| All controls shown green despite RB0 failure | Misleading governance | Critical override |
| Vendor-specific controls chosen too early | Lock-in | Provider-neutral direction |
| Local profile presented as commercial | False assurance | Environment-specific applicability |
| Agents attest their own compliance | Untrusted evidence | Independent verification |
| Control automation silently fails | Undetected gap | Health and alerting |
| Catalogue not updated after architecture change | Obsolete baseline | Change-triggered review |

## 147. Assumptions

- `SEC-001` and `THR-001` remain the primary architecture and threat sources.
- `IAM-001`, `POL-001`, and `SAN-001` define major preventive boundaries.
- Security evidence can be stored and access-controlled.
- Build, environment, route, service, and executor identities can be recorded.
- Pilot scope is controlled and smaller than future commercial scope.
- Control automation can be introduced progressively.
- A global document audit will reconcile IDs, dependencies, owners, and statuses.

## 148. Constraints

- no control is reported verified without evidence;
- no `unknown` or failed `RB0` control is treated as acceptable;
- no raw secrets in control evidence;
- no agent or adapter self-certification;
- no permanent unapproved exception;
- no unsupported compliance claim;
- no vendor selection in this draft;
- no control silently removed because implementation is difficult;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## 149. Acceptance criteria

SEC-002 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts release impact and residual-risk governance;
3. Architecture accepts control placement and applicability;
4. Security accepts the complete control set, ownership, evidence, and exception model;
5. Data accepts classification, privacy, evidence, retention, and export controls;
6. Operations accepts monitoring, patching, incident, emergency, and recovery controls;
7. Quality accepts verification, automation, severity, and release gates;
8. every control has an accountable owner;
9. every control maps to threats and architecture;
10. pilot and commercial baselines are approved;
11. evidence storage and integrity are approved;
12. vulnerability and penetration-testing processes are approved;
13. exceptions and compensating controls are approved;
14. the global audit resolves threat IDs and document dependencies;
15. downstream documents can refine evidence and adapter details without changing control intent.

## 150. Downstream impact

| Document | Required use |
|---|---|
| `DAT-002` | Classification, retention, deletion, privacy, and backup controls |
| `AUD-001` | Control evidence, audit integrity, timelines, and exports |
| `CST-001` | Cost abuse, budget, quota, and attribution controls |
| `ADP-HER-001` | Hermes-specific IAM, tool, model, memory, network, and evidence controls |
| `ADP-CDX-001` | Codex-specific repository, command, package, Git, and evidence controls |
| `UXA-001` | Security administration, denial, incident, and recovery journeys |
| `DSN-001` | Security states, banners, findings, and control dashboards |
| `A11Y-001` | Accessible security administration and incident controls |
| `VVR-001` | Security control, exception, alert, and recovery visual scenarios |
| Document register | Add proposed document and dependencies |

## 151. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial security-control catalogue covering governance, assets, IAM, policy, approvals, sandbox, secrets, data, APIs, integrations, supply chain, audit, vulnerabilities, incidents, recovery, and agent-specific controls |

## 152. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SEC-001` — Security Architecture
- `THR-001` — Threat Model
- `IAM-001` — Identity and Access Management Architecture — proposed/unregistered
- `POL-001` — Policy and Permission Architecture — proposed/unregistered
- `SAN-001` — Sandbox and Secure Execution Architecture — proposed/unregistered
- `AUT-001` — Autonomy and Approval Matrix
- `APR-001` — Approval Contract
- `RUN-001` — Run and Execution Contract
- `ART-001` — Artifact Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
- `PLG-001` — Plugin and Extension Architecture
