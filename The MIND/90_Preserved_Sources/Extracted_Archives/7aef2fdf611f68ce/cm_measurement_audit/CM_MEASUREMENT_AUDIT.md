# CM Measurement Audit

**Project:** Correspondence-Matrix Measurement as a Model of Logical Differentiation  
**Audit date:** 28 September 2026  
**Status:** independent reconstruction, finite verification, formal repair, and bounded literature/priority audit.

## Executive conclusion

There **is** a clean and rigorous measurement theory naturally associated with Correspondence Matrices (CMs), but it is not the thesis's unrestricted rule that every outer product `|alpha><beta|` is a projector, and it is not obtained by treating every compact 2x2 CM as a quantum observable.

The mathematically clean core is this:

1. A Boolean formula/operator `Theta` determines a truth region `E_Theta` in the finite valuation space `Omega_n={0,1}^n`.
2. The same truth data determines a diagonal sharp effect/projector

   `D_Theta = diag(1[v models Theta])`

   on the free module/vector space with valuation basis `|v>`.
3. A **selective measurement outcome** is support restriction/conditioning:

   `M_Theta(S) = S intersect E_Theta`, equivalently `s -> D_Theta s` for a support vector.
4. A **measurement question** distinguishes worlds by its two outcomes. A family of questions `Phi` determines an observation signature and hence an observational partition/topology. Adding an observation is **refinement**; learning an outcome is **update/restriction**. These are different operations.

This repaired formalism preserves the strongest mathematical intuition of the 2015 thesis: observation can convert an undifferentiated possibility set into a progressively differentiated one. It also makes precise where the quantum analogy stops. In the canonical diagonal representation all Boolean effects commute, sequential measurement is simply intersection, and there is no Born rule, amplitude interference, or specifically quantum collapse. The framework becomes genuinely modal/contextual only after adding further state/effect/context structure, such as the separately specified finite-field/chain-ring measurement scenarios; that extra structure is not entailed by the compact CMs themselves.

The most useful conceptual correction is therefore:

> **Unfolding exposes distinctions; measurement selects/conditions relative to distinctions.**

The thesis often mixes these two roles. Separating them produces a substantially cleaner theory of logical differentiation.

---

## 1. Source basis and audit method

The audit used the following supplied sources rather than assuming the historical thesis or current CM work to be correct:

- **2015 thesis:** *On the Ultrametric Unconscious, Quantum Consciousness, and Mental Spaces*, especially pp. 34-48 (CMs, bra-kets, projection, logic waves, purity), pp. 56-63 (unfolding/distinguishing), and pp. 67-72 (collapse, symmetry/asymmetry, measurement analogies).
- **Current CM/LM foundations manuscript:** `CM_LM_Boolean_Operator_Calculus_Revised.tex`, especially its explicit separation of XOR-AND matrix product, pointwise Boolean superposition, and Boolean-function superposition; its frame interpretation of literal CM rotation; and its spectral-boundary section.
- **Current ProLT observation manuscript:** `ProLT_Observation_Topologies_Submission_v0.9_FINAL.tex`, especially the observation-signature formalism and the distinction between observation refinement and premise update.
- **Current modal/chain-ring manuscript:** `Chain Ring.tex`, used only to identify what *additional* contracts are required for a genuinely modal support-level measurement theory. Its global classification theorems are not prerequisites for the core CM conclusions here.
- **Binary order-thinning manuscript:** `binary_order_thinning_finite_posets_reviewed_v3.tex`, used as a boundary on when an added observation can be modeled as same-carrier order thinning and when refinement instead changes the Kolmogorov quotient itself.

The 16 binary CMs were independently regenerated from their four truth values in true-first order `(11,10,01,00)`. Idempotence, sequential products, commutators, state actions, diagonal effects, symmetry stabilizers, and three-variable cylinder embeddings were then exhaustively enumerated. A second implementation, `verify_cm_measurement_independent.py`, does not import the main computation and passed **553 assertions**.

---

## 2. Reconstruction of the thesis measurement system

### 2.1 Classification of the historical constructions

