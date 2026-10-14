# Independent topology, ultrametric and information review

Review date: 2026-09-29. Input: the archived v0.2 TeX and eight-page PDF. This is an AI analytical review, not a report from a human specialist. Proofs below were reconstructed rather than inferred from the prior ledger or finite regression results. Correctness does not certify novelty.

## Disposition

The mathematical claims survive under the intended nonempty ultrametric-space hypotheses. Two local repairs are warranted: make the ultrametric hypothesis explicit in the coordinate-free theorem and tower setup, and explicitly prove continuity in the completion/homeomorphism argument. The latter is a short missing justification, not a counterexample to the conclusion. No theorem needs to be weakened under its intended contract.

## Findings requiring or motivating changes

| ID | Finding in v0.2 | Severity and disposition |
|---|---|---|
| T1 | Theorem 2.2 refers to `(X,d)` without repeating that it is ultrametric; Section 3 begins with merely 'totally bounded'. The intended assumption is evident, but the latter sentence alone allows non-ultrametric spaces, for which threshold closeness need not be transitive. | Local hypothesis omission. Explicitly say 'ultrametric' in both places. For example, `{0,1,2}` with ordinary distance and threshold 1 defeats the unrestricted formulation. |
| T2 | Proposition 3.1 invokes compactness/Hausdorffness to turn a bijection into a homeomorphism without explicitly establishing continuity. | Local proof omission. The finite, positively separated closures of level cells are clopen in the completion. Coordinate maps are therefore continuous. Add this step. |
| T3 | Introduction uses 'complete family of cell-level observables' before defining completeness. | Expository ambiguity. Use agreement under all cell-constant observables, as in the actual theorem. |
| T4 | Prefix metric formula specifies only distinct arguments; the zero diagonal is implicit. | Definition clarity. State `d_lambda(x,x)=0`. |
| T5 | Entropy identity uses refinement without a local reminder; 'Neither cardinality' follows an entropy calculation, although entropy is not a cardinality. | State `F <= F'` and replace the final sentence with an explicit warning about interpreting either quantity as a count of conscious states. |

## Independent proof reconstruction

### Lemma 2.1: constant cross-distances

Let B be an open ball of radius r about b, x,x' in B, and y outside it. Ultrametric recentering gives d(x,x') < r <= d(x,y). For a closed ball, the inequalities become d(x,x') <= r < d(x,y). In both cases the inner distance is strictly smaller than the cross-distance. The two strong triangle inequalities force d(x',y)=d(x,y): a strictly smaller value would imply d(x,y) <= max(d(x,x'),d(x',y)) < d(x,y). Apply the same reasoning to the other ball to get representative independence on B x C. Radius-zero closed balls are singletons and cause no problem. The one-cell case needs no cross-distance statement.

### Theorem 2.2: quotient, topology and maximality

For three different cells, choose one representative in each; the quotient inequality is precisely the original ultrametric inequality. Repeated cells reduce it to zero or equality. Off-diagonal quotient distances are positive, so the finite quotient is discrete; when it has only one point this remains true without taking a minimum over an empty set. Pulling the quotient metric back gives exactly zero within cells and the original metric across cells. A sufficiently small positive ball at any point is its whole cell, so its topology consists of all unions of cells.

Topological indistinguishability in that topology is exactly common-cell membership. Any continuous map into a T0 target must identify two points with identical open neighborhoods: otherwise a distinguishing target open set has an impossible preimage. Surjectivity of q gives the unique factor, and the factor is continuous because the finite quotient is discrete. The actual quotient topology is also discrete, since preimages of all subsets are open. This is the Kolmogorov quotient of the *partition topology*, not of the original Hausdorff metric topology. The original metric space itself has singleton Kolmogorov classes.

T0 is essential to the unconditional continuity implication. From an indiscrete two-point domain to an indiscrete two-point target, the identity is continuous but is not constant on the single domain cell. There is no contradiction with the set-theoretic assertion, which separately requires cell constancy. Nor does continuity from the *original* metric topology imply cell constancy. The source topologies cannot be silently exchanged.

For set-valued maps, define the factor at B to be f(x) for any x in B; constancy is precisely well-definedness. If the map is both cell-constant and nonexpansive for d, then for different cells the factor distance is bounded by d(x,y)=delta(B,C). Inside one cell it is zero. No extension or compactness theorem is being invoked.

For maximality, an admissible pseudometric e is zero inside a cell and is at most d across cells. These are exactly the two cases defining d_P, so e <= d_P pointwise. Since d_P is itself admissible, it is a greatest element, not just maximal. This is an elementary order observation once admissibility is proved; it does not establish a new optimization principle.

One-cell X and a singleton X give d_P=0 and a singleton quotient. A partition into singleton cells gives d_P=d; for finite X it gives the original discrete topology. The theorem does not assert indiscreteness of the whole latent metric space. The clopen hypothesis also makes the observation q continuous from the original metric topology.

