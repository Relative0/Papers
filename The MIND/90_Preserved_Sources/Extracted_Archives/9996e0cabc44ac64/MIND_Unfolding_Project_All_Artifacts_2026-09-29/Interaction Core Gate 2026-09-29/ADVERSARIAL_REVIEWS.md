# Adversarial reviews and resolutions

These are actual internal agent reviews and computational attacks performed during this gate, not external human referee reports. The original handoff's earlier reviews remain separate. Detailed independent reports are ADVERSARIAL_INTEGER_REVIEW.md and ADVERSARIAL_PRIORITY_REVIEW.md; the structural agent's proof notes and C4 certificate provide a third derivation.

## 1. Spectral-sequence attack

**Attack:** the filtration was ambiguously attached to the cone pair; indexing could lose one degree, and a double complex could be misread as automatically collapsing on E2.

**Resolution:** the filtered object is C(K,U), with cone H_n=H_(n+1)(K,U). Missing-first orientations give vertical sign (-1)^p, horizontal signed deletion, and d^r of bidegree (-r,r-1). Empty available simplices remain in degree -1. Both independent reviewers checked these conventions and the two-column shift. The explicit star and C4 examples have nonzero d2 despite boundaries lowering filtration by at most one.

**Retained limit:** the pages converge to associated graded homology; integral extensions are not silently split.

## 2. Combinatorial-topology and priority attack

**Attack:** the proposed available links and interaction machinery merely rename known obstruction complexes.

**Finding:** this overlap is literal. With the vertex cover X=V\M0, Y=V\M1, A=X intersection Y, the complexes Lambda_S are the obstruction complexes in Chacholski--Jin--Scolamiero--Tombari. Filtration-width collapse and cone algebra are standard. The literature map now identifies the published theorem numbers and compares hypotheses with Bjorner--Wachs--Welker.

**Retained contribution:** the Boolean product-poset recognition, same-colour transitivity restrictions, path/cycle block classification, and explicit integral witnesses. No new general obstruction, fibre, spectral-sequence, or biclique theory is claimed. Novelty remains unconfirmed.

## 3. Integer-homology attack

**Attack:** field calculations can hide torsion; E2 collapse can hide extensions; signed incidence need not be TU.

**Resolution:** exact integral statements use a primitive kernel basis from full Smith decomposition, then reduce the next boundary in that basis. The implementation convention D=S*A*T was checked. Both higher-differential witnesses have full signed unit-pivot integer certificates, independently of the field search. The RP2 star has every local available and coarse link torsion-free, but integral d1 creates Z/2. All claims retain chain maps and extension qualifications.

**Retained limits:** the n<=5 exhaustive run is over F2; 435 main-run integer checks are selected, not exhaustive. The 32-state example is checked through its proved reduced interaction model and all links, not a direct SNF of the whole doubled pair. An inherited matching utility concatenates torsion factors without invariant-factor normalization; it is not used for the new gate's torsion comparisons and should be normalized before future multiple-torsion matching tests.

## 4. Graph-theoretic attack

**Attack:** maximum degree, Ferrers neighbourhoods, or chordality may not control same-colour comparisons or available-link attachment maps.

**Resolution:** transitivity was used explicitly: p<p' implies N(p') subset N(p), and z<z' implies N(z) subset N(z'). In degree two, only a C4 with both pairs comparable has a four-core. Longer cycles have no triple cores. Paths have only end triples, with a shared middle edge in the three-edge case. Available links always use the full coarse Q. The smallest connected non-Ferrers chordal-bipartite example is P5; without connectedness, it is 2K2.

**Negative result retained:** both Ferrers/chordal E2-collapse and unrestricted maximum-degree-two E2-collapse are false. The positive class is stated with its actual extra hypothesis.

## 5. Hostile counterexample search

The main enumeration found no d2 through five coarse states. Rather than elevating that absence to a theorem, targeted stars and doubly ordered C4 systems were searched.

* Seven-state K1,3: d2:Z->Z² primitive injective, refuting forest/Ferrers/chordal E2-collapse.
* Eight-state K2,2: d2:Z->Z a unit, refuting full degree-two E2-collapse and making E3 sharp.
* Thirty-two-state K1,31: interaction-created Z/2 with torsion-free local links.

The first two witnesses were minimized under induced restriction, and their restrictions and certificates are saved. Global minimality is not inferred. The 3-state frozen K1,2 counterexample remains the minimal graph-overlap obstruction to the independent coarse-link sum.

## 6. Final synthesis corrections

The root review restricted the ordinary relative deletion-link recursion in FERRERS_AND_CHORDAL_CASES.md to v in U. Every vertex of the current two-colour pair satisfies this condition. For a general pair with v outside U, augmented link/void-complex conventions are required in degree zero; the earlier unrestricted wording could omit the vertex generator. This correction does not change any theorem or example in the present model.

The manuscript candidate keeps the all-exclusive star's ordinary H0 term, avoiding an erroneous loss of cone H1. It does not advertise the example sizes as globally minimal, and it does not merge either prepared section into v0.3.

## Verdict

No unresolved correctness defect was found in the final stated theorems and explicit witnesses after these corrections. The conservative gate verdict is Level B: exact model-specific interacting classifications with sharp failures, rather than a claimed new general topological theory. An independent publication-level proof/priority/editorial convergence pass remains appropriate before integration into a new manuscript version.
