# Formal adaptive model

Date: 2026-09-29. Scope: finite deterministic, noiseless, fixed-library identification.

Let P=P0 be a finite poset on S0, with height the maximum number of strict inequalities in a chain. Thus height at most two permits three-element chains. The initial observation signature is injective (post-T0). Fix an explicitly supplied finite set Q of functions q:S0 -> {0,1}.

The hidden state is unknown. The background observation family specifies the topology and the known truth tables, but its values at the hidden state are not provided as a free query oracle. Otherwise the initial injective signature would already identify the state and the problem would be trivial. This is the same structural-versus-acquired-data convention needed by A1.

A history h records queries and their answers, with support

  S_h = {x in S0 : q(x)=b for every recorded (q,b)}.

Every query is assessed on the current support BEFORE its outcome is conditioned on. For a query r, its one-bit refined order on a support S is

  x <=_r y iff x <=_P y and r(x)<=r(y).

It is legal precisely when the inclusion of order complexes Delta(P|S refined by r) -> Delta(P|S) is a homotopy equivalence. At height at most two, v0.4 identifies this with the repair-forest / invertible relative-boundary test. This is a claim about the order-complex inclusion, not an assertion that the finite posets are isomorphic.

Only nonconstant legal queries are useful. Previously queried tests are constant on a descendant support, so neither a used-query mask nor the full history is needed for the unit-cost recurrence. Duplicate truth tables may be removed. Complements are distinct oriented observations and are available only if supplied in Q. Although q and its complement give the same information partition, their refinement safety can differ.

The model assumes no global consumption shared across counterfactual branches, no query-dependent state change other than refinement and conditioning, and no additional history-dependent cost or syntax restriction. Under these assumptions the current support alone determines the subproblem. More elaborate restrictions would require additional state.

Every branch remains post-T0 and of height at most two. A restriction of an injective signature is injective; adding coordinates preserves injectivity. Branch cancellation gives the stronger identity P_h ~= P0|S_h.

This notion of query activation concerns topological admissibility. It is NOT the fine-measurability obstruction in U6: after T0 every subset is already measurable in the Boolean algebra of signature cells.

See BRANCH_CANCELLATION.md, REPAIR_GRAPH_DYNAMICS.md and FIXED_LIBRARY_IDENTIFICATION.md for the proofs and algorithms.
