---
document_id: DSN-001
title: Agent OS Design System Specification
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
related_documents: []
dependencies:
  - UXA-001
  - NFR-001
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
  - DDD-001
  - DAT-001
  - DCT-001
  - RUN-001
  - APR-001
  - ART-001
  - MOD-001
  - API-001
  - EVT-001
  - TST-001
  - QAG-001
  - OBS-001
  - DEP-001
  - OPS-001
  - PLG-001
related_proposed_documents:
  - UXA-001
  - A11Y-001
  - VVR-001
  - UIF-001
related_adrs:
  - ADR-TBD-DSN-001
  - ADR-TBD-DSN-002
  - ADR-TBD-DSN-003
  - ADR-TBD-DSN-004
  - ADR-TBD-DSN-005
  - ADR-TBD-DSN-006
related_evidence:
  - VIDEO-002
  - VIDEO-003
  - VIDEO-004
---

# DSN-001 — Agent OS Design System Specification

> **Status: Draft — proposed/unregistered.** This document defines the proposed Agent OS design system: visual foundations, semantic tokens, themes, typography, spacing, grid, iconography, motion, component contracts, Mission Control patterns, responsive behavior, accessibility foundations, content style, implementation governance, documentation, testing, and release controls. It does not approve a final commercial brand identity, final implementation framework, final component library, final design-tool workflow, or final accessibility conformance process.

## 1. Purpose

Agent OS needs a design system capable of supporting:

- dense operational dashboards;
- high-risk approvals;
- long-running workflows;
- stale and unknown states;
- artifacts and previews;
- memory and provenance;
- agents, adapters, models, and tools;
- incidents and recovery;
- responsive and accessible user journeys;
- future extensions and plugins.

The design system must make the product:

1. understandable;
2. consistent;
3. accessible;
4. trustworthy;
5. efficient;
6. visually calm;
7. operationally dense when required;
8. safe under uncertainty;
9. reusable across teams;
10. testable and versioned.

## 2. Design-system objectives

The system must:

- provide one semantic token language;
- keep meaning independent from raw colors;
- support light, dark, and system appearance;
- support high-density operations;
- preserve readable hierarchy;
- support 320 px through wide desktop;
- make focus and keyboard states explicit;
- make loading, stale, partial, degraded, unknown, and conflict states consistent;
- make high-risk actions visually distinct;
- make approvals deliberate;
- provide accessible data tables and charts;
- support code, diff, artifact, and timeline views;
- prevent arbitrary local styling;
- support visual-regression testing;
- document component behavior and usage;
- support future first-party extensions without visual fragmentation;
- separate design tokens from brand decisions.

## 3. Non-goals

This document does not:

- define a marketing website;
- define a logo;
- define illustration campaigns;
- define a final trademark palette;
- mandate one CSS or component framework;
- define the final Figma or design-tool organisation;
- replace accessibility specifications;
- replace UX architecture;
- replace visual-verification procedures;
- permit component variants without documented semantics;
- allow color-only meaning;
- allow decorative animation to hide state;
- require every page to use cards;
- define mobile parity for every expert workflow.

## 4. Design principles

### `DSN-P-001 — Calm control plane`

The interface should feel controlled, deliberate, and stable even when the underlying system is complex.

### `DSN-P-002 — Semantics before decoration`

Tokens and components are named by meaning and function, not by visual appearance alone.

### `DSN-P-003 — Operational truth is visually explicit`

State, source, freshness, and limitations must be visible before secondary decoration.

### `DSN-P-004 — Density is configurable`

The system supports comfortable and compact modes without losing labels, focus, or critical context.

### `DSN-P-005 — Accessibility is structural`

Contrast, focus, target size, semantics, reflow, and motion are built into component contracts.

### `DSN-P-006 — Risk is not a color alone`

Risk uses text, icon, shape, hierarchy, and language in addition to color.

### `DSN-P-007 — Components expose state`

Every component documents loading, empty, partial, stale, degraded, blocked, error, unknown, and disabled behavior where applicable.

### `DSN-P-008 — No one-off styling for critical flows`

Approvals, destructive actions, emergency states, and recovery use controlled patterns.

### `DSN-P-009 — Visual hierarchy follows decision hierarchy`

The most important state or action receives the strongest emphasis.

### `DSN-P-010 — Responsive means restructured, not merely compressed`

Complex desktop layouts reorganize meaningfully at smaller widths.

### `DSN-P-011 — Extension surfaces inherit governance`

Plugins and extensions use controlled tokens, components, and accessibility rules.

### `DSN-P-012 — Visual claims require evidence`

A component is not considered complete until its states, responsive behavior, and accessibility are verified.

## 5. Design-system layers

```text
Foundations
→ Semantic tokens
→ Primitives
→ Components
→ Composite patterns
→ Page templates
→ Domain patterns
→ Product experiences
```

## 6. Foundations

Foundations include:

- color;
- typography;
- spacing;
- sizing;
- grid;
- radius;
- border;
- shadow;
- motion;
- iconography;
- content style;
- breakpoints.

## 7. Semantic tokens

Semantic tokens map foundations to meaning.

Examples:

```text
surface.canvas
surface.panel
text.primary
border.subtle
status.success
risk.critical
action.primary
focus.ring
```

## 8. Primitives

Primitives include:

- box;
- stack;
- inline;
- grid;
- text;
- icon;
- divider;
- scroll area;
- visually hidden;
- portal.

## 9. Components

Components include:

- buttons;
- inputs;
- tables;
- dialogs;
- banners;
- tabs;
- badges;
- cards;
- timelines;
- status indicators;
- data displays.

## 10. Composite patterns

Composite patterns include:

- page header;
- approval review;
- run status;
- artifact review;
- empty state;
- error recovery;
- filter toolbar;
- detail panel;
- command confirmation.

## 11. Page templates

Templates include:

- list/detail;
- dashboard;
- review;
- settings;
- operations;
- incident;
- wizard;
- split view;
- comparison.

## 12. Domain patterns

Domain-specific patterns include:

- run lifecycle;
- approval consumption;
- model identity;
- capability readiness;
- artifact provenance;
- memory authority;
- cost certainty;
- event freshness.

## 13. Product experiences

Product experiences assemble the system into Mission Control, onboarding, operations, and review journeys.

## 14. Token architecture

Token tiers:

```text
reference tokens
semantic tokens
component tokens
instance overrides
```

## 15. Reference tokens

Reference tokens define raw values.

Examples:

```text
color.blue.600
space.4
radius.md
font.size.200
shadow.200
duration.fast
```

## 16. Semantic tokens

Examples:

```text
surface.canvas
surface.raised
text.muted
status.warning.background
action.danger.text
```

## 17. Component tokens

Examples:

```text
button.primary.background
table.row.hover
dialog.width.lg
run.state.unknown.icon
approval.footer.border
```

## 18. Instance overrides

Instance overrides are rare and documented.

They must not bypass semantic meaning or accessibility.

## 19. Token naming rules

Token names should be:

- lowercase;
- dot-separated;
- semantic;
- stable;
- technology-neutral;
- independent from implementation class names.

## 20. Token anti-patterns

Avoid:

```text
blueButton
gray3
bigGap
cardShadow2
redText
```

Prefer:

```text
action.primary.background
surface.subtle
space.section
elevation.overlay
text.danger
```

## 21. Token metadata

Each token records:

- name;
- type;
- value;
- theme;
- purpose;
- contrast requirements;
- deprecation;
- owner;
- version.

## 22. Token types

```text
color
dimension
font
fontWeight
lineHeight
letterSpacing
border
radius
shadow
duration
easing
opacity
zIndex
```

## 23. Token source format

A future machine-readable source may use:

- JSON;
- YAML;
- Design Tokens Community Group-compatible format;
- generated CSS variables;
- generated TypeScript types.

Final format requires ADR.

## 24. Token generation

The pipeline should generate:

- CSS custom properties;
- typed application tokens;
- design-tool mappings where selected;
- documentation tables;
- contrast tests;
- theme files.

## 25. Theme model

Supported themes:

```text
light
dark
system
```

Future optional themes:

```text
high_contrast_light
high_contrast_dark
```

## 26. Theme selection

Theme may follow:

- user preference;
- system preference;
- workspace policy only where justified.

Theme cannot hide severity or critical state.

## 27. Theme persistence

Persist as a user preference.

Avoid layout flicker during initial render.

## 28. Theme independence

Components use semantic tokens only.

No component should hard-code a light-theme color.

