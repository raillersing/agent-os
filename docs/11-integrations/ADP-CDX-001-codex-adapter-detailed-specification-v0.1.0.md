---
document_id: ADP-CDX-001
title: Agent OS Codex Adapter Detailed Specification
version: 0.1.0
status: draft
register_status: proposed_unregistered
owner: architecture-owner
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
related_documents: []
dependencies:
  - AGC-001
  - CAP-001
  - MOD-001
  - RUN-001
  - APR-001
  - ART-001
  - ORC-001
  - INT-001
  - POL-001
  - SAN-001
  - SEC-002
  - DAT-002
  - AUD-001
  - CST-001
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
  - CST-001
  - ADP-HER-001
  - PRI-001
  - MCP-001
  - HUM-001
  - FIN-001
  - UIF-001
  - SLO-001
  - IRP-001
  - REL-001
related_adrs:
  - ADR-TBD-CDX-001
  - ADR-TBD-CDX-002
  - ADR-TBD-CDX-003
  - ADR-TBD-CDX-004
  - ADR-TBD-CDX-005
  - ADR-TBD-CDX-006
  - ADR-TBD-CDX-007
  - ADR-TBD-CDX-008
---

# ADP-CDX-001 — Agent OS Codex Adapter Detailed Specification

> **Status: Draft — proposed/unregistered.** This document defines the proposed adapter contract between Agent OS and a Codex-family coding-agent runtime. It covers discovery, authentication, runtime modes, repositories, worktrees, tasks, commands, patches, files, builds, tests, packages, model observations, approvals, sandboxing, Git effects, cloud/local execution, events, costs, evidence, cancellation, recovery, security, compatibility, and conformance testing. It does not assume one stable Codex API, allow Codex to bypass Agent OS governance, grant remote Git authority from local repository access, or select a final OpenAI account, SDK, CLI, desktop, IDE, web, cloud-task, or transport integration.

## Official product grounding — non-normative

As of the document date, official OpenAI materials describe Codex as a coding agent that can work with repositories and local development tools, modify files, run commands and tests, and support delegated cloud work in isolated environments. Official materials also describe multiple client surfaces and packaged capabilities such as plugins or skills.

These observations inform adapter scenarios but are not normative contracts. Agent OS must feature-detect, version-negotiate, and preserve `unsupported` or `unknown` when a specific Codex runtime does not expose a required interface.

## 1. Purpose

The adapter enables Agent OS to orchestrate Codex for governed software-development work while preserving Agent OS authority over identity, repository scope, policy, approvals, sandboxes, costs, artifacts, Git effects, evidence, and release decisions.

It translates between Agent OS workspaces, repositories, tasks, runs, attempts, approvals, artifacts, budgets, and evidence, and Codex execution contexts, repository changes, commands, tests, reviews, and runtime states.

## 2. Objectives

The adapter must:

- identify the exact Codex runtime/client and version;
- declare and validate capabilities;
- distinguish local, desktop, IDE, CLI, SDK, review, remote, and cloud modes where exposed;
- prepare repositories and attempt-specific worktrees safely;
- capture proposed and applied file changes;
- mediate commands, packages, network, secrets, and protected tools;
- separate local edits, commits, pushes, pull requests, merges, releases, and deployments;
- expose model identity and usage where available;
- preserve approvals and repository/branch scope;
- support cancellation, retries, and effect reconciliation;
- produce diffs, tests, artifacts, receipts, cost records, and audit evidence;
- fail closed when identity, repository, approval, or remote-effect state is unknown.

## 3. Non-goals

This specification does not make Codex the control plane, assume a universal Codex API, expose reusable human credentials, grant unrestricted shell/filesystem/network/Git access, permit self-approval, equate test success with acceptance, or guarantee deterministic output and lossless resume.

## 4. Principle — Agent OS remains authoritative

Codex proposes and executes within a governed envelope; Agent OS owns permissions, approvals, run state, artifact acceptance, and release decisions.

## 5. Principle — Repository scope is exact

Every task binds to a repository identity, base revision, branch/worktree, and allowed paths.

## 6. Principle — Git effects are separated

Read, edit, stage, commit, push, PR, merge, tag, release, and deploy are distinct capabilities.

## 7. Principle — One attempt, one change context

Retries preserve prior diffs, commands, tests, costs, and effects.

## 8. Principle — Commands are governed

A coding-task label never grants arbitrary shell or network authority.

## 9. Principle — Diff is the review unit

Material approval binds to the exact repository, base, paths, content, generated files, and requested effect.

## 10. Principle — Tests are evidence

Passing tests support confidence but do not prove requirements, security, UX, or readiness.

## 11. Principle — Remote effects require receipts

Push, PR, merge, release, and deployment need target-specific evidence.

## 12. Principle — Unknown effect blocks blind retry

Ambiguous remote outcomes are reconciled before repetition.

## 13. Principle — Secrets remain brokered

Codex receives references or purpose-bound channels rather than broad credentials.

## 14. Principle — Runtime differences are explicit

Local and cloud modes have different identities, storage, network, and evidence.

## 15. Principle — No silent fallback

Material runtime, model, repository, or mode changes trigger re-evaluation.

## 16. Bounded context

The Codex adapter owns runtime discovery, registration, capability translation, repository preparation requests, command/event translation, patch/diff normalization, test-result normalization, Git-effect mapping, usage observations, health, compatibility, recovery, and adapter evidence.

It does not own repository authorization, policy, approvals, artifact acceptance, provider truth, or deployment authority.

## 17. Logical topology

```text
Agent OS Orchestrator
→ Codex Adapter
→ selected Codex runtime/client
→ model/runtime execution
```

Protected effects:

```text
Codex proposal
→ Adapter normalization
→ Policy and Approval
→ Sandbox / Repository Gateway / Tool Gateway
→ filesystem, Git provider, CI, or deployment target
→ receipt and evidence
```

## 18. Integration modes

Potential modes:

```text
codex_cli_local
codex_desktop_local
codex_ide_local
codex_sdk_embedded
codex_remote_task
codex_cloud_task
codex_review_integration
```

A concrete release may support only one or two modes.

## 19. Mode-specific contract

Each mode declares runtime identity, source-code location, repository credentials, filesystem boundary, network policy, secret mechanism, persistence, cancellation, event delivery, usage/cost source, result model, and known limitations.

## 20. Runtime registration

A registration records runtime ID, client type, version/build, adapter version, OS/environment, local/remote/cloud mode, transport, authentication mode, repository-provider support, capabilities, sandbox observations, model support, event support, owner, validation date, health, and quarantine.

## 21. Identity separation

The Codex process or service identity remains distinct from:

- requesting human;
- Agent OS service;
- logical agent profile;
- sandbox workload;
- repository installation/token;
- CI/deployment identity.

Audit preserves the complete actor chain.

## 22. Registration states

```text
discovered
proposed
registered
authenticated
validated
enabled
ready
degraded
disabled
suspended
quarantined
revoked
retired
unknown
```

## 23. Handshake direction

Where a programmatic interface exists, handshake exchanges protocol version, runtime/client identity, schema versions, capabilities, execution modes, repository features, command/patch support, model observation, streaming, approval/cancellation, usage support, limitations, and integrity metadata.

