# Formal theorem set

Extracted from CAPABILITY_REPORT.md. Operational contracts and model definitions in that report are part of every statement. Imported results remain explicitly identified.


---

## Theorem Q1: exact modal discrimination is a direct-sum condition

Let S_i be sets of nonzero states in a finite-dimensional vector space over a field, and U_i=span(S_i). A complete linear readout can distinguish the labels i with certainty for every possible outcome only if sum_i U_i is a direct sum. Conversely, an invertible basis readout can distinguish the labels when this direct-sum condition holds.

**Proof.** Correctness assigns disjoint sets of readout coordinates to distinct labels. The image of U_i is contained in the corresponding coordinate subspace. A complete readout is injective when all branch maps are collected in a direct sum; hence a nontrivial dependence across label subspaces is impossible. Conversely, choose a basis for each U_i, concatenate these independent bases, and extend to the whole space. Readout in the resulting dual basis identifies the label. For two labels this reduces to U_0 intersect U_1 = {0}. For one state per label it reduces to linear independence. QED.

The same necessary condition applies to ring models after faithful binary expansion. Thus failure even with arbitrary field-linear readout implies failure under the narrower A-linear block readout.

---

## Theorem Q2: Deutsch needs exactly two queries

For the pointwise oracle O_f with fixed invertible G_0,G_1 over characteristic two, no exact one-query procedure can determine f(0) xor f(1), regardless of f-independent ancillary dimension or linear preprocessing/postprocessing.

**Proof.** Write the prepared state in the two address sectors as (a_0,a_1), allowing arbitrary target and spectator degrees of freedom. The four post-query states v_00,v_01,v_10,v_11 obey

    v_00 + v_11 = v_01 + v_10
                 = ((G_0+G_1)a_0, (G_0+G_1)a_1) = w.

If w is nonzero, the constant and balanced spans intersect nontrivially. If w is zero, both sector differences vanish, so all four states coincide. Either case violates Q1. Any complete linear subsequent instrument preserves the relevant obstruction. Two ordinary basis-state queries suffice by storing and XORing the two answers. QED.

This is stronger than saying that the conventional Hadamard matrix becomes singular. It excludes another one-query solution under the same pointwise oracle contract, including a pointwise controlled R-oracle.

The independent finite test examines every nonzero preparation in dimensions 4 and 8: 15 states without a spectator and 255 with a two-level spectator. It does not brute-force arbitrary ancilla dimension; the proof handles that.

---

## Theorem Q3: Deutsch-Jozsa has no exact one-query solution here

For n>=2, partition the N=2^n addresses into four equal sets A,B,C,D. The three functions with supports A union B, A union C, and B union C are balanced and have pointwise XOR zero. The oracle depends affinely on its Boolean control bit, so in characteristic two

    O_f1 + O_f2 + O_f3 = O_0.

For any nonzero prepared state, the constant-zero post-query state is therefore in the span of the balanced post-query states. Invertibility ensures that it is nonzero. Q1 forbids exact distinction. The n=1 case is Q2. QED.

State preparation by shears, the ordinary oracle, and any complete linear readout are all permitted in this no-go result. There is no hidden cost argument: the one-query mechanism itself fails.

A deterministic classical upper bound N/2+1 is inherited by basis-state execution. This report does **not** prove that upper bound optimal for multi-query modal computation. The supported general bounds are 2 <= Q_exact <= N/2+1, with equality 2 when n=1. Conventional randomized bounded-error comparisons require an external probability model and are a different benchmark.

---

## Theorem Q4: exact Bernstein-Vazirani requires n queries

For f_s(x)=s dot x over F2, an exact q-query characteristic-two linear modal algorithm requires q>=n. Basis-state queries at e_1,...,e_n attain n.

**Proof.** Since the dot product is computed in characteristic two, the oracle matrix is affine-linear in the secret bits:

    O_s = O_0 + sum_j s_j A_j.

