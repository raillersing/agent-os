---
document_id: MOD-002
title: Agent OS v2 SEO Module
version: 2.0.0
status: archived
owner: product-owner
approvers:
  - product-owner
created: 2026-08-11
last_reviewed: 2026-08-12
classification: internal
source_of_truth: false
related_documents: [PRD-002, PLG-001, ART-001]
related_adrs: []
---

# Agent OS v2 / SEO Module

> **Document:** `10-SEO_MODULE.md`
> **Version:** 2.0.0
> **Status:** Draft
> **Date:** 2026-08-11
> **Classification:** Internal

---

## 1. Overview

SEO is not an add-on to Agent OS — it is a core competency. Agent OS's $10M+ agency runs on systematic, data-driven search optimization, and the SEO Module brings that operational rigor into the platform.

The SEO Module connects to third-party data providers (SerpAPI, DataForSEO), scrapes SERPs via Playwright when needed, tracks rankings over time, monitors competitors, generates content briefs from live SERP analysis, and publishes finished content through CMS connectors. All data is workspace-scoped and feeds into the audit and cost attribution systems.

**Key principle:** Every SEO action produces evidence. Every ranking change is tracked. Every content brief is derived from real SERP data.

---

## 2. SEO Layer Architecture

The SEO Module sits at **Layer 5 (Intelligence)** and **Layer 6 (Interface)** of the 7-layer Agent OS stack:

```
┌─────────────────────────────────────────┐
│  Layer 7: Gateway / BYOK Model Router   │
├─────────────────────────────────────────┤
│  Layer 6: Interface (Mission Control,   │
│           SEO Dashboard, Workflow Builder│
├─────────────────────────────────────────┤
│  Layer 5: Intelligence (SERP Analysis,  │
│           Content Briefs, Rank Tracking,│
│           Competitor Watch, Keyword R&D) │
├─────────────────────────────────────────┤
│  Layer 4: Memory (Notebook vault,       │
│           semantic search, backlinks)    │
├─────────────────────────────────────────┤
│  Layer 3: Orchestration (Workflows,     │
│           approvals, agent delegation)   │
├─────────────────────────────────────────┤
│  Layer 2: Execution (Agent runs,       │
│           tool calls, artifact provenance)│
├─────────────────────────────────────────┤
│  Layer 1: Persistence (SEO campaigns,   │
│           keywords, rankings, CMS posts) │
└─────────────────────────────────────────┘
```

**Integration points:**
- **Layer 1:** New tables (`seo_campaigns`, `seo_keywords`, `seo_rankings`, `seo_competitors`, `seo_content_briefs`, `cms_connections`, `cms_posts`)
- **Layer 2:** SEO tasks produce artifacts (briefs, reports, crawl results)
- **Layer 3:** SEO workflows orchestrate multi-step pipelines (audit → brief → draft → publish)
- **Layer 4:** Notebook vault is scanned for internal link suggestions; content briefs reference KB articles
- **Layer 6:** SEO Dashboard provides unified analytics view

---

## 3. Features

### 3.1 SERP Analysis

Live SERP data collection for any keyword across configured search engines and locations.

**Capabilities:**
- Query SERP for keyword + engine (Google, Bing) + location + language
- Extract: rankings, featured snippets, People Also Ask, related searches, top 10 URLs
- Cache results for 6 hours to minimize API costs
- Fallback chain: SerpAPI → DataForSEO → Playwright scrape

**Data retention:** SERP snapshots retained 90 days (configurable)

**Cost attribution:** Each SERP query attributed to workspace, campaign, and triggering run

---

### 3.2 Content Brief Generator

Automated analysis of top-ranking content to produce structured briefs for writers.

**Pipeline:**
1. Fetch top 10 results for target keyword
2. Extract: H1/H2/H3 structure, word count, readability score, authority signals (Domain Rating)
3. Extract: LSIs (latent semantic keywords), questions from PAA, content gaps
4. Analyze intent classification (informational, transactional, navigational, commercial)
5. Generate structured brief with recommended outline, word count target, and reference URLs

