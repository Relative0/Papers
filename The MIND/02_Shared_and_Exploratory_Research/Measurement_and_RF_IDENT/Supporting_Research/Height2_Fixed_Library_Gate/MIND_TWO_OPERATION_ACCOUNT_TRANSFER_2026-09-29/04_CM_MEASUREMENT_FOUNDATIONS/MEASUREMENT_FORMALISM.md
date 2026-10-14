# Measurement Formalism for Correspondence Matrices

## 1. Design goal

The goal is to give a mathematically typed meaning to "observation" and "measurement" that preserves the useful truth-operator structure of Correspondence Matrices without importing Hilbert-space physics by terminology alone.

The formalism separates four objects:

1. **worlds/valuations** — what may be the case;
2. **effects/observations** — yes/no predicates on those worlds;
3. **observation interfaces** — which predicates are available for distinguishing worlds;
4. **outcome updates** — which worlds remain possible after an outcome is recorded.

This distinction is the main repair of the 2015 system.

---

## 2. Valuation space, events, and CM truth data

Let `P={X_1,...,X_n}` and

`Omega_P={0,1}^P`.

For a formula `f`, define

`E_f = {v in Omega_P : v models f}`

and its characteristic function

`chi_f(v)=1[v in E_f]`.

For a binary connective `Theta`, the compact CM is

`[Theta]=[[Theta_11,Theta_10],[Theta_01,Theta_00]]`,

where the four entries are exactly `chi_Theta(11),chi_Theta(10),chi_Theta(01),chi_Theta(00)`.

Thus there are three equivalent *data* presentations:

- truth table / truth region `E_Theta`;
- four-bit truth vector `(Theta_11,Theta_10,Theta_01,Theta_00)`;
- compact 2x2 CM `[Theta]`.

They are equivalent as encodings of a binary Boolean function. Their available algebraic operations are not automatically the same.

---

## 3. Canonical truth-effect projector

Let `K` be `R`, `C`, or `F_2` as appropriate and let

`V_P = K^{Omega_P}`

with valuation basis `{|v>}`. Define

`D_f := sum_{v in E_f} |v><v|`.

For two variables in true-first order,

`D_Theta = diag(Theta_11,Theta_10,Theta_01,Theta_00)`.

### Proposition 3.1 — sharp-effect properties

For every Boolean formula `f`:

`D_f^2=D_f`.

Moreover:

- `im D_f = span{|v>:v in E_f}`;
- `ker D_f = span{|v>:v notin E_f}`;
- `rank D_f = |E_f|`;
- over `R` or `C`, `D_f=D_f^*`, so it is an orthogonal projector;
- `D_f D_g = D_{f and g} = D_g D_f`.

**Proof.** Each diagonal entry is 0 or 1, so its square equals itself. Products multiply characteristic functions pointwise. Image, kernel, and rank follow directly from the selected valuation basis coordinates.

This is the canonical projector representation associated with CM truth data. It is distinct from the compact 2x2 CM.

---

## 4. State types

Three state levels should be kept separate.

### 4.1 Possibility support

A state is `S subseteq Omega_P`. This is the minimal, probability-free model.

A Boolean vector `s in {0,1}^{Omega_P}` can encode it by `s_v=1[v in S]`.

### 4.2 Probability state

A probability state is a distribution `p:Omega_P->[0,1]` with total mass 1. This is an optional classical enrichment.

### 4.3 Modal/module state

A modal theory may instead use a nonzero vector/module element together with an explicitly stated effect pairing and possibility rule, e.g. "outcome possible iff contraction is nonzero." This is **not** supplied automatically by the compact CM representation; scalar ring, admissibility, composition, and measurement contexts must be separately declared.

---

## 5. Selective measurement and conditioning

For the true outcome of `f`, define

`M_f(S)=S intersect E_f`.

For the false outcome,

`M_not_f(S)=S intersect E_not_f`.

In support-vector form,

`s -> D_f s`.

For a probability distribution and `p(E_f)>0`,

`p_f(v) = p(v) chi_f(v) / sum_w p(w) chi_f(w)`.

### Proposition 5.1 — repeated measurement

`M_f(M_f(S))=M_f(S)`.

This is ordinary idempotence of set intersection and is the support-level counterpart of `D_f^2=D_f`.

### Proposition 5.2 — sequential sharp measurement

`M_g(M_f(S))=S intersect E_f intersect E_g=M_f(M_g(S))`.

