---
title: 'CM/LM Boolean Operator Calculus'
subtitle: 'Correctness, structure, prior art, and publication audit'
author: 'Technical review prepared for Brian Theory'
date: '22 September 2026'
fontsize: 10pt
geometry: margin=0.8in
colorlinks: true
linkcolor: black
urlcolor: blue
toc: true
toc-depth: 1
header-includes:
  - \usepackage{amsmath,amssymb,mathtools,pdflscape,microtype}
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[L]{\small CM/LM mathematical audit}
  - \fancyhead[R]{\small 22 September 2026}
  - \fancyfoot[C]{\thepage}
  - \setlength{\headheight}{14pt}
  - \setlength{\emergencystretch}{3em}
---

# I. Executive verdict

**The manuscript supports a coherent Boolean representation calculus, but does not currently establish a new underlying algebra or a substantial new theorem independent of its classical ingredients.** Its strongest defensible contribution is the explicitly typed integration of numeric Boolean kernels, formula-valued polarity frames, valuation, and logical pairing. The central identities work. There is one definite polarity-index error and several assumptions, terminology boundaries, and historical attributions to tighten.

The main text reviewed is *Correspondence and Logical Matrices: A Boolean Operator Calculus*, revised foundations draft, 22 September 2026, 25 pages [M]. The historical 29-page attachment [H] and the 21-page computational companion [C] were compared separately. The foundations draft was recovered as indexed File Library content, not as a local PDF. Consequently, its equations and arguments can be assessed, but this is not a complete rendered-page typography certification. The two attached PDFs and selected page images were inspected locally. References to numbered statements below concern [M] unless stated otherwise.

The binary pairing identity

$$
\langle A|[M_{X\Theta Y}]|B\rangle
\equiv (A\Leftrightarrow X)\Theta(Y\Leftrightarrow B)
$$

is correct, including for dependent formulas. So are the general valuation formula, pointwise superposition, the arbitrary-arity tensor construction, and rectangular coefficient selection. These do not need a physical measurement interpretation.

The strongest mathematical improvement is to introduce the formula-valued frame matrix

$$
S_X=\begin{pmatrix}X&\neg X\\\neg X&X\end{pmatrix},
\qquad S_X^2=I,
\qquad
\boxed{[M_{X\Theta Y}]=S_X[\Theta]S_Y.}
$$

This normal form explains formation, valuation, pairing, and reconstruction in one calculation. A partition-of-unity characterization of Boolean selector maps then explains precisely why pairing preserves every outer Boolean connective. These are proposed structural additions, not results silently attributed to the existing draft or certified as historically new.

The principal correction concerns Remark 6.11 and Appendix B. Theorem 6.3 defines $\rho_x$ to reverse an axis when $x_i=0$, but the later intertwiner uses $\rho_\delta$ for a symbolic action that reverses when $\delta_i=1$. The corrected expression is

$$
v_{\mathbf1}(\tau_\delta\mathcal L_X(f))
=\rho_{\mathbf1\Updownarrow\delta}C_f.
$$

Independent code executed **1,536,530 assertions or finite characterizations**, covering all binary CMs, all binary outer operations, signed alignment, logical pairing, valuation, all candidate binary formula tensors, selected exhaustive higher-arity domains, and the compact spectral classification. Counterexamples are recorded separately: the printed intertwiner fails in 48 of its 64 binary function/mask cases. No original compiler implementation or speed benchmark was run.

The novelty result is deliberately narrower than either praise or dismissal. Known Boolean function composition, orthogonal expansion, pointwise function algebras, group actions, and ordinary substitution explain the mathematical substance of the current central theorems. The search did not locate an earlier source presenting the entire same named CM/LM package. That does not certify priority for the package. Some older books and articles were accessible only in preview or abstract form.

**Present classification:** sound in substance after correction, but mainly an expository/representational synthesis. **Plausible target:** publication after major revision in a venue receptive to logical representation or methodology. The evidence does not support calling it a strong new-results pure-mathematics paper after merely cosmetic revision.

# II. Claim-by-claim correctness audit

Classification: **C** correct as stated; **A** missing assumptions; **T** mathematically correct but elementary/redundant as an independent result; **I** incorrect; **U** unclear typing or convention; **M** correct but insufficiently motivated. A standard result can be important to the exposition. These labels are not recommendations to delete all elementary material.

\small

| Location | Status | Assessment and action |
|:---|:---:|:---|
| $\mathbb B$, $\mathbb F_2$, true-first states, Eqs. (1)--(3) | C | Preserve notation. State encoding $x\mapsto(x,\neg x)^T$ is affine, not linear. |
| Proposition 2.1, unique binary representation | T | Bijection with four-bit tables; useful representation contract. |
| Proposition 2.2, coefficient selection | C | Exactly one summand survives. |
| Remark 2.3, XOR versus OR | C | Interchangeable only for disjoint/one-hot selection, not arbitrary products. |
| Proposition 2.4, matrix-unit expansion | T | Standard basis expansion; not the same basis as ANF. |
| Coefficient-space linearity | C | Does not imply that the represented truth function is input-linear. |
| Eq. (6), transpose and polarity flips | C | Left multiplication flips rows; right multiplication flips columns; transpose exchanges operands. |
| Eq. (7), output complement | C | Entrywise $J\Updownarrow[\Theta]$; an affine, not linear, coefficient map. |
| Support order and Eq. (8) | C | Ordinary Boolean support inclusion/difference, not division. |
| Eq. (9) polarity; Eq. (10) LM | C | Declare the ambient formula algebra and equality modulo equivalence. |
| Theorem 3.1, general valuation | C | Correct for arbitrary reference formulas under any actual valuation. |
| Theorem 3.1, all-true specialization | A | Requires a valuation making the reference operands simultaneously true. Automatic for free generators, not arbitrary formulas. |
| Eq. (12), formula-state pairing | C | Equivalence, given by two disjoint minterms. |
| Theorem 4.1, logical pairing | C | Correct even for dependent formulas. Distinguish a selected LM row from an agreement bit supplied to $\Theta$. |
| Example 4.2, implication | C | Explain vacuous truth; a true pairing need not mean both references match. |
| Theorem 4.3, valuation/pairing | C | Valuation preserves the Boolean contraction term. |
| Eq. (15), pointwise outer lift | C | Distinct from matrix multiplication. |
| Theorem 5.1, aligned superposition | C | Valid for every Boolean outer connective in the same operand frame. |
| Example 5.2, signed implication example | C | Aligned words $0111$ and $1110$ XOR to XNOR, $1001$. |
| Eq. (18), canonical term extension | C | Well-defined modulo logical equivalence; supply the short substitution argument. |
| Definitions 6.1--6.2, tensors and LM lift | C | Exactly $2^n$ slots. The declared free-generator algebra supports the reference-cell characterization. |
| Eq. (22), higher contraction | C | Direct coordinate selection. |
| Theorem 6.3, general valuation | C | Correct under its zero-triggered reversal convention. |
| Definition 6.4, pointwise outer operation | C | Formula entries use the canonical Boolean term extension. |
| Theorem 6.5, faithful lift/superposition | C | Correct; standard function-algebra representation mechanism. |
| Corollary 6.6, subalgebra image | C | Pointwise Boolean subalgebra, not a claim of closure under ordinary matrix product. |
| Remark 6.7, orbit interpretation | U | Identify the group mask as $\mathbf1\Updownarrow\alpha$. The image is not the entire coinduced object. |
| Example 6.8 | T | Correct, but duplicates the OR/AND/XOR example later. |
| Theorem 6.9, equivariance characterization | C | Correct for entries in the declared free formula algebra. |
| Remark 6.10, clone interpretation | U | A faithful realization of superposition is justified. A fully internal clone representation needs cross-arity composition and projections specified. |
| Remark 6.11 and Appendix B | I | The reversal-mask complement is missing. |
| Theorem 6.12, coherence | C | Correct for common input reindexing, fixed selectors, and formula term extensions. It is not universal pairwise commutation of all operations. |
| Example 6.13 | T | Correct; combine with Example 6.8. |
| Eqs. (27)--(28), n-ary pairing | C | Correct; incorporate explicitly into the main theorem with a proof. |
| Definition 7.1, flattening | U | For ordered/noncontiguous blocks, specify axis permutation followed by reshape or use an assembly map. |
| Theorem 7.2, rectangular selection | C | Dimensions and scalar selection are correct. |
| Remarks 7.3--7.4, interpretation and size | C | No compression or physical implication. Equal dimensions still require identification of labelled spaces for an endomorphism interpretation. |
| Theorem 8.1, block lift | C | Correct conditional theorem for the displayed disjoint-block decomposition. Not every function has this form. |
| Corollary 8.2, conjunctive separability | C | Correct outer product. Add the rank-at-most-one converse. |
| Example 8.3, four variables | C | Correct in the declared $(W,X)\mid(Y,Z)$ partition. |
| Theorem 9.1, signed frames | U | Correct transformations/group. State whether the pullback is a right action or uses inverse group elements. |
| Theorem 9.2, reindexing/superposition | T | Correct pointwise identity, already contained in Theorem 6.12. |
| Proposition 10.1, top ANF coefficient | C | Correct for positive arity; specify conventions for any nullary case. |
| Corollary 10.2, binary degree criterion | T | Correct standard parity consequence. Prefer explicit algebraic degree language. |
| STP comparison | C | Correct when delta encoding and column order are declared. |
| Eqs. (43)--(45), quarter-turn | C | Correct coefficient-position permutation and logical input substitution. |
| Phase-algebra boundary | C | Additional convolution must remain separate from compact products and entrywise operations. |
| Section 12, characteristic polynomials/Table 1 | C | The selected compact spectral examples are correct over $\mathbb F_2$. |
| Eight idempotents/four symmetric idempotents | C | Confirmed independently. |
| Eqs. (46)--(47), basis reconstruction | T | Correct; move earlier for semantic value. Already present in the historical work. |
| Eq. (48), diagonal truth operator | C | Assignment vectors form an eigenbasis; they need not be the only eigenvectors. |
| Eq. (49), valuation spectral profile | M | Meaningful derived object, but peripheral to coherence. |
| Section 13, compiler interpretation | C/A | Mathematical admission/fusion rules are sound; empirical attributions require actual source artifacts. |
| Proposition 14.1, Boolean closure | T | Scalar/term closure, not closure of normalized logical states or of a fixed-frame LM family under matrix product. |
| Appendix A | C/U | Correct expansion; standardize assignment-indexed versus position-indexed subscripts. |

