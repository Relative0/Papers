# Final Specialist Gate Review
## Exact Bernstein--Vazirani Query Complexity in Characteristic-Two Modal Computation

**Date:** 27 September 2026  
**Status:** Post-audit specialist gate and manuscript revision

## Scope and independence caveat

This gate used four deliberately separated specialist-role passes: (1) adaptive/query-complexity proof adversary, (2) modal and characteristic-two foundations specialist, (3) prior-art/priority specialist, and (4) hostile journal-referee/editor. These are independent reasoning passes performed by the same AI system, not four external human referees. The proof pass was conducted by reconstructing Lemma 3.1 and Theorem 3.2 from the stated contract rather than accepting the previous audit conclusion.

## Executive result

**Lemma 3.1 survives the adaptive-contract attack.**  
**Theorem 3.2 survives the adaptive-contract attack.**  
**No theorem-level prior-art match was located in the final targeted search through 27 September 2026.**  
**The manuscript was revised in response to the specialists before this final verdict.**

The principal substantive change is a more robust node-local proof of Lemma 3.1 on the fixed syntactic adaptive tree. It now explicitly neutralizes the strongest apparent loophole: secret-dependent branch possibility does not implement a secret-dependent nonlinear selector. An impossible branch is represented by a zero vector in a fixed history block; the underlying map and tree remain secret-independent.

The final priority wording is intentionally conservative. The paper now presents the main BV theorem as a differentiated characteristic-two modal specialization, not as a historically certified first result or a new polynomial method.

---

# Specialist 1 - Adaptive query-complexity proof adversary

## Verdict

**PASS after proof hardening.** Confidence: high.

## Contract attacked

The proof was tested under exactly the paper's stated contract:

- a field F of characteristic two, not assumed finite;
- finite-dimensional state spaces;
- arbitrary finite ancillas;
- a finite, syntactically fixed adaptive tree;
- complete linear instruments with injective stacked map;
- branch-dependent future operations determined by recorded history;
- every possible terminal branch required to carry the correct output label;
- a worst-case query bound over root-to-leaf paths;
- at each query node, pointwise actions `G_0,G_1` fixed independently of the secret, while different history nodes may have different fixed pairs;
- no postselection, normalization, probability rule, coefficient inspection, or secret-dependent nonlinear operation.

## Main attempted break: branch existence as hidden nonlinear information

A superficially dangerous feature is that whether a recorded branch exists can depend on the secret. If an algorithm could test the meta-property "is this branch zero?" and then dynamically change the circuit outside the fixed instrument semantics, the polynomial argument could fail.

That operation is **not** present in the stated contract. The algorithm is a fixed history tree. For every syntactic node u, define `psi_u(s)` in its node space and set it to zero for secrets for which the history is impossible. At an instrument child, the formal state is always `L_b psi_u(s)`. Whether that vector evaluates to zero is a semantic possibility statement, not a new map chosen as a function of the secret.

The revised Lemma 3.1 therefore proves the stronger node-local invariant:

> At every fixed tree node u, `psi_u(s)` is a vector-valued multilinear function of the secret bits of degree at most the number of queries on the root-to-u path.

This is the right invariant for an adaptive proof.

## Query step

For the BV secret `s` and Boolean address `x`, characteristic two gives

`f_s(x) = sum_j s_j x_j`

as a scalar in the prime subfield of F. For a fixed query node,

`G_b = G_0 + b(G_0+G_1)` for b in {0,1},

so the full pointwise oracle is affine degree one in the secret bits. A query therefore raises the degree by at most one. Secret-independent gates, injections, instrument components, and appended fixed ancillas do not raise degree.

The proof correctly works with polynomial functions on the Boolean cube, equivalently with the quotient by `s_j^2-s_j`, so multilinearization is justified as equality of functions, not as an ordinary formal-polynomial identity.

## Adaptive cases attacked

### Branch-dependent gates and query pairs
Pass. Different recorded nodes may use different fixed maps. This does not create a secret-dependent map within a node.

### Secret-dependent zero branches
Pass. They remain zero blocks in the common direct sum and do not disappear from the algebraic record.

### Early termination
Pass. An early leaf contributes a fixed terminal block at lower degree.

### Classical history carrying information
Pass. History is itself represented by the direct-sum block index. It can increase ambient dimension, but it cannot increase the dimension of the secret-dependent coefficient span beyond the number of allowed monomials.

### Arbitrary finite ancillas
Pass. They enlarge coefficient vectors but introduce no new secret monomials.

