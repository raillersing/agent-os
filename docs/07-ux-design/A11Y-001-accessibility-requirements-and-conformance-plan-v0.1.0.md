---
document_id: A11Y-001
title: Agent OS Accessibility Requirements and Conformance Plan
version: 1.0.1
status: in-review
owner: quality-owner
approvers:
  - product-owner
  - ux-owner
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
  - quality-owner
created: 2026-07-20
last_reviewed: 2026-08-13
approval_records:
  - role: product-owner
    status: approved
    approval_date: 2026-08-13
    evidence: explicit user confirmation of the WCAG 2.2 AA and MVP accessibility direction
  - role: ux-owner
    status: approved
    approval_date: 2026-08-13
    evidence: approval record preserved from the prior document baseline
  - role: quality-owner
    status: approved
    approval_date: 2026-08-13
    evidence: approval record preserved from the prior document baseline
pending_approvals:
  - architecture-owner
  - security-owner
  - data-owner
  - operations-owner
classification: internal
source_of_truth: false
related_documents: []
dependencies:
  - NFR-001
  - UXA-001
  - DSN-001
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
  - DAT-001
  - DCT-001
  - RUN-001
  - APR-001
  - ART-001
  - MEM-001
  - MOD-001
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
  - VVR-001
  - UIF-001
related_adrs:
  - ADR-TBD-A11Y-001
  - ADR-TBD-A11Y-002
  - ADR-TBD-A11Y-003
  - ADR-TBD-A11Y-004
  - ADR-TBD-A11Y-005
  - ADR-TBD-A11Y-006
---

# A11Y-001 — Agent OS Accessibility Requirements and Conformance Plan

> **Status: In review — Product, UX, and Quality approvals are recorded; Architecture, Security, Data, and Operations approvals remain pending.** This document defines the accessibility requirements and conformance plan for Agent OS. It establishes **WCAG 2.2 Level AA** as the MVP target direction for the web-based Mission Control, together with keyboard, focus, screen-reader, reflow, contrast, motion, forms, tables, charts, approvals, artifacts, operations, testing, evidence, exception, and release-gate requirements. It does not claim current conformance, approve a legal accessibility statement, select final assistive-technology support commitments, or replace testing by disabled users.

## 1. Purpose

Agent OS coordinates consequential work through:

- tasks;
- durable runs;
- approvals;
- agents;
- adapters;
- models;
- tools;
- artifacts;
- memory;
- operational alerts;
- recovery workflows.

Accessibility failures in these surfaces can become:

- usability failures;
- safety failures;
- security failures;
- approval failures;
- evidence failures;
- operational failures.

This plan ensures that people with disabilities can:

1. understand the current state;
2. navigate without a mouse;
3. review exact actions and evidence;
4. approve, reject, or request revision;
5. detect stale, unknown, degraded, and blocked states;
6. operate forms and complex controls;
7. read tables, charts, code, diffs, and timelines;
8. recover from errors;
9. use zoom, reflow, contrast, and reduced motion;
10. receive equivalent information and control.

## 2. Accessibility objectives

Agent OS must:

- target WCAG 2.2 Level AA for user-facing web experiences;
- use semantic HTML as the primary accessibility layer;
- support complete keyboard operation;
- provide visible and predictable focus;
- expose correct names, roles, states, and relationships;
- avoid color-only meaning;
- support text resize, zoom, and reflow;
- support common screen readers;
- support reduced motion and forced-colors environments;
- make dynamic state changes understandable;
- make approvals deliberate and accessible;
- make error recovery accessible;
- provide alternatives for drag-and-drop and pointer gestures;
- provide accessible tables, charts, timelines, code, and diffs;
- preserve accessibility across responsive breakpoints;
- include accessibility in definition of done;
- produce auditable conformance evidence;
- block release for critical accessibility failures.

## 3. Non-goals

This document does not:

- claim that Agent OS currently conforms to WCAG;
- claim legal compliance in every jurisdiction;
- define one universal assistive-technology combination;
- guarantee identical presentation across technologies;
- require every expert workflow to be fully comfortable on mobile;
- allow a desktop-only restriction without an equivalent accessible path;
- permit automated testing to replace manual testing;
- permit ARIA to replace native semantics unnecessarily;
- require decorative media;
- define final public accessibility-statement wording;
- define final procurement documentation;
- replace user research with disabled participants;
- replace `UXA-001`, `DSN-001`, or `VVR-001`.

## 4. Normative direction

The principal target direction is:

```text
WCAG 2.2 Level AA
```

Product, UX, and Quality have accepted this direction. Full controlled-document approval still requires the pending Architecture, Security, Data, and Operations reviews recorded in the front matter.

Additional guidance may include:

- semantic HTML specifications;
- WAI-ARIA and Authoring Practices guidance;
- accessibility requirements applicable to software and ICT procurement;
- platform accessibility APIs;
- browser and assistive-technology documentation.

Where guidance conflicts, the implementation must prioritize:

1. user safety;
2. native semantics;
3. tested assistive-technology behavior;
4. documented conformance;
5. predictable interaction.

## 5. Conformance status vocabulary

```text
not_assessed
assessment_in_progress
partially_conforming
conforming_with_exceptions
conforming
non_conforming
unknown
```

## 6. Not assessed

No sufficient evidence exists.

It must not be presented as conforming.

## 7. Assessment in progress

Testing is active but incomplete.

Known gaps remain visible.

## 8. Partially conforming

Some user journeys or criteria pass while others fail.

This is not a WCAG conformance claim for the complete product.

## 9. Conforming with exceptions

Used internally only when an approved accessibility exception exists.

Public claims require separate legal and quality review.

## 10. Conforming

Requires:

- approved scope;
- complete assessment;
- no unapproved failures;
- current evidence;
- supported environment statement;
- approved declaration.

## 11. Non-conforming

One or more required criteria fail.

The failure and affected journeys must be documented.

## 12. Unknown

The state cannot be established due to:

- missing test;
- unsupported technology;
- inaccessible evidence;
- environment conflict.

Unknown cannot be treated as passing.

## 13. Core accessibility principles

### `A11Y-P-001 — Native before custom`

Use native HTML elements and behavior whenever they satisfy the requirement.

### `A11Y-P-002 — Keyboard equivalence`

Every pointer-operable essential function has a keyboard path.

### `A11Y-P-003 — Programmatic meaning`

Visible labels, states, relationships, and errors are exposed to accessibility APIs.

### `A11Y-P-004 — No color-only meaning`

State, risk, severity, and validation use redundant cues.

### `A11Y-P-005 — Reflow preserves decisions`

Zoom and narrow layouts must not hide critical context or actions.

### `A11Y-P-006 — Focus follows user intent`

Focus movement is deliberate, visible, and reversible.

### `A11Y-P-007 — Dynamic updates are controlled`

Users receive useful status changes without announcement overload.

### `A11Y-P-008 — Complexity has alternatives`

Drag-and-drop, charts, code diffs, visual timelines, and diagrams have accessible alternatives.

### `A11Y-P-009 — Accessibility cannot weaken security`

Accessible authentication and approvals preserve identity, authority, and exactness.

### `A11Y-P-010 — Errors support recovery`

Errors identify the problem, affected field or action, and safe correction.

### `A11Y-P-011 — Critical journeys receive human testing`

Automated scans alone are insufficient for approvals, runs, artifacts, and recovery.

### `A11Y-P-012 — Accessibility evidence is versioned`

Claims are tied to build, route, browser, assistive technology, and date.

## 14. Accessibility dimensions

Agent OS addresses:

```text
vision
hearing
motor
speech
cognitive
neurological
temporary impairment
situational limitation
multiple disabilities
```

## 15. Vision

Includes users who are:

- blind;
- low vision;
- color blind;
- light sensitive;
- using magnification;
- using high contrast;
- using screen readers.

## 16. Hearing

Includes users who:

- are Deaf;
- are hard of hearing;
- cannot use audio;
- work in audio-restricted settings.

## 17. Motor

Includes users who:

- cannot use a mouse;
- use keyboard only;
- use switch controls;
- use alternative pointers;
- have tremor;
- need larger targets;
- use voice control.

## 18. Speech

Includes users who cannot use voice input or voice authentication.

No essential function may depend solely on speech.

## 19. Cognitive

Includes users who benefit from:

- clear language;
- predictable navigation;
- reduced complexity;
- error prevention;
- sufficient time;
- visible context;
- consistent terminology.

## 20. Neurological

Includes users affected by:

- flashing;
- excessive movement;
- vestibular triggers;
- attention overload;
- seizure risk.

## 21. Temporary impairment

Examples:

- injured hand;
- eye strain;
- temporary hearing loss;
- medication-related cognitive effects.

## 22. Situational limitation

Examples:

- bright light;
- noisy environment;
- small screen;
- poor connection;
- one-handed use;
- high zoom.

## 23. Accessibility scope

The accessibility scope includes:

```text
Mission Control shell
authentication
workspace navigation
tasks and runs
approvals
artifacts and previews
memory
agents and integrations
operations and alerts
settings
onboarding
support
notifications
generated documents and exports where controlled
extension UI surfaces
```

## 24. Out-of-scope content

Third-party content may remain partially outside direct control.

Agent OS must still:

- identify third-party origin;
- prevent inaccessible third-party content from blocking core navigation;
- provide metadata or alternatives where possible;
- disclose limitations;
- govern integrations.

## 25. Accessibility responsibility

Accessibility responsibilities include:

```text
product_owner
ux_owner
design_system_owner
implementation_owner
accessibility_reviewer
quality_owner
content_owner
extension_owner
```

## 26. Product owner

Owns:

- accessibility scope;
- priority;
- acceptance;
- user impact;
- exceptions;
- pilot readiness.

## 27. UX owner

Owns:

- journey accessibility;
- information architecture;
- understandable content;
- responsive behavior;
- error recovery.

## 28. Design-system owner

Owns:

- semantic components;
- tokens;
- focus;
- contrast;
- component accessibility;
- documented usage.

## 29. Implementation owner

Owns:

- semantic markup;
- interaction;
- ARIA;
- focus management;
- tests;
- defect correction.

## 30. Accessibility reviewer

Owns:

- manual testing;
- criterion mapping;
- assistive-technology validation;
- findings;
- evidence.

## 31. Quality owner

Owns:

- release gates;
- defect severity;
- evidence completeness;
- exception expiry;
- regression prevention.

## 32. Content owner

Owns:

- labels;
- instructions;
- error language;
- alternatives;
- headings;
- plain language.

## 33. Extension owner

Owns accessibility for plugin or extension UI under the same Agent OS requirements.

## 34. Supported interaction methods

Essential workflows must support:

```text
keyboard
pointer
touch
screen reader
zoom and magnification
reduced motion
forced colors where applicable
```

Voice control and switch-access compatibility should be assessed through semantic and target-quality testing.

## 35. Keyboard baseline

Users must be able to:

- reach every essential control;
- operate every essential control;
- identify current focus;
- escape transient components;
- navigate dialogs;
- access form errors;
- operate tables and menus;
- complete approvals;
- recover from errors.

## 36. Keyboard conventions

Use established conventions for:

- Tab and Shift+Tab;
- Enter;
- Space;
- Arrow keys;
- Escape;
- Home and End where applicable;
- Page Up and Page Down where applicable.

Custom shortcuts must not conflict with browser or assistive-technology shortcuts.

## 37. No keyboard trap

Focus must never become trapped except within a correctly implemented modal interaction that provides an escape or completion path.

## 38. Keyboard order

Focus order follows:

- visual reading order;
- workflow order;
- logical grouping;
- decision hierarchy.

CSS visual reordering must not create a conflicting DOM order.

## 39. Skip navigation

Provide bypass mechanisms for repeated content, including:

- skip to main content;
- skip to primary navigation where useful;
- skip to page actions for complex operations;
- skip to review content in long approvals.

## 40. Landmarks

Pages should use meaningful landmarks:

```text
banner
navigation
main
complementary
search
contentinfo
form
region
```

Avoid excessive unnamed regions.

## 41. Headings

Requirements:

- one clear page heading;
- logical hierarchy;
- no skipped levels without reason;
- headings describe purpose;
- visual style does not determine semantic level.

## 42. Page title

Browser/document titles identify:

- page;
- object;
- workspace where appropriate;
- environment where risk requires.

## 43. Focus visibility

Focus indicators must:

- remain visible in light and dark themes;
- have sufficient contrast;
- not be clipped;
- survive forced colors;
- distinguish focus from selection;
- remain visible inside scroll areas.

## 44. Focus appearance direction

The focused control should have:

- clear outline or equivalent;
- adequate thickness;
- adequate contrast change;
- visible perimeter or area.

Exact implementation is validated against the approved WCAG target.

## 45. Focus not obscured

Sticky headers, drawers, banners, and action bars must not fully obscure the focused item.

## 46. Focus management

Focus is managed after:

- route changes;
- dialog open and close;
- drawer open and close;
- form submission error;
- approval decision;
- deletion;
- item creation;
- notification requiring action;
- dynamic list update.

## 47. Route changes

After navigation:

- focus moves to the page heading or main content start;
- screen-reader users receive meaningful context;
- previous scroll/focus may be restored on back navigation.

## 48. Dialog focus

On open:

- focus moves to the first meaningful element;
- destructive confirmations may focus a safe element rather than the destructive action.

On close:

- focus returns to the invoking control when possible.

## 49. Deleted element focus

After deletion:

- focus moves to a logical sibling, parent, or status message;
- no focus loss to the document body without explanation.

## 50. Focus and virtualized content

Virtualization must not:

- remove the active focused element unexpectedly;
- produce illogical accessibility order;
- hide row count or position;
- break screen-reader navigation.

## 51. Semantic controls

Use native:

- button;
- link;
- input;
- select;
- textarea;
- table;
- details;
- dialog where support is tested.

Avoid clickable `div` or `span` elements for controls.

## 52. Accessible name

Every control must have a unique, descriptive accessible name within its context.

## 53. Visible label

Where a visible label exists, the accessible name should contain the visible text.

This supports speech-input users.

## 54. Role

Custom widgets expose the correct role only when necessary and implemented fully.

## 55. State

Programmatic states include:

- expanded;
- selected;
- checked;
- pressed;
- current;
- invalid;
- required;
- busy;
- disabled;
- modal.

## 56. Relationships

Programmatically expose:

- label;
- description;
- error;
- group;
- table headers;
- tabs and panels;
- controls and controlled region;
- dialog title and description.

## 57. ARIA rule

Use ARIA only when native semantics cannot meet the requirement.

Incorrect ARIA is treated as a defect.

## 58. Hidden content

Distinguish:

- visually hidden but accessible;
- hidden from all users;
- collapsed but discoverable;
- unavailable due to authorization.

Avoid leaving inactive content incorrectly exposed to screen readers.

## 59. Responsive DOM order

Responsive layouts should preserve logical source order.

Do not duplicate the same interactive control in desktop and mobile DOMs unless inactive copies are fully removed from accessibility and tab order.

## 60. Text alternatives

All meaningful non-text content requires an alternative.

## 61. Decorative images

Decorative images have empty alternatives and do not create noise.

## 62. Icons

Icons that convey state or action require:

- accompanying visible text; or
- accessible name and contextual clarity.

## 63. Status icons

The alternative identifies the actual state:

```text
Run state: Unknown
```

not merely:

```text
Question-mark icon
```

## 64. Complex images

Diagrams and architecture images require:

- short alternative;
- nearby description;
- data or textual equivalent where used for decisions.

## 65. Screenshots

Screenshots used as documentation or evidence require:

- purpose;
- relevant text description;
- no essential information only in pixels;
- redaction of sensitive data.

## 66. Charts

Charts require:

- title;
- purpose;
- units;
- time range;
- source;
- freshness;
- key findings;
- accessible data table or equivalent.

## 67. Chart interaction

Keyboard users must be able to:

- reach the chart or its data alternative;
- identify series;
- inspect values through an accessible path;
- access annotations and gaps.

## 68. Chart color

Series and states require redundant differentiation:

- labels;
- line patterns;
- markers;
- textures;
- direct annotation.

## 69. Missing chart data

Missing, stale, or unknown data must be represented textually, not only by a visual gap.

## 70. Data tables

Tables require:

- semantic table structure;
- caption or accessible name;
- correct header association;
- logical reading order;
- accessible sorting;
- accessible selection;
- accessible pagination;
- responsive equivalent.

## 71. Simple tables

Use native table markup.

## 72. Complex tables

Complex tables may require:

- multi-level headers;
- scope or header association;
- summary;
- alternative simplified view.

## 73. Grid widgets

ARIA grids are used only when spreadsheet-like keyboard interaction is genuinely required.

Ordinary data tables should remain native tables.

## 74. Table sorting

Sorting must announce:

- active column;
- direction;
- updated result state.

## 75. Table filters

Filters require:

- labels;
- clear state;
- applied-filter summary;
- no-results message;
- keyboard operation.

## 76. Table selection

Selection must expose:

- selected row;
- count;
- page-versus-all semantics;
- bulk-action scope.

## 77. Responsive tables

At small widths, choose among:

- cards;
- stacked rows;
- priority columns;
- local scroll;
- detail view.

The accessible content and relationships must remain equivalent.

## 78. Virtualized tables

Require manual screen-reader and keyboard validation.

If equivalent access cannot be established, use pagination or non-virtualized alternatives.

## 79. Code blocks

Code blocks require:

- language label where relevant;
- text access;
- wrap option or local scrolling;
- copy button with accessible feedback;
- no automatic execution.

## 80. Diff viewer

The diff viewer must provide:

- unified or split visual view;
- accessible text or list of changes;
- line and file identification;
- keyboard navigation;
- changed-section summary;
- no color-only additions/deletions.

## 81. Diff semantics

Additions and deletions require textual labels, symbols, or programmatic semantics.

## 82. Large diffs

Large diffs may offer:

- file navigator;
- change summary;
- collapse unchanged sections;
- downloadable accessible text;
- desktop-recommended review.

Approval remains blocked when essential content cannot be reviewed.

## 83. Timelines

Timelines require:

- ordered semantic structure;
- event title;
- time;
- source;
- state;
- accessible expansion;
- explicit gaps.

## 84. Timeline time semantics

Distinguish:

- occurred at;
- recorded at;
- observed at.

## 85. Forms

Every form must provide:

- clear purpose;
- labels;
- instructions;
- required status;
- validation;
- errors;
- review for consequential actions;
- safe cancellation.

## 86. Required fields

Required state is:

- visible;
- programmatic;
- explained;
- not communicated only by an asterisk.

## 87. Instructions

Instructions are placed before the relevant input or group where possible.

## 88. Input purpose

Use correct autocomplete and input-purpose metadata where appropriate.

## 89. Field errors

Errors must:

- identify the field;
- explain the issue;
- explain correction;
- persist until fixed or dismissed;
- be programmatically associated.

## 90. Error summary

After failed submission:

- focus moves to the summary;
- summary identifies count;
- links navigate to fields;
- fields retain entered values where safe.

## 91. Warning versus error

Warnings do not use invalid semantics unless the input is actually invalid.

## 92. Success feedback

Success is not communicated only through a disappearing toast.

The updated authoritative state remains visible.

## 93. Autocomplete

Where autocomplete exists:

- suggestions are keyboard accessible;
- status is announced;
- active option is exposed;
- no unexpected auto-submission.

## 94. Combobox

The implementation must follow a tested interaction pattern for:

- input;
- list;
- active option;
- selected values;
- escape;
- loading;
- no results.

## 95. Select

Prefer native select when it satisfies the need.

## 96. Multi-select

Must provide:

- clear selected-item list;
- keyboard removal;
- count or summary;
- no chip overflow that hides content.

## 97. Checkbox

Checkboxes have:

- label;
- state;
- group context;
- indeterminate state when used.

## 98. Radio group

The group has:

- legend;
- one logical tab stop or native behavior;
- visible selected state;
- keyboard arrows where appropriate.

## 99. Switch

Use only for immediate binary settings.

Switch state must be programmatically exposed and described.

## 100. Date and time

Date and time inputs must:

- support keyboard entry;
- expose format;
- expose timezone;
- avoid calendar-only entry;
- validate clearly.

## 101. File upload

File upload must support:

- keyboard selection;
- visible filename;
- type and size;
- progress;
- cancellation;
- retry;
- errors;
- safe preview status.

## 102. Drag-and-drop upload

Drag-and-drop must have an equivalent file-selection control.

## 103. Secret entry

Secret entry must support:

- accessible label;
- purpose;
- reveal/hide state;
- no accidental clipboard or log exposure;
- error recovery;
- secret-reference preference.

## 104. Form timeout

If a session or form times out:

- warn in advance where possible;
- allow extension where safe;
- preserve non-sensitive drafts;
- provide reauthentication;
- avoid data loss without notice.

## 105. Authentication

Authentication must support accessible alternatives.

It must not depend solely on:

- cognitive puzzles;
- visual CAPTCHA;
- speech;
- memory of arbitrary secrets;
- inaccessible device interaction.

## 106. Reauthentication

Reauthentication must:

- explain why;
- preserve action context;
- return to the reviewed action;
- revalidate stale data;
- support assistive technology.

## 107. Password managers

Authentication fields should support password managers and paste unless a documented security reason exists.

## 108. Cognitive function test direction

Authentication should avoid requiring users to transcribe, memorize, or solve information unnecessarily.

## 109. CAPTCHA

If used, provide an accessible alternative and evaluate whether a less exclusionary anti-abuse mechanism is available.

## 110. Time limits

Users must be warned of time limits and allowed to extend or adjust them where the activity permits.

## 111. Approval expiry

Approval expiry is a security property.

Accessibility requirements:

- absolute expiry time;
- timezone;
- warning;
- no reliance on rapidly changing countdown alone;
- recovery through a new request.

## 112. Automatic updates

Automatic refresh must not unexpectedly:

- move focus;
- reset forms;
- reorder focused rows;
- remove reviewed content;
- interrupt screen-reader reading.

## 113. Status messages

Status messages should be announced without moving focus when appropriate.

## 114. Live-region policy

Use:

```text
polite
```

for ordinary asynchronous updates.

Use:

```text
assertive
```

only for urgent safety or blocking messages.

## 115. Announcement throttling

High-frequency run or telemetry updates must be summarized rather than announcing every event.

## 116. Busy state

Regions loading or updating may expose a busy state.

Busy state must not make all current content inaccessible unnecessarily.

## 117. Toast accessibility

Toasts must:

- be programmatically announced;
- remain long enough;
- not contain the only copy of critical information;
- be dismissible where persistent;
- not steal focus unexpectedly.

## 118. Notification center

Notifications require:

- headings;
- state;
- timestamp;
- workspace;
- action;
- accessible grouping and filters.

## 119. Dialogs

Dialogs require:

- title;
- optional description;
- modal semantics where modal;
- focus containment;
- escape/close path;
- focus restoration;
- background inertness where supported.

## 120. Destructive dialog

A destructive dialog must not focus the destructive button by default without explicit design review.

## 121. Nested dialogs

Avoid nested dialogs.

Use a dedicated page for complex workflows.

## 122. Drawers

Drawers require:

- accessible name;
- focus behavior;
- escape;
- close control;
- background behavior;
- responsive alternative.

## 123. Popovers

Popovers must:

- be reachable;
- close predictably;
- not contain essential inaccessible hover-only content;
- manage focus based on interaction type.

## 124. Tooltips

Tooltips:

- supplement visible information;
- appear on hover and focus;
- are dismissible;
- remain hoverable where needed;
- do not contain essential actions.

## 125. Menus

Menus must use appropriate semantics and keyboard behavior.

Do not use menu roles for ordinary navigation lists unless menu interaction is genuinely intended.

## 126. Tabs

Tabs require:

- tablist;
- tab;
- tabpanel relationships;
- keyboard navigation;
- selected state;
- route/deep-link behavior where applicable.

## 127. Accordion

Accordion controls use buttons with expanded state and controlled region references.

## 128. Stepper

Steppers must expose:

- step names;
- current step;
- completed steps;
- errors;
- blocked steps;
- optional/skipped status.

## 129. Breadcrumb

Breadcrumbs use navigation semantics and identify the current page.

## 130. Sidebar

Sidebar navigation must support:

- keyboard;
- current item;
- groups;
- collapse/expand;
- mobile drawer;
- no icon-only ambiguity.

## 131. Command palette

If implemented:

- it must have a clear accessible name;
- focus management;
- keyboard search;
- result role;
- exact command scope;
- no ambiguous protected action.

## 132. Pointer gestures

Essential functionality must not require:

- multipoint gestures;
- path-based gestures;
- precise drawing.

Provide simpler alternatives.

## 133. Drag-and-drop

All drag-and-drop interactions require an alternative using:

- buttons;
- menus;
- move up/down;
- destination selection;
- keyboard commands.

## 134. Pointer cancellation

Actions should generally occur on release, not initial press, and support cancellation or reversal where appropriate.

## 135. Target size

Interactive targets must meet the approved target-size requirements or documented exceptions.

Spacing between compact targets must reduce accidental activation.

## 136. Touch targets

Mobile and touch layouts should generally provide larger targets than compact desktop data grids.

## 137. Motion actuation

Functionality triggered by device motion must have an interface alternative and a way to disable motion activation.

## 138. Orientation

The application should not restrict orientation unless essential.

## 139. Zoom

Content and functionality must remain usable at high browser zoom.

Testing includes at least:

```text
200%
400%
```

for applicable layouts.

## 140. Reflow

At narrow equivalent widths:

- content reflows;
- no page-level horizontal scrolling;
- actions remain available;
- state remains visible;
- review context remains intact.

## 141. Local horizontal scrolling

Allowed only for content whose two-dimensional layout is essential, such as:

- code;
- diff;
- large comparison table;
- timeline;
- diagram.

The scroll region must be keyboard accessible and labelled where necessary.

## 142. Text spacing

Users must be able to apply increased:

- line height;
- paragraph spacing;
- letter spacing;
- word spacing;

without loss of content or function.

## 143. Truncation

Truncated text must have an accessible way to obtain the full value.

Essential labels should not rely on truncation.

## 144. Responsive review

On mobile, high-risk reviews must preserve:

- exact target;
- exact action;
- risk;
- data disclosure;
- cost;
- reversibility;
- decision controls.

If not possible, the decision action is blocked with an accessible explanation.

## 145. Color contrast

Contrast requirements apply to:

- body text;
- large text;
- icons;
- borders necessary to identify controls;
- focus;
- charts;
- selected states;
- disabled text where meaning remains necessary.

## 146. Disabled controls

Disabled controls must remain understandable.

Where reason is not obvious, provide adjacent explanation or accessible details.

## 147. Placeholder contrast

Placeholder text must not be the only label or instruction.

## 148. State color

Success, warning, danger, unknown, stale, and degraded states use:

- text;
- icon;
- shape;
- color.

## 149. Focus contrast

Focus indicators must remain distinguishable from adjacent colors in all themes.

## 150. Dark theme

Dark theme receives independent contrast validation.

It is not a simple inversion.

## 151. Forced colors

Test key controls under forced-colors or high-contrast modes where supported.

Avoid suppressing platform focus and control colors without replacement.

## 152. User color settings

The application should not prevent user style adjustments without necessity.

## 153. Motion

Users who prefer reduced motion receive reduced or removed nonessential motion.

## 154. Vestibular safety

Avoid:

- parallax;
- large zoom transitions;
- rapid full-screen movement;
- uncontrolled auto-scrolling;
- continuous background animation.

## 155. Flashing

Content must not flash at frequencies or areas that create seizure risk.

## 156. Auto-playing media

Avoid auto-playing audio or video.

Provide pause, stop, and volume controls when media exists.

## 157. Animation from interactions

Provide a mechanism to disable nonessential animation triggered by interaction where required.

## 158. Progress animation

Indeterminate progress must be announced as indeterminate.

Animation must not imply a measured percentage.

## 159. Audio and video

If instructional or operational media is provided:

- captions;
- transcript;
- audio description or equivalent where visual detail is essential;
- accessible controls;
- keyboard operation;
- no autoplay with sound.

## 160. Live streams

Live audio requires captions or an equivalent plan where the content is essential.

## 161. Recorded media

Recorded media should have:

- accurate captions;
- transcript;
- description of essential visual information;
- accessible player.

## 162. Cognitive accessibility

The interface should support:

- predictable navigation;
- consistent terminology;
- clear headings;
- short instructions;
- visible progress;
- error prevention;
- review before consequential action;
- no unnecessary time pressure.

## 163. Plain language

Use plain language for:

- user instructions;
- errors;
- warnings;
- unknown states;
- support.

Technical detail remains available separately.

## 164. Abbreviations

Expand uncommon abbreviations at first use or provide an accessible glossary.

## 165. Jargon

Use controlled terms from `GLO-001`.

Avoid introducing synonyms that confuse state or authority.

## 166. Consistent identification

Components with the same function should be identified consistently.

## 167. Consistent navigation

Repeated navigation appears in consistent relative order unless a user-controlled mode changes it.

## 168. Context changes

Do not trigger major context changes solely on:

- focus;
- selection;
- typing;
- opening a field.

Provide explicit activation.

## 169. Error prevention

Consequential actions require:

- review;
- confirmation;
- correction;
- cancellation where possible;
- exact target;
- impact.

## 170. Help

Provide consistent access to:

- contextual help;
- glossary;
- runbook;
- support;
- error code explanation.

## 171. Redundant entry

Avoid asking users to re-enter information already available unless required for security, confirmation, or changed data.

## 172. Accessible authentication

Authentication flows should minimize cognitive barriers while preserving security.

## 173. Reading order

Reading order must remain logical in:

- multi-column dashboards;
- split views;
- side panels;
- responsive rearrangement;
- review pages.

## 174. Visual proximity

Visually related labels and controls should also be programmatically related.

## 175. Whitespace

Whitespace supports grouping but cannot be the only grouping cue.

## 176. Approval accessibility

Approval is a critical accessibility journey.

The user must be able to:

- identify the request;
- understand exact action;
- inspect target and scope;
- inspect diff or content;
- understand risk;
- review evidence;
- reject;
- request revision;
- approve;
- understand expiry;
- verify result.

## 177. Approval heading structure

Approval review uses clear headings for:

- decision summary;
- exact action;
- target;
- changes;
- permissions;
- data;
- cost;
- reversibility;
- evidence;
- decision.

## 178. Approval decision order

Decision controls have a stable order and unambiguous labels.

## 179. Approval keyboard path

All approval content and actions are keyboard accessible without excessive tab repetition.

Skip links or section navigation may be provided for long reviews.

## 180. Approval screen reader path

The screen reader experience should announce:

- request state;
- risk;
- expiry;
- invalidation;
- decision controls;
- updated result.

## 181. Approval invalidation

If review content changes:

- announce invalidation;
- disable old decision controls;
- preserve focus safely;
- provide link to new request.

## 182. Approval expiry

Expiry changes are announced without excessive countdown updates.

## 183. Approval diff alternative

Code or configuration diffs provide an accessible textual alternative.

## 184. Approval mobile restriction

When exact review is not practically accessible on mobile, the decision control must remain unavailable and explain how to continue on a supported layout.

## 185. Run accessibility

Run pages must expose:

- state;
- last reliable evidence;
- current step;
- waiting reason;
- agent;
- adapter;
- model identity;
- cost state;
- actions.

## 186. Run state announcements

State changes should be announced at a useful summary level.

Do not announce every low-level event.

## 187. Run progress

Progress must be:

- determinate with basis; or
- indeterminate and labelled.

## 188. Run stepper

The stepper must expose current, completed, failed, waiting, skipped, and unknown steps.

## 189. Run timeline

The timeline needs a list/table alternative and explicit gaps.

## 190. Waiting state

Waiting reason, owner, duration, and next action must be available to screen readers and keyboard users.

## 191. Stale run

Stale state must not be represented only through color or a subtle timestamp.

## 192. Unknown effect

The unknown-effect panel must:

- receive appropriate heading prominence;
- explain retry risk;
- provide reconciliation action;
- not rely on visual alert styling alone.

## 193. Cancellation

Cancellation confirmation must explain:

- request versus completion;
- possible external effect;
- lack of rollback;
- resulting states.

## 194. Retry

Retry controls must be absent or disabled when effect certainty is unknown.

## 195. Artifacts accessibility

Artifact workflows must support:

- metadata;
- safe preview;
- versioning;
- provenance;
- validation;
- compare;
- acceptance;
- rejection;
- quarantine;
- export;
- deletion.

## 196. Artifact preview

Safe preview must itself be accessible.

Examples:

- text extraction;
- semantic HTML;
- accessible image alternative;
- accessible PDF where available.

## 197. Inaccessible original artifact

If the original cannot be made accessible:

- provide metadata;
- provide an accessible derived representation where possible;
- disclose limitations;
- avoid forcing active rendering;
- preserve governed download where permitted.

## 198. Artifact version comparison

Provide a non-visual or screen-reader-compatible comparison.

## 199. Artifact quarantine

Quarantine reason and blocked actions must be available without relying on warning color.

## 200. Artifact upload progress

Upload progress must be announced in a throttled and understandable manner.

## 201. Artifact validation results

Validation findings should be:

- grouped;
- filterable;
- linked to location where possible;
- understandable;
- navigable by keyboard.

## 202. Memory accessibility

Memory records must expose:

- content;
- source;
- authority;
- confidence;
- freshness;
- conflicts;
- versions;
- citations.

## 203. Memory conflict

Conflicting claims require a structured comparison accessible without visual positioning alone.

## 204. Memory graph

If a visual graph is provided, an accessible list or table of nodes and relationships is required.

## 205. Agent and adapter accessibility

Agent and adapter pages must expose:

- identity;
- capability;
- readiness;
- health;
- validation;
- limitations;
- current sessions.

## 206. Capability matrix

Capability state must be readable as text and table semantics.

## 207. Model identity

Configured, selected, reported, inferred, and unknown identities must be clearly labelled in accessible names and descriptions.

