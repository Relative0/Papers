# Results

All core state arithmetic in this file is over

`A = F2[C4] ~= F2[u]/(u^4)`

with XOR addition and CM cyclic convolution `star`. Integers appear only as finite-set counts or compact bit encodings.

## R1. Re-verification of the known intrinsic structures

**[REGRESSION]** The requested baseline identities were re-run:

- `C^2 = I` for the lower shear `C=[[E0,0],[E0,E0]]`, and `C|0>=(E0,E0)`;
- the regular phase operator satisfies `P^4=I` and `P^T=P^-1`;
- `H_star^2 = I`;
- `H_star^dagger H_star = I`;
- `H_star|0> = E0|0> XOR delta|1>` and `H_star|1> = delta|0> XOR E0|1>`;
- for `chi=(E0,E2)`, `X chi = E2 star chi`;
- `B_star=CNOT(H_star tensor I)` is reversible, with inverse action checked on every one of the `16^4=65,536` two-bit coefficient states;
- all four computational-basis outputs of `B_star` have exactly two nonzero CM branches and Smith class `(0,2)`, hence are CM-nonseparable.

Raw/regression record: `logs/run_summary.json` and `tests/test_cm_modal.py`.

---

# 1. Modal Bell investigation

## R2. Measurement bases as reversible effect bases

**[THEOREM / PROVED]** Let a local two-outcome basis be the two rows of a matrix in `GL2(A)`. For support-only readout, independently multiplying either row by a unit does not change its possible/impossible outcomes, because for a unit `g`, `g a=0` iff `a=0`. Outcome swap also does not change the unordered basis.

**[THEOREM / PROVED + EXHAUSTIVE]** There are exactly **192 unordered reversible projective local bases**.

Proof/count:

1. `A` is local with residue field `F2` and maximal ideal `(u)` of size 8.
2. Reduction modulo `(u)` gives a surjection `GL2(A) -> GL2(F2)`.
3. The kernel has `8^4` elements, so
   `|GL2(A)| = |GL2(F2)| 8^4 = 6*4096 = 24,576`.
4. Independent row-unit rescaling has size `8^2=64`; it acts freely on invertible bases.
5. Outcome swap has size 2 and also acts freely.
6. `24,576/(64*2)=192`.

The exhaustive enumeration independently returns 192 canonical bases in `data/measurement_bases_192.csv`.

**[THEOREM / PROVED + EXHAUSTIVE]** Exactly **4** unordered projective bases are represented by intrinsic-unitary matrices. There are 512 intrinsic-unitary `2x2` matrices and every ring unit `g` obeys `bar(g) star g=E0`, so row-unit rescaling preserves unitarity. Hence `512/(64*2)=4`.

Canonical representatives, using integer bit encodings in the CSV, are:

```text
{(0,E0),       (E0,0)}
{(E0,delta),   (delta,E0)}
{(E0,E1^E3),   (delta,E1)}
{(E0,Omega),   (Omega,E0)}
```

The third representative is projective; its displayed rows are a canonical unit-rescaled form, not a claim that this exact row ordering is `H_star`.

## R3. Explicit strong modal Bell contradiction

Take the support Bell state

`Phi = E0|00> XOR E0|11>`.

Use the following three reversible local bases, entirely inside the embedded `F2` subtheory:

```text
Z = {(E0,0),  (0,E0)}
X = {(E0,E0), (E0,0)}
Y = {(0,E0),  (E0,E0)}
```

**[EXHAUSTIVE]** The possible/impossible joint-outcome tables, in outcome order `00,01,10,11`, are:

| Alice / Bob | Z | X | Y |
| --- | --- | --- | --- |
| **Z** | `1001` | `1110` | `0111` |
| **X** | `1110` | `0111` | `1001` |
| **Y** | `0111` | `1001` | `1110` |

Raw table: `data/modal_bell_mqt_tables.csv`.

**[THEOREM / PROVED]** These possibilities admit no deterministic local hidden-variable assignment.

Let Alice's predetermined bits be `z,x,y` for settings `Z,X,Y`. From the equal-only contexts:

- `ZZ`: `b_Z = z`;
- `XY`: `b_Y = x`;
- `YX`: `b_X = y`.

Now use the three contexts that forbid outcome `11`:

