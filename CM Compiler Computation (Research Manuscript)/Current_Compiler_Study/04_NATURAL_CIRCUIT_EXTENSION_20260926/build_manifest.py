"""Build or verify the content manifest for this local evidence extension."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
MANIFEST = HERE / 'NATURAL_EXTENSION_MANIFEST_SHA256.json'


def inventory():
    rows = []
    for path in sorted(HERE.rglob('*')):
        if not path.is_file() or path == MANIFEST or '__pycache__' in path.parts:
            continue
        blob = path.read_bytes()
        rows.append({'path': path.relative_to(HERE).as_posix(),
                     'sha256': sha256(blob).hexdigest(), 'bytes': len(blob)})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    rows = inventory()
    if args.verify:
        recorded = json.loads(MANIFEST.read_text(encoding='utf-8'))
        if recorded['files'] != rows:
            raise ValueError('natural extension manifest mismatch')
    else:
        result = {'scope': 'All delivered files in this folder except this manifest and Python bytecode.',
                  'files': rows}
        MANIFEST.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(rows)} natural extension files')


if __name__ == '__main__':
    main()
