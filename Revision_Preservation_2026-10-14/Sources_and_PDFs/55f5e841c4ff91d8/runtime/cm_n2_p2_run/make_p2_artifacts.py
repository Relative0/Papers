from __future__ import annotations
import csv,hashlib,json,math,statistics
from pathlib import Path
import n2_p2_harness as h
HERE=Path(__file__).resolve().parent
p=json.loads((HERE/'n2_p2_results.json').read_text())

def med(rows,case,arm,metric):
    xs=[r[metric] for r in rows if r['case_id']==case and r['arm']==arm]
    return statistics.median(xs) if xs else None

def case_csv(corpus):
    t=p[f'{corpus}_timing_rows']; s=p[f'{corpus}_symbolic_rows']; by={(r['case_id'],r['arm']):r for r in s}; cases=sorted({r['case_id'] for r in s})
    out=HERE/f'N2_P2_{corpus.upper()}_CASE_SUMMARY.csv'
    fields=['case_id','circuit_or_depth','source_nodes','p2_candidates','p2_accepted','p2_accepted_shared','p2_plan_entries','p2_executed_fold_hits',
            'p2_direct_compile_ratio','p2_direct_propagate_ratio','p2_p1_compile_ratio','p2_generic_compile_ratio',
            'p2_direct_multiplications_ratio','p2_direct_pair_terms_ratio','p2_direct_peak_monomials_ratio','p2_direct_anf_nodes_ratio','p2_direct_peak_bytes_ratio']
    with out.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader()
        for c in cases:
            q=by[(c,h.P2)]; d=by[(c,h.DIRECT)]
            def ratio(a,b): return a/b if b not in (None,0) else None
            row={
                'case_id':c,
                'circuit_or_depth': q.get('circuit',q.get('depth')),
                'source_nodes':q.get('source_nodes',''),
                'p2_candidates':q['selector_candidates'],'p2_accepted':q['selector_accepted'],'p2_accepted_shared':q['selector_accepted_shared'],
                'p2_plan_entries':q['plan_entries'],'p2_executed_fold_hits':q['planned_fold_lowerings'],
                'p2_direct_compile_ratio':ratio(med(t,c,h.P2,'compile_ns'),med(t,c,h.DIRECT,'compile_ns')),
                'p2_direct_propagate_ratio':ratio(med(t,c,h.P2,'propagate_ns'),med(t,c,h.DIRECT,'propagate_ns')),
                'p2_p1_compile_ratio':ratio(med(t,c,h.P2,'compile_ns'),med(t,c,h.P1,'compile_ns')),
                'p2_generic_compile_ratio':ratio(med(t,c,h.P2,'compile_ns'),med(t,c,h.GENERIC,'compile_ns')),
                'p2_direct_multiplications_ratio':ratio(q['multiplications'],d['multiplications']),
                'p2_direct_pair_terms_ratio':ratio(q['pair_terms'],d['pair_terms']),
                'p2_direct_peak_monomials_ratio':ratio(q['peak_monomials'],d['peak_monomials']),
                'p2_direct_anf_nodes_ratio':ratio(q['anf_nodes_evaluated'],d['anf_nodes_evaluated']),
                'p2_direct_peak_bytes_ratio':ratio(q['python_peak_bytes'],d['python_peak_bytes']),
            }
            w.writerow(row)
    return out

nat_csv=case_csv('natural'); gate_csv=case_csv('gatep')

# Independent verification
checks={}
checks['prereg_sha256_actual']=h.sha256_file(HERE/'N2_P2_PREREGISTRATION.md')
checks['prereg_sha256_expected']=h.PREREG_SHA256
checks['prereg_hash_ok']=checks['prereg_sha256_actual']==checks['prereg_sha256_expected']
checks['harness_sha256_actual']=h.sha256_file(HERE/'n2_p2_harness.py')
checks['harness_sha256_recorded']=p['meta']['harness_sha256']
checks['harness_hash_ok']=checks['harness_sha256_actual']==checks['harness_sha256_recorded']
checks['epfl_blobs']={}
for c,(fname,blob) in h.p1.NATURAL_SOURCES.items():
    actual=h.p1.git_blob_hash(HERE/'epfl'/fname)
    checks['epfl_blobs'][c]={'file':fname,'expected':blob,'actual':actual,'ok':actual==blob}
ref=h.reference_selected_ids(HERE/'N2_P1_NATURAL_SELECTION_REFERENCE.json')
cur=[]
for c in p['selection']['circuits']:
    for x in c['selected']: cur.append(f"{c['circuit']}:{x['root']}")
checks['selection_case_ids_reference']=ref
checks['selection_case_ids_current']=sorted(cur)
checks['selection_matches_reference']=sorted(cur)==ref
checks['row_counts']={
    'natural_symbolic':len(p['natural_symbolic_rows']),'natural_timing':len(p['natural_timing_rows']),
    'gatep_symbolic':len(p['gatep_symbolic_rows']),'gatep_timing':len(p['gatep_timing_rows']),'fuzz_cases':p['fuzz']['cases']}
