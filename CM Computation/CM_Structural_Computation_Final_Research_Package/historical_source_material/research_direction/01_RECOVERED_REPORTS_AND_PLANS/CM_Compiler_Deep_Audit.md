---
title: 'Typed CM compilation: deep pre-submission audit'
subtitle: 'Mathematics, implementation contracts, evidence, and the next experimental freeze'
author: 'Technical audit prepared for Brian Theory'
date: '22 September 2026'
fontsize: 10pt
geometry: margin=0.78in
colorlinks: true
linkcolor: black
urlcolor: blue
toc: true
toc-depth: 1
header-includes:
  - \usepackage{amsmath,amssymb,mathtools,microtype,booktabs,longtable}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[L]{\small Typed CM compiler audit}
  - \fancyhead[R]{\small 22 September 2026}
  - \fancyfoot[C]{\thepage}
  - \setlength{\headheight}{14pt}
  - \setlength{\emergencystretch}{3em}
---

# 1. Executive verdict

**The revised mathematical kernel is sound, but the manuscript is not yet ready for an experimental freeze or a performance-centered submission.** The remaining problems are primarily specifications, implementation scope, and measurement design, not a need for more CM/LM foundations theory.

The paper is substantially improved by the publication split. Its early frame-mismatch example, explicit $S,T,H$ provenance, separate tabulation rule, and scoped completeness statement make a coherent local compiler story. Equations (17) and (18), the worked implication example, the signed transformations, and the structural/hybrid soundness arguments survive independent checking [M, Sections 2–4].

However, inspection of the public implementation reveals distinctions that the paper presently blurs:

**Root compilation versus persistent local rewriting.** The token API attempts to compile the requested root. If that fails, the dense wrapper passes the unchanged original root to the ordinary compiler. Successful speculative child pairs are not inserted into a mixed pair/general IR by the inspected path. Calling this a general local-folding pass without this qualification overstates what has been implemented [C1].

**Syntactic variables versus semantic support.** The implementation collects variable occurrences and removes fixed names; it does not compute essential Boolean dependence. The tabulation rule must define this exact syntactic admission predicate [C1].

**Actual output axes versus unfixed variables.** The dense wrapper and lifting routine retain all requested row/column axes, including fixed axes, and broadcast over them. Consequently, its output size is not always $2^{n_{\mathrm{live}}}$ [C1, C3]. This affects semantic output matching, memory, and budget comparisons.

**Rules versus strategy.** The inference rules establish valid denotations, but do not themselves encode the implementation's structural-first priority or strategy-specific refusal. A primitive can have both structural and tabulated derivations in the displayed relation, although the hybrid algorithm returns the structural one. This is not Boolean unsoundness; it is an operational/provenance specification gap [M, C1].

**Full protocol versus its summary.** The repository contains the actual protocol-v3 plan. It is explicitly pre-freeze and unexecuted, and is much more detailed than the revised paper's summary. It still needs corrections concerning arm/outcome terminology, cold-state measurement, statistical aggregation, multiplicity, and the missing explicit matched generic-folding arm [P].

The strongest current classification is **a compiler-mechanism technical paper with a disciplined negative-results and methodology component**, not an established new Boolean algebra or a demonstrated fast general compiler. A useful final result may be positive, mixed, or negative. A pass on a synthetic two-variable cell would establish a region of utility, not broad circuit prevalence.

## Audit scope and confidence

I inspected the 14-page revised PDF and its LaTeX, compared the 31-page foundations companion and the older 24-page compiler manuscript, read the supplied review history, and inspected all rendered pages of the primary manuscript. I read relevant public code and project records through GitHub at commit:

`0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b`.

The live results site could not be fetched reliably in this environment; its committed source and published evidence files were inspected instead. This is a single AI-assisted audit using several disciplinary lenses, not external human peer review.

The audit-specific reference checker executed **1,083,999 assertions**, including **1,048,576 scalar fusion comparisons** covering 262,144 token/frame/outer-operation configurations. All passed. It also checked 8,080 generated structural expressions and 1,000 independently generated expressions under two fixed maps. These are independent mathematical/reference-model checks, **not a rerun of the project's 116-test suite**. I did not execute the project's compiler, its benchmarks, the S1/S2 recount, the P14 bootstrap, or protocol v3. The repository could be read through the connector but not cloned into the execution environment. Statements about current code behavior below are source-derived; the small edge cases were also exercised in the independent reference model [V].

# 2. Recommended paper identity and thesis

Recommended working title:

> **Typed Frame-Aware Boolean Folding: Pair Compilation, Provenance, and Empirical Boundaries**

Keeping the current title is reasonable, but its subtitle or abstract should make the pair-root implementation boundary explicit.

Recommended thesis:

> A compact Boolean truth token can be coupled to an ordered operand frame, normalized under signed input changes, and composed by sound local rules. An implementation must distinguish structural construction, exact tabulation, and fallback, and must account for failed work and the delivered output. The present implementation is a partial pair-root compiler; its end-to-end advantage over strong packed and sharing-aware alternatives remains an empirical question.

There are two coherent next versions. **Version A** retains the implementation and scopes the paper to pair-root compilation. This is the least disruptive and best supported now. **Version B** actually integrates pair nodes into general IR so that successful local folds survive a non-pairable parent. That may be more useful on larger natural circuits, but it is a new implementation and requires a new specification, regression suite, and experimental freeze. Do not silently describe Version B while measuring Version A.

The mechanism need not be uniquely CM-specific. A generic optimizer reproducing a reduction does not make the reduction worthless. It does mean that representational advantages must be established by costs, compositional interfaces, or useful engineering properties rather than by exclusive mathematical capability.

# 3. Mathematical correctness audit

| Location in [M] | Verdict | Required action |
|:---|:---|:---|
| Equations (3)–(7), true-first states and selection | Correct | Preserve $\mathbb B\cong\mathbb F_2$, $\Updownarrow$, and declared assignment order. |
| Equations (8)–(11), swap/transpose/polarity | Correct transformations | Give a combined normalization formula; cite the full transform range, not only Eq. (11). |
| Equation (12), pointwise outer operation | Correct | Keep distinct from matrix multiplication. |
| Theorem 1 / Eq. (13) | Correct for every binary Boolean outer operation | State common frame and fixed environment. No distributivity assumption is required. |
| Equations (15)–(16), judgment and invariant | Correct after typing refinement | Define syntactic live variables, valid inputs, and strategy semantics. |
| Equation (17), negation | Correct | $\nu(S)=S$, $\nu(T)=\nu(H)=H$. |
| Equation (18), fusion | Correct | Its provenance update is not a lattice join. |
| Equation (19), exact tabulation | Correct | Admission predicate must match syntactic variable collection. |
| Equations (20)–(21), worked example | Correct | Both normalized words and final XNOR word verified. |
| Theorem 2, structural soundness | Correct on admitted derivations | Add finite/well-formed input assumptions. |
| Definition 1 / Theorem 3, fragment completeness | Correct, deliberately syntactic | Retain a short contract; move the inductive proof to an appendix. |
| Lemma 1 / Theorem 4, tabulation/hybrid | Correct | Separate selected-strategy failure from existence of a derivation under another strategy. |
| Equation (22), dense reindexing | Correct with position indices | Say $a,b$ are array positions, unlike assignment-labelled CM subscripts. |
| Section 5.3, output ownership | Supported by inspected lifting code | Actual returned axes need correction. |
| Section 5.4, asymptotic costs | Useful but incompletely qualified | Separate traversal, diagnostics, name/layout operations, and output writing. |

## Explicit normalization lemma

Let $a,b\in\mathbb B$ indicate negation of the **first and second source operands**, and let $s$ indicate whether source operand order is reversed relative to $(R,C)$. With $P=[\Updownarrow]$,

