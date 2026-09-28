# Non-Authoritative Research Handoff

## Purpose

This handoff summarizes one assistant's preliminary audit of the supplied research direction. It is NOT an authority, proof, novelty clearance, or instruction to preserve these conclusions. Astra must independently test, modify, reject, or replace them.

## Preliminary portfolio boundary

The cleanest non-overlap boundary appeared to be:

- `CM-LMs and lifting` owns the foundational CM/LM operator calculus, valuation architecture, logical pairing/reconstruction, arbitrary-arity lifting, polarity/signed-frame organization, rank/separability foundations, and compact spectral boundary material.
- the pair-compiler/computational project owns pair compilation, S/T/H provenance, its compiler rules, and P14/dispatcher-specific conclusions.
- the present research direction potentially owns a task-specific study of persistent exact structural decompositions used for repeated downstream Boolean operations.

The central risk is that generic CM structure, rank, Kronecker factorization, Boolean decomposition, containment lattices, transformation orbits, or pair-compilation material either belongs elsewhere in the portfolio or has substantial external prior art.

## Strongest provisional paper spine

The strongest preliminary direction was:

**Certified structural decomposition artifacts for repeated Boolean restriction and exact counting, with direct downstream operations that do not require reinflating the full truth table after every query.**

This was judged stronger than a broad paper on CM structural geometry, retrieval, containment, transformations, routing, and decomposition all at once.

## Existing artifact families seen in the recovered implementation

The recovered decomposition work appeared to contain four exact artifact families:

1. XOR-component decompositions;
2. GF(2)-rank factorizations across a variable bipartition;
3. cofactor-block/prototype decompositions;
4. Kronecker-product decompositions.

The implementation also appeared to include bounded partition generation, screened versus more exhaustive arms, reconstruction/checking machinery, and cost accounting. Astra must inspect the actual source rather than rely on this summary.

## Important correctness/claim calibrations

Preliminary inspection suggested:

- the current search should be described as optimal/best only within the frozen candidate-partition universe unless a truly exhaustive theorem/algorithm is established;
- theoretical `factor_bits`-style quantities should be distinguished from actual serialized bytes and resident memory;
- deliberately constructed decomposable functions are correctness controls, not evidence of natural prevalence;
- a checker sharing producer code is not the same thing as an independent semantic verifier;
- historical speedups and oracle headroom should not be reused without raw timing/workload/environment reconciliation;
- lifecycle cost must include discovery, conversion, verification, serialization/loading, query work, and fallback where applicable.

## Candidate new theory to investigate, not assume

A potentially unifying result is a restriction-stability framework.

Let f|rho denote restriction under a partial assignment rho. Investigate whether each supported artifact can be transformed directly into an exact artifact for f|rho without materializing the full truth table. Prove this carefully, state exact access/alignment conditions, and search for counterexamples.

Possible consequences to investigate include:

- XOR-component artifacts restrict locally and may permit exact model counting from local zero/one counts;
- a matrix factorization M = U V over GF(2) restricts by selecting compatible rows/columns, with rank nonincrease;
- cofactor-prototype artifacts may restrict by slicing prototypes and merging duplicates/complements;
- Kronecker products may remain factorized under coordinate-aligned restrictions, and one-counts multiply for pure products;
- satisfiability, tautology, model count, and repeated conditioning may be direct artifact queries for some families.

Do not put any of these in a paper until independently proved and computationally checked.

## Candidate hierarchy/separation questions

Investigate whether there are useful, nontrivial relationships among artifact families, such as implications between disjoint XOR structure, matrix rank, prototype counts, and Kronecker structure; strict separations; exponential or polynomial representation-size gaps; closure properties; and conditions under which one representation dominates another for a stated downstream operation.

Be careful not to duplicate the foundational rank/separability content owned by `CM-LMs and lifting`. If a foundational result already belongs there or is standard prior art, cite it and focus new theory on artifact size, persistence, downstream operations, or task-specific complexity.

## Experimental endpoint suggested by the preliminary audit

The cleanest empirical questions appeared to be:

1. How frequently do the exact artifact families occur in natural bounded Boolean functions or local circuit cuts?
2. How much do they reduce ideal payload size, actual serialized size, and/or resident memory?
3. Can restriction, exact model counting, SAT/UNSAT, or related repeated queries be executed directly on the artifact?
4. When does one-time discovery and verification amortize over Q repeated queries?
5. Can an interpretable structural condition predict when an artifact will be worthwhile?
6. Where do the methods fail, and which baseline dominates there?

A suitable lifecycle expression to refine is:

T(Q) = T_discover + T_verify + T_serialize/load + sum_q T_query(q) + T_fallback.

## Baselines and neighboring literatures that require serious treatment

The preliminary audit identified at least the following neighboring areas. Astra must search primary/current literature independently and broaden this list where needed:

- knowledge compilation and tractable queries/transformations;
- ROBDD/BDD and CUDD-style symbolic representations;
- DNNF/d-DNNF/SDD and model counting where relevant;
- disjoint-support decomposition;
- Ashenhurst-Curtis and modern functional decomposition;
- logic synthesis/ABC and local LUT/cut representations;
- ANF/Mobius/Fourier/Walsh-based structural discovery;
- tensor/Kronecker/tensor-train Boolean representations;
- GF(2) matrix factorization and communication/rectangle perspectives when truly applicable;
- circuit DAG/CSE and direct packed truth-table baselines;
- certified knowledge compilation and independently checkable compilation artifacts.

The preliminary audit found enough prior art that none of the four primitive artifact families should be presented as a new decomposition concept merely because it appears in CM form.

## Directions provisionally demoted

These may still be useful, but were not judged the strongest first paper:

- the 16-CM support-containment lattice: likely useful as an appendix/reference visualization rather than a core research contribution;
- transformation-orbit atlases of the 16 binary operators: pedagogically useful but likely too small for the main novelty claim;
- exhaustive A Phi B = T operator atlases: useful artifact/reference, not obviously a paper spine;
- structural retrieval: potentially valuable later, but modern circuit retrieval/GNN/synthesis work creates a stronger baseline burden and synthetically generated family labels risk circularity;
- generic learned backend routing: historical overhead/headroom evidence suggests this should not be prioritized until cheap oracle headroom is demonstrated for the chosen endpoint.

## Alternative publishable outcome

If the positive structural-artifact paper fails, a rigorous negative-results/reproducibility report may still be valuable if it fully reconciles historical experiments and demonstrates, across more than one narrow compiler experiment, how preprocessing, structural selection, verification, conversion, or fallback destroys apparent oracle gains.

## Suggested framing

A preliminary working title was:

`Certified Structural Decomposition Artifacts for Repeated Boolean Restriction and Exact Counting`

Possible subtitle:

`Task-Matched Computation Without Truth-Table Reinflation`

The preliminary audit suggested that `Correspondence Matrices` need not appear in the main title if the final technical contribution is broader than the CM formalism. CM/LM material can motivate and provide an interface while the new paper remains independently understandable.

## Required posture for Astra

Treat all of the above as claims to attack. A stronger paper may emerge from a different endpoint. If so, change direction. The objective is not to vindicate this handoff; it is to produce the strongest non-overlapping, correct, reproducible, and publishable result supported by the evidence and new research.
