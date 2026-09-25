# Master Topic Inventory for the Correspondence Matrix / Logical Matrix Research Threads

**Prepared:** 25 September 2026  
**Purpose:** Consolidate the distinct mathematical, computational, modal/quantum-inspired, historical, prior-art, manuscript-planning, and verification topics explored across the seven supplied ChatGPT threads, so that later papers and handoffs do not silently omit an explored direction or accidentally revive a superseded result.

## Source thread links supplied

1. https://chatgpt.com/c/6ab49adc-5888-83ec-852c-a63124e76bdf
2. https://chatgpt.com/g/g-p-6aabc134341881918ea2ca92b07bfdfb-quantum-cm/c/6ab26040-cfe8-83ec-8de7-23fbcd2eb7e1
3. https://chatgpt.com/g/g-p-6aabc134341881918ea2ca92b07bfdfb-quantum-cm/c/6ab188aa-f804-83ec-b2d7-dc7796e71f8c
4. https://chatgpt.com/g/g-p-6aabc134341881918ea2ca92b07bfdfb/c/6aac475c-a990-83ec-8da2-031cfb2da232
5. https://chatgpt.com/c/6aacf01c-1610-83ec-ab87-5f759032e7fe
6. https://chatgpt.com/g/g-p-6aabc134341881918ea2ca92b07bfdfb/c/6aabc2cf-848c-83ec-91fa-5bceb1746e5a
7. https://chatgpt.com/g/g-p-6aabc134341881918ea2ca92b07bfdfb/c/68ea8fa6-f9a0-8321-ac82-daa866c7d327

## Retrieval note

The private ChatGPT URLs themselves are login-gated and did not expose their full transcripts through ordinary web access. The topic inventory below was therefore reconstructed from retrievable prior-conversation context associated with the user's CM/LM research program, including exact opening prompts, later audits, corrections, manuscript splits, theorem candidates, computational checks, and handoff summaries when those were recoverable.

This gives strong coverage of the **union of topics explored**, but exact URL-to-message provenance is incomplete for several of the seven links. For that reason, this document is organized primarily by research topic and chronological research cluster rather than pretending to possess a perfect per-link transcript map.

---

# 1. Status legend

The following labels are useful when turning this inventory into papers or a research register.

- **ESTABLISHED / CHECKED** — proved in the working framework and/or exhaustively computationally checked within a stated finite scope.
- **THEOREM CANDIDATE** — formalized or strongly supported, but should still be independently proof-audited and novelty-audited.
- **MODEL-DEPENDENT** — true only for a particular tensor, measurement, gate, scalar, or process model.
- **PRIOR-ART HEAVY** — mathematically useful, but the basic phenomenon has substantial antecedents.
- **NEGATIVE / OBSTRUCTION** — a no-go, failure, limitation, or non-closure result.
- **CORRECTED / SUPERSEDED** — an earlier conclusion was later repaired or replaced.
- **OPEN** — investigated but not fully resolved.
- **HISTORICAL / EXPLORATORY** — useful for the intellectual history, but not part of the later audited core.

---

# 2. High-level research clusters represented across the threads

## 2.1 CM/LM foundations and Boolean operator calculus

Major recurring themes:

- compact `2 x 2` Correspondence Matrices for the 16 binary Boolean connectives;
- ordered bra/ket basis conventions and explicit basis-state construction;
- Boolean matrix arithmetic over `F_2` using XOR as addition and AND as multiplication;
- formula-valued Logical Matrices;
- valuation from symbolic LMs to numerical CMs;
- logical pairing;
- operator-on-operator Boolean composition or "superposition";
- frame transport, operand polarity, operand exchange, and normalization;
- higher-arity CMs/LMs;
- arbitrary-arity tensors and matrix flattenings;
- block lifts;
- ANF/Mobius/Reed-Muller relations;
- coherence of symbolic and numerical calculations.

This cluster ultimately became the center of **Correspondence and Logical Matrices: A Boolean Operator Calculus**.

## 2.2 CM computation / compiler research

Recurring themes:

- CMs as a structural representation or IR rather than a claim of a universally faster flat evaluator;
- typed operand frames;
- signed frame normalization;
- operator fusion before expansion;
- structural reduction;
- symbolic DAG/IR compilation;
- retabulation, hybrid execution, and safe fallback;
- bitset execution;
- no-reinflate execution;
- persistent structural caching;
- compile-once/evaluate-many workflows;
- quotienting, measurement, conditioning, and decomposition;
- benchmark methodology and competitor matching;
- correctness gates and pre-freeze protocol audits.

This became the post-split **Operator-Level Boolean Computation with Correspondence Matrices** program.

## 2.3 Pure-Boolean phase / rotation algebra

Recurring themes:

- literal four-cycle rotation of the CM cell positions;
- the `4 x 4` rotation operator `R`;
- the algebra `F_2[C_4]`;
- the chain-ring presentation `F_2[u]/(u^4)`;
- nilpotent filtration;
- rotation/reversal/complement identities;
- Boolean "phase" language;
- transpose/conjugation analogues;
- intrinsic unitary-like and mixer-like operators;
- XOR-cancellation interference.

## 2.4 Boolean modal / quantum-information laboratory

Recurring themes:

- modal state semantics;
- nonzero = possible support rules;
- nonseparability;
- Bell-style support contradictions;
- Hardy witnesses;
- GHZ constructions;
- contextuality;
- teleportation;
- dense coding;
- no-cloning;
- phase kickback;
- Boolean oracle algorithms;
- stabilizer/normalizer analogues;
- probability-completion obstructions;
- tensor-model dependence.

## 2.5 Canonical LM-to-modal bridge

A separate investigation asked whether the formula-valued LM calculus itself canonically generates the later modal/chain-ring measurement theory.

The eventual answer was **only partially**:

- Boolean LM valuation and contraction are canonical;
- symbolic support can be enriched;
- chain-ring amplitudes, modal support semantics, measurement bases, effects, tensor products, and update rules require extra structure/postulates;
- bare LMs do not automatically constitute a quantum or modal quantum theory.

## 2.6 Spectral/dynamical classification of the 16 compact CMs

A dedicated line classified the 16 matrices by:

- rank;
- determinant;
- characteristic/minimal polynomial;
- invertibility;
- nilpotence/idempotence/involution;
- dynamics on `F_2^2`;
- similarity classes;
- signed-frame orbits;
- valuation spectra;
- affine versus nonlinear behavior;
- semigroup/group structure.

## 2.7 Historical quantum-style CM/LM exploration

Earlier threads explored, before the later audits:

- Hermiticity;
- matrix commutators;
- possible logical Lie-algebra structures;
- simultaneous diagonalization;
- a proposed "logical imaginary unit";
- complex-valued fuzzy truth;
- symbolic Hadamard/CNOT analogies;
- Bectors/B-modules;
- evolutionary/time-dependent LMs;
- psychological/consciousness motivations;
- measurement and symmetry-breaking analogies.

These should be preserved as historical/exploratory material, not automatically treated as later validated claims.

---

# 3. Correspondence Matrix foundations

## 3.1 The 16 compact binary CMs

Topics explored:

- Every binary Boolean connective has a compact `2 x 2` truth-value matrix once row/column basis order is fixed.
- The collection contains the usual connectives:
  - FALSE;
  - TRUE;
  - AND;
  - OR;
  - XOR;
  - XNOR/equivalence;
  - NAND;
  - NOR;
  - implications and converse implications;
  - projections and negated projections.
- Basis/order conventions matter and must be stated before transformations or equivalence comparisons.

### Notation conventions that became important

Later manuscripts prefer:

- `B = {0,1} ~= F_2`;
- XOR written as `\Updownarrow`;
- XNOR/equivalence written as `\Leftrightarrow`;
- binary operator variable `\Theta`;
- compact CM `[\Theta]`.

A specific geometric motivation was retained: the XOR CM is a quarter-turn / 90-degree cell rotation of the XNOR CM under the chosen display convention.

## 3.2 Bra-ket construction and contraction

Explored repeatedly:

- Boolean bras and kets as state selectors;
- outer products producing the elementary matrix locations;
- the correction that the basic outer-product form is ket times bra, e.g. `|0><1|`, not `|0>|1>`;
- Boolean contraction using XOR over AND products;
- Einstein-style indexing such as a Boolean analogue of `X_i \Theta_{ij} Y_j`.

The bra-ket formalism was treated as a useful operator notation, not evidence by itself of quantum mechanics.

