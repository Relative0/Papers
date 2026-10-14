"""Refresh/verify the selected root inventory and natural study packages."""
from __future__ import annotations

import argparse
import csv
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'SOURCE_MANIFEST_SHA256.csv'
FIELDS = ('RelativePath', 'SHA256', 'Bytes')


def desired_paths():
    with MANIFEST.open(newline='', encoding='utf-8') as stream:
        current = {row['RelativePath'] for row in csv.DictReader(stream)}
    current.add('build_source_manifest.py')
    for package in ('03_STUDY_DESIGN_20260926',
                    '04_NATURAL_CIRCUIT_EXTENSION_20260926',
                    '05_NATURAL_TIMING_20260926'):
        current.update(path.relative_to(ROOT).as_posix()
                       for path in (ROOT / package).rglob('*')
                       if path.is_file() and '__pycache__' not in path.parts)
    return sorted(current)


def inventory():
    rows = []
    for relative in desired_paths():
        path = ROOT / relative
        blob = path.read_bytes()
        rows.append({'RelativePath': relative, 'SHA256': sha256(blob).hexdigest(),
                     'Bytes': str(len(blob))})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    rows = inventory()
    if args.verify:
        with MANIFEST.open(newline='', encoding='utf-8') as stream:
            recorded = list(csv.DictReader(stream))
        if rows != recorded:
            raise ValueError('root source manifest differs from current files')
    else:
        with MANIFEST.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
    print(f'PASS: {len(rows)} root manifest entries')


if __name__ == '__main__':
    main()