$$
\operatorname{Norm}_{s,a,b}(M)=
\begin{cases}
P^aMP^b,&s=0,\\
(P^aMP^b)^T=P^bM^TP^a,&s=1.
\end{cases}
$$

This is a deterministic transport into a *declared* target frame, not NPN canonicalization over an equivalence class. The represented truth function is preserved under the corresponding operand interpretation. The coordinate oracle checked all 16 tokens, eight transports, and four assignments. Symmetric functions may admit several equivalent descriptions, but their resulting token in a fixed frame is unique.

## The two examples

For the motivating expression,

$$
[\Rightarrow]=1011_2,\qquad [\Rightarrow]^T=1101_2,
\qquad 1011_2\Updownarrow1101_2=0110_2.
$$

Thus $(R\Rightarrow C)\Updownarrow(C\Rightarrow R)=R\Updownarrow C$. Omitting the transpose produces $0000_2$, contradicted by $(R,C)=(1,0)$.

For the revised worked derivation,

$$
R\Rightarrow\neg C\mapsto0111_2,\quad
\neg C\Rightarrow R\mapsto1110_2,\quad
0111_2\Updownarrow1110_2=1001_2=[\Leftrightarrow].
$$

Negating the result gives $0110_2=[\Updownarrow]$. These are correct in the declared true-first order.

## Output complexity needs a lower-bound formulation

An explicitly materialized truth relation with $n_{\mathrm{out}}$ binary axes contains $2^{n_{\mathrm{out}}}$ Boolean entries. In the current byte-per-Boolean array interface, allocation and writing entail $\Omega(2^{n_{\mathrm{out}}})$ output space and time. A simple fill/copy can achieve $\Theta(2^{n_{\mathrm{out}}})$ **materialization overhead**; arbitrary total evaluation is not bounded above by that expression alone. In a packed word model, distinguish $2^{n_{\mathrm{out}}}$ output bits from $\lceil2^{n_{\mathrm{out}}}/w\rceil$ output words.

Replace “costs $\Theta(2^n)$ ... for every explicit method” with this precise distinction. Also use the actual output-axis count, not automatically the number of unfixed variables.

## Coefficient linearity is not input linearity

The one-hot contraction is linear in the matrix coefficients for fixed operands. The state encoding $x\mapsto(x,\neg x)^T$ is affine, not linear. No retained compiler theorem requires the represented Boolean function to be affine. One clarifying sentence is enough; do not restore the companion paper's full coefficient-algebra exposition.

# 4. Rules-section audit

## Define the actual admission predicate

Use

$$
\operatorname{FV}_F(e)=\operatorname{FV}(e)\setminus\operatorname{dom}(F),
$$

where $\operatorname{FV}(e)$ means variables occurring syntactically. No Boolean simplification or essential-support calculation is implicit. Tabulation is admitted when $\operatorname{FV}_F(e)=\{R,C\}$, with $R\ne C$ and neither fixed. The full implementation additionally requires one variable from each disjoint row/column layout [C1].

Two examples show why the distinction is substantive:

$$
e_1=(R\Updownarrow R)\Updownarrow C\equiv C.
$$

Here the implementation's live set is $\{R,C\}$ although essential support is only $\{C\}$. Hybrid compilation can tabulate it as $1010_2$, provenance $T$.

$$
e_2=(R\land C)\Updownarrow(Z\Updownarrow Z)\equiv R\land C.
$$

With $Z$ unfixed, syntactic live variables are $\{R,C,Z\}$, so the pair path refuses even though the function depends on only $R,C$. Fixing $Z$ permits exact tabulation. Neither behavior is unsound; both must be described accurately [C1, V].

## Equation (17)

The rule is correct. A returned structural token remains structural under complement. A structural negation applied to a tabulated child makes the result hybrid. Importantly, provenance describes the **retained derivation**, not a proof that no unsuccessful work occurred earlier in an execution.

## Equation (18): $T$ fused with $T$ must be $H$

The complete update table is:

| $\mu(p,q)$ | $S$ | $T$ | $H$ |
|:---|:---:|:---:|:---:|
| $S$ | $S$ | $H$ | $H$ |
| $T$ | $H$ | $H$ | $H$ |
| $H$ | $H$ | $H$ | $H$ |

Two locally tabulated children followed by a structural fusion have tabulated ancestry and a structural step. Therefore $\mu(T,T)=H$ is correct. Calling this a lattice join is inappropriate: idempotence would require $T\sqcup T=T$. Prefer $\mu$ or call the symbol a provenance-combination operation without order-theoretic claims.

A compact implementation model is $(\sigma,k)$, where $\sigma$ records a structural step in the retained derivation and $k$ counts tabulated leaves. Primitive gives $(1,0)$; Tab gives $(0,1)$; Neg gives $(1,k)$; Fuse gives $(1,k_1+k_2)$. Map these to $S,T,H$ as above. The inspected private pair structure implements this idea [C1]. A larger provenance lattice would add machinery without solving a problem.

## Soundness relation is not a deterministic strategy

A signed primitive also has exactly two syntactic live variables, so the displayed unrestricted rules permit both an $S$ derivation and a $T$ derivation with the same token. Token uniqueness still holds; provenance uniqueness does not follow from those rules.

Use one of two clean solutions. The simpler is to label the rules **admissible semantic constructions**, then define a deterministic algorithm separately. Its modes are structural-only, structural-first with local tabulation, and whole-root tabulation. Alternatively, index judgments by mode and include a failed-structural-attempt premise on the hybrid Tab rule. Either solution must say that fallback follows failure of the **selected algorithm**, not absence of every derivation under all modes.

## An operational companion to the semantic rules

The following fixed-frame core makes priority explicit. `Norm` succeeds only for a supported connective over signed literals whose two distinct underlying variables are exactly the declared pair. Both recursive children are attempted, matching the inspected implementation rather than a short-circuit variant. The public layout-based interface selects the returned pair from its disjoint row and column lists.

```text
Pair(e, Gamma=(R,C,F), allowTab):
    if guarded Norm_Gamma(e) succeeds with t:
        return Pair(R,C,t,S)
    if e = NOT a:
        x = Pair(a,Gamma,allowTab)
        if x is a pair:
            return Pair(R,C,complement(x.token),nu(x.provenance))
    else if e = a Phi b, with Phi supported:
        x = Pair(a,Gamma,allowTab)
        y = Pair(b,Gamma,allowTab)
        if x and y are pairs in the same frame:
            return Pair(R,C,fuse_Phi(x.token,y.token),mu(x.p,y.p))
    if allowTab and FV(e) minus dom(F) = {R,C}:
        return Pair(R,C,tabulate_four(e,Gamma),T)
    return NoPair

TokenRoot(e,Gamma,mode):
    pure_structural: return Pair(e,Gamma,false)
    hybrid:          return Pair(e,Gamma,true)
    retabulate:      if FV(e) minus dom(F) = {R,C}:
                         return Pair(R,C,tabulate_four(e,Gamma),T)
                     else: return NoPair
```

This is a specification, not a replacement claim about unexecuted code. Layout validation and invalid-mode errors occur before this core. `NoPair` carries no truth value: the caller decides whether to invoke an ordinary evaluator, and charges that work to the requested endpoint. With valid acyclic input, the pure-fragment induction proves that the first two modes return the unique token whenever the pure fragment applies.

## Missing base cases and completeness

There is no soundness obligation to add a literal or constant-token base case to the intentionally restricted fragment. A literal root and a fixed-only expression may legitimately return NoPair. However, say so. Constant-valued functions are still obtainable structurally: $(R\land C)\Updownarrow(R\land C)$ returns $0000_2$ with provenance $S$. Thus “no constant syntax rule” is not “no constant token.”

