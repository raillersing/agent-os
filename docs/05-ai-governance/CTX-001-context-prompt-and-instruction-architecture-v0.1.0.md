---
document_id: CTX-001
title: Agent OS Context, Prompt and Instruction Architecture
version: 0.1.0
status: in-review
owner: architecture-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-08-13
last_reviewed: 2026-08-13
classification: internal
source_of_truth: false
related_documents:
  - SAD-001
  - AGC-001
  - MOD-001
  - RUN-001
  - AUT-001
  - POL-001
  - MEM-001
  - DAT-002
  - SEC-001
  - THR-001
  - TST-001
  - AUD-001
  - EVAL-001
  - MLC-001
related_adrs:
  - ADR-003
  - ADR-005
  - ADR-006
  - ADR-007
pending_approvals:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
---

# CTX-001 — Context, Prompt and Instruction Architecture

> **Status: In review.** This document proposes the architecture for how Agent OS constructs, versions, constrains, records, and reasons about the effective context supplied to an AI agent or model. It is non-authoritative until the required review roles approve it.

## 1. Purpose

For an agentic system, the effective model input is part of the executable system state.

A model response can change because of:

- system instructions;
- agent profile instructions;
- mission/task instructions;
- workspace policy;
- memory;
- retrieved knowledge;
- conversation history;
- tool schemas;
- user input;
- external documents or web content;
- summarization/truncation;
- provider/model behavior.

Agent OS therefore MUST NOT model a prompt as an opaque string assembled ad hoc by each adapter.

This document defines the proposed control-plane architecture for context and instruction assembly.

## 2. Goals

The architecture should ensure that Agent OS can answer:

1. What instructions were authoritative for this attempt?
2. What data was supplied to the model?
3. Which parts came from humans, policy, memory, retrieval, tools, agents, or external content?
4. What was omitted, summarized, truncated, or transformed?
5. Which exact context/prompt profile version was used?
6. Which data classifications were disclosed to which provider/model?
7. Can a reviewer reconstruct the effective context without exposing secrets unnecessarily?
8. Can a material context change trigger re-evaluation?

## 3. Core principle — context is typed, not concatenated

Agent OS SHOULD represent context as typed segments with explicit provenance and authority.

Recommended conceptual model:

```text
Context Manifest
├── policy/system constraints
├── agent profile instructions
├── mission/task instructions
├── user input
├── conversation segments
├── authoritative workspace data
├── memory references
├── retrieval references
├── tool schemas/capabilities
├── tool observations
├── external/untrusted content
└── derived summaries
```

Adapters MAY render these segments into provider-specific formats, but they SHOULD NOT silently change authority semantics.

## 4. Instruction authority classes

Agent OS SHOULD distinguish at least:

```text
platform_policy
workspace_policy
agent_profile_instruction
mission_instruction
task_instruction
human_user_instruction
approved_human_decision
tool_contract
retrieved_authoritative_data
memory_verified
memory_unverified
agent_generated_content
external_untrusted_content
derived_summary
```

These are not all equivalent.

Content authority and instruction authority MUST remain separate concepts.

A document can be authoritative as **data** while still being unable to grant new permissions or override platform policy.

## 5. Authority ordering

The precise policy remains governed by `AUT-001` and `POL-001`, but the context assembler SHOULD preserve a stable precedence model such as:

```text
platform/security policy
        ↓
workspace policy
        ↓
approved control-plane decision
        ↓
agent capability/profile constraint
        ↓
mission/task instruction
        ↓
human request within allowed scope
        ↓
retrieved or external content as data
```

Lower-authority content MUST NOT redefine higher-authority policy merely by containing instruction-like text.

## 6. Untrusted content boundary

The following SHOULD be treated as untrusted by default unless an explicit control marks a narrower trusted role:

- web pages;
- emails;
- issue/comment bodies;
- repository files supplied as task data;
- PDFs/documents;
- generated artifacts;
- tool output containing external text;
- retrieved chunks;
- model-generated memory proposals;
- output from another agent;
- pasted instructions inside user-provided data.

Untrusted content may contain text such as “ignore previous instructions”, but that text MUST NOT acquire authority merely because it appears in context.

## 7. Context segment schema

