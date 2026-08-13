---
document_id: EVAL-001
title: Agent OS AI Behavioral Evaluation and Model Qualification Standard
version: 0.1.0
status: in-review
owner: quality-owner
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
  - TST-001
  - QAG-001
  - MOD-001
  - RUN-001
  - AGC-001
  - AUT-001
  - CST-001
  - POL-001
  - SEC-001
  - THR-001
  - MEM-001
  - AUD-001
  - OBS-001
  - CTX-001
  - MLC-001
related_adrs:
  - ADR-003
  - ADR-004
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

# EVAL-001 — AI Behavioral Evaluation and Model Qualification Standard

> **Status: In review.** This document proposes the behavioral evaluation and qualification baseline for models, agent profiles, model bindings, prompts, context assemblies, adapters, and AI-assisted workflows in Agent OS. It is intentionally non-authoritative until the required review roles approve it.

## 1. Purpose

Agent OS must not treat successful API invocation, schema conformance, or infrastructure health as proof that an AI configuration is suitable for a mission.

This standard defines how Agent OS should answer five separate questions:

1. **Can the model or agent perform the required capability?**
2. **Can it do so within the required safety, authority, and data boundaries?**
3. **Is the behavior sufficiently reliable across repeated and adversarial cases?**
4. **Is the cost and latency acceptable for the intended operating profile?**
5. **Has the exact model/context/agent configuration been qualified for the intended use?**

`TST-001` remains the system verification strategy. `EVAL-001` adds AI-behavior evaluation and does not replace functional, security, integration, recovery, accessibility, or operational tests.

## 2. Scope

This standard applies to:

- deterministic provider simulators used to validate Agent OS behavior;
- external model-provider bindings;
- local model bindings;
- model profile changes;
- provider or model version changes;
- context/prompt changes that can materially affect behavior;
- Hermes, Codex, Claude Code, and future adapter profiles;
- agent capability profiles;
- tool-use behavior;
- retrieval and memory-assisted behavior;
- model-routing and fallback candidates;
- release and pilot qualification where AI behavior is part of acceptance.

It does not claim that any current model is qualified, safe, factual, or production-ready.

## 3. Evaluation object

A qualification result must apply to an **evaluation object**, not merely to a model name.

The evaluation object SHOULD identify at minimum:

```text
provider binding
actual model identity when observable
logical model profile
agent profile
adapter + adapter version
context/prompt profile + version
policy profile
capability profile
tool set + tool schema versions
memory/retrieval profile where applicable
runtime/build identity
evaluation suite version
dataset/fixture version
```

A model qualified with one context or tool profile is not automatically qualified with a materially different context or tool profile.

## 4. Qualification states

Agent OS SHOULD distinguish the following states:

```text
unassessed
experimental
qualified_restricted
qualified
regressed
suspended
retired
unknown
```

### `unassessed`
No accepted evaluation evidence exists for the requested operating profile.

### `experimental`
Evidence exists but the configuration is limited to development, test, or explicitly bounded experimentation.

### `qualified_restricted`
The configuration meets criteria only within documented restrictions such as task classes, data classifications, tool scopes, context limits, or human-review requirements.

### `qualified`
The configuration meets the accepted qualification criteria for the stated profile.

### `regressed`
Previously accepted behavior no longer meets one or more release-blocking criteria.

### `suspended`
Use is temporarily blocked because evidence is stale, an incident is active, model identity is uncertain, or a material provider/configuration change has occurred.

### `retired`
The configuration is no longer eligible for new execution.

### `unknown`
Qualification state cannot be established from available evidence. `unknown` MUST NOT be represented as qualified.

## 5. Evaluation layers

Agent OS SHOULD maintain a layered evaluation portfolio.

| Layer | Purpose |
|---|---|
| E0 — Deterministic contract | Validate harness, schema, receipts, routing, usage/cost capture, tool gates and failure handling |
| E1 — Capability | Determine whether the AI configuration can perform the intended task class |
| E2 — Reliability | Measure stability across repeated, perturbed, long-context and edge cases |
| E3 — Safety/authority | Test policy obedience, prompt injection resistance, tool boundaries, approval boundaries and data restrictions |
| E4 — Grounding/provenance | Evaluate support from supplied evidence, citation/source use, unknown handling and claim traceability |
| E5 — Tool/agent behavior | Evaluate tool selection, argument correctness, scope, sequencing, stopping and recovery |
| E6 — Cost/latency | Quantify token use, estimated/measured cost, wall-clock latency and resource amplification |
| E7 — Human acceptance | Evaluate usefulness, comprehensibility, reviewability and operational suitability |
| E8 — Release regression | Compare candidate and accepted baselines before promotion |

