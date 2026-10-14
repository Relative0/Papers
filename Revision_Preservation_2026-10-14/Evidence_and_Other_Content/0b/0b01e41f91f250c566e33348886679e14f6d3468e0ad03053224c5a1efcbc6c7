# Capability and dependency theory for Boolean modal information
## CM/LM, finite fields, the rotation algebra, and two inequivalent tensor models

**Research date:** 18 September 2026  
**Status:** Mathematical audit and research dossier, with independently implemented exact tests.  
**Priority status:** Results derived here are not thereby certified as new to the literature. The supplied chain-ring classification is imported background, not a new discovery of this investigation.

## Executive findings

The useful theory is not an undifferentiated list of quantum analogies. It has three separable layers:

1. Linear state spaces, tensor products and sufficiently rich basis measurements already produce modal complementarity, nonseparability, strong Bell support contextuality, no cloning, teleportation and dense coding over F2. A rotation phase, zero divisors, probabilities and an inner product are unnecessary for these existence results.
2. The rotation restriction introduces additional invariants: the nilpotent valuation, Smith factors, a restricted measurement family, and distinctions between shared-module and literal-register resources. These distinctions disappear partly, but not entirely, when the allowed local group is enlarged.
3. Fourier-based algorithms do not follow from these protocol capabilities. Exact one-query Deutsch and Deutsch-Jozsa fail in the declared characteristic-two query model. Exact Bernstein-Vazirani requires n queries, not one. Genuine phase kickback exists, but its characteristic-two eigenvectors do not supply an invertible Fourier basis.

Two especially informative results derived and tested here are:

- **Leading-layer dense-coding theorem.** For a nonzero d-by-d resource over a finite commutative chain ring, with local invertible encoding and a complete ring-linear joint basis readout, the maximum number of perfectly distinguishable codewords is **d h**, where h is the multiplicity of the lowest Smith valuation. Universal exact teleportation instead requires all Smith factors to be units. Thus nilpotent resources can be dense-coding capable but not universally teleportation capable.
- **Characteristic-two query obstruction.** The linear spans of oracle-dependent output states obstruct exact discrimination. For Bernstein-Vazirani, q queries produce states lying in a span of dimension at most sum_{j=0}^q binomial(n,j); distinguishing 2^n strings therefore requires q >= n.

An important positive control prevents overgeneralization: the known Willcock-Sabry one-query modal algorithm for UNIQUE-SAT works. It was reproduced for every promised function with 1 through 6 input bits. The negative results are algorithm- and query-contract-specific, not a claim that modal computation can never have a query separation.

The principal foundational warning remains: **the shared A-module construction with all nonzero vectors is not closed under independent preparation**, while retaining only unimodular vectors is not closed under conditioning. It defines meaningful support experiments and algebraic protocols, but not, without further choices, a completed physical operational theory.

---

# 0. Sources, reproduction, and evidence boundaries

The three supplied ZIP archives were readable. Their hashes and entry counts are recorded in `data/input_archives.json`. Primary sources inspected included the correctness audit's LaTeX manuscript, its independent source code, the historical rotation-phase and shared-module definitions, the adversarial review's formal theorem proofs, and the source and output files behind the claims.

Paper B, **Operator-Level Boolean Computation with Correspondence Matrices**, was not bundled in these ZIPs. Its complete 19-page parsed text was retrieved from the user's Library and inspected, especially Sections 2 and 8 and Appendix A. Its raw PDF could not be materialized and its requested page image was unavailable; the mathematical text was readable. No raw-byte hash or PDF image inspection of that Library copy is claimed.

Paper B explicitly treats logical pairing as Boolean relationship extraction, not a physical measurement or Born rule. Its coefficient linearity, valuation theorem, one-hot selection, typed operator fusion and explicit-output size bounds are background here [B].

Two kinds of reproduction are distinguished:

- The supplied audit's `audit_models.py` and `audit_protocols.py` were rerun. Their core stages completed. The supplied review's `independent_extensions.py` was also rerun, including 22 ring/dimension campaigns.
- Four **new implementations**, `laboratory.py`, `ablations.py`, `bridges_phase.py`, and `two_setting_theorem.py`, import no supplied code. In particular, they use polynomial coefficients in u rather than the supplied audit's R-coefficient encoding. They independently enumerate resources and measurements, solve support constraints, construct protocols, test oracle obstructions and produce exact rational probability certificates.

The whole historical test runner and a later exhaustive restrictions driver did not finish within their imposed time limits. Old aggregate test totals were not counted as fresh results. A timeout is not a mathematical counterexample, and no claim of rerunning every historical test is made.

"Exhaustive" below always refers to a specified finite domain. A proof, rather than an enumeration, is used for arbitrary dimensions, arbitrary ancillary systems and unbounded query counts. Exact scopes, timings, algorithms and output filenames are in the four `*_metrics.json` files and the computational ledger near the end of this report.

---

# 1. The operational contracts

## 1.1 Models and dimensions

| Label | Objects and composition | Dynamics and readout | Essential distinction |
|---|---|---|---|
| F | Nonzero vectors in F2^d; composite F2^d tensor_F2 F2^e | Invertible linear maps; dual-basis effects; outcome possible iff coefficient is nonzero | Ordinary modal finite-field theory, not complex quantum theory |
| R | A = F2[R] = F2[u]/(u^4), u=1+R | Multiplication by units and, after choosing multiple arms, matrices over A | An algebra of operators; not by itself a state/measurement/tensor theory |
| S | A^m, with shared tensor over A; one logical carrier A^2 | GL_m(A); complete primitive projective bases; nonzero A coefficient means possible | One phase scalar is shared in tensor contraction; nonzero preparations can tensor to zero |
| L | Literal independent registers; one logical-plus-phase carrier F2^8; composites over F2 | Either all field-linear gates/readouts, or explicitly stated A-equivariant/coarse restrictions | Each carrier has its own four-dimensional phase register |
| LM | Boolean formulas modulo equivalence and formula-valued matrices | Boolean valuation, logical pairing, symbolic computation | A classical symbolic layer. It does not automatically postulate modal states or measurement |

For n logical carriers, the shared construction has binary dimension 4*2^n. The literal construction has dimension 8^n. They are not different notations for the same tensor product.

F and unrestricted L belong to the same mathematical finite-field family. L matters because it specifies a larger local carrier, an internal phase representation, and a restricted group inherited from A.

For finite-field states over F2 there is no nontrivial scalar projectivization. For ring states, unit multiples may be identified for support-only purposes. Nonunit multiples must not be identified: they can change annihilators, ranks, and protocol performance. Enumerated state counts in this package count **raw vectors**, not unit-projective state classes.

## 1.2 What a basis measurement means here

For G invertible, its rows r_i are effects. The outcome i is possible on psi when r_i psi is nonzero. A compatible complete instrument can use

    P_i = G^{-1} e_i e_i^T G.

Then P_i P_j = delta_ij P_i and sum_i P_i = I. These are algebraic projectors, generally not self-adjoint projectors in a positive Hilbert space. Over A, a nonzero branch coefficient may be a nonunit; it cannot automatically be divided away.

In the shared two-outcome system, rows are primitive, are quotiented by unit scaling, and the two outcomes can be treated as an unordered basis. There are 24 primitive projective rays and 192 unordered projective bases. A basis is a measurement setting. We do not add an unstated Kochen-Specker rule identifying the choices assigned to a ray across all settings containing that ray.

For literal L, an A-valued effect is a map F2^8 -> F2^4. Calling its outcome merely nonzero is a **block-coarse measurement**, not a complete fine-grained scalar measurement of the independent phase registers.

## 1.3 Exactness and a query

An exact modal algorithm must return the correct answer for **every possible recorded outcome**. It may not inspect its whole support at no cost, discard a possible unsuccessful branch, assume that a possible event will eventually occur, or assign an unprovided probability to it.

A standard Boolean query is the single application of

    U_f |x,y> = |x,y xor f(x)>.

The oracle may act coherently on a state vector, just as a query primitive does in a quantum query model. Preparing or evaluating the truth table of f is not free. A more general pointwise oracle used in the no-go results is

    O_f = sum_x |x><x| tensor G_{f(x)},

where G_0 and G_1 are fixed invertible linear maps. This includes standard bit queries and a separately declared controlled-rotation oracle. It excludes oracles whose definition already contains a global answer such as parity(f).

The proofs allow arbitrary f-independent ancillary spaces and linear processing. Their final-readout form covers complete linear instruments as well: record all branch histories in a direct sum. Completeness means that this combined linear map has no nonzero vector in its common kernel. Postselection that throws away possible branches is outside the exact contract.

## 1.4 Meaning of "minimum"

Necessary conditions are always relative to a declared task and operational contract. The constructions show that certain ingredients are **unnecessary for existence in the compared models**. They do not classify every generalized probabilistic or categorical theory. In particular, tensor structure in a theorem means the specified non-Cartesian composition, not that all possible process theories must use a field tensor product.

---

# A. Capability map

