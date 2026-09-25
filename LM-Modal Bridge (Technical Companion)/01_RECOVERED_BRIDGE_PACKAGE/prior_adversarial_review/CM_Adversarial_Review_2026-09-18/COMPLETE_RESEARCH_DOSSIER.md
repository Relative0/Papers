# From CM rotation to finite-chain-ring contextuality
## Adversarial novelty audit, corrected theorems, and publication architecture

**Review date:** 18 September 2026.  
**Scope:** post-Paper-B theory only.  
**Status:** research assessment with mathematical proofs and reproduced finite checks; not a referee report, formal proof-assistant certification, or exhaustive priority clearance.

## Reading guide and evidence convention

This report answers deliverables A-M. The complete nine-column claim matrix is in `NOVELTY_MATRIX.csv` and `NOVELTY_MATRIX.md`; the annotated references and reproducible query record are in `ANNOTATED_BIBLIOGRAPHY.md` and `SEARCH_LOG.csv`. Reference keys in brackets resolve in the bibliography. All new verification code and its machine-readable outputs are in `checks/`. Fresh rerun results from the supplied audit are in `reproduction/`.

**Source-derived** means the result was already in the supplied corrected audit or its data. **Derived in this review** means an argument or extension developed here, not a claim of established publication priority. **Literature-established** means the mathematical component has a located antecedent, sometimes substantially stronger. A label **candidate** means no equivalent was located in this bounded search; it does not mean that no equivalent exists.

The uploaded ZIP is readable. Its CRC check passed, and all 176 paths listed in the supplied SHA-256 manifest matched. The authoritative baseline was `02_FINAL_AUDIT/CM_Final_Audit`, not an earlier historical ZIP. Its 28-page PDF, TeX, relevant code, tables, and correction ledger were inspected. The archive explicitly says that Paper B, the original CM manuscript, and the earlier phase manuscript were not copied into it. Those documents were located through File Library searches; relevant extracted passages, including Paper B's scope and the original rotation discussion, were consulted. This is **not** a claim that those separate manuscripts were compared byte-for-byte or exhaustively reread. [INPUT; B; CM2018]

# A. Executive research verdict

**A publishable mathematical contribution plausibly survives, but the strongest contribution is not a new circulant algebra, a discovery of Boolean interference, or a derivation of quantum mechanics from logic. It is a classification theorem for a precisely specified family of finite-chain-ring bilinear support models.**

The original 15 candidates do not have equal standing. T1-T6 are classical algebra, short corollaries, or semantic interpretations of classical algebra. T2 is correct and attractive, but its higher-arity content is the standard odd-weight/top-ANF-coefficient criterion. T14-T15 are ordinary rank arguments in the setting of already-known finite-field/modal protocols. T13 admits a stronger statement, but that statement follows from classical permutation-matrix span theory. These should not be advertised as independent major discoveries.

T8-T9 survive as the strongest theorem-level candidates. This review derives a generalization from two-dimensional modules over `F2[u]/(u^4)` to **arbitrary finite commutative chain rings, arbitrary residue fields, and arbitrary bipartite local dimensions**. The result is controlled by two Smith data: the number of nonzero factors and the multiplicity of the least valuation. It gives a uniform Hardy obstruction, identifies when global assignments still exist, and does not rely on exhaustive enumeration. No equivalent classification was located in the inspected modal, ring-contextuality, finite-geometry, coding, or semiring sources. Priority confidence remains provisional.

T11-T12 make a useful consequence: restricted contextuality can distinguish resources that unrestricted field-linear equivalence identifies. The example `(0,2)` versus `(1,1)` is mathematically sound. However, this is a statement about **different allowed measurement theories**, not a paradox or a failure of invariance under legitimate equivalences of one fixed theory.

There is a substantial operational caveat. Declaring every nonzero vector over a ring with zero divisors to be an independently preparable state is not tensor-closed. The supplied audit already recognizes this. Earlier ring-based computation also treats tensor closure and unimodular state spaces explicitly. Thus the safe primary object is an **algebraic support model**, unless a full preparation, measurement-update, and composition contract is supplied. [dB2014]

The recommended paper is therefore:

> **Smith Invariants and Contextuality in Finite-Chain-Ring Support Models**  
> *A rotation-equivariant realization from Boolean correspondence matrices*

This gives the general theorem the title and gives CM its legitimate role: the motivating realization and semantic interpretation. A title beginning with "From Logical Rotation" is defensible for a synthesis article, but weakens the mathematical positioning if it obscures the general classification.

# B. Prior-art and novelty decisions

The full required nine-column matrix is supplied separately, with one row for every T1-T15 and explicit follow-up searches. The classification letters are: A exact known result; B equivalent known result; C direct corollary; D new synthesis/interpretation; E no prior equivalent located; F requires correction or an additional contract.

| Candidate | Assessment | Recommended role |
|---|---|---|
| T1 centralizer and `F2[C4]` | A/B; CM origin is D | Background proposition |
| T2 degree/reversibility | C; binary semantic wording is D | Short secondary corollary, not headline |
| T3 reversal/transpose | A/B algebra; D semantics | Example or semantic proposition |
| T4 complement/socle | C/D | Short proposition with group-algebra credit |
| T5 difference/valuation/rank | A/B | Background; compare sequence linear complexity |
| T6 interferometer | C/D | Diagnostic example |
| T7 induced modal theory | D plus F for an unqualified operational derivation | Definition, motivation, explicit limitations |
| T8 contextuality classification | E candidate, with a broader proof here | Main theorem |
| T9 uniform Hardy family | E candidate as a ring-uniform witness; Hardy logic is known | Main theorem's constructive lemma |
| T10 tensor distinction | A/C; prior operational analysis located | Essential boundary, not novelty headline |
| T11 orbit collapse | C | Secondary corollary |
| T12 equal rank/different restricted contextuality | E/D combination, conditional on T8 | Secondary corollary and motivating example |
| T13 orthogonal basis obstruction | C; stronger all-dimension form available | Appendix or concise boundary theorem |
| T14 teleportation rank criterion | C, with branch invertibility stated | Appendix |
| T15 rank activation | C, with filters/postselection stated | Appendix or omit |

**Priority is not inherited from the age of the CM notation.** A 2018 CM manuscript does not give a 2018 priority date to a theorem first established in a 2026 extension. Later publications can be non-threatening to an earlier precisely documented claim but still precede a later, stronger claim.

# C. Literature review by lineage

## C1. Matrix logic, vector logic, and geometric truth-function symmetries

The matrix representation of logical connectives predates CMs. Edwards treats Boolean matrices; Stern develops matrix logic and its relationship to broader mathematical/physical interpretations; Mizraji represents logical operations by vector and matrix constructions; Eigenlogic uses projectors and eigenvalue semantics; the semi-tensor-product literature supplies logical structure matrices and Boolean-network calculus. These approaches differ in scalar algebra, dimensions, operand encodings, and interpretation. Those differences justify a type ledger, not an unsupported priority claim. [Edwards1972; Stern1988; Stern1992; Mizraji1992; Mizraji2008; Eigenlogic2016; Cheng2011]

Bricken's material is especially relevant to the proposed geometric motivation. His author-hosted symmetry notes discuss two- and three-variable Boolean functions geometrically. An author-hosted extended contents document lists the requested **Notes on Matrix Techniques for Logic**, but the exact nine-page note was not recovered in full during this search. That remains an explicit priority gap, especially for logical-operator geometry; it must not be treated as inspected and ruled out. [BrickenSymmetry; BrickenTOC]

The original CM manuscript explicitly discusses transpose/commutativity and a 90-degree rotation connecting the XOR and equivalence matrices. That supports the historical motivation for the four-position rotation. Paper B supplies the typed operator calculus but already credits matrix logic and ordinary Boolean operations. [CM2018; B]

Thompson's 2023 *Rotational Logic* is an independently convergent comparison for connective rotations. It is not an identified antecedent of the ring-valued contextuality classification. Merely calling it post-2018 does not settle which particular later CM claims it could anticipate. [Thompson2023]

## C2. Circulants, modular group algebras, and finite differences

The lift is the regular representation of a cyclic group algebra. Centralizers of a cyclic shift, polynomial representations, transpose involution, and invertibility via a greatest common divisor are classical circulant theory. MacWilliams's 1971 paper on orthogonal circulants is particularly close to the actual algebra, rather than merely sharing matrix terminology. Norton and Salagean provide the relevant finite-chain-ring coding structure. [MacWilliams1971; NortonSalagean2000]

In characteristic two, `x^(2^n)-1=(x+1)^(2^n)`. Nilpotence, the ideal chain, and rank loss follow immediately. The interpretation as rotational finite differences is useful, but the filtration is not an independent discovery of a new algebraic structure. For cyclic binary sequences, the same polynomial valuation controls linear complexity; Games-Chan is the relevant algorithmic lineage. [GamesChan1983]

The terminal all-ones element is also the norm/socle element of a modular group algebra. In a finite `p`-group algebra over `Fp`, the augmentation ideal is the radical; the sum of all group elements spans the socle. Boolean complementation adds precisely such an all-ones coefficient vector. The bridge is elegant, but algebraically immediate. [Benson2023]

## C3. Boolean degree and Reed-Muller theory

The coefficient of the full monomial in ANF equals truth-table parity. Therefore the unit criterion detects **maximum algebraic degree**, not general nonlinearity in higher arity. The fact that non-affineness and maximum degree coincide for two inputs is the source of the memorable binary slogan. [Carlet2010]

The more extensive derivative/degree correspondence belongs naturally to the elementary abelian translation algebra, not the cyclic chain algebra. Berman's characterization and Charpin's generalization identify Reed-Muller codes with radical powers in modular group algebras. Andriatahiny states the relevant Berman-Charpin theorem explicitly. Thus a proposed paper whose main contribution is discovering the Reed-Muller/radical correspondence would not survive prior-art review. [Berman1967; Charpin1988; Andriatahiny2016]

## C4. Modal and logic-derived process theories

Schumacher-Westmoreland already give field-valued modal states, reversible linear transformations, dual-basis measurements, interference, Bell/Hardy phenomena, and teleportation. James-Ortiz-Sabry connect finite-field quantum computation to typed reversible relational programming with exclusive disjunction. Accordingly, neither "Boolean interference" nor the broad idea of obtaining a quantum-like formalism from logical/programming structures is new. [SW2012; JOS2011]

The semiring/ring literature is closer than a field-only comparison suggests. de Beaudrap explicitly distinguishes distributions from tensor-closed state spaces and uses unimodularity as a generic ring-state condition. Gogioso constructs broader semiring-based process models and carefully distinguishes parity-valued weights from Boolean possibility. These works preclude claiming that ring-valued modal computation or its composition problems were previously unexamined. [dB2014; Gogioso2017]

A subtle comparison is necessary: a theory may be "local" with generalized signed or field-valued weights while its zero/nonzero support is possibilistically nonlocal. Such statements use different meanings of hidden-variable representation. Gogioso's observations do not refute the support theorem below; nor does that theorem refute the semiring result.

## C5. Phases, contextuality, and finite-ring geometry