For non-programmatic clients, a controlled wrapper may synthesize this manifest from validated configuration and runtime probes.

## 24. Authentication modes

Potential modes:

```text
local_process_identity
local_user_session_with_explicit_delegation
OpenAI_account_session_reference
API_credential_reference
workload_identity
mutual_TLS
short_lived_adapter_token
repository_provider_installation
```

Final selection requires ADR and current product verification.

## 25. Human-session protection

A reusable Codex/OpenAI human-session credential must not be copied into a sandbox or unrelated adapter process. Delegated local-session use records the real human and limits effective workspace/system authority.

## 26. Capability manifest

Potential capabilities:

```text
repository.read
repository.explain
filesystem.read
filesystem.modify
patch.propose
patch.apply
command.propose
command.execute
build.execute
test.execute
lint.execute
format.execute
dependency.inspect
dependency.install
git.diff
git.stage
git.commit
git.push
pull_request.review
pull_request.create
pull_request.update
branch.create
branch.merge
tag.create
release.create
deployment.trigger
artifact.generate
stream.output
task.resume
usage.report
```

## 27. Capability fields

Each capability declares code/version, supported modes, schemas, side-effect class, repository/filesystem/network/secret needs, compatible sandbox profiles, approval expectation, idempotency, cancellation, evidence, usage metrics, and limitations.

## 28. Capability validation

Validation uses controlled repository fixtures, positive and negative tests, path/workspace isolation, command/network tests, Git boundaries, cancellation, diff normalization, test-result parsing, evidence, usage, and compatibility review.

## 29. Capability states

```text
declared
validated
enabled
ready
degraded
unsupported
incompatible
revoked
unknown
```

## 30. Capability drift

Drift includes runtime version change, approval-mode change, sandbox behavior change, event/schema change, model change, Git integration change, plugin/skill change, lost cancellation, or lost evidence.

Affected capabilities are suspended pending revalidation.

## 31. Runtime approval-mode normalization

Codex client automation or approval modes are runtime controls, not authoritative Agent OS permission.

Effective authority is:

```text
Agent OS policy and approval
AND sandbox/tool/repository enforcement
AND Codex runtime mode
```

## 32. Plugin and skill governance

Codex plugins, skills, reusable instructions, or app-backed capabilities are versioned extension dependencies with source, publisher, permissions, data handling, app dependencies, workspace enablement, security validation, revocation, and evidence.

A skill prompt cannot grant authority.

## 33. Agent profile mapping

A Codex agent profile may specify runtime mode, work categories, model profile, repository permissions, command policy, package/network policy, Git policy, approvals, sandbox profile, budget, skills/plugins, owner, and version.

## 34. Task categories

```text
codebase_explanation
architecture_analysis
bug_investigation
feature_implementation
refactoring
test_generation
test_execution
documentation_change
dependency_update
security_review
pull_request_review
migration
build_fix
performance_analysis
release_preparation
```

Task category informs controls but never grants authority.

## 35. Repository identity

A repository reference includes provider/host, owner/organization, name, immutable provider ID where available, canonical remote, default branch, workspace, classification, authorized installation/account, fork/mirror state, and verification time.

## 36. Repository authorization

Authorization precedes clone/fetch, path listing, file read, search, branch listing, history, diff, issue/PR access, commands, write, and remote effects.

Repository metadata is protected.

## 37. Repository preparation

Preparation verifies exact repository, provider/account, base revision, branch, dirty state, submodules, large-file handling, path restrictions, required tools, dependency policy, runtime profile, writable scope, and remote-effect permissions.

## 38. Attempt-specific worktree

Recommended direction:

```text
authoritative repository
→ verified base commit
→ attempt-specific worktree or clone
→ Codex execution
→ diff and evidence
→ governed persistence or disposal
```

Unrelated user working trees are not edited by default.

## 39. Dirty working tree

Detect modified, staged, untracked, ignored, and conflicted files. Distinguish pre-existing changes, avoid overwrite, require user choice or isolated snapshot, record baseline, and never claim ownership of pre-existing work.

## 40. Base revision

Every coding attempt binds to an immutable base commit or snapshot. A moving branch name alone is insufficient for reproducibility and approval.

## 41. Branch strategy

Potential strategies:

```text
existing_branch_read_only
attempt_branch
temporary_worktree_branch
user_selected_branch
provider_managed_task_branch
detached_snapshot
```

Branch creation does not imply push permission.

## 42. Allowed and excluded paths

Path scope may cover the full repository or selected directories/files. Typical exclusions include secrets, environment files, production data, build caches, large binaries, unrelated workspaces, deployment keys, and host system paths.

Enforcement occurs outside prompt text.

## 43. Symlinks, submodules, and nested repositories

Preparation validates symlinks, submodules, worktrees, nested repositories, LFS pointers, vendored dependencies, and generated paths to prevent scope escape or unintended remote access.

## 44. Repository snapshot evidence

Record repository ID, canonical remote, base commit, branch, worktree reference, dirty-state summary, submodule commits, path policy, snapshot hash where applicable, and preparation result.

## 45. Task-to-execution mapping

Recommended MVP mapping:

```text
one Agent OS attempt
→ one isolated Codex execution context
→ one repository worktree or snapshot
```

Long tasks may use multiple governed steps while preserving attempt lineage.

## 46. Execution context

An execution context contains run/step/attempt, runtime/client, repository/worktree, base, task instruction, selected context, model profile, command policy, package/network policy, Git policy, approvals, budget, timeout, outputs, and cancellation reference.

## 47. Context minimization

Supply only relevant repository content, specifications, screenshots, and artifacts. Avoid whole-repository dumps, unrelated history, credentials, personal files, other workspaces, production data, and unrestricted environment variables.

## 48. Instruction hierarchy

Repository files, issues, PR descriptions, comments, generated code, package metadata, and web content are untrusted. They cannot change identity, workspace, permission, approval, sandbox, network, secret, evidence, budget, or Git authority.

## 49. Context fingerprints

Consequential attempts record fingerprints of task snapshot, selected repository context, model profile, skill/plugin set, command/tool policy, and output contract without retaining unrestricted content by default.

## 50. Execution lifecycle

```text
proposed
preparing_repository
prepared
starting
running
waiting_for_command_approval
waiting_for_git_approval
waiting_for_external_approval
streaming
cancelling
stopped
collecting_changes
validating
completed_candidate
failed
lost
effect_unknown
reconciliation_required
```

## 51. Execution request

The request includes repository/base, task/run/attempt, instruction, relevant files/artifacts, model, capabilities, path policy, command policy, package/network policy, Git policy, approvals, cost reservation, timeouts, and evidence requirements.

## 52. Execution response

The runtime may return progress, questions, plan, proposed command, proposed patch, applied changes, tests/builds, findings, artifacts, Git proposals/effects, usage, completion candidate, errors, and cancellation state.

The adapter normalizes these and never directly completes the Agent OS run.

## 53. Clarification questions

Record the question, reason, blocking status, context, response, responder, and resulting scope change. Material answers may invalidate approvals or estimates.

## 54. Plan proposal

A plan may include files, commands, tests, dependencies, migrations, risks, Git operations, artifacts, estimate, and approvals. Agent OS validates and versions material plan changes.

## File-read mediation

