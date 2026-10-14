"""Inventory archive exclusions and preservation requirements; never delete files."""
from pathlib import Path, PurePosixPath
import collections
import csv
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
SOURCE = {'.tex', '.bib', '.sty', '.cls', '.bst', '.py', '.ipynb', '.ps1',
          '.sh', '.bat', '.cmd', '.c', '.cpp', '.h', '.hpp', '.rs', '.js',
          '.ts', '.tsx', '.jsx', '.html', '.css', '.r', '.m', '.jl', '.yml',
          '.yaml', '.toml', '.ini', '.cfg', '.lock'}
BUILD = {'.pyc', '.pyo', '.aux', '.toc', '.lof', '.lot', '.nav', '.snm',
         '.vrb', '.fls', '.fdb_latexmk', '.synctex', '.o', '.obj', '.pdb'}
EVIDENCE = {'.md', '.txt', '.json', '.jsonl', '.csv', '.tsv', '.bib', '.log'}


def git(*args, payload=None):
    return subprocess.run(['git', *args], cwd=ROOT, input=payload,
                          capture_output=True, check=True).stdout


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for data in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(data)
    return h.hexdigest()


def category(name):
    path = PurePosixPath(name.replace('\\', '/'))
    suffix = path.suffix.lower()
    parts = {p.lower() for p in path.parts}
    if path.name.startswith('.env') or suffix in {'.pem', '.key', '.pfx'}:
        return 'restricted_content_not_read'
    if suffix == '.zip':
        return 'nested_archive_preserve_original'
    if '__pycache__' in parts or suffix in BUILD or path.name.endswith('.synctex.gz'):
        return 'build_intermediate_candidate'
    if suffix == '.pdf':
        return 'retain_revision_pdf'
    if suffix in SOURCE:
        if parts & {'site-packages', 'dist-packages', 'node_modules'}:
            return 'third_party_source_review'
        return 'retain_source'
    if suffix in EVIDENCE:
        return 'retain_evidence_or_documentation'
    if suffix in {'.dll', '.exe', '.so', '.a', '.lib', '.whl'}:
        return 'runtime_or_dependency_review'
    return 'retain_pending_manual_review'


