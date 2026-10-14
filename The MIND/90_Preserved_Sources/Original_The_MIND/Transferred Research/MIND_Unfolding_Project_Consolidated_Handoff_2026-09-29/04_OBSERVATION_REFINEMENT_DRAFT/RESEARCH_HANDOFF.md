# Research handoff: Observation–Refinement Descent and Cone project

**Status:** Draft v0.2 created. Core mathematics checked. Not yet a submission manuscript.

## Main advance in this round

The proposed Observation–Refinement Descent and Cone theorem has been formalized in a relative good-cover setting:

- cover refinement induces a nerve map;
- different refinement choices are contiguous;
- under good-cover hypotheses the fine-to-coarse nerve map on the same support is a homotopy equivalence;
- for a changing support \(Y\subseteq X\), the mapping cone computes \(H_*(X,Y)\) up to the standard relative nerve identifications;
- for a sheaf/cosheaf, local-to-global reconstruction is handled by descent/colimits rather than by a Boolean conjunction formula.

## Important priority correction

A 2026 preprint by António Leitão, *It's All About Covers: Persistent Homology of Cover Refinements* (arXiv:2602.22784), explicitly develops cover refinements, contiguity of refinement maps, and propagation through nerve/co-nerve functors. Therefore the **contiguity/canonical-homology-map component is not a novelty claim** for this project.

The draft now says this explicitly.

## New structure extracted from the attached `Logical Complexes.tex`

The notes were useful. They led to two clean results:

1. **Boolean unfolding simplex theorem.** For parent \(1^m\), the parent plus all one-coordinate-flip children is an affine \(m\)-simplex.
2. **Exact-layer hypersimplex theorem.** The exact depth-\(k\) states form the vertices of the hypersimplex \(\Delta(m,m-k)\).

The notes' three-variable points \(111,110,101,011\) really do form a tetrahedron. The notes were wrong only in the suggestion that three points could form a 3-simplex or that XOR itself is a scalar distance.

## New exact finite model

The cumulative distinction-history complex
\[
K_r^{(m)}=\operatorname{sk}_r\Delta^{m-1}
\]
has a closed-form step defect:
\[
H_q(K_r,K_{r-1};R)
\cong H_q(\operatorname{Cone}(i_r))
\cong
\begin{cases}
R^{\binom{m}{r+1}},&q=r,\\
0,&q\ne r.
\end{cases}
\]

For \(m=4\):

- \(K_0\): four vertices;
- \(K_1\): \(K_4\), with \(\beta_1=3\);
- \(K_2\): tetrahedral boundary, with \(\beta_2=1\);
- \(K_3\): filled tetrahedron, contractible.

This is a much cleaner prototype of successive differentiation than the older ad hoc path-cycle-disk example.

## Interaction with the existing ProLT program

The draft distinguishes three operations that had previously risked being conflated:

1. **Observation vocabulary extension**: add formulas; topology becomes finer and observational equivalence can split.
2. **Same-carrier order thinning**: a new observation factors through the current \(T_0\) quotient; points do not split, only order relations are removed. The companion height-two rooted-forest theorem applies here.
3. **Cover refinement**: local pieces of a support refine other local pieces; the nerve/refinement theorem applies here.

This separation should remain explicit in all future drafts.

## Strongest next theorem

The strongest next target is now more specific than the original cover-refinement theorem:

### Carrier-Splitting Cone Theorem

When a new observation separates worlds that were previously a single point in the current \(T_0\) quotient, construct a canonical span/correspondence between the old and new order complexes and classify the mapping-cone homology in terms of the split fibers.

This target sits exactly between:

- the existing **same-carrier one-bit order-thinning** theorem, and
- the current **cover-refinement relative-cone** theorem.

A successful theorem here would be much more project-specific and less vulnerable to being only a repackaging of standard nerve theory.

## Secondary next target

Characterize when an observation-generated concept cover is **pair-good** directly from finite observation/incidence data. A finite combinatorial criterion would strengthen the main theorem by making its hypotheses checkable from the logical model itself.

## Files

- `Observation_Refinement_Descent_and_Cone_Draft_v0.2.tex`
- `Observation_Refinement_Descent_and_Cone_Draft_v0.2.pdf`
- `LOGICAL_COMPLEXES_NOTES_AUDIT.md`
- `verify_unfolding_complexes.py`
- `verification_results.json`