File reads are limited to authorized repository/workspace paths. Sensitive or excluded files may be omitted, redacted, or represented by metadata. Out-of-scope reads are denied and audited.

## File-write mediation

Writes are allowed only in declared writable paths and the attempt worktree.

The adapter records created, modified, deleted, renamed, mode-changed, binary, generated, and unexpected files.

## Patch proposal

A patch proposal contains base revision, affected paths, hunks or patch representation, binary/rename metadata, generated-file markers, rationale, expected tests, content hash, and runtime/model references.

## Patch versus applied change

```text
patch proposed
≠ patch applied
≠ working tree validated
≠ commit created
≠ push completed
```

Each transition has separate evidence.

## Patch application

Patch application validates base compatibility, allowed paths, conflicts, file size/type, symlink safety, encoding, generated-file policy, secret detection, and resulting hashes.

Partial application remains explicit.

## Direct file editing

When Codex edits files directly, the adapter reconstructs the complete diff against the exact baseline, including untracked and deleted files.

## Binary and large-file changes

Binary and large-file changes require explicit capability, limits, hashes, metadata, safe preview, and review. Unbounded binary generation is denied.

## Generated files

Generated outputs record generator, source command, input references, reproducibility, expected paths, and review policy. Generated status never bypasses review.

## Normalized diff

The normalized diff captures:

- base/head or before/after hashes;
- path status;
- text hunks;
- binary metadata;
- mode changes;
- renames;
- submodule changes;
- generated-file markers;
- secret-scan result;
- size/count.

Secrets are redacted from display and audit.

## Diff fingerprint

Material approval binds to repository, base commit, branch, all path changes, normalized content, generated files, lockfiles, migrations, and requested Git effect.

Any material change invalidates approval.

## Diff review states

```text
unreviewed
review_required
review_in_progress
changes_requested
approved_for_local_persistence
approved_for_commit
approved_for_push
approved_for_pull_request
rejected
superseded
unknown
```

## Command proposal

A command proposal contains executable, structured arguments, working directory, environment allowlist, purpose, expected outputs, side-effect class, timeout, network/secret needs, resource estimate, approval need, and evidence expectation.

## Command classes

```text
read_only_inspection
format_or_lint
build
unit_test
integration_test
migration_check
code_generation
dependency_install
repository_mutation
service_start
networked_tool
deployment_or_release
other_protected
```

## Command approval

Approval considers command class, executable/arguments, repository/path, sandbox, network, secret, expected writes, cost, target environment, and reversibility.

It binds to the command fingerprint.

## Structured execution

Prefer executable plus argument arrays. Shell evaluation is allowed only through a governed shell capability with fixed interpreter, controlled PATH, safe quoting, bounded environment, timeout, and evidence.

## Command evidence

Record command ID, redacted executable/arguments, working directory, environment names, sandbox, start/end, exit/signal, stdout/stderr references, resource use, file changes, network/tool effects, and effect certainty.

## Exit-code interpretation

Exit code zero does not prove that tests were meaningful, expected files changed, external effects completed, requirements were met, output is safe, or deployment is healthy.

## Output limits

Command output is bounded by bytes, lines, files, duration, and retention. Truncation is explicit, and important evidence remains available by controlled reference where policy permits.

## Background processes

Background processes are denied unless the sandbox profile supports registered services with identity, ports, health, timeout, logs, and cleanup. No process survives the attempt without explicit governance.

## Build execution

Build evidence includes build system/version, target, configuration, dependency state, environment, outputs, warnings/errors, duration/resources, reproducibility limitations, and result.

## Test execution

Test evidence includes framework/version, command, suite, environment, discovered/executed/skipped/failed counts, duration, report files, coverage where available, retry/flaky state, exit status, and limitations.

## Test-result normalization

```text
not_run
passed
passed_with_warnings
failed
partial
cancelled
timed_out
infrastructure_error
results_unparseable
unknown
```

## Flaky, skipped, and deselected tests

Retries are recorded separately. Passing only after retry differs from first-pass success.

Skipped, ignored, quarantined, deselected, or unavailable tests remain visible.

## Coverage

Coverage is meaningful only with known tool, scope, baseline, exclusions, and report. Percentage alone is not proof of correctness or security.

## Lint and formatting

Distinguish check-only and auto-fix modes. Warnings, errors, unsupported files, and all automatic changes are included in evidence and the final diff.

## Migration commands

Database or infrastructure migrations default to generate/inspect/validate in local or test sandbox. Production execution requires a separate operational capability, approval, backup, and rollback plan.

## Local service execution

Starting application services requires explicit ports, network, secrets, fixtures, readiness checks, lifecycle, output limits, and cleanup.

## Smoke checks

Smoke checks record target identity, environment, request type, expected markers, status, timing, and limitations. A single HTTP success does not prove end-to-end correctness.

## Dependency inspection

Read-only dependency inspection may use manifests, lockfiles, local caches, and approved registry metadata without granting installation authority.

## Dependency installation

Installation requires approved registry, package/version or resolver policy, lockfile handling, integrity/provenance where available, lifecycle-script policy, network allowlist, resource limits, secret-free credentials, diff, and evidence.

## Lifecycle scripts

Package lifecycle scripts may execute arbitrary code and therefore require an appropriate sandbox and sometimes explicit approval.

## Lockfile handling

Lockfile changes record package-manager/version, manifest changes, resolved packages, integrity fields, platform differences, registry, and generated status. Large unexplained changes are review findings.

## Vulnerability and license findings

Codex may propose findings, but authoritative severity, exception, and release decisions remain in Agent OS security and quality governance.

## Network access

Network is denied by default or limited to approved package registries, source providers, documentation, test services, model/runtime endpoints, and explicitly approved APIs.

Broad internet access is not inherited from the host.

## Untrusted web and repository content

Documentation, issues, PR comments, package pages, repository instructions, generated code, and web content are untrusted and cannot redefine permissions, approvals, secrets, sandbox, budget, or evidence.

## Secret access

Secrets use references or brokered operations and bind to workspace, attempt, purpose, destination, expiry, policy, and approval.

## Repository-provider identity

Prefer a registered installation or narrowly scoped provider identity over a user's reusable broad personal token. Permissions are limited to the exact repository and operation.

## Git capability taxonomy

```text
git.status
git.diff
git.log
git.branch_list
git.branch_create
git.stage
git.commit
git.fetch
git.push
git.tag_create
git.tag_push
pull_request.read
pull_request.review
pull_request.create
pull_request.update
pull_request.merge
release.create
deployment.trigger
```

## Git read operations

Read operations remain repository-scoped and may expose sensitive branch names, commit messages, PRs, or author metadata. They require authorization and minimization.

## Git stage

Staging is a distinct local mutation. Record staged paths and verify they match the reviewed change set.

## Git commit

Commit creation requires exact repository/worktree, reviewed diff fingerprint, author/committer policy, message, hook policy, signing direction, branch policy, approval where required, and resulting hash.

## Commit attribution

Do not falsely imply that Codex is the human author. The final attribution model may distinguish human requester, Agent OS automation identity, Codex-assisted change, co-authoring direction, signing identity, and evidence reference.

## Git hooks

Git hooks are executable code. The adapter declares whether hooks are disabled, inspected, sandboxed, or allowed, because commit commands may trigger hidden side effects.

