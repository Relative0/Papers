"""Package only standalone release files, excluding local scratch/extraction trees."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
ARCHIVE = PROJECT/'P01_REVISED_DRAFT_2026-09-26.zip'
PREFIX = 'P01_REVISED_DRAFT_2026-09-26/'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def release_files():
    roots = ['manuscript', 'supplement', 'P01_ASTRA_AUDIT']
    files = [ROOT/name for name in ('README.md','REVISION_RESPONSE.md','LITERATURE_COMPARISON.md')]
    for name in roots:
        files += [p for p in (ROOT/name).rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and 'reproduced' not in p.parts]
    validation = ROOT/'validation'
    for name in ('audit_comparison.json', 'source_integrity.json', 'manuscript_changes.patch',
                 'fresh_checks.log', 'companion_checks.log', 'VISUAL_QA.json',
                 'CLEAN_EXTRACTION.json'):
        if (validation/name).exists():
            files.append(validation/name)
    for p in (validation/'build').rglob('*'):
        if p.is_file() and (p.name == 'build_record.json' or p.suffix in ('.log','.txt','.blg')):
            files.append(p)
    return sorted(set(files))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--extract', action='store_true')
    args=ap.parse_args()
    files=release_files()
    entries=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=digest(p)) for p in files]
    with (ROOT/'MANIFEST_SHA256.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['path','bytes','sha256']);w.writeheader();w.writerows(entries)
    files.append(ROOT/'MANIFEST_SHA256.csv')
    with zipfile.ZipFile(ARCHIVE,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p,PREFIX+p.relative_to(ROOT).as_posix())
    ARCHIVE.with_suffix('.zip.sha256').write_text(digest(ARCHIVE)+'  '+ARCHIVE.name+'\n')
    if args.extract:
        destination=ROOT/'validation/clean_extraction'
        if destination.exists():
            raise FileExistsError('Clean-extraction directory already exists')
        destination.mkdir()
        with zipfile.ZipFile(ARCHIVE) as z:
            for entry in z.infolist():
                target=(destination/entry.filename).resolve()
                if not target.is_relative_to(destination.resolve()):
                    raise ValueError('Unsafe archive path')
            z.extractall(destination)
        print('Extracted: '+str(destination/PREFIX))
    print(f'Packaged {len(files)} files, {ARCHIVE.stat().st_size} bytes: {ARCHIVE}')


if __name__=='__main__':
    main()