- `ZX` gives `NOT(z AND y)`;
- `XZ` gives `NOT(x AND z)`;
- `YY` gives `NOT(y AND x)`.

And the three contexts that forbid outcome `00`:

- `ZY` gives `z OR x`;
- `XX` gives `x OR y`;
- `YZ` gives `y OR z`.

Therefore each pair among `z,x,y` must contain exactly one `1`: `z != x`, `x != y`, and `y != z`. Three Boolean bits cannot be pairwise unequal. Contradiction.

**[EXHAUSTIVE]** All `2^6=64` deterministic Alice/Bob global assignments were checked; zero are compatible.

### Interpretation boundary

**[LITERATURE]** This witness is not evidence for a new nilpotent-generated Bell theorem. The settings and state coefficients lie in the embedded `F2` modal subtheory, so the result is best read as an explicit embedding/reproduction of finite-field modal nonlocality inside the CM coefficient ring.

## R4. Complete modal Bell/contextuality classification by Smith class

Let the canonical local-equivalence representatives be

`D_(a,b) = diag(u^a,u^b)`, with `0 <= a <= b <= 4` and `u^4=0`.

Use the **complete 192-basis reversible projective family** from R2 on each party, and use the standard possibilistic hierarchy:

- **strong contextuality:** no deterministic global assignment is compatible with all possible/impossible tables;
- **logical contextuality but not strong:** at least one possible local section has no global extension, but at least one global assignment exists;
- **relationally local:** every possible local section extends to a compatible deterministic global assignment, so the support is exactly a union of global sections.

The zero vector `(4,4)` is excluded from the empirical-model classification because every context has empty support.

**[THEOREM / PROVED + EXHAUSTIVE VERIFICATION]** The 15 Smith classes split exactly as follows:

| Smith class | Separability | Complete 192-basis support classification | Possible sections | Unextendable possible sections |
| --- | --- | --- | ---: | ---: |
| `(0,0)` | nonseparable | **strong** | 141,312 | all |
| `(0,1)` | nonseparable | **logical, not strong** | 139,264 | 73,728 |
| `(0,2)` | nonseparable | **logical, not strong** | 137,216 | 36,864 |
| `(0,3)` | nonseparable | **logical, not strong** | 135,168 | 15,360 |
| `(0,4)` | separable | relationally local | 131,072 | 0 |
| `(1,1)` | nonseparable | **strong** | 135,168 | all |
| `(1,2)` | nonseparable | **logical, not strong** | 131,072 | 65,536 |
| `(1,3)` | nonseparable | **logical, not strong** | 126,976 | 28,672 |
| `(1,4)` | separable | relationally local | 118,784 | 0 |
| `(2,2)` | nonseparable | **strong** | 122,880 | all |
| `(2,3)` | nonseparable | **logical, not strong** | 114,688 | 49,152 |
| `(2,4)` | separable | relationally local | 98,304 | 0 |
| `(3,3)` | nonseparable | **strong** | 98,304 | all |
| `(3,4)` | separable | relationally local | 65,536 | 0 |
| `(4,4)` | zero | degenerate / excluded | 0 | 0 |

So among the ten nonseparable classes, the four equal-valuation classes `(a,a)`, `a<4`, are strongly contextual, while the six strictly off-diagonal classes `(a,b)`, `a<b<4`, are logically contextual but not strongly contextual. Every nonzero separable class `(a,4)` is exactly relationally local.

Because the classification is constant on local `GL2(A) x GL2(A)` orbits, this class theorem classifies **every one of the 65,536 two-party coefficient states**: **26,214** states are strongly contextual, **34,056** are logical-not-strong, **5,265** nonzero states are relationally local, and the remaining one state is the zero vector. Equivalently, **every one of the 60,270 CM-nonseparable two-party states is possibilistically contextual under the complete reversible-basis family**, whereas every nonzero CM-separable state is possibilistically local.

Raw exhaustive result: `data/bell_contextuality_by_smith_class.csv`.

### Proof of invariance under local equivalence

If `M' = U M V^T` with `U,V in GL2(A)`, then for local effect rows `e,f`,

`e M' f^T = (eU) M (fV)^T`.

