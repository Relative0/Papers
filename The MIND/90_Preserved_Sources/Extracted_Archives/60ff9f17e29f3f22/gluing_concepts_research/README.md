# Gluing Concepts Research Package

**Project:** *Gluing Concepts: Composition, Reconstruction, and Clean Decomposition in Simplicial Mental Spaces*  
**Audit date:** 28 September 2026  
**End-state:** **Outcome 4 — Requires additional structure**

This package is the requested independent mathematical audit of the gluing/decomposition research seed in the 2015 thesis. The thesis is treated as a fixed historical source, not as mathematical authority.

## Main determination

The historical material contains two genuine but different research seeds: (i) reconstruction of higher-dimensional/logical objects from lower-dimensional faces, and (ii) local-to-global gluing of compatible presheaf/sheaf information. A rigorous modern theory must separate **ordinary simplicial gluing**, **completion/filling**, **semantic local-to-global coherence**, and **factorization/separability**.

The recommended ontology is two-level: a labelled simplex is an **atomic concept**; a finite simplicial complex is a **conceptual/mental structure**. Nontrivial claims about meaning or independence use a structured concept \((K,\lambda,\mathcal S)\) with an explicitly declared semantic layer.

The strongest next target is **Succinct Structured Factorization**: given a compactly represented simplicial complex and an intensionally represented Boolean/CM semantic object on the same attributes, compute the unique finest partition on which both layers factor, or certify irreducibility, without expanding the full truth table.

## Reproduce the finite computation

Run from the package root:

```bash
python3 code/gluing_audit.py
```

The script is standard-library Python. It writes/updates the JSON/CSV results in `data/`. Exhaustive enumeration was completed for all abstract simplicial complexes using every vertex on labelled vertex sets of size at most 5.

## Key computational result

Across **7,020** complexes using all labelled vertices (n=1..5), the audit performed **104,237** unordered bipartition checks of the minimal-nonface join criterion, with **0 criterion failures** and **0 failures** of reconstruction from the computed finest join factors. These computations validate the implementation and finite test range; they are **not** offered as a novelty claim.

## Package map

The nine requested reports are at the package root and duplicated under `docs/`:

- `GLUING_CONCEPTS_MASTER_AUDIT.md`
- `FORMAL_GLUING_DEFINITIONS.md`
- `DECOMPOSITION_AND_SEPARABILITY.md`
- `GLUING_VS_UNFOLDING.md`
- `CHAIN_LEVEL_GLUING.md`
- `SHEAF_LOCAL_TO_GLOBAL_ANALYSIS.md`
- `FINITE_EXAMPLES.md`
- `LITERATURE_PRIORITY_MAP.md`
- `THEOREMS_COUNTEREXAMPLES_OPEN_PROBLEMS.md`

Additional files include `RESEARCH_LEDGER.md`, `RESEARCH_PROMPT_4.md`, `REPRODUCIBILITY.md`, exact CSV/JSON tables in `data/`, and the script `code/gluing_audit.py`.
