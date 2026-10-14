# Theorem dependency map

This map distinguishes standard background, earlier ProLT-derived material, post-audit
proofs, and computer-assisted evidence. The manuscript is intentionally arranged so
that the primary theorem does not depend on the later sharpness computations.

## Dependency key

- **STD** - established external mathematics.
- **OLD** - validated result already present in the earlier ProLT v0.1-v0.5 program.
- **AUDIT** - proof/strengthening produced during the 24 September 2026 audit.
- **NEW-CERT** - exact post-audit seven-state certificate supplied with the update.
- **COMP** - exhaustive finite computation; not a replacement for a mathematical proof.

| Manuscript result | Status | Direct dependencies | What it establishes |
|---|---|---|---|
| Sec. 2 relative two-layer complex | STD + OLD | order complexes; relative chains; height <=2 | Only deleted edges and triangles occur in the relative complex. |
| Prop. 3.2 integral incidence recognition | AUDIT (strengthens OLD) | four one-bit three-chain patterns; oriented simplicial boundary | Relative boundary is a reduced oriented graph-incidence matrix over Z. |
| Thm. 3.3 complete integral relative homology | AUDIT + STD | Prop. 3.2; graph-incidence rank/cycle formulas; total unimodularity | `H_2=Z^{beta_1}`, `H_1=Z^{c_0}`, no relative torsion, coefficient-independent ranks. |
| Lemma 4.1 two-layer matching--collapse | AUDIT + STD | relative edge--triangle support graph; sink/free-face induction | In dimension <=2, an acyclic perfect relative matching is exactly a direct relative collapse certificate. |
| Thm. 4.2 one-bit height-two recognition | AUDIT + OLD + STD | Thm. 3.3; Lemma 4.1; rooted-tree leaf pruning | F2/field/Z neutrality, rooted forest, perfect acyclic relative matching, collapse, simple type, and homotopy equivalence are equivalent. |
| Cor. 4.3 greedy collapse algorithm | consequence | Thm. 4.2 | Leaf pruning decides the neutral case after defect extraction. |
| Prop. 5.1 repair maps | OLD + STD | comparable monotone maps on posets | Arbitrary-height sufficient homotopy certificates. |
| Cor. 5.2 floors/ceilings and semilattice closure | OLD + STD | Prop. 5.1; finite meets/joins | Concrete down/up repair maps. |
| Cor. 5.3 Horn-type specialization | OLD + STD | Cor. 5.2; classical Horn meet closure; cofinality hypothesis | Qualified Horn/dual-Horn sufficient criteria. |
| Thm. 6.1 binary chain trichotomy | OLD + STD | direct order analysis; beat points | Chain profiles split into $Q=P$, disconnected antitone-threshold, and proper homotopy-neutral cases. |
| Prop. 7.1 unique fitting orientation iff direct collapse | AUDIT + STD | Lemma 4.1; alternating-cycle theorem for perfect matchings | General height-two block criterion for direct relative collapse. |
| Thm. 7.2 seven-element two-bit counterexample | NEW-CERT + direct proof | explicit P, alpha, B; det B=-1; degree obstruction; beat reductions | Integral homology and homotopy equivalence do not force direct collapse for two bits. |
| Prop. 7.3 vertex minimality | COMP | exhaustive C++ checker; Prop. 7.1 | No two-bit height-two counterexample on <=6 vertices. |
| Thm. 7.4 combined sharp two-bit statement | proof + COMP | Thm. 7.2 + Prop. 7.3 | One-bit direct-collapse rigidity is bit-count sharp; seven vertices are minimal by exhaustive certificate. |
| Cor. 7.5 bit-count sharpness | consequence | Thm. 4.2; Thm. 7.2; constant-coordinate padding | One bit is the maximal universal regime; failure persists for every r>=2. |
| Thm. 8.1 cone--whisker realization | AUDIT + STD | elementary thinning analysis; cone/relative LES | One bit with unrestricted height can carry arbitrary finite-poset homotopy type inside a contractible coarse cone. |
| Cor. 8.3 height-three torsion | consequence + STD prior art | Thm. 8.1; 13-point RP2 finite model | Relative Z/2 torsion occurs already in height three with one bit. |

## Primary theorem DAG

```text
one-bit bit-pattern classification
          |
          v
integral reduced graph incidence (Prop. 3.2)
          |
          v
complete integral homology + torsion-freeness (Thm. 3.3)
          |
          +---------------------------+
          |                           |
          v                           v
rooted forest criterion        coefficient independence
          |
          v
nonroot leaf = free deleted edge
          |
          v
direct simplicial collapse
          |
          v
simple-homotopy / homotopy equivalence
```

The reverse implication from homotopy equivalence returns through integral homology,
closing Theorem 4.2.

## Bit-count sharpness DAG

```text
explicit seven-state P, alpha
      |             |              |
      v             v              v
 det(B)=-1   no free deleted edge   P,Q beat-reduce
      |             |              |
      v             v              v
integral       no direct          both endpoint
homology eq.    collapse          complexes contractible
      \             |              /
       \            |             /
        +-----------+------------+
                    |
                    v
     homology + homotopy neutral, not direct-collapse neutral

separate exhaustive checker n<=6
                    |
                    v
        computer-assisted vertex minimality
```

## Height sharpness DAG

```text
arbitrary nonempty finite poset R + minimal z
                    |
         add greatest t and one bit
                    |
        +-----------+------------+
        |                        |
        v                        v
Delta(P)=cone(Delta R)   Delta(Q)=Delta R + whisker
        |                        |
        v                        v
   contractible           collapses to Delta R
        \                        /
         +----------+-----------+
                    |
                    v
relative homology = shifted reduced homology of Delta R
                    |
                    +--> arbitrary refined homotopy types
                    +--> height-three torsion examples
                    +--> acyclic/noncontractible separation
```

## Prior-art boundaries attached to dependencies

The following dependencies are deliberately cited as standard rather than claimed as
new: McCord finite-space realization; Barmak/Quillen-type poset methods; graph
incidence and total unimodularity; Forman-style acyclic matchings (with the manuscript's collapse equivalence proved separately by Lemma 4.1); Bernardi--Klivans
rooted forests and fitting orientations; determinant cancellation among several
fitting orientations; Horn closure systems; and the Ferrers antecedent to the chain
classification.
