# Agent OS v2 — Installation & Deployment Guide

## Goldie Edition

**Version:** 2.0.0-MVP  
**Date:** 2026-08-11

---

## 1. Prerequisites

### 1.1 Required

| Tool | Version | Purpose |
|------|---------|---------|
| Docker | ≥ 27.0 | Container runtime |
| Docker Compose | ≥ 2.24 | Orchestration |
| Git | ≥ 2.40 | Source control |

### 1.2 Recommended (for local development without Docker)

| Tool | Version | Purpose |
|------|---------|---------|
| Node.js | ≥ 20.0 (LTS) | Frontend runtime |
| pnpm | ≥ 9.0 | Package manager (faster, stricter) |
| Python | ≥ 3.12 | Backend runtime |
| uv | ≥ 0.4 | Python package manager (fast, modern) |

### 1.3 System Requirements

| Environment | CPU | RAM | Disk | Notes |
|-------------|-----|-----|------|-------|
| Minimal (single user) | 2 cores | 4 GB | 20 GB | SQLite + Redis only |
| Team (PostgreSQL) | 4 cores | 8 GB | 50 GB | Add pgvector extension |
| Production | 4+ cores | 16+ GB | 100+ GB | SSD required for DB + cache |

---

## 2. Quick Start (One-Command Install)

```bash
# 1. Clone the repository
git clone https://github.com/your-org/agent-os.git
cd agent-os

# 2. Run the installer
./scripts/install.sh

# 3. Open the dashboard
open https://localhost:3000
```

What `install.sh` does:
1. Checks Docker + Docker Compose availability.
2. Creates `.env` from `.env.example` with sensible defaults.
3. Pulls and builds images (`docker compose build`).
4. Runs database migrations (`docker compose run --rm backend alembic upgrade head`).
5. Seeds default admin user and agents.
6. Starts all services (`docker compose up -d`).
7. Prints health-check URLs and next steps.

> **Tip:** Pass `--dev` flag to mount local source for hot-reload.

---

## 3. Local Development Setup

### 3.1 Clone & Structure

```bash
git clone https://github.com/your-org/agent-os.git
cd agent-os
```

```
agent-os/
├── backend/          # FastAPI app
├── frontend/         # Next.js 15 app
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
├── scripts/
│   ├── install.sh
│   ├── dev.sh
│   └── seed.sh
├── docs/
└── .env.example
```

### 3.2 Install Dependencies

**Backend:**
```bash
cd backend
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
pnpm install
```

### 3.3 Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

See §5 for the full reference.

### 3.4 Run Services

**Option A — Docker Compose (recommended for full stack):**
```bash
docker compose -f docker/docker-compose.yml up -d
```

**Option B — Native (for faster iteration):**

Terminal 1 — Redis:
```bash
docker run -d -p 6379:6379 --name agentos-redis redis:7-alpine
```

Terminal 2 — Backend:
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

Terminal 3 — Frontend:
```bash
cd frontend
pnpm dev
```

Terminal 4 — Hermes Gateway (see §7):
```bash
cd ../hermes-gateway
source .venv/bin/activate
python -m hermes.server
```

### 3.5 Verify

| Service | URL | Health Check |
|---------|-----|--------------|
| Frontend | `http://localhost:3000` | Dashboard loads |
| API | `http://localhost:8000/api/v1/health` | `{"status":"ok"}` |
| API Docs | `http://localhost:8000/docs` | Swagger UI |
| Redis | `redis-cli ping` | `PONG` |
| Hermes | `http://localhost:8642/health` | `{"status":"ok"}` |

---

## 4. Docker Compose Topology

### 4.1 Services

```yaml
# docker/docker-compose.yml (excerpt)
services:
  backend:
    build: ./docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///data/agentos.db
      - REDIS_URL=redis://redis:6379/0
      - HERMES_URL=http://hermes:8642
    volumes:
      - agentos-data:/app/data
    depends_on:
      - redis

  frontend:
    build: ./docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

  hermes:
    build: ./docker/Dockerfile.hermes
    ports:
      - "8642:8642"
    environment:
      - HERMES_PROVIDER_KEYS_PATH=/run/secrets/provider_keys
    secrets:
      - provider_keys

  celery-worker:
    build: ./docker/Dockerfile.backend
    command: celery -A app.celery_app worker -l info
    environment:
      - DATABASE_URL=sqlite:///data/agentos.db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
      - backend

  celery-beat:
    build: ./docker/Dockerfile.backend
    command: celery -A app.celery_app beat -l info
    depends_on:
      - redis

  # Team mode — uncomment for PostgreSQL
  # postgres:
  #   image: pgvector/pgvector:pg16
  #   ports:
  #     - "5432:5432"
  #   environment:
  #     - POSTGRES_USER=agentos
  #     - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
  #     - POSTGRES_DB=agentos
  #   volumes:
  #     - postgres-data:/var/lib/postgresql/data

volumes:
  agentos-data:
  redis-data:
  # postgres-data:

secrets:
  provider_keys:
    file: ./secrets/provider_keys.json
```