Right multiplication by `U` or `V` bijects the complete reversible basis family. Unit rescaling and outcome permutation only relabel support events. Therefore strong/logical/relational support status is invariant on each Smith orbit. It is enough to analyze `D_(a,b)`.

### Equal-valuation nonseparable classes are strongly contextual

For `D_(a,a)=u^a I`, `a<4`, use the three embedded-`F2` bases `Z,X,Y` from R3. Every amplitude in the support-Bell tables is `u^a` times either `0` or `E0`. Since `u^a != 0`, the zero/nonzero pattern is exactly the R3 strong-Bell table. Hence every `(a,a)`, `a<4`, is strongly contextual.

### Every off-diagonal nonseparable class has an explicit Hardy/logical witness

Let `a<b<4`, put `p=u^a`, `q=u^b`, and `c=u^(b-a)`, so `q=p c` with nonzero nonunit `c`. Use

```text
R   = {(0,E0), (E0,0)}
X   = {(E0,0), (E0,E0)}
D_c = {(E0,0), (c,E0)}
```

All three are reversible local bases. For `diag(p,q)`, the support tables in outcome order `00,01,10,11` are

```text
R / R   : 1001
R / X   : 0111
D_c / X : 1110
D_c / R : 0111
```

The event `(R_A=0,R_B=0)` is possible. If a deterministic global assignment extended it, then:

1. `R_A=0` and the forbidden `00` in `R/X` force `X_B=1`;
2. `X_B=1` and the forbidden `11` in `D_c/X` force `D_A=0`;
3. `D_A=0` and the forbidden `00` in `D_c/R` force `R_B=1`;
4. this contradicts the assumed `R_B=0`.

Thus a possible event has no global extension: every off-diagonal class is logically contextual.

Raw witnesses: `data/offdiagonal_hardy_witnesses.json`.

### Off-diagonal classes are nevertheless not strongly contextual

For any reversible local basis, at least one row has a **unit first coordinate**; otherwise the first column lies entirely in the maximal ideal and the determinant cannot be a unit. Choose such an outcome for every Alice basis and every Bob basis.

For `D_(a,b)=p diag(1,c)`, the amplitude of any pair of chosen effects `(x,y)` and `(s,t)` is

`p (x s XOR c y t)`.

Here `xs` is a unit while `cyt` is a nonunit. In a local ring, unit XOR nonunit is a unit. Multiplication by the nonzero `p=u^a` therefore remains nonzero. These chosen outcomes define a deterministic global section compatible with **all 192 x 192 contexts**. Hence the off-diagonal classes are not strongly contextual.

### Nonzero separable classes are exactly relationally local

For `D_(a,4)=diag(u^a,0)`, a joint effect `(x,y),(s,t)` is possible exactly when `u^a x s != 0`. Given any possible section at one context, retain those selected outcomes and, at every other local basis, choose a row with unit first coordinate. The original possible condition implies the mixed specified/unit contexts remain nonzero, while all unit/unit contexts are nonzero. Thus every possible section has a global extension.

This proves exact possibilistic locality for all nonzero separable classes.

### Corollary: the natural `B_star` Bell-like state is logically contextual, not strongly contextual

`B_star|00> = E0|00> XOR delta|11>` has Smith class `(0,2)`. Across all 192 reversible projective bases per party, the exact support computation has:

- 10,240 impossible-pair 2-SAT clauses;
- 137,216 possible local sections;
- 100,352 extendable possible sections;
- **36,864 possible sections with no global extension**;
- at least one compatible deterministic global assignment.

The first uncovered canonical event is basis `0` / basis `0`, outcome `00`. An explicit three-setting Hardy witness uses basis IDs `R=0`, `X=16`, `D_delta=28` in `data/measurement_bases_192.csv`.

Thus the earlier “global section exists” observation was only a **negative strong-contextuality result**. The stronger exact-support check reverses the tentative locality interpretation: `Beta_delta` is **logically nonlocal/contextual**, just not strongly so.

The four intrinsic-unitary projective bases remain too small to reveal this: under that restricted family `Beta_delta` has compatible globals and every possible section is covered.

Raw outputs: `data/bell_bstar_complete_reversible_basis_sat.json`, `data/bell_contextuality_by_smith_class.csv`, and `data/offdiagonal_hardy_witnesses.json`.

