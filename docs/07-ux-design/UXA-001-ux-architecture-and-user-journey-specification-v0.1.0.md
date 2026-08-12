---
document_id: UXA-001
title: Agent OS UX Architecture and User Journey Specification
version: 0.1.0
status: draft
register_status: proposed_unregistered
owner: product-owner
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
  - PER-001
  - UCD-001
  - SCP-001
  - PRD-001
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
  - DSN-001
  - A11Y-001
  - VVR-001
  - UIF-001
related_adrs:
  - ADR-TBD-UXA-001
  - ADR-TBD-UXA-002
  - ADR-TBD-UXA-003
  - ADR-TBD-UXA-004
  - ADR-TBD-UXA-005
related_evidence:
  - VIDEO-002
  - VIDEO-003
  - VIDEO-004
---

# UXA-001 — Agent OS UX Architecture and User Journey Specification

> **Status: Draft — proposed/unregistered.** This document defines the user-experience architecture for Agent OS: audiences, information architecture, navigation, Mission Control, workspaces, tasks, runs, approvals, artifacts, memory, adapters, models, operations, system states, trust cues, responsive behavior, accessibility direction, error recovery, and end-to-end journeys. It does not define the final visual design system, final accessibility acceptance procedure, visual-regression tooling, branding, implementation framework, or production UI technology.

## 1. Purpose

Agent OS is not a conventional chat interface.

It is a governed control plane for:

- workspaces;
- people;
- agents;
- tasks;
- durable runs;
- approvals;
- artifacts;
- memory;
- tools;
- integrations;
- operations;
- evidence.

The UX must help users understand:

1. what the system is doing;
2. why it is doing it;
3. which agent, adapter, model, or tool is involved;
4. what is authoritative;
5. what remains unknown;
6. what requires human action;
7. what effect may occur;
8. whether an effect is reversible;
9. what evidence exists;
10. how to recover safely.

## 2. UX objectives

The experience must:

- make complex orchestration understandable;
- separate intent, execution, evidence, and outcome;
- make risk visible without overwhelming users;
- prevent accidental approval;
- preserve workspace context;
- make stale and unknown states explicit;
- support both expert and non-expert users;
- offer clear operational recovery paths;
- avoid dead controls and mock success;
- remain useful on desktop and constrained mobile widths;
- support keyboard and assistive technology;
- disclose source, freshness, and confidence;
- keep sensitive content minimized;
- preserve auditability;
- enable visual verification;
- scale from local MVP to controlled pilot.

## 3. Non-goals

This document does not:

- define final color tokens;
- define final typography;
- define final component APIs;
- define final illustration style;
- define final brand identity;
- authorize UI-only security controls;
- replace backend authorization;
- replace approval contracts;
- guarantee that all workflows fit on mobile;
- make every advanced operation one click;
- hide complexity where it affects safety;
- turn Agent OS into a generic chat product;
- treat dashboards as authoritative state.

## 4. Core UX principles

### `UXA-P-001 — Control before convenience`

The interface should never make a consequential action easier by obscuring risk, scope, or approval.

### `UXA-P-002 — State before decoration`

Current state, freshness, source, limitations, and required action take priority over visual ornament.

### `UXA-P-003 — Intent, execution, and result are distinct`

The UI must not collapse:

```text
requested
accepted
queued
started
completed
failed
cancelled
unknown
```

### `UXA-P-004 — Unknown is visible`

Unknown, stale, partial, degraded, conflicted, and unavailable are first-class UI states.

### `UXA-P-005 — The workspace is the primary scope`

Users should always know which workspace they are operating in.

### `UXA-P-006 — Human approval is deliberate`

Approval screens require exact review material, explicit action, and accessible confirmation.

### `UXA-P-007 — Evidence supports trust`

The interface should link claims to receipts, events, artifacts, approvals, and source metadata.

### `UXA-P-008 — Progressive disclosure`

The interface reveals complexity in layers while keeping critical risk and state always visible.

### `UXA-P-009 — Recovery is designed`

Error states include safe next actions, not only error messages.

### `UXA-P-010 — Accessible by default`

Keyboard, screen-reader, contrast, reflow, semantics, and reduced-motion needs are part of architecture.

### `UXA-P-011 — Mobile is bounded, not deceptive`

On small screens, the UI may restrict high-density operations, but it must not hide essential state or present incomplete review as complete.

### `UXA-P-012 — No dead UI`

Every visible control must be connected, disabled with explanation, or clearly marked as future/demo.

## 5. Experience layers

Agent OS UX has five layers:

```text
orientation
work management
execution control
evidence and review
operations and governance
```

## 6. Orientation layer

Answers:

- Where am I?
- Which workspace?
- Which environment?
- Which role?
- Is the system healthy?
- Is emergency stop active?
- What requires my attention?

## 7. Work-management layer

Supports:

- projects;
- goals;
- tasks;
- queues;
- priorities;
- assignments;
- templates;
- planning.

## 8. Execution-control layer

Supports:

- run creation;
- preflight;
- steps;
- attempts;
- adapters;
- models;
- tools;
- cancellation;
- pause/resume where supported;
- recovery.

## 9. Evidence-and-review layer

Supports:

- approvals;
- artifacts;
- receipts;
- timelines;
- provenance;
- source/freshness;
- acceptance/rejection;
- audit.

## 10. Operations-and-governance layer

Supports:

- adapters;
- model profiles;
- policies;
- budgets;
- alerts;
- backups;
- recovery;
- maintenance;
- access;
- extension lifecycle.

## 11. Primary audiences

```text
product_owner
workspace_owner
operator
reviewer
security_reviewer
data_reviewer
developer
support_operator
read_only_observer
pilot_user
```

## 12. Product Owner

Needs:

- product goals;
- roadmap;
- active work;
- outcomes;
- risks;
- approvals;
- costs;
- pilot status;
- release readiness.

## 13. Workspace Owner

Needs:

- members;
- agents;
- tools;
- policies;
- budgets;
- work queues;
- workspace health;
- data scope.

## 14. Operator

Needs:

- runs;
- queues;
- stale/unknown states;
- adapters;
- providers;
- alerts;
- recovery actions;
- evidence.

## 15. Reviewer

Needs:

- exact approval scope;
- material changes;
- risk;
- source;
- target;
- expiration;
- alternatives;
- accept/reject/revise.

## 16. Security Reviewer

Needs:

- identity;
- permissions;
- secrets;
- network/filesystem;
- data disclosure;
- side effects;
- threat indicators;
- audit evidence.

## 17. Data Reviewer

Needs:

- source;
- classification;
- retention;
- deletion;
- provenance;
- schema;
- export;
- backup implications.

## 18. Developer

Needs:

- tasks;
- branch/worktree;
- diffs;
- test/build evidence;
- Codex runs;
- artifacts;
- approvals;
- Git boundaries.

## 19. Support Operator

Needs:

- workspace-safe diagnostics;
- correlation;
- build/environment;
- known issues;
- user-facing guidance;
- escalation.

## 20. Read-only Observer

Needs:

- current state;
- history;
- artifacts;
- receipts;
- no mutation controls.

## 21. Pilot User

Needs:

- simple orientation;
- clear tasks;
- understandable run status;
- explicit limitations;
- support access;
- minimal technical jargon.

## 22. Experience modes

The interface may adapt to:

```text
standard
review
operations
security
developer
read_only
recovery
maintenance
```

Modes do not replace role authorization.

## 23. Standard mode

Default workspace experience for task and run management.

## 24. Review mode

Optimized for approvals, artifacts, evidence, and decision comparison.

## 25. Operations mode

Optimized for queues, health, stale/unknown runs, adapters, alerts, and recovery.

## 26. Security mode

Optimized for access, policy, secrets, events, findings, and control failures.

## 27. Developer mode

Optimized for repositories, diffs, tests, build artifacts, and adapter traces.

