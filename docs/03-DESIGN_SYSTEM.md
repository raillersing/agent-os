# Agent OS v2 — Goldie Edition Design System

> **Status:** Source of truth for UI/UX implementation.  
> **Scope:** All Next.js 15 + React 19 + Tailwind CSS v4 frontend surfaces.  
> **Theme:** Dark-first, inspired by Julian Goldie "Agentic OS" screenshots.  
> **Version:** 2.0.0

---

## 1. Philosophy

Agent OS is a **dark control plane** — a single dashboard that coordinates multiple AI agents around one shared memory layer. The interface must feel:

1. **Controlled and deliberate** — even when 12 agents are running in parallel.
2. **Trustworthy under uncertainty** — unknown/stale states are explicit, never hidden.
3. **Agent-first** — every agent has instant visual identity through color and shape.
4. **Operationally dense** — Mission Control surfaces KPIs, DAG status, and heartbeat at a glance.
5. **Accessible by default** — focus rings, screen-reader labels, and reduced-motion respect are non-negotiable.

---

## 2. Color Palette

### 2.1 Dark Canvas (Primary Backgrounds)

| Token | Hex | Usage |
|---|---|---|
| `--canvas` | `#0A0A0B` | Root app background (near-black, slightly warm) |
| `--canvas-elevated` | `#111113` | Sidebar, nav panels |
| `--surface` | `#17171A` | Cards, panels, modal backdrops |
| `--surface-raised` | `#1E1E22` | Hover cards, active rows, input backgrounds |
| `--surface-sunken` | `#0D0D0F` | Code blocks, nested panels, terminal |

### 2.2 Agent Identity Colors

Each agent gets a **circular avatar** with its brand color. These colors are sacred — they appear in avatars, status dots, activity rings, and chat bubbles.

| Agent | Hex | Tailwind Token | Notes |
|---|---|---|---|
| **Claude** | `#F97316` | `--agent-claude` | Anthropic orange |
| **OpenClaw** | `#EC4899` | `--agent-openclaw` | Vibrant pink |
| **Hermes** | `#3B82F6` | `--agent-hermes` | Electric blue |
| **Gemini** | `#A3E635` | `--agent-gemini` | Lime / green-yellow |
| **Antigravity** | `#8B5CF6` | `--agent-antigravity` | Violet accent |
| **Codex** | `#9CA3AF` | `--agent-codex` | Neutral gray |
| **Kimi** | `#22D3EE` | `--agent-kimi` | Cyan |
| **Grok** | `#EF4444` | `--agent-grok` | Red (X branding) |
| **Crystal** (Orchestrator) | `#E879F9` | `--agent-crystal` | Magenta |
| **Alex** (Writer) | `#34D399` | `--agent-alex` | Emerald |
| **Elvis** (Media) | `#FBBF24` | `--agent-elvis` | Amber |
| **Joe** (Reviewer) | `#60A5FA` | `--agent-joe` | Sky blue |
| **Free Claude Code** | `#22C55E` | `--agent-fcc` | Green |

### 2.3 Brand Accent

| Token | Hex | Usage |
|---|---|---|
| `--brand` | `#C084FC` | Primary brand purple (soft lavender) |
| `--brand-bright` | `#A855F7` | CTAs, active tabs, selection |
| `--brand-dim` | `#7E22CE` | Deep accent for gradients |
| `--brand-glow` | `rgba(168, 85, 247, 0.15)` | Subtle glow behind cards, rings |

### 2.4 Status Colors

| State | Hex | Tailwind Token | Usage |
|---|---|---|---|
| **Online / Success** | `#22C55E` | `--status-success` | Green dot, healthy heartbeat |
| **Ready / Idle** | `#EAB308` | `--status-ready` | Yellow dot, queued/warming |
| **Offline / Failed** | `#EF4444` | `--status-offline` | Red dot, error, critical |
| **Running / Active** | `#3B82F6` | `--status-running` | Blue pulse, streaming |
| **Unknown** | `#8B5CF6` | `--status-unknown` | Violet, unresolved state |
| **Stale / Degraded** | `#F97316` | `--status-stale` | Orange, needs attention |
| **Blocked / Paused** | `#6B7280` | `--status-blocked` | Gray, awaiting approval |

### 2.5 Text Colors (Dark Theme)

| Token | Hex | Usage |
|---|---|---|
| `--text-primary` | `#F8FAFC` | Headings, primary labels |
| `--text-secondary` | `#94A3B8` | Body, descriptions |
| `--text-muted` | `#64748B` | Metadata, timestamps, disabled hints |
| `--text-inverse` | `#0A0A0B` | Text on brand or success buttons |
| `--text-code` | `#E2E8F0` | Code blocks, terminal output |

### 2.6 Border Colors

| Token | Hex | Usage |
|---|---|---|
| `--border-subtle` | `rgba(255,255,255,0.06)` | Card borders, dividers |
| `--border-default` | `rgba(255,255,255,0.10)` | Input borders, table rows |
| `--border-strong` | `rgba(255,255,255,0.16)` | Focused inputs, active cards |
| `--border-brand` | `#A855F7` | Active tab underline, selected agent |
| `--border-success` | `#22C55E` | Verified, approved boundaries |
| `--border-danger` | `#EF4444` | Error, destructive boundaries |

### 2.7 Gradient Patterns

**Agent Ring (circular avatar border):**
```css
.agent-ring-claude {
  background: conic-gradient(from 0deg, #F97316, #FDBA74, #F97316);
}
.agent-ring-hermes {
  background: conic-gradient(from 0deg, #3B82F6, #60A5FA, #3B82F6);
}
```

**Card Glow (subtle elevation):**
```css
.card-glow {
  box-shadow: 0 0 0 1px rgba(255,255,255,0.06),
              0 4px 24px rgba(0,0,0,0.4),
              0 0 40px -8px rgba(168, 85, 247, 0.08);
}
```

**Mission Control Header:**
```css
.mc-header {
  background: linear-gradient(180deg, rgba(168,85,247,0.08) 0%, transparent 100%);
}
```

---

## 3. Typography

### 3.1 Font Families

| Purpose | Stack | Notes |
|---|---|---|
| **Display / Headings** | `ui-serif, Georgia, "Playfair Display", serif` | Page titles like "Mission Control", "Studio". Adds gravitas. |
| **Body / UI** | `ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif` | All interface text, labels, buttons |
| **Data / Code** | `ui-monospace, "JetBrains Mono", "Fira Code", SFMono-Regular, Menlo, Monaco, Consolas, monospace` | Code blocks, IDs, metrics, terminal |

