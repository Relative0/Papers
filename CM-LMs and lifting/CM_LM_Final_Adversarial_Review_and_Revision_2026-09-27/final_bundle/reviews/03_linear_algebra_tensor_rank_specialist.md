# Review 3 - Finite linear algebra, tensors, and rank specialist

**Review mode:** simulated specialist reconstruction plus exhaustive finite regression tests where applicable.

## Initial recommendation
Minor revision.

## Main findings
The tensor flattening definitions are sound once row and column variable order is treated as part of the type. The matched-frame XOR-AND product theorem is ordinary F2 matrix composition in the declared intermediate frame. The rank/separability theorem is the standard rank-factorization equivalence translated into XORs of conjunctive row/column factors and is correct in that scope.

The manuscript should say explicitly what happens for the zero matrix/function: rank zero corresponds to zero summands, so the empty XOR must mean zero. The noncontiguous flattening convention would also benefit from one worked example because visual reshaping alone can silently permute variables.

## Revision response
Accepted. The zero-rank/empty-XOR convention is now explicit. A three-variable noncontiguous flattening example with R=(3,1) and C=(2) spells out the assembly map and resulting 4x2 matrix. Empty block conventions and the scalar empty Kronecker product are stated.

## Post-revision recommendation
Pass. No rank, reshape, or matched-product correctness blocker found.
