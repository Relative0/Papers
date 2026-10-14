# Independent-Phase Literal-Tensor Robustness Audit

## Purpose

This audit challenges the strongest hidden assumption in the previous native Boolean CM rebuild: the **shared four-bit phase register**.

The test here gives each logical subsystem its **own** four-position CM phase register and composes subsystems by the ordinary Boolean Kronecker tensor product. There is no phase-compression map between parties and no separate coefficient-product primitive.

All matrices contain only Boolean entries. Matrix composition uses **AND on routed bits and XOR on converging routes**.

The local state space is

\[
L = B^2_{\text{logical}} \otimes B^4_{\text{phase}},
\]

so one local system has Boolean vector dimension 8. Therefore:

- one local system: 8 Boolean coordinates,
- two parties: \(8\times 8=64\) coordinates,
- three parties: \(8^3=512\) coordinates.

The native phase rotation remains

\[
P^4=I_4,
\]

acting on the four phase positions.

---

## Headline result

The robustness test is **partly positive and partly corrective**.

1. The Bell possible/impossible contradiction survives literal tensoring exactly in the embedded `Z/X/Y` family.
2. The support GHZ contradiction survives literal tensoring exactly, including the same minimum six-context contradiction.
3. The 15-class contextuality hierarchy for the Choi/operator lift has the **same aggregate strong/logical/local classification and coverage counts** over all 192 rotation-compatible local bases, even though thousands of individual basis-pair support tables change in some classes.
4. The previous compact **four-outcome** universal teleportation protocol does **not** survive when phase registers are independent. The four logical outcomes leave unresolved Alice phase-pair degrees of freedom.
5. Universal exact teleportation nevertheless **does survive** in the fully literal independent-register theory when Alice performs a complete **64-outcome** Bell analysis on the full 8-by-8 local space.
6. For this full literal protocol, the resource criterion remains exactly **full Boolean rank 8**. Among the 65,536 P-block resources, exactly 24,576 are universal resources.
7. A complete Bell analyzer whose every reshaped branch map is Boolean-orthogonal is impossible under the standard transpose bilinear form in even local dimension: flattened orthogonal matrices all have even Hamming weight and therefore lie in a 63-dimensional hyperplane of the 64-dimensional matrix space.

So the shared-register formalism did **not invent** Bell, GHZ, contextuality, or universal Boolean teleportation. It **compressed** the phase degrees of freedom, most visibly reducing the teleportation outcome count from 64 to 4.

---

# 1. Two literal bipartite lifts

Two distinct literal embeddings are useful and should not be conflated.

## 1.1 Anchor lift

The logical Bell state with a fixed phase anchor is

\[
|0,E_0\rangle_A|0,E_0\rangle_B
\oplus
|1,E_0\rangle_A|1,E_0\rangle_B.
\]

As an 8-by-8 coefficient matrix this has Boolean rank 2.

This state carries only the logical Bell correlation; it does not maximally correlate the independent phase registers.

## 1.2 Choi/operator lift

If the old coefficient object is an 8-by-8 Boolean transfer matrix \(M\), its natural literal bipartite state is the vectorization

\[
|M\rangle\rangle
=
\bigoplus_{i,j} M_{ij}|i\rangle_A|j\rangle_B.
\]

For the support-Bell identity resource,

\[
M=I_8,
\]

so

\[
|I_8\rangle\rangle
=
\bigoplus_{j=0}^{7}|j\rangle_A|j\rangle_B.
\]

This correlates **both** the logical bit and the four-position phase register.

For local effects \(e,f: B^8\to B^4\), literal tensor support is

\[
(e\otimes f)|M\rangle\rangle\neq0.
\]

The code independently verifies the equivalent ordinary Boolean matrix identity

\[
(e\otimes f)|M\rangle\rangle\neq0
\quad\Longleftrightarrow\quad
e M f^T\neq0.
\]

---

# 2. Bell contradiction survives

For both the anchor lift and the Choi lift, the embedded `Z/X/Y` possible/impossible tables are exactly

| settings | outcomes `00,01,10,11` |
|---|---|
| ZZ | `1001` |
| ZX | `1110` |
| ZY | `0111` |
| XZ | `1110` |
| XX | `0111` |
| XY | `1001` |
| YZ | `0111` |
| YX | `1001` |
| YY | `1110` |

All \(2^6=64\) deterministic assignments to Alice's and Bob's three settings were checked, and **zero** satisfy all support constraints.

Thus the Bell/modal contradiction is not an artifact of phase-register sharing.

Raw file: `data/bell_literal_tensor_tables.csv`.

---

# 3. Contextuality hierarchy survives in aggregate, but not table-by-table

The previous 192 measurement bases are still well-defined as all projective two-outcome bases coming from reversible **P-compatible** 8-by-8 block gates.

Important scope statement:

> In the independent-register theory these 192 bases are **not** all possible `GL(8,2)` local analyzers. They are the complete rotation-compatible family inherited from the CM phase-block construction.

For each canonical class

\[
M_{a,b}=\operatorname{diag}(N^a,N^b),
\qquad N=P\oplus I,
\]

