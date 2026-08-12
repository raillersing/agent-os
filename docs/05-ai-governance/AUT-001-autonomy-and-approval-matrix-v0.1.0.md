---
document_id: AUT-001
title: Agent OS Autonomy and Approval Matrix
version: 0.2.0
status: draft
owner: product-owner
approvers:
  - product-owner
  - security-owner
  - architecture-owner
  - operations-owner
created: 2026-07-19
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PER-001
  - UCD-001
  - PRD-001
  - SRS-001
  - NFR-001
  - IAM-001
  - POL-001
  - HUM-001
  - SEC-001
  - THR-001
  - SAN-001
  - APR-001
  - RUN-001
  - AUD-001
related_adrs: []
related_evidence:
  - VIDEO-003
  - VIDEO-004
---

# AUT-001 — Agent OS Autonomy and Approval Matrix

> **Status: Draft.** This document defines the proposed autonomy and approval policy baseline for the first Agent OS MVP. It does not grant real permissions, prove that controls exist, authorize production or financial actions, or replace identity, security, sandbox, approval-contract, or incident-response design.

## 1. Document purpose

This document establishes:

- the permitted levels of agent autonomy;
- the risk classes used to classify actions;
- the default policy decisions for representative action classes;
- which actions may execute automatically;
- which actions require human approval;
- which actions are prohibited in the MVP;
- who may approve each action;
- when an independent second human is required;
- mobile approval limits;
- standing-grant limits;
- approval lifecycle, expiry, invalidation, and replay rules;
- emergency stop and revocation behavior;
- agent delegation and self-approval prohibitions;
- evidence and audit obligations.

It is the primary governance input to:

- `IAM-001`;
- `POL-001`;
- `HUM-001`;
- `SEC-001`;
- `THR-001`;
- `SAN-001`;
- `APR-001`;
- `RUN-001`;
- `AGC-001`;
- `TST-001`;
- `RTM-001`.

## 2. Scope

This policy applies to:

- human users;
- agent identities;
- adapter and worker identities;
- tools, MCP servers, integrations, and plugins;
- tasks, runs, and run steps;
- files and repositories;
- model/provider use;
- memory and artifacts;
- Git and external messaging;
- identity, role, budget, and policy changes;
- backups and restore;
- audit and evidence;
- local deployment and operations.

The first MVP remains:

- local and single-node;
- one organization context;
- multiple isolated workspaces;
- one primary operator or a small trusted team;
- Hermes and Codex as initial adapter targets;
- non-public by default;
- non-production;
- read-only toward future business systems;
- without production financial posting;
- without autonomous merge;
- without unrestricted host control.

## 3. Governing principles

1. **Authority comes from policy, not prompts.**
2. **Connection does not equal permission.**
3. **Capability does not equal authorization.**
4. **Agents cannot approve their own actions.**
5. **Human approval must bind to an exact action.**
6. **Material changes invalidate approval.**
7. **Approval is one-time unless a narrower standing grant is explicitly allowed.**
8. **Unknown risk fails closed or enters human review.**
9. **Least privilege is the default.**
10. **Workspace boundaries apply before relevance, routing, or tool execution.**
11. **Consequential actions require more evidence than reversible reads.**
12. **Cancellation revokes future work but does not imply rollback.**
13. **A safer reduction of authority is not treated the same as an expansion.**
14. **Security and integrity override convenience, speed, and cost.**
15. **The agent that proposes an action cannot be the human approver.**
16. **Production, financial, and public effects remain excluded unless explicitly added by future approved scope.**

## 4. Key terms

### Autonomous action

An action executed without a per-action human decision because an active policy already permits it within exact bounds.

### Approval-required action

An action that remains blocked until an eligible human approves the exact proposal.

### Standing grant

A time-bounded policy grant allowing a narrow class of repeatable actions without per-action approval.

### Consequential action

An action that can materially change code, data, permissions, external systems, public content, finances, production state, or access.

### Requester

The human or workload identity proposing or initiating the action.

### Approver

An eligible human identity deciding whether the exact action may proceed.

### Consumption

The atomic use of a valid approval to authorize one execution attempt.

### Independence

The required separation between requester and approver.

## 5. Autonomy levels

| Level | Name | Meaning | MVP use |
|---|---|---|---|
| `L0` | Prohibited | The action cannot be executed by Agent OS in ordinary MVP operation | Critical exclusions |
| `L1` | Observe | Read, inspect, classify, or summarize authorized information | Low-risk reads |
| `L2` | Draft / prepare | Create proposals, drafts, plans, or non-authoritative artifacts | Default safe delegation |
| `L3` | Guarded execution | Execute a bounded, reversible, pre-authorized action under active policy | Selected low/moderate-risk actions |
| `L4` | Approval-gated execution | Execute only after exact human approval | Consequential actions |
| `L5` | High-autonomy orchestration | Long-running or delegated multi-step authority across broad capabilities | Post-MVP; not available |

Rules:

- `L3` does not allow permission expansion.
- `L4` still requires all normal policy, sandbox, data, budget, and audit checks.
- `L5` is not approved merely because a UI exposes goals or agent teams.
- An agent may operate below the maximum permitted level.
- A workspace policy may reduce, but not exceed, the platform maximum.

## 6. Risk classes

| Class | Description | Typical examples | Default outcome |
|---|---|---|---|
| `R0` | Informational, no material side effect | Read public metadata, view state | Allow |
| `R1` | Low risk, bounded, reversible or draft-only | Read authorized file, create draft artifact | Allow with guards |
| `R2` | Moderate risk, local and bounded, recoverable | Start bounded run, run tests, archive output | Guarded execution or approval depending on context |
| `R3` | Consequential | Commit, push, external send, delete, secret use, permission change | Exact human approval |
| `R4` | Critical or excluded | Merge, force push, production write, financial posting, arbitrary shell, disable audit | Deny in MVP |

Risk is increased by:

- broader workspace/resource scope;
- confidential or secret data;
- external destination;
- irreversible effect;
- public visibility;
- production or financial impact;
- permission expansion;
- unknown side-effect state;
- high cost;
- bulk action;
- weak recoverability;
- changed parameters after review;
- mobile/untrusted device;
- unverified tool, adapter, plugin, or destination.

## 7. Policy decision outcomes

| Decision | Meaning |
|---|---|
| `ALLOW` | Action may proceed because it is low risk and fully authorized |
| `ALLOW_WITH_GUARDS` | Action may proceed only after mandatory preflight controls pass |
| `REQUIRE_APPROVAL` | Action remains blocked until exact human approval |
| `DENY` | Action cannot proceed under the current scope/policy |
| `UNKNOWN` | Policy cannot classify safely; treated as deny or approval-review according to stricter security policy |