| Phenomenon | Conventional quantum notion | Exact Boolean/modal analogue and result | Important missing feature |
|---|---|---|---|
| Superposition | Linear combination of amplitudes, with normalization and rays | Nonzero vector addition. F2 already suffices; a state added to itself gives zero, which is not a state | No continuous amplitudes, norm, or constructive intensity |
| Phase and relative phase | Scalar unit-modulus factors; relative phases become observable after mixing | F2 scalar phase is trivial. A has units, including R of order four; relative diagonal units plus a shear change support | R is unipotent, not a diagonalizable complex quarter turn; phase depends on coarse readout |
| Phase kickback | A target eigenvalue becomes a control-dependent phase | In shared A-coefficient theory, Boolean XOR kicks back z=R^2 using (1,z); R uses a four-level cyclic target and a separately declared oracle | Eigenvectors do not form a Fourier basis; standard bit flip cannot have a primitive R-eigenvector |
| Interference | Amplitudes combine, sometimes destructively | W^2=I and W diag(I,R^k) W(v,0)=(v,v+R^k v). Destructive cancellation is exactly XOR cancellation | No amplitude magnitude, fringes with intensities, or Born statistics |
| Complementarity | Incompatible observables and incompatible outcome statistics | Distinct complete dual bases Z, X, Y of F2^2 already give deterministic versus ambiguous outcomes | These are not Hilbert mutually unbiased bases; they can share effect rays |
| Nonseparability | A pure state is not a product across a specified partition | Over a field, coefficient rank >=2. Over the chain ring, at least two nonzero Smith factors | S and L have different products and different separability tests |
| Bell support nonlocality | No local model reproduces the pattern of possible events | A finite support model is nonlocal iff some possible event fails to extend to a global assignment | No Bell expectation value, violation magnitude, or experimental probability |
| Hardy logical contextuality | A possible event and several zero probabilities contradict local predetermined outcomes | Uniform two-setting Hardy witnesses exist for two nonzero Smith factors; unequal valuations yield logical but not strong contextuality with all A-bases | This exact pure-state intermediate stratum depends on ring valuation and measurement contract |
| Strong contextuality | No global assignment is compatible with the support | Already present in F2 Bell states with Z, X, Y; over complete chain-ring bases it is determined by lowest-valuation multiplicity >=2 | Not a generic consequence of a four-cycle phase group |
| GHZ contradiction | All-or-nothing multipartite constraints, conventionally a four-context parity argument | The state 000+111 has a no-global-assignment support table for three local F2 bases; phase-expanded literal GHZ has the corresponding coarse table | For every state in the binary contracts studied here, at most two settings per site always admit a global assignment (R1b); the conventional two-setting GHZ pattern is unavailable |
| No cloning | No physical map copies an arbitrary unknown pure state | Linearity and tensor composition forbid v -> v tensor v on all nonzero F2 vectors when d>=2 | Classical descriptions and basis labels remain copyable |
| No deleting | Reversible dynamics cannot erase one unknown copy without moving the information elsewhere | Reversible deletion with a fixed blank and no information-bearing environment is impossible | A noninvertible diagonal contraction deletes duplicated F2 vectors algebraically, but is not automatically a complete deterministic operation |
| Teleportation | Entanglement plus classical feed-forward transfers an unknown state | Complete invertible-matrix effect bases and inverse branch corrections give exact protocols; universal resource must be invertible | No probabilities or fidelity. Literal 8-dimensional teleportation needs 64 outcomes and unrestricted phase operations beyond the native A-linear analyzer |
| Dense coding | Entanglement increases distinguishable messages for a transmitted carrier | Field resource of rank r: d*r invertible-orbit codewords. Shared chain ring: d*h block messages | Exact distinguishability is not Shannon capacity. Nilpotent dense coding need not imply universal teleportation |
| Entanglement swapping | A joint measurement connects two remote entangled resources | Coefficient contraction M E N; invertible resources and invertible reshaped effects preserve full rank, with local correction | No heralding probability; the allowed analyzer must be specified |
| Remote state preparation | A known target state is prepared remotely using shared correlations | Over a field, a heralded branch prepares phi iff phi is in im(M^T); over A the allowed projective effect must have a primitive preimage | Possibility is not guaranteed occurrence; no optimal communication advantage is established |
| Error correction | A code reverses a declared error channel on an unknown state | An exact distinguishable-syndrome construction exists when error images are injective and form a direct sum; a 3-mobit repetition example works coherently | No noise probabilities, thresholds, CPTP channels, or general Knill-Laflamme replacement |
| Stabilizer-like evolution | Pauli normalizers admit efficient state/effect tableaus | A is a principled equivariant linear algebra, and a genuine Pauli-like finite group exists; its actual normalizer is much smaller than the native gate set | Finiteness or matrix linearity does not imply simulation polynomial in the number of carriers |
| Oracle algorithms | Coherent queries, phase processing and readout yield task-dependent query bounds | Reversible Boolean oracles exist. Deutsch/DJ one-query forms fail; BV needs n queries; known modal UNIQUE-SAT succeeds in one query | A CM implementation on a classical machine is not thereby a faster physical oracle |

Prior modal results in the first, fifth, sixth, ninth, eleventh, thirteenth and fourteenth rows are established background [SW2012, JOS2011]. Exact tests here validate the current conventions rather than establish priority.

---

# B. Dependency matrix and ablations

## B.1 Sufficient structures and conditional necessities

The entries below concern existence or the stated exact task, not universal necessity across all process theories.

| Capability | Sufficient structure in this laboratory | Necessary within the stated task | Ingredients not needed for the displayed construction |
|---|---|---|---|
| State addition and cancellation | F2-vector space, nonzero-state convention | Addition and access to overlapping contributions for cancellation | R, tensor, zero divisors, probabilities, inner product |
| Relative rotation interference | Two arms, reversible shear, nontrivial relative R-action | Mixing before readout; a phase that does not act identically on the chosen input | Tensor product, probabilities, dagger |
| Modal complementarity | F2^2 and more than one complete dual basis | More than the single fixed computational measurement in this construction | R, nilpotents, probabilities |
| Bell/strong support contextuality | Field tensor product, rank-two state, the three F2 bases | A nonproduct resource for the compared complete field/chain-ring models; an adequate measurement scenario | R, zero divisors, nonlinear oracle, probability, dagger |
| Pure-state logical-not-strong stratum with all chain-ring bases | Two unequal nonzero Smith factors | A nontrivial valuation stratum within this complete-basis pure-state family | Length four and order-four R; length-two dual numbers already suffice |
| Universal exact teleportation | Tensor, full-rank resource, complete invertible effect basis, conditional inverse corrections | Invertible resource and implementable complete analyzer/corrections | R, nilpotents, inner product, probability |
| Shared dense advantage | A d-by-d chain-ring resource with leading residue rank h>=2 | h>=2 under ring-linear invertible encoding and complete block readout | Unit Smith factors; universal teleportation |
| Field dense advantage | Rank r>=2 and unrestricted invertible encoding/joint readout | r>=2 under the declared codebook contract | R, nilpotents, probability |
| No cloning | Linear dynamics, tensor composition, e_i,e_j,e_i+e_j allowed | Those state/dynamics assumptions; description copying is a different task | Reversibility, probabilities, dagger |
| Reversible no deleting | Injectivity plus tensor-span comparison and fixed blank | Reversibility/no information-bearing discarded environment | Probability, dagger |
| Exact distinguishable-syndrome correction | Linear embedding and direct-sum injective error images | The direct-sum condition if distinct error labels must be retained | Inner product, probabilities, R |
| Oracle compilation | Classical Boolean circuit, basis-state permutation embedding | Correct coherent implementation and honest accounting of f-evaluation | Nonlinear evolution of amplitudes, R, probability |
| Standard C2^n Fourier algorithm | An invertible character transform would suffice | Enough distinct characters and an invertible transform | These requirements are not supplied by A or F2 |
| Born/amplitude amplification | A suitable probabilistic/norm structure, not specified here | A replacement operational definition is needed before claiming a probability gain | Mere modal support cannot define the usual performance criterion |

"XOR" is not a universal necessary condition for teleportation or contextuality; complex quantum theory and other categories are immediate reasons not to say that. Its role here is that the smallest compared field already supplies sufficient linear algebra.

## B.2 Actual structural ablations

| Change | Result | Evidence and scope |
|---|---|---|
| Replace A by F2 and retain tensor, GL and all dual bases | Bell strong contextuality, no cloning, exact teleportation/dense coding and the repetition correction survive | Proofs; independent Bell and protocol checks |
| Remove R while retaining F2 mixing and tensor operations | The preceding features survive; specifically rotation-sensitive interference is no longer available | Embedded F2 witnesses; no claim about removing the only permitted mixer |
| Remove all nonmonomial mixing and permit only basis states, basis permutations and computational readout | A reversible classical subtheory remains | Basis-state invariance proof |
| Replace length-four A by F2[epsilon]/epsilon^2 | Unequal-valuation logical contextuality and nonprimitive dense/teleportation separation already occur | General chain-ring theorem; supplied extension campaign rerun |
| Retain a literal independent tensor instead of balancing over A | Independent nonzero preparations no longer annihilate; shared and literal separability disagree | Three explicit counterexamples in `independent_tensor_counterexamples.json` |
| Enlarge literal local operations and readout to all GL_8(F2) and field bases | Smith distinctions collapse to binary rank. Every rank>=2 pure resource is strongly contextual with all bases | Rank classification and field specialization of the support theorem |
| Restrict both local preprocessing and measurement bases to O_8(F2) intersect GL_2(A) | There are 512 gates and 4 bases; the identity-resource Bell support becomes local. The canonical D(0,1) still has four unextendable events | Exhaustive 256 assignments for each of 14 canonical resources, not an enumeration of every state under this smaller group |
| Demand transpose-orthogonal teleportation corrections | No complete rank-one exact universal analyzer exists, for any invertible resource and d>=2 | Orthogonal-span theorem; independent O_4 span calculation |
| Substitute an alternating form and change the gate contract accordingly | A two-mobit symplectic alternative does admit complete exact teleportation analyzers; 72 ordered examples among 360 candidates | Exact enumeration using J_2 and J_2 tensor J_2. Not a claim that all native W/CNOT/R gates preserve that form |
| Remove nonlinear Boolean truth logic but retain only affine basis-label reversible gates | The directly compilable Boolean oracles are affine | Gate closure on basis labels. This ablation must not silently retain all GL of the amplitude space, since all GL already contains arbitrary oracle permutations |
| Add support-faithful nonnegative real nonsignalling probabilities to the displayed Bell table | Impossible | Exact rational zero-sum certificates force six modally possible events to probability zero |
| Remove the third setting at every site in the displayed GHZ experiment | No strong subscenario remains; all 27 two-setting subscenarios remain logically contextual | Exhaustive 64 assignments per subscenario |

