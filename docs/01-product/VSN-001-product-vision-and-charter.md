---
document_id: VSN-001
title: Agent OS Product Vision and Project Charter
version: 1.1.0
status: in-review
owner: product-owner
approvers:
  - product-owner
created: 2026-07-16
last_reviewed: 2026-07-16
approval_date: 2026-07-16
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-12
    evidence: explicit user decision selecting Hermes, Codex, and Claude Code as the initial adapter baseline
pending_approvals:
  - architecture-owner
  - security-owner
  - operations-owner
  - quality-owner
classification: internal
source_of_truth: true
related_documents:
  - DOC-000
  - GLO-001
  - VIDEO-001
  - VIDEO-002
  - VIDEO-003
  - VIDEO-004
related_adrs: []
related_evidence:
  - VIDEO-EVIDENCE-INDEX
---

# VSN-001 — Agent OS Product Vision and Project Charter

> **Status: Approved baseline.** VSN-001 is the approved product-vision baseline. It does not prove implementation and does not replace later scope, PRD, architecture, security, requirements, or other controlled decisions. Section 27 contains approved tracked open questions that remain unresolved for later controlled documents.

## 1. Document purpose

This document establishes the proposed product direction, value, boundaries, principles, success measures, constraints, and decision authority for Agent OS. It guides later scope, requirements, architecture, security, UX, delivery, and assurance documents without replacing them.

## 2. Executive summary

**PROPOSED:** Agent OS is a provider-neutral control, orchestration, and governance platform for operating multiple AI agents, models, tools, workflows, knowledge sources, and artifacts through durable workspaces, explicit permissions, human approvals, and complete observability.

The platform opportunity is to replace fragmented, opaque AI work with governed and resumable execution. A user should be able to understand what is running, why it is permitted, which model or tool is involved, what it costs, what it produced, and what evidence supports its status. The first product increment is proposed as a local, single-node, accessible web Mission Control with three agent adapters (Hermes, Codex, and Claude Code), durable task/run state, approvals, governed tools, artifacts, permission-aware memory, audit events, and cost attribution.

This approved vision baseline retains the tracked open questions in Section 27 for later controlled documents. No functionality is claimed to exist.

## 3. Product vision

Enable people and organizations to delegate bounded work across replaceable AI agents and providers without surrendering control, provenance, portability, or operational visibility.

Agent OS should make AI work durable and governable at the workspace level while preserving a path from local use to production operation. It should allow implementation choices to evolve behind stable product concepts and contracts.

## 4. Problem statement

AI-assisted work is fragmented across chat applications, coding agents, model providers, automation services, files, project repositories, media-generation tools, and business dashboards. This fragmentation causes recurring problems:

- users repeatedly reconstruct context and cannot reliably find prior outputs;
- tasks and agent loops can lose state when a process stops;
- provider, model, tool, and storage choices leak into user workflows;
- permissions and approvals are often implicit in prompts rather than enforced controls;
- costs, side effects, sources, and execution status are difficult to attribute;
- memory can mix unverified claims with authoritative knowledge;
- attractive dashboards can hide mock, stale, or disconnected data;
- MCP or tool connectivity can be mistaken for authorization;
- business or profit narratives can be mistaken for accounting facts.

The product problem is therefore broader than multi-provider chat. It is the absence of a coherent control plane for durable, permissioned, observable AI work.

## 5. Opportunity

The opportunity is to provide a consistent operating model across agents, models, tools, knowledge, and artifacts while leaving each implementation replaceable. A governed Agent OS can reduce tool switching, preserve work context, improve review and recovery, expose cost and risk, and make integrations reusable.

The video audit shows a recurring desire for Mission Control, named agents, goals, workspaces, task boards, media artifacts, skills, and memory. Those concepts are useful research inputs. The larger opportunity is to engineer the production foundations that the videos do not demonstrate: durable execution, authorization, isolation, provenance, evaluation, auditability, and authoritative data boundaries.

