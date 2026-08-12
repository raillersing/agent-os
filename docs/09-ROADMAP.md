---
document_id: REL-002
title: Agent OS v2 Goldie Edition Roadmap and Release Plan
version: 2.0.0
status: draft
owner: product-owner
approvers:
  - product-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents: [VSN-002, PRD-002, QAG-001]
related_adrs: []
---

# Agent OS v2 — Roadmap & Release Plan

## Goldie Edition

**Version:** 2.0.0-MVP
**Date:** 2026-08-11

---

## 1. Release Strategy

Agent OS follows **Semantic Versioning** with release trains:

```
v2.0.0-MVP      →  v2.1.0  →  v2.2.0  →  v2.3.0  →  v2.4.0  →  v2.5.0  →  v2.6.0  →  v3.0.0
  (MVP)          (Studio)   (Orchestrator)  (Polish)   (SEO)    (Workflows) (Agentic)  (Commercial)
```

| Version | Codename | Focus | Target |
|---------|----------|-------|--------|
| `v2.0.0-MVP` | Goldie | Core chat, auth, notebook, agents registry | Day 0 |
| `v2.1.0` | Studio | Media generation, terminal, file manager | Day 14 |
| `v2.2.0` | Orchestrator | Live DAG, Kanban, workflows, multi-agent | Day 30 |
| `v2.3.0` | Polish | Voice, Import/Export, Disaster Recovery, desktop app, PWA, white-label, governance | Day 60 |
| `v2.4.0` | SEO | SERP analysis, rank tracking, competitor watch, content briefs, CMS connectors | Day 75 |
| `v2.5.0` | Workflows | Visual Workflow Builder, conditional branches, loops, approval gates, marketplace | Day 90 |
| `v2.6.0` | Agentic | Dynamic Agent Roles, swarm mode, delegation protocol, reflection loops | Day 105 |
| `v3.0.0` | Commercial | Billing, SaaS multi-tenant, ERP connectors | Day 120+ |

Pre-release tags: `-alpha`, `-beta`, `-rc` (release candidate).
Patch releases (`v2.0.1`) for hotfixes only — no new features.

---

## 2. Phase Breakdown (P0–P10)

### P0: Discovery + Bridge — ~2 hours
**Goal:** Validate the FastAPI ↔ Hermes handshake. Prove the stack works end-to-end.

**Milestones:**
- [ ] FastAPI project scaffold (SQLAlchemy 2.0, asyncpg, Alembic)
- [ ] Hermes client module with provider routing
- [ ] Single `POST /gateway/complete` endpoint returning a Claude response
- [ ] Health check endpoint (`/api/v1/health`) covering DB, Redis, Hermes
- [ ] Log all requests to Hermes with trace IDs

**Success Criteria:**
- `curl` to `/gateway/complete` returns a valid Claude response in < 5s.
- Health check returns `ok` for all subsystems.
- Zero 500 errors on synthetic load (10 req/min for 5 min).

**Dependencies:** None. Entry point.

---

### P1: Foundation — ~3 hours
**Goal:** Next.js 15 + Tailwind v4 + Auth + SQLite. The UI shell and user system.

**Milestones:**
- [ ] Next.js 15 app with App Router, Tailwind CSS v4, dark theme
- [ ] JWT auth (login, refresh, logout, register)
- [ ] SQLite auto-migration on first run
- [ ] Zustand auth store with token refresh logic
- [ ] Sidebar navigation shell (Agents, Chat, Notebook, Settings)
- [ ] Responsive layout (mobile drawer, desktop sidebar)

**Success Criteria:**
- User can register, log in, and refresh token without manual intervention.
- UI renders correctly at 320px (mobile) and 1920px (desktop).
- Theme tokens match Design System (§3-DESIGN_SYSTEM.md).
- Lighthouse accessibility score ≥ 90.

**Dependencies:** P0

---

### P2: Brain + Gateway — ~3 hours
**Goal:** Multi-provider chat with SSE streaming. The core product loop.

**Milestones:**
- [ ] Chat session CRUD (create, list, rename, delete)
- [ ] Message composer with agent selector
- [ ] SSE streaming endpoint for all providers
- [ ] Claude, Kimi, Grok, Ollama provider integrations
- [ ] Message bubble component (Markdown render, code blocks, tool calls)
- [ ] Chat history persistence (SQLite)
- [ ] Rate limiting on gateway proxy