the literal Choi state \(|M_{a,b}\rangle\rangle\) was evaluated over all

\[
192^2=36,864
\]

basis pairs.

The aggregate classification is unchanged:

| class type | classes | states |
|---|---:|---:|
| strong contextual | 4 | 26,214 |
| logical contextual, not strong | 6 | 34,056 |
| nonzero relationally local | 4 | 5,265 |
| zero | 1 | 1 |

The exact possible/extendable/uncovered counts also match the shared-register computation class-by-class.

However, this is **not merely the same table in disguise**. Several classes have many basis-pair tables that differ:

| class | differing basis-pair tables out of 36,864 |
|---|---:|
| (0,0) | 5,952 |
| (0,1) | 7,936 |
| (0,2) | 4,096 |
| (1,1) | 11,520 |
| (1,2) | 8,192 |
| many deeper classes | 0 |

So literal tensoring changes detailed support structure but leaves the contextuality hierarchy and aggregate coverage invariant for this family.

This is a stronger robustness result than a simple regression match.

Raw files:

- `data/contextuality_literal_choi_by_rotation_class.csv`
- `data/shared_vs_literal_context_table_differences.csv`

---

# 4. Support GHZ survives literal tensoring

A natural full local GHZ state is

\[
|\mathrm{GHZ}_8\rangle
=
\bigoplus_{j=0}^{7}|j,j,j\rangle,
\]

where \(j\) runs over the combined logical-plus-phase local basis.

Under embedded `Z/X/Y`, its 27 possible/impossible tables exactly reproduce the previous support-GHZ tables.

All \(2^9=512\) deterministic global assignments fail.

An exhaustive minimum-unsatisfiable-context search proves that no set of one through five contexts suffices. A contradiction first appears at six contexts, with the same settings:

\[
ZZZ,\; ZXX,\; XZY,\; XXX,\; YYZ,\; YYY.
\]

So the support GHZ contradiction is also not an artifact of a shared phase register.

For the four P-compatible Boolean-orthogonal bases, this literal GHZ has 1,024 compatible global assignments and every possible section extends, so that restricted family remains relationally local.

Raw file: `data/ghz_literal_support_contexts.csv`.

## Weighted GHZ warning

There is **no unique three-party Choi lift** of one shared phase operator. As an exploratory test, the audit applied \(N^2\) to Charlie's phase leg of the `|111>` term.

That particular lift is local over embedded `Z/X/Y` (16 global assignments, all possible sections covered) but becomes logically contextual over the four P-compatible orthogonal bases (291 globals, 28 possible sections without global extension).

This is deliberately recorded as an exploratory variant, not as a canonical theorem. It shows that the three-party weighted construction needs a separate definition rather than silently inheriting the shared-register version.

---

# 5. The old four-outcome universal teleportation does not survive literally

This is the clearest failure found by the robustness test.

With independent phase registers, Alice's two local systems span

\[
8\times8=64
\]

Boolean dimensions.

If Alice applies only the old four-outcome logical Bell analyzer, leaving both phase registers untouched, each logical outcome still carries a 16-dimensional Alice phase-pair residual.

The audit constructs this full 64-by-64 pair analyzer and the complete 512-dimensional input-resource evolution.

For **each** of the four logical outcomes:

- the global postselected map has rank 8,
- all 16 Alice phase-pair residual sectors are nonzero,
- those 16 sectors induce **16 distinct** Bob maps,
- each residual Bob map has rank 2,
- the branch does **not** factor as one fixed Alice residual state tensor one Bob-only invertible map.

Therefore after only the four logical outcomes Bob does not possess the arbitrary 8-bit local state.

This precisely identifies what the shared phase register was doing: it compressed these phase degrees of freedom into the coefficient algebra.

---

# 6. Universal teleportation survives with 64 complete outcomes

The failure above does **not** destroy universal exact teleportation.

A complete reversible Bell analyzer for two independent local 8-dimensional systems has 64 one-dimensional outcomes.

The audit constructs it in a factorized CM-readable form.

## 6.1 Four logical Bell effects

The existing four logical Bell effect matrices are four linearly independent invertible 2-by-2 Boolean matrices. They span the four-dimensional space of 2-by-2 Boolean matrices.

## 6.2 Sixteen phase Bell effects

The audit constructs sixteen linearly independent invertible 4-by-4 Boolean matrices spanning the full sixteen-dimensional 4-by-4 matrix space.

They are not foreign operations. Let

\[
T=I_4\oplus E_{01}
\]

be one elementary XOR shear. Exhaustive group generation gives

\[
\langle P,T\rangle = GL(4,2),
\]

with exactly

\[
20,160
\]

members.

Therefore every selected phase Bell effect is synthesized from the native rotation \(P\), its inverse, and this one simple Boolean XOR shear.

The 16-effect basis is recorded with explicit synthesis words in

`data/phase_bell_effect_basis_16.json`.

## 6.3 Sixty-four full effects

Taking

\[
R_{mn}=L_m\otimes V_n
\]

for the four logical effects \(L_m\) and sixteen phase effects \(V_n\) gives 64 invertible 8-by-8 Boolean matrices.