## 28. Read-only mode

Removes or disables mutation controls and highlights historical/evidence views.

## 29. Recovery mode

Prioritizes reconciliation, last reliable evidence, blocked actions, and recovery decisions.

## 30. Maintenance mode

Communicates impact, duration, available features, and operator ownership.

## 31. Global information architecture

Recommended top-level architecture:

```text
Home
Work
Runs
Approvals
Artifacts
Memory
Agents
Integrations
Operations
Settings
```

## 32. Home

Purpose:

- orientation;
- attention;
- current state;
- recent work;
- risks;
- quick actions.

## 33. Work

Contains:

- goals;
- projects;
- tasks;
- queues;
- boards;
- templates.

## 34. Runs

Contains:

- active runs;
- waiting;
- blocked;
- stale;
- unknown;
- completed;
- recovery-required.

## 35. Approvals

Contains:

- my review queue;
- expiring;
- high-risk;
- revised;
- consumed;
- history.

## 36. Artifacts

Contains:

- proposed;
- processing;
- review;
- accepted;
- rejected;
- quarantined;
- exported;
- deleted.

## 37. Memory

Contains:

- proposed;
- verified;
- disputed;
- conflicted;
- stale;
- expired;
- deleted;
- sources.

## 38. Agents

Contains:

- agent profiles;
- adapters;
- capabilities;
- readiness;
- workspaces;
- limitations.

## 39. Integrations

Contains:

- providers;
- tools;
- MCP servers;
- external services;
- secrets references;
- health;
- data access.

## 40. Operations

Contains:

- health;
- alerts;
- events and queues;
- backups;
- restores;
- maintenance;
- incidents;
- diagnostics.

## 41. Settings

Contains:

- workspace;
- members;
- roles;
- policies;
- budgets;
- retention;
- appearance;
- notifications;
- extensions.

## 42. Global shell

The shell should include:

- workspace switcher;
- primary navigation;
- page title;
- breadcrumb or journey path;
- environment indicator;
- global search;
- attention center;
- user menu;
- emergency/maintenance banner;
- help/support entry.

## 43. Workspace switcher

Requirements:

- current workspace always visible;
- accessible label;
- recent workspaces;
- search;
- status;
- role;
- suspended/archived states;
- no cross-workspace data preview before selection.

## 44. Environment indicator

Shows:

- development;
- test;
- pilot;
- controlled commercial;
- maintenance;
- recovery.

It must be visually persistent in non-production-like environments to prevent confusion.

## 45. Global attention center

Aggregates:

- approvals;
- stale runs;
- unknown effects;
- failed artifacts;
- expiring credentials;
- budget warnings;
- critical alerts.

It must preserve workspace and role scope.

## 46. Global search

Searches:

- tasks;
- runs;
- artifacts;
- agents;
- approvals;
- memory;
- operations records.

Results show:

- type;
- workspace;
- state;
- freshness;
- source;
- authorization-safe snippet.

## 47. Search safety

- authorization before retrieval;
- no hidden cross-workspace counts;
- no sensitive snippet leakage;
- stale index label;
- direct source fallback where safe;
- unknown/unavailable state.

## 48. Breadcrumb model

Breadcrumbs show current hierarchy, not a fixed full sitemap.

Example:

```text
Workspace
› Project
› Task
› Run
› Attempt
```

Users may navigate upward to visited parents without exposing unrelated destinations.

## 49. Journey path

For complex workflows, show a contextual path:

```text
Task
→ Preflight
→ Run
→ Approval
→ Execution
→ Artifact
→ Review
→ Receipt
```

Current and completed stages are distinct.

## 50. Navigation behavior

- keyboard accessible;
- persistent current location;
- no hidden essential routes;
- mobile drawer;
- collapsed desktop state;
- clear active item;
- no ambiguous icon-only actions without labels.

## 51. Home dashboard

Recommended sections:

```text
system state
my attention
active work
recent outcomes
workspace health
cost and budget
activity
```

## 52. System-state card

Shows:

- environment;
- health;
- readiness;
- maintenance/emergency stop;
- freshness;
- limitations.

## 53. My-attention queue

Shows:

- approvals;
- revisions;
- failed/stale runs;
- artifacts requiring review;
- expiring items.

Priority must reflect risk and deadline, not only recency.

## 54. Active-work view

Shows:

- goals/projects;
- tasks;
- active runs;
- assigned agents;
- blockers;
- last activity.

## 55. Recent-outcomes view

Shows:

- completed runs;
- accepted artifacts;
- rejected outputs;
- resolved incidents;
- receipts.

## 56. Workspace-health view

Shows:

- adapters;
- providers;
- policies;
- budget;
- storage;
- backup;
- open incidents.

## 57. Dashboard density

Provide:

```text
comfortable
compact
```

Critical labels and accessible names remain in both.

## 58. Empty dashboard state

Should:

- explain why it is empty;
- provide the safest next action;
- avoid fake sample metrics unless explicitly in demo mode;
- link to onboarding or templates.

## 59. Work architecture

Work hierarchy:

```text
Goal
→ Project
→ Task
→ TaskSnapshot
→ Run
```

## 60. Goal experience

Goal view includes:

- outcome;
- owner;
- success criteria;
- linked projects;
- risk;
- progress source;
- last review;
- status.

## 61. Project experience

Project view includes:

- purpose;
- goals;
- members;
- tasks;
- artifacts;
- runs;
- decisions;
- timeline;
- budget;
- risks.

## 62. Task list

Columns or card fields:

- title;
- project;
- priority;
- assignee;
- readiness;
- risk;
- current run;
- last activity;
- due date;
- blockers.

## 63. Task board

Potential states:

```text
backlog
planned
ready
running
waiting
blocked
review
done
cancelled
```

Board state is not identical to run state.

## 64. Task detail

Sections:

- overview;
- requirements;
- inputs;
- acceptance criteria;
- dependencies;
- assigned agent;
- model profile;
- tool scope;
- approvals;
- runs;
- artifacts;
- timeline.

## 65. Task creation

Flow:

1. choose project/goal;
2. define objective;
3. define scope and exclusions;
4. attach inputs;
5. define expected outputs;
6. choose agent/profile;
7. set constraints;
8. review risk/preflight;
9. create task;
10. create snapshot when ready.

## 66. Task draft

A draft can change.

It is clearly distinct from immutable `TaskSnapshot`.

## 67. TaskSnapshot UX

Shows:

- version;
- created by;
- created at;
- source task;
- immutable marker;
- scope;
- inputs;
- approvals expected;
- hash/reference;
- comparison with newer task version.

## 68. Task readiness

Readiness dimensions:

```text
requirements
inputs
permissions
agent
capabilities
model
budget
policy
dependencies
```

## 69. Ready state

A task is ready only when all required dimensions pass.

The UI must identify incomplete dimensions.

## 70. Run creation

The run creation action should:

- identify exact task snapshot;
- show agent/adapter/model profile;
- show expected capabilities;
- show risk;
- show estimated cost where available;
- show approvals that may occur;
- support idempotent submission;
- avoid optimistic “started” before server confirmation.

## 71. Run states

Canonical UI states:

```text
created
preflight
queued
dispatching
running
waiting
paused
cancelling
cancelled
completed
failed
stale
unknown
recovery_required
```

## 72. Run-status presentation

Every run state includes:

- label;
- explanation;
- source;
- last transition;
- freshness;
- next expected event;
- available actions;
- limitations.

## 73. Run list

Filters:

- state;
- risk;
- project;
- agent;
- adapter;
- model;
- waiting reason;
- age;
- owner;
- workspace.

## 74. Run card

Fields:

- task;
- state;
- current step;
- assigned agent;
- adapter/model;
- elapsed time;
- last reliable evidence;
- waiting/blocking reason;
- cost state;
- actions.

## 75. Run detail architecture

Recommended tabs or sections:

```text
Overview
Plan
Steps
Attempts
Approvals
Artifacts
Timeline
Evidence
Cost
Diagnostics
```

## 76. Run overview

Shows:

- intent;
- snapshot;
- state;
- progress;
- active step;
- adapter/model;
- risk;
- approvals;
- outputs;
- cost;
- freshness;
- last reliable evidence.

## 77. Run plan

Shows:

- planned steps;
- dependencies;
- approval checkpoints;
- tools;
- expected outputs;
- branches/conditions;
- recovery points.

## 78. Step view

Shows:

- purpose;
- state;
- input references;
- capability;
- attempt count;
- outputs;
- errors;
- waiting reason;
- retry policy.

## 79. Attempt view

Shows:

- attempt number;
- worker;
- adapter session;
- model observation;
- start/end;
- result;
- effect certainty;
- cancellation;
- logs/evidence links.

## 80. Attempt distinction

Retry creates a new attempt.

The UI never overwrites previous attempt evidence.

## 81. Waiting state

Waiting states include:

```text
approval
resource
adapter
provider
budget
dependency
user_input
scheduled_time
reconciliation
```

## 82. Waiting-state UI

Shows:

- reason;
- since;
- owner;
- expected resolution;
- deadline;
- escalation;
- safe action.

## 83. Stale run

A stale run view shows:

- stale label;
- last reliable evidence;
- expected heartbeat;
- suspected component;
- no false failure;
- reconcile action;
- retry blocked where effect uncertain.

## 84. Unknown run

Shows:

- what is unknown;
- last confirmed fact;
- potential consequences;
- why retry may be unsafe;
- operator/reconciliation path;
- evidence links.

## 85. Recovery-required run

Shows:

- trigger;
- affected attempts;
- blocked actions;
- required authority;
- reconciliation checklist;
- recovery history.

## 86. Run progress

Progress may be:

- step-based;
- milestone-based;
- indeterminate;
- blocked;
- unknown.

Do not show misleading percentages without a valid basis.

## 87. Run timeline

Timeline entries show:

- occurred time;
- recorded time;
- source;
- actor;
- event;
- authority state;
- freshness;
- evidence.

## 88. Timeline gaps

Explicitly show:

- missing event;
- source unavailable;
- projection stale;
- external observation gap.

## 89. Cancellation UX

The cancel action shows:

- what will stop;
- what may continue;
- external-effect limitations;
- whether rollback exists;
- confirmation;
- resulting state possibilities.

## 90. Cancellation confirmation

Avoid generic confirmation.

Example:

```text
Request cancellation for Run R-104?
The external provider may already have accepted the current operation.
Cancellation does not guarantee rollback.
```

## 91. Pause/resume UX

Only shown when capability is validated.

If unsupported, the control is absent or disabled with explanation.

## 92. Retry UX

Retry screen shows:

- failed attempt;
- effect certainty;
- reason retry is allowed;
- new attempt;
- cost;
- approval status;
- changed parameters.

## 93. Retry blocked

When effect is unknown:

```text
Retry unavailable
Reconciliation is required before another protected attempt.
```

## 94. Approval architecture

Approval list groups:

```text
my_queue
high_risk
expiring
revision_requested
approved_waiting_execution
consumed
rejected
history
```

## 95. Approval card

Shows:

- requested action;
- risk;
- target;
- requester;
- workspace;
- expiry;
- independence requirement;
- material changes;
- status.

## 96. Approval detail

Required sections:

```text
Decision summary
Exact action
Target and scope
Changes or diff
Data disclosure
Network/filesystem
Secrets
Cost
Reversibility
Evidence
Alternatives
Decision controls
```

## 97. Approval exactness

The UI displays:

- canonical action fingerprint;
- exact target;
- exact version/digest;
- exact diff/content;
- exact provider/adapter/tool;
- exact expiry.

## 98. Approval risk language

Use concrete statements.

Good:

```text
This action will create one Git commit in repository X on branch Y.
It will not push, open a pull request, or merge.
```

Avoid:

```text
Allow agent access?
```

## 99. Approve action

Requires:

- explicit button;
- no preselection;
- stale-data revalidation;
- accessible confirmation;
- authority check;
- exact fingerprint validation.

## 100. Reject action

Allows:

- reason;
- optional structured category;
- no obligation to propose unsafe alternative.

## 101. Request revision

Allows reviewer to ask for:

- narrower scope;
- different target;
- more evidence;
- changed provider;
- reduced permissions;
- corrected artifact.

Creates a new decision path, not mutation of past decision.

## 102. Approval expiry

Shows:

- expiration time;
- countdown as supplemental;
- timezone;
- impact;
- no decision after expiry.

## 103. Approval invalidation

Shows:

- why invalidated;
- material field changed;
- old request preserved;
- new request link.

## 104. Approval consumption

Shows:

- consumed at;
- attempt;
- action;
- result;
- effect certainty;
- no second use.

## 105. Approval mobile behavior

On narrow screens:

- exact scope remains visible;
- diff may use a dedicated full-screen review;
- high-risk approval may be desktop-recommended;
- approval is blocked if critical context cannot be reviewed accessibly.

## 106. Artifact architecture

Artifact areas:

```text
Proposed
Processing
Review
Accepted
Rejected
Quarantined
Exported
Deleted
```

## 107. Artifact list

Shows:

- title/type;
- producer;
- run/task;
- version;
- classification;
- integrity;
- validation;
- review state;
- freshness;
- size.

## 108. Artifact detail

Sections:

```text
Preview
Metadata
Versions
Provenance
Validation
Review
References
Exports
Deletion
Timeline
```

## 109. Artifact preview

Preview must state:

- derived or original;
- renderer;
- generated at;
- limitations;
- safety state;
- active-content status.

## 110. Unsafe preview

If safe preview unavailable:

- show metadata-only view;
- explain why;
- block active original rendering;
- allow governed download only where policy permits.

## 111. Artifact versions

Version list shows:

- immutable version;
- hash;
- producer;
- source;
- changes;
- acceptance state;
- supersession.

## 112. Artifact review

Reviewer can:

- accept exact version for purpose;
- reject;
- request revision;
- add note;
- compare versions;
- inspect validation.

## 113. Artifact acceptance

Acceptance is:

- version-specific;
- purpose-specific;
- reviewer-specific;
- not inherited by newer versions.

## 114. Artifact quarantine

Shows:

- reason;
- source;
- blocked actions;
- reviewer;
- safe metadata;
- remediation.

## 115. Artifact export

Shows:

- exact version;
- destination;
- classification;
- redactions;
- approval;
- external-copy limitation;
- export status.

## 116. Artifact deletion

Shows:

- retention hold;
- copies;
- previews/indexes;
- backups limitation;
- approval;
- tombstone.

## 117. Memory architecture

Memory navigation:

```text
Overview
Sources
Proposals
Verified
Conflicts
Stale
Deleted
```

## 118. Memory record

Shows:

- statement/content summary;
- source;
- authority;
- confidence;
- freshness;
- workspace;
- classification;
- versions;
- conflicts;
- citations.

## 119. Memory proposal

Clearly labelled:

```text
Agent-generated proposal
Not yet verified
```

## 120. Memory verification

Reviewer sees:

- source;
- evidence;
- conflicts;
- intended use;
- expiry;
- correction path.

## 121. Memory conflict

Shows competing claims side by side with:

- sources;
- authority;
- timestamps;
- confidence;
- reviewer decisions;
- unresolved status.

## 122. Memory retrieval disclosure

When memory influences a run, show:

- memory records used;
- source;
- freshness;
- authority;
- citation;
- omitted/conflicting records where relevant.

## 123. Agent architecture

Agent list shows:

- name;
- role;
- adapter;
- capabilities;
- readiness;
- model profile;
- workspace enablement;
- limitations;
- last activity.

## 124. Agent detail

Sections:

```text
Overview
Capabilities
Adapter
Models
Permissions
Workspaces
Runs
Artifacts
Health
Validation
Timeline
```

## 125. Agent identity

The UI distinguishes:

- agent profile;
- adapter runtime;
- model provider;
- actual model;
- tool executor.

## 126. Capability view

Shows:

- declared;
- validated;
- enabled;
- ready;
- authorized;
- approval required;
- limitations;
- last validation.

## 127. Capability drift

Shows:

- previous declaration;
- observed change;
- affected workflows;
- suspended state;
- revalidation action.

## 128. Adapter experience

Adapter list shows:

- name/type;
- version;
- health;
- readiness;
- validation age;
- sessions;
- capabilities;
- errors;
- owner.

## 129. Adapter detail

Sections:

```text
Identity
Health
Capabilities
Sessions
Events
Models
Tools
Permissions
Validation
Runbook
```

## 130. Model profile experience

Shows:

- logical profile;
- configured binding;
- selected route;
- actual identity;
- provider;
- region;
- context/output limits;
- data policy;
- cost state;
- health;
- fallback.

## 131. Actual model identity

Must distinguish:

```text
configured
selected
provider_reported
adapter_reported
locally_observed
inferred
unknown
conflicted
```

## 132. Model fallback UX

Shows:

- original profile;
- fallback;
- reason;
- capability difference;
- provider/region change;
- cost difference;
- data-policy impact;
- approval need.

## 133. Integration architecture

Integration list includes:

- provider;
- tool;
- MCP server;
- storage;
- notification;
- external data source.

## 134. Integration detail

Shows:

- identity;
- trust;
- version/endpoint;
- capabilities;
- permissions;
- data classes;
- secrets references;
- network;
- health;
- validation;
- affected workspaces.

## 135. Secret references UX

Users see:

- reference name;
- purpose;
- provider/account;
- scope;
- status;
- rotation;
- expiry;
- last validation.

They never see the raw secret.

## 136. MCP experience

MCP server view shows:

- identity;
- endpoint/transport;
- tools;
- resources;
- prompts;
- roots;
- drift;
- data policy;
- validation;
- health.

## 137. MCP tool review

Each tool maps to:

- Agent OS capability;
- effect class;
- approval requirement;
- target;
- data disclosure;
- evidence;
- limitations.

## 138. Operations architecture

Operations home includes:

```text
Environment
Health
Alerts
Runs
Events and queues
Adapters and providers
Storage
Backups
Maintenance
Incidents
Diagnostics
```

## 139. Environment view

Shows:

- profile;
- build;
- schema;
- config hash;
- drift;
- services;
- exposure;
- operating state;
- last deployment;
- backup.

## 140. Health view

Shows:

- liveness;
- readiness;
- dependency health;
- freshness;
- capacity;
- data integrity;
- security posture.

## 141. Alert center

Filters:

- severity;
- state;
- owner;
- environment;
- workspace;
- subsystem;
- age.

## 142. Alert detail

Shows:

- rule;
- current value;
- threshold;
- freshness;
- evidence;
- owner;
- runbook;
- acknowledgment;
- suppression;
- resolution.

## 143. Events-and-queues view

Shows:

- outbox;
- inbox;
- dead letters;
- consumer lag;
- event gaps;
- replay;
- projection freshness;
- jobs/leases.

## 144. Backup view

Shows:

- last scheduled;
- last success;
- last verified;
- backup age;
- destination;
- manifest;
- restore drill age;
- warnings.

## 145. Restore view

High-risk workflow shows:

- exact backup;
- target;
- environment;
- maintenance;
- build/schema;
- reconciliation plan;
- approvals;
- progress;
- validation.

## 146. Maintenance view

Shows:

- mode;
- scope;
- start/end;
- owner;
- user impact;
- affected services;
- actions;
- rollback;
- communications.

## 147. Incident view

Shows:

- severity;
- state;
- impact;
- confirmed facts;
- unknowns;
- timeline;
- workstreams;
- recovery;
- communications;
- review actions.

## 148. Diagnostic bundle UX

Shows:

- scope;
- time range;
- workspace;
- classification;
- included signals;
- redaction;
- status;
- expiry;
- export approval.

## 149. Settings architecture

Workspace settings groups:

```text
General
Members
Roles
Policies
Agents
Integrations
Models
Budgets
Data
Notifications
Extensions
Advanced
```

## 150. Settings safety

High-risk settings:

- require reauthentication;
- show impact;
- show affected workflows;
- support review;
- preserve history;
- avoid immediate destructive application without confirmation.

## 151. Member management

Shows:

- person;
- role;
- workspace;
- status;
- last activity;
- authority;
- delegation;
- expiry.

## 152. Role assignment

Shows:

- permissions;
- risk;
- scope;
- expiry;
- reason;
- approval if required;
- no broad “admin” without explanation.

## 153. Policy experience

Policy list shows:

- name;
- scope;
- effect;
- priority;
- status;
- version;
- affected capabilities;
- last evaluation.

## 154. Policy simulation

Before enabling a policy, allow safe simulation against:

- representative actions;
- workspaces;
- roles;
- data classes;
- expected decisions.

## 155. Budget experience

Shows:

- limit;
- used;
- reserved;
- unknown;
- period;
- warning;
- hard block;
- provider/profile.

## 156. Cost presentation

Separate:

```text
estimated
calculated
provider_reported
invoice_reconciled
unknown
conflicted
```

## 157. Retention settings

Shows:

- data class;
- record type;
- period;
- hold;
- deletion method;
- backup limitation;
- owner.

## 158. Extension settings

Shows:

- installed;
- enabled;
- permissions;
- capabilities;
- validation;
- trust;
- update;
- revoke;
- uninstall;
- workspace scope.

## 159. Global UI state model

Canonical states:

```text
initial
loading
refreshing
ready
empty
partial
stale
degraded
blocked
unavailable
error
unknown
conflicted
maintenance
recovery
```

## 160. Initial

No request has started.

## 161. Loading

Primary content unavailable while first request is in progress.

## 162. Refreshing

Current content remains visible while update is fetched.

## 163. Ready

Required data is available and current within threshold.

## 164. Empty

Request succeeded and no records exist.

## 165. Partial

Some sources or fields are unavailable.

## 166. Stale

Data is older than its freshness threshold.

## 167. Degraded

Feature remains partly usable with known subsystem loss.

## 168. Blocked

Action cannot proceed due to policy, approval, dependency, budget, maintenance, or recovery.

## 169. Unavailable

Feature or source cannot currently be used.

## 170. Error

A bounded request or operation failed.

## 171. Unknown

The system cannot establish the current state or external effect.

## 172. Conflicted

Reliable sources disagree.

## 173. Maintenance

Planned or controlled restriction is active.

## 174. Recovery

System is reconciling after failure/restore.

## 175. State-presentation contract

Each non-ready state includes:

- label;
- explanation;
- source;
- last reliable data;
- impact;
- safe next action;
- owner/escalation;
- accessibility announcement where appropriate.

## 176. Loading behavior

- preserve layout;
- avoid large shifts;
- use descriptive labels;
- no indefinite spinner without timeout/alternative;
- support cancellation where relevant.

## 177. Empty behavior

Distinguish:

- no data exists;
- filters remove all data;
- unauthorized data omitted;
- source unavailable.

## 178. Partial behavior

Show which sections are current and which are missing.

Do not hide missing sections.

## 179. Error behavior

Errors should include:

- stable error code where useful;
- human explanation;
- correlation ID;
- retry if safe;
- support path;
- no secret detail.

## 180. Optimistic UI

Use only for reversible, low-risk operations where server reconciliation is reliable.

Do not optimistically show:

- approval consumed;
- protected effect complete;
- run started;
- artifact accepted;
- restore complete;
- role granted.

## 181. Toasts and notifications

Use for supplemental confirmation.

Critical state must remain visible in the page or attention center.