The completeness theorem is correct but mostly a construction invariant: the accepted syntax is generated from exactly the cases handled by the algorithm. It is useful as a specification and test oracle, not a major mathematical novelty claim. Keep its statement short, move its proof, and explicitly avoid completeness for semantic two-variable functions. The current cautionary remark is good.

## Failed work is not provenance

For $(R\land C)\land R$, the hybrid algorithm builds the left structural pair, fails on the right literal, then tabulates the root. The returned result has provenance $T$, while attempt counters include a successful primitive token. This is consistent, not a hidden hybrid bug. Report retained construction provenance and total attempted operations separately. Global attempt counters are appropriate for costs but not a reconstruction of the returned proof [C1, V].

# 5. Implementation/specification consistency audit

## The inspected implementation's actual scope

`compile_expr_to_cm_pair_token` validates layouts, computes expression statistics, tries the requested strategy, and returns either a frozen token object plus diagnostics or `None` plus diagnostics. `ordinary_fallback` is a **signal**, not an executed fallback in this API. `compile_expr_to_cm_pair` is the dense wrapper: it either lifts a successful token or calls the ordinary compiler on the original root [C1].

For example, with row layout $[R,Z]$, column layout $[C]$, and $e=(R\land C)\lor Z$, the inner pair may be recognized, but the root does not reduce to a pair. The wrapper then recompiles $e$ unchanged. The inspected path does not preserve the inner token as an optimized node in general IR. This does not contradict soundness; it limits the implementation claim and the workloads on which the mechanism can save work.

## Contract findings

| Item | Source-derived finding | Severity/action |
|:---|:---|:---|
| Provenance names | $S,T,H$ correspond to `pure_structural`, `full_retabulation`, `hybrid_pair` | Correct mapping; print it explicitly. |
| Legacy strategy | `structural` aliases `hybrid`, flagged in diagnostics | Keep forbidden in confirmatory arms. |
| Requested hybrid strategy | May return $S$, $T$, $H$, or NoPair | Protocol must not require every hybrid-strategy call to end $H$. |
| Live variables | Syntactic collection minus fixed names | Define it; do not imply semantic support discovery. |
| Pair metadata | Canonical row/column names and normalized token; provenance separate publicly | Correct; clarify that signs/order are normalized, not stored independently in every result. |
| Layout scope | Public API takes row/column lists, formal core fixes one pair | Add the selection bridge from disjoint layouts to a returned $(R,C)$. |
| Invalid layouts | Duplicate axes or overlap raise `ValueError` | Distinguish invalid input from legitimate NoPair. |
| Root fallback | Original expression is passed unchanged to ordinary compiler | Scope as partial root compilation or implement genuine mixed-IR retention. |
| Dense output | All ambient requested axes retained, including fixed axes | Repair output contract before comparisons. |
| Nonmutation/ownership | Frozen pair dataclasses; lift returns owned `.copy()` | Supported for inspected path; whole-program guarantee still needs tests. |
| Sharing | Statistics use identity DAG; recursive pair construction lacks node memoization | Account for $N$ and $U$ separately; do not imply $O(U)$ pair compilation. |
| Caches | Composition is cached; LUTs built at import; lift/permutation metadata cached | Freeze all cache states, not only packed-environment cache. |

## Fixed axes: a concrete output mismatch

Consider requested row layout $[R,Z]$, column layout $[C]$, $F(Z)=1$, and source $(R\land C)$. The token has four truth values. The current dense API returns shape $4\times2$, with the $Z$ axis reinserted and repeated, hence **eight entries**, not four. Its budget estimate also uses $|R|+|C|$ [C1, C3].

There are two valid contracts: retain ambient axes, or remove fixed axes and return a restricted relation. The implementation presently follows the first. Both arms must implement the same choice. Merely changing the paper's $n$ without ensuring the comparator's output shape matches is insufficient.

## Cost qualifications

The $O(H)$ quantity in [M] is stack space, not total public-call auxiliary space. `_expr_stats` allocates identity sets, postorder lists, and per-node dictionaries, giving an $O(U)$ diagnostic workspace contribution under unit-cost word assumptions. Unmemoized recursive compilation can revisit shared nodes according to unfolded occurrences $N$.

For the identity-shared family $e_0=R\land C$, $e_{k+1}=e_k\Updownarrow e_k$, the unfolded count is $N_k=4\cdot2^k-1$, whereas the unique object count is $U_k=k+3$. This does not refute an $O(N)$ statement; it shows why it must not be advertised as linear in the input DAG size.

The quadratic rescanning warning is directionally right but not a complete global upper bound for arbitrary layout widths and variable identifiers. A support scan also sorts distinct names and checks membership in row/column lists. A transparent accounting is

$$
T=T_{\mathrm{stats}}+T_{\mathrm{recognition}}+T_{\mathrm{fusion}}
 +\sum_{v\in\mathcal A}T_{\mathrm{scan}}(v)
 +4\sum_{v\in\mathcal T}T_{\mathrm{scalar}}(v)+T_{\mathrm{fallback/output}},
$$

where $\mathcal A$ includes every attempted scan and $\mathcal T$ every performed tabulation, including work later discarded. Bound layout size and name operations before simplifying this to an $O(N^2)$ expression. In main text, say the implementation **can incur quadratic subtree-rescanning work**, rather than claiming an unconditional complete $O(N^2)$ bound.

# 6. Theory balance: exact additions, removals, and placement

| Proposed item | Placement | Decision |
|:---|:---|:---|
| Combined normalization lemma | Main text | Add. It removes ambiguity about source signs after swapping. |
| Soundness invariant and three construction rules plus Tab | Main text | Retain; distinguish semantics from strategy. |
| Full provenance update table | Main text | Add; replace overloaded join terminology. |
| $(\sigma,k)$ implementation model | Appendix or short implementation paragraph | Useful mapping, not a new theory section. |
| Syntactic-fragment completeness | Brief main-text statement, appendix proof | Correct but too elementary to carry contribution weight. |
| Separate theorem restating fusion legality | Do not add | Current invariant and common-frame rule already provide it. |
| Recognition-versus-tabulation separation | Main-text examples | More useful than another theorem. |
| General abstract machine or dependent type system | Future work | Unnecessary for this implementation and evidence scope. |
| Partial evaluation/local-cut relationship | Related work, one paragraph | Add; avoid claiming it is an exclusive CM mechanism. |
| Break-even inequality | Main discussion | Add, especially the same-token no-crossover case. |
| LM normal form, valuation, tensors, spectra, quantum analogies | Companion only | Do not restore. |
| Repeated proof summaries and later-project ratios | Shorten/move | Free space for contracts, reproducibility, and direct results. |

The useful break-even equation is

$$
T_m(K)=C_m+Kq_m,
\qquad T_{\mathrm{CM}}(K)<T_B(K)
\iff C_{\mathrm{CM}}-C_B<K(q_B-q_{\mathrm{CM}}),
$$

after including the endpoint's conversion/materialization costs in the appropriate terms. When both methods return the same token and use the same query routine, $q_B=q_{\mathrm{CM}}$. Then repeated token queries **cannot create a crossover**: the absolute preparation-time difference remains unchanged, and the relative ratio tends toward one. A reuse advantage can arise against a method that still executes a program on each query, or under another genuinely different preparation/query contract. Do not charge a prepared packed token for unnecessary reevaluation.

# 7. Prior art and novelty audit

## What the primary sources establish