> **Note:** Install `Inter` and `JetBrains Mono` via `next/font/google` or self-host. `Playfair Display` (or similar serif) for display headings only.

### 3.2 Type Scale

| Token | Size | Line Height | Weight | Usage |
|---|---|---|---|---|
| `text-display` | 48px / 3rem | 1.1 | 600 | Hero titles (e.g., "Mission Control") |
| `text-h1` | 36px / 2.25rem | 1.15 | 600 | Page titles |
| `text-h2` | 24px / 1.5rem | 1.2 | 600 | Section titles |
| `text-h3` | 20px / 1.25rem | 1.3 | 600 | Card titles, panel headers |
| `text-h4` | 18px / 1.125rem | 1.35 | 500 | Sub-sections |
| `text-body` | 16px / 1rem | 1.5 | 400 | Default body text |
| `text-body-sm` | 14px / 0.875rem | 1.5 | 400 | Secondary body, descriptions |
| `text-caption` | 12px / 0.75rem | 1.4 | 500 | Labels, badges, metadata |
| `text-micro` | 11px / 0.6875rem | 1.3 | 500 | Dense table data, timestamps |
| `text-mono` | 13px / 0.8125rem | 1.4 | 400 | Code, IDs, metrics |

### 3.3 Letter Spacing

| Token | Value | Usage |
|---|---|---|
| `tracking-tight` | -0.02em | Display headings |
| `tracking-normal` | 0 | Body, UI text |
| `tracking-wide` | 0.05em | Labels, captions, ALL CAPS |
| `tracking-mono` | 0 | Monospace data |

### 3.4 Text Patterns

- **Page titles:** Serif, semibold, `--text-primary`, `tracking-tight`
- **Section titles:** Sans-serif, semibold, `--text-primary`
- **Metadata pairs:** Label in `text-caption` uppercase `tracking-wide` `--text-muted`, value in `text-body-sm` `--text-secondary`
- **Agent name in chat:** `text-body-sm` font-weight 600, agent color
- **Status badges:** `text-micro` uppercase, color matches state

---

## 4. Layout

### 4.1 Application Shell

```
┌────────────────────────────────────────────────────────────┐
│ Header (56px)                                              │
│  ⌘K  │  ALL SYSTEMS  │  Time/Location  │  User  │  Bell   │
├────────┬───────────────────────────────────────────────────┤
│        │                                                   │
│ Sidebar│  Main Content Area                                │
│ (64px  │  (fluid, max 1440px centered)                     │
│  wide  │                                                   │
│ icons) │                                                   │
│        │                                                   │
│        │                                                   │
│        │                                                   │
└────────┴───────────────────────────────────────────────────┘
```

### 4.2 Sidebar

- **Width:** 64px (icon-only collapsed), 240px (expanded on hover/focus)
- **Background:** `--canvas-elevated`
- **Border-right:** `--border-subtle`
- **Content:**
  - Top: App logo (crystal/orb icon, 32px)
  - Middle: Agent circular avatars (40px), grouped by category
  - Bottom: Settings, Help, Collapse toggle
- **Agent groups:**
  - **Workspace:** Mission Control, Goals, Notebook
  - **Agents:** Claude, Hermes, OpenClaw, Gemini, Kimi, Grok, Antigravity, Codex
  - **Studio:** Images, Videos, Speech
  - **SEO:** Dashboard, Campaigns, Keywords, Content Briefs, Reports
  - **Workflows:** Builder, Templates, Schedules, Marketplace
  - **System:** Skills, Memory, Runs, Approvals, Roles
- **Active state:** 3px `--border-brand` left border + `--brand-glow` background
- **Tooltip:** On hover, agent name + status in tooltip

### 4.3 Header

- **Height:** 56px
- **Background:** `--canvas` with `backdrop-blur(12px)`
- **Border-bottom:** `--border-subtle`
- **Left:** ⌘K Command Palette button (pill shape, `--surface-raised`, `text-caption`)
- **Center-left:** "ALL SYSTEMS" dropdown (shows environment: DEV / TEST / PILOT / COMMERCIAL)
- **Center-right:** Live clock + timezone
- **Right:** Notification bell (with red dot when pending approvals), user avatar

### 4.4 Content Grid

- **Padding:** 24px (`p-6`) default, 32px (`p-8`) on ≥1280px
- **Max width:** 1440px, centered with `mx-auto`
- **Gap between sections:** 24px (`gap-6`)
- **Card grid:** CSS Grid, `grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4`, gap 16px

### 4.5 Panels

- **Right panel (detail drawer):** 400px wide, slides from right, `--surface` background, `--border-subtle` left border
- **Bottom panel (terminal/logs):** 280px high, resizable, `--surface-sunken` background, monospace text
- **Modal:** Centered, max 560px, `--surface` background, `shadow-400`, `radius-xl`

---

## 5. Components

### 5.1 Cards

**Standard Card:**
```
background: --surface
border: 1px solid --border-subtle
border-radius: --radius-lg (8px)
padding: --space-5 (20px)
transition: border-color 150ms, box-shadow 150ms
hover: border-color --border-default, shadow-100
```

**Metric Card (Mission Control):**
```
Same as standard +:
- Top row: Icon (agent color) + Agent name + Status dot
- Middle: Large numeric value (text-h2, serif for KPI labels)
- Bottom: Delta indicator (↑ 12%) + timestamp
- Running state: --brand-glow pulse animation
```

**Agent Card:**
```
Same as standard +:
- Circular avatar (40px) with conic gradient ring
- Name + role label
- Status dot (8px) positioned bottom-right of avatar
- "Open Chat" or "View Runs" action
- Offline: grayscale(60%) + opacity(0.7)
```

**Attention Card:**
```
border-left: 3px solid --status-warning (or danger)
background: rgba(234, 179, 8, 0.05)
```

### 5.2 Buttons

| Variant | Background | Text | Border | Hover |
|---|---|---|---|---|
| **Primary** | `--brand-bright` | `--text-inverse` | none | brightness(1.1) |
| **Secondary** | `--surface-raised` | `--text-primary` | `--border-default` | `--border-strong` |
| **Ghost** | transparent | `--text-secondary` | none | `--surface-raised` |
| **Danger** | `rgba(239,68,68,0.15)` | `#EF4444` | `rgba(239,68,68,0.3)` | `rgba(239,68,68,0.25)` |
| **Agent** | Agent color at 15% opacity | Agent color | Agent color at 30% | Agent color at 25% |

