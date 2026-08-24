# Dependency Migration Plan

This document tracks coordinated dependency upgrades that cannot safely be done
as isolated Dependabot bumps. PRs in these groups should be created manually,
validated against the full CI matrix, and merged together.

## Backend group: Pydantic / FastAPI / HTTP stack

**Goal** : move from the current pinned set to a modern, mutually compatible set.

Current pinned versions (as of 2026-08-24):
- `pydantic==2.6.1`
- `pydantic-settings==2.1.0`
- `fastapi==0.110.0`
- `starlette<0.37.0,>=0.36.3`
- `httpx==0.26.0`
- `passlib[bcrypt]==1.7.4`
- `bcrypt==4.1.2`

**Target direction** (to be chosen at migration time):
- `pydantic>=2.7.0` (to satisfy modern pydantic-settings)
- `pydantic-settings>=2.15.0`
- `fastapi>=0.115.0` (or the latest version compatible with the chosen pydantic)
- `httpx>=0.27.0` (FastAPI 0.111+ requires httpx >= 0.27 for `TestClient`)
- `bcrypt>=5.0.0` already merged separately; keep aligned with passlib

**Blockers / compatibility notes**:
- FastAPI 0.110.0 pins starlette 0.36.3 and pydantic 2.6.x. Upgrading any one
  of pydantic/pydantic-settings/fastapi/httpx requires upgrading all four.
- `TestClient` in starlette 0.36.3 is incompatible with httpx >= 0.27 if not
  used through FastAPI. After the upgrade, `tests/test_api.py` must be
  re-collected and the full test suite (56 tests) must pass.
- The Temporal SDK and SQLAlchemy 2.0 must remain compatible with the chosen
  pydantic version.

**Acceptance criteria**:
1. `pip install -r backend/requirements.txt` resolves without conflicts.
2. `pip install -r backend/requirements.runtime.txt` resolves without conflicts.
3. `pytest -q` in `backend/` → 56 passed.
4. `python scripts/check_openapi_parity.py` → PASSED.
5. `flake8 app tests scripts` → clean.
6. `docker build -t agent-os-backend:local backend/` succeeds.
7. Alembic migration chain (`alembic upgrade head`) still works from scratch.

**Reference** : Dependabot PR #22 was closed because the isolated bump of
`pydantic-settings` to 2.15.0 breaks dependency resolution against pinned
`pydantic==2.6.1` and `fastapi==0.110.0`.

---

## Frontend group: React / Next.js / Tailwind / ESLint

**Goal** : escape the current EOL / deprecated set and remove build-time
peer-dependency conflicts.

Current pinned versions (as of 2026-08-24):
- `next@14.1.0` (deprecated; security advisory published)
- `react@^18.2.0`
- `react-dom@^18.2.0`
- `@types/react@^18.2.55`
- `@types/react-dom@^18.2.18`
- `tailwindcss@3.4.19`
- `eslint@^8.56.0`
- `eslint-config-next@14.1.0`

**Target direction** (to be chosen at migration time):
- `next@^15` or `^16` (only after security review of breaking changes)
- `react@^19` and `react-dom@^19` (aligned with Next.js 15/16 default)
- `@types/react@^19` and `@types/react-dom@^19`
- `tailwindcss@^4` with `@tailwindcss/postcss` plugin and updated
  `postcss.config.*`
- `eslint@^9` with flat config and `eslint-config-next` matching the chosen
  Next.js version

**Blockers / compatibility notes**:
- Tailwind CSS v4 no longer ships a built-in PostCSS plugin. `tailwindcss`
  cannot be used directly in `postcss.config.*`; it must be replaced by
  `@tailwindcss/postcss`. `src/app/globals.css` must be audited for v4
  incompatibilities.
- eslint-config-next >= 16 requires `eslint>=9.0.0`. The whole ESLint setup
  (`.eslintrc.json`, `eslint` version, any custom plugins) must migrate to
  ESLint 9 flat config in the same PR.
- React 19 type definitions are not compatible with `@types/react-dom@18`.
  React, React-DOM, Next.js and their type packages must be bumped together.

**Acceptance criteria**:
1. `npm ci` in `frontend/` succeeds without `--legacy-peer-deps`.
2. `npm run lint` succeeds.
3. `npm run build` succeeds.
4. `docker build -t agent-os-frontend:local frontend/` succeeds.
5. No unhandled peer-dependency warnings from `npm ci`.

**References**:
- Dependabot PR #19 (tailwindcss 4.3.3) was closed because the isolated bump
  breaks PostCSS configuration.
- Dependabot PR #24 (eslint-config-next 16.3.0) was closed because it requires
  ESLint 9, while the project is still on ESLint 8.
- Dependabot PR #26 (react + @types/react) was closed because the React 19 type
  bump conflicts with the pinned `@types/react-dom@18`.

---

## Process

1. Open one PR per group, not one PR per package.
2. Assign both groups to the same milestone / release.
3. Run the full CI matrix on each PR before merging.
4. After both groups merge, cut a release that documents the dependency
   baseline change.
