# Paper U draft package — v0.1

This package contains an initial theorem-led draft for the ultrametric/resolution paper separated from the simplicial unfolding/gluing project.

## Files

- `Paper_U_Resolution_Limited_Ultrametric_Concepts_v0.1.tex` — main manuscript draft.
- `paper_u_refs.bib` — bibliography.
- `Paper_U_Bridge_to_Paper_F.md` — explicit scope boundary and bridge to the unfolding/gluing paper.

## Core manuscript thesis

Ultrametricity supplies hierarchy and a scale of distinguishability, not topological indistinguishability by itself. Finite-resolution observation maps supply observational equivalence. At resolution `k`, the concept balls are simultaneously fibers of the observation map, zero-classes of an ultrapseudometric, orbits of a within-fiber symmetry group, and the classes on which all level-`k` observables are constant.

## Central theorem package

1. Prefix metric is ultrametric.
2. Concepts are clopen balls and form a laminar rooted hierarchy.
3. Resolution-`k` observation topology is a partition topology; each concept fiber is internally indiscrete.
4. Truncated ultrapseudometric induces exactly that topology.
5. Resolution equivalence theorem identifies coordinate, ball, pseudometric, observable, and group-orbit descriptions.
6. Ultrametric distance is a monotone encoding of minimum distinguishing resolution.
7. Prime-base model is isometric to `Z_p`, with observation quotients `Z/p^k Z`.
8. Finer resolution strictly reduces the invisible symmetry group.
9. XOR is a two-orbit quotient that distinguishes equality/inequality without orienting the operands; one anchor bit completes reconstruction.

## Important scope decision

The manuscript deliberately calls `k -> k+1` **resolution refinement**, not unfolding. Simplicial unfolding is reserved for Paper F.