**Sizes:**
- `sm`: 32px height, `text-caption`, `px-3`, `radius-md`
- `md`: 40px height, `text-body-sm`, `px-4`, `radius-md`
- `lg`: 48px height, `text-body`, `px-6`, `radius-lg`

**Loading state:** Spinner replaces icon/text, `opacity-70`, `cursor-not-allowed`

### 5.3 Inputs

**Text Input:**
```
height: 40px (md)
background: --surface-raised
border: 1px solid --border-default
border-radius: --radius-md
padding: 0 12px
font: text-body-sm

color: --text-primary
placeholder: --text-muted

focus: border --border-brand, ring 2px --brand-glow
disabled: opacity 0.5, cursor not-allowed
error: border --border-danger, ring rgba(239,68,68,0.2)
```

**Search Input (Command Palette style):**
```
height: 48px
background: --surface
border: 1px solid --border-subtle
border-radius: --radius-full (pill)
left icon: magnifying glass, --text-muted
right: ⌘K hint, --text-muted, text-micro
focus: border --border-brand, shadow-200
```

**Textarea:**
```
min-height: 120px
resize: vertical
font: text-body-sm
line-height: 1.5
```

### 5.4 Badges

**Status Badge:**
```
height: 24px
padding: 0 10px
border-radius: --radius-full
font: text-micro uppercase tracking-wide

Examples:
  Online   → bg-green-500/15 text-green-400 border-green-500/25
  Running  → bg-blue-500/15 text-blue-400 border-blue-500/25
  Ready    → bg-yellow-500/15 text-yellow-400 border-yellow-500/25
  Offline  → bg-red-500/15 text-red-400 border-red-500/25
  Unknown  → bg-violet-500/15 text-violet-400 border-violet-500/25
```

**Count Badge (on tabs/icons):**
```
min-width: 20px
height: 20px
border-radius: --radius-full
background: --brand-bright
color: --text-inverse
font: text-micro
position: absolute top-right
```

### 5.5 Tabs

**Navigation Tabs:**
```
container: border-bottom --border-subtle
tab: height 40px, px-4, text-body-sm, --text-muted
active: --text-primary, border-bottom 2px --border-brand
tab hover: --text-secondary
```

**Pill Tabs (Studio, Filters):**
```
pill: height 32px, px-4, radius-full
inactive: --surface-raised, --text-secondary, border --border-subtle
active: --brand-bright, --text-inverse
```

### 5.6 Modals

```
overlay: rgba(0,0,0,0.6) + backdrop-blur(4px)
container: max-w-lg (560px), --surface, radius-xl
shadow: shadow-400
header: pb-4, border-bottom --border-subtle, text-h3
body: py-5
footer: pt-4, border-top --border-subtle, flex justify-end gap-3
close: top-right, ghost button, X icon
animation: scale(0.96)→scale(1) + opacity 0→1, 180ms ease-out
```

### 5.7 Toasts

```
position: bottom-right, gap-3
container: max-w-sm, --surface-raised, radius-lg, border --border-subtle
shadow: shadow-300
padding: 16px

Types:
  Success: left border 3px --status-success, icon check-circle
  Error:   left border 3px --status-offline, icon alert-octagon
  Warning: left border 3px --status-stale, icon alert-triangle
  Info:    left border 3px --status-running, icon info

animation: slide-in from right 280ms ease-out, auto-dismiss 5s
```

### 5.8 Tables

```
container: --surface, radius-lg, border --border-subtle
header-row: --surface-raised, text-caption uppercase tracking-wide --text-muted, height 40px
row: height 48px, border-bottom --border-subtle
row-hover: --surface-raised
selected-row: --brand-glow background
sortable-header: hover --text-primary, sort icon --text-muted
empty-state: centered, icon + text-body-sm --text-muted
```

### 5.9 Chat Components

**Message Bubble:**
```
User:   --surface-raised, --text-primary, left-aligned
Agent:  transparent background, --text-primary, left-aligned, agent-color left border 2px

Both:
  padding: 12px 16px
  border-radius: 0 12px 12px 12px (agent) / 12px 0 12px 12px (user)
  max-width: 85%
```

**Thinking Indicator:**
```
3 dots, each 6px, agent color
animation: bounce staggered 0.6s infinite
```

**Code Block:**
```
background: --surface-sunken
border: --border-subtle
border-radius: --radius-md
font: text-mono
copy button: top-right, ghost, opacity 0→1 on hover
syntax highlighting: One Dark / Catppuccin Mocha theme
```

---

## 5.10 Workflow Builder Canvas

**Canvas:**
```
background: #0D0D0F (dark canvas)
grid: 20px dot grid at rgba(255,255,255,0.03)
minimap: bottom-right, 160px wide, --surface-raised background, 0.4 opacity
pan: drag empty space (grab cursor)
zoom: mouse wheel / toolbar buttons (25% → 200%)
selection: rectangle lasso, cmd-click multi-select
```

**Nodes:**
```
shape: rounded rectangle, radius-lg
padding: 16px 20px
min-width: 180px
shadow: shadow-100
border: 2px solid agent color at 40%
header: agent color left border 3px + icon + label
content: node type badge + description (2 lines max)
status indicator: top-right dot (pulse when running)
selected: ring 2px --brand-glow + shadow-200
hover: border-color transitions to agent color at 80%
```

**Node Types & Colors:**
| Type | Icon | Border Color | Fill |
|---|---|---|---|
| Start | play-circle | --status-success | --status-success at 8% |
| Task | bot | Agent assigned color | Agent color at 8% |
| Condition | git-branch | --status-warning | --status-warning at 8% |
| Loop | repeat | --agent-crystal | --agent-crystal at 8% |
| Approval Gate | shield-check | --status-stale | --status-stale at 8% |
| Delay/Wait | clock | --text-muted | --text-muted at 8% |
| Trigger (cron) | calendar-clock | --agent-hermes | --agent-hermes at 8% |
| Trigger (webhook) | webhook | --agent-hermes | --agent-hermes at 8% |
| End | flag | --status-offline | --status-offline at 8% |

