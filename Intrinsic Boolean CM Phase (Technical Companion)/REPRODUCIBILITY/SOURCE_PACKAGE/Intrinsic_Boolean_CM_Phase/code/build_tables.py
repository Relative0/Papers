#!/usr/bin/env python3
"""Regenerate the two manuscript tables from retained machine-readable results."""
from pathlib import Path
import csv
import json
ROOT = Path(__file__).resolve().parents[1]
NAMES = {0:r'[0]',1:r'[\wedge]',2:r'[\Uparrow]',3:r'[L]',4:r'[\neg\vee]',5:r'[\Leftrightarrow]',6:r'[\neg R]',7:r'[\Leftarrow]',8:r'[\Downarrow]',9:r'[R]',10:r'[m]',11:r'[\vee]',12:r'[\neg L]',13:r'[\Rightarrow]',14:r'[\neg\wedge]',15:r'[T]'}

def main() -> None:
    with (ROOT/'data/elements.csv').open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    table = [r'\begin{center}\small', r'\begin{tabular}{@{}rlrrrrrrl@{}}', r'\toprule', r'Code & CM & $\wt$ & $\nu$ & Rank & Order & Nil. & Inverse code & $N_\star$\\\midrule']
    for row in rows:
        fields = [row['code'], '$'+NAMES[int(row['code'])]+'$', row['weight'], row['valuation'], row['rank'], row['order'] or '--', row['nilpotency'] or '--', row['inverse'] or '--', '$'+NAMES[int(row['norm'])]+'$']
        table.append(' & '.join(fields)+r'\\')
    table += [r'\bottomrule\end{tabular}', r'\end{center}']
    (ROOT/'scalar_table.tex').write_text('\n'.join(table)+'\n', encoding='utf-8')
    result = json.loads((ROOT/'data/verification.json').read_text(encoding='utf-8'))
    specs = [
        ('Independent scalar multiplication comparison','ring_pairs_independently_checked','All pairs'),
        ('Associativity/distributivity','ring_triples_associativity_distributivity','All triples'),
        ('Two-branch operator inventory','operators_tested','Complete universe'),
        ('States checked per operator','states_per_operator','Complete universe'),
        ('Independent binary rank calculations','independent_binary_rank_checks','All operators'),
        ('Invertible operators','invertible_operators','Rank and determinant agree'),
        ('Intrinsic unitary operators','intrinsic_unitaries','Exact ring test'),
        ('Nonmonomial intrinsic unitaries','nonmonomial_unitaries','Exact ring test'),
        ('Unitary involutions','unitary_involutions','Exact ring test'),
        ('Mixing unitary involutions','mixing_unitary_involutions','Exact ring test'),
        ('Global Hamming isometries','global_Hamming_isometries','All states'),
        ('Weight-four-shell preservers','Hamming_shell_preservers','All 70 shell states'),
        ('Shell/unitary intersection','unitary_and_Hamming_shell_intersection','Not the same sets'),
        ('Reversible splitters','reversible_splitters','Both output entries nonzero'),
        ('Detector-profile $(0,2,4,2)$ splitters','four_point_fringe_splitters','All phases'),
        ('Unitary interferometer checks','unitary_interferometer_norm_checks','Invariant component norms'),
        ('Two-bit single-CM DJ detectors','DJ_n2_single_CM_detectors','All weights searched'),
        ('Three-bit quotient-label search','DJ_n3_zero_sum_quotient_labelings','Zero-sum labelings'),
        ('Three-bit minimum detector channels','DJ_n3_minimum_linear_CM_channels','One impossible; two verified'),
        ('Phase-to-ANF truth functions','phase_anf_truth_functions_checked','$1\\le n\\le4$, zero mismatches'),
        ('Kickback branch checks','kickback_basis_checks','All functions through $n=3$'),
        ('Affine hidden-string cases','affine_cases','$1\\le n\\le6$, zero mismatches'),
        ('Marked-pattern cases','marked_cases','$1\\le n\\le6$, background corrected'),
        ('Distinct two-bit search patterns','two_bit_search_raw_unique','Same local splitter architecture'),
        ('Universal marked-coordinate peaks','two_bit_search_marked_peak','None in the tested architecture'),
        ('Local CM-to-ANF elementary cases','local_CM_ANF_cases','All CMs and Boolean inputs'),
        ('Random CM DAG internal nodes','random_CM_DAG_nodes_verified','50 DAGs; zero mismatches'),
        ('Pointwise CM folding valuations','pointwise_CM_folding_checks','All local triples and inputs'),
        ('Nilpotent-interaction regression circuits','nilpotent_interaction_circuits','Five oracle bits per circuit'),
        ('Independent-register/mask conjunctions','independent_register_and_mask_tag_checks','All two-bit assignments'),
        ('Subset-interval kernels','subset_interval_kernels_checked','All functions through $n=3$'),
        ('Subset-interval kernel product pairs','subset_interval_product_pairs','All pairs through $n=3$'),
    ]
    table = [r'\begin{longtable}{@{}L{0.48\textwidth}rL{0.31\textwidth}@{}}',r'\toprule Check or classification & Count & Scope\\\midrule\endhead']
    for label,key,scope in specs:
        table.append(f'{label} & {result[key]:,} & {scope}'+r'\\')
    table.append(r'\bottomrule\end{longtable}')
    (ROOT/'audit_table.tex').write_text('\n'.join(table)+'\n', encoding='utf-8')
    print('Generated scalar_table.tex and audit_table.tex from retained results.')

if __name__ == '__main__':
    main()
