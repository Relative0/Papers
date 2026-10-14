# Phase 5B theorem, counterexample, and proof audit

Date: 2026-09-29. These are mathematical statements with explicit hypotheses; the pilot measurements are separate. None of the proofs establishes publication priority or an industrial speedup. Archived Phase 4/5 files have not been edited.

## Conventions

Let V be a finite declared Boolean variable set and let f be nonfalse. A valid disjoint AND partition P satisfies f = AND over B in P of f_B(x_B). Free variables remain singleton blocks, with the factor true. The canonical finest partition is Pi_f; every valid factor partition is its coarsening. This follows from the finite Cartesian-relation factorization property: if a nonempty relation is a product on two partitions, its projection on a block of either partition is itself the product of the projections on intersections, hence the relation also factors on the common refinement. Repeating over finitely many valid partitions gives the unique finest one. The nonfalse hypothesis matters to this projection argument; an implementation must report unsatisfiability separately rather than quietly applying these proofs to the empty relation.

A vtree is a rooted full binary tree with one leaf per declared variable. Mathematical exposure ignores left/right orientation, while actual SDD sizes and compiler behavior can depend on orientation. There are (2n-3)!! unordered-child labelled vtrees for n>=2: 15 at n=4, 105 at n=5.

## P4-SDD: exact compressed-SDD cut criterion

At a complete compressed decision on X|Y write f = OR_i (p_i AND s_i), with nonfalse, disjoint, exhaustive primes and semantically distinct subs. Each X-assignment satisfies exactly one prime, so its Y-cofactor equals that prime's sub. If f=g(X) AND h(Y), every such cofactor is either false or h. Conversely, if there is exactly one nonfalse sub h, its associated prime g satisfies f=g AND h. Nonfalse f rules out zero nonfalse subs. Therefore the criterion is exactly one nonfalse element, equivalently at most one under the nonfalse assumption.

This is also CM rank one: over F_2 every nonzero row of a rank-one Boolean matrix equals the same row. Trimmed implementations may place a node strictly below the requested vtree node; skipped sides are free and must be handled explicitly. Counting elements at an unrelated normalization node is not the stated criterion.

Apply this criterion at the current subtree. On success recurse into both factors, including true sides. On failure retain the subtree as one block. Any partition into proper clades below this subtree would separate its two children, contradicting the failed cut. Induction proves that E_T(f) is the finest valid partition whose blocks are clades of T. Failure does **not** imply unrestricted semantic primeness.

## F1: factor-exposure optimum

For every nonfalse f, max_T |E_T(f)| = |Pi_f|.

Proof: each E_T(f) is a valid partition and hence a coarsening of Pi_f, establishing the upper bound. Build a subtree on each prime block, then join these subtrees with an arbitrary binary skeleton. Each split in this skeleton separates unions of prime blocks, so the exact cut criterion succeeds until every prime-block root is reached. Within a prime block no nontrivial disjoint split succeeds. This vtree attains Pi_f. No assertion is needed about arbitrary internal splits *inside* a nonsingleton prime block. QED.

This proves existence of an optimal tree and correctness of a ground-truth-free exposure-count objective. It proves neither efficient search nor the ability to recognize that a found tree is globally optimal. All extraction certificates are factor certificates; they are not automatically prime-factor certificates.

### Certification correction: oracle alignment does not erase unknown work

If an external theorem or independently verified certificate establishes prime alignment, E_T(f)=Pi_f and no further SAT is needed. Without that certificate, a nonsingleton exposed block must still be tested for hidden cross-vtree factors. Even on an oracle-built aligned tree the ordinary solver cannot infer alignment merely from a failed subtree cut. Oracle evaluation may report true alignment or true directly exposed prime blocks after the run, but must not silently use those labels to stop algorithmic refinement or remove residual certification time.

A concrete failure is f=(x0 OR x2) AND (x1 OR x3), on T=((x0,x1),(x2,x3)). The root fails but Pi_f={{0,2},{1,3}}. Keeping the root as a final prime block would be incorrect.

## F2: carrier/semantic laminar obstruction

Two partitions P and Q of V can simultaneously be represented by vtree clades iff P union Q is laminar: intersecting blocks must contain one another.

Necessity: two rooted-tree clades are disjoint or one contains the other. Sufficiency: add V and every singleton to the laminar family, remove duplicates, and connect each proper member to its unique minimal strict superset. Children are disjoint and cover their parent because singleton sets were added. This is a rooted hierarchy with leaves V. Resolve every node with more than two children into a binary tree; existing clades persist. QED.

