# Focused Hostile Theorem Audit of U1–U6 and Constrained-Adaptive Extension

**Project:** Unified Differentiation Calculus
**Date:** 29 September 2026
**Method:** source reconstruction, adversarial proof audit, exhaustive bounded computation, independent verifiers, and theorem-level priority search.

## 1. Numbering correction before the audit

The audit prompt anticipated U4=cartesian/saturation, U5=mapping-cone, and U6=constrained observation design. The authoritative unification manuscript numbers them differently:

- U1 — unified preorder thinning;
- U2 — quotient interpretation / T0 transition;
- U3 — canonical lexicographic refinement factorization;
- U4 — mapping-cone / octahedral defect sequence;
- U5 — cartesian fiber-saturation theorem;
- U6 — newly-enabled measurement / non-cartesianity theorem.

Constrained observation design is the following Section 9 program. This audit follows the source numbering and supplies compatibility filenames for the prompt's anticipated numbering.

## 2. Theorem status table

| Result | Correctness | Repair needed? | Prior-art status | Research value |
|---|---|---|---|---|
| U1 | Valid | No | Standard / definitional | Foundational notation only |
| U2 | Valid after repair | **Yes** | Standard quotient-order ingredients | Useful synthesis |
| U3 | Valid | No substantive repair | Lexicographic sum is standard | Strong organizing lemma |
| U4 | Valid | Terminology: LES, not direct sum | Standard octahedral mapping-cone theorem | Useful application to U3 |
| U5 | Valid | No | Pullback/fiber saturation is standard | Clean interface theorem |
| U6 | Valid under stated fine-measurability hypothesis | Hypothesis must remain explicit | Saturation/measurability ingredients standard | Useful measurement-availability interpretation |
| Observation design | Valid | Separate unrestricted vs constrained | 2-dimension/Test Cover nearby | Constrained version promising |
| A1 | Proved | No | Restricted-query search is established; exact ProLT corollary not located | Plausible narrow contribution |

## 3. Strongest hostile findings

### U2 overstatement

At world level, refinement only deletes preorder relations. But quotienting can turn deletion of one direction in a formerly symmetric pair into a **new strict relation between two newly split quotient points**. Thus “splitting + deletion of old quotient comparisons” is incomplete. U3 supplies the correct repair: a split coarse point expands to a fiber poset, while cross-fiber descents are deleted.

### U4 terminology

The standard octahedral triangle is oriented correctly:

\[
\operatorname{Cone}(j)\to\operatorname{Cone}(r)\to\operatorname{Cone}(\pi)\to\operatorname{Cone}(j)[1].
\]

It yields a long exact sequence, not an unconditional direct-sum decomposition.

### U6 hypothesis

The equivalence “cartesian iff coarse measurable” needs `E` to be fine-measurable. Without that hypothesis, an event may cut a fine signature cell while leaving all fine *labels* represented.

## 4. Exhaustive computational gate

### Four-world relation/refinement census

All 65,536 Boolean observation families were reduced to 355 distinct observation-generated preorders. Each was refined by all 16 one-bit observations: 5,680 transitions.

- U1 failures: **0**
- U3 failures: **0**
- pre-T0 simultaneous splitting+thinning cases: **600**
- T0 cases with splitting: **0**, as required

### Cartesian / measurement census

- support/refinement cases: **90,880**
- U5 failures: **0**
- fine-measurable U6 cases: **80,652**
- U6 failures: **0**

Independent partition-only implementation:

- 15 partitions;
- 3,840 partition/label/event cases;
- failures: **0**.

### U4 cone sequence

Over F2, all 5,680 transitions were rebuilt at chain level:

- exactness checks: **62,934**;
- failures: **0**;
- relative-homology dimension checks: **18,982**;
- post-T0 cases checked: **3,504**.

An exact-rational representative census covered 1,420 cases and 15,387 exactness checks with zero failures. The integral result is supported formally by the coefficient-independent cone construction rather than by a full Smith-normal-form census.

## 5. Priority verdict

The hostile literature search removes broad novelty claims from U1, the lexicographic machinery of U3, the cone machinery of U4, and the raw pullback/saturation content of U5. It also places unrestricted observation design next to established Boolean-lattice 2-dimension and Test Cover theory.

The coherent potential contribution is therefore the **ProLT-specific assembly**:

\[
\text{fiber-profile refinement}
\to
\text{lexicographic expansion + descent thinning}
\to
\text{cartesian availability obstruction}
\to
\text{defect sequence},
\]

plus constrained regimes in which ProLT topology genuinely limits allowable observations.

## 6. Adaptive gate: an important negative result

With arbitrary Boolean queries, homotopy-neutrality does **not** make identification harder. At every finite T0 branch, take a linear extension and choose a near-half suffix. Its indicator is isotone, hence topologically redundant and homotopy-neutral. This gives optimal worst-case depth `ceil(log2 n)` on every finite poset.

So a publication-worthy adaptive problem needs a stricter resource: fixed query library, syntax/cost restriction, defect budget, or a nonredundancy constraint.

## 7. New theorem A1

The chain regime nonetheless yields a sharp ProLT-specific result. Using the exact chain classification, safe adaptive identification has optimal depth

\[
\lceil\log_2 n\rceil,
\]

but every safe identification tree must use a **topologically redundant separator** at some two-state cherry. Exactly one redundant query on each worst branch is sufficient. If redundant safe queries are forbidden, identification is impossible.

The key construction uses alternating query profiles on all branches of size at least three and the redundant profile `01` only at the final two-state split.

This was exhaustively optimized through `n=10` and independently verified through `n=30`.

## 8. Final answers to the audit questions

1. **Does U3 survive exactly?** Yes.
2. **Is F genuinely a lexicographic sum?** Yes, under the standard substitution definition.
3. **Is it canonical?** Canonical on realized signature data; canonically isomorphic under relabeling.
4. **Is U5 a real pullback theorem or a saturation restatement?** Both: it is a genuine pullback statement whose proof reduces to exact fiber/profile saturation.
5. **Strongest saturation criterion?** `B_p^T=B_p^S` for every surviving coarse `p`; for fine-measurable events this is equivalent to coarse measurability.
6. **Is U4's cone orientation correct?** Yes under the stated cone convention.
7. **Does U4 give a direct decomposition?** No; it gives an exact triangle and LES. Direct splitting needs extra hypotheses.
8. **Does T0 recover relative homology?** Yes: \(F\cong P\), expansion cone acyclic, and the thinning cone is the relative complex of `(Delta P,Delta Q)`.
9. **Is observation design merely Test Cover/poset dimension?** Unrestricted forms substantially overlap established theory; ProLT-constrained variants remain nontrivial.
10. **What belongs in a paper?** U3 as organizer, repaired U2, U5/U6 as interaction lemmas, and U4 as standard machinery clearly labeled as such; U1 should be background.
11. **Did the adaptive search produce a correct nontrivial theorem?** Yes: A1. It is genuinely tied to the exact ProLT chain admissibility theorem, but novelty should be described conservatively.
12. **Next restricted regime?** Height-two adaptive protocols under the repair-forest/boundary-matrix criterion, preferably with a fixed query library.