## 8. Approver independence levels

| Level | Requirement |
|---|---|
| `I0` | No human approval required |
| `I1` | An eligible human must approve; in the single-user pilot, the same person may be requester and approver only through a distinct explicit manual decision |
| `I2` | A different human identity from the requester is required |
| `I3` | Dual approval by two distinct eligible humans would be required; not implemented in the MVP |

Rules:

- An agent, worker, adapter, or integration identity never satisfies `I1`, `I2`, or `I3`.
- Self-approval through an automated rule is not a human decision.
- Privilege escalation for the requester should require `I2`.
- Production, financial, broad-publication, destructive restore, and security-policy changes require `I2` or remain denied.
- The first single-user pilot may not execute actions whose minimum acceptable independence is unavailable.

## 9. Eligible approval authorities

| Authority | Example responsibility |
|---|---|
| Product Owner | Product scope, public outcome, exceptional product risk |
| Workspace Owner | Workspace membership, budget, workspace-level actions |
| Technical Operator | Adapters, models, tools, local operations |
| Security Owner | Secrets, network, sandbox, sensitive permissions, policy |
| Repository Maintainer | Commit, push, PR, branch operations |
| Data / Knowledge Owner | Memory authority, deletion, data classification |
| Operations Owner | Backup, restore, deployment, recovery |
| Communication Owner | External e-mail, message, publication |
| Business Data Owner | Future read-only ERP/CRM/accounting access |
| Budget Owner | Budget and cost-limit changes |
| Calendar Owner | Calendar side effects |
| Auditor | Evidence export where delegated; not operational approval by default |

Possessing one authority does not imply all others.

## 10. Approval object requirements

Every approval request must contain:

- stable request identifier;
- requester identity and type;
- organization and workspace;
- task, run, and step;
- action class;
- exact parameters;
- normalized target;
- action hash or immutable version;
- risk class;
- policy reason;
- expected effects;
- reversibility and rollback limitations;
- diff or preview where relevant;
- data classification;
- network destination where relevant;
- model/tool/adapter identity where relevant;
- estimated cost impact where available;
- expiry;
- eligible approval authority;
- independence requirement;
- evidence gaps;
- linked prior request if revised.

## 11. Approval lifecycle

```text
requested
  → under-review
  → approved
  → consumed

requested / under-review
  → rejected
  → revision-requested
  → expired
  → cancelled

approved
  → invalidated
  → expired
  → consumed
```

An approved action can still fail. Approval means “authorized to attempt,” not “completed successfully.”

## 12. Approval validity rules

An approval is valid only when:

1. the approver is currently authenticated;
2. the approver has the required authority;
3. the independence requirement is satisfied;
4. the request is unexpired and not cancelled;
5. the action hash and parameters match;
6. the target matches;
7. the policy version remains applicable;
8. relevant workspace membership and permissions remain valid;
9. prerequisite data/tool/model/secret grants remain valid;
10. the approval has not been consumed;
11. the action has not materially changed;
12. no emergency stop or revocation blocks execution.

## 13. Material-change invalidation

A new approval is required when any of the following changes materially:

- target repository, branch, file, record, environment, recipient, or destination;
- command or action type;
- parameters;
- diff or content;
- package name, source, version, or permissions;
- secret or provider account;
- data classification;
- workspace;
- cost/time/step limit beyond the approved bound;
- public audience;
- production/financial impact;
- approval policy;
- requester or executing identity;
- retry attempt after unknown side effect;
- restore source or target.

## 14. Standing grants

Standing grants may be used only for narrow, repeatable `R0`, `R1`, or selected `R2` actions.

A standing grant must define:

- identity or workload;
- organization/workspace;
- capability;
- exact resource scope;
- read/write mode;
- data classes;
- network destinations;
- cost limit;
- time window;
- maximum attempts/steps;
- expiry;
- revocation path;
- audit requirements;
- excluded action classes.

Standing grants are prohibited for:

- raw secret disclosure;
- production access;
- financial posting;
- merge, force push, or history rewrite;
- public publication;
- destructive database operations;
- broad permission expansion;
- audit/sandbox/approval disablement;
- arbitrary shell execution;
- cross-workspace access;
- self-modifying skills.

## 15. Default action matrix

