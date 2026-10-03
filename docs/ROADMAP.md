# Roadmap — Content Command Center

**Status:** Stage 0.5 corrective documentation pass in review; Stage 1A not authorized.
Never auto-run the roadmap. Each stage ends with an owner review gate.

CURRENT-STAGE: 0.5

---

## Stage 0 — Documentation constitution, repository, research (COMPLETE)

**Authorized:** 2026-10-03 directive. **Executed:** repository creation, documentation,
verification, commit, push, evidence. Commits `185b4ea`, `4dfc032` on `main`.

- Deliverables: `README.md`, `AGENTS.md`, all `docs/*` specifications, `.gitignore`,
  `LICENSE_DECISION.md`, `scripts/verify_docs.py`, review checklist.
- Historical note: the repository was created **private** and was deliberately made
  **public** by the owner afterwards (ADR-017). Public visibility grants no license.
- Pass criteria: new repo owned by the CLI-authenticated account; docs exist, links
  resolve, requirement IDs map, sources dated, honest status; staged-file secret scan
  clean; local HEAD == remote `main` SHA; existing repos untouched.
- Gate: owner/architect review before further work.

## Stage 0.5 — Corrective documentation pass (THIS STAGE)

**Authorized:** 2026-10-03 corrective directive on branch
`feature/stage-0p5-architecture-corrections` (draft PR, not merged).

- Corrections: public-repo redactions and licensing clarity; verified-copy-only
  ingestion (hard links removed); local API browser-threat controls; authoritative
  concept-asset relationship plus dedup/republish semantics; Stage 1A/1B split; Python
  3.14 dependency validation; FFmpeg acquisition/checksum plan; SCS reference update to
  `87da9a2`; no lead-attribution duplication; stronger documentation verifier.
- Excluded: application code, software installation, account connections, live posts,
  any spending.
- Pass criteria: verifier passes with strengthened mapping/status checks; staged-file
  security review clean; branch pushed and draft PR opened; `main` untouched.
- Gate: owner review of the draft PR before any Stage 1A work.

## Stage 1A — Ingest core (headless proof)

**Goal:** prove safe, honest, resumable local ingest of real owner media without UI
polish, publishing, or marketing integration.

**Scope:** app start/stop; one user-selected watched folder; standard-library polling
scanner; quiet-period detection; FFprobe validation; Windows lock retry; **verified
copy** (no hard links); source-unchanged-during-copy check; destination SHA-256
verification; resume/recovery; minimal SQLite schema + migrations (`workspace`,
`folder_watch`, `asset`, `ingest_run`); content-hash dedup identity; manual import entry
point; persistent job/error states; local logs free of secrets and PII.

**Explicitly excluded:** composer, publishing, campaign import, thumbnails/search UI,
concept grouping UI, drag-and-drop, any account connection, any AI tool, any cloud call,
Resolve scripting.

**Dependencies:** owner choice of workspace root; owner-authorized download of the
pinned FFmpeg LGPL shared build with checksum verification (`docs/ENVIRONMENT.md` §3);
stack ADR (ADR-005) resolved.

**Fixtures:** generated at test time (FFmpeg `lavfi` or programmatic minimal bytes) into
ignored temp paths — **no committed binary media and no customer footage**. Cases:
valid small clip; half-written file; corrupted file; duplicate pair; locked/in-use file;
Unicode and long paths; nested/junction path; oversized file (cap logic); low-disk
simulation; **pause-and-resume writer** (writer stops long enough to appear finished,
then resumes), with and without a completion sentinel.

**Pass criteria (testable):**
1. A file still being written is not imported until stable across the quiet period; a
   half-written MP4 fails validation without DB or filesystem damage.
2. After import, source hash and mtime are unchanged and the file still exists; no hard
   link was created.
3. Destination SHA-256 matches the source hash computed during copy; a simulated
   mid-copy source change aborts the import and leaves no library row.
4. Duplicate import links/reuses the existing asset; interrupted import resumes or
   restarts from a verified checkpoint without partial rows.
5. The pause-and-resume fixture does not produce a false "complete" library entry when a
   sentinel is present; without a sentinel the known limitation is documented and
   recovery can remove the incomplete copy and re-import.
6. Unicode paths, long paths, and a locked file produce visible, clean outcomes.
7. Low-disk preflight blocks the copy below threshold with a clear message.
8. Local API endpoints reject forged `Host`, foreign `Origin`, and missing CSRF tokens;
   no endpoint can read outside authorized roots.