---

# 2. Pure-CM teleportation

## R5. Universal exact teleportation exists for all 256 one-bit ring states

Let

```text
I = [[E0,0],
     [0,E0]]

X = [[0,E0],
     [E0,0]]

K = [[E0,E0],
     [0,E0]]
```

and let the shared resource be the support Bell state

`R = E0|00> XOR E0|11> = vec(I)`.

Define four nonseparable basis states

`beta_M = (M tensor I) R = vec(M)` for `M in {I,X,K,KX}`.

Their coefficient matrices all have unit determinant, so they lie in Smith class `(0,0)` and are CM-nonseparable.

Let `Q` be the `4x4` Boolean/CM matrix whose columns are those four `beta_M` states:

```text
Q =
[1 0 1 1]
[0 1 1 1]
[0 1 0 1]
[1 0 1 0]
```

where every displayed `1` means `E0`. Its inverse is

```text
Q^-1 =
[0 1 1 1]
[1 0 1 1]
[0 1 1 0]
[1 0 0 1].
```

All entries therefore remain in the pure Boolean subring `{0,E0}`.

Apply `Q^-1` to the sender's unknown input and the sender's half of `R`, then read the two-bit analyzer outcome modally. The receiver's conditional one-bit maps are:

| Outcome | Receiver map `T_m` | Correction `T_m^-1` |
| --- | --- | --- |
| `00` | `XK = [[0,1],[1,1]]` | `KX = [[1,1],[1,0]]` |
| `01` | `K  = [[1,1],[0,1]]` | `K` |
| `10` | `X  = [[0,1],[1,0]]` | `X` |
| `11` | `I` | `I` |

Again, each `1` means `E0`.

**[THEOREM / PROVED]** Every `T_m` is invertible over `A`; therefore for arbitrary

`psi=A|0> XOR B|1>`

we have

`T_m^-1 T_m psi = psi`

for every modal analyzer outcome `m`. No global CM unit quotient is needed.

**[EXHAUSTIVE]** All `16^2=256` choices of `(A,B)` and all four outcome branches were evaluated: **1024/1024 exact recoveries**. Every branch is nonzero for every nonzero input because every `T_m` is invertible.

Raw evidence:

- `data/teleportation_protocol.json`
- `data/teleportation_all_256_states_x4_outcomes.csv`

### Measurement assumption

This is a modal teleportation protocol conditional on the explicit measurement contract in `DEFINITIONS_AND_NOTATION.md`: after the reversible analyzer, a nonzero computational branch is a possible classical outcome. No probabilities are assigned. The original CM/LM paper does not itself specify this ring-valued post-measurement protocol.

### Literature boundary

**[LITERATURE]** Finite-field modal/discrete quantum theories already have teleportation analogues. The result here is therefore not “teleportation from Boolean logic for the first time.” What is established specifically is exact scalar extension to all 256 states over the CM ring, together with a nilpotent-resource obstruction below.

## R6. Nonseparability alone is insufficient: `B_star` resource obstruction

Take the natural `B_star` resource

`Beta_delta = E0|00> XOR delta|11>`

and use `B_star^-1` as the corresponding analyzer. The four conditional receiver maps are

```text
T00 = [[E0,0],     [0,0]]
T01 = [[0,delta],  [delta,0]]
T10 = [[delta,0],  [0,delta]]
T11 = [[0,E0],     [0,0]]
```

**[EXHAUSTIVE]** All four determinants are zero.

**[THEOREM / PROVED]** No one of these branch maps admits an `A`-linear universal correction. If a square matrix `T` had a left inverse `C` with `CT=I`, then taking determinants over the commutative ring would give `det(C)det(T)=1`, forcing `det(T)` to be a unit. Here `det(T)=0` in every branch.

Thus this CM-nonseparable resource is too degenerate for the tested universal teleportation architecture. The obstruction is precisely connected to the nilpotent coefficient `delta` and zero-divisor information loss.

Raw evidence: `data/bstar_teleportation_failure.json`.

## R6b. Complete teleportation-resource theorem

Let an arbitrary resource state have coefficient matrix `M`, and let `W in GL4(A)` be any reversible analyzer. Reshape analyzer outcome row `m` into a `2x2` matrix `R_m`. Direct contraction gives the conditional receiver map

