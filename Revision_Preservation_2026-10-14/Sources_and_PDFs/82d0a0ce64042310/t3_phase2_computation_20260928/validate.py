from common import *
from state import State
from itertools import product
import copy,random,argparse

def main(native=False):
    counts=Counter();start=time.perf_counter()
    sys.path.insert(0,str(PRIOR/'inputs/baseline/CM_COMPUTATION_BASELINE_HANDOFF/reproducibility/code'))
    from artifacts import matrix_rows,rank_factor
    if native:from comparators import Native,Raw,Histogram,cudd_blob
    def check(c,k):
        variants=[('row',False),('column',False),('row',True),('column',True)]
        for orient,dense in variants:
            src=copy.deepcopy(c);state=State(src,k,orient,dense);src['U'][:]=[None]*len(src['U']);src['W'][:]=[None]*len(src['W'])
            assert not hasattr(state,'__dict__') and not hasattr(state,'U');counts['source_disposal']+=1
            def walk(st,rho):
                assert st.count()==oracle(c,rho);counts['t3_prefix_checks']+=1
                blob=st.dumps();rebuilt=State.loads(blob);assert rebuilt.count()==st.count();assert rebuilt.dumps()==blob;counts['residual_roundtrips']+=1
                try:State.loads(blob+b'x')
                except ValueError:pass
                else:raise AssertionError('trailing byte accepted')
                if st.h:
                    for z in c['left']+c['right']:
                        if z in rho:continue
                        for b in (0,1):
                            nxt=State.loads(blob);d=len(nxt.free_a if z in nxt.free_a else nxt.free_b);expected=nxt.s*D(d-1,nxt.h-1)
                            nxt.update(z,b);assert nxt.last_operations==expected;counts['update_work_checks']+=1
                            walk(nxt,{**rho,z:b})
                else:
                    try:st.update(999,0)
                    except ValueError:counts['budget_rejections']+=1
                    else:raise AssertionError('budget accepted')
            walk(state,{})
        if native:
            for method in ('packed','cudd','raw','histogram'):
                obj=Native.packed(c) if method=='packed' else Native.loads(cudd_blob(c)) if method=='cudd' else Raw(c) if method=='raw' else Histogram(c)
                original=obj.dumps()
                # All distinct-coordinate sequences at full depth; initialize each sequence afresh.
                from itertools import permutations
                for order in permutations(c['left']+c['right']):
                    for bits in product((0,1),repeat=c['n']):
                        o=type(obj).loads(original);rho={};assert o.count()==oracle(c,rho)
                        for z,b in zip(order,bits):
                            o.update(z,b);rho[z]=b;assert o.count()==oracle(c,rho);counts['compiled_or_baseline_prefix_checks']+=1
                            if method in ('packed','cudd'):assert Native.loads(o.dumps()).count()==o.count()
                counts['comparator_cases']+=1
    for n in range(4):
        # Deliberately non-contiguous coordinate names and reversed cut order.
        names=list(range(2,2+2*n,2));left=list(reversed(names[:n//2]));right=[x for x in names if x not in left]
        for truth in range(1<<(1<<n)):
            rows,_=matrix_rows(truth,tuple(names),tuple(left));u,b=rank_factor(rows);w=[sum(((v>>j)&1)<<i for i,v in enumerate(b)) for j in range(1<<len(right))]
            c=dict(n=n,p=len(left),q=len(right),r=len(b),left=left,right=right,U=list(u),W=w)
            for k in range(n+1):check(c,k)
            counts['boolean_functions']+=1
    rng=random.Random(20260928)
    # Unequal cuts, inflated width/cancellation and gauge relabeling tests.
    for p,q,r in [(0,2,2),(2,0,2),(1,3,3),(3,1,4),(2,2,3)]:
        for _ in range(12):
            c=dict(n=p+q,p=p,q=q,r=r,left=list(range(p)),right=list(range(p,p+q)),U=[rng.randrange(1<<r) for i in range(1<<p)],W=[rng.randrange(1<<r) for i in range(1<<q)])
            # Independent random legal paths; exhaustive full continuation is above.
            for orientation in ('row','column'):
                s=State(c,c['n'],orientation);rho={};order=rng.sample(c['left']+c['right'],c['n'])
                assert s.count()==oracle(c,{})
                for z in order:
                    b=rng.randrange(2);s.update(z,b);rho[z]=b;assert s.count()==oracle(c,rho);counts['unequal_inflated_checks']+=1
            # Swap factor bit coordinates: invertible gauge, dot product invariant.
            def swap(v):return (v&~3)|((v&1)<<1)|((v&2)>>1)
            cg={**c,'U':list(map(swap,c['U'])),'W':list(map(swap,c['W']))}
            a,b=State(c,min(2,c['n'])),State(cg,min(2,c['n']))
            assert a.count()==b.count() and a.payload_bits()==b.payload_bits();counts['gauge_checks']+=1
    out={'status':'PASS','counts':dict(counts),'seconds':time.perf_counter()-start,'native':native,'source_hashes':{p.name:sha(p.read_bytes()) for p in ROOT.glob('*.py')},'native_sha256':sha((ROOT/'native_count.so').read_bytes()) if native else None}
    write(ROOT/'results'/('correctness_native.json' if native else 'correctness_t3.json'),out);print(json.dumps(out,indent=2))
if __name__=='__main__':main('--native' in sys.argv)
