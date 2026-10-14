# Independent tree-group review of Paper U v0.2

Review date: 29 September 2026. Reviewer: a separately instantiated AI tree-group review role, not an independent human referee. The role read the current v0.2 source, the theorem ledger, strengthening study, adversarial report, and next-review instructions. Prior verdicts were treated as hypotheses, not proof. This report covers the adaptive theorem, its corollary and limitations, information comparison, and frontier appendix. It does not claim an independent literature search; the parallel priority role handles sources and exact-predecessor searches.

## Verdict

The adaptive theorem is correct under its stated contract: **full rooted automorphism group of the infinite regular tree, finite complete frontiers, and pointwise fixation of frontier vertices**. No mathematical repair is required in this part of v0.2. Different old cells may be refined to different relative full levels, including level zero. Mixed relative depths within any one old cell prevent normality. A nonuniform old frontier creates no extra condition. The manuscript draws these distinctions correctly.

The appendix statements and entropy comparison also survive reconstruction. Their mechanisms are elementary and standard. Correctness of these statements does not establish original research novelty or decide publication fit. A claim to a new general group-theoretic or information-theoretic theory would fail this review. As a tightly framed correction/synthesis, these statements can support the note, subject to the separate contribution-fit and source-fidelity gates.

## 1. Contract and potential ambiguities

Let the alphabet have m >= 2 letters. Vertices are finite words, including the empty word e. An automorphism preserves the root and adjacency. A finite complete frontier F is prefix-free and meets every infinite ray once. Write I(F) for all proper prefixes of frontier words and C_s for the infinite cylinder at s. The group G_F fixes every s in F **individually**.

Fixing a vertex s is equivalent to preserving its cylinder C_s as a set; it does not require fixing the boundary points of that cylinder. Fixing every frontier vertex individually is different from preserving the collection F setwise. The latter permits exchanges of frontier cells with compatible tree positions. These distinctions are already explicit in v0.2 and are essential, not terminology.

For example, with F equal to all first-level vertices, the setwise stabilizer is the whole tree automorphism group, whereas the pointwise stabilizer is the first-level kernel and has index m!. Thus the main formula would immediately fail if the paper silently meant setwise stabilization.

The group in the theorem is an abstract group; every restriction map in the proof is also continuous for the usual profinite topology, but no topological-group claim is needed. T_(m,0) must mean the one-vertex rooted tree, whose automorphism group is trivial. This is the standard height convention and is consistent with the formula as written.

## 2. Independent proof reconstruction

### 2.1 Frontier structure and sections

The finite upper tree has vertex set I(F) union F. Every vertex in I(F) has all m children in that upper tree: completeness forces every child subtree to meet F. Fixation of every frontier vertex fixes all its ancestors, so G_F fixes this entire upper tree pointwise. Conversely, independently choose a rooted automorphism of the descendant tree at each s in F, and act identically above F. The actions have disjoint supports and glue to a rooted automorphism. Restriction to these descendant trees and gluing are inverse homomorphisms. Hence G_F is the direct product of |F| copies of Aut(T_m).

This is a direct product, not a semidirect product, precisely because no old frontier cells may be permuted. Under setwise stabilization an additional permutation action can be present.

### 2.2 Boundary orbits

Every element of G_F preserves C_s for each s, so an orbit cannot cross a frontier cell. For any two rays in C_s, choose child permutations successively along the source ray to send its next edge to the next edge of the target ray. Choose arbitrary compatible permutations elsewhere. This constructs a rooted automorphism of the full subtree at s sending one ray to the other; glue it with identity in all other old cells. Thus C_s is a single orbit.

No countability, finite-support, or selected-generator restriction is permitted here. In particular, finite-level transitivity by itself does not prove transitivity on infinite rays.

### 2.3 Exact finite index

