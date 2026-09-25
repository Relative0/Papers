# Research Log

## 2026-09-17 — Pure-Boolean modal investigation pass

### Access / provenance

- Direct access to `C:\Users\brian\Documents\CM Quantum` was **not available** in this environment.
- The original Droncheff CM manuscript was located in the user's ChatGPT File Library and inspected, especially:
  - the CM basis/operator table;
  - XOR linearity and decomposition;
  - rotation/transpose relations;
  - quotient `A \ B = A AND NOT B`;
  - the measurement and LM sections.
- The prior phase research documents were located in the File Library, including the intrinsic Boolean phase paper and `CURRENT_STATE.md`.
- The public GitHub repository `Relative0/Correspondence_Matrices` was inspected through the GitHub connector. Its `docs/research/README.md` explicitly preserves negative results, exact artifact/correctness boundaries, and non-promotion after failed gates; that discipline is followed here.

### Original-paper measurement boundary recorded

The original manuscript says CM/LM action may be viewed as logical measurement and that LMs measure truth/relationships. It also explicitly states that probability densities are not incorporated. This supports a probability-free investigation but does **not** by itself define the ring-valued support rule used here.

Action: the present project defines a separate modal measurement contract in `DEFINITIONS_AND_NOTATION.md` and does not attribute that extension to the manuscript.

### Algebra implementation

Implemented `src/cm_ring.py` with:

- compact four-Boolean-bit encoding of the 16 CMs;
- XOR addition;
- cyclic `star` multiplication;
- Boolean complement;
- original support quotient;
- transpose/conjugation;
- unit/inverse/valuation utilities;
- ring-valued matrix, tensor, dagger, determinant, inverse, and effect contraction.

No signed, real, or complex arithmetic is used for state evolution.

### Baseline re-verification

Rechecked:

- `C^2=I`;
- `H_star^2=I`;
- `H_star^dagger H_star=I`;
- two-branch images of both computational basis states under `H_star`;
- phase kickback `X chi = z star chi`;
- `B_star` inverse on every one of 65,536 two-bit coefficient states.

### Complete one-bit gate inventory

Enumerated all 65,536 `2x2` ring matrices.

Results:

- invertible: 24,576;
- intrinsic-unitary: 512;
- monomial unit phase-permutation: 128;
- nonmonomial invertible branch mixers: 24,448;
- invertible with all entries nonzero: 20,608;
- unitary monomial: 128;
- unitary full splitter: 384.

Analytic check: `|GL2(A)|=|GL2(F2)|*8^4=24,576`.

### Local modal basis classification

Quotiented reversible effect bases by independent unit row scaling and outcome swap.

Results:

- all reversible projective unordered bases: 192;
- intrinsic-unitary projective unordered bases: 4.

The counts agree with the group quotient calculation.

### Modal Bell search

Started with the support Bell state `|00> XOR |11>` and three embedded-F2 reversible bases `Z,X,Y`.

Found a strong support contradiction: no deterministic global assignment.

- all 64 deterministic assignments checked;
- explicit logical contradiction derived from equal-only, forbid-`11`, and forbid-`00` contexts.

Correction/boundary: because every coefficient and effect in this witness lies in `{0,E0}`, the contradiction is inherited from the embedded `F2` modal subtheory. It is **not** a nilpotent-specific CM result.

### `B_star` Bell-like state search and exact support correction

For `Beta_delta=|00> XOR delta|11>`:

- complete four intrinsic-unitary basis family: exact relational local model found (65 compatible global assignments, no uncovered possible sections);
- complete 192 reversible projective basis family: global constraint 2-SAT is satisfiable (10,240 clauses), so **strong** contextuality is ruled out;
- the exact support-extension pass then checked all 137,216 possible sections: 100,352 extend and **36,864 do not**.

This corrects the intermediate interpretation. A global section only rules out strong contextuality; it does not prove possibilistic locality. `Beta_delta` is **logically contextual but not strongly contextual**.

An explicit Hardy-style witness was extracted using canonical basis IDs `R=0`, `X=16`, and `D_delta=28`. Starting from the possible `RR:00` event, forbidden events force `R_A=0 -> X_B=1 -> D_A=0 -> R_B=1`, contradicting the seed `R_B=0`.

### Complete Smith-class contextuality theorem

The exact support-extension method was then run on all 15 canonical Smith representatives under all 192 reversible projective bases. The computational result suggested, and a direct valuation proof established, the complete classification:

- `(a,a)`, `a<4`: **strongly contextual** (4 classes);
- `(a,b)`, `a<b<4`: **logically contextual but not strong** (6 classes);
- `(a,4)`, `a<4`: **relationally local** (4 nonzero separable classes);
- `(4,4)`: zero vector, excluded as a degenerate empty-support model.

Orbit-size aggregation then classifies all 65,536 states: 26,214 strong, 34,056 logical-not-strong, 5,265 nonzero relationally local, and one zero. In particular, all 60,270 nonseparable states are contextual under the complete reversible measurement universe.

Proof ingredients:

1. The complete basis family makes contextuality status invariant under local `GL2(A) x GL2(A)` equivalence.
2. Equal-valuation classes are nonzero scalar multiples of the support Bell matrix and inherit its embedded-F2 strong contradiction.
3. Every off-diagonal class has the same three-setting Hardy implication pattern with `D_c`, `c=u^(b-a)`.
4. Off-diagonal classes are not strong because each reversible basis has an outcome row with unit first coordinate; choosing those outcomes globally makes every context amplitude `u^a(unit XOR nonunit)`, hence nonzero.
5. For separable `diag(u^a,0)`, the same unit-first-coordinate choice extends any specified possible section, proving exact relational locality.

Raw evidence: `data/bell_contextuality_by_smith_class.csv` and `data/offdiagonal_hardy_witnesses.json`.

### Universal pure-CM teleportation

The first attempt using the natural `B_star` resource was found to be degenerate (see below), so a nondegenerate support-Bell basis was constructed.

Shared resource:

`R=|00> XOR |11>`.

Bell-basis columns:

`vec(I), vec(X), vec(K), vec(KX)` with `K=[[1,1],[0,1]]` over `{0,E0}`.

The resulting `4x4` analyzer basis `Q` is Boolean and invertible. Conditional receiver maps after `Q^-1` are `XK,K,X,I`; corrections are `KX,K,X,I`.

Exhaustive result:

- 256 ring-valued one-bit states;
- four outcomes each;
- 1,024/1,024 exact recoveries;
- every outcome branch nonzero for every nonzero input.

No global-unit quotient is used.

### Natural `B_star` teleportation negative result

With `Beta_delta=B_star|00>` and analyzer `B_star^-1`, conditional maps were computed. All four determinants are zero. This proves no branch has a universal `A`-linear inverse correction.

Interpretation developed: CM-nonseparability is too coarse to characterize teleportation resources because zero divisors allow singular but nonseparable coefficient matrices.

### Smith/local-equivalence classification

Used finite-chain-ring Smith theory and an exhaustive binary rank-profile implementation.

Results over all 65,536 two-party coefficient matrices:

- 15 local `GL2(A) x GL2(A)` classes `diag(u^a,u^b)`, `0<=a<=b<=4`;
- separable iff `b=4`;
- five separable classes, ten nonseparable classes;
- 5,266 distinct separable states;
- 60,270 distinct nonseparable states;
- zero mismatches between the Smith criterion and explicit simple-tensor generation.

Resource distinction:

- support Bell: class `(0,0)`;
- `B_star` Bell-like state: class `(0,2)`.

### Local stabilizers

Class orbit counts were used with `|GL2(A)|^2=603,979,776`.

- support Bell exact local stabilizer: 24,576, explicitly `(U,(U^-1)^T)`;
- `B_star` `delta` state exact local stabilizer: 65,536.

Note: these are full two-sided local stabilizers, not the earlier restricted symmetric `U tensor U` stabilizer counts in prior notes.

### Basis-permutation separability classification

Enumerated all 24 two-bit computational-basis permutations.

- 8 preserve all separable states;
- 16 can create nonseparability and each has a retained witness.

The preserving eight are local bit flips with optional party SWAP.

### GHZ investigation

Proved all-cut nonseparability for:

- `G=|000> XOR |111>`;
- `G_delta=|000> XOR delta|111>` generated by `H_star` plus two CNOTs.

For support GHZ under embedded-F2 `Z/X/Y` settings:

- all 512 deterministic assignments checked;
- zero compatible assignments;
- exhaustive search found a minimum contradictory set of six contexts and proved none of size <=5 works;
- a short two-case logical proof was derived from those six contexts.

For `G_delta`:

- embedded-F2 family: 16 globals, exact local support coverage;
- complete intrinsic-unitary family: 23 globals, exact local support coverage.

