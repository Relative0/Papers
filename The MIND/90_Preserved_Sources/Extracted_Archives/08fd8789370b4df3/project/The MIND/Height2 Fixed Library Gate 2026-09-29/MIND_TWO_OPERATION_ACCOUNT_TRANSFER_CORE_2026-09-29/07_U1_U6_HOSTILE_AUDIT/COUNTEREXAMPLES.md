# Counterexamples and repaired overstatements

## C1 — quotient refinement can expose a new strict order inside a split coarse point

**False stronger statement:** “No new strict quotient comparabilities ever appear under refinement.”

Carrier `S={a,b}`; no coarse observations; add `theta(a)=0, theta(b)=1`.

- coarse quotient: one point;
- fine quotient: two-point chain `0<1`.

**Repair:** no fine comparability can connect descendants of two distinct coarse-incomparable points. New strict relations may appear **inside the fiber of one split coarse point**.

## C2 — cartesianity does not imply coarse measurability without fine measurability

Coarse cell `{a,b,c}`; fine cells `{a,b}` and `{c}`; event `E={a,c}`.

`E` cuts a fine cell. Thus it is not fine-measurable and not coarse-measurable, even though the coarser label-profile condition can be cartesian.

**Repair:** U6 must assume `E` is a union of fine signature classes.

## C3 — U4 is not a direct-sum decomposition theorem

The octahedral axiom yields a distinguished triangle and long exact sequence. Without vanishing connecting morphisms and further splitting data, one cannot conclude

\[
D^{\rm total}\cong D^{\rm thin}\oplus D^{\rm exp}.
\]

**Repair:** call U4 an “octahedral defect sequence” or “cone factorization sequence,” not an unconditional direct decomposition.

## C4 — homotopy-neutral query restrictions alone do not make adaptive identification hard

If arbitrary Boolean queries are available on a finite T0 poset, choose a linear extension. Any suffix of a linear extension is an upset and therefore defines an isotone/topologically redundant query. A suffix can be chosen to split the current support as evenly as possible. Repeating yields depth `ceil(log2 n)`.

**Repair of research target:** to obtain nontrivial adaptive complexity, impose a fixed query library, syntactic/cost restriction, or require nonredundant safe queries.
