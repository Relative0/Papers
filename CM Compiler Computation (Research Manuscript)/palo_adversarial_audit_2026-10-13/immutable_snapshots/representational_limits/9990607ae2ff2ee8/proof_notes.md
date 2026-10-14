# Proof notes: representational limits and normalized alternatives

Prepared 13 October 2026. These are research derivations, not a submitted paper or formal proof-assistant certificates. Historical originality is not claimed. References use the keys in **references.bib**.

## 1. Specifications and resource conventions

Let \(h:\{-1,+1\}^n\to\{-1,+1\}\), with positive meaning true. Exact local orthant realization means

\[
h(\operatorname{sgn}x)F(x)>0
\quad(x\in B_R(0),\ \prod_i x_i\ne0).
\]

The domain of \(F\) includes the common corner as an interior point. The specification excludes coordinate walls but requires correctness arbitrarily close to them. Let

\[
Q_n=[-1,1]^n,\qquad
D_{\delta,n}=\{x\in Q_n: |x_i|\ge\delta\ \forall i\},\quad 0<\delta<1.
\]

Define \(d_h(\delta)\) as the smallest total degree of a real polynomial strictly sign-realizing \(h\) on \(D_{\delta,n}\). There is no coefficient, amplitude, or margin bound in this definition. Define \(d_{h,\gamma}^{\rm bd}(\delta)\), \(0<\gamma<1\), by imposing additionally

\[
\|P\|_{Q_n,\infty}\le1,\qquad
h(\operatorname{sgn}x)P(x)\ge\gamma\quad(x\in D_{\delta,n}).
\]

The amplitude bound covers the whole cube, including the excluded boundary region. It is crucial to the Bernstein lower bound. Constants in fixed-arity asymptotics can depend on \(h,n,\gamma\). No statement below gives sharp bounds uniform in growing \(n\), coefficient bit length, neural parameter norm, or evaluation cost.

## 2. Derived fixed-arity polynomial classification

**Proposition P1 (complete argument, dependent on a known lower bound).** For fixed \(n\ge1\):

1. A signed parity \(h(s)=c\prod_{i\in S}s_i\) satisfies \(d_h(\delta)=|S|\), including degree zero for constants.
2. Every non-affine Boolean sign law satisfies
   \[
   d_h(\delta)=\Theta_h(\log(1/\delta))\qquad(\delta\downarrow0).
   \]
3. Every nonconstant Boolean sign law, for fixed \(0<\gamma<1\), satisfies
   \[
   d_{h,\gamma}^{\rm bd}(\delta)=\Theta_{h,\gamma}(1/\delta).
   \]

These are consequences of classical rational/polynomial approximation and threshold degree, not asserted new theorems. The sign-only result does not follow from universal approximation alone.

### 2.1 Parity lower bound

The product polynomial gives the upper bound. For the lower bound, restrict to the Boolean vertices, fixing variables outside \(S\). A polynomial of degree less than \(|S|\) has zero correlation with parity under the uniform measure on those vertices, after multilinear reduction. Strict sign agreement would give strictly positive correlation. Thus degree at least \(|S|\) is necessary, even with arbitrary real coefficients.

### 2.2 Rational construction and logarithmic upper bound

First take \(\delta=2^{-m}\). For a positive integer \(L\), set

\[
p(t)=\prod_{j=0}^m(t+2^{-j})^{2L},\quad
a(t)=p(t)-p(-t),\quad q(t)=p(t)+p(-t),\quad r(t)=a(t)/q(t).
\]

The two polynomials \(p(t),p(-t)\) are nonnegative and cannot vanish together, so \(q(t)>0\) on the entire real line. Consequently \(|r(t)|\le1\). For \(t\in[\delta,1]\), choose a node \(u=2^{-j}\) such that \(u\le t\le2u\). Then

\[
0\le z=\frac{p(-t)}{p(t)}
=\prod_j\left|\frac{2^{-j}-t}{2^{-j}+t}\right|^{2L}
\le3^{-2L}.
\]

The selected ratio is at most \(1/3\), and every other ratio is at most one. Therefore

\[
|r(t)-1|=\frac{2z}{1+z}\le2\,3^{-2L}.
\]

Oddness gives the negative-interval estimate. This is a simple dyadic version of the Newman rational-approximation method; compare [Sherstov2013, Theorem 2.4, author PDF pp. 11-12]. It is not an optimal Zolotarev construction.

