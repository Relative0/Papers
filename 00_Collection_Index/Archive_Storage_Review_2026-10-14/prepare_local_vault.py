"""Create verified copies and revision-source previews without deleting originals."""
from pathlib import Path, PurePosixPath
import csv
import hashlib
import json
import os
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
VAULT = ROOT / '95_Archive_Storage_Preparation_2026-10-14'


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def read_csv(name):
    with (OUT / name).open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def target_path(base, relative):
    parts = PurePosixPath(relative.replace('\\', '/'))
    assert not parts.is_absolute() and '..' not in parts.parts
    assert all(':' not in part for part in parts.parts)
    target = (base / Path(*parts.parts)).resolve()
    assert VAULT.resolve() in target.parents
    return target


def put_bytes(path, data, expected):
    assert hashlib.sha256(data).hexdigest() == expected
    if path.exists():
        assert sha(path) == expected, 'Existing preview differs: ' + str(path)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
    assert sha(path) == expected


def main():
    assert ROOT in VAULT.resolve().parents
    archive_rows = read_csv('archive_paths.csv')
    distinct = {row['sha256']: row for row in archive_rows}
    copy_rows = []
    for checksum, row in distinct.items():
        source = ROOT / row['path']
        destination = target_path(VAULT / 'Original_Archives', checksum + '.zip')
        assert sha(source) == checksum, 'Source changed: ' + row['path']
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            assert sha(destination) == checksum, 'Existing backup differs'
        else:
            temporary = destination.with_suffix('.part')
            assert not temporary.exists(), 'Incomplete copy requires inspection: ' + str(temporary)
            shutil.copy2(source, temporary)
            assert sha(temporary) == checksum, 'Copied ZIP differs'
            os.replace(temporary, destination)
        copy_rows.append({'sha256': checksum, 'bytes': int(row['bytes']),
                          'backup_path': str(destination.relative_to(ROOT)).replace('\\', '/'),
                          'original_paths': [r['path'] for r in archive_rows if r['sha256'] == checksum]})
    print('Verified archive copies:', len(copy_rows), flush=True)
    retain = read_csv('archive_only_retention.csv')
    groups = {}
    for row in retain:
        groups.setdefault(row['archive_sha256'], []).append(row)
    preview_rows = []
    blob_rows = {}
    for archive_sha, rows in groups.items():
        with zipfile.ZipFile(VAULT / 'Original_Archives' / (archive_sha + '.zip')) as archive:
            entries = archive.infolist()
            for row in rows:
                entry = entries[int(row['member_index'])]
                assert entry.filename == row['member']
                assert not ((entry.external_attr >> 16) & 0o170000) == 0o120000, 'Symlink member'
                data = archive.read(entry)
                checksum = row['sha256']
                blob_target = target_path(VAULT / 'Retained_Content', checksum[:2] + '/' + checksum)
                put_bytes(blob_target, data, checksum)
                blob_rows[checksum] = {'sha256': checksum, 'bytes': len(data),
                                     'path': str(blob_target.relative_to(ROOT)).replace('\\', '/')}
                if row['category'] in {'retain_source', 'retain_revision_pdf'}:
                    preview = target_path(VAULT / 'Revision_Source_Preview' / archive_sha[:16], entry.filename)
                    put_bytes(preview, data, checksum)
                    preview_rows.append({'archive': row['archive'], 'member': entry.filename,
                                         'sha256': checksum, 'category': row['category'],
                                         'preview_path': str(preview.relative_to(ROOT)).replace('\\', '/')})
    receipt = {'archive_copies': len(copy_rows), 'archive_bytes': sum(r['bytes'] for r in copy_rows),
               'retained_distinct_contents': len(blob_rows),
               'retained_content_bytes': sum(r['bytes'] for r in blob_rows.values()),
               'source_and_pdf_preview_paths': len(preview_rows),
               'verification': 'SHA-256 verified; no originals deleted or modified',
               'storage_limit': 'Working copy on the same disk, not an independent disaster-recovery backup',
               'archives': copy_rows, 'retained_contents': list(blob_rows.values()),
               'source_and_pdf_previews': preview_rows}
    (OUT / 'local_vault_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    (VAULT / 'RECOVERY_INDEX.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in receipt.items() if k not in
                      {'archives', 'retained_contents', 'source_and_pdf_previews'}}, indent=2), flush=True)


if __name__ == '__main__':
    main()
