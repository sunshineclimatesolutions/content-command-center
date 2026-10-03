# Source Evidence Ledger — Content Command Center

**Purpose:** dated provenance for every external claim used in Stage 0 research. This
file records **where** facts came from and **when** they were checked. It is not a
rewrite of third-party content.

**Access date for all entries unless noted:** **2026-10-03**.

---

## 1. Environment evidence (this machine, commands actually run)

| Fact | Command (summary) | Observed result |
|---|---|---|
| OS | `Win32_OperatingSystem` | Windows 11 Home, 64-bit, current supported build (exact build identifier intentionally not published) |
| Shell | `$PSVersionTable` | Windows PowerShell 5.1 (Desktop) |
| Git | `git --version` | 2.55.0.windows.3 |
| GitHub CLI | `gh --version` | 2.97.0 (2026-07-31) |
| GitHub auth | `gh auth status`, `gh api user` | Active account `sunshineclimatesolutions` (public repo owner). Two additional signed-in accounts exist but are inactive and are deliberately not named in this public repository; tokens redacted by `gh` |
| Node/npm | `node --version`, `npm --version` | v24.19.0 / 11.17.0 |
| Python | `python --version`, `py --version` | 3.14.7 (both); `python3` alias absent |
| FFmpeg/ffprobe | `ffmpeg -version`, `Get-Command` | **Not found / not on PATH** |
| DaVinci Resolve | Start Menu shortcut target + FileVersionInfo | Standard Blackmagic install path, product version 19.0.0.69; a license file is present (contents deliberately not inspected); Studio activation is owner-stated and **not independently verified** |
| Hardware | `Win32_Processor/ComputerSystem/VideoController` | 8-core/16-thread AMD Ryzen 7 7000-series; ~16 GB RAM; RTX 4050-class laptop GPU plus integrated graphics (exact identifiers intentionally not published) |
| Disks | `Get-PSDrive` | System volume >500 GB free; second volume is a cloud-sync mount (`My Drive`/`Shared drives` folders observed) and is **not** counted as local durable storage |
| Ancestor repo check | `git rev-parse --show-toplevel` in `C:\Websites` and the handoff folder | Neither is a git repository; project created as a separate folder |
| Git identity | `git config --get user.name/user.email` | Name configured; the personal email is intentionally **not recorded** in this public repository. It remains visible in commit metadata history, which is not rewritten (ADR-017 residual) |
| GitHub branch rules | `gh api .../rulesets`, `.../branches/main/protection` | Stage 0.5 (public repo): rulesets endpoint returns `[]` (HTTP 200) and protection returns 404 "Branch not protected" — protection **is available at $0**, not currently enabled; recommendation in ADR-018. Historical private-repo 403 evidence preserved in ADR-016 |

## 2. SCS repository sources (read-only)

Repository: `sunshineclimatesolutions/Sunshine-Climate-Solutions` (public).
Default branch `main`, resolved HEAD at retrieval:
**`0a38fec0e604dc201df931c50eb980d432a768b2`** (matches the previously reviewed SHA; not
stale at retrieval time). Files fetched via GitHub API
`repos/.../contents/{path}?ref=<sha>` and the corresponding `download_url`.

| File | Blob SHA | Bytes | Key facts used |
|---|---|---|---|
| `AGENTS.md` | `1c9860b17c8f5aed1bd12aa2c38f8464a9986f3f` | 15515 | No new dependencies/databases/paid services without approval; never push without approval; never fabricate business facts |
| `docs/OPERATIONS-HUB.md` | `732c41f8692958ff59edb92bbaf6b104ecfe0506` | 25310 | System map and governance context |
| `docs/operations/PLATFORM-STATUS.md` | `e40e573b0cf4005095b1d56b9b7b71b82e843d1e` | 15922 | Platform register reviewed 2026-10-01: GTM/GA4 operational; GBP active; TikTok business verification complete; 9 social profiles published; UTM registry 60 links/11 QR assets; LinkedIn Page pending |
| `docs/operations/AUTOMATION-REGISTER.md` | `5723ba9fd97defdf12f86260e58fe8df05bbf16d` | 13737 | Automation inventory context |
| `docs/marketing/CONTENT-OPERATING-SYSTEM.md` | `148024cbc33dc1c5b9fa70b5c7548a3a7bbe2aa0` | 27417 | Two engines (Residential vs Commercial/TAB); platform role matrix; atomization model; Field Proof SOP; UTM rules; fundraising separation; realistic weekly ceiling; guardrails |
| `docs/marketing/90-DAY-CONTENT-CALENDAR.csv` | `70dbe8fc5aa8d3203c00a37862ea206fd1d72135` | 9257 | 12-week plan with campaign IDs (`ac_repair`, `airflow`, `maintenance`, `replacement`, `tab_commissioning`, `commercial_hvac`) and status `Not started` |
| `docs/marketing/WEEKLY-MARKETING-SCORECARD.md` | `5ac10e3d380cc00409b78bd378886213b023b78a` | 5064 | KPI fields; lead/revenue primacy; fundraiser kept separate |
| `src/config/marketing-links.ts` | `502a11e65cec66dd0098d5866d9a45a21ce52fd3` | 31419 | `MarketingLink`/`UtmParams` types; `destinations` paths; `pending` flag; generated documents are outputs |
| `docs/marketing/UTM-MASTER-LINKS.md` | `faf7940b22608ade6745f54cb04be3117b602d9d` | 18922 | Generated output (not authoritative) |
| `docs/marketing/WHERE-TO-PASTE-UTM-LINKS.md` | `d03a2ab0629bb9f3ee673c04eabede1fc6a528b2` | 7085 | Owner placement sheet; pending link for LinkedIn |
| `docs/marketing/SOCIAL-PROFILE-SETUP.md` | `942d0260f03c76895a6e28e46bf758d1e23d11e8` | 10194 | Brand block; profile copy; TikTok business verification owner-confirmed; LinkedIn Page pending eligibility rules |
| `docs/GTM-GA4-SETUP.md` | `15d9de7aff70dbeac74aa25482d473c095e8ad46` | 23059 | Events list (`scs_call_click`, `scs_text_click`, `scs_request_click`, `scs_form_start`, `generate_lead`); do not duplicate analytics |

