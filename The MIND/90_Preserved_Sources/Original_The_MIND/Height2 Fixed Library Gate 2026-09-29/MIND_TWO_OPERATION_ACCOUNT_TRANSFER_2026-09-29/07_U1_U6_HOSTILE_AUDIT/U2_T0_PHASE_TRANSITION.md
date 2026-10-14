# U2 — The T0 phase transition: hostile audit and repair

## Verdict

**VALID WITH REPAIR.** The source correctly identifies world-level refinement as relation deletion, but its quotient-level summary is too strong if read as saying that quotient refinement only splits vertices and deletes old strict comparabilities. Splitting one coarse quotient point can itself expose **new strict order inside the split fiber**.

## Minimal counterexample

Let `S={a,b}` and let the coarse observation family be empty. The coarse world preorder is indiscrete: both `a<=b` and `b<=a`, so the Kolmogorov quotient has one point.

Add one Boolean observation with

\[
\theta(a)=0,\qquad \theta(b)=1.
\]

The refined world preorder deletes `b<=a` but retains `a<=b`. The fine quotient is therefore a two-point chain.

Thus the statement

> no new strict quotient comparabilities can appear under refinement

is false. The new strict comparability appears **inside the descendants of one old coarse quotient point**.

## Repaired theorem

Let `Psi superset Phi`. Write

\[
Q=S/{\sim_\Psi},\qquad P=S/{\sim_\Phi}.
\]

Then:

1. every fine equivalence class lies inside a unique coarse equivalence class;
2. hence there is a canonical surjective map
   \[
   r:Q\to P;
   \]
3. `r` is monotone;
4. if `q1<=q2` in `Q`, then either `r(q1)=r(q2)` or `r(q1)<=r(q2)` in `P`;
5. therefore refinement cannot create comparability between descendants of two **distinct coarse-incomparable** points;
6. a split coarse point may acquire a nontrivial internal fiber order;
7. between distinct coarse points, existing coarse comparabilities may disappear when new coordinates descend.

The clean quotient picture is therefore:

\[
\boxed{\text{fiber expansion within coarse points}\ +\ \text{cross-fiber order thinning}.}
\]

Relative `T0` means every coarse fiber is a singleton. At that stage the expansion mechanism disappears, leaving only same-vertex order thinning.

## Computational attack

The four-world exhaustive audit found 5,680 one-bit observation refinements over all 355 observation-generated preorders:

- pre-T0 redundant: 660;
- pre-T0 splitting only: 578;
- pre-T0 thinning only: 338;
- pre-T0 **both splitting and thinning**: 600;
- T0 redundant: 1,678;
- T0 thinning only: 1,826.

There were zero violations of the repaired carrier-level monotonicity theorem.
