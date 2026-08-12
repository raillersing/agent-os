---
document_id: VVR-001
title: Agent OS Visual Validation and Regression Plan
version: 0.1.0
status: draft
register_status: proposed_unregistered
owner: quality-owner
approvers: [product-owner, architecture-owner, security-owner, operations-owner, quality-owner]
created: 2026-07-20
last_reviewed: 2026-07-20
classification: internal
source_of_truth: false
related_documents: []
dependencies: [UXA-001, DSN-001, A11Y-001, TST-001, QAG-001]
related_proposed_documents: [UXA-001, DSN-001, A11Y-001, UIF-001]
related_adrs: [ADR-TBD-VVR-001, ADR-TBD-VVR-002, ADR-TBD-VVR-003, ADR-TBD-VVR-004, ADR-TBD-VVR-005, ADR-TBD-VVR-006]
---

# VVR-001 — Agent OS Visual Validation and Regression Plan

> **Status: Draft — proposed/unregistered.** This document defines how Agent OS validates the actual rendered interface, governs visual baselines, detects regressions, reviews responsive and accessibility-visible states, preserves evidence, and blocks unsafe integration or release. It does not select final tooling and does not replace functional, accessibility, security, or usability testing.

## 1. Purpose

Agent OS contains interfaces where visual defects can change meaning or create operational risk: wrong workspace context, hidden approval target, unknown effect shown as success, stale dashboards shown as current, clipped evidence, invisible focus, missing emergency controls, incomplete mobile reviews, or false restore completion. Visual validation therefore verifies meaning, hierarchy, state, actions, evidence, responsiveness, and the exact running build.

## 2. Objectives

- validate the current connected runtime;
- detect unintended change before integration and release;
- cover happy, empty, partial, stale, degraded, blocked, error, unknown, conflict, maintenance, and recovery states;
- validate 320, 375, 768, 1024, and 1440 widths;
- validate light and dark themes, density modes, reduced motion, and accessibility-visible states;
- detect clipping, overlap, hidden actions, global overflow, unreadable focus, and misleading hierarchy;
- preserve build-linked evidence;
- require human review for critical flows;
- visually verify each completed frontend integration before the next integration begins.

## 3. Non-goals

Visual similarity does not prove functional correctness. This plan does not replace API tests, keyboard and screen-reader testing, security review, usability research, or connected-state verification. It does not permit automatic baseline approval, pixel-perfect cross-browser claims, review of stale servers, or mock-only pages as proof of implementation.

## 4. Principle — Current runtime first

A capture is valid only when build, environment, route, fixture, browser, viewport, theme, and data state are known.

## 5. Principle — Function before pixels

Visual approval cannot override a dead control, wrong permission, false success, missing persistence, or disconnected mock.

## 6. Principle — Critical states first-class

Unknown, stale, degraded, blocked, invalidated, quarantined, maintenance, and recovery states require explicit scenarios.

## 7. Principle — Human review remains required

Image diffs cannot decide whether changed action hierarchy, approval meaning, or risk is safe.

## 8. Principle — Baselines are intentional

A baseline is an approved rendering of a precise scenario, not an arbitrary passing screenshot.

## 9. Principle — Responsive validation is semantic

Review verifies preserved state, evidence, reading order, and actions, not only absence of overlap.

## 10. Principle — Accessibility is visible

Focus, errors, disabled states, non-color cues, reflow, forced colors, and reduced motion belong in evidence.

## 11. Principle — Noise is controlled

Time, random data, fonts, charts, animation, and polling are stabilized instead of broadly ignored.

## 12. Principle — No dead UI

Every visible control works, is disabled with reason, is authorization-hidden, or is explicitly labelled demo/planned.

## 13. Principle — Review before next integration

A frontend integration is visually accepted before another integration begins.

## 14. Principle — Evidence is traceable

All decisions reference exact captures and metadata.

## 15. Principle — Product truth beats baseline

Requirements and contracts override an obsolete or incorrect baseline.

## 16. Assurance layers

```text
component
→ domain pattern
→ page
→ journey
→ environment
→ release
```
Component checks variants and states. Pattern checks Agent OS-specific compositions. Page checks complete routes. Journey checks transitions. Environment checks the deployed runtime. Release checks complete scope and evidence.

## 17. Controlled term — Scenario

Deterministic combination of route, role, workspace, fixture, state, viewport, theme, density, browser, and interaction.

## 18. Controlled term — Capture

Screenshot, image sequence, or short recording generated from a scenario.

## 19. Controlled term — Baseline

Approved expected rendering for one scenario and version.

## 20. Controlled term — Candidate

Rendering generated by the build under review.

## 21. Controlled term — Diff

Computed or manually observed difference between baseline and candidate.

## 22. Controlled term — Finding

Classified issue or intentional change.

