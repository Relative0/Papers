# Refinement--Measurement Interaction

## 1. Strongest negative result

In the deterministic fixed-carrier base theory, fixed refinements and fixed event-conditionings **always commute**.

Let

\[
R_\psi(S,\Phi)=(S,\Phi\cup\{\psi\}),
\qquad
M_E(S,\Phi)=(S\cap E,\Phi).
\]

Then

\[
M_E R_\psi(S,\Phi)
=
(S\cap E,\Phi\cup\{\psi\})
=
R_\psi M_E(S,\Phi).
\]

This is not a special CM theorem; it follows because the two maps act on separate coordinates.

Exhaustive verification over all 15 partitions, 16 supports, 16 refinement events and 16 measurement events checked **61,440 squares and found zero failures**. At the positive-topology level, 90,880 distinct `(topology, refinement, surviving carrier)` cases likewise commuted under induced-subspace restriction.

The existing ProLT v0.3 result is even more important historically for this project: it already proves after T0 that observation refinement and premise accumulation commute as simplicial inclusions and generate a two-parameter bifiltration. The new audit therefore does **not** claim the commutative square as a new theorem.

## 2. Sequential normal form

For any finite word built from fixed refinements `R_psi_i` and fixed hard outcomes `M_E_j`, commutativity and idempotence give the normal form

\[
(S,\Phi)
\longmapsto
\left(
S\cap\bigcap_j E_j,
\Phi\cup\{\psi_i\}_i
\right),
\]

independent of interleaving and duplicate operations.

The computation directly checked all underlying idempotence/commutation identities required for this normal form.

### Consequence

The primitive calculus cannot generate intrinsic order effects. If order dependence is desired, one must add more structure rather than interpret ordinary intersection as noncommutative measurement.

## 3. The important nontriviality is *typing*, not noncommutation

Suppose only events in the current Boolean algebra `A_Phi` are operationally measurable. Under refinement,

\[
\mathcal A_\Phi\subseteq\mathcal A_{\Phi\cup\{\psi\}}.
\]

Then a prospective event `E` falls into three classes:

1. **persistent:** `E in A_Phi`; measurement exists before and after refinement;
2. **enabled by refinement:** `E notin A_Phi` but `E in A_{Phi+psi}`;
3. **unavailable:** `E` is not measurable even after that refinement.

Across all 61,440 four-world squares the counts were:

- persistent: 24,064;
- enabled by refinement: 13,504;
- unavailable even after: 23,872.

For an enabled event, the apparent expression `R M` is not a competing route: the pre-refinement `M` arrow is **not well typed**. This is a much cleaner interpretation than claiming physical noncommutativity.

## 4. A natural operational composite

A new measurement question can be represented as a two-stage process:

\[
\boxed{Q_{\theta=b}=M_{\theta=b}\circ R_\theta.}
\]

First the interface gains the question `theta`; then an outcome branch is recorded. If `theta` was already available, `R_theta` is redundant.

This directly implements the proposed phrase:

> refinement of what can be distinguished, followed by conditioning of what remains possible.

## 5. When can MR and RM genuinely differ?

At least one base assumption must be relaxed.

### (a) Context-dependent event

If the event selected by a symbol `E` itself depends on `Phi`, then refining `Phi` can change the event and order can matter.

### (b) Disturbing instrument

Replace hard restriction by a state transformation `T_E` that changes more than support. Noncommuting instruments can then produce genuine order effects.

### (c) Adaptive protocol

Let the next refinement depend on a previous outcome. Different branches now use different future tests. This is classically order-sensitive as a decision protocol, although not because set intersections fail to commute.

### (d) Carrier-changing map

For a refinement map `f:Omega' -> Omega`, pullback conditioning commutes automatically:

\[
f^{-1}(S\cap E)=f^{-1}(S)\cap f^{-1}(E).
\]

Direct images need not preserve intersections. Thus noncommutation under carrier change is possible when pushforward, quotienting, or loss of fibre information is involved.

### (e) Contextual/non-Boolean effect structure

If effects do not live in one global Boolean event algebra, a single global intersection calculus no longer exists. That is the cleanest route to genuinely nonclassical measurement structure.