## 6. Product definition

**PROPOSED:** Agent OS is an application-level control plane composed conceptually of:

- an **experience plane** for Mission Control, workspaces, tasks, approvals, artifacts, and administration;
- a **control plane** for identity, policies, routing, budgets, orchestration, audit, and configuration;
- an **execution plane** for isolated agent and tool work;
- a **data plane** for permitted knowledge, artifacts, integrations, and business-system reads.

These are product boundaries, not an approved deployment architecture. Their detailed realization belongs in SAD-001 and later ADRs.

Agent OS is not:

- a replacement for Linux, Windows, or macOS;
- only a multi-provider chat interface;
- an unrestricted autonomous agent;
- an authoritative accounting ledger;
- a guarantee of perfect memory;
- a system that treats MCP connectivity as automatic authorization;
- a collection of decorative dashboards disconnected from real data.

## 7. Target users and stakeholders

### 7.1 Target users — to validate

| User | Primary need | Authority boundary |
|---|---|---|
| Individual operator | Organize and resume AI-assisted project work | Controls personal workspaces within policy |
| Product or business owner | Delegate goals and review outcomes, cost, and evidence | Defines priorities and accepts product outcomes |
| Technical operator | Configure agents, models, tools, and execution | Operates integrations without bypassing security policy |
| Workspace administrator | Manage membership, permissions, budgets, and policies | Administers assigned workspaces, not global secrets by default |
| Reviewer or approver | Review consequential proposed actions | Approves only within explicitly delegated authority |
| Auditor or assurance reviewer | Reconstruct decisions, execution, and evidence | Read-only access to authorized audit material |
| Contributor or consumer | Reuse knowledge and artifacts | Sees only permitted workspace information |

### 7.2 Project stakeholders — authority pending confirmation

| Role | Named owner | Proposed authority |
|---|---|---|
| Product owner | **NOT CONFIRMED** | Vision, scope, priority, user value, and acceptance |
| Architecture owner | **NOT CONFIRMED** | Architecture coherence and ADR review |
| Security owner | **NOT CONFIRMED** | Security controls and risk acceptance |
| Data/finance owner | **NOT CONFIRMED** | Authoritative business-data definitions and reconciliation |
| UX/accessibility owner | **NOT CONFIRMED** | Experience quality and accessibility acceptance |
| Quality owner | **NOT CONFIRMED** | Test strategy, evidence, and quality gates |
| Operations owner | **NOT CONFIRMED** | Deployment, recovery, and operational acceptance |
| Implementers and agents | Multiple; names **NOT CONFIRMED** | Draft and implement within approved scope; cannot self-approve |

## 8. Jobs to be done

**PROPOSED; user research required:**

1. When I start or resume a project, help me recover the relevant context, active work, permissions, and outputs without rebuilding them from separate tools.
2. When I delegate a task, let me choose or route to an appropriate agent/model, bound its permissions and budget, and understand its progress.
3. When an action is consequential, pause it for an authorized human decision and preserve that decision as evidence.
4. When a run fails or is interrupted, let me diagnose, resume, retry, or cancel it without duplicating side effects.
5. When an agent produces an output, store it with provenance and make it retrievable only within its permitted scope.
6. When I connect a tool or MCP server, let me grant the minimum capability required and revoke it independently of the prompt.
7. When I review usage or business information, show source, freshness, lineage, and uncertainty rather than presenting generated values as facts.
8. When providers or agent frameworks change, preserve my core workflows and data through stable adapters and contracts.

## 9. Value proposition

### For users

- continuity across sessions, agents, and tools;
- controlled delegation with visible limits and approvals;
- searchable, permission-aware knowledge and artifacts;
- clearer progress, failure, cost, and recovery information;
- less dependence on any one provider or agent interface.

### For organizations

- consistent policy and audit across AI workflows;
- reusable integrations and provider portability;
- evidence-backed status and acceptance;
- attributable model/tool spend and bounded autonomy;
- safer connection to operational and business data.

