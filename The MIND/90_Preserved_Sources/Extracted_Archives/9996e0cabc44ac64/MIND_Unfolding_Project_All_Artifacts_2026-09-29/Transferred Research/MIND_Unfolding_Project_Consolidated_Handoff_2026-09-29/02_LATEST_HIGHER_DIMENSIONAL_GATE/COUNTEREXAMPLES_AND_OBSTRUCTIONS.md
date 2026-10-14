# Counterexamples and Obstructions

## 1. Forest is not enough

The first attempted extension of the matching theorem is false.

Take the coarse chain

\[
0<1<2
\]

and the availability profile

\[
0:\{1\},\qquad 1:\{0\},\qquad 2:\{0\}.
\]

The exclusive inversion graph has edges

\[
(0,1),\ (0,2),
\]

so it is the two-edge star `K_{1,2}`: a forest, but not a matching.

Direct integral relative homology is

\[
H_1\cong\mathbb Z.
\]

Yet both individual coarse edge links are contractible, so an edgewise direct-sum formula would give zero.

The obstruction is the relative 2-simplex

\[
(0,0)<(1,1)<(2,1),
\]

whose boundary couples the two inversion edges.  This is exactly a three-vertex missing core in the interaction filtration.

This is minimal by coarse-state count: a nonmatching bipartite graph requires at least three incident vertices.

## 2. Height three already allows torsion

The companion same-carrier theory has a cone-whisker realization transferring arbitrary reduced homology one degree upward, including `Z/2` from a finite `RP^2` model.  Carrier splitting contains that regime as a boundary case.

More strongly, the new matching theorem transfers arbitrary coarse-link homology two degrees upward while retaining a one-edge exclusive matching.  Hence torsion is not caused by complicated exclusive interaction.

## 3. Matching does not imply wedge of spheres

Choose a coarse edge link with homology or homotopy not equivalent to a wedge of spheres.  The matching formula transfers its reduced homology.  Therefore a universal wedge theorem would require additional hypotheses on the edge links, such as shellability or a suitable Cohen--Macaulay condition.

## 4. Matching does not imply total unimodularity

The realization theorem transfers torsion.  A chain complex with torsion homology cannot arise from a globally TU boundary theory of the kind sought in the prompt.  More generally, torsion-freeness of the resulting cone homology would still be weaker than total unimodularity of all boundary matrices.

## 5. Pure Horn closure is too strong for nontrivial topology

If the entire refined relation is meet-closed, it has a minimum; so does its projection.  Both order complexes are contractible.  Thus pure Horn closure yields a strong neutral theorem, but not a rich higher-dimensional classification.

## 6. Bounded height alone stops being rigid at height three

Weighted height at most two admits the previous rooted-incidence/TU theorem.  Height three admits torsion in the companion theory.  Therefore a clean coefficient-independent extension cannot be based on height alone beyond the known boundary.

## 7. Generic lower-fiber contractibility is sufficient but not exact

Quillen/Barmak fiber criteria correctly detect many homotopy equivalences, but they do not classify the noncontractible cases.  Björner--Wachs--Welker gives exact-looking wedge formulas only under connectivity hypotheses on all lower fibers.  The matching class deliberately permits arbitrary link topology, including torsion, so those hypotheses are not available uniformly.

## 8. Obstruction hierarchy suggested by computation

The core-size filtration identifies a natural obstruction hierarchy:

1. no exclusive edges: isotone-section neutrality;
2. exclusive matching: independent edge defects, exact link sum;
3. stars: first interaction terms from three-vertex cores;
4. larger bicliques: higher interaction terms;
5. unrestricted case: universality/torsion prevents a simple graph criterion.

This hierarchy is a better guide for the next theorem than graph acyclicity by itself.