### 4.2 Ports

| Service | Port | Protocol | Notes |
|---------|------|----------|-------|
| Frontend | 3000 | HTTP | Next.js dev server / production |
| API | 8000 | HTTP | FastAPI (Uvicorn) |
| Redis | 6379 | TCP | Cache + Celery broker |
| Hermes | 8642 | HTTP | Internal gateway (not exposed externally) |
| PostgreSQL | 5432 | TCP | Team mode only |

### 4.3 Volumes

| Volume | Purpose | Backup? |
|--------|---------|---------|
| `agentos-data` | SQLite DB, uploads, generated artifacts | Yes |
| `redis-data` | Session cache, Celery task state | Optional |
| `postgres-data` | PostgreSQL data + pgvector embeddings | Yes |

---

## 5. Environment Variables Reference

### 5.1 Required

| Variable | Example | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///data/agentos.db` | Database connection string |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection string |
| `JWT_SECRET_KEY` | `change-me-in-production` | HS256 signing key (min 256 bits) |
| `HERMES_URL` | `http://hermes:8642` | Hermes Gateway base URL |

### 5.2 Optional (with defaults)

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | `development`, `staging`, `production` |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `API_HOST` | `0.0.0.0` | FastAPI bind host |
| `API_PORT` | `8000` | FastAPI bind port |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |
| `ACCESS_TOKEN_TTL` | `900` | Access token TTL in seconds (15 min) |
| `REFRESH_TOKEN_TTL` | `604800` | Refresh token TTL in seconds (7 days) |
| `MAX_UPLOAD_SIZE` | `10485760` | Max file upload size in bytes (10 MB) |
| `RATE_LIMIT_DEFAULT` | `120` | Default requests per minute |
| `CELERY_BROKER_URL` | same as `REDIS_URL` | Celery broker |
| `CELERY_RESULT_BACKEND` | same as `REDIS_URL` | Celery result store |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama base URL (local) |
| `ENABLE_SWAGGER` | `True` (dev) / `False` (prod) | `/docs` endpoint |
| `ENABLE_ADMIN` | `False` | FastAPI admin panel |

### 5.3 Provider Keys (encrypted at rest)

| Variable | Provider | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Claude | Anthropic API key |
| `MOONSHOT_API_KEY` | Kimi | Moonshot AI API key |
| `XAI_API_KEY` | Grok | xAI API key |
| `OPENROUTER_API_KEY` | OpenRouter | OpenRouter API key |
| `GEMINI_API_KEY` | Gemini | Google AI API key |
| `OPENAI_API_KEY` | OpenAI | OpenAI API key (for DALL-E in Studio) |

> Store provider keys in `secrets/provider_keys.json` or use Docker secrets. Never commit to Git.

### 5.4 White-Label / Branding

| Variable | Default | Description |
|----------|---------|-------------|
| `BRAND_NAME` | `Agent OS` | Application title |
| `BRAND_LOGO_URL` | — | URL or path to logo SVG |
| `BRAND_PRIMARY_COLOR` | `#A855F7` | Accent color (hex) |
| `BRAND_FAVICON` | — | Favicon path |
| `BRAND_TERMS_URL` | — | Terms of service link |
| `BRAND_PRIVACY_URL` | — | Privacy policy link |

---

## 6. Database Setup

### 6.1 SQLite (Default — Single User / Dev)

No setup required. The backend auto-creates `agentos.db` on first run.

Migrations:
```bash
cd backend
alembic upgrade head
```

> SQLite does **not** support `pgvector`. Semantic search falls back to `sqlite-vec` or is disabled.

### 6.2 PostgreSQL + pgvector (Team Mode)

**Step 1 — Start PostgreSQL with pgvector:**
```bash
docker run -d \
  --name agentos-postgres \
  -e POSTGRES_USER=agentos \
  -e POSTGRES_PASSWORD=SecurePassword123 \
  -e POSTGRES_DB=agentos \
  -p 5432:5432 \
  -v postgres-data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16
```

**Step 2 — Update `.env`:**
```env
DATABASE_URL=postgresql+asyncpg://agentos:SecurePassword123@localhost:5432/agentos
```

**Step 3 — Run migrations:**
```bash
cd backend
alembic upgrade head
```

**Step 4 — Verify pgvector:**
```bash
psql -U agentos -d agentos -c "SELECT * FROM pg_extension WHERE extname = 'vector';"
```

Expected: `vector | 0.7.0 | … | pgvector`.

---

## 7. Redis Setup

### 7.1 Docker (Recommended)