A measurement restriction alone is not an operational restriction if arbitrary preprocessing can rotate it back into all measurements. The orthogonal row above therefore restricts both the local gate group and its induced basis family. Also, full Smith equivalence need not preserve the four-base family; its data describe canonical representatives only.

---

# C. Algorithm suite and formal query results

## Theorem Q1: exact modal discrimination is a direct-sum condition

Let S_i be sets of nonzero states in a finite-dimensional vector space over a field, and U_i=span(S_i). A complete linear readout can distinguish the labels i with certainty for every possible outcome only if sum_i U_i is a direct sum. Conversely, an invertible basis readout can distinguish the labels when this direct-sum condition holds.

**Proof.** Correctness assigns disjoint sets of readout coordinates to distinct labels. The image of U_i is contained in the corresponding coordinate subspace. A complete readout is injective when all branch maps are collected in a direct sum; hence a nontrivial dependence across label subspaces is impossible. Conversely, choose a basis for each U_i, concatenate these independent bases, and extend to the whole space. Readout in the resulting dual basis identifies the label. For two labels this reduces to U_0 intersect U_1 = {0}. For one state per label it reduces to linear independence. QED.

The same necessary condition applies to ring models after faithful binary expansion. Thus failure even with arbitrary field-linear readout implies failure under the narrower A-linear block readout.

## An essential LM/readout ablation

The following lower bounds are **not** claims about unrestricted classical inspection of a state-vector description. For example, prepare |0,0>+|1,0> and apply the standard U_f once. The resulting vector is |0,f(0)>+|1,f(1)>. Reading its two target-one coefficient bits as classical data determines f(0) xor f(1) immediately. What is unavailable in the modal contract is deterministic access to those coefficient bits, not the existence of the vector.

More generally, one vector-oracle interaction on sum_x |x,0> encodes the entire truth table in the coefficient list. Full coefficient inspection gives Deutsch-Jozsa and BV answers as well. A classical machine granted that same batch-vector oracle interface also obtains those answers; a simulator using an ordinary point oracle evaluates f at the relevant addresses rather than receiving exponentially many answers free. LM symbolic computation may inspect formulas or stored coefficients, but doing so is a different readout resource from a physical/modal outcome.

This ablation was tested independently for all four Deutsch functions, all constant/balanced promised functions for n=1,...,4, and all BV strings for n=1,...,8. It is included to expose a query-contract change, **not** to claim an alternative modal speedup. See `description_readout_ablation.json`.

## Theorem Q2: Deutsch needs exactly two queries

For the pointwise oracle O_f with fixed invertible G_0,G_1 over characteristic two, no exact one-query procedure can determine f(0) xor f(1), regardless of f-independent ancillary dimension or linear preprocessing/postprocessing.

**Proof.** Write the prepared state in the two address sectors as (a_0,a_1), allowing arbitrary target and spectator degrees of freedom. The four post-query states v_00,v_01,v_10,v_11 obey

    v_00 + v_11 = v_01 + v_10
                 = ((G_0+G_1)a_0, (G_0+G_1)a_1) = w.

If w is nonzero, the constant and balanced spans intersect nontrivially. If w is zero, both sector differences vanish, so all four states coincide. Either case violates Q1. Any complete linear subsequent instrument preserves the relevant obstruction. Two ordinary basis-state queries suffice by storing and XORing the two answers. QED.

This is stronger than saying that the conventional Hadamard matrix becomes singular. It excludes another one-query solution under the same pointwise oracle contract, including a pointwise controlled R-oracle.

The independent finite test examines every nonzero preparation in dimensions 4 and 8: 15 states without a spectator and 255 with a two-level spectator. It does not brute-force arbitrary ancilla dimension; the proof handles that.

## Theorem Q3: Deutsch-Jozsa has no exact one-query solution here

For n>=2, partition the N=2^n addresses into four equal sets A,B,C,D. The three functions with supports A union B, A union C, and B union C are balanced and have pointwise XOR zero. The oracle depends affinely on its Boolean control bit, so in characteristic two

    O_f1 + O_f2 + O_f3 = O_0.

For any nonzero prepared state, the constant-zero post-query state is therefore in the span of the balanced post-query states. Invertibility ensures that it is nonzero. Q1 forbids exact distinction. The n=1 case is Q2. QED.

State preparation by shears, the ordinary oracle, and any complete linear readout are all permitted in this no-go result. There is no hidden cost argument: the one-query mechanism itself fails.

A deterministic classical upper bound N/2+1 is inherited by basis-state execution. This report does **not** prove that upper bound optimal for multi-query modal computation. The supported general bounds are 2 <= Q_exact <= N/2+1, with equality 2 when n=1. Conventional randomized bounded-error comparisons require an external probability model and are a different benchmark.

## Theorem Q4: exact Bernstein-Vazirani requires n queries

For f_s(x)=s dot x over F2, an exact q-query characteristic-two linear modal algorithm requires q>=n. Basis-state queries at e_1,...,e_n attain n.

**Proof.** Since the dot product is computed in characteristic two, the oracle matrix is affine-linear in the secret bits:

    O_s = O_0 + sum_j s_j A_j.

After q queries, each component of the final vector is a multilinear polynomial of degree at most q in s_1,...,s_n. Thus all 2^n possible final states lie in the span of at most

    sum_{j=0}^{min(q,n)} binomial(n,j)

coefficient vectors. If q<n, this is less than 2^n. Q1 says the 2^n exactly distinguishable secret-dependent states must be linearly independent, a contradiction. Ancillas only enlarge the ambient coefficient vectors, not their number. Complete adaptive linear branches can be recorded in a direct sum and satisfy the same degree bound. QED.

This is a characteristic-two specialization of the polynomial-method architecture, not a claim to invent polynomial query lower bounds [BBCMW2001]. In complex quantum computing, the real/complex polynomial representing XOR is not degree one in the secret bits; hence the argument does not forbid the conventional one-query BV algorithm.

**Consequence:** the fact that the hidden function is F2-linear is not a reason to expect BV to work with F2-valued amplitudes. It is exactly what makes this lower bound strong.

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

## Fourier/Simon boundary

Every multiplicative character C2^n -> F2^times is trivial. Passing to F_{2^k} does not repair this: its unit group has odd order. Over A there are nontrivial involutory units, but every unit reduces to 1 modulo u. Any square character matrix for a nontrivial Boolean group therefore reduces to an all-ones matrix and cannot be invertible over A.

This is a modular-character obstruction, not a theorem that Fourier transforms over finite index sets never exist. Standard finite-field-indexed quantum Fourier transforms use a different amplitude field, typically complex characters. Odd-order groups can also have invertible character transforms in suitable characteristic-two extension fields when their order is invertible and the necessary roots exist. Neither observation supplies the missing C2^n transform here.

For Simon's problem, one may still prepare and condition onto coset states |x>+|x+s>. That is not enough to implement the conventional Fourier sampling algorithm. A fresh exhaustive n=2 search checked all 65,535 nonzero preparations in the 16-dimensional address/output space and all 36 valid standard oracles (three nonzero shifts, twelve output labelings each). **None permits exact one-query recovery of the shift by arbitrary complete field-linear readout.** This finite result has no spectator ancilla and is not an all-size or many-query lower bound.

The standard n=2 coset-state class spans each contain the same nonzero all-ones vector. Thus a fixed finite number of independent coset-state samples cannot guarantee exact discrimination by a complete linear readout: the tensor powers retain that common vector. Conventional probabilistic Simon sampling also does not guarantee success on every finite sample sequence, so this latter observation is not unique to the Boolean theory.

## Grover boundary

The usual marked-state sign flip collapses because -1=1. The usual diffusion operator 2|s><s|-I collapses as well, and the uniform-state normalization 1/N is unavailable for N a positive power of two. More fundamentally, modal support supplies no success probability to amplify and no inner-product angle to rotate.

Nilpotent phases and shears can change support and cancel branches. Calling that "amplitude amplification" would require a new definition and a proof of its operational benefit. No Grover-type speedup is claimed. The known UNIQUE-SAT positive control below also prevents a blanket lower bound on all modal search-like tasks.

