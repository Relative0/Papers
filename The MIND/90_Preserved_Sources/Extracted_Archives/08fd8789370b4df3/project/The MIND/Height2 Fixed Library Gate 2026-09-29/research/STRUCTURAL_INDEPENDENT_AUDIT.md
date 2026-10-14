# Independent structural audit: height-two fixed-library gate

Date: 2026-09-29. This file contains independently checked deductions from the supplied source conventions. Proofs are mathematical proofs; no computation or priority search is claimed here. Novelty remains unassessed except where the construction plainly uses standard linear algebra or graphic matroids.

## 1. Source theorem and conventions

The authoritative one-bit construction is ProLT v0.4, section “Height two: from a boundary matrix to a repair forest.” Height at most two means no strict chain has more than three vertices. A finite post-T0 signature poset is identified with its states, using injectivity of the old signature map.

For a Boolean observation r, the refined order is

    x <=_r y iff x <=_P y and r(x) <= r(y).

Write K=Delta(P), L=Delta(P_r). Vertices are unchanged. Deleted edges D are all strict comparisons (not merely Hasse edges) with bit pattern 10. Deleted triangles A are all three-chains whose word is not nondecreasing:

| Word on x<y<z | Deleted edges | Repair edge |
|---|---|---|
| 010 | yz | root--v_yz |
| 101 | xy | root--v_xy |
| 100 | xy, xz | v_xy--v_xz |
| 110 | xz, yz | v_xz--v_yz |

There is one formal root for every connected component of the coarse poset, including a root with no incident repair edges if needed. Distinct triangles remain distinct graph edges; parallel anchor edges are possible and count as a cycle of length two. Every repair-graph component has at most one root, because no repair edge crosses coarse components and each coarse component has only one root. Rootless repair components can occur.

Over F2, the relative complex is

    0 -> F2^A --B--> F2^D -> 0,

where B is the repair incidence matrix with root rows removed. A 0-by-0 matrix is invertible. The source theorem equates the following for the *inclusion* L -> K:

1. homotopy equivalence;
2. simple homotopy equivalence;
3. a collapse K onto L using deleted edge--triangle pairs;
4. F2 homology equivalence;
5. invertibility of B;
6. repair graph a forest with one root in every component.

The proof is sound: invertibility excludes cycles and rootless components. Conversely, a rooted tree has a nonroot leaf unless it is an isolated root; pair its descent edge with its unique incident deleted triangle. A retained triangle cannot contain a deleted edge, and there are no higher-dimensional cells. Therefore the edge is free, and repeated pruning gives the claimed collapse. The statement is about the specific inclusion, not merely an abstract coincidence of homotopy types.

## 2. Branch cancellation and sufficient state

**Theorem BC.** At every history h of an adaptive protocol beginning with a post-T0 state (S0,P0), the current branch poset is canonically P0 restricted to its surviving support S_h. In particular it remains T0 and has height at most that of P0.

**Proof.** Old coordinates are retained when a query q is appended. On the outcome support T={x in S_h:q(x)=b}, the new coordinate takes the same value b everywhere. Thus for x,y in T,

    x <=_(Phi_h+q) y iff x <=_(Phi_h) y and b<=b
                         iff x <=_(Phi_h) y.

The signature embedding with one constant coordinate appended is a canonical order isomorphism. Iteration gives P0|S_h. Injectivity of the initial signature map persists because its coordinates remain. Restriction also preserves injectivity. QED.

This does not claim that the unconditioned refinement leaves order unchanged. Legality must be tested before the outcome is imposed.

With Q fixed globally, support S is sufficient for a dynamic program. Previously queried tests are constant on S and cannot separate it; retaining them in the global library while excluding currently constant tests yields the same recursion as explicitly removing used tests. No independent accumulated-coordinate state is necessary.

## 3. Exact support restriction theorem

Fix r and T subset P. Let

    D_T = {e in D: both endpoints of e lie in T},
    A_T = {tau in A: all three vertices of tau lie in T}.

