"""Untimed positive and boundary cases supplement the frozen prototype checks."""
from pathlib import Path
import hashlib
import json
from dispatch_diagnostics import h, base, GATE, TupleBoundFactory, exact_stats, ref_decision

HERE=Path(__file__).resolve().parent


def build(cls, multiplicity, filler, reuse_mode):
    f=cls()
    a,b=f.var(0),f.var(1)
    shells=[]
    operations=[(op,a,b,None) for op in ('and','or','xor')]
    operations += [(op,b,a,None) for op in ('and','or','xor')]
    operations += [('tf',x,y,t) for x,y in ((a,b),(b,a)) for t in range(16)
                   if t not in (0,15,12,10,3,5)]
    for op,x,y,t in operations[:multiplicity]:
        shells.append(f.tf(t,x,y) if op=='tf' else f.bin(op,x,y))
    for i in range(filler):
        x=f.var(2+2*i)
        y=f.var(3+2*i)
        if reuse_mode==0:
            f.bin('and',x,y)
        elif reuse_mode==1:
            f.bin('and',a,x)
        elif reuse_mode==2:
            f.nary('andn',(a,b,x,y))
        else:
            f.nary('orn',(a,a,a,a,x,y))
    # Repeat source construction calls must remain CSE hits, not new observations.
    for op,x,y,t in operations[:multiplicity]:
        f.tf(t,x,y) if op=='tf' else f.bin(op,x,y)
    return f


def main():
    rows=[]
    for multiplicity in (0,1,2,3,4,5,6,7,12,26):
        for filler in range(0,101):
            for reuse_mode in range(4):
                f=build(h.DeferredPairTelemetryFactory,multiplicity,filler,reuse_mode)
                g=build(TupleBoundFactory,multiplicity,filler,reuse_mode)
                s=exact_stats(f)
                old=f.dispatch(GATE)[0]
                new=g.dispatch_bool()
                assert old==new==ref_decision(s)
                assert list(f.cache)==list(g.cache)
                rows.append(dict(multiplicity=multiplicity,filler=filler,reuse_mode=reuse_mode,
                                 annotate=old,**s))
    # Demonstrate the latent 32-bit packing precondition without allocating huge DAGs.
    p=(0,(1<<32)+2)
    q=(1,2)
    assert p!=q and ((p[0]<<32)|p[1])==((q[0]<<32)|q[1])
    result=dict(exploratory=True,timed=False,cases=len(rows),passed=True,
                annotated=sum(r['annotate'] for r in rows),
                saturated_tf_cases=sum(r['multiplicity']==26 for r in rows),
                code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                prototype_sha256=hashlib.sha256((HERE/'dispatch_diagnostics.py').read_bytes()).hexdigest(),
                packing_collision=dict(pair1=p,pair2=q),rows=rows)
    (HERE/'targeted_dispatch_checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))


if __name__=='__main__':
    main()
