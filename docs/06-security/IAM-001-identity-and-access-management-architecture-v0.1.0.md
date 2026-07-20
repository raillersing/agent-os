---
document_id: IAM-001
title: Agent OS Identity and Access Management Architecture
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
  - SAD-001
  - DDD-001
  - SEC-001
  - AUT-001
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
  - POL-001
  - SAN-001
  - SEC-002
  - DAT-002
  - AUD-001
related_adrs:
  - ADR-TBD-IAM-001
  - ADR-TBD-IAM-002
  - ADR-TBD-IAM-003
  - ADR-TBD-IAM-004
  - ADR-TBD-IAM-005
  - ADR-TBD-IAM-006
  - ADR-TBD-IAM-007
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# IAM-001 — Agent OS Identity and Access Management Architecture

> **Status: Draft — proposed/unregistered.** This document defines the proposed identity and access management architecture for Agent OS. It covers human and workload identities, organizations and workspaces, authentication, sessions, roles, grants, delegation, reauthentication, service accounts, workload identity, support access, break-glass, invitations, onboarding, offboarding, suspension, revocation, external identity providers, identity evidence, API and event direction, operations, testing, and release gates. It does not define the complete policy language or authorization engine, select a final identity provider, approve production password or MFA policy, or claim enterprise SSO readiness.


## 1. Purpose

Agent OS coordinates consequential work through people, agents, adapters, tools, providers, artifacts, and long-running processes. Every consequential action must be attributable to a valid identity operating within an explicit organization, workspace, role, grant, and session context.

The IAM architecture defines how Agent OS establishes:

1. who or what is acting;
2. how that identity was authenticated;
3. which organization and workspace apply;
4. which permissions and grants are active;
5. whether reauthentication is required;
6. whether delegation is valid;
7. whether approval independence is preserved;
8. how access is suspended or revoked;
9. how emergency access is governed;
10. what evidence proves the access decision.

## 2. Objectives

IAM must:

- provide stable human and workload identity;
- preserve organization and workspace isolation;
- support local-first MVP authentication;
- support future external identity providers;
- separate authentication, authorization, approval, and execution;
- support role-based and attribute-informed access;
- support least privilege;
- support temporary and scoped grants;
- support session and device management;
- support reauthentication for critical actions;
- support rapid revocation;
- support service and workload identities without shared human credentials;
- prevent agent or adapter self-elevation;
- prevent support impersonation without governance;
- support break-glass with strong controls;
- expose access state clearly in the UI;
- produce auditable identity and access evidence;
- remain provider-neutral.

## 3. Non-goals

IAM-001 does not:

- define the complete policy language;
- select final OIDC, SAML, LDAP, passkey, or MFA technology;
- define every business permission;
- authorize agents to approve their own actions;
- authorize anonymous protected access;
- equate authentication with authorization;
- equate a role with unrestricted administration;
- permit shared human accounts;
- permit raw secret storage in IAM records;
- claim enterprise federation readiness;
- define final legal privacy notices;
- replace approval or policy contracts.

## 4. Principle — Identity is explicit

Every protected action has an attributable human or workload identity.

## 5. Principle — Authentication is not authorization

Successful authentication does not imply permission to access a workspace, object, or capability.

## 6. Principle — Authorization is not approval

A permitted action may still require a separate human approval decision.

## 7. Principle — Workspace scope precedes retrieval

Workspace authorization is established before data retrieval, search, ranking, preview, export, or counting.

## 8. Principle — Least privilege

Permissions are narrow, scoped, time-bounded where appropriate, and justified.

## 9. Principle — No self-elevation

Agents, adapters, workloads, and users cannot grant themselves additional authority.

## 10. Principle — Revocation is a negative fact

Suspension, revocation, expiry, and denial survive restore and override stale positive grants.

## 11. Principle — Critical actions require fresh assurance

Sensitive actions may require recent authentication or stronger factors.

## 12. Principle — Service identities are not human substitutes

Workload identities cannot be used as shared human accounts.

## 13. Principle — Break-glass is exceptional

Emergency access is time-bounded, independently approved or reviewed, fully audited, and visible.

## 14. Principle — Identity source is visible

The platform records whether identity is local, federated, service-based, or inferred.

## 15. Principle — Unknown blocks protected access

Unknown session, role, membership, assurance, or revocation state fails closed.

## 16. IAM bounded context

The IAM bounded context owns:

- principals;
- human identities;
- workload identities;
- organizations;
- workspaces;
- memberships;
- roles;
- grants;
- delegations;
- authentication methods;
- sessions;
- devices;
- invitations;
- suspensions;
- revocations;
- break-glass access;
- identity-provider links;
- access evidence.

It does not own the complete policy language, run lifecycle, approval decision, or tool execution.

## 17. Core identity taxonomy

```text
human_identity
workload_identity
agent_profile_identity
adapter_runtime_identity
service_account
external_identity
support_identity
break_glass_identity
device_identity
session_identity
```

## 18. Human identity

Represents a real person with a stable Agent OS subject identifier.

## 19. Workload identity

Represents a non-human runtime, service, worker, or automation component.

## 20. Agent profile identity

Represents the logical Agent OS profile used for assignment and audit; it is not a human identity.

## 21. Adapter runtime identity

Represents a concrete adapter process or deployment instance.

## 22. Service account

A governed workload principal with explicitly assigned grants.

## 23. External identity

A subject asserted by an external identity provider and linked to an Agent OS identity.

## 24. Support identity

A human support operator with constrained diagnostic capabilities.

## 25. Break-glass identity

A controlled emergency identity or emergency grant path.

## 26. Device identity

A known browser or device registration associated with authentication risk and session control.

## 27. Session identity

The authenticated context carrying identity, organization, workspace, assurance, and expiration.

## 28. Identity separation

The following must remain distinct:

```text
person
≠ user account
≠ membership
≠ role
≠ grant
≠ session
≠ approval
≠ agent profile
≠ workload identity
```

One person may have multiple memberships or linked external identities. One session belongs to one authenticated principal and carries only the active scopes granted to it.

## 29. Principal model

A `Principal` is the subject evaluated for access. It records:

- principal ID;
- principal type;
- lifecycle state;
- organization bindings;
- workspace memberships;
- assurance state;
- suspension or revocation state;
- source;
- creation and last verification;
- audit references.

Principal IDs are opaque and stable.

## 30. Human identity model

A human identity may include:

- stable subject ID;
- display name;
- normalized email where used;
- locale;
- timezone;
- status;
- local or federated origin;
- linked identity-provider subjects;
- authentication methods;
- recovery status;
- last successful authentication;
- risk and assurance metadata;
- no raw credential secret.

Personal-data minimization and retention are refined in proposed/unregistered `DAT-002`.

## 31. Workload identity model

A workload identity records:

- workload principal ID;
- component type;
- deployment or instance identity;
- owning organization or platform scope;
- allowed environments;
- certificate, token, or workload-identity reference;
- permitted capabilities;
- grant scope;
- rotation and expiry;
- owner;
- health and revocation state.

It must not reuse a human password or personal API key.

## 32. Agent profile identity

An Agent Profile is a logical profile used for task assignment and visibility. It may reference:

- adapter registration;
- capability set;
- model profile;
- workspace enablement;
- permissions requested through governed execution.

The agent profile cannot authenticate as a human, approve, assign itself a role, or bypass Tool Gateway controls.

