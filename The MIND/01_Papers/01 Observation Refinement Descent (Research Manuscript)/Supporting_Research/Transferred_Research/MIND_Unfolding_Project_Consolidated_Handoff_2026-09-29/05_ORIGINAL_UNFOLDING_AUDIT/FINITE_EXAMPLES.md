# Finite Examples
## Exact 4-attribute prototype for successive differentiation

This document gives one fully explicit finite example satisfying the requested checklist:

1. define \(K_k\);
2. write chain groups;
3. compute boundary matrices;
4. compute homology;
5. define \(U_k\);
6. test \(dU_k=U_kd\);
7. compute induced homology maps;
8. compute relative homology / mapping cones;
9. test reconstruction by gluing.

All homology is over \(\mathbf F_2\), so orientations/signs do not affect the displayed matrices.

The four abstract attributes are

\[
a,b,c,d.
\]

No psychological interpretation is assumed. One may read a simplex as a jointly compatible/observed group of attributes.

---

# 1. Stage \(K_0\): a partially differentiated concept

Let \(K_0\) have vertices

\[
\{a,b,c\}
\]

and edges

\[
ab,\;bc.
\]

Thus \(K_0\) is the path

\[
a-b-c.
\]

## Chain groups

\[
C_1(K_0)=\mathbf F_2\langle ab,bc\rangle,
\]

\[
C_0(K_0)=\mathbf F_2\langle a,b,c\rangle.
\]

There are no 2-simplices.

## Boundary matrix

Using row basis \((a,b,c)\) and column basis \((ab,bc)\),

\[
\partial^{K_0}_1=
\begin{pmatrix}
1&0\\
1&1\\
0&1
\end{pmatrix}.
\]

Its rank is 2.

Therefore

\[
\dim H_0(K_0)=3-2=1,
\]

\[
\dim H_1(K_0)=2-2=0.
\]

So

\[
H_0(K_0)\cong\mathbf F_2,
\qquad
H_1(K_0)=0.
\]

---

# 2. Stage \(K_1\): a relation closes into a cycle

Add vertex \(d\) and edges

\[
cd,\;da.
\]

Thus

\[
K_1=a-b-c-d-a
\]

is a four-cycle.

## Chain groups

\[
C_1(K_1)
=\mathbf F_2\langle ab,bc,cd,da\rangle,
\]

\[
C_0(K_1)
=\mathbf F_2\langle a,b,c,d\rangle.
\]

## Boundary matrix

With row basis \((a,b,c,d)\), column basis \((ab,bc,cd,da)\),

\[
\partial^{K_1}_1=
\begin{pmatrix}
1&0&0&1\\
1&1&0&0\\
0&1&1&0\\
0&0&1&1
\end{pmatrix}.
\]

The rank is 3.

Hence

\[
H_0(K_1)\cong\mathbf F_2,
\]

and

\[
\dim H_1(K_1)=4-3=1.
\]

A generator is

\[
z=ab+bc+cd+da,
\]

because every vertex occurs twice in its boundary:

\[
\partial z=0.
\]

There is no \(C_2\), so \(z\) is not a boundary.

Thus

\[
H_1(K_1)\cong\mathbf F_2.
\]

### Interpretation

A new global cycle has appeared even though every new datum was local. This is an exact example of a structural feature introduced by an observation/refinement step.

---

# 3. The first unfolding map \(U_0:K_0\hookrightarrow K_1\)

Take the simplicial inclusion

\[
u_0:K_0\hookrightarrow K_1.
\]

It induces

\[
U_0=C_*(u_0).
\]

On vertices:

\[
a\mapsto a,\quad b\mapsto b,\quad c\mapsto c.
\]

On edges:

\[
ab\mapsto ab,\qquad bc\mapsto bc.
\]

## Chain-map equation

Since \(u_0\) is simplicial,

\[
\partial^{K_1}U_0=U_0\partial^{K_0}.
\]

The script checks this matrix equality exactly.

## Induced homology map

In degree zero,

\[
(U_0)_*:H_0(K_0)\to H_0(K_1)
\]

is an isomorphism because both complexes are connected.

In degree one,

\[
(U_0)_*:0\to\mathbf F_2
\]

is the unique zero map. The new cycle is born at this stage; it is not inherited from \(K_0\).

---

# 4. Relative homology of the first step

Consider

\[
H_*(K_1,K_0).
\]

Modulo \(K_0\), the relative chain groups are

