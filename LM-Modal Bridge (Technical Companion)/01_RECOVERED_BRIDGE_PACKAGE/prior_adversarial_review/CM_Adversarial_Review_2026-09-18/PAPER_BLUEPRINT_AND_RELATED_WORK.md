# Paper blueprint, contributions and related work

Extract from RESEARCH_REPORT.md. Reference keys resolve in ANNOTATED_BIBLIOGRAPHY.md.

# F. Paper blueprint and publication strategy

## F1. Recommended single-paper architecture

**Preferred title:** *Smith Invariants and Contextuality in Finite-Chain-Ring Support Models.*  
**CM-forward alternative:** *Logical Rotation and Contextuality over Finite Chain Rings.*  
**Descriptive subtitle:** *A rotation-equivariant realization from Boolean correspondence matrices.*

The original proposed narrative is reasonable as a research notebook, but too diffuse as a journal paper. Do not postpone the substantive theorem until after a long tour of familiar quantum-like effects. State the classification in the introduction, explain the CM origin briefly, and prove the abstract result before discussing diagnostics.

| Section | Content and theorem order | Approximate main-text budget |
|---|---|---|
| 1. Question, contribution, prior-art boundary | State the classification and explain why the circulant algebra and modal phenomena are not claimed as new; import Paper B | 2 pages |
| 2. Rings, measurements, and support semantics | Types; primitive rows; complete projective bases; global assignments; no-signalling; operational non-claims | 2-3 pages |
| 3. Hyperplanes and Smith classification | Lemma 8, Theorem 9, Lemma 11, count corollary; all analytic proofs | 4-6 pages |
| 4. CM rotation realization | `A=F2[C4]`; maximal equivariance; semantic corollaries; the 192-basis instance | 2-3 pages |
| 5. Restricted versus unrestricted resources | Same-rank/different-contextuality example; shared/literal support isomorphism; tensor closure boundary | 2-3 pages |
| 6. Verification and limitations | Reproduction table, scope of finite searches, no faithful probability extension, comparison to physical QM | 1-2 pages |
| 7. Outlook | Non-chain rings, preparation-compatible state theories, minimal contextuality witnesses | 1 page |
| Appendices | Detailed inventories; higher-arity classical connections; orthogonal/form obstructions; teleportation diagnostics | As needed |

A 14-20 page main text is a plausible target, not a venue requirement. Formal proofs should remain in the main text when they constitute the contribution. The enormous resource inventory belongs in machine-readable supplements, not as pages of tables.

**Omit from the novelty list:** Paper B's compiler and frame calculus, generic Bell/GHZ demonstrations, generic teleportation and dense coding, broad lists of speculative hardware applications, and a rediscovery of Reed-Muller group codes. The compact interferometer may remain as one illustration of why rotation is being studied.

## F2. Smallest strong contribution list

1. **A complete contextuality classification for bilinear support models over finite commutative chain rings**, in arbitrary bipartite dimensions, with strong contextuality characterized by the multiplicity of the least Smith valuation.
2. **A residue-hyperplane characterization of global assignments and a uniform Hardy witness**, supplying constructive mechanisms for the classification rather than only enumerating a 16-element example.
3. **A carefully typed rotation-equivariant realization and resource comparison**, showing which Smith distinctions disappear after forgetting coefficient-ring structure, while explicitly separating tensor conventions and preparation closure.

The first two are closely linked and may be advertised as one main theorem plus its mechanisms rather than artificially split into independent discoveries. The third is mainly conceptual synthesis with a concrete corollary.

| Contribution | Mathematical novelty | Conceptual novelty | Proof strength | Generalizability | Reviewer interest | Practical evidence |
|---|---|---|---|---|---|---|
| General classification | Strong candidate; bounded priority search | Substantial valuation/contextuality bridge | Analytic proof plus finite checks | All finite commutative chain rings; arbitrary dimensions | Highest | Formal testbed, no speedup claim |
| Hyperplane/Hardy mechanism | Candidate exact formulation; standard ingredients credited | Explains rather than lists classes | Constructive proof | Hyperplane lemma already applies to local rings | High | Efficient verification reduction |
| CM realization and orbit comparison | Mainly synthesis/corollary | Useful bridge and restriction diagnostic | Exact derivations and exhaustive instance | Other group actions possible, not automatic | Moderate | Educational and verification value |

