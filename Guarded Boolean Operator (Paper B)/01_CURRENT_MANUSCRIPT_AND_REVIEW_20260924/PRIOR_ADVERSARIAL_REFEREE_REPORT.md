# Fresh adversarial referee report - Paper B

**Manuscript:** *From Continuous Scores to Guarded Boolean Operators: Exact Sign Quotients, Zero-Aware Abstraction, and Fixed-Frame CM/LM Lifts*  
**Version:** major-revision research draft, 24 September 2026  
**Review posture:** hostile mathematical audit + fresh prior-art/novelty audit  

## Recommendation

**MAJOR REVISION, but for a different reason than the preceding round.**

The prior semantic/type blockers have been repaired. I found no foundational defect in the continuous-score quotient, zero-aware collecting semantics, certification contract, CM/LM typing, or trajectory theorem. The new centered Walsh construction is also algebraically correct in its main realization/count statements.

However, the fresh audit changes the novelty assessment materially:

1. The polynomial/semialgebraic version of an operator fiber is exactly the realization of a strict sign condition of a polynomial family. Realizability, connected components, algorithms, and asymptotic bounds for such sign conditions are classical real algebraic geometry.
2. The centered Walsh construction is linearly equivalent to a classical generic central arrangement of `N` hyperplanes in `R^(N-1)`, or equivalently homogeneous linear separation of the `N` vertices of a centered regular simplex. The count `2^N-2` is the extremal Schlaefli/Cover count in this dimension, and the adjacency structure is the classical tope graph of the corresponding oriented matroid.
3. Therefore neither the exact sign quotient nor the Walsh chamber/count theorem should carry the paper's principal novelty claim.

There is one localized statement issue in the Walsh adjacency language at `n=1`, described below. It is easily repaired.

The manuscript remains potentially useful as a rigorous **methods/interface paper** joining continuous score semantics, zero-aware verified abstraction, and CM/LM transport. To support a stronger standalone research-paper claim, it still needs a genuinely new algorithmic, structural, or application result beyond these classical sign-arrangement facts.

---

## 1. Mathematical audit

### 1.1 Exact operator quotient

**Verdict: correct, essentially the kernel partition of the sign map.**

On the zero-free domain, `Phi(lambda)=Theta_lambda` is a finite-valued map. The fibers `Omega_Theta=Phi^{-1}(Theta)` are exactly intersections of strict sign preimages. They are open, mutually disjoint, cover the zero-free domain, and are clopen relative to it. Any set on which the operator is constant lies in one fiber. Hence the fiber partition is the unique coarsest partition by exact guards.

The topology repair is correct. Taking `Lambda` to be an open subset of Euclidean space makes the zero-free domain locally path-connected. Its connected components are open. Since the operator fibers are clopen, connected components of the zero-free domain coincide with connected components of individual operator fibers.

**Referee interpretation:** this is a useful universal-property formulation, but it is mathematically close to a definition/equivalence-relation observation rather than a substantial theorem.

### 1.2 Polynomial/semialgebraic finiteness

**Verdict: correct, classical.**

For polynomial scores, each Boolean operator fiber is precisely a strict sign-condition realization. The real-algebraic literature already studies feasible sign conditions, their semi-algebraically connected components, bounds, and algorithms for meeting/enumerating those components. The manuscript should cite this literature more directly rather than only the general textbook.

Particularly relevant:

- Basu, Pollack, Roy, *An asymptotically tight bound on the number of semi-algebraically connected components of realizable sign conditions*, Combinatorica 29 (2009), 523-546, DOI 10.1007/s00493-009-2357-x.
- Jeronimo, Perrucci, Sabia, *On sign conditions over real multivariate polynomials*, Discrete Comput. Geom. 44 (2010), 195-222, DOI 10.1007/s00454-009-9200-4.

### 1.3 Isolated crossing proposition

**Verdict: repaired and correct.**

The new one-sided hypothesis is sufficient. The differentiable/transverse corollary is also correct. This fixes the earlier oscillatory counterexample issue.

### 1.4 One-parameter polynomial event bound

**Verdict: correct.**