| Thesis construction | What it actually is | Audit class | Status after reconstruction |
|---|---|---|---|
| 16 binary Correspondence Matrices | A bijective 2x2 arrangement of the four truth values of a binary Boolean function | ordinary Boolean algebra + finite matrix representation | **Sound after typing the multiplication law.** The representation itself is exact, not quantum-specific. |
| `|X>=[X,not X]^T`, `<X|=[X,not X]` | Formula/Boolean-valued row and column notation; after valuation, one-hot vectors | finite linear/semilinear algebra + quantum-inspired notation | **Sound as notation.** It is not a Hilbert-space ket unless extra scalar, inner-product, and state axioms are supplied. |
| Bra-CM-ket evaluation | One-hot selection of a truth-table entry in the numeric CM; formula pairing in the modern LM layer | Boolean/F2 operator calculus | **Sound.** Modern CM work correctly treats it as matrix-element semantics, not spectral measurement. |
| "Logical superposition" by OR | Union of alternative supports/possibilities | ordinary Boolean algebra + quantum-inspired terminology | **Mathematically usable as support union, but not Hilbert superposition.** |
| "Logic wave" = true possibility OR false possibility | A two-alternative support description | Boolean support semantics + quantum-inspired terminology | **Usable after reinterpretation.** It has no amplitudes, phase, norm, or Born probabilities. |
| `[P]=|alpha><beta|` called a projection operator | General rank-one outer product | finite linear algebra + quantum-inspired notation | **Too broad / incorrect as stated.** A general outer product is not idempotent. |
| Projective measurement = `[P]|psi>` | Action of a purported projector | underdefined | **Repair required.** Restrict `P` to an actual idempotent effect/projector and specify outcome semantics. |
| `|1><1|` and `|0><0|` as true/false measurement matrices | Coordinate projectors | finite linear algebra | **Sound special cases.** These are genuine idempotents. |
| "Pure logic state" = exactly one satisfying valuation | Singleton truth support/minterm relative to the declared ambient variables | ordinary Boolean semantics | **Sound as a definition, but not quantum purity.** It is context-relative. |
| Historical "logical distinguishability" definitions using truth of OR/AND | Satisfiability conditions, not a robust equivalence/metric of distinguishability | ordinary Boolean algebra but conceptually underdefined | **Replace.** Use observation signatures/equivalence classes from ProLT. |
| Symmetric CM = `A=A^T` | Invariance under swapping the two operands; exactly commutativity of the binary Boolean function | finite matrix/group action | **Sound but narrow.** It is not a general physical symmetry criterion. |
| Quarter-turn matrix rotation | Signed reindexing of the truth-table frame | finite group action | **Sound in modern form.** `rot(Theta)(x,y)=Theta(not y,x)`; not physical phase by itself. |
| Collapse | Usually a change from a broad Boolean support to a selected sub-support, but sometimes a change to a disjoint formula | quantum-inspired terminology; partly underdefined | **Split into restriction versus unfolding.** Only the former is measurement/conditioning. |
| Distinguishing/unfolding operator `partial` | A custom Boolean face-decomposition transform that negates one omitted coordinate | Boolean/simplicial-inspired construction | **Not a standard simplicial boundary and not measurement in general.** It can create alternatives outside the original truth support. |
| Chain-ring/modal support measurement (later work) | Nonzero-contraction possibility semantics with context families of effects | module/finite-ring mathematics; genuinely modal when the full contract is used | **A separate extension.** It must not be retroactively identified with the thesis's compact-CM measurement. |

### 2.2 The most important historical correction: an outer product is not automatically a projector

The thesis defines a projection operator by

`P = |alpha><beta|`.

In ordinary rank-one operator algebra,

`P^2 = |alpha><beta|alpha><beta| = <beta|alpha> P`.

Therefore `P` is idempotent only when the overlap scalar satisfies `<beta|alpha>=1` (or in a degenerate zero case). A concrete counterexample from the thesis's own Boolean basis is

`|1><0| = [[0,1],[0,0]]`,

which is nonzero but squares to zero under both ordinary matrix multiplication and XOR-AND multiplication over `F_2`. The independent verifier checks this explicitly. Thus the historical definition must be replaced by either `|alpha><alpha|` for normalized orthogonal basis states, or, more generally, by an operator explicitly required to satisfy `P^2=P` (and, for an ordinary orthogonal projector, `P=P*`).

### 2.3 What survives from the historical true/false measurements

The thesis's matrices

`|1><1| = [[1,0],[0,0]]` and `|0><0| = [[0,0],[0,1]]`

are genuine coordinate projections. In the compact CM atlas they coincide as arrays with AND and NOR respectively. This is a valid algebraic observation, but the *type* matters: the same 2x2 array can be read as a binary truth table or as a unary coordinate endomorphism. The modern theory should state which role is active instead of identifying them silently.

---

