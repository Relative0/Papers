from itertools import product
import importlib.util
spec=importlib.util.spec_from_file_location('base','/mnt/data/verify_homotopy_preserving_observations.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)

def repair_graph(n,P,bits):
    Q=base.qrel(n,P,bits)
    hb,rs,mats=base.relative_data(n,P,Q)
    E=rs.get(1,[]); T=rs.get(2,[])
    comps=base.comparable_component_sets(n,P)
    comp_of={v:i for i,C in enumerate(comps) for v in C}
    eidx={e:i for i,e in enumerate(E)}
    # graph vertex labels: ('r',component) and ('e',edge_index)
    verts=[('r',i) for i in range(len(comps))]+[('e',i) for i in range(len(E))]
    gedges=[]
    triangle_profiles=[]
    for tri in T:
        a,b,c=tri
        faces=[(a,b),(a,c),(b,c)]
        dels=[f for f in faces if f in eidx]
        if len(dels)==1:
            u=('r',comp_of[a]); v=('e',eidx[dels[0]])
        elif len(dels)==2:
            u=('e',eidx[dels[0]]); v=('e',eidx[dels[1]])
        else:
            raise AssertionError(('deleted triangle should have 1 or 2 deleted edges',tri,bits,dels))
        gedges.append((u,v,tri))
        triangle_profiles.append((''.join(str(bits[x]) for x in tri),len(dels)))
    return hb,E,T,verts,gedges,triangle_profiles

def rooted_forest(verts,gedges):
    parent={v:v for v in verts}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]];x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra==rb:return False
        parent[rb]=ra;return True
    acyclic=True
    for u,v,_ in gedges:
        if not union(u,v): acyclic=False
    roots_per={}
    for v in verts:
        r=find(v); roots_per.setdefault(r,0)
        if v[0]=='r': roots_per[r]+=1
    return acyclic and all(k==1 for k in roots_per.values())

def run(maxn=6):
    totals=[]
    for n in range(1,maxn+1):
        pc=cases=neutral=neutral_nr=0
        for P in base.natural_posets(n):
            if base.height(n,P)>2: continue
            pc+=1
            for bits in product([0,1],repeat=n):
                cases+=1
                hb,E,T,V,G,prof=repair_graph(n,P,bits)
                neu=all(x==0 for x in hb)
                rf=rooted_forest(V,G)
                if neu!=rf:
                    raise AssertionError(('repair forest equivalence fail',n,bits,hb,E,T,G,prof))
                neutral+=int(neu)
                neutral_nr+=int(neu and not base.is_redundant(P,bits))
        totals.append((n,pc,cases,neutral,neutral_nr))
        print('n',n,'height<=2 posets',pc,'cases',cases,'neutral',neutral,'neutral_nonred',neutral_nr)
    print('ALL REPAIR-FOREST ASSERTIONS PASSED')
    return totals

if __name__=='__main__':
    run(6)
