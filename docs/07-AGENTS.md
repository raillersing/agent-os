---
document_id: DEV-002
title: Agent OS v2 Agents and Conventions
version: 2.0.0
status: archived
owner: architecture-owner
approvers:
  - architecture-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents: [DEV-001, AGC-001, SAD-002]
related_adrs: []
---

# Agent OS v2 — Agents & Conventions

## Agent OS

**Version:** 2.0.0-MVP
**Date:** 2026-08-11

---

## 1. Project Structure Conventions

### 1.1 Frontend (`frontend/src/`)

```
frontend/src/
├── app/                    # Next.js 15 App Router
│   ├── (auth)/             # Route groups
│   ├── (dashboard)/
│   ├── api/                # Next.js API routes (minimal, prefer FastAPI)
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing / dashboard
│   └── globals.css         # Tailwind v4 imports
├── components/             # React components
│   ├── ui/                 # Primitive components (shadcn/ui style)
│   ├── agents/             # Agent-specific cards, status badges
│   ├── chat/               # Chat window, message bubbles, composer
│   ├── notebook/           # Note editor, backlinks, search
│   ├── board/              # Kanban board, columns, cards
│   ├── studio/             # Media generation UI
│   ├── tasks/              # DAG viewer, task list, node details
│   └── shared/             # Layout, nav, breadcrumbs, modals
├── hooks/                  # Custom React hooks
│   ├── useAuth.ts
│   ├── useSSE.ts
│   ├── useWebSocket.ts
│   └── useWorkspace.ts
├── stores/                 # Zustand stores (one per domain)
│   ├── authStore.ts
│   ├── chatStore.ts
│   ├── taskStore.ts
│   └── notebookStore.ts
├── lib/                    # Utilities, API client, constants
│   ├── api.ts              # Centralized fetch wrapper
│   ├── utils.ts            # cn(), formatters
│   └── providers.ts        # Provider configs
├── types/                  # Shared TypeScript interfaces
│   ├── agent.ts
│   ├── task.ts
│   └── chat.ts
└── styles/                 # Theme tokens, custom utilities
    └── theme.css
```

### 1.2 Backend (`backend/app/`)

```
backend/app/
├── api/
│   ├── deps.py             # FastAPI dependencies (DB, auth, rate limit)
│   ├── errors.py           # RFC 7807 Problem Details helpers
│   └── v1/
│       ├── __init__.py
│       ├── router.py       # Aggregates all sub-routers
│       ├── endpoints/
│       │   ├── auth.py
│       │   ├── agents.py
│       │   ├── tasks.py
│       │   ├── chat.py
│       │   ├── notebook.py
│       │   ├── studio.py
│       │   ├── board.py
│       │   ├── workflows.py
│       │   ├── gateway.py
│       │   ├── verifier.py
│       │   ├── approvals.py
│       │   ├── workspace.py
│       │   ├── audit.py
│       │   ├── cost.py
│       │   ├── files.py
│       │   └── terminal.py
│       └── schemas/
│           ├── __init__.py
│           ├── agent.py
│           ├── task.py
│           └── …           # One Pydantic schema file per domain
├── core/
│   ├── config.py           # Pydantic Settings
│   ├── security.py         # Password hashing, JWT encode/decode
│   ├── events.py           # Event bus abstractions
│   └── logging.py          # Structlog configuration
├── db/
│   ├── base.py             # SQLAlchemy declarative base
│   ├── session.py          # Async session factory
│   └── init.py             # DB init (tables, extensions)
├── models/                 # SQLAlchemy ORM models
│   ├── __init__.py
│   ├── user.py
│   ├── workspace.py
│   ├── agent.py
│   ├── task.py
│   ├── task_node.py
│   ├── chat.py
│   ├── note.py
│   ├── audit.py
│   └── …
├── services/               # Business logic (fat services, thin endpoints)
│   ├── agent_service.py
│   ├── task_service.py
│   ├── chat_service.py
│   ├── notebook_service.py
│   └── gateway_service.py
├── workers/                # Celery tasks
│   ├── __init__.py
│   ├── task_runner.py
│   └── studio_jobs.py
├── tests/
│   ├── conftest.py
│   ├── factories.py        # Test data factories
│   └── …                   # Mirror structure of app/
├── alembic/                # Alembic migrations
│   └── versions/
├── main.py                 # FastAPI app factory
└── celery_app.py           # Celery app factory
```