| ID | Domain | Action | Risk | Max level | Decision | Approver | Independence | Mobile |
|---|---|---|---|---|---|---|---|---|
| `ACT-001` | Workspace data | Read authorized workspace metadata | `R0` | `L1` | `ALLOW` | None | `I0` | Allowed |
| `ACT-002` | Workspace data | Read authorized project files or repository content | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-003` | Workspace data | Search authorized tasks, runs, artifacts, audit, or memory | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-004` | Task management | Create or update a draft task | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-005` | Task management | Mark a task ready | `R2` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-006` | Run control | Start a bounded run | `R2` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-007` | Run control | Cancel a run | `R2` | `L2` | `ALLOW_WITH_GUARDS` | Operator or Workspace Owner when not requester-authorized | `I1` | Allowed |
| `ACT-008` | Run control | Retry an idempotent low-risk step | `R2` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-009` | Run control | Resume from a verified checkpoint | `R2` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-010` | Run control | Retry or resume a consequential step | `R3` | `L4` | `REQUIRE_APPROVAL` | Action-domain approver | `I1` | Approval restricted |
| `ACT-011` | Artifacts | Create a draft text/Markdown/JSON/code-patch/test-log artifact | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-012` | Artifacts | Accept an artifact as reviewed output | `R2` | `L3` | `REQUIRE_APPROVAL` | Workspace Owner or delegated Reviewer | `I1` | Allowed with trusted device |
| `ACT-013` | Artifacts | Publish artifact outside the workspace | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner plus Publication authority | `I2 for public publication` | Not allowed by default |
| `ACT-014` | Artifacts | Delete artifact content or metadata | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner or Data Owner | `I1` | Not allowed by default |
| `ACT-015` | Artifacts | Archive or supersede an artifact | `R2` | `L3` | `ALLOW_WITH_GUARDS` | Workspace Owner or delegated Reviewer | `I1` | Allowed |
| `ACT-016` | Memory | Write temporary working context | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-017` | Memory | Write durable generated memory under pre-approved type | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-018` | Memory | Promote memory to verified or authoritative status | `R3` | `L4` | `REQUIRE_APPROVAL` | Knowledge/Data Owner | `I1` | Not allowed by default |
| `ACT-019` | Memory | Correct or supersede memory | `R2` | `L3` | `REQUIRE_APPROVAL` | Knowledge/Data Owner or Workspace Owner | `I1` | Allowed |
| `ACT-020` | Memory | Delete durable memory | `R3` | `L4` | `REQUIRE_APPROVAL` | Data Owner or Workspace Owner | `I1` | Not allowed by default |
| `ACT-021` | Local files | Create or modify an approved working file inside a sandbox | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-022` | Local files | Delete an approved working file | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner or Repository Maintainer | `I1` | Not allowed by default |
| `ACT-023` | Local files | Access a file outside approved workspace mounts | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-024` | Command execution | Run an approved read-only diagnostic command | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-025` | Command execution | Run approved tests or build inside sandbox | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-026` | Command execution | Run an arbitrary shell command | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-027` | Dependencies | Install a package or executable dependency | `R3` | `L4` | `REQUIRE_APPROVAL` | Technical Operator plus Security Owner for executable plugins | `I1; I2 for untrusted source` | Not allowed by default |
| `ACT-028` | Dependencies | Upgrade an approved dependency within pinned policy | `R3` | `L4` | `REQUIRE_APPROVAL` | Technical Operator | `I1` | Not allowed by default |
| `ACT-029` | Network | Call an approved model/provider endpoint | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-030` | Network | Call an approved read-only external API | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-031` | Network | Send data to an unapproved destination | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-032` | Secrets | Use a secret reference through an approved capability | `R3` | `L4` | `REQUIRE_APPROVAL` | Secret Owner or Security Owner | `I1` | Not allowed by default |
| `ACT-033` | Secrets | Display, export, copy, or store a raw secret | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-034` | Git | Read Git status, log, diff, or branch metadata | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-035` | Git | Create or modify an uncommitted patch in approved worktree | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-036` | Git | Create a Git commit | `R3` | `L4` | `REQUIRE_APPROVAL` | Repository Maintainer or Workspace Owner | `I1` | Not allowed by default |
| `ACT-037` | Git | Push a branch | `R3` | `L4` | `REQUIRE_APPROVAL` | Repository Maintainer | `I1` | Not allowed by default |
| `ACT-038` | Git | Create a pull request | `R3` | `L4` | `REQUIRE_APPROVAL` | Repository Maintainer or Product Owner | `I1` | Not allowed by default |
| `ACT-039` | Git | Merge a pull request | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-040` | Git | Force push, delete protected branch, rewrite shared history | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-041` | Messaging | Draft an external e-mail or message | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-042` | Messaging | Send an external e-mail or message | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner or Communication Owner | `I1; I2 for broad/public audience` | Not allowed by default |
| `ACT-043` | Calendar | Create or modify a calendar event with invitees | `R3` | `L4` | `REQUIRE_APPROVAL` | Calendar Owner | `I1` | Not allowed by default |
| `ACT-044` | Calendar | Read authorized calendar availability | `R2` | `L3` | `ALLOW_WITH_GUARDS` | None | `I0` | Review only by default |
| `ACT-045` | Business systems | Read approved ERP/CRM/accounting data | `R3` | `L3` | `REQUIRE_APPROVAL` | Business Data Owner | `I1` | Not allowed by default |
| `ACT-046` | Business systems | Write or modify ERP/CRM/accounting records | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-047` | Financial | Create, modify, approve, or post a financial transaction | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-048` | Production | Access a production system | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-049` | Database | Read approved local Agent OS application data through governed API | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-050` | Database | Execute destructive database operation | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-051` | Database | Apply an approved application migration | `R3` | `L4` | `REQUIRE_APPROVAL` | Technical Operator plus Data/Operations Owner | `I1; I2 when destructive` | Not allowed by default |
| `ACT-052` | Backups | Create a backup | `R2` | `L3` | `ALLOW_WITH_GUARDS` | Technical Operator when schedule/manual | `I1` | Review only by default |
| `ACT-053` | Backups | Restore a backup | `R4` | `L4` | `REQUIRE_APPROVAL` | Technical Operator plus Operations/Data Owner | `I2` | Not allowed |
| `ACT-054` | Identity and roles | Add a workspace member | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner | `I1` | Not allowed by default |
| `ACT-055` | Identity and roles | Change a workspace role or approver authority | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner; Security Owner for sensitive roles | `I1; I2 for own privilege escalation` | Not allowed by default |
| `ACT-056` | Identity and roles | Create or expand platform-administrator authority | `R4` | `L4` | `REQUIRE_APPROVAL` | Existing Platform Administrator plus Security Owner | `I2` | Not allowed |
| `ACT-057` | Integrations | Register an adapter, tool, or MCP server | `R3` | `L4` | `REQUIRE_APPROVAL` | Technical Operator | `I1` | Not allowed by default |
| `ACT-058` | Integrations | Enable a registered capability for a workspace | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner plus Technical Operator for sensitive capabilities | `I1` | Not allowed by default |
| `ACT-059` | Integrations | Expand filesystem, network, data, model, or tool permission | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner and relevant Security/Technical Owner | `I2 for broad expansion` | Not allowed |
| `ACT-060` | Integrations | Revoke or reduce a permission | `R2` | `L3` | `ALLOW_WITH_GUARDS` | Workspace Owner or Technical Operator | `I1` | Allowed |
| `ACT-061` | Models | Create or update a model profile without secret disclosure | `R2` | `L3` | `ALLOW_WITH_GUARDS` | Technical Operator | `I1` | Review only by default |
| `ACT-062` | Models | Change routing or fallback policy | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner plus Technical Operator | `I1` | Not allowed by default |
| `ACT-063` | Costs | Change a workspace or task budget limit | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner or Budget Owner | `I1; I2 for increasing own task budget beyond threshold` | Not allowed by default |
| `ACT-064` | Policy | Change an autonomy or approval policy | `R4` | `L4` | `REQUIRE_APPROVAL` | Product Owner plus Security Owner | `I2` | Not allowed |
| `ACT-065` | Policy | Disable audit, approval, sandbox, or workspace-isolation control | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-066` | Deployment | Expose the local service remotely | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-067` | Deployment | Restart an unhealthy non-production local component | `R2` | `L3` | `ALLOW_WITH_GUARDS` | Technical Operator | `I1` | Review only by default |
| `ACT-068` | Deployment | Deploy to production | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-069` | Audit | Read authorized audit evidence | `R1` | `L2` | `ALLOW_WITH_GUARDS` | None | `I0` | Allowed |
| `ACT-070` | Audit | Export an evidence package | `R3` | `L4` | `REQUIRE_APPROVAL` | Workspace Owner, Auditor, or Data Owner | `I1` | Not allowed by default |
| `ACT-071` | Audit | Modify or delete audit evidence | `R4` | `L0` | `DENY` | None | `I0` | Denied |
| `ACT-072` | Emergency | Trigger emergency stop / revoke future execution | `R2` | `L3` | `ALLOW_WITH_GUARDS` | Workspace Owner, Technical Operator, Security Owner | `I1` | Allowed |