## Positive control: the known one-query UNIQUE-SAT algorithm

Willcock and Sabry give a modal algorithm for the promise that f is identically zero or has exactly one satisfying input [WS2011]. Using s=[[1,0],[1,1]] and s^T, it prepares a uniform F2 superposition on the addresses, makes one standard U_f call, applies further shears, and applies controlled NOTs from the output bit to the address bits.

For f=0, the only final outcome is the all-zero string. For a uniquely satisfying function, that outcome is impossible and at least one other outcome is possible. This is exact modal discrimination, not mere inspection of whether an event could occur.

The package implements the published circuit and tests all 132 promised functions for n=1,...,6. The non-oracle gate count is O(n), not literally constant serial time. A deterministic classical point-query algorithm needs N queries in the worst case to distinguish zero from one marked input. The separation is legitimate in the declared coherent modal query model; it is not evidence of an end-to-end speedup of a classical CM evaluator, which must implement the oracle action and manage the state representation.

---

# D. Resource hierarchy

## D.1 Definitions that must not be conflated

For a finite Bell support scenario:

- **Relationally local:** every supported event extends to a global assignment. The union of those assignments reproduces the support.
- **Logically contextual / Bell-support nonlocal:** at least one supported event does not extend.
- **Strongly contextual:** no global assignment exists at all.

Thus Bell-support nonlocality and logical contextuality are the same level under this definition. They should not be drawn as two distinct strict levels. Probabilistic Bell nonlocality is a different notion [AB2011].

All protocol predicates below name the input carrier, encoding group, measurement contract, single-copy requirement and exactness criterion. A state cannot meaningfully be called simply "teleportable" without that information.

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


## Theorem R1b: two binary settings cannot give strong contextuality

Consider any number of F2 mobits, any nonzero pure state, and at most two complete binary basis measurements per site. The resulting support model always has a global assignment. More generally, the same conclusion holds for two-dimensional local modules over any finite commutative local ring with residue field F2, using nonzero-coefficient support.

**Field proof.** Any two distinct local F2 bases share one effect a; write the other effects as b and a+b. Expand the state in coordinates dual to the local pairs (a,b). Choose an inclusion-minimal set S of b-coordinates with nonzero coefficient. At a site outside S, select the shared effect a in both settings. At a site in S, select b in the first setting and a+b in the second. Every context evaluates to a sum of coefficients indexed by subsets of S. The S coefficient is one and all its proper-subset coefficients are zero. Thus every selected event is possible, giving a global assignment. Coincident local bases only make the construction simpler. QED.

**Local-ring proof.** Let J be the radical and choose a nonzero leading layer of the state in J^a/J^{a+1}. This is a vector space over F2. Apply a linear functional on that layer which gives a nonzero F2-valued logical tensor. Reduce each local basis modulo J and apply the field proof. Every selected event has nonzero leading-layer value under that functional, and hence has nonzero original ring amplitude. QED.

This proof also covers literal independent phase registers with A-linear block-coarse measurements: collect their phase coefficients in the finite local algebra F2[u_1,...,u_n]/(u_i^4), whose residue field is F2, and retain the appropriately restricted local coefficients. It does not identify the literal tensor with the single-variable shared A tensor.

Consequently the usual two-settings-per-party GHZ all-versus-nothing support pattern cannot occur in these contracts, regardless of the number of parties. The three-setting GHZ construction is genuinely a different analogue. This does not exclude Hardy/logical contextuality with two settings. The constructive field certificate was checked for all 65,808 nonzero states of 1 through 4 mobits, in every context of the canonical basis pair; coordinate changes cover the other pairs.

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

## Theorem R4: field dense codebooks and restricted literal codebooks

For a rank-r resource M in M_d(F2), unrestricted local invertible encoding and full joint field-linear readout yield exactly d*r distinguishable invertible-orbit codewords.

**Proof.** X -> X M has image dimension d*r. Invertible matrices span M_d(F2), so actual invertible encodings span that image and contain a basis of it. A joint invertible decoder distinguishes that basis; Q1 supplies the upper bound. QED.

For the structured literal resources obtained by expanding M in M_2(A), binary rank is

    r_bin = 8-a-b.

If Alice's encoders are restricted to GL_2(A) but Bob's final fine-grained decoder is unrestricted, the corresponding maximum invertible-orbit codebook is **2*r_bin**. The same span argument applies because GL_2(A) spans M_2(A) over F2, and X -> X M has binary image dimension 2*r_bin.

This last quantity can be below the ordinary eight-letter unassisted literal baseline. That does not mean that preshared correlations reduce the optimal capacity of a device allowed to discard them and prepare a fresh carrier: it only limits this fixed-resource invertible-orbit codebook. Allowing the baseline preparation strategy gives at least max(8,2*r_bin). The asymmetry between a restricted encoder and unrestricted decoder is an explicitly stated hardware/protocol contract, not a secretly closed homogeneous gate theory.

## D.2 Implication graphs

For complete S measurements and the single-copy exact protocols just specified:

    universal A^2 teleportation
                |
                v
    4-message shared dense coding  <=>  strong contextuality
                |
                v
    logical contextuality  <=>  Bell-support nonlocality
                ^
                |
        shared nonseparability

The last arrow is actually an equivalence: in this complete two-party chain-ring family, shared nonseparability iff logical contextuality. The strict chain is therefore

    teleportation -> strong <=> full shared dense coding
                    -> logical <=> shared nonseparable.

The reverse implications fail as follows:

- D(1,1): strong and four-message shared dense coding, but not universal A^2 teleportation.
- D(0,1): shared nonseparable and logically contextual, but not strong and not four-message shared dense coding.

The first separation requires a **nonprimitive resource**. On primitive shared bipartite resources, a=0, so strong contextuality, four-message dense coding and universal A^2 teleportation coincide. Restricting to primitive states changes the hierarchy, although it does not by itself repair closure under conditioning.

For unrestricted literal L:

    universal d-dimensional teleportation <=> d^2-message dense coding
                    |
                    v
    strong contextuality <=> nonseparability <=> rank >= 2.

The bottom equivalence uses the complete field-linear basis family. A rank-two resource in local dimension eight is strongly contextual but does not teleport an arbitrary eight-dimensional state.

For the structured literal family with A-linear/coarse Bell measurements, the support hierarchy is inherited from R1 after a Bob-side conjugation relabeling, but **literal separability is not**. D(0,4) is a shared product and support-local under the A-family while its literal expansion has rank four and is literally nonseparable. Under all field measurements it is strongly contextual.

Thus "nonseparability implies Bell support nonlocality" is true for the complete field and complete shared-ring contracts, and false for the literal carrier with the restricted/coarse A-family.

## D.3 Equal rank and enlargement of operations

D(0,2) and D(1,1) both have binary rank six. They are equivalent under unrestricted GL_8(F2) local operations, but not under GL_2(A): the first is logical-not-strong and has only two shared block messages; the second is strong and has four. Their restricted literal fine-readout orbit codebooks both have twelve words. This displays exactly which notion of resource power is being compared.

Enlargement to full local field-linear groups **in the literal model L** collapses Smith classes to binary rank, not to a single class of all entangled states. An arbitrary F2-linear local map need not descend to a balanced tensor product over A, so this is not automatically an admissible gate enlargement on the fixed shared composite S. The independent invariant profile

    rank(u^j M) = max(4-a-j,0)+max(4-b-j,0)

explains what the restricted A-linear group preserves and the larger group forgets.

Contextuality does not imply universal teleportation in these models, as D(1,1) shows. Teleportation does imply strong contextuality under the complete F/L and S contracts above. That is not a theorem about all process theories: Spekkens's toy theory supplies teleportation analogues without Bell nonlocality [Spekkens2007, CES2010]. Restricting a particular Bell experiment to Z alone is not a valid counterexample to a statement about all measurements available in a teleportation-capable theory.

---
# E. Stabilizer-like assessment and alternative forms

## E.1 What the rotation restriction actually defines

The centralizer of the cyclic four-step action on F2^4 is precisely A. On m phase-bearing arms, the centralizer of the simultaneous rotation is M_m(A), and its invertible part is GL_m(A). This is a principled **equivariant linear subtheory**, not merely a visually selected list of gates.

If arbitrary arm-addressed elementary shears, diagonal units and arm permutations are admitted, they generate GL_m(A): Gaussian elimination over a local ring has a unit pivot whenever the remaining matrix is invertible. Conjugating an elementary shear by appropriate diagonal rotations gives coefficients R^k; composing shears adds their coefficients, producing every coefficient in A. This generation statement names arm-addressed gates; it does not silently assert that an arbitrary fixed nearest-neighbour circuit catalogue has the same synthesis cost.

The group is finite, with

    |GL_m(A)| = 2^(3*m^2) * |GL_m(F2)|.

Reduction modulo u is onto GL_m(F2), and its kernel consists of I+uK, with 2^(3*m^2) possibilities. Deterministic unit-pivot elimination provides a synthesis normal form in polynomial time in m. It is not necessarily a shortest circuit or a unique group-word normal form.

For a single shared carrier A^2, the nonzero vector orbits under GL_2(A) are classified by the minimum coordinate valuation. Their sizes are 192, 48, 12 and 3. Bipartite local equivalence is the 15-class Smith classification already used. General multipartite orbit classification is not established here.