Hence the core sharp CM effects exhibit no order effect.

---

## 6. Complete measurements versus selected branches

The complete yes/no measurement associated with `f` is the pair

`{E_f,E_not_f}`

or equivalently `{D_f,D_not_f}`.

It partitions any support `S` into

`S_f=S intersect E_f`,  `S_not_f=S intersect E_not_f`.

If both branches are retained together with their labels, no valuation has been lost. A *selective* branch discards the incompatible part. If the outcome label is ignored and the support branches are reunited, one recovers `S`.

This distinction prevents "measurement" from being confused with unconditional destruction.

---

## 7. Observation families and distinguishability

Let

`Phi=(phi_1,...,phi_m)`.

Define the observation signature

`o_Phi(v)=(chi_phi1(v),...,chi_phim(v))`.

Define observational equivalence

`v ~_Phi w  iff  o_Phi(v)=o_Phi(w)`.

This gives a partition `Pi_Phi` of the valuation carrier.

### Theorem 7.1 — exact strict-refinement criterion

Let `Psi=Phi union {psi}`. Then `Psi` strictly increases distinguishability on a support `S` iff there exist `v,w in S` such that

`o_Phi(v)=o_Phi(w)` and `chi_psi(v) != chi_psi(w)`.

Equivalently, the new test splits at least one old signature block.

**Proof.** The new signature is `(o_Phi(v),chi_psi(v))`; two worlds that were previously in one block split exactly when their new coordinate differs.

This is the preferred mathematical definition of "observation increases distinguishability."

---

## 8. Distinguishability and uncertainty are two different axes

A useful state of logical differentiation is the pair

`(S,Pi_Phi)`.

Two operations act on different components:

- **refinement/unfolding** `U_psi`: `(S,Pi_Phi) -> (S,Pi_{Phi union {psi}})`;
- **measurement update** `M_f`: `(S,Pi_Phi) -> (S intersect E_f, Pi_Phi restricted to S intersect E_f)`.

This produces two independent finite measures.

### 8.1 Observational resolution

A simple unweighted resolution is the number of realized signature blocks

`R(Phi,S)=|{o_Phi(v):v in S}|`.

It is monotone nondecreasing under observation refinement.

With a probability distribution, one can instead use entropy of the induced signature random variable.

### 8.2 Residual uncertainty

For uniform support,

`H_0(S)=log_2 |S|`

is Hartley uncertainty. A possible selective outcome satisfies

`H_0(S intersect E_f) <= H_0(S)`.

If `0<|S intersect E_f|<|S|`, the recorded outcome yields positive information

`I_f = log_2(|S|/|S intersect E_f|)`.

These are not the same quantity: one can reduce uncertainty without adding a new discriminating coordinate, or add a discriminating coordinate before learning its outcome.

---

## 9. Unfolding as observation refinement

The thesis's `partial` operator should not be identified with `M_f`. Its motivating examples often change a formula into a family/union of alternatives not contained in the original truth support.

A clean modern interpretation is:

`U : observation description -> finer observation description`.

At fixed carrier, this is exactly ProLT observation refinement.

### Theorem 9.1 — refinement/update naturality

Suppose `U_psi` only enlarges the observation family on the same carrier and `M_f` conditions by a truth region defined independently of that enlargement. Then

`M_f U_psi = U_(psi|E_f) M_f`

in the sense that both routes yield the carrier `S intersect E_f` equipped with the restricted enlarged observation family.

Diagrammatically:

```text
(S, Phi) ----------------U_psi----------------> (S, Phi union {psi})
   |                                              |
  M_f                                            M_f
   |                                              |
   v                                              v
(S intersect E_f, Phi|E_f) --U_(psi|E_f)--> (S intersect E_f, (Phi union {psi})|E_f)
```

If unfolding changes the carrier or introduces new latent coordinates, a different typed diagram is required; commutation is then an additional theorem, not an assumption.

---

## 10. Context embedding and purity

Let `f` be a formula on `n` variables. Its canonical extension to `n+m` variables ignores the added variables:

`iota(f)(x_1,...,x_n,z_1,...,z_m)=f(x_1,...,x_n)`.

### Theorem 10.1 — cylinder-extension law

`E_iota(f)=E_f x {0,1}^m`, hence

`|E_iota(f)|=2^m |E_f|`

and

`rank D_iota(f)=2^m rank D_f`.