## 23. Controlled term — Decision

approved, approved_with_findings, rejected, baseline_update_required, blocked, or unknown.

## 24. Controlled term — Exception

Time-bounded acceptance of a known visual limitation.

## 25. Controlled term — Evidence set

Captures, metadata, diffs, findings, decisions, and exceptions for a scope.

## 26. Roles and review independence

Roles: change author, visual reviewer, UX reviewer, accessibility reviewer, product reviewer, quality owner, and release owner. The author generates candidates but is not the sole approver for approvals, authentication, permissions, unknown effects, destructive actions, emergency stop, restore, security warnings, or workspace context.

## 27. Validation environment — VVE-LOCAL

Interactive validation of the current local branch or worktree.

## 28. Validation environment — VVE-CI

Pinned-browser automated captures with deterministic fixtures.

## 29. Validation environment — VVE-INTEGRATION

Connected frontend/backend validation including persistence, roles, async states, and real errors.

## 30. Validation environment — VVE-PILOT

Validation of the actual controlled pilot deployment.

## 31. Validation environment — VVE-RELEASE

Validation of the exact release-candidate digest in a clean production-like startup.

## 32. Environment identity

Every capture records environment, source revision, build or image digest, frontend asset version, API/schema version, fixture version, browser, operating system, locale, timezone, viewport, theme, density, and capture time.

## 33. Runtime freshness preflight

1. identify and stop obsolete runtimes;
2. rebuild or refresh the changed application;
3. start the canonical runtime;
4. verify process or container status;
5. run an HTTP or route smoke check;
6. verify displayed build and environment;
7. hard-refresh or use a clean browser context;
8. load the exact fixture;
9. confirm authoritative state;
10. begin capture.

Any uncertainty blocks approval.

## 34. Stale runtime response

Old labels, mismatched asset hashes, old ports, multiple dev servers, unrecreated containers, cached service-worker output, or missing build metadata invalidate captures. Stop review, fix the runtime, repeat preflight, and discard invalid evidence.

## 35. Deterministic fixtures

Fixtures are synthetic, stable, versioned, resettable, non-sensitive, and representative. They define IDs, titles, dates, counts, roles, states, artifacts, costs, alerts, and errors. Current time, random IDs, avatars, charts, network output, polling, cursor blinking, and animation are fixed, paused, or explicitly annotated.

## 36. Locale, time, fonts, animation

Automated captures use fixed locale, timezone, clock, fonts, browser, and device-pixel ratio. French expansion scenarios are required for pilot-facing routes. Font failures are findings. Nonessential motion is disabled for pixel capture; reduced-motion is validated separately.

## 37. Stress and boundary data

Cover short and long names, long French labels, long file/model/provider names, long errors, zero/one/many records, unknown totals, expired dates, missing optional values, large and unknown costs, and maximum supported content.

## 38. Baseline governance

Baselines exist for components, domain patterns, pages, and journey milestones. Each has scenario ID, version, source revision, fixture version, browser, viewport, theme, density, reviewer, and approval date. Approved baselines are immutable for that version.

## 39. Baseline update rules

Valid updates follow approved product/design changes, browser-baseline migration, fixture correction, accessibility correction, or route retirement. Invalid reasons include a failing test, inconvenient differences, uninspected output, unstable data, or an unclassified regression.

## 40. Baseline retention

Retain current baselines, relevant prior baselines during migration, release baselines, and critical security/approval evidence. Deletion requires route retirement, no supported-release dependency, and a replacement or audit reference.

## 41. Identifier conventions

```text
Scenario: VVR-<AREA>-<NNN>
Capture: CAP-<SCENARIO>-<BUILD>-<VIEWPORT>-<THEME>
Finding: VIS-<AREA>-<NNN>
Evidence set: VVE-<CHANGE_OR_RELEASE>-<DATE>
```

## 42. Required viewport matrix

```text
320 × 800
375 × 812
768 × 1024
1024 × 768
1440 × 900
```
Also test changed breakpoint minus one, exact breakpoint, and plus one. Test short viewport heights for dialogs, sticky bars, approvals, mobile keyboards, forms, and restore steppers.

## 43. Viewport purpose — 320 px

Narrow mobile, long-label stress, one-column structure, no global overflow, and high-risk review restrictions.

## 44. Viewport purpose — 375 px

Common mobile navigation, card/table adaptation, drawers, dialogs, and sticky actions.

## 45. Viewport purpose — 768 px

Navigation transition, side-panel collapse, table reflow, and tablet reading order.

## 46. Viewport purpose — 1024 px

Standard multi-panel desktop and dense operations.

## 47. Viewport purpose — 1440 px

Wide Mission Control, bounded reading width, comparisons, and high-density operations.

## 48. Zoom, reflow, themes, and modes

