# Theorem / Counterexample Ledger

| ID | Statement | Status | Proof / counterexample / note |
|---|---|---|---|
| T1 | The common-prefix distance `d(x,y)=lambda^{L(x,y)}` is ultrametric. | Proved | Common-prefix lengths satisfy `L(x,z)>=min(L(x,y),L(y,z))`. |
| T2 | Every p-adic metric space is Hausdorff. | Standard theorem | Every metric space is Hausdorff; direct p-adic proof separates distinct points by sufficiently small balls. |
| T3 | Ultrametricity implies the indiscrete topology. | False | Counterexample: `Z_p` has nontrivial clopen balls `a+p^k Z_p`; indeed it is Hausdorff and totally disconnected. |
| T4 | If two ultrametric balls intersect, they are equal. | False in general | Correct: intersecting balls are nested; if they have equal radius, they are equal. |
| T5 | Every point of an ultrametric ball can serve as its center (same radius). | True | Strong triangle inequality gives equality of same-radius balls. |
| T6 | Open p-adic balls are clopen. | True | Their complements are unions of balls; equivalent standard proofs apply. |
| T7 | Closed ultrametric balls are open (positive-radius convention). | True | For `x` in `Bbar(a,r)`, the open ball `B(x,r)` lies in `Bbar(a,r)`. |
| T8 | `x~_k y` iff first `k` coordinates agree is an equivalence relation. | Proved | Equality of finite prefixes is reflexive, symmetric, transitive. |
| T9 | The `~_k` equivalence classes are exactly depth-`k` prefix balls. | Proved | Immediate from definitions. |
| T10 | For full `m`-ary prefix space, `|X/~_k|=m^k`. | Proved | One class for each length-`k` word. |
| T11 | `~_{k+1}` refines `~_k`. | Proved | Agreement on `k+1` coordinates implies agreement on first `k`. |
| T12 | The inverse limit of the finite prefix quotients recovers `A^N`. | Standard | A coherent family of finite prefixes uniquely determines an infinite sequence. |
| T13 | A level-`k` observable factors through `pi_k` iff it is constant on each `~_k` class. | Proved | Standard quotient universal property. |
| T14 | In `Z_p`, common-prefix length equals `v_p(x-y)` for distinct digit expansions. | Standard/proved computationally for finite model | The first differing p-adic digit occurs exactly at the valuation index. |
| T15 | In the thesis Example 2.4, conflicting cylinders intersect in the common attribute set. | False | `{a0=1,...} ∩ {a0=0,...}=empty`. Common attributes require projection/forgetting. |
| T16 | Symmetry of a relation implies equivalence. | False | Symmetric relations need not be reflexive or transitive. Example on `{1,2}`: `R={(1,2),(2,1)}`. |
| T17 | A regular tree's hierarchy can be represented by an ultrametric on its boundary. | Standard | Distance determined by LCA/common-prefix depth. |
| T18 | A finite ultrametric can be represented by a labeled rooted tree/dendrogram. | Standard | Classical representing-tree construction; modern references give isometry iff labeled trees match. |
| T19 | The individual ball family is a Boolean algebra. | Usually false | Complements of balls are generally unions of balls. Fixed-depth cell unions do form a finite Boolean algebra. |
| T20 | Ulrametricity alone causes cognitive indistinguishability. | False as mathematics; modeling choice needed | Distinct points remain topologically distinguishable. Add observation quotient/invariance. |
| T21 | If `G_k` acts transitively inside each fiber and `f` is `G_k`-invariant, then `f` is constant on each fiber. | Proved | For `x,y` in one fiber choose `g` with `gx=y`; then `f(y)=f(gx)=f(x)`. |
| T22 | Uniform depth-`k` prefix ball has measure `m^{-k}` under product/Haar measure. | Standard | Product of `k` branch probabilities `1/m`. |
| T23 | Uniform refinement by one `m`-ary digit gives `log_2 m` bits. | Standard | Self-information `-log_2(1/m)`. |
| T24 | `Q_p` is required to model a hierarchy. | False | Rooted trees/prefix spaces/arbitrary ultrametrics suffice. |
| T25 | Prime-base p-adics provide additional algebraic structure beyond the tree. | True | `Z_p` is a compact topological ring/group; `Q_p` is a local field. |
