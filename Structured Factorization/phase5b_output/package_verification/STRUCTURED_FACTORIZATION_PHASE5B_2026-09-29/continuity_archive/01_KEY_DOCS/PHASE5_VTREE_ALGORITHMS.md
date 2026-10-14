# Vtree Algorithms

## A. Carrier hard-lock

Build a subtree for each carrier block and combine block subtrees by balanced, size-weighted, or interaction-weighted merges.

**Warning:** exact theorem shows crossing carrier/semantic blocks make perfect semantic alignment impossible under the hard-lock constraint.

## B. Syntax-component vtree

For CNF, compute connected components of the primal/clause interaction graph. Make each component a subtree, then recursively partition within components.

This is an established preprocessing idea and should be a baseline, not a novelty claim.

## C. Defect-hypergraph adaptation

1. Start from a baseline tree.
2. Test exposed cuts.
3. For each failed cut, request/minimize a four-corner witness.
4. Record support hyperedge `(U,W)`.
5. Propose local rotations that reduce separation of repeatedly co-occurring support sets.
6. Accept only if the exact factor-exposure/residual-cost objective improves.

Never turn a general defect support into all pairwise must-link edges.

## D. Hybrid

Use syntax components as certified hard modules; carrier as soft cohesion unless compatible; CM defect supports as learned hyperedges; local rotations as the search mechanism.

## E. Exact controls

- fixed balanced tree;
- random tree;
- exhaustive all-vtree factor-exposure optimum for tiny n;
- oracle prime-aligned tree.

The exhaustive exposure optimum and oracle-aligned tree should agree on the maximum direct-factor count, but they differ operationally: the former scores trees using exact cut tests, while the latter directly uses `Pi_f`.
