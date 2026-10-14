# Actual compressed-SDD pipeline

The implementation is `code/hybrid_core.py::compile_extract`. It uses PySDD's
C-backed SDD manager, with an explicit complete vtree read from a temporary
`.vtree` file. Input labels and CNF variables are one based. The word
"industrial" in the requested filename denotes use of an actual maintained
compiler backend; it does not establish industrial-scale performance.

Each CNF clause is built by SDD disjunction, and the formula by conjunction.
Automatic garbage collection and minimization are disabled during ordinary
compilation to preserve the specified input vtree. The finished root is
referenced before optional `manager.minimize()`. B2 uses this actual library
operation; the returned tree is read back from the manager after minimization.
Other searches compile their candidate trees explicitly, charging every
compilation to the method. Recompilation is consequently a material limitation
against the library's in-place dynamic search.

`sdd_size = root.size()` counts reachable decision elements and
`sdd_count = root.count()` counts reachable decision nodes. Constants and
literals have zero decision size; neither measure is a truth-table emulation.
These root-reachable quantities differ from manager-wide live/dead allocations.
Compilation time includes vtree serialization/read, manager initialization,
and CNF Apply operations. Extraction and optional minimization are separate
times. Overall benchmark wall time must additionally include search, defects,
residual SAT, final assembly, and cleanup.

Extraction follows the reproduced compressed-cut criterion. At a decision
node normalized at its vtree split, there is an AND split exactly when one
nonfalse sub remains. Its prime and sub become the two factors. Two or more
nonfalse subs leave the entire scope unresolved. True scopes and literal
scopes factor into singleton coordinates, including free variables.

PySDD uses trimmed nodes. A node can be normalized strictly below the current
declared vtree scope. The extractor locates that descendant subtree and treats
the other branch as true; it does not inspect the descendant's decomposition
as though it were the ancestor's decomposition. This normalization is required
for sound extraction in the presence of omitted/free variables. Extraction is
tested both before and after library minimization.

The result is the finest partition whose blocks are vtree clusters, not in
general the semantic prime partition. Every exposed nonsingleton block remains
a residual block until exact SAT refinement finishes. Therefore "direct block
count" is a legitimate objective, whereas "direct prime count" needs an
independent evaluation comparison. Only singleton exposed blocks are counted
as directly resolved in ground-truth-free operational statistics. If an
evaluation table counts nonsingleton exposed prime factors, that statistic
must be explicitly marked evaluation-only.

False formulas are reported as `satisfiable=false` and `direct_partition=null`.
The canonical nonfalse factorization contract does not assign them a claimed
prime partition. The benchmark runner must retain and report such cases under
its fixed eligibility rule rather than silently treating false as true.

`code/validate_hybrid.py` compares actual extracted partitions against a
separate exhaustive relation-projection test for all functions through three
variables, all three labelled unordered three-leaf vtrees, random cases up to
eight variables, free/literal/trimmed-node cases, and dynamically minimized
trees. Machine-readable counts are in `data/hybrid_validation.json`; the
principal validation stdout is archived in `logs/hybrid_validation.log`.

The actual backend run passed: 903 compilations, including 113 dynamic
minimizations; 881 nonfalse direct partitions agreed exactly with independent
model projections, and all 22 false inputs were reported explicitly. No
discrepancy occurred. The complete combined validation took 9.06 seconds on
the recorded environment; this is correctness-validation time, not a method
performance comparison.

No unrestricted structured-d-DNNF factor-extraction claim is made.

The API contracts used here were checked against the maintained
[PySDD SddNode documentation](https://pysdd.readthedocs.io/en/latest/classes/SddNode.html)
and [Vtree documentation](https://pysdd.readthedocs.io/en/latest/classes/Vtree.html)
on 29 September 2026. Installed-version execution is the operational authority;
the documentation's displayed release label is older than the installed wheel.
