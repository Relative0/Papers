# Paper U v0.2 — fresh hostile priority review

Review date and literature cutoff: **29 September 2026**. This is a fresh analytical review by a separate model agent, not independent human peer review. The inherited priority map supplied leads; its conclusions were not accepted as evidence. Primary passages were reopened and compared with the present theorem contracts. Search is bounded, English-language, and not an exhaustive certification of priority. Dates returned by search engines as “published” were not accepted without primary metadata.

## Verdict

The manuscript survives this priority review **as a short synthesis/correction note**, subject to accurate source verification elsewhere in this review and the three citation repairs below. Original mathematical research novelty is **not established**. No basis was found for reinstating earlier claims to a new observation/latent-state architecture, a new partition topology, or a new general reconstruction theory.

There is a concrete reason to keep the note: it prevents four distinct mistakes in one explicit setting—confusing ultrametric similarity with indistinguishability, treating every collapse as metric, identifying completion with an incomplete starting space, and forming a quotient group from an arbitrary finite-index refinement. That is a defensible expository purpose. Its value is conditional on an audience that encounters those errors. Correct elementary mathematics alone would not justify a research-paper submission.

## Findings requiring or supporting repair

### P1. Add the exact fixed-scale quotient predecessor

The published paper by **Mémoli, Smith and Wan (2023), §2.1, equation (5), Definition 10, printed p.87**, gives precisely the closed-radius equivalence relation and the quotient distance retained between distinct classes. This is a direct mathematical predecessor for Paper U's threshold quotients. It was absent from v0.2's bibliography. The 2021 preprint uses Definition 9; citing that number against the journal publication would be wrong.

