# Agent OS v2 — Goldie Edition / Voice & Talk Mode Module

> **Document:** `13-VOICE_MODULE.md`  
> **Version:** 2.0.0  
> **Status:** Draft  
> **Date:** 2026-08-11  
> **Classification:** Internal

---

## Table of Contents

1. [Overview](#1-overview)
2. [Voice Architecture](#2-voice-architecture)
3. [Features](#3-features)
   - 3.1 Push-to-Talk
   - 3.2 Text-to-Speech (TTS)
   - 3.3 Speech-to-Text (STT)
   - 3.4 Agent Vocal Mode
   - 3.5 Talk Mode UI
4. [Data Model Additions](#4-data-model-additions)
5. [API Endpoints](#5-api-endpoints)
6. [Workflows](#6-workflows)
7. [Provider Integrations](#7-provider-integrations)
8. [Security & Privacy](#8-security--privacy)

---

## 1. Overview

Voice transforms Agent OS from a chatbot interface into a true operating system — one you can talk to, listen to, and control hands-free. Goldie's vision of "talk mode" and a "voice assistant that controls the computer" is not a gimmick; it is a fundamental interaction paradigm that removes friction for power users and unlocks accessibility for everyone.

**Why voice matters:**
- **Accessibility** — users with motor or vision impairments can operate the entire system without a keyboard.
- **Speed** — speaking is 3× faster than typing for most users.
- **Hands-free** — operators can trigger agents, query Mission Control, and approve tasks while working in other tools.
- **Natural interaction** — voice is the most human interface; it builds trust and reduces cognitive load.

**Key principle:** Voice is not a separate app — it is a mode that overlays every surface. Push-to-Talk works in Chat, Mission Control, and the Notebook. TTS narrates agent actions everywhere. The user chooses when to speak, when to type, and when to listen.

---

## 2. Voice Architecture

The Voice Module sits at **Layer 6 (Interface)** and **Layer 7 (Gateway)** of the Agent OS stack, with offline compute at **Layer 2 (Execution)**.

```
┌─────────────────────────────────────────────────────────┐
│  Layer 7: Gateway / BYOK Model Router                   │
│  ├─ ElevenLabs TTS API                                  │
│  ├─ OpenAI Whisper API                                  │
│  ├─ Grok TTS API                                        │
│  └─ Kokoro TTS (local, via Hermes Gateway)              │
├─────────────────────────────────────────────────────────┤
│  Layer 6: Interface (Talk Mode Panel, Waveform,         │
│           Push-to-Talk, Agent Avatar mouth animation)   │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Orchestration (Voice sessions, turn-taking,   │
│           wake-word routing, agent vocal narration)      │
├─────────────────────────────────────────────────────────┤
│  Layer 2: Execution (Whisper STT, Kokoro TTS, VAD,      │
│           RNNoise, streaming chunking)                   │
├─────────────────────────────────────────────────────────┤
│  Layer 1: Persistence (voice_sessions, voice_messages, │
│           voice_profiles, tts_jobs, stt_jobs)           │
└─────────────────────────────────────────────────────────┘
```

**Pipeline (single turn):**

```
[Audio Input] ──► [VAD + Noise Suppression] ──► [STT: Whisper]
                                                          │
                                                          ▼
[Audio Output] ◄── [TTS: Kokoro / ElevenLabs] ◄── [NLP / Intent]
       │                                                  │
       └──────────── [Agent Execution] ◄──────────────────┘
```

1. **Audio Input** — microphone capture via WebAudio API or Electron native.
2. **VAD + Noise Suppression** — Voice Activity Detection gates recording; RNNoise filters background noise.
3. **STT** — faster-whisper (local) or OpenAI Whisper API (cloud) produces transcript.
4. **NLP / Intent** — transcript forwarded to active agent or intent router.
5. **Agent Execution** — agent processes request, produces response text.
6. **TTS** — response text streamed to Kokoro (local), ElevenLabs, or Grok TTS.
7. **Audio Output** — decoded PCM played through WebAudio; waveform visualizer animates during playback.

---

## 3. Features

### 3.1 Push-to-Talk

The primary voice input mechanism. Modeled after Discord and Voxer for muscle-memory compatibility.

**Interactions:**
- **Hold Spacebar** = start recording; **Release** = send audio for transcription.
- **Visual waveform** during recording: amplitude bars in the active agent's brand color (e.g., `#F97316` for Claude, `#3B82F6` for Hermes). Bars animate in real time via WebAudio AnalyserNode.
- **Auto-transcription preview** — a live transcript appears above the input bar before release. User can release to confirm or continue holding to extend recording.
- **Cancel gesture** — swipe left while holding (touch) or press `Esc` while holding (keyboard) to discard the recording without sending.
- **Keyboard shortcuts:**
  - `Space` — push-to-talk when Agent OS window is focused.
  - `Shift+Space` — global hotkey (captured by Electron globalShortcut; brings app to foreground + starts recording).

**Implementation notes:**
- Recording format: WebM/Opus in browser; WAV/PCM fallback for Electron.
- Chunk size: 250 ms packets streamed to STT for minimal latency.
- Maximum hold duration: 5 minutes (configurable); auto-send at limit.

---

### 3.2 Text-to-Speech (TTS)

Agents speak their responses. TTS is streaming, profiled, and selectable per session.

**Providers:**

| Provider | Type | Quality | Latency | Offline | Cost |
|---|---|---|---|---|---|
| **Kokoro TTS** | Local ONNX | Good | Low | ✅ | Free |
| **ElevenLabs** | Cloud API | Excellent | Medium | ❌ | Per-character |
| **Grok TTS** | Cloud API | Good | Medium | ❌ | Included with X Premium+ |

**Agent voice profiles:**
- Each agent can have a distinct voice profile: voice ID, pitch shift (+/- 20%), speed (0.75×–1.5×), pause duration.
- Profile inheritance: agent → role → workspace default → system default.
- Per-agent mute/unmute: user can silence any agent while keeping others audible.

**Streaming TTS:**
- First sentence is synthesized and played as soon as available; remaining text streams in parallel.
- Chunking strategy: split on sentence boundaries (`. `, `! `, `? `, `\n\n`).
- Pre-fetch: agent's first sentence can be pre-generated from a template while the full response is being composed.

**Configuration per workspace:**
```json
{
  "tts_provider": "kokoro",
  "tts_fallback_provider": "elevenlabs",
  "streaming_enabled": true,
  "default_speed": 1.0,
  "agent_profiles": {
    "claude": { "voice_id": "af_sarah", "pitch": 0, "speed": 1.05 },
    "hermes": { "voice_id": "am_michael", "pitch": -2, "speed": 0.95 }
  }
}
```

---

### 3.3 Speech-to-Text (STT)

Transcribes user speech into text for agent consumption.

**Providers:**

| Provider | Type | Accuracy | Latency | Offline | Languages |
|---|---|---|---|---|---|
| **faster-whisper** | Local (CTranslate2, int8) | Very Good | Low | ✅ | 99+ |
| **OpenAI Whisper API** | Cloud | Excellent | Medium | ❌ | 99+ |

**Features:**
- **Language detection** — auto-detect spoken language from first 3 seconds; switch model if needed.
- **Auto-switch** — multilingual users can speak any supported language without manual config; detected language is tagged on the message.
- **Punctuation auto-correction** — post-process transcript with lightweight NLP model to fix missing periods and capitalization.
- **Noise suppression** — RNNoise (WebAssembly) applied to input buffer before STT; significantly improves accuracy in open-office environments.

**Performance targets:**
- Local STT: < 800 ms for a 10-second utterance on a 4-core CPU.
- Cloud STT: < 400 ms for same utterance (network dependent).

---

### 3.4 Agent Vocal Mode

Agents are not silent black boxes — they can narrate their thinking and read results aloud.

**Thinking narration:**
- Agent emits structured "thinking" events during execution: `"I'm analyzing the SERP for 'best AI tools'..."`
- Configurable verbosity: `none` | `minimal` ( milestones only) | `verbose` (every sub-step).
- Thinking audio is queued behind the main response audio or interleaved based on user preference.

**Result read-back:**
- Per-task toggle: agent can read a summary of results in voice after completion.
- Example: *"I've found 12 competitors. The top three are Ahrefs, SEMrush, and Moz. Shall I generate a response brief?"*

**Wake word detection:**
- Phrase: `"Hey Agent OS"` (configurable per workspace).
- Trigger: hands-free activation starts listening mode without a keypress.
- Implementation: lightweight keyword spotting model (e.g., Porcupine or open-source alternative) running locally. No audio leaves the device until wake word fires.

**Voice Activity Detection (VAD):**
- Silero VAD or similar running locally.
- Enables natural conversation flow: system detects when user stops speaking, automatically ends turn, and starts agent processing.
- Prevents premature cutoff during pauses (configurable silence threshold: 800 ms default).

---

### 3.5 Talk Mode UI

A dedicated full-screen voice-first interface accessible from any page via a floating mic pill or `Ctrl+Shift+T`.

**Layout:**
- **Center:** Large circular microphone button (80px) with conic gradient ring that expands while recording.
- **Agent avatar:** Above the mic; animates mouth when agent is speaking (simple SVG mouth shape morph driven by audio amplitude).
- **Waveform visualizer:** Wraps the mic button; bars radiate outward in agent color during recording and inward during playback.
- **Subtitle transcript:** Scrollable text feed below mic (like movie subtitles); user transcript on left, agent response on right.
- **Conversation history:** Persistent hybrid transcript (audio + text); each turn playable via small speaker icon.
- **Mode toggle:** Three-way switch:
  - **Text-only** — voice input disabled; standard chat UI.
  - **Voice-first** — all input via push-to-talk; all agent responses spoken.
  - **Auto** — voice for short responses (< 150 words), text for long responses; user can override per message.

**Responsive:**
- Desktop: center-panel overlay with blurred background (`backdrop-blur-md`).
- Mobile: full-screen sheet; bottom nav hides; swipe down to dismiss.

---

## 4. Data Model Additions

### 4.1 `voice_sessions`

A voice conversation session, scoped to a user and optionally an agent.

```sql
CREATE TABLE voice_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    agent_id        UUID REFERENCES agents(id) ON DELETE SET NULL,
    title           VARCHAR(500),
    mode            VARCHAR(50) NOT NULL DEFAULT 'auto'
    CHECK (mode IN ('text_only', 'voice_first', 'auto')),
    stt_provider    VARCHAR(50) NOT NULL DEFAULT 'whisper_local'
    CHECK (stt_provider IN ('whisper_local', 'whisper_api')),
    tts_provider    VARCHAR(50) NOT NULL DEFAULT 'kokoro'
    CHECK (tts_provider IN ('kokoro', 'elevenlabs', 'grok')),
    wake_word_enabled BOOLEAN DEFAULT FALSE,
    vad_enabled     BOOLEAN DEFAULT TRUE,
    noise_suppression BOOLEAN DEFAULT TRUE,
    audio_retention_days INTEGER DEFAULT 7,
    privacy_cloud_consent BOOLEAN DEFAULT FALSE,
    status          VARCHAR(50) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'paused', 'ended', 'error')),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ended_at        TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_voice_sessions_workspace ON voice_sessions(workspace_id);
CREATE INDEX idx_voice_sessions_user ON voice_sessions(user_id);
CREATE INDEX idx_voice_sessions_agent ON voice_sessions(agent_id);
CREATE INDEX idx_voice_sessions_status ON voice_sessions(status);
CREATE INDEX idx_voice_sessions_started ON voice_sessions(started_at);
```

### 4.2 `voice_messages`

Individual turns within a voice session.

```sql
CREATE TABLE voice_messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES voice_sessions(id) ON DELETE CASCADE,
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    agent_id        UUID REFERENCES agents(id) ON DELETE SET NULL,
    role            VARCHAR(50) NOT NULL
    CHECK (role IN ('user', 'agent', 'system')),
    content_text    TEXT NOT NULL,
    audio_blob_ref  TEXT,
    audio_duration_ms INTEGER,
    audio_format    VARCHAR(20) DEFAULT 'webm'
    CHECK (audio_format IN ('webm', 'ogg', 'wav', 'mp3')),
    stt_confidence  NUMERIC(4,3),
    tts_voice_profile_id UUID REFERENCES voice_profiles(id) ON DELETE SET NULL,
    language        VARCHAR(10) DEFAULT 'en',
    mode_override   VARCHAR(50)
    CHECK (mode_override IN ('text_only', 'voice_first', 'auto')),
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_voice_messages_session ON voice_messages(session_id);
CREATE INDEX idx_voice_messages_workspace ON voice_messages(workspace_id);
CREATE INDEX idx_voice_messages_created ON voice_messages(created_at);
CREATE INDEX idx_voice_messages_role ON voice_messages(role);
```

### 4.3 `voice_profiles`

Per-agent or per-user voice configurations.

```sql
CREATE TABLE voice_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    owner_type      VARCHAR(50) NOT NULL
    CHECK (owner_type IN ('agent', 'user', 'workspace_default')),
    owner_id        UUID NOT NULL,
    name            VARCHAR(255) NOT NULL,
    tts_provider    VARCHAR(50) NOT NULL DEFAULT 'kokoro'
    CHECK (tts_provider IN ('kokoro', 'elevenlabs', 'grok')),
    voice_id        VARCHAR(255) NOT NULL DEFAULT 'default',
    pitch_shift     NUMERIC(3,2) DEFAULT 0.00
    CHECK (pitch_shift BETWEEN -0.20 AND 0.20),
    speed           NUMERIC(3,2) DEFAULT 1.00
    CHECK (speed BETWEEN 0.75 AND 1.50),
    pause_duration_ms INTEGER DEFAULT 250
    CHECK (pause_duration_ms BETWEEN 0 AND 1000),
    is_muted        BOOLEAN DEFAULT FALSE,
    is_default      BOOLEAN DEFAULT FALSE,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (workspace_id, owner_type, owner_id, name)
);

CREATE INDEX idx_voice_profiles_workspace ON voice_profiles(workspace_id);
CREATE INDEX idx_voice_profiles_owner ON voice_profiles(owner_type, owner_id);
CREATE INDEX idx_voice_profiles_muted ON voice_profiles(is_muted);
```

### 4.4 `tts_jobs`

Tracking and queuing for TTS generation.

```sql
CREATE TABLE tts_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    session_id      UUID REFERENCES voice_sessions(id) ON DELETE SET NULL,
    message_id      UUID REFERENCES voice_messages(id) ON DELETE SET NULL,
    text            TEXT NOT NULL,
    provider        VARCHAR(50) NOT NULL
    CHECK (provider IN ('kokoro', 'elevenlabs', 'grok')),
    voice_profile_id UUID REFERENCES voice_profiles(id) ON DELETE SET NULL,
    status          VARCHAR(50) NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'cancelled')),
    audio_blob_ref  TEXT,
    audio_duration_ms INTEGER,
    error_message   TEXT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tts_jobs_workspace ON tts_jobs(workspace_id);
CREATE INDEX idx_tts_jobs_session ON tts_jobs(session_id);
CREATE INDEX idx_tts_jobs_status ON tts_jobs(status);
CREATE INDEX idx_tts_jobs_created ON tts_jobs(created_at);
```

### 4.5 `stt_jobs`

Tracking and queuing for STT transcription.

```sql
CREATE TABLE stt_jobs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    session_id      UUID REFERENCES voice_sessions(id) ON DELETE SET NULL,
    message_id      UUID REFERENCES voice_messages(id) ON DELETE SET NULL,
    audio_blob_ref  TEXT NOT NULL,
    audio_format    VARCHAR(20) NOT NULL DEFAULT 'webm'
    CHECK (audio_format IN ('webm', 'ogg', 'wav', 'mp3', 'opus')),
    provider        VARCHAR(50) NOT NULL
    CHECK (provider IN ('whisper_local', 'whisper_api')),
    language_hint   VARCHAR(10),
    transcript      TEXT,
    confidence      NUMERIC(4,3),
    status          VARCHAR(50) NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'cancelled')),
    error_message   TEXT,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stt_jobs_workspace ON stt_jobs(workspace_id);
CREATE INDEX idx_stt_jobs_session ON stt_jobs(session_id);
CREATE INDEX idx_stt_jobs_status ON stt_jobs(status);
CREATE INDEX idx_stt_jobs_created ON stt_jobs(created_at);
```

---

## 5. API Endpoints

### 5.1 Speech-to-Text

#### POST `/api/v1/voice/stt`
- **Auth:** Bearer
- **Content-Type:** `multipart/form-data`
- **Request:**
  - `audio`: audio blob (WebM/Opus, WAV, or OGG)
  - `session_id`: UUID (optional; creates orphan job if absent)
  - `language_hint`: string, e.g. `"en"` (optional)
  - `provider`: `"whisper_local"` | `"whisper_api"` (optional; defaults to workspace setting)
- **Response:**
```json
{
  "job_id": "uuid",
  "transcript": "Hey Agent OS, analyze the SERP for best AI tools.",
  "confidence": 0.94,
  "language": "en",
  "duration_ms": 3200,
  "provider": "whisper_local"
}
```
- **Behavior:** If async processing is required (large file or queue depth), returns `202` with `job_id` and polls to `/api/v1/voice/stt/{job_id}`.

#### GET `/api/v1/voice/stt/{job_id}`
- **Auth:** Bearer
- **Response:** STT job status and result when complete.

---

### 5.2 Text-to-Speech

#### POST `/api/v1/voice/tts`
- **Auth:** Bearer
- **Request:**
```json
{
  "text": "I've analyzed the SERP. The top result is a comparison article from TechRadar.",
  "voice_profile_id": "uuid",
  "provider": "kokoro",
  "stream": true,
  "session_id": "uuid"
}
```
- **Response:**
  - `stream: true` — `audio/mpeg` or `audio/wav` streamed chunks (`Transfer-Encoding: chunked`).
  - `stream: false` — `200` with JSON containing `audio_url` (presigned URL to blob storage).

#### GET `/api/v1/voice/tts/{job_id}`
- **Auth:** Bearer
- **Response:** TTS job status and download URL when complete.

---

### 5.3 Real-Time Voice WebSocket

#### WS `/api/v1/voice/stream`
- **Auth:** Bearer token passed via `?token=` query param (WebSocket header auth is unreliable in browsers).
- **Protocol:** Bidirectional binary + JSON.

**Client → Server:**
```json
{
  "type": "audio_chunk",
  "session_id": "uuid",
  "payload": "base64(opus_250ms_packet)"
}
```

**Server → Client:**
```json
{
  "type": "transcript_partial",
  "text": "Hey Agent OS",
  "is_final": false
}
```

```json
{
  "type": "transcript_final",
  "text": "Hey Agent OS, analyze the SERP for best AI tools.",
  "confidence": 0.94,
  "language": "en"
}
```

```json
{
  "type": "audio_chunk",
  "payload": "base64(mp3_chunk)",
  "agent_id": "uuid",
  "is_final": false
}
```

**Control messages:**
- `type: "start_session"` — initializes a new voice session with config.
- `type: "end_session"` — closes session, flushes buffers.
- `type: "interrupt"` — user cut off agent mid-sentence; stop TTS playback.
- `type: "mode_change"` — switch between `text_only`, `voice_first`, `auto`.

---

### 5.4 Voice Profiles

#### GET `/api/v1/voice/profiles`
- **Auth:** Bearer
- **Query:** `?workspace_id=uuid&owner_type=agent&owner_id=uuid`
- **Response:** Array of voice profiles.

#### POST `/api/v1/voice/profiles`
- **Auth:** Bearer (workspace owner/admin)
- **Request:** Voice profile JSON (see Data Model).
- **Response:** Created profile.

#### PATCH `/api/v1/voice/profiles/{profile_id}`
- **Auth:** Bearer

#### DELETE `/api/v1/voice/profiles/{profile_id}`
- **Auth:** Bearer

---

### 5.5 Voice Sessions

#### GET `/api/v1/voice/sessions`
- **Auth:** Bearer
- **Query:** `?limit=20&cursor=&status=active`
- **Response:** Paginated voice sessions with message counts and last activity.

#### GET `/api/v1/voice/sessions/{session_id}`
- **Auth:** Bearer
- **Response:** Full session with messages (paginated).

#### POST `/api/v1/voice/sessions`
- **Auth:** Bearer
- **Request:**
```json
{
  "agent_id": "uuid",
  "mode": "auto",
  "stt_provider": "whisper_local",
  "tts_provider": "kokoro",
  "wake_word_enabled": false,
  "vad_enabled": true
}
```

#### DELETE `/api/v1/voice/sessions/{session_id}`
- **Auth:** Bearer
- **Response:** `204` (soft delete — session marked `ended`).

---

## 6. Workflows

### 6.1 Talk Mode Session Lifecycle

```
[User opens Talk Mode]
    → [Create voice_session record]
    → [Initialize WebSocket /api/v1/voice/stream]
    → [User holds Space → VAD active → audio chunks stream]
    → [STT partials appear as subtitles]
    → [User releases Space → final transcript sent to agent]
    → [Agent processes → response text generated]
    → [TTS streaming starts → audio chunks play]
    → [Agent avatar mouth animates during playback]
    → [Waveform visualizer active during recording + playback]
    → [Session persists; user can return later]
```

### 6.2 Voice-Triggered Mission

```
[Wake word detected: "Hey Agent OS"]
    → [Agent OS activates listening mode (no Spacebar needed)]
    → [User: "Run the weekly SEO report for the blog campaign"]
    → [Intent router maps to SEO skill + campaign selector]
    → [Crystal (Orchestrator) confirms via voice]
    → [Workflow starts in background]
    → [Agent narrates milestones as they complete]
    → [Final result: TTS summary + artifact link in Chat]
```

---

## 7. Provider Integrations

| Provider | Type | Endpoint | Auth | Rate Limits | Cost Model |
|---|---|---|---|---|---|
| **Kokoro TTS** | Local ONNX | Internal (Hermes Gateway) | None | CPU-bound | Free |
| **faster-whisper** | Local STT | Internal (Hermes Gateway) | None | CPU-bound | Free |
| **ElevenLabs** | Cloud TTS | REST API v2.1 | API key header | 40 req/s (burst) | Per-character |
| **OpenAI Whisper API** | Cloud STT | REST API v1 | Bearer token | 100 req/min | Per-minute |
| **Grok TTS** | Cloud TTS | xAI REST API | Bearer token | TBD | Included with X Premium+ |
| **Porcupine** | Wake word | Local WASM | License key (free tier) | Real-time | Free tier |
| **Silero VAD** | VAD | Local ONNX | None | Real-time | Free |
| **RNNoise** | Noise suppression | Local WASM | None | Real-time | Free |

**Credential management:**
- Cloud API keys stored as vault references (`credentials_ref`), never in plaintext in config.
- Local-first providers require no credentials and work fully offline.

---

## 8. Security & Privacy

### 8.1 Local-First Guarantee

- **Whisper + Kokoro** = 100% offline voice. No audio ever leaves the device.
- This is the default configuration for fresh installs.
- Cloud providers are opt-in per workspace, with explicit consent UI.

### 8.2 Cloud Toggle & Consent

- Each voice session prompts: `"Use cloud STT/TTS for better accuracy?"` with `Remember my choice` checkbox.
- Toggle available mid-session via Talk Mode UI (shield icon).
- Workspace admin can disable cloud providers entirely via policy.

### 8.3 Audio Retention Policy

- Audio blobs auto-deleted after `audio_retention_days` (default: 7 days, configurable 0–90).
- Setting `audio_retention_days = 0` disables audio storage entirely; only transcripts kept.
- Audio deletion runs as a nightly cron job; verified via integrity checksums.

### 8.4 No Unauthorized Upload

- Audio is never sent to cloud providers without explicit user confirmation per session or blanket workspace consent.
- Wake word detection runs entirely locally; no audio is buffered to cloud while waiting for wake word.
- Electron global hotkey (`Shift+Space`) only captures when the app is already running; it does not start a background listener.

### 8.5 Audit & Compliance

- Every voice session emits audit events: `voice_session_started`, `voice_message_created`, `tts_job_completed`, `stt_job_completed`.
- Cloud provider usage attributed to workspace for cost tracking.
- Failed STT/TTS jobs logged with error classification (network, timeout, malformed audio) for ops monitoring.

---

*End of Voice & Talk Mode Module Document*
