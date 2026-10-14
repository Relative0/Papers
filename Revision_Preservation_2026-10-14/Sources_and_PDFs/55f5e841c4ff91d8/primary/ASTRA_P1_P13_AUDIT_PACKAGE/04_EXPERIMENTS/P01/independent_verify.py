from __future__ import annotations
import json, hashlib, math, statistics
from pathlib import Path
from collections import defaultdict, Counter
R=Path('/mnt/data/cm_n2_p1')
p=json.loads((R/'n2_p1_results.json').read_text())

def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha256(R/'N2_P1_PREREGISTRATION.md')=='ab1f5e6d698b0130c768ef78ac0d1e912af3c19cd3a8c260e90444765a6a6e6a'
assert sha256(R/'n2_p1_harness.py')=='469911b7e6e4a5222aa023dfddbc87e3075bbc5d595f16cc82cc2b7f456ffa5f'
manifest=json.loads((R/'EPFL_SOURCE_MANIFEST.json').read_text()); assert all(x['verified'] for x in manifest['sources'])
ns=p['natural_symbolic_rows']; nt=p['natural_timing_rows']; gs=p['gatep_symbolic_rows']; gt=p['gatep_timing_rows']
assert len(ns)==50 and len(nt)==750 and len(gs)==180 and len(gt)==2880
assert all(r['ok'] for r in ns+nt+gs+gt)
# schedule coverage
arms=p['meta']['protocol']['arms']; natcases=sorted({r['case_id'] for r in nt})
for c in natcases:
    cr=[r for r in nt if r['case_id']==c]
    assert len(cr)==75 and sorted(r['rep'] for r in cr)==list(range(75))
    assert Counter(r['arm'] for r in cr)==Counter({a:15 for a in arms})
# independent median/geomean ratios
def medmap(rows):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r['elapsed_ns'])
    return {k:statistics.median(v) for k,v in d.items()}
def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
def ratio(rows,a,b):
    m=medmap(rows); cs=sorted({r['case_id'] for r in rows}); return gm([m[(c,a)]/m[(c,b)] for c in cs if (c,a) in m and (c,b) in m])
nat_p1_generic=ratio(nt,'cm_profit_sparse','generic_2support_sparse')
nat_p1_direct=ratio(nt,'cm_profit_sparse','direct_sparse_anf')
gate_p1_generic=ratio(gt,'cm_profit_sparse','generic_2support_sparse')
for actual,expected in [(nat_p1_generic,p['summary']['natural_timing']['p1_over_generic_2support_sparse']['geomean_ratio']),
                        (nat_p1_direct,p['summary']['natural_timing']['p1_over_direct_sparse_anf']['geomean_ratio']),
                        (gate_p1_generic,p['summary']['gatep_timing']['p1_over_generic_2support_sparse']['geomean_ratio'])]:
    assert abs(actual-expected)<1e-12,(actual,expected)
# independent symbolic ratios natural p1 vs direct/generic
by={(r['case_id'],r['arm']):r for r in ns}
def symratio(metric,a,b):
    xs=[]
    for c in natcases:
        av,bv=by[(c,a)][metric],by[(c,b)][metric]
        if av>0 and bv>0:xs.append(av/bv)
    return gm(xs)
out={
 'status':'PASS',
 'prereg_sha256':sha256(R/'N2_P1_PREREGISTRATION.md'),
 'harness_sha256':sha256(R/'n2_p1_harness.py'),
 'source_manifest_all_verified':True,
 'row_counts':{'natural_symbolic':len(ns),'natural_timing':len(nt),'gatep_symbolic':len(gs),'gatep_timing':len(gt)},
 'all_correct':True,
 'natural_cases':natcases,
 'natural_p1_over_generic_time':nat_p1_generic,
 'natural_p1_over_direct_time':nat_p1_direct,
 'gatep_p1_over_generic_time':gate_p1_generic,
 'natural_p1_over_generic_python_peak':symratio('python_peak_bytes','cm_profit_sparse','generic_2support_sparse'),
 'natural_p1_over_direct_python_peak':symratio('python_peak_bytes','cm_profit_sparse','direct_sparse_anf'),
 'natural_p1_selector_accepted':p['summary']['p1_selector_natural_totals']['selector_accepted'],
 'gatep_p1_selector_accepted':sum(r['selector_accepted'] for r in gs if r['arm']=='cm_profit_sparse'),
}
(R/'N2_P1_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