**Success Criteria:**
- Chat with Claude streams text smoothly (< 200ms latency between chunks).
- Switching agents mid-conversation creates a new session cleanly.
- Ollama (local) works without any cloud API key.
- 1000 messages in a session load in < 2s with virtualized list.

**Dependencies:** P0, P1

---

### P3: Self Layer — ~3 hours
**Goal:** Notebook knowledge base + vault template. The memory layer.

**Milestones:**
- [ ] Note CRUD (title, body, tags, backlinks)
- [ ] SQLite FTS5 full-text search
- [ ] Semantic search via `sqlite-vec` (or pgvector in team mode)
- [ ] Backlink auto-discovery (`[[Note Title]]` → link)
- [ ] Vault template: pre-seed notes for new workspaces
- [ ] Note editor: Markdown with live preview
- [ ] Notebook ↔ Chat cross-link (cite notes in chat, save chat to note)

**Success Criteria:**
- Create a note, search for it by keyword, result in < 500ms.
- Semantic search returns semantically related notes (not just keyword match).
- Backlinks panel updates automatically when a new note links in.
- Vault template auto-creates on new workspace registration.

**Dependencies:** P1, P2

---

### P4: Agents Registry — ~3 hours
**Goal:** Named agents with skills, colors, and configuration.

**Milestones:**
- [ ] `agents` table with provider, model, color, status, config JSON
- [ ] Agent status badge (online, ready, offline, running)
- [ ] Skills system: register, assign, version skills per agent
- [ ] Agent card component (avatar, color, status, last seen)
- [ ] Agent settings panel (temperature, max tokens, system prompt)
- [ ] Default agents seeded: Claude, Hermes, OpenClaw, Kimi, Grok, Gemini, Antigravity, Codex, Free Claude
- [ ] Agent status polling or WebSocket push

**Success Criteria:**
- All 9 default agents appear with correct brand colors.
- Status transitions accurately reflect Hermes reachability.
- Editing an agent’s system prompt persists and affects next chat session.
- Skills list is versioned and shown in agent detail view.

**Dependencies:** P0, P1, P2

---

### P5: Mission Control — ~3 hours
**Goal:** Live DAG + Kanban. Visual task orchestration.

**Milestones:**
- [ ] Task DAG model (task_nodes, edges, parallel/sequential types)
- [ ] Task creation with agent assignment and goal text
- [ ] DAG live viewer: nodes, edges, status colors, progress bar
- [ ] WebSocket stream for DAG node updates
- [ ] Kanban board: columns (To Do, In Progress, Review, Done)
- [ ] Drag-and-drop card reordering within and across columns
- [ ] Task ↔ Kanban card sync (creating a task spawns a card)
- [ ] DAG drill-down from card (click card → see node tree)

**Success Criteria:**
- Create a 3-node DAG; all nodes execute in correct dependency order.
- WebSocket pushes node status updates within 1s of backend change.
- Kanban drag-and-drop persists column + position to backend.
- 50 cards on board render at 60fps.

**Dependencies:** P2, P4

---

### P6: Execution — ~3 hours
**Goal:** Files, Terminal, Studio. The "do things" layer.

**Milestones:**
- [ ] Files API via Hermes proxy (list, read, write, delete)
- [ ] File tree browser in UI (expandable, breadcrumb, MIME icons)
- [ ] Terminal: WebSocket session with xterm.js
- [ ] Terminal resize, input, ANSI color support
- [ ] Studio: generate image via DALL-E / Stable Diffusion API
- [ ] Studio: generate audio (TTS) via ElevenLabs / local Piper
- [ ] Studio: job queue, progress tracking, result gallery
- [ ] Artifacts table (link generated media to tasks, notes, chat)

**Success Criteria:**
- Write a file via UI; Hermes proxy writes to disk; read back identical.
- Terminal runs `python -c "print('hello')"` and returns output in < 2s.
- Studio image generation completes in < 30s and appears in gallery.
- Artifacts are searchable from Notebook and linked in Chat.

**Dependencies:** P0, P1, P2

---

### P7: Workflows — ~3 hours
**Goal:** 3 ready-to-use workflows. Automation beyond one-off tasks.

