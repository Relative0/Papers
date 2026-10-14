# Novelty and positioning report
## Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation

**Date:** 27 September 2026  
**Purpose:** Narrow the contribution to what the available evidence supports, identify the closest antecedents, and specify publication-safe novelty language.

## Executive conclusion

The paper should **not** claim novelty for any of the following broad ideas:

- modal quantum theory or finite-field amplitudes;
- exact distinguishability via linear independence/direct-sum structure;
- polynomial/degree-per-query lower bounds;
- oracle-identification dimension bounds;
- the fact that query complexity depends on the oracle/access interface;
- the qualitative failure of the standard Deutsch advantage over characteristic two;
- one-query modal UNIQUE-SAT;
- the ordinary complex-amplitude Bernstein--Vazirani algorithm.

The strongest differentiated theorem is narrower:

> **Characteristic-two exact BV theorem.** For any field of characteristic two, any finite adaptive algorithm satisfying the paper's complete recorded modal-readout contract, with arbitrary finite ancillas and pointwise invertible oracle actions fixed independently of the secret at each recorded query node, requires at least `n` queries to recover every `n`-bit Bernstein--Vazirani secret. Standard QXOR attains the bound with `n` queries.

After targeted searches and direct comparison with the closest sources listed below, I did **not** locate a prior theorem with this full combination of scalar domain, access class, finite adaptivity, complete modal readout, arbitrary finite ancillas, and exact `n`-query conclusion. That supports describing the theorem as a **differentiated exact specialization**. It does **not** prove historical firstness. The revised manuscript therefore uses “to our knowledge, a targeted comparison has not located...” rather than “first” or “novel.”

The one-query characteristic-two Deutsch--Jozsa obstruction also appears differentiated in the same targeted search, but its priority is less important to the paper and remains less certain. It should remain a secondary result.

## Claim-by-claim novelty classification

| Claim | Publication-safe classification | Why |
|---|---|---|
| Modal linear computation over characteristic-two fields | **Known background** | Schumacher--Westmoreland establish modal quantum theory over general fields. |
| Complete instrument / trivial common-kernel requirement | **Known antecedent** | `Almost quantum theory` gives the unconditional-operation common-kernel condition. |
| Exact modal discrimination from linear independence/direct sums | **Known principle / elementary label-span extension** | Diamond--Schumacher explicitly discuss distinguishability of linearly independent modal states. |
| Degree grows by at most one per oracle query | **Known architecture, specialized implementation** | Beals et al. establish the polynomial method; Farhi et al. give a closely related function-identification dimension bound. The paper's new work is the characteristic-two secret-bit specialization and recorded adaptive modal implementation, not the general technique. |
| Query complexity depends on oracle access | **Known** | Karl Svozil's 2026 preprint explicitly frames exact query complexity by answer partition plus oracle access and proves response-unitary dependence for Deutsch in the ordinary complex-unitary model. |
| Qualitative failure of the usual Deutsch speedup over `F_2` | **Known** | James--Ortiz--Sabry state the qualitative failure. |
| Exact Deutsch lower bound under the paper's full pointwise/adaptive modal contract | **Rigorous contract-level refinement** | Stronger quantified statement than circuit failure, but should not be the headline novelty. |
| One-query DJ obstruction under the same characteristic-two contract | **Apparently differentiated; priority not certified** | No equivalent theorem located in targeted search; only the one-query obstruction is proved. |
| Exact BV lower bound `q >= n` under finite adaptive complete modal readout, arbitrary finite ancillas, broader pointwise lower-bound interface | **Strongest apparently differentiated theorem** | Closest polynomial/oracle-identification antecedents use standard complex amplitudes and different variables/readout. No matching characteristic-two theorem located. |
| QXOR upper bound `n` for BV | **Elementary matching upper bound** | Querying unit vectors is straightforward; significance comes from matching the lower bound. |
| Ring-valued kickback with singular analyzer and rank `4+2n` | **Model-specific algebraic boundary / illustrative result** | Correct and useful, but elementary relative to the main exact-query theorem; not the paper's central novelty. |
| Modal UNIQUE-SAT positive control | **Known reproduced result** | Willcock--Sabry. |
| Small Simon scan / description-readout ablation | **Finite evidence only** | No general theorem or novelty claim should be attached. |

