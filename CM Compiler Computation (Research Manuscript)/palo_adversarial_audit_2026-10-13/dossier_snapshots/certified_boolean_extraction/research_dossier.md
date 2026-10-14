# Certified Boolean extraction: novelty and feasibility dossier

Research date: **13 October 2026, Asia/Bangkok**. Direction 2 only. This is a research assessment, not a finished paper, priority clearance, independent referee report, or general neural verifier.

## 1. Decision

**RESHAPE and MERGE WITH EXISTING Guarded Dispatch for now.** Pursue a bounded follow-up to decide whether a separate paper is justified. The generic title *Certified Boolean Operators from Differentiable Models* promises a capability that already has substantial antecedents. The defensible question is narrower: how does the geometry of a certified operator dictionary constrain the number, degree, and actual cost of observations needed to identify its operator, and when can that result be used on continuous regions rather than sampled representatives?

The current evidence supports three additions to the existing note: a stronger closest-work comparison, a conditional family theorem extending its four-label star, and a concrete exact range-certificate example. It does **not** yet support a separate general extraction, learning, or dynamics paper. A distinct paper becomes credible only if the family theorem develops beyond a simple star generalization and the implementation provides useful coverage or certificate reuse on an independently motivated family at an honestly measured total cost.

Target readership: formal methods and neuro-symbolic methods researchers interested in small interpretable modules; secondarily real algebraic geometry and exact identification researchers. The present material fits a focused mathematical methods note better than a general neural-learning or high-performance compilation article.

Main reasons:

- Guaranteed rule extraction substantially predates this project. Thrun's primary 1995 proceedings paper explicitly verifies rules over continuous regions.
- Guarded Dispatch already contains the sign quotient, nonempty-guard certification, zero-aware collecting semantics, reduced observations with a proved dictionary, representation invariance, and elementary trajectory results.
- Averkov and Bey supply a particularly close degree/cardinality and coding precedent, beyond the more general Averkov–Bröcker citation already in the note.
- A small exact demonstrator succeeds on a restricted polynomial family. It has no trained-network or PALO evidence, and its range theorem is classical.
- CM/LM provides a convenient typed endpoint. No extraction or cost theorem here disappears if it is replaced by an ordinary truth table with the same metadata.

## 2. Source and version audit

The handoff report was read first, including its evidence policy, source inventory, README, and the guarded-extraction discussion. Its 40,668 earlier rational assertions were **not rerun** or counted as this investigation's evidence.

The four relevant portfolio folder guides and the selected bundles explicitly point to the supplied versions. No newer authoritative manuscript was identified by those navigation files. This is a scoped navigation audit, not a search through every historical ZIP. The guides can lag the actual manuscript: Guarded Dispatch's older GU3 summary omits its stronger degree/test theorem, and the LM top-level guide mentions an old checker-recovery issue that the September 27 bundle reports resolved. Claims below follow the actual selected manuscripts. Modification times were not used to select authority.

All five local PDF SHA-256 values match the handoff inventory. Exact paths, sizes, hashes, and page counts are in `local_sources.json`; the consulted navigation content and its hashes are in `version_navigation.json`.

| Key | Authoritative local version used | Decisive locators and role |
|---|---|---|
| GU | *Guarded Boolean Operators: Exact Dispatch and a Polynomial Guard-Degree Tradeoff*, September 28 reviewed package, 14 PDF pages | Proposition 2.1 pp. 2–3; Theorem 2.2 pp. 3–4; Remark 2.3 p. 4; Lemma 3.1 and Theorem 3.2 pp. 5–6; Propositions 4.1–4.3 pp. 7–8; Proposition 5.1 pp. 9–10; Proposition 5.2 p. 10; Appendix A.1 pp. 11–12. |
| LM | *Correspondence and Logical Matrices: A Typed Boolean Operator Calculus*, September 27 revised manuscript, 32 pages | Theorem 3.1 pp. 7–8; pairing Theorems 4.1/4.4; Theorem 5.4 p. 12; Theorems 6.6 and 6.12 pp. 14–15. |
| COMP | *Operator-Level Boolean Computation with Correspondence Matrices*, September 26 contract revision, 19 pages | Sections 1–3 pp. 1–3; typed compilation Sections 4–5; costs Section 5.4 pp. 8–9; comparators Section 6 pp. 9–10; negative evidence Section 7 and current navigation. |
| PALO | Supplied 57-page author manuscript, first page dated December 2020, publication notice 2021 | Sections 3.5–3.8 pp. 23–27; Section 4 p. 28 and note 29. Journal record: JLAMP 124, 100719, January 2022; DOI 10.1016/j.jlamp.2021.100719. |
| FJ | *Finite-Jet Sign Rigidity on Hyperplane Arrangements and Denjoy–Carleman Realization*, September 27 final submission candidate, 14 pages | Introduction p. 1; common-corner Theorem 4.1; arrangement Theorem 4.5 and Remark 4.6 p. 7; scope table p. 11. Used only to audit the specification. |

The polynomial tests and decoding table on GU p. 6 were also rendered and visually checked. Extraction of the PALO PDF issued malformed-object warnings and some mathematical glyphs are poor in text; its section-level assertions were checked against the equations and prose, with the handoff source as orientation. No source manuscript was changed.

Initial repository status was dirty, with many tracked modifications and untracked research/work directories. The first read-only status is visible in this chat; `initial_git_status.txt` records the working-tree status after this exclusive output directory was created, before research implementation. No source files were edited, staged, committed, or pushed. There were no additional root/ancestor/output `AGENTS.md` files at the paths checked; the supplied Brian guidance and handoff restrictions apply. Sibling chats share the tree, so final global status cannot uniquely attribute concurrent changes.

## 3. Closest primary work

The annotations distinguish results stated by the source from this investigation's interpretation. PDF page references below are one-based physical pages unless journal pages are given. Bibliography keys match `references.bib`. Downloaded texts are research working copies, not intended for public redistribution.

