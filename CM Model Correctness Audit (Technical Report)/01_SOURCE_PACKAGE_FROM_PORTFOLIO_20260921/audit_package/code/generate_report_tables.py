"""Deterministically produce the report tables from the audited CSV files."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parents[1]
def rows(name):
    with (ROOT/'data'/name).open() as f:return list(csv.DictReader(f))
def num(x):return f'{int(x):,}'
classes=rows('class_inventory_audited.csv');contexts=rows('contextuality_audited_15_classes.csv')
tex=[]
tex.append(r'''\subsection{All 15 structured classes}
\begin{longtable}{@{}ccrcccc@{}}
\caption{Complete structured family. The shared separability column refers to model \modelS; literal nonzero product states occur only at rank one. The zero vector is bookkeeping, not an allowed modal preparation.}\label{tab:classes}\\
\toprule $a$ & $b$ & Orbit size & Literal rank & Shared sep. & 192-basis status & Universal\\\midrule\endfirsthead
\toprule $a$ & $b$ & Orbit size & Literal rank & Shared sep. & 192-basis status & Universal\\\midrule\endhead''')
for r,c in zip(classes,contexts):
    status={'STRONG':'Strong','LOGICAL':'Logical','LOCAL':'Local','ZERO':'Excluded'}[c['status_192']]
    tex.append(f"{r['a']} & {r['b']} & {num(r['count'])} & {r['literal_rank']} & {'Yes' if r['shared_separable']=='1' else 'No'} & {status} & {'Yes' if r['universal_single_copy']=='1' else 'No'}\\\\")
tex.append(r'\bottomrule\end{longtable}')
tex.append(r'''\subsection{Exact contextuality coverage counts}
\begin{longtable}{@{}ccrrrc@{}}
\caption{Per-class counts in the complete 192-basis family, identical under the shared/literal setting relabeling. ``Extendable'' counts allowed joint sections having some compatible global assignment.}\label{tab:contexts}\\
\toprule $a$ & $b$ & Possible & Extendable & Uncovered & Status\\\midrule\endfirsthead
\toprule $a$ & $b$ & Possible & Extendable & Uncovered & Status\\\midrule\endhead''')
for r in contexts:
    status={'STRONG':'Strong','LOGICAL':'Logical','LOCAL':'Local','ZERO':'Excluded'}[r['status_192']]
    tex.append(f"{r['a']} & {r['b']} & {num(r['possible'])} & {num(r['extendable'])} & {num(r['uncovered'])} & {status}\\\\")
tex.append(r'\bottomrule\end{longtable}')
tex.append(r'''\subsection{Do not merge the two resource hierarchies}
\begin{longtable}{@{}ccrrrr@{}}
\caption{Largest exact families count vectors including zero. Subtract one for nonzero modal preparations. The last column is the minimum literal-copy count for \emph{heralded} extraction of $I_8$ under unrestricted local Boolean-linear processing.}\label{tab:hierarchy}\\
\toprule $a$ & $b$ & Rank & Shared exact & Literal exact & Literal copies\\\midrule\endfirsthead
\toprule $a$ & $b$ & Rank & Shared exact & Literal exact & Literal copies\\\midrule\endhead''')
for r in classes:
    tex.append(f"{r['a']} & {r['b']} & {r['literal_rank']} & {r['shared_max_exact_vectors']} & {r['literal_max_exact_subspace_vectors']} & {r['literal_activation_min_copies_rank_bound']}\\\\")
tex.append(r'\bottomrule\end{longtable}')
ledger=[
('CM/LM identities','16,384 truth-fusion, 512 alignment, 256 pairing cases','Confirmed','Native Boolean logic, not modal measurement.'),
('Packed Boolean kernel','All 256 pairs of 2x2 matrices; all 65,536 4x4 ranks and inverses; rectangular checks','Confirmed','Independent scalar and packed implementations.'),
('Rotation centralizer','All 65,536 binary 4x4 matrices','16 operators','Exactly the XOR span of I, P, P squared, P cubed.'),
('Rotation powers','Exact identities and ranks 4,3,2,1,0','Confirmed','Different types for the CM identity and its selected operator.'),
('Order-four minimum','All six GL2 maps; explicit 3x3 witness','Correction','Four is not the minimum arbitrary linear dimension.'),
('Gate inventory','All 65,536 phase-block gates','24,576 / 512','Invertible / Boolean-orthogonal; 128 monomial.'),
('Two-party separability','All 65,536 coefficient states and all 65,536 factor pairs','Confirmed','5,266 shared products including zero, versus 10 literal structured vectors of rank at most one.'),
('Local stabilizers','All 15 classes; exact relation-fiber counts','Confirmed','Orbit-stabilizer equality in GL2(A) squared.'),
('Basis-permutation gates','24 permutations on all 5,266 shared product vectors','16 entanglers','Not all possible two-party gates.'),
('Restricted contextuality','15 classes x 36,864 contexts x two models','Confirmed','Exact implication-closure coverage; not brute enumeration of 2^384 assignments.'),
('Shared/literal relation','Every restricted context; 8,640 direct effect-pair checks','Relabeling','Bob coefficient conjugation explains all table changes.'),
('Bell','Nine contexts, all 64 assignments','Contradiction','Modal local-assignment assumptions explicitly stated.'),
('GHZ','27 contexts, all 512 assignments; 101,583 subsets below six','Minimum six','Only this stated context family.'),
('Weighted GHZ','One specified literal lift; Z/X/Y and four orthogonal bases','Mixed','Local in the first family; logically contextual in the second.'),
('P and shear generation','Exact closure of P, inverse P, and T','20,160','All GL4; T leaves the commuting phase subalgebra.'),
('Shared teleportation','256 inputs x four outcomes','1,024 identities','Includes four null regressions; module preparation caveat remains.'),
('Literal teleportation','Two analyzers, each 256 inputs x 64 outcomes','32,768 identities','16,320 meaningful nonzero cases per analyzer.'),
('Direct branch formula','15 canonical plus 16 fixed-seed resources, all 64 branches','1,984 checks','Uses explicit full tensor matrices, including nonsymmetric resources.'),
('All resource ranks','65,536 resources x 64 branches','4,194,304 checks','No branch-rank mismatch.'),
('Reference preservation','64 corrected identity maps tensor I2','Confirmed','Proof extends to every reference dimension.'),
('Dense coding','64 encoded joint states and full inverse decoder','64/64','Basis rank 64; not a physical bandwidth claim.'),
('Old logical-only analyzer','Four labels, each with 16 phase sectors','Fails','Sixteen distinct rank-two Bob maps per logical label.'),
('Shared restricted transfer','983,040 correction fixed-space cases','Confirmed','256, 16, or one vector depending on class.'),
('Shared fixed quotient','983,040 analyzer-row solvability tests','4 / 2 / 3 labels','Scope permits arbitrary A-linear corrections; zero quotient is trivial.'),
('Literal restricted transfer','Rank 1 through 8, complete analyzers','32,640 checks','Attains all 2^r vectors in an r-dimensional subspace.'),
('Literal finite-copy activation','All 15 canonical classes; explicit filters','Positive','Two copies of rank six can heraldedly yield rank eight.'),
('Shared tensor closure','Explicit two nonzero factors','Fails','N cubed times N is zero under the shared tensor.'),
('Shared orthogonal rows','All 65,536 four-block rows','Zero correctable','Among rows meeting the necessary orthogonal condition.'),
('Orthogonal Bell basis','Even-dimensional hyperplane proof','No-go','Complete rank-one analyzer with all corrections orthogonal.'),
('Common bilinear form','All 65,536 four-dimensional forms','Only zero','No nondegenerate form preserves both P and T.'),
('No-cloning','Proof and all 256 basis-cloner inputs','Linear no-go','247 multi-support failures; coefficient copying remains possible.'),
('Probability extension','External real LP and exact affine solution','Fails faithfully','Six modal-possible events forced to zero by no-signalling.'),
('Historical regression','22 + 10 + 15 + 12 named tests','59 pass','Passing old tests does not certify their interpretation.'),
('New test suite','31 named independent tests','31 pass','In addition to all driver enumerations.'),
]
with (ROOT/'data/claim_ledger.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['claim','verified_universe','result','qualification']);w.writerows(ledger)
tex.append(r'''\subsection{Evidence ledger}
\small
\begin{longtable}{@{}L{29mm}L{53mm}L{21mm}L{45mm}@{}}
\caption{Executed universes and proof scopes. All counts are diagnostics, not amplitude values.}\\
\toprule Item & Universe or evidence & Result & Boundary\\\midrule\endfirsthead
\toprule Item & Universe or evidence & Result & Boundary\\\midrule\endhead''')
def esc(s):return s.replace('&',r'\&').replace('_',r'\_').replace('^384',r'\textsuperscript{384}').replace('2^r',r'$2^r$')
for row in ledger:tex.append(' & '.join(esc(s) for s in row)+r'\\')
tex.append(r'\bottomrule\end{longtable}\normalsize')
(ROOT/'paper/generated_tables.tex').write_text('\n'.join(tex)+'\n')
print('Generated report tables and',len(ledger),'ledger entries')

main=(ROOT/'paper/CM_Correctness_Audit.tex').read_text()
(ROOT/'paper/CM_Correctness_Audit_Standalone.tex').write_text(main.replace(r'\input{generated_tables.tex}',(ROOT/'paper/generated_tables.tex').read_text()))