## 16. Detailed action rules

### `ACT-001` — Read authorized workspace metadata

- **Domain:** Workspace data
- **Default risk:** `R0`
- **Maximum autonomous level:** `L1`
- **Default policy decision:** `ALLOW`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Workspace ACL; read-only; audit sampling
- **Notes:** No cross-workspace discovery.
### `ACT-002` — Read authorized project files or repository content

- **Domain:** Workspace data
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Explicit mounted path; read-only grant; data-class check
- **Notes:** Secrets and prohibited files excluded.
### `ACT-003` — Search authorized tasks, runs, artifacts, audit, or memory

- **Domain:** Workspace data
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Workspace-scoped filtering before relevance/search
- **Notes:** No metadata leak from other workspaces.
### `ACT-004` — Create or update a draft task

- **Domain:** Task management
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Within workspace; no permission expansion; version material changes
- **Notes:** Task text cannot grant authority.
### `ACT-005` — Mark a task ready

- **Domain:** Task management
- **Default risk:** `R2`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Readiness validation; policy preflight; limits required
- **Notes:** Block when approvals or permissions unresolved.
### `ACT-006` — Start a bounded run

- **Domain:** Run control
- **Default risk:** `R2`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Persist run first; preflight; budgets; adapter/model/tool scopes
- **Notes:** No open-ended execution.
### `ACT-007` — Cancel a run

- **Domain:** Run control
- **Default risk:** `R2`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Operator or Workspace Owner when not requester-authorized
- **Independence requirement:** `I1`
- **Mobile policy:** Allowed
- **Mandatory guards:** Record cancellation; preserve completed side effects; invalidate pending approvals
- **Notes:** Cancellation does not imply rollback.
### `ACT-008` — Retry an idempotent low-risk step

- **Domain:** Run control
- **Default risk:** `R2`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Retry eligibility; idempotency key; retry/time/cost bounds
- **Notes:** Unsafe side-effect state blocks retry.
### `ACT-009` — Resume from a verified checkpoint

- **Domain:** Run control
- **Default risk:** `R2`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Revalidate scope, approval, budget, resource state
- **Notes:** Unknown side effect blocks resume.
### `ACT-010` — Retry or resume a consequential step

- **Domain:** Run control
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Action-domain approver
- **Independence requirement:** `I1`
- **Mobile policy:** Approval restricted
- **Mandatory guards:** Exact attempt; prior effects; renewed approval
- **Notes:** Approval required even if original action was approved.
### `ACT-011` — Create a draft text/Markdown/JSON/code-patch/test-log artifact

- **Domain:** Artifacts
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Permitted type/size; provenance; integrity hash
- **Notes:** Artifact remains draft/generated.
### `ACT-012` — Accept an artifact as reviewed output

- **Domain:** Artifacts
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner or delegated Reviewer
- **Independence requirement:** `I1`
- **Mobile policy:** Allowed with trusted device
- **Mandatory guards:** Artifact preview; provenance; lifecycle transition
- **Notes:** Acceptance does not make business data authoritative.
### `ACT-013` — Publish artifact outside the workspace

- **Domain:** Artifacts
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner plus Publication authority
- **Independence requirement:** `I2 for public publication`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact destination, content, audience, classification, expiry
- **Notes:** Public publication is consequential.
### `ACT-014` — Delete artifact content or metadata

- **Domain:** Artifacts
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner or Data Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Retention/legal check; exact artifact; backup/restore implications
- **Notes:** Soft delete preferred; audit retained.
### `ACT-015` — Archive or supersede an artifact

- **Domain:** Artifacts
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Workspace Owner or delegated Reviewer
- **Independence requirement:** `I1`
- **Mobile policy:** Allowed
- **Mandatory guards:** Link replacement; preserve history
- **Notes:** No content destruction.
### `ACT-016` — Write temporary working context

- **Domain:** Memory
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Workspace scope; retention bound; source label
- **Notes:** Not promoted to durable memory.
### `ACT-017` — Write durable generated memory under pre-approved type

- **Domain:** Memory
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Type allowlist; source; confidence; retention; no secrets
- **Notes:** Automatic write policy must be explicit.
### `ACT-018` — Promote memory to verified or authoritative status

- **Domain:** Memory
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Knowledge/Data Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Source evidence; conflict check; exact record/version
- **Notes:** Agent cannot self-promote generated claims.
### `ACT-019` — Correct or supersede memory

- **Domain:** Memory
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Knowledge/Data Owner or Workspace Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Allowed
- **Mandatory guards:** Preserve lineage; show old/new; reason
- **Notes:** May be policy-authorized for user-owned preferences.
### `ACT-020` — Delete durable memory

- **Domain:** Memory
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Data Owner or Workspace Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Retention/legal check; exact scope; index propagation
- **Notes:** Audit metadata may remain.
### `ACT-021` — Create or modify an approved working file inside a sandbox

- **Domain:** Local files
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Mounted path; diff capture; size/type limits; no executable install
- **Notes:** Task-scoped grant required.
### `ACT-022` — Delete an approved working file

- **Domain:** Local files
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner or Repository Maintainer
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact path; preview; recoverability; no wildcard deletion
- **Notes:** Bulk deletion escalates risk.
### `ACT-023` — Access a file outside approved workspace mounts

- **Domain:** Local files
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** No override through prompt
- **Notes:** Requires explicit future permission redesign.
### `ACT-024` — Run an approved read-only diagnostic command

- **Domain:** Command execution
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Command allowlist; sandbox; timeout; output limit
- **Notes:** Examples: version/status checks.
### `ACT-025` — Run approved tests or build inside sandbox

- **Domain:** Command execution
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Command profile; resource/time/network limits; workspace path
- **Notes:** No production deployment.
### `ACT-026` — Run an arbitrary shell command

