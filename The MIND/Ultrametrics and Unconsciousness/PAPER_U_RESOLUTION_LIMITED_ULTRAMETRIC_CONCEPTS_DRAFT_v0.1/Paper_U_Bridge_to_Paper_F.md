# Paper U / Paper F boundary and bridge

## 1. Terminology correction

Do **not** call the operation `00 -> {000,001}` simplicial "unfolding." In Paper U it is **resolution refinement**: one observational equivalence class is split into finer classes.

Reserve **unfolding** for Paper F, where a higher simplex or complex is decomposed into lower-dimensional faces/subcomplexes together with incidence, overlap, or attachment data.

## 2. Two different kinds of symmetry reduction

### Paper U: observational symmetry reduction

At resolution `k`, a group `G_k` of tree automorphisms can rearrange states within each depth-`k` concept without changing any available observation. Refining to `k+1` makes some of these rearrangements visible, so

`G_{k+1} < G_k`.

No simplex is decomposed, and no child needs to be chosen merely to refine the partition.

### Paper F: structural symmetry reduction by gluing

Suppose pieces `K_1,...,K_r` are individually isomorphic and hence permutable. Before attachment there may be a large permutation symmetry `H <= S_r`. Once gluing maps, incidences, or overlaps are specified, only

`H_attach = {h in H : h preserves the attaching data}`

remains a symmetry.

Thus asymmetric gluing can genuinely break symmetry by adding relational information.

## 3. Why decomposition needs connection data

A higher simplex cannot in general be reconstructed from an unordered bag of lower-dimensional pieces. One also needs to know which faces intersect, along what common subfaces, and with what identifications/orientations. In categorical language this is a diagram plus a colimit/gluing construction; in simplicial language it is incidence/face data; in sheaf-like language it is compatibility on overlaps.

This is likely central to Paper F: **unfolding without attachment data is information loss**.

## 4. XOR as a bridge concept

For two bits `(a,b)`, XOR has fibers

- XOR = 0: `{00,11}`;
- XOR = 1: `{01,10}`.

So XOR distinguishes equality from inequality while leaving operand orientation unresolved. It is therefore a clean example of **partial distinguishability**. Adding one anchor bit makes the pair fully reconstructible:

`b = a XOR XOR(a,b)`.

Paper U can use this as an elementary illustration of an observation that breaks some symmetry but not all of it. Paper F/CM work can later study how such local distinction operators interact with decomposition and gluing.

## 5. Proposed division of labor

### Paper U
- rooted trees / prefix spaces;
- ultrametrics and p-adic coordinates;
- primitive concepts as balls;
- finite-resolution quotients;
- partition topologies and ultrapseudometrics;
- symmetry groups of unresolved fibers;
- entropy, filtrations, adaptive resolution;
- XOR as partial distinguishability.

### Paper F
- simplices and concept complexes;
- unfolding into faces/subcomplexes;
- exact reconstruction versus information loss;
- gluing and attaching data;
- symmetry effects of assembly;
- chain complexes and homology;
- functorial maps under decomposition/refinement.

### Bridge paper or later section, only if strong theorems appear
Associate an internal complex `K_s` to each hierarchical concept `C_s`. If refinement maps induce simplicial maps `K_{sa} -> K_s`, investigate induced chain and homology maps and the resolution at which a topological feature becomes observable.