### 3.1 Verified rules and Boolean extraction

**Thrun [thrun1993, thrun1995, thrunAuthorCopy].** [Author bibliography](https://web.stanford.edu/~thrun/papers.html); [published NIPS 7 paper](https://proceedings.neurips.cc/paper_files/paper/1994/file/bea5955b308361a1b07bc55042e25e54-Paper.pdf), pp. 505–512, especially Section 2 pp. 506–507 and Section 3 pp. 507–509. Validity Interval Analysis uses conservative activation constraints to verify conjectured region rules; failure to find a contradiction is inconclusive. This directly defeats a broad priority claim for certified continuous-to-symbolic extraction. Its region search/verification is not the proposed polynomial observation-cost theorem.

**Important retrieval discrepancy:** the author's link labelled the 1993 report actually downloads a 48-page PostScript work titled *Extracting Symbolic Knowledge from Artificial Neural Networks*. That copy was obtained, converted with installed Ghostscript, and read: Sections 2 and 3.1, PDF pp. 5–8 and 14–17, printed pp. 3–6 and 12–15. It independently supports the verification contract, but is not silently identified with the exact IAI-TR-93-5 version. CiteSeer mirrors of the specifically titled report were found but could not be opened as full documents. The proceedings paper and its reference [14] verify the report title, identifier, and May 1993 date.

**Mereani and Howe [mereani2019].** [Publisher full text](https://www.scitepress.org/Papers/2019/83629/83629.pdf), Section 3.4 pp. 427–428, PDF pp. 4–5; publication metadata [here](https://www.scitepress.org/PublishedPapers/2019/83629/). They enumerate an exact Boolean function for a network with small Boolean input space, minimize it, and use sampling for larger spaces. This is a direct antecedent for representative-only truth-table extraction. It does not certify a rule throughout a continuous predicate cell or a parameter region. The paper's recognition of exponential table size also prevents claiming compression from CM reshaping.

**Wurm [wurm2025].** [arXiv v1 full text](https://arxiv.org/html/2509.16547v1), Definitions 1–5, Proposition 1 pp. 3–4, Proposition 2 p. 4, Theorems 3–4 pp. 5–6. It reports co-NP completeness for verification of several rational ReLU/Boolean rule classes; its consistency/exhaustiveness questions are separately quantified. Exhaustiveness concerns uniquely determined raw outputs, not merely a thresholded bit. Definition 5 uses “at most one,” so existence must be treated separately. These are barriers to a general efficient extractor, not theorems about the small bilinear family. Do not repeat its broad “no prior verification” language: the Thrun passages refute that reading. Crossref confirms an **IJCNN 2025 publication**, DOI [10.1109/IJCNN64981.2025.11229308](https://doi.org/10.1109/IJCNN64981.2025.11229308), pp. 1–7; this direction should no longer describe it only as a 2025 preprint. The publisher full text was inaccessible; the read version is arXiv v1. Its proofs were read for scope, not independently audited in full.

### 3.2 Polynomial descriptions, coding, and identification

**Averkov and Bey [averkovBey2011].** [Author journal PDF](https://www.math.uni-luebeck.de/mitarbeiter/bey/pub/description_of_polygonal_regions_by_polynomials_of_bounded_degree__10_AVERKOV_BEY.pdf); [arXiv full text](https://arxiv.org/html/1002.0941v1). Theorems 1.1–1.2, Proposition 2.1, Lemmas 2.2–2.3, Proposition 2.4, and Theorem 3.1, arXiv PDF pp. 2–7, are decisive. They relate polynomial degree and inequality count, use boundary-factor divisibility, and formulate product guards using binary incidence matrices and Gray codes. This is the closest mathematical antecedent found. Their objective is a polygon's membership description, with path-like visibility conditions; ours jointly identifies many labels on a promised domain and can have star adjacency. That difference is precise but does not make the mechanism new. Journal: *Monatshefte für Mathematik* 162(1), 19–27; DOI 10.1007/s00605-010-0224-x, online 2010, issue 2011. Regenerated HTML dates are not publication dates.

**Averkov and Bröcker [averkovBrocker2013].** [arXiv v1](https://arxiv.org/abs/1002.0921), Theorems 1.1–1.2 p. 1 and Section 3 pp. 4–5. Polynomial-description cardinality without a fixed guard-degree restriction is established prior work. This paper uses conjunctions of inequalities to describe sets, rather than decoding a multi-label signature. It supplies context, not a neural certificate algorithm. The downloaded PDF contains a later typesetting date while its arXiv identity is v1 from February 2010. The journal DOI is 10.1515/ADVGEOM-2011-059; full publisher access and Crossref lookup failed, so the reviewed theorem version is explicitly the arXiv manuscript.

**Anthony [anthony2026].** [June 28, 2026 v1](https://arxiv.org/abs/2606.29477); [full text](https://arxiv.org/html/2606.29477v1), Theorem 3.3 pp. 9–11, Proposition 4.3 pp. 15–16, Proposition 4.19 pp. 21–22. It identifies target-specific specification sets with chamber facets for threshold and polynomial-feature classes. The entire promised class matters: these are not fixed global test sets or adaptive oracle costs. This substantially overlaps geometric teaching/certificate interpretations, but does not supply the original-coordinate bounded-degree polynomial dispatch library studied here. Its references locate earlier signature results, including Anthony–Brightwell–Shawe-Taylor and Zuev; no priority should be attached to a facet/specification analogy. Read as a current preprint, not an established journal theorem.

**Classical test selection [moret1985, chaki2003].** GU already acknowledges minimum distinguishing tests and minimum predicates. A hitting-set formulation or a known-dictionary query bound is not a new extraction algorithm. The primary DOI records are [Moret–Shapiro](https://doi.org/10.1137/0906067) and [Chaki et al.](https://doi.org/10.1007/978-3-540-39724-3_5). Their full texts were not obtained in this investigation; they remain background citations from GU, not newly audited theorem comparisons. The actual small star query bound is proved below without relying on them.

### 3.3 Verification, composition, and uncertainty

**Xie, Kersting, and Neider [xie2022].** [IJCAI 2022 full text](https://www.ijcai.org/proceedings/2022/0503.pdf), Section 4 pp. 3624–3626, particularly specification networks and NeSAL. Neural proxies can supply semantic predicates inside logical specifications; verification reduces to existing infrastructure. This is close to a concept-predicate extraction interface. A certificate relative to a learned proxy does not establish the proxy's ground-truth meaning. Our proposed certificate must similarly identify the actual predicate map and its encoding assumptions.

**Vehicle [vehicle2025].** [FSCD 2025 publication](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSCD.2025.2), arXiv v2 June 6, 2025; Sections 2.1–2.3 PDF pp. 2–5, Sections 4.1–4.2 pp. 7–10, future work pp. 14–15. Vehicle already links problem-space properties, embeddings, training, neural verification, and theorem-prover use through a typed interface. This is a strong architectural precedent for compositional certificates. Its future-work section explicitly says the theorem prover currently trusts Vehicle's verification assertion and discusses checking solver certificates. A small independently replayable arithmetic certificate is a narrower implementation choice, not a general solution to the embedding gap. LM coherence cannot replace the embedding and range obligations.

**DeepPoly [singh2019].** [Primary full text](https://files.sri.inf.ethz.ch/website/papers/DeepPoly.pdf), Section 4, Theorems 4.2–4.5 pp. 12–15, and Section 4.7 pp. 16–17. Sound abstract transformers bound neural outputs over actual regions, with explicit floating-point rounding treatment. This is a stronger relevant baseline than representative sampling or plain intervals for supported neural networks. A bound that straddles zero is unresolved, not proof of mixed behavior. DeepPoly was read but not executed; the bilinear demonstrator does not claim support from its affine/ReLU machinery for multiplication nodes.

**Abate, Edwards, and Giacobbe [abate2022].** [Neural Abstractions full text](https://arxiv.org/html/2301.11683v1), Definitions 1–2 and Theorem 1 PDF pp. 4–5; Sections 3.2 and 4.2 pp. 6 and 8. NeurIPS **2022**, arXiv posting January 2023. They certify approximation error for a neural ODE plus bounded nondeterministic disturbance, transfer trajectory safety, and enumerate feasible activation modes. This is a useful pattern for region certification and infeasibility handling, but the abstraction is a dynamics overapproximation, not an exact Boolean operator. It would be incorrect to cite its soundness as our discrete extraction theorem.

**Vinzent, Hermanns, and Hoffmann [vinzent2026].** [AAAI 2026 full text](https://ojs.aaai.org/index.php/AAAI/article/view/40965/44926), preliminaries pp. 36439–36440; Definitions 1/3 and Proposition 4 p. 36440; Algorithm 1 p. 36442; Theorems 5–8 p. 36443. Publication metadata confirms March 14, 2026, 40(43), 36438–36447, DOI 10.1609/aaai.v40i43.40965. Policy predicate abstraction and probabilistic CEGAR reason about reachable transition systems and spurious paths/distributions; a common-start-state condition is essential. The termination argument uses **finite bounded-integer concrete states**, not arbitrary continuous inputs. This is a powerful reachability baseline, not a directly applicable polynomial sign atlas. Its technical report proofs were not separately audited. The web tool read the complete relevant passages despite local download failures.

**Manginas et al. [manginas2025].** [Current v2](https://arxiv.org/abs/2502.03274), Section 3.1–3.3 PDF pp. 4–6, Proposition 2 p. 5 and Appendix B. This is the July 29, 2025 version titled *A Scalable Approach to Probabilistic Neuro-Symbolic Robustness Verification*, associated with NeSy 2025. Exact interval optimization through weighted model counting has an NP^PP-complete decision core; the proof uses the familiar multilinear vertex-extremum fact. Their end-to-end bound propagation makes a broad claim for “certifying neuro-symbolic reasoning” especially untenable here. Our strict bit certificate has a different target and avoids weighted counting only by restricting the problem. It does not preserve soft query probabilities.

### 3.4 Evolution and reuse

**Fischer et al. [fischer2022].** [Shared Certificates, v4](https://arxiv.org/html/2109.00542v4), Problems 1–3 pp. 3–7, Theorems 1–2 pp. 7–8; CAV 2022 publication DOI 10.1007/978-3-031-13185-1_7. The current arXiv text is revised November 2023. Intermediate-layer templates already support sound proof reuse through containment tests. A claim that the LM output newly makes certificates reusable would duplicate this idea unless it supplies an additional measurable mechanism. Boolean label reuse alone is weaker than these range templates.

**Ugare et al. [ugare2023].** [Published author PDF](https://debangshu-banerjee.github.io/assets/pdf/Ivan.pdf), Sections 4.2–4.4 pp. 12–17, Theorems 2–4; PLDI 2023, DOI 10.1145/3591299. IVAN reuses branch-and-bound structure across changed networks. Its special perturbation theorem concerns last-layer changes; experiments have wider scope. This is a direct predecessor for parameter persistence/reverification. **Zhang et al. [zhang2025]**, [OLIVE](https://doi.org/10.1145/3720417), Definitions 2–3 and Section 4.3, extends incremental verification with counterexample-oriented ordering. That publisher's full displayed definition/algorithm passage was read; no local full PDF or rerun was obtained.

**Cummins et al. [cummins2016, cummins2026].** [2016 parameter decomposition](https://arxiv.org/abs/1512.04131); [June 12, 2026 Boolean/refinement preprint](https://arxiv.org/html/2606.14925v1), Sections 3.4.1–3.4.2 pp. 21–22, Definitions 3.40–3.41 and Theorem 3.43 pp. 32–33. Structured regulatory models already organize parameters, adjacency, and richer multilevel dynamics. Our sign events describe changes of an extracted table, not attractors or biological evolution. An operator-transition graph alone cannot compete with DSGRN's dynamical content.

**Anani et al. [anani2026].** [Current primary manuscript](https://arxiv.org/abs/2602.22968), v3 May 28, 2026; Section 3.3, Theorem 3.1 PDF p. 5 and Appendix A. Certified Circuits concerns stability of discovered circuit membership under edits to a concept dataset, using randomized deletion and confidence bounds. It is not exact input-region Boolean extraction or parameter-trajectory persistence. The current author page identifies ICML 2026, but the read theorem version remains the arXiv v3; preliminary v1 headline numbers were not used.

### 3.5 Citation paths and search limits

Backward/forward chains actually followed:

1. The Thrun bibliography → author-linked report copy → published NIPS 7 paper and its 1993 reference → Mereani–Howe's Boolean extraction and later DEXiRE citation to Thrun.
2. GU → Averkov–Bröcker → Averkov–Bey → their boundary-factor proposition, coding/Gray-code reformulation, and cited earlier polygon descriptions. Only the decisive Averkov papers were read in full relevant sections; older Gray-code papers are not independently audited.
3. Wurm → its exact rule definitions and complexity propositions; targeted title/citation searches → IJCNN publisher DOI metadata. No exhaustive forward-citation database result was available.
4. Vehicle → Xie/NeSAL and perception-contract literature; Vehicle's own embedding and proof-certificate limitations. Perception Contracts DOI 10.1145/3622875 was inspected as an adjacent source; no new full-proof claim is based on it.
5. Shared Certificates → IVAN → OLIVE, separating reuse across inputs from reuse across changed networks.
6. GU's DSGRN links → 2016 framework → 2026 Boolean-refinement paper.

Search families included certified/provably correct neural rule extraction, Boolean-feature exact extraction, polynomial degree/sign-test/cardinality, bounded-degree polygon descriptions, neural concept verification, proof-sharing/incremental verification, and current 2026 work. Searches were conducted through the current date, including June/May 2026 sources; this is not an exhaustive survey or proof of historical priority.

Access limits: CiteSeer report mirrors and some publisher DOI pages failed; ECAI 2024 *Automated Synthesis of Certified Neural Networks* full PDF was forbidden; Vinzent local download failed twice but the web tool supplied the full relevant PDF passages; OpenReview requested a browser challenge, so Manginas was read via current arXiv v2. No challenge or authentication safeguard was bypassed. Crossref confirmed selected metadata but one request returned HTTP 429. `bibliographic_metadata.json` and `literature/retrieval_manifest.json` retain these outcomes. Full source warnings and regenerated dates are not silently treated as authoritative version evidence.

## 4. Precise extraction contract

Let `Z ⊆ X × Θ` be a declared joint region. `Θ` is parameter space, `X` actual model input space. A fixed model uses a singleton parameter set. A parameter-only study uses fixed declared representatives `r_α(θ)`. These are different specifications.

For a **region** specification choose a total predicate map `P:X→{0,1}^n` with a declared equality policy. Put `Z_α = {(x,θ)∈Z : P(x)=α}` and `s(x,θ)=N_θ(x)−τ`. A strict Boolean interpretation is `q(s)=1` for `s>0`, `0` for `s<0`; it is undefined at zero. The extraction is exact at `α` only when `Z_α` is proved nonempty and all its scores have one strict sign. A full canonical table requires this for every α. Otherwise export the reachability mask and partial facts; an arbitrary completion is not uniquely specified by the model.

For each cell the semantic object is the **attained set** `S_α⊆{−,0,+}`. A solver's overapproximation is a separate object `Ŝ_α` containing it. Keep the following evidence separate:

| Result | Required evidence | What it permits |
|---|---|---|
| UNREACHABLE | Certified emptiness of `Z_α` | Mark the cell absent; no invented output bit. |
| STRICT_TRUE / STRICT_FALSE | Nonemptiness and uniform strict sign | An exact bit on the entire declared cell. |
| MIXED | Actual positive and negative witnesses in that cell | Refute a constant strict bit. A zero is not implied on disconnected cells. |
| TIE_PRESENT | An actual zero witness or exact existence proof | Strict interpretation is not total on that cell. This flag can coexist with MIXED. |
| UNKNOWN | Unsupported class, inconclusive bound, timeout, or unchecked solver answer | Retain uncertainty. No assertion of mixedness or emptiness. |

PALO's Section 3.7 gives threshold equality a total crisp meaning; strict abstention is an **additional chosen certification policy**, not a claim that PALO leaves ties undefined. Its crispification is inserted inside interpretation. The adapter must specify threshold placement and equality policy. Certifying only the final soft score computes another interpretation.

The certificate should bind model/weights identity, real versus floating-point arithmetic, input and parameter domains, predicate/encoding identity, threshold/equality convention, axis/polarity order, nonemptiness, range or sign obligations, checker/backend versions, and uncovered cells. A certificate need not put every item inside a CM: it is metadata plus evidence accompanying the output.

For a solver implementation, use existential queries for emptiness and each sign/zero possibility. UNSAT can establish an exclusion only under a sound trusted solver or replayed proof. SAT with an exactly validated witness establishes existence. UNKNOWN is kept. Many verifiers return trusted decisions rather than portable proof objects; call those solver-validated results and disclose the trusted computing base.

## 5. Preferred research question and theorem development

**Preferred question:** For certified polynomial operator atlases with stated boundary geometry, what is the optimal maximum degree of a fixed binary sign library identifying every label, and how do those bounds change when certificates and feature computation are charged?

The reason to prefer this question is that it supplies an actual mathematical extension of GU, whereas returning a table plus a uniform-sign assertion merely repackages existing certification. The results below are **derivations with supplied arguments, not novelty claims**. They should receive an independent proof/priority review before a manuscript asserts them as its main contribution.

### 5.1 A weighted star theorem under explicit geometry

Assume:

1. `h_1,…,h_q` are pairwise nonassociate irreducible real polynomials in fixed original coordinates, degrees `e_j>0`.
2. On an open ambient domain `U`, outside their zero sets, the only realized sign patterns are all-negative (label 0) and exactly one positive (label j). Every label is nonempty.
3. For each j there is a relatively open regular boundary patch `C_j⊂{h_j=0}` separating labels 0 and j, with all other h nonzero nearby.
4. Each patch is algebraically determining: any polynomial vanishing throughout `C_j` is divisible by `h_j`. This is an explicit hypothesis, not inferred merely from irreducibility when there are no regular real hypersurface points.

For **tests required to be constant on each label**, `k` polynomial indicators `1{H_i>0}` identify the atlas with degree at most `d` if and only if there is an injective code `c:{0,…,q}→{0,1}^k`, normalized to `c(0)=0`, such that

`max_i Σ_{j:c(j)_i=1} e_j ≤ d`.

Necessity: exact decoding makes label signatures distinct. Whenever the bit differs across boundary j, `H_i` must vanish at every point of its boundary patch; otherwise continuity would keep the bit unchanged in a neighborhood. Hypothesis 4 forces `h_j | H_i`. Distinct irreducible factors are relatively prime, so their total degrees add. Normalizing the abstract code by XOR with the base signature preserves these cuts; it does not require taking a pointwise complement of indicators at their zeros.

Sufficiency: for each row use

`H_i = (−1)^(|B_i|+1) ∏_{j∈B_i} h_j`, where `B_i={j:c(j)_i=1}`.

The base has a negative value; a leaf flips the sign precisely when its index belongs to `B_i`. The empty product with the displayed prefactor is `−1`. All such tests are nonzero on the promised domain and their degrees equal the stated loads. They therefore implement the code exactly.

This is an exact reduction to a weighted code-assignment problem **for this guard contract**. It is closely related to Averkov–Bey's product/factor coding methods. It is not a general guard-synthesis theorem for arbitrary networks.

### 5.2 Removing label constancy at information saturation

If `q+1=2^k`, any exact library of k binary tests uses all possible signatures. Each label must get exactly one signature: it needs at least one, and signatures for different labels cannot overlap. Consequently the preceding theorem applies **even when individual tests were not required to be constant on labels**.

For equal boundary degree e, every coordinate of a saturated code differs from the base on exactly `2^(k−1)` leaves. Thus each of the k polynomials has degree at least

`d_min = e·2^(k−1)`,

and the product construction attains it. Fewer than k tests cannot identify `2^k` labels. This gives an infinite family of sharp thresholds for achieving the information minimum, extending GU's q=3, e=2, k=2 calculation. It does **not** give the entire `m_d` curve for arbitrary numbers of labels or unsaturated libraries.

A concrete realization uses `U=R²` and `h_j(u,v)=1−(u−4j)²−v²`. Their positive unit disks are pairwise disjoint, boundaries are regular irreducible circles, and the all-negative exterior is nonempty and connected. Every boundary has an algebraically determining arc. For seven leaves (eight labels), three tests each need degree at least eight. A smooth coordinate transformation cannot turn all seven circles into one global family of disjoint straight full boundary lines on the whole plane; however, the theorem still restricts the **original coordinate guard language**, and feature maps or domain-specific embeddings can change the costs. The circles are a mathematical construction, not evidence of a natural trained operator family.

One can realize the sign dictionary as Boolean representative scores using minterm interpolation in separate Boolean input variables; this proves feasibility of a polynomial model family at finite representatives. It does not certify that each rule is uniform on entire open orthants. Distinguish this synthetic realization from the separate continuous boxes in the demonstrator.

### 5.3 Boundaries and remaining proof obligations

- With `q+1<2^k`, spare signatures permit a polynomial test to vary within a label. The weighted code reduction supplies an upper bound for unrestricted tests but has **no general optimality proof**. Do not generalize the saturated counting argument.
- A general finite exact library still has to cover every discriminant patch with a zero set. This yields the necessary total-degree bound `Σ_i deg(H_i)≥Σ_j e_j` under the determining-patch hypothesis, in addition to `2^k≥q+1`. Those bounds need not be sharp.
- For non-star atlases, assigning one code to each chamber gives weighted boundary-cut lower bounds. Product guards achieve them only when their parity pattern is globally realizable. Repeated factors, multiple boundary components, cycles, nonseparating hypersurfaces, and shared operator labels must be treated explicitly. A graph alone is insufficient to prove an upper bound.
- Adaptive polynomial queries have another contract. The fixed-library theorem does not establish optimal adaptive depth. At e≤d<2e, boundary factor coverage rules out combining two equal-degree factors into one test, but an adaptive branch can exploit a smaller promise domain. Analyze that domain before transferring a lower bound.
- Weighted code synthesis must account for bit complexity and shared arithmetic. No NP-hardness or polynomial-time algorithm claim for that optimization has been proved here.

**A useful next theorem, still unproved:** characterize when a certified non-star atlas admits an optimal degree-bounded code by products of its irreducible boundary factors, including the unsaturated case. This has a stronger potential mathematical contribution than merely replacing three star leaves by seven.

### 5.4 Coordinate-query separation

For the dictionary consisting of one base table and q leaves, each differing from the base at its own single coordinate, a fixed truth-coordinate basis must include all q distinguishing coordinates. A deterministic adaptive algorithm also needs q queries in the worst case: on the base every answer is the base value, leaving the leaf at any unqueried coordinate possible. A leaf has a one-query target-specific certificate. These elementary statements generalize GU Proposition 5.1, but are classical exact identification, not a new learning result. Arbitrary coded polynomial observations can reach `ceil(log2(q+1))` only under the different input/feature observation contract and adequate degree.

## 6. Tractable certification and completed demonstrator

`exact_extraction_demo.py` uses only Python's standard library, exact rational arithmetic, and the family

`F_{D,A,B,C}(x,y)=D+A x+B y+Cxy`.

For Boolean input α it substitutes `x=(2α_1−1)a`, `y=(2α_2−1)b`. Coefficients and positive magnitudes range independently over a rational compact box. The resulting score is multi-affine in the **six variables** `(D,A,B,C,a,b)`. It includes a bias and coefficient sign changes, unlike the positive rescaling already in GU Remark 2.3. It remains a deliberately small, tractable family.

**Classical corner theorem, used here:** a multi-affine real scalar function on a box is a convex combination of its vertex values, using tensor products of the one-dimensional interpolation weights. Hence min and max are attained at vertices. The connected box and continuous score attain every value between those extrema. This permits exact sign-set classification, including actual mixedness and ties, for this special backend. Compact degenerate boxes are allowed; a reversed interval proves emptiness. Independent boxes with up to p active variables require `2^p` vertices per score: tractability is bounded-dimensional, not a dimension-free claim.

The producer returns bounds, extremal witnesses, the exact attained sign set, strict/partial table status, and a hash binding model/frame/domain. A separate replay path recomputes all vertices using direct F rather than the producer's expanded signed score, checks witness membership, recomputes statuses, and rejects modified domains, frames, ranges, and labels. Universal soundness rests on the corner theorem. The implementation is an arithmetic checker, not an independently formally verified proof kernel.

Completed results in `demo_results.json`:

| Check | Outcome and implication |
|---|---|
| Continuous input boxes around magnitude 1/2 | AND certified throughout all four sign boxes for a,b∈[2/5,3/5]. |
| Joint input/parameter box | AND certified with D∈[−1/100,1/100], A,B,C∈[99/100,101/100], same input box. |
| Natural interval baseline on those two cases | UNKNOWN on both; exact corner certificates are EXACT. For fixed coefficients, h1's natural enclosure is [−14/25,1/25], while its true range is [−11/25,−1/25]. This is a precision comparison only. |
| Mixed region a∈[1/2,2], b=1/2 | Positive and negative witnesses for h1; no constant operator emitted. |
| Boundary a=1, b=1/2 | Zero retained as TIE_PRESENT. |
| Empty box / unsupported model | UNREACHABLE / UNKNOWN, respectively; unsupported input-axis positivity also yields UNKNOWN. |
| All 16 binary tables | Realized at a=b=1 using inverse Walsh coefficients, with all four coefficients perturbed independently by 1/20; margin 4/5 certifies the table over the parameter box. These input representatives are singletons, not continuous-input region certificates. |
| Original x+y+xy dispatcher | 576 exact rational points agree with quartic decoding or retain boundary status. |
| Multi-affine interpolation | 2,916 exact assertions across a 3^6 grid and four truth inputs. Finite identity checks support implementation; the written interpolation argument is the universal proof. |
| Star signatures and witnesses | Codes for 2,4,8,16 labels; seven-disk rational witnesses; one weighted q=3 minimax example. These do not establish universal polynomial lower bounds by enumeration. |
| Evolution / scope counterexamples | Equal endpoint tables can hide changes; a non-multi-affine score defeats corner-only certification; a disconnected cell can contain both strict signs and no zero. |

**Total: 3,587 passing assertions.** No training, PALO/LIME integration, generic SMT implementation, constrained polytope backend, floating-point verifier, BDD runtime, or timing benchmark was run. No performance advantage follows from the assertion count.

Reproduce from the project root:

```powershell
& .\.venv\Scripts\python.exe .\output\research\palo_paper_directions_2026-10-13\certified_boolean_extraction\exact_extraction_demo.py
```

The script writes only `demo_results.json` beside itself. A normal Python >=3.10 interpreter also works. Dependencies were not installed.

## 7. Sound composition and CM/LM's actual role

**Elementary derived composition statement.** Suppose exact certificates establish `q(s_i(x,θ))=f_i(P(x))` on domains `Z_i`, all using the same predicate/frame/threshold contract. On their intersection `Z_*`, any **Boolean** outer operation H satisfies

`H(q(s_1),…,q(s_m)) = H(f_1,…,f_m)∘P`.

Proof: substitute each certified equality at the same concrete `(x,θ)`. Frame changes require an actual bijection/reindexing; intersect domains and retain reachable cells. The composite can be sound even if some formal assignments are unreachable, but it is then a partial concrete abstraction; reachability of every input must not be invented.

LM Theorem 6.12 transports precisely this Boolean superposition through lift, valuation, common frame changes, and pairing. It does not manufacture the `Z_i` certificates or preserve raw model values. The separate LM Theorem 5.4 is an XOR–AND **parity kernel composition**, not ordinary functional cascade or existential relational composition. Neither theorem is an unrestricted neural composition result.

**Continuous cascade statement, an unimplemented contract:** to replace `N_2∘N_1` by composed discrete modules, one needs `β(N_1(x))=f_1(P(x))`, a certificate that every reachable intermediate value lies in the certified domain for `N_2`, and `q(N_2(z)−τ)=f_2(β(z))` on that image. Then substitution proves discrete composition. Range inclusion and interface compatibility are reusable obligations. Without them the tables alone cannot justify the replacement. Vehicle and shared-template work already offer much of this architecture.

**Replacement test:** ordinary truth tables with typed axes, region/range certificates, and the same decoder retain all of these guarantees. A BDD can also represent the extracted Boolean function and perform symbolic composition, with variable ordering and domain predicates carried separately. Replacing CM/LM loses its particular formula-valued polarity/pairing API and notation; it loses **no information, sign certificate, query lower bound, or intrinsic speed advantage**. This paper should place CM/LM in an adapter/supplement rather than make it the novelty premise.

Reciprocal value:

- For PALO: a certified strict interpretation of selected learned predicates on named regions can support exact local rules and identify where no such abstraction is justified. This adds a concrete validation contract, while leaving soft scores, gradients, dependence, and posterior semantics outside it.
- For GU: a motivated family, exact range certificates, richer degree/observation analysis, and explicit costs address its own closing limitations.
- For LM/COMP: certified tables could supply a realistic typed input workload. Existing normalization and pair compilation may execute the discrete result. The compiler's negative timing evidence makes an end-to-end advantage an open empirical question.
- For FJ: the region contract prevents misapplying whole-orthant regularity restrictions to finite representatives or boxes bounded away from the common corner. No chain-ring connection is needed here.

## 8. Falsification ledger

The strongest threats are specification errors and rediscovering established machinery. The following are actual arguments/checks, not merely suggested adversarial tests.

1. **Finite samples do not certify a cell.** On [0,1], `g(t)=(t−1/2)^2−1/100` is positive at both endpoints and negative at the midpoint. The demonstrator checks this exactly. More generally a smooth bump outside any finite sample can alter a score's sign. This refutes a general sample-to-region inference. The corner backend is sound only because it checks the declared multi-affine class.
2. **The four-label dictionary is not portable to biased models.** With D=−100, A=B=C=1 and magnitudes ≤3, all four scores are negative. The old AND/X/Y/XNOR promise is false. The 16-table check shows how dramatically the family changes when bias and coefficient signs are admitted.
3. **MIXED is not UNKNOWN.** Natural interval arithmetic straddles zero in the AND box but the exact range is strictly negative; thus a mixed conclusion would be false. Both-sign witnesses prove mixedness; only an enclosure does not.
4. **Both signs need not imply a tie.** `Z={−1,+1}`, score s(x)=x: signs {−,+}, no zero. Zero existence from min/max requires connectedness or a direct solver proof. The exact backend's box hypothesis supplies connectedness.
5. **Vacuous truth on an empty cell cannot pick a unique operator.** If P has P1=P2 everywhere, inputs 10 and 01 are unreachable. Both truth assignments there fit the actual model; the corresponding full LM is a completion choice.
6. **Threshold placement matters.** For p=q=3/5 and τ=1/2, crisp conjunction gives 1, while thresholding soft pq=9/25 gives 0. Thus a final-score extractor cannot claim to implement PALO's internal crisp semantics without an explicit adapter.
7. **Local table agreement does not justify a continuous cascade.** Positive inputs processed by `F_1(x)=x` and `F_2(x)=100x` have the same strict Boolean bit. An outer score `G(z)=z−10` distinguishes their outputs at x=1. Retained range/interface obligations, not table reshaping, are necessary.
8. **Endpoint table equality does not prove persistence.** Let the entire input-independent score be `(t−1/2)(t−3/2)`, t∈[0,2]. Endpoints have the constant-true table; the interior t=1 has constant false; all entries tie at t=1/2 and 3/2. Exact checks record these events. No single-entry transition assumption is justified there.
9. **More labels is not automatically a research contribution.** The saturated-star proof follows GU's counting/divisibility argument and a known coding mechanism. A hostile reviewer can reasonably see it as an exercise unless applications, unsaturated cases, or broader geometry add substance.
10. **Fewer sign bits can require more work.** Computing the two quartic guards from h1,h2,h3 requires the three original scores and two products. The fixed sign-library theorem does not charge that shared arithmetic. Feature lifts similarly move complexity into feature construction or reachability constraints.
11. **Uniform input signs can be impossible under an overstrong specification.** Boxes here avoid the origin. Claiming smooth AND throughout four local open orthants triggers the existing FJ regularity obstruction; proving AND on finitely many points does not address it.

## 9. Evolution along parameter/training trajectories

Treat this as a subordinate application of certificates, not an independent dynamics theorem.

A useful design would keep a certificate on a parameter tube and reuse the operator while subsequent parameters provably remain in that tube. A standard sufficient condition is a certified signed margin μ on the input region and a uniform parameter Lipschitz bound L on a containing neighborhood: perturbations of norm δ with `Lδ<μ` preserve the strict bit. Applying this to every required coordinate gives persistence. This is a derived elementary robustness fact with substantial verification antecedents, not a novelty claim.

For a known polynomial parameter path, pull back scores, isolate all real zeros with exact root certificates, and classify the complementary intervals. Record tangencies, simultaneous crossings, endpoint zeros, and identically zero scores separately. Root isolation is standard; GU already gives basic zero counts and constancy. A possible useful contribution would be amortized certificate maintenance with a demonstrated improvement over IVAN/OLIVE or full recomputation on the chosen structured family.

For actual training logs, optimizer steps are discrete. A line between checkpoints is an extra declared interpolation, not the observed dynamics. Finite logging can miss excursions or multiple transitions; monotonicity of training loss does not make predicate signs monotone. No trajectory experiment on a trained model was performed. A theorem about possible atlas paths does not establish that SGD can reach them.

## 10. Minimum credible paper package and baselines

Conditional title: **Exact Boolean Extraction on Regions: Certificates and Observation Costs**. If merged, retain GU's narrower title and add an extension section plus supplementary demonstrator; avoid retitling the existing note as a general neural extraction system.

**Provisional abstract, with proposed work explicitly conditional:**

> We study exact Boolean abstractions of continuous scores under a declared predicate partition and input/parameter domain. Uniform sign certificates distinguish exact bits from unreachable cells, ties, mixed behavior, and unresolved analysis. For operator atlases with irreducible star boundaries, we relate degree-bounded sign observations to weighted binary codes and obtain a sharp degree threshold at information saturation. A small exact multi-affine backend produces replayable range certificates over joint rational boxes and exports typed Boolean operators. We investigate how representation, feature construction, certification, and certificate reuse affect total extraction and execution cost. General neural-network verification and preservation of soft probabilistic semantics remain outside the contract.

The last cost/reuse sentence is a **planned investigation**, not a completed result. Until an appropriate application and evaluation exist, the abstract describes a potential methods package, not a submission-ready paper.

Proposed outline:

1. Problem and source-aware scope: representative extraction versus uniform regions.
2. Exact/partial interface, witness/proof obligations, arithmetic and equality policy.
3. Operator dictionaries and observation languages; existing GU example as calibration.
4. Weighted-star theorem and a genuinely broader result if obtained.
5. Certificate producer/checker and supported model families.
6. Typed Boolean composition; continuous interface/range obligations.
7. One application, cost-matched baselines, and persistence reuse.
8. Negative cases, scalability limits, and relation to existing extraction/verifiers.

Required proof work: independent review of the weighted-star argument; careful treatment of determining real boundary patches; an unsaturated or non-star theorem if mathematical significance is claimed; formal producer/checker contract; symbolic transport soundness; arithmetic error handling for any actual floating-point deployment. Neural generality requires a supported verifier backend, not an assertion that arbitrary networks are polynomials.

Required empirical work: one independently motivated small module or benchmark; a frozen specification and denominator of all attempted cells; near-boundary, mixed, unreachable, and unsupported cases; both one-shot and repeated use; all cold certification/feature/serialization costs. It is acceptable for the strongest result to be a negative speed or coverage finding.

| Baseline | Match the task | What to measure |
|---|---|---|
| Direct model execution | Same threshold placement and input domain | Runtime after paying validation/certification separately; outputs and abstention policy. |
| Ordinary truth table / packed token | Same operator, frame and certificates | Extraction and representation costs; exact identity with CM endpoint. |
| ROBDD / Boolean decision graph | Same extracted function and reachability predicate | Construction, size, variable-order sensitivity, execution and composition. |
| Natural interval arithmetic | Same model expression and rational domain | Certified coverage, unresolved outcomes, cost. Two cases completed here. |
| Multi-affine exact corners | Same restricted family | Active dimension, vertex count, coefficient bit lengths, producer/replay costs. |
| SMT/CAD or ReLU verifier | Appropriate arithmetic/model class | SAT witness validation, UNSAT trust/proof cost, timeout/UNKNOWN rate. No forced direct ReLU encoding of multiplication. |
| DeepPoly or comparable abstract interpreter | Only supported network operations | Sound certified coverage, precision versus solver cost; disclose numerical semantics. |
| Shared certificates / IVAN / OLIVE | Repeated input regions or changed models, respectively | Cache/template construction, containment/reverification, invalidation, saved full work. |

Use a total cost model such as `T_setup + T_feature + T_certify + T_replay + T_export + Σ T_execute + T_recertify`. If `T_model>T_operator`, break-even repeated use requires enough executions to repay setup and subsequent invalidations. If feature computation already evaluates the original score, symbolic dispatch may never pay. Count sign-information observations separately from rational bit operations, precision, memory, and shared computations. No headline ratio comparing a compact token with a full dense output is valid.

Stopping criteria:

- Merge into GU if the strongest theorem remains the weighted/saturated star plus classical range facts.
- Defer a standalone methods paper if useful regions almost never certify, or certificate cost dominates without a credible repeated-use workload.
- Drop CM-specific speed/novelty framing if matched tables/BDDs retain the same guarantees and costs.
- Defer evolutionary claims if only endpoint records or generic margin bounds are available.
- Pursue a separate paper only after a broader theorem or distinct implementation capability survives comparison with the closest work and has a useful, reproducible example.

## 11. Established, open, and next work

**Established in this investigation:** navigation-selected versions/hashes; the precise overlap map; current publication/version corrections; explicit extraction and composition contracts; the written conditional weighted/saturated-star derivation; a restricted exact producer/replay demonstrator; 3,587 bounded assertions; concrete failures of broader sample, dictionary, cascade, and persistence claims.

**Source results, not newly proved here:** the whole GU degree/cardinality lower bound; general neural rule-verification complexity; published abstract interpretation, shared-template, incremental verification, policy safety, and DSGRN results. Source manuscripts have not been independently proof-audited in full.

**Unproved/unimplemented:** unrestricted unsaturated or non-star optimal guards; general learned-network extraction; large-dimensional scalable exact ranges; floating-point soundness for this backend; portable solver proof integration; useful training-trajectory reuse; any PALO integration, performance advantage, or historical novelty.

Prioritized follow-up, contingent on Brian choosing to continue beyond this initial investigation:

1. **Proof/priority gate:** independently audit the weighted-star statement and make a theorem-by-theorem comparison with Averkov–Bey; attempt the unsaturated/non-star case. A failed novelty gate leads directly to a GU extension. Reuses this dossier and belongs in this chat. Suggested model: **gpt-6-astra, high**, because proof assumptions and prior-art overlap are the main error risks; no claimed price comparison.
2. **Application gate:** select one actual small learned/PALO-style module and define its predicates, region, equality policy, and arithmetic. Existing local diagnostics/edits remain scoped and reversible; paid training or external writes require explicit approval. Keep in this chat while using the same contract. Suggested model for bounded implementation: **gpt-6-luna, high**, with the proof contract fixed and review of verification results.
3. **Only after those gates:** implement the appropriate verifier/range backend and measure meaningful baselines. This becomes a self-contained implementation study and may merit a fresh chat once its inputs and authorization can be compactly handed over; no fresh chat is necessary now and none was created here. Model choice should be revisited against the backend's actual complexity rather than presumed savings.

The initial research task is complete. **No source-manuscript edit, external publication, commit, push, paid run, or additional chat/model run is required to deliver this assessment.** The useful optional next step is the proof/priority gate; a large integration should be deferred until that gate provides a reason to proceed.
