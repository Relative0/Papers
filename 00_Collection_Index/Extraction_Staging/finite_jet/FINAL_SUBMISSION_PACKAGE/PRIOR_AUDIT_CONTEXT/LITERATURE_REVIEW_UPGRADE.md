# Literature Review Upgrade and Verification Ledger
## Finite-Jet Sign Laws on Hyperplane Arrangements
### 27 September 2026

This ledger records the literature added or recontextualized during the post-audit revision. It distinguishes what was checked directly from primary text, what was checked from publisher/institutional metadata and abstracts, and what role each source plays in the manuscript.

| Source | Tradition / relevance | Verification in this pass | How the manuscript uses it | Dependency status |
|---|---|---|---|---|
| Broglia--Tognoli (1989), *Approximation of C-infinity-functions without changing their zero-set* | Signatures, admissibility, nonadmissible signatures and flatness | **Primary PDF inspected.** Definition/admissibility discussion, Theorem 4.2, Corollary 4.5, and Remark 4.6 were inspected. | Direct historical antecedent for the smooth arrangement/orthant obstruction; the manuscript supplies the squared-multiplier reduction. | **Core historical dependency** |
| Fortuna (1991), *Distributions de signes* | Explicit theory of global/partial sign distributions on connected components of complements of codimension-one algebraic sets | Cambridge metadata and extract inspected | Establishes the historical vocabulary and broader sign-distribution program | Context / historical positioning |
| Acquistapace--Broglia (1992), *Signatures and flatness* | Direct continuation of signatures/flatness program | Bibliographic existence verified from institutional metadata; full theorem text not independently audited in this revision | Historical cluster only; no central proof step is delegated to it | Context; **not** a theorem dependency |
| Acquistapace--Broglia (1993), correction to *Signatures and flatness* | Published correction to the 1992 paper | Institutional record verified; pagination cross-checked | Cited alongside 1992 paper so the historical record is not incomplete | Context; **not** a theorem dependency |
| Acquistapace--Broglia (1994), *More about signatures and approximation* | Signatures and approximation by regular functions preserving zero set | DOI/metadata and abstract/summary inspected | Shows the continued development of signature-based approximation theory | Context |
| Acquistapace--Broglia--Fortuna (1994), *When is a distribution of signs locally completable?* | Local completion of prescribed sign distributions | Cambridge publisher abstract and bibliographic data inspected | Demonstrates that sign-distribution realizability was an established explicit research problem | Context |
| Varchenko--Gelfand (1987), *Heaviside functions of a configuration of hyperplanes* | Algebra of integer-valued functions constant on chambers, generated/filtered by Heaviside functions | MathNet bibliographic record and abstract inspected | Places the paper's chamber functions in the classical arrangement-function tradition | Context / combinatorial backdrop |
| Moseley (2017), *Equivariant cohomology and the Varchenko--Gelfand filtration* | Modern extension of VG filtration to arbitrary real hyperplane arrangements and oriented matroids | Publisher abstract/metadata inspected | Modern reference for the scope of the VG framework | Context |
| Basu--Bhatnagar--Gopalan--Lipton (2008) | Polynomial sign representation of parity on finite Boolean grids | Retained from prior audit | Explicitly separated from whole-orthant sign realization | Nearby but distinct |
| Speyer/Wofsey (2014), MathOverflow | Elementary polynomial orthant characterization discussion | Retained, but demoted from historical centerpiece | Useful informal antecedent, not treated as peer-reviewed priority source | Supplementary only |
| Rainer (2022) | Denjoy--Carleman survey; quasianalytic criterion/cutoffs | Retained from technical audit | Main modern source for the exact Roumieu normalization and classical cutoff theorem | Technical dependency |
| Langenbruch (2003) | Positive flat functions / Whitney-type construction | Retained from audit | Stronger constructive antecedent to one-sided selector existence | Technical antecedent |
| Thilliez (2008) | Quasianalytic local rings | Retained | Places division/local-ring machinery in context | Background |
| Bierstone--Milman (2004) | Resolution in Denjoy--Carleman classes | Retained | Demonstrates stronger available machinery not used in the elementary proof | Background |
| Belotto da Silva--Bierstone (2023) | Quasianalytic monomialization | Retained | Distinguishes post-modification monomialization from original-coordinate argument | Background |
| Belotto da Silva--Bierstone--Chow (2018) | Composite quasianalytic functions / axiomatic quasianalytic setting | Retained | Background for closure/division-style frameworks | Background |

