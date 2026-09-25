# Current State of the CM Phase / Boolean-Quantum Research

## 1. Original CM substrate

Use the original paper's convention. A two-input CM is a binary 2x2 matrix with rows `X=1, X=0` and columns `Y=1, Y=0`. The four one-feature basis matrices are, in clockwise cyclic order:

- `E0 = [AND] = [[1,0],[0,0]]`
- `E1 = [UP]  = [[0,1],[0,0]]`
- `E2 = [NOT OR] = [[0,0],[0,1]]`
- `E3 = [DOWN] = [[0,0],[1,0]]`

The original paper uses XOR (rendered as `m` in extracted text), AND, Boolean complement, CM rotations/transposes, quotient `A \ B = A AND NOT B`, LM measurement, and tensor/higher-dimensional constructions.

## 2. Intrinsic Boolean phase algebra

Define a new product `star` by cyclic convolution of CM-basis coefficients over F2:

`E_r star E_s = E_(r+s mod 4)`

and extend by XOR-linearity. This uses only Boolean AND for coefficient products and XOR for coefficient sums.

Then:

`A = F2[C4] ~= F2[u]/(u^4)` with `u = E0 XOR E1 = [L]`.

Let `t = E1`. Then:

- `t^2 = E2`
- `t^3 = E3`
- `t^4 = E0`

Thus `E0,E1,E2,E3` have the multiplicative table of `1, i, -1, -i`, but `E2` is a 180-degree **phase opposite**, not an additive negative under XOR. Characteristic two still has additive `-A=A`.

Multiplication by `t` equals one clockwise CM rotation. Transpose is an automorphism and acts as phase conjugation on the pure four-phase subgroup.

Verified ring structure includes:

- 16 elements total.
- 8 units, exactly the odd-Hamming-weight CMs.
- 8 nilpotents/nonunits, exactly the even-Hamming-weight CMs.
- Unit group is `C4 x C2`.
- Exactly four square roots of the phase-half-turn `E2`: `[UP]`, `[DOWN]`, `[LEFT IMPLIES]`, `[IMPLIES]`.
- The ring is a finite chain ring with the ideal chain recorded in the CSVs.

## 3. Binary operator representation

Let `P` be the 4x4 binary cyclic permutation matrix acting on cyclic CM coefficients. Then:

- `P^4 = I`
- `P^T = P^-1 = P^3`
- multiplication uses only AND/XOR over F2.

`P` is the regular-representation operator for the Boolean phase `t`. It is unipotent rather than a complex rotation: `(P+I)^4=0` and `P^2 != -I` because `-I=I` in F2.

## 4. Reversible branch mixing without an ordinary Hadamard

Two important one-bit mixers are known.

### Simple shear splitter

`C = [[1,0],[1,1]]` over the CM coefficient ring.

- `C^2 = I`.
- `C|0> = |0> XOR |1>` in support terms.
- It is reversible, but is not the strongest intrinsic-unitary analogue.

### Intrinsic-unitary mixer

Let `z=t^2=E2` and `delta=E0 XOR E2 = [XNOR]`. Then `delta star delta = 0`.

Define

`H_star = [[E0, delta],[delta,E0]]`.

Verified:

- `H_star^2=I`.
- `H_star^dagger H_star=I` using matrix transpose plus CM transpose as conjugation.
- `H_star|0> = E0|0> XOR delta|1>`.
- `H_star|1> = delta|0> XOR E0|1>`.

In the 4x4 regular representation, `delta` corresponds to `D=I XOR P^2`, so the complete binary matrix is `[[I,D],[D,I]]` and contains only 0/1 entries.

## 5. Phase kickback

Use the target state

`chi = (E0, E2) = |0> + z|1>` in CM-coefficient notation.

The Boolean swap X satisfies

`X chi = z star chi`.

Therefore a reversible Boolean oracle `U_f|x,y> = |x, y XOR f(x)>` gives

`U_f |x> chi = z^{f(x)} |x> chi`.

This is exact phase kickback inside the pure Boolean CM phase algebra.

## 6. Interference-like splitter / phase / recombiner

A reversible CM splitter using `[L]=E0 XOR E1` produces a detector CM sequence with Hamming weights:

`(0,2,4,2)` for relative phases `0,90,180,270` degrees.

Normalized only as an external counting statistic this is `(0,1/2,1,1/2)`. Do **not** call this a Born probability. The CM evolution is Boolean; Hamming counting is an external integer observable.

An exhaustive search found 8,192 reversible 2x2 CM-ring splitters producing that detector-weight sequence.

## 7. Phase-Mobius / ANF computation

Define the Boolean shear tensor `M_n = C^{tensor n}` and a half-turn phase oracle `P_f`. Starting from the zero basis state:

`M_n P_f M_n e_empty = e_empty XOR delta * ANF(f)`.

The output CM pattern encodes the algebraic normal form (ANF) coefficients of `f`, modulo the special constant-branch encoding.

Verified exhaustively for every Boolean function through n=4 (65,812 function cases total across n=1..4).

Consequences already tested:

- exact constant-vs-nonconstant discrimination;
- Bernstein-Vazirani-like recovery of affine coefficients;
- marked-item pattern decoding;
- n=2 single-CM Deutsch-Jozsa detectors and n=3 multichannel detectors.

This does not establish a quantum or classical speedup: explicit storage of all 2^n branches remains exponential. The current research hypothesis is that CM operator normalization/folding can sometimes reduce compressed ANF propagation cost before expansion.

## 8. Direct CM-to-ANF propagation

For a CM `Theta` with entries ordered as in the paper, and subexpression ANFs `P_X,P_Y`, the Boolean operator has ANF

`a XOR b P_X XOR c P_Y XOR d(P_X P_Y)`

where

- `a = Theta_22`
- `b = Theta_12 XOR Theta_22`
- `c = Theta_21 XOR Theta_22`
- `d = Theta_11 XOR Theta_12 XOR Theta_21 XOR Theta_22`

Thus `d` is CM feature parity. Exactly the odd-weight/unit CMs have a nonlinear `XY` term; exactly the even-weight/nilpotent CMs are affine.

This bridge between the phase-ring unit classification and Boolean multiplicative complexity is worth benchmarking.

## 9. Pure-Boolean Bell-like states and nonseparability

Two-bit coefficient states live in `A^4`, basis order `|00>,|01>,|10>,|11>`.

A state is called **CM-separable** if it factors as a simple tensor of two one-bit CM-coefficient states; otherwise call it **CM-nonseparable**. Prefer this term over physical 'entangled' unless the modal analogy is explicitly being discussed.

The support Bell state

`Phi_plus = E0|00> XOR E0|11>`

was exhaustively checked against all 16^4 simple-factor candidates and has zero factorizations. Phase variants and Psi variants are likewise nonseparable.

A fully intrinsic-unitary Bell transform is

`B_star = CNOT (H_star tensor I)`.

It maps the four computational basis states to four nonseparable CM states:

- `|00> -> E0|00> XOR delta|11>`
- `|01> -> E0|01> XOR delta|10>`
- `|10> -> delta|00> XOR E0|11>`
- `|11> -> delta|01> XOR E0|10>`

The inverse was verified on all 65,536 two-bit CM coefficient states.

Also verified:

`(H_star tensor H_star) Phi_plus = Phi_plus` exactly.

A search found 224 genuine local reversible CM mixers preserving `Phi_plus` exactly under `U tensor U`, and 448 preserving it up to multiplication by a CM unit.

## 10. Measurement language

The original paper's LMs measure logical truth/relationships and extend by tensor construction to higher dimensions. In the pure-Boolean modal interpretation, the safest basic readout is:

- coefficient `0` -> impossible/support absent;
- coefficient nonzero -> possible/support present;
- an LM can refine the readout by testing logical relations/patterns.

This is **not** a probability rule. A nonzero CM coefficient can also carry intrinsic phase structure.

## 11. Bell-like encoding / decoding and no-cloning

Because `B_star` is reversible, `B_star^-1` followed by logical-basis/LM readout is a Bell-basis-like analyzer.

Local X operations move among the four Bell-like states in the tested encoding, allowing a superdense-coding-like algebraic protocol. Do not claim a communication advantage without a physical resource model.

A no-cloning analogue follows from XOR-linearity: a linear map that clones `|0>` and `|1>` cannot also clone `|0> XOR |1>` because linearity yields only `|00> XOR |11>`, whereas tensor-cloning produces all four basis terms.

## 12. Known limitations / corrections

- XOR is not complex amplitude addition.
- `E2` is a phase opposite, not an additive negative.
- The intrinsic self-product/norm has nonzero isotropic elements; it is not a positive probability norm.
- No Born rule has been derived from pure CM Boolean logic.
- Hamming-normalized detector values are external counting statistics, not probabilities.
- The signed `J` lift and Clifford/T results belong to a separate extension and should not be silently imported into the pure-Boolean branch.
- Earlier claims that maximal CHSH required a C16 lift were corrected: in the signed quantum representation C8/Clifford+T suffices projectively. Historical CSVs with contrary names are retained only for provenance.
- 'Computes ANF without a truth table' is not itself novel; Boolean Mobius, ZDD/FDD, Reed-Muller, XAG and related methods are established comparison targets.

## 13. Immediate next research programs

### A. Computation and benchmarking

Implement a CM-normalizing symbolic compiler that folds operator structure before ANF/ZDD expansion. Compare fairly to direct sparse ANF, truth-table Mobius, ZDD/PolyBoRi, ROBDD/CUDD, structural CSE, XAG and other strong baselines. Retain negative results.

### B. Pure-Boolean modal / quantum-like mathematics

Investigate:

1. a modal Bell-test table based only on possible/impossible LM outcomes;
2. pure-CM teleportation of arbitrary `A|0> XOR B|1>`;
3. GHZ-like three-party nonseparability and modal GHZ contradiction;
4. classification of intrinsic reversible gates that preserve or generate nonseparability;
5. modal measurement bases and contextuality-like structures;
6. resource theory for phase, nilpotent mixing and nonseparability.
