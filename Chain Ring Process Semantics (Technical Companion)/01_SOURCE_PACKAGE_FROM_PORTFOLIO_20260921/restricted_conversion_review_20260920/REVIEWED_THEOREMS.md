# Reviewed statements and complete proof amendments

These statements supplement the frozen baseline T07–T12. All universal statements below have analytic proofs. Computations are corroboration over the universes specified in `REPRODUCIBILITY.md`. Historical priority is recorded separately.

## R1. Conventions and selected protocols

Let A=F_2[u]/(u^4). The regular multiplication matrix R(a) uses the column basis (1,u,u^2,u^3). Let J be the anti-diagonal matrix, so R(a)J=JR(a)^T. For an m-by-n A-matrix M, Phi_A(M) has (i,j) block R(M_ij)J. It is a binary pure bipartite vector, not an A-balanced tensor preparation. Its binary coefficient rank is denoted r_B.

A local filter from U(A^m) to U(A^p) is R(L), for L of shape p-by-m. For a second filter Q of shape q-by-n,

    (R(L) tensor R(Q)) Phi_A(M) = Phi_A(L M Q^T).

The same identity holds for B=F_2[u_1,...,u_k]/(u_i^4), with the product Frobenius functional. The selected map may be singular. It is an admissible outcome of an ambient modal instrument by adjoining an identity outcome with the original output type. The common kernel of that instrument is zero.

For a finite adaptive local protocol, fix all classical labels. The product of local maps along this transcript is again a pair of local linear maps, with the declared scalar action. Product logical field ancillas are linear coordinate embeddings; their removal is a coordinate contraction, also linear over the unchanged coefficient ring. If a coarse outcome has one-dimensional nonzero final state, expand each process subspace into a spanning family of maps. Every nonzero resulting vector must equal that binary pure target. At least one exists. Thus pure-target existence reduces to a nonzero pure trajectory. Taking a span cannot cancel unwanted vectors or turn independent vectors into a pure target.

This argument concerns possible selected outcomes. It asserts no success probabilities and no deterministic conversion. It introduces no entangled ancillary resource.

## R2. Exact one-copy preorder, including rectangular systems

Let nonzero M have shape m-by-n and nonzero N have shape p-by-q. Sort their Smith exponents increasingly and pad both lists with exponent 4 to length D=max(min(m,n),min(p,q)). Then the following are equivalent:

1. N=L M Q^T for A-matrices L,Q of the above shapes.
2. Phi_A(N) is a possible pure target under local A-linear filters, finite classical feed-forward and logical product ancillas.
3. b_i >= a_i for every i=1,...,D.

Invertible local equivalence for fixed local dimensions is equality of Smith lists. The theorem is about reachability of each concrete matrix, not just its binary rank.

Proof of necessity. Put H=im(M). The image of M Q^T is an A-submodule K of H, and im(N) is a quotient of K under L. For any finite A-module T, put

    f_j(T)=dim_F2( u^(j-1) T intersect soc(T) ),  j=1,...,4,
    soc(T)={x:u x=0}.

If T has decreasing cyclic lengths ell_i, then f_j(T)=#{i:ell_i>=j}; check this on each A/(u^ell_i). An injection T→H restricts to an injection of each displayed subspace, so f_j(T)<=f_j(H). These threshold inequalities are equivalent to ell_i(T)<=ell_i(H) after padding by zeros. For a surjection, take the exact F_2-dual, with action (a.f)(v)=f(av). A cyclic length-ell Jordan block has a transposed Jordan block on the dual and hence the same length. The injection argument applies to the dual surjection. Applying both steps proves that each cyclic length of im(N) is at most its counterpart in im(M). These lengths are 4-b_i and 4-a_i.

Proof of sufficiency. Use invertible matrices to reduce M and N to their rectangular Smith forms. For each desired nonzero target entry, b_i<4 and the inequality supplies an existing source entry with a_i<=b_i. Select that source coordinate on both sides and multiply one side by u^(b_i-a_i). Set remaining target coordinates to zero. Undo the target Smith basis changes and include the source changes in L,Q. This realizes the actual N. There is no expression u^(4-4) to interpret for a missing coordinate. R1 proves equivalence with protocols.

The complete monotones are

    c_j(M)=#{i:a_i<j},  j=1,...,4.

Each target c_j must be at most its source value, and these inequalities are sufficient. The filtered ranks

    rho_t(M)=rank_F2 R(u^t M)=sum_i max(4-a_i-t,0)

are monotone but their inequalities are insufficient. Source (0,2) has profile (6,4,2,1), target (1,1) has profile (6,4,2,0), yet conversion is impossible since 1<2 in the second position. This is the same pair separated from the larger Malcolmson order in R6.

