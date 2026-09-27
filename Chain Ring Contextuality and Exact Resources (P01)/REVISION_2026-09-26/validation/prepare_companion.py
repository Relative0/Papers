"""Preserve exactly the selected source bytes from the user-supplied archive."""
import csv
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
archive = ROOT.parents[1] / 'Chain Ring Process Semantics (Technical Companion).zip'
prefix = 'Chain Ring Process Semantics (Technical Companion)/01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/research_verification_20260921/code/'
target = ROOT / 'supplement/companion_source'
target.mkdir(exist_ok=True)
records = []
with zipfile.ZipFile(archive) as z:
    for name in ('verify_semantics.py', 'test_semantics.py'):
        member = prefix + name
        data = z.read(member)
        local = ROOT.parents[1] / member
        if local.read_bytes() != data:
            raise ValueError('Archive and local companion source differ: ' + member)
        (target / name).write_bytes(data)
        records.append(dict(archive=archive.name, member=member, bytes=len(data),
                            sha256=hashlib.sha256(data).hexdigest(), local_matches_archive=True))
(ROOT / 'supplement/COMPANION_PROVENANCE.json').write_text(json.dumps(records, indent=2)+'\n')
audit = ROOT / 'P01_ASTRA_AUDIT'
with (audit / 'AUDIT_PACKAGE_SHA256.csv').open(newline='', encoding='utf-8') as f:
    entries = list(csv.DictReader(f))
for entry in entries:
    path = audit / entry['path']
    if hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
        raise AssertionError('Audit integrity mismatch: ' + str(path))
if (audit / 'p01_independent_checks.py').read_bytes() != (ROOT / 'supplement/p01_independent_checks.py').read_bytes():
    raise AssertionError('Audit checker copy mismatch')
print(f'Copied 2 unchanged companion sources; verified {len(entries)} audit hashes.')