## 29. Reference color palette

The following palette is a **reference direction**, not a final commercial brand lock.

### Neutral scale

```text
neutral.0    #FFFFFF
neutral.25   #FCFCFD
neutral.50   #F8FAFC
neutral.100  #F1F5F9
neutral.200  #E2E8F0
neutral.300  #CBD5E1
neutral.400  #94A3B8
neutral.500  #64748B
neutral.600  #475569
neutral.700  #334155
neutral.800  #1E293B
neutral.900  #0F172A
neutral.950  #020617
```

## 30. Reference primary scale

Proposed control-plane blue:

```text
primary.50   #EEF4FF
primary.100  #DDE8FF
primary.200  #B9CEFF
primary.300  #8DADFF
primary.400  #6388F2
primary.500  #4568E6
primary.600  #3154CC
primary.700  #2946A8
primary.800  #253D86
primary.900  #22376B
```

## 31. Reference success scale

```text
success.50   #ECFDF5
success.100  #D1FAE5
success.200  #A7F3D0
success.300  #6EE7B7
success.400  #34D399
success.500  #10B981
success.600  #07815E
success.700  #08664D
success.800  #07513F
success.900  #064334
```

## 32. Reference warning scale

```text
warning.50   #FFFBEB
warning.100  #FEF3C7
warning.200  #FDE68A
warning.300  #FCD34D
warning.400  #FBBF24
warning.500  #F59E0B
warning.600  #B96B00
warning.700  #8A4F00
warning.800  #713F12
warning.900  #5B3410
```

## 33. Reference danger scale

```text
danger.50   #FFF1F2
danger.100  #FFE4E6
danger.200  #FECDD3
danger.300  #FDA4AF
danger.400  #FB7185
danger.500  #F43F5E
danger.600  #BE123C
danger.700  #9F1239
danger.800  #881337
danger.900  #701A30
```

## 34. Reference information scale

Information may reuse the primary scale or a distinct cyan scale if visual differentiation is validated.

## 35. Reference unknown scale

A restrained violet is proposed for unknown or unresolved state.

```text
unknown.50   #F5F3FF
unknown.100  #EDE9FE
unknown.200  #DDD6FE
unknown.300  #C4B5FD
unknown.400  #A78BFA
unknown.500  #8B5CF6
unknown.600  #6D3FD1
unknown.700  #5B32B0
unknown.800  #4C2B8F
unknown.900  #3F2672
```

## 36. Unknown color caution

Unknown is not a decorative “AI purple.”

It must communicate unresolved state and always include text.

## 37. Light-theme semantic surfaces

```text
surface.canvas              neutral.50
surface.panel               neutral.0
surface.subtle              neutral.100
surface.sunken              neutral.100
surface.overlay             neutral.0
surface.disabled            neutral.100
surface.inverse             neutral.900
```

## 38. Dark-theme semantic surfaces

```text
surface.canvas              neutral.950
surface.panel               neutral.900
surface.subtle              neutral.800
surface.sunken              neutral.950
surface.overlay             neutral.800
surface.disabled            neutral.800
surface.inverse             neutral.50
```

## 39. Light-theme semantic text

```text
text.primary                neutral.900
text.secondary              neutral.700
text.muted                  neutral.600
text.disabled               neutral.400
text.inverse                neutral.0
text.link                   primary.700
text.success                success.700
text.warning                warning.700
text.danger                 danger.700
text.unknown                unknown.700
```

## 40. Dark-theme semantic text

```text
text.primary                neutral.50
text.secondary              neutral.200
text.muted                  neutral.300
text.disabled               neutral.500
text.inverse                neutral.950
text.link                   primary.300
text.success                success.300
text.warning                warning.300
text.danger                 danger.300
text.unknown                unknown.300
```

## 41. Semantic borders

```text
border.subtle
border.default
border.strong
border.interactive
border.focus
border.success
border.warning
border.danger
border.unknown
```

## 42. Semantic status colors

```text
status.neutral
status.info
status.success
status.warning
status.danger
status.unknown
status.stale
status.degraded
status.blocked
```

## 43. State color mapping

Proposed direction:

| State | Semantic family |
|---|---|
| Ready / healthy | success |
| Informational | info / primary |
| Waiting | neutral / info |
| Warning | warning |
| Error / failed | danger |
| Unknown | unknown |
| Stale | warning |
| Degraded | warning |
| Blocked | danger or warning depending reason |
| Maintenance | info |
| Recovery | unknown / warning |

## 44. State mapping caution

Color does not determine business semantics.

Text and icon must identify the actual state.

## 45. Contrast requirements

All text, controls, icons, borders, and focus indicators must meet the approved accessibility target.

Detailed thresholds and test matrix belong in proposed/unregistered `A11Y-001`.

## 46. Contrast governance

Contrast is tested:

- at token level;
- at component level;
- in both themes;
- in interactive states;
- in disabled and selected states;
- under forced colors where supported.

## 47. Typography principles

Typography should be:

- readable;
- compact enough for operations;
- consistent;
- language-flexible;
- accessible;
- clear for code and identifiers.

## 48. Font strategy

Preferred direction:

```text
UI sans-serif:
system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif

Code/identifier:
ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace
```

A branded typeface may be introduced later if loading, licensing, and accessibility are acceptable.

## 49. Typography scale

Proposed scale:

```text
font.size.050   11px
font.size.100   12px
font.size.200   13px
font.size.300   14px
font.size.400   16px
font.size.500   18px
font.size.600   20px
font.size.700   24px
font.size.800   30px
font.size.900   36px
font.size.1000  48px
```

## 50. Minimum text size

`11px` may be used only for nonessential dense metadata with adequate contrast and user zoom support.

Default body should remain at least `14px`, preferably `16px` for ordinary reading surfaces.

## 51. Line-height scale

```text
lineHeight.tight     1.2
lineHeight.snug      1.35
lineHeight.normal    1.5
lineHeight.relaxed   1.65
```

## 52. Font-weight scale

```text
font.weight.regular    400
font.weight.medium     500
font.weight.semibold   600
font.weight.bold       700
```

Avoid excessive use of bold.

## 53. Text styles

```text
display
pageTitle
sectionTitle
subsectionTitle
body
bodyStrong
bodyCompact
label
caption
metadata
code
numeric
```

## 54. Page title

Recommended:

- 24–30 px desktop;
- 20–24 px mobile;
- semibold;
- short;
- accompanied by state and actions.

## 55. Section title

Recommended:

- 18–20 px;
- semibold;
- visible hierarchy;
- no all caps.

## 56. Label style

Form labels:

- 13–14 px;
- medium or semibold;
- positioned consistently;
- required status not color-only.

## 57. Metadata style

- compact;
- lower visual emphasis;
- still readable;
- source/freshness labels must not become illegible.

## 58. Code style

Use monospace for:

- code;
- IDs;
- hashes;
- paths;
- fingerprints;
- commands;
- diffs.

Do not use monospace for long explanatory paragraphs.

## 59. Numeric style

Consider tabular numbers for:

- costs;
- durations;
- counts;
- timestamps;
- metrics.

## 60. Line length

Recommended reading width:

```text
45–80 characters
```

Operational tables and code views are exceptions.

## 61. Spacing scale

Base unit direction: `4px`.

```text
space.0    0
space.1    4px
space.2    8px
space.3    12px
space.4    16px
space.5    20px
space.6    24px
space.8    32px
space.10   40px
space.12   48px
space.16   64px
space.20   80px
space.24   96px
```

## 62. Spacing semantics

```text
space.inlineTight
space.inline
space.controlGap
space.fieldGap
space.cardPadding
space.section
space.page
space.layout
```

## 63. Density modes

```text
comfortable
compact
```

## 64. Comfortable density

Typical values:

- 44 px control height;
- 16 px card padding;
- 48–52 px table rows;
- 16–24 px section gaps.

## 65. Compact density

Typical values:

- 36 px control height;
- 12 px card padding;
- 36–40 px table rows;
- 12–16 px section gaps.

## 66. Density accessibility

Compact mode must retain:

- adequate touch targets where touch is expected;
- visible focus;
- readable labels;
- non-overlapping content;
- accessible hit areas.

## 67. Sizing scale

Recommended control heights:

```text
control.xs   28px
control.sm   32px
control.md   36px
control.lg   44px
control.xl   52px
```

## 68. Touch targets

Interactive target area should satisfy the approved accessibility target even if the visual element is smaller.

## 69. Radius scale