After q queries, each component of the final vector is a multilinear polynomial of degree at most q in s_1,...,s_n. Thus all 2^n possible final states lie in the span of at most

    sum_{j=0}^{min(q,n)} binomial(n,j)

coefficient vectors. If q<n, this is less than 2^n. Q1 says the 2^n exactly distinguishable secret-dependent states must be linearly independent, a contradiction. Ancillas only enlarge the ambient coefficient vectors, not their number. Complete adaptive linear branches can be recorded in a direct sum and satisfy the same degree bound. QED.

This is a characteristic-two specialization of the polynomial-method architecture, not a claim to invent polynomial query lower bounds [BBCMW2001]. In complex quantum computing, the real/complex polynomial representing XOR is not degree one in the secret bits; hence the argument does not forbid the conventional one-query BV algorithm.

**Consequence:** the fact that the hidden function is F2-linear is not a reason to expect BV to work with F2-valued amplitudes. It is exactly what makes this lower bound strong.

---

## Theorem Q5: kickback exists, but the requisite Fourier basis does not

Put z=R^2=1+u^2. Then z^2=1. For the standard target flip X and chi=(1,z),

    X chi = z chi,
    U_f (|x> tensor chi) = z^{f(x)} |x> tensor chi.

This is genuine algebraic kickback, using the original bit-oracle contract.

However, the two character columns have matrix

    H_z = [[1,1],[1,z]],
    det(H_z)=1+z=u^2.

This determinant is a nonunit. Row and column elimination give Smith form diag(1,u^2), so it is not an invertible basis change.

More generally, the Walsh-like matrix on n Boolean coordinates, with entries z^{s dot x}, has binary regular-representation rank

    rank_F2(H_z tensor_A ... tensor_A H_z) = 4 + 2n.

**Proof.** Tensor the Smith diagonalization. The diagonal factors are u^{2k}, with multiplicities binomial(n,k). Only k=0 and k=1 survive u^4=0, contributing ranks 4 and 2n. QED.

The matrix has binary dimension 4*2^n, so its loss of rank grows dramatically. The actual unit-amplitude phase columns span only n+1 dimensions over F2. Both ranks were checked for n=1,...,6.

**R itself needs a different target.** Standard bit flip has square I, so a primitive eigenvector with eigenvalue R would imply u^2 chi=0, impossible for a primitive vector. All 192 primitive A^2 vectors were checked. A four-level cyclic target T does have the primitive eigenvector chi_j=R^{-j}, and T chi=R chi. A pointwise oracle that increments this target by f(x) therefore kicks back R^{f(x)}. This is a legitimate separately declared oracle, not automatically one use of the standard XOR oracle. Compute-control-uncompute with a standard bit oracle generally costs two evaluations.

**Literal-register qualification.** The equation X chi=z chi is an A-module eigenvalue equation. After literal binary expansion, multiplication by z is an operator on the target's phase register, not a nontrivial scalar in F2. It therefore does not by itself establish ordinary kickback with an unchanged independent target. In a literal tensor product, equality v tensor X chi=v_prime tensor chi between nonzero simple tensors over F2 forces v_prime=v and X chi=chi. Nontrivial movement of oracle information to a separate control phase register requires an additional interaction or correlated/shared-phase construction. The literal expansion provides a matrix-valued covariance identity, not permission to identify the S and L tensor contracts.

It is also false that R^{a xor b}=R^a R^b for all Boolean a,b: take a=b=1. Factoring a BV phase in this way silently changes the oracle encoding from a Boolean dot product to an integer-count phase.

---

## Theorem R1: chain-ring contextuality classification (imported and independently checked)

Let K be a finite commutative chain ring of length ell, maximal ideal (pi), and residue field k. For a nonzero bipartite coefficient matrix M, use all primitive projective local bases and support r M t^T != 0. Let r be the number of nonzero Smith factors and h the multiplicity of its lowest valuation. Then:

    r=1:          relationally local;
    r>=2, h=1:    logically contextual but not strongly contextual;
    h>=2:         strongly contextual.

