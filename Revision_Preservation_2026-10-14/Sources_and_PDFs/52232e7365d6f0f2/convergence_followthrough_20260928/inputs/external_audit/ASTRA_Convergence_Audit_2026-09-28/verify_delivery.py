"""Check every file recorded in MANIFEST_SHA256.json without modifying it."""
from pathlib import Path
import hashlib
import json
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'MANIFEST_SHA256.json').read_text(encoding='utf-8'))
    errors = []
    for item in manifest['files']:
        p = (root/item['path']).resolve()
        if not p.is_relative_to(root) or not p.is_file():
            errors.append({'path': item['path'], 'error': 'missing or unsafe'})
        elif p.stat().st_size != item['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != item['sha256']:
            errors.append({'path': item['path'], 'error': 'size or SHA-256 mismatch'})
    print(json.dumps({'status': 'PASS' if not errors else 'FAIL',
                      'files_checked': len(manifest['files']), 'issues': errors}, indent=2))
    return int(bool(errors))

if __name__ == '__main__':
    sys.exit(main())