Cheng, Zhao, and Xu explicitly combine same-variable Boolean truth vectors entrywise under an arbitrary outer logical operation. Proposition 3.3 is the direct antecedent; the inspected eight-page author preprint labels this identity Eq. (21), so do not carry an equation number from another version without checking it. Their XOR–AND matrix arithmetic and logical structure matrices also establish the numeric comparison boundary [L1].

Bricken's nine-page note, internally dated March 1997, contains the sixteen compact logical matrices, bra–matrix–ket use, and operand exchange by transpose. It is sufficient to rule out novelty for those features. Its historical public-release date and peer-review status were not established by this audit [L2].

The most important operational antecedents are cut-based synthesis and small truth-function libraries. Mishchenko, Chatterjee, and Brayton use small-cut truth tables, NPN classes, structural hashing, and DAG-aware replacement [L3]. Current mockturtle resynthesis interfaces explicitly pass a truth table **together with its leaf signals** [L4]. Thus ordered input metadata is not absent from conventional tools. A comparison table claiming that generic LUT/cut systems have “no frame metadata” would be misleading.

The official kitty library documents small truth-table operations and canonicalization facilities [L5]. Bryant supplies canonical ordered decision diagrams and Boolean operation algorithms [L6]. LLVM documents established redundancy elimination and simplification passes; Jones, Gomard, and Sestoft describe partial evaluation as specializing a program against static data [L7, L8]. These are antecedents for the surrounding optimization concepts, not proof that any particular implementation has identical cost.

Edwards establishes an earlier Boolean-matrix logic program. Stern's publisher record establishes a substantial earlier matrix-logic treatment. Mizraji's 1992 and 2008 abstracts describe vector truth states and matrix gates, including rectangular dyadic operators on tensor-product inputs. These sources justify historical attribution, but abstract/preview access does **not** justify asserting that their complete works lack the exact compiler integration [L9–L12].

Equality saturation and Souper explore broader equivalent-expression or synthesis spaces. They are adjacent rather than obligatory heavyweight primary baselines for a fixed two-input token constructor. Compare equivalent delivered artifacts and charge search/extraction if such experiments are added [L13, L14]. Simulation-guided synthesis is relevant to bit-parallel operational practice but sampled simulation is not an exact four-assignment proof for larger supports [L15].

## Novelty ledger

| Claim | Classification | Defensible wording |
|:---|:---|:---|
| A binary connective has a compact four-bit matrix | Clearly antecedented | Representation convention, not discovery. |
| Transpose and input/output polarity transforms | Clearly antecedented | Standard coordinate transport used by this compiler. |
| Same-frame pointwise composition | Clearly antecedented | Imported kernel identity. |
| Truth table plus ordered operand identities | Standard ingredient | Explicitly typed here; not absent from LUT/cut practice. |
| Structural/tabulated/hybrid provenance with specified fallback | Plausibly distinctive integration | A concrete auditable specification; historical uniqueness unproved. |
| Fragment soundness and completeness | Standard compiler-proof technique | Necessary correctness contract, not deep new mathematics. |
| CM-exclusive symbolic reduction | Unsupported | Matched generic reduction already contradicts exclusivity. |
| Lower metadata or normalization cost | Empirically unresolved | Requires a matched implementation comparison. |
| End-to-end pair compiler advantage | Empirically unresolved | Requires direct protocol execution. |
| A stronger algorithm than existing cut optimizers | Not established | Do not claim from notation or search non-discovery. |

**Bottom line:** the integration can be useful without being a new algorithmic family. This audit does not establish a theorem or capability genuinely stronger than existing small-function optimization. That is not a reason to discard the work; it is a reason to make utility and reproducibility, rather than priority, the publication argument.

Bibliographic correction: [M]'s Lee2022 entry names “Winston Lee.” The inspected primary publication record uses **Siang-Yun Lee**; use the published author name [L15]. Keep preprint, online-first, issue, and website-review dates distinct.

# 8. Evidence ledger

The following ledger separates evidence records from independent reproduction. Arithmetic consistency checks are not replay of raw experiments.

| Empirical statement | Concrete source | Audit status and permitted use |
|:---|:---|:---|
| 116 focused tests on 19 September; listed feature coverage | [M] 8.1, [O] 4.4, R2 response | Reported historical test run; not rerun here or bound here to the inspected current commit. |
| 1,048,576 project alignment/fusion cases | [M] 8.1 | Historical report. This audit separately ran a clearly counted exhaustive checker [V]. |
| S1/S2: 10,500 generated, 10,389 all-arm; 3,750 S1 + 6,639 S2 | [M] 8.2, [O] 8.1 | Counts internally consistent; raw records not recounted here. |
| Remaining 111: 108 all-fail, two generic/CM only, one sharing-only | Same | Retain all patterns and distinguish resource failure from semantic disagreement. |
| Seven metrics agree in all admitted all-arm cases; generic has more folds in 6,010, CM in zero | Same | Reported mechanism evidence, not a timing or general equivalence theorem. |
| S2 median multiplication counts 35/35, 17/12, 9/0 at the three sharing fractions | Same | Work counts, not speed ratios; division by zero is not an infinite-speed claim. |
| P14: 384 synthetic + 107 natural; 51,102 timing rows; equality on 491 + 512 targeted cases | [M] 8.3, [O] 8.2 | Historical report; raw rows and bootstrap not rerun here. Public P-series guide corroborates disposition and headline ratios [R3]. |
| P14 selects five synthetic cases, zero natural; selected E/D ratios 0.075–0.389 | Same | Retain as narrow exposures, not natural pair-compiler prevalence. |
| P14 E/D 1.0508 synthetic, 1.0607 natural; no-go under frozen rule | Same and [R3] | Negative decision supported by reported estimates and rule; inferential wording requires qualification below. |
| August kernel CM/CSE-flat 0.891 overall, 0.961 at $k=16$; wrapper 2.797 and 1.343 | [R1] paired formula-cluster table and wrapper paragraph | Source record inspected. Correct boundary attribution; raw numerical analysis not rerun. |
| September complete-relation BitSet wins all 78 runnable clusters; packed-CM speed ratio 0.930 versus BitSet | [R2] | Source record inspected. Different evaluator/task, not pair protocol. |
| Query ladder q64 CSE-flat/R2 speedups 1.100 and 1.090 on two hosts | [R2] | Source record inspected. q16 straddles parity across hosts; not portable universal crossover. |
| P15: 490 fresh semantic cases, zero accepted timing worker artifacts | [R4] final JSON | Actual disposition inspected; semantics-only successor, no pair timing result. |
| Protocol-v3 end-to-end result | [P] explicitly pre-freeze; [M] unexecuted | No matching completed run located in inspected materials. Must remain unexecuted in the paper's evidence record. |

## P14: preserve no-go, but distinguish statistical statements

The reported synthetic E/D interval is $[0.9683,1.1075]$, which includes parity. The natural interval is $[1.0176,1.0927]$, which does not. Therefore “the point estimate is slower on both corpora and the promotion rule fails” is supported. “A statistically established slowdown on both corpora” is not supported by those displayed intervals.

The revised table says “98.75% simultaneous interval.” The older text describes 98.75% bounds for four primary comparisons. Four Bonferroni-adjusted marginal intervals at that level target **95% familywise coverage**, assuming the component intervals have their nominal coverage; they do not automatically give 98.75% familywise coverage. The raw analysis must settle the intended convention. Do not change the historical bounds or decision; correct the label after checking the analysis, or temporarily call them “reported multiplicity-adjusted bootstrap bounds.”

The post-split version also drops useful P14 qualifications retained in [O]: the smaller local sampling freeze, Windows/Python environment, uncontrolled affinity, disclosed amendments, and allocation-only `tracemalloc` memory pass. Restore a compact limitations paragraph or bind an accessible methods supplement. “Separately frozen” should not conceal amendments.