`T_m = M^T R_m^T`,

so

`det(T_m) = det(M) star det(R_m)`.

**[THEOREM / PROVED]** A two-party CM resource supports deterministic universal exact one-bit teleportation with a reversible four-outcome analyzer and outcome-conditioned `A`-linear corrections **iff `det(M)` is a unit**, equivalently **iff the resource lies in Smith class `(0,0)`**.

Necessity follows because an exact correction `C_m T_m=I` forces `det(T_m)` to be a unit, which in turn forces `det(M)` to be a unit. This actually rules out even one universally correctable analyzer branch for every singular resource. Sufficiency follows from the existing pure-Boolean analyzer `Q^-1`: all four reshaped analyzer rows have determinant `E0`, hence for every invertible `M` all four branch maps are invertible and can be corrected by `T_m^-1`.

**[EXHAUSTIVE REGRESSION]** All 65,536 resource matrices were checked with that fixed analyzer. Exactly 24,576 succeed on all four branches, exactly matching the 24,576 unit-determinant matrices and exactly matching Smith class `(0,0)`. Every other Smith class contains zero universal exact teleportation resources.

This completes the previously open resource classification: among the ten nonseparable Smith classes, only `(0,0)` supports universal exact teleportation in the stated architecture. In particular, the strongly contextual classes `(1,1)`, `(2,2)`, and `(3,3)` still fail, so even **strong contextuality is not sufficient** for this teleportation task.

Full proof and scope: `TELEPORTATION_RESOURCE_THEOREM.md`. Raw evidence:

- `data/teleportation_resource_theorem.json`
- `data/teleportation_resource_inventory_65536.csv`
- `data/teleportation_resource_by_smith_class.csv`

## R6c. Singular-resource hierarchy below universal exact teleportation

The complete failure of singular resources for arbitrary exact input does **not** mean that all singular classes are operationally equivalent. The follow-up analysis in `SINGULAR_TELEPORTATION_HIERARCHY.md` separates exact restricted-state transfer, fixed quotient transfer, postselection, and ancilla/multicopy activation.

For the canonical Smith representative `D_(a,b)=diag(u^a,u^b)`, the largest common exactly recoverable state family has:

- 256 states for `(0,0)`;
- 16 states, one free `A`-line, for every `(0,b)` with `b>0`;
- only the zero state when `a>0`.

An explicit reversible four-outcome analyzer recovers every `x|0>` on all four branches for every `(0,b)`. The 16-state bound is proved from residue-field rank and the socle structure of finite chain-ring submodules. If `a>0`, every corrected branch map is zero modulo `(u)`, which rules out any nonzero fixed state.

A singular resource also retains a canonical quotient

`Q_(a,b)=A/(u^(4-a)) + A/(u^(4-b))`,

with `2^(8-a-b)` equivalence classes. Requiring every successful outcome to correct to the **same** target `D_(a,b) psi` gives a second complete hierarchy: equal-valuation classes `a=b<4` allow all four outcome rows; off-diagonal nonzero classes `a<b<4` allow at most two; rank-one classes `b=4` allow at most three. All bounds are attained.

This makes `(0,2)` particularly clear. It cannot universally teleport `A|0> XOR B|1>`, but it can exactly transfer the free line `A|0>` and its canonical quotient is `A + A/(u^2)`, containing 64 algebraic equivalence classes. At most two of four analyzer outcome labels can be corrected to that same fixed quotient target.

**[THEOREM / PROVED]** Postselection does not rescue universal exact full-state teleportation: every branch determinant still contains the nonunit resource determinant, so every singular class has zero universally exact success branches. Because the modal model has no probability measure, this is a possible/impossible statement rather than a numerical success probability.

**[THEOREM / PROVED]** Product local ancillas and any finite number of copies of a singular resource do not activate universal exact teleportation. Reduction modulo `(u)` sends every singular `2x2` resource to an `F2` matrix of rank at most one; tensor powers retain rank at most one. Any branch map therefore has residue rank at most one and cannot possess an `A`-linear left inverse onto `A^2`.

Raw evidence:

- `SINGULAR_TELEPORTATION_HIERARCHY.md`
- `data/singular_teleportation_hierarchy_by_smith_class.csv`
- `data/singular_teleportation_hierarchy.json`

---

# 3. GHZ-like states

## R7. Full tripartite nonseparability across every bipartition

Consider

`G = E0|000> XOR E0|111>`

and the intrinsic-mixer-generated state

`G_delta = E0|000> XOR delta|111>`.

`G_delta` is obtained from `|000>` by applying `H_star` to the first bit followed by CNOTs from the first bit to the second and third.

**[THEOREM / PROVED]** Both `G` and `G_delta` are nonseparable across every `1|23` bipartition.

Proof for the first cut; the others follow by symmetry. Suppose

`G_c = (p|0> XOR q|1>) tensor Y`,

where the `|000>` coefficient is `E0` and the `|111>` coefficient is `c`, with `c=E0` or `c=delta !=0`. From `p Y_00 = E0`, both `p` and `Y_00` are units. The coefficient of `|011>` must be zero, so `p Y_11=0`; because `p` is a unit, `Y_11=0`. But then the coefficient `q Y_11` of `|111>` is zero, contradicting `c != 0`.

## R8. Explicit modal GHZ contradiction for the support GHZ state

Use the same embedded-F2 settings `Z,X,Y` at each of three parties.

**[EXHAUSTIVE]** All 27 contexts were generated. Among all `2^9=512` deterministic global assignments, **zero** satisfy all support constraints.

Moreover, an exhaustive subset search finds a six-context contradiction, and proves that no subset of one through five of these 27 contexts is already inconsistent.

One minimum witness is:

| Context | Possible outcomes |
| --- | --- |
| `ZZZ` | `{000,111}` |
| `ZXX` | `{000,001,010,011,100}` |
| `XZY` | `{001,010,011,101}` |
| `XXX` | all except `000` |
| `YYZ` | `{001,011,101,110,111}` |
| `YYY` | all except `111` |

**[THEOREM / PROVED]** These six supports are inconsistent with predetermined local outcomes.

From `ZZZ`, let the common predetermined Z outcome be `z`.

- If `z=1`: `ZXX` forces Bob's and Charlie's X outcomes to be `0`. `XZY` with Bob's `Z=1` forces Alice's X outcome to `0`. Thus `XXX=000`, which is impossible.
- If `z=0`: `YYZ` forces Alice's and Bob's Y outcomes to be `1`. `XZY` with Bob's `Z=0` forces Charlie's Y outcome to `1`. Thus `YYY=111`, which is impossible.

Contradiction in both cases.

Raw evidence: `data/ghz_support_mqt_contexts.csv` and `data/ghz_hidden_variable_search.json`.

As with R3, this positive contradiction lives in the embedded `F2` subtheory and should be compared with existing modal/GHZ contextuality rather than claimed as nilpotent-specific.

## R9. The intrinsic `delta` GHZ state is local for the tested families

**[EXHAUSTIVE / NEGATIVE]** For `G_delta=|000> XOR delta|111>` under all 27 embedded-F2 `Z/X/Y` contexts:

- 16 deterministic global assignments are compatible;
- every possible local section is covered by at least one compatible global assignment.

Hence these supports admit an exact relational local model.

**[EXHAUSTIVE / NEGATIVE]** Under the complete four-basis intrinsic-unitary projective family:

- support GHZ: 44 compatible global assignments, zero uncovered possible sections;
- `delta` GHZ: 23 compatible global assignments, zero uncovered possible sections.

Thus the most direct `H_star`-generated GHZ-like state does not yield a modal GHZ contradiction in either tested natural family.

---

# 4. Complete one-bit gate classification

## R10. `2x2` matrices over the 16-element CM ring

**[EXHAUSTIVE]** Every one of the `16^4=65,536` matrices was classified.

| Class | Count |
| --- | ---: |
| All `2x2` matrices | 65,536 |
| Invertible | 24,576 |
| Intrinsic-unitary (`U^dagger U=I`) | 512 |
| Monomial unit phase-permutation | 128 |
| Nonmonomial invertible branch mixers | 24,448 |
| Invertible with all four entries nonzero | 20,608 |
| Unitary monomial | 128 |
| Unitary full splitter | 384 |

