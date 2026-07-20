---
document_id: CST-001
title: Agent OS Usage, Cost and Budget Architecture
version: 0.1.0
status: draft
register_status: proposed_unregistered
owner: product-owner
approvers:
  - product-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-07-20
last_reviewed: 2026-07-20
classification: internal
source_of_truth: false
dependencies:
  - MOD-001
  - RUN-001
  - POL-001
  - IAM-001
  - DAT-001
  - DAT-002
  - AUD-001
related_official_documents:
  - DOC-000
  - GLO-001
  - VSN-001
  - SCP-001
  - PER-001
  - UCD-001
  - PRD-001
  - SRS-001
  - NFR-001
  - AUT-001
  - RTM-001
  - SAD-001
  - C4-001
  - C4-002
  - DDD-001
  - DAT-001
  - DCT-001
  - MEM-001
  - ORC-001
  - INT-001
  - SEC-001
  - THR-001
  - AGC-001
  - CAP-001
  - MOD-001
  - RUN-001
  - APR-001
  - ART-001
  - API-001
  - EVT-001
  - DEV-001
  - TST-001
  - QAG-001
  - OBS-001
  - DEP-001
  - OPS-001
  - BCP-001
  - PLG-001
related_proposed_documents:
  - UXA-001
  - DSN-001
  - A11Y-001
  - VVR-001
  - IAM-001
  - POL-001
  - SAN-001
  - SEC-002
  - DAT-002
  - AUD-001
  - ADP-HER-001
  - ADP-CDX-001
related_adrs:
  - ADR-TBD-CST-001
  - ADR-TBD-CST-002
  - ADR-TBD-CST-003
  - ADR-TBD-CST-004
  - ADR-TBD-CST-005
  - ADR-TBD-CST-006
  - ADR-TBD-CST-007
  - ADR-TBD-CST-008
---

# CST-001 — Agent OS Usage, Cost and Budget Architecture

> **Status: Draft — proposed/unregistered.** This document defines the proposed usage, cost, pricing, reservation, budget, quota, threshold, approval, reconciliation, forecasting, anomaly, reporting, and evidence architecture for Agent OS. It covers model tokens and requests, tools, adapters, compute, sandbox resources, network, storage, artifacts, memory, external services, human review, internal allocation, provider invoices, credits, refunds, currencies, pricing versions, unknown costs, and release safeguards. It does not define final prices charged to customers, select a billing provider, provide tax or accounting advice, guarantee provider estimates, or treat unknown cost as zero.

## 1. Purpose

Agent OS can consume paid or limited resources through models, adapters, tools, sandboxes, compute, storage, networking, external APIs, human review, and operational support.

The architecture must answer:

1. what resource was consumed;
2. by which organization, workspace, project, run, step, attempt, agent, adapter, and user;
3. under which model, provider, tool, pricing version, and currency;
4. what was estimated before execution;
5. what amount was reserved;
6. what was actually measured;
7. what remains unknown or disputed;
8. which budget or quota was affected;
9. which threshold or approval applied;
10. how estimates and actuals were reconciled.

## 2. Objectives

The architecture must:

- attribute usage and cost to authoritative scopes;
- distinguish estimates, reservations, measurements, charges, invoices, and allocations;
- store pricing versions and effective periods;
- treat unknown cost explicitly;
- support pre-execution budget checks;
- reserve budget for consequential or long-running work;
- reconcile reservations with actual usage;
- support organization, workspace, project, run, user, agent, model, adapter, and cost-center views;
- support hard limits, soft limits, alerts, and approval thresholds;
- prevent cost-control bypass by agents or adapters;
- support retries, cancellations, partial effects, credits, and refunds;
- provide auditable cost evidence;
- protect sensitive commercial information;
- remain provider-neutral and billing-provider-neutral.

## 3. Non-goals

CST-001 does not:

- define final customer-facing product prices;
- define tax, revenue-recognition, invoicing, or accounting policy;
- guarantee that provider estimates equal invoices;
- assume token counts are the only cost source;
- permit agents to increase their own budgets;
- treat a provider acknowledgement as final billing evidence;
- select a payment gateway or subscription platform;
- convert currencies using an unversioned current rate;
- claim chargeback accuracy before reconciliation;
- replace provider contracts or finance review.

## 4. Principle — Unknown cost is not zero

Missing, delayed, unsupported, or disputed cost remains explicit and can block or approval-gate further execution.

## 5. Principle — Usage and cost are distinct

Measured usage, provider charge, internal allocation, and customer price are separate facts.

## 6. Principle — Estimate is not actual

Pre-execution estimates are bounded forecasts and never replace measured or invoiced actuals.

## 7. Principle — Reservation precedes risky consumption

Long-running or expensive actions reserve budget before execution where feasible.

## 8. Principle — Attribution follows the work

Every cost event carries organization, workspace, and operational lineage.

## 9. Principle — Pricing is versioned

Every calculation references an immutable pricing version and effective period.

## 10. Principle — Retries are separately attributable

Each attempt records its own usage, including failed or cancelled work.

## 11. Principle — Policy governs spend

Budget checks and approvals occur at authoritative enforcement boundaries.

## 12. Principle — Agents cannot self-fund

Agents, adapters, and tools cannot modify budgets, thresholds, prices, or approval requirements.

## 13. Principle — Reconciliation preserves differences

Estimate, reservation, measured actual, provider invoice, and correction remain separately visible.

## 14. Principle — Commercial data is protected

Provider rates, discounts, budgets, invoices, and unit economics receive restricted access.

## 15. Principle — Cost evidence is auditable

Material estimates, reservations, thresholds, approvals, actuals, and reconciliations produce evidence.

## 16. Cost bounded context

The Cost and Budget bounded context owns:

- usage definitions;
- usage measurements;
- pricing catalogues and versions;
- cost estimates;
- budget reservations;
- actual cost records;
- budget policies;
- quotas and thresholds;
- cost approvals;
- allocation rules;
- reconciliation;
- credits and adjustments;
- forecasts;
- anomaly findings;
- cost reports;
- cost evidence.

It does not own provider billing systems, customer payment collection, general ledger accounting, or authoritative run state.

## 17. Core distinction

```text
usage measurement
≠ cost estimate
≠ budget reservation
≠ calculated actual
≠ provider invoice line
≠ internal allocation
≠ customer charge
≠ payment
```

These records may be related but must not be collapsed.

## 18. Usage taxonomy

Primary usage classes:

```text
model_input_tokens
model_output_tokens
model_cached_tokens
model_requests
model_audio_seconds
model_image_units
model_video_units
tool_calls
external_api_units
sandbox_cpu_seconds
sandbox_memory_gb_seconds
sandbox_gpu_seconds
sandbox_disk_gb_hours
network_egress_bytes
storage_gb_days
artifact_processing_units
embedding_units
vector_index_units
human_review_minutes
support_minutes
build_minutes
test_minutes
provider_flat_fee
license_seat
other_metered_unit
```

## 19. Usage measurement

A usage measurement records:

- measurement ID;
- metric code;
- quantity;
- unit;
- source;
- observed time;
- period start/end;
- organization/workspace;
- project/task/run/step/attempt;
- principal, agent, adapter, model, provider, and tool where applicable;
- environment;
- classification;
- confidence and completeness;
- source receipt;
- correction relationship.

## 20. Usage source authority

Potential authoritative sources include:

- provider usage response;
- model gateway;
- Tool Gateway;
- sandbox executor;
- storage system;
- network proxy;
- artifact processor;
- human-review workflow;
- provider invoice;
- approved manual adjustment.

The source hierarchy is defined per metric.

## 21. Usage source precedence

Example:

```text
provider invoice line
→ authoritative for provider-billed amount

provider request receipt
→ authoritative for request-level reported units

gateway estimate
→ useful before final provider data, but not final actual

agent self-report
→ non-authoritative observation
```

## 22. Usage completeness

Usage completeness states:

```text
complete
complete_with_limitations
partial
estimated
delayed
conflicted
unsupported
unknown
```

A partial or unknown measurement cannot be presented as complete.

## 23. Usage correction

Corrections append a new record linked to the original. They record:

- corrected metric/quantity;
- reason;
- source;
- correcting actor;
- effective date;
- previous and new calculation impact;
- reconciliation effect.

The original measurement remains traceable.

## 24. Cost taxonomy

Cost categories:

```text
model_provider
tool_provider
external_api
compute
gpu
storage
network
artifact_processing
embedding_and_vector
build_and_ci
human_review
support
license
infrastructure_shared
security_and_compliance
backup_and_recovery
other_direct
other_allocated
```

## 25. Cost scope hierarchy

```text
platform
→ organization
→ workspace
→ project
→ task
→ run
→ step
→ attempt
→ tool/model/resource event
```

Costs may also be attributed to user, agent, adapter, provider, environment, cost center, product feature, and customer contract.

## 26. Cost event

A cost event records:

- cost-event ID;
- type;
- amount;
- currency;
- pricing version;
- usage measurement references;
- estimate/reservation/actual status;
- scope hierarchy;
- provider/tool/model;
- time and billing period;
- source;
- tax/discount treatment reference where applicable;
- confidence;
- evidence;
- correction/reconciliation.

## 27. Cost states

```text
estimated
reserved
accrued
measured
provider_reported
invoiced
allocated
reconciled
adjusted
credited
refunded
disputed
unknown
```

## 28. Estimate

A cost estimate is a pre-execution forecast based on:

- expected usage;
- model/tool selection;
- pricing version;
- context size;
- output limit;
- resource profile;
- duration;
- network/storage estimates;
- retries;
- uncertainty;
- currency;
- taxes/fees direction where relevant.

Estimates include lower, expected, and upper-bound values where uncertainty is material.

## 29. Estimate confidence

```text
high
medium
low
unknown
```

Confidence depends on historical data, provider pricing stability, request shape, runtime variability, and measurement support.

## 30. Estimate range

A structured estimate may contain:

```text
minimum
expected
maximum
currency
pricing_version
assumptions
confidence
expiry
```

An estimate without assumptions and pricing version is incomplete.

## 31. Estimate expiry

Estimates expire after:

- pricing change;
- model/provider change;
- task-scope change;
- prompt/context material change;
- output limit change;
- sandbox profile change;
- external destination/tool change;
- long elapsed time;
- currency-conversion change;
- budget-policy change.

## 32. Budget reservation

A reservation temporarily earmarks budget before consumption.

It records:

- reservation ID;
- budget;
- scope;
- estimated amount;
- upper bound;
- currency;
- pricing version;
- action fingerprint;
- owner;
- approval;
- issue and expiry;
- consumed amount;
- released amount;
- state.

## 33. Reservation states

```text
proposed
pending_approval
active
partially_consumed
fully_consumed
released
expired
cancelled
overrun
reconciliation_required
unknown
```

## 34. Reservation behavior

When an action starts:

- create or validate reservation;
- bind it to the exact run/action fingerprint;
- decrement available budget;
- track actual usage;
- prevent duplicate reservation consumption;
- release unused amount after completion/cancellation;
- reconcile overruns and unknowns.

A reservation is not a payment.

## 35. Reservation expiry

Expired reservations release unused budget unless an active run or protected effect requires reconciliation.

A stale run cannot retain budget indefinitely without renewal policy and evidence.

## 36. Reservation overrun

If actual cost exceeds reservation:

- record overrun;
- apply configured tolerance;
- stop, pause, approval-gate, or continue according to policy;
- alert owners;
- update forecast;
- preserve evidence;
- never rewrite the original reservation.

## 37. Actual cost

Calculated actual cost is derived from usage measurements and the applicable pricing version.

It remains distinct from provider-invoiced cost until reconciliation.

## 38. Provider-reported cost

Provider-reported cost may arrive:

- per request;
- daily;
- monthly;
- through usage API;
- through invoice;
- through account dashboard export.

Its scope and reliability must be recorded.

## 39. Provider invoice

An invoice line may contain:

- provider account;
- billing period;
- service;
- SKU;
- quantity;
- unit price;
- discount;
- tax/fee;
- amount;
- currency;
- credit;
- invoice reference;
- mapping status to Agent OS usage.

Invoice data is commercially restricted.

## 40. Reconciliation

Reconciliation compares:

```text
estimate
reservation
measured usage
calculated actual
provider-reported amount
invoice amount
internal allocation
```

Differences remain visible and are explained.

## 41. Reconciliation states

```text
not_started
matching
matched
matched_with_tolerance
variance_detected
partially_mapped
unmapped
disputed
adjusted
closed
unknown
```

## 42. Variance

A variance record includes:

- expected and actual values;
- absolute and percentage difference;
- currency;
- source records;
- cause category;
- owner;
- materiality;
- remediation;
- final disposition.

Typical causes include pricing drift, retries, provider rounding, discounts, taxes, delayed events, unsupported metrics, and incorrect mapping.

## 43. Tolerance

Tolerance may be defined by:

- absolute amount;
- percentage;
- metric;
- provider;
- cost category;
- environment;
- billing period.

Tolerance is not permission to ignore systematic variance.

## 44. Adjustments

Adjustments include:

- credit;
- refund;
- discount;
- write-off direction;
- manual correction;
- allocation change;
- provider dispute;
- waived internal charge.

Every adjustment has reason, authority, source, amount, currency, period, and evidence.

## 45. Credits and refunds

Credits and refunds remain separate from negative usage. They reference the provider/customer/accounting source and the cost records they offset.

A refund does not erase the original usage.

## 46. Pricing catalogue

The pricing catalogue records:

- provider/tool/service;
- SKU or metric;
- unit;
- price;
- currency;
- minimum/tiers;
- discounts;
- region/account;
- effective start/end;
- source;
- verification date;
- tax/fee treatment direction;
- owner;
- version.

## 47. Pricing version

Pricing versions are immutable. A price change creates a new version with:

- effective period;
- source evidence;
- changed rates;
- account/region scope;
- assumptions;
- reviewer;
- migration impact;
- estimate-expiry implications.

