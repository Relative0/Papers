# Reproducible finite audit

This directory contains original implementations and generated data for the
height-at-most-two, fixed oriented-query-library gate. Source manuscripts were
read for definitions; their verification scripts were not imported or reused.

## Conventions

- States are labelled `0,...,n-1`. Only **naturally labelled** posets are
  enumerated: every strict relation points from a smaller to a larger integer.
  This includes a representative of every isomorphism class, often multiple
  times. Counts are neither unlabelled-poset counts nor all-labelled counts.
- Height counts strict comparisons. A three-element chain has height two.
- The integer query mask `q` has bit `i` equal to the value at state `i`.
  Thus mask `1` on three states is the word `100` in state order, although the
  usual printed binary numeral is `001`. **Orientations matter.**
- For library mask `L`, bit `q-1` means that the nonconstant query with integer
  mask `q` is supplied. Constants are omitted only from library enumeration;
  they cannot change identification depth. Both constants are present in the
  all-query safety checks. Complements are never identified or synthesized.
- Relation-mask bits enumerate pairs `(0,1),(0,2),...,(n-2,n-1)` in lexicographic
  order. The CSV also lists all strict pairs, including transitive pairs.
- `99` denotes infinity in the bounded computations, never a depth of 99.
- Forest safety includes an isolated formal root. The zero-by-zero relative
  boundary matrix is invertible. Every coarse connected component has one root.

## Independent implementations

`repair_graph.py` constructs descent-edge vertices and one formal root per
coarse component, adds the deleted-triangle edges, and checks rooted forests
using disjoint sets. Parallel edges are retained and detected as cycles.

`boundary_matrix.py` constructs deleted relative edges and triangles directly
from the order relation and labels, constructs relative boundary columns, and
performs F2 elimination. It does not import or call the graph implementation.

`run_exhaustive.py` compares these routines on every enumerated poset/query,
then enumerates support restrictions and computes exact library depths. Its
memoized recursion projects the supplied library to the surviving support;
projection preserves the actual orientation and does not add tests. A separate,
uncached, original-query decision-tree feasibility search uses matrix legality
and checks all libraries through n=3 plus a seeded sample at n=4. There were
1,730 independently checked library instances and no disagreement.

`verify_boundary_restriction.py` is a third matrix implementation, importing
neither previous implementation nor the main script. It retains original cell
labels and computes rank by row elimination. Through n=5 it enumerated every
poset, query, and nonempty support: 337,138 parent/query/support cases, including
187,015 cases with safe parent. All exact submatrix, zero removed-row block,
kernel monotonicity, safe-parent full-column-rank, equal-cell-count safety, and
cokernel-dimension assertions passed. Full supports and constant queries are
included; these counts differ intentionally from informative transition counts.

`finalize_artifacts.py` assigns every reported protocol node an actual original
query mask from its supplied library, checks outcome supports, forbids repeated
original tests on a path, and independently checks every repair-safe protocol
node using the matrix implementation. It verified 94 nodes. Leaf `states` are
original state labels; `children[0]` and `children[1]` are query outcomes.

## Reproduce (Python 3.10+, standard library only)

From this directory:

```powershell
python run_exhaustive.py
python verify_families.py
python verify_parity_bipartite.py
python verify_boundary_restriction.py
python finalize_artifacts.py
```

The main run completed in about 67 seconds on this host; timings are not
portability claims. Random seeds are recorded in the scripts and SUMMARY.json.
Run logs include actual stages/counts. Reproduction overwrites generated data
in this directory. `SHA256SUMS.txt` hashes the final artifacts (excluding itself).
Timing fields/logs can change hashes even when mathematical results agree.

## Coverage and results

| n | posets, height <= 2 | all Boolean queries | exact-height-two posets | nonredundant safe queries |
|---:|---:|---:|---:|---:|
| 1 | 1 | 2 | 0 | 0 |
| 2 | 2 | 8 | 0 | 0 |
| 3 | 7 | 56 | 1 | 2 |
| 4 | 39 | 624 | 13 | 50 |
| 5 | 330 | 10,560 | 172 | 1,232 |
| 6 | 4,117 | 263,488 | 2,787 | 36,783 |

Total: 4,496 posets, 274,738 query cases, **zero graph/matrix disagreements**.
The exact-height-two slice reproduces the v0.4 counts: 184,088 query cases and
38,067 nonredundant safe refinements. This is a finite check, not a proof.

Every effective oriented library was enumerated for every poset through n=4:
639,433 instances. Beyond that, 20 seeded random libraries per n=5 poset gave
6,600 instances, and 20 per each of 200 sampled n=6 posets gave 4,000 instances.
Random instances need not be distinct and are not exhaustive coverage.

