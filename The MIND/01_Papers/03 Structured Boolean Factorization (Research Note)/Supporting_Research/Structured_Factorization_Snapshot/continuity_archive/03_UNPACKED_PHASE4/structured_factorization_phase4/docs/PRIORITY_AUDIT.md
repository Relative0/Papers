# Phase 4 Priority Audit

**Date:** 29 September 2026

This note records the claim boundaries discovered while attacking direct factor extraction and incremental SAT.

## 1. Structured d-DNNF / SDD

### Established

- Sentential Decision Diagrams use recursive \((X,Y)\)-partitions; in a partition the primes are nonfalse, mutually exclusive and exhaustive.
- A compressed partition has pairwise distinct subs and is canonical for a fixed split/vtree under the usual SDD reduction conditions.
- Structured d-DNNF is a broader noncanonical representation.
- Vinall-Smeeth (IJCAI 2024), *Structured d-DNNF Is Not Closed under Negation*, proves that structured d-DNNF does not support polynomial-time negation, disjunction, or existential quantification in general.
- 2026 DivKC work explicitly decomposes formulas so components can be compiled independently to d-DNNF, demonstrating active nearby work on decomposition/knowledge-compilation interaction.

### Claim boundary

Do not claim novelty for compressed SDD partitions, canonicity, vtrees, or generic decomposability. The Phase-4 SDD result is best framed as a new-to-this-project bridge:

\[
\text{compressed cofactor exposure}
\longleftrightarrow
\text{CM rank-one flattening}
\longleftrightarrow
\text{AND factorability across the vtree cut},
\]

plus an exact characterization of the finest **vtree-laminar** factorization and its role in a carrier-aware residual algorithm.

A dedicated literature search did not establish a prior theorem with this exact CM/carrier formulation, but this is not proof of historical firstness.

## 2. Read-once operator trees

### Established

Read-once Boolean functions are classical. Polynomial recognition, factoring, and exact identification have been studied for decades, including:

- Bshouty, Hancock, and Hellerstein (JCSS 1995), read-once formulas over generalized bounded-fan-in bases;
- Golumbic, Mintz, and Rotics (DAC 2001; later journal treatment), cograph/normality recognition and factorization;
- Mintz and Golumbic (Discrete Applied Mathematics 2005), general Boolean factoring with read-once routines as a special exact subproblem.

### Claim boundary

Do not claim that Phase 4 discovers efficient read-once factorization. The specific mathematical object worth preserving is the CM theorem:

- requested gate CM rank one \(\Rightarrow\) signed conjunctive split and signed recursive descent;
- requested gate CM rank two \(\Rightarrow\) every cross-support pair has a nonzero four-corner minor, fusing the child supports into one prime factor block.

Whether that exact signed CM-rank recursion has appeared before remains unresolved by the present search.

## 3. Incremental SAT

### Established

Lee, Jiang, and Hung (DAC 2008), *Bi-Decomposing Large Boolean Functions via Interpolation and Satisfiability Solving*, explicitly use incremental SAT and unit assumptions for automatic variable partitioning. Later SAT/QBF bi-decomposition literature broadens these techniques.

### Claim boundary

Do not claim novelty for incremental SAT, assumption solving, or SAT-based Boolean bi-decomposition.

The project-specific comparator is narrower:

- selector variables correspond to **carrier prime blocks**, not arbitrary individual variable classifications;
- one four-copy circuit realizes the project's **CM four-corner rank defect**;
- all carrier-compatible cuts are assumption vectors on that one circuit;
- the result is used to recover the canonical **simultaneous** carrier/semantic partition or to certify residual factors after direct extraction.

## 4. Closest current adjacent work

DivKC (2026) uses divide-and-conquer formula decomposition to improve knowledge compilation to d-DNNF, reporting compilation of formulas previously out of reach for D4. Its goal is compilation scalability rather than recovery of the canonical Cartesian/AND prime partition or the carrier/CM structured factorization considered here. It should nevertheless be cited in any paper positioning decomposition as a preprocessing/compilation strategy.

## 5. Current novelty status

| Item | Mathematical status | Priority status |
|---|---|---|
| compressed-SDD vtree-cut criterion | proved in Phase 4 | likely close to an immediate SDD-cofactor consequence; claim bridge, not firstness |
| finest vtree-laminar extraction | proved in Phase 4 | exact packaging useful; dedicated priority search still needed |
| prime-aligned SDD full extraction | corollary | likely synthesis-level |
| CM signed rank recursion on read-once operator trees | proved in Phase 4 | promising project-specific formulation; read-once factorization itself is old |
| rank-two four-corner fusion proof | proved in Phase 4 | potentially useful CM-specific lemma; firstness unestablished |
| selector-controlled four-corner SAT | proved equivalent and implemented | incremental SAT is prior art; carrier/CM control is project-specific integration |
| hybrid direct-then-SAT architecture | exact synthesis | potentially publishable as an integrated algorithm after industrial benchmarking |

## 6. Publication guidance

A future paper should lead with the exact problem and its cross-layer invariant, not with generic claims about knowledge compilation or SAT. A defensible framing is:

> Given a simplicial carrier and Boolean semantics, recover the canonical finest partition that simultaneously respects join structure and conjunctive semantic structure. We give direct extraction theorems on two structured semantic representations and a carrier-controlled four-corner SAT fallback for the residual case.

The paper should explicitly distinguish theorem novelty, representation-specific reformulation, and engineering contribution.