## 48. Pricing sources

Potential sources:

- provider contract;
- provider price sheet;
- API documentation;
- invoice;
- negotiated account schedule;
- internal infrastructure rate card;
- approved manual rate.

Source confidence and verification date are recorded.

## 49. Tiered pricing

Tiered pricing may depend on cumulative usage, volume, account, region, cache state, model class, or service tier.

The calculator must preserve the exact tier rules and billing period.

## 50. Discounts

Discounts are represented explicitly:

- contractual discount;
- committed-use discount;
- promotional credit;
- volume tier;
- internal subsidy;
- customer-specific price.

Discounts do not alter raw usage measurements.

## 51. Currency model

Each monetary record stores:

- amount;
- ISO-style currency code;
- native/source currency;
- converted amount where needed;
- conversion rate;
- rate source;
- rate date/time;
- conversion version;
- rounding rule.

No unversioned currency conversion is allowed.

## 52. Base and display currency

An organization may choose a reporting currency. Native provider amounts remain stored in their original currency.

Display conversion does not replace native amounts.

## 53. Rounding

Rounding rules are explicit by:

- currency;
- provider;
- invoice;
- report;
- budget;
- UI.

Internal calculations should preserve sufficient precision before final presentation.

## 54. Taxes and fees direction

Taxes, levies, payment fees, and withholding are outside the core MVP calculation unless explicitly configured.

They remain separate line types and require finance/legal review before customer-facing use.

## 55. Budget taxonomy

Budget scopes:

```text
platform_budget
organization_budget
workspace_budget
project_budget
feature_budget
user_budget
agent_budget
provider_budget
model_budget
tool_budget
environment_budget
cost_center_budget
run_budget
```

## 56. Budget record

A budget records:

- budget ID;
- scope and parent;
- owner;
- amount;
- currency;
- period;
- rollover rule;
- hard/soft behavior;
- thresholds;
- reservation policy;
- approval policy;
- allowed categories/providers/models;
- current state;
- effective version.

## 57. Budget periods

Potential periods:

```text
per_action
per_run
daily
weekly
monthly
quarterly
annual
contract_term
custom
```

Period boundaries use an explicit timezone and calendar rule.

## 58. Budget hierarchy

An action may be constrained by multiple budgets simultaneously.

Example:

```text
platform budget
AND organization budget
AND workspace budget
AND run budget
AND provider/model limit
```

The most restrictive current decision applies unless policy explicitly defines otherwise.

## 59. Soft and hard budgets

A soft budget triggers warnings or approval while allowing policy-governed continuation.

A hard budget blocks new consumption or selected protected effects.

Neither should silently interrupt work without clear state and recovery behavior.

## 60. Budget states

```text
draft
active
warning
approval_required
exhausted
suspended
expired
closed
overrun
unknown
```

## 61. Budget rollover

Rollover options:

```text
none
full
capped
percentage
manual
```

Rollover is explicit and versioned. Unused reservations are not automatically equivalent to rollover.

## 62. Quota taxonomy

Quotas may limit non-monetary resources:

- model requests;
- tokens;
- tool calls;
- concurrent runs;
- sandbox minutes;
- GPU seconds;
- storage;
- network egress;
- artifact count/size;
- human-review minutes;
- provider calls.

Quotas complement budgets.

## 63. Quota states

```text
available
approaching
reached
exceeded
suspended
reset_pending
unknown
```

## 64. Thresholds

Thresholds may be defined as:

- percentage of budget;
- absolute amount;
- rate of spend;
- forecasted exhaustion date;
- single-action amount;
- single-run amount;
- daily/provider anomaly;
- unknown-cost exposure.

Each threshold defines action, recipients, cooldown, and evidence.

## 65. Threshold actions

Potential actions:

```text
inform
warn
require_confirmation
require_approval
reduce_concurrency
select_lower_cost_profile
pause_new_runs
block_provider
block_external_effects
activate_cost_freeze
```

Automatic optimization must remain policy-governed and transparent.

## 66. Cost approval

Cost approval is required when an action exceeds a configured amount, uncertainty, rate, or category.

Approval binds to:

- estimated range;
- currency;
- pricing version;
- provider/model/tool;
- target;
- run/action fingerprint;
- upper limit;
- expiry;
- allowed overrun tolerance.

## 67. Cost-approval invalidation

Approval is invalidated by:

- material scope change;
- provider/model/tool change;
- estimate increase beyond tolerance;
- currency/pricing change;
- budget state change;
- expiration;
- policy change;
- previous consumption.

## 68. Unknown cost policy

Unknown cost may arise from:

- missing price;
- unsupported usage;
- delayed provider data;
- invoice-only service;
- ambiguous SKU;
- missing currency rate;
- failed meter;
- external human work;
- provider outage;
- conflicting sources.

Policy may block, cap, require approval, or allow a bounded experimental amount.

## 69. Unknown-cost exposure

Track:

- number of unknown-cost actions;
- estimated upper exposure;
- provider and workspace;
- age;
- reason;
- owner;
- reconciliation status.

Unknown exposure cannot disappear from reports merely because the actual amount is unavailable.

## 70. Cost freeze

An emergency cost freeze may block:

- new paid model calls;
- selected providers;
- high-cost tools;
- external API use;
- GPU execution;
- large exports;
- new sandboxes;
- nonessential background jobs.

It does not remove access to cost investigation, revocation, or emergency recovery.

## 71. Cost-freeze release

Release requires current authorization, reauthentication, reason, budget health, pricing availability, and evidence.

## 72. Attribution model

Each usage/cost event should identify where applicable:

- organization;
- workspace;
- project;
- task;
- run;
- step;
- attempt;
- user/principal;
- agent profile;
- adapter;
- model/provider;
- tool;
- environment;
- feature;
- cost center;
- customer/contract;
- tags.

## 73. Shared-cost allocation

Shared infrastructure costs may be allocated using:

- direct measurement;
- proportional usage;
- reserved capacity;
- equal split;
- weighted factors;
- approved manual allocation.

Allocation method and version are visible.

## 74. Allocation limitations

Internal allocation is not provider billing truth. Reports distinguish:

```text
direct cost
allocated shared cost
commercial price
margin analysis direction
```

## 75. Human-review cost

Human review may be measured by:

- scheduled time;
- active review time;
- approved time entry;
- case duration;
- fixed service unit.

Human cost data may be personal and commercially sensitive.

## 76. Run-level economics

A run may expose:

- estimated cost range;
- reserved amount;
- accrued cost;
- actual measured cost;
- invoice-reconciled cost;
- budget remaining;
- cost by step/attempt;
- cost by model/tool/provider;
- retries and wasted cost;
- unknown exposure;
- value/outcome tags where defined.

## 77. Retry cost

Retries are separately measured and classified:

- user-requested retry;
- automatic safe retry;
- provider retry;
- infrastructure retry;
- failed attempt;
- reconciliation retry.

This supports reliability and waste analysis.

## 78. Cancelled-run cost

Cancellation does not erase incurred usage. The run records:

