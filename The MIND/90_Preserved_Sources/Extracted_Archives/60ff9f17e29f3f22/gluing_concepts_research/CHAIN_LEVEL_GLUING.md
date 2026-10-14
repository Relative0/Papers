# Chain-Level Gluing

## 1. The basic exact sequence

Let \(K=A\cup B\) be a finite simplicial complex and \(D=A\cap B\). For simplicial chains over a commutative coefficient ring, there is a short exact sequence of chain complexes
\[
0\longrightarrow C_\bullet(D)
\xrightarrow{\alpha}
C_\bullet(A)\oplus C_\bullet(B)
\xrightarrow{\beta}
C_\bullet(K)
\longrightarrow0,
\]
with
\[
\alpha(x)=(x,-x),\qquad \beta(a,b)=a+b.
\]
Over \(\mathbb F_2\), minus equals plus. The induced long exact sequence is Mayer–Vietoris:
\[
\cdots\to H_n(D)\to H_n(A)\oplus H_n(B)\to H_n(K)
\xrightarrow{\delta}H_{n-1}(D)\to\cdots.
\]

This is the right chain-level formalization of ordinary common-subcomplex gluing. It says exactly how duplicate overlap chains are identified.

## 2. Example A — two edges glued at a vertex

Let
\[
A=\Delta\{a,b\},\qquad B=\Delta\{b,c\},\qquad D=\Delta\{b\}.
\]
Then \(K=A\cup B\) is the path \(a-b-c\).

Over \(\mathbb F_2\):

- \(\dim C_1(A)=\dim C_1(B)=1\), \(C_1(D)=0\), \(\dim C_1(K)=2\);
- \(\dim C_0(A)=\dim C_0(B)=2\), \(\dim C_0(D)=1\), \(\dim C_0(K)=3\).

At degree 0 the injection sends
\[
b\mapsto (b,b),
\]
and the quotient identifies the two copies of \(b\). The computation in the package gives
\[
H_0(K;\mathbb F_2)\cong\mathbb F_2,\qquad H_1(K;\mathbb F_2)=0.
\]

### Recoverability

If the marked images of \(A\) and \(B\) are retained, the two original edges are trivially recoverable. From the bare path alone, the fact that it was *historically* built from these two particular pieces is extra provenance. Its intrinsic maximal-simplex decomposition happens to recover the edges here, but this coincidence fails in more general examples.

## 3. Example B — two filled triangles glued along an edge

Let
\[
A=\Delta\{a,b,c\},\qquad
B=\Delta\{b,c,d\},\qquad
D=\Delta\{b,c\}.
\]
Then \(K=A\cup B\) has facets \(abc\) and \(bcd\), so it is a triangulated disk.

The exact chain dimensions are:

| degree | \(C_k(D)\) | \(C_k(A)\oplus C_k(B)\) | \(C_k(K)\) |
|---:|---:|---:|---:|
| 2 | 0 | 2 | 2 |
| 1 | 1 | 6 | 5 |
| 0 | 2 | 6 | 4 |

The overlap edge \(bc\) is sent to the pair of its two copies, and the quotient identifies them. Likewise for the overlap vertices \(b,c\).

Every one of \(A,B,D,K\) is contractible. Thus the positive-degree groups in the Mayer–Vietoris sequence vanish. In degree zero, over \(\mathbb F_2\), the nontrivial part is explicitly
\[
0\longrightarrow H_0(D)\cong\mathbb F_2
\xrightarrow{\;1\mapsto(1,1)\;}
H_0(A)\oplus H_0(B)\cong\mathbb F_2^2
\xrightarrow{\;(x,y)\mapsto x+y\;}
H_0(K)\cong\mathbb F_2
\longrightarrow 0.
\]
The first map identifies the common connected component and the second quotients the two local component generators to the single global component. In reduced homology the entire sequence is zero. The package computes
\[
\beta(K)=(1,0,0).
\]

This example is useful because it shows a limit of homology: gluing can be mathematically nontrivial at the chain/incidence level while homology sees no obstruction at all.

## 4. A nontrivial Mayer–Vietoris connecting map

To see what the connecting morphism can detect, cover a simplicial circle \(S^1\) by two contractible arcs \(A\) and \(B\) whose intersection \(D\) consists of two disconnected vertices. In reduced homology,
\[
\widetilde H_1(A)=\widetilde H_1(B)=0,
\qquad
\widetilde H_0(D)\cong\mathbb F_2,
\qquad
\widetilde H_1(S^1)\cong\mathbb F_2.
\]
Exactness forces the connecting map
\[
\delta:\widetilde H_1(S^1)\longrightarrow\widetilde H_0(D)
\]
to be an isomorphism. The global cycle is created precisely because the overlap is disconnected.

This is a meaningful **interaction diagnostic**: the connecting map says that a global class is supported by the way local pieces overlap. It is still not a general notion of conceptual independence.

## 5. Relative homology

For \(A\subseteq K\), the relative groups \(H_*(K,A)\) measure homological structure added when passing from \(A\) to \(K\). In a gluing problem \(K=A\cup_D B\), relative excision often relates
\[
H_*(K,A)\cong H_*(B,D)
\]
under standard hypotheses. This is useful for answering “what does concept \(B\) contribute beyond the overlap \(D\)?”

The phrase should remain homological: a nonzero relative group certifies new topology, not automatically new semantic content.

## 6. Mapping cone viewpoint

The chain map
\[
C_\bullet(D)\xrightarrow{(i_*,-j_*)}C_\bullet(A)\oplus C_\bullet(B)
\]
has a mapping cone. Up to the usual homological equivalences, the cone packages the defect/attachment data of the union and produces the Mayer–Vietoris sequence. This gives a useful bridge to the project's existing mapping-cone/refinement-defect ideas in ProLT, but it should be imported only at the chain level where the hypotheses are explicit.

## 7. Homotopy pushout

For subcomplex inclusions, geometric realizations are cofibrations. Consequently the square
\[
|D|\to|A|,
\qquad
|D|\to|B|
\]
with pushout \(|A\cup_D B|\) is also a homotopy pushout. This lets one use homotopy-invariant tools rather than treating the union only combinatorially.

For arbitrary maps in the category of abstract simplicial complexes, however, categorical colimits can be more rigid than geometric intuition suggests. The safe statement is the subcomplex-inclusion case.

## 8. Splitting is too weak for independence

Over a field, any short exact sequence of vector spaces splits (noncanonically) degree by degree. Therefore a chain-level vector-space splitting of the Mayer–Vietoris sequence cannot, on its own, define “independent concepts.” A meaningful independence result would need a splitting compatible with boundaries **and** the chosen combinatorial/semantic structure, preferably canonically.

## 9. What chain invariants are worth tracking?

For each finite gluing experiment, record:

- dimensions and ranks of \(C_k\) and \(\partial_k\);
- Betti numbers and Euler characteristic;
- the overlap homology \(H_*(D)\);
- ranks of Mayer–Vietoris maps, especially connecting maps;
- relative groups \(H_*(K,A)\), \(H_*(K,B)\);
- whether the square is a strict pushout and/or homotopy pushout;
- whether any observed splitting is canonical or merely linear-algebraic.

These invariants diagnose how pieces interact topologically without pretending to solve the semantic factorization problem.
