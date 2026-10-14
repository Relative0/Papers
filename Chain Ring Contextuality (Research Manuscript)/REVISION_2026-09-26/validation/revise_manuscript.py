"""Apply the bounded audit revision to a preserved manuscript copy."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / '01_SOURCE_PACKAGE_FROM_PORTFOLIO_20260921/source_package/main.tex'
t = SOURCE.read_text(encoding='utf-8')

def replace(old, new):
    global t
    if t.count(old) != 1:
        raise ValueError(f'Expected exactly one occurrence: {old[:100]}')
    t = t.replace(old, new)

replace(r'\usepackage{microtype,url,hyperref}', r'\usepackage{microtype,url,hyperref,placeins}')
replace(r'\author{Brian Theory\thanks{Research draft. Author metadata and venue remain to be finalized.}}',
        r'\author{Brian Theory\\\small B-Theory}')
replace(r'\date{Research draft, 19 September 2026}', r'\date{26 September 2026}')
replace('using all primitive projective local bases and nonzero-amplitude support.',
        'using all primitive projective local bases, setting-indexed outcomes and nonzero-amplitude support.')
replace('with complete rank-one analysis and unrestricted invertible corrections,',
        'with a complete joint covector basis and unrestricted invertible corrections,')
replace('Tensor choice, preparation closure and a conditional symbolic Boolean interface delimit the interpretation.',
        'For primitive resources, maximal coding and universal exact raw teleportation coincide. Tensor choice and preparation closure delimit the interpretation.')
replace('Nonzero Smith rank detects whether a Hardy obstruction is available.',
        'At least two nonzero Smith factors are necessary and sufficient for a Hardy obstruction.')
replace('The contribution is the classification and the comparison under matched contracts.',
        'The contribution is the complete chain-ring classification and the comparison of contextuality, exact orbit coding and raw-vector teleportation through related Smith invariants under explicit contracts.')
replace('The proofs are self-contained. The accompanying priority ledger distinguishes a proof from a claim to precedence: a bounded primary-source review found close ingredients and different-context results, but does not certify that no equivalent theorem exists. The scalar-extension appendix connects the results to Boolean correspondence matrices without making either companion manuscript a dependency of the main theorems.',
        'The proofs are self-contained. The source comparison below identifies established ingredients and the hypotheses that distinguish the present tasks. It makes no claim of historical firstness. A standalone computational supplement supplies finite checks with their exact scope; an optional Boolean-interface note is separate from the article and is not a dependency of its results.')
replace('That distinction matters for comparisons with single-system modal Kochen--Specker arguments',
        'That distinction matters for comparisons with modal noncontextuality and free-will arguments')
replace(r'\cite{Byrne2021,Honold2009}', r'\cite{HonoldLandjev2000,Byrne2021}')
replace('complete nine-row rank-one analyzer', 'complete nine-row covector analyzer')

comparison = r'''

The matrix-spanning ingredient is classical: nonsingular-summand results go back to Wolfson and Zelinsky, and Henriksen proves the stronger statement that every square matrix of size greater than one over a unital ring is a sum of three units \cite{Zelinsky1954,Henriksen1974}. Lemma~\ref{lem:span} supplies a short proof sufficient for our use, followed by residue-basis lifting. Neither this spanning fact nor the existence of modal protocols is asserted as a new general result.

Finite-chain-ring coding also uses module invariants, but its optimization problem must be distinguished. Feng et al.\ study a stochastic channel $Y=AX+BE$ with random transfer and error matrices, deriving capacity results under specified distributions \cite{Feng2014}. Here a sender controls $U$ in $UM$ for a fixed resource $M$, and a single complete joint basis readout must identify the message at every supported outcome. A direct consequence of the former channel definition makes the distinction concrete: if $A$ is uniform in $\GL_d(K)$ and noise is absent, then $AUM$ has the same distribution for every $U\in\GL_d(K)$. This observation is our comparison of the two tasks, not a claim made in that source about the present theorem.

\begin{table}[ht]\centering\small
\begin{tabular}{>{\raggedright\arraybackslash}p{.19\linewidth}>{\raggedright\arraybackslash}p{.25\linewidth}>{\raggedright\arraybackslash}p{.43\linewidth}}
\toprule
Source and domain & Admissible objects & Operations, readout and conclusion\\\midrule
Modal theory \cite{Schumacher2010,Schumacher2012}; fields & Nonzero state vectors; composite vector spaces & Reversible linear maps and basis effects; nonzero contraction gives possibility. Includes finite-field coding and teleportation examples.\\[3pt]
Ring computation \cite{deBeaudrap2014}; commutative rings & Generic vectors whose coordinates generate the unit ideal & Model-dependent algebraic transformations and outcome rules; this admissibility excludes our nonprimitive separator.\\[3pt]
Chain-ring codes \cite{HonoldLandjev2000,Byrne2021} & Submodules and their module types & Code equivalence, geometry and enumeration; no fixed-resource joint support readout or raw teleportation task.\\[3pt]
Matrix channels \cite{Feng2014}; chain rings & Input matrices in a prescribed ambient module & Random $A,B,E$ in $Y=AX+BE$; stochastic decoding and capacity, rather than a controlled orbit with disjoint nonzero supports.\\[3pt]
This article; chain rings & Every nonzero static matrix, including nonprimitive ones & All local bases for support; full $\GL_d(K)$ encoders and one complete joint decoder for exact coding; complete covector analysis and invertible corrections for exact raw recovery. Conclusions: Smith trichotomy, $dh$ messages, and invertibility criterion.\\
\bottomrule
\end{tabular}
\caption{Comparison by scalar domain, admissibility and task. The support hierarchy itself is the established global-section hierarchy \cite{AbramskyBrandenburger2011}. Theorem~\ref{thm:teleport} also applies to finite commutative local rings that are not chain rings.}\label{tab:prior}
\end{table}
'''
replace(r'\section{Scalar, state and measurement contracts}', comparison + '\n' + r'\FloatBarrier' + '\n' + r'\section{Scalar, state and measurement contracts}')
replace(r'\cite{Byrne2021}. We write', r'\cite{HonoldLandjev2000,Byrne2021}. We write')
replace('Its residue $\\bar N$ is well-defined: the ambiguity lies in $(\\pi^{s-a})$, which is contained in $J$. Thus $h=\\rank_k\\bar N$.',
        r'Its residue $\bar N$ is well-defined: entrywise, the ambiguity lies in $\operatorname{Ann}(\pi^a)=(\pi^{s-a})\subseteq J$ (and is zero when $a=0$). Thus $h=\rank_k\bar N$. In contrast, $\bar M$ is zero whenever $a>0$; its rank is then not the leading multiplicity.')
replace('complete joint rank-one effect basis;', 'complete basis of primitive joint covectors;')

overview = r'''

\subsection{Resource map and a worked comparison}
Table~\ref{tab:map} previews the consequences of Theorems~\ref{thm:trichotomy}, \ref{thm:code} and~\ref{thm:teleport} for square resources. Primitivity of $M$, viewed as a vector of entries, is equivalent to $a=0$.
\begin{table}[ht]\centering\small
\begin{tabular}{ccl}
\toprule
Smith region & Orbit messages & Support and raw teleportation\\\midrule
$r=1$ & $d$ & Local; singular for $d\geq2$\\
$r\geq2,\ h=1$ & $d$ & Logical, not strong; singular\\
$2\leq h<d$ & $dh$ & Strong; singular\\
$h=d,\ a>0$ & $d^2$ & Strong; nonprimitive, singular\\
$h=d,\ a=0$ & $d^2$ & Strong; invertible, universally teleporting\\\bottomrule
\end{tabular}
\caption{Square resources under the stated contracts, $d\geq2$. Zero is excluded.}\label{tab:map}
\end{table}

For $A=\A$, compare the four resources in Table~\ref{tab:examples}. In $M=\diag(u,u)=uI_2$, a choice of leading preimage is $N=I_2$, so $a=1$ and $h=2$ even though $\bar M=0$. All four orbit messages remain distinguishable, but the nonzero input $(u^3,0)^T$ is annihilated by $M$ and cannot be universally recovered. By contrast, $\diag(1,u^2)$ is primitive and has two nonzero factors, but only one leading factor; it has a Hardy obstruction and also a global assignment. These examples distinguish $r$, $h$ and invertibility without changing the scalar ring.
\begin{table}[ht]\centering\small
\begin{tabular}{lccclcc}
\toprule
$M$ over $A$ & $r$ & $a$ & $h$ & Support & Messages & Teleports\\\midrule
$\diag(1,0)$ & 1 & 0 & 1 & Local & 2 & No\\
$\diag(1,u^2)$ & 2 & 0 & 1 & Logical, not strong & 2 & No\\
$\diag(u,u)$ & 2 & 1 & 2 & Strong & 4 & No\\
$I_2$ & 2 & 0 & 2 & Strong & 4 & Yes\\\bottomrule
\end{tabular}
\caption{A worked comparison over one chain ring. Teleportation means universal exact raw-vector recovery.}\label{tab:examples}
\end{table}
'''
replace(r'\section{Complete-basis contextuality}', overview + '\n' + r'\section{Complete-basis contextuality}')
replace('Index outcomes by $0,1$. The supported seed $(F_A=0,F_B=0)$ forces $X_B=1$, then $C_A=0$, and then $F_B=1$, a contradiction.',
        r'''Index outcomes by $0,1$. The forcing chain from the supported seed is
\[
(F_A=0,F_B=0)\ \Longrightarrow\ X_B=1
\ \Longrightarrow\ C_A=0\ \Longrightarrow\ F_B=1,
\]
a contradiction. Each implication excludes an outcome using, successively, the zero entries in $FDX^T$, $CDX^T$ and $CDF^T$.''')
replace('Factoring out $\\pi^a$, each selected contraction is a product of units plus terms in the radical, hence is a unit.',
        'In the divided matrix, each selected contraction is a product of units plus terms in the radical, hence is a unit.')
replace('At each forcing step, the forced row has zero contraction with every added coordinate outcome.',
        'The embedded matrices are block diagonal. At each forcing step, the already selected row is supported only in the first two coordinates and therefore has zero contraction with every added coordinate outcome on the other side. No additional outcome can escape the forcing chain.')
replace(r'\section{Exact orbit coding and teleportation}\label{sec:tasks}',
        r'\section{Exact orbit coding and teleportation}\label{sec:tasks}' + '\n' +
        r'The following classical spanning fact is included with a constructive proof; stronger units-generation results are available in \cite{Zelinsky1954,Henriksen1974}.')
replace('Every orbit codeword has a nonzero leading residue. An invertible joint decoder preserves this fact. Exact decoding forces supports for different messages to be disjoint; their nonzero leading residue vectors are therefore independent. Hence their number is at most $dh$.',
        r'''Each row of $X\bar N$ belongs to the $h$-dimensional row space of $\bar N$, and all such rows can be chosen independently, proving $\dim_kV=dh$. Put $v_i=\operatorname{vec}(U_iN)$ and let $D\in\GL_{d^2}(K)$ be a proposed decoder. The vectors $\bar v_i$ and $\bar D\bar v_i$ are nonzero. If a coordinate of $Dv_i$ has nonzero residue, it is a unit, and multiplication by $\pi^a\ne0$ cannot kill it. Thus
\[
\operatorname{supp}(\bar D\bar v_i)
\subseteq\operatorname{supp}(\pi^aDv_i).
\]
Exact decoding requires the supports on the right to be pairwise disjoint. Consequently the nonzero field vectors on the left have disjoint supports and are linearly independent. They lie in the $dh$-dimensional space $\bar D\operatorname{vec}(V)$, giving the upper bound. The reverse support inclusion is neither asserted nor needed.''')
replace(r'\begin{theorem}[Universal raw teleportation]', r'''A joint effect is a primitive covector
\[
e:K^d\otimes_K K^d\longrightarrow K,
\qquad E_{ij}=e(e_i\otimes e_j),
\]
where the first factor holds the input and the second Alice's share of the resource. A complete analysis is a basis of $d^2$ such covectors. Its analysis matrix has rows $\operatorname{vec}(E)^T$ and must be invertible. This is different from requiring an individual reshape $E$ to have matrix rank one: $E$ may be invertible and need not represent a decomposable local effect. For $M=\sum_{j,k}M_{jk}e_j\otimes e_k$, contraction gives
\[
(T_ex)_k=\sum_{i,j}E_{ij}x_iM_{jk},\qquad T_e=M^TE^T.
\]
The branch label is communicated to Bob, who applies a fixed correction for that label.

\begin{theorem}[Universal raw teleportation]''')
replace('with complete rank-one analysis and unrestricted invertible corrections is possible',
        'with a complete joint covector basis and unrestricted invertible corrections is possible')
replace('Fix vectorization so that the branch labeled by the reshaped joint effect $E$ transfers the input by $T=M^TE^T$.',
        'Use the contraction convention above, so a branch with reshape $E$ has transfer $T=M^TE^T$.')
replace('The analyzer existence step extends the explicitly constructed dimension-two and dimension-eight analyzers in the supplied research. It is a residue-lifting corollary of elementary matrix algebra.',
        'The analyzer existence step is a residue-lifting corollary of the classical spanning fact. It requires both invertibility of each reshape and invertibility of the full analysis matrix.')
replace('The smallest example is $\\varepsilon I_2$ over $\\F_2[\\varepsilon]/(\\varepsilon^2)$. This resource is nonprimitive. Restricting preparation to primitive vectors excludes this particular separator and must be stated explicitly.',
        r'''The smallest example is $\varepsilon I_2$ over $\F_2[\varepsilon]/(\varepsilon^2)$. The role of nonprimitivity is exact:
\begin{corollary}[Primitive-resource boundary]\label{cor:primitive}
For a primitive $M\in\Mat_d(K)$ over a finite commutative chain ring, under the stated contracts,
\[
N_{\max}=d^2\quad\Longleftrightarrow\quad M\text{ invertible}
\quad\Longleftrightarrow\quad\text{universal exact raw teleportation}.
\]
\end{corollary}
\begin{proof}
Primitivity gives $a=0$. By Theorem~\ref{thm:code}, maximal coding is equivalent to $h=d$, so all Smith factors are units. Apply Theorem~\ref{thm:teleport}.
\end{proof}
Thus the maximal-coding/nonteleportation separation requires nonprimitive resources and does not occur in the generic state class of \cite{deBeaudrap2014}. This does not equate strong contextuality with teleportation for primitive resources: $2\leq h<d$ is still possible when $d>2$.''')
start = t.index('In one audited restricted bipartite construction,')
end = t.index(r'\subsection{A boundary on the number of settings}', start)
t = t[:start] + t[end:]
replace(r'\begin{theorem}\label{thm:two}', r'\begin{theorem}[Absence of strong contextuality with two settings]\label{thm:two}')

start = t.index(r'\section{Finite verification and reproducibility}')
end = t.index(r'\section{Discussion}', start)
t = t[:start] + r'''\section{Finite verification and reproducibility}\label{sec:verification}
The proofs establish the general statements. The standalone supplement contains a separate checker developed for the September 2026 audit and rerun for this revision. It uses only the Python standard library. It is not the earlier historical runner, whose dependencies are absent from the original article package. The current evidence claims refer only to the files and commands in this supplement.

The support checker enumerates primitive rays, complete bases and exact contraction tables. Forbidden outcome pairs become binary clauses; implication-graph reachability decides global assignments and whether each supported event extends. Smith data are computed afterward for comparison, not used to decide support type. Identical support tables are cached. For the binary field these decisions are also checked by direct assignment enumeration.

\begin{center}\small
\begin{tabular}{p{.27\linewidth}p{.61\linewidth}}
\toprule
Check & Coverage and limitation\\\midrule
Direct support & All $22{,}170$ nonzero $2\times2$ resources over $\F_2,\F_3,\F_4$, $\F_2[u]/(u^2)$, $\F_2[u]/(u^3)$, $\F_3[u]/(u^2)$, and $\mathbb Z/4,\mathbb Z/8,\mathbb Z/9$; zero disagreements.\\[3pt]
Length-four support & Fourteen nonzero Smith representatives and 24 deterministic sampled resources over $A=\A$, each using all 192 local bases; not all $65{,}535$ nonzero resources.\\[3pt]
Hardy and analyzers & 36 ring/exponent Hardy cases; 28 analyzer configurations, checking each reshape and the complete analysis matrix, plus correction identities for one invertible resource per configuration.\\[3pt]
Coding & 52 explicit encoder/decoder certificates across seven rings, including all fourteen nonzero $A$ Smith representatives. These certify achievability; the general upper bound is analytic.\\[3pt]
Binary coding optimum & All 15 nonzero $2\times2$ binary resources, all $20{,}160$ invertible joint decoders per resource, and all disjoint-support subsets of each decoded orbit.\\[3pt]
Two-setting boundary & All 255 nonzero three-party binary tensors for a representative pair of distinct settings per party; the arbitrary-party and ring statements are analytic.\\\bottomrule
\end{tabular}
\end{center}

\input{smith_table}

Table~\ref{tab:smith} uses a separate exhaustive Smith inventory of all $65{,}536$ matrices over $A$, including zero. Its support labels are assigned by Theorem~\ref{thm:trichotomy}; they are not direct support decisions on the entire population. The nonzero counts are $5{,}265$ local, $34{,}056$ logical but not strong, and $26{,}214$ strong. The direct dual-number check yields $81$, $72$ and $102$ respectively for its 255 nonzero matrices.

A separately supplied process-semantics implementation is included unchanged for an additional, scoped cross-check: its Smith types and independently computed regular-representation binary ranks are checked on all $65{,}536$ matrices over $A$. Its inventory agrees with the audit checker. This comparison does not constitute another full support classification or a rerun of every historical process-semantics suite.

From the extracted revision directory, run \texttt{python supplement/run\_reproduction.py}. The wrapper refuses optimized Python execution, runs the full stated population, compares substantive outputs with the supplied reference results, regenerates Table~\ref{tab:smith}, and writes commands, interpreter/platform, exit statuses, runtimes and SHA-256 hashes. Runtime and platform fields are excluded from substantive-output comparisons. The Boolean coefficient-support identity is analytic; no historical LM-product or missing canonical-runner result is claimed as reproduced here. These finite checks corroborate the proofs and do not certify historical priority.

''' + t[end:]
replace('Nonzero rank permits a logical obstruction;', 'At least two nonzero Smith factors permit a logical obstruction;')
replace('First, the nilpotent maximal-code example is a static nonprimitive resource, so it cannot by itself justify a closed process theory.',
        r'First, the nilpotent maximal-code example is a static nonprimitive resource, so it cannot by itself justify a closed process theory. For primitive resources, maximal orbit coding and universal raw teleportation coincide by Corollary~\ref{cor:primitive}.')
replace('The publication priority of the specific classification and exact orbit formula also remains subject to the unresolved source checks listed in the accompanying ledger; the paper claims the displayed proofs, not certified historical firstness.',
        'The contribution is the classification and the explicit comparison of resource criteria. The primary-source comparison is bounded; it does not certify historical firstness for the specific classification or orbit formula.')
start = t.index(r'\appendix')
end = t.index(r'\bibliographystyle{plain}', start)
t = t[:start] + t[end:]
(ROOT / 'manuscript/main.tex').write_text(t, encoding='utf-8', newline='\n')
print('Revised manuscript written; original retained.')
