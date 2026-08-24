---
document_id: GLO-001
title: Agent OS Glossary and Controlled Terminology
version: 0.3.0
status: approved
owner: product-owner
approvers:
  - product-owner
created: 2026-07-16
last_reviewed: 2026-08-18
approval_date: 2026-08-13
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user authorization after document review
  - role: product-owner
    status: approved
    approval_date: 2026-08-18
    evidence: explicit Product Owner approval of the multi-execution backend and normalized economics extension
classification: internal
source_of_truth: true
related_documents:
  - DOC-000
related_adrs: []
---

# GLO-001 — Agent OS Glossary and Controlled Terminology

## Purpose

This glossary defines the initial vocabulary used by the project. Terms remain draft until reviewed during the product-baseline phase.

| Term | Controlled definition |
|---|---|
| Agent OS | Application-level control plane for operating, governing, observing, and extending multiple AI agents, models, tools, workflows, workspaces, and artifacts. It is not a replacement for Windows, Linux, or macOS. |
| Agent | A runtime entity that combines one or more models with instructions, tools, memory, permissions, and an execution loop to perform bounded tasks. |
| Agent adapter | Replaceable integration implementing the Agent OS contract for a specific agent runtime or external agent service. |
| Agent definition | Versioned configuration describing an agent’s identity, capabilities, limits, routing metadata, and default policies. |
| Agent instance | A deployable or active realization of an agent definition. |
| Artifact | Versioned output or input associated with a task or run, such as a report, patch, image, video, dataset, log, or document. |
| Approval | Durable authorization, rejection, modification, or escalation decision associated with a proposed sensitive action. |
| Account | The authenticated platform identity that can own or access one or more workspaces. |
| Capability | Machine-readable statement of what an agent, model, tool, plugin, or integration can perform. |
| Conversation | A durable interaction thread passing through Agent OS. It may be private or linked to a project, mission, task, or run. |
| Control plane | Platform services that manage identity, workspaces, tasks, workflows, policies, routing, approvals, budgets, audit, and configuration. |
| Data plane | Systems and connectors through which agents read or change permitted information and artifacts. |
| Execution plane | Isolated workers, runtimes, agents, and sandboxes where tasks are executed. |
| Experience plane | User-facing interfaces, including web, desktop, mobile, chat, studio, dashboards, and external application integrations. |
| Human-in-the-loop | Workflow design in which a person reviews, supplies information, modifies, approves, or rejects an agent action. |
| Knowledge record | Approved, source-linked information available for future retrieval within a permitted scope. |
| Memory | Stored information used to influence future agent behavior or context; separated into temporary, episodic, project, and authoritative knowledge layers. |
| Model | AI inference system used for language, reasoning, coding, vision, audio, image, video, embedding, or other supported capabilities. |
| Model gateway | Central service that authenticates, routes, limits, observes, and accounts for model-provider requests. |
| Model profile | Provider-neutral set of capability, privacy, cost, latency, and quality requirements used to route a request to an appropriate model. |
| MCP | Model Context Protocol, used by compatible clients and servers to expose tools, resources, and contextual data. |
| A2A | Agent-to-Agent protocol or project profile used for interoperability between independent agents. |
| AG-UI | Event-based interface protocol or project profile connecting interactive user interfaces with agentic backends. |
| Plugin | Versioned extension package that adds bounded capabilities to the Agent OS through declared contracts and permissions. |
| Policy decision | Structured authorization or governance result produced by the policy subsystem for a proposed action. |
| Mission | Outcome-oriented objective within a project. A mission may contain one or more executable tasks. |
| Project | Durable domain or body of work within a workspace. Projects organize missions, conversations, artifacts, memory, and runs. |
| Risk class | Product-facing action tag mapped by AUT-001 to the canonical R0–R4 risk, L0–L5 autonomy, and I0–I3 independence matrix. Tags include read, generate, controlled_write, external_effect, destructive, and critical. |
| Run | Durable execution record created when an agent or workflow processes a task. |
| Run step | Ordered unit of execution, tool use, approval, delegation, or transformation within a run. |
| Skill | Reusable instruction, reference, and optional script package that guides an agent through a repeatable workflow. |
| Task | Work item with an objective, scope, status, ownership, constraints, and expected outputs. |
| Tool | Callable capability exposed through MCP, an API, a local runtime, or another controlled integration. |
| Visibility scope | Resource access scope: private, project, or workspace. Visibility is separate from workspace membership. |
| Workflow | Versioned and durable process coordinating deterministic steps, agents, tools, approvals, retries, and completion rules. |
| Workspace | Primary isolation and organization boundary containing projects, permissions, knowledge, agents, tools, tasks, runs, artifacts, budgets, and policies. |
| Execution Backend | Explicit execution route selected by policy for a run or attempt. Agent OS distinguishes model-provider connections, agent-runtime connections, and the deterministic simulator. |
| Model Provider Connection | Execution backend connection that invokes a model directly through an external provider or local model endpoint, such as the OpenAI Responses API. |
| Agent Runtime Connection | Execution backend connection that governs an agent runtime or session, which may manage model access, tools, state, and work internally. |
| Subscription-backed Runtime | Agent runtime authenticated through an included subscription or session entitlement rather than a per-request API credential and invoice. It is not an actual cost of zero. |
| Actual Monetary Cost | Monetary cost fact sourced from provider billing/calculation, a subscription inclusion, an approved allocation, an invoice, or an explicit unknown state. |
| Normalized Equivalent Cost | Versioned simulated USD value representing equivalent usage under a reference pricing model; it is distinct from actual monetary cost, billing, accounting, and realized savings. |
| Pricing Catalog | Versioned collection of pricing rules for providers, models/SKUs, units, effective periods, conditional rates, sources, freshness, and confidence. |
| Pricing Snapshot | Immutable per-execution capture of the Pricing Catalog rules and identifiers used to calculate or estimate an equivalent cost. |
| Billing Source | Authority or semantic origin of a monetary fact, such as provider invoice, API usage calculation, subscription inclusion, allocation, or unknown. |
| Paid Fallback | Explicitly authorized routing from one backend or runtime to a paid provider/API route, with policy, budget, identity, disclosure, and evidence re-evaluated. |
