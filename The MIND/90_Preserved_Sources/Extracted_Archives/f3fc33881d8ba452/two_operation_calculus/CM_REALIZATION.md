# CM Realization of the Measurement Side

## 1. Exact bridge

For a binary Boolean operator `Theta`, the current CM paper fixes the true-first frame `(11,10,01,00)` and represents the truth table as

\[
[\Theta]=
\begin{pmatrix}
\Theta_{11}&\Theta_{10}\\
\Theta_{01}&\Theta_{00}
\end{pmatrix}.
\]

Define the truth event

\[
E_\Theta=\{11,10,01,00\text{ positions at which }\Theta=1\}.
\]

Then define

\[
\mathsf D_\Theta
=
\operatorname{diag}(\Theta_{11},\Theta_{10},\Theta_{01},\Theta_{00}).
\]

The maps

\[
\Theta\longleftrightarrow [\Theta]
\longleftrightarrow E_\Theta
\longleftrightarrow \mathsf D_\Theta
\]

are bijective at the level of Boolean truth data.

## 2. Boolean-algebra embedding

With pointwise Boolean operations on truth functions/events and diagonal multiplication on effects,

\[
\mathsf D_{\Theta\wedge\Psi}
=
\mathsf D_\Theta\mathsf D_\Psi,
\qquad
\mathsf D_{\neg\Theta}=I-\mathsf D_\Theta
\]

over ordinary characteristic-zero scalars, with the obvious Boolean/complement reading over `F_2`.

All sixteen diagonal truth effects are idempotent. Their rank is truth-support cardinality.

## 3. What the compact CM contributes

The compact CM is useful because it is:

- a typed 2x2 reshaping of binary truth data;
- compatible with the current CM/LM frame calculus;
- linked to formula-valued LM structure and signed input-frame transformations;
- a concise bridge from named connectives to their valuation supports.

But the diagonal projector algebra itself is essentially the ordinary Boolean algebra of subsets of the four valuation points. It should not be advertised as a new projector theory.

## 4. Why this is not Eigenlogic by another name

Eigenlogic is direct prior art for representing propositions by commuting projection operators with truth values as eigenvalues. The present CM route differs in architecture: the compact 2x2 CM and formula-valued LM are primary symbolic/numeric truth-table representations, and the 4x4 diagonal projector is an explicit *bridge* to valuation-space effects.

That distinction can be useful, but it narrows rather than enlarges novelty claims.

## 5. Recommended terminology

- `[Theta]`: **compact correspondence matrix / observable encoding**;
- `E_Theta`: **truth event / support**;
- `D_Theta`: **diagonal truth effect/projector**;
- `M_Theta`: **selective conditioning map**.

Do not call `[Theta]` itself a measurement projector unless the multiplication law and idempotence property have separately been stated.