## 182. Inline validation

Show:

- field;
- reason;
- expected format;
- safe correction;
- summary at top for forms;
- focus management.

## 183. Destructive actions

Require:

- exact target;
- impact;
- dependencies;
- backups/retention where relevant;
- explicit confirmation;
- reauthentication/approval where required.

## 184. Confirmation hierarchy

```text
no confirmation
light confirmation
explicit modal
typed confirmation
approval workflow
```

Choose based on risk.

## 185. Trust cues

The UI uses explicit labels for:

```text
authoritative
source_reported
generated
estimated
inferred
verified
unverified
stale
unknown
conflicted
```

## 186. Provenance display

For important outputs, show:

- producer;
- version;
- inputs;
- run/attempt;
- model/adapter;
- time;
- validation;
- source references.

## 187. Freshness display

Show:

- last updated;
- source observed at;
- threshold state;
- next refresh;
- stale warning.

## 188. Risk display

Risk should include:

- effect class;
- data class;
- reversibility;
- scope;
- external destination;
- approval;
- unknowns.

## 189. Confidence display

Confidence applies only where meaningful.

It must include source and method.

Do not show precise percentages without valid basis.

## 190. Generated summaries

Generated summaries are labelled and link to source material.

They never replace exact approval content or canonical evidence.

## 191. Terminology

Use controlled terms consistently.

Avoid mixing:

- job and task;
- run and attempt;
- approval and permission;
- configured and actual model;
- accepted and completed;
- cancelled and cancellation requested;
- deleted and hidden.

## 192. Plain-language layer

Technical detail may be accompanied by plain-language explanation.

Example:

```text
Effect state: unknown
We cannot confirm whether the external system completed the action.
Do not retry until reconciliation is complete.
```

## 193. Localization architecture

- stable machine codes;
- translatable labels;
- locale-aware date/time;
- timezone visible for approvals;
- expandable layouts;
- no logic based on translated strings.

## 194. Date and time

Show:

- absolute time;
- timezone;
- relative time as supplemental;
- occurred versus recorded time where relevant.

## 195. Numbers and currency

Show:

- locale format;
- currency;
- source;
- rounding;
- unknown state;
- estimated versus reconciled.

## 196. Responsive architecture

Reference widths:

```text
320
375
768
1024
1440+
```

## 197. Small-mobile principles

- one primary column;
- no hidden essential state;
- sticky safe actions only where they do not cover content;
- full-screen sheets for complex review;
- horizontal tables become cards or scoped scroll regions;
- no global horizontal scroll.

## 198. Tablet principles

- collapsible navigation;
- split view where useful;
- accessible touch targets;
- keep approval context visible.

## 199. Desktop principles

- multi-panel layouts;
- resizable detail panes where appropriate;
- dense operations tables;
- persistent contextual navigation;
- keyboard shortcuts.

## 200. Wide-desktop principles

Do not stretch line length excessively.

Use:

- bounded content width;
- side panels;
- comparative views;
- timeline/detail layouts.

## 201. Mobile restrictions

Certain workflows may be:

- view-only;
- desktop-recommended;
- blocked when exact review is impossible.

Examples:

- large code diff approval;
- complex restore;
- policy editing;
- multi-panel incident command.

## 202. Tables

Tables must support:

- accessible headers;
- sorting;
- filtering;
- pagination;
- row actions;
- responsive alternative;
- empty/error/stale states;
- keyboard use.

## 203. Cards

Cards should not hide critical comparison data.

Use cards for mobile summaries and dashboards, not as a substitute for every table.

## 204. Modals

Use for bounded decisions.

Avoid nesting modals.

High-complexity workflows use dedicated pages.

## 205. Drawers and side panels

Useful for:

- quick details;
- filters;
- contextual history.

They must support focus management and full-page alternative.

## 206. Command palette

Potential expert feature for navigation and safe low-risk actions.

It must:

- show exact scope;
- respect permissions;
- exclude ambiguous protected actions;
- remain keyboard accessible.

## 207. Keyboard shortcuts

Shortcuts must:

- be discoverable;
- avoid browser/assistive conflicts;
- never trigger destructive action without confirmation;
- respect current scope.

## 208. Accessibility architecture

Detailed requirements belong in proposed/unregistered `A11Y-001`.

UXA-001 establishes:

- WCAG 2.2 AA direction;
- semantic HTML;
- keyboard access;
- visible focus;
- non-color state;
- reflow;
- screen-reader status;
- accessible charts;
- reduced motion;
- error summaries;
- approval accessibility.

## 209. Focus management

Focus should move predictably after:

- route change;
- dialog open/close;
- form error;
- approval decision;
- deleted item;
- alert acknowledgment.

## 210. Live regions

Use selectively for:

- run-state change;
- critical alert;
- validation;
- operation completion.

Avoid announcing high-frequency telemetry continuously.

## 211. Color use

Color is supplemental.

Every state includes text, icon, pattern, or shape.

## 212. Motion

Motion should:

- explain transitions;
- be brief;
- respect reduced motion;
- not imply false progress;
- avoid distracting operations users.

## 213. Charts

Provide:

- title;
- description;
- units;
- source;
- freshness;
- textual summary;
- accessible table where needed.

## 214. Onboarding architecture

Onboarding steps:

```text
Create or join workspace
→ understand environment
→ configure identity/role
→ add first agent
→ validate adapter/model
→ create task
→ run simulator
→ review artifact
→ inspect receipt
```

## 215. First-run onboarding

Must use safe simulator or read-only flow.

No consequential external effect is required.

## 216. Workspace onboarding

Includes:

- purpose;
- members;
- data class;
- policies;
- budget;
- agents;
- integrations;
- backup/readiness.

## 217. Agent onboarding

Includes:

- adapter;
- capabilities;
- models;
- tools;
- permissions;
- validation;
- test run;
- limitations.

## 218. Onboarding completion

Do not show complete based only on form submission.

Completion requires readiness evidence.

## 219. Help architecture

Help surfaces:

- contextual explanation;
- glossary;
- runbook links;
- support request;
- error-code lookup;
- guided tours;
- keyboard shortcuts.

## 220. Support entry

Support request should prefill:

- environment;
- workspace;
- build;
- route;
- correlation ID;
- safe state summary.

No secret content.

## 221. Documentation links

Links are version-aware and contextual.

Avoid sending users to generic documentation when a specific runbook applies.

## 222. Notification architecture

Channels:

```text
in_app
email
messaging
webhook
```

Only in-app is required for early local MVP.

## 223. Notification priority

```text
informational
attention
action_required
urgent
critical
```

## 224. Notification content

Includes:

- exact subject;
- workspace;
- action;
- deadline;
- risk;
- link;
- no secret/sensitive full content.

## 225. Notification deduplication

Group repeated events.

Do not spam users for high-frequency run updates.

## 226. Notification acknowledgment

Acknowledgment does not mutate underlying business state unless explicitly designed.

## 227. User preference architecture

Preferences may include:

- density;
- appearance;
- locale;
- timezone;
- notification channels;
- reduced motion;
- table columns.

Preferences cannot weaken security.

## 228. Mission Control conceptual layout

Recommended desktop composition:

```text
Global shell
├── Workspace navigation
├── Attention/status header
├── Primary content
│   ├── summary
│   ├── state and actions
│   ├── main workflow
│   └── evidence/timeline
└── Context panel
```

## 229. Run-detail conceptual layout

```text
Header: task + state + actions
Summary: last reliable evidence + waiting/risk
Main: plan/steps/attempts
Side: agent/model/approval/cost
Bottom or tab: timeline/evidence
```

## 230. Approval-detail conceptual layout

```text
Header: action + risk + expiry
Main: exact action/diff/content
Side: target, requester, permissions, cost
Footer: reject, revise, approve
```

Decision actions remain visible only when full required review material is available.

## 231. Artifact-review conceptual layout

