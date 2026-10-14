"""Recount archived observations; never run timing workers or modify old records."""
import csv
import hashlib
import io
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent


def check():
    with ZipFile(ROOT / 'historical_evidence.zip') as z:
        recovery = json.loads((ROOT / 'HISTORICAL_RECOVERY.json').read_text())
        for item in recovery['members']:
            assert hashlib.sha256(z.read(item['recovered_member'])).hexdigest() == item['sha256']
        raw = z.read('s1_s2/results/raw/gate_a_s1_s2.csv')
        rows = list(csv.DictReader(io.StringIO(raw.decode())))
        admitted = [r for r in rows if r['all_arms_ok'] == '1' and r['correctness_status'] == 'OK']
        assert len(rows) == 10500 and len(admitted) == 10389
        families = Counter(r['family'] for r in admitted)
        assert families == {'S1': 3750, 'S2': 6639}
        assert all(r['correctness_status'] in ('OK', 'NO_SUCCESSFUL_ARM') for r in rows)
        fields = ('final_degree', 'final_monomials', 'multiplications', 'output_unique_nodes',
                  'pair_terms', 'peak_monomials', 'serialized_bytes')
        differences = {f: sum(r['cm_frontend_sparse_' + f] != r['generic_2support_sparse_' + f] for r in admitted) for f in fields}
        assert not any(differences.values())
        fold_wins = Counter('generic' if float(r['generic_2support_sparse_successful_folds']) > float(r['cm_frontend_sparse_successful_folds']) else
                            'cm' if float(r['generic_2support_sparse_successful_folds']) < float(r['cm_frontend_sparse_successful_folds']) else 'tie' for r in admitted)
        assert fold_wins['generic'] == 6010 and fold_wins['cm'] == 0
        arms = ('direct_sparse_anf', 'cse_flat_sparse', 'generic_2support_sparse', 'cm_frontend_sparse')
        failures = Counter('|'.join(r[a + '_status'] for a in arms) for r in rows if r['all_arms_ok'] != '1')
        assert failures == {'BUDGET|BUDGET|BUDGET|BUDGET': 108, 'BUDGET|BUDGET|OK|OK': 2, 'BUDGET|OK|BUDGET|BUDGET': 1}
        medians = {}
        for level, expected in [(0.0, [35, 35]), (0.25, [17, 12]), (0.5, [9, 0])]:
            subset = [r for r in admitted if r['family'] == 'S2' and float(r['shared_fraction_requested']) == level]
            medians[str(level)] = [statistics.median(float(r[a + '_multiplications']) for r in subset) for a in ('direct_sparse_anf', 'cm_frontend_sparse')]
            assert medians[str(level)] == expected

        timing = []
        for name in sorted(z.namelist()):
            if name.startswith('p14_original/timing_') and name.endswith('.json'):
                timing.extend(json.loads(z.read(name))['rows'])
        assert len(timing) == 51102
        archived = json.loads(z.read('p14_original/P14_RESULTS.json'))
        freeze = json.loads(z.read('p14_original/P14_FREEZE.json'))
        hashes = {**freeze['source_hashes'], **freeze['manifests']}
        for name, digest in hashes.items():
            assert hashlib.sha256(z.read('p14_original/' + name)).hexdigest() == digest
        estimates = []
        for corpus in ('synthetic', 'natural'):
            for numerator, denominator in (('E', 'F'), ('E', 'D')):
                groups = defaultdict(list)
                for r in timing:
                    if r['corpus'] == corpus and r['endpoint'] == 'recipe' and r['arm'] in (numerator, denominator):
                        groups[(r['case_id'], r['arm'])].append(r['per_compile_ns'])
                cases = sorted({c for c, _ in groups})
                assert len(cases) == (384 if corpus == 'synthetic' else 107)
                ratios = {c: statistics.median(groups[c, numerator]) / statistics.median(groups[c, denominator]) for c in cases}
                estimate = math.exp(statistics.mean(math.log(v) for v in ratios.values()))
                saved = next(r for r in archived['comparisons'] if r['corpus'] == corpus and r['comparison'] == numerator + '/' + denominator)
                assert math.isclose(estimate, saved['geomean'], rel_tol=1e-12)
                assert all(math.isclose(v, saved['case_ratios'][c], rel_tol=1e-12) for c, v in ratios.items())
                estimates.append({'corpus': corpus, 'comparison': numerator + '/' + denominator,
                                  'cases': len(cases), 'geomean_recomputed': estimate,
                                  'historical_ci98_75_not_recomputed': saved['ci98_75']})
    return {'status': 'PASS', 'recovered_member_hashes_checked': len(recovery['members']),
            's1_s2': {'raw_rows': len(rows), 'all_arm_rows': len(admitted), 'families': dict(families),
                      'seven_metric_differences': differences, 'fold_wins': dict(fold_wins),
                      'failure_patterns': dict(failures), 's2_sharing_medians_direct_cm': medians},
            'p14': {'raw_rows': len(timing), 'freeze_hashes_checked': len(hashes), 'primary_estimates': estimates,
                    'scope': 'Point estimates and all primary case ratios regenerated; bootstrap intervals read, not rerun. No new timings.'}}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