Coecke-Edwards-Spekkens place phase groups at the center of comparisons between qubit and toy subtheories. Their `C4` versus `C2 x C2` comparison is particularly close in vocabulary. The group generated by a coefficient rotation is not automatically their phase group: a distinguished observable and the relevant phase-preservation condition must first be specified. [CES2011]

Abramsky-Brandenburger distinguish ordinary, logical, and strong contextuality in a support-based framework. Abramsky-Hardy supply the logical-inequality perspective; Hardy's original argument and Mermin's configurations supply standard contradiction patterns. The new claim cannot be the logical structure of a Hardy contradiction itself. Goldstein also gives an early higher-dimensional reduction to a two-term entangled sector, so that proof strategy by itself is not new. [AB2011; AH2012; Hardy1993; Goldstein1994; Mermin1990]

Saniga-Planat-Minarovjech connect finite quotient-ring projective geometry to Mermin configurations. Their ring labels organize commutation/context geometry; that is not the same construction as putting chain-ring entries into a bipartite amplitude matrix and classifying nonzero bilinear outcomes by Smith factors. Cortez-Morales-Reyes give a more recent and serious ring-contextuality comparison via partial rings of symmetric matrices. Again, the objects and hidden-variable contracts differ. No exact T8-T9 equivalent was identified in these sources. [SPM2006; CMR2022]

## C6. Codes, Bell bases, and characteristic-two forms

Quantum codes constructed from chain-ring codes do not by themselves define quantum mechanics with chain-ring amplitudes. Liu-Liu use coding constructions and Gray images to obtain quantum codes; their result is relevant to a possible application, but not an equivalent modal support model. [LiuLiu2017]

Werner's correspondence between tight teleportation, dense coding, maximally entangled bases, and unitary operator bases takes place in ordinary Hilbert-space quantum theory. Its hypotheses cannot be copied unchanged to characteristic two. Concentration results likewise provide context, not a probability interpretation for a Boolean filter. [Werner2001; BBPS1996]

Transpose preservation of the dot product is not the same as preserving a nonsingular quadratic form in characteristic two. Domokos-Frenkel explicitly warn about that distinction. The stronger span obstruction below reduces to the constant-row/column-sum space whose permutation-matrix basis was established over arbitrary rings by Lueneburg. [DomokosFrenkel2004; Lueneburg1988]

# D. Corrected and generalized formal theorem set

## D0. Types, frames, and notation

Use `C_f` for the original 2 x 2 CM, `a_f` for its four coefficients in cyclic order, `R` for the 4 x 4 rotation, `Lambda(a_f)` for its lifted operator, and `A=F2[R]` for the operator algebra. A block matrix in `M_m(A)` is not an original CM.

For a true-first CM, fix the cyclic truth-position order

\[
(1,1),(1,0),(0,0),(0,1).
\]

Then the index reflection `j -> -j mod 4` exchanges arguments. Other cyclic starting points can require conjugating the reflection; the semantic assertion is not independent of indexing.

The abstract coefficient-ring tensor `A^m tensor_A A^n` and the independent-register tensor `F2^(4m) tensor_F2 F2^(4n)` are different objects. Even their binary dimensions differ: `4mn` versus `16mn`.

## D1. Classical rotation algebra and semantic corollaries (T1-T5)

**Proposition 1.** Let `R e_j=e_(j+1 mod N)` on `F2^N`. Its centralizer is `F2[R]`, naturally isomorphic to `F2[x]/(x^N-1)`.

*Proof.* A commuting matrix is determined by its first column `v`: its j-th column must be `R^j v`. Conversely every such circulant commutes with `R`. The matrices `I,R,...,R^(N-1)` are independent by their action on `e_0`, and the only defining relation is `R^N=I`. For `N=4` there are 16 elements. This is a standard cyclic-vector/regular-representation argument.

**Proposition 2.** For `N=2^n`, set `u=I+R`. Then

\[
A_N\cong\mathbb F_2[u]/(u^N),\qquad
\operatorname{rank}_{\mathbb F_2}(u^\nu v)=N-\nu
\]

for a unit `v` and `0 <= nu <= N`, with the convention `u^N=0`. Its units are exactly coefficient vectors of odd parity.

*Proof.* Frobenius gives `(1+x)^N=1+x^N`. In the quotient, an element is invertible exactly when its constant coefficient in the u-basis is one. That coefficient is its x-polynomial evaluated at one. Multiplication by `u^nu` in the basis `1,u,...,u^(N-1)` shifts basis vectors by `nu` and has rank `N-nu`.

For `N=4`, `u^4=0`, `u^3=I+R+R^2+R^3`, and the ideal chain is

\[
0\subset(u^3)\subset(u^2)\subset(u)\subset A.
\]

There are eight units. In this small algebra every unit is transpose-orthogonal: it is either a rotation matrix or its complement, and the all-ones matrix has square zero. The full unit group has type `C4 x C2`; the native rotation subgroup is only its `C4` subgroup. Do not identify these two groups.

**Corollary 3: maximum-degree criterion (T2).** For any ordering of the `2^n` inputs of a Boolean function `f`, its cyclic-convolution lift is invertible exactly when

\[
\bigoplus_x f(x)=1
\quad\Longleftrightarrow\quad
[x_1\cdots x_n]f=1
\quad\Longleftrightarrow\quad
\deg f=n.
\]

*Proof.* Sum the ANF over all assignments. A monomial of degree less than n occurs an even number of times; the full monomial occurs once. Apply Proposition 2.

For two inputs, this is equivalent to non-affineness. For three or more inputs it is not equivalent to nonlinearity: `f(x1,x2,x3)=x1 x2` is nonlinear but its eight-position lift is singular. The criterion is independent of the selected cyclic truth ordering. This substantially weakens the assertion that the unit test reveals a property specific to CM geometry.

**Corollary 4: reversal and complement (T3-T4).** For `K e_j=e_(-j)`,

\[
KRK=R^{-1},\qquad K\Lambda(a)K=\Lambda(a^\vee)=\Lambda(a)^T.
\]

In the declared CM order, `a^vee` is the truth vector of `f(y,x)`. Also

\[
\Lambda(1+f)=\Lambda(f)+u^3.
\]

More generally, for length `N=2^n`, complement adds `u^(N-1)`, the all-ones group-algebra element. This is translation by a socle element, **not multiplication by it**. Reversal is transpose, **not generally inversion of every lifted operator**; for the eight units at length four these happen to coincide, but that coincidence should not be exported to arbitrary length.

## D2. Rotational differences are not the entire degree filtration

**Proposition 5: two different filtrations.** Under binary indexing of coefficients, write

\[
\sum_j a_j(1+u)^j=\sum_k b_k u^k,
\qquad b_k=\bigoplus_{j\supseteq k}a_j.
\]

The cyclic valuation is the least **numeric index** k for which `b_k=1`. For the translation algebra

\[
B_n=\mathbb F_2[C_2^n]
  \cong\mathbb F_2[u_1,\ldots,u_n]/(u_1^2,\ldots,u_n^2),
\]

with radical `J=(u1,...,un)`, the radical order of the corresponding truth coefficient vector is the least **Hamming weight** of such an index. For nonzero f this is `n-deg f`, and

\[
\Phi(\mathrm{RM}(r,n))=J^{n-r}.
\]

*Proof of the last identity.* An ANF monomial supported on S has group-algebra coefficient polynomial

\[
\prod_{i\in S}(1+u_i)\prod_{i\notin S}u_i.
\]

Its lowest homogeneous degree is `n-|S|`, with leading monomial indexed by the complement of S. Distinct highest-degree ANF monomials have distinct leading terms, so they cannot cancel. This proves the degree/order formula, hence the code identity. The identity is the classical Berman-Charpin connection, not a new theorem claimed here. [Berman1967; Charpin1988; Andriatahiny2016]

For `C4`, the vectors `(1,1,0,0)` and `(1,0,1,0)` both represent affine functions in the declared cyclic CM order, but correspond to `u` and `u^2`. Thus there cannot be a single exact identification of the whole cyclic valuation hierarchy with Boolean degree.

The cyclic hierarchy instead agrees with the usual polynomial description of periodic-sequence linear complexity:

\[
L(a)=N-\deg\gcd(a(x),x^N-1)=N-\nu_{x+1}(a).
\]

This is a useful translation into established terminology. [GamesChan1983]

## D3. Interference and the equivariance restriction (T6-T7)

**Proposition 6.** Let `W=[[I,0],[I,I]]` and `D_k=diag(I,R^k)`. Then `W^2=I` and

\[
WD_kW\binom v0=\binom v{v+R^k v}.
\]

*Proof.* Direct block multiplication. `k=0` cancels the second branch. For `k != 0`, a basis vector distinguishes a nontrivial rotation from the identity. This is phase-sensitive XOR cancellation in an explicitly declared sense, not a Born-rule interferometer.

**Proposition 7: principled gates, additional measurement assumptions.** On `V^m`,

\[
\operatorname{End}_{C_4}(V^m)=M_m(A),
\qquad
\operatorname{Aut}_{C_4}(V^m)=GL_m(A).
\]

*Proof.* A block matrix commutes with `I_m tensor R` exactly when each block commutes with R. Apply Proposition 1.

Consequently the maximal reversible **rotation-equivariant** gate family is well motivated. However, this proposition does not select the state normalization, support map, tensor product, block coarse-graining, or measurement-update rule. Those are additional definitions. The word "derived" is justified for the commutant, not for the entire operational theory.

## D4. Main theorem: contextuality over finite chain rings (T8 generalized)

Let S be a finite commutative chain ring, with maximal ideal `(pi)`, nilpotency length `s`, and residue field `k=F_q`. Let `m,n >= 1`. A row is **primitive** if at least one coordinate is a unit. Projective rows are primitive rows modulo multiplication by a unit.

A local measurement is an unordered projective basis obtained from a reversible matrix in `GL_m(S)` or `GL_n(S)`. Each basis is a distinct measurement setting; outcomes are its rows. We do **not** silently impose an additional single-effect Kochen-Specker identification between different bases.

For `M in M_(m,n)(S)`, define support by

\[
\mathcal E_M(B,C)=\{(i,j):r_i M t_j^T\ne0\}.
\]

A **global assignment** chooses one outcome in each local measurement so that all cross-party pairs are supported. Strong contextuality means no such assignment. Logical contextuality means at least one supported event cannot be extended. Relational locality means every supported event extends; since the scenario is finite, the union of all global assignments then reproduces its support.

Nonzero M gives a nonempty support in every context. The support also satisfies possibilistic no-signalling: a fixed r has some possible partner in a basis precisely when the row `rM` is nonzero, independently of that partner basis.

**Lemma 8: residue-hyperplane criterion.** The support model of M has a global assignment if and only if there are residue-field hyperplanes `H_A subset k^m` and `H_B subset k^n` such that

\[
rMt^T\ne0
\]

for every primitive lift r of a residue vector outside `H_A` and every primitive lift t of a residue vector outside `H_B`.

*Proof.* Suppose a global assignment exists. Let `U_A` be the union of the projective rays it selects at least once, over all Alice settings. The complementary rays cannot contain a reversible basis. Their residue vectors therefore span a proper subspace: otherwise a residue basis could be selected among them and lifted to a reversible basis, using the standard local-ring invertibility criterion. Place that proper subspace inside a hyperplane `H_A`. Every lift of every residue ray outside `H_A` lies in `U_A`. The same holds for Bob. Each pair of such rays is selected in some pair of settings and hence must have nonzero bilinear value. Conversely, every reversible basis contains a row whose reduction lies outside a given hyperplane. Choose such a row in each setting on both sides. The stipulated cross-pair condition makes all choices compatible. QED.

