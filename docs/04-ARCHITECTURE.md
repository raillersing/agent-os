---
document_id: SAD-002
title: Agent OS v2 Architecture — Archived Legacy Snapshot
version: 2.0.1
status: archived
owner: architecture-owner
approvers:
  - architecture-owner
  - security-owner
created: 2026-08-11
last_reviewed: 2026-08-13
classification: internal
source_of_truth: false
related_documents: [SAD-001, C4-001, C4-002, INT-001, DEP-001, ORC-001]
related_adrs: [ADR-001, ADR-003, ADR-004, ADR-005]
---

# Agent OS v2 Architecture — Archived Legacy Snapshot

> **Status:** Archived. **Not a source of truth.**
>
> This file previously described itself as the architectural “single source of truth”. That statement is obsolete and conflicted with its controlled metadata. The active architecture is governed by the registered controlled documents listed below.

## Why this file is archived

This document was an intermediate Agent OS v2 consolidation produced before the current controlled-document architecture and ADR set were finalized. Its detailed diagrams, technology assumptions, provider examples, deployment descriptions, and runtime mappings may no longer match the approved architecture.

It must therefore **not** be used to make implementation, security, deployment, provider, orchestration, or data-model decisions.

The historical content remains recoverable through Git history. Replacing the working-tree copy with this archive notice prevents obsolete prose from competing with the approved sources of truth while preserving provenance in repository history.

## Current authoritative references

Use the following controlled documents instead:

| Subject | Current controlled reference |
|---|---|
| System architecture | `SAD-001` — System Architecture Description |
| System context | `C4-001` — System Context Diagram |
| Container boundaries | `C4-002` — Container Diagram |
| Domain model | `DDD-001` — Domain Model |
| Data architecture | `DAT-001` / `DAT-002` |
| Integration architecture | `INT-001` |
| Durable orchestration | `ADR-004` and `ORC-001` |
| Run semantics | `RUN-001` |
| Adapter contract | `AGC-001` |
| Model-provider abstraction | `MOD-001` |
| Identity and access | `IAM-001` |
| Policy and permissions | `POL-001` |
| Security | `SEC-001`, `SEC-002`, `THR-001` |
| Deployment | `DEP-001` |
| Operations and recovery | `OPS-001`, `BCP-001` |
| Quality and release gates | `QAG-001` |

## Current decision precedence

When a historical statement from this file conflicts with a current controlled source, use this order:

```text
approved ADR
→ approved source-of-truth controlled document
→ approved supporting controlled document
→ in-review proposal, only as non-authoritative direction
→ archived document, historical reference only
```

In particular:

- Temporal is governed by `ADR-004`; this archived file cannot redefine durable orchestration.
- Workspace isolation, approvals, retention, and execution authority are governed by the current controlled contracts and ADRs.
- Provider, adapter, pilot, and tooling decisions under active review must be read from their registered current documents, not inferred from examples that appeared in this legacy snapshot.

## Historical preservation

No attempt is made here to rewrite the historical design as if it had always matched the current architecture. The prior contents remain available through Git history under earlier revisions of `docs/04-ARCHITECTURE.md`.

This archive notice exists solely to remove source-of-truth ambiguity from the current documentation set.