---

## 2. Coding Standards

### 2.1 TypeScript (Frontend)

| Rule | Value |
|------|-------|
| Strict mode | `strict: true` in `tsconfig.json` |
| No implicit any | Enabled |
| Exact optional property types | Enabled |
| No unchecked indexed access | Enabled |
| Target | `ES2022` |
| Module | `ESNext` with `Bundler` resolution |

**Patterns:**
- Prefer `interface` over `type` for object shapes.
- Use `readonly` arrays and tuples where mutation is not intended.
- Avoid `as` casts; use type guards (`isAgent()`, `isTaskNode()`).
- Nullish coalescing: `value ?? defaultValue` (not `||`).

### 2.2 Python (Backend)

| Rule | Value |
|------|-------|
| Type hints | 100% coverage (`mypy --strict`) |
| Formatting | `ruff format` (replaces Black) |
| Linting | `ruff check` with select rules |
| Import style | `isort` / `ruff` sorted, absolute imports preferred |
| Line length | 88 characters |
| String quotes | Double `""` for strings, single `''` for dict keys optional |
| Async | `async` / `await` everywhere (FastAPI, asyncpg, SQLAlchemy 2.0) |

**Patterns:**
- Use Pydantic v2 for all schemas.
- Use SQLAlchemy 2.0 `mapped_column()`, `relationship()` with types.
- DAO / Repository layer optional; keep queries colocated in services.
- No raw SQL strings; use SQLAlchemy Core expressions.

---

## 3. Naming Conventions

### 3.1 Files

| Layer | Convention | Example |
|-------|-----------|---------|
| Components | PascalCase file + directory | `components/ChatWindow.tsx` |
| Hooks | camelCase, prefix `use` | `hooks/useAuth.ts` |
| Stores | camelCase, suffix `Store` | `stores/authStore.ts` |
| Utils / lib | camelCase or kebab-case | `lib/api.ts`, `lib/error-handler.ts` |
| Styles | kebab-case | `styles/theme.css` |
| Python modules | snake_case | `agent_service.py` |
| Python tests | prefix `test_` | `test_agent_service.py` |

### 3.2 Code Identifiers

| Scope | Convention | Example |
|-------|-----------|---------|
| React components | PascalCase | `ChatMessageBubble` |
| Variables / functions | camelCase | `const activeAgent = …` |
| Constants | UPPER_SNAKE_CASE | `const MAX_RETRIES = 3` |
| Python classes | PascalCase | `class AgentService:` |
| Python functions / vars | snake_case | `def get_agent_by_id(...)` |
| Database tables | snake_case, plural | `agent_runs`, `memory_facts` |
| Database columns | snake_case | `created_at`, `workspace_id` |
| API paths | kebab-case | `/task-nodes/{node_id}` |
| Environment variables | UPPER_SNAKE_CASE | `DATABASE_URL`, `REDIS_HOST` |

---

## 4. State Management

### 4.1 Frontend — Zustand

One store per bounded context:

```ts
// stores/chatStore.ts
import { create } from 'zustand';

interface ChatState {
  sessions: ChatSession[];
  activeSessionId: string | null;
  messages: Record<string, ChatMessage[]>;
  isStreaming: boolean;
  setActiveSession: (id: string) => void;
  appendMessage: (sessionId: string, msg: ChatMessage) => void;
}

export const useChatStore = create<ChatState>((set) => ({
  sessions: [],
  activeSessionId: null,
  messages: {},
  isStreaming: false,
  setActiveSession: (id) => set({ activeSessionId: id }),
  appendMessage: (sid, msg) => set((s) => ({
    messages: { ...s.messages, [sid]: [...(s.messages[sid] || []), msg] },
  })),
}));
```

Rules:
- No store imports in UI components directly; export typed selectors.
- Persist critical stores (auth, workspace) with `zustand/middleware` + `localStorage`.
- Never mutate state outside Zustand actions.

### 4.2 Backend — SQLAlchemy 2.0 + Unit of Work

```python
from sqlalchemy.ext.asyncio import AsyncSession

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, dto: TaskCreate) -> Task:
        task = Task(**dto.model_dump())
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
```

Rules:
- One `AsyncSession` per request (FastAPI dependency).
- Explicit `commit()`; no auto-commit.
- Use `selectinload()` for eager loading to avoid N+1.