For arbitrary \(h\), use its ordinary multilinear expectation extension

\[
H_h(u)=\sum_{s\in\{-1,+1\}^n}h(s)
\prod_i\frac{1+s_i u_i}{2}.
\]

On the whole cube \(u\in[-1,1]^n\), \(|H_h(u)|\le1\). If each \(u_i\) is within \(\epsilon\) of the corresponding input sign, a product-distribution coupling gives

\[
h(s)H_h(u)\ge1-n\epsilon.
\]

Each random coordinate differs from \(s_i\) with probability at most \(\epsilon/2\); the union bound controls any incorrect coordinate, and changing a sign label costs at most two. Choose \(L\) so that \(n\epsilon<1\). Substituting \(u_i=r(x_i)\) and multiplying by the positive denominator \(\prod_iq(x_i)\) yields a polynomial of total degree at most \(2Ln(m+1)\) with the required strict signs. For fixed \(n\), \(L\) is constant. For arbitrary \(\delta\), choose a dyadic value no larger than \(\delta\); this changes \(m\) by at most a constant.

For binary AND, \(L=1\) gives

\[
P(x,y)=a(x)q(y)+a(y)q(x)-q(x)q(y).
\]

The positive-side rational error is at most \(1/5\), because \(z\le1/9\) gives \(r\ge4/5\). Thus \(r(x)+r(y)-1\ge3/5\) in the positive-positive guard, and is at most \(-4/5\) whenever at least one input is negative. Clearing denominators preserves signs, but does not preserve this rational margin as a polynomial margin after amplitude normalization.

### 2.3 Lower bound for every non-affine law

A Boolean law is affine over \(\mathbb F_2\) exactly when every two-dimensional face restriction is affine. In algebraic normal form, vanishing of every second Boolean difference at every assignment forces all coefficients of degree at least two to vanish. Thus a non-affine \(h\) has a non-affine two-variable face. Fix the other coordinates at corresponding \(\pm1\) values. The eight non-affine binary laws are precisely AND under input sign flips and/or output negation. These transformations preserve polynomial degree and \(D_{\delta,2}\).

It remains to lower-bound AND. Let \(N\) be odd with \(N\le1/\delta\) and \(N\asymp1/\delta\). Substitute

\[
x=N^{-1}\sum_{i=1}^N z_i,\qquad
y=N^{-1}\sum_{i=1}^N w_i,\quad z_i,w_i\in\{-1,+1\}.
\]

Both magnitudes are at least \(1/N\ge\delta\). An AND sign polynomial becomes a sign polynomial for two independent majority functions without increasing degree. [Sherstov2013, Theorem 1.10, author PDF p. 6] gives threshold degree \(\Omega(\log N)\). Sherstov uses \(-1\) as true; input/output sign flips align conventions without altering degree. This proves \(\Omega(\log(1/\delta))\). Together with the upper bound it proves P1(2).

The finite-set hypothesis is respected: the reduction uses an actual finite Boolean cube. We do not apply a finite-set theorem directly to an infinite interval.

### 2.4 Fixed bounded margin: lower bound

Every nonconstant Boolean function has an edge on which its value changes. Fix the other \(n-1\) coordinates at \(\pm1\) along that edge. The univariate slice \(p\) obeys \(|p|\le1\) on \([-1,1]\), and opposite signs with magnitude at least \(\gamma\) at \(-\delta,+\delta\). The mean value theorem gives \(\xi\in(-\delta,\delta)\) with

\[
|p'(\xi)|\ge\gamma/\delta.
\]

Bernstein's interior polynomial inequality gives

\[
|p'(\xi)|\le d/\sqrt{1-\xi^2}
\le d/\sqrt{1-\delta^2},
\quad d\ge\frac{\gamma\sqrt{1-\delta^2}}{\delta}.
\]

See [KopotunPrymakShevchuk2018, Theorem 24.1, printed p. 56 / PDF p. 59]. This applies to projections and parity as well as AND. Non-affinity is unnecessary for the bounded-margin conclusion.

### 2.5 Fixed bounded margin: upper bound