At n=4 there are 48,212 finite strict-gap instances and 62,314 instances with
finite ordinary depth but infinite repair-safe depth. No strict finite gap is
possible for n<=3; enumeration agrees. The smallest informative activation and
deactivation both occur at n=3, including legal one-step conditioning witnesses.

The minimum-cardinality strict-gap witness found at n=4 is:

- relation `0<1`, states 2 and 3 isolated;
- Q = integer masks `{1,2,5}`;
- ordinary depth 2, repair-safe depth 3.

The minimum-cardinality complement-closed strict-gap witness found at n=4 is:

- relations `0<3` and `1<2`;
- Q = integer masks `{4,5,7,8,10,11}` (three complement pairs);
- ordinary depth 2, repair-safe depth 3.

`verify_families.py` separately retains original query masks and uses a
support-mask DP. It verifies the height-one star and connected exact-height-two
`a<x_i<z` family through n=12: ordinary depth `ceil(log2 n)`, repair-safe depth
`n-1`. It also verifies the activation/deactivation witnesses and both small
complement-closed examples. Predicates agree on every visited checked query.

For the complement-closed parity complete-bipartite family, independently
computed depths at n=4,8,16 are respectively 3,6,11, versus ordinary depths
2,3,4. `verify_parity_bipartite.py` uses the exact height-one isotonicity rule,
checks it against both other implementations on 1,000 seeded support/query
samples at each size, and evaluates the full support recurrence. Its upper
bound `|S|-1` is justified by supplied singleton tests in both orientations.
The primary research audit separately proves the exact formula
`n/2 + log2(n) - 1` by the recurrence `D_k = 2^(k-2) + 1 + D_(k-1)`,
`D_1=1`. These computations check its n=4,8,16 instances; the proof is in the
parent directory's theorem documents, not in the computational enumeration.

## Artifact interpretation

- `HEIGHT2_POSETS.csv`: one row per poset; order masks and strict relations.
- `QUERY_REPAIR_SAFETY.csv`: one row per poset/query, both safety decisions,
  deleted-cell counts, F2 rank, redundancy flag.
- `SAFETY_TRANSITIONS.csv`: one row per nonconstant parent query. `all_support`
  counts proper support restrictions on which the query remains informative.
  `legal_conditioning` counts legal original conditioning queries and outcomes
  on which the unused query remains informative. S/U mean safe/unsafe. Distinct
  conditioning queries/outcomes can give the same support and are counted
  separately. All four transitions are represented. No empty/singleton or
  constant-child query is counted as an informative activation.
- `FIXED_LIBRARY_RESULTS.csv`: all 650,033 exhaustive/random instances.
  `activation_pairs` and `deactivation_pairs` count ordered library-query pairs
  exhibiting the event on at least one outcome at the root, not full-protocol
  event counts. They are computed for exhaustive n<=4; random rows explicitly
  say `not_counted`. `legal_root_queries` counts supplied nonconstant safe tests.
- `ADAPTIVE_DEPTHS.csv`: aggregate depth distribution, preserving sample type.
- `REPAIR_SAFETY_GAPS.csv`: all sampled/exhaustive strict finite gaps and
  ordinary-finite/repair-infinite instances.
- `OPTIMAL_PROTOCOLS.json`: selected minimum-cardinality examples through n=4
  and selected random examples beyond n=4, with actual-library provenance.
  This is not a list of every optimal tree for every enumerated library.
- `MINIMAL_EXAMPLES.json`: first minimum-state-count informative transition
  witnesses, both arbitrary restrictions and legal one-step conditioning.
- `COMPLEMENT_CLOSED_DEPTHS.csv`, `FINAL_CHECKS.json`: complement-closure audit
  of the enumerated libraries and protocol provenance checks.
- `STRUCTURED_FAMILY_DEPTHS.csv`, `STRUCTURED_FAMILY_CERTIFICATES.json`: explicit
  families, supplied masks, exact computed depths; protocol trees for n<=6.
- `PARITY_BIPARTITE_DEPTHS.csv`: separate larger-family support-DP results.
- `BOUNDARY_RESTRICTION_CHECKS.csv`, `BOUNDARY_RESTRICTION_SUMMARY.json`: explicit
  matrix restriction theorem checks and their exact scope.
- `SUMMARY.json`, logs, scripts, `SHA256SUMS.txt`: coverage and reproducibility.

## Limitations

These computations establish finite instances and validate implementations.
They do not establish general theorems or literature priority. No exhaustive
library claim is made above n=4, no exhaustive poset claim above n=6, and no
claim that all labelled versions were counted. The random search is bounded
reconnaissance. Published novelty needs the separate theorem/priority audit.