---

## 5. API Client Patterns

### 5.1 Centralized Fetch (`lib/api.ts`)

```ts
const api = {
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  async request<T>(path: string, opts: RequestInit = {}): Promise<T> {
    const res = await fetch(`${this.baseURL}${path}`, {
      ...opts,
      headers: {
        'Content-Type': 'application/json',
        ...(opts.headers || {}),
      },
    });
    if (!res.ok) throw await parseProblem(res);
    return res.json();
  },
  get: (path: string) => api.request(path, { method: 'GET' }),
  post: (path: string, body: unknown) => api.request(path, { method: 'POST', body: JSON.stringify(body) }),
  // ...
};
```

### 5.2 Interceptors

- **Request:** Attach `Authorization: Bearer <token>` from authStore.
- **Response:** Parse `application/problem+json` on error.
- **Retry:** Exponential backoff on `502/503/504` (max 3 retries).
- **Cancellation:** AbortController per request; cancel on component unmount.

### 5.3 React Query / SWR (Optional)

For server-state-heavy screens, prefer `@tanstack/react-query` over raw fetch:

```ts
const { data, isLoading } = useQuery({
  queryKey: ['agents', workspaceId],
  queryFn: () => api.get(`/agents?workspace_id=${workspaceId}`),
  staleTime: 30_000,
});
```

---

## 6. Component Patterns

### 6.1 Compound Components

Use composition over inheritance for complex UI:

```tsx
<KanbanBoard>
  <KanbanBoard.Column title="To Do">
    <KanbanBoard.Card task={task1} />
    <KanbanBoard.Card task={task2} />
  </KanbanBoard.Column>
</KanbanBoard>
```

### 6.2 Props Interface

Always define explicit interfaces; avoid `React.FC`:

```tsx
interface AgentCardProps {
  agent: Agent;
  variant?: 'compact' | 'detailed';
  onSelect?: (id: string) => void;
}

export function AgentCard({ agent, variant = 'compact', onSelect }: AgentCardProps) {
  // …
}
```

### 6.3 Server Components by Default

- Use Server Components for data-fetching pages.
- Mark interactivity boundaries with `'use client'` only when needed.
- Pass server-fetched data as props to client components.

---

## 7. Testing Strategy

### 7.1 Backend — pytest

```bash
cd backend
pytest -q --cov=app --cov-report=term-missing
```

Coverage target: **>= 80%** for services, **100%** for critical paths (auth, billing).

Test types:
- **Unit:** Service layer with mocked DB (async SQLAlchemy session).
- **Integration:** API endpoints with `TestClient` against SQLite in-memory.
- **E2E (optional):** Full Docker stack with PostgreSQL + Redis.

Fixture pattern:
```python
@pytest.fixture
def agent_factory(db: AsyncSession):
    async def _make(**kwargs):
        agent = AgentFactory.build(**kwargs)
        db.add(agent)
        await db.commit()
        return agent
    return _make
```

### 7.2 Frontend — Vitest + Testing Library

```bash
cd frontend
vitest run --coverage
```

Coverage target: **>= 70%** for utilities, **>= 60%** for components.

Test types:
- **Unit:** Pure functions, hooks, Zustand stores.
- **Component:** React Testing Library + `@testing-library/user-event`.
- **E2E:** Playwright (separate `e2e/` directory).

Example:
```ts
import { render, screen } from '@testing-library/react';
import { AgentCard } from '@/components/agents/AgentCard';

test('renders agent name and status', () => {
  render(<AgentCard agent={{ name: 'Claude', status: 'online' }} />);
  expect(screen.getByText('Claude')).toBeInTheDocument();
  expect(screen.getByLabelText('Status: online')).toBeInTheDocument();
});
```

---

## 8. Git Workflow

### 8.1 Branch Strategy — Trunk-Based Development

```
main        — production-ready, always deployable
  ↑
feature/*   — short-lived (< 2 days), rebase onto main frequently
hotfix/*    — emergency fixes branched from latest tag
```

Rules:
- No long-lived feature branches. If > 2 days, split or use feature flags.
- Rebase before merge; squash if commit history is messy.
- Merge via **fast-forward** or **merge commit** (team preference); never merge broken code.

### 8.2 Commit Message Format

