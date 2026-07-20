---
document_id: PER-001
title: Agent OS Personas and Jobs to Be Done
version: 0.1.0
status: draft
owner: product-owner
approvers:
  - product-owner
  - ux-accessibility-owner
created: 2026-07-19
last_reviewed: 2026-07-19
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - UCD-001
  - PRD-001
  - AUT-001
  - IAM-001
  - UXA-001
  - A11Y-001
related_adrs: []
related_evidence:
  - VIDEO-002
  - VIDEO-003
---

# PER-001 — Agent OS Personas and Jobs to Be Done

> **Status: Draft.** The personas and jobs in this document are evidence-informed hypotheses for the first Agent OS pilot. They have not yet been validated through direct user research. They must not be represented as confirmed market segments, measured behavior, or proof of product-market fit.

## 1. Document purpose

This document defines the proposed users, stakeholder personas, jobs to be done, pains, desired outcomes, authority boundaries, accessibility needs, and pilot-research plan for Agent OS.

It provides a controlled input to:

- `UCD-001` — user journeys and use cases;
- `PRD-001` — product requirements;
- `SRS-001` — functional requirements;
- `AUT-001` — autonomy and approval matrix;
- `IAM-001` — identity and access control;
- `UXA-001` — information architecture;
- `A11Y-001` — accessibility requirements;
- `TST-001` — test strategy.

## 2. Scope

This document covers the people expected to use, configure, govern, review, or audit the first local Agent OS pilot.

The first-pilot boundary is:

- one organization context;
- one primary operator or a small trusted team;
- multiple isolated workspaces;
- local Linux/WSL deployment;
- Hermes and Codex as initial adapter targets;
- no anonymous users;
- no public SaaS onboarding;
- no production financial posting;
- no unrestricted autonomous machine control.

Future commercial, public, multi-organization, or marketplace personas are recorded only as later hypotheses.

## 3. Relationship to approved vision and scope

`VSN-001` establishes the approved product vision: durable, governed, provider-neutral AI work with explicit permissions, human approvals, provenance, artifacts, observability, and cost attribution.

`SCP-001` proposes the detailed first-pilot and MVP boundaries.

This document does not:

- select architecture or technologies;
- grant permissions;
- approve remote or production access;
- prove that any feature exists;
- define final market segmentation;
- replace requirements or security controls.

Where a persona need conflicts with an approved scope or security boundary, the approved boundary prevails until explicitly changed.

## 4. Evidence and confidence model

No direct interviews, observational studies, surveys, or pilot telemetry have yet been completed.

Persona statements use the following confidence labels:

| Label | Meaning |
|---|---|
| `SUPPORTED` | Consistent with approved vision, approved scope, or observed project workflow |
| `PROPOSED` | Reasonable product hypothesis requiring validation |
| `NOT CONFIRMED` | Important but currently unsupported by direct user evidence |
| `FUTURE` | Outside the first MVP or pilot |
| `REJECTED` | Explicitly inconsistent with project principles or scope |

Research videos are used only as supporting discovery material. They do not confirm user demand, safe autonomy, reliable persistence, or production readiness.

## 5. Persona model

Agent OS uses two related persona dimensions.

### 5.1 Human responsibility persona

Describes why a person uses Agent OS and what outcome they own.

Examples:

- Builder-Operator;
- Product or Workspace Owner;
- Technical Operator;
- Reviewer or Approver;
- Auditor or Assurance Reviewer;
- Contributor or Consumer.

### 5.2 Permission role

Describes what an identity may do in a specific organization or workspace.

Examples:

- platform administrator;
- workspace owner;
- operator;
- approver;
- auditor.

A human may hold more than one responsibility persona and more than one permission role. Product requirements must not assume that persona and permission are identical.

## 6. Persona priority