## 2a. SCS reference update (Stage 0.5, 2026-10-03)

The SCS default branch advanced from the Stage 0 snapshot
`0a38fec0e604dc201df931c50eb980d432a768b2` to
**`87da9a2887189552c8872339738f526d3132f883`** (committed 2026-10-03T19:07:08Z):
*"feat: consent-gated first/latest-touch lead attribution (#2)"*.

- The Stage 0 snapshot and blob SHAs in §2 are **preserved as historical evidence** and
  were not rewritten.
- Files changed between the two commits: `AGENTS.md` (rules),
  `docs/marketing/CONTENT-OPERATING-SYSTEM.md` (§12 lead handling), and
  `docs/GTM-GA4-SETUP.md` (attribution documentation). The other nine Stage 0 reference
  files were byte-identical at retrieval.
- New SCS behavior: service-request submissions carry **consent-gated first/latest-touch
  campaign attribution inside lead emails** (lead records only; never analytics), gated
  on analytics consent, 90-day retention, validated campaign tokens. This is
  authoritative SCS functionality.
- **CCC must not duplicate it** (CCC-REQ-036): no lead capture, no consent storage, no
  attribution fields, and no reads of those records. CCC imports only approved campaign
  links read-only and records publication proof.
- Stage 2 freshness checks must compare against `87da9a2` or later.

Secondary (not accessed this session; planning reference only):
`Sparkling-Standard-Cleaning-Co/Sparkling-Standard-Cleaning` — deferred isolation
planning; no private access attempted; no facts asserted.

## 3. External claims with official sources

