---
document_id: ADR-001
title: Technology Stack Selection
version: 1.0.0
status: approved
owner: architecture-owner
approvers:
  - architecture-owner
  - product-owner
created: 2026-07-20
last_reviewed: 2026-07-20
approval_date: 2026-07-20
classification: internal
source_of_truth: true
related_documents:
  - SAD-001
  - DEP-001
  - DEV-001
related_adrs: []
supersedes: []
---

# ADR-001 — Technology Stack Selection

## Status

**Approved** — 2026-07-20

## Context

Agent OS requires a technology stack that supports:

- Multi-agent orchestration with durable state
- Real-time communication between agents and users
- Scalable memory and knowledge management
- Secure sandboxed execution
- Professional development workflow

The stack must be vendor-neutral, production-ready, and aligned with the architecture described in SAD-001.

## Decision

We will use the following technology stack:

### Backend

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| **Runtime** | Python | 3.12+ | Excellent AI/ML ecosystem, async support |
| **API Framework** | FastAPI | 0.110+ | High performance, async, auto-docs |
| **ORM** | SQLAlchemy | 2.0+ | Industry standard, async support |
| **Migrations** | Alembic | 1.13+ | Mature, works with SQLAlchemy |
| **Validation** | Pydantic | 2.0+ | Data validation, settings management |
| **Task Queue** | Celery + Redis | - | Background tasks, scheduled jobs |

### Frontend

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| **Framework** | Next.js | 14+ | React SSR, excellent DX |
| **UI Library** | React | 18+ | Component ecosystem |
| **Styling** | Tailwind CSS | 3+ | Utility-first, rapid development |
| **State** | Zustand | 4+ | Simple, lightweight state management |

### Data Layer

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| **Primary DB** | PostgreSQL | 16+ | ACID, JSONB, mature |
| **Cache** | Redis | 7+ | Sessions, queues, pub/sub |
| **Vector DB** | ChromaDB | 0.4+ | Local, Python-native |
| **File Storage** | Local + S3 | - | Artifacts, documents |

### Infrastructure

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| **Containerization** | Docker | 24+ | Standard, reproducible |
| **Orchestration** | Docker Compose | 2.24+ | Local development |
| **CI/CD** | GitHub Actions | - | Native GitHub integration |
| **Monitoring** | Prometheus + Grafana | - | Industry standard |

### AI/Agent Layer

| Component | Technology | Version | Justification |
|-----------|------------|---------|---------------|
| **LLM Provider** | Claude API | - | Primary thinking engine |
| **Agent Framework** | Custom Python | - | Agent OS native |
| **MCP** | Model Context Protocol | - | Tool integration standard |
| **Memory** | ChromaDB + PostgreSQL | - | Semantic + structured |

## Alternatives Considered

### Backend Framework

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| **Django** | Mature, batteries-included | Heavier, slower for APIs | Rejected |
| **Flask** | Lightweight, flexible | Less async, more boilerplate | Rejected |
| **FastAPI** | Async, fast, auto-docs | Younger ecosystem | **Selected** |

### Frontend Framework

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| **Vue.js** | Simple, gentle learning curve | Smaller ecosystem | Rejected |
| **Svelte** | Fast, compiled | Smaller ecosystem | Rejected |
| **Next.js** | React ecosystem, SSR, DX | Heavier than alternatives | **Selected** |

### Database

| Alternative | Pros | Cons | Decision |
|-------------|------|------|----------|
| **MySQL** | Popular, mature | Less features than PostgreSQL | Rejected |
| **MongoDB** | Flexible schema | No ACID, complex queries | Rejected |
| **PostgreSQL** | Features, ACID, JSONB | Slightly more complex | **Selected** |

## Consequences

### Positive

1. **Python ecosystem** — Excellent AI/ML libraries, Claude API support
2. **FastAPI performance** — Async support for concurrent agent operations
3. **PostgreSQL reliability** — ACID compliance for durable state
4. **Next.js DX** — Fast development, good TypeScript support
5. **Docker consistency** — Same environment dev/staging/production

### Negative

1. **Python GIL** — May need multiprocessing for CPU-bound tasks
2. **Next.js complexity** — Heavier than simple SPA frameworks
3. **PostgreSQL operational** — More complex than SQLite for quick starts

### Mitigations

1. Use Celery for CPU-bound tasks, async for I/O
2. Start with Next.js App Router for simplicity
3. Provide Docker Compose for zero-config PostgreSQL

## Compliance

This decision aligns with:

- **DOC-000** — Vendor neutrality principle
- **SAD-001** — System architecture description
- **DEP-001** — Deployment architecture
- **DEV-001** — Development guide

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Julian Goldie SEO Agent OS — Similar architecture with Claude + Hermes + Obsidian