Already included in `docker-compose.yml`. For standalone:
```bash
docker run -d -p 6379:6379 --name agentos-redis redis:7-alpine
```

### 7.2 Local Install (macOS / Linux)

```bash
# macOS
brew install redis
brew services start redis

# Ubuntu / Debian
sudo apt update && sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Verify:
```bash
redis-cli ping
# → PONG
```

---

## 8. Hermes Gateway Setup

Hermes is the internal gateway that proxies requests to AI providers.

### 8.1 Clone & Install

```bash
git clone https://github.com/your-org/hermes-gateway.git
cd hermes-gateway
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[all]"
```

### 8.2 Configure

Create `hermes-gateway/.env`:
```env
HERMES_PORT=8642
HERMES_PROVIDER_KEYS_PATH=./secrets/provider_keys.json
HERMES_RATE_LIMIT_PER_MIN=60
HERMES_LOG_LEVEL=INFO
```

### 8.3 Run

```bash
python -m hermes.server
```

Verify:
```bash
curl http://localhost:8642/health
# → {"status":"ok"}
```

### 8.4 Docker

Hermes is included in the main `docker-compose.yml`. No manual setup needed if using Docker.

---

## 9. Provider API Keys Setup

Agent OS requires at least one provider key to function. Configure all you want to use.

### 9.1 Kimi (Moonshot AI)

1. Sign up at https://platform.moonshot.cn
2. Generate an API key.
3. Add to `secrets/provider_keys.json`:
```json
{
  "moonshot": {
    "api_key": "sk-your-moonshot-key",
    "base_url": "https://api.moonshot.cn/v1"
  }
}
```

### 9.2 Claude (Anthropic)

1. Sign up at https://console.anthropic.com
2. Create an API key.
3. Add to secrets:
```json
{
  "anthropic": {
    "api_key": "sk-ant-your-anthropic-key",
    "base_url": "https://api.anthropic.com/v1"
  }
}
```

### 9.3 Grok (xAI)

1. Sign up at https://x.ai/api
2. Add to secrets:
```json
{
  "xai": {
    "api_key": "xai-your-xai-key",
    "base_url": "https://api.x.ai/v1"
  }
}
```

### 9.4 OpenRouter

1. Sign up at https://openrouter.ai
2. Add to secrets:
```json
{
  "openrouter": {
    "api_key": "sk-or-your-openrouter-key",
    "base_url": "https://openrouter.ai/api/v1"
  }
}
```

### 9.5 Ollama (Local)

No API key needed. Ensure Ollama is running:
```bash
ollama serve
ollama pull llama3.1
```

Set `OLLAMA_HOST=http://localhost:11434` in `.env`.

---

## 10. First Run

### 10.1 Create Admin User

```bash
cd backend
python -m app.commands.create_admin \
  --email admin@agentos.local \
  --name "System Administrator" \
  --password SecureAdminPass123
```

Or use the Docker helper:
```bash
docker compose run --rm backend python -m app.commands.create_admin \
  --email admin@agentos.local \
  --name "System Administrator" \
  --password SecureAdminPass123
```

### 10.2 Seed Default Agents

```bash
docker compose run --rm backend python -m app.commands.seed_agents
```

This creates pre-configured agents:
- `claude` — Claude Sonnet 4
- `hermes` — Hermes (local reasoning)
- `openclaw` — OpenClaw / OpenRouter
- `kimi` — Kimi Moonshot
- `grok` — Grok 3
- `gemini` — Gemini 2.5

### 10.3 Test Chat

1. Open `http://localhost:3000`.
2. Log in with admin credentials.
3. Click **New Chat** → Select an agent → Send a message.
4. Verify SSE streaming response appears in the chat window.

### 10.4 Verify Health

```bash
# Full stack health check
./scripts/health-check.sh
```

Expected output:
```
✅ Frontend     http://localhost:3000
✅ API          http://localhost:8000/api/v1/health
✅ Redis        localhost:6379
✅ Hermes       http://localhost:8642/health
✅ DB           connected (SQLite)
```

---

## 11. Troubleshooting

### 11.1 Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Frontend can't connect to API` | CORS or wrong `NEXT_PUBLIC_API_URL` | Check `.env` CORS_ORIGINS and API URL |
| `Hermes 502` | Hermes not running or wrong port | Verify `HERMES_URL` and `docker ps` |
| `Celery tasks stuck` | Redis down or worker not started | `docker compose up -d celery-worker` |
| `SQLite locked` | Concurrent writes in dev mode | Switch to PostgreSQL for multi-worker |
| `Chat streaming broken` | SSE blocked by proxy | Ensure no proxy buffers SSE; check `X-Accel-Buffering: no` |
| `Provider key not found` | Missing in `provider_keys.json` | Add key and restart Hermes |
| `Database migration failed` | Schema drift | `alembic downgrade -1 && alembic upgrade head` |

