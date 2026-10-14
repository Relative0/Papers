# A1 — Chain safe-query dichotomy and optimal adaptive depth

## Theorem A1

Let the branch-relative current ProLT signature poset be an `n`-element chain, `n>=2`. Suppose an adaptive protocol may choose arbitrary Boolean query profiles, but every query must be **homotopy-neutral before its outcome is conditioned upon**. Then:

1. complete identification is possible in optimal worst-case depth
   \[
   d_{HN}(n)=\lceil\log_2 n\rceil;
   \]
2. among depth-optimal safe protocols, the minimum possible value of the **maximum number of topologically redundant queries on a root-to-leaf path** is exactly `1`;
3. if topologically redundant queries are forbidden entirely—so every query must be both nonredundant and homotopy-neutral—complete identification is impossible for every `n>=2`.

## Proof

### Lower bound

Any yes/no decision tree with `n` leaves has height at least `ceil(log2 n)`.

### Optimal construction

For any current branch with `m>=3` surviving chain elements, ask the alternating query

\[
0101\cdots
\]

in chain order (either parity choice works with the appropriate base convention).

This profile is:

- not constant;
- not nondecreasing, hence not topologically redundant;
- not of the strict antitone-threshold form `1^k0^{m-k}`.

By the exact ProLT chain classification it is therefore **nonredundant homotopy-neutral**. Its two outcomes retain `ceil(m/2)` and `floor(m/2)` chain elements.

Earlier query coordinates are constant on a branch because their outcomes have been fixed, so each child’s branch-relative signature poset remains the induced subchain. Recurse.

When `m=2`, ask profile `01`. It separates the two candidates and is nondecreasing, hence topologically redundant and homotopy-neutral.

The recurrence

\[
D(m)=1+\max(D(\lceil m/2\rceil),D(\lfloor m/2\rfloor))
\]

with `D(1)=0` gives

\[
D(m)=\lceil\log_2 m\rceil.
\]

Every root-to-leaf path uses nonredundant neutral queries until it reaches a two-point branch, followed by exactly one redundant separator. Thus one redundant query per worst path suffices.

### Necessity of a redundant query

Every finite full binary identification tree with at least two leaves contains a **cherry**: an internal node whose two children are leaves. At that node exactly two candidate worlds remain. Since the branch-relative poset is an induced subchain, it is a two-element chain.

The only informative Boolean profiles on a two-chain are `01` and `10` (up to answer complementation). By the ProLT chain theorem:

- `01` is isotone and topologically redundant;
- `10` is the unique strict antitone threshold and is topology-defective.

Therefore a homotopy-neutral separator at the cherry must be the redundant profile `01`. Every safe identification tree has at least one redundant query on some root-to-leaf path. Combining with the construction proves the exact value `1`.

If redundant queries are forbidden, no two-element branch can ever be resolved, so complete identification is impossible. \(\square\)

## Computational verification

- exact DP for `n=2,...,10` agrees with all three conclusions;
- independent constructive/lower-bound verifier agrees through `n=30`;
- `LEGAL_QUERY_PROFILES.csv` contains all 2,044 profiles examined for `n=2,...,10`.

## Novelty discipline

Restricted-question “20 questions,” constrained binary identification, generalized binary search, and poset search are established areas. Therefore the `ceil(log2 n)` information-theoretic depth should **not** be claimed as novel.

What may be a new ProLT-specific corollary is the exact safe-query statement:

> on chains, ProLT homotopy-neutrality permits information-theoretically optimal adaptive identification, but every safe identification tree is forced to spend a redundant query at a two-state cherry; exactly one such redundant query on a worst branch is sufficient and necessary.

The priority search did not find this particular topological admissibility language/result, but the proof is elementary once the ProLT chain theorem is known. Novelty confidence is therefore **moderate, not high**.