This is the standard laminar-hierarchy property, applied to the project partitions; no firstness claim is made. Example crossing partitions {{0,1},{2,3}} and {{0,2},{1,3}} cannot both be hard subtree constraints. Compatibility of a carrier with the current exposed coarsening does not certify compatibility with the unknown prime partition. A soft score is safe for efficiency; an unsupported hard lock is not.

For the simultaneous carrier/semantic problem, the required exact partition is LCC(Pi_K,Pi_f), the least common coarsening. Refining semantic factors first and taking this LCC is sound. Taking LCC with an incompletely refined exposed partition gives a valid coarsening, but need not give the finest simultaneous answer.

## F3: defect support and its exact information content

Fix cut A|B, row assignments a0,a1 and column assignments b0,b1. Let U be their differing coordinates in A and W their differing coordinates in B. A defect means

    f(a0,b0) f(a1,b1) XOR f(a0,b1) f(a1,b0) = 1.

Some prime block meets both U and W. To prove it, suppose no block does. After fixing all nonvarying coordinates, each prime factor depends on the row only, the column only, or neither. Its corner matrix is an outer product, possibly zero. Entrywise multiplication of such matrices remains an outer product. The determinant must vanish, contradiction. QED.

For U={x}, W={y}, x and y must belong to the same prime block. For larger supports, the assertion is existential. It does **not** say all of U union W lies in one prime block, or identify a sound edge for each cross pair. The natural certificate is the ordered support pair (U,W), with the witness assignments and four truth values retained. A single unlabelled hyperedge loses some of this information and is only a heuristic feature.

Counterexample to treating a whole support union as a must-link: EQ(x0,x1,x2) AND EQ(x3,x4), cut {0,3}|{1,2,4}, admits a defect whose support is all five variables, although its prime blocks have sizes three and two. The supplied independent check verifies this witness-support existence.

## F3-NO-GO: pairwise localization can fail completely

For n>=3 let f_n be true exactly at 0^n and 1^n. Every nontrivial Cartesian decomposition would combine the all-zero projection of one side with the all-one projection of the other, yielding a forbidden mixed model. Thus Pi_f={V}. Fixing n-2 coordinates leaves at most one satisfying entry in any two-variable slice, so every such slice has determinant zero. Across any nontrivial cut the full matrix has only two nonzero entries: the all-zero and all-one row/column pairs. A rank-two minor must select both, and its varying support is all n variables. This disproves universal singleton localization, even for a single semantic prime block. QED.

## P5-POS: irredundant positive CNF

Assume f is a conjunction of nonempty positive clauses, with duplicate clauses removed and no clause properly containing another. Its clause-interaction connected components, with isolated declared variables included, equal Pi_f.

For a positive clause C, f entails C iff some input clause is contained in C: the reverse direction is immediate; otherwise set all variables in C to zero and all other variables to one to obtain a countermodel. Thus the input antichain is exactly the set of positive prime implicates. Given any nonfalse disjoint factorization, its factors can be chosen as monotone projections by fixing satisfying assignments outside each factor. A prime clause C cannot span multiple factors: if no factor implies its local part of C, choose a satisfying assignment for each factor falsifying that local part, contradicting f entails C. If a factor implies a strict local part, C is not prime. Hence each clause lies inside one semantic block, forcing every interaction component into one block. Conversely the CNF explicitly factors across its interaction components. Both directions give equality. QED.

Irredundancy is essential. For f=x0 AND (x0 OR x1), the raw clause graph connects both variables but f=x0 with x1 free. This is a baseline structural fact, not a claim of a new factorization algorithm.

## P4-CM: read-once essential-gate recursion

Assume each leaf occurs once, children have disjoint supports, and every binary gate is essential in both inputs. Induction shows every descendant variable is essential: sensitize it in its child and select an attainable value of the other child that sensitizes the gate. Use the gate's 2x2 Boolean matrix over F_2, complemented entrywise when the requested output polarity is complemented.

Among the ten essential binary gates, rank one occurs precisely for the four signed conjunctions (one nonzero matrix entry); recursively concatenate the prime partitions of the children with the corresponding requested signs. In the rank-two case choose any left variable x and right variable y and independently sensitize each child. The resulting fixed-context two-variable matrix is the gate matrix up to row/column permutations, so its determinant is one. F3's singleton corollary puts x and y in the same prime block. Every cross pair is tied, so the whole support is one block. Leaves give singleton blocks in either polarity. This proves the two-polarity recursion. QED.