\normalsize

## The actual polarity error

For one variable, choose $f(x)=x$ and $\delta=0$. The left side of the printed intertwiner is the unchanged vector $(1,0)$. The earlier definition makes $\rho_0$ reverse that vector to $(0,1)$. No complicated example is needed.

Either retain $\rho$ and replace the later subscript by $\mathbf1\Updownarrow\delta$, or introduce a consistently one-triggered action

$$
\pi_\delta C[\alpha]=C[\alpha\Updownarrow\delta],
\quad
v_x\mathcal L_X(f)=\pi_{\mathbf1\Updownarrow x}C_f,
\quad
v_{\mathbf1}\tau_\delta\mathcal L_X(f)=\pi_\delta C_f.
$$

## Companion-paper audit

The companion's numeric selection, signed alignment, same-frame fusion, LM valuation/pairing, ANF conversion, and the mathematical structural-induction argument are correct under their stated contracts [C, Sections 3--4 and Appendix A]. Its ordinary fallback branch additionally relies on correctness of the ordinary IR evaluator. Exact two-variable support is an admission policy, not a necessary condition for two-input table representability.

Equation (19), $D_{ab}=T_{1-a,1-b}$, must use array-position indices rather than the assignment-labelled CM subscripts used elsewhere. The true-first token versus false-first dense-array storage convention is intentional; confusing it with a change of represented function is the risk.

The attachment reports implementation checks but explicitly says that the confirmatory performance campaign has not been executed. This audit verifies the finite mathematics independently, not the reported 116-test implementation suite. Any foundations sentence attributing exploratory comparison results to this companion needs the actual experiment artifact or weaker wording. The LM is not used in the timed compiler path; the abstract should not imply otherwise.

# III. Mathematical architecture

## A precise organizing claim

For a fixed arity and declared frame, truth functions, numeric truth kernels, and the LM image are isomorphic as pointwise Boolean algebras:

$$
f\in\mathcal B_n,\qquad
C_f\in\mathbb B^{\mathbb B^n},\qquad
\mathcal L_X(f)\in\mathcal F_X^{\mathbb B^n}.
$$

Valuation is a Boolean-algebra homomorphism; signed input changes are pullbacks; logical pairing is a selector built from a Boolean partition of unity. Across arities, the family realizes ordinary Boolean superposition. These are precise structural assertions, unlike an unqualified statement that matrices are operators [B3--B6].

## Frame normal form: a recommended addition

Products in this subsection are explicitly taken over the **formula Boolean ring** $(\mathcal F,\Updownarrow,\wedge)$. They are an auxiliary symbolic matrix algebra, not a redefinition of numeric CM multiplication, pointwise superposition, or logical pairing.

For

$$
S_X=\begin{pmatrix}X&\neg X\\\neg X&X\end{pmatrix}
$$

we have $S_X^T=S_X$ and $S_X^2=I$, because $X\neg X=0$ and $X\Updownarrow\neg X=1$. Expanding the upper-left cell of $S_X[\Theta]S_Y$ gives the disjoint-minterm form of $X\Theta Y$; the other cells give its polarity substitutions. Therefore

$$
\boxed{[M_{X\Theta Y}]=S_X[\Theta]S_Y,\qquad
[\Theta]=S_X[M_{X\Theta Y}]S_Y.} \tag{A}
$$

This reconstructs the whole operator even when $X$ and $Y$ are dependent. For example, $X=P,Y=\neg P$ has no all-true valuation, but the second identity still holds. Thus lack of that special valuation does not destroy faithfulness of the entire matrix. It does limit arguments based only on a reference cell or on treating compound operands as free generators.

Since $v(S_X)=[\Updownarrow]^{1-v(X)}$, valuation follows from (A). Also

$$
\langle A|S_X=\langle A\Leftrightarrow X|,
\qquad
S_Y|B\rangle=|Y\Leftrightarrow B\rangle.
$$

For $K_X=\bigotimes_i S_{X_i}$ in true-first order, $K_X^2=I$ and

$$
\operatorname{vec}(M_f(X))=K_X\operatorname{vec}(C_f).
$$

An ordered rectangular flattening obeys

$$
[M_f(X)]_{R\mid C}=K_{X_R}[f]_{R\mid C}K_{X_C}^{T}. \tag{B}
$$

These formulas are new to the present draft's organization, not certified new mathematics. Boolean orthogonal bases and partition-valued matrices are close antecedents [B3].

## The selector lemma behind coherence