**Connection Lines:**
```
stroke: --text-muted at 50%
stroke-width: 2px
success: --status-success
failure: --status-offline
conditional: --status-warning (dashed when inactive)
animated dash: when data flows (duration 600ms, ease linear)
bezier control: 50px horizontal offset
edge label: text-micro, --text-muted, positioned mid-edge
```

**Toolbar (floating top):**
```
background: --surface-raised
border: --border-subtle
border-radius: radius-lg
padding: 8px 12px
gap: 8px
buttons: add-node (primary), run (success), simulate (secondary), save (ghost), zoom controls (ghost)
tooltip on hover with keyboard shortcut
```

---

## 5.11 SEO Dashboard

**Layout:** Tabbed dashboard with three primary views: Overview, Keywords, Competitors.

**Keyword Position Chart:**
```
type: multi-line chart
background: --surface-sunken
grid lines: rgba(255,255,255,0.04)
line colors: agent palette (one per keyword)
active line: shadow-glow of its color
hover: vertical crosshair + tooltip showing date, position, change
range selector: 7d / 30d / 90d / 1y pill tabs
empty state: "No rank history yet. Add keywords to track."
```

**SERP Preview Cards:**
```
background: --surface
border: --border-subtle
border-radius: radius-lg
padding: 16px

title: text-body, --text-primary, max 2 lines, hover underline
display_url: text-caption, --text-muted, max 1 line
meta_description: text-body-sm, --text-secondary, max 3 lines
featured_snippet badge: bg-yellow-500/15 text-yellow-400, top-right
position badge: "#3" in pill, --brand-bright background
```

**Competitor Table:**
```
columns: Domain | Authority | Top Keywords | New Content | Rank Change
row: height 56px
change up: --status-success with ↑
change down: --status-offline with ↓
new content badge: "+3 this week" in --agent-alex color
click row: expands to show top 5 competing pages
```

**Content Brief Panel:**
```
background: --surface
border-left: 3px solid --agent-alex
padding: 20px
sections: Target Keyword | Suggested Title | Heading Outline | Word Count Target | Authority Gap | Questions to Answer
heading outline: nested list with H2/H3 indicators
export buttons: PDF, Copy Markdown, Send to Agent
```

---

## 5.12 Agent Role Manager

**Role Card:**
```
background: --surface
border: --border-subtle
border-radius: radius-lg
padding: 20px
header: icon (32px, role color) + role name (text-h4) + status badge
body: description (2 lines), assigned agents row (avatar stack, max 5 + count)
footer: skills count badge + autonomy level pill + actions (edit, clone, delete)
hover: border-color → role color at 50%, shadow-100
```

**Drag & Drop Agent Assignment:**
```
source panel: agents list with avatar + name + availability status
target area: role card dropzone highlighted on drag over
feedback: agent avatar snaps into role card on drop
reorder: drag handles within role to change priority
unassign: drag back to source panel or click × on chip
```

**Skill Badge Grid:**
```
badge: height 28px, radius-full, px-3
required skill: role color background at 15%, role color text
optional skill: --surface-raised background, --text-secondary text
missing skill: dashed border --status-offline, --status-offline text
hover: tooltip shows skill description and version
```

---

## 5.13 Approval Gate UI

**Modal:**
```
overlay: rgba(0,0,0,0.7) + backdrop-blur(8px)
container: max-w-2xl (672px), --surface, radius-xl
header: action preview title + risk level badge
body: 
  - Action preview card (what the agent wants to do)
  - Parameters table (key-value, monospace for IDs)
  - Context snippet (collapsed by default)
footer: 
  - Approve button: Primary, green glow
  - Reject button: Danger, requires comment
  - Delegate button: Ghost, opens dropdown of reviewers
  - Comment field: textarea, required for reject
animation: slide-up 200ms ease-out
```

**Approve Button:**
```
background: --status-success
hover: brightness(1.1)
icon: check-circle
label: "Approve & Continue"
```

**Reject Button:**
```
background: rgba(239,68,68,0.15)
text: #EF4444
hover: rgba(239,68,68,0.25)
icon: x-circle
label: "Reject"
disabled state: until comment length > 10 chars
```

**Delegation Option:**
```
trigger: "Delegate…" ghost button
popover: reviewer list with avatar + role + current workload
select: assigns approval to chosen reviewer, notifies original requester
```

---

## 5.14 Voice Waveform

**Purpose:** Real-time amplitude visualization during recording and agent speech playback.

**Structure:**
```
container: flex row, gap 2px, align-items center, height 32px
bar: width 3px, radius-full, agent color at 80% opacity
bar heights: mapped from frequency/amplitude bins (8–24 bars)
```

**States:**
- **Idle:** All bars at minimum height (4px), `--text-muted` at 30%
- **Recording:** Bars animate in real time; peak bar glows with `box-shadow: 0 0 6px agent-color`
- **Agent speaking:** Smooth interpolation (lerp) between frames; color matches active agent
- **Muted:** Bars frozen at current height, opacity 0.3, strikethrough overlay

**Accessibility:**
- `aria-label="Recording… amplitude 73%"` (updated every 500ms)
- `role="meter"`, `aria-valuemin="0"`, `aria-valuemax="100"`
- Reduced motion: bars do not animate; single solid height shows level

---

## 5.15 Talk Mode Panel

**Purpose:** Full-screen immersive voice interface.

**Layout:**
```
overlay: fixed inset-0, --canvas at 95% opacity, backdrop-blur(8px)
panel: centered, max-w-lg (560px), flex column, items-center, gap-8
```

**Elements:**
- **Agent avatar:** 96px circle with conic gradient ring; mouth animation (vertical scale synced to TTS audio buffer)
- **Microphone button:** 80px circle, `--brand-bright` background, `Mic` icon; press-and-hold state: ring expands with `--brand-glow` pulse
- **Subtitle transcript:** Fixed bottom, max-w-2xl, `text-body-sm` `--text-secondary`, centered, auto-scroll
- **Mode toggle:** Segmented control — Text-only | Voice-first | Auto
- **Close button:** Top-right, ghost, `X` icon, returns to previous view

**Animations:**
- Panel enter: `scale(0.9) → scale(1)` + `opacity 0 → 1`, 300ms `--ease-emphasized`
- Agent avatar: subtle float animation (translateY ±4px, 4s infinite)
- Mouth: scaleY mapped to audio amplitude (0.6–1.2), 60fps

---

## 5.16 Push-to-Talk Button

**Purpose:** Primary voice input trigger.

