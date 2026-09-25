# Corrected and generalized formal theorem set

Extract from RESEARCH_REPORT.md. Reference keys resolve in ANNOTATED_BIBLIOGRAPHY.md. Priority and access qualifications are in the full report.

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

