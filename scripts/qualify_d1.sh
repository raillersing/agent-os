#!/usr/bin/env bash
set -Eeuo pipefail

# Reproducible local D1 qualification. All credentials are test-only values.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)-$$"
ARTIFACT_DIR="$ROOT/artifacts/d1/$RUN_ID"
mkdir -p "$ARTIFACT_DIR"
exec > >(tee "$ARTIFACT_DIR/qualification.log") 2>&1
export COMPOSE_PROJECT_NAME=agent-os-d1
export POSTGRES_DB=agent_os_d1
export POSTGRES_USER=agent_os
export POSTGRES_PASSWORD=d1-local-postgres-only
export SECRET_KEY=d1-local-secret-key-not-for-production-0123456789
export ADMIN_EMAIL=admin@d1.local
export ADMIN_PASSWORD=d1-local-admin-only
export TEMPORAL_NAMESPACE=default
export TEMPORAL_TASK_QUEUE=agent-os-d1
export POSTGRES_HOST_PORT=15435 REDIS_HOST_PORT=16381 BACKEND_HOST_PORT=18080 FRONTEND_HOST_PORT=13080
export NEXT_PUBLIC_API_URL=http://127.0.0.1:18080
export CORS_ORIGINS='["http://localhost:3080","http://127.0.0.1:3080","http://127.0.0.1:13080"]'
curl() { command curl --retry 8 --retry-connrefused --retry-delay 1 "$@"; }

dc() { docker compose -p "$COMPOSE_PROJECT_NAME" "$@"; }
PYTHON_IMAGE="${D1_PYTHON_IMAGE:-agent-os-d1-backend}"

cleanup_one_shots() {
  docker ps -aq --filter "label=com.docker.compose.project=$COMPOSE_PROJECT_NAME" \
    --filter "name=${COMPOSE_PROJECT_NAME}-backend-run" | xargs -r docker rm -f >/dev/null 2>&1 || true
}

reset_d1_stack() {
  dc down --remove-orphans -v >/dev/null 2>&1 || true
  cleanup_one_shots
}

