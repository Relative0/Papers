# Paper B - independent mathematical checks

## Finite Walsh checks

An independent standard-library verifier was used to check the centered Walsh claims.

For `n=1,2,3,4`:

- Gram identity: `phi(x).phi(y)=N-1` if `x=y`, `-1` otherwise.
- `sum_x phi(x)=0`.
- rank of the feature/evaluation map is `N-1`.
- constructive sign witness works.

All nonconstant sign labelings were exhaustively checked for:

- `n=1`: 2 labelings;
- `n=2`: 14 labelings;
- `n=3`: 254 labelings;
- `n=4`: 65,534 labelings.

Result: **PASS** for the realization/count statements.

## Adjacency graph count check

For `N=2,4,8,16`, the induced `N`-cube graph after deleting the two constant vertices has:

- `N=2`: 2 vertices, 0 induced-cube edges;
- `N=4`: 14 vertices, 24 edges;
- `N=8`: 254 vertices, 1008 edges;
- `N=16`: 65,534 vertices, 524,256 edges.

These match `N*2^(N-1)-2N`.

## Unary geometric edge case

At `n=1`, the two score functions are `c` and `-c`. Their zero hyperplanes coincide at `{0}`. The two nonconstant operator regions are the rays `c>0` and `c<0`.

- ordinary geometric closures share the codimension-one boundary `{0}`;
- both indexed scores vanish there;
- the two truth tables differ in two entries;
- therefore this is not a *regular one-score facet crossing*.

This is why the manuscript should either restrict the ordinary chamber-adjacency claim to `n>=2` or explicitly define a special regular-adjacency graph.

## Linear-algebra simplification

Let `H'` be the Walsh-Hadamard evaluation matrix with the constant column deleted. Then:

- columns of `H'` are orthogonal;
- `col(H') = 1^perp` in `R^N`;
- `c -> H'c` is an isomorphism from coefficient space to the zero-sum score subspace.

Hence the centered Walsh atlas is linearly equivalent to the coordinate-hyperplane arrangement restricted to `sum_x s_x=0`. This makes the classical Cover/Schlaefli/oriented-matroid structure explicit.
