# Differentiation Measures

Let `Pi` be the observational partition and `S` the surviving support. Write `n_C=|S cap C|` for each block `C`.

## 1. Measures that separate the two axes

### Global observational resolution

\[
D_0(\Pi)=|\Pi|.
\]

It is monotone under refinement but ignores `S`.

### Effective surviving classes

\[
D_S(\Pi)=|\{C\in\Pi:C\cap S\ne\varnothing\}|.
\]

It is nondecreasing under refinement but may decrease under conditioning because whole classes can be eliminated. It therefore should not be advertised as a single monotone for both operations.

### Hartley support uncertainty

\[
H_0(S)=\log_2|S|.
\]

It is nonincreasing under hard conditioning but unchanged by refinement.

The cleanest representation of the two primitive effects may therefore be **vector-valued** rather than forcing one scalar.

## 2. A joint probability-free monotone

Define pair ambiguity

\[
\boxed{
A_2(S,\Pi)=\sum_{C\in\Pi}{|S\cap C|\choose 2}.
}
\]

It counts the unordered pairs of surviving worlds that the current interface still cannot distinguish.

### Proposition

`A_2` is nonincreasing under both operations:

1. partition refinement;
2. support restriction `S' subseteq S`.

**Proof idea.** Splitting a cell of size `a+b` replaces `C(a+b,2)` by `C(a,2)+C(b,2)`, decreasing by `ab`. Restricting support can only decrease each block size.

Moreover,

\[
A_2(S,\Pi)=0
\iff
\Pi|_S\text{ is discrete}.
\]

All 4,800 bounded monotonicity cases in the main computation and 130,560 independently formulated assertions passed.

## 3. Worst-case ambiguity

\[
A_\infty(S,\Pi)=\max_{C\in\Pi}|S\cap C|.
\]

This too is nonincreasing under both refinement and conditioning. It measures the largest residual indistinguishability class rather than total pair ambiguity.

## 4. A precise symmetry connection

Define the **invisible permutation group**

\[
G_{\rm inv}(S,\Pi)
=
\prod_{C\in\Pi}\operatorname{Sym}(S\cap C).
\]

These are exactly the permutations of surviving worlds that operate entirely within current observation cells and are therefore invisible to the two-sided interface.

Its order is

\[
|G_{\rm inv}|=\prod_C |S\cap C|!.
\]

Both refinement and conditioning canonically shrink this within-cell symmetry.

A useful identity is:

\[
\boxed{
A_2(S,\Pi)=\text{number of transpositions contained in }G_{\rm inv}(S,\Pi).
}
\]

Each indistinguishable pair in a cell corresponds to exactly one within-cell transposition. This is elementary group theory, so it is presented as a useful bridge rather than a novelty claim. It gives a cleaner meaning to "symmetry reduction" than the previously tested D4 stabilizer-size criterion, which was not monotone under restriction.

## 5. Probability and information

Let random world `X` have distribution `p`, and let `Y=o_Phi(X)` be its deterministic observation signature.

Then

\[
I(X;Y)=H(Y).
\]

Adding observation `Z` gives the standard chain rule

\[
I(X;Y,Z)=I(X;Y)+I(X;Z\mid Y).
\]

Thus expected resolution gain has a clean information-theoretic interpretation. A realized conditioning branch has surprisal `-log p(E)`; average gain over outcomes is mutual information. Do not assume that normalized posterior Shannon entropy decreases for every individual branch.

## 6. Recommendation

Use three reported quantities rather than one opaque "consciousness" number:

- `A_2(S,Pi)` or `A_infty(S,Pi)` for unresolved ambiguity;
- `|S|` / Hartley uncertainty for remaining possibility mass;
- ProLT topological/homological invariants for directional observational structure that survives beyond the partition layer.
