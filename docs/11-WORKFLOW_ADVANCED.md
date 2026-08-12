---
document_id: ORC-002
title: Agent OS v2 Advanced Workflow Builder
version: 2.0.0
status: archived
owner: architecture-owner
approvers:
  - architecture-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents: [ORC-001, RUN-001, APR-001]
related_adrs: []
---

# Agent OS v2 / Advanced Workflow Builder

> **Document:** `11-WORKFLOW_ADVANCED.md`
> **Version:** 2.0.0
> **Status:** Draft
> **Date:** 2026-08-11
> **Classification:** Internal

---

## 1. Visual DAG Builder

### 1.1 Canvas Architecture

The workflow canvas is built on **React Flow** (`@xyflow/react`) or a custom D3 implementation, depending on performance requirements.

**Canvas spec:**
- Background: `#0D0D0F` grid with 20px spacing, subtle `--border-subtle` lines
- Zoom: 25% to 200%, mouse wheel + pinch gesture
- Pan: Click-drag on empty canvas
- Selection: Box select (Shift+drag) or click individual nodes
- Undo/Redo: Full history stack (Cmd+Z / Cmd+Shift+Z)
- Auto-layout: Dagre or ELK.js for automatic node positioning

**Performance targets:**
- Render <1s for workflows with ≤50 nodes
- 60fps during drag operations
- Mini-map updates throttled to 100ms

### 1.2 Node Types

| Type | Shape | Icon | Purpose |
|---|---|---|---|
| **Start** | Rounded rect, 3px `--brand-bright` top border | `PlayCircle` | Entry point, exactly one per workflow |
| **Task** | Rounded rect, 3px left border in agent color | `Bot` | Assign task to agent with prompt template |
| **Condition** | Diamond shape, `--status-ready` border | `GitBranch` | If/else branch based on expression |
| **Loop** | Rounded rect with circular arrow icon | `Repeat` | Repeat N, while/until, or iterate collection |
| **Approval Gate** | Rounded rect with shield icon, `--status-stale` border | `ShieldCheck` | Pause for human review |
| **Delay/Wait** | Rounded rect with clock icon | `Timer` | Wait N seconds/minutes/hours |
| **Trigger (Cron)** | Rounded rect with clock icon, `--agent-crystal` border | `Clock` | Scheduled execution |
| **Trigger (Webhook)** | Rounded rect with webhook icon, `--agent-crystal` border | `Webhook` | External HTTP trigger |
| **End** | Rounded rect with check icon, `--status-success` border | `CheckCircle` | Terminal node |

### 1.3 Node Data Model

```typescript
interface WorkflowNode {
  id: string;                    // UUID
  type: 'start' | 'task' | 'condition' | 'loop' | 'approval' | 'delay' | 'trigger_cron' | 'trigger_webhook' | 'end';
  config: {
    name: string;
    description?: string;
    // Task-specific
    agent_id?: string;
    prompt_template?: string;
    timeout_seconds?: number;    // default 300
    retry_policy?: {
      max_retries: number;       // default 3
      backoff_multiplier: number; // default 2
      initial_delay_ms: number;   // default 1000
    };
    // Condition-specific
    condition_expression?: string; // e.g., "{{score}} > 8"
    // Loop-specific
    loop_type?: 'repeat_n' | 'while' | 'for_each';
    loop_count?: number;
    loop_collection?: string;    // variable name for for_each
    // Approval-specific
    approvers?: string[];         // user IDs or role names
    expiry_minutes?: number;     // default 1440 (24h)
    // Trigger-specific
    cron_expression?: string;
    webhook_path?: string;
    webhook_method?: 'GET' | 'POST' | 'PUT' | 'PATCH';
    webhook_secret?: string;      // for HMAC verification
    // Delay-specific
    delay_seconds?: number;
  };
  position: { x: number; y: number };
  width?: number;
  height?: number;
  metadata?: Record<string, unknown>;
}
```

### 1.4 Edge Types

| Type | Style | Label |
|---|---|---|
| **Success** | Solid, 2px, `--status-success` | "success" |
| **Failure** | Dashed, 2px, `--status-offline` | "failure" |
| **Conditional** | Solid, 2px, `--status-ready` | Expression result (true/false) |
| **Default** | Solid, 2px, `--border-default` | (no label) |

**Edge Data Model:**

```typescript
interface WorkflowEdge {
  id: string;                    // `${source}__${target}`
  source: string;               // node ID
  target: string;               // node ID
  type: 'success' | 'failure' | 'conditional' | 'default';
  label?: string;
  condition_expression?: string; // for conditional edges
  animated?: boolean;            // true when data flows
  metadata?: Record<string, unknown>;
}
```

---

## 2. Conditional Logic

### 2.1 Expression Engine

**Simple expressions** (default):
- Syntax: Jinja2-style variable substitution with comparison operators
- Examples: `{{score}} > 8`, `{{status}} == "approved"`, `{{items}} | length > 0`
- Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `in`, `not in`, `and`, `or`, `not`
- Functions: `length`, `contains`, `starts_with`, `ends_with`, `match` (regex)

**Advanced expressions** (opt-in):
- JavaScript sandbox via QuickJS or isolated-vm
- Full JS expression evaluation with 100ms timeout
- No network access, no filesystem access, no `require`/`import`
- Memory limit: 64MB per expression

### 2.2 Branch Visualization

- Conditional edges show labels: "true", "false", or custom text
- Unmatched conditions highlight in `--status-stale` with warning icon
- Expression tester: Evaluate against sample JSON payload without executing workflow
- Typeahead autocomplete for available variables in expression editor