- cost before cancellation;
- in-flight unknown exposure;
- released reservation;
- non-refundable provider charges;
- partial external effects;
- cleanup cost;
- reconciliation.

## 79. Failed-run cost

Failed attempts may still incur model, compute, network, tool, and human-review costs. Failure is not equivalent to zero cost.

## 80. Artifact and memory cost

Artifact processing and memory may incur:

- extraction;
- OCR;
- generation;
- validation;
- malware scanning;
- preview;
- storage;
- embeddings;
- vector indexing;
- retrieval;
- re-indexing;
- deletion/rebuild.

These costs follow artifact/memory lineage.

## 81. Sandbox cost

Sandbox cost may include:

- preparation;
- runtime CPU/memory/GPU;
- disk;
- network;
- package/cache;
- evidence collection;
- output validation;
- cleanup;
- failed execution;
- quarantined executor.

Profile and executor identity are recorded.

## 82. Storage cost

Storage usage considers:

- database;
- artifact store;
- audit evidence;
- backups;
- indexes;
- embeddings;
- logs;
- temporary exports;
- sandbox storage.

Retention changes can affect forecasted storage cost.

## 83. Network cost

Network cost distinguishes:

- ingress;
- egress;
- inter-region;
- external provider transfer;
- artifact download;
- backup transfer;
- proxy processing.

Classification and destination remain available for policy.

## 84. Model cost

Model cost records:

- provider;
- configured and actual model identity;
- input/output/cache units;
- multimodal units;
- request count;
- batch/priority tier;
- region/account;
- pricing version;
- fallback;
- provider receipt;
- estimate and actual.

## 85. Fallback cost

A fallback may change:

- model price;
- provider;
- region;
- context limits;
- output behavior;
- latency;
- data policy.

Material fallback triggers cost and policy re-evaluation.

## 86. Tool and external API cost

Tool pricing may be:

- per request;
- per successful result;
- per record;
- per minute;
- percentage-based;
- flat monthly;
- invoice only.

The charging trigger must be explicit.

## 87. Subscription and seat cost direction

Flat subscriptions and seats may be allocated to organizations, workspaces, users, or shared platform cost centers. Allocation is distinct from provider invoice.

## 88. Forecasting

Forecasts may project:

- period-end spend;
- exhaustion date;
- provider/model mix;
- workspace growth;
- storage growth;
- run pipeline;
- committed use;
- unknown-cost exposure;
- seasonal or release effects.

Forecasts expose assumptions and confidence.

## 89. Forecast states

```text
baseline
optimistic
expected
conservative
stress
unknown
```

## 90. Forecast limitations

Forecasts are not guarantees. They can be invalidated by pricing changes, new workloads, retries, provider outages, model fallback, retention growth, or contract changes.

## 91. Anomaly detection

Potential anomalies:

- sudden spend spike;
- unusual provider/model;
- excessive retries;
- high failed-run cost;
- missing usage;
- cost without run attribution;
- usage without price;
- invoice variance;
- budget bypass;
- abnormal network/storage growth;
- dormant account/service spending;
- unknown-cost growth.

## 92. Anomaly states

```text
detected
triaged
expected
false_positive
investigating
contained
resolved
unknown
```

## 93. Anomaly response

Depending on severity:

- notify;
- pause new consumption;
- require approval;
- activate cost freeze;
- revoke adapter/provider;
- inspect security incident;
- correct pricing or attribution;
- reconcile invoice;
- update forecast;
- preserve evidence.

## 94. Cost and security

Cost anomalies may indicate:

- credential compromise;
- runaway agent;
- malicious prompt;
- provider abuse;
- cryptomining or sandbox escape;
- duplicate external effects;
- logging/measurement failure;
- unauthorized workspace use.

Cost monitoring integrates with `SEC-002`.

## 95. Privacy and classification

Cost data may reveal:

- customer activity;
- employee productivity;
- project strategy;
- provider discounts;
- margins;
- infrastructure scale;
- model usage;
- sensitive incident or support activity.

Typical direction: `C2` for ordinary workspace cost, `C3` for provider pricing, contracts, invoices, margins, and security-related spend.

## 96. Retention

Usage and cost records use `DAT-002` profiles.

Possible direction:

- transient estimates/reservations: `R1` or `R2`;
- operational usage and actuals: `R2` or `R3`;
- provider invoices and contractual pricing: `R3`;
- approval and security-related cost evidence: `R4`;
- active disputes/holds: `R5`.

Final periods require business, finance, legal, and security review.

## 97. Deletion treatment

Deletion of a user, workspace, or provider configuration should:

- remove or minimize active profile details;
- preserve financial/audit attribution where required;
- detach personal display data where possible;
- retain stable historical scope IDs;
- remove unnecessary raw provider payloads;
- follow holds and contractual retention;
- preserve deletion evidence.

Deleting a workspace does not automatically erase required invoice or audit records.

## 98. Audit evidence

`AUD-001` should capture:

- estimate creation;
- pricing version;
- reservation;
- threshold result;
- cost approval;
- usage measurement;
- actual cost;
- invoice import;
- variance;
- adjustment;
- budget change;
- cost freeze;
- anomaly;
- reconciliation closure.

Raw provider credentials and unrestricted invoice content are excluded.

## 99. Policy integration

`POL-001` may return:

- permit;
- approval required;
- deny because budget exhausted;
- obligation to use a lower-cost model/profile;
- maximum allowed amount;
- reservation requirement;
- unknown-cost cap;
- cost freeze.

The Tool Gateway and execution boundary revalidate cost policy before protected spend.

## 100. IAM integration

`IAM-001` supplies budget owners, billing owners, workspace roles, cost reviewers, and approvers.

Agents, adapters, service accounts, and sandboxes cannot:

- increase budget;
- change prices;
- approve spend;
- waive variance;
- release cost freeze;
- hide cost records.

## 101. Run integration

`RUN-001` should reference:

- estimate;
- reservation;
- accrued cost;
- actuals;
- thresholds;
- approval;
- cost state;
- unknown exposure;
- reconciliation.

Cost state does not directly determine run success, but policy may block continuation.

## 102. Sandbox integration

`SAN-001` supplies resource measurements and enforces quota/cost obligations. The sandbox cannot self-report final cost without authoritative measurement and pricing.

## 103. Model-profile integration

`MOD-001` supplies configured and selected model profiles, actual identity, fallback, context limits, and provider route needed for pricing and cost evidence.

## 104. Adapter integration

Adapters declare:

- supported usage metrics;
- pricing source;
- provider receipts;
- estimate capability;
- actual-cost capability;
- currency;
- reconciliation limitations;
- fallback behavior.

Unsupported measurement remains explicit.

## 105. Hermes adapter direction

`ADP-HER-001` should define how Hermes exposes:

- model requests and token usage;
- tool calls;
- session duration;
- memory and retrieval usage;
- provider/model fallback;
- background or long-running activity;
- cancellation;
- unknown cost.

Hermes autonomy cannot bypass budget checks.

## 106. Codex adapter direction

