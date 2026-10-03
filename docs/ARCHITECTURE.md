# Architecture — Content Command Center

**Status:** Stage 0 proposal. Every component below is **PROPOSED / ADR REQUIRED** and
unimplemented. Nothing here claims current functionality.

---

## 1. Architectural principles

1. **Local-first:** the core system runs on this Windows PC with no cloud dependency;
   loopback interface only (`127.0.0.1`).
2. **Originals are sacred:** ingest uses verified copies only; hard links are not part
   of the implementation; sources are never mutated.
3. **Honest state:** durable SQLite rows are the single source of UI truth; every status
   has evidence rules.
4. **Separation of concerns:** ingest, library, composer, publishing adapters, and UI are
   distinct modules with explicit interfaces.
5. **Adapters over integrations:** publishing is behind a replacement-safe contract so
   native handoff, manual packages, and future approved APIs coexist.
6. **Idempotent, resumable jobs:** no blind retries on ambiguous outcomes.
7. **Windows-real:** path length, file locks, permissions, drive letters, Unicode, and
   drive-space limits are first-class.

## 2. System context

```mermaid
flowchart LR
  subgraph EXT[External read-only sources]
    SCS[SCS repo: campaign/UTM registry,\n90-day calendar, rules]
  end
  subgraph PROD[Production - owner tools]
    IPH[iPhone 16 Pro Max originals]
    RSV[DaVinci Resolve Studio\nexisting license]
  end
  subgraph CCC[Content Command Center - localhost only]
    WATCH[Watched export folder + stability/FFprobe]
    ING[Ingest service\nSHA-256, metadata, thumbnails]
    DB[(SQLite\ndurable state)]
    LIB[Library + concept grouping]
    CMP[Composer + approvals]
    CAL[Four-week per-destination calendar]
    ADP[PublisherAdapter]
    JOBS[Background jobs + reconciliation]
    UI[Desktop UI - 127.0.0.1]
  end
  NAT[Native schedulers\nMeta / YouTube / TikTok / GBP / Pinterest]
  MAN[Manual handoff pages\ncopy/reveal checklist]
  API[Optional approved official APIs\nlater stage]
  PROOF[Public URLs / owner-reported proof]

  SCS -. read-only snapshot .-> DB
  IPH --> RSV --> WATCH --> ING --> DB
  DB --> LIB --> CMP --> CAL --> ADP
  JOBS --- ADP
  ADP --> NAT --> PROOF
  ADP --> MAN --> PROOF
  ADP -. optional .-> API --> PROOF
  UI <--> DB
  UI <--> CMP
```

## 3. Process boundaries (proposed)

| Process | Responsibility | Trust notes |
|---|---|---|
| API/UI server (FastAPI) | HTTP API + static UI on `127.0.0.1` | No remote bind; no public exposure |
| Watcher/ingest worker | Polling scan, quiet-period checks, FFprobe validation, verified copy, source-unchanged check, destination checksum, thumbnails | Never publishes; writes only to library root + DB; no hard links |
| Job runner | Durable local jobs, retries, reconciliation, reminders | Idempotency keys; no blind retry |
| Future publisher adapters | Native handoff packages, manual packages, approved APIs | Least privilege; per-destination isolation |

A single-process MVP option (one process for API + background tasks) is explicitly on
the table to reduce Windows deployment friction; the ADR must choose before Stage 1
implementation. See `docs/DECISION_LOG.md` ADR-005.

## 4. Proposed stack and Windows constraints

- Python 3.11+ **FastAPI** bound to `127.0.0.1` — PROPOSED. The audit found Python
  **3.14.7** installed; compatibility must be verified in Stage 1A rather than assumed.
- **SQLite** in `%CC_ROOT%\_app\db\content.sqlite` with WAL + explicit migrations.
- A **standard-library polling scanner** for non-recursive folder observation.
  `watchdog` is **deferred**: version 6.0.0 had no CPython 3.14 Windows wheel at
  validation time (ADR-023). Required stability re-scans happen regardless of event
  notifications.
- **FFmpeg/ffprobe CLI** — PROPOSED; **not currently detected on PATH** on this
  machine. Stage 1A requires owner-approved download of a pinned LGPL shared build with
  published-checksum verification, installed under `%CC_ROOT%\_app\tools\`, without
  modifying system PATH. Full procedure: [docs/ENVIRONMENT.md](ENVIRONMENT.md).
- React + Vite + TypeScript UI — PROPOSED.
- Existing Resolve Studio (19.0.0.69) — no scripting dependency required for MVP; a
  watched folder is the integration boundary.

Windows constraints to design for: MAX_PATH/path-length handling, file locking during
render, drive-letter changes, Unicode filenames, antivirus interference with rapid file
writes, and the absence of a guaranteed `D:` drive.

## 5. Data and storage strategy

- Durable metadata lives only in SQLite; the filesystem holds media and manifests.
- Library root is configurable per workspace; SCS first, Sparkling Standard later in a
  separate root with separate permissions.
- No hosting, buckets, or cloud storage in the baseline. If a future approved API needs
  a publicly fetchable media URL, that is a separate design review (limited HTTPS
  staging), never exposure of the whole archive.
- Backups: scheduled consistent SQLite backup + manifests/metadata export to existing
  storage. A true 3-2-1 strategy needs another independent device/location; if none
  exists it remains an **unresolved gap**, not an implied capability.

## 6. UI module map (proposed)

| Module | Purpose |
|---|---|
| Dashboard | Upcoming posts, unscheduled assets, failed publications, connection status, gaps |
| Library | Assets, concepts, filters/search, previews, metadata, relink |
| Composer | Master description → per-platform variants, validation, approval |
| Calendar | Month/week views, per-account coverage, reschedule, status visualization |
| Campaigns | Series/campaign groups, objectives, approved link snapshot status |
| Analytics (later) | Imported platform metrics + links to SCS reporting; never fabricates business outcomes |
| Accounts | Workspace connections, status honesty, permissions, health |
| Settings | Watched folders, storage roots, templates, notifications, security |
| Time & audit | Time per package, audit events, ingest/backup runs |

## 7. Publishing architecture

### 7.1 PublisherAdapter contract (replacement-safe)

```text
PublisherAdapter
  capabilities(account) -> { media_types, max_duration, caption_limit,
                             thumbnails, links, scheduling_window, verification }
  validate(draft, asset) -> [errors, warnings]
  prepare(draft) -> handoff_package | payload
  schedule(mode, when) -> job      # only when user selects that route
  reconcile(job) -> status
  cancel(job) -> status
