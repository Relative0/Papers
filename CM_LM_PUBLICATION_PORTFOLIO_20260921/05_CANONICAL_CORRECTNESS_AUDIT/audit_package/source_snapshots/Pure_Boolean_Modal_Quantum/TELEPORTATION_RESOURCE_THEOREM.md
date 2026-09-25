# Teleportation Resource Theorem for the Pure-Boolean CM Ring

## Result

Let

`A = F2[C4] ~= F2[u]/(u^4)`

be the pure-Boolean CM coefficient ring, and represent a two-party resource state by its `2x2` coefficient matrix

`M = [[m00,m01],[m10,m11]]`.

Consider the same tight modal teleportation architecture used in this project:

1. an arbitrary unknown one-bit state `psi in A^2`;
2. a shared two-party resource `M`;
3. an arbitrary reversible analyzer `W in GL4(A)` acting on the unknown input and Alice's resource subsystem;
4. computational/modal readout of one of four analyzer outcomes; and
5. an outcome-conditioned `A`-linear correction on Bob's one-bit subsystem.

A resource is called **universally exactly teleportation-capable** when every nonzero input can be recovered exactly on every analyzer branch, with no quotient by global units.

## Theorem

**A two-party CM resource supports deterministic universal exact one-bit teleportation in this architecture if and only if its coefficient matrix is invertible. Equivalently, its determinant is a unit. Equivalently, its Smith class is `(0,0)`.**

Thus, among the ten nonseparable Smith classes, exactly one is a universal teleportation resource:

`(0,0)`.

All nine other nonseparable classes are teleportation-inadequate for arbitrary `A|0> XOR B|1>` under any reversible four-outcome analyzer and linear local correction.

## Proof

Write the analyzer row corresponding to outcome `m` as a length-four row and reshape it into a `2x2` matrix

`R_m[a,b] = W[m, 2a+b]`.

If the resource coefficient matrix is `M`, direct index contraction gives Bob's conditional branch map

`T_m = M^T R_m^T`.

Hence, because `A` is commutative,

`det(T_m) = det(M) star det(R_m)`.

Suppose branch `m` admits an exact `A`-linear correction `C_m` for every input. Then

`C_m T_m = I`.

Taking determinants gives

`det(C_m) star det(T_m) = E0`.

Therefore `det(T_m)` must be a unit. A product can be a unit only if both factors are units, so `det(M)` must be a unit. This proves necessity. In fact it proves the stronger statement that a singular resource cannot provide even one analyzer branch that is universally linearly correctable.

For sufficiency, use the already constructed pure-Boolean Bell analyzer

```text
W = Q^-1 =
[0 1 1 1]
[1 0 1 1]
[0 1 1 0]
[1 0 0 1]
```

where each `1` means `E0`.

Its four reshaped row matrices are

```text
R0 = [[0,1],[1,1]]
R1 = [[1,0],[1,1]]
R2 = [[0,1],[1,0]]
R3 = [[1,0],[0,1]]
```

and every determinant equals `E0`, so every `R_m` is invertible. If `M` is invertible then

`T_m = M^T R_m^T`

is invertible for every `m`. Bob therefore applies

`C_m = T_m^-1`,

which gives exact recovery for every `psi in A^2` and every outcome. Since each `T_m` is invertible, every nonzero input has a nonzero branch on every outcome.

This proves sufficiency.

## Smith-class corollary

Over the chain ring `A`, every two-party state is locally equivalent to

`diag(u^a,u^b)`, with `0 <= a <= b <= 4` and `u^4=0`.

Such a matrix is invertible exactly when both invariant factors are units, i.e. exactly when

`a=b=0`.

Therefore universal exact teleportation is a **Smith-class invariant** and the classification is complete:

| Smith class type | Contextuality under all 192 reversible projective bases | Universal exact teleportation |
| --- | --- | --- |
| `(0,0)` | Strong | **Yes** |
| `(1,1),(2,2),(3,3)` | Strong | No |
| `(a,b)`, `a<b<4` | Logical, not strong | No |
| `(a,4)`, `a<4` | Relationally local / separable | No |
| `(4,4)` | Zero state | No |

This separates three notions that had previously been partially conflated:

- nonseparability;
- possibilistic contextuality strength; and
- universal exact teleportation power.

Strong contextuality is not sufficient: the nonzero equal-valuation classes `(1,1)`, `(2,2)`, and `(3,3)` are strongly contextual but cannot teleport an arbitrary ring-valued one-bit state exactly.

## Exhaustive computational verification

The algebraic theorem does not depend on exhaustive search, but the implementation now checks the finite state space as a regression:

- all `65,536` two-party resource matrices were tested with the fixed pure-Boolean Bell analyzer;
- exactly `24,576` succeeded on all four branches;
- those `24,576` are exactly the matrices with unit determinant;
- those `24,576` are exactly Smith class `(0,0)`;
- every other Smith class had zero universal exact resources;
- all `8 x 16 = 128` nonunit-times-arbitrary-scalar products were checked to remain nonunits.

Since Smith class `(0,0)` contains `24,576` states, the theorem says that `24,576 / 60,270 ~= 40.78%` of the nonseparable two-party CM states are universal exact teleportation resources in this architecture.

Raw evidence:

- `data/teleportation_resource_theorem.json`
- `data/teleportation_resource_inventory_65536.csv`
- `data/teleportation_resource_by_smith_class.csv`

## Interpretation

The correct resource invariant is not merely “entangled/nonseparable.” In this ring-valued theory it is **full module rank**, equivalently unit determinant, equivalently Smith class `(0,0)`.

This is the chain-ring analogue of the familiar role played by full-Schmidt-rank/maximally entangled resources in tight ordinary teleportation, but the CM result is sharper in one respect: the zero-divisor structure produces many genuinely nonseparable and even strongly contextual states that nonetheless irreversibly lose module information and therefore cannot carry an arbitrary ring-valued state through a teleportation branch.

## Scope boundary

The theorem is for the project's explicit tight linear/modal architecture: one unknown `A^2` system, one two-party `A^2 tensor A^2` resource, one reversible `4x4` analyzer, four computational/modal outcomes, and outcome-conditioned `A`-linear corrections.

A follow-up investigation now classifies several of those sub-universal tasks; see `SINGULAR_TELEPORTATION_HIERARCHY.md`. In the same `A`-linear framework, singular classes can support restricted-state and quotient transfer, but **cannot** support even one postselected universally exact full-state branch. Product local ancillas and any finite tensor power of a singular resource also fail to activate universal exact teleportation by a residue-field-rank obstruction. Nonlinear operations or a different post-measurement calculus remain outside the theorem.

## Literature position

Finite-field/modal teleportation already exists in the literature, and Werner's ordinary finite-dimensional tight-teleportation classification relates tight teleportation to maximally entangled bases/unitary error bases. Categorical quantum mechanics also studies teleportation over more general scalar systems. The present theorem should therefore not be described as the first algebraic characterization of teleportation resources in a generalized quantum theory.

The narrower result established here is the explicit **CM chain-ring criterion** for this pure-Boolean model: unit determinant / Smith `(0,0)` is necessary and sufficient, while nine other nonseparable Smith classes fail despite retaining contextuality.
