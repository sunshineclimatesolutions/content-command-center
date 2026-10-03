# Environment and Dependencies — Content Command Center

**Status:** Stage 0.5 research. **No software has been installed, downloaded, or
configured by this project.** Machine identifiers are deliberately minimized in this
public repository; capability classes are published instead of serial numbers, build
numbers, driver strings, free-space decimals, or personal account names.

---

## 1. Operating environment (verified 2026-10-03)

| Component | Observed capability | Notes |
|---|---|---|
| OS | Windows 11 Home, 64-bit, current supported build | Windows-first target confirmed |
| Shell | Windows PowerShell 5.1 (Desktop) | Tooling scripts must stay PS 5.1-compatible |
| Git | 2.55.0.windows.3 | Present |
| GitHub CLI | 2.97.0 | Authenticated as `sunshineclimatesolutions` |
| Node / npm | v24.19.0 / 11.17.0 | Frontend tooling available |
| Python | 3.14.7 (`python`, `py`) | Dependency validation in §2 |
| DaVinci Resolve | Installed v19.0.0.69 at the standard Blackmagic install path; license file present (contents never inspected) | Studio activation is **owner-confirmed, not independently verified** |
| FFmpeg / ffprobe | **Not detected on PATH** | Acquisition plan in §3; installation requires owner authorization |

## 2. Python dependency validation (metadata-level, 2026-10-03)

Checked against the PyPI JSON API for the proposed stack. `requires_python` is a lower
bound; wheel availability for **CPython 3.14 / win_amd64** was checked where a package
ships binary components. This is **metadata validation only — nothing was installed or
imported**.

| Package | Latest at check | `requires_python` | CPython 3.14 win_amd64 wheel | Verdict for Python 3.14.7 |
|---|---|---|---|---|
| `fastapi` | 0.142.2 | `>=3.10` | pure Python (`py3-none-any`) | Compatible |
| `uvicorn` | 0.54.0 | `>=3.10` | pure Python | Compatible. **Propose plain `uvicorn`, not `uvicorn[standard]`**, to avoid binary extras; revisit if performance needs justify them |
| `pydantic` | 2.13.5 | `>=3.9` | pure Python + `pydantic-core` 2.49.0 cp314 wheels | Compatible |
| `httpx` | 0.28.1 | `>=3.8` | pure Python | Compatible (test client) |
| `pytest` | 9.1.1 | `>=3.10` | pure Python | Compatible |
| `alembic` | 1.20.0 | `>=3.10` | pure Python + SQLAlchemy 2.1.3 cp314 wheels | Compatible |
| `python-multipart` | 0.0.32 | `>=3.10` | pure Python | Compatible if upload forms are used |
| `watchdog` | 6.0.0 | `>=3.9` | **No cp314 Windows wheel in the latest release** | **Deferred.** Source install on 3.14 would require a C toolchain; unacceptable risk for Stage 1A. |

**Consequence (ADR-023):** Stage 1A uses a deterministic **standard-library polling
scanner** (`os.scandir` on an interval) instead of `watchdog`. Event-based watching is a
performance shortcut we do not need; the required quiet-period re-scans must happen
regardless. `watchdog` is re-evaluated when it ships cp314 Windows wheels.

Exact versions will be pinned in Stage 1A with a lock/requirements file recorded in the
repository; validation here does not replace an install-and-import test at that gate.

## 3. FFmpeg acquisition plan (proposal; owner authorization required)

FFmpeg/ffprobe provide probing, metadata, thumbnails, and derivative validation. They are
**not currently installed**, and Stage 0.5 does not install them.

### 3.1 Chosen distribution candidate

- **Source:** `BtbN/FFmpeg-Builds` GitHub releases (community build, widely used).
- **Pinned asset:** the latest **`n9.0` Windows x64 LGPL shared** zip,
  `ffmpeg-n9.0-latest-win64-lgpl-shared-9.0.zip`, together with the release
  **`checksums.sha256`** asset. Asset presence was verified via the GitHub API on
  2026-10-03; the exact binary hash must be captured at download time.
- **Why LGPL shared:** avoids GPL components (no libx264/GPL parts), keeps obligations
  minimal, and dynamic linking eases compliance if CCC is ever distributed with FFmpeg.
  We only need probe/thumbnail/decode support; final encoding stays in Resolve.
- **Alternative (only if the BtbN asset is unavailable):** gyan.dev release builds —
  documented at download time; note those default to GPL builds.

### 3.2 Installation method (after approval)

1. Download the pinned zip and `checksums.sha256` over HTTPS to a staging folder.
2. **Verify the SHA-256** of the zip against the published checksum line using
   `Get-FileHash -Algorithm SHA256 <file>`; compare case-insensitively. On any mismatch:
   delete the download, stop, and report.
3. Extract to `%CC_ROOT%\_app\tools\ffmpeg\<pinned-version>\` (app-managed tools
   directory). **Do not modify the system PATH** and do not run an installer or require
   admin rights.
4. Configure CCC with absolute `ffmpeg_path`/`ffprobe_path` settings.
5. Record distribution URL, release tag, asset name, SHA-256, and verification date in
   `docs/SOURCE_EVIDENCE.md`.
6. Smoke test: `ffprobe -version` and probe one synthetic fixture (§4) before use.

Limitation: community build checksums protect against transfer corruption, not against a
compromised upstream. The pinned hash, recorded in-repo, makes later silent substitution
visible; verifying a GPG signature is not available from this source and would require a
different distribution if the owner requires that stronger guarantee.

### 3.3 License obligations

FFmpeg core is LGPL-2.1+ (GPL if GPL parts are enabled — avoided by the LGPL asset). If
CCC is ever distributed to third parties with these binaries, follow the FFmpeg
compliance checklist: dynamic linking, source availability corresponding to the binary,
license notices in documentation/About, and no restriction on reverse engineering for
LGPL components. For purely local internal use, obligations are largely latent, but the
chosen build minimizes them if distribution ever happens.

## 4. Synthetic media policy

- All committed or CI fixtures are **generated at test time** (FFmpeg `lavfi` sources
  such as `testsrc2`, `sine`) into ignored/temporary directories.
- **No binary media is committed.** No customer footage, no real exports, no captured
  production media enters the repository at any stage.
- Fixture generators and their expected properties are versioned (scripts), not the
  outputs.
- Where FFmpeg is unavailable, Stage 1A tests may generate the minimal bytes they need
  programmatically in temp storage, but any parse/validation tests that require a real
  container run only in environments where the verified FFmpeg is present.

## 5. Stage 1 boundaries (no implementation now)

Stage 1 is split into **1A (ingest core, headless)** and **1B (library surface)**, with
an owner review gate between them. Exact scope, exclusions, and pass criteria are in
`docs/ROADMAP.md`. Nothing in this document authorizes installation or coding.

## 6. Residual unknowns

- Resolve Studio activation is owner-stated and not independently verifiable in this
  project.
- FastAPI/uvicorn/pydantic behavior on Python 3.14.7 is validated by metadata and wheel
  availability only, not by a runtime test (that happens under Stage 1A approval).
- Antivirus/EDR interference with watched folders and rapid file writes is untested.
- Exact FFmpeg binary hash cannot be recorded until an approved download occurs.