**Output format:** Markdown brief with YAML frontmatter; exportable to JSON

---

### 3.3 Rank Tracker

Historical position tracking with volatility alerts and share-of-voice metrics.

**Tracking:**
- Daily position snapshot per keyword × search engine × location
- Volatility calculation: standard deviation of positions over 30 days
- Alert triggers: position change > ±3, new entrant in top 3, competitor overtaking

**Share of Voice:**
- Calculated as: (sum of CTR estimates for tracked keywords) / (total available CTR for those keywords)
- CTR estimates derived from position using industry-standard curves

---

### 3.4 Competitor Watch

Monitor competitor domains and URLs for content velocity, rank changes, and strategic moves.

**Monitoring scope:**
- Tracked competitor list per campaign (max 25 competitors)
- Weekly digest: new pages detected, rank changes > ±5 positions, lost/gained featured snippets
- Content velocity: pages published per week (estimated from crawl frequency)
- Backlink signal integration (optional via third-party API)

---

### 3.5 Keyword Research

Discover, classify, and cluster keywords for campaign planning.

**Metrics:**
- Search volume (monthly, by country)
- Keyword difficulty (0–100, from provider or estimated)
- Intent classification: informational, navigational, transactional, commercial
- CPC (cost-per-click) for paid context

**Clustering:**
- Semantic similarity via embeddings (pgvector)
- Parent/child keyword relationships
- Export to campaign or content pipeline

---

### 3.6 Internal Link Suggester

Scan the Notebook vault to propose contextual internal links for new and existing content.

**Process:**
1. Generate embedding for target page content
2. Semantic search across all notes for related topics
3. Score matches by relevance and current link equity
4. Propose: anchor text, target URL, context snippet, confidence score
5. Bulk-apply approved suggestions; rejected suggestions stored for learning

---

### 3.7 SEO Audit Crawler

Technical SEO crawler with Lighthouse integration.

**Checks:**
- Page speed (Core Web Vitals: LCP, FID, CLS)
- Mobile-friendliness
- Schema markup validation (JSON-LD, Microdata)
- Broken links (404, 500, redirects)
- Canonical tags, hreflang, robots meta
- SSL/TLS configuration

**Output:** Prioritized fix list with severity (critical, high, medium, low) and estimated impact

**Scale:** Up to 10,000 URLs per crawl; configurable crawl depth and rate limit

---

### 3.8 CMS Connectors

Publish content directly to WordPress, Shopify, and Webflow.

**Supported platforms:**

| Platform | Auth | Endpoints | Features |
|---|---|---|---|
| WordPress | Application Password / JWT | REST API v2 | Posts, pages, media, categories, tags, Yoast/SEO metadata |
| Shopify | Admin API key | GraphQL Admin API | Blog articles, pages, metaobjects |
| Webflow | API token | CMS API | Collections, items, assets |

**Workflow:**
1. Draft created in Agent OS with SEO metadata
2. Preview rendered in Agent OS (CMS-agnostic preview)
3. Review via Two-Lane Verifier or human approval
4. Publish to CMS: draft first, then publish
5. Sync status back to Agent OS (published URL, CMS post ID, last modified)

---

### 3.9 Traffic Analytics

Connect Google Search Console and GA4 to correlate SEO actions with traffic outcomes.

**Google Search Console:**
- OAuth 2.0 connection (user grants access)
- Queries, impressions, clicks, CTR, position per page/query combination
- Date range: up to 16 months historical

**GA4:**
- OAuth 2.0 connection
- Sessions, users, bounce rate, conversions by landing page
- Correlation with ranking changes (same-date overlay charts)

**Dashboard:**
- Traffic vs. ranking correlation chart
- Organic clicks by keyword
- Top gaining/losing pages
- Date range and comparison period controls

---

### 3.10 White-Label SEO Reports

Professional, branded reports for client delivery.

