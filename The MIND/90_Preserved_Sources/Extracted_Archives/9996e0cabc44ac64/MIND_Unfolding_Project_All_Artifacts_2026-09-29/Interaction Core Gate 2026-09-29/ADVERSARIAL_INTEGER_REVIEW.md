# Adversarial review: integral algebra and computational scope

Reviewer role: independent computation/integer-homology agent. Date: 29 September 2026.

Reviewed: `SPECTRAL_SEQUENCE_CONSTRUCTION.md`, `MAX_DEGREE_TWO_CLASSIFICATION.md`, `COUNTEREXAMPLES_AND_FAILURE_BOUNDARY.md`, `C4_COUNTEREXAMPLE_PROOF.md`, and `verify_torsion_star.py`, alongside the imported Smith routine and the new filtered verifier. This is an internal adversarial audit, not external peer review.

## Verdict

No blocking mathematical or implementation defect was found in the reviewed statements under their explicit reduced-cone and augmented-chain conventions. The positive conclusion must remain the stated chain-level classification and restricted collapse theorem. Both unrestricted maximum-degree-two `E2` collapse and unrestricted Ferrers/chordal-bipartite `E2` collapse are false by exact integral witnesses.

## Indexing, signs, and convergence

The filtration is correctly placed on `C(K,U)`, with `H_n(cone)=H_(n+1)(K,U)`. Its first page is available-link reduced homology at coordinates `(p,q)`, total degree `p+q`, and cone degree `p+q-1`. The computational JSON convention `(p,total_degree)` is different and is explicitly documented.

The missing-first shuffle orientation gives vertical differential `(-1)^p partial` and horizontal signed deletion. This makes `v²=h²=vh+hv=0`. A boundary lowering filtration by at most one does not forbid higher page differentials; the displayed `vx=0`, `hx=-vy`, `d2[x]=[hy]` rule is correct.

For supported columns `2,...,M`, no differential of length `M-1` or larger can connect supported columns, hence `E^(M-1)=E∞`. In particular `M=2` gives `E1` collapse, `M=3` gives `E2`, and `M=4` gives `E3`. The new unit `d2` examples make the last bound sharp. Finite filtration eliminates completion issues but does not remove integral extensions.

Augmented available chains, including degree `-1`, are retained in the theorem. The statements do not silently replace reduced link homology with ordinary `H0`. The torsion construction correctly uses **ordinary** `H0(Delta R)=Z` in its interaction row; reducing that row would incorrectly discard its cone `H1=Z`.

## Exact two-column theorem and extensions

For core sizes two and three, the displayed differential agrees with `Cone(h)[2]`: the even column has `+partial`, the odd column has `-partial`, and the off-diagonal entry is `h`. Thus `H_n(cone)=H_(n-1)(Cone(h))` and the short exact sequence

```text
0 -> coker H_(n-1)(h) -> H_n(cone) -> ker H_(n-2)(h) -> 0
```

has the correct indexing.

The field dimension formula is valid. Over `Z`, splitting is justified when the right-hand kernel is free; no canonical splitting or universal integral direct sum is claimed. The text correctly warns that free link homology does not force torsion-free cokernels. The chain complex, not merely abstract groups, preserves all required maps and extension data.

## Degree-two classification

Transitivity gives the stated same-colour neighbourhood inclusions. Degree at most two bounds each colour in a mixed core by two vertices. A four-core is therefore exactly a whole `K2,2` component with both same-colour pairs comparable. Excluding those components leaves two columns and proves the advertised `E2` collapse.

For longer paths, only end triples can occur; the independent end-block decomposition is valid because those triples use disjoint edge sets when the path has at least four edges. For cycles of length at least six, distinct same-colour degree-two vertices are not neighbourhood twins, so no mixed three-core exists. Available links in these component/block calculations must still be computed in the full `Q`, as the document states.

For the full four-core, the signs of `k` in order `(abx,aby,axy,bxy)` are `(-,+,-,+)`. Substituting the four displayed `h` formulas gives `hk=0`. The three `E2` columns and the secondary-map formula are correct. Vanishing middle `E2` groups plus an isomorphism from the fourth to the second column under `d2` is exactly an acyclicity criterion, since a finite filtered module is zero if and only if its associated graded is zero. For nonzero homology the extension warning remains necessary.

## Exact counterexample certificates

