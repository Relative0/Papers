# Modal CM Research Summary

## Executive conclusion

The pure-Boolean CM coefficient ring supports a mathematically coherent **modal linear-state calculus** with reversible mixing, CM-nonseparability, Bell/GHZ possibility contradictions, exact teleportation-like and dense-coding-like protocols, a no-cloning theorem, and a finite local-equivalence theory. None of this requires signed amplitudes or Born probabilities.

The most important outcome of this pass is not that finite Boolean systems can mimic familiar quantum-information structures—that is already known from modal/finite-field quantum theory. The more distinctive result is that the CM ring is **not a field**. Its nilpotent/zero-divisor structure splits CM-nonseparable states into multiple Smith classes, and those classes now have a complete possibilistic Bell classification under all 192 reversible projective local bases: equal-valuation nonseparable classes are strongly contextual, off-diagonal nonseparable classes are logically contextual but not strong, and all nonzero separable classes are relationally local. The same Smith distinction also has operational consequences in teleportation.

The teleportation classification is now complete for the project's tight linear/modal architecture. A two-party resource supports deterministic universal exact teleportation **iff its coefficient matrix has unit determinant, equivalently iff it lies in Smith class `(0,0)`**. Thus all 24,576 `(0,0)` resources work, while all nine other nonseparable Smith classes fail.

This shows that **nonseparability and even strong contextuality are not sufficient teleportation resources over the CM chain ring**. The actual invariant for this task is full module rank / unit determinant.

## Established results

### Algebra and gates

**[PROVED/EXHAUSTIVE]** The working ring is `A=F2[C4] ~= F2[u]/(u^4)`. Baseline `H_star`, shear, phase-kickback, CNOT, and `B_star` identities recheck exactly.

**[EXHAUSTIVE]** Complete one-bit `2x2` inventory:

- 65,536 matrices total;
- 24,576 invertible;
- 512 intrinsic-unitary;
- 128 monomial unit phase-permutations;
- 24,448 nonmonomial invertible branch mixers;
- 20,608 invertible full splitters.

### Modal measurement bases

**[PROVED/EXHAUSTIVE]** Under the explicit support rule “nonzero = possible,” reversible two-outcome effects give 192 unordered projective bases modulo row-unit scaling/outcome swap. Only four projective classes are intrinsic-unitary.

This makes a key methodological distinction: **reversible modal basis change is broader than intrinsic unitarity** in this ring.

### Bell

**[PROVED/EXHAUSTIVE]** The support Bell state with three embedded-F2 reversible settings yields an explicit strong possibilistic Bell contradiction. All 64 deterministic assignments fail.

**[BOUNDARY]** The witness is inherited from the embedded finite-field modal subtheory, so it is not evidence for a new nilpotent Bell mechanism.

**[THEOREM/EXHAUSTIVE]** Across all 192 reversible projective local bases, the complete Smith-class classification is:

- `(a,a)`, `a<4`: **strongly contextual**;
- `(a,b)`, `a<b<4`: **logically contextual but not strong**;
- `(a,4)`, `a<4`: **exactly relationally local**;
- `(4,4)`: zero state, excluded as a degenerate empty-support model.

By local-equivalence invariance this classifies all 65,536 two-party states: 26,214 are strong, 34,056 are logical-not-strong, 5,265 nonzero states are relationally local, and one is the zero vector. Thus **all 60,270 CM-nonseparable states are possibilistically contextual** under this complete measurement universe, while all nonzero CM-separable states are possibilistically local.

For every off-diagonal class there is an explicit three-setting Hardy-style witness showing a possible event with no global extension, while a constructive unit-first-coordinate choice supplies at least one global section across the entire 192-basis family.

**[COROLLARY]** The natural `B_star` `delta` state is class `(0,2)`: it has a global section (so it is not strong), but 36,864 of its 137,216 possible sections are unextendable. It is therefore logically contextual/nonlocal, not local.

### Teleportation

**[PROVED/EXHAUSTIVE]** A pure-Boolean reversible analyzer built from the four nonseparable states `vec(I),vec(X),vec(K),vec(KX)` teleports arbitrary `A|0> XOR B|1>` exactly using the support Bell resource. All `16^2 * 4=1024` state/outcome branches recover exactly.

No global CM phase quotient is needed.

**[THEOREM/PROVED/EXHAUSTIVE]** The complete teleportation-resource theorem is: a resource is universally exactly teleportation-capable iff `det(M)` is a unit iff its Smith class is `(0,0)`. All 65,536 resource states were checked with a fixed pure-Boolean Bell analyzer: exactly 24,576 succeed, all in `(0,0)`, and every other Smith class has zero successes.

**[COROLLARY]** The `B_star`/`delta` resource fails not because the particular natural analyzer was poorly chosen, but because its Smith class `(0,2)` is singular. No reversible analyzer can create a universally correctable branch from it in the stated linear architecture.

**[FOLLOW-UP THEOREM]** Singular classes are not all equally weak. For `(0,b)`, a reversible analyzer can exactly teleport one full free `A`-line (16 ring vectors) on all four outcomes; if `a>0`, no nonzero exact state can be recovered by an `A`-linear correction. Every class retains the Smith quotient `A/(u^(4-a)) + A/(u^(4-b))`. Equal-valuation classes `(1,1),(2,2),(3,3)` can transfer their fixed quotient deterministically on all four outcomes, while off-diagonal nonzero classes have at most two fixed-quotient success labels. Singular resources have zero universally exact postselected branches, and neither product local ancillas nor any finite tensor power activates universal exact teleportation.

### GHZ

**[PROVED]** Both support GHZ and `delta` GHZ states are nonseparable across all bipartitions.