## 3.3 Matrix transformations corresponding to logical transformations

Topics included:

- transpose as operand exchange;
- row/column permutations as input negations or polarity changes;
- quarter-turn rotations;
- full-expression complement;
- literal-negation transforms;
- canonical variable ordering before tensor/direct-product construction;
- signed frames or polarity masks;
- relationships among transformed matrices.

These transformation rules became important both mathematically and for typed compilation.

## 3.4 General finite expressions and higher-dimensional CMs

The work moved beyond only binary `2 x 2` matrices.

Topics:

- general finite propositional expressions represented over ordered assignments;
- `2^n x 2^n` or otherwise higher-dimensional matrix forms, depending on chosen input/output partition;
- arbitrary-arity truth tensors;
- bipartition flattenings;
- row/column frame typing;
- block-matrix lifts;
- tensor-style constructions;
- larger logical matrices built from smaller operators.

A recurring warning was that higher-dimensional constructions are only canonical after basis, variable order, partition, and polarity conventions have been fixed.

## 3.5 Measurement / reconstruction / quotienting / conditioning

CM-native operations explored included:

- selecting or "measuring" rows/columns;
- reconstructing expressions or partial truth relations;
- quotienting or feature subtraction;
- conditioning on fixed variables;
- decomposition;
- partial output rather than forced dense reinflation.

A later computational clarification: these are structural operations on the representation; they should not automatically be described using physical quantum-measurement language.

---

# 4. Formula-valued Logical Matrices

## 4.1 Formula-valued LM layer

A major conceptual distinction was developed between:

- **CMs:** evaluated numerical truth tables/matrices;
- **LMs:** entries that are formulas, terms, or logical expressions.

This made it possible to keep symbolic relations inside matrix form before valuation.

## 4.2 Canonical term lift

A recurring manuscript fix was to state explicitly how a Boolean operator or truth table is lifted to a formula-valued matrix.

This was important because otherwise the manuscript risked moving informally between:

- formulas;
- symbolic matrix entries;
- truth-table coefficients;
- evaluated CMs.

## 4.3 LM to CM valuation

A core result/organizing principle:

- valuation is applied coefficientwise to an LM;
- symbolic contraction and evaluation commute under the stated Boolean semantics;
- numerical CMs are the evaluated shadow of the formula-valued LM.

This is one of the strongest conceptual bridges in the foundations paper.

## 4.4 Logical pairing

A recurring formula was the logical analogue of a bilinear pairing. In one common binary form, the result has the semantics

`<A | M_f(X,Y) | B> = f(A <-> X, Y <-> B)`

with the manuscript's XNOR/equivalence notation.

Interpretive theme:

- pairing compares/aligns external formulas or states with the internal operands;
- the result can be read via "agreement bits";
- the same idea generalizes to higher arity.

## 4.5 Pairing/valuation coherence

Important topics:

- valuation commutes with the pairing construction;
- symbolic and numeric views give the same evaluated result;
- higher-arity pairing coherence;
- frame transport must be accounted for before comparing or combining operators.

This became part of a broader **coherence theorem** or coherence architecture for the paper.

## 4.6 Operator-on-operator Boolean superposition

A separate operation from Boolean matrix multiplication was developed:

- apply a Boolean connective pointwise to aligned matrix entries;
- interpret this as combining whole logical operators;
- lift the same idea symbolically to LMs.

Important distinctions:

- pointwise Boolean operator combination is not the same as XOR-AND contraction;
- same-frame pointwise combination has substantial prior art;
- the distinctive contribution, if any, lies more in the typed LM/valuation/pairing/frame integration than in raw truth-table superposition.

## 4.7 Signed-frame actions

Themes:

- operand order;
- input polarity;
- axis orientation;
- signed/polarity frame actions;
- group structure approximately of the form `(C_2)^n semidirect S_n` for permutation/polarity action;
- normal forms for binary LMs such as factoring operand polarity transforms around a core operator matrix.

One audited normal-form statement had the shape

`M_{X Theta Y} = S_X [Theta] S_Y`

with involutive selector/polarity matrices.

## 4.8 Polarity-mask correction

A concrete correctness repair was found:

- one printed polarity-mask convention failed in 48 of 64 exhaustive cases;
- the mask needed a complemented/XOR-adjusted convention rather than the originally written form.

This is an important "do not regress" item for future versions.

## 4.9 All-true valuation / existence assumptions

Another manuscript-level correction:

- statements involving an "all-true" valuation need existence/compatibility assumptions;
- one should not silently assume arbitrary symbolic formulas can simultaneously receive the desired values.

---

# 5. Coherence and closure results

## 5.1 Boolean closure of operator superposition

The aligned pointwise Boolean combination of binary truth-table matrices remains a valid binary truth-table matrix.

This is algebraically straightforward but important for the operator-calculus narrative.

## 5.2 Symbolic-to-numeric commuting diagrams

The program repeatedly emphasized commuting diagrams of the form:

formula-valued LM  
→ symbolic operator combination / pairing  
→ valuation

versus

formula-valued LM  
→ valuation to CM  
→ numerical operator combination / pairing.

The goal was to show that the symbolic and numerical calculi are not two disconnected formalisms.

## 5.3 Higher-arity closure

Higher-arity extensions included:

- truth tensors;
- tensor flattenings;
- block lifts;
- n-ary pairing;
- aligned frame transport;
- arbitrary finite Boolean operators.

## 5.4 ANF parity bridge

Connections were developed between:

- truth-table coefficients;
- parity transforms;
- algebraic normal form;
- Boolean Mobius transformation;
- operator lifts.

This became especially important in the later phase/oracle work.

---

# 6. Spectral and dynamical classification of the 16 compact CMs

This was a distinct investigation and should not be lost inside the larger CM/LM manuscript.

## 6.1 Rank and determinant

A key structural classification:

- determinant zero iff rank is at most one;
- rank-one/singular binary connectives can be characterized as separable forms such as a one-variable function AND another one-variable function, under the chosen Boolean matrix arithmetic.

An ANF determinant identity was also derived, of the schematic form

`det = alpha_X alpha_Y XOR alpha_0 alpha_XY`.

## 6.2 The six invertible matrices

The six invertible `2 x 2` binary CMs form

`GL_2(F_2) ~= S_3`.

Identified dynamics included:

- XNOR/equivalence as the identity;
- XOR and the two implication-like elements as order-two elements;
- OR and NAND as order-three elements.

Specific iteration identities included:

- `OR^2 = NAND`;
- `OR^3 = XNOR`.

## 6.3 Nilpotent / idempotent / involutive behavior

The 16 matrices were explored for:

- nilpotence;
- idempotence;
- involutions;
- finite iteration cycles;
- functional graph structure.

The all-ones/tautology matrix is nilpotent under `F_2` matrix multiplication because its square vanishes in characteristic two.

## 6.4 Polynomial and similarity classification

Topics included:

- four characteristic-polynomial classes;
- six similarity/minimal-polynomial classes;
- six functional-graph types over `F_2^2`;
- splitting-field/eigenstructure considerations where needed.

## 6.5 Frame and valuation spectra

A particularly interesting result:

- valuation spectra across the basic signed-frame transforms `A, PA, AP, PAP` were compared;
- equality of those spectra characterizes affine functions in the reported analysis;
- the multiset of valuation minimal polynomials was reported to recover the six signed-frame orbits.

## 6.6 Pointwise superposition audit

Thousands of pointwise operator-combination cases were checked.

Findings included:

- some structural subsets, such as symmetric matrices, are closed under broad families of pointwise Boolean operations;
- pointwise AND preserves singularity in the reported binary audit;
- invertibility and idempotence are not universally preserved.

## 6.7 Semigroup / Cayley / commutation questions

Related exploratory topics:

- multiplication tables;
- Cayley tables;
- semigroup structure of all 16 matrices;
- commutation relations;
- centralizers;
- logical analogues of algebraic operator relations.

These connect historically to the earlier "logical Lie algebra" discussions, although the later finite-field classification is the more rigorous setting.

---

# 7. CM-cell rotation and the intrinsic phase algebra

## 7.1 The order-four rotation `R`

A literal quarter-turn of the four positions in a compact `2 x 2` CM was lifted to a `4 x 4` permutation matrix `R` with

`R^4 = I`.

This supplied an intrinsic cyclic action derived from the CM geometry itself.

## 7.2 The 16-element centralizer / circulant algebra