Let $q_w:\mathcal F^I\to\mathcal F$ be $\mathcal F$-linear, with

$$
q_w(T)=\mathop{\Updownarrow}_{i\in I}w_i\wedge T_i.
$$

It is a unital Boolean-algebra homomorphism **if and only if**

$$
w_iw_j=0\ (i\ne j),\qquad
\mathop{\Updownarrow}_{i\in I}w_i=1. \tag{C}
$$

For necessity, apply product and unit preservation to coordinate idempotents. For sufficiency, expand $q_w(T)q_w(U)$: all unequal-index terms vanish. Unit preservation gives complement preservation; XOR preservation is already linearity. Every Boolean term is consequently preserved.

For logical pairing, $w_\alpha=\bigwedge_i A_i^{\langle\alpha_i\rangle}$ satisfies (C), even when the formulas $A_i$ are dependent. This, not a nonexistent distributive law for arbitrary outer connectives, is why pairing respects all pointwise Boolean operations. The $\mathcal F$-linearity condition is essential to the stated classification of selectors.

## Canonical Boolean term lift

Two Boolean terms equal on every bit assignment remain logically equivalent after formula substitution: evaluate the substituted terms under any valuation and use the original truth-function equality. Thus the disjoint-minterm expression defines $\widetilde f$ independently of the chosen representative. This short proof completes the draft's well-definedness claim.

# IV. Novelty and prior-art audit

## Bricken: chronology and features

The inspected nine-page note is internally dated **March 1997**. It is a technical note; its original public-release date and peer-reviewed publication status were not established [B1]. The comparison is with this note, not Bricken's entire corpus.

| Feature | Inspected note |
|:---|:---|
| Sixteen compact truth matrices | Explicit. |
| Two-component states and bra--matrix--ket evaluation | Explicit. |
| XOR/AND arithmetic | Discussed. |
| Transpose and complement | Explicit. |
| Operators as operands | Addition/product examples. |
| Symbolic entries | State/outer-product expressions. |
| Systematic LM polarity lift | Exact construction not located. |
| General LM pairing identity | Not located. |
| LM valuation architecture | Not located. |
| Arbitrary-outer-operation coherence | Not located as a theorem. |

The note also displays $2$ and negative entries. Hence Boolean closure is a distinction of scope, not a claim that Bricken never discussed Boolean arithmetic. No dependency or plagiarism inference follows from antecedence.

## A particularly direct antecedent

Cheng, Zhao, and Xu's **2011** *Matrix Approach to Boolean Calculus*, Definition 2.7 and Proposition 3.3, Eq. (17), explicitly uses XOR--AND matrix arithmetic and combines truth vectors entrywise under an arbitrary binary Boolean outer operation [B2]. This is a direct antecedent for the raw numeric superposition law. Reshaping the vector does not make that law new. The symbolic/frame organization remains a separate comparison question.

## Matrix, vector, and spectral logic

Edwards's 1972 paper is an early Boolean-matrix logic source, but its accessible abstract does not settle exact LM antecedence [B7]. Stern's 1988 book establishes a developed matrix-logic program; a preview cannot certify absence of the pairing construction throughout the book [B8].

Mizraji's vector logic represents logical values in real vector spaces and dyadic gates on tensor-product inputs. That differs from a compact scalar-valued $2\times2$ kernel, but is prior art for operator and outer-product logic. The inspected 2008 article was first available online in 2007; the 1992 article was not fully accessible [B9].

Eigenlogic's assignment-space diagonal truth operators are direct antecedents for $D_\Theta$. The later accessible version of Toffano's preprint explicitly says it intentionally avoids Dirac notation. Cite its spectral construction, not an alleged use of bra-ket typography [B10--B11].

## Boolean expansion, free algebras, and group actions

Orthogonal Boolean expansion is substantially older than the present work; Sampei's 1950 paper is an early relevant source, and later orthonormal-expansion literature makes the partition mechanism explicit [B12--B13]. Free Boolean-algebra and Boolean-power constructions supply the natural functional setting [B4]. The standard coinduction construction supplies the surrounding function object, while the LM is its particular orbit image, not the entire coinduced object [B5].

When formulas in $\mathcal F_X$ are read as Boolean functions, the whole construction has the simple form

$$
M_f(x,\alpha)=f(x\Updownarrow\alpha\Updownarrow\mathbf1). \tag{D}
$$

Thus the lift is a pullback along a fixed map. Its injectivity, pointwise-operation preservation, valuation identities, and the stated equivariance characterization follow from ordinary function algebra. This succeeds as a hostile reduction of the central mathematical claims.

## Logic synthesis and bibliography

Classical superposition is the subject of Boolean clone/iterative-system theory; it is not quantum superposition [B6]. NPN changes and small-cut truth-table manipulation have explicit logic-synthesis antecedents [B14--B15]. These do not establish equal implementation costs, but they require fair local-table comparators before a CM-specific speed claim.

The draft's undated Zhao--Gao--Cheng preprint has a likely related 2012 journal version with the same authors and a modified title. Its publisher record gives receipt in June 2011 and publication in November 2012. Compare full versions before replacing the citation [B16]. Distinguish issue year, advance publication, preprint version, website reposting, and file metadata throughout.

No exact full-package antecedent was located. That is a bounded search result, not proof of theorem novelty or historical priority. Positive antecedents above are enough to reject broad novelty claims for notation, table combination, orbit injectivity, and ordinary evaluation.

# V. Central theorem assessment

**Retain Theorem 6.12 as the organizational center, but do not use its name as evidence of mathematical novelty.** Its four parts are correct under the stated common-frame and Boolean-selector interpretation. The normal form and selector lemma explain why they belong together.

For each declared semantic map $q:D\to E$ and every outer operation $g$, the common pattern is

$$
q\circ\widehat g_D=\widehat g_E\circ q^m,
\qquad
\begin{array}{ccc}
D^m&\xrightarrow{\widehat g_D}&D\\
\downarrow q^m&&\downarrow q\\
E^m&\xrightarrow{\widehat g_E}&E.
\end{array}
$$

The relevant maps include numeric/formula lifts, valuation, common input pullback, and partition selectors. Pairing/valuation naturality additionally says

$$
v(\mathfrak p_{A,B}(M))
=\mathfrak p_{v(A),v(B)}(vM).
$$

The selectors must be valuated too. Similarly, preservation of a scalar under a frame change needs corresponding selector transport; a fixed selector is not invariant under every reindexing.

Output negation is not one of the unchanged-$g$ input-frame symmetries. The correct general law uses the dual operation:

$$
\neg\widehat g(M_1,\ldots,M_m)
=\widehat{g^d}(\neg M_1,\ldots,\neg M_m),
\quad
 g^d(b)=\neg g(\neg b).
$$

For XOR on two zero inputs, pretending that the same $g$ works gives $1=0$. This is a boundary clarification, not evidence that the printed input-reindexing theorem is false.

The present theorem does not yet cover ordinary matrix composition or the block-lift operation. Add their separate laws or avoid saying that every composition in the paper is already covered. A commuting cube is possible, but only with fully specified vertices, selector valuation, and frame actions. A small family of correct squares is preferable to an ambiguous cube.

# VI. Logical pairing assessment

From the normal form,

$$
\begin{aligned}
\langle A|[M_{X\Theta Y}]|B\rangle
&=\langle A|S_X[\Theta]S_Y|B\rangle\\
&=\langle A\Leftrightarrow X|[\Theta]|Y\Leftrightarrow B\rangle\\
&\equiv(A\Leftrightarrow X)\Theta(Y\Leftrightarrow B).
\end{aligned}
$$

