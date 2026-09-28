"""Verify the delivered manifest without modifying artifacts."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'MANIFEST_SHA256.json').read_text())
for item in manifest['files']:
    path = (root / item['path']).resolve()
    assert root in path.parents, item['path']
    assert path.stat().st_size == item['bytes'], item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], item['path']
print(f"PASS: {len(manifest['files'])} manifest entries")
