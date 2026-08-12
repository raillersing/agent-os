---
document_id: ADR-005
title: Conversation Domain, Visibility, and Derived Data Privacy
version: 0.1.0
status: draft
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - quality-owner
created: 2026-08-12
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents:
  - DOC-000
  - ADR-003
  - GLO-001
  - DDD-001
  - DAT-001
  - DCT-001
  - API-001
  - EVT-001
  - MEM-001
  - ART-001
  - IAM-001
  - AUD-001
related_adrs:
  - ADR-003
supersedes: []
---

# ADR-005 — Conversation Domain, Visibility, and Derived Data Privacy

## Status

**Draft — proposed decision.** This ADR defines the domain and privacy boundary for conversations that pass through Agent OS. It does not claim that conversation capture, synchronization, or access control is implemented.

## Decision

`Conversation` is a first-class aggregate in the Agent OS domain. It is an independent interaction thread that may link to a project, mission, task, or run without being forced into the work hierarchy.

Each conversation has:

- an owner and actor chain;
- workspace scope;
- optional project, mission, task, and run links;
- messages and attachments;
- participating agent and provider references;
- visibility: `private`, `project`, or `workspace`;
- explicit shares and revocations;
- retention profile and deletion state;
- derived artifact and memory references;
- audit and correlation identifiers.

The default visibility is `private`. Workspace membership does not grant access to private conversations. Sharing a conversation, message, attachment, artifact, or derived memory is a separate auditable authorization decision.

Only interactions crossing an Agent OS-controlled interface or adapter boundary are captured as Agent OS conversations. External conversations that never pass through Agent OS are not claimed as captured or synchronized.

## Derived-data rules

- Private conversation content cannot create project or workspace-visible memory without an explicit promotion decision.
- Search indexes, embeddings, previews, notifications, exports, artifacts, and caches inherit the most restrictive source visibility unless separately authorized.
- Revoking conversation access revokes access to derived views and triggers projection/index invalidation.
- Deleting a conversation deletes or anonymizes derived content according to its retention and audit obligations.
- Audit records preserve the access or deletion fact without retaining deleted content unnecessarily.

## Acceptance criteria

- A private conversation is invisible to unauthorized members, search, notifications, exports, and derived retrieval.
- A shared conversation can be revoked without changing workspace membership.
- Every message and derived object can be traced to its conversation and actor.
- Conversation deletion has a recoverable period, legal-hold behavior, backup treatment, and audit record.
- Provider and adapter records distinguish captured Agent OS content from external content not observed by Agent OS.