### Inverse oracle access
Pass under the manuscript's stated optional interpretation. The two fixed inverse blocks are again affine in the Boolean oracle value, so the same one-degree-per-query argument applies.

### G0 = G1
Pass. Such a query can be information-free; it does not invalidate the lower-bound implication. The matching upper bound is claimed only for QXOR.

### Infinite characteristic-two fields
Pass. The proof uses only field algebra, the embedded Boolean prime subfield, finite-dimensional state spaces, and a finite tree. No field-cardinality count is used.

## Theorem 3.2

Once Lemma 3.1 is in node-local form, the theorem follows cleanly.

1. Complete recorded evolution keeps every total record nonzero.
2. Exact recovery places each secret's nonzero record entirely in its own output-label direct-sum group.
3. Thus the `2^n` secret records are linearly independent.
4. Lemma 3.1 places all records in the span of at most `sum_{j=0}^q binom(n,j)` coefficient vectors.
5. For `q<n`, that number is strictly below `2^n`.
6. Contradiction; hence `q>=n`.
7. Standard QXOR achieves n queries by querying the n unit addresses.

The alternative point-indicator proof independently reaches `q>=n` and is a useful cross-check.

## Fresh finite stress test

A new adversarial stress program generated **400 random fixed-tree F2 protocols** for n=3 and maximum query depth q=2. It included branch-specific second queries, secret-dependent zero branches, and early-termination variants. Every test respected:

- maximum coordinate ANF degree <=2; and
- rank of the eight secret records <=7 = `sum_{j=0}^2 binom(3,j)`.

This is corroboration only; the quantified theorem rests on the proof, not on the finite test.

---

# Specialist 2 - Modal / finite-field foundations

## Verdict

**PASS WITH CLARIFIED MODEL BOUNDARIES.** Confidence: high on the internal mathematics; moderate-high on cross-literature terminology.

The complete-instrument condition is consistent with the common-kernel condition used for unconditional modal operations in the modal-quantum literature. The paper does not invoke Hilbert-space orthogonality or probability, and the exact discrimination argument correctly uses direct-sum separation of label spans.

The final text now distinguishes three easy-to-conflate locations for finite-field structure:

1. **amplitude field** - the present theorem uses amplitudes in a characteristic-two field;
2. **oracle/register algebra** - finite-field labels can occur inside an otherwise ordinary complex-amplitude quantum computer;
3. **function values** - a learned polynomial can take values in a finite field while the quantum amplitudes remain complex.

This distinction matters for the closest antecedents and is now explicit.

The ring-valued kickback example remains safely isolated in an appendix and is no longer presented as an automatic consequence of the field theorem.

---

# Specialist 3 - 2026-current theorem-level prior-art and priority

## Verdict

**DIFFERENTIATED BUT PRIORITY WORDING MUST REMAIN CAUTIOUS.** Confidence: moderate-high.

## What is not new

- The polynomial method for ordinary quantum query lower bounds is established prior art (Beals et al.).
- Dimension/counting bounds for exact oracle identification are established prior art (Farhi et al.).
- BV is a standard one-query problem in the ordinary complex-amplitude model.
- General exact-query frameworks and oracle/coset identification already include BV-type problems (Montanaro--Jozsa--Mitchison; Copeland--Pommersheim).
- Oracle-response dependence is not new; Svozil's 2026 work makes this especially explicit for exact query complexity and Deutsch-type response unitaries.
- Qualitative failure of the usual Deutsch advantage in two-valued finite-field/modal settings is prior art.

## New closest antecedents added in this gate

### Hanson--Ortiz--Sabry--Tai (2014)
They study finite-field **amplitudes**, making this a particularly important comparison. They explicitly state that the unrestricted two-valued theory cannot express Deutsch's algorithm. For suitable odd-characteristic finite-complex fields they report that deterministic algorithms including Bernstein--Vazirani perform as desired; the paper attributes the specific BV statement there to unpublished results. The revised manuscript now reports that qualification rather than presenting it as a published BV theorem.

### de Beaudrap--Cleve--Watrous (2002)
They give an exact one-query hidden-linear-structure algorithm over `GF(2^m)`, but the computation is an ordinary complex-amplitude quantum algorithm using finite-field QFT/oracle algebra. This is close in vocabulary but different in where the finite field lives and in the oracle problem.

## Current 2026 hit

Karl Svozil's 2026 preprint explicitly frames exact query complexity as depending jointly on the answer partition and the oracle access, and gives a response-unitary criterion for one-query Deutsch in the ordinary complex-unitary model. This narrows the paper's contribution boundary: access-model sensitivity itself must be treated as background.

