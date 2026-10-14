# H2: exact repair-graph and boundary restriction

All coefficients below are F2. P is finite, post-T0, of height at most two; r is ONE oriented Boolean test. Write K=Delta(P), L=Delta(P_r).

## Source theorem reconstructed

Let D be all comparable pairs x<y with r(x)=1,r(y)=0. These are all deleted edges, including transitive comparisons, not just Hasse edges. Let A be all three-chains x<y<z with a nonmonotone bit word. The relative chain complex is

  0 -> F2[A] --B--> F2[D] -> 0.

There are no relative vertices and no cells above dimension two. A matrix column has a 1 exactly at each deleted edge that is a face of its triangle.

| Word | Deleted edges | Repair graph edge |
|---|---|---|
| 010 | yz | formal root to yz |
| 101 | xy | formal root to xy |
| 100 | xy,xz | xy to xz |
| 110 | xz,yz | xz to yz |

The other four words 000,001,011,111 retain the triangle. Introduce one formal root for EVERY coarse comparability component, including components with no deleted cells, and one graph vertex per deleted edge. Keep parallel graph edges. Each deleted triangle contributes the graph edge shown in the table. B is precisely its incidence matrix with root rows removed.

The v0.4 theorem equates: homotopy equivalence of L->K; simple homotopy equivalence; collapse using only deleted edge-triangle pairs; F2 homology equivalence; B invertible; and the repair graph a forest with exactly one root per graph component. A 0-by-0 matrix is invertible. Isolated formal roots are harmless. An isolated descent vertex is not.

Proof checkpoint: relative acyclicity is matrix bijectivity. An invertible reduced incidence matrix excludes cycles and rootless components. Conversely, repeatedly remove a nonroot leaf of the rooted forest. Its deleted edge belongs to exactly one remaining triangle; no retained triangle contains a deleted edge, and height excludes higher cofaces. Hence it is a free edge-triangle collapse. This establishes the full equivalence without assuming that homology generally determines homotopy.

## Exact restriction theorem

For T subseteq P define

  D_T={e in D: both vertices of e lie in T},
  A_T={tau in A: all three vertices of tau lie in T}.

Then, in the inherited cell orders,

  B_r(P|T)=B_r(P)[D_T,A_T].

Moreover B_r(P)[D\D_T,A_T]=0: every face of a retained triangle remains in T.

Proof: induced orders retain exactly those chains whose vertices survive. The r-values and simplicial incidence coefficients are unchanged. This proves both assertions.

At graph level the exact operation is:

1. Remove descent vertices whose underlying pairs do not survive.
2. Remove triangle edges whose underlying triples do not survive, EVEN IF both graph endpoints survive.
3. Recompute the coarse components of P|T. Replace an old formal root by one root for each surviving coarse component and attach each surviving anchor to its new component root.
4. Keep the endpoints of surviving dependency edges. Add isolated roots where required; omit empty coarse components.

This is generally not an induced graph subgraph. In the chain 010, deleting the first state removes the anchor triangle while retaining its descent vertex. Triangle provenance is essential; an abstract unlabeled repair graph alone is insufficient input to the restriction operation.

## Exact defects and all safety transitions

Let c0(T) be the number of graph components with no root and let beta(T) be the ordinary graph cycle rank (parallel edges count). No graph component can contain two formal roots: every graph edge stays inside one coarse component, which has only one root. Standard incidence rank gives

  rank B_T = |D_T|-c0(T),
  dim H1(K_T,L_T;F2)=c0(T),
  dim H2(K_T,L_T;F2)=beta(T)=|A_T|-|D_T|+c0(T).

Thus safety is exactly c0(T)=beta(T)=0.

Extension of a vector by zero gives an injection ker(B_T) -> ker(B). Indeed the retained columns have zero entries in every removed row. Consequently restriction CANNOT create a new column dependence or increase relative H2. This is stronger and more precise than a visual analogy about graph deletion.

| Parent -> child | Exact criterion |
|---|---|
| safe -> safe | c0(T)=0; beta(T)=0 is automatic |
| safe -> unsafe | c0(T)>0; the failure is lost anchoring, never a newly created cycle |
| unsafe -> safe | all parent dependencies on retained triangles disappear, and every residual descent component is rooted |
| unsafe -> unsafe | a retained cycle or a rootless component remains |

In particular, if r was safe on P, then

  r safe on P|T iff |D_T|=|A_T|,
  dim H1(K_T,L_T)=|D_T|-|A_T| >= 0,
  H2(K_T,L_T)=0.

This count shortcut is valid only with the prior safety/column-independence certificate. Equal counts alone do not prove safety in general.

## Incremental implementation

Precompute each query's deleted pairs and triples with their vertex provenance. Deleting a state removes only incident pairs/triples. The boundary update is exact row/column selection, never a numerical approximation. Coarse-root recomputation is needed for a literal graph certificate, but not to obtain B_T from its stored columns.

A full one-query test costs O(n^3) to enumerate chains from an explicit order matrix and O(n+|D|+|A|) graph traversal once cells/components are known. After a safe ancestor, maintain deleted-pair and deleted-triple counts; each vertex deletion costs the number of still-active incident stored cells, and count equality decides safety on every descendant. This does not claim an output-independent constant-time dynamic connectivity algorithm.