## 3. Rebuilding measurement in a modern CM framework

### 3.1 Valuation-space state model

For `n` propositional variables let

`Omega_n = {0,1}^n`.

A Boolean formula `f` determines its truth region

`E_f = {v in Omega_n : v models f}`.

A coarse logical state can be represented as a possibility support `S subseteq Omega_n`. If probabilities are desired, replace `S` by a distribution `p` on `Omega_n`; no probability is assumed by the core theory.

### 3.2 Canonical CM-associated truth effect

Let `V_n` be the free module/vector space with basis `{|v> : v in Omega_n}`. Define

`D_f = sum_{v in E_f} |v><v|`.

For a binary CM in true-first order,

`[Theta] = [[Theta_11,Theta_10],[Theta_01,Theta_00]]`,

this is simply

`D_Theta = diag(Theta_11,Theta_10,Theta_01,Theta_00)`.

This construction is canonical once the valuation order is fixed. It is also exactly the bridge isolated in the current CM manuscript's spectral-boundary section. It should not be confused with the compact 2x2 CM itself.

Every `D_f` satisfies

- `D_f^2=D_f`;
- over ordinary real/complex scalars, `D_f` is self-adjoint and hence an orthogonal projector;
- `im(D_f)=span{|v>:v in E_f}`;
- `ker(D_f)=span{|v>:v notin E_f}`;
- `rank(D_f)=|E_f|`;
- `D_f D_g = D_g D_f = D_{f and g}`.

For the 16 binary connectives, **all 16** therefore become sharp commuting projectors in the four-dimensional interpretation space.

### 3.3 Selective and nonselective measurement

The clean selective true-outcome update is

`M_f(S)=S intersect E_f`.

The false outcome is

`M_not_f(S)=S intersect (Omega_n \ E_f)`.

Equivalently, a support indicator vector `s` updates to `D_f s`. The complete yes/no measurement is the pair of branches `{D_f,D_not_f}`. If the outcome is ignored, the two classical support branches reunite to the original support. If a prior probability `p` is explicitly added, the selective update is ordinary conditioning

`p(v | f) = p(v) 1[v in E_f] / p(E_f)`.

Thus the core CM-associated measurement has a precise interpretation, but it is a **classical sharp event measurement**.

### 3.4 Why this is the cleanest notion of "distinguishing"

Measurement has two logically different components:

- **a question/effect**, which can separate states into outcome classes;
- **an outcome update**, which removes states incompatible with the recorded outcome.

The current ProLT framework supplies the right language for the first component. For an observation family `Phi=(phi_1,...,phi_m)`, define

`o_Phi(v)=(1[v models phi_1],...,1[v models phi_m])`.

Two valuations are observationally indistinguishable exactly when they have the same signature. Adding a new observation `psi` strictly increases distinguishability on a carrier `S` precisely when there are `v,w in S` such that

`o_Phi(v)=o_Phi(w)` but `psi(v) != psi(w)`.

This is stronger and cleaner than the thesis's satisfiability-based definitions of distinguishability.

---

## 4. Exhaustive projector classification of the 16 compact CMs

The same 16 binary arrays behave differently under different multiplication laws. The audit therefore kept four algebras separate.

| Multiplication law on compact 2x2 CMs | Idempotent CMs | Count | Ordered idempotent pairs | Commuting pairs | Noncommuting pairs | Products still idempotent |
|---|---:|---:|---:|---:|---:|---:|
| XOR-AND matrix product over `F_2` | FALSE, AND, NOR, X, Y, XNOR, NOT_Y, NOT_X | 8 | 64 | 40 | 24 | 58 |
| OR-AND Boolean-semiring matrix product | previous 8 + X_IMPLIES_Y, Y_IMPLIES_X, TRUE | 11 | 121 | 65 | 56 | 115 |
| ordinary integer matrix product | same 8 as `F_2` | 8 | 64 | 36 | 28 | 54 |
| cyclic convolution over `F_2` on the four rotation coordinates | FALSE, AND | 2 | 4 | 4 | 0 | 4 |

The full row-by-row data, state actions, finite images/kernels, and ranks are in `PROJECTOR_CLASSIFICATION.csv`; all ordered products are in `SEQUENTIAL_MEASUREMENTS.csv`.

Two conclusions matter for measurement theory.

First, **compact-CM idempotence is representation- and multiplication-dependent**. One cannot call a 2x2 truth-table array a projector without saying which multiplication is being used.

