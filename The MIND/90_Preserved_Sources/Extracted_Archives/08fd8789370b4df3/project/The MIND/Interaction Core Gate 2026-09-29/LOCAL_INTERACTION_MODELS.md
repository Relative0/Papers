# Exact local interaction models

All links below are available links Lambda_S unless explicitly called coarse links. Formulas use missing-first orientation and augmented chains. The coefficient ring is arbitrary.

## K1,2 and K2,1

For P-centre p with Z-leaves z1,z2, incomparable leaves give no triple core; the coarse-edge-link sum is exact. If z1<z2, let e_i=(p0,z_i1) and t=(p0,z1_1,z2_1). Then

    h:Ctilde(Lambda_t) -> Ctilde(Lambda_e1)+Ctilde(Lambda_e2)
      = (inclusion,-inclusion),
    H_n(cone) = H_(n-1)(Cone h).

The dual K2,1 case follows by reversing Q and swapping bits (or the same oriented-boundary calculation).

For the frozen three-chain (1-only,0-only,0-only), the first edge link and triple link are two points; the second edge link is an isolated point and an interval. Each has reduced H0=Z. The induced map is the primitive signed diagonal Z->Z². Thus d1 has rank one and H1(cone)=Z, with all other groups zero. The *coarse* edge links are contractible: this precisely explains why the old independent coarse-link formula fails.

## P4: three edges

Write edges ax,bx,by. The only possible triples are (b0,a0,x1) when b<a and (b0,y1,x1) when y<x. Their boundaries are ax-bx and by-bx. The two possible triple summands share the middle edge bx. Three edge-link summands and up to two triple-link summands form the exact mapping cone. There are no four-cores and no higher differential beyond d1.

## K2,2=C4

If both same-colour pairs are incomparable, four independent coarse-edge-link summands result. If exactly one pair is comparable, there are two triples and two independent star blocks. If both pairs are comparable, there are four edges, four triples, and one four-core, with the full integral three-column complex and d2 formula in MAX_DEGREE_TWO_CLASSIFICATION.md.

For the minimal chain with profile (1,1,0,0), all nine available links have reduced H0=Z. The horizontal complex has ranks 1->4->4, first map injective and second of rank three. It yields H1(cone)=Z, no other groups. An eight-state realization of the same graph instead has d2:Z->Z an isomorphism and acyclic cone; see C4_COUNTEREXAMPLE_PROOF.md. Thus graph type and maximum degree alone do not force E2 collapse.

## First chordal-bipartite non-Ferrers examples

Without connectedness, the smallest is 2K2, already a matching. With connectedness, it is P5 (four edges), not P4: P4 has nested neighbourhoods and is Ferrers. Write P5 edges ax,bx,by,cy. The only possible triples are bax if b<a and bcy if b<c; they have disjoint edge supports and give two independent star blocks.

## First even cycles

C4 is the first cycle and the only degree-two cycle allowing a four-core. For C6 and every longer even cycle, distinct same-colour vertices have distinct two-element neighbourhoods, so transitivity forbids comparable common-neighbour pairs. No triple core exists. The complete answer is the coarse-edge-link sum, with no interaction differential at all. In the minimal height-one realization of C6, all six coarse edge links are empty, so H1(cone)=Z^6.

## First demonstrated higher differential

The seven-state K1,3 witness in COUNTEREXAMPLES_AND_FAILURE_BOUNDARY.md has integral d1=0 but d2:Z->Z² primitive injective. It establishes E2 noncollapse on a tree/Ferrers/chordal-bipartite graph. It is minimal in its own induced-subposet search; global minimum state count is not claimed.

## Interaction-created torsion

The 32-state K1,31 construction in FERRERS_AND_CHORDAL_CASES.md has all available core links torsion-free (reduced H0=Z) and all coarse edge links torsion-free (reduced H1=Z). Its d1 creates Z/2 in H2(cone). This is a constructive existence result, not a smallest-example claim. The exact reduced interaction matrix and all links are verified integrally in interaction_torsion_star.json.

## Exact comparison with computation

The reproducible local-model and integral SNF records are supplied by verify_interaction.py and the supplemental audit scripts. A graph can admit different same-colour orders; each saved model specifies its coarse order and availability. No single small realization is claimed to classify all topologies carried by that graph.
