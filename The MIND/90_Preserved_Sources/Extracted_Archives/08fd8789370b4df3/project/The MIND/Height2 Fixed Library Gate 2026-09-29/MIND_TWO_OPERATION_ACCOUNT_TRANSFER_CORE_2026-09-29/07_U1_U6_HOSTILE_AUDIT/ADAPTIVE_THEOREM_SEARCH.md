# Constrained-adaptive theorem search

## Gate result

The U1–U6 framework survives after two repairs: U2 needs a more accurate quotient statement, and U4 must be described as an exact triangle/LES rather than a direct-sum decomposition. The strongest adaptive search therefore focused on the exact ProLT chain classification.

## Hostile negative result N1 — homotopy-neutrality alone is too weak

Let `P` be any finite T0 poset with `n` candidate worlds, and suppose arbitrary Boolean queries are available. There is an adaptive identification protocol of worst-case depth

\[
\lceil\log_2 n\rceil
\]

using **only topologically redundant (isotone) queries**.

### Proof

Choose a linear extension of the current induced poset. A suffix of a linear extension is an upset: if `x` is in the suffix and `x<=y`, then `y` appears no earlier than `x`, so `y` is also in the suffix. Therefore its indicator is isotone and adding it is topologically redundant.

Choose a suffix whose size is as close to half of the current support as possible and measure that query. Each branch has at most `ceil(m/2)` candidates. Conditioning preserves the induced finite poset, so repeat. The ordinary binary-information lower bound proves optimality.

### Consequence

A constraint of the form “each query must be homotopy-neutral” cannot, by itself, create a worst-case query-complexity gap if the Boolean query pool is unrestricted.

This negative theorem sharply narrows the meaningful adaptive program.

---

## Preferred chain regime

The existing ProLT chain theorem classifies a one-bit profile `b1...bm` on an `m`-chain:

- redundant exactly when the profile is nondecreasing `0*1*`;
- topology-defective exactly for a strict antitone threshold `1^k0^{m-k}`, `1<=k<m`;
- every other profile is nonredundant but homotopy-neutral.

At an adaptive branch, all earlier query bits are constant on the surviving support, so the current induced poset remains a chain. Hence this classification can be applied recursively.

## Computation

Dynamic programming was performed for chain sizes 2 through 10 over the exact legal query language. Independent closed-form verification was run through size 30.

Results for every `2<=n<=10`:

\[
d_{HN}(n)=\lceil\log_2 n\rceil,
\]

minimum worst-path redundant-query count among depth-optimal protocols is `1`, and identification using **only nonredundant homotopy-neutral queries** is impossible.

The constructive policy uses an alternating profile `0101...` whenever the current chain has at least three elements. It is nonconstant, non-isotone, and not a strict antitone threshold, hence is nonredundant homotopy-neutral. It splits the chain into `ceil(m/2)` and `floor(m/2)` survivors. On a final two-element chain, the informative safe profile is `01`, which is redundant.

These computations suggested A1, proved in `ADAPTIVE_THEOREM_FINAL.md`.