The 512 intrinsic-unitaries partition exactly into 128 monomial gates and 384 full splitters.

Raw inventory: `data/gate_inventory_65536.csv`.

**[THEOREM / PROVED]** The invertible count is also derived analytically as `6*8^4=24,576` by reduction to `GL2(F2)`.

**[THEOREM / PROVED]** The monomial count is `2!*8^2=128`.

---

# 5. Separability preservation and generation

## R11. Local maps preserve simple tensors

**[THEOREM / PROVED]** For arbitrary `A`-linear maps `U,V`, not necessarily invertible,

`(U tensor V)(x tensor y) = Ux tensor Vy`.

Therefore every local product map preserves separability.

If `U,V` are invertible, their tensor product also preserves **nonseparability**: if `(U tensor V)s` were separable, applying `U^-1 tensor V^-1` would make `s` separable.

This proof does not require `A` to be a field.

## R12. Complete classification of the 24 two-bit basis permutations

**[EXHAUSTIVE]** Among all `4!=24` computational-basis permutation gates:

- exactly **8** preserve every CM-separable two-party state;
- exactly **16** can map at least one separable state to a nonseparable state.

The preserving eight are exactly the permutations generated by independent local bit flips and party SWAP, i.e. `(S2 x S2) semidirect S2`.

CNOT is among the 16 nonseparability-generating permutations. A transparent witness is

`(|0> XOR |1>) tensor |0>  ->  |00> XOR |11>`.

Raw witnesses for all 16 creating permutations are retained in `data/two_party_basis_permutation_gates.csv`.

**[OPEN]** This is not a classification of all invertible `4x4` matrices over `A`; that much larger separability-preserver problem remains open.

---

# 6. Local equivalence and a Smith-Schmidt analogue

## R13. Exactly 15 local `GL2 x GL2` equivalence classes

**[LITERATURE + THEOREM]** Because `A=F2[u]/(u^4)` is a finite principal chain ring, every `2x2` coefficient matrix has Smith form under invertible row/column operations. Choosing powers of `u` as canonical associates gives exactly

`diag(u^a,u^b)`, `0<=a<=b<=4`,

with `u^4=0`. There are `C(6,2)=15` such ordered pairs with repetition.

**[EXHAUSTIVE]** Every one of the 65,536 coefficient matrices was assigned to exactly one of these 15 classes by its binary rank profile under multiplication by `1,u,u^2,u^3`.

## R14. Exact separability criterion

**[THEOREM / PROVED]** A two-party state in Smith class `(a,b)` is CM-separable iff `b=4`.

Sketch. Any one-party vector over a chain ring can be reduced by a local invertible to `(u^r,0)` (with `r=4` for the zero vector). Hence a simple tensor is locally equivalent to a matrix with at most one nonzero Smith diagonal entry. Conversely `diag(u^a,0)` is visibly an outer product.

**[EXHAUSTIVE]** The set generated by all `16^2 * 16^2=65,536` factor pairs was deduplicated and compared against the Smith criterion for all states: zero mismatches.

Counts:

- **5,266** distinct separable states;
- **60,270** distinct nonseparable states.

## R15. Class sizes and local stabilizers

The complete class table is:

| Smith class `(a,b)` | States in orbit | Separable? | Exact local stabilizer size |
| --- | ---: | --- | ---: |
| (0,0) | 24,576 | no | 24,576 |
| (0,1) | 18,432 | no | 32,768 |
| (0,2) | 9,216 | no | 65,536 |
| (0,3) | 4,608 | no | 131,072 |
| (0,4) | 4,608 | yes | 131,072 |
| (1,1) | 1,536 | no | 393,216 |
| (1,2) | 1,152 | no | 524,288 |
| (1,3) | 576 | no | 1,048,576 |
| (1,4) | 576 | yes | 1,048,576 |
| (2,2) | 96 | no | 6,291,456 |
| (2,3) | 72 | no | 8,388,608 |
| (2,4) | 72 | yes | 8,388,608 |
| (3,3) | 6 | no | 100,663,296 |
| (3,4) | 9 | yes | 67,108,864 |
| (4,4) | 1 | yes | 603,979,776 |

The acting local group has size `24,576^2=603,979,776`, so the stabilizer sizes follow by orbit-stabilizer after the Smith classification identifies each row as one orbit.

