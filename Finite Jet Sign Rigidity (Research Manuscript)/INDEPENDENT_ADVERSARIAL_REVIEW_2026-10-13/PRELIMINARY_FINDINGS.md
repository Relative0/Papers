# Preliminary independent findings — 13 October 2026

Recorded after reading the complete current TeX source, before consulting any prior assessment, review report, research dossier, source diff, or package QA. No source verification has yet been completed. This file is preserved as the initial assessment, not retrospectively edited to match later findings.

## Version and independence

- TeX SHA-256: a9bb9bce6ab7aee4db9af72cc2b292386c5dd8ad47ddcec3e5c957e99513d079.
- PDF SHA-256: 3e574c5fea708bf599d5bcc4bf1b70bddce4c36e824684763a6944145d569bd3.
- Both match the requested version. No intervening change detected.
- Read the user-level AGENTS instructions. No additional AGENTS.md was found in the manuscript subtree or checked filesystem ancestors.
- The shared Git checkout has extensive unrelated pre-existing changes/deletions. They are outside this review's ownership.
- Work is single-reviewer, without delegation. Manuscript and prior packages remain read-only.

## Reconstruction

1. A nonzero polynomial satisfying weak chamber signs has a uniform crossing ratio across each hyperplane: extract its maximal linear factor, choose a generic point where the residual is nonzero, and propagate through the chamber graph. Uniqueness follows from a generic crossing of each distinct hyperplane.
2. The first nonzero homogeneous Taylor polynomial inherits the local signs along positive rays. This works for C^d, including d=0. For arrangements the local bits agree on overlapping neighborhoods and are locally constant along connected hyperplanes; this proves the stated smooth and uniform finite-order consequences.
3. In a divergent normalized Denjoy–Carleman class, a flat germ would violate off-wall nonvanishing. In a convergent class, the primitive of the square of a translated compactly supported function is zero on the negative half-line and strictly positive throughout the positive half-line. Product selectors have exactly one active term per chamber. Generic crossings distinguish the 2^(m+1) parity labels even when the arrangement sign vectors do not form a group.
4. Proposition 7.1 uses the preceding finite-order contrapositive at every order <=k. With D^kF(0)=0 the ray integral gives Beta(k,alpha+1)/(k-1)! = Gamma(alpha+1)/Gamma(k+alpha+1). The k=0 case is a direct Hölder bound. The balanced-corner substitution uses Euclidean radius sqrt(n) delta.
5. Remark 7.2 cancels j! in Taylor remainder and takes the infimum over j. Converting coordinate derivatives to a multilinear operator bound costs n^(j/2), absorbable into B. Gevrey optimization has exponent 1/(s-1), consistent with the factorial-out convention. These are fixed-budget consequences, not uniform bounds over an entire Roumieu class.
6. Theorem 7.3: parity's lower bound is the vertex correlation argument. The dyadic construction has positive denominator on the real line; one nearby node provides ratio <=1/3 and even powers preserve positivity. Substituting into the expectation extension and clearing denominators costs total degree <=2Ln(m+1). Non-affinity over F_2 has a binary non-affine face, and the eight binary non-affine laws have one exceptional corner (or its complement), hence reduce to AND. Odd majority substitution has coordinate magnitudes >=1/N and does not increase degree. The logarithmic lower bound is conditional on the precise cited Sherstov statement. The bounded-margin lower bound uses an edge and Bernstein at an interior point; Jackson plus normalization and the expectation extension yields O_(n,gamma)(1/delta). Constants, gamma=1, and nonuniform growing dimension are explicitly separated.
7. Section 8.3: r^k(x+y-r) has degree k+1 positive homogeneity, smooth angular part, zero k-jet, and a globally bounded derivative of order k+1 away from zero. The near/far segment argument gives Lipschitz D^k for every integer k>=0, including odd k. If C^(k+1) held, homogeneity would force a homogeneous polynomial, impossible with this non-affine sign law. Its positive diagonal gives exact order k+1.
8. Section 8.4: sqrt(x^2+y^2+delta^2) is analytic for fixed delta>0. Derivatives with respect to each input are positive in the positive-positive box; the minimum is (2-sqrt(3))delta. A negative input gives value <-delta. The value -delta at zero exposes the full-corner failure. Analytic-composition language includes the necessary full-neighborhood and independent-coordinate qualifications.

## Preliminary judgment and tests still needed

No central mathematical error identified. The additions look like valid classical consequences assembled with useful reductions, rather than independent new approximation theory. Proposition 7.1 and Remark 7.2 are routine Taylor consequences; the R-function and analytic examples look appropriately limited and attributed. The strongest addition is the continuous guarded-domain degree classification, whose lower bound must be checked against Sherstov's exact finite-domain result and conventions. Publication significance is therefore a separate question from correctness.

Before a final disposition: verify Sherstov Theorem 1.10 and Theorem 2.4, Bernstein/Jackson theorem statements, Shapiro's formulas and differentiability discussion, Rainer's weight conventions and cutoff theorem, and the precise Broglia–Tognoli implication. Inspect the matching PDF, then compare the prior reports and revision record without treating them as authority. A novelty search can support a cautious editorial assessment but cannot establish worldwide priority.