## 208. Integrations accessibility

Integration details include:

- endpoint or provider;
- permissions;
- data disclosure;
- secret-reference state;
- health;
- validation.

## 209. MCP accessibility

MCP tool, resource, and prompt catalogues must be keyboard and screen-reader accessible.

Capability drift must be communicated.

## 210. Operations accessibility

Operations surfaces must support:

- dense keyboard navigation;
- alert review;
- runbook access;
- stale/unknown diagnosis;
- maintenance;
- incidents;
- backups;
- restore.

## 211. Alert accessibility

Alerts require:

- severity text;
- scope;
- source;
- freshness;
- owner;
- runbook;
- acknowledgment;
- resolution.

## 212. Critical alert announcement

Critical alerts may use assertive announcements, but duplicate announcements must be controlled.

## 213. Alert color

Severity cannot rely on red, amber, or green alone.

## 214. Alert table

The alert table needs accessible filtering, sorting, acknowledgment, and detail access.

## 215. Maintenance banner

The banner must:

- be in a meaningful landmark or status region;
- identify environment;
- explain impact;
- identify available functions;
- remain dismissible only when safe.

## 216. Emergency-stop banner

The emergency-stop state must remain persistently perceivable and programmatically available.

## 217. Incident view

Incident status, facts, unknowns, workstreams, and timeline must have semantic structure and keyboard navigation.

## 218. Backup view

Backup status distinguishes:

- completed;
- verified;
- unverified;
- failed;
- overdue;
- unknown.

## 219. Restore workflow

Restore requires:

- accessible stepper;
- exact backup and target;
- confirmation;
- progress;
- errors;
- reconciliation;
- validation;
- blocked release state.

## 220. Diagnostic bundles

Diagnostic bundle creation and export must be accessible, including classification, scope, progress, errors, and expiry.

## 221. Onboarding accessibility

Onboarding must:

- explain context;
- avoid inaccessible tours;
- support keyboard;
- support skip and resume;
- preserve progress;
- use safe simulator;
- provide alternatives to visual callouts.

## 222. Guided tours

Guided tours must not:

- trap focus;
- obscure controls;
- depend on pointer;
- force completion;
- hide page semantics.

## 223. Help and support accessibility

Support entry must be consistently located and keyboard accessible.

## 224. Support form

Support form includes:

- labels;
- impact;
- workspace/environment;
- correlation;
- attachment accessibility;
- privacy warning;
- confirmation.

## 225. Notifications accessibility

Notification preferences and messages must support:

- keyboard;
- screen readers;
- clear urgency;
- channel alternatives;
- no sound-only communication.

## 226. Email notifications

Where email is used, messages should use:

- semantic headings;
- descriptive links;
- text alternatives;
- readable layout;
- plain-text alternative where practical.

## 227. Extension UI accessibility

Extensions must meet the same requirements as core UI.

## 228. Extension declaration

Extension manifests should declare:

- interactive surfaces;
- accessibility support;
- keyboard model;
- known limitations;
- supported languages;
- test evidence.

## 229. Extension validation

Extension accessibility validation includes:

- semantics;
- keyboard;
- focus;
- contrast;
- reflow;
- screen reader;
- errors;
- extension isolation.

## 230. Extension failure

An inaccessible extension cannot block access to:

- core navigation;
- disable/revoke controls;
- audit;
- support;
- recovery.

## 231. Third-party embedded UI

Prefer API-mediated or schema-driven UI.

If an iframe or embedded third-party interface is used:

- title it;
- manage focus;
- disclose origin;
- provide fallback;
- test accessibility;
- preserve escape.

## 232. Generated content accessibility

Agent-generated UI content must not introduce:

- invalid heading structure;
- inaccessible tables;
- image-only text;
- ambiguous links;
- unsafe HTML;
- unlabeled controls.

## 233. Markdown rendering

Markdown must be rendered with:

- semantic headings;
- lists;
- tables;
- code blocks;
- links;
- sanitized HTML;
- accessible structure.

## 234. Generated documents

Where Agent OS generates documents under its control, templates should support:

- heading structure;
- reading order;
- document title;
- language;
- table headers;
- alternative text fields;
- accessible links;
- bookmarks for long documents.

## 235. PDF direction

PDF accessibility may require:

- tagged structure;
- correct reading order;
- document language;
- title;
- headings;
- table semantics;
- image alternatives;
- form-field labels.

Exact PDF conformance scope requires a separate implementation decision.

## 236. CSV exports

CSV is machine-readable but not inherently an accessible presentation.

Provide descriptive headers and accompanying context.

## 237. Print styles

Printed or PDF-rendered review records should preserve:

- title;
- state;
- source;
- timestamp;
- classification;
- decision;
- evidence references.

## 238. Localization

Accessibility must survive translation.

## 239. Language metadata

Set:

- document language;
- language changes for passages where needed.

## 240. Translation expansion

Layouts must support longer labels and instructions.

## 241. Bidirectional text

Future right-to-left support should be evaluated if required.

Do not embed logic in left/right-only visual assumptions.

## 242. Time and timezone

Screen readers and visual users should receive unambiguous date, time, and timezone.

## 243. Numeric content

Costs, percentages, durations, and counts should use locale-aware formatting and descriptive context.

## 244. Accessible content policy

Content authors must follow:

- descriptive headings;
- descriptive links;
- short paragraphs;
- direct instructions;
- canonical terminology;
- explicit uncertainty;
- no emoji-only meaning.

## 245. Link text

Avoid repetitive:

```text
Click here
Read more
Open
```

without context.

Prefer:

```text
View Run R-104 evidence
Review approval request
Open artifact version 3
```

## 246. Icon labels

Visible icon labels should be retained for high-risk and unfamiliar actions.

## 247. Error codes

Error codes supplement, not replace, plain-language explanation.

## 248. Accessibility testing strategy

Testing layers:

```text
static analysis
component automation
integration automation
manual keyboard
manual zoom and reflow
manual visual contrast
screen-reader testing
forced-colors testing
touch and target testing
cognitive walkthrough
disabled-user research
regression testing
```

## 249. Static analysis

Static tools detect:

- missing labels;
- invalid ARIA;
- duplicate IDs;
- obvious contrast issues;
- heading issues;
- language issues.

They do not prove usability.

## 250. Component automation

Each component should test:

- role;
- accessible name;
- state;
- keyboard behavior;
- focus;
- disabled/loading;
- error association.

## 251. Integration automation

Test complete flows:

- sign in;
- create task;
- start run;
- approval;
- artifact review;
- operations alert;
- settings.

## 252. Automated scan scope

Run automated accessibility checks on:

- all primary routes;
- all major dialogs;
- representative data states;
- both themes;
- required responsive widths.

## 253. Manual keyboard test

Verify:

- logical tab order;
- complete operation;
- visible focus;
- no trap;
- escape;
- skip links;
- dynamic updates;
- recovery.

## 254. Manual zoom test

Verify at least:

- 200% zoom;
- 400% zoom or equivalent reflow conditions;
- text spacing overrides;
- narrow width;
- no hidden critical context.

## 255. Screen-reader testing

Proposed baseline combinations:

```text
NVDA with current Firefox
NVDA with current Chromium-based browser
VoiceOver with current Safari
```

A commercial profile may add:

```text
JAWS with current Chromium-based browser
```

Final support commitments require ADR and actual testing capacity.

## 256. Screen-reader smoke routes

At minimum:

- sign in;
- Home;
- task detail;
- run detail;
- approval detail;
- artifact review;
- operations alert;
- settings;
- support.

## 257. Screen-reader acceptance

Verify:

- page title;
- landmarks;
- headings;
- labels;
- table structure;
- state announcements;
- dialog behavior;
- route change;
- error handling;
- decision controls.

## 258. Voice-control direction

Test that visible labels match accessible names and that core actions can be targeted using visible speech commands.

## 259. Switch-access direction

Logical keyboard order and target quality should support switch-style navigation.

## 260. Magnification

Verify:

- focus remains visible;
- sticky elements do not obscure content;
- critical state remains nearby;
- no unexpected focus movement.

## 261. Forced-colors testing

Verify:

- focus;
- selected state;
- buttons;
- inputs;
- status;
- tables;
- charts;
- dialogs;
- banners.

## 262. Reduced-motion testing

Verify:

- nonessential animation removed;
- progress remains understandable;
- no motion-triggered loss of context.

## 263. Touch testing

Verify:

- target sizes;
- spacing;
- zoom;
- orientation;
- accidental activation;
- drag alternatives;
- sticky bars.

## 264. Cognitive walkthrough

Evaluate:

- clarity;
- terminology;
- decision load;
- error prevention;
- visible next steps;
- recovery;
- time pressure;
- consistency.