The final selection holds because the formula-state entries are partitions of unity, or by checking every valuation. No independence assumption is needed.

The operation applies the chosen connective to agreement with a reference frame. **Symbolic matrix-element semantics** is precise. **Relationship extraction** is reasonable when immediately defined by the formula. **Compatibility testing** requires stating which agreement patterns $\Theta$ accepts. Implication can be true because its first agreement bit is false. Statistical correlation, collapse, or physical observation has not been defined.

For assignment bits $i,j$,

$$
\langle X^{\langle i\rangle}|[M_{X\Theta Y}]|Y^{\langle j\rangle}\rangle
\equiv\Theta_{ij}.
$$

This is complete labelled basis reconstruction, already present in the draft's Section 12 and historical Section 4.1.4. Move it earlier. It is elementary but semantically useful; calling it a new tomography theorem would overstate the result.

The n-ary version is

$$
\mathfrak p_A(M_f(X))
\equiv\widetilde f(A_1\Leftrightarrow X_1,\ldots,A_n\Leftrightarrow X_n).
$$

Setting $A_i=X_i^{\langle\beta_i\rangle}$ recovers $f(\beta)$. One generic pairing does not determine an arbitrary function; its complete labelled basis table does.

The historical manuscript already gives an expanded expression equivalent to the modern binary identity. The modern compact statement and all-arity organization are improvements, not a first discovery of that identity in 2026 [H]. Broader priority is limited by access to older literature.

# VII. Operator-on-operator computation assessment

The three operations must appear together early:

$$
AB,\qquad A\widehat\Phi B,\qquad g(f_1,\ldots,f_m).
$$

The first contracts an intermediate index by XOR--AND. The second combines matching entries. The third substitutes functions into a Boolean outer function. The representation theorem realizes the third by the second, not all three by one operation.

For fixed arity, the CM representation and LM image are faithful pointwise Boolean-function algebras. A full clone representation across arities can be completed by transporting projections and ordinary superposition through these faithful maps. Its associativity then follows from ordinary function composition. This is valid, but not an additional difficult theorem.

The operator language is appropriate once its type is specified: a square CM is an endomorphism of a chosen coordinate space; a rectangular CM is a linear map; either can be a scalar-valued Boolean kernel. The same array has several uses, which must not be conflated. Entrywise $A\widehat\Phi B$ is not spectral matrix functional calculus.

The strongest wording is **a typed symbolic/numeric representation of Boolean superposition with polarity-frame and pairing semantics**. Its application can be useful even if a performance advantage is not uniquely CM-specific. Performance remains a separate empirical question, and the companion should own the matched-baseline evidence [C].

# VIII. Higher-dimensional assessment

The explicit numeric truth tensor has exactly $2^n$ bits. Any $2^p\times2^q$ flattening, $p+q=n$, has the same entry count. A formula-valued tensor has $2^n$ formula slots, not necessarily $2^n$ bits of representation cost.

For ordered blocks $R,C$, define an assembly map placing row and column bits into their original variable positions:

$$
[f]_{R\mid C}[r,c]
=f(\operatorname{assemble}_{R\mid C}(r,c)).
$$

This avoids silently treating a noncontiguous variable partition as an ordinary reshape. The corresponding vectorized operation is axis permutation followed by reshape.

A useful rectangular example is

$$
f(X,Y,Z)=X\Updownarrow(Y\wedge Z),\qquad
[f]_{X\mid(Y,Z)}=
\begin{pmatrix}0&1&1&1\\1&0&0&0\end{pmatrix}.
$$

It is a map $\mathbb F_2^4\to\mathbb F_2^2$ and still supports scalar bra--map--ket selection.

The block theorem correctly assumes $f(a,b)=g(a)\Theta h(b)$ on disjoint blocks. It does not say that every function admits one-bit summaries of both blocks. Equality of two two-bit blocks has four distinct row behaviors and cannot have that form, which permits at most two. Universal representability instead follows from minterm/Shannon expansion or common-support cylinder extension followed by pointwise combination. Syntax-tree subexpressions can share variables, so repeated disjoint-block construction alone is not a general completeness proof.

The missing useful interpretation is

$$
f(r,c)=g(r)\wedge h(c)
\quad\Longleftrightarrow\quad
\operatorname{rank}_{\mathbb F_2}[f]_{R\mid C}\le1.
$$

For nonzero matrices this is the ordinary rank-one factorization, unique over $\mathbb F_2$; zero has degenerate nonunique factors. More generally, the minimum number of conjunctive factors in an XOR decomposition

$$
f(r,c)=\mathop{\Updownarrow}_{i=1}^{k}g_i(r)\wedge h_i(c)
$$

is exactly the flattening's $\mathbb F_2$ rank. Each summand has rank at most one, and a rank factorization attains the bound. This is not the OR-based Boolean-rank problem.

Rank survives row/column permutations and transpose, not arbitrary repartitioning. For

$$
f=(X_1\Leftrightarrow X_2)\wedge(X_3\Leftrightarrow X_4),
$$

the ranks in partitions $12\mid34$ and $13\mid24$ are $1$ and $4$ respectively. Invariants must name the allowed action. Hamming weight is preserved by input changes and sent to $2^n-w$ by output complement. Algebraic degree is preserved by signed input permutations, and by output complement for nonconstant functions. Full-degree parity is invariant for positive arity. Spectra generally are not preserved by independent row and column changes.

# IX. Spectral and observable material assessment

**Keep a short explanatory boundary; move the full classification and valuation-spectrum study to an appendix or a separate paper.** The following atlas was independently computed over $\mathbb F_2$.

| Property | Count among sixteen CMs |
|:---|---:|
| Rank zero / one / two | 1 / 9 / 6 |
| Idempotent | 8 |
| Symmetric idempotent | 4 |
| Square-zero, including zero | 4 |
| Involution, including identity | 4 |
| Diagonalizable over $\mathbb F_2$ | 8 |
| No eigenvalue in $\mathbb F_2$ | 2 |

The characteristic-polynomial classes $\lambda^2$, $(\lambda+1)^2$, $\lambda(\lambda+1)$, and $\lambda^2+\lambda+1$ have sizes $4,4,6,2$. OR and NAND are the nonsplitting cases; they diagonalize over $\mathbb F_4$. XOR has repeated eigenvalue $1$ and is not diagonalizable even after field extension. The all-ones tautological CM squares to zero. These examples show why compact spectra are not truth-value readouts.

The associated diagonal operator

$$
D_\Theta=\operatorname{diag}(\Theta_{11},\Theta_{10},\Theta_{01},\Theta_{00})
$$

has an assignment-labelled eigenbasis with the truth values as eigenvalues. This is an established Eigenlogic-style representation [B10--B11]. The unlabelled spectrum retains only the count of ones; the basis labels carry the rest of the truth table.

Independent input polarity changes act by left/right equivalence, not generally similarity. Rank is preserved; eigenvalues, idempotence, and nilpotence need not be. A valuation spectral profile is meaningful but not automatically an invariant under every frame transformation.

No positive-definite inner product, probabilities, Born rule, or physical preparation/measurement semantics follows from these matrices. Use projector in the algebraic idempotent sense only when that meaning is stated. Older Boolean-matrix eigenvalue references often concern a different scalar algebra; do not use their titles alone as evidence about field spectra.

# X. Original-2018 recovery audit