## 10. Architectural and product principles

All principles below are **PROPOSED** pending product and architecture review.

1. **Provider agnosticism:** provider-specific behavior remains behind replaceable adapters.
2. **Model agnosticism:** routing uses capability and policy profiles rather than hard-coded model names in core workflows.
3. **Agent-framework agnosticism:** common task, run, approval, artifact, and event concepts survive replacement of an agent runtime.
4. **Tool and storage portability:** tools and artifact/knowledge stores expose versioned contracts and migration paths.
5. **Standards-based integration:** open, versioned standards are preferred where they meet product and security needs.
6. **Workspace-centered organization:** a workspace is the primary boundary for projects, membership, policy, memory, artifacts, budgets, tasks, and runs.
7. **Durable execution:** task and run state persists independently of an interactive client or worker process.
8. **Evidence before status:** the UI and documentation must not claim success, persistence, safety, or readiness without evidence.
9. **Human control over consequential actions:** irreversible, external, sensitive, or high-risk actions require explicit policy and, where required, approval.
10. **Least privilege:** identities, agents, tools, MCP servers, and integrations receive only necessary scoped permissions for a bounded duration.
11. **Provenance-aware memory:** stored and retrieved context retains source, scope, age, confidence, and correction/deletion controls.
12. **Authoritative source separation:** generated interpretation is visibly separate from authoritative records.
13. **Observable and reproducible runs:** runs emit correlated evidence sufficient to explain inputs, configuration, approvals, steps, outputs, costs, and side effects.
14. **Modular extensibility:** versioned adapters and capability manifests extend the platform without redefining the core domain.
15. **Local-first with a production upgrade path:** the first deployment can run locally while data, contracts, and operations permit later production migration.
16. **Accessibility and responsive design:** primary workflows are designed for keyboard, assistive technology, varying viewport sizes, and perceivable state—not retrofitted after implementation.

## 11. Provider, model, agent, and tool agnosticism

Agent OS should separate four kinds of replaceability:

- **Provider:** authentication, endpoints, commercial terms, and regional behavior belong to provider adapters.
- **Model:** capability, privacy, latency, quality, reliability, and budget requirements belong to provider-neutral model profiles.
- **Agent:** agent definitions declare capabilities, instructions, permissions, limits, and compatible execution contracts.
- **Tool:** tool availability does not grant permission; each invocation is evaluated against identity, workspace policy, scope, risk, and approval requirements.

MCP may be one supported integration protocol, but connection and discovery do not constitute authorization. Final protocol choices and adapter contracts require architecture and security review.

## 12. Core product capabilities

**PROPOSED product capability map; implementation is NOT CONFIRMED:**

- identity, membership, workspaces, projects, and policies;
- agent registry, agent definitions, adapters, and capability discovery;
- model profiles, provider adapters, routing, fallback, and budgets;
- tasks, durable runs, run steps, schedules, retries, resumptions, and cancellation;
- human approvals, escalation, and graded autonomy;
- tools, MCP servers, skills, plugins, and integration governance;
- permission-aware memory, knowledge records, files, and retrieval;
- artifact storage, metadata, provenance, versioning, and preview;
- Mission Control, search, sessions, task views, execution receipts, and administrative views;
- logs, traces, evaluations, token usage, costs, health, and audit events;
- authoritative business-data read models and clearly separated AI analysis;
- adapter/contract validation and an eventual extension SDK.

## 13. MVP scope

The first MVP boundary is approved as the initial vision baseline. Detailed scope, acceptance criteria, sequencing, and implementation decisions remain for later controlled documents. It includes:

- user identity;
- workspaces and projects;
- agent registry;
- model profiles and routing foundation;
- Hermes adapter;
- Codex adapter;
- Claude Code adapter;
- task and run persistence;
- approval inbox;
- tool permission foundation;
- artifact storage and metadata;
- permission-aware memory foundation;
- audit events;
- basic execution receipts;
- token and cost tracking;
- local single-node deployment;
- accessible responsive web Mission Control.

