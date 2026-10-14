# Context and Relative Purity

## 1. Historical issue

The 2015 thesis already observes that `X` is "pure" when considered in a one-variable universe but is not pure after embedding into a two-variable universe, because `X=true` then corresponds to two valuations distinguished by the new variable.

This observation is correct once purity is typed relative to a carrier/context.

## 2. Two different purity notions

### Semantic singleton support

For event `E` and current support `S`, call the outcome semantically singleton if

\[
|S\cap E|=1.
\]

### Observational purity of a world

For `x in S`, define

\[
\boxed{
x\text{ is }(S,\Phi)\text{-pure}
\iff
[x]_\Phi\cap S=\{x\}.
}
\]

This means the current interface uniquely identifies `x` among surviving possibilities.

The two notions coincide only under extra conditions.

## 3. Cylinder extension theorem

Let an event `E subseteq Omega_n` ignore `m` newly introduced variables. Its cylinder extension to `Omega_{n+m}` is

\[
E\times\{0,1\}^m.
\]

Hence

\[
|E^{\uparrow}|=2^m|E|.
\]

A singleton support in `Omega_n` therefore becomes `2^m` worlds after adding `m` unconstrained coordinates. This is ordinary cylinder-set extension, not contextuality by itself.

The three-variable computation checks the simplest case: `X=true` has one satisfying state in `Omega_1` but four in `Omega_3`.

## 4. Where deeper context can enter

There are at least three stronger notions than cylinder extension:

1. the available observation family changes with context;
2. different contexts expose incompatible effect algebras;
3. no global assignment can consistently glue all contextwise outcomes.

Only the third kind reaches the sheaf-theoretic contextuality boundary in the Abramsky--Brandenburger sense. The thesis's context-relative purity observation alone does not establish this.
