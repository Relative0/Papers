# Independent complexity audit

Date: 2026-09-29. Model: explicitly listed finite poset P on n vertices, height at most two (chain length at most three), and an explicitly listed n by m Boolean observation table Q. Observations are oriented Boolean functions; their complements are available only when supplied. Safety is checked before conditioning. Results below do not address succinctly represented exponentially large supports.

## Verified complexity statements

| Problem | Status established here | Qualification |
|---|---|---|
| RF-SAFE(P,q) | Polynomial time | O(n^3) enumeration and graph traversal suffice. |
| RF-IDENT(P,Q) | In NP; exact exponential DP | General NP-hardness is **not** established. |
| RF-DEPTH(P,Q,k) | NP-complete | Already on antichains; explicit reduction below. |
| RF-IDENT on height-at-most-one posets | Polynomial time | Hereditary safety makes arbitrary legal-query greedy recursion complete. |
| RF-DEPTH parameterized by n | FPT | Support DP has at most 2^n states. |
| RF-DEPTH parameterized by k | FPT | Reject n>2^k; otherwise the preceding DP gives a doubly exponential parameter dependence. |

These are mathematical deductions, not benchmark claims.

## C1. Polynomial legality and verification

List comparable pairs and three-element chains. For each query retain the descent edges and deleted triangles. This needs O(n^3) time using a relation matrix. The repair graph has O(n^2) nonroot vertices and O(n^3) edges; ordinary traversal detects cycles and rootless components in time linear in its size. Thus RF-SAFE is polynomial, with a conservative O(n^3) bound after the input relation is available. Matrix rank provides an independent polynomial check, although dense elimination is slower.

A successful identification tree can be pruned to make every internal query nonconstant on its support. Determinism then gives exactly one leaf per initial candidate, hence n leaves and n-1 internal vertices. Repeated tests on one path are constant and disappear. A certificate names a supplied query at each internal vertex and a candidate at each leaf. Propagate supports, verify each query's legality, and check singleton leaves. This takes polynomial time, and the largest root-to-leaf query count verifies a depth bound. Consequently both RF-IDENT and RF-DEPTH lie in NP. Any finite optimum is at most min(m,n-1).

## C2. The exact DP is a standard support-state recursion

Branch cancellation gives the current poset P[S]. Previously asked tests are constant on S, so an unused-test mask is unnecessary in this fixed-library, no-resource-cost model. Write

L(S)={q in Q: q is nonconstant on S and RF-SAFE(P[S],q)}.

Then D(S)=0 for |S|<=1, and otherwise

    D(S) = 1 + min_{q in L(S)} max(D(S intersect q^-1(0)),
                                      D(S intersect q^-1(1))).

An empty minimum means infinity. This is proved by considering the root query of any valid tree and, conversely, joining optimal child trees. The Boolean feasibility recursion replaces min/max by existential choice of a test and conjunction over its two children.

Scanning all supports and tests gives the conservative bound O(2^n m n^3) time and O(2^n) value storage, apart from input and temporary legality data. Only supports realizable as intersections of query outcome cells need evaluation. There are at most min(2^n,3^m) such supports; this is an upper bound, not an assertion that all are legally reachable. These bounds imply FPT in n and in m. For depth parameter k, the information bound rejects n>2^k, giving time O(2^(2^k) m 2^(3k)) on the remaining instances. This generic consequence should not be presented as a sophisticated parameterized algorithm.

## C3. RF-DEPTH is NP-complete, including an explicit threshold reduction

