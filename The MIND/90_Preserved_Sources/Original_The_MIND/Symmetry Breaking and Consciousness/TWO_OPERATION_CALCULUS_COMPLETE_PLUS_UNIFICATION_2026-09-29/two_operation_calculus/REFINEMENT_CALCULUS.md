# Refinement Calculus

## 1. Primitive refinement

For a new Boolean observation `psi`, define

\[
R_\psi(S,\Phi)=(S,\Phi\cup\{\psi\}).
\]

At the two-sided partition level,

\[
\Pi_{\Phi\cup\{\psi\}}
=
\Pi_\Phi\vee\Pi_\psi,
\]

where the join means common refinement (all nonempty block intersections).

A strict discrimination refinement occurs exactly when `psi` splits an old signature cell.

## 2. Algebra

At the observation-family/partition level:

\[
R_\psi^2=R_\psi,
\qquad
R_\psi R_\theta=R_\theta R_\psi.
\]

Thus fixed Boolean refinements form an idempotent commutative semilattice action. If observation families are quotiented by observational equivalence, refinement is a closure/join operation in the partition or generated-algebra lattice.

The exhaustive Omega_2 computation checked all one-event transitions from all 15 partitions:

- 240 transitions total;
- 146 strict partition refinements;
- 94 partition-redundant additions.

## 3. Redundancy has more than one meaning

A test may be:

1. **partition redundant**: it does not split any signature class;
2. **Boolean-algebra redundant**: its event already belongs to `A_Phi`;
3. **ProLT topologically redundant**: its positive truth region is already open in `tau_Phi`;
4. **metric/cost redundant**: adding it changes no declared distance/cost.

These notions need not coincide. The current ProLT manuscript already warns that a positive observation can be topologically redundant while a repeated/weighted coordinate still changes a signature distance.

## 4. Pre-T0 versus post-T0 refinement

This is the most important structural distinction inherited from ProLT.

### Pre-T0

A new observation may split an existing observational equivalence class. The T0 quotient therefore gains points.

### Post-T0

No further world splitting is possible. A new positive observation may still delete one-way specialization comparisons and hence delete simplices from the order complex.

The exhaustive four-point positive-topology study classified all 5,680 `(topology,new event)` transitions:

- 2,338 redundant;
- 1,178 split an indiscernibility class;
- 2,164 preserve the carrier but thin the specialization order.

Among the 3,504 transitions whose source is already T0:

- 1,678 are redundant;
- 1,826 are genuine same-carrier order thinnings;
- 0 split vertices, as required.

This finite enumeration independently confirms the conceptual boundary used in the ProLT order-thinning papers.

## 5. Simultaneous refinement

For a block `Theta=(theta_1,...,theta_k)`, the existing ProLT v0.5 result gives, post-T0,

\[
p\le_{\Phi\cup\Theta}q
\iff
p\le_\Phi q
\text{ and }
\alpha_\Theta(p)\le\alpha_\Theta(q)
\]

coordinatewise. Hence block refinement is the intersection of its one-coordinate refinements.

This is stronger than plain partition splitting: simultaneous positive observations can have homotopical interaction effects even when the carrier is already fully distinguished in the T0 sense.

## 6. Minimal refinement

If *arbitrary* Boolean tests are permitted on an `N`-world support, full two-sided separation needs exactly

\[
\lceil\log_2 N\rceil
\]

bits, by binary coding and the counting lower bound.

Therefore unrestricted minimum separation is not a difficult new optimization problem. The interesting problem begins only when the test pool, formula language, geometry, costs, or ProLT-topology constraints are restricted. Then the problem meets the classical Test Cover/separating-family literature.

For the complete 16-test pool on four worlds, exhaustive enumeration found:

- minimum separator size 2;
- 12 minimum two-test families;
- additionally 128 inclusion-minimal three-test separators which are irredundant but not minimum.