No single scalar score should erase a release-blocking failure in a critical category.

## 6. Evaluation dimensions

Each relevant evaluation suite SHOULD define measurable criteria for the following dimensions.

### 6.1 Task success

- objective completion;
- required outputs present;
- requested format respected;
- constraints respected;
- no unsupported task substitution;
- correct stopping condition.

### 6.2 Factuality and grounding

- claims supported by supplied evidence where required;
- citations or source references correctly attributed where required;
- unsupported assertions measured separately from supported assertions;
- explicit uncertainty when evidence is insufficient;
- no conversion of unknown into false certainty.

### 6.3 Instruction adherence

- authority hierarchy respected;
- system and policy constraints preserved;
- user intent followed within allowed scope;
- untrusted content treated as data rather than authority;
- conflicting instructions resolved according to `CTX-001`.

### 6.4 Tool use

- correct tool selected;
- correct arguments;
- least-privilege scope;
- no unauthorized or unnecessary call;
- approval requirements respected;
- no duplicate consequential effect;
- correct interpretation of tool result;
- correct behavior when tool result is partial, stale, unavailable, or conflicted.

### 6.5 Security and agentic abuse resistance

- prompt and instruction injection;
- memory poisoning;
- authority laundering;
- cross-workspace access attempt;
- secret exfiltration attempt;
- tool escalation;
- malicious artifact/content handling;
- cost amplification;
- unsafe delegation/fan-out;
- reviewer manipulation.

`THR-001`, `SEC-001`, `POL-001`, `AUT-001`, and `TST-001` remain the control authorities for security requirements.

### 6.6 Reliability

- repeated-run variance;
- sensitivity to minor wording changes;
- long-context degradation;
- missing-input behavior;
- contradiction handling;
- retry behavior;
- graceful refusal or escalation where capability is insufficient.

### 6.7 Operational efficiency

- input tokens;
- output tokens;
- cached tokens where observable;
- total token amplification;
- estimated and measured cost states;
- median and tail latency;
- external/tool call count;
- retry count;
- artifact size and execution duration where relevant.

## 7. Evaluation case taxonomy

Suites SHOULD contain a deliberate mix of:

```text
canonical cases
boundary cases
negative cases
ambiguous cases
conflicting-evidence cases
missing-data cases
long-context cases
multi-step cases
adversarial cases
prompt-injection cases
tool-failure cases
provider-failure cases
cost-amplification cases
historical regression cases
real incident reproductions when sanitized and permitted
```

A suite composed only of easy or happy-path examples is not acceptable evidence for critical agentic workflows.

## 8. Dataset and fixture governance

Every evaluation dataset SHOULD have:

- stable identifier;
- semantic or monotonic version;
- owner;
- purpose;
- allowed data classification;
- provenance;
- licensing/use constraints where relevant;
- train/test contamination considerations where known;
- change history;
- expected outcome or grading rubric;
- retirement criteria.

Real secrets MUST NOT be embedded in evaluation fixtures.

Personal or confidential information SHOULD be synthetic unless explicitly governed for the evaluation purpose.

## 9. Golden cases

Golden cases are high-value reference cases with reviewed expectations.

Golden cases SHOULD be used for:

- critical instruction hierarchy;
- approval boundaries;
- tool-call argument correctness;
- no-silent-fallback behavior;
- unknown-state handling;
- workspace isolation;
- model identity reporting;
- cost/usage evidence;
- factual grounding;
- artifact provenance;
- incident regression.

A golden-case update requires review because changing the expected answer can hide a regression.

## 10. Repetition and nondeterminism

Where an AI configuration is nondeterministic, one successful run is insufficient.

The suite SHOULD define:

- number of repeated runs appropriate to consequence and expected variance;
- sampling parameters;
- deterministic seed where supported;
- acceptable pass-rate or distribution;
- maximum catastrophic-failure rate;
- confidence/uncertainty reporting.

