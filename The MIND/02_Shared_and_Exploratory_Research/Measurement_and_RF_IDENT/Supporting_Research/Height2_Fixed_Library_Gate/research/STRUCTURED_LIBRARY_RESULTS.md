# H6: structured posets and libraries

## Exact solved families

The strongest exact depth family obtained here is the connected complete-bipartite parity order on n=2^k states, with coordinate tests and singleton tests, all supplied with both polarities. Its depths are

  d_ad=k, d_RF=2^(k-1)+k-1.

The recurrence D_1=1, D_k=2^(k-2)+1+D_(k-1) is proved in ADAPTIVE_DEPTH_THEORY.md. This is an exact result for a natural complete-bipartite height-one family with a precisely specified library. The genuinely height-two family with one bottom, n-2 middle states and one top attains the maximal finite gap with its oriented code-and-peeling library.

## Arbitrary libraries on a height-one star

Let P consist of incomparable leaves X below a top z. Safe identification is possible iff:

1. Q separates every two leaves;
2. for every leaf x there is a supplied oriented query q with q(x)=0,q(z)=1.

Necessity: leaf pairs must be distinguishable, and the first query separating x from z on the z path must have the safe orientation 0<1.

Sufficiency: along the z branch, successively ask useful supplied queries with q(z)=1. They are isotone and remove their zero-set leaves. Condition 2 eventually leaves only z. Every zero branch is an antichain and condition 1 supplies ordinary identification there.

For A subseteq X let A_qb={x in A:q(x)=b}. If F(A) is the star depth on A union {z}, and d_ad(B) the ordinary fixed-library depth on the leaf antichain B, then

  F(empty)=0,
  F(A)=1+min_(q(z)=1, A_q0 nonempty)
                 max(d_ad(A_q0), F(A_q1)).

The fixed query table, not arbitrary new tests, is used in both terms. This gives an exact feasibility characterization and exact recurrence; it is not a claim of polynomial optimal-depth computation.

## General height-one feasibility

RF-SAFE equals isotonicity, so it is hereditary. The generic hereditary-action proof in FIXED_LIBRARY_IDENTIFICATION.md yields polynomial RF-IDENT on all height-one posets, including crowns and fences with no three-chain. Actual height two is the first place where the proof fails because legal tests can deactivate.

## Which syntactic restrictions actually imply something

| Supplied class | Established conclusion | Limitation |
|---|---|---|
| Isotone tests on P0 | All remain safe; d_RF=d_ad, including infinity | Optimizing ordinary depth need not be easy |
| Old positive signature coordinates / monotone formulas in them | Isotone, hence preceding row | Their outcomes must still be acquired under the model |
| Literals with both polarities | Positive polarity isotone if it is an old coordinate | General supplied attribute coordinates need not be isotone |
| Complement-closed arbitrary library | Penalties persist, including exact linear family above | Complement closure is not unrestricted Boolean synthesis |
| Horn / dual-Horn | v0.4 sufficient repair certificates require its semilattice and cofinality hypotheses | No unrestricted Horn safety claim; restriction can lose hypotheses |
| Affine / XOR | No general safety guarantee | XOR safe on the full Boolean diamond can be unsafe after restriction |
| Bounded formula size | Defines a finite candidate pool once syntax and variables are fixed | Complexity depends on representation; no new bound proved here |
| CM/LM-supported tests | No extra theorem claimed | A precise compiler/allowed-class definition is still needed |

For a concrete XOR boundary, on diamond states 00<01,10<11 the XOR query has profile 0110 and is safe. Restrict to {01,11}; XOR is 10 on a two-chain and is unsafe. This support is obtained by conditioning the isotone old Y coordinate to 1 (with the conventional second-bit Y). Hence even a familiar formula class does not replace branch-relative safety checks.

The external bit codes used in the gap constructions are supplied attributes; they are not asserted to be the old order-embedding signature coordinates.