### Example 2.3 and the geometric hypothesis

With blocks {00,10}, {01}, {11}, the collapsed distances obey d_P(10,01)=1, d_P(10,00)=0 and d_P(00,01)=1/2. Thus even the ordinary triangle inequality fails. Quotient-set existence alone does not license the cross-distance-preserving formula. Conversely, a non-ball block in an equilateral finite space can be collapsed, so the ball condition is sufficient rather than necessary.

### Proposition 3.1: thresholds and completion

Assume explicitly that X is a nonempty totally bounded *ultrametric* space. Positive thresholds make `d <= r_k` an equivalence relation. An open cover by balls of radius less than r_k admits a finite subcover, each member of which lies in a single threshold class; hence there are finitely many classes. Each class is a closed r_k-ball and is open, since an open r_k-ball about each of its points lies in it. All statements allow a singleton X and a positive r_0 despite diameter zero.

The collapse error is zero between classes and equals d <= r_k inside them. Refinement can only change a collapsed distance from zero to d, which proves monotonicity. Each partition-open set is metric-open; every metric neighborhood contains a sufficiently small threshold class. It is the topology *generated* by the union of level topologies that equals the original topology. The union need not be closed under arbitrary unions. The first distinguishing index exists because the thresholds tend to zero; since level zero is one cell, its bounds are `r_kappa < d <= r_(kappa-1)`.

Give the inverse limit the subspace topology inherited from the product of finite discrete quotients. Compatible cells are nested, nonempty, with diameters tending to zero. Representatives form a Cauchy sequence, so their closures in the completion have exactly one common point. At any fixed level, distinct cells have constant positive cross-distances. Finite many cells cover X; their closures cover the completion, remain disjoint, and remain positively separated. They are therefore clopen. Each completion point yields a unique compatible sequence, and the coordinate maps are continuous. The completion is compact (complete plus totally bounded), and the inverse limit is Hausdorff. This *continuous* bijection is a homeomorphism. This supplies the omitted continuity step in v0.2.

Density of X follows without compactness of X: a basic cylinder condition specifies finitely many compatible coordinates and therefore contains the image of a point of their deepest cell. For metric precision, if two compatible sequences first differ at level j, all subsequent intercell distances equal that same positive cross-distance, because finer cells are subsets of the earlier cells. Thus `D(a,b)=lim delta_k(a_k,b_k)` is zero on the diagonal and is eventually constant and positive off it. Taking limits in the strong triangle inequality makes D an ultrametric. For the corresponding completion points, continuity of the extended distance yields exactly D. This also proves the claimed isometry without circularly relying on density alone.

The eventual-zero binary sequences demonstrate the essential incompleteness issue: every finite prefix is attained, so the limit is the full binary boundary; the all-ones sequence is missing from X. Total boundedness alone does not identify X with its completion. Empty spaces are excluded by the manuscript's global nonemptiness convention.

### Prefix calibration and p-adic specialization

For distinct branches, the common-prefix inequality gives the strong triangle inequality for lambda^ell. A length-k cylinder is the closed lambda^k-ball and, for k>=1, the open lambda^(k-1)-ball. An open lambda^k-ball fixes k+1 coordinates. Boundary/radius equalities therefore matter. A first distinction at coordinate ell has observation index ell+1. These equalities depend on the specified scale, not on arbitrary threshold choices.

Countably many finite cylinders form a basis, so their Boolean algebras generate the Borel sigma-algebra. They are not generally themselves a sigma-algebra or a topology. In the prime case, the least-significant-first digit map is bijective onto Z_p and the first nonzero digit of a difference gives its p-adic valuation. Residue compatibility reconstructs unique digits. No field structure or p-adic dynamics enters any earlier proof.

### Section 5: entropy

For one split let w=mu(C_v)>0 and child masses w_a=w p_a. Subtracting the parent term from child entropy gives `-sum w_a log_2 w_a + w log_2 w = w(-sum p_a log_2 p_a)`. If w=0, all child masses are zero and the contribution is zero without defining a conditional law. Sum over any refinement order. Each newly internal vertex is split once, so the displayed identity follows. Under the uniform law, the weights are m^(-|v|); the group log-index has no such weights.

Balanced binary leaves have four masses 1/4 and entropy 2 bits. The comb has masses 1/8,1/8,1/4,1/2 and entropy 3/8+3/8+1/2+1/2=7/4 bits. Both have three splits and index 8. Changing the probability law while holding a frontier fixed is another immediate obstruction to identifying these quantities. This is not a cognitive-data result.

## Limits of this review

The proofs establish the intended conditional mathematics. They do not select a psychologically valid hierarchy or observation map, certify empirical adequacy, settle historical source fidelity, or establish original priority. Tree-group and appendix reconstructions are separately documented. The supplied numerical suite is corroboration only.
