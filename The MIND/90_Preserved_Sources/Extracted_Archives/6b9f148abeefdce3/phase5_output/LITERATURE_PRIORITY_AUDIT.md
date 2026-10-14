# Literature and Priority Audit through 2026

## Claim matrix

| Proposed claim | Priority finding | Safe posture |
|---|---|---|
| Search vtrees by local rotations | Choi & Darwiche 2013 already do dynamic vtree search with rotations/swaps | prior art |
| Optimize vtree for SDD size | established SDD practice | prior art |
| Use graph/treewidth structure to build compilation trees | longstanding dtree/vtree/SDNNF work; active through 2026 | prior art |
| Detect independent CNF components before/inside compilation | standard SAT/#SAT/decision-DNNF technique | prior art |
| Use SAT/QBF to find Boolean bi-decompositions/variable partitions | established by 2008-2012 bi-decomposition literature | prior art |
| Carrier blocks as hard vtree modules | no direct antecedent identified, but unsafe without laminar compatibility | project-specific structural theorem, not yet broad algorithmic novelty |
| Optimize **factor exposure**, not SDD size | no exact antecedent found in this search | potentially distinctive objective; priority not proven |
| Treat CM defect supports as hyperedges for vtree adaptation | no exact antecedent found | potentially distinctive; needs algorithm and experiments |
| Infer pairwise must-link from any failed cut | false | do not claim |

## Key references

1. A. Choi, A. Darwiche, *Dynamic Minimization of Sentential Decision Diagrams*, AAAI 2013, DOI 10.1609/aaai.v27i1.8690.
2. H. Chen, M. Janota, J. Marques-Silva, *QBF-Based Boolean Function Bi-Decomposition*, DATE 2012, arXiv:1112.2313.
3. A. de Colnet, *On the Relative Efficiency of Dynamic and Static Top-Down Compilation to Decision-DNNF*, SAT 2024, DOI 10.4230/LIPIcs.SAT.2024.11.
4. C. Berkholz, S. Mengel, H. Wilhelm, *A Characterization of Efficiently Compilable Constraint Languages*, STACS 2024, DOI 10.4230/LIPIcs.STACS.2024.11.
5. V. Derkinderen, J.-M. Lagniez, *Circuit-Aware d-DNNF Compilation*, IJCAI 2025, DOI 10.24963/ijcai.2025/496.
6. F. Capelli, Y. Choi, S. Mengel, M. Muñoz, G. Van den Broeck, *A Canonical Generalization of OBDD*, SAT 2026, DOI 10.4230/LIPIcs.SAT.2026.10.
7. SAT preprocessing literature documents connected-component splitting as established preprocessing; component caching is standard in model counting.

## Priority conclusion

The broad algorithmic ingredients are crowded prior art. Any publication claim should center on exact carrier/semantic compatibility, CM defect-support structure, or a demonstrated factor-exposure objective advantage rather than on vtree search, hypergraph partitioning, or component decomposition themselves.
