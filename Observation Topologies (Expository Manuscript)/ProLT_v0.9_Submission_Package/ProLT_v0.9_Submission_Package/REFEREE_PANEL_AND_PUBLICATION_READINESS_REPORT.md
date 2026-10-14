# Referee Panel and Publication-Readiness Report

## Manuscript reviewed

**Revised title:** *Observation Topologies for Finite Propositional Semantics: Distinguishability, Distance, and Inference*  
**Revision:** v0.9 submission candidate, September 2026

This report distinguishes three different kinds of evidence:

1. material already present in the supplied ProLT archive;
2. fresh specialist/adversarial review performed for this revision;
3. fresh mechanical and literature checks.

The supplied archive says that v0.8/v0.8.1 previously received an audit and a referee-level pass, but the archive does not contain the full underlying referee reports. Its own review index correctly warns that labels such as "panel" or "referee" do not establish independent human review. I therefore did not treat those summaries as a substitute for a fresh review.

## 1. Fresh review panel

These are simulated specialist/referee roles used to stress-test the manuscript, not independent human referees.

### Reviewer A - finite topology and order theory

**Recommendation:** Acceptable after minor expository revision, provided it is submitted as exposition rather than as a new foundational theory.

**Main findings**

- The signature/up-set representation, specialization preorder, T0 quotient, T1 criterion, and monotonicity statements are mathematically sound under the finite-carrier assumptions.
- The manuscript should avoid making standard Alexandrov-space facts appear novel.
- The relation between a chosen observation presentation and the topology it generates is correctly separated: weights and duplicate coordinates are presentation data and are not recoverable from the topology.

**Action taken:** The revised draft explicitly says the numbered results are self-contained derivations rather than priority claims, and the "ProLT" branding was removed from the mathematical definition and title.

### Reviewer B - logic and topological semantics

**Recommendation:** Minor revision; suitable as an expository logic/topology note.

**Main findings**

- Classical truth-region semantics is kept distinct from the Heyting operations of the open-set algebra.
- Semantic consequence is correctly presented as model-set inclusion; the topology organizes observability and subspaces around it rather than replacing classical consequence.
- The positive-observation convention is potentially easy to misunderstand, but the manuscript correctly distinguishes semantic falsity in a complete signature from nonreceipt of a certificate in an unfinished transcript.

**Action taken:** The abstract and introduction now foreground the classical/expository status; a comparison table distinguishes positive observation, two-sided observation, observation refinement, and premise update.

### Reviewer C - quasi-metric and information geometry

**Recommendation:** Minor revision.

**Main findings**

- The weighted directed set-difference formula is a valid quasi-pseudometric and its zero relation agrees with specialization.
- Symmetrization is weighted Hamming distance.
- The forward-ball proof is correct, including the empty observation family and the strict-radius issue.
- The construction is useful as an explicit coordinate representation but is not a new general quasi-metrization theorem.

**Action taken:** "Symmetric logical distance" and "directed logical distance" were renamed to **symmetric signature distance** and **directed loss distance**. The text now states explicitly that numerical distances depend on the presentation. Dovgoshey-Shanin (2026) was added as a current broad Alexandrov quasi-metrization precedent, alongside Pavlovic and de Brecht.

### Reviewer D - formal concept analysis / rough sets / information systems

**Recommendation:** Minor revision.

**Main findings**

- The comparison with Pawlak-style indiscernibility is appropriate if it is restricted to the two-sided/partition case.
- The incidence table is naturally a formal context, but the manuscript correctly warns that its full open-set lattice is not generally the concept lattice.
- A topology/FCA literature reference closer than the foundational FCA book improves priority hygiene.

**Action taken:** The draft now cites Pei, Ruan, Meng, and Liu (2013) as a related topology-on-attributes construction and states that its carrier differs from the valuation/object carrier here.

### Reviewer E - expository editor

