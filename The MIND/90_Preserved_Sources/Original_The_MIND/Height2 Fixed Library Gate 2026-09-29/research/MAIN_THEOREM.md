# Main result: restriction controls repair-safe adaptive identification

## H8: support restriction theorem and adaptive consequences

Let P be a finite post-T0 poset of height at most two, Q a fixed library of oriented Boolean tests, and r in Q. For a support S write D_r(S) for descent pairs, A_r(S) for deleted three-chains, and B_r(S) for the F2 relative boundary.

1. At every history h the branch poset is canonically P|S_h. Hence the current support alone determines the future unit-cost subproblem.
2. For T subseteq S,

     B_r(T)=B_r(S)[D_r(T),A_r(T)],

   and all entries of retained columns in removed rows are zero.
3. Therefore the actual triangle-column matroid is obtained by deletion, and relative H2 cannot increase. After adjoining artificial root-edge unit columns, restriction is exactly contraction of removed artificial edges plus deletion of removed actual triangle columns.
4. If r is safe on S, it is safe on T iff |D_r(T)|=|A_r(T)|. Any failure is precisely a rootless repair component, with relative H1 dimension |D_r(T)|-|A_r(T)|. It cannot arise by creation of a new triangle-column dependence.
5. Safety is not hereditary: a legal restriction can activate or deactivate an informative test on three states, and three is minimal.
6. The safe identification depth is given exactly by the support min-max recurrence. A legal choice need not preserve future feasibility at height two, unlike the hereditary height-one regime.

### Proof

Part 1 is coordinate cancellation on an answer fiber (BRANCH_CANCELLATION.md). Parts 2-4 follow from induced-chain restriction, reduced graph incidence, and extension of kernel vectors by zero (REPAIR_GRAPH_DYNAMICS.md and MATROID_INTERPRETATION.md). Part 5 is witnessed by the connected fork activation and chain anchor-loss examples (QUERY_ACTIVATION_DEACTIVATION.md). Part 6 follows by induction on support size; the library {010,011} on a three-chain disproves arbitrary-safe-first feasibility preservation (FIXED_LIBRARY_IDENTIFICATION.md).

## Sharp consequences for fixed libraries

For every n>=3 there is a connected poset of actual height two and a fixed library with

  d_ad=ceil(log2 n),  d_RF=n-1.

This attains the universal largest finite additive gap. For complement-closed libraries, a connected height-one family with n=2^k has the exact depths

  d_ad=k,  d_RF=n/2+k-1,  gap=n/2-1,

for k>=1. Both families have unbounded depth ratios. Complete proofs, including polarity limitations and the recurrence proving the second formula, are in ADAPTIVE_DEPTH_THEORY.md.

## Correctness versus novelty

These are proved statements, with bounded computation used as an independent check rather than a substitute for proof. The inherited v0.4 repair-forest theorem is the essential topological input.

The support recurrence, graph-incidence algebra, matroid minors, information bounds and generic query-restriction penalties are established mathematical tools. The best candidate contribution is the precise support-restriction/anchor-loss theorem for this ProLT legality rule and its consequences for activation and feasibility. The extremal examples are useful exact corollaries, but do not by themselves establish a new height-two decision-tree theory.

Novelty confidence is moderate-to-low pending a focused comparison of this specific theorem with prior work. No claim of priority or publication readiness is made from the bounded search.