```

Modes:

- `NATIVE_HANDOFF` — open the documented official destination page with the correct
  export/caption/link surfaced for human final action; record owner confirmation.
- `MANUAL` — produce the complete publication package + checklist + reminder.
- `API_PUBLIC` — only for separately approved, audited, zero-cost official APIs; must
  have idempotency, reconciliation, and verified-publication evidence rules.

No mode may share credentials, cookies, or sessions across workspaces; no mode may use
password login, scraping, or browser automation against platform terms.

### 7.2 Status model

Editorial approval and publication state are separate:

- Concept editorial: `IDEA → SCRIPTED → FILMED → EDITED → IMPORTED →
  READY_FOR_REVIEW → APPROVED → SCHEDULED → PUBLISHED` (concept-level, human).
- Per-destination publication: `DRAFT → PREPARED → APPROVED → EXPORTED →
  NATIVE_SCHEDULED | API_SCHEDULED | MANUAL_PENDING → SUBMITTING →
  PLATFORM_CONFIRMED | OWNER_REPORTED_MANUAL | FAILED | UNKNOWN | CANCELLED`.

Rules: `PLATFORM_CONFIRMED` requires verified public evidence; timeout → `UNKNOWN` with
reconciliation before retry; a parent concept is never fully published while any
selected destination is incomplete.

Deduplication is a **library-identity** concern, not a publishing-suppression rule. An
`asset` is one physical file identified by content hash; an `asset_variant` is a
derivative of an asset; linking an existing asset to another concept is intentional
reuse. The same approved variant may be published to multiple destinations and at
multiple times; each publication draft carries its own destination/time and idempotency
scope. Only an overlapping same-destination duplicate triggers a warning that requires
explicit owner override.

## 8. Publishing destination strategy (summary)

Full dated matrix in `docs/PLATFORM_CAPABILITIES.md`. Baseline:

- Native scheduling/handoff for Facebook, Instagram, YouTube, TikTok, Google Business
  Profile, Pinterest, Nextdoor (Share Plugin).
- Manual packages for X (API is pay-per-use as of 2026), Yelp, Rumble/Locals, and any
  destination without a verified zero-cost route.
- Optional API adapters only after Stage 5-style approval, with the free routes kept
  permanently available.

## 9. Security architecture baseline

- Loopback-only bind; no remote authentication surface initially.
- **Local browser-threat controls (mandatory):**
  - `Host` header allowlist: only `127.0.0.1:<port>` / `localhost:<port>` accepted; all
    others rejected (DNS-rebinding defense).
  - `Origin`/`Referer` validation on state-changing requests against the loopback UI
    origin; missing or foreign origin is rejected.
  - CORS disabled by default (no cross-origin requests); never `*`, never credentials
    with wildcard origins.
  - CSRF protection: every mutating endpoint requires a per-session token in a custom
    header, issued at launch to the local UI; missing/invalid token means refusal.
  - Local application authorization where needed: per-install/per-session token; no
    default credentials; token never logged.
- **File-access confinement:** endpoints address assets by catalog ID; any path input is
  canonicalized and must resolve inside configured roots; traversal, UNC/device paths,
  and reparse points are rejected. No endpoint exposes arbitrary file read/write.
- Secrets (future) via Windows Credential Manager/DPAPI; never in the DB in plaintext,
  logs, fixtures, or git.
- Least-privilege scopes per destination; per-workspace isolation.
- Audit events for approvals, handoffs, status changes, imports, backups, and any
  external send.
- Fail closed on missing/unknown configuration.

## 10. Decisions vs provisional

| Item | Classification |
|---|---|
| Local-first + loopback + SQLite + watched folder | Decision (this charter/directive) |
| Verified-copy-only ingestion; no hard links | Decision (Stage 0.5, ADR-019) |
| Local API `Host`/`Origin`/CSRF/path confinement | Decision (Stage 0.5, ADR-020) |
| `concept_asset` many-to-many as the authoritative grouping relationship | Decision (Stage 0.5, ADR-021) |
| PublisherAdapter contract shape | Decision (provisional; ADR before implementation) |
| FastAPI + React/Vite + SQLite + stdlib polling scanner + FFmpeg CLI | Proposal requiring ADR (see `docs/DECISION_LOG.md`; watchdog deferred, ADR-023) |
| Single-process MVP vs multi-process | Open — ADR required |
| Optional Tauri packaging | Provisional future |
| Postiz/TryPost/Mixpost reuse | Deferred to Stage 5 evaluation |
| Any Docker/self-hosted service | Deferred; resource and license review required |