**Theorem SR.** The repair graph on P|T is obtained as follows:

1. Keep precisely the descent vertices D_T.
2. Keep precisely the triangle edges A_T.
3. For each old coarse component C, replace its formal root by one formal root for each component C' of P|T contained in C. Attach a retained anchor edge to the root of the unique C' containing its triangle.

No new descent or triangle edge appears. A dependency edge survives exactly when both its descent vertices survive, because those two original comparisons together use all three triangle vertices. An anchor edge additionally requires its third, witness vertex to survive. Thus merely inducing on surviving descent vertices and the old roots is wrong: an anchor witness can disappear while the descent remains, and coarse roots can split.

For the relative matrices,

    B_T = B[D_T,A_T].                                      (1)

Moreover,

    B[D\D_T,A_T] = 0.                                     (2)

**Proof.** A comparison or three-chain survives support restriction exactly when all its vertices do. Its bit values and deleted/retained classification do not change. The incidence entries in a surviving triangle are therefore unchanged. Every edge of a surviving triangle has both endpoints in T, proving (2). Coarse-component containment gives the root rule. QED.

This gives a direct incremental implementation: cache descent endpoints and triangle vertex masks once per query; filter these masks at a support; retain the corresponding rows and columns. Root splitting is needed for graph display, but not for boundary construction or rank. Union-find on retained repair edges and roots gives a linear check in retained cell counts after the masks have been filtered. Across a library of m queries, naive first construction costs O(m n^3); no subcubic global update bound is asserted.

## 4. Exact homological defects and all safety transitions

For a repair graph G, let f(G) be the number of components without a root, and c(G) its ordinary cycle rank, counting multiedges. If d=|D| and a=|A|, then

    rank(B)=d-f(G),
    dim H1(K,L;F2)=f(G),
    dim H2(K,L;F2)=c(G)=a-d+f(G).                          (3)

**Proof.** In a rooted connected component the reduced incidence matrix has full row rank. In a rootless component the incidence rank is one less than the number of vertices. Summing gives the first equation; the relative complex gives the second and third. Equivalently the usual graph formula uses total vertices d+r and components f+r, where r is the number of formal roots. QED.

**Theorem CD.** Support restriction cannot create a triangle-column dependence or a relative H2 class: extension by zero gives an injection

    ker B_T -> ker B.

Consequently c(G_T)<=c(G).

**Proof.** Extend a vector indexed by A_T by zeros on A\A_T. Equation (2) guarantees that B kills it whenever B_T does. This map is injective. QED.

This is stronger than saying root splitting cannot create graph cycles. Cycle creation is impossible under arbitrary induced support restriction, even from an unsafe parent. Existing cycles can survive or disappear; they cannot be newly created.

**Corollary SS.** If r is safe on P, then every retained column is independent, so

    rank(B_T)=|A_T|,
    f(G_T)=|D_T|-|A_T| >= 0,
    r is safe on P|T iff |D_T|=|A_T|.                     (4)

Thus deactivation occurs precisely by losing anchors or dependencies in such a way that a surviving descent cluster is no longer attached to any root. It never occurs through cycle creation. Its relative-H1 defect equals the number of rootless components, and also equals

    (number of deleted parent triangles) -
    (number of deleted parent descent edges).

Here “deleted parent” means lost during support restriction, rather than deleted during observation refinement.

All four safety transitions are now exact:

| Parent -> child | Exact criterion |
|---|---|
| safe -> safe | f(G_T)=0; cycles are automatically absent |
| safe -> unsafe | f(G_T)>0; no new cycle obstruction is possible |
| unsafe -> safe | all surviving cycle dependencies are eliminated and f(G_T)=0 |
| unsafe -> unsafe | a surviving cycle or rootless component remains |

The last two rows do not promise that breaking every cycle is sufficient: support loss can simultaneously destroy needed anchors.

## 5. Hereditary safety and minimal transition examples

