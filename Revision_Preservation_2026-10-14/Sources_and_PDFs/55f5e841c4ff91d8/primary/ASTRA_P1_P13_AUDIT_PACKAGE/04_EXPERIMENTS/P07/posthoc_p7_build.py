from __future__ import annotations
import cProfile, io, json, math, pstats, statistics, sys, tracemalloc
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import n2_p7_harness as h

def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))

def peak_for(root,kind):
    tracemalloc.start()
    if kind=='direct':
        f=h.base.Factory(); h.clone_dag(root,f)
    elif kind=='p7': h.build_cword(root)
    elif kind=='p6': h.build_p6(root)
    elif kind=='p5': h.build_p5(root)
    else: raise ValueError(kind)
    _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop(); return peak

rows=[]
for d,i,root,n,oracle in h.generate_gate_cases():
    vals={k:peak_for(root,k) for k in ('direct','p7','p6','p5')}
    rows.append({'case_id':f'{d}:{i}','depth':d,**vals,
                 'p7_over_direct':vals['p7']/vals['direct'],'p7_over_p6':vals['p7']/vals['p6'],'p7_over_p5':vals['p7']/vals['p5']})
summary={k+'_geomean':gm([r[k] for r in rows]) for k in ('p7_over_direct','p7_over_p6','p7_over_p5')}
(HERE/'P7_POSTHOC_BUILD_MEMORY.json').write_text(json.dumps({'rows':rows,'summary':summary},indent=2)+'\n')

# Qualitative cProfile on largest Gate-P source, construction only.
cases=h.generate_gate_cases(); root=max(cases,key=lambda t:h.base.reachable_nodes(t[2]))[2]
out=[]
for name,fn in [('direct',lambda: h.clone_dag(root,h.base.Factory())),('p7',lambda: h.build_cword(root)),('p6',lambda: h.build_p6(root)),('p5',lambda: h.build_p5(root))]:
    pr=cProfile.Profile(); pr.enable()
    for _ in range(2000): fn()
    pr.disable(); s=io.StringIO(); pstats.Stats(pr,stream=s).sort_stats('cumtime').print_stats(35)
    out.append(f'=== {name} ===\n{s.getvalue()}')
(HERE/'P7_POSTHOC_PROFILE.txt').write_text('\n'.join(out))
print(json.dumps(summary,indent=2))
