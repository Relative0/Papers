"""Create a separate v0.5 from the reviewed v0.4 without editing prior versions."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
PREVIOUS = ROOT.parent / 'Manuscript Convergence 2026-09-29'
SOURCE = PREVIOUS / 'Observation_Refinement_Descent_and_Cone_Draft_v0.4.tex'
OUT = ROOT / 'Observation_Refinement_Descent_and_Cone_Draft_v0.5.tex'
CHANGES = []


def replace(text, old, new, why):
    count = text.count(old)
    assert count == 1, (why, count)
    CHANGES.append(why)
    return text.replace(old, new, 1)


def between(text, first, last, new, why):
    assert text.count(first) == text.count(last) == 1, why
    a = text.index(first)
    b = text.index(last, a)
    CHANGES.append(why)
    return text[:a] + new + '\n\n' + text[b:]


def main():
    text = SOURCE.read_text(encoding='utf-8')
    text = replace(text, 'Convergence draft v0.4 --- 29 September 2026',
                   'Referee-repair draft v0.5 --- 29 September 2026',
                   'Version the repaired manuscript separately')
    text = replace(text,
        '''Parts (i) and (iii) follow because choosing $S$ is equivalent to choosing the $k$ zero coordinates, or equivalently the $m-k$ one coordinates.  For (ii),''',
        '''Part (i) follows by choosing the $k$ zero coordinates.  For (iii),
the displayed intersection of the cube with the integer-sum hyperplane is a
bounded polytope.  If two coordinates of a point lie strictly between $0$
and $1$, perturb one upward and the other downward by a sufficiently small
amount; the point is not a vertex.  Exactly one fractional coordinate is
impossible because the coordinate sum is an integer.  Hence every vertex
is a $0$--$1$ vector with exactly $k$ zero coordinates, proving the hull
equality.  For (ii),''',
        'Supply the vertex proof for the hypersimplex equality')
    text = between(text,
        r'\begin{theorem}[Non-congruence of factorized unfolding]',
        r'\subsection{Boolean derivative interpretation}',
        r'''\begin{theorem}[Non-congruence of factorized unfolding]\label{thm:noncongruence}
Fix the arity $m=|A|\ge2$.  There is no Boolean-function operator
$\overline U:\mathsf B(A)\to\mathsf B(A)$ satisfying
\[
\overline U(\Pi(F))=U_{\mathrm{th}}(F)
\]
for every $m$-factor tuple $F\in\mathsf B(A)^m$.
\end{theorem}
\begin{proof}
The constant Boolean functions belong to $\mathsf B(A)$.  At the fixed
arity $m$, take
\[
 F=(0,1,1,\ldots,1),\qquad F'=(0,0,1,\ldots,1).
\]
Both conjunctions are the zero function.  Exactly one factor is false in
$F$, so $U_{\mathrm{th}}(F)=1$; exactly two are false in $F'$, so
$U_{\mathrm{th}}(F')=0$.  One operator on the conjunction cannot give both.
\end{proof}

For $m=1$, by contrast, $\Pi((f))=f$ and
$U_{\mathrm{th}}((f))=\neg f$; ordinary negation is such an operator.
Thus the failure of semantic descent begins at arity two.  For $m\ge2$,
either internal factorization/provenance is part of the concept, a canonical
normal form must be chosen, or the historical rule must be replaced by a
semantic operator.''',
        'Repair fixed-arity noncongruence theorem and one-factor exception')
    old = '''Here profile value $2$ means split.  To check the star example directly,
the available links for the missing pairs $\\{0_0,2_1\\}$ and
$\\{0_0,6_1\\}$ have homotopy type $S^1$; the third pair link and all
three triple links are contractible, and the four-core link is
$\\{0_1,2_0\\}\\simeq S^0$.'''
    new = r'''Here profile value $2$ means split.  The four-core link is
$\{0_1,2_0\}\simeq S^0$.  The three triple links, indexed by their
upper missing states $023$, $026$, and $036$, contain respective paths
\[
 A:2_0-4_1-0_1,\qquad B:2_0-5_1-0_1,\qquad
 C:2_0-3_0-1_0-1_1-0_1.
\]
All three triple links are contractible.  The $02$ edge link is the square
on bipartition $\{0_1,2_0\}\sqcup\{4_1,5_1\}$; the $03$ edge link is a
cone with apex $4_1$.  The $06$ edge link has maximal faces
\[
 [0_1,1_1],\ [0_1,5_1],\ [1_0,1_1],\
 [1_0,3_0,6_0],\ [2_0,3_0,6_0],\
 [2_0,5_0,5_1],\ [2_0,5_0,6_0].
\]
Collapsing its triangle ears leaves the cycle
$0_1-1_1-1_0-3_0-2_0-5_1-0_1$.
Orient $A,B,C$ from $2_0$ to $0_1$.  With the missing-core deletion
signs, their horizontal boundary has components $B-A$ in the $02$ link,
$A-C$ in the $03$ link, and $C-B$ in the $06$ link.  The first traverses
the $02$ square once; hence $d^2:\mathbb Z\to\mathbb Z^2$ has a unit
coordinate and is primitive.  This gives a signed witness independent of
the certificate's rank calculation.'''
    text = replace(text, old, new, 'Add explicit signed seven-state path witness')
    text = between(text, r'\begin{definition}[Pair-good cover]',
        r'\begin{theorem}[Observation--Refinement Descent and Cone Theorem]',
        r'''\begin{definition}[Pair-good subcomplex cover]
Let $Y\subseteq X$ be a finite simplicial pair.  A finite family
$\mathcal U=\{U_i\}_{i\in I}$ of subcomplexes covering $X$ is
\emph{good relative to $Y$} if every nonempty intersection
$U_\sigma=\bigcap_{i\in\sigma}U_i$ is contractible and every nonempty
$U_\sigma\cap Y$ is contractible.  The restricted cover
$\mathcal U|_Y=\{U_i\cap Y\}_{i\in I}$ is indexed after deleting its
empty members.  A finite subcomplex cover of $Y$ is \emph{good} if all
its nonempty intersections are contractible.  The subcomplex condition
is part of these definitions, not a consequence of intersection
contractibility alone.
\end{definition}''',
        'Make the sufficient finite-subcomplex cover class explicit')
    text = replace(text,
        '''Let $Y\\subseteq X$ be a pair of spaces for which the relative nerve theorem applies (for example, a finite simplicial pair covered by suitable subcomplexes, or a paracompact pair with numerable good covers).  Let $\\mathcal U$ be a finite cover of $X$ good relative to $Y$.  Let $\\mathcal V$ be a finite good cover of $Y$ refining $\\mathcal U|_Y$.  Choose any refinement map''',
        '''Let $Y\\subseteq X$ be a finite simplicial pair.  Let $\\mathcal U$
be a finite pair-good subcomplex cover of $X$ and let $\\mathcal V$ be
a finite good subcomplex cover of $Y$ refining $\\mathcal U|_Y$.
Delete empty indexed members before taking nerves.  Thus all three covers
$\\mathcal U$, $\\mathcal U|_Y$, and $\\mathcal V$ lie in the
functorial subcomplex-cover nerve theorem.  Choose any refinement map''',
        'Require functorial nerve hypotheses for all three displayed covers')
    text = replace(text,
        '''intersections are admissible objects of the chosen site, and the displayed
families are covers in that site.  For a sheaf''',
        '''intersections are admissible objects of a site with inclusion
morphisms for the displayed subcomplexes, their pullbacks are represented
by these intersections, and the displayed families are covers in that
site.  Take the sheaf and cosheaf values in a category admitting the
finite limits and colimits used below, for example abelian groups.
For a sheaf''',
        'Specify inclusion-site pullbacks and target categories for descent')
    text = replace(text,
        '''Part (a) is Lemma~\\ref{lem:contiguity}.  For (b), both $\\mathcal V$ and $\\mathcal U|_Y$ are good covers of $Y$.  The functorial/relative form of the nerve theorem~\\cite{BauerEtAl2023,Ramras2026} identifies their nerves with $Y$ and identifies the refinement map with the identity of $Y$ up to homotopy.  Hence $N(\\rho)$ is a homotopy equivalence.''',
        '''Part (a) is Lemma~\\ref{lem:contiguity}.  For (b), the finite
subcomplex-cover nerve theorem~\\cite{BauerEtAl2023,Ramras2026}
supplies compatible equivalences for $\\mathcal V$ and
$\\mathcal U|_Y$ with $Y$.  Functoriality for the refinement map
identifies $N(\\rho)$ with the identity of $Y$ through these
equivalences.  Hence $N(\\rho)$ is a homotopy equivalence.''',
        'Match the nerve proof to the strengthened cover hypothesis')
    text = replace(text,
        r'\item \emph{Did the underlying support or compatibility structure change?}  This is answered by cone/relative homology.',
        r'\item \emph{Does the chosen map fail to be a homology equivalence?}  Cone/relative homology detects this failure; its vanishing alone does not detect every change of support or homotopy type.',
        'Narrow homological-detection wording')
    text = replace(text,
        '''The candidate contribution is the explicit observation-product recognition,
the coarse-edge-link matching formula, the transitivity restrictions on
interacting cores, and the sharp integral positive and negative examples.''',
        '''The candidate contribution is the explicit observation-product recognition,
the coarse-edge-link matching formula, the transitivity restrictions on
interacting cores, and the sharp integral positive and negative examples.
The matching deletion step is a direct specialization of the obstruction
decomposition above; identifying its product-edge link with a suspension
of the coarse link is the model-specific calculation.  The interaction
first page, filtration-width collapse, and two-column kernel/cokernel
sequence use standard filtered-chain and mapping-cone algebra after the
available-link diagram has been identified.  These tools are not claimed
as independent new constructions.''',
        'State precisely which matching and interaction steps are standard')
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    assert len(labels) == len(set(labels))
    refs = re.findall(r'\\(?:eqref|ref)\{([^}]+)\}', text)
    assert set(refs) <= set(labels), set(refs) - set(labels)
    cites = {k.strip() for group in re.findall(r'\\cite\{([^}]+)\}', text) for k in group.split(',')}
    keys = set(re.findall(r'\\bibitem\{([^}]+)\}', text))
    assert cites <= keys, cites - keys
    OUT.write_text(text, encoding='utf-8')
    receipt = {
        'source': str(SOURCE),
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'output': OUT.name,
        'output_sha256': hashlib.sha256(OUT.read_bytes()).hexdigest(),
        'changes': CHANGES,
        'labels': len(labels),
        'citations_used': len(cites),
        'unresolved_source_refs': [],
    }
    (ROOT / 'REPAIR_RECEIPT.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
    print(json.dumps({'changes': len(CHANGES), 'labels': len(labels), 'citations_used': len(cites)}))


if __name__ == '__main__':
    main()
