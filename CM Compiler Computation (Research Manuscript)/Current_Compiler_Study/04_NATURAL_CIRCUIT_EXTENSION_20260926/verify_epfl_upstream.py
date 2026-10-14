"""Compare the copied original BLIF bytes with the pinned upstream Git tree."""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
from pathlib import Path
import subprocess

from prepare_natural_admission import COMMIT, HERE


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True,
                        help='Local clone of https://github.com/lsils/benchmarks')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'NATURAL_ADMISSION.json').read_text(encoding='utf-8'))
    assert manifest['source_commit'] == COMMIT
    tree = subprocess.check_output(['git', '-C', str(args.repo), 'ls-tree', '-r', COMMIT], text=True)
    entries = {}
    for line in tree.splitlines():
        meta, name = line.split('\t', 1)
        mode, kind, oid = meta.split()
        if kind == 'blob':
            entries[name] = oid
    expected = {d['relative_path']: d['git_blob_sha1'] for d in manifest['designs']}
    actual = {name: oid for name, oid in entries.items()
              if name.endswith('.blif') and name.split('/', 1)[0] in ('arithmetic', 'random_control')}
    assert len(actual) == 20
    assert actual == expected
    for name in ('LICENSE', 'README.md'):
        raw = (HERE / 'epfl_original' / name).read_bytes()
        oid = sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        assert oid == entries[name]
    result = {'status': 'PASS', 'repository': manifest['source_repository'],
              'commit': COMMIT, 'original_blif_count': len(actual),
              'matching_git_blobs': len(actual), 'matching_source_notices': 2}
    (HERE / 'UPSTREAM_VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