**[PROVED/EXHAUSTIVE]** Support GHZ has a six-context modal contradiction; all 512 deterministic assignments fail.

**[NEGATIVE/EXHAUSTIVE]** The `H_star`-generated `delta` GHZ state admits exact relational local models for both the tested embedded-F2 setting family and the complete intrinsic-unitary projective family.

### Local equivalence and separability

**[THEOREM/EXHAUSTIVE]** Every two-party state belongs to one of 15 Smith classes `diag(u^a,u^b)`, `0<=a<=b<=4`. CM-separability is exactly `b=4`.

State counts:

- separable: 5,266;
- nonseparable: 60,270.

This supplies a natural **Smith-Schmidt analogue**, without importing norms or probabilities.

### Separability-preserving gates

**[THEOREM]** Every local product map preserves simple tensors; local invertibles preserve separability and nonseparability in both directions.

**[EXHAUSTIVE]** Of 24 two-bit basis permutations, 8 preserve every separable state and 16 can create nonseparability. The preserving eight are exactly local bit flips with optional party SWAP.

### Secondary structures

**[PROVED]** Linear no-cloning analogue.

**[CONSTRUCTION]** Superdense-coding-like four-message modal protocol using the same support-Bell basis as teleportation.

**[PROVED]** Global multiplication by a CM unit is harmless only under support-only semantics; exact CM pattern readout generally sees it.

## What is genuinely special about the CM ring so far?

The embedded-F2 strong Bell/GHZ and generic no-cloning/teleportation motifs have clear modal/finite-field precedents. The current ring-specific content is instead concentrated in five facts:

1. `A` is a length-four finite chain ring with nilpotents and zero divisors rather than a field.
2. Two-party nonseparability therefore has **ten** nonseparable local Smith classes, not a single nonzero rank-two class.
3. The complete reversible-basis possibilistic hierarchy follows those valuations: four equal-valuation classes are strong, while six off-diagonal classes are logical-not-strong.
4. Singular but nonseparable states exist; `diag(1,delta)` is the canonical example.
5. Universal exact teleportation is completely characterized by full module rank: only Smith `(0,0)` works. The other nine nonseparable classes fail, including three strongly contextual classes.

The Hardy implication pattern itself is standard possibilistic logic; the distinctive content is its systematic appearance across the unequal-valuation Smith strata and the theorem tying contextuality strength to chain-ring valuation. This suggests a resource theory indexed by Smith data (and perhaps finer stabilizer/measurement invariants) rather than a binary separable/nonseparable distinction.

## What is only an analogy?

The following language is useful only with explicit qualification:

- “phase” means the multiplicative `C4` subgroup or a ring unit, not a complex phase amplitude;
- “unitary” means `U^dagger U=I` for the CM transpose involution, not preservation of a positive Hilbert norm;
- “measurement” means the explicit LM-compatible modal support contract, not a Born-rule experiment;
- “Bell/GHZ state” means a structurally analogous ring-module vector;
- “teleportation” means exact conditional algebraic state transfer under a four-outcome modal analyzer and classical correction label;
- “Schmidt” refers only to Smith canonical data.

## Main limitations

- No Born rule, probability distribution, positive norm, or physical collapse dynamics.
- No inference that nature follows this ring model.
- No quantum speedup or communication-capacity advantage.
- No full `GL4(A)` separability-preserver classification.
- No canonical reduced-state/partial-trace operation yet; monogamy claims are premature.
- The nilpotent off-diagonal Bell classes are **not strongly contextual**; their positive ring-specific result is logical/Hardy contextuality.
- No nilpotent-specific GHZ contradiction was found for the tested `delta` GHZ measurement families.

## Literature-conditioned novelty position

Modal quantum theory, finite-field quantum computing, possibilistic contextuality, phase-group analyses, vector logic, generalized ring/semiring quantum theories, and finite-chain-ring quantum codes are all established areas.

In particular, `F2[u]/(u^s)` is already used in quantum-code constructions, so the ring family itself is not novel to quantum-information mathematics.

The narrower combination not located in the bounded search is:

- Droncheff's CM/LM logical machinery;
- cyclic CM convolution giving `F2[C4] ~= F2[u]/(u^4)`;
- use of that ring as a pure-Boolean modal state coefficient system;
- CM transpose dagger and the `H_star`/`B_star` gate set;
- LM-compatible support readout; and
- Smith-class resource analysis showing both the strong/logical/local contextuality trichotomy and nilpotent nonseparable teleportation failure.

That is the best candidate for a future paper's distinctive contribution, subject to broader literature review and peer scrutiny.

## Highest-value next experiments

1. **Beyond-tight teleportation:** test whether singular Smith classes can transfer restricted alphabets, quotient states, or succeed with ancillas/multi-round protocols; the deterministic tight theorem is now closed.
2. **Contextuality-resource theorem beyond complete GL bases:** determine which parts of the Smith-class trichotomy survive when measurements are restricted to gate-generated/intrinsic-unitary families, and extend the valuation proof to multipartite states.
3. **Full separability-preserver group:** classify invertible `4x4` maps preserving the simple-tensor variety over the finite chain ring.
4. **Measurement calculus:** connect the original LM construction more tightly to effect modules and define a principled post-measurement update rule.
5. **CM stabilizer subtheory:** compute the group/orbits generated by local units, `P`, `H_star`, CNOT, and selected shears, with explicit comparison to established finite Clifford/stabilizer theories.

## Reproducibility

The package includes source, unit tests, complete state/gate inventories, raw support tables, hidden-variable search outputs, teleportation checks, and a SHA-256 manifest. Run:

```text
python run_all.py
python -m unittest discover -s tests -v
```

The two existing consolidated papers are not overwritten; the new LaTeX manuscript is an addendum under `paper/`.