The public record lists the historical manuscript in May 2018 and states that its content was uploaded on **1 October 2018** [H-public]. These dates must not be conflated. The attached PDF's metadata records a later, 2022 compilation, so it is not itself a byte-identical proof of the earliest public version.

| Historical material | Decision | Reason |
|:---|:---|:---|
| Arbitrary outer-connective operator computation | Restore prominence; credit 2018 | Explicit in Sections 3.2.1 and 3.2.3. |
| Formula-valued LM | Retain modern definition | Earlier core idea, clearer current typing. |
| Positive valuation | Retain with assumptions | General valuation is the better statement. |
| Pairing and basis extraction | Move earlier | Already in historical Section 4.1.4. |
| Matrix-unit basis | Retain briefly | Useful standard explanation. |
| Conjunctive factoring | Restore via rank | Avoid historical product ambiguity. |
| Higher-dimensional construction | Superseded | Ordered tensors/flattenings repair the indexing. |
| Four-variable example | Retain with declared partition | Its displayed numeric values can be correct despite surrounding ordering problems. |
| Rotation and signed symmetry | Retain briefly | Classical input transport, not new phase physics. |
| Support containment/difference | Retain correct operation | Not a quotient or arithmetic remainder. |
| Modulo/division interpretation | Remove | Undefined zero divisors in scalar arithmetic and incorrect identification. |
| Measurement/collapse language | Remove or label historical | No physical operational semantics. |
| Broad complexity suggestions | Remove pending evidence | Explicit arbitrary truth objects still have $2^n$ outputs. |
| Phase algebra and full spectral dynamics | Another paper | They obscure the coherence story. |

On historical page 12,

$$
(X\Rightarrow Y)\Updownarrow(X\vee Y)=\neg X
$$

is false. The correct result is $\neg Y$, word $0101$. On page 17, the juxtaposed asymmetric-matrix factorization is false as XOR--AND matrix multiplication: duplicate summands cancel. Its intended entrywise conjunction is correct. On page 19, two state-pairing minterms must be joined by XOR or disjoint OR, not XNOR.

The three historical four-variable matrices were independently checked on every assignment in the $(W,Y)\mid(X,Z)$ partition and are correct. Surrounding Kronecker-order notation is not thereby validated. Reversing tensor-factor order requires a permutation; transposition alone does not do it. The modern example uses $(W,X)\mid(Y,Z)$, so a different displayed array is expected.

Other historical statements need replacement rather than restoration: calling arbitrary XOR decompositions ANF; confusing a diagonal embedding of a compound truth value with its general binary polarity LM; inconsistent higher-arity basis counts and index ranges; and an observables reference pointing to a duplicated Dirac-notation URL.

# XI. Missing mathematics

The frame normal form (A), selector characterization (C), n-ary pairing, and basis reconstruction are the highest-value additions. They explain rather than enlarge the paper indiscriminately. Rank/separability is the most useful concise application.

If ordinary matrix composition is intended to belong to the calculus, add the following separate theorem. Define $\Omega$ by

$$
[\Omega]=[\Theta][\Psi],\qquad
x\Omega z=\mathop{\Updownarrow}_{y\in\mathbb B}
 (x\Theta y)\wedge(y\Psi z).
$$

With the **same intermediate reference frame $Y$**, symbolic matrix multiplication satisfies

$$
\boxed{[M_{X\Theta Y}][M_{Y\Psi Z}]=[M_{X\Omega Z}].} \tag{E}
$$

Indeed,

$$
S_X[\Theta]S_Y S_Y[\Psi]S_Z
=S_X([\Theta][\Psi])S_Z.
$$

This is parity-based kernel composition, not existential relation composition or clone substitution. It extends to rectangular blocks with matching dimensions and intermediate frames. The identity in an $X$-to-$X$ frame is $S_XIS_X=I$.

The theorem must not be confused with closure of a fixed $(X,Y)$ LM family under arbitrary products. In general,

$$
[M_{X\wedge Y}]^2=(X\Leftrightarrow Y)[M_{X\wedge Y}],
$$

whose coefficients after inverse frame transformation are not constant bits. Matched composable frames and common pointwise-combination frames are different contracts.

Equation (E) is proposed here, not attributed to the current manuscript or claimed as historically new. A category of framed finite kernels would formalize this law, but category terminology is optional. Full morphism classification, Post-lattice classification, universal-property excursions, and semigroup dynamics should be added only for a substantive payoff, not as mathematical decoration.

# XII. Editorial and notation corrections

**Mathematical corrections:** repair the reversal mask; qualify all-true valuation; define pullback direction; keep output negation separate from the common-input-frame identity; make the block theorem's conditional scope explicit.

**Novelty corrections:** credit the earlier binary pairing and arbitrary outer-connective computation; cite the direct 2011 truth-vector identity; do not infer 1997 public availability from an internal note date; distinguish a new organization from new component mathematics.

**Clarifications:** use equality for elements of the quotient formula algebra and equivalence for formula representatives, or explicitly explain the convention. Syntactic equality is a different assertion. Retain $\Theta,[\Theta],\Updownarrow,\Leftrightarrow$. Use $f$ naturally for arbitrary arity. Standardize assignment-indexed $X^{\langle i\rangle}$ and distinguish it from array positions.

Numeric products have coefficients in $\mathbb F_2$; auxiliary symbolic products have coefficients in the formula Boolean ring. Neither is entrywise superposition. The phrase formula-valued LM avoids collision with STP's numeric logical matrices. Use correspondence map for rectangular arrays and Boolean kernel for their scalar-valued truth semantics. Calling a square CM an operator is legitimate once domain, codomain, and basis identification are declared.

Boolean closure means that the specified constructions stay within Boolean scalars/formulas. It does not mean normalized logical states are closed under all vector operations: $|A\rangle\Updownarrow|A\rangle=(0,0)^T$ is Boolean-valued but not of the form $(B,\neg B)^T$.

**Accessibility:** replace repeated claims that this is more than a truth table with one worked chain: implication CM, its LM, a nontrivial valuation, a pairing, and a signed superposition. Example 5.2 is useful. Examples 6.8 and 6.13 need not both repeat OR/AND/XOR. Add the $2\times4$ example above instead.

**Figures:** the indexed foundations captions explain the CM/LM bridges and flattening, but do not themselves specify every compatibility square. Add a typed square showing one outer operation on both levels and state-selector valuation. Show the ordered variable assembly in the flattening figure. The companion's page-13 pairing/valuation figure has a useful sequence but crowded, small equations; its important formulas should be vector text at body-readable size. Final visual certification of the foundations PDF remains a separate check because its local rendering was unavailable.

# XIII. Recommended final paper structure

| Section | Content |
|:---|:---|
| 1. Motivation and exact boundary | One concrete calculation; state the nonphysical and modest novelty claims. |
| 2. Numeric correspondence kernels | True-first selection, three compositions, coefficient linearity, signed input changes. |
| 3. Formula-valued polarity frames | LM definition, normal form, valuation, free versus substituted operands. |
| 4. Logical pairing and reconstruction | Agreement semantics, basis recovery, partition selector lemma. |
| 5. Operators as operands and coherence | Pointwise Boolean superposition, unified theorem, worked square. |
| 6. Higher arity and rectangular maps | Tensors, ordered flattening, n-ary pairing, conditional block construction. |
| 7. Structural consequences | Equivariant image, rank/separability, optional matched-frame product. |
| 8. Relationship to prior work | Feature comparison, chronology, clone/Boolean-algebra interpretation. |
| 9. Computational application and boundaries | Brief admission/fusion interpretation; refer implementation and evidence to companion. |
| 10. Discussion and conclusion | State exactly what the framework enables and what remains unproved/unmeasured. |
| Appendices | Finite checks, spectral boundary/atlas, notation crosswalk, longer historical corrections. |