## F3. Venues and likely objections

These recommendations concern fit, not predicted acceptance. Official scope pages were checked during this review. [VenueQS; VenueFoP; VenueJPA; VenueQPL]

**Quantum Studies: Mathematics and Foundations** is the most natural first target for the mathematical-foundational version. Its scope expressly bridges mathematical methods and foundational questions. Reviewers will ask whether the ring generalization teaches something not already implicit in modal quantum theory. Lead with the full theorem, acknowledge that it is a support model, and compare directly with de Beaudrap and Gogioso.

**Foundations of Physics** is plausible for a carefully positioned modal-model contribution. The prior Schumacher-Westmoreland publication makes the lineage intelligible, but it does not guarantee suitability. The principal challenge will be physical/conceptual significance and the incomplete independent-preparation interpretation of the all-nonzero shared model. Avoid presenting mere algebraic analogies as a reconstruction of physics.

**Journal of Physics A: Mathematical and Theoretical** is a more demanding fit. Its official scope requires significant original mathematics motivated by actual or potential physical phenomena. A chain-ring classification with a clear operational comparison is more plausible than a four-cell Boolean notation paper. Additional classification beyond chain rings or a strong measurement-restriction theorem would improve the case.

**Quantum Physics and Logic (QPL)** is a suitable conference family for the typed/process-theoretic direction. The 2026 meeting and its submission window have already passed; this recommendation is for a future edition, not an available 2026 deadline. The main challenge is compositional closure: a formal process contract or explicit statement that the contribution is about support models would be essential. The current conference description emphasizes algebraic, logical, compositional, and categorical structures.

Do not make a coding or Boolean-function journal the first target merely because the ring and ANF appear. The relevant coding connections are already classical. Likewise, a reversible-computing venue needs an actual new reversible construction, synthesis result, or measured implementation advantage, not just the word "reversible" in the unit criterion.

# G. Publication-ready contribution paragraph

> We study bipartite possibility models defined by nonzero bilinear pairings over finite commutative chain rings. For the complete family of projective reversible local bases, we classify contextuality by the Smith invariants of the resource matrix. A resource with one nonzero Smith factor is relationally local; a resource with multiple nonzero factors is logically contextual, and it is strongly contextual precisely when its least valuation has multiplicity at least two. The proof combines a residue-hyperplane characterization of global assignments with a uniform Hardy construction. As a concrete realization, we lift the four-position rotation of a Boolean correspondence matrix to its classical circulant commutant, `F2[C4]`. This realization exhibits resources of equal underlying binary rank but different contextuality under rotation-equivariant measurements. We separate these results from existing modal quantum theory, from the classical group-algebra description of Boolean degree, and from claims about physical quantum states or unrestricted independent preparation over a ring with zero divisors.

Priority-safe addition, only after the bibliography is updated before submission:

> A bounded literature search located no equivalent Smith-invariant classification for this complete-basis bilinear support model. The circulant algebra, modal phenomena, and individual algebraic ingredients are established; the claim of contribution concerns their stated classification and realization.

# H. Draft related-work section

Matrix and vector representations of propositional logic have a substantial history. Edwards, Stern, and Mizraji study logical operations through Boolean matrices or vector operators, while Eigenlogic and semi-tensor-product methods provide other operator representations of logical functions and networks. Bricken's geometric treatment of Boolean-function symmetries is also relevant to the rotation motivation. We therefore do not claim that logical connectives, their geometric symmetries, or their representation by matrices are new. Paper B supplies the particular typed CM calculus used here and is imported as background. [Edwards1972; Stern1988; Stern1992; Mizraji1992; Mizraji2008; Eigenlogic2016; Cheng2011; BrickenSymmetry; B]