The centralizer of the four-cycle was identified with the `F_2`-span

`Lambda(a) = a_0 I + a_1 R + a_2 R^2 + a_3 R^3`.

This gives a 16-element algebra of binary circulant operators commuting with `R`.

## 7.3 Group algebra and chain-ring identification

A central structural result:

`F_2[C_4] ~= F_2[u]/(u^4)`

with

`u = I + R`

or, in XOR notation, `u = I XOR R`.

This algebra is a finite local chain ring.

## 7.4 Nilpotent filtration

With `N = I + R`:

- `N^4 = 0`;
- powers give a descending filtration;
- matrix ranks follow the sequence `4,3,2,1,0` for the successive powers in the regular representation;
- ideals correspond to powers `(u), (u^2), (u^3)`.

This became one of the clearest algebraic structures emerging from literal CM rotation.

## 7.5 Units and nilpotents

The 16-element ring splits into:

- units;
- nonunits/nilpotents;
- a chain of ideals controlled by `u`-valuation.

Counts and explicit element classifications were explored.

## 7.6 Boolean degree versus lifted reversibility

A strong theorem candidate linked Boolean-function structure to the lifted rotation algebra.

For a binary truth table lifted to `Lambda(a)`:

- invertibility corresponds to odd truth-table weight;
- equivalently, the top ANF coefficient is one;
- equivalently, the Boolean function has full degree two in the binary case.

A higher-arity generalization was explored in which **maximum degree**, not merely generic nonlinearity, is the relevant reversibility criterion.

## 7.7 Operand reversal and phase reversal

Operand exchange / truth-table reversal was connected to

`R -> R^{-1}`.

This supplied a natural involution-like operation on the cyclic phase algebra.

## 7.8 Complement and the deepest nilpotent layer

Complementing a Boolean function was related to adding the highest nonzero nilpotent term, schematically

`Lambda(not f) = Lambda(f) + N^3`.

This is a compact algebraic way of seeing Boolean complement inside the chain-ring representation.

## 7.9 Transpose/conjugation analogue

Because `R^T = R^{-1}`, transpose acts like a reversal/conjugation operation on the cyclic coefficients.

This was used to motivate a star-like algebraic language, with care not to overstate the analogy with complex conjugation.

## 7.10 Degenerate norm

A multiplicative or star-based norm was explored.

Important limitation:

- the norm is degenerate because the ring has nilpotents/zero divisors;
- therefore this intrinsic algebra does **not** produce a Born-rule probability theory.

This is one of the major safeguards against overinterpreting the phase analogy.

---

# 8. Intrinsic unitary-like operators, mixers, and splitters

## 8.1 Intrinsic star-unitaries

The chain-ring/star algebra was searched for operators satisfying unitary-like equations.

Reported finite counts included:

- 65,536 total `2 x 2` matrices over the 16-element ring;
- 24,576 invertible matrices in one full inventory;
- 512 intrinsic star-unitary-like matrices;
- hundreds of nonmonomial examples.

The exact count belongs to the stated definition of intrinsic unitarity and should not be generalized to other notions without rechecking.

## 8.2 Mixer / splitter operators

A Boolean mixer of the form

`H_* = [[1, delta], [delta, 1]]`

with nilpotent `delta` and `delta^2 = 0`

was studied.

Properties investigated:

- reversibility;
- star-unitarity under the intrinsic involution;
- branch mixing;
- generation of Bell-like nonseparable states.

Thousands of "splitter" candidates were counted in exhaustive searches.

## 8.3 Rotation is not itself the mixer

A recurring conceptual clarification:

- `R` is the phase/cell-rotation operator;
- it should not be conflated with the branch-mixing operator.

This became important for avoiding loose quantum analogies.

---

# 9. XOR interference and cancellation

## 9.1 Interference as characteristic-two cancellation

The cleanest intrinsic interference analogue is simply:

- multiple computational paths are combined by XOR;
- equal contributions cancel;
- phase-like ring coefficients can create or remove support through zero-divisor multiplication and XOR addition.

This is exact algebra, not probabilistic wave interference.

## 9.2 Shear / interferometer constructions

Simple reversible shears and mixer-phase-mixer patterns were investigated as Boolean analogues of interferometers.

## 9.3 Zero-divisor cancellation

Examples use the chain-ring filtration, e.g. products of complementary valuations can vanish.

This creates support cancellation mechanisms not present in an ordinary field.

## 9.4 Limitation

The existence of cancellation does **not** imply:

- complex amplitudes;
- Born probabilities;
- Hilbert-space geometry;
- physical wave mechanics.

The language should remain "interference analogue", "XOR cancellation", or similarly qualified.

---

# 10. ANF, Mobius transforms, and Boolean phase oracles

## 10.1 Phase-Mobius / ANF theorem

A central computational identity related:

- truth-table phase/oracle operators;
- a Boolean transform `M_n`;
- the algebraic normal form of `f`.

A representative identity was of the form

`M_n P_f M_n e_empty = e_empty + delta * ANF(f)`.

This expresses the ANF information through a Boolean phase-transform circuit.

## 10.2 Exhaustive verification

Reported checks included tens of thousands of Boolean functions and operator identities, including:

- approximately 65,812 function-level checks in one package;
- approximately 65,808 kernel identities;
- around 1,500 compiled/DAG examples.

These numbers belong to particular scripts/packages and should be cited only with the matching artifact.

## 10.3 Nilpotent interaction bound

Because a tag coefficient can satisfy `delta^2 = 0`, repeated interactions through the same nilpotent tag can collapse.

This produced an important limitation on repeated oracle interaction.

## 10.4 Workarounds

Investigated ways to preserve multiple interactions included:

- independent registers/tags;
- Boolean AND followed by re-encoding;
- literal-register models rather than overcompressed shared-module models.

---

# 11. Phase kickback and failure of the Boolean Fourier analogue

## 11.1 Phase kickback

A Boolean/shared-module phase-kickback construction was found using a phase element such as

`z = R^2 = 1 + u^2`.

A state like `(1,z)^T` can behave as an eigenvector of an exchange operator and carry phase information.

## 11.2 Kickback without a Fourier transform

A key distinction:

- phase kickback survives;
- the natural two-branch character/Fourier-like transform can be singular.

A representative transform `H_z` had Smith form equivalent to something like `diag(1,u^2)` and was not invertible.

This is an especially useful result because it separates two mechanisms that are linked in ordinary quantum algorithms.

---

# 12. Canonical LM-to-modal measurement bridge

## 12.1 What *is* canonical

The following are natural consequences of the symbolic LM framework:

- Boolean valuation;
- Boolean contraction;
- logical pairing;
- commuting symbolic/numeric evaluation;
- exact Boolean support statements after valuation.

## 12.2 What is *not* generated by bare LM valuation

Direct Boolean valuation cannot create non-Boolean chain-ring amplitudes such as

`u, u^2, u^3`.

Therefore the later modal theory requires extra structure.

## 12.3 CM coefficient vector to chain-ring element

The four CM coefficients can be linearly encoded as a chain-ring element through the basis

`1, R, R^2, R^3`

or the equivalent `u` basis.

Important qualification:

- this is basis/order dependent;
- the cyclic multiplication is added structure;
- it is not simply inherited from ordinary Boolean valuation.

## 12.4 Symbolic `A`-enrichment

A richer symbolic object such as

`Boolean formulas tensor A`

was investigated.

This permits:

- formula-valued chain-ring amplitudes;
- exact symbolic support predicates;
- later valuation into the finite chain ring.

## 12.5 "Nonzero = possible" is an extra postulate

Modal measurement uses the rule:

- zero amplitude -> impossible;
- nonzero amplitude -> possible.

This is **not** forced by the original LM semantics. It is an additional modal interpretation.

## 12.6 Effects and measurement bases

The 192 projective/reversible bases used in the chain-ring modal theory are not generated automatically by bare LMs.

They become representable only after adding the chain-ring/module structure.

## 12.7 Division-free updates

Measurement/update maps were written in a basis `B` using projectors

`J_i^B = B^{-1} P_i B`.

Properties checked included:

- idempotence;
- mutual orthogonality;
- completeness;
- repeatability;
- agreement between nonzero branch support and basis-coordinate support.

Reported exhaustive checks included:

- 192 bases;
- 384 projectors;
- 98,304/98,304 repeatability-style tests;
- hundreds of thousands of support checks in the same investigation.

## 12.8 Conditioning and process closure problems

