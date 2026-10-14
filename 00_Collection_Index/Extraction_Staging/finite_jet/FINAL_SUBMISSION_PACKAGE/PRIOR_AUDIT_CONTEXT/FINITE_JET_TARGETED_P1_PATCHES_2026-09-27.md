# Targeted P1 Patches for the Current 14-page Finite-Jet Note

These are proposed textual patches only. They do not silently modify the current manuscript.

## Patch 1 - Broglia--Tognoli applicability and leading-term antecedent

Replace the part of the introduction that says the hyperplane hypotheses “therefore apply” with:

> The smooth arrangement conclusion below is a consequence of the signature-flatness theorem of Broglia and Tognoli. Given a function nonzero off the arrangement, multiplication by the square of every defining affine form produces a function with zero set exactly the arrangement while preserving chamber signs and nonflatness. For $n\ge2$, their homology hypothesis is automatic on $\mathbb R^n$; hyperplane components have global affine equations and are arc-analytically connected, so their theorem applies. The one-dimensional case is elementary and is covered directly below. For a hyperplane arrangement their admissible signatures are precisely the signed-parity laws. Their motivating crossing example already uses the first nonzero Taylor coefficient to force an even/odd parity contradiction; the purpose here is to isolate that mechanism systematically for arbitrary arrangements and finite regularity, not to claim its invention.

## Patch 2 - finite-order quantifier precision

Replace:

> The $C^\infty$ flatness statement is the simultaneous all-orders version of this finite-order obstruction.

with:

> The smooth theorem is a stronger all-orders analogue: it yields a single flat point. The finite-order statements alone do not imply that conclusion by letting $N$ tend to infinity, because the point at which the $N$-jet vanishes may depend on $N$.

## Patch 3 - constructive antecedent

Replace the Langenbruch Proposition 1 pinpoint paragraph with:

> A stronger existence statement is classical. Rainer's Remark~3.13, citing work of Langenbruch, states that for every nonquasianalytic weight sequence and every closed set $A$ there exists an ultradifferentiable function flat on $A$ and positive real analytic on its complement. Taking $A=(-\infty,0]$ gives a one-sided selector. More generally, taking $A$ to be the arrangement and multiplying this positive flat function by an arbitrary locally constant sign on the chambers, then extending by zero on $A$, directly realizes every chamber labeling in the same class. We nevertheless retain the squared-cutoff selector and finite chamber sum because they give an explicit elementary formula adapted to the defining affine forms.

## Patch 4 - polynomial antecedent

At the start of the polynomial-sign literature paragraph, use:

> The factor-parity mechanism is classical. In Broglia--Tognoli Proposition~2.4, maximal powers of irreducible defining polynomials determine whether a polynomial-induced signature changes sign along each component; for hyperplanes this is exactly the parity-bit argument used here. A later MathOverflow discussion gives the same observation in the coordinate-orthant language.

Then either remove the MathOverflow citation or retain it only as a secondary informal pointer.

## Patch 5 - contribution sentence

Prefer:

> The contribution of the note is therefore not the first-nonzero-Taylor-term idea itself, but its systematic arrangement-level packaging, the explicit finite-order formulations, and the normalized synthesis with ultradifferentiable realization and exact counts.

over the stronger-sounding phrase “leading-jet proof architecture” when standing alone.

## Patch 6 - optional arrangement reference

Add to the bibliography if desired:

> A. Björner, M. Las Vergnas, B. Sturmfels, N. White, and G. M. Ziegler, *Oriented Matroids*, 2nd ed., Encyclopedia of Mathematics and its Applications 46, Cambridge University Press, 1999.

Use it only to anchor the standard chamber/sign-vector/topes language; it is not needed for the analytic proof.
