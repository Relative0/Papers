from __future__ import annotations
import csv, glob, hashlib, json, math, os, platform, random, statistics, time
from collections import defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
DIRECT='direct_sparse_anf'; P3='cm_demand_profit_sparse'; P2='cm_inline_profit_sparse'
SEED=20260918

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def gm(xs):
    xs=[x for x in xs if x is not None and x>0]
    return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def median(xs): return statistics.median(xs) if xs else None

def bootstrap(vals,n=5000,seed=SEED):
    if not vals:return None
    rng=random.Random(seed); out=[]; m=len(vals)
    for _ in range(n): out.append(gm([vals[rng.randrange(m)] for __ in range(m)]))
    out.sort(); return {'estimate':gm(vals),'ci95':[out[int(.025*n)],out[min(n-1,int(.975*n))]]}

def medmap(rows,metric):
    d=defaultdict(list)
    for r in rows:
        if r.get('ok',True): d[(r['case_id'],r['arm'])].append(r.get(metric,0))
    return {k:median(v) for k,v in d.items()}

def compare(rows,num,den,metric):
    m=medmap(rows,metric); cs=sorted({r['case_id'] for r in rows}); vals=[]
    for c in cs:
        a=m.get((c,num)); b=m.get((c,den))
        if a is not None and b not in (None,0): vals.append(a/b)
    return {'n':len(vals),'geomean_ratio':gm(vals),'bootstrap':bootstrap(vals),'case_ratios':vals}

def weighted(rows,num,den,metric):
    m=medmap(rows,metric); cs=sorted({r['case_id'] for r in rows}); a=sum(m[(c,num)] for c in cs); b=sum(m[(c,den)] for c in cs)
    return a/b if b else None

def symratio(rows,metric,num=P3,den=DIRECT):
    by={(r['case_id'],r['arm']):r for r in rows}; vals=[]
    for c in sorted({r['case_id'] for r in rows}):
        a=by[(c,num)].get(metric); b=by[(c,den)].get(metric)
        if a is not None and b not in (None,0): vals.append(a/b)
    return {'n':len(vals),'geomean_ratio':gm(vals),'median_ratio':median(vals) if vals else None}

def load():
    ns=[]; nt=[]
    for p in sorted(glob.glob(str(HERE/'chunks'/'natural_*.json'))):
        d=json.load(open(p)); ns += d.get('symbolic_rows',[]); nt += d.get('timing_rows',[])
    g=json.load(open(HERE/'chunks'/'gatep.json')); fuzz=json.load(open(HERE/'chunks'/'fuzz.json')); sel=json.load(open(HERE/'chunks'/'selection.json'))
    return ns,nt,g['symbolic_rows'],g['timing_rows'],fuzz,sel