Second, even when compact idempotents fail to commute, this alone does **not** create quantum measurement. For example, some products of compact idempotents cease to be idempotent, and ordinary integer products can even leave the 0/1 matrix set. No Born probabilities, positive effects, state-update axiom, or operational measurement context follows from this noncommutativity.

The cyclic-convolution result is especially sharp. The separate coefficient algebra is `F_2[C_4] ~= F_2[u]/(u^4)`, a local ring, so it has only the trivial idempotents 0 and 1. In the chosen coefficient basis these are FALSE and AND. Therefore the phase/convolution algebra does **not** supply a rich internal projector lattice for the 16 CMs.

By contrast, the valuation-space diagonal representation has 16/16 projectors, all commuting. It is therefore the right representation if the goal is logical event measurement.

---

## 5. Sequential measurements and compatibility

For the canonical diagonal effects,

`D_f D_g = D_{f and g} = D_g D_f`.

Hence every pair is compatible in the commutation sense and a sequence of recorded true outcomes is simply accumulated Boolean restriction:

`S -> S intersect E_f -> S intersect E_f intersect E_g`.

Order cannot matter in this core theory. This is the decisive reason the repaired CM measurement is classical rather than quantum-like in the operational sense.

A useful distinction is:

- **compact-CM product noncommutativity** = an algebraic property of one representation;
- **measurement incompatibility/order effect** = an operational property of effects/instruments acting on states.

The first does not imply the second.

---

## 6. Symmetry breaking: the proposed stabilizer criterion fails as a general test

The thesis uses transpose symmetry, which for a binary CM is exactly invariance under exchanging the two operands. Exhaustive enumeration confirms that 8 of the 16 binary connectives are transpose-symmetric and 8 are not.

To test a broader symmetry criterion, the audit used the natural signed-input square group `D_4`, generated by swapping `X,Y` and independently negating the two coordinates. For a truth support `S`, let `Stab(S)` be its stabilizer under this group.

The proposed condition

`|Stab(M(S))| < |Stab(S)|`

is **not** a reliable definition of increased distinguishability. Among nonempty strict restrictions `S -> S intersect E`, exhaustive enumeration found:

- 30 cases in which the stabilizer decreased;
- 8 cases in which it **increased**;
- 72 cases in which it stayed the same.

For example,

`X_IMPLIES_Y -> XNOR`

under restriction by XNOR shrinks the support from 3 valuations to 2 while the `D_4` stabilizer grows from 2 to 4. The selected subset is *more symmetric* even though uncertainty has decreased. Conversely,

`XOR -> X_AND_NOT_Y`

shrinks support from 2 valuations to 1 and the stabilizer decreases from 4 to 2.

There is a conceptual reason. If a map `M` were fully `G`-equivariant, then `Stab_G(x) subseteq Stab_G(M(x))`; an equivariant map cannot reduce the stabilizer. Symmetry reduction occurs because a chosen effect/context itself breaks part of the original group action. Stabilizer size therefore measures symmetry, not distinguishability.

The exact criterion for **new distinguishability** is instead partition refinement: a new observation must split at least one existing observation-signature fiber.

See `SYMMETRY_REDUCTION.md`, `SYMMETRY_TABLE.csv`, and `RESTRICTION_SYMMETRY_TRANSITIONS.csv`.

---

## 7. Context dependence and the thesis's "pure" states

The thesis defines a pure logic state as one having exactly one satisfying truth assignment. This is a well-defined combinatorial notion, but it depends on the ambient variable universe.

Let a formula `f` depend on `n` variables and embed it canonically into `n+m` variables by ignoring the new variables. Its truth region becomes the cylinder

`E_f x {0,1}^m`.

Therefore

`|E_f^(n+m)| = 2^m |E_f^(n)|`.

Consequently, any satisfiable singleton support ceases to be singleton as soon as at least one unconstrained variable is adjoined. The audit reproduced the thesis's phenomenon explicitly:

- `X` has support size 1 in one variable and size 4 in a three-variable universe;
- `X and not Y` has support size 1 in two variables and size 2 in three variables;
- `X XOR Y` has support size 2 in two variables and size 4 in three variables.

This is ordinary **cylinder-set extension**, not contextuality in the sheaf/global-section sense. A deeper contextual theory requires incompatible measurement contexts or the failure of a global assignment. The separate modal chain-ring program supplies that kind of additional structure; the cylinder phenomenon alone does not.

