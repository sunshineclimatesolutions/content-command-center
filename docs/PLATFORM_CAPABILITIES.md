# Platform Capabilities — Content Command Center

**Status:** Stage 0 research, checked **2026-10-03**. Baseline policy: native scheduling
and manual handoff are always available; official API auto-publication is optional and
only with verified zero cost + approvals + live tests.

Status vocabulary: **VERIFIED DOCS** (official source fetched/cited this session) ·
**DOC CLAIM** (project/secondary source only) · **ACCOUNT TESTED** (verified in the real
account with evidence — none yet) · **BLOCKED** · **MANUAL** · **UNKNOWN**.

> **No destination below is connected or tested for the SCS accounts.** Capability is not
> account eligibility. SCS account facts were captured at commit
> `0a38fec0e604dc201df931c50eb980d432a768b2` for Stage 0 and remain valid; the SCS
> default branch has since advanced to `87da9a2887189552c8872339738f526d3132f883`
> (consent-gated first/latest-touch lead-attribution work; the Platform Status Register
> itself is unchanged). CCC must not duplicate SCS lead capture or campaign attribution
> (CCC-REQ-036). See `docs/SOURCE_EVIDENCE.md` §2/§2a.

---

## 1. Master matrix

| Destination | Official publishing API | Approval / eligibility | Cost under $0 policy | Native scheduling / handoff | Final action required | Verification capability | Evidence (accessed 2026-10-03) | Status |
|---|---|---|---|---|---|---|---|---|
| **Facebook Pages** | Graph API `POST /{page-id}/feed`; photos/videos/reels endpoints; `scheduled_publish_time` | Meta app; Page `CREATE_CONTENT` task; `pages_manage_posts` etc.; App Review for Advanced access; app for own Page may use Standard access | $0 (API itself) | Meta Business Suite native scheduling (DOC CLAIM — Meta help center referenced, not independently fetched this session) | Per-permission; native path is manual/scheduled in-platform | `is_published`, post id, read-back via `/{page-id}/feed` | https://developers.facebook.com/docs/pages-api/posts/ ; https://developers.facebook.com/docs/graph-api/reference/page/feed/ | VERIFIED DOCS |
| **Instagram** | Instagram API (Instagram Login) or Instagram API with Facebook Login; `POST /{ig-id}/media`, `/media_publish` | Instagram professional account; `instagram_business_content_publish` / `instagram_content_publish`; App Review for Advanced; app for own business may use Standard | $0 API | Meta Business Suite native scheduling (DOC CLAIM, as above) | Public media URL required (or resumable upload only with Facebook Login for Business); Page Publishing Authorization may apply | Container `status_code`; published media id; `content_publishing_limit` | https://developers.facebook.com/docs/instagram-platform/content-publishing/ ; https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media_publish/ | VERIFIED DOCS |
| **YouTube / Shorts** | Data API `videos.insert` with `status.publishAt` | Google Cloud project + OAuth; **verified API projects created after 2020-07-28 upload private-only until audit** | $0 API; audit required | YouTube Studio native scheduling (official help) | Upload then schedule; unverified projects stay private | Video id + privacy status read-back; public URL | https://developers.google.com/youtube/v3/docs/videos/insert ; https://support.google.com/youtube/answer/1270709 | VERIFIED DOCS |
| **TikTok** | Content Posting API direct post (`video.publish` scope) | Registered app + `video.publish` approval; **unaudited clients restricted to private viewing**; audit to lift | $0 API; audit gate | TikTok Studio native scheduling: **15 minutes to 10 days**; Business/Creator account, desktop | Direct post requires audited app; native Studio path is platform-hosted | `publish_id` status fetch; native path verified in Studio UI | https://developers.tiktok.com/doc/content-posting-api-get-started/ (updated 2026-08-04) ; TikTok business blog | VERIFIED DOCS |
| **Google Business Profile** | Business Profile APIs (local posts) | Google Cloud project + Organization account; **verified active GBP 60+ days + matching website + application approval** (0 QPM = not approved; 300 QPM = approved) | $0 API | Native **Schedule this post** and **Repeats** controls in the profile UI | Manual/native post with scheduling; API requires approval | Live/Pending/Not approved status in UI; API status fields | https://developers.google.com/my-business/content/prereqs ; https://support.google.com/business/answer/7342169 | VERIFIED DOCS |
| **LinkedIn (Company Page)** | Organization Posts via Community Management API | Access request; legal organizations only; business email + verified org; app verified by Page super admin; Development tier then Standard tier screencast review | $0 API | Native Page scheduling/interface (owner operation) | Page does not exist yet for SCS → API path blocked | Post id/read-back if approved | https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review ; SCS Platform Status Register (Page pending) | BLOCKED (no SCS Page); VERIFIED DOCS for requirements |
| **Nextdoor** | Publish API (apply for access; access token) | Application/access required | $0 if granted; native plugin free | **Share Plugin** prepopulates a post; user clicks final publish; also manual post | Plugin/API require user final action | Manual URL evidence; API response if approved | https://developer.nextdoor.com/reference/sharing-introduction | VERIFIED DOCS |
| **Pinterest** | Pins API (authorized apps) | App authorization | $0 API | Native scheduler: **up to 30 days ahead, max 10 future scheduled Pins, one at a time**; media not editable after scheduling | Native scheduling in UI; API if authorized | Scheduled/published state in UI | https://help.pinterest.com/en/business/article/schedule-pins | VERIFIED DOCS |
| **X** | X API v2 (pay-per-use) | Developer account; **no free tier for new signups since 2026-02-06**; prepaid credits | **Not $0**: ~$0.015/post, ~$0.20/post containing a URL | None native beyond manual | Manual publication package only | Manual URL confirmation | docs.x.com pricing (via official pricing summaries, 2026-10) | MANUAL under $0 policy |
| **Yelp** | No general social-feed post API; posts are a paid advertising feature; Data Ingestion API is partner/contract-gated | n/a | n/a | Manual profile upkeep | Manual | Manual | https://docs.developer.yelp.com/docs/data-ingestion-faqs | MANUAL |
| **Gab** | Mastodon-compatible API exists but a paid Pro plan appears required for API access per wrapper documentation | Unclear; likely paid | Suspected paid → not $0 | Manual package | Manual | Manual URL | secondary sources only (gab-api-wrapper docs) | UNKNOWN / MANUALpending official verification |
| **Parler** | No verified official public API documentation found | Unclear | Unknown | Manual package | Manual | Manual URL | no official source located | UNKNOWN / MANUAL |
| **Rumble** | No verified official programmatic publish API found (Ads API is unrelated) | n/a | n/a | Web upload; Shorts rules documented | Manual | Manual URL | https://rumble.support/help/upload-shorts | MANUAL / UNKNOWN for API |
| **Locals** | No verified official publish API found | n/a | n/a | Manual | Manual | Manual URL | none located | UNKNOWN / MANUAL |