This lemma uses locality of the coefficient ring, not the principal-ideal condition. It is therefore a promising tool for a later non-chain-ring analysis.

**Theorem 9: complete chain-ring classification.** Put M in Smith form with exponents

\[
0\le a_1\le\cdots\le a_\ell\le s,
\qquad \ell=\min(m,n),\qquad \pi^s=0.
\]

For nonzero M let `r` be the number of nonzero Smith factors (`a_i<s`) and let `h` be the multiplicity of the least exponent `a_1`. Then

\[
\begin{array}{rcl}
r=1 &\Longrightarrow& \text{relationally local},\\
r\ge2,\ h=1 &\Longrightarrow& \text{logically contextual but not strongly contextual},\\
h\ge2 &\Longrightarrow& \text{strongly contextual}.
\end{array}
\]

The zero matrix gives the empty model and is excluded as a state. Here r is a **Smith support count**, not an unspecified ring rank: determinantal rank and other rank conventions over rings need not agree.

*Proof: invariance.* Left/right multiplication by reversible matrices permutes the complete measurement families. Thus the contextuality type depends only on Smith form.

*Proof: r=1.* Write `M=diag(p,0,...)`, p nonzero. Take any supported seed event `(r,t)`, so `p r_1 t_1 != 0`. Keep its selected outcomes in those two settings. In every other setting choose a row with first coordinate a unit, which is always possible in a reversible basis. Cross-pairs between two new choices are nonzero multiples of p; cross-pairs involving one seed outcome are also nonzero because `p r_1` and `p t_1` are nonzero. Thus every supported event extends.

*Proof: h=1 allows a global assignment.* Write

\[
M=\pi^{a_1}\operatorname{diag}(1,\pi^{a_2-a_1},\ldots).
\]

In every local basis choose a row with first coordinate a unit. For any pair of chosen rows, the bracketed bilinear value is a unit plus radical terms and is therefore a unit. Multiplication by `pi^(a_1)` is nonzero. This gives a global assignment.

*Proof: h>=2 precludes a global assignment.* Suppose hyperplanes from Lemma 8 exist, and write `M=pi^a M_0` with the residue matrix `bar(M_0)` of rank h. Let `H_B=ker beta`. The residue vectors outside `H_A` span `k^m`. Since `bar(M_0)` has rank at least two, some x outside `H_A` has `w=x bar(M_0)` not in the line spanned by beta. Choose y in `ker w` but outside `ker beta`; this is possible because the two hyperplanes differ. Lift x to r and y to an initial t. The row `r M_0` is primitive, while `r M_0 t^T` lies in the maximal ideal. Adjust a coordinate of t corresponding to a unit entry of `rM_0` by a radical element to make that dot product exactly zero, without changing its residue. The resulting r,t are both outside the forced hyperplanes but satisfy `rMt^T=0`, contradicting Lemma 8.

*Proof: r>=2 implies logical contextuality.* Apply the uniform Hardy construction below to the first two nonzero Smith coordinates and extend each basis by standard basis rows. All forced events stay within those two coordinates, so extra outcomes do not provide an escape. This completes the classification. QED.

For `S=F2[u]/(u^4)` and `m=n=2`, this is exactly T8: equal finite exponents are strong; unequal finite exponents are logical-not-strong; one finite exponent is local; `(4,4)` is empty. The proof also covers `Z/4`, `Z/8`, `Z/9`, and other mixed-characteristic chain rings, not only polynomial quotients.

**Corollary 10: measurement counts.** The number of projective primitive rows in `S^m` is

\[
q^{(s-1)(m-1)}\frac{q^m-1}{q-1}.
\]

The number of unordered projective reversible bases is

\[
\frac{|GL_m(S)|}{|S^\times|^m m!},
\qquad |GL_m(S)|=q^{m^2(s-1)}|GL_m(q)|.
\]

For m=2 this is `q^(2s-1)(q+1)/2`; at q=2,s=4 it is 192. Counting all nonzero rows as projective points would be wrong: nonprimitive rows do not belong to reversible bases.

## D5. Uniform Hardy family (T9 generalized)

**Lemma 11.** Let `p=pi^a`, `q_0=pi^b`, `0<=a<=b<s`, and `c=pi^(b-a)`, so `pc=q_0 !=0`. Define

\[
F=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
X=\begin{pmatrix}1&0\\1&1\end{pmatrix},\quad
C_c=\begin{pmatrix}1&0\\-c&1\end{pmatrix}.
\]

These matrices are reversible over any such S. Give Alice settings F and `C_c`, and Bob settings F and X. For `D=diag(p,q_0)`, the four amplitude matrices are

\[
FDF^T=\begin{pmatrix}q_0&0\\0&p\end{pmatrix},\quad
FDX^T=\begin{pmatrix}0&q_0\\p&p\end{pmatrix},
\]
\[
C_cDX^T=\begin{pmatrix}p&p\\-q_0&0\end{pmatrix},\quad
C_cDF^T=\begin{pmatrix}0&p\\q_0&-q_0\end{pmatrix}.
\]

Their row-major support strings are respectively `1001`, `0111`, `1110`, `0111`.

The possible event `(F_A=0,F_B=0)` forces `X_B=1`, which forces `C_A=0`, which forces `F_B=1`, a contradiction. Hence that event has no global extension. When `a<b`, c is nilpotent and Theorem 9 supplies a global assignment elsewhere, distinguishing logical from strong contextuality.

The construction works in every residue characteristic; the minus sign is essential outside characteristic two. It uses **two settings per party and three basis templates**, not a growing search over the entire ring. The Hardy implication pattern is classical; the candidate contribution is this valuation-uniform implementation and its role in the complete classification.

## D6. Shared tensors, literal tensors, and orbit collapse (T10-T12)

**Proposition 12.** In `A tensor_A A ~= A`, `u^3 tensor_A u=0`, although both factors are nonzero. In `A tensor_F2 A`, their tensor is nonzero.

*Proof.* The balanced tensor product identifies `a tensor b` with `ab` when both modules are the regular A-module. Over a field, nonzero simple tensors are nonzero, for example by applying dual functionals nonzero on their factors.

Thus arbitrary nonzero A-vectors cannot all be independently preparable under the balanced tensor product. Restricting preparations to unimodular vectors repairs that specific defect: their coefficient ideals are the unit ideal, and so is that of their tensor. But the nonzero support measurement rule can still produce a nonunimodular conditional state. For example, `diag(1,u)` is unimodular as a bipartite coefficient vector, whereas Alice's second standard outcome leaves Bob with `(0,u)`. A complete sequential theory needs a rule for such branches; division by u is not an invertible normalization operation. The classification theorem itself does not assume such a rule. [dB2014]

**Proposition 13.** Embed `M in M_2(A)` into an 8 x 8 binary matrix by the regular representation. Its binary rank is

\[
(4-a)+(4-b)=8-a-b
\]

on Smith type `(a,b)`, using zero for exponent four. Under unrestricted left/right `GL_8(F2)` action, rank is a complete invariant. Under `GL_2(A)` action the Smith pair remains invariant.

In particular `(0,2)` and `(1,1)` both have binary rank six but have different restricted support contextuality: logical-not-strong versus strong. This is a direct corollary of Theorem 9 plus ordinary matrix equivalence.

**Preparation qualification and a stronger example.** If initial shared-ring preparations are restricted to unimodular coefficient vectors, `(1,1)` is excluded. The original rank-six pair therefore does not survive that particular preparation restriction. The general theorem supplies a replacement in dimension three: over the same A, the unimodular resources `diag(1,1,u^3)` and `diag(1,u,u^2)` both have binary rank nine, but are respectively strong and logical-not-strong. Thus the restricted/unrestricted distinction can survive unimodular initial preparations, although this does not solve conditioning closure. This example is derived in this review and checked separately in `checks/additional_boundaries.json`.

**Important source correction, not an optional qualification.** The supplied audit establishes that its particular restricted shared and literal bipartite support models are isomorphic after a Bob-side transpose-involution relabeling. Shared block amplitudes use `sum E_i M_ij F_j`; literal Choi block amplitudes use `sum E_i M_ij F_j^T`. Transpose is the automorphism `R -> R^-1` of A and permutes the 192 projective bases. Consequently these two specific restricted models have the same contextuality classification. Tensor theories differ in general, but these tables do not establish a difference between their restricted contextuality classes. [INPUT, audit section 7.4]

## D7. Stronger transpose-orthogonal span obstruction (T13)

**Proposition 14.** For every `n>=2`, not only even n,

\[
\operatorname{span}_{\mathbb F_2}\{U:U^TU=I\}
 =\{M:M\mathbf1=c\mathbf1,\ \mathbf1^TM=c\mathbf1^T
       \text{ for some }c\in\mathbb F_2\},
\]

and this space has dimension `(n-1)^2+1`. Hence transpose-orthogonal matrices cannot form a basis of `M_n(F2)`.

*Proof.* Each column of U has odd weight, so `1^T U=1^T`; since `U^T=U^(-1)`, this also gives `U1=1`. Every linear combination therefore lies in the stated constant-sum space. Conversely all permutation matrices are transpose-orthogonal. Differences of two permutations that agree except on two rows and columns produce the elementary four-corner rectangles. The rectangles involving a fixed final row and column span the `(n-1)^2`-dimensional zero-row/column-sum space. Adjoining I adds the common-sum direction. This proves equality and the dimension formula. The permutation-span ingredient is classical over arbitrary rings. [Lueneburg1988]

At n=8 the relevant span dimension is 50, not merely bounded by 63. The original even-dimensional parity argument was correct but substantially weaker. This is an elementary boundary theorem, not a new claim to have solved the general Bell-basis problem.

## D8. Alternative forms: a useful obstruction to the proposed repair

R itself preserves the nondegenerate alternating form with matrix `J=R^2`, and the quadratic form

\[
Q(x)=x_0x_2+x_1x_3.
\]

All R-invariant alternating forms on `F2^4` have matrices

\[
b(R+R^3)+cR^2,
\]

and are nondegenerate exactly when c=1. Thus an R-compatible symplectic structure exists. The group preserving J is `Sp_4(F2)`, of order 720; the group preserving Q is the split quadratic group `O_4^+(F2)`, of order 72. These orders were also checked by exhausting the 65,536 binary 4 x 4 matrices. All eight coefficient-ring units preserve J, whereas only the four native rotations preserve Q. The dot-product group `U^T U=I`, the symplectic group, and the quadratic isometry group must not be conflated.

**Proposition 15.** For nonidentity R, the above W and `D=diag(I,R)` do not preserve any common nondegenerate bilinear form on the same doubled space.

*Proof.* Write a candidate form matrix in blocks `B=[[A,C],[E,F]]`. The equation `W^TBW=B` gives `F=0` and `E=C`, so `B=[[A,C],[C,0]]`. Nondegeneracy forces C to be invertible: a nonzero vector in `ker C` would give a null vector of B. But `D^TBD=B` requires `CR=C`, hence R=I, a contradiction.