Give brief credit where an idea first appears rather than postponing all antecedents to Section 8. Keep quarter-turn geometry with signed frames. The full cyclic phase algebra and extensive spectral dynamics belong elsewhere.

# XIV. Novelty ledger

Confidence concerns the assigned category, not a numerical probability of global priority. No entry is certified as new theorem mathematics.

```{=latex}
\begin{landscape}
\small
```

| Result/idea | Closest antecedent | Date/source | Same result? | Difference | Novelty confidence | Recommended wording |
|:---|:---|:---|:---|:---|:---|:---|
| Compact truth matrices | Matrix logic | 1972; note 1997 [B7,B1] | Substantially | Frame convention | Established, high | We use a compact correspondence representation. |
| Boolean bra-ket selection | Explicit logical matrix elements | Note 1997 [B1] | Numeric level | LM organization | Established, high | Useful antecedented notation. |
| XOR--AND matrix arithmetic | Boolean matrix calculus | 2011 [B2] | Yes | Typed use | Established, high | Declared field algebra. |
| Minterm term lift | Orthogonal Boolean expansion | 1950 and later [B12,B13] | Mechanism | Polarity/tensor package | Standard consequence | Canonical term extension. |
| Signed input frames | NPN transformations | Synthesis literature [B14,B15] | Yes | Matrix transport | Established, high | Matrix realization of classical symmetries. |
| Formula-valued binary LM | Author's polarity construction | 2018 [H] | Yes | Explicit modern types | Earlier author contribution | Formalization of the earlier LM. |
| General valuation | Formula evaluation and polarity | Boolean algebra [B4]; [H] | Standard extension | Explicit frame formula | Standard consequence | Valuation/frame compatibility. |
| Binary pairing | Expanded agreement identity | 2018 [H, Sec. 4.1.4] | Equivalent | Compact statement | Earlier author contribution | Earlier pairing in explicit semantic form. |
| N-ary pairing | Partition selection | Boolean expansion [B12,B13] | Mechanism | Uniform tensor notation | Standard consequence | Higher-arity pairing semantics. |
| Arbitrary outer composition | Pointwise truth-vector operation | 2011 Prop. 3.3 [B2] | Yes numerically | Formula/frame compatibility | Established, high | Representation of Boolean superposition. |
| Faithful embedding | Function algebra and orbit encoding | Standard [B4,B5] | Mechanism | Particular polarity image | Standard consequence | Identification theorem. |
| Equivariance characterization | Identity-element reconstruction | Standard group actions [B5] | Structurally | Concrete LM membership test | Standard consequence | Intrinsic characterization. |
| Subalgebra image | Pointwise Boolean algebra | [B4] | Structurally | Specified image | Standard consequence | The image is a Boolean subalgebra. |
| Coherence theorem | Homomorphisms and pullbacks | [B2--B5] | Parts follow | Combined typed statement | Integrated construction, moderate at most | Unified compatibility theorem. |
| Block outer lift | Truth-table/tensor decomposition | Boolean expansion and vector/STP logic | Mechanism | Rectangular symbolic contract | Standard consequence | Conditional typed block construction. |
| Rank/separability | Rank-one outer product | Field linear algebra | Yes | Logical meaning | Useful interpretation | Separability characterized by rank. |
| Boolean closure | Closure under Boolean terms | Boolean algebra [B4] | Yes | Domain discipline | Design principle | No non-Boolean scalar extension is required. |
| ANF parity/degree | Boolean Moebius inversion | Boolean-function theory [B17] | Yes | Visible CM coefficient signature | Established | Coordinate comparison. |
| Compact spectra | Finite-field matrix theory | Standard algebra | Standard computation | Named-connective atlas | Useful interpretation | Algebraic signatures, not truth observables. |
| Diagonal truth operator | Eigenlogic | 2015/2016 [B10,B11] | Yes | Explicit CM bridge | Established | Associated spectral truth representation. |
| Proposed frame normal form | Boolean orthogonal bases | 2009 [B3] | Close mechanism | Exact CM/LM factorization | Interpretation; priority unclaimed | Structural normal form. |
| Proposed matched-frame product | Matrix kernels/change of frame | Standard linear algebra | Mechanism | Distinct composition contract | Interpretation; priority unclaimed | Matched-frame kernel law. |
| Whole CM/LM package | Combination of preceding ingredients | No exact complete source located | Not established identical | Specific organization | Integrated construction, bounded confidence | Unified calculus, not a new Boolean algebra. |

```{=latex}
\normalsize
\end{landscape}
```

# XV. Mock referee panel

## A. Sympathetic algebraic logician

**Contribution:** a symbolic/numeric Boolean-kernel presentation with compatible polarity frames and pairing. **Strongest result:** unified pairing/coherence semantics, especially after the normal form and selector lemma are added. **Objection:** the draft asserts architectural value more often than it identifies its algebra precisely. **Required revision:** correct polarity indexing, declare all valuation hypotheses, prove n-ary pairing, credit Boolean expansion and earlier matrix logic, shorten spectra. **Recommendation:** major revision for a representation or semantics venue; explanatory integration may be worthwhile without a deep new theorem.

## B. Hostile universal-algebra/Boolean-function expert

**Contribution:** a polarity-orbit embedding into a pointwise Boolean algebra. **Strongest result:** equivariance gives a clean but immediate image description. **Objection:** equation (D) reduces the central mathematics to pullback; no new invariant, obstruction, classification, or non-immediate universal property has been established. **Required revision:** submit as exposition/representation or add a substantive application not forced by the definitions. More category terminology is not a remedy. **Recommendation:** reject as a novelty-driven universal-algebra research article; potentially appropriate elsewhere after reframing.

## C. Matrix-logic/logic-synthesis expert

**Contribution:** frame-aware matrix syntax for Boolean functions plus a symbolic semantic extension. **Strongest result:** precise conditions for legal alignment/fusion; matched-middle-frame composition would also clarify actual matrix product. **Objection:** local truth-table combination and NPN handling have close precedents, while the LM is not used in the timed implementation. **Required revision:** separate semantics from compiler evidence, cite direct precedents, remove unsupported empirical attribution, and use matched-capability baselines. **Recommendation:** a concise foundations/methods note may be useful; performance-based acceptance of the companion requires an actual evidence package.

# XVI. Submission readiness checklist

## Must add or correct before submission

| Blocker | Work required |
|:---|:---|
| Reversal-mask inconsistency | Mathematical correction; regression check. |
| All-true valuation and free-generator scope | Assumption/definition clarification; short counterexample. |
| Theorem types, selectors, input-only frame restriction | Proof/statement revision; one diagram. |
| Three distinct compositions | Mathematical/notation clarification. |
| Historical credit and direct prior art | Literature and claim correction. |
| Versioned, complete references and empirical attribution | Bibliography work or removal of unsupported sentence. |
| Exact novelty claim and companion division of labor | Substantive framing revision. |

## High-value additions

| Addition | Work required |
|:---|:---|
| Frame normal form | Short proof; related-work qualification. |
| Partition selector characterization | Short proof, with finite supplement already checked. |
| Unified n-ary pairing/reconstruction | Proof and theorem reorganization. |
| Rank/separability and minimal XOR-factor count | Proof; one example. |
| Matched-frame product, if in scope | Proof and exact type contract. |
| One running example and one rectangular example | Exposition and small figure. |
| Reproducibility supplement | Code, exact counts, limits, and outputs. |

