# H5: sharp fixed-library penalties

All depths are worst-case, unit-cost, and use only the supplied oriented observations.

## Smallest impossibility and finite gaps

On the two-chain x<y, the one-query library {10} distinguishes both states ordinarily but is unsafe. Thus d_ad=1 and d_RF=infinity. One state is always identified, so this is vertex-minimal.

If both depths are finite, binary-tree bounds give

  0 <= d_RF-d_ad <= n-1-ceil(log2 n).

This upper bound is zero for n<=3. The next construction attains it for every n>=3 and gives the smallest strict finite gap at n=4.

## Exact maximal gap on connected, genuine height-two posets

For n>=3, let P_n have bottom a, top z, and n-2 incomparable middle vertices x_1,...,x_(n-2), with every a<x_i<z. Include the transitive comparison a<z. Put k=ceil(log2 n).

Assign distinct k-bit codes:

  c(z)=0,
  c(a)=2^k-1,
  c(x_i)=i,  1<=i<=n-2.

Let Q_n consist of the k coordinate code tests r_j and n-1 peeling tests p_v for v!=z, where p_v(v)=0 and p_v(w)=1 for w!=v. This is a fixed library established before the protocol.

Then

  d_ad(P_n,Q_n)=k,
  d_RF(P_n,Q_n)=n-1.

Proof of ordinary depth: ask the k code bits; the codes distinguish all states. The binary information bound makes this optimal.

Proof of safe upper bound: peel the non-z states, following the value-1 branch until only z remains. The 0 branches are singletons. The test p_a is isotone. A middle peel p_x has at most the single descent a<x on a support containing z; if a is present, its unique repair triangle a<x<z has word 101 and boundary [1]. If a is absent, the test is isotone. Thus the whole peeling tree is legal.

Proof of safe lower bound: follow the history of hidden state z. Every remaining support contains z and is connected when it has more than one vertex. Each code bit is antitone on P_n and on every induced support. A nonconstant antitone observation on a connected poset removes all comparisons between its two answer sets, so its refinement disconnects the component and is unsafe. Consequently only peeling tests can be informative on this path, and each removes exactly one other state. There must be n-1 queries.

The family attains the largest possible finite additive gap. Its ratio (n-1)/ceil(log2 n) also tends to infinity. The same sharp phenomenon already occurs on a height-one star, so it is not uniquely caused by repair triangles.

Polarity caveat: this particular library is not complement-closed. If the complements of its code bits are supplied, those complements are isotone and achieve depth k.

## Exact unbounded penalty with complement closure

There is a separate connected family which removes that caveat.

Let n=2^k, k>=2, with states the k-bit strings. Let L be the even-parity strings and U the odd-parity strings. Make P the complete bipartite height-one order l<u for every l in L,u in U. Include in Q every coordinate bit and its complement, and every singleton indicator and its complement. Thus Q is complement-closed and supplied explicitly.

Ordinary identification has depth k. Safe identification is finite, since every singleton split has an isotone orientation: use the complement of a singleton indicator for a lower vertex, or the indicator for an upper vertex.

For either polarity of a coordinate, exactly n/4 lower vertices carry 1 and n/4 upper vertices carry 0. At height one safety means no descent. Because the order is complete bipartite, making that polarity safe requires eliminating ALL the former group or ALL the latter group. At least n/4 vertices must therefore have been removed before any coordinate polarity is legal.

Follow the nonsingleton outcome of each singleton split for the first n/4 queries. Before that many removals, no coordinate is available, so these singleton splits are forced. The residual support has 3n/4 states, requiring at least ceil(log2(3n/4))=k additional queries, even without safety restrictions. Hence

  k+n/4 <= d_RF <= n-1,
  d_RF-d_ad >= n/4.

The lower bound can be sharpened to an exact solution:

  d_RF=2^(k-1)+k-1=n/2+log2(n)-1,
  d_RF-d_ad=n/2-1.

Here is a proof, rather than an extrapolation from the computed depths 3,6,11 at n=4,8,16.

Write D_k for this family's safe depth and extend the definition to k=1, where a two-chain has D_1=1. For k>=2, peel all n/4 lower vertices whose first bit is 1, using their safe singleton-complement tests. The first coordinate is now isotone. Its 1 branch is an antichain of n/4 upper states, identified with k-2 further coordinates because parity determines the last bit. Its 0 branch is precisely the same parity-bipartite family on k-1 remaining bits. Hence

  D_k <= n/4+1+D_(k-1).

For the converse, take any reduced identifying tree and follow nonsingleton outcomes until the first coordinate query of either polarity. If none occurs on this path, its length is n-1, at least the claimed bound. Otherwise suppose t singleton peels preceded that coordinate. Legality forces a whole forbidden layer/bit cell of size n/4 to have disappeared in one bit half E. Let H be the opposite bit half and t_H the number of states previously peeled there. Then t>=n/4+t_H.

Before these deletions, H is a copy of the (k-1)-bit family. If fixing the chosen coordinate reverses parity, flip one remaining coordinate to identify its two layers with the standard construction; the complement-closed library is preserved. Restricting the original library to H yields exactly the smaller family's library plus constants/duplicates.

Let R_H be the peeled states in H. Any safe identifying tree on H\R_H can be preceded by t_H safe singleton peels within H. Therefore

  D_(k-1) <= t_H + D(H\R_H).

Since the first coordinate is informative, the H branch is nonempty. The original tree has depth at least

  t+1+D(H\R_H) >= n/4+1+D_(k-1).

This proves D_k=2^(k-2)+1+D_(k-1). Summing with D_1=1 gives the formula. Consequently complement closure still permits a linear additive penalty and an unbounded depth ratio on connected posets. This is an exact natural-family result, but its height is one, not the genuinely nonhereditary height-two regime.

## Local lower bounds

For a feasible nonsingleton support define

  b(S)=min_(q in L(S)) max(|S_q0|,|S_q1|).

Then

  D(S) >= 1+ceil(log2 b(S)).

The complete recurrence is stronger than this one-step balance bound. The complement-closed family illustrates a useful adversary improvement: a forced run of t singleton removals gives D(S0)>=t+ceil(log2(n-t)).

Kraft/information bounds and adversary arguments are standard. The specific topological obstruction forcing these legal split families is the content of these examples.
