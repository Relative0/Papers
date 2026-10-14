from __future__ import annotations
import hashlib,json,math,statistics
from collections import defaultdict,Counter
from pathlib import Path
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
PREREG='eb581a115b6d5a8214787d642d9ea496e8b6f9cb2439e9973017c083bf11ff9a'
HARNESS='07e8b2983a19dd5acbacfa2ab58bbb19180bd2b98f15487c1bbfe155f7a03659'

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def gitblob(p):
    b=Path(p).read_bytes(); return hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()
def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
def medmap(rows,metric):
    d=defaultdict(list)
    for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
    return {k:statistics.median(v) for k,v in d.items()}
def ratio(rows,num,den,metric):
    m=medmap(rows,metric); vals=[]
    for c in sorted({r['case_id'] for r in rows}): vals.append(m[(c,num)]/m[(c,den)])
    return gm(vals)

d=json.loads((HERE/'n2_p7_results.json').read_text()); issues=[]
if sha256(HERE/'N2_P7_PREREGISTRATION.md')!=PREREG: issues.append('prereg hash')
if sha256(HERE/'n2_p7_harness.py')!=HARNESS: issues.append('harness hash')
if not d['fuzz']['passed'] or d['fuzz']['failures']: issues.append('fuzz')
expected={'natural_symbolic_rows':50,'natural_lower_timing_rows':1000,'natural_pipeline_timing_rows':600,'natural_pipeline_memory_rows':40,
          'gatep_symbolic_rows':180,'gatep_lower_timing_rows':3600,'gatep_pipeline_timing_rows':2160,'gatep_pipeline_memory_rows':144}
counts={k:len(d[k]) for k in expected}
if counts!=expected: issues.append(('row counts',counts))
for k in expected:
    if any(not r.get('ok',True) for r in d[k]): issues.append(('bad row',k))
for key,reps,arms in [
 ('natural_lower_timing_rows',25,('direct_cword_sparse_anf','cm_cword_sig_sparse','cm_innode_sig_sparse','cm_packed_sig_sparse')),
 ('natural_pipeline_timing_rows',15,('direct_build_sparse','cm_cword_sig_build_sparse','cm_innode_sig_build_sparse','cm_packed_sig_build_sparse')),
 ('gatep_lower_timing_rows',25,('direct_cword_sparse_anf','cm_cword_sig_sparse','cm_innode_sig_sparse','cm_packed_sig_sparse')),
 ('gatep_pipeline_timing_rows',15,('direct_build_sparse','cm_cword_sig_build_sparse','cm_innode_sig_build_sparse','cm_packed_sig_build_sparse'))]:
    c=Counter((r['case_id'],r['arm']) for r in d[key]); cases={r['case_id'] for r in d[key]}
    for case in cases:
        for arm in arms:
            if c[(case,arm)]!=reps: issues.append(('schedule',key,case,arm,c[(case,arm)]))
work=('digest','multiplications','pair_terms','peak_monomials','final_monomials','final_degree','anf_nodes_evaluated')
decision=('selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared','selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction','selector_estimated_benefit','selector_estimated_keep_cost','selector_estimated_fold_cost','fold_lowerings','bypassed_child_shells','transpose_alignments')
for key in ('natural_symbolic_rows','gatep_symbolic_rows'):
    by={(r['case_id'],r['arm']):r for r in d[key]}
    for case in sorted({r['case_id'] for r in d[key]}):
        p7=by[(case,'cm_cword_sig_sparse')]; p6=by[(case,'cm_innode_sig_sparse')]; p5=by[(case,'cm_packed_sig_sparse')]
        direct=by[(case,'direct_sparse_anf')]; dc=by[(case,'direct_cword_sparse_anf')]
        for f in work+decision:
            if p7.get(f)!=p6.get(f): issues.append(('p7/p6 drift',key,case,f,p7.get(f),p6.get(f)))
            if p7.get(f)!=p5.get(f): issues.append(('p7/p5 drift',key,case,f,p7.get(f),p5.get(f)))
        for f in work:
            if direct.get(f)!=dc.get(f): issues.append(('direct drift',key,case,f,direct.get(f),dc.get(f)))
        if p7.get('selector_accepted',0)!=p7.get('fold_lowerings',0): issues.append(('utilization',key,case))