## 33. Adapter runtime identity

Each adapter runtime should present a verifiable identity tied to:

- adapter registration;
- version;
- deployment instance;
- environment;
- certificate or workload credential;
- validation state;
- revocation state.

A runtime identity mismatch blocks readiness and protected dispatch.

## 34. Organization model

An `Organization` is the top-level administrative and ownership boundary for:

- people;
- workspaces;
- billing or budget ownership;
- identity-provider configuration;
- high-level security policy;
- audit ownership;
- support agreements;
- commercial tenancy.

The local MVP may operate with one organization while retaining the model explicitly.

## 35. Workspace model

A `Workspace` is the primary operational and data-isolation scope. A workspace owns or scopes:

- projects and tasks;
- runs and approvals;
- artifacts and memory;
- agents and integrations;
- workspace memberships;
- workspace roles and grants;
- budgets;
- retention and classification settings;
- operational visibility.

Workspace authorization must be established before any protected retrieval.

## 36. Organization and workspace invariants

- every workspace belongs to exactly one organization;
- every workspace-scoped object has one authoritative workspace ID;
- cross-workspace access is denied by default;
- organization roles do not automatically imply every workspace permission;
- suspended workspaces block ordinary activity;
- workspace deletion or archival does not erase audit history;
- membership removal revokes future access and active sessions according to policy.

## 37. Membership model

A membership links a human or eligible workload principal to an organization or workspace. It records:

- membership ID;
- principal ID;
- organization/workspace;
- status;
- role assignments;
- temporary grants;
- invitation source;
- start and expiry;
- suspension;
- owner or sponsor;
- evidence.

Membership is not equivalent to authentication.

## 38. Membership states

```text
invited
pending_verification
active
suspended
expired
revoked
left
archived
unknown
```

## 39. Membership state — Invited

An invitation exists but has not been accepted.

## 40. Membership state — Pending verification

Acceptance occurred but required identity or policy checks are incomplete.

## 41. Membership state — Active

Membership may contribute grants subject to policy and session state.

## 42. Membership state — Suspended

Access is temporarily blocked without deleting history.

## 43. Membership state — Expired

Time-bounded membership ended.

## 44. Membership state — Revoked

Membership was explicitly removed and must not be resurrected by stale state.

## 45. Membership state — Left

The member voluntarily left where supported.

## 46. Membership state — Archived

Historical record retained after organization/workspace lifecycle change.

## 47. Membership state — Unknown

Current validity cannot be established; protected access fails closed.

## 48. Authentication architecture

Authentication establishes a principal and assurance context. It may use:

```text
local credential
passkey or platform authenticator
time-based one-time password
recovery code
federated OIDC
federated SAML
client certificate or workload identity
short-lived service token
```

Final mechanisms and policy require ADR.

## 49. MVP authentication direction

For a local MVP, the recommended direction is:

- named local human accounts;
- securely hashed passwords if passwords are used;
- no shared accounts;
- session cookies with secure attributes;
- reauthentication for critical actions;
- optional second factor for security and operations roles where feasible;
- controlled recovery;
- explicit environment and user identity in the UI.

This is a direction, not an approved production policy.

## 50. Password direction

If passwords are supported:

- store only strong password hashes;
- allow password managers and paste;
- avoid arbitrary composition rules that reduce usability;
- screen against known compromised passwords where feasible;
- use rate limiting and lockout controls proportionate to risk;
- protect reset flows;
- never log password values;
- require reauthentication before changing critical account settings.

Exact length, hashing, and lockout policy requires ADR.

## 51. Passkey direction

Passkeys or WebAuthn-style authenticators are a future preferred direction for stronger, phishing-resistant authentication. The system must still provide accessible, governed recovery and device-loss procedures.

## 52. MFA direction

Potential MFA requirements depend on role and environment. Stronger assurance may be required for:

- security owner;
- organization owner;
- operations owner;
- break-glass activation;
- identity-provider changes;
- role/grant changes;
- secret rotation;
- restore and recovery;
- commercial production access.

The final factor policy requires approval.

## 53. Authentication assurance levels

Proposed internal assurance levels:

```text
AAL0 — unauthenticated or unknown
AAL1 — single verified factor
AAL2 — multi-factor or phishing-resistant single ceremony where approved
AAL3 — high-assurance administrative or workload identity with stronger controls
```

These labels are internal design directions and do not claim alignment with a particular external standard until approved.

## 54. Assurance requirements

Every protected request may specify:

- minimum authentication assurance;
- maximum authentication age;
- required reauthentication;
- required device or workload trust;
- prohibited recovery-only credentials;
- required factor type;
- organization or workspace policy.

Unknown assurance fails closed.

## 55. Federation direction

Future federation may support:

- OpenID Connect;
- SAML;
- enterprise directory provisioning;
- organization-domain discovery;
- just-in-time membership under policy;
- explicit account linking;
- centralized revocation.

Federation does not automatically grant workspace membership or roles.

## 56. External identity linking

Linking an external identity to an Agent OS identity requires:

- authenticated proof from the external provider;
- current Agent OS authentication or controlled invitation;
- conflict detection;
- no email-only silent merge;
- audit evidence;
- unlinking and recovery rules;
- protection against account takeover.

One external identity cannot be silently linked to multiple active Agent OS human identities.

## 57. Invitation architecture

Invitations define:

- inviting principal;
- target organization/workspace;
- proposed role or membership;
- recipient identity hint;
- expiration;
- single-use token;
- acceptance conditions;
- identity verification;
- sponsor;
- audit record.

The invitation token itself is not a permanent credential.

## 58. Invitation security

Invitation flows must prevent:

- token reuse;
- role escalation beyond inviter authority;
- email forwarding takeover without verification;
- indefinite validity;
- hidden organization/workspace scope;
- silent creation of privileged accounts;
- leaking membership existence.

High-privilege invitations may require independent approval.

## 59. Session architecture

A session binds:

- session ID;
- principal;
- authentication method;
- assurance level;
- authentication time;
- issue and expiration;
- organization;
- active workspace where applicable;
- device context;
- IP or network context where policy permits;
- revocation state;
- last activity;
- risk state.

Session identifiers are secret-bearing references and must not appear in logs or URLs.

## 60. Session types

```text
interactive_human
api_human
workload
support
break_glass
recovery
```

## 61. Interactive human session

Used for Mission Control. It should rely on secure, HTTP-only, same-site session protection where a browser cookie model is selected.

## 62. API human session

Represents a human-issued API session or token. It must remain attributable to the human identity, have narrow scopes, expiry, revocation, and no use as a permanent automation credential.

## 63. Workload session

Represents a non-human authenticated channel using short-lived workload credentials, certificate identity, or token exchange.

## 64. Support session

Carries constrained support grants, workspace scope, purpose, expiration, and elevated audit.

## 65. Break-glass session

Carries emergency status, reason, scope, short lifetime, stronger assurance, persistent banner, and mandatory post-use review.

## 66. Recovery session

Allows bounded recovery operations while ordinary activity remains blocked. It cannot silently become a normal production session.

## 67. Session lifetime direction

Session policy distinguishes:

- absolute lifetime;
- idle timeout;
- authentication age;
- reauthentication age;
- critical-action freshness;
- workload token lifetime;
- refresh or renewal rules.

Exact durations must be approved per environment and role.

## 68. Session rotation

Session identifiers should rotate after:

- authentication;
- privilege or membership change;
- reauthentication;
- break-glass activation;
- recovery-mode transition;
- suspected fixation;
- account recovery.

Old identifiers become invalid.

## 69. Session revocation

Revocation triggers include:

- logout;
- password or factor reset;
- membership suspension;
- role or grant revocation;
- identity-provider revocation;
- security incident;
- device loss;
- administrative action;
- break-glass completion;
- workload rotation.

Revocation must propagate promptly and remain authoritative over cached authorization.

## 70. Session inventory

Users and administrators should be able to inspect sessions with:

- device or client description;
- approximate location/network where policy permits;
- created and last active;
- assurance;
- active organization/workspace;
- current status;
- revoke action.

Sensitive network data should be minimized.

## 71. Device model

A device record may include:

- device ID;
- human-readable label;
- platform/browser;
- first and last seen;
- trusted or untrusted status;
- passkey association;
- risk indicators;
- revocation;
- no invasive fingerprinting beyond justified need.

Device trust supplements, but does not replace, identity and authorization.

## 72. Reauthentication

Reauthentication confirms recent control of the authenticated identity before a critical action.

Potential triggers:

- role or permission change;
- secret management;
- identity-provider change;
- export of restricted data;
- destructive deletion;
- emergency-stop release;
- restore;
- break-glass activation;
- support impersonation;
- account recovery;
- changing authentication methods.

## 73. Reauthentication UX

The UI must:

- explain why reauthentication is required;
- preserve the exact reviewed context;
- return the user to the same action;
- refresh stale data;
- invalidate the action if material scope changed;
- support keyboard and assistive technology;
- avoid requesting secrets in insecure content areas.

## 74. Roles and grants boundary

IAM owns identity bindings, role assignments, and grant records. Proposed/unregistered `POL-001` will define the complete policy-evaluation model.

The following remain distinct:

```text
role assignment
→ source of candidate permissions

grant
→ explicit scoped authority record

policy decision
→ evaluated allow/deny/approval requirement

approval
→ human decision for one governed action
```

## 75. Role model

A role is a named collection of candidate permissions or responsibilities. Roles may exist at:

```text
platform
organization
workspace
project
resource
```

Broad roles should be minimized.

## 76. Proposed platform roles

Potential platform roles:

```text
platform_operator
platform_security_reviewer
platform_quality_reviewer
platform_support
```

These are design directions, not automatically available roles.

## 77. Proposed organization roles

Potential organization roles:

```text
organization_owner
organization_admin
organization_security_owner
organization_data_owner
organization_billing_owner
organization_auditor
```

## 78. Proposed workspace roles

Potential workspace roles:

```text
workspace_owner
workspace_admin
project_manager
operator
reviewer
security_reviewer
data_reviewer
developer
support_observer
read_only_observer
```

## 79. Role constraints

- roles are scoped;
- assignment requires authority;
- privileged roles may require approval and reauthentication;
- role assignment has source, reason, actor, date, and expiry;
- a role does not bypass approval requirements;
- a role does not bypass workspace isolation;
- agents and adapters cannot receive human governance roles;
- read-only roles cannot mutate through hidden APIs.

## 80. Grant model

A grant records:

- grant ID;
- principal;
- role or explicit permission set;
- organization/workspace/resource scope;
- actions;
- constraints;
- source;
- reason;
- start;
- expiry;
- delegator;
- approval evidence;
- status;
- revocation.

A grant is immutable in material meaning; changes create a new version or superseding record.

## 81. Grant states

```text
proposed
pending_approval
active
suspended
expired
revoked
superseded
invalid
unknown
```

## 82. Temporary grants

Temporary grants must have:

- exact scope;
- explicit reason;
- short expiry;
- owner;
- approval where required;
- visible countdown or expiry;
- automatic expiration;
- no silent renewal.

Expired grants cannot be restored from stale sessions or backups.

## 83. Standing grants

Standing grants are permitted only where justified by recurring responsibility. They require periodic review, owner, scope, evidence, and revocation capability.

## 84. Direct grants

Direct grants to a principal should be exceptional compared with role-based membership. They require justification and review because they are harder to reason about.

## 85. Negative grants and deny

Explicit deny, suspension, revocation, and emergency restrictions override positive grants. Conflict resolution is refined in proposed/unregistered `POL-001`.

## 86. Resource ownership

Resource ownership may contribute authority but does not imply unrestricted permission. Ownership changes must be audited and cannot bypass organization/workspace controls.

## 87. Delegation

Delegation allows an authorized human to grant a bounded portion of their authority to another eligible human principal.

Delegation does not:

- transfer identity;
- permit credential sharing;
- permit the delegate to exceed delegator scope;
- remove approval independence requirements;
- survive delegator revocation automatically.

## 88. Delegation record

A delegation records:

- delegator;
- delegate;
- scope;
- permissions;
- purpose;
- start and expiry;
- re-delegation allowed or prohibited;
- approval;
- constraints;
- status;
- revocation.

Default direction: no re-delegation.

## 89. Delegation independence

A delegate acting under delegated authority remains a distinct human actor. Approval independence is evaluated using both the delegate and original authority source. Delegation cannot be used to approve one's own request through a proxy.

## 90. Service accounts

Service accounts are workload principals for bounded automation. They require:

- named owner;
- business purpose;
- environment;
- workspace scope;
- narrow grants;
- short-lived or rotated credentials;
- no interactive human login;
- usage monitoring;
- last-used visibility;
- expiry or periodic review;
- rapid revocation.

## 91. Service-account anti-patterns

Prohibited or strongly discouraged:

- one service account shared by unrelated systems;
- permanent broad token;
- use by humans;
- no owner;
- no expiry;
- production credential in source code;
- cross-workspace unscoped access;
- hidden use through agent prompts.

## 92. Workload identity direction

Preferred direction:

```text
workload proves runtime identity
→ Agent OS issues or validates short-lived session
→ session receives narrow grants
→ calls are auditable
```

Potential mechanisms include client certificates, platform workload identity, or signed short-lived assertions. Final mechanism requires ADR.

## 93. API tokens

If API tokens exist:

- token values are shown only at creation;
- only hashes or secure references are stored;
- scopes are explicit;
- expiry is required;
- owner and purpose are visible;
- last-used time is visible;
- revocation is immediate;
- tokens cannot silently inherit new roles;
- high-risk scopes require stronger review.

## 94. Personal access tokens

Personal tokens should be limited or avoided for long-running automation. They remain tied to a human and are revoked when the human loses access.

## 95. Support access

Support access should be designed around:

- read-only diagnostics by default;
- exact workspace scope;
- user or owner request where appropriate;
- purpose and ticket/case reference;
- short duration;
- no raw secrets;
- no arbitrary artifact content access;
- visible support banner;
- complete audit;
- user-facing transparency where policy requires.

## 96. Support impersonation

True impersonation is high risk and should be avoided. Preferred patterns:

- support view using the support operator's own identity;
- permission simulation;
- user-context preview without acting as the user;
- explicit, separately governed impersonation only when unavoidable.

If impersonation exists, it must never conceal the support operator's real identity.

## 97. Break-glass architecture

Break-glass provides emergency access when ordinary identity or policy paths are unavailable.

Requirements:

- clearly defined trigger;
- named accountable human;
- stronger authentication;
- exact environment and scope;
- short duration;
- reason and incident reference;
- visible emergency banner;
- immutable audit;
- automatic expiration;
- post-use review;
- credential rotation where applicable.

