"""Recompute the archived P14 bootstrap intervals without its missing runtime.

This uses the archived analyzer's fixed seed, case/worker resampling order and
linear quantile rule. It reads raw rows from the preserved historical ZIP and
does not import or execute the historical compiler.
"""
from collections import defaultdict
from hashlib import sha256
import json
import math
from pathlib import Path
import random
import statistics
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE.parent / '02_CONTRACT_REVISION_20260926/reproducibility/historical_evidence.zip'
SEED = 2026091902
DRAWS = 10000


def quantile(values, p):
    values = sorted(values)
    x = (len(values) - 1) * p
    i = int(x)
    f = x - i
    return values[i] * (1 - f) + values[min(i + 1, len(values) - 1)] * f


def replay(rows, corpus, a, b, endpoint):
    subset = [r for r in rows if r['corpus'] == corpus and r['endpoint'] == endpoint and r['arm'] in (a, b)]
    groups = defaultdict(list)
    workers = defaultdict(set)
    worker_groups = defaultdict(list)
    families = {}
    for r in subset:
        c = r['case_id']
        w = (r['session'], r['worker'])
        groups[(c, r['arm'])].append(r['per_compile_ns'])
        workers[c].add(w)
        worker_groups[(c, r['arm'], w)].append(r['per_compile_ns'])
        families[c] = r['family']
    cases = sorted(families)
    assert all((c, a) in groups and (c, b) in groups for c in cases)
    med = {k: statistics.median(v) for k, v in groups.items()}
    fam_groups = defaultdict(list)
    for c in cases:
        fam_groups[families[c]].append(c)
    worker_medians = {k: statistics.median(v) for k, v in worker_groups.items()}
    workers = {c: sorted(v) for c, v in workers.items()}
    fams = sorted(fam_groups)
    rng = random.Random(SEED ^ sum(map(ord, corpus + a + b)))
    draws = []
    for _ in range(DRAWS):
        sampled_fams = [rng.choice(fams) for _ in fams]
        logs = []
        for family in sampled_fams:
            fc = fam_groups[family]
            for _ in fc:
                c = rng.choice(fc)
                w = rng.choice(workers[c])
                logs.append(math.log(worker_medians[c, a, w] / worker_medians[c, b, w]))
        draws.append(math.exp(statistics.mean(logs)))
    ratios = [med[c, a] / med[c, b] for c in cases]
    return {
        'corpus': corpus, 'endpoint': endpoint, 'comparison': f'{a}/{b}',
        'cases': len(cases), 'families': len(fams),
        'geomean': math.exp(statistics.mean(math.log(x) for x in ratios)),
        'ci95': [quantile(draws, .025), quantile(draws, .975)],
        'ci98_75': [quantile(draws, .00625), quantile(draws, .99375)],
    }


def main():
    with ZipFile(ARCHIVE) as z:
        manifest = json.loads(z.read('p14_original/P14_ARTIFACT_MANIFEST.json'))['files']
        checked = []
        for name in ['P14_RESULTS.json', 'P14_FREEZE.json', 'P14_ANALYSIS_EXECUTION_AMENDMENT.json',
                     'timing_s0_w0.json', 'timing_s1_w0.json', 'timing_s2_w0.json']:
            data = z.read('p14_original/' + name)
            assert sha256(data).hexdigest() == manifest[name]['sha256'], name
            checked.append(name)
        amendment = json.loads(z.read('p14_original/P14_ANALYSIS_EXECUTION_AMENDMENT.json'))
        assert sha256(z.read('p14_original/analyze_p14_optimized.py')).hexdigest() == amendment['execution_sha256']
        expected = json.loads(z.read('p14_original/P14_RESULTS.json'))
        rows = []
        for name in ['timing_s0_w0.json', 'timing_s1_w0.json', 'timing_s2_w0.json']:
            rows.extend(json.loads(z.read('p14_original/' + name))['rows'])
    comparisons = []
    for section, endpoint in [('comparisons', 'recipe'), ('secondary_ir', 'ir')]:
        for item in expected[section]:
            a, b = item['comparison'].split('/')
            actual = replay(rows, item['corpus'], a, b, endpoint)
            for field in ['cases', 'families']:
                assert actual[field] == item[field], (section, item['corpus'], item['comparison'], field)
            for field in ['geomean', 'ci95', 'ci98_75']:
                observed = actual[field]
                recorded = item[field]
                values = zip(observed, recorded) if isinstance(observed, list) else [(observed, recorded)]
                assert all(abs(x-y) < 1e-12 for x, y in values), (section, item['corpus'], item['comparison'], field)
            comparisons.append(actual)
    output = {
        'status': 'PASS', 'archive_sha256': sha256(ARCHIVE.read_bytes()).hexdigest(),
        'archived_files_verified': checked, 'archived_analyzer_sha256': amendment['execution_sha256'],
        'raw_rows': len(rows), 'draws_per_comparison': DRAWS,
        'comparison_count': len(comparisons), 'match_tolerance': 1e-12,
        'comparisons': comparisons,
        'scope': 'Reanalysis of archived raw rows only; historical imported compiler execution remains unverified.',
    }
    (HERE/'P14_BOOTSTRAP_REPLAY.json').write_text(json.dumps(output, indent=2)+'\n', encoding='utf-8')
    print(f"PASS: {len(comparisons)} P14 interval sets from {len(rows)} raw rows")


if __name__ == '__main__':
    main()
