# License Decision — Content Command Center

**Status: PENDING OWNER APPROVAL. No license is assigned to this project.**

## Why there is no LICENSE file

Content Command Center is a private, local-first business tool. Choosing a license for
our own code is a business decision, separate from documenting the licenses of
third-party components we use. This Stage 0 intentionally does **not** auto-assign an
open-source license.

## Third-party license obligations already identified

| Component | License | Obligation summary |
|---|---|---|
| FFmpeg/ffprobe (proposed dependency) | LGPL-2.1+ core; GPL if GPL parts enabled (e.g. libx264) | Compliance required if distributing binaries/linking; see fetched legal page |
| watchdog (proposed) | Apache-2.0 | Attribution/NOTICE |
| whisper.cpp (deferred) | MIT code; model weights separate terms | Attribution; model license review before use |
| Auto-Editor (optional) | Unlicense | Minimal |
| AutoClip / Steezy Clipper (experimental) | MIT | Attribution |
| LosslessCut (optional manual tool) | GPL-2.0 | Tool use separate; do not link into CCC |
| PySceneDetect (optional) | BSD-3-Clause | Attribution |
| Ollama (deferred) | MIT; model licenses separate | Review before use |
| Postiz / TryPost (Stage 5 spike) | AGPL-3.0 | Network-use source disclosure for modified hosted versions; legal review before fork/distribution; do not copy code into CCC |
| Mixpost Lite (limited check) | MIT core; commercial Pro separate | Verify Lite feature set |
| DaVinci Resolve Studio (existing) | Proprietary owner license | Do not bundle, redistribute, or script against terms |
| SCS campaign/UTM content | Business data (read-only import) | Not redistributed; snapshot contains only approved links |

## Decision options for the owner

1. **All Rights Reserved (private tool)** — no public license; simplest for a private
   business application; future Sparkling Standard use is internal.
2. **A permissive license (MIT/Apache-2.0)** — if the owner wants to share reusable,
   non-private portions (e.g. the publisher-adapter contract or ingest safety module).
3. **Defer** — continue private and revisit before any distribution.

## Constraints on any future choice

- Do not place an OSS license on code that embeds AGPL/GPL-derived code without legal
  review.
- Do not accidentally distribute installation-private data, customer media, secrets, or
  SCS private material with any release (see `.gitignore` and `AGENTS.md`).
- Record the final decision in `docs/DECISION_LOG.md`; add the license file only when
  explicitly approved.
