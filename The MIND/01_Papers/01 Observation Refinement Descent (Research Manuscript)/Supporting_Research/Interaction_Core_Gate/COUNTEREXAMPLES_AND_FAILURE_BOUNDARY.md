# Counterexamples and failure boundary

## Preserved earlier negative results

Nothing in this gate repairs or suppresses the old failures: the historical unfolding rule is not a simplicial differential and is not Boolean-presentation invariant; cycles are not symmetry; proper faces alone do not determine a filler. The frozen three-chain K1,2 counterexample still defeats replacing matching by forest in the coarse-edge-link formula. Matching still permits arbitrary torsion and does not imply total unimodularity. Whole refined Horn/dual-Horn closure remains neutral.

The new results concern the precise interaction filtration, not those already settled claims.

## 1. Seven-state star: forests, Ferrers, and chordal-bipartite graphs need d2

Take Q with Hasse covers

    0<1, 0<2, 1<3, 2<3, 2<5, 3<4, 3<6, 5<6,

and availability (1,2,0,0,2,2,0), where 0 means zero-only, 1 one-only, 2 split. Thus P={0}, Z={2,3,6}, C={1,4,5}; the exclusive graph is K1,3. The Z vertices form a chain 2<3<6, producing a mixed four-core.

Over Z, the only nonzero E1 terms are

    E1_(2,1)=Z², E1_(4,0)=Z.

There are no nonzero triple-core link groups, so E2=E1. The available links for edges 02 and 06 have reduced H1=Z; the third edge link is contractible. The four-core link is the two points (0,1),(2,0), with reduced H0=Z. All other available links are acyclic.

To identify the abutment independently, let R=Q\{0}. Its order complex has facets 134,136,234,236,256. It is contractible: the lower ideals of its maxima 4 and 6 are contractible, with contractible intersection R_<=3. The split induced subposet C={1,4,5} is the edge 1<4 and an isolated vertex 5. The star-pair reduction gives

    H_n(cone)=H_(n-1)(Delta R,Delta C),

so the only nonzero cone group is H2=Z. The only possible differential can therefore only be

    d2:Z -> Z²,

and it is a primitive injection of rank one. Otherwise E_infinity would have the wrong free rank or torsion. The explicit signed chain witness in star_d2_integral_certificate.json verifies this directly. E3=E_infinity.

This disproves E2-collapse for forests, Ferrers graphs, and chordal-bipartite graphs, even when E1 groups are free. Seven states is the smallest induced restriction of the found witness, not a proved global minimum. Exhaustive computation through five coarse states found no d2; the six-state boundary is not settled by the random sample.

## 2. Eight-state C4: degree two also permits d2

Take Q=A2 ordinal-sum R ordinal-sum A2, with bottom antichain {a,a'}, top antichain {y,y'}, and middle R={v,b,w,x} with precisely the strict relations v<x, b<w, b<x. Set P={a,b}, Z={x,y}, and split the remaining four states. Then a<b<x<y and G_psi=K2,2 has maximum degree two.

The exact available-link calculation gives

    E1_(2,1)=Z (edge ay), E1_(4,0)=Z,

with all other terms zero. Thus d1=0. The d2 map is multiplication by a unit, and the cone is acyclic. C4_COUNTEREXAMPLE_PROOF.md gives a geometric loop/filling proof; the integral certificate records the signed chains and exact SNF checks.

This shows E3 is a sharp general bound for maximum degree two. It does not refute the positive theorem excluding a C4 with both same-colour pairs comparable. Minimality is only within the tested restrictions/search, unless a future exhaustive certificate states more.

## 3. Torsion genuinely created by interaction

Take Q={p}+R with p one-only and every state of R zero-only, where R is the face poset of the explicit six-vertex triangulated projective plane in verify_torsion_star.py. There are 32 coarse states and graph K1,31.

All 181 available core links have reduced H0=Z and no torsion. All 31 coarse exclusive-edge links are circles in homology (reduced H1=Z). Nevertheless the integral d1 complex is the ordinary simplicial chain complex of Delta R up to degree shift/sign, so

    H1(cone)=Z, H2(cone)=Z/2.

This establishes interaction-created torsion separately from the frozen inherited-torsion matching examples. It is not a minimality result. Exact SNF was performed on the reduced interaction complex and every link; no direct SNF of the entire doubled 32-state pair is claimed.

## 4. False inferences explicitly rejected

* A boundary that lowers filtration by at most one need not make d2 vanish; zigzag corrections cause higher differentials.
* E2 collapse is not a canonical integral direct-sum decomposition. Extensions must be retained.
* Signed core incidence does not make induced maps on link homology scalar incidence matrices or imply TU.
* Outside the one-column criterion, available links cannot be replaced by full coarse edge links.
* A graph cycle need not create interaction: C6 and longer degree-two cycles have no chain-supported triple cores.
* Ferrers resolutions, chordal-bipartite independence complexes, and unweighted Dowker complexes do not automatically calculate this decorated relative complex.
* Small finite-field searches are not integral or universal collapse proofs. No six-state global d2 minimality claim is made.

## 5. Remaining boundaries

The two- and three-column chain formulas are exact over arbitrary coefficients. They do not supply a general homology-only splitting theorem. The smallest possible interaction-created torsion model and the globally smallest d2 example remain open. A compatible chain contraction/formality condition capable of removing extension and secondary-operation data is a separate research target.
