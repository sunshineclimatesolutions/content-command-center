# User Workflows — Content Command Center

**Status:** Stage 0 (planned workflows; no feature below is implemented yet). Every
path in this document is configurable and illustrative. `%CC_ROOT%` is the
owner-selected workspace root; on this machine the audit found `C:` with ~633 GB free
and `G:` with ~602 GB free and **no `D:` drive**, so examples deliberately avoid a
hard-coded `D:` assumption (see `docs/NO_COST_POLICY.md`).

Conventions used below: `SCS` = Sunshine Climate Solutions workspace,
`stage` = the Content Command Center stage number, `PLANNED` = future behavior.

---

## 1. Weekly/monthly planning workflow

**Goal:** know audience, topic, evidence, owning landing page, and one CTA before
filming.

1. Open the current SCS 90-day calendar (read-only snapshot; see §9) and pick the next
   theme.
2. Confirm the audience segment and engine (Residential vs Commercial/TAB) from the SCS
   content operating system.
3. Confirm the owning landing page and exactly one primary CTA. Do not route everything
   to the homepage.
4. Write five candidate hooks and a shot list.
5. Identify any real Field Proof opportunity already scheduled in normal field work.

Effort removed: no re-deciding strategy mid-edit; the composer later offers only the
approved link for that campaign/placement.

## 2. Standardized shoot checklist (per anchor)

- [ ] Wide equipment / environment shot
- [ ] Clean equipment photo
- [ ] Data plate where privacy and safety permit
- [ ] Instrument reading (context visible)
- [ ] Problem area / duct condition
- [ ] Before condition
- [ ] After condition
- [ ] 10–30 s technician explanation
- [ ] Finished workmanship
- [ ] Vertical close-up(s) of gauges/manometers/labels — **never rely on a horizontal
      center crop to preserve readings**
- [ ] Hook module, symptom module, observation/data module, meaning module, next-step
      module (brief pauses between modules)
- [ ] Privacy: no addresses, faces, plates, paperwork, or phone numbers without
      recorded permission

## 3. iPhone transfer workflow (originals preserved)

