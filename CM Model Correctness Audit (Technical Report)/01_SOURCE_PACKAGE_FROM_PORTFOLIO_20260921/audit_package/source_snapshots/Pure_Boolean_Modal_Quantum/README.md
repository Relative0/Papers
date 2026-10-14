# Pure-Boolean CM Modal / Quantum-like Investigations

**Research snapshot:** 2026-09-17  
**Status:** mathematical/computational working research; not peer reviewed  
**Core coefficient system:** `A = F2[C4] ~= F2[u]/(u^4)`  
**Scope:** Boolean coefficients only. No signed `J` lift, negative/complex amplitudes, square-root normalization, or Born probabilities occur in the claimed constructions.

This directory is a self-contained continuation of the Correspondence-Matrix (CM) phase program focused on modal, possibilistic, and ring-module analogues of quantum structures. It deliberately separates:

1. **proved algebraic statements**;
2. **exhaustive finite searches** over an explicitly stated universe;
3. **computational regression checks**;
4. **open questions/conjectures**; and
5. **literature comparisons**.

The original CM paper remains the source for the CM ordering, XOR/AND logic, rotations/transposes, support quotient, LMs, and tensor constructions. The cyclic-convolution product `star` and the ring interpretation are later research extensions and are not retroactively attributed to the original paper.

## Main results in this snapshot

| Investigation | Result | Evidence status |
| --- | --- | --- |
| Modal Bell test | The support Bell state `E0|00> XOR E0|11>` with three embedded-F2 reversible local bases has **no compatible deterministic local hidden-variable assignment**. An explicit Boolean contradiction is given. | Proved from the displayed support tables; exhaustive check of all `2^6 = 64` deterministic assignments. |
| Complete Smith-class contextuality | Across **all 192 reversible projective local bases**, the ten nonseparable Smith classes split exactly: `(a,a)`, `a<4`, are **strongly contextual**; `(a,b)`, `a<b<4`, are **logically contextual but not strong**; every nonzero separable `(a,4)` class is exactly relationally local. The zero state is excluded. | Theorem with explicit witnesses/global sections plus exhaustive exact-support verification of all 15 canonical classes; by local-equivalence invariance this classifies all 65,536 states. |
| Pure-CM teleportation | A reversible Boolean/CM Bell-basis analyzer and the support Bell resource teleport **every** one-bit ring state `A|0> XOR B|1>`, `A,B in A`, exactly. No global-phase quotient is required. | Algebraic construction plus all `16^2 * 4 = 1024` outcome/state checks. |
| `B_star` Bell/teleport resource | The natural `B_star` state `E0|00> XOR delta|11>` (Smith `(0,2)`) is **logically contextual but not strongly contextual** across all 192 bases, yet it does **not** support the analogous universal correction scheme: all four conditional receiver maps are singular. | Exact support coverage + Hardy witness + proved teleportation obstruction. |
| GHZ | `|000> XOR |111>` is nonseparable across every bipartition and gives a modal GHZ contradiction with six contexts from three embedded-F2 local settings. | Algebraic proof; all `2^9 = 512` deterministic assignments checked; exhaustive search proves no subset of <=5 of the 27 tested contexts is already contradictory. |
| Nilpotent GHZ analogue | `|000> XOR delta|111>` is nonseparable across every cut, but the tested MQT-style and complete intrinsic-unitary basis families admit exact relational local models. | Negative exhaustive finite result for those setting families. |
| One-bit gate inventory | Of `16^4 = 65,536` `2x2` matrices over `A`, `24,576` are invertible, `512` satisfy `U^dagger U=I`, `128` are monomial unit phase-permutation gates, and `24,448` are nonmonomial invertible branch mixers. | Exhaustive finite classification. |
| Local measurement bases | There are `192` unordered reversible projective two-outcome bases modulo independent unit rescaling of effects and outcome swap; only `4` such projective bases are represented by intrinsic-unitaries. | Count proof plus exhaustive enumeration. |
| Two-party local equivalence | All `65,536` two-party coefficient matrices fall into exactly `15` local `GL2(A) x GL2(A)` Smith classes `diag(u^a,u^b)`, `0<=a<=b<=4`. Exactly the five classes with `b=4` are separable. | Chain-ring Smith theorem + exhaustive classification/factorization regression. |
| Distinct states | `5,266` of the `65,536` two-party coefficient states are CM-separable; `60,270` are CM-nonseparable. | Exhaustive finite search. |
| Basis permutations | Among all `24` computational-basis permutations of two bits, exactly `8` preserve separability for every separable ring state; the other `16` have explicit nonseparability witnesses. | Exhaustive finite search. |
| Global CM units | Multiplying a complete state by a unit is invisible to **support-only** possible/impossible readout and preserves separability, but generally changes exact CM-pattern readout. | Proved. |
| No cloning | No `A`-linear exact cloner can clone `|0>`, `|1>`, and `|0> XOR |1>` simultaneously with a fixed blank. | Proved by linearity. |

## Important corrections / boundaries