`ADP-CDX-001` should define how Codex exposes:

- model usage;
- command/build/test time;
- sandbox resources;
- package/network usage;
- repository attempts;
- retries;
- Git effects;
- background work;
- provider receipts and unknowns.

Local file changes do not imply zero cost.

## 107. Cost user experience

Primary surfaces:

```text
budget overview
run estimate
reservation detail
cost approval
live accrued cost
usage explorer
provider/model breakdown
variance and reconciliation
anomaly investigation
pricing catalogue
budget administration
cost freeze
```

## 108. Estimate UX

Before expensive work, show:

- expected range;
- upper bound;
- currency;
- pricing version/time;
- assumptions;
- confidence;
- included/excluded categories;
- budget impact;
- approval requirement;
- expiry.

Do not display false precision.

## 109. Live cost UX

During execution, display:

- estimated;
- reserved;
- measured/accrued;
- unknown exposure;
- budget remaining;
- last update/freshness;
- threshold state;
- provider/model breakdown;
- pause/cancel implications.

A delayed meter is visibly stale.

## 110. Budget UX

Budget views should show:

- scope;
- owner;
- period;
- amount/currency;
- used;
- reserved;
- available;
- forecast;
- thresholds;
- hard/soft behavior;
- rollover;
- exceptions;
- last reconciliation.

## 111. Approval UX

Cost approval displays exact:

- action;
- provider/model/tool;
- target;
- estimated range;
- upper cap;
- currency;
- budget;
- reason;
- expiry;
- overrun tolerance;
- material assumptions.

Approval does not authorize unrelated actions or unlimited overrun.

## 112. Unknown-cost UX

Unknown cost is shown as a first-class state:

```text
Cost cannot currently be determined.
Known measured usage: ...
Unpriced or delayed components: ...
Maximum approved exposure: ...
Next reconciliation: ...
```

Never display `0.00` for unknown cost.

## 113. Variance UX

Variance detail shows:

- estimate;
- reservation;
- calculated actual;
- provider report;
- invoice;
- difference;
- causes;
- disputed items;
- adjustments;
- owner;
- resolution state.

## 114. Anomaly UX

An anomaly view shows:

- scope;
- expected baseline;
- observed amount/rate;
- confidence;
- possible causes;
- security correlation;
- current containment;
- affected budgets/runs;
- reviewer actions.

## 115. Accessibility requirements

Cost interfaces follow proposed/unregistered `A11Y-001`.

Requirements include:

- currency and numbers announced clearly;
- tables with semantic headers;
- charts with equivalent text/table;
- non-color-only thresholds;
- accessible approval dialogs;
- keyboard-operable filters;
- clear stale/unknown states;
- understandable rounding and units;
- no time limit without warning.

## 116. Visual validation

Proposed/unregistered `VVR-001` should cover:

- estimate high/medium/low confidence;
- reservation active/expired/overrun;
- budget normal/warning/exhausted/unknown;
- approval required;
- cost freeze;
- live stale meter;
- unknown cost;
- anomaly;
- variance;
- reconciliation;
- pricing change;
- mobile read-only view;
- dark theme and long currencies/amounts.

## 117. API direction

Potential resources:

```text
/usage-measurements
/cost-events
/cost-estimates
/budget-reservations
/budgets
/quotas
/cost-thresholds
/pricing-catalogues
/pricing-versions
/provider-invoices
/reconciliations
/cost-adjustments
/cost-anomalies
/cost-reports
```

## 118. Command API direction

Potential commands:

```text
estimate-cost
reserve-budget
extend-reservation
release-reservation
record-usage
calculate-actual
import-provider-invoice
reconcile-cost
record-adjustment
create-budget
update-budget
close-budget
request-cost-approval
activate-cost-freeze
release-cost-freeze
acknowledge-anomaly
resolve-anomaly
```

Clients cannot directly set reconciled, invoiced, approved, or confirmed cost states.

## 119. Events

Potential events:

```text
CostEstimated
CostEstimateExpired
BudgetReservationProposed
BudgetReservationActivated
BudgetReservationConsumed
BudgetReservationReleased
BudgetReservationOverrun
UsageMeasured
UsageCorrected
ActualCostCalculated
ProviderCostReported
ProviderInvoiceImported
CostVarianceDetected
CostReconciled
CostAdjusted
BudgetThresholdReached
BudgetExhausted
CostApprovalRequested
CostApprovalGranted
CostApprovalDenied
CostFreezeActivated
CostFreezeReleased
CostAnomalyDetected
CostAnomalyResolved
PricingVersionActivated
```

## 120. Data model direction

Core entities:

```text
UsageMetricDefinition
UsageMeasurement
UsageCorrection
CostCategory
CostEvent
CostEstimate
CostEstimateLine
Budget
BudgetVersion
BudgetReservation
Quota
Threshold
PricingCatalogue
PricingVersion
PricingRate
ProviderInvoice
ProviderInvoiceLine
CostReconciliation
CostVariance
CostAdjustment
CostApprovalReference
CostAnomaly
CostForecast
AllocationRule
CurrencyConversion
```

## 121. Consistency and transactions

Sensitive operations should use transactions or durable sagas:

- reservation activation plus budget availability;
- reservation consumption plus cost accrual;
- budget update plus version;
- threshold transition plus event;
- cost approval consumption;
- invoice import plus reconciliation queue;
- cost-freeze activation.

Partial outcomes remain explicit.

## 122. Idempotency

Usage ingestion, invoice import, reservation commands, provider receipts, and adjustments use idempotency keys.

Duplicate provider invoice lines or usage receipts must not double charge.

## 123. Ordering

Cost processing distinguishes event time, usage period, ingestion time, pricing effective time, invoice period, reconciliation time, and correction effective time.

Late usage updates historical actuals and forecasts without rewriting evidence.

## 124. Pricing-change handling

When a new price becomes effective:

- new estimates use the new version;
- existing approved/reserved actions follow explicit policy;
- stale estimates expire;
- active runs may be re-estimated;
- reports preserve historical pricing;
- invoice reconciliation uses the provider's actual billing period/version.

## 125. Meter outage

When a usage meter fails:

- mark affected cost as delayed/unknown;
- bound exposure where possible;
- block or approval-gate further spend;
- preserve raw provider references;
- alert;
- reconcile after recovery;
- never fabricate usage.

## 126. Pricing-service outage

Without current pricing:

- cached version may be used only within its validity and scope;
- unknown or expired price blocks protected high-cost execution;
- low-risk bounded execution requires explicit policy;
- user sees pricing uncertainty;
- no zero-cost assumption is permitted.

## 127. Budget-service outage

If current budget and reservations cannot be verified:

- new protected spend is blocked or cost-frozen;
- existing safe in-flight work follows explicit policy;
- reservations are not duplicated;
- reconciliation occurs after recovery.

## 128. Provider invoice delay

Delayed invoices leave provider-invoice state pending. Calculated actuals remain available but are not presented as fully reconciled.

## 129. Backup and restore

Back up pricing versions, budgets, reservations, usage measurements, cost events, invoices, reconciliations, adjustments, anomalies, and evidence references.

