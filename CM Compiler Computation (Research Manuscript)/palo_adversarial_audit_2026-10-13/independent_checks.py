"""Independent, bounded audit diagnostics. No network; writes only beside this script."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
from collections import Counter
import importlib.util, json, hashlib, time

OUT=Path(__file__).resolve().parent
checks=Counter()
def check(group, condition):
    assert condition, group
    checks[group]+=1
def mul(values):
    r=Q(1)
    for v in values:r*=v
    return r
def table_value(c,p,q):
    return c[(1-p)*2+(1-q)]
def extension(c,p,q):
    return sum(Q(v)*mul((p if x else 1-p,q if y else 1-q)) for v,(x,y) in zip(c,[(1,1),(1,0),(0,1),(0,0)]))

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def main():
    start=time.perf_counter()
    tables=list(product((0,1),repeat=4))
    for c in tables:
        a,b,e,d=c
        for p,q in product([Q(i,7) for i in range(8)],repeat=2):
            for r in (max(Q(0),p+q-1),min(p,q),p*q):
                weights=[r,p-r,q-r,1-p-q+r]
                direct=sum(v*w for v,w in zip(c,weights))
                check('joint_law',direct==d+(b-d)*p+(e-d)*q+(a-b-e+d)*r)
                check('dependence',direct-extension(c,p,q)==(a-b-e+d)*(r-p*q))
    # Exhaustive exact polynomial-identity rejection via independent unisolvent grids.
    # Two binary child tables each use a variable at most once. The outer bilinear
    # kernel raises any shared variable degree to <=2; three distinct points per
    # variable therefore decide identity, rather than merely sample it.
    folds=[]
    for name,n,left,right in [('same_frame',2,(0,1),(0,1)),('overlap',3,(0,1),(1,2)),('disjoint',4,(0,1),(2,3))]:
        rejected=0
        grid=list(product((Q(0),Q(1,2),Q(1)),repeat=n))
        corners=list(product((0,1),repeat=n))
        # Cache child kernel evaluations.
        lk=[[extension(c,point[left[0]],point[left[1]]) for point in grid] for c in tables]
        rk=[[extension(c,point[right[0]],point[right[1]]) for point in grid] for c in tables]
        for k,c1,c2 in product(range(16),repeat=3):
            outer=tables[k]
            values=[table_value(outer,table_value(tables[c1],x[left[0]],x[left[1]]),table_value(tables[c2],x[right[0]],x[right[1]])) for x in corners]
            safe=True
            for idx,point in enumerate(grid):
                recursive=extension(outer,lk[c1][idx],rk[c2][idx])
                whole=sum(v*mul(t if b else 1-t for b,t in zip(bits,point)) for v,bits in zip(values,corners))
                if recursive!=whole:
                    safe=False;break
            rejected+=not safe
        check('composition_count_reproduction',rejected=={'same_frame':1880,'overlap':1440,'disjoint':0}[name])
        folds.append({'family':name,'circuits':4096,'rejected':rejected,'preserved':4096-rejected,
                      'reason_grid_is_decisive':'coordinate degrees <=2; tensor grid of three distinct points is unisolvent'})
    for a,b in product([Q(i,9) for i in range(1,46)],repeat=2):
        hs=[a-b-a*b,-a+b-a*b,-a-b+a*b]
        check('guard_pair_sums',hs[0]+hs[1]==-2*a*b and hs[0]+hs[2]==-2*b and hs[1]+hs[2]==-2*a)
        if 0 in hs:continue
        actual=(1,*(int(h>0) for h in hs))
        decoder={(0,0):(1,0,0,0),(1,0):(1,1,0,0),(0,1):(1,0,1,0),(1,1):(1,0,0,1)}
        check('quartic_dispatch',actual==decoder[(int(hs[0]*hs[2]<0),int(hs[1]*hs[2]<0))])
    p=Q(1,2)
    examples={'and_repeat':str(p*p),'event_repeat':str(p),'primitive_equivalence':str(extension((1,0,0,1),p,p)),
              'two_implications':str((1-p+p*p)**2),'value_error_p_squared_to_p':'99/10000',
              'input_gradient_error_sup':'1', 'real_switch_at_half':[[str(p),str(1-p)],[str(1-p),str(p)]]}
    # Audit checker domain validation: replay currently accepts negative magnitude
    # contracts, although extract itself rejects them. This does not falsify the
    # polynomial range theorem; it limits the advertised signed-magnitude interface.
    paths=list((OUT/'snapshots').rglob('exact_extraction_demo.py'))
    interface=None
    if paths:
        m=load(paths[0],'extraction_snapshot')
        bounds=m.box(a=Q(-1,2),b=Q(1,2))
        vs=m.vertices(bounds); rows=[];bits=[]
        for alpha in m.FRAME:
            vals=[m.score_original(z,alpha) for z in vs];lo,hi=min(vals),max(vals)
            rows.append({'alpha':list(alpha),'min':str(lo),'max':str(hi),
                         'min_vertex':list(map(str,vs[vals.index(lo)])), 'max_vertex':list(map(str,vs[vals.index(hi)])),
                         'attained_signs':(['-'] if lo<0 else [])+(['0'] if lo<=0<=hi else [])+(['+'] if hi>0 else []),
                         'status':'MIXED' if lo<0<hi else 'TIE_PRESENT' if lo<=0<=hi else 'STRICT'})
            bits.append(1 if lo>0 else 0 if hi<0 else None)
        cert={'model':m.MODEL,'frame':[list(a) for a in m.FRAME],'bounds':m.serial_box(bounds),'range_proof':'multi-affine box interpolation',
              'rows':rows,'status':'EXACT' if all(b is not None for b in bits) else 'NONEXACT','truth_vector':bits if all(b is not None for b in bits) else None}
        cert['contract_sha256']=hashlib.sha256(json.dumps({k:cert[k] for k in ('model','frame','bounds')},sort_keys=True).encode()).hexdigest()
        interface={'extract_status':m.extract(bounds)['status'],'replay_accepts_negative_magnitude':m.replay(cert,bounds),'certificate':cert}
        check('replay_domain_gap',interface['extract_status']=='UNKNOWN' and interface['replay_accepts_negative_magnitude'])
    result={'status':'PASS','checks_by_family':dict(checks),'total_assertions':sum(checks.values()),'independent_composition_counts':folds,
            'examples':examples,'extraction_interface_probe':interface,'elapsed_seconds':time.perf_counter()-start,
            'scope':'Exact finite diagnostics and exhaustive bounded composition identities; no source-wide proof, learning or performance validation.',
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (OUT/'independent_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='extraction_interface_probe'},indent=2))

if __name__=='__main__':main()
