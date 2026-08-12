---
document_id: ADR-003
title: Product Information Architecture, Access Scope, Approval, Retention, and Durable Execution
version: 0.1.0
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-08-12
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PRD-001
  - SAD-001
  - DDD-001
  - DAT-001
  - DAT-002
  - MEM-001
  - API-001
  - RUN-001
  - APR-001
  - EVT-001
  - IAM-001
  - POL-001
  - SAN-001
  - ORC-001
  - PLG-001
  - AUD-001
related_adrs:
  - ADR-001
  - ADR-002
supersedes: []
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-12
    evidence: explicit user approval in project conversation
pending_approvals:
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
---

# ADR-003 — Product Information Architecture, Access Scope, Approval, Retention, and Durable Execution

## Status

**Draft — proposed baseline.** This ADR records the product and architecture decisions explicitly validated by the product owner on 2026-08-12. It is not approved until the required architecture, security, data, operations, and quality review is recorded.

## Context

Agent OS must centralize conversations and work performed through Agent OS while supporting both individual use and collaboration. The platform must preserve provider-neutral adapters, workspace isolation, durable execution, explicit authorization, human control, provenance, and long-lived records.

The decisions below resolve the previously open product-organization and orchestration questions. They refine, but do not silently rewrite, approved vision or technology decisions. Any conflict with an approved ADR is resolved only when this ADR is approved and explicitly supersedes the affected decision.

## Decisions

### 1. Product information hierarchy

Agent OS uses the following controlled hierarchy:

```text
Account
└── Workspace
    └── Project
        └── Mission
            └── Task
                └── Run
```

- A **Project** is a durable domain or body of work.
- A **Mission** is an outcome-oriented objective within a project.
- A **Task** is an executable unit of work with constraints and expected outputs.
- A **Run** is one durable execution of one task snapshot.
- A **Conversation** is an independent interaction thread. It may be private or linked to a project, mission, task, or run without being forced into the hierarchy.

This distinction prevents conversational exploration from being confused with an executable task while retaining traceability between intent, interaction, execution, and output.

### 2. Workspace types and isolation

Agent OS supports:

- **Personal workspace:** private by default and owned by one user.
- **Team workspace:** shared by members through explicit membership and resource permissions.

The workspace remains the primary isolation boundary for projects, conversations, memory, skills, plugins, tools, artifacts, policies, budgets, runs, and audit views. Workspace membership never grants access to every resource inside the workspace.

### 3. Conversation visibility

Conversation visibility has three levels:

- `private`: creator and explicitly authorized agents/services;
- `project`: members authorized for the linked project;
- `workspace`: members authorized for the workspace-level resource.

The default is `private`. Sharing is explicit and auditable. Access checks apply to the conversation, messages, attachments, derived memory, artifacts, and run evidence. A shared artifact does not automatically expose the source conversation.

### 4. Initial agent adapters

The initial adapter baseline contains Codex, Hermes, and Claude Code. Each adapter remains replaceable and must implement the versioned Agent Adapter Contract. Agent OS records only conversations and execution evidence that pass through its controlled adapter or interface boundary.

### 5. Approval and risk policy

Actions are classified as:

| Class | Examples | Default approval |
|---|---|---|
| `read` | Read or analyze permitted data | No |
| `generate` | Draft text, code, image, or analysis | No |
| `controlled_write` | Write within an isolated workspace | Configurable |
| `external_effect` | Send, publish, call a sensitive external API | Required |
| `destructive` | Delete, replace, migrate, or revoke | Required |
| `critical` | Deploy, production access, secret use, Git push | Required plus recent reauthentication |

Workspace policy may require stricter approval but cannot remove approval for `critical` actions. Approval is exact, expiring, single-use, auditable, and invalidated when the normalized action changes. Self-approval is not permitted for critical actions.

### 6. Retention and deletion baseline

- Conversations, artifacts, memory, and run metadata are retained until user or workspace policy requests deletion; archival is preferred for inactive content.
- Audit evidence for consequential actions has a configurable long-retention profile, with seven years as the initial product default where no stricter legal or organizational policy applies.
- Deleted content enters a 30-day recoverable deletion period, except compromised secrets, which are revoked immediately.
- Secrets are never stored in conversations, prompts, ordinary memory, artifacts, or logs.
- Search indexes, embeddings, previews, caches, and derived records follow the source record's deletion policy and must be removed or rebuilt after deletion.
- Backups use encrypted rotation policies defined by the deployment owner; backup retention does not silently override a valid deletion request beyond the documented recovery window.

These defaults are product proposals, not legal retention advice.

### 7. Durable orchestration

Temporal is the proposed durable orchestration engine for long-running workflows, approvals, timers, retries, pause/resume, cancellation, worker recovery, and event history. PostgreSQL remains the authoritative store for Agent OS business state, permissions, conversations, artifacts, memory metadata, and audit records. Redis may support cache, notifications, or auxiliary transport but is not the authoritative run history.

This decision supersedes the task-queue portion of ADR-001 only after this ADR is approved. Celery may remain for bounded auxiliary jobs if a later ADR documents the boundary.

### 8. Plugins and capabilities

Plugins may expose broad capabilities comparable to modern AI agents, including code, file, network, model, browser, MCP, and integration operations. Capability breadth does not bypass governance. Every plugin declares capabilities, data access, network access, filesystem access, secret needs, isolation profile, and effect semantics. The Tool Gateway, policy engine, sandbox, approval service, workspace scope, and audit layer remain mandatory.

## Consequences

### Positive

- Users receive a stable organization model without forcing every conversation into a task.
- Personal and team collaboration share one platform while retaining explicit privacy.
- Risk and approval behavior becomes predictable and testable.
- Temporal supports the long-running, interruptible, approval-gated execution model.
- Plugin extensibility remains powerful without granting implicit authority.

### Trade-offs

- The product model has more concepts and requires clear UI education.
- Per-conversation sharing requires fine-grained authorization and derived-data handling.
- Temporal adds an operational service to local deployments.
- Long retention increases storage, backup, and deletion-governance requirements.

## Required follow-up

1. Update controlled vocabulary, product requirements, domain model, IAM, policy, memory, artifact, plugin, audit, API, run, approval, event, deployment, and orchestration documents.
2. Add machine-readable visibility, risk, approval, retention, and correlation fields to contracts.
3. Create implementation and validation evidence before changing this ADR to `implemented`.
4. Record formal approvers before changing this ADR to `approved`.

## Approval state

The product owner explicitly approved this decision baseline on 2026-08-12. The ADR remains `in-review` pending the other designated approver roles. This record does not authorize implementation status or silently approve the related draft documents.

## Revision history

| Version | Date | Status | Change |
|---|---|---|---|
| 0.1.0 | 2026-08-12 | Draft | Initial validated product and architecture decision baseline |
| 0.1.1 | 2026-08-12 | In-review | Product-owner approval recorded; remaining approvers listed |