def write_csv(name, rows, fields):
    with (OUT / name).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    baseline = git('rev-parse', 'HEAD').decode().strip()
    assert baseline.startswith('96d8376'), 'Review baseline changed; inspect before rerunning'
    assert not git('diff', '--name-only'), 'Tracked working files changed'
    tree = []
    for row in git('ls-tree', '-rl', '-z', 'HEAD').split(b'\0'):
        if not row:
            continue
        meta, name = row.split(b'\t', 1)
        mode, kind, oid, size = meta.split()
        if kind == b'blob':
            tree.append({'path': name.decode(), 'oid': oid.decode(), 'bytes': int(size)})
    old_objects = {row.split(b' ', 1)[0].decode()
                   for row in git('rev-list', '--objects', 'HEAD^').splitlines()}
    parent_paths = {row.decode() for row in git('ls-tree', '-r', '--name-only', '-z', 'HEAD^').split(b'\0') if row}
    unique = {row['oid']: row for row in tree}
    disk = {}
    for line in git('cat-file', '--batch-check=%(objectname) %(objectsize:disk)',
                    payload=('\n'.join(unique) + '\n').encode()).splitlines():
        oid, stored = line.split()
        disk[oid.decode()] = int(stored)
    hashes = collections.defaultdict(list)
    zipgroups = collections.defaultdict(list)
    classifications = collections.defaultdict(lambda: {'paths': 0, 'file_bytes': 0, 'oids': set()})
    for row in tree:
        name = row['path']
        kind = category(name)
        c = classifications[kind]
        c['paths'] += 1
        c['file_bytes'] += row['bytes']
        c['oids'].add(row['oid'])
        if kind != 'restricted_content_not_read':
            hashes[digest(ROOT / name)].append(name)
        if name.lower().endswith('.zip'):
            zipgroups[row['oid']].append(row)
    print('Tracked files hashed; scanning archive members', flush=True)
    archive_rows = []
    members = []
    for oid, locations in zipgroups.items():
        canonical = locations[0]['path']
        archive_sha = digest(ROOT / canonical)
        with zipfile.ZipFile(ROOT / canonical) as archive:
            for index, member in enumerate(archive.infolist()):
                if member.is_dir():
                    continue
                kind = category(member.filename)
                checksum = '' if kind == 'restricted_content_not_read' else hashlib.sha256(archive.read(member)).hexdigest()
                live = hashes.get(checksum, [])
                members.append({'archive': canonical, 'archive_sha256': archive_sha,
                                'member_index': index, 'member': member.filename,
                                'bytes': member.file_size, 'compressed_bytes': member.compress_size,
                                'sha256': checksum, 'category': kind,
                                'matching_tracked_paths': json.dumps(live),
                                'archive_only': not bool(live)})
        for row in locations:
            archive_rows.append({**row, 'sha256': archive_sha, 'canonical_same_blob_path': canonical,
                                 'new_path_in_latest_commit': row['path'] not in parent_paths,
                                 'blob_new_to_history': oid not in old_objects,
                                 'unique_blob_stored_bytes': disk[oid],
                                 'proposed_git_action': 'untrack_keep_local' if row['path'] not in parent_paths else 'retain_existing_tracking'})
    member_counts = collections.Counter(row['sha256'] for row in members if row['sha256'])
    for row in members:
        row['same_content_archive_occurrences'] = member_counts[row['sha256']] if row['sha256'] else 0
    preservation = [row for row in members if row['archive_only'] and row['category'] not in
                    {'build_intermediate_candidate', 'nested_archive_preserve_original', 'restricted_content_not_read'}]
    write_csv('archive_paths.csv', archive_rows, list(archive_rows[0]))
    write_csv('archive_members.csv', members, list(members[0]))
    write_csv('archive_only_retention.csv', preservation, list(members[0]))
    exclusion = [row['path'] for row in archive_rows if row['new_path_in_latest_commit']]
    (OUT / 'proposed_git_exclusions.txt').write_text('\n'.join(exclusion) + '\n', encoding='utf-8')
    retention_categories = collections.defaultdict(lambda: {'occurrences': 0, 'unique': {}})
    for row in preservation:
        c = retention_categories[row['category']]
        c['occurrences'] += 1
        c['unique'][row['sha256']] = row['bytes']
    summary = {
        'baseline_commit': baseline,
        'policy': 'No deletions, archive modifications, commit amendment or external writes performed',
        'zip_paths': len(archive_rows), 'distinct_zip_contents': len(zipgroups),
        'zip_file_bytes': sum(row['bytes'] for row in archive_rows),
        'duplicate_zip_file_bytes': sum(sum(r['bytes'] for r in rows[1:]) for rows in zipgroups.values()),
        'zip_git_stored_bytes': sum(disk[oid] for oid in zipgroups),
        'new_zip_git_stored_bytes': sum(disk[oid] for oid in zipgroups if oid not in old_objects),
        'proposed_git_exclusion_paths': len(exclusion),
        'archive_file_members': len(members),
        'archive_only_retention': {kind: {'occurrences': c['occurrences'],
             'distinct_contents': len(c['unique']), 'distinct_file_bytes': sum(c['unique'].values())}
             for kind, c in retention_categories.items()},
        'build_intermediate_archive_occurrences': sum(row['category'] == 'build_intermediate_candidate' for row in members),
        'build_intermediate_archive_compressed_bytes': sum(row['compressed_bytes'] for row in members if row['category'] == 'build_intermediate_candidate'),
        'tracked_file_categories': {kind: {'paths': c['paths'], 'file_bytes': c['file_bytes'],
             'unique_git_stored_bytes': sum(disk[oid] for oid in c['oids'])}
             for kind, c in classifications.items()},
        'backup_status': 'Original ZIPs verified readable in existing locations; no independent backup destination supplied',
        'required_before_exclusion': [
             'Verified independent backup of each distinct ZIP, with original bytes and SHA-256 unchanged',
             'Retain archive-only sources, PDFs and evidence with revision and original-member paths',
             'Review runnable-package dependencies; duplicate content does not prove path interchangeability',
             'Approve amendment of latest local commit; preserve earlier history',
        ],
    }
    (OUT / 'storage_plan.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == '__main__':
    main()