Negative findings:

- zero divisors complicate conditioning;
- post-measurement branches can leave the chosen class of primitive/unimodular states;
- shared-module tensor constructions are not closed under all preparation/update operations;
- a fully closed process theory was not obtained.

## 12.9 Final bridge conclusion

The correct statement is roughly:

> The LM calculus provides a canonical symbolic Boolean layer and can support a precise interface to an enriched chain-ring/modal model, but the amplitudes, support semantics, effects, measurements, tensor product, and state-update rules are additional structure rather than consequences of bare Logical Matrices.

This conclusion should be preserved in any future synthesis.

---

# 13. Tensor products and the shared-module vs literal-register distinction

This distinction affected many later corrections.

## 13.1 Shared-module tensor model

One construction tensors modules over the chain ring `A`.

Consequences:

- compact algebraic description;
- zero divisors can annihilate tensor factors;
- some expected independent-register behavior is lost.

## 13.2 Literal independent-register model

A different construction expands each ring coefficient into its underlying `F_2` coordinates and treats the resulting bits/registers literally.

Consequences:

- larger state spaces;
- more general Boolean-linear filters/corrections;
- some protocols impossible in the shared model become possible.

## 13.3 Non-equivalence

The two tensor notions are mathematically different and must never be switched mid-proof.

This became one of the most important audit lessons.

## 13.4 Tensor collapse examples

Products involving different `u`-valuations can vanish in the shared-ring tensor construction.

This was used to demonstrate lack of naive tensor closure.

## 13.5 Relabeling caveat

Some apparently different shared/literal support tables were later found to be isomorphic after a transpose/relabeling on Bob's side.

This means not every observed table difference represented a genuine physical/resource distinction.

---

# 14. Contextuality over `F_2[u]/(u^4)`

## 14.1 Exhaustive resource inventory

The `2 x 2` chain-ring resource space contains 65,536 matrices, with 65,535 nonzero resources.

Resources were organized by Smith/valuation type.

## 14.2 Projective rays and bases

The modal measurement geometry included:

- 24 projective rays;
- 192 unordered projective reversible bases.

## 14.3 Smith/valuation classification

One of the strongest candidate results was a classification of support contextuality using Smith exponents/valuations.

A typical trichotomy:

- one nonzero Smith factor -> local/product-like behavior;
- multiple nonzero factors with a unique least valuation -> logically contextual but not strongly contextual;
- repeated least valuation -> strongly contextual;
- zero resource -> empty support.

## 14.4 Counts in the `u^4` ring

Reported exhaustive counts:

- 5,265 local nonzero resources;
- 34,056 logical-but-not-strong resources;
- 26,214 strongly contextual resources.

These sum to all 65,535 nonzero resources.

## 14.5 Fifteen Smith-type classes

The chain-ring resources were grouped into a finite set of canonical Smith representatives/types.

The contextuality status could be described at this invariant level rather than separately for all 65,535 states.

## 14.6 General finite-chain-ring conjecture/theorem candidate

The strongest novelty direction generalized the classification beyond this one ring.

Candidate principle:

- contextuality class is controlled by the multiplicity pattern of the least Smith valuation;
- residue-hyperplane geometry gives the support obstruction;
- a uniform Hardy-style witness can be built from the same invariant data.

This was considered more promising as original mathematics than merely reproducing Bell or teleportation analogues.

## 14.7 Uniform Hardy family

A single construction was developed/proposed to produce Hardy/logical-contextuality witnesses for broad valuation classes.

This deserves preservation as a distinct theorem candidate.

## 14.8 Same rank, different contextuality

Examples were used to show:

- binary matrix rank alone can fail to distinguish modal resource power;
- valuation/Smith data can separate resources of the same underlying binary rank.

Caveat:

- some early example choices had to be repaired after stricter preparation/unimodularity constraints were applied.

## 14.9 Restricted measurement dependence

The 192-basis classification is **model-dependent**.

Under larger unrestricted Boolean gate groups, contextuality classes can collapse or change.

Therefore the result must always name the allowed preparations, measurements, and transformations.

---

# 15. Bell-style phenomena

## 15.1 Bell-like nonseparable states

Pure Boolean/modal models support states with correlations analogous to Bell pairs, such as support on matching outcomes.

## 15.2 Possibilistic Bell contradiction

Bell-type contradictions were obtained at the level of possible/impossible outcomes.

Important:

- these are not CHSH probability violations unless a separate probability theory is added.

## 15.3 Bell behavior does not require the chain ring

A later audit found that some Bell-support contradictions already occur over plain `F_2`.

Therefore:

- Bell support is not evidence that the CM rotation ring is necessary;
- it is useful as a validation phenomenon, not necessarily as a novelty claim.

## 15.4 No support-faithful no-signalling probability completion

Some tested Boolean/modal Bell supports cannot be completed to a faithful no-signalling probability model with exactly the same support.

This is an important obstruction and should not be lost.

## 15.5 Historical signed-lift CHSH work

An earlier signed/lifted construction reproduced standard quantum quantities including `2 sqrt(2)`.

Later conclusion:

- that construction encoded known complex/signed quantum mathematics;
- it did not derive the Born rule from pure Boolean CMs;
- it should be treated as an embedding/reproduction result, not a novel pure-Boolean derivation.

---

# 16. Hardy phenomena

Topics:

- Hardy-style support contradictions;
- valuation-dependent Hardy witnesses;
- relation to unequal Smith valuations;
- uniform Hardy families over finite chain rings;
- logical contextuality distinct from strong contextuality.

This is one of the areas where the chain-ring valuation structure appears mathematically substantive rather than merely decorative.

---

# 17. GHZ phenomena

## 17.1 GHZ-like nonseparability

Multi-register pure-Boolean/modal states analogous to GHZ states were constructed.

## 17.2 Strong contextuality requires richer settings

A reported obstruction:

- two binary measurement settings are insufficient for the desired strong GHZ contextuality in the investigated framework;
- more settings/contexts are required.

## 17.3 Literal-register GHZ constructions

A larger literal Boolean register model produced explicit multi-context contradictions, including a six-context style construction in the audit notes.

## 17.4 Minimality and weighted variants

The research also considered:

- whether the context set was minimal;
- weighted or modified GHZ-style constructions.

These are useful open/detail topics even if not central to the final paper.

---

# 18. Teleportation

Teleportation is the topic with the most important correction history.

## 18.1 Early conclusion: universal teleportation seemed impossible

Restricted constructions, including a small four-outcome protocol, failed.

This led temporarily to the belief that universal exact teleportation was impossible.

**This conclusion was superseded.**

## 18.2 Corrected general Boolean-linear result

In the broader literal independent-register model:

- exact universal state transfer is possible;
- the resource must be full rank / invertible under the relevant representation;
- sufficiently general correction operations must be allowed.

## 18.3 Large-outcome protocol

A larger protocol with 64 outcomes in an 8-dimensional/literal representation was exhaustively checked.

A reported exhaustive test count was:

- 16,384 / 16,384 successful cases.

## 18.4 Resource criterion

A recurring theorem candidate:

> universal exact teleportation iff the resource matrix is invertible/full rank,

for the specified broad Boolean-linear model with complete effects/corrections.

This must not be stated without the model assumptions.

## 18.5 Singular resources

Single-copy singular resources fail to support universal teleportation in the broad audited setting.

They may still teleport restricted subspaces/quotients.

## 18.6 Example singular resource

A resource like `diag(1,u^2)` supports a nontrivial free line/quotient structure but not universal transfer.

## 18.7 Multi-copy activation

An earlier "no activation" claim was overturned.

Two copies of a rank-deficient / `(0,2)`-type resource can activate stronger transfer behavior under enlarged literal Boolean-linear filtering.

This is **model-dependent** and should be carefully separated from stricter shared-ring or unitary/orthogonal-only models.

## 18.8 Restricted models still have teleportation obstructions

Universal transfer may still fail in:

- strict CM-generated subtheories;
- shared-module tensor models;
- orthogonal/unitary-only correction models;
- overly restrictive measurement families.

Thus both statements are true in different models:
- broad Boolean-linear literal teleportation exists;
- narrower CM/modal subtheories can retain genuine no-go results.

---

# 19. Dense coding

## 19.1 Dense-coding-like protocols

Nonseparable resources were used to encode multiple distinguishable messages.

## 19.2 Resource formula

A resource-dependent message-capacity formula of the form

`N_max = d h`