Define the clipped ramp \(v_\delta(t)=\max(-1,\min(1,t/\delta))\), with Lipschitz constant \(1/\delta\). Jackson's theorem gives a degree-\(k\) polynomial \(u\) with uniform error at most \(C/(k\delta)\) on the whole interval. An inspected statement is [BizeulKlartag, Section 2.3, equation (35), PDF p. 12]; the classical kernel construction is in [KopotunPrymakShevchuk2018, Sections 20-21].

Choose error \(\eta\), and put \(r=u/(1+\eta)\). Then \(|r|\le1\) on \([-1,1]\), while on the guarded intervals it differs from the input sign by at most \(\epsilon=2\eta/(1+\eta)\). Applying \(H_h\) yields global amplitude at most one and guarded margin at least \(1-n\epsilon\). For fixed \(n,\gamma<1\), choose \(\eta\) with \(n\epsilon\le1-\gamma\) and \(k=O_{n,\gamma}(1/\delta)\). Total degree is at most \(nk\), proving P1(3).

At \(\gamma=1\), a nonconstant law is impossible: a polynomial bounded by one that equals \(+1\) on any positive open guard is identically \(+1\). This is why \(\gamma<1\) is explicit.

## 3. Finite regularity and normalized corner margins

**Proposition P2 (Taylor consequence).** Let \(h\) be non-affine. If \(F\in C^k\) realizes it on all local orthants, its entire \(k\)-jet at zero vanishes. Choose the least nonzero derivative of order at most \(k\) and apply [FiniteJet2026, Theorem 4.3]. Thus \(F(x)=o(\|x\|^k)\); for \(k=0\), \(F(0)=0\).

If \(F\in C^{k,\alpha}\), \(0<\alpha\le1\), and the Euclidean multilinear-operator norm of \(D^kF\) has Hölder seminorm at most \(H\) in a ball, then

\[
|F(x)|\le H\frac{\Gamma(\alpha+1)}{\Gamma(k+\alpha+1)}\|x\|^{k+\alpha}.
\]

For \(k=0\) this is the Hölder condition. For \(k\ge1\), write \(x=rv\), \(\|v\|=1\), and use integral Taylor remainder:

\[
|F(rv)|\le\frac{H}{(k-1)!}\int_0^r(r-t)^{k-1}t^\alpha dt
=H\frac{\Gamma(\alpha+1)}{\Gamma(k+\alpha+1)}r^{k+\alpha}.
\]

If every balanced corner \(\delta s\) has margin at least \(\gamma\), necessarily

\[
\gamma\le H\frac{\Gamma(\alpha+1)}{\Gamma(k+\alpha+1)}(\sqrt n\delta)^{k+\alpha}.
\]

The rate is attainable, with constants depending on dimension and a fixed cutoff, for every labeling. Choose a smooth one-sided angular cutoff \(\phi\) with \(0\le\phi\le1\), positive on \(t>0\), zero on \(t\le0\), and equal to one for \(t\ge\eta\), where \(0<\eta<1/\sqrt n\). On the unit sphere set

\[
A_h(\theta)=\sum_s h(s)\prod_i\phi(s_i\theta_i),\qquad
F_h(x)=\|x\|^{k+\alpha}A_h(x/\|x\|),\quad F_h(0)=0.
\]

Only one summand is active in an open orthant. The sphere function is smooth, with flat gluing on coordinate walls. Away from zero, \(D^jF_h=O(r^{k+\alpha-j})\) for \(j\le k\), yielding a \(C^k\) extension with zero \(k\)-jet. Its \(k\)-th derivative is homogeneous of degree \(\alpha\) and smooth on the sphere. For its Hölder bound, split pairs into distances comparable to the larger radius (use the size bound) and distances smaller than half that radius (integrate a gradient of size \(O(r^{\alpha-1})\)). Both give \(O(\|x-y\|^\alpha)\). Hence \(F_h\in C^{k,\alpha}\).

At \(\delta s\), angular factors equal one, so \(|F_h(\delta s)|=(\sqrt n\delta)^{k+\alpha}\). On the unit ball \(|F_h|\le1\). For \(\alpha=1\), non-affine \(h\) generally prevents \(C^{k+1}\) regularity. This uses standard homogeneous functions and cutoffs; it is not a claimed original construction. Binary AND already has the classical example

\[
F(x,y)=(x^2+y^2)^{k/2}\big(x+y-\sqrt{x^2+y^2}\big).
\]