## 265. Disabled-user research

Pilot and commercial readiness should include usability sessions with disabled participants where practical.

Participants should cover representative needs, not serve as proof for all disabilities.

## 266. Test data

Accessibility testing requires states including:

```text
empty
loading
ready
partial
stale
degraded
blocked
error
unknown
conflicted
maintenance
recovery
```

## 267. Critical-flow test data

Include:

- long approval;
- large diff;
- unknown effect;
- expired approval;
- quarantined artifact;
- adapter unavailable;
- restore in progress;
- critical alert;
- long translated labels.

## 268. Browser matrix direction

Final matrix should cover supported combinations across:

- Chromium;
- Firefox;
- Safari/WebKit;
- Windows;
- macOS;
- Linux where relevant;
- mobile viewport and touch.

`VVR-001` defines the selected Playwright browser-automation baseline and staged Chromium/Firefox/WebKit coverage; this document governs accessibility semantics and assistive-technology expectations rather than duplicating pixel-baseline rules.

## 269. Browser support statement

The product must publish an internal and future external support statement tied to tested versions.

## 270. Assistive-technology support statement

The support statement distinguishes:

- tested;
- expected compatible;
- known limitation;
- unsupported;
- unknown.

## 271. Test environment identity

Evidence records:

- Agent OS build;
- route;
- environment;
- browser/version;
- OS;
- assistive technology/version;
- theme;
- viewport;
- zoom;
- date;
- tester.

## 272. Evidence types

```text
automated report
manual checklist
screen-reader transcript
video
screenshot
issue record
user-research note
conformance matrix
```

## 273. Evidence storage

Evidence should be:

- versioned;
- linked to build;
- classified;
- reviewable;
- retained according to quality policy.

## 274. Conformance matrix

The matrix maps:

```text
success criterion
→ route/component/journey
→ implementation
→ test
→ result
→ evidence
→ defect/exception
```

## 275. Accessibility acceptance record

Fields:

```text
build
scope
target
tested combinations
automated result
manual result
screen-reader result
known limitations
exceptions
reviewers
decision
```

## 276. Defect severity

Proposed accessibility severity:

```text
A11Y-0 — Critical safety, security, or complete exclusion
A11Y-1 — Core journey blocked
A11Y-2 — Major barrier with limited workaround
A11Y-3 — Moderate barrier
A11Y-4 — Minor or cosmetic accessibility issue
```

## 277. A11Y-0 examples

- screen-reader user cannot identify approval target;
- keyboard user cannot reject or approve;
- focus trap prevents leaving a critical dialog;
- critical unknown effect announced as success;
- inaccessible control causes cross-workspace action;
- flashing content presents seizure risk.

## 278. A11Y-1 examples

- core task or run journey impossible by keyboard;
- authentication inaccessible;
- artifact review inaccessible;
- errors not exposed;
- mobile reflow hides critical action or risk;
- screen reader cannot navigate the main page.

## 279. A11Y-2 examples

- dense table unusable without difficult workaround;
- focus frequently obscured;
- chart lacks usable data alternative;
- large diff review significantly impaired;
- timeout warning inaccessible.

## 280. A11Y-3 examples

- heading hierarchy issue that does not block navigation;
- verbose announcements;
- low-priority target-size issue;
- inconsistent link wording.

## 281. A11Y-4 examples

- minor alternative-text wording;
- redundant announcement;
- small nonessential spacing inconsistency.

## 282. Release blockers

Block release for:

- any unresolved A11Y-0;
- unresolved A11Y-1 in a release-scope journey;
- expired accessibility exception;
- missing keyboard test for critical flows;
- missing screen-reader test for approvals;
- missing reflow test for required widths;
- known inaccessible emergency or recovery control.

## 283. Exception process

An accessibility exception must include:

- failed requirement;
- affected users;
- affected journeys;
- severity;
- technical/business reason;
- workaround;
- compensating support;
- owner;
- expiry;
- remediation;
- approvers.

## 284. Exception principles

Exceptions are:

- rare;
- time-bounded;
- visible;
- not used to bypass avoidable work;
- re-evaluated after architecture changes.

## 285. Non-waivable direction

Normally non-waivable for pilot or commercial release:

- authentication accessibility;
- keyboard access to core journeys;
- approval exactness;
- emergency-stop access;
- screen-reader access to critical state;
- seizure-safety failures;
- cross-workspace accessibility-induced risk.

## 286. Workaround quality

A workaround must be:

- available;
- documented;
- accessible;
- supportable;
- not dependent on an unavailable person;
- not materially less safe.

## 287. Accessibility debt

Examples:

- custom control not fully tested;
- unsupported screen-reader combination;
- inaccessible legacy artifact;
- missing PDF tagging;
- incomplete forced-colors support;
- chart alternative not automated.

## 288. Accessibility-debt record

Fields:

```text
debt_id
scope
user impact
severity
workaround
owner
target date
release impact
evidence
```

## 289. Definition of ready

A feature is ready for implementation when:

- accessibility behavior is specified;
- component patterns are selected;
- keyboard model is defined;
- focus behavior is defined;
- responsive behavior is defined;
- alternatives for visual/pointer interactions are defined;
- test cases exist.

## 290. Definition of done

A feature is done when:

- semantic implementation exists;
- keyboard behavior passes;
- focus passes;
- screen-reader smoke passes where required;
- contrast passes;
- reflow passes;
- errors pass;
- automated checks pass;
- evidence is recorded;
- no blocking defect remains.

## 291. Design review gate

Design review must cover:

- reading order;
- focus order;
- headings;
- labels;
- states;
- color;
- reflow;
- mobile;
- errors;
- timeouts;
- alternatives.

## 292. Component review gate

A stable component requires:

- accessibility anatomy;
- keyboard interactions;
- names/roles/states;
- focus;
- themes;
- forced colors;
- reduced motion;
- tests;
- documentation.

## 293. Journey review gate

Critical journeys require:

- keyboard walkthrough;
- screen-reader walkthrough;
- zoom/reflow;
- error path;
- stale/unknown path;
- recovery path;
- mobile constraints.

## 294. Visual verification integration

`VVR-001` requires accessibility-relevant captures for:

- focus;
- error;
- disabled;
- high contrast;
- dark theme;
- 320/375/768 widths;
- long labels;
- reduced motion states where visual.

## 295. Quality-gate integration

`QAG-001` should require:

- conformance scope;
- automated results;
- manual results;
- screen-reader results;
- exceptions;
- severity review;
- evidence manifest;
- accessibility sign-off.

## 296. Test-strategy integration

`TST-001` should include:

- component accessibility tests;
- keyboard E2E;
- screen-reader manual procedures;
- zoom/reflow;
- forced colors;
- dynamic announcements;
- approval and restore accessibility.

## 297. Security integration

Accessibility must not weaken:

- authentication;
- approval exactness;
- reauthentication;
- secret handling;
- workspace isolation;
- audit.

## 298. Data integration

Accessibility metadata may include:

- alternative text;
- captions;
- language;
- accessible title;
- document structure;
- transcript;
- known limitation.

Detailed classification and retention remain in `DAT-002`.

## 299. Operations integration

Operational runbooks should include accessibility failure handling for:

- inaccessible login;
- inaccessible critical alert;
- inaccessible approval;
- inaccessible incident page;
- broken focus after deployment.

## 300. Deployment integration

Deployment smoke tests should include:

- keyboard navigation;
- focus;
- primary route scan;
- accessibility assets/styles loaded;
- no stale inaccessible bundle.

## 301. Accessibility incident

An accessibility incident may be declared when:

- a critical user group loses access;
- an approval becomes inaccessible;
- a deployment introduces a severe barrier;
- an accessibility workaround fails during pilot.

## 302. Accessibility incident response

- identify affected users and journeys;
- contain or roll back;
- provide accessible alternative;
- communicate;
- preserve evidence;
- fix and retest;
- review root cause.

## 303. Training

Teams need training in:

- semantic HTML;
- keyboard interaction;
- ARIA;
- focus management;
- accessible content;
- accessible design;
- testing;
- document accessibility.

## 304. Developer checklist

- native element;
- accessible name;
- role/state;
- keyboard;
- focus;
- error;
- dynamic announcement;
- zoom/reflow;
- test.

## 305. Designer checklist

- reading order;
- focus order;
- visible labels;
- contrast;
- target size;
- non-color cues;
- responsive;
- error/recovery;
- reduced motion.

## 306. Content checklist

- clear headings;
- descriptive links;
- plain language;
- exact state;
- explicit uncertainty;
- alternative text;
- no image-only text;
- no emoji-only meaning.