- **CM-nonseparable is a ring-module definition, not a claim of physical quantum entanglement.**
- The positive Bell and GHZ contradictions found here live entirely in the embedded `F2` subtheory. They therefore demonstrate that the CM ring **contains** a familiar finite-field modal nonlocal subtheory; they do not show that CM nilpotents are the cause of those contradictions.
- Conversely, nilpotents materially change the state/resource hierarchy. The intrinsic `B_star` Bell-like state has Smith class `(0,2)`: it is nonseparable yet its coefficient matrix is singular. It is also logically contextual but not strongly contextual in the complete reversible-basis universe. More generally, the ten nonseparable Smith classes split into four strong equal-valuation classes and six off-diagonal logical-not-strong classes.
- The off-diagonal logical witnesses are ring-specific in their resource origin: their unequal nilpotent valuations have no analogue as distinct nonzero rank-two classes over a field. The Hardy-style logical implication pattern itself is not claimed as a new form of contextuality.
- The natural `H_star`-generated GHZ-like state is nonseparable but **local for the tested modal measurement families**. This negative result is retained.
- No positive probability norm, Born rule, physical collapse law, or quantum speedup is derived.
- The modal measurement rule used here is an explicit research contract: apply reversible local effect bases and call an outcome possible iff its coefficient is nonzero. The original paper supplies LM truth/relationship measurement machinery and explicitly does not incorporate probability densities, but it does not itself define this ring-valued modal state-measurement semantics.

## Reproduce

Requires Python 3.10+ and only the standard library.

```bash
python run_all.py
python -m unittest discover -s tests -v
```

`run_all.py` regenerates the raw CSV/JSON result files and the summary log. The tests re-check the principal identities, counts, Bell/GHZ contradictions, teleportation, and Smith classification.

## Directory map

```text
Pure_Boolean_Modal_Quantum/
├── README.md
├── DEFINITIONS_AND_NOTATION.md
├── RESULTS.md
├── NEGATIVE_RESULTS.md
├── RESEARCH_LOG.md
├── LITERATURE.md
├── MODAL_CM_RESEARCH_SUMMARY.md
├── TELEPORTATION_RESOURCE_THEOREM.md
├── SINGULAR_TELEPORTATION_HIERARCHY.md
├── EVIDENCE_INDEX.json
├── references.bib
├── MANIFEST_SHA256.txt
├── run_all.py
├── src/
│   ├── cm_ring.py
│   └── analysis_core.py
├── tests/
│   └── test_cm_modal.py
├── data/
│   ├── gate_inventory_65536.csv
│   ├── measurement_bases_192.csv
│   ├── modal_bell_mqt_tables.csv
│   ├── bell_bstar_complete_reversible_basis_sat.json
│   ├── bell_contextuality_by_smith_class.csv
│   ├── offdiagonal_hardy_witnesses.json
│   ├── teleportation_all_256_states_x4_outcomes.csv
│   ├── teleportation_protocol.json
│   ├── bstar_teleportation_failure.json
│   ├── teleportation_resource_theorem.json
│   ├── teleportation_resource_inventory_65536.csv
│   ├── teleportation_resource_by_smith_class.csv
│   ├── singular_teleportation_hierarchy.json
│   ├── singular_teleportation_hierarchy_by_smith_class.csv
│   ├── state_local_class_inventory_65536.csv
│   ├── local_equivalence_classes.csv
│   ├── two_party_basis_permutation_gates.csv
│   ├── ghz_support_mqt_contexts.csv
│   ├── ghz_delta_mqt_contexts.csv
│   └── ghz_hidden_variable_search.json
├── logs/
│   ├── run_summary.json
│   ├── console_output.txt
│   ├── test_output.txt
│   ├── validation.txt
│   ├── run_timing.txt
│   └── chktex.txt
└── paper/
    └── PURE_BOOLEAN_MODAL_CM_ADDENDUM.tex
```

## Source provenance

The working source set for this pass consisted of:

- Brian Droncheff, *Correspondence Matrices; Algorithms for Propositional Logic* (user-supplied manuscript found in the ChatGPT File Library).
- *Intrinsic Boolean Phase Algebra of Correspondence Matrices* (17 September 2026 working draft found in the File Library).
- `CURRENT_STATE.md` from the prior CM phase thread.
- The public repository `Relative0/Correspondence_Matrices`, especially `docs/research/README.md`, used to preserve its correctness-gating, artifact-equivalence, provenance, and negative-result discipline.
- The literature listed in `LITERATURE.md` and `references.bib`.

I did **not** have direct access to `C:\Users\brian\Documents\CM Quantum`; this package is intended to be copied into that location, e.g. as `Pure_Boolean_Modal_Quantum/`.

## Latest theorem

The deterministic tight teleportation resource classification is complete. See `TELEPORTATION_RESOURCE_THEOREM.md`: universal exact one-bit teleportation is possible iff the two-party resource has unit determinant, equivalently Smith class `(0,0)`. The follow-up `SINGULAR_TELEPORTATION_HIERARCHY.md` classifies what remains below that threshold: exact free-line transfer, Smith-quotient transfer, heralded/postselected no-go results, and local-ancilla/finite-copy non-activation.