The diagonal projector rank tracks this exactly: under an `m`-variable cylinder extension, `rank(D_f)` is multiplied by `2^m`. Compact 2x2/F2 rank should not be used as a purity measure because it is a different invariant of a different representation.

---

## 8. Measurement versus unfolding

The thesis's distinguishing operator `partial` is best understood as an **unfolding/refinement transform**, not generally as measurement.

The decisive finite example is the thesis's own two-variable intuition:

`partial(X and Y) = X XOR Y`.

As truth supports,

- `E_(X and Y) = {11}`;
- `E_(X XOR Y) = {10,01}`.

These are disjoint. Therefore `X and Y -> X XOR Y` cannot be a selective conditioning/restriction of the original state. It creates/exposes alternatives rather than selecting a surviving alternative.

This suggests a clean typed split:

- `U` (**unfolding/refinement**) enlarges the observation description or expands a coarse representation so that previously hidden alternatives become separately expressible;
- `M` (**measurement/update**) conditions the current possibility state on a recorded outcome.

The current ProLT manuscript already has the exact analogue: enlarging the observation family is refinement on a fixed carrier, whereas learning a premise restricts the carrier. If `U` merely adds observations on the same carrier and the measurement effect `E` is defined independently of that refinement, the natural restriction/refinement square commutes. If unfolding changes the carrier, introduces latent coordinates, or makes the measurement effect definable only after expansion, `MU` and `UM` need not agree and may not even have the same type.

This separation is one of the strongest recoveries from the thesis. It preserves both intuitions without forcing one operator to do incompatible jobs.

---

## 9. A complete finite path from a coarse state to a differentiated state

Take `Omega_2={11,10,01,00}` and begin with the totally coarse possibility state

`S_0 = TRUE = {11,10,01,00}`.

A valid two-stage selective measurement path is

`TRUE --(XOR=true)--> XOR={10,01} --(X=true)--> X_AND_NOT_Y={10}`.

In diagonal form,

`D_XOR = diag(0,1,1,0)`,

and the second true outcome applies `D_X=diag(1,1,0,0)`, leaving

`D_X D_XOR = diag(0,1,0,0) = D_(X_AND_NOT_Y)`.

The possibility count falls `4 -> 2 -> 1`. Under a uniform prior, the two recorded outcomes yield 1 bit and then 1 further bit of Hartley/Shannon information. The last state is a singleton minterm and therefore maximally differentiated with respect to the two declared Boolean coordinates.

This example also separates **differentiation** from **symmetry breaking**. TRUE and XOR are both invariant under operand swap; the first restriction decreases uncertainty without breaking that symmetry. The second branch to `X_AND_NOT_Y` breaks operand-swap symmetry. Thus the two notions should not be identified.

---

## 10. Quantum-status audit in one paragraph

The core CM/LM calculus is Boolean/F2 mathematics with one-hot selection, truth tensors, signed frame actions, and formula-valued operator structure. Its bra-ket notation is representational; its OR-based "superposition" is support union; and its native compact-CM semantics supplies neither Born probabilities nor state collapse. The canonical diagonal truth effects are projectors, but they all commute and therefore form a classical Boolean sharp-effect algebra. A generalized probabilistic theory would additionally require a convex state space and probabilistic effects/instruments. A genuinely modal theory can be built by adding a finite-field/ring module, admissible states/effects, tensor composition, measurement contexts, and a nonzero-contraction possibility rule; that is an enrichment, not a hidden property of the 2x2 CMs. See `QUANTUM_STATUS_AUDIT.md` for the full axiom-by-axiom comparison.

---

## 11. Literature and priority result

A 2026-current literature search does **not** support priority for the broad ideas "logic by matrices," "logical bra-matrix-ket evaluation," or "logical propositions as projectors." Strong antecedents include Stern's *Matrix Logic* (1988), Mizraji's vector logic (1992/1996), Bricken's internally dated 1997 matrix-logic notes, semi-tensor-product Boolean logic, Cheng-Zhao-Xu's Boolean matrix calculus (2011), and Eigenlogic's explicit treatment of logical propositions as commuting projectors with truth values as eigenvalues (2015/2016 preprints; 2020 publication). Quantum-like cognitive measurement on p-adic mental spaces also predates the thesis in Khrennikov's 2001 preprint / 2003 paper.

The modern CM/LM manuscript already draws the correct priority boundary: the strongest defensible contribution lies in its **typed formula-valued LM architecture, frame coherence, pairing, and integration**, not in matrix logic or physical measurement firstness. The measurement formalism developed in this audit should likewise be presented as a rigorous integration/repair of CM truth operators with standard finite event/projector semantics and the newer ProLT distinction between observation refinement and update.