This rules out simply renaming the existing gate family "symplectic." The obstruction concerns W and D together, even though R alone preserves a symplectic form. A standard doubled representation `G -> diag(G,G^(-T))` preserves a canonical alternating form, but changes the model and does not automatically reproduce its support measurements.

Hermitian forms over `F_(2^(2m))`, with involution `z -> z^(2^m)`, provide another legitimate direction. They change the scalar field and state theory, admit isotropic phenomena, and do not supply real nonnegative probabilities. Classical symplectic actions on Pauli labels should not be confused with linear actions on state amplitudes. [DomokosFrenkel2004; Gogioso2017]

## D9. Literal teleportation and activation (T14-T15)

**Proposition 16.** For literal finite-field coefficient matrices, an outcome branch with reshaped effect matrix `R_m` has transfer matrix `T_m=M^T R_m^T`, up to the declared vectorization convention. If `R_m` is invertible, then `rank(T_m)=rank(M)`. An exact universal linear correction `C_m T_m=I_d` exists exactly when M has full rank.

*Proof.* Right multiplication by an invertible matrix preserves rank. A square transfer map has a left inverse exactly when it is invertible.

A complete measurement basis need not consist of effects whose reshaped matrices are all invertible. Thus "complete measurement" alone is insufficient for the displayed rank equality. A Bell-type analyzer must separately verify branch invertibility and completeness. The supplied literal construction does so; the ring-valued four-outcome analyzer is not the same analyzer. [INPUT; SW2012; Werner2001]

**Proposition 17.** For any field and a rank-r matrix M, `rank(M^(tensor k))=r^k`. There exist unrestricted local rectangular filters extracting `I_d` from that tensor power exactly when `r^k>=d`.

*Proof.* Put M into rank normal form by invertible left/right matrices and tensor those changes of basis. Select d of the `r^k` nonzero coordinate directions; conversely no multiplication by filters can increase rank.

This is an exact algebraic extraction criterion, not a claim of deterministic distillation, a success probability, or a laboratory protocol. The balanced ring tensor can annihilate copies instead, so this result cannot be exported there. In the literal d=8 example, rank six permits two-copy extraction, but a rank-one resource never activates to d>1. [BBPS1996 for the broader concentration lineage]

# E. Proof audit and computational reproducibility

## E1. What has and has not been proved

The algebraic claims T1-T6 are proved by short exact arguments above. T7 is a construction choice, not a theorem that a complete physical or operational theory follows from a CM. T8-T9 have an analytic proof in this report, extending the supplied length-four classification. T10-T12 follow from balanced tensor products, Smith form, and ordinary rank equivalence. T13 is strengthened and proved. T14 requires invertible branch matrices; T15 requires unrestricted linear filters. None of these proofs has been translated into Lean, Isabelle, or another proof assistant.

The computational results certify only the stated finite searches and implementations. Repeating an existing test is not an independent proof. The separate extension checker uses a fresh arithmetic implementation and a different SCC-based 2-SAT procedure; nevertheless, higher-dimensional checks use the proved hyperplane lemma and are therefore not logically independent tests of that lemma.

The claims that fail without qualification are: "nonlinearity iff reversible" beyond two inputs; "cyclic filtration equals the Reed-Muller hierarchy"; "all nonzero ring states are closed under independent preparation"; "any complete measurement has invertible reshaped branches"; "shared and literal restricted bipartite contextuality tables differ"; and "one can repair the existing interferometer merely by choosing a symplectic form."

## E2. Rerunning the supplied audit

A fresh copy of the authoritative audit was run without changing its mathematical implementation. The final independent run exited successfully in 33.04 seconds and the historical run in 44.14 seconds. There were **31 independent tests and 59 historical tests**, for 90 passing tests total. The historical split was 22, 10, 15, and 12 tests. Earlier interrupted aggregate logs in the source archive were not mistaken for final successful evidence.

The local environment was Python 3.13.5 on Linux x86-64, NumPy 2.3.5, SciPy 1.17.0, SymPy 1.14.0, and pytest 9.0.2. Wall-clock timings are descriptive and are not performance benchmarks. These runs verify the archived corrected baseline, not the novelty of that baseline.

| Exhaustive family | Search space and algorithm | Reproduced outcome |
|---|---|---|
| Four-cycle centralizer | All `2^16=65,536` binary 4 x 4 matrices; exact commutation | 16 commuting matrices |
| Ring units | All 16 ring elements; exact multiplication/inversion | 8 units |
| Block gate inventory | All `16^4=65,536` elements of `M_2(A)`; exact binary rank and ring tests | 24,576 reversible; 512 with transpose-orthogonal binary expansion; 128 monomial-unit matrices |
| Projective measurement family | Primitive rows modulo units, then unordered reversible pairs | 24 projective rows, 192 bases; only 4 bases arise from the archived orthogonal restriction |
| Smith resource inventory | All 65,536 matrices; independent valuation/rank profiles | 15 Smith types; 5,265 nonzero simple shared tensors and 60,270 nonseparable resources |
| Complete restricted contextuality | `192^2=36,864` contexts per Smith type, both model conventions; forbidden-event 2-SAT implication closure | 4 strong types, 6 logical-not-strong, 4 local, 1 empty |
| Contextuality by resource count | Expand class inventory using verified Smith types | 26,214 strong; 34,056 logical-not-strong; 5,265 local; 1 zero |
| Direct shared/literal comparison | 8,640 explicitly contracted canonical effect pairs, plus full restricted tables | Isomorphic support models after Bob-side involution relabeling |
| Modal Bell test | Three settings per party; all `2^6=64` deterministic assignments | No global assignment |
| Specified GHZ test | 27 contexts, 112 possible events; all `2^9=512` assignments | No global assignment; a six-context contradiction in that family |
| GHZ minimum within this family | All subsets of 1-5 of the 27 contexts: 101,583 subsets | No smaller contradiction within the searched family; not a universal GHZ minimum |
| Literal teleportation | 256 inputs including zero, 64 branches: 16,384 direct tests | 16,320 nonzero-input branches transfer correctly; 64 zero-input regression cases |
| All resource/branch ranks | `65,536 x 64=4,194,304` branch comparisons | Rank criterion holds for the chosen complete invertible-branch analyzer |
| Restricted spaces and quotients | 983,040 fixed-space and 983,040 quotient checks | Reproduced model-specific hierarchy; not interchangeable with unrestricted rank |
| Probability extension | Linear program over 36 event probabilities plus exact affine constraints | Maximum common positive lower bound is 0; six modal-possible events are forced to probability 0 |

The 192-basis SAT problem has 384 binary measurement-choice variables. Its implicit assignment space has size `2^384`; the audit does **not** enumerate that astronomical set. An impossible joint outcome gives two implications, and transitive implication closure tests consistency and event extendability. Search-space cardinality must not be confused with the number of assignments actually iterated.

The GHZ negative result for the original four familiar contexts is retained in the source audit: absence of a contradiction there was not silently replaced by the successful larger-family result. Bell/GHZ claims should identify their exact state, effect family, coarse-graining, and tensor convention.

## E3. Fresh extension checks produced in this review

`checks/independent_extensions.py` does not import the supplied audit. It implements finite polynomial rings, modular rings, projective rays, residue hyperplanes, direct supports, and iterative Kosaraju SCC solving.

It ran 22 ring/dimension campaigns: binary polynomial chain rings through length five; ternary and quaternary polynomial cases; `F5`; `Z/4`, `Z/8`, `Z/16`, `Z/9`, `Z/27`; square local dimensions three and four in selected rings; and one 2 x 3 case. Every Smith type in each listed campaign was checked against the hyperplane criterion. For all square dimension-two campaigns having at most 192 bases, an independent full-basis 2-SAT test also checked global-assignment existence. The uniform Hardy matrices were checked directly for each relevant exponent pair.

The checker additionally exhausts **65,812 Boolean functions** in one through four variables, verifying parity, top degree, cyclic rank, cyclic valuation, and the translation-algebra degree/radical identity. It exhausts every binary matrix through dimension four for the strengthened orthogonal span, finding span dimensions 1, 2, 5, and 10. The common W/D invariant-bilinear-form space has dimension 17; its universal degeneracy follows from the block proof, not a random sample of forms.

The main new campaign finished successfully in approximately 3.52 seconds in this environment. A separate `additional_boundaries.py` run verified the symplectic/quadratic group counts and the two unimodular rank-nine examples; its timing is recorded separately. Its JSON files record per-case cardinalities and timings. These tests support the proofs; finite data alone do not establish the arbitrary-ring theorem.

## E4. Probability and physical limitations

A no-signalling **possibility** table need not admit a normalized, nonnegative, no-signalling probability table with exactly the same support. The archived Bell table has six possible events that every such probability solution assigns zero. This is the already-known modal obstruction, independently reproduced, not a missing choice of Born-rule formula. Allowing a smaller probability support is a different requirement. [SWNoncontext2010]

The paper must distinguish modal possibility from probability, algebraic nonseparability from physical entanglement, XOR cancellation from complex amplitudes, linear transfer from physical teleportation, and finite-field reversibility from unitarity. A simulator that centrally computes the table is not a Bell experiment with independently controlled distant devices.

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

# J. Generalization roadmap and future-paper map

## J1. Higher arity: what generalizes and what does not

The unit/parity/top-degree equivalence extends to every cyclic action of order `2^n`, and more generally to a regular action of a finite 2-group of that order. The augmentation ideal of its modular group algebra is nilpotent, so a coefficient element is a unit exactly when its augmentation is one. This remains true for nonabelian 2-groups, although left and right regular commutants then involve opposite algebras. It remains a classical augmentation argument, not a comprehensive nonlinearity detector. [Benson2023]

There is a naturality obstruction to extending the *geometric* four-cycle. For `n>=3`, no element of `AGL(n,2)` has order `2^n`. To see this, embed an affine transformation into `GL_(n+1)(2)` by homogeneous coordinates. A 2-power-order element is unipotent, with order at most `2^ceil(log2(n+1))`, strictly smaller than `2^n`. Hypercube automorphisms are affine, so a Hamiltonian Gray-code successor on all `2^n` assignments is not a native hypercube automorphism in these dimensions. An arbitrary truth-table cycle is possible, but it imports an extra ordering choice.

Natural coordinate translations yield `C2^n` and a multivariable radical, with Boolean derivatives and Reed-Muller structure. This is likely the cleaner higher-arity mathematical language, but the chain-ring classification no longer automatically applies: the radical is not principal for n>1. The next substantive theorem would concern contextuality over these non-chain local algebras, not merely restate their known code interpretation.

## J2. Alternative symmetry groups

For cyclic length not a power of two, `x^N-1` has multiple factors; the algebra can split into primary components. Parity alone no longer characterizes units. Multiple commuting rotations give tensor products of truncated polynomial algebras, usually with a multidimensional ideal lattice. Dihedral 2-groups preserve the augmentation unit criterion but introduce noncommutativity. Full affine equivariance may be too restrictive: a 2-transitive permutation action has a two-dimensional commuting algebra, because there are only diagonal and off-diagonal pair orbits. Thus "more symmetry" can shrink, rather than enrich, the available equivariant gates.