## Git push

Push requires separate authorization for repository/provider, remote, branch/refspec, commit hash, force policy, expected remote head, credentials, idempotency, and receipt.

## Push concurrency

Verify the expected remote head before push. Non-fast-forward or changed remote state triggers reconciliation and possibly a new review. Force push is denied by default.

## Push evidence

Evidence includes provider/repository, remote, branch/refspec, local commit, previous/resulting remote head, receipt, actor chain, time, policy/approval, and certainty.

## Pull-request creation

PR creation requires repository, source and target branches, exact remote commit, title/body, linked task/run, reviewers/labels where permitted, draft state, approval, and provider receipt.

Creating a PR does not merge it.

## Pull-request update

Updating title, body, reviewers, labels, source commits, or draft state may be separately governed. Material diff changes invalidate previous code approval.

## Pull-request review

Codex review findings are advisory unless a human-governed workflow assigns formal status. Findings contain path/line, category, suggested severity, rationale, confidence, evidence, proposed fix, and limitations.

Codex cannot independently approve its own authored change.

## Merge

Merge is a high-risk remote effect distinct from PR approval and creation. It requires exact repository, PR, head/base, required checks, review state, merge strategy, branch protection, approval, receipt, and effect verification.

## Tags, releases, and publication

Tag creation, tag push, release creation, artifact publication, and changelog publication are distinct capabilities with exact versions, commits, destinations, signing, and approvals.

## Deployment trigger

Deployment is outside ordinary coding authority and requires environment, artifact/commit digest, configuration, migrations, rollback, approval, health/evidence requirements, and provider receipt.

## Repository effect certainty

```text
not_started
local_effect_confirmed
remote_effect_confirmed
remote_effect_partially_confirmed
remote_effect_unknown
reconciliation_required
```

## Unknown Git effect

When push, PR, merge, tag, release, or deployment outcome is uncertain, stop automatic retry, query provider state, compare expected commit/ref, preserve evidence, reconcile, and obtain new approval if state changed.

## Artifact candidates

Codex may produce patches, source, tests, documentation, reports, build outputs, screenshots, logs, migrations, and release notes. All remain candidates until Agent OS validation and acceptance.

## Artifact validation

Validation may include file type/size, syntax/build, tests, security scans, secret scans, licenses, accessibility, visual validation, diff review, provenance, active-content controls, and expected paths.

## Source provenance

Record repository/base, task/run/attempt, runtime/version, model observation, context fingerprint, commands, tests, diff, approvals, Git effects, and final hashes.

## Screenshots and images

Images consumed by Codex are referenced with classification, purpose, and retention. They are not committed to repositories unless explicitly authorized.

## Visual validation integration

For UI changes, the adapter may coordinate build, local runtime, smoke checks, screenshots at required widths, interaction checks, visual diffs, and reviewer findings.

Human validation remains required where specified by `VVR-001`.

## Model observation

Where available, record configured model/profile, client-selected model, runtime-reported model, provider-reported identity, fallback, context/output limits, usage source, and unknown state.

Do not infer exact model identity from product branding.

## Material model change

A model change may affect quality, context, tools, latency, cost, data handling, and reproducibility. It triggers capability, policy, cost, and possibly approval re-evaluation.

## Usage metrics

Potential metrics include model requests/tokens, task or credit units, command duration, build/test minutes, sandbox resources, network/package use, Git-provider calls, artifact processing, retries, and cloud-task units where exposed.

## Usage completeness

```text
complete
complete_with_limitations
partial
estimated
delayed
unsupported
unknown
```

## Cost estimation and limits

Before execution, estimate measurable model/task usage, commands, build/test resources, package/network use, cloud-task use, retries, artifact processing, and uncertainty.

Codex receives reservation and caps but cannot alter them.

## Unknown cost

When exact consumption is unavailable, record estimated or unknown exposure and apply policy. Never report zero merely because a client exposes no meter.

## Policy integration

Policy governs runtime enablement, repository/path access, commands, packages/network, secrets, stage/commit/push/PR/merge, release/deployment, model changes, costs, exports, support, and recovery.

## Approval categories

```text
command_approval
network_approval
secret_use_approval
dependency_change_approval
diff_approval
commit_approval
push_approval
pull_request_approval
merge_approval
release_approval
deployment_approval
high_cost_approval
destructive_change_approval
```

## Approval binding and wait

Approvals bind to exact command, diff, repository, branch, target, commit, remote, cost, and environment fields. During approval wait, the protected effect is not dispatched, expiry applies, cancellation remains available, and material change invalidates approval.

## Self-review prohibition

Codex-generated review is agent advisory evidence. It cannot satisfy an independent human approval requirement for Codex-authored changes.

## Sandbox mapping

Recommended profiles:

- read/explain: `SAN-P1`;
- isolated build/test: `SAN-P2`;
- controlled repository changes: `SAN-P3`;
- package/docs/provider access: `SAN-P4`;
- push/PR/merge/release/deployment: protected `SAN-P5` gateways.

## Full-runtime isolation

If the Codex client internally executes commands outside Agent OS command mediation, the entire runtime must operate inside an approved sandbox exposing only the attempt worktree and governed channels.

## Host, container, database, and cloud boundaries

Deny unrestricted home directories, SSH keys, credential stores, runtime sockets, cloud metadata, production configuration, other repositories, and desktop apps.

Container access uses isolated/rootless infrastructure without privileged mode or host runtime socket. Production database and cloud apply/deploy operations are separate protected capabilities.

## Event model

Codex adapter events use the Agent OS envelope with runtime, execution context, repository, run/attempt, workspace/environment, actor chain, sequence, correlation, classification, and integrity metadata.

## Lifecycle events

Potential events:

```text
CodexRuntimeDiscovered
CodexRuntimeRegistered
CodexHandshakeCompleted
CodexCapabilityValidated
CodexCapabilityDriftDetected
CodexRepositoryPrepared
CodexExecutionCreated
CodexExecutionStarted
CodexPlanProposed
CodexCommandProposed
CodexCommandStarted
CodexCommandCompleted
CodexPatchProposed
CodexFilesChanged
CodexTestsCompleted
CodexDiffCollected
CodexCommitProposed
CodexCommitCreated
CodexPushProposed
CodexPushCompleted
CodexPullRequestCreated
CodexMergeCompleted
CodexApprovalRequired
CodexUsageReported
CodexCancellationAcknowledged
CodexExecutionCompletedCandidate
CodexExecutionFailed
CodexRemoteEffectUnknown
CodexRuntimeQuarantined
```

## Event ordering and replay

Events use sequence numbers or equivalent cursors. Duplicates, gaps, restarts, replay, and late arrivals remain explicit.

Replay re-emits event/evidence state and never repeats commands, approvals, or Git effects.

## Streaming

Streaming may contain progress, questions, command/patch proposals, findings, logs, usage, and completion candidates. Private model chain-of-thought is neither required nor stored.

## Error taxonomy

```text
runtime_connection_error
runtime_authentication_error
protocol_incompatible
capability_unsupported
repository_not_found
repository_access_denied
repository_state_conflict
path_scope_violation
patch_conflict
command_denied
command_failed
build_failed
test_failed
package_error
network_denied
secret_denied
git_local_error
git_remote_error
pull_request_error
merge_error
model_error
usage_error
cost_error
cancellation_error
evidence_error
security_violation
remote_effect_unknown
unknown_error
```

