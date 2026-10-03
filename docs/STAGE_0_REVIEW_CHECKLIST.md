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
- [ ] Stage 1 scope is narrow and has concrete file-integrity tests (unfinished files,
      locks, duplicates, failure/restart, large and Unicode media, storage capacity).

## Gate decision

- [ ] All documentation links verified; docs audit and git staged-file/secrets checks
      reported accurately.
- [ ] GitHub remote accessible for independent review. If the reviewer connector uses
      another account, grant it access before calling the repo verified.
- [ ] The exact commit under review is recorded (local SHA == remote SHA).
- [ ] **No implementation authorized yet.** Stage 1 begins only after repository and
      architecture audit.
