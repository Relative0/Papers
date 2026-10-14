import csv,glob,hashlib,json,math,statistics,collections
from pathlib import Path
H=Path('.')
summary=json.load(open('N2_P7B_SUMMARY.json')); gate=json.load(open('P7B_FROZEN_GATE.json')); cal=json.load(open('calibration.json')); val=json.load(open('validation_corrected.json')); fuzz=json.load(open('fuzz.json')); gp=json.load(open('gatep.json'))
issues=[]
def check(cond,msg):
    if not cond: issues.append(msg)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
check(sha('N2_P7B_PREREGISTRATION.md')==summary['hashes']['prereg'],'prereg hash')
check(sha('P7B_FROZEN_GATE.json')==summary['hashes']['frozen_gate'],'gate hash')
check(sha('n2_p7b_harness.py')==summary['hashes']['harness_corrected'],'harness hash')
check(gate['selected_threshold']==17==cal['selected_threshold']==summary['threshold'],'threshold freeze')
check(fuzz['passed'] and not fuzz['failures'] and fuzz['cases']==1000,'fuzz')
# source manifest / git blobs
man=json.load(open('EPFL_SOURCE_MANIFEST.json'))
for f in man['files']:
    data=(H/'epfl'/f['file']).read_bytes(); g=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    check(g==f['expected_git_blob'],f"git blob {f['file']}")
    check(hashlib.sha256(data).hexdigest()==f['sha256'],f"sha256 {f['file']}")
# Natural rows
nat=[]; nsym=[]
for p in sorted(glob.glob('natural/*.json')):
    x=json.load(open(p)); nat.extend(x['timing_rows']); nsym.extend(x['symbolic_rows'])
check(len(gp['timing_rows'])==36*20*3,'gatep timing row count')
check(len(gp['symbolic_rows'])==36*3,'gatep symbolic row count')
check(len(nat)==10*15*3,'natural timing row count')
check(len(nsym)==10*3,'natural symbolic row count')
check(all(r['ok'] for r in gp['timing_rows']+gp['symbolic_rows']+nat+nsym),'all eval correctness')
# schedule completeness per case
for label,rows,reps in [('gatep',gp['timing_rows'],20),('natural',nat,15)]:
    by=collections.defaultdict(collections.Counter)
    for r in rows: by[r['case_id']][r['arm']]+=1
    for cid,c in by.items():
        check(c==collections.Counter({'direct_build_sparse':reps,'cm_innode_sig_build_sparse':reps,'dispatch_p6_or_direct':reps}),f'{label} schedule {cid}: {c}')
# deterministic gate rule and natural false positives
for r in [x for x in gp['symbolic_rows']+nsym if x['arm']=='dispatch_p6_or_direct']:
    check(bool(r['annotate'])==(r['two_support_pressure']>=17),f"decision {r['case_id']}")
nat_disp=[r for r in nsym if r['arm']=='dispatch_p6_or_direct']
check(sum(r['annotate'] for r in nat_disp)==0,'natural false-positive annotations')
# P6 utilization on annotated Gate-P
for r in [x for x in gp['symbolic_rows'] if x['arm']=='dispatch_p6_or_direct' and x['annotate']]:
    check(r.get('selector_accepted',0)==r.get('fold_lowerings',0),f"P6 utilization {r['case_id']}")
# dispatch symbolic work equals chosen backend
def verify_choice(symrows):
    by=collections.defaultdict(dict)
    for r in symrows: by[r['case_id']][r['arm']]=r
    for cid,v in by.items():
        z=v['dispatch_p6_or_direct']; chosen='cm_innode_sig_build_sparse' if z['annotate'] else 'direct_build_sparse'; q=v[chosen]
        check(z['digest']==q['digest'],f'digest chosen {cid}')
        for k in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated'):
            check(z[k]==q[k],f'work chosen {cid} {k}')
verify_choice(gp['symbolic_rows']); verify_choice(nsym)
# recompute key case-median ratios
def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
def table(rows):
    by=collections.defaultdict(lambda:collections.defaultdict(list))
    for r in rows: by[r['case_id']][r['arm']].append(r['pipeline_ns'])
    return {cid:{a:statistics.median(v) for a,v in d.items()} for cid,d in by.items()}
for label,rows,skey in [('gatep',gp['timing_rows'],'gatep'),('natural',nat,'natural')]:
    t=table(rows); rr=[v['dispatch_p6_or_direct']/v['direct_build_sparse'] for v in t.values()]; value=gm(rr)
    check(abs(value-summary[skey]['dispatch_over_direct_geomean'])<1e-12,f'{label} ratio')
# corrected validation is fixed threshold, no retuning
check(val['threshold']==17 and val['cases']==60,'corrected validation')
result={'status':'PASS' if not issues else 'FAIL','issues':issues,'threshold':17,'hashes':summary['hashes'],
        'source_manifest_all_verified':not any(x.startswith(('git blob','sha256')) for x in issues),
        'row_counts':{'gatep_symbolic':len(gp['symbolic_rows']),'gatep_timing':len(gp['timing_rows']),'natural_symbolic':len(nsym),'natural_timing':len(nat)},
        'fuzz_cases':fuzz['cases'],'gatep_dispatch_over_direct':summary['gatep']['dispatch_over_direct_geomean'],
        'natural_dispatch_over_direct':summary['natural']['dispatch_over_direct_geomean'],
        'gatep_annotated':summary['gatep']['annotated'],'gatep_fold_cases':summary['gatep']['fold_cases'],'natural_annotated':summary['natural']['annotated']}
open('N2_P7B_INDEPENDENT_VERIFY.json','w').write(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