| Priority | Persona | Pilot importance |
|---:|---|---|
| 1 | PERS-001 — Builder-Operator | Primary daily user and first-pilot focus |
| 2 | PERS-002 — Product / Workspace Owner | Defines goals, value, budget, and acceptance |
| 3 | PERS-003 — Technical Operator / Platform Administrator | Configures and maintains the local platform |
| 4 | PERS-004 — Reviewer / Approver | Controls consequential actions |
| 5 | PERS-005 — Auditor / Assurance Reviewer | Reconstructs decisions and evidence |
| 6 | PERS-006 — Contributor / Artifact Consumer | Uses permitted outputs without operating agents |
| Future | PERS-F01 — Organization Administrator | Multi-organization commercial deployment |
| Future | PERS-F02 — Extension Developer | Adapter or plugin ecosystem |
| Future | PERS-F03 — Business Analyst | Read-only business-system analysis |

## 7. PERS-001 — Builder-Operator

### 7.1 Summary

**PROPOSED primary persona.**

A technically capable individual who uses several AI agents, model providers, repositories, files, and automation tools to design, build, research, document, or operate projects.

This persona may also be the Product Owner in the first pilot.

### 7.2 Context

- works from a personal or organization-controlled computer;
- frequently uses terminals, repositories, IDEs, browsers, and AI tools;
- manages several projects with different contexts;
- wants to move between Hermes, Codex, models, and tools without rebuilding context;
- values speed but does not want loss of control;
- may operate in bandwidth-, compute-, or budget-constrained conditions;
- may need local-first operation because data, connectivity, or cost makes cloud-only usage undesirable.

### 7.3 Primary goals

- resume work without reconstructing context manually;
- delegate bounded tasks to an appropriate agent;
- see which agent, model, tool, and permissions are in use;
- preserve tasks, runs, approvals, artifacts, and decisions;
- prevent unintended changes or external side effects;
- understand failures and recover without duplicate work;
- compare cost, quality, and behavior across agents/providers;
- maintain separation between projects and workspaces.

### 7.4 Pains

- context scattered across conversations, terminals, files, and agents;
- unclear run state after interruption;
- tools that appear connected but are not safely authorized;
- duplicate side effects after retry;
- agent claims that are difficult to verify;
- outputs that are not linked to their source task;
- hidden provider or model switching;
- uncertainty about costs;
- fear that an agent may modify the wrong project or branch;
- difficult recovery after a local restart.

### 7.5 Required capabilities

- workspace and project dashboard;
- task creation with scope and budget;
- agent/model selection or transparent routing;
- visible permissions before execution;
- run timeline;
- pause, cancel, retry, and resume;
- approval requests;
- artifact and evidence retrieval;
- source/provenance display;
- cost and usage attribution;
- local backup and restore guidance.

### 7.6 Authority expectations

The Builder-Operator may:

- create and manage permitted workspaces/projects;
- start low-risk runs;
- inspect results and traces;
- request consequential actions.

The Builder-Operator must not automatically:

- approve every action merely because they created the task;
- access secrets outside policy;
- bypass workspace isolation;
- grant an agent broader permissions through prompt text;
- authorize production or financial effects without the required role.

### 7.7 Success indicators

- can resume a project in minutes without manual context reconstruction;
- can identify the current state of every active run;
- can retrieve the correct artifact and provenance;
- can explain why an action was allowed, blocked, or awaiting approval;
- can recover an interrupted workflow without duplicate side effects;
- can identify attributed cost for a task/run.

## 8. PERS-002 — Product / Workspace Owner

### 8.1 Summary

**SUPPORTED as a governance persona; behavior remains to validate.**

A person accountable for workspace goals, priorities, risk tolerance, budget, user value, and acceptance.

In a small pilot this may be the same person as the Builder-Operator. In a team it may be separate.

### 8.2 Primary goals

- define meaningful goals and priorities;
- delegate work without losing accountability;
- understand progress and blockers;
- review evidence instead of trusting status labels;
- control budgets and approved providers;
- accept or reject product outcomes;
- ensure that work remains within scope;
- prevent mock or stale data from appearing as operational truth.

