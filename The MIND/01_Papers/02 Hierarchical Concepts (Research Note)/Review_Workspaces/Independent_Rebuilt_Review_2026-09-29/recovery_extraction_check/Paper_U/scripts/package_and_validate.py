"""Build a portable recovery archive and verify bytes and nested ZIP integrity."""
from pathlib import Path, PurePosixPath
from io import BytesIO
import hashlib
import json
import platform
import re
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
OUTPUT = BASE / 'Paper_U_Complete_Rebuilt.zip'
EXTRACT = BASE / 'recovery_extraction_check'
SOURCE = next((ROOT / 'original').glob('*.zip'))
PREFIX = 'PAPER_U_INDEPENDENT_REVIEW_HANDOFF_2026-09-29/'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

def safe(name):
    p = PurePosixPath(name.replace('\\', '/'))
    assert not p.is_absolute() and '..' not in p.parts and ':' not in name, name

seen = set()
archives = []
def nested(data, label):
    digest = sha(data)
    if digest in seen:
        return
    seen.add(digest)
    with zipfile.ZipFile(BytesIO(data)) as z:
        assert z.testzip() is None, label
        archives.append({'archive': label, 'sha256': digest, 'entries': len(z.infolist()), 'crc': 'PASS'})
        for info in z.infolist():
            safe(info.filename)
            if info.filename.lower().endswith('.zip'):
                nested(z.read(info), label + ' -> ' + info.filename)

assert sha(SOURCE.read_bytes()) == 'c6adb5f8c5c574a79906aa454d8a5b8c6638aea25a401912bea12aa308186ade'
comparisons = {}
with zipfile.ZipFile(SOURCE) as z:
    for name in ['verification_results.json', 'frontier_groups_m2_d3.csv', 'frontier_groups_m3_d2.csv']:
        current = (ROOT / 'checks/main' / name).read_bytes()
        supplied = z.read(PREFIX + '03_EVIDENCE_AND_REPRODUCIBILITY/supplied_rerun/' + name)
        assert current == supplied, name
        comparisons[name] = 'byte-identical to supplied receipt'
    current = json.loads((ROOT / 'checks/ternary/mixed_ternary_results.json').read_text())
    supplied = json.loads(z.read(PREFIX + '02_INDEPENDENT_REVIEW/tree_review/mixed_ternary_results.json'))
    assert current == supplied
    comparisons['mixed_ternary_results.json'] = 'parsed JSON identical to supplied receipt'
    for local, archived in [
        ('verify_paper_u.py', '03_EVIDENCE_AND_REPRODUCIBILITY/verify_paper_u.py'),
        ('check_mixed_ternary.py', '02_INDEPENDENT_REVIEW/tree_review/check_mixed_ternary.py')]:
        assert (ROOT / 'scripts' / local).read_bytes() == z.read(PREFIX + archived)
        comparisons[local] = 'byte-identical to original script'

nested(SOURCE.read_bytes(), SOURCE.name)
pdf = next((ROOT / 'manuscript').glob('*.pdf'))
reader = PdfReader(pdf)
assert len(reader.pages) == 9
assert all(len(p.extract_text().strip()) > 100 for p in reader.pages)
log = pdf.with_suffix('.log').read_text(encoding='utf-8', errors='replace')
warnings = [line for line in log.splitlines() if re.search(r'Warning:|Overfull|Underfull|^!', line)]
assert not warnings, warnings
dump(ROOT / 'checks/RECOVERY_VALIDATION.json', {
    'review_date': '2026-09-29',
    'provenance': 'Review documents recovered from task record; original lost fresh-review files were unavailable.',
    'python': platform.python_version(),
    'original_source_sha256': sha(SOURCE.read_bytes()),
    'comparison_results': comparisons,
    'main_status': json.loads((ROOT / 'checks/main/verification_results.json').read_text())['status'],
    'ternary_status': current['status'],
    'pdf_pages': len(reader.pages),
    'pdf_sha256': sha(pdf.read_bytes()),
    'final_latex_warnings': warnings,
    'visual_qa': 'All 9 rendered pages inspected by the assistant in this recovery turn; no clipping or overlap observed.',
    'nested_archive_integrity': archives,
    'limits': 'Finite regression checks corroborate proofs; no fresh literature search or historical page inspection during ZIP recovery.'
})

excluded = {'.aux', '.bcf', '.out'}
files = [p for p in sorted(ROOT.rglob('*')) if p.is_file()
         and p.suffix not in excluded and not p.name.endswith('.run.xml')
         and p.name != 'MANIFEST.sha256' and '__pycache__' not in p.parts]
manifest = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in files}
(ROOT / 'MANIFEST.sha256').write_text(''.join(f'{digest}  {name}\n' for name, digest in manifest.items()), encoding='utf-8')
files.append(ROOT / 'MANIFEST.sha256')
assert not OUTPUT.exists(), 'Refusing to overwrite an existing recovery ZIP.'
assert not EXTRACT.exists(), 'Extraction test directory already exists.'
with zipfile.ZipFile(OUTPUT, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in files:
        z.write(p, 'Paper_U/' + p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(OUTPUT) as z:
    assert z.testzip() is None
    names = z.namelist()
    assert len(names) == len(set(names))
    for name in names:
        safe(name)
        target = (EXTRACT / name).resolve()
        assert target.is_relative_to(EXTRACT.resolve())
    z.extractall(EXTRACT)
for name, digest in manifest.items():
    assert sha((EXTRACT / 'Paper_U' / name).read_bytes()) == digest, name
assert (EXTRACT / 'Paper_U/MANIFEST.sha256').read_bytes() == (ROOT / 'MANIFEST.sha256').read_bytes()
receipt = {
    'archive': OUTPUT.name, 'bytes': OUTPUT.stat().st_size,
    'sha256': sha(OUTPUT.read_bytes()), 'files': len(files),
    'crc_test': 'PASS', 'safe_path_test': 'PASS',
    'fresh_extraction': 'PASS', 'extracted_manifest_hashes': 'ALL PASS',
    'unique_nested_zip_archives_verified': len(archives),
    'original_source_archive_unchanged': True,
    'recovery_caveat': 'Fresh-review documents reconstructed from the task record; not a byte-for-byte restoration of lost outputs.'
}
dump(OUTPUT.with_suffix('.receipt.json'), receipt)
OUTPUT.with_suffix('.sha256').write_text(f"{receipt['sha256']}  {OUTPUT.name}\n", encoding='utf-8')
print(json.dumps(receipt, indent=2))