expected_cases=['adder:f[4]','adder:f[5]','cavlc:17','cavlc:35','int2float:e4','int2float:y6','priority:new_n130','priority:new_n174','router:105','router:92']
if d['selection']['case_ids']!=expected_cases: issues.append(('selection',d['selection']['case_ids']))
manifest=json.loads((HERE/'EPFL_SOURCE_MANIFEST.json').read_text()); source_ok=True
for rec in manifest['files']:
    p=ROOT/'cm_n2_p4_run/epfl'/rec['file']
    if sha256(p)!=rec['sha256'] or gitblob(p)!=rec['expected_git_blob']:
        source_ok=False; issues.append(('source',rec['file']))
calc={
 'gatep_p7_over_direct_lower':ratio(d['gatep_lower_timing_rows'],'cm_cword_sig_sparse','direct_cword_sparse_anf','lower_ns'),
 'gatep_p7_over_direct_pipeline':ratio(d['gatep_pipeline_timing_rows'],'cm_cword_sig_build_sparse','direct_build_sparse','pipeline_ns'),
 'gatep_p7_over_direct_build':ratio(d['gatep_pipeline_timing_rows'],'cm_cword_sig_build_sparse','direct_build_sparse','dag_build_ns'),
 'gatep_p7_over_p6_build':ratio(d['gatep_pipeline_timing_rows'],'cm_cword_sig_build_sparse','cm_innode_sig_build_sparse','dag_build_ns'),
 'gatep_p7_over_p5_build':ratio(d['gatep_pipeline_timing_rows'],'cm_cword_sig_build_sparse','cm_packed_sig_build_sparse','dag_build_ns'),
 'natural_p7_over_direct_lower':ratio(d['natural_lower_timing_rows'],'cm_cword_sig_sparse','direct_cword_sparse_anf','lower_ns'),
 'natural_p7_over_direct_pipeline':ratio(d['natural_pipeline_timing_rows'],'cm_cword_sig_build_sparse','direct_build_sparse','pipeline_ns')}
reported={
 'gatep_p7_over_direct_lower':d['gatep']['p7_over_direct:lower_ns']['geomean_ratio'],
 'gatep_p7_over_direct_pipeline':d['gatep']['p7_build_over_direct:pipeline_ns']['geomean_ratio'],
 'gatep_p7_over_direct_build':d['gatep']['p7_build_over_direct:dag_build_ns']['geomean_ratio'],
 'gatep_p7_over_p6_build':d['gatep']['p7_build_over_p6:dag_build_ns']['geomean_ratio'],
 'gatep_p7_over_p5_build':d['gatep']['p7_build_over_p5:dag_build_ns']['geomean_ratio'],
 'natural_p7_over_direct_lower':d['natural']['p7_over_direct:lower_ns']['geomean_ratio'],
 'natural_p7_over_direct_pipeline':d['natural']['p7_build_over_direct:pipeline_ns']['geomean_ratio']}
for k in calc:
    if abs(calc[k]-reported[k])>1e-12: issues.append(('ratio',k,calc[k],reported[k]))
out={'status':'PASS' if not issues else 'FAIL','issues':issues,'prereg_sha256':sha256(HERE/'N2_P7_PREREGISTRATION.md'),'harness_sha256':sha256(HERE/'n2_p7_harness.py'),
     'source_manifest_all_verified':source_ok,'row_counts':counts,'all_correct':not any(not r.get('ok',True) for k in expected for r in d[k]),
     'fuzz_passed':d['fuzz']['passed'],'natural_cases':d['selection']['case_ids'],'recomputed_ratios':calc,
     'gatep_p7_selector_accepted':d['gatep']['p7_diag']['selector_accepted'],'natural_p7_selector_accepted':d['natural']['p7_diag']['selector_accepted']}
(HERE/'N2_P7_INDEPENDENT_VERIFY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
