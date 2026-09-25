"""Finalize an exact inventory and manifest; independently verify generated metadata."""
import csv
import hashlib
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

checks=json.loads((ROOT/'data'/'review_checks.json').read_text(encoding='utf-8'))
runs=json.loads((ROOT/'data'/'run_record.json').read_text(encoding='utf-8'))
assert checks['status']=='PASS' and runs['status']=='PASS'
assert checks['script_sha256']==sha(ROOT/'code'/'review_checks.py')
assert all(run['exit_code']==0 for run in runs['runs'])
assert len(runs['baseline_files'])==runs['verified_manifest_entries']
assert runs['baseline_unchanged']
base=Path(runs['baseline'])
assert sha(base/'MANIFEST_SHA256.txt')==runs['baseline_manifest_sha256']
for row in runs['baseline_files']:
    assert sha(base/row['path'])==row['sha256']
assert 'Ran 12 tests' in (ROOT/'logs'/'baseline_unit_tests.stderr.txt').read_text(encoding='utf-8')
assert '\nOK\n' in (ROOT/'logs'/'baseline_unit_tests.stderr.txt').read_text(encoding='utf-8')
for name,expected in [('LITERATURE_LEDGER.csv',9),('SEARCH_LOG.csv',26)]:
    with (ROOT/name).open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==expected and all(None not in row for row in rows),name

status='''# Restricted-conversion review — complete

20 September 2026. Read `REVIEW_REPORT.md` first, and `REVIEWED_THEOREMS.md` for the proofs and explicit matrices.

The one-copy Smith filtering theorem, normalizer, fixed-orbit code count and selected contextuality counterexample survive review. The retained-phase multi-copy obstruction strengthens to an exact residue-rank/unit-minor criterion, reducing its novelty weight. An explicit two-copy protocol reaches a single retained-register free target when resolved coefficient measurements precede disposal; the same protocol with outcomes forgotten is mixed.

**Publication decision: no separate fourth full paper. Retain a technical companion.** Exact historical attribution of the ambient-linear stabilizer and the combined operational presentation remains unresolved. Cao's directly relevant 2010 matrix-monoid paper was inspected only at abstract level. These priority limits do not create a proof gap in the supplied self-contained arguments.

Verification passed: 65,536 A matrix classifications; 1,966,080 left/right filter checks; 1,225 order comparisons; exhaustive 65,536-matrix checks over a smaller nonchain ring; a declared 4,096-matrix B_2 sample; exact binary activation/discard checks; the complete baseline checker; and its 12 unit tests. Raw logs and exact inputs are retained. The frozen baseline manifest was checked before and after; original files were not changed.

`MANUSCRIPT_AMENDMENTS.md` is the review addendum to the frozen P03 stub and GO_NO_GO memo. No PDF or new typeset manuscript is claimed. The original broad canonical audit's 31 tests and nine historical manifest discrepancies belong to the previous phase; this review does not claim to rerun or repair them.

No required review work remains. Defer more research until a specific phase-access contract has an operational justification. For that closely related mathematical follow-up, reuse this thread and GPT-6 Astra at high effort; no further thread/model run is needed now. Public release would require reconciling historical provenance and separate authorization.

## Exact inventory

The files below form this review snapshot. SHA256 covers every listed file except the manifest itself. Delivery creates a new `Restricted_Conversion_Review_20260920` subfolder under the requested `Process_Semantics_Research` parent; it refuses to overwrite an existing review. The saved copy procedure checks equality of every file hash.

'''
future={'STATUS.md','ARTIFACT_INVENTORY.txt','MANIFEST_SHA256.txt'}
files=sorted({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}|future)
assert not any('__pycache__' in p for p in files)
(ROOT/'STATUS.md').write_text(status+'\n'.join('- `'+p+'`' for p in files)+'\n',encoding='utf-8')
(ROOT/'ARTIFACT_INVENTORY.txt').write_text('\n'.join(files)+'\n',encoding='utf-8')
manifest=''.join(sha(ROOT/p)+'  '+p+'\n' for p in files if p!='MANIFEST_SHA256.txt')
(ROOT/'MANIFEST_SHA256.txt').write_text(manifest,encoding='utf-8')
actual=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file())
assert actual==files
for line in manifest.splitlines():
    digest,relative=line.split('  ',1)
    assert sha(ROOT/relative)==digest
print(json.dumps({'status':'PASS','files':len(files),'manifest_entries':len(files)-1,
                  'baseline_manifest_entries_unchanged':len(runs['baseline_files']),
                  'source_rows':9,'search_and_route_rows':26},indent=2))