**Milestones:**
- [ ] Workflow template engine (YAML/JSON definition, parameterized)
- [ ] Workflow runner: trigger → DAG generation → execution → result
- [ ] Workflow 1: "Code Review" — clone repo → analyze → post PR comments
- [ ] Workflow 2: "Content Pipeline" — research → draft → edit → publish
- [ ] Workflow 3: "Data Sync" — connect API → transform → load to DB
- [ ] Workflow status page (triggered, running, completed, failed)
- [ ] Workflow editor (UI for creating custom templates)

**Success Criteria:**
- All 3 workflows run end-to-end without manual intervention.
- Workflow outputs are saved as artifacts and linked in Notebook.
- Custom workflow template can be created in UI and runs successfully.
- Failed workflow step shows retry button and error log.

**Dependencies:** P5, P6

---

### P8: Workspace — ~2 hours
**Goal:** Asset gallery and workspace management.

**Milestones:**
- [ ] Asset gallery: grid view of all artifacts, filter by type, date, agent
- [ ] Asset preview: image lightbox, audio player, code syntax highlight
- [ ] Workspace settings panel (name, slug, branding toggle)
- [ ] Multi-workspace switcher (top nav dropdown)
- [ ] Workspace isolation: data scoped by workspace ID
- [ ] Invite member by email (role: admin, member, viewer)
- [ ] Member list with role badges and last active

**Success Criteria:**
- Upload 100 images; gallery renders thumbnails in < 3s (lazy load).
- Switching workspace refreshes all data scoped to new workspace.
- Member invitation sends email and creates pending membership.
- Workspace branding (logo, color) applies to login page and dashboard.

**Dependencies:** P1, P6

---

### P9: Governance — ~2 hours
**Goal:** Verifier, cost tracking, audit. Trust and control.

**Milestones:**
- [ ] Verifier: run assertions on agent outputs (schema, regex, LLM-judge)
- [ ] Verifier results page: pass/fail, confidence, human review flag
- [ ] Human review queue: flagged outputs await approval
- [ ] Approval system: approve/reject with comment, audit trail
- [ ] Cost tracking: per-request spend, per-agent spend, per-user spend
- [ ] Budget alerts: threshold email/Slack when 80% of monthly limit
- [ ] Audit events table: all CRUD, auth, gateway calls
- [ ] Audit export: CSV/JSON download

**Success Criteria:**
- Verifier catches a malformed JSON response and flags it for review.
- Cost dashboard shows real-time spend with < 5min delay.
- Budget alert fires when threshold crossed.
- Audit export includes all events for last 30 days in < 10s.

**Dependencies:** P2, P4, P5

---

### P10: Desktop + Polish — ~2 hours
**Goal:** Electron + PWA + white-label. Distribution and finish.

**Milestones:**
- [ ] Electron app wrapper (macOS, Windows, Linux)
- [ ] Auto-updater (Electron + Squirrel / electron-updater)
- [ ] PWA manifest, service worker, offline shell
- [ ] White-label: runtime branding via `/workspace/branding` API
- [ ] Custom CSS injection for enterprise theming
- [ ] Keyboard shortcuts (⌘K command palette, ⌘/ search, ⌘N new chat)
- [ ] Accessibility audit: WCAG 2.1 AA compliance
- [ ] Performance audit: TTI < 3s, LCP < 2.5s on 4G
- [ ] Final docs pass: update all markdown docs to match shipped code

**Success Criteria:**
- Electron app launches and functions identically to web app.
- PWA installs on Chrome/Android and works offline for cached routes.
- White-label rebrand takes < 5 min (API call + reload).
- Lighthouse score ≥ 90 for performance, accessibility, best practices.

**Dependencies:** P1–P9

---

## 3. Dependency Graph

```
P0  Discovery + Bridge
│
├─→ P1  Foundation
│   │
│   ├─→ P2  Brain + Gateway
│   │   │
│   │   ├─→ P3  Self Layer
│   │   │
│   │   ├─→ P4  Agents Registry
│   │   │
│   │   └─→ P6  Execution
│   │       │
│   │       ├─→ P5  Mission Control  ←── P4
│   │       │   │
│   │       │   └─→ P7  Workflows
│   │       │
│   │       └─→ P8  Workspace
│   │
│   └─→ P9  Governance  ←── P2, P4, P5
│
└─→ P10 Desktop + Polish  ←── ALL
```

