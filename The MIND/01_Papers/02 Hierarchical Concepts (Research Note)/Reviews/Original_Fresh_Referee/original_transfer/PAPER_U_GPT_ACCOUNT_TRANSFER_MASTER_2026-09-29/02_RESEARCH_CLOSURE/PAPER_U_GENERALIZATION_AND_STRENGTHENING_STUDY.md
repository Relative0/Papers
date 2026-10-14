# Paper U: generalization and strengthening study

**Date:** 29 September 2026. The proofs below are reconstructions/derivations in this audit. "Derived here" does not assert first priority. The companion priority map identifies standard mechanisms and unresolved exact-statement priority.

## D1. Coordinate-free geometry: what actually generalizes

Let (X,d) be a nonempty ultrametric space and P a finite partition into nonempty clopen balls. Define q_P(x) to be the cell containing x. For different cells B,C put delta_P(B,C)=d(x,y), for x in B,y in C; put delta_P(B,B)=0.

### Lemma: cross-distances are representative independent

For x,x' in a ball B and y outside B, d(x,x')<d(x,y). This follows from the radius inequalities for open or closed balls; singleton balls cause no difficulty. Applying the strong triangle inequality in both directions gives d(x',y)=d(x,y). Applying the same argument inside C proves constancy on B x C.

Consequently delta_P is a finite ultrametric, and its pullback d_P is zero within a cell and equal to the original distance between cells. The strong triangle inequality follows by choosing one representative in each of three cells. The topology of d_P is exactly the partition topology. This proves the coordinate-free collapse without assuming regular branching, a prime alphabet, compactness, or a global uniform depth.

**Why clopen is included.** It ensures the observation map is also continuous from the original latent topology. Positive-radius ultrametric balls are clopen automatically. A finite partition by balls has clopen cells in the ordinary cases here; retaining the explicit hypothesis avoids turning a radius-zero singleton into an unqualified open-ball claim.

### The geometric contribution is substantive but limited

Every partition gives equivalence and an initial topology, without ultrametricity. Ultrametricity supplies compatible threshold equivalences and constant distances between separated balls, permitting an exact distance-preserving collapse. An arbitrary partition may fail: on binary words of length two, collapse {00,10} and leave the others separate. Then d_P(10,01)=1 while d_P(10,00)+d_P(00,01)=1/2.

The converse is false: in a three-point equilateral metric, a two-point block is not a ball, but any partition can be collapsed this way. The result is a sufficient ball-partition theorem, not an iff characterization of all admissible partitions.

### Quantitative accuracy

For any finite ball partition,

    sup_(x,y) (d(x,y)-d_P(x,y)) = max_(B in P) diam(B),

where diameter is a supremum, and the maximum exists because P is finite. Across cells the error is zero; within a cell it is exactly d(x,y). Thus refinement decreases the collapse error, and mesh tending to zero gives uniform metric recovery. This estimate is immediate, not claimed as a new approximation theorem.

### Threshold tower and completion

Assume X is totally bounded and r_0>=diam(X), r_0>r_1>...>0, r_k->0. Let x~_k y iff d(x,y)<=r_k. Transitivity follows from ultrametricity. A finite cover by sufficiently small balls proves finitely many equivalence classes at each k. Classes are clopen balls, the partitions are nested, and

    d_k(x,y) = 0 if d(x,y)<=r_k, otherwise d(x,y),
    0 <= d-d_k <= r_k,  d_k <= d_(k+1).

Their topologies generate the latent topology. If kappa is the first positive index distinguishing a pair, the correct general statement is

    r_kappa < d(x,y) <= r_(kappa-1).

Equality d=lambda^(kappa-1) requires the calibrated prefix distance spectrum; it is not a general ultrametric theorem.

The inverse limit of the finite quotients is the completion of X. Proof: compatible cells are nested and their diameters tend to zero; a choice of points forms a Cauchy sequence in the completion. At each fixed level, positive separation between the finitely many cells makes their closures disjoint and covering. Thus every completion point determines exactly one compatible code. The latent space is dense in the inverse limit. Its compactness/completeness is exactly what removes the possible missing limit points. Eventually zero binary sequences give a concrete incomplete counterexample.

Nested finite clopen partitions with mesh tending to zero also reconstruct topology in a compact space even if their cells are not balls. They do not automatically retain original cross-distances. The revision does not merge these two different assertions.

**D1 decision:** retain. This is a useful generalization of the draft's contract but lies within standard ultrametric/profinite theory.

## D2. Universal properties: three categories, one quotient set

For a fixed finite ball partition P, the quotient q_P has the following precise roles.

**Sets:** composition with q_P gives a bijection between maps P->Y and cell-constant maps X->Y. This follows from surjectivity and the definition of a class.

**Topological spaces:** give X the partition topology and P the discrete topology. The quotient is its Kolmogorov quotient. Continuous maps to a T0 space identify topologically indistinguishable points and therefore factor uniquely. The T0 restriction is essential to this unrestricted factorization assertion; a map to a non-T0 target can distinguish representatives as elements while remaining continuous. If a map is already required to be cell-constant, its factorization is of course valid for any target.

**Metric spaces:** give X the collapsing ultrapseudometric and P the cross-distance metric. A nonexpansive map from X to a metric target must identify zero-distance points, hence factors uniquely and nonexpansively. Equivalently, a cell-constant nonexpansive map from the original (X,d) factors nonexpansively because the metric is unchanged across cells.

**Extremal formulation:** d_P is the greatest pseudometric e<=d vanishing on every cell. Within cells every candidate is zero; across cells every candidate is <=d=d_P. Existence of d_P as a pseudometric was proved using the ball geometry. This is an order-theoretic characterization, not a claim that every arbitrary partition permits this pointwise formula.

**D2 decision:** retain as one synthesis theorem with separate target categories. It is not a new general quotient construction.

## D3. Adaptive symmetry: exact index and exact normality criterion

### Contract

T_m is the full infinite rooted m-ary tree, m>=2. Aut(T_m) means the full group of rooted graph automorphisms. F is a finite complete prefix-free frontier. I(F) is the finite set of proper prefixes of F. G_F fixes each frontier vertex individually, not merely the frontier setwise. F<=F' means refinement.

### Product decomposition and orbits

The upper finite tree is fixed. Sections in descendant subtrees can be chosen arbitrarily and independently, giving

    G_F is isomorphic to product_(s in F) Aut(T_m).

A full regular subtree is transitive on its infinite rays: prescribe successive digit permutations along the source ray to send it to the target ray, complete the other vertex permutations arbitrarily, and take the compatible action on all finite levels. These independent actions give precisely the frontier cylinders as G_F boundary orbits.

This proof does not work for an arbitrary subgroup, even one acting transitively at some finite levels, nor for arbitrary nonregular descendant trees. In particular a countable subgroup cannot have an uncountable boundary fiber as a single orbit. The full group contract is substantive.

### Index

Replace a frontier leaf s by its m children. Restrict the section at s to the first level. This is a surjective homomorphism onto Sym(m); its kernel is the new stabilizer. The index is m!. Every finite refinement is a sequence of exactly N=|I(F') minus I(F)| such operations. Multiplication of subgroup indices yields

    [G_F:G_F'] = (m!)^N.

The index is finite even though both groups are infinite. It counts cosets of allowed transformations, not latent points, not psychological states, and not directly information bits.

### Normality

Claim: G_F' is normal in G_F iff each old frontier cylinder is refined to a single full relative level. Formally, for every s in F there must be an h_s>=0 with

    {t in F': s is a prefix of t} = s Sigma_m^(h_s).

Necessity: if H=G_F' is normal in G=G_F, every g in G permutes the H-orbits. Those orbits are exactly F' cylinders. Inside any old cell, G contains every subtree automorphism, transitive at each relative depth. An F' vertex at relative depth h therefore forces all vertices of that depth to be in F'. Prefix freeness and completeness exclude every other depth in that subtree.

Sufficiency: the refined subgroup in each old-cell factor is a full level stabilizer, the kernel of restriction to the finite height-h_s tree. Products of these kernels are normal. Moreover

    G_F/G_F' is isomorphic to product_(s in F) Aut(T_(m,h_s)).

The heights may differ between old cells. They cannot differ adaptively within a single old cell when normality in its full automorphism factor is required.

### Uniform and local corollaries

At uniform depth k, G_k is Aut(T_m)^(m^k), and G_k/G_(k+1) is Sym(m)^(m^k). Splitting any subset S of current frontier leaves once gives the normal quotient Sym(m)^|S|. A longer normal refinement has finite-tree automorphism groups as factors, generally iterated wreath products, not a single symmetric group of the number of leaves.

### Counterexample: normal steps can compose to a nonnormal inclusion

Binary F={empty word}, F'={00,01,1}. Two splits give index four. A root flip sends its orbit partition to {0,10,11}, so the subgroup is not normal in the original full group. Calling the coset set a quotient group would be wrong. The intermediate local inclusions being normal does not make normality transitive.

### Nonregular failure

On {a,b,c}, put d(a,b)=1/2 and d(a,c)=d(b,c)=1. Whole-space observation has one fiber, but the full isometry group has two orbits, {a,b} and {c}. More generally descendant-tree automorphism groups need not be isomorphic or boundary transitive; children can only be permuted among isomorphic rooted subtrees. There is no blanket strict stabilizer chain for arbitrary hierarchies.

**D3 decision:** this is the strongest sharpened result. Retain proof and counterexamples. Standard section theory makes it plausible as a familiar consequence; exact priority remains a specialist question. Do not use an unlocated exact citation as evidence of first discovery.

## D4. Adaptive frontier structure and observation cost

### Lattice

A finite complete frontier corresponds bijectively to a finite prefix-closed set I of split vertices. Refinement is inclusion of I. Intersection and union of two such sets are again finite prefix-closed; therefore the refinement poset is a distributive lattice. It has a bottom, the root frontier, but no finite top on an infinite tree.

### Kraft constraint

For uniform independent digits, the cylinder at s has mass m^(-|s|). A finite complete frontier partitions the boundary, so these masses sum to one. Conversely a finite prefix-free family with sum one has empty complement: otherwise its open complement contains a cylinder of positive mass. Completeness, not prefix-freeness alone, is needed.

### Least separating frontier under a fixed coordinate order

For a finite set A of distinct infinite branches, let I_A be the prefixes whose cylinders contain at least two elements of A. This is finite because it is a union of common-prefix sets of finitely many distinct pairs. It is prefix-closed. A frontier separates A iff its split-vertex set contains I_A. Thus the frontier of I_A is the unique least separating frontier and has

    1+(m-1)|I_A|

leaves. A nonnegative additive per-split cost is minimized there. Zero-cost extra splits can give additional cost minimizers; positive costs make the minimizer unique. The empty or one-element sample has I_A empty and needs only the root frontier.

This is the uncompressed trie principle. It does not solve the problem of choosing an optimal feature order, arbitrary tests, noisy acquisition, or a task-specific expected stopping cost. Those would be genuinely different observation-design problems. No new general complexity theorem follows.

### Exact information accounting

For probability mu and conditional child distribution p(.|v), the frontier entropy difference is

    H_mu(F')-H_mu(F)
      = sum_(v in I(F') minus I(F)) mu(C_v) H(p(.|v)).

Proof: for one split, subtract the old parent entropy term from the new child terms; the difference is mu(C_v) times the child-distribution entropy. Iterate. Zero-mass parents contribute zero; no division by zero is used.

Under uniform branching, H(F)=log2(m) sum_(v in I(F)) m^(-|v|), also log2(m) times the expected observed prefix length. By contrast log2 index is |I(F)| log2(m!), unweighted. The binary balanced frontier at depth two and comb {000,001,01,1} each have three splits and index eight, but entropies 2 and 7/4 bits. Changing mu with the frontier fixed also changes entropy without changing the group index.

The equation is standard hierarchical chain-rule accounting (Perotti-Almeira-Saracco, 2020), not a new entropy measure. It is retained only to block an invalid symmetry-information identification.

### Precise conditional-expectation contract, removed from the main text

On (X,Borel,mu), let F_k=sigma(q_k), and f in L1. Then M_k=E[f|F_k] is a uniformly integrable martingale and converges a.s. and in L1 to E[f|F_infty], where F_infty=sigma(union F_k). If F_infty is the full sigma-field modulo mu, that limit is f. For f in Lp, 1<=p<infinity, convergence also holds in Lp. In L2 the conditional expectation is the orthogonal projection. Uniform/L-infinity convergence does not follow in general. These are standard results, especially Durrett Theorem 4.6.8, not a contribution.

**D4 decision:** retain adaptive symmetry in the body, frontier/trie facts in a short appendix, and only the entropy-versus-index caution in the body. Move full martingale discussion to this study.

## D5. Bounded noisy extension

For finite output alphabet Y, a stochastic observation is Q:X->Delta(Y). Exact observational equivalence is equality of channel rows: x~_Q y iff Q(x)=Q(y). If Q=K composed with q_P, it is constant on P cells, though K may merge additional cells. Noise does not automatically eliminate exact equivalence; nor does distinctness of noisy distributions guarantee that one sample identifies a state.

A natural distance is d_Q(x,x')=TV(Q(x),Q(x')). This is a pseudometric, but generally not an ultrapseudometric. Bernoulli laws with parameters 0,1/2,1 have distances 1/2,1/2,1, violating the strong triangle inequality. Thus a generic noisy extension exits the ultrametric category.

Postprocessing by a Markov kernel K contracts total variation: write each output difference as a weighted sum of input differences, apply the triangle inequality, sum over outputs, and use that each kernel row sums to one. This is ordinary information-processing monotonicity.

For deterministic observations with finite output sets, postprocessing order reduces to partition refinement: q_1 can be recovered deterministically from q_2 exactly when the q_2 partition refines q_1. Even allowing a stochastic kernel cannot evade this condition when the desired outputs remain deterministic; one row of the kernel cannot equal two different point masses. This is a simple deterministic special case of the comparison-of-experiments viewpoint, not new theory.

**D5 decision:** defer. The bounded study supplies a clear obstruction and a standard compatibility statement, not enough added value to widen the note.

## Reproducible finite checks and their limits

The provided script enumerates all complete frontiers on binary depth four, and all rooted automorphisms for binary depth three and ternary depth two. It tests the index and normality formulas against explicit finite permutation groups, not merely against the same closed formula used to predict them. It also checks quotient distances, entropy, frontier lattices, sample separation, XOR, and explicit counterexamples.

The two group runs cover 258 comparable frontier pairs, including equality, with 178 normal and 80 nonnormal inclusions. These are finite regression checks; the infinite-boundary theorem rests on the proof above. No simulation of cognition or statistical validation is implied.
