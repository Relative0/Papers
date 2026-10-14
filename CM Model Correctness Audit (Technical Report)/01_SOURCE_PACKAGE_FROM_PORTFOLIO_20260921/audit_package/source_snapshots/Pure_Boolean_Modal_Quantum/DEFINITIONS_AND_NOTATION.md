# Definitions and Notation

## 1. Original CM convention

A two-input correspondence matrix (CM) is a Boolean `2x2` array. We retain the original paper's row/column ordering: the first row/column corresponds to truth value `1`, the second to `0`. The cyclic one-feature basis used by the intrinsic phase extension is

```text
E0 = [AND]    = [[1,0],[0,0]]
E1 = [UP]     = [[0,1],[0,0]]
E2 = [NOT OR] = [[0,0],[0,1]]
E3 = [DOWN]   = [[0,0],[1,0]]
```

A four-bit ring element is written

`A = a0 E0 XOR a1 E1 XOR a2 E2 XOR a3 E3`, `ai in F2`.

The code stores this as the integer bit pattern `a0 + 2 a1 + 4 a2 + 8 a3`; that integer is only a compact external encoding.

The original paper's support quotient is distinct from ring division:

`A \ B = A AND NOT B`

entrywise in the four CM features.

## 2. Intrinsic phase ring

Define cyclic convolution by

`E_r star E_s = E_(r+s mod 4)`

and extend by XOR-linearity. Then

`A = F2[C4] ~= F2[t]/(t^4-1) ~= F2[u]/(u^4)`, where `t=E1` and `u=E0 XOR E1`.

We use

```text
1_A   = E0
t     = E1
z     = t^2 = E2
delta = E0 XOR E2 = u^2
Omega = E0 XOR E1 XOR E2 XOR E3 = u^3
```

Important identities:

```text
t^4 = E0
delta star delta = 0
Omega star Omega = 0
```

The ring has 16 elements. Its units are exactly the eight odd-feature-parity CMs; every nonunit is nilpotent. Its ideals form the chain

`0 < (Omega) < (delta) < (u) < A`.

Transpose swaps `E1 <-> E3` and fixes `E0,E2`. We denote this involution by a bar in formulas and by `bar()` in code. It is the intrinsic conjugation used in `dagger`.

## 3. Modules and states

A one-bit CM coefficient state is a vector in `A^2`:

`psi = A|0> XOR B|1>`.

A two-bit state is in `A^4` and is stored in computational order

`|00>, |01>, |10>, |11>`.

It is often identified with the coefficient matrix

```text
M_psi = [[a00,a01],
         [a10,a11]].
```

Under local one-bit matrices `U,V`,

`(U tensor V) psi  <->  U M_psi V^T`.

Three-bit states are stored in ascending computational bitstring order.

All state evolution in the core calculation uses only XOR and `star` multiplication of Boolean-coefficient ring elements.

## 4. CM-separability

**Definition.** A two-party state is **CM-separable** if it is a simple tensor `x tensor y` with `x,y in A^2`. Otherwise it is **CM-nonseparable**.

This is a ring-module factorization property. It is not silently identified with physical quantum entanglement. Phrases such as *entangled-like* or *modal entanglement analogue* are used only after this definition is fixed.

For `2x2` coefficient matrices over this chain ring, local `GL2(A) x GL2(A)` equivalence admits Smith representatives

`diag(u^a,u^b)`, `0 <= a <= b <= 4`,

where exponent `4` means the zero diagonal entry. A state is CM-separable exactly when `b=4`.

## 5. Gates

A one-bit gate is a `2x2` matrix over `A`. Matrix contraction uses `star` for scalar multiplication and XOR for scalar addition.

- **invertible:** determinant is a unit;
- **intrinsic-unitary:** `U^dagger U = I`, where dagger is matrix transpose followed by CM transpose on each entry;
- **monomial phase-permutation gate:** one nonzero unit in each row and column;
- **genuine branch mixer (inventory convention):** invertible and not monomial;
- **full two-branch splitter:** all four entries are nonzero.

Important gates:

```text
C = [[E0, 0 ],
     [E0, E0]]

H_star = [[E0,    delta],
          [delta, E0   ]]

X = [[0, E0],
     [E0, 0]]
```

`CNOT` is the usual computational-basis permutation `|x,y> -> |x,x XOR y>`.

The known Bell-like transform is

`B_star = CNOT (H_star tensor I)`.

## 6. Modal measurement contract used in this project

The original CM manuscript develops CM/LM measurement as logical truth/relationship measurement and explicitly does not add probability densities. For the present ring-valued modal extension we therefore make the following **additional explicit contract**.

A two-outcome local measurement basis is an ordered pair of effect rows `(e0,e1)` forming an invertible `2x2` matrix over `A`. On a one-party state `v`, outcome `i` is:

- **possible** iff `ei v != 0` in `A`;
- **impossible** iff `ei v = 0`.

For multipartite local settings, a joint outcome is possible iff contraction with the tensor product of the selected local effects is nonzero.

This is a support/possibility rule, **not a probability rule**.

Two effect rows differing by multiplication by a unit define the same support-only effect because `g a = 0` iff `a=0` for a unit `g`. Therefore projective measurement bases are quotiented by independent unit rescaling of rows. Outcome swap is also quotiented when counting **unordered** bases.

When the exact CM coefficient pattern is the readout rather than mere zero/nonzero support, unit rescaling is generally observable and must not be quotiented away.

No post-measurement collapse/update rule is assumed in the core Bell/GHZ support tests. Teleportation is stated conditionally: for each possible analyzer outcome, the corresponding receiver branch is computed and corrected.

## 7. Embedded F2 modal bases

Three reversible bases used for the Bell/GHZ witnesses are

```text
Z = {(E0,0),  (0,E0)}
X = {(E0,E0), (E0,0)}
Y = {(0,E0),  (E0,E0)}
```

Each is an invertible `2x2` matrix over the embedded scalar subfield `F2 * E0`. These are the three projective two-outcome bases of the two-dimensional `F2` modal subtheory.

## 8. Hidden-variable / contextuality terminology

For a finite family of local dichotomic settings, a **deterministic global assignment** chooses one outcome for every local setting in advance.

- It is **compatible** if every selected joint outcome is possible in every measurement context.
- If no compatible global assignment exists, the support model is **strongly contextual / strongly possibilistically nonlocal** in the sense of a global-section obstruction.
- If at least one compatible global assignment exists but **some possible local section has no compatible global extension**, the support model is **logically (possibilistically) contextual/nonlocal** but not strong. This is the Hardy-type level of the standard support hierarchy.
- To show an exact relational local hidden-variable representation, every possible local section must extend to at least one compatible global assignment; equivalently, the support is the union of compatible deterministic global sections.

The code distinguishes all three notions. A satisfiable 2-SAT test over a large setting family proves only that strong contextuality is absent; exact support-extension coverage is separately checked.

## 9. Evidence labels

Every substantive result in the prose is tagged as one of:

- **[THEOREM / PROVED]** algebraic proof supplied;
- **[EXHAUSTIVE]** all elements of a stated finite universe enumerated;
- **[REGRESSION]** computational identity/spot check;
- **[OPEN]** conjecture or unresolved question;
- **[LITERATURE]** comparison to published/preprint work.

External integer counts such as Hamming weight, number of states, or number of assignments are diagnostics about a finite Boolean computation. They are not state amplitudes.