## Optional additions

An internal clone formulation requires definitions and short proofs. A genuine categorical account requires objects and composable morphisms chosen carefully; include it only if it simplifies the paper. Full compact dynamics, valuation spectra, and phase algebra merit an appendix or another paper. None is a blocker for a clearly delimited foundations note.

## Remove or move elsewhere

Move full spectral/phase investigations, compiler implementation, benchmark protocols, and runtime claims out of the main foundations narrative. Remove duplicated examples and defensive assertions that the work is more than a truth table. Do not restore historical quotient/modulo or physical-collapse claims. These are focus and correctness changes, not objections to the author's notation.

# XVII. Revised abstract

This proposed abstract assumes incorporation of the normal form and selector characterization; it does not attribute those additions to the existing draft.

> We develop a typed Boolean operator calculus connecting numeric correspondence matrices with formula-valued logical matrices. A binary connective $\Theta$ is represented by a true-first matrix $[\Theta]$, evaluated through an XOR--AND contraction over $\mathbb F_2$. Its logical matrix records the four polarity substitutions of the reference operands. We characterize this symbolic representation by an invertible formula-valued frame transformation and show how valuation recovers the corresponding numeric matrix. Logical pairing has the exact agreement-bit semantics $\langle A|[M_{X\Theta Y}]|B\rangle\equiv(A\Leftrightarrow X)\Theta(Y\Leftrightarrow B)$, while basis pairings recover the connective. A partition-of-unity characterization explains why pairing, valuation, the logical-matrix lift, and common input-frame changes preserve pointwise Boolean superposition. We extend the construction to arbitrary-arity truth tensors and rectangular correspondence maps, with explicit block constructions and a rank interpretation of conjunctive separability. The underlying Boolean, matrix, and group-action ingredients are classical; the contribution is their unified symbolic/numeric organization and its precise representation boundaries. No physical measurement interpretation, truth-table compression, or computational speedup is assumed.

# XVIII. Proposed statement of contributions

1. **Typed representation:** numeric Boolean kernels and formula-valued polarity realizations with explicit arity, frame, indexing, and scalar conventions, characterized by a frame normal form and an orbit-image condition.
2. **Complete pairing semantics:** the agreement-bit identity, its n-ary extension, and basis reconstruction, explained by Boolean partition selectors and separated from physical measurement.
3. **Uniform compatibility:** lifting, valuation, pairing, and common signed input transport respect the declared pointwise Boolean operations; the exact limits are included in the statement.
4. **Higher-dimensional structure:** ordered truth tensors and rectangular maps, conditional block construction, and a rank characterization of conjunctive/XOR-separable kernels.

If the matched-frame product is incorporated, include it in the first or third contribution rather than inflating the list. These are contributions of representation and integration; each supporting lemma is not thereby a priority claim.

# XIX. Bottom-line publication assessment

## By community

As **pure mathematics**, current theorem novelty is insufficient for a strong new-results claim. As **algebraic logic**, the structure is coherent but elementary absent a further non-immediate result or semantic application. As **symbolic computation**, the type contracts can support useful methods, but practical benefit needs implementation evidence. As **logic/matrix representation**, the integration and accessible examples have the strongest potential audience. As **operator foundations**, the appropriate subject is Boolean semantics, not physical quantum theory. These are editorial judgments, not promises about a particular journal.

## Red-team and blue-team conclusions

The requested hostile reduction succeeds for the central mathematical substance: truth tables, polarity pullback, pointwise Boolean algebra, ordinary valuation/substitution, and partition selection explain the results. Matrix notation and the word coherence do not defeat that reduction.

What the search did not establish is that one earlier source presents the entire same package. The package may therefore be distinctive as a formal organization. This is not equivalent to finding a new Boolean algebra or a nontrivial theorem not forced by standard structure.

Even granting all the classical ingredients, a useful paper remains possible because the calculus states which operations act on which objects, supplies exact symbolic/numeric translations, and proves when operator combination can precede or follow evaluation. The normal form and selector theorem make that explanation mathematical rather than rhetorical.

The best current category is **sound but mainly expository synthesis**, after correcting the stated issues. **Publishable after major revision** is a plausible goal in an appropriate venue. **Strong standalone research paper after targeted revision** is not yet supported by the evidence.

## Explicit answer to the final question

**Yes: an expert can be shown a genuine CM/LM Boolean operator calculus, rather than only a list of matrix-decorated identities. That does not imply a new underlying algebra.** The structure is a frame-indexed representation of finite Boolean-function algebras by numeric kernels and formula-valued polarity kernels, equipped with homomorphic selectors, valuation, and signed input pullbacks. With matched intermediate frames, ordinary XOR--AND kernel composition has a transported realization too.

The results carrying that formulation are **the frame normal form and faithful image; the selector characterization and complete pairing semantics; the coherence theorem; and, according to scope, matched-frame composition or rank/separability**. What is still missing for a strong novelty-driven research claim is a substantive application, invariant, classification, obstruction, or other result not already forced by the classical structure identified here.

# Appendix A. Independent finite verification

The bundled standard-library Python program imports no manuscript implementation. It uses true-first indexing, exact bits, XOR--AND products, and complete truth masks for formula equivalence. It checks **1,536,530 assertions or finite characterizations**. Counts are not a statistical sample size and include both scalar and whole-matrix comparisons.

| Family | Scope |
|:---|:---|
| Binary selection/valuation/normal form | All sixteen matrices, all four reference valuations. |
| Binary pairing | All sixteen matrices and all sixteen valuations of $A,B,X,Y$. |
| Same-frame superposition | All $16^3$ outer/inner triples and four assignments. |
| Pairing/superposition | All triples and sixteen selector/reference valuations: 65,536 assertions. |
| Independent signed alignment/fusion | Eight frames per operand, all triples and assignments: 1,048,576 assertions. |
| Formula-tensor image | All $16^4=65,536$ four-cell tensors over the two-generator formula algebra; exactly sixteen LMs. |
| Selector characterization | All $16^4$ weight tuples; exactly 256 partitions of unity. Generator conditions checked, full sufficiency proved analytically. |
| Ternary identities | All 256 functions, eight reference valuations, selectors/indices as appropriate. |
| Ternary signed frames | All 48 signed permutations and eight assignments for each function: 98,304 assertions. |
| Ordered rectangular maps | Twelve ordered nonempty bipartitions, all functions/assignments: 24,576 assertions. |
| Four-variable block lift | All binary block functions and outer connectives, all assignments: 65,536 assertions. |
| Matched intermediate frame | All compact matrix pairs and eight reference valuations: 2,048 assertions. |
| Spectral atlas | All sixteen matrices, exact ranks, polynomials, eigenspaces, and powers. |
| Historical examples | Three displayed four-variable matrices, all assignments in their actual partition. |

The incorrect printed intertwiner has **48 failures among 64** function/mask pairs; this is recorded separately from successful checks. Other recorded counterexamples cover the historical page-12 simplification, the historical factorization interpreted as matrix multiplication, and output-negation noncommutation with unchanged XOR.

Run `python verify_cm_lm.py` in the extracted directory. It writes the numeric verification summary and the machine-readable spectral tables included with this report. Python 3.10 or later is sufficient. The execution time is not a compiler benchmark. These checks do not establish arbitrary arity or historical priority; the proofs in the report address arbitrary finite arity.