Verified journal record: [Journal of Computational Geometry 14(1), 78–143](https://jocg.org/index.php/jocg/article/view/3706), DOI [10.20382/jocg.v14i1a4](https://doi.org/10.20382/jocg.v14i1a4). The [published PDF](https://jocg.org/index.php/jocg/article/download/3706/3365/13424) contains the checked passage.

Recommended insertion at the tower setup: “The quotient metrics are the $t$-closed quotients of Mémoli, Smith and Wan [§2.1, equation (5), Definition 10], with $t=r_k$.” Their definition allows any ultrametric space and $t\geq0$; finiteness here follows separately from total boundedness and positive radius. This repairs attribution, not a false theorem.

### P2. State the Ishiki specialization explicitly

[Ishiki, arXiv:2302.00305v3](https://arxiv.org/html/2302.00305v3), Definition 2.2 and Proposition 2.31, permits continuous **pseudo**-ultrametrics inside disjoint clopen pieces. Take the finite index set to be the cells, its ultrametric to be $\delta_{\mathcal P}$, range set $[0,\infty)$, and all internal pseudo-ultrametrics to be zero. His construction is then exactly $d_{\mathcal P}$. The additional “pleasant” hypothesis concerns genuine compatible internal metrics and is unnecessary here. Proposition 2.32 concerns density and is not needed for this specialization.

Recommended replacement: “The collapse is a special case of Ishiki’s pseudo-ultrametric amalgamation [Proposition 2.31], taking every within-cell pseudo-ultrametric to be zero.” Paper U's inter-ball lemma still supplies representative independence and agreement with the original cross-cell distances. This is more exact attribution than “closely related.”

### P3. Tighten the Kleiner locator

[Kleiner's 2020 text](https://arxiv.org/html/1907.03223v2) develops the automorphism-orbit relation and quotient in **§3.3, equations (3.3)–(3.8)**. Section 3.4 interprets the resulting accessible references. Change “Section 3.4” to “Sections 3.3–3.4.” The underlying attribution is substantively correct. The source concerns intersubjective relabelling/non-collatability, not the same cognitive mechanism or same finite-resolution metric construction as Paper U.

## Theorem-level assessment

| Paper U ingredient | Fresh comparison | Classification |
|---|---|---|
| Partition topology; indistinguishability classes | [Iyer–Shrivastava 2012](https://ijpam.eu/contents/2012-74-3/3/3.pdf), Definition 1, printed p.313, defines topology from partition blocks as a basis | Established construction |
| Kolmogorov and metric identification | [Pirttimäki 2019](https://arxiv.org/pdf/1905.01157), Theorem 5.3, printed p.18, identifies the zero-distance metric quotient with the quotient topology | Established theorem; exact locator correct |
| Finite adaptive ball collapse | P2 above applies to general disjoint clopen cells once a cross-cell ultrametric is specified | Standard construction specialized to ball geometry |
| Greatest dominated collapsing pseudometric | Once admissibility of the displayed collapse is proved, maximality follows pointwise: every competitor is zero inside cells and at most the original distance outside | Immediate extremal corollary, not evidence of separate novelty |
| Calibrated finite quotient tower | P1 above plus elementary uniform-error and nested-partition arguments | Standard threshold quotient with explicit calibration |
| Inverse limit / completion | [Stacks tag 08ZY](https://stacks.math.columbia.edu/tag/08ZY), Lemma 5.22.2, proves the compact Hausdorff totally disconnected / finite-discrete-limit correspondence. [Dovgoshey 2025](https://arxiv.org/html/2502.04228v1), Theorem 10.25, identifies isometric completions through labelled representing trees | Standard topology plus a proved metric identification; no new general reconstruction theorem |
| Tree/end-space representation | [Hughes 2004 author PDF](https://math.vanderbilt.edu/hughescb/Publications/2004_Trees.pdf), Theorem 6.9 and the introductory category descriptions | Much broader categorical context with specified morphisms; manuscript's cautious statement is appropriate |
| Frontier expansions and refinement | [Lawson–Vdovina](https://arxiv.org/pdf/1909.13254), §12, Lemma 12.1, treats expansions of maximal generalized prefix codes; ordinary free-monoid prefix codes are a specialization | Standard prefix-code combinatorics |
| Full-tree sections and stabilizers | [Bartholdi–Grigorchuk–Šunić, Branch Groups](https://arxiv.org/html/math/0510294v2), §§1.2.2–1.2.3: local permutation portraits, level transitivity, section homomorphisms, and full-group product decomposition | Standard ingredients for Paper U's adaptive theorem |
| Adaptive exact normality criterion | No exact prior named statement was located by the searches logged separately; the short argument below derives it from the preceding ingredients | Useful explicit corollary; priority unresolved, originality unsupported |
| Index versus entropy | Counting allowed local permutations has no probability weights; a Shannon chain-rule sum does. Their numerical disagreement is expected | Clarification, not a new information theory |

The source is not treated as an infallible authority: for example, the Branch Groups HTML has an overbroad sentence about arbitrary subgroup stabilizers being normal in the ambient automorphism group. The full-automorphism-group facts used here are independently evident and are the applicable part of its discussion.

## Independent reconstruction of the adaptive priority target

Write $A=\operatorname{Aut}(T_m)$. Fixing the finite frontier pointwise fixes the entire finite upper skeleton. Each remaining descendant tree supports an arbitrary independent element of $A$, so $G_F=\prod_{s\in F} A_s$. Replacing one leaf by its $m$ children imposes exactly one local permutation constraint, with index $m!$. There are exactly $|I(F')\setminus I(F)|$ such constraints. Multiplication of indices is legitimate even when the final subgroup is not normal.

For normality, first observe that the $G_{F'}$-orbits on the boundary are exactly the frontier cylinders. If $G_{F'}\triangleleft G_F$, these orbits are permuted by $G_F$. Inside a fixed old cell $C_s$, the full section $A_s$ is transitive on every relative level. Therefore, if one frontier cylinder occurs at depth $h$, all cylinders at that relative depth occur. Prefix freeness and completeness rule out any other depth in that subtree. Conversely, a full relative level is the kernel of a finite-tree restriction homomorphism. The product of these kernels over old cells is normal, with the stated finite-tree product quotient.

This argument proves correctness under the stated contract and explains why an exact citation may be hard to locate: it is an elementary consequence of customary machinery, not an independently developed general theory. “Not found” must not be converted into “first proved here.”

A direct independent obstruction is $F=\{\varnothing\}$, $F'=\{0,10,11\}$ in the binary tree. A root swap sends this frontier to $\{1,00,01\}$, changing its pointwise stabilizer. By contrast $F=\{0,1\}$, $F'=\{00,01,1\}$ does give a normal inclusion: relative depths may differ between different old cells. Pointwise versus setwise is essential; replacing one by the other changes the groups and the count.

## Required cognitive predecessors rechecked

[Khrennikov 2007](https://arxiv.org/html/q-bio/0610013v3), §4, explicitly introduces associations as equivalence classes and writes their fixed-prefix descriptions. Thus “concepts as prefix classes” cannot be presented as Paper U's new cognitive idea. The source's dynamical assumptions are additional; they do not supply the entire present quotient theorem.

[Khrennikov–Yurova 2017](https://arxiv.org/html/1704.04681v1), §4, identifies states whose outputs agree for all inputs, constructs the factor-state set, and requires transition compatibility. Section 9 then uses an ultrametric/p-adic latent state model. This confirms a substantive latent-state / restricted-observation / quotient predecessor. It is not an assertion that every output-equivalence class is a metric ball, nor a proof of arbitrary adaptive-frontier dynamics.

These checks support v0.2's narrowed claims. They do not validate its empirical or psychoanalytic interpretation. Primary Matte-Blanco and Lauro-Grotto source fidelity is reviewed in the separate historical workstream.

## Recent literature and access limits

* [Dovgoshey, 6 February 2025](https://arxiv.org/abs/2502.04228), Theorem 10.25, is directly relevant as above. Its hypotheses are nonempty totally bounded ultrametric spaces; its conclusion concerns isometric **completions**, not necessarily isometric original spaces.
* [Bartoš–Kubiś–Kwiatkowska–Malicki, v2, 16 June 2026](https://arxiv.org/html/2605.13608v2), §§2.2–2.3, uses two-sorted distance-carrying structures, ball trees, and Cauchy chains. Its morphisms may change the distance sort. It supplies current representation context, not a discovered statement of Paper U's adaptive criterion.
* [Martino, 29 July 2026](https://arxiv.org/html/2607.26644v1), Proposition 3.7, reconstructs a locally finite rooted tree from nested finite clopen equivalence relations encoded by an admissible overlap function. Its §5 concerns automorphism-invariant refinements of finitely generated weakly branch actions. This is relevant recent reconstruction/refinement work, but a different contract from normality of two full-group frontier stabilizers.
* [Xin Li, March 2026](https://arxiv.org/html/2603.03362v1), §3.1, discusses contextual indexing and metric dynamics; the inspected passages do not supply the finite-ball quotient theorem. Do not cite merely for similar vocabulary.
* [Anagnostopoulou-Merkouri, Bailey and Cameron](https://arxiv.org/html/2409.10461v2), on permutation groups and partition lattices, supplies block-structure context. The inspected normal-subgroup passages did not state the exact frontier criterion.
* The [2010 category-as-ball article](https://link.springer.com/article/10.1134/S2070046610010012) and the [2017 topological-unconscious article](https://link.springer.com/article/10.1134/S2070046617010071) still exposed only subscription previews/abstracts. Their unseen contents were not ruled out. The 1997 book chapter and final 2014 cognitive article were not newly obtained in this pass.
* Search-only leads, including ideal-subgroup normality in Sylow tree groups and recent observation-framework preprints, were not promoted to verified theorem matches.

No coverage is claimed after 29 September 2026. No source-access gap proves priority. These gaps do not veto an explicitly non-priority synthesis, but they would veto a “first topological repair” or “first adaptive normality theorem” claim.

## Publication-fit judgment

The eight-page form is coherent if the abstract and introduction identify a practical conceptual correction, and the theorem displays are understood as a reusable worked synthesis. A pure topology or tree-group research audience would reasonably find the mathematical contribution too elementary. A foundations/modeling/expository audience may find the separation of geometry, observation, symmetry, and information useful. No specific journal policy or likelihood of acceptance has been verified.

For the overall scorecard, this workstream recommends: **attribution passes after P1–P3; original research novelty remains unestablished; contribution fit passes only for the explicitly narrowed note and suitable audience**. Historical source fidelity and all mathematical/reproducibility vetoes must be decided separately. Do not let a numeric aggregate override a failure in those gates.

Next required action in the parent review: apply P1–P3, reconcile the separate proof and source audits, and then decide submission readiness. No additional priority search is required for the present non-priority claim; reopen it if stronger novelty language is proposed.

