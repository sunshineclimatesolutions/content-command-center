# Open-Source Evaluation — Content Command Center

**Status:** Stage 0 research. Checked **2026-10-03** unless noted. Nothing here was
locally installed, built, or end-to-end tested; all capability statements are
**DOC CLAIM** from the linked project source unless explicitly marked
**LOCAL VERIFIED** (environment checks only). No paid services are acceptable.

Method: repository metadata verified through the authenticated GitHub API (license,
stars, last push, archive state), plus official project documentation where a claim
matters to integration cost. AGPL/GPL components require owner/legal review before code
reuse or distribution (`LICENSE_DECISION.md`).

---

## 1. Toolchain and media-processing candidates

| Candidate | Source (checked 2026-10-03) | License | Maturity signal (stars / last push) | Prerequisites & resource notes | Windows friction | Verdict |
|---|---|---|---|---|---|---|
| **FFmpeg / ffprobe** | https://ffmpeg.org ; license page https://ffmpeg.org/legal.html | LGPL-2.1+ core; **GPL if GPL parts used** (e.g. libx264); no proprietary relicensing | 64,731 / 2026-10-03 (mirror) | CLI; CPU/RAM for decode/thumbnail work is modest at CCC scale; build matters for license | Official builds via third parties (gyan.dev, BtbN); PATH/config work; **not currently detected on this PC** | **Accept as core dependency candidate** after license review + owner-approved free install in Stage 1 |
| **watchdog** | https://github.com/gorakhargosh/watchdog | Apache-2.0 | 7,423 / 2026-09-22 | Pure Python file-system events; low overhead; Windows ReadDirectoryChangesW backend | Minor: event flakiness on network drives; keep watching local volumes | **Accept** as watcher candidate (still require stability re-scans; never trust events alone) |
| **whisper.cpp** | https://github.com/ggml-org/whisper.cpp | MIT | 54,110 / 2026-10-02 | Local CPU/GPU inference; model files are a separate large download; whisper models have their own license terms | Prebuilt Windows binaries exist; GPU acceleration depends on build | **Defer**: benchmark Resolve Studio's built-in transcription first (Stage 3); add only with measured benefit |
| **Auto-Editor** | https://github.com/WyattBlue/auto-editor | Unlicense | 5,413 / 2026-10-03 | Removes silence; can export a Resolve timeline; CLI | Low; verify output semantics | **Optional Stage 3 candidate** for rough-cut assist after Resolve-native benchmark |
| **AutoClip** | https://github.com/artbyjazi/autoclip | MIT | 161 / 2026-08-01 | Local Whisper + Ollama + auto-crop/captions; pre-1.0 per prior research (not re-verified here) | Requires local LLM runtime and models; quality unproven at scale | **Defer to Stage 3 experiment only**; candidate output never auto-approved |
| **Steezy Clipper** | https://github.com/Steezy-code/clipper | MIT | 5 / 2026-07-11 | Whisper + Qwen/Ollama + OpenCV + FFmpeg pipeline | Very low maturity/adoption | **Reject for now**; recheck only if AutoClip fails and a second experiment is justified |
| **LosslessCut** | https://github.com/mifi/lossless-cut | GPL-2.0 | 44,245 / 2026-09-30 | Standalone GUI trims/cuts; no re-encode by default | Free download; GPL applies to the tool itself, not our code, but does not become a dependency | **Optional owner manual tool**; not a CCC dependency |
| **PySceneDetect** | https://github.com/Breakthrough/PySceneDetect | BSD-3-Clause | 5,217 / 2026-09-21 | Python scene-cut detection; CPU-bound | Low | **Defensive/good**; use only if a concrete segmentation need appears (avoid speculative dependency) |
| **Ollama** | https://github.com/ollama/ollama | MIT | 182,100 / 2026-10-03 | Local LLM runtime; model downloads consume disk; performance depends on GPU/RAM | Windows support exists; VRAM limits | **Optional Stage 3+ candidate** only for local candidate generation; never factual authority |
| **DaVinci Resolve Studio** (existing) | Owner's installed `Resolve.exe` 19.0.0.69 | Proprietary, owner-licensed | LOCAL VERIFIED install; Studio activation owner-confirmed not independently verified | GPU workstation recommended | n/a | **Primary editor**; not OSS; use built-in transcription/reframe before OSS alternatives |