This general theorem and its proof were already in the supplied adversarial review, `FORMAL_THEOREMS.md`, Theorem 9. They are not new claims of this report.

**Proof structure.** Complete bases reduce to residue-field bases. A global assignment exists exactly when there are residue hyperplanes H_A,H_B such that every primitive lift outside those hyperplanes has nonzero cross-pairing. For r=1, any supported seed event extends by choosing a unit in the active Smith coordinate in every other basis. For h=1, choosing unit first coordinates gives a global assignment because the leading term is a unit plus radical terms. For h>=2, choose a residue row outside H_A whose image is not proportional to the functional defining H_B; then choose a residue column outside H_B that annihilates that image. A radical adjustment in a coordinate with unit coefficient lifts this annihilation to an exact zero, contradicting the forced-pair condition.

Logical contextuality for r>=2 follows from the explicit Hardy submatrix. For D=diag(p,q), q=p*c, p and q nonzero, use

    F=[[0,1],[1,0]], X=[[1,0],[1,1]], C=[[1,0],[-c,1]].

The four supports FF, FX, CX, CF are respectively 1001, 0111, 1110, 0111. The FF event 00 forces the X and C choices to be 1, contradicting the forbidden CX event 11. Extra Smith coordinates can be completed by standard rows without giving the forced event an escape. QED.

For A and two logical carriers, write D(a,b)=diag(u^a,u^b), 0<=a<=b<=4, u^4=0. There are 15 Smith classes including zero. The independent inventory and full 192-by-192 support analysis give:

| Resource category | Classes excluding zero | Raw nonzero resources |
|---|---:|---:|
| Shared product / local | 4 | 5,265 |
| Logical but not strong | 6 | 34,056 |
| Strong | 4 | 26,214 |
| Total | 14 | 65,535 |

The strong classes have a=b<4. The logical-not-strong classes have a<b<4. The shared products have b=4.

---

## Theorem R1b: two binary settings cannot give strong contextuality

Consider any number of F2 mobits, any nonzero pure state, and at most two complete binary basis measurements per site. The resulting support model always has a global assignment. More generally, the same conclusion holds for two-dimensional local modules over any finite commutative local ring with residue field F2, using nonzero-coefficient support.

**Field proof.** Any two distinct local F2 bases share one effect a; write the other effects as b and a+b. Expand the state in coordinates dual to the local pairs (a,b). Choose an inclusion-minimal set S of b-coordinates with nonzero coefficient. At a site outside S, select the shared effect a in both settings. At a site in S, select b in the first setting and a+b in the second. Every context evaluates to a sum of coefficients indexed by subsets of S. The S coefficient is one and all its proper-subset coefficients are zero. Thus every selected event is possible, giving a global assignment. Coincident local bases only make the construction simpler. QED.

**Local-ring proof.** Let J be the radical and choose a nonzero leading layer of the state in J^a/J^{a+1}. This is a vector space over F2. Apply a linear functional on that layer which gives a nonzero F2-valued logical tensor. Reduce each local basis modulo J and apply the field proof. Every selected event has nonzero leading-layer value under that functional, and hence has nonzero original ring amplitude. QED.

This proof also covers literal independent phase registers with A-linear block-coarse measurements: collect their phase coefficients in the finite local algebra F2[u_1,...,u_n]/(u_i^4), whose residue field is F2, and retain the appropriately restricted local coefficients. It does not identify the literal tensor with the single-variable shared A tensor.

Consequently the usual two-settings-per-party GHZ all-versus-nothing support pattern cannot occur in these contracts, regardless of the number of parties. The three-setting GHZ construction is genuinely a different analogue. This does not exclude Hardy/logical contextuality with two settings. The constructive field certificate was checked for all 65,808 nonzero states of 1 through 4 mobits, in every context of the canonical basis pair; coordinate changes cover the other pairs.

---

## Theorem R2: leading-layer dense-coding theorem