This is retained as a negative result.

### Secondary results recorded

- linear no-cloning theorem for `{|0>,|1>,|0> XOR |1>}`;
- algebraic/modal superdense-coding-like protocol using `I,X,K,KX`;
- theorem that complete-state unit multiplication is invisible to support-only readout and preserves separability;
- warning that exact CM-pattern readout distinguishes unit multiples;
- Smith pair proposed as a cautious “Smith-Schmidt analogue.”

### Literature search

Current literature was searched before novelty language. Key comparisons are recorded in `LITERATURE.md` and `references.bib`:

- modal quantum theory and finite-field quantum computing;
- possibilistic/sheaf Bell and contextuality;
- phase-group/GHZ work;
- quantum mechanics over sets;
- vector logic/square root of NOT;
- categorical theories over rings/semirings;
- modular stabilizer theory;
- finite-chain-ring quantum-code literature.

Important correction: `F2[u]/(u^s)` already appears in quantum-code literature; `s=4` includes the exact abstract chain ring of this CM phase model. The ring itself therefore must not be claimed as new to quantum information.

### Test execution

Command:

```text
python -m unittest discover -s tests -v
```

Result at this checkpoint: **20 tests passed** after the final contextuality pass. The current package has **22 tests passing** after the teleportation-resource follow-ups.

The exhaustive regeneration command is:

```text
python run_all.py
```

### Next experiments (historical checkpoint)

1. ~~Characterize exactly which of the ten nonseparable Smith classes admit deterministic universal teleportation under arbitrary reversible analyzers and local corrections.~~ **Closed later on 2026-09-17 by the `(0,0)` resource theorem and singular-resource hierarchy.**
2. Determine which parts of the complete-GL measurement contextuality trichotomy survive under narrower gate-generated or intrinsic-unitary measurement families.
3. Extend the valuation-based contextuality analysis to three or more parties, especially the nilpotent GHZ classes.
4. Classify the full `GL4(A)` separability-preserver subgroup, not just basis permutations.
5. Formalize a post-measurement LM/modal update rule and only then revisit monogamy and reduced-state questions.
6. Build the stabilizer-like subgroup generated by `P`, local CM units, `H_star`, and CNOT, and compare its orbit structure to finite modular Clifford formalisms.

## 2026-09-17 — teleportation resource theorem closed

Derived the general branch-map identity `T_m = M^T R_m^T` for arbitrary resource coefficient matrix `M` and arbitrary reversible four-outcome analyzer row reshaping `R_m`. Determinant multiplicativity proves that any universally linearly correctable branch requires `det(M)` to be a unit. The existing embedded-F2 Bell analyzer has four invertible reshaped rows, proving sufficiency for every invertible resource. Therefore deterministic universal exact teleportation is possible iff Smith class is `(0,0)`. Exhaustive regression over all 65,536 resource matrices found exactly 24,576 successes, exactly the `(0,0)` class. This also shows that strongly contextual classes `(1,1)`, `(2,2)`, `(3,3)` are not sufficient teleportation resources.


## 2026-09-17 — singular teleportation hierarchy

Clarified the key example: `delta=u^2`, so `|00> XOR delta|11>` has Smith class `(0,2)`, whereas the support Bell state `|00> XOR |11>` is `(0,0)`. The `(0,2)` state therefore fails universal exact teleportation by the completed unit-determinant theorem.

Investigated four sub-universal tasks. Proved that the maximum exactly recoverable common state family is all 256 states for `(0,0)`, one 16-state free `A`-line for `(0,b), b>0`, and only zero for `a>0`; constructed a reversible four-outcome analyzer attaining the free-line bound. Identified the retained Smith quotient `Q_(a,b)=A/(u^(4-a)) + A/(u^(4-b))`, with `2^(8-a-b)` algebraic classes. For a fixed quotient target `D_(a,b) psi`, proved and computationally attained maximum success-row counts 4 for equal valuations, 2 for off-diagonal nonzero classes, and 3 for rank-one `b=4` classes. Proved that singular resources have zero universally exact postselected full-state branches. Finally, reduction modulo `(u)` gives an ancilla/multicopy no-activation theorem: every singular resource has residue rank at most one, and every finite tensor power remains rank at most one, so no `A`-linear branch can have a left inverse onto `A^2`.

Added `SINGULAR_TELEPORTATION_HIERARCHY.md`, new CSV/JSON evidence, and regression tests.
