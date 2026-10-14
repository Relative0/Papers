# Paper split and freeze plan

## Recommendation

Prepare **one focused research manuscript and one foundations technical report**, not three research papers at present. Preserve simultaneous-refinement and observation-design results in appendices or separate frozen research notes. Promote either into a standalone article only after it gains a result not exhausted by standard machinery and examples.

This is a scope recommendation, not a prediction of acceptance. The present strongest theorem has significant standard-incidence and discrete-Morse overlap. A publishable narrow specialization needs exact positioning, clean statements, and the sharpness results; calling every chapter a new theory would weaken the submission.

## Preferred architecture: Option 1

### Research manuscript A: Binary order thinning of finite posets: homology, collapses, and sharp limits

**One-sentence thesis:** binary observations force a tractable incidence-forest geometry in height two, but this equivalence between homology neutrality and direct collapse breaks under richer labels or greater height.

**Central theorems:** v0.4 `thm:repairforest` with integral strengthening A1; exact collapse certificate/algorithm; A6 one-bit higher-height universality; v0.5 eight-state three-bit counterexample and A4 matching characterization as the bit-count boundary. Theorem numbering should emphasize the preservation theorem and its limits, not every background lemma.

**Prerequisite background only:** finite posets/order complexes; suborders on the same vertices; relative chains; graph incidence; elementary collapse. State the McCord link briefly only when interpreting the result as logical observation topology.

**Sections to include:** (1) general poset problem and contributions; (2) one-bit thinning and elementary rigidity; (3) signed incidence theorem, full relative groups, and rooted-forest equivalences; (4) collapse certificates and logical sufficient conditions; (5) sharp limits: blocks, higher height, torsion; (6) short propositional realization/application; (7) reproducibility appendix. The chain trichotomy should be a short Ferrers/beat-point corollary, not the main novelty claim.

**Exclude:** the historical formula sequence, extensive homology tutorials, broad Stanley-Reisner program, detailed persistence construction, a long survey of unrelated Boolean fragments, and the incorrect dimension section. Include at most one destructive and one noncollapse block example in the body; put the larger torsion certificates in the supplement.

**Repairs before drafting:** C03-C07 and C09-C13; v0.3 source restoration; precise finite-space/order-complex language. The false dimension equality may simply be excluded, but the archived notes and ledger must still receive an explicit erratum.

**Novelty risk:** moderate to high. The forest theorem is an exact specialization of elementary graph incidence plus relative collapse, not a new general topological method. Its value is the characterization under a natural binary-order restriction and the clean boundary when that restriction changes.

**Closest prior art:** R02, R03, R04, R09, R19. Cite all at the point of use. Do not bury the Ferrers antecedent in a final discussion.

**One addition that would most improve it:** resolve the two-bit height-two boundary: does F2-neutrality still force direct collapse? One bit is proved; three bits fail; exhaustive two-bit checks through five vertices find no failure. A structural proof or a small explicit counterexample would make the bit-complexity boundary much sharper.

**Realistic genre:** focused combinatorial-topology research article or substantial short note after positioning; otherwise a rigorous specialist technical report. No acceptance guarantee.

### Companion report F: Homological foundations of finite observation topologies

**One-sentence thesis:** give a reliable dictionary separating topology-invariant order-complex constructions from presentation-sensitive compatibility and metric constructions.

**Central content:** core quotient framework; v0.1 homology, relative groups, mapping cones, Boolean cochains; v0.2 profiles and standard fiber criteria; basic observation/premise filtrations. The report is an organized application of existing theory, not a collection of new theorems.

**Prerequisites:** finite propositional semantics, basic posets, chain complexes. Include explanatory examples for non-specialists.

**Include:** definitions with one consistent specialization convention; the ordinary quotient versus weak realization distinction; model restrictions and their loss of information; the exact split replacement for the old sequence; Dowker/Stanley-Reisner definitions with ghost vertices; fixed-weight Rips constructions; a short annotated prior-art guide.

**Exclude:** unsupported cognitive interpretations, journal-style novelty claims for standard tools, an unbounded research agenda, and full duplicated proofs of the focused article's main theorem.

**Repairs:** all relevant corrections C04-C13. The old notes should be linked as historical motivation, never as validated prerequisites.

**Novelty risk:** low if presented honestly as exposition; very high if submitted as a new homology theory.

**Closest prior art:** R01-R02, R10-R12, R16-R18, R21.

**Most valuable addition:** a compact, independently testable worked example showing all three invariance targets—order topology, compatibility complex, and weighted metric—side by side. This is an expository improvement, not a reason to open another research branch.

**Genre:** citable technical report/expository companion with permanent versioning and reproducible examples.

## Conditional second research paper B

### Simultaneous order thinning and relative topological interaction

**Thesis:** study how separately acceptable coordinate deletions combine, including compensating defects and coefficient-sensitive obstructions.

**Current theorem set:** v0.5 intersection and coefficient criterion; A3 relative Mayer-Vietoris; A4 matching criterion; three/five/eight-state examples; A5 torsion realization. These are correct after C03, but much of the general machinery is already standard.

**Background:** relative chains, Mayer-Vietoris, rooted forests/fitting orientations. No full ProLT foundations chapter.

**Include if promoted:** a nontrivial restriction theorem in bit count or coarse-poset structure, followed by sharp examples and exact computation. Use A3 to explain rather than merely display destructive interaction.

