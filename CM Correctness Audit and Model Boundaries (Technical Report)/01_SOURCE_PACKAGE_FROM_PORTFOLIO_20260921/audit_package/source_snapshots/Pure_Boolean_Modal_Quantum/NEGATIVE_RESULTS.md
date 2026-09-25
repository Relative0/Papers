# Negative Results and Non-Promoted Claims

Negative evidence is part of the result set, not discarded as failed exploration.

## N1. `B_star` nonseparability does not imply universal teleportation

**[PROVED + EXHAUSTIVE]** The natural Bell-like resource

`B_star|00> = E0|00> XOR delta|11>`

is CM-nonseparable, yet with the corresponding `B_star^-1` analyzer all four receiver branch maps have determinant zero. No branch admits a universal `A`-linear inverse correction.

This directly rejects the tempting inference

> “CM-nonseparable + reversible Bell transform automatically gives teleportation.”

The complete resource theorem strengthens this negative result: the support Bell resource works because its coefficient matrix is invertible (Smith `(0,0)`), while the `delta` resource is singular (Smith `(0,2)`). No alternative reversible four-outcome analyzer can make any branch universally linearly correctable for a singular resource.

## N1b. Postselection, local ancillas, and finite copies do not repair a singular full-state resource

**[PROVED]** The singular-resource follow-up strengthens N1 in three directions. First, a singular resource has **zero** analyzer branches that can be universally exactly corrected, so merely designating some outcome as a heralded/postselected success event cannot recover an arbitrary `A^2` input. Second, adding fixed product ancillas on Alice's or Bob's side cannot raise the residue-field rank of a branch map above the rank of the resource. Third, for any finite tensor power `M^(tensor k)`, `rank_F2(Mbar^(tensor k))=rank_F2(Mbar)^k<=1` when `M` is singular, so no finite number of copies activates a branch with an `A`-linear left inverse onto `A^2`.

This no-go is specifically about **universal exact full-state transfer**. Singular resources still have a nontrivial restricted/quotient hierarchy; `(0,2)`, for example, exactly transfers one free `A`-line and retains a 64-class canonical quotient. See `SINGULAR_TELEPORTATION_HIERARCHY.md`.

## N2. `B_star` Bell state is not **strongly** contextual, but it is not local

**[EXHAUSTIVE + PROVED CORRECTION]** All 192 unordered projective reversible two-outcome local bases were enumerated. For `E0|00> XOR delta|11>`, the full impossible-outcome constraint system is satisfiable, so a deterministic global section exists. Therefore there is **no strong** possibilistic Bell contradiction for this state under the complete local basis universe.

However, existence of one global section is not the same as exact possibilistic locality. The completed support-extension check finds:

- 137,216 possible local sections;
- 100,352 extendable sections;
- **36,864 possible sections with no compatible global extension**.

An explicit Hardy-style witness is retained in `data/offdiagonal_hardy_witnesses.json`. Thus the earlier tentative interpretation “perhaps local because a global section exists” is rejected. The correct classification is **logically contextual/nonlocal but not strongly contextual**.

The retained negative result is narrower and still important: `B_star` does not realize an all-versus-nothing/strong contradiction across the complete reversible-basis family.

## N3. Restricting to intrinsic-unitary measurement bases removes the support-Bell contradiction found with reversible shears

**[EXHAUSTIVE]** The complete intrinsic-unitary projective family has only four bases. Under this family:

- support `Phi`: 16 compatible global assignments, every possible section covered;
- support `Psi`: 16 compatible global assignments, every possible section covered;
- `B_star` `delta` state: 65 compatible global assignments, every possible section covered.

Thus the Bell contradiction in `RESULTS.md` depends on allowing reversible local bases more generally, including non-unitary shears in the ring's dagger structure.

This is an important distinction between “reversible” and “intrinsic-unitary” in this model.

## N4. The most direct `H_star`-generated GHZ analogue is local in the tested modal families

**[EXHAUSTIVE]** The state

`G_delta = E0|000> XOR delta|111>`

is nonseparable across every cut, but:

- under the 27 embedded-F2 `Z/X/Y` contexts it has 16 compatible deterministic global assignments and exact support coverage;
- under the complete intrinsic-unitary projective basis family it has 23 compatible global assignments and exact support coverage.

Therefore no modal GHZ contradiction was found for this natural nilpotent GHZ analogue in these families.

## N5. The positive Bell/GHZ contradictions are not nilpotent-specific

**[LITERATURE COMPARISON / CORRECTION]** The successful support Bell and support GHZ witnesses use only coefficients `{0,E0}` and local bases with entries `{0,E0}`. They lie entirely in an embedded `F2` modal subtheory.

They should therefore not be presented as evidence that `delta`, zero divisors, or the full CM phase ring create a new form of Bell/GHZ nonlocality. Their value here is as an exact embedding and a baseline against which genuinely ring-specific states can be compared.

## N6. No Born rule or positive norm emerges from the pure Boolean construction

**[BOUNDARY]** The ring has nonzero nilpotents and zero divisors. The intrinsic dagger self-product is not positive-definite. Hamming weights are external integer counts. Nothing in this pass derives a positive probability measure or Born-type rule.

Do not reinterpret support tables or Hamming-normalized values as quantum probabilities.

## N7. No physical collapse/post-measurement dynamics was derived

**[OPEN]** The project uses an explicit modal support contract: after a reversible basis change, a nonzero coefficient denotes a possible outcome. This is sufficient for possibilistic Bell/GHZ constraints and conditional teleportation branches.

A unique physical post-measurement state-update rule was not derived from the original LM formalism or the ring algebra. Claims requiring such a rule remain open.

## N8. No general two-party separability-preserver classification was completed

**[OPEN]** The complete `24` computational-basis permutation gates were classified, and local product invertibles plus SWAP are proved to preserve separability. But the entire `GL4(A)` universe is vastly larger and was not exhaustively classified.

Do not generalize the 8-versus-16 basis-permutation result to all two-party invertible `4x4` CM-ring gates.

## N9. No monogamy theorem was claimed

**[OPEN]** A monogamy statement normally depends on a notion of reduced state/partial trace and on a resource measure. The present pure modal vector/LM calculus has not fixed a canonical reduction rule with the required operational meaning. Monogamy or its failure is therefore not yet well-posed enough for promotion.

## N10. No computational or communication advantage is established

**[BOUNDARY]** The teleportation and superdense-coding-like constructions are algebraic/modal protocols. They do not by themselves establish physical channel capacities, qubit resources, or quantum speedups.

Likewise, this thread did not benchmark the CM normalization/folding compiler; that belongs to the separate computation/benchmarking research program.

## N11. The ring itself is not novel to quantum-information-adjacent mathematics

**[LITERATURE]** Rings of the form `F2[u]/(u^s)`, including the `s=4` family containing the present ring presentation, already appear in finite-chain-ring coding literature used to construct quantum error-correcting codes. Generalized categorical quantum theories over rings/semirings are also established.

A defensible distinctive target is narrower: the **CM-derived** interpretation of `F2[C4] ~= F2[u]/(u^4)` as a coefficient ring for a pure-Boolean modal state calculus, combined with original CM/LM measurement machinery and the specific reversible gate set. The literature search in this pass did not locate that exact combination, but absence from a bounded search is not proof of novelty.