### 8.3 Pains

- ambiguous completion claims;
- work delivered without acceptance evidence;
- costs that cannot be attributed;
- scope expansion caused by attractive but nonessential features;
- unclear responsibility for approvals;
- dashboards disconnected from real state;
- difficulty comparing agent outcomes.

### 8.4 Required capabilities

- workspace overview;
- goals, tasks, and outcome status;
- evidence-backed completion view;
- budget and usage summary;
- approval delegation;
- risk and exception visibility;
- artifact review;
- success-metric reporting;
- clear distinction between authoritative data and generated analysis.

### 8.5 Authority expectations

May define:

- workspace priorities;
- acceptable outcome;
- budget ceilings;
- approved use cases;
- business-level risk acceptance;
- product approval.

Must not unilaterally override:

- security controls owned by Security;
- architecture integrity controls;
- legal or privacy restrictions;
- external-source truth.

## 9. PERS-003 — Technical Operator / Platform Administrator

### 9.1 Summary

**PROPOSED operational persona.**

A technically responsible user who installs, configures, monitors, backs up, restores, and troubleshoots the local Agent OS environment.

### 9.2 Primary goals

- operate a predictable local installation;
- configure adapters and providers safely;
- manage secrets without exposing values;
- diagnose health and connectivity;
- control storage, logs, and retention;
- restore service and retained data;
- upgrade without losing state;
- verify that Agent OS reports real system state.

### 9.3 Pains

- undocumented configuration;
- credentials copied into prompts or repositories;
- agents with excessive host access;
- provider errors hidden behind generic status;
- unrecoverable local state;
- unclear compatibility across adapter versions;
- logs that expose sensitive data;
- fragile manual startup sequences.

### 9.4 Required capabilities

- installation and configuration guidance;
- health status;
- adapter diagnostics;
- secret-reference configuration;
- storage and backup status;
- safe upgrade/migration procedure;
- audit of permission and configuration changes;
- recovery test procedure;
- clear degraded-state reporting.

### 9.5 Authority expectations

May:

- operate the platform;
- configure approved integrations;
- perform backup and recovery;
- disable unhealthy adapters;
- rotate references to secrets.

Must not automatically:

- read workspace content;
- approve business actions;
- grant itself unrestricted secret access;
- bypass audit;
- change security policy without review.

## 10. PERS-004 — Reviewer / Approver

### 10.1 Summary

**SUPPORTED by the approved human-control principle.**

A person with delegated authority to approve or reject a specific consequential action.

Approval is contextual, not universal. A reviewer may approve Git actions but not financial or production actions.

### 10.2 Primary goals

- understand exactly what is being proposed;
- see the actor, task, parameters, target, risk, and evidence;
- approve, reject, request revision, or let a request expire;
- ensure the action has not materially changed after approval;
- avoid approval fatigue;
- preserve an attributable decision record.

### 10.3 Pains

- vague approval prompts;
- approvals that authorize a broad class of future actions;
- hidden parameter changes;
- requests without diff, target, cost, or side-effect information;
- excessive low-risk approval volume;
- no evidence that rejection was enforced;
- pressure to approve quickly without context.

### 10.4 Required capabilities

- prioritized approval inbox;
- risk class and policy reason;
- human-readable summary plus exact parameters;
- diff or preview where relevant;
- expiry and scope;
- approve/reject/request-change actions;
- clear execution result after decision;
- searchable decision history.

### 10.5 Authority expectations

An approver may only decide within:

- assigned workspace;
- assigned action class;
- defined resource;
- valid time window;
- conflict-of-interest policy where applicable.

An approver must not approve an action that differs materially from the reviewed proposal.

## 11. PERS-005 — Auditor / Assurance Reviewer

### 11.1 Summary

**PROPOSED assurance persona.**

A quality, security, compliance, architecture, or operational reviewer who needs to reconstruct what happened without changing operational state.

### 11.2 Primary goals