**Report sections:**
1. Executive Summary (KPIs, highlights, actions taken)
2. Rankings (tables + charts, period-over-period)
3. Competitor Overview (position comparison, content velocity)
4. Technical Audit (issues + fixes applied)
5. Content Pipeline (briefs generated, articles published)
6. Traffic Analysis (GSC + GA4 correlations)

**Branding:**
- Workspace logo, colors, and custom CSS
- Cover page with client name and report period
- Footer: "Powered by Agent OS" (optional, removable in enterprise tier)

**Formats:** PDF (via headless browser or library), HTML (responsive, interactive charts)
**Delivery:** Download, email (via connected provider), scheduled generation

---

## 4. Data Model Additions

### 4.1 `seo_campaigns`

Groups keywords, competitors, and content briefs under a single SEO initiative.

```sql
CREATE TABLE seo_campaigns (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    target_domain   VARCHAR(500),
    target_location VARCHAR(100) DEFAULT 'us',
    target_language VARCHAR(10) DEFAULT 'en',
    status          VARCHAR(50) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'paused', 'archived')),
    serp_provider   VARCHAR(50) DEFAULT 'serpapi'
    CHECK (serp_provider IN ('serpapi', 'dataforseo', 'playwright', 'none')),
    config_json     JSONB DEFAULT '{}',
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_seo_campaigns_workspace ON seo_campaigns(workspace_id);
CREATE INDEX idx_seo_campaigns_status ON seo_campaigns(status);
```

### 4.2 `seo_keywords`

Keywords tracked within a campaign.

```sql
CREATE TABLE seo_keywords (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    campaign_id     UUID NOT NULL REFERENCES seo_campaigns(id) ON DELETE CASCADE,
    keyword         VARCHAR(500) NOT NULL,
    search_engine   VARCHAR(50) DEFAULT 'google'
    CHECK (search_engine IN ('google', 'bing')),
    location        VARCHAR(100) DEFAULT 'us',
    language        VARCHAR(10) DEFAULT 'en',
    search_volume   INTEGER,
    keyword_difficulty INTEGER,
    cpc             NUMERIC(10,2),
    intent          VARCHAR(50) DEFAULT 'unknown'
    CHECK (intent IN ('informational', 'navigational', 'transactional', 'commercial', 'unknown')),
    status          VARCHAR(50) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'paused', 'archived')),
    tags            TEXT[] DEFAULT '{}',
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (campaign_id, keyword, search_engine, location, language)
);

CREATE INDEX idx_seo_keywords_campaign ON seo_keywords(campaign_id);
CREATE INDEX idx_seo_keywords_workspace ON seo_keywords(workspace_id);
CREATE INDEX idx_seo_keywords_status ON seo_keywords(status);
CREATE INDEX idx_seo_keywords_intent ON seo_keywords(intent);
```

### 4.3 `seo_rankings`

Historical ranking snapshots.

```sql
CREATE TABLE seo_rankings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    campaign_id     UUID NOT NULL REFERENCES seo_campaigns(id) ON DELETE CASCADE,
    keyword_id      UUID NOT NULL REFERENCES seo_keywords(id) ON DELETE CASCADE,
    search_engine   VARCHAR(50) NOT NULL,
    position        INTEGER NOT NULL,
    url             TEXT,
    title           TEXT,
    snippet         TEXT,
    featured_snippet BOOLEAN DEFAULT FALSE,
    serp_features   TEXT[] DEFAULT '{}',
    check_date      DATE NOT NULL,
    check_time      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    data_source     VARCHAR(50) DEFAULT 'api'
    CHECK (data_source IN ('api', 'scrape', 'manual', 'import')),
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_seo_rankings_keyword ON seo_rankings(keyword_id);
CREATE INDEX idx_seo_rankings_campaign ON seo_rankings(campaign_id);
CREATE INDEX idx_seo_rankings_workspace ON seo_rankings(workspace_id);
CREATE INDEX idx_seo_rankings_date ON seo_rankings(check_date);
CREATE INDEX idx_seo_rankings_keyword_date ON seo_rankings(keyword_id, check_date);
```

### 4.4 `seo_competitors`

