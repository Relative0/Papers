# Carrier-Aware Bounded Width + SAT Four-Corner CM — Phase 3 Master Report

**Project:** The MIND / Gluing Concepts / Succinct Structured Factorization  
**Date:** 29 September 2026

## Executive result

Both requested branches were completed.

### Branch A — bounded-width theorem

A full finest-partition FPT result is available when the parameter is the treewidth of the **combined incidence graph** containing both semantic CNF clauses and carrier minimal nonfaces. The proof uses an exact pair-separation formulation: two attributes belong to different prime structured factors exactly when there exists a carrier-compatible cut separating them on which the four-corner CM defect is identically zero. This becomes a fixed-alternation QBF whose incidence width grows only by a constant factor. Bounded-treewidth fixed-alternation QBF is FPT, so `O(n^2)` pair queries recover the unique finest simultaneous partition.

This theorem is mathematically sound and useful, but the priority audit found that its algorithmic core sits close to established QBF bi-decomposition and bounded-width QBF/knowledge-compilation theory. It should currently be treated as a **carrier-aware synthesis theorem**, not advertised as a fundamentally new treewidth result.

### Branch B — SAT four-corner algorithm

An exact DIMACS-generating implementation was built. For a fixed cut it encodes

\[
D_f=(F_{00}\wedge F_{11})\mathbin{\Updownarrow}(F_{01}\wedge F_{10})
\]

with two input copies per original variable and four internal copies of the semantic circuit/CNF.

- SAT => a concrete nonzero-minor witness, hence rank `>1` and nonseparability.
- UNSAT => implicit CM rank `<=1`, hence exact AND-factorization.

The implementation includes a pure-Python DPLL only for reproducibility, DIMACS export for industrial solvers, witness decoding/verification, and recursive refinement restricted to carrier-block unions.

## New theorem statement

Let \(G_{K,\varphi}\) be the combined incidence graph of attributes, CNF clauses, and carrier minimal nonfaces, and let \(\tau=\operatorname{tw}(G_{K,\varphi})\). Then the canonical finest partition on which both the simplicial carrier and CNF semantics factor is computable in

\[
F(\tau)\operatorname{poly}(|K|+|\varphi|).
\]

The proof and exact QBF contract are in `docs/BOUNDED_WIDTH_CARRIER_AWARE_THEOREM.md`.

## Priority correction

The search found strong antecedents that materially narrow any claim:

- SAT-based Boolean bi-decomposition and automatic variable partitioning were already developed by Lee--Jiang--Hung (DAC 2008).
- Chen--Janota--Marques-Silva (DATE 2012) explicitly treat OR/AND/XOR bi-decomposition and use QBF to optimize unknown variable partitions.
- Capelli--Mengel establish FPT algorithms for bounded-treewidth quantified CNF with bounded quantifier alternation.
- bounded-treewidth Boolean circuits/CNFs have mature d-DNNF compilation theory.

Therefore neither "use SAT/QBF for AND decomposition" nor "bounded treewidth makes the quantified decomposition decision FPT" should be claimed as new.

The project-specific content is the coupling of the simplicial carrier constraint, CM four-corner rank certificate, and recovery of the canonical *simultaneous* finest factor partition.

## Computational evidence

- 200 random fixed-cut CNF tests: four-corner SAT encoding vs exhaustive implicit-matrix minors, **0 failures**.
- 80 random carrier-aware factor-recovery tests vs exhaustive partition/product verification, **0 failures**.
- on those 80 tiny examples, carrier blocks reduced the mean raw cut space from 19.35 to 2.4125 and recursive recovery used 1.825 SAT calls on average. These are illustrative only.

## Recommendation for the next convergence gate

Do **not** continue by merely proving another generic bounded-width corollary. The next research phase should compare three stronger possibilities:

1. **structured-d-DNNF direct factor extraction:** can the finest carrier-aware partition be read/recovered in singly exponential (or polynomial in compiled size) time without the generic QBF tower?
2. **incremental SAT implementation:** use one shared four-copy circuit with cut-control assumptions, preserving learned clauses across candidate cuts; benchmark against independent-cut SAT and against existing bi-decomposition formulations.
3. **CM/LM operator-DAG subclass:** search for a syntactic condition under which the prime factor partition is recoverable directly from the typed operator graph, yielding an actual representation-specific theorem rather than a restatement of general Boolean decomposition.

The first and third offer the strongest theorem-level novelty prospects; the second offers the strongest near-term computational evidence.