```text
Header: artifact/version/state
Main: safe preview
Side: provenance, integrity, classification
Bottom: compare, reject, revise, accept
```

## 232. Operations-dashboard conceptual layout

```text
Environment state
Critical alerts
Stale/unknown runs
Queues and dead letters
Adapters/providers
Storage/backups
Recent changes
```

## 233. End-to-end journey J01 — First safe run

1. Sign in.
2. Select workspace.
3. Review workspace health.
4. Create task.
5. Create immutable snapshot.
6. Select simulator agent.
7. Review preflight.
8. Start run.
9. Observe queue and execution.
10. Review text artifact.
11. Accept exact artifact version.
12. Inspect receipt.

## 234. J01 success criteria

- no external effect;
- clear states;
- task snapshot visible;
- adapter/model identity visible;
- artifact provenance;
- receipt;
- no mock success.

## 235. Journey J02 — Approval-gated action

1. Create protected task.
2. Preflight identifies approval.
3. Run reaches waiting approval.
4. Reviewer opens exact request.
5. Reviewer compares action/target/diff.
6. Reviewer approves.
7. Approval is consumed once.
8. Action executes.
9. Outcome and certainty visible.
10. Receipt links decision and result.

## 236. J02 failure paths

- expired request;
- fingerprint mismatch;
- reviewer ineligible;
- independence violation;
- emergency stop;
- dispatch uncertain;
- effect unknown.

## 237. Journey J03 — Reject and revise

1. Reviewer identifies excess scope.
2. Rejects or requests revision.
3. Original request remains immutable.
4. Task/run receives revision state.
5. New bounded action is created.
6. New fingerprint and approval request.
7. Review occurs again.

## 238. Journey J04 — Stale run recovery

1. Operator sees stale alert.
2. Opens run diagnostics.
3. Reviews last reliable evidence.
4. Checks lease and adapter session.
5. Classifies effect certainty.
6. Runs reconciliation.
7. Chooses safe resolution.
8. Records evidence.
9. Run returns to valid state or remains unknown.

## 239. Journey J05 — Artifact quarantine

1. Artifact finalization occurs.
2. Validation flags active or unsafe content.
3. Artifact enters quarantine.
4. User sees metadata-only view.
5. Security reviewer inspects safe evidence.
6. Artifact remains blocked, is rejected, or reprocessed.
7. Timeline preserves decisions.

## 240. Journey J06 — Adapter outage

1. Adapter readiness becomes unhealthy.
2. New dispatch is blocked.
3. Active runs show affected state.
4. Operator inspects adapter.
5. Fallback is evaluated.
6. Users see delay and limitation.
7. Adapter returns or is revoked.
8. Runs reconcile.

## 241. Journey J07 — Restore and recovery

1. Environment enters maintenance.
2. Restore operation is prepared.
3. Exact backup and target reviewed.
4. Restore runs.
5. System starts in recovery-only.
6. Approvals, runs, events, artifacts, memory reconcile.
7. Read-only continuity opens.
8. Safe functions reopen progressively.
9. Normal/degraded state declared.

## 242. Journey J08 — New adapter onboarding

1. Register adapter.
2. Validate identity/version.
3. Review capabilities and permissions.
4. Bind secret references.
5. Run conformance.
6. Enable in one workspace.
7. Run safe test.
8. Observe readiness.
9. Expand only after evidence.

## 243. Journey J09 — Budget exceeded

1. Budget warning appears.
2. User reviews known/estimated/unknown cost.
3. New cost-incurring runs block.
4. Owner inspects reservations and anomalies.
5. Budget changes or work is reduced.
6. Action resumes through policy.

## 244. Journey J10 — Support request

1. User sees error/stale state.
2. Opens support.
3. Safe context is prefilled.
4. User explains impact.
5. Support reviews workspace-scoped diagnostics.
6. Issue is resolved or escalated.
7. User receives clear status.

## 245. Journey-state mapping

Every journey should define:

- entry;
- actor;
- goal;
- prerequisite;
- authoritative objects;
- states;
- alternate paths;
- errors;
- approvals;
- artifacts;
- evidence;
- exit;
- accessibility;
- telemetry.

## 246. Error-recovery matrix

| Condition | User-facing action |
|---|---|
| Network unavailable | Preserve current state, retry safely |
| Session expired | Reauthenticate, preserve draft where safe |
| Stale projection | Show stale, refresh/rebuild |
| Adapter unavailable | Wait, choose approved alternative, cancel |
| Approval expired | Create new request |
| Effect unknown | Reconcile, no retry |
| Artifact unsafe | Metadata-only, quarantine |
| Budget exceeded | Review budget/reservations |
| Maintenance | Explain available functions |
| Cross-workspace denial | Safe denial, support if unexpected |

## 247. Draft preservation

For long forms:

- autosave bounded drafts;
- show save state;
- preserve on session timeout where safe;
- no secret persistence;
- no claim of submission until server confirms.

## 248. Offline behavior

Potential local-first offline behavior:

- cached shell;
- read-only previously loaded data with stale label;
- local drafts;
- no protected execution;
- no silent queue of high-risk commands.

## 249. Performance UX

Targets should support:

- fast shell;
- progressive loading;
- bounded tables;
- virtualized large timelines where accessible;
- no blocking full-page reload for minor updates;
- clear long-running operation state.

## 250. Long-running operations

Show:

- accepted;
- progress or indeterminate;
- elapsed time;
- cancellation semantics;
- background continuation;
- notification when complete;
- evidence link.

## 251. Polling and streaming

UI should:

- show live/last update;
- reconnect safely;
- avoid duplicate entries;
- indicate degraded polling fallback;
- preserve state during reconnect.

## 252. Data-density strategy

Use:

- summary;
- drill-down;
- filters;
- compare;
- export.

Do not present every technical field at once to all users.

## 253. Expert detail

Provide a technical details panel containing:

- IDs;
- versions;
- fingerprints;
- event codes;
- trace/correlation;
- raw safe schemas;
- diagnostics.

## 254. Novice explanation

Provide plain-language explanation adjacent to technical details.

## 255. Security UX

Security-sensitive actions show:

- identity;
- scope;
- expiry;
- effect;
- data;
- destination;
- reason;
- audit.

## 256. Reauthentication UX

For critical actions:

- explain why;
- preserve review context;
- return user to exact action;
- revalidate after authentication.

## 257. Session-expiry UX

- warn before expiry where appropriate;
- preserve safe drafts;
- block stale approvals;
- require refresh of sensitive data.

## 258. Permission-denied UX

Should not reveal unauthorized resource existence unnecessarily.

Provide:

- safe reason;
- required role or contact where allowed;
- correlation ID;
- no hidden “try admin” shortcut.

## 259. Privacy UX

The interface should disclose:

- what data is sent externally;
- provider/region;
- retention;
- source;
- classification;
- export/delete limitations.

Detailed privacy architecture may require a future separately registered document.

## 260. Cost UX

Before cost-incurring action, show where material:

- estimate;
- uncertainty;
- budget impact;
- provider;
- fallback impact.

After execution, show source and reconciliation state.

## 261. Ethical and human-oversight UX

The system should make clear:

- who requested;
- who approved;
- which agent acted;
- what was automated;
- what remains human responsibility;
- how to contest/correct.

## 262. Visual hierarchy direction

Priority order:

```text
critical state
→ required action
→ purpose/context
→ primary workflow
→ evidence
→ secondary metadata
```

## 263. Density and whitespace

Use whitespace to separate decisions and evidence.

Avoid excessive cards that fragment a single workflow.

## 264. Typography direction

Detailed typography belongs in proposed/unregistered `DSN-001`.

UX direction:

- readable;
- clear hierarchy;
- bounded line length;
- monospaced style only for code/IDs/diffs;
- no overly small metadata;
- strong focus/label contrast.

## 265. Color direction

Detailed palette belongs in `DSN-001`.

