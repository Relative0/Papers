# H3: activation, deactivation and their minimal witnesses

Queries are tested before conditioning. "Informative transition" means the target query remains nonconstant on the child support. A reachable witness additionally specifies a legal conditioning query.

## Activation: three states, connected height one

Take P with a<b and a<c, and query r=(1,0,1) in the order (a,b,c). Its only descent is a<b, with no repair triangle, so its relative matrix is 1-by-0 and it is unsafe.

The isotone query q=(0,1,1) is legal. On q=1 the support is {b,c}, an antichain; r=(0,1) is nonconstant and safe with a 0-by-0 matrix. Thus the fixed library {q,r} identifies all three states safely in depth two, although its initially safe subset {q} does not separate b from c.

This shows a real use of initially unavailable tests. Activation is not merely a query becoming constant.

## Deactivation: three-state chain, actual height two

Take x<y<z, r=010 and q=011. Initially r has the sole descent yz and sole deleted triangle xyz of word 010. Its matrix is [1], and the repair graph is a rooted one-edge tree.

The isotone q is safe. Conditioning on q=1 leaves y<z, where r=10. The matrix becomes 1-by-0: the descent vertex survives, its anchor triangle does not. Hence r becomes unsafe.

This also disproves an arbitrary-legal-query greedy feasibility strategy at height two. The library {010,011} is feasible by asking 010 first and then 011 on its {x,z} branch. Asking legal query 011 first strands the {y,z} branch.

## Minimality and hereditary safety

Fewer than three states cannot give a useful transition under proper restriction, since the child has at most one state. Both witnesses above have three states and are therefore vertex-minimal among informative transitions, even with legal one-step reachability required.

If one allows a constant target query on the child, unsafe 10 on a two-chain becomes trivially safe on a singleton. This is a different, uninformative minimum and should not be confused with query activation useful for identification.

For any finite poset, an observation is safe on EVERY induced support iff it is isotone:

* If isotone, it deletes no comparisons on any support.
* If not, there is a descent x<y. Restrict to {x,y}; refinement deletes the sole edge, separating a connected interval into two points.

Thus universal hereditary safety is exactly redundancy. This does not say a fixed library can reach every offending two-point support.

On height at most one, safety at a given support already means isotonicity there and is hereditary below that support. At height two, safe nonredundant queries introduce the first deactivation phenomenon.

## Nonadaptive comparisons, defined explicitly

The activation example separates the adaptive conditioning model from three full-carrier benchmarks:

1. An initially individually safe separating sublibrary does not exist.
2. A sequence that refines the full carrier without conditioning, requiring each prefix inclusion safe, cannot identify using {q,r}: q is redundant and leaves r unsafe.
3. A jointly safe separating block does not exist in this library: every separating block contains r and deletes the sole descending edge a<b without any triangles.

These are the coordinatewise, sequential-prefix and simultaneous notions distinguished in v0.5. They are not interchangeable. This example does NOT separate adaptive query choice from a predetermined schedule that is allowed to condition after every answer and omit constant tests: the schedule q then r works in that latter model. No broader adaptivity advantage is claimed.