```text
radius.none   0
radius.xs     2px
radius.sm     4px
radius.md     6px
radius.lg     8px
radius.xl     12px
radius.full   999px
```

## 70. Radius direction

Use moderate radii.

Agent OS should not become excessively pill-shaped or playful in high-density operational surfaces.

## 71. Border scale

```text
border.width.0   0
border.width.1   1px
border.width.2   2px
```

Focus rings may use 2–3 px combined outline and offset.

## 72. Shadow scale

```text
shadow.none
shadow.100   subtle raised surface
shadow.200   menu/popover
shadow.300   dialog/drawer
shadow.400   critical overlay
```

## 73. Shadow principles

- avoid shadow-only boundaries;
- preserve borders in dark theme;
- use sparingly;
- do not imply interactivity solely with elevation.

## 74. Elevation layers

```text
base
raised
sticky
popover
dialog
toast
criticalOverlay
```

## 75. Z-index scale

A controlled z-index scale prevents arbitrary values.

Example:

```text
z.base             0
z.sticky           100
z.dropdown         200
z.popover          300
z.drawer           400
z.dialog           500
z.toast            600
z.criticalOverlay  700
```

## 76. Z-index rule

Components cannot introduce arbitrary values outside the scale.

## 77. Grid system

Desktop grid direction:

```text
12 columns
24 px gutters
responsive margins
```

Tablet:

```text
8 columns
16–24 px gutters
```

Mobile:

```text
4 columns
16 px margins
```

## 78. Page width

Use:

- fluid layout;
- bounded reading widths;
- full-width operational tables where needed;
- optional wide mode for timelines and diffs.

## 79. Layout primitives

Required primitives:

```text
Stack
Inline
Cluster
Grid
Split
Sidebar
Container
ScrollArea
VisuallyHidden
```

## 80. Stack

Vertical arrangement with semantic gap tokens.

## 81. Inline

Horizontal arrangement with wrapping and alignment.

## 82. Cluster

Flexible grouping for tags, actions, filters, or metadata.

## 83. Split

Two-region layout for main content and context.

## 84. Sidebar

Controlled width, collapse behavior, and mobile drawer adaptation.

## 85. Container

Defines readable width and responsive page padding.

## 86. Scroll area

Creates local scrolling without causing global horizontal overflow.

## 87. Breakpoints

Reference breakpoints:

```text
xs   320px
sm   375px
md   768px
lg   1024px
xl   1280px
2xl  1440px
```

## 88. Breakpoint principle

Design around content needs rather than device names.

## 89. Responsive priorities

At smaller widths:

1. preserve state;
2. preserve required action;
3. preserve critical context;
4. reduce secondary metadata;
5. reorganize layout;
6. defer expert-only views where necessary.

## 90. Global overflow rule

No page-level horizontal overflow at required widths.

Scoped scroll areas are permitted for:

- code;
- diffs;
- wide tables;
- timelines;
- diagrams.

## 91. Iconography principles

Icons should be:

- consistent;
- simple;
- stroke or fill style controlled;
- recognizable;
- paired with text for ambiguous actions;
- accessible.

## 92. Icon size scale

```text
icon.xs   12px
icon.sm   16px
icon.md   20px
icon.lg   24px
icon.xl   32px
```

## 93. Icon-only buttons

Require:

- accessible name;
- tooltip where helpful;
- adequate target;
- visible focus;
- no icon-only critical action unless universally clear and reviewed.

## 94. State icons

Proposed semantic icon families:

- check for confirmed success;
- clock for waiting;
- warning triangle for warning;
- error octagon for critical failure;
- question mark or unresolved symbol for unknown;
- pause/maintenance tool for maintenance;
- circular arrows for recovery;
- shield for security control;
- key/person for approval/authority.

## 95. Illustration principles

Illustrations may support onboarding and empty states.

They must not:

- trivialize security;
- obscure operational state;
- consume excessive space;
- introduce inaccessible text in images.

## 96. Motion principles

Motion supports:

- orientation;
- state transition;
- hierarchy;
- feedback.

Motion does not replace text or state.

## 97. Duration scale

```text
duration.instant   0ms
duration.fast      100ms
duration.normal    180ms
duration.slow      280ms
duration.deliberate 400ms
```

## 98. Easing

Proposed:

```text
easing.standard
easing.enter
easing.exit
easing.emphasized
```

Exact curves require implementation validation.

## 99. Reduced motion

When reduced motion is requested:

- disable nonessential transitions;
- avoid parallax;
- avoid animated counters;
- preserve immediate state feedback;
- use opacity changes carefully.

## 100. Progress motion

Never use animation to imply measurable progress when none exists.

Indeterminate progress is labelled as such.

## 101. Content style principles

Content should be:

- direct;
- specific;
- calm;
- actionable;
- source-aware;
- honest about uncertainty;
- free from unsupported anthropomorphism.

## 102. Voice

Agent OS voice:

```text
precise
calm
transparent
professional
non-dramatic
non-promotional
```

## 103. Button labels

Prefer verb + object:

```text
Create task
Start run
Request approval
Review artifact
Reconcile run
Activate maintenance
```

Avoid vague labels:

```text
OK
Submit
Continue
Do it
```

when more specific wording is available.

## 104. State language

Use canonical terms consistently.

Examples:

```text
Waiting for approval
Cancellation requested
Effect state unknown
Artifact quarantined
Adapter unavailable
```

## 105. Error content

Error pattern:

```text
What happened
What is affected
What remains safe
What the user can do
Correlation or support reference
```

## 106. Unknown content

Example:

```text
We cannot confirm whether the external action completed.
The last reliable evidence was recorded at 14:32 UTC.
Retry is blocked until reconciliation is complete.
```

## 107. Empty-state content

Explain:

- why empty;
- whether data is absent or filtered;
- safest next action;
- relevant permission or limitation.

## 108. Warning content

Warnings should explain consequence.

Avoid generic:

```text
Are you sure?
```

Prefer:

```text
This will revoke the adapter for three workspaces and block new runs.
Active attempts may require reconciliation.
```

## 109. Tooltip content

Tooltips provide short clarification, not essential instructions.

Essential content must remain visible or accessible elsewhere.

## 110. Terminology governance

The design system references controlled terms from `GLO-001`.

UI labels must not invent synonyms that change meaning.

## 111. Component anatomy documentation

Every component specification should include:

```text
purpose
anatomy
variants
sizes
states
behaviors
responsive rules
accessibility
content
tokens
examples
anti-patterns
tests
```

## 112. Component maturity

```text
experimental
candidate
stable
deprecated
retired
```

## 113. Experimental component

May be used only in controlled prototypes or behind explicit scope.

## 114. Candidate component

Implementation exists and is undergoing validation.

## 115. Stable component

Approved for production use with documented states and tests.

## 116. Deprecated component

Supported temporarily but not for new work.

## 117. Retired component

Removed from use; migration complete.

## 118. Component versioning

Breaking changes require:

- migration guide;
- deprecation period;
- visual review;
- accessibility review;
- version update.

## 119. Primitive — Box

Purpose:

- semantic surface wrapper;
- tokenised padding, border, background, radius.

It should not become an unstructured arbitrary styling escape hatch.

## 120. Primitive — Text

Purpose:

- controlled typography;
- semantic text styles;
- truncation and wrapping rules;
- accessible element selection.

## 121. Primitive — Stack

Purpose:

- vertical rhythm;
- no arbitrary margin collapse;
- predictable responsive gaps.

## 122. Primitive — Inline

Purpose:

- horizontal alignment;
- wrapping;
- controlled gaps;
- baseline alignment.

## 123. Primitive — Divider

Supports:

- horizontal;
- vertical;
- labelled section divider where needed.

Must meet contrast requirements.

## 124. Button architecture

Button variants:

```text
primary
secondary
tertiary
quiet
danger
link
```

## 125. Button sizes

```text
sm
md
lg
```

## 126. Button states

```text
default
hover
active
focus
disabled
loading
pressed
```

## 127. Primary button

Use for one dominant action per context.

Avoid multiple competing primary actions in one decision area.

## 128. Secondary button

Use for alternative actions.

## 129. Tertiary button

Use for low-emphasis actions that remain discoverable.

## 130. Quiet button

Use for compact toolbars and contextual actions.

## 131. Danger button

Use only for destructive or high-risk action.

Danger styling is not sufficient; confirmation and exact language remain required.

## 132. Loading button

- retains width;
- indicates operation accepted or pending;
- prevents accidental duplicate activation;
- does not show success until confirmed.