## 98. Break-glass activation

Potential flow:

1. declare incident or continuity need;
2. identify ordinary access failure;
3. authenticate emergency operator strongly;
4. obtain required approval or dual control where feasible;
5. define exact scope and duration;
6. activate break-glass session;
7. display persistent state;
8. perform bounded actions;
9. terminate session;
10. review all actions and remediate.

## 99. Break-glass prohibitions

Break-glass must not:

- erase logs;
- disable audit;
- impersonate another human invisibly;
- become a normal daily account;
- have indefinite validity;
- automatically bypass approvals unrelated to the incident;
- survive recovery without current validation.

## 100. Account lifecycle

Human account lifecycle:

```text
invited
→ pending_verification
→ active
→ suspended or locked
→ recovered or reactivated
→ deactivated
→ archived
```

Deletion and retention depend on legal and audit requirements.

## 101. Onboarding

Onboarding includes:

- invitation or approved provisioning;
- identity verification;
- organization/workspace membership;
- role assignment;
- required training or policy acknowledgment;
- authentication-method setup;
- recovery setup;
- first sign-in;
- review of active sessions and grants.

High-privilege onboarding receives independent review.

## 102. Offboarding

Offboarding should:

1. suspend or revoke active sessions;
2. remove memberships and grants;
3. revoke personal tokens;
4. transfer owned work;
5. rotate shared external credentials if exposure existed;
6. preserve audit and historical authorship;
7. review delegated authority;
8. notify relevant owners;
9. record completion evidence.

## 103. Suspension

Suspension temporarily blocks authentication or authorization while retaining records. It should propagate to sessions, API tokens, delegations, and workload bindings as applicable.

## 104. Lockout

Lockout is a protective authentication state, not necessarily a membership revocation. Recovery must not silently restore suspended roles or grants.

## 105. Account recovery

Recovery must:

- verify identity using approved methods;
- avoid support-only weak proof;
- invalidate relevant sessions and recovery artifacts;
- rotate compromised factors;
- preserve organization/workspace membership only after checks;
- require reauthentication;
- produce audit evidence.

Recovery codes are secret-bearing and require secure storage.

## 106. Deactivation and archival

Deactivation prevents new access. Archival preserves historical references, approvals, authorship, audit, and receipts. Historical records should display the identity state without rewriting past actor attribution.

## 107. Revocation propagation

Revocation must propagate to:

- active browser sessions;
- API tokens;
- refresh tokens;
- workload sessions;
- service-account credentials;
- delegated grants;
- active support sessions;
- cached policy decisions;
- queued protected actions where revalidation is required.

Long-running runs must be evaluated according to action and effect state rather than blindly terminated or continued.

## 108. Active run behavior after access change

When the requesting or owning principal loses access:

- new protected steps require revalidation;
- existing safe computation may continue only under policy;
- pending approvals remain tied to their original request but reviewer eligibility is rechecked;
- external effects are not retried blindly;
- ownership or operator responsibility may be reassigned;
- evidence preserves the original actor.

## 109. Approval independence and IAM

IAM provides identity, role, membership, and delegation facts used by `APR-001`.

It must support checks such as:

- requester and approver are different eligible humans;
- approver is not acting under a conflicting delegation;
- approver has current membership and role;
- approver session assurance is sufficient;
- approval is not performed by an agent, adapter, workload, or service account;
- suspended or revoked identities cannot approve.

## 110. Human-only actions

Human-only actions include, at minimum:

- approval decisions;
- privileged role assignment;
- break-glass activation or review;
- emergency-stop release;
- acceptance of certain residual risks;
- support impersonation authorization;
- final commercial release decisions.

Exact list is refined in `AUT-001`, `APR-001`, and proposed/unregistered `POL-001`.

## 111. Workspace switching

Workspace switching must:

- clearly display the current workspace;
- refresh or clear workspace-scoped caches;
- reauthorize before retrieval;
- prevent stale data from the prior workspace;
- preserve unsaved drafts only when explicitly scoped;
- show role and environment;
- be keyboard and screen-reader accessible.

The URL or route should preserve workspace context where appropriate without exposing secrets.

## 112. Cross-workspace prevention

Controls include:

- workspace ID in every protected domain record;
- authorization before query;
- workspace-bound sessions or request context;
- scoped cache keys;
- scoped search/index queries;
- scoped artifact URLs;
- scoped event subscriptions;
- negative tests;
- audit on denied cross-workspace attempts.

## 113. Organization switching

Organization switching is higher risk than workspace switching and may require:

- fresh authorization;
- separate identity-provider context;
- cleared caches;
- reauthentication;
- explicit organization indicator;
- no silent role carryover.

## 114. Administrative access

Administrative interfaces must:

- use explicit administrative routes or mode;
- show organization/workspace scope;
- show current role and assurance;
- require reauthentication for critical changes;
- expose change impact;
- preserve old and new values;
- produce audit evidence;
- support rollback or revocation where possible.

## 115. Role assignment workflow

Recommended flow:

1. identify target principal;
2. select exact organization/workspace;
3. select role or grant;
4. show resulting permissions and critical capabilities;
5. show conflicts and independence impact;
6. require reason and expiry;
7. require reauthentication or approval where applicable;
8. persist assignment;
9. rotate/revalidate sessions if needed;
10. record evidence.

## 116. Role-review workflow

Periodic access review should show:

- principal;
- membership;
- roles and direct grants;
- delegations;
- last use;
- active sessions/tokens;
- owner;
- expiry;
- sensitive capabilities;
- keep, narrow, suspend, or revoke decisions.

Review completion is recorded.

## 117. Access certification direction

Pilot or commercial environments may require periodic certification for privileged roles and dormant accounts. Exact cadence and regulatory scope require governance approval.

## 118. Dormant identity handling

Dormant accounts or service accounts may be:

- flagged;
- disabled after a configured period;
- reviewed before reactivation;
- excluded from privileged standing grants;
- preserved historically.

Dormancy thresholds require ADR.

## 119. Concurrent sessions

Policy may limit or monitor concurrent sessions for privileged identities. Forced single-session behavior should not be adopted without usability, accessibility, and operational review.

## 120. Session anomaly handling

Potential anomalies:

- impossible travel or unusual location where appropriate;
- new device;
- repeated failed authentication;
- sudden privilege use;
- session reuse after revocation;
- token use from multiple environments;
- workload identity mismatch.

Risk signals inform policy but do not replace evidence.

## 121. Account enumeration protection

Authentication, invitation, reset, and recovery flows should avoid disclosing whether an account, email, organization, or workspace exists beyond what authorized users need.

## 122. Rate limiting

Authentication-sensitive endpoints require rate limits by:

- principal or candidate identifier;
- IP or network context where appropriate;
- device or client;
- organization;
- endpoint.

Rate limits must avoid easy denial of service against legitimate users and support accessible recovery.

## 123. Credential stuffing and brute force

Controls may include:

- breached-password checks;
- progressive delays;
- risk-based challenges;
- MFA;
- IP reputation where justified;
- alerting;
- account protection;
- no raw password logging.

Exact controls belong in proposed/unregistered `SEC-002`.

## 124. Phishing resistance

High-risk roles should prefer phishing-resistant authentication where feasible. Federation metadata, redirect origins, and login branding must be clear to users.

