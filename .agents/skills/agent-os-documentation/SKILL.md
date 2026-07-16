---
name: agent-os-documentation
description: Create, review, register, validate, and maintain controlled Agent OS documentation, ADRs, contracts, traceability, and evidence according to DOC-000.
---

# Agent OS Documentation Skill

## Use this skill when

- creating or revising a controlled document;
- creating an ADR;
- updating the document register;
- generating architecture or contract documentation;
- checking traceability or documentation consistency;
- preparing documentation evidence for a pull request or release.

## Required workflow

1. Read `docs/00-governance/DOC-000-documentation-governance.md`.
2. Read `docs/00-governance/GLO-001-glossary.md`.
3. Inspect `docs/document-register.yaml`.
4. Identify the requested document, its dependencies, owner, phase, and status.
5. Inspect all approved upstream documents before drafting downstream content.
6. Clearly label assumptions, proposals, unresolved questions, and implementation-derived facts.
7. Do not set status to `approved` or `implemented` without explicit human authorization and evidence.
8. Update the document register when creating, moving, renaming, superseding, or archiving a document.
9. Add an ADR when the change is architecturally significant.
10. Run `python3 scripts/validate_docs.py`.
11. Report changed files, validation results, open questions, and required approvals.

## Quality rules

- Preserve stable identifiers.
- Use testable language.
- Avoid duplicate sources of truth.
- Link requirements, architecture, contracts, tests, and evidence.
- Prefer primary external sources.
- Never fabricate citations, repository state, tests, approvals, or implementation status.