Let M be a nonzero d-by-d matrix over a finite commutative chain ring K, d>=2. Alice encodes a message by U M with U in GL_d(K), sends her carrier, and Bob uses one complete K-linear basis measurement on K^{d^2}. Let a be the minimum Smith valuation and h the multiplicity of that valuation. Then the largest perfectly distinguishable codebook has

    N_block(M) = d*h

messages.

**Proof of the upper bound.** Write M=pi^a N with N primitive; its residue matrix has rank h. Every encoded vector U M has the same minimum valuation a, and after dividing by pi^a its leading residue lies in the image of the linear map X -> X N_bar. That image has k-dimension d*h. An invertible joint decoder acts invertibly on residues. Distinct exactly distinguishable messages have disjoint nonzero output supports, so their leading residue vectors are linearly independent. There can be at most d*h.

**Proof of attainability.** Invertible d-by-d matrices over a field span the full matrix algebra for d>=2. For off-diagonal matrix units, subtract I from I+E_ij. For a diagonal matrix unit, use two invertible matrices that differ only in that diagonal entry and whose 2-by-2 corner is [[a,1],[1,0]]. Thus one can choose d*h invertible residue encoders whose products with N_bar are independent. Lift them to GL_d(K). The corresponding divided codeword columns are independent modulo the maximal ideal, so they extend to a free basis of K^{d^2}. Its inverse is a decoder that sends the actual codewords to pi^a e_m. Each has exactly one possible block outcome. QED.

This theorem concerns finite distinguishable messages and the stated invertible-orbit encoding contract. It is not an entropy or noisy-channel capacity theorem.

For d=2 and A:

    a=b<4: 4 block messages;
    a<b:   2 block messages.

Explicit encoders and decoders for all 14 nonzero Smith representatives are in `new_dense_decoders.json`. All 24,576 local encoders per representative were used to verify the relevant spans.

**Corollary.** Under the complete chain-ring basis contract, any shared dense-coding advantage over the d-message baseline occurs exactly when h>=2, which is exactly the strong-contextuality condition in R1. Full d^2-message dense coding requires h=d, not that the common valuation is zero.

---

## Theorem R3: universal exact teleportation requires an invertible resource

For source dimension d, resource coefficient matrix M and a joint rank-one effect reshaped as E_m, the uncorrected output map is

    T_m = M^T E_m^T.

A complete analyzer is a basis of effects, and exact correction of every possible branch requires inverse branch maps. Universal single-copy teleportation is possible if M is invertible and the allowed operations provide a complete effect basis whose reshaped matrices are invertible, together with the needed inverses. If M is singular, such an exact protocol is impossible.

**Necessity.** A nonzero branch map with nonzero kernel maps x and x+k to the same nonzero output for any k in its kernel and a suitable x outside it. The two different possible inputs cannot both be corrected exactly. Thus every nonzero universal branch must be injective. On a finite free module of equal source and output rank, injectivity implies invertibility. Since T_m factors through M^T, M must be invertible. Completeness and a nonzero resource preclude all branches being identically zero. The same argument excludes rescuing a singular resource merely by postselecting a purported universally correct nonzero branch.

**Sufficiency in the compared carriers.** The four matrices

    E0=[[0,1],[1,1]], E1=[[1,0],[1,1]],
    E2=[[0,1],[1,0]], E3=[[1,0],[0,1]]

are all invertible over F2 and their flattened rows are a basis of the four-dimensional matrix space. They therefore also form an invertible analyzer over A. For dimension 8, use the 64 tensor products E_i tensor E_j tensor E_k. Correct with (M^T E_m^T)^{-1}. This matrix identity also preserves arbitrary reference correlations; it is not merely a check on a short list of basis states. QED.

For S with d=2, universal exact teleportation occurs precisely for D(0,0). For literal L with d=8, it occurs precisely at binary rank 8, assuming unrestricted field-linear analyzers and corrections.