Competitor domains and URLs monitored per campaign.

```sql
CREATE TABLE seo_competitors (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    campaign_id     UUID NOT NULL REFERENCES seo_campaigns(id) ON DELETE CASCADE,
    domain          VARCHAR(500) NOT NULL,
    url             TEXT,
    name            VARCHAR(255),
    monitor_type    VARCHAR(50) DEFAULT 'domain'
    CHECK (monitor_type IN ('domain', 'url', 'page')),
    alert_threshold INTEGER DEFAULT 3,
    status          VARCHAR(50) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'paused', 'archived')),
    last_crawled_at TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (campaign_id, domain, monitor_type)
);

CREATE INDEX idx_seo_competitors_campaign ON seo_competitors(campaign_id);
CREATE INDEX idx_seo_competitors_workspace ON seo_competitors(workspace_id);
CREATE INDEX idx_seo_competitors_status ON seo_competitors(status);
```

### 4.5 `seo_content_briefs`

Generated content briefs from SERP analysis.

```sql
CREATE TABLE seo_content_briefs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    campaign_id     UUID REFERENCES seo_campaigns(id) ON DELETE SET NULL,
    keyword_id      UUID REFERENCES seo_keywords(id) ON DELETE SET NULL,
    title           VARCHAR(500) NOT NULL,
    target_keyword  VARCHAR(500) NOT NULL,
    search_intent   VARCHAR(50) DEFAULT 'unknown'
    CHECK (search_intent IN ('informational', 'navigational', 'transactional', 'commercial', 'unknown')),
    recommended_word_count INTEGER,
    outline_json    JSONB DEFAULT '[]',
    lsi_keywords    TEXT[] DEFAULT '{}',
    questions       TEXT[] DEFAULT '{}',
    authority_refs  JSONB DEFAULT '[]',
    top10_analysis  JSONB DEFAULT '{}',
    status          VARCHAR(50) NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'approved', 'in_progress', 'published', 'archived')),
    assigned_to     UUID REFERENCES users(id) ON DELETE SET NULL,
    artifact_id     UUID REFERENCES artifacts(id) ON DELETE SET NULL,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_seo_briefs_campaign ON seo_content_briefs(campaign_id);
CREATE INDEX idx_seo_briefs_workspace ON seo_content_briefs(workspace_id);
CREATE INDEX idx_seo_briefs_status ON seo_content_briefs(status);
CREATE INDEX idx_seo_briefs_keyword ON seo_content_briefs(keyword_id);
```

### 4.6 `cms_connections`

OAuth/API connections to external CMS platforms.

```sql
CREATE TABLE cms_connections (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    platform        VARCHAR(50) NOT NULL
    CHECK (platform IN ('wordpress', 'shopify', 'webflow')),
    display_name    VARCHAR(255) NOT NULL,
    base_url        TEXT NOT NULL,
    auth_type       VARCHAR(50) NOT NULL
    CHECK (auth_type IN ('api_key', 'oauth2', 'basic', 'app_password')),
    credentials_ref VARCHAR(500) NOT NULL,
    config_json     JSONB DEFAULT '{}',
    status          VARCHAR(50) NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'degraded', 'disconnected', 'error')),
    last_sync_at    TIMESTAMPTZ,
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (workspace_id, platform, base_url)
);

CREATE INDEX idx_cms_connections_workspace ON cms_connections(workspace_id);
CREATE INDEX idx_cms_connections_platform ON cms_connections(platform);
CREATE INDEX idx_cms_connections_status ON cms_connections(status);
```

### 4.7 `cms_posts`

Content published via CMS connectors.