The `2^n d` count is a union-of-roots bound on discriminant values. The manuscript correctly distinguishes zero contacts from actual sign changes.

### 1.5 Zero-aware collecting semantics

**Verdict: correct and well typed.**

`S_alpha subset {-1,0,+1}` correctly separates unreachable cells, strict signs, ties/zeros, and two-sided sign ambiguity. The explicit distinction between semantic states and solver `UNKNOWN` is important.

The total-reachability condition is properly identified as a convention for a *canonically induced total Boolean function on the declared cube*, not as the only legitimate abstraction convention.

### 1.6 Guard-certificate soundness

**Verdict: correct but definitional.**

If a certificate proves every indexed score has a strict sign on a guard, then the guard is zero-free and the Boolean operator is exact. This is a valid soundness contract, but its research value depends on an actual proof system/backend, complexity result, or nontrivial verified application.

### 1.7 CM/LM endpoint

**Verdict: internally correct.**

The revised manuscript now states the formula-valued fixed-frame lift explicitly. All-true valuation recovers the correspondence tensor; injectivity follows immediately; pointwise Boolean superposition is consistent with the companion CM/LM manuscript.

For a standalone submission I recommend proving the two short facts used here directly in Paper B rather than relying on an unpublished companion for them. The formula is already present, so this would require only a few lines and remove an avoidable dependency.

### 1.8 Trajectory theorem

**Verdict: correct.**

The discriminant preimage is closed. The discrete object is constant on each connected component of its complement. A closed discrete subset of a compact interval is finite. At boundary times the binary operator is rightly left undefined absent a tie policy.

Minor wording: use "relatively open interval components" rather than "open time intervals" if endpoint components are included.

---

## 2. Centered Walsh atlas - mathematical audit

Let `N=2^n`. The evaluation matrix of the nonconstant Walsh characters has `N-1` orthogonal columns. Its image is exactly the zero-sum subspace

`1^perp = {s in R^N : sum_x s_x = 0}`.

Thus the Walsh coefficient map is a linear isomorphism

`R^(N-1) -> 1^perp`.

Under this isomorphism, the discriminant hyperplanes are simply the coordinate hyperplanes `s_x=0` restricted to `1^perp`. This gives the cleanest description of the construction.

### 2.1 Simplex identity

**Verdict: correct.**

The nonconstant Walsh feature vectors have Gram matrix with diagonal `N-1` and off-diagonal `-1`, hence form a centered regular simplex.

### 2.2 Realization of every nonconstant Boolean labeling

**Verdict: correct, and classically immediate from Fourier expansion.**

For a sign function `h:{-1,+1}^n -> {-1,+1}`, its Walsh-Fourier expansion has constant coefficient `E[h]`. If `h` is nonconstant then `-1<E[h]<1`, so

`h(x)-E[h]`

has exactly the same sign as `h(x)` and has zero constant Fourier coefficient. Therefore its expansion uses only the nonconstant Walsh characters. This gives an even shorter proof than the positive-set sum used in the manuscript.

The manuscript's explicit coefficient witness is correct and equivalent to this centered-Fourier argument.

### 2.3 Exact chamber count `2^N-2`

**Verdict: correct, but classical.**

The `N` simplex normals form a generic central arrangement in dimension `N-1` (for `N>2`; `N=2` is the degenerate duplicate-hyperplane edge case). Classical Schlaefli/Cover counting gives

`2 sum_{j=0}^{N-2} binom(N-1,j) = 2^N-2`.

Equivalently, Cover's 1965 theorem counts the homogeneous dichotomies of points in general position. The present Walsh construction is a concrete coordinate realization of this extremal configuration.

### 2.4 Adjacency graph

**Verdict: correct for the regular-facet graph for `n>=2`; wording needs repair at `n=1`.**

For `n>=2`, the discriminant hyperplanes are distinct and the arrangement realizes the uniform oriented matroid of rank `N-1` on `N` elements. Topes are all sign vectors except the two constant ones, and tope-graph adjacency is Hamming distance one. Hence the graph is the `N`-cube with those two antipodal vertices removed.

