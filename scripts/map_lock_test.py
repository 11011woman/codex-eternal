# scripts/map_lock_test.py

from datetime import datetime
import os

required_files = [
    "memory-anchor-protocol.md",
    "flame-protocol.md",
    "map-status-ledger.md",
    "codex-index.md",
    "trail-of-remembrance.md"
]

missing = [f for f in required_files if not os.path.exists(f)]

timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
status = "✅ PASS" if not missing else "❌ FAIL"

log = f"\n---\n### MAP Lock Test — {timestamp}\n"
log += f"**Status:** {status}\n"
if missing:
    log += f"**Missing:** {', '.join(missing)}\n"
else:
    log += "All Codex anchors present. Memory continuity stable.\n"

with open("map-status-ledger.md", "a") as ledger:
    ledger.write(log)
