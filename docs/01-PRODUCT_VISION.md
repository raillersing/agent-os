---
document_id: VSN-002
title: Agent OS v2 Goldie Edition Product Vision
version: 2.0.0
status: draft
owner: product-owner
approvers:
  - product-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents: [VSN-001, SCP-001, PRD-001]
related_adrs: []
---

# Agent OS v2 — Goldie Edition: Product Vision

> **Document:** `01-PRODUCT_VISION.md`
> **Version:** 2.0.0
> **Status:** Draft
> **Date:** 2026-08-11
> **Classification:** Internal
> **Source of Truth:** True (for v2 Goldie Edition product direction)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Vision Statement](#2-vision-statement)
3. [The Problem](#3-the-problem)
4. [The Opportunity](#4-the-opportunity)
5. [Value Proposition](#5-value-proposition)
6. [Target Personas](#6-target-personas)
7. [Competitive Analysis](#7-competitive-analysis)
8. [7-Layer Blueprint](#8-7-layer-blueprint)
9. [Goldie Edition Differentiators](#9-goldie-edition-differentiators)
10. [Success Metrics](#10-success-metrics)
11. [Explicit Non-Goals](#11-explicit-non-goals)
12. [Risks & Mitigations](#12-risks--mitigations)

---

## 1. Executive Summary

**Agent OS v2 — Goldie Edition** is a local-first, self-hosted, white-label control plane that coordinates multiple AI agents through a unified Mission Control dashboard. Inspired by Julian Goldie's "Agentic OS" concept, it replaces fragmented AI workflows — scattered across ChatGPT, Claude Code, GitHub Copilot, Midjourney, and a dozen browser tabs — with a single, durable workspace where humans remain in control.

The platform is **Bring Your Own Keys (BYOK)**, **provider-agnostic**, and **workspace-centered**. It does not replace your operating system, your ERP, or your judgment. It makes AI work *durable, governable, and observable* at the workspace level while preserving a clean upgrade path from solo local use to team production deployment.

The Goldie Edition introduces:
- **Named agent personas** (Crystal, Alex, Elvis, Joe) alongside model-native adapters (Claude, Hermes, OpenClaw, Kimi, Grok)
- **Mission Control** — a live DAG node-graph showing agent status, heartbeat, and latency
- **Mission Board** — a Kanban-style drag-drop board for agent team coordination
- **Studio** — image, video, and voice generation with 12 output formats
- **Notebook (KB)** — self-hosted markdown knowledge base with wiki-links, backlinks, and semantic search
- **Two-Lane Verifier** — deterministic + LLM quality gates before any artifact is accepted
- **BYOK Model Gateway** — intelligent routing to cheapest/best provider with automatic fallback chains

The tech stack is deliberate and modern: **Next.js 15 + React 19 + Tailwind CSS v4** on the frontend; **FastAPI + SQLAlchemy 2.0 + Alembic** on the backend; **SQLite/PostgreSQL + pgvector** for persistence; **Redis** for cache and queue; **Docker Compose** for local deployment.

---

## 2. Vision Statement

> *Enable individuals and teams to delegate bounded, high-value work across replaceable AI agents and providers — without surrendering control, provenance, operational visibility, or the ability to say "no."*

Agent OS v2 makes AI-assisted work as governable as code deployment:
- Every run is durable, recoverable, and attributable
- Every consequential action pauses for human approval
- Every artifact carries provenance: who made it, with what model, under what policy
- Every dollar of spend is traceable to workspace, task, and run
- Every agent is replaceable — the platform outlives any provider

---

## 3. The Problem

Today's AI-assisted work is fragmented, opaque, and fragile:

| Pain Point | Current Reality | Consequence |
|---|---|---|
| **Context fragmentation** | Users juggle ChatGPT, Claude, Copilot, Midjourney, terminals, and spreadsheets | Context is rebuilt every session; prior outputs are lost |
| **State loss** | Agent loops die when the browser tab closes or the process stops | Hours of work evaporate; retries duplicate side effects |
| **Provider lock-in** | Workflows embed hard-coded model names and provider-specific prompts | Switching providers requires rewriting everything |
| **Permission confusion** | Tools are "connected" via MCP but never truly authorized | Agents act with implicit, excessive authority |
| **Cost blindness** | Token spend is invisible until the monthly bill arrives | No attribution, no budgets, no accountability |
| **Unverified artifacts** | Generated images, code, and documents are accepted without review | Low-quality or incorrect outputs enter production silently |
| **Memory contamination** | Unverified agent claims are stored alongside authoritative knowledge | Decisions are made on hallucinated "facts" |
| **Dashboard fiction** | Attractive UIs present mock, stale, or disconnected data as truth | Users act on fiction |

The root cause is the absence of a **coherent control plane** for durable, permissioned, observable AI work. Agent OS v2 fills that gap.

---

## 4. The Opportunity

The market is crowded with chat interfaces and coding agents, but empty where it matters most:

1. **No product** treats multiple agents as first-class citizens in a unified workspace
2. **No product** enforces durable execution with human-in-the-loop approvals as a core primitive
3. **No product** combines provider-agnostic routing, artifact provenance, and cost attribution in one self-hosted package
4. **No product** offers a local-first, white-label, BYOK model with a clean production upgrade path

Agent OS v2 targets the gap between "AI toys" and "enterprise AI platforms" — a **prosumer/team control plane** that is powerful enough for production workflows, simple enough for solo operators, and transparent enough for auditors.

---

## 5. Value Proposition

### For Individual Operators (Solo Builders, Consultants, Creators)
- **Continuity**: Stop and resume work across sessions without losing context
- **Control**: Define exactly what each agent may do, for how long, and at what cost
- **Visibility**: See real-time status, heartbeat, latency, and spend for every agent
- **Portability**: Switch from Claude to Kimi to Grok without rewriting workflows
- **Studio**: Generate images, videos, and voice from one interface with 12 format options

### For Product Teams (Startups, Agencies, Dev Teams)
- **Governance**: Consistent policy, approval, and audit across all AI workflows
- **Collaboration**: Shared workspaces, Kanban boards, and artifact galleries
- **Cost Control**: Workspace and run-level budgets with automatic enforcement
- **Quality**: Two-Lane Verifier ensures no artifact ships without review
- **White-Label**: Self-host, rebrand, and control your data

### For Organizations (Enterprise, Regulated Industries)
- **Auditability**: Reconstruct any decision, run, approval, or artifact from immutable events
- **Isolation**: Workspace-scoped data, memory, and artifacts with enforced boundaries
- **Compliance**: Human approval for consequential actions; least-privilege tool access
- **Provider Diversity**: Route to cheapest/best provider; automatic fallback prevents single-point-of-failure

---

## 6. Target Personas

### 6.1 Crystal — The Orchestrator Agent
> *"I see the whole system. I route tasks, monitor health, and escalate when humans are needed."*

Crystal is the default orchestrator agent. She does not execute tasks herself; she coordinates other agents, monitors the DAG, enforces policies, and surfaces exceptions to human operators. She is the voice of Mission Control.

### 6.2 Alex — The Writer Agent
> *"I draft, edit, and refine. From blog posts to API docs, I produce clean, attributed text."*

Alex specializes in long-form text generation, content pipelines, and documentation workflows. He understands SEO, tone consistency, and brand voice. He writes; humans approve.

### 6.3 Elvis — The Media Agent
> *"I generate, transform, and curate visual and audio content. 12 formats, one Studio."*

Elvis powers the Studio module: images, videos, speech synthesis, and audio transcription. He manages media pipelines, format conversions, and asset galleries. He is the creative engine.

### 6.4 Joe — The Reviewer Agent
> *"I verify, validate, and flag. Nothing ships without passing my gates."*

Joe is the Two-Lane Verifier: he runs deterministic checks (lint, schema, policy) and LLM-based quality reviews on every artifact. He is the safety net between generation and acceptance.

### 6.5 Human Personas

| ID | Persona | Role | Primary Need | Pain Point |
|---|---|---|---|---|
| `PER-001` | **Builder-Operator** | Solo developer, consultant, creator | Organize and resume AI-assisted project work | Rebuilding context every session |
| `PER-002` | **Product / Workspace Owner** | Team lead, agency owner | Delegate goals and review outcomes, cost, and evidence | No visibility into what agents actually did |
| `PER-003` | **Technical Operator** | DevOps, platform admin | Configure agents, models, tools, and execution | Provider-specific configs leak into workflows |
| `PER-004` | **Reviewer / Approver** | QA, legal, senior engineer | Review consequential proposed actions | No structured approval pipeline |
| `PER-005` | **Auditor / Assurance** | Compliance, security | Reconstruct decisions, execution, and evidence | Audit trails are fragmented or missing |
| `PER-006` | **Contributor / Consumer** | Team member, stakeholder | Reuse knowledge and artifacts | Can't find or trust prior outputs |

---

## 7. Competitive Analysis

| Competitor | Strengths | Weaknesses | Agent OS v2 Advantage |
|---|---|---|---|
| **ChatGPT / Claude** | Best-in-class models; easy UX | Single-provider; no workspace governance; no artifact provenance; stateless threads | Multi-provider; durable state; approvals; cost attribution |
| **GitHub Copilot** | Deep IDE integration; code focus | Narrow scope; no agent orchestration; no artifact governance | General-purpose agents; Mission Control; workspace isolation |
| **AutoGPT / BabyAGI** | Autonomous loops; viral appeal | Unreliable; unsafe; no approval gates; no provenance | Human-in-the-loop; bounded autonomy; durable recovery |
| **LangChain / LlamaIndex** | Powerful frameworks; extensible | Requires engineering assembly; no UI; no governance out-of-box | Complete product; dark-theme UI; BYOK deployment |
| **Vercel AI SDK** | Great streaming; React components | Framework, not product; no persistence; no multi-agent | Full-stack product with durable execution |
| **Dify / Flowise** | Visual workflow builders; open source | Limited governance; weak approval model; no Studio | Two-Lane Verifier; Kanban board; media Studio |
| **Julian Goldie's "Agentic OS" (Concept)** | Inspiring vision; named agents; Mission Control | Not a shipping product; no technical detail | Real implementation of the vision with engineering rigor |

**Key Differentiator:** Agent OS v2 is the only local-first, self-hosted, white-label product that combines **multi-agent orchestration**, **durable execution with recovery**, **human-in-the-loop approvals**, **artifact provenance**, **cost attribution**, and **media Studio** in one coherent platform.

---

## 8. 7-Layer Blueprint

Agent OS v2 is conceptualized as seven interconnected layers. Each layer is replaceable behind stable contracts.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 1: EXPERIENCE PLANE                                                   │
│  • Mission Control (live DAG, KPI cards, status glyphs)                   │
│  • Mission Board (Kanban drag-drop for agent teams)                         │
│  • Chat (SSE streaming, sessions, artifacts, thinking indicators)           │
│  • Studio (Images, Videos, Speech — 12 formats)                            │
│  • Notebook (Markdown KB, wiki-links, backlinks, semantic search)          │
│  • Workspace Gallery (artifacts with metadata, export, sharing)           │
│  • Command Palette (⌘K global search and action)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: CONTROL PLANE                                                      │
│  • Identity & Access Management (users, roles, sessions)                  │
│  • Policy Engine (workspace policies, tool scopes, data classification)    │
│  • Approval Orchestrator (exact-action approvals, escalation, revocation)  │
│  • Budget & Cost Governance (workspace/run budgets, thresholds)           │
│  • Audit & Evidence (immutable events, execution receipts)                  │
│  • Routing & Fallback (BYOK gateway, provider selection, fallback chains)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: ORCHESTRATION PLANE                                                │
│  • Task Engine (DAG definition, state machine, preflight checks)           │
│  • Run Manager (durable runs, steps, checkpoints, resumption)               │
│  • Agent Registry (named agents, adapters, capabilities, health)          │
│  • Workflow Engine (templated DAGs: Daily Digest, Content Pipeline, SEO)   │
│  • Scheduler (cron, event-triggered, manual)                                │
│  • Two-Lane Verifier (deterministic + LLM quality gates)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 4: EXECUTION PLANE                                                    │
│  • Hermes Gateway (:8642) — chat, files, terminal, swarm execution         │
│  • Codex Adapter — code generation, diff, review                            │
│  • Model Adapters — Claude, Kimi, Grok, Ollama, OpenRouter                  │
│  • Tool Gateway — scoped tool invocation with least-privilege enforcement  │
│  • Sandboxed Execution — isolated filesystem, network, process limits       │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 5: DATA PLANE                                                         │
│  • Workspace Data — tasks, runs, approvals, artifacts (SQLite/PostgreSQL) │
│  • Memory & Knowledge — facts, embeddings, semantic retrieval (pgvector)   │
│  • Notebook — markdown pages, wiki-links, backlinks, full-text search     │
│  • Artifact Store — versioned outputs with integrity metadata             │
│  • Cache & Queue — Redis for sessions, jobs, streaming buffers            │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 6: INTEGRATION PLANE                                                  │
│  • Provider Adapters — Anthropic, Moonshot, XAI, Ollama, OpenRouter         │
│  • MCP Servers — Model Context Protocol for tool discovery                  │
│  • ERP/CRM Connectors — read-only business data (post-MVP)                │
│  • Git Integrations — commit, PR, review workflows (approval-gated)        │
│  • Storage Backends — local filesystem, S3-compatible, NAS                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 7: FOUNDATION PLANE                                                   │
│  • Deployment — Docker Compose, local-first, production upgrade path          │
│  • Observability — structured logs, traces, metrics, health endpoints        │
│  • Security — authn/authz, secret management, encryption at rest/transit   │
│  • Backup & Recovery — documented procedures, integrity verification       │
│  • Accessibility — WCAG 2.2 AA, keyboard navigation, screen reader         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Layer Interaction Principles

1. **The Experience Plane never talks directly to the Execution Plane.** All communication flows through the Control Plane (FastAPI) and Orchestration Plane.
2. **The Orchestration Plane never stores secrets.** Secrets live in the Foundation Plane's secret manager.
3. **The Data Plane enforces workspace isolation at every layer.** No cross-workspace leakage is possible by design.
4. **The Execution Plane is replaceable.** Swap Hermes for a new agent runtime without touching the UI.
5. **The Integration Plane is adapter-driven.** New providers and tools are added via versioned adapters, not core changes.

---

## 9. Goldie Edition Differentiators

### 9.1 Named Agents with Personas
Unlike generic "Agent 1" and "Agent 2," Agent OS v2 ships with four named personas — Crystal, Alex, Elvis, Joe — each with distinct capabilities, color identities, and specialization. Users can also register model-native agents (Claude, Hermes, OpenClaw, Kimi, Grok) with their own color-coded circular avatars.

| Agent | Color | Role | Model |
|---|---|---|---|
| Crystal | `#8B5CF6` (Violet) | Orchestrator | Routing-optimized |
| Alex | `#3B82F6` (Blue) | Writer | Claude / Kimi |
| Elvis | `#EC4899` (Pink) | Media | Image/video models |
| Joe | `#22C55E` (Green) | Reviewer | Lightweight verifier |
| Claude | `#F97316` (Orange) | General | Anthropic Claude |
| Hermes | `#3B82F6` (Blue) | Execution | Hermes Gateway |
| OpenClaw | `#EC4899` (Pink) | Coding | GitHub Copilot-style |
| Kimi | `#EF4444` (Red) | Long-context | Moonshot Kimi |
| Grok | `#F59E0B` (Amber) | Real-time | XAI Grok |

### 9.2 Live DAG Mission Control
The home screen displays a **live Directed Acyclic Graph (DAG)** where each node represents an agent, task, or run. Nodes pulse when active, change color by status (green=online, yellow=ready, red=offline, blue=running), and show real-time latency and heartbeat. This is not a static dashboard — it is a live operational picture.

### 9.3 Mission Board (Kanban)
Agent teams are coordinated via a **drag-drop Kanban board** with columns: Backlog → Ready → Running → Review → Done. Each card represents a task assigned to an agent or a swarm. Cards show agent avatar, status dot, cost estimate, and artifact count.

### 9.4 Studio — 12-Format Media Generation
The Studio module supports:
- **Images**: PNG, JPG, WebP, SVG (count display per format)
- **Videos**: MP4, WebM, GIF (count display per format)
- **Speech**: WAV, MP3, OGG, FLAC
- **Transform**: Resize, crop, filter, transcribe, translate

All outputs are artifacts with full provenance.

### 9.5 Notebook (KB) — Self-Hosted Knowledge Base
A markdown-native knowledge base with:
- Wiki-links: `[[Page Name]]` auto-creates bidirectional links
- Backlinks: Every page shows which pages link to it
- Semantic search: pgvector-powered similarity search across notes
- Full-text search: SQLite/PostgreSQL FTS
- Version history: Every edit is a diff

### 9.6 Two-Lane Verifier
Before any artifact is accepted into the Workspace Gallery, it must pass:
- **Deterministic Lane**: Schema validation, lint, policy check, regex guards, checksum verification
- **LLM Lane**: Quality review, factual consistency check, tone evaluation, safety review

Failures are surfaced with specific lane, rule, and confidence.

### 9.7 BYOK Model Gateway
The routing gateway intelligently selects providers based on:
- **Capability matching**: Does the model support the required task type?
- **Cost optimization**: Route to cheapest qualified provider
- **Latency preference**: Route to lowest-latency provider for real-time tasks
- **Quality preference**: Route to highest-quality provider for critical tasks
- **Fallback chain**: If provider A fails, automatically try B, then C, with transparent logging

---

## 10. Success Metrics

| Category | Metric | Target | Measurement |
|---|---|---|---|
| **Durability** | Persisted runs retaining terminal state | ≥99% | Integration tests + pilot telemetry |
| **Governance** | Approval-required actions blocked without approval | 100% | Policy conformance suite |
| **Recovery** | Resumable interruption scenarios without duplicate effects | ≥95% | Fault-injection suite |
| **Isolation** | Cross-workspace negative-access tests | 100% pass | Automated auth suite |
| **Quality** | Artifacts passing Two-Lane Verifier on first submission | ≥80% | Verifier telemetry |
| **Cost** | Billable usage attributed to workspace/task/run | ≥95% | Provider reconciliation |
| **Portability** | Adapter conformance tests (all registered adapters) | 100% pass | Versioned conformance suite |
| **UX** | Defined journey completion rate | ≥80% | Moderated usability tests |
| **Accessibility** | WCAG 2.2 AA compliance for Must journeys | 0 critical blockers | Auto + manual review |
| **Performance** | Mission Control initial load | <2s | Lighthouse / custom timing |
| **Operations** | Local pilot restore from backup | <4 hours | Documented recovery exercise |
| **Documentation** | Requirements linked to architecture/tests/evidence | 100% | RTM validation |

---

## 11. Explicit Non-Goals

The following are **explicitly excluded** from Agent OS v2 Goldie Edition:

1. **Replace operating systems** — Agent OS is an application, not an OS kernel
2. **Build or train foundation models** — We route to models; we do not build them
3. **Unrestricted autonomous agents** — All autonomy is bounded by policy, time, cost, and approval
4. **Production financial posting** — Read-only business analytics at most; no ledger writes
5. **Autonomous merge/deploy** — Git actions are approval-gated; no silent production changes
6. **Multi-agent swarms** — Single-agent reliability first; swarms are post-v2
7. **Self-modifying skills** — Skills are versioned templates; no runtime mutation
8. **Predictive profit automation** — No AI-generated financial decisions
9. **Public multi-tenant SaaS** — Local-first; team mode is self-hosted
10. **Perfect memory** — Memory is governed, scoped, and source-labeled; not guaranteed complete
11. **MCP connectivity = authorization** — Connected tools require explicit policy grants
12. **Mock data in production views** — Every metric in Mission Control is backed by real persisted state

---

## 12. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| **Scope expansion** | MVP becomes unfinishable | High | Enforce Must/Should/Could/Won't-MVP priority model; weekly scope review |
| **Provider API changes** | Adapters break without warning | Medium | Adapter contract tests run hourly; semantic versioning; fallback chains active |
| **Dark theme accessibility** | Color-only status indicators fail WCAG | Medium | Every status has icon + text + color; screen-reader announcements |
| **Complexity of Two-Lane Verifier** | Verifier becomes bottleneck | Medium | Start with 5 deterministic rules + 1 LLM review; expand based on data |
| **Studio format support** | 12 formats exceed initial capacity | Medium | Ship 6 formats MVP; add remaining 6 in v2.1 |
| **Notebook semantic search quality** | Embeddings produce irrelevant results | Medium | Hybrid search (semantic + FTS); user feedback loop; relevance scoring |
| **Local deployment fragility** | Users can't install or recover | Medium | Docker Compose one-liner; documented backup; health diagnostics dashboard |
| **Approval fatigue** | Users bypass governance to move faster | Medium | Risk-based matrix; bulk approvals; smart defaults; clear UX |
| **Cost attribution gaps** | Provider doesn't report usage per call | Low | Graceful degradation; estimate models; manual reconciliation path |
| **Memory contamination** | Unverified claims pollute KB | Medium | Source labeling; confidence scores; human review gates; correction workflows |

---

## Appendix A: Related Documents

| Document | Relationship |
|---|---|
| `02-PRD.md` | Detailed product requirements, user stories, and acceptance criteria |
| `03-DESIGN_SYSTEM.md` | Complete dark-theme design system with Tailwind v4 tokens |
| `04-ARCHITECTURE.md` | C4 diagrams, deployment architecture, data flows |
| `05-DATA_MODEL.md` | Complete SQL schema for all 21 tables |
| `VSN-001` | Approved baseline product vision and charter (v1) |
| `PRD-001` | Controlled product requirements document (v1) |
| `SRS-001` | Functional requirements specification |
| `SAD-001` | System architecture description |
| `SEC-001` / `THR-001` | Security architecture and threat model |
| `AUT-001` | Autonomy and approval matrix |

---

*End of Document — Agent OS v2 Goldie Edition Product Vision*
