# Literature references used for the Phase-4 priority audit

This is a working audit list, not a claim of exhaustive bibliography coverage.

1. A. Darwiche, **SDD: A New Canonical Representation of Propositional Knowledge Bases**, IJCAI 2011. DOI: 10.5591/978-1-57735-516-8/IJCAI11-143.
2. A. Choi and A. Darwiche, **Dynamic Minimization of Sentential Decision Diagrams**, AAAI 2013. Useful for the explicit definition of compressed \((X,Y)\)-partitions and uniqueness of the compressed partition.
3. H. Vinall-Smeeth, **Structured d-DNNF Is Not Closed under Negation**, IJCAI 2024, pp. 3593–3601. DOI: 10.24963/ijcai.2024/398.
4. N. H. Bshouty, T. R. Hancock, and L. Hellerstein, **Learning Boolean Read-Once Formulas over Generalized Bases**, Journal of Computer and System Sciences 50(3), 1995, pp. 521–542. DOI: 10.1006/jcss.1995.1042.
5. M. C. Golumbic, A. Mintz, and U. Rotics, **Factoring and Recognition of Read-Once Functions using Cographs and Normality**, DAC 2001, pp. 109–114. DOI: 10.1145/378239.378356.
6. A. Mintz and M. C. Golumbic, **Factoring Boolean Functions using Graph Partitioning**, Discrete Applied Mathematics 149 (2005), pp. 131–153. DOI: 10.1016/j.dam.2005.02.007.
7. R.-R. Lee, J.-H. R. Jiang, and W.-L. Hung, **Bi-Decomposing Large Boolean Functions via Interpolation and Satisfiability Solving**, DAC 2008. DOI: 10.1145/1391469.1391634. The paper explicitly uses incremental SAT and unit assumptions for automatic variable partitioning.
8. O. Zeyen, K. Tit, and M. Cordy, **DivKC: A Divide-and-Conquer Approach to Knowledge Compilation**, 2026. Adjacent work on splitting formulas into components for independent d-DNNF compilation.

## Priority interpretation

These references establish substantial prior art for SDD decomposition structure, structured-d-DNNF limitations, read-once factorization, and incremental SAT bi-decomposition. Phase 4 therefore restricts its claims to the carrier-constrained simultaneous factor problem, its CM four-corner/rank bridge, the exact signed CM recursion proved for the read-once operator-tree subclass, the vtree-laminar SDD extraction result, and the integration of these direct certificates with a persistent residual SAT oracle.