## Final priority classification

The final targeted search through **27 September 2026** did not locate a paper stating the full theorem combination:

- characteristic-two amplitude field;
- exact recovery of all n-bit BV secrets;
- arbitrary finite ancillas;
- finite adaptive complete recorded instruments;
- history-dependent but secret-independent fixed pointwise invertible query pairs;
- lower bound `q>=n`, with matching n-query QXOR upper bound.

The defensible formulation is therefore:

> **Apparently differentiated theorem under the stated characteristic-two modal contract after targeted search; historical firstness not certified.**

The revised paper uses that level of caution and contains no firstness claim.

---

# Specialist 4 - Hostile journal referee / editor

## Verdict

**SUBSTANTIVELY READY FOR PEER REVIEW AS A FOCUSED TECHNICAL NOTE.**

The manuscript is stronger after the final gate because it no longer asks a referee to infer why adaptivity is covered. The node-local invariant makes the most important theorem easier to audit, and the worked n=2 dependence plus independent point-indicator proof give two useful checks on the central mechanism.

The literature discussion is also materially improved by distinguishing finite-field amplitudes from finite-field oracle/register labels and finite-field function values.

Remaining non-mathematical tasks are venue-specific rather than research blockers: final affiliation/contact/ORCID if desired or required, house bibliography style, and any journal-specific abstract/length formatting.

---

# Changes made to the manuscript after the specialist passes

1. Replaced the path-wise presentation of Lemma 3.1 with a direct induction on every node of the fixed adaptive tree.
2. Defined impossible histories algebraically as zero states in their fixed node blocks.
3. Explicitly explained why branch possibility is not a secret-dependent nonlinear selector.
4. Strengthened Theorem 3.2's proof discussion of classical-history information and zero/nonzero branch patterns.
5. Added/retained the independent point-indicator proof as a cross-check.
6. Added de Beaudrap--Cleve--Watrous as a close finite-field-oracle antecedent.
7. Added Hanson--Ortiz--Sabry--Tai as a close finite-field-amplitude antecedent, with the important qualification that their BV statement is attributed there to unpublished results and is in suitable odd characteristic.
8. Added Montanaro--Jozsa--Mitchison to the exact-query background.
9. Kept Svozil 2026 as the current explicit antecedent for access-model sensitivity.
10. Added the 400-case adaptive-tree stress test to the reproducibility table as finite corroboration, explicitly not as proof.
11. Re-ran LaTeX build and PDF preflight; the final manuscript has 12 pages, no undefined citations/references, and no overfull boxes.

---

# Updated publication gates

| Gate | Final result |
|---|---|
| Mathematical integrity | **PASS** |
| Lemma 3.1 adaptive-contract attack | **PASS** |
| Theorem 3.2 adaptive-contract attack | **PASS** |
| Model/assumption discipline | **PASS** |
| Novelty/priority integrity | **DIFFERENTIATED, CAUTIOUS PRIORITY WORDING REQUIRED** |
| P02-specific evidence/reproducibility | **PUBLICATION-GRADE** |
| Preprint readiness | **READY** subject only to desired author/venue metadata |
| Peer-review submission readiness | **READY FROM A SUBSTANTIVE RESEARCH STANDPOINT**; apply venue-specific formatting/metadata |

## Indicative updated score

Using the same weighted framework as the earlier audit gives an indicative post-gate score of **9.11/10**. The remaining drag is primarily unavoidable priority uncertainty and venue/metadata fit, not a known defect in the main proof.

This score is an editorial aid, not an acceptance probability and not a substitute for an external human referee.

---

# Remaining cautions

1. Do not change the priority language to "first" on the basis of this search.
2. Do not promote the DJ result to a full exact complexity theorem; only the one-query obstruction is proved.
3. Do not generalize the finite Simon scan.
4. Keep the QXOR upper bound distinct from the broader lower-bound query interface.
5. Preserve the finite-tree and secret-independent-linear-operation assumptions; relaxing either would require a new proof.

# Bottom line

The specific final gate requested has been passed: the central adaptive proof survived a fresh adversarial reconstruction, the strongest apparent loophole was converted into an explicit node-local invariant in the manuscript, and the final 2026-current search found important antecedents that sharpen the contribution boundary but did not locate an equivalent characteristic-two adaptive exact BV theorem. The revised manuscript is now substantively ready to circulate as a preprint and to send for external peer review, with appropriately cautious priority wording.
