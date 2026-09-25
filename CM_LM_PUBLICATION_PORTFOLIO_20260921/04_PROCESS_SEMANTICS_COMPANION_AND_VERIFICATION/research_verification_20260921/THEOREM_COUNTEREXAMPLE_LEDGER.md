# Theorems, counterexamples and proof status

Labels: **PA** proved analytically in this dossier; **IP** inherited from inspected or supplied prior work; **EF** exhaustive only over the named finite universe; **CW** computational witness; **CJ** conjectured; **OPEN** unresolved; **CE** disproved by counterexample. A PA label does not assert novelty or independent human verification. Proofs are handwritten mathematical arguments, not proof-assistant certificates.

**Local provenance correction:** the existing 20 September Process_Semantics_Research package and its Restricted_Conversion_Review_20260920 already contain the principal results below. They were discovered during destination-preservation checks and then inspected. T01--T16 are rederivations/reassessments or inherited comparisons, not new project discoveries on 21 September. In particular the earlier review already proves the measurement stabilizer and gives the resolved-disposal witness recorded as T17. See PRIOR_WORK_RECONCILIATION.md.

## T01. Scalar obstruction [PA; elementary; source audit already contains the witness]

Assume the tensor unit is A, independent scalar preparations compose by multiplication, every nonzero scalar is possible, and independent possible preparations have a possible joint preparation. These assumptions are inconsistent: u^3 and u are possible but their joint scalar is zero. More generally the nonzero predicate of any commutative ring with nonzero zero divisors cannot be multiplicative into Boolean possibility. This does not rule out non-Boolean weights, state restrictions, different tensor units, or a changed tensor product.

## T02. Primitive tensor closure and selective failure [PA + IP; CE to the proposed repair]

A vector is primitive iff a coordinate is a unit. Products of unit coordinates prove primitive tensor closure; an invertible matrix preserves the generated coordinate ideal. Nevertheless C=diag(1,u) is a primitive bipartite vector. Its second coordinate effect on Alice leaves (0,u) on Bob, which is nonzero and nonprimitive. Rank-one repeatable coordinate projection on (1,u) also yields (0,u). Dependency: the original nonzero-A support convention. EF: all 36,864 pairs of primitive A^2 vectors checked.

## T03. Quotient tensor and the embedding obstruction [PA; standard module algebra; CE]

The universal bilinear map identifies A/(u^l) tensor_A A/(u^r) with A/(u^min(l,r)). For I=(u^3) ~= A/(u) and J=(u) ~= A/(u^3), their abstract generators have nonzero tensor. The tensor of the two inclusions into A sends it to u^3*u=0. Thus an abstract module isomorphism is insufficient to preserve a branch's embedding into its parent. Retagging cannot be claimed monoidal while also preserving those inclusions. General quotient associativity survives; nonzero element preservation does not.

## T04. Closed binary instruments [PA here; closely inherited from MQT]

For finite binary carriers, branch spaces K_i of linear maps define S -> span K_i S. Joint completeness is intersection ker T=0. A finite basis of all the K_i gives an injective stacked map J. J tensor id is injective, so no nonzero correlated input loses every outcome. The tensor of two injective stacks is injective. For an adaptive sequential test, vanishing of every final branch first implies each intermediate branch vanishes, and then the original state vanishes. Products of maps associate and field tensors obey interchange. Spans commute with those products, so forgetting outcomes is consistent with sequential and parallel composition. Discard is contraction by the entire local dual. Its independence from a complete local test follows because the rows of J span the original dual. This supplies all ten requested operational ingredients in the specification. No new representation theorem is claimed; compare Schumacher--Westmoreland §§3--4.

## T05. Faithful lax, not strong, restriction of scalars [PA; standard]

U retains a map's underlying function, proving faithfulness and preservation of composition, addition and identities. The quotient q imposes a m tensor n = m tensor a n and so is natural; iterated balancing gives the same quotient independently of parentheses. The inclusion F2 -> A supplies the unit map. Dimension mismatch and q(u^3 tensor u)=0 disprove strong monoidality and nonzero-tensor preservation. A chosen ring-state map has source U(A), so a preparation claim also requires the explicit unit map. This is the functor asserted; the resource encoding in T06 is different.

## T06. Frobenius support encoding [PA; classical ingredients; priority unresolved for this interface]

Let Omega=sum_{r=0}^3 u^r tensor u^{3-r}. Multiplication by u on its first or second leg gives the same sum, after omitting zero boundary terms. Hence (a tensor 1)Omega=(1 tensor a)Omega for every a. Define Delta(a)=(a tensor 1)Omega. Applying id tensor tau gives a, so Delta is injective. Therefore (x tensor y)Delta(a)=Delta(xay).