For `n=1`, however, the two score hyperplanes in one-dimensional coefficient space coincide at `{0}`. The two nonconstant unary chambers are the two rays. Their closures share the ordinary codimension-one boundary `{0}`, while their truth tables differ in two entries. The current phrase "regular codimension-one facet" can be interpreted to exclude this multiple-hyperplane boundary, but the subsequent unqualified phrase "chamber adjacency graph" then becomes nonstandard/misleading.

**Required patch:** either

- state item (iv) and the CM/LM facet corollary for `n>=2`, handling `n=1` separately; or
- explicitly define *regular adjacency* as adjacency across a point/facet where exactly one indexed score vanishes, and never identify that with ordinary geometric chamber adjacency in the `n=1` case.

I recommend the first option.

### 2.5 Prior-art consequence for the Walsh section

The entire structural picture is classical under linear equivalence:

- Walsh/Fourier basis: classical Boolean Fourier analysis;
- centered simplex: classical regular-simplex geometry;
- all nonconstant homogeneous dichotomies: Cover/Schlaefli;
- chamber/topes and one-coordinate adjacency: oriented matroid/tope-graph theory.

The section is still valuable as an **exact calibration example for the CM/LM interface**, but it should not be presented as the paper's main independent theorem.

---

## 3. Fresh prior-art audit

### 3.1 Real algebraic sign conditions are closer than the current paper acknowledges

For polynomial scores, the paper's operator fibers are sign-condition realizations. Basu-Pollack-Roy and Jeronimo-Perrucci-Sabia study exactly the realizability and connected-component decomposition of such sign conditions. This is closer than a generic citation to CAD alone.

**Recommended change:** in the polynomial corollary and certification section, explicitly say that the geometric chamber atlas is the connected-component refinement of realizable strict sign conditions of the score family.

### 3.2 DSGRN remains a close structured antecedent

The major revision now handles this appropriately. DSGRN provides finite parameter graphs for switching regulatory-network models and connects parameter nodes to Boolean/logical data; later work treats monotone Boolean functions and logical adjacency. Recent 2026 work explicitly maps Boolean functions into DSGRN parameter space.

The present manuscript is broader in score-family type but much thinner in model/dynamics content. Its genericity alone does not create a strong novelty claim because the generic theorem is elementary.

### 3.3 Logical bifurcation diagrams remain direct trajectory prior art

The paper now correctly treats the trajectory idea as antecedent rather than novel. Keep this positioning.

### 3.4 Abstract interpretation/predicate abstraction

The collecting-sign semantics should continue to be positioned as an exact CM/LM-facing contract, not a new abstract domain. This is currently handled well.

### 3.5 Cover, Schlaefli, and oriented matroids must be added to the Walsh discussion

The current references to Walsh analysis and oriented matroids are not quite enough. Add at least:

- T. M. Cover, *Geometrical and Statistical Properties of Systems of Linear Inequalities with Applications in Pattern Recognition*, IEEE Trans. Electronic Computers EC-14 (1965), 326-334, DOI 10.1109/PGEC.1965.264137.
- A standard hyperplane-arrangement/Schlaefli-Zaslavsky reference for region counts.
- A tope-graph/oriented-matroid reference making explicit that topes form an induced/partial-cube sign graph with one-coordinate adjacency.

Then state plainly that Theorem 8.x is a Walsh-coordinate realization of this classical arrangement.

---

## 4. Novelty assessment after this pass

### Established/classical components

- sign constancy on connected zero-free components;
- exact fibers of a finite-valued sign map;
- strict polynomial sign conditions and their connected components;
- zero-aware sign abstraction at the powerset/collecting-semantics level;
- sign-certificate soundness once strict inequalities are proved;
- Walsh/Fourier expansion;
- regular-simplex realization;
- `2^N-2` central-arrangement/Cover count;
- tope-graph one-coordinate adjacency;
- parameter-to-logical regions in DSGRN/logical bifurcation frameworks;
- CM as truth tensor and LM lift as supplied by the companion theory.

### Potentially distinctive contribution that remains

What remains distinctive is principally the **interface architecture**:

`continuous score family -> zero-aware exact/partial Boolean semantics -> certified guard -> CM -> fixed-frame LM`,