Validate 200% zoom, 400% or equivalent reflow, increased text spacing, light and dark themes, system mode, comfortable and compact density, normal and reduced motion, and forced-colors/high-contrast direction where supported.

## 49. Browser and OS direction

Use one pinned Chromium build for pixel baselines. Perform structural review in Firefox and WebKit/Safari-compatible environments. Inspect fonts, focus, controls, sticky layout, tables, scrollbars, SVG/charts, dialogs, file/date inputs, and overflow. OS coverage follows claimed support, including Windows and Linux/WSL, plus macOS when Safari is claimed.

## 50. Component state matrix

Stable components cover applicable states: default, hover, active, focus, disabled, loading, selected, expanded, error, warning, success, unknown, stale, dark, compact, mobile, and long-label stress.

## 51. Component coverage — Buttons

Primary, secondary, tertiary, quiet, danger, icon, loading, disabled with reason, focus, long label, dark.

## 52. Component coverage — Inputs

Empty, filled, focus, required, error, warning, disabled, read-only, long value, prefix/suffix, dark.

## 53. Component coverage — Tables

Loading, empty, partial, stale, error, selection, bulk actions, long content, local scroll, compact, mobile cards, dark.

## 54. Component coverage — Dialogs

Small, large, long content, validation, destructive, blocked, short height, focus, dark.

## 55. Component coverage — Banners

Environment, maintenance, recovery, security, emergency stop, long content, stacking, mobile, dark.

## 56. Component coverage — Charts

Normal, empty, partial, missing, stale, threshold, long legend, mobile, dark, forced colors.

## 57. Domain coverage — Runs

Required states:

```text
created
preflight
queued
dispatching
running
waiting_approval
waiting_adapter
waiting_provider
waiting_budget
paused
cancelling
cancelled
completed
failed
stale
unknown
recovery_required
```

## 58. Domain coverage — Approvals

Required states:

```text
requested
in_review
expiring
approved
rejected
revision_requested
invalidated
expired
consumed
dispatch_unknown
```

## 59. Domain coverage — Artifacts

Required states:

```text
proposed
processing
review
accepted
rejected
quarantined
exported
deleted
missing_content
preview_unavailable
integrity_failed
```

## 60. Domain coverage — Memory

Required states:

```text
proposed
verified
conflicted
stale
expired
deleted
source_unavailable
index_stale
```

## 61. Domain coverage — Agents and adapters

Required states:

```text
ready
not_ready
degraded
unavailable
validation_expired
capability_drift
revoked
unknown
```

## 62. Domain coverage — Models

Required states:

```text
configured
selected
provider_reported
adapter_reported
actual_unknown
conflicted
fallback_active
provider_unavailable
cost_unknown
```

## 63. Domain coverage — Operations

Required states:

```text
healthy
degraded
maintenance
emergency_stop
critical_alert
stale_dashboard
event_backlog
dead_letters
backup_overdue
restore_in_progress
incident_active
```

## 64. Run review criteria

Preserve canonical state, step, attempt, last reliable evidence, freshness, waiting reason, agent/adapter/model identity, cost certainty, evidence, and next safe action. Unknown effects cannot use success styling or expose retry as the primary action. Previous attempts remain visible.

## 65. Approval review criteria

Validate exact action, exact target, scope, diff/content, data disclosure, network/filesystem, secret purpose, cost, reversibility, expiry, decision hierarchy, invalidation, and one-time consumption. Block when target or diff is inaccessible, expiry is hidden, invalidated requests remain actionable, risk relies on color, or mobile hides material context.

## 66. Artifact review criteria

Cover safe preview, metadata-only state, version comparison, integrity, provenance, classification, validation, quarantine, export, deletion hold, missing content, and long filenames.

## 67. Memory, agent, adapter, and model criteria

Memory exposes source, authority, confidence, freshness, conflict, citations, deletion, and stale index. Agent/adapter views expose readiness, validation age, limitations, drift, sessions, and secret-reference errors. Model views distinguish logical, configured, selected, reported, observed, inferred, unknown, fallback, and cost states.

## 68. Operations criteria

Distinguish health from readiness, current from stale data, completed from verified backup, and restore progress from validated recovery. Cover critical alerts, queues, dead letters, disk pressure, adapter outage, maintenance, emergency stop, incidents, backup failure, and recovery-only mode.

## 69. Future IAM and policy scenarios

`IAM-001` will refine sign-in, session expiry, reauthentication, denial, role assignment, break-glass, suspension, and workspace switching. `POL-001` will refine allow, deny, approval-required, missing attributes, simulation, conflict, stale policy, and prohibited override.

## 70. Route inventory and criticality

Each route records ID, path, owner, primary object, roles, states, viewport coverage, baseline, and last review.