**Theorem HS.** A Boolean observation is safe on every induced subposet of a height-at-most-two P if and only if it is isotone on P.

**Proof.** An isotone observation deletes no comparison on any restriction. Conversely, any descent x<y gives an induced two-state chain on which the query deletes the sole edge and has no triangle to repair it. QED.

This is universality over *all* supports. It does not say that every such support is reachable in an arbitrary supplied library, or that every nonisotone safe query must deactivate along every protocol.

Minimal deactivation on a legal branch uses three states. Let P be x<y<z, r=010 and q=011. Both queries are safe initially: r has one anchor triangle and q is isotone. Conditioning q=1 leaves {y,z}; r restricts to 10 and is unsafe. The repair triangle disappears with x, leaving its descent vertex unanchored. No two-state example exists, because a safe query on a two-state chain must be isotone, and all queries on an antichain remain safe.

For the fixed library {r,q}, asking q first therefore dead-ends on its one branch. Asking r first succeeds: the one branch is singleton {y}, while the zero branch {x,z} has q=01 and is safely identified. Thus choosing an initially safe query greedily can destroy feasibility, even when all library tests were initially safe.

Minimal activation including constant outcome restrictions uses two states: x<y, r=10 unsafe, q=01 safe, and either q-outcome is a singleton on which r is safe but constant. This is a formally valid, uninformative activation.

Minimal **nonconstant** activation uses three states if disconnected posets are allowed. Take a<b with c isolated; r(a,b,c)=(1,0,0) is unsafe. The isotone legal query q=(0,1,0) has outcome-zero support {a,c}, an antichain on which r=(1,0) is safe and informative. No two-state nonconstant example is possible because every proper nonempty branch is a singleton.

Connected posets also admit nonconstant activation at three states: take a<b,a<c, r=101, q=011. Here r is unsafe because a<b descends, while q is isotone; the q=1 branch {b,c} is an antichain with r=01, safe and informative. The three-chain itself cannot realize informative activation: its only unsafe words are 100 and 110, and every nonconstant two-state restriction remains a descending comparable pair. Thus chain-only reconnaissance would miss the smallest connected example.

## 6. Matroid interpretation: restriction and an augmented minor

Let M(B) be the represented matroid on actual triangle columns A.

**Theorem MR.** The actual column matroid under conditioning is exactly ordinary restriction:

    M(B_T)=M(B)|A_T.                                      (5)

**Proof.** First restrict columns to A_T. All rows subsequently removed are zero by (2), so their removal changes no column dependencies. QED.

Calling the complete actual triangle set “a basis of its repair matroid” is insufficient for safety. Any rootless tree has independent actual columns, hence its entire edge set is a basis of its own graphic matroid, but its reduced incidence matrix is not surjective onto descent rows. Rootless rows must be represented in the full target dimension.

For correct ambient bookkeeping, append one artificial anchor column s_e for every descent e:

    Bhat=[ B | I_D ].

This is still a graphic representation: add an artificial edge from each descent vertex to its coarse-component root. Its rank is exactly |D|, whether or not actual triangles have roots or cycles.

**Theorem AM.** A query is safe if and only if its actual triangle set A is a basis of M(Bhat). Under support restriction, the augmented matroid is the standard minor

    M(Bhat_T) = ( M(Bhat) / {s_e:e in D\D_T} )
                         \ (A\A_T).                     (6)

Ground labels on retained columns and artificial anchors are identified canonically.

**Proof.** The basis statement is precisely square invertibility of B in a full-rank ambient representation. Contracting a collection of independent unit columns is represented by deleting their coordinate rows and deleting those unit columns. Deleting the absent actual triangle columns leaves [B_T|I_DT]. QED.

Thus two compatible descriptions are available: actual triangle dependencies undergo deletion alone, while a full-rank ambient rooted graphic matroid undergoes contraction of absent artificial anchors and deletion of absent actual triangles. Formal-root splitting changes the graph realization but does not invalidate either represented-matroid equality. This is standard graphic-matroid machinery specialized to the support geometry, not evidence of a new kind of matroid.