These algorithms are polynomial in the **explicit vector or matrix dimension**. For n logical carriers, m=2^n in S; even writing an unrestricted state takes exponentially many bits. Neither finiteness nor linearity proves efficient simulation in n.

## E.2 A genuine Pauli-like group, and its actual normalizer

Let z=R^2=1+u^2. On A^{2^n}, define

    X_a |x> = |x+a>,
    Z_b |x> = z^(b dot x) |x>,
    P_n = < R I, X_a, Z_b >.

Then

    X_a Z_b = z^(a dot b) Z_b X_a,
    |P_n| = 4 * 4^n.

Modulo the scalar centre <R>, the labels form F2^{2n}; the commutator is the usual nondegenerate alternating form on those labels. This is an actual symplectic commutator structure, rather than a name borrowed from ordinary stabilizer theory.

However, the normalizer does not reproduce the usual complex-qubit normalizer. For n=1, independent exhaustive conjugation inside all 24,576 matrices of GL_2(A) gives:

| Quantity | Exact value |
|---|---:|
| Pauli-like group order | 16 |
| A-linear normalizer order | 256 |
| Induced subgroup of Sp_2(F2) | 2, rather than all 6 |
| Primitive projective measurement bases induced by that normalizer | 4 |
| Nonzero A^2 state orbits under that normalizer | 12 |

The orbit sizes are recorded with representatives in `new_symplectic_and_normalizer.json`; they sum to 255. The induced four-base family happens to be the same family obtained from the transpose-orthogonal A-linear restriction. This is equality of the computed measurement families, not equality of the gate groups.

The native shear W is **not in this normalizer**. For a mobit, W X W is an upper-triangular shear rather than a Pauli-like monomial matrix. There is also an elementary invariant obstructing a would-be Hadamard interchange of X and Z: in their eight-dimensional binary representations,

    rank(X+I)=4,       rank(Z+I)=2.

Thus no binary similarity can exchange them. Correspondingly, their fixed spaces have 16 and 64 vectors, respectively. A single stabilizing generator does not uniformly halve the state-space dimension as in the conventional complex-qubit picture.

Even before adding A, local GL_2(F2) gates together with CNOT generate all GL_4(F2) on two mobits. The independent breadth-first closure has 20,160 elements. Calling that native catalogue a stabilizer simulator merely because its gates are linear would be unjustified.

Contextuality can remain with some resources and the four-base family: the canonical D(0,1) has unextendable events. This observation does **not** prove that such resources are preparable from a chosen computational state using only the normalizer. A state-preparation restriction must be included before claiming contextuality inside a preparation-and-measurement subtheory.

## E.3 A genuinely tractable subtheory

One conservative, efficiently describable subtheory consists of uniform F2 sums over affine subsets of computational basis labels, affine reversible label maps, and computational-basis conditioning. Store an affine set as an offset plus a basis of a binary subspace. NOT, CNOT and SWAP update that representation by binary linear algebra, and conditioning solves additional affine equations. Representation size and update time are polynomial in the number of basis-label bits.

This subtheory has a classical support model and does not supply the complete modal complementary measurements. An arbitrary native shear escapes it: applying W to one side of |00>+|11> produces a three-element support, which cannot be an affine subset over F2. A nonlinear reversible label permutation such as a Toffoli can also leave an affine-support description. Escaping this representation is not itself a proof of computational hardness.

The defensible assessment is therefore:

- a principled finite equivariant algebra exists;
- a genuine Pauli-like subgroup and a computable normalizer exist;
- a small, clearly defined efficient subtheory exists;
- a Gottesman-Knill theorem for the entire native W/R/CNOT theory has not been demonstrated and does not follow from the available evidence [Gottesman1997].

## Theorem E1: transpose orthogonality blocks a complete exact teleportation analyzer

Every U in O_d(F2) fixes the all-ones vector j. Indeed, the binary dot product satisfies x dot x=j dot x; preservation of the dot product implies U^T j=j and hence Uj=j. Therefore the linear span of O_d(F2) lies in the space of matrices whose row sums and column sums all equal one common scalar. That space has dimension

    (d-1)^2+1 < d^2,       d>=2.

For an invertible teleportation resource M, a branch admitting an orthogonal correction has its reshaped effect in a fixed invertible translate of span(O_d(F2)). Such effects cannot span the d^2-dimensional joint dual space. Hence there is no complete rank-one universal teleportation analyzer with transpose-orthogonal corrections. QED.

Permutation matrices already span this row/column-sum space, so the dimension bound is sharp. Independent enumeration gives |O_4(F2)|=48 and span dimension 10. The theorem is about the specified rank-one complete analyzer/correction protocol, not every conceivable enlarged instrument or environment.

## Theorem E2: the native shear and relative rotation preserve no common nondegenerate bilinear form

On two d-dimensional arms, let

    W = [[I,0],[I,I]],        D = diag(I,R),       R != I.

If a bilinear form with block matrix B=[[A,C],[D0,E]] is preserved by W, multiplication gives E=0 and D0=C. Nondegeneracy then forces C to be invertible. Preservation by the relative rotation forces C R=C, which implies R=I, a contradiction. QED.

This rules out rescuing the entire native catalogue merely by substituting an unspecified nondegenerate symplectic form for the transpose dot product. The gate set must change.

There are nevertheless useful **different** form-preserving theories. In the cyclic phase basis, R preserves the alternating form J=R^2. Enumeration gives |Sp_4(F2)|=720, while the split quadratic form Q(x)=x_0 x_2+x_1 x_3 has an isometry group of order 72. On two ordinary mobits with local alternating form J_2 and tensor form J_2 tensor J_2, 72 of the 360 ordered candidates drawn from four distinct invertible reshaped effects give complete symplectic teleportation analyzers. One such analyzer and all checks are in `new_symplectic_and_normalizer.json`.

The symplectic form on amplitude space in this paragraph is a different object from the symplectic **Pauli-label** commutator form in E.2. Neither is a positive inner product. They must not be conflated with one another or with a conventional quantum dagger.

---

# F. Additional formal theorems and the symbolic architecture

## Theorem F1: the rotation algebra is a typed lift, not the original Boolean product

For a four-cycle R over F2, its minimal polynomial is (t+1)^4. Thus the map

    sum_j a_j R^j  <->  sum_j a_j t^j mod (t^4-1)

identifies its 16-element cyclic algebra with F2[u]/(u^4), u=t+1. Matrix multiplication becomes cyclic convolution of the four R-coefficients. The unit group has eight elements and is isomorphic to C4 times C2. Transpose in the cyclic basis induces the involution bar(R)=R^{-1}, with lambda(a)^T=lambda(bar(a)). This is a genuine algebraic involution, but it supplies neither a positive inner product nor a canonical physical state-to-effect identification. With computational block readout, independent coordinate units form a phase group (A^times)^m; under fine field-linear measurements the same transformations need not be invisible phases.

This multiplication is neither entrywise AND of CM truth coefficients nor the original 2-by-2 CM matrix product. For example, the ordinary 2-by-2 identity CM occupies opposite cyclic positions, whose rotation lift is I+R^2=u^2. The identity's lift is square-zero, not a multiplicative identity. Consequently the geometric lift is not an algebra homomorphism for either of those original products. QED.

Every eigenvalue of R in any field extension is 1, since its minimal polynomial is a power of t+1. Its order four is unipotent order, not a copy of multiplication by the complex number i. Relative phase interference is nonetheless real as an algebraic distinction: for W above,

    W diag(I,R^k) W(v,0) = (v,(I+R^k)v).

For k=0 the second arm cancels; for k=1,2,3 the kernels of I+R^k determine which inputs cancel. This is exactly XOR cancellation, with valuation-dependent kernels. Calling it XOR cancellation does not invalidate the calculation; it identifies the mechanism and its limits.

## Theorem F2: shared and literal composition cannot be interchanged

Over A, the nonzero vectors u^3 e_0 and u e_0 tensor to zero. Over F2, the literal tensor of their nonzero four-bit coefficient vectors is nonzero. Thus no faithful interpretation identifying every such shared product with the literal product can preserve both nonzero preparations and composition.

Moreover, the primitive shared bipartite state with coefficient matrix diag(1,u), conditioned by the primitive second-coordinate effect, produces (0,u), which is nonzero but not primitive. Consequently the all-nonzero shared state space fails independent-preparation closure, while restricting to primitive states fails conditioning closure. QED.

These are not minor notation problems. A completed operational proposal must say whether it restricts resources, changes support to a unit test, admits zero/null branches as preparations, enlarges state objects, or uses literal tensors. Each option changes some earlier claims. This report evaluates the given support experiments without silently selecting such a repair.

## Theorem F3: no universal linear cloning

Let V=F2^d with d>=2. There is no linear map C satisfying C(v)=v tensor v for every nonzero v, even with a fixed ancillary blank on the input.

**Proof.** Applying linearity to distinct basis vectors e_i,e_j gives C(e_i+e_j)=e_i tensor e_i+e_j tensor e_j. Cloning e_i+e_j instead requires those terms plus e_i tensor e_j+e_j tensor e_i. The cross terms are nonzero and independent. QED.

No probability, reversibility or inner product was used. Copying a known classical coefficient description, copying computational basis labels with CNOT, and the linear direct-sum map v -> (v,v) are different tasks. The last map is not tensor cloning. This is established modal background, independently recovered here [SW2012, JOS2011].

