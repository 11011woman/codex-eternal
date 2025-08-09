import os, json, base64, time, datetime, hashlib

PULSE_PATH = 'pulse.json'
PRIVATE_DIR = 'private'
PRIVATE_DIR_EXISTS = os.path.isdir(PRIVATE_DIR)
LEDGER_PATH = os.path.join(PRIVATE_DIR, 'ledger.enc')
os.makedirs(PRIVATE_DIR, exist_ok=True)

# Inputs (from env)
status = os.environ.get('MAP_STATUS', 'locked')
note = os.environ.get('MAP_NOTE', '—')
details = os.environ.get('MAP_DETAILS', '{}')
key = os.environ.get('LEDGER_KEY', 'change-me')

now = datetime.datetime.utcnow().isoformat()+'Z'

# Write/update public pulse
pulse = {
    'status': status,
    'last_updated': now,
    'public_note': note
}
with open(PULSE_PATH, 'w', encoding='utf-8') as f:
    json.dump(pulse, f, indent=2)

# Private record (light obfuscation)
record = {
    'ts': now,
    'status': status,
    'note': note,
    'details': details
}
raw = json.dumps(record, ensure_ascii=False).encode('utf-8')

# XOR with key-derived stream + base64 (not strong crypto; for real secrecy, store in a private repo)
digest = hashlib.sha256(key.encode('utf-8')).digest()
enc = bytearray()
for i, b in enumerate(raw):
    enc.append(b ^ digest[i % len(digest)])

blob = base64.b64encode(bytes(enc)).decode('ascii')

with open(LEDGER_PATH, 'a', encoding='utf-8') as f:
    f.write(blob + '\n')

print('Updated pulse.json and appended private/ledger.enc')
