"""Independent raw-row and arithmetic check of the frozen v5 run."""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path
from statistics import median


HERE = Path(__file__).resolve().parent
RUN = HERE / 'run_natural_timing_001'
CASES = HERE.parent / '04_NATURAL_CIRCUIT_EXTENSION_20260926' / 'NATURAL_CASES.jsonl'


def rows(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line]


def main():
    cases = rows(CASES)
    timing = rows(RUN / 'TIMING.jsonl')
    memory = rows(RUN / 'MEMORY.jsonl')
    abc = rows(RUN / 'ABC.jsonl')
    failures = rows(RUN / 'FAILURES.jsonl')
    analysis = json.loads((RUN / 'ANALYSIS.json').read_text(encoding='utf-8'))
    assert len(cases) == 71 and len({(c['design'], c['output']) for c in cases}) == 71
    design_counts = Counter(c['design'] for c in cases)
    assert len(design_counts) == 10 and sum(design_counts.values()) == 71
    assert len(timing) == 2100 and len(memory) == 142 and len(abc) == 1065
    assert len(failures) == 1 and failures[0]['case_index'] == 4
    assert failures[0]['stage'] == 'timing' and 'calibration shortfall' in failures[0]['error']
    timing_groups = defaultdict(list)
    for row in timing:
        i = row['case_index']
        assert row['design'] == cases[i]['design']
        assert row['source_output'] == cases[i]['output']
        assert row['per_call_ns'] == row['sum_ns'] / row['inner_calls']
        assert row['inner_calls'] > 0 and row['sum_ns'] > 0
        timing_groups[(i, row['arm'])].append(row)
    complete = []
    for i in range(71):
        for arm in ('CM_hybrid_fallback', 'direct_packed'):
            group = timing_groups[(i, arm)]
            assert len(group) == (0 if i == 4 else 15)
            assert sorted(r['repetition'] for r in group) == ([] if i == 4 else list(range(15)))
        if i != 4:
            cm = median(r['per_call_ns'] for r in timing_groups[(i, 'CM_hybrid_fallback')])
            direct = median(r['per_call_ns'] for r in timing_groups[(i, 'direct_packed')])
            recorded = analysis['cases'][i]
            assert abs(recorded['ratio_direct_over_cm'] - direct / cm) < 1e-12
            complete.append(direct / cm)
    assert abs(median(complete) - analysis['all_complete_case_median_direct_over_cm']) < 1e-12
    memory_counts = Counter((r['case_index'], r['arm']) for r in memory)
    assert all(memory_counts[(i, arm)] == 1 for i in range(71)
               for arm in ('CM_hybrid_fallback', 'direct_packed'))
    abc_counts = Counter(r['case_index'] for r in abc)
    assert all(abc_counts[i] == 15 for i in range(71))
    for row in abc:
        i = row['case_index']
        assert row['design'] == cases[i]['design']
        assert row['source_output'] == cases[i]['output']
        assert row['truth_sha256'] == cases[i]['source_truth_sha256']
        assert row['abc_return_code'] == 0
    for name, expected in analysis['raw_sha256'].items():
        assert sha256((RUN / name).read_bytes()).hexdigest() == expected
    assert analysis['counts']['python_complete_cases'] == 70
    assert analysis['counts']['abc_complete_cases'] == 71
    print(json.dumps({'status': 'PASS', 'selected_designs': len(design_counts),
                      'selected_cases': len(cases), 'timed_cases': 70,
                      'calibration_failure_case_index': 4,
                      'abc_correct_cases': 71, 'median_direct_over_cm': median(complete)},
                     indent=2))


if __name__ == '__main__':
    main()