## The sixteen-function limitation

Every fixed two-input truth token has only sixteen possible values. That does **not** by itself prove that every entire S1/S2 workload had only two semantic variables; local cuts can be embedded in larger-support expressions. I did not inspect the raw S1/S2 generator closure here. Replace the blanket corpus sentence in [M] Section 10 with a claim about the two-variable benchmark strata unless the generator manifest establishes the broader statement.

# 9. Experimental-methodology audit

The actual plan [P] already includes direct identity-memoized packed evaluation, prepared programs, ABC on a frozen translatable subset, fixed substitutions, common token queries, sharing strata, height bounds, retained failures, and source/environment freezes. Those are strengths. They are **not missing from the project**, although many disappear from the 14-page summary.

**Recommendation: prepare a disclosed protocol-v4 specification before the next freeze**, because the following changes affect arms, endpoints, or inference. This is not authority to reinterpret or rerun a completed historical study.

## A. Make the estimand singular and executable

Retain the intended primary question: cold pair-token construction versus direct packed construction on independently generated signed/permuted structural expressions with measured $N=1023$, $U=N$, no fixed variables, and reuse one. Define the CM arm explicitly as `pure_structural` (or prospectively justify another requested strategy), not merely “cases whose result was pure.” Preserve non-pure outcomes as correctness failures, never a post-measurement filter.

The protocol specifies repetition counts but not a complete statistical aggregation recipe or a fixed count of distinct generated formulas in this cell. Freeze that count and its sampling law. A candidate design is 100 independently seeded formula cases and 30 process observations per case, with a pilot-based precision justification made before confirmation. This is a proposed design, not a power calculation or executed result.

For case $i$, define $r_i=\operatorname{median}_j(T_{B,i,j})/\operatorname{median}_j(T_{\mathrm{CM},i,j})$ and the primary estimate $\operatorname{median}_i r_i$. Specify paired case/process resampling, number of bootstrap draws, seed, interval construction, and treatment of censored observations. Preserve a common case schedule. Repetitions are not independent new formulas. If the intended statistic differs, encode that alternative explicitly before the freeze.

A $1.20\times$ competitor/CM ratio means **16.7% less CM elapsed time**, not 20% less. It can be described as a 20% increase in the speed ratio. A point estimate at least 1.20 with a lower confidence bound above 1 supports superiority with a practical point estimate, not a confidence guarantee of at least $1.20\times$. Retain or alter that rule prospectively and state which claim it permits.

## B. Keep requested strategy separate from observed outcome

The row labelled “Hybrid pair” in [P] says the root must be `hybrid_pair`. That is correct for the deliberately constructed mixed-child stratum, not every call with `strategy="hybrid"`. In other strata the same requested strategy can validly return $S$, $T$, or NoPair. Record both requested strategy and observed outcome for every observation.

Multiple-pair and compound-operand strata also need mechanically validated expectations. A recursively composed structural expression contains compound child formulas but can still be pure; only **opaque** compound operands are excluded. Invalid overlapping layouts should be an API validation stratum, not a timed successful-fallback stratum.

## C. Add the matched generic local-function arm explicitly

The protocol's arm table does not actually name a standalone generic local truth-function optimizer. Add a secondary arm receiving the same leaf identities, signed mapping, source sharing, fixed map, and output requirements. This is the comparison needed to test representational overhead rather than mathematical exclusivity. Direct packed evaluation remains the closest simple primary baseline.

Distinguish structural CSE from identity memoization. Structural CSE may merge equal separately allocated expressions; an identity cache does not. Either allow the same preprocessing and charge it, or expose separate arms. Do not force a stronger baseline to unfold a DAG because the current pair compiler does so.

## D. Make cold and prepared measurements genuinely different

[P] says cold calls start in fresh processes, but also prescribes an untimed warm-up and calibrated repeated inner loops. A warm-up can fill the composition cache and environment cache, and an inner loop can amortize the very setup claimed to be cold.

Declare an imported-runtime cold-call lane: import outside the call timer, perform required correctness/warm-up, reset **all** declared caches, then time one production call in the prescribed state. If batching is required, every iteration must recreate the same cold state with reset accounting specified. Report module/LUT initialization separately or include it symmetrically in an additional process-start lane. Prepared lanes pay construction once, then reuse honestly. Do not retrofit cache state after measurements.

## E. Align artifacts and fallback costs

Freeze token order, actual output axis list, packed bit order, fixed-axis policy, ownership, and digest for every arm. A NoPair response is not an equivalent result to a completed truth table. For a full-workload endpoint, charge attempted pair work **plus** ordinary fallback and required conversion. For token-only admission tests, retain refusals explicitly and do not hide them in a faster-completion-only aggregate.

A natural-corpus prevalence study must distinguish root success, potential local opportunities, and local transformations actually retained by an implemented IR pass. The current wrapper supplies only the first of those outcomes. Converting naturally multi-input circuits into artificial two-leaf cuts changes the research question; document cut extraction and keep original-root results separate.

## F. Measure costs without perturbing primary timings

Record recognition, statistics, support scans, normalization, fusion, tabulation, discarded work, fallback, and output conversion. Fine-grained timers around tiny token operations can dominate the kernel. Use the minimally instrumented production path for primary timing and a separate diagnostic pass for phase attribution; quantify instrumentation overhead. Counters do not substitute for elapsed time.

Report absolute process RSS, retained representation bytes, and output bytes separately. A 10% full-process RSS threshold can be insensitive to a small token allocation under a large interpreter baseline. A noisy or zero incremental RSS result is not proof of equal compiler memory. State the measurement resolution and warm/import baseline, without silently substituting `tracemalloc` for RSS.

## G. Specify multiplicity correctly

[P] says to correct “intervals or tests” with Benjamini–Hochberg. Standard BH is a false-discovery-rate procedure for a family of p-values, not an automatic simultaneous-confidence-interval transformation. Define hypotheses, valid p-values, endpoint families, and dependence assumptions; label ordinary confidence intervals descriptive. Alternatively choose a familywise procedure and compatible intervals prospectively. Neither choice permits a favorable secondary cell to replace primary failure [L16].

## H. Freeze operational policy, not just a list of fields

The plan asks for environment capture but leaves some decisions underspecified: GC enabled/disabled policy, CPU affinity policy, thread counts, hash seed, process-start method, frequency/power controls, crash handling, and whether the 60-second timeout applies to a call, calibration, or the whole arm/case session. Fill these before execution. Retain source hashes for all transitive project modules and external tool versions. Preserve ABC import/optimization/export costs and a verified translatable subset; its unavailable environment cannot be replaced by an unlabelled internal AIG approximation.

# 10. Later-results import decision table

| Evidence family | Endpoint/status | Decision for this paper |
|:---|:---|:---|
| S1/S2 | Exploratory symbolic/ANF work reduction | Keep as mechanism evidence, with generic tie and attrition. |
| P14-PY0 | Frozen recipe-to-owned-ANF dispatcher; no-go | Keep one negative-boundary table and methods supplement. Not pair-token performance. |
| P1–P13 development sequence | Several different construction/lowering/dispatch costs | Supplement or separate optimization-history paper. Do not rank ratios as one experiment. |
| P15 final disposition | Fresh-corpus semantic pass; timing inconclusive; zero accepted timing artifacts | One optional successor-status sentence or supplement. It does not supersede P14 timing or execute protocol v3. |
| August corrected CM/CSE-flat | Post-compilation kernel plus separate wrapper | Brief context only; useful warning about setup overhead. |
| September complete relations | Packed CM versus current BitSet/dense controls | Context for baseline choice, not direct pair evidence. |
| q1/q4/q16/q64 restriction ladder | Prepared repeated explicit residual output | Supplement/context for task matching; not same-token-query reuse. |
| Native multi-root/C38 | Native execution and related-root reuse | Separate systems paper or supplement. Different implementation/task. |
| Counting, SAT, projected count, decomposition, persistence | Smaller-query or storage contracts | Exclude from compiler results. |
| Any future exact protocol-v4 pair run | Matching source/arms/output/freeze | Direct evidence, contingent on actually completed and archived run. |