The MVP should prove durable, governed execution across three agent adapters. It should not attempt broad feature parity with every screen or claim in the research material.

## 14. Post-MVP scope

Subject to evidence, demand, and approved architecture, later increments may include:

- schedules and reusable workflows;
- more provider, agent, tool, storage, ERP, accounting, and CRM adapters;
- advanced evaluation, policy simulation, and cost optimization;
- read-only business performance and finance analysis;
- document and media workflows, followed by image/video/voice Studio capabilities;
- desktop packaging, PWA/offline improvements, and constrained mobile review;
- multi-node and high-availability deployment;
- adapter SDK and governed marketplace;
- bounded multi-agent coordination after single-agent reliability is established.

## 15. Explicit non-goals

The proposed first MVP excludes:

- production financial posting;
- autonomous pull-request merging;
- unrestricted machine control;
- multi-agent swarms;
- self-modifying skills;
- predictive profit automation;
- full image/video/voice Studio;
- adapter marketplace;
- high-availability cluster deployment.

Project-wide non-goals also include replacing desktop operating systems, building foundation models, guaranteeing perfect memory, treating MCP connectivity as authority, silently relying on mock data, or presenting Agent OS as an accounting ledger.

## 16. Autonomy and human-control principles

**PROPOSED:** autonomy is a policy-governed spectrum, not a global on/off setting. Each run should be bounded by identity, workspace, task scope, time, cost, data access, tool permissions, side-effect class, and stop conditions.

- Read-only, reversible, and low-risk steps may qualify for greater autonomy under policy.
- External communication, financial action, production change, credential use, destructive action, or irreversible side effect should require stronger controls and often human approval.
- Approval must be durable, attributable, scoped, time-bounded where appropriate, and linked to the exact proposed action.
- A user must be able to pause, cancel, or revoke future authority without rewriting a prompt.
- “Goal Mode” and long-running autonomy remain post-foundation concepts; video narration does not prove safe or reliable operation.

The detailed autonomy matrix belongs in AUT-001.

## 17. Data, memory, and artifact principles

- Workspace and project permissions apply at ingestion, storage, retrieval, and export.
- Memory is not assumed true because an agent stored it; authoritative knowledge requires source and governance.
- Retrieval should expose source, age, scope, and reason for inclusion where practical.
- Users need correction, deletion, retention, and export controls consistent with policy.
- Artifacts are versioned inputs or outputs linked to tasks, runs, sources, models, tools, and approvals.
- Files and artifacts require integrity metadata, provenance, authorization, lifecycle state, and safe preview behavior.
- Cross-workspace retrieval is denied unless an explicit policy authorizes it.
- “Perfect memory,” automatic write-back, and indefinite retention are rejected as product guarantees.

## 18. Security and trust principles

**PROPOSED:** trust is established through independently enforced controls and evidence, not through model instructions or interface appearance.

- authenticate users, workloads, adapters, and integrations;
- authorize every consequential operation using least privilege;
- isolate execution and limit filesystem, network, secret, and process access;
- store secrets outside source control and prompts;
- classify tool side effects and require policy/approval before execution;
- defend memory and tool flows against prompt injection and untrusted content;
- preserve immutable or tamper-evident audit events appropriate to the threat model;
- make failure, uncertainty, stale data, and partial completion visible;
- support revocation, incident investigation, recovery, and controlled deletion.

Detailed controls and accepted risks belong in SEC-001 and THR-001.

## 19. Business-data and profit-monitoring principles

Agent OS may provide read-only analysis and monitoring using authorized ERP, accounting, CRM, campaign, or operational sources after MVP foundations are proven.

- Source systems remain authoritative for transactions and books and records.
- Revenue, cost, margin, and profit definitions require a named data/finance owner.
- Every metric should expose source, definition, period, freshness, and reconciliation status.
- AI-generated forecasts, classifications, explanations, and recommendations must be labeled as generated analysis.
- Agent OS must not silently post financial entries or treat generated values as accounting records.
- Prototype or promotional profit dashboards are not evidence of accurate or connected business data.

