# U5 — Cartesian fiber-saturation theorem

## Verdict

**VALID AS STATED.** The theorem is a clean ProLT specialization of an elementary pullback/fiber-saturation fact.

For `T subseteq S`, form

\[
\begin{array}{ccc}
F_T&\longrightarrow&P_T\\
\downarrow&&\downarrow\\
F_S&\longrightarrow&P_S.
\end{array}
\]

The vertical arrows are inclusions induced by support restriction. The pullback of `F_S -> P_S` along `P_T -> P_S` is exactly

\[
\pi^{-1}(P_T)=\{(p,a):p\in P_T,\ a\in B_p^S\}.
\]

Meanwhile

\[
F_T=\{(p,a):p\in P_T,\ a\in B_p^T\}.
\]

Therefore the square is cartesian iff

\[
B_p^T=B_p^S
\qquad\forall p\in P_T.
\]

This is stronger than merely saying `T` meets the same coarse fibers. It says every surviving coarse fiber retains every **fine signature type** previously present over it.

The left `Q/F` thinning square is always a pullback because both posets are restricted to exactly the same surviving fine-signature vertices and `Q` is the same-vertex suborder of `F`.

## Saturation terminology

Ordinary saturation for a quotient `q:S->P` is

\[
T=q^{-1}(q(T)),
\]

i.e. `T` is a union of whole coarse fibers. U5 is naturally viewed as a **profile saturation** statement at the intermediate expansion level. Ordinary coarse saturation implies the U5 profile condition, but the two notions should not be silently conflated when `T` is not known to be a union of fine cells.

## Exhaustive verification

All 90,880 support/refinement cases generated from the 355 four-world observation preorders passed. An independent partition-only implementation checked 3,840 partition/bit/event cases with zero failures.