**Recommendation:** Major editorial revision, then acceptability review.

**Main findings**

- The earlier title and "ProLT" naming risked sounding like a claim to a new mathematical theory.
- The inference section devoted too much space to elementary truth-table material.
- The paper needed one compact running example tying signatures, neighborhoods, implication, and XOR together.
- Contextuality and connectedness directions distracted from the paper's actual contribution.

**Action taken:** Retitled and de-branded; added a four-state running table; compressed hypothetical syllogism and the pullback discussion; removed contextuality/connectedness digressions; reframed the nerve material as a presentation-dependence caution; added keywords and cleaner publication-facing front matter.

## 2. Hostile referee attacks

### Hostile Referee 1 - novelty/priority attack

**Attack:** "This is a collection of elementary finite-topology and truth-table facts with new terminology. Hamming distance, specialization, upward-set topologies, semantic consequence, and set-difference quasi-metrics are not new. Reject if presented as original research."

**Assessment:** **Substantially sustained.** This is the strongest objection and cannot be solved by prose alone. The mathematical paper is useful only if its publication identity is explicitly expository/tutorial/methods-oriented, or if a genuinely new theorem/application is added later.

**Revision response:** The paper now says exactly this. The title no longer advertises a new named theory; the abstract says it is an expository synthesis; the introduction says numbered results are not priority claims; and current/older antecedents were added.

### Hostile Referee 2 - conceptual/operational attack

**Attack:** "The paper risks conflating a complete 0/1 semantic signature with an actual partial stream of positive observations; its distances are presentation-dependent; the inference results are essentially tautological; categorical pullback language overstates an intersection; and the late homology/contextuality material looks like scope inflation."

**Assessment:** **Partly sustained, with no correctness failure.** The complete-signature/partial-transcript distinction was already present and mathematically correct, but it needed to be more central. Presentation dependence is real. The inference and pullback material was overlong relative to its novelty. The later scope material was too broad.

**Revision response:** The complete-profile caveat is retained; presentation dependence is now explicit in the distance section; the inference/pullback exposition was shortened; and the scope section was narrowed.

## 3. Mechanical correctness and reproducibility

A fresh finite exhaustive checker was written for the central finite claims. It tested generated topologies, upward-signature representation, indistinguishability, specialization, smallest neighborhoods, two-sided partition topologies, T0/T1 behavior, weighted Hamming and directed-loss distances (including triangle inequalities and topology generation), and finite interior/closure formulas.

**Result:**

> PASS: 648,308 theorem/example checks across 5,054 arbitrary finite observation presentations (carrier size 1..4, observations 0..3).

This is strong regression evidence, not a formal proof assistant certification and not a substitute for peer review. All 13 numbered theorem/proposition/corollary statements remain in the revised manuscript.

The final LaTeX build completes without undefined references, overfull boxes, or LaTeX warnings. The final PDF was rendered and visually inspected, and a before/after render comparison was performed.

## 4. Priority and literature check

The revised positioning is supported by several close antecedents:

- S. Abramsky and S. Vickers, "Quantales, observational logic and process semantics," *Mathematical Structures in Computer Science* 3 (1993), 161-227, DOI 10.1017/S0960129500000189.
- A. Achilleos and V. Kyriakou, "A Topological Framework for Finite Behavioural Observations and Verification," arXiv:2606.23975 (2026). This is a particularly important recent conceptual precedent for topologies generated by finite observations.
- O. Dovgoshey and R. Shanin, "On the closure of one point sets in T0-spaces," *Topology and its Applications* 382 (2026), 109756, DOI 10.1016/j.topol.2026.109756. They establish broad quasi-metrizability of T0 Alexandrov spaces.
- Z. Pei, D. Ruan, D. Meng, and Z. Liu, "Formal concept analysis based on the topology for attributes of a formal context," *Information Sciences* 236 (2013), 66-82, DOI 10.1016/j.ins.2013.02.027.