---

## 3. Loop Constructs

### 3.1 Repeat N Times

Execute child workflow N times, with access to `{{loop.index}}` and `{{loop.total}}`.

### 3.2 Repeat While / Until

Execute while condition is true (pre-check) or until condition becomes true (post-check). Max iterations enforced at workflow level.

### 3.3 Iterate Over Collection

For each item in a collection variable, execute child workflow with `{{item}}` and `{{loop.index}}`.

**Loop safety:**
- Maximum iterations: 100 (configurable per workflow)
- Infinite loop detection: execution timeout halts after 10 minutes
- Break node: exits loop early
- Continue node: skips to next iteration

---

## 4. Approval Gates

### 4.1 Gate Behavior

When execution reaches an Approval Gate node:

1. **Pause:** Run state changes to `waiting_for_approval`
2. **Notify:** Notifications sent to configured approvers (in-app, email, Slack)
3. **Present:** Approval modal shows action preview, parameters, and context
4. **Decide:** Approver chooses approve, reject, or request revision
5. **Resume:** On approve, execution continues with decision context added to variables
6. **Halt:** On reject, execution follows "failure" branch or terminates

### 4.2 Approval Context

The approval request includes:
- Workflow name and current node
- Action preview (what will happen if approved)
- Parameters (sanitized if containing secrets)
- Requesting agent and run ID
- Deadline (configurable, default 24 hours)

### 4.3 Human Review UI

See Design System document (§8.3) for Approval Gate UI specifications.

---

## 5. Triggers

### 5.1 Cron Scheduler

- Visual cron builder (no raw cron strings required for basic schedules)
- Timezone per schedule (default workspace timezone)
- Next-run preview: show next 5 execution times
- Skip policy: `skip` (if previous still running) or `queue`
- Daylight saving awareness

### 5.2 Webhook Receiver

- Configurable path segment: `/webhooks/{workflow_id}/{webhook_path}`
- HTTP methods: POST, PUT, PATCH (GET for simple triggers)
- HMAC-SHA256 signature verification: `X-Webhook-Signature` header
- Payload validation against JSON Schema
- Rate limiting: 60 req/min per webhook
- Response: `202 Accepted` with run ID; async execution

### 5.3 Manual Trigger

- "Run Now" button in workflow builder
- Optional parameter override before execution

### 5.4 Event Trigger

- Subscribe to platform events: `note.created`, `ranking.changed`, `artifact.created`, `task.completed`
- Event filter: match on event type, workspace, and optional payload conditions
- Debounce: configurable cooldown period (default 60s)

---

## 6. Simulation Mode

### 6.1 Dry-Run Execution

- Execute workflow without calling external APIs or agent models
- Mock responses generated based on node type and config
- Task nodes return placeholder text; condition nodes evaluate expressions against sample data
- All execution paths explored for validation

### 6.2 Step-Through

- Pause after each node completion
- "Next" button advances one node
- "Back" button rewinds to previous node
- State snapshot at each step

### 6.3 Variable Inspector

- Panel showing all variables in current execution context
- JSON tree view with collapsible sections
- Highlight variables modified in current step
- Search/filter by variable name

### 6.4 Breakpoint Debugging

- Set breakpoints on any node
- Execution pauses before node runs
- Inspect variables, modify values, then continue or skip node
- Conditional breakpoints: pause only when expression evaluates to true

---

## 7. Workflow Marketplace

### 7.1 Import / Export

**Export:**
- Format: YAML (human-friendly) or JSON (machine-friendly)
- Includes: nodes, edges, config, metadata, version
- Excludes: workspace-specific data (agent IDs mapped by name)

**Import:**
- Validation: schema check, DAG acyclicity, node type support
- Conflict resolution: rename, replace, or skip existing workflows
- Preview before import

### 7.2 Community Gallery

- Optional public sharing of workflow templates
- Star ratings, usage counts, author attribution
- Fork workflow to own workspace
- Curated collections (SEO, DevOps, Content, etc.)

### 7.3 Version Control

- Each workflow tracks versions (auto-increment on save)
- Diff view between versions
- Rollback to any previous version
- Branch: create experimental copy without affecting active version

---

## 8. Error Handling

### 8.1 Retry with Exponential Backoff

Default retry policy per node:
- Max retries: 3
- Initial delay: 1s
- Backoff multiplier: 2 (1s, 2s, 4s)
- Jitter: ±25% randomization to avoid thundering herd

Retry applies to:
- External API calls (SERP, CMS, model providers)
- Agent task execution failures
- Network timeouts

### 8.2 Dead-Letter Queue

Failed nodes that exhaust retries are moved to a dead-letter queue:
- Original payload preserved
- Failure reason and stack trace logged
- Manual retry or edit-and-retry options
- Alert sent to workspace operators after 3 DLQ items in 1 hour

### 8.3 Fallback Branches

Nodes can define fallback edges:
- Primary edge: success path
- Fallback edge: triggered on specific error types (timeout, rate_limit, auth_error)
- Fallback can route to alternative agent, alternative provider, or human escalation

### 8.4 Alert on Repeated Failure

- Configurable threshold: e.g., "alert if same workflow fails 3 times in 24 hours"
- Alert channels: in-app notification, email, webhook
- Alert includes: workflow name, failure node, error summary, last successful run timestamp

---

## 9. Data Model

See `05-DATA_MODEL.md` §4.23–4.27 for workflow builder tables:
- `workflow_templates`
- `workflow_nodes`
- `workflow_edges`
- `workflow_executions`
- `workflow_schedules`

---

*End of Advanced Workflow Builder Document*
