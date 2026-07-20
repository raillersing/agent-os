# Agent OS Makefile

.PHONY: help dev test lint build clean migrate seed

# Default target
help:
	@echo "Agent OS Development Commands"
	@echo "============================"
	@echo ""
	@echo "  make dev          Start development environment"
	@echo "  make dev-build    Start with rebuild"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linting"
	@echo "  make format       Format code"
	@echo "  make build        Build Docker images"
	@echo "  make clean        Stop and remove containers"
	@echo "  make migrate      Run database migrations"
	@echo "  make seed         Seed database"
	@echo "  make logs         View logs"
	@echo "  make shell-backend  Open backend shell"
	@echo ""

# Development
dev:
	docker-compose up -d

dev-build:
	docker-compose up -d --build

# Testing
test:
	cd backend && pytest -v

test-cov:
	cd backend && pytest --cov=app --cov-report=html

# Linting
lint:
	cd backend && black --check . && isort --check-only . && flake8 .

format:
	cd backend && black . && isort .

# Docker
build:
	docker-compose build

clean:
	docker-compose down -v

# Database
migrate:
	docker-compose exec backend alembic upgrade head

seed:
	docker-compose exec backend python -m app.utils.seed

# Logs
logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

# Shell
shell-backend:
	docker-compose exec backend bash

shell-postgres:
	docker-compose exec postgres psql -U agent_os -d agent-os

# Status
status:
	docker-compose ps

# Restart
restart:
	docker-compose restart

restart-backend:
	docker-compose restart backend

restart-frontend:
	docker-compose restart frontend