A context segment SHOULD carry fields equivalent to:

```yaml
segment_id:
segment_type:
authority_class:
source_type:
source_id:
source_version:
workspace_id:
classification:
content_hash:
created_at:
observed_at:
freshness_state:
trust_state:
transformation:
parent_segment_ids: []
redaction_state:
retention_profile:
```

Raw content MAY be stored separately according to classification, retention, and secret-handling rules.

## 8. Effective Context Manifest

Every material model invocation SHOULD have an `effective_context_manifest` or equivalent evidence object.

It SHOULD identify:

- context profile/version;
- ordered segment references;
- effective authority classes;
- source/provenance;
- content hashes;
- transformation/summarization lineage;
- omission/truncation events;
- token-budget decisions;
- redaction events;
- model/provider disclosure decision;
- tool schema versions;
- final rendered prompt/message hash where technically possible and safe.

The manifest is evidence. It does not require storing secret plaintext indefinitely.

## 9. Prompt and instruction profiles

Reusable system instructions and templates SHOULD be versioned configuration artifacts rather than anonymous strings embedded throughout application code.

A profile SHOULD include:

```text
profile_id
version
purpose
owner
applicable agent/task classes
instruction template hash
variable schema
authority class
allowed data classifications
compatible model capabilities
change history
evaluation qualification reference
```

Material profile changes SHOULD trigger the evaluation rules in `EVAL-001`.

## 10. Template variables

Template variables SHOULD be declared and typed.

The renderer SHOULD distinguish:

- instruction-safe variables;
- plain data variables;
- structured JSON/schema variables;
- untrusted text blocks;
- secret references;
- tool schema references.

Untrusted text SHOULD NOT be interpolated into a higher-authority instruction position without an explicit escaping/encoding strategy and security review.

## 11. Context assembly pipeline

Recommended conceptual pipeline:

```text
Task/Run accepted
      ↓
resolve policies + capability profile
      ↓
resolve model/context profile
      ↓
collect candidate context sources
      ↓
authorize workspace/data access
      ↓
classify + label provenance
      ↓
apply redaction/disclosure rules
      ↓
rank/select within token budget
      ↓
summarize/transform where permitted
      ↓
construct Effective Context Manifest
      ↓
render provider/adapter-specific request
      ↓
record invocation evidence
```

Authorization MUST occur before retrieval content is exposed to model-side ranking or prompt construction where cross-workspace leakage could occur.

## 12. Token budget architecture

Context windows are finite. Truncation therefore requires policy, not incidental string slicing.

Each context profile SHOULD define budget classes for:

- invariant policy/system instructions;
- task/mission instructions;
- conversation/history;
- memory;
- retrieval;
- tool descriptions;
- tool observations;
- output reserve.

Example conceptual allocation:

```text
model context capacity
- mandatory system/policy reserve
- task reserve
- tool-schema reserve
- output reserve
= dynamic context budget
```

Numeric allocations SHOULD be configuration and evaluation data rather than hard-coded universal constants.

## 13. Truncation rules

Truncation SHOULD be deterministic where practical and observable.

Agent OS SHOULD NOT silently discard:

- security/policy constraints;
- approval conditions;
- task-critical instructions;
- explicit user constraints;
- provenance required to interpret evidence.

When lower-priority context is removed, the manifest SHOULD record what category was omitted and why.

## 14. Summarization rules

Summaries are derived data, not replacements for provenance.

A summary SHOULD record:

- source segment IDs;
- summarizer identity/profile where relevant;
- summary prompt/version;
- generated content hash;
- source classification maximum;
- verification state;
- freshness;
- whether the original remains available to authorized reviewers.

An agent-generated summary MUST NOT become more authoritative than its sources.

## 15. Memory injection

`MEM-001` governs memory architecture. Context assembly SHOULD preserve memory authority and freshness states.

The model SHOULD be able to distinguish, where relevant:

```text
human_asserted
human_verified
agent_generated
inferred
disputed
conflicted
stale
expired
```

Repetition does not convert an unverified memory into fact.

Memory retrieval MUST be workspace-authorized before ranking or injection.

## 16. Retrieval and RAG context

Retrieved context SHOULD carry:

- source identity;
- source version/date;
- workspace scope;
- classification;
- retrieval query/reference;
- rank/score where meaningful;
- authority/trust state;
- freshness;
- content hash;
- snippet bounds.

Retrieval ranking is relevance evidence, not truth evidence.

## 17. Conversation context

Conversation history SHOULD be explicitly scoped by:

- workspace;
- project/mission/task/run as applicable;
- participant visibility;
- retention policy;
- privacy constraints from `ADR-005`;
- context relevance rules.

Conversation context from another workspace MUST NOT be injected solely because semantic retrieval finds it similar.

## 18. Agent-to-agent delegation

A delegated agent SHOULD receive only the context required for its delegated capability.

Parent agents SHOULD NOT automatically forward:

- all conversation history;
- all workspace memory;
- all credentials;
- all tools;
- all approvals;
- higher classification data than required.

Delegation context SHOULD include a provenance link to the parent run/attempt and an explicit delegated authority envelope.

No child-agent output becomes a new authorization decision merely because the parent trusts the child.

## 19. Tool schema context

Tool descriptions supplied to models are part of executable AI context and SHOULD be versioned.

For each exposed tool, context evidence SHOULD identify:

- tool/capability ID;
- schema version;
- effect class;
- approval class;
- scope constraints;
- target restrictions;
- whether execution is delegated through the Agent OS Tool Gateway.

A model seeing a tool schema does not itself grant permission to execute the tool.

## 20. Tool observations

Tool output SHOULD be represented as observation/data with source identity.

The system SHOULD distinguish:

```text
confirmed result
partial result
stale result
unavailable result
unknown effect
conflicted result
adapter-reported result
provider-reported result
```

The model MUST NOT be instructed to convert `unknown` into success for user convenience.

## 21. Data classification and provider disclosure

Before sending any context segment to an external provider, Agent OS SHOULD evaluate:

- workspace authorization;
- data classification;
- provider/model allowlist;
- region restrictions if configured;
- local-only requirement;
- contractual/policy restrictions;
- redaction/minimization requirements.

A provider fallback MUST re-evaluate disclosure eligibility. Eligibility is not inherited merely because the original provider was allowed.

## 22. Secret handling

Raw secrets SHOULD NOT be inserted into general-purpose model context unless an explicitly approved use case requires it and technical controls support it.

Prefer:

- opaque secret references;
- brokered tool execution;
- scoped credentials at execution boundary;
- redacted context;
- least-privilege temporary tokens.

Secrets MUST NOT be retained in prompt/context evidence simply to improve reproducibility.

## 23. Prompt injection defenses

Context architecture SHOULD use defense in depth:

- authority labeling;
- clear separation of instructions and data;
- least-privilege tools;
- policy enforcement outside the model;
- workspace authorization outside the model;
- approval checks outside the model;
- target/fingerprint validation outside the model;
- default-deny protected effects;
- content provenance;
- adversarial evaluation in `EVAL-001`/`TST-001`.

Prompt wording alone is not an adequate security boundary.

## 24. Provider-specific rendering

Adapters MAY translate the context manifest into provider-native message structures.

Rendering SHOULD preserve, as far as supported:

- instruction/data distinction;
- ordering;
- tool schemas;
- multimodal references;
- content boundaries;
- requested output schema.

Provider-specific quirks SHOULD be treated as adapter/profile behavior and covered by conformance/evaluation evidence.

## 25. Context caching

If provider or local context caching is used, Agent OS SHOULD record enough evidence to determine:

- which stable prefix/profile was cached;
- cache identity/version where observable;
- whether a material policy/context change invalidated the cache;
- usage/cost accounting source;
- data retention/privacy implications.

Cache reuse MUST NOT bypass changed authorization or classification rules.

## 26. Reproducibility manifest

`CTX-001` establishes the context portion of the wider execution reproducibility manifest.

For each material model attempt, the evidence SHOULD allow correlation of:

```yaml
run_id:
attempt_id:
agent_profile_id:
adapter_id:
adapter_version:
model_profile_id:
configured_provider:
actual_provider:
actual_model:
context_profile_id:
context_profile_version:
effective_context_manifest_id:
system_instruction_hash:
prompt_template_versions: []
memory_refs: []
retrieval_refs: []
tool_schema_versions: []
policy_version:
capability_profile_version:
runtime_build:
workflow_version:
usage_record_id:
receipt_id:
```