## 125. Session fixation and CSRF

Browser session architecture must protect against:

- session fixation;
- cross-site request forgery;
- cookie theft;
- mixed-content exposure;
- insecure redirects;
- token leakage in URLs;
- clickjacking.

Exact security controls belong in `SEC-001` and proposed/unregistered `SEC-002`.

## 126. Audit and evidence

IAM evidence includes:

- identity creation and linking;
- authentication success/failure;
- factor enrollment and removal;
- invitation creation and acceptance;
- membership and role changes;
- grant creation and revocation;
- session creation, rotation, and termination;
- support access;
- break-glass use;
- recovery;
- identity-provider changes;
- denied privileged actions.

Detailed evidence architecture belongs in proposed/unregistered `AUD-001`.

## 127. Audit attribution

Every access event records, where applicable:

- actor principal;
- real human identity;
- delegated or support context;
- target principal;
- organization/workspace;
- session;
- authentication method and assurance;
- action;
- result;
- reason;
- source;
- time;
- correlation;
- policy/approval references.

Impersonation must never erase the real actor.

## 128. Access decision evidence

A protected decision should be reconstructable from:

- principal and session;
- memberships;
- roles and grants;
- revocations;
- policy version and result;
- approval requirement;
- target scope;
- time;
- authentication assurance;
- decision outcome.

No raw credential secret is stored in evidence.

## 129. Privacy and minimization

IAM contains personal and security-sensitive data. The architecture should minimize:

- unnecessary profile fields;
- precise location;
- device fingerprinting;
- long-term IP retention;
- copied identity-provider attributes;
- authentication telemetry.

Classification, retention, deletion, and data-subject handling are refined in proposed/unregistered `DAT-002`.

## 130. UI architecture

IAM UI surfaces include:

```text
sign in
account recovery
session management
memberships
roles and grants
invitations
service accounts
identity providers
support access
break-glass
access review
denied-access explanation
```

## 131. Identity presentation

The UI distinguishes:

- human;
- agent;
- adapter;
- service account;
- support operator;
- break-glass session.

Agents must not appear as humans or human approvers.

## 132. Current scope indicators

The shell should show:

- current organization where relevant;
- current workspace;
- current environment;
- current human identity;
- active support or break-glass mode;
- session or reauthentication warnings.

Critical modes use persistent, non-color-only indicators.

## 133. Permission-denied UX

A denial should:

- avoid revealing unauthorized object existence;
- state that access is unavailable;
- identify the required general role or owner only when safe;
- provide support or request-access path;
- include correlation ID;
- preserve the user's current safe context;
- remain accessible.

## 134. Request-access UX

A request-access flow may include:

- requested scope;
- requested role or action;
- reason;
- duration;
- sponsor;
- sensitivity;
- reviewer;
- current status.

A request is not a grant.

## 135. Session-expiry UX

The UI should:

- warn before expiry where appropriate;
- preserve non-sensitive drafts;
- allow accessible reauthentication;
- prevent stale approvals;
- clearly identify expired state;
- avoid silent loss of work.

## 136. Account-recovery UX

Recovery should be:

- clear;
- accessible;
- privacy-safe;
- resistant to enumeration;
- explicit about invalidated sessions;
- explicit about remaining review or delay;
- free from inaccessible CAPTCHA-only steps.

## 137. Role and grant UX

Role/grant views should show:

- exact scope;
- permissions;
- sensitive capabilities;
- source;
- reason;
- start and expiry;
- owner;
- active sessions impacted;
- delegations;
- review history.

Avoid unexplained generic `Admin` labels.

## 138. Break-glass UX

When active, the UI must display:

- emergency mode;
- real actor;
- incident/reference;
- scope;
- expiry;
- blocked/non-blocked actions;
- terminate action;
- audit visibility.

The banner cannot be dismissed while the mode remains active.

## 139. Accessibility requirements

IAM follows proposed/unregistered `A11Y-001`.

Critical requirements include:

- accessible authentication;
- password-manager support;
- keyboard-operable factor setup;
- visible and programmatic labels;
- accessible errors;
- accessible reauthentication;
- accessible role/grant tables;
- no color-only suspension or risk;
- no time limit without warning/recovery;
- screen-reader access to current identity, workspace, and emergency mode.

## 140. API direction

Potential resources:

```text
/principals
/human-identities
/workload-identities
/organizations
/workspaces
/memberships
/roles
/grants
/delegations
/invitations
/sessions
/devices
/service-accounts
/identity-providers
/access-reviews
/support-access
/break-glass-operations
```

## 141. API command direction

Potential commands:

```text
authenticate
reauthenticate
logout
revoke-session
invite-member
accept-invitation
assign-role
revoke-role
create-grant
revoke-grant
delegate
revoke-delegation
suspend-principal
reactivate-principal
link-external-identity
unlink-external-identity
activate-break-glass
terminate-break-glass
```

Clients cannot directly set authoritative lifecycle states.

## 142. API security

IAM APIs require:

- authentication;
- organization/workspace authorization;
- expected-version or ETag for sensitive updates;
- idempotency for consequential commands;
- reauthentication where required;
- audit;
- rate limiting;
- no raw secret response;
- consistent safe error envelopes.

## 143. Event direction

Potential events:

```text
PrincipalCreated
PrincipalSuspended
PrincipalReactivated
PrincipalRevoked
AuthenticationSucceeded
AuthenticationFailed
ReauthenticationCompleted
SessionCreated
SessionRotated
SessionRevoked
InvitationCreated
InvitationAccepted
MembershipActivated
MembershipSuspended
MembershipRevoked
RoleAssigned
RoleRevoked
GrantActivated
GrantExpired
GrantRevoked
DelegationActivated
DelegationRevoked
ServiceAccountCreated
ServiceAccountCredentialRotated
IdentityLinked
IdentityUnlinked
BreakGlassActivated
BreakGlassTerminated
AccessReviewCompleted
```

## 144. Event privacy

Identity events must minimize personal data. Consumers receive references and necessary attributes rather than full profiles or credential data.

## 145. Data model direction

Core entities:

```text
Principal
HumanIdentity
WorkloadIdentity
ExternalIdentityLink
Organization
Workspace
Membership
Role
RolePermission
Grant
Delegation
AuthenticationMethod
Session
Device
Invitation
ServiceAccount
IdentityProvider
AccessReview
SupportAccessGrant
BreakGlassOperation
RevocationRecord
```

## 146. Identifier and uniqueness rules

- principal IDs are opaque and stable;
- normalized email may be unique within an approved scope but is not the primary identity key;
- external identity links are unique by provider and subject;
- workspace membership uniqueness is enforced for active principal/workspace pairs;
- session identifiers are high-entropy secrets;
- invitation tokens are single-use and stored securely;
- service-account names are unique within their scope.

## 147. Consistency and transactions

Sensitive operations should use transactions and optimistic concurrency. Examples:

- role assignment plus evidence;
- invitation acceptance plus membership creation;
- grant revocation plus session invalidation;
- break-glass activation plus audit;
- external identity linking;
- account recovery.

Partial success must be explicit and recoverable.

## 148. Cache and authorization freshness

Authorization caches must include:

- principal;
- organization/workspace;
- role/grant versions;
- revocation version;
- policy version;
- expiry.

Sensitive requests may bypass or revalidate cache. Revocation invalidates affected cache entries.

## 149. Operational states

IAM operational states may include:

```text
normal
degraded_federation
local_only
no_new_sessions
reauthentication_required
break_glass_only
recovery
unknown
```

Fail-open authentication is prohibited.

## 150. Identity-provider outage

During external identity-provider outage:

- new federated authentication may be unavailable;
- existing sessions follow approved lifetime and risk policy;
- privilege expansion is blocked;
- local emergency access may be available only through break-glass;
- the UI shows degraded federation;
- recovery is audited.

No silent fallback to weaker authentication.

## 151. Session-store outage

A session-store outage should fail closed for new protected requests unless a verified architecture provides safe continuity. Cached sessions must not outlive authoritative revocation indefinitely.

## 152. Revocation-store outage

If current revocation cannot be checked, privileged and protected actions are blocked. Read-only continuity may be permitted only under explicit policy.

## 153. Identity restore and disaster recovery

After restore:

- current revocation and suspension facts are reapplied;
- sessions from the backup are invalidated unless explicitly proven safe;
- break-glass state is revalidated;
- identity-provider links are reconciled;
- invitations and recovery tokens are reviewed;
- expired grants remain expired;
- service-account credentials are revalidated or rotated;
- access reviews note the restore.

`BCP-001` and `OPS-001` govern the recovery process.

## 154. Backup scope

IAM backup includes:

- principal and membership records;
- roles and grants;
- delegation;
- identity-provider configuration excluding raw secrets;
- session metadata as required for audit, not necessarily reusable session secrets;
- revocations;
- invitations and recovery-state metadata;
- audit references;
- break-glass records.

Credential secret material follows dedicated secure backup or re-provisioning controls.

## 155. IAM runbooks

Required runbooks:

```text
create and invite user
suspend and reactivate user
offboard user
revoke sessions
recover account
rotate service-account credential
identity-provider outage
federation certificate rotation
role/grant emergency revocation
support access
break-glass activation and review
restore IAM state
investigate unauthorized access
```

## 156. Monitoring

Monitor:

- authentication success and failure;
- lockouts and recovery;
- MFA/passkey enrollment where supported;
- session creation and revocation;
- privileged role changes;
- dormant privileged accounts;
- service-account use;
- support access;
- break-glass activity;
- federation health;
- revocation propagation;
- denied cross-workspace access;
- token age and expiry.

## 157. Alerts

Potential alerts:

```text
authentication_failure_spike
privileged_role_assigned
break_glass_activated
revoked_session_used
service_account_unused_or_overprivileged
identity_provider_unavailable
federation_certificate_expiring
cross_workspace_denial_spike
support_access_active_too_long
revocation_propagation_failed
```

## 158. IAM security incidents

Potential IAM incidents:

- credential compromise;
- account takeover;
- unauthorized role assignment;
- compromised identity provider;
- revoked session still accepted;
- shared account discovery;
- service-account misuse;
- support-access abuse;
- break-glass misuse;
- cross-workspace access;
- identity-linking collision.

## 159. Incident response

IAM incident response should:

1. contain the affected identity or provider;
2. revoke sessions and credentials;
3. preserve evidence;
4. assess memberships, grants, delegations, and affected actions;
5. rotate credentials;
6. notify owners;
7. reconcile approvals and runs;
8. restore trusted authentication;
9. review root cause;
10. update controls and tests.

## 160. Threat considerations

Key threats include:

- brute force and credential stuffing;
- phishing;
- session theft;
- session fixation;
- CSRF;
- account recovery abuse;
- invitation hijacking;
- identity linking collision;
- role escalation;
- confused deputy;
- delegation abuse;
- stale cache after revocation;
- shared service credentials;
- compromised federation metadata;
- support impersonation abuse;
- break-glass normalization.

Detailed mappings belong in `THR-001` and proposed/unregistered `SEC-002`.

## 161. Test strategy

IAM testing includes:

```text
unit
property
schema
authentication integration
session lifecycle
authorization integration
role/grant
delegation
revocation
federation contract
support access
break-glass
cross-workspace
accessibility
performance
fault injection
restore
security abuse
```

## 162. Authentication tests

Test:

- valid and invalid credentials;
- password manager compatibility;
- rate limits;
- lockout and recovery;
- factor enrollment/removal;
- reauthentication;
- session rotation;
- account enumeration protection;
- accessible error paths;
- federation success/failure.

## 163. Session tests

Test:

- absolute and idle expiry;
- logout;
- session rotation;
- concurrent sessions;
- revocation propagation;
- membership suspension;
- role change;
- device removal;
- restore invalidation;
- cookie attributes;
- no token in URL or logs.

## 164. Role and grant tests

Test:

- correct scope;
- privilege boundaries;
- expiry;
- revocation;
- direct grants;
- conflicting denies;
- unauthorized assignment;
- optimistic concurrency;
- session revalidation;
- role display and explanation.

## 165. Delegation tests

Test:

- delegator scope;
- delegate eligibility;
- expiry;
- no re-delegation by default;
- revocation;
- approval independence;
- delegator suspension;
- audit attribution.

## 166. Cross-workspace tests

For every protected entity:

1. create data in workspace A;
2. authenticate a principal limited to workspace B;
3. attempt direct retrieval, search, count, export, event subscription, artifact access, and mutation;
4. verify safe denial and no metadata leakage;
5. repeat with stale cache and revoked membership.

## 167. Service-account tests

Test:

- no interactive login;
- narrow scopes;
- credential rotation;
- expiry;
- workspace isolation;
- last-used visibility;
- revoked credential rejection;
- owner removal;
- no human-role assignment.

## 168. Support and break-glass tests

Test:

- exact scope;
- visible mode;
- expiry;
- reauthentication;
- audit;
- prohibited actions;
- session termination;
- post-use review;
- restore behavior;
- no hidden impersonation.

## 169. Federation tests

Test:

- metadata and certificate validation;
- issuer and audience;
- subject uniqueness;
- account linking;
- deprovisioning;
- attribute changes;
- provider outage;
- clock skew;
- replay;
- logout/revocation behavior;
- no automatic privileged role from untrusted claims.

## 170. Accessibility tests

Critical flows require keyboard and screen-reader testing for:

- sign in;
- account recovery;
- session inventory;
- invitation acceptance;
- role assignment;
- request access;
- reauthentication;
- support access;
- break-glass;
- denial messages.

Requirements are refined in proposed/unregistered `A11Y-001`.

## 171. Visual validation

Proposed/unregistered `VVR-001` should include:

- signed-out and signed-in shells;
- session expiring;
- session revoked;
- reauthentication;
- permission denied;
- invitation states;
- role and grant tables;
- service-account details;
- support mode;
- break-glass banner;
- identity-provider outage;
- workspace switching at required widths and themes.

## 172. Performance and scale direction

IAM performance should support:

- fast session validation;
- bounded role/grant evaluation inputs;
- revocation propagation;
- organization/workspace member lists;
- access-review reporting;
- high-volume authentication logs without slowing login.

Exact targets remain in `NFR-001` or future performance profiles.

## 173. MVP scope

Recommended MVP IAM scope:

- one organization model;
- multiple workspaces;
- named local human accounts;
- secure sessions;
- organization/workspace membership;
- bounded workspace roles;
- role/grant audit;
- reauthentication for critical actions;
- session revocation;
- one or more workload identities for internal services;
- no shared accounts;
- no full enterprise federation requirement;
- no public self-service registration.