After restore:

- current budget versions are verified;
- expired reservations remain expired;
- consumed reservations remain consumed;
- cost freezes and disputes are reapplied;
- post-backup usage/invoices are reconciled;
- duplicate ingestion is prevented;
- reports indicate gaps.

## 130. Negative cost facts after restore

The following remain authoritative:

- exhausted/suspended budget;
- consumed approval;
- expired reservation;
- disputed invoice;
- cost freeze;
- unknown-cost exposure;
- unresolved variance;
- revoked pricing version;
- detected anomaly.

Restore cannot silently reset them.

## 131. Operational states

Cost service states:

```text
healthy
meter_delayed
pricing_stale
budget_read_only
reconciliation_backlog
invoice_pending
cost_freeze
recovery
unknown
```

## 132. Monitoring

Monitor:

- usage ingestion lag;
- unknown-cost amount;
- unpriced usage;
- reservation age;
- reservation overrun;
- budget consumption rate;
- threshold events;
- provider/model mix;
- failed/cancelled-run cost;
- invoice mapping rate;
- variance;
- pricing age;
- currency-rate age;
- duplicate events;
- cost-service health;
- anomaly volume.

## 133. Alerts

Potential alerts:

```text
budget_threshold_reached
budget_exhausted
reservation_overrun
reservation_stale
usage_meter_delayed
unpriced_usage_detected
unknown_cost_exposure_high
pricing_version_expired
invoice_variance_high
invoice_line_unmapped
cost_spike
failed_run_cost_spike
provider_mix_changed
cost_freeze_active
duplicate_usage_or_invoice
currency_rate_stale
```

## 134. Cost incidents

Critical cost incidents include:

- budget bypass;
- unauthorized budget change;
- runaway paid execution;
- credential abuse causing spend;
- duplicate provider effect;
- invoice double import;
- pricing tampering;
- cross-workspace cost leakage;
- hidden unknown cost;
- cost freeze failure;
- incorrect customer-facing charge direction.

## 135. Incident response

1. activate cost freeze or provider block;
2. identify affected scopes and credentials;
3. stop or pause unsafe consumption;
4. preserve usage, policy, approval, and provider evidence;
5. quantify known and unknown exposure;
6. revoke compromised access;
7. reconcile provider records;
8. correct pricing/attribution;
9. notify authorized owners;
10. complete root cause and control improvement.

## 136. Runbooks

Required runbooks:

```text
create and change budget
approve high-cost run
handle reservation overrun
release stale reservation
resolve unknown cost
import provider invoice
reconcile provider invoice
resolve invoice variance
activate cost freeze
release cost freeze
investigate cost anomaly
recover usage meter
recover pricing service
recover budget service
restore cost data
resolve duplicate usage or invoice
```

## 137. Testing strategy

Testing layers:

```text
metric schema
usage ingestion
pricing calculation
tiered pricing
currency conversion
estimate
reservation
budget hierarchy
thresholds
approval binding
actual-cost calculation
reconciliation
invoice import
adjustments
unknown cost
cost freeze
anomaly
workspace isolation
fault injection
security abuse
accessibility
visual regression
performance
backup/restore
```

## 138. Pricing tests

Test effective periods, account/region scope, tiers, discounts, cache pricing, multimodal units, flat fees, minimums, rounding, taxes/fees separation, expired price, conflicting price, and historical recalculation.

## 139. Estimate tests

Test prompt/context changes, output limits, model/provider fallback, sandbox duration, retries, uncertainty range, price change, currency change, expiry, and unknown components.

## 140. Reservation tests

Test creation, approval, insufficient budget, duplicate request, partial consumption, full consumption, cancellation, expiry, extension, overrun, stale run, rollback, and restore.

## 141. Budget tests

Test organization/workspace/project/run hierarchy, soft/hard limits, periods, timezone boundaries, rollover, thresholds, concurrent reservations, budget update, exhaustion, and access control.

## 142. Reconciliation tests

Test matched, tolerance, variance, partial mapping, unmapped invoice, credits, refunds, discounts, corrections, currency difference, late usage, provider rounding, and dispute.

## 143. Unknown-cost tests

Test missing pricing, unsupported metric, provider delay, meter failure, stale currency rate, ambiguous SKU, invoice-only service, and bounded experimental policy.

Verify unknown is never displayed or stored as zero.

## 144. Cross-workspace tests

For every usage, cost, budget, reservation, pricing override, invoice mapping, anomaly, report, and export API:

1. create records in workspace A;
2. authenticate a principal limited to workspace B;
3. attempt direct access, list, search, count, aggregation, chart, and export;
4. verify denial and no metadata leakage;
5. repeat with stale caches and forged IDs.

## 145. Security-abuse tests

Attempt to:

- change budget as an agent;
- spoof lower usage;
- inject a cheaper pricing version;
- reuse an approval;
- bypass reservation;
- duplicate invoice credits;
- suppress unknown cost;
- alter cost evidence;
- export provider pricing without permission;
- use another workspace's budget;
- release cost freeze without authority.

## 146. Fault-injection tests

Inject meter outage, pricing outage, budget-store outage, invoice parser failure, duplicate events, event reordering, clock skew, currency-rate absence, reconciliation crash, partial reservation consumption, and restore interruption.

## 147. Performance direction

Measure usage ingestion throughput, estimate latency, reservation contention, budget-check latency, report query time, invoice import, reconciliation backlog, forecast computation, and high-cardinality attribution.

Formal targets remain in `NFR-001`.

## 148. MVP scope

Recommended MVP:

- core model/tool/sandbox/storage usage metrics;
- immutable pricing versions;
- native currencies;
- estimates with expected and upper bound;
- run/workspace budgets;
- budget reservations;
- soft/hard thresholds;
- approval above configured amount;
- actual-cost calculation;
- explicit unknown cost;
- basic provider invoice import;
- reconciliation and variance;
- cost freeze;
- workspace/run/provider/model reports;
- audit evidence;
- no customer billing or tax engine claim.

## 149. Pilot readiness

Before pilot:

- all enabled paid providers have pricing sources;
- core usage metrics are tested;
- unknown-cost paths are visible;
- budgets and reservations enforce correctly;
- cost approval is bound to exact scope;
- retries/cancellations retain cost;
- provider invoice reconciliation works for the pilot account;
- cross-workspace cost isolation passes;
- cost freeze is exercised;
- alerts and runbooks exist;
- no critical cost-control defect remains.

## 150. Controlled-commercial direction

A controlled commercial profile may add:

- customer subscriptions and entitlements;
- customer-facing prices;
- tax and invoice integration;
- negotiated contract pricing;
- cost centers and chargeback;
- committed-use planning;
- margin reporting;
- payment collection;
- revenue and accounting exports;
- customer budget administrators;
- procurement evidence;
- external financial review.

These require finance, legal, tax, and accounting design.

## 151. Maturity stages

