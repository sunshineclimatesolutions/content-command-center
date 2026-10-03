# No-Cost Policy — Content Command Center

**Status:** Stage 0 policy. Binding for every stage.

**Rule: $0 in new spending.** No new subscriptions, usage-billed APIs, hosting, domains,
paid trials, hardware, or payment-method requirements. A nominal "free tier" is not
treated as unlimited, permanent, or safe to require. Electricity, internet, storage
wear, and owner labor are real existing costs and are never described as free.

---

## 1. Prohibited without explicit owner approval (which must include funding)

- Paid APIs or paid tiers (including X API under current pay-per-use pricing).
- Cloud hosting, object storage/buckets, managed databases, or CI minutes that bill.
- Paid AI inference or cloud transcription; third-party media pipelines (e.g. RunPod,
  OpenAI, Deepgram, Transloadit in the Postiz feature set).
- Domains, tunnels, or services requiring a payment method for a trial.
- Software purchases, license upgrades, or hardware.

## 2. Allowed (existing or genuinely free)

- This Windows PC and its current components.
- Existing DaVinci Resolve installation/license (owner-stated Studio license).
- Existing GitHub account, repository, and free private-repo features.
- Existing social accounts and their free native scheduling tools.
- Free/open-source tools after license review (e.g. FFmpeg, watchdog, whisper.cpp
  optionally) — "free" refers to license/price, while disk, CPU, and owner time remain
  real costs.
- Existing OpenCode access is a pre-existing tool, not approval to incur charges.

## 3. Enforcement per stage

1. Before adding any dependency, answer: price, billing model, license, data sent
   off-machine, and what happens if unavailable. Record in `docs/DECISION_LOG.md`.
2. Never add a required cloud service to a core path. Core works offline.
3. If a capability needs payment, switch to the native/manual route and record the
   limitation honestly.
4. Every stage report includes a cost audit: `$0` or a disclosed violation with cause.
5. No silent trial signup, auto-billing "free credits", or usage-billed endpoint may be
   reachable from CCC code.

## 4. Resource inventory (as measured 2026-10-03)

| Resource | Observed value | Notes |
|---|---|---|
| OS | Windows 11 Home 10.0.26200 (64-bit) | Windows-first target confirmed |
| CPU | AMD Ryzen 7 7735HS, 8 cores / 16 threads | Resolve and local FFmpeg work feasible |
| RAM | 15.2 GB | Adequate for Resolve + local tools; not unlimited |
| GPU | NVIDIA GeForce RTX 4050 Laptop + AMD Radeon iGPU | Resolve acceleration available |
| System disk | `C:` ~633.4 GB free of ~952 GB | Primary candidate for library + DB |
| Other volume | `G:` ~601.7 GB free | Appears to be a **cloud-sync drive** (visible `My Drive`/`Shared drives` folders) — **not counted as local durable storage** |
| Git | 2.55.0.windows.3 | Free, present |
| GitHub CLI | 2.97.0 | Authenticated as `sunshineclimatesolutions` |
| Node | v24.19.0 (npm 11.17.0) | Frontend tooling available |
| Python | 3.14.7 (`python`, `py`) | Proposal targets 3.11+; compatibility check required |
| FFmpeg/ffprobe | **Not detected on PATH** | Stage 1 dependency gap; free install + license review required with owner approval |
| DaVinci Resolve | `C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe` v19.0.0.69; `blackmagic.lic` present (contents not inspected) | Studio activation owner-confirmed, not independently verified |

## 5. Capacity and backup gaps (not hidden)

- Single-machine storage. A true 3-2-1 backup needs an independent device or location;
  if none exists, the gap remains **unresolved** and must be stated rather than papered
  over.
- Media volume will grow; the app must monitor free space and warn early.
- Cloud-sync drives are not a guaranteed backup target and may have data caps or sync
  policies; do not treat `G:` as durable offline storage without owner confirmation and
  a deliberate backup design.
- No printer/scanner/hardware changes are permitted in this project.

## 6. Cost-audit definition for reports

`$0` claims must be supportable: list every service the stage touched, its billing
model, and the evidence that no charge was created. A stage that cannot show this is
reported as a policy violation, not silently accepted.
