import json,math,statistics,tracemalloc,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; sys.path.insert(0,str(HERE))
import n2_p5_harness as h

def peak_build(root,kind):
    tracemalloc.start()
    if kind=='direct': f=h.base.Factory()
    elif kind=='p4': f=h.p4.MetaFactory()
    elif kind=='p5': f=h.PackedMetaFactory()
    else: raise ValueError(kind)
    rr,_=h.clone_dag(root,f)
    _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    return peak

def gm(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
rows=[]
for depth,i,root,n,oracle in h.generate_gate_cases():
    vals={k:peak_build(root,k) for k in ('direct','p4','p5')}
    rows.append({'case_id':f'{depth}:{i}','depth':depth,**vals,'p5_over_direct':vals['p5']/vals['direct'],'p5_over_p4':vals['p5']/vals['p4']})
out={'gatep_cases':len(rows),'p5_over_direct_geomean':gm([r['p5_over_direct'] for r in rows]),'p5_over_p4_geomean':gm([r['p5_over_p4'] for r in rows]),'rows':rows}
(HERE/'P5_POSTHOC_BUILD_MEMORY.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
