#!/usr/bin/env python3
"""Minimal validator for the Agent OS controlled documentation starter.

Checks:
- document register can be parsed with the Python standard library subset used here;
- registered files with status other than planned exist;
- controlled Markdown files contain required front-matter keys;
- document IDs are unique and match the front matter;
- statuses are allowed;
- no approved document contains common unresolved placeholders.

This intentionally avoids third-party dependencies for the starter phase.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
REGISTER = DOCS / "document-register.yaml"
REQUIRED = {
    "document_id",
    "title",
    "version",
    "status",
    "owner",
    "approvers",
    "created",
    "last_reviewed",
    "classification",
    "source_of_truth",
    "related_documents",
    "related_adrs",
}
ALLOWED_STATUS = {
    "draft",
    "in-review",
    "approved",
    "implemented",
    "deprecated",
    "superseded",
    "archived",
}
UNRESOLVED = ("TODO", "TBD", "TO CONFIRM", "REQUIRES CONFIRMATION")


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        raise ValueError("unterminated YAML front matter")
    data: dict[str, str] = {}
    current_list_key: str | None = None
    for raw in parts[1].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_list_key:
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        if not key:
            continue
        data[key] = value.strip()
        current_list_key = key if value.strip() == "" else None
    return data


def parse_register_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in text.splitlines():
        match = re.match(r"\s*- id:\s*(\S+)\s*$", raw)
        if match:
            if current:
                entries.append(current)
            current = {"id": match.group(1)}
            continue
        if current:
            match = re.match(r"\s+(path|status):\s*(.+?)\s*$", raw)
            if match:
                current[match.group(1)] = match.group(2).strip("'\"")
    if current:
        entries.append(current)
    return entries


def main() -> int:
    errors: list[str] = []
    seen_ids: dict[str, Path] = {}

    if not REGISTER.exists():
        errors.append(f"Missing register: {REGISTER}")
        entries = []
    else:
        entries = parse_register_entries(REGISTER.read_text(encoding="utf-8"))

    for entry in entries:
        doc_id = entry.get("id")
        path_value = entry.get("path")
        status = entry.get("status")
        if not doc_id or not path_value or not status:
            errors.append(f"Incomplete register entry: {entry}")
            continue
        path = ROOT / path_value
        if status != "planned" and not path.exists():
            errors.append(f"Registered {status} document does not exist: {path_value}")

    for path in DOCS.rglob("*.md"):
        if "/templates/" in path.as_posix() or path.name == "README.md":
            continue
        try:
            metadata = parse_front_matter(path)
        except ValueError as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue

        missing = sorted(REQUIRED - metadata.keys())
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing metadata {missing}")

        doc_id = metadata.get("document_id", "").strip("'\"")
        if doc_id:
            if doc_id in seen_ids:
                errors.append(
                    f"Duplicate document_id {doc_id}: "
                    f"{seen_ids[doc_id].relative_to(ROOT)} and {path.relative_to(ROOT)}"
                )
            seen_ids[doc_id] = path

        status = metadata.get("status", "").strip("'\"")
        if status and status not in ALLOWED_STATUS:
            errors.append(f"{path.relative_to(ROOT)}: invalid status {status}")

        if status in {"approved", "implemented"}:
            upper = path.read_text(encoding="utf-8").upper()
            for marker in UNRESOLVED:
                if marker in upper:
                    errors.append(
                        f"{path.relative_to(ROOT)}: approved/implemented document contains {marker}"
                    )

    registered_ids = {entry.get("id") for entry in entries}
    for doc_id, path in seen_ids.items():
        if doc_id not in registered_ids:
            errors.append(
                f"Controlled document missing from register: {doc_id} ({path.relative_to(ROOT)})"
            )

    if errors:
        print("Documentation validation FAILED:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Documentation validation PASSED: "
        f"{len(seen_ids)} controlled documents, {len(entries)} register entries."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