Apply this identity in each coefficient block of E(C): (L_x tensor L_y)E(C)=Delta(x C y^T). Nonzero support is identical. A basis of A-linear rows gives an injective stacked binary map (indeed an invertible one), so its block-row instrument is complete in T04. Gates U(P),U(Q) give E(P C Q^T). This proves that all nonzero shared resources have valid encoded preparations and precisely preserves their stated coarse tables.

In binary matrices, E(C) has coefficient matrix rho(C) J, where J reverses the four u-basis coordinates in each block. J is invertible. Thus rank(E(C))=sum_i(4-a_i). For C=(1), rank=4, although 1 is a balanced product. This disproves separability preservation. For the same example, discarding one coefficient leg gives the whole binary space U(A), disproving equality with a scalar-free pure update. EF: all 8,640 effect pairs on 15 Smith representatives, plus all 256 scalar pairs for the balancing identity. The universal proof, not that representative check alone, handles all C and all dimensions.

## T07. Nonseparability of this Frobenius algebra [PA; standard obstruction]

Multiplication of Omega gives four copies of u^3, hence zero. More strongly, if t=sum c_ij u^i tensor u^j commutes with u between its legs, coefficient comparison gives c_{i-1,j}=c_{i,j-1}, with missing indices zero. The only free coefficients lie on anti-diagonals i+j>=3, so t lies in the span of Omega,(u tensor 1)Omega,(u^2 tensor 1)Omega,(u^3 tensor 1)Omega. All have zero product. No commuting t has mu(t)=1. Consequently A is not separable over F2, and the selected Delta is not a section of the balanced quotient or multiplication. Separable-Frobenius preservation theorems are inapplicable.

## T08. Exact embedded algebra normalizer [PA; elementary semilinear normalizer]

Let B=rho(M_2(A)) <= End_F2(A^2). Then

N_GL(8,2)(B) = GL_2(A) semidirect Aut_F2(A), of order 98,304.

Proof: the center of B is scalar multiplication by A. A normalizing g induces an F2-algebra automorphism phi of this center. Let S_phi act coefficientwise on A^2. Then S_phi^{-1}g commutes with every A scalar, hence is an invertible A-linear map. Conversely both factors normalize B. The intersection is trivial because a coefficientwise phi is A-linear only when phi=id. Every automorphism has phi(u)=u+b u^2+c u^3, b,c in F2; each substitution is invertible by triangularity, so there are four. Reduction GL_2(A)->GL_2(F2) has 2^12-element kernel, giving 6*4096*4=98,304.

The full binary state stabilizer of the coarse 192-basis family is also this normalizer [IP, prior local review R3; proof rechecked]. To see this first consider the 24 column subspaces Av for primitive v. A map fixing all of them fixes both axes and A(1,1), so has form diag(T,T). Fixing every graph A(1,a) forces T to commute with regular multiplication by every a, so T is multiplication by a unit. The pointwise stabilizer is therefore A^times. Its binary span is scalar A, since 1 and 1+u^j span A. Every setwise stabilizer normalizes that pointwise stabilizer and hence scalar A, so lies in the above normalizer. The converse is immediate. For row effects use E_x^T=J_2 A x^T and pullback g; the criterion is J_2 g^T J_2 in N, equivalent to g in N because J_2 C^T J_2=C for scalar C. Complementary pairs yield the same stabilizer since each point occurs in a pair. The induced permutation group has order 98,304/8=12,288. This is not the full abstract distant-graph automorphism group. The centralizer of the fixed scalar action, rather than its normalizer, is GL_2(A); allowing phi changes what it means to preserve a labelled u.

EF: all 24,576 GL_2(A) matrices and four coefficientwise automorphisms constructed, producing 98,304 distinct binary matrices. This does not exhaust GL(8,2); the proof supplies exhaustion of the normalizer. Prior relationship: standard semilinear reasoning; Brešar et al., Corollary 3.4, is a broader adjacent automorphism result, not a new-priority basis.

## T09. One-copy reversible classes [PA + IP Smith theory]

For encoded resources E(C), local GL(A) equivalence is exactly Smith equivalence C -> P C Q^T. For 2x2 A matrices there are 15 types 0<=a<=b<=4, including the zero matrix (4,4), hence 14 nonzero classes. Under unrestricted binary local GL there are only the binary rank classes R=8-a-b. The pair (0,2),(1,1) has the same R=6 but different h and different P01 support classes.

Even allowing independent local algebra normalizers cannot identify different Smith types when both endpoints lie in this encoded family: the binary image of the coefficient matrix is the A-module im(C), whose cyclic lengths 4-a_i are invariant under an invertible semilinear map. A local semilinear map need not keep an intermediate tensor inside E(M_2(A)); this does not affect the endpoint argument. EF: all 65,536 matrices classified and their binary ranks independently checked.