## 307. QA checklist

- automated scan;
- keyboard;
- zoom;
- text spacing;
- dark theme;
- forced colors;
- screen reader;
- mobile;
- errors;
- dynamic state.

## 308. Accessibility statement direction

A future public accessibility statement may include:

- conformance target;
- tested scope;
- supported technologies;
- known limitations;
- contact method;
- response process;
- last review.

It requires legal and quality approval.

## 309. ACR/VPAT direction

A future commercial or procurement profile may require an Accessibility Conformance Report or equivalent.

It must be evidence-based and separately approved.

## 310. Procurement

Third-party UI components and tools should be evaluated for:

- accessibility documentation;
- keyboard behavior;
- screen-reader support;
- maintenance;
- issue response;
- licensing;
- ability to patch.

## 311. Third-party component risk

A component library accessibility claim does not prove Agent OS integration accessibility.

## 312. Accessibility telemetry

Potential privacy-safe metrics:

- keyboard-navigation failures in tests;
- accessibility defect count;
- exception age;
- route scan coverage;
- component coverage;
- user-reported barriers.

Do not collect assistive-technology use without a clear privacy basis.

## 313. User feedback

Provide an accessible channel for reporting barriers.

Capture:

- route;
- build;
- assistive technology if voluntarily provided;
- impact;
- workaround;
- urgency.

## 314. Research ethics

Research with disabled participants must:

- be accessible;
- provide compensation where appropriate;
- protect privacy;
- avoid extracting sensitive disability information unnecessarily;
- provide multiple communication methods.

## 315. Maturity stages

```text
A0 — Accessibility foundations
A1 — Core journey accessibility
A2 — Pilot conformance evidence
A3 — Controlled commercial accessibility
A4 — Formal external conformance programme
```

## 316. A0 — Foundations

Includes:

- semantic components;
- keyboard;
- focus;
- contrast;
- automated testing;
- design-system rules.

## 317. A1 — Core journeys

Includes:

- authentication;
- workspace;
- task;
- run;
- approval;
- artifact;
- operations basics.

## 318. A2 — Pilot evidence

Includes:

- screen-reader matrix;
- zoom/reflow;
- exceptions;
- disabled-user feedback;
- release gate;
- support.

## 319. A3 — Controlled commercial

Includes:

- published support statement;
- formal defect SLA direction;
- procurement evidence;
- document accessibility;
- stronger browser/AT matrix.

## 320. A4 — Formal programme

Includes:

- external audit;
- ACR/VPAT where needed;
- regular user testing;
- formal accessibility governance;
- public roadmap.

## 321. Recommended MVP posture

For MVP:

- target WCAG 2.2 AA;
- implement native semantic components;
- support full keyboard operation;
- test NVDA and VoiceOver smoke paths;
- test 320/375/768/1024 widths;
- test 200% and 400% zoom/reflow;
- block critical inaccessible approvals;
- defer formal public conformance claim until evidence is complete.

## 322. Pilot posture

Before pilot:

- core journeys pass;
- approval passes screen-reader and keyboard testing;
- operations critical controls pass;
- accessibility support channel exists;
- exceptions are approved and visible;
- no A11Y-0 or relevant A11Y-1 remains.

## 323. Controlled-commercial posture

Before controlled commercial release:

- supported browser/AT matrix approved;
- public accessibility statement considered;
- document/export accessibility scope defined;
- recurring testing and issue response established;
- commercial accessibility evidence available.

## 324. Requirement catalogue

### Semantics and structure

- `A11Y-REQ-SEM-001` — User-facing pages use semantic landmarks and headings.
- `A11Y-REQ-SEM-002` — Controls expose accessible names, roles, states, and relationships.
- `A11Y-REQ-SEM-003` — Native elements are preferred over custom widgets.
- `A11Y-REQ-SEM-004` — Page titles identify current context.
- `A11Y-REQ-SEM-005` — Responsive layouts preserve logical DOM order.
- `A11Y-REQ-SEM-006` — Generated content preserves semantic structure.
- `A11Y-REQ-SEM-007` — Extension UI follows the same semantic requirements.
- `A11Y-REQ-SEM-008` — Incorrect ARIA is treated as a defect.

### Keyboard and focus

- `A11Y-REQ-KEY-001` — Every essential function is keyboard operable.
- `A11Y-REQ-KEY-002` — No keyboard trap exists.
- `A11Y-REQ-KEY-003` — Focus is visible in all supported themes.
- `A11Y-REQ-KEY-004` — Focus order follows reading and workflow order.
- `A11Y-REQ-KEY-005` — Route and dialog focus are managed.
- `A11Y-REQ-KEY-006` — Sticky UI does not obscure focused controls.
- `A11Y-REQ-KEY-007` — Drag-and-drop has a keyboard alternative.
- `A11Y-REQ-KEY-008` — Critical actions do not rely on shortcuts.

### Perception and responsive behavior

- `A11Y-REQ-PER-001` — Meaning is not conveyed by color alone.
- `A11Y-REQ-PER-002` — Text and non-text contrast meet the approved target.
- `A11Y-REQ-PER-003` — Content supports zoom and reflow.
- `A11Y-REQ-PER-004` — Required widths avoid global horizontal scrolling.
- `A11Y-REQ-PER-005` — Text-spacing overrides do not cause loss.
- `A11Y-REQ-PER-006` — Reduced motion is respected.
- `A11Y-REQ-PER-007` — Flashing content remains within safe limits.
- `A11Y-REQ-PER-008` — Dark and forced-colors modes are tested.

### Forms and errors

- `A11Y-REQ-FRM-001` — Form controls have visible and programmatic labels.
- `A11Y-REQ-FRM-002` — Required state and instructions are explicit.
- `A11Y-REQ-FRM-003` — Errors are associated with fields and summarized.
- `A11Y-REQ-FRM-004` — Entered values are preserved where safe.
- `A11Y-REQ-FRM-005` — Date/time entry has a non-calendar keyboard path.
- `A11Y-REQ-FRM-006` — File upload has a non-drag alternative.
- `A11Y-REQ-FRM-007` — Timeouts provide warning and recovery where possible.
- `A11Y-REQ-FRM-008` — Reauthentication preserves reviewed context.

### Dynamic content and complex widgets

- `A11Y-REQ-DYN-001` — Dynamic status changes are announced appropriately.
- `A11Y-REQ-DYN-002` — High-frequency updates are throttled or summarized.
- `A11Y-REQ-DYN-003` — Dialogs, menus, tabs, and comboboxes follow tested patterns.
- `A11Y-REQ-DYN-004` — Tables expose headers, sorting, filtering, and selection.
- `A11Y-REQ-DYN-005` — Charts provide textual and tabular alternatives.
- `A11Y-REQ-DYN-006` — Code and diffs provide accessible text modes.
- `A11Y-REQ-DYN-007` — Timelines expose ordered events and gaps.
- `A11Y-REQ-DYN-008` — Virtualization is used only after accessibility validation.

### Critical Agent OS journeys

- `A11Y-REQ-CRJ-001` — Authentication is accessible.
- `A11Y-REQ-CRJ-002` — Run state and last reliable evidence are accessible.
- `A11Y-REQ-CRJ-003` — Approval exactness and decisions are accessible.
- `A11Y-REQ-CRJ-004` — Unknown effects and retry restrictions are accessible.
- `A11Y-REQ-CRJ-005` — Artifact review and quarantine are accessible.
- `A11Y-REQ-CRJ-006` — Critical alerts and emergency stop are accessible.
- `A11Y-REQ-CRJ-007` — Restore and recovery controls are accessible.
- `A11Y-REQ-CRJ-008` — Mobile restrictions provide an accessible continuation path.

### Testing and governance

- `A11Y-REQ-GOV-001` — Accessibility evidence is tied to build and environment.
- `A11Y-REQ-GOV-002` — Automated testing is supplemented by manual testing.
- `A11Y-REQ-GOV-003` — Critical journeys receive screen-reader testing.
- `A11Y-REQ-GOV-004` — Accessibility defects use controlled severity.
- `A11Y-REQ-GOV-005` — Critical defects block release.
- `A11Y-REQ-GOV-006` — Exceptions are approved, time-bounded, and monitored.
- `A11Y-REQ-GOV-007` — Accessibility debt is tracked.
- `A11Y-REQ-GOV-008` — Public conformance claims require separate approval.

## 325. Traceability

