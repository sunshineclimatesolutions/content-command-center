# Decision Log — Content Command Center

**Format:** ADR-lite. Status: PROPOSED / ACCEPTED / SUPERSEDED / OPEN. Every material
decision gets an entry with date, context, decision, alternatives, and consequences.

---

### ADR-001 — Separate repository, never inside SCS/Sparkling repos
- **Status:** ACCEPTED (2026-10-03, owner directive)
- **Context:** SCS website is a deployed static site; Sparkling Standard is a separate
  business. Mixing a local desktop application into either repo risks deployments and
  ownership confusion.
- **Decision:** CCC lives in its own private repository created under the currently
  authenticated GitHub account (`sunshineclimatesolutions` namespace), used as a user
  account/repo owner, not as either business website repo.
- **Consequences:** no shared tooling or deployments; SCS/Sparkling stay read-only.

### ADR-002 — Local-first, loopback-only architecture
- **Status:** ACCEPTED (directive)
- **Decision:** Windows desktop app bound to `127.0.0.1`, SQLite, local files; no cloud
  dependency, no public server, no tunnel.
- **Alternatives rejected:** hosted web app (cost, privacy, PC-off caveat still exists
  for local media), cloud object storage (cost + privacy).
- **Consequences:** some future API publishing may need a reviewed media-serving plan if
  a platform requires publicly fetchable media (see ADR-003/Stage 5).

### ADR-003 — Native scheduling and manual handoff are the primary publishing routes
- **Status:** ACCEPTED (directive + verified platform matrix)
- **Decision:** Ship Facebook/Instagram/YouTube/TikTok/GBP/Pinterest/Nextdoor support via
  free native schedulers and clean manual packages first. Official API auto-publication
  is optional, per-destination, and only after approvals and live verification.
- **Evidence:** `docs/PLATFORM_CAPABILITIES.md` (audits, private-only restrictions,
  approval gates).
- **Consequences:** MVP is useful with zero developer approvals; no universal API
  promise; PC-off allows native schedules to run while local jobs do not.

### ADR-004 — SCS campaign/UTM data is imported read-only as a versioned snapshot
- **Status:** ACCEPTED (directive)
- **Decision:** Import generated CSV/JSON from `src/config/marketing-links.ts` outputs
  with source commit SHA + timestamp; exclude `pending` links from approved defaults;
  never generate or edit UTM parameters in CCC.
- **Evidence:** SCS registry structure at commit `0a38fec0…` (`MarketingLink` type,
  `pending` flag).
- **Consequences:** freshness warnings required; no duplicate attribution.

### ADR-005 — Proposed stack (FastAPI + React/Vite/TS + SQLite + watchdog + FFmpeg)
- **Status:** OPEN — ADR REQUIRED before Stage 1A implementation. Python 3.14
  dependency metadata was validated in ADR-023; the stack/process choice remains open.
- **Context:** Machine has Python 3.14.7, Node 24.19; FFmpeg not installed; directive
  proposes Python 3.11+ FastAPI etc.
- **Decision pending:** verify Python version compatibility; decide single-process MVP
  vs separate worker; decide whether the UI is Vite React or a simpler server-rendered
  approach for lower deployment friction on Windows.
- **Constraints:** no paid tooling; offline core; Windows path/lock handling.

### ADR-006 — Project license undecided; no license assigned
- **Status:** ACCEPTED (directive)
- **Decision:** Do not auto-assign an OSS license. Document third-party obligations
  separately (`LICENSE_DECISION.md`). Owner decides later.

### ADR-007 — Reuse existing OSS for publishing only after a Stage 5 spike; max one alternative
- **Status:** PROPOSED (directive)
- **Context:** Postiz (AGPL-3.0) requires PostgreSQL + Redis + Temporal and per-platform
  developer apps; TryPost (AGPL-3.0) claims 12 native platforms; Mixpost Lite is a
  feature-limited MIT core.
- **Decision:** Evaluate self-hosted Postiz as primary and TryPost as the single
  alternative in an isolated Stage 5 spike; do not install multiple schedulers; never
  assume self-hosting bypasses platform approvals.
- **Consequences:** resource/license measurement required; native routes remain.

### ADR-008 — No Docker/self-hosted services in the baseline
- **Status:** ACCEPTED (Stage 0–4)
- **Decision:** Keep the baseline dependency-light; containers are confined to an
  isolated Stage 5 experiment if that stage opens.

### ADR-009 — FFmpeg/ffprobe is a required-but-missing dependency
- **Status:** OPEN — distribution, license, and checksum procedure finalized in ADR-024;
  installation still requires owner authorization
- **Context:** Not detected on PATH on 2026-10-03. FFmpeg is LGPL-2.1+ (GPL parts if
  enabled); no other licensing available.