It is \(C^{k,1}\), analytic away from the corner, and not \(C^{k+1}\) there. [Shapiro2007, equation (3.5) and Section 3.6] describes the first \(k\) vanishing derivatives. The homogeneity proof handles both odd and even \(k\).

## 4. Smooth and Denjoy-Carleman budgets

**Proposition P3 (associated-function consequence).** Let \(F\) be an exact smooth non-affine orthant realization, and suppose throughout \(B_R\)

\[
\|D^jF(x)\|_{\rm op}\le A B^j j! M_j\quad(j\ge0),
\]

with \(A,B\) fixed and \(M\) in the manuscript's factorial-out convention. Flatness and Taylor remainder give

\[
|F(x)|\le A(B\|x\|)^j M_j,\qquad
|F(x)|\le A h_M(B\|x\|),\quad h_M(t)=\inf_{j\ge0}M_jt^j.
\]

Thus \(\gamma\le A h_M(B\sqrt n\delta)\) at balanced corners. Coordinate partial-derivative bounds imply this operator estimate after replacing \(B\) by \(B\sqrt n\), using \(\|v\|_1\le\sqrt n\|v\|_2\). Do not silently equate the two norm conventions.

For Gevrey \(s>1\), \(M_j=(j!)^{s-1}\), optimizing \(j\) gives exponential-scale suppression in \(\delta^{-1/(s-1)}\), up to constants. This is standard associated-function machinery: [Rainer2022, Section 7.1, equation (7.2), Section 7.2, Example 7.1]. Matching optimal cutoffs for arbitrary weights needs stronger assumptions; [Rainer2022, Section 7.3] requires strong non-quasianalyticity. Ordinary non-quasianalyticity alone does not license those optimal estimates.

A fixed exact smooth score has margin decaying faster than every polynomial at the corner. This concerns spatial derivatives, not gradients with respect to learned weights, and proves no training-failure theorem. It cannot be applied to an analytic \(F_\delta\) correct only on \(D_{\delta,n}\), which need not be flat at zero.

## 5. Counterexamples

* Finite fitting: \((x+y+xy-1)/2\) fits AND at \(\pm1\) but is negative at sufficiently small positive-positive points.
* Magnitude dependence: \(x+y+xy\) is negative at \((t,-t)\) and positive at \((2t,-t/2)\) for every small positive \(t\).
* Nonsmooth exact interpretation: \(\min(x,y)=x-\operatorname{ReLU}(x-y)\) realizes AND; an affine skip plus one ReLU suffices.
* Analytic guarded AND: \(F_\varepsilon=x+y-\sqrt{x^2+y^2+\varepsilon^2}\) is analytic globally. For \(\varepsilon=\delta\), its signs are correct on \(D_{\delta,2}\), with positive margin at least \((2-\sqrt3)\delta\). It fails arbitrarily near the positive-positive corner.
* Analytic soft minimum: \(S_\beta=-\beta^{-1}\log(e^{-\beta x}+e^{-\beta y})\) obeys \(\min(x,y)-\log2/\beta\le S_\beta\le\min(x,y)\). For \(\beta=2\log2/\delta\), guarded margin is at least \(\delta/2\); Hessian norm is at most \(\beta/2\). Demanding fixed bounded output margin changes the budget.
* Flat smooth realization: one-sided products of \(e^{-1/t^2}\), zero for \(t\le0\), realize every law; balanced-corner log magnitude is \(-n/\delta^2\).
* Finite differentiability: the classical \(R_0^k\) family realizes AND with \(k\) derivatives and zero \(k\)-jet. Finite differentiability alone does not force parity.
* Removed corner: \(x+y+\sqrt{x^2+y^2}\) realizes OR on the punctured plane and is analytic there. Connectedness does not restore a missing corner.
* Scaling: multiplying a score by a positive constant preserves signs and changes margins and derivative norms. Unnormalized tradeoffs are meaningless.

## 6. Checker scope

**verify_candidates.py** checks all binary and ternary truth tables at Boolean representatives; affine counts and two-face witnesses; dyadic rational constructions at six widths with 34 coordinate values per width; magnitude-dependent and ReLU identities; and four soft-minimum choices. Universal correctness of the rational construction is proved in Section 2.2, not inferred from the grid. The checker does not establish arrangement proofs, lower-bound literature, Hölder estimates, learning behavior, or novelty.
