# AGENTS.md — Content Command Center Project Constitution

This file governs **every** OpenCode/AI engineering session in this repository. It is
binding. If any instruction conflicts with this file, stop and ask the owner.

---

## 1. Mandatory session start

Before changing anything, every session must read:

1. `AGENTS.md` (this file)
2. `README.md`
3. `docs/PRODUCT_CHARTER.md`
4. `docs/ARCHITECTURE.md`
5. `docs/ROADMAP.md`
6. `docs/ACCEPTANCE_TESTS.md`
7. `docs/ENVIRONMENT.md`
8. The current stage's plan/ADR and the files it names

Read external sources only when the assigned task requires them, and only read-only.

Then establish repository truth: `git branch --show-current`, `git rev-parse HEAD`,
`git status --short`, and read the files to be modified before modifying them.

## 2. Document priority when instructions conflict

1. This `AGENTS.md`
2. The current owner directive for the current stage
3. `docs/PRODUCT_CHARTER.md`
4. `docs/ARCHITECTURE.md` + current stage ADR
5. `docs/ROADMAP.md` / `docs/ACCEPTANCE_TESTS.md`
6. Other docs
7. Older research or chat context

If two authoritative documents materially conflict, **stop and ask the owner**. Do not
silently pick one. Record resolved conflicts in `docs/DECISION_LOG.md`.

## 3. Scope and hard boundaries

- Work only in **this** repository. The SCS website repository
  (`sunshineclimatesolutions/Sunshine-Climate-Solutions`) and the Sparkling Standard
  repository are **read-only external sources**. Never push, open PRs, or modify them.
- **$0 new spending.** No subscriptions, trials, paid APIs, hosting, domains, hardware,
  or payment-method requirements. If a task appears to require spending, stop.
- Core functionality must remain Windows-first and offline-capable.
- No live posts, account connections, OAuth registrations, or developer-app submissions
  without a per-stage explicit owner approval.
- No production deployment, no public server, no tunnel exposing the app or media.
- No accidental network use: no telemetry, no silent uploads, no cloud calls in core
  paths. Optional AI tools are local-only and candidate-output-only.
- This repository is **public**: never commit secrets, credentials, personal contact
  details, machine identifiers, private business data, or customer media. Public
  visibility does not grant a license to anyone; the project remains unlicensed until
  the owner decides (see `LICENSE_DECISION.md`).
- Never implement or duplicate SCS lead capture or campaign attribution. CCC may import
  approved campaign links read-only and record publication proof; leads, consent
  records, first/latest-touch attribution, and GA4/GTM data stay in their existing SCS
  systems.

## 4. Engineering conduct

- Make the **narrowest useful change**. Do not perform unrelated refactors or cleanup.
- No speculative SaaS, multi-tenant architecture, or abstract frameworks with no
  current consumer.
- No scraping, no account-password handling, no unauthorized browser automation, no
  CAPTCHA/rate-limit workarounds, no session-cookie reuse against platform terms.
- No duplicate analytics events and no changes to GA4/GTM definitions or the SCS
  website.
- Never let AI output define factual claims, measurements, or authorization. AI
  suggestions are unapproved candidate material until a human reviews them in a
  recorded approval step.
- Keep the separation: ingest → library → composer → publishing adapters → UI. A file
  watcher must not publish; a UI component must not hold authorization truth.

## 5. Truthfulness requirements

- **No fictitious UI.** Every counter, list, status, and button must correspond to
  persisted reality or be explicitly labeled a wireframe/test fixture in the UI itself.
- **No fake publishing.** Destination states are independent; `PLATFORM_CONFIRMED`
  requires a verified public URL or platform acceptance evidence; owner-reported manual
  publication is a separate state from API-verified publication.
- **No fake integrations.** A stored credential is not a connection. A stub adapter
  reports `adapter_not_implemented`; a saved key reports `saved`, not `connected`.
- Use honest statuses: `not_configured`, `saved`, `verified`, `connected`,
  `connection_failed`, `adapter_not_implemented`, `unavailable`, `manual_pending`,
  `platform_confirmed`, `owner_reported_manual`, `unknown`.
- Never claim a test passed, a build is green, a push succeeded, or a protection is
  enforced without the observed command output as evidence.
- Never present a draft upload, private/unlisted upload, or scheduled item as a public
  publication.

## 6. Media safety and immutability

- Never delete, move, rename, or re-encode original media or Resolve exports.
- **Verified copying only.** Hard links are not part of the implementation. After a
  copy, the destination is checksum-verified (SHA-256) and the library record is
  committed in one recoverable transaction; interrupted operations resume or safely
  restart.
- Require all before ingestion: unchanged size+mtime across the full configurable quiet
  period; successful `ffprobe` parse; a successful open/read retry after Windows
  sharing violations; and a post-copy check that the source did not change while
  copying.
- Filesystem quiet-period detection has a known limitation: a writer that pauses long
  enough can look finished. Support an optional explicit render-completion signal (for
  example a sentinel/sidecar file) for producers that can emit one, and never treat
  event notifications alone as completion.
- Deduplicate by content identity in the library, but never let dedup suppress a
  legitimate publication: the same approved material may be published to different
  destinations or at different times, with duplicate warnings only and explicit
  confirmation required.
- No recursive watching by default. No symlink/junction traversal. Validate every path.
- Handle low disk space, unexpected formats, HDR/rotation/Unicode paths, and locked
  files with clean failure states — never by skipping silently.