P15's final JSON reports 384 synthetic plus 106 natural semantic cases, 2,450 memory observations, and **zero** accepted worker timing artifacts. The calibration-cap termination makes timing inconclusive, not a measured win or a measured slowdown. Any follow-up requires a new prospective design, not extension of that observed cap [R4].

# 11. Structure, editorial, and figure audit

The motivating frame mismatch already arrives early enough. Preserve it. The Rules section is markedly more readable than the prior version; the principal task is precision, not another full pedagogical rewrite.

**Figure 1, page 3:** the box combining local tabulation and ordinary-IR fallback has an arrow into “Return pair token with provenance.” This is a real type-level graphical error: ordinary fallback does not produce a pair token. Split it into “eligible local tabulation → Pair” and “NoPair → caller's ordinary path.” Also show fallback when a recursive child fails, not only after the initial normalization box.

**Rules, pages 4–6:** add the three-by-three provenance table and a four-row assignment table beside the worked derivation. A new elaborate diagram is unnecessary. Give the combined normalization formula before the Primitive rule. Separate strategy ordering from logical rule validity. Keep notation fixed rather than replacing $[\Theta]$ throughout.

**Table 2, page 10:** it floats before its P14 subsection and immediately above the protocol-v3 primary-cell paragraph. This juxtaposes different endpoints unnecessarily. Place it after the first P14 description and put “ANF dispatcher, not pair-token protocol” in the caption. Correct the confidence-level label after checking analysis.

**Artifact table, page 7:** keep it; it is valuable. Use ragged-right narrative columns and state whether the public function returns a token, a dense array, or merely an intermediate IR. Large justified word gaps are visible even though the table is not clipped.

**Figure 2, page 9:** an “evidence hierarchy” is useful editorially, but independent tasks are not progressively stronger measurements of the same hypothesis. Rename it “Evidence map and transfer boundaries.” Do not imply that a later project result validates an earlier pair endpoint.

**Abstract/contributions:** remove the detailed later-project clause from the abstract. Keep the ordinary/packed comparison, reported generic tie, negative ANF boundary, and unexecuted status. Five contributions can become four by merging artifact/cost specification with the soundness/interface contribution. A protocol specification is not an executed empirical contribution.

**Redundancy:** Sections 7, 8.4–8.5, 9.5, 10, 11 and Appendix B repeatedly state that endpoints cannot be substituted. Say this prominently once, use a compact evidence table, and recover space for the missing reproducibility statement. Do not lose the caution itself.

**Accidental losses from the split:** restore the concise availability subsection with exact test commands, the immutable full protocol reference, and P14 environment/amendment qualifications. These are compiler material, not foundations duplication [O, Sections 4.5 and 8.2].

Recommended final structure: motivation and claim boundary; numeric/frame contract; ordered compiler and provenance; implementation/output/cost contract; closest prior art; frozen questions and methods; direct pair results; inherited mechanism/negative context; limitations and conclusion. Until direct results exist, label that section as a plan rather than an empty results promise.

# 12. Claim ledger

| Claim | Type | Present status |
|:---|:---|:---|
| Normalized token preserves the signed primitive's function | Mathematical correctness | Proved and independently checked. |
| Same-frame fusion and complement preserve denotation | Mathematical correctness | Proved and exhaustively checked on finite kernel. |
| Pure-fragment acceptance/completeness | Mathematical correctness | Correct within its generated syntax; finite reference checks also pass. |
| Tabulated and hybrid paths are exact | Mathematical correctness | Correct under syntactic admission and shared environment. |
| Ordinary fallback is correct | Interface assumption | Conditional on ordinary evaluator; not established by pair proof alone. |
| Current public code implements structural/hybrid/retabulate modes | Implementation | Supported by pinned source inspection; project suite not rerun. |
| Failed parent preserves local pair optimizations in ordinary IR | Implementation | Not supported by inspected wrapper; it recompiles original root. |
| Fixed axes are removed from dense output | Implementation | False for inspected ambient-axis interface. |
| Local folding can avoid symbolic expansion work | Mechanism evidence | Reported S1/S2 evidence; not unique to CM. |
| CM and generic optimizer always agree operationally | General algorithm claim | Unsupported; observed metric ties do not prove equal algorithms or costs. |
| P14 passes promotion gate | End-to-end empirical | False; retained no-go. |
| P14 significantly slows both corpora | Inferential empirical | Too strong; synthetic displayed interval includes parity. |
| P15 establishes faster late scanning | End-to-end empirical | Unsupported; no accepted timing artifacts. |
| Pair compiler beats direct packed end to end | End-to-end empirical | Unresolved; required run unexecuted in evidence inspected. |
| Natural pure-pair prevalence is high | Prevalence | Unresolved for this implementation. |
| Repeating identical shared token queries creates a speed crossover | Cost claim | False under equal query cost; preparation difference stays fixed. |
| Typed CM integration is historically unique | Priority | Not established by this bounded literature audit. |

# 13. Prioritized revision list

## P0 — before benchmark freeze

**P0.1: Choose the actual implementation scope.** Keep and name pair-root compilation, or implement persistent local pair rewrites. Do not benchmark one and describe the other.

**P0.2: Repair the contracts.** Define syntactic live variables; distinguish invalid input, NoPair, and executed fallback; state ambient fixed-axis behavior; align strategy and provenance semantics in manuscript and protocol. Add regression cases from [V] to the project's own suite.

**P0.3: Freeze a genuinely executable measurement specification.** Pin requested primary strategy, number of formula cases, statistic/bootstrap, generic arm, artifact semantics, cache state, warm-up/loop policy, process environment, failures, memory, and multiplicity. Publish a numbered successor when required by [P].

**P0.4: Re-run the real project tests.** Use the benchmark source closure and external tool environment, not merely this independent reference checker. Verify actual array shapes and fallback delivery.

## P1 — before submission

**P1.1:** Execute the pair-compiler campaign, retaining primary failure and all secondary outcomes. Do not make a positive-region prerequisite for honesty: a valid negative result remains a scientific result.

**P1.2:** Archive source closure, corpus, licenses, protocol, amendments, environment, commands, stdout, raw observations, failures, and analysis. Bind historical S1/S2 and P14 records explicitly rather than relying on review summaries.

**P1.3:** Refine novelty against ordered-leaf cut/LUT interfaces, and give a clear cost-based question rather than implying metadata is unique to CM.

**P1.4:** Correct P14 inferential language and interval labelling; restore omitted methods limitations. Update abstract/conclusion only to match completed evidence.

## P2 — editorial polish

Repair Figure 1 and Table 2 placement; add the small provenance/assignment tables; shorten repeated cautions and completeness proofs; correct published author metadata; keep all longer CM/LM theory in the companion. Provide accessible vector figures and suitable PDF metadata in the submission package.

# 14. Specific rewrite recommendations

## A. Replace the tabulation-admission paragraph

> Let $\operatorname{FV}_F(e)$ be the set of syntactically occurring variable names not bound by $F$. This set is an inexpensive conservative description of the variables that may affect evaluation; it is not the essential Boolean support. Local tabulation is admitted when this set consists of exactly one declared row variable $R$ and one declared column variable $C$. The compiler does not simplify cancellations to discover smaller semantic support.

## B. Add after the inference rules