For the support Bell state `I`, the full exact local stabilizer has the explicit form

`{ (U, (U^-1)^T) : U in GL2(A) }`,

hence size 24,576.

For `Beta_delta=diag(1,delta)`, Smith class `(0,2)` has orbit size 9,216 and exact local stabilizer size 65,536.

## R16. Nilpotent-specific resource hierarchy

**[THEOREM / INTERPRETATION]** The support Bell state has Smith class `(0,0)`, while the natural `B_star` state has class `(0,2)`. Both are CM-nonseparable, but only the first has an invertible coefficient pairing.

Over a field, a nonseparable two-by-two pure-state coefficient matrix has rank two and hence is invertible. Over the CM chain ring, zero divisors permit **singular but nonseparable** classes `(a,b)` with `b<4` and determinant a nonunit or zero.

This Smith splitting is the core ring-specific structural phenomenon of this pass. R4 shows that it controls the strength of complete-basis possibilistic contextuality, while R6 shows that singularity can also obstruct the natural universal-teleportation correction scheme. Thus “nonseparable” is too coarse a resource label for either task.

---

# 7. Secondary results

## R17. No-cloning analogue

**[THEOREM / PROVED]** Let an `A`-linear map with fixed blank clone both computational basis states:

`C|0> = |00>`, `C|1> = |11>`.

Then linearity forces

`C(|0> XOR |1>) = |00> XOR |11>`.

Exact tensor cloning would require

`(|0> XOR |1>) tensor (|0> XOR |1>)`

`= |00> XOR |01> XOR |10> XOR |11>`,

which differs by two nonzero cross terms. Therefore no such linear exact cloner exists for a state set containing these three states.

This is the standard linear/modal no-cloning mechanism, not a CM-specific novelty claim.

## R18. Superdense-coding-like algebraic protocol

**[THEOREM / CONSTRUCTION]** With the shared support Bell resource `R`, the four local sender operations

`I, X, K, KX`

produce the four nonseparable basis states used as columns of `Q`. The receiver applies `Q^-1`, after which the state is one of four computational basis outcomes.

This is a clean two-bit **algebraic/modal coding analogue**.

**Boundary:** without a physical communication/resource model, this does not establish a physical two-classical-bit-per-qubit capacity advantage.

## R19. When a global CM unit is harmless

**[THEOREM / PROVED]** Under support-only readout, complete-state multiplication by a unit `g` is observationally invisible:

`g a_i = 0  iff  a_i=0`

for every coefficient. Unit scaling also preserves separability and nonseparability because `g` can be absorbed into one tensor factor and inverted.

Therefore quotienting states by a global unit is justified **only after** choosing support-only modal semantics.

For exact CM-pattern readout, global unit multiples can be distinguished and should not be quotiented. Multiplication by a nonunit is never a harmless global phase in general because zero divisors can annihilate nonzero coefficients.

## R20. Smith data as a Schmidt-rank analogue

**[PROVED / INTERPRETIVE]** The ordered pair `(a,b)` of Smith valuations is a natural replacement for a single field rank. It distinguishes:

- separable rank-one-like classes `(a,4)`;
- nondegenerate Bell-like class `(0,0)`;
- increasingly nilpotent nonseparable classes such as `(0,2)`.

Calling this a “Schmidt decomposition” would overstate the analogy: there is no positive norm, normalized singular value spectrum, or probability interpretation. “Smith-Schmidt analogue” is safer shorthand.

---

# 8. Open items left by this pass

**[OPEN]** The following were not promoted to results:

- full characterization of all `4x4` two-party invertibles that preserve the Segre/simple-tensor variety over `A`;
- extension of the two-party Smith/contextuality theorem to multipartite states and to restricted physically motivated gate-generated measurement families;
- extension of the singular-resource hierarchy to any future nonlinear or explicitly multi-round measurement/update calculus;
- a canonical partial trace/reduced-state operation compatible with the chosen pure modal/LM semantics, needed before a rigorous monogamy claim;
- a complete stabilizer/Clifford-like subtheory generated specifically by `P`, `H_star`, CNOT, and local CM units;
- error-correcting/code resource statements for the modal state calculus;
- physical or computational complexity advantage claims.
