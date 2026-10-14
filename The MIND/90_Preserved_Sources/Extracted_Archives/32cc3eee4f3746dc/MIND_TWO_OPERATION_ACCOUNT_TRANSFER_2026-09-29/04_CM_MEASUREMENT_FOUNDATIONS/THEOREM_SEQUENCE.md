# Proposed Theorem Sequence for a CM Measurement Paper

A short, coherent paper can be built without making claims about physical consciousness or quantum mechanics. The natural title would be something like **"Boolean Observation and Measurement from Correspondence Matrices"** or **"Correspondence-Matrix Effects, Observation Refinement, and Logical Differentiation."**

## T1. CM-event-projector equivalence

Let `Omega_2={11,10,01,00}`. The following are canonically bijective once the true-first frame is fixed:

1. binary Boolean functions `Theta`;
2. compact CMs `[Theta] in {0,1}^{2x2}`;
3. subsets `E_Theta subseteq Omega_2`;
4. diagonal 0/1 projectors `D_Theta` on `K^{Omega_2}`.

The bijection preserves Boolean complement and meet at the event/projector level.

**Purpose:** establishes the exact measurement bridge without identifying the compact CM with the projector.

## T2. Sharp selective measurement theorem

For support states `S subseteq Omega_n`, define `M_f(S)=S intersect E_f`. Then `M_f` is idempotent. In valuation-space form `D_f` has

`im D_f = span(E_f)`, `ker D_f=span(E_f^c)`, and `rank D_f=|E_f|`.

**Purpose:** gives the rigorous replacement for the thesis's projection/measurement definition.

## T3. Sequential-measurement theorem

For Boolean effects `f,g`,

`D_fD_g=D_gD_f=D_(f and g)`

and

`M_g M_f = M_f M_g = M_(f and g)`.

Corollary: the canonical CM sharp-effect theory has no intrinsic order effects and is a classical Boolean measurement algebra.

## T4. Complete compact-CM idempotent classification

Among the 16 compact binary CMs:

- XOR-AND over `F_2`: exactly 8 idempotents;
- OR-AND Boolean-semiring product: exactly 11;
- ordinary integer/real matrix product: exactly 8;
- cyclic `F_2` convolution on quarter-turn coordinates: exactly 2.

Give the explicit lists and characterize the four compact `F_2` idempotents that are also symmetric.

**Purpose:** closes the natural finite classification while emphasizing type dependence.

## T5. Outer-product projector criterion

For rank-one `P=|alpha><beta|` in any scalar setting where the contraction is defined,

`P^2=<beta|alpha>P`.

Hence a nonzero `P` is idempotent iff `<beta|alpha>=1`. In particular `|1><0|` is nilpotent rather than projective.

**Purpose:** repairs the central historical definition transparently.

## T6. Stabilizer non-monotonicity under logical restriction

Under the signed-input `D_4` action on binary truth supports, strict nonempty restriction `S -> S intersect E` does not monotonically change stabilizer size. Exhibit both an increase and a decrease; optionally state the full finite count `8/30/72` for increase/decrease/same.

Add the general lemma: if `M` is `G`-equivariant then `Stab_G(x) subseteq Stab_G(M(x))`.

**Purpose:** proves that symmetry breaking and distinguishability are distinct notions.

## T7. Observation-refinement criterion

For an observation family `Phi` and new observation `psi`, refinement is strict on a carrier `S` iff `psi` is nonconstant on at least one `Phi`-signature class in `S`.

**Purpose:** supplies the exact notion of increased distinguishability.

## T8. Cylinder-context theorem

If a formula `f` is embedded from `n` variables into `n+m` by ignoring the new variables, then

`E_iota(f)=E_f x {0,1}^m`,

so `|E_iota(f)|=2^m|E_f|` and `rank D_iota(f)=2^m rank D_f`.

Corollary: singleton-support "purity" is not preserved by adjoining an unconstrained variable.

**Purpose:** resolves the thesis's context-dependence observation as ordinary cylinder extension.

## T9. Refinement-update commutative square

At fixed carrier, adding an observation and then restricting to an independently defined event gives the same restricted observation system as restricting first and then adding the restricted observation.

**Purpose:** gives the precise relationship between unfolding/refinement `U` and measurement/update `M` and identifies the hypotheses under which `MU=UM`.

## T10. Classicality boundary

The canonical CM truth effects form a commuting Boolean algebra of sharp projectors. Consequently no sheaf-theoretic contextuality or noncommutative measurement order effect can arise from this full effect algebra alone.

**Purpose:** prevents overclaiming and cleanly motivates a separate modal extension.

## T11. Optional modal-extension schema

State as a *schema*, not as a consequence of T1-T10: a nonclassical extension must specify

- scalar semiring/ring/field;
- admissible states;
- effects and measurement contexts;
- composite-system tensor product;
- possibility/probability rule;
- post-measurement/process semantics.

Only after these are fixed should contextuality, interference, teleportation, or noncommuting measurement theorems be formulated.

**Purpose:** creates a principled bridge to the separate finite-field/chain-ring program without contaminating the core Boolean measurement results.

## Suggested paper narrative

Start from the historical projector mistake, repair it by the valuation-space diagonal effect, prove the classical measurement algebra, then use ProLT to show that **distinguishing** is properly a refinement property rather than a collapse property. The compact-CM idempotent classification and stabilizer counterexamples make strong finite sections. End with the exact boundary between classical CM observation and genuinely modal contextual extensions.