## 7. Exact natural-family feasibility: a height-one star

Let P consist of a greatest state z and incomparable leaves X with x<z for every x. Q is an arbitrary fixed Boolean library.

Every height-one query is safe iff it is isotone, because there are no triangles and therefore no way to repair a descent. On a nonsingleton support A union {z}, an informative safe query necessarily has q(z)=1 and nonempty zero set

    Z_q(A)={x in A:q(x)=0}.

The zero outcome is an antichain. The one outcome remains a star containing z.

**Theorem SF.** Repair-safe identification on this star is feasible if and only if:

1. Q distinguishes every two leaves;
2. for every leaf x there exists q in Q with q(x)=0 and q(z)=1.

**Proof.** Identical complete library signatures cannot be distinguished by any protocol. On the z outcome path, x can be eliminated only by an informative safe query of the displayed orientation; this proves necessity of condition 2. Conversely, ask such oriented queries along the z path until their zero sets cover all leaves. Each peeled zero branch is an antichain and can be identified by remaining library tests because condition 1 holds. Earlier queries are constant on that branch, so they cannot be the sole distinguishers of any surviving leaf pair. QED.

This is polynomial-time feasibility by signature comparisons and coverage, though it does not imply polynomial-time optimal depth.

Write O(Z) for ordinary fixed-library optimal depth on leaf subset Z (all queries are safe because Z is an antichain). Then the exact star depth satisfies

    F(empty)=0,
    F(A)=1+min_{q:q(z)=1, Z_q(A) nonempty}
               max( O(Z_q(A)), F(A\Z_q(A)) ),             (7)

with infinity when the feasible set is empty or a necessary branch is unidentifiable. Previously used queries are constant on the support, so the full fixed Q may remain in this formula. The minimum size of an oriented zero-set cover is a lower bound on the z-path length; (7) also accounts for identifying the groups peeled along that path.

## 8. Independent audit of the maximal-gap family

The parent investigation proposed the following family; every step has been checked independently here.

For n>=3 let P_n have a least state a, a greatest state z, and n-2 incomparable intermediate states x_i, with a<x_i<z. This is connected and has height exactly two. Let k=ceil(log2 n). Assign distinct k-bit labels with label(a)=11...1, label(z)=00...0, and distinct other labels to the intermediate states. Let Q contain:

- all k coordinate tests of these labels;
- each peeling test p_v, v != z, equal to zero exactly at v and one elsewhere.

If an identical test appears twice, treat the library as a set; the argument is unaffected.

**Theorem MG.**

    d_ad(P_n,Q)=ceil(log2 n),
    d_RF(P_n,Q)=n-1,
    Delta_RF=n-1-ceil(log2 n).                            (8)

**Proof.** All states have distinct code labels, so querying code coordinates identifies them in k steps; the binary information bound gives equality.

Each code bit is antitone on P_n. On every nonsingleton support containing z that arises by peeling other states, the induced poset remains connected (every surviving state lies below z). A nonconstant antitone bit removes every comparison between its nonempty zero and one sets. Its refinement therefore disconnects a formerly connected complex and is unsafe. A code bit that is constant is uninformative.

Every informative peeling test is safe on these z-containing supports. The test p_a is isotone. For an intermediate v=x_i, if a survives then the sole descent is a<x_i and its sole repairing triangle is a<x_i<z with word 101, giving a one-by-one invertible matrix. If a is absent, p_x_i is isotone. A peeling test whose exceptional state is absent is constant.

Consequently every informative safe query on the z path removes exactly one other state. This requires n-1 queries. Asking the peeling tests successively attains that bound, with every zero branch a singleton. QED.

The penalty is maximal among *finite* penalties on n states. Every finite identifying binary tree with nonconstant tests has depth at most n-1 after irrelevant nodes are removed, because each queried branch strictly reduces candidate-set size. Meanwhile ordinary depth is at least ceil(log2 n). Thus (8) attains the universal upper bound, and the gap is unbounded as n grows.