```text
VC0 — critical control or safety
VC1 — core journey
VC2 — major supporting journey
VC3 — secondary
VC4 — informational
```
VC0 includes sign-in, approval detail, emergency stop, unknown-effect recovery, restore confirmation, permission changes, and destructive export/delete.

## 71. Coverage by criticality

VC0 receives page and journey validation every release plus cross-browser review. VC1 receives page validation every release and journey validation for major changes. VC2–VC4 use risk-based changed-area coverage and sampling.

## 72. Critical journey inventory

```text
J01 first safe run
J02 approval-gated action
J03 reject and revise
J04 stale or unknown run recovery
J05 artifact quarantine
J06 adapter outage
J07 restore and progressive recovery
J08 adapter onboarding
J09 budget exceeded
J10 support request
```
Evidence covers entry, transitions, alternate/error path, final state, action visibility, and critical focus.

## 73. Screenshot rules

Capture the complete relevant viewport, preserve environment and page context, use consistent scale, avoid sensitive data, and avoid mid-animation. Full-page images do not replace viewport images for sticky, short-height, and overflow checks. Element captures supplement but do not replace page context.

## 74. Video and interaction evidence

Use short labelled recordings for responsive transitions, keyboard/focus, dialogs, drag alternatives, async changes, and reduced motion. For critical actions, capture before action, focused/confirmation state, and resulting authoritative state.

## 75. Metadata sidecar and filenames

Metadata contains scenario, build, route, viewport, theme, density, browser, fixture, state, and time.

```text
<scenario>__<viewport>__<theme>__<state>__<build>.png
```

## 76. Diff type — Pixel

Exact rendered pixel change in a controlled environment.

## 77. Diff type — Layout

Movement, size, overlap, clipping, overflow, or missing element.

## 78. Diff type — Semantic visual

Meaning or hierarchy change requiring human interpretation.

## 79. Diff type — Content

Changed label, value, state, warning, or instruction.

## 80. Diff type — Interaction

Changed focus, hover, expanded, modal, sticky, or transition behavior.

## 81. Diff type — Responsive

Changed restructuring across widths.

## 82. Diff type — Accessibility visual

Changed focus, contrast, error, disabled state, reflow, or non-color cue.

## 83. Thresholds and masks

Pixel thresholds may suppress anti-aliasing noise but cannot suppress missing content, state changes, focus, clipping, action hierarchy, contrast, or overflow. Masks are named, justified, minimal, reviewed, and prohibited over workspace, environment, state, target, risk, approval, errors, warnings, focus, cost certainty, or evidence source.

## 84. Diff triage — intentional_change

Linked to an approved requirement and intentional baseline update.

## 85. Diff triage — regression

Unintended change requiring correction or exception.

## 86. Diff triage — environment_noise

Subpixel, scrollbar, GPU, or font variance to reduce through environment control.

## 87. Diff triage — fixture_change

Test data changed and fixture version requires review.

## 88. Diff triage — browser_variation

Engine-specific difference without semantic or accessibility impact.

## 89. Diff triage — accessibility_issue

Focus, contrast, reflow, non-color cue, text spacing, or reading-order failure.

## 90. Diff triage — functional_visual_mismatch

Rendering conflicts with actual behavior or authoritative state.

## 91. Diff triage — unknown

Cause or correctness cannot be established and critical approval is blocked.

## 92. Triage workflow

1. inspect metadata;
2. reproduce candidate;
3. inspect baseline and requirement;
4. classify changed region;
5. verify functional state;
6. assess responsive and accessibility impact;
7. choose fix, baseline update, exception, or block;
8. record finding and owner;
9. rerun;
10. approve only with current evidence.

## 93. Review checklist — Global shell

- workspace
- environment
- active navigation
- breadcrumb
- page title
- attention center
- user menu
- critical banners
- responsive navigation
- overlap

## 94. Review checklist — Hierarchy

- critical state first
- primary action clear
- secondary actions subordinate
- evidence available
- metadata readable
- no flat card wall

## 95. Review checklist — Typography

- no clipping
- wrapping
- metadata size
- code and IDs
- long labels
- line height

## 96. Review checklist — Spacing

- consistent grouping
- no accidental gaps
- sticky elements clear
- compact mode readable

## 97. Review checklist — Color

- semantic mapping
- non-color cues
- dark contrast
- unknown distinct from success
- disabled readable

## 98. Review checklist — Actions

- functional
- disabled reason
- authorization-hidden
- no silent no-op
- destructive action exact
- focus visible

## 99. Review checklist — Responsive

- no global overflow
- state visible
- actions visible
- correct reordering
- table adaptation
- drawer
- short height
- long labels

## 100. Review checklist — Evidence

- source
- freshness
- build/environment
- model identity source
- approval target
- artifact version
- timeline gaps
- unknowns

