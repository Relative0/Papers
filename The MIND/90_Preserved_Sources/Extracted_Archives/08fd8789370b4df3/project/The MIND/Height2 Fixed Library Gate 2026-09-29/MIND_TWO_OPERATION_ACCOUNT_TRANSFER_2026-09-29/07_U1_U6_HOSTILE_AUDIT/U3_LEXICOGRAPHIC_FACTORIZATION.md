# U3 — Lexicographic fiber-expansion / thinning factorization

## Verdict

**VALID AS STATED**, with two qualifications about positioning:

1. the intermediate object really is the standard **lexicographic sum of posets**;
2. the lexicographic construction itself is standard. The project-specific content is its use as the canonical intermediate object attached to a ProLT observation refinement.

## Setup

For `Psi=(Phi,Theta)` and support `S`, let

\[
P=P_{\Phi,S}.
\]

For each coarse signature `p`, let `C_p` be its coarse class and

\[
B_p=\{\alpha_\Theta(x):x\in C_p\}\subseteq\{0,1\}^{\Theta}
\]

with coordinatewise order. The fine signature poset is

\[
Q=\{(p,a):p\in P,\ a\in B_p\},
\]

with product condition

\[
(p,a)\le_Q(q,b)
\iff
p\le_Pq\ \text{and}\ a\le b.
\]

Define the lexicographic sum

\[
F=\sum_{p\in P}B_p
\]

by

\[
(p,a)\le_F(q,b)
\iff
\begin{cases}
a\le b,&p=q,\\
\text{true},&p<q,\\
\text{false},&p\parallel q.
\end{cases}
\]

This matches the standard definition: substitute the fiber poset `B_p` for each point `p`, and make every element of the `p`-fiber precede every element of the `q`-fiber whenever `p<q`.

## The factorization

There is a canonical factorization

\[
Q\xhookrightarrow{j}F\xrightarrow{\pi}P,
\qquad
\pi(p,a)=p.
\]

`Q` and `F` have the same vertices. The inclusion `j` removes exactly those cross-fiber relations for which the new labels violate `a<=b`. Projection `pi` is surjective and monotone, and the usual fine-to-coarse map is \(\pi\circ j\).

Literal canonicality holds once the realized signature sets are fixed. Under abstract relabeling, the construction is canonical up to the obvious isomorphism.

## T0 specialization

If `Phi` is relatively `T0` on `S`, each coarse class contains one world. Therefore each `B_p` contains one realized new label, so

\[
F\cong P.
\]

U3 then reduces exactly to same-vertex order thinning.

## Additional structural observation

The projection `pi:F->P` is an open surjection in the Alexandrov/up-set topology: if an upset in `F` meets a fiber over `p`, it contains every whole fiber over each `q>p`. Hence it is also a topological quotient map. This is useful but still standard lexicographic-sum behavior.

## Independent finite verification

- 5,680 observation-generated four-world transitions: zero U3 failures.
- independent abstract-poset/fiber verifier through four base points: 3,450 cases, zero failures.

## Priority assessment

Do **not** claim invention of the lexicographic sum, substitution, or fibered-poset idea. A defensible contribution claim, if desired, is narrower: the ProLT fiber-profile refinement has a canonical lexicographic-expansion intermediate that isolates splitting from cross-fiber descent thinning.
