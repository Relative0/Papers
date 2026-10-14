"""Verify delivered hashes and structural completeness, without changing files."""
from pathlib import Path
import hashlib,json,sys

out=Path(__file__).resolve().parents[1];root=out.parent
required=['PHASE5B_MASTER_REPORT.md','TOOLING_AND_ENVIRONMENT.md','REPRODUCTION_AUDIT.md',
 'INDUSTRIAL_SDD_PIPELINE.md','INCREMENTAL_SAT_PIPELINE.md','VTREE_SEARCH_OBJECTIVES.md',
 'DEFECT_HYPERGRAPH_METHOD.md','BENCHMARK_PROTOCOL.md','BENCHMARK_RESULTS.md',
 'STATISTICAL_ANALYSIS.md','THEOREMS_COUNTEREXAMPLES_AND_PROOFS.md','LITERATURE_PRIORITY_AUDIT.md',
 'HOSTILE_REVIEW_LEDGER.md','THEOREM_STATUS.csv','NEXT_RESEARCH_GATE.md','RESEARCH_LEDGER.md',
 'REPRODUCIBILITY.md','requirements-lock.txt','data/benchmark_manifest.json','data/per_instance_results.csv']
missing=[p for p in required if not (out/p).is_file()]
if missing:raise SystemExit(f'Missing required deliverables: {missing}')
hashfile=root/'SHA256SUMS.txt'
if not hashfile.exists():raise SystemExit('Run this verifier in the extracted final package with root SHA256SUMS.txt')
checked=0
for line in hashfile.read_text(encoding='utf-8').splitlines():
    expected,rel=line.split('  ',1);p=(root/rel).resolve()
    if not p.is_relative_to(root.resolve()):raise SystemExit('Invalid manifest path')
    if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise SystemExit(f'Checksum mismatch: {rel}')
    checked+=1
stats=json.loads((out/'data/statistical_summary.json').read_text())
assert stats['total_trials']==2100 and stats['all_successful_correct']
archive=json.loads((out/'data/archive_integrity.json').read_text())
for r in archive['files']:
    assert hashlib.sha256((root/'continuity_archive'/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
print(json.dumps({'checksummed_files':checked,'required_deliverables':len(required),
                  'principal_trials':stats['total_trials'],'archive_files_unchanged':len(archive['files']),'result':'PASS'},indent=2))
