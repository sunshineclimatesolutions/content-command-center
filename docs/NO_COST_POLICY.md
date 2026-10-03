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

## 4. Resource inventory (verified 2026-10-03, identifiers minimized)

This repository is public, so only capability classes are recorded here. Detailed
dependency validation lives in [docs/ENVIRONMENT.md](ENVIRONMENT.md).

| Resource | Capability observed | Notes |
|---|---|---|
| OS | Windows 11 Home, 64-bit, current supported build | Windows-first target confirmed |
| CPU | 8-core / 16-thread AMD Ryzen 7 (7000 series) | Resolve and local FFmpeg work feasible |
| RAM | ~16 GB | Adequate for Resolve + local tools; not unlimited |
| GPU | NVIDIA RTX 4050-class laptop GPU + integrated graphics | Resolve acceleration available |
| Local storage | System volume with >500 GB free; a second volume is a cloud-sync mount | Adequate for Stage 1A; the cloud mount is **not** counted as durable local storage |
| Tooling | Git 2.55, GitHub CLI 2.97 (authenticated), Node 24 / npm 11, Python 3.14.7 | Existing/free |
| FFmpeg/ffprobe | **Not detected on PATH** | Acquisition, license, and checksum procedure in [docs/ENVIRONMENT.md](ENVIRONMENT.md) §3; owner authorization required |
| DaVinci Resolve | Installed v19.0.0.69 at the standard install path; license file present (contents not inspected) | Studio activation owner-confirmed, not independently verified |

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