## Theorem F4: reversible no deleting, and the limitation of a stronger slogan

Suppose an injective linear evolution sends every v tensor v to v tensor b for one fixed nonzero blank b and retains no input-dependent environment. This is impossible for d>=2.

**Proof.** The duplicated vectors span the symmetric-tensor subspace generated by e_i tensor e_i and e_i tensor e_j+e_j tensor e_i. Its dimension is d(d+1)/2. Their proposed outputs span a space of dimension at most d. An injective map cannot make that reduction. QED.

Over F2, however, the noninvertible algebraic contraction

    D(e_i tensor e_j) = delta_ij e_i tensor b

does satisfy D(v tensor v)=v tensor b, because each scalar obeys v_i^2=v_i. Thus **linearity alone** is insufficient for a no-deleting theorem in this model. This map is not automatically an allowed complete deterministic modal process: it has a nonzero kernel, and a completion by additional branches would have to be specified. It may be treated as a heralded algebraic branch. Moving the discarded copy into an information-bearing environment is also not deletion under the fixed-blank/no-environment-information condition.

The package verifies the contraction and the clone-span dimensions for d=2,3,4. No unsupported categorical no-deleting axiom is imported.

## Theorem F5: exact distinguishable-syndrome error correction

Let E:L -> V be an injective linear encoding and F_1,...,F_t a specified list of linear error maps. There exists an injective linear decoder on their joint image satisfying

    D F_a E(psi) = psi tensor |a>

for every a and psi, with distinct retained syndrome labels, if and only if every F_a E is injective and their images form a direct sum.

**Proof.** Distinct output syndrome sectors are independent and preserve each input, proving necessity. For sufficiency, define D separately on each independent image using the inverse of F_a E and the required syndrome label; their direct sum is a well-defined isomorphism onto the corresponding syndrome sectors. Where source and target ambient dimensions agree, extend this isomorphism by completing bases. QED.

This is a precise analogue, not a general replacement for the quantum Knill-Laflamme condition: degenerate errors need not require distinct syndrome labels. For the three-mobit repetition encoding |0> -> |000>, |1> -> |111>, the four errors I,X_1,X_2,X_3 give four disjoint two-dimensional error subspaces that exhaust F2^8. The independent test checks all three nonzero input states and all fifteen nonzero coherent error combinations. After decoding, the logical state factors from the error-syndrome state. No stochastic error rate, fidelity or fault-tolerance threshold is thereby defined.

## Theorem F6: swapping and remote preparation are contraction statements

For resources M_AB and N_CD, a joint effect on B,C with coefficient matrix E produces the A,D resource

    M E N.

If M,E,N are square and invertible, the resulting resource is full-rank and local inverse corrections can put it in a chosen reference form. A complete invertible-matrix effect basis therefore supplies exact entanglement swapping. This is the same contraction algebra underlying teleportation; no rotation phase is needed. Singular or nilpotent factors can reduce rank or annihilate a shared branch.

Over a field, a nonzero desired remote vector phi can occur after one rank-one local effect on resource M exactly when phi belongs to im(M^T). Choose a nonzero preimage effect and extend it to a basis. A full-rank resource reaches every nonzero target in this heralded sense.

Over A, belonging to im(M^T) is not enough for the **primitive projective effect** contract: the target must admit a primitive preimage effect. For example, an invertible M sends primitive effects to primitive targets, not to arbitrary nonprimitive vectors. A possible heralded outcome is not guaranteed to occur. Deterministic remote preparation of a known state can instead prepare it locally and use an available teleportation protocol; this gives no new optimal communication claim. QED.

## Theorem F7: nonlinear Boolean logic has a linear reversible amplitude embedding

For every Boolean function f:{0,1}^n -> {0,1}^k, the basis-label map

    (x,y) -> (x,y xor f(x))

is an involutive permutation. Its permutation matrix is invertible and F2-linear on the amplitude space, and also acts A-linearly after extension of scalars. Nonlinearity of f in x does not imply nonlinear evolution of amplitudes.

A bounded-fan-in Boolean circuit for f can be compiled by computing its gate values into fresh workspace using NOT, CNOT and Toffoli-style reversible gates, XORing the result into y, and uncomputing the workspace. With a T-gate source circuit this straightforward construction uses O(T) workspace and O(T) reversible gates, apart from ordinary input/output bookkeeping. More economical ancilla tradeoffs are possible but not asserted here. Mathematically no ancilla is necessary if the entire permutation U_f is admitted as a primitive; the synthesis cost has then been placed inside that primitive.

The symbolic LM layer can represent and validate the source Boolean formulas using Paper B's valuation and pairing identities. Its existing compiler's admitted fusion rules can be used where their operand-frame preconditions hold; this does not magically extend those rules to arbitrary compound operands or remove truth-table expansion costs [B]. The independent tests cover all sixteen two-input functions, their algebraic-normal-form reversible implementations, and the corresponding LM valuations.

An ablation that removes nonlinear Boolean oracle logic but keeps **all** invertible amplitude matrices is incoherent: the latter already includes every such permutation matrix. A meaningful ablation restricts the gate catalogue, the oracle interface or the cost model.

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
# G. Reproducible computational package

## G.1 Execution and conventions

From the extracted package root, run:

```bash
python -m pip install -r requirements.txt
python code/run_all.py
```

The independent mathematical code is standard-library Python except for SymPy 1.14.0, used for an exact rational probability certificate. There is no numerical quantum simulator, random search, floating-point optimization or supplied-code import in the independent calculations. Python 3.13.5 on Linux was used for this run; the code targets Python 3.10 or later.

`laboratory.py` must run first because it writes the exhaustive gate/ray inventory used by the targeted tests. The runner then executes the ablations, symbolic/phase checks, constructive two-setting theorem checks, and the cross-validation/package checks. Every stage logs to a file. A failed assertion, missing dependency or timeout gives a nonzero exit status rather than a passing summary.

The independent ring representation is the four-bit polynomial in u. Historical audit files use R-coefficients. Their conversion is the binary Pascal transform with columns 1,3,5,15; comparisons transform the encoding explicitly. Transpose-orthogonality is tested in the cyclic R-coordinate basis, not mistakenly in the u-polynomial basis.

Machine-readable resources include the full 65,536-resource inventory, all 192 bases and all 24,576 local A-linear gates. Protocol files give actual effects/corrections or matrices sufficient to reconstruct them. Probability files contain rational linear-combination certificates, not merely an optimizer's Boolean feasibility answer.

## G.2 Finite scope and runtime ledger

The following table is generated from the fresh metrics. Counts in its scope column identify the actual finite experiment; a dash means that enumerating states or gates is not the relevant operation. Runtime is wall time for that stage on this environment, not a portable performance claim.

<!-- LEDGER_START -->
| Experiment | Exact finite scope | Seconds | Output file(s) in data/ |
|---|---|---:|---|
| Bell_GHZ | Bell assignments enumerated=64; Bell contexts=9; Bell measurements per site=3; Bell states=1; GHZ assignments enumerated=512; GHZ contexts=27; GHZ possible events=112; GHZ states=1 | 0.0008 | independent_bell_ghz.json |
| Pauli_normalizer | Pauli like group order=16; ambient local A gates=24576; generated two mobit group order=20160; normalizer order=256; symplectic image order=2 | 0.3118 | new_pauli_normalizer.json |
| algorithms | BV hidden strings total=62; DJ operator coordinate checks=56; Deutsch preparations total=270; UNIQUE SAT n range=[1, 6]; UNIQUE SAT promised functions=132; kickback cases=32 | 0.0270 | new_algorithm_checks.json; unique_sat_reproduction.csv |
| contextuality | boolean variables=384; classification totals={'local': 5265, 'logical_not_strong': 34056, 'strong': 26214}; contexts per class=36864; measurements per party=192; nonzero smith classes=14; resources covered=65535 | 1.5759 | independent_contextuality.csv |
| deletion_QEC | coherent error combinations=15; deletion state checks=25; error checks=45; error input states=3 | 0.0006 | new_deletion_and_error_correction.json |
| dense_capacities | counterexample=D(1,1): four shared block messages but no universal A^2 teleportation; encodings per class=24576; joint measurement block labels=4; resources smith classes=14 | 1.1333 | new_dense_capacity_classes.csv |
| inventory | gates=24576; literal nonzero products in structured family=9; measurements=192; rays=24; resources including zero=65536; shared nonzero products=5265; states A2 including zero=256 | 0.5960 | independent_resource_inventory.csv |
| protocols | gates=displayed complete invertible-matrix bases; inverse corrections; literal dimensions=[2, 8]; literal input branch checks=16400; resources=identity in each carrier; all branch maps checked as identities; shared input branch checks=1024 | 0.0361 | independent_protocols.json |
| GHZ_two_settings | GHZ states=1; assignments each=64; contexts each=8; logical subscenarios=27; strong subscenarios=0; two setting subscenarios=27 | 0.0026 | ghz_two_setting_ablation.csv |
| Simon_n2 | hidden shifts=3; n=2; nonzero preparations=65535; one query successes=0; state dimension=16; valid standard oracles=36 | 1.5820 | small_simon.json |
| orthogonal_ablation | A gates scanned=24576; O8 intersection A linear=512; all binary 4x4 matrices scanned=65536; assignments per representative=256; canonical nonzero resource representatives=14; measurement bases=4 | 0.7739 | independent_orthogonal_ablation.csv; independent_forms.json |
| probability | contexts=9; modal possible events=24; necessarily zero possible events=6; probability variables=36; weak positive events=18 | 0.1502 | independent_probability_certificate.json |
| symplectic_and_normalizer | GL2 candidates=6; Pauli normalizer bases=4; Pauli normalizer gates=256; Pauli normalizer nonzero state orbits=12; ordered analyzer candidates=360; valid symplectic analyzers=72 | 0.0062 | new_symplectic_and_normalizer.json |
| LM_oracles | CM tokens=16; LM pairing valuations=256; ancillas=0; gate set=NOT, CNOT, Toffoli; ANF compilation only for these two-input functions; oracle state dimension=8; reversible oracle basis cases=128 | 0.0009 | lm_reversible_oracles.csv |
| description_readout_ablation | BV hidden strings=510; DJ functions=12956; Deutsch functions=4; readout contract=classical full coefficient inspection, NOT complete modal readout | 0.0481 | description_readout_ablation.json |
| phase_Fourier | Walsh n range=[1, 6]; four level kickback cases=32; primitive eigenvectors checked=192 | 0.0033 | new_phase_fourier.json |
| tensor_boundaries | counterexamples=3; gate or measurement=standard second-coordinate effect for conditioning witness | 0.0001 | independent_tensor_counterexamples.json |
| two_setting_no_strong | all nonzero states tested=65808; n range=[1, 4]; supported context checks=1050666 | 0.1781 | two_setting_no_strong_certificates.json |
<!-- LEDGER_END -->

