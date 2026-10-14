from __future__ import annotations
import csv, hashlib, json, math, random, statistics, time
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
D=json.load(open(HERE/'n2_p4_results.json'))
DIRECT_META='direct_meta_sparse_anf'; P4_NATIVE='cm_meta_native_sparse'; P4_PROP='cm_meta_sig_sparse'; P3='cm_demand_profit_sparse'; P2='cm_inline_profit_sparse'; DIRECT_ORIG='direct_sparse_anf'; DIRECT_BUILD='direct_build_sparse'; P4_BUILD='cm_meta_sig_build_sparse'

def medmap(rows,metric):
 d=defaultdict(list)
 for r in rows:d[(r['case_id'],r['arm'])].append(r[metric])
 return {k:statistics.median(v) for k,v in d.items()}

def gm(xs):
 xs=[x for x in xs if x is not None and x>0]
 return math.exp(sum(math.log(x) for x in xs)/len(xs)) if xs else None

def write_csv(corpus):
 sym=D[f'{corpus}_symbolic_rows']; low=D[f'{corpus}_lower_timing_rows']; pipe=D[f'{corpus}_pipeline_timing_rows']
 by={(r['case_id'],r['arm']):r for r in sym}; ml=medmap(low,'lower_ns'); mp=medmap(pipe,'pipeline_ns'); mb=medmap(pipe,'dag_build_ns')
 cases=sorted({r['case_id'] for r in sym})
 fields=['case_id','circuit','support','source_nodes','depth','direct_lower_us','p4_native_lower_us','p4_prop_lower_us','p3_lower_us','p4_prop_over_direct','p4_prop_over_p3','p4_native_over_direct','direct_build_pipeline_us','p4_build_pipeline_us','p4_pipeline_over_direct','direct_dag_build_us','p4_dag_build_us','p4_dag_build_over_direct','p4_prop_candidates','p4_prop_accepted','p4_prop_fold_lowerings','p4_native_accepted','p3_accepted','p2_accepted','p2_planned_lowerings','direct_multiplications','p4_prop_multiplications','p3_multiplications','p2_multiplications','direct_pair_terms','p4_prop_pair_terms','p3_pair_terms','p2_pair_terms','direct_anf_nodes','p4_prop_anf_nodes','p3_anf_nodes','p2_anf_nodes','direct_peak_monomials','p4_prop_peak_monomials','direct_python_peak_bytes','p4_prop_python_peak_bytes']
 out=HERE/('N2_P4_NATURAL_CASE_SUMMARY.csv' if corpus=='natural' else 'N2_P4_GATEP_CASE_SUMMARY.csv')
 with open(out,'w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for c in cases:
   q=by[(c,P4_PROP)]; n=by[(c,P4_NATIVE)]; x=by[(c,P3)]; z=by[(c,P2)]; d=by[(c,DIRECT_META)]
   row={'case_id':c,'circuit':q.get('circuit',''),'support':q.get('support',''),'source_nodes':q.get('source_nodes',''),'depth':q.get('depth',''),
    'direct_lower_us':ml[(c,DIRECT_META)]/1000,'p4_native_lower_us':ml[(c,P4_NATIVE)]/1000,'p4_prop_lower_us':ml[(c,P4_PROP)]/1000,'p3_lower_us':ml[(c,P3)]/1000,
    'p4_prop_over_direct':ml[(c,P4_PROP)]/ml[(c,DIRECT_META)],'p4_prop_over_p3':ml[(c,P4_PROP)]/ml[(c,P3)],'p4_native_over_direct':ml[(c,P4_NATIVE)]/ml[(c,DIRECT_META)],
    'direct_build_pipeline_us':mp[(c,DIRECT_BUILD)]/1000,'p4_build_pipeline_us':mp[(c,P4_BUILD)]/1000,'p4_pipeline_over_direct':mp[(c,P4_BUILD)]/mp[(c,DIRECT_BUILD)],
    'direct_dag_build_us':mb[(c,DIRECT_BUILD)]/1000,'p4_dag_build_us':mb[(c,P4_BUILD)]/1000,'p4_dag_build_over_direct':mb[(c,P4_BUILD)]/mb[(c,DIRECT_BUILD)],
    'p4_prop_candidates':q.get('selector_candidates',0),'p4_prop_accepted':q.get('selector_accepted',0),'p4_prop_fold_lowerings':q.get('fold_lowerings',0),'p4_native_accepted':n.get('selector_accepted',0),'p3_accepted':x.get('selector_accepted',0),'p2_accepted':z.get('selector_accepted',0),'p2_planned_lowerings':z.get('planned_fold_lowerings',0)}
   for k in ['multiplications','pair_terms','anf_nodes_evaluated','peak_monomials','python_peak_bytes']:
    name={'anf_nodes_evaluated':'anf_nodes','peak_monomials':'peak_monomials','python_peak_bytes':'python_peak_bytes'}.get(k,k)
    row['direct_'+name]=d.get(k); row['p4_prop_'+name]=q.get(k)
    if k in ('multiplications','pair_terms','anf_nodes_evaluated'):
     row['p3_'+name]=x.get(k); row['p2_'+name]=z.get(k)
   w.writerow(row)
 return out

write_csv('natural');write_csv('gatep')
# depth aggregation from case medians
low=D['gatep_lower_timing_rows']; ml=medmap(low,'lower_ns')
depth={}
for dep in (6,8,10):
 cs=[f'{dep}:{i}' for i in range(12)]
 vals=[ml[(c,P4_PROP)]/ml[(c,DIRECT_META)] for c in cs]
 depth[str(dep)]={'geomean_p4_prop_over_direct':gm(vals),'median':statistics.median(vals),'cases_below_1':sum(v<1 for v in vals)}
(HERE/'N2_P4_DEPTH_SUMMARY.json').write_text(json.dumps(depth,indent=2)+'\n')