- reconstruct a task from instruction to outcome;
- identify identities, agents, models, tools, approvals, and side effects;
- distinguish persisted facts from generated interpretation;
- verify isolation and policy enforcement;
- review failures, retries, and recovery;
- trace artifacts to source runs;
- confirm that costs and provider records reconcile sufficiently.

### 11.3 Pains

- incomplete or mutable history;
- missing correlation IDs;
- status without evidence;
- logs containing secrets but lacking useful context;
- inability to distinguish user, agent, and system actions;
- untraceable memory writes;
- undocumented permission changes.

### 11.4 Required capabilities

- read-only audit access;
- correlated run and approval timeline;
- export of authorized evidence;
- filter by workspace, task, agent, provider, action, or period;
- provenance and integrity metadata;
- policy-decision details;
- stale/missing-data indicators;
- retention and deletion evidence.

### 11.5 Authority expectations

May inspect authorized evidence.

Must not:

- alter audit records;
- restart or approve operational actions;
- access unrelated workspace content;
- infer compliance where required evidence is missing.

## 12. PERS-006 — Contributor / Artifact Consumer

### 12.1 Summary

**PROPOSED secondary persona.**

A team member who consumes, reviews, comments on, or reuses permitted artifacts but does not configure agents or execute consequential workflows.

### 12.2 Primary goals

- find current approved outputs;
- understand artifact source and status;
- avoid using superseded or unverified output;
- provide feedback;
- export permitted results;
- know whom to contact when an output is wrong.

### 12.3 Required capabilities

- simple workspace navigation;
- artifact search and preview;
- source/provenance summary;
- lifecycle status;
- comments or review handoff;
- access-denied explanations;
- accessible download/export.

### 12.4 Out of scope for this persona

- provider configuration;
- global policy management;
- secret access;
- high-risk tool execution;
- broad audit export.

## 13. Future personas

### 13.1 PERS-F01 — Organization Administrator

Future commercial or multi-organization persona responsible for tenant configuration, identity federation, billing, policies, and data residency.

Excluded from the first MVP.

### 13.2 PERS-F02 — Extension Developer

Future developer who creates adapters, tools, plugins, or marketplace packages against stable contracts and conformance tests.

An internal adapter implementer may exist earlier, but a public ecosystem is post-MVP.

### 13.3 PERS-F03 — Business Analyst

Future user who consumes read-only operational, ERP, CRM, accounting, or campaign data with lineage and generated-analysis labels.

Production posting authority remains outside this persona.

## 14. Non-target and anti-personas

The MVP is not designed for:

- anonymous public users;
- consumers seeking a general entertainment chatbot;
- users expecting unrestricted autonomous control of a computer;
- organizations requiring immediate public multi-tenant SaaS;
- users expecting Agent OS to replace accounting software;
- users expecting perfect memory;
- users who require unsupported regulated-data processing;
- people seeking to bypass Git, security, or approval governance;
- mobile-only users performing consequential actions.

These exclusions are scope controls, not judgments about future value.

## 15. Jobs-to-be-Done framework

A job is expressed as:

> When **situation**, help me **motivation/action**, so I can achieve **outcome**, while respecting **constraints**.

Jobs are independent of a specific screen or provider. They should remain valid even when Hermes, Codex, models, storage, or UI components change.

## 16. Priority Jobs to Be Done

