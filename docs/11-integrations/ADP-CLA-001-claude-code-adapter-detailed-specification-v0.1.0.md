---
document_id: ADP-CLA-001
title: Claude Code Adapter Detailed Specification
version: 0.1.0
status: draft
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - operations-owner
  - quality-owner
created: 2026-08-12
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents:
  - DOC-000
  - GLO-001
  - SAD-001
  - AGC-001
  - RUN-001
  - API-001
  - APR-001
  - SAN-001
  - IAM-001
  - AUD-001
related_adrs:
  - ADR-003
  - ADR-005
related_evidence: []
---

# ADP-CLA-001 — Claude Code Adapter Detailed Specification

> **Status: Draft.** This profile defines the required conformance boundary for Claude Code. It does not claim that Claude Code is connected, validated, or production-ready in Agent OS.

## 1. Purpose

Claude Code is one of the three initial Agent OS adapter targets. The adapter must expose Claude Code through the provider-neutral `AGC-001` contract without allowing runtime-specific authority to bypass Agent OS identity, workspace scope, policy, approval, sandbox, artifact, memory, or audit controls.

## 2. Required adapter capabilities

The profile must verify, or explicitly report `unknown` or `unsupported` for:

- start, status, cancellation, pause, and resume;
- streaming messages and structured events;
- conversation capture through the Agent OS boundary;
- workspace/project/repository identity;
- tool visibility and tool-call proposals;
- file, command, browser, network, and Git operations;
- sandbox and secret-boundary behavior;
- artifacts, patches, logs, and provenance;
- model/provider identity and usage evidence;
- timeout, heartbeat, retry, and effect-certainty reporting;
- recovery and reconciliation after process or network failure.

## 3. Security requirements

- Claude Code receives a workload identity distinct from the human requester.
- The adapter cannot approve actions or grant capabilities.
- All tool and filesystem effects pass through the Tool Gateway and selected sandbox profile.
- Workspace scope and conversation visibility are attached to every request and event.
- Raw secrets are never included in prompts, ordinary logs, artifacts, or memory.
- Unknown tool visibility, cancellation semantics, or effect certainty blocks protected execution.

## 4. Conformance gates

Claude Code becomes an initial supported adapter only after:

1. adapter contract tests pass;
2. private/project/workspace conversation scope tests pass;
3. approval, cancellation, retry, and unknown-effect tests pass;
4. sandbox, filesystem, network, and secret tests pass;
5. usage, artifact, and audit evidence is verified;
6. capability gaps are registered and accepted by the required owners.

## 5. Open decisions

- official Claude Code invocation boundary;
- supported local installation profiles on Windows and Linux;
- event and stream normalization;
- checkpoint and resume guarantees;
- provider/API usage evidence;
- adapter upgrade and rollback behavior.