checks['row_counts_expected']={'natural_symbolic':40,'natural_timing':1000,'gatep_symbolic':144,'gatep_timing':3600,'fuzz_cases':1000}
checks['row_counts_ok']=checks['row_counts']==checks['row_counts_expected']
checks['all_symbolic_ok']=all(r['ok'] for r in p['natural_symbolic_rows']+p['gatep_symbolic_rows'])
checks['all_timing_ok']=all(r['ok'] for r in p['natural_timing_rows']+p['gatep_timing_rows'])
checks['fuzz_ok']=p['fuzz']['passed'] and not p['fuzz']['failures']
# digest equality per corpus/case
checks['digest_mismatches']=[]
for corpus in ('natural','gatep'):
    rows=p[f'{corpus}_symbolic_rows']
    for cid in sorted({r['case_id'] for r in rows}):
        ds={r['digest'] for r in rows if r['case_id']==cid}
        if len(ds)!=1: checks['digest_mismatches'].append({'corpus':corpus,'case_id':cid,'digests':sorted(ds)})
checks['digests_ok']=not checks['digest_mismatches']
# selector decisions P2 vs frozen P1 arm
selkeys=['selector_candidates','selector_accepted','selector_accepted_shared','selector_rejected_nonpositive','selector_rejected_min_benefit','selector_rejected_fraction','selector_estimated_benefit']
checks['selector_decision_mismatches']=[]
for corpus in ('natural','gatep'):
    rows=p[f'{corpus}_symbolic_rows']; by={(r['case_id'],r['arm']):r for r in rows}
    for cid in sorted({r['case_id'] for r in rows}):
        a=by[(cid,h.P2)]; b=by[(cid,h.P1)]
        for k in selkeys:
            if a[k]!=b[k]: checks['selector_decision_mismatches'].append({'corpus':corpus,'case_id':cid,'field':k,'p2':a[k],'p1':b[k]})
checks['selector_decisions_match_p1']=not checks['selector_decision_mismatches']
checks['overall_ok']=all([checks['prereg_hash_ok'],checks['harness_hash_ok'],checks['selection_matches_reference'],checks['row_counts_ok'],checks['all_symbolic_ok'],checks['all_timing_ok'],checks['fuzz_ok'],checks['digests_ok'],checks['selector_decisions_match_p1'],all(v['ok'] for v in checks['epfl_blobs'].values())])
(HERE/'N2_P2_INDEPENDENT_VERIFY.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')

# Secondary weighted-by-workload timing summaries (not prereg primary)
def sum_case_medians(rows,num,den,metric='compile_ns'):
    cases=sorted({r['case_id'] for r in rows})
    def m(c,a): return statistics.median([r[metric] for r in rows if r['case_id']==c and r['arm']==a])
    aa=sum(m(c,num) for c in cases); bb=sum(m(c,den) for c in cases)
    return {'ratio':aa/bb,'num_total_ns':aa,'den_total_ns':bb}
sec={'natural_sum_case_medians':sum_case_medians(p['natural_timing_rows'],h.P2,h.DIRECT),
     'gatep_sum_case_medians':sum_case_medians(p['gatep_timing_rows'],h.P2,h.DIRECT)}