## R3. Normalizer and dual-action precision

On V=U(A^2), let C be scalar multiplication by A and B=End_A(A^2). Then C is the centre of B and B is the centralizer of C. A binary g normalizing B induces an F_2-algebra automorphism sigma of A. Dividing g by coefficientwise sigma leaves an A-linear invertible map. Conversely both factors normalize B. Thus

    N=N_GL8(F2)(B)=GL_2(A) semidirect Aut_F2(A),  |N|=98,304.

The four ring automorphisms send u to u+c u^2+d u^3, c,d∈F_2. Reduction modulo u gives |GL_2(A)|=6*2^12. These are direct proofs; no inappropriate field-only Skolem–Noether hypothesis is needed.

For the 24 column subspaces P={Av:v primitive}, a map fixing all points fixes the two axes and A(1,1), so is diag(T,T). Fixing A(1,a) for every a forces T to commute with R(a), hence T=R(c) for a unit c. Therefore the pointwise stabilizer is the eight scalar units. Their binary span is C, since 1 and 1+u^j span A. Any setwise stabilizer normalizes this pointwise group, hence C, and so lies in N. Conversely all semilinear maps preserve P. The action on points has order 98,304/8=12,288.

To identify the measurement group without a transpose ambiguity, put J_2=diag(J,J). Writing effect subspaces as columns gives E_x^T=J_2 A x^T. Their column-action stabilizer is J_2 N J_2. A state map g acts by pullback E↦Eg (or Eg^-1 under the opposite active convention). Thus it preserves the row-effect family iff J_2 g^T J_2∈N. Since J_2 C^T J_2=C, this condition is equivalent to g∈N. This proves the original state-group assertion. The 192 complementary unordered pairs give the same stabilizer, because every point occurs in a pair.

Independent semilinear operations can leave the Phi image. Between structured endpoints, however, the Smith type is still necessary: g^-1 R(u)^t g is multiplication by sigma^-1(u)^t, which is u^t times a unit. Hence all ranks rank(R(u)^t X) are invariant under the two local normalizer factors. On structured X these ranks determine the Smith multiplicities by successive differences. Smith equivalence already supplies sufficiency. This does not classify all ambient binary states.

## R4. Exact retained-phase free-target extraction

Algebraic statement. Let (B,m) be a commutative local ring with residue field F. Let N be an s-by-t matrix over B and let d>=1. There exist L of shape d-by-s and Q of shape t-by-d satisfying

    L N Q = I_d

if and only if rank_F(N mod m)>=d.

Proof. Reducing the equation gives I_d=bar(L) bar(N) bar(Q), proving necessity. Conversely choose a nonzero d-by-d minor of bar(N). Let S,T select its rows and columns, so H=SNT. The determinant of H is outside m, hence is a unit; H is invertible by the adjugate formula. Set L=H^-1 S and Q=T. Then LNQ=I_d. This is an explicit construction. No Smith theorem over B is required.

Operational specialization. For B_k=F_2[u_1,...,u_k]/(u_i^4), use its nondegenerate Frobenius pairing and retain all k phase registers. Then Phi_B(N) can produce Phi_B(I_d) on a pure selected branch of the R1 operation class exactly when rank_F2(bar N)>=d. For k copies of Phi_A(M), regrouping gives N=M(u_1) tensor ... tensor M(u_k), so

    rank_F2(bar N)=r_0^k,  r_0=#{unit Smith factors of M}.

Thus the baseline condition r_0^k>=d is both necessary and sufficient.

Why the socle proof gives precisely this condition. Put s=u_1^3...u_k^3. Multiplication by s annihilates m, so sN=s bar(N). In the regular representation multiplication by s has binary rank one. Consequently

    rank_F2 R_B(sN)=rank_F2(bar N).

The right Frobenius matrix is invertible and changes neither side's rank. This identifies the old socle monotone with residue rank on structured states. More general rho_alpha(X)=rank(D_alpha X) remain monotone under B_k-linear local filters by the intertwining relation. Their completeness for arbitrary targets over B_k is not asserted.

For diag(1,u^2), r_0=1. No number of copies gives a retained-phase free target of coordinate rank two. For k=2 the ordinary binary ranks are 36 for the input and 32 for Phi_B2(I_2); the residue ranks are one and two. The obstruction separates ordinary rank from restricted conversion, but it is an elementary unit-minor obstruction.

## R5. Explicit activation with resolved disposal

This is a different, explicitly enlarged operation class. Start with two literal independent copies, permit rectangular B_2-linear local filters, then measure the second phase register in the binary coefficient dual basis, keep the outcome labels, and retain only the first phase register. Such a resolved measurement is allowed in the ambient field-modal theory. It is not a B_2-linear map into a free B_2 output, so R4 does not apply after it.

