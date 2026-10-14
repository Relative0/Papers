# A Modern Audit of the p-Adic / Ultrametric Unconscious

## Executive conclusion

The 2015 thesis contains a **good hierarchical seed** and a **serious topological error**. The good seed is the representation of a concept of order `k` by fixing the first `k` coordinates of an infinite `m`-ary sequence. Those cylinder sets are exactly the natural nodes/balls of a rooted hierarchy. The serious error is the attempt to make ultrametricity itself produce an indiscrete topology or genuine topological indistinguishability. It does not. Ordinary p-adic and ultrametric spaces are metric spaces, hence Hausdorff; p-adic balls are rich clopen neighborhoods and points can be separated.

The clean modern repair is:

1. keep the **hierarchical space** (rooted tree / prefix space / ultrametric);
2. add an explicit **observation map** `pi_k` which reports only the first `k` hierarchical coordinates;
3. define `x ~_k y` iff `pi_k(x)=pi_k(y)`;
4. interpret the quotient `X_k = X / ~_k` as the distinctions available at resolution `k`;
5. if desired, impose a **symmetry/invariance principle** saying observables at level `k` are constant on each fiber of `pi_k`.

This realizes the Matte-Blanco-style claim “members of a class are treated as equivalent although not literally identical” without falsifying topology. The topology remains perfectly separating; **the indistinguishability belongs to the observer/model of access, not to the underlying metric space**.

The p-adics are useful but not essential. The core construction only needs a rooted hierarchy (or an equivalent prefix ultrametric). Prime-base p-adics contribute a particularly elegant algebra, Haar measure, Fourier/wavelet analysis, and non-Archimedean dynamics. If those structures are not used, calling the model “p-adic” adds coordinates more than substance.

---

## 1. Thesis audit: p-adic and ultrametric claims

The thesis's relevant material appears principally in the p-adic/ultrametric preliminaries (pp. 18-22 in the PDF), the “Concepts of Order k” section (pp. 54-55), and the “Unconscious by Ultrametricity” section (pp. 63-66).

