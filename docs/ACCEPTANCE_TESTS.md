# Acceptance Tests — Content Command Center

**Status:** Stage 0 defines the mapping; no application tests exist yet. Every future
stage must update this file with executed results. "Evidence" means observable output
recorded in the stage report (command output, test counts, file checksums, screenshots).

---

## 1. Requirement → stage → test → evidence map

| Req ID | Stage | Focused test | Evidence expected |
|---|---|---|---|
| CCC-REQ-001 | 2 (full), 1A (start) | End-to-end dry run: ingest → concept → variant → approval → handoff record → status | Walkthrough log with persisted rows |
| CCC-REQ-002 | 1B/2 | Concept grouping creates one concept with master/shorts/stills/SRT links via `concept_asset` | DB query output + UI list |
| CCC-REQ-003 | 1B | Search/filter returns correct assets offline | Test output; network disabled |
| CCC-REQ-004 | 2 | Per-platform variants are independently editable | Test mutating one variant; others unchanged |
| CCC-REQ-005 | 2 | Unapproved variant cannot be scheduled/handed off (server-enforced) | API test returns refusal; DB state unchanged |
| CCC-REQ-006 | 2 | Per-destination calendar shows separate rows/states and gap detection | Calendar test + DB assertions |
| CCC-REQ-007 | 2 | Native handoff package contains export/caption/link/date/checklist | Package fixture assertions |
| CCC-REQ-008 | 5 (optional) | Mock-adapter contract tests; live gate blocked until approved | Contract tests; approval record |
| CCC-REQ-009 | 2 | Draft/private/scheduled never produce `platform_confirmed`; timeout → `unknown` | Status-transition test matrix |
| CCC-REQ-010 | 2 | Time entries persist per concept/phase; reports aggregate correctly | Time-entry test + report output |
| CCC-REQ-011 | 1A | Source hash+mtime+existence unchanged after verified copy; no hard link created | Before/after checksums + link-count check |
| CCC-REQ-012 | 1A | Half-written file not ingested; quiet period respected; FFprobe gate; lock retry; pause-and-resume writer does not yield a false complete (with/without sentinel); mid-copy source change aborts | Fixture matrix output incl. pause/resume |
| CCC-REQ-013 | 1A | Duplicate import links the existing asset; dedup never suppresses a legitimate publication to another destination/time; only overlapping same-destination duplicates warn and require confirmation | Duplicate fixture + draft-creation test |
| CCC-REQ-014 | 1A | Recursive/junction/symlink paths refused by default | Traversal fixture tests |
| CCC-REQ-015 | 1A | Corrupted/huge/locked/Unicode/HDR-rotated cases produce clean states | Fixture matrix results |
| CCC-REQ-016 | 1A | Below-threshold free space blocks copy with warning | Simulated disk-space test |
| CCC-REQ-017 | 2 | Snapshot import records source SHA + timestamp; freshness warning appears | Import test + UI state |
| CCC-REQ-018 | 2 | Pending links excluded from approved defaults | Assertion on composer link list |
| CCC-REQ-019 | 2 | Residential vs commercial mappings never mix within a variant | Mapping test |
| CCC-REQ-020 | 2 | Fundraiser links only in explicit support campaigns; never acquisition defaults | Assertion + review |
| CCC-REQ-021 | 0+ | No writes to external repos (git remotes/actions review) | Repo configuration evidence |
| CCC-REQ-022 | 2+ | No GA4/GTM calls; no duplicate events from CCC | Network inspection |
| CCC-REQ-023 | 1A+ | Server binds loopback only; remote connection refused; forged `Host` rejected | Connection test + forged-Host test |
| CCC-REQ-024 | 1+ | Secret scan of repo/logs/fixtures clean; secrets only in OS store | Scan output |
| CCC-REQ-025 | 2+ | Malformed/unknown authorization state fails closed | Negative tests |
| CCC-REQ-026 | 1+ | PII never appears in logs/exports without recorded permission | Log/export inspection |
| CCC-REQ-027 | 2+ | External send requires explicit approval event | Approval-gate test |
| CCC-REQ-028 | 0+ | Cost audit per stage demonstrates $0 | Dependency/billing checklist |
| CCC-REQ-029 | 0+ | License inventory updated before adoption | `docs/SOURCE_EVIDENCE.md` entry |
| CCC-REQ-030 | 0 | `LICENSE_DECISION.md` present; no license assigned | File check |
| CCC-REQ-031 | 1B+ | Every displayed counter maps to a DB query result; fixtures labeled | UI/DB consistency test |
| CCC-REQ-032 | 1+ | Statuses `not_configured/saved/connected/...` accurate; stub never "connected" | Adapter status tests |
| CCC-REQ-033 | 0+ | Required suites run and results reported with counts | Stage reports |
| CCC-REQ-034 | 2 | UI/docs state PC-off limitation for local jobs | Documentation + UI string test |
| CCC-REQ-035 | 6 (guard from 1) | Workspace isolation: no shared roots/accounts/campaigns; cross-workspace access denied | Isolation test suite |
| CCC-REQ-036 | 0.5+ | No lead-capture/attribution endpoints or storage exist; route inventory and docs confirm SCS attribution stays external | Doc review + endpoint inventory |
| CCC-REQ-037 | 1A | Forged `Host`, foreign `Origin`, and missing CSRF token are rejected on mutations; no permissive CORS | Security test output |
| CCC-REQ-038 | 1A | Traversal, UNC/device paths, and reparse points rejected; only ID-based access inside authorized roots | Path-confinement test output |

