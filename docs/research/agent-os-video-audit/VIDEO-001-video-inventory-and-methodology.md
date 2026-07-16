---
document_id: VIDEO-001
title: Video Inventory and Methodology
version: 0.1.0
status: draft
owner: research-owner
approvers:
  - product-owner
created: 2026-07-16
last_reviewed: 2026-07-16
classification: internal
source_of_truth: false
related_documents:
  - VSN-001
  - SCP-001
  - PRD-001
  - SAD-001
  - UXA-001
  - DSN-001
  - SEC-001
  - TST-001
related_adrs: []
---

# VIDEO-001 — Video Inventory and Methodology

| Field | Value |
|---|---|
| Status | Draft |
| Date | 2026-07-16 |
| Scope | Local video evidence only; no product implementation |

## Evidence labels

- **OBSERVED** — directly visible in a reviewed frame or interaction.
- **STATED** — paraphrased from local timestamped narration.
- **INFERRED** — interpretation consistent with, but not proved by, the evidence.
- **PROPOSED** — audit recommendation.
- **NOT CONFIRMED** — the videos do not establish functional reality.

## Source inventory

Creation time is container metadata and is **low trust**. Language `und` means the stream has no declared language. None of the files has an embedded subtitle stream.

| ID | Exact relative path | Size | Duration | Video | Audio | Subtitles | Low-trust creation metadata | SHA-256 |
|---|---|---:|---:|---|---|---|---|---|
| A | `Claude + Hermes Agent_ NEW Agent OS is INSANE!.mp4` | 144,341,594 B | 00:35:21.700 | H.264, 1280×720, 30 fps | AAC, language `und` | None | 2026-05-16T03:42:47Z | `c5092c6d944fcb0836192f224be89490174a35c4387479d4882ee06c9a8e9eaa` |
| B | `Hermes Agent Desktop vs Agent OS- Which Wins..mp4` | 36,464,211 B | 00:10:28.169 | H.264, 1280×720, 30 fps | AAC, language `und` | None | 2026-06-03T00:13:03Z | `38de2d43ef1308ecae1d018daa5e734f167da79bc54368445b8806079109b3ad` |
| C | `How to Build Your Own Agent Operating System.mp4` | 67,955,791 B | 00:32:40.972 | H.264, 1280×720, 30 fps | AAC, language `und` | None | 2026-05-25T14:11:14Z | `7f13d13a5d4ee844b970b1b3f4ee60b5db3b21ff0be65e99d347e242f2116026` |
| D | `How to Build Your Own Agent OS (FREE) - Julian Goldie.mp4` | 26,362,830 B | 00:07:59.678 | H.264, 1138×640, 30 fps | AAC, language `und` | None | Not present | `b1c5d1cc10ff8b5e786f0e053a1165cb60dbe7860e4e7c2e99d3267505904629` |

## Repository discovery

The working folder has no applicable `AGENTS.md`, README, governance document, glossary, register, vision, PRD, or architecture document. `git rev-parse` reports that the folder is not a Git repository. The source prompt is therefore the only governance source, and the suggested `VIDEO-001` through `VIDEO-004` names were used without claiming registration or approval.

## Tools and method

- `ffprobe` collected stream/container metadata; `sha256sum` calculated source checksums.
- Video A was freshly sampled at 60-second intervals (35 frames) and at scene changes using `select='gt(scene,0.32)'`, capped at 40 frames. Timestamps were burned into each extracted image.
- Existing local `_work/` assets for B–D were inspected, mapped to the exact filenames using `_work/transcribe.py`, and copied into the isolated audit directory rather than regenerated after an interrupted full decode. They comprise regular approximately 15-second samples (B 42, C 131, D 32) and capped scene samples (B 48, C 32, D 24). Four incomplete B extraction frames are also retained, yielding 46 B interval files.
- Eight numbered contact sheets provide broad review coverage. Individual source-resolution frames were reviewed when the sheets were ambiguous.
- Three existing local Whisper transcripts (B–D) were copied as supporting evidence. Their opening narration and durations were cross-checked against the matching videos. No long transcript passages are reproduced.
- A mono 16 kHz local WAV was extracted for A, but transcription was not completed: the current Python environment cannot import `faster_whisper`. No package or model was installed or downloaded.

Representative commands:

```bash
ffprobe -v error -show_entries format -show_entries stream -of json VIDEO.mp4
sha256sum ./*.mp4
ffmpeg -i VIDEO.mp4 -vf "fps=1/60,drawtext=...:text='%{pts\\:hms}'" interval_%03d.jpg
ffmpeg -i VIDEO.mp4 -vf "select='gt(scene,0.32)',drawtext=..." -frames:v 40 scene_%03d.jpg
```

## Derived assets

All assets are local under `.local-analysis/agent-os-video-audit/`: `frames/`, `contact-sheets/`, `transcripts/`, and `audio/`. These are analysis artifacts, not product source. Source videos were not altered.

## Limitations

- Sampling can miss brief states, hover labels, motion, or interactions between frames.
- A has no timestamped transcript; audio-only claims from it are not relied upon.
- Whisper text can contain recognition errors, especially product names; it is supporting, not sole, evidence.
- No backend, persistence, identity, security, accounting source, API request, or production deployment was inspected. Those properties are **NOT CONFIRMED**.
- Several videos are promotional/tutorial content and include external web pages. A screen appearing in the edit does not prove it belongs to, or is integrated with, Agent OS.