| Thesis claim | Correct? | Correct statement | Effect on cognitive model |
|---|---|---|---|
| `v_p(r)` is the largest exponent of `p` dividing a nonzero rational, extended by numerator minus denominator valuation. | Essentially yes, with standard caveats. | For `x != 0`, write `x=p^n u/v` with `p` dividing neither `u` nor `v`; then `v_p(x)=n`, and `v_p(0)=+infinity`. | Sound basis for measuring common low-order p-adic digits. |
| `|x|_p = p^{-v_p(n)}` in the norm definition. | Typographical/mathematical error. | `|x|_p = p^{-v_p(x)}` for `x != 0`, and `|0|_p=0`. | Easy repair; no conceptual damage. |
| p-adic closeness means high divisibility of `x-y` by `p`. | Yes. | `d_p(x,y)=|x-y|_p`; large `v_p(x-y)` means many initial base-p digits agree (with p-adic digits ordered from low powers upward). | This is exactly the useful hierarchy/common-prefix idea. |
| In Example 0.10, comparing `|10|_5-|25|_5` with `|24|_5-|25|_5` establishes closeness. | No. | Closeness must compare distances `|10-25|_5=1/5` and `|24-25|_5=1`; the conclusion happens to be the same. | Fixes the metric interpretation. |
| `v_p(a+b) >= min(v_p(a),v_p(b))`, with equality when valuations differ. | Yes. | Standard non-Archimedean valuation law. | Gives the strong triangle inequality. |
| p-adic numbers satisfy the ultrametric inequality. | Yes. | `|a+b|_p <= max(|a|_p,|b|_p)`, hence `d(x,z)<=max(d(x,y),d(y,z))`. | Sound hierarchical geometry. |
| “the points cannot be any number” for the ultrametric relation to hold. | No. | The p-adic metric satisfies the ultrametric inequality for **all** points of `Q_p`. | Remove this restriction. |
| A p-adic sphere `{x:|x-a|_p=r}` is open. | Yes, for `r>0` in the p-adic value setting. | If `x` lies on the sphere, a sufficiently small ball around `x` remains on the same sphere. | Interesting but not central cognitively. |
| “open balls” written as `{x:|x-a|_p<=r}` are open in every metric space. | No. | `<=r` defines a **closed** ball. In an ultrametric space closed balls are also open; this is special, not true in arbitrary metric spaces. | The useful property is clopenness/zero-dimensionality, not indiscreteness. |
| p-adic balls are both open and closed. | Essentially yes (with correct radius conventions). | In `Q_p`, standard balls are clopen; in general ultrametric spaces open balls are closed, and closed balls are open under the usual positive-radius setup. | Supports sharply bounded hierarchical classes. |
| Two overlapping p-adic balls must be equal. | Only if they have the same radius. | Any two intersecting ultrametric balls are **nested**; equal-radius intersecting balls coincide. | This nested/disjoint law is the correct concept hierarchy. |
| Ultrametricity gives an indiscrete topology. | **False.** | Every ultrametric is a metric; every metric space is Hausdorff. `Q_p` is Hausdorff and has many nontrivial clopen sets. | This is the main correction. Indistinguishability cannot come from topology alone. |
| In an ultrametric space, overlapping balls mean their points become topologically indistinguishable. | **False.** | Points lying in one common ball can still be separated by smaller balls. Equal-radius balls may share centers, but the topology remains separating. | Replace with finite-resolution observational equivalence. |
| A `T1` condition is not enough for topological distinguishability. | False terminology. | `T0` already means topological distinguishability; `T1` is stronger, and every metric space is `T2` (Hausdorff). | Clarifies exactly what “indistinguishable” can mean. |
| Fixing the first `k` digits gives a category/concept of order `k`. | Yes, as a hierarchical cylinder/ball construction. | In `A^N` with prefix metric, the set of sequences with a specified length-`k` prefix is a ball/cylinder. For `A={0,...,p-1}` it corresponds to a residue class mod `p^k` in `Z_p`. | This is the strongest surviving thesis idea. |
| Such a concept has radius `1/m^k`. | Convention-dependent but essentially right for a prefix ultrametric. | If `d(x,y)=m^{-L(x,y)}` where `L` is common-prefix length, a length-`k` cylinder is naturally a ball at scale `m^{-k}` (open/closed radius indexing may shift by one). | Harmless once conventions are frozen. |
| In Example 2.4, `{a0=1,a1=1,a2=1} ∩ {a0=0,a1=1} = {a1=1}`. | **False as set intersection.** | Because the first coordinates conflict, the intersection is empty. `{a1=1}` is obtained only by **forgetting/projecting away** the conflicting coordinate, not by intersection. | This is conceptually important: “common attribute” requires projection, existential quantification, or a meet in a different feature lattice, not set intersection of cylinders. |
| Symmetry of an arbitrary relation implies reflexivity and transitivity, hence equivalence. | False. | Symmetry alone does not imply reflexivity or transitivity. An equivalence relation requires all three. | If class-equivalence is desired, define it directly (e.g. `~_k`). |
| Symmetrizing subset inclusion makes a proper subset equal to the whole. | As a formal collapse rule, yes, but not a property of ordinary sets. | If one **imposes** both `A subseteq B` and `B subseteq A`, extensionality yields equality. This is not produced by ultrametricity. | Best treated as a quotient/invariance rule of the cognitive representation, not literal set theory. |

### The key repaired statement

The historically useful property is not “ultrametric spaces are indiscrete.” It is:

> **Ultrametric balls form a laminar hierarchy: if two balls intersect, one contains the other; if they have equal radius, they are equal.**

That gives a canonical tree of nested concepts while preserving complete point separability.

---

## 2. Correct notion of unconscious indistinguishability

Let

`X = A^N`, with `A={0,...,m-1}`,

and let `L(x,y)` be the number of initial coordinates on which `x` and `y` agree. Fix `0<lambda<1` and define

`d(x,y)=0` if `x=y`, otherwise `d(x,y)=lambda^{L(x,y)}`.

This is an ultrametric. For `lambda=1/m`, its balls are precisely prefix classes.

For each resolution `k`, define

`pi_k(x) = (x_0,...,x_{k-1})`

and

`x ~_k y  <=>  pi_k(x)=pi_k(y)`.

Then:

- `~_k` is an equivalence relation;
- every equivalence class is a depth-`k` cylinder/ultrametric ball;
- `X_k = X / ~_k` has exactly `m^k` classes for the full regular hierarchy;
- `~_{k+1}` refines `~_k`;
- there are natural forgetting maps `q_{k+1,k}:X_{k+1}->X_k`;
- the inverse limit of the finite quotients recovers the full sequence space.

### Interpretation

Two states can be objectively different in `X`, and even separated by disjoint open sets, while being **observationally identical at resolution `k`** because the allowed observation `pi_k` does not inspect deeper coordinates.

This is a mathematically exact version of:

> members of a class are equivalent for the system's present mode of access, though they are not literally identical.

### Equivalent formulations

The same idea can be expressed as:

- **equivalence relation:** fibers of `pi_k`;
- **quotient:** `X_k`;
- **partition:** all depth-`k` balls;
- **sigma-algebra:** `F_k = sigma(pi_k)`, the events decidable from the first `k` coordinates;
- **coarse-graining:** map microstates in `X` to macrostates in `X_k`;
- **information partition:** each cell carries unresolved residual information;
- **factor map:** `pi_k` is the factor from the fine system to the coarse system;
- **group invariance:** observables can be required to be invariant under permutations/automorphisms inside each fiber.

These are not rival descriptions; they are compatible layers of the same structure.

---

## 3. Are p-adics essential?

### Rooted tree: essential core

The minimal structure is a rooted tree or nested sequence of partitions. A regular `m`-ary tree already supplies:

- hierarchical depth;
- common ancestor;
- refinement/coarsening;
- prefix equivalence;
- a canonical ultrametric on its boundary.

### Arbitrary ultrametric: useful but still generic

Any ultrametric encodes a hierarchy of balls. Finite ultrametric spaces admit representing rooted trees/dendrograms; conversely, suitable rooted trees with decreasing labels define finite ultrametrics. Thus, for hierarchy alone, the ultrametric and tree descriptions are two faces of nearly the same object.

### Baire/prefix space: often the cleanest cognitive formulation

`A^N` with the common-prefix ultrametric is conceptually transparent and does not require number-theoretic commitments. It is ideal if attributes are symbols rather than arithmetic quantities.

### `m`-adic trees: good coordinates for regular branching

Khrennikov's mental-space work explicitly emphasizes `m`-adic trees. This gives a uniform branching model even when `m` is composite.

### `Z_p`: useful when prime-base algebra is genuinely exploited

For prime `p`, `Z_p` gives:

- a compact additive topological group;
- a ring structure;
- Haar probability measure;
- characters/Fourier analysis;
- p-adic wavelets;
- polynomial and analytic dynamics;
- congruence classes mod `p^k` as exactly the depth-`k` concepts.

### `Q_p`: usually more than the hierarchy needs

`Q_p` allows negative valuations and multiple scales outside the compact unit ball. This is useful for analytic/dynamical models but unnecessary if the cognitive state space is simply an infinite rooted `p`-ary tree.

### More sophisticated non-Archimedean geometry

Bruhat-Tits buildings, Berkovich spaces, rigid geometry, etc. should not be introduced merely to sound more “non-Archimedean.” They become justified only if the research question requires group actions, multiple interacting valuations, analytic continuation, or higher-dimensional non-Archimedean geometry.

### Bottom line

The **intrinsic mathematics is hierarchical/ultrametric**. The p-adic representation is a particularly rich coordinate/algebraic realization of that hierarchy, not the source of indistinguishability.

---

## 4. Algebra of concepts

Let `B_s` be the cylinder/ball associated with a finite prefix `s`.

### Inclusion and refinement

`B_t subseteq B_s` iff `s` is a prefix of `t`.

Going deeper adds attributes and produces a more specific concept.

### Intersection

For prefix balls:

- if prefixes are compatible, the deeper one is the intersection;
- if the prefixes conflict at any coordinate, the intersection is empty.

This corrects the thesis's Example 2.4.

### Least common ancestor / join

For two prefixes `s,t`, their longest common prefix `lcp(s,t)` is the smallest ball containing both. This is their natural join in the ball hierarchy.

### Meet

If balls are nested, the meet is the smaller ball. If disjoint, the set-theoretic intersection is empty. Adding a bottom element `empty` yields a lattice-like structure for finite trees.

### Poset and category

The balls ordered by inclusion form a tree-shaped poset. Every poset canonically defines a thin category, so a category-theoretic presentation is available essentially for free.

### Boolean algebra

The set of **individual balls** is not a Boolean algebra because complements of balls are typically unions of many balls. At any fixed finite depth `k`, however, the power set of the `m^k` quotient cells is a finite Boolean algebra. The increasing union of cylinder algebras generates the Borel sigma-algebra.

### Domain-theoretic view

Finite prefixes ordered by extension form the familiar information order: longer prefixes carry more information. Adding infinite paths gives a standard domain-like completion. This is attractive if “unfolding” is understood as progressive information acquisition.

### Measures, conditional probabilities, information

Under the uniform product/Haar measure,

`mu(B_s)=m^{-|s|}`.

A refinement by one regular branch contributes

`log_2 m` bits

of information. At depth `k`, a fully resolved uniform prefix has entropy

`H_k = k log_2 m`.

For nonuniform branching probabilities `p(a|s)`,