## 174. Pilot scope

Before pilot:

- privileged identities are named;
- session and revocation flows are tested;
- onboarding and offboarding runbooks exist;
- role matrix is approved;
- cross-workspace tests pass;
- break-glass process is exercised;
- support access is bounded;
- local recovery works;
- federation, if used, is tested and documented;
- no critical IAM defect remains.

## 175. Controlled-commercial scope

A controlled commercial profile may require:

- enterprise federation;
- MFA or phishing-resistant authentication for privileged roles;
- automated provisioning/deprovisioning;
- periodic access certification;
- stronger workload identity;
- customer-admin boundaries;
- documented support access;
- security notification;
- approved session and retention policy;
- external review.

## 176. IAM maturity stages

```text
I0 — local named identities and sessions
I1 — workspace roles, grants, revocation, and service identities
I2 — pilot federation, MFA, access review, and break-glass
I3 — controlled commercial SSO/provisioning and stronger governance
I4 — mature multi-tenant IAM programme
```

## 177. Requirement catalogue — Identity and tenancy

- `IAM-REQ-IDN-001` — Every protected action has an attributable principal.
- `IAM-REQ-IDN-002` — Human and workload identities are distinct.
- `IAM-REQ-IDN-003` — Agent and adapter identities cannot act as human approvers.
- `IAM-REQ-IDN-004` — Principal IDs are stable and opaque.
- `IAM-REQ-IDN-005` — Every workspace belongs to one organization.
- `IAM-REQ-IDN-006` — Workspace authorization precedes protected retrieval.
- `IAM-REQ-IDN-007` — Cross-workspace access is denied by default.
- `IAM-REQ-IDN-008` — Suspension and revocation survive restore.
- `IAM-REQ-IDN-009` — Historical attribution survives account deactivation.
- `IAM-REQ-IDN-010` — External identity linking is explicit and audited.
- `IAM-REQ-IDN-011` — Unknown identity or membership state fails closed.
- `IAM-REQ-IDN-012` — Organization and workspace scope are visible in critical UI.

## 178. Requirement catalogue — Authentication and sessions

- `IAM-REQ-AUT-001` — Authentication is separate from authorization.
- `IAM-REQ-AUT-002` — Shared human accounts are prohibited.
- `IAM-REQ-AUT-003` — Credentials are stored only in approved protected form.
- `IAM-REQ-AUT-004` — Session identifiers do not appear in URLs or logs.
- `IAM-REQ-AUT-005` — Session rotation occurs after material assurance changes.
- `IAM-REQ-AUT-006` — Critical actions may require recent reauthentication.
- `IAM-REQ-AUT-007` — Revoked sessions are rejected.
- `IAM-REQ-AUT-008` — Session expiry and authentication age are explicit.
- `IAM-REQ-AUT-009` — Authentication errors avoid account enumeration.
- `IAM-REQ-AUT-010` — Recovery invalidates relevant sessions and factors.
- `IAM-REQ-AUT-011` — Federated login does not automatically create privileged membership.
- `IAM-REQ-AUT-012` — Identity-provider outage never triggers silent weaker authentication.

## 179. Requirement catalogue — Roles, grants, and delegation

- `IAM-REQ-GRT-001` — Roles are scoped and do not imply global administration.
- `IAM-REQ-GRT-002` — Grants record scope, source, reason, start, expiry, and revocation.
- `IAM-REQ-GRT-003` — Temporary grants expire automatically.
- `IAM-REQ-GRT-004` — Negative grants, suspension, and revocation override stale positive authority.
- `IAM-REQ-GRT-005` — Privileged assignments require reauthentication or approval where defined.
- `IAM-REQ-GRT-006` — Agents and workloads cannot self-elevate.
- `IAM-REQ-GRT-007` — Delegation cannot exceed delegator scope.
- `IAM-REQ-GRT-008` — Delegation preserves real actor attribution.
- `IAM-REQ-GRT-009` — Delegation cannot defeat approval independence.
- `IAM-REQ-GRT-010` — Direct grants are visible and reviewable.
- `IAM-REQ-GRT-011` — Role and grant changes invalidate affected authorization caches.
- `IAM-REQ-GRT-012` — Expired grants cannot be restored from stale sessions or backups.

## 180. Requirement catalogue — Workloads and emergency access

- `IAM-REQ-WRK-001` — Service accounts have named owners and purposes.
- `IAM-REQ-WRK-002` — Workload credentials are narrow, rotated, and revocable.
- `IAM-REQ-WRK-003` — Service accounts cannot perform interactive human login.
- `IAM-REQ-WRK-004` — Personal tokens are not used as permanent shared automation credentials.
- `IAM-REQ-WRK-005` — Adapter runtime identity is verified before protected dispatch.
- `IAM-REQ-WRK-006` — Support access is scoped, temporary, and audited.
- `IAM-REQ-WRK-007` — Impersonation never hides the real support operator.
- `IAM-REQ-WRK-008` — Break-glass is time-bounded and visible.
- `IAM-REQ-WRK-009` — Break-glass cannot disable audit.
- `IAM-REQ-WRK-010` — Break-glass use receives mandatory post-use review.
- `IAM-REQ-WRK-011` — Recovery sessions cannot silently become ordinary sessions.
- `IAM-REQ-WRK-012` — Current revocation state overrides restored positive access.

## 181. Requirement catalogue — Operations, evidence, and quality

- `IAM-REQ-OPS-001` — IAM changes produce auditable evidence.
- `IAM-REQ-OPS-002` — Revocation propagates to sessions, tokens, grants, and caches.
- `IAM-REQ-OPS-003` — Identity-provider, session-store, and revocation-store outages have fail-closed behavior.
- `IAM-REQ-OPS-004` — IAM backup excludes ordinary raw secret values.
- `IAM-REQ-OPS-005` — IAM restore invalidates unproven sessions.
- `IAM-REQ-OPS-006` — Privileged access is periodically reviewable.
- `IAM-REQ-OPS-007` — Critical IAM flows are accessible.
- `IAM-REQ-OPS-008` — Cross-workspace access receives negative tests.
- `IAM-REQ-OPS-009` — Break-glass and support access have runbooks.
- `IAM-REQ-OPS-010` — Critical IAM findings block release.
- `IAM-REQ-OPS-011` — IAM evidence is tied to build, environment, actor, scope, and time.
- `IAM-REQ-OPS-012` — IAM exceptions are time-bounded and approved.

## 182. Traceability

| Source | IAM-001 response |
|---|---|
| `SCP-001` | Local-first, workspace-oriented scope |
| `PER-001` | Human, operator, reviewer, support, and developer needs |
| `SRS-001` | Authentication, membership, role, and session functions |
| `NFR-001` | Security, privacy, reliability, accessibility, performance |
| `AUT-001` | Human-only actions and approval boundaries |
| `SAD-001` | Identity and access components |
| `DDD-001` | Principal, organization, workspace, membership, and grant model |
| `DAT-001` | IAM data, retention, restore, and deletion |
| `SEC-001` | Authentication, session, secrets, federation, and emergency controls |
| `THR-001` | IAM threats and abuse cases |
| `RUN-001` | Identity changes during active runs |
| `APR-001` | Approver eligibility and independence |
| `API-001` | Resource and command API direction |
| `EVT-001` | IAM event direction |
| `OPS-001` | IAM operations, recovery, and incidents |
| `BCP-001` | IAM continuity and restore |
| `PLG-001` | Extension and workload identity |