was derived in the shared/modal setting, where `h` depends on the multiplicity of the least Smith valuation.

## 19.3 Separation from teleportation

A major conceptual result:

- some resources support enhanced dense coding but not universal teleportation.

Examples included valuation classes such as:

- `(0,1)`;
- `(0,2)`;
- `(1,1)`.

This shows that dense-coding power and teleportation power are not the same resource monotone in the investigated Boolean/modal theory.

---

# 20. No-cloning

A Boolean/modal no-cloning statement was investigated.

Important qualification:

- no-cloning follows under the assumed class of linear/reversible modal dynamics;
- it should not be presented as an unconstrained theorem about arbitrary Boolean operations.

The result belongs to the structure of the allowed dynamics.

---

# 21. Orthogonality, operator bases, and no-go results

## 21.1 Binary orthogonal operator-basis obstruction

A theorem candidate/no-go:

- even-dimensional binary orthogonal/unitary-like operator bases face structural obstructions.

This matters for:

- teleportation correction bases;
- dense coding;
- Pauli/error-basis analogues.

## 21.2 Symplectic / orthogonal restrictions

The research explored whether familiar stabilizer/error-basis structures survive over characteristic two with the chosen bilinear forms.

Several restrictions/no-go results emerged.

## 21.3 Restricted basis versus general linear basis

A recurring lesson:

- a protocol impossible with orthogonal/unitary corrections may become possible with general invertible Boolean-linear corrections.

This is another reason to state the gate set explicitly.

---

# 22. Stabilizer / Clifford / Pauli-like structures

Topics explored:

- native normalizer-like subgroups;
- rotation/shear/CNOT-style generators;
- Pauli-like operators;
- Clifford analogues;
- finite normalizer calculations;
- comparison with the much richer standard qubit stabilizer formalism.

## 22.1 Signed-lift result

An earlier signed/lifted CM model reproduced standard gates such as:

- `H`;
- `S`;
- `CNOT`;
- Clifford groups;
- Bell/CHSH behavior;
- Deutsch-Jozsa;
- Grover-style dynamics.

Later interpretation:

- this was an encoding of known quantum mathematics using an added signed/phase lift;
- it is not a derivation from pure Boolean CM arithmetic.

## 22.2 Intrinsic Boolean subtheory

The later focus moved to:

- the actual `F_2[C_4]` chain-ring algebra;
- intrinsic mixers;
- characteristic-two constraints;
- modal rather than probabilistic readout.

---

# 23. Boolean oracle/query algorithms

A dedicated capability audit looked at how much familiar quantum-query behavior survives.

## 23.1 Deutsch

Reported result:

- the standard one-query Deutsch advantage fails in the investigated exact Boolean setting;
- two queries are necessary in the audited model.

## 23.2 Deutsch-Jozsa

Reported negative:

- no exact one-query DJ analogue in the chosen Boolean/modal model.

## 23.3 Bernstein-Vazirani

Reported negative:

- exact recovery requires `n` queries rather than one.

## 23.4 Simon

A small-case investigation, including `n=2`, did not produce the standard Simon advantage.

The general problem was not claimed solved.

## 23.5 Grover

No genuine Grover analogue/speedup was established in the pure Boolean modal system.

Any earlier signed-lift reproduction should be kept separate.

## 23.6 UNIQUE-SAT / special oracle cases

Some restricted positive query phenomena were noted in capability audits, including special-case UNIQUE-SAT-style behavior.

These require reconstruction from the matching scripts before publication.

## 23.7 Main algorithmic lesson

Phase kickback can survive even when:

- the Fourier/character transform is singular;
- the usual quantum query advantage disappears.

This is a useful dependency result.

---

# 24. Probability and Born-rule limitations

This should appear prominently in any modal/quantum-facing paper.

## 24.1 No intrinsic Born rule

The pure Boolean/chain-ring model does not derive the Born rule.

## 24.2 Degenerate norms

Nilpotents and zero divisors make natural norm constructions degenerate.

## 24.3 Modal rather than probabilistic interpretation

The clean intrinsic semantics is:

- possible;
- impossible;

rather than a normalized probability distribution.

## 24.4 No faithful probability completion in some Bell cases

Some support tables obstruct no-signalling probability completion.

## 24.5 Signed/complex lifts are additional structure

Whenever standard quantum probabilities or `2 sqrt(2)` appear, the manuscript must say whether a signed/complex lift has been added.

---

# 25. Resource hierarchy and capability map

A broad capability/dependency investigation attempted to classify which algebraic ingredients are required for which phenomena.

Ingredients included:

- plain `F_2` linearity;
- XOR superposition;
- nonseparability;
- chain-ring phase;
- nilpotents;
- zero divisors;
- shared-ring tensors;
- literal independent registers;
- restricted measurements;
- unrestricted `GL` operations;
- orthogonal/unitary-like restrictions;
- filtering/postselection.

Capabilities included:

- interference;
- Bell support;
- Hardy;
- GHZ;
- contextuality;
- teleportation;
- dense coding;
- phase kickback;
- no-cloning;
- query-algorithm effects.

The main intellectual value is not merely that a phenomenon can be reproduced, but **which assumptions are actually necessary**.

---

# 26. Prior-art and novelty findings

## 26.1 Raw Boolean matrix logic has extensive antecedents

The following should not be claimed as wholly new without very careful qualification:

- representing truth tables as Boolean matrices;
- Boolean matrix arithmetic;
- pointwise combination of truth tables/operators;
- polarity and NPN-like actions;
- basis reconstruction;
- spectral truth operators;
- tensor/product representations;
- finite-field/modal quantum analogues.

## 26.2 Bricken

Bricken was identified as an explicit bra-ket / logical-matrix antecedent and should be discussed where the manuscript uses bra-ket logical matrices.

## 26.3 Cheng et al.

Cheng and related semi-tensor-product / matrix-product-of-logic literature provide prior art for:

- same-frame numerical truth-table/operator combination;
- matrix representations of logical networks.

A later manuscript revision explicitly re-centered novelty away from raw pointwise CM combination.

## 26.4 Mizraji / Eigenlogic / STP and related traditions

The broader prior-art search included or proposed comparison with:

- Mizraji-style matrix logic;
- Eigenlogic;
- semi-tensor-product logic/control;
- finite-field linear logic representations;
- Boolean clones/NPN classification;
- modal quantum theory.

## 26.5 CM rotation algebra is mathematically classical in isolation

The identification

`F_2[C_4] ~= F_2[u]/(u^4)`

is classical algebra.

The potentially distinctive aspect is:

- its derivation from literal CM-cell rotation;
- the way it interfaces with the CM/LM framework;
- later resource/contextuality theorems.

## 26.6 Modal Bell/GHZ/teleportation are prior-art heavy

Finite-field and modal quantum theories already contain analogues of:

- superposition;
- interference;
- entanglement/nonseparability;
- Bell phenomena;
- teleportation.

Therefore these are best used as:

- validation;
- comparison;
- capability mapping;

not as headline novelty claims by themselves.

## 26.7 Strongest novelty candidates identified

The most promising candidates included:

1. Smith/valuation-invariant classification of contextuality over finite chain rings.
2. A residue-hyperplane criterion for contextuality.
3. Uniform Hardy witnesses tied to valuation multiplicities.
4. Clean resource separation among contextuality, dense coding, and teleportation.
5. Restricted-versus-literal tensor/model separation.
6. Certain orthogonal/operator-basis obstructions in characteristic two.
7. The integrated typed LM/CM symbolic-numeric coherence architecture, though this remained more "distinctive synthesis" than independently certified new theorem.
8. Boolean degree versus reversibility for the CM-rotation lift, as a useful clean corollary/bridge even if much of the underlying algebra is classical.

---

# 27. Compiler and computational research

## 27.1 Correct positioning of CM computation

The project moved away from presenting "CM" as itself an algorithm or compiler.

Preferred architecture:

`Expression -> CM/typed operator structure -> structural reduction -> symbolic IR/DAG -> bitset/other backend -> Boolean result or optional structural output`

CM is the representation/structural layer.

## 27.2 Structural IR and DAGs

Topics:

- symbolic DAG construction;
- canonical hashing;
- structural reuse;
- common-subexpression handling;
- live-variable analysis;
- delayed materialization;
- local reduction before expansion.

## 27.3 No-reinflate execution

A major engineering theme:

- do not repeatedly materialize dense CMs after structural reductions;
- pass the reduced symbolic Boolean program to a fast backend;
- only reconstruct a dense CM if explicitly required.

## 27.4 Persistent / structural caching

Explored:

- caching compiled IR;
- compile-once/evaluate-many;
- repeated contexts or fixed variables;
- structural hashing across repeated workloads.

Measured conclusion:

- caching can help versus uncached CM execution;
- bitset/ROBDD-style competitors can still be faster overall;
- benefits plateau and depend strongly on reuse.

## 27.5 Typed operand frames

The post-split pair compiler formalized:

- row frame;
- column frame;
- variable order;
- polarity;
- output axes;
- ambient/fixed axes;
- signed transformations.

Two operators can only be fused directly after frame compatibility/alignment has been established.

## 27.6 Structural, hybrid, retabulation, and fallback paths

Compilation paths included:

- structural fusion;
- hybrid handling;
- local retabulation;
- safe fallback to ordinary evaluation.

Fallback semantics were audited carefully.

## 27.7 Pair-root versus persistent rewriting

A major implementation audit found that the actual compiler was a **partial pair-root compiler**, not a fully persistent recursive rewrite system.

In particular:

- successful child folds can be discarded if the root later falls back;
- fallback may recompile/evaluate the original root.

This implementation truth must match the manuscript and benchmark protocol.

## 27.8 Provenance classes `S/T/H`

The compiler tracked operator provenance categories such as:

- structural;
- tabulated/retabulated;
- hybrid.

Rules such as `T + T -> H` were audited.

## 27.9 Syntactic versus essential support

The current implementation uses syntactic support in key decisions rather than fully minimized/essential variable support.

This distinction matters in complexity and pairability claims.

## 27.10 Dense API axes

Even when variables become fixed, the dense API may retain ambient axes.

A cited example involved a `4 x 2` shape with eight entries despite fixed-variable structure.

## 27.11 NoPair signaling

`NoPair` is a signal that pair fusion is unavailable.

The outer wrapper then runs the ordinary path; it is not itself the entire fallback computation.

## 27.12 Cost accounting

The manuscript and benchmark design considered:

- token construction;
- alignment;
- transformation;
- fusion;
- materialization;
- discarded child work;
- fallback;
- cache effects;
- wrapper overhead;
- comparator preparation cost.

## 27.13 Prepared versus one-shot use

A key benchmarking distinction:

- prepared/reused compiled operator;
- one-shot construction plus execution.

Break-even claims depend heavily on which cost model is used.

---

# 28. Compiler benchmark results and negative findings

## 28.1 S1/S2 study

Reported scale:

- 10,500 generated formulas;
- 10,389 admitted/all-arm completions;
- zero correctness disagreements in the admitted cases.

Important finding:

- CM folding and a generic two-support optimizer matched on the symbolic metrics;
- no clear CM-specific win appeared in that comparison.

This is a valuable negative result.

## 28.2 Mechanism counters

The counters were:

- per-formula symbolic operation counts;
- summarized across strata;

not timing averages over one giant computation.

## 28.3 P14-PY0 dispatcher result

A later dispatcher/selection experiment was negative or non-decisive.

It should not be reframed as a successful performance theorem.

## 28.4 P15 semantic pass

A semantic-validation stage passed hundreds of cases, but yielded no accepted timing artifact for performance claims in the reported run.

## 28.5 Large assertion counts

One audit reported over one million assertions, including over one million scalar comparisons.

The exact number belongs to the matching release/gate artifacts.

## 28.6 Gate A: manuscript-source-protocol alignment

Before confirmatory benchmarking, the program required a gate checking that:

1. manuscript;
2. implementation;
3. frozen experimental protocol

describe the same computational object.

Audit topics included:

- pair-root vs persistent rewriting;
- provenance;
- syntactic support;
- substitutions;
- output axes;
- fallback;
- discarded work;
- caching;
- comparator equivalence;
- corpus provenance;
- estimand definition.

## 28.7 Protocol v3/v4

The confirmatory protocol evolved during auditing.

Important principle:

- do not inspect confirmatory performance results until the contract is frozen;
- fix protocol discrepancies first.

---

# 29. Comparison with other Boolean methods

Competitors and references discussed:

- flat bitsets;
- Numba/vectorized execution;
- SymPy;
- Espresso;
- BDD/ROBDD;
- CUDD;
- AIGs;
- generic common-subexpression methods;
- ANF/Mobius methods;
- semi-tensor-product formulations.

## 29.1 Important correction to early speed claims

Earlier CM materials sometimes used aggressive language about exponential or universal computational advantages.

Later benchmark work forced a more careful position:

- dense CM materialization can be expensive;
- bitsets are often the strongest flat execution kernel;
- ROBDD/CUDD can dominate symbolic cases;
- the value of CM is more plausibly structural decomposition, typed operator reuse, quotienting, conditioning, and pre-expansion fusion than universal raw speed.

---

# 30. Quotienting experiments

A computational line tested quotient-like operator differences.

Topics/results:

- directional feature subtraction;
- containment;
- overlap/Jaccard-style relationships;
- exhaustive small tables;
- related/equivalent cases;
- aligned basis/order requirements.

Conclusion:

- quotienting is a distinct CM/operator artifact;
- it was not demonstrated to be a semantic-delta speed advantage over bitsets;
- higher-dimensional claims require explicit alignment conventions.

---

# 31. Paper architecture and research-program splitting

The research repeatedly had to be split to avoid one manuscript containing too many unrelated contributions.

## 31.1 Foundations paper

**Correspondence and Logical Matrices: A Boolean Operator Calculus**

Natural home for:

- compact CMs;
- formula-valued LMs;
- valuation;
- pairing;
- frame transport;
- operator-on-operator Boolean closure;
- higher arity;
- coherence;
- selected spectral facts.

## 31.2 Computational/compiler paper

**Operator-Level Boolean Computation with Correspondence Matrices**

Natural home for:

- typed operator frames;
- signed normalization;
- pair fusion;
- compiler paths;
- fallback;
- cost model;
- benchmarks;
- implementation contract;
- empirical limitations.

## 31.3 Phase/modal/resource paper

A separate paper/program was proposed for:

- CM-cell rotation;
- `F_2[C_4]`;
- chain-ring structure;
- interference;
- modal measurement;
- contextuality;
- tensor distinctions;
- teleportation/dense coding resource theory.

## 31.4 Canonical bridge paper/report

A separate focused investigation is appropriate for:

- LM -> CM valuation;
- symbolic enrichment;
- support semantics;
- effects;
- measurement/update;
- exactly which structures are canonical and which are postulated.

## 31.5 Query-obstruction paper

The negative query-complexity results may be coherent enough for a separate technical note/paper:

- Deutsch;
- DJ;
- BV;
- Simon small cases;
- Fourier singularity;
- kickback without quantum speedup.

## 31.6 "Boolean Modal Laboratory for Quantum Information"

A broader synthesis was proposed as a community-facing paper/report organizing:

- capabilities;
- dependencies;
- resource hierarchies;
- successes;
- failures;
- prior art;
- reproducibility.

---

# 32. Verification and reproducibility artifacts

Across the threads, many types of artifacts were produced or proposed:

- LaTeX manuscripts;
- PDFs;
- verification Python scripts;
- raw CSV/JSON outputs;
- exhaustive tables;
- benchmark protocols;
- response-to-review documents;
- panel audits;
- novelty audits;
- Astra Pro prompts;
- handoff ZIP archives;
- manifests and integrity checks.

## 32.1 Foundations verification

Reported scopes included:

- unary/binary/ternary valuation and pairing;
- all 16 binary rotations;
- block-lift examples;
- tens of thousands of coherence cases;
- one large audit with approximately 1.5 million assertions.

## 32.2 Modal/resource verification

Reported scopes included:

- all 65,536 `2 x 2` chain-ring resource matrices;
- 192 bases;
- hundreds of projectors;
- contextuality classification of all nonzero resources;
- Bell/GHZ support checks;
- teleportation decoders;
- dense-coding encoders;
- multiple named audit suites.

## 32.3 Astra handoff package

One major handoff ZIP reportedly contained:

- deep prompt;
- formal theorem candidates;
- corrected audit state;
- Paper-B exclusion boundary;
- paper architecture;
- prior-art seeds;
- novelty/claim CSV;
- reproducibility code/tests/results;
- historical packages;
- manifest/integrity verification.

The package contained on the order of 181 files.

---

