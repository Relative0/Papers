# Proof and scope audit

Date: 2026-09-29. This is a self-audit plus a separately implemented
computational check, not an independent human or agent referee report.

## Objections checked

1. **Does bounded mean small n?** No: a global least and greatest element,
   with arbitrarily many incomparable middle states. This is the entire class
   of bounded posets of height at most two, not a bounded-size enumeration.
2. **Does count equality improperly prove safety?** No. The two equal-endpoint
   cases have explicit identity boundaries; the ascending case is 0 by 0.
   The descending case has more rows than columns, which suffices for failure.
3. **Could a descending-endpoint query become useful near an endpoint?** No:
   if both endpoints survive it is unsafe; with one endpoint its legality
   forces constancy. This establishes necessity for all possible histories.
4. **Could E-peeling remove something needed later?** It keeps both endpoints,
   so the local safety rule stays unchanged. Peeled branches are antichains.
   The proof explicitly constructs the residual star protocols rather than
   assuming hereditary feasibility on the original height-two poset.
5. **Could equal-endpoint peeling get stuck in the wrong core?** A middle state
   survives exactly when it agrees with the endpoints on every E-query. If a
   noncore state survives, one witnessing E-query is still informative. Thus
   the terminal core is independent of peel order.
6. **Are leaves of the residual stars oriented-separable?** Yes: a core state's
   safe signature must differ from each endpoint, and only ascending queries
   can witness those differences. This provides precisely 0<1 witnesses for
   the relevant star comparisons.
7. **Must the initially safe library separate middle pairs?** No. The explicit
   four-state example needs the initially unsafe test 1100 after 0110 detaches
   the middle antichain. The theorem deliberately uses all Q for middle pairs.
8. **Are unlisted complements or new tests introduced?** No. Trees record
   original query indices. Every node is independently matrix-checked, with
   outcome supports and the absence of repeated useful queries checked too.
9. **Does the result rescue arbitrary-legal-first greedy?** No. The inherited
   three-chain {010,011} remains a counterexample within this solved class.
10. **Does the result settle general RF-IDENT or optimal depth?** No. It gives
    decision and a successful tree on one natural unbounded-size subclass.

## Reproducible finite checks

Run `python verify_bounded_height2.py` in this directory (Python 3.10+,
standard library only). No previous gate verification module is imported.

The generic comparator enumerates relative edges and triangles on each support,
forms the F2 boundary, computes rank by row elimination, and uses that predicate
in the full support feasibility recursion. It does not call the theorem's
structural safety function or signature criterion. The constructive solver
uses the structural rule; a matrix-based traversal then validates every node.

The completed run recorded:

| Check | Coverage | Result |
|---|---|---|
| Structural rule vs relative matrix | 87,376 support/query cases, n=2..8, including constants and empty supports | All agree |
| Criterion vs exact matrix-based feasibility DP | All 16,452 effective libraries for n=2,3,4 | All agree |
| Criterion vs exact matrix-based feasibility DP | 9,000 seeded instances, 1,500 at each n=5..10 | All agree |
| Canonical tree verification | 83,143 internal nodes across 20,582 feasible exhaustive/seeded instances | All pass |
| Named boundary examples | Destructive legal choice on 3 states; essential initially unsafe query on 4 states | Pass |

There is one bounded poset up to isomorphism for each n>=2. This is not an
enumeration of all height-two posets. Libraries for n<=4 include all subsets
of the nonconstant oriented masks; constants cannot affect feasibility.
Larger cases sample library lengths 0..3n and masks uniformly, allow constants
and duplicates, and use seed 2026092907. They need not be distinct. Named
example checks are additional to the pooled node count. Finite checks support
the proof and do not establish it by extrapolation.

The first execution stopped at a generator-expression indentation error before
running any checks. That syntax was corrected; the complete run then passed.
No mathematical discrepancy was encountered. VERIFICATION.json records exact
coverage and timing, and PROTOCOL_EXAMPLES.json preserves actual query IDs.

## Narrow literature check and limitation

The proof is self-contained given the inherited boundary characterization.
A small primary-source search used these queries on 2026-09-29:

- `"decision tree" "double cone" poset`
- `"identification" "poset" "isotone" queries`
- `"decision tree" "homotopy" queries poset`

An apparent nearby source was Jakob Jonsson, [Optimal Decision Trees on
Simplicial Complexes, Electronic Journal of Combinatorics 12 (2005), R3](https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v12i1r3/pdf/).
Its introduction defines a hidden face/subset with membership queries and
connects evasive faces to homology. That is a different specified problem from
identifying a hidden vertex with a supplied oriented library whose legality
depends on refinement. This comparison does not rule out a relevant result
elsewhere in that paper or in other literature. No exhaustive priority review,
novelty confidence upgrade, or public first claim is justified here.

## Preservation and research boundary

All new work is in this sibling phase directory. The archived gate, its hash
manifest, source claim tables, and inherited proofs were not edited. There were
no commits, pushes, external writes, publication, or paid services. The general
classification remains open. A separate referee should reconstruct this short
theorem before it is promoted into a publication claim.
