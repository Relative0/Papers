# Maximum-degree-two exclusive graphs

## Exact theorem

Let G_psi have maximum degree at most two. Suppose no C4 component has **both** its same-colour pairs comparable in Q. Then every mixed core has size at most three. With A, B, and h as in SPECTRAL_SEQUENCE_CONSTRUCTION.md,

    H_n(cone;R) = H_(n-1)(Cone(h:B->A)),
    E^2 = E^infinity,

over every coefficient ring. Acyclicity is equivalent to all H_q(h) being isomorphisms. Over fields, the kernel-plus-cokernel dimension formula is exact; integrally, use the chain cone or its natural short exact sequence, retaining extensions.

In particular this covers all disjoint unions of paths and even cycles of length at least six, with arbitrary available-link topology and arbitrary numbers of split states. It also covers C4 components with at least one incomparable colour pair. It is not a torsion-free or TU theorem.

## Proof of the structural restriction

For p,p' in P and z,z' in Z, transitivity gives

    p<p' implies N(p') subset N(p),
    z<z' implies N(z) subset N(z').

A mixed core is a biclique with both colour classes chains. Degree at most two bounds each class by two vertices, so cores have size at most four. A four-core requires K2,2, which in a degree-two graph is an entire C4 component, and it requires both same-colour pairs comparable. Conversely these comparisons in K2,2 form a four-core. Excluding this case leaves exactly two possible columns, and the exact chain-cone theorem applies.

## Stronger path and cycle classification

Two distinct same-colour degree-two vertices can be comparable only if they have identical neighbourhoods: inclusion plus equal cardinality forces equality. Such twins produce C4. It follows that:

* A C_(2k) component with k>=3 has no mixed 3-core. Its contribution is exactly the frozen coarse-edge-link sum, even though its graph is not a matching.
* In a path with at least three edges, a 3-core can occur only on the first two or last two edges. It consists of a leaf and its distance-two vertex, together with their common neighbour.
* For a P-coloured leaf a and degree-two P-vertex b, the only permitted comparison is b<a. For a Z-coloured leaf y and degree-two Z-vertex x, it is y<x. Reverse directions would force another exclusive edge.

Thus a path of at least four edges decomposes at chain level into at most two end-star blocks and individual interior edge blocks. The two end triples use disjoint edge sets. A path of three edges is exceptional only in that its two possible triples share the middle edge: use one three-edge/two-triple cone block. A two-edge path is the basic star block. These are exact decompositions, not just Betti-number identities.

The relative complex always splits over exclusive graph components, but the link attached to each block must still be computed in the full Q. Graph isomorphism type alone does not determine the answer.

## The remaining C4 case

If both sides are comparable, label the coarse chain a<b<x<y with a,b in P and x,y in Z. Put A=sum of four edge-link complexes, B=sum of four triple-link complexes, and V=Ctilde(Lambda_abxy). The exact complex is

    C_m(K,U) = A_(m-2) + B_(m-3) + V_(m-4),
    d(a,b,c) = (partial a+h b, -partial b+k c, partial c).

In triple order (abx,aby,axy,bxy), k has signs (-,+,-,+). The h maps are signed inclusions specified by

    h(abx)=bx-ax,   h(aby)=by-ay,
    h(axy)=ax-ay,   h(bxy)=bx-by.

Hence hk=0. The E2 columns are coker(Hh), ker(Hh)/im(Hk), and ker(Hk). The sole possible higher differential is

    d2:E2_(4,q) -> E2_(2,q+1).

For a cycle c in V_q with [kc]=0, choose b in B_(q+1) with partial b=kc; then d2[c]=[hb]. This is a complete chain-level computation and E3=E_infinity. It does not by itself prove E2 collapse.

The eight-state example in C4_COUNTEREXAMPLE_PROOF.md realizes d2 as an isomorphism Z->Z. Thus unrestricted maximum-degree-two E2-collapse is **false**, and the E3 bound is sharp even integrally.

There is nevertheless an exact acyclicity test for the full degree-two class: for every integer q, require the middle module ker(H_q h)/im(H_q k) to vanish and require the secondary map

    d2_q:ker(H_q k) -> coker(H_(q+1) h)

to be an isomorphism. Groups outside the supported degrees are zero. These conditions say exactly that all E3 groups vanish. A finite filtered module is zero exactly when its associated graded is zero, so they are necessary and sufficient for cone acyclicity. Apply this per component, together with the two-column and individual-edge blocks. For nonzero homology, the full chain complex retains the integral extension information that page groups alone omit.

## Status

The no-four-core theorem and its path/cycle classification are proved. The algebraic mechanism is classical. The contribution is an explicit recognition and block decomposition for this observation model. This meets Level B's exact interaction complex plus proved collapse criterion, with Level A-style acyclicity recognition on that restricted class; the conservative overall verdict is Level B. General integral cone homology cannot be advertised as the homology of abstract link-homology groups alone without the stated extension qualification.
