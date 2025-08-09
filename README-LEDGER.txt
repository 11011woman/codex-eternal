# Dual-Layer MAP Status Ledger

This adds a public heartbeat (**pulse.json** + **status.html**) and a private, lightly-obfuscated ledger (**private/ledger.enc**).

- Public shows: locked/degraded, timestamp, and a short note.
- Private appends: full details (JSON) per test, XOR-obfuscated with a secret key.

> Note: This is *not* strong cryptography. For true privacy, mirror the private ledger to a **private repo** later. This setup keeps operational details out of plain sight while leaving a public signal.

## Files
- `status.html` — human-readable heartbeat page
- `pulse.json` — machine-readable pulse
- `private/ledger.enc` — private append-only log (base64 of XOR-obfuscated JSON)
- `scripts/update_ledger.py` — updates pulse and appends to private log
- `.github/workflows/update-ledger.yml` — manual workflow to update logs

## Setup
1. Add a repo **secret**: `LEDGER_KEY` (any long passphrase).
2. Commit these files.
3. In GitHub → **Actions** → *Update MAP Ledger* → **Run workflow** with your status and notes.

## View
- Public: `/status.html`
- Machine: `/pulse.json`
- Private: `private/ledger.enc` (in the repo). For better secrecy, move to a private repo.

