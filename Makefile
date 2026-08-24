# Agent OS Makefile

.PHONY: help dev dev-build test test-cov lint format build clean migrate logs logs-backend logs-frontend shell-backend shell-postgres status restart restart-backend restart-frontend

# Default target
help:
	@echo "Agent OS Development Commands"
	@echo "============================"
	@echo ""
	@echo "  make dev             Start development environment"
	@echo "  make dev-build       Start with rebuild"
	@echo "  make test            Run backend tests"
	@echo "  make test-cov        Run backend tests with coverage"
	@echo "  make lint            Run linting"
	@echo "  make format          Format code"
	@echo "  make build           Build Docker images"
	@echo "  make clean           Stop and remove containers"
	@echo "  make migrate         Run database migrations"
	@echo "  make logs            View logs"
	@echo "  make shell-backend   Open backend shell"
	@echo "  make shell-postgres  Open PostgreSQL shell"
	@echo ""

# Development
dev:
	docker compose up -d

dev-build:
	docker compose up -d --build

# Testing
test:
	cd backend && pytest -q

test-cov:
	cd backend && pytest --cov=app --cov-report=html

# Linting
lint:
	cd backend && black --check . && isort --check-only . && flake8 .

format:
	cd backend && black . && isort .

# Docker
build:
	docker compose build

clean:
	docker compose down -v

# Database
migrate:
	docker compose exec backend alembic upgrade head

# Logs
logs:
	docker compose logs -f

logs-backend:
	docker compose logs -f backend

logs-frontend:
	docker compose logs -f frontend

# Shell
shell-backend:
	docker compose exec backend bash

shell-postgres:
	docker compose exec postgres psql -U agent_os -d agent_os

# Status
status:
	docker compose ps

# Restart
restart:
	docker compose restart

restart-backend:
	docker compose restart backend

restart-frontend:
	docker compose restart frontend
