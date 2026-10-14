# Independent combinatorial-topology, graph, and priority review

Date: 2026-09-29. This records an actual independent agent review of `SPECTRAL_SEQUENCE_CONSTRUCTION.md`, `MAX_DEGREE_TWO_CLASSIFICATION.md`, and the concrete C4 proof. It is not an external peer review or a simulated panel consensus. The reviewer also independently derived the star-pair reduction and the seven-state star's integral link-table proof.

## 1. Relative complex and indexing attack

The filtration correctly lives on C_*(K,U), not C_*(K,L). The missing-first orientation gives v=(-1)^p partial, h the signed core deletion, and total degree m=p+q. The cone shift is n=m-1. The two-column formula C(K,U)=Cone(h)[2] and the displayed kernel/cokernel short exact sequence have consistent degrees. The empty augmented degree is retained. No correction required.

The statement that the original boundary changes core size by at most one does not imply vanishing higher differentials. The explicit zigzag hx=-vy and d2[x]=[hy] correctly prevents that error. Finite filtration gives convergence without extra connectivity assumptions. The integral extension warning is essential and present.

## 2. Graph and transitivity attack

The neighborhood inclusions have the correct directions: p<p' forces N(p') subset N(p), while z<z' forces N(z) subset N(z'). Under degree two, a four-core is exactly a C4 component with both same-colour pairs comparable. The no-four-core hypothesis therefore supports the stated two-column theorem.

For a longer cycle, all same-colour vertices have degree two with distinct neighborhoods, ruling out comparable same-colour common-neighbor pairs. Such cycles have no three-cores and the extended edge-link direct sum is valid. On paths, three-cores are confined to the end triples. For paths of at least four edges those triples use disjoint edge sets; for a three-edge path they can share the middle edge. The claimed block decompositions follow because surviving boundaries only delete missing vertices and stay in the same listed block. The links must still be taken in all of Q, as the file explicitly requires.

Care was taken not to confuse P4 (three-edge path, Ferrers) with the smallest connected non-Ferrers chordal-bipartite example P5. If disconnected examples are allowed, 2K2 is already non-Ferrers.

## 3. C4 and coefficient attack

For a<b<x<y, the four-core deletion signs (-,+,-,+), triple-to-edge signs, and hk=0 are consistent. The sole possible higher differential is from column four to column two. The eight-state example's chosen paths have the stated signed boundaries. Its ay-component traverses the available-link cycle once, providing an integral unit d2, not merely a mod-two cancellation.

The files correctly reject unrestricted E2 collapse for maximum degree two, Ferrers, and chordal-bipartite graphs. They also correctly retain E3 collapse and a necessary-and-sufficient acyclicity criterion using the middle E2 term and d2 isomorphisms. This is a criterion for zero homology, not a direct-sum description of nonzero integral groups.

## 4. Torsion origin attack

The all-exclusive star profile has Lambda_S equal to an isolated available point and a principal-ideal cone. Canonical component-difference generators turn d1 into minus the ordinary simplicial boundary of Delta R. A degreewise sign change gives the usual chain complex. Therefore torsion of Delta R arises in d1 homology although every available link is torsion-free. Taking the RP2 face poset also makes all coarse edge links circles. This really distinguishes interaction-created torsion from the frozen matching theorem's inherited torsion.

The verification scope is stated accurately: 181 available links, 31 coarse edge links, and the reduced E1 complex were checked by SNF; the entire doubled 32-state relative pair was not directly reduced. The proof makes that larger reduction unnecessary for correctness. No torsion-minimality claim is justified.

## 5. Strongest priority objection

The available links are exactly the obstruction complexes of Chacholski--Jin--Scolamiero--Tombari, and the collapse bounds and chain-cone recursion are standard filtered-complex algebra. This overlap is literal, not just philosophical. Calling the resulting machinery a new general spectral sequence, obstruction theory, or theory of vertex deletion would be unsupported.

Bjorner--Wachs--Welker's wedge/fiber statements use their specified connectivity or null-attachment hypotheses. Here the nonzero maps are retained and can create torsion or higher differentials, so the project supplies a specialized explicit calculation beyond a sufficient contractibility test. That does not make it globally stronger than their theory.

The genuine candidate contribution is the precise Boolean product-poset realization, the transitivity restrictions on chain-supported cores, and the resulting positive/negative classification and certificates. The all-exclusive star realization is an elementary but useful exact family. Neither targeted searches nor an unlocated identical formula establish publication priority. No standalone claim of a major new general topological theorem is warranted.

## 6. Verdict

No unresolved correctness defect was found in the reviewed spectral-sequence and maximum-degree-two statements. The no-four-core theorem is exact with its extension qualifications; the general degree-two case needs its documented d2; Ferrers/chordal E2 assertions are false. The findings warrant the gate's conservative Level B classification as a project-specific exact result, while novelty remains unconfirmed. The original manuscript baseline should remain frozen until a separate merge/editorial decision; this review itself does not authorize or perform a merge.