| ID | Job statement | Primary persona | MVP priority |
|---|---|---|---|
| `JTBD-001` | When I return to a project, help me recover the current context, state, permissions, and outputs so I can continue without reconstructing everything manually. | Builder-Operator | Must |
| `JTBD-002` | When I delegate work, help me define a bounded task, permitted resources, limits, and expected outcome so the agent cannot silently expand the assignment. | Builder-Operator | Must |
| `JTBD-003` | When an agent or model is selected, show me which capability, provider, model, cost policy, and fallback apply so I understand the execution choice. | Builder-Operator / Owner | Must |
| `JTBD-004` | When work is running, show persisted progress, waiting conditions, failures, costs, and evidence so I can supervise without reading every log line. | Builder-Operator / Owner | Must |
| `JTBD-005` | When an action is consequential, pause it and give the authorized reviewer enough exact context to decide safely. | Approver | Must |
| `JTBD-006` | When a run fails or is interrupted, help me diagnose, retry, resume, or cancel it without duplicating side effects. | Builder-Operator / Technical Operator | Must |
| `JTBD-007` | When an output is produced, retain it with source, version, permissions, and lifecycle state so I can trust and reuse the correct artifact. | All | Must |
| `JTBD-008` | When context is stored as memory, show its source, scope, age, and verification state so unverified claims do not silently become facts. | Builder-Operator / Auditor | Must |
| `JTBD-009` | When resources are consumed, attribute usage and cost to the responsible workspace, task, and run so I can control spend. | Owner / Builder-Operator | Must |
| `JTBD-010` | When I connect an agent, tool, or MCP server, let me grant the minimum capability and revoke it independently of prompt text. | Technical Operator | Must |
| `JTBD-011` | When I investigate an event, let me reconstruct identities, policy, approvals, steps, outputs, and side effects from correlated evidence. | Auditor | Must |
| `JTBD-012` | When I manage a workspace, let me define membership, roles, budget, and permitted integrations without affecting other workspaces. | Workspace Owner | Must |
| `JTBD-013` | When a provider becomes unavailable or unsuitable, preserve the task and workspace concepts so I can change implementation without losing core work. | Builder-Operator / Technical Operator | Should |
| `JTBD-014` | When I review Mission Control, distinguish real, partial, stale, estimated, failed, and unavailable state so I do not act on a misleading dashboard. | All | Must |
| `JTBD-015` | When I operate the local pilot, provide backup, restore, startup, health, and recovery guidance so the platform is not dependent on undocumented knowledge. | Technical Operator | Must |

## 17. Functional job families

### 17.1 Organize and resume

- create a workspace;
- create a project;
- associate approved repositories/files;
- find active tasks and outputs;
- resume from the last reliable state.

### 17.2 Delegate and execute

- define task outcome;
- select or route an agent;
- set limits;
- start a run;
- inspect steps;
- pause, cancel, retry, or resume.

### 17.3 Govern and approve

- classify side effects;
- evaluate policy;
- request approval;
- approve/reject;
- enforce decision;
- preserve evidence.

### 17.4 Retain and retrieve

- store artifacts;
- store governed memory;
- search permitted content;
- inspect provenance;
- correct, supersede, retain, or delete.

### 17.5 Operate and assure

- configure adapters;
- inspect health;
- attribute cost;
- audit actions;
- back up and restore;
- validate isolation and recovery.

## 18. Emotional and social jobs

Users may also need to:

- feel in control while delegating;
- reduce anxiety about unintended actions;
- demonstrate responsible AI operation to collaborators or clients;
- avoid embarrassment from false completion claims;
- trust that a different provider will not destroy project continuity;
- explain decisions and costs to stakeholders;
- maintain professional accountability for AI-assisted work.

These outcomes must not be manipulated through false reassurance. The product should communicate uncertainty and limits honestly.

## 19. Desired outcomes

The first-pilot users should be able to say:

- “I know what is running and why.”
- “I can stop or revoke future authority.”
- “I can recover after interruption.”
- “I can identify the source of this artifact.”
- “I know whether this status is real, stale, estimated, or unknown.”
- “I know which agent, model, and tool were used.”
- “I can see what requires approval.”
- “I can explain the cost of this task.”
- “One workspace cannot silently access another.”
- “I can change providers without redesigning my entire workflow.”

## 20. User stories for MVP discovery

The following are discovery-level stories, not yet controlled requirements.

