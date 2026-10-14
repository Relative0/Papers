from __future__ import annotations
import cProfile, io, json, math, pstats, statistics, tracemalloc, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import n2_p6_harness as h

def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))

def measure_build(root,kind):
    tracemalloc.start()
    if kind=='direct':
        f=h.base.Factory(); rr,_=h.clone_dag(root,f)
    elif kind=='p5':
        f=h.p5.PackedMetaFactory(); rr,_=h.clone_dag(root,f)
    else:
        f=h.InNodeFactory(); rr,_=h.clone_dag(root,f)
    _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return peak,len(f.nodes),f

rows=[]; target=None
for depth,i,root,n,oracle in h.generate_gate_cases():
    if (depth,i)==(10,2): target=root
    vals={}
    factories={}
    for kind in ('direct','p5','p6'):
        peak,count,f=measure_build(root,kind); vals[kind]=peak; factories[kind]=f
    rows.append({'case_id':f'{depth}:{i}','depth':depth,'direct_peak':vals['direct'],'p5_peak':vals['p5'],'p6_peak':vals['p6'],
                 'p6_over_direct':vals['p6']/vals['direct'],'p6_over_p5':vals['p6']/vals['p5'],'nodes':len(factories['p6'].nodes)})
summary={'p6_over_direct_geomean':gm([r['p6_over_direct'] for r in rows]),'p6_over_p5_geomean':gm([r['p6_over_p5'] for r in rows]),
         'p6_over_direct_median':statistics.median(r['p6_over_direct'] for r in rows),'p6_over_p5_median':statistics.median(r['p6_over_p5'] for r in rows)}
Path('P6_POSTHOC_BUILD_MEMORY.json').write_text(json.dumps({'summary':summary,'rows':rows},indent=2)+'\n')

# Profile build-only on one representative fold-rich case.
assert target is not None
out=[]
for kind in ('direct','p5','p6'):
    def work():
        for _ in range(300):
            if kind=='direct': f=h.base.Factory()
            elif kind=='p5': f=h.p5.PackedMetaFactory()
            else: f=h.InNodeFactory()
            h.clone_dag(target,f)
    pr=cProfile.Profile(); pr.enable(); work(); pr.disable()
    s=io.StringIO(); pstats.Stats(pr,stream=s).sort_stats('cumtime').print_stats(30)
    out.append(f'===== {kind} =====\n{s.getvalue()}')
Path('P6_POSTHOC_PROFILE.txt').write_text('\n'.join(out))
print(json.dumps(summary,indent=2))