## 2. Stage 0 acceptance (complete)

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

## 2a. Stage 0.5 acceptance (this stage)

| Check | Method | Result requirement |
|---|---|---|
| Public-repo redaction review | Manual audit + `git grep` for emails/identifiers | No personal email, inactive account names, or unnecessary machine identifiers in docs |
| Licensing clarity | Review `LICENSE_DECISION.md` + README | Public visibility explicitly does not grant reuse rights |
| Protection recommendation | `gh api .../rulesets` availability check | Recommended `main` configuration documented; not applied without owner approval |
| Verified-copy-only policy | Review AGENTS/ARCHITECTURE/DATA_MODEL | No hard-link path remains in the initial plan |
| Local API controls | Review THREAT_MODEL/ARCHITECTURE + requirement mapping | Host/Origin/CORS/CSRF/path-confinement requirements and tests defined |
| Data-model authority | Review DATA_MODEL §7 | `concept_asset` is the only grouping relationship; dedup cannot suppress publication |
| Stage 1A/1B boundaries | Review ROADMAP | Separate scopes, exclusions, and pass criteria |
| Dependency validation | `docs/ENVIRONMENT.md` §2 | Versions checked; watchdog deferral recorded |
| FFmpeg procedure | `docs/ENVIRONMENT.md` §3 | Distribution, checksum, license, and owner gate documented |
| SCS reference | `docs/SOURCE_EVIDENCE.md` §2/§2a | Current `87da9a2` acknowledged; historical snapshot preserved |
| Documentation verifier | `python scripts/verify_docs.py` | Requirement mapping, status marker, docs inventory, anchors all pass |

## 3. Test fixture policy

- **No binary media is committed.** Fixtures are generated at test time (FFmpeg `lavfi`
  sources or programmatically written minimal bytes) into ignored/temporary paths.
- Real owner media is used only for local verification, never committed, logged, or
  copied into reports; no customer footage is ever a fixture.
- Fixture set for Stage 1A: valid small clip; half-written file; corrupted file;
  duplicate pair; locked/in-use file; Unicode and long paths; nested/junction path;
  oversized file (cap logic); low-disk simulation; pause-and-resume writer with and
  without a completion sentinel.

## 4. Pass/fail rules

- A check passes only with observed output recorded in the stage report.
- Skipped tests must be listed with reason; skipped ≠ passed.
- Any false status in UI or report fails the stage regardless of other results.
- A stage cannot be called complete while a listed pass criterion is unverified.