## 2. Publishing/scheduling platforms to evaluate (Stage 5, optional)

| Candidate | Source (checked 2026-10-03) | License | Verified requirements (official docs) | Assessment |
|---|---|---|---|---|
| **Postiz (self-host)** | https://github.com/gitroomhq/postiz-app ; docs: https://github.com/gitroomhq/postiz-docs (configuration reference + providers overview, fetched 2026-10-03) | AGPL-3.0 | Requires **PostgreSQL, Redis, and Temporal** (Temporal since v2.12.0) per official configuration reference; every provider needs **your own registered developer app/OAuth keys**; AI/clipping features require paid third-party keys (OpenAI, RunPod, Deepgram, etc.) that we will not use | **Primary OSS publishing candidate** for a Stage 5 spike. Heavy stack for one user; vendor-cloud social approvals are NOT inherited; resource use must be measured before adoption |
| **TryPost (self-host)** | https://github.com/trypostit/trypost | AGPL-3.0 | README advertises native publishing to 12 platforms + REST/MCP; must independently verify each platform's real developer-app approval and self-host service requirements | **The single alternative** for the Stage 5 comparison. PHP/Laravel stack; no local test yet |
| **Mixpost (Lite)** | https://github.com/inovector/mixpost | MIT core | README describes Lite as a feature-limited version of the commercial Mixpost Pro; Lumite features distinct from Pro | **Limited comparison only**; verify exact Lite connectors before any use; do not assume Pro features |

Rules for Stage 5 (if opened): deploy **one primary + one alternative maximum** in an
isolated environment; mock/dry-run the publisher first; verify which real business
connections can legitimately complete a public post at $0; measure resources and
maintenance; keep native scheduling permanently available. Do not install five
schedulers.

## 3. AGPL / license implications (summary)

- **AGPL-3.0** (Postiz, TryPost): if we modify and run a modified version as a network
  service, §13 requires offering the modified source to users. A private single-user
  local instance is lower risk, but any fork/distribution/hosted use requires legal
  review. Do not copy AGPL code into CCC.
- **MIT/Apache/BSD/Unlicense** candidates are permissive; keep attribution notices.
- **GPL-2.0** (LosslessCut): tool usage is separate from redistribution; do not link its
  code into CCC.
- **FFmpeg**: LGPL-2.1+ by default, GPL if GPL parts are enabled; bundling/distribution
  triggers compliance steps (see legal page fetched 2026-10-03).
- **whisper.cpp**: MIT code, but downloaded model weights carry their own license terms
  that must be reviewed before use.
- **DaVinci Resolve Studio**: proprietary; existing owner license; CCC must not bundle,
  crack, or redistribute it.
- CCC's own license: **pending owner decision** (`LICENSE_DECISION.md`).

## 4. Fit summary per CCC architectural layer

| Layer | Use now | Defer/reject |
|---|---|---|
| File watching | watchdog candidate | — |
| Probe/thumbnail/delivery derivatives | FFmpeg/ffprobe candidate (license + install gate) | — |
| Transcription | Resolve Studio (already owned) | whisper.cpp until measured need |
| Rough-cut/clip assist | none | Auto-Editor/AutoClip/Steezy until Stage 3 benchmark |
| Publishing automation | native schedulers + manual packages | Postiz/TryPost until Stage 5 spike; Mixpost limited check |
| Local LLM | none | Ollama unless a measured local use case exists |

## 5. Evidence integrity notes

- Star counts and push dates fluctuate; they are maturity signals, not quality proof.
- No candidate in this document has been locally executed. Statuses are DOC CLAIM.
- Any future adoption requires a Stage-scoped test with observed results recorded in
  `docs/SOURCE_EVIDENCE.md` and a decision entry in `docs/DECISION_LOG.md`.