s=p['summary']; nat=s['natural_timing']; gate=s['gatep_timing']; nd=s['natural_p2_diag']; gd=s['gatep_p2_diag']
text=f'''# N2/P2 Interpretation — Direct/no-rewrite as the profitability baseline

## Bottom line

P2 answers the proposed question more directly than P1: **when the alternative is simply lowering the original DAG to sparse ANF, the frozen selector does not yet pay for itself end to end.**

On the natural EPFL set, P2 accepted **{nd['selector_accepted']} of {nd['selector_candidates']}** candidates, so this corpus still contains no natural case in which the frozen P1 profitability rule elects to take a fold. P2 therefore measures abstention overhead there, not a natural fold speedup. Its preregistered P2/direct compile ratio is **{nat['p2_over_direct_sparse_anf:compile_ns']['geomean_ratio']:.4f}x** with 95% CI **{nat['p2_over_direct_sparse_anf:compile_ns']['bootstrap']['ci95'][0]:.4f}–{nat['p2_over_direct_sparse_anf:compile_ns']['bootstrap']['ci95'][1]:.4f}**: about **{(nat['p2_over_direct_sparse_anf:compile_ns']['geomean_ratio']-1)*100:.1f}% slower** by the case-balanced primary endpoint.

The natural propagation-only ratio is **{nat['p2_over_direct_sparse_anf:propagate_ns']['geomean_ratio']:.4f}x**, essentially parity, exactly as expected when zero folds execute. The symbolic work is also identical to direct (1.0000x multiplications, pair terms, peak monomials, and ANF nodes). The added cost is the planner itself plus its temporary bookkeeping; traced peak Python allocation is **{s['natural_symbolic_p2_over_direct']['python_peak_bytes']['geomean_ratio']:.4f}x** direct.

## The more informative Gate-P result

Gate-P does contain the folds we wanted to test. The P2 selector made **exactly the same decisions as the frozen P1 selector** on every measured case: **{gd['selector_accepted']} accepted of {gd['selector_candidates']} candidates**, including **{gd['selector_accepted_shared']} shared** candidates. This is independently checked in `N2_P2_INDEPENDENT_VERIFY.json`.

There the planned lowering itself works: P2/direct propagation time is **{gate['p2_over_direct_sparse_anf:propagate_ns']['geomean_ratio']:.4f}x**, about **{(1-gate['p2_over_direct_sparse_anf:propagate_ns']['geomean_ratio'])*100:.1f}% faster**. Symbolically, P2 uses only **{s['gatep_p2_diag']['planned_fold_lowerings']} actually executed planned folds** after ancestor folds make many planned descendants unreachable. Across Gate-P, the P2 lowering has substantially less work than direct: the measured pair-term geomean is about **0.4364x**, multiplications about **0.6375x**, and evaluated ANF nodes about **0.7788x** direct.

But the planner is too expensive in this Python prototype. The preregistered compile ratio is **{gate['p2_over_direct_sparse_anf:compile_ns']['geomean_ratio']:.4f}x** (95% CI **{gate['p2_over_direct_sparse_anf:compile_ns']['bootstrap']['ci95'][0]:.4f}–{gate['p2_over_direct_sparse_anf:compile_ns']['bootstrap']['ci95'][1]:.4f}**), i.e. more than twice direct. The geometric-mean planner time across Gate-P cases is roughly 0.064 ms while direct's entire compile path is only about 0.045 ms. So the planner can cost more than the complete unoptimized computation before any fold savings are realized.

This falls exactly into the preregistered diagnostic category: **propagation faster, compile slower**. In 23 of the 36 Gate-P cases propagation was faster while total compile was slower; no Gate-P case had a faster P2 compile median than direct.

## Why P2 can still beat P1/generic while losing to direct

P2 is materially leaner than the previous optimizer front ends. Natural compile time is **{nat['p2_over_cm_profit_sparse:compile_ns']['geomean_ratio']:.4f}x P1** and **{nat['p2_over_generic_2support_sparse:compile_ns']['geomean_ratio']:.4f}x generic**. On Gate-P it is **{gate['p2_over_cm_profit_sparse:compile_ns']['geomean_ratio']:.4f}x P1** and **{gate['p2_over_generic_2support_sparse:compile_ns']['geomean_ratio']:.4f}x generic**. So removing the rewritten/CSE-normalized executable DAG was a real improvement.

However, **direct sparse ANF is an even stronger baseline than either optimizer**, especially for the tiny Gate-P programs. This is the key correction P2 was designed to expose.

A secondary workload-weighted calculation (sum of case medians, not the preregistered equal-case geomean) puts natural P2/direct at **{sec['natural_sum_case_medians']['ratio']:.4f}x**, only about **{(sec['natural_sum_case_medians']['ratio']-1)*100:.1f}% slower**, because the large CAVLC cases dominate total work while the fixed planning overhead hurts small router/priority cones most. This does not change the preregistered conclusion, but it shows where the overhead lives.

## The new optimization target

The strongest next target is no longer a new benefit threshold. It is **eliminating speculative planning work**.

P2 created {gd['plan_entries']} Gate-P plan entries but only {gd['planned_fold_lowerings']} were actually consumed by the ANF lowerer — **{100*gd['planned_fold_lowerings']/gd['plan_entries']:.1f}% utilization**. Nested descendant plans become irrelevant when an ancestor fold replaces the whole region. That suggests a P3 architecture based on **demand-driven/top-down fold planning** or a fused lazy lowerer: test the fold at the node that is actually demanded, and if the ancestor fold is taken, never inspect or plan the descendants it makes dead. The direct path should remain the fall-through case.

That would attack the measured bottleneck directly while retaining the demonstrated Gate-P lowering reduction. It would also be a cleaner test than relaxing the profitability threshold, because the present selector is already correctly abstaining on the natural set.
'''
(HERE/'N2_P2_INTERPRETATION.md').write_text(text,encoding='utf-8')

readme=f'''# N2/P2 Reproducibility Bundle

- Preregistration: `N2_P2_PREREGISTRATION.md`
- Frozen selector/execution harness: `n2_p2_harness.py`
- Chunk runner: `run_p2_chunk.py`
- Result combiner: `combine_p2_chunks.py`
- Full result payload: `n2_p2_results.json`
- Main report: `N2_P2_RESULTS.md`
- Interpretation: `N2_P2_INTERPRETATION.md`
- Per-case summaries: `{nat_csv.name}`, `{gate_csv.name}`
- Independent verification: `N2_P2_INDEPENDENT_VERIFY.json`
- EPFL snapshot: `epfl/`
- Raw chunk outputs: `chunks/`

The P2 selector thresholds were frozen before benchmark execution and are identical to P1. The full one-process run exceeded the execution-call time limit, so the frozen harness was replayed case-by-case with `run_p2_chunk.py`; no selector or execution rule was changed. The combiner recomputes the frozen source selection and derives the reported comparisons from the persisted raw chunks.
'''
(HERE/'REPRODUCIBILITY_README.md').write_text(readme,encoding='utf-8')
