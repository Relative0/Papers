# Sheaf Local-to-Global Analysis

## 1. Historical thesis seed

The thesis later moves from geometric face pictures to a more promising local-to-global idea: intersect concept topologies, compare shared information, and “look for compatible sections on presheaves” to create sheaves or higher-order concepts. This is mathematically close to genuine sheaf gluing, but the thesis does not establish that its presheaf satisfies the sheaf axiom.

That distinction is decisive.

## 2. Presheaf versus sheaf

Let \(X\) be a topological space (or use a finite Alexandrov/face-poset site). A presheaf \(\mathcal F\) assigns a set \(\mathcal F(U)\) to each open region and a restriction map
\[
\rho^U_V:\mathcal F(U)\to\mathcal F(V)
\]
for \(V\subseteq U\), functorially.

A Set-valued presheaf is a **sheaf** if, for every open cover \(U=\bigcup_iU_i\), sections \(s_i\in\mathcal F(U_i)\) satisfying
\[
s_i|_{U_i\cap U_j}=s_j|_{U_i\cap U_j}\quad\forall i,j
\]
glue to a unique \(s\in\mathcal F(U)\).

For ordinary Set-valued sheaves, pairwise overlap equality is the full compatibility condition. Triple and higher overlaps are automatically controlled by restriction functoriality. Higher coherence becomes a separate issue for stacks, higher categories, homotopical descent, etc.

## 3. Example D — compatible local presheaf data with no global section

Take the discrete two-point space \(X=\{p,q\}\) with cover
\[
U=\{p\},\qquad V=\{q\}.
\]
Define a presheaf \(P\) by
\[
P(W)=\mathbb Z\quad\text{for every nonempty open }W,
\qquad
P(\varnothing)=\{*\}.
\]
All restrictions between nonempty opens are the identity on \(\mathbb Z\); restrictions to \(\varnothing\) are the unique map.

Choose local sections
\[
s_U=0,\qquad s_V=1.
\]
Their overlap is empty, so both restrict to \(*\) and are compatible. A global section \(s\in P(X)=\mathbb Z\) would have to restrict by identity to both 0 and 1, which is impossible.

Thus \(P\) is a presheaf but not a sheaf.

### Important consequence

The prompt asks for “local pieces that pairwise appear compatible but do not admit the intended global gluing, if such an example exists.” It exists at the **presheaf** level, as above. It cannot exist for an ordinary sheaf if “pairwise compatible” means equality of restrictions on every pairwise overlap and the sets truly cover the region: the sheaf axiom is exactly the assertion that such data have a unique global glue.

## 4. Sheafification as repair

A presheaf can be sheafified, producing the nearest sheaf in the categorical sense. For the naive constant-style presheaf above, the associated sheaf is the sheaf of locally constant functions; on the disconnected space \(X\), a global section may choose different integers on the two components, so the local values 0 and 1 now glue.

This is a mathematically precise version of “repair the local representation so globally coherent information can be assembled,” and it is closely related to Steven Phillips's 2020 use of sheaving/sheafification for semantic compositionality.

## 5. What should a concept sheaf store?

Several choices are plausible, but they must not be mixed without type declarations.

- **attribute assignments:** sections are compatible feature/value assignments;
- **logical valuations:** sections are satisfying assignments of formulas local to a subcomplex;
- **CM/LM data:** sections are local truth tensors/matrices with restriction along variable deletion;
- **linguistic/semantic descriptions:** sections are structured semantic records;
- **evidence states:** sections encode observations compatible on shared attributes.

The topology/cover specifies what “local” means. The sheaf specifies which local states are globally coherent.

## 6. Sheaf gluing does not equal concept independence

Suppose two local concept descriptions agree perfectly on their overlap and glue uniquely. They may still be strongly coupled outside the overlap. Sheaf compatibility answers:

> “Can these local descriptions belong to one global description?”

It does not answer:

> “Can the global description factor into two independently variable subsystems?”

For the latter, one needs a product/factorization condition on the sheaf or on its sections. A future structured theorem could require both:

1. a cover/sheaf condition for coherent global reconstruction;
2. an external-product decomposition across the proposed independent blocks.

## 7. Cosheaves: aggregation rather than restriction

A cosheaf is covariant with respect to inclusions and satisfies a colimit-type local-to-global axiom. It is therefore a natural candidate when the intended operation is **assemble local pieces into a global aggregate** rather than **restrict global states to local observations**.

For the Mental Space program, a useful dual architecture is:

- **sheaf:** local semantic states must agree on overlaps;
- **cosheaf:** local contributions aggregate into a global object;
- **simplicial carrier:** records which local regions overlap;
- **factorization layer:** decides whether the final whole is separable.

This is standard sheaf/cosheaf technology applied in a new synthesis; it is not a novel definition of sheaf or cosheaf.

## 8. Contextuality connection

Abramsky and Brandenburger's sheaf-theoretic account of contextuality identifies contextual behavior with obstructions to global sections over a measurement cover. The analogy here is structurally useful: local concept states may be individually admissible yet lack a single global realization.

But two cautions are mandatory:

1. “no global section” is a consistency/contextuality obstruction, not automatically a psychological phenomenon;
2. cohomological obstructions can be sufficient diagnostics without being complete in all variants, so absence of a chosen obstruction does not prove global coherence unless the theorem says so.

## 9. Descent and higher compatibility

For Set-valued sheaves, ordinary pairwise agreement suffices. If later concept data are categories, groupoids, or homotopy types, equality is replaced by isomorphism/equivalence and coherence data on triple and higher overlaps become real. Only then is stack/higher-descent machinery justified.

Thus the recommended research order is:

1. prove the Set/Boolean case completely;
2. move to modules/vector spaces if needed;
3. introduce higher descent only when local semantic states genuinely have nontrivial automorphisms/homotopies.

## 10. Strong next sheaf question

For a finite structured concept \((K,\mathcal F)\), characterize when a cover by subcomplexes \(K_i\) simultaneously has:

- unique sheaf gluing of admissible local sections;
- a canonical cosheaf aggregation of local generators;
- a semantic product decomposition across a partition of the vertex/attribute set.

The key research target is not another proof of the sheaf axiom, but a theorem connecting **coherence** (sheaf) to **separability** (product/rank) under explicit hypotheses.