For each alternative, specify whether the algebra is generated by the symmetry operators or is their commutant; these coincide in the cyclic regular example but not in general. This distinction is another place where a direct extrapolation from C4 can fail.

## J3. Next research questions that could produce new mathematics

The hyperplane criterion suggests an extension to nonprincipal local rings, including `F2[u1,...,un]/(ui^2)`. Determine which bilinear maps satisfy the forced-pair condition and whether an invariant of the associated graded module replaces the least Smith valuation. Establish minimum measurement families realizing each obstruction, rather than minimizing only within a prespecified finite list. Analyze which measurement restrictions destroy logical versus strong contextuality, and classify product-ring support models, where componentwise zeros combine differently.

For operational closure, choose among a fully literal finite-field model, a preparation-compatible unimodular ring model with an explicit conditioning rule, or a typed theory containing quotient-module states. Each changes the question. A quotient-module construction should be proved associative and closed under composition before being called a process theory.

For alternative unitarity, redesign the gates and measurement effects together. R alone is compatible with a symplectic structure; W and the controlled rotation are not simultaneously compatible on the same space. A viable extension must prove its forms, gate closure, complete measurement structure, and contextuality anew.

## J4. Recommended paper split

**One main paper now:** the general chain-ring contextuality theorem, its CM realization, and the restriction/tensor boundaries. This avoids turning 15 observations into 15 nominal contributions.

**A later process-theory paper:** only after independent preparation, conditioning, and tensor closure are established. The symplectic/Hermitian redesign could belong here if it produces a coherent new model.

**A later higher-arity paper:** only after a new result beyond Berman-Charpin, for example a contextuality classification in multivariable augmentation algebras or a genuinely useful synthesis algorithm. A paper consisting only of the degree/parity equivalence and known Reed-Muller correspondence would be weak.

**A separate compilation paper:** retain Paper B's scope. New empirical comparisons should be against matched truth-table/cut-based synthesis methods and include conversion, compilation, and memory costs. They should not be used as evidence of contextuality novelty.

Do not plan five papers merely because five themes are available. Two or three papers with distinct theorem sets are more defensible than fragmenting elementary corollaries.

# K. Applications assessment

| Area | Demonstrated substance | What is not established | Appropriate next test |
|---|---|---|---|
| Formal verification | Small exact arithmetic, independently checkable witnesses, full finite inventories | Formal proof-assistant certification | Encode the hyperplane lemma and chain-ring theorem in a proof assistant |
| Quantum foundations | Controlled separation of support nonlocality, scalar algebra, tensor choice, and gate restrictions | A physical model, Born rule, or laboratory advantage | Formulate a closed operational contract and compare support-preserving embeddings |
| Education | Compact cancellation, Hardy tables, rank and tensor counterexamples | That physical phenomena follow from Boolean arithmetic | Use side-by-side field/ring/Hilbert-space examples with explicit assumptions |
| Coding theory | Established chain-ring and Reed-Muller connections; cyclic rank equals sequence linear complexity | New code parameters, distances, decoders, or quantum code construction | Find a new invariant/algorithm before claiming an application |
| Cellular automata | Lifted operators are linear cyclic convolutions; units give reversible periodic dynamics | A new cellular-automaton classification | Compare exact rules, boundary conditions, and known polynomial criteria |
| Reversible computation | Explicit reversible coefficient-register maps and gate-count inventories | Reversible evaluation of a many-to-one Boolean function without ancillas | Specify input/output encoding, garbage, ancillas, and synthesis cost |
| Cryptography | ANF/weight/difference interpretations suggest diagnostic comparisons | Security advantage, useful S-box, or better diffusion | Measure standard nonlinearity, differential, linear, algebraic, and branch-number criteria |
| Logic synthesis | Paper B provides the relevant operator-folding question | New speedup from the rotation/modal construction | Matched implementation benchmarks outside this paper |
| Hardware | Finite XOR/AND networks can implement the arithmetic | Quantum hardware, energy advantage, optical realization, or asymptotic advantage | Gate/area/depth estimates and an ordinary classical implementation baseline |

The cryptographic caveat is particularly sharp. A balanced Boolean function on n>=2 inputs has even truth-table weight, so its cyclic lift is singular. Every nonzero linear component of an n-bit permutation S-box is balanced. Thus this scalar unit criterion rejects many cryptographically standard component functions; it is not a security quality score. The usual degree bound for bent functions also makes their lifts singular when n>=4. These are consequences of established Boolean-function properties, not a new attack or construction. [Carlet2010]

# L. Bibliography and access limitations

The full annotated bibliography is supplied separately. Each entry gives identifiers where located, the exact reason for relevance, and an access note where necessary. The essential priority gaps are the full Bricken nine-page note, a deeper original-language/group-code backward search around Berman and Charpin, and specialist review of finite-ring contextuality and invariant theory. No subscription MathSciNet, zbMATH, Scopus, or Web of Science search is claimed.

Exact full-text comparison matters especially for a "logic-derived" origin story. Broad overlap in Stern and Bricken is already enough to reject a sweeping first-of-its-kind claim, but partial access is not enough to decide every narrowly formulated semantic bridge. That uncertainty is local to those priority claims; it does not prevent the algebraic proofs in this report.

# M. Search protocol and record

`SEARCH_LOG.csv` records the actual query strings, the web-search route, close hits, and why those hits were equivalent, adjacent, or irrelevant. Primary arXiv manuscripts, author-hosted papers, and publisher pages were preferred. Backward tracing included Berman/Charpin from Andriatahiny, Richman from Domokos-Frenkel, and the broader modal/semiring references from de Beaudrap and Gogioso. Later comparison searches included 2023 rotational logic and recent ring-contextuality work.

A negative exact-phrase result is weak evidence. Searches for "Hardy" and "nilpotent" often retrieve Hardy uncertainty theorems on Lie groups, not logical contextuality. Searches for "quantum rings" often retrieve physical ring-shaped systems. Those were excluded rather than counted as literature coverage. "Valuation algebra" in information-combination theory was also not treated as synonymous with a pi-adic chain-ring valuation.

The priority conclusion is deliberately asymmetric: classical components can be confidently credited once an equivalent source is found, but failure to locate the complete classification justifies only candidate novelty. A pre-submission update and specialist referee-level check should target the abstract theorem, not the term "Correspondence Matrix."

# Final synthesis: what is genuinely distinctive?

The broad thesis does not survive unchanged. The operator algebra is classical; the Boolean degree bridge is an elementary augmentation/parity consequence; quantum-like phenomena over Boolean or finite-field structures have substantial antecedents; and the shared all-nonzero state proposal is not independently preparation-closed.

A narrower and mathematically stronger thesis does survive:

> A CM truth-position rotation supplies a concrete representation-theoretic route to a classical finite chain ring and its maximal rotation-equivariant local maps. Within an explicitly declared bilinear possibility model, the Smith filtration controls the transition from locality to logical contextuality to strong contextuality. This classification extends beyond CMs, beyond the binary residue field, beyond length four, and beyond two-dimensional local modules. Forgetting the coefficient-ring structure can erase distinctions that remain visible to the restricted measurement theory.

The strongest distinctive research object is therefore **the Smith-stratified bilinear support model, with its residue-hyperplane criterion and uniform Hardy witnesses**. The CM origin is a meaningful motivating realization and semantic bridge, not the sole source of its mathematical content. Framed this way, the work has a plausible publishable core. Framed as a new circulant algebra or a derivation of physical quantum mechanics from Boolean logic, it does not.


---

# Supplement 1: complete novelty matrix

# Prior-art and novelty matrix

All T1-T15; review date 18 September 2026. A=known exactly; B=known equivalently; C=direct corollary; D=synthesis; E=no equivalent located; F=requires correction/contract. Candidate labels are not priority guarantees. Reference keys resolve in ANNOTATED_BIBLIOGRAPHY.md.