Follow **Conventional Commits**:

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`

Examples:
```
feat(chat): add SSE streaming for Claude messages
fix(board): prevent card drop on read-only column
docs(api): document rate-limit headers
test(agents): cover agent status transitions
```

---

## 9. Change Control Rules

| Rule | Enforcement |
|------|-------------|
| One branch per feature | Branch name = ticket or descriptive slug |
| No silent requirement changes | Any scope change requires ADR or ticket update |
| Code review required | Minimum 1 approver for all PRs; 2 for auth/billing changes |
| CI must pass | Lint, type-check, tests, build — all green before merge |
| No direct push to `main` | Protected branch with required checks |
| Feature flags for WIP | Gate incomplete UI with `isFeatureEnabled('dag-v2')` |

---

## 10. Documentation Requirements

### 10.1 Architecture Decision Records (ADR)

Any change to:
- Data model (new tables, dropped columns, migration strategy)
- API contracts (breaking changes, new versions)
- Security model (auth mechanism, permission boundaries)
- Infrastructure (new service, container topology)

Template: `docs/adr/NNNN-title.md` with Status (`proposed`, `accepted`, `deprecated`, `superseded`).

### 10.2 Docs Before Code

- Update `docs/06-API_SPEC.md` before implementing new endpoints.
- Update `docs/07-AGENTS.md` conventions before enforcing them in CI.
- Update `docs/04-ARCHITECTURE.md` diagrams before merging structural refactors.

---

## 11. Performance Guidelines

### 11.1 Frontend

| Technique | Where |
|-----------|-------|
| Code splitting | `next/dynamic` for heavy components (Studio, DAG viewer) |
| Lazy loading | `IntersectionObserver` for chat history, note lists |
| Memoization | `React.memo` for cards, `useMemo` for derived data |
| Virtualization | `react-window` or `@tanstack/react-virtual` for long lists (> 100 items) |
| Font optimization | `next/font` for serif headings and sans-serif body |
| Image optimization | `next/image` with WebP/AVIF, lazy loading |

### 11.2 Backend

| Technique | Where |
|-----------|-------|
| DB indexes | Foreign keys, query filters, full-text search columns |
| Connection pooling | asyncpg + SQLAlchemy pool for PostgreSQL |
| Caching | Redis for agent configs, model lists, user sessions |
| Pagination | Cursor-based everywhere; never unbounded `SELECT *` |
| N+1 prevention | `selectinload()`, `joinedload()` in queries |
| Background jobs | Celery for studio generation, long-running tasks |

---

## 12. Security Guidelines

### 12.1 Input Validation

- All API inputs validated via Pydantic v2 schemas.
- Strict string length limits, regex patterns for identifiers.
- File uploads: whitelist MIME types, scan with `python-magic`, size caps.

### 12.2 XSS Prevention

- React escapes content by default; never use `dangerouslySetInnerHTML`.
- If rendering Markdown, use a hardened parser (DOMPurify on backend).
- CSP header: `default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';`

### 12.3 CSRF Protection

- Stateless JWT in `Authorization` header (not cookies) for API calls.
- If cookies used for session fallback, set `SameSite=Strict`, `Secure`, `HttpOnly`.

### 12.4 Secrets Management

| Secret | Storage |
|--------|---------|
| JWT signing key | Environment variable (`JWT_SECRET_KEY`) |
| Provider API keys | Encrypted at rest (AES-256-GCM), decrypted per-request |
| Database credentials | Environment variables or Docker secrets |
| TLS certificates | Bind-mounted or managed by reverse proxy |

No secrets in Git. Use `.env.example` for documentation only.

### 12.5 Dependency Scanning

- `npm audit` / `pip-audit` in CI pipeline.
- Dependabot or Renovate for automated PRs.
- Pin all dependencies with exact versions in lock files.

---

## 13. Tooling Configuration

### 13.1 Frontend (`package.json` scripts)

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "format": "prettier --write .",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest"
  }
}
```

### 13.2 Backend (`pyproject.toml`)

```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]

[tool.mypy]
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
testpaths = ["app/tests"]
asyncio_mode = "auto"
```

### 13.3 Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.x.x
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.x.x
    hooks:
      - id: mypy
  - repo: local
    hooks:
      - id: prettier
        name: prettier
        entry: npx prettier --write
        language: system
        files: \.(ts|tsx|css|md|json|yaml)$
```

---

*End of Agents & Conventions*