## 183. ADR-TBD-IAM-001 — Human authentication and session model

Select local authentication, session cookie/token model, password/passkey direction, timeouts, renewal, and reauthentication.

## 184. ADR-TBD-IAM-002 — Organization, workspace, role, and grant model

Approve tenancy boundaries, role hierarchy, direct grants, expiry, delegation, and access-review model.

## 185. ADR-TBD-IAM-003 — Federation and account linking

Select OIDC/SAML direction, identity-provider metadata, account linking, provisioning, and deprovisioning.

## 186. ADR-TBD-IAM-004 — Workload identity and service credentials

Select service-account, certificate, workload assertion, token exchange, rotation, and ownership model.

## 187. ADR-TBD-IAM-005 — Support access and break-glass

Approve support diagnostic access, impersonation prohibition or controls, emergency authentication, dual control, visibility, and review.

## 188. ADR-TBD-IAM-006 — Revocation, caching, and continuity

Define revocation propagation, cache invalidation, session-store behavior, restore, and fail-closed modes.

## 189. ADR-TBD-IAM-007 — IAM evidence, retention, and access certification

Define audit schema, privacy minimization, retention, access reviews, certification cadence, and evidence exports.

## 190. Open decisions

1. Confirm `IAM-001` registration.
2. Confirm organization and workspace tenancy model.
3. Approve initial human roles.
4. Approve role-assignment authority.
5. Decide local password policy.
6. Decide passkey and MFA timing.
7. Approve session lifetime and idle timeout.
8. Approve reauthentication triggers and maximum age.
9. Decide concurrent-session policy.
10. Select external federation direction.
11. Define account-linking rules.
12. Decide automated provisioning/deprovisioning.
13. Define service-account and workload-identity mechanism.
14. Define personal API token policy.
15. Define temporary grant defaults and maximum duration.
16. Define delegation and re-delegation policy.
17. Define support-access model.
18. Decide whether any true impersonation is allowed.
19. Define break-glass authentication, approval, and expiry.
20. Define revocation propagation objective.
21. Define access-review cadence.
22. Define dormant-account handling.
23. Define identity data retention.
24. Confirm browser and accessibility support for authentication.
25. Define IAM release blockers and exceptions.

## 191. Risks

| Risk | Consequence | Response |
|---|---|---|
| Authentication treated as authorization | Unauthorized access | Separate stages |
| Broad workspace owner role | Excess privilege | Scoped roles and review |
| Email-only account linking | Account takeover | Explicit verified linking |
| Revocation cache stale | Continued access | Versioned invalidation |
| Shared service account | Lost attribution | Named workload identities |
| Personal token used by automation | Offboarding failure | Service accounts |
| Support impersonation hidden | Abuse and trust loss | Real actor preserved |
| Break-glass becomes routine | Control bypass | Short duration and review |
| Federation outage fails open | Compromise | Fail closed |
| Restored sessions remain valid | Unauthorized access | Invalidate/revalidate |
| Delegation defeats independence | Self-approval | Independence checks |
| Direct grants accumulate | Access sprawl | Access review |
| Recovery weakens identity proof | Account takeover | Strong recovery ceremony |
| Device fingerprinting excessive | Privacy issue | Data minimization |
| Session timeout inaccessible | User exclusion/data loss | Accessible warning/recovery |
| Agent shown as human | Misattribution | Distinct identity presentation |
| Unknown membership accepted | Cross-workspace leak | Fail closed |
| Invitation forwarded | Unauthorized membership | Verification and expiry |
| IAM too complex for MVP | Delivery delay | Maturity stages |

## 192. Assumptions

- Agent OS has a browser-based Mission Control.
- Workspace is the primary operational isolation boundary.
- One-organization local deployments remain possible.
- Backend services can enforce workspace scope before retrieval.
- Session and revocation state can be stored durably.
- Privileged actions can require reauthentication.
- Human and workload identities can be represented separately.
- Policy evaluation and approval remain separate contracts.
- IAM evidence can be retained without raw credentials.
- Enterprise federation can be deferred from the first local MVP.

## 193. Constraints

- no shared human accounts;
- no anonymous protected access;
- no agent, adapter, or service account acting as a human approver;
- no raw password, session token, recovery code, or API token in logs;
- no role self-assignment or self-elevation;
- no workspace data retrieval before authorization;
- no silent fallback to weaker authentication;
- no break-glass without visible state and audit;
- no restore that revives expired or revoked access;
- no unsupported enterprise SSO claim;
- no final identity provider selected in this draft;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## 194. Acceptance criteria

IAM-001 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts user, organization, workspace, support, and recovery journeys;
3. Architecture accepts principal, membership, session, grant, and federation boundaries;
4. Security accepts authentication, reauthentication, service identities, support access, break-glass, and revocation;
5. Data accepts identity-data minimization, retention, restore, and historical attribution;
6. Operations accepts onboarding, offboarding, incident, outage, and break-glass runbooks;
7. Quality accepts test coverage, cross-workspace controls, evidence, exceptions, and release gates;
8. the role and grant model is approved;
9. session and reauthentication policy is approved;
10. workload-identity direction is approved;
11. support and break-glass models are approved;
12. revocation and restore behavior is approved;
13. cross-workspace negative tests are accepted;
14. accessibility and visual scenarios are accepted;
15. proposed/unregistered `POL-001`, `SEC-002`, `DAT-002`, and `AUD-001` can refine their domains without changing IAM invariants.

## 195. Downstream impact

| Document | Required use |
|---|---|
| `POL-001` | Policy evaluation, deny precedence, attributes, and explanation |
| `SAN-001` | Workload identity inside sandboxes and execution contexts |
| `SEC-002` | Authentication, session, federation, and revocation control catalogue |
| `DAT-002` | Identity classification, retention, deletion, and privacy |
| `AUD-001` | Authentication, role, grant, support, and break-glass evidence |
| `CST-001` | Organization/workspace budget-owner and billing-role boundaries |
| `ADP-HER-001` | Hermes adapter runtime and workload identity |
| `ADP-CDX-001` | Codex adapter runtime, repository identity, and Git attribution |
| `UXA-001` | Identity, session, denial, and support journeys |
| `DSN-001` | Identity, role, emergency, and session components |
| `A11Y-001` | Accessible authentication and role/grant management |
| `VVR-001` | Identity and access visual scenarios |
| Document register | Add proposed document and dependencies |

## 196. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial IAM architecture covering principals, people, workloads, organizations, workspaces, memberships, authentication, sessions, roles, grants, delegation, service accounts, federation, invitations, onboarding, offboarding, support access, break-glass, revocation, evidence, operations, testing, and release gates |

## 197. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `SAD-001` — System Architecture Description
- `DDD-001` — Domain Model
- `SEC-001` — Security Architecture
- `AUT-001` — Autonomy and Approval Matrix
- `THR-001` — Threat Model
- `APR-001` — Approval Contract
- `API-001` — API Specification
- `EVT-001` — Event Catalog and Async Contract
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
- `PLG-001` — Plugin and Extension Architecture
- `UXA-001` — UX Architecture and User Journey Specification — proposed/unregistered
- `A11Y-001` — Accessibility Requirements and Conformance Plan — proposed/unregistered
- `VVR-001` — Visual Validation and Regression Plan — proposed/unregistered