`data/computational_ledger.json` retains every metric field, including counts too detailed for the display table. `reports/COMPUTATIONAL_LEDGER.md` gives the same information separately. Cross-checks against selected **freshly rerun** supplied outputs are recorded in `data/source_comparison.json`; those reference files and their provenance are included separately from the independent implementation.

The canonical-class reduction is justified only for an invariant operation/measurement family. It is valid for the full GL_2(A) and 192-base experiment. For the four-base orthogonal/normalizer ablation, the computation deliberately says **14 canonical representatives**, not all 65,535 states classified under that smaller group.

## G.3 Source-driver rerun boundaries

The supplied model driver completed algebra, inventory, contextuality and GHZ stages. The supplied protocol driver completed gate synthesis, full literal teleportation/dense coding, model-boundary and probability stages. The separate adversarial-review extension driver completed its 22 small ring/dimension campaigns and Boolean degree/filtration checks. Selected outputs and their logs are retained as reference evidence.

The aggregate historical runner and the subsequent supplied exhaustive restriction sweep timed out. Only the latter's preliminary CM/LM stage completed in that attempt. Files copied from an input archive but not freshly regenerated are not labelled fresh. The independent four-base, phase, gate-normalizer, oracle and tensor-boundary calculations do not depend on completion of those historical sweeps.

The package's manifest hashes all delivered code and data. Mathematical theorems with universal quantifiers are supported by their proofs, not by calling a finite search exhaustive outside its stated range.

---

# H. Prior-art matrix and novelty boundary

| Prior work or family | What it already supplies | What is different in this investigation | Claim status |
|---|---|---|---|
| Schumacher-Westmoreland modal quantum theory [SW2012] | Finite-field nonzero states, linear reversible dynamics, nonorthogonal basis measurements, complementarity, Bell/no-cloning arguments, teleportation and dense coding | Explicit ablations of R, tensor choice, ring valuation and operation groups | Phenomena are known; new calculations verify the current models and dependencies |
| James-Ortiz-Sabry finite-field computing [JOS2011] | A reversible programming account of finite-field superposition and exclusive-disjunction interference | A typed connection to Paper B's particular LM compiler and an honest oracle interface | General Boolean/reversible programming bridge is known; CM-specific compiler integration is narrower |
| Willcock-Sabry UNIQUE-SAT [WS2011] | One-query modal UNIQUE-SAT using nonorthogonal transformations | Independent positive-control reproduction beside no-go results for other standard algorithms | Algorithm is known and explicitly credited |
| de Beaudrap semiring/ring computation [deB2014] | A general amplitude-semiring framework and complexity classifications for cyclic rings and finite fields | The restricted A-equivariant gate/measurement contract and its resource invariants | Finite-ring computation is not new; A is not simply the cyclic ring Z_16 |
| Abramsky-Brandenburger possibilistic contextuality [AB2011] | Global-section tests, logical and strong contextuality, general measurement covers | Exact Smith/leading-layer resource classification and decoder comparison in the supplied chain-ring family | Hierarchy terminology and support methodology are prior art |
| Spekkens toy theory [Spekkens2007] | Complementarity, no-cloning, steering, teleportation and dense-coding analogues without Bell nonlocality | Explicit counterweight to universal implications inferred from the CM models | Shows the CM implication graph is model-relative |
| Relational and categorical process theories [AC2004, Gogioso2017] | Structural descriptions of composition and communication protocols outside complex Hilbert spaces | Precise distinction between OR/AND relations, XOR/AND linear relations, and a shared ring tensor | The categorical protocol viewpoint is known; this report is not about Rovelli's relational interpretation |
| Phase-group methods [CES2010] | Phase-group explanations of GHZ behaviour in specified mutually unbiased qubit theories | R is unipotent; the required observable structure is absent, and two binary settings cannot be strongly contextual here | Order-four R alone does not instantiate that earlier phase-group theorem |
| Stabilizer theory [Gottesman1997] | Actual Pauli normalizers, symplectic label structure, efficient code/state descriptions | A nonstandard 16-element Pauli-like group with a 256-element local normalizer and a native shear outside it | Do not identify binary stabilizer labels with binary amplitudes |
| Finite-field Fourier methods | Character orthogonality when the amplitude algebra has appropriate roots and invertible group order | The direct characteristic-two Boolean-group obstruction in Q5 | Modular-character obstruction is standard algebra; application to this exact oracle contract is the useful organization |
| Polynomial quantum query methods [BBCMW2001] | Polynomial degree as a tool for oracle lower bounds | Characteristic-two affine dependence gives the exact BV bound q>=n, alongside Deutsch/DJ span obstructions | The method is antecedented; priority of these specific modal formulations is not certified |
| Chain-ring module/coding theory [BHKW2022] and the supplied review | Smith types, residue/radical layers and module invariants; the supplied review already proves R1 | Leading-layer exact dense-codebook size d*h and its comparison with universal teleportation | Algebraic foundations and R1 are imported; R2 is a derived theorem requiring focused priority review |
| Quantum teleportation/dense-coding duality [CL2024] | A probabilistic state-discrimination duality for noisy complex-quantum protocols | Exact nonprimitive chain-ring codebooks versus universal recovery of a full free module | The nilpotent separation does not contradict a theorem with different probabilities, normalization and tasks |

A targeted web search was made for the named primary literature and for modal Deutsch/Bernstein-Vazirani, two-setting contextuality, and chain-ring dense coding. It did not identify an exact earlier statement of R1b or R2 in the returned primary sources. That is **not evidence sufficient to certify priority**. Searches also return ordinary quantum algorithms whose *labels* use GF(2), classical codes over rings, modal interpretations of complex quantum mechanics, and optical spatial/temporal modes. Those are not interchangeable with characteristic-two amplitude theories.

The result that most plausibly deserves a focused novelty audit is the combination

    leading Smith multiplicity h
           -> exact shared codebook size d*h
           -> strong support contextuality iff h>=2,

contrasted with unit-rank requirements for universal teleportation and the closure issue for nonprimitive resources. The two-setting global-assignment theorem and the exact modal query bounds form a second, conceptually distinct cluster. Neither cluster depends on renaming an already-known finite-field Bell state a CM state.

---

# I. Negative results and adversarial conclusions

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

## I.2 What the negative results actually eliminate

**Interference is XOR cancellation.** There is no additional physical amplitude magnitude hidden behind the notation. The useful extra structure is the kernel/valuation geometry of which contributions cancel.

**The basic Bell, no-cloning, teleportation and dense-coding constructions do not need CM-specific phase.** They survive the F2 ablation. Their discovery in a CM implementation can still be pedagogically useful, but is not a new quantum-information phenomenon.

**Phase is not Fourier structure.** Standard XOR kickback is available with z=R^2, and cyclic-target kickback with R. Neither supplies a complete invertible Boolean-character transform. One-query Deutsch/DJ and BV phase readout do not follow.

**A two-setting quantum GHZ pattern does not survive these binary modal contracts.** The larger three-setting no-global-assignment table is valid but different. The distinction is a theorem for all numbers of binary sites, not merely a failed search on one GHZ state.

**All nonzero shared-module states do not define a closed preparation theory.** Excluding the problematic nonprimitive states also excludes the most striking dense-coding/teleportation separation, and primitive-only conditioning still needs repair.

**An eight-dimensional literal state is not a two-dimensional shared state.** A four-outcome logical Bell analyzer cannot teleport all its independent phase information. Full literal protocols need the appropriate 64-outcome analyzer and larger operation group.

**An orthogonal restriction is substantive, not cosmetic.** It changes both accessible measurements and exact protocol feasibility. Replacing it with a symplectic form may permit other protocols, but cannot preserve all the native relative-rotation and shear gates simultaneously.