Our rotation algebra is a classical cyclic group algebra. Circulant matrices over finite fields, their transpose involution, and their unit structure are treated in the finite-field circulant literature. The nilpotent presentation at power-of-two length is a standard modular specialization. The connection between the parity of a Boolean truth table and its full ANF coefficient explains the degree criterion in the two-input example. For elementary abelian translation actions, the more extensive degree/radical correspondence is the Berman-Charpin Reed-Muller construction. [MacWilliams1971; NortonSalagean2000; Carlet2010; Berman1967; Charpin1988; Andriatahiny2016]

Schumacher-Westmoreland introduced modal quantum theory with field-valued states and possibility-valued measurement outcomes, including nonlocality and information-transfer analogues. James-Ortiz-Sabry relate finite-field quantum computation to reversible relational programming with exclusive disjunction, and later ring and semiring models make the dependence on scalar algebra and state-space axioms explicit. We use these works as antecedents, not as phenomena to be rediscovered. Our shared-ring supports are not asserted to constitute a tensor-closed state theory with every nonzero vector independently preparable. [SW2012; JOS2011; dB2014; Gogioso2017]

The contextuality terminology follows the distinction between supported global assignments, logical obstruction, and strong obstruction developed in sheaf-based accounts. Hardy arguments supply a familiar pattern of logical contradiction; our contribution is a ring-uniform implementation together with a complete Smith-invariant classification. Phase-group comparisons and finite-ring projective descriptions of Mermin configurations provide related but different uses of finite algebra. In particular, finite-ring labels for commutation configurations and partial-ring Kochen-Specker obstructions should not be identified with the bilinear support model studied here. [AB2011; AH2012; Hardy1993; CES2011; SPM2006; CMR2022]

Finally, operator bases and teleportation have an established Hilbert-space theory. We use their finite-field analogues only as diagnostics of the chosen restrictions. The failure of transpose-orthogonal binary matrices to span the full operator space follows from their fixed row and column sums and classical permutation-matrix span results. It should not be interpreted as a general obstruction to every possible characteristic-two analogue of quantum information. [Werner2001; Lueneburg1988; DomokosFrenkel2004]

# I. Claim-safety table

| Safe wording | Overclaim to reject |
|---|---|
| The rotation lift realizes a classical circulant algebra from a declared CM frame. | CMs introduce a new 16-element operator algebra. |
| In two variables, non-affineness coincides with invertibility of this lift. | Nonlinearity is equivalent to reversibility for arbitrary Boolean functions. |
| The cyclic unit test is truth-table parity; the translation-radical hierarchy recovers a classical Reed-Muller construction. | CM rotation discovers Reed-Muller codes or the entire Boolean degree hierarchy. |
| A specified rotation-equivariant support model has the proved Smith classification. | Quantum theory is deduced uniquely from Boolean logic. |
| No equivalent general classification was located in this bounded search. | We are the first to prove contextuality over rings. |
| A valuation-uniform choice of bases realizes the Hardy pattern. | Hardy contextuality or XOR interference is new. |
| Same binary rank can coexist with different contextuality relative to a fixed restricted measurement family. | Contextuality ceases to be invariant under valid equivalences of one theory. |
| These shared and literal restricted bipartite tables agree up to involution relabeling. | Their different tensor products necessarily give different contextuality tables. |
| All nonzero shared-ring vectors are not tensor-closed as independent preparations. | A closed operational theory has already been constructed for all of them. |
| No full binary operator basis can consist of transpose-orthogonal matrices when dimension exceeds one. | No Bell basis or teleportation is possible in characteristic two. |
| Rank-r tensor powers admit exact extraction by unrestricted linear filters when `r^k>=d`. | Deterministic physical distillation or a success probability has been established. |
| The finite computations reproduce exact claims within stated search families. | Exhaustive computation establishes publication priority or every generalization. |

