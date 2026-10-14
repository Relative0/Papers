# H7: complexity audit

Input representation: an explicit n-state order relation and an explicit n-by-m Boolean query table. Succinct exponentially large carriers are outside scope.

| Problem | Established status |
|---|---|
| RF-SAFE | Polynomial; O(n^3) chain enumeration plus graph traversal suffices |
| RF-IDENT, general height <=2 | In NP; exact exponential support DP; hardness unresolved here |
| RF-DEPTH | NP-complete, already on antichains |
| RF-IDENT, height <=1 | Polynomial by hereditary safety and greedy feasibility |
| RF-DEPTH parameter n | FPT via O(2^n m n^3) support DP |
| RF-DEPTH parameter depth k | FPT by rejecting n>2^k then using the n-parameter algorithm; a crude doubly exponential dependence |

A successful reduced tree has n singleton leaves and n-1 internal nodes. Each node names a supplied query. Propagating its support, verifying one-bit safety and computing the maximum path length takes polynomial time. This proves the NP memberships.

On an antichain every query is safe, so RF-DEPTH contains ordinary minimum worst-case test-tree height. The relevant primary source is [Laber and Nogueira, minimum height decision trees](https://www2.ic.uff.br/~loana/decisiontree.pdf). The independent audit also supplies a complete sentinel-and-copy Set Cover reduction with a separating threshold, avoiding dependence on an ambiguous objective citation.

The main theorem of [Hyafil and Rivest](https://people.csail.mit.edu/rivest/pubs/HR76.pdf) concerns external path length/expected tests. It is not silently substituted for worst-case depth.

Antichains DO NOT prove RF-IDENT hard: there ordinary feasibility is simply distinct query signatures. General height-two RF-IDENT requires a separate argument and is deliberately left open. Nor is PSPACE hardness from succinct contingent planning inherited by this explicit polynomial-certificate model.

Height-one RF-IDENT is polynomial because a currently safe test stays safe on every descendant. Restrict any successful tree to the outcomes of an arbitrary safe query, and prune constants; it remains successful. The resulting choose-any-legal algorithm has at most n-1 internal nodes. The height-two three-chain {010,011} demonstrates precisely why this proof stops.

For nonnegative fixed query costs, the exact recurrence extends by replacing 1 with the selected cost. No new approximation theorem, weighted complexity classification, or treewidth FPT result is established.

Detailed independent proofs, the explicit hardness reduction and parameter bounds are in COMPLEXITY_INDEPENDENT_AUDIT.md. These are algorithmic consequences and standard hardness transfers, not the principal novelty claim.
