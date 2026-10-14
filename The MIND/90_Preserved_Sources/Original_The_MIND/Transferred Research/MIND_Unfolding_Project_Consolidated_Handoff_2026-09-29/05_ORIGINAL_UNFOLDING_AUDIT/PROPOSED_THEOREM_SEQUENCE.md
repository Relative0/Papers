# Proposed Theorem Sequence for a Possible Paper

## Working paper theme

**From Logical Unfolding to Observation-Refinement Complexes: A Mathematical Reconstruction of Successive Concept Differentiation**

The paper should be mathematically standalone. The 2015 thesis and Matte-Blanco provide motivation and the historical operator, but correctness should rest entirely on current definitions.

---

## Part I — Audit and algebraic reconstruction of the historical operator

### Theorem 1 — Non-congruence of historical unfolding

Prove that the factorized unfolding operator does not descend to Boolean equivalence classes. Give the minimal 3-variable redundant-factor counterexample.

**Purpose:** establishes the central syntax/semantics issue immediately.

### Proposition 2 — Gated Boolean derivative representation

For a positive conjunction, identify each unfolding summand with a negation-gated Boolean partial derivative.

**Purpose:** locates the operator in established Boolean calculus.

### Theorem 3 — Exact-layer iteration

Define the idempotent Boolean-lattice lift and prove

\[
U^k(e_\varnothing)=\bigvee_{|S|=k}e_S.
\]

**Purpose:** gives the clean mathematical realization of successive differentiation.

### Theorem 4 — Linearization dichotomy

Show

\[
D^2=2I_2
\]

in the appropriate rank-two incidence sense, hence:

- unsigned linearization is not square-zero over characteristic \(\ne2\);
- it is square-zero over \(\mathbf F_2\);
- signed incidence is square-zero over any coefficient ring.

**Purpose:** explains exactly why the historical operator resembles but is not a chain/cochain differential.

---

## Part II — Representation-invariant observation theory

### Definition 5 — Observation/refinement system

Introduce observation maps \(q_k:X\to O_k\), observational equivalence relations, and refinement by fiber splitting.

### Theorem 6 — Relational unfolding adjunction

For the unfolding relation \(R\), prove existential direct image is left adjoint to the universal residual.

**Purpose:** supplies a rigorous integration/reconstruction operator without falsely asserting invertibility.

### Proposition 7 — Non-invertibility and information-loss criterion

Characterize when relational unfolding is injective on a chosen family of admissible concepts. At minimum prove general non-injectivity; ideally classify restricted families for which the parent is identifiable.

**Potential originality:** this becomes interesting if the admissible family is tied to concept complexes or FCA closure systems.

---

## Part III — Complex-valued refinement

### Definition 8 — Concept-complex functor

Choose one canonical construction, preferably one of:

1. Dowker complex of an object-attribute relation;
2. nerve of an observation cover;
3. order complex of an observation poset.

Avoid presenting multiple alternatives as though they were one theory.

### Theorem 9 — Functoriality / chain-map theorem

Prove that refinement induces a simplicial map (or a controlled span/correspondence) and therefore a chain map

\[
U_k:C_*(K_k)\to C_*(K_{k+1})
\]

or in the natural reverse direction.

### Theorem 10 — Choice independence up to contiguity

Where a cover refinement requires choices, prove that all valid refinement maps are contiguous and therefore induce the same map on homology.

**This should be a key theorem.** It turns noncanonical local refinement into canonical global homological behavior.

---

## Part IV — Topological change and persistence

### Definition 11 — Unfolding defect

Define

\[
\Delta_n(U_k)=H_n(\operatorname{Cone}(U_k)).
\]

Optionally collect dimensions into a defect vector.

### Theorem 12 — Defect vanishing criterion

Prove

\[
\Delta_*(U_k)=0
\iff
U_k\text{ is a quasi-isomorphism}.
\]

For inclusions, identify the defect with relative homology.

### Theorem 13 — Persistence/zigzag realization

Under monotone refinement, obtain an ordinary persistence module. Under mixed add/delete refinement, prove the construction yields a zigzag module.

**Purpose:** gives mathematically correct multi-stage unfolding.

---

## Part V — Reconstruction and gluing

### Theorem 14 — Bare-face reconstruction no-go

Prove that proper-face data do not determine fillers.

**Purpose:** formally closes the main gap in the thesis's gluing intuition.

### Theorem 15 — Exact reconstruction with provenance/intersection data

State and prove exact recovery as a colimit of the full subcomplex-intersection diagram.

### Theorem 16 — Homotopy reconstruction by nerves

Under good-cover conditions, recover homotopy type through the nerve theorem.

### Theorem 17 — Semantic descent theorem

Attach a sheaf/cosheaf of concept data and prove a local-to-global reconstruction criterion.

The strongest version should state a necessary-and-sufficient obstruction to reconstruction, not merely invoke the sheaf axiom.

---

## Part VI — Symmetry is a separate invariant

### Proposition 18 — Independence of homology and automorphism symmetry

Give explicit finite counterexamples:

- symmetric contractible complex with \(H_1=0\);
- unicyclic complex with trivial automorphism group.

### Theorem 19 — Observation-induced symmetry breaking

Given \(G\curvearrowright X\) and refinement-compatible observation maps, prove a subgroup monotonicity theorem

\[
G_{q_{k+1}}\le G_{q_k}.
\]

Relate orbit splitting to observational differentiation.

This is the mathematically defensible descendant of Matte-Blanco's symmetry/asymmetry theme.

---

# Strongest single theorem target

## Observation–Refinement Descent and Cone Theorem

A high-value theorem would combine Theorems 10, 12 and 17 in one nontrivial setting.

### Candidate statement

Let \(X_k\) be an observed support equipped with finite good covers \(\mathcal U_k\), and let each next-stage observation refine the previous one, possibly while changing support through a controlled inclusion or correspondence. Let

\[
K_k=N(\mathcal U_k).
\]

Then under explicit hypotheses:

1. refinement induces a simplicial map \(r_k:K_{k+1}\to K_k\);
2. different refinement choices are contiguous, so \((r_k)_*\) is canonical;
3. if the represented support is unchanged and both covers are good, \((r_k)_*\) is an isomorphism and the mapping cone is acyclic;
4. when the support changes, cone homology identifies the relative topological defect;
5. a compatible semantic sheaf/cosheaf reconstructs global concept data exactly when its descent obstruction vanishes.

### Why this theorem matters

It gives precise answers to all four motivating questions:

- What is unfolding? **Refinement.**
- Can it be a transformation between complexes? **Yes, functorially.**
- What structural change does it make? **Cone/relative homology.**
- Can the pieces be recombined? **Exactly under colimit/descent hypotheses.**

### Research risk

Most ingredients are classical. The theorem is publishable only if the observation semantics and combined statement add a genuinely nontrivial result beyond a repackaging of the nerve theorem, standard contiguity, and sheaf descent. The next phase should therefore freeze the observation category first, then run a theorem-level priority search against that exact formalism.
