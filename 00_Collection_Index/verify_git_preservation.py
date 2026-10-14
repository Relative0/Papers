"""Check retired Git blobs against current files and preservation ZIP members."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def git(*args):
    return subprocess.run(['git', *args], cwd=ROOT, capture_output=True, check=True).stdout


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def main():
    deleted = [s.decode('utf-8') for s in git('diff', '--name-only', '--diff-filter=D', '-z').split(b'\0') if s]
    tree = {}
    for row in git('ls-tree', '-r', '-z', 'HEAD').split(b'\0'):
        if row:
            meta, name = row.split(b'\t', 1)
            tree[name.decode('utf-8')] = meta.split()[2].decode()
    wanted = {tree[p] for p in deleted}
    found = set()
    archives = []
    files = [s.decode('utf-8') for s in git('ls-files', '--cached', '--others', '--exclude-standard', '-z').split(b'\0') if s]
    checked = 0
    for name in sorted(set(files)):
        path = ROOT / name
        if not path.is_file():
            continue
        if path.name.startswith('.env') or path.suffix in ('.pem', '.key'):
            continue
        if path.suffix.lower() == '.zip':
            archives.append(path)
        data = path.read_bytes()
        found.add(blob(data))
        if b'\r\n' in data and b'\0' not in data:
            found.add(blob(data.replace(b'\r\n', b'\n')))
        checked += 1
    archive_members = 0
    corrupt_archives = []
    for path in archives:
        try:
            with zipfile.ZipFile(path) as archive:
                for member in archive.infolist():
                    if member.is_dir():
                        continue
                    data = archive.read(member)
                    found.add(blob(data))
                    if b'\r\n' in data and b'\0' not in data:
                        found.add(blob(data.replace(b'\r\n', b'\n')))
                    archive_members += 1
        except (zipfile.BadZipFile, RuntimeError, OSError) as exc:
            corrupt_archives.append({'path': str(path.relative_to(ROOT)), 'error': str(exc)})
    missing = [p for p in deleted if tree[p] not in found]
    report = {'baseline_commit': git('rev-parse', 'HEAD').decode().strip(),
              'retired_tracked_paths': len(deleted), 'current_files_checked': checked,
              'archives_checked': len(archives), 'archive_members_checked': archive_members,
              'unmatched_retired_paths': missing, 'unreadable_archives': corrupt_archives,
              'status': 'PASS' if not missing and not corrupt_archives else 'FAIL'}
    (ROOT / '00_Collection_Index/GIT_PRESERVATION_CHECK_2026-10-14.json').write_text(
        json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2), flush=True)
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
