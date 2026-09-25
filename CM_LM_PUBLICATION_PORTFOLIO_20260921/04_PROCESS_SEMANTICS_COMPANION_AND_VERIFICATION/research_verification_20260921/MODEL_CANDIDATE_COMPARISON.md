# Candidate comparison

All assertions refer to A=F2[u]/(u^4) unless generalized explicitly. Zero as a failed branch is distinct from zero as an admissible deterministic preparation.

| Candidate | Independent tensor | Conditioning | Verdict and retained content |
|---|---|---|---|
| All nonzero vectors in free A-modules | Fails: u^3 tensor_A u=0 | Linear branches exist, but their independent composition can vanish | Static support model or algebra of partial amplitudes; not independent normalized preparations |
| Primitive free-module vectors, original nonzero readout | Primitive times primitive is primitive; GL preserves primitivity | diag(1,u), second Alice row produces (0,u) | Incomplete; removes nilpotent resources at input but reintroduces them as outputs |
| Primitive vectors, residue/unit-possibility readout | Closed after reduction modulo u | Treat only branches with nonzero residue as possible | A coherent residue-field quotient, but changes P01's support table; e.g. diag(1,u) becomes rank one and local |
| Typed finite modules, ordinary tensor_A and all nonzero elements | Modules associate and stay finite; selected elements may tensor to zero | Images, kernels, annihilators and quotients are typed correctly | Algebraically closed category, not a repair of independent possibility |
| Primitive quotient generators plus retagging | Canonical generators of A/(u^l) tensor to generator in A/(u^min(l,r)) | Dividing a branch by u^a changes its type and its embedding | Works as bookkeeping in isolated branches; treating embeddings as lossless tensor-compatible identifications is false |
| Binary modal completion with A labels | Nonzero field tensors stay nonzero | Nonzero subspaces, complete linear instruments and discard are closed | Strongest explicit operational contract found; retains P01 tables through E, not shared tensor dynamics |
| Mat_A / finite free A-module category with zero maps retained | Symmetric monoidal algebra, exactly associative | Zero and nonzero branch maps are legitimate morphisms | Valid process syntax with A-valued scalars, but nonzero-to-possible is not monoidal |
| Boolean relations / Mat_B with cartesian set carriers | Relational nonempty products compose | Relational image and union are closed | Changes XOR interference and cannot inherit the ring resource results |
| CP*/semiring normalized construction | Established categorical constructions under their own hypotheses | Their own normalization and scalar weights | An alternative theory, not a proof that P01 nonzero support is closed; square-zero amplitudes may have zero norm |

## Primitive variants in detail

Primitivity is standard: de Beaudrap Definition 7 and Appendix B Lemma 9 explicitly use the unit-ideal condition (https://arxiv.org/pdf/1405.7381). His tensor-factor condition must not be mistaken for closure under every outcome of the new selective instrument proposed here.

For a bipartite primitive C, its smallest Smith exponent is 0, so P01's h becomes rank(C mod u). The static trichotomy and dh formula still apply to that restricted input set. For d=2, h=2 forces invertibility, so the nilpotent maximal-code/nonteleporting separator disappears. For d>=3, strong singular primitive resources such as diag(1,1,u) remain; they do not have maximal d^2 code size. These statements do not cure the postselection failure.

A rigorous closed primitive **quotient semantics** can instead reduce every process to F2: take primitive lifts modulo the relation of equal nonzero residue, use binary complete instruments lifted to A, and declare a branch possible iff its residue is nonzero. Joint completeness of the reduced maps ensures a primitive successor exists, and an individual possible branch has a primitive lift. Discard is implemented by binary mixed subspaces. Every lift ambiguity is operationally invisible. This yields ordinary field modal theory with redundant A notation; all higher-valuation resources vanish. It does not retain original nonzero-A possibility.

## Typed modules in detail

Finite A-modules are direct sums of A/(u^l), 1<=l<=4. There is a natural isomorphism A/(u^l) tensor_A A/(u^r) = A/(u^min(l,r)); sums distribute and the usual associators satisfy coherence. A Hom_A(M,A) effect exists even for torsion modules, but there need not be a free dual basis giving the free-module measurement model. With the usual nonzero scalar readout, independent effects can still annihilate. Replacing A-valued effects by typed output maps is sensible bookkeeping; calling every nonzero typed output a Boolean success still requires a new compositional semantics.

The inclusions (u^3)->A and (u)->A give a decisive warning: their abstract tensor source is isomorphic to A/(u), yet the tensor of the inclusions has zero image. A claimed equivalence that forgets these embeddings fails. Annihilator-module tags alone do not change this fact.

There is also an immediate failure of valuation normalization that discards the scalar cost. As maps on the tensor unit A, multiplying by u^3 and multiplying by u are separately nonzero. Their normalized quotient outputs might both be called the unit generator, with tensor type A/(u). In the original balanced diagram their parallel product is multiplication by u^4=0. Thus the claimed normalization cannot preserve this diagram. This disproves that particular repair, not every conceivable indexed or relational theory.

## Categorical antecedents and hypothesis audit

Ordinary module tensor is established algebra (Stacks Project, Tensor products, https://stacks.math.columbia.edu/tag/00CV). Compact closed categorical protocol syntax is established by Abramsky--Coecke (Definition 3.1 and §3.3, https://arxiv.org/pdf/quant-ph/0402130). Neither says that every nonzero morphism is a deterministic preparation.

Gogioso's Theorem 3.2 (https://arxiv.org/pdf/1703.10576) builds an R-probabilistic category from CP*[S-Mat] with the positive scalar subsemiring determined by the involution. For A with identity involution, a pure scalar's weight is a^2: u^2 is nonzero but has zero square. The resulting weight semantics is not P01's nonzero-amplitude rule. Also 1+1=0 prevents the raw nonzero map A->Boolean from preserving addition, while u^3*u=0 prevents multiplicativity.

The tau pairing makes A a Frobenius algebra, but not a separable one. Explicitly mu Delta(a)=4u^3 a=0. A balanced commuting element t in A tensor_k A is a multiple of Omega (solve (u tensor 1)t=(1 tensor u)t coefficientwise), and hence mu(t)=0; it cannot be a separability element with mu(t)=1. Therefore separable-Frobenius preservation claims such as those of McCurdy--Street §2 (https://arxiv.org/pdf/0904.3449) cannot be imported. Nonseparable Frobenius structure is enough for the support encoding, not a tensor equivalence.

Gogioso--Zeng's generalized Mermin theorem has explicit positivity and observable-structure assumptions; its converse in Theorem 5.3 requires a positive semiring. Those hypotheses cannot be inferred from the rotation C4 or from A's unit group. The user-supplied GHZ table remains a bounded example, not a new arbitrary-party theorem here.

## Publication implication

The useful positive result is a carefully delimited support interface inside a known closed theory, coupled with explicit restricted resource calculations. None of the unsuccessful ring repairs should be advertised as a closed ring quantum theory. A different completion remains possible only by changing at least one obstructed assumption; establishing historical distinctiveness of such a completion would require further work.
