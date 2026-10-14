# Quantum Status Audit

## Executive finding

The **core CM/LM calculus is not quantum mechanics and is not, by itself, a nonclassical measurement theory**. It is an exact Boolean/F2 operator representation with useful quantum-inspired notation. A canonical projector semantics exists on valuation space, but it is a commuting Boolean event algebra and is therefore classical. Genuinely modal/contextual behavior requires extra state/effect/context/tensor postulates of the sort stated separately in finite-field or chain-ring models.

## 1. Axiom-by-axiom comparison

| Feature | Core compact CM/LM | Canonical diagonal CM effects | Modal finite-field/chain-ring extension | Ordinary quantum theory |
|---|---|---|---|---|
| State carrier | Boolean/formula states; one-hot valued selectors; truth tensors | subsets/support vectors on finite valuation space; optional classical distributions | nonzero/admissible vectors or module elements under an explicit contract | rays/density operators on complex Hilbert space |
| Scalars | Boolean algebra / `F_2` where declared | `R/C/F_2` can encode the same diagonal 0/1 effects | finite field or finite ring | `C` |
| Superposition | thesis OR-superposition; modern pointwise Boolean operator superposition | set union / vector support; no amplitude phase | linear combinations over finite scalar system can be genuine modal superposition after state axioms | complex linear superposition |
| Inner product | no Hilbert inner product in core | standard Euclidean inner product can be added for diagonal representation, but is not needed for Boolean semantics | usually effect-state pairing / contraction, model-dependent | complex inner product |
| Norm/positivity | absent | optional classical probability simplex | generally no real norm/probability in purely modal version | positive norm; positive density/effects |
| Born rule | absent | absent unless an external classical probability distribution is supplied | absent in possibility-only modal semantics | fundamental |
| Observable | compact CM is a truth-table operator, not generally spectral | `D_f` is a commuting sharp truth effect/projector | context families of declared effects | self-adjoint operator / POVM effects |
| Measurement update | not intrinsically defined in core | support restriction or classical conditioning | possibility branches under model-specific effects/instruments | instrument/Luders or general CP map |
| Sequential order effects | compact matrix products can be noncommutative but lack measurement semantics | none: all `D_f` commute | possible if the declared contexts/process semantics are nonclassical | possible for incompatible measurements |
| Tensor composition | truth tensors / declared flattenings | classical product valuation spaces | must specify balanced/literal tensor and admissibility | Hilbert tensor product |
| Interference | no amplitude interference in core | none | modal cancellation can occur depending on scalar arithmetic but has no Born probabilities | complex-amplitude interference |
| Contextuality | not implied by CMs | none for the full commuting event algebra | can be genuine support-level contextuality when measurement contexts/global-section obstruction are present | contextuality possible |

## 2. Bra-ket notation does not decide the issue

The current CM foundations manuscript explicitly defines one-hot Boolean states and uses bra-ket notation as compact row/map/column notation without assuming Hilbert-space physics. That is the correct stance.

The historical thesis went further rhetorically. Its `|X>` notation and matrix formulas are mathematically useful, but the notation alone establishes neither:

- complex amplitudes;
- normalization;
- phase;
- a Born probability rule;
- self-adjoint observable axioms;
- unitary dynamics;
- physical tensor composition;
- a measurement instrument.

## 3. The historical OR "superposition"

The thesis defines a logic wave as the OR of true and false possibilities and logical superposition as OR of logical states. This is cleanly interpreted as **support union**. It can be written as a 0/1 support vector, but it is not Hilbert superposition.

One could construct a modal vector-space theory over `F_2`, but doing so requires a new state/effect interpretation. The 2015 definitions do not by themselves supply that complete operational contract.

## 4. Compact-CM projectors do not form a quantum observable family

Under XOR-AND multiplication over `F_2`, 8 of the 16 compact CMs are idempotent. Only four are also symmetric: FALSE, AND, NOR, and XNOR. OR has no eigenvalue in `F_2`; XOR is involutory but does not have the truth values of the connective as its spectral data. Therefore the compact CM spectrum is an algebraic invariant, not a truth-observable spectrum.

The current CM manuscript correctly identifies a different representation:

`D_Theta=diag(Theta_11,Theta_10,Theta_01,Theta_00)`.

There the truth values are eigenvalues and valuation basis vectors are eigenvectors. This is a direct bridge to Eigenlogic-style logical observables.

## 5. Why the diagonal projector theory is classical

All `D_f` are diagonal in the same global valuation basis. Consequently

`D_fD_g=D_gD_f=D_(f and g)`.

The sharp effects form a Boolean algebra isomorphic to the power set of the finite valuation space. There is one global assignment space and no incompatibility among these effects. This is a classical event algebra written in projection-operator form.

It is therefore accurate to call it **projective logical measurement**, provided "projective" is understood algebraically. It would be misleading to present it as specifically quantum measurement.

## 6. Relation to effect algebras

The diagonal 0/1 effects are sharp effects. With complement and partial sum on disjoint events they form a finite Boolean effect algebra. Sequential product reduces to meet/intersection because all sharp effects commute.

This is exactly the classical corner of the broader effect-algebra/sequential-effect literature. Non-Boolean finite sequential effect algebras require additional structure; compact CM noncommutativity does not automatically provide it.

## 7. Relation to generalized probabilistic theories

A GPT specifies at least a convex state space, affine effects into `[0,1]`, measurements as compatible collections of effects, and transformations/instruments. The CM truth-effect algebra can be embedded into the ordinary classical simplex GPT on `Omega_n`:

- states = probability vectors on valuations;
- effects = indicator functions or general `[0,1]` functions;
- measurement probabilities = expectation of effects;
- posteriors = classical conditioning/instruments.

Nothing in the core CM calculus forces a nonclassical GPT state space.

## 8. Relation to modal quantum theory

Schumacher-Westmoreland-style modal quantum theory replaces quantitative probabilities by possibility/necessity over finite fields while retaining linear state/effect structure. The supplied chain-ring manuscript goes further to finite local/chain rings and explicitly declares:

- scalar ring;
- admissible state/resource class;
- local basis effects;
- nonzero contraction as possibility;
- complete measurement contexts;
- tensor and correction contracts for information tasks.

Those declarations are exactly what is missing from a bare CM truth-table calculus. If the attached chain-ring theorems survive their own independent review, they represent a serious genuinely modal extension of the broader research program, but they should remain a separate layer from the classical CM measurement formalism.

## 9. Relation to contextuality

Context dependence is not the same as contextuality.

- The thesis's fact that `X` is singleton-supported in one variable but not after adjoining an unconstrained `Y` is cylinder extension.
- ProLT observation families are context-dependent interfaces, but a family of commuting Boolean truth effects still has a global valuation model.
- Abramsky-Brandenburger contextuality requires an obstruction to a compatible global assignment across a measurement cover.

Thus "contextual" should be reserved for the latter kind of theorem when that measurement scenario is actually specified.

## 10. Relation to quantum cognition

Quantum cognition uses quantum probability as a mathematical model for empirical phenomena such as order effects, interference-like probability patterns, and context dependence; it need not claim physical quantum coherence in the brain. This is a more demanding standard than using quantum vocabulary.

A future CM-consciousness model would earn a nonclassical/quantum-cognitive interpretation only if it produces operationally testable deviations from the classical commuting model, for example:

- question-order effects that cannot be represented by one common Boolean event algebra;
- contextuality/global-section obstruction;
- probability interference requiring a non-Kolmogorov model;
- incompatible instruments with empirically distinct sequential predictions.

Until such evidence or axioms are supplied, the most defensible description is **a finite mathematical model of observation, refinement, and logical differentiation**.

## 11. Bottom line

- **Core CM/LM:** Boolean/F2 operator calculus; quantum-inspired notation, not quantum mechanics.
- **Diagonal CM truth effects:** rigorous projectors, but commuting/classical.
- **ProLT refinement/update:** rigorous theory of observational differentiation and conditioning.
- **Finite-field/chain-ring measurement contexts:** candidate genuinely modal/nonclassical extension, requiring separate theorem-level validation.
- **Consciousness application:** mathematically serious as an information/observation model; scientifically quantum only if additional operational axioms and empirical signatures justify that label.
