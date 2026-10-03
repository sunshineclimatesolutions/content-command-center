# Content Command Center (CCC)

A local-first, Windows-first, zero-new-spend media-production and social-distribution
command center for a small field-service business. It designates the space between
**finished DaVinci Resolve exports** and **confirmed public publication**: watched-folder
ingestion, a searchable local library grouped by content concept, platform-native
composer variants, human editorial approval, a four-week per-destination calendar,
honest publication status, and free native-scheduler or clean manual handoffs — with
optional official-API adapters added only after they are approved, free, and proven
end-to-end.

> **CURRENT STATUS: Stage 0 documentation only.** There is no application code in this
> repository. Nothing installs, runs, publishes, or connects to any account. Every
> planned command in these documents is marked **PLANNED**. See
> [Current status](#current-status) and [docs/ROADMAP.md](docs/ROADMAP.md).

---

## 1. Mission

Give a working HVAC owner-operator a dependable, private, offline-capable production
system that turns one planned, professionally edited video into a reviewed, scheduled
set of platform-specific publications — so content preparation happens in organized
weekly/monthly batches instead of daily repetitive upload work, while the owner's
product knowledge, measurements, customer privacy, and accounts stay in his control.
The product objective is **lower routine labor per finished content package**; the
long-term "10–15 minutes/day review" figure is a **target to measure against, never a
promise** (see [docs/PRODUCT_CHARTER.md](docs/PRODUCT_CHARTER.md)).

## 2. The product journey (planned)

1. **Plan from the existing SCS calendar** — pick the next theme, audience, owning
   landing page, evidence type, and one CTA *before* filming.
2. **Film modular content on the iPhone 16 Pro Max** — one long-form anchor, deliberate
   short hooks, instrument close-ups, B-roll, and privacy-safe field photos. Never stage
   Field Proof.
3. **Edit in existing DaVinci Resolve Studio** — reusable `ANCHOR_16x9`, `SHORT_9x16`,
   `FIELD_PROOF_9x16`, `SQUARE_OPTIONAL`, and `THUMBNAIL` templates. Professional editing
   stays in Resolve; CCC is not a video editor.
4. **Export to a watched Resolve folder** — CCC detects completed exports only after
   file stability, FFprobe validation, and Windows-lock retries; originals are never
   modified or deleted.
5. **Ingest safely into the local library** — SHA-256, duplicate detection, metadata,
   thumbnail, and a recoverable database transaction. Interrupted ingests resume.
6. **Group assets into a content concept** — master, shorts, stills, subtitle files,
   project reference, captions, and proof live under one stable concept ID.
7. **Compose platform variants** — one master description, independently editable
   platform drafts using verified campaign/UTM links imported read-only from the SCS
   registry, with explicit human approval per variant.
8. **Schedule four weeks per destination** — a calendar tracks each platform account
   separately: locally prepared → approved → native-scheduler handoff → scheduled on
   destination → provider-accepted → public publication verified → owner-reported
   manual → unknown/failed.
9. **Hand off or publish through the safest available route** — free native schedulers
   and copy/reveal manual packages work from day one; official API auto-publication is
   later, optional, and only after approvals and verified live tests.
10. **Measure** — time spent per finished package, per-destination status gaps, and
    rule-based improvements. Leads/bookings/revenue remain the primary business KPIs in
    the existing SCS scorecard; the app never invents them.

## 3. Audience and scope

| Dimension | Decision |
|---|---|
| Primary user | Owner-operator of Sunshine Climate Solutions LLC (SCS), residential HVAC, Spring Hill / Tampa Bay, FL |
| Immediate business goal | Residential customer acquisition; commercial/TAB content kept a **distinct engine** with distinct CTAs |
| Second workspace | Sparkling Standard Cleaning Co. — deliberately deferred, fully isolated workspace (Stage 6, separate permissions, media root, campaigns, accounts) |
| Platform | Windows-first local desktop; core functions work offline |
| Budget | **$0 in new spending** — no subscriptions, usage-billed APIs, hosting, domains, paid trials, hardware, or payment methods |
| Existing assets used | This Windows PC, existing DaVinci Resolve (owner-licensed Studio), existing iPhone 16 Pro Max, existing GitHub account, existing social accounts, genuinely free/open-source tools subject to verification |

**In scope:** planning aids, watched-folder ingest, local library, concept grouping,
composer and approval, per-destination calendar, native handoff packages, manual
publication workflow, read-only SCS campaign/UTM snapshot import, optional approved API
adapters, honest status tracking, backup/restore, workspace isolation.

**Out of scope (first releases):** video editing, website rebuild, paid services,
cloud hosting, scraping or credential sharing, CAPTCHA/rate-limit workarounds,
multi-tenant SaaS, automatic factual HVAC captions without approval, advanced AI
orchestration without measured benefit, universal API-publishing promises, anything
that deletes or mutates original media, "published" status based only on optimistic
provider responses.

**Non-negotiable invariants:** original files are immutable; every displayed number and
button corresponds to persisted reality or is clearly labeled a fixture; approvals are
human and explicit; publishing confirmation is independent per destination; the SCS
and Sparkling Standard repositories are read-only to this project; secrets never enter
git, logs, or reports; the app binds to loopback only; no live post is made without
separate authorization.

## 4. Realistic output example

From **one** professionally edited horizontal HVAC anchor filmed and cut in Resolve,
when the footage genuinely supports it:

- 1 horizontal master (`ANCHOR_16x9`) for YouTube,
- ~3 genuinely distinct vertical clips (`SHORT_9x16`) — e.g. problem hook, myth, tool
  or measurement — not three arbitrary 30-second chunks,
- 1–2 real field photographs,
- 1–2 thumbnail candidates (owner-approved),
- caption variants per destination with approved tracked links,
- individually tracked publication jobs per destination.

The SCS operating system (see [docs/SOURCE_EVIDENCE.md](docs/SOURCE_EVIDENCE.md)) caps
realistic weekly capacity at roughly 1 anchor, 3–4 vertical clips, 1 Field Proof
package, 2–3 GBP posts, ~3 Facebook posts, 1–2 Nextdoor posts and 1–2 LinkedIn posts
when commercially relevant. CCC must never manufacture filler to hit a quota.

## 5. Architecture (planned)

```text
 EXISTING SCS PLAN + APPROVED UTM REGISTRY (read-only snapshot)
                    │
 iPhone 16 Pro Max ─┤
 (originals, verified copy)
                    ▼
        LOCAL ARCHIVE + DAVINCI RESOLVE (existing Studio)
                    │  render/export
                    ▼
        WATCHED RESOLVE EXPORT FOLDER
                    │  stability → FFprobe → SHA-256 → thumbnail
                    ▼
   CONTENT COMMAND CENTER  [http://127.0.0.1 — local only]
   ├── FastAPI backend + SQLite + background jobs (PLANNED)
   ├── Local library / concept grouping / transcripts + subtitles
   ├── Composer + editorial approval + four-week per-destination calendar
   ├── PublisherAdapter contract
   │     ├── NATIVE_HANDOFF   → free native schedulers (Meta Business Suite,
   │     │                      YouTube Studio scheduling, TikTok Studio 15 min–10 days,
   │     │                      GBP posts with Schedule/Repeat, Pinterest ≤30 days)
   │     ├── MANUAL           → copy/reveal package + checklist + reminder
   │     └── API_PUBLIC       → optional, later, approved + audited official APIs only
   └── Proof / audit / backup
                    │
                    ▼
   PLATFORM-CONFIRMED PUBLIC URLS or OWNER-REPORTED MANUAL PUBLICATION
   (never inferred from a draft upload, scheduled item, or optimistic API response)
```

**Important truth:** a scheduler running on this PC cannot publish while the PC is off
or offline. Genuine native scheduling (platform-hosted) survives shutdown; local jobs do
not. Some platform APIs remain restricted to approved/audited apps, and some (for
example the current X API) require payment — those destinations stay manual under the
$0 policy (see [docs/PLATFORM_CAPABILITIES.md](docs/PLATFORM_CAPABILITIES.md)).

## 6. Proposed technology stack — PROPOSED / ADR REQUIRED

Nothing below is implemented or installed by this repository.

| Layer | Proposal | Status |
|---|---|---|
| Backend | Python 3.11+ **FastAPI** bound to `127.0.0.1`, background workers | PROPOSED / ADR REQUIRED. Local machine currently has Python **3.14.7**; exact version compatibility must be verified in Stage 1. |
| Database | **SQLite** (single file, WAL, migrations) | PROPOSED / ADR REQUIRED |
| File watching | `watchdog` + stability/lock/FFprobe checks | PROPOSED / ADR REQUIRED |
| Media probing/thumbnails | **FFmpeg / ffprobe CLI** (LGPL/GPL — see license notes) | PROPOSED / ADR REQUIRED. **Not currently detected on PATH**; Stage 1 must resolve with a free build after owner approval. |
| Frontend | React + Vite + TypeScript, desktop-optimized UI | PROPOSED / ADR REQUIRED |
| Editor | Existing **DaVinci Resolve** 19.0.0.69 (`Resolve.exe`) | Present on machine; Studio activation owner-confirmed, not independently verified |
| Packaging | Plain local process first; optional Tauri later | PROPOSED / ADR REQUIRED |

A materially simpler alternative (for example a single-process local app with minimal
frontend tooling) must be considered in `docs/ARCHITECTURE.md` and the Stage 1 ADR
before implementation. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and
[docs/DECISION_LOG.md](docs/DECISION_LOG.md).

## 7. Milestones and owner approval gates

| Stage | Scope | Gate |
|---|---|---|
| **Stage 0** | This documentation constitution, private repo, evidence | **CURRENT — stopped for architectural review** |
| Stage 1 | Local media proof: watched folder, safe ingest, SHA-256, SQLite library, import/relink | Owner approves Stage 1 scope after reviewing Stage 0 |
| Stage 2 | Production package: concepts, read-only SCS link/calendar snapshot, composer, approval, four-week calendar, native handoff packages | Owner review of Stage 1 evidence |
| Stage 3 | Edit-time reduction benchmark: Resolve-native workflow vs one OSS rough-cut and one optional local clipper on safe sample content | Measured benefit required before adoption |
| Stage 4 | Native batching and reliability: reminders, queue, missed-post handling, status reconciliation, backup/restore drill | Owner review |
| Stage 5 | **Optional** verified auto-publication: self-hosted Postiz vs TryPost spike, then separately approved official API integrations | Separate explicit permission required |
| Stage 6 | **Optional** analytics imports and isolated Sparkling Standard workspace | Only when SCS product is stable |

Never auto-run the roadmap. Full details: [docs/ROADMAP.md](docs/ROADMAP.md).

## 8. Documentation map

| Document | Purpose |
|---|---|
| [AGENTS.md](AGENTS.md) | Enforceable rules for every future coding session |
| [docs/PRODUCT_CHARTER.md](docs/PRODUCT_CHARTER.md) | Vision, priorities, requirement IDs, acceptance mapping |
| [docs/USER_WORKFLOWS.md](docs/USER_WORKFLOWS.md) | Exact user journeys, naming, folder layout, recovery |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Components, processes, boundaries, publisher adapter contract |
| [docs/DATA_MODEL.md](docs/DATA_MODEL.md) | Entities, relationships, lifecycles, migrations, backups |
| [docs/OPEN_SOURCE_EVALUATION.md](docs/OPEN_SOURCE_EVALUATION.md) | Dated OSS research with licenses and fit |
| [docs/PLATFORM_CAPABILITIES.md](docs/PLATFORM_CAPABILITIES.md) | Per-destination API/scheduler feasibility matrix |
| [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md) | Assets, threats, controls, required tests |
| [docs/NO_COST_POLICY.md](docs/NO_COST_POLICY.md) | $0 enforcement rules and available-resource inventory |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Stage scope, gates, deliverables, pass/fail criteria |
| [docs/ACCEPTANCE_TESTS.md](docs/ACCEPTANCE_TESTS.md) | Requirement → stage → test → evidence cross-reference |
| [docs/DECISION_LOG.md](docs/DECISION_LOG.md) | Decisions, alternatives, open questions |
| [docs/SOURCE_EVIDENCE.md](docs/SOURCE_EVIDENCE.md) | Dated provenance for SCS and external claims |
| [docs/STAGE_0_REVIEW_CHECKLIST.md](docs/STAGE_0_REVIEW_CHECKLIST.md) | Independent reviewer checklist for this stage |
| [LICENSE_DECISION.md](LICENSE_DECISION.md) | License decision is pending owner approval; no license assigned |

## 9. Development rules and definition of done

Every future session must start by reading [AGENTS.md](AGENTS.md) and the current
stage's documents, work on a `feature/stage-N-description` branch in **this** repository
only, add or update tests, run the focused and required suites, and report evidence in
the standard report format defined in AGENTS.md. A change is done only when it is
implemented, tested with observed results, security-reviewed for private data, and
honestly reported. No feature may rely on a paid service, a live account, or an
unapproved API.

## 10. Current status

- **Stage 0 — complete upon commit/push:** repository constitution documents, research
  ledger, and a zero-dependency documentation verifier.
- **Application code:** none. Implementation begins no earlier than an approved Stage 1.
- **External connections:** none. No social account is connected; no credential is
  stored; no post has been published.
- **Costs incurred:** $0 new spending by this project.
- **Known environment gaps:** FFmpeg/ffprobe not detected; Python 3.14.7 (proposal
  targets 3.11+); Resolve Studio activation owner-confirmed only; no D: drive exists
  on this machine (paths in examples are illustrative and configurable).
