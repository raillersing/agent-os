---
document_id: VIDEO-003
title: Agent OS Capability and Opportunity Brief
version: 0.1.0
status: draft
owner: research-owner
approvers:
  - product-owner
created: 2026-07-16
last_reviewed: 2026-07-16
classification: internal
source_of_truth: false
related_documents:
  - VIDEO-001
  - VIDEO-002
  - VSN-001
  - SCP-001
  - PRD-001
  - SAD-001
  - UXA-001
  - DSN-001
  - SEC-001
  - TST-001
related_adrs: []
---

# VIDEO-003 — Agent OS Capability and Opportunity Brief

| Field | Value |
|---|---|
| Status | Draft |
| Date | 2026-07-16 |

## Executive summary

The videos communicate a valuable product promise: one durable place to select agents, pursue goals, reuse context, invoke tools, and find outputs. The opportunity is not to clone the showcased interface; it is to turn that promise into a provider-agnostic control plane with explicit trust boundaries, resumable execution, permission-aware memory, artifact provenance, and authoritative business-data connectors.

## Video-inspired capabilities

1. Unified workspaces spanning multiple projects, sessions, tasks, and artifacts.
2. Replaceable named agents and provider/model adapters rather than agent-specific product silos.
3. Mission Control showing actionable run, task, cost, and health status—not decorative KPIs.
4. Goals decomposed into durable tasks, schedules, checkpoints, retries, resumptions, and cancellation.
5. Central registry for tools, MCP servers, skills, connectors, and their scoped credentials.
6. Permission-aware memory/knowledge with provenance, retention, user correction, and project isolation.
7. Media/document Studio with asynchronous jobs, lineage, versions, safety state, and reusable artifacts.
8. Human approvals and graded autonomy for consequential actions.
9. Logs, traces, evaluations, token/latency/cost monitoring, and exportable audit history.
10. Business dashboards fed by authoritative ERP/accounting/CRM sources, with AI commentary explicitly separated from books and records.

## Production requirements not visibly demonstrated

- Policy-based model routing by capability, data residency/privacy, latency, reliability, and budget.
- RBAC/ABAC, tenant isolation, secret vaulting, sandboxing, allowlists, egress control, and approval policies.
- Idempotent workflow execution, queues, leases, retries, dead-letter handling, and disaster recovery.
- Versioned contracts for agents, models, tools, skills, memory records, and artifacts.
- Evaluation gates, prompt/model version provenance, reproducibility, and safe rollback.
- Accessible responsive UX, offline/local-first behavior where appropriate, and web/PWA/desktop parity rules.
- Data lineage, reconciliation, freshness indicators, accounting-period locks, and explicit “AI estimate” labels.

## Recommended differentiators

- **Policy router:** explain why a model/provider was selected and allow a user override within policy.
- **Execution receipt:** every action links intent, approval, inputs, tool calls, outputs, costs, and side effects.
- **Memory debugger:** show what was retrieved, why, its source, permissions, age, and correction/delete controls.
- **Artifact graph:** connect goals, tasks, sessions, sources, prompts, models, versions, and downstream uses.
- **Autonomy budget:** bound time, spend, tool scopes, and risk per run; pause automatically at thresholds.
- **Authoritative finance mode:** reconcile source-system facts before generating narrative, never posting AI values as accounting records.
- **Adapter SDK:** conformance tests and capability manifests for model, tool, MCP, storage, and business-system plugins.

## Priorities and boundary

### P0 — foundational/required

Identity/tenant boundaries; agent/model adapter contracts; durable task/run state; scoped tool execution; secrets; audit log; artifact store; permission-aware memory; approvals; baseline observability.

### P1 — strong MVP

Mission Control, sessions, projects/workspaces, goals/tasks, provider routing, tool/MCP registry, file/document artifacts, cost budgets, accessible responsive web UI, local-first single-node deployment with an upgrade path.

### P2 — post-MVP

Image/video/voice Studio, schedules/automations, team/crew orchestration, advanced evaluations, ERP/CRM/accounting read-only dashboards, desktop wrapper, PWA/offline enhancements, adapter marketplace.

### P3 — experimental

Hours-long high-autonomy goal mode, self-modifying skills, predictive profit recommendations, multi-agent swarms, and mobile action control. These require strong evaluation and safety evidence.

## Concepts to retain, adapt, reject

- **Retain:** unified shell, agent identity, visible workspaces, artifacts, goals, and media browsing.
- **Adapt:** card density, long sidebar, agent-centric navigation, “memory” into a transparent governed subsystem, and Studio into job-based asset management.
- **Reject:** implied “perfect memory,” unbounded autonomy, opaque profit claims, visual status without execution evidence, and any assumption that MCP connectivity equals safe authorization.

## Value

Users gain continuity, less tool switching, controlled delegation, searchable outputs, and understandable spend. Organizations gain governed AI operations, provider portability, auditability, reusable integrations, and safer linkage to operational and financial data.