## T10. Exact one-copy selected filter order [PA]

For equal-sized matrices, pad sorted Smith exponent lists by 4. A nonzero D is obtainable as F C G^T with arbitrary A-linear local selected filters iff b_i>=a_i for every i, where a and b are the source and target exponents. Rectangular targets obey the same padded-list condition with compatible matrix sizes.

Sufficiency: put C in Smith form; multiply its i-th row by u^{b_i-a_i}, with a zero row interpreted in the obvious way, then apply invertible changes to reach D. Necessity: im(F C G^T) is a quotient of a submodule of im(C). For an A-module M with cyclic lengths l_i sorted decreasingly, the number of lengths at least t is dim_F2(soc(M) intersect u^{t-1}M). Under a submodule inclusion those subspaces inject, so those counts cannot increase. For a quotient Q, the map u^{t-1}M/u^t M -> u^{t-1}Q/u^t Q is onto, giving the same count inequality. Thus the sorted cyclic lengths of a subquotient cannot exceed those of M componentwise. Since l_i=4-a_i, b_i>=a_i follows. A finite adaptive branch of local filters is still one product F on Alice and one G on Bob, so classical feed-forward does not evade necessity for a selected pure output under this task.

Every filter is a permitted possible branch of {F,I} in the ambient field theory. This is not a claim of deterministic conversion or a nonzero real success probability. EF: 1,966,080 single-sided filter products, followed by transitive closure on the 15-type graph, agree with the criterion for all 225 pairs. This finite certificate also checks the 2x2 case independently of the module proof.

## T11. Monotones and a contextuality increase [PA; CE to h monotonicity]

Under T10 the exponents cannot decrease; r, binary rank R, and the threshold counts #{i:a_i<t} cannot increase. The least exponent cannot decrease. These are useful conversion monotones. The leading multiplicity h is **not** one: diag(u,1) diag(1,u)=diag(u,u), so h increases from 1 to 2, and P01's support type increases from logical/non-strong to strong. Its frozen codebook size increases from 2 to 4. This does not create binary entanglement: rank drops from 7 to 6. A contextuality statement for a fixed family is not automatically a monotone for local postselection that changes support.

## T12. Full-label multi-copy unit-rank criterion [PA; bounded operational scope]

Let r0=#{i:a_i=0}, and keep all k independent phase labels. On free R_k modules, E(C)^{tensor_k k} is the Frobenius encoding of C^{tensor k} over R_k. It can be converted by R_k-linear selected filters to E_Rk(I_d), with zero unused coordinates allowed, iff d<=r0^k.

Proof: choose Smith changes independently in each copy. The resulting diagonal entries are monomials product_j u_j^{a_{i_j}}. Exactly r0^k are units. Reduction modulo (u_1,...,u_k) gives matrix rank r0^k. Any selected local product decreases that residue rank, whereas the target has rank d. Conversely select d unit entries with coordinate projections; those entries are exactly 1 in the chosen Smith frame. The projections are valid selected branches. This is an exact argument for every k, not merely a finite check.

In particular diag(1,u) has r0=1, and diag(u,u) has r0=0: neither produces a free R_k target of dimension >=2 at any k in this task. For larger d0 with r0>=2, multiple copies can supply larger free R_k targets. These targets have binary local dimension 4^k*d. Extracting a fixed eight-dimensional A-labelled target after resolved phase disposal is possible in a different task (T17). **OPEN:** a complete classification for broader or unobserved-disposal protocols. EF: 60 residue-count cases for k=1..4 are a regression check only.

The earlier review R4 proves the stronger standard unit-minor statement: for any matrix N over any commutative local B, rectangular L,N,Q can satisfy LNQ=I_d iff rank(N mod maximal ideal)>=d. Necessity is reduction; sufficiency selects a d-by-d unit minor H=SNT and takes L=H^{-1}S,Q=T. T12 is an immediate specialization; no Smith classification over R_k is required.

## T13. Unrestricted binary activation [PA + IP ordinary rank]

With arbitrary local binary filters, a pure coefficient matrix of rank R converts to a rank-D target iff D<=R; k copies have rank R^k. Thus an encoded rank-six resource reaches a rank-eight target with two copies under that enlarged task. This is ordinary field matrix normal form, not a new activation phenomenon. It cannot be exported to T12, whose target and operations are different.

## T14. Three distinct exact coding contracts [PA; P01 inherited where stated]

For square d>=2 and R=sum(4-a_i):

1. GL_d(A) encoders and transported A-basis coefficient-block decoder: N=dh, by P01's theorem and the explicit complete realization in the specification.
2. The same encoders but an arbitrary binary joint basis decoder: N=dR.
3. All binary local encoders GL_(4d)(2) and arbitrary binary joint basis decoder: N=(4d)R.

