"""Record completed original-suite rerun and input integrity; no tests are rerun."""
import hashlib
import json
import platform
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT / 'PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29'
RERUN = ROOT / 'reproducibility' / 'supplied_rerun'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

entries = []
for line in (ORIGINAL / 'MASTER_MANIFEST_SHA256.txt').read_text().splitlines():
    expected, relative = line.split('  ', 1)
    actual = sha(ORIGINAL / relative)
    entries.append({'path': relative, 'expected': expected, 'actual': actual, 'match': expected == actual})
assert len(entries) == 40 and all(x['match'] for x in entries)

comparisons = []
for name in ['verification_results.json', 'frontier_groups_m2_d3.csv', 'frontier_groups_m3_d2.csv']:
    a = ORIGINAL / '03_EVIDENCE_AND_REPRODUCIBILITY' / 'evidence' / name
    b = RERUN / name
    row = {'file': name, 'original_sha256': sha(a), 'rerun_sha256': sha(b), 'byte_identical': a.read_bytes() == b.read_bytes(),
           'identical_after_crlf_to_lf': a.read_bytes().replace(b'\r\n', b'\n') == b.read_bytes().replace(b'\r\n', b'\n')}
    if name.endswith('.json'):
        row['parsed_json_equal'] = json.loads(a.read_text()) == json.loads(b.read_text())
        assert row['parsed_json_equal']
    assert row['identical_after_crlf_to_lf']
    comparisons.append(row)

result = {'review_date': '2026-09-29', 'python': platform.python_version(), 'platform': platform.platform(),
          'input_manifest': entries,
          'original_script_sha256': sha(ORIGINAL / '03_EVIDENCE_AND_REPRODUCIBILITY' / 'scripts' / 'verify_paper_u.py'),
          'original_transfer_zip_sha256': sha(ROOT / 'PAPER_U_INDEPENDENT_REVIEW_HANDOFF_2026-09-29' / '04_PRIOR_TRANSFER' / 'PAPER_U_GPT_ACCOUNT_TRANSFER_MASTER_2026-09-29.zip'),
          'output_comparisons': comparisons,
          'command': 'python <prior-transfer>/03_EVIDENCE_AND_REPRODUCIBILITY/scripts/verify_paper_u.py --out <review>/reproducibility/supplied_rerun',
          'suite_result': json.loads((RERUN / 'verification_results.json').read_text()),
          'qualification': 'Same original program rerun; not an independent implementation. JSON differs only by Windows CRLF versus original LF. CSV files match byte-for-byte. Independently authored targeted checks are in tree_review.'}
(ROOT / 'reproducibility' / 'REPRODUCTION_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps({'input_manifest_entries': len(entries), 'integrity': 'PASS', 'comparisons': comparisons}, indent=2))