See `LITERATURE_PRIORITY_MAP.md` for construction-level comparisons and URLs/DOIs.

---

## 12. Proposed theorem program

The clean paper-sized mathematical development is summarized in `THEOREM_SEQUENCE.md`. The central sequence is:

1. CM/event/diagonal-projector equivalence on finite valuation space.
2. Exact image/kernel/rank and selective-measurement theorem.
3. Sequential-measurement/intersection theorem and commutativity/classicality corollary.
4. Complete 16-CM compact idempotent classification under each multiplication law.
5. Failure of stabilizer monotonicity under restriction.
6. Exact observation-refinement criterion for increased distinguishability.
7. Cylinder-extension theorem for context-relative purity.
8. Refinement/update commutative square.
9. Classicality boundary for the core CM measurement algebra.
10. Optional modal-extension theorem schema stating exactly which additional contracts are required before contextual measurement claims are meaningful.

---

## 13. Answers to the five required questions

### 1. What is the cleanest CM notion of measurement?

A CM represents a Boolean event/effect; lift its truth vector to the valuation-space diagonal projector `D_Theta`. A recorded outcome acts by `S -> S intersect E_Theta` (or `s -> D_Theta s`). The measurement question itself is represented by the two complementary effects. This is mathematically exact, typed, and compatible with the modern CM framework.

### 2. Does it give anything beyond ordinary Boolean restriction?

At the **core measurement level, no**: the canonical sharp CM measurement is ordinary finite Boolean event restriction/conditioning written in operator form. The genuinely useful extra structure is organizational: CM/LM typing, frame actions, tensorization, and the ProLT observation architecture make it possible to distinguish *what can be observed* from *which possibilities survive*. Nonclassical behavior requires extra modal/probabilistic/contextual postulates not present in the compact CM calculus.

### 3. When does it increase distinguishability?

Adding an observation `psi` increases distinguishability exactly when it splits an existing observation-signature class: there exist `v,w` with the same old signature but different `psi` values. A recorded outcome may reduce uncertainty whenever it is a proper nonempty restriction, but that is not the same as increasing pairwise distinguishability among survivors. Stabilizer decrease is neither necessary nor the right definition.

### 4. How does it differ from unfolding?

Unfolding/refinement exposes or creates a finer description of alternatives; measurement/conditioning selects the alternatives compatible with an outcome. The thesis's `AND -> XOR` example proves they cannot be identified because XOR is disjoint from the AND truth support. Under fixed-carrier observation refinement, unfolding and measurement satisfy a natural commuting restriction square; under carrier-expanding unfolding they need not commute.

### 5. Is there a serious mathematical route from this theory to the thesis's intended notion of conscious differentiation?

**Yes as a rigorous mathematical model of logical/observational differentiation, not yet as a theory of phenomenal consciousness.** A defensible route is to model an informational state by `(S,Phi)`: `S` is the current possibility support and `Phi` the currently available observation family. Differentiation has two independent monotone directions: refine `Phi` to split observational equivalence classes, and condition `S` on recorded outcomes to reduce uncertainty. This gives exact finite invariants, commuting diagrams, information measures, and testable order/context extensions. To make a scientific claim about consciousness, the model would still need an operational mapping from cognitive/neural experiments to states, observations, and updates, plus empirical predictions that distinguish it from ordinary classical conditioning. If noncommutative/quantum-cognitive behavior is claimed, order effects, contextuality, or probability-interference data would have to justify the extra structure rather than the words "superposition" or "collapse" doing so by analogy.

---

## Reproducibility files

- `cm_measurement_compute.py` — exhaustive primary enumeration.
- `verify_cm_measurement_independent.py` — separate implementation and cross-check.
- `verification_report.json` — 553-predicate PASS record.
- `PROJECTOR_CLASSIFICATION.csv` — all 16 compact CMs under four multiplication laws.
- `DIAGONAL_EFFECT_PROJECTORS.csv` — all 16 canonical valuation-space projectors.
- `SEQUENTIAL_MEASUREMENTS.csv` — compact algebraic sequences plus all 256 diagonal-effect sequences.
- `SYMMETRY_TABLE.csv`, `RESTRICTION_SYMMETRY_TRANSITIONS.csv` — symmetry audit.
- `THREE_VARIABLE_EMBEDDING.csv` — explicit context/cylinder examples.