```sql
CREATE TABLE cms_posts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id    UUID NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    connection_id   UUID NOT NULL REFERENCES cms_connections(id) ON DELETE CASCADE,
    campaign_id     UUID REFERENCES seo_campaigns(id) ON DELETE SET NULL,
    brief_id        UUID REFERENCES seo_content_briefs(id) ON DELETE SET NULL,
    cms_post_id     VARCHAR(255),
    cms_post_url    TEXT,
    title           VARCHAR(500) NOT NULL,
    content_ref     TEXT,
    status          VARCHAR(50) NOT NULL DEFAULT 'draft'
    CHECK (status IN ('draft', 'scheduled', 'published', 'unpublished', 'deleted', 'error')),
    seo_metadata    JSONB DEFAULT '{}',
    published_at    TIMESTAMPTZ,
    sync_status     VARCHAR(50) DEFAULT 'pending'
    CHECK (sync_status IN ('pending', 'synced', 'failed', 'conflict')),
    metadata_json   JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at      TIMESTAMPTZ
);

CREATE INDEX idx_cms_posts_connection ON cms_posts(connection_id);
CREATE INDEX idx_cms_posts_workspace ON cms_posts(workspace_id);
CREATE INDEX idx_cms_posts_status ON cms_posts(status);
CREATE INDEX idx_cms_posts_campaign ON cms_posts(campaign_id);
```

---

## 5. API Endpoints

### 5.1 Campaigns

#### GET `/seo/campaigns`
- **Auth:** Bearer
- **Query:** `?limit=20&cursor=&status=active`
- **Response:** Paginated SEO campaigns

#### POST `/seo/campaigns`
- **Auth:** Bearer
- **Request:**
```json
{
  "name": "Q3 Blog SEO",
  "description": "Blog content optimization campaign",
  "target_domain": "https://example.com",
  "target_location": "us",
  "target_language": "en",
  "serp_provider": "serpapi"
}
```

#### GET `/seo/campaigns/{campaign_id}`
- **Auth:** Bearer
- **Response:** Full campaign with keyword and competitor counts

#### PATCH `/seo/campaigns/{campaign_id}`
- **Auth:** Bearer

#### DELETE `/seo/campaigns/{campaign_id}`
- **Auth:** Bearer
- **Response:** `204` (soft delete)

---

### 5.2 Keywords

#### GET `/seo/campaigns/{campaign_id}/keywords`
- **Auth:** Bearer
- **Response:** Paginated keywords for campaign

#### POST `/seo/campaigns/{campaign_id}/keywords`
- **Auth:** Bearer
- **Request:**
```json
{
  "keyword": "agent operating system",
  "search_engine": "google",
  "location": "us",
  "language": "en",
  "tags": ["primary", "commercial"]
}
```

#### GET `/seo/keywords/{keyword_id}/rankings`
- **Auth:** Bearer
- **Query:** `?from=2026-07-01&to=2026-08-11`
- **Response:** Historical rankings array

#### DELETE `/seo/keywords/{keyword_id}`
- **Auth:** Bearer

---

### 5.3 SERP Analysis

#### POST `/seo/serp/query`
- **Auth:** Bearer
- **Request:**
```json
{
  "keyword": "agent operating system",
  "search_engine": "google",
  "location": "us",
  "language": "en",
  "cache": true
}
```
- **Response:** SERP snapshot with top 10, features, PAA

---

### 5.4 Content Briefs

#### POST `/seo/briefs/generate`
- **Auth:** Bearer
- **Request:**
```json
{
  "keyword_id": "uuid",
  "campaign_id": "uuid",
  "include_questions": true,
  "include_authority_refs": true
}
```
- **Response:** `202` with brief generation job ID

#### GET `/seo/briefs`
- **Auth:** Bearer
- **Response:** Paginated briefs

#### GET `/seo/briefs/{brief_id}`
- **Auth:** Bearer
- **Response:** Full brief with outline, LSIs, questions

#### PATCH `/seo/briefs/{brief_id}`
- **Auth:** Bearer

---

### 5.5 Competitors

#### GET `/seo/campaigns/{campaign_id}/competitors`
- **Auth:** Bearer

#### POST `/seo/campaigns/{campaign_id}/competitors`
- **Auth:** Bearer
- **Request:**
```json
{
  "domain": "competitor.com",
  "monitor_type": "domain",
  "alert_threshold": 3
}
```