Production financial posting and predictive profit automation are excluded from the MVP.

## 20. Deployment vision

**PROPOSED:** begin with a local single-node deployment suitable for a controlled Linux/WSL development and pilot environment. Preserve explicit boundaries for identity, orchestration, execution, data, and adapters so that later deployments can add remote access, managed services, isolation, backup, scaling, regional controls, and high availability without replacing core product concepts.

Local-first does not mean local-only, insecure by default, or exempt from backup and authorization. The supported operating systems, container strategy, remote-access model, tenancy model, recovery objectives, and production topology are **NOT CONFIRMED** and require later architecture and operations decisions.

## 21. Product success metrics

The following values are approved as **initial baseline targets**, not implementation commitments. They remain subject to refinement in later controlled documents with product, architecture, security, or quality validation as identified in Section 27.

| Category | PROPOSED initial target | Measurement method |
|---|---:|---|
| Successful persisted runs | ≥99% of accepted MVP runs retain terminal state and required records | Integration test and pilot telemetry over an approved run cohort |
| Approval-policy enforcement | 100% of test actions classified as approval-required are blocked without a valid approval | Policy conformance suite including denial and expiry cases |
| Run resumption | ≥95% of resumable interruption scenarios continue without duplicate side effects | Fault-injection suite across defined checkpoints |
| Cross-workspace isolation | 100% pass rate for approved negative-access tests | Automated authorization and retrieval isolation suite |
| Artifact retrieval | ≥99% successful retrieval of retained, authorized pilot artifacts | Storage/API tests plus pilot telemetry, excluding deliberate deletion |
| Trace completeness | 100% of accepted runs emit the required event/receipt fields | Schema validation against a defined minimum trace contract |
| Cost attribution | ≥95% of billable model/tool events attributed to workspace, task, and run | Reconciliation of provider/tool usage against Agent OS cost events |
| Adapter conformance | 100% pass rate for required Hermes, Codex, and Claude Code contract tests | Versioned adapter conformance suite |
| User task completion | Establish baseline, then target ≥80% for defined MVP journeys | Moderated and instrumented usability tests with representative users |
| Accessibility | WCAG 2.2 AA for defined MVP workflows; zero unresolved critical blockers | Automated checks plus keyboard and assistive-technology review |
| Recovery time | Restore the local pilot service and retained data within 4 hours | Documented recovery exercise from an approved backup scenario |
| Documentation traceability | 100% of accepted MVP requirements link to architecture, tests, and evidence | RTM and document-validator checks |

Final targets must account for workload, sample size, exclusions, measurement ownership, and operational cost.

## 22. Project success criteria

Before the MVP can be accepted, evidence should demonstrate that:

1. at least two approved agent adapters operate through common registered capabilities;
2. tasks and runs survive defined interruption scenarios with controlled recovery;
3. consequential actions are blocked until policy and required approval conditions are satisfied;
4. model and tool activity can be attributed to a workspace, task, run, identity, and cost event where applicable;
5. artifacts are retrievable with provenance and authorization controls;
6. cross-workspace isolation tests pass;
7. Mission Control reports real persisted state and distinguishes unknown, partial, failed, and stale states;
8. no accepted MVP workflow silently depends on non-persistent mock data;
9. required documentation, contracts, tests, operational guidance, and acceptance evidence are traceable;
10. product, architecture, security, UX/accessibility, quality, and operations owners explicitly accept their respective evidence.

These criteria are approved as vision-level success criteria; later controlled documents must refine owners, thresholds, acceptance methods, and implementation evidence.

## 23. Constraints

