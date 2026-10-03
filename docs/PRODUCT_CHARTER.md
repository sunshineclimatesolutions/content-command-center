# Product Charter — Content Command Center

**Status:** Stage 0.5 (corrective documentation pass) · **Owner:** Aaron Thomas · **Issued:** 2026-10-03

This charter is the source of truth for what Content Command Center (CCC) is, what it
must do, and how change is controlled. Implementation status is always tracked honestly
in `README.md` and `docs/ROADMAP.md`, never here.

---

## 1. Vision

A private, local-first Windows application that turns each professionally edited
DaVinci Resolve video into a reviewed, scheduled, per-platform publication set with
minimal repetitive work — while preserving customer privacy, factual honesty, original
media, and the $0 new-spend constraint. CCC sits between production (Resolve) and
distribution (platforms). It is deliberately **not** a video editor, a website, a
scraper, a cloud SaaS, or a Hootsuite clone.

## 2. Objective vs target

- **Objective (measurable, in scope):** reduce recurring routine labor per finished
  content package — measured as recorded time spent in prepare/review/schedule/handoff
  per published package — through batching, reuse, safe automation, and native
  scheduling, compared against the owner's own baseline.
- **Target (aspirational, not a promise):** progressively approach a steady-state
  review workload of 10–15 minutes/day, dominated by comment/lead response and
  exception handling rather than repetitive production. This number is a benchmark, not
  a deliverable, and never justifies reducing lead-response quality or factual review.

## 3. Primary users and workspaces

| Workspace | Status | Notes |
|---|---|---|
| Sunshine Climate Solutions (SCS) | Primary, first releases | Residential acquisition first; separate commercial/TAB engine language and CTAs |
| Sparkling Standard Cleaning Co. | Deferred to Stage 6 | Fully isolated: media root, permissions, branding, campaigns, connections, calendar |

## 4. Requirement IDs

Stable IDs are used by `docs/ROADMAP.md`, `docs/ACCEPTANCE_TESTS.md`, and the decision
log. IDs are never renumbered; withdrawn requirements are marked withdrawn.

### Product and workflow

| ID | Requirement |
|---|---|
| CCC-REQ-001 | The product journey (plan → film → Resolve → watched export → ingest → library → composer → approval → calendar → handoff/publish → confirmed status) exists end-to-end without leaving originals behind. |
| CCC-REQ-002 | One content concept groups a master, vertical variants, stills, thumbnails, subtitles, captions, project reference, and publication proof under one stable ID. |
| CCC-REQ-003 | The library is searchable/filterable locally and remains usable offline. |
| CCC-REQ-004 | Composer creates independently editable platform variants from an owner-approved master description. |
| CCC-REQ-005 | Every publication variant requires explicit human approval before scheduling or handoff. |
| CCC-REQ-006 | A four-week, per-destination calendar tracks each account separately with the lifecycle states in `docs/DATA_MODEL.md`. |
| CCC-REQ-007 | Native scheduler handoff and manual packages are first-class, always-available publication routes. |
| CCC-REQ-008 | Official API auto-publication is optional, per-destination, verified, and separately approved. |
| CCC-REQ-009 | The system records honest, independent status per destination and never equates draft/private/scheduled with publicly published. |
| CCC-REQ-010 | The system tracks time spent per finished content package for the objective in §2. |

### Media safety

| ID | Requirement |
|---|---|
| CCC-REQ-011 | Original media and Resolve exports are never modified, renamed, moved, or deleted by CCC. Hard links are not used for ingestion. |
| CCC-REQ-012 | Ingestion uses verified copying: a configurable quiet period (size+mtime unchanged across the full period), FFprobe validation, Windows-lock recovery, a source-unchanged-during-copy check, destination SHA-256 verification, and resumable/transaction-safe recovery. |
| CCC-REQ-013 | SHA-256 content hashing and deduplication prevent duplicate library imports; deduplication never suppresses a legitimate publication to a different destination or time, which requires only a warning plus explicit confirmation. |
| CCC-REQ-014 | Folder watching is non-recursive by default; paths are validated; symlink/junction traversal is refused. |
| CCC-REQ-015 | Corrupted, huge, locked, HDR/rotated, and Unicode-path media fail cleanly with visible error states. |
| CCC-REQ-016 | The app warns on low disk space and never silently risks data loss. |

