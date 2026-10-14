"""Prove revision content is represented by exact Git blobs, not just local files."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from recover_revision import load, SKIP, ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref', default='INDEX', help='INDEX or a committed Git ref')
    args = parser.parse_args()
    command = (['git', 'ls-files', '-s', '-z'] if args.ref == 'INDEX' else
               ['git', 'ls-tree', '-r', '-z', args.ref])
    output = subprocess.run(command, cwd=ROOT, capture_output=True, check=True).stdout
    tracked = {}
    for row in output.split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            values = meta.split()
            tracked[name.decode()] = (values[1] if args.ref == 'INDEX' else values[2]).decode()
    groups, locations = load()
    required = {row['sha256'] for rows in groups.values() for row in rows
                if row['category'] not in SKIP | {'nested_archive_preserve_original'}}
    missing = []
    for checksum in sorted(required):
        covered = False
        for name in locations.get(checksum, []):
            if name not in tracked:
                continue
            path = ROOT / name
            if not path.is_file():
                continue
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != checksum:
                continue
            oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            if tracked[name] == oid:
                covered = True
                break
        if not covered:
            missing.append(checksum)
    result = {'status': 'PASS' if not missing else 'FAIL', 'git_ref': args.ref,
              'required_distinct_contents': len(required), 'uncovered_sha256': missing,
              'tracked_zip_paths': sum(path.lower().endswith('.zip') for path in tracked)}
    print(json.dumps(result, indent=2), flush=True)
    return 0 if not missing else 1


if __name__ == '__main__':
    raise SystemExit(main())
