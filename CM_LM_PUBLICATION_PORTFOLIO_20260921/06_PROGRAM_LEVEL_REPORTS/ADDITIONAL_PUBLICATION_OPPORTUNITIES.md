# Additional CM/LM publication opportunities

**Audit date:** 20 September 2026  
**Scope:** material in `CM_Correctness_Audit_Standalone.tex`, the three-paper portfolio, the canonical adversarial review, and the current research-gap ledger.

## Decision

The three manuscripts cover the strongest claims that are ready to carry a research paper now:

- **Paper B:** typed CM/LM Boolean computation, valuation, compiler behavior, and bounded empirical evidence.
- **P01:** chain-ring contextuality, fixed-orbit coding, tensor boundaries, and universal raw-transfer criteria.
- **P02:** exact characteristic-two query obstructions and the kickback/Fourier boundary.

The correctness audit is not redundant. It should be retained as a **reproducible technical companion** because it contains explicit constructions, finite classifications, negative results, and model-boundary evidence that the papers properly omit. However, the uncaptured results do not presently form a defensible fourth research paper merely by collecting them. Many are classical algebra, established modal-quantum phenomena, direct rank consequences, or examples of the general theorems already in P01.

The next full paper should be created only by solving one of the open organizing problems below.

## Publication map

| Priority | Proposed output | Present status | What would make it publishable |
|---|---|---|---|
| 1 | **Closed process semantics for chain-ring modal models** | Best new-paper program; not yet solved | Specify preparation, tensor, effects, conditioning, and composition so the state class is closed. Reprove the resource results inside that contract and compare it functorially with the literal finite-field model. |
| 2 | **Restricted-operation resource theory** | Strong related program; may merge with priority 1 | Characterize the normalizer of the rotation-compatible measurement family inside the full binary linear group; prove conversion monotones and activation/distillation criteria under the restricted operations. |
| 3 | **Multipartite contextuality in the literal CM-derived model** | Viable short-note seed | Generalize the audited GHZ table beyond one state and one 27-context family: classify a state family, arbitrary party number, or a declared measurement family. Establish analytical minimality rather than only finite-case minimality. |
| 4 | **Support-realizability classification** | Viable theorem seed | Replace the single Bell-table probability obstruction with a characterization of which CM-induced support models admit support-faithful no-signalling probability completions. |
| 5 | **Higher-arity rotation/augmentation models** | Speculative | Obtain a result beyond the known circulant, group-algebra, Reed–Muller, and parity facts—for example a contextuality classification in multivariable augmentation algebras or a useful synthesis theorem. |
| 6 | **Machine-checked CM/chain-ring foundations** | Optional verification or artifact paper | Formalize the residue-hyperplane lemma, Smith trichotomy, tensor counterexample, and raw-transfer criterion in Lean, Isabelle, or Coq, with the executable finite evidence as regression tests. |
| 7 | **Compiler performance follow-up** | Belongs with Paper B, not the modal papers | Execute the frozen P15-style corpus/comparator/environment protocol against matched baselines and report full conversion, compilation, memory, and output costs. |

Priorities 1 and 2 should be treated as one program until there are enough independent theorems to justify two papers.

## Material that should be preserved, with its proper role

| Audit material | Preserve as | Reason |
|---|---|---|
| Four-cycle rotation, exact 16-element centralizer, corrected nilpotent, and `F_2[u]/(u^4)` identification | Companion background / derivation | The CM-to-ring route is useful and distinctive as exposition, but cyclic centralizers and circulant polynomial algebras are classical. |
| Shear and `H_rot` interference circuits; 12-of-15 splitting count | Worked examples / teaching article | They make XOR cancellation and access assumptions concrete. The block identities and finite-field interference are not strong standalone novelty. |
| Shared separability count, stabilizers, and basis-permutation entanglers | Reproducibility supplement | Useful finite inventory; currently a case study rather than a general theorem story. |
| Rank-2 phase-anchored state versus rank-8 universal resource | Main boundary example in a future process/resource paper | It clearly demonstrates that the literal theory changes both tensor structure and resource content. |
| Three-setting Bell table and 64-assignment certificate | Companion example | The contextuality framework and the general chain-ring result already have homes; the explicit table is still useful for readers and testing. |
| Literal `GHZ_8`, six-context contradiction, and weighted variant | Seed for priority 3 | The present minimality is only within one declared 27-context family. A family theorem is still needed. |
| Explicit 64-outcome analyzer, `P,T` synthesis, and failure of the old four-outcome analyzer | Companion construction / future resource-paper example | P01 contains the general existence and rank results. The explicit circuit remains valuable implementation evidence. |
| Shared and literal exact-subspace hierarchies | Future process/resource paper | These make the consequences of tensor and operation choices visible, but must be stated under a closed operational contract. |
| Literal multi-copy rank activation | Appendix/example | Under unrestricted field-linear filters it is a direct consequence of Kronecker-rank multiplication and normal form; it is not a headline novelty claim. Restricted-operation activation could become new work. |
| Orthogonal-correction and bilinear-form obstructions | Design constraint / appendix | The supplied even-dimensional bound is weaker than known span facts for binary orthogonal matrices. It usefully rules out one repair, but does not found a paper. |
| Linear modal no-cloning | Background theorem | Modal/finite-field no-cloning is established prior work. The classical-coefficient-access distinction is valuable exposition. |
| No support-faithful no-signalling probability completion for the displayed Bell support | Boundary example / seed for priority 4 | The exact certificate is useful, while the general phenomenon is known in modal quantum theory. A classification would be new work. |