A logical-only four-outcome analyzer does not teleport the entire independent eight-dimensional literal carrier. Its missing phase degrees cannot be treated as classical outcomes that were never measured. The full literal protocol has 64 outcomes and needs operations outside the native M_2(A) phase-linear span.

---

## Theorem R4: field dense codebooks and restricted literal codebooks

For a rank-r resource M in M_d(F2), unrestricted local invertible encoding and full joint field-linear readout yield exactly d*r distinguishable invertible-orbit codewords.

**Proof.** X -> X M has image dimension d*r. Invertible matrices span M_d(F2), so actual invertible encodings span that image and contain a basis of it. A joint invertible decoder distinguishes that basis; Q1 supplies the upper bound. QED.

For the structured literal resources obtained by expanding M in M_2(A), binary rank is

    r_bin = 8-a-b.

If Alice's encoders are restricted to GL_2(A) but Bob's final fine-grained decoder is unrestricted, the corresponding maximum invertible-orbit codebook is **2*r_bin**. The same span argument applies because GL_2(A) spans M_2(A) over F2, and X -> X M has binary image dimension 2*r_bin.

This last quantity can be below the ordinary eight-letter unassisted literal baseline. That does not mean that preshared correlations reduce the optimal capacity of a device allowed to discard them and prepare a fresh carrier: it only limits this fixed-resource invertible-orbit codebook. Allowing the baseline preparation strategy gives at least max(8,2*r_bin). The asymmetry between a restricted encoder and unrestricted decoder is an explicitly stated hardware/protocol contract, not a secretly closed homogeneous gate theory.

---

## Theorem E1: transpose orthogonality blocks a complete exact teleportation analyzer

Every U in O_d(F2) fixes the all-ones vector j. Indeed, the binary dot product satisfies x dot x=j dot x; preservation of the dot product implies U^T j=j and hence Uj=j. Therefore the linear span of O_d(F2) lies in the space of matrices whose row sums and column sums all equal one common scalar. That space has dimension

    (d-1)^2+1 < d^2,       d>=2.

For an invertible teleportation resource M, a branch admitting an orthogonal correction has its reshaped effect in a fixed invertible translate of span(O_d(F2)). Such effects cannot span the d^2-dimensional joint dual space. Hence there is no complete rank-one universal teleportation analyzer with transpose-orthogonal corrections. QED.

Permutation matrices already span this row/column-sum space, so the dimension bound is sharp. Independent enumeration gives |O_4(F2)|=48 and span dimension 10. The theorem is about the specified rank-one complete analyzer/correction protocol, not every conceivable enlarged instrument or environment.

---

## Theorem E2: the native shear and relative rotation preserve no common nondegenerate bilinear form

On two d-dimensional arms, let

    W = [[I,0],[I,I]],        D = diag(I,R),       R != I.

If a bilinear form with block matrix B=[[A,C],[D0,E]] is preserved by W, multiplication gives E=0 and D0=C. Nondegeneracy then forces C to be invertible. Preservation by the relative rotation forces C R=C, which implies R=I, a contradiction. QED.

This rules out rescuing the entire native catalogue merely by substituting an unspecified nondegenerate symplectic form for the transpose dot product. The gate set must change.

There are nevertheless useful **different** form-preserving theories. In the cyclic phase basis, R preserves the alternating form J=R^2. Enumeration gives |Sp_4(F2)|=720, while the split quadratic form Q(x)=x_0 x_2+x_1 x_3 has an isometry group of order 72. On two ordinary mobits with local alternating form J_2 and tensor form J_2 tensor J_2, 72 of the 360 ordered candidates drawn from four distinct invertible reshaped effects give complete symplectic teleportation analyzers. One such analyzer and all checks are in `new_symplectic_and_normalizer.json`.

The symplectic form on amplitude space in this paragraph is a different object from the symplectic **Pauli-label** commutator form in E.2. Neither is a positive inner product. They must not be conflated with one another or with a conventional quantum dagger.

---

---

## Theorem F1: the rotation algebra is a typed lift, not the original Boolean product

