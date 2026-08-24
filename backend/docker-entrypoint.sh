#!/bin/sh
set -e

# Apply the latest Alembic revisions before starting the API.
alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8080