\[
C_1(K_1,K_0)=\mathbf F_2\langle cd,da\rangle,
\]

\[
C_0(K_1,K_0)=\mathbf F_2\langle d\rangle.
\]

Both relative edges have boundary \(d\), because their other endpoints lie in \(K_0\). Hence

\[
\partial^{\rm rel}_1=
\begin{pmatrix}
1&1
\end{pmatrix}.
\]

Its rank is 1, so

\[
H_1(K_1,K_0)\cong\mathbf F_2,
\qquad
H_0(K_1,K_0)=0.
\]

This relative class is represented by

\[
cd+da.
\]

When combined with the path \(a-b-c\) already present in \(K_0\), it closes the new loop.

---

# 5. Mapping cone of \(U_0\)

For the chain inclusion

\[
U_0:C_*(K_0)\to C_*(K_1),
\]

one obtains

\[
H_n(\operatorname{Cone}(U_0))\cong H_n(K_1,K_0).
\]

Thus

\[
H_1(\operatorname{Cone}(U_0))\cong\mathbf F_2,
\]

and the other relevant cone homology groups vanish.

The cone therefore records exactly the new one-dimensional structure introduced at stage 1.

---

# 6. Stage \(K_2\): higher-order relations fill the loop

Now add the diagonal \(ac\) and two 2-simplices

\[
abc,\qquad acd.
\]

Thus \(K_2\) is a triangulated disk:

\[
K_2=\Delta(abc)\cup_{ac}\Delta(acd).
\]

## Chain groups

\[
C_2(K_2)
=\mathbf F_2\langle abc,acd\rangle,
\]

\[
C_1(K_2)
=\mathbf F_2\langle ab,bc,cd,da,ac\rangle,
\]

\[
C_0(K_2)
=\mathbf F_2\langle a,b,c,d\rangle.
\]

## Degree-one boundary matrix

With rows \((a,b,c,d)\) and columns \((ab,bc,cd,da,ac)\),

\[
\partial^{K_2}_1=
\begin{pmatrix}
1&0&0&1&1\\
1&1&0&0&0\\
0&1&1&0&1\\
0&0&1&1&0
\end{pmatrix}.
\]

Its rank is 3.

## Degree-two boundary matrix

With edge rows \((ab,bc,cd,da,ac)\) and triangle columns \((abc,acd)\),

\[
\partial^{K_2}_2=
\begin{pmatrix}
1&0\\
1&0\\
0&1\\
0&1\\
1&1
\end{pmatrix}.
\]

Its rank is 2.

Hence

\[
\beta_0=4-3=1,
\]

\[
\beta_1=5-3-2=0,
\]

\[
\beta_2=2-2=0.
\]

Therefore

\[
H_0(K_2)\cong\mathbf F_2,
\qquad
H_1(K_2)=H_2(K_2)=0.
\]

The former cycle is now a boundary:

\[
\partial(abc+acd)
=ab+bc+cd+da.
\]

The diagonal \(ac\) cancels because it occurs twice.

---

# 7. The second unfolding map \(U_1:K_1\hookrightarrow K_2\)

Again use the simplicial inclusion.

The chain-map equation

\[
\partial^{K_2}U_1=U_1\partial^{K_1}
\]

is verified exactly by the script.

## Induced homology map

Degree zero:

\[
(U_1)_*:H_0(K_1)\to H_0(K_2)
\]

is an isomorphism.

Degree one:

\[
(U_1)_*:H_1(K_1)\to H_1(K_2)=0
\]

kills the unique loop class. Explicitly,

\[
z=ab+bc+cd+da
\]

maps to

\[
z=\partial(abc+acd)
\]

inside \(K_2\).

This is a clean example of a topological feature disappearing under added higher-order information.

---

# 8. Relative homology of the second step

Modulo \(K_1\), the only new 1-simplex is \(ac\) and the two new 2-simplices are \(abc,acd\):

\[
C_2(K_2,K_1)=\mathbf F_2^2,
\]

\[
C_1(K_2,K_1)=\mathbf F_2\langle ac\rangle.
\]

Both triangle boundaries reduce to \(ac\) in the quotient, so

\[
\partial^{\rm rel}_2=
\begin{pmatrix}
1&1
\end{pmatrix}.
\]

Therefore

\[
H_2(K_2,K_1)\cong\mathbf F_2,
\]

\[
H_1(K_2,K_1)=0.
\]

The generator is represented by

\[
abc+acd.
\]