## Error envelope

An error contains stable code/category, safe message, retryability, effect certainty, repository/run/attempt, runtime/component, command or Git reference, correlation, source time, evidence, remediation hint, and no raw secret.

## Retryability

```text
not_retryable
retryable_same_attempt_for_read_only
retryable_new_attempt
retry_after_repository_refresh
retry_after_approval
retry_after_operator_action
retry_after_reconciliation
unknown
```

Repository-changing retries normally use a new attempt or explicit governed continuation.

## Cancellation model

```text
requested
acknowledged
stopping
commands_stopping
processes_stopped
changes_collected
cleanup_pending
cleaned
remote_effect_unknown
reconciliation_required
```

## Cancellation propagation

Cancellation propagates to Codex task/session, model request when supported, process group, background services, package/network actions, sandbox, pending Git/tool proposals, secret leases, and cost reservation after reconciliation.

## Cancellation with local changes

Local changes are collected and fingerprinted, preserved as provisional artifacts or discarded by policy, never committed/pushed automatically, and remain linked to the cancelled attempt.

## Cancellation with remote effects

If a remote Git, release, or deployment effect may have occurred, block retry, query provider state, preserve receipts/errors, reconcile exact state, and create corrective action if required.

## Lost execution

On lost execution:

1. stop new protected dispatch;
2. inspect sandbox/processes;
3. collect repository state;
4. inspect remote provider state;
5. preserve events and logs;
6. mark uncertain effects;
7. revoke channels;
8. decide safe retry or reconciliation.

## Health model

Health dimensions:

```text
adapter_transport
codex_runtime
model_route
repository_access
sandbox
command_executor
network_gateway
secret_broker
git_provider
event_stream
usage_meter
audit_evidence
```

## Health states and readiness

```text
healthy
degraded
unavailable
incompatible
quarantined
unknown
```

Readiness is capability-specific and may verify runtime identity/version, repository access, worktree creation, sandbox, commands, model route, network/package policy, Git provider, usage/cost, and evidence.

## Quarantine

Quarantine may follow identity mismatch, tampering, capability drift, host-scope escape, secret exposure, Tool/Git bypass, cross-workspace access, evidence manipulation, uncontrolled remote effects, or compromised plugins/skills.

Quarantined runtimes receive no protected tasks.

## Upgrade and compatibility

Before upgrade, record current versions, compare capabilities, run repository-fixture tests, validate commands, patches, builds, tests, Git, cancellation, usage, and evidence, then stage/canary with rollback.

## Compatibility matrix

Record Agent OS version, adapter version, Codex client/runtime/version, OS, integration mode, wrapper/protocol, model profile, validated capabilities, limitations, test environment/date, and evidence.

States:

```text
compatible
compatible_with_limitations
requires_translation
incompatible
untested
unknown
```

## Feature flags and canary

New capabilities are enabled by environment, workspace, runtime version, repository class, capability, and risk. Start with synthetic/test repositories, read-only tasks, then local changes, builds/tests, optional commits, and finally separately governed remote Git.

## Rollback

Rollback may disable a capability, runtime version, plugin/skill, or adapter release while preserving worktrees according to policy, attempts, costs, evidence, commits, remote effects, unknown states, and quarantines.

## Local development direction

Recommended initial local integration:

- one validated Codex CLI or controlled local runtime wrapper;
- explicit repository selection;
- attempt-specific worktree;
- `SAN-P1` through `SAN-P3`;
- no network by default;
- no raw credentials;
- no autonomous commit/push/PR/merge;
- command, diff, and test evidence;
- explicit human review.

## Cloud-task direction

A cloud/remote task must record remote environment identity, repository source/base, provider account, network/secrets, task lifecycle, resulting patch/branch/commit, usage/cost, evidence, cancellation, retention, and deletion.

Cloud isolation is accepted only to the extent supported by current official evidence and validated integration behavior.

## IDE and desktop direction

IDE/desktop integration requires a wrapper, SDK, plugin, local protocol, or controlled handoff preserving repository scope, identity, commands, changes, and evidence. UI presence alone is not a stable machine contract.

## Review integration direction

A read-only PR review mode preserves repository, PR, base, and head identity and returns structured findings. It cannot provide independent human approval for its own generated work.

## Audit evidence

`AUD-001` evidence covers runtime registration, repository preparation, task/context fingerprints, plans/questions, commands, file changes, builds/tests, dependency actions, model observations, approvals, sandbox/network/secrets, Git effects/receipts, artifacts, usage/cost, cancellation, recovery, and quarantine.

## Evidence package

A Codex attempt package may include:

- task snapshot;
- runtime/client/version;
- model profile/observation;
- repository/base/worktree;
- context fingerprint;
- commands and outputs;
- normalized diff;
- scans/build/tests;
- approvals;
- Git receipts;
- artifacts;
- usage/cost;
- violations;
- cancellation/cleanup;
- completeness and limitations.

## Evidence completeness

```text
complete
complete_with_declared_limitations
partial
incomplete
conflicted
unknown
```

Missing remote receipts, truncated output, unparseable tests, unknown model identity, or unknown cost remain declared.

## Observability

Monitor runtime readiness, repository preparation, active executions, command denials/failures, patch conflicts, changed paths, build/test duration and failures, package/network access, approval waits, Git effects, remote uncertainty, model errors, usage freshness, cost overruns, cancellation, event gaps, evidence completeness, and quarantine.

## Metrics

Potential metrics:

```text
codex_runtime_ready
codex_executions_active
codex_repository_prepare_seconds
codex_commands_total
codex_command_denials_total
codex_command_failures_total
codex_files_changed_total
codex_patch_conflicts_total
codex_build_seconds
codex_tests_executed_total
codex_tests_failed_total
codex_approval_wait_seconds
codex_git_commits_total
codex_git_pushes_total
codex_remote_effect_unknown_total
codex_cancellation_seconds
codex_usage_delay_seconds
codex_cost_overrun_total
codex_evidence_incomplete_total
codex_runtime_quarantined
```

## Alerts

Potential alerts:

```text
codex_runtime_unavailable
codex_identity_mismatch
codex_capability_drift
codex_repository_scope_violation
codex_host_access_attempt
codex_secret_exposure_detected
codex_unapproved_command_attempt
codex_network_bypass_attempt
codex_git_remote_mismatch
codex_force_push_attempt
codex_remote_effect_unknown
codex_cost_overrun
codex_usage_meter_delayed
codex_cancellation_timeout
codex_evidence_failure
codex_runtime_quarantined
```

## Operational dashboard

Show runtime/client/version, mode, capabilities, active repository contexts, executions, degraded dependencies, command/Git queues, approvals, usage/cost freshness, event cursor, evidence health, quarantine/incidents, and upgrade status.

## Runbooks

Required runbooks:

```text
register Codex runtime
validate capabilities
enable Codex for workspace/repository
prepare isolated worktree
recover dirty worktree conflict
investigate command denial/failure
resolve patch conflict
reconcile unknown Git effect
cancel stuck task
recover lost local execution
recover lost cloud task
handle unknown usage/cost
quarantine runtime
revoke repository credentials
upgrade adapter/runtime
rollback adapter/runtime
delete local/cloud task data
```