Where an exact value cannot be observed, the evidence SHOULD use an explicit state such as `unknown` rather than inventing precision.

## 27. Privacy-preserving reproducibility

Reproducibility does not require indefinite raw-prompt retention.

Depending on classification and retention policy, evidence MAY use:

- hashes;
- immutable references;
- encrypted restricted storage;
- redacted copies;
- structural manifests;
- source version IDs;
- deletion tombstones.

`DAT-002`, `ADR-005`, and `AUD-001` govern retention, privacy, and evidence requirements.

## 28. Change classification

Context changes SHOULD be categorized as:

### Non-material
Examples: comment-only metadata, formatting that cannot affect rendered context.

### Material low-risk
Examples: wording adjustment within a non-critical informational template.

### Material behavioral
Examples:

- system instruction change;
- authority-order change;
- new tool description;
- new memory strategy;
- retrieval strategy change;
- truncation priority change;
- summarization prompt change;
- provider-specific rendering change.

Material behavioral changes SHOULD trigger relevant `EVAL-001` regression suites.

## 29. Context drift detection

Agent OS SHOULD be able to detect mismatch between:

- configured context profile and executed profile;
- expected tool schema and observed schema;
- expected policy version and runtime policy version;
- expected prompt hash and rendered hash;
- approved model profile and actual model identity.

Material drift SHOULD produce audit evidence and MAY block or suspend protected execution according to policy.

## 30. Minimum MVP baseline

Before the first real model-provider vertical slice is considered complete, the implementation SHOULD support at minimum:

1. versioned context profile identity;
2. typed separation of system/task/user/untrusted content;
3. explicit workspace authorization before memory/retrieval injection;
4. tool schema version evidence;
5. provider disclosure/classification checks;
6. no silent policy/tool authority via prompt text;
7. effective context manifest or equivalent evidence;
8. prompt/system-template hashes or version IDs;
9. recorded truncation/summarization when material;
10. correlation with run/attempt/model/usage/audit records.

## 31. Implementation guidance

The MVP does not require a complex prompt-management SaaS or a dedicated external prompt registry.

A repository-backed/versioned configuration approach is acceptable initially if it provides:

- stable IDs;
- explicit versions;
- reviewable changes;
- deterministic rendering where practical;
- tests/evals;
- runtime evidence of the selected profile.

The architecture SHOULD avoid premature dependence on a vendor-specific prompt-management platform.

## 32. Failure behavior

Context assembly MUST fail safely when:

- required policy cannot be resolved;
- workspace authorization cannot be established;
- required classification is unknown;
- context profile is incompatible with the selected model;
- mandatory instruction segment is missing;
- disclosure policy blocks the provider;
- context exceeds supported capacity without an allowed truncation strategy;
- required provenance cannot be established for a protected workflow.

The system SHOULD expose the reason rather than silently degrade to a less-governed context.

## 33. Governance

- Product owns intended task/user semantics.
- Architecture owns context assembly contracts and profile compatibility.
- Security owns authority separation, prompt-injection boundaries and disclosure controls.
- Data owns classification, provenance, retention and memory/retrieval data rules.
- Operations owns runtime configuration integrity and operational evidence.
- Quality owns context regression and evaluation evidence integration.

No agent-generated prompt or context change may self-approve a change to critical authority or security policy.

## 34. Relationship to evaluation and lifecycle

`CTX-001`, `EVAL-001`, and `MLC-001` form a control loop:

```text
context/model configuration
        ↓
behavioral evaluation
        ↓
qualification
        ↓
controlled rollout
        ↓
observability/incidents
        ↓
context/model change
        ↓
re-evaluation
```

## 35. Review focus

Reviewers should specifically validate:

- instruction-authority classes and precedence;
- separation between authoritative data and authoritative instruction;
- effective-context evidence requirements;
- token-budget/truncation semantics;
- summarization and memory authority rules;
- provider disclosure controls;
- prompt-injection defense outside the model;
- reproducibility versus privacy trade-offs;
- minimum MVP implementation scope.