Proof of 2: GL_d(A) spans M_d(A) over F2. Indeed I+aE_ij is invertible for i!=j, so aE_ij is a difference of invertibles; left multiplication by a suitable permutation gives every aE_ii. The orbit's binary span is therefore {XC:X in M_d(A)}, of dimension dR. Disjoint decoder supports force codewords to be binary linearly independent, giving the upper bound. Choose dR independent orbit vectors and extend them to a binary basis to attain it. Proof of 3 is the same field argument. Case 1 relies on P01's stronger restriction on the decoder, not on this binary span bound.

These counts are one-shot exact message counts, with no discard/reprepare encoding, no real probabilities and no asymptotic capacity claim. The field carrier's unrestricted baseline is 4d, so the original comparison to d is not an unrestricted communication advantage.

## T15. Teleportation and recovery boundary [IP + PA comparison]

P01's shared raw-vector theorem requires invertible C. In the full binary completion the encoded resource has rank 4d iff C is invertible, and the known binary full-analyzer raw transfer criterion gives the same yes/no answer. This coincidence does not identify analyzers: the complete rank-one binary analyzer has (4d)^2 outcomes, while a shared A analyzer has d^2 A-valued rows. On a known binary subspace, the field rank bound and field corrections may recover dimensions up to R; on a free A submodule the structured free rank is r0. Quotient recovery after a nilpotent multiplier recovers only the coset modulo its annihilator.

## T16. Probability and multipartite limits [IP / OPEN]

P01's coarse tables are possibilistically no-signalling, and T04 supplies a closed realization. Schumacher--Westmoreland §5 distinguishes weak probability resolutions (some possible events may be assigned zero) from support-faithful resolutions; the latter need not exist. No new support-realizability classification or multipartite minimality theorem has been proved here. Generalized Mermin theorems require their stated observable and positivity hypotheses. The audit's existing finite GHZ certificates remain finite certificates.

## Explicitly unproved propositions

* OPEN: complete resource preorder with free ancillary systems, label-discard, catalysts and selected coefficient-resolution measurements.
* OPEN: a novel ring-native closed semantics retaining the original nonprimitive hierarchy while deliberately changing one of T01's assumptions.
* OPEN: exact historical priority of the particular support interface and its packaging with the restricted resource tasks.
* CJ: none is promoted as a result in this release. Computational agreement is not used to conceal a conjectural universal statement.

## T17. Resolved-disposal activation, inherited and rerun [IP + CW; prior review R5]

Set B=A[u_2]/(u_2^4), write v=u_2, and use two copies of diag(1,u_1^2), so N=diag(1,v^2,u_1^2,u_1^2 v^2). Let L have rows (1,0,0,0),(v,0,0,0), and Q have rows (v^3,0,0,0),(v^2,0,0,0). Then L N Q^T=[[v^3,v^2],[0,v^3]]. Select the binary coefficient functional ell=[v^3] on each party's v register. Since (ell tensor ell)Delta_v(a)=ell(a), the retained A coefficient matrix is I_2. Every step is a possible branch of a complete ambient instrument. The final resource is E_A(I_2) with one retained A register per party.

The witness uses only N_00=1, so it also works with the unit sectors of two copies of E_A(diag(1,0)); it does not demonstrate an exclusive nilpotent resource. Forgetting the coefficient outcomes gives span{E_A(I_2),E_A(E_12)}, a two-dimensional mixed state, rather than the pure target. The coefficient functional is not the module quotient v->0: ell(v*v^2)=1. The copied earlier checker was rerun on this exact witness; input rank 36, filtered rank 8, output rank 8, unobserved mixed-state dimension 2, and the literal output equals the desired binary rows. This is an inherited explicit construction, not a new result of this run.

## T18. Established comparison orders are not interchangeable [IP + PA comparison]

Aranda Pino et al. Definition 2.1 and Antoine et al. §2.5 explicitly use rectangular factorization X=LYR. This is the underlying filter relation. Hung--Li Definition 3.1 additionally allows triangular-block erasure; their Proposition 3.7 concerns that larger Malcolmson order. For source (0,2) and target (1,1), the filtered binary ranks decrease from (6,4,2,1) to (6,4,2,0), but T10 forbids conversion because the second exponent would decrease. Therefore those rank inequalities are insufficient for the pure-filter task. The normalized functions rank(rho_{A/(u^j)}(C mod u^j))/j are the established quotient Sylvester ranks in Jaikin-Zapirain--Lopez-Alvarez Proposition 2.2. These antecedents materially reduce novelty, without weakening the direct proofs.