## 133. Disabled button

Must have:

- accessible disabled state;
- explanation where reason is not obvious;
- no inaccessible tooltip-only explanation.

## 134. Split button

Use sparingly.

Primary action and menu alternatives must be clearly related.

Not recommended for high-risk approval decisions.

## 135. Icon button

Requires accessible name and controlled hit target.

## 136. Link component

Variants:

```text
inline
standalone
subtle
external
```

External links indicate new origin and relevant risk where needed.

## 137. Text input

Anatomy:

- label;
- input;
- optional description;
- optional prefix/suffix;
- validation;
- error;
- character count where needed.

## 138. Input states

```text
default
focus
filled
disabled
read_only
error
warning
success
loading
```

## 139. Input validation

- validate after reasonable interaction;
- preserve typed value;
- show field and summary error;
- avoid red-only indication;
- do not expose secret value.

## 140. Password and secret fields

Raw secret entry, where unavoidable:

- obscured by default;
- no value in logs;
- reveal control with accessible state;
- no accidental persistence;
- clear scope/purpose.

Preferred UX uses secret references rather than repeated secret entry.

## 141. Textarea

Supports:

- resize rules;
- character/size limit;
- autosize with maximum;
- markdown/code mode only when explicit.

## 142. Search input

Supports:

- accessible search role;
- clear button;
- loading;
- empty;
- stale-index state;
- shortcut hint.

## 143. Select

Use native or accessible custom select.

Must support:

- keyboard;
- typeahead;
- disabled options;
- clear value;
- loading;
- long labels.

## 144. Combobox

Use for searchable selections with many options.

Must expose:

- input;
- list;
- active option;
- selected values;
- loading and no results.

## 145. Multi-select

Display selected items without excessive chips.

Provide summary when many values are selected.

## 146. Checkbox

Use for independent binary selections.

Indeterminate state must be explicit.

## 147. Radio group

Use for mutually exclusive choices.

All options remain visible where feasible.

## 148. Switch

Use for immediate on/off settings only.

Do not use for actions requiring approval, complex consequences, or form submission.

## 149. Date and time input

Must display:

- timezone;
- locale;
- absolute value;
- validation;
- expiry meaning.

## 150. File input

Supports:

- local selection;
- preview where safe;
- filename/type/size;
- validation;
- progress;
- cancellation;
- retry;
- quarantine.

## 151. URL input

May be optional fallback where product workflows permit.

Must validate scheme and destination policy.

## 152. Form field group

Groups related fields with legend or heading.

## 153. Form layout

Desktop:

- single column for complex review;
- two columns for short related fields;
- avoid overly wide fields.

Mobile:

- single column;
- logical order;
- sticky actions only when safe.

## 154. Form actions

Order should be consistent:

```text
primary action
secondary action
cancel/back
```

High-risk flows may reverse emphasis to prevent accidental action only when documented and tested.

## 155. Error summary

At form submission:

- appears near form heading;
- links to fields;
- receives focus;
- uses clear count and instructions.

## 156. Badge architecture

Badge types:

```text
status
category
count
risk
environment
classification
```

## 157. Badge constraints

- short text;
- not sole source of meaning;
- accessible contrast;
- no excessive badge clutter;
- no decorative badges for core data.

## 158. Status badge

Uses canonical state label and semantic icon/color.

## 159. Risk badge

Uses:

```text
low
moderate
high
critical
```

with exact domain explanation elsewhere.

## 160. Environment badge

Shows:

```text
DEV
TEST
PILOT
COMMERCIAL
RECOVERY
MAINTENANCE
```

Environment indicators should be persistent.

## 161. Classification badge

Examples:

```text
public
internal
confidential
restricted
```

Exact taxonomy belongs in proposed/unregistered `DAT-002`.

## 162. Tag

Tags are user-defined or categorical metadata.

They must not be confused with controlled status badges.

## 163. Card architecture

Card variants:

```text
standard
interactive
summary
metric
attention
review
```

## 164. Card principle

A card groups one coherent object or concept.

Avoid card-per-field layouts.

## 165. Interactive card

Must support:

- keyboard activation;
- visible focus;
- nested-action rules;
- clear selected state.

## 166. Metric card

Shows:

- value;
- label;
- source;
- freshness;
- trend;
- state;
- unknown handling.

## 167. Attention card

Used for:

- approval;
- alert;
- stale run;
- budget warning;
- quarantine.

Includes exact action and deadline.

## 168. Table architecture

Table modes:

```text
standard
compact
dataDense
comparison
```

## 169. Table anatomy

- caption or accessible label;
- toolbar;
- header;
- body;
- row;
- cells;
- selection;
- actions;
- pagination;
- state area.

## 170. Table states

```text
loading
empty
partial
stale
error
ready
```

## 171. Table sorting

- visible active sort;
- keyboard accessible;
- stable;
- announced;
- server/client behavior documented.

## 172. Table filtering

- filters visible or summarised;
- clear all;
- count;
- no-result explanation;
- preserved where appropriate.

## 173. Table selection

- row checkbox;
- select page versus all distinction;
- clear count;
- bulk-action safety;
- cross-page semantics explicit.

## 174. Table row actions

Use an action menu when multiple secondary actions exist.

Primary row navigation may use linked title.

## 175. Responsive table

Strategies:

```text
priority columns
stacked rows
cards
local horizontal scroll
detail drawer
```

Choice depends on comparison needs.

## 176. Data table accessibility

Detailed requirements belong in `A11Y-001`.

Minimum direction:

- semantic table;
- correct headers;
- caption;
- keyboard actions;
- no inaccessible virtualisation;
- announced sorting and selection.

## 177. Pagination

Supports:

- previous/next;
- page size;
- current range;
- total if known;
- cursor mode where total unknown.

## 178. Infinite scroll

Avoid for operational records where position, audit, and return navigation matter.

## 179. Tabs

Use for related sections of one object.

Tabs must:

- be keyboard accessible;
- preserve route/deep link where useful;
- not hide critical state only in an inactive tab.

## 180. Segmented control

Use for small mutually exclusive view modes.

Examples:

```text
comfortable / compact
grid / list
```

## 181. Accordion

Use for secondary detail.

Do not collapse essential approval or risk content by default.

## 182. Breadcrumb

Shows hierarchy and supports navigation to parents.

Must wrap or collapse accessibly on mobile.

## 183. Sidebar

Supports:

- expanded;
- collapsed;
- mobile drawer;
- grouped navigation;
- persistent current item;
- workspace context.

## 184. Top bar

Contains only global controls.

Avoid duplicating page actions in the top bar.

## 185. Workspace switcher

Component states:

- ready;
- loading;
- no access;
- suspended workspace;
- search;
- multiple roles;
- mobile.

## 186. Environment indicator

Persistent and non-dismissable when environment confusion could cause risk.

## 187. Attention center

Combines counts and items from multiple domains.

It must not hide severity behind a single count.

## 188. Command palette

Candidate component for experts.

Constraints:

- navigation first;
- safe actions only;
- exact scope;
- no ambiguous protected actions;
- permission-aware.

## 189. Page header

Anatomy:

- breadcrumb;
- title;
- state;
- description;
- metadata;
- primary action;
- secondary actions;
- alerts/limitations.

## 190. Section header

Anatomy:

- title;
- optional description;
- count;
- action;
- state.

## 191. Toolbar

Used for:

- search;
- filters;
- view mode;
- selection;
- export;
- refresh.

Must reflow on mobile.

## 192. Filter bar

Supports:

- filter chips;
- count;
- clear;
- saved view;
- responsive drawer.

## 193. Empty state

Variants:

```text
first_use
no_results
no_permission
source_unavailable
filtered_empty
```

## 194. Skeleton

Use only when layout is known.

Do not use skeleton indefinitely or for data with unknown structure.

## 195. Spinner

Use for bounded local loading.

Pair with text for operations lasting more than a brief moment.

## 196. Progress bar

Variants:

```text
determinate
indeterminate
segmented
```

Show basis and current state.

## 197. Inline message

Variants:

```text
info
success
warning
danger
unknown
```

Use for contextual feedback.

## 198. Banner

Variants:

```text
environment
maintenance
recovery
security
critical
```

Critical banners are persistent and accessible.

## 199. Toast

Use for transient supplemental confirmation.

Do not rely on toast alone for critical outcomes.

## 200. Tooltip

Short supplemental information only.

## 201. Popover