> The displayed rules define sound constructions, not execution priority. The structural-only algorithm disables Tab. The hybrid algorithm first attempts Primitive, then recursive Neg or Fuse, and invokes Tab only after those attempts fail. The whole-root tabulation algorithm bypasses structural construction. NoPair means that the selected algorithm did not return a pair; another strategy may still admit the same expression. A fixed-frame token is unique by its four truth values, whereas provenance is attached to the chosen construction.

## C. Replace the general fallback description

> The token-only API returns either a framed token with diagnostics or NoPair. It does not itself execute the ordinary evaluator. The dense wrapper handles NoPair by compiling the original expression through the ordinary path and charging the failed pair attempt. In the current implementation, speculative successful child pairs are not retained in that fallback IR. Correctness of this branch assumes correctness of the ordinary evaluator on valid inputs.

## D. Replace the output-size statement

> Let $n_{\mathrm{out}}$ denote the number of axes in the actual requested output layout. The current dense API retains ambient row and column axes, including fixed axes reinserted by broadcasting, so $n_{\mathrm{out}}$ need not equal the number of unfixed source variables. Its owned output contains $2^{n_{\mathrm{out}}}$ Boolean cells. Allocation and writing impose an exponential materialization cost; total evaluation also includes source compilation and computation.

## E. Replace the provenance wording

> Provenance records the retained construction: $S$ for a derivation containing only structural steps, $T$ for direct tabulation of the returned subtree, and $H$ for a structural step above tabulated ancestry. Negation maps $S$ to $S$ and otherwise to $H$. Fusion returns $S$ only when both children are $S$; all other combinations return $H$. This is a construction update, not a lattice join. Total attempted work is reported separately.

## F. Replace the P14 headline paragraph

> The frozen P14 recipe-to-owned-ANF study failed its promotion criterion. Exact dispatch had case-balanced E/D geometric means of 1.0508 on synthetic cases and 1.0607 on natural cones. The displayed synthetic interval includes parity, while the natural interval is entirely above parity. Five selected synthetic cases were highly favorable, but neither those cases nor an alternative aggregation replaces the preregistered no-go result. This is an ANF-dispatch boundary, not a test of the pair-token compiler against packed evaluation.

## G. Replace the generic-comparator novelty sentence

> Standard small-function and cut-based optimizers also maintain correspondences between table coordinates and input signals. The present contribution is the explicit specification and implementation of this CM-based pair interface, its construction provenance and fallback behavior, and an empirical test of its costs. Mathematical reductions need not be exclusive to CM to be useful; a representation-specific advantage requires a matched-capability comparison.

## H. Proposed abstract

Correspondence matrices encode binary Boolean connectives as four-bit tokens with an ordered operand frame. We specify a partial compiler that normalizes signed or swapped variable occurrences into a declared frame and combines compatible tokens before subsequent evaluation or expansion. Structural construction, exact four-assignment tabulation, hybrid derivations, and failure are distinguished by explicit provenance and a common denotational invariant. The current token API compiles an admitted root; its dense wrapper otherwise evaluates the original expression through an ordinary fallback path. We distinguish token construction, source traversal, sharing, discarded work, and output materialization so that constant-size fusion is not confused with constant-cost compilation. Reported exploratory symbolic studies show local folding reductions also obtained by a matched generic optimizer, while a separate frozen ANF-dispatch study fails its promotion criterion. Neither study establishes an end-to-end advantage for this pair compiler. We therefore present the compiler contract and a prospective task-matched evaluation against direct packed and prepared alternatives, with performance, natural-workload prevalence, and amortization left contingent on the completed experiment.

# 15. Missing artifacts and experiments

The existence of source code and a plan should not be confused with a complete benchmark archive. The actual protocol-v3 file is available [P]; it should not be listed as missing. The following items remain missing from, or not independently established by, this audit's evidence set.

| Required item | Exact gap |
|:---|:---|
| Confirmatory pair run | No completed matching source/arm/output/freeze/raw-observation set located. |
| Project correctness rerun | 116-test historical claim not executed here; add the new contract regressions to the real suite. |
| S1/S2 archive binding | Need exact raw file, generator closure, hash, admission logic, recount script and result. |
| P14 reproducibility binding | Need original/amended freezes, full raw rows, estimator and interval implementation, environment and replay receipts. |
| Natural-root/cut prevalence | Need untouched corpus intake, extraction definition, denominators, design-family grouping and retained-vs-potential folding distinction. |
| Matched generic pair implementation | Explicit frozen secondary arm with equivalent local information and output. |
| Dense endpoint parity | Fixed-axis retention/removal, shape, bit order, budget, ownership and conversion parity across actual APIs. |
| Time and memory policy | Full cold/prepared definitions, process controls, calibrated measurement resolution and failure estimand. |
| Archival release | Immutable source closure, third-party licenses/redistribution permissions, references, code/data manifest and release identifier. |

No expensive cloud campaign is needed to resolve the specification findings. The immediate work is a small set of source-level regression tests and a repaired freeze specification. A pilot then validates the harness; it is not confirmatory evidence.

# 16. Submission-readiness assessment

**Ready now, after the identified corrections:** a focused working preprint or technical report explaining the typed pair-root transformation, its soundness, its provenance, its actual fallback interface, and the inherited evidence boundaries.

**Not established now:** faster complete pair compilation, lower compiler memory, high natural-workload pairability, a broad reusable compiler advantage, or historical priority for frame-aware truth-table composition.

**Next scientific gate:** reconcile the manuscript, actual APIs, and a numbered experimental specification; run the real correctness suite; then freeze and execute the task-matched pair experiment. More foundations theory would not substitute for this gate. A negative or mixed completed result should be retained rather than reframed as a hidden positive.

## Final-paper question checklist

| Question group | Status |
|:---|:---|
| Exact transformation, token type, normalization, fusion soundness | Answered; add explicit scope and environment. |
| Structural versus tabulated versus hybrid | Answered mathematically; strategy/provenance wording needs repair. |
| Fallback trigger and delivered artifact | Source establishes it; manuscript must distinguish signal from execution. |
| Pure-complete fragment | Answered, narrow and syntactic. |
| Asymptotic/constant-factor cost | Partial; diagnostic/name/layout and failed-work costs need explicit accounting. |
| Avoided symbolic expansion work | Reported mechanism evidence, not direct pair timing. |
| Generic reproducibility of reduction | Observed S1/S2 metric ties; no universal implementation equivalence claim. |
| Specific CM metadata advantage | Unresolved beyond explicitness/auditability. |
| Natural prevalence, sharing effects, reuse break-even, output regimes | Need the frozen empirical map; same-token-query no-crossover follows analytically. |
| Closest direct packed baseline | Identified and specified. |
| End-to-end wins/losses for this pair compiler | Unresolved. P14 is a different negative endpoint; P15 is timing-inconclusive. |

The strongest paper is therefore not the longest one. It is the one whose scope, implementation, proofs, and measurements describe the same transformation.

# Sources and verification record

## Supplied sources

**[M]** Brian Theory. *Operator-Level Boolean Computation with Correspondence Matrices*. Revised post-split draft, 22 September 2026, 14 pages. Files `Operator_Level_CM_Compiler_Revised_Draft(1).pdf` and corresponding `.tex`. Page/section references in this report use this version.

**[F]** Brian Theory. *Correspondence and Logical Matrices: A Boolean Operator Calculus*. LM-centered foundations companion, 22 September 2026, 31 pages. Supplied PDF and LaTeX. Used for the publication boundary, not exhaustively re-audited here.

**[O]** *Operator-Level_Boolean_Computation_with_Correspondence_Matrices_current(1).pdf*, 24-page pre-split comparison source. Used for implementation/test/protocol and P14 qualifications lost in shortening, not to override [M].