with explicit handling of zeros, unreachable cells, solver uncertainty, and completion policies.

That can be a useful contribution, but it is a methods/specification contribution more than a new mathematical classification theorem.

### Research-paper strength

As a pure/theoretical research paper, I would still regard the novelty as **insufficiently strong** unless another substantive result is added.

As a methods/interface paper, the manuscript is becoming coherent and defensible, provided the Walsh section is honestly reclassified as a classical calibration and the real-algebraic sign-condition literature is integrated more directly.

---

## 5. Highest-value next research additions

If the goal is a stronger standalone research paper, I would prioritize one of these.

### A. Certified nonlinear case study / prototype

Implement exact or proof-producing guard certification for a nontrivial nonlinear score family. Report:

- raw sign-condition cells;
- connected components;
- quotient compression into Boolean operators;
- emitted CMs and fixed-frame LMs;
- certificates/checkable inequalities;
- runtime and failure/UNKNOWN behavior.

This would turn the current contract into an evaluated method.

### B. Restricted guard-language minimality

The unrestricted coarsest fiber partition is tautological. The nontrivial problem is:

> Given a declared guard language (linear inequalities, bounded-degree polynomial inequalities, a fixed predicate library, etc.), find or approximate a minimum-complexity exact guarded cover/partition.

A theorem on existence, complexity, hardness, approximation, or canonical normal forms here would be genuinely stronger.

### C. Operator-quotient complexity/compression

For polynomial score families, study the relationship between:

- number of realizable strict sign conditions/components;
- number of distinct Boolean operators after quotienting;
- geometry/complexity of the union fibers.

Classical sign-condition bounds count geometric cells; a nontrivial theorem about **operator quotient compression** under structured score families could be distinctive.

### D. CM/LM-specific symmetry theorem

If a score family is equivariant under polarity/frame actions, derive a quotient theorem for its operator fibers/transition graph compatible with the CM/LM frame action. This would exploit structure absent from generic sign-condition theory. A general statement must be checked against classical Boolean-function NPN/group-action literature.

---

## 6. Required revisions before the next referee round

1. Repair the `n=1` Walsh adjacency edge case.
2. Add Cover/Schlaefli-Zaslavsky/tope-graph prior art and explicitly identify the Walsh arrangement as classical under linear equivalence.
3. Replace any wording implying the `2^N-2` count or hypercube-minus-constants graph is independently novel.
4. In the polynomial corollary, identify operator fibers as strict sign-condition realizations and cite sign-condition algorithms/bounds directly.
5. Consider demoting "Exact operator quotient" from a headline theorem to a proposition/universal-property lemma unless a restricted-guard minimality result is added.
6. Prove the short fixed-frame LM facts used here directly, or make the companion manuscript publicly citable/stable.
7. Use "relatively open interval components" in the trajectory statement.
8. Decide explicitly whether the submission is a methods/interface paper or a theorem paper. The current mathematical novelty supports the former more naturally.

---

## 7. Referee scorecard

| Criterion | Assessment |
|---|---|
| Core semantic correctness | Strong |
| Topological formulation | Strong after Euclidean restriction |
| Zero/reachability semantics | Strong |
| Certification contract | Sound, but mostly definitional |
| CM/LM typing | Strong |
| Walsh algebra | Correct |
| Walsh adjacency statement | One localized `n=1` wording/edge-case repair |
| Prior-art coverage | Improved, but still missing Cover/sign-condition/tope specifics |
| Novelty as theorem paper | Weak after fresh prior-art audit |
| Value as methods/interface paper | Good |
| Current standalone readiness | Major revision |

## Final recommendation

**MAJOR REVISION.** The paper is no longer blocked by foundational correctness. The decisive issue is now contribution identity. The fresh audit shows that the new Walsh theorem is a classical generic-central-arrangement/Cover/tope result in Walsh coordinates, while polynomial operator fibers are classical sign-condition realizations. Preserve these as useful calibration/background, but do not make them the novelty spine.

The best next move is to either (a) deliberately recast Paper B as a rigorous methods/interface article, or (b) add a genuinely new restricted-guard, quotient-complexity, symmetry, or certified-nonlinear result before another adversarial review.