**Structure:**
```
base: 56px circle, --surface-raised background, border 2px solid --border-default
icon: Mic, 24px, --text-secondary

pressed state:
  - border-color: --brand-bright
  - box-shadow: 0 0 0 0 rgba(168,85,247,0.4) → 0 0 0 20px rgba(168,85,247,0)
  - animation: pt-ring 1.2s ease-out infinite
  - icon: --brand-bright

recording state:
  - background: rgba(168,85,247,0.15)
  - ring expands outward (concentric circles fading)
  - waveform bars appear around button (Voice Waveform component, 16 bars radial)
```

**Interaction:**
- Mouse/touch: press-and-hold ≥ 300ms to start recording; release to send
- Keyboard: Spacebar (global when app focused); Shift+Space (global hotkey via Electron)
- Cancel: swipe left while holding, or press Escape
- Tooltip on hover: "Hold to talk"

**Accessibility:**
- `aria-pressed` toggles during recording
- `aria-label` updates: "Hold space to talk" → "Recording… release to send" → "Processing…"
- Focus ring visible on keyboard activation

---

## 5.17 Migration Wizard

**Purpose:** Guided data import from external tools.

**Step Indicator:**
```
container: flex, gap-0, border-bottom --border-subtle
step: flex-1, py-3, text-center, text-caption
active step: --brand-bright text, bottom border 2px --brand-bright
completed step: --status-success text, check icon
future step: --text-muted
```

**Upload Dropzone:**
```
container: dashed border 2px --border-default, radius-xl, py-12, text-center
active drag: border --brand-bright, background --brand-glow
icon: Upload, 32px, --text-muted
label: "Drop export ZIP here or click to browse", text-body-sm --text-secondary
hint: "Max 2 GB", text-caption --text-muted
```

**Preview Table:**
```
columns: Type | Title | Date | Status
row: height 48px, border-bottom --border-subtle
status: pill badge — Ready (green), Conflict (yellow), Error (red)
pagination: first 10 items, "Showing 10 of 1,247"
```

**Progress Bar:**
```
container: full width, height 8px, radius-full, background --surface-sunken
fill: --brand-bright, radius-full, transition width 300ms ease-out
label below: "Importing 847 of 1,247 notes…", text-body-sm --text-secondary
ETA: "~3 minutes remaining", text-caption --text-muted
```

**Summary Screen:**
```
stats row: 3 cards — Imported (green) / Skipped (yellow) / Errors (red)
error log: collapsible panel, monospace text, scrollable max-h-48
action buttons: "Done" (primary), "Export error log" (ghost)
```

---

## 5.18 Backup Widget

**Purpose:** Compact at-a-glance backup health indicator.

**Structure:**
```
card: --surface, border --border-subtle, radius-lg, padding 16px, max-w-xs
header row: flex justify-between, items-center
  - title: "Backup", text-h4
  - status icon: 16px
    ✅ healthy → Check, --status-success
    ⚠️ warning → AlertTriangle, --status-stale
    ❌ failed → AlertOctagon, --status-offline
body: text-body-sm --text-secondary
  - "Last backup: 2 hours ago" (healthy)
  - "Backup failed 3 days ago" (warning/failed)
footer: "Backup Now" button, sm, primary
```

**States:**
- **Healthy:** Green icon + text; "Last backup: {time} ago"; button label "Backup Now"
- **Warning:** Orange icon + text; "Last backup failed {time} ago"; button label "Retry Backup"
- **Failed:** Red icon + text; "Backup failed — {error_summary}"; button label "Fix & Retry"; attention card border-left 3px red
- **In Progress:** Spinner replaces icon; "Backing up… {percent}%"; button disabled

**Hover:** Card border-color transitions to `--border-default`; shadow-100.

**Click behavior:** Clicking widget navigates to Settings → Backup & Recovery.

---

## 6. Animations & Motion

### 6.1 Duration Scale

| Token | Duration | Usage |
|---|---|---|
| `--duration-instant` | 0ms | Instant state changes |
| `--duration-fast` | 100ms | Hover, focus ring, border |
| `--duration-normal` | 180ms | Button press, card hover, toggle |
| `--duration-slow` | 280ms | Panel slide, modal, drawer |
| `--duration-deliberate` | 400ms | Page transitions, sidebar expand |

### 6.2 Easing

| Token | Curve | Usage |
|---|---|---|
| `--ease-standard` | `cubic-bezier(0.4, 0, 0.2, 1)` | General transitions |
| `--ease-enter` | `cubic-bezier(0, 0, 0.2, 1)` | Elements appearing |
| `--ease-exit` | `cubic-bezier(0.4, 0, 1, 1)` | Elements leaving |
| `--ease-emphasized` | `cubic-bezier(0.2, 0.8, 0.2, 1)` | Hero elements, agent activation |

### 6.3 Agent Pulse (Running State)

```css
@keyframes agent-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(var(--agent-color-rgb), 0.4); }
  50% { box-shadow: 0 0 0 8px rgba(var(--agent-color-rgb), 0); }
}

.agent-running .avatar-ring {
  animation: agent-pulse 2s ease-in-out infinite;
}
```

### 6.4 Stream Reveal (Chat)

```css
@keyframes stream-reveal {
  from { opacity: 0; transform: translateY(4px); }
  to   { opacity: 1; transform: translateY(0); }
}

.message-chunk {
  animation: stream-reveal 120ms ease-out forwards;
}
```

### 6.5 Card Enter (Dashboard)

```css
@keyframes card-enter {
  from { opacity: 0; transform: translateY(12px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.metric-card {
  animation: card-enter 300ms ease-out backwards;
  animation-delay: calc(var(--index) * 60ms);
}
```

### 6.6 Skeleton Loading

```
background: linear-gradient(90deg, --surface 25%, --surface-raised 50%, --surface 75%)
background-size: 200% 100%
animation: shimmer 1.5s infinite
border-radius: --radius-md
```

### 6.7 DAG Node Status

| State | Visual |
|---|---|
| **Idle** | Static, `--border-subtle` |
| **Running** | `--brand-bright` border, agent-pulse glow |
| **Success** | `--status-success` fill, check icon |
| **Failed** | `--status-offline` border, alert icon |
| **Skipped** | `--text-muted` dashed border |

---

## 7. Icon System

### 7.1 Agent Avatars