## Data classification and retention

Repository content, prompts, screenshots, command output, diffs, tests, Git metadata, cloud-task data, and evidence inherit Agent OS classification.

Directional retention:

- worktrees/temp: `R0/R1`;
- task/session metadata and logs: `R1/R2`;
- accepted artifacts: project profile;
- Git/release evidence: `R3/R4`;
- incidents: `R4/R5`;
- provider/cloud data: separately tracked.

## Deletion

Deletion may cover local task/session data, worktrees/clones, caches, logs, screenshots, patch candidates, provider/cloud tasks, plugin/skill context, indexes, secret leases, and exports.

Deleting an Agent OS task does not silently erase authoritative repository commits or remote PRs.

## Privacy

Minimize human identity fields sent to Codex and repository providers. Prefer stable principal references to unnecessary names, emails, or full profiles.

## API direction

Potential resources:

```text
/codex-runtimes
/codex-runtimes/{id}/capabilities
/codex-runtimes/{id}/health
/codex-repository-contexts
/codex-executions
/codex-command-proposals
/codex-change-sets
/codex-test-results
/codex-git-actions
/codex-events
/codex-usage
/codex-evidence
/codex-quarantines
```

## Command API direction

Potential commands:

```text
discover
register
authenticate
validate-capabilities
enable
disable
revoke
prepare-repository
create-execution
send-clarification
approve-command
apply-patch
collect-diff
run-build
run-tests
stage-changes
create-commit
push-branch
create-pull-request
update-pull-request
merge-pull-request
cancel
reconcile-git-effect
quarantine
release-quarantine
upgrade
rollback
```

Clients cannot set completion, capability validation, Git confirmation, or evidence verification directly.

## Data model direction

```text
CodexRuntimeRegistration
CodexRuntimeInstance
CodexCapabilityMapping
CodexCompatibilityRecord
CodexRepositoryContext
CodexWorktree
CodexExecution
CodexEventCursor
CodexPlan
CodexClarification
CodexCommandProposal
CodexCommandExecution
CodexChangeSet
CodexFileChange
CodexPatch
CodexTestResult
CodexBuildResult
CodexModelObservation
CodexGitAction
CodexRemoteReceipt
CodexUsageReport
CodexEvidencePackage
CodexHealthSnapshot
CodexQuarantine
```

## Conformance test strategy

Test runtime registration, identity, capabilities, repository authorization, worktrees, paths, task/attempt mapping, commands, files/patches, builds/tests, packages/network, secrets, models, approvals, sandbox, Git local/remote, artifacts, usage/cost, events/replay, cancellation, recovery, evidence, security abuse, fault injection, performance, accessibility, visual UI, upgrades, and rollback.

## Registration tests

Valid runtime, unsupported client, wrong environment, invalid version, revoked identity, stale validation, incompatible wrapper, and mixed modes.

## Repository tests

Correct/wrong repository, unauthorized branch, dirty tree, submodules, symlink escape, nested repository, large files, allowed/excluded paths, secrets, and cleanup.

## Worktree tests

Creation, unique scope, baseline hash, concurrent attempts, branch collision, stale base, untracked files, cancellation, persistence, and deletion.

## Command tests

Read-only, write, prohibited executable, shell injection, wrong directory, network, secrets, timeout, output limits, background/child process, and cleanup.

## Patch and file tests

Proposal, application, direct edits, conflict, binary, rename, delete, mode, generated files, disallowed path, secret introduction, encoding, and fingerprint.

## Build and test tests

Success, failure, warning, timeout, infrastructure error, skipped tests, flaky retries, malformed report, coverage, changed files, and service cleanup.

## Package tests

Approved/denied registry, exact version, lockfile, lifecycle scripts, integrity mismatch, network denial, cache, vulnerability finding, and rollback.

## Git-local tests

Status, diff, stage, commit, hooks, message, attribution, signing direction, wrong branch, stale approval, and resulting hash.

## Git-remote tests

Exact push, wrong remote, changed head, non-fast-forward, force denial, duplicate push, unknown response, PR create/update, merge checks, tag/release, outage, and reconciliation.

## Approval tests

Command, diff, commit, push, PR, merge, release, deployment, cost, expiry, eligibility, self-review, fingerprint change, consumption, denial, and policy change.

## Sandbox tests

Read-only, computation, repository write, restricted network, secrets, host path, runtime socket, Docker, database, background process, limits, and cleanup.

## Model and usage tests

Configured/observed model, fallback, usage, delayed meter, opaque credits, estimate, cost cap, cancellation cost, and unknown cost.

## Event tests

Ordering, duplicates, gaps, restart, replay, late events, mixed IDs, schema, oversized events, and secret leakage.

## Cancellation tests

Before start, model, command, build, test, install, local Git, remote Git, cloud task, event loss, timeout, local changes, and cleanup.

## Recovery tests

Adapter/process crash, desktop close, cloud-task loss, Agent OS restart, stale worktree, stale credentials, unknown push, partial PR, and replay.

## Security-abuse tests

Wrong repository/workspace, host home, credentials, runtime socket, approval bypass, unrestricted network, secrets, policy/budget modification, self-approval, wrong remote, force push, merge bypass, evidence suppression, false effect confirmation, and plugin authority.

## Cross-workspace tests

Direct access, search, count, download, event subscription, mutation, forged repository IDs, and stale-cache isolation.

## Fault-injection tests

Runtime/model/sandbox outage, disk full, process kill, registry failure, Git timeout, duplicate responses, event loss, audit outage, meter outage, secret-broker failure, and restore interruption.

## Performance direction

Measure repository preparation, context indexing, startup, command latency, diff collection, build/test duration, event throughput, cancellation, Git-provider round trips, evidence packaging, and concurrency. Formal targets remain in `NFR-001`.

## Accessibility and visual validation

Views follow proposed `A11Y-001` and `VVR-001`, including repository selection, dirty conflicts, plans, command approval, diff review, partial/failed tests, commit/push/PR approvals, remote-head conflict, unknown effect, cost overrun, cancellation, degradation, quarantine, mobile read-only review, dark theme, and large diffs.

## MVP scope

Recommended MVP:

- one validated local Codex runtime/client;
- explicit repository selection;
- attempt-specific worktrees;
- read, explain, modify, build, test, lint, and format;
- structured command proposals;
- `SAN-P1` to `SAN-P3`;
- network denied by default;
- brokered package access;
- normalized diff and file-change evidence;
- explicit model/usage unknown states;
- cancellation and cleanup;
- optional local commit only after approval;
- no autonomous push, PR, merge, release, or deployment;
- complete attempt evidence package.

## Pilot readiness

Before pilot:

- runtime identity/version and capabilities are validated;
- repository/worktree/path/secret isolation passes;
- commands and sandbox controls pass;
- builds/tests produce normalized evidence;
- diff approval is exact;
- local commit boundaries pass;
- remote Git remains disabled or separately validated;
- model and cost limitations are visible;
- cancellation/recovery works;
- cross-workspace tests pass;
- plugins/skills are inventoried;
- quarantine works;
- no critical defect remains.

