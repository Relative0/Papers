# Independent audit of the native Boolean CM block rebuild

Date: 2026-09-17

## Bottom line

The central algebraic/computational claims of the native block rebuild reproduce on a clean rerun. In particular, the support-Bell resource gives exact branch-wise recovery of every 8-bit one-logical-bit CM phase state on all four outcomes **when the allowed dynamics are arbitrary invertible XOR/AND Boolean-linear maps in the stated block model**.

That statement is narrower than physical quantum teleportation. The present model assumes the modal possible/impossible measurement contract and conditional selection of one Alice outcome. It supplies no Born probabilities, no physical collapse model, and no experimental realization. Multi-party states also use a **shared 4-bit phase register** across logical branches; they are not the full tensor product of an independent local 4-bit phase register for every party.

A new audit boundary is important: the explicit universal protocol is **not orthogonal-only**. Its standard 4x4 Bell analyzer is invertible but not Boolean-orthogonal, and two of the four 8x8 branch corrections are invertible but non-orthogonal. Moreover, an exhaustive scan of all 65,536 possible single-outcome row-blocks built from the P-generated 4x4 phase operators found **no** outcome block that is simultaneously compatible with an orthogonal analyzer and gives an orthogonally correctable support-Bell branch. Thus the universal result is currently a theorem for general reversible Boolean-linear dynamics, not for the stricter Boolean-orthogonal subtheory.

## Audit actions

- SHA-256 manifest verified with no mismatch.
- Full result generator rerun from a clean copy; it reproduced the stated summary.
- Original regression suite rerun: 12/12 passed.
- Added explicit scope-boundary tests for general-reversible versus orthogonal-only dynamics.
- Rechecked the GHZ six-context minimum independently from the generated support table: no unsatisfiable subset exists with 1 through 5 contexts; a 6-context contradiction exists.
- Rechecked the standard support-Bell teleportation branch maps: all four have Boolean rank 8 and invertible corrections; all 256 inputs x 4 outcomes recover exactly.
- Rechecked all 65,536 resource matrices under the fixed standard Bell analyzer: branch rank equals resource rank on every outcome, and exactly 24,576 resources have rank 8.

## Scope table

| Claim | Audit status | Scope / failure mode |
|---|---|---|
| `P^4 = I`, `P^T=P^3` | PASS | Exact native Boolean permutation identities. |
| `N=P XOR I`, `N^4=0`, ranks `4,3,2,1,0` | PASS | Ordinary XOR/AND Boolean matrix composition. |
| 16 P-generated phase operators = full centralizer of P | PASS, exhaustive | All 65,536 Boolean 4x4 matrices checked. |
| 65,536 two-branch phase-block gates; 24,576 invertible; 512 orthogonal | PASS, exhaustive | All four-selector 2x2 block gates checked. |
| 192 reversible projective measurement bases | PASS | Uses the explicit support-measurement quotient by invertible phase row scaling and outcome swap. |
| Boolean split/recombine interference | PASS | Exact XOR cancellation; not a probability interference law. |
| Bell Z/X/Y support contradiction | PASS, exhaustive | All 64 deterministic global assignments fail under the stated possible/impossible semantics. |
| Complete two-party contextuality classification | PASS under measurement contract | 15 rotation-filtration normal classes; conclusion depends on admitting all 192 reversible projective bases as measurements. |
| Universal exact support-Bell teleportation | PASS under general reversible dynamics | 1,024/1,024 input-outcome checks. Analyzer/corrections need not be orthogonal. |
| Universal resource criterion = Boolean rank 8 | PASS for fixed standard Bell analyzer; theorem-level rank bound | All 65,536 resources checked; standard analyzer reaches the resource-rank upper bound. |
| `(0,2)` universal teleportation | FAIL | Resource rank 6, therefore exact arbitrary 8-bit recovery is impossible. Standard analyzer preserves all 6 available dimensions. |
| Orthogonal-only support-Bell teleportation | NEGATIVE in the P-block analyzer model | No orthogonal-analyzer outcome block gives an orthogonally correctable support-Bell branch; standard protocol is not orthogonal-only. |
| Support GHZ contradiction over Z/X/Y | PASS | Zero global assignments; minimum unsatisfiable context set has size 6. |
| Rotation-weighted GHZ contradiction over tested basis families | FAIL / negative result | Embedded Z/X/Y has 16 globals; four orthogonal bases have 23 globals; all possible sections are covered in those tests. |
| Physical/Born-rule quantum teleportation | NOT CLAIMED | No probabilities, collapse dynamics, no-signalling theorem, or physical implementation has been established. |
| Full independent local phase-register tensor model | NOT TESTED | Current construction uses one shared 4-bit phase register across logical branches. |

## Interpretation

It is therefore accurate to say **“universal exact modal CM teleportation”** only with the qualifiers above: arbitrary unknown state in the model, exact recovery on each modal measurement branch, using general invertible Boolean-linear operations. It is not yet accurate to shorten that to “we have ordinary quantum teleportation,” nor to claim the result inside an orthogonal-only dynamics restriction.