**Parallel tracks:**
- P2 + P3 + P4 can proceed in parallel after P1.
- P6 can start after P2.
- P8 can start after P1 and P6.
- P9 can start after P2, P4, P5.
- P10 must wait for all preceding phases.

---

## 4. Success Criteria per Phase (Checklist)

| Phase | CI Pass | Tests | Review | Demo | Sign-off |
|-------|---------|-------|--------|------|----------|
| P0 | ✅ | Unit tests for Hermes client | 1 reviewer | CLI demo | Tech lead |
| P1 | ✅ | E2E: register → login → logout | 1 reviewer | UI walkthrough | Product owner |
| P2 | ✅ | E2E: chat SSE with 3 providers | 1 reviewer | Live chat demo | Product owner |
| P3 | ✅ | Unit + E2E: search, backlinks | 1 reviewer | Notebook demo | Product owner |
| P4 | ✅ | Unit: agent status transitions | 1 reviewer | Agent registry demo | Product owner |
| P5 | ✅ | E2E: create DAG, verify order | 1 reviewer | Kanban + DAG demo | Product owner |
| P6 | ✅ | E2E: file CRUD, terminal, studio | 1 reviewer | Execution demo | Product owner |
| P7 | ✅ | E2E: run all 3 workflows | 2 reviewers | Workflow demo | Tech lead + PO |
| P8 | ✅ | E2E: workspace switch, invite | 1 reviewer | Workspace demo | Product owner |
| P9 | ✅ | E2E: verifier, cost, audit | 2 reviewers | Governance demo | Tech lead + PO |
| P10 | ✅ | E2E: Electron, PWA, white-label | 2 reviewers | Distribution demo | Tech lead + PO |

---

## 5. Release Model: MVP → Commercial

### 5.1 MVP (v2.0.0-MVP) — Day 0

**What ships:**
- P0–P6 complete
- Auth, chat (multi-provider), notebook, agents, tasks, DAG, Kanban, files, terminal, studio
- SQLite default, PostgreSQL optional
- Docker Compose single-command deploy

**What is intentionally absent:**
- Workflows (P7) — template system not ready
- Desktop app (P10) — Electron not bundled
- Commercial billing (v3) — no metering, no plans

**Gate:** 2 successful end-to-end demos with no P0 bugs.

### 5.2 Studio (v2.1.0) — Day 14

**What ships:**
- P7: 3 workflows ready
- Studio improvements: batch generation, model picker, history
- Bug fixes from MVP feedback

### 5.3 Orchestrator (v2.2.0) — Day 30

**What ships:**
- Multi-agent swarm (early): delegate sub-tasks to multiple agents
- Workflow marketplace: share/import community templates
- Advanced DAG: conditional branches, loops, retries

### 5.4 Polish (v2.3.0) — Day 60

**What ships:**
- P10: Electron, PWA, white-label
- Voice / Talk Mode: push-to-talk, STT, TTS, voice profiles
- Import / Export: Obsidian, Notion, ChatGPT, Claude, Evernote, OneNote, Markdown
- Disaster Recovery: auto-backup, cloud targets, Git sync, encrypted export, one-click restore
- Accessibility full compliance
- Performance budget enforcement in CI
- Internationalization (i18n) framework ready

### 5.5 SEO (v2.4.0) — Day 75

**What ships:**
- SEO Module: SERP analysis, rank tracking, competitor watch, content briefs
- CMS connectors: WordPress, Shopify, Webflow
- Traffic analytics: GSC + GA4 integration
- White-label SEO reports

### 5.6 Workflows (v2.5.0) — Day 90

**What ships:**
- Visual Workflow Builder: drag-and-drop DAG canvas
- Conditional branches (if/else), loops, approval gates
- Cron and webhook triggers
- Simulation / dry-run mode
- Workflow marketplace (import/export)

### 5.7 Agentic (v2.6.0) — Day 105

**What ships:**
- Dynamic Agent Roles: create, assign, switch, clone
- Agent Role Manager UI with skill templates
- Swarm mode: multi-agent collaboration
- Delegation protocol with structured handoff
- Reflection loops and memory profiles

### 5.8 Commercial (v3.0.0) — Day 120+