| Claim | Exact formal statement | Closest prior work | Earliest located source | Equivalent / stronger / weaker? | What remains distinctive | Novelty confidence | Publication recommendation | Additional searches still needed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1. Four-cycle centralizer | Cent(R)=F2[R] ~= F2[x]/(x^4-1) ~= F2[u]/u^4; u=I+R; 16 elements. | Classical cyclic-vector/regular representation and circulant polynomial theory [MacWilliams1971]. | MacWilliams 1971 is a close explicit located source; centralizer theory is older, earliest origin not established. | A/B: equivalent classical algebra; general cyclic centralizer theorem is stronger. | CM truth-position geometry motivates a realization; it does not change the algebra. | Known; CM interpretation: New synthesis | Background | Retrieve older circulant and cyclic-centralizer references; inspect Bricken exact matrix note for the semantic origin. |
| T2. Degree and reversibility | For N=2^n and any truth ordering, Lambda_N(f) is invertible iff XOR_x f(x)=1 iff top ANF coefficient=1 iff deg(f)=n. For n=2 only, equivalent to non-affineness. | Augmentation unit criterion; Boolean parity/top ANF identity; periodic cyclic convolution [MacWilliams1971; Carlet2010; GamesChan1983]. | MacWilliams 1971 and Games-Chan 1983 for close algebraic/sequence components; exact earliest Boolean bridge not established. | C: direct corollary; higher-arity nonlinearity slogan is false, maximum-degree version true. | A compact binary semantic bridge; no equivalent explicit CM wording located. | New synthesis, not a strong theorem-novelty candidate | Secondary theorem (short corollary) | Check older Boolean-function/circulant cellular-automaton literature for the exact combined sentence; distinguish maximum degree from nonlinearity. |
| T3. Operand and phase reversal | With cyclic CM order (11,10,00,01), K e_j=e_-j gives K Lambda(a) K=Lambda(a^vee)=Lambda(a)^T, and a^vee represents f(y,x). | Circulant transpose/dihedral reflection; Boolean symmetry and NPN lineage [MacWilliams1971; BrickenSymmetry; CM2018]. | Classical circulant involution, explicitly close MacWilliams 1971; Boolean symmetry notes 1997; earliest general reflection identity not established. | A/B algebra plus D interpretation; indexing condition is essential. | Semantic interpretation of the standard reflection in an explicitly declared logical frame. | New synthesis | Background or example | Full Bricken matrix note; older logic-rotation and NPN treatments. Do not conflate transpose with inverse for general lifts. |
| T4. Complement and socle | For N=2^n, Lambda_N(1+f)=Lambda_N(f)+(1+R)^(N-1); at N=4 this is translation by u^3. | Norm element/socle of modular p-group algebras; pointwise complement [Benson2023 and its older references]. | Classical modular group-algebra theory; Benson 2023 is a modern explicit treatment, not earliest priority. | C/D: immediate identification of two standard all-ones elements. | A clean semantic statement connecting complement to the terminal filtration element. | New synthesis | Secondary proposition or example | Backward trace through Jennings-era modular group-algebra sources; check prior complement/socle terminology. Do not call the translation multiplication. |
| T5. Rotational-difference filtration | In A_N=F2[u]/u^N, u^N=0, rank(u^k)=N-k; every nonzero a=u^nu v with v a unit has rank N-nu. Cyclic valuation is not the full Boolean degree filtration. | Chain rings, augmentation ideals, repeated-root cyclic codes, periodic sequence linear complexity [NortonSalagean2000; GamesChan1983]. | Games-Chan 1983 is a close algorithmic antecedent; algebraic filtration is classical and older. | A/B: equivalent or direct consequence. | Rotational-information interpretation and comparison of numeric-index versus Hamming-degree filtrations. | Known | Background | Older finite-difference/cyclic-code references; explicitly credit Berman-Charpin for the different C2^n radical/Reed-Muller filtration. |
| T6. Boolean rotation interferometer | W=[[I,0],[I,I]], D_k=diag(I,R^k); W^2=I and W D_k W(v,0)=(v,v+R^k v). | Linear reversible circuits and finite-field/modal interference [SW2012; JOS2011; Gogioso2017]. | Modal preprints 2010; James-Ortiz-Sabry 2011 is especially close to Boolean/logic-derived cancellation. | C/D: elementary block identity; interference phenomenon has prior formulations. | A compact rotation-sensitive implementation inside the chosen CM-induced commutant. | New synthesis | Example | Check earlier modal interferometer and reversible XOR circuit realizations; specify operational meaning of phase. |
| T7. Restricted modal subtheory | End_C4((F2^4)^m)=M_m(A), Aut_C4=GL_m(A). The nonzero support rule, preparations, tensor and conditioning are additional choices. | Modal quantum theory; logic-derived reversible relational programming; ring/semiring process theories; phase-group subtheories [SW2012; JOS2011; dB2014; Gogioso2017; CES2011]. | Stern 1988/1992 for broad logic-physics motivation; SW 2010 and JOS 2011 for direct modal/programming antecedents. | D synthesis; F for claiming full operational theory is forced by geometry. | Maximal rotation-equivariant gate family has a precise representation-theoretic motivation. | New synthesis | Definition / motivation, not main theorem | Full Bricken/Stern access for narrow origin claims; prove state preparation, conditioning and composition closure before calling it a complete process theory. |
| T8. Complete contextuality classification | For finite commutative chain ring S, arbitrary m,n, Smith support count r and least-valuation multiplicity h: r=1 local; r>=2,h=1 logical-not-strong; h>=2 strong; zero empty. Uses all unordered projective GL bases and r_i M t_j^T !=0. | Support hierarchy [AB2011]; modal nonlocality [SWNoncontext2010]; finite-ring projective geometry [SPM2006]; partial-ring contextuality [CMR2022]. | No equivalent complete classification located. Hardy 1993, modal 2010, and sheaf 2011 are antecedents to components, not this exact theorem. | E candidate. The review proves a stronger arbitrary-chain-ring/arbitrary-dimension statement than the supplied length-four theorem. | Smith filtration determines contextuality type; residue-hyperplane criterion and analytic proof replace enumeration. | High candidate, provisional priority | Main theorem | Specialist search of finite-local-ring bilinear support models, matroid basis selection, ring-valued modal nonlocality; MathSciNet/zbMATH and full backward/forward citation audit still needed. |
| T9. Uniform Hardy family | For p=pi^a, q0=pi^b=pc !=0, use F=[[0,1],[1,0]], X=[[1,0],[1,1]], C=[[1,0],[-c,1]]. Four supports FF=1001, FX=0111, CX=1110, CF=0111 give a nonextendable event over every finite chain ring. | Hardy logical pattern; Goldstein higher-dimensional reduction; modal Hardy arguments [Hardy1993; Goldstein1994; SWNoncontext2010; AH2012]. | Hardy 1993 and Goldstein 1994 for the implication/projection strategy; no ring-uniform valuation template located. | E candidate for uniform implementation; underlying Hardy contradiction is exactly known. | Two settings per party, three templates, all residue characteristics and nonzero Smith pairs. | High candidate as part of T8, not a separate broad Hardy discovery | Main theorem constructive lemma | Search nilpotent/valuation-parametrized nonlocality; consult modal foundations specialists; compare generalized ring Hardy constructions and effect restrictions. |
| T10. Shared versus literal tensors | u^3 tensor_A u=0 in A tensor_A A, but u^3 tensor_F2 u!=0. All nonzero ring vectors are not independent-preparation closed; the particular archived restricted bipartite tables are nevertheless isomorphic by Bob transpose involution. | Balanced tensor products; explicit ring-state closure/unimodularity [dB2014]; semiring process semantics [Gogioso2017]. | Abstract tensor fact classical; de Beaudrap 2014 explicitly treats relevant operational closure. | A/C: fact and broad warning known; proposed claim of previously unanalyzed composition is not sustained. | Typed diagnosis of this particular construction, including equal restricted tables despite inequivalent ambient tensor models. | Known | Essential limitations section | Analyze conditioning of nonunimodular branches and quotient-module processes; do not advertise a restricted contextuality-table difference disproved by the audit. |
| T11. Restricted orbit collapse | GL2(A) x GL2(A) preserves Smith pair (a,b); full GL8(F2) x GL8(F2) preserves only binary rank 8-a-b. | Smith form and ordinary rank equivalence; restricted-operation resource theory. | Classical normal-form theory; earliest exact resource-language formulation not established. | C: direct consequence of forgetting A-linearity. | Concrete demonstration of what information the restricted coefficient structure retains. | Known | Secondary corollary | Compare resource theories under restricted local operations; characterize which subgroup normalizes the allowed measurement family. |
| T12. Same field rank, different restricted contextuality | D_(0,2) and D_(1,1) both expand to binary rank 6 but are respectively logical-not-strong and strong for the fixed complete A-linear measurement family. Under unimodular initial preparation the rank-six strong example is excluded; diag(1,1,u^3) versus diag(1,u,u^2) gives a replacement in dimension three, both binary rank 9. | T8 plus rank normal form; measurement-relative contextuality [AB2011; CES2011]. | No exact example located; components are classical or modal antecedents. | E/D combination, conditional on the fixed model contract and T8; not an unrestricted contextuality invariant. | A transparent example of distinct Smith/contextuality strata collapsing under field-linear equivalence. The higher-dimensional replacement survives unimodular initial preparation, though conditioning closure remains unresolved. | Moderate candidate | Secondary theorem / motivating example | Check subtheory-resource orbit examples; explicitly track changes of allowed measurements under enlarged local transformations. |
| T13. Orthogonal operator-basis obstruction | For every n>=2, span_F2{U:U^T U=I}={M:M1=c1 and 1^T M=c1^T}, dimension (n-1)^2+1<n^2. Stronger than the even-n parity hyperplane bound. | Binary bilinear orthogonal group; classical permutation-matrix span [Lueneburg1988]; characteristic-two form distinctions [DomokosFrenkel2004]. | Lueneburg 1988 is an explicit stronger span ingredient and calls part of it folklore; first-ever source not established. | C: original is weaker than an elementary consequence of known span theory. | Useful warning that transpose-orthogonality is too restrictive; explicit n=8 span dimension 50. | Not novel as a main theorem | Appendix | Older permutation-span/Birkhoff module literature; exact finite-field error-basis statements. Distinguish bilinear from quadratic orthogonal groups. |
| T14. Teleportation rank criterion | For invertible reshaped branch R_m, T_m=M^T R_m^T has rank(M). A universal exact square linear correction exists iff M is full rank. Completeness alone does not ensure branch invertibility. | Elementary rank invariance; generalized teleportation and modal protocols [Werner2001; SW2012]. | Werner 2001 (preprint 2000) for architecture; ordinary rank theorem much older. | C: routine linear algebra, with a necessary branch condition. | Correct typed placement of the supplied literal analyzer and resource boundary. | Not novel | Appendix | Check finite-field complete invertible-matrix effect bases if claimed; distinguish algebraic correction from probability and physical teleportation. |
| T15. Multi-copy rank activation | For field matrices rank(M^tensor k)=rank(M)^k; unrestricted rectangular local filters can extract I_d iff r^k>=d. This is conditional algebraic extraction, not deterministic physical distillation. | Rank of Kronecker products; entanglement concentration/SLOCC [BBPS1996]. | Classical matrix rank; Bennett et al. 1996 (preprint 1995) for physical concentration lineage. | C: direct normal-form argument. | Clarifies why literal field resources and balanced-ring resources may have different activation behavior. | Not novel | Appendix or omit | Study restricted A-linear filters or nonfree-module resource activation only if seeking a genuinely new theorem. |


---

# Supplement 2: annotated bibliography

# Annotated bibliography and source-access record

Review date: 18 September 2026. Keys match the main report. Identifiers refer to the named source, except where an access note explicitly gives a citing source. An earliest located reference is not automatically the first-ever publication. Primary papers, author-hosted materials and publisher records were used; no subscription-index search is claimed.

## [INPUT]

Correctness Audit of Boolean CM Modal Models. User-supplied corrected audit package, 18 September 2026. No independent publication status or author attribution is asserted.

Source: ../Astra_CM_Novelty_Research_Package_2026-09-18(1).zip

**Why it matters:** Authoritative source baseline: model definitions, correction ledger, code, finite inventories, protocol tests.

**Access / priority qualification:** ZIP fully readable; all 176 manifest-listed hashes matched. The 28-page audit PDF, TeX, relevant code/data and four rendered contact sheets were inspected. Historical snapshots are evidence of earlier stages, not the final specification.

## [B]

Brian Theory. Operator-Level Boolean Computation with Correspondence Matrices. Unpublished manuscript supplied in File Library, located in its 17 September 2026 upload.

Source: File Library: operator-level-boolean-computation-with-correspondence-matrices.pdf

**Why it matters:** Defines the hard exclusion boundary: operator/frame/fusion/LM calculus is background, not a contribution of this paper.

**Access / priority qualification:** Relevant extracted passages and bibliography were read through File Library. The separate full binary was not in the uploaded ZIP and was not exhaustively reread or byte-compared.

## [CM2018]

Brian Droncheff. Correspondence Matrices; Algorithms for Propositional Logic. ResearchGate preprint, version 1.0.1, May 2018. DOI: 10.13140/RG.2.2.28036.37764.

Source: https://doi.org/10.13140/RG.2.2.28036.37764

**Why it matters:** Original discussion of CM rotations and transpose/commutativity; establishes the motivation, not priority for the 2026 extensions.

**Access / priority qualification:** Original manuscript excerpts located in File Library; dating and identifier cross-referenced against Paper B bibliography. No claim that a 2026 theorem appeared in this 2018 manuscript.

## [Edwards1972]

C. R. Edwards. The Logic of Boolean Matrices. The Computer Journal 15(3), 247-253 (1972). DOI: 10.1093/comjnl/15.3.247.

Source: https://doi.org/10.1093/comjnl/15.3.247

**Why it matters:** Antecedent to matrix-based manipulation of Boolean functions.

**Access / priority qualification:** Bibliographic record and Paper B reference consulted; not an exhaustive rereading of the original article.

## [Stern1988]

August Stern. Matrix Logic: Theory and Applications. North-Holland, 1988. DOI: 10.1016/C2009-0-14445-8.

Source: https://doi.org/10.1016/C2009-0-14445-8

**Why it matters:** Longstanding operator/matrix logic lineage; defeats broad claims that logical connectives as operators are unprecedented.

**Access / priority qualification:** Publisher/book metadata and available previews, not a full-book audit.

## [Stern1992]

August Stern. Matrix Logic and Mind: A Probe into a Unified Theory of Mind and Matter. North-Holland, 1992. ISBN 978-0-444-88798-6.

