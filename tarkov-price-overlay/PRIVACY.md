# Privacy and network policy

This fork is intentionally designed to work without analytics or a developer-controlled control plane.

## Removed from upstream

- Anonymous usage telemetry and its durable event queue.
- The persistent machine-wide install UUID stored under `%PROGRAMDATA%\TarkovPriceOverlay\install_id`.
- Remote announcements served by the upstream developer backend.
- In-app feedback uploads, including screenshot attachments.
- Background automatic update checks and the upstream binary updater.

The application does not read Escape from Tarkov process memory, inject DLLs, install a driver, synthesize game input, or modify game files.

## Runtime network allowlist

Background/application data traffic is limited to:

- `127.0.0.1:8765` — the bundled local OCR/data sidecar.
- `api.tarkov.dev` — Tarkov catalog/pricing data.
- `json.tarkov.dev` — fallback Tarkov catalog/pricing data.

Links to GitHub, item wiki pages, PayPal, or KakaoPay are opened only after an explicit user click. The application does not send analytics to those destinations.

## Screen and log access

Item lookup and stash scanning use screenshots captured locally. Normal captures are processed in memory. Setting `TARKOV_DEBUG_CAPTURE=1` explicitly enables local debug-image saving.

Quest synchronization reads Escape from Tarkov log files from the detected/user-selected game directory. It does not write to Tarkov logs.

## Updates

This fork deliberately has no background updater. Use the repository Releases page manually and verify release hashes/provenance before installing.

## CI enforcement

`scripts/check_network_policy.py` scans runtime source on every push/PR. It rejects the removed telemetry host, non-allowlisted hard-coded network hosts, and common process-memory/injection APIs. This is intended to make privacy regressions visible during future upstream merges.