- **Shape:** Perfect circle (`radius-full`)
- **Size:** 40px in sidebar, 32px in chat, 48px in agent profile
- **Default:** First letter of agent name, white text, solid agent color background
- **Custom:** Optional uploaded image, masked to circle
- **Status dot:** 8px circle, positioned at bottom-right, offset 2px
  - Online: `--status-success`
  - Ready: `--status-ready`
  - Offline: `--status-offline`
  - Running: `--status-running` with pulse

### 7.2 Icon Library

Use **Lucide React** as the primary icon library. It is consistent, stroke-based, and tree-shakeable.

| Context | Icon | Size |
|---|---|---|
| Mission Control | `LayoutDashboard` | 20px |
| Agents | `Bot` | 20px |
| Chat | `MessageSquare` | 20px |
| Studio | `Wand2` | 20px |
| Notebook | `BookOpen` | 20px |
| Memory | `Brain` | 20px |
| Skills | `Zap` | 20px |
| Runs | `PlayCircle` | 20px |
| Approvals | `ShieldCheck` | 20px |
| SEO | `BarChart3` | 20px |
| Workflow Builder | `GitBranch` | 20px |
| Agent Roles | `UserCog` | 20px |
| Settings | `Settings` | 20px |
| Command Palette | `Search` | 16px |
| Close | `X` | 16px |
| External Link | `ExternalLink` | 14px |
| Copy | `Copy` | 14px |
| Check | `Check` | 16px |
| Alert | `AlertTriangle` | 16px |
| Info | `Info` | 16px |

### 7.3 Icon Rules

- Stroke width: 1.5px (default), 2px for active states
- All icons use `currentColor` for easy theming
- Icon-only buttons must have `aria-label`
- Icons paired with text: gap 8px, icon vertically centered

---

## 8. Tailwind CSS v4 Theme Configuration

### 8.1 `@theme` Block (Tailwind v4)

Add to your global CSS file (e.g., `globals.css`):

```css
@import "tailwindcss";

@theme {
  /* ── Colors ── */
  --color-canvas: #0A0A0B;
  --color-canvas-elevated: #111113;
  --color-surface: #17171A;
  --color-surface-raised: #1E1E22;
  --color-surface-sunken: #0D0D0F;

  --color-brand: #C084FC;
  --color-brand-bright: #A855F7;
  --color-brand-dim: #7E22CE;

  --color-text-primary: #F8FAFC;
  --color-text-secondary: #94A3B8;
  --color-text-muted: #64748B;
  --color-text-inverse: #0A0A0B;
  --color-text-code: #E2E8F0;

  --color-border-subtle: rgba(255, 255, 255, 0.06);
  --color-border-default: rgba(255, 255, 255, 0.10);
  --color-border-strong: rgba(255, 255, 255, 0.16);

  /* Agent colors */
  --color-agent-claude: #F97316;
  --color-agent-openclaw: #EC4899;
  --color-agent-hermes: #3B82F6;
  --color-agent-gemini: #A3E635;
  --color-agent-antigravity: #8B5CF6;
  --color-agent-codex: #9CA3AF;
  --color-agent-kimi: #22D3EE;
  --color-agent-grok: #EF4444;
  --color-agent-crystal: #E879F9;
  --color-agent-alex: #34D399;
  --color-agent-elvis: #FBBF24;
  --color-agent-joe: #60A5FA;
  --color-agent-fcc: #22C55E;

  /* Status colors */
  --color-status-success: #22C55E;
  --color-status-ready: #EAB308;
  --color-status-offline: #EF4444;
  --color-status-running: #3B82F6;
  --color-status-unknown: #8B5CF6;
  --color-status-stale: #F97316;
  --color-status-blocked: #6B7280;

  /* ── Typography ── */
  --font-sans: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
  --font-serif: ui-serif, Georgia, "Playfair Display", serif;
  --font-mono: ui-monospace, "JetBrains Mono", "Fira Code", SFMono-Regular, Menlo, Monaco, Consolas, monospace;

  --font-size-display: 3rem;
  --font-size-h1: 2.25rem;
  --font-size-h2: 1.5rem;
  --font-size-h3: 1.25rem;
  --font-size-h4: 1.125rem;
  --font-size-body: 1rem;
  --font-size-body-sm: 0.875rem;
  --font-size-caption: 0.75rem;
  --font-size-micro: 0.6875rem;
  --font-size-mono: 0.8125rem;

  --line-height-display: 1.1;
  --line-height-h1: 1.15;
  --line-height-h2: 1.2;
  --line-height-h3: 1.3;
  --line-height-body: 1.5;
  --line-height-caption: 1.4;

  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.05em;

  /* ── Spacing ── */
  --space-0: 0px;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;

  /* ── Sizing ── */
  --control-xs: 28px;
  --control-sm: 32px;
  --control-md: 40px;
  --control-lg: 48px;

  /* ── Radius ── */
  --radius-none: 0px;
  --radius-xs: 2px;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;

  /* ── Shadows ── */
  --shadow-100: 0 1px 2px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.04);
  --shadow-200: 0 4px 12px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.05);
  --shadow-300: 0 12px 32px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.06);
  --shadow-400: 0 24px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08);

  /* ── Z-Index ── */
  --z-base: 0;
  --z-sticky: 100;
  --z-dropdown: 200;
  --z-popover: 300;
  --z-drawer: 400;
  --z-modal: 500;
  --z-toast: 600;
  --z-overlay: 700;

  /* ── Animation ── */
  --duration-instant: 0ms;
  --duration-fast: 100ms;
  --duration-normal: 180ms;
  --duration-slow: 280ms;
  --duration-deliberate: 400ms;

  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --ease-emphasized: cubic-bezier(0.2, 0.8, 0.2, 1);
}
```

### 8.2 Global Base Styles

```css
@layer base {
  html {
    background-color: var(--color-canvas);
    color: var(--color-text-primary);
    font-family: var(--font-sans);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  ::selection {
    background-color: rgba(168, 85, 247, 0.3);
    color: var(--color-text-primary);
  }

  /* Scrollbar */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }
  ::-webkit-scrollbar-track {
    background: transparent;
  }
  ::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.2);
  }
}
```

---

## 9. Responsive Breakpoints

| Name | Width | Key Changes |
|---|---|---|
| `xs` | 320px | Minimum supported width. Sidebar hides, bottom nav appears. |
| `sm` | 480px | Single column layouts. Stacked cards. |
| `md` | 768px | Sidebar visible as icon rail. 2-column grids. |
| `lg` | 1024px | Full sidebar expanded. 3-column grids. Right panel visible. |
| `xl` | 1280px | Maximum content padding. 4-column grids. |
| `2xl` | 1536px | Ultra-wide layout. Side-by-side panels permitted. |

