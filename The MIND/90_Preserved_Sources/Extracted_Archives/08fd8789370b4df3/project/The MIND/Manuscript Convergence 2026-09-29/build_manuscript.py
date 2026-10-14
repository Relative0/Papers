"""Create v0.4 from frozen v0.3 and two reviewed, unmerged sections.

Inputs are read-only. Every replacement asserts its intended target.
The new file is a convergence draft, not a submission candidate.
"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent/'Transferred Research/MIND_Unfolding_Project_Consolidated_Handoff_2026-09-29'
GATE = ROOT.parent/'Interaction Core Gate 2026-09-29'
SOURCE = BASE/'01_CURRENT_MANUSCRIPT/Observation_Refinement_Descent_and_Cone_Draft_v0.3.tex'
OUT = ROOT/'Observation_Refinement_Descent_and_Cone_Draft_v0.4.tex'
changes=[]


def replace(text, old, new, label):
    assert text.count(old)==1, (label,text.count(old))
    changes.append(label)
    return text.replace(old,new,1)


def region(text, start, end, new, label):
    assert text.count(start)==1 and text.count(end)==1,label
    a=text.index(start); z=text.index(end,a)
    changes.append(label)
    return text[:a]+new+'\n\n'+text[z:]


def main():
    text=SOURCE.read_text(encoding='utf-8')
    matching=(BASE/'01_CURRENT_MANUSCRIPT/MANUSCRIPT_REVISION_SECTION.tex').read_text(encoding='utf-8')
    interaction=(GATE/'MANUSCRIPT_INTERACTION_SECTION.tex').read_text(encoding='utf-8')
    text=replace(text,'Research draft v0.3 --- 29 September 2026',
                 'Convergence draft v0.4 --- 29 September 2026','Versioned new draft; frozen v0.3 unchanged')
    text=replace(text,r'\large Carrier Splitting, Descent, Mapping-Cone Defects, and Boolean Unfolding Complexes',
                 r'\large Carrier Splitting, Interaction-Core Homology, and Descent','Subtitle reflects integrated mathematical core')
    text=replace(text,r'\subsection{Why the signs disappear over $\Ftwo$}',
                 r'\subsection{Why the signs disappear over \texorpdfstring{$\Ftwo$}{F2}}',
                 'Supply plain-text PDF bookmark for mathematical heading')
    text=region(text,r'\begin{abstract}',r'\end{abstract}',r'''\begin{abstract}
A 2015 proposal for concept unfolding combined Boolean distinction, simplicial
boundary, and local-to-global reconstruction.  We separate these operations
and study one precise refinement model: a new Boolean observation splits the
states of a finite observational poset $Q$, producing an induced subposet
$Q^\psi\subseteq Q\times\{0<1\}$ with projection $\pi$.

Carrier splitting factors through a homotopy-neutral split completion followed
by order thinning.  In weighted height at most two its cone has a complete
integral rooted-incidence classification.  At arbitrary height, a two-colour
missing-copy model identifies the obstruction.  If the exclusive inversion
graph is a matching, cone homology is the direct sum of coarse edge-link
reduced homology shifted by two, with no torsion-freeness assumption.

Beyond matching, a filtration by mixed-core size has first page given by
available-link homology.  When cores have at most three vertices, an explicit
chain mapping cone computes the defect and the spectral sequence collapses at
$E^2$, with integral extensions retained.  Maximum-degree-two exclusive graphs
stabilize at $E^3$; an eight-state $K_{2,2}$ example proves this bound sharp.
A seven-state star rules out unconditional $E^2$ collapse for forests, Ferrers
graphs, and chordal-bipartite graphs.  An all-exclusive star family further
shows that interaction can create torsion even when all local links have
torsion-free homology.

The Boolean historical reconstruction and cover/descent framework are retained
as separate interpretations.  The general cofiber, obstruction-complex,
spectral-sequence, nerve, and sheaf machinery is classical.  The contribution
claimed here is the explicit observation-product specialization and its
positive classifications and integral failure boundaries; publication priority
for the exact specialization remains subject to review.''','Update abstract without broad novelty claims')
    marker=r'\section{Historical operator: what survives and what does not}'
    conventions=r'''\subsection{Conventions and result hierarchy}
Finite observational posets are assumed nonempty.  An order complex includes
the empty face.  Its augmented chain complex is denoted $\widetilde C_*$;
in particular $\widetilde H_{-1}(\Delta\varnothing;R)=R$.
Joins and suspensions of empty links use this simplicial convention; the
formal $(-1)$-sphere has no vertices.  Ordinary homology is zero in negative
degrees.  A coefficient ring is commutative with identity.

For a chain map $f:A_*\to B_*$, use
$\Cone(f)_n=B_n\oplus A_{n-1}$ and
$d(b,a)=(d_Bb+f(a),-d_Aa)$.
For a map of spaces or simplicial complexes, $\Cone(f)$ denotes its homotopy
cofiber and its homology is explicitly reduced.  For nonempty source and
target these conventions agree under the usual chain comparison.  A simplicial
map that repeats an image vertex sends that oriented simplex to zero on
normalized chains.  A shift $C[k]_n=C_{n-k}$ has differential $(-1)^k d_C$.

The main mathematical results are organized as follows.
\begin{enumerate}[label=(\arabic*)]
\item Theorem~\ref{thm:split-factorization} converts a changing observational
carrier into a neutral split completion followed by order thinning.
\item Theorem~\ref{thm:carrier-graph} gives the exact integral low-height result;
Theorem~\ref{thm:exclusive-matching} gives the all-height coarse-edge-link formula.
\item Theorems~\ref{thm:two-column-interaction} and
\ref{thm:degree-two-interaction} describe controlled overlap, including the
sharp distinction between $E^2$ and $E^3$ collapse.
\item Theorem~\ref{thm:main} treats cover refinement and descent separately.
It reconstructs data on the support actually covered; restriction from $X$ to
a proper subspace $Y$ need not preserve or uniquely extend global sections.
\end{enumerate}
The historical Boolean and simplex-skeleton constructions motivate the model;
they are not a claim to new general Boolean, polyhedral, or sheaf theory.

'''
    text=replace(text,marker,conventions+marker,'Explicit augmented, cone, shift, and support conventions')

    # The low-height incidence graph is not the exclusive inversion graph.
    a=text.index(r'\subsection{Exact low-height classification}')
    z=text.index(r'\subsection{Sharpness beyond weighted height two}',a)
    low=text[a:z].replace(r'G_\psi',r'\mathcal D_\psi')
    low=low.replace('Parallel graph edges are allowed.',
                    'Parallel graph edges are allowed.  Here a rooted forest means a forest\nwith exactly one formal root in each graph component.  This incidence graph\n$\\mathcal D_\\psi$ is different from the exclusive inversion graph introduced later.')
    proof_start=low.index(r'\begin{proof}',low.index(r'\label{thm:carrier-graph}'))
    proof_end=low.index(r'\end{proof}',proof_start)+len(r'\end{proof}')
    low=low[:proof_start]+r'''\begin{proof}
The relative complex has only $C_2\to C_1$, since all vertices are retained
and the split completion has dimension at most two.  A deleted triangle of
bit type $100$ or $110$ has two inversion edges with opposite boundary signs;
a triangle of type $010$ or $101$ has one.  Consequently its matrix is the
oriented incidence matrix of $\mathcal D_\psi$ with formal-root rows deleted.
Each graph component contains at most one root, because triangles cannot
connect different coarse components.  Relative graph homology therefore gives
$H_2=\mathbb Z^{\beta_1(\mathcal D_\psi)}$ and
$H_1=\mathbb Z^{c_0(\mathcal D_\psi)}$.  Incidence matrices and their row
submatrices are totally unimodular.

Vanishing of both groups is exactly the rooted-forest condition.  In a rooted
tree with an edge, choose a nonroot leaf.  Its inversion edge occurs in just
one remaining deleted triangle and in no retained triangle, so the pair is
an elementary simplicial collapse.  Iterating leaf removal deletes every
relative edge and triangle.  Conversely a relative collapse gives a homotopy
equivalence and hence vanishing relative homology.  Finally the split-completion
projection is a homotopy equivalence, so two-out-of-three gives the statement
about $\Delta\pi$.  The free groups displayed above also show the equivalence
with acyclicity over every field.
\end{proof}'''+low[proof_end:]
    low=low.replace('The exact height-two theorem for one-bit thinning is proved\nin the companion structural-computation manuscript.',
                    'The same height-two one-bit result is developed in the companion\norder-thinning manuscript~\\cite{DroncheffThinning2026}; the proof above makes\nthe transfer used here self-contained.')
    text=text[:a]+low+text[z:]
    changes.append('Disambiguate incidence graph and supply self-contained low-height proof')
    text=replace(text,'Companion results show that one-bit',
                 r'Companion results~\cite{DroncheffThinning2026} show that one-bit','Attribute unintegrated height-three companion results')

    matching=matching[matching.index(r'\section'):]
    matching=matching.replace('finite poset $R$.  Make the','nonempty finite poset $R$.  Make the')
    matching=matching.replace('The atom crosscut is a\nfull simplex',
                             'By the classical crosscut theorem~\\cite{Bjorner1995}, the atom crosscut is a\nfull simplex')
    matching=matching.replace('Under the matching hypothesis only $r=2$ occurs, so the spectral sequence\ncollapses immediately and recovers Theorem~\\ref{thm:exclusive-matching}.',
        'Under the matching hypothesis only $r=2$ occurs, so the spectral sequence\ncollapses immediately and recovers Theorem~\\ref{thm:exclusive-matching}.')
    # The original unmerged filtration presentation is now supplied more precisely
    # by the next section; retain its label as a forward-reference target.
    a=matching.index(r'\subsection{Beyond matching: the interaction-core filtration}')
    z=matching.index(r'\begin{remark}[Priority boundary]',a)
    matching=matching[:a]+r'''The matching hypothesis is sufficient, not necessary: the same proof applies
whenever there is no mixed three-vertex core.  Section~\ref{sec:interaction-cores}
makes this criterion and the nonmatching interaction maps explicit.

'''+matching[z:]
    # Explicit T2 derivation, rather than an unexplained shift.
    matching=matching.replace('The long exact sequences\nof triples together with simplicial excision give',
        'Since $H_*(K,K_P)=H_*(K,K_Z)=0$, the triple $(K,K_P,L)$,\nsimplicial excision for $U=K_P\\cup K_Z$, and the triple $(K,U,K_Z)$ give\n$H_n(K,L)\\cong H_n(K_P,L)\\cong H_n(U,K_Z)\\cong H_{n+1}(K,U)$.\nThus')
    matching=matching.replace('Hence the relative chain complex splits\nas',
        'Reorienting each simplex with the two core vertices first gives an even\nchain shift.  Hence the relative chain complex splits\nas')
    empty_theorem=r'''\begin{proposition}[Empty-exclusive-graph neutrality]
\label{prop:empty-exclusive}
If $E_\psi=\varnothing$, then $\Delta\pi$ is a homotopy equivalence.
\end{proposition}
\begin{proof}
Set $b(s)=1$ exactly when some $p\in P$ satisfies $p\le s$.
This isotone choice takes an available value at every state: it is $1$ on $P$
and cannot be $1$ on $Z$ without an exclusive edge.  The section
$r(s)=(s,b(s))$ obeys $\pi r=\mathrm{id}$.
On $Q^\psi$, the map $c(s,a)=(s,\max\{a,b(s)\})$ is available and isotone,
with $\mathrm{id}\le c\ge r\pi$.  Comparable poset maps are homotopic,
so $r$ is a homotopy inverse.
\end{proof}

'''
    matching=matching.replace(r'\begin{theorem}[Exclusive-Inversion Matching Theorem]',empty_theorem+r'\begin{theorem}[Exclusive-Inversion Matching Theorem]')
    interaction=interaction[interaction.index(r'\section'):]
    interaction=interaction.replace('In every cycle component of length at least six the cone contribution is',
        'In every cycle component of length at least six the cone contribution is')
    interaction=interaction.replace('The first differential is the\nsigned sum',
        'The first differential is the\nsigned sum')
    interaction=interaction.replace('The filtration is finite.\nOnly columns',
        'The filtration is finite and exhaustive.  The abutment is the associated\ngraded of homology, so integral extension data may remain.\nOnly columns')
    interaction=interaction.replace('For a $C_4$ whose two pairs are comparable, write the core order',
        'For a $C_4$ component whose two pairs are comparable, restrict to its\nrelative chain summand and write the core order')
    # Add all nine links so the sharpness proof can be checked without scripts.
    key='The four-core link consists of $b_1,x_0$; all triple links are\ncontractible; only the edge $ay$ has a nontrivial available link, a circle\nup to homotopy.'
    expanded=r'''The four-core link consists of $b_1,x_0$.  The triple links $abx$ and
$bxy$ are cones with apex $y'_1$ and $a'_0$, respectively; the links $aby$
and $axy$ are the two paths displayed below.  The edge links $ax$, $by$,
and $bx$ are cones, with apex $y'_1$, $a'_0$, and either of those vertices.
The remaining edge link $ay$ has maximal simplices
\[
 [a_1,b_1,w_1],\quad[v_0,x_0,y_0],\quad
 [a_1,v_1],\quad[v_0,v_1],\quad[w_0,w_1],\quad[w_0,y_0].
\]
Collapsing its two triangle ears leaves a cycle.  Thus the stated first-page
groups follow directly from all nine available links.'''
    assert key in interaction
    interaction=interaction.replace(key,expanded)
    interaction=interaction.replace('where $hk=0$.  The only possible higher differential is',r'''where $h,k$ are the signed core-deletion inclusions and $hk=0$.
In triple order $(abx,aby,axy,bxy)$, the signs of $k$ are $(-,+,-,+)$,
while $h(abx)=bx-ax$, $h(aby)=by-ay$, $h(axy)=ax-ay$, and
$h(bxy)=bx-by$, each term meaning its corresponding inclusion.
The only possible higher differential is''')
    interaction=interaction.replace('Their difference generates the sole loop in the $ay$ link.  Therefore',
        'Give each path orientation from $x_0$ to $b_1$.  In the $ay$ component\nof the signed zigzag, the first path minus the second traverses the loop once;\nthe other edge components are cycles in contractible links.  Therefore')
    star_end='These are explicit counterexamples, not global minimality claims.'
    interaction=interaction.replace(star_end,r'''Here profile value $2$ means split.  To check the star example directly,
the available links for the missing pairs $\{0_0,2_1\}$ and
$\{0_0,6_1\}$ have homotopy type $S^1$; the third pair link and all
three triple links are contractible, and the four-core link is
$\{0_1,2_0\}\simeq S^0$.
For the abutment, write $T=Q\setminus\{0\}$ and $C=\{1,4,5\}$.
The complex $\Delta T$ is contractible: its two maximal-element lower ideals
are cones whose intersection is the lower ideal of $3$.
The complex $\Delta C$ is an edge and an isolated point.
In a star profile $Q=\{p\}\oplus T$, with $p$ one-only, $C$ split, and
$T\setminus C$ zero-only, the refined complex is the union of
$\Delta((T\times\{0\})\cup(C\times\{1\}))$ and the cone
$\Delta((\{p\}\times\{1\})\cup(C\times\{1\}))$.
The first piece retracts to $\Delta T$, and the intersection is $\Delta C$.
The homotopy-pushout description consequently gives
$\widetilde H_n(\Cone(\Delta\pi))\cong H_{n-1}(\Delta T,\Delta C)$.
Here this is $\mathbb Z$ only at $n=2$; the sole possible $d^2$ must be a
primitive injection.  The supplementary certificate records all link matrices
and signed chains.  These are explicit counterexamples, not global minimality claims.''')
    horn=r'''\subsection{Whole-relation Horn closure is neutral}
\begin{proposition}
If the nonempty refined Boolean relation is closed under coordinatewise meet,
then $\Delta\pi$ is a homotopy equivalence.  The dual statement holds for
coordinatewise join closure.
\end{proposition}
\begin{proof}
Finiteness and meet closure give a minimum in the refined relation.
Its coordinate projection is again meet closed and nonempty, so also has a
minimum.  Both order complexes are contractible.  Join closure gives maxima.
\end{proof}
The hypothesis concerns the whole realized refined relation; it is not merely
a closure assumption on a selected subset of observations.  This is an
elementary application of closure-system topology, not a new Horn theorem.

'''
    interaction=interaction.replace(r'\begin{remark}[Scope and priority]',horn+r'\begin{remark}[Scope and priority]')
    text=replace(text,r'\section{Cover refinement and canonical homology maps}',
        matching+'\n\n'+interaction+'\n\n'+r'\section{Cover refinement and canonical homology maps}',
        'Integrate matching and interaction sections with proof and boundary clarifications')

    old=r'''\item if the cover members are admissible objects of the chosen site (for example, open sets for an ordinary sheaf) and $\mathcal F$ is a sheaf of sets or abelian groups on $X$, then compatible local sections on either cover reconstruct a unique global section; refinement changes the presentation of the local data but not the reconstructed global section;
\item dually, under the same site/admissibility convention, if $\mathcal G$ is a cosheaf, the global assembled object is the colimit of its local intersection diagram, and this assembly is compatible with refinement.'''
    new=r'''\item assume additionally that $X$, $Y$, the cover members, and their
intersections are admissible objects of the chosen site, and the displayed
families are covers in that site.  For a sheaf $\mathcal F$, compatible data
on $\mathcal U$ reconstruct $\mathcal F(X)$; compatible data on
$\mathcal U|_Y$ or $\mathcal V$ reconstruct $\mathcal F(Y)$.
Refinement between the latter two covers preserves that section on $Y$.
No unique extension from $Y$ to $X$ is asserted;
\item under the same site hypothesis, a cosheaf $\mathcal G$ is assembled
as the colimit of the intersection diagram on each covered support: the
colimits are $\mathcal G(X)$ and $\mathcal G(Y)$, respectively.
Refinement on $Y$ preserves its colimit; inclusion induces the comparison
$\mathcal G(Y)\to\mathcal G(X)$, which need not be an isomorphism.'''
    text=replace(text,old,new,'Correct sheaf and cosheaf support error in original theorem')
    old=r'''For (e), assuming the cover belongs to the site on which $\mathcal F$ is defined, the sheaf axiom identifies global sections with compatible local families: $\mathcal F(X)$ is the equalizer of the first two \v{C}ech restriction maps.  Since both covers represent the same global object, refinement transports compatible families without changing their unique glue.  Part (f) is the dual cosheaf statement: $\mathcal G(X)$ is the colimit of the local intersection diagram, and refinement induces the canonical comparison maps between such colimits.'''
    new=r'''For (e), apply the sheaf axiom separately on each support: compatible
families on a cover of $S$ are the equalizer describing $\mathcal F(S)$,
for $S=X$ or $S=Y$.  The covers $\mathcal U|_Y$ and $\mathcal V$ cover
the same $Y$, so their gluing maps agree with refinement.  Restriction
$\mathcal F(X)\to\mathcal F(Y)$ is a separate map and need not be bijective.
Part (f) is the dual cosheaf colimit statement, again on each support separately.'''
    text=replace(text,old,new,'Correct descent proof rather than silently identifying X and Y')
    marker=r'\subsection{What the theorem means for unfolding}'
    warning=r'''\begin{example}[Restriction is not unique extension]
Take the discrete space $X=\{a,b\}$, $Y=\{a\}$, and the sheaf of
integer-valued functions.  Singleton covers satisfy the stated good-cover
conditions.  Data on $Y$ determine an element of $\mathbb Z$, whereas
$\mathcal F(X)=\mathbb Z^2$; restriction is the projection onto the first
coordinate.  A section on $Y$ therefore has many extensions to $X$.
This distinguishes descent on a fixed support from an extension problem.
\end{example}

'''
    text=replace(text,marker,warning+marker,'Retain explicit counterexample to old descent wording')
    text=replace(text,'the current paper handles refinement through covers, relative cone defects, and descent, while the order-thinning paper handles a special same-carrier refinement regime with sharper combinatorial recognition.',
        'the present paper treats changing carriers, matching and interacting cone defects, and cover-level descent, while the companion order-thinning paper develops the same-carrier incidence theorem and its separate sharpness results.',
        'Update stale scope description after integration')
    text=region(text,r'\section{Priority and novelty position}',r'\section{Next theorem targets}',r'''\section{Priority and novelty position}
The standard ingredients include Boolean/Hamming and hypersimplex geometry,
chain cones, beat-point reductions, relative nerve theorems, sheaf descent,
poset-fiber methods, and filtered-complex spectral sequences.
For the cover $X_0=V(K)\setminus M_0$, $X_1=V(K)\setminus M_1$, with
$A=X_0\cap X_1=V(L)$, each $\Lambda_S$ is precisely the available-vertex
obstruction complex $\operatorname{St}(S,A)$ of
Chach\'olski--Jin--Scolamiero--Tombari~\cite{ChacholskiEtAl2021}, with
our augmented empty-face convention.  Their published Corollary~7.2 treats
several outside vertices and Theorem~8.6 controls the homotopy fibers of the
vertex-cover inclusion through these obstruction complexes.

The Bj\"orner--Wachs--Welker fiber theorem~\cite{BjornerWachsWelker2005}
gives decompositions under explicit fiber-connectivity or null-attachment
hypotheses.  Here the attachment maps are retained and may produce torsion
or higher differentials.  This is a narrower exact computation, not a
replacement for general fiber theory.  Likewise, Ferrers graph resolutions,
graph independence complexes, and unweighted biclique complexes do not by
themselves identify the available-link diagram used here.

The candidate contribution is the explicit observation-product recognition,
the coarse-edge-link matching formula, the transitivity restrictions on
interacting cores, and the sharp integral positive and negative examples.
The historical audit and descent framework provide interpretation rather
than priority for classical machinery.  No claim of first discovery of the
exact specialization is made solely from its absence in a targeted search.
The separate convergence report records the primary-source comparison and
the remaining publication-level judgment.''','Conservative theorem-level priority positioning')
    text=region(text,r'\section{Next theorem targets}',r'\section{Conclusion}',r'''\section{Next theorem target}
The matching case, the two-column interaction case, and the degree-two
$E^3$ bound are now established.  Unrestricted $E^2$ collapse in the
proposed graph classes is false, so it is no longer an open target.

\begin{question}[Integral secondary maps in a four-cycle]
For each integer $k\ge2$, can an exclusive $K_{2,2}$ profile with
torsion-free available-link homology realize
$d^2:\mathbb Z\to\mathbb Z$ as multiplication by $k$?
Alternatively, what restrictions does the product-poset geometry impose
on the possible integral secondary maps?
\end{question}
This isolates interaction-created torsion at the smallest exclusive graph
that supports a four-core.  The unit example above does not resolve it.
The smallest possible higher-differential or interaction-torsion realization
also remains open globally; induced-restriction minimality is weaker.''','Replace settled research prompts by precise remaining question')
    text=region(text,r'\section{Conclusion}',r'\appendix',r'''\section{Conclusion}
Observation refinement is a transformation between representations, not a
chain boundary.  Carrier splitting has a neutral-completion factorization,
an exact low-height incidence description, and an all-height matching
edge-link formula.  Beyond matching, available-link inclusions form the
interaction complex.  Two core columns give an exact chain cone and
$E^2$ collapse; degree two permits a genuine $d^2$ and only the sharp
$E^3$ bound in general.  Interaction can create integral torsion even from
torsion-free local links.

Cover refinement and descent answer a separate question on the support
actually covered.  The historical Boolean reconstruction, local-to-global
data, and structural homology therefore remain distinct.  The mathematical
claims of this draft are the stated specialized formulas and failure
boundaries; general topological machinery and publication priority are not
silently strengthened.''','Conclusion reflects final scope and retained limits')
    repro=r'''\subsection{Carrier-splitting and interaction verification}
The transferred matching gate records 3,242 integral matching cases through
four coarse states, 1,707 product-link checks over $\mathbb F_2$, and 639
additional nonempty matching five-state checks over $\mathbb F_2$.
The interaction gate enumerates 90,201 naturally labelled poset/profile
cases through five states over $\mathbb F_2$, plus 5,000 seeded six-state
trials.  Coarse-poset isomorphism postprocessing yields 87 poset types and
16,761 profiles; exclusive graphs give 70 colour-preserving types with
isolated exclusive vertices retained.  These are different counts of the
same bounded exhaustive evidence, not additional independent cases.

The main interaction run makes 435 selected integral comparisons, supplemented
by nine exact local models, signed integer certificates for both $d^2$
witnesses, and a separate 32-state torsion construction.  The latter checks
181 available links, 31 coarse edge links, and the proved reduced interaction
matrix by Smith normal form, not the whole doubled pair.  The projective-plane
triangulation has facets
\[
012,013,024,035,045,125,134,145,234,235.
\]
An additional 20,000 targeted $K_{2,2}$ trials locate the sharp secondary
differential; these trials are not an exhaustive or uniform isomorphism sample.
All coefficients, seeds, scripts, and integer certificates are recorded in
the accompanying interaction-gate reports.  Computations support the proofs
and do not establish global minimality or publication priority.

'''
    text=replace(text,r'\begin{thebibliography}{99}',repro+r'\begin{thebibliography}{99}','Add coefficient-accurate integrated reproducibility record')
    bib=(BASE/'02_LATEST_HIGHER_DIMENSIONAL_GATE/MANUSCRIPT_BIBLIOGRAPHY_ADDITIONS.tex').read_text(encoding='utf-8')
    bib=bib[bib.index(r'\bibitem{ChacholskiEtAl2021}'):bib.index(r'\bibitem{DefantWilliams2023}')]
    bib+=r'''\bibitem{DroncheffThinning2026}
B.~Theory,
\emph{Binary Order Thinning of Finite Posets: Homology, Collapses, and Sharp Limits},
unpublished companion research manuscript, 27 September 2026, reviewed v3.
The archived title page uses the name Brian Theory.

'''
    text=replace(text,r'\end{thebibliography}',bib+r'\end{thebibliography}','Add cited matching references and identify archived companion accurately')
    standard_cites={
        'This lemma is standard.  In particular, Leit\\~ao\'s 2026 framework':
            'This lemma is standard.  In particular, Leit\\~ao\'s 2026 framework~\\cite{Leitao2026}',
        'The functorial/relative form of the nerve theorem identifies':
            'The functorial/relative form of the nerve theorem~\\cite{BauerEtAl2023,Ramras2026} identifies',
        'the sheaf axiom separately on each support:':
            'the sheaf axiom~\\cite{Curry2013} separately on each support:',
        'Part (iv) is the standard dimension and vertex description of the hypersimplex;':
            'Part (iv) is the standard dimension and vertex description of the hypersimplex~\\cite{GelfandEtAlHypersimplex};',
        'The mapping cone of an inclusion computes the relative homology of the pair.':
            'The mapping cone of an inclusion computes the relative homology of the pair~\\cite{Hatcher2002}.',
        'There is a finite convergent spectral sequence\n':
            'The finite-filtration construction~\\cite{Weibel1994} gives a convergent spectral sequence\n'
    }
    for old,new in standard_cites.items():
        text=replace(text,old,new,'Add direct attribution: '+new.split('cite{')[-1].split('}')[0])
    crosscut=r'''\bibitem{Bjorner1995}
A.~Bj\"orner,
``Topological methods,''
in \emph{Handbook of Combinatorics}, Vol.~2,
R.~L.~Graham, M.~Gr\"otschel, and L.~Lov\'asz (eds.),
Elsevier, 1995, pp.~1819--1872.

'''
    text=replace(text,r'\end{thebibliography}',crosscut+r'\end{thebibliography}','Add classical crosscut reference')
    nerve=r'''\bibitem{BauerEtAl2023}
U.~Bauer, M.~Kerber, F.~Roll, and A.~Rolle,
``A unified view on the functorial nerve theorem and its variations,''
\emph{Expositiones Mathematicae} 41(4) (2023), 125503.
\href{https://doi.org/10.1016/j.exmath.2023.04.005}{doi:10.1016/j.exmath.2023.04.005}.

'''
    text=replace(text,r'\end{thebibliography}',nerve+r'\end{thebibliography}','Add directly relevant functorial nerve reference')
    text=replace(text,r'\emph{Discrete \& Computational Geometry} 63 (2020).',r'\emph{Discrete \& Computational Geometry} 63 (2020), 549--559.','Complete Fernandez--Minian bibliographic record')
    text=replace(text,'''homotopy-colimit methods.  A realistic next target is not another universal forest
theorem, but a classification of higher-dimensional inversion complexes under
additional structural hypotheses on $Q$ and on the split profile $(A_0,A_1)$.''','''homotopy-colimit methods.  The next two sections give all-height results under
matching and interaction-core hypotheses, together with explicit obstructions
to stronger graph-class conclusions.''','Replace obsolete transition by integrated section roadmap')
    # No duplicate labels, unresolved source-level refs, or missing bibliography keys.
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    assert len(labels)==len(set(labels)), 'duplicate labels'
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    assert set(refs)<=set(labels),set(refs)-set(labels)
    cites={k.strip() for group in re.findall(r'\\cite\{([^}]+)\}',text) for k in group.split(',')}
    keys=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    assert cites<=keys,cites-keys
    OUT.write_text(text,encoding='utf-8')
    receipt={'input_sha256':{str(p.relative_to(ROOT.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [SOURCE,BASE/'01_CURRENT_MANUSCRIPT/MANUSCRIPT_REVISION_SECTION.tex',GATE/'MANUSCRIPT_INTERACTION_SECTION.tex']},'output':OUT.name,'output_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'changes':changes,'labels':len(labels),'citations_used':len(cites),'unresolved_source_refs':[]}
    (ROOT/'INTEGRATION_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print(json.dumps({'output':OUT.name,'changes':len(changes),'labels':len(labels),'citations_used':len(cites)}))


if __name__=='__main__': main()