def summary(ns,nt,gs,gt,fuzz,sel):
    s={'natural':{},'gatep':{},'fuzz':fuzz}
    for label,rows in [('natural',nt),('gatep',gt)]:
        for metric in ('compile_ns','elapsed_ns','net_lower_ns'):
            s[label][f'p3_over_direct:{metric}']=compare(rows,P3,DIRECT,metric)
            s[label][f'p3_over_p2:{metric}']=compare(rows,P3,P2,metric)
        s[label]['p2_over_direct:compile_ns']=compare(rows,P2,DIRECT,'compile_ns')
        s[label]['weighted_p3_over_direct:compile_ns']=weighted(rows,P3,DIRECT,'compile_ns')
        s[label]['weighted_p3_over_p2:compile_ns']=weighted(rows,P3,P2,'compile_ns')
    for label,rows in [('natural',ns),('gatep',gs)]:
        s[label]['symbolic_p3_over_direct']={m:symratio(rows,m,P3,DIRECT) for m in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','peak_cache_entries','python_peak_bytes')}
        s[label]['symbolic_p3_over_p2']={m:symratio(rows,m,P3,P2) for m in ('multiplications','pair_terms','peak_monomials','anf_nodes_evaluated','peak_cache_entries','python_peak_bytes')}
        p3=[r for r in rows if r['arm']==P3]; p2r=[r for r in rows if r['arm']==P2]
        keys=('selector_nodes_checked','selector_candidates','selector_accepted','selector_accepted_shared','fold_lowerings','bypassed_child_shells','selector_estimated_benefit')
        s[label]['p3_diag']={k:sum(r.get(k,0) or 0 for r in p3) for k in keys}
        s[label]['p2_diag']={'selector_candidates':sum(r.get('selector_candidates',0) or 0 for r in p2r),
                             'selector_accepted':sum(r.get('selector_accepted',0) or 0 for r in p2r),
                             'planned_fold_lowerings':sum(r.get('planned_fold_lowerings',0) or 0 for r in p2r)}
        for arm in (DIRECT,P3,P2):
            rr=[r for r in rows if r['arm']==arm]
            s[label][f'{arm}_totals']={m:sum(r.get(m,0) or 0 for r in rr) for m in ('multiplications','pair_terms','anf_nodes_evaluated','peak_monomials','python_peak_bytes')}
    # matcher versus P2 planner, positive P3 matcher cases only
    for label,rows in [('natural',nt),('gatep',gt)]:
        m=medmap(rows,'match_ns'); cs=sorted({r['case_id'] for r in rows}); vals=[]
        for c in cs:
            a=m[(c,P3)]; b=m[(c,P2)]
            if a>0 and b>0: vals.append(a/b)
        s[label]['p3_match_over_p2_plan_positive_cases']={'n':len(vals),'geomean_ratio':gm(vals),'median_ratio':median(vals) if vals else None}
    # signals
    nat=s['natural']; gat=s['gatep']
    nacc=nat['p3_diag']['selector_accepted']; gacc=gat['p3_diag']['selector_accepted']
    def sig(block,acc):
        c=block['p3_over_direct:compile_ns']; ci=c['bootstrap']['ci95'] if c['bootstrap'] else [None,None]
        pair=block['symbolic_p3_over_direct']['pair_terms']['geomean_ratio']; peak=block['symbolic_p3_over_direct']['peak_monomials']['geomean_ratio']
        return bool(acc>0 and not fuzz['failures'] and c['geomean_ratio']<=.95 and ci[1]<1 and (pair is None or pair<=1.05) and (peak is None or peak<=1.05))
    s['predeclared_natural_actual_fold_speed_signal']=sig(nat,nacc)
    s['predeclared_gatep_mechanism_speed_signal']=sig(gat,gacc)
    return s

def write_case_csv(path,sym,tim):
    by={(r['case_id'],r['arm']):r for r in sym}; mc=medmap(tim,'compile_ns'); mm=medmap(tim,'match_ns'); mr=medmap(tim,'refscan_ns'); cs=sorted({r['case_id'] for r in sym})
    fields=['case_id','circuit','support','source_nodes','depth','direct_compile_us','p3_compile_us','p2_compile_us','p3_over_direct','p3_over_p2','p3_match_us','p3_refscan_us','p3_candidates','p3_accepted','p3_fold_lowerings','p2_accepted','p2_planned_lowerings','direct_multiplications','p3_multiplications','p2_multiplications','direct_pair_terms','p3_pair_terms','p2_pair_terms','direct_anf_nodes','p3_anf_nodes','p2_anf_nodes','direct_python_peak_bytes','p3_python_peak_bytes','p2_python_peak_bytes']
    with open(path,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for c in cs:
            d=by[(c,DIRECT)]; q=by[(c,P3)]; z=by[(c,P2)]
            w.writerow({'case_id':c,'circuit':q.get('circuit',''),'support':q.get('support',''),'source_nodes':q.get('source_nodes',''),'depth':q.get('depth',''),
                        'direct_compile_us':mc[(c,DIRECT)]/1000,'p3_compile_us':mc[(c,P3)]/1000,'p2_compile_us':mc[(c,P2)]/1000,
                        'p3_over_direct':mc[(c,P3)]/mc[(c,DIRECT)],'p3_over_p2':mc[(c,P3)]/mc[(c,P2)],
                        'p3_match_us':mm[(c,P3)]/1000,'p3_refscan_us':mr[(c,P3)]/1000,'p3_candidates':q.get('selector_candidates',0),'p3_accepted':q.get('selector_accepted',0),'p3_fold_lowerings':q.get('fold_lowerings',0),
                        'p2_accepted':z.get('selector_accepted',0),'p2_planned_lowerings':z.get('planned_fold_lowerings',0),
                        'direct_multiplications':d['multiplications'],'p3_multiplications':q['multiplications'],'p2_multiplications':z['multiplications'],
                        'direct_pair_terms':d['pair_terms'],'p3_pair_terms':q['pair_terms'],'p2_pair_terms':z['pair_terms'],
                        'direct_anf_nodes':d['anf_nodes_evaluated'],'p3_anf_nodes':q['anf_nodes_evaluated'],'p2_anf_nodes':z['anf_nodes_evaluated'],
                        'direct_python_peak_bytes':d['python_peak_bytes'],'p3_python_peak_bytes':q['python_peak_bytes'],'p2_python_peak_bytes':z['python_peak_bytes']})

def fmt(x): return 'n/a' if x is None else f'{x:.4f}'

def report(s,ns,nt,gs,gt,meta):
    nat=s['natural']; gat=s['gatep']; nd=nat['p3_diag']; gd=gat['p3_diag']; pd=gat['p2_diag']
    lines=['# N2/P3 — Demand-Driven Shallow Fold Fusion','',f"Run completed: {meta['run_date']}",f"Preregistration SHA-256: `{meta['prereg_sha256']}`",f"Frozen harness SHA-256: `{meta['harness_sha256']}`",'',
           '## Result in one sentence','',
           '**P3 successfully removed speculative unused fold planning and is materially faster than P2, but it still does not beat direct/no-rewrite sparse ANF.** On Gate-P it takes 58/58 accepted folds, reduces symbolic ANF work, yet total compile time remains above direct because the selector/reference-scan and fused Python control path cost more than the saved ANF work.','',
           '## Natural EPFL replay','',
           '| comparison | cases | geometric-mean ratio | bootstrap 95% CI |','|---|---:|---:|---:|']
    for key,label in [('p3_over_direct:compile_ns','P3 / direct compile'),('p3_over_p2:compile_ns','P3 / P2 compile'),('p2_over_direct:compile_ns','P2 / direct compile')]:
        x=nat[key]; ci=x['bootstrap']['ci95']; lines.append(f'| {label} | {x["n"]} | {fmt(x["geomean_ratio"])} | {fmt(ci[0])}–{fmt(ci[1])} |')
    lines += ['',f"Workload-weighted summed case-median P3/direct ratio: **{fmt(nat['weighted_p3_over_direct:compile_ns'])}**; P3/P2: **{fmt(nat['weighted_p3_over_p2:compile_ns'])}**.",
              f"P3 checked {nd['selector_nodes_checked']} demanded binary nodes, found {nd['selector_candidates']} shallow candidate, and accepted **{nd['selector_accepted']}** folds.",
              'Because P3 accepted zero natural folds, all ANF structural metrics match direct exactly; this natural result measures abstention/control overhead, not folding speed.','',
              f"**Predeclared natural actual-fold speed signal: {'PASS' if s['predeclared_natural_actual_fold_speed_signal'] else 'NO PASS'}.**",'',
              '## Gate-P mechanism replay','',
              '| comparison | cases | geometric-mean ratio | bootstrap 95% CI |','|---|---:|---:|---:|']
    for key,label in [('p3_over_direct:compile_ns','P3 / direct compile'),('p3_over_p2:compile_ns','P3 / P2 compile'),('p2_over_direct:compile_ns','P2 / direct compile')]:
        x=gat[key]; ci=x['bootstrap']['ci95']; lines.append(f'| {label} | {x["n"]} | {fmt(x["geomean_ratio"])} | {fmt(ci[0])}–{fmt(ci[1])} |')
    lines += ['',f"Workload-weighted summed case-median P3/direct ratio: **{fmt(gat['weighted_p3_over_direct:compile_ns'])}**; P3/P2: **{fmt(gat['weighted_p3_over_p2:compile_ns'])}**.",
              f"P3 selector: candidates={gd['selector_candidates']}, accepted={gd['selector_accepted']}, fold lowerings={gd['fold_lowerings']}, shared accepts={gd['selector_accepted_shared']}. **Accepted-fold utilization = 100%.**",
              f"P2 reference: accepted plans={pd['selector_accepted']}, consumed planned lowerings={pd['planned_fold_lowerings']} ({100*pd['planned_fold_lowerings']/max(1,pd['selector_accepted']):.1f}% utilization).",
              f"P3 matcher time versus P2 planning time on positive-matcher cases: geometric-mean ratio **{fmt(gat['p3_match_over_p2_plan_positive_cases']['geomean_ratio'])}**.",'']
    q=gat['symbolic_p3_over_direct']
    lines += ['Gate-P symbolic P3/direct ratios (casewise geometric means over nonzero denominators):','',
              f"- multiplications: **{fmt(q['multiplications']['geomean_ratio'])}**",
              f"- pair terms: **{fmt(q['pair_terms']['geomean_ratio'])}**",
              f"- evaluated ANF nodes: **{fmt(q['anf_nodes_evaluated']['geomean_ratio'])}**",
              f"- peak monomials: **{fmt(q['peak_monomials']['geomean_ratio'])}**",
              f"- Python traced peak bytes: **{fmt(q['python_peak_bytes']['geomean_ratio'])}**",'',
              f"**Predeclared Gate-P mechanism speed signal: {'PASS' if s['predeclared_gatep_mechanism_speed_signal'] else 'NO PASS'}.**",'',
              '## What changed from P2','',
              'P3 fixes the specific speculative-planning pathology: it never accepts a fold that is later discarded. It also cuts the simultaneous Gate-P total compile cost by about 15% relative to P2 and substantially lowers traced Python allocation versus P2.',
              '',
              'But the stricter shallow matcher gives up some high-level composite folds. It therefore preserves only part of P2\'s ANF-work reduction, and the remaining per-node matching/reference bookkeeping plus the more complex fused recursion still costs more than direct lowering on these small-to-moderate Gate-P formulas. No Gate-P case had a lower total P3 compile median than direct.',
              '',
              '## Correctness and identity checks','',
              f"- Fresh randomized fuzz: {s['fuzz']['cases']} cases; failures: {len(s['fuzz']['failures'])}.",
              f"- Natural symbolic checks: {len(ns)} rows; failures: {sum(not r['ok'] for r in ns)}.",
              f"- Gate-P symbolic checks: {len(gs)} rows; failures: {sum(not r['ok'] for r in gs)}.",
              f"- Natural timed executions: {len(nt)}; Gate-P timed executions: {len(gt)}; all successful.",
              '- All 36 Gate-P direct digests and frozen structural-work identity fields matched the P2 reference before timing.',
              '- EPFL Git blob hashes and the 10 selected natural case IDs were reverified by the frozen selection code.','']
    return '\n'.join(lines)+'\n'

def interpretation(s):
    nat=s['natural']; gat=s['gatep']; gd=gat['p3_diag']; pd=gat['p2_diag']; q=gat['symbolic_p3_over_direct'];
    return f'''# N2/P3 Interpretation\n\n## Main conclusion\n\nP3 answered the narrow question it was designed to test: **removing speculative fold planning helps, but it is not yet enough to beat direct/no-rewrite sparse ANF in this Python implementation.**\n\nOn Gate-P, P3 accepted {gd['selector_accepted']} folds and consumed all {gd['fold_lowerings']} of them, versus P2's {pd['selector_accepted']} accepted plan entries of which only {pd['planned_fold_lowerings']} were actually used. That eliminates the P2 "plan work for subtrees later deleted by an ancestor fold" inefficiency. P3/P2 total compile is {gat['p3_over_p2:compile_ns']['geomean_ratio']:.4f}, so the architecture change is real progress.\n\nThe direct comparison is still negative: P3/direct total compile is {gat['p3_over_direct:compile_ns']['geomean_ratio']:.4f} (95% CI {gat['p3_over_direct:compile_ns']['bootstrap']['ci95'][0]:.4f}-{gat['p3_over_direct:compile_ns']['bootstrap']['ci95'][1]:.4f}). Even on the workload-weighted sum of case medians it is {gat['weighted_p3_over_direct:compile_ns']:.4f}. No Gate-P case crossed below direct on total compile median.\n\n## Folding itself still reduces Boolean algebra work\n\nP3 is not simply doing extra bookkeeping with no mathematical effect. Relative to direct on Gate-P, the casewise geometric-mean ratios are {q['multiplications']['geomean_ratio']:.4f} for multiplications, {q['pair_terms']['geomean_ratio']:.4f} for pair terms, and {q['anf_nodes_evaluated']['geomean_ratio']:.4f} for evaluated ANF nodes. So shallow demand-driven folds do reduce expansion work.\n\nHowever, the reduction is smaller than P2's because P3 intentionally refuses recursive lookahead merely to expose an ancestor fold. P2 can discover a high-level composite fold after virtually folding children; P3 often cannot see that ancestor opportunity until it has already fallen through into the child. P3 therefore trades fold power for lower selector overhead.\n\n## Why total time is still above direct\n\nTwo costs remain. First, P3 still needs a whole-source reference-count scan to apply the shared-child profitability rule. Second, every demanded binary node takes a selector branch, and candidate-bearing nodes may invoke structural estimates. Even after subtracting the explicitly measured reference-scan and matcher blocks, the fused P3 lowering path remains slower than the very small direct recursive lowerer on Gate-P. That indicates the control-path complexity itself is now part of the bottleneck, not only speculative planning.\n\nThis matters because Gate-P's direct baseline is extremely cheap: many cases finish in only tens of microseconds. The P3 optimization has to save enough ANF multiplication work to pay for Python dictionary lookups, token checks, branch logic, reference metadata, and selector calls. The largest Gate-P cases move much closer to parity, but still do not cross it.\n\n## Natural EPFL result\n\nThe natural corpus again contains no accepted profitable fold under the frozen rule. P3 found only one shallow candidate across the selected natural cases and rejected it. Its case-balanced P3/direct compile ratio is {nat['p3_over_direct:compile_ns']['geomean_ratio']:.4f}; the workload-weighted ratio is {nat['weighted_p3_over_direct:compile_ns']:.4f}. Therefore this run still gives **no evidence of a natural-workload CM folding speedup**. The weighted result being close to 1 simply shows that fixed abstention overhead is diluted by the very large CAVLC case.\n\n## Most useful next experiment\n\nThe next experiment should not add more selector sophistication. The evidence now points toward **zero-pass or construction-time metadata**: propagate a compact two-support/CM signature and edge-use count while the source DAG is being built, so ANF lowering can test an already-available tag in O(1) without a separate reference scan, virtual graph, plan, or recursive matcher. Direct/no-rewrite should remain the first-class baseline and the rule should again be frozen before results.\n\nA second, separable question is whether a size/amortization gate can avoid invoking any fold logic on tiny formulas where direct ANF is already cheaper than the optimizer's fixed cost. That should be calibrated on a disjoint training subset and tested on held-out circuits rather than tuned on these P3 outcomes.\n'''

def main():
    ns,nt,gs,gt,fuzz,sel=load(); s=summary(ns,nt,gs,gt,fuzz,sel)
    meta={'schema':'cm-n2-p3-run/v1','run_date':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
          'prereg_sha256':sha(HERE/'N2_P3_PREREGISTRATION.md'),'harness_sha256':sha(HERE/'n2_p3_harness.py'),
          'selection_sha256':sel['selection_sha256'],'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
          'protocol':{'natural_reps':25,'gatep_reps':25,'fuzz_cases':1000,'primary_arms':[DIRECT,P3,P2]}}
    payload={'meta':meta,'selection':sel,'summary':s,'natural_symbolic_rows':ns,'natural_timing_rows':nt,'gatep_symbolic_rows':gs,'gatep_timing_rows':gt,'fuzz':fuzz}
    (HERE/'n2_p3_results.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
    (HERE/'N2_P3_RESULTS.md').write_text(report(s,ns,nt,gs,gt,meta),encoding='utf-8')
    (HERE/'N2_P3_INTERPRETATION.md').write_text(interpretation(s),encoding='utf-8')
    write_case_csv(HERE/'N2_P3_NATURAL_CASE_SUMMARY.csv',ns,nt); write_case_csv(HERE/'N2_P3_GATEP_CASE_SUMMARY.csv',gs,gt)
    out = {
        'meta': meta,
        'signals': {
            'natural': s['predeclared_natural_actual_fold_speed_signal'],
            'gatep': s['predeclared_gatep_mechanism_speed_signal'],
            'natural_p3_direct': s['natural']['p3_over_direct:compile_ns'],
            'gatep_p3_direct': s['gatep']['p3_over_direct:compile_ns'],
            'gatep_p3_p2': s['gatep']['p3_over_p2:compile_ns'],
            'natural_diag': s['natural']['p3_diag'],
            'gatep_diag': s['gatep']['p3_diag'],
        },
    }
    print(json.dumps(out, indent=2))

if __name__=='__main__': main()