Refinement is equivalent to I(F) being contained in I(F'). Split vertices in I(F') minus I(F) in an order in which ancestors occur first. Each next vertex is then a leaf of the current frontier, and splitting it into its m children produces the next frontier. Every added internal vertex is split once, so the number of operations is exactly N.

At one such leaf s, the current pointwise stabilizer has a full independent section at s. Its action on the m children is a surjection onto Sym(m). The kernel fixes these children individually and is exactly the stabilizer of the new frontier. Consequently one split has index m!. Multiplicativity of subgroup indices along the finite chain gives [G_F:G_F'] = (m!)^N.

Multiplicativity of index does not require each intermediate subgroup to be normal in the original group. The proof correctly avoids inferring a quotient-group structure from a finite index. Equality F=F' gives N=0 and index one. Every strict refinement has N>0 and therefore is a proper subgroup because m>=2.

### 2.4 Normality: necessity by boundary orbits

Put H=G_F'. If H is normal in G=G_F, then for every boundary point x and g in G, g(Hx)=H(gx). Therefore g permutes the H-orbit partition, already shown to consist exactly of the cylinders of F'. Fix s in F and choose t in F' below s at relative depth h. The full section of G at s is transitive on the m^h words at this relative depth. Every cylinder at that depth is therefore the image of C_t and must also be an H-orbit. Distinct tree vertices have distinct cylinders for m>=2, so every word of s Sigma_m^h belongs to F'. Those cylinders already cover C_s. Prefix-freeness excludes any other frontier vertex under s. Thus the refinement inside each old cell is exactly one full relative level.

This argument does not force a common h across old cells, because G_F cannot exchange those cells. It also does not force a common absolute depth. If h=0, t=s and the old cell is left unchanged.

### 2.5 Independent alternative necessity argument

The same conclusion follows without infinite boundary orbits. Suppose the relative frontier inside an old cell has unequal leaf depths. At the minimum leaf depth h there is a leaf u and also an internal vertex v; otherwise there would be no deeper leaf. A rooted automorphism of that old cell can send u to v, because they have equal relative depth. A nontrivial child permutation supported below u lies in H, since u is a frontier vertex and its descendants are unrestricted. Its conjugate is supported below v with nontrivial first-level action. Completeness guarantees frontier descendants under the moved children of v, so this conjugate moves a frontier vertex and is not in H. Hence H is not normal.

This is also an explicit mechanism for nonnormality: a symmetry allowed below an unsplit leaf can be conjugated to a location where the finer observation already resolves it.

### 2.6 Normality: sufficiency and quotient

If the relative frontier under s is Sigma_m^(h_s), its pointwise stabilizer in the section group is the kernel of restriction to the finite rooted tree of height h_s. Restriction is onto: extend a finite rooted automorphism below its terminal vertices using the natural labelled descendant-tree identifications. The kernel is normal, and the quotient is Aut(T_(m,h_s)). Taking the product over old cells proves both sufficiency and the stated quotient formula.

At h_s=0 the restriction has trivial target and the kernel is the entire factor. Leaving a cell unchanged therefore contributes an index-one, trivial quotient factor. Different h_s cause no difficulty. The height-h finite-tree group is an iterated wreath product in its natural action; it should not be replaced by Sym(m^h). For example, at m=3 and h=2 its order is 1296, much smaller than 9!.

### 2.7 Corollary and example

For a uniform frontier at depth k there are m^k factors. Refining all once gives quotient Sym(m)^(m^k). Refining only a subset S once gives relative heights one on S and zero elsewhere, hence quotient Sym(m)^|S| and normality. S may be empty.

For the binary refinement {e} to {00,01,1}, I(F') has two vertices, so index four is correct. Root interchange transports the fine orbit partition to {C_0,C_10,C_11}; these are different partitions. Normality fails. Successive local normal inclusions can indeed have a nonnormal composite inclusion. The manuscript's example and its interpretation are correct.

## 3. What cannot be generalized without new hypotheses

For an arbitrary subgroup K of Aut(T_m), a pointwise frontier stabilizer may not have independent arbitrary sections. Its available local permutations may be proper subgroups of Sym(m), correlated between cells, or trivial. The index formula and orbit clause need not survive. The trivial subgroup is the simplest failure.

A stronger warning is the finitary automorphism group: it is countable and transitive on every finite level, but each infinite-boundary orbit is countable while a cylinder is uncountable. Thus even finite-level transitivity is insufficient for the boundary orbit clause. The full-group assumption in v0.2 is substantive.

For a nonregular rooted tree with a finite complete frontier, independent sections still yield a product of the automorphism groups of the actual descendant trees when the full rooted automorphism group is used. The factors may differ and their boundary actions may fail to be transitive. Child permutations can only exchange isomorphic descendant trees. There is no universal factorial index based only on the number of children and no universal strictness statement. The three-point ultrametric example in v0.2 is correct: c is distinguished by its distance pattern, while a and b can be exchanged, so the full isometry orbits are {a,b} and {c}, unlike the one-cell observation partition.

No additional manuscript repair is needed; the stated limitations already block the false extensions.

## 4. Frontier appendix, including edge cases

The association F -> I(F) is a bijection between finite complete frontiers and finite prefix-closed sets of vertices, with the empty internal set allowed. Given an internal set I, stopping at the first vertex outside I gives a finite complete frontier, and its proper prefixes are exactly I. Refinement becomes inclusion of internal sets. Union and intersection remain finite and prefix-closed, so they give join and meet and satisfy distributivity. The empty set corresponds to the root frontier, the bottom. Splitting any leaf gives a strict finite refinement, so there is no finite top.

In the finite upper full tree, counting edges as m times the number of internal vertices and also as total vertices minus one gives |F|=1+(m-1)|I(F)|. This includes F={e}. Under the uniform measure, frontier cylinders are disjoint and covering, giving Kraft equality. Conversely, a **finite** prefix-free family with total cylinder measure one must cover: its complement is open, and a nonempty open complement contains a positive-measure cylinder. Finiteness is needed for that argument. For instance, the infinite binary prefix code {0,10,110,...} has total mass one but misses the all-ones ray. The manuscript expressly states the finite hypothesis.

For a finite set A of distinct infinite rays, every prefix containing at least two samples is a common prefix of a distinct pair. Each pair has finitely many common prefixes; a finite union is finite. Prefix-closure is immediate. If a frontier separates A, every vertex of I_A must be internal: otherwise a stopping ancestor contains the same pair. Conversely, splitting exactly I_A stops only at cylinders containing at most one sample. Thus a frontier separates A iff its internal set contains I_A, which proves the unique least refinement and the minimum-leaf formula.

For A empty or a singleton, I_A is empty and the least frontier is {e}, with one leaf. Unoccupied branches still contribute leaves because the frontier must cover the entire boundary, not merely the sample. The word "distinct" is important: repeated observations of one identical infinite ray cannot be separated as different latent points by prefix observations. Feature order and allowed tests remain fixed; no optimal arbitrary-query decision-tree result follows.

These edge cases require no correction. An optional single sentence recording the empty/singleton case could help readers, but adding it is not a correctness prerequisite.

## 5. Information calculation

For a split at v of mass M>0 with child masses M p_a, subtracting the old contribution -M log_2 M from the child contributions gives M times the finite distribution entropy of p. If M=0, all child masses are zero and the gain is zero. Iterating over the newly split vertices gives the exact displayed formula, independently of split order. No division by zero occurs under the manuscript's convention.

For uniform independent digits, M=m^(-|v|), whereas logarithmic group index contributes log_2(m!) per split regardless of depth or mass. The binary balanced-versus-comb calculation is correct: three split vertices produce index eight in both cases, while the entropy is 2 versus 7/4 bits. More starkly, a point-mass source has zero entropy at every frontier while every strict refinement has positive logarithmic group index. Thus index is not an information gain without extra structure; neither count identifies conscious states.

## 6. Independently authored bounded regression

Files: `check_mixed_ternary.py`, `mixed_ternary_results.json`, and `mixed_ternary_run.log`. Run with Python 3.10.11 using only the standard library:

```powershell
python .\check_mixed_ternary.py --out .
```

The script constructs eight local adjacent-swap permutations on the nine terminal vertices of T_(3,2), then computes group closure by breadth-first search. It does not use the theorem's order formula to manufacture or count group elements. The closure contains 1296 elements. Pointwise stabilizers are selected by testing preservation of each individual cylinder; setwise stabilizers are separately selected by preservation of the partition collection. Normality is tested by conjugating every subgroup element by each ambient generator, stopping upon an explicit counterexample. As the chosen adjacent-swap generators are involutions and generate the ambient group, successful testing on these generators establishes normality in this finite group.

| Relative frontier | Pointwise order | Setwise order | Index | Normal |
|---|---:|---:|---:|---|
| {e} | 1296 | 1296 | 1 | yes |
| {0,1,2} | 216 | 1296 | 6 | yes |
| all nine length-two words | 1 | 1296 | 1296 | yes |
| {00,01,02,1,2} | 36 | 432 | 36 | no |

The concrete uncertainty addressed is **normality for m>2 when both the old frontier and refinement depths are nonuniform**. Use the old frontier F={0,10,11,12,2}, with old absolute depths one and two. The finite permutation image needed for these checks is a product of five copies of the explicitly enumerated group, acting on 45 terminal nodes, two further levels below each old cell. Its order is 3,656,158,440,062,976; the full product is not enumerated. The factor stabilizers and conjugations are enumerated, and product membership supplies the finite composite check.

* Relative full heights (2,1,0,1,2) produce a normal subgroup. The global old/new frontiers directly give N=10. The index obtained from the enumerated factor orders is 60,466,176=6^10. New absolute frontier depths are two and three. This tests mixed h_s and h_s=0 together.
* Replace the relative frontier below old cell 10 with {00,01,02,1,2}. The global count becomes N=11 and the index is 362,797,056=6^11. The inclusion is nonnormal. New absolute depths are two, three, and four. An explicit witness in that factor has g interchange first digits 0 and 1 and h interchange terminal vertices 11 and 12. The element h fixes the uneven frontier individually, but g h g^(-1) interchanges 01 and 02 and therefore does not. The complete permutations are retained in JSON.

This extends the supplied fixed-small-global-depth checks by targeting nonuniform old cells and different relative refinements, without trying to enumerate an infeasibly large full product. It is finite-image evidence, not a substitute for the infinite proof. The factorwise direct-product step is supported by the proof in Section 2, not independently discovered by the computation.

Additional exact appendix checks enumerate all nine ternary complete frontiers through depth two, all 81 meet/join pairs, and all 512 subsets of the nine depth-two sample codes. They verify Kraft equality with rational arithmetic, the leaf formula, and the least separating frontier and unique minimum leaf count. The ten empty/singleton sample cases explicitly give the root frontier. These finite sample codes stand for distinct infinite rays with arbitrary fixed tails; their first two digits already distinguish them.

All checks passed. No test failure was edited away; there was one run of the completed regression. The computation makes no cognitive or empirical claim.

## 7. Manuscript action and remaining gate

Required tree-group/appendix repair: none. Optional clarity only: spell out that height zero gives the trivial finite-tree automorphism group, and that empty/singleton samples use the root frontier. The existing pointwise qualifier and full-group hypotheses should remain explicit in any shortening.

This role supports mathematical survival of the narrowed note, not an unconditional submission verdict. Exact theorem priority, historical fidelity, overall contribution fit, and publication venue remain separate gates. In particular, the short proof and standard mechanisms make the adaptive statement useful for precision without supplying evidence of original research novelty.
