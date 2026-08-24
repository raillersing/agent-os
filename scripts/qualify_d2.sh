#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
cd "$repo_root"
export PYTHONPATH="$repo_root/backend${PYTHONPATH:+:$PYTHONPATH}"
if [[ -n "${D2_DATABASE_URL:-}" ]]; then
  export DATABASE_URL="$D2_DATABASE_URL"
fi

pytest_args=(backend/tests/test_d2_provider.py)
if [[ "${D2_INCLUDE_D1:-1}" == "1" ]]; then
  pytest_args+=(backend/tests/test_simulator.py backend/tests/test_d1_execution.py)
fi
python3 -m pytest "${pytest_args[@]}"
python3 -m black --check backend/app backend/tests
python3 -m isort --check-only backend/app backend/tests
python3 -m flake8 backend/app backend/tests
python3 scripts/validate_docs.py
python3 scripts/evals/run_d2_golden.py
if [[ "${D2_LIVE:-0}" == "1" ]]; then
  python3 scripts/evals/run_d2_live.py
fi
echo "D2 qualification PASS: simulator default, OpenAI adapter opt-in, context manifest and cost semantics covered"