- Canonical work occurs in a Git-reviewed repository; approval cannot be inferred from file creation or commit.
- The initial development and pilot environment is assumed to be local Linux/WSL, pending confirmation.
- Local evidence files and videos remain outside Git tracking.
- Secrets and credentials must not be committed or embedded in controlled documents.
- Open and versioned standards are preferred at integration boundaries, subject to fitness and security review.
- Architecture, security, product scope, business metrics, and visible UX require human validation.
- The project starts documentation-first; application implementation status is currently **NOT CONFIRMED**.
- Scope must remain bounded enough to prove three adapters and governed durable execution before expanding.

## 24. Assumptions

The following assumptions are retained explicitly and require validation:

- the first pilot can run on a local single-node Linux/WSL environment;
- initial users need Hermes, Codex, and Claude Code adapters;
- a workspace is the appropriate primary isolation and organization boundary;
- users value continuity, governed delegation, artifact retrieval, and cost visibility more than broad media features in the first MVP;
- provider/model diversity is valuable enough to justify adapter contracts in the MVP;
- external business systems, if connected, can expose authorized read interfaces with usable lineage;
- product, architecture, security, data, UX, quality, and operations review roles can be assigned;
- Git-based review is the initial approval record, unless governance later defines another mechanism.

No assumption is an approved business decision.

## 25. Dependencies

### Controlled-document dependencies

- DOC-000 for documentation governance;
- GLO-001 for controlled terminology;
- SCP-001 and PRD-001 for approved boundaries and detailed requirements;
- PER-001 and UCD-001 for validated users and journeys;
- NFR-001 and AUT-001 for quality attributes and autonomy policy;
- SAD-001, SEC-001, and THR-001 for architecture and security decisions;
- adapter, run, approval, artifact, API, and event contracts planned in the register;
- TST-001, RTM-001, and QAG-001 for validation and acceptance.

### External and project dependencies — pending confirmation

- availability and permitted use of Hermes, Codex, and Claude Code integration surfaces;
- model-provider accounts and commercial/privacy terms;
- supported identity, storage, execution, and secret-management mechanisms;
- representative pilot users, workspaces, tasks, and datasets;
- named decision owners and review capacity.

## 26. Principal risks

| Risk | Consequence | Proposed response |
|---|---|---|
| Scope expansion | An unbounded collection of AI features prevents a credible MVP | Enforce the Section 13/15 boundary through SCP-001 and PRD-001 |
| Provider leakage | Core workflows become costly to replace | Define capability and adapter contracts before provider-specific behavior |
| Prototype-as-proof | UI presence is mistaken for functional reality | Require persistence, integration, and acceptance evidence before status |
| Excessive tool authority | Agents cause unauthorized or irreversible effects | Least privilege, isolation, policy decisions, approvals, and revocation |
| Memory contamination or leakage | Unverified or cross-workspace data influences work | Provenance, ACL-aware retrieval, source separation, correction, and tests |
| Fragile long-running runs | Lost state or duplicate side effects | Durable state, idempotency, checkpoints, retries, and fault testing |
| Incomplete observability | Operators cannot explain cost, failure, or effect | Required events, correlated receipts, evaluation, and reconciliation |
| False business confidence | Generated or stale metrics are treated as records | Authoritative-source lineage, freshness, reconciliation, and labels |
| Accessibility debt | Mission Control excludes users or requires redesign | Include accessibility acceptance in MVP design and testing |
| Premature infrastructure | Complexity delays product evidence | Local single-node first; scale only against measured need |
| Documentation drift | Decisions, contracts, and implementation diverge | Register, traceability, validators, review gates, and evidence |

## 27. Approved tracked open questions for later controlled documents

