# Interaction-core spectral sequence: exact conventions and theorems

Gate date: 29 September 2026. This is a new research artifact. The transferred package and manuscript v0.3 remain frozen.

## 1. Model and homology convention

Let Q be a finite poset, with each state available at bit 0 only (Z), bit 1 only (P), or both bits (C). Let D=Q x {0<1}, K=Delta D, and L=Delta Q^psi. The missing sets are M0=P x {0} and M1=Z x {1}. Put K_P=K[V(K)\M0], K_Z=K[V(K)\M1], and U=K_P union K_Z.

Throughout, H_n(cone) means the homology of the algebraic mapping cone, equivalently **reduced** homology of the topological homotopy cofiber. The frozen reduction gives

    H_n(cone;R) = H_n(K,L;R) = H_(n+1)(K,U;R).

The mixed-core filtration is on C_*(K,U), not directly on C_*(K,L). The latter also has single-colour relative simplices. Conflating the pairs would give an incorrect first page and degree shift.

## 2. Oriented chain identification

A relative simplex has a unique nonempty mixed core S (at least one vertex from each missing colour) and an available simplex T in

    Lambda_S = lk_K(S)[V(L)].

Include the empty available simplex in augmented chain degree -1. Write S=(s_0,...,s_(p-1)) and T=(t_0,...,t_q), in their inherited orders. Orient the full simplex by listing S first and T second. Its sign relative to the original increasing order is the sign of this shuffle. The resulting basis is denoted S wedge T.

The relative boundary is exactly

    d(S wedge T) = sum_i (-1)^i (S\{s_i}) wedge T
                  + (-1)^p S wedge partial(T),

where a term whose remaining core is not mixed is zero. Deleting a missing vertex induces the actual inclusion Lambda_S -> Lambda_(S\{s_i}). Thus d=v+h, where v preserves p, h lowers p by one, and v^2=h^2=vh+hv=0. The equality h^2=0 uses cancellation of the two orders of deletion, including the identical inclusion maps to the common target.

This is a finite double complex, with total degree m=p+q. It is also an explicit general interaction complex **of link chains**. Replacing chains by homology and keeping only h is not valid in general.

## 3. Pages and convergence

Filter increasingly by F_p=span{relative simplices with at most p missing vertices}. Then

    E^0_(p,q) = direct_sum_(|S|=p) Ctilde_q(Lambda_S;R),
    d^0 = (-1)^p partial,
    E^1_(p,q) = direct_sum_(|S|=p) Htilde_q(Lambda_S;R),
    d^1 = sum_i (-1)^i (Lambda_S -> Lambda_(S\{s_i}))_*.

In the general spectral-sequence convention,

    d^r: E^r_(p,q) -> E^r_(p-r,q+r-1).

It converges to gr_F H_(p+q)(K,U;R), hence the associated graded of cone homology in degree n=p+q-1. The filtration is finite and exhaustive, so there are no convergence or completion qualifications. Over a general ring the abutment retains extension data.

For a class represented by x in column p with vx=0, d^1[x]=[hx]. If hx=-vy can be solved in column p-1, the next differential is represented by hy. This zigzag explains why d^2 can be nonzero although the original chain boundary lowers the filtration by at most one. The seven-state star in COUNTEREXAMPLES_AND_FAILURE_BOUNDARY.md realizes this phenomenon integrally.

## 4. Bounded-core collapse theorem

If every mixed core has size at most M>=2, then

    E^(M-1) = E^infinity.

Proof: nonzero columns lie in 2,...,M. A differential with r>=M-1 cannot connect two such columns. This is sharper than the proposed E^M bound, and is standard finite-filtration support reasoning. If there are no mixed cores, the chain complex is zero and the frozen isotone-section theorem additionally gives a homotopy equivalence.

The bound is sharp for M=4: the explicit K_(1,3) example has nonzero d^2 and stabilizes only on E^3.

## 5. Exact two-column theorem

Assume there is no mixed core of cardinality at least four. Define augmented chain complexes

    A = direct_sum_(|S|=2) Ctilde_*(Lambda_S;R),
    B = direct_sum_(|S|=3) Ctilde_*(Lambda_S;R),

and let h:B->A be the signed sum of link inclusions obtained by deleting a core vertex, retaining mixed faces. Use Cone(h)_k=A_k direct_sum B_(k-1), with boundary (a,b)->(partial a+h b,-partial b). Then there is an actual chain isomorphism

    C_*(K,U;R) = Cone(h)[2],
    H_n(cone;R) = H_(n-1)(Cone(h)).

Here a shift [2] raises total degree by two. The two nonzero filtration columns force E^2 collapse. The exact integral conclusion is the natural short exact sequence

    0 -> coker H_(n-1)(h) -> H_n(cone)
      -> ker H_(n-2)(h) -> 0.

Consequently **cone acyclicity is equivalent to h being a quasi-isomorphism**, including augmented link degree -1. This is necessary and sufficient, not just a sufficient fibre criterion. It is a homology statement, and must not be upgraded to homotopy equivalence.

Over a field k, the sequence splits noncanonically and

    dim H_n(cone;k) = dim coker H_(n-1)(h) + dim ker H_(n-2)(h).

Over Z it splits if the right-hand kernel is free abelian. No general splitting is asserted. If all relevant link homology groups are free abelian, this freeness condition holds, but cokernels can still have torsion. Over arbitrary coefficient rings, use the chain cone or the exact sequence without assuming projectivity.

## 6. One-column extension of the matching theorem

The following condition is equivalent to having no mixed 3-core:

    any two exclusive vertices of the same colour sharing an exclusive
    neighbour are incomparable in Q.

Indeed a comparable such pair and their common neighbour are exactly a mixed 3-core; every larger core contains one. Under this condition, every available edge link is the full product-edge link: any missing vertex in that link would create a 3-core. Thus the frozen matching proof applies unchanged and yields

    H_n(cone;R) = direct_sum_(p,z in E_psi)
                    Htilde_(n-2)(lk_(Delta Q)[p,z];R).

This **extends the hypothesis**, rather than altering the frozen theorem. It covers, for example, every exclusive even cycle of length at least six in the maximum-degree-two class.

## 7. Components and exact recursion for larger cores

Every mixed core lies in one connected component of the exclusive graph. A surviving boundary face stays in that component. Therefore C_*(K,U) decomposes as a direct sum over its nontrivial exclusive graph components. The available links still use the whole Q.

For arbitrary core size, let G_p be the column complex with (G_p)_m=direct_sum_(|S|=p) Ctilde_(m-p)(Lambda_S) and vertical differential (-1)^p partial. The horizontal maps give a degree-zero chain map

    h_p:G_p[-1] -> F_(p-1).

Then

    F_p = Cone(h_p).

This is an exact integral iterative computation retaining chains and extensions. It is standard filtered-chain algebra specialized to this model; it is not a closed formula in abstract link homology groups and is not an independent novelty claim.

## 8. Status and prior-art boundary

The spectral-sequence construction, mapping-cone long exact sequence, and support-based collapse are standard. Lambda_S is precisely an available-vertex obstruction complex in the sense of Chacholski--Jin--Scolamiero--Tombari. The model-specific content is the two-colour product reduction, the recognition of chain-supported mixed cores, the graph/transitivity restrictions proved in MAX_DEGREE_TWO_CLASSIFICATION.md, and the exact positive/negative consequences for observation refinement. See LITERATURE_PRIORITY_MAP.md for theorem-level comparisons.