# Appendix B. Annotated sources and access limits

**[M]** Brian Theory, *Correspondence and Logical Matrices: A Boolean Operator Calculus*, revised foundations draft, 22 September 2026. File Library filename: `CM_LM_Boolean_Operator_Calculus_Coherence_Revised.pdf`. Formal statements and indexed text inspected; no local rendered PDF was substituted.

**[H]** Brian Droncheff, *Correspondence Matrices; Algorithms for Propositional Logic*, supplied historical manuscript, 29 pages. Local text and selected mathematical page images inspected. **[H-public]** public record and text: DOI 10.13140/RG.2.2.28036.37764; record lists May 2018, upload statement 1 October 2018. <https://doi.org/10.13140/RG.2.2.28036.37764>

**[C]** Brian Theory, *Operator-Level Boolean Computation with Correspondence Matrices*, supplied 21-page companion. Mathematical text and selected page images inspected; its source code and benchmark data were not supplied.

**[B1]** William Bricken, *Notes on Matrix Techniques for Logic*, internally dated March 1997, nine-page technical note. Full note and relevant images inspected. Original public-availability date and peer-reviewed status unestablished. <https://wbricken.com/pdfs/01bm/01math/03math-supporting/math-tangential/04matrix-tech.pdf>

**[B2]** Daizhan Cheng, Yin Zhao, Xiangru Xu, *Matrix Approach to Boolean Calculus*, CDC/ECC 2011, pp. 6950--6955. DOI 10.1109/CDC.2011.6160289. Full primary text inspected, particularly Definition 2.7 and Proposition 3.3, Eq. (17). <https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/0224.pdf>

**[B3]** Stan Gudder and Frederic Latremoliere, *Boolean Inner-Product Spaces and Boolean Matrices*, arXiv:0902.1290, 8 February 2009. Full primary text inspected. Default matrix reduction is OR, so application to XOR--AND requires the partition/disjointness distinction. <https://arxiv.org/abs/0902.1290>

**[B4]** Stanley Burris and H. P. Sankappanavar, *A Course in Universal Algebra*, Springer 1981; corrected author-hosted edition 2012. Relevant free Boolean-algebra, Boolean-ring, and Boolean-power sections inspected. <https://www.math.uwaterloo.ca/~snburris/htdocs/UALG/univ-algebra2012.pdf>

**[B5]** Stacks Project, tag 04D4, *G-sets and morphisms*. Primary exposition inspected for coinduction. A living reference, not an original-priority date. <https://stacks.math.columbia.edu/tag/04D4>

**[B6]** Emil L. Post, *The Two-Valued Iterative Systems of Mathematical Logic*, Annals of Mathematics Studies 5, Princeton University Press, 1941. Publisher preview confirms the original year and iterative/substitution framework. Do not confuse later reprint metadata with this year.

**[B7]** C. R. Edwards, *The Logic of Boolean Matrices*, The Computer Journal 15(3):247--253, 1972. DOI 10.1093/comjnl/15.3.247. Publisher record and abstract inspected, not a complete full-text priority search.

**[B8]** August Stern, *Matrix Logic: Theory and Applications*, North-Holland, 1988. Publisher preview inspected; full-book search unavailable. <https://api.pageplace.de/preview/DT0400.9781483295497_A23889179/preview-9781483295497_A23889179.pdf>

**[B9]** Eduardo Mizraji, *Vector Logic: A Natural Algebraic Representation of the Fundamental Logical Gates*, Journal of Logic and Computation 18(1), 2008; advance publication 23 October 2007. DOI 10.1093/logcom/exm057. Full author-supplied article inspected. The earlier *Vector logics*, Fuzzy Sets and Systems 50(2):179--185, 1992, DOI 10.1016/0165-0114(92)90216-Q, was bibliographically checked but not fully accessible.

**[B10]** Zeno Toffano, *Eigenlogic in the Spirit of George Boole*, arXiv:1512.06632, initially 21 December 2015; later version dated 6 February 2018. The spectral construction and later discussion of deliberately avoiding Dirac notation must be cited version-accurately. <https://arxiv.org/abs/1512.06632>

**[B11]** Francois Dubois and Zeno Toffano, *Eigenlogic: A Quantum View for Multiple-Valued and Fuzzy Systems*, arXiv:1607.03509, initially 7 July 2016. Primary preprint. <https://arxiv.org/abs/1607.03509>

**[B12]** Yoemon Sampei, *On the Orthogonal Expansion of the Boolean Polynomial and Its Applications I*, Journal of the Faculty of Science, Hokkaido University, Series I, 11(3):113--125, 1950. DOI 10.14492/hokmj/1530864050. Primary record and relevant material establish an early orthogonal-expansion lead; not a certificate for the exact LM identity.

**[B13]** Virendra Sule, *Generalization of Boole--Shannon Expansion, Consistency of Boolean Equations and Elimination by Orthonormal Expansion*, arXiv:1306.2484, 2013. Primary preprint on orthonormal Boolean expansion. <https://arxiv.org/abs/1306.2484>

**[B14]** Alan Mishchenko, Satrajit Chatterjee, Robert K. Brayton, *DAG-Aware AIG Rewriting: A Fresh Look at Combinational Logic Synthesis*, DAC 2006, 532--536. DOI 10.1145/1146909.1147048. Relevant small-cut/NPN antecedent.

**[B15]** Xuegong Zhou, Lingli Wang, Alan Mishchenko, *Fast Adjustable NPN Classification Using Generalized Symmetries*, ACM TRETS 12(2), article 7, 2019. DOI 10.1145/3313917. Author-hosted primary article inspected. <https://people.eecs.berkeley.edu/~alanmi/publications/2019/trets19_npn.pdf>

**[B16]** Yin Zhao, Xu Gao, Daizhan Cheng, *Semi-tensor product approach to Boolean functions*, undated author-hosted preprint. <https://lsc.amss.ac.cn/~dcheng/preprint/bf01.pdf>. Likely related published article: *Some applications of the matrix expression of Boolean function via semi-tensor product*, 2012, issue 6, 743--749, DOI 10.7523/j.issn.2095-6134.2012.6.004. Publisher record: received 28 June 2011, published 15 November 2012. Full-version equivalence should be checked before substituting references.

**[B17]** Claude Carlet, *Boolean Functions for Cryptography and Error-Correcting Codes*, primary author-hosted chapter, ANF and degree background. <https://www.math.univ-paris13.fr/~carlet/chap-fcts-Bool-corr.pdf>

**Additional spectral leads, not full-text priority certifications:** D. E. Rutherford, *The Eigenvalue Problem for Boolean Matrices*, Proceedings of the Royal Society of Edinburgh A 67(1):25--38, issue year 1965, DOI 10.1017/S0080454100010712; T. S. Blyth, *On Eigenvectors of Boolean Matrices*, 67(3):196--204, 1967, DOI 10.1017/S0080454100008049. Verify scalar conventions before attributing field-spectrum results to them.

# Appendix C. Scope limits

This is not a complete historical-priority certificate. Full access was unavailable for several older works; absence of an exact antecedent in the inspected material does not prove absence from the literature. The main foundations PDF was accessible as indexed content, not a local rendering. The original compiler source and experimental artifacts were not supplied. No physical interpretation or speed advantage was verified.

These limitations do not weaken the explicit counterexamples, reconstructed proofs, or executed finite checks. They limit the strength of the novelty and visual-proofreading conclusions. The appropriate conclusion is a coherent representation calculus whose independent new-theorem significance remains unestablished.
