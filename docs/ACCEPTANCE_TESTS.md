# Acceptance Tests — Content Command Center

**Status:** Stage 0 defines the mapping; no application tests exist yet. Every future
stage must update this file with executed results. "Evidence" means observable output
recorded in the stage report (command output, test counts, file checksums, screenshots).

---

## 1. Requirement → stage → test → evidence map

| Req ID | Stage | Focused test | Evidence expected |
|---|---|---|---|
| CCC-REQ-001 | 2 (full), 1 (start) | End-to-end dry run: ingest → concept → variant → approval → handoff record → status | Walkthrough log with persisted rows |
| CCC-REQ-002 | 1/2 | Concept grouping creates one concept with master/shorts/stills/SRT links | DB query output + UI list |
| CCC-REQ-003 | 1 | Search/filter returns correct assets offline | Test output; network disabled |
| CCC-REQ-004 | 2 | Per-platform variants are independently editable | Test mutating one variant; others unchanged |
| CCC-REQ-005 | 2 | Unapproved variant cannot be scheduled/handed off (server-enforced) | API test returns refusal; DB state unchanged |
| CCC-REQ-006 | 2 | Per-destination calendar shows separate rows/states and gap detection | Calendar test + DB assertions |
| CCC-REQ-007 | 2 | Native handoff package contains export/caption/link/date/checklist | Package fixture assertions |
| CCC-REQ-008 | 5 (optional) | Mock-adapter contract tests; live gate blocked until approved | Contract tests; approval record |
| CCC-REQ-009 | 2 | Draft/private/scheduled never produce `platform_confirmed`; timeout → `unknown` | Status-transition test matrix |
| CCC-REQ-010 | 2 | Time entries persist per concept/phase; reports aggregate correctly | Time-entry test + report output |
| CCC-REQ-011 | 1 | Source hash+mtime+existence unchanged after ingest | Before/after checksums |
| CCC-REQ-012 | 1 | Half-written file not ingested; stability window respected; FFprobe gate; lock retry | Fixture test output |
| CCC-REQ-013 | 1 | Duplicate import rejected; duplicate publish blocked by idempotency | Duplicate fixture + job test |
| CCC-REQ-014 | 1 | Recursive/junction/symlink paths refused by default | Traversal fixture tests |
| CCC-REQ-015 | 1 | Corrupted/huge/locked/Unicode/HDR-rotated cases produce clean states | Fixture matrix results |
| CCC-REQ-016 | 1 | Below-threshold free space blocks copy with warning | Simulated disk-space test |
| CCC-REQ-017 | 2 | Snapshot import records source SHA + timestamp; freshness warning appears | Import test + UI state |
| CCC-REQ-018 | 2 | Pending links excluded from approved defaults | Assertion on composer link list |
| CCC-REQ-019 | 2 | Residential vs commercial mappings never mix within a variant | Mapping test |
| CCC-REQ-020 | 2 | Fundraiser links only in explicit support campaigns; never acquisition defaults | Assertion + review |
| CCC-REQ-021 | 0+ | No writes to external repos (git remotes/actions review) | Repo configuration evidence |
| CCC-REQ-022 | 2+ | No GA4/GTM calls; no duplicate events from CCC | Network inspection |
| CCC-REQ-023 | 1+ | Server binds loopback only; remote connection refused | `netstat`/connection test |
| CCC-REQ-024 | 1+ | Secret scan of repo/logs/fixtures clean; secrets only in OS store | Scan output |
| CCC-REQ-025 | 2+ | Malformed/unknown authorization state fails closed | Negative tests |
| CCC-REQ-026 | 1+ | PII never appears in logs/exports without recorded permission | Log/export inspection |
| CCC-REQ-027 | 2+ | External send requires explicit approval event | Approval-gate test |
| CCC-REQ-028 | 0+ | Cost audit per stage demonstrates $0 | Dependency/billing checklist |
| CCC-REQ-029 | 0+ | License inventory updated before adoption | `docs/SOURCE_EVIDENCE.md` entry |
| CCC-REQ-030 | 0 | `LICENSE_DECISION.md` present; no license assigned | File check |
| CCC-REQ-031 | 1+ | Every displayed counter maps to a DB query result; fixtures labeled | UI/DB consistency test |
| CCC-REQ-032 | 1+ | Statuses `not_configured/saved/connected/...` accurate; stub never "connected" | Adapter status tests |
| CCC-REQ-033 | 0+ | Required suites run and results reported with counts | Stage reports |
| CCC-REQ-034 | 2 | UI/docs state PC-off limitation for local jobs | Documentation + UI string test |
| CCC-REQ-035 | 6 (guard from 1) | Workspace isolation: no shared roots/accounts/campaigns; cross-workspace access denied | Isolation test suite |

## 2. Stage 0 acceptance (this stage)

| Check | Method | Result requirement |
|---|---|---|
| New private repo owned by authenticated CLI account | `gh api user`, `gh repo view` | login matches repo owner; `visibility=PRIVATE` |
| Documentation present and substantive | File inventory + review | All files in README map exist |
| Internal links resolve | `scripts/verify_docs.py` | Zero broken relative links |
| Requirement IDs present and mapped | Verifier + manual | IDs in charter and map |
| Honest status | Review | README/roadmap state Stage 0 docs-only |
| SCS sources recorded with SHA | `docs/SOURCE_EVIDENCE.md` | Commit SHA + blob SHAs recorded |
| Staged files contain no secrets/media | Manual scan + staged diff | No matches; no media extensions |
| Local HEAD == remote main | `git rev-parse HEAD` + GitHub API | SHA equality observed |
| Existing repos unchanged | Review of this run's commands | No writes/pushes to them |

## 3. Test fixture policy

- Synthetic fixtures only in the repository (tiny generated videos/images).
- Real owner media is used for local verification only and is never committed, logged,
  or copied into reports.
- Fixture set for Stage 1: tiny valid MP4; half-written MP4; corrupted MP4; duplicate
  pair; locked/in-use file; Unicode-name file; nested/junction path; HDR/rotated sample
  if feasible; oversized file for cap logic; low-disk simulation.

## 4. Pass/fail rules

- A check passes only with observed output recorded in the stage report.
- Skipped tests must be listed with reason; skipped ≠ passed.
- Any false status in UI or report fails the stage regardless of other results.
- A stage cannot be called complete while a listed pass criterion is unverified.
