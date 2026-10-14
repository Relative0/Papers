# Signed integral witnesses and what they prove

This supplement indexes the readable arguments in v0.5 Section 9.1 and the archived integer certificates. It is not a claim of global minimality. In the following, an available link is `Λ_S=lk_K(S)[V(L)]`, with `K=Δ(Q×{0<1})` and `L=ΔQ^ψ`. The signed horizontal differential deletes one missing-core vertex; the vertical differential is the available-link boundary with the missing-first sign. Cone degree is relative total degree minus one.

## Seven-state star: primitive `d²: Z→Z²`

Take the poset with covers

`0<1, 0<2, 1<3, 2<3, 2<5, 3<4, 3<6, 5<6`

and availability profile `(1,2,0,0,2,2,0)`, where `1` means one-only, `0` zero-only, and `2` split. Its exclusive graph is `K1,3`. The four-core available link is the two vertices `{0_1,2_0}`. The three triple cores, indexed by their upper missing states, admit paths from `2_0` to `0_1`:

| Core | Path |
|---|---|
| `023` | `A: 2_0—4_1—0_1` |
| `026` | `B: 2_0—5_1—0_1` |
| `036` | `C: 2_0—3_0—1_0—1_1—0_1` |

Each triple link is contractible. The `02` edge link is the square with bipartition `{0_1,2_0}` and `{4_1,5_1}`. The `03` edge link is a cone with apex `4_1`. The `06` link has maximal faces `[0_1,1_1]`, `[0_1,5_1]`, `[1_0,1_1]`, `[1_0,3_0,6_0]`, `[2_0,3_0,6_0]`, `[2_0,5_0,5_1]`, and `[2_0,5_0,6_0]`; collapsing its triangle ears leaves the cycle `0_1—1_1—1_0—3_0—2_0—5_1—0_1`.

Orient the paths from `2_0` to `0_1`. For the four-core zero-cycle, the triple corrections have signs `(-,+,-)` in `(023,026,036)` order. Their horizontal boundary gives `B−A` in the `02` link, `A−C` in the `03` link, and `C−B` in the `06` link. `B−A` traverses the square exactly once. Therefore the integral `d²:Z→Z²` has a unit coordinate and is primitive. The first-page groups are `Z²` at `(2,1)` and `Z` at `(4,0)`; they are unchanged on `E²`. The remaining cone group is `H₂=Z`.

This disproves unconditional `E²` collapse for forests, Ferrers graphs, and chordal-bipartite graphs. It says nothing about global minimality or about the positive two-column theorem.

## Eight-state four-cycle: unit `d²: Z→Z`

Use `Q=A₂⊕R⊕A₂` with bottom `{a,a'}`, middle `{v,b,w,x}` satisfying `v<x`, `b<w`, `b<x`, and top `{y,y'}`. Make `a,b` one-only and `x,y` zero-only, splitting the others. The exclusive core is `a<b<x<y`. The four-core link is `{b_1,x_0}`. Triple links `abx` and `bxy` are cones; the two path links are

`x_0—y_0—w_0—w_1—b_1` and `x_0—v_0—v_1—a_1—b_1`.

Edge links `ax`, `by`, and `bx` are cones. The remaining `ay` link has maximal simplices `[a_1,b_1,w_1]`, `[v_0,x_0,y_0]`, `[a_1,v_1]`, `[v_0,v_1]`, `[w_0,w_1]`, `[w_0,y_0]`; collapse of the two triangle ears leaves a circle.

For triple order `(abx,aby,axy,bxy)`, the signed core-deletion map from the four-core is `k=(-,+,-,+)`. With both relevant paths oriented from `x_0` to `b_1`, their `ay` edge-link component is the first path minus the second and traverses the circle once. Other edge-link components lie in contractible links. Thus `d²:Z→Z` is a unit and `E³=0`, proving the degree-two `E³` page bound sharp.

## Archived certificates and limits

The original signed-chain JSON certificates and verifiers live under `../Interaction Core Gate 2026-09-29/`:

- `star_d2_integral_certificate.json` and `c4_d2_integral_certificate.json` record the chosen chains, page groups, and integer unit reductions.
- `verify_d2_certificate.py` regenerates those certificates; the convergence run produced copies in `../Manuscript Convergence 2026-09-29/build/certificates/` without modifying the earlier files.
- `../Independent Expert Review/independent_checks.py` and `independent_results.json` provide an independently coded selected-case check, including direct relative pairs and the signed paths. The independent report describes the algorithm's limits.

The 32-state projective-plane example is a different phenomenon: the `d¹` interaction creates `Z/2` in cone degree two while each available link has free reduced homology. Its verifier uses the reduced interaction model and local links rather than a direct Smith reduction of the full doubled pair. The three-chain profile `(1,0,0)` remains the basic two-column counterexample to summing coarse edge links outside matching.