`mu(B_{sa}) = mu(B_s) p(a|s)`

and the information increment is `-log p(a|s)`.

Thus the hierarchy naturally supports Bayesian refinement and martingale/filtration language without needing any quantum analogy.

---

## 5. Formalizing “symmetry” without conflating it with equality

The term “symmetry” should be split into several mathematical notions.

### A. Automorphism symmetry

A regular rooted tree has a large automorphism group. The stabilizer of a depth-`k` node acts within its descendant subtree. If the model treats all descendants as equivalent at depth `k`, this group action makes that precise.

### B. Observational symmetry

An observable `f` available at depth `k` is `F_k`-measurable, equivalently constant on every `~_k` class. Then exchanging two states inside the same class leaves every allowed observation unchanged.

This is the strongest candidate for Matte-Blanco's “treated as identical” language.

### C. Exchangeability

If probabilities assigned to members of a class are invariant under finite permutations, one obtains a probabilistic symmetry. This is stronger than mere indistinguishability and should be added only if empirically motivated.

### D. Measure invariance

For regular p-adic models, Haar measure is invariant under translations. Tree automorphism-invariant measures give another option. Again, invariance is a property of the probabilistic law, not identity of states.

### E. Orbit equivalence

A symmetry group `G` partitions `X` into orbits. One can take “unconscious classes” to be orbits if the chosen symmetries are psychologically motivated. This is more flexible than fixed-prefix classes but less directly tied to the thesis's hierarchy.

### Recommended synthesis

Use **observational equivalence first**, and optionally strengthen it with a group action:

`x ~_k y` iff all level-`k` observables agree on `x,y`.

In the canonical prefix model this is equivalent to sharing the first `k` coordinates. A regular-tree automorphism group can then explain why no allowed observable prefers one representative of a fiber over another.

---

## 6. Dynamics: what is justified and what is decorative

### Natural dynamics

1. **Bayesian refinement:** posterior probabilities on child nodes after new evidence.
2. **Markov motion on a tree:** transitions among hierarchical states or between parent/child scales.
3. **Martingales on the filtration `F_k`:** conditional expectations as resolution increases.
4. **Random walks on trees:** justified if transitions between conceptual neighborhoods are part of the empirical model.

### Specifically p-adic dynamics

Polynomial maps, locally analytic maps, p-adic diffusion, wavelets, and Vladimirov-type operators become meaningful if one wants:

- scale-homogeneous dynamics;
- spectral decompositions tied to p-adic balls;
- diffusion over a hierarchy;
- analytic maps respecting the p-adic algebra.

Khrennikov's early work already proposed p-adic dynamical systems for subconscious processing and memory retrieval. Therefore, a new project should not claim novelty merely for “p-adic dynamics of ideas.”

### Recommended discipline

Start with the quotient/filtration model. Add dynamics only after defining an empirical or theoretical transition law. Do **not** retain p-adic pseudodifferential machinery solely because the original thesis used p-adic language.

---

## 7. Literature and priority audit through 2026

### Well-established before the 2015 thesis

- **Khrennikov (1998)**: *Human subconscious as a p-adic dynamical system*, Journal of Theoretical Biology 193(2), 179-196, DOI 10.1006/jtbi.1997.0604. The paper models a space of ideas by p-adic numbers and explicitly interprets p-adic nearness through a long common root.
- **Albeverio, Khrennikov & Kloeden (1999)**: *Memory retrieval as a p-adic dynamical system*, Biosystems 49(2), 105-115, DOI 10.1016/S0303-2647(98)00035-5.
- **Khrennikov (2007)**: *Toward an adequate mathematical model of mental space: conscious/unconscious dynamics on m-adic trees*, Biosystems 90(3), 656-675, DOI 10.1016/j.biosystems.2007.02.004. Mental states are branches; associations are balls; ideas are collections of balls.
- **Lauro-Grotto (2007/2008)**: *The Unconscious as an Ultrametric Set*, American Imago 64, 52-62, DOI 10.1353/aim.2008.0009. Explicitly connects ultrametric organization with Matte-Blanco.
- **Khrennikov (2010)**: *Modelling of psychological behavior on the basis of ultrametric mental space: Encoding of categories by balls*, p-Adic Numbers, Ultrametric Analysis and Applications 2(1), 1-20, DOI 10.1134/S2070046610010012.
- **Murtagh (2012)**: *Ultrametric Model of Mind, I: Review*, p-Adic Numbers, Ultrametric Analysis and Applications 4(3), DOI 10.1134/S2070046612030041, explicitly models Matte-Blanco's symmetric/asymmetric being via ultrametric topology.
- **Murtagh (2014)**: *Mathematical Representations of Matte Blanco's Bi-Logic, based on Metric Space and Ultrametric or Hierarchical Topology*, Language and Psychoanalysis 3(2), 40-63, DOI 10.7565/landp.2014.008.
- **Khrennikov (2014)**: *Cognitive processes of the brain: An ultrametric model of information dynamics in unconsciousness*, p-Adic Numbers, Ultrametric Analysis and Applications 6(4), 293-302, DOI 10.1134/S2070046614040049.