UX direction:

- neutral shell;
- restrained accent;
- semantic colors;
- non-color redundancy;
- accessible contrast;
- no decorative alert saturation.

## 266. Icon direction

- consistent;
- labelled where ambiguous;
- no icon-only critical actions;
- distinguish state and action icons;
- accessible hidden text.

## 267. Visual evidence direction

The UI should support safe screenshots of:

- state;
- approval;
- artifact;
- dashboard;
- errors.

Sensitive values should be avoidable or redacted.

## 268. Visual verification dependency

Detailed procedures belong in proposed/unregistered `VVR-001`.

UXA requires visual verification for:

- new routes;
- responsive changes;
- approval flows;
- artifact views;
- operations states;
- empty/error/stale states;
- keyboard focus.

## 269. Design-system dependency

Detailed tokens, components, variants, and implementation contracts belong in proposed/unregistered `DSN-001`.

## 270. Accessibility dependency

Detailed conformance, testing, assistive-technology matrix, and exceptions belong in proposed/unregistered `A11Y-001`.

## 271. UI-state dependency

A separate proposed/unregistered `UIF-001` may formalize machine-readable UI states and feedback. Its need should be resolved during the documentation audit.

## 272. Analytics and UX measurement

Potential measures:

- task completion;
- time to understand run state;
- time to review approval;
- approval errors;
- stale-run recovery time;
- artifact-review completion;
- support requests;
- accessibility blockers;
- mobile abandonment;
- unknown-state misunderstanding.

## 273. Analytics safety

Do not collect:

- raw prompts;
- artifact content;
- secret values;
- unrestricted identifiers;
- keystrokes;
- sensitive review material.

## 274. UX research direction

Methods:

- journey review;
- prototype usability;
- cognitive walkthrough;
- accessibility review;
- operator rehearsal;
- pilot observation;
- support-analysis review.

## 275. Prototype stages

```text
low_fidelity
interaction_prototype
connected_frontend
integrated_system
pilot_candidate
```

## 276. Prototype labelling

Every prototype states:

- data source;
- mock versus real;
- connected actions;
- unsupported actions;
- build/version;
- intended audience.

## 277. Mock-data policy

Mock data:

- clearly labelled;
- isolated;
- not mixed with real operational data;
- disabled in release surfaces unless intentional demo mode;
- excluded from evidence.

## 278. Dead-control policy

A control must be:

- functional;
- disabled with reason;
- hidden due to authorization;
- explicitly marked planned/demo.

No silent no-op.

## 279. Visual validation workflow

For visible changes:

1. rebuild current runtime;
2. verify environment/build;
3. run smoke;
4. hard refresh;
5. test changed actions;
6. inspect required widths;
7. inspect state variants;
8. verify keyboard;
9. record evidence;
10. approve before next integration.

## 280. UX defect severity direction

```text
UX0 — Unsafe or blocking critical control
UX1 — Core journey impossible or misleading
UX2 — Major degradation
UX3 — Moderate usability issue
UX4 — Cosmetic
```

## 281. UX0 examples

- approval hides material target;
- unknown effect shown successful;
- cross-workspace data exposed;
- destructive action mislabelled;
- keyboard user cannot reject/approve;
- mobile hides critical risk;
- stale data shown current.

## 282. UX1 examples

- run cannot be recovered;
- artifact review impossible;
- button no-op;
- state disappears after refresh;
- critical error has no recovery path;
- workspace context ambiguous.

## 283. UX acceptance criteria by stage

### Developer complete

- changed flow functional;
- states handled;
- visual verification;
- keyboard smoke;
- no mock/dead control.

### Integration candidate

- connected backend;
- persistence;
- errors;
- stale/unknown;
- cross-workspace;
- responsive.

### Release candidate

- critical journeys;
- accessibility;
- evidence;
- operations states;
- performance;
- no UX0/UX1.

### Pilot ready

- real user acceptance;
- support;
- limitations;
- observation;
- critical workflows understandable.

## 284. UX quality gate

A feature is UX-complete when:

- information architecture is coherent;
- primary journey is connected;
- states are explicit;
- errors recover;
- permissions are understood;
- risk is visible;
- evidence is available;
- responsive behavior works;
- accessibility passes;
- visual verification is recorded.

## 285. Journey inventory template

```text
Journey ID:
Name:
Actor:
Goal:
Entry:
Prerequisites:
Authoritative objects:
Main path:
Alternate paths:
Failure paths:
Approvals:
Artifacts:
Evidence:
Exit:
Responsive:
Accessibility:
Metrics:
```

## 286. Screen inventory template

```text
Screen ID:
Route:
Audience:
Purpose:
Primary object:
Primary action:
Secondary actions:
States:
Data sources:
Freshness:
Permissions:
Responsive:
Accessibility:
Evidence:
```

## 287. Component-use template

```text
Component:
Purpose:
Contexts:
States:
Data:
Actions:
Risk:
Responsive:
Accessibility:
Telemetry:
```

## 288. Content template

```text
Title:
Plain-language summary:
State:
Source:
Freshness:
Required action:
Limitations:
Technical details:
Support:
```

## 289. Requirement catalogue

### Architecture and navigation

- `UXA-REQ-ARC-001` — Workspace context is persistent.
- `UXA-REQ-ARC-002` — Navigation reflects controlled information architecture.
- `UXA-REQ-ARC-003` — Environment state is visible.
- `UXA-REQ-ARC-004` — Critical attention items are discoverable.
- `UXA-REQ-ARC-005` — Breadcrumbs reflect current journey.
- `UXA-REQ-ARC-006` — Global search is authorization-safe.
- `UXA-REQ-ARC-007` — Responsive navigation preserves essential routes.
- `UXA-REQ-ARC-008` — The core remains usable without optional plugins.

### State and trust

- `UXA-REQ-STA-001` — Canonical UI states are explicit.
- `UXA-REQ-STA-002` — Unknown and stale are never shown as ready.
- `UXA-REQ-STA-003` — Source and freshness are shown for critical state.
- `UXA-REQ-STA-004` — Configured and actual model identities are distinct.
- `UXA-REQ-STA-005` — Cancellation request and completion are distinct.
- `UXA-REQ-STA-006` — Generated summaries are labelled.
- `UXA-REQ-STA-007` — Partial and conflicted states expose limitations.
- `UXA-REQ-STA-008` — Dashboards cannot create false green.

### Runs and approvals

- `UXA-REQ-RUN-001` — TaskSnapshot is visible and immutable.
- `UXA-REQ-RUN-002` — Run, step, and attempt are distinct.
- `UXA-REQ-RUN-003` — Waiting reason and owner are visible.
- `UXA-REQ-RUN-004` — Unknown effects block retry UI.
- `UXA-REQ-RUN-005` — Approval review shows exact action and target.
- `UXA-REQ-RUN-006` — Approval controls are deliberate and accessible.
- `UXA-REQ-RUN-007` — Approval consumption is visible and unique.
- `UXA-REQ-RUN-008` — Recovery actions preserve evidence.

### Artifacts, memory, and evidence

- `UXA-REQ-EVD-001` — Artifact version, integrity, provenance, and classification are visible.
- `UXA-REQ-EVD-002` — Unsafe artifacts use metadata-only or safe preview.
- `UXA-REQ-EVD-003` — Acceptance is version- and purpose-specific.
- `UXA-REQ-EVD-004` — Memory source, authority, freshness, and conflicts are visible.
- `UXA-REQ-EVD-005` — Agent-generated memory is labelled unverified.
- `UXA-REQ-EVD-006` — Receipts and timelines are linked.
- `UXA-REQ-EVD-007` — Evidence gaps are visible.
- `UXA-REQ-EVD-008` — External copies and deletion limitations are disclosed.

### Responsive, accessibility, and quality