The seven-state star was checked independently in the full doubled-product complex. Its integral first page has `Z²` at `(p,total)=(2,3)` and `Z` at `(4,4)`, with no other groups; total mixed homology is `H3=Z`. Thus the unique possible `d2` is a primitive injection. Full signed chains `x,y` verify its zigzag directly in `star_d2_integral_certificate.json`.

The eight-state `K2,2` witness was checked independently of the structural agent's link-path proof. Its integral first page has `Z` in each of those two positions, while both the mixed and direct cone-pair complexes are acyclic. The independently computed signed zigzag and unit-pivot reduction give a unit `d2`. These checks agree with the explicit loop traversed once in `C4_COUNTEREXAMPLE_PROOF.md`; acyclicity is not being used to claim homotopy equivalence.

The stored star minimization checks all 336 induced restrictions of sizes four through six retaining the original bottom, then finds a seven-state restriction. Smaller sizes cannot support `d2`. This establishes minimal cardinality within the particular original ten-state witness, not global minimality. The C4 audit checks all 15 proper induced restrictions retaining its four exclusive states; dropping an exclusive state leaves no possible four-core. Its induced-restriction minimality is also distinct from global minimality. The published gate wording preserves this distinction.

## Integral torsion construction

`verify_torsion_star.py` constructs a concrete six-vertex closed triangulated surface: its face counts, edge degrees, connected cyclic vertex links, and exact homology are checked. The face poset has ordinary `H0=Z`, `H1=Z/2`; it is not merely labelled `RP2` without a certificate.

For a mixed core `p0` followed by a nonempty `R1` chain, the available link consists of isolated `p1` and the principal ideal below the chain's first state. The latter is a cone. Under deletion inclusions the two connected components remain distinguished, so the chosen reduced `H0` generator maps identically. Horizontal core deletion therefore gives the negative ordinary simplicial boundary of `Delta R`. The computed integral `d1` complex is the actual interaction row, not an unjustified replacement by unrelated scalar incidence.

Only row `q=0` survives on `E1`, forcing `E2` collapse and leaving only one filtration piece in each total degree. There is consequently no unresolved extension in the reported `H1(cone)=Z`, `H2(cone)=Z/2`. All 181 available links and all 31 coarse exclusive-edge links are checked independently and are torsion-free. This certifies torsion arising from the interaction maps relative to those local links. The script correctly does not claim a direct Smith reduction of the entire doubled 32-state pair.

## Smith routine and field-page implementation

The installed SymPy documentation explicitly gives the decomposition convention `D=S*A*T`. Therefore the last columns of `T` form a primitive basis for `ker A`, and expressing the next boundary through `T^-1 B` is correct. The imported routine checks that the rows outside the kernel vanish, converts the kernel coordinates back into the integer domain, and performs a second Smith decomposition. This detects torsion rather than merely computing rational rank differences.

The main field verifier sorts cells by filtration before boundary reduction. Positive interval lengths equal spectral-sequence page numbers; length-zero pairs are the associated-graded differential. It independently checks `E1` against same-filtration matrix ranks and the final result against separate unfiltered boundary ranks in every processed case. The explicit integral examples further check the nonzero `d2` interpretation, so the absence of `d2` in the smaller sample is not an artifact of an implementation that can detect only `d1`.

All main exhaustive claims are over `F2`. Exact integral claims identify their selected or explicit cases. The 435 selected integral checks are not advertised as exhaustive five-state Smith calculations. Random trials and natural-label duplicates are also disclosed. No torsion-freeness theorem is inferred from the small sample.

One inherited utility caveat for future work: the old matching verifier's `add_groups` concatenates torsion lists. This represents the direct-sum group but does not normalize coprime factors to canonical invariant factors (`[2,3]` versus `[6]`). The new gate's exact checks do not use this helper for torsion comparisons, so it does not affect any reported result. Future matching tests with several torsion summands should canonicalize before list equality comparisons.

## Preservation and completion conditions

After the new calculations, all 83 original manifest entries still match their archived hashes. A transient Python bytecode file created beside the imported source was removed; bytecode creation is now disabled before importing that source. No frozen source or manuscript was changed.

The reviewed mathematics is ready to consolidate with its negative results and scope restrictions. The remaining review responsibility is bibliographic priority and editorial integration, not an unproved integral collapse claim. A manuscript merge remains a separate post-gate action.
