#!/usr/bin/env python3
"""Check the checked-in OpenAPI contract against the mounted FastAPI app."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.main import app  # noqa: E402

CONTRACT_SCHEMAS = {
    "Agent",
    "AgentCreate",
    "AgentUpdate",
    "Run",
    "RunCreate",
    "RunOptions",
    "Memory",
    "MemoryCreate",
    "MemorySearchResults",
    "Tool",
    "ToolExecution",
    "ToolResult",
    "Workspace",
    "WorkspaceCreate",
    "Project",
    "ProjectCreate",
    "ProjectUpdate",
    "Mission",
    "MissionCreate",
    "Task",
    "TaskCreate",
    "ExecutionRun",
    "ExecutionRunCreate",
    "RunAttempt",
    "Artifact",
    "ExecutionReceipt",
    "Automation",
    "AutomationCreate",
    "Approval",
    "ApprovalCreate",
    "ApprovalDecision",
    "AuditEvent",
}


def properties(schema: dict, schemas: dict) -> set[str]:
    result = set(schema.get("properties", {}))
    for branch in schema.get("allOf", []):
        reference = branch.get("$ref", "")
        name = reference.rsplit("/", 1)[-1]
        if name:
            result.update(properties(schemas.get(name, {}), schemas))
        result.update(branch.get("properties", {}))
    return result


def main() -> int:
    contract = yaml.safe_load(
        (ROOT / "schemas/openapi.yaml").read_text(encoding="utf-8")
    )
    runtime = app.openapi()
    errors: list[str] = []

    expected_paths = set(runtime["paths"])
    actual_paths = set(contract["paths"])
    for path in sorted(expected_paths - actual_paths):
        errors.append(f"missing path: {path}")
    for path in sorted(actual_paths - expected_paths):
        errors.append(f"unmounted path: {path}")

    runtime_schemas = runtime["components"]["schemas"]
    contract_schemas = contract["components"]["schemas"]
    for name in sorted(CONTRACT_SCHEMAS):
        if name not in runtime_schemas:
            errors.append(f"missing runtime schema: {name}")
            continue
        if name not in contract_schemas:
            errors.append(f"missing contract schema: {name}")
            continue
        runtime_properties = properties(runtime_schemas[name], runtime_schemas)
        contract_properties = properties(contract_schemas[name], contract_schemas)
        if runtime_properties != contract_properties:
            errors.append(
                f"schema {name} properties differ: "
                f"runtime={sorted(runtime_properties)} "
                f"contract={sorted(contract_properties)}"
            )

    if errors:
        print("OpenAPI parity FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"OpenAPI parity PASSED: {len(expected_paths)} paths and "
        f"{len(CONTRACT_SCHEMAS)} application schemas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