For a four-cycle R over F2, its minimal polynomial is (t+1)^4. Thus the map

    sum_j a_j R^j  <->  sum_j a_j t^j mod (t^4-1)

identifies its 16-element cyclic algebra with F2[u]/(u^4), u=t+1. Matrix multiplication becomes cyclic convolution of the four R-coefficients. The unit group has eight elements and is isomorphic to C4 times C2. Transpose in the cyclic basis induces the involution bar(R)=R^{-1}, with lambda(a)^T=lambda(bar(a)). This is a genuine algebraic involution, but it supplies neither a positive inner product nor a canonical physical state-to-effect identification. With computational block readout, independent coordinate units form a phase group (A^times)^m; under fine field-linear measurements the same transformations need not be invisible phases.

This multiplication is neither entrywise AND of CM truth coefficients nor the original 2-by-2 CM matrix product. For example, the ordinary 2-by-2 identity CM occupies opposite cyclic positions, whose rotation lift is I+R^2=u^2. The identity's lift is square-zero, not a multiplicative identity. Consequently the geometric lift is not an algebra homomorphism for either of those original products. QED.

Every eigenvalue of R in any field extension is 1, since its minimal polynomial is a power of t+1. Its order four is unipotent order, not a copy of multiplication by the complex number i. Relative phase interference is nonetheless real as an algebraic distinction: for W above,

    W diag(I,R^k) W(v,0) = (v,(I+R^k)v).

For k=0 the second arm cancels; for k=1,2,3 the kernels of I+R^k determine which inputs cancel. This is exactly XOR cancellation, with valuation-dependent kernels. Calling it XOR cancellation does not invalidate the calculation; it identifies the mechanism and its limits.

---

## Theorem F2: shared and literal composition cannot be interchanged

Over A, the nonzero vectors u^3 e_0 and u e_0 tensor to zero. Over F2, the literal tensor of their nonzero four-bit coefficient vectors is nonzero. Thus no faithful interpretation identifying every such shared product with the literal product can preserve both nonzero preparations and composition.

Moreover, the primitive shared bipartite state with coefficient matrix diag(1,u), conditioned by the primitive second-coordinate effect, produces (0,u), which is nonzero but not primitive. Consequently the all-nonzero shared state space fails independent-preparation closure, while restricting to primitive states fails conditioning closure. QED.

These are not minor notation problems. A completed operational proposal must say whether it restricts resources, changes support to a unit test, admits zero/null branches as preparations, enlarges state objects, or uses literal tensors. Each option changes some earlier claims. This report evaluates the given support experiments without silently selecting such a repair.

---

## Theorem F3: no universal linear cloning

Let V=F2^d with d>=2. There is no linear map C satisfying C(v)=v tensor v for every nonzero v, even with a fixed ancillary blank on the input.

**Proof.** Applying linearity to distinct basis vectors e_i,e_j gives C(e_i+e_j)=e_i tensor e_i+e_j tensor e_j. Cloning e_i+e_j instead requires those terms plus e_i tensor e_j+e_j tensor e_i. The cross terms are nonzero and independent. QED.

No probability, reversibility or inner product was used. Copying a known classical coefficient description, copying computational basis labels with CNOT, and the linear direct-sum map v -> (v,v) are different tasks. The last map is not tensor cloning. This is established modal background, independently recovered here [SW2012, JOS2011].

---

## Theorem F4: reversible no deleting, and the limitation of a stronger slogan

Suppose an injective linear evolution sends every v tensor v to v tensor b for one fixed nonzero blank b and retains no input-dependent environment. This is impossible for d>=2.

**Proof.** The duplicated vectors span the symmetric-tensor subspace generated by e_i tensor e_i and e_i tensor e_j+e_j tensor e_i. Its dimension is d(d+1)/2. Their proposed outputs span a space of dimension at most d. An injective map cannot make that reduction. QED.

Over F2, however, the noninvertible algebraic contraction

    D(e_i tensor e_j) = delta_ij e_i tensor b

