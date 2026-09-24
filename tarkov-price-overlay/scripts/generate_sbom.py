"""Generate a small deterministic CycloneDX SBOM from pinned dependency files."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
components: dict[tuple[str, str], dict] = {}

lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
for path, meta in (lock.get("packages") or {}).items():
    if not path.startswith("node_modules/"):
        continue
    name = path[len("node_modules/"):]
    version = meta.get("version")
    if not version:
        continue
    key = ("npm", name)
    components[key] = {
        "type": "library",
        "name": name,
        "version": str(version),
        "purl": f"pkg:npm/{name.replace('@', '%40', 1)}@{version}",
    }

for line in (ROOT / "python-core" / "requirements.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "==" not in line:
        continue
    name, version = line.split("==", 1)
    key = ("pypi", name.lower())
    components[key] = {
        "type": "library",
        "name": name,
        "version": version,
        "purl": f"pkg:pypi/{name}@{version}",
    }

doc = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "version": 1,
    "metadata": {"component": {"type": "application", "name": "tarkov-price-overlay-privacy-fork"}},
    "components": [components[k] for k in sorted(components)],
}
(ROOT / "sbom.cdx.json").write_text(
    json.dumps(doc, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
print(f"Wrote {len(doc['components'])} components to sbom.cdx.json")