Source: https://www.sciencedirect.com/book/9780444887986/matrix-logic-and-mind

**Why it matters:** Important comparison for broad claims connecting matrix logic with quantum or physical interpretation.

**Access / priority qualification:** Publisher preview, including introductory material, inspected; full chapters were not available. This leaves narrow priority claims unresolved.

## [BrickenSymmetry]

William Bricken. Symmetry in Boolean Functions with Examples for Two and Three Variables. Author notes, March 1997; accompanying figures dated April 2002.

Source: https://www.wbricken.com/pdfs/01bm/01math/03math-supporting/math-tangential/03symmetry%26figures.pdf

**Why it matters:** Geometric symmetries of Boolean functions are close antecedents to the origin narrative.

**Access / priority qualification:** Author-hosted document consulted; the dates of text and figures should not be collapsed into one publication date.

## [BrickenTOC]

William Bricken. Extended Table of Contents. Author bibliography/index, 21 April 2005. Lists Notes on Matrix Techniques for Logic, nine pages.

Source: https://wbricken.com/pdfs/10map/02etoc.050421.pdf

**Why it matters:** Confirms existence of the exact matrix-logic note requested by the user.

**Access / priority qualification:** Index inspected. The exact nine-page note, described as 1997 in the research seed, was not recovered in full. Do not state that it was read and excluded as equivalent.

## [Mizraji1992]

Eduardo Mizraji. Vector logics: The matrix-vector representation of logical calculus. Fuzzy Sets and Systems 50(2), 179-185 (1992). DOI: 10.1016/0165-0114(92)90216-Q.

Source: https://doi.org/10.1016/0165-0114(92)90216-Q

**Why it matters:** Vector truth values and matrix representations of logical operations predate CMs.

**Access / priority qualification:** Primary publication metadata and the later vector-logic treatment consulted.

## [Mizraji2008]

Eduardo Mizraji. Vector Logic: A Natural Algebraic Representation of the Fundamental Logical Gates. Journal of Logic and Computation 18(1), 97-121 (2008); online 23 October 2007. DOI: 10.1093/logcom/exm057.

Source: https://doi.org/10.1093/logcom/exm057

**Why it matters:** Explicit matrix-operator account of monadic and dyadic logic; scalar and dimension differences must be stated rather than assumed to confer novelty.

**Access / priority qualification:** Author-posted primary PDF text and publication metadata consulted. PDF production header says 97..122; the published citation gives 97-121.

## [MizrajiRoot2021]

Eduardo Mizraji. Generalized "Square roots of Not" matrices, their application to the unveiling of hidden logical operators and to the definition of fully matrix circular Euler functions. arXiv:2107.06067, first submitted 22 June 2021; version 5, 10 June 2024.

Source: https://arxiv.org/abs/2107.06067

**Why it matters:** Adjacent comparison for roots of logical negation and quantum-like matrix operations; not the chain-ring contextuality theorem.

**Access / priority qualification:** Primary arXiv abstract and version history inspected. Uses complex matrices of arbitrary dimension, not the characteristic-two chain-ring support model. Full 25-page paper was not audited.

## [Eigenlogic2016]

Francois Dubois and Zeno Toffano. Eigenlogic: a Quantum View for Multiple-Valued and Fuzzy Systems. arXiv:1607.03509 (2016).

Source: https://arxiv.org/abs/1607.03509

**Why it matters:** Projector/eigenvalue approach to logical operators and a quantum-inspired interpretation.

**Access / priority qualification:** Primary arXiv material consulted; not identified with XOR/AND circulant convolution.

## [Cheng2011]

Daizhan Cheng, Hongsheng Qi, and Zhiqiang Li. Matrix Expression of Logic. In Analysis and Control of Boolean Networks, pp. 55-65. Springer, 2011. DOI: 10.1007/978-0-85729-097-7_3.

Source: https://doi.org/10.1007/978-0-85729-097-7_3

**Why it matters:** STP and logical structure matrices provide established matrix-logic context.

**Access / priority qualification:** Publisher chapter and available text consulted; the chapter is not a claim of priority for the ring-support theorem.

## [ChengBoolean2011]

Daizhan Cheng, Yin Zhao, and Xiangru Xu. Matrix approach to Boolean calculus. Proceedings of the 50th IEEE Conference on Decision and Control and European Control Conference, pp. 6950-6955 (2011). DOI: 10.1109/CDC.2011.6160289.

Source: https://doi.org/10.1109/CDC.2011.6160289

**Why it matters:** Explicit Boolean matrix operations with XOR addition and AND multiplication; already acknowledged in Paper B.

**Access / priority qualification:** Metadata and Paper B attribution consulted; no new-paper contribution is assigned to this basic scalar calculus.

## [Thompson2023]

Declan Thompson. Rotational Logic. Author article, 11 March 2023.

Source: https://declanthompson.github.io/blog/blogic/rotational/

**Why it matters:** Independently convergent later example of geometric rotations of truth-function representations.

**Access / priority qualification:** Author article inspected. It does not establish the ring-valued contextuality classification. A post-2018 date alone does not make it irrelevant to a new 2026 claim.

## [MacWilliams1971]

F. J. MacWilliams. Orthogonal Circulant Matrices over Finite Fields, and How to Find Them. Journal of Combinatorial Theory, Series A 10, 1-17 (1971). DOI: 10.1016/0097-3165(71)90062-8.

Source: https://doi.org/10.1016/0097-3165(71)90062-8

**Why it matters:** Close classical source for the circulant polynomial representation, transpose involution and unit/orthogonality criteria.

**Access / priority qualification:** Publisher metadata and indexed primary PDF text consulted. An attempted CORE-hosted full-PDF retrieval failed; do not call this an exhaustive full-paper reread.

## [NortonSalagean2000]

Graham H. Norton and Ana Salagean. On the Structure of Linear and Cyclic Codes over a Finite Chain Ring. Applicable Algebra in Engineering, Communication and Computing 10, 489-506 (2000). DOI: 10.1007/PL00012382.

Source: https://doi.org/10.1007/PL00012382

**Why it matters:** Finite-chain-ring structure and coding-theoretic setting of the valuation hierarchy.

**Access / priority qualification:** Publisher and institutional repository records/text consulted; not a contextuality classification.

## [GamesChan1983]

Richard A. Games and Agnes Hui Chan. A fast algorithm for determining the complexity of a binary sequence with period 2^n (Corresp.). IEEE Transactions on Information Theory 29(1), 144-146 (1983). DOI: 10.1109/TIT.1983.1056619.

Source: https://ieeexplore.ieee.org/document/1056619

**Why it matters:** The cyclic polynomial valuation/rank has a standard periodic-sequence linear-complexity interpretation.

**Access / priority qualification:** IEEE record and primary indexed material consulted. This is an algorithmic antecedent, not a claim that every CM semantic phrase occurs in it.

## [Benson2023]

David J. Benson. The socle of the group algebra of a finite p-group. arXiv:2303.09940 (2023).

Source: https://arxiv.org/abs/2303.09940

**Why it matters:** Modern primary exposition of the classical augmentation-radical and group-norm socle facts, with backward references.

**Access / priority qualification:** ArXiv primary text consulted. It is an exposition of older theory, not the earliest priority source for those facts.

## [Carlet2010]

Claude Carlet. Boolean Functions for Cryptography and Error-Correcting Codes. In Yves Crama and Peter L. Hammer (eds.), Boolean Models and Methods in Mathematics, Computer Science, and Engineering, pp. 257-397. Cambridge University Press, 2010. DOI: 10.1017/CBO9780511780448.011.

Source: https://doi.org/10.1017/CBO9780511780448.011

**Why it matters:** ANF, weight parity, Boolean derivatives, degree, balancedness and bent-function comparisons.

**Access / priority qualification:** Author chapter text and publisher metadata consulted. Print year is 2010; Cambridge online publication date is 5 June 2013. Do not mistake the latter for the origin of these facts.

## [Berman1967]

S. D. Berman. On the theory of group codes. Cybernetics and Systems Analysis 3, 25-31 (1967). DOI: 10.1007/BF01072842.

Source: https://doi.org/10.1007/BF01072842

**Why it matters:** Earliest located source in the Reed-Muller/group-algebra radical-power lineage.

**Access / priority qualification:** Publisher record verified; the exact theorem was checked through Andriatahiny and its attribution. Original-language full-text audit remains a follow-up.

## [Charpin1988]

Pascale Charpin. Une generalisation de la construction de Berman des codes de Reed et Muller p-aires. Communications in Algebra 16, 2231-2246 (1988).

Source: https://arxiv.org/abs/1601.07633

**Why it matters:** Generalization in the Berman-Charpin lineage; essential credit for the radical/Reed-Muller correspondence.

**Access / priority qualification:** Bibliographic entry traced through Andriatahiny; the linked source is that accessible citing paper, not Charpin itself. Original article and DOI were not independently recovered.

## [Andriatahiny2016]

Harinaivo Andriatahiny. The Generalized Reed-Muller codes and the radical powers of a modular algebra. arXiv:1601.07633, first submitted 28 January 2016.

Source: https://arxiv.org/abs/1601.07633

**Why it matters:** Theorem 3.6 explicitly states the Berman-Charpin radical-power characterization and distinguishes the non-prime-field case.

**Access / priority qualification:** Full primary manuscript inspected. A date inside a later served PDF is not used to replace the arXiv submission history.

## [SW2012]

Benjamin Schumacher and Michael D. Westmoreland. Modal Quantum Theory. Foundations of Physics 42, 918-925 (2012). DOI: 10.1007/s10701-012-9650-z. arXiv:1010.2929 (2010).

Source: https://arxiv.org/abs/1010.2929

**Why it matters:** Core antecedent for field-valued modal states, dual-basis measurements, reversible maps, interference and quantum-information analogues.

**Access / priority qualification:** Primary manuscript read and journal metadata independently verified. Field theory is not automatically a zero-divisor-ring process theory.

## [SWNoncontext2010]

Benjamin Schumacher and Michael D. Westmoreland. Non-contextuality and free will in modal quantum theory. arXiv:1010.5452 (2010).

Source: https://arxiv.org/abs/1010.5452

**Why it matters:** Modal Bell/noncontextuality arguments and failure of a strictly positive no-signalling probability extension of the full support.

**Access / priority qualification:** Full primary manuscript and relevant table screenshot inspected. The reproduced probability obstruction is not new.

## [JOS2011]

Roshan P. James, Gerardo Ortiz, and Amr Sabry. Quantum Computing over Finite Fields: Reversible Relational Programming with Exclusive Disjunctions. arXiv:1101.3764 (2011).

Source: https://arxiv.org/abs/1101.3764

**Why it matters:** Especially close prior art for a logic/programming-derived Boolean finite-field quantum-like theory.

**Access / priority qualification:** Full primary manuscript consulted. Defeats a broad first logic-to-modal origin claim; does not supply the exact chain-ring Smith classification located here.

## [dB2014]

Niel de Beaudrap. On computation with probabilities modulo k. arXiv:1405.7381, version 2 (2014). Version 1 was titled On the power of modal quantum computation.

Source: https://arxiv.org/abs/1405.7381

**Why it matters:** Ring/semiring computation; explicitly addresses tensor-closed state spaces and generic unimodular states.