Used for contextual controls or metadata.

Must close predictably and support keyboard/focus.

## 202. Dropdown menu

Contains related actions.

Destructive actions are separated and clearly labelled.

## 203. Dialog

Use for bounded tasks and decisions.

Dialog states include:

- default;
- loading;
- validation;
- dangerous;
- blocked;
- success.

## 204. Dialog width tokens

```text
dialog.sm
dialog.md
dialog.lg
dialog.xl
dialog.full
```

## 205. Drawer

Use for:

- mobile navigation;
- filters;
- detail preview;
- activity.

Complex approvals and restores use dedicated pages rather than drawers.

## 206. Confirmation dialog

Must include:

- exact action;
- target;
- impact;
- reversibility;
- primary/secondary actions;
- risk.

## 207. Destructive confirmation

May require:

- typed target;
- reauthentication;
- approval;
- backup confirmation.

## 208. Stepper

Use for:

- onboarding;
- configuration;
- restore;
- migration;
- controlled multi-step workflows.

## 209. Stepper states

```text
not_started
current
complete
error
blocked
skipped
```

## 210. Stepper rule

Users may navigate backward where safe.

They cannot skip required safety steps.

## 211. Timeline

Timeline supports:

- domain events;
- audit;
- external observations;
- operator actions;
- gaps;
- source labels.

## 212. Timeline item

Anatomy:

- icon;
- event title;
- time;
- source;
- summary;
- evidence link;
- state;
- expansion.

## 213. Timeline gap

Uses explicit gap pattern, not blank space.

## 214. Activity feed

Less authoritative than timeline.

Useful for recent collaboration and updates.

## 215. Status indicator

Forms:

```text
dot
badge
iconText
statusPanel
```

Never use dot alone for critical state.

## 216. Health indicator

Shows:

- state;
- freshness;
- dependency impact;
- last check;
- details.

## 217. Readiness indicator

Distinct from health.

Examples:

```text
Healthy but not ready
Degraded and partially ready
Unknown readiness
```

## 218. Freshness indicator

Shows:

- current;
- recent;
- aging;
- stale;
- expired;
- unavailable;
- unknown;
- conflicted.

## 219. Source indicator

Labels:

```text
authoritative
adapter_reported
provider_reported
generated
estimated
inferred
unknown
```

## 220. Risk indicator

Combines:

- severity;
- effect class;
- scope;
- reversibility;
- data classification;
- unknowns.

## 221. Avatar and agent identity

Human and agent identities must be visually distinguishable without implying a human-like persona.

## 222. Human identity marker

Use controlled person icon/avatar.

## 223. Agent identity marker

Use agent or system icon and role label.

Avoid photorealistic human avatars for agents by default.

## 224. Adapter marker

Distinct technical integration icon.

## 225. Model marker

Shows profile/model identity with source label.

## 226. Run-state pattern

Component includes:

- state badge;
- step;
- last reliable evidence;
- freshness;
- waiting reason;
- actions;
- cost state.

## 227. Run stepper pattern

Shows:

- planned steps;
- current;
- completed;
- waiting;
- failed;
- skipped;
- unknown.

## 228. Attempt history pattern

Uses chronological list/table.

Previous attempts remain visible.

## 229. Waiting-reason pattern

Shows:

- reason;
- owner;
- since;
- expected resolution;
- deadline;
- next action.

## 230. Unknown-effect pattern

Must use a dedicated high-emphasis panel.

Content:

- unresolved statement;
- last reliable evidence;
- risk of retry;
- reconciliation action;
- evidence links.

## 231. Approval-review pattern

Anatomy:

```text
risk header
decision summary
exact action
target and scope
diff/content
permissions and data
cost and reversibility
evidence
decision footer
```

## 232. Approval decision footer

Contains:

- reject;
- request revision;
- approve.

Approve is not automatically the primary visual action in every risk context; hierarchy must be tested.

## 233. Approval stale state

If review material changes:

- disable decision controls;
- show invalidation reason;
- link to new request.

## 234. Approval consumed state

Read-only pattern with:

- consumed time;
- attempt;
- result;
- effect certainty.

## 235. Diff viewer

Supports:

- unified;
- split;
- syntax highlighting;
- line numbers;
- changed-section summary;
- keyboard navigation;
- large-diff performance;
- accessible text mode.

## 236. Diff viewer risk

Large or complex diff approval may require desktop and dedicated review mode.

## 237. Code block

Supports:

- language;
- copy;
- wrap;
- local horizontal scroll;
- line numbers optional;
- no automatic execution.

## 238. Command block

Displays:

- command;
- environment;
- working directory;
- expected effect;
- copy action.

## 239. Artifact-review pattern

Includes:

- safe preview;
- version;
- provenance;
- integrity;
- classification;
- validation;
- compare;
- review actions.

## 240. Artifact preview frame

Shows:

- derived/original;
- renderer;
- generated time;
- safety state;
- zoom/download controls.

## 241. Quarantine pattern

Uses:

- strong warning;
- metadata-only content;
- reason;
- blocked actions;
- security review.

## 242. Memory-evidence pattern

Shows:

- statement;
- source;
- authority;
- confidence;
- freshness;
- conflicts;
- citations.

## 243. Model-identity pattern

Shows:

```text
Logical profile
Configured binding
Selected route
Actual observation
Source
Freshness
```

## 244. Cost-certainty pattern

Shows:

```text
estimated
calculated
provider reported
invoice reconciled
unknown
conflicted
```

with currency and pricing version.

## 245. Adapter-readiness pattern

Shows:

- health;
- readiness;
- validation age;
- capability drift;
- active sessions;
- restrictions.

## 246. Capability matrix

Table or grid showing:

- capability;
- declared;
- validated;
- enabled;
- ready;
- authorized;
- approval required.

## 247. Policy-decision pattern

Shows:

- decision;
- policy/version;
- reason codes;
- matched rules;
- missing attributes;
- simulation/live status.

Detailed policy content belongs in proposed/unregistered `POL-001`.

## 248. Identity-and-access pattern

Shows:

- person/workload;
- role;
- workspace;
- grants;
- expiry;
- delegation;
- session;
- reauthentication.

Detailed IAM rules belong in proposed/unregistered `IAM-001`.

## 249. Incident pattern

Includes:

- severity;
- state;
- impact;
- facts;
- unknowns;
- containment;
- workstreams;
- timeline;
- communication;
- recovery.

## 250. Maintenance pattern

Shows:

- mode;
- environment;
- scope;
- owner;
- duration;
- available functions;
- next update.

## 251. Emergency-stop pattern

High-priority persistent pattern with:

- active scope;
- activated by;
- reason;
- blocked actions;
- active work;
- release authority.

## 252. Backup pattern

Shows:

- last backup;
- verification;
- age;
- destination;
- size;
- restore drill;
- warnings.

## 253. Restore pattern

Includes:

- backup manifest;
- target;
- build/schema;
- steps;
- reconciliation;
- validation;
- approvals;
- progress;
- stop conditions.

## 254. Chart architecture

Supported chart types:

```text
line
bar
stacked bar
area
scatter
histogram
donut only when justified
status matrix
timeline
```

## 255. Chart selection

Choose chart based on question, not aesthetic preference.

## 256. Chart color

Use semantic and categorical palettes with accessible differentiation.

Do not use red/green-only comparison.

## 257. Chart annotations

Include:

- threshold;
- incident;
- deployment;
- data gap;
- stale period;
- source change.

## 258. Chart fallback

Provide textual summary and accessible table where required.

## 259. Data visualisation anti-patterns

Avoid:

- 3D charts;
- excessive gradients;
- unlabeled axes;
- misleading truncated axes;
- decorative donut charts for critical values;
- color-only series;
- hidden missing data.

## 260. Page template — Dashboard

Structure:

```text
Page header
Critical state/attention
Key metrics
Primary workflow panels
Secondary diagnostics
Recent activity
```

## 261. Page template — List/detail

Structure:

```text
List toolbar
List/table
Selection
Detail panel or route
History/evidence
```

## 262. Page template — Review

Structure:

```text
Review header
Exact review content
Context/risk
Evidence
Decision controls
```

## 263. Page template — Settings

Structure:

```text
Settings navigation
Section title
Current state
Form/content
Impact and history
Actions
```

## 264. Page template — Operations

Structure:

```text
Environment state
Critical alerts
Health
Queues/runs
Dependencies
Capacity
Changes
Runbooks
```

## 265. Page template — Incident

Structure:

```text
Severity/status
Impact and facts
Containment
Workstreams
Timeline
Communication
Recovery
Post-incident actions
```

## 266. Page template — Wizard

Used for:

- onboarding;
- integration setup;
- restore;
- high-risk configuration.

## 267. Page template — Comparison

Used for:

- artifact versions;
- policy changes;
- model fallback;
- extension permissions;
- configuration drift.

## 268. Sidebar width

Reference:

```text
expanded  248–280px
collapsed 64–72px
```

Exact values require implementation testing.

## 269. Context panel width

Reference:

```text
320–420px
```

Should collapse or move below content at narrower widths.

## 270. Table density

Comfortable:

```text
48–52px rows
```

Compact:

```text
36–40px rows
```

## 271. Code/diff layout

May use full-width mode and local horizontal scrolling.

## 272. Approval mobile layout

Use dedicated full-screen review.

Decision footer may be sticky only if it does not cover content and all required review material remains accessible.

## 273. Responsive sidebar

At mobile widths:

- off-canvas drawer;
- focus trap;
- close on route;
- workspace context visible;
- current item announced.

## 274. Responsive page actions

Actions may move into:

- overflow menu;
- bottom action bar;
- full-width buttons.

Primary risk state remains visible.

## 275. Responsive tables

Use priority and card patterns only where comparison is not lost.

For approval/diff tables, use scoped horizontal scroll or dedicated review mode.

## 276. Responsive charts

- simplify annotations;
- support horizontal scroll only locally;
- provide textual summary;
- avoid tiny labels.

## 277. Theme — Light

Characteristics:

- neutral canvas;
- white panels;
- dark text;
- restrained blue accent;
- semantic state backgrounds.

## 278. Theme — Dark

Characteristics:

- near-black canvas;
- dark panels;
- high-contrast text;
- softened saturated colors;
- visible borders;
- no pure-black large areas unless validated.

## 279. Theme — System

Tracks operating-system preference.

User can override.

## 280. Forced colors

Components should remain usable under forced-colors modes where supported.

## 281. Print and export styles

Important review/evidence pages may support print or PDF-safe output.

Print styles should:

- include source/version;
- include timestamps;
- include classification;
- avoid interactive-only meaning;
- preserve page breaks.

## 282. Security considerations

The design system must prevent:

- secret exposure through components;
- unsafe HTML rendering;
- misleading success;
- clickjacking-like overlays;
- hidden destructive actions;
- ambiguous target selection;
- inaccessible approvals.

## 283. Content sanitisation

Rich text and extension content must use safe rendering.

No arbitrary HTML or script injection.

## 284. CSP compatibility

UI components and extension surfaces should support strict Content Security Policy.

## 285. External links

Show:

- destination host where relevant;
- external icon;
- privacy/security warning for sensitive export;
- safe `rel` behavior.

## 286. Copy-to-clipboard

For sensitive values:

- minimise use;
- show copied state;
- avoid logging;
- expire displayed value where appropriate.

## 287. Secret reference component

Displays reference metadata only.

No reveal of raw secret in ordinary UI.

## 288. File preview security

Artifact preview components:

- render derived safe output;
- isolate active content;
- expose safety state;
- avoid direct browser execution of untrusted original.

## 289. Extension UI governance

Extension UI must:

- use approved tokens;
- use approved primitives/components;
- declare routes/panels;
- comply with accessibility;
- respect CSP;
- avoid global styling;
- expose version/publisher when relevant.

## 290. Styling isolation

Potential approaches:

- CSS layers;
- namespaced styles;
- shadow DOM where suitable;
- iframe for untrusted extension UI;
- token-only theming.

Final approach requires ADR.

## 291. Component implementation contract

Every component should provide:

- typed properties;
- semantic variants;
- accessible defaults;
- controlled class/style overrides;
- test IDs only when necessary;
- stable DOM semantics where practical.

## 292. Escape hatches

Escape hatches must be:

- rare;
- documented;
- reviewed;
- prohibited for critical state semantics.

## 293. CSS architecture direction

Potential direction:

```text
design tokens
→ CSS custom properties
→ component styles
→ utility/layout primitives
→ page composition
```

Final styling methodology requires ADR.

## 294. Utility-class use

Utility classes may be used internally, but public component APIs remain semantic.

## 295. Component API example

```ts
type StatusBadgeProps = {
  state:
    | "ready"
    | "waiting"
    | "warning"
    | "danger"
    | "unknown"
    | "stale"
    | "degraded";
  label: string;
  source?: string;
  freshness?: string;
};
```

This is illustrative, not a final implementation commitment.

## 296. Token API example

```css
:root {
  --surface-canvas: #F8FAFC;
  --surface-panel: #FFFFFF;
  --text-primary: #0F172A;
  --action-primary-background: #3154CC;
  --focus-ring: #4568E6;
}
```

## 297. Dark-theme token example

```css
[data-theme="dark"] {
  --surface-canvas: #020617;
  --surface-panel: #0F172A;
  --text-primary: #F8FAFC;
  --action-primary-background: #6388F2;
  --focus-ring: #8DADFF;
}
```

## 298. State-panel example

```text
Unknown effect
Last reliable evidence: provider accepted the request at 14:32 UTC.
We cannot confirm whether the action completed.
Retry is blocked until reconciliation is complete.
[Reconcile run] [View evidence]
```

## 299. Component documentation site

A future documentation environment should include:

- foundations;
- tokens;
- component anatomy;
- interactive examples;
- all states;
- responsive previews;
- accessibility notes;
- code examples;
- usage guidance;
- changelog.

## 300. Story catalogue

Every stable component should have stories/examples for:

```text
default
hover
focus
disabled
loading
error
empty
stale
unknown
dark theme
compact density
mobile
keyboard
```

where applicable.

## 301. Visual test matrix

Components should be tested across:

```text
light / dark
comfortable / compact
320 / 375 / 768 / 1024 / 1440
default / focus / disabled / error / unknown
```

Detailed procedures belong in proposed/unregistered `VVR-001`.

## 302. Accessibility test matrix

Detailed test requirements belong in `A11Y-001`.

Design-system minimum:

- keyboard;
- focus;
- names/roles/states;
- contrast;
- zoom/reflow;
- reduced motion;
- screen-reader smoke;
- forced colors where supported.

## 303. Unit tests

Verify:

- variants;
- state mapping;
- disabled/loading;
- keyboard interactions;
- event behavior;
- generated classes/tokens.

## 304. Integration tests

Verify:

- forms;
- dialogs;
- menus;
- tables;
- approvals;
- route changes;
- responsive shell;
- theme persistence.

## 305. Visual-regression tests

Verify:

- token changes;
- component variants;
- page templates;
- domain patterns;
- dark theme;
- responsive states;
- overflow;
- focus.

## 306. Manual visual review

Required for:

- new component;
- major token change;
- approval pattern;
- artifact preview;
- operations dashboard;
- responsive restructuring;
- accessibility-sensitive interaction.

## 307. Browser matrix direction

Minimum direction:

- current Chromium;
- current Firefox;
- current Safari or WebKit where supported;
- Windows and Linux desktop;
- common mobile viewport simulation.

Final matrix requires approval.

## 308. Device matrix direction

- keyboard/mouse desktop;
- touch mobile;
- tablet;
- high-DPI;
- zoom 200–400%;
- reduced motion;
- dark mode.

## 309. Visual evidence

Evidence may include:

- screenshot;
- video;
- story snapshot;
- automated diff;
- review note;
- build/environment identity.

## 310. Visual baselines

Baselines are:

- versioned;
- reviewed;
- environment-specific;
- updated only with intentional change;
- not blindly accepted.

## 311. Visual-diff triage

Classify:

```text
intentional
regression
environment_noise
font_rendering
data_variation
unknown
```

## 312. Design-system governance

Governance roles:

```text
system_owner
component_owner
accessibility_reviewer
security_reviewer
implementation_owner
quality_reviewer
```

## 313. System owner

Owns:

- principles;
- roadmap;
- tokens;
- stability;
- adoption;
- deprecation.

## 314. Component owner

Owns:

- API;
- documentation;
- tests;
- migration;
- issues.

## 315. Accessibility reviewer

Reviews:

- semantics;
- keyboard;
- focus;
- contrast;
- assistive technology;
- exceptions.

## 316. Security reviewer

Reviews:

- rich content;
- secret fields;
- preview;
- external links;
- extension UI;
- destructive actions.

## 317. Contribution workflow