This family uses fixed query orientation. Automatically adding complements would change the supplied library and invalidate the claimed example: complements of the antitone code bits are isotone and would identify efficiently. Complement closure is an additional hypothesis, not part of the stated primary problem.

The height-one star version, with z assigned the zero code and leaves assigned distinct nonzero codes, has the same exact maximal gap. The height-two version is preferable for this gate because it explicitly uses the 101 repair triangle to certify intermediate peeling tests.

### Complement-closed unbounded-gap family

The parent investigation subsequently supplied a family that removes the polarity caveat for *unboundedness*, although it does not claim the exact maximal gap. Let n=2^k, k>=2, with states all k-bit strings. Put every even-parity string below every odd-parity string, with no other strict comparisons. This is a connected height-one complete bipartite poset. The fixed library contains every coordinate and its complement, and every singleton indicator and its complement.

**Theorem CG.** For this complement-closed library,

    d_ad=k,
    n/4+k <= d_RF <= n-1,
    Delta_RF >= n/4.                                     (9)

For k=2, d_RF=3 and d_ad=2 exactly.

**Proof.** The k coordinates identify all states, and the binary lower bound gives ordinary depth k. For any coordinate polarity, exactly n/4 lower states have value one and exactly n/4 upper states have value zero. Height-one safety is isotonicity, so that polarity can be safe on a support only after all states in at least one of these two forbidden sets have disappeared. Until n/4 states have been removed, no coordinate polarity is legal.

The only remaining available informative queries are singleton indicators or their complements; each isolates exactly one state. An adversary follows the nonsingleton branch of the first n/4 queries. These queries must all be singleton tests, since before the last such query fewer than n/4 states have disappeared. The remaining support has size 3n/4, requiring at least ceil(log2(3n/4))=k more queries even with no safety constraint. This proves the lower bound.

Every remaining vertex has a safe singleton polarity: the singleton indicator is isotone for an upper vertex, and its complement is isotone for a lower vertex. Successive peeling therefore identifies all states in at most n-1 queries, proving finiteness and the upper bound. For n=4 both bounds are three. QED.

The argument establishes linear unbounded penalties even under complement closure, so orientation alone does not explain the phenomenon. The construction is nevertheless already height one; it is an appropriate boundary/control theorem for a height-at-most-two investigation, not evidence that the gap itself needs the nontrivial repair mechanism.

### Exact depth of the complement-closed parity family

The parent investigation subsequently strengthened (9) to an exact recurrence. The proof below was independently hostile-audited, including the residual-library identification and the first-coordinate lower bound.

Let D_k be repair-safe depth for the parity bipartite family on all k-bit strings, with all coordinate polarities and singleton polarities. Include k=1 as the two-state-chain base instance, where D_1=1. Then

    D_k = 2^(k-2)+1+D_(k-1),                  k>=2,
    D_k = 2^(k-1)+k-1,                        k>=1,
    Delta_RF = 2^(k-1)-1 = n/2-1.                        (10)

**Upper bound.** Fix a coordinate q. Peel all n/4 lower vertices for which q=1, using their isotone singleton complements. Query q. It is now safe, since no lower state has q=1. Its q=0 branch is the canonical parity bipartite instance on k-1 free coordinates and n/2 states. The restricted library contains exactly that canonical smaller library, together with constants and duplicates. Its q=1 branch consists of the n/4 upper states with q=1, an antichain. Their k-1 remaining coordinates satisfy one parity equation, so k-2 coordinate tests identify them. Since D_(k-1)>=k-2, the resulting depth is at most n/4+1+D_(k-1).

**Lower bound.** Consider any safe identifying tree, removing constant queries. Follow nonsingleton branches of its singleton queries until the first coordinate query (of either polarity). Suppose t singleton peels occur first. If no coordinate query ever occurs on this path, its length is n-1, which is at least n/2+k-1 because k<=2^(k-1).