## 101. Responsive defect — overflow_global

Page-level horizontal scrolling at a required width.

## 102. Responsive defect — overflow_local_unlabelled

Local scroll without clear scope or keyboard access.

## 103. Responsive defect — content_clipped

Critical labels, IDs, targets, costs, or states lack full access.

## 104. Responsive defect — action_hidden

Required action disappears without an alternative.

## 105. Responsive defect — state_hidden

State is moved into an inaccessible region.

## 106. Responsive defect — reading_order_conflict

Visual order conflicts with DOM, keyboard, or decision order.

## 107. Responsive defect — sticky_obstruction

Sticky UI covers focus, errors, review content, or final rows.

## 108. Responsive defect — breakpoint_jump

Content unexpectedly disappears, duplicates, or shifts.

## 109. Responsive defect — touch_target_overlap

Targets overlap or become unsafe.

## 110. Responsive defect — mobile_review_incomplete

A high-risk decision lacks exact context.

## 111. Accessibility-visible scenarios

Capture focus on navigation, primary actions, dialog controls, table actions, and approval decisions; form error summary; invalid fields; disabled-with-reason; critical banner; unknown state; dark theme; forced-colors sample; 400% reflow; text-spacing override; reduced motion; and long translated labels.

## 112. Focus acceptance

Focus is clearly visible, unclipped, distinguishable from selection, within the viewport, and sufficiently contrasted in every supported theme and contrast environment.

## 113. Charts, previews, code, and diffs

Charts cover normal, empty, partial, missing, stale, threshold, long legend, mobile, dark, and forced colors. Artifact previews identify original/derived, renderer, safety, unavailable/quarantine, zoom, and mobile. Code/diffs validate long lines, local scroll, additions/deletions, line numbers, focus, dark theme, accessible review mode, and mobile restrictions.

## 114. Async state validation

Cover initial loading, refreshing, partial response, timeout, reconnect, polling fallback, late events, and duplicate suppression. Loading preserves layout and avoids false completion. Refreshing retains current data with freshness. Timeout shows certainty and safe action. Reconnect shows stale data and reconciliation warnings.

## 115. Empty, error, unknown, and conflict

Empty distinguishes first use, no results, filters, no permission, unavailable source, and not loaded. Errors include plain language, safe retry, correlation, preserved input, and no secrets. Unknown shows last reliable evidence, unresolved scope, blocked retry, and reconciliation. Conflict shows competing sources and resolution.

## 116. Maintenance and recovery

Maintenance shows environment, scope, impact, owner, duration, available functions, and next update. Recovery shows recovery-only status, blocked ordinary actions, reconciliation progress, validation gates, and staged return to service.

## 117. Functional smoke linked to review

Exercise changed navigation, dialogs, forms, filters, sorting, safe fixture decisions, cancellation, retry, errors, persistence after refresh, and authorization. A screenshot is not proof that the control works.

## 118. Dead, disabled, and hidden controls

A visible no-op is a defect. Disabled controls expose their reason and recovery path. Authorization-hidden controls are absent visually and from keyboard interaction and do not leak protected-object existence.

## 119. Persistence validation

After refresh or navigation, verify workspace selection, task/run state, approvals, artifact decisions, settings, and connected data. A mock reset or browser-only state does not prove persistence.

## 120. Build, cache, and service workers

UI, template, asset, runtime, or API-presentation changes require validation against the rebuilt or refreshed visible application. Where caches or service workers exist, validate stale client, update available, offline, invalidation, reload prompts, and mixed-version prevention.

## 121. Automated capture workflow

1. provision environment;
2. load fixture;
3. set clock, locale, timezone, theme, and density;
4. open route;
5. wait for a scenario-ready marker;
6. disable nonessential motion;
7. capture;
8. compare;
9. publish artifacts;
10. request human review.

Arbitrary sleeps are not the primary readiness mechanism.

## 122. Flakiness and quarantine

A flaky test produces inconsistent output for identical code and fixture. Causes include fonts, animation, time, random data, polling, network, browser updates, scrollbars, GPU/canvas, or unstable layout. Quarantine requires ID, reason, owner, expiry, release impact, and compensating manual review. VC0 scenarios cannot remain quarantined for release.

## 123. Manual review workflow

1. inspect intent;
2. review primary desktop;
3. review 320 and 375 mobile;
4. review 768 and 1024;
5. review dark theme;
6. review critical states;
7. review focus and reflow;
8. compare baseline;
9. exercise changed controls;
10. record decision.

## 124. Comparison techniques

Use side-by-side for hierarchy, overlay for movement and alignment, blink comparison as a supplement, and heatmaps to locate change. None replaces semantic interpretation.

## 125. Finding quality

A finding records scenario, location, expected, observed, classification, severity, user impact, functional impact, accessibility impact, evidence, owner, and next action.