## Closest prior art and exact overlap

### 1. Beals et al. (2001) - polynomial method

**Source:** Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca, Ronald de Wolf, *Quantum Lower Bounds by Polynomials*, JACM 48(4), 778--797. DOI: https://doi.org/10.1145/502090.502097  
Preprint: https://arxiv.org/abs/quant-ph/9802049

**Overlap:** Query amplitudes can be represented by low-degree polynomials in oracle variables, with degree increasing in a controlled way per query.

**Difference:** Their setting is ordinary complex-amplitude quantum computation and standard black-box variables. P02 uses characteristic-two amplitudes, exact all-branches modal readout, and the BV promise to express each pointwise oracle call as affine degree one in the `n` secret bits themselves.

**Effect on novelty:** Do not claim a new polynomial method. Claim the characteristic-two specialization and adaptive modal theorem.

### 2. Farhi, Goldstone, Gutmann, Sipser (1999) - function-identification dimension bound

**Source:** *Bound on the number of functions that can be distinguished with k quantum queries*, Physical Review A 60, 4331--4333. DOI: https://doi.org/10.1103/PhysRevA.60.4331  
Preprint: https://arxiv.org/abs/quant-ph/9901012

**Overlap:** If a standard complex quantum algorithm distinguishes a family of Boolean functions with `k` queries, the number distinguishable is bounded by a binomial sum. This is structurally very close to P02's coefficient-span count.

**Difference:** Farhi et al. parameterize polynomials by the truth-table entries over an address set of size `N`. For BV, that bound does not rule out the standard one-query quantum algorithm. P02 exploits the characteristic-two identity `f_s(x)=sum_j s_j x_j` inside the amplitude field, collapsing the oracle dependence to only `n` secret variables and producing `sum_{j<=q} C(n,j)`.

**Effect on novelty:** This source should be cited prominently as a closest methodological antecedent. The revised paper now does so.

### 3. Combarro et al. (2021) - exact one-query promise problems

**Source:** Elías F. Combarro et al., *On a poset of quantum exact promise problems*, Quantum Information Processing 20, 214 (2021). DOI: https://doi.org/10.1007/s11128-021-03156-3

**Overlap:** Standard complex exact one-query promise problems include Deutsch--Jozsa and Bernstein--Vazirani and are studied in a common framework.

**Difference:** Ordinary Hilbert-space amplitudes and measurement; their one-query BV result is the familiar complex-amplitude result, not a characteristic-two modal theorem.

### 4. Copeland and Pommersheim (2021) - oracle identification

**Source:** Daniel Copeland and Jamie Pommersheim, *Quantum query complexity of symmetric oracle problems*, Quantum 5, 403 (2021). DOI: https://doi.org/10.22331/q-2021-03-07-403

**Overlap:** General exact/probabilistic oracle-identification questions and group-character methods.

**Difference:** Complex unitary oracle groups and character theory; not the characteristic-two complete-modal-readout contract.

### 5. Montanaro (2012) - finite-field-valued functions

**Source:** Ashley Montanaro, *The quantum query complexity of learning multilinear polynomials*, Information Processing Letters 112(11), 438--442 (2012). DOI: https://doi.org/10.1016/j.ipl.2012.03.002

**Overlap:** Exact quantum learning of unknown polynomials over finite fields, including `q=2` Reed--Muller structure.

**Difference:** The unknown function's algebra is over a finite field, but the quantum amplitudes and measurement theory remain ordinary complex quantum mechanics. This is not a finite-field-amplitude/modal result.

### 6. Svozil (2026) - access-model dependence

