# Audit of the attached `Logical Complexes.tex` notes

## Bottom line

The notes are useful. They contain two ideas that survive almost exactly after the ambient algebra is clarified:

1. Boolean valuation vectors naturally live in an affine/vector geometry over \(\mathbf F_2\), where XOR is vector difference.
2. The observation that signs can disappear and a second boundary can cancel is correct for **formal simplicial chains over \(\mathbf F_2\)**.

The notes also reveal a stronger geometric structure not stated there: exact unfolding layers are **hypersimplices**, and the parent plus all one-coordinate distinctions is an affine simplex.

## What is correct or salvageable

### 1. XOR of Boolean points

For \(x,y\in\mathbf F_2^m\),
\[
x\Updownarrow y=x+y
\]
is the coordinatewise difference vector. Its Hamming weight is the scalar Hamming distance:
\[
d_H(x,y)=\mathrm{wt}(x\Updownarrow y).
\]
So the notes' repeated use of XOR as a geometric difference is sound after this wording change.

### 2. The points \(G,D,E,F\)

The notes use
\[
G=111,\quad D=110,\quad E=101,\quad F=011.
\]
Relative to \(G\), the three differences are
\[
G\Updownarrow D=001,\quad G\Updownarrow E=010,\quad G\Updownarrow F=100.
\]
They are a basis. Therefore the **four** points \(G,D,E,F\) are affinely independent and form a genuine tetrahedron.

This corrects the note's suggestion that three such points might already make a 3-simplex. Any three points in \(\mathbb R^3\) are coplanar; a tetrahedron needs four affinely independent points.

### 3. The special relation \(D\Updownarrow E=F\)

This is correct for the three-variable example:
\[
110\Updownarrow101=011.
\]
Indeed \(\{000,110,101,011\}\) is the even-parity two-dimensional subspace of \(\mathbf F_2^3\).

It is a low-arity coincidence, not a general law of one-flip layers. For \(m>3\), XOR of two one-flip children of \(1^m\) has Hamming weight two and normally leaves the one-flip layer.

### 4. The \(\partial^2=0\) intuition

The notes' cancellation intuition is valid after moving to a formal chain group. Over \(\mathbf F_2\), the simplicial boundary is
\[
d[v_0,\ldots,v_n]=\sum_i[v_0,\ldots,\widehat v_i,\ldots,v_n],
\]
with no visible signs because \(-1=+1\). Every codimension-two face occurs twice in \(d^2\), so it cancels.

The necessary correction is conceptual: the XOR/addition here is **addition of formal simplices in the chain group**, not XOR of the vertex labels themselves. The two additions may both be over \(\mathbf F_2\), but they act in different vector spaces.

## Stronger structure recovered from the notes

### Exact layers are hypersimplices

Starting from \(1^m\), the states reached by switching exactly \(k\) coordinates are
\[
L_k^{(m)}=\{x\in\{0,1\}^m:\mathrm{wt}(x)=m-k\}.
\]
Their convex hull is the hypersimplex
\[
\Delta(m,m-k)=\left\{x\in[0,1]^m:\sum_i x_i=m-k\right\}.
\]
Only the first and last nontrivial layers are simplices in general.

For \(m=4\) the layer geometry is:

**point -> tetrahedron -> octahedron -> tetrahedron -> point.**

This is a clean modern replacement for the notes' questions about planes, simplices, and apparently redundant Boolean points.

### Distinction histories form a simplex skeleton filtration

If a state is labeled by the subset \(S\subseteq[m]\) of coordinates that have been distinguished, then allowing all distinction sets of size at most \(r+1\) gives
\[
K_r=\operatorname{sk}_r\Delta^{m-1}.
\]
Thus successive differentiation has a canonical simplicial filtration even though each exact state layer is generally a hypersimplex rather than a simplex.

For the step \(K_{r-1}\hookrightarrow K_r\),
\[
H_q(K_r,K_{r-1};R)\cong
\begin{cases}
R^{\binom{m}{r+1}},&q=r,\\
0,&q\ne r.
\end{cases}
\]
The same groups are the homology of the mapping cone of the inclusion.

## What should not be carried forward literally

- Do not call the XOR vector itself a scalar distance; use its Hamming weight.
- Do not use a determinant of three position vectors to decide affine independence of four points. Use differences from one base point.
- Do not identify Boolean valuation vectors with simplicial chains.
- Do not treat conjunction of logical labels as the simplicial boundary.
- Do not infer that a collection of proper faces contains its filler.
- Do not infer symmetry from the existence of a homology cycle.

## Recommendation

The useful material from the notes should be retained as a short section in the new paper, but in the following repaired form:

1. valuation space \(\mathbf F_2^m\);
2. XOR as difference vector and Hamming weight as distance;
3. one-flip affine simplex theorem;
4. exact layers as hypersimplices;
5. chain complex over \(\mathbf F_2\) as a separate formal object;
6. cumulative distinction skeletons and their cone defects.

That is stronger, cleaner, and more general than the original notes while preserving the intuition that motivated them.