- **Decision needed (Stage 1A):** owner-approved free build source, install location,
  license compliance, and pinning; probe must run as a subprocess with validated
  arguments.

### ADR-010 — Meta destinations use native scheduling first
- **Status:** ACCEPTED
- **Context:** IG publishing via API needs professional account + permissions + often a
  public media URL or Facebook Login resumable upload; Page Publishing Authorization may
  apply; App Review for Advanced access.
- **Decision:** Compose + native Business Suite scheduling first; evaluate API adapters
  only in Stage 5 with real approvals.

### ADR-011 — X is manual-only under the $0 policy
- **Status:** ACCEPTED (verified pricing)
- **Context:** X API moved to pay-per-use; no free tier for new developers (2026).
- **Decision:** Prepare manual packages; do not add X API credentials.

### ADR-012 — TikTok native scheduling window treated as 15 min–10 days
- **Status:** ACCEPTED
- **Decision:** Do not claim longer native windows; third-party longer windows rely on
  their own servers and the Content Posting API audit gate (unaudited = private-only).

### ADR-013 — Sparkling Standard workspace deferred
- **Status:** ACCEPTED (directive)
- **Decision:** Do not build multi-workspace until SCS is stable; design schema
  workspace-scoped (ADR-002/`docs/DATA_MODEL.md`) so Stage 6 is additive, not a rewrite.

### ADR-014 — SQLite as the durable store with explicit migrations and backups
- **Status:** ACCEPTED
- **Decision:** Single-file SQLite with WAL, ordered migrations, consistent backups,
  restore drill at Stage 4.

### ADR-015 — Seed repo into account `sunshineclimatesolutions`, repo name `content-command-center`
- **Status:** ACCEPTED (2026-10-03)
- **Context:** `gh auth status` shows active account `sunshineclimatesolutions`; the
  directive requires the currently authenticated account and forbids assuming an org.
  Both `content-command-center` and `content-command-center-app` were verified unused;
  the preferred name was free.
- **Decision:** Create `sunshineclimatesolutions/content-command-center` as a **private**
  repository.
- **Consequences:** same account also owns the SCS website repo; isolation is enforced
  by repository boundaries and procedural gates (no cross-push ever).

### ADR-016 — Branch protection/rulesets unavailable for this private repo; procedural gates only
- **Status:** SUPERSEDED (2026-10-03, Stage 0.5). The repository was deliberately made
  **public** by the owner; rulesets and branch protection are available on public
  repositories at $0 (verified: rulesets endpoint returns `[]` with HTTP 200; protection
  endpoint returns 404 "Branch not protected"). See ADR-017/ADR-018. Historical text
  preserved below.
- **Context (historical):** `gh api repos/sunshineclimatesolutions/content-command-center/rulesets` and
  `.../branches/main/protection` both returned HTTP 403:
  *"Upgrade to GitHub Pro or make this repository public to enable this feature."*
- **Decision (historical):** Do **not** upgrade billing or make the repository public. Enforce review
  gates procedurally: `main` is documentation-only until owner approval; all future work
  goes to `feature/stage-N-description` branches with draft PRs; merges require explicit
  owner approval (see `AGENTS.md` §10). No false claim of technical enforcement.
- **Consequences:** protection depended on discipline and review, not GitHub settings.

### ADR-017 — Repository deliberately made public by the owner
- **Status:** ACCEPTED (owner action; observed 2026-10-03, Stage 0.5)
- **Context:** Created private on 2026-10-03 (ADR-015); the owner changed visibility to
  public for independent architectural review.
- **Decision:** Reflect the public status in docs; preserve the private-creation history;
  apply redactions (personal email, inactive account names, unnecessary machine
  identifiers) without rewriting Git history; state clearly that public visibility does
  not grant a license (`LICENSE_DECISION.md`).
- **Residual:** the commit-author email remains visible in Git history; rewriting history
  is not authorized. Future commits may use a neutral identity only with owner approval.
- **Consequences:** all future contributions must assume world-readable content.

### ADR-018 — Recommended `main` protection for the public repository ($0)
- **Status:** PROPOSED — do not apply without owner approval
- **Context:** Public repositories get rulesets/branch protection on GitHub Free; the
  current state is unprotected (`[]` rulesets; 404 "Branch not protected").
- **Recommended ruleset targeting `main`:** require a pull request before merging with
  **0 required approvals** (single-owner workflow, self-merge allowed); dismiss stale
  approvals off; require linear history optional; **block force pushes**; **restrict
  deletions**; no required status checks (no CI yet); no mandatory external reviewers.
- **Consequences:** protects history from force-push/deletion while keeping the owner
  able to merge their own draft PRs.