| Source | A11Y-001 response |
|---|---|
| `NFR-001` | Accessibility and usability targets |
| `PER-001` | User abilities, contexts, and needs |
| `UCD-001` | Critical journeys and alternate paths |
| `UXA-001` | Information architecture, state, responsive priorities |
| `DSN-001` | Tokens, components, themes, patterns |
| `RUN-001` | Run, step, attempt, cancellation, recovery |
| `APR-001` | Exact approval and consumption |
| `ART-001` | Artifact review, preview, quarantine |
| `MEM-001` | Memory source, authority, conflict |
| `MOD-001` | Model identity and cost states |
| `OBS-001` | Alerts, charts, freshness, health |
| `OPS-001` | Maintenance, incident, emergency, restore |
| `PLG-001` | Extension UI accessibility |
| `TST-001` | Test strategy and evidence |
| `QAG-001` | Release gates and exception control |

## 326. ADR backlog

### `ADR-TBD-A11Y-001 — Accessibility target and supported scope`

WCAG 2.2 AA is the approved Product/UX/Quality target direction. This ADR remains needed to complete Architecture, Security, Data, and Operations agreement on the controlled conformance scope, included surfaces, generated documents, and third-party-content policy.

### `ADR-TBD-A11Y-002 — Browser and assistive-technology support matrix`

Approve tested browser, operating-system, screen-reader, zoom, forced-colors, and touch combinations.

### `ADR-TBD-A11Y-003 — Component interaction patterns`

Approve keyboard/focus patterns for menus, dialogs, comboboxes, tables, grids, timelines, diff viewers, and command palettes.

### `ADR-TBD-A11Y-004 — Accessibility test and evidence stack`

Select automated accessibility tools, test harnesses, evidence format, reporting, regression integration, and storage. Browser visual automation itself is governed by `VVR-001`.

### `ADR-TBD-A11Y-005 — Accessibility exceptions and release governance`

Approve severity, blockers, exception authority, expiry, remediation, and public claim process.

### `ADR-TBD-A11Y-006 — Document and export accessibility`

Define HTML, PDF, presentation, spreadsheet, email, and export accessibility scope and tooling.

## 327. Open decisions

1. Complete Architecture, Security, Data, and Operations approval of `A11Y-001`.
2. Define exact WCAG 2.2 AA conformance scope before any public conformance claim.
3. Confirm browser/assistive-technology support matrix.
4. Confirm NVDA browser combinations.
5. Confirm VoiceOver/Safari support.
6. Decide whether JAWS enters pilot or commercial testing.
7. Confirm forced-colors support.
8. Confirm high-contrast theme requirement.
9. Confirm required zoom and reflow tests beyond the baseline already stated.
10. Confirm target-size interpretation for compact operations.
11. Confirm virtualized-table policy.
12. Confirm accessible diff-viewer implementation.
13. Confirm chart alternative format.
14. Confirm PDF/export accessibility scope.
15. Confirm disabled-user research schedule.
16. Confirm accessibility defect response targets.
17. Confirm exception approvers.
18. Confirm public accessibility-statement timing.
19. Confirm ACR/VPAT need.
20. Confirm automated accessibility test tools.
21. Confirm evidence storage.
22. Confirm extension accessibility validation.
23. Confirm mobile approval restrictions.
24. Resolve whether `UIF-001` remains a separate state contract.

## 328. Risks

| Risk | Consequence | Response |
|---|---|---|
| Automated scan treated as proof | Major barriers missed | Manual/AT testing |
| Custom controls overused | Broken keyboard/semantics | Native-first |
| ARIA added incorrectly | Worse accessibility | Tested patterns |
| Focus hidden by sticky UI | Keyboard exclusion | Focus-not-obscured testing |
| Large diff inaccessible | Unsafe approval | Text alternative/desktop path |
| Color-only unknown state | Unsafe retry | Redundant cues |
| Virtualized tables break AT | Operations exclusion | Validate or paginate |
| Mobile hides review context | Unsafe approval | Block/accessible continuation |
| Toast carries only result | Missed critical feedback | Persistent state |
| Dynamic updates overwhelm | Screen-reader overload | Throttling |
| Dark mode untested | Contrast failures | Independent validation |
| Forced-colors ignored | Control invisibility | Dedicated testing |
| PDF output inaccessible | Procurement/user barrier | Scope and tagging |
| Extension UI bypasses rules | Fragmented accessibility | Validation and isolation |
| Timeout loses work | Cognitive/motor barrier | Warning and draft preservation |
| CAPTCHA inaccessible | Authentication exclusion | Accessible alternative |
| Accessible path weakens security | Security incident | Preserve exact authority |
| Exception becomes permanent | Persistent exclusion | Expiry and gate |
| No disabled-user testing | Design assumptions persist | Research |
| Accessibility added after UI | Expensive rework | Definition of ready |

## 329. Assumptions

- Agent OS uses a browser-based primary interface;
- semantic HTML is available;
- UXA-001 and DSN-001 define architecture and components;
- accessibility can be included in CI and manual review;
- testing environments can use NVDA and VoiceOver;
- core flows can avoid inaccessible third-party embeds;
- high-risk mobile workflows may be constrained;
- accessibility support can be part of pilot operations;
- formal public conformance claims are deferred;
- disabled-user research is feasible before broader commercialization.

## 330. Constraints

- no unsupported conformance claim;
- no mouse-only essential function;
- no color-only state;
- no keyboard trap;
- no inaccessible approval decision;
- no inaccessible emergency-stop release path;
- no raw secret exposure through accessibility APIs;
- no critical status delivered only through toast or sound;
- no global horizontal scrolling at required reflow widths;
- no automated-test-only sign-off;
- no permanent unapproved accessibility exception.

## 331. Acceptance criteria

A11Y-001 may advance from `in-review` to `approved` when:

1. Product, UX, and Quality approvals remain recorded.
2. Architecture accepts semantic, interaction, dynamic-content, and extension boundaries.
3. Security accepts authentication, approval, reauthentication, and secret-accessibility controls.
4. Data accepts accessible metadata, document, export, and retention implications.
5. Operations accepts accessible alerts, incidents, maintenance, emergency, and recovery.
6. the WCAG 2.2 AA target scope is explicitly accepted across the required roles;
7. browser/assistive-technology matrix is approved;
8. critical journey test matrix is approved;
9. approval, run, artifact, and operations requirements are accepted;
10. automated and manual test responsibilities are assigned;
11. accessibility evidence format is defined;
12. exception process is approved;
13. `VVR-001` can consume these requirements for visual and interaction regression without changing them.

Implementation evidence remains separate from document approval; neither this document nor the repository currently claims WCAG conformance.

## 332. Downstream impact

| Document | Required use |
|---|---|
| `VVR-001` | Focus, contrast, reflow, theme, error, and responsive evidence |
| `IAM-001` | Accessible authentication, sessions, roles, reauthentication |
| `POL-001` | Accessible decision explanation and simulation |
| `SAN-001` | Accessible execution state and violation handling |
| `SEC-002` | Accessibility-related control catalogue and evidence |
| `DAT-002` | Accessibility metadata, document, retention, and deletion |
| `AUD-001` | Accessible timelines, receipts, and evidence exports |
| `CST-001` | Accessible costs, budgets, charts, and tables |
| `ADP-HER-001` | Accessible capability/session/tool/model state |
| `ADP-CDX-001` | Accessible repository, command, test, and diff review |
| Document register | Keep status, version, and dependencies synchronized |

## 333. Revision and approval history

### Approval state

- Current status: `in-review`
- Current version: `1.0.1`
- Product Owner: approved 2026-08-13
- UX Owner: approved 2026-08-13
- Quality Owner: approved 2026-08-13
- Architecture Owner: pending
- Security Owner: pending
- Data Owner: pending
- Operations Owner: pending

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial accessibility requirements and conformance plan covering WCAG 2.2 AA direction, semantics, keyboard, focus, names/roles/states, contrast, reflow, forms, authentication, tables, charts, code/diffs, dynamic content, approvals, runs, artifacts, operations, responsive behavior, testing, evidence, exceptions, and release gates |
| 1.0.0 | 2026-08-13 | Inconsistent approval metadata | Front matter stated approved while the body remained draft and specialist approval records were incomplete |
| 1.0.1 | 2026-08-13 | In review | Harmonized approval state, preserved Product/UX/Quality approvals, retained WCAG 2.2 AA direction, and recorded pending specialist reviews |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `NFR-001` — Non-Functional Requirements
- `UXA-001` — UX Architecture and User Journey Specification — registered
- `DSN-001` — Agent OS Design System Specification — registered
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `MEM-001` — Memory and Knowledge Architecture
- `MOD-001` — Model Profile Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `PLG-001` — Plugin and Extension Architecture
- `TST-001` — Test Strategy and Verification Plan
- `QAG-001` — Quality Assurance and Release Gates
- `VVR-001` — Visual Validation and Regression Plan
