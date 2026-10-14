# Structural Class Comparison

| Structural class | Exact result found | Nontrivial in dimension >2? | Torsion? | Priority assessment |
|---|---|---:|---:|---|
| Exclusive inversion graph is a matching | Direct-sum coarse-edge-link formula for all integral cone homology | **Yes** | **Yes** | Strongest gate result; specialized exact theorem, close to standard vertex-deletion machinery |
| Bounded coarse poset + matching | Only global bottom-to-top inversion can contribute | Yes | Depends on proper part | Clean corollary |
| Finite distributive lattice + endpoint matching | Boolean `B_r` gives `H_r=Z`; non-Boolean distributive gives zero | **Yes** | No | Very clean structured example; crosscut theory is standard |
| Entire refined relation Horn / meet-closed | Both refined and projected posets have minima; cone contractible | No | No | Exact but topologically trivial |
| Entire refined relation dual-Horn / join-closed | Dual contractibility result | No | No | Exact but topologically trivial |
| Exclusive inversion graph empty | Isotone section; homotopy equivalence | No | No | Exact zeroth obstruction |
| Exclusive inversion graph a forest | No edgewise classification; 3-chain star is counterexample | Already fails in smallest star | N/A | **Rejected** |
| Coarse chain | Existing Ferrers/independence-complex trichotomy | No rich high homology | No | Mostly prior art / companion result |
| Weighted height <=2 | Existing rooted-incidence/TU classification | Dimension <=2 only | No | Previous exact theorem |
| Height 3 without further restriction | Torsion already possible | Yes | Yes | Too broad for clean coefficient-independent theorem |
| Controlled BWW lower fibers | Classical wedge/fiber results under connectivity hypotheses | Sometimes | Yes | Strong prior art; useful sufficient framework |
| Shellable/Cohen--Macaulay relevant edge links + matching | Matching formula specializes to concentrated/torsion-free homology as appropriate | Yes | Usually no over chosen coefficients | Corollary, not separate core theorem |
| General exclusive graph | Interaction-core spectral sequence indexed by chain-supported bicliques | Yes | Yes | Level-C general machinery; classification open |

## Main comparison

The strongest natural dividing line discovered is **interaction degree**, not height or graph acyclicity.

- `E_psi = empty`: no mixed interaction exists; a monotone section gives homotopy neutrality.
- `E_psi` a matching: every mixed relative simplex has one unique exclusive edge; exact link summation follows.
- first shared endpoint: three-vertex cores appear and generate differentials between edge defects.
- larger bicliques: higher interaction levels appear.

This explains both why the matching theorem is exact and why the forest generalization fails.
