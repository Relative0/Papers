# U4 — Mapping-cone / octahedral defect sequence

## Verdict

**VALID WITH TERMINOLOGY REPAIR.** The orientation of the proposed triangle is correct under the standard cone convention, but the word **decomposition** must not be read as a direct-sum decomposition. What is obtained canonically is a distinguished triangle and a long exact sequence.

Let

\[
A=C_*(\Delta Q),\quad B=C_*(\Delta F),\quad C=C_*(\Delta P),
\]

and let

\[
f=j_*:A\to B,\qquad g=\pi_*:B\to C,\qquad h=gf=r_*.
\]

Use the homological cone convention

\[
\operatorname{Cone}(f)_n=B_n\oplus A_{n-1},
\]

\[
d(b,a)=(d_Bb+f(a),-d_Aa).
\]

Then the standard octahedral cone triangle is

\[
\operatorname{Cone}(f)
\longrightarrow
\operatorname{Cone}(gf)
\longrightarrow
\operatorname{Cone}(g)
\longrightarrow
\operatorname{Cone}(f)[1].
\]

One convenient pair of the first chain maps is

\[
\alpha(b,a)=(g(b),a),
\qquad
\beta(c,a)=(c,f(a)).
\]

The third morphism is the connecting map determined by the cone triangle; sign conventions vary with the chosen definition of shift/cone. The finite verifier uses one fixed convention and checks exactness on homology directly.

Define

\[
D_k^{\rm thin}=H_k\operatorname{Cone}(f),\qquad
D_k^{\rm total}=H_k\operatorname{Cone}(gf),\qquad
D_k^{\rm exp}=H_k\operatorname{Cone}(g).
\]

Then

\[
\cdots\to
D_k^{\rm thin}\to
D_k^{\rm total}\to
D_k^{\rm exp}\to
D_{k-1}^{\rm thin}\to\cdots.
\]

## Relative homology

Because `j:Delta Q -> Delta F` is a simplicial inclusion, with the convention above

\[
H_k\operatorname{Cone}(j_*)\cong H_k(\Delta F,\Delta Q)
\]

with **no degree shift**.

At relative `T0`, \(F\cong P\); therefore `pi` is an isomorphism and `Cone(pi_*)` is acyclic. Consequently

\[
D_k^{\rm total}\cong D_k^{\rm thin}
\cong H_k(\Delta P,\Delta Q).
\]

This recovers the existing post-T0 relative-homology formulation.

## No automatic direct sum

The long exact sequence does not imply

\[
D^{\rm total}\cong D^{\rm thin}\oplus D^{\rm exp}.
\]

A splitting requires additional hypotheses (for example, vanishing connecting maps plus algebraic splitting conditions); even over a field, a resulting vector-space splitting need not be natural.

## Verification

- exhaustive over F2 for all 5,680 four-world transitions: 62,934 exactness checks, zero failures;
- 18,982 relative-homology dimension checks, zero failures;
- all 3,504 post-T0 transition cases passed the acyclic-expansion/relative reduction check;
- independent exact-rational representative census: 1,420 cases, 15,387 exactness checks, zero failures.

The construction is coefficient-independent at the chain level; the integral statement follows formally from the same chain maps and the standard octahedral theorem, rather than from an exhaustive Smith-normal-form census.

## Priority assessment

The mapping-cone triangle for a composite is standard homological algebra. The possible project contribution is the **choice of U3 factorization to which it is applied**, not the octahedral sequence itself.