## 2. Documented conflicts and cautions

1. **Facebook scheduled window:** the Pages API *posts* guide states `scheduled_publish_time`
   must be between **10 minutes and 30 days**; the Page *feed* reference snippet states
   **10 minutes and 75 days**. Both are official pages. Exact operational window is
   **UNKNOWN pending verification**; Stage 2 must test against the live Page before
   relying on any value.
2. **Instagram posting limit:** the content-publishing guide cites **100 posts/24 h**
   while the media_publish reference cites **50 posts/24 h**. Treat the effective limit as
   account-verified via `GET /{ig-id}/content_publishing_limit`; do not hard-code either.
3. **TikTok window:** TikTok's own materials state **15 minutes–10 days** for normal
   posts; some third-party tools claim longer via their own servers. CCC must not claim
   longer native scheduling.
4. **TikTok business verification ≠ API audit:** SCS business verification is complete
   (owner-confirmed 2026-10-01), but `video.publish` + audit is a separate developer
   process. Never conflate them.
5. **YouTube audit:** an unaudited project's uploads are locked private; a successful
   upload response is NOT a public publication.
6. **Draft upload ≠ published:** TikTok drafts, YouTube private/unlisted, IG containers,
   and native scheduled items are all pre-publication states.
7. **GBP eligibility clock:** 60+ days verified/active plus matching website; the SCS
   profile is owner-confirmed active, but API approval status is untested.
8. **LinkedIn page dependency:** Community Management API requires a Page and an app
   verified by its super admin; the SCS Page is pending, so this path is blocked until
   the owner creates it.

## 3. CCC operating policy derived from this matrix

- **Always available:** Facebook, Instagram, YouTube, TikTok, GBP, Pinterest, Nextdoor
  via native schedulers/Share Plugin/manual packages.
- **Manual only under $0:** X, Yelp, Rumble, Locals, Gab, Parler (and any destination
  whose API terms/cost cannot be verified as free).
- **Optional API adapters (later, per-destination approval):** Facebook Pages,
  Instagram, YouTube, TikTok, GBP, Pinterest, Nextdoor Publish API — each only after
  separate owner approval, developer-app registration, and an end-to-end live test that
  produces a verified public URL without duplicates.
- **Never:** paid API fallback, account-password automation, scraping, CAPTCHA/rate-limit
  bypass, or treating provider acceptance as public confirmation.
- **Not CCC's job:** lead capture, consent storage, and first/latest-touch campaign
  attribution stay in the existing SCS website systems (CCC-REQ-036); CCC imports only
  approved campaign links and records publication proof.

## 4. Required per-destination UI honesty

Each destination view must display: connection status (`not_configured`, `saved`,
`connected`, `connection_failed`, `adapter_not_implemented`, `unavailable`), the route in
use (`native_handoff`, `manual`, `api_public`), the last verified public URL or
owner-reported confirmation, and any known restriction (window, media type, approval).