- **Domain:** Command execution
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Only approved capability profiles may execute
- **Notes:** A prompt is not an allowlist.
### `ACT-027` — Install a package or executable dependency

- **Domain:** Dependencies
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Technical Operator plus Security Owner for executable plugins
- **Independence requirement:** `I1; I2 for untrusted source`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact source/version/hash/license/permissions; sandbox; rollback plan
- **Notes:** No self-modifying skills.
### `ACT-028` — Upgrade an approved dependency within pinned policy

- **Domain:** Dependencies
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Technical Operator
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Diff/lockfile; vulnerability/license result; tests; backup where needed
- **Notes:** May later use approved maintenance window policy.
### `ACT-029` — Call an approved model/provider endpoint

- **Domain:** Network
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Approved profile; data-class check; destination allowlist; budget
- **Notes:** Actual provider/model recorded.
### `ACT-030` — Call an approved read-only external API

- **Domain:** Network
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Destination and method allowlist; data minimization; rate/cost limits
- **Notes:** Response is untrusted input.
### `ACT-031` — Send data to an unapproved destination

- **Domain:** Network
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Network policy denies
- **Notes:** Cannot be authorized by prompt.
### `ACT-032` — Use a secret reference through an approved capability

- **Domain:** Secrets
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Secret Owner or Security Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Secret never exposed; exact target/capability; short-lived access; receipt
- **Notes:** Standing grants highly restricted.
### `ACT-033` — Display, export, copy, or store a raw secret

- **Domain:** Secrets
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Redaction; reference-only handling
- **Notes:** Break-glass process outside ordinary agent workflow.
### `ACT-034` — Read Git status, log, diff, or branch metadata

- **Domain:** Git
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Authorized repository; read-only; bounded output
- **Notes:** No remote mutation.
### `ACT-035` — Create or modify an uncommitted patch in approved worktree

- **Domain:** Git
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Approved path; diff recorded; no unrelated files; tests required
- **Notes:** Working-tree changes remain reviewable.
### `ACT-036` — Create a Git commit

- **Domain:** Git
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Repository Maintainer or Workspace Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact diff, files, message, tests, branch; one-time approval
- **Notes:** Agent cannot approve its own commit.
### `ACT-037` — Push a branch

- **Domain:** Git
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Repository Maintainer
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact repo/remote/branch/commit; no force; policy checks
- **Notes:** Force push separately prohibited.
### `ACT-038` — Create a pull request

- **Domain:** Git
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Repository Maintainer or Product Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact base/head/title/body; pushed commits; CI state
- **Notes:** External publication side effect.
### `ACT-039` — Merge a pull request

- **Domain:** Git
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Human/manual merge outside autonomous MVP
- **Notes:** May be reconsidered post-MVP with separate controls.
### `ACT-040` — Force push, delete protected branch, rewrite shared history

- **Domain:** Git
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** No ordinary approval path
- **Notes:** Break-glass human operations only.
### `ACT-041` — Draft an external e-mail or message

- **Domain:** Messaging
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Draft only; destination and content visible; no send
- **Notes:** Stored as draft artifact or connected-system draft.
### `ACT-042` — Send an external e-mail or message

- **Domain:** Messaging
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner or Communication Owner
- **Independence requirement:** `I1; I2 for broad/public audience`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact recipients, subject, body, attachments, classification, expiry
- **Notes:** Changed content/recipient invalidates approval.
### `ACT-043` — Create or modify a calendar event with invitees

- **Domain:** Calendar
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Calendar Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact time, timezone, attendees, recurrence, description
- **Notes:** External notification side effect.
### `ACT-044` — Read authorized calendar availability

- **Domain:** Calendar
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Time and calendar scope; privacy minimization
- **Notes:** No attendee data beyond need.
### `ACT-045` — Read approved ERP/CRM/accounting data

- **Domain:** Business systems
- **Default risk:** `R3`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Business Data Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Read-only connector; fields, period, purpose, freshness, source lineage
- **Notes:** Post-MVP candidate, not MVP baseline.
### `ACT-046` — Write or modify ERP/CRM/accounting records

- **Domain:** Business systems
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** No MVP write connector
- **Notes:** Future requires dedicated scope/security review.
### `ACT-047` — Create, modify, approve, or post a financial transaction

- **Domain:** Financial
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Source system remains authoritative
- **Notes:** Production financial posting excluded.
### `ACT-048` — Access a production system

- **Domain:** Production
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** No production credentials or route in MVP
- **Notes:** Future high-risk workflow requires separate approval system.
### `ACT-049` — Read approved local Agent OS application data through governed API

- **Domain:** Database
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Workspace authorization; API only; no direct credential exposure
- **Notes:** Audit according to data class.
### `ACT-050` — Execute destructive database operation

- **Domain:** Database
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Backup and human break-glass outside ordinary agent execution
- **Notes:** Includes DROP, mass delete, unsafe migration.
### `ACT-051` — Apply an approved application migration

- **Domain:** Database
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Technical Operator plus Data/Operations Owner
- **Independence requirement:** `I1; I2 when destructive`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact migration/version; backup; tests; rollback/forward plan; maintenance state
- **Notes:** Destructive migrations require stricter independence.
### `ACT-052` — Create a backup

- **Domain:** Backups
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Technical Operator when schedule/manual
- **Independence requirement:** `I1`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Approved destination; encryption; manifest; integrity check
- **Notes:** Scheduled backups may use standing policy.
### `ACT-053` — Restore a backup

- **Domain:** Backups
- **Default risk:** `R4`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Technical Operator plus Operations/Data Owner
- **Independence requirement:** `I2`
- **Mobile policy:** Not allowed
- **Mandatory guards:** Exact backup, target, maintenance state, integrity, impact, rollback plan
- **Notes:** Restore can overwrite current state.
### `ACT-054` — Add a workspace member

- **Domain:** Identity and roles
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact identity, workspace, role, expiry if temporary
- **Notes:** No cross-workspace implicit membership.
### `ACT-055` — Change a workspace role or approver authority

- **Domain:** Identity and roles
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner; Security Owner for sensitive roles
- **Independence requirement:** `I1; I2 for own privilege escalation`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Before/after permissions; last-owner protection; conflict checks
- **Notes:** Self-elevation requires independent approver.
### `ACT-056` — Create or expand platform-administrator authority

- **Domain:** Identity and roles
- **Default risk:** `R4`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Existing Platform Administrator plus Security Owner
- **Independence requirement:** `I2`
- **Mobile policy:** Not allowed
- **Mandatory guards:** Exact identity; scope; expiry; MFA/session requirements
- **Notes:** May be unavailable in single-user pilot except bootstrap.
### `ACT-057` — Register an adapter, tool, or MCP server