These establish that the broad idea “unconscious cognition is hierarchical/ultrametric, possibly p-adic, with categories encoded by balls” was already an active program before 2015.

### After 2015

- **Iurato, Khrennikov & Murtagh (2016)** developed further p-adic/ultrametric formal foundations for consciousness/unconsciousness and explicitly included Matte-Blanco and symmetry-breaking themes.
- **Khrennikov & Iurato (2017)** discussed topological structure of a mathematical model of the unconscious.
- **Dragovich, Khrennikov, Kozyrev & Misic (2021)** reviewed p-adic mathematics in theoretical biology, including cognition.
- Recent work continues to use tree/prefix ultrametrics in neural/computational contexts, but the hierarchy itself is by now standard mathematics rather than a distinctive novelty claim.

### What appears not to be standard in the searched literature

I did **not** find a clear prior source that makes the following exact repair the centerpiece:

> the ultrametric space remains Hausdorff, while Matte-Blanco-style indistinguishability is imposed by a finite-resolution observation quotient `X -> X_k`, equivalently an increasing filtration of accessible sigma-algebras, optionally combined with invariance under within-fiber symmetries.

This should be treated as a **potentially useful synthesis/clarification**, not yet as a priority claim. A publication-quality novelty claim would require a dedicated database-level search of the mathematical cognition, coarse-graining, symbolic dynamics, and psychoanalytic modeling literatures.

---

## 8. Strongest defensible formulation of an “ultrametric unconscious”

### Definition (resolution-limited ultrametric unconscious)

A resolution-limited ultrametric cognitive model is a tuple

`(X,d,{pi_k}_{k>=0},mu,G)`

where:

1. `(X,d)` is a complete ultrametric state space (often the boundary of a rooted locally finite tree);
2. `pi_k:X->X_k` is a nested family of finite or countable observation maps satisfying `pi_k = q_{k+1,k} o pi_{k+1}`;
3. the fiber relation `x ~_k y iff pi_k(x)=pi_k(y)` defines the states indistinguishable at resolution `k`;
4. `mu` is an optional probability measure on `X`;
5. `G` is an optional symmetry group whose action preserves the hierarchy/measure and whose relevant subgroup acts inside observational fibers.

An **unconscious mode at resolution `k`** is one in which admissible observables are restricted to functions measurable with respect to `sigma(pi_k)` (or invariant under the designated within-fiber symmetries). A transition toward finer discrimination is a refinement from `k` to `k+1` or, more generally, to a strictly finer observation partition.

### The essential point

The phrase “treated as identical” means:

`f(x)=f(y)` for every currently admissible observable `f`,

not `x=y` in the underlying space.

That distinction rescues the conceptual intuition and makes the theory mathematically orthodox.

---

## Final answers

### 1. What does ultrametricity contribute?

A canonical geometry of hierarchy: nested/disjoint balls, common ancestors, a scale of refinement, clopen concept regions, and distances determined by depth of shared classification. It is an excellent mathematical representation of hierarchical similarity.

### 2. What do p-adics contribute?

For prime `p`, they add a rich algebraic and analytic package on top of the hierarchy: arithmetic, Haar measure, Fourier/wavelet methods, analytic dynamical systems, and a canonical identification of depth-`k` concepts with congruence classes modulo `p^k`. They are not required for hierarchy itself.

### 3. What must be supplied by an observation/quotient structure?

Actual indistinguishability. Ultrametricity does not erase distinctions. The model must specify which distinctions are accessible: an observation map, equivalence relation, partition, sigma-algebra, coarse-graining, or invariance group.

### 4. Does the combination produce a mathematically interesting theory?

Yes. The combination of a hierarchical ultrametric state space with an explicit filtration of observational quotients is coherent, mathematically clean, and connects topology, probability, information, group symmetry, symbolic dynamics, and cognitive coarse-graining. Its research value will depend on going beyond rephrasing—e.g. proving nontrivial results about optimal observation schedules, dynamics under refinement, invariants of concept hierarchies, or empirical predictions.

