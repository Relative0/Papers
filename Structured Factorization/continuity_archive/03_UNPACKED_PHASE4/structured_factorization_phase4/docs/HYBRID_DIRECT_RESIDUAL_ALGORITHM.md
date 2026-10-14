# Hybrid Direct-Then-Residual Exact Factorization

## Contract

Input:

- simplicial carrier prime partition \(\Pi_K\) (or minimal nonfaces from which it is computed);
- semantic representation in one of the supported forms:
  - support-disjoint/read-once CM/LM operator tree;
  - compressed SDD with vtree \(T\);
  - general CNF/circuit for fallback;
- exact four-corner SAT oracle using one persistent selector-controlled base encoding.

Output: the unique finest simultaneous carrier/semantic AND-factor partition.

## Algorithm

### Case A — read-once CM/LM tree

1. Compute the exact semantic prime partition \(\Pi_f\) by signed CM-rank recursion.
2. Return
   \[
   \operatorname{LCC}(\Pi_K,\Pi_f).
   \]

No SAT is required.

### Case B — compressed SDD

1. Compute the finest vtree-laminar semantic partition \(\Pi_T\) by the compressed-cut recursion.
2. Form
   \[
   \Pi_0=\operatorname{LCC}(\Pi_K,\Pi_T).
   \]
3. Since \(\Pi_0\) is a valid simultaneous factorization, process each block independently.
4. Within each block, use the persistent four-corner SAT oracle to test only unions of carrier-prime subblocks that remain inside that block.
5. Recursively split on UNSAT defect queries until no further valid split exists.

Return the union of the residual prime blocks.

## Exactness lemma

Let \(\Pi_*\) be the finest simultaneous partition. If \(\Pi_0\) is any valid simultaneous partition, then \(\Pi_*\) refines \(\Pi_0\). Therefore no block of \(\Pi_*\) crosses two blocks of \(\Pi_0\), and residual search may be performed independently inside the blocks of \(\Pi_0\).

This makes direct extraction a **safe decomposition certificate**, not merely a heuristic pruning rule.

## Practical implication

A good vtree does not need to expose every factor to be useful. Every factor it certifies reduces the residual cut universe exactly. The unresolved part can still be solved by the same SAT oracle, preserving correctness.
