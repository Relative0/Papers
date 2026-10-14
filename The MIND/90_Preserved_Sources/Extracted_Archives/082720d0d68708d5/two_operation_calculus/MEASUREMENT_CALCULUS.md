# Measurement / Conditioning Calculus

## 1. Primitive hard outcome

Let `E subseteq Omega` be an event. A recorded true outcome acts by

\[
M_E(S,\Phi)=(S\cap E,\Phi).
\]

The false outcome uses `Omega\E`.

This is **conditioning/restriction**, not observation-interface refinement.

## 2. Algebra

For fixed ambient events:

\[
M_E^2=M_E,
\qquad
M_E M_F=M_{E\cap F}=M_FM_E.
\]

Thus hard classical measurements also form an idempotent commutative semilattice action.

Impossible outcome: `S cap E = empty`.  
Nondestructive outcome on support: `S subseteq E`.  
Redundant relative to `S`: `S cap E = S`.

## 3. Complete versus selective measurement

The yes/no question associated with `E` is the partition

\[
\{E,\Omega\setminus E\}.
\]

If both outcome branches are retained with labels, no world need be discarded. A **selective** branch performs `S -> S cap E` or `S -> S cap E^c`.

This separation is useful for the thesis language: the question creates or invokes a distinction, whereas a recorded outcome selects a branch.

## 4. CM realization

For a binary connective `Theta` on valuation order `(11,10,01,00)`, let

\[
E_\Theta=\{v:\Theta(v)=1\}.
\]

The compact CM

\[
[\Theta]=
\begin{pmatrix}
\Theta_{11}&\Theta_{10}\\
\Theta_{01}&\Theta_{00}
\end{pmatrix}
\]

is an exact reshaping of the characteristic vector of `E_Theta`.

The canonical truth-effect operator is instead

\[
D_\Theta=
\operatorname{diag}(\Theta_{11},\Theta_{10},\Theta_{01},\Theta_{00}).
\]

Then

\[
D_\Theta^2=D_\Theta,
\qquad
D_\Theta D_\Psi=D_{\Theta\wedge\Psi},
\qquad
\operatorname{rank}D_\Theta=|E_\Theta|.
\]

All 16 binary truth effects are therefore commuting sharp projectors on the four-dimensional valuation basis. This is distinct from asking which compact 2x2 arrays are idempotent under a chosen compact-CM product.

## 5. Probability extension

Given probability `p` with `p(E)>0`, selective conditioning is

\[
p_E(x)=\frac{p(x)1_E(x)}{p(E)}.
\]

A pointwise realized outcome does **not** guarantee that Shannon entropy decreases; rare conditioning can increase the entropy of the normalized posterior. The robust information statement is expected information gain / mutual information across outcomes.

## 6. Modal extension

A modal finite-field or chain-ring measurement theory requires additional primitives: a state module, admissible effects, a state-effect pairing, an outcome-possibility rule, and measurement contexts. None of these follows merely from the compact CM truth table. The project should keep the classical event-conditioning calculus and the separate modal-support calculus typed apart.
