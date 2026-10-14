"""Preserve required members recursively, including revisions in nested ZIPs."""
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import zipfile

from review_archive_storage import category, ROOT, OUT

DEST = ROOT / 'Revision_Preservation_2026-10-14'
SKIP = {'build_intermediate_candidate', 'restricted_content_not_read'}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def write_content(data, checksum, archive_sha, name, kind):
    if kind in {'retain_source', 'retain_revision_pdf'}:
        parts = PurePosixPath(name.replace('\\', '/'))
        assert not parts.is_absolute() and '..' not in parts.parts
        assert all(':' not in part for part in parts.parts)
        target = DEST / 'Sources_and_PDFs' / archive_sha[:16] / Path(*parts.parts)
    else:
        target = DEST / 'Evidence_and_Other_Content' / checksum[:2] / checksum
    assert DEST.resolve() in target.resolve().parents
    if target.exists():
        assert sha(target) == checksum
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
    return target.relative_to(ROOT).as_posix()


def main():
    index = json.loads((DEST / 'ARCHIVE_INDEX.json').read_text())
    contexts = {row['sha256']: row for row in index}
    locations = json.loads((DEST / 'CONTENT_LOCATIONS.json').read_text())
    checked_locations = {}
    rows = []
    source_rows = []
    scanned = set()
    unread = []
    added = set()

    def valid_locations(checksum):
        if checksum not in checked_locations:
            checked_locations[checksum] = [path for path in locations.get(checksum, [])
                if (ROOT / path).is_file() and not path.lower().endswith('.zip')
                and sha(ROOT / path) == checksum]
        return checked_locations[checksum]

    def walk(data, archive_sha, parent=None, parent_member=None, depth=0):
        assert depth < 16, 'Inspect unusually deep nesting'
        if archive_sha not in contexts:
            contexts[archive_sha] = {'sha256': archive_sha, 'bytes': len(data),
                'original_paths': [], 'nested_in': []}
        if parent:
            contexts[archive_sha].setdefault('nested_in', []).append(
                {'archive_sha256': parent, 'member': parent_member})
        if archive_sha in scanned:
            return
        scanned.add(archive_sha)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for number, member in enumerate(archive.infolist()):
                if member.is_dir():
                    continue
                kind = category(member.filename)
                if kind == 'restricted_content_not_read':
                    unread.append({'archive_sha256': archive_sha, 'member': member.filename})
                    rows.append({'archive_sha256': archive_sha, 'member_index': number,
                        'member': member.filename, 'bytes': member.file_size,
                        'sha256': '', 'category': kind})
                    continue
                payload = archive.read(member)
                checksum = hashlib.sha256(payload).hexdigest()
                rows.append({'archive_sha256': archive_sha, 'member_index': number,
                    'member': member.filename, 'bytes': member.file_size,
                    'sha256': checksum, 'category': kind})
                if kind == 'nested_archive_preserve_original':
                    walk(payload, checksum, archive_sha, member.filename, depth + 1)
                elif kind not in SKIP:
                    paths = valid_locations(checksum)
                    if not paths:
                        path = write_content(payload, checksum, archive_sha, member.filename, kind)
                        locations[checksum] = [path]
                        checked_locations[checksum] = [path]
                        added.add(checksum)
                    if kind in {'retain_source', 'retain_revision_pdf'}:
                        source_rows.append({'archive_sha256': archive_sha, 'member': member.filename,
                            'sha256': checksum, 'category': kind,
                            'retained_path': checked_locations[checksum][0]})
    for record in index:
        path = ROOT / record['local_backup_path']
        assert sha(path) == record['sha256']
        walk(path.read_bytes(), record['sha256'])
    for checksum, paths in checked_locations.items():
        if paths:
            locations[checksum] = paths
    with (DEST / 'ARCHIVE_MEMBER_MAP.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    for name, value in [('CONTENT_LOCATIONS.json', locations), ('SOURCE_AND_PDF_INDEX.json', source_rows),
                        ('ARCHIVE_INDEX.json', list(contexts.values()))]:
        (DEST / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
    required = [r for r in rows if r['category'] not in SKIP | {'nested_archive_preserve_original'}]
    assert all(valid_locations(row['sha256']) for row in required)
    result = {'status': 'PASS', 'root_archives': len(index), 'distinct_archives_including_nested': len(scanned),
        'all_member_occurrences': len(rows), 'required_member_occurrences': len(required),
        'distinct_required_contents': len({row['sha256'] for row in required}),
        'source_and_pdf_member_occurrences': len(source_rows),
        'additional_preserved_contents': len(added), 'restricted_members_not_read': unread,
        'excluded_member_categories': sorted(SKIP), 'original_zip_files_modified': False}
    (OUT / 'recursive_preservation_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
