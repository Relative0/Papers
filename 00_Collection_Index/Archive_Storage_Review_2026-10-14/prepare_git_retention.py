"""Prepare ordinary files to replace archive-only sources, PDFs and evidence."""
from pathlib import Path
import csv
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DEST = ROOT / 'Revision_Preservation_2026-10-14'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def copy(source, target, checksum):
    assert ROOT in source.resolve().parents
    assert DEST.resolve() in target.resolve().parents
    assert digest(source) == checksum
    if target.exists():
        assert digest(target) == checksum
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        assert digest(target) == checksum


def main():
    receipt = json.loads((OUT / 'local_vault_receipt.json').read_text())
    DEST.mkdir(exist_ok=True)
    content_locations = {}
    previews = []
    for row in receipt['source_and_pdf_previews']:
        source = ROOT / row['preview_path']
        tail = source.relative_to(ROOT / '95_Archive_Storage_Preparation_2026-10-14' / 'Revision_Source_Preview')
        target = DEST / 'Sources_and_PDFs' / tail
        copy(source, target, row['sha256'])
        relative = target.relative_to(ROOT).as_posix()
        content_locations.setdefault(row['sha256'], []).append(relative)
        previews.append({**row, 'retained_path': relative})
    for row in receipt['retained_contents']:
        if row['sha256'] in content_locations:
            continue
        target = DEST / 'Evidence_and_Other_Content' / row['sha256'][:2] / row['sha256']
        copy(ROOT / row['path'], target, row['sha256'])
        content_locations[row['sha256']] = [target.relative_to(ROOT).as_posix()]
    member_rows = []
    with (OUT / 'archive_members.csv').open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            checksum = row['sha256']
            if checksum and checksum not in content_locations:
                paths = json.loads(row['matching_tracked_paths'])
                if paths:
                    content_locations[checksum] = paths
            member_rows.append({key: row[key] for key in
                ('archive_sha256', 'member_index', 'member', 'bytes', 'sha256', 'category')})
    with (DEST / 'ARCHIVE_MEMBER_MAP.csv').open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(member_rows[0]))
        writer.writeheader(); writer.writerows(member_rows)
    (DEST / 'CONTENT_LOCATIONS.json').write_text(json.dumps(content_locations, indent=2) + '\n', encoding='utf-8')
    (DEST / 'SOURCE_AND_PDF_INDEX.json').write_text(json.dumps(previews, indent=2) + '\n', encoding='utf-8')
    archive_index = [{'sha256': row['sha256'], 'bytes': row['bytes'],
                      'original_paths': row['original_paths'], 'local_backup_path': row['backup_path']}
                     for row in receipt['archives']]
    (DEST / 'ARCHIVE_INDEX.json').write_text(json.dumps(archive_index, indent=2) + '\n', encoding='utf-8')
    required = {'retain_source', 'retain_revision_pdf', 'retain_evidence_or_documentation',
                'retain_pending_manual_review', 'runtime_or_dependency_review', 'third_party_source_review'}
    checked = 0
    verified = set()
    for row in member_rows:
        if row['category'] not in required:
            continue
        paths = content_locations.get(row['sha256'], [])
        assert paths, 'Missing retained member: ' + row['member']
        if row['sha256'] not in verified:
            assert any((ROOT / path).is_file() and digest(ROOT / path) == row['sha256'] for path in paths)
            verified.add(row['sha256'])
        checked += 1
    result = {'status': 'PASS', 'source_and_pdf_retained_paths': len(previews),
              'archive_member_requirements_verified': checked,
              'distinct_required_contents_verified': len(verified),
              'archive_backups': receipt['archive_copies'],
              'retained_archive_only_distinct_contents': receipt['retained_distinct_contents'],
              'original_archives_modified': False, 'git_history_changed': False}
    (OUT / 'git_retention_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
