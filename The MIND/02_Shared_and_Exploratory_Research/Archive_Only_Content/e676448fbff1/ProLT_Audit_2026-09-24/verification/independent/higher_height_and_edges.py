"""Additional independently proved extensions and edge-case regression tests."""
from audit_checks import *

def cone_whisker(source,name):
    data=json.loads((OUT/source).read_text())
    n=data['n']; r=set(map(tuple,data['P_strict']))
    z=next(x for x in range(n) if not any(b==x for a,b in r))
    p=r|{(v,n) for v in range(n)}
    labels=[0 if v==z else 1 for v in range(n)]+[0]
    q=thin(n+1,p,labels)
    assert q==r|{(z,n)}
    betti={str(pr):relative_betti(n+1,p,q,pr) for pr in (2,3,5)}
    rec={'name':name,'n':n+1,'chosen_minimal_element':z,'labels':labels,
         'P_strict':sorted(p),'Q_strict':sorted(q),'relative_betti':betti,
         'proof':'P is cone on R; Q is R plus a whisker at minimal z. H_k(P,Q;Z)=reduced H_(k-1)(Delta R;Z).',
         'relative_torsion_degree':2,'relative_torsion':data['relative_H1_torsion']}
    dump(name+'.json',rec)
    return rec

if __name__=='__main__':
    a=cone_whisker('torsion2_RP2_13.json','onebit_height3_torsion2_14')
    b=cone_whisker('torsion3_Moore_79.json','onebit_height3_torsion3_80')
    assert a['relative_betti']['2']==[0,0,1,1]
    assert b['relative_betti']['2']==[0,0,0,0]
    assert b['relative_betti']['3']==[0,0,1,1]
    # Empty and singleton carriers; contradictory / tautological / duplicated bits.
    checked=0
    for n in range(5):
        for p in natural_posets(n,2):
            for labels in it.product(range(2),repeat=n):
                q=thin(n,p,labels)
                assert thin(n,p,[0]*n)==p==thin(n,p,[1]*n)
                assert thin(n,p,[3*x for x in labels])==q # duplicated observation
                for pr in (2,3,5):
                    assert relative_betti(n,p,q,pr)==relative_betti(n,p,thin(n,p,[3*x for x in labels]),pr)
                checked+=1
    dump('edge_case_checks.json',{'cases':checked,'status':'PASS','prime_fields':[2,3,5]})
    print(json.dumps({'onebit_h3_examples':[a['relative_betti'],b['relative_betti']],'edge_cases':checked},indent=2))
