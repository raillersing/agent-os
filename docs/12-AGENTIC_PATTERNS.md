# Agent OS v2 — Goldie Edition / Agentic Patterns

> **Document:** `12-AGENTIC_PATTERNS.md`  
> **Version:** 2.0.0  
> **Status:** Draft  
> **Date:** 2026-08-11  
> **Classification:** Internal

---

## 1. Dynamic Agent Roles

### 1.1 Role Definition Schema

A **role** is a configurable identity template that agents can assume. Roles are not agents — they are hats that agents wear.

```typescript
interface AgentRole {
  id: string;                    // UUID
  workspace_id: string;           // scope
  name: string;                   // e.g., "Senior Editor"
  slug: string;                   // URL-safe identifier
  description: string;
  icon: string;                   // Lucide icon name or uploaded image URL
  color: string;                  // Hex color for UI theming
  default_agent_id?: string;     // preferred agent if no assignment
  skills: string[];              // skill IDs required/associated
  system_prompt_template: string; // Jinja2 template with role variables
  memory_profile: {
    episodic_weight: number;      // 0.0–1.0, default 0.7
    semantic_weight: number;     // 0.0–1.0, default 0.3
    decay_half_life_days: number; // default 30
  };
  autonomy_level: 'full' | 'suggest' | 'confirm_each' | 'manual';
  config_json: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}
```

**System prompt template variables:**
- `{{role_name}}` — role display name
- `{{agent_name}}` — assigned agent's name
- `{{workspace_name}}` — current workspace
- `{{skills}}` — list of associated skills
- `{{autonomy_level}}` — current autonomy setting

### 1.2 Agent Assignment

Many-to-many relationship between agents and roles:

- One agent can hold multiple roles (with priority order)
- One role can have multiple assigned agents
- Assignment includes: `priority` (1 = highest), `is_active`, `assigned_at`, `assigned_by`
- Runtime selection: highest-priority active agent for the role is chosen

**Assignment resolution:**
1. Filter to active assignments for the role
2. Sort by priority ascending
3. Check agent health (online/reachable)
4. Select first healthy agent
5. If no healthy agents, queue task with retry

### 1.3 Runtime Switching

Users can change an agent's role mid-conversation:

1. User clicks "Switch Role" in chat header
2. System shows available roles for current agent
3. User selects new role
4. System:
   - Preserves last 20 messages as context
   - Loads new role's system prompt template
   - Replaces agent's current system prompt
   - Adds system message: "Role switched to {new_role} at {timestamp}"
   - Logs switch event in session metadata

**Constraints:**
- Switch is atomic (no message generation during switch)
- Agent must be assigned to the target role
- Switch count limited to 10 per session (configurable)

### 1.4 Role Analytics

Dashboard metrics per role:

| Metric | Description |
|---|---|
| Usage count | Times role was assigned to a task |
| Success rate | % of tasks completed without failure |
| Avg cost | Mean token cost per task |
| Avg latency | Mean time from assignment to completion |
| Top tasks | Most frequent task types for this role |
| Agent distribution | Which agents are most often assigned |
| Trend | 30-day usage chart |

---

## 2. Delegation Protocol

### 2.1 Structured Delegation

When Crystal (or any orchestrator) delegates a task, the message is a structured object:

```json
{
  "delegation_id": "uuid",
  "task": {
    "title": "Write landing page copy",
    "description": "Create conversion-focused copy for the pricing page",
    "requirements": ["Include 3 pricing tiers", "CTA above the fold"]
  },
  "context": {
    "session_id": "uuid",
    "previous_messages": ["..."],
    "relevant_memories": ["..."],
    "workspace_preferences": { "tone": "professional", "brand_voice": "..." }
  },
  "deadline": "2026-08-15T17:00:00Z",
  "success_criteria": [
    "Copy is between 200-400 words",
    "Includes all 3 pricing tiers",
    "Passes Two-Lane Verifier"
  ],
  "output_format": {
    "type": "markdown",
    "sections": ["headline", "subheadline", "body", "cta"]
  },
  "approval_needed": true,
  "escalation_policy": {
    "on_timeout": "notify_owner",
    "on_failure": "retry_once_then_escalate"
  }
}
```

### 2.2 Agent Acceptance

The receiving agent can:
- **Accept:** Begin execution immediately
- **Reject with reasoning:** Explain why task cannot be handled (missing skills, capacity, conflict)
- **Request clarification:** Ask for more information before accepting
- **Propose alternative:** Suggest a modified task that fits capabilities

### 2.3 Progress Reporting

During execution, the agent reports back to the orchestrator:

```json
{
  "report_type": "progress",
  "delegation_id": "uuid",
  "status": "in_progress",
  "completed_steps": 2,
  "total_steps": 5,
  "current_step": "Drafting body copy",
  "partial_output": "…preview…",
  "estimated_completion": "2026-08-12T14:30:00Z",
  "blocked_by": null
}
```

Report types: `started`, `progress`, `blocked`, `completed`, `failed`

### 2.4 Handoff Protocol

When an agent is overloaded or failing:

1. Orchestrator detects high latency or error rate
2. Initiates handoff: proposes alternative agent with same role
3. Transfers context: full delegation object + execution state + partial outputs
4. New agent accepts or rejects handoff
5. Original agent is notified and relieved

---

## 3. Reflection Loop

### 3.1 Post-Task Reflection

After each task completion, the agent writes a reflection:

```json
{
  "reflection_id": "uuid",
  "agent_id": "uuid",
  "task_id": "uuid",
  "run_id": "uuid",
  "what_worked": ["The outline structure was clear", "Client approved on first review"],
  "what_did_not_work": ["Took too long to find the right tone", "Had to regenerate image twice"],
  "what_to_improve": ["Pre-load brand voice examples", "Use faster image provider"],
  "confidence": 0.85,
  "created_at": "2026-08-11T14:00:00Z"
}
```

### 3.2 Personal Memory

Reflections are stored in the agent's **personal memory** — not in the shared workspace vault. This ensures:
- Agent learns from its own experience without polluting shared knowledge
- Reflections can be candid (not subject to workspace governance)
- Agent-specific learning is portable if the agent is reassigned

### 3.3 Periodic Synthesis

Weekly and monthly reflection synthesis:

- **Weekly:** Aggregate top 5 patterns from reflections → suggest prompt adjustments
- **Monthly:** Deep analysis of recurring failures → propose skill additions or workflow changes
- **System prompt updates:** Optional automatic injection of synthesized learnings into agent's system prompt (with user approval)

---

## 4. Swarm Mode

### 4.1 Multi-Agent Collaboration

For complex tasks, multiple agents collaborate in real time with defined roles:

| Swarm Role | Responsibility | Typical Agent |
|---|---|---|
| **Lead** | Coordinates swarm, makes final decisions, resolves conflicts | Crystal |
| **Researcher** | Gathers information, fact-checks, finds sources | Claude / Kimi |
| **Writer** | Produces drafts, follows briefs, maintains tone | Alex |
| **Reviewer** | Evaluates quality, suggests improvements, catches errors | Joe |
| **Fact-Checker** | Verifies claims against sources, flags inaccuracies | Claude |

### 4.2 Shared Workspace

During swarm execution, agents share a **collaborative context**:

- Real-time message bus (Redis pub/sub or WebSocket)
- Shared scratchpad: markdown document all agents can append to
- Lock mechanism: only one agent can modify a section at a time
- Version history: every edit tracked with agent attribution

### 4.3 Consensus Mechanism

Before final output is produced:

1. Writer submits draft to shared workspace
2. Reviewer evaluates against criteria (quality, completeness, tone)
3. Fact-Checker verifies all claims
4. If Reviewer rejects: draft returns to Writer with comments
5. If Fact-Checker flags issues: Writer corrects or removes claims
6. Lead approves final version or escalates to human

**Consensus rules:**
- Reviewer approval is mandatory for final output
- Fact-Checker flags block publication until resolved
- Lead can override Reviewer with explicit reasoning (logged)

---

## 5. Memory Profiles

### 5.1 Memory Types

Each agent maintains three memory layers:

| Type | Content | Storage | Retrieval |
|---|---|---|---|
| **Episodic** | Conversations, task executions, reflections | Personal memory table | Semantic search + recency |
| **Semantic** | Facts, concepts, relationships learned | Personal memory table | Semantic search |
| **Procedural** | Skills, workflows, patterns learned | `role_skills` + `agent_reflections` | Direct lookup |

### 5.2 Memory Decay

Older memories lose importance unless reinforced:

```
importance_score = base_importance × (0.5 ^ (days_since_last_access / half_life))
```

- Default half-life: 30 days
- Accessing a memory refreshes its timestamp
- High-importance memories (marked by agent or user) have extended half-life (90 days)
- Expired memories moved to `archived` state, not deleted

### 5.3 Memory Sharing

Agents can voluntarily share memories:

- Agent A extracts a memory as a "lesson learned"
- Agent A proposes sharing with Agent B
- Agent B receives shared memory with source attribution
- Agent B can accept (incorporates into own memory) or reject
- Shared memories marked with `shared_from_agent_id`

---

## 6. Human-in-the-Loop Patterns

### 6.1 Autonomy Levels

Users can configure autonomy per role, per agent, or per task:

| Level | Behavior | Use Case |
|---|---|---|
| **Fully Autonomous** | Agent executes without asking; only alerts on failure | Trusted, repetitive tasks |
| **Suggest** | Agent proposes action, executes after brief delay unless stopped | Semi-trusted workflows |
| **Confirm Each Step** | Agent pauses before each significant action, waits for approval | Sensitive operations |
| **Manual Only** | Agent provides analysis and recommendations; human executes | High-stakes decisions |

### 6.2 Escalation

Agents escalate to humans when:

- Confidence score < configured threshold (default 0.7)
- Task failure after max retries
- Ambiguous requirements that need clarification
- Detected conflict with workspace policy
- Approval gate reached in workflow

**Escalation methods:**
- In-app notification with action buttons
- Email (if configured)
- Slack DM or channel message (if connected)

### 6.3 Override

Humans can override any running agent:

- **Pause:** Freeze agent execution immediately
- **Redirect:** Change task parameters or reassign to different agent
- **Inject:** Add context or instructions mid-execution
- **Terminate:** Cancel execution with reason
- **Rollback:** Revert to previous checkpoint and retry

All overrides are logged as audit events with full context snapshot.

---

## 7. Data Model

See `05-DATA_MODEL.md` §4.28–4.33 for agentic patterns tables:
- `agent_roles`
- `agent_role_assignments`
- `role_skills`
- `agent_reflections`
- `swarm_sessions`
- `swarm_participants`

---

*End of Agentic Patterns Document*
