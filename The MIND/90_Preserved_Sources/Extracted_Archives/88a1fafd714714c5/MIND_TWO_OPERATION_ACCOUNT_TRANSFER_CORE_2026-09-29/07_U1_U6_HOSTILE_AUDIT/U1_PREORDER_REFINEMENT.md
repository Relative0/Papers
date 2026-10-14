# U1 — Preorder refinement by intersection

## Verdict

**VALID AS STATED.** The result is exact, but it is essentially definitional once the observation preorder is defined coordinatewise. It should be retained as the foundational bookkeeping lemma, not advertised as a new theorem.

Let `S` be a finite support and let every observation `phi` take values in a preorder `A_phi`. Define

\[
x\preceq_{\Phi,S}y
\iff
x,y\in S\ \text{and}\ \phi(x)\le_{A_\phi}\phi(y)\quad\forall\phi\in\Phi.
\]

Boolean values are not essential. Any preordered codomains work.

For observation families `Phi,Theta`,

\[
\preceq_{\Phi\cup\Theta,S}
=
\preceq_{\Phi,S}\cap\preceq_{\Theta,S}.
\]

For `T subseteq S`,

\[
\preceq_{\Phi,T}
=
\preceq_{\Phi,S}\cap(T\times T).
\]

The second identity is simultaneously the restriction of a relation, the induced subpreorder, and—under the finite Alexandrov correspondence—the specialization preorder of the induced subspace.

## Hidden hypotheses

1. Each observation must be a total map on the carrier under consideration. Partial observations require either restricting their domains or adding an explicit undefined value/order.
2. The observation codomain must carry a preorder if the coordinatewise order definition is to make sense.
3. Duplicated/indexed observations do not change the induced relation unless later weights/costs use multiplicity.

## Novelty classification

Finite topological spaces are classically equivalent to finite preorders, and `T0` is exactly antisymmetry. The intersection identity adds no independent novelty. Its value is architectural: it puts refinement and support restriction in one relation calculus.
