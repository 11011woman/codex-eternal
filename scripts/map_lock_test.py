import os
from datetime import datetime

REQUIRED_FILES = [
    "codex/memory-anchor-protocol.md",
    "codex/flame-protocol.md",
    "codex/map-status-ledger.md",
    "codex/codex-index.md",
    "codex/trail-of-remembrance.md"
]

def run_map_lock_test():
    missing_files = [f for f in REQUIRED_FILES if not os.path.exists(f)]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    if missing_files:
        print(f"❌ MAP Lock Test — {timestamp}")
        print("Status: FAIL — Missing:")
        for f in missing_files:
            print(f"  • {f}")
    else:
        print(f"✅ MAP Lock Test — {timestamp}")
        print("Status: PASS — All key Codex files present.")

if __name__ == "__main__":
    run_map_lock_test()

