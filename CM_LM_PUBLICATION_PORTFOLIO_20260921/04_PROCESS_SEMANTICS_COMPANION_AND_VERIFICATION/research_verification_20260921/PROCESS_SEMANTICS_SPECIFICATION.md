# Closed semantics and its limits

Research date: 21 September 2026. Status: an explicit closed **binary modal completion**, with a faithful single-system ring interface and a nonmonoidal support encoding. This is not a closed completion preserving every shared-ring operation. Proofs appear in THEOREM_COUNTEREXAMPLE_LEDGER.md. The ambient field construction has substantial prior art in Schumacher--Westmoreland, *Almost quantum theory*, §§3--4 (https://arxiv.org/html/1204.0701v1). The interface below is derived explicitly rather than inferred from a matrix embedding.

The local 20 September process-semantics package and its reviewed technical companion already contain this construction. This run preserves those files and supplies a new verification/reconciliation snapshot, not a replacement theory.

## 1. Systems and states

An operational carrier is a finite-dimensional vector space V over k=F2. The tensor unit is k. A pure preparation is a nonzero vector; a general preparation is a nonzero linear subspace S <= V. The zero subspace is an impossible branch, never a deterministic preparation. Mixture is linear span, not vector addition. Different classical alternatives do not XOR each other away.

An A-labelled carrier V_m is the underlying binary space of A^m, dimension 4m, with multiplication by u recorded as an operator N_m. A native 2x2 CM is neither V_m nor its operator algebra. The chosen cyclic CM coefficient order motivates A but is not an operational postulate.

## 2. Independent preparation and composition

Independent systems use V tensor_k W. Independent mixed preparations use the span of s tensor t. This is nonzero whenever both inputs are nonzero: pick nonzero s,t and separating binary functionals. Associativity, symmetry and the unit laws are the usual field-tensor isomorphisms. Independent copies have independent scalar actions. In k copies the coefficient algebra is

R_k = A tensor_k ... tensor_k A = F2[u_1,...,u_k]/(u_1^4,...,u_k^4),

not A with all u_i identified. R_k is local but is not a chain ring for k>1.

## 3. Processes, effects and complete instruments

A branch V -> W is a finite linear subspace K <= Hom_k(V,W). Its action is K(S)=span{T s:T in K,s in S}. A finite list of outcome-labelled branches K_i is a complete instrument iff the joint evaluation map into a direct sum of copies of W is injective; equivalently intersection_{i,T in K_i} ker(T)={0}. Unequal output carriers W_i are allowed by taking the appropriately typed direct sum. Choose any basis of each K_i to check this condition.

Composition uses the span of all products of branch maps; parallel composition uses the span of tensor products. This retains a concrete process representation even when different representations have the same operational action. A reversible pure process is an invertible binary map. A selected linear filter T is admissible as one branch of the complete instrument {T,I}; the two outcomes are classical alternatives, not a coherent sum. This asserts possible success only; there is no success probability or fairness guarantee.

A terminal effect is a subspace E <= V*. It is possible on S exactly when some e(s) is nonzero. A terminal measurement is complete iff its effect subspaces together span V*. A dual basis is a special case. The deterministic discard effect is all of V*.

## 4. Conditioning, discard and communication

Upon outcome i retain the nonzero subspace K_i(S) in its declared output carrier. Zero outcomes cannot occur. On a correlated reference, act with id tensor T before taking span; never replace a joint state by a product of its marginals.

For a state S <= V tensor W, discarding V gives span{(e tensor id)s:e in V*,s in S}. Forgetting a classical outcome gives the span of its branch states. A classical register is a finite set of labels with a tuple of conditional subspaces; merge labels by span, and copy or transmit labels by ordinary finite relations/functions. Subsequent instruments can depend on a communicated label. Classical communication does not transmit a coefficient vector or license coefficient inspection.

Every complete instrument has at least one nonzero branch on every nonzero state, including with a reference. This follows because its stacked binary map is injective and field tensor preserves injectivity. Tensoring two complete instruments and composing adaptive complete instruments preserve this property. Finite instrument trees, mixtures and discards therefore form a closed theory. Local complete instruments leave the remote unconditional marginal unchanged: the rows of their stacked maps span the full local dual, so taking all conditional slices gives the same remote span. This proves possibilistic no-signalling, not a real probability rule.

## 5. State equivalence and units

In the full ambient theory, mixed states are equivalent exactly when their subspaces are equal: a separating functional distinguishes unequal subspaces. Over F2 there is no nontrivial scalar-ray quotient for pure vectors. An A-unit is generally a nontrivial binary operator. For example, on V_1, 1 and (1+u) are distinguished by the effect extracting the u coefficient. Thus global A-unit multiplication is detectable with full binary effects.

With only A-linear operations and coarse zero/nonzero A-valued readout, unit multiples give identical supports. That is equivalence relative to that restricted observation contract; it is not equality of raw coefficients. An unknown unit correction is insufficient for a raw-vector recovery claim. Effects from the full ambient theory break this restricted equivalence.

## 6. Ring gates and the functorial boundary

Restriction of scalars U: finite A-modules -> finite binary vector spaces sends a module and a map to their underlying vector space and map. It is faithful, additive, and preserves identities, composition and direct sums. Its natural lax monoidal comparison is the balanced quotient

q_{M,N}: U(M) tensor_k U(N) -> U(M tensor_A N),

with unit map k -> U(A), 1 -> 1. Associativity follows from the universal balancing relations. It is not strong monoidal: the unit dimensions are 1 and 4; for A^m,A^n the two tensor dimensions are 16mn and 4mn. q kills u^3 tensor_k u. A ring preparation A -> M is sent to a map U(A) -> U(M), not directly to a binary preparation k -> U(M); precomposition with 1 selects the corresponding vector. This extra distinction prevents an invalid state-preservation assertion.

For one labelled carrier, U embeds End_A(A^m)=M_m(A) faithfully, and embeds GL_m(A) into GL(4m,2). It does not preserve balanced separability, nonzero tensor preparation or arbitrary contextuality/resource contracts.

## 7. Explicit support-preserving bipartite encoding

Fix the u-basis and define the Frobenius functional tau(a)=[u^3]a and

Omega=sum_{r=0}^3 u^r tensor_k u^{3-r}; Delta(a)=(a tensor 1)Omega.

Delta is injective and (x tensor y)Delta(a)=Delta(xay). For C=(C_ij) in M_{m,n}(A), define

E(C)=sum_{i,j,r} (e_i u^r) tensor_k (e_j C_ij u^{3-r}).

Every nonzero C gives a permitted pure binary preparation, including nonprimitive C. If x is an A-linear row, its binary block map L_x:V_m -> U(A) has four output coordinates. Then

(L_x tensor L_y)E(C)=Delta(x C y^T).

For each B in GL_m(A), the family of block rows L_{B_i} is a complete instrument. Its output retains a four-dimensional coefficient register. If that register is discarded, each coarse outcome has effect subspace span of its four component binary functionals. The resulting two-party coarse supports are **exactly** P01's supports, including all 192 unordered projective bases for m=2. No probabilities are introduced.

This is an encoding of resources and selected measurement tables, not a monoidal embedding of the shared-A process theory. E of a shared product need not be a binary product: E(1) on A tensor A is Omega of binary Schmidt rank 4. Discarding Alice's coefficient register after her coarse outcome generally leaves an A-generated binary subspace, not P01's single raw conditional vector. Even for C=(1), the Bob marginal is U(A), a four-dimensional mixed state.

## 8. Precisely restricted resource tasks

**One-copy pure conversion task:** supplied resources E(C); local selected filters U(F),U(G), with F,G arbitrary A matrices of declared sizes; complete each with an identity failure-labelled branch. Only nonzero successes count. Reversible equivalence uses GL(A). No free additional bipartite resources, coefficient measurements, or discard/reprepare encodings are admitted to this conversion task. Every finite local adaptive branch is still a product of the specified filters; the conversion preorder below is exact for this task. Ambient binary operations are available only when a different task explicitly admits them.

**Full-label k-copy conversion task:** local carriers are free R_k modules; allowed selected filters are R_k-linear and the target is E_{R_k}(I_d) over this same R_k. Tensoring tasks introduces new labels and forms R_{k+l}; it does not identify labels. This task has the exact unit-rank criterion in the theorem ledger. An output on a single A carrier, discarding phase labels, catalytic resources, and arbitrary free ancilla assistance define different conversion tasks. No complete classification of that larger generated resource theory is claimed.

With resolved coefficient measurements before disposal, the earlier review already gives a two-copy route to a single-register E_A(I_2), rerun here as T17. Thus existence of any such activation is not an open milestone. Forgetting the selected outcomes in that witness produces a mixed state. The unresolved question concerns suitably justified broader conversion classes, not the existence of this known protocol.

**Matched P01 coding:** Alice encodes by GL_d(A). After transmission, Bob's decoder on E(M_d(A)) is the transported action of one GL_{d^2}(A) map on coefficients, extended to a binary invertible map on a chosen complement. Outcomes are the d^2 coefficient blocks, discarding their internal binary coordinates. This is a well-defined complete binary experiment and reproduces dh exactly. It is a restricted task embedded in the closed ambient theory. Its d-message baseline is not the unrestricted 4d-dimensional binary carrier baseline.

The distinctions between a closed ambient process theory, a closed list of allowed finite instruments, and an optimization over a frozen resource task are deliberate. The normalizer theorem does not license additional gates in any task without restating that task.

## 9. Recovery types

Raw exact recovery means the corrected linear map is literally I on the promised domain, including its references. Recovery on A/(u^l) means equality of induced quotient maps; lifting its answer need not recover an A vector. Recovery modulo Ann(a) means identifying inputs with the same image under multiplication by a. The isomorphism A/(u^{4-a}) -> (u^a), [x] -> u^a x, preserves those typed data only. It cannot be inverted on all of A, and its inclusion into A is not preserved as a monomorphism by balanced tensoring with arbitrary modules.

## 10. What has and has not been resolved

There is a fully defined preparation/conditioning/composition theory that retains the selected ring support tables and a useful restricted conversion hierarchy. Its ambient semantics is established binary modal theory. There is no construction here preserving simultaneously all nonzero shared-A states, all nonzero-effect outcomes, balanced independent composition and ordinary independent possibility. The scalar obstruction rules that conjunction out. No Born rule, physical implementation, hardware prediction, algorithmic speedup, or undeclared communication advantage is asserted.