## 126. Severity — VIS-0

Unsafe, security-sensitive, or critical-state misrepresentation.

## 127. Severity — VIS-1

Core journey blocked or materially misleading.

## 128. Severity — VIS-2

Major responsive or visual degradation.

## 129. Severity — VIS-3

Moderate inconsistency.

## 130. Severity — VIS-4

Minor cosmetic difference.

## 131. Severity examples

VIS-0: wrong workspace, hidden approval target, unknown shown as success, missing emergency stop, misleading destructive action, invisible critical focus, cross-workspace data, restore shown complete too early.

VIS-1: primary action unavailable, incomplete mobile approval, unusable artifact review, overflow hiding controls, stale state omitted, inaccessible dialog, silent no-op button.

VIS-2: major table clipping, unusable 768 px operations layout, unreadable dark theme, translated-label overlap, unusable chart legend.

## 132. Release and integration blockers

Release is blocked by unresolved VIS-0, relevant VIS-1, unknown VC0 diffs, missing runtime identity, missing critical mobile/dark/focus/reflow evidence, stale baselines, or dead controls.

The next frontend integration is blocked until the current integration is rendered in the current runtime, required widths are reviewed, changed actions are smoke-tested, and findings are resolved or covered by an approved exception.

## 133. Exceptions and non-waivable issues

An exception records finding, scope, severity, users, affected widths/themes/browsers, workaround, owner, expiry, remediation, and approvers. Normally non-waivable: wrong scope, misleading approval, misleading unknown state, missing emergency control, invisible critical focus, hidden mobile review context, and dead controls.

## 134. Evidence manifest and integrity

The manifest includes source/build, environment, route and scenario inventories, captures, diffs, findings, decisions, exceptions, reviewers, and date. Critical files may be hashed. Evidence uses synthetic data and appropriate classification.

## 135. Retention and redaction

Retain release-candidate evidence, critical security/approval changes, major redesign migrations, pilot acceptance, and incident visuals. Prefer synthetic data over redaction; redaction must not obscure the field being validated.

## 136. CI and change-review direction

CI may generate captures, compare, publish diffs, fail on missing baselines, and enforce thresholds. It cannot approve baseline updates. A future change review may attach evidence summaries, candidates, diffs, findings, and rationale. No Git action is authorized during drafting.

## 137. Pilot and deployment smoke

Before pilot, review the actual deployment, critical routes, supported French labels, desktop/mobile, operational states, support access, and limitations. After deployment, hard-refresh, verify build, shell, banners, primary routes, one safe interaction, no global overflow, and no asset/font failure.

## 138. Rollback and incident evidence

After rollback, verify the previous build identity, critical routes, semantics, data compatibility, and no mixed assets. UI incident evidence includes safe user report, build, route, viewport, browser, reproduction, corrected capture, and root-cause link.

## 139. Design-system blast radius

Token changes require broad component/theme/focus/chart/extension coverage. Typography changes require wrapping, tables, buttons, navigation, dialogs, French expansion, code, and print. Spacing changes require density, overflow, sticky elements, short heights, forms, and operations. Breakpoint changes require minus-one/exact/plus-one checks.

## 140. Content and specialist review

Changed labels are reviewed for clarity, controlled terminology, wrapping, translation, accessible name, action exactness, and errors. Security-sensitive language receives Security review when material. Classification, retention, source, freshness, and cost certainty receive Data review. Health, readiness, backup verification, restore completion, maintenance, and incidents receive Operations review.

## 141. Definition of ready

Routes, scenarios, states, viewports, baseline impact, fixtures, and accessibility-visible states are identified before implementation.

## 142. Definition of done

The current runtime is reviewed, changed controls work, required states/viewports/themes are captured, focus/reflow are reviewed, findings resolved, evidence stored, and a reviewer decision recorded.

## 143. Scenario template

```text
Scenario ID:
Title:
Criticality:
Route/component:
Actor/role:
Workspace:
Fixture:
State:
Viewport:
Theme:
Density:
Browser:
Preconditions:
Interaction:
Expected visual result:
Functional assertion:
Accessibility-visible assertion:
Capture list:
Owner:
```

## 144. Baseline template

```text
Baseline ID:
Scenario:
Version:
Build/source:
Fixture version:
Viewport:
Theme:
Browser:
Approved rendering:
Known browser variations:
Reviewer:
Approved at:
```

## 145. Finding template

```text
Finding ID:
Scenario:
Capture:
Location:
Expected:
Observed:
Classification:
Severity:
User impact:
Functional impact:
Accessibility impact:
Decision:
Owner:
Evidence:
```

## 146. Exception template

```text
Exception ID:
Finding:
Scope:
Severity:
Affected users:
Affected environments:
Reason:
Workaround:
Compensating validation:
Owner:
Expiry:
Remediation:
Approvers:
```

