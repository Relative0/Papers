"""Implementation A: rooted repair graph, using disjoint sets; no matrices."""
from itertools import combinations

def analyze(n, pairs, q):
    relation = set(pairs)
    coarse = list(range(n))
    def find(parent, x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a,b in pairs:
        coarse[find(coarse,a)] = find(coarse,b)
    roots = sorted({find(coarse,x) for x in range(n)})
    desc = [(a,b) for a,b in pairs if (q>>a)&1 and not (q>>b)&1]
    vertices = {e:i for i,e in enumerate(desc)}
    root_index = {r:len(desc)+i for i,r in enumerate(roots)}
    parent = list(range(len(desc)+len(roots)))
    cyclic = False
    edges = []
    for a,b,c in combinations(range(n),3):
        if (a,b) not in relation or (b,c) not in relation:
            continue
        de = [vertices[e] for e in ((a,b),(a,c),(b,c)) if e in vertices]
        if not de:
            continue
        assert len(de) in (1,2)
        u,v = (de[0],root_index[find(coarse,a)]) if len(de)==1 else de
        edges.append((u,v,(a,b,c)))
        ru,rv = find(parent,u),find(parent,v)
        if ru==rv:
            cyclic=True
        else:
            parent[ru]=rv
    rootcounts = {}
    for v in root_index.values():
        r = find(parent,v)
        rootcounts[r] = rootcounts.get(r,0)+1
    safe = not cyclic and all(rootcounts.get(find(parent,v),0)==1 for v in range(len(parent)))
    return safe, len(desc), len(edges), len(roots)
