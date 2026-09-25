# Research Summary: LM Calculus to Modal Measurement

## Bottom line

A mathematically meaningful bridge exists, but the later modal/effect framework is **not derived directly** from Paper B's formula-valued LMs.

The exact positive bridge is:

`Boolean formula algebra B -> enriched algebra B tensor_F2 A -> valuation specialization into A -> support predicate for nonzero amplitudes`.

The exact missing modal structure is:

- the independently introduced multiplication making the four CM coefficients into `A = F2[u]/(u^4)`;
- the admissible measurement family, e.g. rows of `GL_n(A)`;
- the support rule `a != 0` means "possible".

## Strongest positive theorem

For a symbolic effect/state contraction in `B tensor A`, define `Supp_A(q)` to be the Boolean predicate true exactly on valuations for which the specialized ring amplitude is nonzero. Then

`v(Supp_A(<E,S>)) = 1` iff `<v_A(E), v_A(S)> != 0`.

Therefore `Supp_A(<E,S>)` is satisfiable iff there exists a Boolean valuation making the corresponding concrete modal event possible.

## Strongest negative theorem

No unital Boolean-ring homomorphism `B -> F2[u]/(u^4)` can produce nilpotent or nontrivial unit amplitudes. Every Boolean formula is idempotent, and the local chain ring has only idempotents 0 and 1. Any direct Boolean-ring map therefore factors through ordinary `F2` valuation.

## What Paper B already gives

- formula-valued LMs over the Boolean algebra of formulas modulo logical equivalence;
- positive and general valuations;
- XOR-AND logical pairing;
- exact pairing identity;
- theorem that valuation commutes with pairing.

These are background, not new bridge novelty.

## What the later modal theory adds

- the cyclic/chain-ring scalar algebra;
- ring-valued states and resources;
- effects as rows of reversible local bases;
- the complete 192 projective two-outcome basis family;
- the rule that nonzero amplitude means possible.

The modal source explicitly calls the last rule an additional contract.

## Measurement-family result

Bare Paper-B complement-paired logical states evaluate only to coordinate effects. They therefore do not generate all embedded-F2 modal effects and cannot generate the 192-basis family.

After a CM coefficient basis is chosen, every ring coefficient can be encoded by a four-bit CM and hence by a Paper-B LM. Thus all modal effects are **LM-encodable as coefficient data**, but are not generated as original LM effects.

## Sequential update

For any reversible basis `B`, define branch projector

`J_i^B = B^{-1} P_i B`.

This is idempotent, orthogonal across distinct outcomes, resolves the identity, and satisfies

`J_i^B psi != 0` iff `(B psi)_i != 0`.

It is invariant under independent unit scaling of measurement rows and gives exact same-basis repeatability without dividing by the measured amplitude.

## Remaining process-theory obstruction

Zero divisors prevent closure:

- `(u,0)` and `(u^3,0)` are both nonzero but their tensor is zero;
- restricting to unimodular preparations is not enough, because conditioning can produce nonzero nonunimodular states, e.g. `diag(1,u)` conditioned on Alice's second standard effect leaves `(0,u)`.

Therefore the current framework has a clean branch update but not yet a closed unrestricted sequential process theory.

## Paper recommendation

Use this as a central theoretical bridge section of the Boolean-modal synthesis paper, not as a standalone claim that LMs derive modal quantum measurement.

The best narrative is:

`LM -> Boolean-ring contraction -> valuation naturality -> direct-map obstruction -> A-enrichment -> symbolic-support theorem -> modal effect family -> extra support contract -> branch update -> closure obstruction`.