The long exact sequence of the pair contains the connecting map

\[
H_2(K_2,K_1)\longrightarrow H_1(K_1),
\]

and here both spaces are one-dimensional. The relative 2-class maps to the cycle that gets filled.

---

# 9. Mapping cone of \(U_1\)

Again

\[
H_n(\operatorname{Cone}(U_1))\cong H_n(K_2,K_1).
\]

Thus

\[
H_2(\operatorname{Cone}(U_1))\cong\mathbf F_2,
\]

with the other relevant groups zero.

This degree shift is informative: the second step does not create a surviving 2-hole. It introduces a relative 2-dimensional filler whose boundary kills the previous 1-cycle.

---

# 10. Persistence interpretation

The degree-one persistence module is

\[
0=H_1(K_0)
\longrightarrow
H_1(K_1)\cong\mathbf F_2
\longrightarrow
H_1(K_2)=0.
\]

There is one degree-one interval born at stage 1 and dying at stage 2.

This demonstrates why persistence can be a useful language for successive differentiation:

- a newly distinguished relation can create a global topological feature;
- later higher-order compatibility can explain/fill that feature;
- persistence separates transient from stable structure.

One should not infer a psychological meaning from interval length without an empirical observation model.

---

# 11. Reconstruction by gluing

## Exact gluing of \(K_2\)

Let

\[
T_1=\Delta(abc),
\qquad
T_2=\Delta(acd).
\]

Their intersection is

\[
T_1\cap T_2=\Delta(ac).
\]

The pushout/union

\[
T_1\cup_{\Delta(ac)}T_2
\]

is exactly \(K_2\).

Thus the global concept is reconstructed from two local pieces **because the common overlap is retained**.

## Nerve of this cover

The cover \(\{T_1,T_2\}\) has nerve consisting of two vertices joined by an edge, since the intersection is nonempty. Both pieces and their intersection are contractible, so it is a good cover. The nerve is contractible, matching the homotopy type of the disk \(K_2\).

## Gluing the 1-cycle

Cover \(K_1\) by its four edge subcomplexes

\[
E_{ab},E_{bc},E_{cd},E_{da}.
\]

Adjacent edge complexes meet at vertices; opposite ones do not. The nerve of this good cover is itself a four-cycle. Hence the nerve theorem recovers

\[
K_1\simeq S^1.
\]

---

# 12. Why the thesis's naive face reconstruction fails

Suppose one is given the three edge faces

\[
ab,\quad bc,\quad ac.
\]

They are compatible as the boundary of a triangle. But they occur in both:

1. the hollow cycle \(\partial\Delta^2\), and
2. the filled simplex \(\Delta^2\).

Therefore the data do not determine whether \(abc\) exists.

This is the exact obstruction to treating "glue all faces" as an automatic inverse to unfolding.

Recovery requires an additional rule such as:

- every 3-clique is filled (flag complex);
- a parent provenance label;
- a designated horn filler;
- an intersection/colimit diagram that explicitly contains the higher simplex;
- a semantic condition declaring triple compatibility.

---

# 13. Symmetry counterexample computation

The script also checks two complexes/graphs.

## Symmetric but no 1-homology

A filled triangle has

\[
|\operatorname{Aut}|=6,
\qquad
\beta_1=0.
\]

## 1-homology but no nontrivial automorphisms

Take triangle \(a-b-c-a\), add leaf \(p\) at \(a\), and attach path \(b-q-r\). The graph has

\[
\beta_1=1,
\]

but exhaustive permutation checking gives

\[
|\operatorname{Aut}|=1.
\]

Therefore homology and symmetry cannot be identified.

---

# 14. Checklist result

| Required item | Prototype result |
|---|---|
| define \(K_k\) | \(K_0\) path, \(K_1\) cycle, \(K_2\) triangulated disk |
| chain groups | written explicitly above |
| boundary matrices | all displayed |
| homology | \((1,0)\), \((1,1)\), \((1,0,0)\) Betti profiles |
| define \(U_k\) | simplicial inclusions |
| test \(dU=Ud\) | exact matrix verification passes |
| induced homology | H0 isomorphisms; H1 born then killed |
| relative/cone | \(H_1(K_1,K_0)=\mathbf F_2\); \(H_2(K_2,K_1)=\mathbf F_2\) |
| gluing | exact pushout along \(ac\); good-cover nerves verified conceptually |

The exact machine-readable results are in `finite_complex_results.json`.
