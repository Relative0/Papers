# Finite Hierarchy Example: Four Binary Attributes

## 1. Setup

Use four ordered binary attributes:

- `a0`: color (`0=blue`, `1=red`)
- `a1`: size (`0=small`, `1=large`)
- `a2`: texture (`0=rough`, `1=smooth`)
- `a3`: motion (`0=still`, `1=moving`)

A fully specified state is a 4-bit string

`x=a0 a1 a2 a3`.

There are 16 depth-4 states.

Define the common-prefix ultrametric

`d(x,y)=0` if `x=y`, otherwise `2^{-L(x,y)}`,

where `L(x,y)` is the number of initial coordinates on which `x,y` agree.

This finite model is the first four levels of the boundary of the infinite binary tree. If the bits are interpreted as least-significant-first p-adic digits,

`Phi(a0a1a2a3)=a0 + 2 a1 + 4 a2 + 8 a3`,

then for distinct depth-4 strings

`d(x,y)=|Phi(x)-Phi(y)|_2`.

The supplied script verifies this exhaustively.

---

## 2. Depth 0

### Concept balls

- `B_epsilon = {all 16 states}`.

### Quotient

`X/~_0` has one class.

### Observable

No attribute is visible.

### Unobservable

Color, size, texture, motion, and every distinction among the 16 leaves.

### Measure and information

`mu(B_epsilon)=1`, information gained = `0` bits.

---

## 3. Depth 1

### Concept balls

- `B_0`: all blue states, prefix `0`
- `B_1`: all red states, prefix `1`

Each contains 8 depth-4 leaves.

### Inclusions

`B_0,B_1 subset B_epsilon`, and `B_0 intersection B_1 = empty`.

### Quotient

`X/~_1 = {0,1}`.

### Observable

Color only.

### Unobservable

All distinctions in size, texture and motion.

### Distances

Any state beginning `0` and any state beginning `1` have distance `1`.

### Measure/information

Each ball has measure `1/2`; observing the first bit yields 1 bit under the uniform model.

---

## 4. Depth 2

### Concept balls

- `B_00`: blue-small
- `B_01`: blue-large
- `B_10`: red-small
- `B_11`: red-large

Each contains 4 leaves.

### Inclusions

`B_00,B_01 subset B_0`; `B_10,B_11 subset B_1`.

Sibling balls are disjoint.

### Quotient

`X/~_2 = {00,01,10,11}`.

### Observable

Color and size.

### Unobservable

Texture and motion.

### Example distances

- `0000` vs `0010`: common prefix `00`, so `d=1/4`.
- `0000` vs `0100`: common prefix `0`, so `d=1/2`.
- `0000` vs `1000`: no common initial bit, so `d=1`.

---

## 5. Depth 3

### Concept balls

`B_000, B_001, B_010, B_011, B_100, B_101, B_110, B_111`.

Semantically, for example:

- `B_000`: blue-small-rough
- `B_001`: blue-small-smooth
- `B_111`: red-large-smooth

Each contains 2 leaves (still/moving unresolved).

### Quotient

`|X/~_3|=8`.

### Observable

Color, size, texture.

### Unobservable

Motion.

### Measure/information

Each ball has measure `1/8`; a fully specified depth-3 prefix carries 3 bits in the uniform hierarchy.

---

## 6. Depth 4

### Concept balls

All 16 singleton prefixes:

`0000,0001,0010,0011,0100,0101,0110,0111,1000,1001,1010,1011,1100,1101,1110,1111`.

### Quotient

`|X/~_4|=16`.

### Observable

All four modeled attributes.

### Unobservable

Nothing **within this finite four-attribute model**. In an infinite hierarchy, deeper coordinates would remain unresolved.

---

## 7. Full ball hierarchy

There are

`1+2+4+8+16 = 31`

prefix balls through depth 4. The generated file `balls_depth4.csv` lists every ball, its members, uniform measure, and information depth.

The inclusion order is exactly the binary rooted tree.

---

## 8. Least common ancestors and joins

Take `x=0011` and `y=0000`.

Their longest common prefix is `00`, so their least common concept is `B_00`.

Take `x=0011` and `y=0110`.

Their longest common prefix is `0`, so their least common concept is `B_0`.

Take `x=0011` and `y=1110`.

Their longest common prefix is empty, so their least common concept is the root `B_epsilon`.

Thus the least common ancestor gives the natural “smallest common generalization.”

---

## 9. Correct handling of “shared attributes”

Suppose

`C=B_011` (blue-large-smooth)

and

`D=B_111` (red-large-smooth).

Then

`C intersection D = empty`

because they disagree on color.

Yet both share the attributes “large” and “smooth.” To extract that shared information, one must **project away color**, e.g.

`rho_{1,2}(a0,a1,a2,a3)=(a1,a2)`.

Then

`rho_{1,2}(C)=rho_{1,2}(D)=(1,1)`.

This is the correct mathematical replacement for the thesis's operation that treated conflicting cylinders as if their intersection retained common coordinates.

---

## 10. Rooted-tree vs ultrametric vs p-adic descriptions

### Rooted-tree description

A path records successive attribute choices. Depth is specificity. LCA is shared generalization.

### Ultrametric description

Distance is determined only by the earliest coordinate at which two states diverge. Balls are exactly hierarchical concepts.

### 2-adic description

Interpret bit `a_i` as the coefficient of `2^i`. Then agreeing on the first `k` attributes means the corresponding integers are congruent modulo `2^k`. The concept ball is a residue class mod `2^k`.

### What p-adics add here

Nothing is gained for the four-bit hierarchy itself beyond arithmetic coordinates. p-adic structure becomes useful when one wants algebraic dynamics, Haar measure, harmonic analysis, or infinite-depth arithmetic.

---

## 11. Observational interpretation

At depth `k`, the observer receives only `pi_k(x)`.

Thus, if the true state is `0011`, then:

- at `k=0`: it is indistinguishable from all 15 other states;
- at `k=1`: indistinguishable from the 7 other blue states;
- at `k=2`: indistinguishable from the 3 other blue-small states;
- at `k=3`: indistinguishable from `0010` only;
- at `k=4`: uniquely identified among the 16 modeled states.

The underlying space has not changed. Only the observation partition has refined.

This is the central mechanism proposed for a rigorous “ultrametric unconscious.”