The supplied panel audit, rules-update notes, revision memo, R1/R2 reports and response, foundations audit, handoff summary and rebuild prompt were used as review history. Historical assertions in them are not treated as fresh verification.

## Public code and records

All following repository paths were inspected at commit `0ab8ffd0c23ffa71ee951d375b1c170ffdcc084b` of **Relative0/Correspondence_Matrices**. The commit pins the inspected files, not necessarily each historical experiment's execution closure.

**[C1]** `cm_build_pair.py`; Git blob `4379a4661d9989cbaf65707f1349fd429fdda434`. Pair recognition, variable collection, provenance, diagnostics, token and dense interfaces.

**[C2]** `cm_token.py`; Git blob `391e9249e288c219f29173f92e3b8cb5cefb7d98`. Token transforms, common query, import-time LUT construction, composition cache.

**[C3]** `cm_normalize.py`; Git blob `ad1ab1c6b0846f1ffb4955df50644c84158c00c9`. Ambient-axis lifting, cached layout metadata, owned output copy.

**[P]** `paper_program/01_audit/EVALUATION_PROTOCOL_V3.md`; Git blob `d496a81c0da673c0a15b02cc20bbe076a0a88d64`. Dated 15 September 2026; analysis plan complete, corpus/environment/run unfrozen. Entire plan inspected.

**[R1]** *CM benchmark audit correction — 2026-08-25*, in `deliverables_n22_24/corrections_2026_08_25`. Paired formula-cluster table and wrapper interpretation inspected; source snapshot and raw-record references listed there.

**[R2]** *Architecture-aware CM comparison refresh after C37*, `docs/research/CM_ARCHITECTURE_AWARE_COMPARISON_REFRESH_AFTER_C37_2026_09_03.md`, updated 4 September. Complete-relation and cross-machine query-ladder sections inspected.

**[R3]** Committed P-series study guide and late-scan status page sources in `deliverables_n22_24/master_explainer_2026_08_03`; latest commit and its predecessor `1e599e1e2af92cb088b4d761c890678e6cd58947`. Curated study indices, not substitutes for raw bundles.

**[R4]** `results/2026-09-21/P15_FINAL_DISPOSITION_20260921.json`, beneath the same site directory; Git blob `156df8b75d9ae552e48dff774698f75ced092121`. Schema `p15-py0-final-disposition/v1`; status `TIMING_INCONCLUSIVE_NO_PERFORMANCE_CLAIM`.

## Primary literature and technical documentation

**[L1]** Daizhan Cheng, Yin Zhao, and Xiangru Xu. *Matrix Approach to Boolean Calculus*. CDC–ECC 2011, pp. 6950–6955. DOI: **10.1109/CDC.2011.6160289**. Inspected author preprint: [DerBool_cdc11.pdf](https://lsc.amss.ac.cn/~dcheng/preprint/DerBool_cdc11.pdf), eight pages, Definition 2.7 and Proposition 3.3. Equation numbering differs from some cited versions.

**[L2]** William Bricken. *Notes on Matrix Techniques for Logic*. Technical note internally dated March 1997. [Author-hosted PDF](https://wbricken.com/pdfs/01bm/01math/03math-supporting/math-tangential/04matrix-tech.pdf). Nine-page parsed text inspected; original public-release and peer-reviewed status unestablished.

**[L3]** Alan Mishchenko, Satrajit Chatterjee, and Robert Brayton. *DAG-Aware AIG Rewriting: A Fresh Look at Combinational Logic Synthesis*. DAC 2006, pp. 532–535. DOI: **10.1145/1146909.1147048**. [Academic-hosted paper](https://web.cecs.pdx.edu/~mperkows/CLASS_573/febr-2007/p532-mishchenko.pdf). Small-cut/NPN/DAG discussion inspected; no benchmark values imported.

**[L4]** mockturtle official documentation. [Cut rewriting](https://mockturtle.readthedocs.io/en/latest/algorithms/cut_rewriting.html). Current documentation inspected on 22 September 2026; explicit truth-table and leaf-iterator interface.

**[L5]** kitty official documentation. [Operations](https://libkitty.readthedocs.io/en/latest/operations.html) and library documentation. Current documentation inspected; do not infer a benchmarked library version from the website version label.

**[L6]** Randal E. Bryant. *Graph-Based Algorithms for Boolean Function Manipulation*. IEEE Transactions on Computers C-35(8), 677–691, 1986. DOI: **10.1109/TC.1986.1676819**. Author publication record and accessible paper located.

**[L7]** LLVM official documentation. [Passes](https://www.llvm.org/docs/Passes.html). GVN/redundancy-elimination and simplification descriptions; version must be pinned for an actual compiler experiment.

**[L8]** Neil D. Jones, Carsten K. Gomard, and Peter Sestoft. *Partial Evaluation and Automatic Program Generation*. Prentice Hall, 1993. [Author-hosted book page and preface](https://studwww.itu.dk/people/sestoft/pebook/). Program-specialization definition inspected; no claim of complete book review.

**[L9]** C. R. Edwards. *The Logic of Boolean Matrices*. The Computer Journal 15(3), 247–253, 1972. DOI: **10.1093/comjnl/15.3.247**. Publisher abstract/metadata inspected, not full paper.

**[L10]** August Stern. *Matrix Logic: Theory and Applications*. North-Holland, 1988. ISBN **9780444704320**. Elsevier edition record/description inspected, not complete book.

**[L11]** Eduardo Mizraji. *Vector logics: The matrix-vector representation of logical calculus*. Fuzzy Sets and Systems 50(2), 179–185, 1992. DOI: **10.1016/0165-0114(92)90216-Q**. Publisher abstract inspected.

**[L12]** Eduardo Mizraji. *Vector Logic: A Natural Algebraic Representation of the Fundamental Logical Gates*. Journal of Logic and Computation 18(1), 97–121, 2008; online 23 October 2007. DOI: **10.1093/logcom/exm057**. Publisher abstract and date record inspected.

**[L13]** Max Willsey et al. *egg: Fast and Extensible Equality Saturation*. POPL 2021; [arXiv:2004.03082](https://arxiv.org/abs/2004.03082). Primary abstract inspected for the algorithmic comparison boundary.

**[L14]** Raimondas Sasnauskas et al. *Souper: A Synthesizing Superoptimizer*. [arXiv:1711.04422](https://arxiv.org/abs/1711.04422), 2017. Primary abstract inspected; no Souper experiment conducted.

**[L15]** Siang-Yun Lee, Heinz Riener, Alan Mishchenko, Robert K. Brayton, and Giovanni De Micheli. *A Simulation-Guided Paradigm for Logic Synthesis and Verification*. IEEE TCAD 41(8), 2573–2586, 2022. DOI: **10.1109/TCAD.2021.3108704**. EPFL publication abstract and author publication list inspected.

**[L16]** Yoav Benjamini and Yosef Hochberg. *Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing*. JRSS B 57(1), 289–300, 1995. DOI: **10.1111/j.2517-6161.1995.tb02031.x**. Primary publisher summary distinguishes FDR from familywise error and states independence assumptions for the original result.

## Independent computation

**[V]** `independent_checker.py`, `independent_results.json`, and `independent_stdout.txt`, supplied with this report. Python 3.13.5, standard library only. This is a new audit reference model, not project source. The test tally distinguishes scalar comparisons, generated-expression properties, and edge checks. It is not a count of unique project tests or a performance experiment.

Reproduce with:

```text
python independent_checker.py --output independent_results.json
```

The source manifest records hashes of uploaded inputs and generated deliverables. No external human review, cloud execution, project-code edit, original benchmark rerun, or performance claim is implied by this package.