### 11.2 Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f celery-worker

# Backend (native)
cd backend
python -m app.main 2>&1 | tee logs/app.log
```

### 11.3 Health Checks

| Endpoint | Expected | Check Command |
|----------|----------|---------------|
| `/api/v1/health` | `{"status":"ok"}` | `curl http://localhost:8000/api/v1/health` |
| `/api/v1/health/db` | `{"status":"ok","latency_ms":3}` | `curl http://localhost:8000/api/v1/health/db` |
| `/api/v1/health/redis` | `{"status":"ok"}` | `curl http://localhost:8000/api/v1/health/redis` |
| `/api/v1/health/hermes` | `{"status":"ok"}` | `curl http://localhost:8000/api/v1/health/hermes` |

---

## 12. Upgrade Path

### 12.1 Safe Migrations

```bash
# 1. Pull latest
git pull origin main

# 2. Backup database
cp data/agentos.db data/agentos.db.$(date +%Y%m%d).bak

# 3. Rebuild images
docker compose build

# 4. Run migrations
docker compose run --rm backend alembic upgrade head

# 5. Restart
docker compose up -d
```

### 12.2 Backup Strategy

| Data | Method | Frequency | Retention |
|------|--------|-----------|-----------|
| SQLite DB | `cp` / `sqlite3 .backup` | Daily | 7 days |
| PostgreSQL | `pg_dump` | Daily | 30 days |
| Redis | `BGSAVE` + `cp dump.rdb` | Hourly | 24 hours |
| Generated artifacts | `rsync` to S3 / NAS | On creation | 90 days |

Automated backup script:
```bash
# scripts/backup.sh
#!/bin/bash
BACKUP_DIR=/backups/agentos/$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

docker exec agentos-backend sqlite3 /app/data/agentos.db ".backup $BACKUP_DIR/agentos.db"
pg_dump -h localhost -U agentos agentos > $BACKUP_DIR/agentos.sql 2>/dev/null || true
docker exec agentos-redis redis-cli BGSAVE
docker cp agentos-redis:/data/dump.rdb $BACKUP_DIR/

tar czf $BACKUP_DIR.tar.gz $BACKUP_DIR
rm -rf $BACKUP_DIR
```

---

## 13. Production Deployment Checklist

### 13.1 TLS & Reverse Proxy

```nginx
# nginx / Caddy example
server {
    listen 443 ssl http2;
    server_name agentos.example.com;

    ssl_certificate /etc/letsencrypt/live/agentos.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/agentos.example.com/privkey.pem;

    location / {
        proxy_pass http://frontend:3000;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Use **Caddy** for automatic TLS (recommended):
```
agentos.example.com {
    reverse_proxy /api/* backend:8000
    reverse_proxy /ws/* backend:8000
    reverse_proxy * frontend:3000
}
```

### 13.2 Production `.env` Changes

```env
ENVIRONMENT=production
LOG_LEVEL=WARNING
CORS_ORIGINS=https://agentos.example.com
ENABLE_SWAGGER=False
ENABLE_ADMIN=False
RATE_LIMIT_DEFAULT=120
JWT_SECRET_KEY=<256-bit-random-hex>
DATABASE_URL=postgresql+asyncpg://agentos:SecurePass@postgres:5432/agentos
```

Generate a strong JWT secret:
```bash
openssl rand -hex 32
```

### 13.3 Hardening Checklist

- [ ] TLS 1.3 enabled; HSTS header set
- [ ] `JWT_SECRET_KEY` rotated from default; ≥ 256 bits
- [ ] Provider keys stored in Docker secrets or external vault (HashiCorp Vault, AWS Secrets Manager)
- [ ] PostgreSQL password strong, non-default port optional
- [ ] Redis bound to Docker network only (not exposed to host)
- [ ] Hermes gateway not exposed to public internet
- [ ] Firewall rules: only 443 (HTTPS) open to public
- [ ] Rate limiting enabled at reverse proxy layer (fail2ban / nginx limit_req)
- [ ] Backups automated and tested monthly
- [ ] Monitoring: Prometheus + Grafana or UptimeRobot
- [ ] Log aggregation: Loki / ELK / CloudWatch
- [ ] Health check alerts on PagerDuty / Slack

### 13.4 Docker Compose Production Overrides

```yaml
# docker-compose.prod.yml
services:
  backend:
    restart: unless-stopped
    deploy:
      replicas: 2
    environment:
      - ENVIRONMENT=production

  frontend:
    restart: unless-stopped
    deploy:
      replicas: 2

  celery-worker:
    restart: unless-stopped
    deploy:
      replicas: 4

  postgres:
    restart: unless-stopped
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./backups:/backups

  redis:
    restart: unless-stopped
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
```

Run with:
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

*End of Installation & Deployment Guide*
