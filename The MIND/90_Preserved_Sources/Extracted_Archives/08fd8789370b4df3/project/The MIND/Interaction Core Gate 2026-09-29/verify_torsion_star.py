"""Exact integral interaction-created torsion in a Ferrers star.

This checks the reduced E1 interaction model, each available core link, and
each coarse edge link. It does not claim a direct SNF of the entire doubled
32-state example. The chain reduction is proved in FERRERS_AND_CHORDAL_CASES.md.
"""
from itertools import combinations
from pathlib import Path
import json
import verify_interaction as audit

b = audit.baseline
ROOT = Path(__file__).resolve().parent


def nonzero(h):
    return {str(k): v for k, v in h.items() if v['free'] or v['torsion']}


def main():
    facets = [(0,1,2),(0,1,3),(0,2,4),(0,3,5),(0,4,5),
              (1,2,5),(1,3,4),(1,4,5),(2,3,4),(2,3,5)]
    faces = sorted({tuple(s) for f in facets for k in (1,2,3)
                    for s in combinations(f,k)}, key=lambda s:(len(s),s))
    face_sets = [set(f) for f in faces]
    order = [[a <= c for c in face_sets] for a in face_sets]
    chains = b.chains(order)
    h = nonzero(b.ordinary_homology_Z(order))
    assert h == {'0': {'free':1,'torsion':[]}, '1':{'free':0,'torsion':[2]}}
    assert [sum(len(f)==k for f in faces) for k in (1,2,3)] == [6,15,10]
    edge_degrees = {e:sum(set(e)<=set(t) for t in facets) for e in combinations(range(6),2)}
    assert set(edge_degrees.values()) == {2}
    # Links in the original triangulation are connected cycles; establish
    # the closed triangulated surface directly rather than relying on a label.
    vertex_links = {}
    for v in range(6):
        link_edges = [tuple(x for x in f if x!=v) for f in facets if v in f]
        deg = {w:sum(w in e for e in link_edges) for w in range(6) if w!=v}
        assert set(deg.values()) == {2}
        seen={next(iter(deg))}
        while True:
            new=seen | {w for e in link_edges if any(x in seen for x in e) for w in e}
            if new==seen: break
            seen=new
        assert len(seen)==5
        vertex_links[v]={'vertices':5,'edges':5,'connected':True}
    # Q is a new minimum p plus R, with p one-only and R zero-only.
    # Coarse [p,z] edge links are precisely vertex links in Delta R.
    coarse_links=[]
    for z in range(len(faces)):
        vertices=[i for i in range(len(faces)) if i!=z and (order[i][z] or order[z][i])]
        link_order=b.induced_le(order,vertices)
        lh=nonzero(b.reduced_homology_Z(link_order))
        assert lh == {'1':{'free':1,'torsion':[]}}
        coarse_links.append({'state':z,'face':faces[z],'reduced_homology':lh})
    # Every mixed core is p0 followed by a nonempty R1 chain sigma.
    # Its available link is isolated p1 disjoint principal ideal R<=min sigma.
    core_checks=[]
    for dim, simplices in chains.items():
        for sigma in simplices:
            low=[i for i in range(len(faces)) if order[i][sigma[0]]]
            low_order=b.induced_le(order,low)
            link_order=[[True]+[False]*len(low)]
            link_order.extend([[False]+row for row in low_order])
            lh=nonzero(b.reduced_homology_Z(link_order))
            assert lh == {'0':{'free':1,'torsion':[]}}
            core_checks.append({'sigma':sigma,'core_size':len(sigma)+1,'link_homology':lh})
    # With canonical difference-of-components generators, d1 is the negative
    # ordinary simplicial differential of Delta R (deleting p kills mixedness).
    matrices={d:[[-x for x in row] for row in m] for d,m in b.integer_boundary(chains).items()}
    interaction_h=nonzero(b.homology_Z({d:len(s) for d,s in chains.items()},matrices))
    assert interaction_h==h
    out={
        'coarse_states':32,'exclusive_graph':'K_1,31','profile':'new minimum P; all 31 R states Z; no split states',
        'facets':facets,'face_vector':[6,15,10],'vertex_links':vertex_links,
        'R_homology_Z':h,'E1_q_row':0,'E1_link_groups':'all reduced H_0 = Z',
        'E1_link_count':len(core_checks),'E1_link_checks':core_checks,
        'coarse_edge_links':coarse_links,'d1_homology_Z':interaction_h,
        'cone_homology_Z':{'1':{'free':1,'torsion':[]},'2':{'free':0,'torsion':[2]}},
        'collapse':'E2 by single q=0 row','torsion_origin':'integral d1 interaction, not any available or coarse edge link',
        'verification_scope':'exact SNF of reduced E1 complex and every link; whole doubled pair not directly SNF tested',
        'minimality':'not claimed'}
    (ROOT/'interaction_torsion_star.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
    print(json.dumps({k:out[k] for k in ('coarse_states','exclusive_graph','E1_link_count','cone_homology_Z','verification_scope')}))


if __name__=='__main__':
    main()
