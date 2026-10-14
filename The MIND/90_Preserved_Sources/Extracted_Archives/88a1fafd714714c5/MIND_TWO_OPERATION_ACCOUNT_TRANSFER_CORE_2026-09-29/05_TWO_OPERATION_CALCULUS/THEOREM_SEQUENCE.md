# Proposed Theorem Sequence and Status

Status labels:

- **S** = standard/known structure;
- **A** = elementary project specialization/derived result;
- **P** = project-specific result already present in supplied ProLT work;
- **C** = contribution candidate needing dedicated novelty audit.

## T1. Observation partition theorem — S

Every finite observation family `Phi` induces the equivalence relation

\[
x\sim_\Phi y\iff o_\Phi(x)=o_\Phi(y),
\]

hence a canonical partition and finite Boolean algebra of definable unions of cells.

## T2. Refinement theorem — S / P

Adding observations refines the indiscernibility partition. In ProLT it also enlarges the positive topology and thins the specialization preorder. The latter formulation is already in the current ProLT manuscript.

## T3. Measurement theorem — S

Hard Boolean outcome measurement is event restriction

\[
M_E(S)=S\cap E,
\]

with idempotent commuting diagonal characteristic projector.

## T4. Two-axis factorization theorem — A

The primitive fixed-carrier operations act on separate coordinates:

\[
R_\psi(S,\Phi)=(S,\Phi+\psi),
\qquad
M_E(S,\Phi)=(S\cap E,\Phi).
\]

## T5. Commutation / normal-form theorem — S / already P internally

For fixed ambient events/tests, every refinement commutes with every hard conditioning. Any finite sequence reduces to the union of refinements plus the intersection of outcome events.

This is elementary, and the post-T0 simplicial version is already Theorem 8.1 in ProLT v0.3.

## T6. Pair-ambiguity monotonicity theorem — A

\[
A_2(S,\Pi)=\sum_C {|S\cap C|\choose2}
\]

is nonincreasing under both partition refinement and support restriction.

## T7. Invisible-symmetry theorem — A

The group

\[
G_{inv}(S,\Pi)=\prod_C Sym(S\cap C)
\]

shrinks under both operations, and `A_2` is exactly the number of within-cell transpositions.

## T8. Relative-purity theorem — S / A

A world is observationally pure relative to `(S,Phi)` iff its signature cell intersects `S` only in that world. Cylinder extension by `m` unconstrained Boolean variables multiplies semantic support cardinality by `2^m`.

## T9. Minimal separation theorem — S

With arbitrary yes/no tests, full separation of `N` worlds needs exactly `ceil(log2 N)` tests. With a supplied restricted test pool, minimum separation is Test Cover and is NP-hard in general.

## T10. CM realization theorem — A

For binary `Theta`, compact CM truth data, event `E_Theta`, and diagonal projector `D_Theta` are canonically equivalent encodings of the four truth values. The 4x4 diagonal map embeds Boolean conjunction as projector product.

## T11. Pre-T0/post-T0 refinement dichotomy — P

Before T0, a new observation may split quotient points. After T0, refinement cannot split vertices and acts by deletion of specialization comparisons. This is already a central result/boundary of the current ProLT program.

## T12. Typed measurement-availability theorem — A

If operational events at interface `Phi` are `A_Phi`, refinement yields `A_Phi subseteq A_Psi`. An event can therefore be persistent, newly enabled, or still unavailable. A newly enabled measurement does not create a noncommuting square; the earlier arrow is absent.

## T13. ProLT refinement/update bifiltration — P

For post-T0 observation sequence `Phi_a` and decreasing support sequence `S_b`, the existing complexes

\[
K_{a,b}=\Delta(P_{\Phi_a,S_b})
\]

form commuting inclusion squares and, after index reversal, a two-parameter filtration.

## T14. Nonclassicality boundary theorem — S-level structural criterion

If all effects embed into one global Boolean event algebra and updates are restrictions, the theory admits a classical global event model. To obtain contextual nonclassicality, add contextwise compatibility/effect data for which no global Boolean assignment exists, or add a distinct nonclassical state/instrument contract.

## Research conclusion

No theorem in T1--T14 should presently be advertised as a newly discovered foundational theorem solely because it is phrased in CM/ProLT notation. The strongest project-specific mathematical content remains on the richer ProLT refinement side (order thinning, homology, repair forests, simultaneous interactions). The two-operation paper can nevertheless be valuable as the integration theorem/interface that makes those results interact cleanly with conditioning.
