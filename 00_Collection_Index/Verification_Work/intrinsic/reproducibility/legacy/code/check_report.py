#!/usr/bin/env python3
"""Independently reaggregate the retained audit and verify binary unitarity.

Uses Python's standard library only. Does not import the experiment module.
This is a separate implementation check, not external third-party replication.
"""
from pathlib import Path
from collections import Counter
import csv
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[1]

def regular_rows(a: int) -> list[int]:
    """Circulant rows, constructed directly from the four coefficient bits."""
    return [sum(((a >> ((row-col) % 4)) & 1) << col for col in range(4)) for row in range(4)]

def check() -> dict:
    data = ROOT/'data'
    result = json.loads((data/'verification.json').read_text(encoding='utf-8'))
    digest = hashlib.sha256((ROOT/'code/verify_intrinsic.py').read_bytes()).hexdigest()
    if digest != result['script_sha256']:
        raise AssertionError('Experiment script differs from the recorded execution hash. Rerun it.')
    counts = Counter()
    seen = set()
    for row in csv.DictReader((data/'operators.csv').open(newline='', encoding='utf-8')):
        v = {k:int(x) for k,x in row.items()}
        tup = tuple(v[k] for k in ('a','b','c','d'))
        if tup in seen:
            raise AssertionError('Duplicate operator record')
        seen.add(tup)
        blocks = [regular_rows(a) for a in tup]
        binary_rows = [blocks[0][j] | (blocks[1][j] << 4) for j in range(4)]
        binary_rows += [blocks[2][j] | (blocks[3][j] << 4) for j in range(4)]
        # rho(U^dagger) = rho(U)^T, so ordinary binary orthogonality is
        # an independent check of the ring-unitary flag for every operator.
        orthogonal = all(((binary_rows[i]&binary_rows[j]).bit_count() & 1)==int(i==j) for i in range(8) for j in range(8))
        if orthogonal != bool(v['unitary']):
            raise AssertionError(f'Binary orthogonality disagrees at {tup}')
        counts['operators_tested'] += 1
        for source,target in [('invertible','invertible_operators'),('unitary','intrinsic_unitaries'),('hamming_global','global_Hamming_isometries'),('hamming_shell','Hamming_shell_preservers'),('splitter','reversible_splitters'),('fringe_0242','four_point_fringe_splitters')]:
            counts[target] += v[source]
        counts['unitary_and_Hamming_shell_intersection'] += v['unitary']*v['hamming_shell']
        monomial = (v['b']==0 and v['c']==0) or (v['a']==0 and v['d']==0)
        counts['nonmonomial_unitaries'] += v['unitary']*int(not monomial)
        counts['unitary_involutions'] += v['unitary']*v['involution']
        counts['mixing_unitary_involutions'] += v['unitary']*v['involution']*int(not monomial)
        if bool(v['invertible']) != (v['binary_rank']==8):
            raise AssertionError('Rank/determinant mismatch in stored data')
    if len(seen)!=16**4 or any(not 0 <= k < 16 for tup in seen for k in tup):
        raise AssertionError('Operator universe is incomplete')
    for key,value in counts.items():
        if result[key] != value:
            raise AssertionError(f'Aggregate mismatch: {key}: {value} != {result[key]}')
    expected = {'intrinsic_unitaries':512,'nonmonomial_unitaries':384,'unitary_involutions':96,'mixing_unitary_involutions':72,'invertible_operators':24576,'global_Hamming_isometries':32,'Hamming_shell_preservers':512,'unitary_and_Hamming_shell_intersection':256,'reversible_splitters':22528,'four_point_fringe_splitters':8192,'phase_anf_truth_functions_checked':65812,'affine_cases':252,'marked_cases':126,'local_CM_ANF_cases':64,'random_CM_DAG_nodes_verified':1500,'subset_interval_product_pairs':65808,'subset_interval_kernels_checked':276}
    for key,value in expected.items():
        if result[key] != value:
            raise AssertionError(f'Manuscript value mismatch: {key}')
    for file,key,column in [('phase_anf_exhaustive.csv','phase_anf_truth_functions_checked','functions'),('affine_hidden_strings.csv','affine_cases','functions'),('marked_pattern_decoding.csv','marked_cases','marks')]:
        records=list(csv.DictReader((data/file).open(newline='',encoding='utf-8')))
        if sum(int(r[column]) for r in records)!=result[key] or any(int(r.get('mismatches','0')) for r in records):
            raise AssertionError(f'Regression summary mismatch in {file}')
    return {'status':'PASS','operators_reaggregated':len(seen),'independent_binary_orthogonality_checks':len(seen),'manuscript_count_checks':len(expected),'experiment_script_sha256':digest,'scope':'Independent implementation and aggregation; not third-party replication'}

if __name__=='__main__':
    try:
        checked=check()
    except (AssertionError,OSError,ValueError,KeyError) as exc:
        print(f'REPORT CHECK FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
    (ROOT/'data/report_check.json').write_text(json.dumps(checked,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(checked,indent=2))