On an antichain, every observation leaves the order complex unchanged. RF-DEPTH therefore contains ordinary fixed-library minimum worst-case identification depth exactly. The primary minimum-height source is [Laber and Nogueira, 2004](https://www2.ic.uff.br/~loana/decisiontree.pdf). Their objective is maximum path length. In contrast, the principal theorem of [Hyafil and Rivest, 1976](https://people.csail.mit.edu/rivest/pubs/HR76.pdf) concerns total external path length / expected tests. Those objectives must not be silently interchanged.

For a direct many-one proof, start from Set Cover (U,C,k), with |U|>=2 and union C=U. Put d=ceil(log2 |U|), z=d+1. Make z disjoint copies of U and one sentinel *. For each set in each copy supply its membership test and balanced binary identification tests supported entirely inside that set. All tests are zero at *. Let tau be the minimum cover size. On the sentinel path, true sets of queried tests must cover every other object. Each such set lies in one original set in one copy; therefore that path has at least z tau queries. Conversely, query a minimum cover in each copy along the zero path, and use the balanced auxiliary tests on each positive branch. This constructs a tree of depth at most z tau+d. Thus the threshold K=zk+d accepts tau<=k and rejects tau>=k+1, since z(k+1)>zk+d. The construction is polynomial. Taking the antichain on these objects completes the reduction. Together with C1 this proves NP-completeness.

This sentinel construction is an explicit elementary amplification of the set-cover approach, not a new complexity contribution.

## C4. RF-IDENT hardness does not follow

Ordinary unbounded-depth feasibility is equivalent to pairwise distinct rows of the supplied test table. On an antichain that condition is also sufficient for repair-safe feasibility. Therefore the antichain reduction proves no hardness for RF-IDENT. In particular, NP-completeness of depth does not imply NP-completeness of unrestricted feasibility. A general RF-IDENT classification needs a separate reduction or algorithm; it remains open in this gate.

There is also no justification for importing PSPACE- or EXPTIME-hardness from succinct contingent planning: here the states and tests are explicit, successful trees have polynomial-size certificates, and every informative observation strictly shrinks its outcome supports.

## C5. Exact polynomial feasibility under hereditary legality

Suppose a legality predicate has the property that a test legal on S stays legal on every subset T of S (constants may be pruned). If S has a successful tree, any currently legal nonconstant test q may be asked first: restrict that successful tree to either q outcome, delete empty branches, and suppress constant queries. Every surviving query remains legal by heredity. Thus both outcome supports remain feasible.

Consequently, recursively choose any legal nonconstant test, and fail only if a nonsingleton support has none. This is a complete feasibility algorithm. There are at most n-1 internal nodes, so it runs in polynomial time when legality does. This statement concerns feasibility, not optimal depth.

For height-at-most-one posets there are no triangles. The relative boundary can be invertible only when there are no descents, so safety is precisely isotonicity. Isotonicity is hereditary under induced restriction. RF-IDENT on this entire class, including crowns and fences without three-element chains, is therefore polynomial. A direct implementation scans m tests against O(n^2) relations at each of O(n) nodes: O(m n^3) is sufficient. This is a generic hereditary-action argument specialized to ProLT.

## C6. Exact complement-closed parity-family depth

This strengthens the caution that the sharp star-family gap disappears when complements of its code tests are added.

Let k>=1 and n=2^k. The vertices are all bit words x in {0,1}^k. Let L be the even-parity words and U the odd-parity words, and put every relation l<u for l in L, u in U. This defines a connected complete bipartite height-one poset. Supply all coordinate tests and their complements, together with all singleton indicators and their complements. The library is complement-closed. Write D_k for its repair-safe adaptive depth. Then

    D_k = 2^(k-1) + k - 1,       d_ad = k,
    Delta_RF = 2^(k-1)-1 = n/2-1.

**Base case.** D_1=1: the order is a two-chain and the ascending coordinate is safe.

**Upper recurrence.** For k>=2, fix a coordinate j and safely peel its n/4 lower vertices with x_j=1, using complements of their singleton indicators. The coordinate query x_j is then isotone. Its zero child is a full instance P_(k-1): fixing a bit either preserves parity or reverses it, and flipping one remaining coordinate corrects the latter case while preserving the complement-closed library. Its one child is an antichain of n/4 upper vertices, identifiable by k-2 remaining coordinate tests because their parity determines the last coordinate. Therefore

    D_k <= n/4 + 1 + D_(k-1).

**Lower recurrence.** Prune constant queries. Follow nonsingleton outcomes of singleton tests until the first coordinate test (in either polarity). If no coordinate occurs, this path uses n-1 queries, which is at least the claimed value. Otherwise let t be the number of preceding singleton deletions. Each coordinate polarity has a descent graph K_(n/4,n/4). Its safety forces one whole forbidden layer/bit cell to have been removed, in a bit half E. Let H be the other bit half, initially a canonical P_(k-1), and let t_H count its removed vertices. Then t>=n/4+t_H.

Let R be the survivors in H. Its inherited library is the smaller canonical library restricted to R, plus constants and duplicates. Every vertex of H can be safely peeled: use the complement of a lower vertex's singleton indicator, or an upper vertex's singleton indicator. Prefixing such peels for H minus R to an optimal protocol on R proves

    D_(k-1) <= t_H + D(R).

The original tree's H child requires at least D(R) additional queries. Hence its worst-case depth is at least

    t + 1 + D(R) >= n/4 + 1 + D_(k-1).

An informative first coordinate has R nonempty; the prefix bound also remains valid for R empty with D(empty)=0. Earlier asked singleton tests and the chosen coordinate are constant on R, so excluding repeated tests makes no difference. Combining the recurrences and D_1=1 yields D_k=2^(k-1)+k-1. Ordinary depth k follows by asking coordinates, with the binary information bound giving equality.

This is an exact linear additive-gap theorem, not merely a computational pattern. It uses height one, so it cannot by itself demonstrate a phenomenon unique to height-two repair triangles. Independent finite computation is useful as a bug check, but the recurrence proof is the theorem.

## Previously recorded collateral source defect preserved

The transferred `03_PROLT_PRIMARY_SOURCES/CLAIM_AUDIT_TABLE.csv` already records V5-06 as `FALSE/COUNTEREXAMPLE` and V5-07 as `NEEDS_MAJOR_REPAIR`. ProLT v0.5, Proposition `prop:2dim`, states odim_P(Q)=dim_2(Q) whenever P is a total order extending Q. The independent check here confirms the recorded defect: take P=Q to be a two-element chain; odim_P(P)=0 by definition, whereas dim_2(P)=1. The proof incorrectly treats the oriented comparisons supplied by a linear order as constraints on both ordered directions. The following stated NP-completeness corollary is unsupported by that proposition, and the table explicitly withdraws the inherited total-coarse-order hardness. This is a preserved known correction, not a new flaw discovered by this gate. The current RF-DEPTH proof does not use any observation-dimension complexity claim.

## Remaining complexity gate

The highest-value unresolved classification is RF-IDENT on height exactly two with a supplied library, where legal-query deactivation defeats the hereditary greedy proof. Keep it open until a complete reduction or polynomial algorithm is independently checked. Do not promote the standard support DP, NP membership, or antichain depth hardness to the principal research contribution.