### 9.1 Responsive Rules

- **< 768px:** Sidebar collapses to bottom tab bar. Header compresses to hamburger + search + avatar.
- **< 1024px:** Right detail drawer becomes full-screen modal.
- **< 768px:** Chat sidebar (sessions) becomes a slide-out drawer.
- **All widths:** No horizontal page scroll. Tables get horizontal scroll within container.

---

## 10. Accessibility

### 10.1 Focus Management

```css
:focus-visible {
  outline: 2px solid var(--color-brand-bright);
  outline-offset: 2px;
  border-radius: var(--radius-md);
}
```

- All interactive elements must show a visible focus ring.
- Focus rings use `--brand-bright` (`#A855F7`) for consistency.
- Skip-link at top of page: "Skip to main content".

### 10.2 Color Contrast

| Pair | Ratio | WCAG |
|---|---|---|
| `--text-primary` (#F8FAFC) on `--surface` (#17171A) | 15.3:1 | AAA |
| `--text-secondary` (#94A3B8) on `--surface` (#17171A) | 7.2:1 | AAA |
| `--text-muted` (#64748B) on `--surface` (#17171A) | 4.6:1 | AA |
| `--brand-bright` (#A855F7) on `--surface` (#17171A) | 5.1:1 | AA |
| `--status-success` (#22C55E) on `--surface` (#17171A) | 7.8:1 | AAA |
| `--status-offline` (#EF4444) on `--surface` (#17171A) | 5.9:1 | AA |

> **Rule:** Status is never communicated by color alone. Every status badge includes an icon + text label.

### 10.3 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .agent-running .avatar-ring {
    animation: none;
    box-shadow: 0 0 0 2px var(--color-brand-bright);
  }
}
```

- All non-essential animations respect `prefers-reduced-motion`.
- Running agents switch from pulse to solid ring.
- Stream reveal becomes instant.
- Skeleton shimmer becomes static placeholder.

### 10.4 Screen Reader

- Agent status dots: `aria-label="Claude is online"`
- Chat messages: `role="log"`, `aria-live="polite"`
- Mission Control KPIs: `aria-label="Agent Heartbeat: 42ms"`
- Tables: `scope="col"`, captions where needed
- Icons in buttons: `aria-hidden="true"` when paired with text; `aria-label` when standalone

### 10.5 Touch Targets

- Minimum touch target: 44 × 44px
- Sidebar icons: 48 × 48px tap area
- Mobile buttons: 48px minimum height

---

## 11. Page-Specific Patterns

### 11.1 Mission Control

- **Background:** `--canvas` with subtle radial gradient from top-center (`--brand-glow`)
- **Header:** Serif display title "Mission Control" + live clock
- **KPI Grid:** 4 metric cards across top (Agents Online, Tasks Running, Avg Latency, Approval Queue)
- **Agent DAG:** Center canvas with draggable nodes, pan/zoom controls
- **Recent Activity:** Right panel, scrollable timeline

### 11.2 Chat

- **Layout:** Sidebar (sessions) + Main (chat) + Optional right (artifacts)
- **Session list:** Pinned at top, search filter, group by date
- **Message area:** Reverse scroll, auto-scroll to bottom on new message
- **Input:** Fixed bottom, 48px height, textarea with send button
- **Thinking:** Agent name + "is thinking..." with pulsing dots

### 11.3 Studio

- **Tabs:** Images | Videos | Speech (pill tabs with counts)
- **Gallery:** Masonry or CSS Grid, hover reveals actions
- **Generation form:** Left panel, preview right
- **Formats:** 12 format cards (Blog Post, Podcast, Deep Dive, etc.)

### 11.4 Notebook (KB)

- **Layout:** File tree sidebar + Editor + Backlinks panel
- **Editor:** Markdown with wiki-link highlighting `[[Note Title]]`
- **Backlinks:** List of notes linking to current, with context snippets
- **Search:** Full-text + semantic (vector) search results

### 11.5 Workflow Builder

- **Layout:** Full-screen canvas with floating toolbar (top) and properties panel (right)
- **Canvas:** Dark grid (`#0D0D0F`); pan-drag on empty space; zoom 25–200%
- **Node palette:** Left sidebar, draggable node types with icons and descriptions
- **Toolbar:** Add node, run (live), simulate (dry-run), save, zoom controls
- **Properties panel:** Node/edge config: expressions, agent assignment, timeout, retry policy
- **Mini-map:** Bottom-right, 160px, `--surface-raised` at 0.4 opacity
- **Simulation overlay:** Variable inspector (bottom), step-through controls (floating)

### 11.6 SEO Dashboard

- **Layout:** Tabbed view — Overview, Keywords, Competitors, Briefs, Reports
- **Overview:** KPI cards (tracked keywords, avg position, organic traffic, competitors watched)
- **Keyword tab:** Multi-line position chart (time-series), filter by campaign/intent
- **Competitor tab:** Table with change indicators; expand row for top competing pages
- **Briefs tab:** Card grid with status badges (draft → approved → published)
- **Reports tab:** Report history list with download links and scheduled generation status

### 11.7 Agent Role Manager

- **Layout:** Grid of role cards with search/filter bar at top
- **Role card:** Icon (32px, role color), name, assigned agent avatar stack, skill count, autonomy pill
- **Detail drawer:** Role config editor (name, color, system prompt template, memory profile)
- **Assignment panel:** Drag agents from pool into role; reorder by priority; set primary
- **Skill grid:** Required vs optional skill badges; version pinning; missing-skill warnings

### 11.8 Talk Mode

- **Layout:** Full-screen overlay (section 5.15)
- **Background:** `--canvas` opaque
- **Agent avatar:** 96px with mouth animation synced to TTS
- **Waveform:** 32 bars in agent color, 48px height
- **Subtitles:** Centered, max 3 lines, auto-scroll
- **Mic button:** 96px circular, press-and-hold with expanding ring
- **Mode toggle:** Text-only / Voice-first / Auto pills
- **History:** Slide-out drawer from right showing audio + text hybrid transcript

### 11.9 Migration Wizard

- **Layout:** Centered modal or full-page wizard, max-width 800px
- **Step indicator:** Top, 6 steps with connector lines
- **Content area:** Changes per step (source selector, dropzone, preview table, config form, progress, summary)
- **Navigation:** "Back" (ghost) + "Next" (primary) or "Start Import" (primary)
- **Progress step:** Large progress bar with ETA and cancel button
- **Review step:** Summary cards: imported count, skipped count, error count; "Go to Notebook" CTA

### 11.10 Backup & Restore

- **Layout:** Settings sub-page or dashboard widget + full-page restore wizard
- **Widget:** Compact card (section 5.18) shown in Mission Control or Settings
- **Restore wizard:** Step 1 select backup → Step 2 validate integrity → Step 3 preview → Step 4 confirm → Step 5 execute with progress
- **History table:** List of backups with timestamp, size, type (auto/manual), target, status, actions (restore, download, delete)

---

## 12. File Structure Convention

```
frontend/src/
├── app/
│   ├── globals.css           # @theme block + base styles
│   ├── layout.tsx            # Shell with Sidebar + Header
│   ├── page.tsx              # Mission Control (home)
│   ├── agents/
│   ├── chat/
│   ├── studio/
│   ├── notebook/
│   ├── skills/
│   ├── memory/
│   └── settings/
├── components/
│   ├── ui/                   # Primitive components
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   ├── Badge.tsx
│   │   ├── Modal.tsx
│   │   ├── Toast.tsx
│   │   ├── Tabs.tsx
│   │   ├── AgentAvatar.tsx
│   │   └── StatusDot.tsx
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── AppShell.tsx
│   └── features/
│       ├── ChatMessage.tsx
│       ├── StreamReveal.tsx
│       ├── AgentCard.tsx
│       ├── MetricCard.tsx
│       ├── DagNode.tsx
│       └── CodeBlock.tsx
├── lib/
│   ├── utils.ts              # cn() helper, class variance authority
│   └── tokens.ts             # TypeScript token constants
└── hooks/
    ├── useAgentStatus.ts
    ├── useReducedMotion.ts
    └── useTheme.ts
```

---

## 13. Implementation Checklist

- [ ] Install Tailwind CSS v4 (`npm install tailwindcss@next`)
- [ ] Configure `globals.css` with `@theme` block
- [ ] Add Google Fonts (Inter, JetBrains Mono, Playfair Display) via `next/font`
- [ ] Implement `AgentAvatar` with conic gradient ring + status dot
- [ ] Implement `StatusDot` with pulse animation for running state
- [ ] Implement dark-only base styles (no light mode required for v2)
- [ ] Add `prefers-reduced-motion` media query globally
- [ ] Verify all color contrast ratios ≥ AA (4.5:1 for text)
- [ ] Add `aria-label` to all icon-only buttons
- [ ] Test keyboard navigation through Sidebar → Pages → Actions
- [ ] Configure `shadow-*` and `z-*` tokens in `@theme`
- [ ] Verify touch targets ≥ 44px on mobile
- [ ] Implement `WorkflowCanvas` with React Flow / xyflow (pan, zoom, snap)
- [ ] Implement `DagNode` variants: task, condition, loop, approval_gate, trigger, delay, end
- [ ] Implement `ConnectionLine` with animated dash on data flow
- [ ] Implement `SeoDashboard` with keyword chart, SERP cards, competitor table
- [ ] Implement `AgentRoleCard` with avatar stack and skill badge grid
- [ ] Implement `ApprovalGateModal` with preview, approve/reject/comment/delegate
- [ ] Add `WorkflowBuilder`, `SeoDashboard`, `AgentRoleManager` routes to sidebar
- [ ] Implement `VoiceWaveform` with 32 bars, agent-color, 30fps amplitude updates
- [ ] Implement `TalkModePanel` full-screen overlay with mic button, avatar, subtitles
- [ ] Implement `PushToTalkButton` with press-and-hold ring expansion animation
- [ ] Implement `MigrationWizard` 6-step flow with step indicator and preview table
- [ ] Implement `BackupWidget` with status badge, progress bar, and "Backup Now" action
- [ ] Add `TalkMode`, `MigrationWizard`, `BackupRestore` routes to sidebar/settings
- [ ] Implement `VoiceWaveform` with amplitude bar animation and agent color theming
- [ ] Implement `TalkModePanel` with full-screen overlay, mic button, agent avatar mouth animation, subtitle scroll
- [ ] Implement `PushToTalkButton` with press-and-hold interaction, expanding ring, cancel gesture
- [ ] Implement `MigrationWizard` with step indicator, upload dropzone, preview table, progress bar with ETA
- [ ] Implement `BackupWidget` with last-backup status, health indicator, "Backup Now" action

---

## 14. Token Quick Reference

| Token | Value | Notes |
|---|---|---|
| `--color-canvas` | `#0A0A0B` | App background |
| `--color-surface` | `#17171A` | Cards, panels |
| `--color-brand-bright` | `#A855F7` | Primary accent, focus |
| `--color-text-primary` | `#F8FAFC` | Main text |
| `--color-text-muted` | `#64748B` | Secondary text |
| `--color-border-subtle` | `rgba(255,255,255,0.06)` | Default borders |
| `--font-sans` | Inter, system-ui | UI text |
| `--font-serif` | Playfair Display, Georgia | Headings |
| `--font-mono` | JetBrains Mono | Code |
| `--radius-lg` | 8px | Cards |
| `--radius-full` | 9999px | Avatars, pills |
| `--shadow-200` | 0 4px 12px rgba(0,0,0,0.4) | Elevated surfaces |
| `--duration-normal` | 180ms | Standard transition |
| `--ease-standard` | `cubic-bezier(0.4,0,0.2,1)` | Default ease |

---

## 15. Related Documents

| Document | ID | Relationship |
|---|---|---|
| Product Vision | `VSN-001` | Strategic context |
| PRD | `PRD-001` | Feature requirements |
| Architecture | `SAD-001` | Backend contracts, data flow |
| API Specification | `API-001` | Endpoint contracts for UI |
| Voice Module | `VCE-001` | STT/TTS pipeline, WebSocket API |
| Import / Export | `IMP-001` | Migration formats and job API |
| Disaster Recovery | `DR-001` | Backup targets, restore procedures |
| Accessibility | `A11Y-001` | Detailed a11y conformance plan |
| Video Evidence | `VIDEO-002` | Screenshot audit, observed patterns |

---

*Document version: 2.0.0*  
*Last updated: 2026-08-11*  
*Owner: UX Lead / Frontend Lead*