The read-once/disjoint-support hypothesis is indispensable: x XOR x is constant despite a rank-two XOR gate. A general shared DAG is outside the theorem. This elementary CM formulation does not supersede the established read-once Boolean-function literature.

## P5B-T1: output-sensitive defect-support minimization

Fix a cut and a correct permanent four-corner SAT encoding Phi. For S subset V define D(S) to mean that Phi is satisfiable together with x_v^(0)=x_v^(1) for every v outside S. Equality is imposed for coordinates outside S, without fixing their common value. Witnesses are allowed to change after each query. D is upward monotone: enlarging S removes equality constraints.

Given a known feasible starting support S0 of size m, sequentially try deleting each coordinate. Retain a deletion exactly when its SAT query succeeds. There are at most m additional queries and the final S is feasible and inclusion-minimal. Indeed a failed deletion at an earlier larger set stays infeasible at every smaller set by monotonicity. Every final witness uses all of S; otherwise its strictly smaller actual support would be feasible. The witness therefore certifies F3 on its two nonempty cut-side supports. This is inclusion-minimality, not minimum cardinality.

A balanced group-deletion variant has the output-sensitive bound

    number of SAT queries <= 1 + 2 d ceil(log2 m),

where d is the size of the support actually returned (m>=1). Place the initial support into any fixed balanced binary hierarchy of height ceil(log2 m). To process a group G, query D(current minus G). If SAT, delete G. If UNSAT and G is not singleton, recursively process its children; otherwise retain that singleton. A final support S is feasible. Every failed group intersects S: if it did not, S would be a feasible subset of the earlier candidate current minus G, contradicting UNSAT. At any depth the disjoint failed groups thus number at most d. Only children of failed groups are queried, so there are at most 2d queries at each nonroot depth and one root query. At every retained leaf, its failed deletion persists, proving inclusion-minimality. QED.

No uniqueness assumption is required for this output-sensitive bound. If every inclusion-minimal support has size at most a structural parameter d0, substitute d0 for d. Merely promising that *some* support has size d0 is insufficient: for EQ(x0,x1,x2) AND EQ(x3,x4) across {0,3}|{1,2,4}, minimal supports {0,1,2} and {3,4} coexist. Deletion order can return the larger one. The supplied finite check demonstrates both outcomes.

This is an application of generic monotone-predicate minimization/group deletion, not a new general minimization theorem. It counts oracle queries; SAT queries can still be hard. It gives no FPT wall-time result, does not prove a small residual partition, and gives no universal pairwise witness. Unsat cores of equality assumptions may accelerate an implementation only with a separate correctness argument: a core is not itself a defect witness and must not be converted automatically into semantic must-link edges. The production pilot uses sequential minimization; the group version is validated independently here as a theorem target, not an experimentally established performance advantage.

## Independent finite checks

`code/theory_independent_checks.py` imports no archived code. It checks laminar representability against all unordered-child labelled vtrees and all pairs of partitions through n=5, f_n support behavior across every nontrivial cut through n=8, the five-variable minimal-versus-minimum counterexample, and both deletion algorithms over every nonempty upward support predicate and every coordinate order through n=4. Data are `data/theory_independent_checks.json`; stdout is `logs/theory_independent_checks.log`. These finite checks support implementation confidence and do not replace the proofs above.

## What is not proved

There is no polynomial-time unrestricted semantic factor extraction theorem for arbitrary structured d-DNNFs here; no guaranteed vtree-search convergence bound; no general small-defect-width promise; no minimum-cardinality support bound from greedy deletion; no FPT hybrid runtime theorem; and no theorem that smaller SDDs expose more factors. Empirical Pareto cases must be labeled computational observations. The F1 optimum does not imply that a practical local optimum is semantically optimal.

## T4 implementation observation: size and exposure can trade off

A recorded real-SDD move for repeated_module_heldout_n6 increases size 17 to 18 while increasing exposure 1 to 2 and reducing residual calls 7 to 5. This is a reproducible finite computational observation, not a theorem about global optima or a priority claim. Exact inputs/vtrees are in data/size_exposure_tradeoff_example.json; timing limitations are in SUPPLEMENTARY_DIAGNOSTICS.md.