Release-blocking unsafe behavior MUST NOT be averaged away by good mean performance.

Example principle:

```text
99 acceptable outputs + 1 unauthorized protected action
!= qualified
```

## 11. Grading methods

Evaluation MAY combine:

- exact match;
- structured/schema comparison;
- deterministic rules;
- programmatic task verification;
- state-machine verification;
- reference-answer comparison;
- human review;
- pairwise preference;
- rubric-based scoring;
- model-assisted judging.

For critical controls, deterministic or human-verifiable evidence SHOULD take precedence over opaque model judging.

## 12. Model-assisted judging

Model-assisted judges MAY be used for bounded qualitative dimensions but MUST NOT be treated as infallible.

When used, evidence SHOULD record:

- judge provider/model identity when observable;
- judge prompt/rubric version;
- candidate output;
- reference/context supplied to the judge;
- judge result and rationale where permitted;
- calibration against reviewed human examples;
- known judge biases/limitations;
- disagreement rate where dual or human review is used.

A model SHOULD NOT be the sole judge of a critical security or authority property that can be verified deterministically.

## 13. Human evaluation

Human evaluation is required where usefulness, reviewability, nuanced correctness, or operational suitability cannot be adequately measured automatically.

Human-evaluation records SHOULD include:

- rubric version;
- reviewer role;
- blinded candidate identity where useful;
- outcome;
- rationale for material failures;
- conflict/adjudication mechanism;
- reviewer independence where required by policy.

Generated summaries may assist reviewers but may not replace required human decisions.

## 14. Pass criteria

Every suite MUST define explicit pass criteria before a candidate is evaluated for release promotion.

Criteria MAY include:

- minimum task-success rate;
- maximum unsupported-claim rate;
- maximum unauthorized-tool-call rate;
- maximum critical failure count;
- maximum cost per accepted task class;
- latency percentile bounds;
- minimum grounding/citation score;
- minimum human acceptance score;
- zero tolerance for specified T0 failures.

Numeric thresholds are policy/configuration data and SHOULD NOT be hard-coded in product logic unless a separate approved requirement requires it.

## 15. Release-blocking failures

The following are release-blocking for any operating profile in which they are applicable:

- cross-workspace data disclosure;
- secret disclosure;
- agent self-approval;
- protected effect without required approval;
- concealed provider/model substitution;
- silent fallback that weakens policy or data boundary;
- fabricated successful tool result used as authoritative state;
- critical prompt-injection authority takeover;
- retry that can duplicate an unknown consequential effect;
- material evidence/provenance fabrication;
- evaluation harness unable to establish actual candidate identity where identity is required by the qualification profile.

## 16. Comparative evaluation

Candidate promotion SHOULD compare against the current accepted baseline rather than only against absolute thresholds.

A comparison SHOULD report:

```text
capability delta
safety delta
grounding delta
tool-use delta
cost delta
latency delta
reliability delta
known-behavior changes
new failure modes
resolved failure modes
```

A cheaper or faster candidate does not automatically pass if it materially degrades safety or required capability.

## 17. Qualification profile

Qualification SHOULD be scoped, for example:

```yaml
qualification_profile:
  task_class: repository_analysis
  max_data_classification: internal
  allowed_tools:
    - repository.read
    - tests.run
  protected_effects: prohibited
  human_review: required_for_final_artifact
  model_profile: engineering_reasoning_v1
  context_profile: repo_analysis_v3
  adapter_profile: codex_restricted_v1
```

Qualification outside the declared profile is `unassessed` unless separately covered.

## 18. Qualification evidence package

A qualification decision SHOULD reference an immutable or content-addressed evidence package containing:

- evaluation object manifest;
- suite identifiers and versions;
- dataset/fixture versions;
- code/build identity;
- execution environment;
- provider/model actual identity state;
- context/prompt profile hashes;
- results by case and dimension;
- aggregate metrics;
- critical failures;
- cost/latency summary;
- human-review evidence where applicable;
- known limitations;
- exceptions;
- decision and reviewer identity.

`AUD-001` governs audit/evidence integrity.

## 19. Promotion gate

Recommended lifecycle:

```text
candidate discovered/configured
        ↓
compatibility and contract checks
        ↓
E0 deterministic harness checks
        ↓
behavioral eval suites
        ↓
security/adversarial evals
        ↓
cost/latency comparison
        ↓
human evaluation where required
        ↓
qualification decision
        ↓
limited rollout
        ↓
observability and incident feedback
        ↓
promote / restrict / regress / suspend
```

The lifecycle is coordinated with `MLC-001`.

## 20. Change-triggered re-evaluation

Re-evaluation SHOULD be triggered by a material change to any of:

- actual model or model snapshot/version;
- provider API behavior;
- model profile;
- system instruction;
- material prompt template;
- context assembly policy;
- retrieval/memory strategy;
- tool set or tool schema;
- adapter major/minor behavior relevant to execution;
- safety/policy profile;
- data classification rules;
- runtime behavior affecting outputs;
- incident or newly discovered failure mode.

A metadata-only change that cannot affect behavior need not invalidate qualification.

## 21. Continuous regression

Selected deterministic and bounded AI evals SHOULD run continuously or at defined release gates.

The regression portfolio SHOULD prioritize:

- critical golden cases;
- recent incidents;
- high-use task classes;
- high-cost task classes;
- security-sensitive agent behavior;
- model-routing/fallback behavior;
- newly changed context/prompt components.

Real-provider evaluations SHOULD remain bounded and opt-in where cost, availability, or data policy requires it.

## 22. Evaluation observability

Operational dashboards SHOULD be capable of distinguishing:

- evaluation result from production result;
- provider/model identity;
- suite version;
- qualification state;
- regression state;
- critical failure category;
- cost/latency trend;
- evidence freshness.

Production monitoring does not substitute for controlled evaluation, and controlled evaluation does not substitute for production monitoring.

## 23. Incident feedback loop

Confirmed AI incidents SHOULD create one or more of:

- sanitized regression case;
- new adversarial case;
- grading-rule update;
- qualification restriction;
- model/profile suspension;
- context/prompt change;
- policy/control change;
- new operational alert.

The incident itself MUST NOT be silently converted into training/evaluation data if data-use policy does not permit it.

## 24. Minimum MVP evaluation baseline

Before the first real external model binding is considered implementation-complete, Agent OS SHOULD have at minimum:

1. a deterministic simulator suite;
2. one capability suite for the first vertical-slice task class;
3. one authority/prompt-injection suite;
4. one tool-use suite if tools are exposed;
5. one unknown/partial/unavailable-state suite;
6. one usage/cost evidence suite;
7. model identity and no-silent-fallback checks;
8. repeat-run behavior measurement for the real model binding;
9. qualification evidence stored with the candidate version;
10. a documented decision: experimental, restricted, qualified, or rejected.

## 25. Governance and decision authority

- Product defines acceptable mission outcome and user-impact criteria.
- Architecture defines capability/profile compatibility and execution invariants.
- Security defines release-blocking abuse and authority failures.
- Data defines data-use and evaluation-dataset constraints.
- Operations defines operational cost/latency/reliability acceptance for supported environments.
- Quality owns evaluation methodology, evidence sufficiency, regression governance, and release-gate integration.

No AI agent may self-approve its own qualification for a critical capability.

## 26. Relationship to existing documents

- `TST-001`: broader system verification and test strategy.
- `QAG-001`: release gates and acceptance governance.
- `MOD-001`: logical model profile contract.
- `CTX-001`: context, instruction and prompt assembly.
- `MLC-001`: provider/model lifecycle and change management.
- `AUT-001` / `POL-001`: autonomy, authority and policy.
- `SEC-001` / `THR-001`: security requirements and threat model.
- `CST-001`: usage, price and budget evidence.
- `RUN-001` / `AUD-001`: execution and evidence lineage.

## 27. Review focus

Reviewers should specifically validate:

- whether qualification is correctly scoped to a complete AI configuration rather than a model name;
- which failure classes must be zero-tolerance for the MVP;
- which quantitative thresholds should be policy-configured later;
- what evidence must be persisted for repeatability and audit;
- where human evaluation is mandatory;
- how model-assisted judging may be used without becoming circular evidence;
- which suites must block the first external-provider vertical slice.