### Business integration

| ID | Requirement |
|---|---|
| CCC-REQ-017 | SCS campaign/UTM links are imported only as a read-only, versioned snapshot with source commit SHA and freshness warning. |
| CCC-REQ-018 | Pending or unverified SCS links are never offered as approved publishing defaults. |
| CCC-REQ-019 | Residential and commercial/TAB content use distinct campaign mappings, landings, and CTAs. |
| CCC-REQ-020 | The fundraising `/support/` layer stays segregated from customer-acquisition variants. |
| CCC-REQ-021 | CCC never writes to, deploys, or changes the SCS or Sparkling Standard repositories. |
| CCC-REQ-022 | CCC never creates duplicate GA4/GTM events or changes analytics definitions. |

### Security and privacy

| ID | Requirement |
|---|---|
| CCC-REQ-023 | The application binds to loopback only and exposes no public server or tunnel. |
| CCC-REQ-024 | Secrets are stored via the OS credential store/DPAPI and never in git, logs, reports, or fixtures. |
| CCC-REQ-025 | Authorization/state checks fail closed; client-supplied state never grants permissions. |
| CCC-REQ-026 | Customer-identifying media and private notes are never exported, logged, or published without recorded permission. |
| CCC-REQ-027 | Media sent to any external destination is an explicit, reviewed action by the owner. |

### Cost and licensing

| ID | Requirement |
|---|---|
| CCC-REQ-028 | Zero new spending: no paid service, subscription, trial, API, hosting, domain, hardware, or payment-method requirement. |
| CCC-REQ-029 | Third-party licenses are inventoried with obligations (notably AGPL/GPL/LGPL) before code reuse or distribution. |
| CCC-REQ-030 | The project's own license remains undecided until owner approval (`LICENSE_DECISION.md`); public repository visibility does not grant any reuse license. |

### Engineering integrity

| ID | Requirement |
|---|---|
| CCC-REQ-031 | No fictitious UI: every displayed value maps to persisted reality or is labeled a fixture. |
| CCC-REQ-032 | No fake integrations: statuses reflect actual implementation and verification. |
| CCC-REQ-033 | Every behavioral change has tests; failures are reported with real observed output. |
| CCC-REQ-034 | Local scheduling limits are visible in the UI and docs (PC off ⇒ no local job runs). |
| CCC-REQ-035 | Workspace isolation prevents cross-business media, campaign, and credential exposure. |

### Local API and browser safety

| ID | Requirement |
|---|---|
| CCC-REQ-036 | CCC does not duplicate SCS lead capture or campaign attribution. Leads, consent records, and first/latest-touch attribution remain in their existing SCS systems; CCC imports campaign links read-only and records only publication proof. |
| CCC-REQ-037 | The local API validates `Host` against the loopback allowlist, validates `Origin`/`Referer` on state-changing calls, disables cross-origin CORS by default, and requires a per-session CSRF token for mutations. |
| CCC-REQ-038 | API file access is ID-based and confined to authorized roots; no endpoint can read or manipulate arbitrary paths, UNC/device paths, or reparse points. |

## 5. Non-goals

Paid dependencies; cloud hosting; account-password bots; bypassing platform controls; an
in-house full editor; multi-tenant SaaS; automatic unapproved HVAC captions or claims;
advanced AI orchestration without measured benefit; universal API publishing promises;
ingest that mutates originals; status derived only from optimistic provider responses;
website changes; multi-user remote access in early stages.

## 6. Phased scope

Scope is delivered in the stages defined in `docs/ROADMAP.md` (0–6). Each stage has
explicit exclusions and an owner gate; Stage 6 is optional. No stage auto-advances.

## 7. Change control

1. Requirements may be added/changed only by owner directive or approved stage scope.
2. Every material change is recorded in `docs/DECISION_LOG.md` with rationale.
3. Requirement → stage → test → evidence mapping lives in `docs/ACCEPTANCE_TESTS.md`.
4. Conflicting authoritative documents stop work until resolved by the owner.
5. Documentation and UI must never claim more than verified implementation state.
