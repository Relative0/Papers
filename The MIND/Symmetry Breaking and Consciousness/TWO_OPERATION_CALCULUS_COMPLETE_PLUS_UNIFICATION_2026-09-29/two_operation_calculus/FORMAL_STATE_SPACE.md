# Formal State Space

## 1. Recommendation

For a fixed finite carrier `Omega`, the cleanest primitive state is

\[
\boxed{(S,\Phi)}
\]

with:

- `S subseteq Omega`: the currently viable worlds;
- `Phi=(phi_i)`: the currently available observation family.

The partition, Boolean event algebra, positive topology, and specialization preorder should be **derived** from `Phi`, not substituted for it prematurely.

This matters because two mathematically different observational structures coexist.

## 2. Two-sided indiscernibility layer

For Boolean observations define

\[
o_\Phi(x)=(\phi_i(x))_{i\in I}.
\]

Then

\[
x\sim_\Phi y \iff o_\Phi(x)=o_\Phi(y)
\]

is an equivalence relation with partition

\[
\Pi_\Phi=\Omega/{\sim_\Phi}.
\]

Equivalently, `Phi` generates a finite Boolean algebra

\[
\mathcal A_\Phi=\{\text{unions of blocks of }\Pi_\Phi\}\subseteq 2^\Omega.
\]

For finite carriers, the following carry the same two-sided discrimination data up to presentation:

1. the signature map and its fibres;
2. the equivalence relation `~_Phi`;
3. the partition `Pi_Phi`;
4. the Boolean subalgebra `A_Phi` whose atoms are those blocks.

This is standard mathematics and is especially close to Pawlak rough-set information systems, where attributes induce exactly such an indiscernibility relation.

## 3. Positive ProLT layer is strictly richer than the partition

The current ProLT formalism uses positive truth regions to generate a finite topology `tau_Phi`. Its specialization preorder is

\[
x\preceq_\Phi y
\iff
o_\Phi(x)\subseteq o_\Phi(y)
\]

when signatures are viewed by support inclusion.

The symmetric part of this preorder recovers `~_Phi`, but the preorder contains additional directional information. Consequently, after the space has become T0, the partition is already discrete while **further observations can still refine the ProLT topology by deleting one-way specialization comparisons**.

The exhaustive four-world calculation makes the distinction concrete:

- 15 two-sided partitions of a four-point carrier;
- 355 positive finite topologies;
- 219 of those topologies are T0.

Therefore replacing `Phi` by `Pi_Phi` is appropriate for a classical two-sided discrimination calculus, but it throws away precisely the post-T0 order-thinning structure that the later ProLT work studies.

## 4. Recommended typed state hierarchy

Use three levels explicitly.

### Level A: primitive observational state

\[
\mathfrak x=(\Omega,S,\Phi).
\]

### Level B: classical discrimination shadow

\[
\mathsf D(\mathfrak x)=(S,\Pi_\Phi,\mathcal A_\Phi).
\]

### Level C: ProLT positive-observation shadow

\[
\mathsf P(\mathfrak x)=(S,\tau_\Phi,\preceq_\Phi).
\]

This avoids treating partition refinement and ProLT order refinement as the same thing.

## 5. Order on states

At the partition level, a natural "more differentiated / more informed" order is

\[
(S,\Pi)\sqsubseteq(T,\Lambda)
\quad\Longleftrightarrow\quad
T\subseteq S
\text{ and }
\Lambda\text{ refines }\Pi.
\]

Depending on convention, this is the product lattice

\[
\mathcal P(\Omega)^{op}\times\operatorname{Part}(\Omega).
\]

This is mathematically clean but not novel by itself. A ProLT-enriched state replaces the partition coordinate by an observation topology/preorder and thereby retains the directional structure.

## 6. Ontic versus epistemic reading

None of the finite theorems requires an ontic interpretation. `S` may mean either:

- states genuinely possible in the model; or
- states not yet ruled out by an observer.

Similarly, `Phi` may represent physically available tests, experimental interventions, linguistic predicates, or merely a chosen representational interface. Any cognitive interpretation must therefore be added explicitly rather than inferred from the mathematics.