1. Who are the named product, architecture, security, data/finance, UX, quality, and operations owners?
2. Is the first deployment single-user, trusted-team, or multi-organization?
3. Which users and priority jobs form the first pilot, and which workspaces/tasks represent them?
4. Are Hermes, Codex, and Claude Code the approved first adapters, and what integration modes are permitted?
5. Is Agent OS initially an internal platform, a personal product, or a future commercial offering?
6. Is remote access required in the first pilot, or is local-only access sufficient?
7. Which actions are consequential enough to require approval in the first MVP?
8. Which data classes may enter memory, artifacts, logs, and model-provider requests?
9. Which business systems and metric definitions, if any, belong in post-MVP discovery?
10. Which standards and protocols are required versus merely candidates, including MCP, A2A, and AG-UI?
11. What detailed scope, sequencing, and acceptance criteria should SCP-001 apply to the approved MVP inclusions and explicit exclusions in Sections 13 and 15?
12. What final targets, samples, exclusions, and owners should later controlled documents apply to the approved initial baseline targets in Section 21?
13. Is WCAG 2.2 AA the approved accessibility baseline for all defined MVP workflows?
14. Is four hours an acceptable proposed recovery target for the local pilot, and what data-loss objective applies?
15. What budget, schedule, staffing, and provider-spend constraints govern the MVP?
16. What review and reapproval conditions apply to future material revisions of VSN-001?

## 28. Relationship to the video audit

The local video audit is Draft research evidence, not an approved product or architecture authority.

- [VIDEO-001](../research/agent-os-video-audit/VIDEO-001-video-inventory-and-methodology.md) defines source inventory, method, evidence labels, and limitations.
- [VIDEO-002](../research/agent-os-video-audit/VIDEO-002-ui-ux-evidence-audit.md) records `OBSERVED`, `STATED`, `INFERRED`, `PROPOSED`, and `NOT CONFIRMED` UI/UX findings.
- [VIDEO-003](../research/agent-os-video-audit/VIDEO-003-agent-os-capability-opportunity-brief.md) proposes capability opportunities and MVP/post-MVP priorities.
- [VIDEO-004](../research/agent-os-video-audit/VIDEO-004-architecture-and-documentation-impact.md) identifies future architecture and documentation impacts.
- [Video evidence index](../research/agent-os-video-audit/video-evidence-index.csv) provides timestamped supporting evidence.

The audit supports exploration of a unified Mission Control, named agents, goals/tasks, workspaces, artifacts, Studio, skills, and memory. It does **not** confirm backend persistence, provider routing, secure execution, authorization, accounting accuracy, autonomous reliability, or production readiness. This vision adopts recommendations only as labeled proposals and explicitly rejects treating interface presence or narration as proof.

## 29. Related controlled documents

| Document | Relationship | Current status |
|---|---|---|
| DOC-000 | Governs document status, evidence, approval, and traceability | Draft |
| GLO-001 | Defines Agent OS terminology used here | Draft |
| VIDEO-001 through VIDEO-004 | Draft research inputs and limitations | Draft |
| SCP-001 | Will define detailed scope and MVP acceptance boundaries | Planned; not created |
| PRD-001 | Will convert approved vision/scope into product requirements | Planned; not created |
| PER-001 / UCD-001 | Will validate users, jobs, and journeys | Planned; not created |
| SAD-001 | Will decide architecture; this vision does not | Planned; not created |
| AUT-001 / SEC-001 / THR-001 | Will define autonomy and security controls | Planned; not created |
| TST-001 / RTM-001 / QAG-001 | Will define validation, traceability, and gates | Planned; not created |

## 30. Approval and revision history

### Approval state

- Current status: `approved`
- Approval authority: Product Owner
- Approval date: 2026-07-16
- Approved baseline version: `1.0.0`
- Tracked open questions: Section 27 remains unresolved and is approved for later controlled-document follow-up

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-16 | Draft | Initial vision and charter skeleton | Draft authoring; not approved |
| 0.2.0 | 2026-07-16 | Draft | Expanded evidence-based product vision, boundaries, principles, MVP, metrics, risks, and audit traceability | Documentation revision requested by user; not approved |
| 1.0.0 | 2026-07-16 | Approved | Product Owner approved the product vision, charter, principles, proposed MVP boundary, explicit non-goals, success framework, risks, and tracked open questions as the initial product baseline. | Product Owner explicit approval |
