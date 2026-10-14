"""Recover an archived revision from ordinary repository files, without ZIP inputs."""
import argparse
import collections
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SKIP = {'build_intermediate_candidate', 'restricted_content_not_read'}


def load():
    groups = collections.defaultdict(list)
    with (HERE / 'ARCHIVE_MEMBER_MAP.csv').open(encoding='utf-8', newline='') as stream:
        for row in csv.DictReader(stream):
            groups[row['archive_sha256']].append(row)
    locations = json.loads((HERE / 'CONTENT_LOCATIONS.json').read_text())
    return groups, locations


def content(row, locations):
    for name in locations.get(row['sha256'], []):
        path = (ROOT / name).resolve()
        assert ROOT in path.parents and '.git' not in path.parts
        if path.is_file():
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() == row['sha256']:
                return data
    raise ValueError('Missing revision content: ' + row['member'])


def safe_target(destination, member):
    parts = PurePosixPath(member.replace('\\', '/'))
    if parts.is_absolute() or '..' in parts.parts or any(':' in part for part in parts.parts):
        raise ValueError('Unsafe member path: ' + member)
    target = (destination / Path(*parts.parts)).resolve()
    if destination not in target.parents:
        raise ValueError('Member escapes output directory')
    return target


def nested_zip(checksum, groups, locations, ancestry=()):
    if checksum in ancestry:
        raise ValueError('Cyclic archive structure')
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for row in groups[checksum]:
            if row['category'] in SKIP:
                continue
            data = (nested_zip(row['sha256'], groups, locations, (*ancestry, checksum))
                    if row['category'] == 'nested_archive_preserve_original' else content(row, locations))
            safe_target(Path('/').resolve(), row['member'])
            archive.writestr(row['member'], data)
    return output.getvalue()


def recover(checksum, destination, groups, locations, restore_nested=False):
    destination = destination.resolve()
    if destination == ROOT or destination == HERE or '.git' in destination.parts:
        raise ValueError('Choose a separate recovery directory')
    count = 0
    for row in groups[checksum]:
        if row['category'] in SKIP:
            continue
        target = safe_target(destination, row['member'])
        if row['category'] == 'nested_archive_preserve_original' and not restore_nested:
            count += recover(row['sha256'], target.with_name(target.name + '.contents'),
                             groups, locations, restore_nested)
            continue
        data = (nested_zip(row['sha256'], groups, locations) if row['category'] ==
                'nested_archive_preserve_original' else content(row, locations))
        if target.exists():
            if target.read_bytes() != data:
                raise ValueError('Refusing to overwrite different output: ' + str(target))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open('xb') as stream:
                stream.write(data)
        count += 1
    return count


def verify_all(groups, locations):
    checked = set()
    for rows in groups.values():
        for row in rows:
            if row['category'] in SKIP | {'nested_archive_preserve_original'}:
                continue
            if row['sha256'] not in checked:
                content(row, locations)
                checked.add(row['sha256'])
    return {'status': 'PASS', 'revision_archives': len(groups), 'distinct_contents': len(checked)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-all', action='store_true')
    parser.add_argument('--archive', help='Full original ZIP SHA-256 from ARCHIVE_INDEX.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--restore-nested-zips', action='store_true',
                        help='Recreate nested ZIPs for tools expecting them; original ZIP hashes will differ')
    args = parser.parse_args()
    groups, locations = load()
    if args.verify_all:
        print(json.dumps(verify_all(groups, locations)))
    else:
        if args.archive not in groups or args.output is None:
            parser.error('Supply a known --archive and a separate --output directory')
        print(json.dumps({'status': 'PASS', 'files_recovered': recover(
            args.archive, args.output, groups, locations, args.restore_nested_zips)}))


if __name__ == '__main__':
    main()
