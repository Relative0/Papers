"""Verify the final archive and refresh only P01's scoped source manifest."""
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent
archive=PROJECT/'P01_REVISED_DRAFT_2026-09-26.zip'
prefix='P01_REVISED_DRAFT_2026-09-26/'
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:
        raise AssertionError('Archive CRC failure')
    manifest=list(csv.DictReader(io.StringIO(z.read(prefix+'MANIFEST_SHA256.csv').decode())))
    if set(z.namelist()) != {prefix+x['path'] for x in manifest}|{prefix+'MANIFEST_SHA256.csv'}:
        raise AssertionError('Manifest does not cover precisely the archive payload')
    for row in manifest:
        data=z.read(prefix+row['path'])
        if len(data)!=int(row['bytes']) or hashlib.sha256(data).hexdigest()!=row['sha256']:
            raise AssertionError(row['path'])
        if data != (ROOT/row['path']).read_bytes():
            raise AssertionError('Archive/local mismatch: '+row['path'])
    tested=json.loads(z.read(prefix+'validation/CLEAN_EXTRACTION.json'))
    for name, sha in tested['tested_payload_sha256'].items():
        if hashlib.sha256(z.read(prefix+name)).hexdigest()!=sha:
            raise AssertionError('Final archive differs from tested input: '+name)

with (ROOT/'validation/pre_revision_manifest.csv').open(newline='',encoding='utf-8-sig') as f:
    previous=list(csv.DictReader(f))
paths={PROJECT/x['RelativePath'] for x in previous}
paths|={ROOT/x['path'] for x in manifest}
paths|={ROOT/'MANIFEST_SHA256.csv',archive,archive.with_suffix('.zip.sha256')}
with (PROJECT/'SOURCE_MANIFEST_SHA256.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=['RelativePath','SHA256','Bytes'],lineterminator='\n')
    w.writeheader()
    for path in sorted(paths):
        w.writerow(dict(RelativePath=path.relative_to(PROJECT).as_posix(),
                        SHA256=hashlib.sha256(path.read_bytes()).hexdigest(),Bytes=path.stat().st_size))
print(f'PASS: {len(manifest)} archive file hashes, all clean-tested inputs, {len(paths)} scoped project manifest entries.')
print('Archive SHA256: '+hashlib.sha256(archive.read_bytes()).hexdigest())