## Controlled-commercial direction

Future controlled commercial support may add managed cloud tasks, stronger workload identity, organization-managed repository installations, signed runtime/wrapper builds, customer-specific executor pools, protected push/PR workflows, automated read-only review, controlled merge/release/deployment, high-availability events, customer audit exports, and formal compatibility certification.

## Maturity stages

```text
X0 — manual Codex use outside Agent OS
X1 — local registered runtime, isolated worktree, governed commands and diffs
X2 — builds/tests, cost, evidence, cancellation, optional approved commit
X3 — protected remote Git, cloud tasks, review integrations, stronger identity
X4 — mature multi-tenant Codex integration and controlled delivery
```

## Requirement catalogue — Identity, runtime, and repository

- `CDX-REQ-REG-001` — Codex runtime and adapter use distinct authenticated identities.
- `CDX-REQ-REG-002` — Runtime/client type and version are recorded.
- `CDX-REQ-REG-003` — Capabilities are validated per mode.
- `CDX-REQ-REG-004` — Repository authorization precedes metadata and content retrieval.
- `CDX-REQ-REG-005` — Every attempt binds to exact repository and base.
- `CDX-REQ-REG-006` — Attempt-specific worktrees isolate changes.
- `CDX-REQ-REG-007` — Pre-existing changes are detected and preserved.
- `CDX-REQ-REG-008` — Path policy is enforced outside prompts.
- `CDX-REQ-REG-009` — Cross-workspace contexts are prohibited.
- `CDX-REQ-REG-010` — Capability drift suspends use.
- `CDX-REQ-REG-011` — Quarantined runtimes receive no protected work.
- `CDX-REQ-REG-012` — Compatibility limitations are explicit.

## Requirement catalogue — Commands, changes, and tests

- `CDX-REQ-DEV-001` — Commands use structured proposals and policy.
- `CDX-REQ-DEV-002` — Shell, network, packages, secrets, containers, databases, and cloud access are separately governed.
- `CDX-REQ-DEV-003` — Every changed path is captured.
- `CDX-REQ-DEV-004` — Proposed and applied patches remain distinct.
- `CDX-REQ-DEV-005` — Diff fingerprints cover all material changes.
- `CDX-REQ-DEV-006` — Command/test success does not directly complete the run.
- `CDX-REQ-DEV-007` — Skipped, flaky, partial, timed-out, and unparseable tests remain visible.
- `CDX-REQ-DEV-008` — Generated and binary files receive explicit treatment.
- `CDX-REQ-DEV-009` — Processes are bounded and cleaned.
- `CDX-REQ-DEV-010` — Secret scanning applies to changes, logs, and artifacts.
- `CDX-REQ-DEV-011` — Cancellation preserves provisional changes and evidence.
- `CDX-REQ-DEV-012` — Retries preserve attempts and costs.

## Requirement catalogue — Git and protected effects

- `CDX-REQ-GIT-001` — Git read, stage, commit, push, PR, merge, tag, release, and deploy are distinct.
- `CDX-REQ-GIT-002` — Commit approval binds to reviewed diff and state.
- `CDX-REQ-GIT-003` — Push approval binds to remote, ref, commit, and expected head.
- `CDX-REQ-GIT-004` — Force push is denied by default.
- `CDX-REQ-GIT-005` — PR creation does not imply merge.
- `CDX-REQ-GIT-006` — Codex cannot independently approve its authored changes.
- `CDX-REQ-GIT-007` — Remote effects require receipts or verified state.
- `CDX-REQ-GIT-008` — Unknown effects block blind retry.
- `CDX-REQ-GIT-009` — Material state change invalidates approval.
- `CDX-REQ-GIT-010` — Deployment is separate from coding authority.
- `CDX-REQ-GIT-011` — Historical Git effects remain attributable.
- `CDX-REQ-GIT-012` — Remote credentials are scoped and revocable.

## Requirement catalogue — Cost, evidence, security, and quality

- `CDX-REQ-OPS-001` — Usage completeness and model identity are explicit.
- `CDX-REQ-OPS-002` — Unknown cost is not zero.
- `CDX-REQ-OPS-003` — Runtime cannot modify budgets or approvals.
- `CDX-REQ-OPS-004` — Commands, diffs, tests, Git effects, and receipts are audited.
- `CDX-REQ-OPS-005` — Raw secrets are excluded.
- `CDX-REQ-OPS-006` — Policy, approval, sandbox, and Git controls fail closed.
- `CDX-REQ-OPS-007` — Cross-workspace paths and APIs receive negative tests.
- `CDX-REQ-OPS-008` — Cancellation/recovery preserve unknown effects.
- `CDX-REQ-OPS-009` — Plugins and skills cannot grant authority.
- `CDX-REQ-OPS-010` — Critical defects block pilot/release.
- `CDX-REQ-OPS-011` — Interfaces are accessible and visually validated.
- `CDX-REQ-OPS-012` — Codex cannot self-certify completion or conformance.

## Traceability

| Source | ADP-CDX-001 response |
|---|---|
| `AGC-001` | Adapter identity, commands, events, errors, lifecycle, and evidence |
| `CAP-001` | Capabilities, readiness, validation, and drift |
| `MOD-001` | Model profiles, observations, fallback, limits, and usage |
| `RUN-001` | Task/run/attempt mapping, retries, cancellation, and completion |
| `APR-001` | Command, diff, Git, release, deployment, and cost approvals |
| `ART-001` | Patch, source, tests, reports, screenshots, validation, and acceptance |
| `ORC-001` | Plans, dependencies, scheduling, and coordination |
| `INT-001` | Repository, provider, CI, deployment, and service boundaries |
| `POL-001` | Repository, command, network, secret, Git, cost, and effect decisions |
| `SAN-001` | Worktrees, filesystem, command, network, process, secret, and cleanup |
| `SEC-002` | Source, supply-chain, prompt, Git, audit, and release controls |
| `DAT-002` | Repository, prompt, cloud task, logs, artifacts, retention, and deletion |
| `AUD-001` | Actor chains, commands, diffs, tests, Git receipts, and evidence |
| `CST-001` | Task, command, sandbox, network, retries, cost, and unknown exposure |
| `ADP-HER-001` | Shared adapter states, identity, events, evidence, and recovery |

## ADR-TBD-CDX-001 — Integration modes, identity, and transport

Select initial client/runtime, wrapper/API, authentication, process ownership, and trust boundaries.

## ADR-TBD-CDX-002 — Capabilities and approval-mode normalization

Define manifest, modes, plugins/skills, validation, drift, compatibility, and effective authority.

## ADR-TBD-CDX-003 — Repository, worktree, path, and context architecture

Define identities, installations, worktrees/snapshots, dirty state, submodules, paths, context, and cleanup.

## ADR-TBD-CDX-004 — Command, package, network, and sandbox execution

Define schemas, shell, builds/tests, installs, containers, databases, cloud tools, secrets, resources, and evidence.

## ADR-TBD-CDX-005 — Change-set, diff, artifact, and review model

Define file changes, patches, diffs, fingerprints, generated/binary files, scans, tests, visual validation, and acceptance.

## ADR-TBD-CDX-006 — Git provider and software-delivery effects