collect_diagnostics() {
  set +e
  {
    echo "run_id=$RUN_ID"
    echo "started_at=$STARTED_AT"
    echo "finished_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    git rev-parse HEAD 2>/dev/null | sed 's/^/commit_sha=/'
    git branch --show-current 2>/dev/null | sed 's/^/branch=/'
    git status --short 2>/dev/null | sed 's/^/dirty=/'
  } > "$ARTIFACT_DIR/manifest.txt"
  dc ps > "$ARTIFACT_DIR/compose-final.txt" 2>&1
  docker version > "$ARTIFACT_DIR/docker-version.txt" 2>&1
  docker compose version > "$ARTIFACT_DIR/docker-compose-version.txt" 2>&1
  dc config > "$ARTIFACT_DIR/compose-resolved.yaml" 2>&1
  docker ps -a --filter "label=com.docker.compose.project=$COMPOSE_PROJECT_NAME" \
    --format '{{.ID}} {{.Names}} {{.Status}}' > "$ARTIFACT_DIR/container-list.txt" 2>&1
  for service in postgres redis temporal backend temporal-worker frontend; do
    dc logs --no-color "$service" > "$ARTIFACT_DIR/log-$service.txt" 2>&1
  done
  while read -r container; do
    [ -n "$container" ] || continue
    docker inspect --format '{{json .State}}' "$container" >> "$ARTIFACT_DIR/container-states.jsonl" 2>/dev/null
    docker inspect "$container" >> "$ARTIFACT_DIR/inspect-$container.json" 2>/dev/null
    docker inspect --format '{{.Name}} status={{.State.Status}} exit={{.State.ExitCode}} oom_killed={{.State.OOMKilled}} error={{.State.Error}} started={{.State.StartedAt}} finished={{.State.FinishedAt}}' "$container" >> "$ARTIFACT_DIR/container-state-summary.txt" 2>/dev/null
  done < <(docker ps -aq --filter "label=com.docker.compose.project=$COMPOSE_PROJECT_NAME")
  if command -v sha256sum >/dev/null; then
    sha256sum "$ARTIFACT_DIR"/* > "$ARTIFACT_DIR/artifact-sha256.txt" 2>/dev/null
  fi
}

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
trap collect_diagnostics EXIT

# Preflight and reset are intentionally scoped to the dedicated D1 project.
docker info > "$ARTIFACT_DIR/docker-preflight.txt"
docker compose version >> "$ARTIFACT_DIR/docker-preflight.txt"
dc ps -a > "$ARTIFACT_DIR/compose-initial.txt" 2>&1 || true
# Remove only D1 test volumes/histories so every run starts controlled.
reset_d1_stack
dc config --quiet
dc up -d postgres redis
until docker exec "${COMPOSE_PROJECT_NAME}-postgres-1" pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" >/dev/null 2>&1; do sleep 2; done
dc up -d temporal backend temporal-worker
until curl -fsS http://127.0.0.1:18080/health >/dev/null; do sleep 2; done

# Prove the D1 migration is reversible, then restore the head before fixtures.
dc stop backend temporal-worker temporal >/dev/null
dc start postgres redis >/dev/null
cleanup_one_shots
dc run --rm --no-deps backend alembic upgrade head
dc run --rm --no-deps backend alembic downgrade 0004
dc run --rm --no-deps backend alembic upgrade head
dc up -d temporal backend temporal-worker >/dev/null
until curl -fsS http://127.0.0.1:18080/health >/dev/null; do sleep 2; done

token=$(curl -fsS -X POST http://127.0.0.1:18080/api/v1/auth/token -H 'Content-Type: application/json' -d '{"email":"admin@d1.local","password":"d1-local-admin-only"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["access_token"])')
auth="Authorization: Bearer $token"
json_id() { python3 -c 'import json,sys; print(json.load(sys.stdin)[sys.argv[1]])' "$1"; }
ws=$(curl -fsS -X POST http://127.0.0.1:18080/api/v1/workspaces -H "$auth" -H 'Content-Type: application/json' -d '{"name":"D1 qualification"}')
wid=$(printf '%s' "$ws" | json_id id)
project=$(curl -fsS -X POST http://127.0.0.1:18080/api/v1/projects -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"name\":\"D1 project\",\"purpose\":\"qualification\"}")
pid=$(printf '%s' "$project" | json_id project_id)
mission=$(curl -fsS -X POST http://127.0.0.1:18080/api/v1/missions -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"project_id\":\"$pid\",\"title\":\"D1 mission\",\"objective\":\"qualification\"}")
mid=$(printf '%s' "$mission" | json_id id)
task=$(curl -fsS -X POST http://127.0.0.1:18080/api/v1/tasks -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"project_id\":\"$pid\",\"mission_id\":\"$mid\",\"title\":\"D1 task\",\"desired_outcome\":\"evidence\"}")
tid=$(printf '%s' "$task" | json_id id)

run=$(curl -fsS -X POST "http://127.0.0.1:18080/api/v1/tasks/$tid/runs" -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"input_text\":\"success\",\"simulator_profile\":\"success\",\"idempotency_key\":\"happy\"}")
rid=$(printf '%s' "$run" | json_id id)
for _ in $(seq 1 30); do
  result=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$rid?workspace_id=$wid" -H "$auth")
  if printf '%s' "$result" | python3 -c 'import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if d["state"] == "completed" and d["artifacts"] and d["receipt"] else 1)'; then
    break
  fi
  sleep 1
done
# Re-read after the polling window so a completion committed at the boundary
# is not mistaken for a failed qualification assertion.
result=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$rid?workspace_id=$wid" -H "$auth")
printf '%s' "$result" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["state"] == "completed" and d["attempts"] and d["artifacts"] and d["receipt"]'
dc up -d frontend
until curl -fsS http://127.0.0.1:13080 >/dev/null; do sleep 2; done
docker run --rm --network host \
  -e D1_FRONTEND_URL=http://127.0.0.1:13080 \
  -e D1_WORKSPACE_ID="$wid" -e D1_API_TOKEN="$token" \
  -v "$ROOT/scripts/d1_frontend_e2e.mjs:/workspace/d1_frontend_e2e.mjs:ro" \
  -w /workspace mcr.microsoft.com/playwright:v1.51.1-jammy \
  sh -c 'npm install --silent --no-save playwright@1.51.1 && node d1_frontend_e2e.mjs' \
  2>&1 | tee "$ARTIFACT_DIR/frontend-e2e.txt"
duplicate=$(curl -fsS -X POST "http://127.0.0.1:18080/api/v1/tasks/$tid/runs" -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"input_text\":\"success\",\"simulator_profile\":\"success\",\"idempotency_key\":\"happy\"}")
test "$(printf '%s' "$duplicate" | json_id id)" = "$rid"
test "$(curl -s -o /dev/null -w '%{http_code}' -X POST "http://127.0.0.1:18080/api/v1/tasks/$tid/runs" -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"input_text\":\"different\",\"simulator_profile\":\"success\",\"idempotency_key\":\"happy\"}")" = 409
curl -fsS "http://127.0.0.1:18080/api/v1/audit-events?workspace_id=$wid&limit=200" -H "$auth" | python3 -c 'import json,sys; events=json.load(sys.stdin); rid=sys.argv[1]; assert sum(e["event_type"] == "run.dispatched" and e["resource_id"] == rid for e in events) == 1' "$rid"

# Cross-workspace reads fail closed.
ws_b=$(curl -fsS -X POST http://127.0.0.1:18080/api/v1/workspaces -H "$auth" -H 'Content-Type: application/json' -d '{"name":"D1 other workspace"}' | json_id id)
test "$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:18080/api/v1/execution-runs/$rid?workspace_id=$ws_b" -H "$auth")" = 404
test "$(curl -s -o /dev/null -w '%{http_code}' -X POST "http://127.0.0.1:18080/api/v1/tasks/$tid/runs" -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$ws_b\",\"input_text\":\"cross\",\"simulator_profile\":\"success\",\"idempotency_key\":\"cross\"}")" = 404

start_run() {
  local profile="$1" key="$2"
  curl -fsS -X POST "http://127.0.0.1:18080/api/v1/tasks/$tid/runs" -H "$auth" -H 'Content-Type: application/json' -d "{\"workspace_id\":\"$wid\",\"input_text\":\"$profile\",\"simulator_profile\":\"$profile\",\"idempotency_key\":\"$key\"}" | json_id id
}
check_run() {
  local id="$1" state="$2"
  echo "checking run=$id expected=$state"
  result=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$id?workspace_id=$wid" -H "$auth")
  audit=$(curl -fsS "http://127.0.0.1:18080/api/v1/audit-events?workspace_id=$wid&limit=200" -H "$auth")
  printf '%s' "$result" | python3 -c 'import json,sys; d=json.load(sys.stdin); expected=sys.argv[1]; ok=d["state"] == expected and d["receipt"] and d["receipt"]["terminal_state"] == expected and d["attempts"] and all(a["state"] != "retrying" for a in d["attempts"]); ok = ok and (expected != "completed" or d["artifacts"]); print(json.dumps({"state":d["state"],"receipt":d["receipt"],"attempts":[a["state"] for a in d["attempts"]],"artifacts":len(d["artifacts"])})); raise SystemExit(0 if ok else 1)' "$state"
  printf '%s' "$audit" | python3 -c 'import json,sys; events=json.load(sys.stdin); run_id=sys.argv[1]; assert any(e["resource_type"] == "execution_run" and e["resource_id"] == run_id for e in events)' "$id"
}

for profile in non_retryable_failure timeout retryable_failure; do
  id=$(start_run "$profile" "matrix-$profile")
  for _ in $(seq 1 15); do sleep 1; state=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$id?workspace_id=$wid" -H "$auth" | python3 -c 'import json,sys;print(json.load(sys.stdin)["state"])'); [ "$state" = failed ] && break; done
  check_run "$id" failed
  if [ "$profile" = retryable_failure ]; then
    curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$id?workspace_id=$wid" -H "$auth" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert len(d["attempts"]) == 2'
  else
    curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$id?workspace_id=$wid" -H "$auth" | python3 -c 'import json,sys; d=json.load(sys.stdin); assert len(d["attempts"]) == 1'
  fi
done

# Real Temporal cancellation: the slow Activity is running when cancel is sent.
cancel_id=$(start_run slow_success cancellation)
sleep 2
curl -fsS -X POST "http://127.0.0.1:18080/api/v1/execution-runs/$cancel_id/cancel?workspace_id=$wid" -H "$auth" >/dev/null
check_run "$cancel_id" cancelled

# Temporal durable recovery across a real worker stop/start.
recover_id=$(start_run slow_success worker-recovery)
sleep 2
dc stop temporal-worker >/dev/null
state=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$recover_id?workspace_id=$wid" -H "$auth" | python3 -c 'import json,sys;print(json.load(sys.stdin)["state"])')
test "$state" = running -o "$state" = queued
dc start temporal-worker >/dev/null
for _ in $(seq 1 45); do sleep 1; state=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$recover_id?workspace_id=$wid" -H "$auth" | python3 -c 'import json,sys;print(json.load(sys.stdin)["state"])'); [ "$state" = completed ] && break; done
check_run "$recover_id" completed

# API restart does not remove the durable read model or Temporal execution.
api_id=$(start_run slow_success api-recovery)
sleep 2
dc restart backend >/dev/null
until curl -fsS http://127.0.0.1:18080/health >/dev/null; do sleep 1; done
for _ in $(seq 1 45); do sleep 1; state=$(curl -fsS "http://127.0.0.1:18080/api/v1/execution-runs/$api_id?workspace_id=$wid" -H "$auth" | python3 -c 'import json,sys;print(json.load(sys.stdin)["state"])'); [ "$state" = completed ] && break; done
check_run "$api_id" completed

# Re-run the D1 fault/concurrency regression tests in the same qualification.
# These tests cover post-commit dispatch recovery, terminal Activity redelivery,
# cancellation/completion races, workspace boundaries, and concurrent accepts.
docker run --rm -v "$ROOT:/workspace" -w /workspace "$PYTHON_IMAGE" sh -c \
  'pip install --quiet pytest==7.4.4 pytest-asyncio==0.23.4 && cd /tmp && DATABASE_URL=sqlite+aiosqlite:///./d1-regression.db SECRET_KEY=test-secret-key-with-more-than-32-characters ADMIN_EMAIL=admin@test.local ADMIN_PASSWORD=test-password PYTHONPATH=/workspace/backend pytest -q /workspace/backend/tests/test_d1_execution.py -k "accepted_run or accepted_run_remains_recoverable or unknown_temporal or unknown_cancellation or duplicate_post_cancellation or activity_redelivery or cancellation_completion or workspace_isolation or concurrent_duplicate"' \
  2>&1 | tee "$ARTIFACT_DIR/d1-regression-tests.txt"

# Re-run all repository gates in the same qualified run. The backend quality
# container is disposable and uses an isolated SQLite file for unit tests.
docker run --rm -v "$ROOT:/workspace" -w /workspace "$PYTHON_IMAGE" sh -c \
  'pip install --quiet pytest==7.4.4 pytest-asyncio==0.23.4 black==24.1.1 isort==5.13.2 flake8==7.0.0 && cd /tmp && DATABASE_URL=sqlite+aiosqlite:///./d1-gate.db SECRET_KEY=test-secret-key-with-more-than-32-characters ADMIN_EMAIL=admin@test.local ADMIN_PASSWORD=test-password PYTHONPATH=/workspace/backend pytest -q /workspace/backend/tests && cd /workspace && black --check backend && isort --check-only backend && flake8 backend' \
  2>&1 | tee "$ARTIFACT_DIR/backend-gates.txt"

docker compose -p "$COMPOSE_PROJECT_NAME" build frontend 2>&1 | tee "$ARTIFACT_DIR/frontend-image-build.txt"
dc run --rm --no-deps frontend npm run lint 2>&1 | tee "$ARTIFACT_DIR/frontend-lint.txt"
dc run --rm --no-deps frontend npm run build 2>&1 | tee "$ARTIFACT_DIR/frontend-build.txt"

docker run --rm -v "$ROOT:/workspace" -w /workspace "$PYTHON_IMAGE" sh -c \
  'python3 scripts/validate_docs.py && python3 scripts/check_openapi_parity.py' \
  2>&1 | tee "$ARTIFACT_DIR/documentation-openapi.txt"

docker run --rm -v "$ROOT:/workspace" -w /workspace node:22.14.0-bookworm-slim sh -c \
  'npx --yes @redocly/cli@1.34.0 lint schemas/openapi.yaml && npx --yes @asyncapi/cli@2.16.3 validate --fail-severity warn schemas/asyncapi.yaml' \
  2>&1 | tee "$ARTIFACT_DIR/schema-gates.txt"

dc config --quiet
cleanup_one_shots
test -z "$(docker ps -aq --filter "label=com.docker.compose.project=$COMPOSE_PROJECT_NAME" --filter "name=${COMPOSE_PROJECT_NAME}-backend-run")"
dc ps > "$ARTIFACT_DIR/compose-post-gates.txt"

echo "D1 qualification PASS: workspace=$wid task=$tid run=$rid"
echo "D1 artifacts: $ARTIFACT_DIR"