| Topic | Source URL | Source date/status | Claim recorded in CCC docs |
|---|---|---|---|
| TikTok Content Posting API | https://developers.tiktok.com/doc/content-posting-api-get-started/ | Page "last updated August 4, 2026" | Direct post needs app + `video.publish` approval; **unaudited clients restricted to private viewing**; audit lifts restriction; `FILE_UPLOAD` supported; photo posts need verified domain URL |
| YouTube uploads | https://developers.google.com/youtube/v3/docs/videos/insert | Page "last updated 2026-09-14" | Unaudited projects created after 2020-07-28 upload private-only until audit; quota stated: 100 calls/day in Video Uploads bucket; `status.publishAt` supported |
| YouTube scheduled publishing | https://support.google.com/youtube/answer/1270709 | fetched 2026-10-03 | Videos must be private/scheduled first; scheduling in Studio |
| Google Business Profile API prerequisites | https://developers.google.com/my-business/content/prereqs | Page "last updated 2026-08-28" | Requires verified/active GBP 60+ days + matching website + application approval; 0 QPM vs 300 QPM approval indicator |
| GBP native posts scheduling/Repeats | https://support.google.com/business/answer/7342169 | fetched 2026-10-03 | "Schedule this post" and "Repeats" controls exist; post statuses Live/Pending/Not approved |
| LinkedIn Community Management review | https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review | Page updated 2026-02-11 | Legal organizations only; verified business email/org; Page super admin verifies app; Development then Standard tier screencast review |
| Facebook Pages posts API | https://developers.facebook.com/docs/pages-api/posts/ | official docs via search index; direct fetch blocked (HTTP 400) | `POST /{page-id}/feed`; `pages_manage_posts` + tasks; `scheduled_publish_time` "10 minutes and 30 days" |
| Facebook Page feed reference | https://developers.facebook.com/docs/graph-api/reference/page/feed/ | official docs via search index | States scheduling window "10 minutes and 75 days" — **conflicts with posts guide** |
| Instagram content publishing | https://developers.facebook.com/docs/instagram-platform/content-publishing/ | official docs via search index; direct fetch blocked | Professional account; publish permissions; media must be publicly accessible server (resumable upload only via Facebook Login for Business); PPA possible; limit stated 100/24 h |
| Instagram media publish reference | https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media_publish/ | official docs via search index | States 50 posts/24 h — **conflicts with guide**; PPA + 2FA requirements |
| Pinterest scheduling | https://help.pinterest.com/en/business/article/schedule-pins | fetched 2026-10-03 | Business account; up to 30 days ahead; max 10 future scheduled Pins; one at a time; media not editable after scheduling |
| Nextdoor Share Plugin / Publish API | https://developer.nextdoor.com/reference/sharing-introduction | page updated 2025-06-10 | Publish API requires application/access token; Share Plugin needs no API key and user manually finalizes |
| X API pricing | docs.x.com pricing page (official; surfaced via dated summaries, Sept 2026) | checked 2026-10-03 | Pay-per-use since 2026-02-06; no free tier for new signups; ~$0.015/post, ~$0.20/post with URL; prepaid credits |
| Yelp API scope | https://docs.developer.yelp.com/docs/data-ingestion-faqs | fetched via search index 2026-10-03 | "Posts are a paid advertising feature… not available through the Data Ingestion API"; partner APIs gated |
| Rumble uploads | https://rumble.support/help/upload-shorts | 2026-02-04/2026-05-06 | Manual web upload flow; no official programmatic publish API documented |
| Postiz self-host requirements | https://raw.githubusercontent.com/gitroomhq/postiz-docs/main/self-host/configuration/reference.mdx | fetched 2026-10-03 | Required `DATABASE_URL` (PostgreSQL), `REDIS_URL`, Temporal since v2.12.0; paid AI/transcode keys optional but needed for those features |
| Postiz provider keys | https://raw.githubusercontent.com/gitroomhq/postiz-docs/main/self-host/providers/overview.mdx | fetched 2026-10-03 | Each platform needs your own developer app/OAuth keys; unconfigured platforms appear but fail to connect |
| TryPost capabilities | https://github.com/trypostit/trypost (README) | fetched 2026-10-03 | Self-host; AGPL-3.0; claims 12 native platforms, REST/MCP; cloud separate |
| Mixpost Lite | https://github.com/inovector/mixpost (README) | fetched 2026-10-03 | MIT core; Lite is a feature-limited version of commercial Pro |
| FFmpeg license | https://ffmpeg.org/legal.html | fetched 2026-10-03 | LGPL-2.1+ with optional GPL parts; no proprietary licensing; compliance checklist for linking/distribution |
| OSS metadata | GitHub API `repos/{owner}/{repo}` | 2026-10-03 | Postiz 36,655★/AGPL/2026-10-03; TryPost 668★/AGPL/2026-10-03; Mixpost 3,770★/MIT/2026-03-16; AutoClip 161★/MIT/2026-08-01; Steezy-clipper 5★/MIT/2026-07-11; Auto-Editor 5,413★/Unlicense/2026-10-03; whisper.cpp 54,110★/MIT/2026-10-02; watchdog 7,423★/Apache-2.0/2026-09-22; LosslessCut 44,245★/GPL-2.0/2026-09-30; PySceneDetect 5,217★/BSD-3-Clause/2026-09-21; Ollama 182,100★/MIT/2026-10-03 |
| Python 3.14 dependency validation | PyPI JSON API (`pypi.org/pypi/<pkg>/json`) | 2026-10-03 | FastAPI 0.142.2, Uvicorn 0.54.0, Pydantic 2.13.5 (+ cp314 `pydantic-core` 2.49.0), SQLAlchemy 2.1.3 (cp314 wheels), HTTPX 0.28.1, pytest 9.1.1, Alembic 1.20.0, python-multipart 0.0.32 compatible with CPython 3.14; **watchdog 6.0.0 lacks a cp314 Windows wheel → deferred** (ADR-023) |
| FFmpeg build availability | GitHub API `repos/BtbN/FFmpeg-Builds/releases/latest` | 2026-10-03 | Release `latest` (published 2026-10-03) includes `checksums.sha256` and `ffmpeg-n9.0-latest-win64-lgpl-shared-9.0.zip` (73.6 MB) → chosen candidate (ADR-024); **no download performed** |

## 4. Verification honesty notes

- Direct fetches of Meta developer pages returned HTTP 400 to this tool; the claims above
  were corroborated from the official pages' indexed content and are marked accordingly.
  They remain DOC CLAIM until account-tested.
- No SCS account, social account, or developer app was accessed, connected, or modified.
- No token, cookie, credential, or private customer datum appears in this repository.
- Old zero-cost research referenced by the handoff was read for context and is treated
  as non-authoritative; where it conflicts with verified current sources (e.g. Postiz
  Temporal requirement), the current source and master directive win
  (`docs/DECISION_LOG.md`).