```text
proposal
→ design review
→ accessibility/security review
→ candidate implementation
→ tests and examples
→ visual review
→ adoption
→ stable
```

## 318. Component proposal

Includes:

- problem;
- existing alternatives;
- contexts;
- states;
- anatomy;
- accessibility;
- responsive;
- tokens;
- migration;
- owner.

## 319. Duplicate-component prevention

Before adding a component:

- search existing catalogue;
- evaluate variant;
- evaluate composition;
- avoid one-off wrapper.

## 320. Breaking-change governance

Breaking changes require:

- rationale;
- impact inventory;
- migration guide;
- deprecation;
- codemod where useful;
- visual/accessibility review;
- release note.

## 321. Deprecation policy

A deprecated component:

- shows warning in documentation;
- has replacement;
- has removal target;
- remains tested during support period.

## 322. Token deprecation

Tokens cannot be silently repurposed.

Create new semantic token and deprecate old one.

## 323. Design-system versioning

Use semantic versioning direction:

- patch: fixes without semantic change;
- minor: additive tokens/components;
- major: breaking contract.

## 324. Release notes

Include:

- added;
- changed;
- fixed;
- deprecated;
- removed;
- accessibility;
- migrations;
- visual impact.

## 325. Adoption metrics

Potential:

- percentage of screens using stable components;
- duplicate style count;
- token usage;
- accessibility defects;
- visual-regression coverage;
- component issue age;
- deprecated usage.

## 326. Metric caution

Do not optimise adoption percentage at the expense of correct UX.

## 327. Design debt

Examples:

- hard-coded color;
- arbitrary spacing;
- duplicate component;
- inaccessible focus;
- untested dark theme;
- unresponsive table;
- undocumented variant;
- stale token.

## 328. Design-debt record

Fields:

- debt ID;
- component/screen;
- issue;
- risk;
- owner;
- workaround;
- target;
- release impact.

## 329. Quality gate

A screen or component is design-system complete when:

- semantic tokens are used;
- component API is documented;
- states are implemented;
- responsive behavior is verified;
- accessibility is verified;
- dark theme works;
- no global overflow;
- visual evidence exists;
- content follows terminology;
- no one-off critical styling.

## 330. Release blockers

Examples:

- approval action visually ambiguous;
- focus invisible;
- critical state color-only;
- stale/unknown shown as success;
- mobile hides risk;
- unsafe artifact preview;
- global horizontal overflow;
- unreadable dark theme;
- dead component state;
- unreviewed token breaking change.

## 331. Anti-pattern — card wall

Avoid pages composed of many equally weighted cards.

Use hierarchy and grouping.

## 332. Anti-pattern — rainbow status

Avoid too many unrelated colors.

Use a restrained semantic palette.

## 333. Anti-pattern — tiny metadata

Source, freshness, and classification may be lower emphasis but must remain readable.

## 334. Anti-pattern — decorative gradients

Gradients should not carry state or dominate operational surfaces.

## 335. Anti-pattern — icon-only workflow

Do not make core workflows depend on memorising icons.

## 336. Anti-pattern — disabled without reason

Users need to understand why an action is unavailable and how to resolve it.

## 337. Anti-pattern — optimistic protected success

Never show approval, protected execution, or restore as complete before authoritative confirmation.

## 338. Anti-pattern — unbounded modal

Complex operations belong on dedicated pages.

## 339. Anti-pattern — hover-only information

Essential content must be available without hover.

## 340. Anti-pattern — low-contrast dark theme

Dark theme is not merely color inversion.

## 341. Anti-pattern — arbitrary extension styling

Extensions cannot override global typography, tokens, or layout without governance.

## 342. Anti-pattern — screenshot-driven implementation only

Screenshots are evidence, not the component contract.

## 343. Reference page inventory

The design system should document patterns for:

```text
Home dashboard
Task list/detail
Run list/detail
Approval queue/detail
Artifact list/review
Memory record/conflict
Agent detail
Adapter detail
Model profile
Integration detail
Operations dashboard
Incident detail
Settings
Onboarding
```

## 344. Reference component inventory

Foundational components:

```text
Box
Stack
Inline
Grid
Text
Icon
Divider
Button
IconButton
Link
Input
Textarea
Search
Select
Combobox
Checkbox
Radio
Switch
DateTime
FileInput
FormField
Badge
Tag
Card
Table
Pagination
Tabs
Accordion
Breadcrumb
Sidebar
TopBar
Toolbar
FilterBar
EmptyState
Skeleton
Progress
InlineMessage
Banner
Toast
Tooltip
Popover
Menu
Dialog
Drawer
Stepper
Timeline
StatusIndicator
Chart
CodeBlock
DiffViewer
```

## 345. Reference domain-pattern inventory

```text
RunStatePanel
RunStepper
AttemptHistory
WaitingReason
UnknownEffectPanel
ApprovalReview
ApprovalDecisionFooter
ArtifactReview
ArtifactPreview
QuarantinePanel
MemoryEvidence
ModelIdentity
CostCertainty
AdapterReadiness
CapabilityMatrix
PolicyDecision
IdentityAccessSummary
IncidentStatus
MaintenanceBanner
EmergencyStopBanner
BackupStatus
RestoreProgress
```

## 346. Design token checklist

- semantic name;
- light/dark value;
- type;
- usage;
- contrast;
- owner;
- tests;
- documentation;
- deprecation status.

## 347. Component checklist

- purpose;
- anatomy;
- variants;
- states;
- responsive;
- accessibility;
- content;
- tokens;
- examples;
- tests;
- owner;
- maturity.

## 348. Screen checklist

- page template;
- workspace/environment;
- title/state;
- primary action;
- empty/loading/error/stale/unknown;
- responsive;
- keyboard;
- focus;
- source/freshness;
- visual evidence.

## 349. Approval-pattern checklist

- exact action;
- exact target;
- diff/content;
- risk;
- data;
- secrets;
- cost;
- reversibility;
- expiry;
- reject/revise/approve;
- mobile;
- accessibility.

## 350. Artifact-pattern checklist

- exact version;
- safe preview;
- integrity;
- provenance;
- classification;
- validation;
- compare;
- acceptance;
- export;
- deletion.

## 351. Operations-pattern checklist

- environment;
- health/readiness;
- freshness;
- alert severity;
- owner/runbook;
- stale/unknown;
- maintenance;
- emergency stop;
- capacity;
- backup.

## 352. Requirement catalogue

### Tokens and themes

- `DSN-REQ-TOK-001` — Components use semantic tokens.
- `DSN-REQ-TOK-002` — Light and dark themes are supported.
- `DSN-REQ-TOK-003` — Tokens are machine-readable and versioned.
- `DSN-REQ-TOK-004` — Token changes include contrast validation.
- `DSN-REQ-TOK-005` — Tokens are not silently repurposed.
- `DSN-REQ-TOK-006` — Component tokens cannot weaken semantic meaning.
- `DSN-REQ-TOK-007` — Extension surfaces use approved tokens.
- `DSN-REQ-TOK-008` — Theme selection cannot hide critical state.

### Components and patterns

- `DSN-REQ-CMP-001` — Components document anatomy, variants, states, and accessibility.
- `DSN-REQ-CMP-002` — Critical workflows use controlled patterns.
- `DSN-REQ-CMP-003` — Disabled actions expose reason where needed.
- `DSN-REQ-CMP-004` — Unknown, stale, partial, and degraded states are supported.
- `DSN-REQ-CMP-005` — Protected success is never optimistic.
- `DSN-REQ-CMP-006` — Untrusted previews use safe patterns.
- `DSN-REQ-CMP-007` — Complex workflows use dedicated pages.
- `DSN-REQ-CMP-008` — Components have stable maturity and ownership.

### Responsive and accessibility

- `DSN-REQ-ACC-001` — Required widths avoid global horizontal overflow.
- `DSN-REQ-ACC-002` — Keyboard and focus states are built in.
- `DSN-REQ-ACC-003` — State is not communicated by color alone.
- `DSN-REQ-ACC-004` — Reduced motion is supported.
- `DSN-REQ-ACC-005` — Mobile preserves critical review context.
- `DSN-REQ-ACC-006` — Tables and charts have accessible alternatives.
- `DSN-REQ-ACC-007` — Dark theme meets contrast requirements.
- `DSN-REQ-ACC-008` — Extension UI follows the same accessibility contract.

### Governance and quality