### ADR-019 — Verified-copy-only ingestion; hard links removed
- **Status:** ACCEPTED (Stage 0.5 directive)
- **Decision:** The initial implementation never hard-links. Copy → source-unchanged
  check → destination SHA-256 verification → single recoverable transaction. Optional
  explicit completion sentinel documented; quiet-period detection acknowledged as
  heuristic.
- **Consequences:** extra disk usage and copy time accepted for safety and clarity.

### ADR-020 — Local API browser-threat controls
- **Status:** ACCEPTED (Stage 0.5 directive)
- **Decision:** `Host` allowlist, `Origin`/`Referer` validation, CORS disabled by
  default, per-session CSRF token header on mutations, ID-based file access confined to
  authorized roots; fail closed. Requirements CCC-REQ-037/038; tests in Stage 1A.
- **Consequences:** the UI must send the token; no cross-origin integrations.

### ADR-021 — `concept_asset` is the authoritative grouping relationship
- **Status:** ACCEPTED (Stage 0.5 directive)
- **Decision:** Remove `asset.concept_id`; assets link to concepts only through the
  many-to-many `concept_asset` join. `asset_variant` models derivatives; reuse is
  intentional linking. Dedup is library identity only and must never suppress a
  legitimate publication; overlapping same-destination duplicates warn and require
  confirmation.
- **Consequences:** simpler, unambiguous model; cross-concept reuse is first-class.

### ADR-022 — Stage 1 split into 1A (ingest core) and 1B (library surface)
- **Status:** ACCEPTED (Stage 0.5 directive)
- **Decision:** 1A proves safe ingest headlessly; 1B adds thumbnails, search, concept
  grouping, manual import, relink, and restart persistence. Separate gates; no
  publishing in either.
- **Consequences:** smaller reviewable increments; UI work waits for a proven core.

### ADR-023 — Dependency validation for Python 3.14; watchdog deferred
- **Status:** ACCEPTED (Stage 0.5, verified 2026-10-03)
- **Context:** PyPI metadata: FastAPI 0.142.2, Uvicorn 0.54.0, Pydantic 2.13.5 (+cp314
  pydantic-core), SQLAlchemy 2.1.3 (cp314 wheels), HTTPX 0.28.1, pytest 9.1.1, Alembic
  1.20.0 compatible with Python 3.14; **watchdog 6.0.0 has no cp314 Windows wheel**.
- **Decision:** Use a standard-library polling scanner in Stage 1A; defer watchdog;
  prefer plain `uvicorn` over `[standard]`; pin exact versions in Stage 1A.
- **Consequences:** one fewer dependency; re-evaluate watchdog when wheels exist.

### ADR-024 — FFmpeg acquisition via pinned LGPL shared build with checksum verification
- **Status:** PROPOSED — installation requires owner authorization
- **Decision:** Download the pinned BtbN `n9.0` win64 **LGPL shared** zip plus
  `checksums.sha256`; verify SHA-256; extract to `%CC_ROOT%\_app\tools\ffmpeg\<pin>\`;
  configure absolute paths; never modify PATH; record URL/tag/hash/date in
  `docs/SOURCE_EVIDENCE.md`.
- **Consequences:** minimal license obligations; no GPL components; checksums detect
  transfer corruption (upstream compromise remains a residual risk).

### ADR-025 — SCS reference advances to `87da9a2`; no lead-attribution duplication
- **Status:** ACCEPTED (Stage 0.5 directive)
- **Context:** SCS `main` advanced from `0a38fec0` to
  `87da9a2887189552c8872339738f526d3132f883` ("feat: consent-gated first/latest-touch
  lead attribution (#2)"). Changed files: `AGENTS.md`,
  `docs/marketing/CONTENT-OPERATING-SYSTEM.md`, `docs/GTM-GA4-SETUP.md`; the other nine
  Stage 0 reference files are byte-identical.
- **Decision:** Preserve the Stage 0 snapshot (`0a38fec0`) as historical evidence and
  acknowledge `87da9a2` as the current reference. CCC does not duplicate lead capture or
  attribution (CCC-REQ-036); leads stay in SCS systems.
- **Consequences:** SCS freshness checks in Stage 2 must compare against `87da9a2` or
  later.

### Known documented conflicts (see also `docs/SOURCE_EVIDENCE.md`)
- Facebook `scheduled_publish_time`: official pages state 30 days vs 75 days — exact
  value UNKNOWN pending live verification.
- Instagram daily publish limit: official pages state 100 vs 50 — verify via
  `content_publishing_limit`.
- Old research claimed "Postiz needs PostgreSQL/Redis" without mentioning Temporal;
  the current official configuration reference requires Temporal since v2.12.0. The
  master directive wins; old research corrected.
