# CM Four-Corner Defect Localization

## Sound inference from a witness

For a failed cut `A|B`, let a witness use row assignments `a0,a1` and column assignments `b0,b1`. Define support sets

- `U={x in A : a0(x) != a1(x)}`;
- `W={y in B : b0(y) != b1(y)}`.

If the four-corner determinant is nonzero, then some semantic prime factor block intersects both `U` and `W`.

This supports a **hyperedge constraint** `(U,W)`: at least one prime block crosses these two support sets.

## Pairwise edge rule

Only when `|U|=|W|=1` is a direct must-link pair sound without further inference.

## Counterexample to universal pairwise localization

`f_n=1` only on `0^n` and `1^n` is semantically prime, but every two-variable fixed-context slice has at most one satisfying corner and therefore rank <= 1. No pairwise rank-two witness exists.

For a cut `A|B`, a nonzero minor requires the two row assignments to be `0^A,1^A` and the two column assignments to be `0^B,1^B` (up to swapping), hence the witness varies all variables. This defeats any universal claim that witness minimization reaches a variable pair.

## Research direction

Use defect supports as hyperedges and optimize vtrees so high-frequency co-defect supports remain locally clustered. Do not project a support hyperedge to all pairwise edges; that would create false must-links.

A useful theorem remains open: query complexity of shrinking a support hyperedge under bounded defect-support width, bounded carrier block size, or bounded interaction treewidth.