**Source:** Karl Svozil, *Answer Partitions and Oracle Access Determine Quantum Query Complexity*, arXiv:2605.12675v4. https://arxiv.org/abs/2605.12675

**Overlap:** Very important contemporary antecedent. It explicitly says that an answer partition does not determine exact query complexity without its access model. For Deutsch, a controlled response unitary admits a one-query exact solution iff the response unitary has the needed `-1` eigenvalue; alternative response dimensions can raise the exact cost.

**Difference:** Ordinary complex-unitary quantum theory, Hilbert-space block discrimination, and response-unitary spectra. It does not supply the characteristic-two adaptive BV theorem or the modal complete-instrument proof.

**Effect on novelty:** The broad “oracle choice matters” rhetoric is no longer defensible as a contribution. The revised manuscript explicitly treats it as background and cites Svozil.

### 7. Modal antecedents

- Benjamin Schumacher and Michael Westmoreland, *Modal Quantum Theory*, Foundations of Physics 42 (2012), 918--925. https://doi.org/10.1007/s10701-012-9650-z
- Benjamin Schumacher and Michael Westmoreland, *Almost quantum theory*. https://arxiv.org/abs/1204.0701
- Roshan P. James, Gerardo Ortiz, Amr Sabry, *Quantum Computing over Finite Fields: Reversible Relational Programming with Exclusive Disjunctions*. https://arxiv.org/abs/1101.3764
- Jeremiah Willcock and Amr Sabry, *Solving UNIQUE-SAT in a Modal Quantum Theory*. https://arxiv.org/abs/1102.3587
- Phillip Diamond and Benjamin Schumacher, *Cloning, deleting, and hiding in modal quantum theory*. https://arxiv.org/abs/2310.04397

These sources delimit the model background, qualitative Deutsch antecedent, positive modal algorithm, and distinguishability principle. None was found to contain the fully quantified P02 BV theorem.

## Searches performed

Targeted searches included combinations and synonyms of:

- `Bernstein-Vazirani modal quantum theory`
- `Bernstein Vazirani characteristic two amplitudes query`
- `Bernstein-Vazirani finite-field quantum computing`
- `adaptive Bernstein-Vazirani query lower bound modal`
- `Deutsch-Jozsa characteristic-two modal quantum`
- `finite field quantum amplitudes Bernstein Vazirani query complexity`
- `exact oracle identification polynomial dimension query`
- `answer partitions oracle access query complexity`
- citation chaining from Beals, Farhi, Combarro, Copeland--Pommersheim, Montanaro, Schumacher--Westmoreland, James--Ortiz--Sabry, and Svozil.

No search result by itself proves absence. The correct conclusion remains “no equivalent theorem located in the targeted search,” not “the theorem is the first.”

## Recommended novelty wording

### Safe abstract/introduction wording

> The general polynomial method and the dependence of exact query complexity on oracle access have substantial prior antecedents. The contribution here is narrower: an exact characteristic-two Bernstein--Vazirani lower bound that remains valid for arbitrary finite ancillas and finite adaptive complete recorded modal readout under the stated pointwise access contract.

### Safe priority wording

> To our knowledge, a targeted comparison with the closest modal, polynomial-method, and exact oracle-identification literature has not located a prior theorem with this full combination of scalar domain, access class, adaptivity/readout model, and exact conclusion. We do not claim historical firstness.

### Wording to avoid

- “first proof that oracle choice matters”
- “new polynomial method”
- “first finite-field Bernstein--Vazirani result” without qualification
- “Deutsch fails in characteristic two” as a new observation
- “Deutsch--Jozsa exact complexity is 2” (not proved)
- any claim that the finite Simon scan establishes a general lower bound

## Publication positioning

The paper is strongest as a **focused exact-query technical note/research article** centered on Theorem 3.2 in the revised manuscript. The revised title and abstract now make BV the headline, move Deutsch/DJ to related obstructions, place the ring calculation in an appendix, and make the novelty boundary explicit.