**What ships:**
- SaaS multi-tenant architecture
- Billing: Stripe integration, usage-based plans
- Enterprise SSO (SAML, OIDC)
- ERP connectors: Salesforce, HubSpot, NetSuite
- SLA guarantees, support portal

---

## 6. Feature Flags and Toggles

Incomplete features are gated by runtime flags in `app/core/config.py`:

```python
class Settings(BaseSettings):
    ENABLE_WORKFLOWS: bool = False
    ENABLE_STUDIO_TTS: bool = False
    ENABLE_SWARM: bool = False
    ENABLE_COST_TRACKING: bool = False
    ENABLE_ELECTRON: bool = False
    ENABLE_PWA: bool = False
    ENABLE_WHITE_LABEL: bool = False
    ENABLE_SEO: bool = False
    ENABLE_VISUAL_WORKFLOWS: bool = False
    ENABLE_AGENT_ROLES: bool = False
    ENABLE_VOICE: bool = False
    ENABLE_IMPORT_EXPORT: bool = False
    ENABLE_DISASTER_RECOVERY: bool = False
```

**Rules:**
- Flags default to `False` on `main`.
- Feature branch sets flag to `True` for local testing.
- Merge to `main` only when flag can safely default to `False` (no broken UI).
- Remove flag and hard-enable when phase is signed off.
- Document flags in `docs/09-ROADMAP.md` and `.env.example`.

**Frontend gating:**
```tsx
// components/Nav.tsx
import { isFeatureEnabled } from '@/lib/features';

{isFeatureEnabled('workflows') && (
  <NavLink href="/workflows">Workflows</NavLink>
)}
```

---

## 7. Post-MVP Backlog

| Feature | Target | Notes |
|---------|--------|-------|
| Swarm multi-agent | v2.6.0 | Auto-delegate, consensus, retry loops |
| NotebookLM integration | v2.2.0 | Ingest PDFs, generate podcasts, summaries |
| MCP (Model Context Protocol) | v2.5.0 | Universal tool calling standard |
| ERP connectors | v3.0.0 | Salesforce, HubSpot, NetSuite, SAP |
| Voice mode | v2.3.0 | Real-time speech-to-text, text-to-speech |
| Code interpreter | v2.1.0 | Sandbox Python execution, charts, CSV analysis |
| Plugin marketplace | v2.5.0 | Third-party skills, themes, integrations |
| Mobile native app | v3.0.0 | React Native or Capacitor wrapper |
| Federated learning | v3.0.0 | On-device model fine-tuning |
| Compliance suite | v3.0.0 | SOC 2, GDPR, HIPAA audit helpers |

---

## 8. Risk Register

### 8.1 Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| SSE/WebSocket scale issues | Medium | High | Load test with 1000 concurrent streams; fallback to polling |
| PostgreSQL + pgvector performance | Medium | High | Benchmark on target dataset; add indexes; shard if needed |
| Hermes provider outage | High | Medium | Circuit breaker pattern; fallback to next provider; queue retries |
| SQLite concurrency limits | High | Medium | Document "switch to PostgreSQL for team mode"; add warning in UI |
| Next.js 15 + React 19 compat | Low | Medium | Pin exact versions; run RC builds early; monitor ecosystem |

### 8.2 Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Provider pricing changes | Medium | High | Cost tracking P9; budget alerts; multi-provider fallback |
| Competition shipping first | Medium | High | MVP scope locked; no scope creep; ship fast |
| Enterprise sales cycle | High | Medium | Build self-serve SaaS first; enterprise as upsell |
| Open-source licensing confusion | Low | Medium | Clear license (Apache 2.0 / AGPL); CLA if needed |

### 8.3 Operational Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Key person dependency | Medium | High | Document everything (this roadmap); pair programming; bus factor ≥ 2 |
| Deployment complexity | Medium | Medium | Docker Compose one-command; comprehensive docs; install script |
| Security vulnerability | Low | High | Dependabot; SAST in CI; penetration test before v3 |
| Data loss | Low | Critical | Automated backups (P9); point-in-time recovery for PostgreSQL |

---

## 9. Changelog

| Version | Date | Notes |
|---------|------|-------|
| 2.0.0-MVP | 2026-08-11 | Initial roadmap for Goldie Edition |

---

*End of Roadmap & Release Plan*