- Preserve source-truth provenance for every asset; tests use generated synthetic media.
  Never commit binary media or use runtime customer media as a fixture.

## 7. Sensitive content, rights, and claims

- Customer footage, addresses, faces, plates, paperwork, phone numbers, and personal
  data must not be exported, logged, or published without recorded permission.
- Field measurements require context; never present one number as a universal standard.
  Never fabricate HVAC measurements, reviews, job outcomes, or customer claims.
- Respect music/stock/third-party media licenses and platform commercial-music rules.
- The SCS fundraising layer (`/support/`) stays separate from customer-acquisition
  content; never mix campaign types in one publication variant.

## 8. Security defaults

- Bind the application to `127.0.0.1` only. No remote login, no public media server.
- Defend the local API against malicious browser requests: validate `Host` against the
  loopback allowlist, validate `Origin`/`Referer` on state-changing calls, disable
  cross-origin CORS by default, require a per-session CSRF token header on mutations,
  and use `SameSite=Strict` if cookies are ever introduced.
- File access is by catalog ID only; every path is canonicalized and confined to
  configured roots. No endpoint may read or manipulate an arbitrary path, UNC/device
  path, or reparse point.
- Future secrets go to the Windows Credential Manager / DPAPI, never to files, git
  history, screenshots, logs, or reports.
- Principle of least privilege for OAuth scopes and local processes.
- Fail closed when authorization or configuration is unknown or malformed.
- Never log tokens, secrets, private notes, or customer data.
- Media shared with any external platform must be an explicit, reviewed action.

## 9. Testing and verification

- Every behavioral change ships with focused unit/integration tests, plus the file-safety
  tests listed in `docs/ACCEPTANCE_TESTS.md` where ingest is involved.
- Run focused tests during development; run the stage's required suite before reporting.
- Never delete, skip, loosen, or rewrite a legitimate test to obtain green output.
- When a test fails, read the failure, classify it (defect/regression/test
  expectation/pre-existing/environment), and fix the root cause.
- Report actual observed counts and command output; never reuse stale results.
- Verify UI claims against persisted data in tests.

## 10. Git and release workflow

- Stage 0: a single documentation commit on `main` in this new repository, pushed only
  after owner-authorized pre-push verification steps.
- Later stages: branch `feature/stage-N-description`; push the feature branch to this
  repository and open a **draft PR** when possible.
- **Never** merge a feature branch, push application code directly to `main`, tag a
  release, deploy, or connect a real account without explicit owner approval for that
  specific step.
- Never force-push, rewrite history, or reset away owner work.
- Stage only intended files with explicit paths; review `git status`, `git diff`, and
  `git diff --cached`; run `git diff --cached --check`; confirm no secrets/media/debug
  files are staged.
- No automatic dependencies, Actions, branch protections, billing changes, or public
  visibility changes. If branch protection is unavailable under the plan, document the
  limitation and use procedural gates instead.

## 11. Owner approval gates

Explicit owner approval is required before:

- any stage beyond the one currently authorized;
- any live social account connection, developer-app registration, OAuth flow, or post;
- any purchase, signup, trial, or payment-method entry;
- any modification to the SCS or Sparkling Standard repositories;
- merging, tagging, deploying, or changing repository visibility/protection/billing;
- adopting a new third-party dependency with license obligations that need review.

## 12. When to STOP immediately

Stop and escalate to the owner when:

- the working repository/remote is not this Content Command Center repository;
- credentials, payment, or account access are requested by a tool/step;
- a critical external source is inaccessible and couldn't be marked provisional;
- a platform API turns out paid, restricted, or unapproved for the needed action;
- instructions conflict with this file or between authoritative documents;
- continuing would risk deleting/altering originals, exposing private data, or making a
  live publication;
- an unresolved safety or security question blocks honest completion.

Report the blocker, what was completed, and what remains — never guess around it.

## 13. Required report format for every stage

```text
STAGE / TASK:
STATUS: VERIFIED DOCUMENTATION | TESTED LOCALLY | TESTED WITH ACCOUNT | PARTIAL | BLOCKED
BRANCH / HEAD / REMOTE / PR:
COMPLETED:
EVIDENCE (commands + actual results):
FILES CHANGED:
TESTS RUN (counts, observed results):
SCREENSHOTS / DEMO (only real, labeled):
NOT COMPLETED / DEFERRED:
COST AUDIT ($0 or disclosed violation):
RISKS / UNKNOWNS:
APPROVAL REQUESTED:
```

Labels must be used precisely: **VERIFIED DOCUMENTATION** (sources checked),
**TESTED LOCALLY** (commands run on this machine), **TESTED WITH ACCOUNT** (verified in
a real account with evidence), **UNKNOWN**, **BLOCKED**. Never blur them.

## 14. Performance and code quality

Prefer clear interfaces, small helpers, parameterized queries, server-derived scope,
explicit domain boundaries, typed structures, and deterministic behavior. Avoid
duplicated policy logic, unbounded table loads where scoped queries suffice, swallowed
exceptions around security behavior, and copy-pasted authorization. Correctness and
maintainability come before cleverness.

## 15. Documentation duties

When a decision is made, record it in `docs/DECISION_LOG.md`. When a new source is
used, record it in `docs/SOURCE_EVIDENCE.md` with date and URL. When behavior changes,
update `docs/ACCEPTANCE_TESTS.md`. Keep this file concise; detailed guidance belongs in
the referenced documents.