- As a Builder-Operator, I need to create a bounded task so that an agent has explicit limits.
- As a Builder-Operator, I need to view a persisted run timeline so that a browser refresh does not erase operational truth.
- As an Approver, I need to see the exact proposed action and diff so that approval is informed.
- As a Technical Operator, I need to configure secret references without displaying secret values.
- As an Auditor, I need to correlate task, run, approval, tool, and artifact records.
- As a Workspace Owner, I need to restrict an integration to one workspace.
- As an Artifact Consumer, I need to know whether an output is approved, draft, stale, or superseded.
- As a Product Owner, I need evidence-backed completion status instead of a decorative success card.

Formal user stories and acceptance criteria belong in `UCD-001`, `PRD-001`, and `SRS-001`.

## 21. Authority and permission expectations

| Persona | Typical authority | Required limitation |
|---|---|---|
| Builder-Operator | Starts bounded work and manages permitted project context | Cannot bypass policy or self-expand permissions |
| Product / Workspace Owner | Defines goals, scope, budget, membership, and acceptance | Cannot override independent security/legal controls |
| Technical Operator | Configures and operates approved infrastructure/integrations | Does not inherit access to all workspace content |
| Approver | Decides specific action classes within delegated scope | Approval expires and is bound to exact parameters |
| Auditor | Reads authorized evidence | Cannot modify operational or audit state |
| Contributor | Reads/reuses permitted artifacts | Cannot configure high-risk execution |

The final authorization model belongs in `IAM-001`, `POL-001`, `AUT-001`, and `APR-001`.

## 22. Contexts of use

### 22.1 Primary context

- desktop or laptop;
- local Linux/WSL runtime;
- modern browser;
- keyboard and mouse;
- one or more code/document projects;
- individual or trusted-team workspace;
- variable internet connectivity;
- cost-conscious provider usage.

### 22.2 Secondary context

- tablet or mobile browser for review, status, and low-risk approvals;
- remote access only after explicit security and deployment approval.

### 22.3 Unsupported first-MVP context

- public kiosks;
- anonymous public access;
- mobile-only platform administration;
- consequential actions from an untrusted device;
- production control rooms requiring high availability;
- regulated processing without approved controls.

## 23. Accessibility and inclusion needs

The personas must not assume perfect vision, color perception, motor precision, hearing, memory, connectivity, or advanced English fluency.

The product should support:

- keyboard-only navigation;
- visible focus;
- semantic headings and landmarks;
- screen-reader labels;
- non-color status indicators;
- sufficient contrast;
- scalable text and responsive layouts;
- clear language;
- persistent error and approval context;
- reduced-motion preferences;
- large target sizes;
- accessible tables and timelines;
- explicit time-zone and date formatting;
- localization-ready content architecture.

WCAG 2.2 AA remains the proposed baseline pending approval in `A11Y-001` and `NFR-001`.

## 24. Connectivity, hardware, and local constraints

The first-pilot design should consider:

- intermittent or expensive connectivity;
- provider requests that may fail or time out;
- limited local CPU, RAM, or storage;
- laptop restart or sleep;
- WSL and filesystem boundary complexity;
- unavailable providers;
- delayed cost data;
- inability to download large artifacts;
- local backup media constraints.

The UI must not present network failure as task success.

## 25. Trust and explainability expectations

Users need explanations at different levels.

### Builder-Operator

- why an agent/model was selected;
- why a tool was allowed or blocked;
- what the run is waiting for;
- what changed;
- how to recover.

### Approver

- exact proposed action;
- target and side effects;
- policy reason;
- evidence and diff;
- expiry.

### Owner

- progress, cost, risk, outcome, and acceptance evidence.

### Auditor

- full correlated record and known evidence gaps.

Explanations must distinguish facts, provider reports, inferences, estimates, and generated summaries.

## 26. Failure and recovery expectations

Users should never need to infer whether an interrupted run is still executing.

Expected recovery affordances include:

- explicit last known persisted state;
- worker/adapter health;
- retry eligibility;
- side-effect status;
- checkpoint information;
- safe cancellation;
- operator instructions;
- no duplicate action without idempotency protection or renewed approval.