# 33. Historical / exploratory topics to preserve but label carefully

These are easy to lose because later research became more formal.

## 33.1 Logical imaginary unit

An early idea proposed a special logical transformation analogous to `i`, intended to add a second logical-state layer and support phase/rotation-like behavior.

Later pure-Boolean phase work found a more concrete route through the four-cycle ring, so the "logical imaginary unit" idea should be preserved historically but not confused with the later chain-ring construction.

## 33.2 Hermiticity

Questions explored:

- what Hermitian matrices provide;
- real eigenvalues;
- orthogonal eigenvectors for distinct eigenvalues;
- unitary diagonalization;
- relation to physical observables.

Correction emphasized:

- commutation does not require Hermiticity.

## 33.3 Commutators and a logical Lie algebra

Exploratory idea:

- use matrix commutators to study closure and algebraic relations among logical operators.

This was not the main later path but remains a potentially interesting algebraic direction.

## 33.4 Simultaneous diagonalization

Correction:

- commuting matrices do not automatically become diagonal;
- suitable commuting diagonalizable families may share an eigenbasis.

## 33.5 Complex-valued fuzzy truth

Explored interpretation:

- modulus inside the unit disk as degree/certainty;
- phase as a separate truth/fuzziness mode.

This belongs to a different enriched logic direction than the later pure-Boolean chain-ring model.

## 33.6 Bectors and B-modules

Historical constructs:

- Boolean-ring state vectors;
- module-theoretic logical states;
- possible bridge to algebraic geometry/module theory;
- building blocks for CM construction.

## 33.7 Evolutionary / time-dependent Logical Matrices

Exploratory topics:

- logistic/activation functions evolving proposition values;
- Heaviside binarization;
- LM-to-CM time evolution;
- coupled/entangled LMs;
- ambiguity at the threshold.

This line is conceptually separate from the later static Boolean operator papers.

## 33.8 Cognitive / Matte-Blanco motivation

Earlier CM research was related to:

- symmetry/asymmetry in conscious versus unconscious logic;
- Matte-Blanco;
- p-adic/ultrametric precedents;
- measurement/symmetry-breaking analogies;
- self-awareness/self-reference motivations.

These are motivation/application topics, not mathematical evidence for the later modal quantum results.

---

# 34. Corrections and superseded conclusions register

This section should be treated as a "do not regress" checklist.

## 34.1 Universal teleportation

**Superseded:** "Universal Boolean teleportation is impossible."

**Current audited position:** It is possible in a broad literal independent-register Boolean-linear model with full-rank/invertible resources and sufficiently general corrections. Narrower CM/shared/orthogonal models can still have genuine obstructions.

## 34.2 Four-outcome teleportation

**Failed:** a small four-outcome construction.

**Replacement:** a larger complete protocol, including a 64-outcome construction in the audited literal model.

## 34.3 No multi-copy activation

**Superseded:** singular resources never activate.

**Current position:** multi-copy activation can occur under enlarged literal Boolean-linear filtering.

## 34.4 Shared tensor = literal tensor

**False / unsafe.**

The shared `A`-module tensor and literal `F_2` register tensor must be kept separate.

## 34.5 Contextuality as gate-invariant absolute property

**Too strong.**

The 192-basis contextuality classification depends on the allowed measurement/gate model and may collapse under broader transformations.

## 34.6 Bell = CHSH probability violation

**Incorrect without added probability theory.**

Pure Boolean/modal Bell results are support/possibility statements.

## 34.7 Born rule from CM phase algebra

**Not obtained.**

The intrinsic norm is degenerate; no Born-rule derivation exists.

## 34.8 LM valuation automatically yields chain-ring amplitudes

**False.**

The chain-ring enrichment is additional structure.

## 34.9 Nonzero = possible follows from LM semantics

**False.**

It is a modal postulate/interface rule.

## 34.10 CM pointwise superposition as uniquely novel

**Too strong.**

Same-frame numerical truth-table combination has prior art. The more defensible distinction is the integrated LM/valuation/pairing/frame architecture.

## 34.11 CM as "the compiler"

**Corrected.**

CM is better described as a structural representation/operator layer used by compiler-style algorithms.

## 34.12 Universal raw speed advantage

**Not supported.**

Bitsets, ROBDD/CUDD, and generic optimizers can outperform CM pipelines. CM's plausible advantage is structural/pre-expansion/reuse-oriented and workload dependent.

## 34.13 Polarity-mask formula

**Concrete bug fixed.**

The earlier printed mask convention failed exhaustive cases and must remain corrected.

## 34.14 Signed-lift quantum results as intrinsic Boolean results

**Corrected.**

The signed/complex-like lift reproduces known quantum mathematics but is additional structure, not an intrinsic pure-Boolean derivation.

---

# 35. Negative results and obstructions worth preserving

These are scientifically valuable and should not be lost simply because they are negative.

- No intrinsic Born rule from the chain-ring norm.
- Some Bell supports have no faithful no-signalling probability completion.
- Shared-module tensor/state classes are not closed under all conditioning/update operations.
- Natural Boolean Fourier/character transforms can be singular.
- Phase kickback can exist without an invertible analyzer.
- Standard one-query Deutsch advantage fails in the audited model.
- Exact one-query Deutsch-Jozsa fails.
- Bernstein-Vazirani loses the one-query advantage.
- Simon small cases did not yield the standard speedup.
- No pure Boolean Grover advantage was established.
- Strict orthogonal/unitary operator-basis requirements create characteristic-two obstructions.
- Singular single-copy resources do not universally teleport.
- Two binary settings are insufficient for the targeted strong GHZ contextuality.
- Dense CM materialization is not generally competitive with flat bitsets.
- A generic support-aware optimizer matched CM folding in the S1/S2 symbolic metrics.
- P14-PY0 did not establish a useful dispatcher win.
- Quotienting did not establish a semantic-delta speed advantage.
- A fully closed chain-ring modal process theory remains unresolved.

---

# 36. Open questions and research directions

## 36.1 General finite-chain-ring contextuality theorem

Can the Smith/valuation criterion be proved cleanly for a broad class of finite commutative chain rings?

Subquestions:

- exact hypotheses;
- residue-field dependence;
- arbitrary local dimension;
- number of parties;
- allowed measurement bases.

## 36.2 Uniform Hardy witness theorem

Can the proposed uniform construction be made fully general and minimal?

## 36.3 Resource monotones

Can contextuality, dense-coding capacity, teleportation capability, and activation be organized by monotones based on:

- Smith rank;
- valuation multiplicity;
- free rank;
- annihilator depth;
- orbit size?

## 36.4 Multi-copy activation hierarchy

Questions:

- minimum copy number by Smith type;
- restrictions under unitary/orthogonal-only filters;
- whether activation survives in stricter CM-generated subtheories.

## 36.5 Closed process theory

Can one choose an enlarged state/process category that is closed under:

- tensor product;
- measurement;
- conditioning;
- composition;

without losing the desired CM/LM connection?

## 36.6 Canonicality of the modal bridge

Can the chain-ring/modal enrichment be characterized by a universal property, rather than simply chosen?

## 36.7 Higher-arity CM rotation algebra

How does the binary `C_4` rotation structure generalize to:

- larger truth tensors;
- Reed-Muller structure;
- permutation groups of cells;
- multi-variable degree filtrations?

## 36.8 Spectral/semigroup paper on the 16 compact CMs

Potential self-contained topic:

- full semigroup;
- Green relations;
- similarity;
- orbit structure;
- functional graphs;
- minimal polynomials;
- Boolean-function class relations;
- frame invariants.

## 36.9 Restricted stabilizer-like subtheory

Can a natural CM-derived gate set support a useful normal form, Gottesman-Knill-type simulation statement, or exact classification?

## 36.10 Query-complexity theorem paper

Can the observed Deutsch/DJ/BV limitations be proved in a unified algebraic framework?

## 36.11 Compiler confirmatory benchmark

Still requires a frozen protocol where manuscript, source, and estimand are exactly aligned.

## 36.12 Compiler structural advantage

Find workloads where typed pre-expansion fusion, quotienting, conditioning, or reuse gives a clear advantage over strong generic competitors.

---

# 37. Easy-to-miss topics checklist

The following items are especially likely to disappear when the work is divided into papers.

