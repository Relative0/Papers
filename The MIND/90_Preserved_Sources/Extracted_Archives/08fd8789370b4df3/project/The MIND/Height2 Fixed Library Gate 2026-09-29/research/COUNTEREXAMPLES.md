# Preserved counterexamples and rejected conjectures

Bit words are written in the stated vertex order, not as the usual high-bit-first numeral. Data files use integer masks with bit i at state i.

| Rejected claim | Exact witness / repair |
|---|---|
| Safety is hereditary | Chain x<y<z, r=010; legal q=011, outcome 1 leaves yz with unsafe r=10 |
| An initially unsafe query can never be used | Fork a<b,a<c, r=101; q=011 is safe, outcome 1 leaves antichain bc with safe r=01 |
| Any legal first query preserves feasibility | On the chain Q={010,011}, 010-first identifies; 011-first strands yz |
| Conditioning acts by induced repair-graph subgraph | Chain 010: delete x; descent yz remains, anchor triangle xyz disappears |
| Deactivation can create a new repair cycle | Impossible: retained columns have zero entries in deleted rows, so child kernel embeds in parent kernel |
| Equal deleted-cell counts always imply safety | The six-state example below has B=[[1,1],[0,0]], with equal row/column counts but rank one |
| Independent actual triangle columns suffice | Any descending two-chain has a 1-by-0 matrix: independent columns, unspanned row |
| Complement closure eliminates every penalty | Parity complete-bipartite family has exact gap n/2-1 |
| Safe identification is possible whenever Q separates | Two-chain Q={10}: ordinary depth 1, safe depth infinity |
| Individual safety implies simultaneous safety | v0.5 three-chain tests 010 and 101; each safe, joint refinement disconnected |
| A jointly safe block must have a safe first coordinate | v0.5 five-state compensating example; preserved as a source distinction, not used as one-bit evidence |
| U2 allows only deletion of old quotient comparisons | A coarse equivalent pair split by bit 01 gains strict internal fiber order |
| U4 gives an unconditional direct sum | It gives the standard octahedral exact triangle and long exact sequence; splitting needs hypotheses |
| U6 holds without fine measurability | A support may cut fine cells while retaining every fine label, so profile saturation does not imply coarse measurability |

## Equal counts but singular matrix: six-state explicit witness

Use a four-state fan a<b<c and a<b<d with r(a,b,c,d)=(1,0,1,1). Its only descent is ab and its two triangles both have word 101. Its matrix is [1 1], exhibiting a parallel-edge cycle.

Adjoin the disjoint descending two-chain e<f with r(e,f)=10, which contributes one zero row. In the combined order,

  D={ab,ef}, A={abc,abd}, B=[[1,1],[0,0]].

Deleted-cell counts agree, but rank is one, relative H1 and H2 each have dimension one, and the query is unsafe. This exact example explains why the count shortcut requires a safe-ancestor certificate.

## Source corrections retained

The transferred CLAIM_AUDIT_TABLE.csv already marks v0.5 V5-06 (equality with classical 2-dimension) false and V5-07 (inherited hardness) in need of major repair. Independently check P=Q a two-chain: relative observation dimension is 0, classical Boolean embedding dimension is 1. This is a CONFIRMED EXISTING correction, not a new discovery in this gate.

V5-09 needs its ambient complex to retain unsupported deleted edges: use the full coarse 1-skeleton together with deleted triangles, with retained edges as roots, or explicitly handle unsupported rows. The present one-bit matrix always includes every descent, including unanchored ones.

A1's theorem statement is preserved. One proof sentence in the transferred file says every path uses exactly one redundant query; the alternating construction can instead reach a singleton directly (e.g. the 1 branch of 010). The correct claim, already in the theorem statement, is maximum one per path and necessity on at least one path. No change to A1's conclusions is needed.