Failure language must be specific enough to support action but must not expose secrets.

## 27. Onboarding and adoption expectations

The first onboarding flow should help the primary operator:

1. understand the local and non-production boundary;
2. create or select an organization context;
3. create a workspace;
4. register or verify Hermes and Codex adapters;
5. configure provider/model profiles using secret references;
6. review permissions;
7. run a safe diagnostic task;
8. inspect the resulting trace and artifact;
9. understand approvals;
10. verify backup and recovery guidance.

The onboarding must not claim that a connected integration is fully authorized or production-ready.

## 28. Pilot participant profile

A representative first pilot should include at least:

- one Builder-Operator who actively uses more than one AI agent or provider;
- one person capable of acting as Product/Workspace Owner;
- one person capable of technical operation;
- one distinct reviewer for at least some approval scenarios;
- one assurance review perspective, even if the same person performs the audit after a scenario.

The pilot may use one person in several roles, but tests must still preserve separation of responsibilities where required.

## 29. Pilot tasks

Suggested research and acceptance tasks:

1. create two isolated workspaces;
2. connect or register Hermes and Codex;
3. define a bounded documentation or coding task;
4. start a run and inspect persisted state;
5. trigger a candidate approval action;
6. reject once and verify enforcement;
7. approve a revised action and verify exact binding;
8. interrupt and recover a run;
9. retrieve an artifact with provenance;
10. search memory without crossing workspace boundaries;
11. compare attributed usage/cost;
12. inspect the audit trail;
13. restore retained data from a documented backup scenario.

## 30. Research plan

### 30.1 Discovery interviews

Interview 5–8 representative technical operators/builders where practical.

Topics:

- current tools and project contexts;
- context-loss incidents;
- failure and recovery;
- permission and approval habits;
- cost-management behavior;
- artifact retrieval;
- trust in agent status;
- local versus remote preferences.

### 30.2 Contextual observation

Observe at least three real or representative workflows from task creation to output review.

Record:

- tool switching;
- manual context transfer;
- approval points;
- interruptions;
- evidence used to judge completion;
- hidden or duplicated side effects.

### 30.3 Prototype evaluation

Test low-fidelity then functional prototypes for:

- Mission Control;
- task definition;
- run timeline;
- approval inbox;
- artifact provenance;
- adapter configuration;
- failure recovery.

### 30.4 Pilot telemetry

Collect only approved, privacy-safe metrics such as:

- time to resume;
- task completion;
- approval decision time;
- failed and recovered runs;
- artifact retrieval success;
- cost attribution coverage;
- access-denial correctness.

## 31. Hypotheses to validate

| ID | Hypothesis |
|---|---|
| `HYP-001` | Users value durable context more than broad media features in the MVP |
| `HYP-002` | A workspace is an understandable primary isolation boundary |
| `HYP-003` | Users will accept mandatory approval for clearly consequential actions |
| `HYP-004` | Users need a summarized run view plus optional detailed evidence |
| `HYP-005` | Provider-neutral agent/model profiles reduce switching cost |
| `HYP-006` | Provenance materially increases artifact reuse and trust |
| `HYP-007` | Cost attribution at task/run level changes delegation behavior |
| `HYP-008` | Local-first operation is valuable enough to justify operational complexity |
| `HYP-009` | Separate approver authority is workable in a small trusted team |
| `HYP-010` | Users can understand distinctions among fact, estimate, stale, and unknown state |

## 32. Persona and journey success measures

Initial proposed measures:

| Measure | Initial target |
|---|---:|
| Defined MVP journey completion | At least 80% after onboarding |
| Time to find current run state | Median under 30 seconds in usability testing |
| Approval decision comprehension | At least 90% correctly identify target and side effect |
| Artifact provenance comprehension | At least 90% correctly identify producing task/run |
| Workspace-isolation mental model | At least 90% correctly predict denied cross-workspace access |
| Recovery task completion | At least 80% complete with provided guidance |
| Critical accessibility blockers | Zero unresolved for defined MVP journeys |
| Misinterpretation of stale/mock state as real | Zero in acceptance testing |

