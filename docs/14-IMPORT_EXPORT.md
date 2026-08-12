---
document_id: ART-002
title: Agent OS v2 Goldie Edition Import and Export Module
version: 2.0.0
status: draft
owner: data-owner
approvers:
  - data-owner
  - security-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: true
related_documents: [ART-001, DAT-003, SEC-001]
related_adrs: []
---

# Agent OS v2 — Goldie Edition / Import & Export Module

> **Document:** `14-IMPORT_EXPORT.md`
> **Version:** 2.0.0
> **Status:** Draft
> **Date:** 2026-08-11
> **Classification:** Internal

---

## Table of Contents

1. [Overview](#1-overview)
2. [Import Sources](#2-import-sources)
   - 2.1 Obsidian Vault Import
   - 2.2 Notion Import
   - 2.3 ChatGPT / Claude Export Import
   - 2.4 Evernote / Apple Notes / OneNote
   - 2.5 Generic Markdown Import
3. [Export](#3-export)
4. [Migration Wizard UI](#4-migration-wizard-ui)
5. [Data Model Additions](#5-data-model-additions)
6. [API Endpoints](#6-api-endpoints)
7. [Security & Privacy](#7-security--privacy)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Overview

Users have data everywhere — Obsidian vaults, Notion workspaces, ChatGPT conversation histories, Evernote notebooks. If Agent OS cannot import that data, users will not switch. If Agent OS cannot export data in standard formats, users will not trust it.

**Import reduces adoption friction.** A user with 5,000 Obsidian notes should be able to migrate in under 10 minutes with connections, tags, and attachments intact.

**Export guarantees data portability and trust.** Users must be able to leave with their data at any time, in formats they can open elsewhere (Markdown, JSON, PDF). Encrypted exports ensure that portable backups are secure.

**Key principle:** Import is a first-class feature, not an afterthought. Every supported source gets a dedicated parser, conflict-resolution UI, and progress tracking. Every export format is validated for completeness and integrity.

---

## 2. Import Sources

### 2.1 Obsidian Vault Import

Obsidian is the dominant local-first markdown note-taking tool. Its vault structure (folders of `.md` files + `.obsidian/` config + attachments) maps cleanly to Agent OS Notebook.

**Input formats:**
- ZIP export (recommended): `MyVault.zip` containing folders + `.md` files + attachments.
- Local folder path (Electron/desktop only): direct read from filesystem.

**Parsing pipeline:**
1. **Unpack** — extract ZIP to temp directory; validate structure (at least one `.md` file).
2. **Parse markdown** — for each `.md` file:
   - Extract YAML frontmatter → note metadata (title, tags, created, modified).
   - Preserve wiki-links `[[Note Title]]` → Agent OS wiki-links `[[Note Title]]` ( Notebook links).
   - Preserve hashtags `#tag` → Agent OS tags.
   - Body text → note content (markdown).
3. **Parse attachments** — images, PDFs, audio → stored as Agent OS artifacts with provenance.
4. **Parse graph data** — `.obsidian/graph.json` (if present) → `note_links` table entries for backlink graph.
5. **Conflict resolution** — if a note with same title exists:
   - **Skip** — leave existing note untouched.
   - **Overwrite** — replace with imported version.
   - **Merge** — append imported body to existing body with horizontal rule separator + metadata banner.
6. **Progress tracking** — real-time progress bar: `"Importing 847 of 1,247 notes…"` with ETA calculated from throughput.

**Obsidian plugin handling:**
- Dataview, Templater, Excalidraw plugins → notes containing plugin syntax are imported as-is with a warning badge.
- Future: plugin syntax converters (Dataview tables → markdown tables) in v2.1+.

**Post-import:**
- Full-text index rebuilt.
- Semantic embeddings generated for all imported notes (background queue).
- Import summary report: notes imported, attachments imported, links resolved/unresolved, conflicts handled.

---

### 2.2 Notion Import

Notion is the dominant collaborative knowledge base. Its HTML export preserves rich formatting, databases, and page hierarchy.

**Input format:**
- Notion export ZIP: HTML files + CSV files (for databases) + file attachments + JSON `table_of_contents`.

**Parsing pipeline:**
1. **Unpack** — extract ZIP; read `table_of_contents.json` for page hierarchy.
2. **Parse HTML → Markdown** — using `html-to-markdown` or `turndown` with custom rules:
   - Headers → markdown headers.
   - Bulleted lists → `- ` lists.
   - Numbered lists → `1. ` lists.
   - Tables → markdown tables (with alignment).
   - Callouts → `> **Note:** …` blockquotes.
   - Toggle blocks → collapsible `<details>` HTML (preserved in markdown).
   - Embeds → artifact references with URL.
3. **Preserve page hierarchy** — Notion page tree → Notebook folder structure.
   - Root pages → top-level folders.
   - Sub-pages → nested folders.
   - Database pages → structured notes with properties table.
4. **Parse databases** — CSV files converted to structured notes:
   - Properties (columns) → YAML frontmatter key-value pairs.
   - Rows → individual notes or inline tables depending on user choice.
5. **Parse attachments** — files in `…/` subdirectories → artifacts.
6. **Conflict resolution** — same as Obsidian import.

**Limitations documented:**
- Notion inline databases with complex relations → flattened properties; relations noted as text.
- Notion comments → not imported (no equivalent in Notebook).
- Notion AI-generated content → imported as-is with no special handling.

---

### 2.3 ChatGPT / Claude Export Import

Conversation histories from ChatGPT and Claude contain valuable context, prompts, and shared artifacts.

**ChatGPT import:**
- **Input:** OpenAI data export JSON (`conversations.json`).
- **Parsing:**
  - Each conversation → one Agent OS chat session.
  - Messages mapped: `user` → user message, `assistant` → agent message (model noted in metadata).
  - `create_time` / `update_time` preserved as message timestamps.
  - Shared links extracted from `moderation_results` or message attachments → artifact references.
  - Custom GPTs noted as "imported custom GPT" with name preserved.
- **Tag:** All imported chats auto-tagged `"imported-from-chatgpt"`.

**Claude import:**
- **Input:** Anthropic export (JSON or markdown transcript, depending on Anthropic's current export format).
- **Parsing:**
  - Each conversation → chat session.
  - Messages mapped with `sender` (human/assistant) and `timestamp`.
  - Attachments (if included in export) → artifacts.
- **Tag:** `"imported-from-claude"`.

**Thread structure preservation:**
- ChatGPT's branching conversations (where user edits a message and creates a parallel branch) → flattened into the main thread with branch notes in metadata.
- Future: full branch tree visualization in v2.2+.

---

### 2.4 Evernote / Apple Notes / OneNote

**Evernote (ENEX):**
- **Input:** `.enex` file (Evernote XML export).
- **Parsing:**
  - Each `<note>` → one Agent OS note.
  - `<title>` → note title.
  - `<content>` (ENML) → converted to markdown via ENML→MD transformer.
  - `<tag>` → Agent OS tags.
  - `<notebook>` → Notebook folder.
  - `<resource>` (attachments) → artifacts.
  - `<created>` / `<updated>` → timestamps.
- **Conflict resolution:** same as Obsidian.

**Apple Notes:**
- No official API for bulk export.
- **Documented path:** Manual copy-paste per note, or use third-party exporter tools (e.g., `exporter` CLI) to produce Markdown/JSON, then import via Generic Markdown Import.
- UI shows: "Apple Notes has no official export. Use a third-party tool to export to Markdown, then use Generic Import below."

**OneNote:**
- Microsoft Graph API allows reading notebooks, sections, and pages.
- **Documented path:** Enterprise users can use Graph API token; personal users export sections as `.mht` or PDF, then manually convert.
- UI shows: "OneNote export via Microsoft Graph API (enterprise) or manual export to HTML."
- `.mht`/HTML parsed to markdown via same pipeline as Notion HTML import.

---

### 2.5 Generic Markdown Import

The catch-all for any folder of `.md` files.

**Input:**
- ZIP of `.md` files, or drag-and-drop folder (Electron/desktop).
- Supports nested folder structures.

**Auto-detection:**
- Wiki-links `[[...]]` — converted to Notebook links.
- Tags `#tag` or frontmatter `tags: [...]` — preserved.
- Frontmatter YAML — parsed into note metadata.
- Links to local images/PDFs — imported as artifacts.

**Bulk operations:**
- Drag-and-drop onto Notebook sidebar triggers import wizard.
- Preview first 10 items before confirming.
- Option to import into existing folder or create new folder.

---

## 3. Export

### 3.1 Workspace Export

Complete workspace snapshot in a single ZIP.

**Contents:**
```
workspace-export-{slug}-{timestamp}.zip
├── db_dump.sql              # SQLite/PostgreSQL dump of workspace tables
├── notes/                   # All Notebook pages as .md files
│   ├── folder-a/
│   ├── folder-b/
│   └── …
├── artifacts/               # All artifacts with original filenames
│   ├── images/
│   ├── documents/
│   └── …
├── chats/                   # All chat sessions as JSON
│   ├── session-uuid.json
│   └── …
├── config.json              # Workspace settings, agent configs, roles
│   (API keys excluded by default)
└── manifest.json            # Inventory: counts, checksums, export metadata
```

**Options:**
- Include API keys: opt-in checkbox (dangerously labeled "Include provider credentials").
- Filter by date range: only export data created after a chosen date.
- Filter by type: notes only, chats only, or full workspace.

---

### 3.2 Notebook Export

Obsidian-compatible ZIP of all notes.

**Contents:**
```
notebook-export-{slug}-{timestamp}.zip
├── folder-a/
│   ├── Note Title.md
│   └── …
├── folder-b/
│   └── …
├── attachments/             # Images, PDFs referenced by notes
└── .obsidian/app.json       # Minimal Obsidian config for compatibility
```

**Compatibility guarantees:**
- Wiki-links `[[Note Title]]` preserved.
- Frontmatter YAML preserved.
- Tags preserved as frontmatter or inline hashtags.
- Attachments referenced with relative paths.

---

### 3.3 Chat Export

Conversation histories in JSON or Markdown transcript.

**JSON format:**
```json
{
  "sessions": [
    {
      "id": "uuid",
      "title": "SEO Strategy Discussion",
      "agent_id": "uuid",
      "created_at": "2026-08-11T10:00:00Z",
      "messages": [
        { "role": "user", "content": "…", "timestamp": "…" },
        { "role": "agent", "content": "…", "model": "claude-sonnet-4", "timestamp": "…" }
      ]
    }
  ]
}
```

**Markdown transcript:**
- Each session → one `.md` file.
- Format: `# Session Title` → `**User:** …` → `**Agent (Claude):** …`.
- Timestamps in ISO format as HTML comments for machine readability.

---

### 3.4 SEO Report Export

SEO module reports in PDF or HTML.

- **PDF:** Generated via headless browser or PDF library; branded with workspace colors/logo.
- **HTML:** Responsive, interactive charts (Chart.js or similar); self-contained single file with inlined CSS/JS.

See `10-SEO_MODULE.md` §3.10 for detailed report structure.

---

### 3.5 Encrypted Export

Any export format can be encrypted with AES-256-GCM.

**Process:**
1. User provides password (min 12 characters, entropy meter shown).
2. ZIP contents encrypted before archiving.
3. Output: `.zip.enc` or password-protected ZIP (depending on library support).
4. Integrity: SHA-256 checksum of decrypted contents stored in manifest.
5. Recovery: decryption requires the exact password; no backdoor, no recovery key stored.

**UI warning:** "If you lose this password, your export cannot be recovered. Store it in a password manager."

---

## 4. Migration Wizard UI

A 6-step guided wizard for all import sources.

### Step 1: Select Source
- Card grid: Obsidian, Notion, ChatGPT, Claude, Evernote, Generic Markdown.
- Each card shows source icon, brief description, and "Popular" badge for top 2.

### Step 2: Upload File or Provide Path
- **ZIP upload:** Drag-and-drop zone with max size indicator (2 GB).
- **Local path:** Text input (Electron/desktop only) with "Browse" button.
- **Validation:** File type check, size check, basic structure validation (e.g., ZIP contains `.md` files for Obsidian).

### Step 3: Preview
- Table showing first 10 items with mapping preview:
  - Original title → Mapped title
  - Original type → Agent OS type
  - Status: Ready / Conflict / Error
- If conflicts detected, highlight rows and show conflict count.

### Step 4: Configure
- **Folder mapping:** Map source folders to Notebook folders (auto-mapped by name similarity).
- **Conflict resolution:** Global toggle — Skip / Overwrite / Merge (overridable per item).
- **Tag rules:** Prefix imported tags (e.g., `"imported/obsidian"`) or preserve as-is.
- **Date handling:** Use original created/modified dates vs. import timestamp.

### Step 5: Import
- Progress bar with ETA, cancel button, and real-time log.
- Log shows: item name, status, error (if any).
- Cancel gracefully: already-imported items kept; resume from checkpoint supported.

### Step 6: Review
- Summary cards: Imported (green), Skipped (yellow), Errors (red).
- Error log: expandable panel with full error messages and item names.
- Actions: "Go to Notebook", "Export error log" (JSON), "Import another source".

---

## 5. Data Model Additions

### 5.1 `import_jobs`

Tracks all import operations.

```sql
CREATE TABLE import_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    source_type     VARCHAR(50) NOT NULL
    CHECK (source_type IN ('obsidian', 'notion', 'chatgpt', 'claude', 'evernote', 'generic_markdown', 'onenote')),
    source_name     VARCHAR(255),
    input_ref       TEXT NOT NULL,          -- path to uploaded ZIP or folder
    status          VARCHAR(50) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'validating', 'preview_ready', 'running', 'completed', 'failed', 'cancelled')),
    config_json     JSONB DEFAULT '{}',     -- conflict_resolution, tag_rules, folder_mapping
    progress_pct    INTEGER DEFAULT 0
    CHECK (progress_pct BETWEEN 0 AND 100),
    items_total     INTEGER,
    items_imported  INTEGER DEFAULT 0,
    items_skipped   INTEGER DEFAULT 0,
    items_failed    INTEGER DEFAULT 0,
    error_log       TEXT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_import_jobs_workspace ON import_jobs(workspace_id);
CREATE INDEX idx_import_jobs_user ON import_jobs(user_id);
CREATE INDEX idx_import_jobs_status ON import_jobs(status);
CREATE INDEX idx_import_jobs_created ON import_jobs(created_at);
```

### 5.2 `import_mappings`

Maps individual imported items to their Agent OS counterparts.

```sql
CREATE TABLE import_mappings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id          UUID NOT NULL REFERENCES import_jobs(id) ON DELETE CASCADE,
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    source_type     VARCHAR(50) NOT NULL,
    source_id       TEXT,                   -- original ID (e.g., Obsidian filename, Notion page ID)
    source_title    TEXT,
    target_type     VARCHAR(50) NOT NULL
    CHECK (target_type IN ('note', 'artifact', 'chat_session', 'tag', 'folder')),
    target_id       UUID,                   -- Agent OS ID after import
    target_title    TEXT,
    status          VARCHAR(50) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'imported', 'skipped', 'failed', 'merged')),
    error_message   TEXT,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_import_mappings_job ON import_mappings(job_id);
CREATE INDEX idx_import_mappings_workspace ON import_mappings(workspace_id);
CREATE INDEX idx_import_mappings_status ON import_mappings(status);
CREATE INDEX idx_import_mappings_target ON import_mappings(target_type, target_id);
```

### 5.3 `export_jobs`

Tracks all export operations.

```sql
CREATE TABLE export_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    export_type     VARCHAR(50) NOT NULL
    CHECK (export_type IN ('workspace', 'notebook', 'chats', 'seo_report', 'audit_package')),
    format          VARCHAR(50) NOT NULL
    CHECK (format IN ('zip', 'json', 'markdown', 'pdf', 'html')),
    scope_json      JSONB DEFAULT '{}',     -- filters: date_range, include_api_keys, etc.
    status          VARCHAR(50) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'running', 'completed', 'failed', 'cancelled')),
    file_ref        TEXT,                   -- path to generated file
    file_size_bytes BIGINT,
    checksum        VARCHAR(64),            -- SHA-256
    encrypted       BOOLEAN DEFAULT FALSE,
    error_message   TEXT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_export_jobs_workspace ON export_jobs(workspace_id);
CREATE INDEX idx_export_jobs_user ON export_jobs(user_id);
CREATE INDEX idx_export_jobs_status ON export_jobs(status);
CREATE INDEX idx_export_jobs_created ON export_jobs(created_at);
```

---

## 6. API Endpoints

### 6.1 Import

#### POST `/api/v1/import`
- **Auth:** Bearer (workspace member+)
- **Content-Type:** `multipart/form-data`
- **Request:**
  - `file`: ZIP or folder archive.
  - `source_type`: `"obsidian"` | `"notion"` | `"chatgpt"` | `"claude"` | `"evernote"` | `"generic_markdown"`.
  - `config_json`: stringified JSON with `conflict_resolution`, `tag_rules`, `folder_mapping`.
- **Response:**
```json
{
  "job_id": "uuid",
  "status": "pending",
  "message": "Import job queued. Use GET /import/{id} to track progress."
}
```

#### GET `/api/v1/import/{job_id}`
- **Auth:** Bearer
- **Response:**
```json
{
  "id": "uuid",
  "status": "running",
  "progress_pct": 67,
  "items_total": 1247,
  "items_imported": 836,
  "items_skipped": 0,
  "items_failed": 2,
  "eta_seconds": 180,
  "error_log": "…"
}
```

#### POST `/api/v1/import/{job_id}/cancel`
- **Auth:** Bearer
- **Response:** `200` with updated status `"cancelled"`.

#### GET `/api/v1/import/{job_id}/preview`
- **Auth:** Bearer
- **Response:** First 10 items with mapping preview (same structure as import_mappings table).

---

### 6.2 Export

#### POST `/api/v1/export`
- **Auth:** Bearer
- **Request:**
```json
{
  "export_type": "workspace",
  "format": "zip",
  "scope_json": {
    "date_from": "2026-01-01",
    "date_to": "2026-08-11",
    "include_api_keys": false,
    "include_chats": true,
    "include_artifacts": true
  },
  "encrypted": true,
  "password": "…"
}
```
- **Response:**
```json
{
  "job_id": "uuid",
  "status": "running",
  "message": "Export job queued."
}
```

#### GET `/api/v1/export/{job_id}`
- **Auth:** Bearer
- **Response:** Export job status and metadata.

#### GET `/api/v1/export/{job_id}/download`
- **Auth:** Bearer
- **Response:** `302` redirect to presigned URL, or `200` with `application/octet-stream` if served directly.
- **Behavior:** Download link valid for 24 hours; one-time use if served directly.

---

## 7. Security & Privacy

### 7.1 Data Isolation
- Import jobs are workspace-scoped; no cross-workspace data leakage.
- Uploaded files stored in workspace-isolated temp directories.
- Temp files deleted after import completion or after 24 hours (whichever comes first).

### 7.2 Credential Protection
- Exported `config.json` excludes API keys by default.
- If user opts in to include API keys, they are encrypted with the same AES-256-GCM password as the rest of the export.
- Export passwords are never stored server-side; they exist only in the user's session during generation.

### 7.3 Audit & Compliance
- Every import and export emits audit events: `import_started`, `import_completed`, `export_started`, `export_downloaded`.
- Failed imports log error details (without exposing sensitive data) for ops debugging.

---

## 8. Troubleshooting

| Issue | Likely Cause | Resolution |
|---|---|---|
| "ZIP contains no `.md` files" | Wrong file selected, or ZIP is a different export format | Verify export source; try re-exporting from original app |
| "Notion HTML parse failed" | Complex embeds or unsupported block types | Retry with "skip unsupported blocks" option; report block type for future support |
| "ChatGPT JSON parse failed" | Export format changed by OpenAI | Check OpenAI export format version; update parser if needed |
| "Out of memory during import" | Very large vault (>50K notes) on limited RAM | Split vault into chunks; use local path import instead of ZIP |
| "Export too large to download" | >2GB workspace with many artifacts | Use Notebook-only export, or use backup/restore for large data |

---

*End of Import & Export Module Document*
