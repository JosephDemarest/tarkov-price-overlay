# Security policy

## Scope

This fork deliberately stays on the screenshot/OCR/log-reading side of the Tarkov integration boundary. Code that reads or writes the game process, injects code, installs a kernel driver, or bypasses BattlEye is out of scope and will not be accepted.

## Automated gates

Every push/PR runs:

- TypeScript/Vite production build.
- Python syntax compilation.
- Rust `cargo check`.
- Static runtime URL allowlist enforcement.
- Static rejection of common process-memory/injection APIs.
- Deterministic CycloneDX SBOM generation.
- High-severity dependency review on pull requests.

Dependabot monitors npm, Cargo, Python, and GitHub Actions dependencies.

## Reporting

Open a private GitHub security advisory for vulnerabilities when available. Do not include secrets, credentials, or private Tarkov/account data in a public issue.

## Release trust

The application intentionally has no background self-updater. Releases should be built from a tagged commit, publish SHA-256 hashes, and attach the CI-generated SBOM. Until that release workflow is established and reviewed, build from source if you require source-to-binary provenance.