does satisfy D(v tensor v)=v tensor b, because each scalar obeys v_i^2=v_i. Thus **linearity alone** is insufficient for a no-deleting theorem in this model. This map is not automatically an allowed complete deterministic modal process: it has a nonzero kernel, and a completion by additional branches would have to be specified. It may be treated as a heralded algebraic branch. Moving the discarded copy into an information-bearing environment is also not deletion under the fixed-blank/no-environment-information condition.

The package verifies the contraction and the clone-span dimensions for d=2,3,4. No unsupported categorical no-deleting axiom is imported.

---

## Theorem F5: exact distinguishable-syndrome error correction

Let E:L -> V be an injective linear encoding and F_1,...,F_t a specified list of linear error maps. There exists an injective linear decoder on their joint image satisfying

    D F_a E(psi) = psi tensor |a>

for every a and psi, with distinct retained syndrome labels, if and only if every F_a E is injective and their images form a direct sum.

**Proof.** Distinct output syndrome sectors are independent and preserve each input, proving necessity. For sufficiency, define D separately on each independent image using the inverse of F_a E and the required syndrome label; their direct sum is a well-defined isomorphism onto the corresponding syndrome sectors. Where source and target ambient dimensions agree, extend this isomorphism by completing bases. QED.

This is a precise analogue, not a general replacement for the quantum Knill-Laflamme condition: degenerate errors need not require distinct syndrome labels. For the three-mobit repetition encoding |0> -> |000>, |1> -> |111>, the four errors I,X_1,X_2,X_3 give four disjoint two-dimensional error subspaces that exhaust F2^8. The independent test checks all three nonzero input states and all fifteen nonzero coherent error combinations. After decoding, the logical state factors from the error-syndrome state. No stochastic error rate, fidelity or fault-tolerance threshold is thereby defined.

---

## Theorem F6: swapping and remote preparation are contraction statements

For resources M_AB and N_CD, a joint effect on B,C with coefficient matrix E produces the A,D resource

    M E N.

If M,E,N are square and invertible, the resulting resource is full-rank and local inverse corrections can put it in a chosen reference form. A complete invertible-matrix effect basis therefore supplies exact entanglement swapping. This is the same contraction algebra underlying teleportation; no rotation phase is needed. Singular or nilpotent factors can reduce rank or annihilate a shared branch.

Over a field, a nonzero desired remote vector phi can occur after one rank-one local effect on resource M exactly when phi belongs to im(M^T). Choose a nonzero preimage effect and extend it to a basis. A full-rank resource reaches every nonzero target in this heralded sense.

Over A, belonging to im(M^T) is not enough for the **primitive projective effect** contract: the target must admit a primitive preimage effect. For example, an invertible M sends primitive effects to primitive targets, not to arbitrary nonprimitive vectors. A possible heralded outcome is not guaranteed to occur. Deterministic remote preparation of a known state can instead prepare it locally and use an available teleportation protocol; this gives no new optimal communication claim. QED.

---

## Theorem F7: nonlinear Boolean logic has a linear reversible amplitude embedding

For every Boolean function f:{0,1}^n -> {0,1}^k, the basis-label map

    (x,y) -> (x,y xor f(x))

is an involutive permutation. Its permutation matrix is invertible and F2-linear on the amplitude space, and also acts A-linearly after extension of scalars. Nonlinearity of f in x does not imply nonlinear evolution of amplitudes.

A bounded-fan-in Boolean circuit for f can be compiled by computing its gate values into fresh workspace using NOT, CNOT and Toffoli-style reversible gates, XORing the result into y, and uncomputing the workspace. With a T-gate source circuit this straightforward construction uses O(T) workspace and O(T) reversible gates, apart from ordinary input/output bookkeeping. More economical ancilla tradeoffs are possible but not asserted here. Mathematically no ancilla is necessary if the entire permutation U_f is admitted as a primitive; the synthesis cost has then been placed inside that primitive.

