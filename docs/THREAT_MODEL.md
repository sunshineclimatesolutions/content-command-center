# Threat Model — Content Command Center

**Status:** Stage 0 design. Controls below are requirements for future stages, not
implemented features. Severity reflects impact on the owner's accounts, customer
privacy, and original media.

---

## 1. Assets to protect

| Asset | Why it matters |
|---|---|
| Original media and Resolve project files | Irreplaceable field footage |
| Customer-identifying footage/photos/notes | Privacy, consent, professional trust |
| Workspace credentials and future OAuth tokens | Account takeover risk |
| SCS campaign/UTM registry integrity | Attribution accuracy and business reporting |
| Publication state truth | Avoiding duplicate or false "published" claims |
| Local SQLite DB and backups | Library integrity and recovery |
| SCS and Sparkling Standard repositories | Must remain untouched |

## 2. Threats, controls, and required tests

| # | Threat | Control requirements | Tests (stage) |
|---|---|---|---|
| T1 | **Credential exposure** (tokens in git, logs, screenshots, errors, backups) | OS credential store/DPAPI only; secrets referenced by key name; redaction in logs/audit/errors; `.gitignore` deny list; pre-commit secret scan in workflow | Secret-scan fixture test; log redaction test; repo staged-file audit (every stage, Stage 0 verified) |
| T2 | **Malicious path traversal** via filenames/metadata/media (e.g. `..\`, absolute paths, reserved names) | Canonicalize and validate every path against configured roots; refuse traversal, symlinks/junctions; sanitize derived filenames; never execute media metadata | Path traversal suite incl. Unicode, long paths, reserved device names (Stage 1) |
| T3 | **Arbitrary file deletion/mutation** | Ingest never deletes or moves sources; writes only inside library root; hard-link only same-volume by explicit config; no `shutil.rmtree` on derived input | File-immutability tests: source hash+mtime unchanged after ingest; no delete API exposed (Stage 1) |
| T4 | **Recursive ingestion loops / junctions** | Non-recursive watch default; ignore reparse points; dedup by content hash; explicit enable for recursion with review | Recursive/linked-folder test; duplicate storm test (Stage 1) |
| T5 | **Large-file / disk exhaustion** | Configurable size cap warning; disk-space preflight; block ingest when free space below threshold; no infinite retries | Huge-file and low-disk simulated tests (Stage 1) |
| T6 | **Stale/compromised OAuth** | `connection_failed` state, no blind retries, re-auth via official flow, scope minimization, disconnect procedure, token expiry visibility | Expired/invalid token tests with mocked provider (Stage 5, if opened) |
| T7 | **Cross-account / cross-workspace publishing** | Workspace isolation of accounts, media roots, campaigns; explicit account confirmation per draft; adapter resolves account from DB, never from request body alone; fail closed | Cross-workspace confusion test (Stage 2/5); authorization-boundary tests |
| T8 | **Unsafe customer footage export** | Publication requires explicit owner approval per variant; PII redaction checklist; exports/downloads treated as security boundaries; no auto-upload to AI/cloud | Approval-gate tests; export review checklist evidence (Stage 2+) |
| T9 | **False reporting** (UI says published when it isn't) | Independent per-destination states; evidence rules for `platform_confirmed`; unknown-on-timeout; no optimistic counters; fixtures labeled | Status-truth tests: draft/private/scheduled never `platform_confirmed` (Stage 2+) |
| T10 | **Unreliable background jobs** (crash mid-ingest/publish) | Durable job rows, idempotency keys, resume-safe ingest, reconciliation, no duplicate public posting on retry | Kill/restart mid-ingest test; ambiguous-timeout reconciliation test (Stage 1/5) |
| T11 | **Supply-chain / dependency risk** | Pin versions; review licenses; no postinstall network surprises; vendor free builds from reputable sources after license review | Dependency audit before adoption (each stage) |
| T12 | **Paid-service leakage** | No paid endpoints, no trial signups, no payment methods; dependency checklist; network egress review for core paths | Cost-audit checklist per stage report |
| T13 | **Prompt/***AI***-induced factual or authorization errors** | AI output is candidate-only; human approval recorded; AI never generates measurements/claims as fact; AI has no publish permission and no shell/SQL/filesystem tools | AI-candidate labeling tests; approval-bypass test (Stage 3+, only if AI used) |
| T14 | **Log/audit data leakage** | Audit payloads redacted; no tokens, no private notes; logs rotate and stay local | Audit redaction test; log inspection (every stage) |
| T15 | **Backup gap / single-disk loss** | Consistent DB backup + manifest export; restore drill; encrypted credential exclusion; unresolved 3-2-1 gap stated honestly | Backup/restore drill (Stage 4) |

## 3. Trust boundaries

- **Loopback boundary:** UI/API on `127.0.0.1`; no remote exposure. Any future remote
  access is a new design review with authentication, not a config toggle.
- **Filesystem boundary:** watched folder (untrusted input surface) → validated ingest →
  library root (trusted managed area) → DB.
- **External publication boundary:** a draft crossing to any platform is an owner-approved
  action with evidence, never an automatic side effect of ingest or approval.
- **AI boundary:** local AI tools are non-authoritative proposers; no tool use against
  accounts, shell, SQL, or filesystem mutation.

## 4. Owner approval requirements

Explicit approval is required for: connecting any account, registering any developer
app/OAuth, sending any media externally, changing loopback exposure, adopting a
dependency with license obligations, enabling recursion/junction handling, and any
migration touching existing data.

## 5. Residual risks accepted for Stage 0

- Documentation claims rest on sources dated 2026-10-03 and may change.
- No automated secret scanning exists yet beyond the manual Stage 0 scan documented in
  `docs/SOURCE_EVIDENCE.md`; a scripted scan is a Stage 1+ deliverable.
- Windows workstation compromise (malware/keylogger) is outside CCC's control; OS-level
  security and backups remain owner responsibilities.