#### GET `/seo/competitors/{competitor_id}/changes`
- **Auth:** Bearer
- **Response:** Recent changes digest

---

### 5.6 CMS Connections

#### GET `/seo/cms-connections`
- **Auth:** Bearer

#### POST `/seo/cms-connections`
- **Auth:** Bearer (owner/admin)
- **Request:**
```json
{
  "platform": "wordpress",
  "display_name": "Company Blog",
  "base_url": "https://blog.example.com",
  "auth_type": "app_password",
  "credentials": { "username": "admin", "password": "…" }
}
```

#### DELETE `/seo/cms-connections/{connection_id}`
- **Auth:** Bearer (owner/admin)

---

### 5.7 CMS Posts

#### POST `/seo/cms-connections/{connection_id}/posts`
- **Auth:** Bearer
- **Request:**
```json
{
  "title": "What is an Agent Operating System?",
  "content": "…markdown…",
  "status": "draft",
  "seo_metadata": {
    "meta_title": "…",
    "meta_description": "…",
    "focus_keyword": "agent operating system"
  }
}
```

#### GET `/seo/cms-posts`
- **Auth:** Bearer
- **Response:** Paginated posts with sync status

---

### 5.8 Reports

#### POST `/seo/reports/generate`
- **Auth:** Bearer
- **Request:**
```json
{
  "campaign_id": "uuid",
  "report_type": "weekly_rank",
  "format": "pdf",
  "date_range": { "from": "2026-07-01", "to": "2026-08-11" }
}
```

---

## 6. Workflows

### 6.1 SEO Content Pipeline

```
[Trigger: New brief approved]
    → [Crystal: Analyze brief and assign writer]
    → [Alex: Write draft from brief]
    → [Joe: Two-Lane Verifier review]
    → [Approval Gate: Human review]
    → [Elvis: Generate featured image]
    → [CMS Connector: Publish to WordPress]
    → [Notification: Report published]
```

### 6.2 Weekly Rank Report

```
[Cron: Every Monday 09:00]
    → [Fetch all active keyword rankings]
    → [Calculate volatility and SoV]
    → [Compare to previous week]
    → [Generate branded PDF report]
    → [Email to configured recipients]
    → [Store report artifact]
```

### 6.3 Competitor Alert Response

```
[Event: Competitor rank change detected]
    → [Crystal: Analyze impact on our keywords]
    → [Generate response brief]
    → [Approval Gate: Review response strategy]
    → [If approved: Create content task]
    → [Notify campaign owner]
```

---

## 7. Provider Integrations

| Provider | Type | Endpoints | Rate Limits | Cost Model |
|---|---|---|---|---|
| **SerpAPI** | SERP Data | REST API, JSON | 100 req/s (paid) | Per-query billing |
| **DataForSEO** | SERP Data | REST API, JSON | 2000 req/min | Per-task credits |
| **Playwright** | Scrape | Local browser | Throttled (configurable) | Compute cost only |
| **GSC API** | Traffic | OAuth 2.0 REST | 1000 req/day | Free |
| **GA4 API** | Traffic | OAuth 2.0, Data API | 120 req/min | Free |
| **WordPress REST** | CMS | REST API v2 | Configurable | Free (self-hosted) |
| **Shopify Admin** | CMS | GraphQL Admin | 40 req/s (burst) | Included in plan |
| **Webflow CMS** | CMS | REST API | 60 req/min | Included in plan |

**Credential management:** All API keys and OAuth tokens stored via `credentials_ref` (secret vault reference), never in plain text.

---

## 8. Security & Governance

- All SEO data is workspace-scoped; no cross-workspace campaign visibility
- SERP API keys stored as vault references in `cms_connections.credentials_ref`
- Crawler respects `robots.txt` and configurable rate limits (default: 1 req/s)
- Competitor monitoring limited to public data; no scraping behind paywalls
- All SEO actions emit audit events (campaign creation, keyword addition, publish action)
- GSC/GA4 OAuth scopes: read-only by default; explicit consent for write actions

---

*End of SEO Module Document*