**No general native stabilizer simulation theorem has been established.** Matrix size, state descriptions and oracle implementation costs remain essential. A four-cycle, a finite gate group and XOR arithmetic are insufficient evidence.

**A coefficient-wise Boolean formula is not a physical measurement.** LM valuation can compile numerical semantics after a model is chosen, but does not choose a tensor, a complete instrument or a probability rule. Symbolically reading a global answer from a truth vector cannot be charged as one black-box point query.

**No general Grover or Simon speedup has been obtained.** The standard Fourier/reflection mechanisms fail. This does not exclude every alternative modal algorithm; UNIQUE-SAT is a concrete reason not to make that stronger claim.

## I.3 Remaining explicitly unclassified questions

The report does not determine the optimal multi-query Deutsch-Jozsa complexity, all-ancilla/all-size Simon complexity, general multipartite orbit structure for native local gates, a preparation-closed many-carrier normalizer subtheory, or a preferred operational completion of shared nonprimitive states. It also does not give a general noisy-channel/error-correction theory or certify priority of the newly derived theorem formulations. Those are named boundaries of this investigation, not silently positive or negative entries in the capability map.

---

# J. Paper recommendation and final dependency synthesis

## J.1 Recommendation

There is enough coherent mathematics for a research paper, but the best organizing claim is **separation of resources**, not a catalogue titled as though every quantum algorithm survived.

A strong primary-paper title would be:

**Boolean Modal Information: Tensor Choice, Valuation Resources, and Exact Protocols**

Its core should be the operational contracts; the shared/literal closure and separability distinctions; the imported contextuality classification with full attribution; the leading-layer dense-coding theorem; the universal-teleportation criterion; and the resulting strict resource hierarchy. A short field-modal laboratory section can demonstrate the familiar positive protocols without making them the novelty claim. The restricted orthogonal and actual normalizer calculations provide useful boundary results.

The proposed title **A Boolean Modal Laboratory for Quantum Information: Logical Operators, Phase, Contextuality and Exact Protocols** is suitable for the broader reproducible exposition or software companion. As a journal research title it should not obscure that several central phenomena are standard modal quantum theory and that the shared construction is not yet a fully closed operational theory.

The algorithm cluster is sufficiently different to merit a separate paper or substantial companion note:

**Exact Query Obstructions in Characteristic-Two Modal Computation**

That paper should lead with Q1-Q4, include the kickback-versus-Fourier distinction, and reproduce UNIQUE-SAT as the counterweight. The Simon result should remain a scoped finite experiment; Grover should remain a clearly delimited mechanism obstruction. A dedicated literature check of modal query complexity is required before submitting priority claims.

The symbolic LM augmentation belongs in a bridge/implementation section or a separate foundations note. Paper B's valuation and compiler theorems should be cited, not republished as newly obtained physics. Applications to verified Boolean circuit compilation, small-model testing, educational protocol laboratories and algebraic resource diagnosis are defensible; physical quantum speedups are not established.

## J.2 Minimal counterexamples worth placing in the main paper

The smallest nontrivial finite commutative chain ring, F2[epsilon]/(epsilon^2), with two-dimensional local modules already supplies epsilon*I_2: strong support contextuality and four-message shared dense coding without universal teleportation. Field scalar algebras cannot supply this nilpotent separation, and one-dimensional carriers cannot supply the nonseparable two-factor resource. Thus neither length four nor an order-four CM rotation is minimal for that phenomenon.

The same dual-number ring supplies diag(1,epsilon): a pure logically contextual but not strongly contextual resource under the complete primitive-basis contract. In ordinary complete-basis field modal theory, a pure bipartite state is either rank-one local or rank-at-least-two strong, so there is no corresponding intermediate pure-state class there.

In the given A, diag(1,u^2) and diag(u,u) have the same binary rank six but different shared codebook capacities and contextuality strengths. A literal expansion of diag(1,0) has rank four yet is support-local under the restricted coarse A-measurements. These are small, explicit witnesses that rank, separability and contextuality cannot be moved between models without naming the operations and readout.

## J.3 The dependency map in one statement

**Linear addition alone** gives superposition-like combination and XOR cancellation. **Multiple complete dual bases** give modal complementarity. **Tensor composition, nonproduct states and sufficiently rich effects** give Bell/strong support contextuality and the no-cloning obstruction already over F2. **An invertible resource, a complete invertible-matrix effect basis and feed-forward inverses** give exact teleportation; full probability theory and CM rotation do not enter its proof.

**Valuation and restricted A-linearity** introduce the genuinely distinctive internal hierarchy: Smith types, equal-binary-rank inequivalence, the logical-but-not-strong pure-state stratum, and the leading-layer dense-codebook size d*h. **Nonprimitive nilpotent resources** separate dense coding from universal teleportation, while simultaneously exposing why an operational completion is necessary.

**Phase kickback needs an appropriate eigenvector and declared controlled action. Fourier algorithms need more:** an invertible character transform and a compatible readout. The latter is absent for Boolean groups in these characteristic-two scalar theories. Exact Deutsch and Deutsch-Jozsa therefore lose their one-query forms, and exact BV requires n queries, despite the existence of modal Bell nonlocality and teleportation.

Finally, **probabilistic quantum notions do not follow from support**. The displayed Bell table cannot even be assigned faithful nonsignalling nonnegative real probabilities. A norm, dagger or scalar involution cannot be added by notational analogy; its effect on gates, states, measurements and the support table must be proved.

The distinctive contribution is thus a dependency and separation theory for a restricted algebraic laboratory, not evidence that Boolean logic has secretly reconstructed all of quantum mechanics.

---

# References and source keys

**[B]** B. Theory. *Operator-Level Boolean Computation with Correspondence Matrices*. Unpublished manuscript supplied in the user's Library; complete 19-page text inspected. Sections 2 and 8 and Appendix A are the principal imported definitions and proofs. No raw PDF redistribution is included.

**[Audit]** Supplied *CM Final Audit*, archive dated 18 September 2026. Primary LaTeX manuscript, `code/audit_models.py`, `code/audit_protocols.py`, `code/audit_restrictions.py`, and associated data. Archive hash is in `data/input_archives.json`.

**[Review]** Supplied *CM Adversarial Review*, archive dated 18 September 2026. In particular `FORMAL_THEOREMS.md`, Theorem 9, and `checks/independent_extensions.py`. The chain-ring support classification is imported from this source.

**[SW2012]** Benjamin Schumacher and Michael D. Westmoreland. *Modal quantum theory*. Foundations of Physics 42 (2012), 918-925. DOI: 10.1007/s10701-012-9650-z. Preprint: arXiv:1010.2929.

**[JOS2011]** Roshan P. James, Gerardo Ortiz and Amr Sabry. *Quantum Computing over Finite Fields*. arXiv:1101.3764 (2011).

**[WS2011]** Jeremiah Willcock and Amr Sabry. *Solving UNIQUE-SAT in a Modal Quantum Theory*. arXiv:1102.3587 (2011). The circuit, not the paper's shorthand constant-time wording, is the positive control here.

**[deB2014]** Niel de Beaudrap. *On computation with 'probabilities' modulo k*. arXiv:1405.7381v2 (2014).

**[AB2011]** Samson Abramsky and Adam Brandenburger. *The sheaf-theoretic structure of non-locality and contextuality*. New Journal of Physics 13 (2011), 113036. DOI: 10.1088/1367-2630/13/11/113036. arXiv:1102.0264.

**[Spekkens2007]** Robert W. Spekkens. *Evidence for the epistemic view of quantum states: A toy theory*. Physical Review A 75 (2007), 032110. DOI: 10.1103/PhysRevA.75.032110. Preprint arXiv:quant-ph/0401052 appears under the title *In defense of the epistemic view of quantum states: a toy theory*.

**[AC2004]** Samson Abramsky and Bob Coecke. *A categorical semantics of quantum protocols*. arXiv:quant-ph/0402130 (2004).

**[CES2010]** Bob Coecke, Bill Edwards and Robert W. Spekkens. *Phase groups and the origin of non-locality for qubits*. arXiv:1003.5005; Electronic Notes in Theoretical Computer Science 270(2) (2011), 15-36. DOI: 10.1016/j.entcs.2011.01.021.

**[Gogioso2017]** Stefano Gogioso. *Fantastic Quantum Theories and Where to Find Them*. arXiv:1703.10576v2 (2017). Its semiring Born-style constructions must not be equated with the support-only measurement rule used here.

**[Gottesman1997]** Daniel Gottesman. *Stabilizer Codes and Quantum Error Correction*. Caltech PhD thesis, arXiv:quant-ph/9705052 (1997).

**[BBCMW2001]** Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf. *Quantum Lower Bounds by Polynomials*. Journal of the ACM 48(4) (2001), 778-797. arXiv:quant-ph/9802049.

**[BHKW2022]** Eimear Byrne, Anna-Lena Horlemann, Karan Khathuria and Violetta Weger. *Density of Free Modules over Finite Chain Rings*. arXiv:2106.09403v2 (2022). Used as primary background for finite-chain-ring module terminology, not as a claim about modal dense coding.

**[CL2024]** Eric Chitambar and Felix Leditzky. *On the Duality of Teleportation and Dense Coding*. IEEE Transactions on Information Theory 70(5) (2024), 3529-3537. DOI: 10.1109/TIT.2023.3331821. arXiv:2302.14798v2.
