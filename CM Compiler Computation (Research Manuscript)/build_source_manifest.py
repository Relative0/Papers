"""Refresh or verify the actual current collection's SHA-256 inventory.

Historical paths and earlier manifest versions are preserved in the archive
identified in ARCHIVE_INDEX_2026-10-13.md. The live CSV uses real relative paths.
"""
from pathlib import Path
from hashlib import sha256
import argparse
import csv

ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'SOURCE_MANIFEST_SHA256.csv'
FIELDS=('RelativePath','SHA256','Bytes')

def inventory():
    rows=[]
    for path in sorted(ROOT.rglob('*'),key=lambda p:p.relative_to(ROOT).as_posix()):
        if not path.is_file() or path==MANIFEST or '__pycache__' in path.parts:
            continue
        assert ROOT in path.resolve().parents, 'File escapes collection: '+str(path)
        assert not (path.name.startswith('.env') or path.suffix.lower() in {'.pem','.key','.pfx'}), 'Sensitive file requires explicit authorization'
        digest=sha256()
        with path.open('rb') as stream:
            for block in iter(lambda:stream.read(1024*1024),b''):
                digest.update(block)
        rows.append({'RelativePath':path.relative_to(ROOT).as_posix(),
                     'SHA256':digest.hexdigest(),'Bytes':str(path.stat().st_size)})
    return rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--verify',action='store_true')
    args=parser.parse_args()
    rows=inventory()
    if args.verify:
        with MANIFEST.open(encoding='utf-8-sig',newline='') as stream:
            assert rows==list(csv.DictReader(stream)), 'Manifest differs from current files'
    else:
        with MANIFEST.open('w',encoding='utf-8',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator='\r\n')
            writer.writeheader(); writer.writerows(rows)
    print(f'PASS: {len(rows)} current source manifest entries')

if __name__=='__main__':
    main()