Their flattened rows are linearly independent, so they form an invertible 64-by-64 analyzer.

For the maximally correlated resource

\[
|I_8\rangle\rangle,
\]

Bob's branch map for outcome \((m,n)\) is an invertible Boolean map. Bob applies its Boolean inverse.

Every arbitrary local state

\[
\psi\in B^8
\]

was tested. There are \(2^8=256\) such vectors.

All

\[
256\times64=16,384
\]

input/outcome cases recover the input **exactly**.

A separate direct 512-dimensional simulation was compared with the compact branch-map formula for all 64 outcomes for both the full-rank identity resource and the rank-6 canonical `(0,2)` resource. They match exactly.

Raw file: `data/teleportation_literal_256x64.csv`.

---

# 7. Resource theorem survives

For a literal Choi resource \(|M\rangle\rangle\), and any of the invertible Bell effects \(R_m\), the Bob branch map has the Boolean matrix form

\[
T_m=M^T R_m^T.
\]

Since \(R_m\) is invertible,

\[
\operatorname{rank}(T_m)=\operatorname{rank}(M).
\]

Thus:

\[
\boxed{\text{universal exact literal-tensor teleportation}\iff \operatorname{rank}(M)=8}
\]

within this complete reversible Bell-basis architecture.

All 65,536 P-block resource matrices were enumerated. Exactly

\[
24,576
\]

have full rank 8.

Rank histogram:

| rank | resources |
|---:|---:|
| 0 | 1 |
| 1 | 9 |
| 2 | 78 |
| 3 | 648 |
| 4 | 5,280 |
| 5 | 5,760 |
| 6 | 10,752 |
| 7 | 18,432 |
| 8 | 24,576 |

For every one of the 15 canonical rotation classes, all 64 Bell outcomes have branch rank equal to the resource rank.

In particular the canonical `(0,2)` resource remains rank 6. It still cannot universally recover an arbitrary 8-bit state, but the full analyzer does not lose additional rank.

Raw file: `data/teleportation_literal_by_rotation_class.csv`.

---

# 8. Orthogonal-only universal Bell analyzer: structural no-go

The previous audit found that the compact teleportation protocol required reversible operations outside the Boolean-orthogonal subset. The independent-register test strengthens that negative result.

If an 8-by-8 Boolean matrix \(U\) is orthogonal,

\[
U^T U=I_8.
\]

Each of its eight columns has odd Hamming weight. Therefore the total number of `1` entries in \(U\) is the sum of eight odd integers, which is even.

Hence every flattened orthogonal 8-by-8 matrix lies in the even-weight hyperplane of the 64-dimensional Boolean matrix space. That hyperplane has dimension 63.

Therefore 64 reshaped orthogonal effects can never be linearly independent:

\[
\boxed{\text{no complete 64-outcome Bell analyzer can have every effect orthogonal}}
\]

under the standard transpose-based Boolean orthogonality condition.

As a lower-dimensional check, exhaustive enumeration finds 48 orthogonal 4-by-4 Boolean matrices, but their flattened span has dimension only 10 of 16.

This suggests that transpose-orthogonality is probably **too restrictive to serve as the full analogue of complex unitarity in characteristic two**, rather than indicating that the Boolean theory lacks reversible dynamics.

---

# 9. What survived and what failed

| question | literal independent phase registers |
|---|---|
| Native phase rotation \(P\) | survives |
| XOR interference | survives locally |
| Bell support contradiction | survives exactly |
| Support GHZ contradiction | survives exactly |
| Six-context minimum GHZ proof | survives exactly |
| 15-class contextuality hierarchy over 192 P-compatible bases | same aggregate classification/counts |
| Individual contextuality support tables | some change substantially |
| Old 4-outcome arbitrary-state teleportation | **fails** |
| Full arbitrary-state teleportation | **survives with 64 outcomes** |
| Full-rank resource criterion | survives |
| `(0,2)` universal teleportation | still fails, rank 6 |
| Complete orthogonal-only Bell analyzer | structurally impossible under current orthogonality definition |
| Weighted three-party phase construction | no unique literal lift; needs separate theory |

---

# 10. Interpretation

The most useful conclusion is not simply that the earlier shared-register theory was right or wrong.

The two constructions describe different ways of organizing the same Boolean ingredients:

- **shared phase register:** treats the four-position phase structure as a coefficient/operator algebra attached to logical branches;
- **independent phase registers:** treats phase as an explicit local subsystem and tensors it normally between parties.

The shared construction is substantially more compact. The independent construction exposes the phase degrees of freedom explicitly.

The fact that Bell, support GHZ, contextuality and full-rank teleportation survive the explicit construction is strong evidence that these effects are not merely artifacts of the shared-register encoding.

At the same time, the independent construction shows exactly what the compact encoding was buying: a four-outcome module-style teleportation protocol becomes a 64-outcome full Boolean Bell analysis when phase is promoted to an independent local subsystem.

That difference should be treated as a real structural distinction, not hidden.

---

# Reproducibility

Run:

```bash
python code/independent_tensor_audit.py
pytest -q
```

The generated audit run takes about 32 seconds in the supplied environment. The regression suite contains 12 tests.