```text
C0 — informal provider dashboards and manual estimates
C1 — measured usage, pricing versions, run/workspace budgets
C2 — reservations, approvals, reconciliation, anomalies, cost freeze
C3 — customer allocation, contracts, chargeback, commercial reporting
C4 — mature FinOps and externally integrated billing programme
```

## 152. Requirement catalogue — Measurement and pricing

- `CST-REQ-MEA-001` — Every material paid or limited resource has a controlled usage metric.
- `CST-REQ-MEA-002` — Usage measurements record source, unit, scope, time, and completeness.
- `CST-REQ-MEA-003` — Pricing is immutable by version and effective period.
- `CST-REQ-MEA-004` — Every cost calculation references a pricing version.
- `CST-REQ-MEA-005` — Native provider currency is preserved.
- `CST-REQ-MEA-006` — Currency conversion records rate, source, date, and rounding.
- `CST-REQ-MEA-007` — Estimates declare assumptions, range, confidence, and expiry.
- `CST-REQ-MEA-008` — Unknown pricing or usage is not treated as zero.
- `CST-REQ-MEA-009` — Corrections append and preserve original measurements.
- `CST-REQ-MEA-010` — Provider invoice data remains distinct from calculated actual cost.
- `CST-REQ-MEA-011` — Model fallback triggers cost re-evaluation when material.
- `CST-REQ-MEA-012` — Usage and cost records preserve workspace attribution.

## 153. Requirement catalogue — Budgets, reservations, and approvals

- `CST-REQ-BUD-001` — Protected expensive actions perform current budget checks.
- `CST-REQ-BUD-002` — Long-running or high-cost actions reserve budget where feasible.
- `CST-REQ-BUD-003` — Reservations bind to exact action fingerprints.
- `CST-REQ-BUD-004` — Agents and adapters cannot modify budgets or approve spend.
- `CST-REQ-BUD-005` — Soft and hard budget behavior is explicit.
- `CST-REQ-BUD-006` — Multiple applicable budgets are evaluated together.
- `CST-REQ-BUD-007` — Temporary reservations expire and release unused amount.
- `CST-REQ-BUD-008` — Reservation overruns are visible and policy-governed.
- `CST-REQ-BUD-009` — Cost approvals bind to amount, currency, pricing version, target, and expiry.
- `CST-REQ-BUD-010` — Material estimate changes invalidate cost approval.
- `CST-REQ-BUD-011` — Cost freeze is restrictive, visible, and auditable.
- `CST-REQ-BUD-012` — Budget unknown state blocks unbounded protected spend.

## 154. Requirement catalogue — Actuals, reconciliation, and reporting

- `CST-REQ-REC-001` — Each attempt records its own usage and cost.
- `CST-REQ-REC-002` — Failed and cancelled work retains incurred cost.
- `CST-REQ-REC-003` — Actual calculated cost remains distinct from invoice cost.
- `CST-REQ-REC-004` — Reconciliation preserves estimate, reservation, actual, invoice, and variance.
- `CST-REQ-REC-005` — Duplicate usage or invoice records do not double charge.
- `CST-REQ-REC-006` — Credits and refunds do not erase original usage.
- `CST-REQ-REC-007` — Shared-cost allocation method is versioned and visible.
- `CST-REQ-REC-008` — Unknown-cost exposure appears in reports.
- `CST-REQ-REC-009` — Reports distinguish direct, allocated, and customer-price concepts.
- `CST-REQ-REC-010` — Late usage and invoices update reports without rewriting evidence.
- `CST-REQ-REC-011` — Material variance has owner and resolution.
- `CST-REQ-REC-012` — Reconciled status requires supporting evidence.

## 155. Requirement catalogue — Governance, security, and quality

- `CST-REQ-GOV-001` — Cost data access is workspace- and role-scoped.
- `CST-REQ-GOV-002` — Provider pricing, discounts, invoices, and margin data receive restricted classification.
- `CST-REQ-GOV-003` — Cost changes and approvals are audited.
- `CST-REQ-GOV-004` — Cost anomalies integrate with security response.
- `CST-REQ-GOV-005` — Cross-workspace cost aggregation is denied by default.
- `CST-REQ-GOV-006` — Cost-service outages do not silently fail open.
- `CST-REQ-GOV-007` — Restore preserves exhausted budgets, consumed reservations, freezes, and disputes.
- `CST-REQ-GOV-008` — Critical cost paths receive fault-injection and abuse tests.
- `CST-REQ-GOV-009` — Cost interfaces are accessible.
- `CST-REQ-GOV-010` — Cost visual states receive regression validation.
- `CST-REQ-GOV-011` — Critical cost-control failures block pilot and release.
- `CST-REQ-GOV-012` — Commercial billing claims require finance/legal/accounting approval.

## 156. Traceability

| Source | CST-001 response |
|---|---|
| `MOD-001` | Model/provider identity, routes, limits, fallback, and usage units |
| `RUN-001` | Run/step/attempt attribution, retries, cancellation, and completion |
| `POL-001` | Budget decisions, thresholds, approvals, obligations, and cost freeze |
| `IAM-001` | Budget owners, billing roles, approvers, and workspace access |
| `SAN-001` | Compute, network, storage, tool, and sandbox resource measurements |
| `DAT-001` | Cost-system records, lineage, stores, and reporting |
| `DAT-002` | Classification, retention, deletion, invoices, and financial evidence |
| `AUD-001` | Estimates, reservations, approvals, actuals, invoices, reconciliation, and anomaly evidence |
| `SEC-002` | Cost abuse, budget bypass, anomaly, credential, and recovery controls |
| `AGC-001` | Adapter usage and receipt contract |
| `CAP-001` | Resource/cost capability declarations |
| `API-001` | Cost resources and commands |
| `EVT-001` | Usage, cost, budget, threshold, and reconciliation events |
| `OBS-001` | Spend metrics, freshness, alerts, and dashboards |
| `OPS-001` | Cost runbooks, incidents, recovery, and provider operations |
| `BCP-001` | Cost-data backup, restore, and post-restore reconciliation |

## 157. ADR-TBD-CST-001 — Usage metric and cost-event model

Approve metric taxonomy, source authority, completeness, corrections, scope hierarchy, and cost-state vocabulary.

## 158. ADR-TBD-CST-002 — Pricing catalogue and currency architecture

Define pricing sources, versions, tiers, discounts, currencies, conversions, rounding, tax/fee separation, and verification.

## 159. ADR-TBD-CST-003 — Estimation and reservation model

Define estimate ranges, confidence, expiry, reservation lifecycle, upper bounds, concurrency, overrun, and release.

## 160. ADR-TBD-CST-004 — Budget, quota, threshold, and approval policy

Define hierarchy, hard/soft behavior, periods, rollover, thresholds, cost approvals, unknown-cost caps, and freeze.

## 161. ADR-TBD-CST-005 — Actual-cost and provider-invoice reconciliation

Define provider imports, invoice mapping, tolerances, variance, corrections, credits, refunds, disputes, and closure.

## 162. ADR-TBD-CST-006 — Attribution, allocation, and reporting

Define organization/workspace/project/run attribution, shared-cost allocation, cost centers, human review, and report access.