- `UXA-REQ-QUA-001` — Critical journeys support keyboard use.
- `UXA-REQ-QUA-002` — State is not communicated by color alone.
- `UXA-REQ-QUA-003` — Required widths avoid global horizontal overflow.
- `UXA-REQ-QUA-004` — Mobile preserves essential review context.
- `UXA-REQ-QUA-005` — Dead controls are prohibited.
- `UXA-REQ-QUA-006` — Mock data is clearly isolated.
- `UXA-REQ-QUA-007` — Visible changes receive visual verification.
- `UXA-REQ-QUA-008` — Critical UX defects block release.

## 290. Traceability

| Source | UXA-001 response |
|---|---|
| `PER-001` | Audience goals and needs |
| `UCD-001` | Journeys and use cases |
| `SCP-001` | Scope and product boundaries |
| `PRD-001` | Product behavior and outcomes |
| `SRS-001` | Functional screens and actions |
| `NFR-001` | Accessibility, performance, security, usability |
| `AUT-001` | Approval and autonomy presentation |
| `RUN-001` | Run, step, attempt, recovery |
| `APR-001` | Exact approval UX |
| `ART-001` | Artifact review and acceptance |
| `MEM-001` | Memory source, authority, conflict |
| `MOD-001` | Model identity and cost presentation |
| `API-001` | UI commands, errors, freshness |
| `EVT-001` | Timelines and async state |
| `OBS-001` | Health, freshness, dashboards, alerts |
| `OPS-001` | Recovery, maintenance, incidents |
| `PLG-001` | Extension and MCP UX |

## 291. ADR backlog

### `ADR-TBD-UXA-001 — Primary information architecture and shell`

Confirm top-level navigation, workspace switcher, global search, attention center, and environment indicator.

### `ADR-TBD-UXA-002 — Mission Control page architecture`

Confirm dashboard, task, run, approval, artifact, memory, and operations layouts.

### `ADR-TBD-UXA-003 — Canonical UI state and freshness model`

Confirm state vocabulary, freshness thresholds, partial/unknown presentation, and machine-readable mapping.

### `ADR-TBD-UXA-004 — Responsive and mobile operating model`

Confirm supported widths, mobile restrictions, responsive tables, and high-risk review behavior.

### `ADR-TBD-UXA-005 — UX evidence and analytics`

Confirm usability research, telemetry, visual verification, prototype labelling, and release evidence.

## 292. Open decisions

1. Confirm `UXA-001` registration.
2. Confirm top-level navigation labels.
3. Confirm whether Home and Mission Control are the same route.
4. Confirm project/goal/task hierarchy.
5. Confirm workspace switcher behavior.
6. Confirm environment indicator placement.
7. Confirm attention-center grouping.
8. Confirm global search scope.
9. Confirm desktop density defaults.
10. Confirm supported mobile workflows.
11. Confirm high-risk mobile approval restrictions.
12. Confirm run-detail tab structure.
13. Confirm approval-detail layout.
14. Confirm artifact-review layout.
15. Confirm operations dashboard scope.
16. Confirm canonical UI state vocabulary.
17. Resolve whether `UIF-001` is a separate document.
18. Confirm onboarding sequence.
19. Confirm localization priorities.
20. Confirm browser/device support.
21. Confirm UX analytics policy.
22. Confirm prototype and mock labelling.
23. Confirm visual-verification evidence.
24. Confirm design-system dependency.
25. Confirm accessibility review ownership.

## 293. Risks

| Risk | Consequence | Response |
|---|---|---|
| Chat-centric design hides orchestration | Users misunderstand control | Mission Control architecture |
| Too many top-level sections | Cognitive overload | Progressive disclosure |
| Workspace context lost | Cross-workspace error | Persistent switcher/scope |
| Unknown shown as failed/success | Unsafe retry/decision | Explicit unknown state |
| Approval too generic | Accidental authorization | Exact review material |
| Mobile hides critical detail | Unsafe review | Restrict or full-screen |
| Dashboards treated as truth | False confidence | Source/freshness |
| Too many cards | Fragmented workflow | Purposeful hierarchy |
| Technical language overwhelms | Pilot adoption failure | Plain-language layer |
| Simplification hides risk | Unsafe action | Risk always visible |
| Dead buttons | False completeness | No-dead-control rule |
| Mock data mixed with real | Misleading evidence | Explicit demo isolation |
| Stale frontend after change | Invalid visual review | Build/hard-refresh workflow |
| Accessibility added late | Rework/exclusion | Architectural requirement |
| Cost shown without source | Misleading decisions | State/source labels |
| Model identity conflated | Wrong trust assumptions | Configured/actual distinction |
| Timeline gaps hidden | False audit confidence | Gap indicators |
| Recovery not designed | Operator dead ends | Recovery journeys |
| Overly dense desktop UI | Error-prone operation | Density modes |
| Excessive documentation links | User abandonment | Contextual help |

## 294. Assumptions

- Agent OS uses a web-based Mission Control;
- workspace is the primary operational scope;
- the control plane exposes durable domain state;
- API/events support source and freshness metadata;
- users may operate at different technical levels;
- high-risk actions require deliberate review;
- mobile access is useful but not sufficient for every operation;
- accessibility target is WCAG 2.2 AA direction;
- local-first deployment remains important;
- design system, accessibility, and visual verification will be specified separately.

## 295. Constraints

- no UI-only authorization;
- no false success from optimistic state;
- no hidden unknown/stale state;
- no dead controls;
- no unlabelled mock operational data;
- no approval without exact review context;
- no mobile approval when critical evidence cannot be reviewed;
- no raw secret display;
- no arbitrary plugin UI script;
- no final design tokens or component library in this document;
- no final accessibility or visual-regression tooling selected;
- no Git commit, push, PR, merge, or release during the documentation drafting phase.

## 296. Acceptance criteria

UXA-001 may advance to `1.0.0` when:

1. It is formally added to the document register.
2. Product accepts information architecture, journeys, and onboarding.
3. Architecture accepts object/state mapping and UI/backend boundaries.
4. Security accepts approval, scope, secrets, and recovery presentation.
5. Data accepts provenance, classification, freshness, and deletion presentation.
6. Operations accepts Mission Control, alerts, maintenance, recovery, and incident views.
7. Quality accepts responsive, accessibility, mock, dead-control, and visual-verification gates.
8. top-level navigation is approved;
9. run and approval journeys are approved;
10. canonical UI states are approved;
11. mobile limitations are explicit;
12. source/freshness/unknown presentation is consistent;
13. critical screen inventory is complete;
14. `DSN-001`, `A11Y-001`, and `VVR-001` can refine implementation without changing core UX invariants;
15. the global consistency audit resolves `UIF-001`.

## 297. Downstream impact

| Document | Required use |
|---|---|
| `DSN-001` | Tokens, components, patterns, visual hierarchy |
| `A11Y-001` | Detailed conformance and testing |
| `VVR-001` | Screenshot baselines and regression workflow |
| `IAM-001` | Identity, roles, sessions, reauthentication UX |
| `POL-001` | Policy simulation and decision explanation |
| `AUD-001` | Evidence, timelines, receipts |
| `CST-001` | Cost and budget presentation |
| `ADP-HER-001` | Hermes operational and capability UX |
| `ADP-CDX-001` | Codex repository, diff, tests, Git controls UX |
| Document register | Add proposed document and dependencies |

## 298. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial UX architecture covering audiences, information architecture, Mission Control, tasks, runs, approvals, artifacts, memory, agents, integrations, operations, UI states, trust, responsive behavior, accessibility direction, onboarding, support, journeys, and quality gates |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `PER-001` — Personas and Jobs to Be Done
- `UCD-001` — User Journeys and Use Cases
- `SCP-001` — Scope and Boundaries
- `PRD-001` — Product Requirements Document
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `MEM-001` — Memory and Knowledge Architecture
- `MOD-001` — Model Profile Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `PLG-001` — Plugin and Extension Architecture
