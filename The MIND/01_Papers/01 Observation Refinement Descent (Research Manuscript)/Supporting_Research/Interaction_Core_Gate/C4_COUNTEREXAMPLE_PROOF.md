# Eight-state C4 counterexample to E2 collapse

## The exact construction

Let `A={a,a'}` and `B={y,y'}` be two-element antichains. Let `R={v,b,w,x}` have exactly the strict relations

`v<x`, `b<w`, `b<x`.

Set `Q=A ordinal-sum R ordinal-sum B`. Make `a,b` 1-only, `x,y` 0-only, and all other states split. The exclusive graph is exactly `K_(2,2)`, with edges `ax,ay,bx,by`; both colour pairs are comparable, and the missing four-core is

`S=(a0<b0<x1<y1)`.

The natural labels used in `c4_search.json` are

`(a,a',v,b,w,x,y,y')=(0,1,2,3,4,5,6,7)`.

Thus the availability vector is `[1,2,2,1,2,0,0,2]`, and the full strict relations are

* `0<2,3,4,5,6,7`;
* `1<2,3,4,5,6,7`;
* `2<5,6,7`;
* `3<4,5,6,7`;
* `4<6,7`;
* `5<6,7`.

This graph has maximum degree two and is simultaneously Ferrers and chordal bipartite. Consequently the example refutes E2-collapse claims for each of those entire classes.

## All available links

Subscripts on coarse letters denote product bits. The link of the four-core is exactly the two-point complex `{b1,x0}`, so its reduced `H_0` is `Z`.

The four triple links are contractible:

| Core | Available-link description |
|---|---|
| `abx` | Two edges from `b1,x0` to common maximum `y'1` |
| `aby` | Path `b1 -- w1 -- w0 -- y0 -- x0` |
| `axy` | Path `b1 -- a1 -- v1 -- v0 -- x0` |
| `bxy` | Two edges from common minimum `a'0` to `b1,x0` |

Three edge links are contractible. The `ax` link is a cone with maximum `y'1`; the `by` link is a cone with minimum `a'0`; the `bx` link is a cone (indeed it has both these vertices).

The `ay` link has vertices

`a1,b1,v0,v1,w0,w1,x0,y0`.

Its maximal simplices are the two triangles `[a1,b1,w1]`, `[v0,x0,y0]`, and the four edges `[a1,v1]`, `[v0,v1]`, `[w0,w1]`, `[w0,y0]`. Collapsing the two triangle ears gives a six-edge cycle. Hence this link is homotopy equivalent to `S^1` and has reduced integral `H_1=Z` only.

Therefore the integral first page is exactly

`E^1_(4,0)=Z`, `E^1_(2,1)=Z`,

with every other group zero. Here the second index is available-link degree `q`, so the relative total degree is `r+q`. There is no nonzero `d^1`, and `E^2=E^1`.

## The signed d2 is a unit

Orient missing cores first and available simplices second, as in `SPECTRAL_SEQUENCE_CONSTRUCTION.md`. Let

`c=[b1]-[x0]`

generate the reduced `H_0` of the four-core link. For each triple link choose an oriented path `P_t` with boundary `c`:

`P_abx=[x0,y'1]-[b1,y'1]`,

`P_aby=[x0,y0]-[w0,y0]+[w0,w1]-[b1,w1]`,

`P_axy=-[v0,x0]+[v0,v1]-[a1,v1]+[a1,b1]`,

`P_bxy=-[a'0,x0]+[a'0,b1]`.

In the triple ordering `(abx,aby,axy,bxy)`, deletion from the four-core has signs `(-,+,-,+)`. Thus

`b=(-P_abx, P_aby, -P_axy, P_bxy)`

satisfies `d_link b=k c`, and the `d^2` zigzag is represented by `h b`. Its `ay` component is

`P_axy-P_aby`.

This traverses the loop of the `ay` link exactly once. The other edge components are cycles in contractible links. It follows that

`d^2:E^2_(4,0) -> E^2_(2,1)`

is multiplication by `1` up to the choice of generator orientation. This is an integral statement and remains a nonzero unit map over every nonzero coefficient ring.

Consequently `E^3=0`, and the reduced mapping-cone homology is zero in every degree. The bound `E^3=E^infinity` for maximum-degree-two exclusive graphs is sharp. In particular, an acyclic cone can have two nonzero E2 groups which cancel only at d2.

## Independent exact computations and scope

`verify_c4_search.py --trials 20000` sampled 4,000 poset/profile pairs for each `n=6,7,8,9,10`, with seed `2026092917`. It encountered 15,655 distinct labelled poset/profile pairs, five nonzero-d2 cases, and six cases with a nonzero fourth column on E2. This is random finite evidence, not a uniform or isomorphism-complete enumeration.

The selected eight-state example has 108 mixed relative cells. The direct integral Smith-normal-form computations give zero homology both for `C_*(K,U)` and for `C_*(K,L)`. Every available link was also checked separately over `Z`.

`python verify_c4_search.py --audit-existing` checks each path above against the actual link poset, checks its signed boundary, and forms the target cycle. It attaches an abstract 2-cell along that cycle and uses integral SNF to verify that only ordinary `H_0=Z` remains. Together with the separately computed `H_1=Z`, this certifies that the target is a primitive generator, not a nonunit multiple.

The same audit checks all 15 proper induced restrictions retaining the four exclusive vertices; none has nonzero d2. Deleting an exclusive vertex leaves at most three missing vertices and cannot retain this d2. Thus this witness is minimal under induced-subposet restriction with inherited availability. **It is not claimed globally minimal among all posets or all C4 examples.**

