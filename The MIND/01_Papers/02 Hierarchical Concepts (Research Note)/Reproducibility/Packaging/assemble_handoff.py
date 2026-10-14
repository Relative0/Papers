"""Assemble and verify the complete, non-destructive Paper U handoff."""
from pathlib import Path
import argparse
import difflib
import hashlib
import json
import re
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive-name', default='PAPER_U_INDEPENDENT_REVIEW_COMPLETE_2026-09-29.zip')
args = parser.parse_args()
if Path(args.archive_name).name != args.archive_name or not args.archive_name.endswith('.zip'):
    parser.error('--archive-name must be a ZIP basename')
PACKAGE = ROOT / 'PAPER_U_INDEPENDENT_REVIEW_HANDOFF_2026-09-29'
ORIGINAL = ROOT / 'PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29'
NAME = 'Paper_U_Resolution_Limited_Ultrametric_Concepts'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

for extension, old_name, new_name in [
    ('tex', f'{NAME}_v0.2.tex', f'{NAME}_v0.3.tex'),
    ('bib', 'paper_u_refs_v0.2.bib', 'paper_u_refs_v0.3.bib'),
]:
    old = (ORIGINAL / '01_CURRENT_MANUSCRIPT' / old_name).read_text(encoding='utf-8').splitlines(keepends=True)
    new = (PACKAGE / '01_CURRENT_MANUSCRIPT' / new_name).read_text(encoding='utf-8').splitlines(keepends=True)
    delta = ''.join(difflib.unified_diff(old, new, fromfile=old_name, tofile=new_name))
    (PACKAGE / '02_INDEPENDENT_REVIEW' / f'v0.2_to_v0.3_{extension}.diff').write_text(delta, encoding='utf-8', newline='\n')

tex = (PACKAGE / '01_CURRENT_MANUSCRIPT' / f'{NAME}_v0.3.tex').read_text(encoding='utf-8')
bib = (PACKAGE / '01_CURRENT_MANUSCRIPT' / 'paper_u_refs_v0.3.bib').read_text(encoding='utf-8')
bbl = (PACKAGE / '01_CURRENT_MANUSCRIPT' / f'{NAME}_v0.3.bbl').read_text(encoding='utf-8')
citations = {key for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}', tex) for key in group.split(',')}
bibkeys = set(re.findall(r'@\w+\{([^,]+),', bib))
bblkeys = set(re.findall(r'\\entry\{([^}]+)\}', bbl))
assert len(citations) == 20 and citations <= bibkeys and citations <= bblkeys
reader = PdfReader(PACKAGE / '01_CURRENT_MANUSCRIPT' / f'{NAME}_v0.3.pdf')
assert len(reader.pages) == 9
text = '\n'.join(page.extract_text() or '' for page in reader.pages)
assert all(token in text for token in ['Definition 10', 'Sections 3.3', '148', 'Routledge', '2018'])
assert '??' not in text
log = (PACKAGE / '03_EVIDENCE_AND_REPRODUCIBILITY' / 'build_logs' / f'{NAME}_v0.3.log').read_text(encoding='utf-8', errors='replace')
assert not re.search(r'LaTeX Warning:|Package .* Warning:|Overfull \\|Underfull \\', log)

# No external source PDFs or page-image exports are distributed.
assert not (PACKAGE / '02_INDEPENDENT_REVIEW' / 'historical_review' / 'evidence').exists()
json_paths = list(PACKAGE.rglob('*.json'))
for path in json_paths:
    json.loads(path.read_text(encoding='utf-8-sig'))

validation = {'status': 'PASS', 'review_date': '2026-09-29', 'pdf_pages': len(reader.pages),
              'cited_keys': sorted(citations), 'all_citations_in_bib_and_bbl': True,
              'final_tex_warnings_or_box_warnings': False, 'json_files_parsed_before_receipt': len(json_paths),
              'external_source_images_distributed': False,
              'original_transfer_zip_sha256': sha(PACKAGE / '04_PRIOR_TRANSFER' / 'PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29.zip'),
              'manuscript_pdf_sha256': sha(PACKAGE / '01_CURRENT_MANUSCRIPT' / f'{NAME}_v0.3.pdf'),
              'manuscript_tex_sha256': sha(PACKAGE / '01_CURRENT_MANUSCRIPT' / f'{NAME}_v0.3.tex')}
(PACKAGE / '03_EVIDENCE_AND_REPRODUCIBILITY' / 'FINAL_VALIDATION.json').write_text(json.dumps(validation, indent=2) + '\n', encoding='utf-8', newline='\n')

manifest_path = PACKAGE / 'MANIFEST_SHA256.json'
files = sorted(p for p in PACKAGE.rglob('*') if p.is_file() and p != manifest_path)
manifest = {p.relative_to(PACKAGE).as_posix(): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in files}
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')

zip_path = ROOT / args.archive_name
if zip_path.exists():
    raise FileExistsError('Refusing to overwrite an existing delivered ZIP')
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in sorted(p for p in PACKAGE.rglob('*') if p.is_file()):
        archive.write(path, arcname=PACKAGE.name + '/' + path.relative_to(PACKAGE).as_posix())

with zipfile.ZipFile(zip_path) as archive:
    assert archive.testzip() is None
    assert len(archive.namelist()) == len(manifest) + 1
    for relative, entry in manifest.items():
        data = archive.read(PACKAGE.name + '/' + relative)
        assert hashlib.sha256(data).hexdigest() == entry['sha256'] and len(data) == entry['bytes']

receipt = {'status': 'PASS', 'archive': zip_path.name, 'bytes': zip_path.stat().st_size,
           'sha256': sha(zip_path), 'manifest_files': len(manifest), 'archive_entries': len(manifest) + 1,
           'all_entries_read_and_hash_verified': True, 'zip_crc_test': 'PASS', 'content_validation': validation,
           'excluded': ['external copyrighted historical-source PDF and rendered pages', 'local scratch files', 'intermediate build artifacts'],
           'complete_prior_transfer_included': True}
zip_path.with_suffix('.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8', newline='\n')
zip_path.with_suffix('.sha256').write_text(f'{receipt["sha256"]}  {zip_path.name}\n', encoding='ascii')
print(json.dumps({'archive': str(zip_path), 'status': 'PASS', 'files': receipt['archive_entries'], 'bytes': receipt['bytes'], 'sha256': receipt['sha256']}, indent=2))