- `DSN-REQ-GOV-001` — Design-system changes are reviewed and versioned.
- `DSN-REQ-GOV-002` — Breaking changes include migration guidance.
- `DSN-REQ-GOV-003` — Stable components have visual and interaction tests.
- `DSN-REQ-GOV-004` — Visual baselines are reviewed.
- `DSN-REQ-GOV-005` — One-off critical styling is prohibited.
- `DSN-REQ-GOV-006` — Design debt is tracked.
- `DSN-REQ-GOV-007` — Documentation reflects actual implementation.
- `DSN-REQ-GOV-008` — Critical visual defects block release.

## 353. Traceability

| Source | DSN-001 response |
|---|---|
| `UXA-001` | Information architecture, states, journeys, responsive priorities |
| `NFR-001` | Accessibility, performance, compatibility, usability |
| `RUN-001` | Run and attempt patterns |
| `APR-001` | Approval review patterns |
| `ART-001` | Artifact review and safe preview |
| `MEM-001` | Memory evidence and conflicts |
| `MOD-001` | Model identity and cost presentation |
| `OBS-001` | Health, freshness, alerts, dashboards |
| `OPS-001` | Maintenance, recovery, incident patterns |
| `PLG-001` | Extension UI governance |
| `TST-001` | Component and visual testing |
| `QAG-001` | Design and accessibility release gates |

## 354. ADR backlog

### `ADR-TBD-DSN-001 — Token source and generation pipeline`

Select token schema, code generation, CSS variables, typed APIs, and design-tool synchronisation.

### `ADR-TBD-DSN-002 — Component implementation framework`

Select component framework, styling approach, documentation environment, and package structure.

### `ADR-TBD-DSN-003 — Theme and contrast profile`

Approve reference palette, light/dark themes, high-contrast direction, and contrast automation.

### `ADR-TBD-DSN-004 — Responsive grid and density`

Confirm breakpoints, sidebar widths, density modes, control sizes, and mobile restrictions.

### `ADR-TBD-DSN-005 — Visual-regression and component test stack`

Select stories/examples, screenshot tooling, browsers, baseline storage, and review workflow.

### `ADR-TBD-DSN-006 — Extension UI isolation and design-system access`

Define token distribution, component access, CSS isolation, CSP, sandbox/iframe model, and version compatibility.

## 355. Open decisions

1. Confirm `DSN-001` registration.
2. Approve or revise the reference palette.
3. Confirm primary accent family.
4. Confirm unknown-state visual family.
5. Confirm light/dark theme as MVP requirement.
6. Confirm high-contrast themes.
7. Confirm typography strategy.
8. Confirm minimum body and metadata sizes.
9. Confirm density defaults.
10. Confirm breakpoint values.
11. Confirm sidebar and context-panel widths.
12. Confirm component implementation framework.
13. Confirm styling architecture.
14. Confirm token source format.
15. Confirm documentation environment.
16. Confirm icon library/style.
17. Confirm chart library direction.
18. Confirm rich-text rendering model.
19. Confirm diff-viewer approach.
20. Confirm visual-regression stack.
21. Confirm browser matrix.
22. Confirm component maturity process.
23. Confirm extension UI isolation.
24. Confirm design-system ownership.
25. Confirm `UIF-001` need after state-contract review.

## 356. Risks

| Risk | Consequence | Response |
|---|---|---|
| Palette becomes brand too early | Rework | Reference semantic direction |
| Raw colors used directly | Inconsistent themes | Semantic tokens |
| Dark theme added late | Contrast defects | Theme from start |
| Too many component variants | Fragmentation | Governance and maturity |
| Compact mode harms accessibility | Exclusion/errors | Target and focus rules |
| Cards overused | Weak hierarchy | Page templates |
| Unknown looks decorative | Misunderstood risk | Dedicated semantics |
| Disabled controls unexplained | User dead end | Reason pattern |
| Visual regression accepted blindly | Hidden defects | Human review |
| Component docs drift | Incorrect implementation | Versioned examples/tests |
| Extension UI breaks shell | Fragmentation/security | Isolation and tokens |
| Arbitrary z-index | Overlay defects | Controlled scale |
| Utility classes leak as API | Brittle usage | Semantic component API |
| Tiny metadata hides source | Trust failure | Readability requirement |
| Color-only status | Accessibility failure | Redundant indicators |
| Motion implies progress | False certainty | Motion policy |
| Diff viewer inaccessible | Unsafe approval | Text/keyboard modes |
| Hard-coded widths overflow | Mobile regression | Responsive primitives |
| One-off critical styling | Inconsistent decisions | Controlled domain patterns |
| Design system too broad for MVP | Delivery delay | Maturity and phased adoption |

## 357. Assumptions

- Agent OS uses a web interface;
- UXA-001 defines the primary information architecture;
- light and dark themes are valuable;
- semantic tokens can be generated;
- a shared component package is feasible;
- extension UI will be constrained;
- accessibility and visual verification receive separate detailed documents;
- the design system can evolve in phases;
- the visual identity remains restrained and provider-neutral;
- the user will review actual rendered UI before integration progresses.

## 358. Constraints

- no color-only state;
- no raw secret display;
- no arbitrary third-party CSS/script;
- no protected optimistic success;
- no global horizontal overflow at required widths;
- no unreviewed breaking token change;
- no one-off critical action pattern;
- no unsupported claim of WCAG conformance in this draft;
- no final framework or toolchain selected;
- no commercial brand lock in this reference palette;
- no Git commit, push, PR, merge, or package publication during current drafting.

## 359. Acceptance criteria

DSN-001 may advance to `1.0.0` when:

1. It is formally added to the document register.
2. Product accepts visual principles, foundations, and component scope.
3. Architecture accepts token, package, extension, and implementation boundaries.
4. Security accepts rich content, secret, preview, external-link, and extension UI controls.
5. Data accepts classification, provenance, and data-visualisation presentation.
6. Operations accepts dense dashboards, alerts, maintenance, recovery, and incident patterns.
7. Quality accepts responsive, accessibility, visual-regression, maturity, and release gates.
8. the reference palette is approved or replaced;
9. light/dark token mappings are complete;
10. foundational components and domain patterns are inventoried;
11. responsive and density rules are approved;
12. component documentation and test requirements are approved;
13. extension UI governance is accepted;
14. `A11Y-001` and `VVR-001` can refine verification without changing design-system semantics;
15. the global audit resolves `UIF-001`.

## 360. Downstream impact

| Document | Required use |
|---|---|
| `A11Y-001` | Detailed contrast, keyboard, AT, target, reflow, and exception criteria |
| `VVR-001` | Baseline, screenshot, diff, browser, and review workflow |
| `IAM-001` | Identity, session, role, reauthentication components |
| `POL-001` | Policy decision, simulation, permission patterns |
| `SAN-001` | Sandbox status and execution-review patterns |
| `SEC-002` | Security-control state and evidence components |
| `DAT-002` | Classification, retention, hold, deletion patterns |
| `AUD-001` | Timeline, evidence, receipt, export patterns |
| `CST-001` | Cost certainty, budget, usage visualisation |
| `ADP-HER-001` | Hermes capability, session, tool, and model patterns |
| `ADP-CDX-001` | Repository, branch, diff, test, and Git-control patterns |
| Document register | Add proposed document and dependencies |

## 361. Revision and approval history

### Approval state

- Current status: `draft`
- Register status: `proposed_unregistered`
- Current version: `0.1.0`
- Approved by: no one
- Required next action: register proposal, then Product, Architecture, Security, Data, Operations, and Quality review

### Revision history

| Version | Date | Status | Summary |
|---|---|---|---|
| 0.1.0 | 2026-07-20 | Draft | Initial Agent OS design system covering foundations, tokens, themes, reference palette, typography, spacing, grid, iconography, motion, components, domain patterns, page templates, responsive behavior, accessibility foundations, extension UI, testing, governance, and release criteria |

## References

- `DOC-000` — Documentation Governance and Source-of-Truth Policy
- `GLO-001` — Glossary and Controlled Terminology
- `UXA-001` — UX Architecture and User Journey Specification — proposed/unregistered
- `NFR-001` — Non-Functional Requirements
- `RUN-001` — Run and Execution Contract
- `APR-001` — Approval Contract
- `ART-001` — Artifact Contract
- `MEM-001` — Memory and Knowledge Architecture
- `MOD-001` — Model Profile Contract
- `OBS-001` — Observability Architecture
- `OPS-001` — Operations and Production Runbook
- `PLG-001` — Plugin and Extension Architecture