9. No network egress occurs during ingest (inspection/monitoring evidence).
10. Tests report actual counts; failures are not skipped.

**Gate:** owner reviews Stage 1A evidence and explicitly approves Stage 1B.

## Stage 1B — Library surface

**Goal:** make the proven ingest core usable.

**Scope:** thumbnail generation and display; search/filter; concept creation and
`concept_asset` linking; drag-and-drop/manual import UI; relink after folder move; clean
restart persistence; read-only status honesty in the UI; time-entry capture groundwork
(CCC-REQ-010).

**Explicitly excluded:** publishing, campaign import, calendar, API connections.

**Pass criteria:** every displayed counter/status maps to DB state (CCC-REQ-031);
grouping uses only `concept_asset`; relink restores access without duplicating assets;
restart preserves state; tests report actual results.

**Gate:** owner review before Stage 2.

## Stage 2 — Production package

**Goal:** the useful end-to-end workflow without any API connection.

**Scope:** content concepts/versions and master-vs-short relationships; read-only
validated SCS calendar and approved-UTM snapshot (source SHA + freshness warning);
independent platform composer; editorial approval recorded; basic four-week calendar;
usable native handoff (correct export, caption, CTA, date, platform URL, checklist,
copy/reveal); per-account proof and states; no false auto-publishing.

**Excluded:** API auto-posting, analytics imports, Sparkling Standard, AI generation.

**Pass criteria:** approved-only variants can be handed off; pending UTM links are never
offered; every displayed status matches DB state; a concept cannot be fully published
while a selected destination is incomplete; manual confirmation is a distinct state from
API verification.

**Gate:** owner review.

## Stage 3 — Reduce edit time (benchmark before complexity)

**Goal:** measure, don't assume.

**Scope:** compare existing Resolve Studio workflow/templates/transcription/reframe
against **one** OSS rough-cut option and **one optional** local clipper on safe approved
sample content. Record machine specs, processing time, owner edit time, measured time
saved, quality defects, and when automation should be skipped. Implement only the
combination with demonstrated benefit.

**Excluded:** unverified AI claims; any cloud AI; auto-approval of AI output.

**Pass criteria:** a written benchmark table with real timings and sample evidence;
adoption decision (adopt/reject) recorded in the decision log; no factual claims or
measurements generated by AI.

**Gate:** owner review.

## Stage 4 — Native batching and reliability

**Goal:** a four-week batch that survives real life.

**Scope:** refine scheduling packages and handoffs for actual free native schedulers;
reminders; queue; missed-post handling; honest status reconciliation; backup + restore
drill; friction audit of four-week preparation.

**Excluded:** API auto-publication; paid scheduling tools.

**Pass criteria:** a full four-week package is prepared and tracked; a restore drill
recovers the DB and library links; missed-post handling surfaces exceptions rather than
faking completion; statuses remain evidence-based.

**Gate:** owner review.

## Stage 5 — OPTIONAL verified auto-publication

**Goal:** evidence-driven decision on API auto-posting.

**Scope:** isolated self-hosted spike of **Postiz (primary) and TryPost (alternative
only)**, including actual resource use and licensing; mocked publisher first; then —
only with separate permission — real OAuth/developer app registrations, approved
official APIs, token storage, idempotent jobs, and end-to-end verified publication.
Native/manual routes stay available. A locally hosted scheduler that cannot run while
the PC is off must be visible in UX/docs.

**Excluded:** paid X or any paid API; Mixpost beyond a limited check; connecting SCS
accounts without explicit approval.

**Pass criteria:** one verified public post with a real URL and no duplicate, per
approved destination; resource/license report; clear decision to adopt or reject each
tool; no account risk introduced.

**Gate:** explicit separate owner approval before any real connection.

## Stage 6 — OPTIONAL analytics/workspace expansion

**Scope:** stronger analytics imports (honest, non-duplicative) and a properly isolated
Sparkling Standard workspace (separate root, permissions, branding, campaigns,
connections). Only when the SCS product is stable.

**Pass criteria:** cross-workspace tests prove no data/credential leakage; analytics
imports never write into SCS GA4/GTM.

**Gate:** owner review.

---

## Cross-references

Requirement → stage → test → evidence mapping lives in
`docs/ACCEPTANCE_TESTS.md`. Decisions live in `docs/DECISION_LOG.md`. Dated sources live
in `docs/SOURCE_EVIDENCE.md`.
