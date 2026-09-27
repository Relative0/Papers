"""Verify the recovered portable P14 runtime candidate without executing it."""
from hashlib import sha256
import json
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
record = json.loads((HERE/'P14_RUNTIME_RECOVERY.json').read_text(encoding='utf-8'))
bundle = HERE/record['bundle']
assert sha256(bundle.read_bytes()).hexdigest() == record['bundle_sha256']
with ZipFile(bundle) as archive:
    assert set(archive.namelist()) == set(record['members'])
    for name, identity in record['members'].items():
        content = archive.read(name)
        assert len(content) == identity['bytes'] and sha256(content).hexdigest() == identity['sha256'], name
print(f"PASS: {len(record['members'])} portable candidate files; historical execution identity remains open")