- [ ] LM is symbolic/formula-valued; CM is its evaluated numeric shadow.
- [ ] Canonical term-lift definition.
- [ ] Logical pairing / agreement-bit semantics.
- [ ] Valuation-pairing coherence.
- [ ] Signed-frame and polarity transport.
- [ ] Corrected polarity-mask convention.
- [ ] Arbitrary-arity tensors/flattenings/block lifts.
- [ ] Distinction between XOR-AND contraction and pointwise Boolean operator superposition.
- [ ] Cheng et al. prior art for raw numerical same-frame combination.
- [ ] Bricken bra-ket/logical-matrix prior art.
- [ ] Spectral classification of the 16 compact CMs.
- [ ] `GL_2(F_2) ~= S_3` structure of the six invertible CMs.
- [ ] Rank-one/separability criterion.
- [ ] Valuation spectra / affine-function characterization.
- [ ] Literal four-cycle CM rotation `R`.
- [ ] Centralizer = 16 circulant operators.
- [ ] `F_2[C_4] ~= F_2[u]/(u^4)`.
- [ ] Nilpotent filtration and rank sequence.
- [ ] Boolean degree <-> lifted reversibility.
- [ ] Operand reversal <-> `R^{-1}`.
- [ ] Complement <-> deepest nilpotent layer.
- [ ] Degenerate norm -> no Born rule.
- [ ] Mixer/splitter is distinct from the rotation operator.
- [ ] XOR cancellation as the intrinsic interference analogue.
- [ ] Phase-Mobius / ANF bridge.
- [ ] Nilpotent repeated-interaction limitation.
- [ ] Phase kickback survives while the natural Fourier transform can be singular.
- [ ] Bare LM valuation cannot create chain-ring amplitudes.
- [ ] "Nonzero = possible" is extra modal semantics.
- [ ] 24 rays / 192 reversible projective bases.
- [ ] Division-free projectors and repeatability checks.
- [ ] Conditioning/tensor non-closure.
- [ ] Shared-module tensor != literal independent-register tensor.
- [ ] Smith/valuation contextuality classification.
- [ ] 5,265 local / 34,056 logical / 26,214 strong resource counts.
- [ ] Uniform Hardy witness direction.
- [ ] Same binary rank can hide different restricted resource power.
- [ ] Bell support contradictions do not require CM rotation.
- [ ] Bell support != CHSH probability violation.
- [ ] No-support-faithful no-signalling completion for some tables.
- [ ] GHZ strong-contextuality setting obstruction.
- [ ] Earlier "teleportation impossible" conclusion is superseded.
- [ ] Broad Boolean-linear teleportation iff invertible/full-rank resource, with model qualifications.
- [ ] Failed four-outcome protocol versus successful larger/64-outcome protocol.
- [ ] Multi-copy activation of singular resources under broader literal filtering.
- [ ] Dense coding and teleportation are distinct resource capabilities.
- [ ] Dense-coding `d h` style capacity result.
- [ ] No-cloning is conditional on the allowed linear/modal dynamics.
- [ ] Orthogonal/unitary operator-basis obstruction in characteristic two.
- [ ] Restricted stabilizer/normalizer questions.
- [ ] Signed-lift quantum reproductions are additional structure / prior-art heavy.
- [ ] Deutsch/DJ/BV negative query results.
- [ ] Simon small-case negative and Grover unresolved.
- [ ] CM is structural representation/IR, not "the compiler".
- [ ] No-reinflate architecture.
- [ ] Persistent structural cache / compile-once-evaluate-many.
- [ ] Pair-root implementation versus persistent rewriting.
- [ ] S/T/H provenance.
- [ ] Syntactic versus essential support.
- [ ] Fallback semantics and discarded child work.
- [ ] S1/S2 negative result: generic optimizer matched CM symbolic metrics.
- [ ] P14-PY0 negative/non-decisive result.
- [ ] Quotienting is structurally meaningful but not a demonstrated speed advantage.
- [ ] Gate A manuscript-source-protocol alignment.
- [ ] Strong competitors: bitset, CUDD/ROBDD, AIG, SymPy, Espresso, Numba.
- [ ] Historical logical imaginary unit idea.
- [ ] Hermiticity/commutator/simultaneous-diagonalization explorations.
- [ ] Complex-valued fuzzy truth direction.
- [ ] Bectors/B-modules.
- [ ] Evolutionary/time-dependent LMs.
- [ ] Matte-Blanco / cognitive motivation, clearly separated from mathematical claims.

---

# 38. Recommended "research register" structure going forward

To make sure nothing explored is lost, maintain one master register with one row per result/topic and at least these fields:

| Field | Purpose |
|---|---|
| Topic ID | Stable identifier |
| Topic/result | Short name |
| Mathematical setting | `F_2`, `F_2[C_4]`, chain ring, literal registers, compiler, etc. |
| Status | Established / candidate / corrected / negative / open / historical |
| Assumptions | Gate set, tensor model, measurement set, frame conventions |
| Main statement | Exact current claim |
| Supersedes | Earlier result if corrected |
| Proof/check artifact | Script, theorem proof, notebook, CSV |
| Test scope | Exhaustive range / random range / theorem only |
| Prior art | Main antecedents |
| Novelty status | Standard / synthesis / plausible new / unverified |
| Paper home | Foundations / compiler / modal-resource / query / appendix |
| Cross-links | Related topics |
| Next action | Proof, literature search, benchmark, exposition, etc. |

---

# 39. Suggested paper-home map

## Foundations / Boolean operator calculus

Include:

- 16 compact CMs;
- basis conventions;
- formula-valued LMs;
- canonical term lift;
- valuation;
- logical pairing;
- frame actions;
- operator-on-operator Boolean closure;
- coherence;
- higher arity;
- selected spectral classification;
- carefully scoped ANF bridge.

Avoid overloading with:

- full chain-ring modal resource theory;
- teleportation;
- contextuality classification;
- compiler benchmarks.

## Compiler paper

Include:

- typed CM tokens;
- signed frames;
- normalization;
- fusion rules;
- retabulation/hybrid/fallback;
- actual pair-root implementation semantics;
- correctness;
- cost model;
- frozen empirical protocol;
- honest negative benchmark results.

## Phase / modal resource paper

Include:

- CM-cell rotation;
- chain-ring derivation;
- nilpotent filtration;
- interference;
- projective bases;
- Smith resource theory;
- contextuality/Hardy;
- dense coding;
- teleportation model distinction;
- activation;
- probability limitations.

## LM-to-modal bridge note

Include:

- canonical Boolean valuation;
- symbolic enrichment;
- what extra scalar structure is required;
- support semantics;
- effects;
- projectors;
- conditioning;
- process-closure obstruction.

## Query / algorithm note

Include:

- phase kickback;
- singular Fourier transform;
- Deutsch;
- Deutsch-Jozsa;
- Bernstein-Vazirani;
- Simon small cases;
- Grover non-result;
- dependency theorem if a unified proof is found.

## Historical / conceptual appendix or separate essay

Include only if useful:

- logical imaginary unit;
- Hermiticity/Lie-algebra exploration;
- complex fuzzy truth;
- Bectors;
- evolutionary LMs;
- cognitive/Matte-Blanco motivation.

---

# 40. Bottom-line coverage assessment

The explored research program is substantially broader than any single manuscript. The main bodies of work are:

1. **CM/LM foundations and coherence**;
2. **spectral/dynamical structure of the 16 compact CMs**;
3. **compiler/structural computation**;
4. **CM-cell rotation and finite chain-ring phase algebra**;
5. **modal measurement and the LM-to-modal bridge**;
6. **contextuality/Hardy/resource classification**;
7. **Bell/GHZ/nonseparability**;
8. **teleportation/dense coding/no-cloning**;
9. **tensor-model and process-theory distinctions**;
10. **phase kickback and Boolean query complexity**;
11. **orthogonal/stabilizer/operator-basis obstructions**;
12. **historical quantum/fuzzy/cognitive explorations**;
13. **prior-art/novelty auditing**;
14. **verification, reproducibility, and manuscript architecture**.

The most dangerous omissions would be the **correction history** rather than the headline topics. In particular, any future synthesis should explicitly preserve:

- the corrected teleportation result;
- the shared-vs-literal tensor distinction;
- the model dependence of contextuality;
- the absence of an intrinsic Born rule;
- the non-canonical status of chain-ring amplitudes and modal measurement relative to bare LMs;
- the prior art for raw pointwise CM combination;
- the compiler's actual pair-root/fallback behavior;
- the negative query and benchmark results.

Those items determine the correct boundaries of the research as much as the positive constructions do.