**Exclude:** treating intersections alone as a new theory; determinant/torsion facts without credit; repeating Paper A's full one-bit proof; the unrelated dimension-complexity branch.

**Repairs:** C03 and all coefficient/ordinary-versus-order-complex conventions. Explicitly distinguish coordinatewise safety from sequential safety on the actual intermediate orders.

**Novelty risk:** high without another structural theorem. Mayer-Vietoris is useful but does not by itself make this a new interaction theory.

**Prior art:** R03-R04, R18-R19.

**Best added theorem:** a complete two-bit classification, a structural forbidden configuration criterion, or an efficiently checkable nontrivial joint-safety theorem for a natural family.

**Genre now:** frozen research note/appendix. **Genre after that theorem:** focused research article or short note.

## Conditional dimension note C

### Minimum Boolean observations for a prescribed suborder

**Thesis:** characterize the minimum number of Q-upsets required to remove exactly the comparisons of P absent from Q.

**Correct theorem set:** universality; A2 conflict-coloring/generalized Boolean-rank identity; repaired height-one NP-completeness; elementary bounds; target-antichain formula. Remove v0.5's classical 2-dimension equality and inherited total-order hardness.

**Background:** finite orders, graph coloring, generalized rectangle covering. Topology is not needed to prove these results.

**Include if promoted:** one substantial restricted-family theorem, with explicit input representation. Good targets are a prescribed coarse chain or a structurally bounded conflict graph.

**Exclude:** a claim to have invented generalized Boolean covering; using “Boolean dimension” without specifying which inequivalent definition is intended; generic NP-completeness as the sole selling point.

**Repairs:** C01-C02 are blocking; bibliography must include R06-R08 and distinguish fixed-family reducts from arbitrary feature design.

**Novelty risk:** high. The general covering mechanism is already established. The exact poset restriction may be worth studying, but absence of an exact name does not establish novelty.

**Prior art:** R06-R08, R13; R22 is a terminology collision, not an equivalent parameter.

**Best added theorem:** classify the conflict graphs arising when P is a specified total order and derive a genuine algorithmic or hardness theorem for that family. Do not assume the existing general-height-one reduction proves this.

**Genre now:** corrected technical note, frozen. Standalone research short note only after a structural result and a renewed targeted literature check.

## Alternative architecture: Option 2

Use **two** research manuscripts plus the foundations report: A contains only one-bit preservation, repair criteria, and higher-height sharpness; B contains all block interaction, torsion, matching, and the resolved two-bit question. This is coherent if B gains its own central theorem. It is not recommended immediately because current B risks being a standard-methods-and-examples paper, while splitting the sharpness examples out of A can make A look too slight.

A third independent dimension paper is not justified by the current package. It is mathematically separate and should remain so, but separateness alone does not establish publishability.

## Freeze register and dependencies

| Branch / claims | Decision | Reason / condition |
|---|---|---|
| Core quotient and orientation; V1-01..06 | FREEZE_AS_VALIDATED_BACKGROUND | Standard, correct; retain distinctions and carrier conventions |
| Old formula exactness and old ad hoc simplices | DROP/REPLACE | Invalid historical constructions, replaced by v0.1 |
| V1 cochains, Dowker, SR, Rips; elementary relative groups | TECHNICAL_REPORT_ONLY | Useful synthesis; no independent contribution demonstrated |
| V2 profile/fiber hierarchy | FREEZE_AS_VALIDATED_BACKGROUND | Standard tools plus useful examples |
| V3 positive DNF, adjoint rigidity, elementary counts | FREEZE_AS_VALIDATED_BACKGROUND | Do not expand into separate branches |
| V3 chain theorem | FREEZE_AS_VALIDATED_BACKGROUND | Ferrers overlap; direct proof useful, not main novelty |
| V4 forest/integral A1/algorithm | FREEZE_FOR_PAPER_A | Main exact characterization; preserve narrow novelty label |
| V4 Horn/repair criteria | FREEZE_FOR_PAPER_A | Sufficient-condition examples; no blanket fragment theorem |
| V5 interaction examples, A3 | FREEZE_FOR_PAPER_A or conditional B | Standard exact-sequence explanation and sharp examples |
| V5 eight-state failure, A4 | FREEZE_FOR_PAPER_A | Bit-count boundary; no minimality claim |
| A5 block torsion; A6 higher-height one-bit universality | FREEZE_FOR_PAPER_A | Strong limits; put large certificates in supplement |
| V5-06 2-dimension equality | DROP/REPLACE | False; A2 replaces it |
| V5-07 total-order complexity | BLOCKED_BY_CORRECTNESS | Original proof fails; restricted truth unresolved |
| A2 corrected dimension framework | BLOCKED_BY_NOVELTY / DEFER | Established covering framework; needs structured result |
| Two-bit height-two boundary | PURSUE_NEXT | Only active theorem target |
| Persistence, SR syzygies, inference-gap applications | DEFER | No current theorem justifies independent expansion |
| Cognitive/mental-space and threshold applications | DEFER | No defensible application bridge established |

No result is to be silently lost: freeze the source snapshot and ledger, add the erratum and dependency table, and refer deferred branches to this register. Freezing is not deleting; it is ending active expansion until a concrete reopening condition is met.