## 147. Route inventory template

```text
Route ID:
Path:
Page:
Owner:
Criticality:
Roles:
Primary object:
States:
Viewports:
Themes:
Scenarios:
Baseline:
Last reviewed:
```

## 148. Requirement catalogue — RUN

- `VVR-REQ-RUN-001` — Visual validation uses the current identified runtime.
- `VVR-REQ-RUN-002` — Captures identify build, environment, route, browser, viewport, theme, and fixture.
- `VVR-REQ-RUN-003` — Fixtures are deterministic, synthetic, and versioned.
- `VVR-REQ-RUN-004` — Stale runtime blocks approval.
- `VVR-REQ-RUN-005` — Changed controls receive functional smoke testing.
- `VVR-REQ-RUN-006` — Evidence is versioned and reviewable.
- `VVR-REQ-RUN-007` — Critical evidence avoids real secrets and personal data.
- `VVR-REQ-RUN-008` — Post-deployment visual smoke verifies the actual deployment.

## 149. Requirement catalogue — BAS

- `VVR-REQ-BAS-001` — Baselines are scenario-specific and approved.
- `VVR-REQ-BAS-002` — Baseline updates require intentional rationale.
- `VVR-REQ-BAS-003` — CI cannot auto-approve baselines.
- `VVR-REQ-BAS-004` — Masks are minimal and cannot cover critical state.
- `VVR-REQ-BAS-005` — Unknown diffs block critical scenarios.
- `VVR-REQ-BAS-006` — Browser variation is documented.
- `VVR-REQ-BAS-007` — Flaky tests are tracked and time-bounded.
- `VVR-REQ-BAS-008` — Retired baselines preserve replacement or migration history.

## 150. Requirement catalogue — COV

- `VVR-REQ-COV-001` — Required widths include 320, 375, 768, 1024, and 1440.
- `VVR-REQ-COV-002` — Light and dark themes are validated where supported.
- `VVR-REQ-COV-003` — Critical states receive explicit scenarios.
- `VVR-REQ-COV-004` — Global horizontal overflow is prohibited at required widths.
- `VVR-REQ-COV-005` — Mobile preserves essential state and review context.
- `VVR-REQ-COV-006` — Long text and localization stress are validated.
- `VVR-REQ-COV-007` — Focus and reflow receive visual evidence.
- `VVR-REQ-COV-008` — Cross-browser review covers claimed engines.

## 151. Requirement catalogue — QUA

- `VVR-REQ-QUA-001` — Visual approval does not override functional failure.
- `VVR-REQ-QUA-002` — Dead controls are defects.
- `VVR-REQ-QUA-003` — Unknown, stale, partial, and degraded states are not shown as success.
- `VVR-REQ-QUA-004` — Critical visual changes receive independent review.
- `VVR-REQ-QUA-005` — VIS-0 and relevant VIS-1 findings block release.
- `VVR-REQ-QUA-006` — An integration is visually reviewed before the next frontend integration.
- `VVR-REQ-QUA-007` — Exceptions are time-bounded and approved.
- `VVR-REQ-QUA-008` — Baselines follow approved requirements and contracts.

## 152. Traceability

| Source | VVR-001 response |
|---|---|
| `UXA-001` | Routes, journeys, states, responsive priorities |
| `DSN-001` | Tokens, themes, components, domain patterns |
| `A11Y-001` | Focus, contrast, reflow, forced colors, critical journeys |
| `TST-001` | Test environments, automation, evidence, defects |
| `QAG-001` | Release gates and exceptions |
| `RUN-001` | Run and recovery visual states |
| `APR-001` | Approval states and exact review |
| `ART-001` | Artifact preview, quarantine, and versions |
| `MEM-001` | Memory source, conflict, and stale states |
| `MOD-001` | Model identity and cost certainty |
| `OBS-001` | Health, freshness, alerts, and charts |
| `OPS-001` | Runtime verification, maintenance, incident, restore |
| `DEP-001` | Environment and deployment identity |
| `PLG-001` | Extension UI validation |

## 153. ADR-TBD-VVR-001 — Visual capture and regression toolchain

Select browser automation, screenshot engine, component environment, diff engine, and artifact publication.

## 154. ADR-TBD-VVR-002 — Baseline storage and governance

Define storage, versioning, approvals, retention, and release linkage.

## 155. ADR-TBD-VVR-003 — Canonical browser, OS, and font environment

Approve pixel-baseline environment and cross-browser review.

## 156. ADR-TBD-VVR-004 — Fixture and runtime-readiness architecture

Define fixtures, fixed clock, locale, providers, fonts, and scenario-ready markers.

## 157. ADR-TBD-VVR-005 — Review workflow and release gates