## 163. ADR-TBD-CST-007 — Cost observability, anomaly, and recovery

Define freshness, anomalies, security correlation, alerts, outages, backup, restore, and negative-fact reapplication.

## 164. ADR-TBD-CST-008 — Commercial billing and finance boundary

Define future subscriptions, entitlements, customer pricing, invoicing, tax, accounting, payment, margin, and finance approvals.

## 165. Open decisions

1. Confirm `CST-001` registration.
2. Approve usage metrics and source authority.
3. Define initial provider/model/tool pricing catalogue.
4. Approve pricing-version format and verification cadence.
5. Define currency and conversion rules.
6. Define estimate range and confidence model.
7. Define reservation thresholds and expiry.
8. Define run, workspace, organization, provider, and model budgets.
9. Define hard versus soft budget behavior.
10. Define quota types and reset periods.
11. Define threshold actions and recipients.
12. Define cost-approval thresholds and overrun tolerance.
13. Define unknown-cost caps.
14. Define cost-freeze authority and release.
15. Define provider invoice import formats.
16. Define reconciliation tolerances and variance ownership.
17. Define credits, refunds, and adjustment authority.
18. Define shared-cost allocation methods.
19. Define forecast assumptions and confidence.
20. Define cost anomaly model and security integration.
21. Define retention and deletion periods.
22. Define provider pricing/invoice access controls.
23. Confirm accessibility and visual scenarios.
24. Confirm Hermes and Codex usage mappings.
25. Decide when commercial billing becomes a separate controlled document.

## 166. Risks

| Risk | Consequence | Response |
|---|---|---|
| Unknown cost displayed as zero | Uncontrolled spend | Explicit unknown |
| Estimate shown as guaranteed | Misleading decision | Range/confidence |
| Price changes without version | Wrong actuals | Immutable pricing |
| Agent raises its own budget | Autonomy abuse | Human-only IAM/policy |
| Reservation consumed twice | Budget distortion | Idempotency |
| Retry cost hidden | Waste and bad forecast | Attempt attribution |
| Cancelled run shown free | Underreported spend | Preserve actuals |
| Provider invoice double import | Duplicate cost | Invoice idempotency |
| Invoice treated as usage truth | Lost operational detail | Separate records |
| Currency conversion unversioned | Inconsistent reports | Rate version |
| Shared cost allocation hidden | Misleading unit economics | Visible method |
| Cost data leaks provider discount | Commercial harm | C3 access |
| Cost anomaly ignored | Credential abuse/runaway agent | Security correlation |
| Meter outage fails open | Unknown exposure | Cap/freeze/approval |
| Budget outage loses reservations | Overspend | Durable transactions |
| Restore revives expired reservation | False available budget | Negative facts |
| Model fallback changes price silently | Budget overrun | Re-evaluation |
| Billing scope introduced prematurely | Architecture complexity | Separate maturity |
| Tax/accounting assumptions embedded | Compliance error | Finance/legal review |
| Cost controls make UX opaque | User distrust | Clear estimate/status |

## 167. Assumptions

- Model Gateway, Tool Gateway, sandbox, storage, and adapters can emit usage measurements.
- Pricing can be represented by immutable versions.
- Workspace and run attribution are available.
- Budgets and reservations can use durable transactional state.
- Provider invoice data can be imported at least manually for pilot reconciliation.
- Cost evidence can be retained without raw credentials.
- Customer billing can remain outside the initial MVP.
- Finance, legal, tax, and accounting review will precede commercial billing claims.

## 168. Constraints

- unknown cost is never zero;
- no agent, adapter, service account, or sandbox may alter budget or approve spend;
- no cost calculation without pricing version;
- no unversioned currency conversion;
- no hidden retry, failed-run, or cancelled-run cost;
- no duplicate usage or invoice charging;
- no cross-workspace cost access or aggregation without authority;
- no final customer price, tax, invoice, or accounting policy in this draft;
- no unsupported reconciliation claim;
- no raw provider credentials in cost evidence;
- no Git commit, push, PR, merge, or deployment during current documentation drafting.

## 169. Acceptance criteria

CST-001 may advance to `1.0.0` when:

1. it is formally added to the document register;
2. Product accepts estimates, budgets, approvals, reports, anomalies, and user-facing limitations;
3. Architecture accepts measurement, pricing, reservation, budget, reconciliation, and reporting boundaries;
4. Security accepts budget authority, cost freeze, anomaly, data access, and abuse controls;
5. Data accepts attribution, classification, retention, deletion, invoice, and lineage treatment;
6. Operations accepts meters, provider imports, outages, alerts, runbooks, backup, and restore;
7. Quality accepts pricing, reservation, reconciliation, cross-workspace, fault-injection, accessibility, and visual tests;
8. initial usage metrics and pricing sources are approved;
9. budgets, quotas, thresholds, and approvals are approved;
10. unknown-cost policy and cost freeze are approved;
11. provider invoice reconciliation is approved;
12. currency, rounding, and adjustment rules are approved;
13. audit evidence and retention are approved;
14. Hermes and Codex usage mappings are accepted;
15. commercial billing remains explicitly separated until finance/legal/accounting design is approved.

## 170. Downstream impact

| Document | Required use |
|---|---|
| `ADP-HER-001` | Hermes model, tool, memory, session, retry, provider, and unknown-cost measurements |
| `ADP-CDX-001` | Codex model, command, build, test, sandbox, package, network, Git, and retry measurements |
| `SEC-002` | Cost-abuse, budget, quota, anomaly, and recovery controls |
| `DAT-002` | Cost/invoice classification, retention, deletion, and provider-data lifecycle |
| `AUD-001` | Estimate, reservation, approval, actual, invoice, reconciliation, anomaly, and freeze evidence |
| `UXA-001` | Estimate, approval, live cost, budget, variance, anomaly, and freeze journeys |
| `DSN-001` | Cost states, badges, tables, charts, warnings, and approvals |
| `A11Y-001` | Accessible numeric, chart, currency, budget, and approval interactions |
| `VVR-001` | Cost/budget visual scenarios and regression baselines |
| Document register | Add proposed document and dependencies |

## 171. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial usage, cost, pricing, reservation, budget, quota, threshold, approval, reconciliation, forecasting, anomaly, reporting, evidence, recovery, and commercial-boundary architecture |

## 172. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `MOD-001` — Model Profile Contract
- `RUN-001` — Run and Execution Contract
- `IAM-001` — Identity and Access Management Architecture — proposed/unregistered
- `POL-001` — Policy and Permission Architecture — proposed/unregistered
- `SAN-001` — Sandbox and Secure Execution Architecture — proposed/unregistered
- `SEC-002` — Security Control Catalogue — proposed/unregistered
- `DAT-002` — Data Classification, Retention and Deletion Standard — proposed/unregistered
- `AUD-001` — Audit and Evidence Architecture — proposed/unregistered
- `API-001` — API Specification
- `EVT-001` — Event Catalog and Async Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `BCP-001` — Business Continuity and Disaster Recovery Plan
