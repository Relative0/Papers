# Vtree Adaptation Formalism

## Objects

- `V`: variable set.
- `Pi_f`: canonical semantic prime AND-partition.
- `Pi_K`: carrier partition.
- `T`: rooted binary vtree with leaves `V`.
- `Cl(T)`: leaf sets of all subtrees of `T`.
- `E_T(f)`: finest exact AND-factor partition obtainable by recursively applying the compressed-SDD split criterion along `T`.

## Exact score

Define

`Exposure(T,f) = |E_T(f)|`.

This score is semantic but does not require the ground-truth prime partition: it is computed directly from compressed-SDD cofactor equality / the equivalent CM rank-one cut test.

Secondary exact scores:

- maximum unresolved block size;
- residual variable volume;
- naive residual cut volume;
- number of singleton attributes directly resolved.

## Safe adaptation rule

Changing a vtree may change which factors are exposed but must never delete an exact residual possibility. The hybrid algorithm therefore returns exact factors certified by the current tree and delegates every unresolved block to exact four-corner SAT.

## Carrier handling

Hard constraint: require `B in Cl(T)` for every `B in Pi_K` only if desired. This is safe for correctness but can be harmful for exposure.

Soft carrier score: reward short carrier-block span / common ancestry without requiring exact clades.

Exact compatibility test: `Pi_K union Pi_f` is jointly clade-realizable iff laminar. Since `Pi_f` is unknown in practice, detected semantic factors can be checked incrementally for crossings with carrier blocks.

## Suggested local objective

For a proposed rotation `T -> T'`, use lexicographic objective:

1. maximize newly certified direct factor blocks;
2. minimize residual cut volume;
3. minimize compiled SDD size;
4. optionally reward soft carrier cohesion.

No ground-truth prime partition enters the objective.