- **Domain:** Integrations
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Technical Operator
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Source, endpoint, version, capabilities, data/network risk; validation separate
- **Notes:** Registration does not grant use.
### `ACT-058` — Enable a registered capability for a workspace

- **Domain:** Integrations
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner plus Technical Operator for sensitive capabilities
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact capability, scope, paths, destinations, expiry, budget
- **Notes:** Least privilege.
### `ACT-059` — Expand filesystem, network, data, model, or tool permission

- **Domain:** Integrations
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner and relevant Security/Technical Owner
- **Independence requirement:** `I2 for broad expansion`
- **Mobile policy:** Not allowed
- **Mandatory guards:** Before/after scope; reason; expiry; active-run impact
- **Notes:** Agent cannot self-expand.
### `ACT-060` — Revoke or reduce a permission

- **Domain:** Integrations
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Workspace Owner or Technical Operator
- **Independence requirement:** `I1`
- **Mobile policy:** Allowed
- **Mandatory guards:** Show affected runs; fail closed for future use; preserve evidence
- **Notes:** Reduction is generally safer but can disrupt work.
### `ACT-061` — Create or update a model profile without secret disclosure

- **Domain:** Models
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Technical Operator
- **Independence requirement:** `I1`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Provider/model/capability/budget/data-class; validation state
- **Notes:** No raw secret.
### `ACT-062` — Change routing or fallback policy

- **Domain:** Models
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner plus Technical Operator
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Before/after routes; privacy/cost/capability impact; effective time
- **Notes:** No silent fallback.
### `ACT-063` — Change a workspace or task budget limit

- **Domain:** Costs
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner or Budget Owner
- **Independence requirement:** `I1; I2 for increasing own task budget beyond threshold`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Old/new limit; currency; period; active-run impact
- **Notes:** Decreasing limit may use guarded path.
### `ACT-064` — Change an autonomy or approval policy

- **Domain:** Policy
- **Default risk:** `R4`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Product Owner plus Security Owner
- **Independence requirement:** `I2`
- **Mobile policy:** Not allowed
- **Mandatory guards:** Versioned policy diff; impact analysis; tests; effective time; rollback
- **Notes:** Agents cannot change policy.
### `ACT-065` — Disable audit, approval, sandbox, or workspace-isolation control

- **Domain:** Policy
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** No ordinary approval path
- **Notes:** Break-glass human incident process only.
### `ACT-066` — Expose the local service remotely

- **Domain:** Deployment
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Remote access outside MVP
- **Notes:** Requires DEP/SEC/THR/IRP update.
### `ACT-067` — Restart an unhealthy non-production local component

- **Domain:** Deployment
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Technical Operator
- **Independence requirement:** `I1`
- **Mobile policy:** Review only by default
- **Mandatory guards:** Component allowlist; active-run impact; maintenance/audit
- **Notes:** No host-wide reboot.
### `ACT-068` — Deploy to production

- **Domain:** Deployment
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Production deployment outside MVP
- **Notes:** Future release workflow required.
### `ACT-069` — Read authorized audit evidence

- **Domain:** Audit
- **Default risk:** `R1`
- **Maximum autonomous level:** `L2`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Allowed
- **Mandatory guards:** Auditor ACL; workspace scope; redaction
- **Notes:** Read-only.
### `ACT-070` — Export an evidence package

- **Domain:** Audit
- **Default risk:** `R3`
- **Maximum autonomous level:** `L4`
- **Default policy decision:** `REQUIRE_APPROVAL`
- **Eligible approver:** Workspace Owner, Auditor, or Data Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Not allowed by default
- **Mandatory guards:** Exact records/period; redaction; destination; manifest
- **Notes:** Disclosure risk.
### `ACT-071` — Modify or delete audit evidence

- **Domain:** Audit
- **Default risk:** `R4`
- **Maximum autonomous level:** `L0`
- **Default policy decision:** `DENY`
- **Eligible approver:** None
- **Independence requirement:** `I0`
- **Mobile policy:** Denied
- **Mandatory guards:** Retention process only; no ordinary mutation
- **Notes:** Correction uses append-only explanatory event.
### `ACT-072` — Trigger emergency stop / revoke future execution

- **Domain:** Emergency
- **Default risk:** `R2`
- **Maximum autonomous level:** `L3`
- **Default policy decision:** `ALLOW_WITH_GUARDS`
- **Eligible approver:** Workspace Owner, Technical Operator, Security Owner
- **Independence requirement:** `I1`
- **Mobile policy:** Allowed
- **Mandatory guards:** Immediate future block; record actor/reason; preserve evidence
- **Notes:** May interrupt work; no rollback guarantee.


## 17. Source-control policy summary

### Automatically permitted under guards

- inspect status, log, diff, and branch metadata;
- create or update a reviewable uncommitted patch inside an approved worktree;
- run approved tests/builds in the sandbox.

### Exact human approval required

- create a commit;
- push a branch;
- create a pull request;
- delete an unprotected working branch where future policy permits;
- install or upgrade executable dependencies.

### Prohibited in MVP

- autonomous merge;
- force push;
- rewrite shared history;
- delete protected branches;
- bypass required CI or review;
- use unknown credentials/remotes;
- operate outside approved repository/worktree scope.

## 18. External communication policy summary

Agents may draft communication.

They may not send, publish, invite, or notify external parties without exact approval covering:

- recipients or audience;
- content;
- attachments;
- destination/channel;
- sender identity;
- time;
- data classification;
- public visibility;
- expiry.

Changing any recipient or content invalidates approval.

## 19. Secret-handling policy

Agents may receive capability-level access to a secret through a secure mechanism only when:

- the secret owner/security authority permits it;
- the value is not exposed to ordinary prompts, logs, memory, artifacts, or UI;
- the target and purpose are exact;
- access is short-lived where practical;
- network/tool scope is restricted;
- use is recorded without recording the value;
- approval is renewed when material context changes.

Agents may never:

- display raw secrets;
- copy secrets into source files;
- store secrets as memory;
- export secrets in artifacts;
- send secrets to unapproved providers or tools;
- infer authorization because a secret exists in the environment.

## 20. Agent delegation rules

The MVP does not support open-ended multi-agent swarms.

Where one adapter/runtime internally delegates:

- the parent grant is the maximum authority;
- the child identity receives equal or narrower scope;
- child activity must correlate to the parent run;
- no child may approve an action;
- no child may expand time, budget, data, file, tool, model, or network scope;
- recursion/delegation depth must be bounded;
- all consequential actions still require the defined human approval;
- unsupported delegation must be reported as unavailable, not hidden.

## 21. Retry and resume policy

A retry or resume may proceed without new approval only when:

- the original action was not approval-required, or the approval explicitly covers the attempt model;
- the exact action and target are unchanged;
- no material side effect occurred, or idempotency guarantees safe repetition;
- the approval remains valid;
- the retry count, budget, and time limits remain inside policy;
- the adapter/tool state is sufficiently known.

A new approval is required when:

- the previous side effect is unknown;
- the action is consequential;
- parameters or target changed;
- the original approval expired or was consumed;
- the recovery method introduces new capability;
- the cost/time bound materially increases.

## 22. Cancellation and emergency stop

### Cancellation

Cancellation:

- prevents future dispatch where enforceable;
- requests adapter/tool stop;
- invalidates or cancels related pending approvals;
- preserves completed effects and evidence;
- may end in `cancelled`, `failed`, or `unknown`;
- does not promise rollback.

### Emergency stop

An authorized human must be able to:

- stop future run dispatch;
- disable selected adapters/tools;
- revoke selected permissions;
- block approval consumption;
- mark active runs for pause/cancel/review;
- preserve current evidence;
- record actor, reason, time, and scope.

Emergency stop must not delete audit evidence.

## 23. Mobile policy

Default MVP mobile behavior:

### Permitted

- view Mission Control;
- inspect tasks, runs, artifacts, costs, and audit summaries;
- reject or request revision where the reviewer has sufficient context;
- cancel a run where policy permits;
- perform low-risk read-only actions.

### Restricted by default

- approve `R3` actions;
- use secrets;
- change roles or permissions;
- commit, push, create PR;
- send external communications;
- restore backups;
- install packages;
- expose services remotely;
- approve public, production, financial, or destructive actions.

Server-side authorization must enforce the restriction; responsive UI alone is not a control.

## 24. Approval UX requirements

The approval interface must provide:

- plain-language summary;
- exact technical details;
- clear target and scope;
- risk and policy reason;
- preview or diff;
- what will happen;
- what cannot be undone automatically;
- cost/time impact;
- expiry;
- requester and executing agent;
- prior rejection/revision context;
- approve, reject, request revision, and cancel controls;
- keyboard and screen-reader usability;
- warning when evidence is incomplete.

No approval should rely on color alone or a generic “Allow” button without action detail.

## 25. Approval fatigue controls

To reduce unsafe approval behavior:

- batch approval of unrelated consequential actions is prohibited by default;
- recurring low-risk actions should use narrow standing grants rather than repeated vague approvals;
- requests should be deduplicated;
- risk and urgency should be visible;
- stale requests should expire;
- repeated denied requests should be surfaced;
- the product should measure approval volume, latency, rejection, expiry, and comprehension;
- high-risk actions must not be downgraded merely to reduce volume.

## 26. Conflict-of-interest rules

At minimum:

- an agent cannot approve;
- an identity cannot independently approve its own privilege escalation;
- a requester cannot satisfy `I2`;
- a person who configured an untrusted executable plugin should not be the sole security approver for its broad permissions;
- financial, production, public, destructive restore, and security-policy actions require independent authority or remain denied;
- audit reviewers do not gain operational mutation authority.

## 27. Policy evaluation order

A proposed action should be evaluated in this order:

1. identity authentication;
2. organization/workspace membership;
3. global exclusion/prohibition;
4. resource ownership and data classification;
5. capability registration and health;
6. explicit grant and expiry;
7. sandbox/path/network boundary;
8. model/provider restrictions;
9. side-effect and risk classification;
10. budget/time/step limits;
11. approval requirement;
12. approval validity and independence;
13. emergency stop/revocation;
14. dispatch;
15. receipt and audit.

Any hard denial stops evaluation before execution.

## 28. Evidence requirements

For all `R2`, `R3`, and attempted `R4` actions, retain where applicable:

- requester and executing identity;
- workspace/task/run/step;
- action class and parameters;
- target;
- risk classification;
- policy version and result;
- approval request and decision;
- approver authority;
- independence result;
- action hash/version;
- timestamps;
- adapter/model/tool;
- cost/time;
- execution result;
- known side effects;
- retry/resume lineage;
- evidence gaps.

## 29. Security failure behavior

When policy, identity, approval, scope, or evidence is uncertain:

- do not execute the protected action;
- preserve the proposed action;
- display a safe, actionable reason;
- avoid leaking protected target details;
- record the failure where possible;
- route to review when appropriate;
- do not silently downgrade the risk;
- do not retry indefinitely.

## 30. Required conformance tests

The test strategy must include:

- agent self-approval attempt;
- workload identity posing as human;
- prompt-based permission expansion;
- changed parameter after approval;
- changed target after approval;
- expired approval;
- cancelled approval;
- replay/double consumption;
- concurrent approval consumption;
- unknown side effect followed by retry;
- secret disclosure attempt;
- cross-workspace action;
- unapproved network destination;
- arbitrary shell request;
- commit/push/merge policy;
- external message content/recipient change;
- role self-escalation;
- audit-disable request;
- emergency stop during active run;
- mobile approval restriction;
- standing-grant expiry and revocation.

All mandatory denial tests must pass before MVP acceptance.

## 31. Metrics

The pilot should track:

- actions by risk class;
- allow, deny, and approval-required decisions;
- approval volume;
- approval decision time;
- rejection, revision, expiry, cancellation;
- invalidation causes;
- attempted replay;
- policy evaluation failures;
- emergency-stop use;
- permission revocation latency;
- user comprehension for approval scenarios;
- actions blocked because independence was unavailable.

Metrics must not expose secret values or unrelated workspace data.

## 32. Relationship to IAM and policy enforcement

`AUT-001` defines the intended product policy.

`IAM-001` will define:

- identities;
- roles;
- permissions;
- delegation;
- session assurance;
- role assignment;
- workspace membership.

`POL-001` will define:

- policy representation;
- evaluation engine;
- precedence;
- conflict handling;
- decision evidence;
- versioning;
- simulation and testing.

`APR-001` will define the approval data and state contract.

`SAN-001` will define the execution boundary that enforces action limits.

## 33. Assumptions

This draft assumes:

- the MVP remains local and non-production;
- one primary operator or small trusted team is acceptable;
- some `I2` actions may remain unavailable in a single-user pilot;
- Hermes and Codex can operate under a shared policy envelope;
- the platform can identify actions before side effects occur;
- tools can expose normalized targets and parameters;
- policy decisions can be persisted before dispatch;
- approval consumption can be atomic;
- named approval authorities will be assigned before implementation acceptance.

## 34. Constraints

- this document does not grant permissions;
- the action matrix is a proposed baseline;
- production, financial, public, and broad destructive actions remain excluded;
- no agent may approve;
- no prompt may expand authority;
- security controls override performance/convenience;
- no hidden mock policy decision is acceptable;
- unsupported action classification must remain unknown/denied;
- GitHub versioning is deferred until the full documentation drafting phase is complete.

## 35. Risks

| Risk | Consequence | Response |
|---|---|---|
| Too many approvals | Approval fatigue | Narrow standing grants for low-risk classes |
| Too few approvals | Unsafe side effects | Default consequential classes to exact approval |
| Same person holds many roles | Weak independence | Record role used; keep `I2` actions unavailable when necessary |
| Adapter hides action details | Informed approval impossible | Block until exact normalized action exists |
| Tool side effect occurs before policy | Control bypass | Enforce policy at gateway before dispatch |
| Approval replay | Duplicate consequential effect | Atomic one-time consumption |
| Policy drift | Old approval authorizes new behavior | Bind policy/action version and invalidate changes |
| Mobile convenience pressure | High-risk approval on weak context | Restrict mobile by default |
| Emergency stop mistaken for rollback | Hidden completed effects | Preserve evidence and state limitations |
| Broad standing grants | Persistent excessive authority | Limit scope, expiry, and eligible risk classes |
| Unknown side effect after timeout | Unsafe retry | Block retry or require new approval |
| Single-user pilot overgeneralization | Commercial controls insufficient | Revisit independence before trusted-team/production expansion |

## 35A. ADR-003 canonical action vocabulary

`AUT-001` is the authoritative source for action risk, autonomy, and approval behavior. The product-facing action tags from `ADR-003` map to the existing controlled matrix as follows:

| Product action tag | Typical risk range | Typical autonomy | Default control |
|---|---|---|---|
| `read` | `R0–R1` | `L1–L2` | Allow with scope and data guards |
| `generate` | `R1` | `L2` | Allow as draft/non-authoritative output |
| `controlled_write` | `R2–R3` | `L3–L4` | Workspace policy decides; approval for consequential writes |
| `external_effect` | `R3` | `L4` | Exact approval required |
| `destructive` | `R3–R4` | `L4` or `L0` | Approval only where explicitly permitted; otherwise deny |
| `critical` | `R4` | `L4` or `L0` | Recent reauthentication and elevated approval, or deny |

`critical` does not mean that an action is always approvable. Production access, financial posting, arbitrary shell, audit disablement, and other excluded actions remain denied under the existing matrix. `ADR-003`, API, approval, and event documents must reference this mapping rather than define a competing risk vocabulary.

## 36. Open decisions

1. Which actions are executable after approval versus proposal-only in the MVP?
2. Can Git commit be executed after same-human explicit approval in the first pilot?
3. Can push or PR creation be executed, or should they remain proposal-only?
4. Which exact low-risk command profiles qualify for `L3`?
5. Which memory types permit automatic durable writes?
6. Which artifact lifecycle changes require approval?
7. Which mobile actions, if any, can approve `R2` requests?
8. Which actions require `I2` in the trusted-team pilot?
9. What approval expiry defaults apply by action class?
10. What maximum standing-grant duration applies?
11. What revocation enforcement latency is acceptable?
12. Which cost increases require independent approval?
13. Which backup creation operations may run on a schedule?
14. Which restore operations require dual control?
15. Which connector reads are allowed after MVP?
16. What is the emergency-stop scope and operator interface?
17. Which policy engine and representation will be selected?
18. How are action hashes normalized across adapters/tools?
19. What evidence is mandatory before a request can be approved?
20. Which decisions would invalidate the current MVP scope?

## 37. Acceptance criteria

AUT-001 may advance to version `1.0.0` when:

1. Product Owner approves the autonomy levels and action classes;
2. Security approves the risk model, default denials, independence, secret, network, and permission rules;
3. Architecture confirms that proposed actions can be normalized and blocked before side effect;
4. Operations accepts backup, restore, emergency-stop, and local-control rules;
5. every action in the MVP has a default policy decision;
6. every `REQUIRE_APPROVAL` action identifies an eligible authority and independence level;
7. every `DENY` action is consistent with `SCP-001`;
8. mobile and standing-grant policies are explicit;
9. retry, resume, cancellation, expiry, invalidation, and replay behavior are covered;
10. testable denial/conformance scenarios are defined;
11. open decisions have owners in downstream documents;
12. metadata, terminology, links, Markdown, and validation checks pass.

## 38. Downstream traceability

| AUT area | Downstream documents |
|---|---|
| Identity and approver authority | `IAM-001` |
| Policy decisions and precedence | `POL-001` |
| Human-in-the-loop UX and procedures | `HUM-001`, `UXA-001`, `A11Y-001` |
| Approval states and exact-action binding | `APR-001` |
| Run pause/resume/cancel | `RUN-001`, `ORC-001` |
| Tool and network enforcement | `SEC-001`, `SAN-001`, `INT-001` |
| Secret access | `SEC-002`, `SEC-001` |
| Git and external actions | Adapter/tool specifications |
| Audit evidence | `AUD-001`, `OBS-001` |
| Tests | `TST-001`, `QAG-001`, `RTM-001` |

## 39. Revision and approval history

### Approval state

- Current status: `draft`
- Current version: `0.1.0`
- Approved by: no one
- Approval date: not applicable
- Required next action: Product, Security, Architecture, and Operations review

### Revision history

| Version | Date | Status | Summary | Authority |
|---|---|---|---|---|
| 0.1.0 | 2026-07-19 | Draft | Initial autonomy levels, risk classes, independence rules, approval lifecycle, standing-grant policy, emergency controls, and 72-action default matrix | Draft authoring; not approved |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `VSN-001` — Product Vision and Project Charter
- `SCP-001` — Scope and System Boundaries
- `PER-001` — Personas and Jobs to Be Done
- `UCD-001` — User Journeys and Use Cases
- `PRD-001` — Product Requirements Document
- `SRS-001` — Functional Requirements Specification
- `NFR-001` — Non-Functional Requirements