Final thresholds, samples, exclusions, and ownership belong in `NFR-001` and `TST-001`.

## 33. Product implications

The persona analysis implies that the MVP needs:

- a state-oriented Mission Control rather than a chat-only interface;
- durable workspace navigation;
- progressive disclosure of technical detail;
- explicit status semantics;
- an approval inbox separate from normal notifications;
- artifact-centric retrieval;
- provenance in every relevant detail view;
- workspace-level settings and permission views;
- diagnostics for technical operators;
- read-only assurance views;
- responsive but desktop-primary design;
- strong error, stale, and unknown-state patterns.

## 34. Risks

| Risk | Consequence | Response |
|---|---|---|
| Persona based only on project owner | Product overfits one technical user | Conduct interviews and separate responsibility roles |
| Technical-user bias | Nontechnical stakeholders cannot use Mission Control | Test plain-language summaries and progressive detail |
| Role conflation | Creator self-approves every action | Model responsibility and permission separately |
| Approval fatigue | Users bypass or ignore governance | Risk-based policy and measurable approval quality |
| False trust | Explanations create unjustified confidence | Label evidence, uncertainty, and source type |
| Local-only overfitting | Later production migration becomes expensive | Preserve stable contracts and organization/workspace keys |
| Accessibility treated as later work | Major redesign becomes necessary | Include accessibility in journeys and acceptance from the start |
| Research without representative tasks | Personas remain abstract | Use real project scenarios and measurable outcomes |

## 35. Open decisions

1. Who will participate in first-pilot interviews and observation?
2. Is the first pilot one person, a small trusted team, or both in sequence?
3. Which exact projects and tasks represent the pilot?
4. Which personas must be separate people for approval testing?
5. Which languages must the first UI support?
6. Is mobile approval included, and for which low-risk actions?
7. What accessibility review resources are available?
8. Which user data may be captured in telemetry?
9. Which onboarding steps can be automated safely?
10. Which role owns final persona validation?
11. What commercial personas should be researched before post-MVP planning?
12. Which hypotheses would invalidate or materially change the MVP?

## 36. Acceptance criteria

PER-001 may advance to version 1.0.0 when:

1. the Product Owner accepts the priority personas and non-target users;
2. the first-pilot model is aligned with approved SCP-001;
3. every primary persona has goals, pains, authority, and success outcomes;
4. priority jobs have stable identifiers;
5. persona and permission role are clearly separated;
6. accessibility and local-environment constraints are represented;
7. future personas are not presented as MVP scope;
8. research assumptions and evidence gaps remain explicit;
9. UCD-001 can derive journeys without inventing additional primary users;
10. metadata, links, terminology, and validation checks pass.

## 37. Downstream traceability

| Downstream document | Required use of PER-001 |
|---|---|
| `UCD-001` | Map each journey/use case to persona and job IDs |
| `PRD-001` | Prioritize requirements by user outcome |
| `SRS-001` | Identify actors, permissions, failure behavior, and acceptance |
| `AUT-001` | Map action class to requester and approver authority |
| `IAM-001` | Separate human responsibility from permission roles |
| `UXA-001` | Organize navigation by primary jobs |
| `A11Y-001` | Define inclusive journey requirements |
| `TST-001` | Recruit representative users and test persona outcomes |
| `RTM-001` | Trace goals and jobs to requirements and evidence |

## 38. Revision and approval history

### Approval state

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Approval date: not applicable
- Required next action: Product Owner and UX/accessibility review

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial personas, jobs, authority boundaries, research hypotheses, and pilot-participant model | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `VIDEO-002` — UI/UX Evidence Audit
- `VIDEO-003` — Agent OS Capability and Opportunity Brief
