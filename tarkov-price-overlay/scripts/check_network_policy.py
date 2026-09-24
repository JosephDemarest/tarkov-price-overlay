"""Static privacy/security policy gate for runtime source."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIRS = [ROOT / "src", ROOT / "python-core", ROOT / "src-tauri"]
ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "api.tarkov.dev",
    "json.tarkov.dev",
    "github.com",
    "paypal.me",
    "qr.kakaopay.com",
    "schema.tauri.app",
}
FORBIDDEN_STRINGS = {
    "api.aquapado.com": "upstream telemetry/control-plane host",
    "ReadProcessMemory": "game/process memory access",
    "WriteProcessMemory": "game/process memory write",
    "CreateRemoteThread": "process injection",
    "VirtualAllocEx": "process injection",
    "NtReadVirtualMemory": "game/process memory access",
    "SetWindowsHookEx": "low-level Windows hook",
}

violations: list[str] = []
url_re = re.compile(r"https?://[^\s\"'<>)}\]]+")

for base in RUNTIME_DIRS:
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".rs", ".ts", ".tsx", ".json", ".toml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        for needle, reason in FORBIDDEN_STRINGS.items():
            if needle in text:
                violations.append(f"{rel}: forbidden {reason}: {needle}")
        for raw in url_re.findall(text):
            host = urlparse(raw.rstrip(".,;")).hostname
            if host and host not in ALLOWED_HOSTS:
                violations.append(f"{rel}: network host not allowlisted: {host}")

if violations:
    print("Privacy/security policy violations:")
    print("\n".join(f" - {v}" for v in violations))
    sys.exit(1)

print("Runtime network/privacy policy OK")
