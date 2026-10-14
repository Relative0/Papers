# RF-IDENT on bounded posets of height at most two

Date: 2026-09-29. Status: proved here, with a separate matrix-based finite check;
not independently refereed and no priority claim.

## Scope and statement

Here **bounded** means that the poset has a least element a and a greatest
element z. It does not mean bounded cardinality. Height counts strict
inequalities. For n >= 2 every such poset of height at most two is exactly

    P = {a} + M + {z},

where M is an antichain, every a < x < z for x in M, and a < z is included.
Indeed a comparison between two middle elements would give a chain with three
strict inequalities. For M nonempty the height is exactly two. This includes
the three-chain and all the bottom/middle/top posets used in H5 of the earlier
gate, with **arbitrary** explicitly supplied oriented Boolean query libraries.

Fix such a library Q, with m tests, and put

    Q_safe = {q in Q : q(a) <= q(z)}.

Two states are separated by a family when at least one supplied test gives
different values on them. Then:

**Theorem.** Repair-safe identification is feasible if and only if

1. Q separates every pair of distinct states in M;
2. Q_safe separates each of a and z from every other state of P.

Equivalently, a and z are singleton signature classes for Q_safe, and all
middle-state signatures for Q are distinct. Q_safe is exactly the family safe
on the full initial poset. The theorem does **not** require Q_safe to separate
all middle pairs.

Both decision and construction of a successful identifying tree take
O(n^2 + m n^2) time by direct scans, including checking that a supplied explicit
order matrix has the stated form. A successful reduced tree has n leaves and
n-1 internal nodes. Its depth need not be optimal. Empty and singleton carriers
are trivially identifiable and handled separately.

## Proof of the local safety rule

Use the inherited one-bit relative-boundary characterization over F2, whose
collapse proof is in the earlier gate's REPAIR_GRAPH_DYNAMICS.md. For a support
S containing both endpoints, write R = S intersect M. There are only the
triangles a < x < z with x in R. Consider endpoint values:

| q(a), q(z) | Relative boundary | Safety |
|---|---|---|
| 0,1 | No deleted edges or triangles | Safe |
| 0,0 | Each x with q(x)=1 gives just descent xz and triangle axz, word 010 | Safe: identity matrix |
| 1,1 | Each x with q(x)=0 gives just descent ax and triangle axz, word 101 | Safe: identity matrix |
| 1,0 | One descent az, plus exactly one of ax,xz per x; one column per x | Unsafe: |R|+1 rows, |R| columns |

Thus q is safe on every support containing a,z if and only if q(a)<=q(z).
This also covers R empty. No count-equality shortcut is used to infer general
matrix invertibility: the safe cases exhibit the actual matrices.

If only a remains, the support is a lower star a<R, and safety means no
descent: either q(a)=0 or q is constant 1. If only z remains, it is an upper
star R<z: either q(z)=1 or q is constant 0. With neither endpoint the support
is an antichain and every query is safe. These exhaust all induced supports.

**Consequence.** A query outside Q_safe can be useful and legal only on a
support containing neither endpoint. With both endpoints it is unsafe; with
just a, legality forces it constant 1; with just z, legality forces it constant
0. Its later usefulness is confined to antichain branches.

## Necessity

Indistinguishable middle states cannot be identified by any Q-tree, proving
condition 1.

For an endpoint e and any other state v, follow their shared history until
the first query separating them. Its support contains e and v and the query
is useful. By the preceding consequence it belongs to Q_safe. Thus every
endpoint/state pair must be separated by Q_safe, proving condition 2. This
argument permits arbitrary adaptive histories and does not assume that
initial safety is hereditary.

## Sufficiency and a canonical construction

Partition Q_safe as

    E = {q : q(a)=q(z)},
    A = {q : q(a)=0, q(z)=1}.

Condition 2 for a,z implies A is nonempty. Maintain the unique branch
containing both endpoints. While some E-query is nonconstant on this branch,
ask it. It is safe by the local rule. Its opposite-to-endpoint outcome contains
only middle states, hence is an antichain; identify that branch by arbitrary
supplied separating queries from Q. Condition 1 guarantees this is possible.
The endpoint outcome retains a,z and strictly fewer middle states. Previously
asked queries are constant there, so they require no special exclusion rule.

After these peels the endpoint branch is {a,z} union C, where

    C = {x in M : q(x)=q(a)=q(z) for every q in E}.

This set is independent of the order of the informative peels. Ask any s in A.
Its children are the lower star {a} union C_0 and the upper star C_1 union {z},
where C_b = {x in C : s(x)=b}.

For each x in C_0, condition 2 supplies a Q_safe test r separating a,x.
It cannot belong to E by the definition of C. Thus r belongs to A and
r(a)=0,r(x)=1. Such tests are safe everywhere on the lower star and, along
the a outcome, eventually remove every leaf. Every detached branch is an
antichain whose states remain separated by Q. Hence this star is identifiable.

For each x in C_1, the same argument using separation of x,z gives an A-test
r with r(x)=0,r(z)=1. These safely remove every leaf along the z outcome of
the upper star, again leaving identifiable antichain branches.

This constructs an identifying tree using only actual supplied queries.
Every useful query strictly shrinks both outcome supports; therefore the
reduced tree has exactly n leaves and n-1 internal nodes. Directly scanning
m queries over at most n states at each node gives O(m n^2) construction time.
Checking the two conditions by pairwise query scans has the same bound.

## Equivalent core criterion

The same theorem says that Q must separate all states, A must be nonempty,
and for every x in C the string (q(x))_(q in A) must contain both 0 and 1.
Indeed E cannot distinguish a core state from either endpoint. A value 1 is
needed to distinguish it from a and a value 0 to distinguish it from z.
States outside C already have an E-query distinguishing them from both.

This also proves that after all E-peels, **any** ascending endpoint query is a
successful first split of the residual problem. It does not say that any
initially legal query is safe to choose first.

## Essential boundary examples

**Legal greedy choice still fails.** On a<x<z, Q={010,011}, where words list
values in that state order, both tests are initially safe. The canonical
construction asks 010, isolates x, then uses 011 on {a,z}. Asking 011 first
leaves {x,z}, where 010 is the unsafe descent 10 and 011 is constant. The
problem is feasible but this legal first choice destroys feasibility.

**Initially unsafe tests can be essential.** On a<x,y<z, use state order
(a,x,y,z) and Q={0110,0001,1100}. The first two tests are initially safe;
1100 is not. Ask 0110 to produce {a,z} and {x,y}. Use 0001 on the former and
1100 on the latter. Without 1100, x,y have identical signatures. Thus the
criterion cannot be replaced by pairwise separation under Q_safe alone.

**Both global endpoints matter.** The proof uses that every support with
both endpoints has the same simple boundary pattern and that losing either
endpoint leaves a star. It makes no assertion for arbitrary height-two posets,
for disjoint unions of these bounded posets, or for posets having only a least
or only a greatest element. General height-two RF-IDENT remains in NP with its
classification unresolved by this result. No RF-DEPTH hardness argument is used.

## Relationship to the inherited gate

This is a new subclass feasibility theorem, not a change to the completed
gate's general classification. It extends that gate's specified-library
bottom/middle/top examples to arbitrary oriented libraries on that poset class.
Its mechanism explicitly accommodates both deactivation and essential later
activation. It relies only on the verified branch-cancellation and boundary
criteria. U2's internal-fiber caveat, U4's exact-sequence terminology, U6's
fine-measurability hypothesis, A1, and V5-06/07/09 corrections are untouched.