## What should not be split into separate papers now

- A paper centered only on the rotation centralizer or the ring isomorphism.
- A paper centered only on no-cloning, teleportation, dense coding, or finite-field interference.
- A paper centered only on unrestricted rank activation.
- A paper centered only on the current orthogonal no-go.
- A paper presenting the finite inventories as if exhaustive computation alone established a general theory.
- A paper claiming that the Boolean model supplies a physical probability rule, physical quantum advantage, or hardware prediction.

These items remain useful as examples, appendices, datasets, and negative controls.

## Highest-value research plan

### A. Closed chain-ring process semantics

The central unresolved problem is the zero-tensor witness `u^3 tensor_A u = 0` for two nonzero proposed preparations. A publishable solution should:

1. Choose the state class: primitive/unimodular vectors, typed quotient modules, or another explicitly justified class.
2. Define independent composition and prove associativity plus closure.
3. Define complete effects and selective conditioning; prove that every permitted branch remains in the state class or in a declared typed successor.
4. State the allowed reversible and nonreversible operations.
5. Re-evaluate contextuality, coding, teleportation, and copy activation under this contract.
6. Prove the exact relation to the literal `F_2` expansion; an injective linear representation alone is insufficient because it is not monoidal.

This would turn the audit's main correction into a constructive theory rather than a warning.

### B. Restricted-operation conversions

The most promising concrete theorem questions are:

- Which subgroup of `GL(8,2)` normalizes the embedded `M_2(A)` gate algebra and the 192-basis measurement family?
- Which invariants survive that subgroup: Smith type, leading valuation multiplicity, support contextuality class, exact code size, or a coarser combination?
- What are the exact one-copy and multi-copy conversion preorders under admissible local filters?
- Does any singular structured resource activate while all intermediate states and filters remain inside a preparation-closed restricted theory?

These questions are more likely to produce new mathematics than repeating unrestricted binary-rank normal forms.

### C. Multipartite contextuality

The existing GHZ computation becomes a paper only after at least one analytical extension:

- an `n`-party construction with a bounded or exact context count;
- a classification of weighted GHZ states under the declared rotation-compatible bases;
- a theorem relating multipartite flattening/valuation data to logical or strong contextuality; or
- a proof of global minimality for an explicitly defined measurement class.

The existing six-context witness and the weighted example are good regression fixtures for that work.

## Literature boundary

The present triage relies on the following primary-source boundaries:

- Schumacher and Westmoreland already provide finite-field modal states, Bell nonlocality, and no-cloning: <https://arxiv.org/abs/1010.2929>.
- James, Ortiz, and Sabry already provide finite-field interference, reversible computation, teleportation, and dense-coding analogues: <https://arxiv.org/abs/1101.3764>.
- Abramsky and Brandenburger supply the general global-section framework for logical and strong contextuality: <https://arxiv.org/abs/1102.0264>.
- Gogioso and Zeng give general multipartite Mermin nonlocality conditions in abstract process theories, so a CM-derived GHZ paper needs a precise restricted-model result: <https://arxiv.org/abs/1506.02675>.
- De Beaudrap treats computation over semirings/rings, including finite fields and cyclic rings: <https://arxiv.org/abs/1508.07338>.
- Werner supplies the tight teleportation/dense-coding/operator-basis comparison in ordinary quantum theory: <https://arxiv.org/abs/quant-ph/0003070>.

A fresh specialist priority search is still required before submitting any new theorem. The current review supports opportunity ranking, not first-discovery claims.

## Preservation anchors

Do not discard or overwrite these sources:

- `C:\Users\brian\Downloads\CM_Correctness_Audit_Standalone.tex`
- `output\cm_lm_publication_20260918\runs\canonical_01\audit\paper\CM_Correctness_Audit.pdf`
- `output\cm_lm_publication_20260918\runs\canonical_01\audit\paper\CM_Correctness_Audit_Standalone.tex`
- `output\cm_lm_publication_20260918\runs\canonical_01\audit\code\`
- `output\cm_lm_publication_20260918\runs\canonical_01\audit\data\`
- `output\cm_lm_publication_20260918\runs\canonical_01\audit\tests\`
- `output\cm_lm_publication_20260918\runs\canonical_01\audit\MANIFEST_SHA256.txt`
- `output\cm_lm_publication_20260918\runs\canonical_01\adversarial\NOVELTY_MATRIX.md`
- `output\cm_lm_publication_20260918\RESEARCH_GAPS_AFTER_DEEP_DIVE.md`

The audit archive already contains the executable evidence, raw tables, historical snapshots, and manifest needed to keep the uncaptured mathematics recoverable. Its safest immediate publication role is a versioned technical report or software companion with a permanent archive identifier, cited by the three papers where detailed constructions or negative controls matter.
