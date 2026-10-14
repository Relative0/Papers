# H4: exact fixed-library feasibility and depth

Fix P0 and the oriented library Q. For S subseteq S0 let

  L(S)={q in Q : q is nonconstant on S and RF-SAFE(P0|S,q)}.

Let S_qb={x in S:q(x)=b}. With infinity allowed, define

  D(S)=0,                                      if |S|<=1;
  D(S)=1+min_(q in L(S)) max(D(S_q0),D(S_q1)), otherwise.

The minimum of an empty set is infinity. A legal root whose child is infeasible also has infinite value; nonempty L(S) alone does not imply feasibility.

## Correctness

Every safe identifying tree begins with some q in L(S), then identifies each outcome support. Branch cancellation makes these induced-support subproblems exactly the stated ones. Conversely, attach optimal child trees below any legal q whose children are feasible. Induction on |S| proves the recurrence and reconstructs an optimal tree.

There is no missing remaining-query factor: any previously asked query is constant on S and is already excluded from L(S). For a fixed library the support bitmask is sufficient. Complement availability and costs must never be silently changed.

Ordinary depth D_ad uses all nonconstant library queries in place of L(S). Its feasibility is simply pairwise separation by Q. Safe feasibility F(S) replaces min/max with the Boolean rule

  F(S)= OR_(q in L(S)) [F(S_q0) AND F(S_q1)],

with F(S)=true for |S|<=1.

For nonnegative fixed query costs c(q), replace the leading 1 by c(q). The present computations use unit costs.

## Bounds and state space

If n=|S0|>=2 and identification is feasible, every reduced binary tree has exactly n singleton leaves and n-1 internal nodes. Therefore

  ceil(log2 n) <= d_ad <= d_RF <= min(m,n-1).

No useful query repeats on a path. At most 2^n supports need be memoized; reachable supports are intersections of supplied outcome fibers, often much fewer. A straightforward upper bound is O(2^n m n^3) time, including a fresh safety calculation, and exponential support storage. Precomputed masks/cells and the restriction theorem improve constants and permit exact incremental updates; this is not a polynomial general solver.

The single-query graph predicate is polynomial, but composing it with a support-dependent min-max decision tree is standard planning/decision-tree machinery. The recurrence itself is not a novelty claim.

## A useful hereditary-action lemma

Suppose a legal test remains legal on every smaller support. If an identifying legal tree exists at S, then ANY legal nonconstant q at S can be asked first without destroying feasibility. Restrict the existing tree to each outcome support of q; remove constant nodes. Every surviving query is legal by heredity.

For height at most one, RF safety is isotonicity and has this hereditary property. Greedily choose any legal nonconstant query at every node; report failure only at a nonsingleton leaf without a legal split. The resulting tree has at most n-1 internal nodes, so this decides RF-IDENT in polynomial time (e.g. O(m n^3) with direct order scans). Optimization of depth is still difficult, even on antichains.

At actual height two the three-chain {010,011} counterexample in QUERY_ACTIVATION_DEACTIVATION.md defeats this greedy lemma. General height-two RF-IDENT complexity is left open here.