Approve roles, severity, evidence manifests, exceptions, and release sign-off.

## 158. ADR-TBD-VVR-006 — Responsive, accessibility, and extension matrix

Approve widths, zoom, forced colors, themes, density, localization stress, and extension coverage.

## 159. Open decisions

1. Confirm registration.
2. Select capture, component-story, diff, and baseline-storage tooling.
3. Select canonical browser, OS, fonts, and device-pixel ratio.
4. Confirm Firefox and WebKit review scope.
5. Confirm viewport heights and breakpoint-edge checks.
6. Confirm French and pseudo-localization scope.
7. Confirm forced-colors and 400% reflow methods.
8. Confirm fixture loading and scenario-ready markers.
9. Confirm evidence retention and CI integration.
10. Confirm independent VC0 review and exception approvers.
11. Confirm pilot-day device checks and extension UI scope.
12. Resolve whether `UIF-001` becomes a separate UI-state contract.

## 160. Risks

| Risk | Consequence | Response |
|---|---|---|
| Stale runtime review | False approval | Runtime preflight |
| Pixel tests without human review | Unsafe semantic change | Independent review |
| Dynamic data noise | Ignored differences | Deterministic fixtures |
| Masks over critical content | Missed defect | Mask governance |
| Automatic baseline updates | Regression normalised | Explicit approval |
| One viewport/theme only | Hidden defects | Required matrix |
| Screenshot without smoke | Dead controls pass | Functional smoke |
| Mock state treated as connected | False completeness | Data-source labelling |
| Browser/font drift | Noisy failures | Pinned environment |
| Mobile cards omit data | Incomplete review | Semantic responsive checks |
| Focus not captured | Keyboard regression | Focus scenarios |
| French labels untested | Pilot clipping | Locale stress |
| Evidence leaks data | Security/privacy issue | Synthetic fixtures |
| Flaky tests stay quarantined | Coverage loss | Expiry and owner |
| Process too heavy | Teams bypass it | Risk-based criticality |

## 161. Assumptions

- Agent OS uses a browser-based Mission Control.
- UXA-001, DSN-001, and A11Y-001 define architecture, components, and accessibility-visible behavior.
- Deterministic fixtures and a pinned browser can be created.
- Visual artifacts and metadata can be stored.
- Reviewers can inspect the actual current runtime.
- Visual validation remains mandatory before moving between frontend integrations.
- Git integration occurs only after drafting and global consistency review.

## 162. Constraints

- no approval from a stale or unidentified runtime;
- no automatic baseline acceptance;
- no visual sign-off for dead controls;
- no masking critical state, target, evidence, or action;
- no production secrets or personal data in fixtures;
- no global horizontal overflow at required widths;
- no high-risk mobile decision without complete review context;
- no pixel-perfect cross-browser claim;
- no substitution for functional or accessibility testing;
- no unresolved VIS-0 release;
- no Git commit, push, PR, merge, or baseline publication during drafting.

## 163. Acceptance criteria

VVR-001 may advance to `1.0.0` when it is registered; Product accepts route and journey coverage; Architecture accepts deterministic runtime and evidence boundaries; Security accepts fixtures and critical-control review; Operations accepts runtime verification and deployment smoke; Quality accepts baselines, severity, exceptions, and gates; and the viewport/theme/browser matrices, critical scenarios, evidence manifest, and integration blockers are approved.

## 164. Downstream impact

| Document | Required use |
|---|---|
| `IAM-001` | Authentication, session, role, and reauthentication scenarios |
| `POL-001` | Policy decision and permission scenarios |
| `SAN-001` | Sandbox state, violation, execution, and recovery scenarios |
| `SEC-002` | Security-control status and evidence |
| `DAT-002` | Classification, retention, and deletion states |
| `AUD-001` | Timeline, receipt, and evidence validation |
| `CST-001` | Cost and budget tables, charts, and unknown states |
| `ADP-HER-001` | Hermes adapter and capability scenarios |
| `ADP-CDX-001` | Repository, diff, command, test, and Git-action scenarios |
| Document register | Add the proposed document and dependencies |

## 165. Revision and approval history

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial visual validation and regression plan covering runtime identity, deterministic fixtures, baselines, viewports, themes, browsers, states, pages, journeys, captures, diffs, responsive and accessibility review, evidence, exceptions, integration gates, and release controls |

## 166. References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `UXA-001` — UX Architecture and User Journey Specification — proposed/unregistered
- `DSN-001` — Agent OS Design System Specification — proposed/unregistered
- `A11Y-001` — Accessibility Requirements and Conformance Plan — proposed/unregistered
- `TST-001` — Test Strategy and Verification Plan
- `QAG-001` — Quality Assurance and Release Gates
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `PLG-001` — Plugin and Extension Architecture