Write v=u_2 and use logical input order (0,0),(0,1),(1,0),(1,1). For two copies of diag(1,u^2), the regrouped coefficient matrix is

    N=diag(1,v^2,u_1^2,u_1^2 v^2).

Choose the following two B_2-linear filters, each of shape 2-by-4:

    L = [1  0  0  0]       Q = [v^3  0  0  0]
        [v  0  0  0]           [v^2  0  0  0].

Then

    L N Q^T = [v^3  v^2]
              [ 0   v^3] = W.

Let ell extract the coefficient of v^3 in F_2[v]/(v^4). Both parties now select ell on their second phase register. On a scalar Frobenius block Delta_v(a),

    (ell tensor ell) Delta_v(a) = ell(a),

as follows directly from Delta_v(a)=sum_(i=0)^3 v^i tensor v^(3-i)a. Therefore the retained coefficient matrix is obtained by applying ell entrywise to W, giving I_2. The retained state is exactly Phi_A(I_2). Every used branch is part of a complete ambient instrument; the final state is nonzero. A single copy cannot make this target under the original A-linear contract by R2.

The construction uses only N_00=1. It also works for two copies of Phi_A(diag(1,0)), whose selected unit sectors are Delta_A(1) tensor Delta_A(1). These already have binary Schmidt rank 16. The protocol transfers part of existing phase entanglement into a logical coordinate; it does not reveal an exclusive power of nilpotent resource amplitudes.

For the displayed witness, the final unresolved mixture contains two independent vectors. Besides the desired Phi_A(I_2), coefficient outcomes (2,3) or (3,2) give Phi_A(E_12). Thus blind disposal produces span{Phi_A(I_2),Phi_A(E_12)} of dimension two. This proves only that forgetting the labels in this protocol does not give the pure target. It does not classify every protocol permitting unobserved phase disposal.

The total local map intertwines u_1. It does not intertwine u_2 with the quotient action u_2=0: ell(v*v^2)=1 whereas v acts as zero on that quotient. Treating this measurement as ordinary B_2-module quotienting would be incorrect.

## R6. Priority distinctions for comparison and rank

The following are source comparisons, not new algebraic results.

- The factorization relation N=LMQ is the algebraic comparison in Aranda Pino et al., Definition 2.1, and Antoine et al., section 2.5 / Lemma 2.6 proof. At fixed square size it is the principal two-sided-ideal preorder (Green's J preorder). Our A-filter interpretation is a specialization.
- Hung–Li's Definition 3.1 adds the step [C E;0 D]↦diag(C,D). Their Lemma 3.6, with A=u, k=0, j=m=1, permits diag(u,u) below diag(1,u^2). R2 forbids this as a local-filter conversion. Therefore their Proposition 3.7 is not a sufficiency theorem for this operational contract.
- On A, define q_j(M)=rank_F2 R_(A/(u^j))(M mod u^j). Direct Smith calculation gives q_j=sum_i max(j-a_i,0)=rho_(4-j). Consequently q_j/j are the standard extreme Sylvester ranks described in Jaikin-Zapirain–López-Álvarez Proposition 2.2. These rank inequalities classify the broader Malcolmson order under Hung–Li's hypotheses; they do not replace the complete c_j here.

Exact chain-ring filter classification priority in Cao's 2010 paper remains unresolved because its full text was not inspected. The independently written proof of R2 does not depend on that inaccessible paper. A bounded search cannot certify the novelty of the combined operational presentation.

## R7. Coding and contextuality checks

For fixed nonzero M in Mat_d(A), d>=2, with GL_d(A) encoders and an arbitrary binary joint basis decoder, the orbit span is {XM:X∈Mat_d(A)}. Indeed I+aE_ij and I express each off-diagonal aE_ij as a sum of invertibles, and multiplying by a permutation gives diagonal matrix units. The row image of M has binary dimension r_B, hence the orbit span has dimension d*r_B. Disjoint nonzero decoded supports imply linear independence; conversely an orbit basis extends to a full binary basis. This proves the exact fixed-orbit message count d*r_B. It is not a capacity with arbitrary preparations, adaptive multi-use encoders, or restricted decoders.

The filter diag(u,1) takes diag(1,u) to diag(u,u), raising the leading multiplicity from one to two and, using P01's static classification, logical to strong contextuality. The binary rank drops from seven to six. Thus leading multiplicity, the P01 code count 2h, and strong-contextuality status are not monotone under the selected filters declared here. This is a direct counterexample, not a new general theory of hidden nonlocality or a probabilistic contextuality resource theorem.
