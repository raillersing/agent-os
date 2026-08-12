# Agent OS v2 — Goldie Edition: Product Requirements Document

> **Document:** `02-PRD.md`  
> **Version:** 2.0.0  
> **Status:** Draft  
> **Date:** 2026-08-11  
> **Classification:** Internal  
> **Source of Truth:** True (for v2 Goldie Edition requirements)  

---

## Table of Contents

1. [Document Purpose](#1-document-purpose)
2. [Product Summary](#2-product-summary)
3. [Tech Stack](#3-tech-stack)
4. [Release Model](#4-release-model)
5. [Feature Requirements](#5-feature-requirements)
   - 5.1 Mission Control
   - 5.2 Named Agents
   - 5.3 Chat
   - 5.4 Mission Board (Kanban)
   - 5.5 Studio
   - 5.6 Notebook (KB)
   - 5.7 Skills / Workflows
   - 5.8 Two-Lane Verifier
   - 5.9 BYOK Model Gateway
   - 5.10 Workspace & Memory
   - 5.11 Approvals & Governance
   - 5.12 Audit & Cost
   - 5.13 SEO Module
   - 5.14 Visual Workflow Builder
   - 5.15 Dynamic Agent Roles
   - 5.16 Voice / Talk Mode
   - 5.17 Import / Export
   - 5.18 Disaster Recovery
6. [User Stories](#6-user-stories)
7. [Acceptance Criteria](#7-acceptance-criteria)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Dependencies & Constraints](#9-dependencies--constraints)
10. [Open Decisions](#10-open-decisions)

---

## 1. Document Purpose

This document translates the Agent OS v2 — Goldie Edition Product Vision into detailed, actionable product requirements. It serves as the single source of truth for feature definition, user story derivation, acceptance criteria, and non-functional requirements for the v2 development team.

Every requirement includes:
- Stable identifier (`PRD-v2-<DOMAIN>-<NUMBER>`)
- Priority (`Must` / `Should` / `Could` / `Won't-v2`)
- User story mapping
- Measurable acceptance criteria
- Security / governance implications
- Traceability to vision and prior controlled documents

---

## 2. Product Summary

Agent OS v2 — Goldie Edition is a local-first, self-hosted, white-label Agent Operating System that coordinates multiple AI agents through a unified dark-theme Mission Control dashboard. It introduces named agent personas, a live DAG status view, Kanban mission board, media Studio, self-hosted Notebook knowledge base, Two-Lane artifact verification, and an intelligent BYOK Model Gateway.

The platform enforces durable execution, human-in-the-loop approvals, workspace isolation, artifact provenance, and complete cost attribution. It is built on Next.js 15 + React 19 + Tailwind CSS v4 (frontend) and FastAPI + SQLAlchemy 2.0 + Alembic (backend), with SQLite/PostgreSQL + pgvector for persistence and Redis for cache/queue.

---

## 3. Tech Stack

### 3.1 Frontend
| Technology | Version | Purpose |
|---|---|---|
| Next.js | 15 | App Router, SSR/SSG, API routes |
| React | 19 | UI framework, concurrent features |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Utility-first styling with `@theme` tokens |
| shadcn/ui | latest | Base component library |
| Framer Motion | latest | Animations (pulse, transitions, stream reveal) |
| React Query | 5.x | Server state management |
| Zustand | latest | Client state management |
| React Hook Form | latest | Form handling |
| Zod | latest | Schema validation |

### 3.2 Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.12 | Runtime |
| FastAPI | 0.115+ | API framework, auto-docs, dependency injection |
| SQLAlchemy | 2.0 | ORM, async queries |
| Alembic | latest | Database migrations |
| asyncpg | latest | Async PostgreSQL driver |
| Pydantic | 2.x | Data validation, settings |
| Redis | 7.x | Cache, sessions, job queue, SSE pub/sub |
| Celery | latest | Background task processing |
| Uvicorn | latest | ASGI server |

### 3.3 Database & Storage
| Technology | Version | Purpose |
|---|---|---|
| SQLite | 3.45+ | Default local mode |
| PostgreSQL | 16+ | Team mode with pgvector |
| pgvector | 0.7+ | Vector embeddings for semantic search |
| Redis | 7.x | Cache, queue, session store |

### 3.4 AI Providers & Adapters
| Provider | Adapter | Capabilities |
|---|---|---|
| Anthropic Claude | `adp-claude` | Chat, code, reasoning, artifacts |
| Moonshot Kimi | `adp-kimi` | Long-context, chat, reasoning |
| XAI Grok | `adp-grok` | Real-time, chat, reasoning |
| Ollama | `adp-ollama` | Local models, chat, embeddings |
| OpenRouter | `adp-openrouter` | Fallback, multi-provider routing |
| Hermes Gateway | `adp-hermes` | Internal execution engine (:8642) |

### 3.5 Infrastructure
| Technology | Purpose |
|---|---|
| Docker Compose | Local deployment, service orchestration |
| Nginx (optional) | Reverse proxy, SSL termination |
| Prometheus + Grafana | Metrics and observability |

---

## 4. Release Model

### Release `v2.0-MVP` — Goldie Foundation
- Dark-theme Mission Control shell
- Named agents (Crystal, Alex, Elvis, Joe) with circular avatars
- Claude + Hermes adapters
- Basic chat with SSE streaming
- Workspace + project scaffolding
- Task creation + durable runs
- Local SQLite deployment

### Release `v2.1-Studio` — Media & Knowledge
- Studio: Image generation (6 formats)
- Notebook: Markdown KB with wiki-links
- Mission Board: Kanban board (read-only)
- PostgreSQL + pgvector option
- Agent health heartbeat

### Release `v2.2-Orchestrator` — Workflows & Governance
- Mission Board: Full drag-drop
- Skills / Workflows: 3 templated DAGs
- Two-Lane Verifier v1
- BYOK Model Gateway v1
- Approval inbox with risk scoring
- Cost attribution dashboard

### Release `v2.3-Polish` — Quality & Scale
- Studio: Video + Speech (12 total formats)
- Notebook: Semantic search
- Voice / Talk Mode: push-to-talk, STT, TTS, voice profiles
- Import / Export: Obsidian, Notion, ChatGPT, Claude, Evernote, OneNote, Markdown
- Disaster Recovery: auto-backup, cloud targets, Git sync, encrypted export, one-click restore
- Full agent roster (OpenClaw, Kimi, Grok)
- Accessibility audit (WCAG 2.2 AA)
- Backup/restore procedures
- Performance optimization

### Release `v2.4-SEO` — Search & Scale
- SEO Module: SERP analysis, rank tracking, competitor watch, content briefs
- CMS connectors: WordPress, Shopify, Webflow
- Visual Workflow Builder: drag-drop DAG, conditional branches, loops, approval gates
- Dynamic Agent Roles: custom roles, skill templates, role switching
- Traffic analytics: GSC + GA4 integration
- White-label SEO reports

### Release `v2.5-Workflows` — Visual Orchestration
- Visual Workflow Builder: drag & drop DAG canvas
- Conditional branches (if/else), loops, approval gates
- Cron and webhook triggers
- Simulation / dry-run mode
- Workflow marketplace (import/export)

### Release `v2.6-Agentic` — Dynamic Roles & Swarm
- Dynamic Agent Roles: create, assign, switch, clone
- Agent Role Manager UI with skill templates
- Swarm mode: multi-agent collaboration
- Delegation protocol with structured handoff
- Reflection loops and memory profiles

---

## 5. Feature Requirements

### 5.1 Mission Control (PRD-v2-MC)

The home screen and primary operational view. Dark theme, live DAG, KPI cards, status glyphs.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-MC-001` | Display live DAG node-graph of active agents, tasks, and runs | Must | As an operator, I see a real-time graph of what is running so I can understand system health at a glance | DAG renders within 2s of page load; nodes pulse when status=running; edges show data flow direction |
| `PRD-v2-MC-002` | Show KPI/status cards: active agents, pending tasks, approvals awaiting review, daily cost, system health | Must | As a workspace owner, I see summary KPIs so I know if attention is needed | Cards update via SSE every 5s; values reconcile with detail records; zero/unavailable/stale states are visually distinct |
| `PRD-v2-MC-003` | Agent status dots with color semantics: green=online, yellow=ready/idle, red=offline/error, blue=running, gray=unknown | Must | As an operator, I see agent status via color-coded dots so I know which agents are operational | Each status has icon + text + color (not color-only); tooltip shows last heartbeat timestamp and latency |
| `PRD-v2-MC-004` | Display agent heartbeat and latency per adapter | Must | As a technical operator, I see real-time latency so I can diagnose slow agents | Heartbeat updates every 10s; latency shown in ms; stale (>60s) heartbeats trigger unknown state |
| `PRD-v2-MC-005` | Command Palette (⌘K) for global search and quick actions | Should | As a power user, I use ⌘K to jump to any workspace, task, or agent so I don't navigate through menus | ⌘K opens with Cmd/Ctrl+K; searches across workspaces, tasks, agents, artifacts; shows 10 results with keyboard navigation |
| `PRD-v2-MC-006` | "ALL SYSTEMS" button showing aggregate system status | Should | As an operator, I click ALL SYSTEMS to see a rollup of all subsystem health | Button color reflects worst subsystem (red if any critical); dropdown lists all subsystems with individual status |
| `PRD-v2-MC-007` | Time/location display in header | Could | As a distributed team member, I see current time and timezone so I coordinate with others | Shows local time + configurable secondary timezone; updates every minute |
| `PRD-v2-MC-008` | Distinguish zero, unavailable, stale, estimated, partial, failed, and unknown states in every metric | Must | As an operator, I never mistake missing data for zero or success | Empty states have distinct icons; stale data shows "last updated X min ago"; estimated values are labeled with confidence |

---

### 5.2 Named Agents (PRD-v2-AGT)

Personified agents with distinct capabilities, colors, and specializations.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-AGT-001` | Crystal (orchestrator) agent with violet `#8B5CF6` circular avatar | Must | As an operator, I interact with Crystal to coordinate tasks across other agents | Crystal appears in sidebar; avatar is violet circle with white "C"; routes tasks to appropriate agents |
| `PRD-v2-AGT-002` | Alex (writer) agent with blue `#3B82F6` circular avatar | Must | As a content creator, I delegate writing tasks to Alex so I get consistent drafts | Alex avatar is blue circle with white "A"; specializes in long-form text, blog posts, docs |
| `PRD-v2-AGT-003` | Elvis (media) agent with pink `#EC4899` circular avatar | Must | As a media producer, I ask Elvis to generate images and videos so I don't switch tools | Elvis avatar is pink circle with white "E"; triggers Studio workflows; shows media generation status |
| `PRD-v2-AGT-004` | Joe (reviewer) agent with green `#22C55E` circular avatar | Must | As a QA lead, I rely on Joe to verify artifacts before they ship | Joe avatar is green circle with white "J"; runs Two-Lane Verifier; shows pass/fail per artifact |
| `PRD-v2-AGT-005` | Claude adapter with orange `#F97316` circular avatar | Must | As a user, I chat with Claude through Agent OS so my conversation history is durable | Claude avatar is orange circle; supports chat, code, reasoning; status shows Anthropic API health |
| `PRD-v2-AGT-006` | Hermes adapter with blue `#3B82F6` circular avatar | Must | As a developer, I use Hermes for terminal, file, and code execution | Hermes avatar is blue circle with "H"; gateway on :8642; status shows reachability |
| `PRD-v2-AGT-007` | OpenClaw adapter with pink `#EC4899` circular avatar | Should | As a developer, I use OpenClaw for GitHub-integrated coding workflows | OpenClaw avatar is pink circle; supports PR review, code generation; status shows GitHub API health |
| `PRD-v2-AGT-008` | Kimi adapter with red `#EF4444` circular avatar | Should | As a researcher, I use Kimi for long-context document analysis | Kimi avatar is red circle; supports 1M+ token context; status shows Moonshot API health |
| `PRD-v2-AGT-009` | Grok adapter with amber `#F59E0B` circular avatar | Could | As a news analyst, I use Grok for real-time information | Grok avatar is amber circle; status shows XAI API health |
| `PRD-v2-AGT-010` | Each agent shows capability declaration and limitations transparently | Must | As an operator, I see what each agent can and cannot do before delegating | Capability card lists supported/unsupported/unknown capabilities; limitations are visible, not hidden |
| `PRD-v2-AGT-011` | Agent health check with distinct states: registered, reachable, validated, degraded, failed, stale, unknown | Must | As a technical operator, I know the exact state of every adapter | Health states are distinct in UI; degraded shows specific limitation; stale shows last check timestamp |
| `PRD-v2-AGT-012` | Workspace-level agent enable/disable | Must | As a workspace owner, I enable only the agents my team needs | Enabled agents appear in workspace sidebar; disabled agents are hidden but historical runs remain visible |

---

### 5.3 Chat (PRD-v2-CHT)

Multi-provider chat with sessions, SSE streaming, thinking indicators, code blocks, and artifacts.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-CHT-001` | Sessions sidebar with pinned sessions, search, and recent conversations | Must | As a user, I find previous chat sessions in a sidebar so I resume context | Sidebar shows session list with agent avatar, title preview, last message time; pinned sessions stick to top; search filters by title and content |
| `PRD-v2-CHT-002` | SSE streaming for real-time responses with typing/thinking indicators | Must | As a user, I see responses stream in real time so I know work is happening | SSE connection established within 500ms; tokens appear as they arrive; thinking indicator shows during model processing |
| `PRD-v2-CHT-003` | Code blocks with syntax highlighting, copy button, and language label | Must | As a developer, I receive code with proper formatting so I can read and use it immediately | Code blocks detect language from markdown or model output; syntax highlighting via Shiki/Prism; copy button copies to clipboard |
| `PRD-v2-CHT-004` | Artifacts panel for generated content (documents, images, files) | Must | As a user, I see generated artifacts in a side panel so I can review and download them | Artifacts appear in right panel with type icon, title, timestamp; downloadable with one click; linked to run provenance |
| `PRD-v2-CHT-005` | Support switching between agents mid-conversation with context preservation | Should | As a user, I switch from Claude to Kimi in the same session so I compare outputs | Context (last N messages) follows to new agent; system prompt adapts to agent personality; switch is logged |
| `PRD-v2-CHT-006` | Message retry and regeneration | Should | As a user, I regenerate a response if the first one is unsatisfactory | Regenerate button on each assistant message; creates new run with same context; old message remains visible |
| `PRD-v2-CHT-007` | Export conversation as Markdown or JSON | Could | As a user, I export chat history for documentation or sharing | Export button in session menu; Markdown preserves formatting; JSON includes full metadata |
| `PRD-v2-CHT-008` | Tool call display: show which tool was called, with what arguments, and the result | Must | As an operator, I see exactly what tools an agent invoked so I audit its actions | Tool call blocks show tool name, arguments (sanitized if secrets), execution time, success/failure, result preview |
| `PRD-v2-CHT-009` | Message input with multiline support, attachment upload, and agent mention (@Crystal) | Should | As a user, I mention specific agents and attach files to my messages | @ triggers agent autocomplete; file upload shows progress; attachments linked to message |
| `PRD-v2-CHT-010` | Empty states distinguish "no messages", "session deleted", and "loading" | Must | As a user, I understand why a chat area is empty | Each empty state has distinct icon, title, and helper text; loading shows skeleton shimmer |

---

### 5.4 Mission Board (Kanban) (PRD-v2-KBN)

Drag-drop board for coordinating agent teams across task lifecycle.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-KBN-001` | Kanban board with columns: Backlog, Ready, Running, Review, Done | Must | As a workspace owner, I visualize all team tasks on a board so I track progress | Board loads within 2s; columns are clearly labeled; task counts shown per column |
| `PRD-v2-KBN-002` | Drag-and-drop task cards between columns with state transition validation | Must | As a workspace owner, I move tasks by dragging so I update status naturally | Drag uses native HTML5 DnD or library; drop targets highlight on hover; invalid transitions blocked with toast explanation |
| `PRD-v2-KBN-003` | Task cards show: title, assigned agent avatar, status dot, priority badge, cost estimate, artifact count | Must | As an operator, I see task details at a glance without opening each card | Card renders compact summary; agent avatar is 24px colored circle; priority badge uses color (red=high, yellow=medium, green=low) |
| `PRD-v2-KBN-004` | Click card to open detail drawer with full task info, run history, and artifacts | Must | As a workspace owner, I inspect task details in a drawer so I don't lose board context | Drawer slides from right; shows task definition, current run state, step timeline, linked artifacts; close returns to board |
| `PRD-v2-KBN-005` | Filter by agent, status, priority, and date range | Should | As a workspace owner, I filter the board so I focus on relevant tasks | Filter bar at top; multi-select filters; filter state in URL for shareability; clear filters button |
| `PRD-v2-KBN-006` | Bulk actions: select multiple cards, move to column, archive, or assign to agent | Could | As a workspace owner, I perform bulk actions so I manage many tasks efficiently | Checkbox on each card; bulk action bar appears on selection; actions applied with confirmation |
| `PRD-v2-KBN-007` | Swimlanes by project or agent | Could | As a workspace owner, I group tasks by project so I see parallel workstreams | Horizontal swimlane headers; tasks grouped under project/agent name; collapsible |

---

### 5.5 Studio (PRD-v2-STU)

Media generation module with tabs for Images, Videos, and Speech. Supports 12 output formats inspired by NotebookLM.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-STU-001` | Studio tabbed interface: Images, Videos, Speech | Must | As a media producer, I navigate between media types in tabs so I access the right tool | Tabs switch content area; active tab underlined with accent color; URL reflects active tab |
| `PRD-v2-STU-002` | Images: support PNG, JPG, WebP, SVG generation with count per format | Must | As a designer, I generate images in multiple formats so I use them across projects | Format selector shows count of existing images per format; generation shows progress bar; output appears in gallery grid |
| `PRD-v2-STU-003` | Videos: support MP4, WebM, GIF generation with count per format | Should | As a content creator, I generate short videos so I enhance my content | Format selector shows count; generation shows progress with ETA; preview on hover |
| `PRD-v2-STU-004` | Speech: support WAV, MP3, OGG, FLAC synthesis | Should | As a podcaster, I synthesize speech so I create voiceovers | Format selector shows count; voice selector (if multiple voices); playback inline |
| `PRD-v2-STU-005` | Generation parameters: prompt input, negative prompt, size, quality, seed | Must | As a creator, I control generation parameters so I get predictable results | Parameters persist per session; presets for common sizes; seed shown and copyable for reproducibility |
| `PRD-v2-STU-006` | Gallery view with grid layout, metadata overlay, and download | Must | As a creator, I browse generated media in a gallery so I find and reuse assets | Grid shows thumbnail + format badge + timestamp; hover shows metadata (prompt, seed, model); click opens lightbox |
| `PRD-v2-STU-007` | Each generated media is an artifact with full provenance (prompt, model, parameters, timestamp) | Must | As an operator, I trace every generated image back to its creation parameters | Artifact page shows full provenance; links to run and agent; exportable as JSON |
| `PRD-v2-STU-008` | Delete media with confirmation and audit log | Should | As a workspace owner, I delete old media with audit trail so I manage storage | Delete requires confirmation; soft delete with 30-day retention; deletion event in audit log |

---

### 5.6 Notebook (KB) (PRD-v2-NBK)

Self-hosted markdown knowledge base with wiki-links, backlinks, and semantic search.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-NBK-001` | Create, edit, and delete markdown pages with WYSIWYG or raw markdown editor | Must | As a knowledge worker, I write and edit documentation in a markdown editor so I maintain our KB | Editor supports both modes; toolbar for common formatting; auto-save every 5s; conflict detection |
| `PRD-v2-NBK-002` | Wiki-links: `[[Page Name]]` auto-creates bidirectional links | Must | As a knowledge worker, I link between pages so I build a connected knowledge graph | `[[` triggers page autocomplete; creating new page from link works; broken links shown in distinct style |
| `PRD-v2-NBK-003` | Backlinks panel: every page shows which pages link to it | Must | As a knowledge worker, I discover related content via backlinks so I never miss connections | Backlinks panel in right sidebar; shows linking page title + excerpt; click navigates to source |
| `PRD-v2-NBK-004` | Full-text search across all pages | Must | As a user, I search the KB so I find relevant documentation | Search is instant (debounced 300ms); highlights matches; supports phrase queries; shows result count |
| `PRD-v2-NBK-005` | Semantic search via pgvector embeddings | Should | As a user, I find conceptually related pages even if keywords don't match | Search results include "semantic matches" section; shows similarity score; requires PostgreSQL + pgvector |
| `PRD-v2-NBK-006` | Page history with diff view | Should | As a knowledge worker, I review page history so I track changes and revert if needed | History shows chronological list of edits; diff view highlights additions/deletions; revert to any version |
| `PRD-v2-NBK-007` | Notebook is workspace-scoped; no cross-workspace page access | Must | As a workspace owner, I know our KB is isolated from other workspaces | Pages carry workspace_id; cross-workspace access denied; search scoped to current workspace |
| `PRD-v2-NBK-008` | Export page or entire notebook as Markdown ZIP | Could | As a user, I export the KB for backup or migration | Export button in settings; ZIP contains all .md files with metadata JSON; preserves wiki-links as relative paths |

---

### 5.7 Skills / Workflows (PRD-v2-WFL)

Templated DAGs for reusable agent workflows.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-WFL-001` | Skill template: "Daily X Digest" — scrapes configured sources, summarizes with Alex, delivers via email | Should | As a marketer, I run a daily digest so I stay informed without manual research | Template prompts for sources and delivery email; runs on schedule; output is a markdown artifact |
| `PRD-v2-WFL-002` | Skill template: "Content Pipeline" — research → outline → draft (Alex) → review (Joe) → publish | Should | As a content manager, I run a content pipeline so I produce articles with built-in QA | DAG shows 4 steps with agent assignments; Joe's review gate blocks publish until approved; artifacts at each stage |
| `PRD-v2-WFL-003` | Skill template: "SEO Audit" — crawl site → analyze (Crystal) → generate report → suggest fixes | Could | As an SEO specialist, I run automated SEO audits so I identify issues systematically | Template prompts for target URL; output is structured report with priority ratings; suggestions linked to knowledge base |
| `PRD-v2-WFL-004` | Visual DAG builder: nodes are steps, edges are dependencies, agents assigned to nodes | Should | As a technical operator, I build custom workflows visually so I don't write DAG JSON by hand | Drag nodes from palette; connect with edges; assign agent per node; validate DAG (no cycles, all nodes reachable) |
| `PRD-v2-WFL-005` | Workflow execution with live status per node | Must | As an operator, I see each step's status in a workflow so I know where bottlenecks are | Running nodes pulse; completed nodes show checkmark; failed nodes show X with error detail; tooltip shows step output |
| `PRD-v2-WFL-006` | Workflow scheduling: manual, cron, or event-triggered | Should | As a workspace owner, I schedule workflows so they run automatically | Cron builder UI; event triggers (new artifact, new task); timezone-aware scheduling; next run preview |

---

### 5.8 Two-Lane Verifier (PRD-v2-TLV)

Deterministic + LLM quality gates for artifact acceptance.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-TLV-001` | Deterministic lane: schema validation, lint, policy check, regex guards, checksum | Must | As a QA lead, I enforce deterministic checks so obvious errors never pass | Configurable rules per artifact type; each rule shows pass/fail + detail; lane fails if any rule fails |
| `PRD-v2-TLV-002` | LLM lane: quality review, factual consistency, tone evaluation, safety review | Must | As a QA lead, I get AI-powered quality assessment so subjective issues are flagged | Uses configured review model; outputs structured score per dimension; confidence shown; lane fails if score < threshold |
| `PRD-v2-TLV-003` | Artifact blocked from Workspace Gallery until both lanes pass | Must | As a workspace owner, I know no unverified artifact enters our gallery | Failed artifacts show in "Needs Review" queue; passed artifacts auto-promote to Gallery; bypass requires explicit override |
| `PRD-v2-TLV-004` | Verifier results are stored as audit events linked to artifact and run | Must | As an auditor, I trace verifier decisions to the exact checks run | Each verification creates audit event; links artifact_id, run_id, rules applied, scores, timestamp |
| `PRD-v2-TLV-005` | Configurable thresholds per artifact type and workspace | Should | As a workspace owner, I adjust quality thresholds so standards match our needs | UI for threshold configuration; presets (strict, standard, lenient); per-artifact-type overrides |
| `PRD-v2-TLV-006` | Human override with mandatory reason and audit trail | Should | As a workspace owner, I override verifier results in exceptional cases | Override button shows only for failed artifacts; requires reason text; event logged with actor, reason, original scores |

---

### 5.9 BYOK Model Gateway (PRD-v2-GWY)

Intelligent provider routing with capability matching, cost optimization, and fallback chains.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-GWY-001` | Provider-neutral model profiles with capability declaration | Must | As a technical operator, I define model profiles by capability so my workflows are provider-agnostic | Profile includes: name, provider, model ID, capabilities (chat, code, image, vision), max tokens, cost per 1K tokens |
| `PRD-v2-GWY-002` | Capability-based routing: match task requirements to model capabilities | Must | As an operator, tasks route to models that can actually handle them | Routing checks task requirements against model capabilities; no routing to unsupported models; fallback for ambiguous matches |
| `PRD-v2-GWY-003` | Cost-optimized routing: select cheapest qualified provider | Should | As a workspace owner, I minimize costs by routing to cheapest capable model | Cost comparison table visible; routing decision logged; user can override with cost-preference toggle |
| `PRD-v2-GWY-004` | Latency-priority routing: select lowest-latency provider for real-time tasks | Could | As a user, I get fast responses for chat by routing to low-latency models | Latency benchmark per provider; routing decision considers task priority; override in task settings |
| `PRD-v2-GWY-005` | Quality-priority routing: select highest-quality provider for critical tasks | Could | As a user, I get best quality for important tasks by routing to top-tier models | Quality score per model per task type; routing decision logged; override available |
| `PRD-v2-GWY-006` | Fallback chain: if primary provider fails, automatically try secondary, then tertiary | Must | As an operator, my tasks don't fail just because one provider is down | Fallback chain configured per workspace; each fallback attempt logged; total timeout enforced; notification on final failure |
| `PRD-v2-GWY-007` | Transparent routing log: show which provider was selected, why, and fallback history | Must | As an operator, I understand why a specific model was used | Routing log in run detail shows: requested profile, selected provider+model, routing reason, fallback attempts, final cost |
| `PRD-v2-GWY-008` | Workspace-level provider enable/disable and budget limits | Must | As a workspace owner, I control which providers my team can use and how much they spend | Toggle per provider per workspace; budget input with currency; hard stop or warn threshold; usage bar shows consumption |

---

### 5.10 Workspace & Memory (PRD-v2-WSP)

Workspace-centered organization with permission-aware memory.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-WSP-001` | Create workspace with name, description, icon, color theme, and policy profile | Must | As a workspace owner, I create isolated workspaces so projects don't interfere | Form validates name uniqueness; icon selector with 20 presets; color theme affects sidebar accent; policy profile selected from presets |
| `PRD-v2-WSP-002` | Workspace-scoped data: tasks, runs, approvals, artifacts, memory, costs, audit events | Must | As a workspace member, I know our data is never visible to other workspaces | Every record carries workspace_id; API rejects cross-workspace requests; search scoped to workspace |
| `PRD-v2-WSP-003` | Memory facts with source, scope, producer, confidence, and verification state | Must | As an operator, I trust memory because I can see where it came from | Memory record shows: source (agent/user), producer (model/agent), confidence score, verification status, created_at |
| `PRD-v2-WSP-004` | Semantic memory retrieval with source, age, and reason for inclusion | Should | As a user, I understand why certain context was included in my chat | Retrieved memories show in context panel with source link, age, relevance score; hover shows full content |
| `PRD-v2-WSP-005` | Memory correction, supersession, and controlled deletion | Should | As a user, I fix or remove inaccurate memories so they don't propagate | Edit button on memory card; supersede creates new version; delete requires confirmation; audit log tracks changes |
| `PRD-v2-WSP-006` | Cross-workspace memory retrieval denied by default | Must | As a workspace owner, I know memory doesn't leak between projects | Negative tests confirm denial; safe error message; no metadata leakage |
| `PRD-v2-WSP-007` | Artifact gallery with metadata, preview, download, and sharing | Must | As a team member, I browse and reuse artifacts from our workspace gallery | Gallery grid with filters (type, agent, date); preview modal with metadata sidebar; download with format selector; share generates link |
| `PRD-v2-WSP-008` | Workspace member management: invite, remove, role assignment | Must | As a workspace owner, I manage team membership so access is controlled | Invite by email/username; roles: Owner, Operator, Contributor, Viewer; remove with transfer ownership check |

---

### 5.11 Approvals & Governance (PRD-v2-APR)

Human-in-the-loop approval system for consequential actions.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-APR-001` | Approval inbox with pending requests prioritized by risk and age | Must | As a reviewer, I see all pending approvals so I act on urgent items first | Inbox shows: requester, action summary, risk level (low/medium/high), age, expiry; sorted by risk then age; unread badge |
| `PRD-v2-APR-002` | Exact-action approval: request identifies task, run, action, parameters, target, risk, reason, expiry | Must | As a reviewer, I approve exactly what was proposed, not a vague summary | Approval card shows: full action description, parameters (sanitized), target resource, risk classification, proposed effects, expiry time |
| `PRD-v2-APR-003` | Approve, reject, request revision, expire, cancel, invalidate outcomes | Must | As a reviewer, I have clear decision options so I communicate intent precisely | Each outcome has distinct button + confirmation modal; reject requires reason; revision request includes comment field |
| `PRD-v2-APR-004` | Approval bound to exact parameters; material change requires new approval | Must | As an operator, I know approved actions can't be silently modified | Parameter hash stored with approval; execution time verification; mismatch triggers new approval request |
| `PRD-v2-APR-005` | Approval expiry blocks execution and requires renewal | Must | As a workspace owner, I know approvals don't last forever | Expiry shown as countdown; expired approvals move to "Expired" tab; renewal creates new request with same parameters |
| `PRD-v2-APR-006` | Prevent double consumption or replay of approval | Must | As an auditor, I know each approval is used exactly once | Approval state machine: pending → approved → consumed; consumed approvals rejected on replay; audit event per state change |
| `PRD-v2-APR-007` | Revocation of future authority without rewriting prompts | Must | As a workspace owner, I revoke an agent's permission instantly | Revoke button in agent permissions panel; takes effect within 5s; active runs paused; audit event logged |
| `PRD-v2-APR-008` | Risk classification: low (auto-approve under policy), medium (single approver), high (multi-approver) | Should | As a workspace owner, I configure approval rules so low-risk actions aren't bottlenecked | Risk matrix configurable per workspace; auto-approve threshold; multi-approver for high-risk; escalation on timeout |
| `PRD-v2-APR-009` | Approval decisions are immutable audit events | Must | As an auditor, I reconstruct who approved what and when | Every decision creates immutable audit event; includes: approver identity, decision, timestamp, request hash, reason |

---

### 5.12 Audit & Cost (PRD-v2-AUD)

Complete observability with immutable audit events and cost attribution.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-AUD-001` | Immutable audit event log: identity, workspace, task, run, step, approval, artifact, timestamp | Must | As an auditor, I reconstruct any decision from the event log | Events append-only; tamper-evident (hash chain or similar); queryable by workspace, date range, actor, event type |
| `PRD-v2-AUD-002` | Execution receipt per run: inputs, configuration, steps, outputs, effects, cost | Must | As an operator, I have a complete receipt for every run | Receipt auto-generated on run completion; links all related entities; exportable as PDF/JSON; includes failure reasons if applicable |
| `PRD-v2-AUD-003` | Cost dashboard: spend by workspace, project, task, run, provider, model, time period | Must | As a workspace owner, I understand where money is spent | Dashboard shows: total spend, breakdown by provider/model, trend chart, budget vs actual, top spenders |
| `PRD-v2-AUD-004` | Cost attribution to workspace, task, run, identity, provider, model | Must | As a finance lead, I attribute every dollar of AI spend | Every billable event carries: workspace_id, task_id, run_id, identity_id, provider, model, tokens, cost |
| `PRD-v2-AUD-005` | Budget thresholds: hard stop or warning at workspace and run level | Must | As a workspace owner, I prevent runaway costs | Threshold input in workspace settings; hard stop blocks new runs; warning shows banner; notification on threshold breach |
| `PRD-v2-AUD-006` | Distinguish provider-reported, calculated, estimated, pending, unavailable cost values | Must | As an operator, I never mistake an estimate for a fact | Cost labels: "provider-reported", "calculated", "estimated", "pending", "unavailable"; estimated values show confidence |
| `PRD-v2-AUD-007` | Reconciliation view: compare provider bills to Agent OS cost events | Should | As a finance lead, I reconcile provider invoices with internal records | Import provider CSV; match by date/model/run; show matched/unmatched/reconciled status; export discrepancy report |
| `PRD-v2-AUD-008` | Health dashboard: control plane, adapters, storage, queue, event processing | Must | As a technical operator, I diagnose system health | Cards for each subsystem: status (green/yellow/red), last check, key metric; click drills to detail view |
| `PRD-v2-AUD-009` | Health states: registered, reachable, validated, degraded, failed, stale, unknown | Must | As a technical operator, I understand precise health status | Each state has distinct icon + label + color; degraded shows specific issue; stale shows last success timestamp |
| `PRD-v2-AUD-010` | Backup and restore: documented procedure covering all retained data | Must | As a technical operator, I recover from failures | Backup script in repo; covers DB, Redis, file store; restore procedure tested monthly; RPO < 1 hour, RTO < 4 hours |

### 5.13 SEO Module (PRD-v2-SEO)

Search engine optimization module powering Goldie’s agency workflows: SERP intelligence, rank tracking, competitor watch, content brief generation, and direct CMS publishing.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-SEO-001` | SERP API integration: query live search results via SerpAPI, DataForSEO, or Playwright scraping | Must | As an SEO strategist, I see current search results so I can plan content | Supports Google (desktop/mobile), Bing; configurable locale/device; raw HTML and parsed JSON; rate-limit aware |
| `PRD-v2-SEO-002` | Content brief generator: analyze top 10 results → extract headings, keywords, questions, word count, authority signals → structured brief | Must | As a content strategist, I generate a data-driven brief before writing | Top 10 fetched automatically; brief includes: suggested title, meta description, heading outline, target word count, keyword density, question targets, authority gap analysis |
| `PRD-v2-SEO-003` | Rank tracker with historical data: store daily position per keyword per engine/device, render trend charts | Must | As an SEO operator, I track keyword position over time | Daily snapshots stored; chart shows position history (0–100); volatility alerts when position changes >5 in 24h |
| `PRD-v2-SEO-004` | Competitor watch: monitor competitor domains for new content, backlink changes, and rank shifts | Must | As an SEO lead, I know immediately when a competitor publishes or outranks us | Configurable competitor URLs; alerts on new pages detected, rank changes, and title/meta updates |
| `PRD-v2-SEO-005` | Keyword research: search volume, difficulty, intent classification (informational, navigational, transactional, commercial), clustering | Should | As a strategist, I discover new keyword opportunities | Volume/difficulty from provider API or estimates; intent classified by model; clustering groups semantically similar keywords |
| `PRD-v2-SEO-006` | CMS connectors for WordPress (REST API), Shopify (Admin API), Webflow (CMS API): publish draft → review → publish | Must | As a publisher, I push approved content directly to our CMS without copy-paste | OAuth or API key auth; draft creation with SEO metadata; preview link; status sync (draft → review → published); error retry |
| `PRD-v2-SEO-007` | Internal link suggester: scan vault/notes → propose contextual internal links for new content | Should | As an SEO writer, I enrich articles with internal links automatically | Scans notes and published CMS posts; proposes anchor text and target URL; confidence score per suggestion |
| `PRD-v2-SEO-008` | SEO audit crawler: technical checks for page speed, mobile-friendliness, schema markup, broken links, canonical tags | Should | As a technical SEO, I find and fix site issues | Crawl scheduling; issues scored by severity; exportable checklist; integration with workflow to auto-create fix tasks |
| `PRD-v2-SEO-009` | Traffic analytics dashboard: connect Google Search Console API and GA4 to pull real clicks, impressions, CTR, sessions | Should | As an SEO lead, I correlate rankings with actual traffic | OAuth to GSC and GA4; daily data pull; dashboard shows traffic by page/keyword/query; trend lines aligned with rank charts |
| `PRD-v2-SEO-010` | White-label SEO reports: branded PDF/HTML reports with charts, summaries, and next-step recommendations | Could | As an agency owner, I send professional reports to clients | Configurable logo, colors, cover page; scheduled generation; export PDF + HTML; includes all campaign KPIs |

---

### 5.14 Visual Workflow Builder (PRD-v2-VWB)

Drag-and-drop DAG builder for designing, simulating, and sharing agentic workflows with conditional branches, loops, and human approval gates.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-VWB-001` | Drag & drop canvas: add, move, connect, and delete nodes visually on an infinite dark canvas | Must | As a workflow designer, I build agent pipelines without writing code | Pan, zoom, snap-to-grid; undo/redo; multi-select; keyboard shortcuts for common actions |
| `PRD-v2-VWB-002` | Conditional / if-else nodes: branch workflow based on expression against runtime variables | Must | As a designer, I route tasks differently depending on quality scores | Expression editor with autocomplete; supports simple (`{{score}} > 8`) and advanced (JavaScript sandbox); visual branch labels |
| `PRD-v2-VWB-003` | Loop / repeat nodes: iterate N times, while/until condition, or over a collection | Must | As a designer, I repeat tasks until criteria are met or for each item in a list | Loop types: count, while, for-each; break/continue support; max iteration guard to prevent infinite loops |
| `PRD-v2-VWB-004` | Approval gate nodes: pause execution, send notification, surface human review UI, resume with context | Must | As an operator, I insert human checkpoints into automated workflows | Gate shows action preview; approve/reject/revise options; comment required on reject; timeout and escalation rules |
| `PRD-v2-VWB-005` | Cron trigger nodes: schedule recurring workflow executions with timezone support | Must | As an operator, I run workflows on a schedule | Cron expression builder with presets; timezone selector; next-run preview; skip if already running |
| `PRD-v2-VWB-006` | Webhook trigger nodes: receive external HTTP events to start a workflow with signature verification | Must | As a developer, I trigger Agent OS workflows from external systems | HMAC signature verification; configurable HTTP methods; payload parsed into workflow variables; retry on queue overflow |
| `PRD-v2-VWB-007` | Simulation / dry-run mode: execute workflow without external API calls, inspect variables at each step | Must | As a designer, I test workflows safely before going live | Simulated trace shown step-by-step; variable inspector; breakpoints; condition branches evaluated against injected test values |
| `PRD-v2-VWB-008` | Workflow marketplace: import/export workflows as YAML/JSON; community gallery; version control per workflow | Should | As a user, I share workflows with my team or the community | Export preserves nodes, edges, and metadata; import validates schema; version history with diff; fork/clone support |

---

### 5.15 Dynamic Agent Roles (PRD-v2-DAR)

Replace fixed agent assignments with fully configurable roles, dynamic assignment, and per-role skill templates.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-DAR-001` | Create custom agent roles: name, description, icon, color, system prompt template, memory profile, autonomy level | Must | As a workspace owner, I define roles that match our org, not fixed personas | Role creation form with validation; slug auto-generated; system prompt supports variables; icon from built-in set |
| `PRD-v2-DAR-002` | Assign any agent to any role dynamically: many-to-many agents ↔ roles with priority and primary flag | Must | As an operator, I assign the best available agent to a role mid-flight | Assignment UI shows agent capacity; priority ordering; primary flag for default selection; re-assignment updates running tasks optionally |
| `PRD-v2-DAR-003` | Role-based skill templates: each role declares required and optional skills with versioning | Must | As a workspace owner, I enforce skill coverage per role | Skills grid per role; required vs optional; version pinning; missing-skill warning when assigning an under-qualified agent |
| `PRD-v2-DAR-004` | Role switching mid-conversation: preserve context while changing system prompt and capabilities | Should | As a user, I redirect a conversation to a different specialty without losing history | Switch triggered by user or agent; context summarized and passed; old role noted in metadata; seamless UI transition |
| `PRD-v2-DAR-005` | Role history and analytics: usage frequency, success rate, average cost, average latency per role | Should | As a manager, I understand which roles deliver value | Dashboard shows role usage over time; success/failure rates; cost attribution; filter by workspace and date range |
| `PRD-v2-DAR-006` | Clone/copy role configurations: duplicate a role with all skills, prompt, and settings to a new role | Should | As a workspace owner, I iterate on role configs without starting from scratch | Clone action creates new role with suffix; prompts/skills copied; assignments not copied by default; edit before save |

### 5.16 Voice / Talk Mode (PRD-v2-VCE)

Voice-first interaction layer that makes Agent OS feel like a real operating system — hands-free, natural, and accessible.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-VCE-001` | Push-to-Talk: hold Spacebar to record, release to send; visual waveform during recording in agent color | Must | As a user, I talk to my agents naturally using a push-to-talk gesture I already know from Discord/Voxer | Spacebar press starts recording within 200ms; release sends audio blob to STT; waveform bars animate in real time with amplitude; cancel via swipe-left or Escape while holding |
| `PRD-v2-VCE-002` | Text-to-Speech with local (Kokoro) and cloud (ElevenLabs, Grok) options; per-agent voice profiles with pitch/speed | Must | As a user, I hear each agent speak in a distinct voice so I know who is talking without looking | TTS engine selectable per agent; voice profile stored per agent (pitch, speed, voice ID); streaming TTS starts playback within 500ms of first sentence; mute/unmute toggle per agent |
| `PRD-v2-VCE-003` | Speech-to-Text with local Whisper (faster-whisper CPU int8) and cloud OpenAI Whisper API; language auto-detection + punctuation correction | Must | As a user, I speak in any supported language and Agent OS transcribes accurately offline | Local STT runs fully offline; cloud STT used when local model confidence < threshold; language detected automatically; punctuation auto-corrected; noise suppressed via RNNoise or similar |
| `PRD-v2-VCE-004` | Agent Vocal Mode: agent narrates thinking process with configurable verbosity; reads back task results in voice | Should | As an operator, I hear what the agent is doing while I work on something else | Configurable verbosity (silent / brief / verbose); narration triggers via "is thinking" events; task result read-back optional per task; respects agent mute state |
| `PRD-v2-VCE-005` | Wake word detection: "Hey Agent OS" activates listening hands-free; VAD for natural conversation flow | Should | As a user, I activate voice mode without touching the keyboard | Wake word detected via local lightweight model; VAD detects end-of-utterance for automatic send; configurable wake word phrase; disable/enable per workspace |
| `PRD-v2-VCE-006` | Talk Mode UI: full-screen overlay with large mic button, animated agent avatar (mouth moves), subtitle transcript scroll, conversation history | Must | As a user, I have a dedicated voice-first interface that feels immersive | Full-screen panel toggled from chat or global shortcut; agent avatar shows speaking animation (mouth waveform sync); transcript scrolls like subtitles; audio+text hybrid history; mode toggle: Text-only ↔ Voice-first ↔ Auto |
| `PRD-v2-VCE-007` | Audio retention policy: auto-delete voice recordings after N days (configurable); separate from text messages | Must | As a workspace owner, I control how long audio recordings are retained | Default retention: 30 days; configurable per workspace; audio deleted via scheduled Celery task; text transcript retained independently unless user deletes |
| `PRD-v2-VCE-008` | Privacy toggle: local-only voice mode (Whisper + Kokoro) with no cloud transmission; explicit confirmation required to enable cloud | Must | As a privacy-conscious user, I know my voice never leaves my machine unless I explicitly allow it | Default mode: local-only; cloud toggle shows warning modal; per-session cloud choice stored in session metadata; no audio sent to cloud without user confirmation |

---

### 5.17 Import / Export (PRD-v2-IMP)

Data migration layer that reduces adoption friction by importing from existing tools and ensures data portability via rich exports.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-IMP-001` | Obsidian Vault import: accept ZIP or folder path; parse .md → notes (preserve wiki-links, tags, frontmatter); attachments → artifacts; graph → note_links; conflict resolution skip/overwrite/merge | Must | As an Obsidian user, I import my entire vault into Agent OS without losing connections | ZIP upload or local path input; wiki-links `[[...]]` converted to Notebook links; tags `#...` preserved; frontmatter YAML parsed into note metadata; attachments stored as artifacts; progress bar with ETA; conflict resolution UI for duplicates |
| `PRD-v2-IMP-002` | Notion import: accept Notion export ZIP (HTML + CSV + files); parse HTML → markdown; preserve page hierarchy → notebook folders; databases → structured notes; embeds → artifact references | Must | As a Notion user, I migrate my workspace with hierarchy and databases intact | HTML parsed to markdown via html-to-markdown; page hierarchy mapped to Notebook folder structure; databases converted to structured notes with properties; Notion embeds become artifact references; progress tracked per page |
| `PRD-v2-IMP-003` | ChatGPT / Claude export import: JSON → chat sessions with messages, model, timestamp; preserve thread structure; tag with source | Should | As a ChatGPT/Claude user, I bring my conversation history into Agent OS | OpenAI export JSON parsed to sessions; Anthropic export parsed similarly; conversation threads preserved; shared links/artifacts extracted from messages; auto-tag "imported-from-chatgpt" / "imported-from-claude" |
| `PRD-v2-IMP-004` | Evernote ENEX import: notes with tags, notebooks, attachments; Apple Notes / OneNote documented manual paths | Could | As an Evernote user, I migrate my legacy notes | ENEX XML parsed to markdown; tags and notebooks preserved; attachments stored as artifacts; Apple Notes and OneNote noted as manual/third-party export paths in docs |
| `PRD-v2-IMP-005` | Generic markdown import: any folder of .md files → notes; auto-detect wiki-links, tags, frontmatter; bulk drag-and-drop | Should | As a user, I import any folder of markdown files easily | Folder upload or drag-and-drop; auto-detects wiki-links, tags, frontmatter; bulk import with progress bar; conflict resolution options |
| `PRD-v2-IMP-006` | Export: workspace ZIP (notes + chats + artifacts + settings), notebook ZIP (Obsidian-compatible .md), chat JSON/Markdown transcript, SEO PDF/HTML; AES-256-GCM encrypted export with password | Must | As a user, I export my data in standard formats for backup or migration | Workspace export generates ZIP with DB dump, notes/, artifacts/, config.json; notebook export produces Obsidian-compatible .md files with preserved wiki-links; chat export as JSON or Markdown; SEO reports as PDF/HTML; encrypted export with user-provided password and integrity checksum |

---

### 5.18 Disaster Recovery (PRD-v2-DR)

Backup, recovery, and resilience for a local-first product — trust requires recoverability.

| ID | Requirement | Priority | User Story | Acceptance Criteria |
|---|---|---|---|---|
| `PRD-v2-DR-001` | Auto-backup: daily at 2 AM (configurable frequency); full workspace (DB + notes + artifacts + config); tar.gz/zstd compression; retention: 7 daily + 4 weekly + 12 monthly | Must | As a workspace owner, I know my data is backed up automatically every night | Celery scheduled task; backup includes SQLite/PostgreSQL dump, files/, config/; compression configurable; retention policy enforced via automated cleanup; backup metadata stored (size, duration, checksum) |
| `PRD-v2-DR-002` | Cloud backup targets: S3-compatible (AWS, Wasabi, B2, MinIO), Dropbox, Google Drive; encrypted with AES-256-GCM before upload; chunked for >100 MB | Should | As a user, I store backups off-site in my preferred cloud | Target configured via UI/API; pre-upload encryption with user-derived key; chunked upload for large workspaces; retry with exponential backoff; target health check before upload |
| `PRD-v2-DR-003` | Git sync for Notebook: auto-commit on save (configurable); auto-generated commit messages; remote push to GitHub/GitLab/Gitea; branch per workspace; diff view in UI | Should | As a developer, I version-control my knowledge base | Git repository initialized in Notebook directory; commit on save or periodic; remote push with configured credentials; branch naming: `agentos-notebook-{workspace_slug}`; diff view shows additions/deletions per page |
| `PRD-v2-DR-004` | Encrypted export: one-click "Export Everything" → password-protected ZIP with DB dump, notes, artifacts, config, agent configs; API keys excluded by default (opt-in) | Must | As a user, I create a portable encrypted snapshot of my entire workspace | Export includes all workspace-scoped data; AES-256-GCM encryption; API keys excluded by default with checkbox to include; checksum (SHA-256) included; integrity report generated |
| `PRD-v2-DR-005` | One-click restore: from backup ZIP with version detection, integrity validation, temp restore, atomic swap; rollback keeps previous state 24h; point-in-time and granular restore | Must | As a user, I restore my workspace from backup without technical expertise | Upload backup ZIP; version detected and validated; restored to temp directory; atomic swap on success; previous state retained 24h for rollback; granular restore options: full workspace, Notebook only, Chat history only |
| `PRD-v2-DR-006` | Health monitoring dashboard: last backup status, failure alerts (email/push), disk space warning, monthly automated integrity check | Should | As a workspace owner, I know immediately if backup health degrades | Dashboard widget shows last backup time + status; alert on failure (configurable channels); disk space warning at 85%; monthly integrity check restores a random backup to temp and validates; results logged |

---

## 6. User Stories

### US-001: First-Time Setup
> As a solo operator, I install Agent OS v2 locally using Docker Compose so I can start using it within 15 minutes.

**Acceptance:**
- One-command install: `docker compose up -d`
- First-run wizard creates admin user and default workspace
- Health check endpoint confirms all services running
- No manual database migration needed (Alembic auto-runs)

### US-002: Delegate to Crystal
> As a workspace owner, I ask Crystal to "create a content pipeline for the blog" so she sets up the workflow with Alex and Joe assigned.

**Acceptance:**
- Crystal understands natural language task description
- Creates workflow DAG with correct steps and agent assignments
- Shows me the DAG for confirmation before execution
- Stores workflow template for reuse

### US-003: Chat with Multi-Provider Fallback
> As a developer, I start a coding chat with Claude, but Claude is rate-limited, so Agent OS automatically falls back to Kimi without losing my context.

**Acceptance:**
- Claude rate-limit detected within 5s
- Fallback to Kimi initiated automatically
- Context (last 20 messages) preserved
- User notified of fallback with reason
- Routing log shows the chain

### US-004: Generate and Verify Image
> As a designer, I prompt Elvis to generate a product mockup, which passes the Two-Lane Verifier and appears in the Gallery.

**Acceptance:**
- Elvis accepts image generation prompt
- Studio shows generation progress
- On completion, deterministic lane runs (file integrity, size check)
- LLM lane runs (quality, safety)
- Both lanes pass → artifact promoted to Gallery
- Gallery shows image with full provenance

### US-005: Build Knowledge Base
> As a consultant, I create a "Client Onboarding" page in the Notebook, link to "Contracts" and "SLA" pages, and find it via semantic search when I search "agreement terms".

**Acceptance:**
- Page created with markdown editor
- Wiki-links `[[Contracts]]` and `[[SLA]]` created
- Backlinks panel shows "Client Onboarding" on Contracts and SLA pages
- Semantic search for "agreement terms" returns all three pages with relevance scores

### US-006: Approve Consequential Action
> As a senior developer, I review and approve a pull request creation proposed by OpenClaw because it passed all automated checks.

**Acceptance:**
- OpenClaw proposes PR creation with title, description, changed files
- Approval request appears in inbox with "high" risk
- Reviewer sees exact diff, test results, and run history
- Approval creates PR; rejection cancels with reason logged
- Audit event links approval to PR URL

### US-007: Track Team Spend
> As an agency owner, I view the cost dashboard and see that Workspace "Client Alpha" spent $127 this week, mostly on Claude for content generation.

**Acceptance:**
- Dashboard shows spend by workspace
- Drill-down shows tasks, runs, models
- Trend chart compares this week vs last week
- Budget bar shows $127 / $500 (25% used)
- Export CSV for invoicing

### US-008: Recover Interrupted Run
> As an operator, I accidentally restart Docker during a long-running SEO audit, then resume the run from the last checkpoint without duplicate crawl.

**Acceptance:**
- Run state persists in database
- On restart, Mission Control shows "interrupted" status
- Resume button available with last checkpoint timestamp
- Resume continues from checkpoint; completed steps skipped
- No duplicate crawl requests sent
- Audit log shows interruption and resumption events

### US-009: Board Coordination
> As a product manager, I drag a task from "Running" to "Review" because the agent finished, and Joe automatically picks it up for verification.

**Acceptance:**
- Drag task to Review column
- State transition validated (running → review is allowed)
- Joe notified or auto-assigned
- Task card updates to show assigned to Joe
- When Joe finishes, task moves to Done

### US-010: Export Audit Package
> As a compliance officer, I export all audit events for Workspace "Finance" for Q3 2026 as a tamper-evident package.

**Acceptance:**
- Filter events by workspace, date range, event types
- Export generates signed package with hash
- Package includes all events, metadata, and verification signature
- Excludes other workspace data

---

## 7. Acceptance Criteria

### Global Acceptance Criteria

Every feature in Agent OS v2 must satisfy:

| ID | Criterion | Applies To |
|---|---|---|
| `AC-GLOBAL-001` | Feature works in dark theme without visual regressions | All UI |
| `AC-GLOBAL-002` | Feature is keyboard-navigable (Tab, Enter, Escape, arrow keys) | All interactive elements |
| `AC-GLOBAL-003` | Feature is screen-reader accessible (ARIA labels, roles, live regions) | All dynamic content |
| `AC-GLOBAL-004` | Feature respects `prefers-reduced-motion` | All animations |
| `AC-GLOBAL-005` | Feature supports responsive breakpoints: mobile (<640px), tablet (640-1024px), desktop (>1024px) | All primary workflows |
| `AC-GLOBAL-006` | Feature works with both SQLite (solo) and PostgreSQL+pgvector (team) backends | All data features |
| `AC-GLOBAL-007` | Feature enforces workspace isolation for all data access | All data features |
| `AC-GLOBAL-008` | Feature emits audit events for security-relevant actions | All CRUD operations |
| `AC-GLOBAL-009` | Feature handles offline/degraded states gracefully | All network-dependent features |
| `AC-GLOBAL-010` | Feature includes empty states with contextual help | All data-display features |

### Feature-Specific Acceptance Criteria

#### Mission Control
- `AC-MC-001`: DAG renders <2s on initial load; node count supports up to 50 nodes without frame drops
- `AC-MC-002`: SSE updates every 5s; reconnection after disconnect within 3s
- `AC-MC-003`: KPI cards show correct values verified against database queries

#### Chat
- `AC-CHT-001`: SSE streaming starts within 500ms of request; tokens render as they arrive
- `AC-CHT-002`: Code blocks support 20+ languages with syntax highlighting
- `AC-CHT-003`: Sessions persist across browser refresh; scroll position restored

#### Studio
- `AC-STU-001`: Image generation completes within 60s for standard sizes
- `AC-STU-002`: Gallery supports lazy loading for 1000+ items
- `AC-STU-003`: Each format shows accurate count badge

#### Notebook
- `AC-NBK-001`: Wiki-link autocomplete responds within 200ms
- `AC-NBK-002`: Semantic search returns results within 1s for <10K pages
- `AC-NBK-003`: Page history retains last 50 versions

#### Mission Board
- `AC-KBN-001`: Drag-drop works with mouse and touch; keyboard alternative provided
- `AC-KBN-002`: Board loads <2s with up to 100 tasks
- `AC-KBN-003`: Invalid transitions blocked with explanatory toast

#### SEO Module
- `AC-SEO-001`: SERP query returns results within 10s; cached results return within 500ms
- `AC-SEO-002`: Content brief generated within 60s for standard keywords; brief includes all 6 required sections
- `AC-SEO-003`: Rank tracker chart renders within 2s for 50 keywords × 90 days
- `AC-SEO-004`: CMS publish succeeds or fails with detailed error; status sync within 5s
- `AC-SEO-005`: SEO audit crawl completes 1000 URLs within 5 minutes
- `AC-SEO-006`: White-label report generation completes within 30s; PDF is valid and branded

#### Visual Workflow Builder
- `AC-WFL-001`: Canvas renders <1s with ≤50 nodes; drag maintains 60fps
- `AC-WFL-002`: Simulation mode executes full workflow in <5s without external calls
- `AC-WFL-003`: Cron trigger fires within 1 minute of scheduled time
- `AC-WFL-004`: Webhook trigger processes payload and starts execution within 2s
- `AC-WFL-005`: Conditional expression evaluates correctly in both simple and JS sandbox modes

#### Dynamic Agent Roles
- `AC-ROL-001`: Role creation validates all required fields; slug uniqueness enforced
- `AC-ROL-002`: Role switch preserves last 20 messages; no context loss observed
- `AC-ROL-003`: Analytics dashboard shows accurate usage, success rate, and cost per role
- `AC-ROL-004`: Clone operation copies all role config except assignments

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Requirement | Target | Measurement |
|---|---|---|
| Mission Control initial page load | <2s | Lighthouse TTI |
| Chat SSE connection establishment | <500ms | Custom timing |
| API response time (p95) | <200ms | Prometheus metrics |
| Database query time (p95) | <50ms | Query logging |
| DAG render (50 nodes) | <2s | Browser performance API |
| Kanban board load (100 tasks) | <2s | Browser performance API |
| Notebook search (10K pages) | <1s | Custom timing |
| Image generation (standard) | <60s | Studio telemetry |
| Video generation (10s clip) | <5min | Studio telemetry |

### 8.2 Scalability

| Requirement | Target |
|---|---|
| Workspaces per organization | Unlimited (PostgreSQL) / 10 (SQLite) |
| Agents per workspace | 50 |
| Concurrent runs per workspace | 10 |
| Chat sessions per user | 1000 |
| Messages per session | 10,000 |
| Artifacts per workspace | 100,000 |
| Notebook pages per workspace | 50,000 |
| Audit events retention | 2 years (configurable) |
| Max artifact size | 100MB |
| Max total storage per workspace | 100GB (configurable) |

### 8.3 Security

| Requirement | Standard |
|---|---|
| Authentication | JWT with refresh tokens; session expiry |
| Authorization | RBAC with workspace isolation |
| Password storage | bcrypt with salt |
| API rate limiting | 100 req/min per user |
| Secret management | Environment variables or vault; never in source |
| Audit immutability | Append-only log; hash verification |
| Data encryption | TLS 1.3 in transit; AES-256 at rest |
| Input sanitization | All user inputs validated via Pydantic/Zod |
| XSS prevention | Output encoding; CSP headers |
| CSRF protection | SameSite cookies; CSRF tokens for state-changing ops |

### 8.4 Reliability

| Requirement | Target |
|---|---|
| Uptime (local single-node) | 99.5% |
| Run state durability | ≥99% terminal state retention |
| Approval policy enforcement | 100% |
| Cross-workspace isolation | 100% pass rate |
| Backup integrity verification | Monthly |
| Recovery Time Objective (RTO) | <4 hours |
| Recovery Point Objective (RPO) | <1 hour |

### 8.5 Accessibility

| Requirement | Standard |
|---|---|
| WCAG compliance | 2.2 AA |
| Keyboard navigation | All Must journeys completable |
| Screen reader support | NVDA, JAWS, VoiceOver |
| Color independence | Status never color-only |
| Focus management | Visible focus rings; logical tab order |
| Motion preference | `prefers-reduced-motion` respected |
| Text scaling | Readable at 200% zoom |
| Touch target size | Minimum 44x44px |

### 8.6 Compatibility

| Requirement | Target |
|---|---|
| Browsers | Chrome 120+, Firefox 121+, Safari 17+, Edge 120+ |
| Operating systems | Linux (Ubuntu 22.04+), macOS 14+, Windows 11/WSL2 |
| Docker | Engine 24.0+, Compose 2.20+ |
| PostgreSQL | 16+ with pgvector 0.7+ |
| SQLite | 3.45+ |
| Redis | 7.0+ |

---

## 9. Dependencies & Constraints

### 9.1 External Dependencies

| Dependency | Status | Risk |
|---|---|---|
| Anthropic Claude API | Required for Claude adapter | Medium (rate limits) |
| Moonshot Kimi API | Required for Kimi adapter | Medium (availability) |
| XAI Grok API | Required for Grok adapter | High (beta stability) |
| Ollama | Required for local models | Low (open source) |
| OpenRouter | Required for fallback routing | Low (aggregator) |
| Hermes Gateway | Internal service on :8642 | Low (controlled) |
| shadcn/ui | UI component foundation | Low (open source) |
| Framer Motion | Animation library | Low (mature) |

### 9.2 Technical Constraints

- **Local-first default**: MVP must run on a single Linux/WSL machine with Docker Compose
- **No cloud dependency by default**: Core features work without internet after initial setup
- **SQLite as default**: PostgreSQL + pgvector is team mode; SQLite is solo mode
- **Secrets never in source**: All credentials via environment variables or secret vault
- **Dark theme first**: UI is designed dark; light mode is optional post-MVP
- **TypeScript strict**: Frontend uses strict mode; no `any` without documented exception
- **Python 3.12+**: Backend requires 3.12 for improved async and type hints

### 9.3 Business Constraints

- **BYOK**: Users bring their own API keys; no bundled provider credits
- **White-label**: No hard-coded branding; theme configurable per workspace
- **Self-hosted**: No SaaS offering in v2; deployment is customer's responsibility
- **Open core**: Core platform open; premium features TBD post-v2

---

## 10. Open Decisions

The following decisions remain open and require stakeholder input:

| # | Decision | Options | Impact |
|---|---|---|---|
| 1 | **Light mode support** | Ship v2 dark-only vs. ship both | Effort ~2 weeks; accessibility benefit |
| 2 | **Mobile app** | PWA vs. native vs. none | PWA ~4 weeks; native ~12 weeks |
| 3 | **Real-time collaboration** | Operational transforms vs. CRDT vs. none | CRDT most robust; adds ~6 weeks |
| 4 | **Plugin SDK** | v2.3 vs. v3.0 | Enables marketplace; significant architecture |
| 5 | **LLM for verifier** | Same provider as task vs. dedicated cheap model | Cost vs. independence tradeoff |
| 6 | **Video generation backend** | Local GPU (Ollama) vs. cloud API vs. hybrid | Cost, latency, privacy tradeoff |
| 7 | **Notification channels** | In-app only vs. email vs. Slack vs. all | Scope creep risk |
| 8 | **Multi-language UI** | English only vs. i18n framework from start | i18n adds ~3 weeks but saves later |
| 9 | **Telemetry/analytics** | Opt-in vs. opt-out vs. none | Product improvement vs. privacy |
| 10 | **Payment integration** | Stripe for team billing vs. none | Not needed for self-hosted; future SaaS |

---

## Appendix A: Requirement Traceability

| PRD-v2 ID | Vision Section | Prior Document | Status |
|---|---|---|---|
| `PRD-v2-MC-*` | §5.1 Mission Control | `PRD-UI-*` | New |
| `PRD-v2-AGT-*` | §5.2 Named Agents | `PRD-AGT-*` | Extended |
| `PRD-v2-CHT-*` | §5.3 Chat | `FR-UI-*` | Extended |
| `PRD-v2-KBN-*` | §5.4 Mission Board | — | New |
| `PRD-v2-STU-*` | §5.5 Studio | `PRD-ART-*` | Extended |
| `PRD-v2-NBK-*` | §5.6 Notebook | `MEM-001` | New |
| `PRD-v2-WFL-*` | §5.7 Skills / Workflows | `ORC-001` | Extended |
| `PRD-v2-TLV-*` | §5.8 Two-Lane Verifier | — | New |
| `PRD-v2-GWY-*` | §5.9 BYOK Gateway | `PRD-MOD-*` | Extended |
| `PRD-v2-WSP-*` | §5.10 Workspace | `PRD-WSP-*` | Extended |
| `PRD-v2-APR-*` | §5.11 Approvals | `PRD-APR-*` | Extended |
| `PRD-v2-AUD-*` | §5.12 Audit & Cost | `PRD-AUD-*`, `PRD-CST-*` | Extended |
| `PRD-v2-SEO-*` | §5.13 SEO Module | — | New |
| `PRD-v2-VWB-*` | §5.14 Visual Workflow Builder | — | New |
| `PRD-v2-DAR-*` | §5.15 Dynamic Agent Roles | — | New |
| `PRD-v2-VCE-*` | §5.16 Voice / Talk Mode | — | New |
| `PRD-v2-IMP-*` | §5.17 Import / Export | — | New |
| `PRD-v2-DR-*` | §5.18 Disaster Recovery | — | New |

---

## Appendix B: Glossary

| Term | Definition |
|---|---|
| **Agent** | A configured identity with capabilities, instructions, and permissions that can execute tasks |
| **Adapter** | A provider-specific integration that maps Agent OS concepts to an external agent runtime or model API |
| **Artifact** | A versioned output (file, document, media) linked to a run with provenance metadata |
| **DAG** | Directed Acyclic Graph; a workflow where steps have dependencies and no cycles |
| **Mission Control** | The primary operational dashboard showing system status, active work, and KPIs |
| **Run** | A single execution instance of a task with durable state and evidence |
| **Skill** | A reusable workflow template with predefined DAG, agent assignments, and parameters |
| **Two-Lane Verifier** | A quality gate combining deterministic checks and LLM-based review |
| **Workspace** | The primary isolation boundary for projects, members, data, and policy |
| **SERP** | Search Engine Results Page; the visible results for a given keyword query |
| **Content Brief** | A structured document outlining content requirements based on competitor analysis |
| **Workflow Canvas** | The visual DAG builder surface where nodes and edges are arranged |
| **Agent Role** | A defined persona with system prompt, skills, and visual identity that can be assigned to any agent |
| **Approval Gate** | A workflow node that pauses execution until a human reviewer makes a decision |
| **Voice Session** | A continuous voice interaction period with STT, TTS, and transcript history |
| **Voice Profile** | Per-agent TTS configuration: voice ID, pitch, speed, provider preference |
| **Import Job** | An asynchronous background task that transforms external data into Agent OS entities |
| **Backup Job** | An asynchronous task that creates a compressed, encrypted snapshot of workspace data |
| **Restore Job** | An asynchronous task that validates and applies a backup snapshot to the workspace |
| **Git Sync Config** | Per-workspace Git repository settings for automatic Notebook versioning |

---

*End of Document — Agent OS v2 Goldie Edition Product Requirements Document*