Define commit attribution, signing, push, head checks, PR, review, merge, tag, release, deployment, receipts, and reconciliation.

## ADR-TBD-CDX-007 — Model, usage, cost, events, and evidence

Define model observations, current task/credit limitations, meters, costs, events, packages, freshness, and unknowns.

## ADR-TBD-CDX-008 — Cancellation, cloud tasks, upgrade, and hardening

Define local/cloud cancellation, task loss, cleanup, provider deletion, upgrades, quarantine, remote pools, and certification.

## Open decisions

1. Confirm `ADP-CDX-001` registration.
2. Select the first supported Codex mode.
3. Define the stable machine integration.
4. Define authentication and session delegation.
5. Approve capability manifest and client-mode normalization.
6. Govern plugins and skills.
7. Define repository-provider installations.
8. Approve worktree/snapshot and dirty-tree behavior.
9. Define command and shell policy.
10. Define package and lifecycle-script policy.
11. Define container, database, and cloud access.
12. Define normalized diff and test schemas.
13. Define local commit attribution/signing.
14. Decide whether push/PR are in pilot.
15. Define remote Git receipts/reconciliation.
16. Define cloud-task retention/deletion.
17. Define model and usage/credit mapping.
18. Define unknown-cost policy.
19. Define cancellation/lost-task timeouts.
20. Align shared terminology with `ADP-HER-001`.
21. Confirm accessibility and visual scenarios.
22. Decide when release/deployment receives a separate specification.

## Risks

| Risk | Consequence | Response |
|---|---|---|
| UI behavior treated as stable API | Fragility | Wrapper/version negotiation |
| Human session reused broadly | Credential exposure | Scoped delegation |
| Repository selected only by path | Wrong target | Canonical identity/base |
| Dirty worktree overwritten | User data loss | Isolated worktree |
| Prompt-only path restriction | Escape | Filesystem enforcement |
| Full-auto mode treated as authority | Bypass | Agent OS intersection |
| Hidden command hooks | Unexpected effects | Sandbox/evidence |
| Runtime socket exposed | Host compromise | Prohibited |
| Package hooks execute code | Supply-chain risk | Controlled install |
| Green tests treated as acceptance | False confidence | Structured review |
| Diff omits files | Incomplete approval | Normalized change set |
| Self-approval | No independence | Human review |
| Local commit mistaken for push | False success | Separate states |
| Timed-out push retried | Duplicate effect | Reconciliation |
| Force push | History loss | Default deny |
| Cloud retention unknown | Data risk | Provider lifecycle |
| Usage unavailable shown free | Hidden spend | Explicit unknown |
| Plugin grants authority | Tool/data exposure | Extension governance |
| Task deletion assumed to delete Git | False deletion | Separate lifecycle |
| Product capabilities change | Compatibility break | Revalidate official docs |

## Assumptions

- At least one Codex client/runtime can be invoked through a controllable integration.
- Agent OS can wrap or sandbox local execution.
- Repositories can use attempt-specific worktrees or snapshots.
- Remote Git effects can be mediated through scoped provider identities.
- Codex capabilities, models, surfaces, and usage reporting may change.
- Unsupported capabilities remain explicit.
- MVP can launch without remote Git write effects.
- Official OpenAI documentation will be rechecked before implementation and release.

## Constraints

- no Codex IAM, policy, approval, or release authority;
- no unrestricted host, shell, Docker socket, network, secret, cloud, database, or Git access;
- no path control enforced only by prompt;
- no unrelated user worktree edits by default;
- no local commit interpreted as push;
- no PR interpreted as merge;
- no unknown remote effect retried blindly;
- no test pass interpreted as full acceptance;
- no self-approval;
- no unknown model/cost presented as confirmed or zero;
- no unsupported product feature treated as guaranteed;
- no final OpenAI plan, account, SDK, transport, or billing selection;
- no Git commit, push, PR, merge, or deployment during documentation drafting.

## Acceptance criteria

ADP-CDX-001 may advance to `1.0.0` when:

1. it is registered;
2. Product accepts repository, command, diff, approval, Git, cost, and limitation journeys;
3. Architecture accepts runtime, repository/worktree, command, event, model, Git, and recovery boundaries;
4. Security accepts identity, path, sandbox, network, secrets, packages, plugins, Git, prompt injection, and quarantine;
5. Data accepts repository/context, cloud task, logs, artifacts, provider data, retention, and deletion;
6. Operations accepts registration, credentials, health, upgrades, rollback, cancellation, incidents, and runbooks;
7. Quality accepts conformance, negative, cross-workspace, build/test, Git, fault-injection, accessibility, visual, and compatibility tests;
8. first mode and machine interface are selected;
9. capabilities and approval-mode normalization are approved;
10. worktree/path architecture is approved;
11. command/package/network/sandbox contracts are approved;
12. diff/test/artifact evidence is approved;
13. Git boundaries are approved;
14. usage/cost/cancellation/evidence limitations are approved;
15. current official behavior is revalidated before implementation.

## Downstream impact

| Document or phase | Required use |
|---|---|
| `ADP-HER-001` | Reconcile shared adapter terminology and states |
| `SEC-002` | Add Codex-specific control evidence |
| `DAT-002` | Finalize repository, cloud-task, artifact, log, and deletion treatment |
| `AUD-001` | Finalize commands, diffs, tests, Git receipts, and evidence |
| `CST-001` | Finalize Codex usage and unknown-cost treatment |
| `UXA-001` | Codex repository, command, diff, Git, cost, and recovery journeys |
| `DSN-001` | Codex runtime, worktree, command, test, Git, and unknown states |
| `A11Y-001` | Accessible code review, diffs, approvals, and logs |
| `VVR-001` | Codex visual scenarios |
| Global documentation audit | Reconcile IDs, dependencies, vocabularies, owners, and priorities |
| Document register | Add proposed document |

## Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial detailed Codex adapter specification covering runtime modes, identity, capabilities, repositories, worktrees, commands, patches, builds, tests, packages, models, approvals, sandbox, Git, artifacts, cost, events, evidence, cancellation, recovery, security, compatibility, and rollout |

## References

### Internal documents

- `AGC-001` — Agent Adapter Contract
- `CAP-001` — Agent Capability Schema
- `MOD-001` — Model Profile Contract
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `ORC-001` — Workflow and Orchestration Architecture
- `INT-001` — Integration Architecture
- `POL-001` — Policy and Permission Architecture — proposed/unregistered
- `SAN-001` — Sandbox and Secure Execution Architecture — proposed/unregistered
- `SEC-002` — Security Control Catalogue — proposed/unregistered
- `DAT-002` — Data Classification, Retention and Deletion Standard — proposed/unregistered
- `AUD-001` — Audit and Evidence Architecture — proposed/unregistered
- `CST-001` — Usage, Cost and Budget Architecture — proposed/unregistered
- `ADP-HER-001` — Hermes Adapter Detailed Specification — proposed/unregistered

### Official product sources consulted

- OpenAI Help Center — *Using Codex with your ChatGPT plan*.
- OpenAI Help Center — *OpenAI Codex CLI — Getting Started*.
- OpenAI Help Center — *Plugins in Codex*.
- OpenAI Help Center — *ChatGPT Work and Codex*.

Current product behavior must be revalidated at implementation time.