The symbolic LM layer can represent and validate the source Boolean formulas using Paper B's valuation and pairing identities. Its existing compiler's admitted fusion rules can be used where their operand-frame preconditions hold; this does not magically extend those rules to arbitrary compound operands or remove truth-table expansion costs [B]. The independent tests cover all sixteen two-input functions, their algebraic-normal-form reversible implementations, and the corresponding LM valuations.

An ablation that removes nonlinear Boolean oracle logic but keeps **all** invertible amplitude matrices is incoherent: the latter already includes every such permutation matrix. A meaningful ablation restricts the gate catalogue, the oracle interface or the cost model.

---

## Theorem F8: a sufficient symbolic extension exists, but is additional structure

Let B be the Boolean algebra of formulas modulo logical equivalence, regarded as a Boolean ring with XOR and AND. Every b in B satisfies b^2=b, so B has no nonzero nilpotents. It cannot itself be identified with A, which contains u!=0 and u^4=0.

A well-typed symbolic augmentation is

    A_B = B[u]/(u^4).

Every Boolean valuation v:B -> F2 extends uniquely coefficientwise to a ring homomorphism A_B -> A. It commutes with matrix addition, multiplication, tensor contraction and effect pairing. If a=sum_{j=0}^3 b_j u^j, the formula

    Poss(a) = b_0 OR b_1 OR b_2 OR b_3

satisfies v(Poss(a))=1 exactly when the evaluated A coefficient is nonzero. Thus the augmented symbolic system can compile the chosen modal support test, once a tensor/effect contract has separately been supplied. QED.

This is a constructive sufficient bridge, not a claim that Paper B already determines that contract canonically. The use of OR for the **nonzero test** is essential: XOR of coefficient bits would test parity, not nonzeroness. A symbolic representation of all oracle-dependent amplitudes is also not a free query readout of the answer.

The clean architecture is therefore

    Boolean formulas / reversible oracle synthesis
                       |
                       v
    linear amplitude dynamics over F2 or the specified A-module
                       |
                       v
    separately declared complete modal effect/instrument semantics.

Paper B supplies the first layer and valuation-compatible Boolean reasoning. The modal state space, tensor product, admissible effects and instruments are additional model choices.

---

---

## Theorem I1: the displayed Bell support has no faithful real nonsignalling probabilities

Take the Bell state with coefficient matrix I_2 and local effects

    Z=((1,0),(0,1)), X=((1,1),(1,0)), Y=((0,1),(1,1)).

In outcome order 00,01,10,11, the nine support strings are

| Alice / Bob | Z | X | Y |
|---|---|---|---|
| Z | 1001 | 1110 | 0111 |
| X | 1110 | 0111 | 1001 |
| Y | 0111 | 1001 | 1110 |

Number probabilities context-major from 0 through 35. Normalization, nonsignalling and the twelve forbidden events imply the three exact equations

    p_4+p_27=0,       p_11+p_12=0,       p_19+p_32=0.

All six entries are modally possible. Nonnegativity therefore forces each of them to zero, contradicting faithfulness, which requires positive probability for every possible event. Exact rational combinations of the constraint rows proving these equations are delivered in `independent_probability_certificate.json`. QED.

If faithfulness is dropped, the remaining constraints have a unique nonnegative solution: eighteen entries equal 1/2 and all others are zero. Its Z/X correlation subtable has

    E_ZZ=+1, E_ZX=-1, E_XZ=-1, E_XX=-1,
    E_ZZ-E_ZX-E_XZ-E_XX=4.

This weak completion is not a complex-quantum correlation either. Perfect correlations would require A_Z psi=B_Z psi and A_Z psi=-B_X psi, while the other two require A_X psi=-B_Z psi and A_X psi=-B_X psi. Together they force B_Z psi=-B_Z psi and hence psi=0 over characteristic zero. The same argument applies to a purification of a mixed realization. This is an obstruction for this support experiment, not a claim that no Boolean subtheory can ever carry probabilities.