## Primary antecedent crosswalk: Broglia--Tognoli 1989

The primary 1989 source was inspected rather than inferred from citations.

### Relevant statements

- **Theorem 4.2:** a nonadmissible signature forces flatness at some type-changing point under the stated geometric conditions.
- **Remark 4.6:** for dimension two, and in general when the irreducible components are normal crossing, their proof yields flatness at any type-changing point.
- The earlier admissibility discussion characterizes admissible signatures through products of defining equations with parity of exponents controlling changes of sign.

Primary source:
https://www.numdam.org/article/AIF_1989__39_3_611_0.pdf

The revised manuscript does not merely cite this source; it explains why the manuscript's slightly different zero-set hypothesis reduces to the older setup by replacing `F` with `F prod ell_j^2`.

## Sign-distribution literature now represented

### Fortuna 1991

Publisher extract explicitly defines a global or partial sign distribution as an assignment of signs to connected components of the complement of a codimension-one real algebraic set.

https://doi.org/10.1112/S0025579300006434

This is a substantially closer historical vocabulary than treating the problem only as Boolean sign representation.

### Acquistapace--Broglia--Fortuna 1994

The publisher abstract studies when a locally prescribed sign distribution on components of the complement of an algebraic curve on a smooth algebraic surface is induced by a regular function.

https://doi.org/10.4153/CJM-1994-024-2

This source supports the revised paper's statement that realizability/completability of sign distributions is an established problem family.

### Acquistapace--Broglia 1994

The abstract concerns the signature induced by a smooth function off a codimension-one algebraic zero set and relates it to regular approximation with the same zero set.

https://doi.org/10.1007/BF01265306

## Hyperplane chamber-function literature now represented

### Varchenko--Gelfand 1987

The MathNet abstract describes a ring of integer-valued functions on the complement of a finite real affine hyperplane arrangement that are constant on every connected component, with a filtration by degrees in the hyperplane Heaviside functions.

https://doi.org/10.1007/BF01077800

This is conceptually relevant because the manuscript's chamber labelings are `{+1,-1}`-valued chamber functions. The revised text carefully states the difference: the VG algebra asks about chamber functions as algebraic/combinatorial objects, whereas the manuscript asks which such labelings arise as the sign of one function under analytic regularity conditions.

### Moseley 2017

The publisher abstract states that the Varchenko--Gelfand filtration framework is extended to arbitrary real hyperplane arrangements and oriented matroids.

https://doi.org/10.1016/j.jalgebra.2016.10.010

## What the literature review does **not** claim

- It does not claim that every result in the sign-distribution literature literally states the manuscript's theorem.
- It does not claim that the Varchenko--Gelfand algebra proves the analytic rigidity result.
- It does not claim that absence of a search hit proves novelty of the finite-`C^N` formulation.
- It does not claim an exhaustive bibliography of real algebraic sign-separation theory.
- It does not treat a MathOverflow post as equivalent to a refereed source.

## Remaining literature-risk level

After this upgrade, the largest historical-priority risk identified in the original audit is substantially reduced because the manuscript now cites and explains the direct 1989 antecedent and situates it inside the subsequent sign-distribution literature.

The remaining risk is **narrow**, not structural: a specialist could identify an earlier or more explicit finite-regularity statement equivalent to the new `C^N` corollary. The manuscript avoids making a firstness claim about that corollary, so such a discovery would normally require an added citation rather than a conceptual rewrite.

