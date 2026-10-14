from __future__ import annotations
import hashlib,json,math,statistics
from collections import defaultdict,Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
PREREG='c91961a3665c2ec0a87b3e7da47c38cd39f5c62def3f68ce911733d1c6621ff8'
HARNESS='2829424b0d70516f10409fc10e04adc3fdf68c01e1f6a1c36a5787401b800d0b'

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def gitblob(p):
    b=Path(p).read_bytes(); return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
def medmap(rows,metric):
    d=defaultdict(list)
    for r in rows: d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}
def ratio(rows,num,den,metric):
    m=medmap(rows,metric); vals=[]
    for c in sorted({r['case_id'] for r in rows}): vals.append(m[(c,num)]/m[(c,den)])
    return gm(vals)

d=json.loads((HERE/'n2_p5_results.json').read_text())
issues=[]
if sha256(HERE/'N2_P5_PREREGISTRATION.md')!=PREREG: issues.append('prereg hash')
if sha256(HERE/'n2_p5_harness.py')!=HARNESS: issues.append('harness hash')
if not d['fuzz']['passed'] or d['fuzz']['failures']: issues.append('fuzz')
expected={'natural_symbolic_rows':40,'natural_lower_timing_rows':750,'natural_pipeline_timing_rows':450,'natural_pipeline_memory_rows':30,
          'gatep_symbolic_rows':144,'gatep_lower_timing_rows':2700,'gatep_pipeline_timing_rows':1620,'gatep_pipeline_memory_rows':108}
counts={k:len(d[k]) for k in expected}
if counts!=expected: issues.append(('row counts',counts))
for k in expected:
    if any(not r.get('ok',True) for r in d[k]): issues.append(('bad row',k))
# Schedule counts.
for prefix,reps,arms in [('natural_lower_timing_rows',25,('direct_packed_sparse_anf','cm_packed_sig_sparse','cm_meta_sig_sparse')),
                         ('natural_pipeline_timing_rows',15,('direct_build_sparse','cm_packed_sig_build_sparse','cm_meta_sig_build_sparse')),
                         ('gatep_lower_timing_rows',25,('direct_packed_sparse_anf','cm_packed_sig_sparse','cm_meta_sig_sparse')),
                         ('gatep_pipeline_timing_rows',15,('direct_build_sparse','cm_packed_sig_build_sparse','cm_meta_sig_build_sparse'))]:
    c=Counter((r['case_id'],r['arm']) for r in d[prefix])
    cases={r['case_id'] for r in d[prefix]}
    for case in cases:
        for arm in arms:
            if c[(case,arm)]!=reps: issues.append(('schedule',prefix,case,arm,c[(case,arm)]))
# Symbolic P5/P4 equivalence and direct-clone identity.
work=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated')
decision=('selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared','selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction','selector_estimated_benefit','selector_estimated_keep_cost','selector_estimated_fold_cost','fold_lowerings','bypassed_child_shells','transpose_alignments')
for key in ('natural_symbolic_rows','gatep_symbolic_rows'):
    by={(r['case_id'],r['arm']):r for r in d[key]}
    for case in sorted({r['case_id'] for r in d[key]}):
        p5=by[(case,'cm_packed_sig_sparse')]; p4=by[(case,'cm_meta_sig_sparse')]; direct=by[(case,'direct_sparse_anf')]; dp=by[(case,'direct_packed_sparse_anf')]
        for f in work+decision:
            if p5.get(f)!=p4.get(f): issues.append(('p5/p4 drift',key,case,f,p5.get(f),p4.get(f)))
        for f in work:
            if direct.get(f)!=dp.get(f): issues.append(('direct drift',key,case,f,direct.get(f),dp.get(f)))
        if p5.get('selector_accepted',0)!=p5.get('fold_lowerings',0): issues.append(('utilization',key,case))
# Frozen natural selection.
case_ids=d['selection']['case_ids']
expected_cases=['adder:f[4]','adder:f[5]','cavlc:17','cavlc:35','int2float:e4','int2float:y6','priority:new_n130','priority:new_n174','router:105','router:92']
if case_ids!=expected_cases: issues.append(('selection',case_ids))
# EPFL blob hashes.
manifest=json.loads((ROOT/'cm_n2_p4_run/EPFL_SOURCE_MANIFEST.json').read_text())
source_ok=True
for rec in manifest['files']:
    p=ROOT/'cm_n2_p4_run/epfl'/rec['file']
    if sha256(p)!=rec['sha256'] or gitblob(p)!=rec['expected_git_blob']: source_ok=False; issues.append(('source',rec['file']))
# Recompute central ratios from raw rows.
calc={
 'gatep_p5_over_direct_lower':ratio(d['gatep_lower_timing_rows'],'cm_packed_sig_sparse','direct_packed_sparse_anf','lower_ns'),
 'gatep_p5_over_direct_pipeline':ratio(d['gatep_pipeline_timing_rows'],'cm_packed_sig_build_sparse','direct_build_sparse','pipeline_ns'),
 'gatep_p5_over_direct_build':ratio(d['gatep_pipeline_timing_rows'],'cm_packed_sig_build_sparse','direct_build_sparse','dag_build_ns'),
 'gatep_p5_over_p4_build':ratio(d['gatep_pipeline_timing_rows'],'cm_packed_sig_build_sparse','cm_meta_sig_build_sparse','dag_build_ns'),
 'natural_p5_over_direct_lower':ratio(d['natural_lower_timing_rows'],'cm_packed_sig_sparse','direct_packed_sparse_anf','lower_ns'),
 'natural_p5_over_direct_pipeline':ratio(d['natural_pipeline_timing_rows'],'cm_packed_sig_build_sparse','direct_build_sparse','pipeline_ns')}
reported={
 'gatep_p5_over_direct_lower':d['gatep']['p5_over_direct:lower_ns']['geomean_ratio'],
 'gatep_p5_over_direct_pipeline':d['gatep']['p5_build_over_direct:pipeline_ns']['geomean_ratio'],
 'gatep_p5_over_direct_build':d['gatep']['p5_build_over_direct:dag_build_ns']['geomean_ratio'],
 'gatep_p5_over_p4_build':d['gatep']['p5_build_over_p4:dag_build_ns']['geomean_ratio'],
 'natural_p5_over_direct_lower':d['natural']['p5_over_direct:lower_ns']['geomean_ratio'],
 'natural_p5_over_direct_pipeline':d['natural']['p5_build_over_direct:pipeline_ns']['geomean_ratio']}
for k in calc:
    if abs(calc[k]-reported[k])>1e-12: issues.append(('ratio',k,calc[k],reported[k]))
out={'status':'PASS' if not issues else 'FAIL','issues':issues,'prereg_sha256':sha256(HERE/'N2_P5_PREREGISTRATION.md'),'harness_sha256':sha256(HERE/'n2_p5_harness.py'),
     'source_manifest_all_verified':source_ok,'row_counts':counts,'all_correct':not any(not r.get('ok',True) for k in expected for r in d[k]),
     'fuzz_passed':d['fuzz']['passed'],'natural_cases':case_ids,'recomputed_ratios':calc,
     'gatep_p5_selector_accepted':d['gatep']['p5_diag']['selector_accepted'],'natural_p5_selector_accepted':d['natural']['p5_diag']['selector_accepted']}
(HERE/'N2_P5_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