Otherwise denote the first coordinate polarity by q. Originally each of its two forbidden sets, lower states with q=1 and upper states with q=0, has n/4 elements. Safety requires at least one forbidden set to have been completely removed. Let E be the coordinate half containing such a removed set, and H the opposite half. If t_H states were removed from H, then

    t >= n/4+t_H.                                       (11)

Before any deletions H is a canonical parity bipartite instance on k-1 coordinates, possibly with the two parity classes interchanged. That interchange is removed by flipping one free coordinate, which preserves the complemented coordinate/singleton library. Let R be the t_H removed states and D(H\R) the optimal depth of the residual instance. Every singleton can be safely peeled from any induced subposet of H by choosing its appropriate polarity. Prepending these t_H safe singleton peels to an optimal protocol for H\R therefore gives

    D_(k-1) <= t_H+D(H\R).                              (12)

The actual tree's q-outcome in H must take at least D(H\R) further queries. Previous singleton queries and q itself are constant on this outcome, so excluding already used tests changes no residual identification capability. Because q is informative, both coordinate outcomes, including H\R, are nonempty. Combining (11)--(12), the tree has depth at least

    t+1+D(H\R) >= n/4+1+D_(k-1).

Together with the upper construction this proves the recurrence. Its solution is (10), and ordinary depth remains exactly k. QED.

For k=2,3,4 this yields exact safe depths 3,6,11. The proof, rather than any finite computation, establishes the full family. Complement closure therefore permits a sharp linear safety penalty in this supplied family. The exact recurrence still relies only on height-one isotonicity and structured library geometry.

## 9. Independently confirmed existing source corrections

The supplied `03_PROLT_PRIMARY_SOURCES/CLAIM_AUDIT_TABLE.csv` already flags v0.5 claim V5-06 as `FALSE/COUNTEREXAMPLE` and V5-07 as `NEEDS_MAJOR_REPAIR`. The check performed in this investigation independently confirms those existing corrections; it is not a newly discovered source defect.

Specifically, v0.5's raw TeX claims odim_P(Q)=dim_2(Q) whenever P is a total order extending Q. As written this is false: take Q=P a two-state chain. The source definition gives odim_P(P)=0, while the classical Boolean order-embedding dimension of a two-state chain is 1. The proposed proof incorrectly treats the biconditional imposed only on P-comparable forward pairs as if it were imposed on every ordered pair. The complexity corollary justified by that equality is therefore unsupported by that argument. The existing audit withdraws the inherited total-order hardness claim and records a separate repaired general-case result; the raw TeX must not override those later corrections.

The same claim-audit table flags V5-09 as `NEEDS_MINOR_REPAIR`: generating the ambient complex only from deleted triangles can omit deleted edges unsupported by any triangle, thereby omitting zero rows of the relative boundary matrix. The recorded repair is to take G=K^(1) union the deleted triangles and R=the retained edges, so every deleted edge remains represented. This correction is consistent with the full-descent-row and ambient-matroid bookkeeping in the present audit.

These inherited corrections do not affect the v0.4 repair theorem, branch cancellation, restriction dynamics, or the current fixed-library model. They are preserved here for source provenance; repairing observation dimension theory is outside this gate.

## 10. Hostile verdict and priority limits

The dynamic program is an ordinary restricted decision tree with a support-dependent legal action set. Its recursion alone is not a contribution. The useful structural content proved above is the exact restriction law, the one-sided cycle monotonicity and rootless-component deactivation formula, the explicit augmented graphic-matroid minor, and the exact maximal-gap family on a connected height-two class. All follow with short proofs from the source representation; none should be called novel without a theorem-level literature audit.

An especially useful adversarial check is to keep three notions distinct: one-bit safety on the current conditioned support, sequential safety of unconditioned accumulated refinements, and simultaneous block safety. The branch-cancellation theorem only concerns the first adaptive model and does not transfer v0.4 graph conclusions to arbitrary multi-bit block refinements.