Therefore the thesis's singleton-support notion of "pure logic state" is not preserved by adjoining an unconstrained variable. This is ordinary cylinder extension.

A stronger contextuality notion requires a family of measurement contexts for which compatible local outcome data fail to admit a global assignment; cylinder replication does not provide that obstruction.

---

## 11. Compact-CM idempotents: algebraic projectors, not automatically effects

Let `A` be a 2x2 compact CM. Four products were audited separately.

### 11.1 XOR-AND over `F_2`

Exactly eight of the 16 satisfy `A^2=A`:

`FALSE, AND, NOR, X, Y, XNOR, NOT_Y, NOT_X`.

The symmetric/self-transpose members are exactly

`FALSE, AND, NOR, XNOR`.

Over ordinary real scalars these four are orthogonal coordinate projectors. The other four real idempotents are oblique rather than orthogonal projectors.

### 11.2 Boolean-semiring product

Exactly eleven are idempotent: the previous eight plus

`X_IMPLIES_Y, Y_IMPLIES_X, TRUE`.

### 11.3 Ordinary integer/real multiplication

Among the 16 zero-one arrays, the same eight as the `F_2` case are idempotent.

### 11.4 Cyclic convolution on rotation coordinates

Only FALSE and AND are idempotent. In the coefficient-ring identification `F_2[C_4] ~= F_2[u]/(u^4)`, they are 0 and 1. This algebra is local, so it has no nontrivial idempotents.

These facts are useful structural classifications. They do not replace the valuation-space effect representation, where all 16 Boolean events are projectors.

---

## 12. Symmetry is not distinguishability

Let a group `G` act on a state object. A smaller stabilizer can be a meaningful notion of lower symmetry, but it is not a general information criterion.

### Proposition 12.1 — equivariant maps cannot decrease stabilizers

If `M` is `G`-equivariant, then

`Stab_G(x) subseteq Stab_G(M(x))`.

**Proof.** If `gx=x`, then `gM(x)=M(gx)=M(x)`.

Thus any genuine stabilizer decrease must come from a context/effect that is not invariant under the full symmetry group, or from changing the group being considered.

For fixed-effect restriction `S -> S intersect E`, exhaustive `D_4` computation confirms that stabilizer size can increase, decrease, or remain unchanged. Therefore use signature partition refinement for distinguishability and reserve stabilizers for symmetry analysis.

---

## 13. Finite worked differentiation path

Start with no restriction:

`S_0=TRUE={11,10,01,00}`.

Ask the XOR question and record TRUE:

`S_1=S_0 intersect XOR={10,01}`.

Then ask X and record TRUE:

`S_2=S_1 intersect X={10}=X AND NOT Y`.

The associated projectors satisfy

`D_X D_XOR D_TRUE = D_(X AND NOT Y)`.

Support sizes are `4 -> 2 -> 1`. This is a valid finite model of progressive differentiation.

By contrast,

`AND -> XOR`

cannot be a conditioning step because `AND intersect XOR=FALSE`. If retained as a thesis idea, it belongs to unfolding/re-description rather than measurement.

---

## 14. Optional probabilistic and modal enrichments

### Classical probabilistic extension

Add a prior `p` and use ordinary conditioning. This immediately yields expected information gain and allows empirical estimation.

### Generalized probabilistic extension

A GPT requires a convex state space, an effect space of affine maps to `[0,1]`, measurements whose effects sum to the unit effect, and instruments/channels for post-measurement states. The core CM event algebra embeds into the classical simplex GPT but is not by itself a general GPT specification.

### Modal extension

A finite-field/ring model can instead use possibility/necessity: states are admissible module vectors; effects are covectors; an outcome is possible when the contraction is nonzero; measurements are declared context families of effects. Contextuality then becomes a global-section/support question. These axioms are additional to CM truth-table representation.

---

## 15. Recommended terminology

For a future paper, use:

- **CM** for compact truth-table operator `[Theta]`;
- **truth effect** or **valuation projector** for `D_Theta`;
- **observation refinement** for adding tests;
- **selective measurement/update** for support restriction;
- **conditioning** only when a probability state is present;
- **unfolding** for a representation/refinement transform that exposes latent alternatives;
- **modal measurement** only after a complete modal state/effect/context contract has been stated.

Avoid using "collapse," "pure," "superposition," "observable," or "entanglement" without defining the exact mathematical sense each time.