These sources make it inappropriate to sell the paper as a theorem-level priority claim for the general observation-topology or quasi-metric ideas. They do not invalidate the manuscript's narrower value as a coherent finite propositional synthesis.

No literature search can prove the nonexistence of an even closer antecedent. The defensible strategy is therefore the one now used in v0.9: make no broad novelty claim, cite the closest known traditions, and let the contribution be the integrated exposition.

## 5. Publication-readiness scorecard - revised v0.9

The numerical average is secondary to the hard distinction between **expository submission** and **original-research submission**.

| Category | Weight | Score / 10 | Confidence | Principal finding |
| --- | ---: | ---: | --- | --- |
| Mathematical correctness | 20% | **9.5** | High | All 13 numbered claims survived reconstruction and the finite exhaustive regression suite. |
| Completeness of proofs/results | 8% | **9.1** | High | Proofs cover their stated finite scope; no hidden use of an unproved research claim was found. |
| Model and assumption discipline | 8% | **9.4** | High | Complete signatures, positive evidence, two-sided observation, presentation data, and premise restriction are explicitly separated. |
| Novelty and priority | 12% | **5.5** | Moderate | Core mathematics is largely classical; the defensible contribution is synthesis, not theorem-level priority. |
| Scientific significance | 8% | **6.8** | Moderate | Useful conceptual/pedagogical integration, but no new algorithm, invariant, complexity result, or validated application. |
| Literature coverage and positioning | 8% | **8.8** | High | Added direct observational-logic, 2026 observation-topology, 2026 quasi-metric, and topology/FCA antecedents. |
| Reproducibility | 7% | **9.4** | High | Buildable source plus an executable finite regression checker with 648,308 passing checks. |
| Internal consistency | 6% | **9.4** | High | Terminology and scope now agree with the explicitly expository identity. |
| Resolution of prior reviewer concerns | 5% | **9.2** | Moderate-High | Known issues in the supplied review record and the fresh hostile passes were addressed; full historical referee texts were not bundled. |
| Exposition and readability | 5% | **9.2** | High | Stronger title/abstract, comparison table, running example, and shorter inference section. |
| Scope and structural focus | 4% | **9.1** | High | Contextuality/connectedness digressions removed; nerve material kept only as a presentation-dependence caution. |
| Evidence and citation quality | 4% | **8.8** | High | Primary/foundational references now support the main positioning claims; exact exhaustive priority clearance remains impossible. |
| Submission hygiene | 3% | **9.4** | High | Clean 19-page build, consistent metadata/title, keywords, no build warnings, no internal workflow prose. |
| Venue/form fit | 2% | **8.5** | High for expository venues | Strong fit as an expository/tutorial note; weak fit if submitted to a venue expecting a new research theorem. |

**Weighted score: 8.60 / 10.**

The relatively low novelty score is intentional and should not be "repaired" by stronger novelty language; doing so would make the paper less defensible.

## 6. Final handling-editor judgment

### Expository/tutorial submission

**READY FOR SUBMISSION**, subject only to adapting the LaTeX to the target venue's house style and confirming that the byline is the intended publication name. I would be comfortable releasing this v0.9 as a public preprint explicitly labeled as an expository/tutorial note.

### Original-research submission

**NOT READY AS AN ORIGINAL-RESEARCH PAPER.** The blocking issue is not correctness or exposition. It is that the central finite topology, specialization, Hamming, quasi-metric, and semantic-consequence ingredients are established mathematics. A research-journal submission that markets these as new results would be vulnerable to an immediate novelty rejection.

### What would change that second judgment

A genuinely new result could justify a separate research version: for example, a nontrivial observation-selection/minimality theorem, complexity classification, new invariant, or a validated application where the topology yields a result not obtained by ordinary set/FCA/rough-set language alone. That work should be added only if it is independently substantive; the present expository paper should not be inflated merely to raise a novelty score.
