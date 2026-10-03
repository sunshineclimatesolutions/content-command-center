# Stage 0 Review Checklist — Content Command Center

Adapted from the owner-supplied review checklist. Use it after Stage 0 is submitted.
**None of these claims is true merely because the implementer asserts it.**

## Identity and repository isolation

- [ ] `gh api user` authenticated login matches the new repo owner in the reported URL
      (expected: `sunshineclimatesolutions`).
- [ ] Repo is **new and private**, and reachable from the account/connector used for
      review.
- [ ] Reported local `HEAD` equals remote `main` SHA; the repo contains only approved
      documentation and the small verification script.
- [ ] Neither existing business website has new writes, deployment changes, or
      unauthorized integration changes.
- [ ] No token, `.env`, private customer media, other local archives, or billing
      credentials appear in repository history.
- [ ] If private-repo branch protection is unavailable under the active plan, the human
      gate is documented; no false assertion of enforcement.

## Product fidelity

- [ ] README describes the complete workflow from the SCS calendar through
      shooting/Resolve, ingestion, asset library, approval, four-week plan, and actual
      confirmed publication.
- [ ] Residential lead acquisition stays primary; TAB/commercial engine remains
      distinct; Sparkling Standard remains deferred and separately controlled.
- [ ] `$0` **new** spend is enforceable; no obligatory paid service, paid API, new
      hardware, or payment-required free tier.
- [ ] Original footage is preserved; local files and SQLite are the core; existing
      Resolve Studio remains the professional editor.
- [ ] AI-assisted clip selection and generated descriptions (if ever used) are optional
      unapproved candidates, never invented HVAC measurements.
- [ ] Native scheduling and manual packages make the MVP useful **without** social API
      grants and **without** leaving the PC on for a local scheduler.
- [ ] Published vs draft-uploaded vs remotely scheduled vs owner-reported manual states
      are separate per destination.

## Technical documentation

- [ ] Root `AGENTS.md` explicitly requires documentation review at the start of every
      session and has owner gates, no-cost, safety, test, Git, reporting, and STOP rules.
- [ ] Charter, workflows, architecture/data model, cost/license policy, threat model,
      open-source evaluation, platform matrix, roadmap, acceptance tests, and evidence
      ledger all exist and are internally consistent.
- [ ] Source ledger grounds the SCS repo's current state and labels inaccessible
      material unknown/provisional.
- [ ] Feature claims and subscription/API restrictions are dated and attributed; Postiz
      and alternatives are **not** presumed account-tested.
- [ ] Planned stacks are flagged as decisions/proposals, not implemented features.
- [ ] Stage 1A/1B scope is narrow and has concrete file-integrity tests (unfinished files,
      locks, duplicates, failure/restart, large and Unicode media, storage capacity).

## Stage 0.5 corrective pass

- [ ] Repository visibility is **public** and the docs state the owner changed it
      deliberately; the original private creation is preserved as history (ADR-017).
- [ ] Redaction audit: no personal email, inactive account names, or unnecessary
      machine identifiers in committed docs; the residual commit-author email in Git
      history is disclosed, not hidden.
- [ ] Licensing clarity: public visibility is explicitly not a reuse license
      (`LICENSE_DECISION.md`).
- [ ] `main` protection recommendation documented (PR required, force-push blocked,
      deletion blocked, 0 approvals, no mandatory external reviewers) and **not applied**
      without owner approval (ADR-018).
- [ ] Verified-copy-only ingestion: no hard-link option remains in
      AGENTS/ARCHITECTURE/DATA_MODEL/ROADMAP; source-unchanged and destination-checksum
      requirements are present.
- [ ] Pause-and-resume test case and completion-sentinel limitation documented.
- [ ] Local API browser-threat controls (Host/Origin/CORS/CSRF) and path-confinement
      requirements map to CCC-REQ-037/038 with Stage 1A tests.
- [ ] `concept_asset` is the single authoritative grouping relationship; dedup cannot
      suppress legitimate cross-destination/time publication (DATA_MODEL §7).
- [ ] Stage 1A/1B scopes finalized with exclusions and pass criteria; nothing implemented.
- [ ] Python 3.14 dependency validation recorded; watchdog deferral documented.
- [ ] FFmpeg distribution/checksum/license procedure documented; installation still
      gated on owner authorization.
- [ ] SCS reference acknowledges `87da9a2` while preserving the Stage 0 snapshot; no
      lead-attribution duplication (CCC-REQ-036).
- [ ] `scripts/verify_docs.py` checks requirement mapping, status markers, docs
      inventory, and anchors; all checks pass.
- [ ] Draft PR opened from `feature/stage-0p5-architecture-corrections`; not merged.

## Gate decision

- [ ] All documentation links verified; docs audit and git staged-file/secrets checks
      reported accurately.
- [ ] GitHub remote accessible for independent review. If the reviewer connector uses
      another account, grant it access before calling the repo verified.
- [ ] The exact commit under review is recorded (local SHA == remote SHA).
- [ ] **No implementation authorized yet.** Stage 1A begins only after repository and
      architecture audit.