1. Transfer originals from the iPhone 16 Pro Max over the existing cable/local method to
   a staging folder under `%CC_ROOT%\SCS\00_INBOX\IPHONE_IMPORT\`.
2. Verify copy integrity with the OS or a checksum tool before considering any cleanup.
3. **Do not delete iPhone originals** until the archival copy is verified.
4. Keep HDR/VFR originals untouched; standardize transforms/color consciously on the
   Resolve timeline.
5. Leave transfer staging for the owner to sort by date/concept; CCC does not need to
   ingest camera originals in the first stages (export ingestion is the priority).

## 4. Resolve editing and export workflow

1. Duplicate/reuse Resolve templates: `ANCHOR_16x9`, `SHORT_9x16`, `SQUARE_OPTIONAL`,
   `FIELD_PROOF_9x16`, `THUMBNAIL` — created by the owner inside Resolve Studio
   (existing license). Native Resolve tools (transcription/subtitles, Smart Reframe,
   titles) are used before introducing any third-party assist tool.
2. Export the horizontal master first with clean audio; optionally export an external
   SRT for YouTube.
3. Export genuinely distinct vertical shorts; do not create arbitrary chunks.
4. Export stills/thumbnails as needed.
5. Export target: the watched folder
   `%CC_ROOT%\SCS\00_INBOX\RESOLVE_EXPORTS\`. This is a **landing zone**, not the
   archive.

## 5. Watched-folder ingestion (PLANNED, Stage 1A)

1. Owner renders into the watched folder (Resolve may remain open or be closed later).
2. A standard-library polling scanner (no `watchdog` dependency; see
   [docs/ENVIRONMENT.md](ENVIRONMENT.md)) detects a new file. It is not imported until
   all of these hold:
   - size and mtime are unchanged across the full configurable **quiet period**;
   - `ffprobe` parses it successfully;
   - open/read retries succeed after any Windows sharing violation.
3. **Verified copy only** (no hard links): CCC copies the source into a library staging
   path, then:
   - re-checks that the source size/mtime did not change while copying;
   - computes the destination SHA-256 and verifies it equals the source hash computed
     during the copy;
   - extracts metadata and generates a thumbnail;
   - commits one recoverable database transaction (asset + ingest run).
4. Duplicates are detected by content hash; an existing asset is linked rather than
   re-imported. Deduplication never blocks publishing the same approved material to
   other destinations or at other times (see [docs/DATA_MODEL.md](DATA_MODEL.md) §7).
5. The original export in the landing zone is **never deleted, moved, or modified** by
   CCC.
6. Interrupted copy/import operations resume or restart from a verified checkpoint;
   incomplete staging output is removed only after being proven unusable, and failures
   are visible with error state and retry.
7. **Known limitation:** a writer that pauses longer than the quiet period can appear
   finished. For producers that can emit one, an optional explicit completion signal (a
   sentinel/sidecar file such as `<name>.ccc-ready`) is treated as the authoritative
   completion marker. Filesystem stability alone remains a heuristic; a watcher event is
   never treated as completion.

## 6. Concept grouping (PLANNED)

1. CCC proposes a concept ID from the filename/date; the owner can assign/rename.
2. Owner links master, shorts, stills, thumbnails, SRT, and project reference to the
   concept.
3. Concept status flows: `IDEA → SCRIPTED → FILMED → EDITED → IMPORTED →
   READY_FOR_REVIEW → APPROVED → SCHEDULED → PUBLISHED` (see `docs/DATA_MODEL.md`).
   Per-destination publication states are separate and never inferred from concept
   status.

## 7. Caption/description review workflow (PLANNED)

1. Composer shows one master description and platform tabs (Facebook, Instagram, TikTok,
   YouTube + Shorts, GBP, LinkedIn, Nextdoor, X, others).
2. Each platform draft is independently editable; the app warns about length, media
   format, thumbnail, link, and required settings before approval.
3. Owner reviews facts (measurements with context), CTA, and approved tracked link.
   AI-assisted drafts, if used, are clearly marked as unapproved candidates.
4. Owner explicitly approves each variant. Approval is recorded with actor/time.

## 8. Four-week batching workflow (PLANNED)

1. Prepare concepts and variants for four weeks.
2. Calendar shows per-account coverage and upcoming gaps.
3. Use native schedulers where they exist (see `docs/PLATFORM_CAPABILITIES.md`):
   - Facebook/Instagram: Meta Business Suite native scheduling.
   - YouTube: Studio scheduling (and/or `publishAt` later if an approved API path is
     used).
   - TikTok: TikTok Studio desktop scheduling, 15 minutes to 10 days ahead.
   - Google Business Profile: native Schedule (and Repeats) controls.
   - Pinterest: up to 30 days ahead, max 10 future scheduled Pins (help-center limits).
   - Nextdoor: Share Plugin prepopulates a post; the user clicks final publish.
3. Platforms without an eligible/zero-cost path (for example X under current pay-per-use
   pricing, Yelp, Rumble/Locals, and unverified Gab/Parler routes) get a **manual
   package**: correct export, caption, approved link, target URL, checklist, and a
   reminder.
4. Record for each destination: locally prepared → approved → native-scheduler handoff
   → scheduled on destination → provider-accepted → **public publication verified** or
   **owner-reported manual** (or failed/unknown).
5. A concept is not "fully published" while any selected destination remains incomplete.

## 9. SCS campaign/UTM snapshot workflow (PLANNED, read-only)

1. CCC imports a versioned snapshot of SCS `src/config/marketing-links.ts` output
   (generated CSV/JSON preferred) with source commit SHA and timestamp.
2. Pending links (`pending: true`, e.g. LinkedIn until the Company Page exists) are
   excluded from approved defaults and shown only as unavailable.
3. The owner selects only approved links matching engine/campaign/placement.
4. Freshness warning appears when the snapshot is older than a configurable age or the
   upstream SHA changes.
5. CCC never edits, generates, or deploys SCS website content, and never invents UTM
   parameters.
6. CCC never captures or stores lead attribution. SCS commit
   `87da9a2887189552c8872339738f526d3132f883` introduced consent-gated first/latest-touch
   campaign attribution in lead emails on the website. That system is authoritative;
   CCC must not reproduce it, read its records, or write attribution fields (see
   [docs/SOURCE_EVIDENCE.md](SOURCE_EVIDENCE.md) §2a).

## 10. Publication verification workflow (PLANNED)

| Route | Evidence required to mark `platform_confirmed` |
|---|---|
| Native scheduler | Destination UI acceptance + post URL, owner record |
| Official API with response | Provider response id AND verified public/visibility state where an endpoint allows it |
| API without verification endpoint | Remains `provider_accepted` until owner (or a later read-back) verifies public state |
| Manual | `owner_reported_manual` with timestamp and optional URL — never merged with API-verified |
| Ambiguous API timeout | `unknown`; reconcile before any retry to prevent duplicates |

The app never marks a draft upload, private/unlisted video, container, or scheduled item
as publicly published.

## 11. Exception and recovery workflows (PLANNED)

| Situation | Expected behavior |
|---|---|
| Locked file during render | Retry with backoff; keep job pending; surface error if it persists |
| Corrupted/partial export | Fail validation; do not ingest; keep file in place; visible error |
| Duplicate export | Map to existing asset/version; no duplicate ingest or publication |
| App crash during ingest | Resume or safely redo; no partial DB rows; no source mutation |
| Disk nearly full | Warn at configured threshold; block risky copies; suggest archive/cleanup |
| Link snapshot stale | Warn; require refresh before approving new variants |
| Token expired/invalid (later stages) | Mark connection `connection_failed`; never retry blindly or publish |
| Publication failed | Per-destination failure state with reason; retry only when idempotent/safe |
| Wrong account selected | Workflow requires explicit account confirmation per workspace; isolation enforced |
| Writer pauses long enough to look finished | Sentinel signal (if the producer emits one) wins; otherwise the quiet-period heuristic may import early — recovery removes the incomplete copy and re-imports on owner request |

## 12. Local folder structure (configurable example)

```text
%CC_ROOT%\
  _app\
    db\content.sqlite
    backups\
    logs\                       # no secrets, no customer PII
  SCS\
    00_INBOX\IPHONE_IMPORT\     # transfer staging (originals preserved)
    00_INBOX\RESOLVE_EXPORTS\   # watcher input; never a permanent archive
    2026\2026-10\SCS-2026-10-001-hot-bedroom\
      01_RAW\CAM_A\
      01_RAW\BROLL\
      02_PROJECT\               # .drp and relink notes
      03_TRANSCRIPTS\           # .txt/.srt/.json with review flags
      04_MASTERS\               # pristine 16:9 output
      05_SHORTS\S01\
      05_SHORTS\S02\
      06_STILLS\
      07_SOCIAL_PACKAGES\
      08_PROOF\                 # URLs, acceptance evidence, timestamps
      manifest.json
    _ARCHIVE\
  SPARKLING_STANDARD\...        # separate workspace root and permissions (deferred)
```

Filename policy (illustrative):

- `SCS-20261003-001_hot-bedroom_MASTER_16x9_v01.mp4`
- `SCS-20261003-001_hot-bedroom_SHORT01_9x16_v02.mp4`
- `SCS-20261003-001_hot-bedroom_SHORT01_9x16_v02.srt`
- `SCS-20261003-001_hot-bedroom_SHORT01_THUMB_v01.jpg`

SQLite is the authoritative index; folder paths are convenience. Assets keep stable IDs
and support relinking if folders move.

## 13. User effort removed by each planned automation

| Automation | Manual alternative removed |
|---|---|
| Watched-folder stable ingest | Manually noticing/renaming/copying every render |
| Metadata + thumbnail generation | Opening each file to check specs |
| SHA-256 + dedup | Accidentally importing/re-posting the same render |
| Concept grouping | Hunting files across folders per platform |
| Read-only UTM snapshot | Retyping campaign URLs and risking wrong UTMs |
| Composer variants + approval log | Re-typing captions on every platform site |
| Per-destination calendar | Losing track of which platform got what and when |
| Native handoff packages | Re-deciding export/caption/link/date at upload time |
| Status + proof tracking | Forgetting whether something actually went public |
| Time-per-package metric | Guessing whether a process change helped |