**Access / priority qualification:** Full primary HTML text consulted, especially the state-space closure definition and generic-state/unimodularity discussion. This is operational prior art for T10, not just abstract tensor algebra.

## [Gogioso2017]

Stefano Gogioso. Fantastic Quantum Theories and Where to Find Them. arXiv:1703.10576 (2017).

Source: https://arxiv.org/abs/1703.10576

**Why it matters:** Semiring/involution process constructions, parity and finite-field examples, phase groups, and generalized non-determinism.

**Access / priority qualification:** Full primary manuscript, including section 7, inspected. Its generalized-weight locality must not be confused with Boolean support locality.

## [CES2011]

Bob Coecke, Bill Edwards, and Robert W. Spekkens. Phase groups and the origin of non-locality for qubits. Electronic Notes in Theoretical Computer Science 270(2), 15-36 (2011). DOI: 10.1016/j.entcs.2011.01.021. arXiv:1003.5005 (2010).

Source: https://arxiv.org/abs/1003.5005

**Why it matters:** Phase groups and restricted subtheories, including C4 versus C2 x C2.

**Access / priority qualification:** Full primary manuscript consulted. A cyclic coefficient shift is not automatically a categorical phase without the required observable structure.

## [Spekkens2007]

Robert W. Spekkens. In defense of the epistemic view of quantum states: a toy theory. Physical Review A 75, 032110 (2007). DOI: 10.1103/PhysRevA.75.032110. arXiv:quant-ph/0401052.

Source: https://arxiv.org/abs/quant-ph/0401052

**Why it matters:** Controlled epistemically restricted toy theories; useful comparison for what a restricted model is intended to explain.

**Access / priority qualification:** Primary manuscript consulted as an adjacent lineage, not as an equivalent algebra or contextuality theorem.

## [AB2011]

Samson Abramsky and Adam Brandenburger. The Sheaf-Theoretic Structure of Non-Locality and Contextuality. New Journal of Physics 13, 113036 (2011). DOI: 10.1088/1367-2630/13/11/113036. arXiv:1102.0264.

Source: https://arxiv.org/abs/1102.0264

**Why it matters:** Definitions of support models, global sections, logical contextuality and strong contextuality.

**Access / priority qualification:** Primary manuscript inspected; the proposed theorem uses this support hierarchy in a specified bipartite scenario.

## [AH2012]

Samson Abramsky and Lucien Hardy. Logical Bell inequalities. Physical Review A 85, 062114 (2012). DOI: 10.1103/PhysRevA.85.062114. arXiv:1203.1352.

Source: https://arxiv.org/abs/1203.1352

**Why it matters:** Logical contradiction/inequality framework; credit for the logic of witnesses, rather than claiming the Hardy implication pattern as new.

**Access / priority qualification:** Primary arXiv/APS material consulted.

## [Hardy1993]

Lucien Hardy. Nonlocality for two particles without inequalities for almost all entangled states. Physical Review Letters 71(11), 1665-1668 (1993). DOI: 10.1103/PhysRevLett.71.1665.

Source: https://doi.org/10.1103/PhysRevLett.71.1665

**Why it matters:** Original Hardy contradiction lineage; the proposed novelty is a uniform ring implementation, not the contradiction pattern.

**Access / priority qualification:** APS publication record and comparison material inspected; no claim that its Hilbert-space measurement assumptions are the same as arbitrary reversible ring bases.

## [Goldstein1994]

Sheldon Goldstein. Nonlocality without inequalities for almost all entangled states for two particles. Physical Review Letters 72, 1951-1953 (1994). DOI: 10.1103/PhysRevLett.72.1951.

Source: https://doi.org/10.1103/PhysRevLett.72.1951

**Why it matters:** Streamlined and generalized Hardy proof, including a higher-dimensional reduction to two Schmidt terms.

**Access / priority qualification:** Primary APS text consulted in the final search. Adjacent higher-dimensional proof strategy, not a chain-ring Smith classification.

## [Mermin1990]

N. David Mermin. Simple unified form for the major no-hidden-variables theorems. Physical Review Letters 65, 3373-3376 (1990). DOI: 10.1103/PhysRevLett.65.3373.

Source: https://doi.org/10.1103/PhysRevLett.65.3373

**Why it matters:** Standard Mermin/GHZ contradiction lineage; finite diagnostic examples require this credit.

**Access / priority qualification:** Primary APS text and metadata consulted.

## [SPM2006]

Metod Saniga, Michel Planat, and Milan Minarovjech. The Projective Line Over the Finite Quotient Ring GF(2)[x]/<x^3-x> and Quantum Entanglement II. The Mermin "Magic" Square/Pentagram. arXiv:quant-ph/0603206 (2006). Journal reference: Theoretical and Mathematical Physics 151, 625-631 (2007). DOI: 10.1007/s11232-007-0049-5.

Source: https://arxiv.org/abs/quant-ph/0603206

**Why it matters:** Direct finite-ring/projective-geometry comparison; ring geometry organizes Mermin configurations.

**Access / priority qualification:** Full primary manuscript inspected. This is not the same as using ring-valued bilinear amplitudes and classifying by Smith factors.

## [CMR2022]

Ida Cortez, Camilo Morales, and Manuel L. Reyes. Minimal ring extensions of the integers exhibiting Kochen-Specker contextuality. arXiv:2211.13216, first submitted 2022; version 4, 19 November 2025.

Source: https://arxiv.org/abs/2211.13216

**Why it matters:** Recent serious ring-contextuality antecedent: partial rings of symmetric matrices and algebraic hidden states.

**Access / priority qualification:** Primary full text/version history inspected. Its objects and contextuality contract differ from the finite-chain-ring bilinear support model; no exact equivalence located.

## [LiuLiu2017]

Xiusheng Liu and Hualu Liu. Quantum codes from linear codes over finite chain rings. Quantum Information Processing 16, article 240 (2017). DOI: 10.1007/s11128-017-1695-7. arXiv:1704.06375.

Source: https://arxiv.org/abs/1704.06375

**Why it matters:** Chain rings are already used in quantum-code constructions; this does not establish ring-valued quantum amplitudes or their contextuality.

**Access / priority qualification:** Primary manuscript/publication records consulted.

## [DomokosFrenkel2004]

M. Domokos and P. E. Frenkel. On orthogonal invariants in characteristic 2. Journal of Algebra 274(2), 662-688 (2004). DOI: 10.1016/S0021-8693(03)00513-1. arXiv:math/0303106.

Source: https://arxiv.org/abs/math/0303106

**Why it matters:** Distinguishes characteristic-two bilinear and quadratic orthogonal structures; prevents using the wrong group theory for U^T U=I.

**Access / priority qualification:** Primary manuscript, especially its initial form conventions and backward references, inspected.

## [Lueneburg1988]

Heinz Lueneburg. On a Decomposition of Square Matrices over a Ring with Identity. Publications de l'IRMA, Strasbourg, 358/S-18, Actes du 16e Seminaire Lotharingien de Combinatoire, pp. 109-111 (1988).

Source: https://mat.univie.ac.at/~slc/opapers/sc18luene.pdf

**Why it matters:** Theorem 3 supplies the classical constant-row/column-sum permutation-matrix span fact used to strengthen T13.

**Access / priority qualification:** Full primary paper and theorem screenshot inspected. The text itself describes the dimension ingredient as folklore; 1988 is an explicit located source, not an earliest-ever claim.

## [Werner2001]

Reinhard F. Werner. All Teleportation and Dense Coding Schemes. Journal of Physics A: Mathematical and General 34, 7081-7094 (2001). DOI: 10.1088/0305-4470/34/35/332. arXiv:quant-ph/0003070.

Source: https://arxiv.org/abs/quant-ph/0003070

**Why it matters:** General teleportation/error-basis architecture. The finite-field rank criterion is elementary linear algebra in a well-established protocol lineage.

**Access / priority qualification:** Primary manuscript/publication metadata consulted; complex unitarity conditions are not silently imported into F2.

## [BBPS1996]

Charles H. Bennett, Herbert J. Bernstein, Sandu Popescu, and Benjamin Schumacher. Concentrating Partial Entanglement by Local Operations. Physical Review A 53, 2046-2052 (1996). DOI: 10.1103/PhysRevA.53.2046. arXiv:quant-ph/9511030.

Source: https://arxiv.org/abs/quant-ph/9511030

**Why it matters:** Entanglement-concentration lineage; prevents marketing rank multiplication as a novel physical activation principle.

**Access / priority qualification:** Primary manuscript consulted. The report proves only conditional algebraic extraction and assigns no physical success probability.

## [VenueQS]

Quantum Studies: Mathematics and Foundations. Official aims and scope, consulted 18 September 2026.

Source: https://link.springer.com/journal/40509/aims-and-scope

**Why it matters:** Potential venue for mathematically explicit quantum-foundational support models.

**Access / priority qualification:** Official journal page. Fit is an assessment, not an acceptance prediction.

## [VenueFoP]

Foundations of Physics. Official aims and scope, consulted 18 September 2026.

Source: https://link.springer.com/journal/10701/aims-and-scope

**Why it matters:** Potential venue if the paper explains what the model isolates about foundations rather than only presenting a finite algebra.

**Access / priority qualification:** Official journal page.

## [VenueJPA]

Journal of Physics A: Mathematical and Theoretical. Official journal scope, consulted 18 September 2026.

Source: https://publishingsupport.iopscience.iop.org/journals/journal-of-physics-a-mathematical-and-theoretical/about-journal-physics-mathematical-theoretical/

**Why it matters:** Conditional mathematical-physics target; requires significance and comparison beyond a small toy realization.

**Access / priority qualification:** Official IOP page. No prestige, impact-factor, or acceptance-rate assumptions used.

## [VenueQPL]

Quantum Physics and Logic. Official conference site and scope, consulted 18 September 2026.

Source: https://qplconference.org/

**Why it matters:** Potential future-edition venue if developed as a categorical/logical process theory.

**Access / priority qualification:** Official site. The 2026 conference dates are already past; no current submission opportunity is asserted.



---

# Supplement 3: search scope

# Search scope and reproducibility limitations

The accompanying log records actual query strings and important primary-source follow-ups from this review. Search results were grouped and assessed across the closely related queries; a source listed as a close hit is not a claim that every repeated query independently returned it. The API does not expose the backend search-engine identity. No direct Google Scholar, MathSciNet, zbMATH, Scopus, or Web of Science search is claimed.

The date is the review date, 18 September 2026, not a per-call timestamp. ArXiv identifiers, publisher DOIs, and author URLs allow later researchers to reproduce the source checks even if search rankings change. The log is an auditable search account, not a complete transcript of every scrolling, screenshot, or metadata call.

No exact equivalent to the full finite-chain-ring Smith classification was located. That is not a proof of priority. Main unresolved checks are: full Bricken matrix-techniques notes; older Berman/Charpin original texts and their backward references; specialist finite-local-ring contextuality and matroid/bilinear basis-selection literature; and a final pre-submission citation update.

Repeated searches and irrelevant Hardy-inequality, physical-ring, jewelry, or valuation-algebra results are not counted as positive literature coverage. Primary author manuscripts and publisher pages are distinguished from metadata-only or inaccessible items in the bibliography.
